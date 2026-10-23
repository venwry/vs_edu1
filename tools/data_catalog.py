"""Resolve canonical records into deterministic compatibility views. No model calculations."""
import argparse, copy, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text())

def write(path, value):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def manifest():
    return read('data/manifest.json')

def resolve(node, stack=()):
    if isinstance(node, list):
        return [resolve(x, stack) for x in node]
    if not isinstance(node, dict):
        return node
    if set(node) == {'$source'}:
        path = node['$source']
        if path in stack:
            raise ValueError('Circular source reference: ' + path)
        if not (ROOT/path).resolve().is_relative_to(ROOT):
            raise ValueError('Source path outside repository')
        return resolve(read(path)['data'], (*stack, path))
    if set(node) == {'$merge'}:
        result = {}
        for part in node['$merge']:
            part = resolve(part, stack)
            overlap = result.keys() & part.keys()
            if overlap:
                raise ValueError('Duplicate field ownership: ' + str(overlap))
            result.update(part)
        return result
    return {k: resolve(v, stack) for k, v in node.items()}

def build(check=False):
    m = manifest()
    for output, template in m['documents'].items():
        value = resolve(template)
        if check:
            if read(output) != value:
                raise ValueError('Stale compatibility view: ' + output)
        else:
            write(output, value)
    return len(m['documents'])

def store_document(path, value):
    """Legacy mutation bridge: update owned source fields atomically, then rebuild.

    Existing records/fields only. New entities must be authored and registered explicitly;
    refusing an unknown shape prevents a legacy script from silently losing data.
    """
    m = manifest()
    if path not in m['documents']:
        write(path, value)
        return
    changes = {}
    def distribute(template, incoming):
        if isinstance(template, dict) and set(template) == {'$source'}:
            name = template['$source']; record = copy.deepcopy(read(name))
            # Sources with nested ownership must be updated through their nested template.
            if contains_directive(record['data']):
                distribute(record['data'], incoming)
            else:
                record['data'] = incoming
                if name in changes and changes[name] != record:
                    raise ValueError('Conflicting writes to shared source: ' + name)
                changes[name] = record
        elif isinstance(template, dict) and set(template) == {'$merge'}:
            if set(incoming) != set(resolve(template)):
                raise ValueError('Register added/removed fields in data/manifest.json first: ' + path)
            for part in template['$merge']:
                keys = resolve(part).keys()
                distribute(part, {k: incoming[k] for k in keys})
        elif isinstance(template, list):
            if len(template) != len(incoming):
                raise ValueError('Register added/removed records in data/manifest.json first: ' + path)
            old_records = [resolve(t) for t in template]
            if all(isinstance(r, dict) and 'id' in r for r in old_records):
                by_id = {r['id']: t for r, t in zip(old_records, template)}
                if set(by_id) != {r.get('id') for r in incoming}:
                    raise ValueError('Register added/removed record IDs in manifest first')
                template[:] = [by_id[r['id']] for r in incoming]
            for before, after in zip(template, incoming):
                old = resolve(before)
                if isinstance(old,dict) and 'id' in old and old['id'] != after.get('id'):
                    raise ValueError('Record order/identity changed; update manifest explicitly')
                distribute(before, after)
        elif isinstance(template, dict):
            if set(template) != set(incoming):
                raise ValueError('Unexpected document structure: ' + path)
            for key in template:
                distribute(template[key], incoming[key])
        elif template != incoming:
            raise ValueError('Cannot overwrite literal manifest value')
    distribute(m['documents'][path], value)
    # Validate all proposed writes before persisting any of them.
    import jsonschema
    for name, record in changes.items():
        schema = (ROOT/name).parent / record['$schema']
        from schema_validation import record_validator
        record_validator(json.loads(schema.read_text())).validate(record)
    for name, record in changes.items():
        write(name, record)
    write('data/manifest.json', m)
    build()

def contains_directive(value):
    if isinstance(value,dict):
        return '$source' in value or '$merge' in value or any(contains_directive(v) for v in value.values())
    return isinstance(value,list) and any(contains_directive(v) for v in value)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print(('Checked' if args.check else 'Built'), build(args.check), 'compatibility views')

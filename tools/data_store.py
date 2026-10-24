"""Read the single authoritative collection layer; legacy shapes exist only in memory."""
import copy, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def registry(root=ROOT):
    return json.loads((Path(root)/'schemas/data-registry.json').read_text())

def view_name(path, root=ROOT):
    reg=registry(root); path=str(path).removeprefix('./')
    path=reg['legacy_paths'].get(path,path)
    name=Path(path).stem
    return name if (path.startswith('generated/catalogs/') or path.startswith('catalog:')) and name in reg['views'] else (path[8:] if path.startswith('catalog:') and path[8:] in reg['views'] else None)

def normalize_component_ids(value, root=ROOT):
    """Translate archival IDs and composite map keys in memory; preserve all numbers."""
    reg=registry(root);aliases={**reg.get('component_id_aliases',{}),**reg.get('device_assembly_aliases',{})}
    families=reg.get('device_family_aliases',{})
    def translate(v):
        if isinstance(v,str):
            if v in aliases:return aliases[v]
            return '|'.join(aliases.get(p,p) for p in v.split('|')) if '|' in v else v
        if isinstance(v,list):return [translate(x) for x in v]
        if isinstance(v,dict):
            out={}
            for k,x in v.items():
                key=translate(k)
                if key in out:raise ValueError('Component identifier collision: '+key)
                out[key]=translate(x)
            if out.get('catalog_ref') in families and out.get('id') in families[out['catalog_ref']]:out['catalog_ref']=out['id']
            return out
        return v
    return translate(value)

def assembly_records(stored, devices):
    """Build the runtime BOM index from its sole source owners; never persist copies."""
    rows=copy.deepcopy(stored)
    rows.extend({'id':d['id'],**copy.deepcopy(d['bom_assembly_metadata']),'lines':copy.deepcopy(d['bom_assembly_definition'])} for d in devices if 'bom_assembly_definition' in d)
    if len({r['id'] for r in rows})!=len(rows):raise ValueError('Duplicate device/assembly BOM identity')
    return rows

def read_document(path, root=ROOT):
    root=Path(root);reg=registry(root);name=view_name(path,root)
    if name is None:
        actual=reg['legacy_paths'].get(str(path),str(path))
        value=json.loads((root/actual).read_text())
        return normalize_component_ids(value,root) if actual.startswith('generated/models/') else value
    cache={}
    def collection(file):
        if file not in cache:cache[file]=json.loads((root/file).read_text())
        return cache[file]
    def select(ref):
        rows=collection(ref['file'])[ref['key']]
        return assembly_records(rows,collection(ref['device_file'])['devices']) if ref.get('device_file') else copy.deepcopy(rows)
    recipe=reg['views'][name]
    if recipe.get('story'):
        world=collection('data/world.json');structure=collection('data/timeline-structure.json')
        events={e['id']:e for e in collection('data/events.json')['events']};contracts=collection('data/contracts.json')
        phases=[]
        for phase in structure['phases']:
            p=copy.deepcopy(phase);ids=p.pop('event_refs');p['events']=[]
            for id in ids:
                e=copy.deepcopy(events[id]);contract=e.pop('agreement_ref',None)
                if contract is not None:e['agreement_terms']=copy.deepcopy(contracts[contract])
                p['events'].append(e)
            phases.append(p)
        return {'assumptions':{k:copy.deepcopy(world[k]) for k in ['scenario','entities','principles','conventions']},'phases':phases,'processes':copy.deepcopy(structure['processes'])}
    if 'merge' in recipe:
        result={}
        for ref in recipe['merge']:
            part=select(ref)
            if result.keys() & part.keys():raise ValueError('Overlapping field ownership: '+name)
            result.update(part)
        return result
    return {key:select(ref) for key,ref in recipe.items()}

def document_text(path, root=ROOT):
    if view_name(path,root):return json.dumps(read_document(path,root),indent=2,ensure_ascii=False)+'\n'
    return (Path(root)/registry(root)['legacy_paths'].get(str(path),str(path))).read_text()

def document_bytes(path, root=ROOT):
    if view_name(path,root):return document_text(path,root).encode()
    return (Path(root)/registry(root)['legacy_paths'].get(str(path),str(path))).read_bytes()

def store_document(path, value, root=ROOT):
    """Write edits back to their sole collection owners; no catalogue is materialised."""
    root=Path(root);reg=registry(root);name=view_name(path,root)
    if name is None:
        actual=reg['legacy_paths'].get(str(path),str(path))
        if actual in reg['files']:
            from validate_data import validate_collections
            validate_collections(root,{actual:value})
        target=root/actual;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n');return
    changes={}
    def assign(ref,payload):
        file=ref['file']
        if file not in changes:changes[file]=json.loads((root/file).read_text())
        if ref.get('device_file'):
            device_file=ref['device_file']
            if device_file not in changes:changes[device_file]=json.loads((root/device_file).read_text())
            devices={d['id']:d for d in changes[device_file]['devices'] if 'bom_assembly_definition' in d}
            owned=[r for r in payload if r['id'] in devices]
            if len(owned)!=len(devices) or {r['id'] for r in owned}!=set(devices):raise ValueError('Device BOMs must be edited at their existing owners')
            for row in owned:
                device=devices[row['id']];device['bom_assembly_definition']=copy.deepcopy(row['lines'])
                device['bom_assembly_metadata']=copy.deepcopy({k:v for k,v in row.items() if k not in ['id','lines']})
            payload=[r for r in payload if r['id'] not in devices]
            if any(r['id'].startswith('device.') for r in payload):raise ValueError('Add device BOMs in data/devices.json')
        changes[file][ref['key']]=copy.deepcopy(payload)
    recipe=reg['views'][name]
    if recipe.get('story'):
        world={k:value['assumptions'][k] for k in ['scenario','entities','principles','conventions']}
        for k,v in world.items():assign({'file':'data/world.json','key':k},v)
        phases=[];events=[];contracts=json.loads((root/'data/contracts.json').read_text())
        for phase in value['phases']:
            p=copy.deepcopy(phase);evs=p.pop('events');p['event_refs']=[]
            for event in evs:
                e=copy.deepcopy(event);p['event_refs'].append(e['id'])
                if 'agreement_terms' in e:
                    contracts[e['id']]=e.pop('agreement_terms');e['agreement_ref']=e['id']
                events.append(e)
            phases.append(p)
        changes['data/contracts.json']=contracts
        assign({'file':'data/events.json','key':'events'},events)
        assign({'file':'data/timeline-structure.json','key':'phases'},phases)
        assign({'file':'data/timeline-structure.json','key':'processes'},value['processes'])
    elif 'merge' in recipe:
        remaining=set(value)
        for ref in recipe['merge']:
            existing=json.loads((root/ref['file']).read_text())[ref['key']]
            if not set(existing)<=set(value):raise ValueError('Missing owned fields: '+name)
            assign(ref,{k:value[k] for k in existing});remaining-=set(existing)
        if remaining:raise ValueError('Assign new programme fields to an explicit collection owner: '+str(remaining))
    else:
        if set(value)!=set(recipe):raise ValueError('Unexpected catalogue fields: '+name)
        for k,ref in recipe.items():assign(ref,value[k])
    from validate_data import validate_collections
    validate_collections(root,changes)
    for file,payload in changes.items():(root/file).write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')

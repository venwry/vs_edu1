"""Validate authoritative records, schemas, deterministic views and immutable baselines."""
import hashlib,json,sys
from pathlib import Path
import jsonschema
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools'))
from data_catalog import build, manifest, read, resolve
from schema_validation import record_validator
m=manifest();build(check=True)
seen={};sources=set()
def visit(x):
 if isinstance(x,dict):
  if set(x)=={'$source'}:sources.add(x['$source'])
  for v in x.values():visit(v)
 elif isinstance(x,list):
  for v in x:visit(v)
visit(m['documents'])
for name in sorted(sources):
 record=read(name)
 key=(record['record_type'],record['id'])
 # Document sections intentionally share a document ID; their ownership is by path.
 if record['record_type']!='document-section':
  assert key not in seen,(key,seen.get(key),name)
  seen[key]=name
 schema=((R/name).parent/record['$schema']).resolve()
 assert schema.is_relative_to(R/'schemas'),name
 validator=record_validator(json.loads(schema.read_text()))
 validator.validate(record)
for folder in ('data','site/config'):
 for path in (R/folder).rglob('*.json'):
  if path.name=='manifest.json':continue
  assert str(path.relative_to(R)) in sources,('Unregistered source',path)
assert not list(R.glob('*.json')),'Root JSON data files must be migrated'
for old,path in m['paths'].items():assert (R/path).is_file(),(old,path)
# Ensure the assembled catalog's established references and schema are still available.
jsonschema.Draft202012Validator(read('schemas/legacy/logix_aion_story.schema.json')).validate(read(m['paths']['logix_aion_story.json']))
jsonschema.Draft202012Validator(read('schemas/legacy/hardware_bom.schema.json')).validate(read(m['paths']['hardware_bom.json']))
# Financial baselines must not drift when reorganizing or rebuilding views.
frozen=read('tests/migration-baseline.json')['semantic_sha256']
for old,path in m['paths'].items():
 if path.startswith('baselines/'):
  h=hashlib.sha256(json.dumps(read(path),sort_keys=True,ensure_ascii=False).encode()).hexdigest()
  assert h==frozen[old],('Frozen baseline changed',path)
print(f'PASS: {len(sources)} canonical records, schemas, views and immutable baselines')

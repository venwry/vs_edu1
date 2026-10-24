"""One-time identity migration audit: physical BOMs and archived economics are unchanged."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from data_store import read_document,registry,normalize_component_ids
from validate_data import validate_collections
fixture=read_document('tests/fixtures/component-migration.json')
digest=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
validate_collections()
rows=read_document('data/components.json')['components'];ids={x['id'] for x in rows}
assert len(rows)==len(ids)==287
assert 'components' not in read_document('data/sourcing.json')
assert 'base_parts' not in read_document('data/components.json')
assert sum(x['bom_role']=='material' for x in rows)==279
assert sum(x['bom_role']=='assembly' for x in rows)==4
assert sum(x['bom_role']=='specification' for x in rows)==4
for x in rows:
 assert not {'catalog_ref','unit_cost','currency','quote_date','quantity_tier','manufacturing_requirements'}&x.keys()
 assert not any(k in x.get('specification',{}) for k in ['access_time_ns','cycle_time_ns','refresh_requirement','bare_tube_ordering_code'])
assert sum(bool(x.get('manufacturer_part_number')) for x in rows)==7
aliases=registry()['component_id_aliases'];assert len(aliases)==279 and set(aliases.values())<=ids
assert len(set(aliases.values())&set(fixture['former_base_ids']))==33
for path,expected in fixture['frozen_files'].items():
 assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path+' archival bytes changed'
 raw=json.loads((ROOT/path).read_text());normalized=read_document(path)
 if path.startswith('generated/models/'):
  assert normalized==normalize_component_ids(raw),path
  assert normalize_component_ids(normalized)==normalized,'Adapter is not idempotent'
  # Numbers must remain equal, including ordering and null/boolean distinction.
  def numbers(v):
   if isinstance(v,dict):return [n for x in v.values() for n in numbers(x)]
   if isinstance(v,list):return [n for x in v for n in numbers(x)]
   return [v] if type(v) in (int,float) else []
  assert numbers(raw)==numbers(normalized),path+' numbers changed'
# Device ownership was migrated subsequently; its independently derived fingerprints
# replace the older whole-view hashes while keeping the component identity/archive checks.
for name,expected in read_document('tests/fixtures/device-migration.json')['expected_views'].items():
 value=read_document('catalog:'+name)
 if name=='hardware-bom':value['assemblies'].sort(key=lambda r:r['id'])
 assert digest(value)==expected,name
# Fail safely rather than silently overwrite a collision in a component-keyed cost map.
try:normalize_component_ids({'bompart.part.z80a':1,'part.z80a':2})
except ValueError:pass
else:raise AssertionError('Colliding model IDs accepted')
print('PASS: 287 components, canonical references, preserved physical assemblies and 25 expected views, and all archived values/bytes')

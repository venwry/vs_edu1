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
assert len(rows)==len(ids)==350
assert 'components' not in read_document('data/sourcing.json')
assert 'base_parts' not in read_document('data/components.json')
assert sum(x['bom_role']=='material' for x in rows)==348
assert sum(x['bom_role']=='assembly' for x in rows)==0
assert sum(x['bom_role']=='specification' for x in rows)==2
for x in rows:
 assert not {'catalog_ref','unit_cost','currency','quote_date','quantity_tier','manufacturing_requirements'}&x.keys()
 assert not any(k in x.get('specification',{}) for k in ['access_time_ns','cycle_time_ns','refresh_requirement','bare_tube_ordering_code'])
assert sum(bool(x.get('manufacturer_part_number')) for x in rows)==10
aliases=registry()['component_id_aliases'];assert len(aliases)==280 and set(aliases.values())<=ids|{d['id'] for d in read_document('data/devices.json')['devices']}|set(registry()['record_family_aliases'])
assert len(aliases)==len(set(aliases))
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
# Whole-view fingerprints are superseded by validate_chassis_migration.py.
# Fail safely rather than silently overwrite a collision in a component-keyed cost map.
try:normalize_component_ids({'bompart.part.z80a':1,'part.z80a':2})
except ValueError:pass
else:raise AssertionError('Colliding model IDs accepted')
print('PASS: canonical component roles, archive values/bytes and alias collision rejection')

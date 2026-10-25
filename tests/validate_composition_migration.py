"""Structural migration invariants and read-only cutover simulation checks."""
import copy,hashlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from completion_audit import historical_bom
from data_store import read_document,registry,project_collections
from validate_products import validate_products
from validate_data import validate_collections
from simulate_compositions import simulate
validate_collections()
source={f:read_document(f) for f in registry()['files']};ds=source['data/devices.json']['devices'];ps=source['data/product-catalog.json']['products']
assert len(ds)==60 and len(ps)==63
assert len([d for d in ds if d['category']=='base_computer'])==6
assert not any(p['id'].startswith('computer.') for p in ps)
assert 'external_platforms' not in source['data/product-catalog.json']
assert len(source['data/ecosystem-inputs.json']['external_platforms'])==1
assert not any('bom_assembly_definition' in d or d['id'].startswith('device.chassis.') for d in ds)
assert len([d for d in ds if not d['composition_history']])==2
assert all(h['valid_from']==d['introduced']['event_start_date'] for d in ds for h in d['composition_history'])
assert all(h['valid_to']=='1990-01-01' for d in ds for h in d['composition_history'])
assert len([d for d in ds if d['introduced']['event_start_date']=='1982-06-07'])==5
assert len(source['data/assemblies.json']['assemblies'])==28
assert len(source['data/retired_assemblies.json']['assemblies'])==19
assert not ({a['id'] for a in source['data/assemblies.json']['assemblies']} & {a['id'] for a in source['data/retired_assemblies.json']['assemblies']})
fixture=read_document('tests/fixtures/composition-migration.json')
digest=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
bom=historical_bom(read_document('catalog:hardware-bom'));assert {a['id']:digest(a['lines']) for a in bom['assemblies']}==fixture['assembly_lines'],'Production BOM changed during simulation-only migration'
for path,h in fixture['financial_files'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==h,path
before={p:p.read_bytes() for p in (R/'data').glob('*.json')}
r=simulate();assert all(p.read_bytes()==b for p,b in before.items())
assert r['summary']['compared_versions']==27 and r['summary']['full_cutover_equal']==26
assert any(f['kind']=='full_cutover_inventory_change' and f['owner']=='offer.comdex82_artemis_autocad' for f in r['findings'])
assert r['summary']['findings_by_kind'].get('unknown_start_date',0)==0
# Ref uniqueness, flat products, version ordering and cycles are strict source invariants.
def reject(fn):
 docs=copy.deepcopy(source);p=next(p for p in docs['data/product-catalog.json']['products'] if p['id']=='bundle.artemis_128_mono');fn(p,docs)
 try:validate_products(docs,{})
 except ValueError:return
 raise AssertionError('Invalid composition accepted')
reject(lambda p,d:p['composition_history'][0]['composition_definition'].append(copy.deepcopy(p['composition_history'][0]['composition_definition'][0])))
reject(lambda p,d:p['composition_history'][0]['composition_definition'][0].update(ref='bundle.aurelia_mono'))
reject(lambda p,d:p['composition_history'][1].update(valid_from=p['composition_history'][0]['valid_from']))
reject(lambda p,d:p['composition_history'][1].update(version_number=1))
reject(lambda p,d:d['data/devices.json']['devices'][0]['composition_history'][0]['composition_definition'][0].update(ref=d['data/devices.json']['devices'][0]['id']))
reject(lambda p,d:p['composition_history'][0]['composition_definition'][0].update(quantity=None))
# Unknown proposal dates remain unresolved rather than fabricated launch dates.
assert all(h.get('date_status')=='unknown' for p in ps for h in p['composition_history'] if h['valid_from'] is None)
print('PASS: versioned owners, flat products, archive partition, 97 historical BOMs after validated delivery-scope deltas; unchanged finances, negative validation and read-only simulation')

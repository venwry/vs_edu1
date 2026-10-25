"""Approved design quantities, version metadata ownership and single-drive layouts."""
import copy,json,hashlib,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from data_store import read_document,registry
from validate_data import validate_collections
from validate_products import validate_products
from simulate_compositions import simulate
from completion_audit import historical_bom
validate_collections()
source={f:read_document(f) for f in registry()['files']}
D={d['id']:d for d in source['data/devices.json']['devices']};P={p['id']:p for p in source['data/product-catalog.json']['products']};C={c['id']:c for c in source['data/components.json']['components']}
def lines(d):return {l['ref']:l for l in d['composition_history'][0]['composition_definition']}
assert not {'offer.retail.connected_office','offer.retail.development_team','bundle.proposed_artemis_pro_small_office'}&P.keys()
assert 'part.athena.hdd' not in C and registry()['component_id_aliases']['part.athena.hdd']=='part.hdd_5mb'
assert C['part.hdd_5mb']['introduced']['event_start_date']=='1980-07-15'
assert lines(D['device.athena.hdd'])['part.hdd_5mb']['quantity']==1
for id in ['product.artemis_budget_128_hdd','product.athena','product.athena_server']:
 for v in P[id]['composition_history']:
  storage=[l for l in v['composition_definition'] if D.get(l['ref'],{}).get('category') in ['floppy_drive_mechanism','hard_disk_drive']]
  assert sum(l['quantity'] for l in storage if D[l['ref']]['category']=='floppy_drive_mechanism')==1
  assert sum(l['quantity'] for l in storage if D[l['ref']]['category']=='hard_disk_drive')==1
assert P['product.artemis_budget_128_hdd']['composition_history'][0]['valid_from']=='1980-11-19'
for id in ['device.base_computer.artemis','device.base_computer.artemis_pro']:
 assert lines(D[id])['part.artemis_dma']['quantity']==1
for d in D.values():
 if d['composition_history']:
  assert 'bom_assembly_metadata' not in d
  assert all('bom_assembly_metadata' in h for h in d['composition_history'])
 if d['category']=='base_computer':assert sum(l['quantity'] for l in lines(d).values() if l['ref'].endswith('.controller_cable'))==1
 if d['category']=='floppy_drive_mechanism':assert not any(l.endswith('.controller_cable') for l in lines(d))
 if d['id']=='device.flexibus_keyboard':
  assert d['specification']['key_count']==104
  for suffix in ['key_switches','keycaps','matrix_diodes']:assert lines(d)['part.device.flexibus_keyboard.'+suffix]['quantity']==104
for suffix in ['aurelia','artemis']:
 d=D['device.network_card_'+suffix]
 assert lines(d)['part.logix_network_cable']['quantity']==1
 assert any(ref.endswith('.delivery_set') for ref in lines(d))
 assert len(lines(P['product.'+suffix+'_network_upgrade']))==2
for p in P.values():
 for h in p['composition_history']:assert not any(l['ref']=='part.logix_supplemental_distribution_media' for l in h['composition_definition'])
# Metadata belongs to an explicit version; removing it must fail.
docs=copy.deepcopy(source);docs['data/devices.json']['devices'][0]['composition_history'][0].pop('bom_assembly_metadata')
try:validate_products(docs,{})
except ValueError:pass
else:raise AssertionError('Missing manufacturing metadata accepted')
r=simulate();s=r['summary'];assert s['compared_versions']==72 and s['unchanged_versions']==64
assert s['unknown_components']==37
assert s['findings_by_kind']=={'inventory_change':8}
historical_bom(read_document('catalog:hardware-bom'))
f=read_document('tests/fixtures/composition-migration.json')
for path,h in f['financial_files'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==h
print('PASS: approved quantities, unique version metadata, 1 FDD + 1 HDD layouts, network delivery, removal scope, simulation and immutable finances')

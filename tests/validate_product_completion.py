"""Approved snapshot-based definitions and explicit device delivery scope."""
import copy,json,hashlib,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from data_store import read_document
from validate_data import validate_collections
from completion_audit import historical_bom
from simulate_compositions import simulate
validate_collections()
load=lambda f:json.loads((R/f).read_text())
ps={p['id']:p for p in load('data/product-catalog.json')['products']};ds={d['id']:d for d in load('data/devices.json')['devices']};cs={c['id']:c for c in load('data/components.json')['components']}
f=load('tests/fixtures/product-completion.json');assert len(f['added_parts'])==54 and len(f['superseded_parts'])==17
assert all(cs[id]['vendor']=='Logix' and cs[id]['bom_role']=='material' for id in f['added_parts'])
assert all(cs[id]['production_status']=='excluded' for id in f['superseded_parts'])
retail=load('generated/models/retail-catalog-1982-results.json')['snapshots'];pricing={p['id']:p for p in load('generated/models/pricing-results.json')['products']}
for p in ps.values():
 if not p['id'].startswith('bundle.proposed_'):continue
 name=pricing[p['id']]['name']
 dates=[dt for dt,s in retail.items() if name in s['announced_offers'] or any(l['ref']==p['id'] for l in s['current_offer_prices']) or any(l['ref']==p['id'] for c in s['solutions']+s['upgrades'] for l in c['pricing']['lines'])]
 assert p['introduced']['event_start_date']==min(dates)==p['composition_history'][0]['valid_from']
 assert 'not the conference opening date' in p['introduced']['timeline_note']
 assert not any(h.get('unresolved_items') for h in p['composition_history'])
for d in ds.values():
 for h in d['composition_history']:
  lines={l['ref']:l for l in h['composition_definition']}
  if d['category'] in ['base_computer','monitor']:
   keys=['documentation','mains_cable','packout']+(['signal_cable'] if d['category']=='monitor' else [])
   for key in keys:assert lines['part.'+d['id']+'.'+key]['quantity']==1
   assert not set(lines)&set(f['superseded_parts'])
  if d['category']=='floppy_drive_mechanism':assert lines['part.'+d['id']+'.controller_cable']['quantity'] is None
for id in ['offer.retail.connect_office','offer.retail.cpm_migration']:
 h=ps[id]['composition_history'][0];assert h['composition_status']=='unresolved'
 assert h['composition_definition'] and all(l['quantity'] is None and l['condition']!='always' for l in h['composition_definition'])
network=ps['bundle.proposed_artemis_pro_small_office'];assert network['catalogue_status']=='announced';assert network['commercial_terms']['shipping_date'] is None
lines={l['ref']:l for l in network['composition_history'][0]['composition_definition']}
assert lines['part.logix_network_cable']['quantity']==3
assert lines['edition.bpi_client_server.era_client']['quantity']==2
assert lines['device.base_computer.artemis']['quantity']==2 and lines['device.base_computer.artemis_pro']['quantity']==1
for file in ['data/assemblies.json','data/retired_assemblies.json']:
 assert not any(l['ref'].startswith('assembly.') for a in load(file)['assemblies'] for l in a['lines'])
# Validate each approved changed owner, then compare all 97 pre-change assembly fingerprints.
b=historical_bom(read_document('catalog:hardware-bom'));old=load('tests/fixtures/composition-migration.json')
digest=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert {a['id']:digest(a['lines']) for a in b['assemblies']}==old['assembly_lines']
for path,h in old['financial_files'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==h
r=simulate();assert not any(x['kind'] in ['unknown_start_date','child_date_coverage','unresolved_package'] for x in r['findings'])
assert r['summary']['full_cutover_equal']==26 and r['summary']['findings_by_kind']['quotation_scope_unresolved']==2
assert {line:sum(p['computer_line']==line for p in ps.values()) for line in ['Aurelia','Artemis','Athena']}=={'Aurelia':4,'Artemis':8,'Athena':2}
print('PASS: snapshot-derived dates, flat resolved packages, announced status, 54 delivery parts, no duplicate packout, scoped unknowns and unchanged financial files')

from data_paths import read_document, document_bytes, document_text
from data_paths import resolve_path
"""Cross-model checks for the DRI, NCC 1979 cards and independent sourcing revision."""
import hashlib, json, math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return read_document(n, root=R)
s=read('generated/catalogs/logix-aion-story.json');t=read('generated/catalogs/logix-aion-technical-catalog-v2.json');b=read('generated/catalogs/hardware-bom.json');c=read('generated/models/manufacturing-costs.json');p=read('generated/catalogs/manufacturing-programs.json')
e={e['id']:e for phase in s['phases'] for e in phase['events']}
r={x['id']:x for v in t.values() if isinstance(v,list) for x in v if isinstance(x,dict) and 'id' in x}
a={x['id']:x for x in b['assemblies']};cost={x['id']:x for x in c['products']}
assert e['event.dri_founding']['date']=={'start':'1974','end':'1974'}
assert e['event.smc_agreement']['date']=={'start':'1978-07','end':'1978-07'}
assert e['event.smc_sales']['date']=={'start':'1979-10','end':'1979-10'}
assert e['event.dri_cpm']['date']['start']=='1976-09-01'
assert 'event.dri_founding' in e['event.dri_cpm']['related_event_refs']
assert sum(x['value'] for x in e['event.dri_founding']['agreement_terms'] if x['type']=='equity')==100
fund=p['dri_founding'];assert fund['initial_paid_in_usd']+fund['scheduled_balance_usd']==fund['committed_capital_usd']==250000
cards=['device.s100_flexibus_card','device.apple2_video_card','device.s100_video_card']
assert set(cards)<=set(e['event.apple_extensions']['product_refs'])
for id in cards:
 assert r[id]['introduced']['event_start_date']=='1979-06-04'
 assert cost[id]['snapshots']['1978']['total_usd'] is None
 assert cost[id]['snapshots']['1979']['total_usd']>0
 assert all(x['actor_ref']!='actor.dri' for x in e['event.apple_extensions']['participants'])
assert not any('6502' in id for id in r if id.startswith('software.'))
for id in cards[1:]:
 lines={x['ref']:x['quantity'] for x in a['assembly.'+id]['lines']}
 assert lines['bompart.part.aion_4116']==8
 assert lines['bompart.part.aurelia_video_chip']==1
 inv={x['component_ref']:x['quantity'] for x in cost[id]['snapshots']['1979']['bom_lines']}
 assert inv['bompart.part.aion_4116']==8
 assert inv['bompart.part.aurelia_video_chip']==1
for id in ['device.apple2_expansion_card','device.s100_flexibus_card']:
 inv={x['component_ref']:x['quantity'] for x in cost[id]['snapshots']['1979']['bom_lines']}
 assert inv['bompart.part.flexibus_host_controller']==2
 assert not any('controller_and_two_port' in x for x in inv)
prog=p['smc_transfer'];assert set(prog['licensed_part_refs'])==set(b['supplier_programs'][0]['part_refs'])
assert 'part.era1' not in prog['licensed_part_refs']
for k in ['low','central','high']:assert sum(x[k+'_usd'] for x in prog['nre_items'])==prog['nre_total_usd'][k]
for x in c['supplier_scenarios']['chips']:
 assert x['snapshots']['1979']['purchase_price_usd'] is None
for alt in c['supplier_scenarios']['cards']:
 assert alt['snapshots']['1979']['total_usd'] is None
 for y in ['1980','1981']:
  v=alt['snapshots'][y];base=cost[alt['catalog_ref']]['snapshots'][y]
  assert math.isclose(sum(v['breakdown_usd'].values()),v['total_usd'],abs_tol=.011)
  assert math.isclose(v['total_usd']-base['total_usd'],v['delta_vs_aion_base_usd'],abs_tol=.011)
  # Internal fabrication labor disappears for replaced chips; purchase price is material.
  assert v['breakdown_usd']['workforce']<base['breakdown_usd']['workforce']
  assert v['breakdown_usd']['bom_materials']>base['breakdown_usd']['bom_materials']
for file,digest in c['metadata']['source_sha256'].items():assert hashlib.sha256(document_bytes(resolve_path(file), root=R)).hexdigest()==digest
print('PASS: partial dates, founding capital, all three launch offers, exact silicon quantities, deferred 6502, SMC date gates and replacement costs, NRE separation and generated-input hashes.')

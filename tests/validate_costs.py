from pathlib import Path
import json,math,subprocess,sys
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
d=read('manufacturing_costs.json');c=read('logix_aion_technical_catalog_v2.json');b=read('hardware_bom.json')
rows=d['products'];by={p['id']:p for p in rows};assert len(by)==len(rows)
covered={p['catalog_ref'] for p in rows};excluded={p['catalog_ref'] for p in d['coverage_exclusions']}
for group in ['computers','devices','software_products','services','offered_bundles','base_parts','technologies','proposed_bundles']:
 for p in c[group]:assert (p['id'] in covered) != (p['id'] in excluded),p['id']
assert {e['id'] for e in c['platform_editions']}<=by.keys()
assert all(p['id'] in by for p in c['offered_bundles'])
for p in rows:
 assert set(p['snapshots'])=={'1978','1979','1980','1981'}
 for year,s in p['snapshots'].items():
  if p['available_from']>year+'-06-15':assert s['status']=='not_yet_offered' and s['total_usd'] is None
  elif s['total_usd'] is not None:
   assert math.isclose(sum(s['breakdown_usd'].values()),s['total_usd'],abs_tol=.011),p['id']
   assert 0<=s['low_usd']<=s['total_usd']<=s['high_usd']
   assert all(v>=0 for v in s['breakdown_usd'].values())
   for line in s['bom_lines']:
    assert line['quantity']>0
    amount=sum(d['component_cost_assumptions'][line['component_ref']]['annual_cost_buckets_usd'][year].values())*line['quantity']
    assert abs(round(amount,2)-line['extended_recurring_cost_usd'])<.011
# Exact snapshot cutoffs and significant scenario dimensions.
assert by['computer.aurelia_plus']['snapshots']['1979']['total_usd'] is None
assert by['software.abacus_3']['snapshots']['1980']['total_usd'] is None
assert by['device.apple2_expansion_card']['snapshots']['1979']['total_usd']>0
assert by['service.bpi_training']['snapshots']['1978']['total_usd']>0
assert by['bundle.artemis_pro_1mb_server']['snapshots']['1981']['status']=='announced_shipping_unconfirmed'
def inv(id,y):return {x['component_ref']:x['quantity'] for x in by[id]['snapshots'][str(y)]['bom_lines']}
assert inv('computer.aurelia',1978)['bompart.part.dram_16kbit']==24
assert inv('computer.aurelia',1978)['bompart.part.vram_16kbit_dual_port']==8
assert inv('computer.aurelia',1978)['bompart.part.flexibus_host_controller']==3
assert inv('bundle.artemis_pro_1mb_server',1981)['bompart.part.dram_64kbit']==128
assert inv('bundle.artemis_pro_1mb_server',1981)['bompart.device.network_card_artemis.network_card_pcb']==1
assert inv('bundle.artemis_128_mono',1981)['bompart.device.network_card_artemis.network_card_pcb']==1
assert not any(k.startswith('bompart.software.aionix.') for k in inv('bundle.artemis_128_mono',1981))
assert any(k.startswith('bompart.software.aionix_server.') for k in inv('bundle.artemis_128_mono',1981))
assert not any(k.startswith('bompart.computer.') for k in inv('bundle.aurelia_network_upgrade',1981))
assert by['bundle.aurelia_mono']['snapshots']['1978']['breakdown_usd']['included_service_delivery']>0
# The assessment does not turn assumptions into manufacturing facts.
assert all(x['unit_cost'] is None for x in b['components'])
assert all(x['cost_rollup_status'].startswith('blocked') for x in b['assemblies'])
print(f'PASS: {len(rows)} cost rows, complete offering coverage, arithmetic, dates, NIC/OS single counting, 1 MiB RAM and preserved engineering unknowns.')

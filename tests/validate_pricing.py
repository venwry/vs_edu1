import json, math, hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'pricing_results.json').read_text());c=json.loads((R/'manufacturing_costs.json').read_text());costs={x['id']:x for x in c['products']}
rows={x['id']:x for x in p['products']}
assert len(rows)==len(p['products'])==91
assert p['metadata']['cost_model_sha256']==hashlib.sha256((R/'manufacturing_costs.json').read_bytes()).hexdigest()
count=0
for x in rows.values():
 assert x['offering_end'] is None
 for y,s in x['snapshots'].items():
  if s['date']<x['offering_start']:
   assert s['retail_price_usd'] is None;continue
  count+=1;price=s['retail_price_usd'];cost=s['manufacturing_cost_usd'];fee=s['computerland_fee_rate']
  assert abs(s['computerland_fee_usd']-round(price*fee,2))<.011
  assert abs(s['revenue_after_fee_usd']-(price-s['computerland_fee_usd']))<.011
  assert abs(s['unit_profit_usd']-(s['revenue_after_fee_usd']-cost))<.011
  assert price+0.01>=s['price_floor_usd']
  assert abs(s['stress']['profit_usd']-round(price*.9*(1-s['stress']['fee_rate'])-cost*1.2,2))<.011
  proxy=s['competitor']['normalized_price_usd']; balance=s['pricing_balance']
  margin=100*s['unit_profit_usd']/s['revenue_after_fee_usd']
  assert abs(margin-balance['margin_pct'])<.011
  if proxy and cost/(1-fee)<=proxy:
   assert balance['status']=='balanced_proxy'
   assert abs(margin-100*(1-price/proxy))<=.1
   assert abs(price-math.sqrt(cost*proxy/(1-fee)))<=.02
  elif proxy:
   assert balance['status']=='cost_floor_above_proxy'
   assert -.001<=s['unit_profit_usd']<=.02 and price>proxy
  else:
   assert balance['status']=='no_proxy_cost_based'
   assert abs(margin-25)<=.1 and balance['discount_pct'] is None
  if 'before_you_buy_variant' in s:
   v=s['before_you_buy_variant']; credit=v['voucher_face_value_usd']
   net=v['retail_price_usd']*(1-fee)
   assert abs(v['contribution_after_full_voucher_usd']-(net-cost-credit))<.02
   target=100*(1-v['retail_price_usd']/proxy) if proxy else 25
   assert abs(100*v['contribution_after_full_voucher_usd']/net-target)<.1
  assert abs(sum(v['extended_cost_usd'] for v in s['cost_components'])-cost)<.011
  assert abs(sum(s['cost_breakdown_usd'].values())-cost)<.08
  for part in s['cost_components']:
   ref=part['cost_ref']
   if ref in costs:assert part['unit_cost_usd']==costs[ref]['snapshots'][y]['total_usd']
  for eid in s['competitor']['evidence_refs']:
   e=p['competitor_evidence'][eid];assert p['sources'][e['source_ref']]['date']<=s['date'],(eid,y)
  if x['announced_only']:assert s['status']=='announced_shipping_unconfirmed'
  if x['channel']=='direct':assert fee==0
assert count==323
assert rows['bundle.aurelia_plus_mono']['snapshots']['1979']['retail_price_usd'] is None
assert rows['software.abacus_3']['snapshots']['1980']['retail_price_usd'] is None
assert rows['bundle.proposed_artemis_office']['snapshots']['1980']['cost_components'][-1]['cost_ref']=='edition.abacus_2.era'
assert rows['bundle.proposed_artemis_office']['snapshots']['1981']['cost_components'][-1]['cost_ref']=='software.abacus_3'
network=rows['bundle.proposed_artemis_pro_small_office']['snapshots']['1981']
assert {x['cost_ref']:x['quantity'] for x in network['cost_components']}['bundle.artemis_128_mono']==2
assert all(x['cost_ref']!='device.network_card_artemis' for x in network['cost_components'])
assert rows['service.academy_customer_site']['snapshots']['1981']['manufacturing_cost_usd']==round(73.85*8,2)
assert not any(x.startswith('part.') or x.startswith('computer.') for x in rows)
print('PASS: 91 offers / 323 snapshots; date gates, source chronology, exact cost reconciliation, fees, margins, stress and bundle dependencies.')



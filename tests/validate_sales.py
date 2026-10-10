import json,hashlib,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
s=read('sales_forecast.json');p=read('pricing_results.json');b=read('pricing_baseline.json');site=read('site_pages.json')
assert s['metadata']['source_pricing_sha256']==hashlib.sha256((R/'pricing_results.json').read_bytes()).hexdigest()
assert p['metadata']['baseline_sha256']==hashlib.sha256((R/'pricing_baseline.json').read_bytes()).hexdigest()
for offer in p['products']:
 for year,x in offer['snapshots'].items():
  if x['retail_price_usd'] is None:continue
  old=b['products'][offer['id']][year]
  assert abs(x['unit_profit_usd']-.6*old['unit_profit_usd'])<.011
  assert x['manufacturing_cost_usd']==old['manufacturing_cost_usd']
  assert x['computerland_fee_rate']==old['computerland_fee_rate']
  if 'before_you_buy_variant'in x:
   v=x['before_you_buy_variant'];ov=old['before_you_buy_variant']
   assert abs(v['retail_price_usd']-x['manufacturing_cost_usd']-.6*(ov['retail_price_usd']-x['manufacturing_cost_usd']))<.011
for sc in s['scenarios']:
 for key,rows in [('calendar_1978',sc['months'][:7]),('launch_year',sc['months'])]:
  a=sc[key];assert sum(x['units'] for x in rows)==a['units']
  assert a['expanded_market_units']==a['baseline_market_units']+a['new_or_accelerated_logix_purchases']+a['halo_competitor_purchases']
  assert a['diverted_purchases']+a['new_or_accelerated_logix_purchases']==a['units']
  assert abs(a['unit_market_share_pct']-a['units']/a['expanded_market_units']*100)<.006
  for k in ['customer_retail_spend_usd','supplier_revenue_after_channel_usd','recurring_cost_usd','unit_contribution_total_usd']:assert math.isclose(sum(x[k] for x in rows),a[k],abs_tol=.011)
 assert sc['months'][-1]['cumulative_units']==sc['launch_year']['units']
 assert sc['launch_year']['units']<=sc['delivery_capacity_units']
central=next(x for x in s['scenarios'] if x['id']=='central');assert central['calendar_1978']['units']==10350 and central['launch_year']['units']==28200
assert 'pricing' in site['navigation'] and 'sales' in site['navigation']
print('PASS: proportional reduction against immutable baseline, cost/fee preservation, course variants, forecast hashes, period totals, capacity, market denominators and navigation configuration.')

import json,hashlib,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
s=read('sales_forecast.json');p=read('pricing_results.json');b=read('pricing_baseline.json');site=read('site_pages.json')
assert s['metadata']['source_pricing_sha256']==hashlib.sha256((R/'pricing_results.json').read_bytes()).hexdigest()
assert p['metadata']['baseline_sha256']==hashlib.sha256((R/'pricing_baseline.json').read_bytes()).hexdigest()
b['products'].update(read('compatibility_pricing_baseline.json')['products'])
for offer in p['products']:
 for year,x in offer['snapshots'].items():
  if x['retail_price_usd'] is None:continue
  if offer['id'] not in b['products']:
   assert x['baseline_status']=='new_offer_no_historical_sales_anchor'
   assert 'no historical' in x['pre_reduction']['basis'].lower()
   continue
  old=b['products'][offer['id']][year]
  assert x['pricing_balance']['status'] in ('balanced_proxy','no_proxy_cost_based','cost_floor_above_proxy')
  assert x['cost_revision']['baseline_manufacturing_cost_usd']==old['manufacturing_cost_usd']
  assert abs(x['manufacturing_cost_usd']-old['manufacturing_cost_usd']-x['cost_revision']['delta_usd'])<.011
  assert x['computerland_fee_rate']==old['computerland_fee_rate']
  if 'before_you_buy_variant'in x:
   v=x['before_you_buy_variant'];ov=old['before_you_buy_variant']
   assert v['contribution_after_full_voucher_usd']>=0
for sc in s['scenarios']:
 for key,rows in [('calendar_1978',sc['months'][:7]),('launch_year',sc['months'])]:
  a=sc[key];assert sum(x['units'] for x in rows)==a['units']
  assert a['expanded_market_units']==a['baseline_market_units']+a['new_or_accelerated_logix_purchases']+a['halo_competitor_purchases']
  assert a['diverted_purchases']+a['new_or_accelerated_logix_purchases']==a['units']
  assert abs(a['unit_market_share_pct']-a['units']/a['expanded_market_units']*100)<.006
  for k in ['customer_retail_spend_usd','supplier_revenue_after_channel_usd','recurring_cost_usd','unit_contribution_total_usd']:assert math.isclose(sum(x[k] for x in rows),a[k],abs_tol=.011)
 assert sc['months'][-1]['cumulative_units']==sc['launch_year']['units']
 assert sc['launch_year']['units']<=sc['delivery_capacity_units']
ratio=s['pricing_comparison']['revised_complete_package_usd']/s['pricing_comparison']['previous_complete_package_usd']
for sc in s['scenarios']:
 expected=min(round(22000*ratio**(-sc['elasticity_assumption'])/1000)*1000,sc['delivery_capacity_units'])
 assert sc['pre_reaction_units']==expected
 for row in sc['months']:
  assert row['units']==max(0,row['pre_reaction_units']-row['apple_displacement_units']-row['tandy_deferred_units']+row['compatibility_gain_units'])+row['bpi_gain_units']
assert 'pricing' in site['navigation'] and 'sales' in site['navigation']
print('PASS: balanced pricing against immutable demand baseline, explicit cost rebase and fee preservation, course variants, forecast hashes, period totals, capacity, market denominators and navigation configuration.')

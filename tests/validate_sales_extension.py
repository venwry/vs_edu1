"""Period boundaries, price timing, stock-flow conservation and independent receipts."""
import hashlib,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
f=json.loads((R/'sales_forecast.json').read_text());p=json.loads((R/'pricing_results.json').read_text());offers={x['id']:x for x in p['products']}
assert f['metadata']['source_campaign_sha256']==hashlib.sha256((R/'ncc_1979_campaign.json').read_bytes()).hexdigest()
assert f['metadata']['forecast_end']=='1979-11-30'<f['metadata']['aurelia_plus_launch']=='1979-12-03'
policy=f['post_ncc_policy']
for year in ['1978','1979']:
 assert math.isclose(policy['complete_package_'+year+'_usd'],sum(offers[r]['snapshots'][year]['retail_price_usd'] for r in f['pricing_comparison']['references']),abs_tol=.001)
for s in f['scenarios']:
 rows=s['post_ncc_months'];assert len(rows)==6 and len(s['months'])==12
 opening=s['reaction_components']['bpi_capacity_deferred'];cumulative=s['launch_year']['units']
 for i,r in enumerate(rows):
  assert r['month']==f'1979-{i+6:02}' and r['aurelia_plus_units']==0
  assert r['opening_unmet_units']==opening
  assert r['returning_demand_units']+r['lapsed_demand_units']==opening
  assert r['new_demand_units']+r['returning_demand_units']==r['units']+r['unmet_demand_units']
  assert r['units']==min(r['demand_including_returning_units'],r['delivery_capacity_units'])
  assert r['new_demand_units']==r['baseline_demand_units']+r['price_gain_units']+sum(v if k.endswith('gain') else -v for k,v in r['effects'].items())
  cumulative+=r['units'];assert cumulative==r['cumulative_units'];opening=r['unmet_demand_units']
  w=.1 if i==0 else 0;assert r['old_price_fraction']==w
  for k in r['average_sale']:
   expected=round(w*policy['average_sale_by_price_year']['1978'][k]+(1-w)*policy['average_sale_by_price_year']['1979'][k],2)
   assert expected==r['average_sale'][k]
  assert abs(r['customer_retail_spend_usd']-r['units']*r['average_sale']['retail_price_usd'])<.011
  b=r['bpi'];assert b['customer_installations']==b['single_accounting_licenses']+b['four_module_customers']+b['complete_suite_licenses']
  assert abs(b['bpi_receipts_after_channel_usd']-.75*b['retail_spend_usd'])<.011
 for key,rr in [('june_november_1979',rows),('calendar_1979_through_november',s['months'][7:]+rows),('launch_through_november_1979',s['months']+rows)]:
  a=s[key];assert a['units']==sum(x['units'] for x in rr)
  for k in ['customer_retail_spend_usd','supplier_revenue_after_channel_usd','recurring_cost_usd','unit_contribution_total_usd']:assert abs(a[k]-sum(x[k] for x in rr))<.011
  for k in a['bpi']:assert abs(a['bpi'][k]-sum(x['bpi'][k] for x in rr))<.011
 a=s['june_november_1979'];assert a['opening_unmet_units']+a['new_demand_units']==a['units']+a['lapsed_demand_units']+a['ending_unmet_units']
print('PASS: November forecast boundary, June price timing, monthly capacity, demand conservation and independent BPI receipts.')

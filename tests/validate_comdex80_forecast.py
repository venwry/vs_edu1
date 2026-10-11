"""Check horizon continuity, model queues, financial baskets and launch claim limits."""
import json,hashlib,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
f=read('sales_forecast.json');c=read('ncc_1980_campaign.json');p={x['id']:x for x in read('pricing_results.json')['products']}
assert f['metadata']['forecast_end']=='1980-11-18'<f['metadata']['comdex1980_date']=='1980-11-19'
assert f['metadata']['source_ncc1980_campaign_sha256']==hashlib.sha256((R/'ncc_1980_campaign.json').read_bytes()).hexdigest()
assert c['launch_date']=='1980-05-19' and c['benchmark']['measured_results'] is None
assert c['compatibility_policy']['supported_through']=='2000-12-31'
assert c['presentation'][0]['start_minute']==0 and c['presentation'][-1]['end_minute']==55
assert all(a['end_minute']==b['start_minute'] for a,b in zip(c['presentation'],c['presentation'][1:]))
fields={'customer_retail_spend_usd':'retail_price_usd','supplier_revenue_after_channel_usd':'revenue_after_fee_usd','recurring_cost_usd':'manufacturing_cost_usd','unit_contribution_total_usd':'unit_profit_usd'}
for kind,parts in f['comdex1980_policy']['components'].items():
 for value in fields.values():assert math.isclose(f['comdex1980_policy']['average_sale_1980'][kind][value],round(sum(p[x['product_ref']]['snapshots']['1980'][value]*x['quantity'] for x in parts),2),abs_tol=.001)
for s in f['scenarios']:
 rows=s['ncc_to_comdex1980_months'];assert len(rows)==7
 queues={k:s['comdex_to_ncc1980_months'][-1]['products'][k]['unmet_demand_units'] for k in ['aurelia','aurelia_plus']};queues['artemis']=0
 cum=s['launch_through_ncc1980']['units']
 assert rows[0]['period_start']=='1980-05-19' and rows[-1]['period_end']=='1980-11-18'
 for i,r in enumerate(rows):
  assert r['month_fraction']==(13/31 if i==0 else 18/30 if i==6 else 1)
  assert sum(x['intending_buyers'] for x in r['products'].values())==r['buyer_pool_before_price_response']
  for kind,x in r['products'].items():
   assert x['opening_unmet_units']==queues[kind]
   assert x['returning_demand_units']+x['lapsed_demand_units']==queues[kind]
   assert x['new_demand_units']+x['returning_demand_units']==x['units']+x['unmet_demand_units']
   assert x['units']<=x['delivery_capacity_units'];queues[kind]=x['unmet_demand_units']
   avg=f['ncc1980_policy']['average_sale_by_computer'][kind] if i==0 and kind!='artemis' else f['comdex1980_policy']['average_sale_1980'][kind]
   for a,b in fields.items():assert math.isclose(x[a],round(x['units']*avg[b],2),abs_tol=.001)
  assert r['units']==sum(x['units'] for x in r['products'].values())
  assert r['new_demand_units']==sum(x['new_demand_units'] for x in r['products'].values())
  cum+=r['units'];assert cum==r['cumulative_units']
  assert math.isclose(r['bpi']['bpi_receipts_after_channel_usd'],round(r['bpi']['retail_spend_usd']*.75,2),abs_tol=.001)
 a=s['ncc_to_comdex1980'];assert cum==s['launch_through_comdex1980']['units']
 assert a['units']==sum(r['units'] for r in rows)==sum(a[k+'_units'] for k in queues)
 for field in fields:
  assert math.isclose(a[field],sum(r[field] for r in rows),abs_tol=.011)
  assert math.isclose(s['launch_through_comdex1980'][field],s['launch_through_ncc1980'][field]+a[field],abs_tol=.011)
 assert len(s['academy_months'])==12
print('PASS: COMDEX cutoff, launch commitments, exclusive buyer cohorts, delivery queues, prices and financial aggregation.')

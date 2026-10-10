"""Product queues, partial periods, course-day constraints and receipt boundaries."""
import hashlib,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
f=read('sales_forecast.json');p={x['id']:x for x in read('pricing_results.json')['products']}
assert f['metadata']['forecast_end']=='1980-05-18'<f['metadata']['ncc1980_date']=='1980-05-19'
assert f['metadata']['source_comdex_campaign_sha256']==hashlib.sha256((R/'comdex_1979_campaign.json').read_bytes()).hexdigest()
for sc in f['scenarios']:
 rows=sc['comdex_to_ncc1980_months'];assert len(rows)==6
 cumulative=sc['launch_through_november_1979']['units'];queues={'aurelia':sc['june_november_1979']['ending_unmet_units'],'aurelia_plus':0}
 for i,r in enumerate(rows):
  assert r['month_fraction']==(18/31 if i==5 else 1)
  assert r['units']==sum(x['units'] for x in r['products'].values())
  assert r['new_demand_units']==sum(x['new_demand_units'] for x in r['products'].values())
  for kind,x in r['products'].items():
   assert x['opening_unmet_units']==queues[kind]
   assert x['returning_demand_units']+x['lapsed_demand_units']==queues[kind]
   assert x['new_demand_units']+x['returning_demand_units']==x['units']+x['unmet_demand_units']
   assert x['units']<=x['delivery_capacity_units'];queues[kind]=x['unmet_demand_units']
  cumulative+=r['units'];assert cumulative==r['cumulative_units']
  assert r['applications']['pulse_licenses_on_new_aurelia_plus']<=r['products']['aurelia_plus']['units']
  assert math.isclose(r['bpi']['bpi_receipts_after_channel_usd'],r['bpi']['retail_spend_usd']*.75,abs_tol=.011)
 a=sc['comdex_to_ncc1980'];assert a['units']==sum(x['units'] for x in rows)
 assert a['opening_unmet_units']+a['new_demand_units']==a['units']+a['lapsed_demand_units']+a['ending_unmet_units']
 assert cumulative==sc['launch_through_ncc1980']['units']
 assert a['aurelia_units']+a['aurelia_plus_units']==a['units']
 assert a['abacus2_existing_owner_licenses']<=sc['launch_through_november_1979']['units']
 for field in ['customer_retail_spend_usd','supplier_revenue_after_channel_usd','recurring_cost_usd','unit_contribution_total_usd']:
  assert abs(a[field]-sum(r[field] for r in rows))<.011
  assert abs(sc['launch_through_ncc1980'][field]-sc['launch_through_november_1979'][field]-a[field])<.011
 waiting=0
 for r in sc['academy_months']:
  assert r['opening_unmet_requests']==waiting
  assert r['returning_requests']+r['lapsed_requests']==waiting
  assert r['new_requests']==sum(r['drivers'].values())
  assert r['new_requests']+r['returning_requests']==r['enrolments']+r['unmet_requests']
  waiting=r['unmet_requests'];assert r['enrolments']==sum(x['enrolments'] for x in r['courses'].values())
  assert r['scheduled_teaching_days']==sum(x['teaching_days'] for x in r['courses'].values())<=r['available_teaching_days']
  assert r['available_teaching_days']<=min(r['rooms']*18,r['instructors']*15)*r['month_fraction']
  for kind,x in r['courses'].items():
   assert x['enrolments']<=x['requested_enrolments'] and x['enrolments']<=x['classes']*6
   assert x['teaching_days']==x['classes']*f['academy_demand_policy']['course_days'][kind]
  if r['month']<'1979-12':assert r['courses']['pulse']['enrolments']==0
 for k,rr in [('academy_to_ncc1980',sc['academy_months']),('academy_comdex_to_ncc1980',sc['academy_months'][6:])]:
  a=sc[k];assert a['enrolments']==sum(x['enrolments'] for x in rr)
  assert a['opening_unmet_requests']+a['new_requests']==a['enrolments']+a['lapsed_requests']+a['ending_unmet_requests']
# Existing products retain 1979 prices; Plus mix uses only explicit new-product proxies.
for c in f['ncc1980_policy']['plus_components']:
 assert p[c['product_ref']]['snapshots'][str(c['snapshot_year'])]['retail_price_usd'] is not None
assert f['ncc1980_policy']['average_sale_by_computer']['aurelia']==f['post_ncc_policy']['average_sale_by_price_year']['1979']
print('PASS: NCC cutoff, product/Academy queue conservation, capacity, course durations, Pulse platform and price basis.')

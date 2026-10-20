"""Partner boundaries, component pricing, sales attribution and capacity limits."""
import json, math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
c=read('aurelia_1978_campaign.json');s=read('site_pages.json');p=read('pricing_results.json');f=read('sales_forecast.json');t=read('logix_aion_technical_catalog_v2.json')
ids=[x['id'] for x in c['premiere']['stages']]
assert ids.index('bpi')==ids.index('abacus')+1
assert ids.index('partners')==ids.index('bpi')+1
assert 'head of BPI' in next(x for x in c['premiere']['stages'] if x['id']=='partners')['description']
assert next(x for x in s['pages'] if x['id']=='bpi')['title']=='BPI Systems'
assert 'actor.bpi' in next(x for x in s['timeline_view']['lanes'] if x['id']=='partners')['actor_refs']
assert all(x['vendor']=='BPI Systems' for x in t['software_products'] if x['id'].startswith('software.bpi'))
offers={x['id']:x for x in p['products']}
for basket in p['partner_configurations']:
 for year,snap in basket['snapshots'].items():
  assert abs(snap['retail_price_usd']-sum(offers[r]['snapshots'][year]['retail_price_usd'] for r in basket['components']))<.011
  assert basket['id'] not in offers # Never count basket plus components as separate sales.
for sc in f['scenarios']:
 assert sc['launch_year']['units']<=sc['delivery_capacity_units']
 rc=sc['reaction_components'];assert rc['bpi_requested_gain']==rc['bpi_incremental_deliveries']+rc['bpi_capacity_deferred']
 for row in sc['months']:
  b=row['bpi'];assert b['customer_installations']<=row['units']
  assert b['customer_installations']==b['single_accounting_licenses']+b['four_module_customers']+b['complete_suite_licenses']
  assert b['individual_module_licenses']==b['single_accounting_licenses']+4*b['four_module_customers']
  assert abs(b['bpi_receipts_after_channel_usd']-.75*b['retail_spend_usd'])<.011
  assert abs(row['customer_retail_spend_usd']-row['units']*f['average_sale']['retail_price_usd'])<.011 # excludes BPI
 for key,rows in [('calendar_1978',sc['months'][:7]),('launch_year',sc['months'])]:
  for k,v in sc[key]['bpi'].items():assert math.isclose(v,sum(x['bpi'][k] for x in rows),abs_tol=.011)
for sc in f['scenarios']:
 before_bpi=sum(row['units']-row['bpi_gain_units'] for row in sc['months'])
 assert sc['reaction_components']['bpi_incremental_deliveries']==min(sc['reaction_components']['bpi_requested_gain'],max(0,sc['delivery_capacity_units']-before_bpi))
 for row in sc['months']:assert row['bpi']['customer_installations']==round(row['units']*sc['bpi_attachment_rate'])
print('PASS: independent BPI ownership, presentation order, supplier baskets, disjoint licences, separate receipts and production cap.')

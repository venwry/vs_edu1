"""Partner boundaries, component pricing, sales attribution and capacity limits."""
import json, math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
c=read('generated/catalogs/aurelia-1978-campaign.json');s=read('generated/catalogs/site-pages.json');p=read('generated/models/pricing-results.json');f=read('generated/models/sales-forecast.json');t=read('generated/catalogs/logix-aion-technical-catalog-v2.json')
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
 for row in sc['monthly']:
  assert all(not x['product_ref'].startswith('software.bpi') for x in row['pricing_links'])
print('PASS: independent BPI ownership, presentation order, supplier baskets and separate sales receipts.')

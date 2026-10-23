from data_paths import read_document, document_bytes, document_text
"""Cross-model checks for dated offerings, finite shipments, capacity funding and returns."""
import json, math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
read=lambda n:read_document(n, root=R)
p=read('generated/models/pricing-results.json');c=read('generated/models/retail-catalog-1982-results.json');s=read('generated/models/sales-forecast.json');r=read('generated/models/roi-1974-1980.json');m=read('generated/models/quarterly-market-share.json')
close=lambda a,b:abs(a-b)<.06
for ref,comp in [('bundle.artemis_budget_128',3299),('bundle.artemis_budget_128_hdd',4995)]:
 x=next(p for p in p['products'] if p['id']==ref)
 assert x['offering_start']=='1980-05-19'
 for y in ['1978','1979']:assert x['snapshots'][y]['retail_price_usd'] is None
 for y in ['1980','1981','1982']:
  a=x['snapshots'][y];assert close(a['manufacturing_cost_usd'],sum(a['cost_breakdown_usd'].values()))
  assert close(a['unit_profit_usd'],a['retail_price_usd']-a['computerland_fee_usd']-a['manufacturing_cost_usd'])
 a=x['snapshots']['1982'];assert abs(a['contribution_margin_on_net_revenue_pct']-(1-a['retail_price_usd']/comp)*100)<.02
for date,v in c['snapshots'].items():
 budget=[x for x in v['solutions'] if x['id'] in ['budget_colour','budget_hdd']]
 assert len(budget)==(2 if date>='1980-05-19' else 0)
 for x in budget:
  assert ('Abacus 3' in ' '.join(x['includes']))==(date>='1980-11-19')
for case in s['scenarios']:
 for row in case['monthly']:
  budget=[l for l in row['pricing_links'] if l['product_ref'].startswith('bundle.artemis_budget_128')]
  if row['month']<'1980-05':assert not budget
  else:assert sum(l['quantity'] for l in row['pricing_links'])==row['computer_units']
  assert sum(l['quantity'] for l in budget)<=row['products']['artemis']
for scope in [m,m['business_market']]:
 for case in scope['scenarios']:
  for row in case['quarterly']:
   assert row['total_market_units']==sum(v['units'] for v in row['manufacturers'].values())
   assert abs(sum(v['share_pct'] for v in row['manufacturers'].values())-100)<1e-8
   if scope is m['business_market'] and row['quarter']<'1982-Q1':assert row['manufacturers']['ibm']['units']==0
for case in r['scenarios']:
 for before,after in zip(case['quarterly'],case['quarterly'][1:]):
  if after['quarter']<'1980-Q1':continue
  assert close(after['free_cash_flow_usd'],after['ebitda_usd']-after['capex_usd']-after['inventory_cash_change_usd'])
  assert close(after['cumulative_net_cash_usd'],before['cumulative_net_cash_usd']+after['free_cash_flow_usd'])
  assert close(after['operating_profit_ebit_usd'],after['net_revenue_usd']-after['operating_cash_cost_usd']-after['depreciation_usd'])
  assert close(after['cumulative_accounting_roi_pct'],after['cumulative_operating_profit_usd']/(after['cumulative_capex_usd']+after['inventory_balance_usd'])*100)
 for a in case['capacity_plan']:assert a['funding_quarter']<a['service_quarter']
print('PASS: budget dates, balanced pricing, sales substitution, all/business denominators, capacity lead time, ROI and cash continuity.')

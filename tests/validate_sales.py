"""Reconcile every current sales dollar to dated retail pricing, cents and ROI."""
import json,hashlib
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
def cents(x):return int((Decimal(str(x))*100).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
s=read('sales_forecast.json');p={x['id']:x for x in read('pricing_results.json')['products']};roi=read('roi_1974_1980.json');i=read('industrial_investment_1974_1981.json')
F=['customer_retail_spend_usd','supplier_revenue_after_channel_usd','recurring_cost_usd','unit_contribution_total_usd']
assert set(s)=={'metadata','policy','financial_policy','scenarios','sources'}
assert 'reassessed_1980_1982' not in s
for src in s['sources']:assert hashlib.sha256((R/src['path']).read_bytes()).hexdigest()==src['sha256']
for sc in s['scenarios']:
 assert len(sc['monthly'])==60 and len(sc['quarterly'])==20 and len(sc['annual'])==5
 for r in sc['monthly']:
  assert r['computer_units']==sum(r['products'].values())
  if r['month']<'1978-06':assert not r['computer_units']
  if r['month']<'1979-12':assert r['products']['aurelia_plus']==0
  if r['month']<'1980-05':assert r['products']['artemis']==0
  if r['month']<'1981-07':assert r['products']['artemis_pro']==0
  assert cents(r[F[3]])==cents(r[F[1]])-cents(r[F[2]])
  for line in r['pricing_links']:
   ref=line['product_ref'];snap=p[ref]['snapshots'][str(line['snapshot_year'])];n=Decimal(str(line['quantity']))
   for f,key in zip(F[:3],['retail_price_usd','revenue_after_fee_usd','manufacturing_cost_usd']):assert cents(line[f])==cents(n*Decimal(str(snap[key])))
   assert not ref.startswith('software.bpi') and ref!='software.aion_development_team'
  for f in F:assert cents(r[f])==sum(cents(line[f]) for line in r['pricing_links'])
 for grain in ['quarterly','annual']:
  for a in sc[grain]:
   subset=[r for r in sc['monthly'] if (r['month'][:4] if grain=='annual' else r['month'][:4]+'-Q'+str((int(r['month'][5:])-1)//3+1))==a['period']]
   assert a['computer_units']==sum(r['computer_units'] for r in subset)
   for f in F:assert cents(a[f])==sum(cents(r[f]) for r in subset)
central=next(x for x in s['scenarios'] if x['id']=='central')
assert {r['year']:r['computer_units'] for r in central['annual']}=={1978:10073,1979:59073,1980:82916,1981:108198,1982:119389}
for r in central['monthly']:
 if not r['computer_units']:continue
 assert r['products']=={f:i['monthly_demand'][r['month']]['products'].get(f,0) for f in r['products']}
 receipts=[x for x in roi['monthly_revenue_links'] if x['month']==r['month'] and x['stream']=='computer_baskets']
 assert len(receipts)==1
 assert cents(receipts[0]['customer_gross_usd'])==cents(r[F[0]])
 assert cents(receipts[0]['supplier_net_usd'])==cents(r[F[1]])
print('PASS: one current forecast, 60 months × 3 scenarios, launch gates, dated offer pricing, exact cents aggregation and ROI reconciliation.')

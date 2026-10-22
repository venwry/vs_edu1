"""Reconcile revised sales, clone contracts, date gates and unit-price arithmetic."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
read=lambda n:json.loads((R/n).read_text())
s=read('sales_forecast.json');roi=read('roi_1974_1980.json');inputs=read('sales_reassessment_inputs.json');baseline=read('sales_roi_baseline_1982.json')
F=['customer_retail_spend_usd','supplier_revenue_after_channel_usd','recurring_cost_usd','unit_contribution_total_usd']
close=lambda a,b:abs(a-b)<.05
for source in s['sources']:assert hashlib.sha256((R/source['path']).read_bytes()).hexdigest()==source['sha256']
for case in s['scenarios']:
 assert len(case['monthly'])==72 and len(case['quarterly'])==24 and len(case['annual'])==6
 for r in case['monthly']:
  assert r['computer_units']==sum(r['products'].values())
  if r['month']<'1981-07':assert r['products'].get('artemis_pro',0)==0
  if r['month']<'1982-12':assert not r.get('autocad_licenses',0)
  if r['month']<'1981-11':assert not r['team_licenses']
  for key in F:assert close(r[key],sum(l[key] for l in r['pricing_links']))
  for l in r['pricing_links']+r.get('additional_offer_links',[]):
   for key,unit in zip(F[:3],['unit_retail_usd','unit_after_channel_usd','unit_recurring_cost_usd']):assert close(l[key],l['quantity']*l[unit])
   assert close(l[F[3]],l[F[1]]-l[F[2]])
   assert l['product_ref']!='software.autocad_1_artemis'
  if r['month']>='1981-01':assert sum(l['quantity'] for l in r['pricing_links'])==r['computer_units']
 for a in case['annual']:
  rows=[r for r in case['monthly'] if r['month'].startswith(str(a['year']))]
  assert a['computer_units']==sum(r['computer_units'] for r in rows)
  for key in F:assert close(a[key],sum(r[key] for r in rows))
 contracts=next(c for c in s['contract_scenarios'] if c['id']==case['id'])['quarterly']
 assert len(contracts)==40
 for row in contracts:
  assert row['quarter']>='1982-Q1'
  assert close(row['aion_chipsets']+row['sgs_chipsets'],row['computer_units'])
  assert row['whole_computer_royalty_usd']==0 and row['partner_computer_retail_revenue_included'] is False
  assert close(row['project_revenue_usd'],sum(row[k] for k in ['chipset_receipts_usd','platform_software_receipts_usd','sgs_royalty_usd']))
 for quarter in next(c for c in roi['scenarios'] if c['id']==case['id'])['quarterly']:
  if quarter['quarter']<'1981-Q1':continue
  sq=next(q for q in case['quarterly'] if q['quarter']==quarter['quarter'])
  assert quarter['computer_units']==sq['computer_units']
  assert close(quarter['revenue_streams_usd']['computer_baskets'],sq['supplier_revenue_after_channel_usd'])
print('PASS: 72 months, all scenario totals, date gates, complete-system counting, contract boundaries and ROI receipts.')

"""Validate revised pre-tax cash/asset bridge; the old industrial plan is a baseline."""
import json,re,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];m=json.loads((R/'roi_1974_1980.json').read_text());report=(R/'roi.html').read_text();close=lambda a,b:abs(a-b)<.25
assert json.loads(re.search(r'<script id="roi-model" type="application/json">(.*?)</script>',report,re.S).group(1))==m
for source in m['sources']:assert hashlib.sha256((R/source['path']).read_bytes()).hexdigest()==source['sha256']
for scenario in m['scenarios']:
 rows=scenario['quarterly'];assert len(rows)==40 and len({r['quarter'] for r in rows})==40
 cash=cap=dep=ebit=peak=prior_inventory=prior_assets=0
 for r in rows:
  assert close(r['customer_gross_usd']-r['channel_fees_usd']-r['promotional_credits_usd'],r['net_revenue_usd'])
  assert close(sum(r['revenue_streams_usd'].values())-r['promotional_credits_usd'],r['net_revenue_usd'])
  assert close(r['source_operating_expenses_usd']-r['replaced_generic_marketing_usd']-r['eliminated_internal_royalties_usd']+r['marketing_expense_usd'],r['operating_cash_cost_usd'])
  assert close(r['net_revenue_usd']-r['operating_cash_cost_usd'],r['ebitda_usd'])
  assert close(r['ebitda_usd']-r['depreciation_usd'],r['operating_profit_ebit_usd'])
  assert close(r['ebitda_usd']-r['capex_usd']-r['inventory_cash_change_usd'],r['free_cash_flow_usd'])
  assert close(r['inventory_balance_usd']-prior_inventory,r['inventory_cash_change_usd'])
  cash+=r['free_cash_flow_usd'];cap+=r['capex_usd'];dep+=r['depreciation_usd'];ebit+=r['operating_profit_ebit_usd'];peak=max(peak,-cash)
  assert close(cash,r['cumulative_net_cash_usd']) and close(peak,r['peak_external_funding_usd'])
  assert close(cap-dep+r['inventory_balance_usd'],r['end_operating_assets_usd'])
  assert close((prior_assets+r['end_operating_assets_usd'])/2,r['average_operating_assets_usd'])
  if r['average_operating_assets_usd']>0:assert abs(r['quarterly_pretax_roi_pct']-100*r['operating_profit_ebit_usd']/r['average_operating_assets_usd'])<.002
  if r['quarter']>='1981-Q1':
   b=r['reassessment_bridge'];assert close(b['computer_recurring_cost_usd']+b['addon_recurring_cost_usd']+b['oem_recurring_cost_usd']+b['retained_other_cash_cost_usd']+b['additional_programme_expense_usd']-b['internal_cpm_royalty_eliminated_usd'],r['operating_cash_cost_usd'])
  prior_inventory=r['inventory_balance_usd'];prior_assets=r['end_operating_assets_usd']
 assert scenario['first_cash_payback_quarter']==next((r['quarter'] for r in rows if r['peak_external_funding_usd']>0 and r['cumulative_net_cash_usd']>=0),None)
assert '1983' in report and 'market-share.html' in report
print('PASS: 3 × 40 quarters, receipts/costs, capital/depreciation, credit/inventory, cumulative funding and all ROI formulas.')

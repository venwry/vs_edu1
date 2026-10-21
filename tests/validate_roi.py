"""Validate the ROI/marketing accounting bridge and published assets."""
import json,re,hashlib,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(n):return json.loads((R/n).read_text())
m=load('roi_1974_1980.json');i=load('industrial_investment_1974_1981.json');budget=load('marketing_budget_1974_1980.json');report=(R/'roi.html').read_text()
assert json.loads(re.search(r'<script id="roi-model" type="application/json">(.*?)</script>',report,re.S).group(1))==m
assert budget==m['marketing']
for source in m['sources']:assert hashlib.sha256((R/source['path']).read_bytes()).hexdigest()==source['sha256'],source['path']
for scenario in m['scenarios']:
 rows=scenario['quarterly'];assert len(rows)==36 and len({r['quarter'] for r in rows})==36
 cash=cap=dep=profit=revenue=peak=prior_inventory=prior_assets=0
 for r in rows:
  q=r['quarter'];assert q<='1982-Q4'
  capacity=next(x for x in i['quarterly_capacity'] if x['quarter']==q)
  assert r['computer_units']==capacity['customer_computers']
  assert abs(r['capex_usd']-sum(x['capital_usd'] for x in i['quarterly_entity_costs'] if x['quarter']==q))<.1
  close=lambda a,b: abs(a-b)<.15
  assert close(r['customer_gross_usd']-r['channel_fees_usd']-r['promotional_credits_usd'],r['net_revenue_usd'])
  assert close(sum(r['revenue_streams_usd'].values())-r['promotional_credits_usd'],r['net_revenue_usd'])
  assert close(r['source_operating_expenses_usd']-r['replaced_generic_marketing_usd']-r['eliminated_internal_royalties_usd']+r['marketing_expense_usd'],r['operating_cash_cost_usd'])
  assert close(r['net_revenue_usd']-r['operating_cash_cost_usd'],r['ebitda_usd'])
  assert close(r['ebitda_usd']-r['depreciation_usd'],r['operating_profit_ebit_usd'])
  assert close(r['ebitda_usd']-r['capex_usd']-r['inventory_cash_change_usd'],r['free_cash_flow_usd'])
  assert close(r['inventory_balance_usd']-prior_inventory,r['inventory_cash_change_usd'])
  expense=sum(x['central_usd'] for x in budget['items'] if x['quarter']==q and x['treatment']=='expense')*scenario['marketing_multiplier']
  assert close(expense,r['marketing_expense_usd'])
  cash+=r['free_cash_flow_usd'];cap+=r['capex_usd'];dep+=r['depreciation_usd'];profit+=r['operating_profit_ebit_usd'];revenue+=r['net_revenue_usd'];peak=max(peak,-cash)
  assert close(cash,r['cumulative_net_cash_usd']) and close(peak,r['peak_external_funding_usd'])
  assert close(cap-dep+r['inventory_balance_usd'],r['end_operating_assets_usd'])
  if r['average_operating_assets_usd']>0:assert abs(r['quarterly_pretax_roi_pct']-100*r['operating_profit_ebit_usd']/r['average_operating_assets_usd'])<.002
  else:assert r['quarterly_pretax_roi_pct'] is None
  prior_inventory=r['inventory_balance_usd'];prior_assets=r['end_operating_assets_usd']
 assert scenario['first_cash_payback_quarter']==next((r['quarter'] for r in rows if r['peak_external_funding_usd']>0 and r['cumulative_net_cash_usd']>=0),None)
central=next(s for s in m['scenarios'] if s['id']=='central')
for a in m['annual_central']:
 for key in ['net_revenue_usd','operating_cash_cost_usd','capex_usd','free_cash_flow_usd']:
  assert abs(a[key]-sum(r[key] for r in central['quarterly'] if r['quarter'].startswith(str(a['year']))))<.1
site=load('site_pages.json');pages={p['id']:p for p in site['pages']}
assert pages['roi']['path']=='roi.html' and 'roi' in site['navigation']
for id in site['navigation']:assert 'href="'+pages[id]['path']+'"' in report
assert '__MODEL__' not in report and '__NAV__' not in report
static_html=re.sub(r'<script\b[^>]*>.*?</script>','',report,flags=re.S)
for href in re.findall(r'href="([^"#]+)"',static_html):
 if not href.startswith(('http:','https:')):assert (R/href).exists(),href
print('PASS: 3 scenarios × 36 quarters, revenue/cost bridge, marketing replacement, credit treatment, depreciation/cash distinction, funding/ROI formulas, hashes and published navigation')


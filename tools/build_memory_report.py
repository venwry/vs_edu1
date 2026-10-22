"""Build the RAM revision comparison from the same committed financial models."""
import json, html, hashlib
from pathlib import Path
from memory_manufacturing import policy, evaluate, selected
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
b=read('memory_manufacturing_baseline.json');p=policy()
c=read('manufacturing_costs.json');prices=read('pricing_results.json');i=read('industrial_investment_1974_1981.json');roi=read('roi_1974_1980.json');sales=read('sales_forecast.json')
cp={x['id']:x for x in c['products']};pp={x['id']:x for x in prices['products']}
central=next(x for x in roi['scenarios'] if x['id']=='central')
products=[]
for ref in ['bundle.aurelia_plus_mono','bundle.aurelia_plus_color','bundle.artemis_256_color','bundle.artemis_256_mono_pro','bundle.artemis_pro_512_server','bundle.artemis_pro_1mb_server','device.artemis_ram_256kb_bank_kit']:
 for y in ['1980','1981']:
  old=b['prices'][ref][y];new=pp[ref]['snapshots'][y]['retail_price_usd']
  if old is None:continue
  products.append(dict(product_ref=ref,year=y,previous_cost_usd=b['costs'][ref][y],revised_cost_usd=cp[ref]['snapshots'][y]['total_usd'],previous_retail_usd=old,revised_retail_usd=new,retail_change_pct=round((new/old-1)*100,3)))
recipes=[]
for r in p['memory_recipes']:
 year=max(1981,int(r['available_from'][:4]));wc=p['wafer_cost_by_year'][str(year)][r['node_um']]
 recipes.append(dict(r,comparison_year=year,**evaluate(r,wc)))
roi_changes=[]
for year in [1980,1981]:
 old=next(x for x in b['roi_central'] if x['quarter']==f'{year}-Q4');new=next(x for x in central['quarterly'] if x['quarter']==f'{year}-Q4')
 for metric in ['cumulative_net_revenue_usd','cumulative_operating_profit_usd','cumulative_net_cash_usd','cumulative_capex_usd','peak_external_funding_usd','cumulative_accounting_roi_pct']:
  roi_changes.append(dict(year=year,metric=metric,previous=old[metric],revised=new[metric],change=round(new[metric]-old[metric],3)))
demand=[]
future_cap=sum(x['usd'] for x in p['capital_schedule'] if x['quarter']>'1982-Q4')
future_eng=sum(x['loaded_payroll_and_validation_usd'] for x in p['future_engineering'] if int(x['period'])>1982)
m=dict(status=p['status'],baseline_commit=b['source_commit'],era_policy=p['era_policy'],products=products,recipes=recipes,roi=roi_changes,investment=i['memory_manufacturing'],forward_budget_total_usd=future_cap+future_eng,forward_budget_basis='Capital plus stated engineering/validation budgets after 1982; excludes future production operating costs. Not a complete 1983 cash forecast.',cash_after_reserving_forward_budgets_usd=round(central['quarterly'][-1]['cumulative_net_cash_usd']-future_cap-future_eng,2),first_cash_payback_quarter=central['first_cash_payback_quarter'])
m['sources']=[dict(path=f,sha256=hashlib.sha256((R/f).read_bytes()).hexdigest()) for f in ['memory_manufacturing.json','memory_manufacturing_baseline.json','manufacturing_costs.json','pricing_results.json','industrial_investment_1974_1981.json','roi_1974_1980.json','sales_forecast.json']]
(R/'memory_manufacturing_impact.json').write_text(json.dumps(m,indent=2)+'\n')
# The RAM manufacturing HTML page has been retired.

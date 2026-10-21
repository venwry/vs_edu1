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
current_sales=next(x for x in sales['scenarios'] if x['id']=='central')['ncc_to_comdex1980']
demand=[]
for k,v in b['sales_to_nov18'].items():demand.append(dict(period='NCC–Nov 18 1980 constrained deliveries',family=k,previous=v,revised=current_sales[k]))
for f in ['aurelia','aurelia_plus','artemis','artemis_pro']:
 def total(md):return sum(v['products'].get(f,0) for m,v in md.items() if m.startswith('1981'))
 demand.append(dict(period='1981 conditional full demand',family=f,previous=total(b['monthly_demand']),revised=total(i['monthly_demand'])))
future_cap=sum(x['usd'] for x in p['capital_schedule'] if x['quarter']>'1982-Q4')
future_eng=sum(x['loaded_payroll_and_validation_usd'] for x in p['future_engineering'] if int(x['period'])>1982)
m=dict(status=p['status'],baseline_commit=b['source_commit'],era_policy=p['era_policy'],products=products,recipes=recipes,sales=demand,roi=roi_changes,investment=i['memory_manufacturing'],forward_budget_total_usd=future_cap+future_eng,forward_budget_basis='Capital plus stated engineering/validation budgets after 1982; excludes future production operating costs. Not a complete 1983 cash forecast.',cash_after_reserving_forward_budgets_usd=round(central['quarterly'][-1]['cumulative_net_cash_usd']-future_cap-future_eng,2),first_cash_payback_quarter=central['first_cash_payback_quarter'])
m['sources']=[dict(path=f,sha256=hashlib.sha256((R/f).read_bytes()).hexdigest()) for f in ['memory_manufacturing.json','memory_manufacturing_baseline.json','manufacturing_costs.json','pricing_results.json','industrial_investment_1974_1981.json','roi_1974_1980.json','sales_forecast.json']]
(R/'memory_manufacturing_impact.json').write_text(json.dumps(m,indent=2)+'\n')
def table(headers,rows):return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(f'{x:,.2f}' if isinstance(x,float) else str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
site=read('site_pages.json');pages={x['id']:x for x in site['pages']}
nav=''.join('<a href="'+pages[x]['path']+'">'+html.escape(pages[x]['title'])+'</a>' for x in site['navigation'])
body='<h1>RAM manufacturing</h1><p>January 1979 programme start · 2.75, 2.0 and 1.5 µm development · nominal USD</p><p>'+html.escape(p['era_policy'])+'</p><p>Scenario assumptions, not measured factory yields. Manufacturing release requires retention, speed, repair coverage, matched-tool and board qualification. The cheapest qualified recipe wins; a smaller feature size is not automatically cheaper.</p>'
body+='<h2>Production decision</h2><p>For the June 1981 snapshot, repaired 3 µm RAM beats the 2.75 µm candidate after spare area, repair operations and wafer costs. AION 64K chips replace purchased chips in PRO modules after qualification. RAM capacity, bus width, CPU speed and graphics specifications remain unchanged. The original purchased-memory record remains a qualified contingency, without booked savings.</p>'
body+=table(['Recipe','Available','Area mm²','Comparison year','Die yield %','Packaged chip USD'],[[r['id'],r['available_from'],r['die_area_mm2'],r['comparison_year'],r['die_yield']*100,r['good_packaged_chip_cost_usd']] for r in recipes])
body+='<p>All first four recipes above use the same 1981 wafer-cost basis. Later nodes use their own release-year costs; they are prospective 64K x 1 recipes, not assumed larger memories. Repair recovers only a share of spatial defects and never systematic/non-area losses.</p><h2>Costs and balanced retail prices</h2><p>The existing balanced-percentages rule is retained: P = √(C × B / (1 − channel fee)). It equates margin as a percentage of net receipts with the discount from the market reference. Savings are not passed through dollar for dollar.</p>'
body+=table(['Product','Year','Old cost','New cost','Old retail','New retail','Retail Δ %'],[[x[k] for k in ['product_ref','year','previous_cost_usd','revised_cost_usd','previous_retail_usd','revised_retail_usd','retail_change_pct']] for x in products])
body+='<h2>Demand response</h2><p>The current model includes the 1980–82 market reassessment. Changes relative to the old baseline combine memory pricing, market reactions and capacity policy; they are not an isolated causal RAM benefit. PRO remains conditional on July 1981 qualification.</p>'+table(['Period','Family','Previous units','Revised units'],[[x[k] for k in ['period','family','previous','revised']] for x in demand])
body+='<h2>Investment and ROI</h2><p>Through 1982, the model includes $2,925,000 in process capital and $468,000 of pilot/nonpayroll spending. The 1982 $600,000 engineering provision is reconciled against existing payroll. Earlier scheduled process engineering remains funded. Repair costs are inside RAM recurring costs. The original 120 PM DRAM programme is not charged again. The pilot line adds no saleable output to the legacy fab.</p>'
body+=table(['Year-end','Metric','Previous','Revised','Change'],[[x[k] for k in ['year','metric','previous','revised','change']] for x in roi_changes])
body+='<p>Historical comparison rows end in 1981; the current financial horizon extends through December 1982. ROI is project-wide, pre-tax and unlevered; it is not the isolated return on the memory programme. Full-demand revenue matches the expanded industrial cost plan. The original constrained delivery forecast remains separately labelled.</p>'
body+=f'<p>Forward 1983 capital: ${future_cap:,.0f}; engineering/validation: ${future_eng:,.0f}; total: ${future_cap+future_eng:,.0f}. These out-of-horizon budgets are disclosed rather than charged early. End-1982 cash after reserving this entire budget is ${m["cash_after_reserving_forward_budgets_usd"]:,.0f}. This is a funding sensitivity, not future ROI; no 1983 sales, production costs or terminal value are invented.</p>'
body+='<h2>Development roadmap</h2><p>Procurement and installation start January 1979. Separate process intervals and milestone events are shown on the timeline. 2.75 µm pilot: December 1979; process review: June 1980; RAM cost review: June 1981. 2.0 µm pilot: September 1981; RAM release target: July 1982. 1.5 µm pilot: March 1983; RAM release target: October 1983.</p><p><a href="timeline.html">Timeline</a> · <a href="roi.html">Quarterly ROI</a> · <a href="memory_manufacturing_impact.json">Comparison JSON</a> · <a href="market-outlook.html">Methodology and regeneration</a></p>'
doc='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RAM manufacturing | Logix / AION</title><style>body{font:16px/1.6 system-ui;margin:0;color:#e7edf6;background:#111827}nav,main{padding:24px;max-width:1280px;margin:auto}nav{display:flex;gap:16px;flex-wrap:wrap}a{color:#8dd4ff}h1{font-size:38px}h2{margin-top:40px}table{border-collapse:collapse;width:100%;font-size:14px}td,th{text-align:left;padding:10px;border-bottom:1px solid #374151}.scroll{overflow:auto}th{color:#9ee8ca}</style><nav class="site-nav">'+nav+'</nav><main>'+body+'</main><script type="application/json" id="memory-impact">'+json.dumps(m).replace('</','<\\/')+'</script></html>'
(R/'memory-manufacturing.html').write_text(doc)
print(json.dumps({'products':products,'demand':demand,'end_1981':roi_changes[-6:],'forward_budget':future_cap+future_eng},indent=2))

"""Publish the canonical reaction forecast and its cross-model reconciliation."""
import json,hashlib,html,sys
from pathlib import Path
from collections import defaultdict
from market_outlook import POLICY,quarter,team_units
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
def write(n,d):(R/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
I=read('industrial_investment_1974_1981.json');S=read('sales_forecast.json')
if '--sales' in sys.argv:
 scenarios=[]
 for name,mult in POLICY['bounds'].items():
  monthly=[]
  for m,r in I['monthly_demand'].items():
   if m<'1980':continue
   # Bounds apply once to the central result, preserving launch gates.
   products={k:round(v*mult) for k,v in r['products'].items()}
   monthly.append({'month':m,'products':products,'computer_units':sum(products.values()),'team_licenses':round(team_units(m)*mult),'basis':r['basis']})
  quarterly=[]
  for q in sorted({quarter(r['month']) for r in monthly}):
   rows=[r for r in monthly if quarter(r['month'])==q]
   quarterly.append({'quarter':q,'products':{k:sum(r['products'].get(k,0) for r in rows) for k in ['aurelia','aurelia_plus','artemis','artemis_pro']},'computer_units':sum(r['computer_units'] for r in rows),'team_licenses':sum(r['team_licenses'] for r in rows)})
  annual=[{'year':y,'computer_units':sum(r['computer_units'] for r in quarterly if r['quarter'].startswith(str(y))),'team_licenses':sum(r['team_licenses'] for r in quarterly if r['quarter'].startswith(str(y)))} for y in [1980,1981,1982]]
  scenarios.append({'id':name,'monthly':monthly,'quarterly':quarterly,'annual':annual})
 S['reassessed_1980_1982']={'status':'Canonical current forecast; older scenario sections retained as historical constrained-delivery references.','policy':POLICY,'scenarios':scenarios,'financial_case':'Central demand funds the industrial plan and ROI; conservative/strong sales bounds are not recomputed financial scenarios.'}
 S['metadata']['current_forecast_horizon']='1982-12-31'
 S['metadata']['source_pricing_sha256']=hashlib.sha256((R/'pricing_results.json').read_bytes()).hexdigest()
 for f,k in [('market_reactions.json','source_reactions_sha256'),('logix_aion_story.json','source_story_sha256')]:S['metadata'][k]=hashlib.sha256((R/f).read_bytes()).hexdigest()
 write('sales_forecast.json',S)
 sys.exit()
ROI=read('roi_1974_1980.json');sc=next(x for x in S['reassessed_1980_1982']['scenarios'] if x['id']=='central');fin=next(x for x in ROI['scenarios'] if x['id']=='central');cap={r['quarter']:r for r in I['quarterly_capacity']};finq={r['quarter']:r for r in fin['quarterly']}
rows=[]
for r in sc['quarterly']:
 q=r['quarter'];rows.append({**r,'peak_month_demand':cap[q]['peak_month_customer_demand'],'capacity_month':cap[q]['installed_computer_capacity_month'],**{k:finq[q][k] for k in ['net_revenue_usd','capex_usd','operating_profit_ebit_usd','free_cash_flow_usd','cumulative_accounting_roi_pct']}})
end=fin['quarterly'][-1]
if '--timeline' in sys.argv:
 story=read('logix_aion_story.json');site=read('site_pages.json');events={e['id']:e for p in story['phases'] for e in p['events']}
 for year in [1980,1981,1982]:
  id=f'event.financial_review_{year}';date=f'{year}-12-31';annual=next(a for a in ROI['annual_central'] if a['year']==year);units=next(a['computer_units'] for a in sc['annual'] if a['year']==year);last=finq[f'{year}-Q4']
  if id not in events:
   event={'id':id,'title':f'{year} sales, capacity and investment review','event_type':'development','date':{'start':date,'end':date},'participants':[{'actor_ref':'actor.logix','role':'participant'}],'actions':[{'actor_refs':['actor.logix'],'description':'Scenario financial checkpoint. Forecast sales match costed production; capacity includes 5% commercial headroom. Details and assumptions are in market-outlook.html.'}],'outcomes':[],'agreement_terms':[],'metrics':[],'product_refs':[],'related_event_refs':[]}
   next(p for p in story['phases'] if p['period']['start']<=date<=p['period']['end'])['events'].append(event)
   next(l for l in site['timeline_view']['lanes'] if l['id']=='logix')['event_refs'].append(id);events[id]=event
  events[id]['metrics']=[{'name':k,'value':v,'unit':unit,'qualifier':'Central alternative-history forecast; nominal, pre-tax five-entity project scope.'} for k,v,unit in [('annual_computer_sales',units,'computers'),('annual_net_revenue',annual['net_revenue_usd'],'USD'),('annual_capital_investment',annual['capex_usd'],'USD'),('annual_operating_profit',annual['operating_profit_ebit_usd'],'USD'),('cumulative_accounting_roi',last['cumulative_accounting_roi_pct'],'percent'),('cumulative_free_cash',last['cumulative_net_cash_usd'],'USD')]]
 for p in story['phases']:p['events'].sort(key=lambda e:e['date']['start'])
 write('logix_aion_story.json',story);write('site_pages.json',site)
 sys.exit()

M={'title':'Market reactions, demand and returns through 1982','status':'Alternative-history central forecast, not historical accounts','policy':POLICY,'quarterly':rows,'annual':sc['annual'],'end_1982':end,'team_development_reconciliation':I['team_development_reconciliation'],'team_campaign_reconciliation':ROI['team_campaign_reconciliation'],'regeneration':['python3 tools/rebuild_outlook.py'],'sources':[{'path':f,'sha256':hashlib.sha256((R/f).read_bytes()).hexdigest()} for f in ['sales_forecast.json','industrial_investment_1974_1981.json','roi_1974_1980.json','logix_aion_story.json','market_reactions.json','team_development_program.json','tools/market_outlook.py']]}
write('market_outlook_1980_1982.json',M)
esc=html.escape
money=lambda x:'$'+format(x/1e6,',.2f')+'m'
def table(headers,rows):return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+esc(str(x))+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
site=read('site_pages.json');pages={p['id']:p for p in site['pages']};nav=''.join('<a href="'+esc(pages[i]['path'])+'">'+esc(pages[i]['title'])+'</a>' for i in site['navigation'])
annual=[]
for a in sc['annual']:
 f=next(r for r in ROI['annual_central'] if r['year']==a['year']);annual.append([a['year'],format(a['computer_units'],','),a['team_licenses'],money(f['net_revenue_usd']),money(f['capex_usd']),money(f['operating_profit_ebit_usd']),money(f['free_cash_flow_usd'])])
content='<p class="tag">Alternative history · revised planning case</p><h1>1980–82 market outlook</h1><p>CP/M and documented interfaces sustain Logix demand. Recession, IBM’s independently commissioned OS and selective native-software adoption constrain growth. Adam schedules capacity before peaks with <b>5% commercial headroom</b>; no reserve units are counted as sales.</p>'
content+='<p><a href="timeline.html">Open the updated timeline</a> · <a href="roi.html">Quarterly ROI</a> · <a href="industrial_investment_1974_1981.html">Manufacturing investment</a> · <a href="market_outlook_1980_1982.json">Complete model JSON</a></p>'
content+='<h2>Central forecast</h2>'+table(['Year','Computers','Team licences','Net revenue','Capital spend','Operating profit','Free cash flow'],annual)
content+='<p>End-1982 cumulative accounting ROI: <b>'+str(end['cumulative_accounting_roi_pct'])+'%</b>. Cumulative free cash: <b>'+money(end['cumulative_net_cash_usd'])+'</b>. Peak funding: '+money(end['peak_external_funding_usd'])+'. First cash payback: '+str(fin['first_cash_payback_quarter'] or 'not reached')+'.</p><p>ROI = cumulative EBIT ÷ (cumulative capital spending + ending inventory). This is a nominal, pre-tax, five-entity project measure, not Adam’s shareholder return. Cash flow includes new investments and inventory; no terminal liquidation is assumed.</p>'
content+='<h2>Quarterly sales and capacity</h2>'+table(['Quarter','Aurelia','Aurelia+','Artemis','PRO','Team','Peak / month','Capacity / month','Capex','Net revenue'],[[r['quarter'],*r['products'].values(),r['team_licenses'],r['peak_month_demand'],r['capacity_month'],money(r['capex_usd']),money(r['net_revenue_usd'])] for r in rows])
content+='<p>Assembly capacity targets the next two quarters’ peak × 1.05. Fab purchases precede commissioning by four quarters. Equipment rounding, one-down redundancy and installed facilities can produce more than 5% actual idle capacity. Inventory retains 45 input days + 14 finished-goods days + 1.5 days (5% of a month) reserve, funded a quarter ahead.</p>'
content+='<h2>Market assumptions by quarter</h2>'+table(['Quarter','Reaction'],[[r['quarter'],POLICY['quarter_reasons'][i]] for i,r in enumerate(rows)])
content+='<h2>Scenario bounds</h2>'+table(['Case','1980 computers','1981 computers','1982 computers'],[[s['id'],*[format(a['computer_units'],',') for a in s['annual']]] for s in S['reassessed_1980_1982']['scenarios']])
content+='<p>Bounds are ±20% judgement assumptions, not confidence intervals. Published ROI uses central demand; the ROI page’s low/high controls vary marketing cost only. The selected IBM launch date is March 15, 1982; delayed qualification can change these results.</p>'
content+='<h2>Development and campaign integration</h2>'+table(['Quarter','Gross Team development','Existing payroll allocated','Incremental expense'],[[r['quarter'],money(r['gross_development_usd']),money(r['existing_payroll_allocated_usd']),money(r['incremental_development_usd'])] for r in I['team_development_reconciliation']])
content+=table(['Quarter','Gross Team campaign','Existing outreach allocated','Incremental expense'],[[r['quarter'],money(r['gross_campaign_usd']),money(r['existing_marketing_reallocated_usd']),money(r['incremental_campaign_usd'])] for r in ROI['team_campaign_reconciliation']])
content+='<p>The $1.38m development and $276,000 campaign budgets include contingency. Only the amount beyond reassigned existing funding is added. Small-team support and delivery remain recurring unit costs. Four-client purchases are contained in computer totals; half of Team buyers also buy two Aurelia and two Artemis network upgrades and an eight-port hub. Initial Team sales use the first costed 1982 price as an explicit launch proxy.</p>'
content+='<h2>Manufacturing and port-development boundaries</h2><ul>'+''.join('<li>'+esc(x)+'</li>' for x in POLICY['premises'])+'</ul><p>1982 includes $700,000 of process capital, the $600,000 memory-engineering provision net of allocated existing payroll, $144,000 pilot operations, and DRI 68k prototype work. No 68k licence receipts or 1983 sales are booked. Larger server storage remains unpriced; Team adoption is limited to small repositories.</p>'
content+='<details><summary>Reproduce the model</summary><pre>'+esc('\n'.join(M['regeneration']))+'</pre><p>Legacy filenames retain their names for stable links; model metadata and report horizons extend through 1982. Historical sales sections remain references only.</p></details>'
(R/'market-outlook.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>1980–82 market outlook · Logix / AION</title><style>body{margin:0;background:#101827;color:#e6edf6;font:16px/1.55 system-ui}nav{padding:18px;background:#172437;display:flex;gap:16px;flex-wrap:wrap}a{color:#8ed8ef}main{max-width:1200px;margin:auto;padding:30px}h1{font-size:40px}h2{margin-top:40px}.tag{color:#87c7bf}.scroll{overflow:auto}table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:12px;text-align:left;border-bottom:1px solid #344357;vertical-align:top}th{color:#8ed8ef;background:#172437}p{max-width:1000px}pre{white-space:pre-wrap}</style></head><body><nav class="site-nav">'+nav+'</nav><main>'+content+'</main><script id="outlook-model" type="application/json">'+json.dumps(M).replace('</','<\\/')+'</script></body></html>')
print(json.dumps({'annual':annual,'end_1982':{k:end[k] for k in ['cumulative_accounting_roi_pct','cumulative_net_cash_usd','peak_external_funding_usd']}}))

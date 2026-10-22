"""Publish the canonical reaction forecast and its cross-model reconciliation."""
import json,hashlib,html,sys
from pathlib import Path
from collections import defaultdict
from market_outlook import POLICY,quarter,team_units
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
def write(n,d):(R/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
I=read('industrial_investment_1974_1981.json');S=read('sales_forecast.json')
ROI=read('roi_1974_1980.json');sc=next(x for x in S['scenarios'] if x['id']=='central');fin=next(x for x in ROI['scenarios'] if x['id']=='central');cap={r['quarter']:r for r in I['quarterly_capacity']};finq={r['quarter']:r for r in fin['quarterly']}
rows=[]
for r in sc['quarterly']:
 if r['quarter']<'1980':continue
 q=r['quarter'];rows.append({**r,'peak_month_demand':cap[q]['peak_month_customer_demand'],'capacity_month':cap[q]['installed_computer_capacity_month'],**{k:finq[q][k] for k in ['net_revenue_usd','capex_usd','operating_profit_ebit_usd','free_cash_flow_usd','cumulative_accounting_roi_pct']}})
end=fin['quarterly'][-1]
if '--timeline' in sys.argv:
 story=read('logix_aion_story.json');site=read('site_pages.json');events={e['id']:e for p in story['phases'] for e in p['events']}
 for year in [1980,1981,1982]:
  id=f'event.financial_review_{year}';date=f'{year}-12-31';annual=next(a for a in ROI['annual_central'] if a['year']==year);units=next(a['computer_units'] for a in sc['annual'] if a['year']==year);last=finq[f'{year}-Q4']
  if id not in events:
   event={'id':id,'title':f'{year} sales, capacity and investment review','event_type':'development','date':{'start':date,'end':date},'participants':[{'actor_ref':'actor.logix','role':'participant'}],'actions':[{'actor_refs':['actor.logix'],'description':'Scenario financial checkpoint. Forecast sales match costed production; capacity includes 5% commercial headroom. Details and assumptions are in market_outlook_1980_1982.json.'}],'outcomes':[],'agreement_terms':[],'metrics':[],'product_refs':[],'related_event_refs':[]}
   next(p for p in story['phases'] if p['period']['start']<=date<=p['period']['end'])['events'].append(event)
   next(l for l in site['timeline_view']['lanes'] if l['id']=='logix')['event_refs'].append(id);events[id]=event
  events[id]['metrics']=[{'name':k,'value':v,'unit':unit,'qualifier':'Central alternative-history forecast; nominal, pre-tax five-entity project scope.'} for k,v,unit in [('annual_computer_sales',units,'computers'),('annual_net_revenue',annual['net_revenue_usd'],'USD'),('annual_capital_investment',annual['capex_usd'],'USD'),('annual_operating_profit',annual['operating_profit_ebit_usd'],'USD'),('cumulative_accounting_roi',last['cumulative_accounting_roi_pct'],'percent'),('cumulative_free_cash',last['cumulative_net_cash_usd'],'USD')]]
 for p in story['phases']:p['events'].sort(key=lambda e:e['date']['start'])
 write('logix_aion_story.json',story);write('site_pages.json',site)
 sys.exit()

M={'title':'Market reactions, demand and returns through 1982','status':'Alternative-history central forecast, not historical accounts','policy':POLICY,'quarterly':rows,'annual':[a for a in sc['annual'] if a['year']>=1980],'end_1982':end,'team_development_reconciliation':I['team_development_reconciliation'],'team_campaign_reconciliation':ROI['team_campaign_reconciliation'],'regeneration':['python3 tools/rebuild_outlook.py'],'sources':[{'path':f,'sha256':hashlib.sha256((R/f).read_bytes()).hexdigest()} for f in ['sales_forecast.json','industrial_investment_1974_1981.json','roi_1974_1980.json','logix_aion_story.json','market_reactions.json','team_development_program.json','tools/market_outlook.py']]}
write('market_outlook_1980_1982.json',M)

# HTML report retired; canonical forecast JSON remains available to dependent models.

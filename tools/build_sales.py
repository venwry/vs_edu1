"""Build the single current sales forecast from accepted demand and dated retail prices."""
import json,hashlib,calendar
from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP
from market_outlook import POLICY,reassess,team_units,quarter
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
def save(n,d):(R/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def cents(n):return int((Decimal(str(n))*100).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
inputs=read('sales_model_inputs.json');prices={r['id']:r for r in read('pricing_results.json')['products']}
F=['customer_retail_spend_usd','supplier_revenue_after_channel_usd','recurring_cost_usd','unit_contribution_total_usd'];families=['aurelia','aurelia_plus','artemis','artemis_pro']
def snapshot(ref,year):
 eligible={int(y):v for y,v in prices[ref]['snapshots'].items() if v.get('retail_price_usd') is not None}
 y=max([y for y in eligible if y<=year],default=min(eligible))
 return y,eligible[y]
central=reassess(inputs['demand_anchor_months'])
scenarios=[]
for name,mult in POLICY['bounds'].items():
 rows=[]
 for month in [f'1978-{m:02}' for m in range(1,6)]+list(central):
  source=central.get(month,{'products':{},'basis':'Pre-launch: no computer sales.'})
  products={f:round(source['products'].get(f,0)*mult) for f in families};year=max(1978,int(month[:4])-(int(month[5:])<6));links=[]
  totals={f:0 for f in F}
  for family,count in products.items():
   if not count:continue
   for item in inputs['basket_components'][family]:
    ref=item['product_ref'];vintage,p=snapshot(ref,year);quantity=Decimal(str(item['quantity'])).quantize(Decimal('0.000000001'))*count
    gross=cents(quantity*Decimal(str(p['retail_price_usd'])));net=cents(quantity*Decimal(str(p['revenue_after_fee_usd'])));cost=cents(quantity*Decimal(str(p['manufacturing_cost_usd'])))
    vals=dict(zip(F,[gross,net,cost,net-cost]));totals={k:totals[k]+vals[k] for k in F}
    links.append({'family':family,'product_ref':ref,'quantity':float(quantity),'snapshot_year':vintage,'snapshot_proxy':vintage>year,'unit_retail_usd':p['retail_price_usd'],'unit_after_channel_usd':p['revenue_after_fee_usd'],'unit_recurring_cost_usd':p['manufacturing_cost_usd'],**{k:v/100 for k,v in vals.items()}})
  rows.append({'month':month,'period_start':month+'-01','period_end':month+'-'+str(calendar.monthrange(int(month[:4]),int(month[5:]))[1]),'products':products,'computer_units':sum(products.values()),'team_licenses':round(team_units(month)*mult),'basis':source['basis'],**{k:v/100 for k,v in totals.items()},'pricing_links':links})
 def aggregate(key):
  groups={}
  for r in rows:groups.setdefault(key(r['month']),[]).append(r)
  return [{'period':k,'products':{f:sum(r['products'][f] for r in rr) for f in families},'computer_units':sum(r['computer_units'] for r in rr),'team_licenses':sum(r['team_licenses'] for r in rr),**{f:sum(cents(r[f]) for r in rr)/100 for f in F}} for k,rr in groups.items()]
 scenarios.append({'id':name,'title':name.title(),'monthly':rows,'quarterly':[dict(r,quarter=r['period']) for r in aggregate(quarter)],'annual':[dict(r,year=int(r['period'])) for r in aggregate(lambda m:m[:4])]})
files=['pricing_results.json','sales_model_inputs.json','logix_aion_story.json','market_reactions.json','tools/market_outlook.py']
metadata={'title':'Current computer sales and package financials','current_forecast_horizon':'1982-12-31','schema_version':2,'currency':'nominal USD','source_pricing_sha256':hashlib.sha256((R/files[0]).read_bytes()).hexdigest(),'source_story_sha256':hashlib.sha256((R/'logix_aion_story.json').read_bytes()).hexdigest(),'source_reactions_sha256':hashlib.sha256((R/'market_reactions.json').read_bytes()).hexdigest()}
model={'metadata':metadata,'policy':POLICY,'financial_policy':{'scope':'Computer baskets only. Standalone Team Edition, BPI, cards, upgrades and Academy revenue remain separate in ROI. Bundle components appear once; their constituent editions are not additional sales.','retail_spend':'Quantity × dated retail_price_usd for every weighted basket offer.','after_channel_fees':'Quantity × dated revenue_after_fee_usd, already net of the modeled fee.','recurring_cost':'Quantity × dated manufacturing_cost_usd; includes the recurring contents and services defined in retail pricing.','contribution':'After channel fees minus recurring cost, before corporate development, marketing, capital/depreciation and tax.','timing':'Use June snapshot from June onward, prior-year snapshot January–May. First available snapshot is a labelled proxy for offers introduced after the prior snapshot. June snapshots proxy the whole month.','rounding':'Round each weighted offer line to cents, then sum lines, months, quarters and years. Contribution is net receipts minus recurring cost in integer cents.','demand':'Accepted central demand unchanged. Conservative/strong scale each product count by 0.8/1.2 once; these are scenario bounds, not separate historical versions.'},'scenarios':scenarios,'sources':[{'path':f,'sha256':hashlib.sha256((R/f).read_bytes()).hexdigest()} for f in files]}
save('sales_forecast.json',model)
print('Built current monthly sales and dated package financials, 1978–1982.')

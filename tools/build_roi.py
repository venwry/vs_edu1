from data_store import read_document, document_bytes, document_text
"""Rebuild itemized marketing and project ROI through 1982 from committed inputs."""
import json,math,hashlib,re,html
from pathlib import Path
from collections import defaultdict
R=Path(__file__).resolve().parents[1]
def read(f):return read_document(f, root=R)
I=read('generated/models/industrial-investment-1974-1981.json');S=read('generated/models/sales-forecast.json');P=read('generated/models/pricing-results.json')
prices={p['id']:p for p in P['products']}; Q=[f'{y}-Q{q}' for y in range(1974,1983) for q in range(1,5)];base=next(x for x in S['scenarios'] if x['id']=='central');inputs=read('generated/catalogs/sales-model-inputs.json')
def qr(m):return m[:4]+'-Q'+str((int(m[5:7])-1)//3+1)
def snap(ref,year):
 d=prices[ref]['snapshots']; ys=[k for k,v in d.items() if v.get('retail_price_usd') is not None]
 eligible=[y for y in ys if int(y)<=year];return d[max(eligible or ys,key=int)]
def money(x):return round(x,2)
revenue=[];revenueq=defaultdict(lambda:defaultdict(float));revenue_entity=defaultdict(lambda:defaultdict(float))
def rev(m,stream,gross,net,units,basis):
 revenue.append({'month':m,'quarter':qr(m),'stream':stream,'units':round(units,4),'customer_gross_usd':money(gross),'channel_fees_usd':money(gross-net),'supplier_net_usd':money(net),'basis':basis})
 revenueq[qr(m)]['gross']+=gross;revenueq[qr(m)]['channel']+=gross-net;revenueq[qr(m)]['net']+=net;revenueq[qr(m)][stream]+=net
for m,md in I['monthly_demand'].items():
 if m>'1982-12':continue
 row=next(r for r in base['monthly'] if r['month']==m)
 rev(m,'computer_baskets',row['customer_retail_spend_usd'],row['supplier_revenue_after_channel_usd'],row['computer_units'],'Canonical current sales: weighted basket quantities × dated retail pricing; cents summed from offer lines.')
 for l in I['product_cost_links']:
  if l['month']==m and l['product_ref'].startswith('software.bpi'):
   ps=snap(l['product_ref'],l['cost_snapshot_year']);rev(m,'bpi_licenses',l['units']*ps['retail_price_usd'],l['units']*ps['revenue_after_fee_usd'],l['units'],'Independent BPI licenses matched once to costed quantities and dated prices.')
 for cohort in inputs['standalone_applications']:
  if cohort['month']!=m:continue
  for ref,key in [('software.abacus_2','existing_aurelia_abacus2_licenses'),('software.pulse_1','pulse_licenses_on_new_aurelia_plus')]:
   n=cohort['applications'].get(key,0)
   if n:
    ps=snap(ref,max(1978,int(m[:4])-(int(m[5:])<6)));rev(m,'standalone_applications',n*ps['retail_price_usd'],n*ps['revenue_after_fee_usd'],n,'Additional application cohort, priced once from the dated retail model.')
 # Match separately costed card allowance from investment model.
 for l in I['product_cost_links']:
  if l['month']==m and l['product_ref'] in ['device.apple2_expansion_card','device.s100_flexibus_card','device.apple2_video_card','device.s100_video_card']:
   ps=snap(l['product_ref'],l['cost_snapshot_year']);rev(m,'standalone_cards',l['units']*ps['retail_price_usd'],l['units']*ps['revenue_after_fee_usd'],l['units'],'Matches explicit 2% per-card allowance already costed in industrial model')
# Team software and additional network offerings: match exactly the costed cohort.
from market_outlook import team_units
for m in I['monthly_demand']:
 n=team_units(m)
 if not n:continue
 for ref,mult in [('software.aion_development_team',1),('bundle.aurelia_network_upgrade',1),('bundle.artemis_network_upgrade',1),('device.network_hub.8_port',.5)]:
  ps=snap(ref,1982 if m>='1982-06' or ref=='software.aion_development_team' else 1981)
  rev(m,'team_and_network',n*mult*ps['retail_price_usd'],n*mult*ps['revenue_after_fee_usd'],n*mult,'Team cohort; half equip four existing clients plus 8-port hub. Initial Team launch uses first available 1982 cost-based price as explicit launch proxy; no later retrospective reprice of other offers.')
# Academy throughput is already staffed/costed in the investment model.
course_refs={'fundamentals':'service.academy_regular_courses.course_1','fundamentals_abacus':'service.academy_regular_courses.course_2','business_workflow':'service.academy_regular_courses.course_3','developer':'service.academy_regular_courses.course_4','bpi':'service.bpi_training','pulse':'service.pulse_training'}
academy=[]
for cap in I['quarterly_capacity']:
 q=cap['quarter']
 if q not in Q or not cap['course_enrolments']:continue
 yy=int(q[:4]);price_year=max(1978,yy-(q.endswith('Q1')));mix=defaultdict(float)
 for r in inputs['academy_requests']:
  if qr(r['month'])==q:
   for k,v in r['courses'].items():mix[k]+=v['requested_enrolments']
 if not sum(mix.values()):mix.update({'fundamentals':.35,'fundamentals_abacus':.25,'business_workflow':.15,'developer':.10,'bpi':.10,'pulse':.05 if yy>=1980 else 0})
 norm=sum(mix.values());gross=fundamental_count=0
 for course,w in mix.items():
  if not w:continue
  n=cap['course_enrolments']*w/norm;ps=snap(course_refs[course],price_year);gross+=n*ps['retail_price_usd']
  if course=='fundamentals':fundamental_count=n;fundamental_price=ps['retail_price_usd']
 revenueq[q]['gross']+=gross;revenueq[q]['net']+=gross;revenueq[q]['academy_tuition']+=gross
 academy.append({'quarter':q,'enrolments':cap['course_enrolments'],'gross_tuition_usd':money(gross),'fundamentals_enrolments':round(fundamental_count,2),'fundamentals_price_usd':fundamental_price,'basis':'Existing modeled course throughput; requested-course mix where available, otherwise explicit 35/25/15/10/10/5 mix normalized. Direct tuition has no ComputerLand fee. Teaching payroll already included.'})
# Marketing: itemized nominal allowances, no assertion of signed contracts.
items=[]
def add(q,e,category,program,qty,rate,basis,treatment='expense',source=None):
 items.append({'id':f'mkt.{len(items)+1:03}','quarter':q,'entity':e,'cost_type':category,'programme':program,'quantity':qty,'unit_cost_usd':rate,'central_usd':money(qty*rate),'low_usd':money(qty*rate*.65),'high_usd':money(qty*rate*1.75),'treatment':treatment,'basis':basis,'source_ref':source,'status':'New planning allowance; not an agreed contract or historical invoice'})
for q in Q:
 if q<'1975-Q1':continue
 yy=int(q[:4]);esc=1.08**(yy-1978)
 if q<'1977-Q4':
  add(q,'Logix','brand_pr_oem_outreach','Foundations',1,5000*esc,'Brand materials and partner prospecting; no public unreleased-product claims')
  continue
 if q<'1978-Q2':
  add(q,'Logix','launch_planning_agency','Aurelia preparation',1,35000*esc,'External launch planning; existing staff payroll remains in investment model')
  continue
 net=revenueq[q]['computer_baskets'];bpi=revenueq[q]['bpi_licenses']
 # At least 5 served launch markets, expand to 20 by 1980; no national-network reach claims.
 markets={1978:5,1979:12,1980:20,1981:20,1982:20}[yy];slots=80 if q.endswith('Q2') else 50
 add(q,'Logix','paid_tv_airtime','Regional television',markets*slots,750*esc,'60-second equivalent regional spots; markets × insertions; media rate is a planning assumption')
 add(q,'Logix','print_advertising','Business and trade press',12 if q.endswith(('Q2','Q4')) else 8,6000*esc,'Equivalent full-page placements; titles and insertion orders not yet contracted')
 add(q,'Logix','dealer_coop_advertising','Dealer merchandising',net,.02,'2% of supplier basket revenue; new allowance, separate from 25% channel fee. Apple archival 5% sales plan is a scale comparator, not Logix contract.')
 add(q,'Logix','agency_media_management','Media management',1,(markets*slots*750*esc+6000*esc*(12 if q.endswith(('Q2','Q4')) else 8))*.12,'12% external media/creative administration allowance on bought media')
 add(q,'Logix','direct_mail_brochures','Lead response',max(2000,net/500),1.5*esc,'Printed product brochures and postage; not product manuals')
 add(q,'Logix','external_pr_research','PR and measurement',3,8000*esc,'External PR retainer and response research; no extra sales uplift assumed')
 add(q,'Logix','dealer_roadshows','Regional demonstrations',markets,6000*esc,'Venue/demo rentals, freight and travel; payroll already budgeted')
 add(q,'AION Software','developer_marketing','Application and developer outreach',1,30000*esc,'External workshops, developer literature and demo distribution; core engineering excluded')
 add(q,'AION Labs','oem_silicon_marketing','Semiconductor partner outreach',1,10000*esc,'Trade literature and partner travel; process-transfer engineering already budgeted')
 add(q,'DRI','oem_cpm_marketing','CP/M OEM outreach',1,8000*esc,'Partner marketing and documentation promotion; software maintenance excluded')
 add(q,'BPI','accountant_dealer_marketing','Independent BPI campaign',1,15000*esc+bpi*.025,'Accountant demos, case studies, dealer qualification and specialist events; engineering/payroll already included')
 add(q,'BPI','upgrade_credit_redemptions','BPI upgrade promotion',bpi,.02,'Expected credits provision at 2% of BPI receipts; no additional upgrade revenue assumed','contra_revenue')
for q,n,e,amt,desc in [('1978-Q1','Aurelia commercial preproduction','Logix',40000,'Script, casting approach, location/design and storyboards'),('1978-Q2','Aurelia celebrity contract','Logix',200000,'Michael Douglas is only a fictional proposed lead; allowance for negotiation and usage, not an actual fee'),('1978-Q2','Aurelia film production','Logix',150000,'60-second film, crew, sets, shoot and post-production'),('1978-Q2','Aurelia music and rights','Logix',25000,'Music, releases and regional usage clearance'),('1978-Q2','Aurelia versions and masters','Logix',20000,'Regional end cards and broadcast masters'),('1979-Q2','Commercial usage renewal','Logix',75000,'Conditional continued rights/edits; not assumed perpetual celebrity permission'),('1979-Q4','Aurelia+ creative refresh','Logix',100000,'New demonstrations, print creative and TV versions; no second celebrity assumed'),('1980-Q1','Artemis campaign preparation','Logix',60000,'Agency, storyboards, qualified demonstrations and preview materials'),('1980-Q2','Artemis commercial production','Logix',180000,'New production and post; no celebrity contract assumed'),('1980-Q4','Abacus 3 / Pulse 3 creative','AION Software',60000,'Product film and print creative; no invented launch software sales')]:
 add(q,e,'commercial_production_rights',n,1,amt,desc,source='generated/catalogs/aurelia-1978-campaign.json' if 'Aurelia commercial'in n or q<'1979-Q1' else 'generated/catalogs/ncc-1980-campaign.json' if q>='1980-Q1' else 'generated/catalogs/comdex-1979-campaign.json')
conferences=[('1978-Q2','NCC 1978',1,'generated/catalogs/aurelia-1978-campaign.json'),('1979-Q2','NCC 1979',1.15,'generated/catalogs/ncc-1979-campaign.json'),('1979-Q4','COMDEX 1979',1.2,'generated/catalogs/comdex-1979-campaign.json'),('1980-Q2','NCC 1980',1.4,'generated/catalogs/ncc-1980-campaign.json'),('1980-Q4','COMDEX 1980',1.3,'generated/catalogs/ncc-1980-campaign.json')]
for q,name,scale,source in conferences:
 for category,qty,rate,basis in [('exhibit_venue',1,45000,'Exhibition space, session rooms and venue services'),('booth_signage',1,35000,'Booth fabrication/rental, furnishings and signage'),('stage_av_projection',1,40000,'Staging, PA, projection rental and specialist video-conversion services'),('rehearsal_demo_rental',1,18000,'Rehearsal room and backup/demo-system rentals; purchased Academy assets not charged again'),('recording_crew',4,7000,'Four production days, multicamera/audio crew; professional filming'),('editing_broadcast_rights',1,35000,'Post-production, clearances, full-session and station-ready edits'),('press_hospitality',1,12000,'Press kits, briefing room and modest hospitality'),('travel_lodging',30,1200,'Thirty travelling participants; travel/lodging, not wages'),('freight_drayage',1,18000,'Exhibition freight, handling, insurance and on-site logistics'),('contract_event_staff',1,12000,'Temporary booth/registration staff; permanent employees already funded'),('station_copies_dispatch',150,70,'Voluntary station copies supplied free; zero airtime purchase/content revenue here')]:
  add(q,'Logix',category,name,qty,rate*scale,basis,source=source)
 for entity,amount in [('AION Software',15000),('BPI',10000),('DRI',8000),('AION Labs',8000)]:add(q,entity,'partner_sessions_travel',name,1,amount*scale,'Separate partner clinics/travel; no duplicate shared-booth charge',source=source)
 add(q,'Logix','event_contingency',name,1,scale*15000,'Explicit event contingency; not a percentage layered into other items',source=source)
# Integrate accepted Team campaign; reallocate existing developer outreach first.
team_campaign=[]
for q,gross in [('1981-Q3',36000),('1981-Q4',178000),('1982-Q1',62000)]:
 remaining=gross;credit=0
 for item in items:
  if item['quarter']==q and item['cost_type']=='developer_marketing':
   used=min(remaining,item['central_usd']);credit+=used;remaining-=used
   item['central_usd']=money(item['central_usd']-used);item['quantity']=1;item['unit_cost_usd']=item['central_usd'];item['low_usd']=money(item['central_usd']*.65);item['high_usd']=money(item['central_usd']*1.75)
   item['basis']+='; Team campaign reallocation deducted to prevent duplication.'
 add(q,'AION Software','team_campaign','Team Edition campaign',1,gross,'Accepted pilot, dealer, COMDEX and follow-up budget including contingency; replaces allocated developer outreach.',source='generated/catalogs/team-development-program.json')
 team_campaign.append({'quarter':q,'gross_campaign_usd':gross,'existing_marketing_reallocated_usd':money(credit),'incremental_campaign_usd':money(gross-credit)})
# Tuition purchase credits: recognize expected redemptions in a one-quarter lag, once as contra-revenue.
for a in academy:
 idx=Q.index(a['quarter'])+1
 if idx>=len(Q):continue
 add(Q[idx],'Logix','academy_purchase_credit','Learn before you decide',a['fundamentals_enrolments']*.35,a['fundamentals_price_usd']*.5,'35% redemption assumption; 50% Fundamentals tuition credit, one-quarter lag within six-month validity. No separate course subsidy duplicated.','contra_revenue','generated/catalogs/aurelia-1978-campaign.json')
# Incremental Mono Pro campaign only; baseline Artemis film and conference remain above.
display_revision=json.load(open(R/'generated/catalogs/artemis-display-revision.json'))
for q,category,amount,basis in [('1980-Q1','commercial_production_rights',35000,'Additional Mono Pro demonstration footage and print masters'),('1980-Q2','stage_av_projection',25000,'Incremental NCC high-resolution demonstrations and video conversion; not a second conference'),('1980-Q2','dealer_training_materials',40000,'Dealer materials, external sessions and travel; no duplicate demo-computer purchase or permanent payroll'),('1980-Q2','print_advertising',60000,'Additional high-resolution office/productivity placements'),('1980-Q2','paid_tv_airtime',75000,'Incremental regional Mono Pro commercial airtime'),('1980-Q3','paid_tv_airtime',75000,'Follow-up regional campaign'),('1980-Q3','print_advertising',40000,'Follow-up business press'),('1980-Q3','dealer_roadshows',30000,'Additional display demonstrations, rentals and travel'),('1980-Q4','stage_av_projection',25000,'Incremental COMDEX Mono Pro demonstration'),('1980-Q4','print_advertising',30000,'Year-end display campaign')]:
 add(q,'Logix',category,'Mono Pro incremental campaign',1,amount,basis+'; unquoted planning budget; combined intent effect is applied once in sales.',source='generated/catalogs/artemis-display-revision.json')
for q,amount in display_revision['incremental_marketing_usd'].items():assert sum(x['central_usd'] for x in items if x['quarter']==q and x['programme']=='Mono Pro incremental campaign')==amount
marketingq={q:{'expense_usd':money(sum(x['central_usd'] for x in items if x['quarter']==q and x['treatment']=='expense')),'contra_revenue_usd':money(sum(x['central_usd'] for x in items if x['quarter']==q and x['treatment']=='contra_revenue'))} for q in Q}
# Source operating costs already include a generic campaign line: replace, never stack.
# Depreciation is a planning charge; investment cash remains actual quarterly capex schedule.
assets=[]
for a in I['capital_schedule']:
 if a['quarter'] not in Q:continue
 typ=a['cost_type'];life=20 if 'building' in typ else 10 if typ=='fab_equipment' else 7 if 'fitout'in typ else 5
 match=re.search(r'commissioned (\d{4}-Q[1-4])',a['basis']);ready=match.group(1) if match else a['quarter']
 assets.append(dict(a,service_quarter=ready,useful_life_years=life,depreciation_method='Straight line, zero salvage; begins quarter after service; construction-in-progress not depreciated'))
results=[];annual=[]
for scenario in [{'id':'low_marketing','factor':.65},{'id':'central','factor':1},{'id':'high_marketing','factor':1.75}]:
 cumulative_cash=cumulative_cap=cumulative_dep=cumulative_ebit=cumulative_revenue=0;peakfunding=0;previous_assets=0;previous_inventory=0;payback=None
 rows=[]
 for q in Q:
  er=[x for x in I['quarterly_entity_costs'] if x['quarter']==q];capacity=next(x for x in I['quarterly_capacity'] if x['quarter']==q)
  sourceopex=sum(x['operating_usd'] for x in er);oldmarketing=sum(x['cost_type_usd'].get('campaign_dealer_enablement',0) for x in er)
  internalroyalty=sum(x['usd'] for x in I['interentity_transfers'] if x['quarter']==q and x['type']=='provisional CP/M royalty')
  marketing=marketingq[q]['expense_usd']*scenario['factor'];credits=marketingq[q]['contra_revenue_usd']*scenario['factor']
  revenue_net=revenueq[q]['net']-credits;opex=sourceopex-oldmarketing-internalroyalty+marketing
  depreciation=sum(a['usd']/(a['useful_life_years']*4) for a in assets if a['service_quarter']<q and (int(q[:4])-int(a['service_quarter'][:4]))*4+int(q[-1])-int(a['service_quarter'][-1])<=a['useful_life_years']*4)
  capex=sum(x['capital_usd'] for x in er);inventory=capacity['gross_inventory_funding_usd'];change=inventory-previous_inventory
  ebitda=revenue_net-opex;ebit=ebitda-depreciation;fcf=ebitda-capex-change
  cumulative_cash+=fcf;cumulative_cap+=capex;cumulative_dep+=depreciation;cumulative_ebit+=ebit;cumulative_revenue+=revenue_net
  peakfunding=max(peakfunding,-cumulative_cash);endassets=cumulative_cap-cumulative_dep+inventory;avgassets=(previous_assets+endassets)/2
  if peakfunding>0 and cumulative_cash>=0 and payback is None:payback=q
  recost=sum(l['units']*l['unit_cost_usd'] for l in I['product_cost_links'] if l['quarter']==q)-internalroyalty
  row={'quarter':q,'computer_units':capacity['customer_computers'],'customer_gross_usd':money(revenueq[q]['gross']),'channel_fees_usd':money(revenueq[q]['channel']),'promotional_credits_usd':money(credits),'net_revenue_usd':money(revenue_net),'revenue_streams_usd':{k:money(revenueq[q][k]) for k in ['computer_baskets','standalone_applications','standalone_cards','bpi_licenses','academy_tuition','team_and_network']},'source_operating_expenses_usd':money(sourceopex),'replaced_generic_marketing_usd':money(oldmarketing),'eliminated_internal_royalties_usd':money(internalroyalty),'recurring_product_cost_reference_usd':money(recost),'other_resource_costs_usd':money(opex-marketing-recost),'marketing_expense_usd':money(marketing),'total_marketing_and_credits_usd':money(marketing+credits),'operating_cash_cost_usd':money(opex),'ebitda_usd':money(ebitda),'depreciation_usd':money(depreciation),'operating_profit_ebit_usd':money(ebit),'capex_usd':money(capex),'inventory_balance_usd':money(inventory),'inventory_cash_change_usd':money(change),'free_cash_flow_usd':money(fcf),'cumulative_net_cash_usd':money(cumulative_cash),'cumulative_capex_usd':money(cumulative_cap),'cumulative_operating_profit_usd':money(cumulative_ebit),'cumulative_net_revenue_usd':money(cumulative_revenue),'end_operating_assets_usd':money(endassets),'average_operating_assets_usd':money(avgassets),'quarterly_pretax_roi_pct':round(ebit/avgassets*100,3) if avgassets>0 else None,'cumulative_accounting_roi_pct':round(cumulative_ebit/(cumulative_cap+inventory)*100,3) if cumulative_cap+inventory>0 else None,'peak_external_funding_usd':money(peakfunding),'cumulative_cash_return_on_peak_funding_pct':round(cumulative_cash/peakfunding*100,3) if peakfunding>0 else None,'period_status':'Current demand, dated retail prices and matched manufacturing capacity'}
  rows.append(row);previous_assets=endassets;previous_inventory=inventory
 results.append({'id':scenario['id'],'marketing_multiplier':scenario['factor'],'quarterly':rows,'first_cash_payback_quarter':payback,'sales_uplift_from_marketing_budget':0,'sensitivity_basis':'Only marketing expense/credit budget changes. No invented causal sales response.'})
 if scenario['id']=='central':
  for y in range(1974,1983):
   rr=[r for r in rows if r['quarter'].startswith(str(y))];annual.append({'year':y,**{k:money(sum(r[k] for r in rr)) for k in ['net_revenue_usd','operating_cash_cost_usd','total_marketing_and_credits_usd','operating_profit_ebit_usd','capex_usd','free_cash_flow_usd']},'ending_cumulative_cash_usd':rr[-1]['cumulative_net_cash_usd']})
sources=['generated/models/industrial-investment-1974-1981.json','generated/models/sales-forecast.json','generated/models/pricing-results.json','generated/catalogs/aurelia-1978-campaign.json','generated/catalogs/ncc-1979-campaign.json','generated/catalogs/comdex-1979-campaign.json','generated/catalogs/ncc-1980-campaign.json','generated/catalogs/team-development-program.json']
marketing_model={'metadata':{'title':'Marketing and conference budget 1974–1982','currency':'nominal USD','status':'New scenario allowances supplement the previously unbudgeted campaign specifications'},'items':items,'quarterly':marketingq,'coverage':{'included':['Commercial development, proposed talent rights, production, editing, music and broadcast versions','Paid regional TV and print media, agency management, PR, direct mail','Conference venue, booth, staging/projection, rehearsal, recording, editing, press, travel, drayage, temporary staff and contingency','Free station-copy supply and dispatch; no guaranteed editorial airtime','Dealer co-op, roadshows, developer/OEM clinics, BPI accountant/dealer promotion','Academy purchase credits and BPI upgrade credit provision'], 'already_funded_not_recharged':['Permanent company and marketing-adjacent staff payroll','Product/compatibility/porting engineering and BPI validation','Academy buildings, demonstration classroom computers and instructors','Customer product manuals/media in manufacturing costs','ComputerLand channel fees in net sales'], 'limits':['Celebrity availability, fee and usage rights are fictional proposed arrangements, not verified contract terms','No causal campaign ROI or marketing-created sales increment can be estimated without a no-marketing counterfactual','Terminal Q4 1980 course credit redemptions can occur in 1981; no 1981 cash cost is silently pulled into 1980']} }
M={'metadata':{'title':'Project ROI and cash flow, 1974–1982','currency':'nominal USD','scope':'Five-entity project ecosystem, pre-tax and unlevered; not shareholder ROI or consolidated legal accounts','scenario':'Full-demand central industrial plan; historical constrained-delivery forecasts retained as reference only','source_commit_reviewed':'8b4b09b2b708453376d0952a6db190889f130e21','horizon':'1974-Q1–1982-Q4','accounting_status':'Planning cash-cost and depreciation bridge, not audited GAAP financial statements'},'definitions':{'quarterly_pretax_roi':'Quarter EBIT / average opening and closing operating assets (net modeled fixed assets including CIP + inventory). Nonannualized pre-tax ROIC proxy; no tax assumption.','cumulative_accounting_roi':'Cumulative EBIT / (cumulative capex + ending inventory). Custom since-inception accounting ROI, not annualized; do not compare directly with quarterly ROI.','cumulative_cash_return':'Cumulative free cash flow / peak external funding requirement to date. Includes pre-revenue losses; excludes terminal asset-sale value. During maximum funding draw the ratio can be -100%.','free_cash_flow':'Net revenue − cash operating costs − capex − change in inventory. Depreciation is deducted only for EBIT, not cash flow.','net_revenue':'Customer spend less channel fees and expected promotional credits; BPI independent sales and Academy direct tuition included once.','operating_assets':'Net fixed assets plus gross inventory. No AR, AP, debt, excess cash or legal-entity tax balance sheet is supplied.','peak_external_funding':'Maximum cumulative negative free cash balance, starting at zero. Existing founder-equity commitments finance this requirement; they are not operating returns.'},'assumptions':{'matching':'Revenue uses the same full-demand computer units as the industrial cost plan. Historical basket realization is preserved, not recalculated from a later catalog price. Original capacity-limited sales are only a reference; no hybrid ROI divides their revenue by expanded-demand costs.','academy':'Industrial-plan course volumes and staffing retained. Requested-course mix used where available; otherwise stated mix. Direct tuition charged once. Permanent teaching payroll already funded.','sales_end_1980':'November 19–December sales and quantities use the industrial extrapolation at the final forecast price. No invented Abacus 3/Pulse 3 incremental software sales.','working_capital':'Uses committed one-quarter-ahead inventory funding, including 1981 Q1 prebuild at 1980 year-end. Cash-sale/collection assumption and no supplier credit. No terminal inventory liquidation.','depreciation':'Straight-line zero-salvage planning lives: buildings 20y, fab tools 10y, fitout 7y, other equipment 5y; quarter after service. Explicit fab commissioning dates prevent depreciation of construction in progress.','marketing':'Replace existing generic campaign/dealer expense in the ROI bridge; underlying historical industrial file remains an independently reproducible baseline. Credits are contra-revenue, other marketing is expense.','ownership':'No company-specific ROI is asserted: Logix/AION basket revenue sharing, semiconductor transfer prices and several licences remain unspecified. Costs/marketing retain entity attribution; internal DRI royalties/reimbursements are eliminated in ecosystem totals.','exclusions':['Income/payroll taxes beyond existing loaded wages, interest/debt schedules, shareholder distributions, new acquisition/equity valuations','Receivables/payables collection effects, VAT/sales tax and Danish FX','Unforecast OEM sales, unsupported product revenues and terminal asset value','Unknown acquisition/replacement cost of future equipment in the secret facility'],'1981_extension':'Conditional full-demand forecast; 1981 basket prices use current dated balanced prices, PRO begins July. No 1982–83 revenue or ROI is asserted. Future process budgets are disclosed separately.', 'bounds':'Marketing sensitivity is 0.65×/1×/1.75× planned spending only. It does not cover all sales, BOM or fab-yield uncertainty.'},'scenarios':results,'annual_central':annual,'monthly_revenue_links':revenue,'academy_revenue':academy,'marketing':marketing_model,'asset_depreciation_schedule':assets,'sources':[{'path':f,'sha256':hashlib.sha256(document_bytes(f, root=R)).hexdigest()} for f in sources],'historical_context':[{'url':'https://archive.computerhistory.org/resources/text/2009/102712693.05.01acc.pdf','title':'Apple marketing plan (archival primary document)','use':'Supports period mix of press, dealer co-op, demonstrations, PR and direct mail; proposed dealer co-op was 5% of sales. Model uses 2% of net basket receipts as its own assumption, not a quoted Logix rate.'},{'url':'https://www.sec.gov/Archives/edgar/data/1024478/000102447816000068/fy16ex99.htm','title':'Issuer ROIC reconciliation filed with SEC','use':'Illustrates explicit numerator/denominator reconciliation and that ROIC definitions differ. This project uses a clearly labelled pre-tax operating-assets proxy, not that issuer’s after-tax measure.'}]}
M['team_campaign_reconciliation']=team_campaign
M['memory_manufacturing']=I.get('memory_manufacturing',{})
M['assumptions']['working_capital']='One-quarter-ahead inventory funding through 1982; terminal inventory retained without liquidation. Cash collection and no supplier credit remain planning assumptions.'
M['assumptions']['matching']='Current 1980–82 reaction demand matches industrial production and revenue exactly. Earlier basket realization is retained; later prices use dated June snapshots. June snapshots proxy the whole June month. No historical 1982 competitor quote is asserted.'
M['assumptions']['1981_extension']='Reassessed demand through December 1982 from market_outlook.py. Dated balanced prices, 1982 process investment and Team costs included. Initial Team price uses first available 1982 snapshot; no volume savings from the unproven 2 um ramp.'
M['metadata']['scenario']='Single current sales forecast through 1982; matching quantities and prices across sales and ROI.'
M['assumptions']['matching']='Computer-package revenue is read directly from current sales monthly totals. BPI and other non-basket streams are added separately once.'
M['assumptions']['sales_end_1980']='All current monthly sales use dated retail pricing; no superseded constrained-delivery series is included.'
M['display_revision']={'policy':display_revision,'interpretation':'Current hardware and manufacturing policy; ERAv1 remains at 3 um. Current sales and ROI use the same dated retail prices.'}
(R/'generated/models/artemis-display-impact.json').write_text(json.dumps(M['display_revision'],indent=2)+'\n')
(R/'generated/models/marketing-budget-1974-1980.json').write_text(json.dumps(marketing_model,indent=2)+'\n');(R/'generated/models/roi-1974-1980.json').write_text(json.dumps(M,indent=2)+'\n')
site=read('generated/catalogs/site-pages.json');pages={p['id']:p for p in site['pages']};nav=''.join('<a href="'+html.escape(pages[i]['path'])+'"'+(' aria-current="page"' if i=='roi' else '')+'>'+html.escape(pages[i]['title'])+'</a>' for i in site['navigation'])
display_section='<section class="panel"><h2>Current sales and pricing</h2><p>Computer-package revenue matches the single current sales forecast. Standalone software, BPI, cards and Academy receipts are added separately. <a href="sales.html">Sales and contribution</a></p></section>'
template=R/'tools/roi_template.html'
if template.exists():(R/'roi.html').write_text(template.read_text().replace('__NAV__',nav).replace('__MODEL__',json.dumps(M).replace('</','<\\/')).replace('__DISPLAY_REVISION__',display_section))
print(json.dumps({'annual':annual,'end_1981':results[1]['quarterly'][-1],'payback':results[1]['first_cash_payback_quarter'],'marketing_items':len(items)},indent=2))


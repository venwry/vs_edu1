"""Rebuild 1980–83 sales, contract economics, ROI bridge and quarterly unit shares.
Frozen baseline makes reruns idempotent. All new commercial terms are scenarios.
"""
import json,math,calendar,hashlib,html
from pathlib import Path
from collections import defaultdict
from copy import deepcopy
R=Path(__file__).resolve().parents[1]
read=lambda n:json.loads((R/n).read_text())
def save(n,x):(R/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def money(v):return round(v+1e-9,2)
def qtr(m):return m[:4]+'-Q'+str((int(m[5:7])-1)//3+1)
def allocate(n,weights):
 if not n:return dict.fromkeys(weights,0)
 total=sum(weights.values());raw={k:n*v/total for k,v in weights.items()};a={k:int(v) for k,v in raw.items()}
 for k in sorted(raw,key=lambda k:raw[k]-a[k],reverse=True)[:n-sum(a.values())]:a[k]+=1
 return a
B=read('baselines/sales-roi-baseline-1982.json');I=read('generated/catalogs/sales-reassessment-inputs.json');P=read('generated/models/pricing-results.json');C=read('generated/models/retail-catalog-1982-results.json');D=read('generated/models/manufacturing-costs.json')['reviews']['comdex-1982']
oldS=next(s for s in B['sales']['scenarios'] if s['id']=='central');oldR=next(s for s in B['roi']['scenarios'] if s['id']=='central')
oldmonths={r['month']:r for r in oldS['monthly']};oldquarters={r['quarter']:r for r in oldS['quarterly']};oldroi={r['quarter']:r for r in oldR['quarterly']};annual={p['id']:p for p in P['products']};nov={p['id']:p for p in D['prices']}
F=['customer_retail_spend_usd','supplier_revenue_after_channel_usd','recurring_cost_usd','unit_contribution_total_usd'];families=['aurelia','aurelia_plus','artemis','artemis_pro']
def unit(ref,m):
 date=m+'-28'
 if ref.startswith('bundle.artemis_budget_128'):
  p=annual[ref];choices=[v for v in list(p['snapshots'].values())+[p['launch_snapshot']]+p.get('dated_snapshots',[]) if v.get('retail_price_usd') is not None and v['date']<=date];v=max(choices,key=lambda v:v['date']);return v['retail_price_usd'],v['revenue_after_fee_usd'],v['manufacturing_cost_usd'],v['date'],'Dated budget assessment; launch/Abacus/NIC gates retained'
 if ref.startswith('solution.'):
  assert m>='1982-12'
  p=next(p for p in C['snapshots']['1982-12-15']['solutions'] if p['id']==ref.split('.',1)[1]);v=p['pricing']
  return v['amount_usd'],v['amount_usd']-v['dealer_fee_usd'],v['cost_usd'],'1982-11-29','Accepted task configuration; known priced contents only where final quotation requirements remain'
 if m>='1982-12' and ref in nov:
  p=nov[ref];return p['retail_price_usd'],p['retail_price_usd']-(p['dealer_fee_usd'] or 0),p['manufacturing_cost_usd'],p['date'],p['pricing_status']
 dates=[d for d in C['snapshots'] if d<=date];view=C['snapshots'][max(dates)] if dates else None
 if view:
  row=next((p for p in view['current_offer_prices'] if p['ref']==ref),None)
  if row:return row['retail'],row['retail']-row['fee'],row['cost'],row['date'],row['basis']
 p=annual[ref];assert p['offering_start']<=date,(ref,m)
 snapshots=[s for s in p['snapshots'].values() if s['retail_price_usd'] is not None];before=[s for s in snapshots if s['date']<=date];s=max(before,key=lambda s:s['date']) if before else min(snapshots,key=lambda s:s['date'])
 return s['retail_price_usd'],s['revenue_after_fee_usd'],s['manufacturing_cost_usd'],s['date'],'Dated assessment; conditional shipment assumption where announced'
weights={
 'aurelia':[('bundle.proposed_aurelia_office',.7),('bundle.proposed_aurelia_accounts',.2),('bundle.proposed_aurelia_developer',.1)],
 'aurelia_plus':[('bundle.proposed_aurelia_plus_office',.6),('bundle.proposed_aurelia_plus_accounts',.25),('bundle.proposed_aurelia_plus_developer',.1),('bundle.proposed_aurelia_plus_analysis',.05)],
 'artemis':[('bundle.proposed_artemis_office',.4),('bundle.proposed_artemis_office_color',.1),('bundle.proposed_artemis_accounts',.2),('bundle.proposed_artemis_developer',.15),('bundle.proposed_artemis_analysis',.1),('bundle.proposed_artemis_migration',.05)],
 'artemis_pro':[('bundle.artemis_pro_512_server',.65),('bundle.artemis_pro_1mb_server',.35)]}
def line(ref,n,m,family,scope):
 gross,net,cost,date,basis=unit(ref,m);assert cost is not None,(ref,m)
 g=money(n*gross);r=money(n*net);c=money(n*cost)
 return {'family':family,'product_ref':ref,'quantity':n,'snapshot_year':int(date[:4]),'snapshot_proxy':date>m+'-28','assessment_date':date,'basis':basis,'scope':scope,'unit_retail_usd':gross,'unit_after_channel_usd':net,'unit_recurring_cost_usd':cost,**dict(zip(F,[g,r,c,money(r-c)]))}
def totals(lines):return {k:money(sum(l[k] for l in lines)) for k in F}
def cohort(name,y,q,mindex):
 n=I[name].get(str(y),[0]*4)[q-1]
 if y==1982 and q==4 and name.startswith('cad'):return n if mindex==2 else 0
 if y==1982 and q==2 and name in ['colour_upgrade_units','mouse_only_learning_units']:return n if mindex==2 else 0
 if y==1981 and q==4 and name=='team_paid_licenses':return [0,round(n/3),n-round(n/3)][mindex]
 return allocate(n,{0:1,1:1,2:1})[mindex]
scenarios=[];roi_cases=[];markets=[];all_contracts=[]
for sid,settings in I['scenarios'].items():
 scale=settings['volume'];rows=deepcopy([r for r in oldS['monthly'] if r['month']<'1980-01']);contract_rows=[];qdetails={}
 for y in [1980,1981,1982,1983]:
  for q in range(1,5):
   key=f'{y}-Q{q}';anchor=oldquarters[f'{min(y,1982)}-Q{q}'];clone_units={p['id']:round(p['quarterly_units'].get(key,0)*scale) for p in I['clones']}
   lost=round(sum(clone_units[p['id']]*I['cannibalisation']['US' if p['country']=='US' else 'other'] for p in I['clones']))
   gross=round(anchor['computer_units']*I['logix_gross_factors_vs_baseline'][str(y)][q-1]*scale);n=max(0,gross-lost)
   if y==1980 and q==1:gross=n=anchor['computer_units'] # frozen pre-launch history in every case
   # UK is inside Logix total; clone machines are disjoint and excluded from Logix sales.
   uk=round(I['aion_tech_uk_subset'].get(str(y),[0]*4)[q-1]*scale)
   shares=anchor['products'] if y<1983 else {'aurelia':.005,'aurelia_plus':1-I['native_share_1983'][q-1]-.005,'artemis':I['native_share_1983'][q-1]-I['pro_share_1983'][q-1],'artemis_pro':I['pro_share_1983'][q-1]}
   products=allocate(n,shares)
   if y in [1981,1982]:
    shift=min(products['aurelia_plus'],round(n*(.10 if y==1981 else .15)));products['aurelia_plus']-=shift;products['artemis']+=shift
   monthly_products={f:allocate(products[f],{j:oldmonths[f'{min(y,1982)}-{(q-1)*3+j+1:02}']['products'][f] for j in range(3)}) for f in families}
   if y==1980 and q==2:
    for f in families:
     first=oldmonths['1980-04']['products'][f];rest=allocate(products[f]-first,{j:oldmonths[f'1980-{5+j:02}']['products'][f] for j in range(2)});monthly_products[f]={0:first,1:rest[0],2:rest[1]}
   qdetails[key]={'gross_logix_intent':gross,'cannibalised_by_clones':lost,'clone_units':clone_units,'aion_tech_uk_subset':uk}
   for j in range(3):
    m=f'{y}-{(q-1)*3+j+1:02}';prod={f:monthly_products[f][j] for f in families};lines=[];addons=[]
    if m<'1980-05':
     rows.append(deepcopy(oldmonths[m]));continue
    cad=round(cohort('cad_new_systems',y,q,j)*scale);assert cad<=prod['artemis_pro']
    for family,count in prod.items():
     normal=count-(cad if family=='artemis_pro' else 0)
     mix=dict(weights[family])
     if family=='artemis':
      if m<'1981-01':mix={'bundle.proposed_artemis_office':.6,'bundle.proposed_artemis_developer':.25,'bundle.proposed_artemis_migration':.15}
      bm=I['budget_mix'][str(y)];mix={k:v*(1-bm['floppy']-bm['hdd']) for k,v in mix.items()};mix['bundle.artemis_budget_128']=bm['floppy'];mix['bundle.artemis_budget_128_hdd']=bm['hdd']
     if m>='1982-12' and family=='artemis':
      mix['solution.office_professional']=mix.pop('bundle.proposed_artemis_office')
      mix['solution.business_accounts']=mix.pop('bundle.proposed_artemis_accounts')
     allocations=allocate(normal,mix)
     for ref,quantity in allocations.items():
      if quantity:lines.append(line(ref,quantity,m,family,'Complete task bundle; component contents counted once'))
    if cad:lines.append(line('offer.comdex82_reference_hardware',cad,m,'artemis_pro','CAD host replaces ordinary PRO sale; Autodesk licence accounted outside project revenue'))
    for name,ref in [('team_paid_licenses','software.aion_development_team'),('colour_upgrade_units','offer.ncc82_colour_upgrade'),('mouse_only_learning_units','offer.ncc82_mouse_learning'),('cad_upgrade_licenses','offer.comdex82_professional_hardware')]:
     quantity=round(cohort(name,y,q,j)*scale)
     if quantity:addons.append(line(ref,quantity,m,'existing_owner' if name!='team_paid_licenses' else 'team_software','Separate cohort; no computer unit, no additional bundled mouse or sponsored Autodesk licence counted'))
    cadlic=cad+round(cohort('cad_upgrade_licenses',y,q,j)*scale)
    rows.append({'month':m,'period_start':m+'-01','period_end':m+'-'+str(calendar.monthrange(y,int(m[5:]))[1]),'products':prod,'computer_units':sum(prod.values()),'team_licenses':round(cohort('team_paid_licenses',y,q,j)*scale),'autocad_licenses':cadlic,'autodesk_independent_retail_spend_usd':cadlic*1000,'basis':'Reassessed purpose-bundle demand, explicit clone cannibalisation and CAD host substitution. Shipment assumptions conditional on acceptance.',**totals(lines),'pricing_links':lines,'additional_offer_links':addons,'additional_offers':totals(addons)})
   # OEM receipts: chipset supply OR SGS royalty; never both on the same chipset.
   eco=I['oem_economics'];native=I['clone_native_share'].get(str(y),[0]*4)[q-1];aion=eco['aion_supply_fraction'].get(str(y),[0]*4)[q-1]
   for partner in I['clones']:
    units=clone_units[partner['id']]
    if not units:continue
    transfer=(1-native)*eco['aurelia_chipset_transfer_usd']+native*eco['artemis_chipset_transfer_usd'];chip=units*aion*transfer;royalty=units*(1-aion)*transfer*settings['royalty'];software=units*eco['platform_software_fee_usd'];cost=chip*eco['chipset_recurring_cost_fraction']+units*eco['platform_software_delivery_cost_usd']+royalty*eco['sgs_audit_cost_fraction']
    contract_rows.append({'quarter':key,'manufacturer':partner['name'],'manufacturer_id':partner['id'],'country':partner['country'],'computer_units':units,'native_units':round(units*native),'aion_chipsets':round(units*aion,3),'sgs_chipsets':round(units*(1-aion),3),'chipset_receipts_usd':money(chip),'platform_software_receipts_usd':money(software),'sgs_royalty_usd':money(royalty),'project_revenue_usd':money(chip+software+royalty),'project_recurring_cost_usd':money(cost),'whole_computer_royalty_usd':0,'partner_computer_retail_revenue_included':False})
 def aggregate(key):
  groups=defaultdict(list)
  for row in rows:groups[key(row['month'])].append(row)
  return [dict(period=k,products={f:sum(r['products'][f] for r in rr) for f in families},computer_units=sum(r['computer_units'] for r in rr),team_licenses=sum(r['team_licenses'] for r in rr),autocad_licenses=sum(r.get('autocad_licenses',0) for r in rr),**{f:money(sum(r[f] for r in rr)) for f in F}) for k,rr in sorted(groups.items())]
 quarterlies=[dict(r,quarter=r['period']) for r in aggregate(qtr)];annuals=[dict(r,year=int(r['period'])) for r in aggregate(lambda m:m[:4])]
 scenarios.append({'id':sid,'title':sid.title(),'monthly':rows,'quarterly':quarterlies,'annual':annuals});all_contracts.append({'id':sid,'quarterly':contract_rows})
 # Bridge the frozen industrial/ROI resource baseline into the revised forecast.
 # Additional costs replace old computer baskets, Team/network and BPI attach allowances.
 results=[];cumulative=capcum=depcum=ebitcum=revcum=0.;peak=0.;previous_inventory=0.;previous_assets=0.;payback=None;credit_balance=0.;new_assets=[]
 max_capacity=oldquarters['1979-Q4']['computer_units']*4
 for old in oldR['quarterly']:
  if old['quarter']<'1980-Q1':results.append(deepcopy(old))
 previous=results[-1];cumulative=previous['cumulative_net_cash_usd'];capcum=previous['cumulative_capex_usd'];ebitcum=previous['cumulative_operating_profit_usd'];revcum=previous['cumulative_net_revenue_usd'];previous_inventory=previous['inventory_balance_usd'];previous_assets=previous['end_operating_assets_usd'];depcum=capcum+previous_inventory-previous_assets;peak=previous['peak_external_funding_usd']
 capacity_funding=defaultdict(float);capacity_plan=[]
 for cq in qdetails:
  demand=next(r['computer_units'] for r in quarterlies if r['quarter']==cq)+sum(r['aion_chipsets']*.15 for r in contract_rows if r['quarter']==cq)
  required=demand*4*(1+I['capacity']['headroom']);extra=max(0,required-max_capacity)*I['capacity']['incremental_capex_per_extra_annualised_system']*settings['extra_cost'];max_capacity=max(max_capacity,required)
  py,pq=int(cq[:4]),int(cq[-1])-1
  if pq==0:py-=1;pq=4
  funding=f'{py}-Q{pq}'
  if extra:capacity_funding[funding]+=extra;capacity_plan.append({'service_quarter':cq,'funding_quarter':funding,'amount_usd':money(extra),'annualised_capacity_units':required})
 for q in qdetails:
  y=int(q[:4]);bq=f'{min(y,1982)}-Q{q[-1]}';base=oldroi[bq];olds=oldquarters[bq];rr=[r for r in rows if qtr(r['month'])==q];salesq=next(r for r in quarterlies if r['quarter']==q);factor=salesq['computer_units']/olds['computer_units'];infl=1.06 if y==1983 else 1
  addon=totals([l for r in rr for l in r.get('additional_offer_links',[])]);oem=[r for r in contract_rows if r['quarter']==q];oemnet=sum(r['project_revenue_usd'] for r in oem);oemcost=sum(r['project_recurring_cost_usd'] for r in oem)
  oldteam=olds.get('team_licenses',0);oldteamcost=0
  for ref,mult in [('software.aion_development_team',1),('bundle.aurelia_network_upgrade',1),('bundle.artemis_network_upgrade',1),('device.network_hub.8_port',.5)]:
   oldteamcost+=oldteam*mult*unit(ref,'1982-06')[2]
  bpi_net=base['revenue_streams_usd'].get('bpi_licenses',0);bp=unit('software.bpi_suite','1982-06');bpi_cost=bpi_net*bp[2]/bp[1]
  removed_net=base['revenue_streams_usd'].get('computer_baskets',0)+base['revenue_streams_usd'].get('team_and_network',0)+bpi_net
  othernet=(base['net_revenue_usd']-removed_net)*factor
  othercost=max(0,base['operating_cash_cost_usd']+base['eliminated_internal_royalties_usd']-olds['recurring_cost_usd']-oldteamcost-bpi_cost)*infl*(.65+.35*factor)
  programmes=[p for p in I['programme_costs'] if p['quarter']==q];expense=sum(p['amount_usd'] for p in programmes if p['category']=='expense')*settings['extra_cost'];credit_balance+=sum(p['amount_usd'] for p in programmes if p['category']=='working_capital')
  internal_royalty=10*(salesq['products']['aurelia']+salesq['products']['aurelia_plus'])
  costs=-internal_royalty+salesq['recurring_cost_usd']+addon['recurring_cost_usd']+oemcost+othercost+expense
  revenue=salesq['supplier_revenue_after_channel_usd']+addon['supplier_revenue_after_channel_usd']+oemnet+othernet
  if q=='1980-Q1':
   revenue=base['net_revenue_usd'];costs=base['operating_cash_cost_usd'];othernet=revenue-salesq['supplier_revenue_after_channel_usd'];othercost=costs+internal_royalty-salesq['recurring_cost_usd']
  equivalent=salesq['computer_units']+sum(r['aion_chipsets']*.15 for r in oem)
  extra_capex=capacity_funding[q]
  capex=base['capex_usd']*infl+extra_capex
  extra_dep=sum(a['amount']/20 for a in new_assets if a['quarter']<q)
  baseline_depreciation=base['depreciation_usd'] if y<1983 else sum(a['usd']/(a['useful_life_years']*4) for a in B['roi']['asset_depreciation_schedule'] if a['service_quarter']<q and (y-int(a['service_quarter'][:4]))*4+int(q[-1])-int(a['service_quarter'][-1])<=a['useful_life_years']*4)
  depreciation=baseline_depreciation+extra_dep
  new_capital=extra_capex+(base['capex_usd']*infl if y==1983 else 0)
  if new_capital:new_assets.append({'quarter':q,'amount':new_capital,'useful_life_years':5,'basis':'Incremental expansion plus 1983 maintenance capital; depreciation starts next quarter'})
  inventory=(salesq['recurring_cost_usd']+addon['recurring_cost_usd']+oemcost)*2/3+credit_balance
  inventory_change=inventory-previous_inventory;ebitda=revenue-costs;ebit=ebitda-depreciation;fcf=ebitda-capex-inventory_change
  cumulative+=fcf;capcum+=capex;depcum+=depreciation;ebitcum+=ebit;revcum+=revenue;peak=max(peak,-cumulative);assets=capcum-depcum+inventory;avgassets=(assets+previous_assets)/2
  if peak and cumulative>=0 and payback is None:payback=q
  row=deepcopy(base);row.update(quarter=q,computer_units=salesq['computer_units'],net_revenue_usd=money(revenue),operating_cash_cost_usd=money(costs),ebitda_usd=money(ebitda),operating_profit_ebit_usd=money(ebit),capex_usd=money(capex),depreciation_usd=money(depreciation),inventory_balance_usd=money(inventory),inventory_cash_change_usd=money(inventory_change),free_cash_flow_usd=money(fcf),cumulative_net_cash_usd=money(cumulative),cumulative_capex_usd=money(capcum),cumulative_operating_profit_usd=money(ebitcum),cumulative_net_revenue_usd=money(revcum),end_operating_assets_usd=money(assets),average_operating_assets_usd=money(avgassets),peak_external_funding_usd=money(peak),quarterly_pretax_roi_pct=round(ebit/avgassets*100,3),cumulative_accounting_roi_pct=round(ebitcum/(capcum+inventory)*100,3),cumulative_cash_return_on_peak_funding_pct=round(cumulative/peak*100,3),period_status='Reassessed 1980–83 scenario; incremental capacity is an allowance, not a released fab plan')
  row['revenue_streams_usd']={'computer_baskets':salesq['supplier_revenue_after_channel_usd'],'additional_paid_offers':addon['supplier_revenue_after_channel_usd'],'clone_supply_software_royalties':money(oemnet),'baseline_other_receipts_net_credits':money(othernet)}
  row['reassessment_bridge']={'base_quarter':bq,'volume_ratio':factor,'retained_other_net_receipts_usd':money(othernet),'retained_other_cash_cost_usd':money(othercost),'additional_programme_expense_usd':money(expense),'oem_recurring_cost_usd':money(oemcost),'addon_recurring_cost_usd':addon['recurring_cost_usd'],'computer_recurring_cost_usd':salesq['recurring_cost_usd'],'internal_cpm_royalty_eliminated_usd':internal_royalty,'incremental_capacity_capex_usd':money(extra_capex),'component_credit_balance_usd':credit_balance,'autodesk_independent_retail_spend_excluded_usd':sum(r.get('autodesk_independent_retail_spend_usd',0) for r in rr),'legacy_bpi_attach_net_removed_usd':money(bpi_net),'legacy_bpi_attach_cost_removed_estimate_usd':money(bpi_cost)}
  # Reconcile displayed gross/fees: retained receipts are already net of historical credits.
  gross=salesq['customer_retail_spend_usd']+addon['customer_retail_spend_usd']+oemnet+othernet
  row.update(customer_gross_usd=money(gross),channel_fees_usd=money(gross-revenue),promotional_credits_usd=0,recurring_product_cost_reference_usd=money(salesq['recurring_cost_usd']+addon['recurring_cost_usd']+oemcost),other_resource_costs_usd=money(othercost+expense),marketing_expense_usd=money(base['marketing_expense_usd']*infl*(.65+.35*factor)+sum(p['amount_usd'] for p in programmes if 'campaign' in p['id'] or 'launch' in p['id'])*settings['extra_cost']))
  row['recurring_product_cost_reference_usd']=money(row['recurring_product_cost_reference_usd']-internal_royalty);row['other_resource_costs_usd']=money(othercost+expense-row['marketing_expense_usd']);row['total_marketing_and_credits_usd']=row['marketing_expense_usd'];row['source_operating_expenses_usd']=money(costs-row['marketing_expense_usd']+internal_royalty);row['replaced_generic_marketing_usd']=0;row['eliminated_internal_royalties_usd']=internal_royalty
  results.append(row);previous_inventory=inventory;previous_assets=assets
 roi_cases.append({'id':sid,'marketing_multiplier':1,'incremental_asset_schedule':new_assets,'capacity_plan':capacity_plan,'quarterly':results,'first_cash_payback_quarter':payback,'sales_uplift_from_marketing_budget':None,'sensitivity_basis':'Demand 0.8/1/1.2; programme/capacity cost 1.25/1/.9; SGS royalty 3/4/5%. Scenario bounds, not probabilities.'})
 shares=[]
 for q,detail in qdetails.items():
  y=q[:4];qindex=int(q[-1])-1;logix=next(r['computer_units'] for r in quarterlies if r['quarter']==q);clones=detail['clone_units'];platform=logix+sum(clones.values());anchor=I['market']['historical_calibration_units'].get(y,I['market']['1983_planning_units']);world=round(anchor*I['market']['quarter_weights'][qindex]*settings['market']+.2*platform)
  units={'logix':logix,**clones,'other_manufacturers':world-platform};assert min(units.values())>=0
  shares.append({'quarter':q,'total_market_units':world,'manufacturers':{k:{'units':v,'share_pct':v/world*100} for k,v in units.items()},'platform_units':platform,'platform_share_pct':platform/world*100,**detail})
 markets.append({'id':sid,'quarterly':shares})
# Persist single current forecast and ROI, retaining historical pre-1980 values.
S=deepcopy(B['sales']);S['scenarios']=scenarios;S['metadata'].update(title='Reassessed Logix sales and purpose bundles',current_forecast_horizon='1983-12-31',reassessment_inputs='generated/catalogs/sales-reassessment-inputs.json');S['policy']=I;S['financial_policy'].update(scope='Logix computer task bundles only. Additional paid offers and clone supply/royalties are separate streams in ROI. Autodesk licence receipts excluded from project revenue.',demand='1980–83 reassessment; clone cannibalisation and CAD substitution explicit.',timing='Use dated June/December catalogue assessments; June snapshots proxy whole June, COMDEX CAD shipments begin December 1982. 1983 holds December 1982 unit prices/costs; new Office Professional and Business Accounts priced contents replace legacy variants. Pending installation/backup scope is not claimed as a firm quote; support/qualification allowances remain explicit. No speculative process savings.');S['contract_scenarios']=all_contracts
S['metadata']['source_story_sha256']=hashlib.sha256((R/'generated/catalogs/logix-aion-story.json').read_bytes()).hexdigest()
S['sources']=[{'path':p,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest()} for p in ['baselines/sales-roi-baseline-1982.json','generated/catalogs/sales-reassessment-inputs.json','generated/models/pricing-results.json','generated/models/retail-catalog-1982-results.json','generated/catalogs/logix-aion-story.json']]
save('generated/models/sales-forecast.json',S)
M=deepcopy(B['roi']);M['scenarios']=roi_cases;M['metadata'].update(title='Project ROI and cash flow, 1974–1983',horizon='1974-Q1–1983-Q4',scenario='Reassessed Logix sales, clone programme and Autodesk sponsorship; pre-tax project scope');M['assumptions'].update(matching='New task-bundle recurring costs replace baseline computer costs. Old Team/network and BPI attach allowances removed before new cohorts are added. Retained other receipts scale with volumes; 65% fixed/35% variable other resources and 6% 1983 escalation are explicit assumptions.',ownership='Five-entity project resource scope retained. Independent clone computer sales, Aion Tech retail profit and Autodesk licence receipts excluded. Only scenario chipset/software receipts and SGS royalties accrue to this scope.',working_capital='Two months revised recurring product costs plus revolving component credit; no terminal recovery. Capacity expansion uses $120 per extra annualised system equivalent, 5% headroom, funding one quarter before service and five-year depreciation. Requires engineering validation.',bounds='Combined demand, programme-cost and SGS-royalty scenarios; not confidence intervals.',**{'1980_extension':'Through 1983; accepted clone launch January 1982. AutoCAD sales begin December 1982 conditional on acceptance. 1983 unit prices/costs carry December 1982; retained resources rise 6%.'});M['reassessment_inputs']=I;M['annual_central']=[]
for y in range(1974,1984):
 rr=[r for r in roi_cases[1]['quarterly'] if r['quarter'].startswith(str(y))];M['annual_central'].append({'year':y,**{k:money(sum(r[k] for r in rr)) for k in ['net_revenue_usd','operating_cash_cost_usd','total_marketing_and_credits_usd','operating_profit_ebit_usd','capex_usd','free_cash_flow_usd']},'ending_cumulative_cash_usd':rr[-1]['cumulative_net_cash_usd']})
M['monthly_revenue_links']=[r for r in M['monthly_revenue_links'] if r['month']<'1980-01'];M['assumptions']['internal_royalties']='Restore baseline eliminations before deriving retained costs, then eliminate the modeled $10 CP/M royalty per new Aurelia/Aurelia+ from project costs. Independent software publishers remain outside this elimination.'
M['assumptions']['exclusions']=['Taxes, debt/interest, equity valuations and terminal asset sales','Independent clone computer revenue, Aion Tech retail profits and Autodesk licence receipts','Unspecified board/monitor export purchase orders and unqualified process savings','1984–2000 compatibility/support liabilities and future product development outside this horizon']
M['reassessment_bridge_note']='1980–83 monthly computer/add-on lines are in generated/models/sales-forecast.json; quarterly contract and resource bridges are authoritative. Earlier marketing/industrial schedules remain baseline inputs, not updated capacity commitments.'
M['sources']=[{'path':p,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest()} for p in ['baselines/sales-roi-baseline-1982.json','generated/catalogs/sales-reassessment-inputs.json','generated/models/sales-forecast.json','generated/models/pricing-results.json','generated/models/retail-catalog-1982-results.json','generated/catalogs/logix-aion-story.json']]
save('generated/models/roi-1974-1980.json',M)
market={'metadata':{'title':'Quarterly microcomputer market share','period':'1980-Q1–1983-Q4','status':'Alternative-history unit-shipment scenario; quarterly market totals are modelled, not observed','scope':I['geography']},'methodology':I['market'],'manufacturers':[{'id':'logix','name':'Logix (including UK distribution)'}]+[{'id':p['id'],'name':p['name']+' — compatible line'} for p in I['clones']]+[{'id':'other_manufacturers','name':'Other manufacturers and legacy product lines'}],'scenarios':markets,'sources':M['sources']}
business=[]
business_names={'apple':'Apple','ibm':'IBM — substitute OS','tandy':'Tandy / Radio Shack','commodore':'Commodore business systems','nec':'NEC business systems','osborne':'Osborne','other_business':'Other business suppliers'}
for case in markets:
 out=[]
 for row in case['quarterly']:
  q=row['quarter'];y=q[:4];qi=int(q[-1])-1;settings=I['scenarios'][case['id']];platform=row['platform_units'];world=round(I['business_market']['annual_baseline_units'][y]*I['business_market']['quarter_weights'][qi]*settings['market']+.2*platform)
  assert world>=platform
  weights=deepcopy(I['business_market']['rival_weights'])
  if y<'1982':weights['ibm']=0
  elif y=='1982':weights['ibm']*=I['business_market']['ibm_1982_ramp'][qi]
  if y<'1981':weights['osborne']=0
  if q=='1981-Q1':weights['osborne']=0
  units={k:v['units'] for k,v in row['manufacturers'].items() if k!='other_manufacturers'};units.update(allocate(world-platform,weights))
  out.append({**row,'total_market_units':world,'platform_share_pct':platform/world*100,'manufacturers':{k:{'units':v,'share_pct':v/world*100} for k,v in units.items()}})
 business.append({'id':case['id'],'quarterly':out})
market['business_market']={'methodology':I['business_market'],'manufacturers':[p for p in market['manufacturers'] if p['id']!='other_manufacturers']+[{'id':k,'name':v} for k,v in business_names.items()],'scenarios':business}
save('generated/models/quarterly-market-share.json',market)
# Render existing ROI report from the same revised JSON.
site=read('generated/catalogs/site-pages.json');pages={p['id']:p for p in site['pages']};nav=''.join('<a href="'+html.escape(pages[i]['path'])+'">'+html.escape(pages[i]['title'])+'</a>' for i in site['navigation'])
template=(R/'tools/roi_template.html').read_text().replace('1974–1982','1974–1983').replace('through 1982','through 1983')
notice='<section class="panel"><h2>1980–1983 reassessment</h2><p>Includes revised task-bundle sales, five clone partners, SGS transfer costs, localisation, UK preparation, Autodesk sponsorship and explicit capacity/credit allowances. Independent partner computer sales and AutoCAD receipts are excluded from project revenue. Programme amounts and OEM economics are planning assumptions. <a href="market-share.html">Quarterly market share</a> · <a href="generated/catalogs/sales-reassessment-inputs.json">Assumptions and budgets</a></p></section>'
(R/'roi.html').write_text(template.replace('__NAV__',nav).replace('__MODEL__',json.dumps(M).replace('</','<\\/')).replace('__DISPLAY_REVISION__',notice))
print(json.dumps({'sales':scenarios[1]['annual'][-3:],'roi':M['annual_central'][-3:],'end_roi':roi_cases[1]['quarterly'][-1]['cumulative_accounting_roi_pct']},indent=2))

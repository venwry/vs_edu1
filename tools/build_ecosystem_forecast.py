"""Quarterly, auditable third-party ecosystem scenario; no changes to project ROI."""
import json, math, hashlib, html
from pathlib import Path
from collections import defaultdict
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
def save(n,x):(R/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def qtr(month):return month[:4]+'-Q'+str((int(month[5:7])-1)//3+1)
Q=[f'{y}-Q{q}' for y in range(1978,1984) for q in range(1,5) if (y,q)>=(1978,2)]
S=read('generated/models/sales-forecast.json');K=read('generated/models/quarterly-market-share.json');Contract=S['contract_scenarios'];P=read('generated/catalogs/ecosystem-forecast-policy.json')
# Delivered units, not unconstrained buyer intent, establish the installed market.

def allocate(total,weights):
 if not weights or total<=0:return {k:0 for k in weights}
 scale=sum(weights.values());raw={k:total*v/scale for k,v in weights.items()};result={k:int(v) for k,v in raw.items()}
 for k in sorted(raw,key=lambda k:(-(raw[k]-result[k]),k))[:total-sum(result.values())]:result[k]+=1
 return result

scenarios=[]
for spec in P['scenarios']:
 idx=spec['id'];rows=[];apps={};makers={};models={};base_c=base_a=external_base=external_native_base=0.;prior_logix=None;cum=defaultdict(int);prev_tui=[];previous_model_counts={};last_cpm=last_native=0
 for t,q in enumerate(Q):
  matched=next((r for r in next(z for z in S['scenarios'] if z['id']==idx)['quarterly'] if r['quarter']==q),None)
  logix=matched['products'] if matched else {'aurelia':0,'aurelia_plus':0,'artemis':0,'artemis_pro':0}
  prior_logix=logix
  new_c=logix.get('aurelia',0)+logix.get('aurelia_plus',0);new_a=logix.get('artemis',0)+logix.get('artemis_pro',0)
  base_c*=1-P['host_retirement_per_quarter'];base_a*=1-P['host_retirement_per_quarter'];external_base*=1-P['host_retirement_per_quarter'];external_native_base*=1-P['host_retirement_per_quarter']
  external=[]
  for oem in P['oem_prospects']:
   if q>='1982-Q1' and oem['name'] in ['North Star','Vector Graphic']:continue
   start=Q.index(oem['first_supported_quarter']);start+=0 if oem['name']=='Tandy' else spec['qualification_delay_quarters']
   if t<max(6,start):continue # no supported external cohort before 1979 Q4
   units=round(oem['initial_quarter_units']*spec['external_adoption_multiplier']*1.15**(t-start))
   units=min(units,4000)
   external.append(dict(manufacturer=oem['name'],model=oem['model'],units=units,status=oem['status']))
  partners=[r for r in next(z for z in Contract if z['id']==idx)['quarterly'] if r['quarter']==q]
  for partner in partners:external.append(dict(manufacturer=partner['manufacturer'],model='Qualified Aurelia/Artemis clone configurations',units=partner['computer_units'],status='Signed founding partner; January 1982 launch; scenario shipment count'))
  new_external=sum(x['units'] for x in external);new_external_native=sum(r['native_units'] for r in partners);new_external_cpm=new_external-new_external_native;external_base+=new_external_cpm;external_native_base+=new_external_native;base_c+=new_c;base_a+=new_a
  eligible_c=base_c+external_base
  # Mature CP/M catalogue discovery grows sublinearly with qualified installed base.
  maturity=min(1,.45+.035*t)*spec['developer_multiplier']
  target_c=max(last_cpm,round((12+18*math.sqrt(eligible_c/1000))*maturity))
  target_tui=max(1,round(target_c*min(.52,.12+.018*t)*spec['tui_adoption_multiplier']))
  target_tui=min(target_c,target_tui)
  # Named products are candidates, dates are qualification assumptions, not historical endorsements.
  for a in P['application_candidates']:
   if q>=a['cpm_first'] and a['id'] not in apps:apps[a['id']]=dict(a,cpm_first=q,native_first=None,tui_first=a.get('tui_first'),kind='named_candidate')
  n=0
  while sum(a['cpm_first'] is not None for a in apps.values())<target_c:
   n+=1;aid=f'cohort_{q}_{n:03}'
   apps[aid]=dict(id=aid,name='Independent '+P['long_tail_categories'][(len(apps))%len(P['long_tail_categories'])]+' title '+str(len(apps)+1),cpm_first=q,native_first=None,tui_first=None,weight=1,kind='anonymous_cohort')
  cpm=[a for a in apps.values() if a['cpm_first'] is not None and a['cpm_first']<=q]
  tui=[a for a in cpm if a['tui_first'] and a['tui_first']<=q]
  for a in [a for a in cpm if a['kind']=='anonymous_cohort' and not a['tui_first']][:max(0,target_tui-len(tui))]:a['tui_first']=q
  tui=[a for a in cpm if a['tui_first'] and a['tui_first']<=q]
  native=[]
  if q>='1980-Q2':
   for a in apps.values():
    if a['id']=='bpi':a['native_first']='1980-Q2'
    planned={'vertical':'1980-Q3','comms':'1980-Q4','science':'1981-Q1','education':'1981-Q2'}.get(a['id'])
    if planned and q>=planned:a['native_first']=planned
   native_maturity=min(1,.2+.1*(t-Q.index('1980-Q2')))*spec['developer_multiplier']
   # At least one quarter of porting delay. Legacy assembler products do not become C ports.
   port_target=round(len(prev_tui)*min(.72,.20+.045*(t-Q.index('1980-Q2')))*native_maturity)
   ported=[a for a in apps.values() if a['native_first'] is not None and a['cpm_first'] is not None]
   for aid in [a for a in prev_tui if apps[a]['kind']=='anonymous_cohort' and apps[a]['native_first'] is None][:max(0,port_target-len(ported))]:apps[aid]['native_first']=q
   native_only_target=round(7*math.sqrt((base_a+external_native_base)/1000)*native_maturity)
   existing=sum(a['cpm_first'] is None for a in apps.values())
   for n in range(max(0,native_only_target-existing)):
    aid=f'native_{q}_{n:03}';apps[aid]=dict(id=aid,name='Independent native '+P['native_categories'][(existing+n)%len(P['native_categories'])]+' title '+str(existing+n+1),cpm_first=None,tui_first=None,native_first=q,weight=1.3,kind='anonymous_cohort')
   native=[a for a in apps.values() if a['native_first'] is not None and a['native_first']<=q]
  # BPI suite counts as one product family/customer licence, not five modules plus bundle.
  bpi_c=round(new_c*.2);bpi_a=round(new_a*.2)
  c_budget=round((P['cpm_copies_per_new_host']*(new_c+new_external_cpm)+P['cpm_copies_per_existing_host_quarter']*max(0,eligible_c-new_c-new_external_cpm))*spec['purchase_multiplier'])
  a_budget=round((P['native_copies_per_new_host']*(new_a+new_external_native)+P['native_copies_per_existing_host_quarter']*max(0,base_a+external_native_base-new_a-new_external_native))*spec['purchase_multiplier']*min(1,.35+.09*max(0,t-Q.index('1980-Q2')))) if native else 0
  c_sales=allocate(c_budget,{a['id']:a['weight']*(1.4 if a in tui else 1) for a in cpm if a['id']!='bpi'});c_sales['bpi']=bpi_c
  a_sales=allocate(a_budget,{a['id']:a['weight'] for a in native if a['id']!='bpi'}) if len(native)>1 else {};a_sales['bpi']=bpi_a if native else 0
  # Every platform licence sold is counted once, even where one family has two editions.
  cp_copies=sum(c_sales.values());na_copies=sum(a_sales.values());tui_copies=sum(c_sales.get(a['id'],0) for a in tui)
  hwbase=base_c+base_a+(external_base+external_native_base)*P['external_flexibus_attach']
  ready=min(1,.35+.04*t)*spec['developer_multiplier']
  supplier_target=max(len(makers),round((1+.75*math.sqrt(hwbase/1000)+.3*t)*ready))
  for n in range(len(makers),supplier_target):
   mid=f'supplier_{n+1:03}';kind=['printer','storage','serial_modem','internal_card','monitor','instrument'][n%6]
   gate={'printer':'1978-Q3','storage':'1978-Q4','serial_modem':'1979-Q3','internal_card':'1979-Q1','monitor':'1979-Q4','instrument':'1980-Q1'}[kind]
   if q<gate:break
   makers[mid]=dict(id=mid,name='Independent '+kind.replace('_',' ')+' specialist '+str(n+1),category=kind,first_quarter=q)
  for mid,maker in makers.items():
   age=t-Q.index(maker['first_quarter']);count=1+age//4
   for n in range(count):
    model_id=mid+f'_m{n+1}'
    if model_id not in models:models[model_id]=dict(id=model_id,manufacturer_id=mid,category=maker['category'],first_quarter=q,name=maker['name']+' / qualified model '+str(n+1),platform='host-specific adapter/driver required' if maker['category'] in ['internal_card','monitor'] else 'qualified FlexiBUS class profile')
  hw_new=new_c+new_a+new_external*P['external_flexibus_attach']
  hw_budget=round((hw_new*P['devices_per_new_host']+max(0,hwbase-hw_new)*P['devices_per_existing_host_quarter'])*spec['purchase_multiplier']*min(1,.5+.03*t)) if models else 0
  hw_sales=allocate(hw_budget,{mid:P['hardware_category_weights'][v['category']] for mid,v in models.items()})
  for mid,units in hw_sales.items():models[mid].setdefault('quarterly_units',{})[q]=units
  for a in apps.values():
   a.setdefault('cpm_quarterly_copies',{})[q]=c_sales.get(a['id'],0);a.setdefault('native_quarterly_copies',{})[q]=a_sales.get(a['id'],0)
  for key,value in [('cpm',cp_copies),('native',na_copies),('devices',hw_budget),('external_computers',new_external)]:cum[key]+=value
  ports=sum(a['cpm_first'] is not None for a in native)
  rows.append(dict(quarter=q,host_basis='Matched reassessed Logix scenario; contracted clone cohorts replace North Star/Vector prospect rows from 1982',logix_new_units=logix,logix_active_cpm=round(base_c),logix_active_aionix=round(base_a),external_active_cpm_tui=round(external_base),external_active_aionix=round(external_native_base),external_supported_manufacturers=len(external),external_computer_models=len(external)+len(partners),external_computers_sold=new_external,external_computers_cumulative=cum['external_computers'],external_oems=external,cpm_applications=len(cpm),tui_applications=len(tui),aionix_applications=len(native),cross_platform_families=ports,distinct_application_families=len(cpm)+len(native)-ports,cpm_copies_sold=cp_copies,tui_copies_sold=tui_copies,aionix_copies_sold=na_copies,cpm_cumulative_copies=cum['cpm'],aionix_cumulative_copies=cum['native'],device_manufacturers=len(makers),device_models=len(models),devices_sold=hw_budget,devices_cumulative=cum['devices'],all_hardware_manufacturers=len(makers)+len(external),all_hardware_models=len(models)+len(external)+len(partners),all_hardware_units=hw_budget+new_external))
  prev_tui=[a['id'] for a in tui];last_cpm=len(cpm);last_native=len(native)
 scenarios.append(dict(id=idx,title=spec['title'],quarterly=rows,applications=list(apps.values()),device_manufacturers=list(makers.values()),device_models=list(models.values())))
M=dict(metadata=dict(title='Third-party ecosystem',horizon='1978-Q2–1983-Q4',baseline_commit='1d6bfb9c2633d56d32b479723acd03ee0e100925',status='Alternative-history forecast, not observed third-party shipments',currency='Unit counts, not revenue',financial_treatment='Independent third-party retail receipts remain excluded. Scenario clone chipset/software and SGS royalties are separately included in revised project ROI.'),policy=P,scenarios=scenarios,sources=[dict(path=n,sha256=hashlib.sha256((R/n).read_bytes()).hexdigest()) for n in ['generated/catalogs/ecosystem-forecast-policy.json','generated/models/sales-forecast.json','generated/models/quarterly-market-share.json','generated/catalogs/logix-aion-technical-catalog-v2.json']])
save('generated/models/ecosystem-forecast.json',M)
site=read('generated/catalogs/site-pages.json');pages={p['id']:p for p in site['pages']};nav=''.join('<a href="'+html.escape(pages[x]['path'])+'"'+(' aria-current="page"' if x=='ecosystem' else '')+'>'+html.escape(pages[x]['title'])+'</a>' for x in site['navigation'])
(R/'ecosystem.html').write_text((R/'tools/ecosystem_template.html').read_text().replace('__NAV__',nav).replace('__MODEL__',json.dumps(M,ensure_ascii=False).replace('</','<\\/')))
print(json.dumps({s['id']:s['quarterly'][-1] for s in scenarios},indent=2))


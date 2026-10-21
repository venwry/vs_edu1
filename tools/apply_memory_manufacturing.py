"""Apply the accepted RAM-focused manufacturing roadmap idempotently."""
import json, copy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(n): return json.loads((R/n).read_text())
def save(n,v): (R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')

policy={
 'status':'Accepted alternative-history planning scenario; all production releases require engineering qualification.',
 'era_policy':'ERA1 and its 6/8 MHz variants remain 55 mm2 on the original 3.0 um Micralign process. No CPU shrink or speed-bin uplift.',
 'financial_horizon':'Recurring prices/costs through June 1981; industrial cash and ROI through 1981 Q4. Later recipe economics and budgets are prospective; no invented 1982–83 company sales.',
 'wafer_cost_by_year':{'1978':{'3.0':210},'1979':{'3.0':220},'1980':{'3.0':235},'1981':{'3.0':255,'2.75':285},'1982':{'3.0':276,'2.75':308,'2.0':340},'1983':{'3.0':298,'2.75':333,'2.0':360,'1.5':400}},
 'memory_recipes':[
  {'id':'dram64_3um_launch','node_um':'3.0','available_from':'1979-12-03','die_area_mm2':45,'defect_density_cm2':2.4,'nonarea_yield':.85*.85,'processed_wafer_usd':220,'repair_fraction_of_spatial_failures':0},
  {'id':'dram64_3um_control','node_um':'3.0','available_from':'1980-06-01','die_area_mm2':45,'defect_density_cm2':2.0,'nonarea_yield':.85*.90,'processed_wafer_usd':235,'repair_fraction_of_spatial_failures':0},
  {'id':'dram64_3um_repair','node_um':'3.0','available_from':'1981-01-01','die_area_mm2':47.25,'defect_density_cm2':1.7,'nonarea_yield':.85*.90,'processed_wafer_usd':255,'repair_fraction_of_spatial_failures':.35,'repair_cost_per_wafer_usd':12},
  {'id':'dram64_275um_repair','node_um':'2.75','available_from':'1981-06-01','die_area_mm2':40,'defect_density_cm2':2.6,'nonarea_yield':.88*.85,'processed_wafer_usd':285,'repair_fraction_of_spatial_failures':.35,'repair_cost_per_wafer_usd':12},
  {'id':'dram64_2um_repair','node_um':'2.0','available_from':'1982-07-01','die_area_mm2':28,'defect_density_cm2':2.6,'nonarea_yield':.85*.90,'processed_wafer_usd':340,'repair_fraction_of_spatial_failures':.35,'repair_cost_per_wafer_usd':12},
  {'id':'dram64_15um_repair','node_um':'1.5','available_from':'1983-10-01','die_area_mm2':19,'defect_density_cm2':2.5,'nonarea_yield':.85*.85,'processed_wafer_usd':400,'repair_fraction_of_spatial_failures':.35,'repair_cost_per_wafer_usd':15}],
 'selection_policy':'Minimum recurring cost among date-qualified 64K x 1 recipes, same 75 mm wafer and electrical contract. 2.75 um is evaluated against repaired 3 um; smaller node alone does not select production.',
 'repair_model':'Y=Y0*(exp(-D*A/100)+r*(1-exp(-D*A/100))). r=.35 is the assumed recoverable share of spatial die failures, not all failing dies. Never repair Y0 losses. Spare structures add 5% area to 3 um. Repair operations/testing add recurring wafer cost. No historical multiplier is imported.',
 'qualification':['Released capacity/pinout/rails and refresh contract','Retention over temperature and voltage, read/write and disturb tests','Defect-map coverage and fuse programming with full post-repair retest','Speed bins and all-bank board power/timing qualification','At least two matched steppers and recipe-specific one-down capacity before volume stepper manufacture'],
 'capital_schedule':[
  {'quarter':'1979-Q1','usd':180000,'purpose':'Stepper programme facilities and procurement; commissioned 1979-Q4'},
  {'quarter':'1979-Q2','usd':450000,'purpose':'First GCA stepper and bay installation; commissioned 1979-Q4'},
  {'quarter':'1979-Q3','usd':420000,'purpose':'Reticle, metrology and process integration equipment; commissioned 1979-Q4'},
  {'quarter':'1980-Q1','usd':325000,'purpose':'Matched second stepper procurement; commissioned 1980-Q2'},
  {'quarter':'1980-Q2','usd':300000,'purpose':'Second stepper acceptance, matching and support; commissioned 1980-Q2'},
  {'quarter':'1980-Q3','usd':125000,'purpose':'Memory laser repair/test equipment; commissioned 1981-Q1'},
  {'quarter':'1980-Q4','usd':125000,'purpose':'Memory repair installation and acceptance; commissioned 1981-Q1'},
  {'quarter':'1981-Q3','usd':150000,'purpose':'2 um etch/metrology upgrade; commissioned 1982-Q2'},
  {'quarter':'1981-Q4','usd':150000,'purpose':'2 um process equipment; commissioned 1982-Q2'},
  {'quarter':'1982-Q1','usd':150000,'purpose':'2 um equipment installation; commissioned 1982-Q2'},
  {'quarter':'1982-Q2','usd':150000,'purpose':'2 um process acceptance; commissioned 1982-Q2'},
  {'quarter':'1982-Q3','usd':200000,'purpose':'1.5 um equipment and metrology upgrade; commissioned 1983-Q3'},
  {'quarter':'1982-Q4','usd':200000,'purpose':'1.5 um equipment procurement; commissioned 1983-Q3'},
  {'quarter':'1983-Q1','usd':200000,'purpose':'1.5 um optics/alignment/process upgrade; commissioned 1983-Q3'},
  {'quarter':'1983-Q2','usd':200000,'purpose':'1.5 um installation; commissioned 1983-Q3'},
  {'quarter':'1983-Q3','usd':200000,'purpose':'1.5 um qualification equipment; commissioned 1983-Q3'},
  {'quarter':'1983-Q4','usd':200000,'purpose':'1.5 um selected release and matching; commissioned 1983-Q4'}],
 'capital_basis':'Nominal USD engineering allowances, not quotations. Full added programme excludes demand-driven legacy fab capacity, which is recomputed independently. Future capital after 1981 is disclosed separately from closed-horizon ROI.',
 'pilot_operations':{'from_quarter':'1979-Q4','through_quarter':'1981-Q4','wafers_per_month':20,'processed_wafer_usd':300,'nonpayroll_operations_usd_per_quarter':18000,'basis':'Dedicated development line. 60 pilot wafers/quarter plus utilities, service and consumables; programme engineering payroll separate. No pilot saleable output credited.'},
 'engineering_programs':[
  {'id':'stepper_process_development','entity':'AION Labs','start':'1979-Q1','end':'1981-Q4','person_months':180,'product_refs':['technology.nmos_275um'],'scope':'Incremental stepper process, reticles, metrology, matching and RAM shrink trials; excludes existing 120 PM original 64K programme.'},
  {'id':'dram_redundancy','entity':'AION Labs','start':'1980-Q1','end':'1980-Q4','person_months':60,'product_refs':['part.aion_4164'],'scope':'Spare rows/columns, fuses, defect maps, repair/retest, retention and reliability; repaired production target January 1981.'},
  {'id':'pro_aion_memory_qualification','entity':'Logix','start':'1980-Q3','end':'1981-Q2','person_months':24,'product_refs':['computer.artemis_pro'],'scope':'AION memory modules, full-bank timing/power/refresh and server qualification.'}],
 'future_engineering':[{'period':'1982','person_months':120,'loaded_payroll_and_validation_usd':600000},{'period':'1983','person_months':144,'loaded_payroll_and_validation_usd':780000}],
 'future_engineering_basis':'Additional forward annual planning allowance; includes prototype/mask/validation work, excludes capital above and later volume operating cost. Not included in 1974–81 ROI.',
 'sources':[{'url':'https://www.lithoguru.com/scientist/litho_history/Optical_lithography_40_years_and_holding_Bruning_2007.pdf','use':'GCA stepper history/field, not AION yield or budget.'},{'url':'https://ieeexplore.ieee.org/document/1051630/','use':'1981 laser-programmable DRAM redundancy precedent; no published yield factor reused.'}]}

# Preserve the previously discussed quarterly generic-logic envelope separately from RAM economics.
rows=[('1979-Q4',2.75,6,.65),('1980-Q1',2.75,5,.75),('1980-Q2',2.75,4,.8),('1980-Q3',2.75,3.5,.83),('1980-Q4',2.75,3,.85),('1981-Q1',2.75,2.8,.85),('1981-Q2',2.75,2.6,.88),('1981-Q3',2,4.5,.7),('1981-Q4',2,4,.75),('1982-Q1',2,3.5,.8),('1982-Q2',2,3,.83),('1982-Q3',2,2.6,.85),('1982-Q4',2,2.3,.88),('1983-Q1',1.5,4,.7),('1983-Q2',1.5,3.5,.78),('1983-Q3',1.5,3,.83),('1983-Q4',1.5,2.5,.85)]
import math
policy['quarterly_process_envelope']=[{'quarter':q,'node_um':f,'defect_density_cm2':d,'nonarea_yield':y,'yield_budgets':[{'target_yield':t,'die_area_mm2':round(min(90,100/d*math.log(y/t)),2),'logic_transistors':round(min(90,100/d*math.log(y/t))*700*(3/f)**2)} for t in [.1,.25,.5]]} for q,f,d,y in rows]
policy['envelope_limits']='Newest generic logic process, 90 mm2 planning field cap, N=A*700*(3/F)^2. Not a memory density model; older qualified recipes remain available. No ERA migration.'
save('memory_manufacturing.json',policy)

c=load('logix_aion_technical_catalog_v2.json'); by={x['id']:x for a in c.values() if isinstance(a,list) for x in a if isinstance(x,dict) and 'id' in x}
for node,name,when in [('3um','3.0','1978-06-05'),('275um','2.75','1980-06'),('2um','2.0','1982-07'),('15um','1.5','1983-10')]:
 id='technology.nmos_'+node
 tech={'id':id,'name':name+' µm NMOS manufacturing process','category':'semiconductor_manufacturing','owner':'AION Labs','introduced':{'event_name':'Scenario process qualification target','event_start_date':when},'specification':{'node_um':float(name),'wafer_diameter_mm':75,'lithography':'Micralign projection' if node=='3um' else 'GCA reduction stepper; tool/optics upgrades qualified per node','status':'Accepted scenario roadmap; qualification gates in memory_manufacturing.json','recipe_separation':'Logic, SRAM, DRAM capacitor/sense circuits and analog require separate qualification. One metal baseline; additional polysilicon is recipe-specific.','policy_file':'memory_manufacturing.json'},'used_by':['part.era1','part.aion_4164'] if node=='3um' else ['part.aion_4164']}
 c['technologies']=[x for x in c['technologies'] if x['id']!=id]+[tech]
era=by['part.era1'];era['manufacturing_process_ref']='technology.nmos_3um';era['manufacturing_planning']={'node_um':3.0,'die_area_mm2':55,'policy':'Both 6 and 8 MHz remain on original Micralign process; speed-bin and electrical qualification unchanged.'}
dram=by['part.aion_4164'];dram['used_in']=sorted(set(dram['used_in']+['part.artemis_ram_module_128kb','computer.artemis_pro']))
dram['specification']['manufacturing_planning'].update(policy_file='memory_manufacturing.json',revision_policy='1980 process-control improvement; 1981 repaired 3 um die includes 5% spare area. Evaluate 2.75 um against repaired 3 um; apply only if cheaper. Later 2/1.5 um releases are prospective.',cost_1980_usd=None,cost_1981_usd=None)
dram['specification']['electrical_contract']='64K x 1; released pinout/rails/timing/refresh remain gates. Common module interface only after retention, speed and all-bank qualification; no capacity or bus-width change.'
mod=by['part.artemis_ram_module_128kb'];mod['specification']['chip_type_ref']='part.aion_4164';mod['name']='Artemis M128-16 128 KiB / 16-bit AION-qualified RAM module'
mod['manufacturing_requirements']=['Sixteen AION 64K x 1 chips per module; PRO and bank kits use matched qualified grades. Keep purchased 64K supplier as a separately qualified contingency, with no automatic substitution or price saving.']
pro=by['computer.artemis_pro'];pro['memory']['sourcing_policy']='AION 64K x 1 production grade after server qualification; 64/128 chips for 512 KiB/1 MiB. Existing 32-bit bank widths, capacities and populations unchanged.'
by['part.dram_64kbit']['used_in']=[]
for x in [mod,pro]:
 x.setdefault('technology_refs',[])
 if 'technology.nmos_3um' not in x['technology_refs']:x['technology_refs'].append('technology.nmos_3um')
from memory_manufacturing import selected, evaluate
mp=dram['specification']['manufacturing_planning']
mp['legacy_fields_scope']='Top-level die area and maturity describe the original launch revision only; production_revisions are authoritative for dated 1980/81 economics.'
mp['status']='Accepted RAM process/repair scenario, not proven yield. Spare structures, retention, repair coverage and speed require qualification; recipe details in memory_manufacturing.json.'
mp['production_revisions']={str(y):dict(selected(y),**evaluate(selected(y),policy['wafer_cost_by_year'][str(y)][selected(y)['node_um']])) for y in [1980,1981]}
mp['cost_1980_usd']=round(mp['production_revisions']['1980']['good_packaged_chip_cost_usd'],4)
mp['cost_1981_usd']=round(mp['production_revisions']['1981']['good_packaged_chip_cost_usd'],4)
save('logix_aion_technical_catalog_v2.json',c)
b=load('hardware_bom.json')
for a in b['assemblies']:
 if a['id']=='assembly.part.artemis_ram_module_128kb':
  for l in a['lines']:
   if l['ref']=='bompart.part.dram_64kbit':l['ref']='bompart.part.aion_4164';l['role']='AION 64K x 1 data DRAM; PRO-qualified grade'
save('hardware_bom.json',b)

s=load('logix_aion_story.json');site=load('site_pages.json')
if not any(x['id']=='phase.manufacturing_1981_1983' for x in s['phases']):
 s['phases'].append({'id':'phase.manufacturing_1981_1983','title':'Memory manufacturing and process scaling','kind':'between_conferences','period':{'start':'1981-11-19','end':'1983-12-31','precision':'range','qualifier':'Scenario roadmap beyond existing commercial forecast','display':'1981-11-19 to 1983-12-31'},'events':[]})
lane={'id':'manufacturing','title':'AION manufacturing','description':'Process development, RAM yield and release gates','actor_refs':['actor.labs','actor.logix'],'event_refs':[],'process_refs':[]}
for id,title,start,end,refs in [
 ('stepper_install','Stepper line procurement and installation','1979-01-01','1979-09-30',['technology.nmos_275um']),
 ('process_275','2.75 µm development and memory qualification','1979-07-01','1981-06-30',['technology.nmos_275um','part.aion_4164']),
 ('dram_repair','DRAM yield control and repair development','1980-01-01','1980-12-31',['part.aion_4164']),
 ('process_2','2.0 µm process and RAM shrink development','1981-01-01','1982-12-31',['technology.nmos_2um','part.aion_4164']),
 ('process_15','1.5 µm process and RAM shrink development','1982-04-01','1983-12-31',['technology.nmos_15um','part.aion_4164'])]:
 pid='process.'+id; phases=[p['id'] for p in s['phases'] if p['period']['start']<=end and p['period']['end']>=start]
 proc={'id':pid,'title':title,'participants':[{'actor_ref':'actor.labs','role':'process_developer'}],'actions':[{'actor_refs':['actor.labs'],'description':'Develop and qualify the dated manufacturing scenario; ERA1 remains on 3 µm. Budgets, yields and release gates are in memory_manufacturing.json.'}],'outcomes':[],'agreement_terms':[],'metrics':[],'product_refs':refs,'related_event_refs':[],'period':{'start':start,'end':end,'precision':'range','qualifier':'Selected scenario schedule, conditional on qualification','display':start+' to '+end},'phase_refs':phases,'date_basis':'provisional'}
 s['processes']=[x for x in s['processes'] if x['id']!=pid]+[proc];lane['process_refs'].append(pid)
milestones=[('stepper_order','Stepper programme approved and equipment ordered','1979-01','technology.nmos_275um'),('stepper_accept','Stepper installation and lithography acceptance','1979-09','technology.nmos_275um'),('pilot_275','First complete 2.75 µm pilot lots','1979-12','technology.nmos_275um'),('production_275','Selected 2.75 µm process release review','1980-06','technology.nmos_275um'),('dram_control_release','Improved 3 µm DRAM process-control release','1980-06','part.aion_4164'),('dram_repair_release','Repairable 64K DRAM production target','1981-01','part.aion_4164'),('dram_275_review','2.75 µm RAM qualification and cost-selection review','1981-06','part.aion_4164'),('pilot_2','First complete 2.0 µm pilot lots','1981-09','technology.nmos_2um'),('production_2','Selected 2.0 µm process release review','1982-06','technology.nmos_2um'),('dram_2_release','2.0 µm 64K RAM selected release target','1982-07','part.aion_4164'),('mature_2','2.0 µm repeatable-production review','1982-12','technology.nmos_2um'),('pilot_15','First complete 1.5 µm pilot lots','1983-03','technology.nmos_15um'),('production_15','Selected 1.5 µm process release review','1983-09','technology.nmos_15um'),('dram_15_release','1.5 µm 64K RAM selected release target','1983-10','part.aion_4164'),('mature_15','1.5 µm repeatable-production review','1983-12','technology.nmos_15um')]
for id,title,date,ref in milestones:
 eid='event.'+id
 for phase in s['phases']:phase['events']=[x for x in phase['events'] if x['id']!=eid]
 phase=next(p for p in s['phases'] if p['period']['start'][:7]<=date<=p['period']['end'][:7])
 phase['events'].append({'id':eid,'title':title,'event_type':'development','date':{'start':date,'end':date},'participants':[{'actor_ref':'actor.labs','role':'manufacturer'}],'actions':[{'actor_refs':['actor.labs'],'description':'Selected alternative-history milestone; qualify measured process, retention/speed, tool matching and cost before release. Existing processors retain their current process. See memory_manufacturing.json.'}],'outcomes':[],'agreement_terms':[],'metrics':[],'product_refs':[ref],'related_event_refs':[]});lane['event_refs'].append(eid)
for phase in s['phases']:phase['events'].sort(key=lambda x:x['date']['start'])
s['assumptions']['conventions']['phase_order']='Nine consecutive phases from 1972-01-01 through 1983-12-31; later manufacturing roadmap is provisional and does not establish later product sales.'
site['timeline_view']['lanes']=[x for x in site['timeline_view']['lanes'] if x['id']!='manufacturing']+[lane]
site['pages']=[p for p in site['pages'] if p['id']!='memory-manufacturing']+[{'id':'memory-manufacturing','path':'memory-manufacturing.html','title':'RAM manufacturing','description':'Qualified RAM process selection, balanced prices and investment impact.','kind':'report','record_refs':[],'aliases':['Memory manufacturing']}]
if 'memory-manufacturing' not in site['navigation']:site['navigation'].append('memory-manufacturing')
next(p for p in site['pages'] if p['id']=='roi')['description']='Quarterly revenue, investments, marketing, operating profit, ROI and cash recovery through 1981.'
save('logix_aion_story.json',s);save('site_pages.json',site)
print('Applied RAM process roadmap, retained 3 um ERA1, updated AION PRO modules and manufacturing timeline.')

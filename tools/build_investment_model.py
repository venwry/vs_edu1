from data_store import read_document, document_bytes, document_text
import json, math, hashlib, calendar
from pathlib import Path
from collections import defaultdict
from memory_manufacturing import policy as memory_policy
from market_outlook import POLICY, reassess, team_units, team_quarter_budget
ROOT=Path(__file__).resolve().parent.parent
S=ROOT; OUT=ROOT
def load(n):return read_document(n+'.json',root=S)
sales=load('sales_forecast'); costs=load('manufacturing_costs'); cat=load('logix_aion_technical_catalog_v2'); price=load('pricing_results')
cp={x['id']:x for x in costs['products']}; pp={x['id']:x for x in price['products']}; chips=costs['chip_fabrication_models']
entities=['Logix','AION Labs','AION Software','DRI','BPI']
quarters=[f'{y}-Q{q}' for y in range(1974,1983) for q in range(1,5)]
def qi(q):return quarters.index(q)
def quarter(m):return m[:4]+'-Q'+str((int(m[5:7])-1)//3+1)
def rnd(x):return round(x,2)
def expand(ref):
 if ref in cp:return [(ref,1)]
 if ref in pp:
  a=[]
  for x in pp[ref]['components']:
   a += [(r,n*x['quantity']) for r,n in expand(x['cost_ref'])]
  return a
 raise ValueError(ref)
def snapshot(ref,y):
 p=cp[ref]; yy=str(y)
 if yy not in p['snapshots'] or p['snapshots'][yy].get('total_usd') is None:
  yy=next(k for k,v in p['snapshots'].items() if v.get('total_usd') is not None)
 return p['snapshots'][yy],int(yy)
inputs=load('sales_model_inputs');baskets=inputs['basket_components']
# Conditional server production added only after an explicitly assumed qualification date.
revision=load('artemis_display_revision'); pro_mix=revision['mono_pro_pro_console_share']
baskets['artemis_pro']=[{'product_ref':'bundle.artemis_pro_512_server','quantity':.75*(1-pro_mix)},{'product_ref':'bundle.artemis_pro_1mb_server','quantity':.25*(1-pro_mix)},{'product_ref':'bundle.artemis_pro_512_mono_pro','quantity':.75*pro_mix},{'product_ref':'bundle.artemis_pro_1mb_mono_pro','quantity':.25*pro_mix}]
programs=[]
def prog(id,owner,start,end,pm,refs,scope):
 programs.append(dict(id=id,entity=owner,start=start,end=end,person_months=pm,low_person_months=round(pm*.7),high_person_months=round(pm*1.7),product_refs=refs,scope=scope,productive_hours_per_person_month=130,effort_basis='Bottom-up work-package judgement; includes integration, verification, documentation and release work; future tools reduce layout effort, not qualification.'))
prog('z80_platform','DRI','1974-Q4','1978-Q2',145,['software.cpm_aurelia'],'CP/M core evolution, BIOS, banking/XIP, TUI contracts, storage integrity, OEM validation')
prog('aurelia_architecture','Logix','1975-Q1','1978-Q2',240,['computer.aurelia','technology.flexibus'],'Architecture 45 PM; board schematics/layout 65; firmware 50; EMC/power/timing/test fixtures and two respins 80')
prog('launch_silicon','AION Labs','1975-Q1','1978-Q1',360,['part.aion_4116','part.aurelia_video_chip','part.flexibus_host_controller','part.flexibus_device_controller'],'4116 DRAM sensing/refresh and buffered-controller timing, digital video and FlexiBUS silicon; process integration and qualification; masks provided by secret facility, consumables still budgeted')
# Incremental engineering for the accepted sprite/system-controller extension; not included in baseline programmes.
prog('sprite_sram_extension','AION Labs','1976-Q1','1978-Q1',48,['part.aion_2114','part.aurelia_video_chip'],'SRAM cell/process and separate-bus video revision, layout, probe/test and sprite timing qualification')
prog('aurelia_system_controller','AION Labs','1976-Q1','1978-Q1',60,['part.aurelia_system_controller'],'DMA, bank mapper, independent refresh, bus arbitration, two-clock qualification, layout and respin allowance')
prog('aurelia_extension_board','Logix','1977-Q1','1978-Q2',24,['computer.aurelia'],'Controller/SRAM PCB routing, power/pinout, fixtures and simultaneous-load qualification; plus derivative covered by plus_hardware')
prog('aurelia_dma_bios','DRI','1977-Q1','1978-Q2',18,['software.cpm_aurelia'],'Physical-bank DMA drivers, refresh/reset/abort contract and device-ready integration')
prog('sprite_dma_sdk','AION Software','1977-Q2','1978-Q2',12,['software.aurelia_sdk'],'Sprite descriptors, upload API, DMA examples, compatibility and documentation')
prog('tools_tui_office','AION Software','1975-Q2','1978-Q2',300,['software.business_tools_aurelia','software.simple_c_z80','software.aurelia_sdk'],'Editor, assembler/linker/compiler, libraries, common UI, office tools, installer/manuals, regression suite')
prog('abacus1','AION Software','1976-Q1','1978-Q2',180,['software.abacus_1'],'Sparse spreadsheet, formula parser/evaluator, recalculation graph, persistence, printing, memory budgeting')
prog('bpi_initial','BPI','1977-Q1','1978-Q2',144,['software.bpi_suite'],'Five modules, reconciliation, journals, audit trails, accounting expert review, jurisdiction-limited payroll, pilot businesses')
prog('bpi_port_help','AION Software','1977-Q2','1978-Q2',45,['software.bpi_suite'],'C/TUI port assistance; BPI retains application ownership')
prog('plus_hardware','Logix','1978-Q2','1979-Q4',108,['computer.aurelia_plus'],'RAM mapping, AION 64K system DRAM board/power/refresh qualification, PCB derivatives and firmware; production ramp by December 1979 within the existing 108 PM')
prog('abacus2_pulse','AION Software','1978-Q2','1979-Q4',240,['software.abacus_2','software.pulse_1'],'Spreadsheet evolution and interactive language/runtime; syntax, evaluation, debugger, persistence and user testing')
prog('era_silicon','AION Labs','1977-Q1','1980-Q1',480,['part.era1','part.artemis_mmu','part.artemis_dma','part.artemis_graphics_chip','part.artemis_fdd_hdd_controller'],'ISA/ABI and simulator 80 PM; CPU architecture/logic 100; physical/layout 65; MMU/DMA/storage/graphics 105; verification/bring-up/respins 130')
prog('artemis_video_card_increment','AION Labs','1978-Q2','1980-Q1',revision['engineering_person_months']['AION Labs video increment'],['part.artemis_graphics_chip'],'Increment beyond original graphics work: enlarged SRAM pipeline, DRAM arbitration, sprite bus, parallel renderer, masks and respin verification')
prog('mono_pro_receiver','AION Labs','1978-Q3','1980-Q1',revision['engineering_person_months']['AION Labs monitor receiver'],['part.mono_pro_controller'],'Palette/receiver ASIC, DAC switching, verification and silicon qualification; analog circuitry remains external')
prog('mono_pro_card_board','Logix','1978-Q3','1980-Q2',revision['engineering_person_months']['Logix card and monitor qualification'],['device.artemis_video_card','device.mono_pro'],'Dedicated slot/card PCB and tube/yoke/analog monitor qualification, calibration fixtures, safety and EMC; incremental to baseline hardware')
prog('artemis_display_drivers','AION Software','1979-Q1','1980-Q2',revision['engineering_person_months']['AION Software display drivers'],['software.aionix','software.artemis_sdk'],'Mode discovery, 400-line fonts, page flips, sprites, monitor compatibility and driver regression')
prog('aion_64k_dram','AION Labs','1977-Q3','1979-Q3',120,['part.aion_4164'],'64K cell/array, sense amps, refresh/retention, bias/power, process integration, masks, probe, speed bins and respin; finish silicon qualification by Q3 1979 for Q4 Aurelia+ ramp, reuse in Artemis. Existing 120 PM moved earlier, not duplicated.')
prog('artemis_tier_hardware','Logix','1979-Q1','1980-Q2',24,['device.artemis_video_card_16kb','part.artemis_ram_module_128kb_aion'],'Economy card host bridge and AION high-density modules: PCB, power, firmware and combined-load qualification')
prog('artemis_economy_driver','AION Software','1979-Q2','1980-Q2',12,['software.aionix','software.artemis_sdk'],'Detect fitted card, reject incompatible monitors/modes, serialize host writes and regression-test both video tiers')
prog('artemis_hardware','Logix','1978-Q1','1980-Q2',300,['computer.artemis','device.artemis_cpm80_module'],'32-bit bus timing, paired RAM, PCB signal/power integrity, firmware, compatibility card, fixtures and system stress testing')
prog('aionix_core','AION Software','1978-Q1','1980-Q2',330,['software.aionix','software.aion_c_ide','software.artemis_sdk'],'OS, scheduler, protection, filesystem, drivers, ERA compiler backend/ABI, native tools and performance validation')
prog('aionix_dri','DRI','1978-Q1','1980-Q2',150,['software.aionix'],'DRI kernel/filesystem/driver expertise; AION reimburses assigned cost; same people not counted in AION headcount')
prog('oem_compatibility','AION Software','1978-Q4','1980-Q2',100,['software.aurelia_compatibility_kit','software.abacus_1'],'Tandy port, compatibility contract, adapters and certification tests')
prog('dri_oem','DRI','1978-Q3','1980-Q2',75,['software.cpm_model_ii'],'CP/M OEM ports and maintenance protected from AIONix diversion')
prog('bpi_era','BPI','1979-Q2','1980-Q2',80,['software.bpi_suite'],'ERA native port, precision/file format and database consistency tests')
prog('native_apps_v3','AION Software','1979-Q3','1980-Q4',230,['software.abacus_3','software.pulse_3','software.business_tools_artemis'],'Native applications and expanded functionality, measured resource budgets and compatibility tests')
prog('network_server','AION Software','1979-Q2','1981-Q2',420,['software.aionix_server'],'TCP/IP implementation, network drivers, server protocol, authentication, locking and recovery; no assumption of modern network stack availability')
prog('cpm_network','DRI','1979-Q4','1981-Q2',100,['software.cpm_aurelia_networking'],'CP/M network clients, bounded memory buffers and regression testing')
prog('bpi_rdbms','BPI','1979-Q1','1981-Q2',540,['software.bpi_client_server'],'RDBMS 220 PM; concurrent application/server migration 160; crash recovery, locking, reporting and pilot validation 160')
prog('pro_network_hardware','Logix','1979-Q3','1981-Q2',210,['computer.artemis_pro','device.network_card_artemis'],'Server boards, network adapter, storage/power/thermal design, burn-in and multi-client qualification')
prog('silicon_sustain','AION Labs','1980-Q2','1981-Q4',120,list(chips),'Process retargeting, test coverage, failure analysis and controlled revisions')
for work in memory_policy()['engineering_programs']:
 prog(work['id'],work['entity'],work['start'],work['end'],work['person_months'],work['product_refs'],work['scope'])
# Recurring software support/compatibility sustaining engineering, separate from initial development.
for e,pm in [('AION Software',210),('DRI',96),('BPI',90),('Logix',96)]:prog('sustain_'+e,e,'1978-Q3','1981-Q4',pm,[],'Maintenance, documentation, release engineering and compatibility stewardship through 1981 only; 1982 extension covered by retained payroll; further obligations excluded')
source_refs=[dict(path=str(p.relative_to(S)),sha256=hashlib.sha256(document_bytes(str(p.relative_to(S)),root=S)).hexdigest(),url='https://github.com/venwry/vs_edu1/blob/52662752fae4abf14ce6a8adab2e4554ea932677/'+p.name) for p in [S/n for n in ['generated/models/sales-forecast.json','generated/models/manufacturing-costs.json','generated/catalogs/logix-aion-technical-catalog-v2.json','generated/models/pricing-results.json','generated/catalogs/hardware-bom.json','generated/catalogs/logix-aion-story.json','generated/catalogs/manufacturing-programs.json','generated/catalogs/memory-manufacturing.json','baselines/memory-manufacturing-baseline.json','generated/catalogs/team-development-program.json','tools/market_outlook.py','generated/catalogs/sales-model-inputs.json']]]
monthly={r['month']:{'products':r['products'],'basis':r['basis']} for r in next(s for s in sales['scenarios'] if s['id']=='central')['monthly'] if r['computer_units']}
sensitivities=[]
for scenario in sales['scenarios']:
 demand=scenario['monthly'];peak=max(r['computer_units'] for r in demand)
 sensitivities.append({'scenario':scenario['id'],'computer_demand_1978_1981':sum(r['computer_units'] for r in demand),'horizon':'1978–1982 (stable report key)','peak_month_computers':peak,'capacity_with_reserve':math.ceil(peak*1.05)})
# Cost and component links: each final sellable offering once, not every catalog row.
chip_vintages=defaultdict(lambda:defaultdict(float))
links=[]; chip_q=defaultdict(lambda:defaultdict(float)); q_units=defaultdict(float); q_month_peak=defaultdict(float)
q_entity_buckets=defaultdict(lambda:defaultdict(lambda:defaultdict(float))); q_components=defaultdict(lambda:defaultdict(float))
for m,row in monthly.items():
 q=quarter(m);year=int(m[:4]);q_units[q]+=sum(row['products'].values());q_month_peak[q]=max(q_month_peak[q],sum(row['products'].values()))
 items=defaultdict(float)
 for family,n in row['products'].items():
  for b in baskets[family]:
   for ref,mult in expand(b['product_ref']):items[ref]+=n*b['quantity']*mult
 # Historical additional application cohorts, no inferred external OEM hardware.
 for r in inputs['standalone_applications']:
  if r['month']==m:
   a=r.get('applications',{});items['software.abacus_2']+=a.get('existing_aurelia_abacus2_licenses',0);items['software.pulse_1']+=a.get('pulse_licenses_on_new_aurelia_plus',0)
 installs=sum(row['products'].values())*.2
 items['software.bpi_suite.bpi_general_accounting']+=installs*.5
 for ref in ['software.bpi_suite.bpi_general_accounting','software.bpi_suite.bpi_accounts_receivable','software.bpi_suite.bpi_accounts_payable','software.bpi_suite.bpi_inventory_control']:items[ref]+=installs*.25
 items['software.bpi_suite']+=installs*.25
 # Additional independent cards/upgrades lack forecasts; demand allowance is explicit, not zero.
 if m>='1979-06':
  for ref in ['device.apple2_expansion_card','device.s100_flexibus_card','device.apple2_video_card','device.s100_video_card']:
   if ref in cp:items[ref]+=sum(row['products'].values())*.02
 if m>='1981-07':items['software.bpi_client_server']+=row['products'].get('artemis_pro',0)
 # Team software and a modest network attach: half of buyers equip four existing
 # clients (two of each family) and one 8-port hub; server networking is bundled.
 if team_units(m):
  items['software.aion_development_team']+=team_units(m)
  for ref,mult in [('bundle.aurelia_network_upgrade',1),('bundle.artemis_network_upgrade',1),('device.network_hub.8_port',.5)]:
   for part,count in expand(ref):items[part]+=team_units(m)*mult*count
 for ref,units in items.items():
  if not units:continue
  # Preserve old cost vintage until June price snapshots; first available cost for new products is a labelled proxy.
  sy=max(1978,year-(int(m[5:])<6));snap,sy=snapshot(ref,sy);owner='BPI' if 'bpi' in ref else ('Logix' if ref.startswith('software.cpm') else ('AION Software' if ref.startswith(('software.','edition.')) else 'Logix'))
  buckets=dict(snap['breakdown_usd']);internal=defaultdict(float);bom=[]
  for line in snap.get('bom_lines',[]):
   part=line['component_ref'];qty=line['quantity']*units;q_components[q][part]+=qty;bom.append({'component_ref':part,'quantity_per_offer':line['quantity']})
   cref=part.removeprefix('bompart.')
   if cref in chips:
    chip_q[q][cref]+=qty
    chip_vintages[q][(cref,sy)]+=qty
    for k,v in costs['component_cost_assumptions'][part]['annual_cost_buckets_usd'][str(sy)].items():internal[k]+=v*line['quantity']
  for k,v in buckets.items():
   q_entity_buckets[q][owner][k]+=units*(v-internal.get(k,0))
  links.append(dict(month=m,quarter=q,entity=owner,product_ref=ref,units=round(units,4),cost_snapshot_year=sy,unit_cost_usd=snap['total_usd'],embedded_aion_chip_cost_usd=round(sum(internal.values()),5),external_and_nonfab_cost_usd=rnd(units*(snap['total_usd']-sum(internal.values()))),cost_type_usd={k:rnd(units*(v-internal.get(k,0))) for k,v in buckets.items()},bom=bom))
# Chip wafer demand, per family, already contains package and die yield. Reserve is capacity, not automatic overproduction.
wafer_rows=[];wafer_peak={};good_chip_total={}
for q in quarters:
 y=max(1978,int(q[:4]));total=0;goods=0
 groups=[(ref,n,vintage) for (ref,vintage),n in chip_vintages[q].items()]
 for ref,n,vintage in groups:
  model=chips[ref][str(vintage)];good=model['gross_usable_dies']*model['die_yield']*model['packaging_test_yield'];w=math.ceil(n/good);total+=w;goods+=n
  wafer_rows.append(dict(quarter=q,chip_ref=ref,cost_snapshot_year=vintage,good_chips=math.ceil(n),good_packaged_dies_per_wafer=round(good,3),wafer_starts=w,die_area_mm2=model['die_area_mm2'],die_yield=model['die_yield'],package_yield=model['packaging_test_yield']))
  unit=costs['component_cost_assumptions']['bompart.'+ref]['annual_cost_buckets_usd'][str(vintage)]
  for k,v in unit.items():q_entity_buckets[q]['AION Labs'][k]+=n*v
 ratio=q_month_peak[q]/(q_units[q]/3) if q_units[q] else 1
 wafer_peak[q]=math.ceil(total/3*ratio*1.05*1.05) # 5% engineering/monitor wafers beyond 5% commercial reserve
 good_chip_total[q]=goods
# Fab equipment capacities are engineering assumptions with explicit operation counts and OEE.
equipment=[
 ('projection','Perkin-Elmer Micralign (1973 family)','lithography',25,8,180000,35,'planning passes/hour; eight masks; qualify 3 µm process window and throughput with process-matched masks before release'),
 ('resist','Period manual spin coat/develop stations','lithography',35,8,45000,18,'manual stations; no modern track assumed'),
 ('furnace','Thermco horizontal diffusion/oxidation furnace bank','thermal',100/6,6,140000,45,'100-wafer batch/6 h; six equivalent thermal visits'),
 ('lpcvd','Period horizontal hot-wall CVD tube system','deposition',75/4,3,130000,35,'75 wafers/4 h; polysilicon/dielectric recipe compatibility unresolved'),
 ('implant','Varian/Extrion period ion implanter, exact model to qualify','implant',35,2,280000,40,'threshold/source-drain recipe; commissioning and dose uniformity gate'),
 ('wet','Segregated wet-clean/etch benches','clean/etch',80,12,45000,28,'twelve batch-equivalent visits; chemistry and exhaust segregation'),
 ('metal','Varian period vacuum aluminium evaporator','metallization',50/2,1,100000,30,'50-wafer load/2 h; NMOS metallization assumption'),
 ('metrology','Optical microscope, film-thickness and electrical metrology station','metrology',35,4,60000,18,'four equivalent sample-normalized visits'),
 ('probe','Electroglas wafer prober with period memory/logic tester','wafer test',8,1,150000,20,'8 wafers/hour; video RAM retention tests may lower throughput'),
 ('dice','Period wafer saw and die-attach cell','back end',1200,1,90000,25,'good-die equivalents/hour'),
 ('bond','Kulicke & Soffa period wire-bond workstation','back end',140,1,40000,14,'finished packages/hour, pin-count dependent'),
 ('package','Package sealing and lead-finish cell','back end',350,1,75000,25,'packages/hour; procure leadframes/ceramic shells'),
 ('test','Period memory/LSI final-test and burn-in cell','back end',180,1,180000,30,'packages/hour; programmable fixtures and memory dwell gate')]
stages=[]
for id,start,end in [('pilot','1976-Q3','1977-Q4'),('launch','1978-Q1','1979-Q4'),('growth','1980-Q1','1981-Q4'),('1982_expansion','1982-Q1','1982-Q4')]:
 qs=[q for q in quarters if start<=q<=end];target=max([wafer_peak[q] for q in qs]+[300]);target=math.ceil(target/250)*250
 goods=max([good_chip_total[q]/3*(q_month_peak[q]/(q_units[q]/3) if q_units[q] else 1)*1.05/0.93 for q in qs]+[15000])
 tools=[]
 for eid,name,step,rate,visits,usd,area,note in equipment:
  req=goods if step=='back end' else target
  per=rate*24*30*.65/visits
  n=max(2,math.ceil(req/per)+1) # one redundant unit; OEE applied independently
  tools.append(dict(id=eid,machine=name,count=n,nominal_1978_unit_cost_usd=usd,installed_cost_usd=rnd(n*usd*1.25),footprint_m2=n*area,passes_per_wafer=visits,rate_per_hour=round(rate,3),effective_monthly_capacity_one_down=round((n-1)*per),basis=note))
 clean=math.ceil(sum(t['footprint_m2'] for t in tools if t['id'] not in ['dice','bond','package','test'])*2/100)*100
 gross=math.ceil((clean*2.7+sum(t['footprint_m2'] for t in tools if t['id'] in ['dice','bond','package','test'])*2+650)/100)*100
 stages.append(dict(id=id,commissioned=start,through=end,wafer_starts_per_month=target,packaging_input_per_month=math.ceil(goods),cleanroom_m2=clean,gross_building_m2=gross,site_hectares=round(gross*3/10000,2),tools=tools,tool_installed_1978_usd=sum(x['installed_cost_usd'] for x in tools),facility_1978_usd=round(clean*1700+(gross-clean)*420+900000),design_power_kw=round(gross*.12),water_m3_day=round(target/30*.22+25),notes='Capacity assumes 24/7 four-crew operation, 65% tool OEE, one redundant unit per critical group. Footprints include service corridors; gross adds utilities, back end, labs and offices. All rates, prices and facilities intensities are planning assumptions.'))
# Quarterly ledger: resource expenses separate from intra-ecosystem reimbursements and equity financing.
ledger=[];capacity=[];capital=[];team_reconciliation=[]
def cap(q,e,kind,amount,note):capital.append(dict(quarter=q,entity=e,cost_type=kind,usd=rnd(amount),basis=note))
for item in memory_policy()['capital_schedule']:
 if item['quarter'] in quarters:cap(item['quarter'],'AION Labs','memory_process_equipment',item['usd'],item['purpose'])
prevtools=prevbuilding=0
for stage in stages:
 tq=qi(stage['commissioned']);yy=int(stage['commissioned'][:4]);infl=1.08**(yy-1978)
 for typ,tot,prev in [('fab_equipment',stage['tool_installed_1978_usd'],prevtools),('fab_building_utilities',stage['facility_1978_usd'],prevbuilding)]:
  delta=max(0,tot-prev)*infl
  for offset,share in [(-4,.15),(-3,.25),(-2,.35),(-1,.25)]:cap(quarters[tq+offset],'AION Labs',typ,delta*share,'Capacity commissioned '+stage['commissioned']+'; phased procurement/install; quoted price unavailable')
 prevtools=stage['tool_installed_1978_usd'];prevbuilding=stage['facility_1978_usd']
for q,amt in [('1975-Q2',120000),('1976-Q2',180000),('1977-Q2',260000),('1979-Q2',400000)]:cap(q,'AION Labs','process_test_development_equipment',amt,'Pilot characterization and design/test equipment; secret future machinery acquisition unpriced')
# Incremental card/monitor capacity above the pre-revision per-system envelope.
def display_mix(q):
 rows=[r['products'] for m,r in monthly.items() if quarter(m)==q];total=sum(sum(r.values()) for r in rows)
 art=sum(r.get('artemis',0) for r in rows)/total if total else 0
 pro=sum(r.get('artemis_pro',0) for r in rows)/total if total else 0
 return art,pro
assembly_area=0;dc_area=0;centres=0;prior_wc=0;prior_software_seats=defaultdict(int)
for q in quarters:
 y=int(q[:4]);idx=qi(q);infl=1.08**(y-1978);wage={1974:4.2,1975:4.6,1976:5.0,1977:5.5,1978:5.99,1979:6.54,1980:7.08,1981:7.85,1982:8.45}[y]*1.35
 current_peak=q_month_peak[q];future_peak=max([q_month_peak[k] for k in quarters[idx:min(idx+3,len(quarters))]]+[0]);required=math.ceil(future_peak*1.05)
 stage=next((s for s in reversed(stages) if s['commissioned']<=q),None)
 # Assembly supplier policy: outsourced bare PCBs, displays, drives, keyboards, metal/plastic, cartons and bulk print.
 direct_hours=sum(v['workforce'] for e,v in q_entity_buckets[q].items() if e=='Logix')/wage
 direct_fte=math.ceil(direct_hours/390) if direct_hours else 0
 art,pro=display_mix(q);am=revision['mono_pro_artemis_bundle_share'];pm=revision['mono_pro_pro_console_share']
 future_mixes=[display_mix(k) for k in quarters[idx:min(idx+3,len(quarters))]]
 station_hours=max([10+.6*(a+p)+.5*a*am+2.25*p*pm for a,p in future_mixes])
 volume=.22+.04*art*am+.12*pro*pm;tonnes=.045+.004*art*am+.015*pro*pm
 reserved_volume=max([.22+.04*a*am+.12*p*pm for a,p in future_mixes])
 pcb_area=.6+.04*(art+pro)+.02*art*am+.08*pro*pm
 stations=math.ceil(required*station_hours/(22*2*8*.8)) if required else 0
 reqarea=math.ceil((stations*14+required/22*6+600)/500)*500 if required else (500 if q>='1976-Q1' else 0)
 reqdc=math.ceil((required*reserved_volume*.5/.9+200)/250)*250 if required else 0
 if reqarea>assembly_area:cap(q,'Logix','factory_fitout_and_equipment',(reqarea-assembly_area)*220*infl,'Leased industrial shell, ESD benches, through-hole wave solder, fixtures and burn-in; two-quarter look-ahead');assembly_area=max(assembly_area,reqarea)
 if reqdc>dc_area:cap(q,'Logix','distribution_fitout',(reqdc-dc_area)*90*infl,'Three regional nodes as demand grows; leased floor area, racking and handling');dc_area=max(dc_area,reqdc)
 enrol=0;days=0
 for r in inputs['academy_requests']:
  if quarter(r['month'])==q:
   for name,v in r['courses'].items():days+=v['requested_enrolments']*inputs['academy_course_days'][name]/6
   enrol+=r['new_requests']
 if q>='1980-Q2':
  # Post-May training forecast is absent: use independent 30% new-system enrolments, five days each.
  enrol=max(enrol,q_units[q]*.30);days=max(days,enrol*5/6)
 elif '1978-Q2'<=q<'1979-Q2':enrol=q_units[q]*.4;days=enrol*4/6
 rooms=math.ceil(days*1.05/(54*.85)) if days else 0;instructors=math.ceil(days*1.05/45) if days else 0
 needcentres=min(24,max(5,math.ceil(rooms/3))) if rooms else 0
 if needcentres>centres:cap(q,'Logix','academy_fitout',(needcentres-centres)*30000*infl,'Leased three-room centres; furniture and fitout; classroom computers budgeted separately');centres=max(centres,needcentres)
 training_hw=max(0,rooms*9-(capacity[-1]['training_computers'] if capacity else 0));cap(q,'Logix','academy_computers',training_hw*1200*infl,'Nine computers/room; incremental internal-equipment allowance at cost; omitted from retail sales') if training_hw else None
 logfte=math.ceil((q_units[q]*volume/3*1.05)/(22*6)) + (9 if q_units[q] else 0)
 # Staff support is based on included service budget and avoided double payroll.
 support_budget=q_entity_buckets[q]['Logix'].get('included_service_delivery',0)
 supportfte=math.ceil(support_budget/(wage*1.6*520))
 capacity.append(dict(quarter=q,customer_computers=math.ceil(q_units[q]),peak_month_customer_demand=math.ceil(current_peak),installed_computer_capacity_month=required,assembly_gross_m2=assembly_area,assembly_stations=stations,distribution_total_m2=dc_area,logistics_fte=logfte,assembly_direct_fte=direct_fte,academy_centres=centres,academy_rooms=rooms,dealer_hosted_rooms=max(0,rooms-centres*3),academy_instructors=instructors,training_computers=rooms*9,course_enrolments=math.ceil(enrol),display_mix_assumptions={'artemis_share':art,'pro_share':pro,'mono_pro_artemis_uptake':am,'mono_pro_pro_uptake':pm,'station_hours_per_system':station_hours,'packed_m3_per_system':volume,'packed_tonnes_per_system':tonnes,'supplier_pcb_m2_per_system':pcb_area},factory_shift_pattern='2 x 8 h, 22 days/month, 80% productive utilization',outbound_m3_month=rnd(current_peak*volume),outbound_tonnes_month=rnd(current_peak*tonnes),linehaul_trailer_loads_month=math.ceil(current_peak*volume/55),dealer_drops_week=math.ceil(current_peak/4.33/12),carton_capacity_month=math.ceil(required*5),manual_pages_month=math.ceil(required*500),media_sets_month=math.ceil(required*3),supplier_bare_pcb_m2_month=round(required*pcb_area),fab_wafer_starts_required_month=wafer_peak[q],fab_capacity_month=stage['wafer_starts_per_month'] if stage else 0))
 for e in entities:
  buckets=dict(q_entity_buckets[q][e]);eng=sum(p['person_months']/(qi(p['end'])-qi(p['start'])+1)/3 for p in programs if p['entity']==e and p['start']<=q<=p['end'])
  scheduled_eng=eng
  prior_peak=max([sum(p['person_months']/(qi(p['end'])-qi(p['start'])+1)/3 for p in programs if p['entity']==e and p['start']<=z<=p['end']) for z in quarters[:idx+1]]+[0])
  if q>='1978-Q3':eng=max(eng,prior_peak*.60)
  active=(q>='1975-Q1') if e in entities[:3] else (q>='1974-Q4' if e=='DRI' else q>='1977-Q1')
  prod=direct_fte if e=='Logix' else (math.ceil((stage['wafer_starts_per_month']/300)*4+45) if e=='AION Labs' and stage else (6 if e=='AION Labs' and q>='1975-Q3' else 0))
  # Labs staffing: production four crews; additional sustaining process staff counted separately below.
  process=(math.ceil(prod*.40)+12 if stage else 3) if e=='AION Labs' and active else 0
  ops=math.ceil(prod*.22) if e=='Logix' else process
  service=(supportfte+instructors+logfte+centres*2) if e=='Logix' else (math.ceil(q_units[q]/15000)+2 if active and q>='1978-Q2' else 0)
  admin=math.ceil((eng+prod+ops+service)*.13)+(2 if active else 0)
  hc=math.ceil(eng)+prod+ops+service+admin
  # Engineering salaries: 1978 loaded annual USD 30k; specialist fab 28k; operations 520 paid hours/q.
  engcost=eng*7500*infl;prod_pay=prod*wage*520;opspay=(ops+admin)*6500*infl
  servicepay=(instructors*7800*infl+logfte*5000*infl+centres*2*4500*infl+supportfte*wage*1.6*520) if e=='Logix' else service*6500*infl
  embedded=buckets.get('workforce',0)+buckets.get('operating_overhead',0)+buckets.get('included_service_delivery',0)
  salaries=prod_pay+opspay+servicepay
  for k in ['workforce','operating_overhead','included_service_delivery']:buckets.pop(k,None)
  buckets['production_service_admin_payroll']=max(embedded,salaries) # baseline minimum avoids deleting outsourced/support expenses
  pilot=memory_policy()['pilot_operations']
  if e=='AION Labs' and pilot['from_quarter']<=q<=pilot['through_quarter']:
   buckets['stepper_pilot_nonpayroll']=pilot['wafers_per_month']*3*pilot['processed_wafer_usd']+pilot['nonpayroll_operations_usd_per_quarter']
  buckets['engineering_payroll']=engcost
  if e=='AION Software' and team_quarter_budget(q):
   gross=team_quarter_budget(q)
   # Half the paid unscheduled engineering reserve remains protected for maintenance.
   credit=min(max(0,eng-scheduled_eng)*7500*infl*.5,max(0,gross-(45000 if q.startswith('1981') else 0)))
   buckets['team_incremental_development']=gross-credit
   team_reconciliation.append({'quarter':q,'gross_development_usd':rnd(gross),'existing_payroll_allocated_usd':rnd(credit),'incremental_development_usd':rnd(gross-credit),'basis':'At most half of already paid retained sustaining capacity is reassigned; contingency is fully incremental. Initial network authentication/OS work is already funded and excluded from Team scope.'})
  if e=='AION Labs' and q.startswith('1982'):
   # Existing 1982 forward engineering provision includes payroll AND validation.
   gross=150000
   credit=min(engcost*.5,gross)
   buckets['memory_1982_engineering_topup']=gross-credit
   buckets['stepper_pilot_nonpayroll']=36000
  if e=='DRI' and q.startswith('1982'):
   # Eight engineers on MMU/reference-machine feasibility, no shipping port revenue.
   buckets['aionix_68k_port_topup']=max(0,8*7500*infl-engcost*.5)
   buckets['aionix_68k_prototype_validation']=20000

  buckets['engineering_prototypes_masks_validation']=engcost*(.25 if e in ['Logix','AION Labs'] else .10)
  area=assembly_area+dc_area+min(rooms,centres*3)*90 if e=='Logix' else (stage['gross_building_m2'] if e=='AION Labs' and stage else (hc*14))
  buckets['facilities_lease_maintenance']=area*(12 if e=='AION Labs' else 9)*infl if active else 0
  if e=='AION Labs' and stage:
   # HVAC base load is additive: prior unit energy covers process only.
   buckets['base_load_utilities']=stage['design_power_kw']*.5*24*91*{1976:.022,1977:.025,1978:.028,1979:.031,1980:.037,1981:.043,1982:.047}.get(y,.02)
   buckets['equipment_service_spares']=stage['tool_installed_1978_usd']*.05/4*infl
  if e=='Logix' and rooms>centres*3:buckets['dealer_hosted_classroom_rental']=(rooms-centres*3)*54*80*infl
  if e=='Logix' and q>='1977-Q4':buckets['campaign_dealer_enablement']=max(60000*infl,q_units[q]*18)
  if e=='AION Software' and active:buckets['international_coordination_travel']=engcost*.06
  if e=='BPI' and active:buckets['accounting_domain_validation']=engcost*.12
  if active:
   seats=math.ceil(eng)+admin
   if seats>prior_software_seats[e]:cap(q,e,'engineering_office_equipment',(seats-prior_software_seats[e])*5000*infl,'Terminals, shared development computer allocation, lab/office equipment; not future-tool acquisition');prior_software_seats[e]=seats
  capex=sum(x['usd'] for x in capital if x['quarter']==q and x['entity']==e)
  ledger.append(dict(quarter=q,entity=e,headcount=hc,roles={'development_engineering':round(eng,2),'scheduled_programme_fte_subset':round(scheduled_eng,2),'retained_sustaining_fte_subset':round(eng-scheduled_eng,2),'production':prod,'process_quality_supervision':ops,'service_training_logistics':service,'administration':admin},cost_type_usd={k:rnd(max(0,v)) for k,v in buckets.items()},operating_usd=rnd(sum(max(0,v) for v in buckets.values())),capital_usd=rnd(capex),cash_spend_before_working_capital_usd=rnd(capex+sum(max(0,v) for v in buckets.values())),embedded_payroll_overhead_replaced_usd=rnd(embedded)))
 # 45 days purchased-input + 14 days finished goods + 5% one-month reserve stock; no receivables/payables assumptions.
 unitcost=sum(x['external_and_nonfab_cost_usd'] for x in links if x['quarter']==q)
 wc=unitcost*(45+14+1.5)/91
 capacity[-1]['gross_inventory_funding_usd']=rnd(wc);capacity[-1]['inventory_cash_change_usd']=rnd(wc-prior_wc);prior_wc=wc
# Intercompany payments/receipts are displayed separately from the sum of resource expenses.
transfers=[]
for q in quarters:
 dri_pm=sum(p['person_months']/(qi(p['end'])-qi(p['start'])+1) for p in programs if p['id']=='aionix_dri' and p['start']<=q<=p['end'])
 if dri_pm:transfers.append(dict(quarter=q,payer='AION Software',recipient='DRI',type='AIONix cost reimbursement',usd=rnd(dri_pm*2500*1.08**(int(q[:4])-1978)*1.23),treatment='Cash payment/receipt only; DRI payroll already included in resource expenses; eliminate in ecosystem sum'))
 royalties=sum(x['units']*x['cost_type_usd'].get('recurring_licenses',0)/x['units'] for x in links if x['quarter']==q and 'microsoft' not in x['product_ref'])
 if royalties:transfers.append(dict(quarter=q,payer='Logix / distributed product owner',recipient='DRI',type='provisional CP/M royalty',usd=rnd(royalties),treatment='Already in product cost; eliminate for ecosystem-resource total; exact contractual terms unresolved'))
# Finance the next quarter's inventory target before demand arrives; no supplier-credit assumption.
prior=0
for i,c in enumerate(capacity):
 target=capacity[min(i+1,len(capacity)-1)]['gross_inventory_funding_usd']
 c['gross_inventory_funding_usd']=target;c['inventory_cash_change_usd']=rnd(target-prior);prior=target
summary=[]
for y in range(1974,1983):
 rows=[r for r in ledger if r['quarter'].startswith(str(y))];qs=[c for c in capacity if c['quarter'].startswith(str(y))];elim=sum(t['usd'] for t in transfers if t['quarter'].startswith(str(y)) and t['type']=='provisional CP/M royalty')
 summary.append(dict(year=y,computer_demand=sum(c['customer_computers'] for c in qs),capex_usd=rnd(sum(r['capital_usd'] for r in rows)),entity_operating_sum_usd=rnd(sum(r['operating_usd'] for r in rows)),ecosystem_resource_operating_usd=rnd(sum(r['operating_usd'] for r in rows)-elim),year_end_headcount=sum(r['headcount'] for r in rows if r['quarter'].endswith('Q4')),year_end_inventory_funding_usd=qs[-1]['gross_inventory_funding_usd']))
model={'metadata':{'title':'Logix / AION industrial investment and workforce plan','version':'1.0','source_repository':'venwry/vs_edu1','source_commit':'b7e15dbc062fe52bb86e156e27c3190195047134','created':'2026-10-11','horizon':'1974-Q1 through 1982-Q4','currency':'nominal USD of each quarter; 8% annual escalation for new planning allowances, repository unit costs retain dated snapshots','status':'Engineering scenario, not historical accounts, supplier quotations or released production design','previous_sessions':'Unavailable; committed forecasts used instead','ownership':'Five independently reported entities; sum is ecosystem resource requirement, not a legal consolidated financial statement'},'summary_annual':summary,'assumptions':{'reserve':'5% installed good-output headroom; not 5% extra sales or perpetual overproduction. One-month 5% reserve inventory funded separately. 5% additional fab engineering/monitor/training-equipment allowance. Tool one-down redundancy and OEE are separate availability protections.','demand':'Central unconstrained first-year intent plus signed reaction effects; thereafter new demand only, no repeated returning backorders. Premium-price discouraged buyers are not demand at the offered price. 1980 Nov 19 onward explicitly extrapolated.','1981_extension':'Superseded by market_outlook.py: explicit quarterly demand through 1982; PRO conditional from July 1981.','unforecast_scope':'External OEM silicon licences are not chip orders. Tandy hardware excluded. Selected add-in cards have explicit 2% attach allowance; other unforecast products remain unquantified and are listed as gaps. Full demand claim applies to modeled baskets, not unknown catalog demand.','geography':'Logix assembly San Jose; AION Labs Cambridge assumed Massachusetts (confirm); AION applications Copenhagen with OS group near DRI California. US distribution; Denmark costs are USD planning equivalents, not a local DKK payroll/FX forecast.','manufacturing':'Buy bare PCBs, remaining externally sourced system DRAM/CPUs, displays, drive/printer mechanisms, molded/metal parts, packaging and bulk print. Make custom logic, AION system controllers, AION 2114 sprite SRAM and AION 4116 display-memory chips and AION 64K system DRAM for Aurelia+ / Artemis, populate/test boards, integrate and pack. Supplier reserved capacity is specified; supplier-owned plants are not Logix capital.','staff_retention':'Retain at least 60% of historical peak programme engineering FTE from 1978 Q3 for defects, releases and next designs; paid sustaining capacity above scheduled work is separately identified. Training uses up to 24 dedicated centres and dealer-hosted rooms thereafter.', 'software_estimation':'130 productive hours/person-month; quarterly smooth staffing per programme; 0.7–1.7 effort envelope, not statistical probability. Staffing cannot replace elapsed integration and pilot time.','cost_boundary':'Capex plus operating resource expenses; depreciation excluded from cash totals. Debt interest, taxes, stock compensation and receivables/payables excluded. Inventory cash changes separate. Purchased component costs include suppliers’ margins/capital.','payroll':'Embedded production workforce/overhead/support replaced by larger of existing allowance and staffing cash payroll, never added twice. Any excess baseline allowance represents outsourced/other operations.','capital_timing':'Fab ordered four quarters before commissioning. Assembly uses two-quarter forward peak; facilities planning capacity must precede customer shipments. Academy equipment allowance is separate and not inferred retail demand.','secret_facility':'Future CAD/laser lithography retained as narrative premise; acquisition/replacement and maintenance dependencies unpriced, outside public-company budget. Mask/test development consumables included.'},'sources':source_refs,'historical_anchors':[{'title':'ASML / Perkin-Elmer history','url':'https://www.asml.com/en/company/stories/2023/seven-things-about-our-wilton-history','use':'Micralign first shipped 1973 at $95,000; model 1978 allowance $180,000 is not a quote.'},{'title':'SEMI oral history, Dennosuke Uchida','url':'https://www.semi.org/en/Oral-History-Interview-Dennosuke-Uchida','use':'GCA steppers reached production in 1977, Japan early 1978; early throughput constraints support projection-aligner baseline.'},{'title':'Computer History Museum equipment suppliers','url':'https://www.computerhistory.org/siliconengine/turnkey-equipment-suppliers-change-industry-dynamics/','use':'Period vendor families for furnaces, vacuum/implant, probe and deposition; exact models/recipes require qualification.'},{'title':'ASML founding history','url':'https://www.asml.com/en/company/about-asml/history','use':'ASML PAS 2000 launched 1984, therefore excluded from 1974–81 line.'}],'engineering_programs':programs,'monthly_demand':monthly,'scenario_demand_sensitivity':sensitivities,'quarterly_capacity':capacity,'fab_stages':stages,'quarterly_component_requirements':[{'quarter':q,'component_ref':p,'production_quantity':round(n,3),'supplier_reserved_quantity':math.ceil(n*1.05),'quantity_status':'Functional sets remain sets when source BOM quantity is unresolved'} for q,parts in q_components.items() for p,n in parts.items()],'quarterly_wafer_loading':wafer_rows,'product_cost_links':links,'quarterly_entity_costs':ledger,'capital_schedule':capital,'interentity_transfers':transfers,'financing_events':[{'quarter':'1974-Q4','recipient':'DRI','usd':250000,'status':'founder commitment in story; quarter placement assumption','treatment':'equity funding, not operating expense'},{'quarter':'1977-Q1','recipient':'BPI','usd':150000,'status':'offer only, not assumed closed','treatment':'excluded from expense and committed funding'}],'logistics_design':{'nodes':['San Jose assembly / western distribution','Chicago-area leased cross-dock / central distribution','Cambridge-area eastern distribution and AION fab dispatch'],'flows':['Qualified supplier deliveries → San Jose receiving, ESD/quarantine and incoming test','Cambridge packaged chips → San Jose weekly insured air shipment; 4-week chip buffer before peak ramps','San Jose finished packages → three regional nodes by consolidated road linehaul','Regional nodes → ComputerLand stores weekly LTL delivery and replenishment; dealer count unknown, drops inferred at 12 systems/drop','Academy computers → centres before course launch; manuals/media replenished monthly; returns routed to regional repair pool'],'parameters':{'package_volume_m3_per_computer_basket':.22,'package_mass_kg':45,'usable_trailer_m3':55,'pallet_m3':.9,'cartons_per_basket':5,'manual_pages_per_basket':500,'media_sets_per_basket':3,'print_capacity_rule':'500 pages x installed system capacity; outsource offset print/binding, 4-week buffer; verify actual editions/page counts before order','linehaul_rule':'ceil(monthly basket volume / 55 m3); contracted carriers, not owned fleet','service_target':'weekly dealer replenishment, 14-day finished goods, 45-day purchased input buffer funded one quarter ahead; inventory buffer is scenario not optimized service simulation'},'cost_treatment':'Repository per-offer freight retained; warehouse labor/facility cash floor budgeted separately. No second per-truck charge added. Carrier lane quotes, customer/store counts and split-shipment volumes unresolved.'},'fab_recommendation':{'public_process':'75 mm, 3 µm silicon-gate NMOS target for the costed 52 mm² video controller, 30 mm² system controller, 20 mm² sprite SRAM and 18 mm² AION 4116 DRAM; 3.5 µm sensitivity requires larger dies and a fresh capacity/cost run. Logic, SRAM and DRAM process compatibility, retention, sense amplifiers and process window require validation. Analog/DAC integration is a separate recipe qualification gate.','preferred_lithography':'Micralign projection for period availability, mask life and mature-node throughput; reserve space and reticle conversion budget before considering GCA 4800 on a later critical-layer pilot. No stepper savings assumed without wafer trials.','wafer_supply':'Buy prime polished doped wafers; no crystal puller or wafer slicing/polishing factory. No epitaxy reactor in base NMOS flow unless device design requires epitaxial substrate.','mask_supply':'Future facility supplies design/master capability; public mask inspection, revision control and process-matched working masks remain necessary.','optimality':'Least-complex fit to stated 75 mm process and modeled volumes, not proven global optimum. Compare qualified SMC outsourcing with public-fab expansion at each gate; licence alone is not available wafer capacity.','expansion_gate':'Order expansion when six-month forecast exceeds 80% qualified one-down capacity; maintain recipe-specific tool matching and separation.','yield_stress':'Halving die yield doubles wafer starts at same shipments; package test yield 0.93 remains separate. Compute stressed load per row; reserve is insufficient to cover a 50% yield loss.','schedule_gates':['1975: process specification, utilities design and pilot contracts','1976 Q3: pilot tooling commissioned; 1976–77 recipe/video RAM qualification','1977: freeze first-production masks, PCB and interfaces; no sales before release qualification','1978 Q1: volume line ready, product qualification and inventory ahead of June launch','1979: fund extra ERA validation/respins and qualify expansion before 1980 launch','1981: PRO/network/customer pilots; July shipping is conditional scenario']},'open_gaps':['166 unresolved BOM quantity substitutions remain engineering functional-set assumptions, not released purchasable part counts.','Sales forecast omits many standalone peripherals, training after May 1980, upgrades, OEM die shipments and 1981 products; explicit new assumptions cover only selected gaps.','Full factory capacities depend on validated operation times; 10 assembly hours/basket for space sizing is a conservative planning routing separate from financial labor allowances.','Fab throughput, tool purchase prices, cleanroom construction, facility loads and staffing are engineering allowances with roughly -30%/+60% capex range.','No signed SMC supply capacity or outsourcing quotes; no claim of guaranteed production.','Architecture timing, ERA ISA validation, 64K DRAM procurement, video RAM retention and RDBMS crash recovery can force calendar delay regardless of hiring.','DRI independent OEM sales and BPI non-Logix business are outside workload and demand; headcounts cover this story programme only.','1982–2000 binary compatibility maintenance obligation remains unfunded beyond this horizon.']}
model['memory_manufacturing']={
 'policy_file':'generated/catalogs/memory-manufacturing.json',
 'era_policy':memory_policy()['era_policy'],
 'development_line':{'steppers_initial':1,'steppers_from_1980_Q2':2,'pilot_wafers_per_month':20,'one_down_capacity_wafers_month':1462,'production_output_credited':0,'basis':'Separate pilot bay; 25 passes/hour, eight layers, 65% OEE. No added saleable output or legacy capacity credit.'},
 'included_process_capital_usd':sum(x['usd'] for x in memory_policy()['capital_schedule'] if x['quarter'] in quarters),
 'future_capital_schedule':[x for x in memory_policy()['capital_schedule'] if x['quarter'] not in quarters],
 'future_engineering':[r for r in memory_policy()['future_engineering'] if int(r['period'])>1982],
 'boundary':'Future budgets after 1982 excluded from closed-horizon cash/ROI; reported as forward commitments. Recurring RAM repair costs are inside chip costs, not charged again as pilot operations.'}
model['fab_recommendation']['preferred_lithography']='Retain Micralign production, including ERA1 at 3 um. Separate GCA stepper development from 1979; qualify memory recipes and select lower recurring cost. Do not credit pilot output against sales capacity.'
model['fab_recommendation']['public_process']+=' Memory recipe and repair revisions follow generated/catalogs/memory-manufacturing.json; ERA1 is unchanged.'
model['team_development_reconciliation']=team_reconciliation
model['market_outlook_policy']=POLICY
model['assumptions']['continued_support']='1982 maintenance continues through retained engineering payroll; new Team, memory and DRI port budgets credit only explicitly allocated capacity. Additional programme funding can buy contractor services and is not presented as permanent employee headcount.'
model['assumptions']['demand']='Reassessed quarterly market-reaction forecast through 1982; monthly product counts match sales and ROI. Only the current sales forecast is retained.'
model['assumptions']['foresight']='Adam anticipates peaks: assembly uses a two-quarter look-ahead; fab expansion is ordered four quarters before commissioning. 5% is target commercial headroom, not a cap on indivisible equipment or installed idle capacity.'
model['memory_manufacturing']['engineering_1982']={'gross_provision_usd':600000,'incremental_topup_usd':rnd(sum(r['cost_type_usd'].get('memory_1982_engineering_topup',0) for r in ledger)), 'basis':'Half of paid retained Labs engineering payroll is allocated first; remainder is incremental. Pilot nonpayroll is separate. June 1982 mature 3 um RAM unit costs retained for volume; 2 um output not credited before repeatability.'}
model['open_gaps']=[x.replace('1982–2000','1983–2000').replace('1981 products','unmodeled products') for x in model['open_gaps']]
# Payer cash bridge, financing separate. Product costs retain traceable recurring categories.
for r in ledger:
 outgoing=sum(t['usd'] for t in transfers if t['quarter']==r['quarter'] and t['payer']==r['entity'] and t['type']=='AIONix cost reimbursement')
 incoming=sum(t['usd'] for t in transfers if t['quarter']==r['quarter'] and t['recipient']==r['entity'])
 r['additional_transfer_payments_usd']=outgoing;r['transfer_receipts_usd']=incoming
 r['cash_after_transfer_receipts_before_sales_and_inventory_usd']=rnd(r['cash_spend_before_working_capital_usd']+outgoing-incoming)
model['engineering_effort_totals']={e:{'scheduled_person_months':sum(p['person_months'] for p in programs if p['entity']==e),'additional_retained_sustaining_person_months':round(sum(r['roles']['retained_sustaining_fte_subset']*3 for r in ledger if r['entity']==e),1),'peak_engineering_fte':max(r['roles']['development_engineering'] for r in ledger if r['entity']==e)} for e in entities}
model['fab_cost_totals']={k:round(sum(r[k] for r in ledger if r['entity']=='AION Labs'),2) for k in ['capital_usd','operating_usd']}
model['facility_alternatives']=[{'option':'Preferred public integrated fab','basis':'Maintain story manufacturing independence; staged 75 mm line with one-down tool redundancy. More capital than outsourced pilot, but directly traceable capacity.'},{'option':'Contract pilot then build production line','basis':'Could avoid early duplicate pilot line operating cost. Requires compatible, confidential, contracted 1975–77 process access; not established by later SMC licence. No invented saving included.'},{'option':'Buy SMC-qualified dies after 1979','basis':'Evaluate source contract and masks/process compatibility per part; cost model in repository offers 1.6x internal recurring price proxy. Volume guarantees and non-recurring transfer costs remain unresolved.'}]
model['supplier_factory_equivalents']=[
 {'process':'Bare PCB manufacture','ownership':'external qualified supplier; capacity reservation not owned capex','peak_output_month':capacity[-1]['supplier_bare_pcb_m2_month'],'unit':'finished board m2','utilization':0.8,'assumed_output_m2_per_factory_m2_month':2.5,'equivalent_gross_factory_m2':math.ceil(capacity[-1]['supplier_bare_pcb_m2_month']/2.5/.8/100)*100,'basis':'Period photo-tool/drill/plating/etch/test line; complex multilayer share unresolved; throughput intensity assumption, not vendor commitment'},
 {'process':'Enclosures and metal chassis','ownership':'external supplier','peak_output_month':capacity[-1]['installed_computer_capacity_month']*3,'unit':'equivalent enclosure sets including peripherals','equivalent_gross_factory_m2':3500,'basis':'Approximately 12 moulding/forming cells x 4000 sets/month, plus tools, inspection and packing; exact materials/tool cavities unresolved'},
 {'process':'Cartons and protective inserts','ownership':'external converter','peak_output_month':capacity[-1]['carton_capacity_month'],'unit':'cartons','equivalent_gross_factory_m2':1500,'basis':'One finishing line reserved at 1200 cartons/hour x 176h x 0.65 = 137280/month; buy corrugated sheet, no paper mill'},
 {'process':'Printed manuals / binding','ownership':'external printer','peak_output_month':capacity[-1]['manual_pages_month'],'unit':'printed pages','equivalent_gross_factory_m2':1000,'basis':'Two offset press equivalents: 4000 sheets/h x 16 pages x 176h x 0.60 = 13.5m pages/month; finishing/binding can be bottleneck'},
 {'process':'Media duplication and packing','ownership':'Logix assembly allocation','peak_output_month':capacity[-1]['media_sets_month'],'unit':'media sets','equivalent_gross_factory_m2':450,'basis':'Included within assembly gross area; 16 parallel duplicate/verify stations at 6 sets/h x 352h x .8 = 27034 sets/month: use 32 stations = 54067. Cartridge programmer mix to qualify.'}]
model['pcb_architecture_delivery_plan']={'board_families':[{'family':'Aurelia / Aurelia+','new_layouts':8,'derivatives':6,'scope':'Motherboard, memory, floppy/FlexiBUS peripherals, keyboard/display interface, revised mapping; 2-layer first choice, 4-layer only when needed for return paths'},{'family':'Apple / S-100 compatibility','new_layouts':4,'derivatives':2,'scope':'Distinct bus voltage, decoding, connector and timing validation, not just connector replacement'},{'family':'Artemis / PRO','new_layouts':10,'derivatives':6,'scope':'Mainboards, paired RAM, storage, graphics, Z80 compatibility, network/hub and server variants; 4-layer planning assumption for mainboards'}],'effort_rule':'Simple derivative 1–3 PM; moderate board 4–7 PM; new high-speed mainboard 12–20 PM including bring-up; approximately 180–300 PCB-specific PM inside Logix programme totals, not additive. Architecture/firmware/system validation accounts for remaining Logix effort.','release_gates':['ISA/ABI, register map and bus ownership frozen before PCB freeze','Worst-case clock/setup/hold, refresh and video arbitration checked across all DMA masters','Power sequencing, rail currents, analog/digital return paths and decoupling verified','Two prototype spins per new mainboard; connector/PCB tooling controlled by revision','In-circuit/functional test fixtures and burn-in recipes released before volume production'],'limits':'Counts are grouped design-work estimates from offering families, not an asserted released drawing list; exact PCB dimensions/layers remain BOM open decisions.'}
model['cost_uncertainty']={'capital_low_usd':round(sum(x['capex_usd'] for x in summary)*.7),'capital_high_usd':round(sum(x['capex_usd'] for x in summary)*1.6),'basis':'Correlated scenario allowance, not confidence interval; operating costs depend separately on BOM, wages, volume, yield and outsourcing.'}
# Check totals and identify product demand not sized.
modeled={x['product_ref'] for x in links}
model['unquantified_catalog_offers']=[{'product_ref':p['id'],'reason':'No standalone demand forecast; may be included inside a modeled bundle, otherwise not sized'} for p in costs['products'] if p['id'] not in modeled]
for c in capacity:
 assert c['installed_computer_capacity_month']>=math.ceil(c['peak_month_customer_demand']*1.05)-1
 assert c['fab_capacity_month']>=c['fab_wafer_starts_required_month'],c
for r in ledger:assert abs(sum(r['cost_type_usd'].values())-r['operating_usd'])<.2
for st in stages:
 for t in st['tools']:assert t['effective_monthly_capacity_one_down']>=(st['packaging_input_per_month'] if t['id'] in ['dice','bond','package','test'] else st['wafer_starts_per_month'])-1
model['validation']={'status':'passed','checks':['36 quarters x 5 entities','quarterly category sums equal operating totals within rounding','installed assembly capacity >= demand plus 5%','fab qualified target >= required starts plus commercial reserve and monitor wafers','each equipment group meets stage target with one unit down','source hashes and cost/product/component references preserved'],'limitation':'Arithmetic and consistency validation only; no measured engineering feasibility or supplier quotes.'}
(OUT/'generated/models/industrial-investment-1974-1981.json').write_text(json.dumps(model,indent=2))
print(json.dumps({'annual':summary,'fab':[{k:v for k,v in s.items() if k!='tools'} for s in stages],'engineering_person_months':sum(p['person_months'] for p in programs),'product_links':len(links)},indent=2))
template=ROOT/'tools/industrial_investment_template.html'
if template.exists():
 import html
 site=read_document('generated/catalogs/site-pages.json', root=ROOT)
 pages={x['id']:x for x in site['pages']}
 navigation=''.join('<a href="'+html.escape(pages[i]['path'],quote=True)+'"'+(' aria-current="page"' if i=='industrial-investment' else '')+'>'+html.escape(pages[i]['title'])+'</a>' for i in site['navigation'])
 (OUT/'industrial_investment_1974_1981.html').write_text(template.read_text().replace('__PROJECT_NAV__',navigation).replace('__MODEL__',json.dumps(model,indent=2).replace('</','<\\/')))


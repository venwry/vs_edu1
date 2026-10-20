#!/usr/bin/env python3
"""Rebuild June-15 commercial pricing; run from any directory. USD, no tax."""
import json, math, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
load=lambda n:json.loads((ROOT/n).read_text())
costs=load('manufacturing_costs.json'); catalog=load('logix_aion_technical_catalog_v2.json')
C={p['id']:p for p in costs['products']}; YEARS=range(1978,1982)
sources={}
for y,title in [(1978,'Natural_Language'),(1979,'Artificial_Intelligence'),(1980,'Inter_Computer_Communications'),(1981,'Operating_Systems')]:
 sources['byte'+str(y)]={'title':f'BYTE June {y}, original vendor/dealer advertisements','date':f'{y}-06-01','date_note':'Issue month; June issue used as contemporary evidence, not a verified June 15 transaction.','url':f'https://vintageapple.org/byte/pdf/{y}06_Byte_Magazine_Vol_0{y-1975+0}-06_{title}.pdf'}
# BYTE volume is calendar year minus 1975.
sources['apple_support']={'title':'Apple Computer December 1980 prospectus, Service and Support','date':'1980-12-12','url':'https://doczz.net/doc/2960732/4600000-shares-apple-computer--inc.','facts':'Extended limited warranty $195/year from January 1980. Used only for 1981; hardware warranty is not equivalent to telephone assistance.'}
sources['training1977']={'title':'Microcomputer Digest Jan/Feb 1977, course listings','date':'1977-02-01','url':'https://manuals.plus/m/a04b31de011730336cf1777189472c4fd612bba6bfb5fc0f170b48cd4d2737a9','facts':'National Semiconductor four-day fundamentals course $395. Older engineering-training proxy, not a current office-user course quotation.'}
# Evidence records avoid implying estimated normalized baskets are advertised SKUs.
E={}
def evidence(k,name,price,year,page,note='',source=None):
 E[k]={'name':name,'observed_price_usd':price,'source_ref':source or 'byte'+str(year),'pdf_page':page,'comparison_limit':note}
evidence('h78','North Star Horizon-1 assembled, 16K, one disk',1899,1978,19,'Requires terminal and extra RAM; not an integrated 48K system.')
evidence('r78','North Star 16K assembled RAM board',459,1978,33,'S-100 board, not bare DRAM.')
evidence('t78','Soroc IQ120 assembled terminal',869.95,1978,182,'Terminal includes keyboard; more than a monitor.')
evidence('p78','Centronics 80-column printer advertised below $600',600,1978,55,'Upper-bound anchor; different printing mechanism and speed.')
evidence('disk78','North Star additional assembled drive',450,1978,33,'Cabinet and power supply separately $39 each.')
evidence('gl78','CBASIC general ledger package',995,1978,196,'High-end ledger proxy; not a price for each BPI module.')
evidence('a79','Apple II 48K',1495,1979,261,'Advertisement offers $200 accessory credit with this configuration.')
evidence('d79','Apple Disk II with controller',595,1979,261)
evidence('m79','Sanyo 9-inch monochrome monitor',169,1979,261)
evidence('ep79','Electric Pencil II CP/M edition',225,1979,183,'Full word processor; Business Tools only promises a text editor.')
evidence('basic79','Microsoft disk BASIC-80',300,1979,122,'CP/M version; Aurelia delivery/license terms differ.')
evidence('board79','16K S-100 RAM board',295,1979,269,'Board-level proxy; advertised promotional price.')
evidence('a80','Apple II 48K cash price',1100,1980,231)
evidence('d80','Apple Disk II with controller',495,1980,231)
evidence('m80','Sanyo 9-inch monochrome monitor',169,1980,231)
evidence('m12_80','Leedex 12-inch monochrome monitor',139,1980,231)
evidence('color80','Zenith 13-inch color monitor',429,1980,231,'Composite color, not identical Logix signal or resolution.')
evidence('v80','VisiCalc discounted',122,1980,223)
evidence('c80','BDS C compiler',125,1980,106,'Small C toolchain; not a complete native/cross IDE.')
evidence('wc80','Whitesmiths C',500,1980,133,'Advertised starting price; platform configuration may add cost.')
evidence('bpi80','Osborne/MICAH accounting application',95,1980,231,'General ledger, AR, AP, payroll; CBASIC/runtime and installation prerequisites differ.')
evidence('pt80','Peachtree business application',399,1980,223,'Higher-end alternative; not used to ignore cheaper Osborne offerings.')
evidence('ram80','CCS 64K dynamic RAM board',695,1980,223,'S-100 board; different electrical organization from Artemis.')
evidence('comm79','Apple communications card',225,1979,261,'Serial communication interface, not a FlexiBUS expansion bridge.')
evidence('comm80','Apple communications card',190,1980,231,'Serial communication interface, not a FlexiBUS expansion bridge.')
evidence('soft80','Microsoft Z80 SoftCard with CP/M',349,1980,231,'Does not include separate 64K onboard RAM as Artemis module does.')
evidence('p80','Axiom EX-801 printer',495,1980,231,'Different speed, paper handling and print technology.')
evidence('a81','Apple II Plus 48K',1189,1981,103)
evidence('d81','Apple Disk II with controller',529,1981,103)
evidence('m81','Sanyo 9-inch monochrome monitor',155,1981,427)
evidence('m12_81','Leedex 12-inch monochrome monitor',129,1981,427)
evidence('color81','Zenith 13-inch color monitor',349,1981,427)
evidence('v81','VisiCalc discounted',120,1981,427)
evidence('soft81','Microsoft Z80 SoftCard',269,1981,427,'No additional onboard RAM equivalence.')
evidence('ram81','California Computer Systems 64K dynamic RAM board',599,1981,427,'S-100; capacity-normalized multiples are estimates, not matching 32-bit banks.')
evidence('card81','Apple 16K memory card',169,1981,427,'Address mapping and compatibility differ.')
evidence('p81','Okidata Microline 80',420,1981,427)
evidence('disk81','CCI external 40-track disk drive',314,1981,427,'TRS-80 interface, 102K; not a full FlexiBUS equivalent.')
evidence('server81','Corvus 5 MB Winchester disk system',3750,1981,75,'Storage subsystem only, not a complete server.')
evidence('ii81','TRS-80 Model II 64K',3499,1981,427,'Business-system proxy; no ERA, MMU or 512K memory.')
evidence('acct81','CP/M general ledger / AR / AP / payroll',195,1981,357,'Inventory separately $395; several suppliers undercut premium packages.')
evidence('support81','Apple extended limited warranty',195,1981,None,source='apple_support')
evidence('course','NSC four-day microprocessor fundamentals',395,1977,None,'Older technical course, not equivalent office instruction.',source='training1977')
P=[]; byid={}
def add(id,name=None,group=None,bench=None,note='',start=None,unit=None,parts=None,direct=False,announced=False):
 c=C.get(id); p={'id':id,'name':name or c['name'],'type':group,'offering_start':start or c['available_from'],'offering_end':None,'unit':unit or (c['unit'] if c else 'one complete package'),'channel':'direct' if direct else 'ComputerLand','computerland_fee_rate':0 if direct else .25,'status':'approved_pricing_proposal','notes':[note] if note else [],'components':parts or [{'cost_ref':id,'quantity':1}],'benchmark_key':bench,'announced_only':announced or bool(c and c.get('announced_only')),'snapshots':{}}
 P.append(p);byid[id]=p;return p
# Per-year benchmark amounts are normalized estimates unless exactly identified below.
B={}
def bench(key,values,refs,description,kind='normalized_proxy'):
 B[key]={'values':values,'refs':refs,'description':description,'kind':kind}
bench('aurelia',[2800,2059,1764,1873],[['h78','r78','t78'],['a79','d79','m79'],['a80','d80','m80'],['a81','d81','m81']], '1978 conservative $2,800 basket estimate below Horizon 48K + terminal $3,686.95; 1979 Apple + disk + monitor less $200 accessory credit; later actual item sums. CP/M, support and display capability differ.')
bench('color',[3100,2359,2024,2067],[['h78','r78'],['a79','d79','m79'],['a80','d80','color80'],['a81','d81','color81']], '1978/79 color allowance $300 is estimated; 1980/81 Apple, drive and observed color monitor summed.')
bench('plus',[None,None,3000,2800],[[],[],['a80','d80','soft80'],['a81','d81','soft81']], 'Estimated 64K CP/M, 80-column, dual-drive business basket; includes allowances for second drive and display upgrade. Not an advertised package.')
bench('pluscolor',[None,None,3290,3020],[[],[],['a80','d80','color80','soft80'],['a81','d81','color81','soft81']], 'Same business basket with color allowance; not an equivalent 80-column color quotation.')
bench('art128',[None,None,4200,4000],[[],[],['h78','wc80'],['ii81','ram81']], 'Estimated expanded business workstation basket. No contemporaneous equivalent for ERA/MMU/multitasking. 1980 uses older Horizon baseline plus contemporary expansion allowance; 1981 Model II plus memory allowance.')
bench('art256',[None,None,5400,5200],[[],[],['h78','r78'],['ii81','ram81']], 'Capacity-normalized business workstation estimate, not an observed 256K machine price; obsolete 1978 RAM price is not carried forward as a current quote.')
bench('art128color',[None,None,4490,4220],[[],[],['color80'],['ii81','color81']], 'Business workstation proxy plus color/display allowance; no exact equivalent.')
bench('art256color',[None,None,5690,5420],[[],[],['color80'],['ii81','color81']], 'Expanded workstation proxy plus color/display allowance; no exact equivalent.')
bench('pro512',[None,None,None,11000],[[],[],[],['ii81','server81','ram81']], 'Estimated multiuser-capable hardware basket: $3,499 business host + $3,750 5 MB storage + about $3,751 RAM/network/OS allowance. No measured equivalence.')
bench('pro1024',[None,None,None,15000],[[],[],[],['ii81','server81','ram81']], 'PRO512 comparator plus $4,000 estimated extra memory/integration allowance; no exact 1 MiB quotation.')
bench('keyboard',[140,150,160,170],[[],[],[],[]], 'No comparable finished standalone keyboard quote established. Planning price envelope, not a verified market discount.', 'unverified_proxy')
for key,vals,refs,desc in [
 ('mono1',[180,169,169,155],[['t78'],['m79'],['m80'],['m81']],'1978 standalone display price estimated; later observed Sanyo prices. Logix custom interface differs.'),
 ('mono2',[None,None,139,129],[[],[],['m12_80'],['m12_81']],'Low-cost 12-inch monochrome displays; exact bandwidth/connector equivalence unproven.'),
 ('color1',[450,450,429,349],[['t78'],['m79'],['color80'],['color81']],'1978/79 color monitor amounts estimated; 1980/81 observed Zenith color price.'),
 ('color2',[None,None,429,349],[[],[],['color80'],['color81']],'Color display category comparison; Logix resolution and interface differ.'),
 ('ram16',[459,295,200,169],[['r78'],['board79'],['r78'],['card81']],'Complete memory boards, not bare chip sets. 1980 $200 is an estimate.'),
 ('printer',[600,600,495,420],[['p78'],['p78'],['p80'],['p81']],'1979 holds 1978 anchor as estimate. Printer speed/quality differs; 1978 is an upper-bound advertised price.'),
 ('disk',[528,495,440,314],[['disk78'],['d79'],['d80'],['disk81']],'1978 drive plus $39 cabinet + $39 PSU; 1979/80 second Apple drive; 1981 CCI lower-capacity drive. No universal protocol equivalence.'),
 ('disk2',[None,595,495,529],[[],['d79'],['d80'],['d81']],'Apple Disk II/controller retail anchor; Logix drive capacity/interface differs.'),
 ('applecard',[None,225,190,175],[[],['comm79'],['comm80'],['comm80']],'Apple communication-card category proxy; 1981 price estimated. Not a FlexiBUS bridge equivalent.'),
 ('compat',[None,None,549,438],[[],[],['soft80'],['soft81','card81']],'SoftCard plus estimated/observed memory allowance; Artemis module includes 64K dedicated RAM, so comparison remains weak.'),
 ('ram64',[None,None,695,599],[[],[],['ram80'],['ram81']],'1980 CCS 64K board $695 in BYTE PDF p223; 1981 $599. Different bus and memory organization.'),
 ('ram256',[None,None,2780,2396],[[],[],['ram80'],['ram81']],'Four times 64K board price: capacity-normalized estimate, not one advertised 256K kit.'),
 ('net',[None,None,None,None],[[],[],[],['server81']],'Corvus networking ecosystem establishes category, but no verified equivalent adapter/hub quote by cutoff. Cost-based price; no discount claim.'),
 ('tools',[150,150,100,100],[['gl78'],['ep79'],['v80'],['v81']],'Estimated utility/editor bundle value. Full word processors overstate Business Tools capabilities.'),
 ('abacus1',[100,100,122,120],[['gl78'],['ep79'],['v80'],['v81']],'1978/June1979 lack a verified shipping spreadsheet equivalent; $100 planning proxy. VisiCalc anchors only from 1980.'),
 ('abacus2',[None,None,122,120],[[],[],['v80'],['v81']],'VisiCalc spreadsheet proxy; not identical capacity/reporting.'),
 ('abacus3',[None,None,None,200],[[],[],[],['v81']],'VisiCalc $120 plus $80 estimated advanced-reporting value; no exact advanced-suite quote.'),
 ('pulse',[None,None,200,200],[[],[],['wc80'],['v81']],'Estimated interactive-language environment value; not a historical Pulse equivalent.'),
 ('pulse3',[None,None,None,300],[[],[],[],['v81']],'Estimated richer environment value; no matched market price.'),
 ('simplec',[100,125,125,125],[['gl78'],['basic79'],['c80'],['c80']],'1978/79 estimates; BDS C $125 observed 1980, held as 1981 estimate.'),
 ('ide',[None,None,500,500],[[],[],['wc80'],['wc80']],'Whitesmiths C starting price; native/cross IDE capabilities differ, 1981 holdover estimate.'),
 ('sdk',[100,100,100,100],[['t78'],['basic79'],['wc80'],['wc80']],'Documentation/tool package planning value; no matching SDK quote.',),
 ('sdkera',[None,None,150,150],[[],[],['wc80'],['wc80']],'Estimated SDK/documentation value, not measured competitor discount.'),
 ('basic',[None,300,325,325],[[],['basic79'],['basic79'],['basic79']],'Microsoft BASIC-80 $300 1979, $325 BYTE June1980 PDF106; 1981 carry-forward estimate.'),
 ('account',[195,195,95,195],[['gl78'],['basic79'],['bpi80'],['acct81']],'1978/79 $195 conservative category estimates; 1980 lower-price Osborne $95; 1981 CP/M application $195. Runtime dependencies differ.'),
 ('support',[None,None,None,195],[[],[],[],['support81']],'Apple hardware warranty is only a spending reference. No equivalent telephone-support quote; cost-based recommendation.'),
 ('training',[395,395,395,395],[['course']]*4,'Older four-day engineering course reference only. Course-day normalized price is an estimate, not office-course equivalence.'),
 ('registration',[None]*4,[[]]*4,'No equivalent developer registration quote established. Cost-based access price including SDK.')]: bench(key,vals,refs,desc,'unverified_proxy' if key in ['tools','pulse','pulse3','sdk','sdkera','support','registration','training'] else 'category_proxy')
for id in ['bundle.aurelia_mono','bundle.aurelia_color','bundle.aurelia_plus_mono','bundle.aurelia_plus_color','bundle.artemis_128_mono','bundle.artemis_128_color','bundle.artemis_256_mono','bundle.artemis_256_color','bundle.artemis_pro_512_server','bundle.artemis_pro_1mb_server']:
 b=['aurelia','color','plus','pluscolor','art128','art128color','art256','art256color','pro512','pro1024'][len(P)];add(id,group='Complete computer systems',bench=b)
for id in ['bundle.aurelia_network_upgrade','bundle.artemis_network_upgrade']:add(id,group='Networking',bench='net')
for id,b in [('flexibus_keyboard','keyboard'),('mono_monitor_1','mono1'),('color_monitor_1','color1'),('mono_monitor_2','mono2'),('color_monitor_2','color2'),('aurelia_ram_16kb_card','ram16'),('flexiprint40','printer'),('flexidisk','disk'),('apple2_expansion_card','applecard'),('flexidisk_ii','disk2'),('artemis_cpm80_module','compat'),('artemis_ram_64kb_bank_kit','ram64'),('artemis_ram_256kb_bank_kit','ram256')]:add('device.'+id,group='Peripherals and expansion',bench=b)
for id in ['s100_flexibus_card','apple2_video_card','s100_video_card']:
 add('device.'+id,group='Peripherals and expansion',note='NCC June 1979 offer. Cost-based planning price; no matched historical competitor benchmark. Host, monitor and any separate FlexiBUS card are excluded. Uses AION chips at launch; SMC sourcing remains an alternative scenario.')
for n in [4,8,16]:add('device.network_hub.'+str(n)+'_port',group='Networking',bench='net')
for id,b in [('business_tools_aurelia','tools'),('abacus_1','abacus1'),('simple_c_z80','simplec'),('aurelia_sdk','sdk'),('microsoft_basic_aurelia','basic'),('pulse_1','pulse'),('abacus_2','abacus2'),('business_tools_artemis','tools'),('aion_c_ide','ide'),('artemis_sdk','sdkera'),('abacus_3','abacus3'),('pulse_3','pulse3')]:add('software.'+id,group='Software and developer tools',bench=b)
add('edition.abacus_2.era',name='Abacus 2.0 — Artemis edition',group='Software and developer tools',bench='abacus2',note='Separate selectable platform SKU; do not sum with the Z80 edition for one purchase.')
for p in costs['products']:
 if p['id'].startswith('software.bpi_suite.'):add(p['id'],group='Business applications',bench='account',note='Z80 at launch; native Artemis edition from 1980-05-19. Same price per platform license.')
add('software.bpi_suite',name='BPI complete five-application bundle',group='Business applications',bench='account',note='One five-application license and consolidated media/documentation; cost uses existing suite estimate, not five separately packaged copies.')
add('software.bpi_client_server',name='BPI client-server — server package',group='Business applications',bench='net',note='Proposed one-server entitlement, all five business modules; clients sold separately. Existing media/delivery cost proxy, not software development.')
add('offer.bpi_client',name='BPI client-server — additional client',group='Business applications',bench='net',start='1981-05-04',parts=[{'cost_ref':'edition.bpi_client_server.era_client','quantity':1}],unit='one client entitlement, Z80 or ERA',note='Same conservative $38.39 full-pack cost proxy per client; no unsupported royalty split assumed.')
for id in ['customer_care','regular_support','professional_support','professional_business_onsite']:
 add('service.'+id,group='Support',bench='support',direct=True,note='Direct-service channel assumed; ComputerLand commission 0%. No repair parts included in modeled delivery workload.')
for n in range(1,5):
 add('service.academy_regular_courses.course_'+str(n),group='Training',bench='training',direct=True,note='Regular-course price; before-you-buy variant +$50. Fundamentals receives 50% tuition purchase credit; other courses retain their $150 voucher. Voucher remains promotional spend, excluded from manufacturing cost; exposure shown separately.')
add('service.academy_customer_site',group='Training',bench='training',direct=True,unit='one two-day class for up to 8 learners; travel extra at cost',parts=[{'cost_ref':'service.academy_customer_site','quantity':8}],note='Commercial unit reconciled from cost model per-learner estimate ×8. Two days assumed; minimum class charge protects low attendance.')
for id in ['bpi_training','pulse_training']:add('service.'+id,group='Training',bench='training',direct=True,note='Modeled course duration: BPI 3 days; Pulse 2 days. These durations are commercial assumptions, not original catalog terms.')
for id in ['aurelia_commercial_developer_license','artemis_commercial_developer_license']:add('service.'+id,group='Developer programs',bench='registration',direct=True,note='One registration including SDK; no duplicate SDK charge.')
# New manufacturer kit and optional services; cost-based, no asserted competitor discount.
for id in ['software.aurelia_compatibility_kit','service.aurelia_compatibility_support','service.aurelia_compatibility_certification']:
 add(id,group='Developer programs',direct=True,note='COMDEX 1979 manufacturer programme; optional support/certification, no per-machine runtime royalty. Cost-based annual planning price; launch and extra-work quotations are separate. Development/NRE excluded.')
# Approved use-case bundles, both generations, use exact component references.
for b in catalog['proposed_bundles']:
 add(b['id'],b['name'],'Application bundles',start=b['earliest_offer_date'],parts=[{'cost_ref':r,'quantity':1} for r in [b['base_bundle_ref']]+b['included_software']+b['included_devices']],note='Approved commercial bundle. Base system includes one year Regular Support; no second support charge.')
def package(id,name,base,software,devices=[],start='1980-05-19',note=''):
 return add('bundle.proposed_artemis_'+id,'Artemis — '+name,'Application bundles',start=start,parts=[{'cost_ref':r,'quantity':1} for r in [base]+software+devices],note=note or 'Approved commercial package; RAM selection is not a measured software minimum.')
office=package('office','Office productivity','bundle.artemis_128_mono',['software.business_tools_artemis','edition.abacus_2.era'])
office['component_variants']=[{'effective_from':'1980-11-19','replace':{'edition.abacus_2.era':'software.abacus_3'}}]
package('accounts','Small-business accounting','bundle.artemis_256_mono',['software.business_tools_artemis','software.bpi_suite'],['device.flexiprint40'])
package('developer','C development','bundle.artemis_256_mono',['software.business_tools_artemis','software.aion_c_ide','software.artemis_sdk'])
package('analysis','Interactive analysis','bundle.artemis_256_color',['software.business_tools_artemis','software.abacus_3','software.pulse_3'],start='1980-11-19')
mig=package('migration','CP/M migration','bundle.artemis_256_mono',['software.business_tools_artemis','edition.abacus_2.era','software.cpm_aurelia'],['device.artemis_cpm80_module'],note='Adds one CP/M software pack conservatively; no second keyboard/monitor or onboard module RAM charge.')
mig['component_variants']=office['component_variants']
package('network_workstation','Network business workstation','bundle.artemis_256_mono',['software.business_tools_artemis','offer.bpi_client'],start='1981-05-04',note='Base 1981 system already includes NIC and AIONix Server. Requires separately purchased compatible BPI server; no standalone operation promised.')
add('bundle.proposed_artemis_pro_small_office','Artemis PRO — Small-office business network','Network installation bundles',start='1981-05-04',announced=True,parts=[{'cost_ref':r,'quantity':n} for r,n in [('bundle.artemis_pro_512_server',1),('bundle.artemis_128_mono',2),('device.network_hub.4_port',1),('software.bpi_client_server',1),('offer.bpi_client',2),('software.business_tools_artemis',2),('device.flexiprint40',1),('assumption.network_cables',3)]],note='One 512K/5MB server, two 128K monochrome workstations, four-port hub, three cables, BPI server + two clients, two Office Suite copies and one printer. Installation/training/backup media excluded and separately quoted. PRO shipment unconfirmed.')
# Deliberately explicit non-source cost addition, separate from engineering BOM.
extra={'assumption.network_cables':{'name':'Finished network cable, allowance','cost_usd':15,'low_usd':10,'high_usd':25,'rationale':'Unspecified cable length/connectors: $15 recurring delivered cost per connection; revise after interface is finalized.'}}

def round_price(v):
 step=5 if v<100 else 10
 return int(math.ceil((v+1)/step)*step-1)
def components(p,date):
 ps=[dict(x) for x in p['components']]
 for v in p.get('component_variants',[]):
  if date>=v['effective_from']:
   for x in ps:x['cost_ref']=v['replace'].get(x['cost_ref'],x['cost_ref'])
 return ps

def cost(p,y):
 total=lo=hi=0;breakdown={};out=[]
 for x in components(p,f'{y}-06-15'):
  ref=x['cost_ref'];q=x['quantity']
  if ref in C:
   s=C[ref]['snapshots'][str(y)];assert s['total_usd'] is not None,(p['id'],ref,y)
   c,l,h=s['total_usd'],s['low_usd'],s['high_usd'];bd=s['breakdown_usd']
  elif ref in extra:
   e=extra[ref];c,l,h=e['cost_usd'],e['low_usd'],e['high_usd'];bd={'logistics':c}
  else:
   ss=byid[ref]['snapshots'][str(y)];c,l,h=ss['manufacturing_cost_usd'],ss['cost_low_usd'],ss['cost_high_usd'];bd=ss['cost_breakdown_usd']
  total+=q*c;lo+=q*l;hi+=q*h
  for k,v in bd.items():breakdown[k]=breakdown.get(k,0)+q*v
  out.append({'cost_ref':ref,'quantity':q,'unit_cost_usd':c,'extended_cost_usd':round(q*c,2)})
 return round(total,2),round(lo,2),round(hi,2),{k:round(v,2) for k,v in breakdown.items()},out

def assess(p,y):
 date=f'{y}-06-15';idx=y-1978
 if date<p['offering_start']:return {'date':date,'status':'not_yet_available','retail_price_usd':None,'manufacturing_cost_usd':None}
 c,lo,hi,bd,parts=cost(p,y);fee=p['computerland_fee_rate'];worst=.30 if fee else 0
 floor=c/((1-worst)*.75)
 benchmark=None;refids=[];kind='cost_based';desc='No matching contemporaneous price; recommendation uses delivery-cost floor.'
 b=B.get(p['benchmark_key'])
 if b:
  benchmark=b['values'][idx];refids=b['refs'][idx];kind=b['kind'];desc=b['description']
  if p['id']=='software.bpi_suite' and benchmark:benchmark*=5;desc+=' Five modules summed; not a quoted suite price.'
  if p['type']=='Training':
   days=C.get(p['id'],{}).get('course_days',2)
   if p['id']=='service.academy_customer_site':days=2
   benchmark=395/4*days*(8 if p['id']=='service.academy_customer_site' else 1)
   desc+=' Daily normalization uses $98.75/student-day; customer-site assumes eight learners.'
  if p['type']=='Support':benchmark=None;kind='cost_based';desc+=' Benchmark withheld as non-equivalent.'
 # Bundle benchmark and component-price ceiling are separate, traceable calculations.
 separate=0;hasprices=True;benchsum=0;hasbench=True
 for x in parts:
  ref=x['cost_ref'];q=x['quantity'];child=byid.get(ref)
  if child and child is not p:
   s=child['snapshots'].get(str(y),{});v=s.get('retail_price_usd');bv=s.get('competitor',{}).get('normalized_price_usd')
   if v is None:hasprices=False
   else:separate+=q*v
   if bv is None:hasbench=False
   else:benchsum+=q*bv;refids+=s.get('competitor',{}).get('evidence_refs',[])
  elif ref in extra:separate+=q*round_price(extra[ref]['cost_usd']/ .525);hasbench=False
  else:hasprices=False;hasbench=False
 if p['type'] in ['Application bundles','Network installation bundles']:
  kind='composite_proxy';desc='Sum of constituent competitor estimates; not a historical offered bundle. Missing comparator components prevent an aggregate discount claim.'
  benchmark=round(benchsum,2) if hasbench else None
 candidate=benchmark*.75 if benchmark else floor
 if hasprices:candidate=min(candidate,separate*.95) if benchmark else separate*.95
 # Explicit service price choices maintain affordable access, existing annual tiers as anchors.
 if p['type']=='Support':
  anchors={'service.customer_care':[49]*4,'service.regular_support':[99,99,129,139],'service.professional_support':[179,189,209,229],'service.professional_business_onsite':[0,0,449,499]}
  candidate=anchors[p['id']][idx]
 # Unknown standalone network prices use cost floor, never invent discount evidence.
 price=round_price(max(floor,candidate));prior=p['snapshots'].get(str(y-1),{}).get('retail_price_usd')
 if prior and price>prior and floor<=prior:price=prior
 price=max(price,round_price(floor))
 revenue=round(price*(1-fee),2);profit=round(revenue-c,2)
 gap=round((1-price/benchmark)*100,2) if benchmark else None
 warnings=[]
 if benchmark and price>.8*benchmark:warnings.append('Cannot reach 20% below this benchmark while respecting the cost floor.')
 if kind in ['unverified_proxy','normalized_proxy','composite_proxy','cost_based']:warnings.append('Estimated or unmatched comparator; discount is indicative, not verified like-for-like.')
 if round(price*.9*(1-worst)-hi,2)<0:warnings.append('High cost scenario plus markdown loses money; oversupply protection is not guaranteed.')
 if hasprices and price>separate:warnings.append('Bundle cost floor exceeds separately priced components; review configuration before launch.')
 status='announced_shipping_unconfirmed' if p['announced_only'] else 'available_proposal'
 s={'date':date,'status':status,'retail_price_usd':price,'manufacturing_cost_usd':c,'cost_low_usd':lo,'cost_high_usd':hi,'cost_breakdown_usd':bd,'cost_components':parts,'computerland_fee_rate':fee,'computerland_fee_usd':round(price*fee,2),'revenue_after_fee_usd':revenue,'unit_profit_usd':profit,'contribution_margin_on_net_revenue_pct':round(profit/revenue*100,2),'price_floor_usd':round(floor,2),'competitor':{'normalized_price_usd':benchmark,'evidence_refs':sorted(set(refids)),'assessment_type':kind,'assessment':desc,'discount_pct':gap,'discount_claim':'indicative' if benchmark else 'not_claimed'},'separate_purchase_price_usd':round(separate,2) if hasprices else None,'stress':{'fee_rate':worst,'markdown_pct':10,'cost_increase_pct':20,'profit_usd':round(price*.9*(1-worst)-c*1.2,2),'high_cost_profit_usd':round(price*.9*(1-worst)-hi,2)},'warnings':warnings}
 if p['type']=='Training' and 'regular_courses.course_' in p['id']:
  fundamentals=p['id'].endswith('.course_1')
  credit=round((price+50)*.5,2) if fundamentals else 150
  s['before_you_buy_variant']={'retail_price_usd':price+50,'voucher_face_value_usd':credit,'voucher_basis':'50% of Fundamentals tuition' if fundamentals else 'Existing fixed voucher for other courses','voucher_redemption_assumed_pct':100,'maximum_incremental_promotion_cost_usd':credit,'contribution_after_full_voucher_usd':round(price+50-c-credit,2),'note':'Fundamentals credit valid six months toward one Aurelia via Academy or participating dealers reimbursed by Logix; no purchase obligation. Other course terms unchanged. Reserve marketing expense once across course and computer sale.'}
 return s
# Dependency order: all standalone offers precede composite bundles.
for p in P:
 for y in YEARS:p['snapshots'][str(y)]=assess(p,y)
 p.pop('benchmark_key')
# Group consistently without affecting dependencies.
groups=['Complete computer systems','Application bundles','Network installation bundles','Peripherals and expansion','Networking','Software and developer tools','Business applications','Support','Training','Developer programs']
P.sort(key=lambda p:groups.index(p['type']))
model={'metadata':{'title':'Logix / AION retail pricing assessment','schema_version':'1.0','currency':'USD','price_basis':'Nominal US retail prices before sales tax; June 15 snapshots, 1978–1981','source_commit':'47177a6a75b07f0c2a9a00aedf2a30a9793cb1de','cost_model_file':'manufacturing_costs.json','cost_model_sha256':hashlib.sha256((ROOT/'manufacturing_costs.json').read_bytes()).hexdigest(),'snapshots':[f'{y}-06-15' for y in YEARS],'status':'Recommended pricing scenario; does not overwrite historical catalog price fields'},'policy':{'target_discount_pct':25,'acceptable_discount_band_pct':[20,30],'default_computerland_fee_pct':25,'catalog_fee_range_pct':[20,30],'fee_basis':'Percent of retail selling price; assumption interpreting catalog retailer-margin term. Hardware/software via ComputerLand; services direct with zero fee. Service channel is a proposal.','minimum_margin_on_net_revenue_at_max_fee_pct':25,'rounding':'Round upward to $4/$9 endings below $100; $9 endings above. Prevent annual increases unless required by cost floor.','formula':'fee=retail*rate; revenue=retail-fee; profit=revenue-recurring_cost; retail_floor=cost/((1-max_fee)*0.75)','profit_definition':'Unit contribution, not net corporate profit. Excludes R&D, capital/depreciation, marketing/vouchers, software development, tax and finance. Costs include modeled logistics and service delivery.','risk':'25% net margin at 30% fee approximately covers simultaneous 10% retail markdown and 20% cost overrun. It does not cover unsold stock, actual warranty failures or the entire original high-cost envelope.','availability':'No documented withdrawal dates: offering_end=null. Announced PRO products retain provisional prices, excluded from available-only filters. No 1979 June prices for December Aurelia+; no 1980 June prices for November Abacus/Pulse 3.','benchmark_policy':'Primary period advertisements; itemized baskets and judgment adjustments labeled estimates. No later IBM PC, 1982 networks or later warranty prices used retroactively. Observed mail-order prices are included as competitive pressure. No exact benchmark means no substantiated discount claim.','bundle_policy':'Base-system costs already include keyboard, display, OS and one-year support. 1981 Artemis includes NIC and Server edition automatically. BPI suite and developer registration already include their respective contents. Composite rows are alternative purchase units, not additive sales totals.','service_scope':'On-site support is a proposed capped eight-hour engagement with modeled travel, not unlimited annual repairs. Training prices assume eight learners; customer-site sold as class ×8 with travel extra. BPI/Pulse course durations remain model assumptions.'},'sources':sources,'competitor_evidence':E,'additional_cost_assumptions':extra,'types':groups,'products':P,'excluded':['OEM chips and licensing','Bare computer chassis and internal assemblies','Standalone NICs replaced by complete network upgrade offerings','Bundled operating systems','Prototype/superseded RAM','Duplicate platform editions except separately selectable Abacus 2 platform SKUs','Academy direct-sales channel record']}
# Balance contribution/net revenue against the discount to the dated proxy.
# Frozen baselines remain audit/demand anchors; no compounded price reductions.
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
def cents(value):return float(Decimal(str(value)).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP))
def ceil_cents(value):return float(Decimal(str(value)).quantize(Decimal('0.01'),rounding=ROUND_CEILING))
baseline=load('pricing_baseline.json');oem_path=ROOT/'compatibility_pricing_baseline.json'
oem_baseline=load('compatibility_pricing_baseline.json')
assert not set(baseline['products']) & set(oem_baseline['products'])
baseline['products'].update(oem_baseline['products'])
model['metadata']['compatibility_baseline_sha256']=hashlib.sha256(oem_path.read_bytes()).hexdigest()
FALLBACK_MARGIN=.25

def balanced_price(cost,fee,benchmark,credit_rate=0,fixed_credit=0):
 # Effective contribution = P*(1-fee-credit_rate)-cost-fixed_credit.
 effective_cost=cost+fixed_credit
 floor=effective_cost/(1-fee-credit_rate)
 if benchmark:
  # Equate effective contribution / net revenue to 1-P/benchmark.
  k=credit_rate*benchmark/(1-fee)
  ideal=(k+math.sqrt(k*k+4*effective_cost*benchmark/(1-fee)))/2
  status='balanced_proxy' if floor<=benchmark else 'cost_floor_above_proxy'
 else:
  ideal=effective_cost/((1-fee)*(1-FALLBACK_MARGIN)-credit_rate)
  status='no_proxy_cost_based'
 price=max(cents(ideal),ceil_cents(floor))
 # Choose the adjacent cent with the smallest displayed percentage gap.
 if status=='balanced_proxy':
  def gap(p):
   net=cents(p-cents(p*fee));credit=cents(p*credit_rate+fixed_credit)
   return abs((net-cost-credit)/net-(1-p/benchmark))
  price=min([v for v in [cents(price-.01),price,cents(price+.01)] if v+1e-9>=floor],key=gap)
 return price,status

for offer in P:
 for year,s in offer['snapshots'].items():
  if s['retail_price_usd'] is None:continue
  old=baseline['products'][offer['id']][year]
  cost=s['manufacturing_cost_usd'];fee=s['computerland_fee_rate'];benchmark=s['competitor']['normalized_price_usd']
  assert fee==old['computerland_fee_rate']
  s['cost_revision']={'reason':'Current accepted hardware and delivery costs; frozen original costs retained for audit.', 'baseline_manufacturing_cost_usd':old['manufacturing_cost_usd'], 'current_manufacturing_cost_usd':cost, 'delta_usd':cents(cost-old['manufacturing_cost_usd'])}
  price,status=balanced_price(cost,fee,benchmark)
  commission=cents(price*fee);revenue=cents(price-commission);profit=cents(revenue-cost)
  margin=cents(profit/revenue*100);discount=cents((1-price/benchmark)*100) if benchmark else None
  s['pre_reduction']={**old,'retail_reduction_pct':cents((1-price/old['retail_price_usd'])*100),'basis':'Frozen original audit and sales-demand anchor; old 40% contribution policy superseded.'}
  s.update(retail_price_usd=price,computerland_fee_usd=commission,revenue_after_fee_usd=revenue,unit_profit_usd=profit,contribution_margin_on_net_revenue_pct=margin,legacy_price_floor_usd=s['price_floor_usd'],price_floor_usd=ceil_cents(cost/(1-fee)))
  s['competitor']['discount_pct']=discount
  s['pricing_balance']={'status':status,'margin_pct':margin,'discount_pct':discount,'gap_percentage_points':cents(abs(margin-discount)) if discount is not None else None,'fallback_margin_pct':25 if benchmark is None else None}
  stress=s['stress'];stress['profit_usd']=cents(price*.9*(1-stress['fee_rate'])-cost*1.2);stress['high_cost_profit_usd']=cents(price*.9*(1-stress['fee_rate'])-s['cost_high_usd'])
  s['warnings']=[w for w in s['warnings'] if not w.startswith(('Cannot','High cost','Bundle cost'))]
  if status=='cost_floor_above_proxy':s['warnings'].append('Cannot balance nonnegative contribution with a discount: central-cost break-even exceeds the proxy. Price held at break-even; negative discount shown as a premium.')
  if status=='no_proxy_cost_based':s['warnings'].append('No matched proxy: use a 25% contribution margin on net revenue; no discount percentage is invented.')
  if stress['profit_usd']<0:s['warnings'].append('Markdown plus higher costs and maximum channel fee loses money; balanced pricing is not a stress-profit guarantee.')
  if stress['high_cost_profit_usd']<0:s['warnings'].append('High cost scenario plus markdown loses money.')
  if 'before_you_buy_variant' in s:
   v=s['before_you_buy_variant'];fundamentals=offer['id'].endswith('.course_1')
   tuition,vstatus=balanced_price(cost,0,benchmark,credit_rate=.5 if fundamentals else 0,fixed_credit=0 if fundamentals else 150)
   credit=cents(tuition*.5) if fundamentals else 150
   contribution=cents(tuition-cost-credit)
   v.update(retail_price_usd=tuition,voucher_face_value_usd=credit,maximum_incremental_promotion_cost_usd=credit,contribution_after_full_voucher_usd=contribution)
   v['pricing_balance']={'status':vstatus,'margin_after_full_voucher_pct':cents(contribution/tuition*100),'discount_pct':cents((1-tuition/benchmark)*100) if benchmark else None}
   v['note']='Tuition balances contribution after full voucher redemption against the same course proxy. Credit is reserved once as promotional expense, not manufacturing cost. Half-tuition Fundamentals credit / fixed $150 other-course credit retained; no additional fixed surcharge.'
   if vstatus=='cost_floor_above_proxy':s['warnings'].append('Course variant cannot balance below the proxy after reserving its voucher; priced at voucher-inclusive break-even.')
 for i,note in enumerate(offer['notes']):
  offer['notes'][i]=note.replace('variant +$50','variant priced separately including full voucher provision')
# Reconcile displayed separate-purchase comparisons against revised component prices.
for offer in P:
 for year,s in offer['snapshots'].items():
  if s['retail_price_usd'] is None or s['separate_purchase_price_usd'] is None:continue
  total=0
  for component in s['cost_components']:
   ref=component['cost_ref'];q=component['quantity']
   if ref in byid:total+=q*byid[ref]['snapshots'][year]['retail_price_usd']
   else:total+=q*round_price(extra[ref]['cost_usd']/.525)
  s['separate_purchase_price_usd']=cents(total)
  if s['retail_price_usd']>total:s['warnings'].append('Bundle price exceeds revised separate components; compare both purchase routes.')
model['metadata'].update(schema_version='1.2',source_commit=baseline['metadata']['source_commit'],baseline_file='pricing_baseline.json',baseline_sha256=hashlib.sha256((ROOT/'pricing_baseline.json').read_bytes()).hexdigest())
model['policy'].update(target_discount_pct=None,acceptable_discount_band_pct=None,minimum_margin_on_net_revenue_at_max_fee_pct=None,rounding='Nearest cent; adjacent-cent check minimizes the percentage gap. Nonnegative central contribution takes precedence.',formula='For proxy B, cost C and fee f: P=sqrt(C*B/(1-f)); contribution/net=1-C/(P*(1-f)) equals proxy discount=1-P/B. If C/(1-f)>B use break-even. Without a proxy use C/((1-f)*0.75).',risk='Stress losses remain visible. Equality is calibrated to central costs and baseline fees; interactive fee/cost scenarios retain prices and may diverge.',baseline='Frozen original baselines retained only for audit and demand anchoring. The former 40% contribution-reduction policy is superseded; each rebuild uses current costs and unchanged dated proxies.',scope='All priced offers and annual snapshots. Promotional course variants balance after full voucher provision; partner baskets remain component sums.',price_floor='Central-cost break-even at baseline fee.',fallback_margin_on_net_revenue_pct=25,matching_tolerance_percentage_points=.1,course_variant='Balance contribution after full voucher redemption against the course proxy. Fundamentals credit remains 50% of tuition; other regular-course credit $150. Reserve redemption once in marketing.',bundle_balance='Each offered bundle uses its own proxy and costs. Exact percentage matching can exceed separate component prices; both routes are disclosed, with no invented discount cap.')

# Independent partner baskets are component sums, outside the immutable SKU baseline.
bp={'business_accounts':['software.bpi_suite.bpi_general_accounting'],
    'trading_office':['software.bpi_suite.bpi_general_accounting','software.bpi_suite.bpi_accounts_receivable','software.bpi_suite.bpi_accounts_payable','software.bpi_suite.bpi_inventory_control'],
    'complete_business':['software.bpi_suite']}
by_id={x['id']:x for x in P}
model['partner_configurations']=[]
for key,licenses in bp.items():
 refs=['bundle.proposed_aurelia_office','device.flexidisk','device.flexiprint40']+licenses
 row={'id':'bpi_'+key,'name':'Aurelia '+key.replace('_',' ').title()+' — dealer configuration','supplier_policy':'Logix hardware, AION applications and independently licensed BPI Systems software. Component basket, not an additional SKU.','components':refs,'snapshots':{}}
 for year in YEARS:
  ss=[by_id[r]['snapshots'][str(year)] for r in refs]
  row['snapshots'][str(year)]={k:cents(sum(x[k] for x in ss)) for k in ['retail_price_usd','manufacturing_cost_usd','computerland_fee_usd','revenue_after_fee_usd','unit_profit_usd']} if all(x['retail_price_usd'] is not None for x in ss) else {'retail_price_usd':None}
 model['partner_configurations'].append(row)
model['policy']['independent_bpi']='BPI Systems owns and supports its applications independently. BPI receipts belong to BPI; baskets combine suppliers and do not imply Logix revenue or ownership. Training, setup, support contracts, upgrade-credit redemptions and tax excluded; quote separately. No new discount applied.'
model['policy']['bpi_upgrade_credit']='Eligible same-platform module net licence payments credited once toward complete suite, capped at suite price, with credited licences retired; no cash refund or training/setup credit. Redemption costs must be modelled if upgrades are forecast.'
for product in P:
 if product['id'].startswith('software.bpi') or product['id']=='offer.bpi_client':
  product['notes'].append('Independent BPI Systems software: separately licensed, BPI-owned and supported. Displayed receipts/contribution are BPI estimates, not Logix income; specialist support and development budgets excluded.')

(ROOT/'pricing_results.json').write_text(json.dumps(model,indent=2,ensure_ascii=False)+'\n')
print(f'{len(P)} products; '+str(sum(s['retail_price_usd'] is not None for p in P for s in p['snapshots'].values()))+' assessed snapshots')


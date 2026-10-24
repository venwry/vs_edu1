from data_store import read_document, document_bytes, document_text
"""Deterministic, assumption-based recurring unit cost model; run from any directory."""
from pathlib import Path
import json, math, copy, hashlib
from collections import defaultdict,Counter
from memory_manufacturing import policy as memory_policy, selected as memory_selected, evaluate as memory_evaluate
R=Path(__file__).resolve().parents[1]
C=read_document('generated/catalogs/logix-aion-technical-catalog-v2.json', root=R); B=read_document('generated/catalogs/hardware-bom.json', root=R)
records={x['id']:x for v in C.values() if isinstance(v,list) for x in v if isinstance(x,dict) and 'id' in x}
assemblies={x['id']:x for x in B['assemblies']}; components={x['id']:x for x in B['components'] if x['bom_role']=='material'}
pending=[a['id'] for a in assemblies.values() if a.get('cost_assessment_status')=='pending_reassessment']
if pending:raise ValueError('Cost rebuild blocked: qualify revised module routing/allowances and reassess before publishing: '+', '.join(pending))
years=[1978,1979,1980,1981,1982]; snapshots=[f'{y}-06-15' for y in years]
wages=[5.99,6.54,7.08,7.85,8.30]; electricity=[.028,.031,.037,.043,.047]; overhead=[1,1.09,1.2,1.32,1.43]
K=['bom_materials','workforce','energy','consumables','operating_overhead','yield_and_rework','instructions','packaging','logistics','recurring_licenses','included_service_delivery']
def vec():return dict.fromkeys(K,0.)
def add(a,b,n=1):
 for k in K:a[k]+=b.get(k,0)*n
 return a
# Explicit bought-in component price assumptions, nominal USD at each June snapshot.
prices={'part.z80a':[18,14,11,9],'part.z80b':[35,30,24,18],'part.dram_16kbit':[6,4.5,3.25,2.25],'part.dram_64kbit':[80,65,40,25], 'part.ball_tv90_crt':[45,44,43,42],'part.sony_kv1204_display_assembly':[130,126,122,118],'part.motorola_ds3000_140a_crt':[65,63,60,56],'part.medium_resolution_rgb_crt':[190,180,170,158],'part.mpi_mp40_mechanism':[120,115,110,105],'part.hdd_5mb':[1500,1400,1150,950]}
# Area is an engineering assumption; video RAM/video areas follow catalog planning ranges.
chip_area={'part.era1':55,'part.flexibus_host_controller':12,'part.flexibus_device_controller':10,'part.aurelia_video_chip':52,'part.aion_2114':20,'part.aurelia_system_controller':30,'part.aurelia_monitor_dac':6,'part.color_monitor_controller':14,'part.mono_monitor2_controller':9,'part.artemis_dma':18,'part.artemis_mmu':30,'part.artemis_graphics_chip':80,'part.mono_pro_controller':12,'part.artemis_fdd_hdd_controller':22,'part.aion_4116':18,'part.aion_4164':45}
prices['part.brimar_m36_141w_crt']=[95,92,90,85] # Bare tube, unquoted nominal planning purchase price.
# 1982 OEM estimates, not verified quotes; hardware BOM quantities unchanged.
for ref,value in {'part.z80a':8,'part.z80b':16,'part.dram_16kbit':1.75,'part.dram_64kbit':18,'part.ball_tv90_crt':41,'part.sony_kv1204_display_assembly':114,'part.motorola_ds3000_140a_crt':53,'part.medium_resolution_rgb_crt':150,'part.mpi_mp40_mechanism':100,'part.hdd_5mb':850,'part.brimar_m36_141w_crt':82}.items():prices[ref].append(value)
ncc=read_document('generated/catalogs/ncc-1982-inputs.json', root=R)
chip_area.update(ncc['custom_die_area_mm2'])
custom=set(chip_area)
# Functional-set allowances for the NCC 1979 cards; component-level selections remain unresolved.
card_allowances={'apple_expansion_pcb':5,'s100_expansion_pcb':8,'apple_host_interface':7,'s100_host_interface':10,'video_ram_window_and_bus_arbitration':8,'video_clock_reset':3,'digital_video_transceivers_and_connector':8,'flexibus_two_port_transceivers_connectors':8}
# All unresolved multi-part line items are priced as one functional set, not as one discrete part.
allowances={'module_pcb':3,'module_connector_contacts':2,'decoupling_and_bulk_capacitors':1,'data_buffers_and_byte_enable_logic':4,'capacity_identification_straps':.15,'key_switches':18,'keycaps':5,'matrix_diodes':1.5,'scan_controller_and_firmware_storage':4,'flexibus_interface_electronics':5,'keyboard_pcb':4,'keyboard_enclosure':6,'keyboard_cable':2,'passives_protection_and_internal_harnesses':4,'external_cable_and_regional_mains_packout':2,'video_receiver_and_sync_circuitry':5,'video_amplifier':4,'hv_deflection_and_psu_not_included_by_oem':0,'monitor_enclosure':12,'video_link_receiver':5,'rgb_dac_and_amplifiers_not_included_by_oem':12,'video_link_receiver_and_grayscale_amplifier':7,'video_receiver_and_rgb_amplifiers':13,'ram_card_pcb':4,'slot_connector_contacts':2,'mapper_decode_and_refresh_interface':4,'identification_storage_and_buffers':3,'motor_and_printhead_drivers_excluded_by_mechanism':12,'local_sequencer_firmware_font_rom_and_buffer_ram':14,'printer_psu':14,'printer_enclosure':15,'initial_ribbon':2,'525_inch_floppy_mechanism':100,'floppy_controller_and_data_separator':18,'local_firmware_processor_and_sector_ram':12,'drive_psu':12,'drive_enclosure':10,'apple_ii_card_pcb':5,'host_bus_decode_and_buffering':7,'boot_and_driver_rom':4,'disk_ii_sequencer_interface':8,'525_inch_dual_format_floppy_mechanism':115,'aurelia_and_apple_ii_format_controller':22,'local_refresh_controller':5,'boot_rom_or_host_upload_implementation':3,'mailbox_window_arbitration_and_doorbells':12,'bus_width_conversion_and_clock_reset':9,'compatibility_card_pcb':8,'network_card_pcb':7,'z80_host_interface':6,'network_controller_framing_crc_and_buffers':24,'firmware_rom':3,'differential_data_and_clock_transceivers':6,'network_port_connector':2,'32_bit_slot_interface_and_pio_dma_selection':12,'network_connector':2,'per_port_transceiver_termination_and_protection_assembly':8,'shared_arbiter_clock_and_firmware':30,'4_port_pcb':10,'4_port_psu':12,'4_port_enclosure':12,'8_port_pcb':14,'8_port_psu':16,'8_port_enclosure':16,'16_port_pcb':22,'16_port_psu':22,'16_port_enclosure':24,'kit_packout_and_instructions':0,'floppy_controller_data_separator_and_buffers':18,'mainboard_pcb':20,'psu':28,'enclosure_and_chassis':24,'boot_rom_chips':8,'clock_reset_interrupts_mapper_and_bus_buffers':18,'connectors_passives_fasteners_and_harnesses':18,'525_inch_single_density_floppy_mechanism':100,'525_inch_double_density_floppy_mechanism':125,'paired_bank_dram_controller_refresh_and_data_buffers':24,'cartridge_pcb_and_connector_if_cartridge_delivered':3,'cartridge_shell_label_and_instructions':2,'bundle_cables_media_manuals_and_carton_packout':0}
allowances.update(card_allowances)
allowances['economy_video_byte_bridge']=6.5 # 1978 allowance, learning to $5.85 in 1980; no second video ASIC
allowances.update({'artemis_video_card_pcb':12,'artemis_video_slot_connector':8,'artemis_video_host_interface':9,'artemis_video_clock_transceivers':10,'mono_pro_yoke':18,'mono_pro_hv_deflection_psu':45,'mono_pro_precision_ladder':3,'mono_pro_video_amplifier':10,'mono_pro_link_receiver':4,'mono_pro_pcb':8,'mono_pro_enclosure':18})
allowances.update({'sprite_interface_package_pcb_test':7.4,'system_controller_interface_pcb_test':11.5,'clock_reset_interrupts_and_bus_buffers':13})
inputs={}; chip_models={}
def chip_cost(ref,i):
 area=chip_area[ref];diameter=75;usable=.9*(math.pi*(diameter/2)**2/area-math.pi*diameter/math.sqrt(2*area));d=[2.8,2.4,2.,1.7,1.6][i];maturity=.72 if ref.startswith('part.artemis') or ref=='part.era1' else 1
 if i>=3 and maturity<1:maturity=.86
 if ref=='part.aion_4164':maturity=.85
 if ref in ncc['custom_die_area_mm2']:maturity=ncc['custom_maturity']
 memory_recipe=None
 if ref=='part.aion_4164' and i>=2:
  memory_recipe=memory_selected(years[i]);area=memory_recipe['die_area_mm2'];d=memory_recipe['defect_density_cm2']
  usable=.9*(math.pi*(diameter/2)**2/area-math.pi*diameter/math.sqrt(2*area))
  yield_die=memory_evaluate(memory_recipe)['die_yield']
 else:yield_die=max(.08,math.exp(-d*area/100)*.85*maturity)
 good=usable*yield_die
 wafer=[210,220,235,255,276][i];package=4 if ref=='part.artemis_graphics_chip' else 3 if ref=='part.aurelia_system_controller' else 2.5 if ref in ['part.era1','part.artemis_mmu'] else .65;test=1.3 if area>=30 else .35;py=.93
 if ref in ncc['package_usd']:package=ncc['package_usd'][ref]
 if memory_recipe:
  wafer=memory_policy()['wafer_cost_by_year'][str(years[i])][memory_recipe['node_um']]+memory_recipe.get('repair_cost_per_wafer_usd',0)
 v=vec();v['bom_materials']=(wafer*.18/good+package)/py;v['workforce']=(wafer*.36/good+test)/py;v['energy']=wafer*.10/good/py;v['consumables']=wafer*.24/good/py;v['operating_overhead']=wafer*.12/good/py
 chip_models.setdefault(ref,{})[str(years[i])]={'die_area_mm2':area,'wafer_diameter_mm':diameter,'gross_usable_dies':round(usable,2),'die_yield':round(yield_die,4),'packaging_test_yield':py,'recurring_processed_wafer_cost_usd':wafer,'package_usd':package,'test_labor_usd':test,'good_packaged_chip_cost_usd':round(sum(v.values()),4),'cost_status':'engineering scenario, not supplier quote or proven silicon yield'}
 model=chip_models[ref][str(years[i])]
 model['process_node_um']=float(memory_recipe['node_um']) if memory_recipe else 3.0
 if memory_recipe:model.update(memory_recipe=memory_recipe['id'],raw_die_yield=round(memory_evaluate(memory_recipe)['raw_die_yield'],4),repair_fraction_of_spatial_failures=memory_recipe.get('repair_fraction_of_spatial_failures',0),repair_cost_per_wafer_usd=memory_recipe.get('repair_cost_per_wafer_usd',0))
 return v
for cid,comp in components.items():
 ref=comp['id'];key=cid.split('.')[-1];costs=[];note='One functional set; allowance is a modeling assumption, not an exact released component list.'
 for i in range(len(years)):
  v=vec()
  if ref in custom:v=chip_cost(ref,i);note='Internal fabrication at recurring cash cost; wafer losses, packaging and final-test yield included. Capital and mask NRE excluded.'
  elif cid in ncc['purchased_components']:
   v['bom_materials']=ncc['purchased_components'][cid]['unit_cost_usd'];note=ncc['purchased_components'][cid]['basis']+' June 1982 allowance only; prelaunch cost rows are unavailable.'
  elif ref in prices:v['bom_materials']=prices[ref][i];note='Assumed OEM purchase price; supplier manufacturing overhead/profit remains embedded.'
  elif key=='local_64_kib_ram_implementation':v['bom_materials']=8*prices['part.dram_64kbit'][i];note='Assumes eight purchased 64Kx1 DRAMs for local 64 KiB.'
  elif key=='rom_eprom_eeprom_or_media_selection':
   v['bom_materials']=({'cpm_aurelia':6,'business_tools_aurelia':6,'aionix':18,'business_tools_artemis':12,'aionix_server':24,'cpm_aurelia_networking':10}[cid.split('.')[2]])*[1,.93,.86,.8,.76][i];note='Provisionally mask-ROM cartridge population; recurring mask replication included, original design/mask NRE excluded. EEPROM substitute would cost more.'
  else:
   if key not in allowances:raise ValueError('No cost assumption for '+cid)
   base=allowances[key];factor=[1,.96,.9,.85,.81][i] if key in ['sprite_interface_package_pcb_test','system_controller_interface_pcb_test'] or any(x in key for x in ['floppy','ram','rom','controller','logic','buffer','firmware','pcb']) else overhead[i]
   if '.computer.artemis' in cid and key in ['mainboard_pcb','psu','enclosure_and_chassis','connectors_passives_fasteners_and_harnesses']:base*=1.7
   if '.computer.artemis_pro' in cid and key in ['psu','enclosure_and_chassis']:base*=1.25
   if 'color_monitor' in cid and key=='monitor_enclosure':base*=1.5
   v['bom_materials']=base*factor
   if key=='clock_reset_interrupts_and_bus_buffers':note='Remaining clock/reset/interrupt/buffer set: 18 USD baseline less 5 USD replaced bank/decode logic in 1978, then annual learning. No second mapper charge.'
   if key.endswith('_interface_package_pcb_test') or key=='system_controller_interface_pcb_test':note='Incremental package/interface/PCB/assembly-test functional allowance, excludes silicon and baseline assembly routing; detailed released BOM pending.'
   if key=='hv_deflection_and_psu_not_included_by_oem':note='Zero additional charge assumes complete OEM CRT/chassis includes HV, deflection and PSU. Increase if purchasing bare tubes.'
   if key=='kit_packout_and_instructions' or key=='bundle_cables_media_manuals_and_carton_packout':note='Accounted once in final-product instructions/packaging/logistics; not repeated in recursive BOM.'
  costs.append({k:round(x,5) for k,x in v.items() if x})
 inputs[cid]={'name':comp['name'],'basis':note,'annual_cost_buckets_usd':dict(zip(map(str,years),costs)),'confidence':'low','price_range_multipliers':[.7,1.55] if ref not in custom else [.5,2.5]}
quantity_assumptions={}
def quantity(a,l):
 if l['quantity'] is not None:return l['quantity']
 q=3 if l['ref']=='part.flexibus_host_controller' and a.startswith(('assembly.computer.aurelia.','assembly.computer.aurelia_plus.')) else 2 if l['ref']=='part.flexibus_host_controller' and a in ['device.apple2_expansion_card','device.s100_flexibus_card'] else 1
 quantity_assumptions[a+'|'+l['ref']]={'quantity':q,'unit':'functional set' if l['ref'] not in [x for x in custom] else 'chip','reason':'One controller die per port, pending released ports-per-die definition.' if q in [2,3] else 'Unspecified engineering quantity replaced by one priced functional set (or one controller die); not a catalog amendment.'}
 return q
def routing(a):
 if a in ncc['routing']:
  x=ncc['routing'][a];return (x['hours'],x['kwh'],x['consumables_usd'])
 if a.startswith('assembly.part.'):
  return (.22, .6,.35) if 'module_' in a else (0,0,0)
 if a.startswith('assembly.computer.'):
  if a.endswith('.base'):return (3.5 if 'artemis' in a else 2.4,12 if 'artemis' in a else 7,2.5)
  return (.18,1,.15) # installation and verification, not another complete build
 if a.startswith('assembly.media.'):return (.08,.08,.08)
 if a.startswith('assembly.bundle.'):return (.2,.2,.25)
 if a.startswith(('device.','assembly.device.')):
  if 'mono_pro' in a:return (1.5,5,1.5)
  if 'artemis_video_card' in a:return (.6,1,.7)
  if 'monitor' in a:return (1.0,4,1)
  if 'print' in a:return (1.3,2,1.2)
  if 'disk' in a:return (.65,1,.6)
  if 'keyboard' in a:return (.75,.25,.4)
  if 'hub' in a:return (.75,1,.7)
  if 'bank_kit' in a:return (.08,.1,.08)
  return (.4,.5,.35)
 return (0,0,0)
assembly_inputs={a:{'assembly_hours_1978':routing(a)[0],'kwh_1978':routing(a)[1],'consumables_usd_1978':routing(a)[2],'operating_overhead_fraction_of_loaded_labor':.25,'rework_allowance_fraction_of_labor':.10,'incremental_material_scrap_rate':.015 if routing(a)[0] else 0} for a in assemblies}
def rollup(a,i,source_inputs=None):
 source_inputs=inputs if source_inputs is None else source_inputs
 v=vec();flat=Counter()
 for line in assemblies[a]['lines']:
  q=quantity(a,line);ref=line['ref']
  if ref in assemblies:
   child,leaves=rollup(ref,i,source_inputs);add(v,child,q);flat.update({k:n*q for k,n in leaves.items()})
  else:add(v,source_inputs[ref]['annual_cost_buckets_usd'][str(years[i])],q);flat[ref]+=q
 h,kwh,cons=routing(a);h*=1 if a in ncc['routing'] else 1-.05*i;labor=h*wages[i]*1.35
 v['workforce']+=labor;v['energy']+=kwh*electricity[i];v['consumables']+=cons*overhead[i];v['operating_overhead']+=labor*.25;v['yield_and_rework']+=labor*.10+sum(v[k] for k in ['bom_materials'])*(.015 if h else 0)
 return v,flat
rows=[]
def date(x):return x.get('introduced',{}).get('event_start_date','1978-06-05')
def row(id,ref,name,group,unit,start,**kwargs):
 d={'id':id,'catalog_ref':ref,'name':name,'group':group,'unit':unit,'available_from':start,'assumptions':[],'snapshots':{},**kwargs};rows.append(d);return d
# Hardware product rows use the canonical BOM configurations, retaining shipping uncertainty.
for x in C['computers']+C['devices']:
 if x.get('superseded_by'):continue
 prod=next(p for p in B['products'] if p['catalog_ref']==x['id']);refs=prod['assembly_refs']
 if x['id'] in ['computer.artemis','computer.artemis_pro']:
  configs=[z for z in x['memory']['configurations'] if z['shipping_configuration']]
  for conf in configs:
   a='assembly.'+x['id']+'.'+conf['id'];row(x['id']+'.'+conf['id'],x['id'],x['name']+f' — {conf["ram_kb"]} KiB ({conf["populated_modules"]} modules)', 'Computers','one chassis, no keyboard/monitor/system cartridge',date(x),assembly_ref=a,announced_only=x['id']=='computer.artemis_pro',assumptions=['Separate system bundle rows include the OS, accessories and bundled support; do not add these rows to bundle costs.'])
   if x['id']=='computer.artemis':row(x['id']+'.'+conf['id']+'.networked',x['id'],x['name']+f' — {conf["ram_kb"]} KiB networked','Computers','one chassis with NIC, no OS/accessories','1981-05-04',assembly_ref=a+'.networked')
 else:
  for a in refs:row(x['id']+(('.'+a.split('.')[-1]) if len(refs)>1 else ''),x['id'],x['name']+((' — '+a.split('.')[-1].replace('_',' ')) if len(refs)>1 else ''),'Computers' if x['id'].startswith('computer') else 'Peripherals','one chassis, no accessories/system cartridge' if x['id'].startswith('computer') else 'one finished accessory',date(x),assembly_ref=a)
# OEM custom chips are explicitly offered by the component-licensing service.
for ref in sorted(custom):
 x=records[ref];row(ref,ref,x['name'],'OEM chips','one tested packaged chip, bulk shipment',date(x),assembly_ref='assembly.'+ref)
# Software production excludes development; platform variants retain distinct availability.
software_profiles={'aurelia_compatibility_kit':(5,800),'abacus_1':(1,80),'simple_c_z80':(3,220),'aurelia_sdk':(5,800),'bpi_suite':(5,700),'microsoft_basic_aurelia':(1,180),'pulse_1':(3,240),'abacus_2':(2,160),'aion_c_ide':(6,400),'artemis_sdk':(8,1000),'abacus_3':(4,280),'pulse_3':(4,300),'bpi_client_server':(8,800)}
team_delivery=read_document('generated/catalogs/team-development-program.json', root=R)['delivery']
software_profiles.update(ncc['software_profiles'])
software_profiles['autocad_1_artemis']=(0,0) # Future independent product: no June retail/royalty estimate.
software_profiles['aion_development_team']=(team_delivery['disks'],team_delivery['printed_pages'])
external_platform_ids={x['id'] for x in C.get('external_platforms',[])}
external_editions=[]
for x in C['platform_editions']:
 if x['platform_support'] and all(s['computer_ref'] in external_platform_ids for s in x['platform_support']):
  external_editions.append(x);continue
 key=x['id'].split('.')[1];a='assembly.media.software.'+key
 kwargs={'assembly_ref':a} if a in assemblies else {'software_profile':software_profiles.get(key)}
 if kwargs.get('software_profile','present') is None:kwargs={'not_costed_reason':'No qualified media, licence and delivery cost profile is recorded for this edition.'}
 if records[x['product_ref']].get('vendor')=='Autodesk':kwargs['not_costed_reason']='Future independent Autodesk product; distribution and licence terms not costed.'
 if key=='aion_development_team':kwargs['service_hours']=team_delivery['onboarding_staff_hours']+team_delivery['first_year_support_staff_hours']
 row(x['id'],x['id'],x['name'],'Software editions','one edition media/manual set',date(x),**kwargs,assumptions=['Edition reproduction and delivery only; product is a grouping and has no additional manufacturing charge.'])
for m in records['software.bpi_suite']['modules']:row('software.bpi_suite.'+m['name'].lower().replace(' ','_'),'software.bpi_suite',m['name'],'Software','one module media/manual set','1978-06-05',software_profile=[1,140])
for x in C['offered_bundles']:
 row(x['id'],x['id'],x['name'],'Bundles','one complete catalog offer',date(x),assembly_ref=x['bom_assembly_ref'],manufacturing_variants=x.get('manufacturing_variants',[]),included_services=x.get('included_services',[]),announced_only=bool(x.get('availability_status')),assumptions=['Recursive BOM packout; never sum a bundle and its constituent product rows.','The dated manufacturing variant determines NIC and OS inclusion.'])
# Service delivery units are necessary to avoid calling an annual contract a manufactured item.
for x in C['services']:
 id=x['id'];category=x['category'];args={}
 if category=='sales_channel':args={'not_costed_reason':'Sales channel, not a manufactured product. Marketing/sales activity excluded; product logistics is already included.'};unit='not applicable'
 elif category=='oem_licensing':args={'not_costed_reason':'Negotiated licensing has no defined unit. Recurring chip manufacture is assessed in individual OEM chip rows; engineering/NRE is excluded.'};unit='negotiated contract'
 elif category=='compatibility_engineering':args={'service_hours':x['engineering_hours']};unit=x['delivery_unit']
 elif category=='support':args={'service_hours':{'service.customer_care':.6,'service.regular_support':2,'service.professional_support':4,'service.professional_business_onsite':8}[id],'travel':100 if 'onsite' in id else 0};unit='one customer-year'
 elif category=='developer_program_and_license':args={'developer_sdk':'software.aurelia_sdk' if 'aurelia' in id else 'software.artemis_sdk','service_hours':2};unit='one registration with SDK'
 elif category=='training':args={'course_days':2 if 'pulse' in id else 3 if 'bpi' in id else 2,'onsite':'customer_site' in id};unit='one learner-course (8 learners, 6 contact hours/day)'
 else:raise ValueError('Unsupported service category '+category+' for '+id)
 row(id,id,x['name'],'Services',unit,date(x),**args,assumptions=['Course duration and service usage are explicit planning units, not established contractual limits. Free promotional vouchers are excluded as marketing.'])
 if id in ['service.academy_before_you_buy','service.academy_regular_courses']:
  for n,course in enumerate(records['service.academy_before_you_buy']['courses']):row(id+'.course_'+str(n+1),id,x['name']+' — '+course['name'],'Services','one learner-course (8 learners)',date(x),course_days=course['days'],assumptions=['No voucher/promotion charge; same physical delivery cost for regular and before-you-buy courses.'])
# Estimate final fulfillment only once at the top product level.
def fulfillment(r,i):
 g=r['group'];scale=overhead[i];v=vec()
 if g=='OEM chips':v.update(instructions=.02*scale,packaging=.12*scale,logistics=.15*scale);return v
 if g=='Computers':v.update(instructions=2*scale,packaging=8*scale,logistics=12*scale);return v
 if g=='Bundles':
  small='upgrade' in r['id'];v.update(instructions=(4 if small else 8)*scale,packaging=(3 if small else 18)*scale,logistics=(4 if small else 24)*scale);return v
 if g in ['Software','Software editions']:v.update(packaging=1.2*scale,logistics=1.5*scale);return v
 if g=='Peripherals':
  big=any(k in r['catalog_ref'] for k in ['monitor','mono_pro','color_pro','print','disk']);v.update(instructions=1.2*scale,packaging=(6 if big else 1.8)*scale,logistics=(8 if big else 2.5)*scale)
 return v

def support_cost(hours,i,travel=0):
 v=vec();v['workforce']=hours*wages[i]*1.35*1.6;v['operating_overhead']=v['workforce']*.25+hours*1.5*overhead[i];v['instructions']=1*overhead[i];v['logistics']=travel*overhead[i];return v

def estimate(r,i,source_inputs=None):
 v=vec();flat=Counter();a=r.get('assembly_ref');snapshot=snapshots[i]
 for variant in r.get('manufacturing_variants',[]):
  if variant['effective_from']<=snapshot:a=variant['assembly_ref']
 if a:v,flat=rollup(a,i,source_inputs)
 if r.get('software_profile'):
  disks,pages=r['software_profile'];v['bom_materials']=disks*[1.6,1.5,1.4,1.3,1.2][i];v['instructions']=(pages*.018+1.2)*overhead[i];v['workforce']=(.08+.025*disks)*wages[i]*1.35;v['energy']=.1*electricity[i];v['consumables']=.1*overhead[i];v['operating_overhead']=v['workforce']*.25
 if r['group'] in ['Software','Software editions'] and a:v['instructions']+=3*overhead[i]
 # Third-party rights are uncertain but recurring royalty costs are not software development.
 ref=r['catalog_ref']
 if ref=='software.cpm_aurelia':v['recurring_licenses']+=10
 if ref=='software.microsoft_basic_aurelia':v['recurring_licenses']+=20
 if ref=='software.cpm_aurelia_networking':v['recurring_licenses']+=5
 if a and r['group']=='Bundles':
  if any(k.startswith('part.software.cpm_aurelia.') for k in flat):v['recurring_licenses']+=10
  if any(k.startswith('part.software.cpm_aurelia_networking.') for k in flat):v['recurring_licenses']+=5
 for srv in r.get('included_services',[]):v['included_service_delivery']+=sum(support_cost(2,i).values())*srv.get('duration_years',1)
 if 'service_hours' in r:add(v,support_cost(r['service_hours'],i,r.get('travel',0)))
 if r.get('developer_sdk'):
  sdk=next(x for x in rows if x['id']==r['developer_sdk']);sv,_,_=estimate(sdk,i);add(v,sv)
 if 'course_days' in r:
  days=r['course_days'];h=days*7.5/8;v['workforce']+=h*wages[i]*1.35*2;v['energy']+=days*4*electricity[i];v['consumables']+=days*.4*overhead[i];v['instructions']+=days*2*overhead[i];v['operating_overhead']+=v['workforce']*.3+days*1.5*overhead[i];v['logistics']+=(days*35/8 if r.get('onsite') else 0)*overhead[i]
 add(v,fulfillment(r,i));return v,flat,a
for r in rows:
 for i,y in enumerate(years):
  if r['available_from']>snapshots[i]:r['snapshots'][str(y)]={'status':'not_yet_offered','total_usd':None};continue
  if r.get('not_costed_reason'):r['snapshots'][str(y)]={'status':'not_applicable','total_usd':None,'reason':r['not_costed_reason']};continue
  v,flat,a=estimate(r,i);breakdown={k:round(n,2) for k,n in v.items()};total=round(sum(breakdown.values()),2)
  low,high=(.55,1.9) if r['group']=='Services' else (.5,2.5) if r['group']=='OEM chips' else (.7,1.6)
  if 'artemis_pro' in r['id']:low,high=.65,1.75
  r['snapshots'][str(y)]={'status':'announced_shipping_unconfirmed' if r.get('announced_only') else 'offered_estimate','total_usd':total,'low_usd':round(total*low,2),'high_usd':round(total*high,2),'breakdown_usd':breakdown,'bom_assembly_ref':a,'bom_lines':[{'component_ref':k,'quantity':n,'extended_recurring_cost_usd':round(n*sum(inputs[k]['annual_cost_buckets_usd'][str(y)].values()),2)} for k,n in sorted(flat.items())],'confidence':'low','range_basis':'Scenario envelope, not statistical confidence interval; excludes capital, R&D and software development.'}
# Team license includes capped services; editions are alternative distributions, never additive sales.
for r in rows:
 if r['id']=='software.aion_development_team':
  r['unit']='one server / four-concurrent-developer license, media, 20h onboarding and 12h first-year support'
  r['assumptions']=['12 disks, 1000 printed pages and 32 staff-hours are planning allowances. Hardware, development/NRE, marketing and capital excluded; no recurring royalty for owned software.']
# Coverage ledger deliberately includes internal/superseded records without pretending they are products.
covered={r['catalog_ref'] for r in rows};excluded=[{'catalog_ref':x['id'],'reason':'External partner offering; manufacturing/media boundary and OEM terms not costed.'} for x in C.get('external_platforms',[])+C.get('external_partner_products',[])+external_editions]
for cat in ['computers','devices','software_products','services','offered_bundles','components','technologies','proposed_bundles']:
 for x in C[cat]:
  if x['id'] not in covered:excluded.append({'catalog_ref':x['id'],'reason':'Proposed bundle, not offered' if cat=='proposed_bundles' else 'Technology/specification, not separately sold' if cat=='technologies' else 'Superseded/prototype part, not active offering' if x.get('superseded_by') or 'prototype' in x['id'] or '128kbit' in x['id'] or 'module_64kb' in x['id'] else 'Purchased/internal component; included in end-product BOM, not a separate Logix offering'})
sources=[{'id':'bls_wages','title':'BLS via FRED: manufacturing production-worker average hourly earnings','url':'https://fred.stlouisfed.org/data/AHEMAN','used_for':'June nominal wage anchors: 5.99, 6.54, 7.08, 7.85 USD/h. Benefits factor and skill multipliers are assumptions.'},{'id':'eia_power','title':'EIA Annual Energy Review Table 8.10','url':'https://www.eia.gov/totalenergy/data/annual/txt/ptb0810.html','used_for':'Annual US industrial electricity proxies: 2.8, 3.1, 3.7, 4.3 cents/kWh. Annual rates are retrospective proxies, not June-specific tariffs.'},{'id':'byte_1978','title':'BYTE November 1978 advertising','url':'https://vintageapple.org/byte/pdf/197811_Byte_Magazine_Vol_03-11_OSCAR_amateur_radio_satellites.pdf','used_for':'Retail 4116 kit price sanity check only. OEM DRAM prices are scenario discounts; this later-1978 advertisement is not a June quote.'},{'id':'disk_retail','title':'Apple Disk II advertisement, BYTE August 1978','url':'https://vintageapple.org/byte/pdf/197808_Byte_Magazine_Vol_03-08_Pascal.pdf','used_for':'495 USD complete-drive retail comparison only; not its manufacturing cost.'},{'id':'seagate_oem','title':'Computer History Museum corporate-history report: Seagate','url':'https://archive.computerhistory.org/resources/access/text/2015/04/102740040-05-01-acc.pdf','used_for':'Historical 5 MB drive pricing span (single-unit 1500 USD, 5000-unit tier 775 USD); 950 USD 1981 OEM central value is an assumption, not a dated Logix quote.'}]
model={'metadata':{'title':'Logix / AION recurring unit cost assessment','version':'1.2','currency':'USD','price_basis':'nominal dollars of each snapshot year; no conversion to current money','snapshots':snapshots,'source_commit':'c4567d340882e132ca92671861487af453dafc80','source_note':'Baseline commit; source hashes identify the edited inputs used for this build.','source_sha256':{n:hashlib.sha256(document_bytes(n, root=R)).hexdigest() for n in ['generated/catalogs/logix-aion-technical-catalog-v2.json','generated/catalogs/hardware-bom.json','generated/catalogs/manufacturing-programs.json','generated/catalogs/memory-manufacturing.json']},'estimate_status':'engineering planning scenario; no supplier quotes; not audited manufacturing accounts','generated_by':'tools/build_cost_assessment.py'},'scope':{'included':['Purchased BOM and internal-chip recurring fabrication','Direct and test labor plus 35% employment burden','Electricity','Process consumables, materials lost to yield and rework','Recurring factory maintenance/supervision allowance','Printed instructions and media duplication','Packaging','Inbound/outbound logistics allowance to US distribution/customer','Assumed recurring third-party royalties','Explicitly bundled support delivery; service rows use their stated units'],'excluded':['R&D and design engineering','Land, factory construction and equipment purchases','Capital depreciation, equipment leases and financing','Original masks, tooling and fixture NRE','Software and firmware development, including maintenance-release development','Marketing, promotion and vouchers','ComputerLand fees and retailer margin','Profit, income/sales tax and working-capital interest'],'boundary':'US production/distribution scenario. Purchased parts retain vendor margins/capital in their purchase price. Routine maintenance is included; Logix-owned capital cost is excluded. No fleet-wide total is calculated: rows include overlapping bundles and alternatives.'},'assumptions':{'offering_policy':'Introduction on/before June 15 qualifies as offered, not proven shipment. No withdrawals are specified: earlier models/versions remain in the scenario. PRO is marked announced/shipping unconfirmed. Non-shipping RAM expansion targets excluded as factory configurations.','scale':'Planning scale: 10,000 hardware units per family/year, OEM electronics orders generally 10k–100k pieces; PRO 1,000/year, cartridges/printed editions 5,000 copies. Volumes are assumptions, not story facts. Steady recurring runs even at recently announced launches; ramp risk in high range.','labor_usd_per_hour':dict(zip(map(str,years),wages)),'labor_burden_multiplier':1.35,'electricity_usd_per_kwh':dict(zip(map(str,years),electricity)),'assembly_learning':'5 percentage points less assembly time each year relative to 1978 baseline; new/complex designs retain larger operation-hour budgets.','logistics':'Per-unit bulk US freight/handling allowance. No individually quoted route or international customs model.','custom_fabrication':'75 mm NMOS wafer assumption, die area and yield per chip below. Advanced design/mask access does not eliminate recurring wafer processing or failures. No capital/NRE allocation.','royalties':'CP/M 10 USD/copy, CP/M networking 5 USD, Microsoft BASIC 20 USD; provisional contract allowances, not sourced contract terms. Owned software has no external royalty.','service_units':'Support is per customer-year; training is per learner at 8 learners and 6 teaching hours/day plus 1.5 prep hours/class/day. Unspecified course lengths are scenario assumptions. No repair-parts entitlement is assumed unless stated.','uncertainty':'Hardware/software ranges usually 0.70–1.60× central; PRO 0.65–1.75×; OEM silicon 0.50–2.50×; services 0.55–1.90×. Correlated scenario envelopes, not statistical intervals. Custom chip yield and 64K DRAM procurement dominate risk.','double_counting':'Nested BOMs count each component once. Final manuals/cartons/freight applied only at the top-level offer. Chip fabrication labor/energy is categorized inside the breakdown; extended BOM line costs include these internal conversion costs and must not be added to the total again.'},'sources':sources,'component_cost_assumptions':inputs,'chip_fabrication_models':chip_models,'assembly_routing_assumptions':assembly_inputs,'unresolved_quantity_assumptions':quantity_assumptions,'products':rows,'coverage_exclusions':excluded}
# Separate procurement and one-time program scenarios; never folded silently into base costs.
programs=read_document('generated/catalogs/manufacturing-programs.json', root=R)
program=programs['smc_transfer']
alt_inputs=copy.deepcopy(inputs);supplier_chips=[]
for ref in program['licensed_part_refs']:
 cid=ref;annual={}
 for i,y in enumerate(years):
  if snapshots[i] < program['initial_sales_date']:
   annual[str(y)]={'status':'not_yet_available','purchase_price_usd':None};continue
  internal=sum(inputs[cid]['annual_cost_buckets_usd'][str(y)].values())
  price=round(internal*program['purchase_price_proxy']['central_multiplier']+program['purchase_price_proxy']['inbound_freight_usd_per_chip'],5)
  alt_inputs[cid]['annual_cost_buckets_usd'][str(y)]={'bom_materials':price}
  annual[str(y)]={'status':'conditional_on_part_qualification','aion_internal_recurring_cost_usd':round(internal,5),'purchase_price_usd':price,'low_usd':round(internal*program['purchase_price_proxy']['low_multiplier']+program['purchase_price_proxy']['inbound_freight_usd_per_chip'],5),'high_usd':round(internal*program['purchase_price_proxy']['high_multiplier']+program['purchase_price_proxy']['inbound_freight_usd_per_chip'],5),'includes':'Supplier conversion cost, margin/capital recovery and any embedded license royalty; inbound freight. Do not add AION fabrication cost again.'}
 supplier_chips.append({'part_ref':ref,'snapshots':annual})
card_scenarios=[]
for r in rows:
 if r['id'] not in programs['ncc1979_card_refs']:continue
 annual={}
 for i,y in enumerate(years):
  if snapshots[i]<program['initial_sales_date']:
   annual[str(y)]={'status':'not_yet_available','total_usd':None};continue
  v,flat,a=estimate(r,i,alt_inputs);bd={k:round(n,2) for k,n in v.items()};total=round(sum(bd.values()),2)
  annual[str(y)]={'status':'conditional_on_all_used_parts_qualified','total_usd':total,'breakdown_usd':bd,'delta_vs_aion_base_usd':round(total-r['snapshots'][str(y)]['total_usd'],2),'replaced_chip_quantities':{ref:flat[ref] for ref in program['licensed_part_refs'] if flat[ref]}}
 card_scenarios.append({'catalog_ref':r['id'],'name':r['name'],'snapshots':annual})
model['manufacturing_programs']=programs
model['supplier_scenarios']={'supplier':'SMC','basis':'Illustrative purchased-price sensitivity, not an SMC quote. Independent commercial sales start October 1979, after the June 1979 snapshot. Base costs retain AION fabrication; alternate rows replace rather than add chip costs. Part qualification is required, not assumed proven.','chips':supplier_chips,'cards':card_scenarios}
model['assumptions']['second_source']='June 1979 cards use AION chips. SMC procurement is a separate conditional scenario from October 1979; June 1980/1981 comparisons do not assert a purchasing switch or a price reduction.'
model['assumptions']['joint_dri']='DRI remains a separately owned licensor despite Adam’s minority stake. Existing provisional per-copy CP/M allowance remains; the $250,000 founder capital commitment is excluded from unit costs.'

model['assumptions']['extension_1982']='June 15 1982: nominal planning wage $8.30/h, power $0.047/kWh, overhead index 1.43; OEM prices are estimates. 3 µm non-memory defect density 1.6/cm², maturity .86 for ERA/Artemis; memory uses dated existing recipe policy. No new line investment, demand or total profit inferred.'
model['metadata']['source_sha256']['generated/catalogs/ncc-1982-inputs.json']=hashlib.sha256(document_bytes('generated/catalogs/ncc-1982-inputs.json', root=R)).hexdigest()
model['assumptions']['ncc_1982']='New products use itemized June-dollar allowances, dedicated launch routing without prior-year learning, conservative new-logic yields, and dated qualified RAM. Estimates do not certify production readiness. Updates have no extra licence fee; driver media is included in mouse BOM. Autodesk future royalties are uncosted.'
model['metadata']['source_sha256']['generated/catalogs/team-development-program.json']=hashlib.sha256(document_bytes('generated/catalogs/team-development-program.json', root=R)).hexdigest()
previous_path=R/'generated/models/manufacturing-costs.json'
if previous_path.exists():
 previous=json.loads(previous_path.read_text())
 if 'reviews' in previous:model['reviews']=previous['reviews']
(R/'generated/models/manufacturing-costs.json').write_text(json.dumps(model,indent=2,ensure_ascii=False)+'\n')
print('Rows:',len(rows),'components:',len(inputs),'unknown BOM quantities assumed:',len(quantity_assumptions))
for r in rows:
 if r['group'] in ['Computers','Bundles']:print(r['name'],[r['snapshots'][str(y)]['total_usd'] for y in years])




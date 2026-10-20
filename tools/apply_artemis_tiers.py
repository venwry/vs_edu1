"""One-time, idempotent migration to accepted Artemis hardware tiers.
Run before the normal builders. All monetary values remain explicit planning assumptions.
"""
import json,copy,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(f):return json.loads((R/f).read_text())
def save(f,x):(R/f).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def edit(f,a,z):
 p=R/f;s=p.read_text()
 if a not in s:raise AssertionError((f,a[:100]))
 p.write_text(s.replace(a,z))
def repair_64k_requirements():
 cat=load('logix_aion_technical_catalog_v2.json')
 part=next((x for x in cat['base_parts'] if x['id']=='part.aion_4164'),None)
 if part:
  bom=load('hardware_bom.json')
  for x in bom['components']+bom['assemblies']:
   if x['id'] in ['bompart.part.aion_4164','assembly.part.aion_4164']:x['requirements']=part['manufacturing_requirements']
  save('hardware_bom.json',bom)
if (R/'artemis_tiers.json').exists():
 repair_64k_requirements()
 print('Artemis tier migration already applied; normal builders remain authoritative.')
 raise SystemExit(0)
c=load('logix_aion_technical_catalog_v2.json');b=load('hardware_bom.json')
r={x['id']:x for a in c.values() if isinstance(a,list) for x in a if isinstance(x,dict) and 'id'in x}
a=r['computer.artemis'];intro=copy.deepcopy(a['introduced'])
small='device.artemis_video_card_16kb';large='device.artemis_video_card'
aion='part.aion_4164';mod='part.artemis_ram_module_128kb_aion'
# Freeze this revision's actual predecessor, rather than relabel an older baseline.
oldroi=load('roi_1974_1980.json');oldinv=load('industrial_investment_1974_1981.json');oldsales=load('sales_forecast.json')
last=next(x for x in oldroi['scenarios'] if x['id']=='central')['quarterly'][-1]
year=next(x for x in oldinv['summary_annual'] if x['year']==1980)
baseline={'source_commit':'a19af421f897cdb29b7a7937348bf08f55b33c13','status':'Frozen preceding 32 KiB-card model; scenario comparison, not historical accounts.','metrics':{'artemis_deliveries_to_nov18':next(x for x in oldsales['scenarios'] if x['id']=='central')['ncc_to_comdex1980']['artemis_units'],'full_demand_1980':year['computer_demand'],'end_1980_headcount':year['year_end_headcount'],**{k:last[k] for k in ['cumulative_accounting_roi_pct','cumulative_net_cash_usd','peak_external_funding_usd','cumulative_net_revenue_usd']}}}
save('artemis_display_baseline.json',baseline)
big=copy.deepcopy(a['video']);v=copy.deepcopy(r['computer.aurelia']['video'])
v.update(video_ram_kb=16,card_ref=small,controller_ref='part.aurelia_video_chip')
v['display_memory']={'chip_ref':'part.aion_4116','chip_count':8,'capacity_bytes':16384,'bank_data_width_bits':8,'organization':'16K × 8 bits; independent display refresh.'}
v['pixel_buffer']={'pages':4,'bytes_per_page':40,'total_bytes':160,'bits_per_pixel':4,'location':'Inside reused Aurelia controller','policy':'FREE/FILLING/READY/READING banks; output latches and serializer. Never overwrite active bank; underrun preserves sync.'}
v['character_row_cache']={'banks':2,'bytes_per_bank':160,'total_bytes':320}
v['host_interface']={'host_width_bits':32,'local_display_width_bits':8,'implementation':'Buffered 32-to-8-bit bridge with byte enables, staging latches and bounded READY/backpressure. Word uploads require up to four local transfers; no native 32-bit display-memory bank is claimed.','hot_swap':False}
v['arbitration']=big['arbitration']
v['monitor_policy']='Mono II / Color II use legacy 200-line raster profiles. No 26.88 kHz output and no Mono Pro support. CPU word size does not widen local display memory. All five sprites remain available.'
for m in v['text_modes']+v['bitmap_modes']:m['required_raster_ids']=(['raster_320_200'] if m['width']<=320 else [])+['raster_640_200']
smallrec=copy.deepcopy(r[large]);smallrec.update(id=small,name='Logix Artemis 16 KiB economy video card',specification=v,bom_assembly_refs=['assembly.'+small],offered_with=['computer.artemis'])
smallrec['manufacturing_requirements']=['Reuse qualified Aurelia video silicon; verify 32-bit host bridge, byte order, byte enables, DMA wait handling, clocks and power. Mono Pro unsupported.']
c['devices'].append(smallrec);r[large]['name']='Logix Artemis 32 KiB professional video card'
a['video']=copy.deepcopy(v)
a['video_variants']=[{'card_ref':small,'configuration_ids':[x['id'] for x in a['memory']['configurations'] if x['id'].startswith('m32_')],'specification':copy.deepcopy(v)},{'card_ref':large,'configuration_ids':[x['id'] for x in a['memory']['configurations'] if x['id'].startswith('m128_')],'specification':big}]
a['memory']['video_ram_kb']=16;a['memory']['video_ram_policy']='16 KiB with the 128 KiB low-density configuration; 32 KiB with the 256 KiB AION high-density configuration. Expanding a low-density machine does not automatically replace its card.'
a['io_and_expansion']['dedicated_video_slot']['included_card_ref']=small
a['io_and_expansion']['dedicated_video_slot']['configuration_card_refs']={'m32_128':small,'m128_256':large}
a['compatible_devices'].append(small)
a['manufacturing_requirements']=[x.replace('Qualify 32 KiB DRAM, 1 KiB sprite SRAM and Mono Pro timings together.','Qualify the selected 16/32 KiB card and 1 KiB sprite SRAM; Mono Pro is offered with the 32 KiB card only.') for x in a['manufacturing_requirements']]
part=copy.deepcopy(r['part.aion_4116']);part.update(id=aion,name='AION 64 Kbit DRAM (4164-equivalent)',introduced=intro,used_in=[mod],bom_assembly_refs=['assembly.'+aion])
part['specification']=copy.deepcopy(r['part.dram_64kbit']['specification']);part['specification'].update(capacity_kbit=64,data_width_bits=1,organization='64K × 1',manufacturing_planning={'die_area_mm2':45,'wafer_mm':75,'maturity_multiplier':0.85,'cost_1980_usd':15.1296,'cost_1981_usd':14.4529,'status':'Accepted central scenario; not proven yield. Smaller cell/array, sense amplifiers, retention, substrate bias, timing and process qualification required. No redundant-row yield benefit assumed.','boundary':'Recurring fabricated/package/test cost; development, masks and fab capital budgeted separately.'})
part['manufacturing_requirements']=['Qualify AION 64K×1 silicon, process, speed/retention bins, refresh and module power rails before the assumed May 1980 launch. Mature purchased DRAM is not silently treated as equivalent production evidence.']
c['base_parts'].append(part)
module=copy.deepcopy(r['part.artemis_ram_module_128kb']);module.update(id=mod,name='Artemis M128-16A 128 KiB / 16-bit AION RAM module',used_in=['computer.artemis'],bom_assembly_refs=['assembly.'+mod])
module['specification']['chip_type_ref']=aion;module['manufacturing_requirements']=['Sixteen AION 64K×1 chips per module; two modules provide Artemis 256 KiB with 32 chips. Electrical qualification pending.']
c['base_parts'].append(module)
for cfg in a['memory']['configurations']:
 if cfg['module_ref']=='part.artemis_ram_module_128kb':cfg['module_ref']=mod
a['memory']['module_refs']=[mod if x=='part.artemis_ram_module_128kb' else x for x in a['memory']['module_refs']]
r['part.artemis_ram_module_128kb']['used_in']=['computer.artemis_pro','device.artemis_ram_256kb_bank_kit']
# Canonical BOM: separate configured card from common motherboard.
assemblies={x['id']:x for x in b['assemblies']}
def line(ref,n=1,role='included component'):return {'ref':ref,'quantity':n,'unit':'each','role':role,'condition':'always','quantity_status':'defined'}
def addproduct(id):b['products'].append({'catalog_ref':id,'production_status':'design_baseline','assembly_refs':['assembly.'+id],'requirements':['Accepted planning design; qualification pending.']})
cp=copy.deepcopy(next(x for x in b['components'] if x['id']=='bompart.part.aion_4116'))
cp.update(id='bompart.'+aion,name=part['name'],catalog_ref=aion,manufacturer='AION Labs');b['components'].append(cp)
aa=copy.deepcopy(assemblies['assembly.part.aion_4116']);aa.update(id='assembly.'+aion,name=part['name'],lines=[line('bompart.'+aion)]);b['assemblies'].append(aa);addproduct(aion)
aa=copy.deepcopy(assemblies['assembly.part.artemis_ram_module_128kb']);aa.update(id='assembly.'+mod,name=module['name'],requirements=module['manufacturing_requirements'])
for l in aa['lines']:
 if l['ref']=='bompart.part.dram_64kbit':l['ref']='bompart.'+aion
b['assemblies'].append(aa);addproduct(mod)
bridge=copy.deepcopy(next(x for x in b['components'] if x['id'].endswith('.artemis_video_host_interface')))
bridge.update(id='bompart.'+small+'.economy_video_byte_bridge',name='32-bit host staging and 8-bit video bus bridge',catalog_ref=None,requirements=['Functional set: staging latches, byte enables, ordering, bounded READY; additional to existing card host buffering.']);b['components'].append(bridge)
aa=copy.deepcopy(assemblies['assembly.'+large]);aa.update(id='assembly.'+small,name=smallrec['name'],requirements=smallrec['manufacturing_requirements'])
for l in aa['lines']:
 if l['ref']=='bompart.part.artemis_graphics_chip':l['ref']='bompart.part.aurelia_video_chip'
 if l['ref']=='bompart.part.aion_4116':l['quantity']=8;l['role']='16 KiB / 8-bit local display RAM'
aa['lines'].append(line(bridge['id']));b['assemblies'].append(aa);addproduct(small)
assemblies['assembly.computer.artemis.base']['lines']=[l for l in assemblies['assembly.computer.artemis.base']['lines'] if l['ref']!='assembly.'+large]
for aa in b['assemblies']:
 if re.fullmatch(r'assembly\.computer\.artemis\.m(?:32|128)_\d+',aa['id']):
  high='.m128_' in aa['id']
  aa['lines'].append(line('assembly.'+(large if high else small),role='Exactly one configured video card'))
  if high:
   for l in aa['lines']:
    if l['ref']=='assembly.part.artemis_ram_module_128kb':l['ref']='assembly.'+mod
# Retire incompatible/duplicated offers rather than keep selectable stale bundles.
removed={'bundle.artemis_128_mono_pro','bundle.artemis_256_mono'}
c['offered_bundles']=[x for x in c['offered_bundles'] if x['id'] not in removed]
b['offers']=[x for x in b['offers'] if x['catalog_ref'] not in removed]
b['assemblies']=[x for x in b['assemblies'] if not any(x['id'] in ['assembly.'+id,'assembly.'+id+'.networked'] for id in removed)]
for x in c['offered_bundles']:
 if x.get('computer_ref')=='computer.artemis' and 'computer_configuration'in x:
  conf=x['computer_configuration'];conf['video_card_ref']=small if conf['ram_kb']==128 else large
  if conf['ram_kb']==256:conf['module_ref']=mod
# Existing references to retired mono256 mean the replacement Mono Pro offering.
def rewrite(x):
 if isinstance(x,dict):return {k:rewrite(v) for k,v in x.items()}
 if isinstance(x,list):return [rewrite(v) for v in x]
 if x=='bundle.artemis_256_mono':return 'bundle.artemis_256_mono_pro'
 if x=='bundle.artemis_128_mono_pro':return 'bundle.artemis_128_mono'
 return x
c=rewrite(c);b=rewrite(b)
# Both diagram layers group card-owned parts within a single component.
for kind in ['hardware','memory']:
 d=c['artemis_explorer']['diagrams'][kind]
 internal={'display_dram','sprite_sram','pixel_fifo','display_refresh'}
 d['nodes']=[n for n in d['nodes'] if n['id'] not in internal]
 d['edges']=[e for e in d['edges'] if not any(x in internal for x in e)]
 for n in d['nodes']:
  if n['id'] in ['graphics','video_ram']:n.update(title='Replaceable video card',record_ref=small,computer_path='video')
c['artemis_explorer']['memory_note']='Functional address map. The selected replaceable video card contains its controller, 16 or 32 KiB display DRAM, independent 1 KiB sprite SRAM and internal buffers. Host MMU, DMA and system refresh remain outside the card. Numeric apertures are not yet assigned.'
mem=next(x for x in c['technologies'] if x['id']=='technology.artemis_memory_model')['specification']
mem['display_memory_design'].update(display_dram_bytes='16384 on Artemis 128; 32768 on Artemis 256 and PRO',card_ref='device.artemis_video_card_16kb',card_variants=[small,large],on_chip_pixel_fifo_bytes='160 on economy; 640 on professional',on_chip_row_cache_bytes=320)
mem['physical_memory_design']['supported_module_refs'].append(mod)
api=next(x for x in c['technologies'] if x['id']=='technology.logix_display_api')['specification']
api['text_mode_policy']='Aurelia/Aurelia+ and Artemis 128 economy card: native 40×25 and 80×25 with 8×8 cells. Artemis 256/PRO professional card adds 80×25 at 8×16 and 80×40 at 8×10 with Mono Pro. Intersect card and monitor capabilities.'
api['video_ram_storage_policy']['graphics_buffering']='Aurelia family and Artemis economy card: 16 KiB, two 8000-byte bitmap pages or one 16000-byte page. Artemis professional card: 32 KiB, two 8000/16000-byte pages or one 32000-byte page. All text modes support two pages and one shared font; five sprites use separate SRAM.'
site=load('site_pages.json')
next(p for p in site['pages'] if p['id']=='peripherals')['record_refs'].append(small)
save('site_pages.json',site);save('logix_aion_technical_catalog_v2.json',c);save('hardware_bom.json',b)
# Cost model preserves the explicitly selected 45 mm² / 0.85 scenario and dated dollars.
edit('tools/build_cost_assessment.py',"'part.aion_4116':18","'part.aion_4116':18,'part.aion_4164':45")
edit('tools/build_cost_assessment.py',"custom=set(chip_area)","custom=set(chip_area)")
edit('tools/build_cost_assessment.py'," if i==3 and maturity<1:maturity=.86"," if i==3 and maturity<1:maturity=.86\n if ref=='part.aion_4164':maturity=.85")
edit('tools/build_cost_assessment.py',"allowances.update(card_allowances)","allowances.update(card_allowances)\nallowances['economy_video_byte_bridge']=6.5 # 1978 allowance, learning to $5.85 in 1980; no second video ASIC")
# Pricing removes unsupported offers and gives color/mono variants real cost dependencies.
edit('tools/build_pricing.py',"'bundle.artemis_128_color','bundle.artemis_256_mono','bundle.artemis_256_color'","'bundle.artemis_128_color','bundle.artemis_256_color'")
edit('tools/build_pricing.py',"'art128color','art256','art256color'","'art128color','art256color'")
edit('tools/build_pricing.py',"('artemis_128_mono_pro','art128pro'),","")
edit('tools/build_pricing.py',"'bundle.artemis_256_mono'","'bundle.artemis_256_mono_pro'")
edit('tools/build_pricing.py',"add('device.artemis_video_card',","add('device.artemis_video_card_16kb',group='Peripherals and expansion',note='Included in Artemis 128; separate replacement only. 32-bit host bridge, 8-bit local memory; Mono Pro unsupported.')\nadd('device.artemis_video_card',")
p=R/'tools/build_pricing.py';s=p.read_text();start=s.index('# Mono Pro versions retain exactly');end=s.index('# Deliberately explicit non-source cost addition',start)
s=s[:start]+"""# Color II alternatives keep the same card and system-memory tier.
for source in ['office','developer','migration']:
 original=byid['bundle.proposed_artemis_'+source]
 import copy
 revised=copy.deepcopy(original);revised['id']=original['id']+'_color';revised['name']=original['name']+' / Color II'
 for component in revised['components']:
  component['cost_ref']={'bundle.artemis_128_mono':'bundle.artemis_128_color','bundle.artemis_256_mono_pro':'bundle.artemis_256_color'}.get(component['cost_ref'],component['cost_ref'])
 P.append(revised);byid[revised['id']]=revised
""" +s[end:];p.write_text(s)
# Explicit sales mix: original 70% office / 15% developer / 15% migration retained.
p=R/'tools/extend_sales_comdex80.py';s=p.read_text()
start=s.index("    mix=revision['mono_pro_artemis_bundle_share']");end=s.index('    def basket',start)
s=s[:start]+"""    # 70% Artemis128, 30% Artemis256; 80% monochrome / 20% Color II within each tier.
    parts['artemis']=[('bundle.proposed_artemis_office',.56),('bundle.proposed_artemis_office_color',.14),('bundle.proposed_artemis_developer',.12),('bundle.proposed_artemis_developer_color',.03),('bundle.proposed_artemis_migration',.12),('bundle.proposed_artemis_migration_color',.03),('device.flexidisk',1),('device.flexiprint40',.7)]
""" +s[end:]
s=s.replace('conservative/central/strong intent uplift 6%/12%/18%','conservative/central/strong intent uplift 2.4%/4.8%/7.2%, scaled to 24% Mono Pro uptake')
needle="            n=sum(x['units'] for x in products.values());"
s=s.replace(needle,"""            art_units=products['artemis']['units']
            weights={'artemis_128_mono':.56,'artemis_128_color':.14,'artemis_256_mono_pro':.24,'artemis_256_color':.06}
            allocation={k:int(art_units*w) for k,w in weights.items()}
            for key in sorted(weights,key=lambda k:art_units*weights[k]-allocation[k],reverse=True)[:art_units-sum(allocation.values())]:allocation[key]+=1
            products['artemis']['configuration_units']=allocation
""" +needle);p.write_text(s)
rev=load('artemis_display_revision.json');rev.update(mono_pro_artemis_bundle_share=.24,demand_uplift={'conservative':.024,'central':.048,'strong':.072},demand_basis='70% Artemis128 (16 KiB card), 30% Artemis256 (32 KiB card and AION system RAM). Within each tier 80% monochrome and 20% Color II: total Mono Pro uptake 24%. Previous display-specific interest uplift scaled by 24/60; price elasticity applied once afterwards. Mix and response are scenario assumptions, not observed orders. Campaign remains $435,000; no additional price/value marketing bonus.')
rev['engineering_person_months'].update({'AION Labs 64K DRAM':120,'Logix memory and economy card':24,'AION Software economy driver':12})
save('artemis_display_revision.json',rev)
# New memory production needs development work and is automatically counted in fab loading.
edit('tools/build_investment_model.py',"prog('artemis_hardware'","""prog('aion_64k_dram','AION Labs','1977-Q3','1980-Q1',120,['part.aion_4164'],'64K cell/array, sense amps, refresh/retention, bias/power, process integration, masks, probe, speed bins and respin; additional to the existing 16K programme')
prog('artemis_tier_hardware','Logix','1979-Q1','1980-Q2',24,['device.artemis_video_card_16kb','part.artemis_ram_module_128kb_aion'],'Economy card host bridge and AION high-density modules: PCB, power, firmware and combined-load qualification')
prog('artemis_economy_driver','AION Software','1979-Q2','1980-Q2',12,['software.aionix','software.artemis_sdk'],'Detect fitted card, reject incompatible monitors/modes, serialize host writes and regression-test both video tiers')
prog('artemis_hardware'""")
# ROI describes current inputs and compares against the immediately preceding committed model.
edit('tools/build_roi.py','Central Artemis interest increases 12% before elasticity','Central Artemis display-related interest increases 4.8% before elasticity')
edit('tools/build_roi.py','Engineering increment: 150 person-months. Mono Pro uptake: 60% of Artemis','Engineering increment: 306 person-months (150 display plus 156 memory/economy-card). Mono Pro uptake: 24% of Artemis')

(R/'artemis-explorer.js').write_text("/* Artemis-family views use the same diagram shell as Aurelia, with catalog-owned layouts. */\nwindow.startArtemisExplorer=function(catalog,page,siteLink){\n'use strict';\nconst $=id=>document.getElementById(id),esc=v=>String(v??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c]));\nconst records=Object.fromEntries(Object.values(catalog).filter(Array.isArray).flat().filter(x=>x?.id).map(x=>[x.id,x]));\nconst settings=catalog.artemis_explorer,c=records[page.record_refs[0]],rec=id=>records[id],human=k=>k.replace(/_/g,' '),at=(obj,path)=>path.split('.').reduce((v,k)=>v?.[k],obj);\nif(!settings||!c?.memory?.configurations?.length)throw Error('The catalog is missing the Artemis architecture definitions.');\nconst value=v=>Array.isArray(v)?v.map(value).join('; '):v&&typeof v==='object'?Object.entries(v).map(([k,x])=>human(k)+': '+value(x)).join(' · '):typeof v==='boolean'?(v?'Yes':'No'):records[v]?.name||String(v??'—');\nconst fields=v=>Object.entries(v||{}).map(([k,x])=>`<div><dt>${esc(human(k))}</dt><dd>${esc(value(x))}</dd></div>`).join('');\nconst dl=v=>'<dl class=\"fields\">'+fields(v)+'</dl>';\nconst table=(heads,rows)=>'<div class=\"table-wrap\"><table><thead><tr>'+heads.map(h=>'<th scope=\"col\">'+esc(h)+'</th>').join('')+'</tr></thead><tbody>'+rows.map(r=>'<tr>'+r.map(x=>'<td>'+esc(value(x))+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>';\nconst configurations=c.memory.configurations,maxKB=c.memory.physical_capacity_limit_kb;\nlet layer='hardware',selected='',nodes=[],edges=[];\nconst network=()=>Boolean(c.networking?.included_by_default)||$('era').value==='1981';\nconst ramConfiguration=()=>configurations.find(x=>x.id===$('artemis-ram').value)||configurations.find(x=>x.id===c.memory.default_configuration);\nconst video=()=>c.video_variants?.find(v=>v.configuration_ids.includes(ramConfiguration().id))?.specification||c.video;\nconst module=()=>rec(ramConfiguration().module_ref);\nconst ram=()=>ramConfiguration().ram_kb;\nconst ramFacts=()=>({...ramConfiguration(),module_name:module().name,module_capacity_kb:module().specification.capacity_kb,module_data_width_bits:16,bank_data_width_bits:32,empty_sockets:c.memory.ram_sockets-ramConfiguration().populated_modules,physical_capacity_limit_kb:maxKB,capacity_limit_status:c.memory.capacity_limit_status,population_policy:c.memory.population_policy,upgrade_policy:c.memory.upgrade_policy,reliability_policy:c.memory.reliability_policy});\nconst clean=r=>Object.fromEntries(Object.entries(r||{}).filter(([k])=>!['id','used_by','used_in','compatible_with'].includes(k)));\nfunction add(id,title,sub,col,row,data,optional=false){nodes.push({id,title,sub,col,row,data,optional});}\nfunction product(id,col,row,optional=false,sub){const r=rec(id);if(!r)throw Error('Missing catalog record: '+id);add(id,r.name,sub||r.introduced?.event_start_date||human(r.category),col,row,clean(r),optional);}\nfunction definition(n){if(n.id==='network'&&!network())return;\n if(n.requires_compatible_device&&!c.compatible_devices.includes(n.record_ref))return;\n let r=n.record_ref?rec(['graphics','video_ram'].includes(n.id)?video().card_ref:n.id==='os'&&network()?settings.network_software_ref:n.record_ref):null,data=r?clean(r):{},source=r?.specification||r;\n if(n.fields)data=Object.fromEntries(n.fields.map(k=>[k,source[k]]));\n if(n.computer_path){const part=n.computer_path==='video'?video():n.computer_path.startsWith('video.')?at(video(),n.computer_path.slice(6)):at(c,n.computer_path);data=typeof part==='object'?{...data,...part}:{...data,policy:part};}\n if((n.id==='graphics'||n.id==='video_ram')&&data.specification){delete data.specification;delete data.manufacturing_requirements;}\n if(r?.specification_ref)data[rec(r.specification_ref).name]=rec(r.specification_ref).specification;\n if(n.id==='ram')data=ramFacts();\n if(n.id==='apps')data={compatible_software:c.compatible_software,software_compatibility:c.software_compatibility};\n let sub=r?.name||human(n.computer_path?.split('.').pop()||n.id);\n if(n.id==='cpu')sub=c.processor.variant+' · '+c.processor.clock_mhz+' MHz';\n if(n.id==='ram')sub=ram()+' KB · '+ramConfiguration().populated_modules+' modules · '+ramConfiguration().populated_banks+' banks';\n if(n.id==='graphics'||n.id==='video_ram')sub=video().video_ram_kb+' KB video RAM · '+video().text_modes.map(m=>m.columns+'×'+m.rows+' ('+m.glyph_width+'×'+m.glyph_height+')').join(' / ');\n if(n.id==='virtual')sub=rec(settings.memory_ref).specification.virtual_address_bits+'-bit virtual addresses';\n if(n.id==='physical')sub=rec(settings.memory_ref).specification.physical_address_bits+'-bit physical addresses';\n if(n.id==='rom')sub=c.io_and_expansion.rom_eeprom_cartridge_slots.count+' cartridge slots';\n if(n.id==='disk')sub=c.storage.internal_fdd.count+' floppy drives'+(c.storage.internal_hdd?' + '+c.storage.internal_hdd.capacity_mb+' MB HDD':'');\n add(n.id,n.title,sub,n.column,n.row,data,Boolean(n.optional));\n}\nfunction configuredDiagram(name){const view=settings.diagrams[name];view.nodes.forEach(definition);edges=view.edges.filter(e=>e.every(id=>nodes.some(n=>n.id===id)));}\nfunction peripherals(){\n add('host',c.name,'Host computer',2,1,{form_factor:c.form_factor,io_and_expansion:c.io_and_expansion});\n product('technology.flexibus',1,2,false,c.io_and_expansion.flexibus_ports+' ports');\n product(video().technology_ref,2,2);product('technology.plug_and_execute',3,2,false,c.io_and_expansion.expansion_slots.count+' × '+c.io_and_expansion.expansion_slots.width_bits+'-bit slots');\n edges=[['host','technology.flexibus'],['host',video().technology_ref],['host','technology.plug_and_execute']];\n const bundled=new Set(catalog.offered_bundles.filter(b=>b.computer_ref===c.id).flatMap(b=>b.included_devices||[]));\n c.compatible_devices.filter(id=>id!=='device.mono_pro'||video().video_ram_kb===32).filter(id=>network()||![settings.network_adapter_ref,'device.network_hub'].includes(id)).forEach((id,i)=>{\n  const d=rec(id),standard=id===video().card_ref||(id===settings.network_adapter_ref&&network()),bundle=bundled.has(id),optional=!standard&&!bundle;\n  product(id,i%3+1,Math.floor(i/3)+3,optional,(standard?'Included in selected configuration':bundle?'Bundle option':'Optional')+' · '+d.introduced.event_start_date);\n  const parent=d.category==='memory_expansion'?'host':['device.artemis_video_card','device.artemis_video_card_16kb'].includes(id)?'host':id==='device.network_hub'?settings.network_adapter_ref:d.category==='display'?video().technology_ref:['device.artemis_cpm80_module',settings.network_adapter_ref].includes(id)?'technology.plug_and_execute':'technology.flexibus';\n  edges.push([parent,id,optional]);\n });\n}\nfunction software(){const mode=$('software-mode').value;\n if(mode==='internals'){\n  configuredDiagram('software');\n  if(c.compatible_devices.includes(settings.compatibility_ref)){product(settings.compatibility_ref,3,4,true);edges.push(['files',settings.compatibility_ref,true]);}\n }else if(mode==='cartridge'){\n  const tools=rec(settings.business_tools_ref);product(tools.id,2,1);\n  tools.features.forEach((feature,i)=>{const id='tool-'+i;add(id,feature,'Office Suite component',i%3+1,Math.floor(i/3)+2,{suite:tools.name,feature,delivery:tools.delivery,portability_contract:tools.portability_contract});edges.push([tools.id,id]);});\n  product('technology.logix_tui_standard',1,5);product('technology.logix_display_api',3,5);edges.push([tools.id,'technology.logix_tui_standard'],[tools.id,'technology.logix_display_api']);\n }else if(mode==='portability'){\n  const ids=['api','tui','display','framework','language','artemis_tools','aurelia_tools'].map(k=>settings.portability_refs[k]);\n  ids.forEach((id,i)=>product(id,i%3+1,Math.floor(i/3)+1));edges=ids.slice(1).map(id=>[ids[0],id]);\n }else{\n  c.compatible_software.map(rec).forEach((r,i)=>product(r.id,i%3+1,Math.floor(i/3)+1,false,(r.sold_separately?'Sold separately':'Compatible software')+' · '+r.introduced.event_start_date));\n }\n}\nconst offers=[...(catalog.offered_bundles||[]),...(catalog.proposed_bundles||[])].filter(b=>b.computer_ref===c.id);\nfunction bundleItems(b,seen=new Set()){\n if(seen.has(b.id))throw Error('Circular base bundle: '+b.id);seen.add(b.id);\n let items=b.base_bundle_ref?bundleItems(rec(b.base_bundle_ref),seen):[];\n if(b.computer_configuration)items.push({id:b.computer_ref,configuration:b.computer_configuration});\n for(const id of [...(b.included_devices||[]),...(b.included_software||[])])items.push({id});\n for(const item of b.included_services||[])items.push({id:item.service_ref,duration_years:item.duration_years});\n return items;\n}\nfunction bundles(){const b=rec($('bundle-select').value);if(!b)return;\n add('bundle',b.name,b.availability||(b.status==='proposed'?'Proposed offer':'Catalog offer'),2,1,{...clean(b),explorer_note:settings.bundle_note});\n bundleItems(b).forEach((item,i)=>{const r=rec(item.id),id='bundle-item-'+i,col=i%3+1,row=Math.floor(i/3)+2;\n  if(item.configuration)add(id,r.name,item.configuration.ram_kb+' KB RAM'+(item.configuration.hdd_mb?' · '+item.configuration.hdd_mb+' MB HDD':''),col,row,{configuration:item.configuration,processor:r.processor,storage:r.storage});\n  else add(id,r.name,item.duration_years?item.duration_years+' year(s)':'Included',col,row,{...clean(r),...(item.duration_years?{duration_years:item.duration_years}:{})});\n  edges.push(['bundle',id]);\n });\n}\nfunction select(){const n=nodes.find(n=>n.id===selected);if(!n)return;\n $('diagram').querySelectorAll('[data-node]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.node===selected)));\n $('inspector').innerHTML='<div class=\"eyebrow\">'+esc(layer)+'</div><h2>'+esc(n.title)+'</h2><p>'+esc(n.sub)+'</p>'+window.renderSpecification(n.data,records);window.bindSpecificationControls($('inspector'));\n}\nfunction draw(){window.drawArchitectureWires($('diagram'),edges);}\nfunction details(){\n $('memory-section').innerHTML='<div class=\"eyebrow\">Memory organization</div><h2>'+esc(c.name)+' · '+ram()+' KB RAM</h2><p>'+esc(settings.memory_note)+'</p>'+table(['Resource','Configuration'],[['Virtual addressing',rec(settings.memory_ref).specification.virtual_address_bits+' bits'],['Physical addressing',rec(settings.memory_ref).specification.physical_address_bits+' bits'],['RAM population',ramConfiguration().populated_modules+' × '+module().specification.capacity_kb+' KB / 16-bit modules'],['Populated banks',ramConfiguration().populated_banks+' / '+c.memory.bank_count],['Data DRAM chips',ramConfiguration().data_chip_count],['Qualification',ramConfiguration().validation_status],['Available sockets',c.memory.ram_sockets],['Physical capacity design target',maxKB+' KB · qualification pending'],['Display DRAM',video().video_ram_kb+' KiB on replaceable card'],['Exclusive sprite SRAM','1 KiB; separate bus'],['Internal pixel buffer','4 × '+video().pixel_buffer.bytes_per_page+' bytes'],['Internal character row cache','2 × 160 bytes'],['Video-card connector','1 dedicated; four general slots retained'],['Cartridge slots',c.io_and_expansion.rom_eeprom_cartridge_slots]])+'<p>'+esc(settings.ram_note)+'</p><details><summary>RAM modules and process memory</summary>'+dl(clean(module()))+dl(rec(settings.os_model_ref).specification)+'</details>';\n $('software-section').innerHTML='<div class=\"eyebrow\">System organization</div><h2>'+esc(rec(network()?settings.network_software_ref:settings.os_ref).name)+'</h2>'+dl(clean(rec(network()?settings.network_software_ref:settings.os_ref)));\n $('portability-section').innerHTML='<div class=\"eyebrow\">Platform records</div>'+page.record_refs.filter(id=>id!==c.id).map(id=>`<details id=\"${esc(id)}\"><summary>${esc(rec(id).name)}</summary>${dl(clean(rec(id)))}</details>`).join('')+'<details><summary>'+esc(c.name)+' · full specification</summary>'+window.renderSpecification({...Object.fromEntries(Object.entries(clean(c)).filter(([k])=>k!=='video_variants')),video:video(),memory:{...c.memory,video_ram_kb:video().video_ram_kb}},records)+'</details>';window.bindSpecificationControls($('portability-section'));\n}\nfunction build(){nodes=[];edges=[];\n $('ram-choice').hidden=true;$('artemis-ram-choice').hidden=layer==='bundles';$('era').parentElement.hidden=Boolean(c.networking?.included_by_default)||layer==='bundles';\n $('offering-controls').hidden=!['software','bundles'].includes(layer);$('software-choice').hidden=layer!=='software';$('bundle-choice').hidden=layer!=='bundles';\n $('stats').innerHTML=[['Processor',c.processor.variant+' · '+c.processor.clock_mhz+' MHz'],['System RAM',ram()+' KB'],['Video RAM',video().video_ram_kb+' KB'],['Text display',video().text_modes.map(m=>m.columns+'×'+m.rows+' ('+m.glyph_width+'×'+m.glyph_height+')').join(' / ')]].map(([k,v])=>'<div class=\"stat\"><span>'+esc(k)+'</span><strong>'+esc(v)+'</strong></div>').join('');\n $('view-title').textContent=c.name.toUpperCase()+' / '+layer.toUpperCase();$('diagram-note').textContent=settings.notes[layer];\n if(layer==='hardware'||layer==='memory')configuredDiagram(layer);else if(layer==='peripherals')peripherals();else if(layer==='software')software();else bundles();\n if(!nodes.some(n=>n.id===selected))selected=nodes[0]?.id;\n $('diagram').innerHTML='<svg class=\"wires\" aria-hidden=\"true\"></svg>'+nodes.map(n=>`<button class=\"node ${n.optional?'optional':''}\" style=\"grid-column:${n.col};grid-row:${n.row}\" data-node=\"${esc(n.id)}\" aria-pressed=\"false\" aria-controls=\"inspector\"><small>${esc(layer)}</small><strong>${esc(n.title)}</strong>${['graphics','video_ram'].includes(n.id)?'<span class=\"video-card-contents\"><span>Controller: '+esc(rec(video().controller_ref).name)+'</span><span>Display RAM: '+video().video_ram_kb+' KiB</span><span>Sprite SRAM: 1 KiB, exclusive bus</span></span>':'<span>'+esc(n.sub)+'</span>'}<span class=\"plus\" aria-hidden=\"true\">+</span></button>`).join('');\n $('diagram').querySelectorAll('[data-node]').forEach(b=>b.addEventListener('click',()=>{selected=b.dataset.node;select();}));select();details();requestAnimationFrame(draw);\n}\n$('diagram').closest('main').classList.add('artemis-explorer');\n$('models').innerHTML=settings.page_ids.map(id=>siteLink(id)).join(' · ');$('page-heading').textContent=page.title;$('intro').textContent=page.description;\n$('launch').textContent=c.introduced.event_start_date;$('event').textContent=c.introduced.event_name;\n$('load-panel').hidden=true;$('ram-choice').hidden=true;\nconst control=document.createElement('label');control.id='artemis-ram-choice';control.className='era';control.innerHTML='RAM <select id=\"artemis-ram\">'+configurations.map(cfg=>`<option value=\"${esc(cfg.id)}\"${cfg.id===c.memory.default_configuration?' selected':''}>${cfg.ram_kb} KB · ${cfg.populated_modules} × ${rec(cfg.module_ref).specification.capacity_kb} KB · ${cfg.populated_banks} banks${cfg.shipping_configuration?' · shipping':' · expansion target'}</option>`).join('')+'</select>';$('ram-choice').after(control);\n$('era').disabled=false;$('era').value=c.networking?'1981':'launch';$('era').options[0].textContent='Launch configuration';$('era').options[1].textContent=rec(settings.network_software_ref).introduced.event_start_date+' · networking';\n$('software-mode').innerHTML=settings.software_views.map(v=>'<option value=\"'+esc(v.id)+'\">'+esc(v.label)+'</option>').join('');\n$('bundle-select').innerHTML=offers.map(b=>'<option value=\"'+esc(b.id)+'\">'+esc(b.name)+'</option>').join('');\n$('context').textContent=settings.context;$('timeline').innerHTML=settings.computer_refs.map(rec).map(x=>'<time>'+esc(x.introduced.event_start_date)+'</time><p>'+esc(x.name)+' · '+esc(x.introduced.event_name)+'</p>').join('');\nconst cs=settings.computer_refs.map(rec);$('comparison').closest('article').querySelector('h2').textContent='Artemis family comparison';\n$('comparison').innerHTML=table(['Component',...cs.map(x=>x.name)],[['Processor',...cs.map(x=>x.processor.variant+' · '+x.processor.clock_mhz+' MHz')],['Shipping RAM',...cs.map(x=>x.memory.configurations.filter(r=>r.shipping_configuration).map(r=>r.ram_kb).join(' / ')+' KB')],['RAM module',...cs.map(x=>x.memory.module_refs.map(id=>rec(id).specification.capacity_kb+' KB / 16-bit').join(' or '))],['Internal hard disk',...cs.map(x=>x.storage.internal_hdd?x.storage.internal_hdd.capacity_mb+' MB':'Not included')],['Video RAM',...cs.map(x=>(x.video_variants?'16 / 32':x.video.video_ram_kb)+' KiB')],['Networking',...cs.map(x=>x.networking?'Included at launch':'Standard from '+rec(settings.network_software_ref).introduced.event_start_date)]]);\nfor(const button of document.querySelectorAll('[data-layer]')){button.disabled=false;button.addEventListener('click',()=>{layer=button.dataset.layer;document.querySelectorAll('[data-layer]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));selected='';build();});}\nfor(const id of ['artemis-ram','era','software-mode','bundle-select'])$(id).addEventListener('change',build);\nif(typeof ResizeObserver!=='undefined')new ResizeObserver(draw).observe($('diagram'));window.addEventListener('resize',draw);build();\n};\n")

css=next((R/x for x in ['atlas.css','style.css','styles.css'] if (R/x).exists()),None)
if css:css.write_text(css.read_text()+'\n.video-card-contents{display:grid;gap:.3rem;border:1px solid currentColor;padding:.45rem;margin-top:.35rem;font-size:.78rem}.video-card-contents span{display:block}\n')
p=R/'tests/validate_artemis_video.py';s=p.read_text().replace("v=r['computer.artemis']['video'];assert v==r['computer.artemis_pro']['video']","v=r['computer.artemis_pro']['video'];assert v==r['computer.artemis']['video_variants'][1]['specification']")
s=s.replace("for host in ['computer.artemis','computer.artemis_pro']:","for host in ['computer.artemis_pro']:")
p.write_text(s)
p=R/'tests/validate_pricing.py';s=p.read_text().replace('==91','==90').replace('==234','==232').replace('91 offers / 234 snapshots','90 offers / 232 snapshots');p.write_text(s)
(R/'tests/validate_artemis_tiers.py').write_text('''"""Check configuration-specific card, sourcing, offer and demand invariants."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(f):return json.loads((R/f).read_text())
c=read('logix_aion_technical_catalog_v2.json')
r={x['id']:x for a in c.values() if isinstance(a,list) for x in a if isinstance(x,dict) and 'id'in x}
b=read('hardware_bom.json');aa={x['id']:x for x in b['assemblies']}
def pop(id):
 out={}
 for x in aa[id]['lines']:
  sub=pop(x['ref']) if x['ref'] in aa else {x['ref']:1}
  for k,n in sub.items():out[k]=out.get(k,0)+n*(x['quantity'] or 1)
 return out
small=r['computer.artemis']['video']
assert small['video_ram_kb']==16 and small['display_memory']['bank_data_width_bits']==8
assert small['host_interface']['host_width_bits']==32
assert small['pixel_buffer']['total_bytes']==160
assert small['sprite_memory']['capacity_bytes']==1024
assert len(small['text_modes'])==2 and len(small['bitmap_modes'])==6
for m in small['text_modes']:
 assert 2*m['ram_bytes_per_page']+m['font_bytes']<=16384
for m in small['bitmap_modes']:
 assert m['bytes_per_framebuffer']<=16384
 assert m['double_buffering']==(2*m['bytes_per_framebuffer']<=16384)
for m in small['text_modes']+small['bitmap_modes']:
 assert m['sprites_available']==5 and 'raster_640_400' not in m['required_raster_ids']
lo=pop('assembly.computer.artemis.m32_128');hi=pop('assembly.computer.artemis.m128_256');pro=pop('assembly.computer.artemis_pro.base')
assert lo['bompart.part.aion_4116']==8 and lo['bompart.part.aion_2114']==2
assert lo['bompart.part.aurelia_video_chip']==1 and not lo.get('bompart.part.artemis_graphics_chip')
assert hi['bompart.part.aion_4116']==16 and hi['bompart.part.aion_2114']==2
assert hi['bompart.part.aion_4164']==32 and not hi.get('bompart.part.dram_64kbit')
assert hi['bompart.part.artemis_graphics_chip']==1 and not hi.get('bompart.part.aurelia_video_chip')
assert not pro.get('bompart.part.aion_4164')
assert 'bundle.artemis_128_mono_pro' not in r and 'bundle.artemis_256_mono' not in r
for layer in ['hardware','memory']:
 nodes=c['artemis_explorer']['diagrams'][layer]['nodes']
 assert not {'display_dram','sprite_sram','pixel_fifo','display_refresh'}&{n['id'] for n in nodes}
 assert any(n.get('computer_path')=='video' for n in nodes)
for sc in read('sales_forecast.json')['scenarios']:
 for month in sc['ncc_to_comdex1980_months']:
  a=month['products']['artemis']
  assert sum(a['configuration_units'].values())==a['units']
  assert set(a['configuration_units'])=={'artemis_128_mono','artemis_128_color','artemis_256_mono_pro','artemis_256_color'}
iv=read('industrial_investment_1974_1981.json')
assert sum(p['person_months'] for p in iv['engineering_programs'] if p['id'] in ['aion_64k_dram','artemis_tier_hardware','artemis_economy_driver'])==156
print('PASS: Artemis tier BOMs, mode allocation, monitor constraints, selected-card diagrams, AION sourcing and sales reconciliation.')
''')
for f in ['logix_aion_story.json','ncc_1980_campaign.json']:
 if (R/f).exists():
  doc=rewrite(load(f))
  if f=='ncc_1980_campaign.json':doc['artemis_configuration_policy']='Artemis 128: 16 KiB card with Mono II or Color II. Artemis 256: 32 AION 64 Kbit system RAM chips and 32 KiB card with Mono Pro or Color II. Mono Pro requires the professional card; Color II uses legacy timings. See artemis_tiers.json.'
  if f=='logix_aion_story.json':
   e=next(e for p in doc['phases'] for e in p['events'] if e['id']=='event.artemis_launch')
   for act in e['actions']:
    if 'Ship the replaceable 32 KiB video card' in act['description']:
     act['description']='Ship Artemis 128 with a replaceable 16 KiB video card and Mono II or Color II; ship Artemis 256 with 32 AION 64 Kbit system RAM chips, a 32 KiB video card and Mono Pro or Color II. Both cards include 1 KiB exclusive sprite SRAM. Only the professional card and Mono Pro enable 640×400 modes; Color II keeps legacy timings. High-resolution demonstrations and paid follow-up campaign are separately budgeted; production qualification remains required.'
   e['product_refs']+=['device.artemis_video_card_16kb','part.aion_4164']
  save(f,doc)
doc=R/'ARTEMIS_VIDEO_CARD.md';s=doc.read_text()
s=s.replace('## Card and monitor','## Professional card and monitor (Artemis 256 / PRO)')
s=s.replace('## Text modes','## Professional card text modes').replace('## Bitmap modes','## Professional card bitmap modes')
s=s.replace('Four new complete hardware offers cover Artemis 128/256 KiB and PRO 512 KiB/1 MiB with keyboard and Mono Pro. Original legacy-monitor Artemis and server-only PRO offers remain alternatives.','Artemis 128 includes the 16 KiB economy card and Mono II or Color II. Artemis 256 includes the 32 KiB professional card and Mono Pro or Color II. PRO console offers retain the professional card and Mono Pro; server-only PRO offers remain available.')
s=s.replace('60% Mono Pro uptake among Artemis packages','24% Mono Pro uptake among Artemis packages').replace('6%/12%/18%','2.4%/4.8%/7.2%')
s=s.replace('Incremental engineering is 150 person-months:','Display engineering is 150 person-months:')
s=s.replace('Existing chip/process and OS programmes remain separately funded.','The tier revision adds 156 person-months: AION Labs 120 for the 64 Kbit DRAM, Logix 24 for modules/economy-card integration, and AION Software 12 for the economy driver. Total incremental engineering is 306 person-months. Existing chip/process and OS programmes remain separately funded.')
s=s.replace('## Professional card and monitor',"""## Economy card (Artemis 128)

The 16 KiB card reuses the Aurelia controller, eight AION 4116 chips, two AION 2114 sprite SRAMs, four 40-byte pixel pages and two 160-byte row caches. A buffered bridge connects the 32-bit host to 8-bit local display memory; a CPU word write needs up to four local transfers. This is not native 32-bit display memory. Its modes match Aurelia: 40×25 and 80×25 text with 8×8 cells, plus six legacy bitmap modes. Each 8000-byte bitmap supports two pages; each 16000-byte bitmap supports one. It cannot drive Mono Pro. Canonical per-mode allocations are shown in the selected-card explorer tables.

See [ARTEMIS_TIERS.md](ARTEMIS_TIERS.md) for the configuration and sourcing policy.

## Professional card and monitor""",1)
doc.write_text(s)
for p in R.glob('*.md'):
 s=p.read_text().replace('for the 32 KiB card, dedicated 1 KiB sprite SRAM','for the 16/32 KiB configuration-specific cards, dedicated 1 KiB sprite SRAM')
 if p.name=='RAM_BOM_DESIGN.md':
  s=s.replace('| Artemis | 256 KiB | 64K × 1 |','| Artemis | 256 KiB | AION 64K × 1 |')
  s=re.sub(r'covers all \d+ hardware records and \d+ offered hardware bundles\. Its \d+ assemblies and \d+ component requirements include both catalog parts and unresolved implementation requirements\.', 'covers all active hardware and offered bundles; validators reconcile coverage and recursive assembly contents. Assemblies include catalog parts and unresolved implementation requirements.',s)
  s=s.replace('All cost rollups are explicitly blocked; a sum of known lines must not be presented as a complete manufacturing cost.','The later manufacturing-cost model supplies explicit planning estimates for unresolved quantities; these are not supplier quotations.')
 p.write_text(s)
(R/'ARTEMIS_TIERS.md').write_text('''# Artemis configuration tiers

| Offering | System RAM | Included replaceable video card | Monitor alternatives |
|---|---|---|---|
| Artemis 128 | 64 × purchased 16 Kbit chips, 128 KiB | 16 KiB display DRAM + 1 KiB sprite SRAM; Aurelia controller | Logix Mono II / Logix Color II |
| Artemis 256 | 32 × AION 64 Kbit chips, 256 KiB | 32 KiB display DRAM + 1 KiB sprite SRAM; professional controller | Mono Pro / Logix Color II |
| Artemis PRO | Existing purchased high-density memory | Existing 32 KiB professional card | Existing console/headless offers |

Both cards contain the controller, display RAM, independent sprite SRAM and internal four-page pixel buffer. They use the dedicated replaceable-card connector. Host DMA, MMU and system refresh remain dedicated host components in the diagrams. Power off before replacement. The RAM selector changes the card shown throughout the Artemis explorer. Expansion of a low-density configuration does not automatically change its card.

The economy card connects the 32-bit host through byte staging to **8-bit local memory**. Eight 4116 chips provide 16 KiB; they cannot form a native 32-bit-wide 16 KiB memory array. The reused controller has four 40-byte pixel pages. It retains all Aurelia text/bitmap modes and five sprites in every mode. No 400-line modes are offered. The professional card retains four 160-byte pages and all 32 KiB modes. Only Mono Pro accepts its 26.88 kHz 640×400 raster; Color II continues to use legacy timings.

## Cost boundary and risk

The selected central AION 64 Kbit scenario assumes a 45 mm² die, 75 mm wafer and 0.85 maturity multiplier with the existing dated defect-density, wafer, packaging and test assumptions. It produces approximately $15.13 per chip in 1980 ($484.15 for 32) and $14.45 in 1981 ($462.49 for 32). The $462 selection is the 1981 estimate, not an undated launch price. Module PCBs, buffers, connectors, assembly and system testing are additional. AION is replacing purchased chips only in Artemis high-density configurations; PRO sourcing remains unchanged.

This is an unproven manufacturing scenario. Retention, refresh, sense amplifiers, cell/process integration, speed bins, power rails, host bridge timing and board loading require qualification. The investment model adds 120 AION Labs person-months for DRAM development, 24 Logix person-months for hardware integration and 12 AION Software person-months for economy-card support. The model's existing prototype/mask allowance and fab-capacity calculations apply; recurring chip cost does not pay for development or factory capex.

## Pricing, demand and finance

Prices are rebuilt from the configured BOM using the existing balanced contribution/net-receipts and below-proxy rule. Current dated results are in [pricing](pricing.html) and [manufacturing costs](manufacturing-costs.html); no manually maintained duplicate totals are used here.

The sales mix is an assumption: 70% Artemis 128 and 30% Artemis 256, each with 80% monochrome and 20% Color II. Therefore 24% of Artemis units use Mono Pro. The prior display appeal uplift is scaled by 24/60 to 2.4% / 4.8% / 7.2% before the existing price-elasticity adjustment; it is not added again as a second marketing bonus. The $435,000 display campaign is retained. Monthly configuration allocations sum exactly to Artemis deliveries.

Sales feed manufacturing, fab loading, staffing, logistics and capacity with 10% good-output headroom. ROI incorporates revised prices, costs, demand, engineering and capital; the comparison baseline is the preceding main commit a19af421. These are scenario estimates, not historical accounts or demonstrated production yields.

Run the five normal builders (cost, pricing, sales, investment, ROI), followed by Python validators and JavaScript DOM tests. tools/apply_artemis_tiers.py is an idempotent migration; artemis_tiers.json records application of the policy.
''')

# Exercise both card choices and ensure the visible component actually contains its parts.
edit('tests/atlas.test.cjs',"selectRAM('m32_128',128,4,2);","selectRAM('m32_128',128,4,2);assert(d.querySelector('[data-node=\"video_ram\"] .video-card-contents').textContent.includes('Display RAM: 16 KiB'));assert(d.querySelector('[data-node=\"video_ram\"] .video-card-contents').textContent.includes('Sprite SRAM: 1 KiB'));")
edit('tests/atlas.test.cjs',"selectRAM('m128_256',256,2,1);","selectRAM('m128_256',256,2,1);assert(d.querySelector('[data-node=\"video_ram\"] .video-card-contents').textContent.includes('Display RAM: 32 KiB'));assert(!d.querySelector('[data-node=\"display_dram\"]'));")

save('artemis_tiers.json',{'status':'Accepted planning scenario; electrical qualification pending','artemis_128':{'system_ram_kib':128,'video_card_ref':small,'monitor_refs':['device.mono_monitor_2','device.color_monitor_2']},'artemis_256':{'system_ram_kib':256,'system_ram_chip_ref':aion,'system_ram_chip_count':32,'video_card_ref':large,'monitor_refs':['device.mono_pro','device.color_monitor_2']},'pro_sourcing_changed':False,'sales_mix':{'artemis_128_mono':.56,'artemis_128_color':.14,'artemis_256_mono_pro':.24,'artemis_256_color':.06}})
repair_64k_requirements()
print('Applied Artemis configuration tiers; rebuild all derived models next.')

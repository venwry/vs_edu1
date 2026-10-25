/* Commercial source projection. Shared by browser and Python: no generated catalogue files. */
(function(root){'use strict';
const clone=x=>JSON.parse(JSON.stringify(x));
function project(input,{legacyBOM=false}={}){
 const docs=clone(input),pc=docs['data/product-catalog.json'];if(!pc)return docs;
 // Compatibility release labels are derived, never stored on products.
 const campaigns=Object.values(docs['data/campaigns.json']||{}).filter(c=>c&&typeof c==='object'&&c.id);
 for(const p of pc.products){const campaign=campaigns.find(c=>c.id===p.launch_campaign_ref);const start=p.composition_history.map(h=>h.valid_from).sort()[0];p.introduced={event_name:campaign?.title||campaign?.metadata?.title||p.launch_campaign_ref,event_start_date:start};}
 const editions=docs['data/software-editions.json'].software_editions;
 const softwareIds=new Set(editions.map(e=>e.id)),softwareLines=new Map();
 for(const e of editions){
  let group=softwareLines.get(e.software_line_id);
  if(!group){group={id:e.software_line_id,name:e.software_line_name,category:e.software_line_category,vendor:e.vendor,introduced:clone(e.introduced),edition_refs:[]};softwareLines.set(group.id,group);}
  group.edition_refs.push(e.id);if(e.introduced.event_start_date<group.introduced.event_start_date)group.introduced=clone(e.introduced);
  e.product_ref=e.software_line_id;e.delivery=e.distribution.medium;
  e.sold_separately=pc.products.some(p=>p.category==='software'&&p.id!=='product.aion_development_team'&&p.id!=='product.bpi_client_server'&&p.composition_history.some(h=>h.composition_definition.some(l=>l.ref===e.id||docs['data/devices.json'].devices.find(d=>d.id===l.ref)?.composition_history.some(v=>v.composition_definition.some(x=>x.ref===e.id)))));
  if(e.id==='software.aion_development_team'){const t=pc.products.find(p=>p.id==='product.aion_development_team').commercial_terms;e.specification.delivery_cost_assumptions={disks:t.total_distribution_diskettes,printed_pages:t.total_printed_pages,onboarding_staff_hours:t.onboarding_staff_hours,first_year_support_staff_hours:t.first_year_support_staff_hours,note:t.allocation_status};e.specification.commercial_unit={unit:'one server, four concurrent developer sessions',hardware_included:false};}
 }
 docs['data/software-products.json']={software_products:[...softwareLines.values()]};
 docs['data/software-editions.json'].platform_editions=editions;
 const physical=docs['data/devices.json'].devices;
 for(const d of physical)d.software_refs=[...new Set(d.composition_history.flatMap(h=>h.composition_definition.filter(l=>softwareIds.has(l.ref)).map(l=>l.ref)))];

 for(const d of physical){const h=d.composition_history?.[0];if(h){d.bom_assembly_definition=clone(h.composition_definition);if(h.bom_assembly_metadata)d.bom_assembly_metadata=clone(h.bom_assembly_metadata);}}
 const platformKeys=['introduced','technology_refs','lifecycle_policy','vendor','technical_profile','default_configuration','recommended_software_ref','production_status','upgrade_product_refs','role','availability','product_status','inclusion_qualification','programme_ref'];
 const platforms=physical.filter(d=>d.category==='base_computer').map(d=>{const p={id:d.id.replace('device.base_computer.','computer.'),name:d.name.replace(' — base computer',''),category:'computer',chassis_ref:d.id,computer_line:null,catalogue_status:'platform',hardware_assembly_refs:d.platform_assembly_refs||[]};for(const k of platformKeys)if(k in d)p[k]=clone(d[k]);return p;});
 const expandVersion=h=>{const out={main_product:null,connected_devices:[],attached_products:[]};if(h.legacy_assembly_ref)out.hardware_assembly_ref=h.legacy_assembly_ref;for(const line of h.composition_definition){const {ref,element_type,unit,role,condition,quantity_status,...other}=clone(line);if(element_type==='main_product'){if(!out.main_product)out.main_product={device_ref:ref};}else if(element_type==='connected_device')out.connected_devices.push({device_ref:ref,...other});else out.attached_products.push({[ref.startsWith('service.')?'service_ref':/^(software|edition)\./.test(ref)?'software_ref':'product_ref']:ref,...other});}return out;};
 for(const p of pc.products)if(p.composition_history){const [first,...rest]=p.composition_history;if(first)Object.assign(p,expandVersion(first));else Object.assign(p,{main_product:null,connected_devices:[],attached_products:[]});p.revisions=rest.map(h=>({...expandVersion(h),effective_from:h.valid_from,...p.revision_metadata?.find(r=>r.version_number===h.version_number)}));}
 pc.external_platforms=docs['data/ecosystem-inputs.json']?.external_platforms||[];

 const devices=docs['data/devices.json'].devices,parts=docs['data/components.json'].components,technologies=docs['data/standards.json'].technologies;
 const records=Object.fromEntries([...devices,...parts,...technologies,...editions,...pc.products,...platforms].map(r=>[r.id,r]));
 function resolve(v,seen=[]){if(Array.isArray(v))return v.map(x=>resolve(x,seen));if(v&&typeof v==='object'){if(v.source_ref){if(seen.includes(v.source_ref+JSON.stringify(v.path)))throw Error('Cyclic specification reference');let x=records[v.source_ref];for(const key of v.path)x=x?.[key];if(x===undefined)throw Error('Missing specification source '+v.source_ref+':'+v.path);return resolve(x,[...seen,v.source_ref+JSON.stringify(v.path)]);}return Object.fromEntries(Object.entries(v).map(([k,x])=>[k,resolve(x,seen)]));}return v;}
 for(const d of devices)if(d.specification_ref)d.specification={...clone(records[d.specification_ref].specification),...(d.specification||{})};
 for(const d of devices){if(d.specification)d.specification=resolve(d.specification);const r=d.specification?.sprite_profile_ref;if(r)d.specification.sprites=clone(records[r.technology_ref].specification.profiles[r.profile]);}
 for(const t of technologies)t.specification=resolve(t.specification);
 // Legacy export only: current UI resolves source composition histories directly.
 const stored=[];docs['data/assemblies.json']={assemblies:stored};
 const assemblies=new Map();
 const line=(ref,quantity,role='')=>({ref,quantity,unit:'each',role,condition:'always',quantity_status:quantity===null?'unresolved':'defined'});
 if(legacyBOM)for(const r of [...devices,...editions,...pc.products])for(const h of r.composition_history||[]){
  const id=h.legacy_assembly_ref||r.id;
  if(assemblies.has(id))continue;
  const a={id,name:r.name,status:'incomplete',requirements:[],routing:{operations:[],minutes_per_unit:null,first_pass_yield:null,rework_rate:null,scrap_rate:null,fixture_refs:[]},cost_rollup_status:'blocked_pending_component_and_routing_definition',...clone(h.bom_assembly_metadata||{}),lines:clone(h.composition_definition).filter(l=>!l.ref.startsWith('service.')).map(l=>Object.fromEntries(['ref','quantity','unit','role','condition','quantity_status'].map(k=>[k,l[k]])))};
  assemblies.set(id,a);if(!devices.includes(r))stored.push(a);
 }
 function softwareFor(p){const refs=new Set();const walk=id=>{const d=records[id];for(const s of d?.software_refs||[])refs.add(s);for(const l of d?.bom_assembly_definition||[])if(records[l.ref]?.bom_assembly_definition)walk(l.ref);};if(p.main_product)walk(p.main_product.device_ref);for(const e of p.connected_devices||[])walk(e.device_ref);for(const e of p.attached_products||[]){if(e.software_ref)refs.add(e.software_ref);else if(e.product_ref)walk(e.product_ref);}return [...refs];}
 function legacyOffer(p){
  const o=clone(p);o.bom_assembly_ref=p.hardware_assembly_ref;
  o.included_devices=(p.connected_devices||[]).map(e=>e.device_ref);o.included_software=softwareFor(p);o.included_services=(p.attached_products||[]).filter(e=>e.service_ref);
  o.manufacturing_variants=(p.revisions||[]).filter(v=>v.hardware_assembly_ref).map(v=>({effective_from:v.effective_from,assembly_ref:v.hardware_assembly_ref}));
  const ram=(p.connected_devices||[]).filter(e=>records[e.device_ref]?.category==='memory_expansion');
  if(p.main_product&&ram.length){const e=ram[0],spec=records[e.device_ref].specification;o.computer_configuration={ram_kb:ram.reduce((n,e)=>n+e.quantity*records[e.device_ref].specification.capacity_kb,0),module_ref:e.device_ref,populated_modules:e.quantity,populated_banks:e.quantity/2};}
  return o;
 }
 const computers=platforms.map(p=>{
  const c={...clone(p),...resolve(p.technical_profile)},ch=records[p.chassis_ref],familyLine=['Aurelia','Artemis','Athena'].find(x=>ch.id.includes(x.toLowerCase())),slots=ch.expansion_socket_groups.flatMap(g=>g.sockets);
  const offerings=pc.products.filter(x=>x.computer_ref===p.id&&x.composition_history?.length);
  const configurations=offerings.flatMap(x=>{const h=x.composition_history[0],ram=h.composition_definition.find(l=>records[l.ref]?.category==='memory_expansion'),s=records[ram?.ref]?.specification;if(!ram||!s)return [];return [{id:x.id,product_ref:x.id,shipping_configuration:true,module_ref:ram.ref,populated_modules:ram.quantity,populated_banks:ram.quantity/2,ram_kb:ram.quantity*s.capacity_kb,data_chip_count:ram.quantity*s.chips,bank_population:Array.from({length:ram.quantity/2},(_,i)=>({bank:i,slots:[2*i,2*i+1]}))}];});
  const base={lines:offerings[0]?.composition_history[0].composition_definition||[]};
  const mem=c.memory||{};const fixed=records['device.subsystem.'+p.id.slice(9)+'.base_memory'];if(mem.physical_population&&fixed){const l=fixed.bom_assembly_definition.find(l=>records[l.ref]?.category==='memory_ic');if(l)Object.assign(mem.physical_population,{chip_ref:l.ref,data_chip_count:l.quantity,data_ram_kb:fixed.specification.capacity_kb});}if(configurations.length){mem.configurations=configurations;mem.default_configuration=configurations.find(x=>x.id===p.default_configuration)?.id||configurations[0].id;mem.module_refs=slots.find(s=>s.id==='ram')?.compatible_device_refs||[];}
  const selected=configurations.find(x=>x.id===mem.default_configuration);mem.ram_kb=selected?.ram_kb||records['device.subsystem.'+p.id.slice(9)+'.base_memory']?.specification.capacity_kb||0;
  mem.video_ram_kb=c.video?.video_ram_kb||c.video?.display_memory?.capacity_bytes/1024||16;mem.sprite_ram_kb=1;mem.sprite_sram_kb=1;
  if(c.video)c.video.card_ref=c.video.controller_ref&&familyLine!=='Aurelia'?p.technical_profile.video.source_ref:undefined;
  c.memory=mem;c.storage={};
  for(const l of base?.lines||[]){const d=records[l.ref];if(!d)continue;if(['floppy_drive_mechanism','hard_disk_drive'].includes(d.category)){const key=d.category==='hard_disk_drive'?'internal_hdd':'internal_fdd';c.storage[key]={...clone(d.specification||{}),count:l.quantity};}}
  c.storage.hdd_included=Boolean(c.storage.internal_hdd);
  const ctrl=ch.bom_assembly_definition.find(l=>records[l.ref]?.category==='io_controller_ic'&&l.ref.includes('fdd'))?.ref;if(ctrl)c.storage.controller_ref=ctrl;
  c.chipset=ch.bom_assembly_definition.filter(l=>l.ref.startsWith('part.')&&/controller|mmu|dma/.test(l.ref)).map(l=>l.ref);
  if(p.recommended_software_ref){c.operating_system_ref=p.recommended_software_ref;if(c.rom_and_cartridges)c.rom_and_cartridges.system_cartridge_ref=p.recommended_software_ref;}
  c.bom_assembly_refs=[ch.id];c.manufacturing_status=ch.manufacturing_status;c.manufacturing_requirements=ch.bom_assembly_metadata.requirements;
  c.compatible_devices=[...new Set(slots.flatMap(s=>s.compatible_device_refs))];
  c.compatible_software=docs['data/software-editions.json'].platform_editions.filter(e=>(e.platform_support||[]).some(s=>s.computer_ref===p.id)).map(e=>e.id);
  c.default_video_card_ref=familyLine==='Aurelia'?undefined:p.technical_profile.video.source_ref;
  if(familyLine==='Athena')c.graphics_card_ref=c.default_video_card_ref;
  c.video_variants=[];c.configuration_video_card_refs={};
  for(const cfg of configurations){const a={lines:records[cfg.product_ref]?.composition_history[0].composition_definition||base.lines};const card=a?.lines.find(l=>records[l.ref]?.category==='video_expansion_card');if(card){c.configuration_video_card_refs[cfg.id]=card.ref;let v=c.video_variants.find(v=>v.card_ref===card.ref);if(!v){v={card_ref:card.ref,configuration_ids:[],specification:{...clone(records[card.ref].specification),card_ref:card.ref}};c.video_variants.push(v);}v.configuration_ids.push(cfg.id);}}
  for(const k of ['network','networking','networking_from_ncc_1981'])if(c[k]){c[k].adapter_ref='device.network_card_'+(familyLine==='Aurelia'?'aurelia':'artemis');c[k].included_by_default=p.id==='computer.artemis_pro';if(k==='network'){c[k].card_ref=c[k].adapter_ref;c[k].card_count=(base?.lines||[]).filter(l=>l.ref===c[k].card_ref).reduce((n,l)=>n+l.quantity,0);c[k].included=c[k].card_count>0;}}
  delete c.technical_profile;return c;
 });
 docs['data/computers.json']={computers,external_platforms:pc.external_platforms};
 const commercialGroup=p=>p.category==='software'?'commercial_offerings':'offered_bundles';
 docs['data/offers.json']=Object.fromEntries(['offered_bundles','proposed_bundles','commercial_offerings'].map(k=>[k,pc.products.filter(p=>commercialGroup(p)===k).map(legacyOffer)]));
 const mappings=[...computers.map(c=>({catalog_ref:c.id,production_status:c.production_status||'design_baseline',assembly_refs:c.bom_assembly_refs,requirements:c.manufacturing_requirements})),...devices.filter(d=>d.hardware_assembly_refs).map(d=>({catalog_ref:d.id,production_status:d.production_status,assembly_refs:d.hardware_assembly_refs,requirements:d.manufacturing_requirements||[]})),...parts.filter(p=>p.production_status).map(p=>({catalog_ref:p.id,production_status:p.production_status,assembly_refs:p.bom_role==='material'&&p.production_status!=='excluded'?[p.id]:[],requirements:p.requirements||[]}))];
 docs['data/product-boms.json']={...clone(pc.bom_policy),products:mappings,offers:pc.products.filter(p=>commercialGroup(p)==='offered_bundles').map(p=>({catalog_ref:p.id,kind:p.category,assembly_ref:p.hardware_assembly_ref||p.id,compatible_host_ref:p.computer_ref,included_host:Boolean(p.main_product),effective_from:p.composition_history[0].valid_from,requirements:p.acceptance||[],licenses_and_services:'Tracked outside recurring hardware BOM; physical media remains included.'})),proposed_offer_refs:pc.products.filter(p=>commercialGroup(p)==='proposed_bundles').map(p=>p.id)};
 const retail=clone(pc.catalog_editions[0]);for(const key of ['solutions','upgrades'])retail[key]=retail[key].map(e=>{const p=records[e.product_ref],r=p.retail_presentation;return {...clone(r),components:r.component_product_ref?[{ref:r.component_product_ref,quantity:1}]:(p.attached_products||[]).map(e=>({ref:e.product_ref||e.software_ref||e.service_ref,quantity:e.quantity}))};});
 docs['data/retail-catalog.json']={retail_catalog_1982:retail};
 return docs;
}
const api={project};if(typeof module!=='undefined')module.exports=api;root.CatalogModel=api;
if(typeof require!=='undefined'&&require.main===module){let s='';process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>(()=>{const request=JSON.parse(s);process.stdout.write(JSON.stringify(project(request.documents||request,{legacyBOM:request.legacyBOM===true})));})());}
})(typeof window==='undefined'?globalThis:window);

/* Authoritative collection loader. Compatibility shapes are transient, never files. */
(function(root){'use strict';
const node=typeof module!=='undefined'&&module.exports;
function nameFor(path,registry){path=String(path).replace(/^\.\//,'');path=registry.legacy_paths[path]||path;const name=path.startsWith('catalog:')?path.slice(8):path.split('/').pop().replace(/\.json$/,'');return (path.startsWith('catalog:')||path.startsWith('generated/catalogs/'))&&registry.views[name]?name:null;}
function normalizeComponentIds(value,registry){
 const aliases={...registry.component_id_aliases,...registry.device_assembly_aliases,...registry.record_id_aliases},families=registry.device_family_aliases||{};
 function visit(v){
  if(typeof v==='string')return aliases[v]|| (v.includes('|')?v.split('|').map(p=>aliases[p]||p).join('|'):v);
  if(Array.isArray(v))return v.map(visit);
  if(v&&typeof v==='object'){const out={};for(const [k,x] of Object.entries(v)){const key=visit(k);if(Object.hasOwn(out,key))throw Error('Component identifier collision: '+key);out[key]=visit(x);}if(registry.record_family_aliases?.[out.catalog_ref])out.historical_variant_refs=registry.record_family_aliases[out.catalog_ref];if(families[out.catalog_ref]?.includes(out.id))out.catalog_ref=out.id;return out;}
  return v;
 }
 return visit(value);
}
function assemblyRecords(stored,devices){
 const clone=x=>JSON.parse(JSON.stringify(x));const rows=[...clone(stored),...devices.filter(d=>Object.hasOwn(d,'bom_assembly_definition')).map(d=>({id:d.id,...clone(d.bom_assembly_metadata),lines:clone(d.bom_assembly_definition)}))];
 if(new Set(rows.map(r=>r.id)).size!==rows.length)throw Error('Duplicate device/assembly BOM identity');return rows;
}
function computerRecords(stored,devices,components){
 const clone=x=>JSON.parse(JSON.stringify(x)),ds=new Map(devices.map(d=>[d.id,d])),ps=new Map(components.map(p=>[p.id,p]));
 return stored.map(row=>{const c=clone(row),ch=ds.get(c.chassis_ref);for(const key of ['processor','form_factor','io_and_expansion'])c[key]=clone(ch[key]);const cpu=ps.get(c.processor.part_ref);c.processor.variant=cpu.name;c.processor.clock_mhz=cpu.specification.clock_mhz;
 const slots=Object.fromEntries(ch.expansion_socket_groups.flatMap(g=>g.sockets).map(s=>[s.id,s])),io=c.io_and_expansion;
 if(slots.flexibus)io.flexibus_ports=slots.flexibus.capacity;if(io.expansion_slots)io.expansion_slots.count=slots.expansion.capacity;else io.general_expansion_slot_count=slots.expansion.capacity;
 if(io.dedicated_video_slot)io.dedicated_video_slot.count=slots.video_card.capacity;else if(slots.video_card)io.graphics_card_count=slots.video_card.capacity;
 if(c.rom_and_cartridges)c.rom_and_cartridges={xip_slots:Object.values(slots).filter(s=>s.connection==='rom_cartridge').reduce((n,s)=>n+s.capacity,0),...c.rom_and_cartridges};
 if(io.rom_eeprom_cartridge_slots)io.rom_eeprom_cartridge_slots.count=Object.values(slots).filter(s=>s.connection==='rom_cartridge').reduce((n,s)=>n+s.capacity,0);
 if(slots.ram){const ram=slots.ram,mem=c.memory;mem.ram_sockets=ram.capacity;mem.modules_per_bank=ram.installation_multiple;if(ram.capacity!==null){mem.bank_count=ram.capacity/ram.installation_multiple;mem.physical_capacity_limit_kb=ch.memory_constraints.max_ram_kib;mem.capacity_limit_status=ch.memory_constraints.qualification_status;mem.mixed_density_allowed=ch.memory_constraints.mixed_module_types_allowed;}else mem.maximum_ram_kb=ch.memory_constraints.max_ram_kib;}
 const slot=c.io_and_expansion.dedicated_video_slot||{};if(c.default_video_card_ref)slot.included_card_ref=c.default_video_card_ref;if(c.configuration_video_card_refs)slot.configuration_card_refs=c.configuration_video_card_refs;return c;});
}
function assemble(name,registry,collections){
 if(collections['data/product-catalog.json'])collections=root.CatalogModel.project(collections,{legacyBOM:name==='hardware-bom'});
 const recipe=registry.views[name],clone=x=>JSON.parse(JSON.stringify(x)),select=r=>r.wrap?{products:clone(collections[r.file][r.key])}:r.chassis_file?computerRecords(collections[r.file][r.key],collections[r.chassis_file].devices,collections['data/components.json'].components):r.device_file?assemblyRecords(collections[r.file][r.key],collections[r.device_file].devices):clone(collections[r.file][r.key]);
 if(recipe.story){const world=collections['data/world.json'],structure=collections['data/timeline-structure.json'],events=new Map(collections['data/events.json'].events.map(e=>[e.id,e])),contracts=collections['data/contracts.json'];return {assumptions:Object.fromEntries(['scenario','entities','principles','conventions'].map(k=>[k,clone(world[k])])),phases:structure.phases.map(phase=>{const p=clone(phase),ids=p.event_refs;delete p.event_refs;p.events=ids.map(id=>{if(!events.has(id))throw Error('Missing event '+id);const e=clone(events.get(id));if(e.agreement_ref){e.agreement_terms=clone(contracts[e.agreement_ref]);delete e.agreement_ref;}return e;});return p;}),processes:clone(structure.processes)};}
 if(recipe.merge){const result={};for(const ref of recipe.merge){const part=select(ref);for(const k of Object.keys(part))if(Object.hasOwn(result,k))throw Error('Overlapping field ownership: '+name);Object.assign(result,part);}return result;}
 return Object.fromEntries(Object.entries(recipe).map(([k,r])=>[k,select(r)]));
}
function filesFor(name,reg){
 const r=reg.views[name];if(r.story)return ['data/world.json','data/timeline-structure.json','data/events.json','data/contracts.json'];
 const files=(r.merge||Object.values(r)).flatMap(x=>[x.file,...(x.device_file?[x.device_file]:[]),...(x.chassis_file?[x.chassis_file,'data/components.json']:[])]);
 return [...new Set(files.filter(f=>!['data/computers.json','data/offers.json','data/product-boms.json','data/retail-catalog.json','data/software-products.json'].includes(f)).concat((reg.commercial_projection_files||[]).filter(f=>f!=='data/retired_assemblies.json')))];
}
if(node){const fs=require('node:fs'),path=require('node:path');function read(file,base=__dirname){const reg=JSON.parse(fs.readFileSync(path.join(base,'schemas/data-registry.json'),'utf8')),name=nameFor(file,reg);if(!name){const actual=reg.legacy_paths[file]||file,value=JSON.parse(fs.readFileSync(path.join(base,actual),'utf8'));return actual.startsWith('generated/models/')?normalizeComponentIds(value,reg):value;}const collections=Object.fromEntries(filesFor(name,reg).map(p=>[p,JSON.parse(fs.readFileSync(path.join(base,p),'utf8'))]));return assemble(name,reg,collections);}module.exports={read,assemble,filesFor,nameFor,normalizeComponentIds,assemblyRecords,computerRecords};return;}
const cache=new Map();function json(path){if(!cache.has(path))cache.set(path,root.fetch(path).then(r=>{if(!r.ok)throw Error('Unable to load '+path);return r.json();}).catch(e=>{cache.delete(path);throw e;}));return cache.get(path);}
async function fetchData(path,options){if(String(path).replace(/^\.\//,'').startsWith('generated/models/')){const [response,reg]=await Promise.all([root.fetch(path,options),json('schemas/data-registry.json')]);return {ok:response.ok,status:response.status,json:async()=>normalizeComponentIds(await response.json(),reg)};}if(!String(path).replace(/^\.\//,'').startsWith('generated/catalogs/')&&!String(path).startsWith('catalog:'))return root.fetch(path,options);const reg=await json('schemas/data-registry.json'),name=nameFor(path,reg);if(!name)return root.fetch(path,options);const files=filesFor(name,reg),values=await Promise.all(files.map(json));return {ok:true,status:200,json:async()=>assemble(name,reg,Object.fromEntries(files.map((p,i)=>[p,values[i]])))};}
root.DataStore={compositionAlias:async id=>(await json('schemas/data-registry.json')).composition_aliases?.[id],fetch:fetchData,assemble,filesFor,nameFor,normalizeComponentIds,assemblyRecords,computerRecords,resolveComponentId:async id=>{const reg=await json('schemas/data-registry.json');return reg.component_id_aliases?.[id]||reg.device_assembly_aliases?.[id]||reg.record_id_aliases?.[id]||id;},deviceFamily:async id=>{const reg=await json('schemas/data-registry.json');return reg.device_family_aliases?.[id]||reg.record_family_aliases?.[id]||[];}};
})(typeof window==='undefined'?globalThis:window);

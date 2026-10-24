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
 const recipe=registry.views[name],clone=x=>JSON.parse(JSON.stringify(x)),select=r=>r.chassis_file?computerRecords(collections[r.file][r.key],collections[r.chassis_file].devices,collections['data/components.json'].components):r.device_file?assemblyRecords(collections[r.file][r.key],collections[r.device_file].devices):clone(collections[r.file][r.key]);
 if(recipe.story){const world=collections['data/world.json'],structure=collections['data/timeline-structure.json'],events=new Map(collections['data/events.json'].events.map(e=>[e.id,e])),contracts=collections['data/contracts.json'];return {assumptions:Object.fromEntries(['scenario','entities','principles','conventions'].map(k=>[k,clone(world[k])])),phases:structure.phases.map(phase=>{const p=clone(phase),ids=p.event_refs;delete p.event_refs;p.events=ids.map(id=>{if(!events.has(id))throw Error('Missing event '+id);const e=clone(events.get(id));if(e.agreement_ref){e.agreement_terms=clone(contracts[e.agreement_ref]);delete e.agreement_ref;}return e;});return p;}),processes:clone(structure.processes)};}
 if(recipe.merge){const result={};for(const ref of recipe.merge){const part=select(ref);for(const k of Object.keys(part))if(Object.hasOwn(result,k))throw Error('Overlapping field ownership: '+name);Object.assign(result,part);}return result;}
 return Object.fromEntries(Object.entries(recipe).map(([k,r])=>[k,select(r)]));
}
function filesFor(name,reg){const r=reg.views[name];return r.story?['data/world.json','data/timeline-structure.json','data/events.json','data/contracts.json']:[...new Set((r.merge||Object.values(r)).flatMap(x=>[x.file,...(x.device_file?[x.device_file]:[]),...(x.chassis_file?[x.chassis_file,'data/components.json']:[])]))];}
if(node){const fs=require('node:fs'),path=require('node:path');function read(file,base=__dirname){const reg=JSON.parse(fs.readFileSync(path.join(base,'schemas/data-registry.json'),'utf8')),name=nameFor(file,reg);if(!name){const actual=reg.legacy_paths[file]||file,value=JSON.parse(fs.readFileSync(path.join(base,actual),'utf8'));return actual.startsWith('generated/models/')?normalizeComponentIds(value,reg):value;}const collections=Object.fromEntries(filesFor(name,reg).map(p=>[p,JSON.parse(fs.readFileSync(path.join(base,p),'utf8'))]));return assemble(name,reg,collections);}module.exports={read,assemble,filesFor,nameFor,normalizeComponentIds,assemblyRecords,computerRecords};return;}
const cache=new Map();function json(path){if(!cache.has(path))cache.set(path,root.fetch(path).then(r=>{if(!r.ok)throw Error('Unable to load '+path);return r.json();}).catch(e=>{cache.delete(path);throw e;}));return cache.get(path);}
async function fetchData(path,options){if(String(path).replace(/^\.\//,'').startsWith('generated/models/')){const [response,reg]=await Promise.all([root.fetch(path,options),json('schemas/data-registry.json')]);return {ok:response.ok,status:response.status,json:async()=>normalizeComponentIds(await response.json(),reg)};}if(!String(path).replace(/^\.\//,'').startsWith('generated/catalogs/')&&!String(path).startsWith('catalog:'))return root.fetch(path,options);const reg=await json('schemas/data-registry.json'),name=nameFor(path,reg);if(!name)return root.fetch(path,options);const files=filesFor(name,reg),values=await Promise.all(files.map(json));return {ok:true,status:200,json:async()=>assemble(name,reg,Object.fromEntries(files.map((p,i)=>[p,values[i]])))};}
root.DataStore={fetch:fetchData,assemble,filesFor,nameFor,normalizeComponentIds,assemblyRecords,computerRecords,resolveComponentId:async id=>{const reg=await json('schemas/data-registry.json');return reg.component_id_aliases?.[id]||reg.device_assembly_aliases?.[id]||reg.record_id_aliases?.[id]||id;},deviceFamily:async id=>{const reg=await json('schemas/data-registry.json');return reg.device_family_aliases?.[id]||reg.record_family_aliases?.[id]||[];}};
})(typeof window==='undefined'?globalThis:window);

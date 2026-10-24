/* Authoritative collection loader. Compatibility shapes are transient, never files. */
(function(root){'use strict';
const node=typeof module!=='undefined'&&module.exports;
function nameFor(path,registry){path=String(path).replace(/^\.\//,'');path=registry.legacy_paths[path]||path;const name=path.startsWith('catalog:')?path.slice(8):path.split('/').pop().replace(/\.json$/,'');return (path.startsWith('catalog:')||path.startsWith('generated/catalogs/'))&&registry.views[name]?name:null;}
function normalizeComponentIds(value,registry){
 const aliases={...registry.component_id_aliases,...registry.device_assembly_aliases},families=registry.device_family_aliases||{};
 function visit(v){
  if(typeof v==='string')return aliases[v]|| (v.includes('|')?v.split('|').map(p=>aliases[p]||p).join('|'):v);
  if(Array.isArray(v))return v.map(visit);
  if(v&&typeof v==='object'){const out={};for(const [k,x] of Object.entries(v)){const key=visit(k);if(Object.hasOwn(out,key))throw Error('Component identifier collision: '+key);out[key]=visit(x);}if(families[out.catalog_ref]?.includes(out.id))out.catalog_ref=out.id;return out;}
  return v;
 }
 return visit(value);
}
function assemblyRecords(stored,devices){
 const clone=x=>JSON.parse(JSON.stringify(x));const rows=[...clone(stored),...devices.filter(d=>Object.hasOwn(d,'bom_assembly_definition')).map(d=>({id:d.id,...clone(d.bom_assembly_metadata),lines:clone(d.bom_assembly_definition)}))];
 if(new Set(rows.map(r=>r.id)).size!==rows.length)throw Error('Duplicate device/assembly BOM identity');return rows;
}
function assemble(name,registry,collections){
 const recipe=registry.views[name],clone=x=>JSON.parse(JSON.stringify(x)),select=r=>r.device_file?assemblyRecords(collections[r.file][r.key],collections[r.device_file].devices):clone(collections[r.file][r.key]);
 if(recipe.story){const world=collections['data/world.json'],structure=collections['data/timeline-structure.json'],events=new Map(collections['data/events.json'].events.map(e=>[e.id,e])),contracts=collections['data/contracts.json'];return {assumptions:Object.fromEntries(['scenario','entities','principles','conventions'].map(k=>[k,clone(world[k])])),phases:structure.phases.map(phase=>{const p=clone(phase),ids=p.event_refs;delete p.event_refs;p.events=ids.map(id=>{if(!events.has(id))throw Error('Missing event '+id);const e=clone(events.get(id));if(e.agreement_ref){e.agreement_terms=clone(contracts[e.agreement_ref]);delete e.agreement_ref;}return e;});return p;}),processes:clone(structure.processes)};}
 if(recipe.merge){const result={};for(const ref of recipe.merge){const part=select(ref);for(const k of Object.keys(part))if(Object.hasOwn(result,k))throw Error('Overlapping field ownership: '+name);Object.assign(result,part);}return result;}
 return Object.fromEntries(Object.entries(recipe).map(([k,r])=>[k,select(r)]));
}
function filesFor(name,reg){const r=reg.views[name];return r.story?['data/world.json','data/timeline-structure.json','data/events.json','data/contracts.json']:[...new Set((r.merge||Object.values(r)).flatMap(x=>[x.file,...(x.device_file?[x.device_file]:[])]))];}
if(node){const fs=require('node:fs'),path=require('node:path');function read(file,base=__dirname){const reg=JSON.parse(fs.readFileSync(path.join(base,'schemas/data-registry.json'),'utf8')),name=nameFor(file,reg);if(!name){const actual=reg.legacy_paths[file]||file,value=JSON.parse(fs.readFileSync(path.join(base,actual),'utf8'));return actual.startsWith('generated/models/')?normalizeComponentIds(value,reg):value;}const collections=Object.fromEntries(filesFor(name,reg).map(p=>[p,JSON.parse(fs.readFileSync(path.join(base,p),'utf8'))]));return assemble(name,reg,collections);}module.exports={read,assemble,filesFor,nameFor,normalizeComponentIds,assemblyRecords};return;}
const cache=new Map();function json(path){if(!cache.has(path))cache.set(path,root.fetch(path).then(r=>{if(!r.ok)throw Error('Unable to load '+path);return r.json();}).catch(e=>{cache.delete(path);throw e;}));return cache.get(path);}
async function fetchData(path,options){if(String(path).replace(/^\.\//,'').startsWith('generated/models/')){const [response,reg]=await Promise.all([root.fetch(path,options),json('schemas/data-registry.json')]);return {ok:response.ok,status:response.status,json:async()=>normalizeComponentIds(await response.json(),reg)};}if(!String(path).replace(/^\.\//,'').startsWith('generated/catalogs/')&&!String(path).startsWith('catalog:'))return root.fetch(path,options);const reg=await json('schemas/data-registry.json'),name=nameFor(path,reg);if(!name)return root.fetch(path,options);const files=filesFor(name,reg),values=await Promise.all(files.map(json));return {ok:true,status:200,json:async()=>assemble(name,reg,Object.fromEntries(files.map((p,i)=>[p,values[i]])))};}
root.DataStore={fetch:fetchData,assemble,filesFor,nameFor,normalizeComponentIds,assemblyRecords,resolveComponentId:async id=>{const reg=await json('schemas/data-registry.json');return reg.component_id_aliases?.[id]||reg.device_assembly_aliases?.[id]||id;},deviceFamily:async id=>(await json('schemas/data-registry.json')).device_family_aliases?.[id]||[]};
})(typeof window==='undefined'?globalThis:window);

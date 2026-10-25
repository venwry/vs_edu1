const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const store=require('../data-store.js'),root=path.resolve(__dirname,'..'),reg=store.read('schemas/data-registry.json');
const components=store.read('data/components.json').components,catalog=store.read('catalog:logix-aion-technical-catalog-v2'),bom=store.read('catalog:hardware-bom');
assert.deepEqual(catalog.components,components);assert.deepEqual(bom.components,components);
assert.equal(components.length,347);assert.equal(new Set(components.map(x=>x.id)).size,347);
assert(!('base_parts' in catalog));assert(!('components' in store.read('data/sourcing.json')));
const z=components.find(x=>x.id==='part.z80a');assert(z.specification.clock_mhz===4&&z.vendor==='Zilog'&&z.manufacturer==='Zilog');assert.equal(z.qualification_status,'unresolved');
const hdd=components.find(x=>x.id==='part.hdd_5mb');assert.equal(hdd.manufacturer_part_number,'ST506');
const video=components.find(x=>x.id==='part.artemis_graphics_chip');assert(video.alternate_names.includes('Artemis custom graphics chip'));assert(!video.requirements.some(x=>x.includes('Clarify that 16 KiB')));
for(const r of components)for(const key of ['catalog_ref','unit_cost','currency','quote_date','quantity_tier','manufacturing_requirements'])assert(!Object.hasOwn(r,key));
const raw=JSON.parse(fs.readFileSync(path.join(root,'generated/models/manufacturing-costs.json'))),normalized=store.read('generated/models/manufacturing-costs.json');
assert(raw.component_cost_assumptions['bompart.part.z80a']);assert(normalized.component_cost_assumptions['part.z80a']);assert(!normalized.component_cost_assumptions['bompart.part.z80a']);
assert.deepEqual(store.normalizeComponentIds(normalized,reg),normalized);
assert.throws(()=>store.normalizeComponentIds({'bompart.part.z80a':1,'part.z80a':2},reg),/collision/);
const numbers=x=>typeof x==='number'?[x]:x&&typeof x==='object'?Object.values(x).flatMap(numbers):[];assert.deepEqual(numbers(raw),numbers(normalized));
(async()=>{
 const requested=[],context={fetch:async p=>{requested.push(p);return {ok:true,status:200,json:async()=>JSON.parse(fs.readFileSync(path.join(root,p)))}}};vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(root,'data-store.js'),'utf8'),context);
 assert.equal(await context.DataStore.resolveComponentId('bompart.part.z80a'),'part.z80a');
 assert.equal(await context.DataStore.resolveComponentId('bompart.device.flexidisk.drive_psu'),'part.device.flexidisk.drive_psu');
 const response=await context.DataStore.fetch('generated/models/manufacturing-costs.json');assert.equal(JSON.stringify(await response.json()),JSON.stringify(normalized));
 assert.equal(requested.filter(p=>p==='schemas/data-registry.json').length,1);
 const model=require('../bom-details.js').createModel(catalog,bom,normalized);assert.equal(model.items.length,['components','devices','computers','software_products','platform_editions','external_partner_products','offered_bundles','proposed_bundles','commercial_offerings'].reduce((n,k)=>n+catalog[k].length,0));assert(model.rows('part.z80a').some(r=>r.ref==='part.z80a'));
 globalThis.renderSpecification=x=>JSON.stringify(x);const costHtml=model.renderCosts('part.z80a',{fullRecords:true});assert(costHtml.includes('Component cost assumptions by year'));assert(costHtml.includes(JSON.stringify(normalized.component_cost_assumptions['part.z80a'])));delete globalThis.renderSpecification;
 console.log('PASS: single identity/schema, combined fields, archived-map normalization, collision rejection, raw browser reads and alias caching');
})().catch(e=>{console.error(e);process.exitCode=1});

// Removed wrappers resolve directly to component material records, including archived costs.
const simpleStore=require('../data-store.js'),simpleBom=simpleStore.read('catalog:hardware-bom'),simpleCatalog=simpleStore.read('catalog:logix-aion-technical-catalog-v2'),simpleCosts=simpleStore.read('generated/models/manufacturing-costs.json');
assert(!simpleBom.assemblies.some(a=>a.id.startsWith('assembly.part.')));
for(const a of simpleBom.assemblies.filter(a=>a.id.startsWith('assembly.computer.')))assert(a.lines.every(l=>/^(part|device)\./.test(l.ref)));
const simpleModel=require('../bom-details.js').createModel(simpleCatalog,simpleBom,simpleCosts);
assert.deepEqual(simpleModel.assemblyIds('part.z80a'),['part.z80a']);assert.equal(simpleModel.rows('part.z80a').length,1);
assert(simpleCatalog.components.find(p=>p.id==='part.z80a').cost_rollup_status);
assert(simpleCosts.products.some(p=>p.assembly_ref==='part.aion_2114'));

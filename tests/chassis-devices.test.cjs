const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),{JSDOM,VirtualConsole}=require('jsdom');
const root=path.resolve(__dirname,'..'),store=require('../data-store.js'),read=p=>fs.readFileSync(path.join(root,p),'utf8');
const c=store.read('catalog:logix-aion-technical-catalog-v2'),b=store.read('catalog:hardware-bom'),cost=store.read('generated/models/manufacturing-costs.json'),{createFamilyModel}=require('../artemis-configurator.js');
const by=Object.fromEntries([...c.devices,...c.components].map(r=>[r.id,r]));
assert.deepEqual(c.components.filter(r=>/^part\.(erav1|era2)_/.test(r.id)).map(r=>r.name),['ERAv1 6MHz (initial)','ERAv1 8MHz (upgraded)','ERA^2 12MHz','ERA^2 16MHz rev2']);
assert(!c.components.some(p=>p.variants||p.category==='memory_module'));
for(const p of c.platform_editions)for(const ref of p.physical_media_refs||[]){assert.equal(by[ref].category,'rom_cartridge');assert(by[ref].software_refs.includes(p.id));}
assert.equal(c.devices.filter(d=>d.category==='computer_chassis').length,6);
const am=createFamilyModel(c,b,cost,'aurelia'),base=am.options.find(o=>o.id==='computer.aurelia');assert(!am.state(base,am.revisions(base)[0],base.available).software.includes('software.cpm_aurelia'));
for(const family of ['aurelia','artemis','athena']){
 const model=createFamilyModel(c,b,cost,family);assert.equal(model.options.filter(o=>o.chassis).length,2);
 for(const o of model.options.filter(o=>o.chassis)){const r=model.revisions(o)[0],s=model.state(o,r,r.from);assert.equal(model.assessments(o,r).length,0);assert(!s.network&&!s.primary);assert.equal(s.ram.ram_kb,family==='aurelia'?(o.id.endsWith('_plus')?64:48):0);assert(!s.tree.assemblyRefs.some(id=>by[id]?.category==='rom_cartridge'||by[id]?.category==='memory_expansion'));}
}
(async()=>{
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
 async function boot(file,query){const dom=new JSDOM(read(file),{url:'https://atlas.test/'+file+query,runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:vc}),w=dom.window;w.fetch=async p=>({ok:true,json:async()=>store.read(p)});w.IntersectionObserver=class{observe(){}disconnect(){}};for(const s of w.document.scripts)w.eval(s.src?read(new URL(s.src).pathname.slice(1)):s.textContent);for(let i=0;i<100&&!w.document.querySelector('[data-ready]');i++)await new Promise(r=>setTimeout(r,10));return dom;}
 for(const family of ['aurelia','artemis','athena']){
  const dom=await boot(family+'.html','?configuration=device.chassis.'+family),d=dom.window.document;
  assert.deepEqual([...d.querySelectorAll('#configuration-stats>div>span')].map(n=>n.textContent),['Processor','System RAM']);
  assert(d.getElementById('configuration-diagram').textContent.includes('Available sockets and compatibility'));assert.equal(d.querySelectorAll('[data-evaluation]').length,0);dom.window.close();
 }
 for(const [old,count] of [['part.era1',2],['part.era2',2],['bompart.part.era1',2]]){
  const dom=await boot('bom-navigator.html','?element='+old),d=dom.window.document;assert.equal(d.querySelectorAll('#bom-rows tr').length,count);assert(d.getElementById('bom-inspector').textContent.includes('Select a variant'));dom.window.close();
 }
 const model=require('../bom-details.js').createModel(c,b,cost);assert(model.renderCosts('part.erav1_8mhz').includes('not speed-bin-specific'));
 assert.deepEqual(errors,[]);console.log('PASS: six bare chassis, zero removable populations, four CPUs, physical cartridges, two summary fields and ambiguous legacy CPU links');
})().catch(e=>{console.error(e);process.exitCode=1;});

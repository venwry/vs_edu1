const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),{JSDOM,VirtualConsole}=require('jsdom');
const root=path.resolve(__dirname,'..'),store=require('../data-store.js'),read=p=>fs.readFileSync(path.join(root,p),'utf8');
const c=store.read('catalog:logix-aion-technical-catalog-v2'),b=store.read('catalog:hardware-bom'),cost=store.read('generated/models/manufacturing-costs.json'),{createFamilyModel}=require('../artemis-configurator.js');
const by=Object.fromEntries([...c.devices,...c.components].map(r=>[r.id,r]));
assert.deepEqual(c.components.filter(r=>/^part\.(erav1|era2)_/.test(r.id)).map(r=>r.name),['ERAv1 6MHz (initial)','ERAv1 8MHz (upgraded)','ERA^2 12MHz','ERA^2 16MHz rev2']);
assert(!c.components.some(p=>p.variants||p.category==='memory_module'));
for(const p of c.platform_editions)for(const ref of p.physical_media_refs||[]){assert.equal(by[ref].category,'rom_cartridge');assert(by[ref].software_refs.includes(p.id));}
assert.equal(c.devices.filter(d=>d.category==='base_computer').length,6);
for(const family of ['aurelia','artemis','athena']){
 const model=createFamilyModel(c,b,cost,family);assert.equal(model.options.length,{aurelia:4,artemis:8,athena:2}[family]);
 assert(!model.options.some(o=>o.chassis||o.target||o.combination));
 for(const ch of c.devices.filter(d=>d.category==='base_computer'))assert(!ch.bom_assembly_definition.some(l=>by[l.ref]&&['memory_expansion','rom_cartridge','video_expansion_card','network_interface_card','floppy_drive_mechanism','hard_disk_drive'].includes(by[l.ref].category)));
}
(async()=>{
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
 async function boot(file,query){const dom=new JSDOM(read(file),{url:'https://atlas.test/'+file+query,runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:vc}),w=dom.window;w.fetch=async p=>({ok:true,json:async()=>store.read(p)});w.IntersectionObserver=class{observe(){}disconnect(){}};for(const s of w.document.scripts)w.eval(s.src?read(new URL(s.src).pathname.slice(1)):s.textContent);for(let i=0;i<100&&!w.document.querySelector('[data-ready]');i++)await new Promise(r=>setTimeout(r,10));return dom;}
 for(const family of ['aurelia','artemis','athena']){
  const dom=await boot(family+'.html','?configuration=device.base_computer.'+family),d=dom.window.document;
  assert.deepEqual([...d.querySelectorAll('#configuration-stats>div>span')].map(n=>n.textContent),['Processor','System RAM']);
  const details=d.getElementById('configuration-tab-details'),bomTab=d.getElementById('configuration-tab-bom');
  assert.equal(details.textContent,'Details');assert.equal(bomTab.textContent,'Bill of materials');
  assert.equal(details.getAttribute('aria-selected'),'true');assert(d.getElementById('configuration-panel-bom').hidden);
  bomTab.click();assert.equal(bomTab.getAttribute('aria-selected'),'true');assert(d.getElementById('configuration-panel-details').hidden);assert(!d.getElementById('configuration-panel-bom').hidden);
  bomTab.dispatchEvent(new dom.window.KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}));assert.equal(details.getAttribute('aria-selected'),'true');assert.equal(d.activeElement,details);
  assert(d.querySelector('[data-component="chassis"]'));assert.equal(d.getElementById('artemis-configuration').options.length,{aurelia:4,artemis:8,athena:2}[family]);dom.window.close();
 }
 {
  const dom=await boot('bom-navigator.html','?element=assembly.part.z80a'),d=dom.window.document;
  assert(d.getElementById('bom-inspector').textContent.includes('Zilog Z80A'));
  d.getElementById('tab-bom').click();assert(d.getElementById('panel-bom').textContent.includes('terminal material item'));dom.window.close();
 }
 for(const [old,count] of [['part.era1',2],['part.era2',2],['bompart.part.era1',2]]){
  const dom=await boot('bom-navigator.html','?element='+old),d=dom.window.document;assert.equal(d.querySelectorAll('#bom-rows tr').length,count);assert(d.getElementById('bom-inspector').textContent.includes('Select a variant'));dom.window.close();
 }
 const model=require('../bom-details.js').createModel(c,b,cost);assert(model.renderCosts('part.erav1_8mhz').includes('not speed-bin-specific'));
 assert.deepEqual(errors,[]);console.log('PASS: six bare chassis, zero removable populations, four CPUs, physical cartridges, two summary fields and ambiguous legacy CPU links');
})().catch(e=>{console.error(e);process.exitCode=1;});

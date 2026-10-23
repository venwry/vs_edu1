const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {JSDOM,VirtualConsole}=require('jsdom'),root=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(root,p),'utf8'),json=p=>require('../data-store.js').read(p);
const catalog=json('generated/catalogs/logix-aion-technical-catalog-v2.json'),bom=json('generated/catalogs/hardware-bom.json'),cost=json('generated/models/manufacturing-costs.json');
const model=require('../bom-details.js').createModel(catalog,bom,cost);
for(const key of ['base_parts','devices','computers','software_products','platform_editions','offered_bundles','proposed_bundles','commercial_offerings'])for(const r of catalog[key]||[])assert(model.items.some(i=>i.id===r.id),'Missing '+r.id);
for(const c of bom.components)assert(model.items.some(i=>i.id===c.id||i.id===c.catalog_ref),'Missing manufacturing part '+c.id);
assert.equal(new Set(model.items.map(x=>x.id)).size,model.items.length);
assert.deepEqual(new Set(model.items.map(x=>x.class)),new Set(['Part','Peripheral','Computer','Expansion','Software','Software product','Software edition','Bundle']));
assert(model.items.filter(x=>x.id.startsWith('bundle.proposed_')).every(x=>x.release==='no release'));
assert.equal(model.items.filter(x=>x.release==='no release').length,12);
assert(model.items.every(x=>x.release),'Every navigator element has a date or explicit no release');
const {releaseDate,vendorName}=require('../bom-details.js');
assert.equal(releaseDate({}), ''); // Unknown is distinct from explicitly unused.
assert.equal(releaseDate({introduced:{event_name:'no release',event_start_date:null},available_from:'1980'}),'no release');
for(const [id,date] of [
 ['bompart.computer.aurelia.boot_rom_chips','1978-06-05'],
 ['bompart.part.artemis_ram_module_128kb.module_pcb','1980-05-19'],
 ['bompart.device.network_card_artemis.firmware_rom','1981-05-04'],
 ['bompart.device.mono_pro_17.highspeed_link_pcb','1982-06'],
 ['bompart.part.artemis_ram_module_32kb_x16.module_pcb','no release']
])assert.equal(model.items.find(x=>x.id===id).release,date,id);
for(const [id,vendor] of [
 ['bompart.computer.aurelia.boot_rom_chips','AION Labs'],
 ['bompart.device.flexibus_keyboard.scan_controller_and_firmware_storage','Logix'],
 ['bompart.computer.aurelia.psu','Logix'],
 ['bompart.computer.aurelia.525_inch_single_density_floppy_mechanism','Shugart Associates'],
 ['part.hdd_5mb','Seagate Technology'],
 ['software.product.cpm','Digital Research']
])assert.equal(vendorName(model.items.find(x=>x.id===id).record,model.records),vendor,id);
for(const id of ['computer.artemis','bundle.artemis_128_mono','device.artemis_video_card_64kb'])assert(model.assemblyIds(id).length,id+' has assemblies');
assert(model.rows(model.assemblyIds('bundle.artemis_128_mono')[0]).some(x=>x.depth>0));
assert(model.render('bompart.computer.artemis.boot_rom_chips').includes('Unknown'));
(async()=>{
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
 const dom=new JSDOM(read('bom-navigator.html'),{url:'https://atlas.test/bom-navigator.html?element=device.artemis_video_card_64kb',runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:vc}),w=dom.window,d=w.document;
 w.fetch=async p=>({ok:true,json:async()=>json(p)});for(const s of d.scripts)w.eval(read(new URL(s.src).pathname.slice(1)));
 for(let i=0;i<60&&!d.querySelector('main[data-ready]');i++)await new Promise(r=>setTimeout(r,10));
 assert(d.querySelector('main[data-ready]'));assert.equal(d.querySelectorAll('#bom-rows tr').length,model.items.length);assert(d.querySelector('[data-element="device.artemis_video_card_64kb"][aria-pressed=true]'));assert.equal(d.querySelectorAll('[role=tab]').length,4);
 assert.equal(d.querySelector('[role=tab][aria-selected=true]').textContent,'Details');
 d.getElementById('tab-bom').click();assert(!d.getElementById('panel-bom').hidden);assert(d.getElementById('panel-bom').textContent.includes('Bill of materials'));
 d.getElementById('tab-costs').click();assert(d.getElementById('panel-costs').textContent.includes('1982-06-15'));assert(d.getElementById('panel-costs').textContent.includes('ncc-1982'));
 d.getElementById('tab-costs').dispatchEvent(new w.KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));assert.equal(d.activeElement.id,'tab-events');assert(!d.getElementById('panel-events').hidden);assert(d.querySelector('#panel-events a[href^="timeline.html#"]'));
 d.querySelector('[data-element="offer.comdex82_artemis_autocad"]').click();d.getElementById('tab-costs').click();assert(d.getElementById('panel-costs').textContent.includes('Unknown'));assert(d.getElementById('panel-costs').textContent.includes('1982-11-29'));
 d.getElementById('tab-costs').dispatchEvent(new w.KeyboardEvent('keydown',{key:'Home',bubbles:true}));assert.equal(d.activeElement.id,'tab-details');

 const change=(id,value)=>{d.getElementById(id).value=value;d.getElementById(id).dispatchEvent(new w.Event('change'));};
 change('bom-class','Software');assert.equal(d.querySelectorAll('#bom-rows tr').length,model.items.filter(x=>x.class==='Software').length);
 const category=model.items.find(x=>x.class==='Software'&&x.release).category;change('bom-category',category);const date=model.items.find(x=>x.class==='Software'&&x.category===category&&x.release).release;change('bom-release',date);assert.equal(d.querySelectorAll('#bom-rows tr').length,model.items.filter(x=>x.class==='Software'&&x.category===category&&x.release===date).length);
 change('bom-class','Computer');assert.equal(d.querySelectorAll('#bom-rows tr').length,0);assert(d.getElementById('bom-inspector').textContent.includes('No elements'));
 d.getElementById('bom-reset').click();assert.equal(d.querySelectorAll('#bom-rows tr').length,model.items.length);
 assert(![...d.getElementById('bom-release').options].some(option=>option.value==='Unknown'));
 change('bom-release','no release');assert.equal(d.querySelectorAll('#bom-rows tr').length,12);assert([...d.querySelectorAll('#bom-rows tr')].every(tr=>tr.lastElementChild.textContent==='no release'));
 assert.deepEqual(errors,[]);dom.window.close();
 for(const [old,current] of [['edition.abacus_2.z80','software.abacus_2'],['part.artemis_ram_module_128kb_aion','part.ram_128kb_x32'],['device.artemis_ram_256kb_bank_kit','offer.ram_256kb_bank']]){
  const redirected=new JSDOM(read('bom-navigator.html'),{url:'https://atlas.test/bom-navigator.html?element='+old,runScripts:'outside-only',virtualConsole:vc});const rw=redirected.window;rw.fetch=async p=>({ok:true,json:async()=>json(p)});
  for(const script of rw.document.scripts)rw.eval(read(new URL(script.src).pathname.slice(1)));
  for(let i=0;i<60&&!rw.document.querySelector('main[data-ready]');i++)await new Promise(r=>setTimeout(r,10));
  assert(rw.document.querySelector('[data-element="'+current+'"][aria-pressed=true]'));assert.equal(new URL(rw.location.href).searchParams.get('element'),current);
  if(current.startsWith('part.')||current.startsWith('offer.')){rw.document.getElementById('tab-costs').click();assert(rw.document.getElementById('panel-costs').textContent.includes('pending reassessment'));}
  redirected.window.close();
 }
 console.log('PASS: BOM Navigator coverage, deep link, combined filters, empty/reset states and component BOMs');
})().catch(e=>{console.error(e);process.exitCode=1;});

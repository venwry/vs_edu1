const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(root,p),'utf8'),store=require('../data-store.js');
const catalog=store.read('catalog:logix-aion-technical-catalog-v2'),bom=store.read('catalog:hardware-bom'),cost=store.read('generated/models/manufacturing-costs.json');
const model=require('../bom-details.js').createModel(catalog,bom,cost);
assert.equal(catalog.devices.length,60);assert(!fs.existsSync(path.join(root,'data/peripherals.json')));
for(const ports of [4,8,16]){const id=`device.network_hub.${ports}_port`,device=catalog.devices.find(d=>d.id===id);assert.equal(device.specification.port_count,ports);assert.deepEqual(model.assemblyIds(id),[id]);assert.deepEqual(bom.assemblies.find(a=>a.id===id).lines,device.bom_assembly_definition);}
(async()=>{
 for(const old of ['device.network_hub','assembly.device.network_card_aurelia']){
  const dom=new JSDOM(read('bom-navigator.html'),{url:'https://atlas.test/bom-navigator.html?element='+old,runScripts:'outside-only'}),w=dom.window,d=w.document;
  w.fetch=async p=>({ok:true,json:async()=>store.read(p)});for(const s of d.scripts)w.eval(read(new URL(s.src).pathname.slice(1)));
  for(let i=0;i<100&&!d.querySelector('main[data-ready]');i++)await new Promise(r=>setTimeout(r,10));
  assert(d.querySelector('main[data-ready]'));
  if(old==='device.network_hub'){
   assert.equal(d.querySelectorAll('#bom-rows tr').length,3);assert(d.getElementById('bom-inspector').textContent.includes('Select a variant'));
   for(const ports of [4,8,16]){const id=`device.network_hub.${ports}_port`;d.querySelector(`[data-element="${id}"]`).click();d.getElementById('tab-bom').click();assert(d.getElementById('panel-bom').textContent.includes('Bill of materials'));assert.equal(new URL(w.location.href).searchParams.get('element'),id);}
   d.getElementById('bom-reset').click();assert.equal(d.querySelectorAll('#bom-rows tr').length,628);
  }else assert(d.querySelector('[data-element="device.network_card_aurelia"][aria-pressed=true]'));
  w.close();
 }
 console.log('PASS: inline device BOMs, distinct hub SKUs, retired family selection and assembly deep links');
})().catch(e=>{console.error(e);process.exitCode=1;});

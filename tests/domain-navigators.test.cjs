const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{JSDOM,VirtualConsole}=require('jsdom');
const root=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(root,p),'utf8'),json=p=>require('../data-store.js').read(p);
const site=json('generated/catalogs/site-pages.json'),catalog=json('generated/catalogs/logix-aion-technical-catalog-v2.json'),story=json('generated/catalogs/logix-aion-story.json');
const records=Object.fromEntries(Object.values(catalog).filter(Array.isArray).flat().filter(r=>r?.id).map(r=>[r.id,r]));
const bom=require('../bom-details.js').createModel(catalog,json('generated/catalogs/hardware-bom.json'),json('generated/models/manufacturing-costs.json'));
const tech=site.pages.find(p=>p.id==='technology'),services=site.pages.find(p=>p.id==='trainings-and-services');
assert.equal(tech.record_refs.length,22);assert.equal(services.record_refs.length,15);
assert(services.record_refs.includes('service.bpi_training'));assert(services.record_refs.includes('service.component_licensing'));
const all=[...tech.record_refs,...services.record_refs,...bom.items.map(i=>i.id)];assert.equal(new Set(all).size,all.length,'Navigator membership must not overlap');
for(const old of json('tests/fixtures/retired-domain-records.json'))for(const id of json('schemas/data-registry.json').device_family_aliases[old]||[old])assert(all.includes(id),'Lost record '+id);
for(const page of [tech,services])for(const id of page.record_refs)assert.equal(site.record_page_links[id],page.id);
(async()=>{
 for(const [page,deep] of [[tech,'technology.flexibus'],[services,'service.bpi_training']]){
  const errors=[],requests=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
  const dom=new JSDOM(read(page.path),{url:'https://atlas.test/'+page.path+'#'+deep,runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:vc}),w=dom.window,d=w.document;
  w.fetch=async p=>{requests.push(p);return {ok:true,json:async()=>json(p)}};
  for(const s of d.scripts)w.eval(read(new URL(s.src).pathname.slice(1)));
  for(let i=0;i<100&&!d.querySelector('main[data-ready]');i++)await new Promise(r=>setTimeout(r,10));
  assert(d.querySelector('main[data-ready]'));assert.equal(d.querySelectorAll('#bom-rows tr').length,page.record_refs.length);assert(d.querySelector('[data-element="'+deep+'"][aria-pressed=true]'));
  const reg=json('schemas/data-registry.json');const expected=new Set(['schemas/data-registry.json',...['logix-aion-story','logix-aion-technical-catalog-v2','site-pages'].flatMap(n=>require('../data-store.js').filesFor(n,reg))]);assert.deepEqual(requests.sort(),[...expected].sort());
  assert.equal(d.querySelectorAll('[role=tab]').length,2);
  for(const id of page.record_refs){d.querySelector('[data-element="'+id+'"]').click();d.getElementById('tab-details').click();assert(d.getElementById('bom-inspector').textContent.includes(records[id].name));d.getElementById('tab-events').click();const events=story.phases.flatMap(p=>p.events).filter(e=>(e.product_refs||[]).includes(id));assert.equal(d.querySelectorAll('#panel-events article').length,events.length);}
  d.getElementById('tab-events').dispatchEvent(new w.KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));assert.equal(d.activeElement.id,'tab-details');
  d.getElementById('tab-details').dispatchEvent(new w.KeyboardEvent('keydown',{key:'End',bubbles:true}));assert.equal(d.activeElement.id,'tab-events');
  for(const filter of ['bom-class','bom-category','bom-release']){const select=d.getElementById(filter);select.selectedIndex=1;select.dispatchEvent(new w.Event('change'));assert(d.querySelectorAll('#bom-rows tr').length>0);d.getElementById('bom-reset').click();assert.equal(d.querySelectorAll('#bom-rows tr').length,page.record_refs.length);}
  const categories=[...d.getElementById('bom-category').options].slice(1);for(const option of categories){d.getElementById('bom-category').value=option.value;d.getElementById('bom-category').dispatchEvent(new w.Event('change'));assert([...d.querySelectorAll('#bom-rows tr')].every(tr=>tr.children[2].textContent===option.value.replace(/_/g,' ')));}
  assert.deepEqual(errors,[]);dom.window.close();
 }
 // Retired pages are absent; their records remain in the canonical navigators.
 for(const name of ['academy','operating-systems','business-software','bpi','software-development','flexibus','video-system','networking','peripherals']){assert(!site.pages.some(p=>p.id===name));assert(!fs.existsSync(path.join(root,name+'.html')));}
 console.log('PASS: 22 technologies/platforms and 15 services, lossless/disjoint membership, all details/events, filters, keyboard tabs, old anchors and light data loading');
})().catch(e=>{console.error(e);process.exitCode=1;});

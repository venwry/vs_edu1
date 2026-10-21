// npm install --no-save jsdom; node tests/atlas.test.cjs
const {JSDOM,VirtualConsole}=require('jsdom');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const config=JSON.parse(read('site_pages.json')),story=JSON.parse(read('logix_aion_story.json'));
const tick=()=>new Promise(r=>setTimeout(r,35));
async function boot(page,overrides={},url='https://atlas.test/'+page.path){
 const errors=[],fetched=[];const vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e));
 const dom=new JSDOM(read(page.path),{url,runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:vc});
 const w=dom.window;w.IntersectionObserver=class{observe(){}unobserve(){}disconnect(){}};w.fetch=async p=>{const name=p.replace('./','');fetched.push(name);return {ok:true,json:async()=>overrides[name]||JSON.parse(read(name))};};
 if(page.kind==='report'){const script=w.document.querySelector('script:not([type])');if(script)w.eval(script.textContent);return {dom,w,d:w.document,errors,fetched};}
 w.eval(read('sales.js'));w.eval(read('pricing.js'));w.eval(read('manufacturing-costs.js'));w.eval(read('timeline-model.js'));w.eval(read('architecture-explorer.js'));w.eval(read('artemis-explorer.js'));w.eval(read('atlas.js'));await tick();
 assert.equal(errors.length,0,errors.map(e=>e.message).join('\n'));
 return {dom,w,d:w.document,errors,fetched};
}
(async()=>{
 const targets=new Map(),links=[];
 for(const page of config.pages){
  const {w,d,dom,errors,fetched}=await boot(page);
  assert.equal(d.querySelector('h1').textContent,page.title,page.id);
  for(const target of ['pricing.html','sales.html','industrial_investment_1974_1981.html','roi.html'])assert(d.querySelector('.site-nav a[href="'+target+'"]'),page.id+' missing '+target);
  assert.equal(fetched.length,page.kind==='report'?0:['costs','pricing','sales'].includes(page.kind)?4:3);
  assert(!d.querySelector('#catalogs'),page.id+' failed to load');
  if(page.kind==='explorer'){
   const initialRAM={aurelia:48,'aurelia-plus':64,artemis:128,'artemis-pro':512}[page.id];
   assert(d.querySelector('#stats').textContent.includes(initialRAM+' KB'));
   assert.equal(d.querySelectorAll('[data-model]').length,0);
   for(const layer of d.querySelectorAll('[data-layer]')){
    layer.click();await tick();assert(d.querySelectorAll('[data-node]').length>0,layer.dataset.layer);
    if(['aurelia','aurelia-plus'].includes(page.id)&&['hardware','memory'].includes(layer.dataset.layer)){
     for(const id of ['mapper','dma','sprite_ram'])assert(d.querySelector('[data-node="'+id+'"]'),page.id+' missing '+id);
     assert(d.querySelector('[data-node="dma"]').textContent.includes('Same system-controller die'));
     assert(d.querySelector('#memory-section').textContent.includes('independent')||d.querySelector('#memory-section').textContent.includes('refresh'));
    }
    for(const node of d.querySelectorAll('[data-node]')){node.click();assert(d.querySelector('#inspector').textContent.trim());}
    if(layer.dataset.layer==='software')for(const option of d.querySelector('#software-mode').options){
     d.querySelector('#software-mode').value=option.value;d.querySelector('#software-mode').dispatchEvent(new w.Event('change'));assert(d.querySelectorAll('[data-node]').length>0);
    }
   }
   if(page.id==='aurelia'){
    d.querySelector('[data-layer="memory"]').click();const card=d.querySelector('#ram-card');card.checked=true;card.dispatchEvent(new w.Event('change'));
    assert(d.querySelector('#stats').textContent.includes('64 KB'));assert(d.querySelector('#memory-section').textContent.includes('64 KB'));
   }
   if(page.explorer_family==='artemis'){
    assert(!d.body.textContent.includes('undefined'),page.id+' contains undefined values');
    d.querySelector('[data-layer="memory"]').click();
    assert(d.querySelector('[data-node="virtual"]').textContent.includes('32-bit'));
    assert(d.querySelector('[data-node="physical"]').textContent.includes('24-bit'));
    const ram=d.querySelector('#artemis-ram');
    const selectRAM=(id,capacity,modules,banks)=>{ram.value=id;ram.dispatchEvent(new w.Event('change'));assert.equal(ram.value,id);assert(d.querySelector('#stats').textContent.includes(capacity+' KB'));d.querySelector('[data-node="ram"]').click();assert(d.querySelector('#inspector').textContent.includes('Populated modules'+modules));assert(d.querySelector('#inspector').textContent.includes('Populated banks'+banks));};
    if(page.id==='artemis'){
     selectRAM('m32_128',128,4,2);assert(d.querySelector('[data-node="video_ram"] .video-card-contents').textContent.includes('Display RAM: 16 KiB'));assert(d.querySelector('[data-node="video_ram"] .video-card-contents').textContent.includes('Sprite SRAM: 1 KiB'));
     selectRAM('m32_256',256,8,4);
     selectRAM('m128_256',256,2,1);assert(d.querySelector('[data-node="video_ram"] .video-card-contents').textContent.includes('Display RAM: 32 KiB'));assert(!d.querySelector('[data-node="display_dram"]'));
     assert(d.querySelector('#memory-section').textContent.includes('2 × 128 KB / 16-bit modules'));
    }else selectRAM('m128_512',512,4,2);
    selectRAM('m128_1024',1024,8,4);
    assert(d.querySelector('#memory-section').textContent.includes('qualification pending'));
    d.querySelector('[data-layer="hardware"]').click();
    if(page.id==='artemis'){
     assert(d.querySelector('[data-node="compatibility"]'));
     assert(!d.querySelector('[data-node="network"]'));
     const era=d.querySelector('#era');era.value='1981';era.dispatchEvent(new w.Event('change'));assert(d.querySelector('[data-node="network"]'));
     era.value='launch';era.dispatchEvent(new w.Event('change'));assert(!d.querySelector('[data-node="network"]'));
    }else{
     assert(!d.querySelector('[data-node="compatibility"]'));
     assert(d.querySelector('[data-node="network"]'));assert(d.querySelector('#era').parentElement.hidden);
     assert(d.querySelector('[data-node="disk"]').textContent.includes('5 MB HDD'));
    }
    d.querySelector('[data-layer="bundles"]').click();
    const bundle=d.querySelector('#bundle-select');
    for(const option of bundle.options){bundle.value=option.value;bundle.dispatchEvent(new w.Event('change'));assert(d.querySelector('[data-node="bundle"]'));
     if(option.value.includes('128'))assert(d.querySelector('[data-node="bundle-item-0"]').textContent.includes('128 KB'));
     if(option.value.includes('1mb'))assert(d.querySelector('[data-node="bundle-item-0"]').textContent.includes('1024 KB'));
     if(option.value.includes('network_upgrade'))assert(!d.querySelector('#diagram').textContent.includes('Host computer'));
    }
   }
  }
  targets.set(page.path,new Set([...d.querySelectorAll('[id]')].map(x=>x.id)));
  for(const a of d.querySelectorAll('a[href]'))links.push([page.path,a.getAttribute('href')]);
  assert.equal(errors.length,0,errors.map(e=>e.message).join('\n'));dom.window.close();
 }
 for(const [source,href] of links){
  const u=new URL(href,'https://atlas.test/'+source),file=u.pathname.slice(1);
  if(u.origin!=='https://atlas.test')continue;
  if(['ncc_1980_campaign.json','market_outlook_1980_1982.json','TEAM_EDITION_1982.md','ecosystem_forecast.json','ecosystem_forecast_policy.json','ECOSYSTEM_FORECAST.md','artemis_display_impact.json','memory_manufacturing_impact.json','MEMORY_MANUFACTURING.md','SALES_VIEW.md','roi_1974_1980.json','marketing_budget_1974_1980.json','ROI.md','industrial_investment_1974_1981.json','manufacturing_costs.json','pricing_results.json','sales_forecast.json','NCC_1980_CAMPAIGN.md','SALES_COMDEX1980.md'].includes(file)){assert(fs.existsSync(path.join(root,file)));continue;}
  assert(targets.has(file),source+' -> '+href);
  if(u.hash)assert(targets.get(file).has(decodeURIComponent(u.hash.slice(1))),source+' -> missing '+href);
 }
 const page=config.pages.find(p=>p.id==='timeline'),{dom,w,d}=await boot(page,{},'https://atlas.test/timeline.html#event.bpi_offer');
 const events=story.phases.flatMap(p=>p.events);
 assert.equal(d.querySelectorAll('.event').length,events.length);
 assert.equal(d.querySelectorAll('.swim-heading').length,config.timeline_view.lanes.length);
 const cards=[...d.querySelectorAll('[data-event]')];
 assert.equal(cards.length,events.length);
 assert.equal(new Set(cards.map(c=>c.dataset.event)).size,events.length);
 for(const card of cards){
  const lane=config.timeline_view.lanes.find(l=>l.event_refs.includes(card.dataset.event));
  assert.equal(card.closest('[data-lane]').dataset.lane,lane.id);
 }
 assert.equal(d.querySelector('.timeline-workspace').firstElementChild.className,'event-inspection');
 assert.deepEqual([...d.querySelectorAll('.calendar-year')].map(x=>x.textContent),Array.from({length:12},(_,i)=>String(1972+i)));
 assert(d.querySelector('.timeline-origin [data-event="event.power"]'));
 assert(!d.querySelector('.calendar-grid [data-event="event.power"]'));
 assert.equal(d.querySelectorAll('.swim-event.approximate').length,0);
 assert.equal(d.querySelector('[data-event="event.lottery"] time').textContent,'1972-02-06');
 assert.equal(d.querySelectorAll('[data-select-process]').length,story.processes.flatMap(p=>[p,...(p.subprocesses||[])]).length);
 assert.equal(d.querySelectorAll('[data-select-process="process.international_investment"]').length,0);
 assert(!d.querySelector('[data-event="event.basic_develop"]'));
 assert(!d.querySelector('[data-event="event.harvard"]'));
 w.location.hash='#process.economics_studies';await tick();
 assert.equal(d.getElementById('process-inspection').hidden,false);assert(d.querySelector('#process-inspection [data-process="process.economics_studies"]').open);
 for(const cell of d.querySelectorAll('.calendar-cell')){
  const positions=[...cell.querySelectorAll('.calendar-event')].map(x=>parseFloat(x.style.top));
  for(let i=1;i<positions.length;i++)assert(positions[i]-positions[i-1]>=88,'event cards overlap');
 }
 const phaseButton=d.querySelector('[data-select-phase="phase.ncc78"]');phaseButton.click();
 assert.equal(w.location.hash,'#phase.ncc78');
 assert.equal(d.getElementById('phase-inspection').hidden,false);
 assert(d.getElementById('phase-inspection').textContent.includes('Aurelia premiere and first months of sales'));
 assert.equal(d.querySelectorAll('#phase-filter option').length,10);
 assert(!d.querySelector('#phase-inspection [data-process="process.market_expansion"]'));
 assert(!d.querySelector('#phase-inspection [data-event="event.market_growth"]'));
 assert(d.getElementById('phase-inspection').textContent.includes('1978-06-05 to 1979-06-03'));
 w.location.hash='#phase.after_ncc78';await tick();
 assert(d.getElementById('phase-inspection').textContent.includes('Aurelia premiere and first months of sales'));
 assert.equal(d.querySelectorAll('.event:not([hidden])').length,0);
 d.querySelector('[data-event="event.bpi_offer"]').click();
 assert.equal(d.getElementById('phase-inspection').hidden,true);
 assert(d.getElementById('event.bpi_offer').open);
 assert.equal(d.getElementById('event.bpi_offer').hidden,false);
 d.querySelector('[data-event="event.ibm_project"]').click();
 assert.equal(w.location.hash,'#event.ibm_project');
 assert.equal(d.getElementById('event.ibm_project').hidden,false);
 assert.equal(d.getElementById('event.bpi_offer').hidden,true);
 const expand=d.getElementById('expand-events');expand.checked=true;expand.dispatchEvent(new w.Event('change'));
 assert.equal(d.querySelectorAll('.event:not([hidden])').length,events.length);
 expand.checked=false;expand.dispatchEvent(new w.Event('change'));
 assert.equal(d.querySelectorAll('.event:not([hidden])').length,1);
 const actor=d.getElementById('actor-filter');actor.value='actor.ibm';actor.dispatchEvent(new w.Event('change'));
 assert.equal(d.querySelectorAll('.event').length,events.filter(e=>e.participants.some(x=>x.actor_ref==='actor.ibm')).length);
 assert.equal(d.querySelectorAll('[data-event]').length,events.filter(e=>e.participants.some(x=>x.actor_ref==='actor.ibm')).length);
 w.location.hash='#event.bpi_offer';await tick();
 assert.equal(actor.value,'');assert.equal(d.getElementById('event.bpi_offer').hidden,false);
 actor.value='';actor.dispatchEvent(new w.Event('change'));
 const search=d.getElementById('event-search');search.value='150000';search.dispatchEvent(new w.Event('input'));
 assert(d.getElementById('event.bpi_offer'));
 search.value='no event matches this query';search.dispatchEvent(new w.Event('input'));assert.equal(d.querySelectorAll('.event').length,0);
 dom.window.close();
 const changed=structuredClone(story);changed.phases[0].events[0].title='JSON update reaches the timeline';
 const dynamic=await boot(page,{'logix_aion_story.json':changed});assert(dynamic.d.body.textContent.includes('JSON update reaches the timeline'));dynamic.dom.window.close();
 const offline=await boot(page,{},'file:///atlas/timeline.html');assert(offline.d.querySelector('#catalogs'));offline.dom.window.close();
 console.log(`PASS: ${config.pages.length} pages, ${events.length} timeline events, ${links.length} links; four computer explorers, RAM expansion, networking, bundles, filters, JSON updates and offline recovery.`);
})().catch(e=>{console.error(e);process.exitCode=1;});




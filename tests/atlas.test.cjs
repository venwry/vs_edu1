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
 const w=dom.window;w.fetch=async p=>{const name=p.replace('./','');fetched.push(name);return {ok:true,json:async()=>overrides[name]||JSON.parse(read(name))};};
 w.eval(read('architecture-explorer.js'));w.eval(read('atlas.js'));await tick();
 assert.equal(errors.length,0,errors.map(e=>e.message).join('\n'));
 return {dom,w,d:w.document,errors,fetched};
}
(async()=>{
 const targets=new Map(),links=[];
 for(const page of config.pages){
  const {w,d,dom,errors,fetched}=await boot(page);
  assert.equal(d.querySelector('h1').textContent,page.title,page.id);
  assert.equal(fetched.length,3);
  assert(!d.querySelector('#catalogs'),page.id+' failed to load');
  if(page.kind==='explorer'){
   assert(d.querySelector('#stats').textContent.includes(page.id==='aurelia'?'48 KB':'64 KB'));
   assert.equal(d.querySelectorAll('[data-model]').length,0);
   for(const layer of d.querySelectorAll('[data-layer]')){
    layer.click();await tick();assert(d.querySelectorAll('[data-node]').length>0,layer.dataset.layer);
    for(const node of d.querySelectorAll('[data-node]')){node.click();assert(d.querySelector('#inspector').textContent.trim());}
    if(layer.dataset.layer==='software')for(const option of d.querySelector('#software-mode').options){
     d.querySelector('#software-mode').value=option.value;d.querySelector('#software-mode').dispatchEvent(new w.Event('change'));assert(d.querySelectorAll('[data-node]').length>0);
    }
   }
   if(page.id==='aurelia'){
    d.querySelector('[data-layer="memory"]').click();const card=d.querySelector('#ram-card');card.checked=true;card.dispatchEvent(new w.Event('change'));
    assert(d.querySelector('#stats').textContent.includes('64 KB'));assert(d.querySelector('#memory-section').textContent.includes('64 KB'));
   }
  }
  targets.set(page.path,new Set([...d.querySelectorAll('[id]')].map(x=>x.id)));
  for(const a of d.querySelectorAll('a[href]'))links.push([page.path,a.getAttribute('href')]);
  assert.equal(errors.length,0,errors.map(e=>e.message).join('\n'));dom.window.close();
 }
 for(const [source,href] of links){
  const u=new URL(href,'https://atlas.test/'+source),file=u.pathname.slice(1);
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
 assert.equal(d.querySelectorAll('[data-event]').length,2);
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
 console.log(`PASS: ${config.pages.length} pages, ${events.length} timeline events, ${links.length} links; diagrams, RAM expansion, filters, JSON updates and offline recovery.`);
})().catch(e=>{console.error(e);process.exitCode=1;});

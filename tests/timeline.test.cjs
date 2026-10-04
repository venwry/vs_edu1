// Tests continuous and nested calendar geometry and navigation.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {JSDOM,VirtualConsole}=require('jsdom');
const root=path.resolve(__dirname,'..'),read=n=>fs.readFileSync(path.join(root,n),'utf8');
const story=JSON.parse(read('logix_aion_story.json'));
const tick=()=>new Promise(resolve=>setTimeout(resolve,60));
async function boot(file,hash=''){
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e));
 const dom=new JSDOM(read(file),{url:'https://atlas.test/'+file+hash,runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:vc}),w=dom.window;
 w.IntersectionObserver=class{observe(){}unobserve(){}disconnect(){}};w.fetch=async p=>({ok:true,json:async()=>JSON.parse(read(p.replace('./','')))});
 Object.defineProperty(w.HTMLElement.prototype,'offsetWidth',{get(){return this.id==='timelinejs'?1200:500;}});
 Object.defineProperty(w.HTMLElement.prototype,'offsetHeight',{get(){return this.id==='timelinejs'?800:200;}});
 w.eval(read('timeline-model.js'));w.eval(read('atlas.js'));await tick();
 assert.equal(errors.length,0,errors.map(e=>e.message).join('\n'));
 return {dom,w,d:w.document,errors};
}
(async()=>{
 const {dom,w,d}=await boot('timeline.html');
 const css=d.createElement('style');css.textContent=read('atlas.css');d.head.append(css);
 assert.equal(w.getComputedStyle(d.querySelector('.timeline-workspace')).height,'870px');
 assert.equal(w.getComputedStyle(d.querySelector('.timeline-workspace')).marginBottom,'0px');
 assert.equal(w.getComputedStyle(d.querySelector('.timeline-main')).paddingBottom,'0px');
 assert.equal(d.querySelectorAll('[data-select-phase]').length,8);
 assert.equal(d.querySelectorAll('[data-select-process]').length,8);
 assert(!d.querySelector('#timeline-panel #assumptions'));
 assert(d.getElementById('assumptions-panel').hidden);
 const head=d.querySelector('[data-lane-heading]'),toggle=head.querySelector('.lane-toggle'),handle=head.querySelector('.lane-resize'),grid=d.querySelector('.continuous-calendar');
 const initial=Number(handle.getAttribute('aria-valuenow'));
 const pointer=(target,type,x)=>{const event=new w.MouseEvent(type,{bubbles:true,clientX:x,button:0});Object.defineProperty(event,'pointerId',{value:7});target.dispatchEvent(event);};
 pointer(handle,'pointerdown',100);pointer(d,'pointermove',180);pointer(d,'pointerup',180);
 assert.equal(Number(handle.getAttribute('aria-valuenow')),initial+80);
 assert(!d.body.classList.contains('resizing-lane'));
 toggle.click();assert.equal(toggle.getAttribute('aria-expanded'),'false');assert.equal(grid.style.gridTemplateColumns.split(' ')[2],'32px');
 const body=d.getElementById(toggle.getAttribute('aria-controls'));assert([...body.children].every(el=>el.hidden));
 assert(d.querySelector('.origin-event').hidden);
 toggle.click();assert.equal(Number(handle.getAttribute('aria-valuenow')),initial+80);assert([...body.children].every(el=>!el.hidden));
 toggle.click();d.getElementById('event-search').dispatchEvent(new w.Event('input'));
 const restored=d.querySelector('[data-lane-heading]');assert.equal(restored.querySelector('.lane-toggle').getAttribute('aria-expanded'),'false');
 restored.querySelector('.lane-toggle').click();assert.equal(Number(restored.querySelector('.lane-resize').getAttribute('aria-valuenow')),initial+80);
 restored.querySelector('.lane-resize').dispatchEvent(new w.KeyboardEvent('keydown',{key:'Home',bubbles:true}));
 assert.equal(Number(restored.querySelector('.lane-resize').getAttribute('aria-valuenow')),Number(restored.dataset.defaultWidth));
 const yearHeight=parseFloat(d.querySelector('.calendar-grid').style.getPropertyValue('--year-height'));
 for(const phase of story.phases){
  const node=d.getElementById(phase.id),M=w.AtlasTimeline;
  const top=(M.point(M.boundary(phase.period.start))-1972)*yearHeight;
  const height=(M.point(M.boundary(phase.period.end,true))-M.point(M.boundary(phase.period.start)))*yearHeight;
  assert.equal(parseFloat(node.style.top),top);assert.equal(parseFloat(node.style.height),height);
 }
 const investment=d.getElementById('process.international_investment');
 assert.equal(investment.dataset.approximate,'false');assert.equal(investment.dataset.start,'1973-01-01');assert.equal(investment.dataset.end,'1975-12-31');
 assert.equal(parseFloat(investment.style.top),yearHeight);assert.equal(parseFloat(investment.style.height),yearHeight*3);
 assert.equal(d.querySelectorAll('.calendar-process.approximate').length,5);
 const study=w.AtlasTimeline.processSpan(story.processes.find(p=>p.id==='process.economics_studies'),story);
 assert.equal(study.startDate,'1972-09-25');assert.equal(study.approximate,true);
 for(const lane of d.querySelectorAll('.lane-processes')){
  const nodes=[...lane.children];
  for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++)if(nodes[i].style.left===nodes[j].style.left){
   const a=nodes[i],b=nodes[j];assert(parseFloat(a.style.top)+parseFloat(a.style.height)<=parseFloat(b.style.top)||parseFloat(b.style.top)+parseFloat(b.style.height)<=parseFloat(a.style.top),'overlapping processes share a track');
  }
 }
 investment.querySelector('[data-select-process]').click();assert(!d.getElementById('process-inspection').hidden);assert(d.getElementById('process-inspection').textContent.includes('Recorded interval'));
 d.getElementById('assumptions-tab').click();assert(d.getElementById('timeline-panel').hidden);assert.equal(w.location.hash,'#assumptions');
 d.getElementById('timeline-tab').click();assert(!d.getElementById('timeline-panel').hidden);assert.equal(w.location.hash,'#process.international_investment');
 const filter=d.getElementById('phase-filter');filter.value='phase.foundations';filter.dispatchEvent(new w.Event('change'));
 assert.equal(parseFloat(d.getElementById('process.international_investment').style.height),yearHeight*3,'phase filter must not clip a process range');
 const type=d.getElementById('type-filter');type.value='process';type.dispatchEvent(new w.Event('change'));assert.equal(d.querySelectorAll('[data-event]').length,0);assert.equal(d.querySelectorAll('[data-select-process]').length,6);
 w.location.hash='#process.artemis_engineering';await tick();assert.equal(type.value,'');assert.equal(filter.value,'');assert(d.getElementById('process-inspection').textContent.includes('Approximate'));
 dom.window.close();
 const direct=await boot('timeline.html','#assumptions');assert(direct.d.getElementById('timeline-panel').hidden);direct.dom.window.close();
 const nested=await boot('timeline.html','#process.harvard_year_4');
 assert(nested.d.getElementById('process-inspection').textContent.includes('Harvard Economics Bachelor Yr 4'));
 const parent=nested.d.getElementById('process.economics_studies'),M=nested.w.AtlasTimeline;
 for(const child of story.processes.find(p=>p.id==='process.economics_studies').subprocesses){
  const el=nested.d.getElementById(child.id),span=M.processSpan(child,story);
  assert.equal(el.parentElement,parent);
  assert.equal(parseFloat(el.style.top),(M.point(span.start)-1972)*yearHeight-(M.point(study.start)-1972)*yearHeight);
  assert.equal(parseFloat(el.style.height),(M.point(span.end)-1972)*yearHeight-(M.point(span.start)-1972)*yearHeight);
  el.click();assert(nested.d.getElementById('process-inspection').textContent.includes(child.title));
 }
 assert(!nested.d.querySelector('button button'));
 assert(!nested.d.querySelector('.site-footer'));
 assert.equal(nested.d.querySelector('#timeline-panel').lastElementChild.className,'timeline-workspace');
 assert.equal(nested.w.getComputedStyle(parent).display,'block');
 for(const old of ['organization_buildout','market_monitoring','market_expansion']){
  assert(!nested.d.querySelector('[data-select-process="process.'+old+'"]'));
  nested.w.location.hash='#process.'+old;await tick();assert(nested.d.getElementById('timeline-panel').hidden);assert(nested.d.getElementById('assumption.'+old).open);
 }
 nested.w.location.hash='#process.nyse_speculation';await tick();assert(!nested.d.getElementById('timeline-panel').hidden);assert(nested.d.getElementById('event.us_nyse_start').open);
 nested.dom.window.close();
 console.log('PASS: continuous and nested geometry, filters, tabs, migrated aliases and no timeline footer.');
})().catch(e=>{console.error(e);process.exitCode=1;});

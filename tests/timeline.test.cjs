// Tests the real pinned TimelineJS as well as custom calendar geometry.
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
 if(file==='timeline2.html')w.eval(fs.readFileSync(process.env.TIMELINEJS_TEST_BUNDLE||require.resolve('@knight-lab/timelinejs/dist/js/timeline.js'),'utf8'));
 w.eval(read('timeline-model.js'));w.eval(read('atlas.js'));await tick();
 assert.equal(errors.length,0,errors.map(e=>e.message).join('\n'));
 return {dom,w,d:w.document,errors};
}
(async()=>{
 const {dom,w,d}=await boot('timeline.html');
 assert.equal(d.querySelectorAll('[data-select-phase]').length,8);
 assert.equal(d.querySelectorAll('[data-select-process]').length,8);
 assert(!d.querySelector('#timeline-panel #assumptions'));
 assert(d.getElementById('assumptions-panel').hidden);
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
 assert.equal(d.querySelectorAll('.calendar-process.approximate').length,7);
 const study=w.AtlasTimeline.processSpan(story.processes.find(p=>p.id==='process.economics_studies'),story);
 assert.equal(study.startDate,'1972-02-06');assert.equal(study.approximate,true);
 for(const lane of d.querySelectorAll('.lane-processes')){
  const nodes=[...lane.children];
  for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++)if(nodes[i].style.left===nodes[j].style.left){
   const a=nodes[i],b=nodes[j];assert(parseFloat(a.style.top)+parseFloat(a.style.height)<=parseFloat(b.style.top)||parseFloat(b.style.top)+parseFloat(b.style.height)<=parseFloat(a.style.top),'overlapping processes share a track');
  }
 }
 investment.click();assert(!d.getElementById('process-inspection').hidden);assert(d.getElementById('process-inspection').textContent.includes('Recorded interval'));
 d.getElementById('assumptions-tab').click();assert(d.getElementById('timeline-panel').hidden);assert.equal(w.location.hash,'#assumptions');
 d.getElementById('timeline-tab').click();assert(!d.getElementById('timeline-panel').hidden);assert.equal(w.location.hash,'#process.international_investment');
 const filter=d.getElementById('phase-filter');filter.value='phase.foundations';filter.dispatchEvent(new w.Event('change'));
 assert.equal(parseFloat(d.getElementById('process.international_investment').style.height),yearHeight*3,'phase filter must not clip a process range');
 const type=d.getElementById('type-filter');type.value='process';type.dispatchEvent(new w.Event('change'));assert.equal(d.querySelectorAll('[data-event]').length,0);assert.equal(d.querySelectorAll('[data-select-process]').length,3);
 w.location.hash='#process.artemis_engineering';await tick();assert.equal(type.value,'');assert.equal(filter.value,'');assert(d.getElementById('process-inspection').textContent.includes('Approximate'));
 dom.window.close();
 const second=await boot('timeline2.html','#process.international_investment'),d2=second.d;
 assert(d2.getElementById('timeline-two-status').textContent.includes('8 processes'));
 assert.equal(d2.querySelectorAll('.tl-timemarker').length,40);
 assert.equal(d2.querySelectorAll('.tl-timemarker-with-end').length,8);
 assert.equal(d2.querySelectorAll('.tl-timeera').length,8);
 assert(d2.getElementById('process.international_investment-marker').classList.contains('tl-timemarker-active'));
 assert.equal(d2.querySelectorAll('#event\\.power').length,1);
 const jump=d2.getElementById('timeline-two-jump');jump.value='event.plus_launch';jump.dispatchEvent(new second.w.Event('change'));
 assert(d2.getElementById('event.plus_launch-marker').classList.contains('tl-timemarker-active'));
 const phase=d2.getElementById('timeline-two-phase');phase.value='phase.ncc80';phase.dispatchEvent(new second.w.Event('change'));
 assert.equal(second.w.location.hash,'#phase.ncc80');
 d2.getElementById('assumptions-tab').click();assert(d2.getElementById('timeline-panel').hidden);d2.getElementById('timeline-tab').click();assert(!d2.getElementById('timeline-panel').hidden);
 second.w.location.hash='#event.exchanges';await tick();assert(d2.getElementById('process.international_investment-marker').classList.contains('tl-timemarker-active'));
 assert.equal(second.errors.length,0);second.dom.window.close();
 for(const file of ['timeline.html','timeline2.html']){const direct=await boot(file,'#assumptions');assert(direct.d.getElementById('timeline-panel').hidden);assert(!direct.d.getElementById('assumptions-panel').hidden);direct.dom.window.close();}
 console.log('PASS: continuous phase/process geometry, approximate envelopes, collision tracks, filtering, tabs, deep links; real TimelineJS has 40 markers, 8 ranges and 8 eras.');
})().catch(e=>{console.error(e);process.exitCode=1;});

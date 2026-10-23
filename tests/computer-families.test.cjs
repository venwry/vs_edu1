const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {JSDOM,VirtualConsole}=require('jsdom'),root=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(root,p),'utf8'),json=p=>require('../data-store.js').read(p);
const catalog=json('generated/catalogs/logix-aion-technical-catalog-v2.json'),bom=json('generated/catalogs/hardware-bom.json'),cost=json('generated/models/manufacturing-costs.json');
const {createFamilyModel}=require('../artemis-configurator.js');
async function boot(family,query=''){
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));const dom=new JSDOM(read(family+'.html'),{url:'https://atlas.test/'+family+'.html'+query,runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:vc}),w=dom.window,d=w.document;
 w.fetch=async p=>({ok:true,json:async()=>json(p)});w.IntersectionObserver=class{observe(){}disconnect(){}};
 for(const s of d.scripts)w.eval(s.src?read(new URL(s.src).pathname.slice(1)):s.textContent);
 for(let i=0;i<60&&!d.querySelector('#artemis-workbench[data-ready]');i++)await new Promise(r=>setTimeout(r,10));
 assert(d.querySelector('#artemis-workbench[data-ready]'),d.body.textContent.slice(-500));return {dom,w,d,errors};
}
(async()=>{
 for(const family of ['artemis','aurelia','athena']){
  const model=createFamilyModel(catalog,bom,cost,family),{dom,w,d,errors}=await boot(family),select=d.getElementById('artemis-configuration');
  assert(!d.getElementById('artemis-revision'));assert(!d.getElementById('artemis-cost-date'));assert.equal(d.querySelectorAll('.configuration-sections>li').length,6);
  assert.equal(select.options.length,model.options.reduce((n,o)=>n+model.revisions(o).length,0));
  for(const option of model.options)for(const [i,rev] of model.revisions(option).entries()){
   select.value=i?option.id+'::'+rev.id:option.id;select.dispatchEvent(new w.Event('change'));await new Promise(r=>setTimeout(r,0));
   assert.equal(d.getElementById('artemis-workbench').dataset.configuration,option.id);assert(!d.querySelector('.configuration-empty'));assert.equal(d.querySelectorAll('[data-evaluation]').length,model.assessments(option,rev).length);
   for(const {date,snapshot} of model.assessments(option,rev)){d.querySelector('[data-evaluation="'+date+'"]').click();assert(d.getElementById('configuration-bom-date').textContent.includes(date));assert.equal(d.querySelector('#configuration-bom-table table tbody').children.length,snapshot.bom_lines.length);await new Promise(r=>setTimeout(r,0));}
   for(const button of d.querySelectorAll('[data-component]')){assert(button.querySelector('.component-label'));assert(!button.querySelector('br'));button.click();assert(d.getElementById('configuration-inspector').textContent.includes(button.querySelector('.component-label').textContent));await new Promise(r=>setTimeout(r,0));}
   if(option.upgrade)assert(!d.querySelector('[data-component="cpu"]'));else{assert(d.querySelector('[data-component="cpu"] .component-value').textContent.includes('MHz'));if(family==='artemis'){const state=model.state(option,rev,model.assessments(option,rev).at(-1)?.date||rev.from);assert.equal(d.querySelectorAll('[data-component^="bank-"]').length,state.ram.populated_banks);assert.equal(Boolean(d.querySelector('[data-record-ref="device.network_card_artemis"][data-component^="slot-"]')),state.network);}}
  }
  if(family==='aurelia'){const combos=model.options.filter(o=>o.combination);assert.equal(combos.length,6);for(const o of combos){const s=model.state(o,model.revisions(o)[0],o.available);assert(s.network);assert(s.software.includes('software.cpm_aurelia_networking'));assert(!s.software.includes('software.cpm_aurelia'));assert(!s.snapshot);}}
  if(family==='athena'){assert.equal(select.options.length,2);assert(d.getElementById('configuration-status').textContent.includes('planning'));assert(d.getElementById('configuration-cost-table').textContent.includes('No June 15'));assert.equal(d.querySelectorAll('[data-component^="bank-"]').length,2);assert(d.querySelector('[data-component="hdd"] .component-value').textContent.includes('20 MB'));}
  w.dispatchEvent(new w.Event('resize'));await new Promise(r=>setTimeout(r,20));assert.deepEqual(errors,[]);dom.window.close();
 }
 const {dom,d}=await boot('artemis','?configuration=bundle.artemis_128_mono&revision=assembly.bundle.artemis_128_mono.networked');assert(d.getElementById('artemis-configuration').value.includes('::'));assert(d.querySelector('[data-component="slot-0"]'));dom.window.close();
 console.log('PASS: all computer families, every configuration/revision/component, cost history, compact rows, populated banks, network selections and legacy links');
})().catch(e=>{console.error(e);process.exitCode=1;});

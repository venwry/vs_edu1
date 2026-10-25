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
// No cost-row, catalogue-status or hardcoded-ID membership filter is permitted.
const probe=JSON.parse(JSON.stringify(catalog)),template=probe.product_catalog.products.find(p=>p.id==='product.aurelia_mono');
probe.product_catalog.products.push({...template,id:'offer.selector_probe',name:'Selector probe',catalogue_status:'planned'});
assert(createFamilyModel(probe,bom,cost,'aurelia').options.some(o=>o.id==='offer.selector_probe'&&!o.cost));
template.computer_line=null;assert(!createFamilyModel(probe,bom,cost,'aurelia').options.some(o=>o.id===template.id));
(async()=>{
 const legacy=await boot('artemis','?configuration=bundle.artemis_budget_128_hdd');assert.equal(legacy.d.getElementById('artemis-configuration').value,'product.artemis_budget_128_hdd');legacy.dom.window.close();
 for(const family of ['artemis','aurelia','athena']){
  const model=createFamilyModel(catalog,bom,cost,family),{dom,w,d,errors}=await boot(family),select=d.getElementById('artemis-configuration');
  const line={aurelia:'Aurelia',artemis:'Artemis',athena:'Athena'}[family];
  assert.deepEqual([...select.options].map(o=>o.value),catalog.product_catalog.products.filter(p=>p.computer_line===line).map(p=>p.id));
  assert(!d.getElementById('artemis-revision'));assert.equal(select.options.length,{aurelia:4,artemis:8,athena:2}[family]);
  for(const option of model.options){
   select.value=option.id;select.dispatchEvent(new w.Event('change'));await new Promise(r=>setTimeout(r,0));
   const rev=model.revisions(option).at(-1);assert.equal(d.getElementById('artemis-workbench').dataset.configuration,option.id);
   assert.equal(d.querySelectorAll('[data-evaluation]').length,model.assessments(option,rev).length);
   for(const {date,snapshot} of model.assessments(option,rev)){d.querySelector('[data-evaluation="'+date+'"]').click();assert(d.getElementById('configuration-bom-date').textContent.includes(date));assert.equal(d.querySelector('#configuration-bom-table table tbody').children.length,snapshot.bom_lines.length);}
   for(const button of d.querySelectorAll('[data-component]')){button.click();assert(d.getElementById('configuration-inspector').textContent.includes(button.querySelector('.component-label').textContent));}
   d.getElementById('configuration-tab-bom').click();assert(!d.getElementById('configuration-panel-bom').hidden);d.getElementById('configuration-tab-details').click();
  }
  assert.deepEqual(errors,[]);dom.window.close();
 }
 console.log('PASS: all 14 commercial products, line-only membership, details/BOM tabs, every selectable component and saved cost evaluation');
})().catch(e=>{console.error(e);process.exitCode=1;});

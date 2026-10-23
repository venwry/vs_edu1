const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{JSDOM,VirtualConsole}=require('jsdom');
const root=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(root,p),'utf8'),json=p=>JSON.parse(read(p));
const {vendorName}=require('../bom-details.js');
assert.equal(vendorName({vendor:'Vendor',owner:'Owner'}),'Vendor');
assert.equal(vendorName({product_ref:'software.parent'},{'software.parent':{vendor:'Publisher'}}),'Publisher');
assert.equal(vendorName({catalog_ref:'part.chip'},{'part.chip':{vendor:'Chip maker'}}),'Chip maker');
assert.equal(vendorName({name:'Logix branded item'}),'Unknown','Names must not be used to guess vendor');
const cycle={id:'loop',product_ref:'loop'};assert.equal(vendorName(cycle,{loop:cycle}),'Unknown');
const collator=new Intl.Collator('en',{numeric:true,sensitivity:'base'});
(async()=>{
 for(const page of ['technology','trainings-and-services','bom-navigator']){
  const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
  const dom=new JSDOM(read(page+'.html'),{url:'https://atlas.test/'+page+'.html',runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:vc}),w=dom.window,d=w.document;
  w.fetch=async p=>({ok:true,json:async()=>json(p)});for(const s of d.scripts)w.eval(read(new URL(s.src).pathname.slice(1)));
  for(let i=0;i<100&&!d.querySelector('main[data-ready]');i++)await new Promise(r=>setTimeout(r,10));
  assert(d.querySelector('main[data-ready]'));const rows=()=>[...d.querySelectorAll('#bom-rows tr')],total=rows().length;
  assert.equal(d.querySelectorAll('[data-sort]').length,5);assert(rows().every(r=>r.children.length===5));
  const selected=d.querySelector('[data-element][aria-pressed=true]').dataset.element;d.getElementById('tab-events').click();const panel=d.getElementById('panel-events');
  for(const [i,key] of ['name','class','category','vendor','release'].entries()){
   const button=d.querySelector('[data-sort="'+key+'"]');if(button.closest('th').getAttribute('aria-sort')!=='ascending')button.click();
   for(const dir of [1,-1]){
    if(dir===-1)button.click();assert.equal(button.closest('th').getAttribute('aria-sort'),dir===1?'ascending':'descending');
    const values=rows().map(r=>r.children[i].textContent);let unknown=false,last;
    for(const value of values){if(value==='Unknown'){unknown=true;continue;}assert(!unknown,'Unknown must sort last');if(last!==undefined)assert(dir*collator.compare(last,value)<=0,key+' order on '+page);last=value;}
    assert.equal(d.querySelector('[data-element][aria-pressed=true]').dataset.element,selected);assert.equal(d.getElementById('panel-events'),panel,'Sorting must preserve inspector state');assert.equal(d.getElementById('tab-events').getAttribute('aria-selected'),'true');
   }
  }
  const change=(id,value)=>{d.getElementById(id).value=value;d.getElementById(id).dispatchEvent(new w.Event('change'));};
  const vendor=d.getElementById('bom-vendor');const available=[...vendor.options].slice(1).map(o=>o.value);assert(available.length);assert.deepEqual([...new Set(rows().map(r=>r.children[3].textContent))].sort(),available.slice().sort());
  for(const value of available){change('bom-vendor',value);assert(rows().length);assert(rows().every(r=>r.children[3].textContent===value));}
  d.getElementById('bom-reset').click();assert.equal(rows().length,total);assert.equal(vendor.value,'');assert.equal(d.querySelector('[data-sort=name]').closest('th').getAttribute('aria-sort'),'ascending');
  const first=rows()[0],cl=first.children[1].textContent,category=first.children[2].textContent,ven=first.children[3].textContent;
  const categoryOption=[...d.getElementById('bom-category').options].find(o=>o.textContent===category).value;
  const expected=rows().filter(r=>r.children[1].textContent===cl&&r.children[2].textContent===category&&r.children[3].textContent===ven).length;
  change('bom-class',cl);change('bom-category',categoryOption);change('bom-vendor',ven);assert.equal(rows().length,expected);assert.deepEqual(errors,[]);dom.window.close();
 }
 console.log('PASS: all three navigators sort all five columns both ways, preserve selection/tab state, filter vendor with other filters, reset and safely inherit explicit vendors');
})().catch(e=>{console.error(e);process.exitCode=1;});

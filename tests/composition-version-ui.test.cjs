const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require('jsdom'),root=path.resolve(__dirname,'..'),store=require('../data-store');
async function boot(file,query,ready){
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
 const dom=new JSDOM(fs.readFileSync(path.join(root,file),'utf8'),{url:'https://test.local/'+file+query,runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:vc});const w=dom.window;
 w.fetch=async p=>({ok:true,json:async()=>store.read(p)});w.IntersectionObserver=class{observe(){}disconnect(){}};
 for(const script of w.document.scripts)w.eval(script.src?fs.readFileSync(path.join(root,new URL(script.src).pathname.slice(1)),'utf8'):script.textContent);
 for(let i=0;i<80&&!w.document.querySelector(ready);i++)await new Promise(r=>setTimeout(r,10));
 assert(w.document.querySelector(ready));return {dom,w,d:w.document,errors};
}
(async()=>{
 let t=await boot('bom-navigator.html','?element=device.artemis_professional_video_128kb','#tab-bom');t.d.querySelector('#tab-bom').click();
 let select=t.d.querySelector('[data-composition-version]');assert.deepEqual([...select.options].map(o=>o.textContent),['1982-06-07 - 1982-11-29','1982-11-29 - 1990-01-01']);
 assert.equal(select.value,'2');const count=()=>t.d.querySelector('#panel-bom .bom-table-scroll table tbody').children.length;const november=count();select.value='1';select.dispatchEvent(new t.w.Event('change'));assert.equal(count(),november-1);assert.deepEqual(t.errors,[]);t.dom.window.close();
 t=await boot('artemis.html','?configuration=bundle.artemis_128_mono','#artemis-workbench[data-ready]');t.d.querySelector('#configuration-tab-bom').click();
 select=t.d.querySelector('#configuration-element-bom [data-composition-version]');assert.equal(select.options.length,2);assert.equal(select.value,'2');
 assert(t.d.querySelector('#configuration-diagram [data-component^="software-"][data-record-ref="software.aionix_server"]'));
 select.value='1';select.dispatchEvent(new t.w.Event('change'));assert.equal(t.d.querySelector('#configuration-element-bom [data-composition-version]').value,'1');assert(!t.d.querySelector('#configuration-diagram [data-component^="software-"][data-record-ref="software.aionix_server"]'));
 assert.deepEqual(t.errors,[]);t.dom.window.close();console.log('PASS: Navigator and computer BOM selectors, exact date labels, November device revision and parent product changes');
})().catch(e=>{console.error(e);process.exitCode=1});

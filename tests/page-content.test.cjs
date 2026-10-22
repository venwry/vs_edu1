// Baseline capture: BASELINE_ROOT=/path/to/original UPDATE_PAGE_BASELINE=1 node tests/page-content.test.cjs
// Normal test compares visible text, table counts and link targets with the pre-migration pages.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {JSDOM,VirtualConsole}=require('jsdom');
const root=path.resolve(__dirname,'..'),input=process.env.BASELINE_ROOT||root;
const paths=JSON.parse(fs.readFileSync(path.join(root,'data/manifest.json'),'utf8')).paths;
const baselinePath=path.join(__dirname,'page-content-baseline.json');
const normalize=s=>{for(const [old,current] of Object.entries(paths))s=s.split(current).join(old);return s.replace(/\s+/g,' ').trim();};
async function inspect(file){
 const errors=[],requests=[];const vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
 const dom=new JSDOM(fs.readFileSync(path.join(input,file),'utf8'),{url:'https://atlas.test/'+file,runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:vc});const w=dom.window;
 w.IntersectionObserver=class{observe(){}unobserve(){}disconnect(){}};
 w.fetch=async url=>{const name=String(url).replace(/^\.\//,'');requests.push(name);return {ok:fs.existsSync(path.join(input,name)),json:async()=>JSON.parse(fs.readFileSync(path.join(input,name),'utf8'))};};
 for(const script of w.document.querySelectorAll('script')){
  if(script.type&&script.type!=='text/javascript')continue;
  if(script.src){const name=new URL(script.src).pathname.slice(1);w.eval(fs.readFileSync(path.join(input,name),'utf8'));}else w.eval(script.textContent);
 }
 await new Promise(r=>setTimeout(r,150));
 assert.equal(errors.length,0,file+': '+errors.join('\n'));
 assert(!w.document.querySelector('#catalogs'),file+' failed to load');
 const links=[...w.document.querySelectorAll('a[href]')].map(a=>normalize(a.getAttribute('href')));
 const clone=w.document.body.cloneNode(true);clone.querySelectorAll('script,style').forEach(n=>n.remove());
 const text=normalize(clone.textContent);
 const result={text_sha256:crypto.createHash('sha256').update(text).digest('hex'),text_length:text.length,tables:clone.querySelectorAll('table').length,links};
 dom.window.close();return result;
}
(async()=>{
 const result={};for(const file of fs.readdirSync(input).filter(f=>f.endsWith('.html')).sort())result[file]=await inspect(file);
 if(process.env.UPDATE_PAGE_BASELINE==='1'){assert(process.env.BASELINE_ROOT,'Capture only against the original checkout');fs.writeFileSync(baselinePath,JSON.stringify(result,null,2)+'\n');console.log('Captured',Object.keys(result).length,'original pages');}
 else{const baseline=JSON.parse(fs.readFileSync(baselinePath,'utf8'));for(const [file,value] of Object.entries(result))assert.deepEqual(value,baseline[file],file+' content changed');assert.deepEqual(Object.keys(result),Object.keys(baseline));console.log('PASS:',Object.keys(result).length,'HTML pages retain text, tables and links');}
})().catch(e=>{console.error(e);process.exitCode=1;});

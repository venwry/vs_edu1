const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {JSDOM,VirtualConsole}=require('jsdom');const root=path.resolve(__dirname,'..'),read=f=>fs.readFileSync(path.join(root,f),'utf8'),site=JSON.parse(read('generated/catalogs/site-pages.json'));
async function boot(file,suffix=''){
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));const dom=new JSDOM(read(file),{url:'https://atlas.test/'+file+suffix,runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:vc}),w=dom.window;
 w.IntersectionObserver=class{observe(){}disconnect(){}};w.fetch=async p=>({ok:true,json:async()=>JSON.parse(read(p.replace(/^\.\//,'')))});
 for(const script of w.document.scripts){if(script.type&&script.type!=='text/javascript')continue;if(script.textContent.includes('location.replace'))continue;w.eval(script.src?read(new URL(script.src).pathname.slice(1)):script.textContent);}
 await new Promise(r=>setTimeout(r,150));assert.equal(errors.length,0,file+': '+errors.join('\n'));assert(!w.document.querySelector('#catalogs'),file+' boot failed');assert(!w.document.querySelector('[role=alert]'),file+' supplementary load failed');return dom;
}
(async()=>{
 const nav=read('site/navigation.html').trim(),costs=JSON.parse(read('generated/models/manufacturing-costs.json')),coverage=new Set();
 for(const p of site.pages){const dom=await boot(p.path),d=dom.window.document;
 assert.equal(d.querySelectorAll('.atlas-header').length,1,p.path);const h=d.querySelector('.atlas-header').cloneNode(true);h.querySelectorAll('[aria-current]').forEach(a=>a.removeAttribute('aria-current'));assert.equal(h.outerHTML,nav,p.path+' shared navigation');assert.equal(h.querySelectorAll('nav a').length,19);assert.equal(h.querySelectorAll('nav section').length,5);assert.equal(h.querySelector('.atlas-brand'),null);assert.equal(h.querySelector('a[href="ecosystem.html"]').textContent,'3rd Party');
 for(const n of d.querySelectorAll('[data-cost-id]'))coverage.add(n.dataset.costId);
 if(p.id==='aurelia'||p.id==='artemis'){assert.equal(d.querySelectorAll('#family-model option').length,2);const c=d.getElementById('family-configuration');assert(c.options.length>2);c.value=c.options[2].value;c.dispatchEvent(new dom.window.Event('change'));assert(d.getElementById('selected-configuration').textContent.includes(c.options[2].textContent.split(' · ')[0]));}
 if(p.id==='timeline'){for(const group of site.campaign_groups){assert(d.getElementById(group.event_ref));for(const id of group.step_refs){assert(d.getElementById(group.event_ref).contains(d.getElementById(id)));assert(!d.querySelector('[data-event="'+id+'"]'));}}assert(d.getElementById('entities'));}
 dom.window.close();}
 assert(costs.products.every(p=>coverage.has(p.id)),'every manufacturing/commercial cost row has a visible destination');
 for(const [source,target] of Object.entries(site.redirects)){const d=new JSDOM(read(source)).window.document;assert.equal(d.getElementById('redirect-target').getAttribute('href'),target);assert(d.body.textContent.includes('location.hash'));assert(fs.existsSync(path.join(root,target.split('#')[0])));}
 for(const [file,id,processor] of [['aurelia.html','computer.aurelia_plus','6 MHz'],['artemis.html','computer.artemis_pro','8 MHz']]){const dom=await boot(file,'#'+id);assert.equal(dom.window.document.getElementById('family-model').value,id);assert(dom.window.document.getElementById('stats').textContent.includes(processor));dom.window.close();}
 const eco=JSON.parse(read('generated/models/ecosystem-forecast.json'));for(const s of eco.scenarios)for(const q of s.quarterly){assert(q.cpm_applications>=q.qualified_legacy_pool);assert(q.tui_applications<=q.cpm_applications);assert.equal(q.external_computer_models,q.external_oems.length);assert.equal(q.distinct_application_families,q.cpm_applications+q.aionix_applications-q.cross_platform_families);}
 console.log('PASS: 19 shared headers, 14 redirects, family configurations, campaign groups, complete cost coverage and ecosystem accounting');
})().catch(e=>{console.error(e);process.exitCode=1;});

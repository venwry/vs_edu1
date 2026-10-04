const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'..'),dom=new JSDOM('<div id="inspector"></div>',{runScripts:'outside-only'}),w=dom.window;
w.eval(fs.readFileSync(path.join(root,'architecture-explorer.js'),'utf8'));
const catalog=JSON.parse(fs.readFileSync(path.join(root,'logix_aion_technical_catalog_v2.json'),'utf8')),records=Object.fromEntries(Object.values(catalog).filter(Array.isArray).flat().filter(x=>x?.id).map(x=>[x.id,x]));
const mmu=Object.values(records).find(x=>x.specification?.implementation_design?.title==='ERA MMU v1');assert(mmu);
const panel=w.document.getElementById('inspector');panel.innerHTML=w.renderSpecification(mmu.specification,records);w.bindSpecificationControls(panel);
assert(panel.querySelectorAll('.spec-properties').length>2);assert(panel.querySelectorAll('details').length>5);assert(panel.textContent.includes('4096'));assert(!panel.textContent.includes('[object Object]'));
function leaves(x){return x&&typeof x==='object'?Object.values(x).flatMap(leaves):[x];}
for(const leaf of leaves(mmu.specification)){if(typeof leaf==='string'&&leaf)assert(panel.textContent.includes(records[leaf]?.name||leaf),'Missing '+leaf);}
panel.querySelector('[data-spec-expand="true"]').click();assert([...panel.querySelectorAll('details')].every(x=>x.open));panel.querySelector('[data-spec-expand="false"]').click();assert([...panel.querySelectorAll('details')].every(x=>!x.open));
panel.innerHTML=w.renderSpecification({ram_slots:8,banks:4,modules_per_bank:2,module_data_width_bits:16,bank_data_width_bits:32,physical_limit_kb:1024,mixed_density_allowed:false});const groups=panel.querySelector('.spec-property-groups');assert.equal(groups.children.length,2);assert.equal(groups.children[0].querySelectorAll('tbody tr').length,4);assert.equal(groups.children[1].querySelectorAll('tbody tr').length,3);
panel.innerHTML=w.renderSpecification({note:'<img src=x onerror=alert(1)>',zero:0,flag:false,unknown:null,empty:[]});assert(!panel.querySelector('img'));assert(panel.textContent.includes('Unspecified'));assert(panel.textContent.includes('No'));assert(panel.textContent.includes('0'));
dom.window.close();console.log('PASS: full MMU content, compact paired columns, nested sections, bulk controls and escaped values.');

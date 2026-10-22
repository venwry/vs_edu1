const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'..'),dom=new JSDOM('<div id="inspector"></div>',{runScripts:'outside-only'}),w=dom.window;
w.eval(fs.readFileSync(path.join(root,'architecture-explorer.js'),'utf8'));
const catalog=JSON.parse(fs.readFileSync(path.join(root,'generated/catalogs/logix-aion-technical-catalog-v2.json'),'utf8')),records=Object.fromEntries(Object.values(catalog).filter(Array.isArray).flat().filter(x=>x?.id).map(x=>[x.id,x]));
const mmu=Object.values(records).find(x=>x.specification?.implementation_design?.title==='ERA MMU v1');assert(mmu);
const panel=w.document.getElementById('inspector');panel.innerHTML=w.renderSpecification(mmu.specification,records);w.bindSpecificationControls(panel);
assert(panel.querySelectorAll('.spec-properties').length>2);assert(panel.querySelectorAll('details').length>5);assert(panel.textContent.includes('4096'));assert(!panel.textContent.includes('[object Object]'));
function leaves(x){return x&&typeof x==='object'?Object.values(x).flatMap(leaves):[x];}
for(const leaf of leaves(mmu.specification)){if(typeof leaf==='string'&&leaf)assert(panel.textContent.includes(records[leaf]?.name||leaf),'Missing '+leaf);}
panel.querySelector('[data-spec-expand="true"]').click();assert([...panel.querySelectorAll('details')].every(x=>x.open));panel.querySelector('[data-spec-expand="false"]').click();assert([...panel.querySelectorAll('details')].every(x=>!x.open));
panel.innerHTML=w.renderSpecification({ram_slots:8,banks:4,modules_per_bank:2,module_data_width_bits:16,bank_data_width_bits:32,physical_limit_kb:1024,mixed_density_allowed:false});const groups=panel.querySelector('.spec-property-groups');assert.equal(groups.children.length,1);assert.equal(groups.children[0].querySelectorAll('tbody tr').length,7);
panel.innerHTML=w.renderSpecification({note:'<img src=x onerror=alert(1)>',zero:0,flag:false,unknown:null,empty:[]});assert(!panel.querySelector('img'));assert(panel.textContent.includes('Unspecified'));assert(panel.textContent.includes('No'));assert(panel.textContent.includes('0'));
for(const id of ['computer.aurelia','computer.aurelia_plus','computer.artemis','computer.artemis_pro']){
 panel.innerHTML=w.renderSpecification(records[id].video,records);
 const tables=panel.querySelectorAll('.video-mode-table');assert.equal(tables.length,2);
 assert.equal(tables[0].querySelectorAll('tbody tr').length,records[id].video.text_modes.length);assert.equal(tables[1].querySelectorAll('tbody tr').length,records[id].video.bitmap_modes.length);
 for(const mode of [...records[id].video.text_modes,...records[id].video.bitmap_modes]){
  const row=[...panel.querySelectorAll('.video-mode-table tbody tr')].find(r=>r.textContent.includes(mode.id));assert(row);
  assert(row.textContent.includes(String(mode.ram_bytes_per_page??mode.bytes_per_framebuffer)));
  if(mode.bits_per_pixel)assert.equal(row.children[5].textContent,mode.double_buffering?'Yes':'No');
 }
 const headings=[...panel.querySelectorAll('summary')].map(x=>x.textContent.toLowerCase());
 assert(!headings.includes('text mode'));assert(!headings.includes('graphics modes'));assert(!headings.includes('bitmap mode'));
 assert(!panel.textContent.includes('used / free'));
 assert(!panel.textContent.includes('0 sprites'));
 assert.equal(tables[0].querySelectorAll('thead th').length,id.includes('artemis')?6:5);
 assert.equal(tables[1].querySelectorAll('thead th').length,id.includes('artemis')?7:6);
 assert(panel.textContent.includes('All modes support five sprites')); 
}
dom.window.close();console.log('PASS: full MMU content, single Property/Value table, nested sections, bulk controls and escaped values.');

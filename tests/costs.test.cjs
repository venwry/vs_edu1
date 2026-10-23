const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'..'),read=n=>fs.readFileSync(path.join(root,n),'utf8'),model=require('../data-store.js').read('generated/models/manufacturing-costs.json');
(async()=>{
 const dom=new JSDOM('<div id="app"></div>',{url:'https://atlas.test/manufacturing-costs.html',runScripts:'outside-only'}),w=dom.window;w.eval(read('data-store.js'));w.eval(read('manufacturing-costs.js'));w.document.getElementById('app').innerHTML=w.costTemplate;w.fetch=async()=>({ok:true,json:async()=>model});await w.startCostAssessment();const d=w.document;
 assert(d.getElementById('dated-costs').textContent.includes('November'));assert(d.getElementById('dated-costs').textContent.includes('461.30'));
assert.equal(d.querySelectorAll('.cost-table tbody tr').length,model.products.length);assert.equal(d.querySelectorAll('.cost-table thead th').length,6);
 assert(d.getElementById('cost-sourcing').textContent.includes('1979-10'));assert(d.getElementById('cost-sourcing').textContent.includes('330,000'));assert(d.querySelector('[data-cost-row="device.apple2_video_card"][data-cost-year="1979"]'));
 for(const ref of ['bundle.artemis_budget_128','bundle.artemis_budget_128_hdd']){d.querySelector('[data-cost-row="'+ref+'"][data-cost-year="1982"]').click();assert(d.getElementById('cost-detail').textContent.includes('Budget'));assert(!/NaN|undefined/.test(d.getElementById('cost-detail').textContent));}
 const button=d.querySelector('[data-cost-row="computer.aurelia"][data-cost-year="1978"]');button.click();assert(!d.getElementById('cost-detail').hidden);assert(d.getElementById('cost-detail').textContent.includes('Workforce'));assert(d.getElementById('cost-detail').textContent.includes('Freight'));assert(d.getElementById('cost-detail').textContent.includes('24'));
 d.getElementById('cost-close').click();assert(d.getElementById('cost-detail').hidden);
 assert(!d.querySelector('[data-cost-row="computer.aurelia_plus"][data-cost-year="1979"]'));
 d.getElementById('cost-group').value='Bundles';d.getElementById('cost-group').dispatchEvent(new w.Event('change'));assert.equal(d.querySelectorAll('.cost-table tbody tr').length,model.products.filter(p=>p.group==='Bundles').length);
 d.getElementById('cost-available').value='1978';d.getElementById('cost-available').dispatchEvent(new w.Event('change'));assert.equal(d.querySelectorAll('.cost-table tbody tr').length,2);
 d.getElementById('cost-search').value='no match';d.getElementById('cost-search').dispatchEvent(new w.Event('input'));assert(d.getElementById('cost-matrix').textContent.includes('No matching'));
 dom.window.close();console.log('PASS: all cost rows, five-year matrix, unavailable cells, filters and detailed breakdowns.');
})();



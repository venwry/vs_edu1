const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'..'),read=n=>fs.readFileSync(path.join(root,n),'utf8'),model=JSON.parse(read('manufacturing_costs.json'));
(async()=>{
 const dom=new JSDOM('<div id="app"></div>',{url:'https://atlas.test/manufacturing-costs.html',runScripts:'outside-only'}),w=dom.window;w.eval(read('manufacturing-costs.js'));w.document.getElementById('app').innerHTML=w.costTemplate;w.fetch=async()=>({ok:true,json:async()=>model});await w.startCostAssessment();const d=w.document;
 assert.equal(d.querySelectorAll('.cost-table tbody tr').length,model.products.length);assert.equal(d.querySelectorAll('.cost-table thead th').length,5);
 const button=d.querySelector('[data-cost-row="computer.aurelia"][data-cost-year="1978"]');button.click();assert(!d.getElementById('cost-detail').hidden);assert(d.getElementById('cost-detail').textContent.includes('Workforce'));assert(d.getElementById('cost-detail').textContent.includes('Freight'));assert(d.getElementById('cost-detail').textContent.includes('24'));
 d.getElementById('cost-close').click();assert(d.getElementById('cost-detail').hidden);
 assert(!d.querySelector('[data-cost-row="computer.aurelia_plus"][data-cost-year="1979"]'));
 d.getElementById('cost-group').value='Bundles';d.getElementById('cost-group').dispatchEvent(new w.Event('change'));assert.equal(d.querySelectorAll('.cost-table tbody tr').length,12);
 d.getElementById('cost-available').value='1978';d.getElementById('cost-available').dispatchEvent(new w.Event('change'));assert.equal(d.querySelectorAll('.cost-table tbody tr').length,2);
 d.getElementById('cost-search').value='no match';d.getElementById('cost-search').dispatchEvent(new w.Event('input'));assert(d.getElementById('cost-matrix').textContent.includes('No matching'));
 dom.window.close();console.log('PASS: all cost rows, four-year matrix, unavailable cells, filters and detailed breakdowns.');
})();

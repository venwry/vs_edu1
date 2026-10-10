const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'..'),read=n=>fs.readFileSync(path.join(root,n),'utf8'),model=JSON.parse(read('pricing_results.json'));
(async()=>{const dom=new JSDOM('<div id="app"></div>',{url:'https://atlas.test/pricing.html',runScripts:'outside-only'}),w=dom.window;w.eval(read('pricing.js'));w.document.getElementById('app').innerHTML=w.pricingTemplate;w.fetch=async()=>({ok:true,json:async()=>model});await w.startPricing();const d=w.document;
assert.equal(d.querySelectorAll('.pricing-row').length,79);assert.equal(d.querySelectorAll('.pricing-group').length,10);assert.equal(d.querySelectorAll('.pricing-table thead tr:nth-child(2) th').length,24);
const select=(id,value)=>{d.getElementById(id).value=value;d.getElementById(id).dispatchEvent(new w.Event('change'));};
const first=d.querySelector('[data-product="bundle.aurelia_mono"][data-year="1978"]');first.click();assert(d.getElementById('pricing-detail').textContent.includes('North Star'));
select('pricing-fee','0.30');let s=model.products.find(p=>p.id==='bundle.aurelia_mono').snapshots['1978'];assert(d.getElementById('pricing-detail').textContent.includes((s.retail_price_usd*.3).toLocaleString('en-US',{style:'currency',currency:'USD'})));
d.querySelector('[data-product="service.academy_regular_courses.course_1"][data-year="1978"]').click();assert(d.getElementById('pricing-detail').textContent.includes('$69.19 purchase credit'));assert(d.getElementById('pricing-detail').textContent.includes('50% of Fundamentals tuition'));first.click();
const v=w.pricingCalculate(s,.30);assert.equal(v.profit,Math.round((s.retail_price_usd*.7-s.manufacturing_cost_usd)*100)/100);
select('pricing-cost','cost_high_usd');assert(d.getElementById('pricing-detail').textContent.includes('selected cost'));
select('pricing-year','1979');assert(!d.querySelector('[data-product="bundle.aurelia_plus_mono"]'));assert.equal(d.querySelectorAll('.pricing-table thead tr:nth-child(2) th').length,6);
select('pricing-year','1981');select('pricing-availability','available');assert(!d.querySelector('[data-product="bundle.artemis_pro_512_server"]'));
select('pricing-type','Support');assert.equal(d.querySelectorAll('.pricing-row').length,4);assert(d.querySelector('.pricing-row').textContent.includes('0%'));
d.getElementById('pricing-search').value='no such product';d.getElementById('pricing-search').dispatchEvent(new w.Event('input'));assert(d.getElementById('pricing-matrix').textContent.includes('No matching'));
w.close();console.log('PASS: grouped annual matrix, source detail, fee/cost recalculation, service channels and availability filters.');})();


const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'..'),read=n=>fs.readFileSync(path.join(root,n),'utf8'),model=JSON.parse(read('pricing_results.json'));
(async()=>{const dom=new JSDOM('<div id="app"></div>',{url:'https://atlas.test/pricing.html',runScripts:'outside-only'}),w=dom.window;w.eval(read('pricing.js'));w.document.getElementById('app').innerHTML=w.pricingTemplate;w.fetch=async url=>({ok:true,json:async()=>url.includes('retail_catalog')?JSON.parse(read('retail_catalog_1982_results.json')):model});await w.startPricing();const d=w.document;
assert(d.getElementById('dated-prices').textContent.includes('November'));assert(d.getElementById('dated-prices').textContent.includes('461.30'));
assert.equal(d.querySelectorAll('.pricing-row').length,model.products.length);assert.equal(d.querySelectorAll('.pricing-group').length,10);assert.equal(d.querySelectorAll('.pricing-table thead tr:nth-child(2) th').length,6);
assert.equal(d.getElementById('catalog-date').value,'1982-06-15');
assert.equal(d.getElementById('catalog-date').options.length,10);
assert.equal(d.querySelectorAll('#solutions + p + .solution-grid .solution-card').length,6);
assert.equal(d.querySelectorAll('#solution-upgrades + .solution-grid .solution-card').length,5);
assert.equal(d.getElementById('historical-pricing').open,false);
assert(!d.getElementById('solution-professional_cad'));
assert(d.getElementById('solution-professional_drawing').textContent.includes('$1,496.62'));
assert(!d.getElementById('retail-catalog').textContent.includes('Could not load'));
for(const year of ['1978','1979','1980','1981','1982']){
 d.getElementById('catalog-date').value=year+'-06-15';d.getElementById('catalog-date').dispatchEvent(new w.Event('change'));
 assert(d.getElementById('catalog-date-status').textContent.includes(year+'-06-15'));
 assert.equal(d.getElementById('pricing-year').value,year);
 assert.equal(!!d.getElementById('solution-mouse_starter'),year==='1982');
 assert.equal(!!d.getElementById('solution-office_professional'),Number(year)>=1980);
 if(Number(year)<1980)assert(!d.getElementById('solution-office_essentials').textContent.includes('Aurelia+'));
}
for(const year of ['1978','1979','1980','1981','1982']){
 d.getElementById('catalog-date').value=year+'-12-15';d.getElementById('catalog-date').dispatchEvent(new w.Event('change'));
 assert(d.getElementById('catalog-date-status').textContent.includes(year+'-12-15'));
 assert(!d.getElementById('catalog-retry'));
 assert.equal(!!d.getElementById('solution-professional_cad'),year==='1982');
 assert.equal(!!d.getElementById('solution-development_team'),Number(year)>=1981);
 if(year==='1979')assert(d.getElementById('solution-office_essentials').textContent.includes('Aurelia+'));
 if(year==='1980')assert(d.getElementById('solution-office_professional').textContent.includes('Abacus 3'));
 if(year==='1982')assert(d.getElementById('solution-professional_drawing').textContent.includes('$1,604.80'));
}
d.getElementById('pricing-year').value='';d.getElementById('pricing-year').dispatchEvent(new w.Event('change'));
const style=d.createElement('style');style.textContent=read('pricing.css');d.head.append(style);const matrix=d.getElementById('pricing-matrix');assert.equal(w.getComputedStyle(matrix).resize,'both');assert.equal(w.getComputedStyle(matrix).overflow,'auto');matrix.style.width='640px';matrix.style.height='320px';
const select=(id,value)=>{d.getElementById(id).value=value;d.getElementById(id).dispatchEvent(new w.Event('change'));};
const first=d.querySelector('[data-product="bundle.aurelia_mono"][data-year="1978"]');first.click();assert(d.getElementById('pricing-detail').textContent.includes('North Star'));
select('pricing-fee','0.30');let s=model.products.find(p=>p.id==='bundle.aurelia_mono').snapshots['1978'];assert(d.getElementById('pricing-detail').textContent.includes((Math.floor((Math.round(s.retail_price_usd*100)*30+50)/100)/100).toLocaleString('en-US',{style:'currency',currency:'USD'})));
d.querySelector('[data-product="service.academy_regular_courses.course_1"][data-year="1978"]').click();assert(d.getElementById('pricing-detail').textContent.includes(model.products.find(p=>p.id==='service.academy_regular_courses.course_1').snapshots['1978'].before_you_buy_variant.voucher_face_value_usd.toLocaleString('en-US',{style:'currency',currency:'USD'})+' purchase credit'));assert(d.getElementById('pricing-detail').textContent.includes('50% of Fundamentals tuition'));first.click();
const v=w.pricingCalculate(s,.30);assert.equal(Math.round(v.profit*100),Math.round(s.retail_price_usd*100)-Math.round(v.fee*100)-Math.round(s.manufacturing_cost_usd*100));assert.equal(w.pricingCalculate({retail_price_usd:1668.05,manufacturing_cost_usd:751.18},.30).fee,500.42);
select('pricing-cost','cost_high_usd');assert(d.getElementById('pricing-detail').textContent.includes('selected cost'));
select('pricing-year','1979');assert(!d.querySelector('[data-product="bundle.aurelia_plus_mono"]'));assert.equal(d.querySelectorAll('.pricing-table thead tr:nth-child(2) th').length,6);
select('pricing-year','1981');select('pricing-availability','available');assert(!d.querySelector('[data-product="bundle.artemis_pro_512_server"]'));
select('pricing-year','1982');assert(d.querySelector('[data-product="software.aion_development_team"][data-year="1982"]'));
assert(d.getElementById('team-adoption').textContent.includes('$745.23'));
d.querySelector('[data-product="software.aion_development_team"][data-year="1982"]').click();assert(d.getElementById('pricing-detail').textContent.includes('approved below-cost adoption price'));assert(!d.getElementById('pricing-detail').textContent.includes('target contribution margin is 25%'));
select('pricing-type','Support');assert.equal(d.querySelectorAll('.pricing-row').length,4);assert(d.querySelector('.pricing-row').textContent.includes('0%'));
d.getElementById('pricing-search').value='no such product';d.getElementById('pricing-search').dispatchEvent(new w.Event('input'));assert(d.getElementById('pricing-matrix').textContent.includes('No matching'));
assert.equal(matrix.style.width,'640px');assert.equal(matrix.style.height,'320px');w.close();console.log('PASS: grouped annual matrix, source detail, fee/cost recalculation, service channels and availability filters.');})();




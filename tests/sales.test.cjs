const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{JSDOM}=require('jsdom');
const R=path.resolve(__dirname,'..'),read=n=>fs.readFileSync(path.join(R,n),'utf8'),model=JSON.parse(read('sales_forecast.json'));
(async()=>{const dom=new JSDOM('<div id="app"></div>',{url:'https://atlas.test/sales.html',runScripts:'outside-only'}),w=dom.window;w.eval(read('sales.js'));w.document.getElementById('app').innerHTML=w.salesTemplate;w.fetch=async()=>({ok:true,json:async()=>model});await w.startSales();const d=w.document;
assert.equal(d.querySelectorAll('#sales-calendar tbody tr').length,60);
assert(d.getElementById('sales-coverage').textContent.includes('1982-12-31'));
assert.deepEqual([...d.getElementById('sales-year').options].map(x=>x.value),['all','1978','1979','1980','1981','1982']);
for(const forecast of model.reassessed_1980_1982.scenarios){
 const legacy=model.scenarios.find(x=>x.id===forecast.id);
 for(const year of ['1980','1981','1982']){
  const monthly=w.salesCalendarRows(legacy,'month',year,forecast),quarterly=w.salesCalendarRows(legacy,'quarter',year,forecast),annual=w.salesCalendarRows(legacy,'year',year,forecast);
  assert.equal(monthly.length,12);assert.equal(quarterly.length,4);assert.equal(annual.length,1);
  const expected=forecast.annual.find(x=>x.year===Number(year)).computer_units;
  for(const rows of [monthly,quarterly,annual]){
   assert.equal(rows.reduce((n,r)=>n+r.units,0),expected);
   for(const row of rows){assert.equal(row.units,Object.values(row.products).reduce((a,b)=>a+b,0));assert(!row.partial);assert.equal(row.financialAvailable,false);}
  }
  d.getElementById('sales-scenario').value=forecast.id;d.getElementById('sales-year').value=year;d.getElementById('sales-year').dispatchEvent(new w.Event('change'));
  assert.equal(d.querySelectorAll('#sales-calendar tbody tr').length,12);
  assert(d.querySelector('#sales-calendar tfoot').textContent.includes(expected.toLocaleString('en-US')));
  assert(!/NaN|undefined/.test(d.querySelector('#sales-calendar').textContent));
 }
}
d.getElementById('sales-basis').value='historical';d.getElementById('sales-basis').dispatchEvent(new w.Event('change'));
assert.equal(d.getElementById('sales-year').value,'all');
d.getElementById('sales-scenario').value='central';d.getElementById('sales-scenario').dispatchEvent(new w.Event('change'));
const central=model.scenarios.find(s=>s.id==='central');assert(d.getElementById('sales-content').textContent.includes(central.calendar_1978.units.toLocaleString('en-US')));assert(d.getElementById('sales-content').textContent.includes(central.launch_year.units.toLocaleString('en-US')));assert.equal(d.querySelectorAll('#sales-calendar tbody tr').length,35);assert.equal(d.querySelector('#sales-calendar tbody tr').dataset.period,'1978-01');
for(const sc of model.scenarios){d.getElementById('sales-scenario').value=sc.id;d.getElementById('sales-scenario').dispatchEvent(new w.Event('change'));assert(d.getElementById('sales-status').textContent.includes(sc.title));assert(d.getElementById('sales-content').textContent.includes(sc.calendar_1978.units.toLocaleString('en-US')));assert.equal(d.querySelectorAll('#demand-1979 tbody tr').length,6);assert(d.getElementById('sales-content').textContent.includes(sc.launch_through_november_1979.units.toLocaleString('en-US')));assert(d.getElementById('sales-content').textContent.includes('1979-11'));assert.equal(d.querySelectorAll('#ncc1980-months tbody tr').length,6);assert.equal(d.querySelectorAll('#comdex1980-months tbody tr').length,7);assert(d.getElementById('sales-content').textContent.includes(sc.launch_through_comdex1980.units.toLocaleString('en-US')));assert.equal(d.querySelectorAll('#academy-months tbody tr').length,12);assert(d.getElementById('sales-content').textContent.includes(sc.launch_through_ncc1980.units.toLocaleString('en-US')));assert(d.getElementById('sales-content').textContent.includes(sc.academy_comdex_to_ncc1980.enrolments.toLocaleString('en-US')));}

const change=(id,value)=>{d.getElementById(id).value=value;d.getElementById(id).dispatchEvent(new w.Event('change'));};
const fields=['customer_retail_spend_usd','supplier_revenue_after_channel_usd','recurring_cost_usd','unit_contribution_total_usd'];
for(const scenario of model.scenarios){
 const month=w.salesCalendarRows(scenario,'month'),quarter=w.salesCalendarRows(scenario,'quarter'),annual=w.salesCalendarRows(scenario,'year');
 assert.equal(month.length,35);assert.equal(quarter.length,12);assert.equal(annual.length,3);
 const sources=['months','post_ncc_months','comdex_to_ncc1980_months','ncc_to_comdex1980_months'].flatMap(k=>scenario[k]);
 const total=sources.reduce((n,r)=>n+r.units,0);assert.equal(total,scenario.launch_through_comdex1980.units);
 for(const rows of [month,quarter,annual]){
  assert.equal(rows.reduce((n,r)=>n+r.units,0),total);
  for(const r of rows)assert.equal(r.units,Object.values(r.products).reduce((a,b)=>a+b,0));
  for(const f of fields)assert.equal(rows.reduce((n,r)=>n+r.cents[f],0),sources.reduce((n,r)=>n+Math.round(r[f]*100),0));
 }
 assert.equal(month.filter(r=>r.key==='1980-05').length,1);
 const may=month.find(r=>r.key==='1980-05');assert.equal(may.units,sources.filter(r=>r.month==='1980-05').reduce((n,r)=>n+r.units,0));assert.equal(may.partial,false);
 assert.equal(month.at(-1).key,'1980-11');assert.equal(month.at(-1).end,'1980-11-18');assert(month.at(-1).partial);
 assert(quarter.at(-1).partial);assert(annual.at(-1).partial);assert(!annual[0].partial);assert(!annual[1].partial);
 assert.equal(annual[0].units,scenario.calendar_1978.units);assert.equal(annual[1].units,scenario.calendar_1979.units);assert.equal(annual[2].units,scenario.calendar_1980_to_comdex.units);
 const filtered=w.salesCalendarRows(scenario,'month','1979');assert.equal(filtered.length,12);assert.equal(filtered[0].cumulative,scenario.months.find(r=>r.month==='1979-01').cumulative_units);
 change('sales-scenario',scenario.id);change('sales-period','quarter');assert.equal(d.querySelectorAll('#sales-calendar tbody tr').length,12);
 change('sales-period','year');assert.equal(d.querySelectorAll('#sales-calendar tbody tr').length,3);
 change('sales-year','1980');assert.equal(d.querySelectorAll('#sales-calendar tbody tr').length,1);assert(d.querySelector('#sales-calendar').textContent.includes('Partial'));
 assert(!/NaN|undefined/.test(d.querySelector('#sales-calendar').textContent));change('sales-year','all');change('sales-period','month');
}
let exported;w.Blob=Blob;w.URL.createObjectURL=b=>{exported=b;return 'blob:test';};w.URL.revokeObjectURL=()=>{};w.HTMLAnchorElement.prototype.click=function(){};
change('sales-period','quarter');change('sales-year','1980');d.getElementById('sales-export').click();const csv=await exported.text();assert.equal(csv.split('\r\n').length,5);assert(csv.includes('1980-Q4,1980-10-01,1980-11-18,true'));
change('sales-basis','current');change('sales-scenario','central');change('sales-year','1982');
d.getElementById('sales-export').click();const currentCSV=await exported.text();
assert.equal(currentCSV.split('\r\n').length,5);assert(currentCSV.includes('artemis_pro'));assert(currentCSV.includes('1982-Q4,1982-10-01,1982-12-31,false'));
const records=currentCSV.split('\r\n').slice(1).map(x=>x.split(','));assert.equal(records.reduce((n,r)=>n+Number(r[8]),0),119389);assert(records.every(r=>r.slice(-4).every(x=>x==='')));
change('sales-period','year');assert.equal(d.querySelectorAll('#sales-calendar tbody tr').length,1);assert(d.querySelector('#sales-calendar').textContent.includes('119,389'));
w.location.hash='#academy-demand';w.onhashchange();assert(d.getElementById('sales-source-details').open);

w.fetch=async()=>({ok:false,status:503});await w.startSales();assert(d.getElementById('sales-retry'));w.fetch=async()=>({ok:true,json:async()=>model});await w.startSales();assert(!d.getElementById('sales-retry'));w.close();console.log('PASS: continuous monthly/quarterly/annual reconciliation, split May, partial periods, filters, CSV, legacy anchors and fetch-error recovery.');})();


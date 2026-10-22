const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{JSDOM}=require('jsdom');
const R=path.resolve(__dirname,'..'),read=n=>fs.readFileSync(path.join(R,n),'utf8'),model=JSON.parse(read('sales_forecast.json'));
(async()=>{const dom=new JSDOM('<div id="app"></div>',{url:'https://atlas.test/sales.html',runScripts:'outside-only'}),w=dom.window;w.eval(read('sales.js'));w.document.getElementById('app').innerHTML=w.salesTemplate;w.fetch=async()=>({ok:true,json:async()=>model});await w.startSales();const d=w.document;
const change=(id,v)=>{d.getElementById(id).value=v;d.getElementById(id).dispatchEvent(new w.Event('change'));};
const fields=['customer_retail_spend_usd','supplier_revenue_after_channel_usd','recurring_cost_usd','unit_contribution_total_usd'];
assert(!d.getElementById('sales-basis'));assert(!d.getElementById('sales-source-details'));assert.equal(d.querySelectorAll('#sales-calendar tbody tr').length,72);
assert.deepEqual([...d.getElementById('sales-year').options].map(x=>x.value),['all','1978','1979','1980','1981','1982','1983']);
for(const sc of model.scenarios){
 change('sales-scenario',sc.id);
 for(const year of ['1978','1979','1980','1981','1982','1983']){
  change('sales-year',year);const expected=sc.annual.find(r=>r.year===+year);
  for(const [grain,count] of [['month',12],['quarter',4],['year',1]]){
   change('sales-period',grain);const rows=w.salesCalendarRows(sc,grain,year);assert.equal(rows.length,count);assert.equal(d.querySelectorAll('#sales-calendar tbody tr').length,count);
   assert.equal(rows.reduce((n,r)=>n+r.units,0),expected.computer_units);
   for(const f of fields)assert.equal(rows.reduce((n,r)=>n+r.cents[f],0),Math.round(expected[f]*100));
   assert(!/NaN|undefined|—/.test(d.querySelector('#sales-calendar').textContent));
   assert(d.querySelector('#sales-calendar tfoot').textContent.includes(expected.customer_retail_spend_usd.toLocaleString('en-US',{style:'currency',currency:'USD'})));
  }
 }
}
let exported;w.Blob=Blob;w.URL.createObjectURL=b=>{exported=b;return 'blob:test';};w.URL.revokeObjectURL=()=>{};w.HTMLAnchorElement.prototype.click=function(){};
change('sales-scenario','central');change('sales-year','1982');change('sales-period','quarter');d.getElementById('sales-export').click();
const csv=await exported.text(),records=csv.split('\r\n').slice(1).map(r=>r.split(','));assert.equal(records.length,4);assert(csv.includes('artemis_pro'));assert.equal(records.reduce((n,r)=>n+Number(r[8]),0),202412);
const annual=model.scenarios.find(s=>s.id==='central').annual.find(r=>r.year===1982);for(let k=0;k<4;k++)assert.equal(records.reduce((n,r)=>n+Math.round(Number(r[10+k])*100),0),Math.round(annual[fields[k]]*100));
w.fetch=async()=>({ok:false,status:503});await w.startSales();assert(d.getElementById('sales-retry'));w.fetch=async()=>({ok:true,json:async()=>model});await w.startSales();assert(!d.getElementById('sales-retry'));w.close();console.log('PASS: current-only sales, all years/scenarios/periods, priced financial columns, exact CSV totals and fetch recovery.');})();


(()=>{'use strict';
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num=x=>new Intl.NumberFormat('en-US').format(x),money=x=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(x),exact=x=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(x);
const financialFields=['customer_retail_spend_usd','supplier_revenue_after_channel_usd','recurring_cost_usd','unit_contribution_total_usd'];
const families=['aurelia','aurelia_plus','artemis','artemis_pro'];
const monthEnd=month=>new Date(Date.UTC(Number(month.slice(0,4)),Number(month.slice(5,7)),0)).toISOString().slice(0,10);
function calendarRows(s,grain='month',year='all'){
 const sources=s.monthly.map(r=>({...r,units:r.computer_units,products:Object.fromEntries(families.map(f=>[f,{units:r.products[f]}]))}));
 const monthly=new Map();
 for(const x of sources){
  const key=x.month,start=x.period_start||key+'-01',end=x.period_end||monthEnd(key);
  if(!monthly.has(key))monthly.set(key,{key,start,end,units:0,financialAvailable:true,products:Object.fromEntries(families.map(f=>[f,0])),cents:Object.fromEntries(financialFields.map(f=>[f,0]))});
  const row=monthly.get(key);row.start=row.start<start?row.start:start;row.end=row.end>end?row.end:end;row.units+=x.units;row.financialAvailable&&=x.financialAvailable!==false;
  for(const f of families)row.products[f]+=x.products?.[f]?.units??(f==='aurelia'?x.units:0);
  for(const f of financialFields)row.cents[f]+=Math.round((x[f]||0)*100);
 }
 const grouped=new Map();let cumulative=0;
 for(const row of [...monthly.values()].sort((a,b)=>a.key.localeCompare(b.key))){
  cumulative+=row.units;
  if(year!=='all'&&!row.key.startsWith(year))continue;
  const y=row.key.slice(0,4),q=Math.floor((Number(row.key.slice(5))-1)/3)+1;
  const key=grain==='year'?y:grain==='quarter'?`${y}-Q${q}`:row.key;
  if(!grouped.has(key))grouped.set(key,{key,start:row.start,end:row.end,units:0,financialAvailable:true,products:Object.fromEntries(families.map(f=>[f,0])),cents:Object.fromEntries(financialFields.map(f=>[f,0]))});
  const g=grouped.get(key);g.end=row.end;g.units+=row.units;g.financialAvailable&&=row.financialAvailable;g.cumulative=cumulative;
  for(const f of families)g.products[f]+=row.products[f];
  for(const f of financialFields)g.cents[f]+=row.cents[f];
 }
 return [...grouped.values()].map(g=>{
  const y=g.key.slice(0,4),quarter=Number(g.key.slice(-1));
  const first=grain==='year'?`${y}-01`:grain==='quarter'?`${y}-${String((quarter-1)*3+1).padStart(2,'0')}`:g.key;
  const last=grain==='year'?`${y}-12`:grain==='quarter'?`${y}-${String(quarter*3).padStart(2,'0')}`:g.key;
  return {...g,partial:g.start!==first+'-01'||g.end!==monthEnd(last),...Object.fromEntries(financialFields.map(f=>[f,g.cents[f]/100]))};
 });
}
window.salesCalendarRows=calendarRows;
function calendarChart(rows){
 const width=1000,height=270,left=65,right=20,top=20,bottom=55,plot=height-top-bottom,max=Math.max(1,...rows.map(r=>r.units));
 const step=(width-left-right)/Math.max(1,rows.length),bar=Math.min(100,step*.72),colors=['#70c7b5','#86a9ed','#e9b46f','#d39bea'];
 let svg='';
 for(let i=0;i<=4;i++){const y=top+plot-i*plot/4;svg+=`<line x1="${left}" x2="${width-right}" y1="${y}" y2="${y}" stroke="currentColor" opacity=".15"/><text x="${left-10}" y="${y+4}" text-anchor="end">${num(Math.round(max*i/4))}</text>`;}
 rows.forEach((r,i)=>{let y=top+plot;const x=left+step*i+(step-bar)/2;
  families.forEach((f,j)=>{const h=r.products[f]/max*plot;y-=h;svg+=`<rect x="${x}" y="${y}" width="${bar}" height="${h}" fill="${colors[j]}"${r.partial?' opacity=".65"':''}><title>${esc(r.key)}${r.partial?' (partial)':''} · ${['Aurelia','Aurelia+','Artemis','Artemis PRO'][j]}: ${num(r.products[f])}</title></rect>`;});
  if(rows.length<=12||i%Math.ceil(rows.length/10)===0||i===rows.length-1)svg+=`<text x="${x+bar/2}" y="${height-25}" text-anchor="middle">${esc(r.key)}${r.partial?'*':''}</text>`;
 });
 return `<div class="sales-chart"><svg viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="sales-chart-title sales-chart-desc"><title id="sales-chart-title">Computer deliveries by calendar period</title><desc id="sales-chart-desc">Stacked Aurelia, Aurelia+, Artemis and Artemis PRO deliveries. Partial periods are lighter and marked with an asterisk. Exact figures follow in the table.</desc>${svg}</svg></div><div class="sales-legend"><span style="--series:#70c7b5">Aurelia</span><span style="--series:#86a9ed">Aurelia+</span><span style="--series:#e9b46f">Artemis</span><span style="--series:#d39bea">Artemis PRO</span><small>* Partial period; not annualized</small></div>`;
}
function calendarOverview(s,rows,grain){
 const total={units:0,financialAvailable:true,products:Object.fromEntries(families.map(f=>[f,0])),cents:Object.fromEntries(financialFields.map(f=>[f,0]))};
 rows.forEach(r=>{total.units+=r.units;total.financialAvailable&&=r.financialAvailable;families.forEach(f=>total.products[f]+=r.products[f]);financialFields.forEach(f=>total.cents[f]+=r.cents[f]);});
 const first=rows[0],last=rows.at(-1),label={month:'Monthly',quarter:'Quarterly',year:'Annual'}[grain];
 const card=(l,v,n)=>`<article><span>${l}</span><strong>${v}</strong><small>${n}</small></article>`;
 const cells=r=>`${families.map(f=>`<td>${num(r.products[f])}</td>`).join('')}<td><strong>${num(r.units)}</strong></td><td>${num(r.cumulative)}</td>${financialFields.map(f=>`<td>${r.financialAvailable?exact(r.cents[f]/100):"—"}</td>`).join('')}`;
 return `<section aria-labelledby="sales-calendar-heading"><h2 id="sales-calendar-heading">${label} sales · ${esc(s.title)}</h2><p id="sales-coverage">Selected coverage: <strong>${esc(first.start)}–${esc(last.end)}</strong>. Current forecast through December 31, 1983. January–May 1978 are documented pre-launch zeros; later missing months are not filled with zeros.</p><div class="sales-kpis">${card('Computers delivered',num(total.units),'Sum of selected periods')}${card('Customer retail spend',total.financialAvailable?money(total.cents.customer_retail_spend_usd/100):"—",'Computer packages only')}${card('Receipts after channel fees',total.financialAvailable?money(total.cents.supplier_revenue_after_channel_usd/100):"—",'Computer packages only')}${card('Recurring contribution',total.financialAvailable?money(total.cents.unit_contribution_total_usd/100):"—",'Before marketing, R&D, capital and tax')}</div>${calendarChart(rows)}<div class="sales-table-wrap" tabindex="0" role="region" aria-label="Sales by calendar period"><table id="sales-calendar"><caption>${label} computer sales and package financials, nominal USD. Financials are calculated from dated retail prices and weighted basket quantities. Cumulative deliveries always start at launch, even with a year filter.</caption><thead><tr><th scope="col">Period / coverage</th><th scope="col">Aurelia</th><th scope="col">Aurelia+</th><th scope="col">Artemis</th><th scope="col">Artemis PRO</th><th scope="col">Total units</th><th scope="col">Cumulative units</th><th scope="col">Retail spend</th><th scope="col">After channel fees</th><th scope="col">Recurring cost</th><th scope="col">Contribution</th></tr></thead><tbody>${rows.map(r=>`<tr data-period="${esc(r.key)}"><th scope="row">${esc(r.key)}${r.partial?' <span class="sales-partial">Partial</span>':''}<small>${esc(r.start)}–${esc(r.end)}</small></th>${cells(r)}</tr>`).join('')}</tbody><tfoot><tr><th scope="row">Selected total</th>${cells({...total,cumulative:last.cumulative})}</tr></tfoot></table></div><p class="sales-callout">Retail spend = quantity × dated retail price. After channel fees uses the pricing model’s net receipts. Recurring cost uses the same offering’s manufacturing cost. Contribution = after-channel receipts − recurring cost, before development, marketing, capital/depreciation and tax. Weighted offer lines are rounded to cents and then summed. These are computer-package totals; standalone Team Edition, BPI, cards, upgrades and Academy tuition are included separately in ROI.</p><p>Dated June/December catalogue assessments apply. 1983 holds December 1982 unit prices and costs. CAD systems replace ordinary PRO sales; upgrades and independent partner computer sales do not increase Logix computer totals. <a href="pricing.html">Retail pricing</a> · <a href="market-share.html">Quarterly market share and clones</a> · <a href="roi.html">Quarterly ROI</a>.</p></section>`;
}
window.salesTemplate=`<main class="sales-main"><div class="eyebrow">Alternative history · current forecast</div><h1 class="page-title">Logix computer demand and sales</h1><p class="sales-lead">One current forecast, 1978–1983. Compare monthly, quarterly and annual sales for Aurelia, Aurelia+, Artemis and Artemis PRO, with retail spend, receipts after channel fees, recurring cost and contribution. Reassessed task-bundle demand includes explicit clone cannibalisation. Incremental manufacturing capacity is budgeted as a planning allowance; conservative and strong cases vary demand and programme costs.</p><div class="sales-controls"><label>Scenario<select id="sales-scenario"><option value="conservative">Conservative</option><option value="central" selected>Central</option><option value="strong">Strong</option></select></label><label>Period<select id="sales-period"><option value="month">Monthly</option><option value="quarter">Quarterly</option><option value="year">Annually</option></select></label><label>Year<select id="sales-year"><option value="all">All available years</option></select></label><button id="sales-export" type="button">Export selected CSV</button><a href="pricing.html">Retail pricing</a> · <a href="market-share.html">Quarterly market share and clones</a><a href="generated/models/sales-forecast.json" download>Download forecast JSON</a></div><p id="sales-status" role="status">Loading forecast…</p><div id="sales-content"></div></main>`;
window.startSales=async()=>{const $=id=>document.getElementById(id);let m;try{const r=await fetch('./generated/models/sales-forecast.json',{cache:'no-store'});if(!r.ok)throw Error(r.status);m=await r.json();}catch(e){$('sales-status').innerHTML='Could not load the forecast. Serve over HTTP. <button id="sales-retry">Retry</button>';$('sales-retry').onclick=window.startSales;return;}
function render(){
 const s=m.scenarios.find(x=>x.id===$('sales-scenario').value),previousYear=$('sales-year').value,years=s.annual.map(r=>String(r.year));
 $('sales-year').innerHTML='<option value="all">All available years</option>'+years.map(y=>`<option value="${y}">${y}</option>`).join('');$('sales-year').value=years.includes(previousYear)?previousYear:'all';
 const grain=$('sales-period').value,rows=calendarRows(s,grain,$('sales-year').value);
 $('sales-content').innerHTML=calendarOverview(s,rows,grain);
 $('sales-status').textContent=`${s.title} scenario · nominal USD · ${rows.length} ${grain==='year'?'annual':grain==='quarter'?'quarterly':'monthly'} periods`;
 $('sales-export').onclick=()=>{
  const headers=['period','coverage_start','coverage_end','partial',...families,'units','cumulative_units',...financialFields];
  const lines=rows.map(r=>[r.key,r.start,r.end,r.partial,...families.map(f=>r.products[f]),r.units,r.cumulative,...financialFields.map(f=>(r.cents[f]/100).toFixed(2))]);
  const csv=[headers,...lines].map(r=>r.join(',')).join('\r\n'),url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download=`logix-sales-${s.id}-${grain}-${$('sales-year').value}.csv`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 };
}
for(const id of ['sales-scenario','sales-period','sales-year'])$(id).onchange=render;
render();};
})();


// Standard-library execution smoke test; full DOM integration is covered by atlas.test.cjs (jsdom).
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'roi.html'),'utf8');const data=html.match(/<script id="roi-model" type="application\/json">([\s\S]*?)<\/script>/)[1],code=html.match(/<\/script><script>([\s\S]*?)<\/script>/)[1];let nodes={};
function node(id){return nodes[id]||(nodes[id]={value:({scenario:'central',year:'all',roiMeasure:'quarterly_pretax_roi_pct',marketingQuarter:'all',marketingEntity:'all'})[id]||'',_html:'',textContent:id==='roi-model'?data:'',get innerHTML(){return this._html},set innerHTML(v){this._html=v;let o=v.match(/<option(?: value="([^"]*)")?>(.*?)<\/option>/);if(o)this.value=o[1]??o[2]},click(){}})}
let ctx={document:{getElementById:node,createElement:()=>({click(){}})},Blob,URL,setTimeout,console};vm.createContext(ctx);vm.runInContext(code,ctx);
assert(node('flows').innerHTML.includes('36 quarters'));assert(!/NaN|undefined/.test(node('flows').innerHTML));assert(/cash payback|Cash payback/.test(node('verdict').innerHTML));
node('year').value='1980';node('year').onchange();assert(node('flows').innerHTML.includes('4 quarters'));assert(node('flows').innerHTML.includes('1980-Q4'));
let baseline=node('kpis').innerHTML;node('scenario').value='high_marketing';node('scenario').onchange();assert.notEqual(node('kpis').innerHTML,baseline);
let previousROI=node('roi').innerHTML;node('roiMeasure').value='cumulative_cash_return_on_peak_funding_pct';node('roiMeasure').onchange();assert.notEqual(node('roi').innerHTML,previousROI);assert(!/NaN|undefined/.test(node('roi').innerHTML));
node('marketingQuarter').value='1978-Q2';node('marketingEntity').value='Logix';node('marketingQuarter').onchange();assert(node('marketingLines').innerHTML.includes('Aurelia celebrity contract'));assert(!node('marketingLines').innerHTML.includes('COMDEX 1980'));
console.log('PASS: report execution, all-quarter chart, year filter, marketing sensitivity, ROI measure and marketing filters');


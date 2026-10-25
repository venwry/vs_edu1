/* Shared read-only BOM presentation. Unknowns and saved estimate boundaries are preserved. */
(function(root){
'use strict';
const resolverAPI=typeof module!=='undefined'&&module.exports?require('./composition-resolver.js'):root.CompositionResolver;
const categories=typeof module!=='undefined'&&module.exports?require('./catalog-categories.js'):root.CatalogCategories;
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const money=v=>Number.isFinite(v)?'$'+v.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}):'Unknown';
// Prefer explicit attribution; editions and BOM parts may inherit from their linked record.
function vendorName(record,records={},seen=new Set()){
 if(!record||seen.has(record))return 'Unknown';seen.add(record);
 for(const key of ['vendor','provider','manufacturer','owner','publisher','developer','supplier']){
  const value=record[key];if(typeof value==='string'&&value.trim())return value.trim();
 }
 for(const key of ['product_ref','catalog_ref'])if(records[record[key]]){const value=vendorName(records[record[key]],records,seen);if(value!=='Unknown')return value;}
 if(record.candidate_manufacturers?.length)return record.candidate_manufacturers.map(x=>x.name+' (candidate)').join(' / ');
 return 'Unknown';
}
function pendingCostReason(assemblies,ids,seen=new Set()){
 for(const id of ids){if(seen.has(id))continue;seen.add(id);const a=assemblies.get(id);if(!a)continue;
  if(a.cost_assessment_status==='pending_reassessment')return 'The 32-bit RAM module revision changes the physical BOM. Current manufacturing costs are unknown pending reassessment; previous evaluations describe the superseded design.';
  const reason=pendingCostReason(assemblies,(a.lines||[]).map(l=>l.ref),seen);if(reason)return reason;
 }
 return '';
}
function releaseDate(record){
 if(record.introduced?.event_name==='no release')return 'no release';
 return record.introduced?.event_start_date||record.available_from||'';
}
function createModel(catalog,bom,cost){
 const records=Object.fromEntries(Object.values(catalog).filter(Array.isArray).flat().filter(r=>r?.id).map(r=>[r.id,r]));
 for(const p of catalog.product_catalog?.products||[])records[p.id]=p;
 for(const c of catalog.computers||[])if(records[c.chassis_ref])records[c.id]={...c,composition_history:records[c.chassis_ref].composition_history};
 const graph=resolverAPI.create(records),assemblies=new Map(),components=new Map((catalog.components||bom.components).map(r=>[r.id,r]));
 const items=new Map();
 function add(r,cl){const category=categories.category(r,records);if(!category)throw Error('Missing canonical category: '+r.id);items.set(r.id,{id:r.id,name:r.name||r.id,class:cl,category,release:releaseDate(r),record:r});}
 for(const r of catalog.components||[])add(r,'Part');
 for(const r of catalog.devices||[])add(r,r.category==='base_computer'?'Base computer':r.virtual?'Internal subsystem':categories.isExpansion(r)?'Expansion':'Peripheral');
 for(const r of catalog.computers||[])add(r,'Computer');
 for(const r of catalog.software_products||[])add(r,'Software product');
 for(const r of catalog.platform_editions||[])add(r,'Software edition');
 for(const r of catalog.external_partner_products||[])add(r,'Software');
 for(const key of ['offered_bundles','proposed_bundles','commercial_offerings'])for(const r of catalog[key]||[])add(r,'Bundle');

 const reviewRows=Object.entries(cost.reviews||{}).flatMap(([key,r])=>[...(r.products||r.prices||[]),...(key==='ncc-1982'?[{id:'software.aion_development_team',name:'AION Development Team',...r.team_launch_price},{id:'software.aion_development_team',name:'AION Development Team',...r.team_1982_price}]:[])].map(row=>({...row,review:key})));
 for(const r of reviewRows)if(!items.has(r.id))throw Error('Missing canonical record for reviewed offering: '+r.id);
 const isMaterial=id=>components.get(id)?.bom_role==='material';
 function assemblyIds(id){return graph.versions(id).length||isMaterial(id)?[id]:[];}
 function rows(id,version){return graph.versions(id).length?graph.resolve(id,{version:version??graph.versions(id).at(-1).version_number}).rows:isMaterial(id)?[{ref:id,quantity:1,unit:'each',condition:'always',quantity_status:'defined',depth:0,name:components.get(id).name}]:[];}
 function renderBOM(id,opts={}){
  const history=graph.versions(id),version=opts.version??history.at(-1)?.version_number;
  let html='<section class="bom-detail" data-composition-owner="'+esc(id)+'"><h3>Bill of materials</h3>';
  if(!history.length)return html+'<p>'+(isMaterial(id)?'This component is a terminal material item. Supplier quotations are not recorded; saved estimates are historical.':'No composition is defined for this element.')+'</p></section>';
  html+='<label>Composition version <select data-composition-version aria-label="Composition version">'+history.map(h=>'<option value="'+h.version_number+'"'+(h.version_number===Number(version)?' selected':'')+'>'+esc(h.valid_from||'Unknown')+' - '+esc(h.valid_to)+'</option>').join('')+'</select></label>';
  try{
   const result=graph.resolve(id,{version});
   html+='<p>Quantities are per parent. Each child uses the version valid at its parent’s start date. End dates are exclusive.</p>';
   if(result.issues.length)html+='<p role="alert">'+result.issues.map(x=>esc(x.message||x.kind+': '+x.ref)).join('<br>')+'</p>';
   html+='<div class="bom-table-scroll"><table><thead><tr><th>Element</th><th>Quantity</th><th>Unit</th><th>Role / condition</th><th>Composition dates</th></tr></thead><tbody>'+result.rows.map(l=>'<tr><td style="padding-left:'+(.5+l.depth)+'rem">'+esc(l.name)+'</td><td>'+esc(l.quantity??'Unknown')+'</td><td>'+esc(l.unit)+'</td><td>'+esc([l.role,l.condition,l.quantity_status].filter(Boolean).join(' · '))+'</td><td>'+esc(l.valid_from?l.valid_from+' - '+l.valid_to:'')+'</td></tr>').join('')+'</tbody></table></div>';
   if(opts.fullRecords&&typeof root.renderSpecification==='function')html+='<details><summary>Composition records and qualification</summary>'+root.renderSpecification({owner:records[id],selected_version:result.version,nested_versions:result.nodes},records)+'</details>';
  }catch(e){html+='<p role="alert">'+esc(e.message)+'</p>';}
  return html+'</section>';
 }
 function costStatus(id,version){
  if(!graph.versions(id).length)return '';
  const result=graph.resolve(id,{version:version??graph.versions(id).at(-1).version_number});
  return result.nodes.some(n=>n.metadata.cost_assessment_status==='pending_reassessment')?'Current manufacturing costs are unknown pending reassessment; saved evaluations describe the superseded design.':'';
 }
 function renderCosts(id,opts={}){
  let html='<section class="bom-detail">';
  const blocked=costStatus(id,opts.version);if(blocked){const dates=[...new Set([...reviewRows.filter(p=>p.id===id).map(p=>p.date||p.cost_date),...(cost.dated_assessments||[]).filter(a=>(a.products||[]).some(p=>p.id===id)).map(a=>a.date)].filter(Boolean))];return html+'<p class="cost-reassessment-pending">'+esc(blocked)+'</p>'+(dates.length?'<p>Archived dated evaluations: '+dates.map(esc).join(', ')+'. These do not establish current manufacturing costs.</p>':'')+'<p><a href="generated/models/manufacturing-costs.json">Archived evaluations of the superseded design</a></p></section>'; }
  const products=cost.products.filter(p=>p.id===id||p.catalog_ref===id||p.historical_variant_refs?.includes(id));
  if(products.some(p=>p.historical_variant_refs?.includes(id)))html+='<p>Historical processor-family estimates below are not speed-bin-specific. They are not new quotations or additional configuration costs.</p>';
  if(products.length){html+='<h3>Recorded costs</h3><p>Nominal USD engineering estimates. Software costs may include media, licensing and delivery. Component and assembly costs overlap; do not add them together.</p>';for(const p of products){html+='<details data-bom-cost="'+esc(p.id)+'" data-cost-id="'+esc(p.id)+'"><summary>'+esc(p.name)+'</summary><div class="bom-table-scroll"><table><thead><tr><th>June 15 evaluation</th><th>Total recurring cost</th><th>Range</th><th>Status</th></tr></thead><tbody>'+Object.entries(p.snapshots||{}).filter(([y,s])=>s.status!=='not_yet_offered'&&(cost.metadata.snapshots||[]).includes(y+'-06-15')).map(([y,s])=>'<tr><td>'+esc(y+'-06-15')+'</td><td>'+money(s.total_usd)+'</td><td>'+money(s.low_usd)+' – '+money(s.high_usd)+'</td><td>'+esc(s.status)+'</td></tr>').join('')+'</tbody></table></div>'+'</details>';}}
  const dated=(cost.dated_assessments||[]).flatMap(a=>(a.products||[]).filter(p=>p.id===id).map(p=>({date:a.date,basis:a.basis,...p})));
  const reviews=reviewRows.filter(p=>p.id===id);
  if(dated.length||reviews.length){html+='<h3>Dated reviews</h3><p>Separate evaluations; do not add review totals to annual estimates. Unknown costs remain unknown.</p><div class="bom-table-scroll"><table><thead><tr><th>Evaluation</th><th>Source</th><th>Recurring cost</th><th>Range</th></tr></thead><tbody>'+reviews.map(p=>'<tr><td>'+esc(p.date||p.cost_date||'Unknown')+'</td><td>'+esc(p.review)+'</td><td>'+money(p.manufacturing_cost_usd)+'</td><td>'+money(p.cost_low_usd)+' – '+money(p.cost_high_usd)+'</td></tr>').join('')+'</tbody></table></div>';
   if(typeof root.renderSpecification==='function')html+='<details><summary>Dated cost decomposition, pricing and assumptions</summary>'+root.renderSpecification({cost_assessments:dated,reviews,review_context:Object.fromEntries([...new Set(reviews.map(r=>r.review))].map(key=>[key,Object.fromEntries(Object.entries(cost.reviews[key]).filter(([k])=>!['products','prices','cost_assessment','team_launch_price','team_1982_price'].includes(k)))]))},records)+'</details>';
  }
  const componentIds=components.has(id)?[id]:[];
  const componentInputs=Object.fromEntries((opts.fullRecords?componentIds:[]).filter(key=>cost.component_cost_assumptions?.[key]).map(key=>[key,cost.component_cost_assumptions[key]]));
  if(Object.keys(componentInputs).length&&typeof root.renderSpecification==='function')html+='<details><summary>Component cost assumptions by year</summary><p>Recorded unit input allowances; these are not additional complete-product costs.</p>'+root.renderSpecification(componentInputs,records)+'</details>';
  if(!products.length&&!dated.length&&!reviews.length&&!Object.keys(componentInputs).length)html+='<p>No manufacturing cost assessment is recorded for this element.</p>';
  return html+'</section>';
 }
 function render(id,opts={}){return renderBOM(id,opts)+renderCosts(id);}
 function bind(host){for(const select of host.querySelectorAll('[data-composition-version]'))select.addEventListener('change',()=>{const section=select.closest('[data-composition-owner]'),id=section.dataset.compositionOwner,version=Number(select.value);section.outerHTML=renderBOM(id,{version,fullRecords:true});bind(host);if(root.bindSpecificationControls)root.bindSpecificationControls(host);host.dispatchEvent(new CustomEvent('compositionchange',{bubbles:true,detail:{ref:id,version}}));});for(const d of host.querySelectorAll('[data-bom-cost]'))d.addEventListener('toggle',()=>{if(!d.open||d.dataset.loaded)return;d.dataset.loaded='true';const p=cost.products.find(p=>p.id===d.dataset.bomCost);d.insertAdjacentHTML('beforeend',root.renderSpecification(p,records));root.bindSpecificationControls(d);});}
 return {bind,records,items:[...items.values()].sort((a,b)=>a.name.localeCompare(b.name)||a.id.localeCompare(b.id)),graph,costStatus,assemblies,components,assemblyIds,rows,render,renderBOM,renderCosts};
}
root.BomDetails={createModel,esc,vendorName,pendingCostReason,releaseDate};if(typeof module!=='undefined')module.exports=root.BomDetails;
})(typeof window==='undefined'?globalThis:window);

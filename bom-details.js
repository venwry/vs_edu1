/* Shared read-only BOM presentation. Unknowns and saved estimate boundaries are preserved. */
(function(root){
'use strict';
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
 const assemblies=new Map(bom.assemblies.map(r=>[r.id,r])),components=new Map(bom.components.map(r=>[r.id,r]));
 const items=new Map();
 function add(r,cl){const category=categories.category(r,records);if(!category)throw Error('Missing canonical category: '+r.id);items.set(r.id,{id:r.id,name:r.name||r.id,class:cl,category,release:releaseDate(r),record:r});}
 for(const r of catalog.components||[])add(r,'Part');
 for(const r of catalog.devices||[])add(r,r.category==='computer_chassis'?'Chassis':r.virtual?'Internal subsystem':categories.isExpansion(r)?'Expansion':'Peripheral');
 for(const r of catalog.computers||[])add(r,'Computer');
 for(const r of catalog.software_products||[])add(r,'Software product');
 for(const r of catalog.platform_editions||[])add(r,'Software edition');
 for(const r of catalog.external_partner_products||[])add(r,'Software');
 for(const key of ['offered_bundles','proposed_bundles','commercial_offerings'])for(const r of catalog[key]||[])add(r,'Bundle');

 const reviewRows=Object.entries(cost.reviews||{}).flatMap(([key,r])=>[...(r.products||r.prices||[]),...(key==='ncc-1982'?[{id:'software.aion_development_team',name:'AION Development Team',...r.team_launch_price},{id:'software.aion_development_team',name:'AION Development Team',...r.team_1982_price}]:[])].map(row=>({...row,review:key})));
 for(const r of reviewRows)if(!items.has(r.id))throw Error('Missing canonical record for reviewed offering: '+r.id);
 const isMaterial=id=>components.get(id)?.bom_role==='material';
 function assemblyIds(id){const r=records[id];return [...new Set([
 ...(assemblies.has(id)||isMaterial(id)?[id]:[]),...(bom.products||[]).filter(p=>p.catalog_ref===id).flatMap(p=>p.assembly_refs||[]),
 ...(bom.offers||[]).filter(p=>p.catalog_ref===id).map(p=>p.assembly_ref),r?.bom_assembly_ref,...(r?.bom_assembly_refs||[]),...(r?.physical_media_refs||[]),
 ...(r?.manufacturing_variants||[]).map(v=>v.assembly_ref),
 ...cost.products.filter(p=>p.catalog_ref===id||p.id===id).map(p=>p.assembly_ref),
 ...['assembly.'+id,'assembly.media.'+id].filter(x=>assemblies.has(x))
 ].filter(x=>assemblies.has(x)||isMaterial(x)))];}
 function rows(id,seen=new Set(),depth=0){if(seen.has(id))return [];const a=assemblies.get(id);if(!a)return isMaterial(id)?[{ref:id,quantity:1,unit:'each',condition:'always',quantity_status:'defined',depth,name:components.get(id).name}]:[];const next=new Set(seen).add(id);return (a.lines||[]).flatMap(l=>[{...l,depth,name:assemblies.get(l.ref)?.name||components.get(l.ref)?.name||records[l.ref]?.name||l.ref},...(assemblies.has(l.ref)?rows(l.ref,next,depth+1):[])]);}
 function renderBOM(id,opts={}){
  const ids=opts.assemblyRef?(assemblies.has(opts.assemblyRef)||isMaterial(opts.assemblyRef)?[opts.assemblyRef]:[]):assemblyIds(id);
  let html='<section class="bom-detail"><h3>Bill of materials</h3>';
  if(isMaterial(id))html+='<p>This component is a terminal material item. Supplier quotations are not recorded; saved engineering estimates are shown in Manufacturing costs.</p>';
  if(!ids.length)html+='<p>No constituent assembly BOM is recorded for this element.</p><p>Supplier quotations are not recorded; any saved engineering cost assumptions are shown in Manufacturing costs.</p>';
  for(const aid of ids){const a=assemblies.get(aid)||components.get(aid);html+='<details'+(ids.length===1?' open':'')+'><summary>'+esc(a.name||aid)+'</summary><p>'+esc(a.status||'')+' · Quantities below are per parent assembly; nested rows are not additional totals.</p><div class="bom-table-scroll"><table><thead><tr><th>Element</th><th>Quantity</th><th>Unit</th><th>Role / condition</th></tr></thead><tbody>'+rows(aid).map(l=>'<tr><td style="padding-left:'+(.5+l.depth)+'rem">'+esc(l.name)+'</td><td>'+esc(l.quantity??'Unknown')+'</td><td>'+esc(l.unit||'—')+'</td><td>'+esc([l.role,l.condition,l.quantity_status].filter(Boolean).join(' · '))+'</td></tr>').join('')+'</tbody></table></div></details>';}
  if(opts.fullRecords&&typeof root.renderSpecification==='function'){
   const assemblySet=new Set(ids);for(const aid of ids)for(const row of rows(aid))if(assemblies.has(row.ref))assemblySet.add(row.ref);
   const partIds=new Set([...assemblySet].flatMap(aid=>rows(aid).map(l=>l.ref)));
   const source={requirements:(bom.products||[]).filter(p=>p.catalog_ref===id),offers:(bom.offers||[]).filter(p=>p.catalog_ref===id),assemblies:[...assemblySet].filter(aid=>assemblies.has(aid)).map(aid=>assemblies.get(aid)),components:[...components.values()].filter(p=>p.id===id||partIds.has(p.id))};
   html+='<details><summary>Full BOM records and qualification</summary>'+root.renderSpecification(source,records)+'</details>';
  }
  return html+'</section>';
 }
 function renderCosts(id,opts={}){
  let html='<section class="bom-detail">';
  const blocked=pendingCostReason(assemblies,assemblyIds(id));if(blocked)return html+'<p class="cost-reassessment-pending">'+esc(blocked)+'</p><p><a href="generated/models/manufacturing-costs.json">Archived evaluations of the superseded design</a></p></section>';
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
 function bind(host){for(const d of host.querySelectorAll('[data-bom-cost]'))d.addEventListener('toggle',()=>{if(!d.open||d.dataset.loaded)return;d.dataset.loaded='true';const p=cost.products.find(p=>p.id===d.dataset.bomCost);d.insertAdjacentHTML('beforeend',root.renderSpecification(p,records));root.bindSpecificationControls(d);});}
 return {bind,records,items:[...items.values()].sort((a,b)=>a.name.localeCompare(b.name)||a.id.localeCompare(b.id)),assemblies,components,assemblyIds,rows,render,renderBOM,renderCosts};
}
root.BomDetails={createModel,esc,vendorName,pendingCostReason,releaseDate};if(typeof module!=='undefined')module.exports=root.BomDetails;
})(typeof window==='undefined'?globalThis:window);

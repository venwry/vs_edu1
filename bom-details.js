/* Shared read-only BOM presentation. Unknowns and saved estimate boundaries are preserved. */
(function(root){
'use strict';
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const money=v=>Number.isFinite(v)?'$'+v.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}):'Unknown';
function createModel(catalog,bom,cost){
 const records=Object.fromEntries(Object.values(catalog).filter(Array.isArray).flat().filter(r=>r?.id).map(r=>[r.id,r]));
 const assemblies=new Map(bom.assemblies.map(r=>[r.id,r])),components=new Map(bom.components.map(r=>[r.id,r]));
 const items=new Map();
 function add(r,cl,category){items.set(r.id,{id:r.id,name:r.name||r.id,class:cl,category:r.category||category,release:r.introduced?.event_start_date||r.available_from||'',record:r});}
 for(const r of catalog.base_parts||[])add(r,'Part','Component');
 for(const r of catalog.devices||[])add(r,/expansion|video_card|network.*card|compatibility/.test(r.category||'')||/cpm80_module/.test(r.id)?'Expansion':'Peripheral','Peripheral');
 for(const r of catalog.computers||[])add(r,'Computer','Computer');
 for(const key of ['software_products','platform_editions','external_partner_products'])for(const r of catalog[key]||[])add(r,'Software',key==='platform_editions'?'Platform edition':'Software');
 for(const key of ['offered_bundles','proposed_bundles','commercial_offerings'])for(const r of catalog[key]||[])add(r,'Bundle',key==='proposed_bundles'?'Proposed bundle':key==='commercial_offerings'?'Commercial offering':'Catalogue bundle');
 for(const r of bom.components)if(!r.catalog_ref||!items.has(r.catalog_ref))add(r,'Part','Manufacturing component');
 function assemblyIds(id){const r=records[id];return [...new Set([
 ...(assemblies.has(id)?[id]:[]),...(bom.products||[]).filter(p=>p.catalog_ref===id).flatMap(p=>p.assembly_refs||[]),
 ...(bom.offers||[]).filter(p=>p.catalog_ref===id).map(p=>p.assembly_ref),r?.bom_assembly_ref,
 ...(r?.manufacturing_variants||[]).map(v=>v.assembly_ref),
 ...cost.products.filter(p=>p.catalog_ref===id||p.id===id).map(p=>p.assembly_ref),
 ...['assembly.'+id,'assembly.media.'+id].filter(x=>assemblies.has(x))
 ].filter(x=>assemblies.has(x)))];}
 function rows(id,seen=new Set(),depth=0){if(seen.has(id))return [];const a=assemblies.get(id);if(!a)return [];const next=new Set(seen).add(id);return (a.lines||[]).flatMap(l=>[{...l,depth,name:assemblies.get(l.ref)?.name||components.get(l.ref)?.name||records[l.ref]?.name||l.ref},...rows(l.ref,next,depth+1)]);}
 function render(id,opts={}){
  const ids=opts.assemblyRef?(assemblies.has(opts.assemblyRef)?[opts.assemblyRef]:[]):assemblyIds(id);
  let html='<section class="bom-detail"><h3>Bill of materials</h3>';
  if(!ids.length){const parts=components.has(id)?[components.get(id)]:bom.components.filter(p=>p.catalog_ref===id);html+='<p>No constituent assembly BOM is recorded for this element.</p>';if(parts.length)html+='<p>Component unit cost: '+parts.map(p=>Number.isFinite(p.unit_cost)?esc(p.unit_cost+' '+(p.currency||'(currency unspecified)')):'Unknown').join(' / ')+'. Supplier qualification and pricing remain as recorded in the specification.</p>';}
  for(const aid of ids){const a=assemblies.get(aid);html+='<details'+(ids.length===1?' open':'')+'><summary>'+esc(a.name||aid)+'</summary><p>'+esc(a.status||'')+' · Quantities below are per parent assembly; nested rows are not additional totals.</p><div class="bom-table-scroll"><table><thead><tr><th>Element</th><th>Quantity</th><th>Unit</th><th>Role / condition</th></tr></thead><tbody>'+rows(aid).map(l=>'<tr><td style="padding-left:'+(.5+l.depth)+'rem">'+esc(l.name)+'</td><td>'+esc(l.quantity??'Unknown')+'</td><td>'+esc(l.unit||'—')+'</td><td>'+esc([l.role,l.condition,l.quantity_status].filter(Boolean).join(' · '))+'</td></tr>').join('')+'</tbody></table></div></details>';}
  const products=cost.products.filter(p=>p.id===id||p.catalog_ref===id);
  if(products.length){html+='<h3>Recorded costs</h3><p>Nominal USD engineering estimates. Software costs may include media, licensing and delivery. Component and assembly costs overlap; do not add them together.</p>';for(const p of products){html+='<details data-bom-cost="'+esc(p.id)+'" data-cost-id="'+esc(p.id)+'"><summary>'+esc(p.name)+'</summary><div class="bom-table-scroll"><table><thead><tr><th>June 15 evaluation</th><th>Total recurring cost</th><th>Range</th><th>Status</th></tr></thead><tbody>'+Object.entries(p.snapshots||{}).filter(([y,s])=>s.status!=='not_yet_offered'&&(cost.metadata.snapshots||[]).includes(y+'-06-15')).map(([y,s])=>'<tr><td>'+esc(y+'-06-15')+'</td><td>'+money(s.total_usd)+'</td><td>'+money(s.low_usd)+' – '+money(s.high_usd)+'</td><td>'+esc(s.status)+'</td></tr>').join('')+'</tbody></table></div>'+'</details>';}}
  return html+'</section>';
 }
 function bind(host){for(const d of host.querySelectorAll('[data-bom-cost]'))d.addEventListener('toggle',()=>{if(!d.open||d.dataset.loaded)return;d.dataset.loaded='true';const p=cost.products.find(p=>p.id===d.dataset.bomCost);d.insertAdjacentHTML('beforeend',root.renderSpecification({assumptions:p.assumptions,snapshots:p.snapshots},records));root.bindSpecificationControls(d);});}
 return {bind,records,items:[...items.values()].sort((a,b)=>a.name.localeCompare(b.name)||a.id.localeCompare(b.id)),assemblies,components,assemblyIds,rows,render};
}
root.BomDetails={createModel,esc};if(typeof module!=='undefined')module.exports=root.BomDetails;
})(typeof window==='undefined'?globalThis:window);

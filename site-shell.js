/* Shared navigation and domain details. All product facts come from canonical projections. */
'use strict';
const atlasEscape=v=>String(v??'Unknown').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const atlasLabel=v=>v.replace(/_/g,' ');
function atlasValue(value){
 if(value===null)return '<em>Unknown</em>';
 if(Array.isArray(value))return value.length?'<ul>'+value.map(x=>'<li>'+atlasValue(x)+'</li>').join('')+'</ul>':'<span>None recorded</span>';
 if(value&&typeof value==='object')return '<dl>'+Object.entries(value).map(([k,v])=>'<dt>'+atlasEscape(atlasLabel(k))+'</dt><dd>'+atlasValue(v)+'</dd>').join('')+'</dl>';
 return atlasEscape(value);
}
const atlasDetails=(title,value,id='')=>'<details'+(id?' id="'+atlasEscape(id)+'"':'')+'><summary>'+atlasEscape(title)+'</summary>'+atlasValue(value)+'</details>';
window.setupFamilyControls=function(tech,page){
 const models=page.model_refs;if(!models)return;
 const records=Object.fromEntries(Object.values(tech).filter(Array.isArray).flat().filter(x=>x?.id).map(x=>[x.id,x]));
 const selected=page.record_refs[0],host=document.getElementById('models');host.className='family-controls';
 host.innerHTML='<label>Computer model<select id="family-model">'+models.map(id=>'<option value="'+id+'"'+(id===selected?' selected':'')+'>'+atlasEscape(records[id].name)+'</option>').join('')+'</select></label><label>Documented configuration<select id="family-configuration"><option value="">Custom configuration using the controls below</option></select></label>';
 const choice=document.getElementById('family-configuration');
 const offers=(tech.offered_bundles||[]).filter(b=>b.computer_ref===selected||b.hardware?.computer_ref===selected||b.computer===selected);
 // Legacy bundles use computer_ref; only actual full computer offerings qualify.
 for(const b of offers){const option=document.createElement('option');option.value=b.id;option.textContent=b.name+' · '+(b.introduced?.event_start_date||b.available_from||'date unspecified');choice.append(option);}
 document.getElementById('family-model').addEventListener('change',e=>{const url=new URL(location.href);url.searchParams.set('model',e.target.value);url.searchParams.delete('configuration');url.hash=e.target.value;location.assign(url);});
 const note=document.createElement('div');note.className='configuration-summary';note.id='selected-configuration';host.after(note);
 function update(){const b=offers.find(x=>x.id===choice.value);if(!b){note.textContent='Select a documented offering to inspect its monitor, storage, software, launch date and manufacturing variants. RAM and networking can also be explored below.';return;}
  const config=b.computer_configuration,ram=document.getElementById('artemis-ram');if(config&&ram){const match=[...ram.options].find(o=>o.value===config.memory_configuration_ref||o.value===config.memory_configuration_id||o.textContent.startsWith(config.ram_kb+' KB'));if(match){ram.value=match.value;ram.dispatchEvent(new Event('change'));}}
  document.querySelector('[data-layer="bundles"]')?.click();
  const bundle=document.getElementById('bundle-select');if(bundle&&[...bundle.options].some(o=>o.value===b.id)){bundle.value=b.id;bundle.dispatchEvent(new Event('change'));}
  note.innerHTML='<h3>'+atlasEscape(b.name)+'</h3><p>This offering is dated '+atlasEscape(b.introduced?.event_start_date||b.available_from||'as recorded below')+'. Later networking and manufacturing variants retain their own dates.</p>'+'<p>Included devices: '+(b.included_devices||[]).map(id=>atlasEscape(records[id]?.name||id)).join(' · ')+'</p>'+atlasDetails('Included hardware, software and configuration',b);
 }
 choice.addEventListener('change',()=>{const url=new URL(location.href);if(choice.value)url.searchParams.set('configuration',choice.value);else url.searchParams.delete('configuration');history.replaceState(null,'',url);update();});
 const initial=new URLSearchParams(location.search).get('configuration');if(offers.some(b=>b.id===initial))choice.value=initial;update();
};
(async function(){
 const path=location.pathname.split('/').pop()||'index.html';for(const a of document.querySelectorAll('.atlas-header a'))if(a.getAttribute('href')===path)a.setAttribute('aria-current','page');
 const host=document.getElementById('site-details');if(!host)return;
 try{
  const get=async p=>{const r=await fetch(p);if(!r.ok)throw Error('Unable to load '+p);return r.json();};
  const [site,tech,bom,cost]=await Promise.all(['generated/catalogs/site-pages.json','generated/catalogs/logix-aion-technical-catalog-v2.json','generated/catalogs/hardware-bom.json','generated/models/manufacturing-costs.json'].map(get));
  const page=site.pages.find(p=>p.id===host.dataset.page);if(!page)return;
  const records=Object.fromEntries(Object.values(tech).filter(Array.isArray).flat().filter(x=>x?.id).map(x=>[x.id,x]));
  if(['aurelia','artemis'].includes(page.id)){const section=document.createElement('section');section.id='component-specifications';section.innerHTML='<h2>Model and component specifications</h2>'+page.record_refs.filter(id=>records[id]&&!document.getElementById(id)).map(id=>atlasDetails(records[id].name,records[id],id)).join('');host.append(section);}
  const owned=new Map(Object.entries(site.record_page_links||{}));
  // All cost rows have a visible home. Explicit primary ownership wins; family
  // dependencies are additionally visible on their relevant computer pages.
  function owner(row){if(['Bundles','Services'].includes(row.group))return 'pricing';if(owned.has(row.catalog_ref))return owned.get(row.catalog_ref);const id=row.catalog_ref||row.id;
   if(/athena|era2|4164/.test(id))return 'athena';if(/artemis|era1/.test(id))return 'artemis';if(/aurelia|z80|4116/.test(id))return 'aurelia';
   if(row.group==='OEM chips')return 'flexibus';if(row.group==='Peripherals')return /network/.test(id)?'networking':'peripherals';if(/abacus|business_tools/.test(id))return 'business-software';if(/bpi/.test(id))return 'bpi';if(/aionix|cpm/.test(id))return 'operating-systems';return 'software-development';
  }
  const rows=cost.products.filter(r=>owner(r)===page.id||(!['Bundles','Services'].includes(r.group)&&page.record_refs.includes(r.catalog_ref)));
  if(rows.length){const section=document.createElement('section');section.id='product-costs';section.innerHTML='<h2>'+(page.id==='pricing'?'Bundle and service delivery costs':'Components, BOMs and manufacturing')+'</h2><p>Nominal USD estimates at the recorded assessment dates. Unknown quantities and qualification gaps remain explicit. Component rows and complete assemblies overlap; do not add both as independent costs. Software rows include duplication, licensing and delivery where applicable.</p>';
   const components=new Map(bom.components.map(x=>[x.id,x])),assemblies=new Map(bom.assemblies.map(x=>[x.id,x]));
   for(const row of rows){
    const d=document.createElement('details');d.id='cost-'+row.id;d.dataset.costId=row.id;d.innerHTML='<summary>'+atlasEscape(row.name)+' · '+atlasEscape(row.group)+'</summary>';
    d.addEventListener('toggle',()=>{if(!d.open||d.dataset.loaded)return;d.dataset.loaded='true';const refs=bom.products.filter(p=>p.catalog_ref===row.catalog_ref),assemblySet=new Map(),partSet=new Map();function visit(id){if(assemblies.has(id)&&!assemblySet.has(id)){const a=assemblies.get(id);assemblySet.set(id,a);for(const l of a.lines||[])visit(l.ref);}else if(components.has(id))partSet.set(id,components.get(id));}for(const p of refs)for(const id of p.assembly_refs||[])visit(id);
    d.insertAdjacentHTML('beforeend',(records[row.catalog_ref]?atlasDetails('Technical specification',records[row.catalog_ref]):'')+atlasDetails('Dated cost assessments and breakdowns',row)+atlasDetails('BOM requirements and assemblies',{products:refs,assemblies:[...assemblySet.values()],components:[...partSet.values()]}));});section.append(d);
   }host.append(section);
  }
  if(['artemis','video-system','flexibus','software-development','operating-systems','ecosystem','pricing'].includes(page.id)){
   const [june,november]=await Promise.all(['generated/models/ncc-1982-review.json','generated/models/comdex-1982-cost-review.json'].map(get));
   const dated=[...june.products,...november.prices].filter(r=>page.id==='pricing'||page.record_refs.includes(r.id));
   if(dated.length)host.insertAdjacentHTML('beforeend','<section id="dated-reviews"><h2>1982 dated product cost and price reviews</h2>'+dated.map(r=>atlasDetails(r.name+' · '+r.date,r)).join('')+'</section>');
  }
  const uncosted=bom.products.filter(p=>page.record_refs.includes(p.catalog_ref)&&!rows.some(r=>r.catalog_ref===p.catalog_ref));if(uncosted.length)host.insertAdjacentHTML('beforeend','<section><h2>BOM requirements without a costed product row</h2><p>No complete manufacturing estimate is implied by these records.</p>'+uncosted.map(p=>atlasDetails(records[p.catalog_ref]?.name||p.catalog_ref,{requirements:p,assemblies:bom.assemblies.filter(a=>p.assembly_refs.includes(a.id))})).join('')+'</section>');
  if(page.id==='industrial-investment'){
   const global=Object.fromEntries(Object.entries(cost).filter(([k])=>k!=='products'));
   host.insertAdjacentHTML('beforeend','<section id="manufacturing-method"><h2>Manufacturing methods, supplier programmes and assumptions</h2><p>Product costs are attached to computer, software and standards pages. Bundle and service delivery costs appear under Retail pricing.</p>'+Object.keys(global).map(k=>'<details data-method="'+atlasEscape(k)+'"><summary>'+atlasEscape(atlasLabel(k))+'</summary></details>').join('')+'</section>');
  }
  host.querySelectorAll('[data-method]').forEach(d=>d.addEventListener('toggle',()=>{if(d.open&&!d.dataset.loaded){d.dataset.loaded='true';d.insertAdjacentHTML('beforeend',atlasValue(cost[d.dataset.method]));}}));
  if(page.id==='ecosystem'){
   const policy=await get('generated/catalogs/ecosystem-forecast-policy.json');
   host.insertAdjacentHTML('afterbegin','<section id="product-catalogue"><h2>Third-party product catalogue</h2><p>These products are established in the alternative-history specification. Historical product existence does not establish a Logix contract or a native port.</p>'+page.record_refs.filter(id=>records[id]).map(id=>atlasDetails(records[id].name,records[id],id)).join('')+'<h3>Qualification, candidate products and growth assumptions</h3><p>Named examples illustrate a broader supplier and application base; they are not a ceiling. CP/M compatibility, native C ports, qualified devices and actual paid licences are distinct measures. Native ports require source rights, engineering and testing; binary compatibility is never assumed across CPU families.</p>'+atlasDetails('Model policy and plausible manufacturers',policy)+'</section>');
  }
  // Make every old cost deep-link usable without restoring a separate cost page.
  const id=decodeURIComponent(location.hash.slice(1));const target=document.getElementById(id);if(target){for(let p=target;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;}
 }catch(error){host.insertAdjacentHTML('beforeend','<p role="alert">Supplementary specifications could not load: '+atlasEscape(error.message)+'. Reload this page to retry.</p>');}
})();

(async function(){
'use strict';
const $=id=>document.getElementById(id),esc=BomDetails.esc;
try{
 const pageId=document.documentElement.dataset.page,bomMode=pageId==='bom-navigator';
 const get=async p=>{const r=await fetch(p);if(!r.ok)throw Error('Unable to load '+p);return r.json();};
 const [catalog,story]=await Promise.all(['generated/catalogs/logix-aion-technical-catalog-v2.json','generated/catalogs/logix-aion-story.json'].map(get));
 let model;
 if(bomMode){const [bom,cost]=await Promise.all(['generated/catalogs/hardware-bom.json','generated/models/manufacturing-costs.json'].map(get));model=BomDetails.createModel(catalog,bom,cost);}
 else{
  const site=await get('generated/catalogs/site-pages.json'),page=site.pages.find(p=>p.id===pageId);
  if(!page)throw Error('Missing navigator configuration');
  const records=Object.fromEntries(Object.values(catalog).filter(Array.isArray).flat().filter(r=>r?.id).map(r=>[r.id,r]));
  const items=page.record_refs.map(id=>{const r=records[id];if(!r)throw Error('Missing catalogue record '+id);return {id,name:r.name||id,record:r,class:id.startsWith('technology.')?'Technology':id.startsWith('service.')?(/training|course/.test(r.category||'')||/training|academy_(before|regular|customer)/.test(id)?'Training':'Service'):'External platform',category:r.category||'Uncategorized',release:r.introduced?.event_start_date||r.available_from||''};}).sort((a,b)=>a.name.localeCompare(b.name)||a.id.localeCompare(b.id));
  model={items,records,bind:()=>{}};
 }
 let selected=new URLSearchParams(location.search).get('element')||decodeURIComponent(location.hash.slice(1));
 for(const [id,key] of [['bom-class','class'],['bom-category','category'],['bom-release','release']])for(const value of [...new Set(model.items.map(x=>x[key]||'Unknown'))].sort()){const o=document.createElement('option');o.value=value;o.textContent=value.replace(/_/g,' ');$(id).append(o);}
 let activeTab='details';
 const tabs=bomMode?[['details','Details'],['bom','Bill of Materials'],['costs','Manufacturing costs'],['events','Related events']]:[['details','Details'],['events','Related events']];
 function relatedEvents(id){
  const events=story.phases.flatMap(p=>p.events).filter(e=>(e.product_refs||[]).includes(id));
  return events.length?events.map(e=>'<article><h3><a href="timeline.html#'+esc(e.id)+'">'+esc(e.title)+'</a></h3><p>'+esc(e.date?.start||'Unknown date')+'</p>'+renderSpecification({actions:e.actions,outcomes:e.outcomes,agreement_terms:e.agreement_terms,metrics:e.metrics},model.records)+'</article>').join(''):'<p>No directly related events are recorded for this element.</p>';
 }
 function inspect(item){
  selected=item.id;const url=new URL(location.href);url.searchParams.set('element',selected);url.hash='';history.replaceState(null,'',url);
  const host=$('bom-inspector');host.innerHTML='<h2>'+esc(item.name)+'</h2><p>'+esc(item.class)+' · '+esc(item.category.replace(/_/g,' '))+'</p><div class="bom-tabs" role="tablist" aria-label="Element information">'+tabs.map(([id,label])=>'<button type="button" role="tab" id="tab-'+id+'" aria-controls="panel-'+id+'">'+label+'</button>').join('')+'</div>'+tabs.map(([id])=>'<section role="tabpanel" id="panel-'+id+'" aria-labelledby="tab-'+id+'" tabindex="0" hidden></section>').join('');
  function activate(id,focus=false){activeTab=id;for(const [key] of tabs){const tab=$('tab-'+key),panel=$('panel-'+key),on=key===id;tab.setAttribute('aria-selected',String(on));tab.tabIndex=on?0:-1;panel.hidden=!on;if(on&&!panel.dataset.loaded){panel.innerHTML=key==='details'?renderSpecification(item.record,model.records):key==='bom'?model.renderBOM(item.id,{fullRecords:true}):key==='costs'?model.renderCosts(item.id,{fullRecords:true}):relatedEvents(item.id);panel.dataset.loaded='true';bindSpecificationControls(panel);model.bind(panel);}if(on&&focus)tab.focus();}}
  for(const [id] of tabs){$('tab-'+id).onclick=()=>activate(id);$('tab-'+id).onkeydown=e=>{const i=tabs.findIndex(t=>t[0]===id);const next=e.key==='ArrowRight'?(i+1)%tabs.length:e.key==='ArrowLeft'?(i+tabs.length-1)%tabs.length:e.key==='Home'?0:e.key==='End'?tabs.length-1:null;if(next!==null){e.preventDefault();activate(tabs[next][0],true);}};}
  activate(activeTab);for(const b of document.querySelectorAll('[data-element]'))b.setAttribute('aria-pressed',String(b.dataset.element===selected));
 }
 function render(){const list=model.items.filter(x=>[['bom-class','class'],['bom-category','category'],['bom-release','release']].every(([id,key])=>!$(id).value||$(id).value===(x[key]||'Unknown')));$('bom-count').textContent=list.length+' elements';$('bom-rows').innerHTML=list.map(x=>'<tr data-catalog-id="'+esc(x.id)+'"><td><button type="button" data-element="'+esc(x.id)+'" aria-controls="bom-inspector" aria-pressed="false">'+esc(x.name)+'</button></td><td>'+esc(x.class)+'</td><td>'+esc(x.category.replace(/_/g,' '))+'</td><td>'+esc(x.release||'Unknown')+'</td></tr>').join('');for(const b of document.querySelectorAll('[data-element]'))b.onclick=()=>inspect(list.find(x=>x.id===b.dataset.element));if(list.length)inspect(list.find(x=>x.id===selected)||list[0]);else $('bom-inspector').innerHTML='<p>No elements match these filters.</p>';}
 for(const id of ['bom-class','bom-category','bom-release'])$(id).onchange=render;
 $('bom-reset').onclick=()=>{for(const id of ['bom-class','bom-category','bom-release'])$(id).value='';render();};render();document.querySelector('main').dataset.ready='true';
}catch(e){$('bom-count').textContent='';$('bom-inspector').innerHTML='<p role="alert">'+esc(e.message)+'. Reload to retry.</p>';}
})();

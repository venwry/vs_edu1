(async function(){
'use strict';
const $=id=>document.getElementById(id),esc=BomDetails.esc;
try{
 const [catalog,bom,cost]=await Promise.all(['generated/catalogs/logix-aion-technical-catalog-v2.json','generated/catalogs/hardware-bom.json','generated/models/manufacturing-costs.json'].map(async p=>{const r=await fetch(p);if(!r.ok)throw Error('Unable to load '+p);return r.json();}));
 const model=BomDetails.createModel(catalog,bom,cost);let selected=new URLSearchParams(location.search).get('element');
 for(const [id,key] of [['bom-class','class'],['bom-category','category'],['bom-release','release']])for(const value of [...new Set(model.items.map(x=>x[key]||'Unknown'))].sort()){const o=document.createElement('option');o.value=value;o.textContent=value.replace(/_/g,' ');$(id).append(o);}
 function inspect(item){selected=item.id;const url=new URL(location.href);url.searchParams.set('element',selected);history.replaceState(null,'',url);$('bom-inspector').innerHTML='<h2>'+esc(item.name)+'</h2><p>'+esc(item.class)+' · '+esc(item.category.replace(/_/g,' '))+'</p>'+renderSpecification(item.record,model.records)+model.render(item.id);bindSpecificationControls($('bom-inspector'));model.bind($('bom-inspector'));for(const b of document.querySelectorAll('[data-element]'))b.setAttribute('aria-pressed',String(b.dataset.element===selected));}
 function render(){const list=model.items.filter(x=>[['bom-class','class'],['bom-category','category'],['bom-release','release']].every(([id,key])=>!$(id).value||$(id).value===(x[key]||'Unknown')));$('bom-count').textContent=list.length+' elements';$('bom-rows').innerHTML=list.map(x=>'<tr data-catalog-id="'+esc(x.id)+'"><td><button type="button" data-element="'+esc(x.id)+'" aria-controls="bom-inspector" aria-pressed="false">'+esc(x.name)+'</button></td><td>'+esc(x.class)+'</td><td>'+esc(x.category.replace(/_/g,' '))+'</td><td>'+esc(x.release||'Unknown')+'</td></tr>').join('');for(const b of document.querySelectorAll('[data-element]'))b.onclick=()=>inspect(list.find(x=>x.id===b.dataset.element));if(list.length)inspect(list.find(x=>x.id===selected)||list[0]);else $('bom-inspector').innerHTML='<p>No elements match these filters.</p>';}
 for(const id of ['bom-class','bom-category','bom-release'])$(id).onchange=render;
 $('bom-reset').onclick=()=>{for(const id of ['bom-class','bom-category','bom-release'])$(id).value='';render();};render();document.querySelector('main').dataset.ready='true';
}catch(e){$('bom-count').textContent='';$('bom-inspector').innerHTML='<p role="alert">'+esc(e.message)+'. Reload to retry.</p>';}
})();

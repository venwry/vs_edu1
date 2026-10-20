/* Artemis-family views use the same diagram shell as Aurelia, with catalog-owned layouts. */
window.startArtemisExplorer=function(catalog,page,siteLink){
'use strict';
const $=id=>document.getElementById(id),esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const records=Object.fromEntries(Object.values(catalog).filter(Array.isArray).flat().filter(x=>x?.id).map(x=>[x.id,x]));
const settings=catalog.artemis_explorer,c=records[page.record_refs[0]],rec=id=>records[id],human=k=>k.replace(/_/g,' '),at=(obj,path)=>path.split('.').reduce((v,k)=>v?.[k],obj);
if(!settings||!c?.memory?.configurations?.length)throw Error('The catalog is missing the Artemis architecture definitions.');
const value=v=>Array.isArray(v)?v.map(value).join('; '):v&&typeof v==='object'?Object.entries(v).map(([k,x])=>human(k)+': '+value(x)).join(' · '):typeof v==='boolean'?(v?'Yes':'No'):records[v]?.name||String(v??'—');
const fields=v=>Object.entries(v||{}).map(([k,x])=>`<div><dt>${esc(human(k))}</dt><dd>${esc(value(x))}</dd></div>`).join('');
const dl=v=>'<dl class="fields">'+fields(v)+'</dl>';
const table=(heads,rows)=>'<div class="table-wrap"><table><thead><tr>'+heads.map(h=>'<th scope="col">'+esc(h)+'</th>').join('')+'</tr></thead><tbody>'+rows.map(r=>'<tr>'+r.map(x=>'<td>'+esc(value(x))+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>';
const configurations=c.memory.configurations,maxKB=c.memory.physical_capacity_limit_kb;
let layer='hardware',selected='',nodes=[],edges=[];
const network=()=>Boolean(c.networking?.included_by_default)||$('era').value==='1981';
const ramConfiguration=()=>configurations.find(x=>x.id===$('artemis-ram').value)||configurations.find(x=>x.id===c.memory.default_configuration);
const module=()=>rec(ramConfiguration().module_ref);
const ram=()=>ramConfiguration().ram_kb;
const ramFacts=()=>({...ramConfiguration(),module_name:module().name,module_capacity_kb:module().specification.capacity_kb,module_data_width_bits:16,bank_data_width_bits:32,empty_sockets:c.memory.ram_sockets-ramConfiguration().populated_modules,physical_capacity_limit_kb:maxKB,capacity_limit_status:c.memory.capacity_limit_status,population_policy:c.memory.population_policy,upgrade_policy:c.memory.upgrade_policy,reliability_policy:c.memory.reliability_policy});
const clean=r=>Object.fromEntries(Object.entries(r||{}).filter(([k])=>!['id','used_by','used_in','compatible_with'].includes(k)));
function add(id,title,sub,col,row,data,optional=false){nodes.push({id,title,sub,col,row,data,optional});}
function product(id,col,row,optional=false,sub){const r=rec(id);if(!r)throw Error('Missing catalog record: '+id);add(id,r.name,sub||r.introduced?.event_start_date||human(r.category),col,row,clean(r),optional);}
function definition(n){if(n.id==='network'&&!network())return;
 if(n.requires_compatible_device&&!c.compatible_devices.includes(n.record_ref))return;
 let r=n.record_ref?rec(n.id==='os'&&network()?settings.network_software_ref:n.record_ref):null,data=r?clean(r):{},source=r?.specification||r;
 if(n.fields)data=Object.fromEntries(n.fields.map(k=>[k,source[k]]));
 if(n.computer_path)data={...data,...at(c,n.computer_path)};
 if(r?.specification_ref)data[rec(r.specification_ref).name]=rec(r.specification_ref).specification;
 if(n.id==='ram')data=ramFacts();
 if(n.id==='apps')data={compatible_software:c.compatible_software,software_compatibility:c.software_compatibility};
 let sub=r?.name||human(n.computer_path?.split('.').pop()||n.id);
 if(n.id==='cpu')sub=c.processor.variant+' · '+c.processor.clock_mhz+' MHz';
 if(n.id==='ram')sub=ram()+' KB · '+ramConfiguration().populated_modules+' modules · '+ramConfiguration().populated_banks+' banks';
 if(n.id==='graphics'||n.id==='video_ram')sub=c.video.video_ram_kb+' KB video RAM · '+c.video.text_mode.characters;
 if(n.id==='virtual')sub=rec(settings.memory_ref).specification.virtual_address_bits+'-bit virtual addresses';
 if(n.id==='physical')sub=rec(settings.memory_ref).specification.physical_address_bits+'-bit physical addresses';
 if(n.id==='rom')sub=c.io_and_expansion.rom_eeprom_cartridge_slots.count+' cartridge slots';
 if(n.id==='disk')sub=c.storage.internal_fdd.count+' floppy drives'+(c.storage.internal_hdd?' + '+c.storage.internal_hdd.capacity_mb+' MB HDD':'');
 add(n.id,n.title,sub,n.column,n.row,data,Boolean(n.optional));
}
function configuredDiagram(name){const view=settings.diagrams[name];view.nodes.forEach(definition);edges=view.edges.filter(e=>e.every(id=>nodes.some(n=>n.id===id)));}
function peripherals(){
 add('host',c.name,'Host computer',2,1,{form_factor:c.form_factor,io_and_expansion:c.io_and_expansion});
 product('technology.flexibus',1,2,false,c.io_and_expansion.flexibus_ports+' ports');
 product(c.video.technology_ref,2,2);product('technology.plug_and_execute',3,2,false,c.io_and_expansion.expansion_slots.count+' × '+c.io_and_expansion.expansion_slots.width_bits+'-bit slots');
 edges=[['host','technology.flexibus'],['host',c.video.technology_ref],['host','technology.plug_and_execute']];
 const bundled=new Set(catalog.offered_bundles.filter(b=>b.computer_ref===c.id).flatMap(b=>b.included_devices||[]));
 c.compatible_devices.filter(id=>network()||![settings.network_adapter_ref,'device.network_hub'].includes(id)).forEach((id,i)=>{
  const d=rec(id),standard=id===settings.network_adapter_ref&&network(),bundle=bundled.has(id),optional=!standard&&!bundle;
  product(id,i%3+1,Math.floor(i/3)+3,optional,(standard?'Included in selected configuration':bundle?'Bundle option':'Optional')+' · '+d.introduced.event_start_date);
  const parent=d.category==='memory_expansion'?'host':id==='device.network_hub'?settings.network_adapter_ref:d.category==='display'?c.video.technology_ref:['device.artemis_cpm80_module',settings.network_adapter_ref].includes(id)?'technology.plug_and_execute':'technology.flexibus';
  edges.push([parent,id,optional]);
 });
}
function software(){const mode=$('software-mode').value;
 if(mode==='internals'){
  configuredDiagram('software');
  if(c.compatible_devices.includes(settings.compatibility_ref)){product(settings.compatibility_ref,3,4,true);edges.push(['files',settings.compatibility_ref,true]);}
 }else if(mode==='cartridge'){
  const tools=rec(settings.business_tools_ref);product(tools.id,2,1);
  tools.features.forEach((feature,i)=>{const id='tool-'+i;add(id,feature,'Office Suite component',i%3+1,Math.floor(i/3)+2,{suite:tools.name,feature,delivery:tools.delivery,portability_contract:tools.portability_contract});edges.push([tools.id,id]);});
  product('technology.logix_tui_standard',1,5);product('technology.logix_display_api',3,5);edges.push([tools.id,'technology.logix_tui_standard'],[tools.id,'technology.logix_display_api']);
 }else if(mode==='portability'){
  const ids=['api','tui','display','framework','language','artemis_tools','aurelia_tools'].map(k=>settings.portability_refs[k]);
  ids.forEach((id,i)=>product(id,i%3+1,Math.floor(i/3)+1));edges=ids.slice(1).map(id=>[ids[0],id]);
 }else{
  c.compatible_software.map(rec).forEach((r,i)=>product(r.id,i%3+1,Math.floor(i/3)+1,false,(r.sold_separately?'Sold separately':'Compatible software')+' · '+r.introduced.event_start_date));
 }
}
const offers=[...(catalog.offered_bundles||[]),...(catalog.proposed_bundles||[])].filter(b=>b.computer_ref===c.id);
function bundleItems(b,seen=new Set()){
 if(seen.has(b.id))throw Error('Circular base bundle: '+b.id);seen.add(b.id);
 let items=b.base_bundle_ref?bundleItems(rec(b.base_bundle_ref),seen):[];
 if(b.computer_configuration)items.push({id:b.computer_ref,configuration:b.computer_configuration});
 for(const id of [...(b.included_devices||[]),...(b.included_software||[])])items.push({id});
 for(const item of b.included_services||[])items.push({id:item.service_ref,duration_years:item.duration_years});
 return items;
}
function bundles(){const b=rec($('bundle-select').value);if(!b)return;
 add('bundle',b.name,b.availability||(b.status==='proposed'?'Proposed offer':'Catalog offer'),2,1,{...clean(b),explorer_note:settings.bundle_note});
 bundleItems(b).forEach((item,i)=>{const r=rec(item.id),id='bundle-item-'+i,col=i%3+1,row=Math.floor(i/3)+2;
  if(item.configuration)add(id,r.name,item.configuration.ram_kb+' KB RAM'+(item.configuration.hdd_mb?' · '+item.configuration.hdd_mb+' MB HDD':''),col,row,{configuration:item.configuration,processor:r.processor,storage:r.storage});
  else add(id,r.name,item.duration_years?item.duration_years+' year(s)':'Included',col,row,{...clean(r),...(item.duration_years?{duration_years:item.duration_years}:{})});
  edges.push(['bundle',id]);
 });
}
function select(){const n=nodes.find(n=>n.id===selected);if(!n)return;
 $('diagram').querySelectorAll('[data-node]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.node===selected)));
 $('inspector').innerHTML='<div class="eyebrow">'+esc(layer)+'</div><h2>'+esc(n.title)+'</h2><p>'+esc(n.sub)+'</p>'+window.renderSpecification(n.data,records);window.bindSpecificationControls($('inspector'));
}
function draw(){window.drawArchitectureWires($('diagram'),edges);}
function details(){
 $('memory-section').innerHTML='<div class="eyebrow">Memory organization</div><h2>'+esc(c.name)+' · '+ram()+' KB RAM</h2><p>'+esc(settings.memory_note)+'</p>'+table(['Resource','Configuration'],[['Virtual addressing',rec(settings.memory_ref).specification.virtual_address_bits+' bits'],['Physical addressing',rec(settings.memory_ref).specification.physical_address_bits+' bits'],['RAM population',ramConfiguration().populated_modules+' × '+module().specification.capacity_kb+' KB / 16-bit modules'],['Populated banks',ramConfiguration().populated_banks+' / '+c.memory.bank_count],['Data DRAM chips',ramConfiguration().data_chip_count],['Qualification',ramConfiguration().validation_status],['Available sockets',c.memory.ram_sockets],['Physical capacity design target',maxKB+' KB · qualification pending'],['Video RAM',c.video.video_ram_kb+' KB'],['Cartridge slots',c.io_and_expansion.rom_eeprom_cartridge_slots]])+'<p>'+esc(settings.ram_note)+'</p><details><summary>RAM modules and process memory</summary>'+dl(clean(module()))+dl(rec(settings.os_model_ref).specification)+'</details>';
 $('software-section').innerHTML='<div class="eyebrow">System organization</div><h2>'+esc(rec(network()?settings.network_software_ref:settings.os_ref).name)+'</h2>'+dl(clean(rec(network()?settings.network_software_ref:settings.os_ref)));
 $('portability-section').innerHTML='<div class="eyebrow">Platform records</div>'+page.record_refs.filter(id=>id!==c.id).map(id=>`<details id="${esc(id)}"><summary>${esc(rec(id).name)}</summary>${dl(clean(rec(id)))}</details>`).join('')+'<details><summary>'+esc(c.name)+' · full specification</summary>'+dl(clean(c))+'</details>';
}
function build(){nodes=[];edges=[];
 $('ram-choice').hidden=true;$('artemis-ram-choice').hidden=layer==='bundles';$('era').parentElement.hidden=Boolean(c.networking?.included_by_default)||layer==='bundles';
 $('offering-controls').hidden=!['software','bundles'].includes(layer);$('software-choice').hidden=layer!=='software';$('bundle-choice').hidden=layer!=='bundles';
 $('stats').innerHTML=[['Processor',c.processor.variant+' · '+c.processor.clock_mhz+' MHz'],['System RAM',ram()+' KB'],['Video RAM',c.video.video_ram_kb+' KB'],['Text display',c.video.text_mode.characters]].map(([k,v])=>'<div class="stat"><span>'+esc(k)+'</span><strong>'+esc(v)+'</strong></div>').join('');
 $('view-title').textContent=c.name.toUpperCase()+' / '+layer.toUpperCase();$('diagram-note').textContent=settings.notes[layer];
 if(layer==='hardware'||layer==='memory')configuredDiagram(layer);else if(layer==='peripherals')peripherals();else if(layer==='software')software();else bundles();
 if(!nodes.some(n=>n.id===selected))selected=nodes[0]?.id;
 $('diagram').innerHTML='<svg class="wires" aria-hidden="true"></svg>'+nodes.map(n=>`<button class="node ${n.optional?'optional':''}" style="grid-column:${n.col};grid-row:${n.row}" data-node="${esc(n.id)}" aria-pressed="false" aria-controls="inspector"><small>${esc(layer)}</small><strong>${esc(n.title)}</strong><span>${esc(n.sub)}</span><span class="plus" aria-hidden="true">+</span></button>`).join('');
 $('diagram').querySelectorAll('[data-node]').forEach(b=>b.addEventListener('click',()=>{selected=b.dataset.node;select();}));select();details();requestAnimationFrame(draw);
}
$('diagram').closest('main').classList.add('artemis-explorer');
$('models').innerHTML=settings.page_ids.map(id=>siteLink(id)).join(' · ');$('page-heading').textContent=page.title;$('intro').textContent=page.description;
$('launch').textContent=c.introduced.event_start_date;$('event').textContent=c.introduced.event_name;
$('load-panel').hidden=true;$('ram-choice').hidden=true;
const control=document.createElement('label');control.id='artemis-ram-choice';control.className='era';control.innerHTML='RAM <select id="artemis-ram">'+configurations.map(cfg=>`<option value="${esc(cfg.id)}"${cfg.id===c.memory.default_configuration?' selected':''}>${cfg.ram_kb} KB · ${cfg.populated_modules} × ${rec(cfg.module_ref).specification.capacity_kb} KB · ${cfg.populated_banks} banks${cfg.shipping_configuration?' · shipping':' · expansion target'}</option>`).join('')+'</select>';$('ram-choice').after(control);
$('era').disabled=false;$('era').value=c.networking?'1981':'launch';$('era').options[0].textContent='Launch configuration';$('era').options[1].textContent=rec(settings.network_software_ref).introduced.event_start_date+' · networking';
$('software-mode').innerHTML=settings.software_views.map(v=>'<option value="'+esc(v.id)+'">'+esc(v.label)+'</option>').join('');
$('bundle-select').innerHTML=offers.map(b=>'<option value="'+esc(b.id)+'">'+esc(b.name)+'</option>').join('');
$('context').textContent=settings.context;$('timeline').innerHTML=settings.computer_refs.map(rec).map(x=>'<time>'+esc(x.introduced.event_start_date)+'</time><p>'+esc(x.name)+' · '+esc(x.introduced.event_name)+'</p>').join('');
const cs=settings.computer_refs.map(rec);$('comparison').closest('article').querySelector('h2').textContent='Artemis family comparison';
$('comparison').innerHTML=table(['Component',...cs.map(x=>x.name)],[['Processor',...cs.map(x=>x.processor.variant+' · '+x.processor.clock_mhz+' MHz')],['Shipping RAM',...cs.map(x=>x.memory.configurations.filter(r=>r.shipping_configuration).map(r=>r.ram_kb).join(' / ')+' KB')],['RAM module',...cs.map(x=>x.memory.module_refs.map(id=>rec(id).specification.capacity_kb+' KB / 16-bit').join(' or '))],['Internal hard disk',...cs.map(x=>x.storage.internal_hdd?x.storage.internal_hdd.capacity_mb+' MB':'Not included')],['Video RAM',...cs.map(x=>x.video.video_ram_kb+' KB')],['Networking',...cs.map(x=>x.networking?'Included at launch':'Standard from '+rec(settings.network_software_ref).introduced.event_start_date)]]);
for(const button of document.querySelectorAll('[data-layer]')){button.disabled=false;button.addEventListener('click',()=>{layer=button.dataset.layer;document.querySelectorAll('[data-layer]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));selected='';build();});}
for(const id of ['artemis-ram','era','software-mode','bundle-select'])$(id).addEventListener('change',build);
if(typeof ResizeObserver!=='undefined')new ResizeObserver(draw).observe($('diagram'));window.addEventListener('resize',draw);build();
};

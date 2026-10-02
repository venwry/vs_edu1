window.startArchitectureExplorer=function(initialCatalog,pageConfig,siteLink){

'use strict';
const $=id=>document.getElementById(id),esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let catalog,records,computers,settings,model=0,layer='hardware',selected='',nodes=[],edges=[];
const rec=id=>records[id];
const label=k=>k.replace(/_/g,' ').replace(/\b(kb|mhz|ram|rom|cpu|vram|bios|cpm|tui|rgb|id|api)\b/gi,x=>x.toUpperCase());
function value(v){if(Array.isArray(v))return v.map(value).join('; ');if(v&&typeof v==='object')return Object.entries(v).map(([k,x])=>label(k)+': '+value(x)).join(' · ');if(typeof v==='boolean')return v?'Yes':'No';return records?.[v]?.name||String(v??'—');}
const facts=obj=>Object.entries(obj||{}).map(([k,v])=>[label(k),value(v)]);
const list=items=>'<ul>'+items.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>';
function table(headers,rows){return '<table><thead><tr>'+headers.map(x=>'<th scope="col">'+esc(x)+'</th>').join('')+'</tr></thead><tbody>'+rows.map(row=>'<tr>'+row.map(x=>'<td>'+esc(x)+'</td>').join('')+'</tr>').join('')+'</tbody></table>';}
function add(id,title,sub,col,row,category,description,pairs=[],extra=[],optional=false){nodes.push({id,title,sub,col,row,category,description,facts:pairs,extra,optional});}
function product(id,col,row,optional=false){const r=rec(id);const data=r.specification||r.components||{};add(id,r.name,r.introduced?.event_start_date||label(r.category),col,row,label(r.category),r.description||value(data),[...facts(data),...facts(Object.fromEntries(['vendor','version','connection','capacity_kb','delivery','features','contents','modules','positioning','toolchain','portable_runtime','portability_contract','adds','introduced'].filter(k=>r[k]!==undefined).map(k=>[k,r[k]])))],r.features_ref?[value(rec(r.features_ref)?.specification||rec(r.features_ref))]:[],optional);}
function install(data){
 if(!data?.aurelia_explorer||!Array.isArray(data.computers)||!Array.isArray(data.software_products))throw Error('This file is not a compatible Logix catalog.');
 const map=Object.fromEntries(Object.values(data).filter(Array.isArray).flat().filter(x=>x&&x.id).map(x=>[x.id,x]));
 const config=data.aurelia_explorer,cs=config.computer_refs.map(id=>map[id]);
 if(cs.some(x=>!x?.memory?.organization||!x.processor)||!map[config.os_ref]?.internal_organization||!map[config.memory_ref]?.regions)throw Error('The catalog is missing the Aurelia architecture definitions.');
 catalog=data;records=map;settings=config;computers=cs.filter(x=>x.id===pageConfig.record_refs[0]);model=0;
 $('models').innerHTML=siteLink('aurelia')+' · '+siteLink('aurelia-plus');$('page-heading').textContent=pageConfig.title;
 document.querySelectorAll('[data-layer],#era').forEach(x=>x.disabled=false);
 $('intro').textContent=pageConfig.description;$('context').textContent=settings.context;
 $('timeline').innerHTML=settings.timeline.map(x=>`<time>${esc(x.date)}</time><p><b>${esc(x.title)}</b> · ${esc(x.description)}</p>`).join('');
 const comparison=[['Processor',...cs.map(c=>rec(c.processor.part_ref).name+' · '+c.processor.clock_mhz+' MHz')],['System RAM',...cs.map(c=>c.memory.ram_kb+' KB')],['Video RAM',...cs.map(c=>c.memory.video_ram_kb+' KB')],['Text display',...cs.map(c=>c.video.text_mode.characters)],['Internal floppy',...cs.map(c=>value(c.storage.internal_fdd))],['FlexiBUS ports',...cs.map(c=>c.io_and_expansion.flexibus_ports)],['Expansion slots',...cs.map(c=>c.io_and_expansion.expansion_slots.count+' × '+c.io_and_expansion.expansion_slots.width_bits+'-bit')],['Cartridge slots',...cs.map(c=>c.rom_and_cartridges.xip_slots)],['OS foundation',...cs.map(c=>rec(c.rom_and_cartridges.system_cartridge_ref).base_version)]];
 $('comparison').innerHTML=table(['Component',...cs.map(c=>c.name)],comparison);
 build();$('load-panel').hidden=true;
}
function activeComputer(){
 const base=computers[model];
 if(!base.memory.expansion_ref||!$('ram-card').checked)return base;
 const expanded=base.memory.expanded_organization;
 return {...base,memory:{...base.memory,ram_kb:expanded.ram_kb,organization:expanded}};
}
function build(){
 if(!catalog)return;nodes=[];edges=[];const c=activeComputer(),m=c.memory,io=c.io_and_expansion,os=rec(settings.os_ref),mm=rec(settings.memory_ref),net=$('era').value==='1981';
 document.querySelectorAll('[data-model]').forEach(b=>b.setAttribute('aria-pressed',Number(b.dataset.model)===model));
 $('ram-choice').hidden=!c.memory.expansion_ref||layer==='bundles';$('ram-card-label').textContent=c.memory.expansion_ref?'Install '+rec(c.memory.expansion_ref).name:'';$('era').parentElement.hidden=layer==='bundles';
 $('launch').textContent=c.introduced.event_start_date;$('event').textContent=c.introduced.event_name;
 $('stats').innerHTML=[['Processor',rec(c.processor.part_ref).name+' · '+c.processor.clock_mhz+' MHz'],['System RAM',m.ram_kb+' KB'],['Video RAM',m.video_ram_kb+' KB'],['Text display',c.video.text_mode.characters]].map(([k,v])=>`<div class="stat"><span>${esc(k)}</span><strong>${esc(v)}</strong></div>`).join('');
 $('offering-controls').hidden=!['software','bundles'].includes(layer);$('software-choice').hidden=layer!=='software';$('bundle-choice').hidden=layer!=='bundles';
 $('view-title').textContent=c.name.toUpperCase()+' / '+layer.toUpperCase();$('diagram-note').textContent=settings.notes[layer];
 if(layer==='hardware'){
 add('cpu',rec(c.processor.part_ref).name,c.processor.clock_mhz+' MHz',2,1,'Processor',value(rec(c.processor.part_ref).specification),facts(c.processor));
 add('ram','System RAM',m.ram_kb+' KB',1,1,'Memory',m.organization.note,facts({installed_ram_kb:m.ram_kb,lower_ram_kb:m.organization.contiguous_lower_ram_kb,common_system_ram_kb:m.organization.common_system_ram_kb}),[mm.specification.application_policy]);
 add('rom','ROM & cartridges',c.rom_and_cartridges.xip_slots+' cartridge slots',3,1,'Firmware',mm.specification.rom_policy,facts(c.rom_and_cartridges));
 add('video','Video subsystem',m.video_ram_kb+' KB video RAM',1,2,'Display',mm.specification.vram_policy,facts(c.video));
 add('mapper',mm.name,mm.specification.page_size_kb+' KB pages',2,2,'Memory mapper',mm.description,facts(mm.specification),mm.requirements);
 add('flex',rec('technology.flexibus').name,io.flexibus_ports+' ports',3,2,'Peripheral interface',value(rec('technology.flexibus').specification),facts(rec('technology.flexibus').specification));
 add('storage','Internal floppy',c.storage.internal_fdd.count+' × '+c.storage.internal_fdd.size_inch+'″',1,3,'Storage',value(c.storage.internal_fdd),facts(c.storage.internal_fdd));
 add('expansion','Expansion slots',io.expansion_slots.count+' × '+io.expansion_slots.width_bits+'-bit',2,3,'Expansion',value(rec('technology.plug_and_execute').specification),facts(io.expansion_slots));
 edges=nodes.filter(x=>x.id!=='mapper').map(x=>['mapper',x.id]);
 if(net){product('device.network_card_aurelia',3,3,true);edges.push(['expansion','device.network_card_aurelia',true]);}
 }else if(layer==='peripherals'){
 add('host',c.name,'Host computer',2,2,'Computer',c.form_factor,[['FlexiBUS ports',io.flexibus_ports],['Video link',rec(c.video.technology_ref).name]]);
 add('flex',rec('technology.flexibus').name,io.flexibus_ports+' ports',2,1,'Interface',value(rec('technology.flexibus').specification),facts(rec('technology.flexibus').specification));
 product('device.flexibus_keyboard',1,1);product('device.flexiprint40',3,1,true);product('device.flexidisk',1,2,true);product('device.flexidisk_ii',3,2,true);
 add('link',rec(c.video.technology_ref).name,'Display interface',2,3,'Video',value(rec(c.video.technology_ref).specification),facts(rec(c.video.technology_ref).specification));
 const bundled=new Set(catalog.offered_bundles.filter(x=>x.computer_ref===c.id).flatMap(x=>x.included_devices||[]));
 const displays=c.compatible_devices.map(rec).filter(x=>x?.category==='display');
 displays.forEach((r,i)=>{const positions=[[1,3],[3,3],[1,4],[3,4]], [col,row]=positions[i];product(r.id,col,row,!bundled.has(r.id));const n=nodes[nodes.length-1];n.sub=(bundled.has(r.id)?'Bundle option':'Optional')+' · '+r.introduced.event_start_date;edges.push(['link',r.id,!bundled.has(r.id)]);});
 edges.push(['host','flex'],['flex','device.flexibus_keyboard'],['flex','device.flexiprint40',true],['flex','device.flexidisk',true],['flex','device.flexidisk_ii',true],['host','link']);
 if(net){product('device.network_card_aurelia',2,4,true);edges.push(['host','device.network_card_aurelia',true]);}
 }else if(layer==='bundles'){
 buildBundle(c);
 }else if(layer==='software'&&$('software-mode').value!=='internals'){
 buildSoftware(c);
 }else if(layer==='software'){
 const positions={apps:[1,1],ccp:[2,1],tui:[3,1],bdos:[1,2],bios:[2,2],drivers:[3,2],boot:[1,3],runtime:[2,3]};
 os.internal_organization.forEach(r=>{const [col,row]=positions[r.id];add(r.id,r.diagram_label,r.responsibility,col,row,'Software',r.description,[['Component',r.name],['Residence',r.residence],['OS foundation',os.base_version]],r.id==='tui'?os.tui_features.map(x=>x.name+': '+x.description):r.id==='runtime'?mm.call_sequence:[]);});edges=os.internal_relationships.map(e=>[...e]);
 if(net){product('software.cpm_aurelia_networking',3,3,true);edges.push(['drivers','software.cpm_aurelia_networking',true]);}
 }else{
 add('cpu','CPU address space',mm.specification.cpu_address_space_kb+' KB',2,1,'Logical memory',mm.description,facts({cpu_address_space_kb:mm.specification.cpu_address_space_kb,page_size_kb:mm.specification.page_size_kb}));
 add('mapper','Logix memory mapper',mm.specification.page_size_kb+' KB pages',2,2,'Mapping',mm.specification.implementation,facts(mm.specification),mm.requirements);
 add('ram','Physical system RAM',m.ram_kb+' KB',1,1,'RAM',m.organization.note,facts(m.organization));
 add('rom','ROM / cartridges','Banked execution',3,1,'ROM',mm.specification.rom_policy,facts(c.rom_and_cartridges));
 add('vram','Video RAM',m.video_ram_kb+' KB',3,2,'Display memory',mm.specification.vram_policy,[['Mapped pages',m.video_ram_kb/mm.specification.page_size_kb],['Page size',mm.specification.page_size_kb+' KB']]);
 m.organization.normal_view.forEach((r,i)=>add('region'+i,r.role,r.start+'–'+r.end,i+1,3,'Normal application map',r.description,[['Size',(parseInt(r.end,16)-parseInt(r.start,16)+1)/1024+' KB']],[mm.normal_map_explanation]));
 edges=[['cpu','mapper'],['mapper','ram'],['mapper','rom'],['mapper','vram'],...m.organization.normal_view.map((r,i)=>['mapper','region'+i])];
 }
 if(c.memory.expansion_ref&&['hardware','memory'].includes(layer)){
 const card=rec(c.memory.expansion_ref);product(card.id,1,4,true);const n=nodes[nodes.length-1];n.sub=($('ram-card').checked?'Installed':'Optional')+' · '+card.capacity_kb+' KB';n.facts.push(...facts(card.memory_mapping));edges.push([layer==='hardware'?'expansion':'mapper',card.id,true]);
 }
 if(!nodes.some(x=>x.id===selected))selected=nodes[0].id;
 $('diagram').innerHTML='<svg class="wires" aria-hidden="true"></svg>'+nodes.map(n=>`<button class="node ${n.optional?'optional':''}" style="grid-column:${n.col};grid-row:${n.row}" data-node="${esc(n.id)}" aria-pressed="${n.id===selected}" aria-controls="inspector"><small>${esc(n.category)}</small><strong>${esc(n.title)}</strong><span>${esc(n.sub)}</span><span class="plus" aria-hidden="true">+</span></button>`).join('');
 $('diagram').querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{selected=b.dataset.node;selectNode();}));selectNode();renderArchitecture(c,os,mm);renderPortability();requestAnimationFrame(draw);
}

function buildSoftware(c){
 const tools=rec('software.business_tools_aurelia');
 if($('software-mode').value==='portability'){buildPortability();return;}
 if($('software-mode').value==='cartridge'){
 add(tools.id,'Business Tools cartridge',tools.delivery,2,1,'Independent offering',tools.description,[['Introduced',tools.introduced.event_start_date],['Delivery',tools.delivery]],tools.runtime_notes);
 tools.subcomponents.forEach((s,i)=>{const col=i%3+1,row=Math.floor(i/3)+2;add(s.id,s.name,'Cartridge subcomponent',col,row,'Business Tools',s.description,[],tools.runtime_notes);edges.push([tools.id,s.id]);});
 (tools.system_dependencies||[]).forEach((dep,i)=>{add('dependency'+i,dep.name,'External · system cartridge',i+2,3,'System dependency',dep.description,[['Provided by',rec(dep.software_ref).name]]);edges.push([tools.id,'dependency'+i]);});
 }else{
 const software=c.compatible_software.map(rec).filter(x=>x?.sold_separately);
 software.forEach((s,i)=>{product(s.id,i%3+1,Math.floor(i/3)+1);nodes[nodes.length-1].sub='Sold separately · '+s.introduced.event_start_date;});
 }
}

function portableRecords(){return Object.fromEntries(Object.entries(settings.portability_refs).map(([k,id])=>[k,rec(id)]));}
function buildPortability(){
 const p=portableRecords();$('diagram-note').textContent=settings.notes.portability;
 add('shared','Shared application code','Portable logic + small adapters',2,1,'Application',p.framework.specification.migration_model,[],p.framework.specification.application_structure);
 add('api',p.api.name,p.api.specification.version,2,2,'Shared interface',p.api.specification.contract,[],p.api.specification.versioning);
 add('tui','Adaptive TUI','Capabilities, contexts and controls',1,2,'System service',p.tui.specification.state_model,[],p.tui.specification.services.map(x=>x.name+': '+x.description));
 add('graphics','Display & graphics','Enumerate · test · select',3,2,'System service',p.display.specification.mode_policy,[],p.display.specification.functions.map(x=>x.name+': '+x.purpose));
 add('aurelia_build',p.aurelia_tools.name,'Aurelia-hosted Z80 build',1,3,'Development environment',p.aurelia_tools.description,facts(p.aurelia_tools.toolchain));
 add('artemis_build',p.artemis_tools.name,'Artemis-hosted native / cross build',3,3,'Development environment',p.artemis_tools.description,facts(p.artemis_tools.toolchain));
 p.language.specification.targets.forEach((t,i)=>add(t.id,t.name,'Separate target binary',i*2+1,4,'Build target','Target-specific startup code, libraries and calling convention; the C API is shared.',facts(t),p.language.specification.rules));
 edges=[['shared','api'],['api','tui'],['api','graphics'],['shared','aurelia_build'],['shared','artemis_build'],['aurelia_build','z80_cpm'],['artemis_build','z80_cpm'],['artemis_build','era_aionix']];
}
function renderPortability(){
 const p=portableRecords(),api=p.api.specification,g=p.display.specification,lang=p.language.specification,f=p.framework.specification;
 $('portability-section').innerHTML='<div class="eyebrow">C development and migration</div><h2>One API. Separate target builds.</h2><p>'+esc(api.contract)+' '+esc(api.compatibility)+'</p><div class="table-wrap">'+table(['Profile','Target','Contract'],f.build_profiles.map(x=>[x.id,x.target,x.description]))+'</div><details open><summary>Display discovery and mode selection</summary><p>'+esc(g.mode_policy)+'</p>'+table(['C function','Purpose'],g.functions.map(x=>[x.name,x.purpose]))+'<p>'+esc(g.monitor_policy)+'</p><p>'+esc(g.text_mode_policy)+'</p><ol>'+g.selection_sequence.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ol></details><details><summary>Mode descriptors, drawing and future modes</summary>'+list(g.mode_descriptor_fields)+list(g.drawing_operations)+'<p>'+esc(g.future_modes)+'</p><p>'+esc(g.compatibility_canvas)+'</p><p>'+esc(g.framebuffer_policy)+'</p></details><details><summary>Adaptive TUI and application contexts</summary>'+list(p.tui.specification.services.map(x=>x.name+': '+x.description))+'<p>'+esc(p.tui.specification.state_model)+'</p>'+list(p.tui.specification.compatibility_rules)+'</details><details><summary>API versioning, ownership and errors</summary>'+list(api.versioning)+list(api.ownership)+'<p>'+esc(api.file_formats)+'</p><p>Errors: '+esc(api.errors.join('; '))+'</p></details><details><summary>C language and target data models</summary><p>'+esc(lang.language_profile)+'</p><div class="table-wrap">'+table(['Target','char','short','int','long','Data pointer'],lang.targets.map(t=>[t.name,t.char_bits+' bits',t.short_bits+' bits',t.int_bits+' bits',t.long_bits+' bits',t.ordinary_data_pointer_bits+' bits']))+'</div><p>'+esc(lang.width_status)+'</p>'+list(lang.required_features)+list(lang.rules)+'<p>Remaining ABI work</p>'+list(lang.remaining_abi_work)+'</details><details><summary>Aurelia development tools</summary><p>'+esc(p.aurelia_tools.description)+'</p>'+list(p.aurelia_tools.features)+list(facts(p.aurelia_tools.toolchain).map(([k,v])=>k+': '+v))+'</details><details><summary>Artemis native and cross-compilation IDE</summary><p>'+esc(p.artemis_tools.description)+'</p>'+list(p.artemis_tools.features)+list(facts(p.artemis_tools.toolchain).map(([k,v])=>k+': '+v))+'</details><details><summary>Migration boundaries and verification</summary>'+list(f.portability_boundaries)+'<p>'+esc(api.runtime_status)+'</p></details>';
}
function bundleItems(b){
 let result=[];
 if(b.base_bundle_ref)result=bundleItems(rec(b.base_bundle_ref));
 else if(b.computer_ref&&!b.id.includes('upgrade'))result.push({id:b.computer_ref});
 (b.included_devices||[]).forEach(id=>result.push({id}));(b.included_software||[]).forEach(id=>result.push({id}));
 (b.included_services||[]).forEach(s=>result.push({id:s.service_ref,duration:s.duration_years}));
 return result.filter((x,i,arr)=>arr.findIndex(y=>y.id===x.id)===i);
}
function buildBundle(c){
 const bundles=[...catalog.offered_bundles,...(catalog.proposed_bundles||[])].filter(b=>b.computer_ref===c.id||(b.also_compatible_with||[]).includes(c.id));
 const select=$('bundle-select'),chosen=select.value;select.innerHTML=bundles.map(b=>`<option value="${esc(b.id)}">${b.status==='proposed'?'Proposed':'Existing'} · ${esc(b.name)}</option>`).join('');if(bundles.some(b=>b.id===chosen))select.value=chosen;
 const b=rec(select.value),status=b.status==='proposed'?'Proposed package':'Existing offer';
 add('bundle',b.name,status,2,1,'Bundle',b.description||b.name,[['Status',status],['Available from',b.earliest_offer_date||b.introduced?.event_start_date],['Pricing',b.pricing||'No bundle price specified']],b.notes||[]);
 bundleItems(b).forEach((item,i)=>{const x=rec(item.id),col=i%3+1,row=Math.floor(i/3)+2;
 if(x.id.startsWith('computer.'))add(x.id,x.name,x.memory.ram_kb+' KB base RAM',col,row,'Included computer',x.form_factor,facts({processor:x.processor,ram_kb:x.memory.ram_kb,video_ram_kb:x.memory.video_ram_kb}),['Bundle specifications are independent of the exploratory RAM-card and networking controls.']);
 else{product(x.id,col,row);const n=nodes[nodes.length-1];n.category='Included '+label(x.category);if(item.duration){n.sub=item.duration+' year included';n.facts.push(['Included duration',item.duration+' year']);}if(x.subcomponents)n.extra=x.subcomponents.map(s=>s.name+': '+s.description);}
 edges.push(['bundle',x.id]);
 });
}
function selectNode(){const n=nodes.find(x=>x.id===selected);document.querySelectorAll('[data-node]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.node===selected));$('inspector').innerHTML=`<div class="badge">${esc(n.category)} / ${esc(computers[model].name)}</div><h2>${esc(n.title)}</h2><p>${esc(n.description)}</p><dl class="facts">${n.facts.map(([k,v])=>`<div class="fact"><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl>${n.extra.length?'<details><summary>Expand details</summary>'+list(n.extra)+'</details>':''}`;}
function renderArchitecture(c,os,mm){
 const o=c.memory.organization;
 $('memory-section').innerHTML='<div class="eyebrow">Memory organization</div><h2>'+esc(c.name)+' · '+esc(c.memory.ram_kb)+' KB RAM</h2><p>'+esc(mm.description)+'</p><div class="memory-bar">'+o.normal_view.map(r=>`<div style="flex:${parseInt(r.end,16)-parseInt(r.start,16)+1}"><b>${esc(r.start)}–${esc(r.end)}</b>${esc(r.role)}</div>`).join('')+'</div><div class="table-wrap">'+table(['Normal CPU range','Role'],o.normal_view.map(r=>[r.start+'–'+r.end,r.role]))+'</div><p>'+esc(o.note)+' '+esc(mm.specification.common_ram_budget_status)+'</p><p>'+esc(mm.normal_map_explanation)+'</p><p>'+esc(mm.full_ram_explanation)+'</p>'+ (c.memory.expansion_ref?'<details open><summary>Optional RAM expansion</summary><p>'+esc(rec(c.memory.expansion_ref).description)+'</p>'+list(Object.values(rec(c.memory.expansion_ref).memory_mapping).map(value))+'</details>':'') +'<details><summary>How a banked service call works</summary><ol>'+mm.call_sequence.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ol></details><details><summary>Mapping rules and implementation requirements</summary>'+list([...Object.entries(mm.specification).map(([k,v])=>label(k)+': '+value(v)),...mm.requirements])+'</details>';
 const va=os.vanilla_architecture;
 if(mm.specification.implementation_design){const d=mm.specification.implementation_design;$('memory-section').innerHTML+='<details open><summary>CP/M memory discovery and application RAM</summary>'+table(['Installed RAM','Application range','BDOS entry / exclusive limit','TPA bytes'],d.application_memory_profiles.map(p=>[p.installed_ram_kb+' KB',p.application_start+'–'+p.application_end_inclusive,p.bdos_entry,p.tpa_bytes]))+list(facts(d).filter(([k])=>k!=='application memory profiles').map(([k,v])=>k+': '+v))+'</details>';}
 $('software-section').innerHTML='<div class="eyebrow">Operating-system architecture</div><h2>'+esc(os.name)+'</h2><p>'+esc(os.description)+'</p><p>'+esc(os.development_lineage)+'</p><details open><summary>CP/M internal structure</summary><p>'+esc(va.execution_model)+'</p><div class="table-wrap">'+table(['Component','Responsibility'],va.components.map(r=>[r.name,r.description]))+'</div><p>Application entry: <code>'+esc(va.application_entry)+'</code> · Program load address: <code>'+esc(va.program_load_address)+'</code></p><div class="table-wrap">'+table(['Conventional memory region','Purpose'],va.memory_layout.map(r=>[r.region,r.purpose]))+'</div></details><details><summary>Vanilla CP/M 1.4 changes from 1.3</summary>'+list(va.changes_from_1_3)+list(va.limits)+'</details><h2>Proposed internal organization</h2><div class="structure">'+os.internal_organization.map(r=>'<article><small>'+esc(r.responsibility)+'</small><h3>'+esc(r.name)+'</h3><p>'+esc(r.description)+'</p><p><b>Residence:</b> '+esc(r.residence)+'</p></article>').join('')+'</div><details><summary>Aurelia-specific runtime requirements</summary>'+list(os.logix_requirements)+'</details><details><summary>TUI functionality and compatibility</summary>'+list(os.tui_features.map(r=>r.name+': '+r.description))+list(os.compatibility_notes)+'</details><h2>Independent software offerings</h2>'+c.compatible_software.map(rec).filter(x=>x?.sold_separately).map(x=>'<details><summary>'+esc(x.name)+' · '+esc(x.introduced.event_start_date)+'</summary><p>'+esc(x.description||x.positioning||x.relationship||label(x.category))+'</p><p>'+esc(x.delivery||'Delivery format not specified')+'</p>'+list(x.features||x.contents||x.modules?.map(m=>m.name+': '+m.features.join(', '))||[value(rec(x.features_ref)?.specification||{})])+'</details>').join('');
}
function draw(){const parent=$('diagram'),svg=parent.querySelector('svg');if(!svg)return;const r=parent.getBoundingClientRect();svg.innerHTML=edges.map(([a,b,opt])=>{const an=parent.querySelector(`[data-node="${a}"]`),bn=parent.querySelector(`[data-node="${b}"]`);if(!an||!bn)return '';const ar=an.getBoundingClientRect(),br=bn.getBoundingClientRect();return `<path class="wire ${opt?'optional':''}" d="M${ar.x+ar.width/2-r.x},${ar.y+ar.height/2-r.y} L${br.x+br.width/2-r.x},${br.y+br.height/2-r.y}"/>`;}).join('');}
function failure(message){$('load-panel').hidden=false;$('load-status').textContent=message;$('file-choice').hidden=false;}
async function load(){
 $('load-panel').hidden=false;$('file-choice').hidden=true;$('load-status').textContent='Loading the product catalog…';
 if(location.protocol==='file:'){failure('Choose the accompanying JSON file to explore this page offline.');return;}
 try{const response=await fetch('./logix_aion_technical_catalog_v2.json',{cache:'no-store'});if(!response.ok)throw Error('HTTP '+response.status);install(await response.json());}catch(error){failure('Could not load the product catalog. Retry, or choose the JSON file below. '+error.message);}
}
$('catalog-file').addEventListener('change',async e=>{const f=e.target.files[0];if(!f)return;try{install(JSON.parse(await f.text()));}catch(error){failure('Could not open this catalog. '+error.message);}finally{e.target.value='';}});
$('retry').addEventListener('click',load);document.querySelectorAll('[data-layer]').forEach(b=>b.addEventListener('click',()=>{layer=b.dataset.layer;document.querySelectorAll('[data-layer]').forEach(x=>x.setAttribute('aria-pressed',x===b));build();}));$('era').addEventListener('change',build);$('ram-card').addEventListener('change',build);$('software-mode').addEventListener('change',()=>{selected='';build();});$('bundle-select').addEventListener('change',()=>{selected='';build();});if(typeof ResizeObserver!=='undefined')new ResizeObserver(draw).observe($('diagram'));window.addEventListener('resize',draw);install(initialCatalog);


};
window.architectureTemplate="<main>\n<section class=\"hero\"><div><div class=\"eyebrow\">Alternative history \u00b7 Architecture</div><h1 id=\"page-heading\"></h1><p class=\"intro\" id=\"intro\"></p></div><div class=\"hero-note\"><div class=\"eyebrow\">First appearance</div><strong id=\"launch\"></strong><span id=\"event\"></span></div></section>\n<div id=\"load-panel\" class=\"loading\"><p id=\"load-status\" role=\"status\">Loading the product catalog\u2026</p><div id=\"file-choice\" hidden><label>Open the accompanying JSON catalog <input id=\"catalog-file\" type=\"file\" accept=\".json,application/json\"></label><button id=\"retry\">Retry loading</button></div></div>\n<div class=\"models\" id=\"models\" role=\"group\" aria-label=\"Computer model\"></div><div id=\"stats\" class=\"stats\" aria-live=\"polite\"></div>\n<section class=\"workspace\" aria-label=\"Interactive architecture explorer\"><div class=\"toolbar\"><div class=\"tabs\" role=\"group\" aria-label=\"Architecture layer\"><button data-layer=\"hardware\" aria-pressed=\"true\" disabled>01 Hardware</button><button data-layer=\"peripherals\" aria-pressed=\"false\" disabled>02 Peripherals</button><button data-layer=\"software\" aria-pressed=\"false\" disabled>03 Software</button><button data-layer=\"memory\" aria-pressed=\"false\" disabled>04 Memory</button><button data-layer=\"bundles\" aria-pressed=\"false\" disabled>05 Bundles</button></div><label class=\"era\" id=\"ram-choice\" hidden><input type=\"checkbox\" id=\"ram-card\"> <span id=\"ram-card-label\"></span></label><label class=\"era\">Networking <select id=\"era\" disabled><option value=\"launch\">Base configuration</option><option value=\"1981\">With 1981 upgrade</option></select></label></div>\n<div class=\"toolbar\" id=\"offering-controls\" hidden><label id=\"software-choice\">Software view <select id=\"software-mode\"><option value=\"internals\">System internals</option><option value=\"cartridge\">Business Tools cartridge</option><option value=\"packages\">Independent software</option><option value=\"portability\">C portability & builds</option></select></label><label id=\"bundle-choice\" hidden>Bundle <select id=\"bundle-select\"></select></label></div><div class=\"explorer\"><div class=\"canvas\"><div class=\"canvas-top\"><span id=\"view-title\"></span><span>SELECT A BLOCK TO EXPLORE \u2197</span></div><div id=\"diagram\" class=\"diagram\" aria-label=\"Functional architecture diagram\"></div><div class=\"legend\"><span><i></i>Functional relationship</span><span><i class=\"dashed\"></i>Optional accessory / upgrade</span></div><p class=\"diagram-note\" id=\"diagram-note\"></p></div><aside class=\"inspector\" id=\"inspector\" aria-live=\"polite\" aria-label=\"Selected component details\"></aside></div></section>\n<noscript>Enable JavaScript to load the JSON catalog and explore the architecture.</noscript>\n<section class=\"details-section\" id=\"memory-section\"></section><section class=\"details-section\" id=\"software-section\"></section><section class=\"details-section\" id=\"portability-section\"></section>\n<section class=\"lower\"><article><div class=\"eyebrow\">The platform in context</div><h2>A computer. An ecosystem.</h2><p id=\"context\"></p><div id=\"timeline\" class=\"timeline\"></div></article><article><div class=\"eyebrow\">Generation comparison</div><h2>What changes with the plus?</h2><div id=\"comparison\" class=\"table-wrap\"></div></article></section></main>";

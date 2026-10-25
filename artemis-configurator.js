/* Artemis-only configuration workbench. Authored catalogues and saved cost snapshots
   remain authoritative; this module selects and presents them without recosting. */
(function(root){
'use strict';
const categories=typeof module!=='undefined'&&module.exports?require('./catalog-categories.js'):root.CatalogCategories;
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const human=v=>String(v).replace(/_/g,' ');
const money=v=>Number.isFinite(v)?'$'+v.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}):'Not costed';
const processorLabel=(records,p)=>{const name=records[p.part_ref]?.name||p.variant||'';return /MHz/.test(name)?name:p.clock_mhz+' MHz '+name;};
const clean=r=>Object.fromEntries(Object.entries(r||{}).filter(([k])=>!['used_by','used_in','compatible_with','technical_profile'].includes(k)));
function createFamilyModel(catalog,bom,cost,familyId){
 const compositionModel=(typeof module!=='undefined'&&module.exports?require('./bom-details.js'):root.BomDetails).createModel(catalog,bom,cost),graph=compositionModel.graph,model={records:compositionModel.records,components:compositionModel.components,assemblies:new Map(),costs:new Map(cost.products.map(p=>[p.id,p])),cost},line={aurelia:'Aurelia',artemis:'Artemis',athena:'Athena'}[familyId];
 // The sole membership qualifier is computer_line. Availability only labels the choice.
 const products=catalog.product_catalog.products.filter(p=>p.computer_line===line);
 model.bomRows=snapshot=>(snapshot?.bom_lines||[]).map(l=>({...l,name:model.records[l.component_ref]?.name||human(l.component_ref),basis:l.component_ref.startsWith('budgetcost.')?'Complete recurring-cost component':'BOM material',unitCost:Number.isFinite(l.extended_recurring_cost_usd)&&l.quantity>0?l.extended_recurring_cost_usd/l.quantity:null}));
 const options=products.map(p=>{
  const hostRef=p.computer_ref||p.id,host=model.records[hostRef];
  const ram=(p.connected_devices||[]).find(e=>model.records[e.device_ref]?.category==='memory_expansion');
  const config=host.memory.configurations?.find(c=>c.module_ref===ram?.device_ref&&c.populated_modules===ram?.quantity);
  const offer={...p,included_devices:p.connected_devices.map(e=>e.device_ref),included_software:p.attached_products.filter(e=>e.software_ref).map(e=>e.software_ref),manufacturing_variants:(p.revisions||[]).map(r=>({assembly_ref:r.hardware_assembly_ref,effective_from:r.effective_from})),computer_configuration:config?{ram_configuration_id:config.id}:undefined};
  return {id:p.id,name:p.name,group:line+' products',hostRef,ramId:config?.id,offer,cost:model.costs.get(p.id),assemblyRef:p.hardware_assembly_ref||p.id,available:p.introduced.event_start_date,planning:p.catalogue_status==='planned',professional:p.id==='product.comdex82_artemis_autocad',product:p};
 });
 function state(option,revision,date){
  const host=JSON.parse(JSON.stringify(model.records[option.hostRef])),tree=walk(option.id,revision.version),refs=new Set(tree.assemblyRefs.filter(id=>model.records[id]));for(const l of tree.leaves)if(model.records[l.ref])refs.add(l.ref);
  const selected=graph.select(option.id,{version:revision.version});
  const version={connected_devices:selected.composition_definition.filter(l=>l.element_type==='connected_device').map(l=>({...l,device_ref:l.ref}))};
  for(const e of version.connected_devices||[])refs.add(e.device_ref);
  host.storage={controller_ref:host.storage.controller_ref,internal_fdd:{count:0}};for(const e of version.connected_devices||[]){const d=model.records[e.device_ref];if(['floppy_drive_mechanism','hard_disk_drive'].includes(d?.category)&&e.used_socket==='internal_drive'){host.storage[d.category==='hard_disk_drive'?'internal_hdd':'internal_fdd']={...d.specification,count:e.quantity};}}
  const modules=(version.connected_devices||[]).filter(e=>model.records[e.device_ref]?.category==='memory_expansion');
  const first=modules[0],ram=first?{module_ref:first.device_ref,populated_modules:first.quantity,populated_banks:first.quantity/2,ram_kb:modules.reduce((n,e)=>n+e.quantity*model.records[e.device_ref].specification.capacity_kb,0),bank_population:Array.from({length:first.quantity/2},(_,i)=>({bank:i,slots:[2*i,2*i+1]}))}:{ram_kb:host.memory.ram_kb};
  const video=[...refs].filter(id=>categories.isVideoCard(model.records[id])),primary=video.find(id=>id==='device.artemis_video_card_64kb')||video.find(id=>id!=='device.artemis_professional_video_128kb');
  return {option,revision,date,host,tree,refs,ram,primary,additional:video.filter(id=>id!==primary),network:[...refs].some(id=>id.startsWith('device.network_card')),displays:[...refs].filter(id=>categories.isMonitor(model.records[id])),peripherals:(version.connected_devices||[]).filter(e=>e.used_socket==='flexibus').flatMap(e=>Array(e.quantity||0).fill(e.device_ref)),software:[...refs].filter(id=>id.startsWith('software.')||id.startsWith('edition.')),snapshot:assessments(option,revision).find(x=>x.date===date)?.snapshot,externalHdd:option.product.storage?.hard_disk_enclosure==='external qualified subsystem'};
 }
 function revisions(option){return graph.versions(option.id).map(h=>({id:option.id+'@'+h.version_number,version:h.version_number,from:h.valid_from,to:h.valid_to,label:h.valid_from+' - '+h.valid_to}));}
 function walk(id,version){const result=graph.resolve(id,{version:version??graph.versions(id).at(-1).version_number});return {assemblyRefs:result.nodes.map(n=>n.ref),leaves:result.leaves.map(l=>({...l,quantity:l.total_quantity,assemblyPath:l.path,component:model.components.get(l.ref)})),issues:result.issues};}
 function assessments(option,revision){if(compositionModel.costStatus(option.id,revision.version))return [];return (cost.metadata.snapshots||[]).filter(date=>revision.from<=date&&date<revision.to).flatMap(date=>{const snapshot=option.cost?.snapshots?.[date.slice(0,4)];return snapshot&&snapshot.status!=='not_yet_offered'?[{date,snapshot}]:[];});}
 return {...model,options,state,revisions,walk,assessments,graph,costStatus:compositionModel.costStatus};
}

if(typeof module!=='undefined'&&module.exports)module.exports={createFamilyModel};
if(!root.document)return;
root.setupArtemisWorkbench=function(catalog,page){
 if(!['artemis','aurelia','athena'].includes(page.id))return;
 const main=document.querySelector('#app>main');
 main.classList.add('artemis-workbench-page');
 const hero=main.querySelector('.hero');
 hero.querySelector('h1').textContent=page.title;
 for(const node of [...main.children])if(node!==hero)node.remove();
 const panel=document.createElement('section');panel.id='artemis-workbench';panel.innerHTML='<p role="status">Loading configurations, manufacturing evaluations and BOMs…</p>';hero.after(panel);
 DataStore.fetch('generated/models/manufacturing-costs.json').then(r=>r.json()).then(cost=>mount(createFamilyModel(catalog,{},cost,page.id),root.BomDetails.createModel(catalog,{},cost))).catch(error=>{panel.innerHTML='<p role="alert">'+esc(error.message)+'</p><button id="retry-artemis-workbench">Retry</button>';panel.querySelector('button').onclick=()=>location.reload();});
 async function mount(model,bomDetails){
  const records=model.records,params=new URLSearchParams(location.search),modelRef=params.get('model')||page.record_refs[0];
  if(params.has('configuration')){const [id,...version]=params.get('configuration').split('::');params.set('configuration',[await DataStore.resolveComponentId(id),...version].join('::'));}
  let option=model.options.find(x=>x.id===params.get('configuration')?.split('::')[0])||model.options.find(x=>x.hostRef===modelRef&&!x.upgrade&&!x.target)||model.options.find(x=>!x.upgrade&&!x.target),revision,chosenDate,selected='configuration',nodes=new Map();
  panel.innerHTML=`<div class="configuration-toolbar"><label class="configuration-main-choice" for="artemis-configuration">System configuration<select id="artemis-configuration"></select></label></div><p id="configuration-status" class="configuration-status" role="status"></p><div class="configuration-stats" id="configuration-stats"></div><section class="configuration-workspace" aria-label="Computer configuration and component details"><div class="configuration-canvas"><div class="configuration-canvas-heading"><strong>Configuration contents</strong><span>Select any component to inspect it →</span></div><div class="configuration-diagram-scroll" tabindex="0" role="region" aria-label="Nested configuration contents"><div id="configuration-diagram"></div></div><p id="configuration-diagram-note"></p></div><aside class="configuration-inspector" id="configuration-inspector" aria-label="Selected configuration component" aria-live="polite"></aside></section><section class="configuration-cost-section" id="configuration-cost-history"><div class="configuration-section-heading"><div><span class="eyebrow">Nominal USD · saved engineering estimates</span><h2>Manufacturing cost over time</h2></div></div><p>Each row is a recorded June 15 evaluation of this hardware revision. Select a date to inspect its bill of materials.</p><div id="configuration-cost-table"></div></section><section class="configuration-cost-section" id="configuration-bom"><div class="configuration-section-heading"><div><span class="eyebrow" id="configuration-bom-date"></span><h2>Bill of materials &amp; cost decomposition</h2></div></div><div id="configuration-bom-table"></div></section>`;
  const $=id=>document.getElementById(id);
  const column=document.createElement('div');column.className='configuration-detail-column';$('configuration-inspector').before(column);column.innerHTML='<div class="bom-tabs" role="tablist" aria-label="Selected element information"><button type="button" role="tab" id="configuration-tab-details" aria-controls="configuration-panel-details">Details</button><button type="button" role="tab" id="configuration-tab-bom" aria-controls="configuration-panel-bom">Bill of materials</button></div><div id="configuration-panel-details" role="tabpanel" aria-labelledby="configuration-tab-details"></div><div id="configuration-panel-bom" role="tabpanel" aria-labelledby="configuration-tab-bom" hidden><div id="configuration-element-bom"></div></div>';
  $('configuration-panel-details').append($('configuration-inspector'));
  $('configuration-panel-bom').append($('configuration-cost-history'),$('configuration-bom'));
  function activateTab(key,focus=false){for(const name of ['details','bom']){const on=name===key,tab=$('configuration-tab-'+name);tab.setAttribute('aria-selected',String(on));tab.tabIndex=on?0:-1;$('configuration-panel-'+name).hidden=!on;if(on&&focus)tab.focus();}}
  for(const key of ['details','bom']){const tab=$('configuration-tab-'+key);tab.onclick=()=>activateTab(key);tab.onkeydown=e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();activateTab(e.key==='Home'?'details':e.key==='End'?'bom':key==='details'?'bom':'details',true);}};}
  activateTab('details');

  const select=$('artemis-configuration');
  const choices=model.options.map(o=>({option:o,revision:model.revisions(o).at(-1),value:o.id,label:o.name+(o.planning?' · planned':o.product.availability_status==='announced'?' · announced':o.product.catalogue_status==='qualification_pending'?' · acceptance pending':'')}));
  for(const group of [...new Set(model.options.map(x=>x.group))]){const g=document.createElement('optgroup');g.label=group;for(const c of choices.filter(x=>x.option.group===group)){const el=document.createElement('option');el.value=c.value;el.textContent=c.label;g.append(el);}select.append(g);}
  function initRevision(wanted){const revisions=model.revisions(option);revision=revisions.find(r=>r.id===wanted)||revisions.at(-1);select.value=option.id;initDate(params.get('evaluation'));}
  function initDate(wanted){const rows=model.assessments(option,revision);chosenDate=rows.find(r=>r.date===wanted)?.date||rows.at(-1)?.date||revision.from;}
  function updateUrl(){const url=new URL(location.href);url.searchParams.set('configuration',select.value);url.searchParams.delete('revision');url.searchParams.delete('evaluation');url.searchParams.set('model',option.hostRef);if(url.hash.startsWith('#computer.'))url.hash=option.hostRef;history.replaceState(null,'',url);}
  function button(id,title,subtitle,data,ref,extra=''){
   nodes.set(id,{title,subtitle,data,ref});return '<button type="button" class="configuration-node '+extra+'" data-component="'+esc(id)+'"'+(ref?' data-record-ref="'+esc(ref)+'"':'')+' aria-controls="configuration-inspector" aria-pressed="false"><span class="component-label">'+esc(title)+'</span>'+(subtitle?'<strong class="component-value">'+esc(subtitle)+'</strong>':'')+'</button>';
  }
  function recordButton(id,ref,title,subtitle,extra={}){const r=id==='configuration'&&option.product?option.product:records[ref],scope=subtitle||'',reference=/reference|Compatible/.test(scope);const label=title||human(r?.category||ref?.split('.')[0]||'Component');const value=(!title||reference)?r?.name||ref:subtitle;const html=button(id,label,value,{...clean(r),...extra},ref);nodes.get(id).scope=scope;return html;}
  function empty(){return '';}
  function group(id,title,contents,tone){
   const box=document.createElement('div');box.innerHTML=contents;
   const primary=[],optional=[],reference=[];
   for(const child of box.children){const note=nodes.get(child.dataset.component)?.scope||nodes.get(child.dataset.component)?.subtitle||'';const target=/Compatible (option|\/ separately)/.test(note)?optional:/reference/i.test(note)?reference:primary;target.push('<li>'+child.outerHTML+'</li>');}
   const nested=(name,items)=>items.length?'<li><details class="configuration-subgroup"><summary>'+name+' ('+items.length+')</summary><ul>'+items.join('')+'</ul></details></li>':'';
   return '<li class="configuration-group '+tone+'" id="configuration-group-'+id+'"><details open><summary>'+esc(title)+'</summary><ul class="configuration-group-items">'+primary.join('')+nested('Compatible options · not included',optional)+nested('Architecture and full specifications',reference)+'</ul></details></li>';
  }
  function diagram(s){
   nodes=new Map();
   if(s.option.chassis){
    const ch=records[s.option.id];let contents=recordButton('configuration',ch.id,ch.name,'Base computer; no removable devices fitted');
    contents+='<ul class="configuration-sections">'+group('fixed','Fixed hardware',[...s.refs].filter(id=>id!==ch.id&&!records[id].virtual).map((id,i)=>recordButton('fixed-'+i,id,null,'Permanently fitted')).join(''),'configuration-blue')+group('subsystems','Internal subsystems',[...s.refs].filter(id=>records[id].virtual).map((id,i)=>recordButton('subsystem-'+i,id,null,'Fixed BOM group; not a purchasable expansion')).join(''),'configuration-green')+'</ul>';
    contents+='<details open><summary>Available sockets and compatibility</summary>'+root.renderSpecification(ch.expansion_socket_groups,records)+'</details>';
    $('configuration-diagram').className='configuration-list';$('configuration-diagram').innerHTML=contents;$('configuration-diagram-note').textContent='Sockets describe available connections. They do not imply that compatible devices are included.';root.bindSpecificationControls($('configuration-diagram'));bindNodes();return;
   }
   if(page.id!=='artemis'){familyList(s);return;}
   const host=s.host,ram=s.ram,module=records[ram.module_ref],io=host.io_and_expansion;
   let monitor=s.displays.map((id,i)=>recordButton('monitor-'+i,id)).join('')||empty('Monitor','Not included in this configuration');
   const videoLink=s.displays.length?recordButton('display-link','technology.logix_digital_video','Display interface',s.option.professional?'Digital primary / analog professional display':'Logix 4-bit digital video',{selected_monitor_refs:s.displays,...(s.option.professional?{professional_link:records['device.mono_pro_17']?.specification}: {})}):'';
   let expansion=s.primary?recordButton('video',s.primary,'Dedicated video slot',records[s.primary]?.name):empty('Dedicated video slot');
   const cards=[...(s.network?['device.network_card_artemis']:[]),...s.additional,...(s.refs.has('device.artemis_cpm80_module')?['device.artemis_cpm80_module']:[])];
   for(let i=0;i<io.expansion_slots.count;i++)expansion+=cards[i]?recordButton('slot-'+i,cards[i],'Expansion slot '+(i+1),records[cards[i]].name):empty('Expansion slot '+(i+1),'Empty · '+io.expansion_slots.width_bits+'-bit');
   let ports='';for(let i=0;i<io.flexibus_ports;i++)ports+=s.peripherals[i]?recordButton('port-'+i,s.peripherals[i],'FlexiBUS port '+(i+1),records[s.peripherals[i]].name):empty('FlexiBUS port '+(i+1));
   let core=recordButton('cpu',host.processor.part_ref,'Processor',processorLabel(records,host.processor),{selected_host_processor:host.processor})+recordButton('mmu','part.artemis_mmu','MMU','Memory management',{architecture:records['technology.artemis_memory_model']?.specification})+recordButton('dma','part.artemis_dma','DMA','Direct memory access')+recordButton('disk-controller',host.storage.controller_ref,'Disk controller','Floppy / hard disk')+recordButton('flexibus-controller','part.flexibus_host_controller','FlexiBUS interface',io.flexibus_ports+' external ports',{host_interface:io.flexibus_ports+' external ports; chip quantities remain subject to the recorded BOM assumptions.'});
   let memory='';for(let i=0;i<host.memory.bank_count;i++){const populated=ram.bank_population?.some(b=>b.bank===i)??i<ram.populated_banks;memory+=populated?recordButton('bank-'+i,ram.module_ref,'DRAM bank '+(i+1),host.memory.modules_per_bank+' × '+module.specification.capacity_kb+' KiB modules',{selected_bank:ram.bank_population?.find(b=>b.bank===i),configuration:ram}):empty('DRAM bank '+(i+1),'Empty · matched pair required');}
   const os=s.software.find(id=>/^software\.aionix/.test(id));const tools=s.refs.has('device.rom_cartridge.business_tools_artemis')?'software.business_tools_artemis':null;
   memory+=os?recordButton('os-rom',records[os]?.physical_media_refs?.[0]||os,'System ROM cartridge',records[os].name,{capacity_note:'ROM capacity is not specified in this offering record.'}):empty('System cartridge','Not included');
   memory+=tools?recordButton('tools-rom',records[tools]?.physical_media_refs?.[0]||tools,'Application cartridge','AION Business Tools',{capacity_note:'ROM capacity is not specified in this offering record.'}):empty('Application cartridge','Not included');
   memory+=button('boot-rom','Boot ROM','On mainboard',{assembly:host.id,boot_components:s.tree.leaves.filter(l=>/boot_rom/.test(l.ref))},'part.'+host.id+'.boot_rom_chips');
   let disks='';for(let i=0;i<host.storage.internal_fdd.count;i++)disks+=button('fdd-'+i,'Internal floppy '+(i+1),host.storage.internal_fdd.size_inch+'″ · '+host.storage.internal_fdd.density,host.storage.internal_fdd,[...s.refs].find(id=>records[id]?.category==='floppy_drive_mechanism'&&id.startsWith('device.')));
   if(host.storage.internal_hdd)disks+=recordButton('hdd',[...s.refs].find(id=>records[id]?.category==='hard_disk_drive'&&id.startsWith('device.'))||host.storage.internal_hdd.part_ref,'Internal hard disk',host.storage.internal_hdd.capacity_mb+' MB',host.storage.internal_hdd);
   if(s.externalHdd)disks+=recordButton('external-hdd','part.hdd_5mb','External hard disk','5 MB · separate enclosure',{storage:s.option.offer.storage});
   // Retain the old architecture's named memory and software views as selectable children.
   const settings=catalog.artemis_explorer;
   function references(layer){return settings.diagrams[layer].nodes.filter(n=>n.record_ref).map(n=>{
    let ref=n.id==='video_ram'?s.primary:n.record_ref;
    if(layer==='software'&&n.id==='os')ref=s.software.find(id=>/^software\.aionix/.test(id))||settings.os_ref;
    if(!records[ref])return '';
    return recordButton('reference-'+layer+'-'+n.id,ref,n.title,'Architecture reference',n.fields?{selected_fields:Object.fromEntries(n.fields.map(k=>[k,records[ref].specification?.[k]]))}:{});
   }).join('');}
   memory+=references('memory');
   let software=s.software.map((id,i)=>recordButton('software-'+i,id,null,'Included in this configuration')).join('');
   const compatible=(host.compatible_software||[]).filter(id=>!s.software.includes(id));
   software+=compatible.map((id,i)=>recordButton('compatible-software-'+i,id,null,'Compatible / separately supplied · '+(records[id]?.introduced?.event_start_date||'date unknown'))).join('');
   software+=references('software');
   software+=Object.entries(settings.portability_refs).map(([key,id])=>recordButton('portability-'+key,id,null,'Development / portability reference')).join('');
   const present=new Set([...nodes.values()].map(n=>n.ref));
   for(const id of host.compatible_devices||[]){if(present.has(id)||!records[id])continue;const r=records[id],entry=recordButton('optional-'+id,id,null,'Compatible option — not fitted · '+(r.introduced?.event_start_date||'date unknown'));if(categories.isMemory(r))memory+=entry;else if(categories.isExpansion(r))expansion+=entry;else ports+=entry;present.add(id);}
   // Full platform records previously exposed in the reference accordion remain reachable.
   for(const id of page.record_refs){if(id===host.id||present.has(id)||!records[id]||id.startsWith('computer.')||id.startsWith('product.')||id.startsWith('computer_system.'))continue;
    const entry=recordButton('platform-'+id,id,null,'Platform reference — not an included item');
    if(/^(software|edition)\./.test(id)||/api|abi|cpm|os_model|portability|tui/.test(id))software+=entry;else if(/memory|xip/.test(id))memory+=entry;else if(/video|display|monitor|mono_pro|color_pro/.test(id))monitor+=entry;else core+=entry;
   }
   if(s.option.upgrade){core='';memory='';disks='';expansion=[...s.refs].filter(id=>id.startsWith('device.')).map((id,i)=>recordButton('upgrade-'+i,id,null,'Included in upgrade kit')).join('');ports='';monitor='';software=s.software.map((id,i)=>recordButton('upgrade-software-'+i,id,null,'Included in upgrade kit')).join('');}
   core=recordButton('chassis',host.chassis_ref,'Base computer','Fixed hardware and available sockets')+core;
   const system=recordButton('configuration',s.option.offer?.id||host.id,s.option.name,'Full configuration · specifications and cost decomposition',{selected_memory:s.option.upgrade?undefined:ram,selected_revision:revision});
   $('configuration-diagram').className='configuration-list';
   $('configuration-diagram').innerHTML=system+'<ul class="configuration-sections">'+group('core','Mainboard core elements',core||empty('Host computer not included'),'configuration-blue')+group('memory','Memory and Cartridges',memory||empty('Not included'),'configuration-green')+group('disks','Disk drives',disks||empty('Not included'),'configuration-yellow')+group('expansion','Expansion cards',expansion||empty('Not included'),'configuration-green')+group('ports','Flexibus and Video peripherals',monitor+videoLink+ports||empty('Not included'),'configuration-yellow')+group('software','Software',software||empty('Not included'),'configuration-blue')+'</ul>';
   // Discard nodes built for a host that is absent from an upgrade kit.
   const visible=new Set([...$('configuration-diagram').querySelectorAll('[data-component]')].map(b=>b.dataset.component));nodes=new Map([...nodes].filter(([id])=>visible.has(id)));
   $('configuration-diagram-note').textContent=s.option.upgrade?'This upgrade kit is not a complete computer configuration.':'Fitted components, compatible options and architecture references are identified separately. Select the configuration name for its complete BOM and cost history.';
   bindNodes();
  }
  function familyList(s){
   const host=s.host,groups={core:[],memory:[],disks:[],expansion:[],ports:[],software:[]},included=new Set();
   function add(group,id,ref,title,value,data={}){if(ref)included.add(ref);groups[group].push(ref?recordButton(id,ref,title,value,data):button(id,title,value,data));}
   if(!s.option.upgrade){
    add('core','cpu',host.processor.part_ref,'Processor',processorLabel(records,host.processor),{selected_host_processor:host.processor});
    const controller=host.memory.system_controller_ref;if(controller)add('core','system-controller',controller,'System controller',records[controller].name);
    if(host.video?.controller_ref)add('core','graphics-controller',host.video.controller_ref,'Video controller',records[host.video.controller_ref].name);
    if(s.ram.module_ref){for(let i=0;i<s.ram.populated_banks;i++)add('memory','bank-'+i,s.ram.module_ref,'DRAM bank '+(i+1),host.memory.modules_per_bank+' × '+records[s.ram.module_ref].specification.capacity_kb+' KiB',{configuration:s.ram});}
    else add('memory','ram',host.memory.physical_population?.chip_ref,'System RAM',s.ram.ram_kb+' KiB',host.memory);
    const os=host.operating_system_ref||host.rom_and_cartridges?.system_cartridge_ref;
    const candidateOs=s.option.upgradeOffer?.included_software?.[0]||os,selectedOs=s.software.includes(candidateOs)?candidateOs:null;
    if(selectedOs)add('memory','os-rom',[...s.refs].find(id=>records[id]?.software_refs?.includes(selectedOs))||records[selectedOs]?.physical_media_refs?.[0]||selectedOs,host.memory.os_rom?'System ROM':'System cartridge',host.memory.os_rom?host.memory.os_rom.capacity_bytes/1024+' KiB · '+records[selectedOs].name:records[selectedOs].name,{rom:host.memory.os_rom});
    if(host.io_and_expansion.eeprom_bios?.included)add('core','boot-rom',null,'EEPROM BIOS','Boot and diagnostics',host.io_and_expansion.eeprom_bios);
    else if(host.rom_and_cartridges?.mainboard_rom)add('core','boot-rom',null,'Mainboard ROM','Boot / BIOS / drivers',{contents:host.rom_and_cartridges.mainboard_rom});
    const fdd=host.storage.internal_fdd;for(let i=0;i<(fdd?.count||0);i++)add('disks','fdd-'+i,[...s.refs].find(id=>records[id]?.category==='floppy_drive_mechanism'&&id.startsWith('device.')),'Internal floppy '+(i+1),fdd.size_inch+'″ · '+fdd.density,fdd);
    const hdd=host.storage.internal_hdd;if(hdd)add('disks','hdd',[...s.refs].find(id=>records[id]?.category==='hard_disk_drive'&&id.startsWith('device.'))||hdd.part_ref,'Internal hard disk',hdd.capacity_mb+' MB',hdd);
    if(s.primary)add('expansion','video',s.primary,'Video card',records[s.primary].name);
   }
   for(const ref of s.refs){const r=records[ref];if(!r||r.category==='base_computer'||(included.has(ref)&&!ref.startsWith('software.')))continue;if(ref.startsWith('software.'))add('software','included-'+ref,ref,'Included software',r.name);else if(ref.startsWith('device.')){const group=r.virtual?(r.category==='memory_assembly'?'memory':'core'):r.category==='firmware_memory'||r.category==='rom_cartridge'?'memory':categories.hardwareGroup(r);add(group,'included-'+ref,ref,human(r.category||'Peripheral'),r.name);}}
   if(!s.option.upgrade){
    for(const ref of s.refs){const r=records[ref];if(ref.startsWith('part.')&&!included.has(ref)&&r&&!categories.isMemory(r)&&!categories.isDisk(r)&&s.tree.leaves.some(l=>l.ref===ref&&l.assemblyPath?.includes(host.chassis_ref))){add('core','fitted-'+ref,ref,human(r.category||'Component'),r.name);}}
    for(const ref of host.compatible_devices||[]){if(included.has(ref))continue;const r=records[ref];if(!r)continue;const group=categories.hardwareGroup(r);groups[group].push(recordButton('optional-'+ref,ref,null,'Compatible option — not fitted'));included.add(ref);}
    for(const ref of host.compatible_software||[]){if(included.has(ref))continue;groups.software.push(recordButton('compatible-'+ref,ref,null,'Compatible / separately supplied'));included.add(ref);}
    const refs=new Set([...(host.technology_refs||[]),...page.record_refs]);
    for(const ref of refs){if(included.has(ref)||!records[ref]||ref.startsWith('computer.')||ref.startsWith('product.')||ref.startsWith('computer_system.'))continue;const group=/memory|ram|xip/.test(ref)?'memory':/^(software|edition)\.|api|abi|os_model|portability|tui/.test(ref)?'software':/video|display|monitor/.test(ref)?'ports':'core';groups[group].push(recordButton('reference-'+ref,ref,null,'Architecture reference'));}
   }
   if(!s.option.upgrade)groups.core.unshift(recordButton('chassis',host.chassis_ref,'Base computer','Fixed hardware and available sockets'));
   const rootButton=recordButton('configuration',s.option.offer?.id||host.id,s.option.name,'Full specification and BOM',{selected_memory:s.option.upgrade?undefined:s.ram});
   const sections=[['core','Mainboard core elements'],['memory','Memory and Cartridges'],['disks','Disk drives'],['expansion','Expansion cards'],['ports','Flexibus and Video peripherals'],['software','Software']];
   $('configuration-diagram').className='configuration-list';$('configuration-diagram').innerHTML=rootButton+'<ul class="configuration-sections">'+sections.map(([id,title])=>group(id,title,groups[id].join(''),'')).join('')+'</ul>';
   $('configuration-diagram-note').textContent=s.option.upgrade?'This upgrade kit is not a complete computer configuration.':'Only populated elements are listed. Compatible options and architecture references are separate from the selected configuration.';bindNodes();
  }

  function bindNodes(){if(!nodes.has(selected))selected=nodes.keys().next().value;for(const b of $('configuration-diagram').querySelectorAll('[data-component]'))b.addEventListener('click',()=>{selected=b.dataset.component;inspect();});inspect();}
  function inspect(){const n=nodes.get(selected);if(!n)return;for(const b of $('configuration-diagram').querySelectorAll('[data-component]'))b.setAttribute('aria-pressed',String(b.dataset.component===selected));
   const system=selected==='configuration';$('configuration-cost-history').hidden=!system;$('configuration-bom').hidden=!system;
   let bomRef=n.ref;
   const childVersion=model.graph.resolve(option.id,{version:revision.version}).nodes.find(n=>n.ref===bomRef)?.version_number;
   const bomHtml=system?bomDetails.renderBOM(option.id,{version:revision.version}):bomDetails.render(bomRef||selected,{version:childVersion});
   $('configuration-inspector').innerHTML='<div class="eyebrow">'+(system?'Selected configuration':'Selected component')+'</div><h2>'+esc(n.title)+'</h2><p>'+esc([n.subtitle,n.scope!==n.subtitle?n.scope:''].filter(Boolean).join(' · '))+'</p>'+root.renderSpecification(n.data,records);$('configuration-element-bom').innerHTML=bomHtml;root.bindSpecificationControls($('configuration-inspector'));root.bindSpecificationControls($('configuration-element-bom'));bomDetails.bind($('configuration-element-bom'));
  }
  $('configuration-element-bom').addEventListener('compositionchange',e=>{if(e.detail.ref!==option.id)return;revision=model.revisions(option).find(r=>r.version===e.detail.version);initDate();render();});
  function table(headers,rows,caption){return '<div class="configuration-table-scroll" tabindex="0"><table><caption>'+esc(caption)+'</caption><thead><tr>'+headers.map(x=>'<th scope="col">'+esc(x)+'</th>').join('')+'</tr></thead><tbody>'+rows.join('')+'</tbody></table></div>';}
  const td=v=>'<td>'+esc(v)+'</td>';
  function renderCosts(s){
   const rows=model.assessments(option,revision);
   $('configuration-cost-table').innerHTML=rows.length?table(['Evaluation','BOM materials','Manufacturing & fulfillment¹','Licences & services','Total recurring cost','Recorded total range','Status'],rows.map(({date,snapshot:r})=>{const b=r.breakdown_usd||{},extras=Number.isFinite(b.recurring_licenses)&&Number.isFinite(b.included_service_delivery)?b.recurring_licenses+b.included_service_delivery:null,physical=Number.isFinite(r.total_usd)&&extras!==null?r.total_usd-extras:null;return '<tr'+(date===chosenDate?' class="selected-evaluation"':'')+'><th scope="row"><button type="button" data-evaluation="'+date+'" aria-pressed="'+(date===chosenDate)+'">15 June '+date.slice(0,4)+'</button></th>'+td(money(b.bom_materials))+td(money(physical))+td(money(extras))+td(money(r.total_usd))+td(Number.isFinite(r.low_usd)&&Number.isFinite(r.high_usd)?money(r.low_usd)+' – '+money(r.high_usd):'Not recorded')+td(human(r.status))+'</tr>';}),'Cost of '+option.name+' · '+revision.label)+'<p class="configuration-footnote">¹ Physical materials, production, media, packaging and logistics; excludes separately identified recurring licences and service delivery. Ranges apply to the complete recurring estimate. Figures are planning estimates, not supplier quotes. No later-year costs are extrapolated.</p>':'<p class="configuration-empty-state">No June 15 evaluation is recorded for this configuration and revision. '+(option.professional?'The CAD offering starts after the last annual snapshot; its November review is linked below.':option.target?'This is an unqualified expansion design target.':'Unknown costs have not been replaced with zero.')+'</p>';
   const blocked=model.costStatus(option.id,revision.version);if(blocked)$('configuration-cost-table').innerHTML='<p class="cost-reassessment-pending">'+esc(blocked)+'</p>';
   for(const b of $('configuration-cost-table').querySelectorAll('[data-evaluation]'))b.onclick=()=>{chosenDate=b.dataset.evaluation;render();};
   $('configuration-bom-date').textContent=s.snapshot?'Evaluation · '+chosenDate:'Configuration · '+revision.from;
   const lines=model.bomRows(s.snapshot),aggregate=lines.some(l=>l.basis!=='BOM material');
   let html='';
   if(lines.length){html+=table(['Component / cost item','Quantity','Unit cost²','Extended cost','Basis'],lines.map(l=>'<tr>'+ '<th scope="row">'+esc(l.name)+'</th>'+td(l.quantity??'Unspecified')+td(money(l.unitCost))+td(money(l.extended_recurring_cost_usd))+td(l.basis)+'</tr>'),aggregate?'Recorded cost components — full recurring costs, not a material-only BOM':'Costed BOM — leaf components, including model quantity assumptions');
    const sum=lines.every(l=>Number.isFinite(l.extended_recurring_cost_usd))?lines.reduce((n,l)=>n+l.extended_recurring_cost_usd,0):null;
    html+='<p class="configuration-footnote">² Unit cost is the recorded extended cost divided by the estimated quantity. '+(aggregate?'These package and allowance rows already contain production overheads; do not add them to the decomposition below.':'Quantities may include documented model assumptions where the manufacturing BOM remains unresolved.')+' Listed subtotal: <strong>'+money(sum)+'</strong>.</p>';
    const breakdown=s.snapshot.breakdown_usd||{};
    html+=table(['Cost decomposition','USD'],Object.entries(breakdown).map(([k,v])=>'<tr><th scope="row">'+esc(human(k))+'</th>'+td(money(v))+'</tr>').concat('<tr class="configuration-total"><th scope="row">Total recurring estimate</th>'+td(money(s.snapshot.total_usd))+'</tr>'),'Reconciliation to the saved evaluation');
   }else html+='<p class="configuration-empty-state">No costed BOM is recorded for this selection. Structural quantities and unresolved items are listed below where available.</p>';
   if(option.combination)html+='<p>This is a documented host and compatible upgrade combination, not a separately priced catalogue bundle. The base and upgrade BOMs are shown separately; replacement software/media and packaging have not been consolidated into a new assembly or cost.</p>'+bomDetails.render(option.offer?.id||option.hostRef)+bomDetails.render(option.upgradeOffer.id);
   if(s.tree.leaves.length&&!option.combination){html+='<details class="configuration-source-details"'+(!lines.length||aggregate?' open':'')+'><summary>Physical BOM · component quantities and unresolved items</summary>'+table(['Component','Structural quantity','Quantity status'],s.tree.leaves.map(l=>'<tr><th scope="row">'+esc(l.component?.name||l.ref)+'</th>'+td(l.quantity??'Unresolved')+td(l.quantity===null?'Unresolved in authoritative BOM':l.quantity_status||'Defined')+'</tr>'),'Structural BOM for '+revision.id)+'<p>Nested assemblies are expanded to their physical components. Structural quantities can remain unresolved even when the saved estimate uses a documented allowance.</p></details>';}
   html+='<details class="configuration-source-details"><summary>Configuration, assumptions and source records</summary>'+root.renderSpecification({configuration:option.chassis?records[option.id]:option.offer||records[option.hostRef],revision,estimate_assumptions:option.cost?.assumptions,quantity_assumptions:Object.fromEntries(Object.entries(model.cost.unresolved_quantity_assumptions||{}).filter(([k])=>s.tree.assemblyRefs.some(id=>k.startsWith(id+'|')))),estimate_status:model.cost.metadata.estimate_status},records)+'</details><p class="configuration-source-links"><a href="data/view.html?view=hardware-bom">BOM source</a> · <a href="generated/models/manufacturing-costs.json">June 15 evaluations</a>'+(option.professional?' · <a href="generated/models/manufacturing-costs.json">November 1982 CAD review</a>':'')+'</p>';
   $('configuration-bom-table').innerHTML=html;root.bindSpecificationControls($('configuration-bom-table'));bomDetails.bind($('configuration-bom-table'));
  }
  function render(){const s=model.state(option,revision,chosenDate);const status=option.chassis?'Base computer with permanently fitted hardware only; standalone price and manufacturing cost are not established.':option.combination?'Documented host plus optional networking upgrade; no combined cost assessment is recorded.':option.planning?s.host.product_status:option.target?s.ram.validation_status:option.professional?option.offer.status:option.cost?.announced_only||option.offer?.availability_status==='announced'?'Announced; shipment date unconfirmed.':'Offered in the catalogue; engineering estimate, not confirmed shipment.';
   $('configuration-status').textContent=option.name+' · '+status;
   $('configuration-stats').innerHTML=[['Processor',option.upgrade?'Host not included':processorLabel(records,s.host.processor)],['System RAM',option.upgrade?'Host not included':s.ram.ram_kb+' KiB']].map(([k,v])=>'<div><span>'+esc(k)+'</span><strong>'+esc(v)+'</strong></div>').join('');
   diagram(s);renderCosts(s);updateUrl();panel.dataset.ready='true';panel.dataset.configuration=option.id;
  }
  select.onchange=()=>{const choice=choices.find(c=>c.value===select.value);option=choice.option;revision=choice.revision;initDate();render();};
  initRevision(params.get('configuration')?.split('::')[1]||params.get('revision'));render();

 }
};
})(typeof window!=='undefined'?window:globalThis);

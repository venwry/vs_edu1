/* Artemis-only configuration workbench. Authored catalogues and saved cost snapshots
   remain authoritative; this module selects and presents them without recosting. */
(function(root){
'use strict';
const categories=typeof module!=='undefined'&&module.exports?require('./catalog-categories.js'):root.CatalogCategories;
const family=['computer.artemis','computer.artemis_pro'];
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const human=v=>String(v).replace(/_/g,' ');
const money=v=>Number.isFinite(v)?'$'+v.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}):'Not costed';
const clean=r=>Object.fromEntries(Object.entries(r||{}).filter(([k])=>!['used_by','used_in','compatible_with'].includes(k)));
function createModel(catalog,bom,cost){
 const records=Object.fromEntries(Object.values(catalog).filter(Array.isArray).flat().filter(x=>x?.id).map(x=>[x.id,x]));
 const assemblies=new Map(bom.assemblies.map(x=>[x.id,x])),components=new Map(bom.components.map(x=>[x.id,x])),costs=new Map(cost.products.map(x=>[x.id,x]));
 const options=[];
 for(const offer of catalog.offered_bundles.filter(x=>family.includes(x.computer_ref))){
  options.push({id:offer.id,name:offer.name,group:offer.computer_configuration?'Complete systems':'Upgrade kits — host not included',hostRef:offer.computer_ref,ramId:offer.computer_configuration?.ram_configuration_id,offer,cost:costs.get(offer.id),assemblyRef:offer.bom_assembly_ref,available:offer.introduced.event_start_date,upgrade:!offer.computer_configuration});
 }
 for(const row of cost.products.filter(x=>x.group==='Computers'&&family.includes(x.catalog_ref))){
  options.push({id:row.id,name:row.name+' · chassis only',group:'Chassis only',hostRef:row.catalog_ref,ramId:records[row.catalog_ref].memory.configurations.find(x=>row.id.includes('.'+x.id))?.id,cost:row,assemblyRef:row.assembly_ref,available:row.available_from});
 }
 for(const offer of catalog.commercial_offerings||[]){
  const hostRef=offer.component_refs?.find(id=>family.includes(id));if(!hostRef)continue;
  const amount=offer.configuration?.host?.match(/(\d+)\s*MiB/);
  options.push({id:offer.id,name:offer.name,group:'Professional offerings — acceptance pending',hostRef,ramId:amount?records[hostRef].memory.configurations.find(x=>x.ram_kb===Number(amount[1])*1024)?.id:null,offer,cost:costs.get(offer.id),available:offer.introduced.event_start_date,professional:true});
 }
 for(const hostRef of family)for(const ram of records[hostRef].memory.configurations.filter(x=>!x.shipping_configuration)){
  options.push({id:hostRef+'.'+ram.id+'.target',name:records[hostRef].name+' · '+ram.ram_kb+' KiB / '+records[ram.module_ref].specification.capacity_kb+' KiB modules',group:'Expansion design targets — not qualified offers',hostRef,ramId:ram.id,assemblyRef:'assembly.'+hostRef+'.'+ram.id,available:records[hostRef].introduced.event_start_date,target:true});
 }
 function revisions(option){return [{id:option.assemblyRef||option.id,from:option.available,label:'Original configuration · '+option.available},...(option.offer?.manufacturing_variants||[]).map(v=>({id:v.assembly_ref,from:v.effective_from,label:'Networking revision · '+v.effective_from}))];}
 function revisionAt(option,date){return revisions(option).filter(r=>r.from<=date).at(-1);}
 function assessments(option,revision){
  return (cost.metadata.snapshots||[]).filter(d=>d.endsWith('-06-15')).flatMap(date=>{
   const snapshot=option.cost?.snapshots?.[date.slice(0,4)],r=revisionAt(option,date);
   if(!r||r.id!==revision.id||!snapshot||snapshot.status==='not_yet_offered')return [];
   return [{date,snapshot}];
  });
 }
 function walk(id,seen=new Set()){
  if(seen.has(id))throw Error('Circular BOM assembly: '+id);const a=assemblies.get(id);if(!a)return {assemblyRefs:[],leaves:[]};
  const next=new Set(seen).add(id),out={assemblyRefs:[id],leaves:[]};
  for(const line of a.lines||[]){if(assemblies.has(line.ref)){const child=walk(line.ref,next);out.assemblyRefs.push(...child.assemblyRefs);out.leaves.push(...child.leaves.map(l=>({...l,quantity:l.quantity===null||line.quantity===null?null:l.quantity*line.quantity})));}else out.leaves.push({...line,component:components.get(line.ref)});}
  return out;
 }
 function state(option,revision,date){
  const host=records[option.hostRef],ram=host.memory.configurations.find(r=>r.id===option.ramId)||host.memory.configurations.find(r=>r.id===host.memory.default_configuration);
  const tree=walk(revision.id),refs=new Set();
  for(const id of tree.assemblyRefs){const r=id.replace(/^assembly\.(media\.)?/,'');if(records[r])refs.add(r);}
  for(const leaf of tree.leaves)if(leaf.component?.catalog_ref)refs.add(leaf.component.catalog_ref);
  for(const id of option.offer?.included_devices||[])refs.add(id);
  for(const id of option.offer?.component_refs||[])refs.add(id);
  // The dated assembly owns the OS/NIC revision. Budget overlays carry additional software.
  if(![...refs].some(id=>/^software\.aionix/.test(id)))for(const id of option.offer?.included_software||[])refs.add(id);
  for(const id of option.offer?.included_software||[])if(!/^software\.aionix/.test(id))refs.add(id);
  for(const v of option.offer?.software_variants||[])if(v.effective_from<=date)for(const id of v.add||[])refs.add(id);
  const dedicated=host.video_variants?.find(v=>v.configuration_ids.includes(ram.id))?.specification||host.video;
  const videoRefs=[...refs].filter(id=>categories.isVideoCard(records[id]));
  if(!videoRefs.length&&!option.upgrade)videoRefs.push(option.offer?.computer_configuration?.video_card_ref||dedicated.card_ref||host.io_and_expansion.dedicated_video_slot.included_card_ref);
  // Professional CAD replaces the base primary card; do not count both.
  const primary=videoRefs.find(id=>id==='device.artemis_video_card_64kb')||videoRefs.find(id=>id!=='device.artemis_professional_video_128kb');
  const additional=videoRefs.filter(id=>id!==primary);
  const network=refs.has('device.network_card_artemis')||(!option.upgrade&&Boolean(host.networking?.included_by_default));
  const displays=[...refs].filter(id=>categories.isMonitor(records[id]));
  const peripherals=[...refs].filter(id=>id.startsWith('device.')&&!displays.includes(id)&&!videoRefs.includes(id)&&id!=='device.network_card_artemis'&&id!=='device.artemis_cpm80_module'&&!/ram_/.test(id));
  return {option,revision,date,host,ram,tree,refs,primary,additional,network,displays,peripherals,software:[...refs].filter(id=>id.startsWith('software.')),externalHdd:option.offer?.storage?.hard_disk_enclosure==='external qualified subsystem',snapshot:assessments(option,revision).find(x=>x.date===date)?.snapshot};
 }
 function bomRows(snapshot){
  return (snapshot?.bom_lines||[]).map(line=>{
   const component=components.get(line.component_ref),id=line.component_ref.replace(/^budgetcost\./,'');
   return {...line,name:component?.name||records[id]?.name||(id==='allowance.artemis_budget_5mb_subsystem'?'5 MB external HDD subsystem — drive, enclosure, integration and delivery':human(line.component_ref)),basis:line.component_ref.startsWith('budgetcost.')?'Complete recurring-cost component':'BOM material',unitCost:Number.isFinite(line.extended_recurring_cost_usd)&&Number.isFinite(line.quantity)&&line.quantity>0?line.extended_recurring_cost_usd/line.quantity:null};
  });
 }
 return {records,assemblies,components,costs,options,revisions,assessments,state,bomRows,walk,cost};
}
function createFamilyModel(catalog,bom,cost,familyId){
 if(familyId==='artemis')return createModel(catalog,bom,cost);
 const model=createModel(catalog,bom,cost),{records,costs}=model;
 const hosts=catalog.computers.filter(r=>r.id==='computer.'+familyId||r.id.startsWith('computer.'+familyId+'_'));
 const options=[];
 for(const host of hosts){
  const row=cost.products.find(r=>r.id===host.id);
  options.push({id:host.id,name:host.name+(familyId==='athena'?' · planned configuration':' · chassis only'),group:familyId==='athena'?'Planned systems':'Chassis only',hostRef:host.id,cost:row,assemblyRef:row?.assembly_ref||host.bom_assembly_refs?.[0],available:host.introduced.event_start_date,planning:familyId==='athena'});
 }
 for(const offer of catalog.offered_bundles.filter(o=>hosts.some(h=>h.id===o.computer_ref))){const upgrade=(bom.offers||[]).find(o=>o.catalog_ref===offer.id)?.included_host===false;options.push({id:offer.id,name:offer.name,group:upgrade?'Upgrade kits — host not included':'Complete systems',hostRef:offer.computer_ref,offer,cost:costs.get(offer.id),assemblyRef:offer.bom_assembly_ref,available:offer.introduced.event_start_date,upgrade});}
 if(familyId==='aurelia'){
  const upgrade=catalog.offered_bundles.find(o=>o.id==='bundle.aurelia_network_upgrade');
  for(const base of [...options].filter(o=>!o.upgrade))if(upgrade&&(base.hostRef===upgrade.computer_ref||upgrade.also_compatible_with?.includes(base.hostRef))){options.push({...base,id:base.id+'.with-networking',name:base.name+' · networking upgrade fitted',group:'Systems with optional networking upgrade',cost:null,combination:true,upgradeOffer:upgrade,available:upgrade.introduced.event_start_date});}
 }
 function state(option,revision,date){
  const host=records[option.hostRef],ram=host.memory.configurations?.find(c=>c.id===host.memory.default_configuration)||{ram_kb:host.memory.ram_kb},tree=model.walk(revision.id),refs=new Set([...(option.offer?.included_devices||[]),...(option.offer?.included_software||[])]);
  for(const id of tree.assemblyRefs){const ref=id.replace(/^assembly\.(media\.)?/,'');if(records[ref])refs.add(ref);}
  for(const line of tree.leaves)if(line.component?.catalog_ref)refs.add(line.component.catalog_ref);
  if(!option.upgrade){if(host.operating_system_ref)refs.add(host.operating_system_ref);if(host.rom_and_cartridges?.system_cartridge_ref)refs.add(host.rom_and_cartridges.system_cartridge_ref);if(host.network?.included)refs.add(host.network.card_ref);}
  if(option.upgradeOffer){for(const id of option.upgradeOffer.included_devices||[])refs.add(id);for(const id of option.upgradeOffer.included_software||[])refs.add(id);refs.delete(host.rom_and_cartridges?.system_cartridge_ref);}
  const primary=host.graphics_card_ref||host.video?.card_ref;
  const network=[...refs].some(id=>/^device.network_card/.test(id));
  return {option,revision,date,host,ram,tree,refs,primary,network,displays:[...refs].filter(id=>categories.isMonitor(records[id])),peripherals:[...refs].filter(id=>id.startsWith('device.')),software:[...refs].filter(id=>id.startsWith('software.')),snapshot:model.assessments(option,revision).find(x=>x.date===date)?.snapshot};
 }
 return {...model,options,state};
}

if(typeof module!=='undefined'&&module.exports)module.exports={createModel,createFamilyModel};
if(!root.document)return;
root.setupArtemisWorkbench=function(catalog,page){
 if(!['artemis','aurelia','athena'].includes(page.id))return;
 const main=document.querySelector('#app>main');
 main.classList.add('artemis-workbench-page');
 const hero=main.querySelector('.hero');
 hero.querySelector('h1').textContent=page.title;
 for(const node of [...main.children])if(node!==hero)node.remove();
 const panel=document.createElement('section');panel.id='artemis-workbench';panel.innerHTML='<p role="status">Loading configurations, manufacturing evaluations and BOMs…</p>';hero.after(panel);
 Promise.all(['generated/catalogs/hardware-bom.json','generated/models/manufacturing-costs.json'].map(async path=>{const r=await fetch(path);if(!r.ok)throw Error('Unable to load '+path);return r.json();})).then(([bom,cost])=>mount(createFamilyModel(catalog,bom,cost,page.id),root.BomDetails.createModel(catalog,bom,cost))).catch(error=>{panel.innerHTML='<p role="alert">'+esc(error.message)+'</p><button id="retry-artemis-workbench">Retry</button>';panel.querySelector('button').onclick=()=>location.reload();});
 function mount(model,bomDetails){
  const records=model.records,params=new URLSearchParams(location.search),modelRef=params.get('model')||page.record_refs[0];
  let option=model.options.find(x=>x.id===params.get('configuration')?.split('::')[0])||model.options.find(x=>x.hostRef===modelRef&&!x.upgrade&&!x.target)||model.options.find(x=>!x.upgrade&&!x.target),revision,chosenDate,selected='configuration',nodes=new Map();
  panel.innerHTML=`<div class="configuration-toolbar"><label class="configuration-main-choice" for="artemis-configuration">System configuration<select id="artemis-configuration"></select></label></div><p id="configuration-status" class="configuration-status" role="status"></p><div class="configuration-stats" id="configuration-stats"></div><section class="configuration-workspace" aria-label="Computer configuration and component details"><div class="configuration-canvas"><div class="configuration-canvas-heading"><strong>Configuration contents</strong><span>Select any component to inspect it →</span></div><div class="configuration-diagram-scroll" tabindex="0" role="region" aria-label="Nested configuration contents"><div id="configuration-diagram"></div></div><p id="configuration-diagram-note"></p></div><aside class="configuration-inspector" id="configuration-inspector" aria-label="Selected configuration component" aria-live="polite"></aside></section><section class="configuration-cost-section" id="configuration-cost-history"><div class="configuration-section-heading"><div><span class="eyebrow">Nominal USD · saved engineering estimates</span><h2>Manufacturing cost over time</h2></div></div><p>Each row is a recorded June 15 evaluation of this hardware revision. Select a date to inspect its bill of materials.</p><div id="configuration-cost-table"></div></section><section class="configuration-cost-section" id="configuration-bom"><div class="configuration-section-heading"><div><span class="eyebrow" id="configuration-bom-date"></span><h2>Bill of materials &amp; cost decomposition</h2></div></div><div id="configuration-bom-table"></div></section>`;
  const $=id=>document.getElementById(id);
  const column=document.createElement('div');column.className='configuration-detail-column';$('configuration-inspector').before(column);column.append($('configuration-inspector'),$('configuration-cost-history'),$('configuration-bom'));

  const select=$('artemis-configuration');
  const choices=model.options.flatMap(o=>model.revisions(o).map((r,i)=>({option:o,revision:r,value:i?o.id+'::'+r.id:o.id,label:o.name+(model.revisions(o).length>1?' · '+(i?'Networking':'Original')+' · '+r.from:'')})));
  for(const group of [...new Set(model.options.map(x=>x.group))]){const g=document.createElement('optgroup');g.label=group;for(const c of choices.filter(x=>x.option.group===group)){const el=document.createElement('option');el.value=c.value;el.textContent=c.label;g.append(el);}select.append(g);}
  function initRevision(wanted){const revisions=model.revisions(option);revision=revisions.find(r=>r.id===wanted)||revisions[0];select.value=choices.find(c=>c.option===option&&c.revision.id===revision.id).value;initDate(params.get('evaluation'));}
  function initDate(wanted){const rows=model.assessments(option,revision);chosenDate=rows.find(r=>r.date===wanted)?.date||rows.at(-1)?.date||revision.from;}
  function updateUrl(){const url=new URL(location.href);url.searchParams.set('configuration',select.value);url.searchParams.delete('revision');url.searchParams.delete('evaluation');url.searchParams.set('model',option.hostRef);if(url.hash.startsWith('#computer.'))url.hash=option.hostRef;history.replaceState(null,'',url);}
  function button(id,title,subtitle,data,ref,extra=''){
   nodes.set(id,{title,subtitle,data,ref});return '<button type="button" class="configuration-node '+extra+'" data-component="'+esc(id)+'"'+(ref?' data-record-ref="'+esc(ref)+'"':'')+' aria-controls="configuration-inspector" aria-pressed="false"><span class="component-label">'+esc(title)+'</span>'+(subtitle?'<strong class="component-value">'+esc(subtitle)+'</strong>':'')+'</button>';
  }
  function recordButton(id,ref,title,subtitle,extra={}){const r=records[ref],scope=subtitle||'',reference=/reference|Compatible/.test(scope);const label=title||human(r?.category||ref?.split('.')[0]||'Component');const value=(!title||reference)?r?.name||ref:subtitle;const html=button(id,label,value,{...clean(r),...extra},ref);nodes.get(id).scope=scope;return html;}
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
   if(page.id!=='artemis'){familyList(s);return;}
   const host=s.host,ram=s.ram,module=records[ram.module_ref],io=host.io_and_expansion;
   let monitor=s.displays.map((id,i)=>recordButton('monitor-'+i,id)).join('')||empty('Monitor','Not included in this configuration');
   const videoLink=s.displays.length?recordButton('display-link','technology.logix_digital_video','Display interface',s.option.professional?'Digital primary / analog professional display':'Logix 4-bit digital video',{selected_monitor_refs:s.displays,...(s.option.professional?{professional_link:records['device.mono_pro_17']?.specification}: {})}):'';
   let expansion=s.primary?recordButton('video',s.primary,'Dedicated video slot',records[s.primary]?.name):empty('Dedicated video slot');
   const cards=[...(s.network?['device.network_card_artemis']:[]),...s.additional,...(s.refs.has('device.artemis_cpm80_module')?['device.artemis_cpm80_module']:[])];
   for(let i=0;i<io.expansion_slots.count;i++)expansion+=cards[i]?recordButton('slot-'+i,cards[i],'Expansion slot '+(i+1),records[cards[i]].name):empty('Expansion slot '+(i+1),'Empty · '+io.expansion_slots.width_bits+'-bit');
   let ports='';for(let i=0;i<io.flexibus_ports;i++)ports+=s.peripherals[i]?recordButton('port-'+i,s.peripherals[i],'FlexiBUS port '+(i+1),records[s.peripherals[i]].name):empty('FlexiBUS port '+(i+1));
   let core=recordButton('cpu',host.processor.part_ref,'Processor',host.processor.variant+' · '+host.processor.clock_mhz+' MHz',{selected_host_processor:host.processor})+recordButton('mmu','part.artemis_mmu','MMU','Memory management',{architecture:records['technology.artemis_memory_model']?.specification})+recordButton('dma','part.artemis_dma','DMA','Direct memory access')+recordButton('disk-controller',host.storage.controller_ref,'Disk controller','Floppy / hard disk')+recordButton('flexibus-controller','part.flexibus_host_controller','FlexiBUS interface',io.flexibus_ports+' external ports',{host_interface:io.flexibus_ports+' external ports; chip quantities remain subject to the recorded BOM assumptions.'});
   let memory='';for(let i=0;i<host.memory.bank_count;i++){const populated=ram.bank_population?.some(b=>b.bank===i)??i<ram.populated_banks;memory+=populated?recordButton('bank-'+i,ram.module_ref,'DRAM bank '+(i+1),host.memory.modules_per_bank+' × '+module.specification.capacity_kb+' KiB modules',{selected_bank:ram.bank_population?.find(b=>b.bank===i),configuration:ram}):empty('DRAM bank '+(i+1),'Empty · matched pair required');}
   const os=s.software.find(id=>/^software\.aionix/.test(id));const tools=s.software.find(id=>id==='software.business_tools_artemis');
   memory+=os?recordButton('os-rom',os,'System ROM cartridge',records[os].name,{capacity_note:'ROM capacity is not specified in this offering record.'}):empty('System cartridge','Not included');
   memory+=tools?recordButton('tools-rom',tools,'Application cartridge','AION Business Tools',{capacity_note:'ROM capacity is not specified in this offering record.'}):empty('Application cartridge','Not included');
   memory+=button('boot-rom','Boot ROM','On mainboard',{assembly:host.id,boot_components:s.tree.leaves.filter(l=>/boot_rom/.test(l.ref))},'bompart.'+host.id+'.boot_rom_chips');
   let disks='';for(let i=0;i<host.storage.internal_fdd.count;i++)disks+=button('fdd-'+i,'Internal floppy '+(i+1),host.storage.internal_fdd.size_inch+'″ · '+host.storage.internal_fdd.density,host.storage.internal_fdd,'bompart.'+host.id+'.525_inch_double_density_floppy_mechanism');
   if(host.storage.internal_hdd)disks+=recordButton('hdd',host.storage.internal_hdd.part_ref,'Internal hard disk',host.storage.internal_hdd.capacity_mb+' MB',host.storage.internal_hdd);
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
   for(const id of page.record_refs){if(id===host.id||present.has(id)||!records[id]||family.includes(id)||id.startsWith('bundle.')||id.startsWith('offer.'))continue;
    const entry=recordButton('platform-'+id,id,null,'Platform reference — not an included item');
    if(/^(software|edition)\./.test(id)||/api|abi|cpm|os_model|portability|tui/.test(id))software+=entry;else if(/memory|xip/.test(id))memory+=entry;else if(/video|display|monitor|mono_pro|color_pro/.test(id))monitor+=entry;else core+=entry;
   }
   if(s.option.upgrade){core='';memory='';disks='';expansion=[...s.refs].filter(id=>id.startsWith('device.')).map((id,i)=>recordButton('upgrade-'+i,id,null,'Included in upgrade kit')).join('');ports='';monitor='';software=s.software.map((id,i)=>recordButton('upgrade-software-'+i,id,null,'Included in upgrade kit')).join('');}
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
    add('core','cpu',host.processor.part_ref,'Processor',(host.processor.variant||records[host.processor.part_ref]?.name)+' · '+host.processor.clock_mhz+' MHz',{selected_host_processor:host.processor});
    const controller=host.memory.system_controller_ref;if(controller)add('core','system-controller',controller,'System controller',records[controller].name);
    if(host.video?.controller_ref)add('core','graphics-controller',host.video.controller_ref,'Video controller',records[host.video.controller_ref].name);
    if(s.ram.module_ref){for(let i=0;i<s.ram.populated_banks;i++)add('memory','bank-'+i,s.ram.module_ref,'DRAM bank '+(i+1),host.memory.modules_per_bank+' × '+records[s.ram.module_ref].specification.capacity_kb+' KiB',{configuration:s.ram});}
    else add('memory','ram',host.memory.physical_population?.chip_ref,'System RAM',s.ram.ram_kb+' KiB',host.memory);
    const os=host.operating_system_ref||host.rom_and_cartridges?.system_cartridge_ref;
    const selectedOs=s.option.upgradeOffer?.included_software?.[0]||os;
    if(selectedOs)add('memory','os-rom',selectedOs,host.memory.os_rom?'System ROM':'System cartridge',host.memory.os_rom?host.memory.os_rom.capacity_bytes/1024+' KiB · '+records[selectedOs].name:records[selectedOs].name,{rom:host.memory.os_rom});
    if(host.io_and_expansion.eeprom_bios?.included)add('core','boot-rom',null,'EEPROM BIOS','Boot and diagnostics',host.io_and_expansion.eeprom_bios);
    else if(host.rom_and_cartridges?.mainboard_rom)add('core','boot-rom',null,'Mainboard ROM','Boot / BIOS / drivers',{contents:host.rom_and_cartridges.mainboard_rom});
    const fdd=host.storage.internal_fdd;for(let i=0;i<(fdd?.count||0);i++)add('disks','fdd-'+i,null,'Internal floppy '+(i+1),fdd.size_inch+'″ · '+fdd.density,fdd);
    const hdd=host.storage.internal_hdd;if(hdd)add('disks','hdd',hdd.part_ref,'Internal hard disk',hdd.capacity_mb+' MB',hdd);
    if(s.primary)add('expansion','video',s.primary,'Video card',records[s.primary].name);
   }
   for(const ref of s.refs){const r=records[ref];if(!r||(included.has(ref)&&!ref.startsWith('software.')))continue;if(ref.startsWith('software.'))add('software','included-'+ref,ref,'Included software',r.name);else if(ref.startsWith('device.')){const expansion=categories.isExpansion(r);add(expansion?'expansion':'ports','included-'+ref,ref,human(r.category||'Peripheral'),r.name);}}
   if(!s.option.upgrade){
    for(const ref of s.refs){const r=records[ref];if(ref.startsWith('part.')&&!included.has(ref)&&r&&!categories.isMemory(r)&&!categories.isDisk(r)){add('core','fitted-'+ref,ref,human(r.category||'Component'),r.name);}}
    for(const ref of host.compatible_devices||[]){if(included.has(ref))continue;const r=records[ref];if(!r)continue;const group=categories.hardwareGroup(r);groups[group].push(recordButton('optional-'+ref,ref,null,'Compatible option — not fitted'));included.add(ref);}
    for(const ref of host.compatible_software||[]){if(included.has(ref))continue;groups.software.push(recordButton('compatible-'+ref,ref,null,'Compatible / separately supplied'));included.add(ref);}
    const refs=new Set([...(host.technology_refs||[]),...page.record_refs]);
    for(const ref of refs){if(included.has(ref)||!records[ref]||ref.startsWith('computer.')||ref.startsWith('bundle.'))continue;const group=/memory|ram|xip/.test(ref)?'memory':/^(software|edition)\.|api|abi|os_model|portability|tui/.test(ref)?'software':/video|display|monitor/.test(ref)?'ports':'core';groups[group].push(recordButton('reference-'+ref,ref,null,'Architecture reference'));}
   }
   const rootButton=recordButton('configuration',s.option.offer?.id||host.id,s.option.name,'Full specification and BOM',{selected_memory:s.option.upgrade?undefined:s.ram});
   const sections=[['core','Mainboard core elements'],['memory','Memory and Cartridges'],['disks','Disk drives'],['expansion','Expansion cards'],['ports','Flexibus and Video peripherals'],['software','Software']];
   $('configuration-diagram').className='configuration-list';$('configuration-diagram').innerHTML=rootButton+'<ul class="configuration-sections">'+sections.map(([id,title])=>group(id,title,groups[id].join(''),'')).join('')+'</ul>';
   $('configuration-diagram-note').textContent=s.option.upgrade?'This upgrade kit is not a complete computer configuration.':'Only populated elements are listed. Compatible options and architecture references are separate from the selected configuration.';bindNodes();
  }

  function bindNodes(){if(!nodes.has(selected))selected=nodes.keys().next().value;for(const b of $('configuration-diagram').querySelectorAll('[data-component]'))b.addEventListener('click',()=>{selected=b.dataset.component;inspect();});inspect();}
  function inspect(){const n=nodes.get(selected);if(!n)return;for(const b of $('configuration-diagram').querySelectorAll('[data-component]'))b.setAttribute('aria-pressed',String(b.dataset.component===selected));
   const system=selected==='configuration';$('configuration-cost-history').hidden=!system;$('configuration-bom').hidden=!system;
   let bomRef=n.ref;
   const bomHtml=system?'':bomDetails.render(bomRef||selected);
   $('configuration-inspector').innerHTML='<div class="eyebrow">'+(system?'Selected configuration':'Selected component')+'</div><h2>'+esc(n.title)+'</h2><p>'+esc([n.subtitle,n.scope!==n.subtitle?n.scope:''].filter(Boolean).join(' · '))+'</p>'+root.renderSpecification(n.data,records)+bomHtml;root.bindSpecificationControls($('configuration-inspector'));bomDetails.bind($('configuration-inspector'));
  }
  function table(headers,rows,caption){return '<div class="configuration-table-scroll" tabindex="0"><table><caption>'+esc(caption)+'</caption><thead><tr>'+headers.map(x=>'<th scope="col">'+esc(x)+'</th>').join('')+'</tr></thead><tbody>'+rows.join('')+'</tbody></table></div>';}
  const td=v=>'<td>'+esc(v)+'</td>';
  function renderCosts(s){
   const rows=model.assessments(option,revision);
   $('configuration-cost-table').innerHTML=rows.length?table(['Evaluation','BOM materials','Manufacturing & fulfillment¹','Licences & services','Total recurring cost','Recorded total range','Status'],rows.map(({date,snapshot:r})=>{const b=r.breakdown_usd||{},extras=Number.isFinite(b.recurring_licenses)&&Number.isFinite(b.included_service_delivery)?b.recurring_licenses+b.included_service_delivery:null,physical=Number.isFinite(r.total_usd)&&extras!==null?r.total_usd-extras:null;return '<tr'+(date===chosenDate?' class="selected-evaluation"':'')+'><th scope="row"><button type="button" data-evaluation="'+date+'" aria-pressed="'+(date===chosenDate)+'">15 June '+date.slice(0,4)+'</button></th>'+td(money(b.bom_materials))+td(money(physical))+td(money(extras))+td(money(r.total_usd))+td(Number.isFinite(r.low_usd)&&Number.isFinite(r.high_usd)?money(r.low_usd)+' – '+money(r.high_usd):'Not recorded')+td(human(r.status))+'</tr>';}),'Cost of '+option.name+' · '+revision.label)+'<p class="configuration-footnote">¹ Physical materials, production, media, packaging and logistics; excludes separately identified recurring licences and service delivery. Ranges apply to the complete recurring estimate. Figures are planning estimates, not supplier quotes. No later-year costs are extrapolated.</p>':'<p class="configuration-empty-state">No June 15 evaluation is recorded for this configuration and revision. '+(option.professional?'The CAD offering starts after the last annual snapshot; its November review is linked below.':option.target?'This is an unqualified expansion design target.':'Unknown costs have not been replaced with zero.')+'</p>';
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
   html+='<details class="configuration-source-details"><summary>Configuration, assumptions and source records</summary>'+root.renderSpecification({configuration:option.offer||records[option.hostRef],revision,estimate_assumptions:option.cost?.assumptions,quantity_assumptions:Object.fromEntries(Object.entries(model.cost.unresolved_quantity_assumptions||{}).filter(([k])=>s.tree.assemblyRefs.some(id=>k.startsWith(id+'|')))),estimate_status:model.cost.metadata.estimate_status},records)+'</details><p class="configuration-source-links"><a href="generated/catalogs/hardware-bom.json">BOM source</a> · <a href="generated/models/manufacturing-costs.json">June 15 evaluations</a>'+(option.professional?' · <a href="generated/models/manufacturing-costs.json">November 1982 CAD review</a>':'')+'</p>';
   $('configuration-bom-table').innerHTML=html;root.bindSpecificationControls($('configuration-bom-table'));bomDetails.bind($('configuration-bom-table'));
  }
  function render(){const s=model.state(option,revision,chosenDate);const status=option.combination?'Documented host plus optional networking upgrade; no combined cost assessment is recorded.':option.planning?s.host.product_status:option.target?s.ram.validation_status:option.professional?option.offer.status:option.cost?.announced_only||option.offer?.availability_status==='announced'?'Announced; shipment date unconfirmed.':'Offered in the catalogue; engineering estimate, not confirmed shipment.';
   $('configuration-status').textContent=option.name+' · '+status;
   $('configuration-stats').innerHTML=[['Processor',option.upgrade?'Host not included':s.host.processor.clock_mhz+' MHz '+(s.host.processor.variant||records[s.host.processor.part_ref]?.name||'')],['System RAM',option.upgrade?'Host not included':s.ram.ram_kb+' KiB'],['Display',s.primary?records[s.primary]?.name:option.upgrade?'Host not included':'Not specified'],['Networking',s.network?'NIC included':'Not included']].map(([k,v])=>'<div><span>'+esc(k)+'</span><strong>'+esc(v)+'</strong></div>').join('');
   diagram(s);renderCosts(s);updateUrl();panel.dataset.ready='true';panel.dataset.configuration=option.id;
  }
  select.onchange=()=>{const choice=choices.find(c=>c.value===select.value);option=choice.option;revision=choice.revision;initDate();render();};
  initRevision(params.get('configuration')?.split('::')[1]||params.get('revision'));render();

 }
};
})(typeof window!=='undefined'?window:globalThis);

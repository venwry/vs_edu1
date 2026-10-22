/* Artemis-only configuration workbench. Authored catalogues and saved cost snapshots
   remain authoritative; this module selects and presents them without recosting. */
(function(root){
'use strict';
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
  const videoRefs=[...refs].filter(id=>records[id]?.category==='video_card'||/device\.artemis.*video/.test(id));
  if(!videoRefs.length&&!option.upgrade)videoRefs.push(option.offer?.computer_configuration?.video_card_ref||dedicated.card_ref||host.io_and_expansion.dedicated_video_slot.included_card_ref);
  // Professional CAD replaces the base primary card; do not count both.
  const primary=videoRefs.find(id=>id==='device.artemis_video_card_64kb')||videoRefs.find(id=>id!=='device.artemis_professional_video_128kb');
  const additional=videoRefs.filter(id=>id!==primary);
  const network=refs.has('device.network_card_artemis')||(!option.upgrade&&Boolean(host.networking?.included_by_default));
  const displays=[...refs].filter(id=>records[id]?.category==='display');
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
if(typeof module!=='undefined'&&module.exports)module.exports={createModel};
if(!root.document)return;
root.setupArtemisWorkbench=function(catalog,page){
 if(page.id!=='artemis')return;
 const main=document.querySelector('#app>main');
 main.classList.add('artemis-workbench-page');
 const legacy=document.createElement('details');legacy.id='artemis-reference-views';legacy.className='artemis-reference-views';legacy.innerHTML='<summary>More architecture views · software, memory, bundles and full specifications</summary>';
 const hero=main.querySelector('.hero');
 for(const node of [...main.children])if(node!==hero&&!node.id.startsWith('computer.'))legacy.append(node);
 main.append(legacy);
 const panel=document.createElement('section');panel.id='artemis-workbench';panel.innerHTML='<p role="status">Loading configurations, manufacturing evaluations and BOMs…</p>';hero.after(panel);
 Promise.all(['generated/catalogs/hardware-bom.json','generated/models/manufacturing-costs.json'].map(async path=>{const r=await fetch(path);if(!r.ok)throw Error('Unable to load '+path);return r.json();})).then(([bom,cost])=>mount(createModel(catalog,bom,cost))).catch(error=>{panel.innerHTML='<p role="alert">'+esc(error.message)+'</p><button id="retry-artemis-workbench">Retry</button>';panel.querySelector('button').onclick=()=>location.reload();});
 function mount(model){
  const records=model.records,params=new URLSearchParams(location.search),modelRef=params.get('model')||page.record_refs[0];
  let option=model.options.find(x=>x.id===params.get('configuration'))||model.options.find(x=>x.hostRef===modelRef&&!x.upgrade&&!x.target),revision,chosenDate,selected='cpu',nodes=new Map(),connections=[];
  panel.innerHTML=`<div class="configuration-toolbar"><label class="configuration-main-choice" for="artemis-configuration">System configuration<select id="artemis-configuration"></select></label><label for="artemis-revision">Hardware revision<select id="artemis-revision"></select></label><label for="artemis-cost-date">BOM evaluation<select id="artemis-cost-date"></select></label></div><p id="configuration-status" class="configuration-status" role="status"></p><div class="configuration-stats" id="configuration-stats"></div><section class="configuration-workspace" aria-label="Combined Artemis hardware and peripherals"><div class="configuration-canvas"><div class="configuration-canvas-heading"><strong>Hardware &amp; peripherals</strong><span>Select any component to inspect it →</span></div><div class="configuration-diagram-scroll" tabindex="0" role="region" aria-label="Hardware and peripherals diagram"><div id="configuration-diagram"></div></div><p id="configuration-diagram-note"></p></div><aside class="configuration-inspector" id="configuration-inspector" aria-label="Selected configuration component" aria-live="polite"></aside></section><section class="configuration-cost-section" id="configuration-cost-history"><div class="configuration-section-heading"><div><span class="eyebrow">Nominal USD · saved engineering estimates</span><h2>Manufacturing cost over time</h2></div></div><p>Each row is a recorded June 15 evaluation of this hardware revision. Select a date to inspect its bill of materials.</p><div id="configuration-cost-table"></div></section><section class="configuration-cost-section" id="configuration-bom"><div class="configuration-section-heading"><div><span class="eyebrow" id="configuration-bom-date"></span><h2>Bill of materials &amp; cost decomposition</h2></div></div><div id="configuration-bom-table"></div></section>`;
  const $=id=>document.getElementById(id);
  const select=$('artemis-configuration');
  for(const group of [...new Set(model.options.map(x=>x.group))]){const g=document.createElement('optgroup');g.label=group;for(const o of model.options.filter(x=>x.group===group)){const el=document.createElement('option');el.value=o.id;el.textContent=o.name;g.append(el);}select.append(g);}select.value=option.id;
  function initRevision(wanted){const revisions=model.revisions(option);revision=revisions.find(r=>r.id===wanted)||revisions.at(-1);$('artemis-revision').innerHTML=revisions.map(r=>'<option value="'+esc(r.id)+'">'+esc(r.label)+'</option>').join('');$('artemis-revision').value=revision.id;initDate(params.get('evaluation'));}
  function initDate(wanted){const rows=model.assessments(option,revision);chosenDate=rows.find(r=>r.date===wanted)?.date||rows.at(-1)?.date||revision.from;$('artemis-cost-date').innerHTML=rows.length?rows.map(r=>'<option value="'+r.date+'">June 15, '+r.date.slice(0,4)+'</option>').join(''):'<option value="'+esc(chosenDate)+'">No annual evaluation</option>';$('artemis-cost-date').value=chosenDate;$('artemis-cost-date').disabled=!rows.length;}
  function updateUrl(){const url=new URL(location.href);url.searchParams.set('configuration',option.id);url.searchParams.set('revision',revision.id);url.searchParams.set('evaluation',chosenDate);url.searchParams.set('model',option.hostRef);if(family.includes(url.hash.slice(1)))url.hash=option.hostRef;history.replaceState(null,'',url);}
  function button(id,title,subtitle,data,ref,extra=''){
   nodes.set(id,{title,subtitle,data,ref});return '<button type="button" class="configuration-node '+extra+'" data-component="'+esc(id)+'"'+(ref?' data-record-ref="'+esc(ref)+'"':'')+' aria-controls="configuration-inspector" aria-pressed="false"><strong>'+esc(title)+'</strong>'+(subtitle?'<span>'+esc(subtitle)+'</span>':'')+'</button>';
  }
  function recordButton(id,ref,title,subtitle,extra={}){const r=records[ref];return button(id,title||r?.name||human(id),subtitle,{...clean(r),...extra},ref);}
  function empty(title,note='Not fitted'){return '<div class="configuration-empty"><span>'+esc(title)+'</span><em>'+esc(note)+'</em></div>';}
  function group(id,title,contents,tone){return '<section class="configuration-group '+tone+'" id="configuration-group-'+id+'"><h3>'+esc(title)+'</h3><div class="configuration-group-items">'+contents+'</div></section>';}
  function diagram(s){
   nodes=new Map();connections=[];
   if(s.option.upgrade){$('configuration-diagram').className='configuration-upgrade';$('configuration-diagram').innerHTML=group('upgrade','Upgrade kit — host computer not included',[...s.refs].filter(id=>/^(device|software)\./.test(id)).map((id,i)=>recordButton('upgrade-'+i,id)).join(''),'configuration-green');$('configuration-diagram-note').textContent='This option supplies an upgrade kit. It is not a complete computer configuration.';bindNodes();return;}
   const host=s.host,ram=s.ram,module=records[ram.module_ref],io=host.io_and_expansion;
   const monitor=s.displays.map((id,i)=>recordButton('monitor-'+i,id)).join('')||empty('Monitor','Not included in this configuration');
   const videoLink=s.displays.length?recordButton('display-link','technology.logix_digital_video','Display interface',s.option.professional?'Digital primary / analog professional display':'Logix 4-bit digital video',{selected_monitor_refs:s.displays,...(s.option.professional?{professional_link:records['device.mono_pro_17']?.specification}: {})}):'';
   let expansion=s.primary?recordButton('video',s.primary,'Dedicated video slot',records[s.primary]?.name):empty('Dedicated video slot');
   const cards=[...(s.network?['device.network_card_artemis']:[]),...s.additional,...(s.refs.has('device.artemis_cpm80_module')?['device.artemis_cpm80_module']:[])];
   for(let i=0;i<io.expansion_slots.count;i++)expansion+=cards[i]?recordButton('slot-'+i,cards[i],'Expansion slot '+(i+1),records[cards[i]].name):empty('Expansion slot '+(i+1),'Empty · '+io.expansion_slots.width_bits+'-bit');
   let ports='';for(let i=0;i<io.flexibus_ports;i++)ports+=s.peripherals[i]?recordButton('port-'+i,s.peripherals[i],'FlexiBUS port '+(i+1),records[s.peripherals[i]].name):empty('FlexiBUS port '+(i+1));
   const core=recordButton('cpu',host.processor.part_ref,'Processor',host.processor.variant+' · '+host.processor.clock_mhz+' MHz',{selected_host_processor:host.processor})+recordButton('mmu','part.artemis_mmu','MMU','Memory management',{architecture:records['technology.artemis_memory_model']?.specification})+recordButton('dma','part.artemis_dma','DMA','Direct memory access')+recordButton('disk-controller',host.storage.controller_ref,'Disk controller','Floppy / hard disk')+recordButton('flexibus-controller','part.flexibus_host_controller','FlexiBUS interface',io.flexibus_ports+' external ports',{host_interface:io.flexibus_ports+' external ports; chip quantities remain subject to the recorded BOM assumptions.'});
   let memory='';for(let i=0;i<host.memory.bank_count;i++){const populated=ram.bank_population?.some(b=>b.bank===i)??i<ram.populated_banks;memory+=populated?recordButton('bank-'+i,ram.module_ref,'DRAM bank '+(i+1),host.memory.modules_per_bank+' × '+module.specification.capacity_kb+' KiB modules',{selected_bank:ram.bank_population?.find(b=>b.bank===i),configuration:ram}):empty('DRAM bank '+(i+1),'Empty · matched pair required');}
   const os=s.software.find(id=>/^software\.aionix/.test(id));const tools=s.software.find(id=>id==='software.business_tools_artemis');
   memory+=os?recordButton('os-rom',os,'System ROM cartridge',records[os].name,{capacity_note:'ROM capacity is not specified in this offering record.'}):empty('System cartridge','Not included');
   memory+=tools?recordButton('tools-rom',tools,'Application cartridge','AION Business Tools',{capacity_note:'ROM capacity is not specified in this offering record.'}):empty('Application cartridge','Not included');
   memory+=button('boot-rom','Boot ROM','On mainboard',{assembly:host.id,boot_components:s.tree.leaves.filter(l=>/boot_rom/.test(l.ref))});
   let disks='';for(let i=0;i<host.storage.internal_fdd.count;i++)disks+=button('fdd-'+i,'Internal floppy '+(i+1),host.storage.internal_fdd.size_inch+'″ · '+host.storage.internal_fdd.density,host.storage.internal_fdd);
   if(host.storage.internal_hdd)disks+=recordButton('hdd',host.storage.internal_hdd.part_ref,'Internal hard disk',host.storage.internal_hdd.capacity_mb+' MB',host.storage.internal_hdd);
   if(s.externalHdd)disks+=recordButton('external-hdd','part.hdd_5mb','External hard disk','5 MB · separate enclosure',{storage:s.option.offer.storage});
   $('configuration-diagram').className='configuration-board';
   $('configuration-diagram').innerHTML='<svg class="configuration-wires" aria-hidden="true"></svg>'+group('monitors','Monitor / display',monitor+videoLink,'configuration-yellow')+group('expansion','Expansion slots',expansion,'configuration-green')+group('ports','FlexiBUS ports',ports,'configuration-green')+group('core','Mainboard core',core,'configuration-blue')+group('memory','Memory & cartridges',memory,'configuration-green')+group('disks','Disk drives',disks,'configuration-yellow');
   connections=[['cpu','configuration-group-expansion'],['mmu','configuration-group-memory'],['disk-controller','configuration-group-disks'],['flexibus-controller','configuration-group-ports']];if(s.displays.length&&s.primary)connections.push(['display-link','video']);
   $('configuration-diagram-note').textContent='Functional connections; illustrative slot numbering. The primary video connector is dedicated and does not consume a general expansion slot. '+(s.option.target?ram.validation_status:'Only components included in the selected configuration are shown.');
   bindNodes();requestAnimationFrame(drawWires);
  }
  function bindNodes(){if(!nodes.has(selected))selected=nodes.keys().next().value;for(const b of $('configuration-diagram').querySelectorAll('[data-component]'))b.addEventListener('click',()=>{selected=b.dataset.component;inspect();});inspect();}
  function inspect(){const n=nodes.get(selected);if(!n)return;for(const b of $('configuration-diagram').querySelectorAll('[data-component]'))b.setAttribute('aria-pressed',String(b.dataset.component===selected));$('configuration-inspector').innerHTML='<div class="eyebrow">Selected component</div><h2>'+esc(n.title)+'</h2><p>'+esc(n.subtitle||'')+'</p>'+root.renderSpecification(n.data,records);root.bindSpecificationControls($('configuration-inspector'));}
  function drawWires(){const board=$('configuration-diagram'),svg=board?.querySelector('svg');if(!svg)return;const box=board.getBoundingClientRect();if(!box.width)return;svg.setAttribute('viewBox','0 0 '+box.width+' '+box.height);svg.innerHTML=connections.map(([from,to])=>{const a=board.querySelector('[data-component="'+from+'"]')||$(from),b=board.querySelector('[data-component="'+to+'"]')||$(to);if(!a||!b)return '';const ra=a.getBoundingClientRect(),rb=b.getBoundingClientRect(),right=rb.left>ra.left,x1=(right?ra.right:ra.left)-box.left,x2=(right?rb.left:rb.right)-box.left,y1=(ra.top+ra.bottom)/2-box.top,y2=(rb.top+rb.bottom)/2-box.top,mid=(x1+x2)/2;return '<path d="M '+x1+' '+y1+' H '+mid+' V '+y2+' H '+x2+'"/>';}).join('');}
  function table(headers,rows,caption){return '<div class="configuration-table-scroll" tabindex="0"><table><caption>'+esc(caption)+'</caption><thead><tr>'+headers.map(x=>'<th scope="col">'+esc(x)+'</th>').join('')+'</tr></thead><tbody>'+rows.join('')+'</tbody></table></div>';}
  const td=v=>'<td>'+esc(v)+'</td>';
  function renderCosts(s){
   const rows=model.assessments(option,revision);
   $('configuration-cost-table').innerHTML=rows.length?table(['Evaluation','BOM materials','Manufacturing & fulfillment¹','Licences & services','Total recurring cost','Recorded total range','Status'],rows.map(({date,snapshot:r})=>{const b=r.breakdown_usd||{},extras=Number.isFinite(b.recurring_licenses)&&Number.isFinite(b.included_service_delivery)?b.recurring_licenses+b.included_service_delivery:null,physical=Number.isFinite(r.total_usd)&&extras!==null?r.total_usd-extras:null;return '<tr'+(date===chosenDate?' class="selected-evaluation"':'')+'><th scope="row"><button type="button" data-evaluation="'+date+'" aria-pressed="'+(date===chosenDate)+'">15 June '+date.slice(0,4)+'</button></th>'+td(money(b.bom_materials))+td(money(physical))+td(money(extras))+td(money(r.total_usd))+td(Number.isFinite(r.low_usd)&&Number.isFinite(r.high_usd)?money(r.low_usd)+' – '+money(r.high_usd):'Not recorded')+td(human(r.status))+'</tr>';}),'Cost of '+option.name+' · '+revision.label)+'<p class="configuration-footnote">¹ Physical materials, production, media, packaging and logistics; excludes separately identified recurring licences and service delivery. Ranges apply to the complete recurring estimate. Figures are planning estimates, not supplier quotes. No later-year costs are extrapolated.</p>':'<p class="configuration-empty-state">No June 15 evaluation is recorded for this configuration and revision. '+(option.professional?'The CAD offering starts after the last annual snapshot; its November review is linked below.':option.target?'This is an unqualified expansion design target.':'Unknown costs have not been replaced with zero.')+'</p>';
   for(const b of $('configuration-cost-table').querySelectorAll('[data-evaluation]'))b.onclick=()=>{chosenDate=b.dataset.evaluation;$('artemis-cost-date').value=chosenDate;render();};
   $('configuration-bom-date').textContent=s.snapshot?'Evaluation · '+chosenDate:'Configuration · '+revision.from;
   const lines=model.bomRows(s.snapshot),aggregate=lines.some(l=>l.basis!=='BOM material');
   let html='';
   if(lines.length){html+=table(['Component / cost item','Quantity','Unit cost²','Extended cost','Basis'],lines.map(l=>'<tr>'+ '<th scope="row">'+esc(l.name)+'</th>'+td(l.quantity??'Unspecified')+td(money(l.unitCost))+td(money(l.extended_recurring_cost_usd))+td(l.basis)+'</tr>'),aggregate?'Recorded cost components — full recurring costs, not a material-only BOM':'Costed BOM — leaf components, including model quantity assumptions');
    const sum=lines.every(l=>Number.isFinite(l.extended_recurring_cost_usd))?lines.reduce((n,l)=>n+l.extended_recurring_cost_usd,0):null;
    html+='<p class="configuration-footnote">² Unit cost is the recorded extended cost divided by the estimated quantity. '+(aggregate?'These package and allowance rows already contain production overheads; do not add them to the decomposition below.':'Quantities may include documented model assumptions where the manufacturing BOM remains unresolved.')+' Listed subtotal: <strong>'+money(sum)+'</strong>.</p>';
    const breakdown=s.snapshot.breakdown_usd||{};
    html+=table(['Cost decomposition','USD'],Object.entries(breakdown).map(([k,v])=>'<tr><th scope="row">'+esc(human(k))+'</th>'+td(money(v))+'</tr>').concat('<tr class="configuration-total"><th scope="row">Total recurring estimate</th>'+td(money(s.snapshot.total_usd))+'</tr>'),'Reconciliation to the saved evaluation');
   }else html+='<p class="configuration-empty-state">No costed BOM is recorded for this selection. Structural quantities and unresolved items are listed below where available.</p>';
   if(s.tree.leaves.length){html+='<details class="configuration-source-details"'+(!lines.length||aggregate?' open':'')+'><summary>Physical BOM · component quantities and unresolved items</summary>'+table(['Component','Structural quantity','Quantity status'],s.tree.leaves.map(l=>'<tr><th scope="row">'+esc(l.component?.name||l.ref)+'</th>'+td(l.quantity??'Unresolved')+td(l.quantity===null?'Unresolved in authoritative BOM':l.quantity_status||'Defined')+'</tr>'),'Structural BOM for '+revision.id)+'<p>Nested assemblies are expanded to their physical components. Structural quantities can remain unresolved even when the saved estimate uses a documented allowance.</p></details>';}
   html+='<details class="configuration-source-details"><summary>Configuration, assumptions and source records</summary>'+root.renderSpecification({configuration:option.offer||records[option.hostRef],revision,estimate_assumptions:option.cost?.assumptions,quantity_assumptions:Object.fromEntries(Object.entries(model.cost.unresolved_quantity_assumptions||{}).filter(([k])=>s.tree.assemblyRefs.some(id=>k.startsWith(id+'|')))),estimate_status:model.cost.metadata.estimate_status},records)+'</details><p class="configuration-source-links"><a href="generated/catalogs/hardware-bom.json">BOM source</a> · <a href="generated/models/manufacturing-costs.json">June 15 evaluations</a>'+(option.professional?' · <a href="generated/models/comdex-1982-cost-review.json">November 1982 CAD review</a>':'')+'</p>';
   $('configuration-bom-table').innerHTML=html;root.bindSpecificationControls($('configuration-bom-table'));
  }
  function render(){const s=model.state(option,revision,chosenDate);const status=option.target?s.ram.validation_status:option.professional?option.offer.status:option.cost?.announced_only||option.offer?.availability_status==='announced'?'Announced; shipment date unconfirmed.':'Offered in the catalogue; engineering estimate, not confirmed shipment.';
   $('configuration-status').textContent=option.name+' · '+status;
   $('configuration-stats').innerHTML=[['Processor',option.upgrade?'Host not included':s.host.processor.clock_mhz+' MHz '+s.host.processor.variant],['System RAM',option.upgrade?'Host not included':s.ram.ram_kb+' KiB'],['Display',s.primary?records[s.primary]?.name:option.upgrade?'Host not included':'Not specified'],['Networking',s.network?'NIC included':'Not included']].map(([k,v])=>'<div><span>'+esc(k)+'</span><strong>'+esc(v)+'</strong></div>').join('');
   diagram(s);renderCosts(s);updateUrl();panel.dataset.ready='true';panel.dataset.configuration=option.id;
  }
  select.onchange=()=>{option=model.options.find(o=>o.id===select.value);initRevision();render();};$('artemis-revision').onchange=()=>{revision=model.revisions(option).find(r=>r.id===$('artemis-revision').value);initDate();render();};$('artemis-cost-date').onchange=()=>{chosenDate=$('artemis-cost-date').value;render();};
  root.addEventListener('resize',drawWires);if(root.ResizeObserver)new ResizeObserver(drawWires).observe($('configuration-diagram'));
  initRevision(params.get('revision'));render();
 }
};
})(typeof window!=='undefined'?window:globalThis);

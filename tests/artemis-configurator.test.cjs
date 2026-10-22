const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {JSDOM,VirtualConsole}=require('jsdom');
const root=path.resolve(__dirname,'..'),read=f=>fs.readFileSync(path.join(root,f),'utf8'),json=f=>JSON.parse(read(f));
const catalog=json('generated/catalogs/logix-aion-technical-catalog-v2.json'),bom=json('generated/catalogs/hardware-bom.json'),cost=json('generated/models/manufacturing-costs.json');
const {createModel}=require('../artemis-configurator.js'),model=createModel(catalog,bom,cost);
assert.equal(new Set(model.options.map(o=>o.id)).size,model.options.length);
const family=['computer.artemis','computer.artemis_pro'];
for(const offer of catalog.offered_bundles.filter(o=>family.includes(o.computer_ref)))assert(model.options.some(o=>o.id===offer.id),'missing offer '+offer.id);
for(const host of catalog.computers.filter(x=>family.includes(x.id)))for(const cfg of host.memory.configurations)assert(model.options.some(o=>o.hostRef===host.id&&o.ramId===cfg.id),'missing memory option '+cfg.id);
const mono=model.options.find(o=>o.id==='bundle.artemis_128_mono'),[launch,network]=model.revisions(mono);
assert.deepEqual(model.assessments(mono,launch).map(x=>x.date),['1980-06-15']);
assert.deepEqual(model.assessments(mono,network).map(x=>x.date),['1981-06-15','1982-06-15']);
const base=model.state(mono,launch,'1980-06-15'),net=model.state(mono,network,'1981-06-15');
assert.equal(base.network,false);assert.equal(net.network,true);assert(base.software.includes('software.aionix'));assert(net.software.includes('software.aionix_server'));assert(!net.software.includes('software.aionix'));assert.equal(net.primary,'device.artemis_video_card_16kb');assert.deepEqual(net.displays,['device.mono_monitor_2']);
for(const option of model.options)for(const revision of model.revisions(option)){
 const dates=model.assessments(option,revision);for(const {date,snapshot} of dates){assert(date>=revision.from);assert.equal(snapshot,option.cost.snapshots[date.slice(0,4)]);assert.notEqual(snapshot.status,'not_yet_offered');const state=model.state(option,revision,date);assert(state.host);assert(state.ram);assert.equal(state.snapshot,snapshot);}
 if(option.target||option.professional)assert.equal(dates.length,0);
}
const budget=model.options.find(o=>o.id==='bundle.artemis_budget_128_hdd');const budgetState=model.state(budget,model.revisions(budget).at(-1),'1981-06-15');assert(budgetState.network);assert(budgetState.externalHdd);assert(budgetState.software.includes('software.abacus_3'));assert(model.bomRows(budgetState.snapshot).every(l=>l.basis==='Complete recurring-cost component'));
const unknown=model.bomRows({bom_lines:[{component_ref:'unpriced',quantity:null,extended_recurring_cost_usd:null}]})[0];assert.equal(unknown.unitCost,null);
(async()=>{
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
 const dom=new JSDOM(read('artemis.html'),{url:'https://atlas.test/artemis.html',runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:vc}),w=dom.window,d=w.document;
 w.IntersectionObserver=class{observe(){}disconnect(){}};w.fetch=async p=>({ok:true,json:async()=>json(String(p).replace(/^\.\//,''))});
 for(const script of d.scripts){if(script.src)w.eval(read(new URL(script.src).pathname.slice(1)));else if(!script.type||script.type==='text/javascript')w.eval(script.textContent);}
 for(let i=0;i<40&&!d.querySelector('#artemis-workbench[data-ready]');i++)await new Promise(r=>setTimeout(r,25));
 assert(d.querySelector('#artemis-workbench[data-ready]'),d.body.textContent.slice(-500));
 const change=(id,value)=>{const el=d.getElementById(id);el.value=value;el.dispatchEvent(new w.Event('change'));};
 assert.equal(d.querySelectorAll('#artemis-configuration option').length,model.options.length);
 for(const option of model.options){change('artemis-configuration',option.id);assert.equal(d.getElementById('artemis-workbench').dataset.configuration,option.id);assert(d.getElementById('configuration-inspector').textContent.length>20);for(const button of d.querySelectorAll('#configuration-diagram [data-component]')){button.click();assert(d.getElementById('configuration-inspector').textContent.includes(button.querySelector('strong').textContent));}for(const rev of model.revisions(option)){change('artemis-revision',rev.id);const dates=model.assessments(option,rev);assert.equal(d.querySelectorAll('[data-evaluation]').length,dates.length);for(const {date,snapshot} of dates){change('artemis-cost-date',date);assert(d.getElementById('configuration-bom-date').textContent.includes(date));assert.equal(d.querySelectorAll('#configuration-bom-table table')[0].querySelectorAll('tbody tr').length,snapshot.bom_lines.length);}}
 }
 change('artemis-configuration','bundle.artemis_256_color');assert(d.querySelector('[data-component="bank-0"]'));assert.equal(d.querySelectorAll('[data-component^="bank-"]').length,1);assert.equal(d.querySelectorAll('#configuration-group-expansion .configuration-group-items>*').length,5);
 d.querySelector('[data-component="mmu"]').click();assert(d.getElementById('configuration-inspector').textContent.includes('Artemis MMU chip'));
 change('artemis-cost-date','1981-06-15');assert.equal(d.querySelector('[data-component="mmu"]').getAttribute('aria-pressed'),'true');
 change('artemis-configuration','bundle.artemis_pro_1mb_mono_pro');assert.equal(d.querySelectorAll('[data-component^="bank-"]').length,4);assert(d.querySelector('[data-component="hdd"]'));assert(d.querySelector('[data-component="fdd-1"]'));assert(d.getElementById('configuration-status').textContent.includes('unconfirmed'));
 change('artemis-configuration','offer.comdex82_artemis_autocad');assert(d.getElementById('configuration-cost-table').textContent.includes('No June 15'));assert.equal(d.querySelectorAll('[data-component^="monitor-"]').length,2);assert(d.getElementById('configuration-stats').textContent.includes('NIC included'));
 change('artemis-configuration','bundle.artemis_network_upgrade');assert(!d.querySelector('[data-component="cpu"]'));assert(d.getElementById('configuration-diagram-note').textContent.includes('not a complete computer'));
 assert.deepEqual(errors,[]);dom.window.close();console.log('PASS:',model.options.length,'configuration choices, dated revisions, BOM identity, all controls and component inspector');
})().catch(e=>{console.error(e);process.exitCode=1;});

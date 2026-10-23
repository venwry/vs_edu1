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
console.log('PASS: Artemis offerings, revisions, saved costs, memory configurations and unknown quantities');

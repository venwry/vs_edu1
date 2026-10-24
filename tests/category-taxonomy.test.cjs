const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const read=p=>require('../data-store.js').read(p);
const c=read('generated/catalogs/logix-aion-technical-catalog-v2.json'),b=read('generated/catalogs/hardware-bom.json'),cost=read('generated/models/manufacturing-costs.json');
const allowed=new Set(read('schemas/category.schema.json').enum),categories=require('../catalog-categories.js'),details=require('../bom-details.js');
const m=details.createModel(c,b,cost),item=id=>m.items.find(x=>x.id===id);
assert.equal(m.items.length,398);assert.equal(new Set(m.items.map(x=>x.id)).size,398);
for(const x of m.items)assert(allowed.has(x.category),x.id+' '+x.category);
for(const x of c.platform_editions){assert(!Object.hasOwn(x,'category'));assert.equal(item(x.id).category,m.records[x.product_ref].category);}
for(const x of b.components){assert(!Object.hasOwn(x,'catalog_ref'));assert.deepEqual(x,m.records[x.id]);}
for(const [id,cat] of Object.entries({'part.color_monitor_controller':'display_controller_ic','part.aurelia_monitor_dac':'video_dac_ic','part.artemis_graphics_chip':'graphics_controller_ic','device.color_monitor_1':'monitor','device.artemis_video_card':'video_expansion_card','part.computer.artemis.mainboard_pcb':'printed_circuit_board'}))assert.equal(item(id).category,cat);
assert.equal(c.devices.filter(categories.isMonitor).length,7);
for(const x of c.devices)assert.equal(item(x.id).class,categories.isExpansion(x)?'Expansion':'Peripheral');
assert.equal(categories.hardwareGroup(m.records['part.ram_64kb_x32']),'memory');
assert.equal(categories.hardwareGroup(m.records['device.artemis_video_card']),'expansion');
assert.equal(details.vendorName(m.records['computer.artemis'],m.records),'Logix');
assert.equal(details.vendorName(m.records['software.aionix2'],m.records),'AION Software');
assert.equal(details.vendorName(m.records['software.microsoft_basic_aurelia'],m.records),'Microsoft');
const core=item('part.device.mono_pro_17.oem_17inch_core').record;
assert.equal(core.manufacturer,null);assert.equal(core.qualification_status,'unresolved');assert.equal(details.vendorName(core),'Ball Brothers (candidate)');
assert.equal(m.items.filter(x=>details.vendorName(x.record,m.records)==='Unknown').length,11);
for(const review of Object.values(cost.reviews))for(const row of review.products||review.prices||[])assert(m.records[row.id],row.id+' has a canonical identity');
console.log('PASS: 398 canonical categories, parent inheritance, hardware groups, reviewed offers and qualified vendor attribution');

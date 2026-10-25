const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {create,fromDocuments}=require('../composition-resolver');
const line=(ref,quantity=1)=>({ref,quantity,unit:'each',condition:'always',role:'',quantity_status:quantity===null?'unresolved':'defined'});
const history=(n,start,end,lines)=>({version_number:n,valid_from:start,valid_to:end,composition_definition:lines});
const records=[{id:'part.x',bom_role:'material'},
 {id:'device.child',composition_history:[history(1,'1980-01-01','1981-01-01',[line('part.x',2)]),history(2,'1981-01-01','1990-01-01',[line('part.x',5)])]},
 {id:'device.parent',composition_history:[history(1,'1980-06-01','1990-01-01',[line('device.child',3)])]},
 {id:'product.test',composition_history:[history(1,'1982-01-01','1990-01-01',[line('device.parent',2)])]}];
const graph=create(records);
// A late pricing date does not silently upgrade a child of a 1980 parent.
assert.equal(graph.resolve('product.test',{date:'1984-01-01'}).leaves[0].total_quantity,12);
assert.equal(graph.select('device.child',{date:'1981-01-01'}).version_number,2);
assert.throws(()=>graph.select('device.child',{date:'1990-01-01'}),/No unique/);
assert.throws(()=>graph.resolve('device.child',{}),/requires/);
assert.equal(graph.resolve('device.parent',{version:1}).rows[0].version_number,1);
records[2].composition_history[0].composition_definition[0].quantity=null;
assert.equal(graph.resolve('product.test',{version:1}).leaves[0].total_quantity,null);
records[2].composition_history[0].valid_from='1979-01-01';
assert.equal(graph.resolve('device.parent',{version:1}).issues[0].kind,'child_date_coverage');
records[2].composition_history[0].valid_from='1980-06-01';records[1].composition_history[0].composition_definition=[line('device.parent')];
assert.throws(()=>graph.resolve('device.parent',{version:1}),/cycle/);
const root=path.resolve(__dirname,'..'),docs=Object.fromEntries(['devices','software-editions','product-catalog','components','services'].map(n=>[n,JSON.parse(fs.readFileSync(path.join(root,'data',n+'.json')))]));
const live=fromDocuments(docs);let count=0;
for(const p of [...docs.devices.devices,...docs['software-editions'].software_editions,...docs['product-catalog'].products])for(const h of p.composition_history){const result=live.resolve(p.id,{version:h.version_number});assert.deepEqual(result.issues,[],p.id);count++;}
for(const [id,quantity] of [['offer.comdex82_artemis_autocad',4],['offer.comdex82_reference_hardware',4],['offer.comdex82_professional_hardware',2],['offer.comdex82_upgrade_autocad',2]]){
 const r=live.resolve(id,{date:'1982-11-29'});assert.equal(r.leaves.filter(l=>l.ref==='part.aion_2114').reduce((n,l)=>n+l.total_quantity,0),quantity,id);
}
console.log('PASS: '+count+' composition versions; boundary dates, recursive parent dates, unknown quantities, missing coverage, cycles and four November inventories');

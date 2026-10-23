const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..'),loader=require('../data-store.js');
const reg=loader.read('schemas/data-registry.json'),fixture=loader.read('tests/fixtures/single-data-migration.json');
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==='object'?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
(async()=>{
 const py=JSON.parse(require('node:child_process').execFileSync('python',['-c',"import sys,json;sys.path.insert(0,'tools');from data_store import registry,read_document;print(json.dumps({n:read_document('catalog:'+n) for n in registry()['views']}))"],{cwd:root,maxBuffer:10000000}));for(const name of Object.keys(reg.views))assert.deepEqual(loader.read('catalog:'+name),py[name],name);
 const calls=[],collections={},ctx={fetch:async p=>{calls.push(p);assert(!p.startsWith('generated/catalogs/'));return {ok:true,json:async()=>collections[p]||loader.read(p)}}};
 vm.createContext(ctx);vm.runInContext(fs.readFileSync(path.join(root,'data-store.js'),'utf8'),ctx);
 const file='data/components.json';collections[file]=loader.read(file);collections[file].base_parts[0].vendor='Migration test supplier';
 const name='logix-aion-technical-catalog-v2';
 const [a,b]=await Promise.all([ctx.DataStore.fetch('catalog:'+name),ctx.DataStore.fetch('generated/catalogs/'+name+'.json')]);
 assert.equal((await a.json()).base_parts[0].vendor,'Migration test supplier');assert.deepEqual(await a.json(),await b.json());
 assert.equal(calls.length,new Set(calls).size,'Concurrent reads must share collection requests');
 assert(!fs.existsSync(path.join(root,'generated/catalogs')));
 console.log('PASS: all 25 JS views preserve payloads; direct edits appear without generation; concurrent fetches are deduplicated');
})().catch(e=>{console.error(e);process.exitCode=1});

// JSON-in/JSON-out bridge: Python uses exactly the browser's resolution algorithm.
const fs=require('node:fs'),path=require('node:path'),resolver=require('../composition-resolver.js');
let input='';process.stdin.on('data',s=>input+=s);process.stdin.on('end',()=>{
 try{const request=JSON.parse(input),base=request.root||path.resolve(__dirname,'..');
 const docs=request.documents||Object.fromEntries(['devices','software-editions','product-catalog','components','services'].map(name=>[name,JSON.parse(fs.readFileSync(path.join(base,'data',name+'.json'),'utf8'))]));
 const registry=JSON.parse(fs.readFileSync(path.join(base,'schemas/data-registry.json'),'utf8'));
 const aliases={...registry.record_id_aliases,...registry.device_assembly_aliases,...registry.platform_device_aliases,...registry.composition_aliases};
 const graph=resolver.fromDocuments(docs,aliases);
 const results=request.requests.map(q=>{try{return {result:graph.resolve(q.ref,q.selection)}}catch(e){return {error:e.message}}});
 process.stdout.write(JSON.stringify(results));
 }catch(e){process.stderr.write(e.stack);process.exitCode=1;}
});

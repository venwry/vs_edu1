/* Authoritative temporal composition graph, shared by browsers and Python via Node. */
(function(root){'use strict';
function create(records,aliases={}){
 const index=Array.isArray(records)?Object.fromEntries(records.map(r=>[r.id,r])):records;
 function identity(ref){const alias=aliases[ref];return typeof alias==='string'?{ref:alias}:alias||{ref};}
 function owner(ref){return index[identity(ref).ref];}
 function versions(ref){return owner(ref)?.composition_history||[];}
 function select(ref,{version,date}={}){
  const target=identity(ref),history=versions(ref);version=version??target.version_number;
  if(version===undefined&&!date)throw Error('Composition selection requires a version or date: '+ref);
  const matches=history.filter(h=>(version===undefined||h.version_number===Number(version))&&(!date||h.valid_from&&h.valid_from<=date&&date<h.valid_to));
  if(matches.length!==1)throw Error('No unique composition version for '+target.ref+' at '+(date||'version '+version));
  return matches[0];
 }
 function resolve(ref,selection){
  const target=identity(ref),record=owner(ref),rows=[],issues=[],nodes=[];
  if(!record)throw Error('Unknown composition owner: '+ref);
  const initial=select(ref,selection);
  function walk(r,h,path,multiplier,conditions){
   if(path.includes(r.id))throw Error('Composition cycle: '+[...path,r.id].join(' -> '));
   nodes.push({ref:r.id,quantity:multiplier,version_number:h.version_number,valid_from:h.valid_from,valid_to:h.valid_to,metadata:h.bom_assembly_metadata||{}});
   const next=[...path,r.id];
   for(const line of h.composition_definition){
    const child=owner(line.ref),quantity=line.quantity===null||multiplier===null?null:line.quantity*multiplier;
    const row={...line,name:child?.name||line.ref,depth:path.length,total_quantity:quantity,path:next,conditions:[...conditions,line.condition],leaf:!child?.composition_history};rows.push(row);
    if(!child){issues.push({kind:'missing_reference',ref:line.ref});continue;}
    if(child.composition_history){
     if(next.includes(child.id))throw Error('Composition cycle: '+[...next,child.id].join(' -> '));
     try{const chosen=select(child.id,{date:h.valid_from});row.version_number=chosen.version_number;row.valid_from=chosen.valid_from;row.valid_to=chosen.valid_to;walk(child,chosen,next,quantity,row.conditions);}
     catch(e){if(e.message.startsWith('Composition cycle'))throw e;issues.push({kind:'child_date_coverage',ref:child.id,parent:r.id,date:h.valid_from,message:e.message});row.issue=e.message;}
    }
   }
  }
  walk(record,initial,[],1,[]);
  const leaves=rows.filter(r=>r.leaf&&index[r.ref]?.bom_role==='material');
  return {ref:target.ref,version:initial,rows,nodes,leaves,issues};
 }
 return {records:index,identity,owner,versions,select,resolve};
}
function fromDocuments(docs,aliases={}){return create(Object.values(docs).flatMap(d=>Object.values(d).filter(Array.isArray).flat()).filter(r=>r?.id),aliases);}
const api={create,fromDocuments};root.CompositionResolver=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window==='undefined'?globalThis:window);

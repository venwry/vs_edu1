"""Validate collection schemas, identities, references and assembly integrity without writing."""
import json,re,sys
from pathlib import Path
import jsonschema
from data_store import ROOT,registry,read_document
from schema_validation import record_validator

def validate_collections(root=ROOT, overrides=None):
    root=Path(root);reg=registry(root);overrides=overrides or {}
    expected=set(reg['files']);actual={p.relative_to(root).as_posix() for p in (root/'data').rglob('*.json')}
    if expected!=actual:raise ValueError('Unregistered/missing collections: '+str(expected^actual))
    docs={p:overrides[p] if p in overrides else json.loads((root/p).read_text()) for p in reg['files']}
    if set(overrides)-expected:raise ValueError('Unregistered write target')
    for p,doc in docs.items():
        schema=(root/p).parent/doc['$schema']
        if not schema.resolve().is_relative_to((root/'schemas/collections').resolve()):raise ValueError('Invalid schema location: '+p)
        record_validator(json.loads(schema.read_text())).validate(doc)
    def unique(rows,label):
        ids=[r['id'] for r in rows]
        if len(ids)!=len(set(ids)):raise ValueError('Duplicate IDs in '+label)
        return {r['id']:r for r in rows}
    # Use the provided documents, including staged edits, for all relationship checks.
    recipe=reg['views']['logix-aion-technical-catalog-v2']
    tech={k:docs[v['file']][v['key']] for k,v in recipe.items()}
    records=unique([r for rows in tech.values() if isinstance(rows,list) for r in rows if isinstance(r,dict) and 'id'in r],'technical records')
    def refs(value):
        if isinstance(value,dict):
            for v in value.values():refs(v)
        elif isinstance(value,list):
            for v in value:refs(v)
        elif isinstance(value,str) and re.fullmatch(r'(?:computer|software|part|device|technology|service|bundle|edition)\.[a-z0-9_.]+',value):
            if value not in records:raise ValueError('Unresolved technical reference: '+value)
    refs(tech)
    for e in tech['platform_editions']:
        if e['product_ref'] not in {p['id'] for p in tech['software_products']}:raise ValueError('Edition must reference a software product: '+e['id'])
    parts=unique(docs['data/sourcing.json']['components'],'BOM components');assemblies=unique(docs['data/assemblies.json']['assemblies'],'assemblies')
    for p in parts.values():
        if p.get('catalog_ref') and p['catalog_ref'] not in records:raise ValueError('Unresolved sourcing catalogue reference: '+p['id'])
    for a in assemblies.values():
        for line in a['lines']:
            if line['ref'] not in parts and line['ref'] not in assemblies:raise ValueError('Unresolved BOM line: '+line['ref'])
            q=line.get('quantity')
            if q is not None and (isinstance(q,bool) or not isinstance(q,(float,int)) or q<=0):raise ValueError('Invalid BOM quantity: '+a['id'])
    done=set()
    def visit(id,active):
        if id in active:raise ValueError('Cyclic assembly: '+id)
        if id in done:return
        for line in assemblies[id]['lines']:
            if line['ref'] in assemblies:visit(line['ref'],active|{id})
        done.add(id)
    for id in assemblies:visit(id,set())
    for p in docs['data/product-boms.json']['products']+docs['data/product-boms.json']['offers']:
        if p['catalog_ref'] not in records:raise ValueError('Unresolved product/offer link')
        for id in p.get('assembly_refs',[])+([p['assembly_ref']] if p.get('assembly_ref') else []):
            if id not in assemblies:raise ValueError('Unresolved assembly link: '+id)
    events=unique(docs['data/events.json']['events'],'events');phases=unique(docs['data/timeline-structure.json']['phases'],'phases');event_refs=[]
    contracts=docs['data/contracts.json']
    for e in events.values():
        if e.get('agreement_ref') and e['agreement_ref'] not in contracts:raise ValueError('Unresolved agreement: '+e['id'])
    for p in phases.values():event_refs.extend(p['event_refs'])
    if len(event_refs)!=len(set(event_refs)) or set(event_refs)!=set(events):raise ValueError('Every event must belong to exactly one phase')
    return len(docs)

if __name__=='__main__':print('PASS:',validate_collections(),'authoritative collections; schemas, IDs, references and acyclic BOMs')

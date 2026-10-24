"""Validate collection schemas, identities, references and assembly integrity without writing."""
import json,re,sys
from pathlib import Path
import jsonschema
from data_store import ROOT,registry,read_document,assembly_records,computer_records
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
    parts=unique(docs['data/components.json']['components'],'components');assemblies=unique(assembly_records(docs['data/assemblies.json']['assemblies'],docs['data/devices.json']['devices']),'assemblies')
    aliases=reg.get('component_id_aliases',{})
    if not set(aliases.values())<=set(records)|set(reg.get('record_family_aliases',{})):raise ValueError('Unresolved component alias target')
    device_aliases=reg.get('device_assembly_aliases',{})
    if not set(device_aliases.values())<=assemblies.keys():raise ValueError('Unresolved device BOM alias target')
    if any(r['id'].startswith('device.') for r in docs['data/assemblies.json']['assemblies']):raise ValueError('Device BOM must be owned by data/devices.json')
    aliases={**aliases,**device_aliases,**reg.get('record_id_aliases',{})}
    if not set(reg.get('record_id_aliases',{}).values())<=records.keys():raise ValueError('Unresolved migrated record alias')
    for family,targets in {**reg.get('device_family_aliases',{}),**reg.get('record_family_aliases',{})}.items():
        if family in records or not targets or len(targets)!=len(set(targets)) or not set(targets)<=records.keys():raise ValueError('Invalid device family aliases')
    def reject_retired(v):
        if isinstance(v,str):
            if v in aliases or v in reg.get('device_family_aliases',{}) or v in reg.get('record_family_aliases',{}) or any(x in aliases for x in v.split('|')):raise ValueError('Retired component ID in source: '+v)
        elif isinstance(v,list):
            for x in v:reject_retired(x)
        elif isinstance(v,dict):
            for k,x in v.items():reject_retired(k);reject_retired(x)
    for doc in docs.values():reject_retired(doc)
    for p in parts.values():
        for aid in p.get('bom_assembly_refs',[]):
            if aid not in assemblies:raise ValueError('Unresolved component assembly: '+aid)
        if p['bom_role']=='assembly' and not p.get('bom_assembly_refs'):raise ValueError('Assembly component has no assembly: '+p['id'])
    for a in assemblies.values():
        for line in a['lines']:
            if line['ref'] in parts and parts[line['ref']]['bom_role']!='material':raise ValueError('BOM leaf must be a material; reference the assembly for composed parts: '+line['ref'])
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
    from device_configuration import validate_devices,configuration
    device_map={d['id']:d for d in tech['devices']}
    validate_devices(device_map,assemblies,records)
    for aid in assemblies:
        fit=configuration(aid,assemblies,device_map)
        if fit['status']=='invalid':raise ValueError('Invalid socket population: '+aid+' '+str(fit['issues']))
    unique([{'id':p['catalog_ref']} for p in docs['data/product-boms.json']['products']],'product BOM mappings')
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

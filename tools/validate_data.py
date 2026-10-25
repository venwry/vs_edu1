"""Validate collection schemas, identities, references and assembly integrity without writing."""
import json,re,sys
from pathlib import Path
import jsonschema
from data_store import ROOT,registry,read_document,computer_records,project_collections
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
    device_owners={d['id']:d for d in docs['data/devices.json']['devices']}
    for alias,target in reg.get('platform_device_aliases',{}).items():
        if target not in device_owners or device_owners[target]['category']!='base_computer' or alias!=target.replace('device.base_computer.','computer.'):
            raise ValueError('Invalid platform compatibility owner: '+alias)
    source_docs=docs
    docs=project_collections(docs)
    from validate_products import validate_products
    validate_products(source_docs,docs)
    # Use the provided documents, including staged edits, for all relationship checks.
    recipe=reg['views']['logix-aion-technical-catalog-v2']
    tech={k:docs[v['file']][v['key']] for k,v in recipe.items() if k!='product_catalog'}
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
    parts=unique(docs['data/components.json']['components'],'components')
    aliases=reg.get('component_id_aliases',{})
    if not set(aliases.values())<=set(records)|set(reg.get('record_family_aliases',{})):raise ValueError('Unresolved component alias target')
    device_aliases=reg.get('device_assembly_aliases',{})
    if not set(device_aliases.values())<=set(records):raise ValueError('Unresolved device BOM alias target')
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
        if p['bom_role'] not in ['material','assembly','specification']:raise ValueError('Invalid component role')
    from device_configuration import validate_devices
    device_map={d['id']:d for d in tech['devices']}
    validate_devices(device_map,{},records)
    owners={o['id']:o for o in source_docs['data/devices.json']['devices']+source_docs['data/software-editions.json']['software_editions']+source_docs['data/product-catalog.json']['products']}
    for alias,target in reg.get('composition_aliases',{}).items():
        owner=owners.get(target['ref'])
        if not owner or not any(h['version_number']==target['version_number'] for h in owner['composition_history']):raise ValueError('Invalid composition alias: '+alias)
    if source_docs['data/assemblies.json']['assemblies']:raise ValueError('Active assembly definitions are retired; edit composition histories')
    events=unique(docs['data/events.json']['events'],'events');phases=unique(docs['data/timeline-structure.json']['phases'],'phases');event_refs=[]
    contracts=docs['data/contracts.json']
    for e in events.values():
        if e.get('agreement_ref') and e['agreement_ref'] not in contracts:raise ValueError('Unresolved agreement: '+e['id'])
    for p in phases.values():event_refs.extend(p['event_refs'])
    if len(event_refs)!=len(set(event_refs)) or set(event_refs)!=set(events):raise ValueError('Every event must belong to exactly one phase')
    return len(source_docs)

if __name__=='__main__':print('PASS:',validate_collections(),'authoritative collections; schemas, IDs, references and acyclic BOMs')

"""Commercial connection validation against the actual device socket owners."""
from collections import defaultdict

def validate_products(source, projected):
    products=source['data/product-catalog.json']['products'];devices={d['id']:d for d in source['data/devices.json']['devices']}
    by={p['id']:p for p in products}
    if len(by)!=len(products):raise ValueError('Duplicate commercial product identity')
    for p in products:
        for version in [p,*p.get('revisions',[])]:
            main=version.get('main_product');connections=version.get('connected_devices',[])
            if not main:
                if p['computer_line'] is not None:raise ValueError('Computer line requires an included chassis: '+p['id'])
                continue
            chassis=devices[main['device_ref']]
            expected=next((name for name in ['Aurelia','Artemis','Athena'] if name.lower() in chassis['id']),None)
            if p['computer_line'] is not None and p['computer_line']!=expected:raise ValueError('Wrong computer line: '+p['id'])
            occupants=defaultdict(int);types=defaultdict(set);quantities=defaultdict(int)
            installed={e['device_ref'] for e in connections}
            software=set()
            for e in connections:
                d=devices[e['device_ref']];software.update(d.get('software_refs',[]))
                if d.get('selectable') is False:raise ValueError('Fixed device supplied as an attachment')
                target=e.get('connected_to',chassis['id'])
                if target!=chassis['id'] and target not in installed:raise ValueError('Connection provider not installed')
                slots={s['id']:s for g in devices[target].get('expansion_socket_groups',[]) for s in g['sockets']}
                sid=e['used_socket']
                if sid is None:
                    if e.get('qualification_status')!='connection_not_specified':raise ValueError('Unqualified connection must be explicit')
                    continue
                if sid not in slots or e['device_ref'] not in slots[sid]['compatible_device_refs']:raise ValueError('Device not allowed at socket: '+p['id']+' '+e['device_ref'])
                slot=slots[sid];q=e['quantity']
                if q is None:continue
                occupants[target,sid]+=q;quantities[target,sid,e['device_ref']]+=q
                if slot['capacity'] is not None and occupants[target,sid]>slot['capacity']:raise ValueError('Socket over capacity: '+p['id'])
                limit=slot.get('device_quantity_limits',{}).get(e['device_ref'])
                if limit is not None and quantities[target,sid,e['device_ref']]>limit:raise ValueError('Device limit exceeded')
                if slot.get('installation_multiple') and q%slot['installation_multiple']:raise ValueError('Unmatched RAM population')
                if d['category']=='memory_expansion':types[target,sid].add(e['device_ref'])
            if not chassis.get('memory_constraints',{}).get('mixed_module_types_allowed',False) and any(len(v)>1 for v in types.values()):raise ValueError('Mixed memory module types')
            if software & {e.get('software_ref') for e in p.get('attached_products',[])}:raise ValueError('Cartridge software duplicated in product: '+p['id'])
    # Derived commercial products have no second persisted hardware-population list.
    for p in products:
        if any(k in p for k in ['included_devices','included_software','computer_configuration','bom_assembly_definition']):raise ValueError('Duplicate commercial composition')
    known=set(by)|set(devices)
    for doc in source.values():
        for rows in doc.values():
            if isinstance(rows,list):known.update(r['id'] for r in rows if isinstance(r,dict) and 'id' in r)
    graph={}
    for p in products:
        refs=[e.get('product_ref') or e.get('software_ref') or e.get('service_ref') for e in p.get('attached_products',[])]
        if p.get('base_bundle_ref'):refs.append(p['base_bundle_ref'])
        if any(r not in known for r in refs):raise ValueError('Unresolved attached product: '+p['id'])
        graph[p['id']]=[r for r in refs if r in by]
    visited=set()
    def visit(id,path):
        if id in path:raise ValueError('Cyclic commercial package: '+id)
        if id in visited:return
        for ref in graph[id]:visit(ref,path|{id})
        visited.add(id)
    for id in graph:visit(id,set())

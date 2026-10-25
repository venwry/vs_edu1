"""Validate versioned source composition and commercial socket populations.
Temporal child feasibility is reported by simulate_compositions.py until cutover.
"""
from collections import defaultdict
from datetime import date

def validate_products(source, projected):
    products=source['data/product-catalog.json']['products']
    devices={d['id']:d for d in source['data/devices.json']['devices']}
    product_ids={p['id'] for p in products}
    known=set()
    for doc in source.values():
        for rows in doc.values():
            if isinstance(rows,list):known.update(r['id'] for r in rows if isinstance(r,dict) and 'id' in r)
    graph=defaultdict(set)
    for owner in [*devices.values(),*products]:
        versions=owner['composition_history'];numbers=[];previous=None
        if any(k in owner for k in ['bom_assembly_definition','main_product','connected_devices','attached_products','base_bundle_ref']):raise ValueError('Duplicate legacy composition: '+owner['id'])
        for version in versions:
            n=version['version_number'];numbers.append(n)
            start=version['valid_from'];end=version['valid_to'];date.fromisoformat(end)
            if start is not None:
                date.fromisoformat(start)
                if start>=end:raise ValueError('Invalid composition interval')
                if previous and start<previous:raise ValueError('Overlapping composition intervals')
            elif version.get('date_status')!='unknown':raise ValueError('Unknown start date must be explicit')
            previous=end
            refs=set()
            for line in version['composition_definition']:
                ref=line['ref']
                if ref in refs:raise ValueError('Duplicate composition ref: '+ref)
                refs.add(ref)
                if ref not in known:raise ValueError('Unresolved composition reference: '+ref)
                if ref in product_ids:raise ValueError('Product nesting is forbidden: '+ref)
                if (line['quantity'] is None)!=(line['quantity_status']=='unresolved'):raise ValueError('Quantity status mismatch')
                if owner['id'] in devices:
                    if not ref.startswith(('part.','device.')):raise ValueError('Nonphysical device constituent')
                    if ref in devices:graph[owner['id']].add(ref)
                elif line.get('element_type') not in ['main_product','connected_device','attached_product']:raise ValueError('Missing commercial element type')
            if owner['id'] in product_ids:validate_connections(owner,version,devices)
        if numbers!=sorted(set(numbers)):raise ValueError('Version numbers must be unique and increasing')
    done=set()
    def visit(ref,path):
        if ref in path:raise ValueError('Cyclic device composition: '+ref)
        if ref in done:return
        for child in graph[ref]:visit(child,path|{ref})
        done.add(ref)
    for ref in list(graph):visit(ref,set())

def validate_connections(product,version,devices):
    lines=version['composition_definition'];mains=[x for x in lines if x['element_type']=='main_product']
    if product['computer_line'] is not None:
        if len(mains)!=1 or mains[0]['quantity']!=1:raise ValueError('Computer selector product requires one main product')
        expected=next((n for n in ['Aurelia','Artemis','Athena'] if n.lower() in mains[0]['ref']),None)
        if expected!=product['computer_line']:raise ValueError('Wrong computer line')
    installed={x['ref']:x for x in lines if x['ref'] in devices}
    supplied_software={s for ref in installed for s in devices[ref].get('software_refs',[])}
    if supplied_software & {x['ref'] for x in lines if x['element_type']=='attached_product'}:raise ValueError('Cartridge software duplicated')
    used=defaultdict(int);types=defaultdict(set)
    for line in lines:
        if line['element_type']!='connected_device':continue
        device=devices[line['ref']]
        if device.get('selectable') is False:raise ValueError('Fixed device supplied as an attachment')
        placements=line.get('placements',[line])
        if 'placements' in line and sum(x['quantity'] for x in placements)!=line['quantity']:raise ValueError('Placement quantity mismatch')
        for e in placements:
            target=e.get('connected_to') or (mains[0]['ref'] if len(mains)==1 else None)
            # Standalone expansion/upgrade kits need not contain their host.
            if not target:
                if product['computer_line'] is not None:raise ValueError('Missing connection provider')
                continue
            if target not in installed:raise ValueError('Connection provider not installed: '+target)
            slots={s['id']:s for g in devices[target].get('expansion_socket_groups',[]) for s in g['sockets']}
            sid=e.get('used_socket',line.get('used_socket'))
            if sid is None and line.get('qualification_status')=='connection_not_specified':continue
            if sid not in slots or line['ref'] not in slots[sid]['compatible_device_refs']:raise ValueError('Device not allowed at socket: '+product['id']+' '+line['ref'])
            slot=slots[sid];q=e['quantity'];count=installed[target]['quantity']
            if q is None or count is None:continue
            used[target,sid]+=q
            if slot['capacity'] is not None and used[target,sid]>slot['capacity']*count:raise ValueError('Socket over capacity')
            limit=slot.get('device_quantity_limits',{}).get(line['ref'])
            if limit is not None and q>limit*count:raise ValueError('Device limit exceeded')
            if slot.get('installation_multiple') and q%(slot['installation_multiple']*count):raise ValueError('Unmatched RAM population')
            if device['category']=='memory_expansion':types[target,sid].add(line['ref'])
    for (target,sid),kinds in types.items():
        if len(kinds)>1 and not devices[target].get('memory_constraints',{}).get('mixed_module_types_allowed',False):raise ValueError('Mixed memory module types')

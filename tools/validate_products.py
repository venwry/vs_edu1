"""Validate versioned source composition and commercial socket populations.
Temporal child feasibility uses the shared composition resolver.
"""
from collections import defaultdict
from datetime import date

def validate_products(source, projected):
    products=source['data/product-catalog.json']['products']
    devices={d['id']:d for d in source['data/devices.json']['devices']}
    editions={e['id']:e for e in source['data/software-editions.json']['software_editions']}
    physical={**devices,**editions}
    groups={}
    for e in editions.values():
        key=e['software_line_id'];value=(e['software_line_name'],e['software_line_category'])
        if key in groups and groups[key]!=value:raise ValueError('Inconsistent software line metadata: '+key)
        groups[key]=value
        if any(k in e for k in ['product_ref','delivery','sold_separately','physical_media_refs']):raise ValueError('Duplicate legacy software ownership')
    product_ids={p['id'] for p in products}
    known=set()
    for doc in source.values():
        for rows in doc.values():
            if isinstance(rows,list):known.update(r['id'] for r in rows if isinstance(r,dict) and 'id' in r)
    owners={x['id']:x for x in [*devices.values(),*products]}
    for assembly in source['data/assemblies.json']['assemblies']:
        if 'metadata_owner_ref' not in assembly:continue
        owner=owners.get(assembly['metadata_owner_ref'])
        version=next((h for h in owner['composition_history'] if h['version_number']==assembly['metadata_version_number']),None) if owner else None
        if not version or version.get('legacy_assembly_ref')!=assembly['id'] or not version.get('bom_assembly_metadata'):raise ValueError('Invalid assembly metadata owner/version')
        if any(k in assembly for k in ['requirements','routing','cost_rollup_status']):raise ValueError('Duplicate assembly manufacturing metadata')
    graph=defaultdict(set)
    for owner in [*physical.values(),*products]:
        versions=owner['composition_history'];numbers=[];previous=None
        if any(k in owner for k in ['bom_assembly_definition','main_product','connected_devices','attached_products','base_bundle_ref']):raise ValueError('Duplicate legacy composition: '+owner['id'])
        for version in versions:
            if (owner['id'] in devices or version.get('legacy_assembly_ref')) and not version.get('bom_assembly_metadata'):raise ValueError('Missing version manufacturing metadata: '+owner['id'])
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
                if owner['id'] in physical:
                    if not ref.startswith('part.') and ref not in physical:raise ValueError('Nonphysical composition constituent')
                    if ref in physical:graph[owner['id']].add(ref)
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
    from compositions import resolve_many
    requests=[{'ref':o['id'],'selection':{'version':h['version_number']}} for o in [*physical.values(),*products] for h in o['composition_history']]
    for result in resolve_many(requests,documents=source):
        if result['issues']:raise ValueError('Invalid temporal composition: '+str(result['issues']))
        if devices.get(result['ref'],{}).get('category')=='base_computer':
            removable={'memory_expansion','rom_cartridge','video_expansion_card','network_interface_card','floppy_drive_mechanism','hard_disk_drive','keyboard','monitor'}
            if any(devices.get(n['ref'],{}).get('category') in removable for n in result['nodes'][1:]):raise ValueError('Removable device included in bare base computer')


def validate_connections(product,version,devices):
    lines=version['composition_definition'];mains=[x for x in lines if x['element_type']=='main_product']
    if product['category']=='computer_system':
        if not product['id'].startswith('product.') or sum(x['quantity'] or 0 for x in mains)<2:raise ValueError('Computer system requires a product ID and multiple computers')
        if any(devices[x['ref']]['category']!='base_computer' for x in mains):raise ValueError('Computer system main products must be base computers')
    if product['computer_line'] is not None:
        if len(mains)!=1 or mains[0]['quantity']!=1:raise ValueError('Computer selector product requires one main product')
        expected=next((n for n in ['Aurelia','Artemis','Athena'] if n.lower() in mains[0]['ref']),None)
        if expected!=product['computer_line']:raise ValueError('Wrong computer line')
    installed={x['ref']:x for x in lines if x['ref'] in devices}
    supplied_software=set()
    def software_in(ref,seen):
        if ref in seen:return
        if ref not in devices:
            if ref.startswith(('software.','edition.')):supplied_software.add(ref)
            return
        for h in devices[ref]['composition_history']:
            for l in h['composition_definition']:software_in(l['ref'],seen|{ref})
    for ref in installed:software_in(ref,set())
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

"""Resolve fitted devices from the single BOM graph and validate socket occupancy."""
from collections import defaultdict

def configuration(assembly_ref, assemblies, devices):
    """No saved attachment list: quantity/path comes exclusively from BOM lines."""
    fitted=[]
    def walk(ref,quantity,path,inside_chassis=False):
        d=devices.get(ref)
        if d:
            fitted.append({'ref':ref,'quantity':quantity,'path':path,'fixed':inside_chassis})
            inside_chassis=inside_chassis or d['category']=='base_computer'
        a=assemblies.get(ref)
        if not a:return
        if ref in path:raise ValueError('Cyclic configuration: '+ref)
        for l in a['lines']:
            q=None if quantity is None or l['quantity'] is None else quantity*l['quantity']
            walk(l['ref'],q,path+[ref],inside_chassis)
    walk(assembly_ref,1,[])
    chassis=[r for r in fitted if devices[r['ref']]['category']=='base_computer']
    if len(chassis)!=1:return {'fitted':fitted,'assignments':[],'issues':[], 'status':'not_single_chassis'}
    ch=devices[chassis[0]['ref']];sockets={s['id']:s for g in ch['expansion_socket_groups'] for s in g['sockets']}
    occupied=defaultdict(int);assignments=[];issues=[];modules=defaultdict(int);device_counts=defaultdict(int);ram_kib=0
    # Video providers supply their own display outputs. Fixed integrated video uses chassis video_out.
    for row in fitted:
        d=devices[row['ref']]
        if not row['fixed'] and d['category']!='base_computer':
            for g in d.get('expansion_socket_groups',[]):
                for s in g['sockets']:
                    sid=d['id']+':'+s['id'];capacity=None if s['capacity'] is None or row['quantity'] is None else s['capacity']*row['quantity']
                    sockets[sid]={**s,'capacity':capacity}
    for row in fitted:
        d=devices[row['ref']]
        if (d.get('virtual') and d['category']=='memory_assembly') or d['category']=='memory_expansion':ram_kib+=(d.get('specification',{}).get('capacity_kb',d.get('capacity_kb',0)))*(row['quantity'] or 0)
        if row['fixed'] or d['category']=='base_computer':continue
        matches=[id for id,s in sockets.items() if d['id'] in s['compatible_device_refs']]
        if not matches:
            connections={'memory_expansion':['memory_module','expansion_card'],'rom_cartridge':['rom_cartridge'],'network_interface_card':['expansion_card'],'video_expansion_card':['dedicated_video','expansion_card'],'monitor':['video'],'hard_disk_drive':['internal_storage'],'floppy_drive_mechanism':['internal_storage']}.get(d['category'],[])
            known=any(s['connection'] in connections for s in sockets.values()) or d['category']=='rom_cartridge' and not ch['configuration_requirements']['external_application_cartridges_supported']
            issues.append({'ref':d['id'],'kind':'incompatible_device' if known else 'unresolved_connection','message':'No documented compatible socket for this fitted device.'});continue
        sid=next((id for id in matches if sockets[id]['capacity'] is None or occupied[id]+(row['quantity'] or 0)<=sockets[id]['capacity']),matches[0]);slot=sockets[sid]
        assignments.append({**row,'socket_ref':sid})
        if row['quantity'] is None:issues.append({'ref':d['id'],'kind':'unknown_quantity'});continue
        occupied[sid]+=row['quantity'];device_counts[(sid,d['id'])]+=row['quantity']
        limit=slot.get('device_quantity_limits',{}).get(d['id'])
        if limit is not None and device_counts[(sid,d['id'])]>limit:issues.append({'ref':d['id'],'kind':'capacity_exceeded'})
        if slot['capacity'] is None:issues.append({'ref':sid,'kind':'unknown_capacity'})
        elif occupied[sid]>slot['capacity']:issues.append({'ref':sid,'kind':'capacity_exceeded'})
        if slot.get('installation_multiple'):modules[(sid,d['id'])]+=row['quantity']
    for (sid,id),qty in modules.items():
        if qty%sockets[sid]['installation_multiple']:issues.append({'ref':id,'kind':'unmatched_memory_modules'})
    limits=ch['memory_constraints']
    if limits['max_ram_kib'] is not None and ram_kib>limits['max_ram_kib']:issues.append({'ref':ch['id'],'kind':'capacity_exceeded'})
    if not limits['mixed_module_types_allowed'] and len({id for sid,id in modules})>1:issues.append({'ref':ch['id'],'kind':'mixed_memory_types'})
    return {'fitted':fitted,'assignments':assignments,'issues':issues,'status':'invalid' if any(i['kind'] in ['capacity_exceeded','unmatched_memory_modules','mixed_memory_types','incompatible_device'] for i in issues) else 'qualification_pending' if issues else 'documented_fit'}

def validate_devices(devices,assemblies,records):
    for d in devices.values():
        groups=d.get('expansion_socket_groups',[]);ids=[s['id'] for g in groups for s in g['sockets']]
        if len(ids)!=len(set(ids)):raise ValueError('Duplicate physical socket: '+d['id'])
        if len({g['id'] for g in groups})!=len(groups):raise ValueError('Duplicate socket group: '+d['id'])
        for g in groups:
            for s in g['sockets']:
                if not set(s['compatible_device_refs'])<=devices.keys():raise ValueError('Socket compatibility must reference devices')
                if any(devices[r].get('virtual') or devices[r].get('selectable') is False for r in s['compatible_device_refs']):raise ValueError('Fixed subsystem offered in socket')
        if d.get('virtual') and d.get('selectable') is not False:raise ValueError('Virtual subsystem cannot be selectable')
        for id in d.get('software_refs',[]):
            if id not in records or not records[id].get('product_ref'):raise ValueError('Media must reference a software edition')
        if d['category']=='base_computer':
            if records.get(d['processor']['part_ref'],{}).get('category')!='processor_ic':raise ValueError('Chassis CPU must reference a processor component')
            for row in configuration(d['id'],assemblies,devices)['fitted']:
                r=devices[row['ref']]
                if r['category'] in ['memory_expansion','rom_cartridge','video_expansion_card','network_interface_card','floppy_drive_mechanism','hard_disk_drive','keyboard','monitor']:raise ValueError('Removable device included in bare chassis: '+r['id'])

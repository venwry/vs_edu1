"""Read the single authoritative collection layer; legacy shapes exist only in memory."""
import copy, json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def registry(root=ROOT):
    return json.loads((Path(root)/'schemas/data-registry.json').read_text())

def view_name(path, root=ROOT):
    reg=registry(root); path=str(path).removeprefix('./')
    path=reg['legacy_paths'].get(path,path)
    name=Path(path).stem
    return name if (path.startswith('generated/catalogs/') or path.startswith('catalog:')) and name in reg['views'] else (path[8:] if path.startswith('catalog:') and path[8:] in reg['views'] else None)

def normalize_component_ids(value, root=ROOT):
    """Translate archival IDs and composite map keys in memory; preserve all numbers."""
    reg=registry(root);aliases={**reg.get('component_id_aliases',{}),**reg.get('device_assembly_aliases',{}),**reg.get('record_id_aliases',{})}
    families=reg.get('device_family_aliases',{})
    def translate(v):
        if isinstance(v,str):
            if v in aliases:return aliases[v]
            return '|'.join(aliases.get(p,p) for p in v.split('|')) if '|' in v else v
        if isinstance(v,list):return [translate(x) for x in v]
        if isinstance(v,dict):
            out={}
            for k,x in v.items():
                key=translate(k)
                if key in out:raise ValueError('Component identifier collision: '+key)
                out[key]=translate(x)
            if out.get('catalog_ref') in reg.get('record_family_aliases',{}):out['historical_variant_refs']=reg['record_family_aliases'][out['catalog_ref']]
            if out.get('catalog_ref') in families and out.get('id') in families[out['catalog_ref']]:out['catalog_ref']=out['id']
            return out
        return v
    return translate(value)

def assembly_records(stored, devices):
    """Build the runtime BOM index from its sole source owners; never persist copies."""
    rows=copy.deepcopy(stored)
    rows.extend({'id':d['id'],**copy.deepcopy(d['bom_assembly_metadata']),'lines':copy.deepcopy(d['bom_assembly_definition'])} for d in devices if 'bom_assembly_definition' in d)
    if len({r['id'] for r in rows})!=len(rows):raise ValueError('Duplicate device/assembly BOM identity')
    return rows

def computer_records(stored, devices, components):
    devices={d['id']:d for d in devices};components={p['id']:p for p in components};rows=copy.deepcopy(stored)
    for c in rows:
        chassis=devices[c['chassis_ref']]
        for key in ['processor','form_factor','io_and_expansion']:c[key]=copy.deepcopy(chassis[key])
        cpu=components[c['processor']['part_ref']];c['processor']['variant']=cpu['name'];c['processor']['clock_mhz']=cpu['specification']['clock_mhz']
        slots={s['id']:s for g in chassis['expansion_socket_groups'] for s in g['sockets']};io=c['io_and_expansion']
        if 'flexibus' in slots:io['flexibus_ports']=slots['flexibus']['capacity']
        if 'expansion_slots' in io:io['expansion_slots']['count']=slots['expansion']['capacity']
        else:io['general_expansion_slot_count']=slots['expansion']['capacity']
        if 'dedicated_video_slot' in io:io['dedicated_video_slot']['count']=slots['video_card']['capacity']
        elif 'video_card' in slots:io['graphics_card_count']=slots['video_card']['capacity']
        if 'rom_and_cartridges' in c:c['rom_and_cartridges']={'xip_slots':sum(s['capacity'] for s in slots.values() if s['connection']=='rom_cartridge'),**c['rom_and_cartridges']}
        if 'rom_eeprom_cartridge_slots' in io:io['rom_eeprom_cartridge_slots']['count']=sum(s['capacity'] for s in slots.values() if s['connection']=='rom_cartridge')
        if 'ram' in slots:
            ram=slots['ram'];mem=c['memory'];mem['ram_sockets']=ram['capacity'];mem['modules_per_bank']=ram['installation_multiple']
            if ram['capacity'] is not None:
                mem['bank_count']=ram['capacity']//ram['installation_multiple'];mem['physical_capacity_limit_kb']=chassis['memory_constraints']['max_ram_kib'];mem['capacity_limit_status']=chassis['memory_constraints']['qualification_status'];mem['mixed_density_allowed']=chassis['memory_constraints']['mixed_module_types_allowed']
            else:mem['maximum_ram_kb']=chassis['memory_constraints']['max_ram_kib']
        slot=c['io_and_expansion'].get('dedicated_video_slot',{})
        if c.get('default_video_card_ref'):slot['included_card_ref']=c['default_video_card_ref']
        if c.get('configuration_video_card_refs'):slot['configuration_card_refs']=c['configuration_video_card_refs']
    return rows

def project_collections(docs):
    result=subprocess.run(['node',str(ROOT/'data-store.js')],input=json.dumps(docs),text=True,capture_output=True)
    if result.returncode:raise ValueError('Invalid catalogue projection: '+result.stderr[-1800:])
    return json.loads(result.stdout)

def read_document(path, root=ROOT):
    root=Path(root);reg=registry(root);name=view_name(path,root)
    if name is None:
        actual=reg['legacy_paths'].get(str(path),str(path))
        value=json.loads((root/actual).read_text())
        return normalize_component_ids(value,root) if actual.startswith('generated/models/') else value
    cache={}
    if reg.get("commercial_projection_files"):
        source={f:json.loads((root/f).read_text()) for f in reg["commercial_projection_files"]}
        cache=project_collections(source)
    def collection(file):
        if file not in cache:cache[file]=json.loads((root/file).read_text())
        return cache[file]
    def select(ref):
        rows=collection(ref['file'])[ref['key']]
        if ref.get('wrap'):return {'products':copy.deepcopy(rows)}
        if ref.get('chassis_file'):return computer_records(rows,collection(ref['chassis_file'])['devices'],collection('data/components.json')['components'])
        return assembly_records(rows,collection(ref['device_file'])['devices']) if ref.get('device_file') else copy.deepcopy(rows)
    recipe=reg['views'][name]
    if recipe.get('story'):
        world=collection('data/world.json');structure=collection('data/timeline-structure.json')
        events={e['id']:e for e in collection('data/events.json')['events']};contracts=collection('data/contracts.json')
        phases=[]
        for phase in structure['phases']:
            p=copy.deepcopy(phase);ids=p.pop('event_refs');p['events']=[]
            for id in ids:
                e=copy.deepcopy(events[id]);contract=e.pop('agreement_ref',None)
                if contract is not None:e['agreement_terms']=copy.deepcopy(contracts[contract])
                p['events'].append(e)
            phases.append(p)
        return {'assumptions':{k:copy.deepcopy(world[k]) for k in ['scenario','entities','principles','conventions']},'phases':phases,'processes':copy.deepcopy(structure['processes'])}
    if 'merge' in recipe:
        result={}
        for ref in recipe['merge']:
            part=select(ref)
            if result.keys() & part.keys():raise ValueError('Overlapping field ownership: '+name)
            result.update(part)
        return result
    return {key:select(ref) for key,ref in recipe.items()}

def document_text(path, root=ROOT):
    if view_name(path,root):return json.dumps(read_document(path,root),indent=2,ensure_ascii=False)+'\n'
    return (Path(root)/registry(root)['legacy_paths'].get(str(path),str(path))).read_text()

def document_bytes(path, root=ROOT):
    if view_name(path,root):return document_text(path,root).encode()
    return (Path(root)/registry(root)['legacy_paths'].get(str(path),str(path))).read_bytes()

def store_document(path, value, root=ROOT):
    """Write edits back to their sole collection owners; no catalogue is materialised."""
    root=Path(root);reg=registry(root);name=view_name(path,root)
    if name is None:
        actual=reg['legacy_paths'].get(str(path),str(path))
        if actual in reg['files']:
            from validate_data import validate_collections
            validate_collections(root,{actual:value})
        target=root/actual;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n');return
    current=read_document(path,root)
    if current==value:return
    # Derived commercial/technical views are read-only except device-owned BOM edits.
    if name in ['logix-aion-technical-catalog-v2','hardware-bom','retail-catalog-1982']:
        if name=='logix-aion-technical-catalog-v2':
            edited=[k for k in current if current[k]!=value.get(k)]
            allowed=['components','services','external_partner_products']
            if not edited or any(k not in allowed for k in edited):raise ValueError('Edit the authoritative product, device or technology record')
            changes={}
            for k in edited:
                ref=reg['views'][name][k];file=ref['file']
                if file not in changes:changes[file]=json.loads((root/file).read_text())
                changes[file][ref['key']]=copy.deepcopy(value[k])
            from validate_data import validate_collections
            validate_collections(root,changes)
            for file,payload in changes.items():(root/file).write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
            return
        if name!='hardware-bom':raise ValueError('Edit the authoritative product, device or technology record')
        if any(value.get(k)!=v for k,v in current.items() if k!='assemblies'):raise ValueError('Edit authoritative BOM metadata at its owner')
        before={a['id']:a for a in current['assemblies']};after={a['id']:a for a in value['assemblies']}
        if before.keys()!=after.keys():raise ValueError('Add/remove BOM owners in authoritative collections')
        devices=json.loads((root/'data/devices.json').read_text());by={d['id']:d for d in devices['devices']}
        for id,a in after.items():
            if a==before[id]:continue
            if id not in by:raise ValueError('Edit commercial attachments or stored assembly at its source owner')

            if len(by[id]['composition_history'])!=1:raise ValueError('Edit the explicit composition version at its source owner')
            by[id]['composition_history'][0]['composition_definition']=copy.deepcopy(a['lines'])
            by[id]['composition_history'][0]['bom_assembly_metadata']={k:copy.deepcopy(v) for k,v in a.items() if k not in ['id','lines']}
        from validate_data import validate_collections
        validate_collections(root,{'data/devices.json':devices})
        (root/'data/devices.json').write_text(json.dumps(devices,indent=2,ensure_ascii=False)+'\n')
        return
    changes={}
    def assign(ref,payload):
        file=ref['file']
        if file not in changes:changes[file]=json.loads((root/file).read_text())
        if ref.get('device_file'):
            device_file=ref['device_file']
            if device_file not in changes:changes[device_file]=json.loads((root/device_file).read_text())
            devices={d['id']:d for d in changes[device_file]['devices'] if d.get('composition_history')}
            owned=[r for r in payload if r['id'] in devices]
            if len(owned)!=len(devices) or {r['id'] for r in owned}!=set(devices):raise ValueError('Device BOMs must be edited at their existing owners')
            for row in owned:
                device=devices[row['id']]
                if len(device['composition_history'])!=1:raise ValueError('Edit the explicit composition version at its source owner')
                device['composition_history'][0]['composition_definition']=copy.deepcopy(row['lines'])
                device['composition_history'][0]['bom_assembly_metadata']=copy.deepcopy({k:v for k,v in row.items() if k not in ['id','lines']})
            payload=[r for r in payload if r['id'] not in devices]
            if any(r['id'].startswith('device.') for r in payload):raise ValueError('Add device BOMs in data/devices.json')
        if ref.get('chassis_file'):
            payload=copy.deepcopy(payload)
            stored={c['id']:c for c in changes[file][ref['key']]}
            for c in payload:
                # Hydrated fields are read-only here; edit the owning chassis instead.
                expected=computer_records([stored[c['id']]],changes.get(ref['chassis_file'],json.loads((root/ref['chassis_file']).read_text()))['devices'],changes.get('data/components.json',json.loads((root/'data/components.json').read_text()))['components'])[0]
                if 'rom_and_cartridges' in c:
                    if c['rom_and_cartridges'].pop('xip_slots',None)!=expected['rom_and_cartridges']['xip_slots']:raise ValueError('Edit cartridge slots on the owning chassis')
                for key in set(expected['memory'])-set(stored[c['id']]['memory']):
                    if c['memory'].pop(key,None)!=expected['memory'][key]:raise ValueError('Edit memory limits on the owning chassis: '+key)
                for key in ['processor','form_factor','io_and_expansion']:
                    if c.pop(key,None)!=expected[key]:raise ValueError('Edit hardware fields on the owning chassis: '+key)
        changes[file][ref['key']]=copy.deepcopy(payload)
    recipe=reg['views'][name]
    if recipe.get('story'):
        world={k:value['assumptions'][k] for k in ['scenario','entities','principles','conventions']}
        for k,v in world.items():assign({'file':'data/world.json','key':k},v)
        phases=[];events=[];contracts=json.loads((root/'data/contracts.json').read_text())
        for phase in value['phases']:
            p=copy.deepcopy(phase);evs=p.pop('events');p['event_refs']=[]
            for event in evs:
                e=copy.deepcopy(event);p['event_refs'].append(e['id'])
                if 'agreement_terms' in e:
                    contracts[e['id']]=e.pop('agreement_terms');e['agreement_ref']=e['id']
                events.append(e)
            phases.append(p)
        changes['data/contracts.json']=contracts
        assign({'file':'data/events.json','key':'events'},events)
        assign({'file':'data/timeline-structure.json','key':'phases'},phases)
        assign({'file':'data/timeline-structure.json','key':'processes'},value['processes'])
    elif 'merge' in recipe:
        remaining=set(value)
        for ref in recipe['merge']:
            existing=json.loads((root/ref['file']).read_text())[ref['key']]
            if not set(existing)<=set(value):raise ValueError('Missing owned fields: '+name)
            assign(ref,{k:value[k] for k in existing});remaining-=set(existing)
        if remaining:raise ValueError('Assign new programme fields to an explicit collection owner: '+str(remaining))
    else:
        if set(value)!=set(recipe):raise ValueError('Unexpected catalogue fields: '+name)
        for k,ref in recipe.items():assign(ref,value[k])
    from validate_data import validate_collections
    validate_collections(root,changes)
    for file,payload in changes.items():(root/file).write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')

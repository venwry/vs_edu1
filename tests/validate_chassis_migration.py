"""Independent physical-equivalence audit against the pre-chassis revision."""
import json,hashlib,sys,copy,tempfile,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from data_store import read_document,registry,store_document
from validate_data import validate_collections
from device_configuration import configuration
f=read_document('tests/fixtures/chassis-migration.json');validate_collections()
t=read_document('catalog:logix-aion-technical-catalog-v2');b=read_document('catalog:hardware-bom');a={r['id']:r for r in b['assemblies']};d={r['id']:r for r in t['devices']};p={r['id']:r for r in t['components']};records={r['id']:r for rows in t.values() if isinstance(rows,list) for r in rows if isinstance(r,dict) and 'id'in r}
inverse={v:k for k,vs in f['processor_families'].items() for v in vs}
def flat(id):
 if id in p:return [[inverse.get(id,id),1]]
 result=[]
 for l in a[id]['lines']:
  rows=flat(l['ref']) if l['ref'] in a else [[inverse.get(l['ref'],l['ref']),1]]
  result.extend([[ref,None if q is None or l['quantity'] is None else q*l['quantity']] for ref,q in rows])
 return sorted(result,key=lambda x:(x[0],str(x[1])))
for old,expected in f['assembly_leaves'].items():
 id=f['aliases'].get(old,old)
 if old=='assembly.part.era1':id='part.erav1_6mhz'
 id=registry().get('record_id_aliases',{}).get(id,id)
 if id in read_document('data/product-catalog.json')['retired_configuration_ids']:
  assert id not in a;continue
 assert flat(id)==expected,old+' physical BOM changed'
for path,h in f['frozen_files'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==h,path
assert not any('variants'in r or r['category']=='memory_module' for r in p.values())
for old in f['components']:
 new=d[f['aliases'][old['id']]];assert new['category']=='memory_expansion';assert new.get('specification')==old['specification']
for old in f['computers']:
 c=records[old['id']];ch=d[c['chassis_ref']];assert ch['category']=='computer_chassis';assert c['processor']['clock_mhz']==old['processor']['clock_mhz']
 assert inverse.get(c['processor']['part_ref'],c['processor']['part_ref'])==old['processor']['part_ref']
 assert c['memory']['ram_kb']>=0
 assert configuration(ch['id'],a,d)['status']=='documented_fit'
for id in a:assert configuration(id,a,d)['status']!='invalid',id
for s in t['platform_editions']:
 for id in s.get('physical_media_refs',[]):assert s['id'] in d[id]['software_refs'] and d[id]['category']=='rom_cartridge'
# Negative socket tests: duplicate sockets, overfilled slots, single unmatched RAM module.
base=copy.deepcopy(a['assembly.computer.artemis.m32_128']);memory=next(l for l in base['lines'] if l['ref']=='device.ram_64kb_x32');memory['quantity']=1
assert configuration(base['id'],{**a,base['id']:base},d)['status']=='invalid'
memory['quantity']=10;assert configuration(base['id'],{**a,base['id']:base},d)['status']=='invalid'
base=copy.deepcopy(a['assembly.computer.artemis.m32_128']);base['lines'].append({'ref':'device.apple2_video_card','quantity':1})
assert configuration(base['id'],{**a,base['id']:base},d)['status']=='invalid'
base=copy.deepcopy(a['assembly.computer.artemis.m32_128']);base['lines'].append({'ref':'device.ram_128kb_x32','quantity':2})
assert configuration(base['id'],{**a,base['id']:base},d)['status']=='invalid'
# Unknown Athena limits never become a qualified capacity or zero sockets.
for id in ['computer.athena','computer.athena_server']:
 c=records[id];ch=d[c['chassis_ref']];assert next(g for g in ch['expansion_socket_groups'] if g['id']=='cartridges')['sockets']==[]
 assert configuration(c['bom_assembly_refs'][0],a,d)['status']=='qualification_pending'
 # Every original functional set survived, including combined mainboard/chassis set.
 old=next(x for x in f['athena_functional_boms'] if x['computer_ref']==id)
 for key,original in zip(['hdd','fdd','bios','mainboard_set','system_rom'],old['functional_components']):
  part=p['part.'+id.split('.')[1]+'.'+key];assert part['name']==original['name'];assert part.get('manufacturer')==original.get('manufacturer');assert part.get('manufacturer_part_number')==original.get('manufacturer_part_number')
# Writes through either logical view preserve source ownership exactly.
with tempfile.TemporaryDirectory() as tmp:
 root=Path(tmp)
 for folder in ['data','schemas']:shutil.copytree(R/folder,root/folder)
 before={p:p.read_bytes() for p in (root/'data').glob('*.json')}
 for view in ['hardware-bom','logix-aion-technical-catalog-v2']:
  store_document('catalog:'+view,read_document('catalog:'+view,root),root)
 assert all(path.read_bytes()==raw for path,raw in before.items()),'Roundtrip changed canonical files'
 bad=read_document('catalog:logix-aion-technical-catalog-v2',root);bad['computers'][0]['processor']['clock_mhz']=99
 try:store_document('catalog:logix-aion-technical-catalog-v2',bad,root)
 except ValueError:pass
 else:raise AssertionError('Hydrated chassis hardware silently overwritten')
 assert all(path.read_bytes()==raw for path,raw in before.items())
print('PASS: old flattened BOMs and archives unchanged; six chassis, processor bins, memory/media ownership, slot constraints and write roundtrips')

# A shared internal-drive pool supports either drive type, without additional bays.
for name,capacity in [('artemis',2),('artemis_pro',3),('athena',2),('athena_server',2)]:
 ch=d['device.chassis.'+name];slots=[s for g in ch['expansion_socket_groups'] for s in g['sockets'] if s['connection']=='internal_storage']
 assert len(slots)==1 and slots[0]['id']=='internal_drive' and slots[0]['capacity']==capacity
 assert {d[r]['category'] for r in slots[0]['compatible_device_refs']}=={'floppy_drive_mechanism','hard_disk_drive'}
 for ref in slots[0]['compatible_device_refs']:
  test={'id':'test','lines':[{'ref':ch['id'],'quantity':1},{'ref':ref,'quantity':capacity}]}
  fit=configuration('test',{**a,'test':test},d);assert fit['status']!='invalid',fit
  test['lines'][1]['quantity']=capacity+1
  assert configuration('test',{**a,'test':test},d)['status']=='invalid'

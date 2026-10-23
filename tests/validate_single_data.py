"""Exercise integrity rejection and source-only writes in an isolated copy."""
import copy,json,shutil,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from data_store import ROOT,read_document,store_document
from validate_data import validate_collections
with tempfile.TemporaryDirectory() as tmp:
 root=Path(tmp)
 for directory in ('data','schemas'):shutil.copytree(ROOT/directory,root/directory)
 original=read_document('catalog:logix-aion-technical-catalog-v2',root)
 changed=copy.deepcopy(original);changed['base_parts'][0]['vendor']='Test supplier'
 store_document('catalog:logix-aion-technical-catalog-v2',changed,root)
 assert read_document('catalog:logix-aion-technical-catalog-v2',root)==changed
 assert not (root/'generated').exists()
 snapshots={p:p.read_bytes() for p in (root/'data').glob('*.json')}
 for kind in ('duplicate','reference','cycle','empty'):
  if kind in ('duplicate','reference'):
   value=copy.deepcopy(changed)
   if kind=='duplicate':value['base_parts'].append(copy.deepcopy(value['base_parts'][0]))
   else:value['platform_editions'][0]['product_ref']='software.missing_reference'
   target='catalog:logix-aion-technical-catalog-v2'
  else:
   target='data/assemblies.json';value=read_document(target,root)
   if kind=='empty':value={}
   else:value['assemblies'][0]['lines'][0]['ref']=value['assemblies'][0]['id']
  try:store_document(target,value,root)
  except (ValueError,KeyError):pass
  else:raise AssertionError('Accepted '+kind)
  assert all(p.read_bytes()==v for p,v in snapshots.items()),'Invalid write changed files'
print('PASS: source-only writes, duplicate IDs, unresolved references, cycles and empty writes rejected before mutation')

from data_paths import read_document, document_bytes, document_text
"""Check first offering use through forward BOM links and dated manufacturing variants."""
import json, collections
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parents[1])
c=read_document('generated/catalogs/logix-aion-technical-catalog-v2.json');b=read_document('generated/catalogs/hardware-bom.json')
records={r['id']:r for v in c.values() if isinstance(v,list) for r in v if isinstance(r,dict) and 'id' in r}
former_base=set(read_document('tests/fixtures/component-migration.json')['former_base_ids'])
assemblies={r['id']:r for r in b['assemblies']};parts={r['id']:r for r in b['components']};first={}
def date(r):return r.get('introduced',{}).get('event_start_date') or r.get('available_from') or ''
from compositions import resolve_many
owners=read_document('data/devices.json')['devices']+read_document('data/software-editions.json')['software_editions']+read_document('data/product-catalog.json')['products']
requests=[{'ref':o['id'],'selection':{'version':h['version_number']}} for o in owners for h in o['composition_history']]
for result in resolve_many(requests):
 d=result['version']['valid_from']
 if not d:continue
 for line in result['leaves']:
  ref=line['ref'];first[ref]=min(first.get(ref,d),d)
errors=[]
for p in b['components']:
 if p['id'] in former_base or p.get('production_status')=='excluded':continue
 expected=first.get(p['id']);actual=p.get('introduced',{}).get('event_start_date')
 # A component's preserved month-precision date may contain a newly precise device first use.
 if expected!=actual and not (isinstance(actual,str) and len(actual)==7 and isinstance(expected,str) and expected.startswith(actual+'-')):errors.append((p['id'],actual,expected))
assert not errors, errors
for p in b['components']:
 if p['id'] not in former_base and p['id'] not in first and p.get('production_status')!='excluded':
  assert p['introduced']=={'event_name':'no release','event_start_date':None},p['id']
for p in c['proposed_bundles']:
 assert p['introduced']['event_start_date'] is not None,p['id']
print('PASS: component first-use dates match forward BOM reachability, including variant effective dates')
print(collections.Counter(first.get(p['id'],'no release') for p in b['components'] if p['id'] not in former_base))

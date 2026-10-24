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
def walk(id,d,seen):
 if id in seen:return
 if id in parts:
  if id not in first or d<first[id]:first[id]=d
  return
 a=assemblies.get(id)
 if not a:return
 d=max(d,a.get('effective_from',''))
 for line in a['lines']:
  ref=line['ref'];p=parts.get(ref,{});r=records.get(ref,{}) if ref in former_base else {}
  walk(ref,max(d,date(r)),seen|{id})
for key in ['computers','devices','platform_editions','offered_bundles','commercial_offerings']:
 for r in c[key]:
  d=date(r)
  if not d:continue
  refs=set(r.get('bom_assembly_refs',[])+r.get('physical_media_refs',[]));
  if r['id'] in assemblies:refs.add(r['id'])
  refs.add(r.get('bom_assembly_ref'))
  for p in b['products']:
   if p['catalog_ref']==r['id']:refs.update(p.get('assembly_refs',[]))
  for p in b['offers']:
   if p['catalog_ref']==r['id']:walk(p.get('assembly_ref'),max(d,p.get('effective_from','')),set())
  for ref in refs:walk(ref,d,set())
  for v in r.get('manufacturing_variants',[]):walk(v['assembly_ref'],max(d,v.get('effective_from','')),set())
errors=[]
for p in b['components']:
 if p['id'] in former_base:continue
 expected=first.get(p['id']);actual=p.get('introduced',{}).get('event_start_date')
 if expected!=actual:errors.append((p['id'],actual,expected))
assert not errors, errors
for p in b['components']:
 if p['id'] not in former_base and p['id'] not in first:
  assert p['introduced']=={'event_name':'no release','event_start_date':None},p['id']
for p in c['proposed_bundles']:
 assert p['introduced']=={'event_name':'no release','event_start_date':None},p['id']
print('PASS: component first-use dates match forward BOM reachability, including variant effective dates')
print(collections.Counter(first.get(p['id'],'no release') for p in b['components'] if p['id'] not in former_base))

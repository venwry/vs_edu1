from data_paths import read_document, document_bytes, document_text
from data_paths import resolve_path
from pathlib import Path
import json,hashlib,re,math
R=Path(__file__).resolve().parents[1]
def read(n):return read_document(n, root=R)
m=read('generated/models/ecosystem-forecast.json');text=(R/'ecosystem.html').read_text()
embedded=json.loads(re.search(r'<script type="application/json" id="ecosystem-model">(.*?)</script>',text,re.S).group(1))
assert embedded==m
for src in m['sources']:assert hashlib.sha256(document_bytes(resolve_path(src['path']), root=R)).hexdigest()==src['sha256'],src['path']
for s in m['scenarios']:
 assert len(s['quarterly'])==23
 cumulative_c=cumulative_a=cumulative_d=cumulative_o=0
 apps=s['applications'];models=s['device_models']
 assert len({a['id'] for a in apps})==len(apps)
 assert len({a['id'] for a in models})==len(models)
 for r in s['quarterly']:
  q=r['quarter'];c=[a for a in apps if a['cpm_first'] and a['cpm_first']<=q];t=[a for a in c if a['tui_first'] and a['tui_first']<=q];a=[a for a in apps if a['native_first'] and a['native_first']<=q]
  assert len(c)==r['cpm_applications'] and len(t)==r['tui_applications'] and len(a)==r['aionix_applications']
  assert len({x['id'] for x in c+a})==r['distinct_application_families']
  assert sum(x['cpm_quarterly_copies'].get(q,0) for x in c)==r['cpm_copies_sold']
  assert sum(x['cpm_quarterly_copies'].get(q,0) for x in t)==r['tui_copies_sold']
  assert sum(x['native_quarterly_copies'].get(q,0) for x in a)==r['aionix_copies_sold']
  assert len([x for x in models if x['first_quarter']<=q])==r['device_models']
  assert len({x['manufacturer_id'] for x in models if x['first_quarter']<=q})==r['device_manufacturers']
  assert sum(x['quarterly_units'].get(q,0) for x in models)==r['devices_sold']
  assert sum(x['units'] for x in r['external_oems'])==r['external_computers_sold']
  assert r['all_hardware_manufacturers']==r['device_manufacturers']+r['external_supported_manufacturers']
  assert r['all_hardware_models']==r['device_models']+r['external_computer_models']
  cumulative_c+=r['cpm_copies_sold'];cumulative_a+=r['aionix_copies_sold'];cumulative_d+=r['devices_sold'];cumulative_o+=r['external_computers_sold']
  assert (cumulative_c,cumulative_a,cumulative_d,cumulative_o)==(r['cpm_cumulative_copies'],r['aionix_cumulative_copies'],r['devices_cumulative'],r['external_computers_cumulative'])
  if q<'1980-Q2':assert not a and r['aionix_copies_sold']==0
  if q<'1979-Q4':assert r['external_supported_manufacturers']==0
 for a in apps:
  if a['kind']=='anonymous_cohort' and a['cpm_first'] and a['native_first']:assert a['tui_first']<a['native_first']
  for q,n in a['cpm_quarterly_copies'].items():assert n>=0 and (not n or a['cpm_first']<=q)
  for q,n in a['native_quarterly_copies'].items():assert n>=0 and (not n or a['native_first']<=q)
 for key in ['wordstar','dbase','supercalc','bdsc']:assert next(a for a in apps if a['id']==key)['native_first'] is None
# Match each reassessed scenario, not the frozen industrial baseline.
sales=read('generated/models/sales-forecast.json')
for scenario in m['scenarios']:
 current=next(s for s in sales['scenarios'] if s['id']==scenario['id'])
 for row in scenario['quarterly']:
  match=next(r for r in current['quarterly'] if r['quarter']==row['quarter'])
  assert row['logix_new_units']==match['products']
central=next(s for s in m['scenarios'] if s['id']=='central')
assert 3<=next(r for r in central['quarterly'] if r['quarter']=='1980-Q2')['external_supported_manufacturers']<=5
for k in ['cpm_applications','aionix_applications','devices_sold','cpm_copies_sold']:
 assert m['scenarios'][0]['quarterly'][-1][k]<central['quarterly'][-1][k]<m['scenarios'][2]['quarterly'][-1][k]
assert '__MODEL__' not in text and '__NAV__' not in text
print('PASS: 3 scenarios × 23 quarters; dated releases, deduplicated titles, licences, manufacturer/model ledgers, sales reconciliation, host anchors and source hashes')


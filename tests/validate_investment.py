from data_paths import read_document, document_bytes, document_text
from data_paths import resolve_path
"""Validate published industrial assets and their repository integration."""
from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parents[1]
model=read_document('generated/models/industrial-investment-1974-1981.json', root=root)
report=(root/'industrial_investment_1974_1981.html').read_text()
embedded=json.loads(re.search(r'<script id="model" type="application/json">(.*?)</script>',report,re.S).group(1))
assert embedded==json.loads(document_text('generated/models/industrial-investment-1974-1981.json',root=root)),'Published HTML and archived JSON differ: regenerate both'
rows=model['quarterly_entity_costs']
assert len(rows)==180 and len({(x['quarter'],x['entity']) for x in rows})==180
for r in rows:
 assert abs(sum(r['cost_type_usd'].values())-r['operating_usd'])<.2
 cap=sum(x['usd'] for x in model['capital_schedule'] if (x['quarter'],x['entity'])==(r['quarter'],r['entity']))
 assert abs(cap-r['capital_usd'])<.1
for r in model['quarterly_capacity']:
 assert r['installed_computer_capacity_month']>=r['peak_month_customer_demand']*1.05-.001
 assert r['fab_capacity_month']>=r['fab_wafer_starts_required_month']
for source in model['sources']:
 assert hashlib.sha256(document_bytes(resolve_path(source['path']), root=root)).hexdigest()==source['sha256'],source['path']+' changed: regenerate model'
site=read_document('generated/catalogs/site-pages.json', root=root);pages={x['id']:x for x in site['pages']}
assert 'industrial-investment' in site['navigation']
assert pages['industrial-investment']['path']=='industrial_investment_1974_1981.html'
for id in site['navigation']:assert 'href="'+pages[id]['path']+'"' in report
assert '__MODEL__' not in report and '__PROJECT_NAV__' not in report
print('PASS: 180 quarterly records, accounting, reserve capacity, source hashes, HTML/JSON parity and shared navigation')


"""One-time migration audit: every original JSON value is preserved (including list order).

Do not use this as a permanent gate after intentional content changes.
"""
import hashlib,json
from data_catalog import ROOT,manifest,read
m=manifest();baseline=read('tests/migration-baseline.json')
for old,expected in baseline['semantic_sha256'].items():
 value=read(m['paths'][old])
 actual=hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
 assert actual==expected,old
print('PASS: all',len(baseline['semantic_sha256']),'original JSON documents are semantically identical')

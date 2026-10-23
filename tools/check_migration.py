"""One-time losslessness audit against the single-layer migration base, not a permanent data freeze."""
import hashlib,json
from data_store import ROOT,read_document
fixture=read_document('tests/fixtures/single-data-migration.json')
for name,expected in fixture['views'].items():
 actual=hashlib.sha256(json.dumps(read_document('catalog:'+name),ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 assert actual==expected,'Changed payload: '+name
for path,expected in fixture['frozen_files'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
print('PASS: all 25 prior catalogue payloads and all saved model/baseline bytes are preserved')

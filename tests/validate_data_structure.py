"""Validate the single source layer and unchanged frozen baselines."""
import hashlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from validate_data import validate_collections
from data_store import read_document,registry
import jsonschema
count=validate_collections()
assert not (R/'generated/catalogs').exists(),'Do not restore generated specification copies'
assert not (R/'data/manifest.json').exists(),'Per-record assembly manifest is retired'
for schema,view in [('logix_aion_story','logix-aion-story'),('hardware_bom','hardware-bom')]:
 jsonschema.Draft202012Validator(read_document('schemas/legacy/'+schema+'.schema.json')).validate(read_document('catalog:'+view))
frozen=read_document('tests/migration-baseline.json')['semantic_sha256']
for old,path in registry()['legacy_paths'].items():
 if path.startswith('baselines/'):
  actual=hashlib.sha256(json.dumps(read_document(path),sort_keys=True,ensure_ascii=False).encode()).hexdigest();assert actual==frozen[old],path
print('PASS:',count,'authoritative files, legacy consumer contracts and immutable baselines')

"""Structural migration audit; frozen semantic digests are not financial recalculations."""
import hashlib,json,sys,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools'))
from merge_cost_reviews import merge
model=json.loads((R/'generated/models/manufacturing-costs.json').read_text())
expected=json.loads((R/'tests/fixtures/cost-consolidation-hashes.json').read_text())
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
reviews=model['reviews']
assert digest({k:v for k,v in model.items() if k!='reviews'})==expected['annual']
for key in ('ncc-1982','comdex-1982'):assert digest(reviews[key])==expected[key]
assert model['dated_assessments'][0]==reviews['comdex-1982']['cost_assessment']
for name in ('ncc-1982-review.json','comdex-1982-cost-review.json'):assert not (R/'generated/models'/name).exists()
import jsonschema
jsonschema.validate(reviews,json.loads((R/'schemas/models/manufacturing-reviews.schema.json').read_text()))
# The migration must be safe to repeat on already-consolidated output.
with tempfile.TemporaryDirectory(dir=R.parent) as tmp:
 root=Path(tmp);target=root/'generated/models/manufacturing-costs.json';target.parent.mkdir(parents=True);target.write_text(json.dumps(model))
 merge(root);first=target.read_bytes();merge(root);assert target.read_bytes()==first
print('PASS: all annual values and both complete reviews preserved; migration idempotent; review schema valid')

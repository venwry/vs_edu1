"""Validate explicit approved delivery-scope changes before historical audit comparison."""
import copy,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def historical_bom(bom):
    result=copy.deepcopy(bom)
    changes=json.loads((R/'tests/fixtures/product-completion.json').read_text())['assembly_changes']
    found=set()
    for a in result['assemblies']:
        if a['id'] not in changes:continue
        c=changes[a['id']];digest=hashlib.sha256(json.dumps(a['lines'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
        assert digest==c['after_sha256'],a['id']+' differs from reviewed delivery-scope change'
        a['lines']=copy.deepcopy(c['before']);found.add(a['id'])
    assert found==set(changes)
    return result

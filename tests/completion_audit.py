"""Validate explicit approved delivery-scope changes before historical audit comparison."""
import copy,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def historical_bom(bom):
    result=copy.deepcopy(bom)
    result=software_baseline(result)
    result=resolution_baseline(result)
    changes=json.loads((R/'tests/fixtures/product-completion.json').read_text())['assembly_changes']
    found=set()
    for a in result['assemblies']:
        if a['id'] not in changes:continue
        c=changes[a['id']];digest=hashlib.sha256(json.dumps(a['lines'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
        assert digest==c['after_sha256'],a['id']+' differs from reviewed delivery-scope change'
        a['lines']=copy.deepcopy(c['before']);found.add(a['id'])
    assert found==set(changes)
    return result


def resolution_baseline(bom):
    result=copy.deepcopy(bom)
    changes=json.loads((R/'tests/fixtures/composition-resolution.json').read_text())['assembly_changes']
    found=set()
    for a in result['assemblies']:
        if a['id'] not in changes:continue
        c=changes[a['id']]
        digest=hashlib.sha256(json.dumps(a['lines'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
        assert digest==c['after_sha256'],a['id']+' differs from approved composition resolution'
        a['lines']=copy.deepcopy(c['before']);found.add(a['id'])
    assert found==set(changes)
    return result


def software_baseline(bom):
    result=cutover_baseline(bom)
    f=json.loads((R/'tests/fixtures/software-delivery.json').read_text())
    digest=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    found=set();added=set();rows=[]
    for a in result['assemblies']:
        if a['id'] in f['added']:
            assert digest(a['lines'])==f['added'][a['id']],a['id']
            added.add(a['id']);continue
        if a['id'] in f['changed']:
            c=f['changed'][a['id']];assert digest(a['lines'])==c['after_sha256'],a['id']
            a['lines']=copy.deepcopy(c['before']);found.add(a['id'])
        rows.append(a)
    assert found==set(f['changed']) and added==set(f['added'])
    result['assemblies']=rows
    return result


def cutover_baseline(bom):
    result=copy.deepcopy(bom)
    f=json.loads((R/'tests/fixtures/composition-cutover.json').read_text())
    digest=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    found=set();added=set();rows=[]
    for a in result['assemblies']:
        if a['id'] in f['added']:
            assert digest(a['lines'])==f['added'][a['id']],a['id']
            added.add(a['id']);continue
        if a['id'] in f['changed']:
            c=f['changed'][a['id']];assert digest(a['lines'])==c['after_sha256'],a['id']
            a['lines']=copy.deepcopy(c['before']);found.add(a['id'])
        rows.append(a)
    assert found==set(f['changed']) and added==set(f['added'])
    assert not set(f['removed']) & {a['id'] for a in rows}
    result['assemblies']=rows+list(copy.deepcopy(f['removed']).values())
    return result

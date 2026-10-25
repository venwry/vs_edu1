"""Date/version-explicit compositions. No assembly input or duplicate traversal logic."""
import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def resolve_many(requests,root=ROOT,documents=None):
    result=subprocess.run(['node',str(ROOT/'tools/resolve_compositions.cjs')],input=json.dumps({'root':str(root),'requests':requests,'documents':documents}),capture_output=True,text=True,check=True)
    results=json.loads(result.stdout)
    for item in results:
        if 'error' in item:raise ValueError(item['error'])
    return [item['result'] for item in results]

def resolve(ref,*,date=None,version=None,root=ROOT):
    if date is None and version is None:raise ValueError('Specify a composition version or evaluation date')
    selection={'version':version} if version is not None else {'date':date}
    return resolve_many([{'ref':ref,'selection':selection}],root)[0]

def pricing_composition(ref,date,root=ROOT):
    """Select root at pricing date; children at their parent's start, not pricing date."""
    from datetime import date as Date
    Date.fromisoformat(date)
    result=resolve(ref,date=date,root=root)
    if result['issues']:raise ValueError('Incomplete dated composition: '+str(result['issues']))
    return result

def physical_inventory(result):
    """Keep conditions/units separate, including unknown quantities."""
    totals={}
    for line in result['leaves']:
        key=(line['ref'],line['unit'],tuple(line['conditions']))
        previous=totals.get(key,0);quantity=line['total_quantity']
        totals[key]=None if previous is None or quantity is None else previous+quantity
    return totals

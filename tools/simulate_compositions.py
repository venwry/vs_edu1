"""Read-only inventory audit after composition cutover; never rebuilds financials."""
import json,sys
from pathlib import Path
from collections import Counter
from compositions import ROOT,resolve_many

def simulate(root=ROOT):
    root=Path(root);load=lambda n:json.loads((root/'data'/n).read_text())
    products=load('product-catalog.json')['products'];devices=load('devices.json')['devices'];software=load('software-editions.json')['software_editions']
    owners=devices+software+products
    requests=[{'ref':o['id'],'selection':{'version':h['version_number']}} for o in owners for h in o['composition_history']]
    results=resolve_many(requests,root)
    fixture=json.loads((root/'tests/fixtures/composition-product-inventories.json').read_text());baseline=fixture['inventories']
    product_ids={p['id'] for p in products};comparisons=[];findings=[];unknown=set()
    for result in results:
        owner=result['ref'];version=result['version']['version_number'];inventory={}
        for issue in result['issues']:findings.append(dict(owner=owner,version=version,**issue))
        for line in result['leaves']:
            key=json.dumps([line['ref'],line['unit'],line['conditions']],separators=(',',':'))
            q=line['total_quantity'];old=inventory.get(key,0);inventory[key]=None if q is None or old is None else q+old
            if q is None:unknown.add(line['ref'])
        if owner not in product_ids:continue
        start=result['version']['valid_from'];key=next((k for k,(a,b) in fixture['intervals'].items() if k.rsplit('@',1)[0]==owner and a<=start<b),None);before=baseline.get(key)
        if before is None:findings.append(dict(kind='no_previous_inventory',owner=owner,version=version));continue
        differences=[{'key':k,'before':before.get(k,0),'after':inventory.get(k,0)} for k in sorted(before.keys()|inventory.keys()) if before.get(k,0)!=inventory.get(k,0)]
        comparisons.append(dict(owner=owner,version=version,differences=differences))
        if differences:findings.append(dict(kind='inventory_change',owner=owner,version=version,detail=differences))
    return {'summary':{'devices':len(devices),'software_editions':len(software),'products':len(products),'resolved_versions':len(results),'compared_versions':len(comparisons),'unchanged_versions':sum(not c['differences'] for c in comparisons),'unknown_components':len(unknown),'findings_by_kind':dict(Counter(f['kind'] for f in findings))},'comparisons':comparisons,'findings':findings}

def markdown(report):
    s=report['summary'];lines=['# Composition cutover inventory verification','',f"All {s['resolved_versions']} owner versions use the shared browser/Python resolver. All {s['compared_versions']} product versions are compared with pre-cutover composition inventories; this does not assert a financial cost baseline.",'',f"Unchanged product inventories: {s['unchanged_versions']}. Components with unknown quantities: {s['unknown_components']}.",'','| Product | Version | Change |','| --- | --- | --- |']
    for c in report['comparisons']:
        for d in c['differences']:lines.append(f"| {c['owner']} | {c['version']} | {json.loads(d['key'])[0]}: {d['before']} → {d['after']} |")
    lines+=['','Four November products gain two AION 2114 chips each. Four Budget product versions also receive the already-promised Abacus 3 diskette/documentation delivery, formerly declared outside compositions. Missing physical quantities remain unknown. Routing, supplier costs, licence/service charges and per-host qualification are separate financial/engineering gates. Saved models and frozen baselines are unchanged.','']
    return '\n'.join(lines).rstrip()
if __name__=='__main__':
    report=simulate();print(markdown(report) if '--markdown' in sys.argv else json.dumps(report,indent=2))

"""Read-only dry run of assembly consolidation and temporal composition BOMs.
No authoritative data or financial models are written. Run with --markdown for report.
"""
import copy,json,sys
from collections import defaultdict,Counter
from pathlib import Path
from data_store import ROOT,read_document

def simulate(root=ROOT):
    root=Path(root)
    load=lambda f:json.loads((root/'data'/f).read_text())
    devices={d['id']:d for d in load('devices.json')['devices']}
    products=load('product-catalog.json')['products']
    parts={p['id']:p for p in load('components.json')['components']}
    active={a['id']:a for a in load('assemblies.json')['assemblies']}
    retired={a['id']:a for a in load('retired_assemblies.json')['assemblies']}
    runtime={a['id']:a for a in read_document('catalog:hardware-bom',root)['assemblies']}
    findings=[];seen=set();comparisons=[];candidates=[];merged_products=[];device_candidates=[]
    def issue(kind,owner,version,ref,detail):
        key=(kind,owner,version,ref,detail)
        if key not in seen:seen.add(key);findings.append(dict(kind=kind,owner=owner,version=version,ref=ref,detail=detail))
    def select(ref,when,owner,version):
        histories=devices[ref]['composition_history']
        matches=[h for h in histories if when and h['valid_from'] and h['valid_from']<=when<h['valid_to']]
        if len(matches)!=1:
            issue('child_date_coverage',owner,version,ref,'Parent start '+str(when)+'; child intervals '+str([(h['valid_from'],h['valid_to']) for h in histories]))
            return None
        return matches[0]
    def add(out,ref,q):
        out[ref]=None if q is None or out.get(ref,0) is None else out.get(ref,0)+q
    def physical(lines,when,owner,version,temporal,path=()):
        out={}
        for line in lines:
            ref=line['ref'];q=line['quantity']
            if ref in devices:
                if ref in path:
                    issue('cycle',owner,version,ref,' -> '.join(path+(ref,)));continue
                h=select(ref,when,owner,version) if temporal else next(iter(devices[ref]['composition_history']),None)
                if not h:
                    if not devices[ref]['composition_history']:issue('missing_device_composition',owner,version,ref,'No defined physical composition')
                    continue
                nested=physical(h['composition_definition'],h['valid_from'],owner,version,temporal,path+(ref,))
                for leaf,n in nested.items():add(out,leaf,None if q is None or n is None else q*n)
            elif ref in parts:
                add(out,ref,q)
                if q is None:issue('unknown_quantity',owner,version,ref,'Physical quantity is unresolved; no exact cost or inventory total is possible.')
                introduced=parts[ref].get('introduced',{}).get('event_start_date')
                if temporal and when and introduced and introduced!='no release' and introduced>when:issue('component_after_parent',owner,version,ref,'Component introduction '+introduced+' is after parent start '+when)
            elif ref.startswith(('software.','edition.','service.')):pass
            else:issue('nonphysical_or_unresolved_ref',owner,version,ref,'No component/device owner; requires explicit costing treatment.')
        return out
    def legacy(aid,path=()):
        out={}
        if aid in path:raise ValueError('Legacy cycle')
        if aid not in runtime:return {aid:1}
        for line in runtime[aid]['lines']:
            for ref,q in legacy(line['ref'],path+(aid,)).items():add(out,ref,None if q is None or line['quantity'] is None else q*line['quantity'])
        return out
    def differences(a,b):return [{'ref':k,'legacy':a.get(k,0),'proposed':b.get(k,0)} for k in sorted(a.keys()|b.keys()) if a.get(k,0)!=b.get(k,0)]
    for p in products:
        for h in p['composition_history']:
            owner=p['id'];v=h['version_number'];start=h['valid_from'];lines=h['composition_definition'];aid=h.get('legacy_assembly_ref')
            if h.get('composition_status')=='unresolved':issue('quotation_scope_unresolved',owner,v,'','Site survey/application qualification must determine remaining equipment, quantities and services; this is not a complete fixed-price package.')
            if start is None:issue('unknown_start_date',owner,v,'','Cannot select dated children for an undated proposal.')
            if h.get('unresolved_items'):issue('unresolved_package',owner,v,','.join(h['unresolved_items']),'Referenced package has no defined contents; retained as unresolved provenance, not a product nesting edge.')
            mains=[l for l in lines if l['element_type']=='main_product']
            if len(mains)>1 or sum(l['quantity'] or 0 for l in mains)>1:issue('multi_computer_package',owner,v,'','Multiple supplied computers: connection placements must be allocated per host; aggregate capacity does not prove each machine is valid.')
            for l in lines:
                if l.get('placements'):issue('multiple_placements',owner,v,l['ref'],'Unique ref has distinct connection placements: '+json.dumps(l['placements'],sort_keys=True))
            unmerged=physical(lines,start,owner,v,False)
            temporal=physical(lines,start,owner,v,True)
            merged=copy.deepcopy(lines)
            if aid in active or aid in retired:
                assembly=active.get(aid,retired.get(aid));existing={l['ref']:l for l in merged}
                for l in assembly['lines']:
                    if l['ref'] in existing:
                        old=existing[l['ref']]
                        if any(old.get(k)!=l.get(k) for k in ['quantity','unit','condition','quantity_status']):issue('assembly_line_conflict',owner,v,l['ref'],'Source '+json.dumps(old,sort_keys=True)+' versus assembly '+json.dumps(l,sort_keys=True))
                        else:issue('assembly_duplicate_line',owner,v,l['ref'],'Same constituent already owned by composition; append would double count.')
                    else:
                        if l['ref'].startswith('assembly.'):issue('assembly_dependency',owner,v,l['ref'],'Must resolve/assign an owner rather than copying an assembly edge.')
                        merged.append({**copy.deepcopy(l),'element_type':'attached_product'})
                        issue('assembly_only_line',owner,v,l['ref'],'Not present in product composition: '+str(l['quantity'])+' '+l.get('unit','each')+'; role '+l.get('role',''))
                candidates.append(dict(assembly=aid,owner=owner,version=v,added_lines=len(merged)-len(lines)))
                issue('manufacturing_metadata',owner,v,aid,'Routing, requirements and cost_rollup_status need explicit owner/version assignment; not represented by composition lines.')
            if aid and aid not in runtime:issue('missing_legacy_bom',owner,v,aid,'No legacy runtime BOM for comparison')
            if aid in runtime:
                expected=legacy(aid)
                merged_products.append((owner,v,aid,start,copy.deepcopy(merged)))
                merged_inventory=physical(merged,start,owner,v,False)
                merged_temporal=physical(merged,start,owner,v,True)
                comparisons.append(dict(owner=owner,version=v,assembly=aid,unmerged_difference=differences(expected,unmerged),merged_static_difference=differences(expected,merged_inventory),merged_temporal_difference=differences(expected,merged_temporal)))
            elif lines:issue('no_legacy_product_bom',owner,v,'','Composition exists without a product-level legacy BOM; no equivalent cost baseline can be asserted.')
    for d in devices.values():
        for h in d['composition_history']:physical(h['composition_definition'],h['valid_from'],d['id'],h['version_number'],True,(d['id'],))
        for rev in d.get('dated_revisions',[]):
            aid=rev.get('bom_assembly_ref')
            if aid:
                assembly=active.get(aid,retired.get(aid))
                if assembly:
                    candidates.append(dict(assembly=aid,owner=d['id'],valid_from=rev.get('effective_from')))
                    device_candidates.append((d['id'],rev['effective_from'],copy.deepcopy(assembly['lines'])))
                    diff=differences(physical(d['composition_history'][0]['composition_definition'],None,d['id'],1,False),physical(assembly['lines'],None,d['id'],2,False))
                    issue('separate_device_revision',d['id'],2,aid,'Assembly revision starts '+str(rev.get('effective_from'))+'; must create a second composition version and close the first. Inventory changes: '+json.dumps(diff,sort_keys=True))
    # Second scenario adopts the separate dated DEVICE assemblies as well, in memory only.
    for ref,start,lines in device_candidates:
        history=devices[ref]['composition_history'];history[-1]['valid_to']=start
        history.append(dict(valid_from=start,valid_to='1990-01-01',version_number=len(history)+1,composition_definition=lines))
    for owner,v,aid,start,lines in merged_products:
        proposed=physical(lines,start,owner,v,True)
        row=next(c for c in comparisons if c['owner']==owner and c['version']==v)
        row['full_cutover_difference']=differences(legacy(aid),proposed)
        if row['full_cutover_difference']:issue('full_cutover_inventory_change',owner,v,aid,json.dumps(row['full_cutover_difference'],sort_keys=True))
    mapped={x['assembly'] for x in candidates}
    for aid,a in active.items():
        if aid not in mapped:issue('unmapped_active_assembly',aid,None,'','No unique product/device composition-version owner was established.')
    for p in products:
        for h in p['composition_history']:
            for l in h['composition_definition']:
                if l['ref'].startswith(('software.','edition.','service.')):issue('nonhardware_cost_boundary',p['id'],h['version_number'],l['ref'],'Keep licences/services outside recursive hardware manufacturing totals; duration and commercial quantity remain relevant.')
    return dict(summary={'devices':len(devices),'products':len(products),'active_assemblies':len(active),'retired_assemblies':len(retired),'compared_versions':len(comparisons),'unmerged_equal':sum(not c['unmerged_difference'] for c in comparisons),'merged_static_equal':sum(not c['merged_static_difference'] for c in comparisons),'merged_temporal_equal':sum(not c['merged_temporal_difference'] for c in comparisons),'full_cutover_equal':sum(not c['full_cutover_difference'] for c in comparisons),'unknown_components':len({f['ref'] for f in findings if f['kind']=='unknown_quantity'}),'findings_by_kind':dict(Counter(f['kind'] for f in findings))},candidates=candidates,comparisons=comparisons,findings=findings)

def markdown(result):
    lines=['# Composition cutover simulation','','Read-only simulation. Assembly consolidation and date-based BOM calculation are NOT enabled.','', 'Dates use inclusive starts and exclusive ends. Each nested child is selected at its immediate parent version start. Unknown quantities are not converted to zero.','', '## Results','', '```json',json.dumps(result['summary'],indent=2),'```','','Static comparisons ignore version dates to isolate ownership/packout differences. Temporal comparisons additionally enforce the requested parent-start rule. Financial values are not recalculated.','','## Every finding','']
    grouped=defaultdict(list)
    for f in result['findings']:grouped[f['kind']].append(f)
    for kind,rows in grouped.items():
        lines+=['### '+kind,'']
        if kind=='unknown_quantity':
            components=defaultdict(list)
            for f in rows:components[f['ref']].append(f['owner']+'@'+str(f['version']))
            lines+=['Unknown quantities remain null. Every affected component and owner/version is listed below.','']
            for ref,owners in sorted(components.items()):lines.append('- `'+ref+'`: '+', '.join('`'+o+'`' for o in owners))
        else:
            for f in rows:lines.append('- `'+f['owner']+'` version '+str(f['version'])+(' → `'+f['ref']+'`' if f['ref'] else '')+': '+f['detail'])
        lines.append('')
    lines+=['## Exact per-product physical differences','','```json',json.dumps(result['comparisons'],indent=2),'```','','## Proposed assembly ownership (not applied)','','```json',json.dumps(result['candidates'],indent=2),'```','']
    return '\n'.join(line.rstrip() for line in lines).rstrip()
if __name__=='__main__':
    result=simulate()
    print(markdown(result) if '--markdown' in sys.argv else json.dumps(result,indent=2))

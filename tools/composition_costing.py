"""Strict date-specific physical cost inputs; never infer quotes or routing.
Financial build stages can consume this result after their inputs are qualified.
Licence/service charges remain separate and this function does not publish models.
"""
from compositions import pricing_composition

def material_cost(ref,date,unit_costs,*,condition_values=None,root=None):
    kwargs={} if root is None else {'root':root}
    result=pricing_composition(ref,date,**kwargs)
    condition_values=condition_values or {};lines=[];total=0
    for line in result['leaves']:
        for condition in line['conditions']:
            if condition!='always' and condition not in condition_values:
                raise ValueError('Unqualified supply condition: '+condition)
        if any(c!='always' and not condition_values[c] for c in line['conditions']):continue
        quantity=line['total_quantity']
        if quantity is None:raise ValueError('Unknown quantity: '+line['ref'])
        key=(line['ref'],line['unit'])
        if key not in unit_costs:raise ValueError('Missing dated unit cost: '+str(key))
        price=unit_costs[key]
        if not price['valid_from']<=date<price['valid_to']:raise ValueError('Unit cost outside evaluation date: '+line['ref'])
        extended=quantity*price['amount'];total+=extended
        lines.append({**line,'unit_cost':price['amount'],'extended_cost':extended})
    return {'ref':result['ref'],'date':date,'version_number':result['version']['version_number'],'material_cost':total,'lines':lines,'manufacturing_owners':result['nodes'],'status':'materials_only_not_total_manufacturing_cost'}

"""Reject unrecognised categories in source schemas and service costing."""
import ast, copy, json, sys
from pathlib import Path
import jsonschema
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools'))
from schema_validation import record_validator
def read(p):return json.loads((R/p).read_text())
record=read('data/hardware/peripherals/device.color_monitor_1.json')
validator=record_validator(read('schemas/records/peripheral.schema.json'))
validator.validate(record)
for invalid in ['display','display_component','Monitor','not_a_category']:
    bad=copy.deepcopy(record);bad['data']['category']=invalid
    try:validator.validate(bad)
    except jsonschema.ValidationError:pass
    else:raise AssertionError('Accepted noncanonical category '+invalid)
tree=ast.parse((R/'tools/build_cost_assessment.py').read_text())
service_loop=next(n for n in tree.body if isinstance(n,ast.For) and ast.unparse(n.iter)=="C['services']")
catalog=read('generated/catalogs/logix-aion-technical-catalog-v2.json')
records={x['id']:x for v in catalog.values() if isinstance(v,list) for x in v if isinstance(x,dict) and 'id' in x}
rows=[]
env={'C':catalog,'records':records,'row':lambda *args,**kwargs:rows.append((args,kwargs)),'date':lambda x:x.get('introduced',{}).get('event_start_date')}
code=compile(ast.Module(body=[service_loop],type_ignores=[]),'<service costing>','exec')
exec(code,env);assert len(rows)>=len(catalog['services'])
env['C']={'services':[{'id':'service.invalid','category':'renamed_support'}]}
try:exec(code,env)
except ValueError as e:assert 'Unsupported service category' in str(e)
else:raise AssertionError('Unknown service silently costed as training')
print('PASS: canonical schema rejects legacy codes; unsupported service categories fail explicitly')

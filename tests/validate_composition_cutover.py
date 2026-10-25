"""Shared Python/browser graph and immutable financial boundary."""
import sys,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from compositions import resolve,pricing_composition
from simulate_compositions import simulate
from data_store import registry
s=simulate()['summary'];assert (s['resolved_versions'],s['compared_versions'],s['unchanged_versions'])==(164,72,64)
a=resolve('assembly.device.artemis_professional_video_128kb.comdex82',version=2)
b=pricing_composition('device.artemis_professional_video_128kb','1982-11-29')
assert a['leaves']==b['leaves'] and b['version']['version_number']==2
assert pricing_composition('device.artemis_professional_video_128kb','1982-11-28')['version']['version_number']==1
try:resolve('device.mono_pro_17')
except ValueError:pass
else:raise AssertionError('Implicit date accepted')
for path,digest in json.loads((R/'tests/fixtures/composition-migration.json').read_text())['financial_files'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
assert 'data/retired_assemblies.json' not in registry()['commercial_projection_files']
assert json.loads((R/'data/assemblies.json').read_text())['assemblies']==[]
print('PASS: all version inventories, explicit pricing dates, revision aliases and unchanged financial files')

from unittest.mock import patch
from composition_costing import material_cost
example={'ref':'device.test','version':{'version_number':1},'nodes':[], 'leaves':[{'ref':'part.test','unit':'set','conditions':['always'],'total_quantity':3}]}
prices={('part.test','set'):{'amount':2,'valid_from':'1980-01-01','valid_to':'1981-01-01'}}
with patch('composition_costing.pricing_composition',return_value=example):
    assert material_cost('device.test','1980-06-01',prices)['material_cost']==6
    try:material_cost('device.test','1981-01-01',prices)
    except ValueError:pass
    else:raise AssertionError('Expired unit price accepted')
    example['leaves'][0]['total_quantity']=None
    try:material_cost('device.test','1980-06-01',prices)
    except ValueError:pass
    else:raise AssertionError('Unknown quantity guessed')
print('PASS: dated unit prices, supplied-set units and unknown-quantity costing guard')

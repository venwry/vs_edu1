"""Shared RAM process economics. Assumptions are scenario inputs, not measured yields."""
import json, math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def policy():
    return json.loads((ROOT / 'generated/catalogs/memory-manufacturing.json').read_text())

def evaluate(recipe, wafer_cost=None):
    a = recipe['die_area_mm2']
    gross = .9 * (math.pi * 37.5**2/a - math.pi*75/math.sqrt(2*a))
    y0 = recipe['nonarea_yield']
    spatial = math.exp(-recipe['defect_density_cm2']*a/100)
    raw = y0*spatial
    # Repair never recovers non-area/systematic failures. Area includes spare circuits.
    repaired = y0*(spatial + recipe.get('repair_fraction_of_spatial_failures', 0)*(1-spatial))
    wafer = (wafer_cost if wafer_cost is not None else recipe['processed_wafer_usd']) + recipe.get('repair_cost_per_wafer_usd', 0)
    good = gross*repaired*.93
    return dict(gross_usable_dies=gross, raw_die_yield=raw, die_yield=repaired,
                good_packaged_dies_per_wafer=good, recurring_processed_wafer_cost_usd=wafer,
                good_packaged_chip_cost_usd=(wafer/(gross*repaired)+.65+1.3)/.93)

def selected(year, as_of=None):
    p = policy()
    as_of = as_of or f'{year}-06-15'
    candidates = [x for x in p['memory_recipes'] if x['available_from'] <= as_of]
    # Compare only releases with the required capacity/interface; all candidates are 64K x 1.
    return min(candidates, key=lambda r: evaluate(r, p['wafer_cost_by_year'][str(year)].get(r['node_um'], r['processed_wafer_usd']))['good_packaged_chip_cost_usd'])

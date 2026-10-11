# Industrial investment, capacity and workforce — 1974–1981

Open [Industrial investment](industrial_investment_1974_1981.html) from the Atlas navigation or home-page card. The [JSON model](industrial_investment_1974_1981.json) and HTML are generated together and committed as project assets.

The report adds 32 quarters × five entities (Logix, AION Labs, AION Software, DRI and BPI), product/BOM cost links, supplier/factory capacity, distribution and Academy logistics, engineering work packages, headcount, a staged 75 mm semiconductor line, capital schedules, inventory funding and interentity transfers. Existing sales, BOM and unit-cost inputs are not overwritten.

## Rebuild

Python 3.9+ and standard library only, from any working directory:

```sh
python tools/build_investment_model.py
python tests/validate_investment.py
node tests/atlas.test.cjs
```

The Atlas suite additionally requires its existing `jsdom` dependency. The generator reads source JSON at the repository root and writes both published assets there. Edit model assumptions in `tools/build_investment_model.py`; edit presentation in `tools/industrial_investment_template.html`. Do not hand-edit generated outputs. Navigation is generated from `site_pages.json`.

## Boundaries

- Nominal USD, not present-day money. New planning allowances use the documented escalation assumption.
- Reviewed source baseline: commit `52662752fae4abf14ce6a8adab2e4554ea932677`. Embedded hashes identify the actual input bytes used in each build; the commit records the original reviewed baseline, not a promise that future inputs are unchanged.
- Earlier conversation retrieval was unavailable. Committed sales forecasts provide the baseline. New demand is separated from repeated returning backorders.
- The forecast stops November 18, 1980. Subsequent demand is explicitly extrapolated, with conditional PRO shipments in July 1981. Unknown standalone catalog demand is listed rather than silently treated as zero.
- Reserve means 10% good-output capacity, not 10% extra sales. Inventory funding and die/package yield losses are distinct.
- Equipment, facility and staffing figures are engineering allowances, not quotations or proven production specifications. The future-equipped secret facility remains a separate unpriced dependency.
- DRI and BPI are independent entities. Ecosystem resource costs are not legal consolidated accounts. Reimbursements and equity commitments are distinguished from operating expenses.
- Embedded production payroll and custom-chip costs are reconciled to avoid charging the same resource twice. Purchased components retain supplier costs/margins.

The report validates arithmetic and capacity assumptions. It does not establish electrical release, supplier commitments, yield, commercial contracts or feasibility. Retain these qualifications when reusing the estimates.


## ROI and complete marketing budget through 1980

Open [Quarterly ROI](roi.html) for revenue, marketing-adjusted operating costs, investment, quarterly ROI and cash-recovery charts. [ROI.md](ROI.md) documents the bridge and reproduction steps. The ROI model replaces the industrial report's generic marketing allowance with itemized commercial, conference and promotional budgets; its net cash/returns are project-wide and pre-tax.

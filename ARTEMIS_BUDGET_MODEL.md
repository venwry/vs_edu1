# Artemis budget offering and demand reassessment

Accepted correction: May 1980 launch, not December 1979. Both configurations remain available in December 1982. Existing 12-inch Color II limits apply; no 1982 Color Pro feature is backdated. Initial packages include AIONix/Business Tools; Abacus 3 is included only from November 1980 and NIC from May 1981. The HDD configuration keeps both floppies and adds a complete 5 MB subsystem, external where necessary.

The cost overlay uses frozen source breakdowns in `generated/catalogs/artemis-budget-inputs.json`; update those inputs deliberately after a new base-cost assessment. No supplier quote is claimed. 1980–81 use a 25% contribution margin after the 25% dealer fee. 1982 uses the balanced percentage principle against $3,299 and $4,995 hardware reference baskets: retail = sqrt(cost × comparator / 0.75). IBM’s substitute OS and narrower software portfolio remain story assumptions. No earlier IBM-PC comparison is used.

Run after base cost and pricing builds, in this order:

```
python tools/build_artemis_budget.py
python tools/build_retail_catalog.py
python tools/build_sales_reassessment.py
python tools/build_ecosystem_forecast.py
python tests/validate_budget_model.py
```

Sales factors are finite scenario judgements, not measured elasticities or historical market outcomes. Budget configurations substitute for other Artemis baskets within computer totals; clone cannibalisation is deducted once. Adam’s foresight means capacity follows the forecast with 5% headroom. Incremental capacity funding occurs one quarter before service, inventory is still financed and additional qualification/service work remains an expense. Greater sales do not imply automatically higher percentage ROI.

Business-only market share is shown separately from all microcomputers. Its 1980–83 baseline volumes are 450k/650k/950k/1.5m, with quarterly weights 23/24/25/28%. These are explicit low-confidence addressable-market assumptions. All Logix and clone units are allocated to business; if any are home/education purchases, their business share must be reduced. Competitor weights allocate residual demand; they do not reproduce historical Apple/IBM sales. Unit share is not revenue share or installed base.

ROI is pre-tax consolidated project accounting return: cumulative EBIT / (cumulative capital spending + ending inventory and component-credit working capital). It is not IRR or return on equity. Independent clone computer revenue and Autodesk licence revenue are excluded. Base industrial/resource costs are bridged from the frozen model; incremental capacity is a planning allowance, not a released factory engineering plan.

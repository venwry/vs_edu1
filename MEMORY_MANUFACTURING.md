# RAM manufacturing and investment revision

ERAv1 remains a 55 mm², 3 µm design with the existing 6/8 MHz variants. CPU performance, RAM capacities, bank widths and graphics are unchanged. The programme begins in January 1979, with separate development processes and milestone events on the timeline.

The accepted alternative-history model compares released 64K x 1 DRAM recipes by recurring packaged-chip cost. Process control and repairable 3 µm DRAM are the economical 1980/81 route. Initial 2.75 µm RAM remains a qualified candidate; its higher wafer cost and immature yield outweigh its smaller die. The 2.0 µm and 1.5 µm release targets remain prospective, dated July 1982 and October 1983. Their costs do not flow into 1981 products or ROI.

## Yield and qualification

`tools/memory_manufacturing.py` applies `Y = Y0 × [exp(−D×A/100) + r×(1−exp(−D×A/100))]`. Area includes spare structures; repair recovers only spatial failures. Non-area failures cannot be repaired. Wafer economics include repair operations, package/test costs and final-test yield. These are explicit scenario inputs, not measured historical performance. The 35% recovery assumption requires defect-map validation, fuse programming and complete retest. A smaller feature size does not itself imply a memory density, CPU speed or guaranteed yield improvement.

AION 4164 replaces purchased 64K chips in the generic 128 KiB module, including PRO and expansion kits. Aurelia+ uses eight chips; Artemis 256 KiB uses 32; PRO 512 KiB/1 MiB uses 64/128. Server-grade qualification must cover speed, retention, refresh, power, voltage and all-bank operation. Purchased-memory specifications remain available as a contingency but receive no automatic cost credit.

Cost snapshots are June 15. RAM wafer loading and fab charges use the latest date-eligible chip snapshot, preventing an unavailable early computer cost snapshot from pulling a later RAM recipe backward. The 1979 launch chip is the pre-June 1980 proxy. This conservatively delays repair savings until the June 1981 financial snapshot even though the engineering release target is January. Other legacy silicon retains its existing annual planning convention. Monthly retail and demand changes also respect dated snapshots.

## Prices, demand and investment

The existing balanced-percentages policy remains `P = sqrt(C × B / (1 − fee))`: margin/net receipts equals discount/market reference. Existing elasticities drive demand changes; no additional technology or marketing uplift is added. The 1981 price response is normalized for the 1980 response already embedded in its starting run rate. PRO sales start conditionally in July 1981.

The industrial model includes $2.225m process capital through 1981, 264 incremental engineering person-months through the existing payroll model, and $324k pilot/nonpayroll spending. The previously funded 120 PM original 64K programme is not repeated. Repair operations are charged in recurring chip costs. Pilot lots produce no credited saleable output; the legacy fab retains its own reserve and redundancy requirements.

The 1982–83 forward budget adds $1.5m capital and $1.38m engineering/validation. These are commitments beyond the financial horizon, not a complete future operating budget. The report discloses end-1981 cash after reserving all $2.88m. It does not present that reserve sensitivity as future ROI or invent 1982–83 revenue.

The previous model is frozen at commit `8b4b09b2b708453376d0952a6db190889f130e21` in `memory_manufacturing_baseline.json`. Both comparison cases use the same 1981 ROI extension, including cost-matched BPI license revenues. The revised case also corrects RAM vintage matching in fab costing. ROI is project-wide and includes induced demand, capacity, inventory, payroll and marketing costs; it is not a causal or isolated return on the memory programme. Legacy ROI JSON filenames remain stable while their metadata and contents extend through 1981.

## Regenerate and validate

```sh
python tools/apply_memory_manufacturing.py
python tools/build_cost_assessment.py
python tools/build_pricing.py
python tools/build_sales.py
python tools/build_investment_model.py
python tools/build_roi.py
python tools/build_memory_report.py
for test in tests/validate_*.py; do python "$test"; done
node --test tests/*.test.cjs
```

Python validators require `jsonschema`; DOM tests require `jsdom`. Do not rerun older configuration migrations after this migration: they may restore superseded BOMs or manufacturing assumptions. Do not regenerate the frozen comparison from revised inputs.

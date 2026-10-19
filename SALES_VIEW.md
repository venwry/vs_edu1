# Calendar sales view

[sales.html](sales.html) presents one continuous forecast from January 1978 through November 18, 1980. Select a scenario, monthly / quarterly / annual grouping, and an optional calendar year. The stacked chart, KPIs, table and CSV export all use the same selected rows.

The page reads `sales_forecast.json`; it does not alter forecasts, prices or financial models. `sales.js` normalizes the four disjoint source arrays (`months`, `post_ncc_months`, `comdex_to_ncc1980_months`, `ncc_to_comdex1980_months`) and sums flows into calendar periods. The two May 1980 segments are combined exactly once. January–May 1978 use the documented pre-launch zero-sales assumption. Months beyond the forecast cutoff are not invented.

All views show Aurelia, Aurelia+, Artemis and total computer deliveries, cumulative deliveries since launch, computer-package retail spend, receipts after channel fees, recurring costs and contribution. Money is aggregated in integer cents from the source values. Contribution is summed as reported; original source rounding can produce small differences from receipts minus cost. It is not net corporate profit. Independent BPI, separate applications and Academy tuition are excluded from computer-package financials.

November 1980, Q4 1980 and the 1980 annual total are partial, ending November 18; they are never annualized. Exact coverage dates appear in the table and CSV. Cumulative units retain their since-launch meaning when filtering to one year. The footer totals the selected periods; its cumulative cell is the final since-launch balance, not a sum of cumulative rows.

Original campaign-period tables, demand assumptions, Academy estimates through May 18, 1980 and their existing anchor links remain in an expandable section. Later extrapolated full-demand planning in the industrial investment and ROI reports is linked separately, rather than mixed into the capacity-limited sales forecast.

Validation (requires the project's existing jsdom dependency):

```sh
node tests/sales.test.cjs
node tests/atlas.test.cjs
```

Checks cover all three scenarios, financial and model-unit reconciliation across all groupings, the May boundary, partial-year labels, year filtering, cumulative balances, CSV export, existing anchors and fetch-error recovery.

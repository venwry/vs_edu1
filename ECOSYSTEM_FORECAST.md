# Third-party ecosystem forecast, 1978–1983

Open [Third-party ecosystem](ecosystem.html). It includes three adoption scenarios, quarter/year selectors, application and paid-copy charts, quarterly tables, likely leading software, hardware categories, a supported OEM table, a device-model ledger and CSV export.

This is an alternative-history forecast. It does not claim that named suppliers actually built Logix versions, or convert recruitment targets into recorded shipments. Breakthru TUI is the user-facing name used here for the project's documented Logix TUI API. The entire worldwide CP/M market is not counted as a qualified Logix market.

## Market anchor and boundaries

The model takes delivered units from the four nonoverlapping periods in `sales_forecast.json`, including the split May 1980 periods, through November 18, 1980. It adds 12/30 of the industrial plan's November demand and its December plan, then uses the conditional 1981 industrial monthly volumes. These tails are explicit projections. Through 1981 all three ecosystem cases share that same central Logix host series.

From 1982, quarterly Logix shipments change by −2% / +4% / +8% in conservative / central / strong cases. Native share grows 3.5 percentage points each quarter, capped at 85%; PRO is 4% of all shipments in 1982 and 7% in 1983. Existing hosts retire at 1% per quarter. There is no new feedback into the project's financial forecast or ROI. Third-party sales are independent receipts, not Logix revenue.

External supported CP/M/TUI configurations have separate, explicitly assumed OEM cohorts. Tandy's October 1979 release is a story anchor; its volumes are assumptions. Other brands are unsigned prospects. Their initial supported-configuration shipments grow 15% per quarter, capped at 4,000 per OEM per quarter. Qualification is delayed two quarters in the conservative case or advanced one quarter in the strong case, but never before 1979 Q4. Tandy's release date stays fixed. Only 35% of these external hosts contribute to the FlexiBUS accessory market. Global CP/M popularity provides potential existing software supply, not an invented global host count.

## Catalogue and licence calculations

For quarter index `t=0` at 1978 Q2 and active qualified CP/M hosts `H`:

- CP/M title target = `(12 + 18 × sqrt(H/1000)) × min(1, 0.45 + 0.035t) × developer multiplier`, rounded and never below already available titles.
- TUI-aware target = CP/M title count × `min(0.52, 0.12 + 0.018t)` × TUI adoption multiplier, bounded by total CP/M titles. Named release gates and existing TUI titles remain respected.
- Native AIONix starts in 1980 Q2. Tool maturity starts at 0.2 and rises 0.1 per quarter to 1. Native portable-C cohorts draw from the prior quarter's TUI pool, with a completion share starting at 0.20 and rising 0.045 per quarter to 0.72. Native-only title supply scales as `7 × sqrt(native hosts/1000) × maturity × developer multiplier`.
- Named assembler-heavy products do not enter that automatic C-port cohort. BPI is an existing native 1980 Q2 anchor. New vertical-business, communications, scientific and education C/TUI exemplar families have stated native release targets from 1980 Q3 to 1981 Q2.
- CP/M paid licences = `1.15 × new hosts + 0.10 × existing active hosts`, multiplied by scenario purchasing intensity. AIONix uses 1.45 and 0.13, with a launch-ramp factor from 0.35 to 1.
- The existing independent BPI family is counted separately at 20% of new Logix hosts; it is not assumed on external OEM hosts. This is a customer-licence measure, not the financial model's individual module/bundle SKU count. No Logix or AION bundled application copies are included.

Licence totals are allocated to eligible title families by declared relative weights using largest-remainder rounding. TUI-aware titles receive a 1.4 preference weight. Named candidates represent a small part of the catalogue; anonymous cohorts represent the long tail. Their identifiers are numerical forecast constructs, not invented commercial product announcements. Default names such as “vertical-business package” are exemplars of one family, not an entire category being counted as one title. All popularity rankings are modeled rankings.

CP/M title totals contain the TUI subset. AIONix counts native ERA editions only. CP/M programs running through a Z80 coprocessor are not native AIONix titles. Cross-platform product families are deduplicated in the unique-family total. Versions, languages and disk formats do not create new families. Titles/models are assumed to remain available through 1983; no catalogue retirements are modeled.

## Hardware calculations

Accessory supplier target = `(1 + 0.75 × sqrt(qualified hardware hosts/1000) + 0.3t) × min(1, 0.35 + 0.04t) × developer multiplier`. Entry gates progress from printers in 1978 Q3 to specialist instruments in 1980 Q1. Each supplier starts with one model and adds one qualified model every four quarters. Generic manufacturers are unique suppliers, not duplicate dealers; no named brand is asserted to have signed a new contract.

Quarterly accessory sales = `0.34 × new qualified hosts + 0.045 × existing active hosts`, scaled by purchasing intensity and an initial supplier ramp of `min(1, 0.5 + 0.03t)`. Category weights allocate those units across eligible models. OEM computer shipments, manufacturer counts and model counts are reported separately, then combined only in explicitly labeled totals.

These rates represent a plausible small business aftermarket, not observed conversion rates. They remain sensitive to price, dealer access, service quality, competitors, resource constraints and actual conformance. Low/high scenarios vary developer participation, TUI adoption, purchase intensity, external OEM adoption and later host growth together; they are not probability intervals.

## Engineering interpretation

Published SDKs, versioned interfaces and Adam's C policy improve the investment case, but C alone is not a guarantee of portability. Shared C application logic must respect different integer/pointer widths, banked versus virtual memory, CP/M records versus AIONix streams, and numeric/file-format contracts. Assembly and direct hardware access impose greater migration effort. Full dual-target tools arrive in May 1980, not in the 1979 public SDK.

FlexiBUS supports external cross-host reuse after class/driver qualification. It has one device per point-to-point port, quiescent attachment and at most 50 KB/s before overhead. Monitor compatibility depends on electrical/raster/readability qualification. Internal cards remain platform-specific even when software APIs are shared. Apple II/S-100 adapters are access paths, not proof of official OEM support or CP/M execution on an unmodified Apple II. Existing 1.4-derived CP/M also needs explicit compatibility qualification for software requiring later OS services.

Historical sources in the policy support category choices and timing examples. All numerical forecasts, port-effort ranges and fictional qualification dates are analytical assumptions. The new ecosystem page leaves existing costs, prices, sales and ROI arithmetic unchanged.

## Regeneration

```sh
python tools/build_ecosystem_forecast.py
python tests/validate_ecosystem_forecast.py
node tests/ecosystem.test.cjs
```

The Python builder uses only the standard library. The DOM test requires the project's `jsdom` dependency. If shared navigation changes, regenerate the industrial, ROI and memory report HTML as well. `ecosystem_forecast_policy.json` holds editable commercial assumptions; generated JSON contains source hashes, all 23 quarterly rows per scenario, title families, supplier/model ledgers and their quarterly sales.

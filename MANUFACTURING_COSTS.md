# Recurring unit manufacturing and delivery costs, 1978–1981

Open `manufacturing-costs.html` through the same static server as the Atlas. It reads `manufacturing_costs.json`: 122 rows with four June 15 snapshots. There are 48 priced rows in 1978, 55 in 1979, 95 in 1980 and 120 in 1981. Rows overlap (bundles, parent software, platform editions and individual components), so **do not add all rows into a company-wide total**.

These are engineering scenario estimates, not historical Logix accounts or supplier quotations. The alternative-history design is taken from the catalog revision recorded in JSON. Historical wages and electricity prices anchor the conversion costs; component procurement, volumes, fabrication yields and operation times are explicit assumptions. The engineering BOM retains its unresolved quantities and prices unchanged.

## Illustrative results

Nominal USD, rounded to whole dollars; each year's snapshot is June 15. A dash means not yet offered. Consult the page/JSON for the scenario ranges.

| Complete offering | 1978 | 1979 | 1980 | 1981 |
|---|---:|---:|---:|---:|
| Aurelia monochrome system | 751 | 722 | 701 | 695 |
| Aurelia color system | 854 | 823 | 800 | 793 |
| Aurelia+ monochrome system | — | — | 1,118 | 998 |
| Artemis 128 KiB monochrome system | — | — | 1,180 | 1,208 |
| Artemis 256 KiB monochrome system | — | — | 2,273 | 1,875 |
| Artemis PRO 512 KiB server | — | — | — | 3,509 |
| Artemis PRO 1 MiB server | — | — | — | 5,236 |

The 1981 Artemis bundle includes its dated networking variant and Server OS replacement, so its cost is not directly comparable to the non-networked 1980 configuration. PRO estimates are for announced offers; shipping dates remain unconfirmed. The PRO offers contain only the components actually listed in their BOMs: no invented monitor or keyboard is added.

## Cost boundary

Included: purchased BOM, recurring internal-chip fabrication, loaded production/test labor, energy, production consumables, assembly scrap/rework, factory operation/maintenance allowance, manuals, physical software duplication, packaging, logistics and provisional recurring third-party license charges. Bundled support contributes its expected delivery cost. Service rows use customer-years, learner-courses or registrations rather than pretending to be hardware units.

Excluded: R&D, design, original mask/tooling NRE, software/firmware development, land/buildings/equipment, capital depreciation and financing, marketing/promotion/vouchers, ComputerLand fees and retailer margins, profit and taxes. Purchased component prices inevitably include suppliers' own overhead and margins. No attempt is made to remove their capital costs from a procurement price.

Computer chassis rows exclude external keyboard/monitor and the system software cartridge. Bundle rows include their canonical accessories, software delivery and included support. Packaging/manuals/freight are applied once at the final offer, not separately to every internal assembly. Assembly test labor is incremental at each assembly level. Internal chip costs already incorporate wafer and package losses; board-level yield/rework is additional.

## Model and assumptions

- US production and domestic distribution; nominal dollars of each year. No present-day inflation conversion.
- Planning volumes: 10,000 hardware units per family/year, 1,000 PRO/year, 5,000 media/manual sets, component orders generally 10,000–100,000 pieces. These are assumptions, not story sales forecasts or quoted tiers. Supplier availability and volume discounts may dominate actual results.
- Loaded manufacturing labor equals June BLS manufacturing hourly earnings multiplied by 1.35 for employment burden. Skilled service staff and instructors have additional 1.6× and 2× wage multipliers.
- Assembly hours, kWh and consumables per assembly are recorded in JSON. Routine supervision/maintenance is 25% of loaded assembly labor; a 10% labor rework allowance and 1.5% incremental materials loss apply to assemblies with processing operations. Equipment depreciation is excluded.
- Each of 221 component-cost entries has annual price/cost buckets. An unresolved multi-part line is one priced **functional set**, not an assertion that a circuit contains one physical part. There are 166 explicitly identified unresolved quantity substitutions. Three Aurelia/Aurelia+ FlexiBUS ports provisionally use three host-controller dies; the engineering integration remains undecided.
- Custom silicon uses a 75 mm wafer scenario, explicit die area and year-dependent defect density. Good die output is geometric usable dies times die yield. Recurring processed-wafer cost is allocated 18% substrate/materials, 36% workforce, 10% energy, 24% consumables and 12% operations. Packaging and final-test labor are added and divided by 93% packaging/test yield. All these fabrication parameters are unverified planning assumptions; design and mask access does not eliminate yield risk. Yield loss is already inside the chip's cost buckets.
- Purchased 16K DRAM central prices are $6/$4.50/$3.25/$2.25 per chip; 64K DRAM $80/$65/$40/$25. The first two 64K prices are unused in pre-introduction products. These are assumed OEM tiers, not verified quotations. High-density Artemis cost is especially sensitive to 64K DRAM sourcing. A 1 MiB PRO needs 128 data DRAMs, not eight chips.
- AION-made display RAM is separate from purchased system DRAM: `part.aion_4116`, 18mm² central die, $3.4452 each / $27.5618 for eight in 1978. The buffered Aurelia controller uses 48mm² and costs $18.743, giving $46.30 for the chipset. All are scenario estimates, excluding capital and development; see VIDEO_DESIGN.md. Later years use the existing annual yield-learning model.
- The 1981 5 MB HDD allowance is $950; historical Seagate single-unit and large-order pricing provide a plausibility bracket, not a Logix purchase agreement.
- The Artemis video RAM organization is unresolved; it is provisionally costed as eight AION 4116-equivalent 16K×1 DRAMs. CRT pricing assumes a complete OEM display chassis; the otherwise unspecified separate HV/deflection/PSU line is therefore zero. Bare-tube sourcing would require an additional allowance.
- CP/M, its networking distribution, and Microsoft BASIC have provisional recurring rights allowances of $10, $5 and $20 respectively. These are not sourced contract terms. Software development remains excluded. AIONix is owned in the scenario and receives no invented third-party royalty.
- Software profiles record diskette counts and printed page counts. General BPI is a five-module set; module rows and platform edition rows are alternatives. Developer registrations include the SDK delivery once.
- Training assumes eight learners and six contact hours plus 1.5 preparation hours per day; unspecified course durations are explicitly modeled. Support hours are expected usage per customer-year, not contractual caps. Sales-channel and individually negotiated OEM-license records remain N/A; actual OEM chip production is costed separately.
- No discontinuation dates exist in the catalog, so earlier products continue in later snapshots. This is a retention assumption, not proof of historical availability. Only shipping-baseline RAM configurations are treated as factory configurations; expansion targets remain represented by their offered kits.

## Uncertainty and interpretation

Hardware/software ranges generally span 0.70–1.60× central, PRO 0.65–1.75×, custom OEM chips 0.50–2.50×, services 0.55–1.90×. These are correlated scenario envelopes, not confidence intervals, not sums of independently quoted best/worst prices. Component assumptions also include narrower/broader input sensitivity factors for reuse; those factors are not independently propagated into the aggregate envelope.

The central estimates assume a working design in recurring production. They are not a feasibility verdict, and startup fab under-utilization or failed qualification could push costs above the range. No electrical performance, production yield, defect rate or factory output is established by this calculation.

The JSON preserves cents for checking arithmetic, while the page displays whole dollars. The apparent precision does not imply accurate quotations. Select any priced cell to see its cost categories and flattened BOM; the JSON also records fabrication parameters, assembly routing, quantity assumptions, source references and excluded catalog records.

## Historical anchors

- [BLS/FRED manufacturing earnings](https://fred.stlouisfed.org/data/AHEMAN): June 1978–1981 wages are $5.99, $6.54, $7.08 and $7.85/hour. The burden and skill multipliers are assumptions.
- [EIA Table 8.10](https://www.eia.gov/totalenergy/data/annual/txt/ptb0810.html): annual industrial electricity prices proxy each snapshot, at 2.8, 3.1, 3.7 and 4.3 cents/kWh. They are retrospective annual rates, not June utility tariffs.
- [BYTE November 1978](https://vintageapple.org/byte/pdf/197811_Byte_Magazine_Vol_03-11_OSCAR_amateur_radio_satellites.pdf): an advertised eight-chip 4116 retail kit is a sanity check; later advertising is not a contemporaneous June OEM quote.
- [Apple advertisement, BYTE August 1978](https://vintageapple.org/byte/pdf/197808_Byte_Magazine_Vol_03-08_Pascal.pdf): the Disk II's $495 complete-unit retail offer is only a market comparison, not manufacturing cost.
- [Seagate corporate history, Computer History Museum](https://archive.computerhistory.org/resources/access/text/2015/04/102740040-05-01-acc.pdf): recorded 5 MB drive pricing spans $1,500 singly to $775 at 5,000 units. The modeled $950 is explicitly interpolated judgment.

## Reproduction and validation

```sh
python tools/build_cost_assessment.py
python tests/validate_costs.py
node tests/costs.test.cjs
node tests/atlas.test.cjs
```

The generator owns price and process assumptions; adjust it and regenerate JSON for alternative scenarios. Tests check offering coverage, endpoints, arithmetic, one-count NIC/OS inclusion, correct RAM population, filters and detailed views. Original engineering BOM files are read-only inputs. The page is integrated into the shared Atlas navigation and loads its cost data separately.



## NCC 1979 cards and independent SMC sourcing

Three new cards have explicit engineering assemblies: S-100 FlexiBUS, Apple II video, and S-100 video. Each video card counts one Aurelia video controller and eight 16Kx1 video RAMs (16 KiB). The two-port Apple/S-100 FlexiBUS interfaces use two host dies as an explicit cost assumption pending final ports-per-die design. Controller silicon is split from transceivers to prevent hidden/double-counted fabrication cost.

The June 1979 snapshot uses AION-produced chips. SMC’s initial commercial sales start in October 1979, with per-part qualification gates. Base annual unit costs retain AION fabrication; conditional 1980/1981 card alternatives replace those chip costs with purchased SMC components. The illustrative price proxy is 1.6 times modeled internal recurring chip cost plus $0.25 inbound freight; 1.2–2.4 times is a sensitivity range, not a quote. Vendor margin/capital recovery and any embedded royalty are included, not charged again. No supplier-switch or cost-saving claim follows from licensing.

`manufacturing_programs.json` separately budgets process/layout support, SMC-compatible ready-to-use masks/revisions, pilot wafers, qualification/test engineering and training. Its $175,000–$610,000 range ($330,000 central) is a planning allowance in nominal 1978–1979 USD, not an agreed payment. New fab equipment and major process-capacity expansion are excluded. Mask delivery helps but does not establish DRAM retention, sensing or production yields. None of this NRE is silently amortized into product rows.

Adam’s $250,000 DRI founder commitment is equity financing, not an expense per CP/M copy. Existing provisional OEM royalty allowances remain because DRI is a separately owned licensor.


The 1978 campaign, professional NCC filming/editing and free station-copy distribution are marketing costs, excluded from hardware BOMs and recurring unit costs. The campaign budget is unspecified, not zero; see `aurelia_1978_campaign.json`. Academy setup is distinct from existing recurring course delivery. Fundamentals 50% tuition credit is calculated in pricing as promotional exposure, counted once across the course and system sale including dealer reimbursement.


Tandy Model II and its external partner interface are Tandy-owned designs, not added to Logix BOM/unit-cost totals. The Abacus port requires engineering expenditure and native media qualification; no invented OEM royalty, port budget or extra retail unit is assigned. Their commercial terms remain unresolved in the partner specification.


NCC 1979 campaign, engineering support and compatibility certification expenses remain unbudgeted operating programmes, not changes to recurring hardware costs. See NCC_1979_CAMPAIGN.md and CONSISTENCY_REVIEW_1979.md.

The December 1979 manufacturer compatibility kit and optional support/certification add three rows, first costed in the June 1980 snapshot. Reproduction and bounded engineering workloads exclude programme development/NRE. See AURELIA_COMPATIBILITY_KIT.md.

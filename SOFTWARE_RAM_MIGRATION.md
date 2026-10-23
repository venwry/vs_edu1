# Software products, editions and shared RAM modules

This revision implements the author's requested catalogue semantics. It is an
accepted story-design change, not evidence of historically qualified hardware.
The author confirmed 32-bit **modules** and chose to preserve advertised system
capacities. This therefore changes physical BOM quantities, rather than labels alone.

## Software ownership

`data/software/products/` contains 14 abstract products. Abacus, Pulse, AIONix,
CP/M and BPI each have one product. `data/software/editions/` contains 32 concrete
editions. Each edition owns `version` (nullable when unspecified), `edition`,
execution target, availability, platform support, dependencies and its rich
specification. Product category and common vendor are inherited through
`product_ref`; no second category is authored on editions.

For example `software.product.abacus` contains Abacus 1.x, 2.0 and 3.0 editions.
`software.abacus_2` is **Abacus 2.0 (CP/M edition)** and
`edition.abacus_2.era` is **Abacus 2.0 (AIONix edition)**. The old version-level ID
is retained for the first concrete edition; its formerly separate platform row
is merged into it. Other target editions retain their IDs. Platform-specific
Artemis extensions are not attributed to the CP/M edition. Unknown software
versions remain null. Version-specific facts are preserved on each applicable
edition, allowing platform editions to diverge independently.

Product envelopes use version 3; edition envelopes use version 2. The one legacy
external hardware entry in the software-product projection retains its v2 schema
until a separate hardware classification migration. Schema v3 restricts products
to identity, introduction, vendor, category and edition membership. The Navigator
distinguishes **Software product** and **Software edition** classes.

Computer compatibility lists reference concrete editions. A shared cartridge BOM
is a physical delivery assembly, not another software product. Cost builders
iterate editions and do not charge an additional abstract product row.

## RAM ownership and arithmetic

| Canonical module | Capacity | Width | DRAM | Ranks | Chips | Paired bank |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| `part.ram_64kb_x32` | 64 KiB | 32 bits | 16K × 1 | 1 | 32 | 128 KiB |
| `part.ram_128kb_x32` | 128 KiB | 32 bits | 16K × 1 | 2 | 64 | 256 KiB |
| `part.ram_256kb_x32` | 256 KiB | 32 bits | AION 64K × 1 | 1 | 32 | 512 KiB |
| `part.ram_256kb_x32_2um` | 256 KiB | 32 bits | AION 64K × 1, 2 µm | 1 | 32 | 512 KiB |

Both modules share the 32-bit host bus and are independently selected by address;
a bank groups their capacity rather than concatenating their data lanes into a
64-bit bus. Every module/rank requires decode and refresh. This is a new accepted
interface target; connector, timing, power and loading still require qualification
on each host. The 2 µm variant remains distinct because its chip/process
specification differs, not because it belongs to Athena.

Shipping/offered system capacities remain 128/256 KiB for Artemis, 512/1024 KiB
for PRO, and planned 256/1024 KiB for Athena/base/server. Artemis and Athena now
share the same 128 KiB module for their 256 KiB systems. This uses **128 16K×1
chips per system**, versus 32 64K×1 chips in the former 16-bit-module design.
The unoffered 192 KiB expansion target is retired because it cannot be formed
from matched pairs of these modules. Original configuration IDs remain stable;
the module references and quantities, not ID spelling, specify their geometry.

`offer.ram_64kb_module` sells one 64 KiB module; it cannot populate a complete bank
alone. `offer.ram_256kb_bank` contains two 128 KiB modules. These are commercial
pack quantities pointing to the same physical module records, not duplicate
expansion hardware. Aurelia's `device.aurelia_ram_16kb_card` remains a separate
16 KiB, 8-bit slot card with its original eight-chip BOM.

The older prototype and explicitly superseded 8-bit Artemis records remain
historical/excluded records, not offered module alternatives. Their specifications
are not rewritten to pretend they were the new 32-bit design.

## References, archived costs and unknowns

Authored BOMs, host configurations, shared-controller requirements, Athena's
functional BOM and standalone offers use the new module identities. Exact merged
IDs redirect in `site/config/document.site_pages.json` (`record_redirects`),
including old Navigator bookmarks. Redirects are one-way identity migrations,
not a second category vocabulary or editable copy of product data.

Frozen baselines and saved financial assessments are unchanged. Revised assemblies
have `cost_assessment_status: pending_reassessment`; this status propagates through
nested BOMs in both the Navigator and computer configurators. Current costs are
shown as unknown and archived evaluations remain accessible. They must not be
combined with revised quantities. The cost builder stops before calculating or
publishing until revised module routing/allowances are qualified. It also handles
software editions lacking cost profiles explicitly, without inventing a profile.

The ecosystem-only pipeline is regenerated from current inputs so provenance
hashes remain valid; it does not rebuild sales, prices or ROI. Full numerical
reassessment remains pending, since the new connector, decoding, PCB/routing and
qualification costs are not known. A historical 16-bit-module allowance is not a
valid current 32-bit-module quotation.

## Verification

Source/schema/reference validation, module chip arithmetic, recursive hardware BOM
quantities, preserved system capacities, Athena functional BOM, software edition
membership and canonical categories are checked. Browser tests cover all three
computer configuration pages, Navigator filtering/tabs and merged-ID redirects.
Reviewed page snapshots reflect the requested edition names, shared modules,
retired target and explicit cost-reassessment state.

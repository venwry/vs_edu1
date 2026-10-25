# Software lines, editions and delivery compositions

Base commit: 73140502ff08ab63a58da86616a48fbe825b838d.

The 14 stored software-line records are removed with data/software-products.json.
All 32 editions now live in software-editions.json.software_editions (schema 4.0.0).
Each stores software_line_id, software_line_name and software_line_category. Labels
and categories must agree across each line. product_ref, sold_separately, delivery
and reverse physical_media_refs are no longer authoritative fields. Vendor inheritance
is materialized at each edition while explicit edition vendor overrides are preserved.
The line's membership and earliest introduction are derived. Existing software.product.*
links resolve to an in-memory group, not an arbitrary edition. Its displayed vendor
comes from the earliest encountered edition; that is not a separate supplier assertion.
The Model II FlexiBUS external product remains in ecosystem-inputs.json.

There are 21 authoritative collections. Legacy platform_editions/software_products
views are derived only. Python delegates projection to the same JS reader used by the
browser. Legacy edition/line writes are rejected; edit software_editions directly.
No catalogue generation step or replacement software-line JSON file is introduced.

## Physical fulfillment

Every edition has composition_history with standard dated versions and physical lines.
Products formerly attaching Business Tools as a bare software edition now attach its
physical cartridge in the application-cartridge socket; the edition is included once
through that device. Software distribution and installation requirements remain separate from licensing and
commercial prices. The two entertainment editions' former month-only June 1982 date
uses the existing NCC date convention, 1982-06-07, with an explicit precision note.

Cartridge devices contain hardware plus their software edition reference. Editions
own software documentation and a licence document; hardware shell/label/packaging
sets explicitly exclude those documents. Athena system-ROM devices likewise reference
AIONix 2 documentation. Device software_refs and edition physical_media_refs are not
stored. Source validation detects cycles spanning both devices and software, forbids
product nesting, and rejects adding software again beside its supplied cartridge.

Diskette editions own labelled/sleeved installation media, documentation, licence
documents and packaging. Physical disk counts are null until released images and
formats establish them. Unknown quantities do not become zero or a guessed disk count.
Model II Abacus retains its 8-inch format and Radio Shack/Tandy distribution channel.
CP/M Model II and Microsoft BASIC remain external compatibility entries with empty,
explicitly unresolved compositions: no Logix product, price or supplied-media claim.

Aurelia and Artemis SDKs contain printed reference/documentation sets and three logical
media groups: interfaces/libraries; sample code; utilities/conformance tests. Each group
has unresolved physical disk count. Compiler/IDE is a dependency, not duplicated in the
SDK. This is a platform supplement, not a promise of a complete development toolchain.
The historical comparison was Apple's January 1983 Lisa Pascal specification, which
lists development tools plus reference/workshop/system manuals:
https://bitsavers.trailing-edge.com/pdf/apple/brochures/Lisa/Pascal_Brochure_Jan83.pdf
That source does not establish media counts for these fictional SDKs.

## Server/client packages

Development Team and BPI each have one commercial software product containing server
and platform-specific client editions directly. Server installation media installs to
the HDD. Client startup media runs under the existing network-capable OS, connects to
the server and loads additional modules/data. The bootstrap remains local. No separate
client cartridge or duplicate OS licence is created. BPI database writes, business
logic and transaction handling remain on the server; clients do not modify shared
raw database files.

Server/client editions own their respective diskette groups and documentation sets.
The commercial package owns one licence certificate and one outer package. A media
set is distinct from a deployment copy, client licence or concurrent session.
Development Team preserves one server/four concurrent sessions and the existing
combined 12-disk/1000-page assumptions, plus 20-hour onboarding and 12-hour first-year
support. Server/client media/page allocations remain unresolved. Those totals are
stored once on the product; legacy software cost-assumption fields are derived therefrom.
BPI's standalone package leaves client seat count and disk allocation unqualified;
its restored office-system configurations preserve their existing two-client entitlement.

The existing computer-system products expand the relevant package's edition/material
lines directly, preserving the flat-product rule. This corrects the BPI server reference
(formerly the CP/M client ID). Each package includes distribution media for supported
platforms once; seat counts are held in commercial_terms, not media-line quantities.

## Commercial catalogue and calculation boundary

19 products are added: 17 standalone editions/cartridge deliveries, plus the Team and
BPI server/client packages. They use product.* IDs, category software and computer_line
null. No new price is invented. Separate sale is represented by these products; runtime
compatibility sold_separately is derived from standalone product contents, including
cartridge delivery. Individual package clients are not separately offered.
There are 63 products, 60 devices, 32 editions and 452 components (102 new media and
documentation components). The 14 single-computer selector choices are unchanged.

BOM Navigator traverses software physical compositions using the same assembly index
as devices. The runtime synthesizes 32 edition BOM owners and 19 software-product BOM
owners; none are stored as duplicate assembly records. Existing product assemblies now
include supplied software's physical delivery. Licence fees, services, entitlement and
NRE do not become physical manufacturing lines. General assembly consolidation and
production date-based selection remain deferred. Saved financial outputs/baselines
are byte-identical, so they do not claim newly rebuilt fulfillment costs.

Simulation includes software physical leaves. The 27 existing comparable versions
still agree with the updated runtime graph; the hypothetical November graphics revision
still adds two SRAM chips in one configuration. The report lists 28 distinct unknown
physical components, predominantly unallocated diskette groups. There are 44 versions
without a product-level legacy BOM/cost baseline. These remain explicitly unasserted.

## Validation

Run tools/validate_data.py, tests/validate_data_structure.py and
 tests/validate_software_delivery.py, plus migration audits and browser tests.
The new audit covers consistent line metadata, external exclusions, cartridge/software
cycles, duplicate software inclusion, SDK media groups, package entitlements, flat
products and immutable financial files. tests/fixtures/software-delivery.json validates
15 changed runtime owners and 51 new owners before older historical audits reconstruct
their original comparison view. Original historical fixtures remain unchanged.

Final verification: all 21 source collections, legacy schemas and migration audits
pass. Python validators: 24/43 pass, with the same 19 pre-existing failures. Browser
checks: 21/22 pass, retaining the existing atlas timeline pricing-link failure. All
14 reviewed page snapshots are refreshed for the approved source/delivery changes.

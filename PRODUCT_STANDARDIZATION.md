# Commercial product naming and categories

All 63 records in data/product-catalog.json.products use five categories:

| Category | Records | ID prefix |
| --- | ---: | --- |
| computer | 15 | product. |
| computer_software_bundle | 15 | product. |
| expansion_kit | 11 | product. |
| software | 19 | product. |
| computer_system | 3 | computer_system. |

A computer with peripherals/cartridges is computer. Separately included application
software in any composition version makes the record computer_software_bundle;
this includes the Budget products whose later versions include Abacus 3. Developer
packages with an SDK/compiler also use that category. Kits without a main computer
remain expansion_kit even when software is supplied (e.g. the AutoCAD upgrade).
Standalone software/cartridge products retain software. Multi-computer products
remain computer_system. No constituent quantities, release dates or version intervals
change in this migration.

42 existing IDs change prefix. References in source collections, consumers, builders
and tests use canonical IDs. Registry record_id_aliases retains old bookmarks and
archived model identities, including the earlier names of restored computer systems.
Saved financial JSON and frozen baselines are unchanged; the loader translates IDs
in memory. Computer configuration query parameters also resolve old product IDs.
Migration inventory fixtures apply the same identity-only translation; their stored
physical quantities and financial hashes remain unchanged.

record_kind and source_group are removed from source records and the schema.
They previously drove compatibility projections. Platform views now come directly
from base-computer devices and are never inserted into product_catalog.products.
For legacy list names, offered nonsoftware products populate offered_bundles;
planned/proposed computer products populate proposed_bundles; all remaining products
populate commercial_offerings. These are disjoint derived views based on category
and catalogue_status, not independent stored classifications. All 63 products occur
exactly once, including the two planned Athena products previously omitted from
these legacy commercial lists. The BOM Navigator consequently has 628 entries.

computer_line remains the sole configuration-dropdown membership rule: 4 Aurelia,
8 Artemis, 2 Athena products. Availability and qualification statuses are unchanged.
Validators enforce category/prefix agreement and computer/software classification.
Run tests/validate_product_standardization.py and the product, composition, Navigator
and computer-family suites. Refresh UI snapshots only for the intentional IDs,
category labels and removed redundant metadata; do not rebuild financial models.

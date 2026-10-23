# Technology and Trainings and Services navigators

The active site has 13 pages in four header sections. Software is no longer a header section. Standards & services contains Technology, Trainings and Services, and BOM Navigator.

`technology.html` collects the 22 remaining records from the retired domain pages: 21 technology/architecture standards and the TRS-80 Model II partner-platform configuration. The latter remains explicitly classified as External platform rather than being relabelled as a technology or lost during migration. Products already covered by BOM Navigator remain there.

`trainings-and-services.html` replaces Academy with its 15 unique training, support, licensing and certification records. BPI Products training (`service.bpi_training`) and custom-chip licensing/supply (`service.component_licensing`) appear once each; both already belonged to the Academy record set. The Academy capacity-plan link is retained.

Both pages share the BOM Navigator's full-width 50/50 layout, Name/Class/Category/Vendor/Release date table, combined filters and reset action. Their right panes contain Details and Related events tabs, with keyboard navigation and lazy panel rendering. Exact event product references determine related events. Unknown dates stay unknown. The pages fetch only the technical catalogue, story and site configuration; they do not load manufacturing models or BOMs. Query-string selections and legacy record hash anchors work on all three navigators.

Page membership and canonical record ownership are authored in `site/config/document.site_pages.json` and projected by `python tools/data_catalog.py`. No technical, service, event or financial source values were changed. No schema fields were added, and no financial builders were run.

The eight emptied domain pages and `academy.html` are removed from active navigation and page configuration. Following the requested cleanup, their HTML files are deleted; old incoming URLs are no longer served. Canonical record links still route to Technology, Trainings and Services, or BOM Navigator according to ownership. Static links and older aliases are rewritten to canonical destinations by `tools/build_site.py`.

Validation includes a frozen list of every record referenced by the nine retired pages, ensuring all remain available and that navigator memberships are disjoint. `tests/domain-navigators.test.cjs` checks every technology/service record and its event membership, filters, keyboard tabs, deep links, light data loading and retired-page absence. Site tests check the four header groups, all 13 primary pages, the index redirect and absence of all 22 retired pages and complete manufacturing-cost coverage. Canonical source/schema/reference checks and the existing cost-consolidation audit remain unchanged.

Validation run: canonical schemas/references, hardware BOMs, cost-preservation audit, both new navigators, BOM Navigator, site organisation and reviewed page-content snapshots pass. The pre-existing `atlas.test.cjs` assertion for the retired timeline `.site-nav` pricing link remains; it was not removed or weakened. Financial hashes and model outputs are untouched. Interaction checks use jsdom; a rendered browser was unavailable.

## Obsolete HTML cleanup

Removed the 22 retired root HTML documents and four unused fragments (`comdex-1982-artemis`, `comdex-1982-video-system`, `ncc-1982-video-system`, `ncc-1982-software-development`). The 13 active pages, index entry point, report templates, shared navigation, active timeline/pricing fragments and test navigation fixture remain. The legacy `redirects` mapping is retained as a build-time link-rewrite map; only index.html is emitted as a redirect. The site builder removes any retired page left by older stages, while NCC/COMDEX review builders no longer emit or read their obsolete reports.

No source facts, schemas, dates, estimates or financial outputs changed. Page snapshots drop only the 22 deliberately deleted pages; remaining-page content must still match.

## Navigator table sorting and vendors

All three navigators provide sortable buttons for all five column headers. Repeated clicks toggle ascending/descending order; text sorts naturally, dates use their recorded date strings, and Unknown values stay last. Sorting preserves the selected element, active tab and inspector contents. Reset clears filters and restores Name ascending. Header buttons are keyboard accessible and expose aria-sort.

Vendor filtering combines with Class, Category and Release date. Vendor attribution uses explicit vendor/provider/manufacturer/owner/publisher/developer/supplier strings, in that order, falling back to a linked product or catalogue record for editions and components. It never infers a vendor from a name, host computer or bundle contents; absent attribution is Unknown (including current service records). No canonical data or financial outputs change.

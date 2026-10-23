# Technology and Trainings and Services navigators

The active site has 13 pages in four header sections. Software is no longer a header section. Standards & services contains Technology, Trainings and Services, and BOM Navigator.

`technology.html` collects the 22 remaining records from the retired domain pages: 21 technology/architecture standards and the TRS-80 Model II partner-platform configuration. The latter remains explicitly classified as External platform rather than being relabelled as a technology or lost during migration. Products already covered by BOM Navigator remain there.

`trainings-and-services.html` replaces Academy with its 15 unique training, support, licensing and certification records. BPI Products training (`service.bpi_training`) and custom-chip licensing/supply (`service.component_licensing`) appear once each; both already belonged to the Academy record set. The Academy capacity-plan link is retained.

Both pages share the BOM Navigator's full-width 50/50 layout, Name/Class/Category/Release date table, combined filters and reset action. Their right panes contain Details and Related events tabs, with keyboard navigation and lazy panel rendering. Exact event product references determine related events. Unknown dates stay unknown. The pages fetch only the technical catalogue, story and site configuration; they do not load manufacturing models or BOMs. Query-string selections and legacy record hash anchors work on all three navigators.

Page membership and canonical record ownership are authored in `site/config/document.site_pages.json` and projected by `python tools/data_catalog.py`. No technical, service, event or financial source values were changed. No schema fields were added, and no financial builders were run.

The eight emptied domain pages and `academy.html` are removed from active navigation and page configuration. Their URLs remain redirect-only documents to preserve incoming links. Stable record anchors route directly to Technology, Trainings and Services, or BOM Navigator according to ownership. Static links and older aliases are rewritten to canonical destinations by `tools/build_site.py`.

Validation includes a frozen list of every record referenced by the nine retired pages, ensuring all remain available and that navigator memberships are disjoint. `tests/domain-navigators.test.cjs` checks every technology/service record and its event membership, filters, keyboard tabs, deep links, light data loading and retired-page redirects. Site tests check the four header groups, all 13 primary pages, 23 redirects and complete manufacturing-cost coverage. Canonical source/schema/reference checks and the existing cost-consolidation audit remain unchanged.

Validation run: canonical schemas/references, hardware BOMs, cost-preservation audit, both new navigators, BOM Navigator, site organisation and reviewed page-content snapshots pass. The pre-existing `atlas.test.cjs` assertion for the retired timeline `.site-nav` pricing link remains; it was not removed or weakened. Financial hashes and model outputs are untouched. Interaction checks use jsdom; a rendered browser was unavailable.

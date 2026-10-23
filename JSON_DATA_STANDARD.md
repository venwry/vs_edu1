# JSON schema and documentation standard

This document is the normative authoring contract for the Logix / AION project.
Read it before changing any data, schema, model or page. Record versions are specified
by each schema: **2.0.0** for components, BOM components, peripherals, computers,
software products and offers; other record types retain **1.0.0**.

## Ownership and directories

| Location | Owner and purpose |
| --- | --- |
| `data/world/` | Actors, premise, principles and world conventions |
| `data/hardware/` | Computers, chips/components, peripherals and configurations |
| `data/software/` | Operating systems, applications, development tools and platform editions |
| `data/standards/` | Shared architecture, ISA, ABI, API, interface and protocol definitions |
| `data/manufacturing/` | Physical BOMs, supplier parts, process recipes and qualification |
| `data/commercial/` | Offers, services, dated catalogues and contract terms |
| `data/timeline/` | Events, processes, phases, releases and market reactions |
| `data/marketing/` | Campaign messages, audience, demonstrations and execution plans |
| `data/business/` | Editable cost, demand, marketing, funding and investment assumptions |
| `data/programs/` | Coordination records linking work across domains |
| `data/evidence/` | Source evidence, review scope and unresolved decisions |
| `site/config/` | Page navigation, labels, record/page mappings and explorer layouts |
| `baselines/` | Frozen calibration and comparison inputs; never silently refresh |
| `generated/catalogs/` | Deterministic compatibility projections, never edit directly |
| `generated/models/` | Calculated financial and business outputs, never edit directly |
| `schemas/records/` | Typed record envelopes and domain payload field contracts |
| `schemas/documents/` | Strict owned-field contracts for split programme/input documents |
| `schemas/legacy/` | Existing rich story and BOM schemas, applied to assembled projections |
| `data/manifest.json` | Explicit source membership, order, ownership and legacy path mapping |

Create `data/scenarios/` when adding an independent alternate assumption set. Do not
copy the entire product catalogue to represent a financial scenario. Store its ID,
baseline references and explicit overrides. New directories must have an owner and
purpose documented here; do not create miscellaneous or temporary data buckets.

## Record envelope

Every authoritative record uses this envelope:

```json
{
  "$schema": "../../../schemas/records/computer.schema.json",
  "schema_version": "1.0.0",
  "id": "computer.aurelia",
  "record_type": "computer",
  "data": {
    "id": "computer.aurelia",
    "name": "Logix Aurelia"
  }
}
```

This is an envelope illustration; the complete computer payload must satisfy its
schema. `$schema` resolves relative to the record file. The wrapper ID identifies
its record; existing domain IDs inside `data` remain unchanged. BOM product links
have their own wrapper identity and retain `catalog_ref` to the technical product.
Split document sections share the original document identity but have disjoint
field ownership, identified by their paths.

Use UTF-8, two-space indentation and one trailing newline. Use `snake_case` keys.
Use lowercase filenames; preserve existing dotted IDs. New descriptive filenames
use hyphens. Never put schema revisions into a filename like `_v2`; the retained
legacy aggregate name is a compatibility exception, not an authoring precedent.

Separate `schema_version` from software version, hardware revision and in-world
effective dates. A breaking field/meaning change requires a new schema version,
a migration and consumer tests. Additive changes require an updated schema and
examples. Do not weaken a schema merely to make an invalid record pass.

## Compatibility payload policy

The directory migration deliberately preserves all original payload values and
array order. The common envelope is standardised; historical payload field names,
status prose, units and partial date formats remain losslessly represented in
`data`. They are not silently interpreted or rewritten. Shared narrative and BOM
schemas remain enforced, and record schemas constrain allowed payload fields.

For existing entities, use their domain schema's field names. A future conversion
of `ram_kb` to bytes, or of free-text status to enums, must be a documented semantic
migration, with explicit conversion rules and before/after display tests. Never
keep two editable fields representing the same fact. Newly introduced domains
must use the conventions below from the start.

## Identity and relationships

### Canonical product categories (version 2)

`category` describes function using one lowercase `snake_case` vocabulary enforced
by `schemas/category.schema.json`. It is not a display alias, record type, platform,
availability status or qualification status. The shared schema is registered locally
by `tools/schema_validation.py`; schema validation does not retrieve remote files.

For example a finished monitor uses `monitor`, its controller IC uses
`display_controller_ic`, and a host video card uses `video_expansion_card`. Previously
generic `catalog_component` and `unresolved_component` records now use functional
categories such as `printed_circuit_board`. Their unknown manufacturer, quantities,
prices and `qualification_status` remain unchanged.

Software editions inherit the parent product's category through `product_ref`; do
not add a second editable category to the edition. Linked BOM component categories
must match their `catalog_ref`. `catalog-categories.js` supplies explicit hardware
group predicates for consumers, without old-code aliases or a second label map.
Services, technologies and accounting categories are separate domains and are not
silently converted to the BOM product vocabulary.

`candidate_manufacturers`, when present on a BOM component, is an array of
`{name, basis}` objects identifying unqualified candidates. It never replaces a
null `manufacturer` or implies a procurement commitment. Vendor means the selling
brand/publisher; it does not automatically identify the physical manufacturer.

See `CATEGORY_MIGRATION.md` for conversion rules, affected sources and verification.

- Keep stable IDs such as `computer.aurelia`, `part.era1`, `actor.logix` and
  `event.artemis_launch`, even when names or paths change.
- Use `*_ref` and `*_refs` for domain relationships. Reference the authoritative ID,
  not a display label or file path. Keep source-file references in provenance.
- A software product and its platform edition are distinct. Editions own execution
  targets, platform support dates, dependencies and resource requirements.
- A computer design, manufactured assembly and commercial offer are distinct.
  Offers own included hardware/software/services; BOMs own physical quantities.
- An event references a campaign, offer or contract. It must not copy their full
  specification, terms or price calculation. Contract terms extracted from legacy
  events are projected back into their original event views automatically.
- Treat `used_by`, `used_in` and similar reverse lists as compatibility data until
  their owning schema is migrated. Do not add more manually maintained reverse
  relationships; derive them from forward references.
- Preserve independent partner ownership, commercial boundaries and licensing.
  A compatible Autodesk or Tandy product is not automatically a Logix product.

## Time, status and uncertainty

For new temporal types, use `start`, `end`, `precision` and `basis`; dates are
`YYYY`, `YYYY-MM`, `YYYY-MM-DD` or explicitly labelled `YYYY-Qn` periods. A month-only
date must not acquire an invented day. Specify inclusive/exclusive interval policy.
Separate announcement, demonstration, availability, shipment and withdrawal.

Calendar order and narrative order are independent. In particular, the protagonist's
2025 event may belong to an early narrative phase. Do not validate phase membership
by assuming all events lie inside the phase's calendar interval.

New status fields must separate editorial status (`proposed`, `accepted`,
`superseded`), engineering readiness (`design`, `qualification_pending`, `qualified`),
commercial availability and evidence basis (`historical_source`, `story_assumption`,
`engineering_estimate`, `model_result`). Preserve the original explanatory text.
Accepted fiction is not measured engineering evidence; a scenario estimate is not
an observed historical sale. Numerical uncertainty ranges need a stated method;
scenario envelopes are not statistical confidence intervals.

## Quantities, finance and unknowns

Use numeric values and unambiguous units. Prefer bytes for memory, Hz for clock
rates, mm² for die area and person-months for effort. Do not assume an existing
`kb` means decimal kilobytes; establish its intended meaning before conversion.

Money must carry currency, period/effective date, nominal/constant-price basis and
scope. Use `_usd` only where the enclosing record explicitly establishes nominal
USD and date basis. Rates use 0–1; fields ending `_pct` use 0–100. Never interchange
the two. Market share must specify units/revenue/installed-base denominator,
geography, segment and period. ROI definitions must distinguish the project's
existing accounting, cash and quarterly measures.

Use `null` for explicitly unknown values, not zero or `"TBD"`. An absent optional
field means not supplied; an empty array means known to contain no entries.
Unknown BOM quantities or prices must block a complete cost roll-up or produce an
explicit partial total. Preserve no-double-counting rules for OEM assemblies,
licences, support, royalties, capital and NRE.

## Manifest and compatibility views

`data/manifest.json` reconstructs the previous consumer-facing shapes:

- `{"$source": "data/...json"}` inserts a record's `data`.
- `{"$merge": [...]}` combines disjoint owned field groups. Duplicate keys fail.
- Lists explicitly preserve record and narrative order.
- `paths` maps old filenames to current projections, results, schemas or baselines.

`$source` and `$merge` are reserved assembly directives, not domain ID references.
A record must be registered once in the appropriate projection. Do not use directory
glob order as a product order. The compiler rejects cycles and overlapping ownership.
Never edit a compatibility projection or author both a source and a copied aggregate.

Run `python tools/data_catalog.py` after source changes. Commit the updated views
with their sources so the static HTML pages work without a server-side build.
`python tools/data_catalog.py --check` rejects stale views.

Existing financial snapshots retain old path strings in their provenance and text.
Resolve these through `paths`; do not change historical input hashes to pretend the
model was recalculated. New model runs record current input paths and hashes.

## Builders and calculated data

Data assembly does not recalculate prices, sales, costs or ROI. Those operations
can change the information displayed by the site and must be intentional.

The existing financial chain has base and reassessment stages. Its writers are
listed in `BUILD_PIPELINE.md`; use the declared orchestrator rather than running a
base-stage writer after the final reassessment. An output without its required
stage order is not an authoritative final result. The orchestrator stages calculations in an isolated checkout and publishes only
after all stages succeed. New stages must declare inputs,
outputs, predecessor stages, baseline/scenario and model version. New models should
write distinct stage outputs and publish the selected result once.

Legacy scripts that update authored data use `store_document` in `data_catalog.py`.
It distributes changes back to owned source fields, validates before writing, and
rebuilds projections. New identities/fields must be explicitly registered first;
the bridge refuses unknown record sets rather than losing new data.

Frozen baselines must remain immutable. A deliberate replacement is a new named
baseline with source commit, purpose, scenario, input hashes and rationale; update
its consumers explicitly. Generated reports must identify model, assumptions and
scope. Preserve archived outputs until a deliberate numerical rebuild.

## Documentation required for every change

A pull request must state:

1. Which facts or assumptions changed, and why.
2. Their authoritative source paths and affected IDs.
3. Whether the change is historical evidence, accepted story, proposal or estimate.
4. Effective dates, uncertainty and unresolved decisions.
5. Schema/version changes, conversion rules and affected consumers.
6. Builders run, generated outputs changed and validation results.

A new schema needs a purpose, required/optional fields, units, reference targets,
unknown-value rules and one realistic example. Put substantial explanations in
Markdown; retain concise machine-readable basis/notes with the relevant record.
Document external historical sources with URL/title and the specific supported
claim. Do not cite a source as support for fictional consequences or forecast factors.

## Required validation

Install `jsonschema` for Python and `jsdom@26.1.0` for Node. Then run:

```sh
python tools/data_catalog.py --check
python tests/validate_data_structure.py
node tests/page-content.test.cjs
node --test tests/*.test.cjs
```

Run relevant `tests/validate_*.py` domain checks as well. Some legacy checks already
fail at the migration baseline; `MIGRATION_VALIDATION.md` records them. Do not erase
assertions to hide failures. New failures must be resolved or explicitly explained.

`tools/check_migration.py` is a one-time losslessness audit against the source commit,
not a permanent prohibition on intentional data edits. Likewise, update page-content
fixtures only when an intentional content/UI change has been reviewed; never refresh
snapshots simply to hide a reorganisation regression. The fixture normalises moved
JSON paths but preserves visible content, tables and link targets.

## Site organisation additions

`navigation_sections` contains ordered `{title, page_refs}` groups; each page ID
must exist in `pages` and appear exactly once. `navigation` is the matching flattened
order. `redirects` maps retired relative HTML paths to canonical destinations.
`record_page_links` gives the primary page ID for a stable technical record ID;
shared details may appear elsewhere but links resolve to the primary owner.
`campaign_groups` associates an `event_ref`, dated `step_refs`, and a relative
`content_path`. Grouping is presentation-only: never delete the underlying events.
Computer page `model_refs` identify selectable models, not newly invented variants.
These are additive version-1 fields; schemas and consumers are updated together.

The ecosystem policy's `compatibility_pool` documents annual discoverable-family
assumptions, scenario qualification fractions, lag, counting and sales treatment,
partner support and historical-source claims. Counts are distinct application
families; fractions are 0–1 and lag is quarters. Named examples, qualified families,
native editions and paid licences must remain separate concepts. See
`HTML_ORGANIZATION.md` for ownership, formulas and maintenance commands.

# Google Business Profile categories — DEFERRED in v0.2

This document reserves the path `taxonomy/gbp-categories.json` for a future
protocol revision. **The data file is intentionally absent from v0.2.**

---

## Intended schema

When `gbp-categories.json` is added, it will use this shape:

```json
{
  "version": "<source-list version or fetch date>",
  "source": "<upstream provider, e.g. PlePer>",
  "source_url": "<URL of the export tool or list>",
  "generated_on": "YYYY-MM-DD",
  "count": <int>,
  "entries": [
    {
      "gbp_id": "gcid:full_service_restaurant",
      "name": "Restaurant",
      "parent_path": ["Food and Drink", "Restaurants"],
      "parent_naics_code": null
    }
  ]
}
```

Field semantics:

- **`gbp_id`** — Google's `gcid:` identifier for the category. Stable
  identifier; prefer over `name` for machine matching.
- **`name`** — Human-readable category name as Google displays it. Subject
  to change; not a stable key.
- **`parent_path`** — Google's own breadcrumb (top-level category → leaf).
  Useful for grouping in pickers without requiring a NAICS map.
- **`parent_naics_code`** — `null` in the initial release. See below.

## Why no NAICS mapping?

There is no authoritative GBP→NAICS mapping. Google does not publish one
and none of the third-party category lists (PlePer, Sterling Sky,
BlueShift) include NAICS codes. We declined to stamp a heuristic mapping
with the protocol's authority — see `README.md` in this directory for the
longer rationale.

Implementations needing a sector rollup should derive it from `naics_code`
(required on every manifest), not from the GBP category.

## Why no data file in v0.2?

Original v0.2 plan was to source GBP categories from PlePer Tools,
Sterling Sky, or a similar publicly-maintained list. As of the v0.2
authoring date (2026-04-27):

- **PlePer's tool** is live and current but offers no machine-readable
  download — only HTML tables intended for copy-paste into a spreadsheet.
- **Sterling Sky's "Ultimate List" page returns 404.** It appears to have
  been retired.
- **No GitHub repository carrying a current, maintained list was located.**
  The most-recent candidate (`adviceinteractivegroup/gmb_categories`)
  was last updated in 2018 and is too stale to ship as authoritative
  protocol data.

Rather than vendor an obviously-outdated list, v0.2 ships the schema
field (`business.gbp_primary_category`) as a free string with no enum
constraint. The protocol does not block on a categorization file that
isn't blocking the architecture.

## Plan for v0.3

A maintainer pulls the current category list from PlePer's export tool
(~10 minutes of human work — open the tool, select EN/US, copy the
TSV, paste into a file). A small script in `scripts/` parses the TSV
into the JSON shape above. The file lands at `taxonomy/gbp-categories.json`.

At that point, `business.gbp_primary_category` *may* tighten to enum
validation against `gbp_id` values — but only if upstream data quality
proves stable enough. Otherwise the field stays free-string with the
data file used as a discovery aid only.

Community PRs adding the data file are welcome at any time.

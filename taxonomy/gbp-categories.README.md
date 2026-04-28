# Google Business Profile categories

This file ships the Google Business Profile (GBP) category list as a
discovery aid for the protocol's `business.gbp_primary_category` and
`business.gbp_secondary_categories` fields.

- **Data file:** [`gbp-categories.json`](./gbp-categories.json)
- **Source TSV (vendored):** [`sources/gbp-pleper-2026-04-28.tsv`](./sources/gbp-pleper-2026-04-28.tsv)
- **Snapshot:** GBP categories — Apr 2026 snapshot
- **Source:** [PlePer Tools — GBP Categories](https://pleper.com/index.php?do=tools&sdo=gmb_categories)
  (English / USA), fetched 2026-04-28
- **Build script:** [`../scripts/build-gbp.py`](../scripts/build-gbp.py)

---

## Shape

The file is a bare JSON array of category entries, sorted by `gcid`:

```json
[
  {
    "gcid": "pizza_restaurant",
    "name": "Pizza restaurant",
    "parent_naics_code": null,
    "parent_path": null
  }
]
```

Field semantics:

- **`gcid`** — Google's category identifier (the value following the
  `gcid:` prefix in Google's APIs). Stable identifier; prefer over
  `name` for machine matching.
- **`name`** — Human-readable category name as Google currently
  displays it. Subject to change; not a stable key.
- **`parent_naics_code`** — Reserved. `null` on every entry today.
- **`parent_path`** — Reserved. `null` on every entry today.

`parent_naics_code` and `parent_path` are reserved for a future revision
that ships authoritative mappings. They stay `null` here because no
authoritative GBP→NAICS mapping exists, and PlePer's export does not
carry Google's breadcrumb paths.

## How to use

The v0.2 schema treats `business.gbp_primary_category` as a free
string — the schema does **not** enforce membership in this list.
Consumers who want to validate it can do so locally against
`gcid` values:

```python
import json
gcids = {e["gcid"] for e in json.load(open("taxonomy/gbp-categories.json"))}
assert manifest["business"]["gbp_primary_category"] in gcids
```

The same check works for every entry of `business.gbp_secondary_categories`.

Treating this file as a discovery aid (not a hard constraint) is
deliberate: GBP categories evolve roughly monthly, and breaking a
producer's manifest because Google added or renamed a category would
be a poor tradeoff in v0.2. v0.3 is the planned point at which the
schema may tighten `gbp_primary_category` to enum validation against
this list — alongside other breaking changes — once upstream data
quality proves stable enough.

## Why no NAICS mapping?

There is no authoritative GBP→NAICS mapping. Google does not publish
one and none of the third-party category lists (PlePer, Sterling Sky,
BlueShift) include NAICS codes. We declined to stamp a heuristic
mapping with the protocol's authority — see [`README.md`](./README.md)
in this directory for the longer rationale.

Implementations needing a sector rollup should derive it from
`naics_code` (required on every manifest), not from the GBP category.

## Refreshing the snapshot

GBP categories evolve. To refresh:

1. Open [PlePer's tool](https://pleper.com/index.php?do=tools&sdo=gmb_categories)
   with EN / USA selected and copy the table to a `.tsv` file. The
   file must have a `GCID<TAB>Category` header.
2. Save it at `taxonomy/sources/gbp-pleper-<YYYY-MM-DD>.tsv`.
3. Run the build:

   ```sh
   GBP_TSV=taxonomy/sources/gbp-pleper-<YYYY-MM-DD>.tsv \
   GBP_SNAPSHOT=<YYYY-MM-DD> \
       python3 scripts/build-gbp.py
   ```

4. Update the dates and snapshot label at the top of this README.
5. Diff `taxonomy/gbp-categories.json` to see what Google added,
   removed, or renamed. Note any meaningful churn in `CHANGELOG.md`.

Community PRs refreshing the snapshot are welcome at any time.

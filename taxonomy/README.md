# Taxonomy

Industry classification reference data used by the Nod protocol.

These files are intentionally vendored into the protocol repo (rather than
fetched at runtime) so that a given protocol version pins a specific
classification snapshot. Implementations read them as-is.

---

## Files

### `naics-2022.json`

The full North American Industry Classification System (NAICS), 2022 revision,
as a flat array of entries with explicit parent links.

- **Source:** US Census Bureau, https://www.census.gov/naics/
- **Source files:**
  - https://www.census.gov/naics/2022NAICS/2-6%20digit_2022_Codes.xlsx
  - https://www.census.gov/naics/2022NAICS/2022_NAICS_Descriptions.xlsx
- **Entries:** 2,125 across five levels:
  - `sector` (20) — 2-digit codes, e.g. `54` Professional Services. Three
    sectors are published as ranges (`31-33` Manufacturing, `44-45` Retail
    Trade, `48-49` Transportation and Warehousing); these appear as their
    range strings.
  - `subsector` (96) — 3-digit codes
  - `industry-group` (308) — 4-digit codes
  - `industry` (689) — 5-digit codes
  - `national-industry` (1,012) — 6-digit codes (US-specific)

#### Schema

```json
{
  "version": "NAICS 2022",
  "source": "US Census Bureau",
  "source_url": "https://www.census.gov/naics/",
  "source_files": [...],
  "generated_on": "2026-04-27",
  "count": 2125,
  "levels": ["sector", "subsector", "industry-group", "industry", "national-industry"],
  "entries": [
    {
      "code": "722511",
      "title": "Full-Service Restaurants",
      "parent_code": "72251",
      "level": "national-industry",
      "description": "This industry comprises establishments primarily engaged in providing food services to patrons who order and are served while seated..."
    }
  ]
}
```

`parent_code` is `null` for sectors. Entries whose Census description was
just `"See industry description for X."` (common for 5-digit `industry`
rows that delegate to a single 6-digit child) have been resolved to the
child's description.

#### How to update

When Census publishes a new NAICS revision (next expected: NAICS 2027):

1. Update the source URLs in `scripts/build-naics.py` (Census version path
   in particular — they change with each revision).
2. Re-run the parser, replacing this file:
   ```sh
   pip install openpyxl
   curl -sSL -o /tmp/naics-codes.xlsx 'https://www.census.gov/naics/<NEW>/...'
   curl -sSL -o /tmp/naics-descs.xlsx 'https://www.census.gov/naics/<NEW>/...'
   NAICS_CODES=/tmp/naics-codes.xlsx NAICS_DESCS=/tmp/naics-descs.xlsx \
     python3 scripts/build-naics.py
   ```
3. Bump the protocol version — adding/removing/renaming codes is a breaking
   change for any merchant whose `naics_code` is removed or whose
   classification path shifts.

---

### `gbp-categories.json` — DEFERRED in v0.2

The path is reserved for Google Business Profile categories, but **no data
file ships with v0.2**. See `gbp-categories.README.md` in this directory
for the intended schema, the reason no current authoritative source could
be vendored, and the v0.3 plan to populate it.

In v0.2, `business.gbp_primary_category` is a free string with no enum
constraint.

---

## License

Census NAICS data is in the public domain (US government work).

When the GBP category file is added in a future revision, the structured
list will be licensed under the same terms as the rest of this repo
(MIT — see `/LICENSE`); category names themselves are factual descriptors
not subject to copyright.

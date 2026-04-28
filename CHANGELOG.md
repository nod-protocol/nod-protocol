# Changelog

All notable changes to the nod protocol are documented here. Format
loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

The protocol version is defined in [`VERSION`](VERSION) at the repo
root and enforced by [`tests/check_consistency.py`](tests/check_consistency.py).

---

## [0.2] — 2026-04-27

**Breaking change.** Architectural restructure into a layered model.
Existing v0.1 manifests will not validate against the v0.2 schema and
must be migrated.

### Why

The v0.1 schema embedded an ad-hoc 12-value `business.type` enum that
could not represent the actual diversity of businesses, and mixed
business identity with the agent-commerce surface in the same top-level
namespace. v0.2 separates the two:

- **Core** describes the business's identity, classification, locations,
  and contact info — universal across all businesses.
- **The `ai.opennod.agent-commerce` extension** carries the agent
  contract — discovery, transactions, information, support, and
  policies. Adopting this extension is what makes a manifest agent-ready.

Classification moves to industry-standard taxonomies: NAICS 2022 for
the canonical industry code (vendored at `taxonomy/naics-2022.json`)
and Google Business Profile categories for the consumer-facing
taxonomy (path reserved at `taxonomy/gbp-categories.json`; see
`taxonomy/gbp-categories.README.md` for the v0.2 deferral).

Industry-specific fields (`servesCuisine` for restaurants,
`medicalSpecialty` for clinics, etc.) move to the new
`ai.opennod.schema-org-extension` extension which adopts Schema.org's
LocalBusiness subtype vocabulary directly rather than inventing
parallel field names.

### Added

- `taxonomy/naics-2022.json` — full NAICS 2022 hierarchy (2,125
  entries, 5 levels) sourced from US Census Bureau XLSX files.
- `scripts/build-naics.py` — reproducible parser for the NAICS source files.
- `taxonomy/gbp-categories.README.md` — schema and rationale for the
  intentionally-deferred GBP category file.
- `extensions/agent-commerce/v0.1.json` + README — the full
  agent-commerce extension schema.
- `extensions/merchant-voice/v0.1.json` + README — narrative layer
  (positioning, ideal customer, story, specialties, accommodations).
- `extensions/schema-org-bridge/v0.1.json` + README — meta-schema for
  declaring a Schema.org LocalBusiness subtype and its inline properties.
- `business.naics_code` (string, required) on the core schema.
- `business.gbp_primary_category` (string, required) on the core schema.
- `business.gbp_secondary_categories` (string[], optional) on the core schema.
- `business.dba_names` (string[], optional) on the core schema.
- `tests/check_consistency.py` — drift-detection test enforcing
  agreement between `VERSION`, schema's `nod_version` const, and every
  example's `nod_version`.

### Changed (breaking)

| v0.1 location | v0.2 location |
|---|---|
| top-level `discovery` | `extensions["ai.opennod.agent-commerce"].discovery` |
| top-level `transactions` | `extensions["ai.opennod.agent-commerce"].transactions` |
| top-level `information` | `extensions["ai.opennod.agent-commerce"].information` |
| top-level `support` | `extensions["ai.opennod.agent-commerce"].support` |
| top-level `agent_policies` | `extensions["ai.opennod.agent-commerce"].policies` |
| `transactions.policies` (returns/cancellation/etc.) | `extensions["ai.opennod.agent-commerce"].transactions.transaction_policies` |
| `agent_policies.require_human_confirmation` | `extensions["ai.opennod.agent-commerce"].policies.confirmation_requirements` |
| `transactions.purchase.payment_methods` (string[]) | `extensions["ai.opennod.agent-commerce"].transactions.purchase.payment_methods` (object[] — `rail`, `agent_endpoint`, `currencies`, `min/max_amount`, `settlement_window`) |
| `business.type` (12-value enum) | **removed.** Use `business.naics_code` + `business.gbp_primary_category`. |
| `business.naics_codes` (string[]) | **replaced by** `business.naics_code` (string, singular, required). For multiple codes, use one primary `naics_code` and optionally enumerate others under `categories`. |
| `nod_version: "0.1"` | `nod_version: "0.2"` |
| `$schema: "...nod/v0.1.json"` | `$schema: "...nod/v0.2.json"` |

### Migration notes

- The protocol is still pre-1.0; no stability commitments yet apply.
  v1.0 will lock breaking changes behind MAJOR bumps.
- Existing v0.1 manifests will need their data migrated. The mapping
  table above is mechanical for most fields; the `payment_methods`
  conversion (string → object) is the one transformation that requires
  judgment about which rails are agent-friendly.
- Industry extensions like `ai.opennod.restaurant` from v0.1 are
  preserved for backward compatibility but new manifests SHOULD use
  `ai.opennod.schema-org-extension` instead.
- The GBP→NAICS mapping is intentionally not shipped in v0.2. See
  `taxonomy/gbp-categories.README.md`.

### Removed

- `business.type` (12-value enum). Industry classification now uses
  NAICS + GBP.
- `business.naics_codes` (array). Replaced by singular required
  `naics_code` plus optional secondary categories.

---

## [0.1] — 2026-03-23

Initial public draft of the protocol. See
[`spec/nod-protocol-v0.1.md`](spec/nod-protocol-v0.1.md), preserved
as historical reference.

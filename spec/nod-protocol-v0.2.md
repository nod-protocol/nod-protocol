# nod Protocol Specification v0.2

**Status:** Draft
**Version:** 0.2.0
**Date:** 2026-04-27
**Authors:** OpenNOD
**License:** MIT

> The protocol version is defined in [`/VERSION`](../VERSION) at the repo root. Do not change it elsewhere. Tests in [`tests/check_consistency.py`](../tests/check_consistency.py) enforce that VERSION, schema's `nod_version` const, and every example's `nod_version` agree.

> v0.2 is a **breaking change** from v0.1. See [`CHANGELOG.md`](../CHANGELOG.md) for the migration table and rationale. The v0.1 spec is preserved at [`spec/nod-protocol-v0.1.md`](nod-protocol-v0.1.md) for historical reference.

---

## 1. Introduction

### 1.1 Purpose

The nod (Notarized Object Declaration) protocol defines a machine-readable
format for businesses to declare what they are and how AI agents may
transact with them. A nod manifest lives at `/.well-known/nod.json` on
the merchant's domain.

### 1.2 What changed in v0.2

v0.2 introduces a **layered architecture** that separates the merchant's
identity from the agent contract:

- **Core manifest** — describes the *business*: identity, classification,
  locations, contact info, hours. Universal across every business,
  agent-aware or not.
- **`ai.opennod.agent-commerce` extension** — describes the *agent
  contract*: discovery, transactions, real-time information, support
  interfaces, and the policies governing all of it. A manifest *with*
  this extension is agent-ready; one without it just describes a
  business.
- **`ai.opennod.schema-org-extension` extension** — declares which
  Schema.org `LocalBusiness` subtype applies and supplies that subtype's
  industry-specific properties (`servesCuisine`, `acceptsReservations`,
  `medicalSpecialty`, etc.).
- **`ai.opennod.merchant-voice` extension** — narrative / positioning /
  specialties for merchant differentiation.

OpenNOD's distinctive contribution is the agent-commerce layer. We adopt
NAICS for industry classification, Schema.org subtypes for
industry-specific fields, and define agent-commerce primitives in our
own extension.

### 1.3 Design principles

1. **Agent-first** — every field exists because an agent needs it, not
   because a human developer finds it elegant.
2. **Adopt, don't reinvent** — NAICS for classification, Schema.org for
   industry-specific shape, MCP / OpenAPI / GraphQL for interfaces.
   OpenNOD only adds what those standards don't cover.
3. **Layered** — core describes business identity; extensions describe
   capability layers. A merchant adopts each layer independently.
4. **Discoverable** — `/.well-known/nod.json` plus optional `<link>` tag
   plus optional DNS TXT record.
5. **Validatable** — every artifact in this repo is checked for internal
   consistency by `tests/check_consistency.py`.

### 1.4 Relationship to existing standards

| Standard | Role in nod v0.2 |
|---|---|
| **NAICS 2022** | Required `business.naics_code` classifies the business. Full taxonomy vendored at `taxonomy/naics-2022.json`. |
| **Google Business Profile categories** | Required `business.gbp_primary_category` for the consumer-facing taxonomy merchants are familiar with. v0.2 ships free-string only — see `taxonomy/gbp-categories.README.md`. |
| **Schema.org LocalBusiness subtypes** | Industry-specific fields use Schema.org property names via the schema-org-bridge extension. We do not redefine restaurant, hotel, medical, retail vocabularies — Schema.org already has them. |
| **JSON-LD / `business.schema_org`** | The core manifest may link to a separate JSON-LD document at `business.schema_org`. Distinct from inline Schema.org properties in the bridge extension. |
| **OpenAPI / GraphQL / MCP** | Referenced by URL inside the agent-commerce extension's `discovery` block. Not redefined. |
| **robots.txt / sitemap.xml** | Complementary. nod adds agent-specific declarations; robots.txt and sitemap.xml retain their roles. |
| **llms.txt** | Complementary. llms.txt is the *informational* layer (what the site is/contains); nod is the *transactional* layer (what agents can do). |

---

## 2. Manifest discovery

Unchanged from v0.1.

### 2.1 Well-known URL

```
https://{domain}/.well-known/nod.json
```

Agents MUST check this URL first. Fallbacks: `/nod.json`, an HTML
`<link rel="nod-manifest">` tag, or a DNS TXT record at
`_nod.{domain}`.

### 2.2 Content type

Served as `Content-Type: application/json` with
`Access-Control-Allow-Origin: *`.

---

## 3. Core manifest schema

### 3.1 Root object

```json
{
  "$schema": "https://opennod.ai/schema/nod/v0.2.json",
  "nod_version": "0.2",
  "generated_at": "2026-04-27T12:00:00Z",
  "business": { ... },
  "extensions": {
    "ai.opennod.agent-commerce": { ... },
    "ai.opennod.schema-org-extension": { ... },
    "ai.opennod.merchant-voice": { ... }
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `$schema` | URI | RECOMMENDED | URL of the JSON Schema. |
| `nod_version` | string | REQUIRED | Must equal `"0.2"`. |
| `generated_at` | ISO 8601 datetime | REQUIRED | When this manifest was last generated. |
| `business` | object | REQUIRED | Core business identity. See §3.2. |
| `extensions` | object | OPTIONAL | Reverse-domain-namespaced extensions. See §4. |

### 3.2 `business` object

The `business` object is the core. Only four fields are required:

- `name` — business name
- `naics_code` — primary NAICS 2022 industry code
- `gbp_primary_category` — primary Google Business Profile category
- `url` — primary business URL

#### Identity

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | REQUIRED | Customer-facing business name. |
| `legal_name` | string | OPTIONAL | Legal entity name. |
| `dba_names` | string[] | OPTIONAL | Doing-business-as names. |
| `description` | string | OPTIONAL | Plain-language description of what the business does. |
| `founded` | string | OPTIONAL | Year (or full date) the business was founded. |
| `logo` | URI | OPTIONAL | Logo image URL. |
| `url` | URI | REQUIRED | Primary business URL — must match the serving domain. |

#### Classification

| Field | Type | Required | Description |
|---|---|---|---|
| `naics_code` | string | REQUIRED | Primary NAICS 2022 code. Pattern: `^(\d{2,6}\|31-33\|44-45\|48-49)$`. Use the most specific applicable code (typically 6-digit national-industry). The full taxonomy is at `taxonomy/naics-2022.json`. |
| `gbp_primary_category` | string | REQUIRED | Primary GBP category. v0.2 accepts free string with no enum constraint pending an authoritative GBP list (see `taxonomy/gbp-categories.README.md`). A future protocol revision may tighten to enum-validated. |
| `gbp_secondary_categories` | string[] | OPTIONAL | Additional GBP categories in priority order. |
| `categories` | string[] | OPTIONAL | Free-form category tags (distinct from NAICS and GBP). |

#### Location and contact

| Field | Type | Required | Description |
|---|---|---|---|
| `locations` | location[] | OPTIONAL | Physical and/or virtual locations. Each location carries address, coordinates, hours, and per-location contact. |
| `contacts` | object | OPTIONAL | Contact channels keyed by purpose (`general`, `support`, `press`, …). |
| `social` | object | OPTIONAL | Social media profile URLs keyed by network. |

#### Trust and identifiers

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_org` | URI | OPTIONAL | URL to a Schema.org JSON-LD document. Distinct from inline Schema.org properties in the `ai.opennod.schema-org-extension` extension. |
| `identifiers` | object | OPTIONAL | DUNS, EIN, LEI, etc. |

### 3.3 What is no longer in core

These v0.1 top-level fields have moved to the `ai.opennod.agent-commerce`
extension:

| v0.1 location | v0.2 location |
|---|---|
| `discovery` | `extensions["ai.opennod.agent-commerce"].discovery` |
| `transactions` | `extensions["ai.opennod.agent-commerce"].transactions` |
| `information` | `extensions["ai.opennod.agent-commerce"].information` |
| `support` | `extensions["ai.opennod.agent-commerce"].support` |
| `agent_policies` | `extensions["ai.opennod.agent-commerce"].policies` |
| `transactions.policies` (inner) | `extensions["ai.opennod.agent-commerce"].transactions.transaction_policies` |
| `agent_policies.require_human_confirmation` | `extensions["ai.opennod.agent-commerce"].policies.confirmation_requirements` |

`business.type` (the v0.1 enum) is **removed** — replaced by
`naics_code` + `gbp_primary_category`.

`business.naics_codes` (plural array) is **replaced** by `naics_code`
(singular, required) plus optional `gbp_secondary_categories`.

---

## 4. Extensions

Extensions use reverse-domain namespacing. Three are defined by this
protocol revision; merchants MAY add their own under any namespace.

### 4.1 `ai.opennod.agent-commerce` (REQUIRED for agent-ready merchants)

The full agent-commerce surface — discovery, transactions, information,
support, policies, plus authorization_levels, automated_booking_capabilities,
and notes. This is OpenNOD's distinctive contribution.

Schema: [`extensions/agent-commerce/v0.1.json`](../extensions/agent-commerce/v0.1.json).
Documentation: [`extensions/agent-commerce/README.md`](../extensions/agent-commerce/README.md).

A merchant *without* this extension publishes a directory listing — they
have not opted into agent commerce.

### 4.2 `ai.opennod.schema-org-extension` (RECOMMENDED)

Declares a Schema.org `LocalBusiness` subtype and supplies its
industry-specific properties. Replaces the v0.1 ad-hoc industry
extensions (`ai.opennod.restaurant`, `ai.opennod.hotel`, …) for new
manifests.

Schema: [`extensions/schema-org-bridge/v0.1.json`](../extensions/schema-org-bridge/v0.1.json).
Documentation: [`extensions/schema-org-bridge/README.md`](../extensions/schema-org-bridge/README.md).

### 4.3 `ai.opennod.merchant-voice` (OPTIONAL)

Narrative fields: positioning, ideal customer, story, specialties,
accommodations.

Schema: [`extensions/merchant-voice/v0.1.json`](../extensions/merchant-voice/v0.1.json).
Documentation: [`extensions/merchant-voice/README.md`](../extensions/merchant-voice/README.md).

### 4.4 Custom extensions

Merchants and platforms MAY add extensions under any namespace
(reverse-domain recommended). Consumers MUST ignore unknown extension
keys gracefully.

---

## 5. Validation rules

### 5.1 Required fields

A valid v0.2 manifest MUST contain:

1. `nod_version` — must equal `"0.2"`
2. `generated_at` — valid ISO 8601 datetime
3. `business.name` — non-empty
4. `business.naics_code` — matches the NAICS pattern (§3.2)
5. `business.gbp_primary_category` — non-empty string
6. `business.url` — valid URI matching the serving domain

### 5.2 Conditional requirements

These apply when the named extension is present:

- `extensions["ai.opennod.agent-commerce"]` — see [`extensions/agent-commerce/README.md`](../extensions/agent-commerce/README.md) for inner conditional requirements.
- `extensions["ai.opennod.schema-org-extension"]` — `schema_org_type` and `properties` are both required.

### 5.3 URI validation

All URIs MUST use HTTPS (except localhost during development) and be
absolute at the root level. Relative URIs are permitted within nested
objects.

### 5.4 Freshness

`generated_at` SHOULD be within the last 30 days. Manifests older than
90 days SHOULD be treated as potentially stale.

---

## 6. Versioning

Semantic: `MAJOR.MINOR`. v0.2's increment is MINOR but the changes are
breaking — the protocol is still pre-1.0 and stability commitments do
not yet apply. v1.0 will lock breaking changes behind MAJOR bumps.

When reading a manifest, agents SHOULD:
1. Read `nod_version` first.
2. Process all fields they understand.
3. Ignore unknown fields and unknown extensions.
4. Never fail on unexpected data.

---

## 7. Conformance levels

| Level | Required artifacts |
|---|---|
| **L1: Declarative** | Valid v0.2 core manifest. Agents can describe the business. |
| **L2: Discoverable** | + `ai.opennod.agent-commerce` extension with `discovery.catalog` or `discovery.search`. |
| **L3: Queryable** | + `ai.opennod.agent-commerce.information` endpoints. |
| **L4: Transactable** | + `ai.opennod.agent-commerce.transactions` with at least one capability. |
| **L5: Agent-native** | + MCP server, webhooks, real-time APIs, `authorization_levels` declared. |

---

## 8. Security considerations

Unchanged from v0.1.

The manifest MUST NOT contain customer personal data, internal
credentials, proprietary business intelligence, or anything not intended
for public consumption.

Businesses SHOULD implement rate limiting on all agent-facing endpoints,
monitor for unusual access patterns, maintain the ability to revoke
agent access, and log agent interactions for audit.

---

## Appendix A: Complete field reference

The JSON Schema at [`schema/schema.json`](../schema/schema.json) is the
authoritative core reference. Extension schemas live under
[`extensions/`](../extensions/).

## Appendix B: Migration from v0.1

See [`CHANGELOG.md`](../CHANGELOG.md) for a complete migration table.

## Appendix C: Glossary

| Term | Definition |
|---|---|
| **Agent** | An AI system acting on behalf of a human user. |
| **Manifest** | The nod.json file declaring a business's agent-facing capabilities. |
| **Core** | The fields defined directly in `schema/schema.json` (identity, classification, locations, contacts). |
| **Extension** | An optional, namespaced object under `extensions[]` adding capabilities or fields beyond core. |
| **NAICS** | North American Industry Classification System. The US/Canada/Mexico government industry taxonomy. |
| **GBP** | Google Business Profile. Google's consumer-facing business category taxonomy. |
| **Schema.org `LocalBusiness`** | The W3C-published vocabulary for business data; subtypes like `Restaurant` or `MedicalBusiness` add industry-specific properties. |
| **MCP** | Model Context Protocol — Anthropic's protocol for AI-tool communication. |

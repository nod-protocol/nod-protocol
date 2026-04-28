# Agent-Commerce Extension

**Manifest key:** `extensions["ai.opennod.agent-commerce"]`
**Schema:** [`v0.1.json`](./v0.1.json) — `https://opennod.ai/schema/extensions/agent-commerce/v0.1.json`
**Status:** v0.1, evolving.

---

## Purpose

This extension is the full agent-commerce surface of a nod manifest:
**everything about how an agent interacts with the merchant**, in one
place. Discovery, transactions, real-time information, support
interfaces, and the policies governing those interactions all live here.

The split with core is intentional and load-bearing:

- **Core nod manifest** — the merchant's identity, classification (NAICS,
  GBP), addresses, contact info, hours, basic metadata. Universal across
  every business, agent-aware or not.
- **`ai.opennod.agent-commerce` extension** — the agent contract. A
  manifest without this extension describes a business; a manifest with
  this extension describes a business that's ready to be transacted with
  by agents.

Adopting this extension is what makes a nod manifest agent-ready. It is
OpenNOD's distinctive contribution on top of the open standards we adopt
(NAICS for classification, Schema.org via the schema-org-bridge extension
for industry-specific fields).

## Top-level shape

```
extensions["ai.opennod.agent-commerce"] = {
  policies:                          {...},     // rules: rate limits, auth, confirmation, data usage
  discovery:                         {...},     // catalog, search, MCP, feeds
  transactions:                      {...},     // purchase, booking, subscription, etc.
  information:                       {...},     // inventory, pricing, hours, reviews, FAQ endpoints
  support:                           {...},     // order tracking, returns, contact, webhooks
  authorization_levels:              {...},     // per-action authorization matrix
  automated_booking_capabilities:    [...],     // per-service-type booking config
  notes:                             "..."      // free-text agent guidance
}
```

The first five (`policies`, `discovery`, `transactions`, `information`,
`support`) are migrated from the v0.1 core schema's top-level fields and
are structurally compatible apart from one rename: the inner returns/
cancellation/price-match block (formerly `transactions.policies`) is
renamed to **`transactions.transaction_policies`** to avoid clashing
with the new top-level `policies` block.

The last three are net-new in v0.2 of the protocol.

## What changed from v0.1 of the protocol

If you are migrating from a v0.1 manifest:

| v0.1 location | v0.2 location |
|---|---|
| top-level `discovery` | `extensions["ai.opennod.agent-commerce"].discovery` |
| top-level `transactions` | `extensions["ai.opennod.agent-commerce"].transactions` |
| top-level `information` | `extensions["ai.opennod.agent-commerce"].information` |
| top-level `support` | `extensions["ai.opennod.agent-commerce"].support` |
| top-level `agent_policies` | `extensions["ai.opennod.agent-commerce"].policies` |
| `transactions.policies` (returns/cancellation/etc.) | `extensions["ai.opennod.agent-commerce"].transactions.transaction_policies` |
| `agent_policies.require_human_confirmation` | `extensions["ai.opennod.agent-commerce"].policies.confirmation_requirements` |

`transactions.purchase.payment_methods` was an array of strings in v0.1.
In v0.2 it is an array of `payment_method` objects with rail-specific
fields (`rail`, `agent_endpoint`, `currencies`, `min_amount`,
`max_amount`, `settlement_window`).

## New fields in v0.2

### `authorization_levels`

A per-action matrix richer than `policies.confirmation_requirements`
(which is a single threshold). Keys are action names; values are
`{ level, threshold?, rationale? }` where `level` is one of:

- `autonomous` — agent may perform without human confirmation
- `requires_human_confirmation` — must obtain explicit human approval
- `prohibited` — agent must not attempt this action at all

Conventional action keys: `place_order`, `modify_order`, `cancel_order`,
`request_refund`, `initiate_dispute`, `book_appointment`,
`modify_appointment`, `cancel_appointment`, `subscribe`, `unsubscribe`,
`modify_subscription`, `update_account`, `update_payment_method`,
`request_quote`, `accept_quote`, `sign_terms`, `sign_contract`,
`share_pii`, `share_payment_credentials`. Unlisted action keys inherit
`policies.confirmation_requirements`.

### `automated_booking_capabilities`

Per-service-type structured booking capabilities. Use when different
bookable service types have different agent rules (e.g. a hotel taking
room bookings autonomously but requiring human confirmation for spa
appointments). Each entry covers one `service_type` with booking
windows, modification/cancellation policy, and party-size limits.

If all bookings have identical agent rules, omit this and use
`transactions.booking` + `authorization_levels`.

### `notes`

Free-text guidance for agents that doesn't fit a structured field.
Operational facts only — not marketing.

## Example

```json
{
  "extensions": {
    "ai.opennod.agent-commerce": {
      "policies": {
        "allow_automated_purchases": true,
        "confirmation_requirements": {
          "purchases_above": 500,
          "currency": "USD",
          "subscription_signups": false,
          "account_changes": true
        },
        "rate_limits": {
          "search": { "requests": 60, "period": "minute" }
        },
        "authentication": {
          "methods": ["oauth2", "api_key"],
          "registration_url": "https://example.com/agents/register"
        },
        "data_usage": {
          "allow_caching": true,
          "cache_ttl_seconds": 3600,
          "allow_price_tracking": true,
          "allow_training": false
        }
      },
      "discovery": {
        "catalog": {
          "type": "product_feed",
          "format": "json",
          "url": "https://example.com/catalog.json",
          "total_items": 1250,
          "updated_at": "2026-04-27T08:00:00Z"
        },
        "search": {
          "endpoint": "https://example.com/api/search",
          "method": "GET",
          "parameters": {
            "q": { "type": "string", "required": true }
          },
          "response_format": "application/json",
          "authentication": "api_key"
        }
      },
      "transactions": {
        "capabilities": ["purchase"],
        "purchase": {
          "endpoint": "https://example.com/api/checkout",
          "method": "POST",
          "authentication": "oauth2",
          "payment_methods": [
            { "rail": "card", "currencies": ["USD"], "max_amount": 5000 },
            { "rail": "stablecoin-usdc", "agent_endpoint": "https://example.com/usdc", "currencies": ["USDC"], "settlement_window": "instant" }
          ],
          "currencies": ["USD"]
        },
        "transaction_policies": {
          "returns": {
            "url": "https://example.com/returns",
            "summary": "30-day returns, refund to original payment",
            "window_days": 30
          }
        },
        "terms_of_service": "https://example.com/tos",
        "privacy_policy": "https://example.com/privacy"
      },
      "authorization_levels": {
        "place_order": { "level": "autonomous", "threshold": { "amount_above": 500, "currency": "USD" } },
        "request_refund": { "level": "requires_human_confirmation" },
        "sign_contract": { "level": "prohibited" }
      },
      "notes": "We do not ship to PO boxes despite what address validators allow. Custom orders require a follow-up email; do not attempt them through the standard checkout."
    }
  }
}
```

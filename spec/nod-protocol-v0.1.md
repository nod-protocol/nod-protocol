# NOD Protocol Specification v0.1

**Status:** Draft
**Version:** 0.1.0
**Date:** 2026-03-23
**Authors:** OpenNOD
**License:** MIT

> The protocol version is defined in [`/VERSION`](../VERSION) at the repo root. Do not change it elsewhere.

---

## 1. Introduction

### 1.1 Purpose

The NOD (Notarized Object Declaration) Protocol defines a machine-readable format for businesses to declare their capabilities, offerings, and interaction interfaces to AI agents. It serves as the bridge between AI agents acting on behalf of humans and businesses seeking to be discovered, evaluated, and transacted with by those agents.

### 1.2 Problem Statement

AI agents increasingly attempt to interact with businesses on behalf of users — searching for products, comparing services, making purchases, booking appointments, and managing post-transaction workflows. These agents face systematic failures because:

- Business information is locked in human-readable HTML, not machine-consumable structures
- Transaction capabilities are hidden behind JavaScript-rendered UIs with no programmatic interface
- Policies (returns, pricing, availability) are buried in prose, not structured data
- There is no standard way for a business to declare "here is what I offer, here is how an agent can interact with me"

The NOD Protocol solves this by providing a single, discoverable, machine-readable manifest that tells any AI agent everything it needs to know to interact with a business.

### 1.3 Design Principles

1. **Agent-first** — Every field exists because an agent needs it, not because a human developer finds it elegant
2. **Progressive complexity** — A minimal manifest takes 30 minutes to create; a comprehensive one can be auto-generated
3. **Standards-compatible** — Extends and references schema.org, OpenAPI, MCP, and JSON-LD rather than replacing them
4. **Discoverable** — Agents can find the manifest through well-known URLs without prior knowledge
5. **Versionable** — The protocol evolves without breaking existing implementations
6. **Validatable** — Any manifest can be programmatically checked for correctness

### 1.4 Relationship to Existing Standards

| Standard | Relationship |
|----------|-------------|
| schema.org / JSON-LD | NOD references and extends schema.org types. Existing structured data is complementary. |
| OpenAPI / Swagger | NOD links to OpenAPI specs for API-capable businesses. NOD does not redefine API documentation. |
| MCP (Model Context Protocol) | NOD declares MCP server endpoints. MCP handles the actual agent-server communication. |
| robots.txt | NOD adds agent-specific directives. robots.txt remains authoritative for crawl permissions. |
| sitemap.xml | NOD references sitemaps for content discovery. Does not replace them. |
| Open Graph | OG tags serve social platforms. NOD serves AI agents. Both can coexist. |

---

## 2. Manifest Discovery

### 2.1 Well-Known URL

The primary discovery mechanism is a well-known URL:

```
https://{domain}/.well-known/nod.json
```

Agents MUST check this URL first. If not found, agents MAY check:

```
https://{domain}/nod.json
```

### 2.2 HTML Link Tag (Secondary)

Businesses MAY also declare their manifest via an HTML `<link>` tag:

```html
<link rel="nod-manifest" href="/.well-known/nod.json" type="application/json" />
```

This supports businesses that cannot serve files from `/.well-known/` (e.g., some hosted platforms).

### 2.3 DNS TXT Record (Tertiary)

For businesses with multiple domains or subdomains:

```
_nod.example.com TXT "v=nod1; manifest=https://example.com/.well-known/nod.json"
```

### 2.4 Content Type

The manifest MUST be served with `Content-Type: application/json` and SHOULD include `Access-Control-Allow-Origin: *` to permit cross-origin agent access.

### 2.5 Caching

The manifest SHOULD include standard HTTP cache headers. Agents SHOULD respect `Cache-Control` and `ETag` headers. Recommended TTL: 24 hours for stable businesses, 1 hour for businesses with frequently changing inventory.

---

## 3. Manifest Schema

### 3.1 Root Object

```json
{
  "$schema": "schema/schema.json",
  "nod_version": "0.1",
  "generated_at": "2026-03-23T12:00:00Z",
  "business": { ... },
  "discovery": { ... },
  "transactions": { ... },
  "information": { ... },
  "support": { ... },
  "agent_policies": { ... },
  "extensions": { ... }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string (URI) | RECOMMENDED | URL of the JSON Schema for validation |
| `nod_version` | string | REQUIRED | Protocol version (semver: "0.1") |
| `generated_at` | string (ISO 8601) | REQUIRED | When this manifest was last generated/updated |
| `business` | object | REQUIRED | Core business identity and metadata |
| `discovery` | object | RECOMMENDED | How agents find products/services/information |
| `transactions` | object | OPTIONAL | How agents can transact with this business |
| `information` | object | RECOMMENDED | Real-time data endpoints (inventory, hours, etc.) |
| `support` | object | OPTIONAL | Post-transaction and customer support interfaces |
| `agent_policies` | object | RECOMMENDED | Rules and permissions for agent interactions |
| `extensions` | object | OPTIONAL | Industry-specific extensions |

### 3.2 Business Object

The `business` object declares who the business is.

```json
{
  "business": {
    "name": "Acme Running Co.",
    "legal_name": "Acme Running Company LLC",
    "description": "Premium running shoes and gear for athletes of all levels",
    "type": "ecommerce",
    "categories": ["retail", "sporting_goods", "footwear"],
    "naics_codes": ["448210"],
    "url": "https://acmerunning.com",
    "logo": "https://acmerunning.com/logo.png",
    "founded": "2018",
    "locations": [
      {
        "type": "physical",
        "name": "Flagship Store",
        "address": {
          "street": "123 Main St",
          "city": "Portland",
          "state": "OR",
          "postal_code": "97201",
          "country": "US"
        },
        "coordinates": {
          "latitude": 45.5152,
          "longitude": -122.6784
        },
        "hours": {
          "timezone": "America/Los_Angeles",
          "regular": {
            "monday": { "open": "09:00", "close": "20:00" },
            "tuesday": { "open": "09:00", "close": "20:00" },
            "wednesday": { "open": "09:00", "close": "20:00" },
            "thursday": { "open": "09:00", "close": "20:00" },
            "friday": { "open": "09:00", "close": "21:00" },
            "saturday": { "open": "10:00", "close": "21:00" },
            "sunday": { "open": "10:00", "close": "18:00" }
          },
          "exceptions": [
            {
              "date": "2026-12-25",
              "status": "closed",
              "reason": "Christmas Day"
            }
          ]
        },
        "phone": "+1-503-555-0100",
        "email": "flagship@acmerunning.com"
      }
    ],
    "contacts": {
      "general": { "email": "hello@acmerunning.com", "phone": "+1-800-555-0100" },
      "support": { "email": "support@acmerunning.com", "phone": "+1-800-555-0101" },
      "press": { "email": "press@acmerunning.com" }
    },
    "social": {
      "x": "https://x.com/acmerunning",
      "instagram": "https://instagram.com/acmerunning",
      "linkedin": "https://linkedin.com/company/acmerunning"
    },
    "schema_org": "https://acmerunning.com/schema/organization.jsonld",
    "identifiers": {
      "duns": "123456789",
      "ein": "XX-XXXXXXX",
      "lei": "XXXXXXXXXXXXXXXXXXXX"
    }
  }
}
```

#### 3.2.1 Business Type Enum

| Value | Description |
|-------|-------------|
| `ecommerce` | Online retail / product sales |
| `saas` | Software as a Service |
| `restaurant` | Food service / dining |
| `hotel` | Accommodation / lodging |
| `healthcare` | Medical / health services |
| `professional_services` | Consulting, legal, accounting, etc. |
| `marketplace` | Multi-vendor platform |
| `media` | Content / publishing |
| `education` | Educational institution or platform |
| `nonprofit` | Non-profit organization |
| `government` | Government agency or service |
| `other` | Other business type |

### 3.3 Discovery Object

The `discovery` object tells agents how to find what the business offers.

```json
{
  "discovery": {
    "catalog": {
      "type": "product_feed",
      "format": "json",
      "url": "https://acmerunning.com/feeds/products.json",
      "total_items": 1250,
      "updated_at": "2026-03-23T06:00:00Z",
      "schema": "https://schema.org/Product",
      "pagination": {
        "type": "cursor",
        "page_size": 100
      }
    },
    "search": {
      "endpoint": "https://acmerunning.com/api/v1/search",
      "method": "GET",
      "parameters": {
        "q": { "type": "string", "required": true, "description": "Search query" },
        "category": { "type": "string", "required": false, "description": "Filter by category slug" },
        "min_price": { "type": "number", "required": false },
        "max_price": { "type": "number", "required": false },
        "in_stock": { "type": "boolean", "required": false, "default": true },
        "sort": { "type": "string", "enum": ["relevance", "price_asc", "price_desc", "newest"], "default": "relevance" },
        "page": { "type": "integer", "default": 1 },
        "per_page": { "type": "integer", "default": 20, "max": 100 }
      },
      "response_format": "application/json",
      "rate_limit": { "requests": 60, "period": "minute" },
      "authentication": "none"
    },
    "categories": [
      {
        "name": "Running Shoes",
        "slug": "running-shoes",
        "url": "https://acmerunning.com/category/running-shoes",
        "item_count": 340,
        "subcategories": [
          { "name": "Road Running", "slug": "road-running", "item_count": 180 },
          { "name": "Trail Running", "slug": "trail-running", "item_count": 95 },
          { "name": "Racing", "slug": "racing", "item_count": 65 }
        ]
      }
    ],
    "sitemap": "https://acmerunning.com/sitemap.xml",
    "openapi": "https://acmerunning.com/api/openapi.yaml",
    "graphql": "https://acmerunning.com/api/graphql",
    "mcp_server": {
      "url": "https://acmerunning.com/mcp",
      "capabilities": ["search", "product_details", "inventory_check"],
      "authentication": "api_key",
      "documentation": "https://docs.acmerunning.com/mcp"
    },
    "feeds": {
      "new_arrivals": {
        "url": "https://acmerunning.com/feeds/new-arrivals.json",
        "format": "json",
        "update_frequency": "daily"
      },
      "deals": {
        "url": "https://acmerunning.com/feeds/deals.json",
        "format": "json",
        "update_frequency": "hourly"
      }
    },
    "llms_txt": {
      "url": "https://acmerunning.com/llms.txt",
      "full_url": "https://acmerunning.com/llms-full.txt",
      "description": "Structured guidance for AI systems about Acme Running's products and content"
    }
  }
}
```

#### 3.3.1 Catalog Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | REQUIRED | One of: `product_feed`, `service_list`, `menu`, `inventory`, `custom` |
| `format` | string | REQUIRED | One of: `json`, `xml`, `csv`, `jsonld` |
| `url` | string (URI) | REQUIRED | URL of the catalog feed |
| `total_items` | integer | RECOMMENDED | Total number of items in catalog |
| `updated_at` | string (ISO 8601) | RECOMMENDED | Last update timestamp |
| `schema` | string (URI) | RECOMMENDED | Schema used for item descriptions |
| `pagination` | object | OPTIONAL | Pagination details if feed is paginated |

#### 3.3.2 Search Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `endpoint` | string (URI) | REQUIRED | Search API endpoint |
| `method` | string | REQUIRED | HTTP method (GET or POST) |
| `parameters` | object | REQUIRED | Map of parameter names to their specs |
| `response_format` | string | REQUIRED | MIME type of response |
| `rate_limit` | object | RECOMMENDED | Rate limiting details |
| `authentication` | string | REQUIRED | One of: `none`, `api_key`, `oauth2`, `bearer` |

#### 3.3.3 llms_txt Object

The optional `llms_txt` field references a site's [llms.txt](https://llmstxt.org/) file — the emerging standard (proposed by Jeremy Howard, 2024) for providing structured guidance to AI systems about a site's content and capabilities.

**Relationship:** `nod.json` is the *transactional* manifest — it declares what agents can *do* with a business. `llms.txt` is the *informational* layer — it tells LLMs what the site *is* and *contains*. Together they provide complete agent coverage: discovery + interaction.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string (URI) | REQUIRED | URL of the llms.txt file (typically `/llms.txt`) |
| `full_url` | string (URI) | OPTIONAL | URL of llms-full.txt (expanded version with full content) |
| `description` | string | OPTIONAL | Brief description of what the llms.txt covers |

```json
{
  "llms_txt": {
    "url": "https://example.com/llms.txt",
    "full_url": "https://example.com/llms-full.txt",
    "description": "Product catalog, API documentation, and support guides"
  }
}
```

### 3.4 Transactions Object

The `transactions` object declares how agents can transact with the business.

```json
{
  "transactions": {
    "capabilities": ["purchase", "booking", "subscription"],
    "purchase": {
      "type": "api",
      "endpoint": "https://acmerunning.com/api/v1/orders",
      "method": "POST",
      "authentication": "oauth2",
      "oauth2": {
        "authorization_url": "https://acmerunning.com/oauth/authorize",
        "token_url": "https://acmerunning.com/oauth/token",
        "scopes": ["read:products", "write:orders", "read:orders"]
      },
      "documentation": "https://docs.acmerunning.com/api/orders",
      "cart_api": {
        "add": { "method": "POST", "endpoint": "/api/v1/cart/items" },
        "remove": { "method": "DELETE", "endpoint": "/api/v1/cart/items/{item_id}" },
        "view": { "method": "GET", "endpoint": "/api/v1/cart" },
        "checkout": { "method": "POST", "endpoint": "/api/v1/cart/checkout" }
      },
      "payment_methods": ["credit_card", "paypal", "apple_pay", "google_pay"],
      "currencies": ["USD"],
      "tax_handling": "calculated_at_checkout",
      "shipping": {
        "methods_endpoint": "/api/v1/shipping/methods",
        "estimate_endpoint": "/api/v1/shipping/estimate",
        "regions": ["US", "CA"]
      }
    },
    "booking": null,
    "subscription": {
      "type": "api",
      "endpoint": "https://acmerunning.com/api/v1/subscriptions",
      "plans_endpoint": "https://acmerunning.com/api/v1/subscriptions/plans",
      "authentication": "oauth2"
    },
    "promotions": {
      "coupon_validation": {
        "endpoint": "/api/v1/coupons/validate",
        "method": "POST"
      },
      "active_promotions_feed": "https://acmerunning.com/feeds/promotions.json"
    },
    "policies": {
      "returns": {
        "url": "https://acmerunning.com/policies/returns",
        "summary": "30-day returns on unworn items with tags attached",
        "window_days": 30,
        "conditions": ["unworn", "tags_attached", "original_packaging"],
        "refund_method": "original_payment",
        "restocking_fee_percent": 0
      },
      "cancellation": {
        "url": "https://acmerunning.com/policies/cancellation",
        "summary": "Orders can be cancelled within 1 hour of placement",
        "window_minutes": 60
      },
      "price_match": {
        "available": true,
        "url": "https://acmerunning.com/policies/price-match",
        "summary": "We match verified lower prices from authorized retailers"
      }
    },
    "terms_of_service": "https://acmerunning.com/terms",
    "privacy_policy": "https://acmerunning.com/privacy"
  }
}
```

#### 3.4.1 Transaction Capabilities Enum

| Value | Description |
|-------|-------------|
| `purchase` | One-time product purchases |
| `booking` | Appointment/reservation booking |
| `subscription` | Recurring service subscriptions |
| `quote` | Request-for-quote workflows |
| `auction` | Bidding/auction participation |
| `donation` | Accept donations |
| `custom` | Custom transaction flow (must document) |

### 3.5 Information Object

Real-time data endpoints for agents.

```json
{
  "information": {
    "inventory": {
      "endpoint": "https://acmerunning.com/api/v1/inventory/{sku}",
      "method": "GET",
      "authentication": "none",
      "freshness": "real_time",
      "response_schema": {
        "sku": "string",
        "in_stock": "boolean",
        "quantity": "integer",
        "estimated_restock": "string|null"
      }
    },
    "pricing": {
      "endpoint": "https://acmerunning.com/api/v1/products/{id}/price",
      "method": "GET",
      "authentication": "none",
      "includes_tax": false,
      "currency": "USD"
    },
    "hours": {
      "endpoint": "https://acmerunning.com/api/v1/locations/{id}/hours",
      "method": "GET",
      "response_includes": ["regular_hours", "holiday_hours", "current_status"]
    },
    "reviews": {
      "endpoint": "https://acmerunning.com/api/v1/products/{id}/reviews",
      "method": "GET",
      "aggregation": {
        "average_rating": 4.6,
        "total_reviews": 12847,
        "rating_distribution": { "5": 8234, "4": 2891, "3": 1102, "2": 387, "1": 233 }
      },
      "third_party": [
        { "platform": "trustpilot", "url": "https://trustpilot.com/review/acmerunning.com", "rating": 4.5 },
        { "platform": "google", "rating": 4.7 }
      ]
    },
    "faq": {
      "url": "https://acmerunning.com/api/v1/faq",
      "format": "json",
      "topics": ["shipping", "returns", "sizing", "product_care"]
    },
    "structured_content": {
      "schema_org": "https://acmerunning.com/schema/organization.jsonld",
      "json_ld_pages": [
        "https://acmerunning.com/about",
        "https://acmerunning.com/contact"
      ]
    }
  }
}
```

### 3.6 Support Object

Post-transaction interaction interfaces.

```json
{
  "support": {
    "order_tracking": {
      "endpoint": "https://acmerunning.com/api/v1/orders/{order_id}/tracking",
      "method": "GET",
      "authentication": "bearer"
    },
    "returns": {
      "initiate_endpoint": "https://acmerunning.com/api/v1/returns",
      "method": "POST",
      "authentication": "bearer",
      "required_fields": ["order_id", "items", "reason"]
    },
    "contact": {
      "channels": [
        {
          "type": "chat",
          "url": "https://acmerunning.com/api/v1/support/chat",
          "protocol": "websocket",
          "hours": "24/7",
          "agent_compatible": true
        },
        {
          "type": "email",
          "address": "support@acmerunning.com",
          "expected_response_time": "4_hours"
        },
        {
          "type": "phone",
          "number": "+1-800-555-0101",
          "hours": { "timezone": "America/Los_Angeles", "weekdays": "08:00-20:00", "weekends": "10:00-18:00" },
          "agent_compatible": false
        }
      ],
      "mcp_server": {
        "url": "https://acmerunning.com/mcp/support",
        "capabilities": ["order_status", "return_initiation", "faq_query"]
      }
    },
    "webhooks": {
      "available_events": ["order.shipped", "order.delivered", "return.approved", "return.refunded"],
      "registration_endpoint": "https://acmerunning.com/api/v1/webhooks",
      "documentation": "https://docs.acmerunning.com/webhooks"
    }
  }
}
```

### 3.7 Agent Policies Object

Rules governing how agents may interact with the business.

```json
{
  "agent_policies": {
    "allow_automated_purchases": true,
    "require_human_confirmation": {
      "purchases_above": 500.00,
      "currency": "USD",
      "subscription_signups": true,
      "account_changes": true
    },
    "rate_limits": {
      "search": { "requests": 60, "period": "minute" },
      "product_details": { "requests": 120, "period": "minute" },
      "transactions": { "requests": 10, "period": "minute" }
    },
    "authentication": {
      "methods": ["api_key", "oauth2"],
      "registration_url": "https://developers.acmerunning.com/register",
      "documentation": "https://docs.acmerunning.com/auth"
    },
    "data_usage": {
      "allow_caching": true,
      "cache_ttl_seconds": 3600,
      "allow_comparison": true,
      "allow_price_tracking": true,
      "allow_training": false
    },
    "preferred_agent_identification": {
      "header": "X-Agent-Id",
      "user_agent_prefix": "NOD-Agent/"
    },
    "human_fallback": {
      "url": "https://acmerunning.com",
      "description": "Direct the user to our website for actions that require human interaction"
    }
  }
}
```

---

## 4. Data Types

### 4.1 Primitive Types

| Type | Format | Example |
|------|--------|---------|
| `string` | UTF-8 text | `"Acme Running"` |
| `integer` | Whole number | `1250` |
| `number` | Decimal number | `149.99` |
| `boolean` | true/false | `true` |
| `uri` | RFC 3986 URI | `"https://example.com/api"` |
| `datetime` | ISO 8601 | `"2026-03-23T12:00:00Z"` |
| `date` | ISO 8601 date | `"2026-03-23"` |
| `time` | HH:MM (24h) | `"09:00"` |
| `currency` | ISO 4217 | `"USD"` |
| `country` | ISO 3166-1 alpha-2 | `"US"` |
| `language` | BCP 47 | `"en-US"` |
| `phone` | E.164 | `"+15035550100"` |

### 4.2 Enum Types

All enums are lowercase with underscores. Unknown values MUST be preserved by consumers (forward compatibility).

---

## 5. Validation Rules

### 5.1 Required Fields

A valid NOD manifest MUST contain:
1. `nod_version` — matching a published protocol version
2. `generated_at` — valid ISO 8601 datetime
3. `business.name` — non-empty string
4. `business.type` — valid business type enum value
5. `business.url` — valid URI matching the serving domain

### 5.2 Conditional Requirements

- If `transactions` is present, at least one capability must be declared with a corresponding configuration object
- If `discovery.search` is present, `endpoint`, `method`, and `parameters` are required
- If `discovery.catalog` is present, `type`, `format`, and `url` are required
- If any `authentication` field is set to `oauth2`, the `oauth2` configuration object is required

### 5.3 URI Validation

All URIs MUST:
- Use HTTPS (except for localhost development)
- Be absolute URIs (no relative paths in root-level fields)
- Be reachable (validators SHOULD verify with HEAD requests)

Relative URIs are permitted within nested objects (e.g., `cart_api` endpoints) and are resolved against `business.url`.

### 5.4 Freshness

- `generated_at` SHOULD be within the last 30 days
- Manifests older than 90 days SHOULD be treated as potentially stale by agents
- The HTTP `Last-Modified` header SHOULD match `generated_at`

---

## 6. Versioning

### 6.1 Protocol Versioning

The protocol uses semantic versioning: `MAJOR.MINOR`

- **MINOR** increments add optional fields or new sections. Existing manifests remain valid.
- **MAJOR** increments may remove or restructure required fields. Agents must handle version negotiation.

### 6.2 Manifest Versioning

Businesses SHOULD update `generated_at` whenever manifest content changes. Businesses MAY include an `etag` or `version` field for change detection.

### 6.3 Agent Version Negotiation

Agents SHOULD:
1. Read `nod_version` first
2. Process all fields they understand
3. Ignore unknown fields (forward compatibility)
4. Never fail on unexpected data

---

## 7. Minimum Viable Implementations

### 7.1 Tier 1: Basic Presence (30 minutes)

The absolute minimum for any business:

```json
{
  "nod_version": "0.1",
  "generated_at": "2026-03-23T12:00:00Z",
  "business": {
    "name": "Joe's Coffee Shop",
    "type": "restaurant",
    "description": "Specialty coffee and pastries in downtown Portland",
    "url": "https://joescoffee.com",
    "locations": [
      {
        "type": "physical",
        "address": {
          "street": "456 Oak Ave",
          "city": "Portland",
          "state": "OR",
          "postal_code": "97201",
          "country": "US"
        },
        "hours": {
          "timezone": "America/Los_Angeles",
          "regular": {
            "monday": { "open": "06:00", "close": "18:00" },
            "tuesday": { "open": "06:00", "close": "18:00" },
            "wednesday": { "open": "06:00", "close": "18:00" },
            "thursday": { "open": "06:00", "close": "18:00" },
            "friday": { "open": "06:00", "close": "20:00" },
            "saturday": { "open": "07:00", "close": "20:00" },
            "sunday": { "open": "07:00", "close": "16:00" }
          }
        },
        "phone": "+1-503-555-0200"
      }
    ],
    "contacts": {
      "general": { "email": "hello@joescoffee.com" }
    }
  },
  "agent_policies": {
    "human_fallback": {
      "url": "https://joescoffee.com",
      "description": "Visit our website or call for orders and inquiries"
    }
  }
}
```

### 7.2 Tier 2: Discoverable Business (2-4 hours)

Adds discovery and information capabilities:

- Catalog/menu feed
- Category structure
- Business hours API
- FAQ endpoint
- Schema.org references

### 7.3 Tier 3: Transactable Business (1-2 days)

Full transaction support:

- API-based purchasing/booking
- OAuth2 authentication
- Webhook notifications
- Return/support automation

### 7.4 Tier 4: Agent-Native Business (ongoing)

Full agent integration:

- MCP server
- Real-time inventory
- Programmatic everything
- Agent-specific pricing/terms

---

## 8. Industry Extensions

The `extensions` field allows industry-specific data.

### 8.1 Extension Namespacing

Extensions use reverse-domain namespacing:

```json
{
  "extensions": {
    "ai.opennod.restaurant": {
      "cuisine_types": ["coffee", "bakery"],
      "dietary_options": ["vegan", "gluten_free"],
      "menu_url": "https://joescoffee.com/api/menu",
      "reservation_system": null,
      "delivery_platforms": ["doordash", "ubereats"],
      "average_meal_price": { "amount": 8.50, "currency": "USD" }
    }
  }
}
```

### 8.2 Registered Extensions

| Namespace | Industry | Status |
|-----------|----------|--------|
| `ai.opennod.restaurant` | Food & Beverage | Draft |
| `ai.opennod.hotel` | Hospitality | Draft |
| `ai.opennod.healthcare` | Healthcare | Draft |
| `ai.opennod.ecommerce` | E-commerce | Draft |
| `ai.opennod.saas` | Software | Draft |
| `ai.opennod.professional` | Professional Services | Draft |

Custom extensions using other namespaces are permitted and encouraged.

---

## 9. Security Considerations

### 9.1 Authentication

Businesses SHOULD require authentication for:
- Any write operation (purchases, bookings, account changes)
- High-frequency read operations (search, inventory checks)
- Personally identifiable information access

Businesses SHOULD NOT require authentication for:
- Reading the NOD manifest itself
- Basic catalog/menu browsing
- Business information (hours, locations, policies)

### 9.2 Agent Identification

Agents SHOULD identify themselves via:
1. `User-Agent` header including `NOD-Agent/{version}` prefix
2. `X-Agent-Id` header with a registered agent identifier
3. OAuth2 client credentials for authenticated operations

### 9.3 Data Privacy

The NOD manifest MUST NOT contain:
- Customer personal data
- Internal system credentials
- Proprietary business intelligence
- Information not intended for public consumption

### 9.4 Abuse Prevention

Businesses SHOULD:
- Implement rate limiting on all endpoints
- Monitor for unusual access patterns
- Maintain the ability to revoke agent access
- Log agent interactions for audit purposes

---

## 10. Conformance Levels

### 10.1 Level 1: Declarative

Business publishes a valid manifest with `business` section complete. Agents can discover and describe the business.

### 10.2 Level 2: Discoverable

Business publishes catalog/search capabilities. Agents can find products/services.

### 10.3 Level 3: Queryable

Business exposes real-time information endpoints. Agents can check inventory, pricing, availability.

### 10.4 Level 4: Transactable

Business supports programmatic transactions. Agents can purchase/book/subscribe.

### 10.5 Level 5: Agent-Native

Business provides full agent infrastructure (MCP servers, webhooks, real-time APIs). Agents can handle complete interaction lifecycles.

---

## Appendix A: Complete Field Reference

See the JSON Schema at `schema/schema.json` for the machine-readable complete field reference.

## Appendix B: MIME Type Registration

The NOD manifest uses `application/json`. A dedicated MIME type (`application/nod+json`) may be registered in future versions.

## Appendix C: Glossary

| Term | Definition |
|------|-----------|
| **Agent** | An AI system acting on behalf of a human user |
| **Manifest** | The nod.json file declaring a business's agent-facing capabilities |
| **NOD Score** | A 0-100 composite score measuring agent readiness |
| **AEO** | Agent Engine Optimization — optimizing for AI agent discovery and interaction |
| **MCP** | Model Context Protocol — Anthropic's protocol for AI-tool communication |

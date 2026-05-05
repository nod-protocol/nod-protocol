# Getting Started with the NOD Protocol

This guide walks you through creating a NOD manifest for your business and checking your site's agent readiness score.

## What is a NOD Manifest?

A NOD manifest is a JSON file that describes your business in a format AI agents can natively consume. It tells agents:

- **Who you are** — business name, type, locations, hours, contacts
- **What you offer** — product catalogs, service lists, menus
- **How to transact** — APIs, checkout flows, booking systems
- **What the rules are** — rate limits, authentication, policies

Think of it as a machine-readable business card that enables AI agents to discover, understand, and interact with your business without scraping HTML or guessing at page structure.

## Step 1: Create Your Manifest

Create a file called `nod.json` with this minimal structure:

```json
{
  "nod_version": "0.1",
  "generated_at": "2026-03-23T12:00:00Z",
  "business": {
    "name": "Your Business Name",
    "type": "ecommerce",
    "description": "A brief description of what your business does",
    "url": "https://yourbusiness.com",
    "locations": [
      {
        "type": "physical",
        "address": {
          "street": "123 Main St",
          "city": "Your City",
          "state": "CA",
          "postal_code": "90210",
          "country": "US"
        },
        "phone": "+1-555-000-0000"
      }
    ],
    "contacts": {
      "general": {
        "email": "hello@yourbusiness.com"
      }
    }
  }
}
```

Replace the values with your actual business information.

### Business Types

Set `business.type` to one of:
`ecommerce`, `saas`, `restaurant`, `hotel`, `healthcare`, `professional_services`, `marketplace`, `media`, `education`, `nonprofit`, `government`, `other`

## Step 2: Host Your Manifest

Place the file at this URL on your website:

```
https://yourbusiness.com/.well-known/nod.json
```

**For most web servers**, create a `.well-known` directory in your web root and place `nod.json` inside it.

**For platforms that don't support `.well-known`**, you can:
1. Host at `https://yourbusiness.com/nod.json` instead
2. Add a link tag to your homepage: `<link rel="nod-manifest" href="/nod.json" type="application/json" />`

### CORS Headers

Add this header so agents from any origin can read your manifest:

```
Access-Control-Allow-Origin: *
```

## Step 3: Validate Your Manifest

Use the validator to check your manifest:

```bash
python -m validators.validate path/to/nod.json
```

Or validate a live manifest:

```bash
python -m validators.validate https://yourbusiness.com/.well-known/nod.json
```

The validator checks:
- JSON syntax
- Required fields
- Data types and formats
- Logical consistency

## Step 4: Check Your NOD Score

Run the scanner on your website:

```bash
python -m scanner https://yourbusiness.com
```

This produces a score from 0-100 across 7 categories:

1. **Structured Data** (20%) — JSON-LD, schema.org, Open Graph
2. **Discovery** (20%) — Sitemaps, feeds, search endpoints
3. **Transaction Readiness** (15%) — Pricing, checkout, payment
4. **API Access** (15%) — APIs, documentation, MCP
5. **Content Parseability** (10%) — Semantic HTML, structure
6. **Reliability** (10%) — Speed, bot access, SSR
7. **NOD Protocol** (10%) — Your manifest completeness

## Step 5: Improve Your Score

### Quick wins (biggest score impact):

1. **Add JSON-LD** to your homepage with an Organization entity
2. **Create a sitemap.xml** if you don't have one
3. **Add schema.org Product/Service** entities to product/service pages
4. **Publish your NOD manifest** (even a minimal one)
5. **Ensure your site serves content without JavaScript** (SSR)

### Medium effort:

6. Add a product/service feed (JSON or XML)
7. Document any APIs you have (OpenAPI spec)
8. Add structured pricing (schema.org Offer entities)
9. Improve semantic HTML (proper heading hierarchy, landmarks)

### Advanced:

10. Expose a search API
11. Build an MCP server for agent interactions
12. Implement OAuth2 for programmatic transactions
13. Add webhook support for order/booking events

## Examples

See the `/examples/` directory for complete manifests across different business types:

- `ecommerce/` — Online retail store
- `saas/` — Software platform
- `restaurant/` — Restaurant with ordering and reservations
- `hotel/` — Hotel with room booking
- `healthcare/` — Medical practice
- `professional-services/` — Professional services firm

Each directory contains a `minimal.json` and `comprehensive.json` showing the range of implementation depth.

## For Agent Developers

If you're building an AI agent that needs to discover and interact with businesses:

1. Check `/.well-known/nod.json` on any domain
2. Fall back to `<link rel="nod-manifest">` in HTML
3. Parse the manifest to understand the business's capabilities
4. Use declared APIs, feeds, and MCP servers for interaction
5. Respect `agent_policies` for rate limits and authentication
6. Identify your agent via `User-Agent: NOD-Agent/1.0` header

The manifest tells you exactly what the business supports — no need to guess or scrape.

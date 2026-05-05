# NOD Protocol — Guide for Agent Developers

This guide explains how AI agent developers can consume NOD manifests to discover and interact with businesses.

## Discovery Flow

When your agent needs to interact with a business at `example.com`:

```
1. GET https://example.com/.well-known/nod.json
   → If 200: Parse manifest
   → If 404: Try step 2

2. GET https://example.com/
   → Parse HTML for <link rel="nod-manifest" href="...">
   → If found: Fetch and parse manifest
   → If not found: No NOD manifest available
```

## Reading the Manifest

### Check Capabilities First

```python
manifest = fetch_nod_manifest("example.com")

# What can this business do?
if manifest.get("transactions"):
    caps = manifest["transactions"]["capabilities"]
    # ["purchase", "booking", "subscription"]

# How do I search their catalog?
if manifest.get("discovery", {}).get("search"):
    search = manifest["discovery"]["search"]
    # Use search.endpoint, search.parameters, search.method
```

### Respect Agent Policies

Always check `agent_policies` before interacting:

```python
policies = manifest.get("agent_policies", {})

# Rate limits
rate_limits = policies.get("rate_limits", {})
# {"search": {"requests": 60, "period": "minute"}}

# Does this business allow automated purchases?
if not policies.get("allow_automated_purchases", False):
    # Fall back to human_fallback URL
    fallback = policies["human_fallback"]["url"]

# What purchases need human confirmation?
confirm = policies.get("require_human_confirmation", {})
if order_total > confirm.get("purchases_above", float('inf')):
    # Ask the human to confirm
```

### Agent Identification

Identify your agent properly:

```
User-Agent: NOD-Agent/1.0 MyAgentName/2.0
X-Agent-Id: my-agent-registered-id
```

## Common Interaction Patterns

### Product Search

```python
search = manifest["discovery"]["search"]

response = requests.get(
    search["endpoint"],
    params={"q": "running shoes", "max_price": 150, "in_stock": True},
    headers={"User-Agent": "NOD-Agent/1.0"}
)
products = response.json()
```

### Check Inventory

```python
inventory = manifest["information"]["inventory"]

response = requests.get(
    inventory["endpoint"].replace("{sku}", "SKU-12345"),
    headers={"User-Agent": "NOD-Agent/1.0"}
)
stock = response.json()
# {"sku": "SKU-12345", "in_stock": true, "quantity": 42}
```

### Make a Purchase (OAuth2)

```python
oauth = manifest["transactions"]["purchase"]["oauth2"]

# 1. Get access token
token = get_oauth_token(
    oauth["token_url"],
    scopes=["write:orders"],
    client_id=MY_CLIENT_ID
)

# 2. Add to cart
cart_api = manifest["transactions"]["purchase"]["cart_api"]
requests.post(
    f"{manifest['business']['url']}{cart_api['add']['endpoint']}",
    json={"product_id": "123", "quantity": 1},
    headers={"Authorization": f"Bearer {token}"}
)

# 3. Checkout
requests.post(
    f"{manifest['business']['url']}{cart_api['checkout']['endpoint']}",
    json={"payment_method": "credit_card", "shipping_method": "standard"},
    headers={"Authorization": f"Bearer {token}"}
)
```

### Use MCP Server

If the business exposes an MCP server:

```python
mcp = manifest["discovery"].get("mcp_server")
if mcp:
    # Connect to MCP server
    # mcp["url"] — server URL
    # mcp["capabilities"] — what the server can do
    # mcp["authentication"] — how to authenticate
```

## Graceful Degradation

Not every business will have a NOD manifest. Your agent should handle:

1. **No manifest** — Fall back to schema.org structured data, then HTML parsing
2. **Partial manifest** — Use what's available, skip missing sections
3. **Stale manifest** — Check `generated_at`; if > 90 days old, data may be outdated
4. **Unknown fields** — Ignore fields you don't recognize (forward compatibility)
5. **Rate limited** — Respect `agent_policies.rate_limits`, implement exponential backoff

## Caching

- Cache manifests for the duration specified by HTTP `Cache-Control` headers
- Default: 24 hours if no cache headers
- Re-fetch if your interaction fails (manifest may have been updated)

## Conformance Levels

The manifest's capabilities indicate its conformance level:

| Level | Has | Agent Can |
|-------|-----|-----------|
| 1: Declarative | `business` | Describe the business |
| 2: Discoverable | `business` + `discovery` | Find products/services |
| 3: Queryable | + `information` | Check real-time data |
| 4: Transactable | + `transactions` | Purchase/book/subscribe |
| 5: Agent-Native | + MCP + webhooks | Full lifecycle automation |

Check what level the business supports and adjust your interaction accordingly.

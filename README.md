# nod

An open protocol for AI-agent commerce on the web. `nod` defines a single
JSON manifest that any business can publish at `/.well-known/nod.json` to
declare what it is, what it offers, and how an AI agent may transact with
it — without scraping HTML.

## Status

**v0.1 — draft.** The protocol version is defined in [`VERSION`](VERSION)
at the repo root.

## Quick start (merchants)

```bash
# 1. Copy the closest example
cp examples/restaurant/minimal.json my-nod.json

# 2. Edit with your business details (name, type, url, contacts, …)
$EDITOR my-nod.json

# 3. Validate against the schema
#    Any JSON Schema 2020-12 validator works; e.g. ajv-cli:
npx -y ajv-cli validate -s schema/schema.json -d my-nod.json --spec=draft2020

# 4. Deploy to /.well-known/nod.json on your domain
#    (must be served as Content-Type: application/json)

# 5. Optionally link from your homepage
#    <link rel="nod-manifest" href="/.well-known/nod.json"
#          type="application/json" />
```

## Verify API

A hosted verify endpoint is available at **`https://api.opennod.ai`**.
This is a managed service — it is **not** part of this repo. Agents may
also fetch and parse manifests directly without using the verify API.

## Documents

- Specification: [`spec/nod-protocol-v0.1.md`](spec/nod-protocol-v0.1.md)
- JSON Schema: [`schema/schema.json`](schema/schema.json)
- Examples: [`examples/`](examples/) — one minimal and one comprehensive
  manifest per business type (ecommerce, saas, restaurant, hotel,
  healthcare, professional-services)

## License

MIT — see [`LICENSE`](LICENSE).

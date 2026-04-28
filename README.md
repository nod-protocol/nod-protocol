# nod

An open protocol for AI-agent commerce on the web. `nod` defines a single
JSON manifest that any business can publish at `/.well-known/nod.json` to
declare what it is, what it offers, and how an AI agent may transact with
it — without scraping HTML.

## Status

**v0.2 — draft.** The protocol version is defined in [`VERSION`](VERSION)
at the repo root. v0.2 is a breaking change from v0.1; see
[`CHANGELOG.md`](CHANGELOG.md).

v0.2 introduces a layered architecture: the core manifest describes the
business; the `ai.opennod.agent-commerce` extension describes the agent
contract.

## Quick start (merchants)

```bash
# 1. Copy the closest example
cp examples/restaurant/minimal.json my-nod.json

# 2. Edit with your business details (name, naics_code, gbp_primary_category, url, …)
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

- Specification (current): [`spec/nod-protocol-v0.2.md`](spec/nod-protocol-v0.2.md)
- Specification (historical): [`spec/nod-protocol-v0.1.md`](spec/nod-protocol-v0.1.md)
- Core JSON Schema: [`schema/schema.json`](schema/schema.json)
- Extensions: [`extensions/`](extensions/) — agent-commerce, merchant-voice, schema-org-bridge
- Taxonomies: [`taxonomy/`](taxonomy/) — NAICS 2022, GBP categories (deferred)
- Examples: [`examples/`](examples/) — minimal and comprehensive manifests across six industries
- Changelog: [`CHANGELOG.md`](CHANGELOG.md)

## Tests

```bash
pip install jsonschema
python3 tests/check_consistency.py
```

See [`tests/README.md`](tests/README.md).

## License

MIT — see [`LICENSE`](LICENSE).

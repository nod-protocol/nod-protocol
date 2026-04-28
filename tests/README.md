# Tests

Internal-consistency checks for the nod protocol repo.

## What gets checked

[`check_consistency.py`](check_consistency.py) verifies:

- The `VERSION` file, the core schema's `nod_version` const, the core
  schema's `$id`, and every example's `nod_version` all agree.
- The spec doc for the current `VERSION` exists at
  `spec/nod-protocol-v<VERSION>.md`.
- The core schema and every extension schema are valid JSON Schema
  Draft 2020-12.
- Every `examples/**/*.json` validates against the core schema.
- Any `extensions["ai.opennod.*"]` block in an example validates
  against the corresponding extension schema.

## Running

```bash
pip install jsonschema
python3 tests/check_consistency.py
```

Exit code is 0 on success, 1 on any consistency failure, 2 if
`jsonschema` is not installed.

## Adding a new check

If you find a way the artifacts can drift apart, add a check here
rather than fixing it once. Drift detection is the point.

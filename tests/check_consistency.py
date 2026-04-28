"""Drift-detection consistency check for the nod protocol repo.

Enforces that:
  - VERSION matches schema's nod_version const
  - VERSION is reflected in schema $id
  - The current spec doc (spec/nod-protocol-v<VERSION>.md) exists
  - Every extension JSON Schema is itself a valid Draft 2020-12 schema
  - Every example/*.json:
      * has nod_version equal to VERSION
      * has $schema URL referencing v<VERSION> (when present)
      * validates against schema/schema.json
      * has any declared extensions[ai.opennod.*] validate against the
        corresponding extension schema where one exists

Exit code 0 on success, 1 on any failure. Print all failures before
exiting so a single run surfaces every problem.

Usage:
    pip install jsonschema
    python3 tests/check_consistency.py
"""
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.stderr.write("jsonschema is required: pip install jsonschema\n")
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent

# Maps extension namespace key → schema file path
EXTENSION_SCHEMAS = {
    "ai.opennod.agent-commerce": REPO / "extensions" / "agent-commerce" / "v0.1.json",
    "ai.opennod.merchant-voice": REPO / "extensions" / "merchant-voice" / "v0.1.json",
    "ai.opennod.schema-org-extension": REPO / "extensions" / "schema-org-bridge" / "v0.1.json",
}


def main() -> int:
    failures: list[str] = []

    def fail(msg: str) -> None:
        failures.append(msg)

    # 1. VERSION
    version = (REPO / "VERSION").read_text().strip()
    print(f"VERSION: {version}")

    # 2. Core schema
    core_schema = json.loads((REPO / "schema" / "schema.json").read_text())
    schema_const = core_schema.get("properties", {}).get("nod_version", {}).get("const")
    if schema_const != version:
        fail(f"schema/schema.json nod_version const is {schema_const!r}, expected {version!r}")
    schema_id = core_schema.get("$id", "")
    if f"v{version}.json" not in schema_id:
        fail(f"schema/schema.json $id {schema_id!r} should include v{version}.json")
    try:
        Draft202012Validator.check_schema(core_schema)
    except Exception as e:
        fail(f"schema/schema.json invalid as JSON Schema: {e}")

    # 3. Spec doc for current version exists
    spec_path = REPO / "spec" / f"nod-protocol-v{version}.md"
    if not spec_path.exists():
        fail(f"missing spec doc: spec/nod-protocol-v{version}.md")

    # 4. Extension schemas valid
    for ns, sp in EXTENSION_SCHEMAS.items():
        if not sp.exists():
            fail(f"extension schema for {ns} missing at {sp.relative_to(REPO)}")
            continue
        ext_schema = json.loads(sp.read_text())
        try:
            Draft202012Validator.check_schema(ext_schema)
        except Exception as e:
            fail(f"{sp.relative_to(REPO)} invalid as JSON Schema: {e}")

    # 5. Examples
    core_validator = Draft202012Validator(core_schema)
    ext_validators = {
        ns: Draft202012Validator(json.loads(sp.read_text()))
        for ns, sp in EXTENSION_SCHEMAS.items()
        if sp.exists()
    }

    examples = sorted((REPO / "examples").rglob("*.json"))
    if not examples:
        fail("no example manifests found under examples/")

    for ex in examples:
        rel = ex.relative_to(REPO)
        try:
            data = json.loads(ex.read_text())
        except json.JSONDecodeError as e:
            fail(f"{rel}: invalid JSON: {e}")
            continue

        if data.get("nod_version") != version:
            fail(f"{rel}: nod_version is {data.get('nod_version')!r}, expected {version!r}")

        sch = data.get("$schema", "")
        if sch and f"v{version}.json" not in sch:
            fail(f"{rel}: $schema URL {sch!r} should reference v{version}.json")

        for err in core_validator.iter_errors(data):
            path = "/".join(str(p) for p in err.absolute_path) or "<root>"
            fail(f"{rel}: core schema violation at {path}: {err.message}")

        # Validate any known extensions
        for ns, payload in (data.get("extensions") or {}).items():
            v = ext_validators.get(ns)
            if not v:
                continue  # unknown extension is fine
            for err in v.iter_errors(payload):
                path = "/".join(str(p) for p in err.absolute_path) or "<root>"
                fail(f"{rel}: extension {ns} violation at {path}: {err.message}")

    # Report
    if failures:
        print()
        for f in failures:
            print(f"  FAIL: {f}")
        print(f"\n{len(failures)} consistency failure(s). Examples checked: {len(examples)}.")
        return 1

    print(f"OK: {len(examples)} example(s), all consistent with VERSION {version}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

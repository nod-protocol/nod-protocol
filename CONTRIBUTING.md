# Contributing to the NOD Protocol

Thank you for your interest in contributing to the NOD Protocol. This is an open standard, and community input is essential to making it useful, adoptable, and rigorous.

## Ways to Contribute

### 1. Propose Changes to the Spec

The NOD Protocol specification lives in `/spec/`. To propose changes:

1. Open an issue describing the change and its rationale
2. Reference specific section numbers from the spec
3. Explain the agent interaction scenario that motivates the change
4. If the community agrees, submit a PR modifying the spec

**Spec change principles:**
- Every field must serve a real agent interaction need
- Backward compatibility: new fields should be optional (minor version)
- Simplicity: if it can be derived from existing standards, reference them instead
- Testability: every field should be validatable

### 2. Add Industry Extensions

The `extensions` system (spec Section 8) allows industry-specific data. To propose a new extension:

1. Open an issue with the namespace (e.g., `ai.opennod.automotive`)
2. List the fields with types and descriptions
3. Provide at least two example manifests using the extension
4. Explain which agent interactions the extension enables

### 3. Improve the Scanner

The scanner in `/scanner/` evaluates websites. To contribute:

- **New checks:** Add checks within existing categories that improve scoring accuracy
- **Bug fixes:** Fix incorrect parsing, false positives/negatives
- **Performance:** Reduce scan time or resource usage
- **Platform support:** Improve cross-platform compatibility

### 4. Submit Example Manifests

Real-world examples in `/examples/` help businesses understand implementation. Submit examples for:

- New business types not yet covered
- Real businesses (with permission) as case studies
- Edge cases (multilingual, multi-location, marketplace)

### 5. Build Parsers and Libraries

The `/parsers/` directory will house libraries for consuming NOD manifests in different languages. Contributions welcome for:

- Python, JavaScript/TypeScript, Go, Ruby, PHP, Java
- Framework integrations (WordPress plugin, Shopify app, etc.)

## Development Setup

```bash
git clone https://github.com/opennod/nod-protocol.git
cd nod-protocol
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run tests:
```bash
python -m pytest tests/
```

Run the scanner:
```bash
python -m scanner https://example.com
```

Validate a manifest:
```bash
python -m validators.validate examples/ecommerce/comprehensive.json
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-change`)
3. Make your changes with clear commit messages
4. Ensure all tests pass
5. Update documentation if the change affects the spec or usage
6. Submit a PR with:
   - **What** the change does
   - **Why** it's needed (link to issue if applicable)
   - **How** it was tested

## Code Style

- Python: Follow PEP 8. Use type hints.
- JSON: 2-space indentation, sorted keys in schemas
- Markdown: One sentence per line (for clean diffs)

## Spec Versioning

- **Minor versions** (0.1 → 0.2): Add optional fields, new extensions, clarifications
- **Major versions** (0.x → 1.0): Restructure required fields, breaking changes

The spec follows an RFC-like process:
1. **Draft** — Open for comment
2. **Candidate** — Implementable, seeking feedback
3. **Stable** — Production-ready, backward-compatible changes only

## Code of Conduct

Be constructive. Focus on what's best for the standard and the ecosystem. Disagree on merits, not personalities.

## Questions?

Open a discussion in the GitHub Discussions tab or email contribute@opennod.ai.

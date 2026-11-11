# SigmaRail Spec

The machine-readable contract for SigmaRail data and the strategy capabilities that consume it.
Generated artifacts describe SQL and Python owned by their component repositories; this package
does not duplicate ClickHouse or LEAN application runtimes.

## Reproducible build

From the workspace, using Python 3.10+ with the `build` extra installed:

```bash
python -m pip install -e 'sigmarail-spec[build,test]'
python sigmarail-spec/tools/build.py --workspace .
python sigmarail-spec/tools/build.py --workspace . --check
python -m pytest sigmarail-spec/tests -q
```

The build verifies `spec/sources.lock.json`, exports the source contracts, and writes normalized
JSON to `src/sigmarail_spec/data/`. `--check` is read-only and fails if any generated artifact differs.
It never connects to ClickHouse or runs load/populate.

The SigmaRail source checkout is currently a new, uncommitted repository. Its lock entry therefore pins
the relevant SQL and generator input tree by SHA-256 rather than a Git commit. All other source
repositories are pinned by both Git revision and relevant-source-tree digest. Refresh pins only
after reviewing source changes:

```bash
python sigmarail-spec/tools/build.py --workspace . --write-lock
python sigmarail-spec/tools/build.py --workspace .
```

The LEAN tree keeps a source copy of the expression runtime because its execution container must
not depend on the larger SigmaRail package at runtime. Check or refresh that copy explicitly after
reviewing runtime changes:

```bash
python sigmarail-spec/tools/sync_lean_vendor.py --destination LeanProjects/VeraTradingLab/vera_spec
python sigmarail-spec/tools/sync_lean_vendor.py --destination LeanProjects/VeraTradingLab/vera_spec --write
```

The first command checks hashes without writing; the second writes the canonical expression,
evaluator, and entry-trigger modules plus a manifest. The same distribution ships a `vera_spec`
compatibility import namespace for Python consumers that are migrating incrementally.

## Runtime retrieval API

The package depends only on Pydantic at runtime for the canonical expression models; retrieval loads
packaged JSON and does not read sibling workspaces. Stable document IDs and MCP
URIs are listed in `sigmarail_spec.list_documents()`.

```python
from sigmarail_spec import get_document, get_document_text, list_documents

index = get_document("sigmarail-spec://v1/index")
alpha_slot = get_document("sigmarail-spec://v1/strategy/slots/alpha")
schema_text = get_document_text("sigmarail-spec://v1/data/schema")
```

`get_document()` returns a new dictionary each call. `get_document_text()` returns the exact
packaged JSON text. Both accept IDs, URIs, or package-relative paths. The expression runtime is
importable from `sigmarail_spec.expr`, `sigmarail_spec.evaluate`, and `sigmarail_spec.entry_trigger_ast`; those
modules were bootstrapped from VeraSpec once, and are canonical here thereafter. Historical origin
and the current scope boundary are recorded in `metadata/runtime-provenance.json`.

## MCP delivery

Studio serves the versioned JSON documents as standard MCP Resources, with a URI template for
on-demand slices under `sigmarail-spec://v1/{document}`. Agents can first read the compact index, then
fetch only the data domain, expression, or strategy slot they need. The JSON documents are the
contract; MCP only transports them, so another MCP client can consume the same package without a
Studio-specific schema. The generated `mcp/` documents describe the current SigmaRail-aligned tool
names, descriptions, input schemas, and output schemas, extracted from Studio's decorated Python
functions. The catalog deliberately omits knowledge-base, research, portfolio, and broad catalog
tools while those remain outside the cleaned SigmaRail core.

## Contract areas

- `data/lineage.json`: generated tables, columns, Sharadar roots, and exclusions.
- `data/transforms.json`: `xform_*` target, input/output, order, source SQL path, and content hash.
- `data/fields.json`: queryable SigmaRail field subset matched to the existing VeraBase registry.
- `data/expressions.json` and `data/expressions/`: canonical expression JSON Schema and domain slices.
- `data/strategy/`: Studio authoring, universe query, and executable `VeraLabV1` schemas.
- `data/runtime-capabilities.json`: generated LEAN model/action parameters and action behavior flags.
- `data/index.json`: compact retrieval catalog for agents and MCP Resources.

SigmaRail SQL core currently does not evaluate expression ASTs. The expression section remains because
Studio and TradingLab consume that runtime contract. Domain expression documents point to the
single core AST and add only the field IDs for that domain; they do not assert domain-specific
operator support or SQL execution support.

Semantic annotations that cannot safely be inferred are maintained in `metadata/annotations.json`.
SQL and code remain authoritative for executable behavior.

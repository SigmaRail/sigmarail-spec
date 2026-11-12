"""Read-only access to the packaged SigmaRail specification documents."""

from __future__ import annotations

import json
from importlib.resources import files
from typing import Any
from urllib.parse import unquote

from .expr import (
    MAX_BOOL_DEPTH, MAX_FORMULA_DEPTH, AllExpr, AnyExpr, BoolExprItem, CmpEq,
    CmpGt, CmpGte, CmpLt, CmpLte, ColBetweenExpr, ColEqExpr, ColGteExpr,
    ColLteExpr, ColRef, FormulaExpr, InTickersExpr, LitVal, NotExpr, Operand,
    RegimeAllowsEntriesExpr, RegimeExpr, RegimeMartAllowsEntriesExpr,
    SignalCompareExpr, SignalExpr, SpecExpr, WhereExpr, bool_expr_depth,
    is_runtime_only_expr, parse_bool_expr, validate_bool_expr_depth,
)
from .entry_trigger_ast import ENUM_TRIGGER_TYPES, compile_entry_trigger, trigger_eval_row
from .data_query import (
    DataQueryV1,
    QueryAliasExpression,
    QueryArithmeticExpression,
    QueryComputedField,
    QueryExpression,
    QueryField,
    QueryFieldExpression,
    QueryJoin,
    QueryLiteralExpression,
    QueryOrder,
    QueryPredicate,
)
from .evaluate import (
    evaluate_entry_triggers,
    evaluate_single_trigger,
    evaluate_slot_bool,
    evaluate_slot_number,
    evaluate_where_ast,
)

__version__ = "0.2.0"


def _index() -> dict[str, Any]:
    return json.loads(files("sigmarail_spec").joinpath("data/index.json").read_text(encoding="utf-8"))


def list_documents() -> list[dict[str, str]]:
    """List stable document IDs, MCP URIs, titles, and relative package paths."""
    return [dict(item) for item in _index()["documents"]]


def _find_document(key: str) -> dict[str, str]:
    value = unquote(str(key).strip())
    for item in _index()["documents"]:
        if value in (item["id"], item["uri"], item["path"]):
            return item
    raise KeyError(f"unknown SigmaRail spec document: {value}")


def get_document_text(key: str) -> str:
    """Return the exact packaged JSON document text addressed by ID, URI, or path."""
    item = _find_document(key)
    return files("sigmarail_spec").joinpath("data", item["path"]).read_text(encoding="utf-8")


def get_document(key: str) -> dict[str, Any]:
    """Load a packaged JSON document as a fresh dictionary."""
    value = json.loads(get_document_text(key))
    if not isinstance(value, dict):
        raise TypeError(f"SigmaRail spec document is not a JSON object: {key}")
    return value


__all__ = [
    "MAX_BOOL_DEPTH", "MAX_FORMULA_DEPTH", "AllExpr", "AnyExpr", "BoolExprItem",
    "DataQueryV1", "QueryAliasExpression", "QueryArithmeticExpression",
    "QueryComputedField", "QueryExpression", "QueryField", "QueryFieldExpression",
    "QueryJoin", "QueryLiteralExpression", "QueryOrder", "QueryPredicate",
    "__version__",
    "CmpEq", "CmpGt", "CmpGte", "CmpLt", "CmpLte", "ColBetweenExpr",
    "ColEqExpr", "ColGteExpr", "ColLteExpr", "ColRef", "FormulaExpr",
    "InTickersExpr", "LitVal", "NotExpr", "Operand", "RegimeAllowsEntriesExpr",
    "RegimeExpr", "RegimeMartAllowsEntriesExpr", "SignalCompareExpr", "SignalExpr",
    "SpecExpr", "WhereExpr", "bool_expr_depth", "is_runtime_only_expr",
    "parse_bool_expr", "validate_bool_expr_depth", "ENUM_TRIGGER_TYPES", "evaluate_entry_triggers",
    "compile_entry_trigger",
    "trigger_eval_row",
    "evaluate_single_trigger",
    "evaluate_slot_bool",
    "evaluate_slot_number",
    "evaluate_where_ast",
    "get_document",
    "get_document_text",
    "list_documents",
]

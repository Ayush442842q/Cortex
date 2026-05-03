"""Cortex - JSON Flattener Tool."""
from __future__ import annotations

import json
from tools import BaseTool


def _flatten(obj, prefix=""):
    rows = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            rows.update(_flatten(value, f"{prefix}.{key}" if prefix else key))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            rows.update(_flatten(value, f"{prefix}.{i}" if prefix else str(i)))
    else:
        rows[prefix] = obj
    return rows


class JsonFlattenerTool(BaseTool):
    name = "json_flattener"
    description = "Flatten nested JSON into dotted keys."
    usage_example = "json_flattener {\"a\":{\"b\":1}}"

    def run(self, input: str) -> str:
        try:
            return json.dumps(_flatten(json.loads(input)), indent=2)
        except Exception as exc:
            return f"[json_flattener] ERROR: {exc}"

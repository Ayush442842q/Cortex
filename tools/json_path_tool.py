"""Cortex - JSON Path Tool."""
from __future__ import annotations

import json
from tools import BaseTool


class JsonPathTool(BaseTool):
    name = "json_path"
    description = "Get a dotted path from JSON text. Usage: <path> | <json>."
    usage_example = "json_path user.name | {\"user\":{\"name\":\"Ada\"}}"

    def run(self, input: str) -> str:
        path, sep, raw = input.partition("|")
        if not sep:
            return "[json_path] Usage: <path> | <json>"
        try:
            obj = json.loads(raw)
            for part in path.strip().split("."):
                obj = obj[int(part)] if isinstance(obj, list) else obj[part]
            return json.dumps(obj, indent=2) if isinstance(obj, (dict, list)) else str(obj)
        except Exception as exc:
            return f"[json_path] ERROR: {exc}"

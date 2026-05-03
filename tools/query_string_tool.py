"""Cortex - Query String Tool."""
from __future__ import annotations

import json
import urllib.parse
from tools import BaseTool


class QueryStringTool(BaseTool):
    name = "query_string"
    description = "Parse URL query-string text into JSON."
    usage_example = "query_string a=1&b=hello"

    def run(self, input: str) -> str:
        query = input.strip().lstrip("?")
        return json.dumps(urllib.parse.parse_qs(query, keep_blank_values=True), indent=2)

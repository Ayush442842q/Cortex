"""Cortex - Line Sorter Tool."""
from __future__ import annotations

from tools import BaseTool


class LineSorterTool(BaseTool):
    name = "line_sorter"
    description = "Sort lines alphabetically. Prefix input with 'desc ' for descending order."
    usage_example = "line_sorter banana\napple\ncarrot"

    def run(self, input: str) -> str:
        text = input.rstrip("\n")
        reverse = text.lower().startswith("desc ")
        if reverse:
            text = text[5:]
        lines = [line for line in text.splitlines() if line.strip()]
        return "\n".join(sorted(lines, key=str.lower, reverse=reverse))

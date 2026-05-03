"""Cortex - Table Formatter Tool."""
from __future__ import annotations

from tools import BaseTool


class TableFormatterTool(BaseTool):
    name = "table_formatter"
    description = "Format pipe-separated rows as a padded text table."
    usage_example = "table_formatter name|age\nAda|36"

    def run(self, input: str) -> str:
        rows = [[cell.strip() for cell in line.split("|")] for line in input.splitlines() if line.strip()]
        if not rows:
            return "[table_formatter] Provide pipe-separated rows."
        widths = [max(len(row[i]) if i < len(row) else 0 for row in rows) for i in range(max(map(len, rows)))]
        return "\n".join(" | ".join((row[i] if i < len(row) else "").ljust(widths[i]) for i in range(len(widths))) for row in rows)

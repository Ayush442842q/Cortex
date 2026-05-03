"""Cortex - CSV to Markdown Tool."""
from __future__ import annotations

import csv
import io
from tools import BaseTool


class CsvToMarkdownTool(BaseTool):
    name = "csv_to_markdown"
    description = "Convert CSV text to a Markdown table."
    usage_example = "csv_to_markdown name,age\nAda,36"

    def run(self, input: str) -> str:
        rows = list(csv.reader(io.StringIO(input)))
        if not rows:
            return "[csv_to_markdown] No CSV rows found."
        header = rows[0]
        lines = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
        lines.extend("| " + " | ".join(row) + " |" for row in rows[1:])
        return "\n".join(lines)

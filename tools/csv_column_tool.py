"""Cortex - CSV Column Tool."""
from __future__ import annotations

import csv
import io
from tools import BaseTool


class CsvColumnTool(BaseTool):
    name = "csv_column"
    description = "Extract a named column from CSV text. Usage: <column> | <csv>."
    usage_example = "csv_column name | name,age\nAda,36"

    def run(self, input: str) -> str:
        column, sep, raw = input.partition("|")
        if not sep:
            return "[csv_column] Usage: <column> | <csv>"
        rows = csv.DictReader(io.StringIO(raw.strip()))
        values = [row.get(column.strip(), "") for row in rows]
        return "\n".join(values) if values else "[csv_column] No values found."

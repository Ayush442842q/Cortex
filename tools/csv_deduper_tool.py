"""Cortex - CSV Deduper Tool."""
from __future__ import annotations

import csv
import io
from tools import BaseTool


class CsvDeduperTool(BaseTool):
    name = "csv_deduper"
    description = "Remove duplicate CSV rows."
    usage_example = "csv_deduper a,b\n1,2\n1,2"

    def run(self, input: str) -> str:
        reader = csv.reader(io.StringIO(input))
        out, seen = [], set()
        for row in reader:
            key = tuple(row)
            if key not in seen:
                seen.add(key)
                out.append(row)
        buf = io.StringIO()
        csv.writer(buf, lineterminator="\n").writerows(out)
        return buf.getvalue().strip()

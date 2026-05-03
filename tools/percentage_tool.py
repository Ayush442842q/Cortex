"""Cortex - Percentage Tool."""
from __future__ import annotations

from tools import BaseTool


class PercentageTool(BaseTool):
    name = "percentage"
    description = "Calculate percent, percent change, or part. Commands: of <pct> <value>, change <old> <new>, part <part> <whole>."
    usage_example = "percentage change 100 125"

    def run(self, input: str) -> str:
        parts = input.split()
        try:
            if parts[0] == "of":
                return str(float(parts[1]) / 100 * float(parts[2]))
            if parts[0] == "change":
                old, new = float(parts[1]), float(parts[2])
                return f"{((new - old) / old * 100):.2f}%"
            if parts[0] == "part":
                return f"{(float(parts[1]) / float(parts[2]) * 100):.2f}%"
        except Exception:
            pass
        return "[percentage] Usage: of <pct> <value> | change <old> <new> | part <part> <whole>"

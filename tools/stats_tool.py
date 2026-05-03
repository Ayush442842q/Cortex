"""Cortex - Stats Tool."""
from __future__ import annotations

import statistics
from tools import BaseTool


class StatsTool(BaseTool):
    name = "stats"
    description = "Calculate count, sum, mean, median, min, max, and population standard deviation for numbers."
    usage_example = "stats 1 2 3 4 5"

    def run(self, input: str) -> str:
        try:
            nums = [float(x.strip(",")) for x in input.split()]
            return f"count: {len(nums)}\nsum: {sum(nums)}\nmean: {statistics.mean(nums)}\nmedian: {statistics.median(nums)}\nmin: {min(nums)}\nmax: {max(nums)}\npstdev: {statistics.pstdev(nums)}"
        except Exception as exc:
            return f"[stats] ERROR: {exc}"

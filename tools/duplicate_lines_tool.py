"""Cortex - Duplicate Lines Tool."""
from __future__ import annotations

from collections import Counter
from tools import BaseTool


class DuplicateLinesTool(BaseTool):
    name = "duplicate_lines"
    description = "Find duplicate non-empty lines and their counts."
    usage_example = "duplicate_lines apple\nbanana\napple"

    def run(self, input: str) -> str:
        counts = Counter(line.strip() for line in input.splitlines() if line.strip())
        duplicates = [(line, count) for line, count in counts.items() if count > 1]
        if not duplicates:
            return "[duplicate_lines] No duplicates found."
        return "\n".join(f"{count}x {line}" for line, count in sorted(duplicates))

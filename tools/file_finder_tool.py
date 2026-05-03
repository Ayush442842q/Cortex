"""Cortex - File Finder Tool."""
from __future__ import annotations

from pathlib import Path
from tools import BaseTool


class FileFinderTool(BaseTool):
    name = "file_finder"
    description = "Find files by glob. Usage: <root> | <pattern>."
    usage_example = "file_finder . | *.py"

    def run(self, input: str) -> str:
        root_text, sep, pattern = input.partition("|")
        if not sep:
            return "[file_finder] Usage: <root> | <pattern>"
        root = Path(root_text.strip()).expanduser()
        matches = sorted(root.rglob(pattern.strip()))
        if not matches:
            return "[file_finder] No matches."
        return "\n".join(str(p) for p in matches[:100])

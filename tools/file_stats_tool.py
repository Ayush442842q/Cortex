"""Cortex - File Stats Tool."""
from __future__ import annotations

from pathlib import Path
from tools import BaseTool


class FileStatsTool(BaseTool):
    name = "file_stats"
    description = "Show size, line count, and modified time for a file."
    usage_example = "file_stats README.md"

    def run(self, input: str) -> str:
        p = Path(input.strip()).expanduser()
        if not p.is_file():
            return f"[file_stats] File not found: {p}"
        stat = p.stat()
        try:
            lines = sum(1 for _ in p.open("rb"))
        except OSError:
            lines = 0
        return f"Size: {stat.st_size} bytes\nLines: {lines}\nModified: {stat.st_mtime}"

"""Cortex - ASCII Table Tool."""
from __future__ import annotations

from tools import BaseTool


class AsciiTableTool(BaseTool):
    name = "ascii_table"
    description = "Show printable ASCII characters and codes, optionally for a range like '65 90'."
    usage_example = "ascii_table 65 70"

    def run(self, input: str) -> str:
        parts = input.split()
        start, end = (32, 126)
        if len(parts) == 2:
            start, end = int(parts[0]), int(parts[1])
        start, end = max(0, start), min(127, end)
        return "\n".join(f"{i:3d}  0x{i:02x}  {repr(chr(i))[1:-1]}" for i in range(start, end + 1))

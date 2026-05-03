"""Cortex - Number Base Tool."""
from __future__ import annotations

from tools import BaseTool


class NumberBaseTool(BaseTool):
    name = "number_base"
    description = "Convert integers between decimal, binary, octal, and hexadecimal."
    usage_example = "number_base 255"

    def run(self, input: str) -> str:
        raw = input.strip().lower()
        if not raw:
            return "[number_base] Usage: <integer>"
        try:
            value = int(raw, 0)
            return f"dec: {value}\nbin: {bin(value)}\noct: {oct(value)}\nhex: {hex(value)}"
        except ValueError as exc:
            return f"[number_base] ERROR: {exc}"

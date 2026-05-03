"""Cortex - Roman Numeral Tool."""
from __future__ import annotations

from tools import BaseTool


PAIRS = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


class RomanNumeralTool(BaseTool):
    name = "roman_numeral"
    description = "Convert an integer from 1 to 3999 into a Roman numeral."
    usage_example = "roman_numeral 2026"

    def run(self, input: str) -> str:
        try:
            n = int(input.strip())
            if not 1 <= n <= 3999:
                return "[roman_numeral] Number must be between 1 and 3999."
            out = []
            for value, symbol in PAIRS:
                while n >= value:
                    out.append(symbol)
                    n -= value
            return "".join(out)
        except ValueError:
            return "[roman_numeral] Usage: <integer>"

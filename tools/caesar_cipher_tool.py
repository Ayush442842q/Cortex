"""Cortex - Caesar Cipher Tool."""
from __future__ import annotations

from tools import BaseTool


class CaesarCipherTool(BaseTool):
    name = "caesar_cipher"
    description = "Shift letters by N positions. Usage: <shift> <text>."
    usage_example = "caesar_cipher 3 attack at dawn"

    def run(self, input: str) -> str:
        shift_text, _, text = input.strip().partition(" ")
        try:
            shift = int(shift_text) % 26
        except ValueError:
            return "[caesar_cipher] Usage: <shift> <text>"
        out = []
        for ch in text:
            base = 65 if ch.isupper() else 97
            out.append(chr((ord(ch) - base + shift) % 26 + base) if ch.isalpha() else ch)
        return "".join(out)

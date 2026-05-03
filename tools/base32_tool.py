"""Cortex - Base32 Tool."""
from __future__ import annotations

import base64
from tools import BaseTool


class Base32Tool(BaseTool):
    name = "base32"
    description = "Base32 encode or decode text. Commands: encode <text> | decode <base32>."
    usage_example = "base32 encode hello"

    def run(self, input: str) -> str:
        cmd, _, text = input.strip().partition(" ")
        try:
            if cmd == "encode":
                return base64.b32encode(text.encode()).decode()
            if cmd == "decode":
                return base64.b32decode(text.encode()).decode(errors="replace")
        except Exception as exc:
            return f"[base32] ERROR: {exc}"
        return "[base32] Usage: encode <text> | decode <base32>"

"""Cortex - Base58 Tool."""
from __future__ import annotations

from tools import BaseTool


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


class Base58Tool(BaseTool):
    name = "base58"
    description = "Base58 encode UTF-8 text."
    usage_example = "base58 hello"

    def run(self, input: str) -> str:
        data = input.encode()
        n = int.from_bytes(data, "big")
        out = ""
        while n:
            n, rem = divmod(n, 58)
            out = ALPHABET[rem] + out
        pad = len(data) - len(data.lstrip(b"\0"))
        return "1" * pad + (out or "1")

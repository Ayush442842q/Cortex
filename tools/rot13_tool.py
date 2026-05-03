"""Cortex - ROT13 Tool."""
from __future__ import annotations

import codecs
from tools import BaseTool


class Rot13Tool(BaseTool):
    name = "rot13"
    description = "Apply ROT13 to text."
    usage_example = "rot13 hello"

    def run(self, input: str) -> str:
        return codecs.decode(input, "rot_13")

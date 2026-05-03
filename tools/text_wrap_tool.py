"""Cortex - Text Wrap Tool."""
from __future__ import annotations

import textwrap
from tools import BaseTool


class TextWrapTool(BaseTool):
    name = "text_wrap"
    description = "Wrap text to a width. Usage: <width> <text>."
    usage_example = "text_wrap 40 long text here"

    def run(self, input: str) -> str:
        width_text, _, text = input.strip().partition(" ")
        try:
            width = int(width_text)
        except ValueError:
            return "[text_wrap] Usage: <width> <text>"
        return textwrap.fill(text, width=max(10, width))

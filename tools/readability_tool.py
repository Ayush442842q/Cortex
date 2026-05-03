"""Cortex - Readability Tool."""
from __future__ import annotations

import re
from tools import BaseTool


class ReadabilityTool(BaseTool):
    name = "readability"
    description = "Estimate Flesch reading ease for English text."
    usage_example = "readability This is a short sentence."

    def run(self, input: str) -> str:
        words = re.findall(r"[A-Za-z]+", input)
        sentences = max(1, len(re.findall(r"[.!?]", input)))
        syllables = sum(max(1, len(re.findall(r"[aeiouyAEIOUY]+", w))) for w in words)
        if not words:
            return "[readability] No words found."
        score = 206.835 - 1.015 * (len(words) / sentences) - 84.6 * (syllables / len(words))
        return f"Flesch reading ease: {score:.1f}"

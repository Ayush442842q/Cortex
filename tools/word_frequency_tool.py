"""Cortex - Word Frequency Tool."""
from __future__ import annotations

import re
from collections import Counter
from tools import BaseTool


class WordFrequencyTool(BaseTool):
    name = "word_frequency"
    description = "Show the most common words in text."
    usage_example = "word_frequency hello hello cortex"

    def run(self, input: str) -> str:
        words = re.findall(r"[a-z0-9]+", input.lower())
        if not words:
            return "[word_frequency] No words found."
        return "\n".join(f"{word}: {count}" for word, count in Counter(words).most_common(20))

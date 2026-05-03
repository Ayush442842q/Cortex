"""Cortex - Sentence Splitter Tool."""
from __future__ import annotations

import re
from tools import BaseTool


class SentenceSplitterTool(BaseTool):
    name = "sentence_splitter"
    description = "Split text into numbered sentences."
    usage_example = "sentence_splitter Hello. How are you?"

    def run(self, input: str) -> str:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", input.strip()) if s.strip()]
        return "\n".join(f"{i}. {s}" for i, s in enumerate(sentences, 1)) if sentences else "[sentence_splitter] No sentences found."

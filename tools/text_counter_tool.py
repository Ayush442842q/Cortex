"""Cortex - Text Counter Tool."""
from __future__ import annotations

import re
from tools import BaseTool


class TextCounterTool(BaseTool):
    name = "text_counter"
    description = "Count characters, words, sentences, paragraphs, and lines in text."
    usage_example = "text_counter Hello world."

    def run(self, input: str) -> str:
        text = input
        words = re.findall(r"\b\w+\b", text)
        sentences = re.findall(r"[^.!?]+[.!?]", text)
        paragraphs = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
        return (
            f"Characters: {len(text)}\n"
            f"Words: {len(words)}\n"
            f"Sentences: {len(sentences)}\n"
            f"Paragraphs: {len(paragraphs)}\n"
            f"Lines: {len(text.splitlines())}"
        )

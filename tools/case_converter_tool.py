"""Cortex - Case Converter Tool."""
from __future__ import annotations

import re
from tools import BaseTool


def _words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+", text)


class CaseConverterTool(BaseTool):
    name = "case_converter"
    description = "Convert text between snake_case, kebab-case, camelCase, PascalCase, upper, lower, and title case."
    usage_example = "case_converter snake Hello world"

    def run(self, input: str) -> str:
        mode, _, text = input.strip().partition(" ")
        if not text:
            return "[case_converter] Usage: <snake|kebab|camel|pascal|upper|lower|title> <text>"
        words = _words(text)
        if mode == "snake":
            return "_".join(w.lower() for w in words)
        if mode == "kebab":
            return "-".join(w.lower() for w in words)
        if mode == "camel":
            return words[0].lower() + "".join(w.capitalize() for w in words[1:]) if words else ""
        if mode == "pascal":
            return "".join(w.capitalize() for w in words)
        if mode == "upper":
            return text.upper()
        if mode == "lower":
            return text.lower()
        if mode == "title":
            return text.title()
        return f"[case_converter] Unknown mode: {mode}"

"""Cortex - Diff Tool
Compare text snippets or files and return unified diffs.
"""
from __future__ import annotations

import difflib
from pathlib import Path

from tools import BaseTool


def _read(value: str) -> str:
    path = Path(value).expanduser()
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8", errors="replace")
    return value


class DiffTool(BaseTool):
    name = "diff"
    description = "Compare text or files. Commands: text <old> | <new>, files <old_path> | <new_path>, words <old> | <new>."
    usage_example = "diff text hello | hello world"

    def run(self, input: str) -> str:
        raw = input.strip()
        if not raw:
            return "[diff] Commands: text <old> | <new> | files <old_path> | <new_path> | words <old> | <new>"

        command, _, rest = raw.partition(" ")
        command = command.lower()
        left, sep, right = rest.partition("|")
        if not sep:
            return f"[diff] {command} needs a '|' separator."
        left = left.strip()
        right = right.strip()

        try:
            if command == "text":
                old_lines = left.splitlines()
                new_lines = right.splitlines()
                result = difflib.unified_diff(old_lines, new_lines, fromfile="old", tofile="new", lineterm="")
                return "\n".join(result) or "[diff] No differences."

            if command == "files":
                old_text, new_text = _read(left), _read(right)
                result = difflib.unified_diff(
                    old_text.splitlines(),
                    new_text.splitlines(),
                    fromfile=left,
                    tofile=right,
                    lineterm="",
                )
                return "\n".join(result) or "[diff] No differences."

            if command == "words":
                old_words = left.split()
                new_words = right.split()
                result = difflib.ndiff(old_words, new_words)
                return "\n".join(result) or "[diff] No differences."

            return f"[diff] Unknown command: {command}"
        except Exception as exc:
            return f"[diff] ERROR: {exc}"

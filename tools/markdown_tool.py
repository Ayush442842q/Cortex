"""Cortex - Markdown Tool
Inspect and transform Markdown text or files.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from tools import BaseTool


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def _slugify(text: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_-]+", "-", slug)


def _read_source(value: str) -> str:
    path = Path(value).expanduser()
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8", errors="replace")
    return value


class MarkdownTool(BaseTool):
    name = "markdown"
    description = "Work with Markdown. Commands: toc <text|file>, stats <text|file>, links <text|file>, strip <text|file>."
    usage_example = "markdown toc README.md"

    def run(self, input: str) -> str:
        raw = input.strip()
        if not raw:
            return "[markdown] Commands: toc <text|file> | stats <text|file> | links <text|file> | strip <text|file>"

        command, _, source = raw.partition(" ")
        command = command.lower()
        source = source.strip()
        if not source:
            return f"[markdown] {command} needs text or a file path."

        try:
            text = _read_source(source)

            if command == "toc":
                rows = []
                for line in text.splitlines():
                    match = HEADING_RE.match(line)
                    if not match:
                        continue
                    level = len(match.group(1))
                    title = match.group(2).strip()
                    rows.append(f"{'  ' * (level - 1)}- [{title}](#{_slugify(title)})")
                return "[markdown toc]\n" + ("\n".join(rows) if rows else "No headings found.")

            if command == "stats":
                words = re.findall(r"\b\w+\b", text)
                headings = sum(1 for line in text.splitlines() if HEADING_RE.match(line))
                links = len(re.findall(r"\[[^\]]+\]\([^)]+\)", text))
                return f"[markdown stats]\n  Lines: {len(text.splitlines())}\n  Words: {len(words)}\n  Headings: {headings}\n  Links: {links}"

            if command == "links":
                links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)
                if not links:
                    return "[markdown links] No markdown links found."
                return "[markdown links]\n" + "\n".join(f"  {label}: {url}" for label, url in links[:50])

            if command == "strip":
                stripped = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
                stripped = re.sub(r"`([^`]+)`", r"\1", stripped)
                stripped = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", stripped)
                stripped = re.sub(r"[*_>#-]+", " ", stripped)
                stripped = re.sub(r"\s+", " ", stripped).strip()
                return stripped

            return f"[markdown] Unknown command: {command}"
        except OSError as exc:
            return f"[markdown] ERROR: {exc}"

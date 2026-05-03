"""Cortex - Log Analyzer
Summarize logs and extract likely error lines.
"""
from __future__ import annotations

import os
import re
from collections import Counter
from pathlib import Path

from tools import BaseTool


LEVEL_RE = re.compile(r"\b(TRACE|DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL|FATAL)\b", re.IGNORECASE)
DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}")


def _read(value: str) -> str:
    path = Path(value).expanduser()
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8", errors="replace")
    return value


class LogAnalyzerTool(BaseTool):
    name = "logs"
    description = "Analyze logs. Commands: summary <text|file>, errors <text|file>, levels <text|file>, grep <pattern> | <text|file>."
    usage_example = "logs errors app.log"

    def run(self, input: str) -> str:
        raw = input.strip()
        if not raw:
            return "[logs] Commands: summary <text|file> | errors <text|file> | levels <text|file> | grep <pattern> | <text|file>"

        command, _, rest = raw.partition(" ")
        command = command.lower()
        rest = rest.strip()
        if not rest:
            return f"[logs] {command} needs text or a file path."

        try:
            if command == "grep":
                pattern, sep, source = rest.partition("|")
                if not sep:
                    return "[logs] Usage: grep <pattern> | <text|file>"
                rx = re.compile(pattern.strip(), re.IGNORECASE)
                text = _read(source.strip())
                matches = [line for line in text.splitlines() if rx.search(line)]
                return "[logs grep]\n" + ("\n".join(matches[:50]) if matches else "No matches.")

            text = _read(rest)
            lines = text.splitlines()
            levels = Counter()
            timestamps = 0
            for line in lines:
                match = LEVEL_RE.search(line)
                if match:
                    level = match.group(1).upper()
                    if level == "WARNING":
                        level = "WARN"
                    levels[level] += 1
                if DATE_RE.search(line):
                    timestamps += 1

            if command == "levels":
                if not levels:
                    return "[logs levels] No log levels detected."
                return "[logs levels]\n" + "\n".join(f"  {level}: {count}" for level, count in levels.most_common())

            if command == "errors":
                error_lines = [
                    line for line in lines
                    if re.search(r"\b(error|critical|fatal|exception|traceback|failed)\b", line, re.IGNORECASE)
                ]
                return "[logs errors]\n" + ("\n".join(error_lines[:50]) if error_lines else "No likely error lines found.")

            if command == "summary":
                return (
                    "[logs summary]\n"
                    f"  Lines: {len(lines)}\n"
                    f"  Timestamped lines: {timestamps}\n"
                    f"  Levels: {dict(levels)}"
                )

            return f"[logs] Unknown command: {command}"
        except Exception as exc:
            return f"[logs] ERROR: {exc}"

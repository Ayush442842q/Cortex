"""Cortex - Project Inspector
Summarize a source tree without external dependencies.
"""
from __future__ import annotations

import os
from collections import Counter
from pathlib import Path

from tools import BaseTool


IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
}


def _walk(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for name in files:
            yield Path(current) / name


def _line_count(path: Path) -> int:
    try:
        with open(path, "rb") as handle:
            return sum(1 for _ in handle)
    except OSError:
        return 0


class ProjectInspectorTool(BaseTool):
    name = "project_inspector"
    description = "Inspect a project tree. Commands: summary <path>, tree <path> [depth], extensions <path>, todos <path>."
    usage_example = "project_inspector summary ."

    def run(self, input: str) -> str:
        raw = input.strip()
        if not raw:
            return "[project_inspector] Commands: summary <path> | tree <path> [depth] | extensions <path> | todos <path>"

        parts = raw.split()
        command = parts[0].lower()
        root = Path(parts[1] if len(parts) > 1 else ".").expanduser()
        if not root.exists():
            return f"[project_inspector] Path not found: {root}"

        try:
            if command == "summary":
                files = list(_walk(root))
                by_ext = Counter(path.suffix.lower() or "[none]" for path in files)
                total_bytes = sum(path.stat().st_size for path in files if path.exists())
                total_lines = sum(_line_count(path) for path in files if path.suffix.lower() in {".py", ".md", ".txt", ".toml", ".yml", ".yaml", ".json"})
                lines = [
                    f"[project summary: {root.resolve()}]",
                    f"  Files : {len(files)}",
                    f"  Bytes : {total_bytes:,}",
                    f"  Lines : {total_lines:,} text/source lines",
                    "  Top extensions:",
                ]
                lines.extend(f"    {ext}: {count}" for ext, count in by_ext.most_common(10))
                return "\n".join(lines)

            if command == "extensions":
                files = list(_walk(root))
                by_ext = Counter(path.suffix.lower() or "[none]" for path in files)
                return "[project extensions]\n" + "\n".join(f"  {ext}: {count}" for ext, count in by_ext.most_common())

            if command == "tree":
                depth = int(parts[2]) if len(parts) > 2 else 2
                root_resolved = root.resolve()
                rows = [f"{root_resolved.name}/"]
                for path in sorted(_walk(root)):
                    rel = path.relative_to(root)
                    if len(rel.parts) > depth:
                        continue
                    rows.append("  " * (len(rel.parts) - 1) + f"- {rel.name}")
                    if len(rows) >= 80:
                        rows.append("... truncated")
                        break
                return "\n".join(rows)

            if command == "todos":
                markers = ("TODO", "FIXME", "HACK", "XXX")
                matches = []
                for path in _walk(root):
                    if path.suffix.lower() not in {".py", ".md", ".txt", ".toml", ".yml", ".yaml", ".json"}:
                        continue
                    try:
                        for index, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                            if any(marker in line for marker in markers):
                                matches.append(f"{path}:{index}: {line.strip()}")
                    except OSError:
                        continue
                if not matches:
                    return "[project todos] No TODO/FIXME/HACK/XXX markers found."
                return "[project todos]\n" + "\n".join(f"  {line}" for line in matches[:50])

            return f"[project_inspector] Unknown command: {command}"
        except Exception as exc:
            return f"[project_inspector] ERROR: {exc}"

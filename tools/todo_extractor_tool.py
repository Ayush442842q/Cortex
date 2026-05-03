"""Cortex - TODO Extractor Tool."""
from __future__ import annotations

from pathlib import Path
from tools import BaseTool


class TodoExtractorTool(BaseTool):
    name = "todo_extractor"
    description = "Extract TODO, FIXME, HACK, and XXX markers from text files under a path."
    usage_example = "todo_extractor ."

    def run(self, input: str) -> str:
        root = Path(input.strip() or ".").expanduser()
        markers = ("TODO", "FIXME", "HACK", "XXX")
        hits = []
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".py", ".md", ".txt", ".toml", ".yml", ".yaml", ".json"}:
                for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                    if any(m in line for m in markers):
                        hits.append(f"{path}:{i}: {line.strip()}")
        return "\n".join(hits[:100]) if hits else "[todo_extractor] No markers found."

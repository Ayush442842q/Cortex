"""Cortex - Path Utils Tool."""
from __future__ import annotations

from pathlib import Path
from tools import BaseTool


class PathUtilsTool(BaseTool):
    name = "path_utils"
    description = "Inspect path parts: absolute path, name, suffix, parent, and stem."
    usage_example = "path_utils ./tools/example.py"

    def run(self, input: str) -> str:
        p = Path(input.strip()).expanduser()
        return f"absolute: {p.resolve()}\nparent: {p.parent}\nname: {p.name}\nstem: {p.stem}\nsuffix: {p.suffix}"

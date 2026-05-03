"""Cortex - TOML Keys Tool."""
from __future__ import annotations

import tomllib
from pathlib import Path
from tools import BaseTool


class TomlKeysTool(BaseTool):
    name = "toml_keys"
    description = "List top-level keys in a TOML file."
    usage_example = "toml_keys pyproject.toml"

    def run(self, input: str) -> str:
        path = Path(input.strip()).expanduser()
        if not path.is_file():
            return f"[toml_keys] File not found: {path}"
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        return "\n".join(sorted(data.keys())) or "[toml_keys] No keys found."

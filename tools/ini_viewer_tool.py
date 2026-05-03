"""Cortex - INI Viewer Tool."""
from __future__ import annotations

import configparser
import json
from pathlib import Path
from tools import BaseTool


class IniViewerTool(BaseTool):
    name = "ini_viewer"
    description = "Read an INI file and return sections/values as JSON."
    usage_example = "ini_viewer setup.cfg"

    def run(self, input: str) -> str:
        path = Path(input.strip()).expanduser()
        if not path.is_file():
            return f"[ini_viewer] File not found: {path}"
        parser = configparser.ConfigParser()
        parser.read(path, encoding="utf-8")
        return json.dumps({section: dict(parser[section]) for section in parser.sections()}, indent=2)

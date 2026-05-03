"""Cortex - Slugify Tool."""
from __future__ import annotations

import re
import unicodedata
from tools import BaseTool


class SlugifyTool(BaseTool):
    name = "slugify"
    description = "Turn text into a URL-safe slug."
    usage_example = "slugify My New Blog Post!"

    def run(self, input: str) -> str:
        text = unicodedata.normalize("NFKD", input.strip()).encode("ascii", "ignore").decode()
        text = re.sub(r"[^\w\s-]", "", text.lower())
        return re.sub(r"[-\s_]+", "-", text).strip("-") or "[slugify] Empty slug."

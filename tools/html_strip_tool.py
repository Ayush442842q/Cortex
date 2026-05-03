"""Cortex - HTML Strip Tool."""
from __future__ import annotations

import html
import re
from tools import BaseTool


class HtmlStripTool(BaseTool):
    name = "html_strip"
    description = "Strip HTML tags and unescape entities."
    usage_example = "html_strip <p>Hello &amp; welcome</p>"

    def run(self, input: str) -> str:
        text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", input, flags=re.I | re.S)
        text = re.sub(r"<[^>]+>", " ", text)
        return re.sub(r"\s+", " ", html.unescape(text)).strip()

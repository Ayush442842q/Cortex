"""Cortex - HTML Link Extractor Tool."""
from __future__ import annotations

import re
from tools import BaseTool


class HtmlLinkExtractorTool(BaseTool):
    name = "html_link_extractor"
    description = "Extract href URLs from HTML anchor tags."
    usage_example = "html_link_extractor <a href='https://example.com'>x</a>"

    def run(self, input: str) -> str:
        links = re.findall(r"<a\s+[^>]*href=['\"]([^'\"]+)['\"]", input, flags=re.I)
        return "\n".join(links) if links else "[html_link_extractor] No links found."

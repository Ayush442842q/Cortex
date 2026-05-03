"""Cortex - Robots Parser Tool."""
from __future__ import annotations

from tools import BaseTool


class RobotsParserTool(BaseTool):
    name = "robots_parser"
    description = "Summarize User-agent, Allow, Disallow, and Sitemap lines from robots.txt text."
    usage_example = "robots_parser User-agent: *\nDisallow: /admin"

    def run(self, input: str) -> str:
        rows = []
        for line in input.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and ":" in line:
                key, value = line.split(":", 1)
                if key.lower() in {"user-agent", "allow", "disallow", "sitemap"}:
                    rows.append(f"{key.strip()}: {value.strip()}")
        return "\n".join(rows) if rows else "[robots_parser] No robots directives found."

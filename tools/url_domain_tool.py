"""Cortex - URL Domain Tool."""
from __future__ import annotations

import urllib.parse
from tools import BaseTool


class UrlDomainTool(BaseTool):
    name = "url_domain"
    description = "Extract scheme, host, port, and registrable-looking domain from a URL."
    usage_example = "url_domain https://sub.example.com:8080/path"

    def run(self, input: str) -> str:
        parsed = urllib.parse.urlparse(input.strip())
        host = parsed.hostname or ""
        parts = host.split(".")
        domain = ".".join(parts[-2:]) if len(parts) >= 2 else host
        return f"scheme: {parsed.scheme}\nhost: {host}\nport: {parsed.port or ''}\ndomain: {domain}"

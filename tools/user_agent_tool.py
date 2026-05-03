"""Cortex - User Agent Tool."""
from __future__ import annotations

import re
from tools import BaseTool


class UserAgentTool(BaseTool):
    name = "user_agent"
    description = "Do a lightweight parse of a browser user-agent string."
    usage_example = "user_agent Mozilla/5.0 ..."

    def run(self, input: str) -> str:
        ua = input.strip()
        browser = "Unknown"
        for name in ("Chrome", "Firefox", "Safari", "Edge", "Opera"):
            if name.lower() in ua.lower():
                browser = name
                break
        os_name = "Windows" if "Windows" in ua else "macOS" if "Mac OS" in ua else "Linux" if "Linux" in ua else "Android" if "Android" in ua else "iOS" if re.search(r"iPhone|iPad", ua) else "Unknown"
        mobile = bool(re.search(r"Mobile|Android|iPhone|iPad", ua, re.I))
        return f"Browser: {browser}\nOS: {os_name}\nMobile: {mobile}"

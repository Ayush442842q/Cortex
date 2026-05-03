"""Cortex - URL Tool
Parse, build, and modify URLs.
"""
from __future__ import annotations

import json
import urllib.parse

from tools import BaseTool


class UrlTool(BaseTool):
    name = "url"
    description = "Parse and modify URLs. Commands: parse <url>, query <url>, add-query <url> | key=value [key=value...], join <base> | <path>."
    usage_example = "url parse https://example.com/search?q=cortex"

    def run(self, input: str) -> str:
        raw = input.strip()
        if not raw:
            return "[url] Commands: parse <url> | query <url> | add-query <url> | key=value ... | join <base> | <path>"

        command, _, rest = raw.partition(" ")
        command = command.lower()
        rest = rest.strip()
        if not rest:
            return f"[url] {command} needs input."

        try:
            if command == "parse":
                parsed = urllib.parse.urlparse(rest)
                data = {
                    "scheme": parsed.scheme,
                    "netloc": parsed.netloc,
                    "path": parsed.path,
                    "params": parsed.params,
                    "query": parsed.query,
                    "fragment": parsed.fragment,
                }
                return json.dumps(data, indent=2)

            if command == "query":
                parsed = urllib.parse.urlparse(rest)
                query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
                return json.dumps(query, indent=2)

            if command == "add-query":
                url_part, sep, params_part = rest.partition("|")
                if not sep:
                    return "[url] Usage: add-query <url> | key=value [key=value...]"
                parsed = urllib.parse.urlparse(url_part.strip())
                query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
                for item in params_part.split():
                    if "=" not in item:
                        return f"[url] Invalid query pair: {item}"
                    key, value = item.split("=", 1)
                    query.append((key, value))
                new_query = urllib.parse.urlencode(query)
                return urllib.parse.urlunparse(parsed._replace(query=new_query))

            if command == "join":
                base, sep, path = rest.partition("|")
                if not sep:
                    return "[url] Usage: join <base> | <path>"
                return urllib.parse.urljoin(base.strip(), path.strip())

            return f"[url] Unknown command: {command}"
        except Exception as exc:
            return f"[url] ERROR: {exc}"

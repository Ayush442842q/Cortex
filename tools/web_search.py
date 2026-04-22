"""
Cortex — Web Search Tool (Week 5)
Searches the web using DuckDuckGo (no API key needed).
"""
from __future__ import annotations
import sys, json, urllib.request, urllib.parse, html, re

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name: str = ""
        description: str = ""
        usage_example: str = ""
        def run(self, user_input: str) -> str:
            raise NotImplementedError

def _ddg_search(query: str, max_results: int = 5) -> list[dict]:
    encoded = urllib.parse.quote_plus(query)
    url = (
        f"https://api.duckduckgo.com/?q={encoded}"
        "&format=json&no_html=1&skip_disambig=1"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Cortex-Agent/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    results = []
    if data.get("AbstractText"):
        results.append({
            "title": data.get("Heading", "Abstract"),
            "url": data.get("AbstractURL", ""),
            "snippet": data["AbstractText"],
        })
    for topic in data.get("RelatedTopics", []):
        if len(results) >= max_results:
            break
        if "Topics" in topic:
            for sub in topic["Topics"]:
                if len(results) >= max_results:
                    break
                text = html.unescape(re.sub(r"<[^>]+>", "", sub.get("Text", "")))
                if text:
                    results.append({"title": text[:80], "url": sub.get("FirstURL", ""), "snippet": text})
        else:
            text = html.unescape(re.sub(r"<[^>]+>", "", topic.get("Text", "")))
            if text:
                results.append({"title": text[:80], "url": topic.get("FirstURL", ""), "snippet": text})
    return results

def _fetch_page(url: str, max_chars: int = 2000) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Cortex-Agent/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read().decode(errors="replace")
    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]

class WebSearchTool(BaseTool):
    name = "web_search"
    description = (
        "Search the web for up-to-date information. "
        "Commands: search <query> | fetch <url>"
    )
    usage_example = "web_search search Python async tutorial"
    MAX_RESULTS = 5

    def run(self, user_input: str) -> str:
        user_input = user_input.strip()
        if not user_input:
            return "[web_search] Provide: search <query> | fetch <url>"
        parts = user_input.split(None, 1)
        cmd = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""
        if cmd == "fetch":
            if not arg:
                return "[web_search] fetch requires a URL."
            try:
                return f"[Fetched: {arg}]\n{_fetch_page(arg)}"
            except Exception as exc:
                return f"[web_search] fetch failed: {exc}"
        query = arg if cmd == "search" else user_input
        if not query:
            return "[web_search] search requires a query."
        try:
            results = _ddg_search(query, max_results=self.MAX_RESULTS)
        except Exception as exc:
            return f"[web_search] search failed: {exc}"
        if not results:
            return f"[web_search] No results found for: {query}"
        lines = [f"[Search results for: {query}]"]
        for i, r in enumerate(results, 1):
            lines.append(f"\n{i}. {r['title']}")
            if r["url"]:
                lines.append(f"   URL: {r['url']}")
            lines.append(f"   {r['snippet']}")
        return "\n".join(lines)
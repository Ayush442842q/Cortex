"""Cortex - HTTP Status Tool."""
from __future__ import annotations

from http import HTTPStatus
from tools import BaseTool


class HttpStatusTool(BaseTool):
    name = "http_status"
    description = "Explain HTTP status codes."
    usage_example = "http_status 404"

    def run(self, input: str) -> str:
        try:
            status = HTTPStatus(int(input.strip()))
            return f"{status.value} {status.phrase}: {status.description}"
        except Exception:
            return "[http_status] Unknown HTTP status code."

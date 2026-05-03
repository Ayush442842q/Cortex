"""Cortex - MIME Lookup Tool."""
from __future__ import annotations

import mimetypes
from tools import BaseTool


class MimeLookupTool(BaseTool):
    name = "mime_lookup"
    description = "Guess MIME type from a filename or extension."
    usage_example = "mime_lookup report.pdf"

    def run(self, input: str) -> str:
        mime, encoding = mimetypes.guess_type(input.strip())
        return f"MIME: {mime or 'unknown'}\nEncoding: {encoding or 'none'}"

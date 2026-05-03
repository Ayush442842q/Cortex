"""Cortex - Encoding Tool
Encode, decode, and inspect common text representations.
"""
from __future__ import annotations

import base64
import binascii
import html
import urllib.parse

from tools import BaseTool


class EncodingTool(BaseTool):
    name = "encoding"
    description = "Encode and decode text. Commands: base64-encode, base64-decode, url-encode, url-decode, html-escape, html-unescape, hex-encode, hex-decode."
    usage_example = "encoding base64-encode hello world"

    def run(self, input: str) -> str:
        raw = input.strip()
        if not raw:
            return "[encoding] Commands: base64-encode | base64-decode | url-encode | url-decode | html-escape | html-unescape | hex-encode | hex-decode"

        command, _, value = raw.partition(" ")
        command = command.lower()
        value = value.strip()
        if not value:
            return f"[encoding] {command} needs input text."

        try:
            if command in ("base64-encode", "b64e"):
                return base64.b64encode(value.encode("utf-8")).decode("ascii")
            if command in ("base64-decode", "b64d"):
                return base64.b64decode(value.encode("ascii"), validate=True).decode("utf-8", errors="replace")
            if command in ("url-encode", "quote"):
                return urllib.parse.quote(value, safe="")
            if command in ("url-decode", "unquote"):
                return urllib.parse.unquote(value)
            if command == "html-escape":
                return html.escape(value)
            if command == "html-unescape":
                return html.unescape(value)
            if command == "hex-encode":
                return value.encode("utf-8").hex()
            if command == "hex-decode":
                return bytes.fromhex(value).decode("utf-8", errors="replace")
            return f"[encoding] Unknown command: {command}"
        except (binascii.Error, ValueError, UnicodeDecodeError) as exc:
            return f"[encoding] ERROR: {exc}"

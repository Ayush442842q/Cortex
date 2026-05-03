"""Cortex - JWT Decoder Tool."""
from __future__ import annotations

import base64
import json
from tools import BaseTool


def _decode_part(part: str) -> dict:
    padded = part + "=" * (-len(part) % 4)
    return json.loads(base64.urlsafe_b64decode(padded.encode()).decode())


class JwtDecoderTool(BaseTool):
    name = "jwt_decoder"
    description = "Decode JWT header and payload without verifying the signature."
    usage_example = "jwt_decoder eyJhbGciOi..."

    def run(self, input: str) -> str:
        parts = input.strip().split(".")
        if len(parts) < 2:
            return "[jwt_decoder] Usage: <jwt>"
        try:
            return json.dumps({"header": _decode_part(parts[0]), "payload": _decode_part(parts[1])}, indent=2)
        except Exception as exc:
            return f"[jwt_decoder] ERROR: {exc}"

"""Cortex - Random Tool
Generate UUIDs, tokens, and random choices.
"""
from __future__ import annotations

import secrets
import string
import uuid

from tools import BaseTool


class RandomTool(BaseTool):
    name = "random"
    description = "Generate UUIDs, secure tokens, random integers, choices, and strings. Commands: uuid, token [bytes], int <min> <max>, choice <items...>, string [length]."
    usage_example = "random token 32"

    def run(self, input: str) -> str:
        raw = input.strip()
        if not raw:
            return "[random] Commands: uuid | token [bytes] | int <min> <max> | choice <items...> | string [length]"

        parts = raw.split()
        command = parts[0].lower()

        try:
            if command == "uuid":
                return str(uuid.uuid4())

            if command == "token":
                size = int(parts[1]) if len(parts) > 1 else 32
                if size < 1 or size > 4096:
                    return "[random] token bytes must be between 1 and 4096."
                return secrets.token_urlsafe(size)

            if command == "int":
                if len(parts) != 3:
                    return "[random] Usage: int <min> <max>"
                lo, hi = int(parts[1]), int(parts[2])
                if lo > hi:
                    lo, hi = hi, lo
                return str(secrets.randbelow(hi - lo + 1) + lo)

            if command == "choice":
                if len(parts) < 2:
                    return "[random] Usage: choice <item> [item...]"
                return secrets.choice(parts[1:])

            if command == "string":
                length = int(parts[1]) if len(parts) > 1 else 24
                if length < 1 or length > 4096:
                    return "[random] string length must be between 1 and 4096."
                alphabet = string.ascii_letters + string.digits
                return "".join(secrets.choice(alphabet) for _ in range(length))

            return f"[random] Unknown command: {command}"
        except Exception as exc:
            return f"[random] ERROR: {exc}"

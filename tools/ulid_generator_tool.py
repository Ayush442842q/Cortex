"""Cortex - ULID Generator Tool."""
from __future__ import annotations

import secrets
import time
from tools import BaseTool


ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def _encode(value: int, length: int) -> str:
    out = []
    for _ in range(length):
        out.append(ALPHABET[value & 31])
        value >>= 5
    return "".join(reversed(out))


class UlidGeneratorTool(BaseTool):
    name = "ulid_generator"
    description = "Generate a ULID-like sortable identifier."
    usage_example = "ulid_generator"

    def run(self, input: str) -> str:
        timestamp_ms = int(time.time() * 1000)
        random_bits = secrets.randbits(80)
        return _encode(timestamp_ms, 10) + _encode(random_bits, 16)

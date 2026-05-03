"""Cortex - UUID Inspector Tool."""
from __future__ import annotations

import uuid
from tools import BaseTool


class UuidInspectorTool(BaseTool):
    name = "uuid_inspector"
    description = "Inspect UUID version, variant, and integer value."
    usage_example = "uuid_inspector 550e8400-e29b-41d4-a716-446655440000"

    def run(self, input: str) -> str:
        try:
            value = uuid.UUID(input.strip())
            return f"version: {value.version}\nvariant: {value.variant}\nint: {value.int}"
        except ValueError as exc:
            return f"[uuid_inspector] ERROR: {exc}"

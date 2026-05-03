"""Cortex - License Header Tool."""
from __future__ import annotations

from tools import BaseTool


class LicenseHeaderTool(BaseTool):
    name = "license_header"
    description = "Generate a short license header for MIT, Apache-2.0, or GPL-3.0."
    usage_example = "license_header MIT Ayush 2026"

    def run(self, input: str) -> str:
        parts = input.split()
        license_id = parts[0] if parts else "MIT"
        owner = parts[1] if len(parts) > 1 else "Author"
        year = parts[2] if len(parts) > 2 else "2026"
        if license_id.lower() == "mit":
            return f"Copyright (c) {year} {owner}\nLicensed under the MIT License."
        if license_id.lower() in {"apache", "apache-2.0"}:
            return f"Copyright {year} {owner}\nLicensed under the Apache License, Version 2.0."
        if license_id.lower() in {"gpl", "gpl-3.0"}:
            return f"Copyright (C) {year} {owner}\nLicensed under the GNU GPLv3."
        return f"[license_header] Unknown license: {license_id}"

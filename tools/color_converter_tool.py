"""Cortex - Color Converter Tool."""
from __future__ import annotations

from tools import BaseTool


class ColorConverterTool(BaseTool):
    name = "color_converter"
    description = "Convert colors between hex and RGB. Use 'hex #336699' or 'rgb 51 102 153'."
    usage_example = "color_converter hex #336699"

    def run(self, input: str) -> str:
        parts = input.strip().replace(",", " ").split()
        if len(parts) < 2:
            return "[color_converter] Usage: hex <#rrggbb> | rgb <r> <g> <b>"
        mode = parts[0].lower()
        try:
            if mode == "hex":
                value = parts[1].lstrip("#")
                if len(value) == 3:
                    value = "".join(ch * 2 for ch in value)
                r, g, b = int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
                return f"rgb({r}, {g}, {b})"
            if mode == "rgb" and len(parts) >= 4:
                r, g, b = [max(0, min(255, int(x))) for x in parts[1:4]]
                return f"#{r:02x}{g:02x}{b:02x}"
            return "[color_converter] Unknown mode."
        except Exception as exc:
            return f"[color_converter] ERROR: {exc}"

"""Cortex - Unit Converter Tool."""
from __future__ import annotations

from tools import BaseTool


FACTORS = {"m_to_ft": 3.28084, "ft_to_m": 0.3048, "km_to_mi": 0.621371, "mi_to_km": 1.60934, "kg_to_lb": 2.20462, "lb_to_kg": 0.453592}


class UnitConverterTool(BaseTool):
    name = "unit_converter"
    description = "Convert simple units. Usage: <conversion> <value>, e.g. km_to_mi 5."
    usage_example = "unit_converter km_to_mi 10"

    def run(self, input: str) -> str:
        conv, _, value = input.strip().partition(" ")
        try:
            if conv == "c_to_f":
                return str(float(value) * 9 / 5 + 32)
            if conv == "f_to_c":
                return str((float(value) - 32) * 5 / 9)
            return str(float(value) * FACTORS[conv])
        except Exception:
            return f"[unit_converter] Available: {', '.join(sorted([*FACTORS, 'c_to_f', 'f_to_c']))}"

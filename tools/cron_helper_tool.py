"""Cortex - Cron Helper Tool."""
from __future__ import annotations

from tools import BaseTool


class CronHelperTool(BaseTool):
    name = "cron_helper"
    description = "Explain simple five-field cron expressions."
    usage_example = "cron_helper */5 * * * *"

    def run(self, input: str) -> str:
        fields = input.split()
        if len(fields) != 5:
            return "[cron_helper] Usage: <minute> <hour> <day-of-month> <month> <day-of-week>"
        labels = ["minute", "hour", "day of month", "month", "day of week"]
        return "\n".join(f"{label}: {value}" for label, value in zip(labels, fields))

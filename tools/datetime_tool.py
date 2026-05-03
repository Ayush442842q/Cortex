"""Cortex - Date and Time Tool
Format timestamps, convert time zones, and do simple date arithmetic.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from tools import BaseTool


def _parse_dt(value: str) -> datetime:
    if value.lower() == "now":
        return datetime.now(timezone.utc)
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


class DateTimeTool(BaseTool):
    name = "datetime"
    description = "Work with dates and time zones. Commands: now [zone], convert <datetime> | <zone>, add <datetime> | <days>, diff <a> | <b>."
    usage_example = "datetime convert 2026-05-04T10:00:00+00:00 | Asia/Kolkata"

    def run(self, input: str) -> str:
        raw = input.strip()
        if not raw:
            return "[datetime] Commands: now [zone] | convert <datetime> | <zone> | add <datetime> | <days> | diff <a> | <b>"

        command, _, rest = raw.partition(" ")
        command = command.lower()
        rest = rest.strip()

        try:
            if command == "now":
                zone = rest or "UTC"
                current = datetime.now(ZoneInfo(zone))
                return current.isoformat(timespec="seconds")

            if command == "convert":
                value, sep, zone = rest.partition("|")
                if not sep:
                    return "[datetime] Usage: convert <datetime> | <zone>"
                converted = _parse_dt(value.strip()).astimezone(ZoneInfo(zone.strip()))
                return converted.isoformat(timespec="seconds")

            if command == "add":
                value, sep, days = rest.partition("|")
                if not sep:
                    return "[datetime] Usage: add <datetime> | <days>"
                result = _parse_dt(value.strip()) + timedelta(days=float(days.strip()))
                return result.isoformat(timespec="seconds")

            if command == "diff":
                left, sep, right = rest.partition("|")
                if not sep:
                    return "[datetime] Usage: diff <datetime_a> | <datetime_b>"
                delta = _parse_dt(right.strip()) - _parse_dt(left.strip())
                seconds = int(delta.total_seconds())
                return f"{seconds} seconds ({seconds / 86400:.2f} days)"

            return f"[datetime] Unknown command: {command}"
        except ZoneInfoNotFoundError as exc:
            return f"[datetime] Unknown timezone: {exc}"
        except Exception as exc:
            return f"[datetime] ERROR: {exc}"

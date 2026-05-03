"""Cortex - Password Strength Tool."""
from __future__ import annotations

import re
from tools import BaseTool


class PasswordStrengthTool(BaseTool):
    name = "password_strength"
    description = "Estimate password strength using simple local heuristics."
    usage_example = "password_strength correct-horse-battery-staple"

    def run(self, input: str) -> str:
        pw = input.strip()
        score = 0
        checks = {
            "length>=12": len(pw) >= 12,
            "lower": bool(re.search(r"[a-z]", pw)),
            "upper": bool(re.search(r"[A-Z]", pw)),
            "digit": bool(re.search(r"\d", pw)),
            "symbol": bool(re.search(r"[^A-Za-z0-9]", pw)),
        }
        score = sum(checks.values())
        label = "weak" if score <= 2 else "medium" if score <= 4 else "strong"
        return f"Strength: {label}\nScore: {score}/5\n" + "\n".join(f"{k}: {v}" for k, v in checks.items())

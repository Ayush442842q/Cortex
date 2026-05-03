"""Cortex - Env Var Checker Tool."""
from __future__ import annotations

import os
from tools import BaseTool


class EnvVarCheckerTool(BaseTool):
    name = "env_var_checker"
    description = "Check whether environment variables are set."
    usage_example = "env_var_checker PATH GROQ_API_KEY"

    def run(self, input: str) -> str:
        keys = input.split()
        if not keys:
            return "[env_var_checker] Usage: <VAR> [VAR...]"
        return "\n".join(f"{key}: {'set' if os.environ.get(key) else 'missing'}" for key in keys)

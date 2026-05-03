"""Cortex - Env File Tool
Read, validate, and update .env-style files.
"""
from __future__ import annotations

import os
from pathlib import Path

from tools import BaseTool


def _parse_env(path: Path) -> tuple[list[str], dict[str, str]]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines() if path.exists() else []
    values: dict[str, str] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return lines, values


class EnvFileTool(BaseTool):
    name = "env_file"
    description = "Inspect and edit .env files. Commands: list <file>, get <file> <key>, set <file> <key> <value>, unset <file> <key>, validate <file>."
    usage_example = "env_file list .env"

    def run(self, input: str) -> str:
        raw = input.strip()
        if not raw:
            return "[env_file] Commands: list <file> | get <file> <key> | set <file> <key> <value> | unset <file> <key> | validate <file>"

        parts = raw.split(None, 3)
        command = parts[0].lower()

        try:
            if command in ("list", "validate"):
                if len(parts) < 2:
                    return f"[env_file] Usage: {command} <file>"
                path = Path(parts[1]).expanduser()
                lines, values = _parse_env(path)
                if command == "list":
                    if not values:
                        return "[env_file] No variables found."
                    return "[env_file variables]\n" + "\n".join(f"  {key}=<set>" for key in sorted(values))
                invalid = []
                for idx, line in enumerate(lines, 1):
                    stripped = line.strip()
                    if not stripped or stripped.startswith("#"):
                        continue
                    if "=" not in stripped or not stripped.split("=", 1)[0].strip().replace("_", "").isalnum():
                        invalid.append(f"line {idx}: {line}")
                return "[env_file] Valid .env file." if not invalid else "[env_file invalid]\n" + "\n".join(invalid)

            if command == "get":
                if len(parts) < 3:
                    return "[env_file] Usage: get <file> <key>"
                path = Path(parts[1]).expanduser()
                _, values = _parse_env(path)
                key = parts[2]
                return values.get(key, f"[env_file] {key} is not set.")

            if command == "set":
                if len(parts) < 4:
                    return "[env_file] Usage: set <file> <key> <value>"
                path = Path(parts[1]).expanduser()
                key, value = parts[2], parts[3]
                path.parent.mkdir(parents=True, exist_ok=True)
                lines, values = _parse_env(path)
                updated = False
                output = []
                for line in lines:
                    if line.strip().startswith(f"{key}="):
                        output.append(f"{key}={value}")
                        updated = True
                    else:
                        output.append(line)
                if not updated:
                    output.append(f"{key}={value}")
                path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
                return f"[env_file] Set {key} in {path}."

            if command == "unset":
                if len(parts) < 3:
                    return "[env_file] Usage: unset <file> <key>"
                path = Path(parts[1]).expanduser()
                key = parts[2]
                if not path.exists():
                    return f"[env_file] File not found: {path}"
                lines, _ = _parse_env(path)
                output = [line for line in lines if not line.strip().startswith(f"{key}=")]
                path.write_text("\n".join(output).rstrip() + ("\n" if output else ""), encoding="utf-8")
                return f"[env_file] Removed {key} from {path}."

            return f"[env_file] Unknown command: {command}"
        except Exception as exc:
            return f"[env_file] ERROR: {exc}"

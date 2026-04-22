"""
Cortex — Prompt Manager Tool (Week 8)
Save, load, list, delete, and run prompt templates.
Stored in ~/.cortex/prompts/
"""
from __future__ import annotations
import sys, os, re
from pathlib import Path

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name: str = ""
        description: str = ""
        usage_example: str = ""
        def run(self, user_input: str) -> str:
            raise NotImplementedError

PROMPTS_DIR = Path.home() / ".cortex" / "prompts"
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

def _safe_name(name): return re.sub(r"[^a-zA-Z0-9_\-]", "_", name.strip())[:64]
def _path(name): return PROMPTS_DIR / f"{_safe_name(name)}.txt"

class PromptManagerTool(BaseTool):
    name = "prompt"
    description = (
        "Manage prompt templates.\n"
        "  prompt save <n> | <text>   -- save\n"
        "  prompt load <n>            -- show\n"
        "  prompt list                -- list all\n"
        "  prompt delete <n>          -- delete\n"
        "  prompt run <n> [k=v ...]   -- fill {{vars}} and return"
    )
    usage_example = "prompt save greet | Hello, {{name}}!"

    def run(self, user_input: str) -> str:
        user_input = user_input.strip()
        if not user_input:
            return "[prompt] Commands: save | load | list | delete | run"
        parts = user_input.split(None, 1)
        cmd, rest = parts[0].lower(), (parts[1].strip() if len(parts) > 1 else "")
        if cmd == "save":
            if "|" not in rest:
                return "[prompt] save: use 'save <name> | <text>'"
            name, text = rest.split("|", 1)
            name, text = name.strip(), text.strip()
            if not name or not text:
                return "[prompt] Name and text required."
            _path(name).write_text(text, encoding="utf-8")
            return f"[prompt] Saved '{name}'."
        elif cmd == "load":
            p = _path(rest)
            if not p.exists(): return f"[prompt] '{rest}' not found."
            return f"[prompt: {rest}]\n{p.read_text(encoding='utf-8')}"
        elif cmd == "list":
            files = sorted(PROMPTS_DIR.glob("*.txt"))
            if not files: return "[prompt] No saved prompts."
            return "[Saved prompts]\n" + "\n".join(f"  {f.stem}" for f in files)
        elif cmd == "delete":
            p = _path(rest)
            if not p.exists(): return f"[prompt] '{rest}' not found."
            p.unlink()
            return f"[prompt] Deleted '{rest}'."
        elif cmd == "run":
            parts2 = rest.split()
            if not parts2: return "[prompt] run needs a name."
            name = parts2[0]
            p = _path(name)
            if not p.exists(): return f"[prompt] '{name}' not found."
            text = p.read_text(encoding="utf-8")
            for pair in parts2[1:]:
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    text = text.replace("{{" + k.strip() + "}}", v.strip())
            remaining = re.findall(r"\{\{(\w+)\}\}", text)
            result = f"[prompt run: {name}]\n{text}"
            if remaining:
                result += f"\n\n[warn] Unfilled vars: {', '.join(remaining)}"
            return result
        return f"[prompt] Unknown command '{cmd}'. Use: save | load | list | delete | run"
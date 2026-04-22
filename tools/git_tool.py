"""
Cortex — Git Tool (Week 6)
Run common git operations from the agent.
"""
from __future__ import annotations
import subprocess, sys, os, shutil

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name: str = ""
        description: str = ""
        usage_example: str = ""
        def run(self, user_input: str) -> str:
            raise NotImplementedError

def _git(args: list[str], cwd: str | None = None) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git"] + args,
        capture_output=True, text=True,
        cwd=cwd or os.getcwd(),
        timeout=30,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

class GitTool(BaseTool):
    name = "git"
    description = (
        "Run git operations: status, log, diff, add, commit, push, pull, "
        "branch, checkout, clone, init."
    )
    usage_example = "git status"
    SAFE_CMDS = {
        "status", "log", "diff", "add", "commit",
        "push", "pull", "branch", "checkout", "clone",
        "init", "fetch", "stash", "show", "remote",
    }

    def run(self, user_input: str) -> str:
        user_input = user_input.strip()
        if not user_input:
            return "[git] Provide a git command, e.g.: git status"
        if user_input.lower().startswith("git "):
            user_input = user_input[4:].strip()
        parts = user_input.split()
        cmd = parts[0].lower()
        if cmd not in self.SAFE_CMDS:
            return (
                f"[git] '{cmd}' is not in the allowed command list.\n"
                f"Allowed: {', '.join(sorted(self.SAFE_CMDS))}"
            )
        code, out, err = _git(parts)
        lines = []
        if out:
            lines.append(out)
        if err:
            lines.append(err)
        if not lines:
            lines.append(f"[git {cmd}] Done (no output).")
        return "\n".join(lines)
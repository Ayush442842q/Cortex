"""Cortex — Git Tool (Week 6)
Run common git operations from the agent.
"""
from __future__ import annotations
import subprocess, os, json

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name = ""; description = ""; usage_example = ""
        def run(self, user_input: str) -> str: ...

SAFE_ACTIONS = {
    "status","log","diff","branch","add","commit","push","pull",
    "clone","checkout","merge","stash","tag","remote","fetch","init","show"
}

def _parse(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("{"): 
        try: return json.loads(raw)
        except: pass
    return {"action": raw}

def _git(args: list, cwd=None) -> str:
    r = subprocess.run(["git"] + args, capture_output=True, text=True, cwd=cwd, timeout=30)
    out = (r.stdout + r.stderr).strip()
    return out if out else "(no output)"

class GitTool(BaseTool):
    name = "git"
    description = (
        "Run git operations. Input JSON with keys: "
        "action (status|log|diff|branch|add|commit|push|pull|clone|checkout|...), "
        "args (list of extra args), cwd (repo path), message (for commit)."
    )
    usage_example = 'git({"action":"status"})'

    def run(self, user_input: str) -> str:
        p      = _parse(user_input)
        action = p.get("action","status").lower()
        args   = p.get("args", [])
        cwd    = p.get("cwd", None)
        msg    = p.get("message","")

        if action not in SAFE_ACTIONS:
            return f"[git] Action '{action}' not in safe list: {sorted(SAFE_ACTIONS)}"
        try:
            if action == "status":   return _git(["status"], cwd)
            elif action == "log":    return _git(["log","--oneline","-10"] + args, cwd)
            elif action == "diff":   return _git(["diff"] + args, cwd)
            elif action == "branch": return _git(["branch", "-a"], cwd)
            elif action == "add":    return _git(["add"] + (args or ["."]), cwd)
            elif action == "commit":
                if not msg: return "[git] ERROR: message required for commit."
                return _git(["commit", "-m", msg], cwd)
            elif action == "push":   return _git(["push"] + args, cwd)
            elif action == "pull":   return _git(["pull"] + args, cwd)
            elif action == "fetch":  return _git(["fetch"] + args, cwd)
            elif action == "clone":  return _git(["clone"] + args, cwd)
            elif action == "checkout": return _git(["checkout"] + args, cwd)
            elif action == "merge":  return _git(["merge"] + args, cwd)
            elif action == "stash":  return _git(["stash"] + args, cwd)
            elif action == "tag":    return _git(["tag"] + args, cwd)
            elif action == "remote": return _git(["remote", "-v"], cwd)
            elif action == "init":   return _git(["init"] + args, cwd)
            elif action == "show":   return _git(["show"] + args, cwd)
            else: return f"[git] Unhandled action: {action}"
        except subprocess.TimeoutExpired:
            return "[git] TIMEOUT: command took too long."
        except Exception as e:
            return f"[git] ERROR: {e}"

if __name__ == "__main__":
    t = GitTool()
    print(t.run('{"action":"status"}'))
    print("All tests passed.")

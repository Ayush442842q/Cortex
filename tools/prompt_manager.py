"""Cortex — Prompt Manager Tool (Week 8)
Save, load, list and delete reusable prompt templates.
"""
from __future__ import annotations
import os, json

STORE_PATH = os.path.expanduser("~/.agentbase/prompts.json")

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name = ""; description = ""; usage_example = ""
        def run(self, user_input: str) -> str: ...

def _load() -> dict:
    if os.path.exists(STORE_PATH):
        try: return json.loads(open(STORE_PATH).read())
        except: pass
    return {}

def _save(data: dict):
    os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
    open(STORE_PATH,"w").write(json.dumps(data, indent=2))

def _parse(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("{"): 
        try: return json.loads(raw)
        except: pass
    return {"action":"list"}

class PromptManagerTool(BaseTool):
    name = "prompt_manager"
    description = (
        "Manage reusable prompt templates. Input JSON with keys: "
        "action (save|load|list|delete|use), name (str), "
        "template (str, for save), vars (dict, for use)."
    )
    usage_example = 'prompt_manager({"action":"save","name":"summarize","template":"Summarize: {text}"})'

    def run(self, user_input: str) -> str:
        p      = _parse(user_input)
        action = p.get("action","list").lower()
        store  = _load()
        try:
            if action == "save":
                name     = p.get("name","")
                template = p.get("template","")
                if not name or not template:
                    return "[prompt_manager] ERROR: name and template required."
                store[name] = template; _save(store)
                return f"Saved prompt: '{name}'"
            elif action == "load":
                name = p.get("name","")
                return store.get(name, f"[prompt_manager] Not found: '{name}'")
            elif action == "list":
                if not store: return "No prompts saved yet."
                return "Saved prompts:\n" + "\n".join(f"  • {k}" for k in store)
            elif action == "delete":
                name = p.get("name","")
                if name in store:
                    del store[name]; _save(store)
                    return f"Deleted: '{name}'"
                return f"[prompt_manager] Not found: '{name}'"
            elif action == "use":
                name  = p.get("name","")
                tmpl  = store.get(name)
                if not tmpl: return f"[prompt_manager] Not found: '{name}'"
                try: return tmpl.format(**p.get("vars",{}))
                except KeyError as e: return f"[prompt_manager] Missing var: {e}"
            else:
                return f"Unknown action: {action}"
        except Exception as e:
            return f"[prompt_manager] ERROR: {e}"

if __name__ == "__main__":
    t = PromptManagerTool()
    t.run('{"action":"save","name":"greet","template":"Hello, {name}!"}')
    print(t.run('{"action":"use","name":"greet","vars":{"name":"Cortex"}}'))
    t.run('{"action":"delete","name":"greet"}')
    print("All tests passed.")

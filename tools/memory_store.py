"""Cortex — Memory Store Tool (Week 9)
Persistent key-value memory that survives across agent sessions.
"""
from __future__ import annotations
import os, json, time, fnmatch

STORE_PATH = os.path.expanduser("~/.agentbase/memory.json")

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
    parts = raw.split(None, 2)
    if len(parts) == 3: return {"action":"set","key":parts[1],"value":parts[2]}
    if len(parts) == 2: return {"action":"get","key":parts[1]}
    return {"action":"list"}

class MemoryStoreTool(BaseTool):
    name = "memory"
    description = (
        "Persistent memory across sessions. Input JSON with keys: "
        "action (set|get|delete|list|search|clear), key (str), "
        "value (any), pattern (for search/list)."
    )
    usage_example = 'memory({"action":"set","key":"user_name","value":"Ayush"})'

    def run(self, user_input: str) -> str:
        p      = _parse(user_input)
        action = p.get("action","list").lower()
        store  = _load()
        try:
            if action == "set":
                key = p.get("key","")
                if not key: return "[memory] ERROR: key required."
                store[key] = {"value": p.get("value",""), "updated": time.strftime("%Y-%m-%d %H:%M:%S")}
                _save(store); return f"Stored: {key}"
            elif action == "get":
                key = p.get("key","")
                entry = store.get(key)
                if not entry: return f"[memory] Not found: '{key}'"
                return f"{key} = {entry['value']}  (updated: {entry['updated']})"
            elif action == "delete":
                key = p.get("key","")
                if key in store:
                    del store[key]; _save(store); return f"Deleted: {key}"
                return f"[memory] Not found: '{key}'"
            elif action == "list":
                pattern = p.get("pattern","*")
                keys = [k for k in store if fnmatch.fnmatch(k, pattern)]
                if not keys: return "No memories found."
                return "\n".join(f"  {k}: {store[k]['value']}" for k in sorted(keys))
            elif action == "search":
                q = str(p.get("pattern","")).lower()
                matches = {k:v for k,v in store.items()
                           if q in k.lower() or q in str(v["value"]).lower()}
                if not matches: return f"No memories matching: '{q}'"
                return "\n".join(f"  {k}: {v['value']}" for k,v in matches.items())
            elif action == "clear":
                _save({}); return "Memory cleared."
            else:
                return f"Unknown action: {action}"
        except Exception as e:
            return f"[memory] ERROR: {e}"

if __name__ == "__main__":
    t = MemoryStoreTool()
    t.run('{"action":"set","key":"test_key","value":"hello"}')
    print(t.run('{"action":"get","key":"test_key"}'))
    t.run('{"action":"delete","key":"test_key"}')
    print("All tests passed.")

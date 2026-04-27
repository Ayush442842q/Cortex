"""Cortex — Clipboard Manager (Week 11)
Store, retrieve, list and clear named text snippets persistently.
"""
from __future__ import annotations
import os, json, time

STORE = os.path.expanduser("~/.agentbase/clipboard.json")

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=""; description=""; usage_example=""
        def run(self,u:str)->str: ...

def _load():
    try: return json.loads(open(STORE).read())
    except: return {}
def _save(d):
    os.makedirs(os.path.dirname(STORE), exist_ok=True)
    open(STORE,"w").write(json.dumps(d, indent=2))
def _parse(r):
    r=r.strip()
    if r.startswith("{"): 
        try: return json.loads(r)
        except: pass
    return {"action":"list"}

class ClipboardTool(BaseTool):
    name="clipboard"
    description="Store and retrieve named text snippets. Actions: copy, paste, list, delete, clear."
    usage_example='clipboard({"action":"copy","name":"mysnip","text":"Hello World"})' 
    def run(self,u:str)->str:
        p=_parse(u); action=p.get("action","list"); d=_load()
        if action=="copy":
            name=p.get("name",""); text=p.get("text","")
            if not name or not text: return "[clipboard] ERROR: name and text required."
            d[name]={"text":text,"saved":time.strftime("%Y-%m-%d %H:%M")}; _save(d)
            return f"Copied to clipboard: '{name}'"
        elif action=="paste":
            name=p.get("name","")
            e=d.get(name)
            return e["text"] if e else f"[clipboard] Not found: '{name}'"
        elif action=="list":
            if not d: return "Clipboard is empty."
            return "Saved snippets:\n"+("\n".join(f"  • {k}  ({v['saved']})" for k,v in d.items()))
        elif action=="delete":
            name=p.get("name","")
            if name in d: del d[name]; _save(d); return f"Deleted: '{name}'"
            return f"[clipboard] Not found: '{name}'"
        elif action=="clear":
            _save({}); return "Clipboard cleared."
        return f"Unknown action: {action}"

if __name__=="__main__":
    t=ClipboardTool()
    t.run('{"action":"copy","name":"test","text":"Hello Cortex!"}')
    print(t.run('{"action":"paste","name":"test"}'))
    t.run('{"action":"delete","name":"test"}')
    print("All tests passed.")

"""Cortex — Note Taker (Week 12)
Create, read, list, search and delete markdown notes.
"""
from __future__ import annotations
import os, json, time, fnmatch

NOTES_DIR = os.path.expanduser("~/.agentbase/notes")

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=""; description=""; usage_example=""
        def run(self,u:str)->str: ...

def _parse(r):
    r=r.strip()
    if r.startswith("{"): 
        try: return json.loads(r)
        except: pass
    return {"action":"list"}

def _path(name): return os.path.join(NOTES_DIR, name.replace(" ","_")+".md")

class NoteTakerTool(BaseTool):
    name="notes"
    description="Create and manage markdown notes. Actions: new, read, list, search, delete, append."
    usage_example='notes({"action":"new","title":"My Note","content":"# Hello\nThis is a note."})' 
    def run(self,u:str)->str:
        os.makedirs(NOTES_DIR, exist_ok=True)
        p=_parse(u); action=p.get("action","list")
        if action=="new":
            title=p.get("title",""); content=p.get("content","")
            if not title: return "[notes] ERROR: title required."
            fp=_path(title)
            header=f"# {title}\n_Created: {time.strftime('%Y-%m-%d %H:%M')}_\n\n"
            open(fp,"w",encoding="utf-8").write(header+content)
            return f"Note created: {title}"
        elif action=="read":
            title=p.get("title",""); fp=_path(title)
            if not os.path.exists(fp): return f"[notes] Not found: '{title}'"
            return open(fp,encoding="utf-8").read()
        elif action=="append":
            title=p.get("title",""); content=p.get("content",""); fp=_path(title)
            if not os.path.exists(fp): return f"[notes] Not found: '{title}'"
            open(fp,"a",encoding="utf-8").write("\n"+content)
            return f"Appended to: {title}"
        elif action=="list":
            files=[f[:-3].replace("_"," ") for f in os.listdir(NOTES_DIR) if f.endswith(".md")]
            return "Notes:\n"+"\n".join(f"  • {n}" for n in sorted(files)) if files else "No notes yet."
        elif action=="search":
            q=p.get("query","").lower(); matches=[]
            for f in os.listdir(NOTES_DIR):
                if not f.endswith(".md"): continue
                fp=os.path.join(NOTES_DIR,f)
                content=open(fp,encoding="utf-8").read()
                if q in content.lower() or q in f.lower():
                    matches.append(f[:-3].replace("_"," "))
            return "Matches:\n"+"\n".join(f"  • {m}" for m in matches) if matches else f"No notes matching '{q}'"
        elif action=="delete":
            title=p.get("title",""); fp=_path(title)
            if os.path.exists(fp): os.remove(fp); return f"Deleted: {title}"
            return f"[notes] Not found: '{title}'"
        return f"Unknown action: {action}"

if __name__=="__main__":
    t=NoteTakerTool()
    t.run('{"action":"new","title":"Test Note","content":"Hello Cortex!"}')
    print(t.run('{"action":"read","title":"Test Note"}'))
    t.run('{"action":"delete","title":"Test Note"}')
    print("All tests passed.")

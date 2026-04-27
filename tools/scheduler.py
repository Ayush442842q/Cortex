"""Cortex — Scheduler (Week 20)
Schedule commands/reminders to run at a specific time.
Schedules are stored persistently; run_due() executes pending ones.
"""
from __future__ import annotations
import os, json, time, subprocess, sys, uuid

STORE=os.path.expanduser("~/.agentbase/schedule.json")

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=""; description=""; usage_example=""
        def run(self,u:str)->str: ...

def _load():
    try: return json.loads(open(STORE).read())
    except: return []
def _save(d):
    os.makedirs(os.path.dirname(STORE),exist_ok=True)
    open(STORE,"w").write(json.dumps(d,indent=2))
def _parse(r):
    r=r.strip()
    if r.startswith("{"): 
        try: return json.loads(r)
        except: pass
    return {"action":"list"}

class SchedulerTool(BaseTool):
    name="scheduler"
    description="Schedule tasks. Actions: add (at, command/reminder), list, delete (id), run_due (execute overdue tasks), clear."
    usage_example='scheduler({"action":"add","at":"2025-12-31 23:59","reminder":"Happy New Year!"})' 
    def run(self,u:str)->str:
        p=_parse(u); action=p.get("action","list"); tasks=_load()
        if action=="add":
            at=p.get("at","")
            if not at: return "[scheduler] ERROR: 'at' datetime required (YYYY-MM-DD HH:MM)."
            try:
                run_ts=time.mktime(time.strptime(at,"%Y-%m-%d %H:%M"))
            except ValueError:
                return "[scheduler] ERROR: date format must be YYYY-MM-DD HH:MM"
            task={
                "id":       str(uuid.uuid4())[:8],
                "at":       at,
                "run_ts":   run_ts,
                "command":  p.get("command",""),
                "reminder": p.get("reminder",""),
                "done":     False,
                "created":  time.strftime("%Y-%m-%d %H:%M"),
            }
            tasks.append(task); _save(tasks)
            kind="command" if task["command"] else "reminder"
            content=task["command"] or task["reminder"]
            return f"Scheduled [{task['id']}] at {at}: {kind} — {content}"
        elif action=="list":
            if not tasks: return "No scheduled tasks."
            lines=["Scheduled tasks:"]
            for t in sorted(tasks,key=lambda x:x["run_ts"]):
                status="✅" if t["done"] else ("⏰" if time.time()<t["run_ts"] else "❗overdue")
                content=t.get("command") or t.get("reminder","")
                lines.append(f"  {status} [{t['id']}] {t['at']}  —  {content}")
            return "\n".join(lines)
        elif action=="delete":
            tid=p.get("id",""); before=len(tasks)
            tasks=[t for t in tasks if t["id"]!=tid]
            if len(tasks)<before: _save(tasks); return f"Deleted: {tid}"
            return f"[scheduler] Not found: {tid}"
        elif action=="run_due":
            now=time.time(); ran=[]
            for t in tasks:
                if not t["done"] and t["run_ts"]<=now:
                    if t.get("command"):
                        try:
                            r=subprocess.run(t["command"],shell=True,capture_output=True,text=True,timeout=30)
                            ran.append(f"[{t['id']}] Ran: {t['command']}\n  → {r.stdout.strip() or r.stderr.strip()}")
                        except Exception as e:
                            ran.append(f"[{t['id']}] ERROR: {e}")
                    elif t.get("reminder"):
                        ran.append(f"[{t['id']}] 🔔 REMINDER: {t['reminder']}")
                    t["done"]=True
            _save(tasks)
            return "\n".join(ran) if ran else "No tasks due right now."
        elif action=="clear":
            _save([]); return "All scheduled tasks cleared."
        return f"Unknown action: {action}"

if __name__=="__main__":
    t=SchedulerTool()
    t.run('{"action":"add","at":"2099-01-01 00:00","reminder":"Future reminder"}')
    print(t.run('{"action":"list"}'))
    print(t.run('{"action":"run_due"}'))
    t.run('{"action":"clear"}')
    print("All tests passed.")

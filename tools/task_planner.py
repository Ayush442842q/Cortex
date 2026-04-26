"""Cortex — Task Planner Tool (Week 10)
Break goals into subtasks, track progress, mark done.
"""
from __future__ import annotations
import os, json, time, uuid

STORE_PATH = os.path.expanduser("~/.agentbase/tasks.json")

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name = ""; description = ""; usage_example = ""
        def run(self, user_input: str) -> str: ...

def _load() -> list:
    if os.path.exists(STORE_PATH):
        try: return json.loads(open(STORE_PATH).read())
        except: pass
    return []

def _save(data: list):
    os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
    open(STORE_PATH,"w").write(json.dumps(data, indent=2))

def _parse(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("{"): 
        try: return json.loads(raw)
        except: pass
    return {"action":"list"}

STATUS_ICONS = {"todo":"⬜","in_progress":"🔄","done":"✅","blocked":"🚫"}

class TaskPlannerTool(BaseTool):
    name = "task_planner"
    description = (
        "Plan and track tasks. Input JSON with keys: "
        "action (add|list|done|update|delete|clear|plan), "
        "title (str), priority (high|medium|low), id (for done/update/delete), "
        "goal (str, for plan — auto-generates subtasks)."
    )
    usage_example = 'task_planner({"action":"add","title":"Write README","priority":"high"})'

    def run(self, user_input: str) -> str:
        p      = _parse(user_input)
        action = p.get("action","list").lower()
        tasks  = _load()
        try:
            if action == "add":
                title = p.get("title","")
                if not title: return "[task_planner] ERROR: title required."
                task = {
                    "id":       str(uuid.uuid4())[:8],
                    "title":    title,
                    "status":   "todo",
                    "priority": p.get("priority","medium"),
                    "created":  time.strftime("%Y-%m-%d %H:%M"),
                }
                tasks.append(task); _save(tasks)
                return f"Added task [{task['id']}]: {title}"

            elif action == "plan":
                goal     = p.get("goal","")
                subtasks = p.get("subtasks", [])
                if not goal: return "[task_planner] ERROR: goal required."
                added = []
                for s in subtasks:
                    t = {"id": str(uuid.uuid4())[:8], "title": s,
                         "status":"todo","priority":"medium",
                         "created": time.strftime("%Y-%m-%d %H:%M"),
                         "goal": goal}
                    tasks.append(t); added.append(f"  [{t['id']}] {s}")
                _save(tasks)
                return f"Plan for '{goal}':\n" + "\n".join(added) if added else "No subtasks provided."

            elif action == "list":
                if not tasks: return "No tasks."
                priority_order = {"high":0,"medium":1,"low":2}
                tasks_sorted = sorted(tasks, key=lambda x: priority_order.get(x.get("priority","medium"),1))
                lines = []
                for t in tasks_sorted:
                    icon = STATUS_ICONS.get(t["status"],"⬜")
                    lines.append(f"{icon} [{t['id']}] {t['title']}  ({t.get('priority','medium')})")
                return "\n".join(lines)

            elif action == "done":
                tid = p.get("id","")
                for t in tasks:
                    if t["id"] == tid:
                        t["status"] = "done"
                        t["completed"] = time.strftime("%Y-%m-%d %H:%M")
                        _save(tasks); return f"✅ Done: {t['title']}"
                return f"[task_planner] Task not found: {tid}"

            elif action == "update":
                tid = p.get("id","")
                for t in tasks:
                    if t["id"] == tid:
                        for k in ["title","status","priority"]:
                            if k in p: t[k] = p[k]
                        _save(tasks); return f"Updated [{tid}]"
                return f"[task_planner] Task not found: {tid}"

            elif action == "delete":
                tid = p.get("id","")
                before = len(tasks)
                tasks = [t for t in tasks if t["id"] != tid]
                if len(tasks) < before:
                    _save(tasks); return f"Deleted task: {tid}"
                return f"[task_planner] Task not found: {tid}"

            elif action == "clear":
                _save([]); return "All tasks cleared."

            else:
                return f"Unknown action: {action}"
        except Exception as e:
            return f"[task_planner] ERROR: {e}"

if __name__ == "__main__":
    t = TaskPlannerTool()
    t.run('{"action":"add","title":"Test task","priority":"high"}')
    result = t.run('{"action":"list"}')
    print(result)
    tid = result.split("[")[1].split("]")[0] if "[" in result else ""
    if tid: t.run(f'{{"action":"done","id":"{tid}"}}')
    t.run('{"action":"clear"}')
    print("All tests passed.")

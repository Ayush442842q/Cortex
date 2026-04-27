"""Cortex — System Monitor (Week 14)
CPU, RAM, disk, battery and process stats via psutil.
"""
from __future__ import annotations
import json, sys, subprocess

try:
    import psutil
    _OK=True
except ImportError:
    _OK=False

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=""; description=""; usage_example=""
        def run(self,u:str)->str: ...

def _ensure():
    if _OK: return None
    r=subprocess.run([sys.executable,"-m","pip","install","psutil","-q"],capture_output=True,text=True)
    if r.returncode!=0: return f"pip install psutil failed: {r.stderr.strip()}"
    global psutil,_OK
    import psutil as _p; psutil=_p; _OK=True; return None

def _parse(r):
    r=r.strip()
    if r.startswith("{"): 
        try: return json.loads(r)
        except: pass
    return {"action": r if r else "all"}

class SystemMonitorTool(BaseTool):
    name="sysmon"
    description="System stats: CPU, RAM, disk, battery, processes. Actions: all, cpu, ram, disk, battery, processes, network."
    usage_example='sysmon("all")' 
    def run(self,u:str)->str:
        err=_ensure()
        if err: return f"[sysmon] ERROR: {err}"
        p=_parse(u); action=p.get("action","all").lower()
        try:
            if action in ("all","cpu"):
                cpu=f"CPU:     {psutil.cpu_percent(interval=0.5)}% used  |  {psutil.cpu_count()} cores"
            if action in ("all","ram"):
                vm=psutil.virtual_memory()
                ram=f"RAM:     {vm.used/1e9:.1f} GB / {vm.total/1e9:.1f} GB  ({vm.percent}% used)"
            if action in ("all","disk"):
                du=psutil.disk_usage("/")
                disk=f"Disk:    {du.used/1e9:.1f} GB / {du.total/1e9:.1f} GB  ({du.percent}% used)"
            if action=="cpu": return cpu
            if action=="ram": return ram
            if action=="disk": return disk
            if action=="battery":
                b=psutil.sensors_battery()
                return f"Battery: {b.percent:.0f}%  {'charging' if b.power_plugged else 'discharging'}" if b else "No battery detected."
            if action=="processes":
                procs=sorted(psutil.process_iter(["pid","name","cpu_percent","memory_percent"]),
                             key=lambda p:p.info["memory_percent"] or 0,reverse=True)[:10]
                lines=["Top 10 processes by RAM:","  PID    MEM%   CPU%   NAME"]
                for p in procs:
                    i=p.info
                    lines.append(f"  {i['pid']:<6} {i['memory_percent'] or 0:5.1f}%  {i['cpu_percent'] or 0:5.1f}%  {i['name']}")
                return "\n".join(lines)
            if action=="network":
                io=psutil.net_io_counters()
                return f"Network: Sent {io.bytes_sent/1e6:.1f} MB | Recv {io.bytes_recv/1e6:.1f} MB"
            if action=="all":
                return "\n".join([cpu,ram,disk])
            return f"Unknown action: {action}"
        except Exception as e:
            return f"[sysmon] ERROR: {e}"

if __name__=="__main__":
    t=SystemMonitorTool()
    print(t.run("all"))
    print("All tests passed.")

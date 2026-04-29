"""Cortex — Process Manager Tool (Week 23) [System & OS]
List, search, kill and monitor running processes.
"""
from __future__ import annotations
import subprocess, sys, os, re
try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=description=usage_example=""
        def run(self,i): raise NotImplementedError

def _run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
    return r.stdout.strip(), r.stderr.strip()

class ProcessManagerTool(BaseTool):
    name="process"
    description="Manage processes. Commands: list | search <name> | kill <pid> | top | info <pid>"
    usage_example="process search python"

    def run(self, inp: str) -> str:
        inp=inp.strip()
        if not inp: return "[process] Commands: list | search <name> | kill <pid> | top | info <pid>"
        parts=inp.split(None,1); cmd=parts[0].lower(); arg=parts[1].strip() if len(parts)>1 else ""
        is_win=sys.platform=="win32"
        if cmd=="list":
            if is_win:
                out,_=_run(["tasklist","/FO","CSV","/NH"])
                lines=out.strip().splitlines()[:20]
                return "[Processes (top 20)]\n"+chr(10).join(lines)
            else:
                out,_=_run(["ps","aux","--sort=-%cpu"])
                return "[Processes]\n"+chr(10).join(out.splitlines()[:21])
        elif cmd=="search":
            if not arg: return "[process] search needs a name"
            if is_win:
                out,_=_run(["tasklist","/FI",f"IMAGENAME eq {arg}*","/FO","CSV"])
            else:
                out,_=_run(["pgrep","-l","-f",arg])
            return f"[process search: {arg}]\n{out or 'No match found'}"
        elif cmd=="kill":
            if not arg: return "[process] kill needs a PID"
            try:
                pid=int(arg)
                if is_win: out,err=_run(["taskkill","/PID",str(pid),"/F"])
                else: out,err=_run(["kill",str(pid)])
                return f"[process] Killed PID {pid}. {out or err}"
            except ValueError: return "[process] kill needs a numeric PID"
            except Exception as e: return f"[process] kill failed: {e}"
        elif cmd=="top":
            if is_win:
                out,_=_run(["tasklist","/FO","CSV","/NH"])
                return "[Top Processes]\n"+chr(10).join(out.splitlines()[:10])
            else:
                out,_=_run(["ps","aux","--sort=-%mem"])
                return "[Top by Memory]\n"+chr(10).join(out.splitlines()[:11])
        elif cmd=="info":
            if not arg: return "[process] info needs a PID"
            if is_win:
                out,_=_run(["tasklist","/FI",f"PID eq {arg}","/FO","LIST"])
            else:
                out,_=_run(["ps","-p",arg,"-o","pid,ppid,cmd,%cpu,%mem,etime"])
            return f"[process info: {arg}]\n{out or 'PID not found'}"
        return f"[process] Unknown command: {cmd}"

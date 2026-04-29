"""Cortex — Disk Analyzer Tool (Week 28) [System & OS]
Analyze disk space usage by folder/file.
"""
from __future__ import annotations
import os, sys
from pathlib import Path
try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=description=usage_example=""
        def run(self,i): raise NotImplementedError

def _human(n):
    for u in ["B","KB","MB","GB","TB"]:
        if n<1024: return f"{n:.1f} {u}"
        n/=1024
    return f"{n:.1f} PB"

def _dir_size(path):
    total=0
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_file(follow_symlinks=False): total+=entry.stat().st_size
                elif entry.is_dir(follow_symlinks=False): total+=_dir_size(entry.path)
            except: pass
    except: pass
    return total

class DiskAnalyzerTool(BaseTool):
    name="disk"
    description="Analyze disk usage. Commands: usage <path> | top <path> [n] | drives | find-large <path> [mb]"
    usage_example="disk top . 10"

    def run(self, inp: str) -> str:
        inp=inp.strip()
        if not inp: return "[disk] Commands: usage | top | drives | find-large"
        parts=inp.split(); cmd=parts[0].lower()
        path=parts[1] if len(parts)>1 else "."
        if cmd=="drives":
            if sys.platform=="win32":
                import subprocess
                out=subprocess.run(["wmic","logicaldisk","get","size,freespace,caption"],
                    capture_output=True,text=True).stdout
                return f"[disk drives]\n{out.strip()}"
            else:
                import subprocess
                out=subprocess.run(["df","-h"],capture_output=True,text=True).stdout
                return f"[disk drives]\n{out.strip()}"
        if not os.path.exists(path): return f"[disk] Path not found: {path}"
        if cmd=="usage":
            size=_dir_size(path)
            p=Path(path).resolve()
            return f"[disk usage: {p}]\n  Total: {_human(size)}"
        elif cmd=="top":
            n=int(parts[2]) if len(parts)>2 else 10
            try:
                entries=[]
                for entry in os.scandir(path):
                    try:
                        size=entry.stat().st_size if entry.is_file(follow_symlinks=False) else _dir_size(entry.path)
                        entries.append((size,entry.name))
                    except: pass
                entries.sort(reverse=True)
                lines=[f"[disk top {n}: {path}]"]
                for size,name in entries[:n]:
                    lines.append(f"  {_human(size):>10}  {name}")
                return chr(10).join(lines)
            except Exception as e: return f"[disk] Error: {e}"
        elif cmd=="find-large":
            mb=float(parts[2]) if len(parts)>2 else 100
            threshold=mb*1024*1024
            found=[]
            for root,dirs,files in os.walk(path):
                for f in files:
                    fp=os.path.join(root,f)
                    try:
                        s=os.path.getsize(fp)
                        if s>=threshold: found.append((s,fp))
                    except: pass
            found.sort(reverse=True)
            if not found: return f"[disk] No files larger than {mb}MB in {path}"
            lines=[f"[find-large >{mb}MB in {path}: {len(found)} files]"]
            for size,fp in found[:20]: lines.append(f"  {_human(size):>10}  {fp}")
            return chr(10).join(lines)
        return f"[disk] Unknown command: {cmd}"

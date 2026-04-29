"""Cortex — CSV Analyzer Tool (Week 24) [Data & File]
Load, inspect, filter, sort and summarize CSV files.
"""
from __future__ import annotations
import csv, io, os, json
from pathlib import Path
try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=description=usage_example=""
        def run(self,i): raise NotImplementedError

def _load(path):
    with open(path,encoding="utf-8",errors="replace") as f:
        rows=list(csv.DictReader(f))
    return rows

class CsvAnalyzerTool(BaseTool):
    name="csv"
    description="Analyze CSV files. Commands: info <file> | head <file> [n] | col <file> <column> | filter <file> <col>=<val> | stats <file> <col>"
    usage_example="csv info data.csv"

    def run(self, inp: str) -> str:
        inp=inp.strip()
        if not inp: return "[csv] Commands: info | head | col | filter | stats"
        parts=inp.split(); cmd=parts[0].lower()
        if len(parts)<2: return f"[csv] {cmd} needs a file path"
        path=parts[1]
        if not os.path.exists(path): return f"[csv] File not found: {path}"
        try: rows=_load(path)
        except Exception as e: return f"[csv] Load error: {e}"
        if not rows: return "[csv] File is empty or has no rows"
        cols=list(rows[0].keys())
        if cmd=="info":
            return (f"[csv info: {path}]\n"
                    f"  Rows   : {len(rows)}\n"
                    f"  Cols   : {len(cols)}\n"
                    f"  Fields : {', '.join(cols)}")
        elif cmd=="head":
            n=int(parts[2]) if len(parts)>2 else 5
            lines=[",".join(cols)]
            for r in rows[:n]: lines.append(",".join(str(r.get(c,"")) for c in cols))
            return f"[csv head: {path}]\n"+chr(10).join(lines)
        elif cmd=="col":
            if len(parts)<3: return "[csv] col needs a column name"
            col=parts[2]
            if col not in cols: return f"[csv] Column '{col}' not found. Available: {', '.join(cols)}"
            vals=[r[col] for r in rows[:20]]
            return f"[csv col: {col}]\n"+chr(10).join(vals)
        elif cmd=="filter":
            if len(parts)<3: return "[csv] filter needs col=val"
            expr=parts[2]
            if "=" not in expr: return "[csv] filter: use col=value"
            k,v=expr.split("=",1)
            matched=[r for r in rows if r.get(k,"").lower()==v.lower()]
            if not matched: return f"[csv] No rows where {k}={v}"
            lines=[",".join(cols)]+[",".join(str(r.get(c,"")) for c in cols) for r in matched[:10]]
            return f"[csv filter {k}={v}: {len(matched)} rows]\n"+chr(10).join(lines)
        elif cmd=="stats":
            if len(parts)<3: return "[csv] stats needs a column name"
            col=parts[2]
            if col not in cols: return f"[csv] Column '{col}' not found"
            vals=[]
            for r in rows:
                try: vals.append(float(r[col]))
                except: pass
            if not vals: return f"[csv] Column '{col}' has no numeric values"
            return (f"[csv stats: {col}]\n"
                    f"  Count : {len(vals)}\n"
                    f"  Min   : {min(vals):.4g}\n"
                    f"  Max   : {max(vals):.4g}\n"
                    f"  Mean  : {sum(vals)/len(vals):.4g}\n"
                    f"  Sum   : {sum(vals):.4g}")
        return f"[csv] Unknown command: {cmd}"

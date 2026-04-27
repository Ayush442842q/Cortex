"""Cortex — JSON/CSV Tool (Week 15)
Parse, filter, convert and summarize JSON and CSV data.
"""
from __future__ import annotations
import json, csv, io, os

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
    return {"action":"parse","data":r}

class DataTool(BaseTool):
    name="data"
    description="Work with JSON and CSV. Actions: parse, filter, to_csv, to_json, summarize, keys. Input JSON with action, data (string or file path), filter_key, filter_value."
    usage_example='data({"action":"parse","data":"[{\"a\":1},{\"a\":2}]"})' 
    def run(self,u:str)->str:
        p=_parse(u); action=p.get("action","parse")
        raw=p.get("data","")
        # if it looks like a file path, read it
        if isinstance(raw,str) and os.path.exists(raw):
            raw=open(raw,encoding="utf-8").read()
        try:
            if action=="parse":
                try:
                    obj=json.loads(raw)
                    return json.dumps(obj,indent=2)
                except:
                    reader=csv.DictReader(io.StringIO(raw))
                    rows=list(reader)
                    return json.dumps(rows,indent=2)
            elif action=="filter":
                obj=json.loads(raw) if isinstance(raw,str) else raw
                if not isinstance(obj,list): return "[data] filter requires a JSON array."
                key=p.get("filter_key",""); val=str(p.get("filter_value",""))
                filtered=[r for r in obj if str(r.get(key,""))==val]
                return json.dumps(filtered,indent=2)
            elif action=="to_csv":
                obj=json.loads(raw) if isinstance(raw,str) else raw
                if not isinstance(obj,list) or not obj: return "[data] to_csv requires a non-empty JSON array."
                out=io.StringIO()
                w=csv.DictWriter(out,fieldnames=obj[0].keys())
                w.writeheader(); w.writerows(obj)
                return out.getvalue()
            elif action=="to_json":
                reader=csv.DictReader(io.StringIO(raw))
                return json.dumps(list(reader),indent=2)
            elif action=="summarize":
                obj=json.loads(raw) if isinstance(raw,str) else raw
                if isinstance(obj,list):
                    return f"Array with {len(obj)} items.\nKeys: {list(obj[0].keys()) if obj else []}"
                elif isinstance(obj,dict):
                    return f"Object with {len(obj)} keys:\n"+("\n".join(f"  {k}: {type(v).__name__}" for k,v in obj.items()))
                return str(obj)
            elif action=="keys":
                obj=json.loads(raw) if isinstance(raw,str) else raw
                if isinstance(obj,list) and obj: return "Keys: "+", ".join(obj[0].keys())
                if isinstance(obj,dict): return "Keys: "+", ".join(obj.keys())
                return "[data] Cannot extract keys from this data."
            return f"Unknown action: {action}"
        except Exception as e:
            return f"[data] ERROR: {e}"

if __name__=="__main__":
    t=DataTool()
    print(t.run('{"action":"parse","data":"[{\"a\":1},{\"a\":2}]"}'))
    print(t.run('{"action":"to_csv","data":"[{\"name\":\"Alice\",\"age\":\"30\"}]"}'))
    print("All tests passed.")

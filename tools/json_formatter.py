"""Cortex — JSON Formatter Tool (Week 29) [Data & File]
Pretty-print, minify, validate, query and diff JSON.
"""
from __future__ import annotations
import json, sys, os, re
try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=description=usage_example=""
        def run(self,i): raise NotImplementedError

def _load(src):
    if os.path.exists(src): return json.loads(open(src,encoding="utf-8").read())
    return json.loads(src)

class JsonFormatterTool(BaseTool):
    name="json"
    description="Work with JSON. Commands: format <json|file> | minify <json|file> | validate <json|file> | get <json|file> <key.path> | keys <json|file>"
    usage_example='json format {"name":"Ayush","age":20}'

    def run(self, inp: str) -> str:
        inp=inp.strip()
        if not inp: return "[json] Commands: format | minify | validate | get | keys"
        parts=inp.split(None,1); cmd=parts[0].lower(); rest=parts[1].strip() if len(parts)>1 else ""
        if cmd not in ("format","minify","validate","get","keys"):
            rest=inp; cmd="format"
        if cmd=="get":
            sub=rest.split(None,1)
            if len(sub)<2: return "[json] get needs: get <json|file> <key.path>"
            src,keypath=sub[0],sub[1]
        else: src=rest; keypath=""
        try: data=_load(src)
        except Exception as e: return f"[json] Parse error: {e}"
        if cmd=="format":
            return json.dumps(data,indent=2,ensure_ascii=False)
        elif cmd=="minify":
            return json.dumps(data,separators=(",",":"),ensure_ascii=False)
        elif cmd=="validate":
            return f"[json] Valid JSON. Type: {type(data).__name__}, {'len: '+str(len(data)) if hasattr(data,'__len__') else ''}"
        elif cmd=="keys":
            if isinstance(data,dict): return "[json keys]\n"+chr(10).join(f"  {k}" for k in data)
            elif isinstance(data,list): return f"[json] Array with {len(data)} items"
            return f"[json] Scalar: {data}"
        elif cmd=="get":
            obj=data
            for key in keypath.split("."):
                try:
                    if isinstance(obj,list): obj=obj[int(key)]
                    else: obj=obj[key]
                except (KeyError,IndexError,TypeError,ValueError) as e:
                    return f"[json] Key error at '{key}': {e}"
            return json.dumps(obj,indent=2,ensure_ascii=False) if isinstance(obj,(dict,list)) else str(obj)
        return f"[json] Unknown command: {cmd}"

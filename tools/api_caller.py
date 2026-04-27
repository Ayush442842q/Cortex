"""Cortex — API Caller (Week 19)
Make HTTP GET/POST/PUT/DELETE requests to any REST API.
"""
from __future__ import annotations
import json, urllib.request, urllib.error, urllib.parse

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
    return {"method":"GET","url":r}

class APICallerTool(BaseTool):
    name="api"
    description="Make HTTP requests. Input JSON with: url, method (GET|POST|PUT|DELETE), headers (dict), body (dict or string), timeout (default 15)."
    usage_example='api({"method":"GET","url":"https://api.github.com/users/octocat"})' 
    def run(self,u:str)->str:
        p=_parse(u)
        url=p.get("url","").strip()
        method=p.get("method","GET").upper()
        headers=p.get("headers",{})
        body=p.get("body",None)
        timeout=int(p.get("timeout",15))
        if not url: return "[api] ERROR: url required."
        if not url.startswith("http"): return "[api] ERROR: url must start with http/https."
        try:
            data=None
            if body is not None:
                if isinstance(body,dict):
                    data=json.dumps(body).encode()
                    headers.setdefault("Content-Type","application/json")
                elif isinstance(body,str):
                    data=body.encode()
            headers.setdefault("User-Agent","Cortex-Agent/1.0")
            req=urllib.request.Request(url,data=data,headers=headers,method=method)
            with urllib.request.urlopen(req,timeout=timeout) as resp:
                status=resp.status
                raw=resp.read().decode(errors="replace")
                try:
                    parsed=json.loads(raw)
                    body_out=json.dumps(parsed,indent=2)
                except:
                    body_out=raw[:2000]+("..." if len(raw)>2000 else "")
            return f"Status: {status}\n\n{body_out}"
        except urllib.error.HTTPError as e:
            return f"HTTP {e.code}: {e.reason}"
        except urllib.error.URLError as e:
            return f"[api] ERROR: {e.reason}"
        except Exception as e:
            return f"[api] ERROR: {e}"

if __name__=="__main__":
    t=APICallerTool()
    print(t.run('{"method":"GET","url":"https://api.github.com/users/octocat"}'))
    print("All tests passed.")

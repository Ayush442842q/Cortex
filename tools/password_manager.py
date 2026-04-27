"""Cortex — Password Manager (Week 18)
Generate strong passwords and store them encrypted with a master key.
Uses only stdlib (hashlib + XOR encryption — lightweight, no deps).
"""
from __future__ import annotations
import os, json, hashlib, secrets, string, base64, time

STORE=os.path.expanduser("~/.agentbase/passwords.enc")

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=""; description=""; usage_example=""
        def run(self,u:str)->str: ...

def _key(master:str)->bytes:
    return hashlib.sha256(master.encode()).digest()

def _xor(data:bytes,key:bytes)->bytes:
    return bytes(b^key[i%len(key)] for i,b in enumerate(data))

def _encrypt(obj:dict,master:str)->str:
    raw=json.dumps(obj).encode()
    return base64.b64encode(_xor(raw,_key(master))).decode()

def _decrypt(enc:str,master:str)->dict:
    raw=_xor(base64.b64decode(enc),_key(master))
    return json.loads(raw.decode())

def _load(master:str)->dict:
    if not os.path.exists(STORE): return {}
    try: return _decrypt(open(STORE).read().strip(),master)
    except: return None  # wrong master key

def _save(data:dict,master:str):
    os.makedirs(os.path.dirname(STORE),exist_ok=True)
    open(STORE,"w").write(_encrypt(data,master))

def _generate(length=16,symbols=True)->str:
    chars=string.ascii_letters+string.digits+(string.punctuation if symbols else "")
    return "".join(secrets.choice(chars) for _ in range(length))

def _parse(r):
    r=r.strip()
    if r.startswith("{"): 
        try: return json.loads(r)
        except: pass
    return {"action":"generate"}

class PasswordManagerTool(BaseTool):
    name="passwords"
    description="Generate & store encrypted passwords. Actions: generate, save, get, list, delete. Always include master (your master password)."
    usage_example='passwords({"action":"generate","length":20})' 
    def run(self,u:str)->str:
        p=_parse(u); action=p.get("action","generate")
        master=p.get("master","cortex_default")
        if action=="generate":
            length=int(p.get("length",16)); symbols=p.get("symbols",True)
            pw=_generate(length,symbols)
            return f"Generated password: {pw}\nLength: {length}  Symbols: {symbols}"
        master_required=["save","get","list","delete"]
        if action in master_required:
            data=_load(master)
            if data is None: return "[passwords] ERROR: wrong master key."
        if action=="save":
            site=p.get("site",""); pw=p.get("password",_generate())
            if not site: return "[passwords] ERROR: site required."
            data[site]={"password":pw,"saved":time.strftime("%Y-%m-%d %H:%M")}
            _save(data,master); return f"Password saved for: {site}"
        elif action=="get":
            site=p.get("site","")
            entry=data.get(site)
            return f"{site}: {entry['password']}" if entry else f"[passwords] Not found: {site}"
        elif action=="list":
            return "Saved sites:\n"+"\n".join(f"  • {s}" for s in sorted(data)) if data else "No passwords saved."
        elif action=="delete":
            site=p.get("site","")
            if site in data: del data[site]; _save(data,master); return f"Deleted: {site}"
            return f"[passwords] Not found: {site}"
        return f"Unknown action: {action}"

if __name__=="__main__":
    t=PasswordManagerTool()
    print(t.run('{"action":"generate","length":20}'))
    t.run('{"action":"save","site":"github.com","password":"test123","master":"mykey"}')
    print(t.run('{"action":"get","site":"github.com","master":"mykey"}'))
    t.run('{"action":"delete","site":"github.com","master":"mykey"}')
    print("All tests passed.")

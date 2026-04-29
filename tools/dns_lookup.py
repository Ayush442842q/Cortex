"""Cortex — DNS Lookup Tool (Week 21) [Web & Network]
Resolve hostnames, reverse lookup IPs, query MX/NS/TXT records.
"""
from __future__ import annotations
import socket, subprocess, sys
try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=description=usage_example=""
        def run(self,i): raise NotImplementedError

class DnsLookupTool(BaseTool):
    name="dns"
    description="DNS lookups. Commands: resolve <host> | reverse <ip> | mx <domain> | ns <domain>"
    usage_example="dns resolve google.com"

    def run(self, inp: str) -> str:
        inp=inp.strip()
        if not inp: return "[dns] Commands: resolve | reverse | mx | ns"
        parts=inp.split(None,1); cmd=parts[0].lower(); arg=parts[1].strip() if len(parts)>1 else ""
        if cmd=="resolve":
            if not arg: return "[dns] resolve needs a hostname"
            try:
                results=socket.getaddrinfo(arg,None)
                ips=sorted({r[4][0] for r in results})
                return f"[dns] {arg}\n"+chr(10).join(f"  {ip}" for ip in ips)
            except Exception as e: return f"[dns] resolve failed: {e}"
        elif cmd=="reverse":
            if not arg: return "[dns] reverse needs an IP"
            try: return f"[dns] {arg} -> {socket.gethostbyaddr(arg)[0]}"
            except Exception as e: return f"[dns] reverse failed: {e}"
        elif cmd in ("mx","ns","txt"):
            if not arg: return f"[dns] {cmd} needs a domain"
            try:
                import subprocess
                r=subprocess.run(["nslookup",f"-type={cmd}",arg],capture_output=True,text=True,timeout=10)
                return f"[dns {cmd}] {arg}\n{(r.stdout or r.stderr)[:800]}"
            except Exception as e: return f"[dns] {cmd} query failed: {e}"
        else: return f"[dns] Unknown command: {cmd}"

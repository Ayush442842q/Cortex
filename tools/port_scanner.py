"""Cortex — Port Scanner Tool (Week 26) [Web & Network]
Scan open TCP ports on a host.
"""
from __future__ import annotations
import socket, concurrent.futures, sys
try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=description=usage_example=""
        def run(self,i): raise NotImplementedError

COMMON_PORTS={20:"FTP-data",21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",
    80:"HTTP",110:"POP3",143:"IMAP",443:"HTTPS",3306:"MySQL",5432:"PostgreSQL",
    6379:"Redis",8080:"HTTP-alt",8443:"HTTPS-alt",27017:"MongoDB"}

def _scan(host,port,timeout=0.5):
    try:
        with socket.create_connection((host,port),timeout=timeout): return True
    except: return False

class PortScannerTool(BaseTool):
    name="portscan"
    description="Scan TCP ports. Commands: scan <host> | scan <host> <port> | common <host>"
    usage_example="portscan common google.com"

    def run(self, inp: str) -> str:
        inp=inp.strip()
        if not inp: return "[portscan] Commands: scan <host> | scan <host> <port> | common <host>"
        parts=inp.split(); cmd=parts[0].lower()
        if cmd not in ("scan","common"): parts=["scan"]+parts; cmd="scan"
        host=parts[1] if len(parts)>1 else ""
        if not host: return "[portscan] Need a host"
        if cmd=="common":
            open_ports=[]
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
                futures={ex.submit(_scan,host,p):p for p in COMMON_PORTS}
                for f,p in futures.items():
                    if f.result(): open_ports.append(p)
            if not open_ports: return f"[portscan] {host}: no common ports open"
            lines=[f"[portscan] {host} — open ports:"]
            for p in sorted(open_ports): lines.append(f"  {p:5d}  {COMMON_PORTS.get(p,'unknown')}")
            return chr(10).join(lines)
        elif cmd=="scan":
            if len(parts)>2:
                port=int(parts[2])
                status="OPEN" if _scan(host,port) else "CLOSED"
                return f"[portscan] {host}:{port} is {status}"
            # scan 1-1024
            open_ports=[]
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as ex:
                futures={ex.submit(_scan,host,p):p for p in range(1,1025)}
                for f,p in futures.items():
                    if f.result(): open_ports.append(p)
            lines=[f"[portscan] {host} (1-1024) — {len(open_ports)} open:"]
            for p in sorted(open_ports): lines.append(f"  {p}  {COMMON_PORTS.get(p,'')}")
            return chr(10).join(lines) if open_ports else f"[portscan] {host}: no open ports in 1-1024"
        return "[portscan] Unknown command"

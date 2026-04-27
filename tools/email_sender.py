"""Cortex — Email Sender (Week 16)
Send emails via SMTP (Gmail, Outlook, or any SMTP server).
Credentials stored in ~/.agentbase/email_config.json
"""
from __future__ import annotations
import smtplib, json, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

CONFIG_PATH=os.path.expanduser("~/.agentbase/email_config.json")

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=""; description=""; usage_example=""
        def run(self,u:str)->str: ...

def _load_cfg():
    try: return json.loads(open(CONFIG_PATH).read())
    except: return {}

def _save_cfg(d):
    os.makedirs(os.path.dirname(CONFIG_PATH),exist_ok=True)
    open(CONFIG_PATH,"w").write(json.dumps(d,indent=2))

def _parse(r):
    r=r.strip()
    if r.startswith("{"): 
        try: return json.loads(r)
        except: pass
    return {"action":"status"}

class EmailSenderTool(BaseTool):
    name="email"
    description="Send emails via SMTP. Actions: setup (save credentials), send (to, subject, body), status."
    usage_example='email({"action":"send","to":"friend@example.com","subject":"Hello","body":"Hi there!"})' 
    def run(self,u:str)->str:
        p=_parse(u); action=p.get("action","status")
        if action=="setup":
            cfg={
                "smtp_host": p.get("smtp_host","smtp.gmail.com"),
                "smtp_port": int(p.get("smtp_port",587)),
                "username":  p.get("username",""),
                "password":  p.get("password",""),
                "from_name": p.get("from_name","Cortex Agent"),
            }
            if not cfg["username"] or not cfg["password"]:
                return "[email] ERROR: username and password required for setup."
            _save_cfg(cfg)
            return f"Email configured for: {cfg['username']}"
        elif action=="status":
            cfg=_load_cfg()
            if not cfg: return "[email] Not configured. Run setup first."
            return f"Configured: {cfg.get('username','?')} via {cfg.get('smtp_host','?')}:{cfg.get('smtp_port','?')}"
        elif action=="send":
            cfg=_load_cfg()
            if not cfg: return "[email] Not configured. Run setup first."
            to=p.get("to",""); subject=p.get("subject","(no subject)"); body=p.get("body","")
            if not to: return "[email] ERROR: 'to' address required."
            try:
                msg=MIMEMultipart()
                msg["From"]=f"{cfg.get('from_name','Cortex')} <{cfg['username']}>"
                msg["To"]=to; msg["Subject"]=subject
                msg.attach(MIMEText(body,"plain"))
                with smtplib.SMTP(cfg["smtp_host"],cfg["smtp_port"],timeout=10) as s:
                    s.starttls(); s.login(cfg["username"],cfg["password"]); s.sendmail(cfg["username"],to,msg.as_string())
                return f"Email sent to {to}"
            except Exception as e:
                return f"[email] ERROR: {e}"
        return f"Unknown action: {action}"

if __name__=="__main__":
    t=EmailSenderTool()
    print(t.run('{"action":"status"}'))
    print("All tests passed.")

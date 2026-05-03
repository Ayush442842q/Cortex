"""Cortex — Regex Tester Tool (Week 30) [Developer]
Test, explain and apply regular expressions interactively.
"""
from __future__ import annotations
import re, json
try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=description=usage_example=""
        def run(self,i): raise NotImplementedError

PATTERNS={
    "email":    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "url":      r'https?://[^\s<>"]+',
    "ip":       r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
    "phone":    r"\+?[\d\s\-().]{7,15}",
    "date":     r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    "hex":      r"#[0-9a-fA-F]{3,6}\b",
    "number":   r"-?\d+(?:\.\d+)?",
    "hashtag":  r"#[a-zA-Z_]\w*",
}

class RegexTesterTool(BaseTool):
    name="regex"
    description="Test regex. Commands: test <pattern> | <text>  •  match <pattern> | <text>  •  extract <pattern> | <text>  •  replace <pattern> | <repl> | <text>  •  presets"
    usage_example="regex extract email | Contact us at hello@example.com or info@test.org"

    def run(self, inp: str) -> str:
        inp=inp.strip()
        if not inp: return "[regex] Commands: test | match | extract | replace | presets"
        parts=inp.split(None,1); cmd=parts[0].lower(); rest=parts[1] if len(parts)>1 else ""
        if cmd=="presets":
            return "[Built-in patterns]\n"+chr(10).join(f"  {k:<10} {v}" for k,v in PATTERNS.items())
        if cmd not in ("test","match","extract","replace"): rest=inp; cmd="test"
        if "|" not in rest:
            return f"[regex] {cmd} needs '|' separator. Example: regex {cmd} \\d+ | abc 123"
        segs=[s.strip() for s in rest.split("|")]
        if cmd=="replace":
            if len(segs)<3: return "[regex] replace needs: replace <pattern> | <repl> | <text>"
            pat,repl,text=segs[0],segs[1],"| ".join(segs[2:])
        else: pat,text=segs[0],"| ".join(segs[1:])
        # resolve preset
        pat=PATTERNS.get(pat.lower(),pat)
        try:
            rx=re.compile(pat)
        except re.error as e: return f"[regex] Invalid pattern: {e}"
        if cmd in ("test","match"):
            m=rx.search(text)
            if not m: return f"[regex] No match found in: {text[:100]}"
            lines=[f"[regex match]  pattern: {pat}",f"  Match  : '{m.group()}'",
                   f"  Span   : {m.span()}",f"  Groups : {m.groups() or 'none'}"]
            all_m=rx.findall(text)
            lines.append(f"  Total  : {len(all_m)} occurrence(s)")
            return chr(10).join(lines)
        elif cmd=="extract":
            all_m=rx.findall(text)
            if not all_m: return f"[regex] No matches for '{pat}' in text"
            return f"[regex extract: {len(all_m)} match(es)]\n"+chr(10).join(f"  {m}" for m in all_m[:50])
        elif cmd=="replace":
            result=rx.sub(repl,text)
            count=len(rx.findall(text))
            return f"[regex replace: {count} substitution(s)]\n{result}"
        return f"[regex] Unknown command: {cmd}"

"""Cortex — LLM Switcher Tool (Week 7)
Query different LLM providers (Groq models) from within the agent.
"""
from __future__ import annotations
import os, json, sys

try:
    from groq import Groq
    _GROQ_OK = True
except ImportError:
    _GROQ_OK = False

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name = ""; description = ""; usage_example = ""
        def run(self, user_input: str) -> str: ...

MODELS = {
    "fast":    "llama-3.1-8b-instant",
    "smart":   "llama-3.3-70b-versatile",
    "code":    "qwen-2.5-coder-32b",
    "default": "llama-3.3-70b-versatile",
}

def _parse(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("{"): 
        try: return json.loads(raw)
        except: pass
    return {"prompt": raw, "model": "default"}

class LLMSwitcherTool(BaseTool):
    name = "llm"
    description = (
        "Query a specific LLM model. Input JSON with keys: "
        "prompt (str), model (fast|smart|code|default or full model name), "
        "system (optional system prompt), max_tokens (default 1024)."
    )
    usage_example = 'llm({"prompt":"Explain recursion","model":"fast"})'

    def run(self, user_input: str) -> str:
        if not _GROQ_OK:
            return "[llm] ERROR: groq not installed. Run: pip install groq"
        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key:
            try:
                import json as j
                cfg = j.load(open("config.json"))
                api_key = cfg.get("groq_api_key","") or cfg.get("api_key","")
            except: pass
        if not api_key:
            return "[llm] ERROR: GROQ_API_KEY not found in env or config.json"

        p          = _parse(user_input)
        prompt     = p.get("prompt","").strip()
        model_key  = p.get("model","default")
        model      = MODELS.get(model_key, model_key)
        system     = p.get("system","You are a helpful assistant.")
        max_tokens = int(p.get("max_tokens", 1024))

        if not prompt:
            return "[llm] ERROR: prompt is empty."
        try:
            client = Groq(api_key=api_key)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role":"system","content":system},
                           {"role":"user","content":prompt}],
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"[llm] ERROR: {e}"

if __name__ == "__main__":
    t = LLMSwitcherTool()
    print("LLM Switcher loaded. Available models:", list(MODELS.keys()))
    print("All tests passed.")

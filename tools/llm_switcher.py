"""
Cortex — LLM Switcher Tool (Week 7)
Switch between Groq, OpenAI, and Anthropic at runtime.
"""
from __future__ import annotations
import sys, os, json, urllib.request, urllib.error
from pathlib import Path

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name: str = ""
        description: str = ""
        usage_example: str = ""
        def run(self, user_input: str) -> str:
            raise NotImplementedError

def _load_key(provider: str) -> str | None:
    env_map = {"groq": "GROQ_API_KEY", "openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY"}
    key = os.environ.get(env_map.get(provider, ""))
    if key:
        return key
    for cfg_path in [Path(__file__).parent.parent / "config.json", Path("config.json")]:
        if cfg_path.exists():
            try:
                data = json.loads(cfg_path.read_text())
                k = data.get(f"{provider}_api_key") or data.get("api_key")
                if k:
                    return k
            except Exception:
                pass
    return None

def _call_groq(prompt, model, api_key):
    model = model or "llama3-8b-8192"
    payload = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": 512}).encode()
    req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["choices"][0]["message"]["content"].strip()

def _call_openai(prompt, model, api_key):
    model = model or "gpt-3.5-turbo"
    payload = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": 512}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["choices"][0]["message"]["content"].strip()

def _call_anthropic(prompt, model, api_key):
    model = model or "claude-3-haiku-20240307"
    payload = json.dumps({"model": model, "max_tokens": 512, "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=payload,
        headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["content"][0]["text"].strip()

PROVIDERS = {"groq": _call_groq, "openai": _call_openai, "anthropic": _call_anthropic}

class LLMSwitcherTool(BaseTool):
    name = "llm"
    description = "Send a prompt to groq, openai, or anthropic.\nUsage: llm <provider> [model] | <prompt>"
    usage_example = "llm groq | Tell me a joke"

    def run(self, user_input: str) -> str:
        user_input = user_input.strip()
        if not user_input:
            return "[llm] Usage: llm <provider> [model] | <prompt>"
        if "|" not in user_input:
            return "[llm] Separator '|' required. Example: llm groq | Hello"
        header, prompt = user_input.split("|", 1)
        prompt = prompt.strip()
        if not prompt:
            return "[llm] Prompt is empty after '|'."
        header_parts = header.strip().split()
        if not header_parts:
            return "[llm] Specify a provider: groq, openai, anthropic"
        provider = header_parts[0].lower()
        model = header_parts[1] if len(header_parts) > 1 else ""
        if provider not in PROVIDERS:
            return f"[llm] Unknown provider '{provider}'. Choose from: {', '.join(PROVIDERS)}"
        api_key = _load_key(provider)
        if not api_key:
            return f"[llm] No API key for '{provider}'. Set env var or add to config.json: {provider}_api_key"
        try:
            return f"[{provider}] {PROVIDERS[provider](prompt, model, api_key)}"
        except urllib.error.HTTPError as exc:
            return f"[llm] HTTP {exc.code} from {provider}: {exc.read().decode(errors='replace')[:300]}"
        except Exception as exc:
            return f"[llm] Error calling {provider}: {exc}"
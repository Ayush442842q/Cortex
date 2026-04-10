"""
config.py — Loads and manages agent configuration from config.json
"""

import json
import os
import sys

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
PLACEHOLDER = "API_KEY_HERE"

DEFAULTS = {
    "api_key": PLACEHOLDER,
    "model": "llama-3.3-70b-versatile",
    "theme": "monokai",
    "max_iterations": 10,
    "timeout_seconds": 30,
    "show_thinking": True
}


def load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULTS.copy())
        print(f"[!] config.json not found — created at: {CONFIG_FILE}")
        print("[!] Add your Groq API key and restart.\n")

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            user_config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[!] config.json is invalid JSON: {e}")
        sys.exit(1)
    except OSError as e:
        print(f"[!] Could not read config.json: {e}")
        sys.exit(1)

    return {**DEFAULTS, **user_config}


def save_config(config: dict):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except OSError as e:
        print(f"[!] Could not save config.json: {e}")


def get_api_key(config: dict) -> str:
    from rich.console import Console
    from rich.prompt import Prompt
    console = Console()

    # 1. config.json
    key = config.get("api_key", "").strip()
    if key and key != PLACEHOLDER and key.startswith("gsk_"):
        return key

    # 2. Environment variable
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if key and key.startswith("gsk_"):
        return key

    # 3. Ask user
    console.print("\n[yellow]⚠  No Groq API key found.[/yellow]")
    key = Prompt.ask("Enter your Groq API key", password=True)

    if not key or not key.strip().startswith("gsk_"):
        console.print("[red]❌ Invalid key. Must start with 'gsk_'. Exiting.[/red]")
        sys.exit(1)

    save_it = Prompt.ask("Save to config.json?", choices=["y", "n"], default="y")
    if save_it == "y":
        config["api_key"] = key.strip()
        save_config(config)
        console.print("[green]✅ Key saved.[/green]")

    return key.strip()

"""
main.py — Entry point for AgentBase

Run with:
    python main.py
"""

import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from config import load_config, get_api_key
from agent import Agent

console = Console()


def show_banner():
    console.print(Panel.fit(
        "[bold cyan]🤖  AgentBase[/bold cyan]\n"
        "[dim]Your extensible AI agent — powered by Groq[/dim]\n"
        "[yellow]Add tools weekly. Build something great.[/yellow]",
        border_style="cyan",
        padding=(1, 4)
    ))


def show_help():
    console.print("\n[bold]Commands:[/bold]")
    console.print("  [cyan]tools[/cyan]    — List all loaded tools")
    console.print("  [cyan]clear[/cyan]    — Clear conversation memory")
    console.print("  [cyan]reset[/cyan]    — Same as clear")
    console.print("  [cyan]help[/cyan]     — Show this menu")
    console.print("  [cyan]exit[/cyan]     — Quit\n")
    console.print("[dim]Anything else → sent directly to the agent as a task[/dim]\n")


def main():
    config = load_config()
    api_key = get_api_key(config)

    show_banner()
    show_help()

    agent = Agent(
        api_key=api_key,
        model=config.get("model", "llama-3.3-70b-versatile"),
        max_iterations=config.get("max_iterations", 10),
        show_thinking=config.get("show_thinking", True),
        theme=config.get("theme", "monokai")
    )

    console.print(f"[green]✅ Agent ready. {len(agent.tools)} tool(s) loaded.[/green]\n")

    while True:
        try:
            user_input = Prompt.ask("[bold yellow]You[/bold yellow]").strip()

            if not user_input:
                continue

            cmd = user_input.lower()

            if cmd == "exit":
                console.print("[cyan]Goodbye! 🚀[/cyan]")
                break

            elif cmd in ("clear", "reset"):
                agent.reset_history()

            elif cmd == "tools":
                agent.show_tools()

            elif cmd == "help":
                show_help()

            else:
                # Send to agent
                agent.run(user_input)

        except KeyboardInterrupt:
            console.print("\n[cyan]Goodbye! 🚀[/cyan]")
            break


if __name__ == "__main__":
    main()

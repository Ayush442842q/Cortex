"""
agent.py — The main agent loop

This is the heart of the system.
It connects the Brain (thinking) to the Tools (doing)
and runs the ReAct loop: Think → Act → Observe → Repeat
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from brain import Brain
from tools import load_all_tools

console = Console()


class Agent:
    def __init__(self, api_key: str, model: str, max_iterations: int = 10,
                 show_thinking: bool = True, theme: str = "monokai"):
        self.tools = load_all_tools()
        self.brain = Brain(
            api_key=api_key,
            model=model,
            tools=self.tools,
            show_thinking=show_thinking
        )
        self.max_iterations = max_iterations
        self.show_thinking = show_thinking
        self.theme = theme
        self.history = []  # Conversation memory within a session

    def run(self, goal: str):
        """
        Run the agent on a user goal.
        Loops: Think → Pick Tool → Run Tool → Observe → Repeat
        Stops when tool == "respond" or max_iterations reached.
        """
        console.print(f"\n[bold cyan]🎯 Goal:[/bold cyan] {goal}\n")

        for iteration in range(1, self.max_iterations + 1):

            # Brain decides what to do
            with console.status("[bold cyan]🧠 Thinking...[/bold cyan]", spinner="dots"):
                decision = self.brain.decide(goal, self.history)

            tool_name = decision.get("tool", "respond")
            tool_input = decision.get("input", "")
            thinking = decision.get("thinking", "")

            # Show thinking if enabled
            if self.show_thinking and thinking:
                console.print(f"[dim]💭 {thinking}[/dim]")

            # Show which tool is being used
            if tool_name != "respond":
                console.print(f"[bold yellow]🔧 Using tool:[/bold yellow] [cyan]{tool_name}[/cyan]")
                console.print(f"[dim]   Input: {tool_input}[/dim]\n")

            # Get the tool
            tool = self.tools.get(tool_name)
            if not tool:
                console.print(f"[red]❌ Unknown tool: {tool_name}[/red]")
                break

            # Run the tool
            try:
                result = tool.run(tool_input)
            except Exception as e:
                result = f"Tool error: {e}"
                console.print(f"[red]❌ Tool failed: {e}[/red]")

            # If it's the respond tool, show final answer and stop
            if tool_name == "respond":
                console.print(Panel(
                    result,
                    title="[bold green]✅ Agent Response[/bold green]",
                    border_style="green"
                ))
                # Save to history
                self.history.append({
                    "user": goal,
                    "assistant": f"[Tool: {tool_name}] {result}"
                })
                return result

            # Otherwise, show the tool result and continue the loop
            console.print(Panel(
                str(result),
                title=f"[yellow]📤 Result from {tool_name}[/yellow]",
                border_style="yellow"
            ))

            # Add result to history so brain knows what happened
            self.history.append({
                "user": goal,
                "assistant": f"[Tool: {tool_name}] Input: {tool_input}\nResult: {result}"
            })

            # Update goal context with what we just did
            goal = (
                f"Original task: {goal}\n"
                f"Last action: Used '{tool_name}' with input '{tool_input}'\n"
                f"Result: {result}\n"
                f"Continue until the original task is fully complete."
            )

        console.print(f"[red]⚠ Reached max iterations ({self.max_iterations}). Stopping.[/red]")

    def reset_history(self):
        """Clear session memory."""
        self.history = []
        console.print("[dim]🔄 Memory cleared.[/dim]")

    def show_tools(self):
        """Display all loaded tools."""
        from rich.table import Table
        table = Table(title="🧰 Loaded Tools", border_style="cyan")
        table.add_column("Tool", style="cyan", width=20)
        table.add_column("Description", style="white")
        for name, tool in self.tools.items():
            table.add_row(name, tool.description)
        console.print(table)

from tools import BaseTool


class TerminalTool(BaseTool):
    name = "terminal"
    description = (
        "Run shell commands in the terminal and return the output. "
        "Pass any command as input, e.g. 'ls', 'echo hello', 'git status'."
    )
    usage_example = "echo hello"

    def run(self, input: str) -> str:
        command = input.strip()
        if not command:
            return "No command provided. Example: 'echo hello'"
        return f"Command received: '{command}' — execution not yet implemented."

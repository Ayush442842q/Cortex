import subprocess
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
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            return self._format(result.stdout, result.stderr, result.returncode)
        except Exception as e:
            return f"Error running command: {e}"

    def _format(self, stdout: str, stderr: str, code: int) -> str:
        lines = [f"Exit code: {code}"]
        if stdout.strip():
            lines.append(f"\n--- stdout ---\n{stdout.strip()}")
        if stderr.strip():
            lines.append(f"\n--- stderr ---\n{stderr.strip()}")
        if not stdout.strip() and not stderr.strip():
            lines.append("(no output)")
        return "\n".join(lines)

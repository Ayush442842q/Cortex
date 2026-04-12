import subprocess
from tools import BaseTool


class TerminalTool(BaseTool):
    name = "terminal"
    description = (
        "Run shell commands in the terminal and return the output. "
        "Pass any command as input, e.g. 'ls', 'echo hello', 'git status'. "
        "Long-running commands are killed after 30 seconds."
    )
    usage_example = "echo hello"

    TIMEOUT = 30  # seconds

    def run(self, input: str) -> str:
        command = input.strip()
        if not command:
            return "No command provided. Example: 'echo hello'"
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            try:
                stdout, stderr = process.communicate(timeout=self.TIMEOUT)
                return self._format(stdout, stderr, process.returncode, timed_out=False)
            except (subprocess.TimeoutExpired, KeyboardInterrupt):
                process.kill()
                process.communicate()
                return self._format("", f"Command timed out after {self.TIMEOUT}s.", -1, timed_out=True)
        except Exception as e:
            return f"Error running command: {e}"

    def _format(self, stdout: str, stderr: str, code: int, timed_out: bool = False) -> str:
        lines = [f"Exit code: {code}"]
        if timed_out:
            lines.append("Status: TIMED OUT")
        if stdout.strip():
            lines.append(f"\n--- stdout ---\n{stdout.strip()}")
        if stderr.strip():
            lines.append(f"\n--- stderr ---\n{stderr.strip()}")
        if not stdout.strip() and not stderr.strip():
            lines.append("(no output)")
        return "\n".join(lines)

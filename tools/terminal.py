import os
import re
import subprocess
from tools import BaseTool


# Commands that could cause irreversible system damage
_BLOCKLIST = [
    r"\brm\s+-rf\b",
    r"\brmdir\s+/s\b",
    r"\bdel\s+/f\b",
    r"\bformat\b",
    r"\bmkfs\b",
    r"\bdd\b",
    r"\bshutdown\b",
    r"\breboot\b",
    r"\bhalt\b",
    r":\s*\(\s*\)\s*\{",    # fork bomb pattern: :(){
    r"\bsudo\s+rm\b",
    r"\bchmod\s+-R\s+777\b",
    r"> /dev/sd",
    r"\bwipefs\b",
]


def _is_blocked(command: str) -> str | None:
    """Returns the matched pattern string if blocked, else None."""
    for pattern in _BLOCKLIST:
        if re.search(pattern, command, re.IGNORECASE):
            return pattern
    return None


class TerminalTool(BaseTool):
    name = "terminal"
    description = (
        "Run shell commands in the terminal and return the output. "
        "Supports: 'run <command>', 'cd <path>', 'setenv KEY=VALUE', 'getenv KEY'. "
        "Dangerous commands (rm -rf, format, shutdown, etc.) are blocked. "
        "Example: 'run git status', 'cd H:/myproject', 'setenv DEBUG=1'."
    )
    usage_example = "run echo hello"

    TIMEOUT = 30

    def __init__(self):
        self._cwd = os.getcwd()
        self._env = os.environ.copy()

    def run(self, input: str) -> str:
        input = input.strip()
        if not input:
            return "No command provided. Example: 'run echo hello'"

        if input.lower().startswith("cd "):
            return self._change_dir(input[3:].strip())

        if input.lower().startswith("setenv "):
            return self._set_env(input[7:].strip())

        if input.lower().startswith("getenv "):
            return self._get_env(input[7:].strip())

        command = input[4:].strip() if input.lower().startswith("run ") else input

        blocked = _is_blocked(command)
        if blocked:
            return (
                f"Blocked: command matches dangerous pattern and was not executed.\n"
                f"If you intended something safe, rephrase the command."
            )

        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self._cwd,
                env=self._env
            )
            try:
                stdout, stderr = process.communicate(timeout=self.TIMEOUT)
                return self._format(stdout, stderr, process.returncode)
            except (subprocess.TimeoutExpired, KeyboardInterrupt):
                process.kill()
                process.communicate()
                return self._format("", f"Command timed out after {self.TIMEOUT}s.", -1, timed_out=True)
        except Exception as e:
            return f"Error running command: {e}"

    def _change_dir(self, path: str) -> str:
        path = os.path.expanduser(path)
        if not os.path.isdir(path):
            return f"Directory not found: {path}"
        self._cwd = os.path.abspath(path)
        return f"Working directory changed to: {self._cwd}"

    def _set_env(self, expr: str) -> str:
        if "=" not in expr:
            return "Usage: setenv KEY=VALUE"
        key, _, value = expr.partition("=")
        key = key.strip()
        value = value.strip()
        if not key:
            return "Invalid: key cannot be empty."
        self._env[key] = value
        return f"Set {key}={value}"

    def _get_env(self, key: str) -> str:
        key = key.strip()
        value = self._env.get(key)
        if value is None:
            return f"{key} is not set."
        return f"{key}={value}"

    def _format(self, stdout: str, stderr: str, code: int, timed_out: bool = False) -> str:
        lines = [f"[cwd: {self._cwd}]", f"Exit code: {code}"]
        if timed_out:
            lines.append("Status: TIMED OUT")
        if stdout.strip():
            lines.append(f"\n--- stdout ---\n{stdout.strip()}")
        if stderr.strip():
            lines.append(f"\n--- stderr ---\n{stderr.strip()}")
        if not stdout.strip() and not stderr.strip():
            lines.append("(no output)")
        return "\n".join(lines)

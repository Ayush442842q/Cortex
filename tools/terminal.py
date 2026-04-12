"""
tools/terminal.py
=================
TerminalTool — shell command execution for the Cortex agent.

All operations are invoked through run(input) where input is a
plain-English command string.

Supported commands:
  run <command>        — execute any shell command
  cd <path>            — change working directory for subsequent commands
  cwd                  — print current working directory
  setenv KEY=VALUE     — set an environment variable for this session
  getenv KEY           — retrieve an environment variable
  which <program>      — find a program on PATH

Safety:
  Dangerous commands (rm -rf, format, shutdown, dd, etc.) are blocked
  by a regex blocklist and never executed.

Cross-platform:
  Works on Windows (cmd.exe) and Linux/macOS (sh).
  Long-running commands are killed after TIMEOUT seconds.
"""

import os
import re
import shutil
import subprocess
import sys
from tools import BaseTool

G     = "\033[92m"
R     = "\033[91m"
B     = "\033[96m"
RESET = "\033[0m"

_IS_WINDOWS = sys.platform.startswith("win")

# ── Blocklist ─────────────────────────────────────────────────────────────────

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
    r":\s*\(\s*\)\s*\{",
    r"\bsudo\s+rm\b",
    r"\bchmod\s+-R\s+777\b",
    r"> /dev/sd",
    r"\bwipefs\b",
]


def _is_blocked(command: str) -> bool:
    """Return True if the command matches any entry in the blocklist."""
    for pattern in _BLOCKLIST:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False


# ── Tool ──────────────────────────────────────────────────────────────────────

class TerminalTool(BaseTool):
    """
    Shell execution tool for the Cortex agent.

    Runs commands in a subprocess, captures stdout + stderr, enforces a
    timeout, blocks dangerous commands, and tracks working directory and
    environment variables across calls within the same session.
    """

    name = "terminal"
    description = (
        "Run shell commands in the terminal and return the output. "
        "Supports: 'run <command>', 'cd <path>', 'setenv KEY=VALUE', "
        "'getenv KEY', 'which <program>', 'cwd'. "
        "Dangerous commands are blocked. Works on Windows and Linux/macOS. "
        "Example: 'run git status', 'which python', 'cwd'."
    )
    usage_example = "run echo hello"

    TIMEOUT = 30

    def __init__(self):
        self._cwd = os.getcwd()
        self._env = os.environ.copy()

    # ── Entry point ───────────────────────────────────────────────────────────

    def run(self, input: str) -> str:
        """Parse the command string and dispatch to the right helper."""
        if not input or not input.strip():
            return "No command provided. Example: 'run echo hello'"

        input = input.strip()
        lower = input.lower()

        if lower == "cwd":
            return f"Current working directory: {self._cwd}"

        if lower.startswith("cd "):
            return self._change_dir(input[3:].strip())

        if lower.startswith("setenv "):
            return self._set_env(input[7:].strip())

        if lower.startswith("getenv "):
            return self._get_env(input[7:].strip())

        if lower.startswith("which ") or lower.startswith("where "):
            return self._which(input.split(None, 1)[1].strip())

        command = input[4:].strip() if lower.startswith("run ") else input

        if not command:
            return "Empty command after 'run'."

        if _is_blocked(command):
            return (
                "Blocked: command matches a dangerous pattern and was not executed.\n"
                "If you intended something safe, rephrase the command."
            )

        return self._execute(command)

    # ── Execution ─────────────────────────────────────────────────────────────

    def _execute(self, command: str) -> str:
        """Run a shell command in a subprocess and return formatted output."""
        try:
            kwargs = dict(
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self._cwd,
                env=self._env,
            )
            if _IS_WINDOWS:
                kwargs["encoding"] = "utf-8"
                kwargs["errors"] = "replace"

            process = subprocess.Popen(command, **kwargs)
            try:
                stdout, stderr = process.communicate(timeout=self.TIMEOUT)
                return self._format(stdout, stderr, process.returncode)
            except (subprocess.TimeoutExpired, KeyboardInterrupt):
                process.kill()
                process.communicate()
                return self._format(
                    "", f"Command timed out after {self.TIMEOUT}s.", -1, timed_out=True
                )
        except Exception as e:
            return f"Error running command: {e}"

    # ── Sub-commands ──────────────────────────────────────────────────────────

    def _change_dir(self, path: str) -> str:
        """Change the persistent working directory for this session."""
        path = os.path.expanduser(path.strip())
        if not path:
            return "Usage: cd <path>"
        if not os.path.isdir(path):
            return f"Directory not found: {path}"
        self._cwd = os.path.abspath(path)
        return f"Working directory changed to: {self._cwd}"

    def _set_env(self, expr: str) -> str:
        """Set a session-scoped environment variable (KEY=VALUE)."""
        if not expr or "=" not in expr:
            return "Usage: setenv KEY=VALUE"
        key, _, value = expr.partition("=")
        key, value = key.strip(), value.strip()
        if not key:
            return "Invalid: key cannot be empty."
        self._env[key] = value
        return f"Set {key}={value}"

    def _get_env(self, key: str) -> str:
        """Retrieve a session or system environment variable by name."""
        key = key.strip()
        if not key:
            return "Usage: getenv KEY"
        value = self._env.get(key)
        if value is None:
            return f"{key} is not set."
        return f"{key}={value}"

    def _which(self, program: str) -> str:
        """Find the full path of an executable on the current PATH."""
        if not program:
            return "Usage: which <program>"
        path = shutil.which(program, path=self._env.get("PATH"))
        if path:
            return f"{program} found at: {path}"
        return f"{program} not found in PATH."

    # ── Output formatter ──────────────────────────────────────────────────────

    def _format(self, stdout: str, stderr: str, code: int, timed_out: bool = False) -> str:
        """Format command output into a readable string for the agent."""
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


# ── Standalone self-test suite ────────────────────────────────────────────────

if __name__ == "__main__":
    import tempfile

    tool = TerminalTool()
    passed = 0
    failed = 0

    def check(label: str, result: str, expected: str):
        global passed, failed
        if expected.lower() in result.lower():
            print(f"  {G}✔{RESET}  {label}")
            passed += 1
        else:
            print(f"  {R}✘{RESET}  {label}")
            print(f"       got: {result[:120]}")
            failed += 1

    print()
    print(f"{B}{'='*55}{RESET}")
    print(f"{B}  Terminal Tool — self-test{RESET}")
    print(f"{B}{'='*55}{RESET}")

    # Basic echo
    check("echo command",    tool.run("run echo hello cortex"), "hello cortex")

    # cwd
    check("cwd",             tool.run("cwd"),                   "working directory")

    # cd to temp dir
    with tempfile.TemporaryDirectory() as tmp:
        check("cd valid",    tool.run(f"cd {tmp}"),             "changed to")
        check("cwd updated", tool.run("cwd"),                   tmp.lower()[:10])
        check("cd invalid",  tool.run("cd /this/does/not/exist/xyz"), "not found")

    # env vars
    check("setenv",          tool.run("setenv CORTEX_TEST=42"), "set cortex_test=42")
    check("getenv",          tool.run("getenv CORTEX_TEST"),    "cortex_test=42")
    check("getenv missing",  tool.run("getenv CORTEX_NOKEY"),   "not set")

    # which / where
    check("which python",    tool.run("which python"),          "python")

    # blocklist
    check("blocked rm -rf",  tool.run("run rm -rf /"),          "blocked")
    check("blocked shutdown", tool.run("run shutdown /s /t 0"), "blocked")
    check("blocked format",  tool.run("run format C:"),         "blocked")

    # timeout
    check("timeout",         tool.run("run python -c \"import time; time.sleep(60)\""), "timed out")

    # empty command
    check("empty input",     tool.run(""),                      "no command")
    check("empty run",       tool.run("run"),                   "empty command")

    print()
    print(f"  Results: {G}{passed} passed{RESET}  {R}{failed} failed{RESET}")
    print(f"{B}{'='*55}{RESET}")
    print()
    if failed:
        sys.exit(1)

"""
tools/code_writer.py — Week 1 Tool: Code Writer

Auto-discovered by Cortex on next run. No other changes needed.

- Extracts Python code from agent input (plain or ```python blocks)
- Executes it in a sandboxed subprocess with a timeout
- Returns stdout + stderr so the agent can reason on results
- Auto-installs missing pip packages and retries once
- Windows-safe: uses Popen + communicate() (works with Anaconda)
"""

import os
import re
import sys
import subprocess
import tempfile
import textwrap

# ── Self-setup ────────────────────────────────────────────────────────────────

_SANDBOX_DIR = os.path.expanduser("~/.agentbase/sandbox")

def _setup():
    if sys.version_info < (3, 7):
        print("[code_writer] WARNING: Python 3.7+ recommended.")
    os.makedirs(_SANDBOX_DIR, exist_ok=True)

_setup()

# ── BaseTool import ───────────────────────────────────────────────────────────

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name = "base_tool"
        description = ""
        usage_example = ""
        def run(self, input: str) -> str:
            raise NotImplementedError


# ── Helpers ───────────────────────────────────────────────────────────────────

def _extract_code(raw: str) -> str:
    fenced = re.search(r"```(?:python)?\s*\n(.*?)```", raw, re.DOTALL)
    if fenced:
        return fenced.group(1).strip()
    return textwrap.dedent(raw).strip()


def _auto_install(error_output: str) -> list:
    installed = []
    pattern = re.findall(r"No module named ['\"]([a-zA-Z0-9_\-]+)['\"]", error_output)
    for pkg in set(pattern):
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "-q"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            installed.append(pkg)
    return installed


def _run_code(code: str, timeout: int = 15) -> dict:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", dir=_SANDBOX_DIR,
        delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        tmp_path = f.name

    process = subprocess.Popen(
        [sys.executable, tmp_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, cwd=_SANDBOX_DIR
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return {
            "stdout": stdout.strip(), "stderr": stderr.strip(),
            "returncode": process.returncode, "timed_out": False
        }
    except (subprocess.TimeoutExpired, KeyboardInterrupt):
        process.kill()
        process.communicate()
        return {
            "stdout": "", "stderr": f"Execution timed out after {timeout}s.",
            "returncode": -1, "timed_out": True
        }
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


# ── Tool class ────────────────────────────────────────────────────────────────

class CodeWriterTool(BaseTool):
    name = "code_writer"
    description = (
        "Write and execute Python code. Pass the code as input (plain or in a "
        "```python block). Returns stdout, stderr, and exit code so you can "
        "reason on the result. Auto-installs missing packages."
    )
    usage_example = "```python\nimport math\nprint(math.sqrt(144))\n```"
    TIMEOUT = 15

    def run(self, input: str) -> str:
        if not input.strip():
            return "No code provided. Please pass Python code as input."
        code = _extract_code(input)
        if not code:
            return "Could not extract any code from the input."
        result = _run_code(code, timeout=self.TIMEOUT)
        if result["returncode"] != 0 and "No module named" in result["stderr"]:
            installed = _auto_install(result["stderr"])
            if installed:
                result = _run_code(code, timeout=self.TIMEOUT)
                if result["returncode"] == 0:
                    result["stderr"] = (
                        f"[Auto-installed: {', '.join(installed)}]\n" + result["stderr"]
                    ).strip()
        return _format_result(result, code)


def _format_result(result: dict, code: str) -> str:
    lines = [f"Exit code: {result['returncode']}"]
    if result["timed_out"]:
        lines.append("Status: TIMED OUT")
    if result["stdout"]:
        lines.append("\n--- stdout ---")
        lines.append(result["stdout"])
    if result["stderr"]:
        lines.append("\n--- stderr ---")
        lines.append(result["stderr"])
    if not result["stdout"] and not result["stderr"]:
        lines.append("(no output)")
    return "\n".join(lines)


# ── Standalone test ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  Cortex — Code Writer Tool  (Week 1)")
    print("=" * 55)
    print(f"  Sandbox dir : {_SANDBOX_DIR}")
    print(f"  Python      : {sys.executable}")
    print(f"  Timeout     : {CodeWriterTool.TIMEOUT}s per run")
    print("=" * 55)

    tool = CodeWriterTool()
    tests = [
        ("Basic print",   "print('Hello from Cortex!')"),
        ("Math",          "import math\nprint(f'pi = {math.pi:.4f}')\nprint(f'sqrt(2) = {math.sqrt(2):.4f}')"),
        ("Fenced block",  "```python\nfor i in range(5):\n    print(f'item {i}')\n```"),
        ("Syntax error",  "def broken(\n    print('oops')"),
        ("Timeout guard", "import time\ntime.sleep(30)\nprint('done')"),
    ]
    for label, code in tests:
        print(f"\n[TEST] {label}")
        print("-" * 40)
        print(tool.run(code))

    print("\n" + "=" * 55)
    print("  All 5 tests done. Drop into tools/ and go!")
    print("=" * 55)

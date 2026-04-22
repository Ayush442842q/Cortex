"""
tools/env_setup.py — Week 4 Tool: Environment Setup

Auto-discovered by Cortex on next run. No other changes needed.

- Creates virtual environments (venv)
- Installs pip packages individually or from requirements.txt
- Scaffolds new project folder structures
- Shows info about the current Python environment
- Lists installed packages
- Works on Windows, Mac, and Linux
"""

import os
import sys
import subprocess
import shutil
import re


try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name = "base_tool"
        description = ""
        usage_example = ""
        def run(self, input: str) -> str:
            raise NotImplementedError


class EnvSetupTool(BaseTool):
    name = "env_setup"
    description = (
        "Set up development environments: create virtual envs, install packages, "
        "scaffold project structures, and inspect the current Python environment. "
        "Commands: 'create-venv <path>', 'install <package>', "
        "'install-reqs <requirements.txt>', 'scaffold <project-name>', "
        "'info', 'list-packages'."
    )
    usage_example = "create-venv ./myenv"

    def run(self, input: str) -> str:
        input = input.strip()
        if not input:
            return "No command provided. Example: 'create-venv ./myenv'"

        parts = input.split(None, 1)
        action = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        try:
            if action == "create-venv":
                return self._create_venv(arg)
            elif action == "install":
                return self._install_package(arg)
            elif action == "install-reqs":
                return self._install_requirements(arg)
            elif action == "scaffold":
                return self._scaffold_project(arg)
            elif action == "info":
                return self._env_info()
            elif action == "list-packages":
                return self._list_packages()
            else:
                return (
                    f"Unknown command: '{action}'. "
                    "Available: create-venv, install, install-reqs, "
                    "scaffold, info, list-packages"
                )
        except Exception as e:
            return f"Error: {e}"

    # ── Actions ───────────────────────────────────────────────────────────────

    def _create_venv(self, path: str) -> str:
        if not path:
            return "Usage: create-venv <path>  e.g. create-venv ./myenv"
        path = os.path.expanduser(path)
        if os.path.exists(path):
            return f"Path already exists: {path}"
        result = subprocess.run(
            [sys.executable, "-m", "venv", path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return f"Failed to create venv:\n{result.stderr}"
        # Detect activate script path
        if os.name == "nt":
            activate = os.path.join(path, "Scripts", "activate")
        else:
            activate = os.path.join(path, "bin", "activate")
        return (
            f"Virtual environment created at: {path}\n"
            f"Activate with:\n"
            f"  Windows : {activate}.bat\n"
            f"  Mac/Linux: source {activate}"
        )

    def _install_package(self, package: str) -> str:
        if not package:
            return "Usage: install <package-name>  e.g. install requests"
        packages = [p.strip() for p in package.split(",") if p.strip()]
        results = []
        for pkg in packages:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", pkg],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                # Extract version from pip output
                version_match = re.search(
                    rf"Successfully installed.*?{re.escape(pkg)}-([^\s]+)",
                    result.stdout
                )
                ver = version_match.group(1) if version_match else "latest"
                results.append(f"  ✔ {pkg} ({ver})")
            else:
                err = result.stderr.strip().split("\n")[-1]
                results.append(f"  ✘ {pkg} — {err}")
        return "Package installation results:\n" + "\n".join(results)

    def _install_requirements(self, path: str) -> str:
        if not path:
            return "Usage: install-reqs <path/to/requirements.txt>"
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return f"File not found: {path}"
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return f"Failed:\n{result.stderr.strip()}"
        # Count packages installed
        installed = re.findall(r"Successfully installed (.+)", result.stdout)
        summary = installed[0] if installed else "All packages already satisfied."
        return f"Requirements installed from {path}:\n{summary}"

    def _scaffold_project(self, name: str) -> str:
        if not name:
            return "Usage: scaffold <project-name>"
        name = name.strip().replace(" ", "_")
        base = os.path.join(os.getcwd(), name)
        if os.path.exists(base):
            return f"Directory already exists: {base}"

        # Project structure
        structure = {
            "": ["README.md", "requirements.txt", ".gitignore", "main.py"],
            "src": ["__init__.py"],
            "tests": ["__init__.py", "test_main.py"],
            "docs": [],
        }

        created = []
        for folder, files in structure.items():
            dir_path = os.path.join(base, folder) if folder else base
            os.makedirs(dir_path, exist_ok=True)
            for fname in files:
                fpath = os.path.join(dir_path, fname)
                with open(fpath, "w", encoding="utf-8") as f:
                    if fname == "README.md":
                        f.write(f"# {name}\n\nProject description here.\n")
                    elif fname == ".gitignore":
                        f.write("__pycache__/\n*.pyc\n.env\nvenv/\n.venv/\ndist/\nbuild/\n")
                    elif fname == "requirements.txt":
                        f.write("# Add your dependencies here\n")
                    elif fname == "main.py":
                        f.write(f'"""Entry point for {name}."""\n\ndef main():\n    print("Hello from {name}!")\n\nif __name__ == "__main__":\n    main()\n')
                    elif fname == "test_main.py":
                        f.write(f'"""Tests for {name}."""\n\ndef test_placeholder():\n    assert True\n')
                created.append(("  " if folder else "") + ("  " if not folder else "") + fpath.replace(base, name))

        lines = [f"Project scaffolded at: {base}", "", "Structure created:"]
        lines += [f"  {name}/"]
        for folder, files in structure.items():
            if folder:
                lines.append(f"    {folder}/")
            for fname in files:
                indent = "      " if folder else "    "
                lines.append(f"{indent}{fname}")
        return "\n".join(lines)

    def _env_info(self) -> str:
        pip_ver = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True, text=True
        ).stdout.strip()
        in_venv = (
            hasattr(sys, "real_prefix") or
            (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
        )
        return (
            f"Python version : {sys.version}\n"
            f"Executable     : {sys.executable}\n"
            f"Pip            : {pip_ver}\n"
            f"In virtualenv  : {'Yes' if in_venv else 'No'}\n"
            f"Working dir    : {os.getcwd()}"
        )

    def _list_packages(self) -> str:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=columns"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return f"Failed to list packages: {result.stderr}"
        lines = result.stdout.strip().split("\n")
        count = max(0, len(lines) - 2)  # subtract header rows
        return f"Installed packages ({count} total):\n\n" + result.stdout.strip()


# ── Standalone test ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import tempfile
    print("=" * 55)
    print("  Cortex — Environment Setup Tool  (Week 4)")
    print("=" * 55)

    tool = EnvSetupTool()

    print("\n[TEST] env info")
    print("-" * 40)
    print(tool.run("info"))

    print("\n[TEST] install package")
    print("-" * 40)
    print(tool.run("install requests"))

    print("\n[TEST] list packages")
    print("-" * 40)
    output = tool.run("list-packages")
    # just show first 5 lines to keep output short
    lines = output.split("\n")
    print("\n".join(lines[:7]) + "\n  ...")

    print("\n[TEST] scaffold project")
    print("-" * 40)
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        print(tool.run("scaffold my_project"))

    print("\n[TEST] create venv")
    print("-" * 40)
    with tempfile.TemporaryDirectory() as tmp:
        venv_path = os.path.join(tmp, "testvenv")
        print(tool.run(f"create-venv {venv_path}"))

    print("\n" + "=" * 55)
    print("  All tests done. Drop into tools/ and go!")
    print("=" * 55)

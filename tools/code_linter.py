"""Cortex — Code Linter Tool (Week 25) [Developer]
Lint Python files using pyflakes (stdlib only fallback available).
"""
from __future__ import annotations
import subprocess, sys, os, ast, re
try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=description=usage_example=""
        def run(self,i): raise NotImplementedError

def _ast_check(path):
    """Basic lint using ast — no external deps needed."""
    issues=[]
    try:
        src=open(path,encoding="utf-8",errors="replace").read()
        tree=ast.parse(src,filename=path)
    except SyntaxError as e:
        return [f"SyntaxError: {e}"]
    # detect unused imports (simple heuristic)
    imports={}
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):
            for alias in node.names:
                name=alias.asname or alias.name.split(".")[0]
                imports[name]=node.lineno
        elif isinstance(node,ast.ImportFrom):
            for alias in node.names:
                name=alias.asname or alias.name
                imports[name]=node.lineno
    # check if name appears in source beyond its import line
    src_lines=src.splitlines()
    for name,lineno in imports.items():
        rest="\n".join(src_lines[lineno:])
        if not re.search(r"\b"+re.escape(name)+r"\b",rest):
            issues.append(f"Line {lineno}: possibly unused import: {name!r}")
    return issues or ["No issues found (basic AST check)"]

class CodeLinterTool(BaseTool):
    name="lint"
    description="Lint Python code. Commands: lint <file> | check <file> | syntax <file>"
    usage_example="lint myfile.py"

    def run(self, inp: str) -> str:
        inp=inp.strip()
        if not inp: return "[lint] Provide a Python file path"
        parts=inp.split(None,1)
        cmd=parts[0].lower() if len(parts)>1 else "lint"
        path=parts[1].strip() if len(parts)>1 else parts[0]
        if cmd not in ("lint","check","syntax"): path=inp; cmd="lint"
        if not os.path.exists(path): return f"[lint] File not found: {path}"
        if not path.endswith(".py"): return f"[lint] Only .py files supported"
        # try pyflakes first
        try:
            r=subprocess.run([sys.executable,"-m","pyflakes",path],capture_output=True,text=True,timeout=15)
            output=(r.stdout+r.stderr).strip()
            if not output: output="No issues found"
            return f"[lint: {path}]\n{output}"
        except Exception:
            pass
        # fallback: ast check
        issues=_ast_check(path)
        return f"[lint (AST): {path}]\n"+chr(10).join(issues)

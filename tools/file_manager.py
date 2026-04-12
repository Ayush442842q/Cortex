"""
tools/file_manager.py
=====================
FileManagerTool — file-system operations for the Cortex agent.

Supported commands (all via run(input)):
  read   <path>               — read a text file (50 KB cap)
  write  <path> | <content>  — overwrite / create a file
  append <path> | <content>  — append to a file
  list   <path>               — list directory contents
  mkdir  <path>               — create directory (incl. parents)
  delete <path>               — delete file or directory tree
  move   <src>  | <dest>     — move / rename
  copy   <src>  | <dest>     — copy file or directory tree
  search <path> | <pattern>  — recursive glob search
  exists <path>               — check whether a path exists
"""

import os
import re
import glob
import shutil
from tools import BaseTool

G     = "\033[92m"
R     = "\033[91m"
B     = "\033[96m"
RESET = "\033[0m"


class FileManagerTool(BaseTool):
    """
    File-system tool for the Cortex agent.

    All operations are invoked through run(input) where input is a
    plain-English command string. Two-argument commands use '|' as
    the separator (e.g. 'write notes.txt | Hello world').
    """

    name = "file_manager"
    description = (
        "Manage files and folders: read, write, append, list, create, "
        "delete, move, copy, search. Pass a command like: "
        "'read path/to/file', 'write path/to/file | content', "
        "'list path/', 'delete path/to/file', "
        "'move src | dest', 'copy src | dest', "
        "'search path/ | pattern', 'mkdir path/to/dir'."
    )
    usage_example = "read README.md"

    MAX_READ_BYTES = 50_000  # cap file reads at ~50 KB

    # ── Entry point ───────────────────────────────────────────────────────────

    def run(self, input: str) -> str:
        """
        Parse the command string and dispatch to the right action method.
        Returns a plain-text result that the agent can reason on.
        """
        input = input.strip()
        if not input:
            return "No command provided. Example: 'read README.md'"

        parts = re.split(r"\s*\|\s*", input, maxsplit=1)
        command_part = parts[0].strip()
        arg2 = parts[1].strip() if len(parts) > 1 else ""

        tokens = command_part.split(None, 1)
        if not tokens:
            return "Empty command."

        action = tokens[0].lower()
        path   = tokens[1].strip() if len(tokens) > 1 else ""

        try:
            if action == "read":
                return self._read(path)
            elif action == "write":
                return self._write(path, arg2)
            elif action == "append":
                return self._append(path, arg2)
            elif action in ("list", "ls"):
                return self._list(path or ".")
            elif action == "mkdir":
                return self._mkdir(path)
            elif action in ("delete", "rm"):
                return self._delete(path)
            elif action in ("move", "mv"):
                return self._move(path, arg2)
            elif action in ("copy", "cp"):
                return self._copy(path, arg2)
            elif action in ("search", "find"):
                return self._search(path, arg2)
            elif action == "exists":
                return self._exists(path)
            else:
                return (
                    f"Unknown action: '{action}'. "
                    "Available: read, write, append, list, delete, "
                    "move, copy, search, mkdir, exists"
                )
        except PermissionError:
            return f"Permission denied: {path}"
        except Exception as e:
            return f"Error: {e}"

    # ── Action methods ────────────────────────────────────────────────────────

    def _read(self, path: str) -> str:
        """Read a text file and return its contents (capped at MAX_READ_BYTES)."""
        if not path:
            return "Usage: read <path>"
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return f"File not found: {path}"
        if os.path.isdir(path):
            return f"{path} is a directory. Use 'list {path}' instead."
        size = os.path.getsize(path)
        if size > self.MAX_READ_BYTES:
            return (
                f"File too large ({size:,} bytes). "
                f"Max read size is {self.MAX_READ_BYTES:,} bytes."
            )
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        lines = content.count("\n") + 1
        return f"[{path}] ({lines} lines, {size:,} bytes)\n\n{content}"

    def _write(self, path: str, content: str) -> str:
        """Overwrite (or create) a file with content."""
        if not path:
            return "Usage: write <path> | <content>"
        if not content:
            return "No content provided. Usage: write <path> | <content>"
        path = os.path.expanduser(path)
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Written {len(content):,} chars to {path}"

    def _append(self, path: str, content: str) -> str:
        """Append content to an existing file (creates if absent)."""
        if not path:
            return "Usage: append <path> | <content>"
        if not content:
            return "No content provided. Usage: append <path> | <content>"
        path = os.path.expanduser(path)
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"Appended {len(content):,} chars to {path}"

    def _list(self, path: str) -> str:
        """List the contents of a directory (or stat a single file)."""
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return f"Path not found: {path}"
        if os.path.isfile(path):
            size = os.path.getsize(path)
            return f"[file] {path} ({size:,} bytes)"
        entries = sorted(os.listdir(path))
        if not entries:
            return f"{path}/ is empty."
        lines = []
        for e in entries:
            full = os.path.join(path, e)
            if os.path.isdir(full):
                lines.append(f"  [dir]  {e}/")
            else:
                size = os.path.getsize(full)
                lines.append(f"  [file] {e}  ({size:,} bytes)")
        return f"{path}/  ({len(entries)} items)\n" + "\n".join(lines)

    def _mkdir(self, path: str) -> str:
        """Create a directory (and any missing parents)."""
        if not path:
            return "Usage: mkdir <path>"
        path = os.path.expanduser(path)
        os.makedirs(path, exist_ok=True)
        return f"Directory ready: {path}"

    def _delete(self, path: str) -> str:
        """Delete a file or entire directory tree."""
        if not path:
            return "Usage: delete <path>"
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return f"Not found: {path}"
        if os.path.isdir(path):
            shutil.rmtree(path)
            return f"Deleted directory: {path}"
        os.remove(path)
        return f"Deleted file: {path}"

    def _move(self, src: str, dest: str) -> str:
        """Move or rename a file or directory."""
        if not src or not dest:
            return "Usage: move <src> | <dest>"
        src  = os.path.expanduser(src)
        dest = os.path.expanduser(dest)
        if not os.path.exists(src):
            return f"Source not found: {src}"
        if os.path.exists(dest):
            return f"Destination already exists: {dest}"
        shutil.move(src, dest)
        return f"Moved: {src} -> {dest}"

    def _copy(self, src: str, dest: str) -> str:
        """Copy a file or directory tree to a new location."""
        if not src or not dest:
            return "Usage: copy <src> | <dest>"
        src  = os.path.expanduser(src)
        dest = os.path.expanduser(dest)
        if not os.path.exists(src):
            return f"Source not found: {src}"
        if os.path.isdir(src):
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        return f"Copied: {src} -> {dest}"

    def _search(self, path: str, pattern: str) -> str:
        """Recursively search path for files matching a glob pattern."""
        if not path or not pattern:
            return "Usage: search <path> | <pattern>"
        path = os.path.expanduser(path)
        if not os.path.isdir(path):
            return f"Search path not found or not a directory: {path}"
        matches = glob.glob(os.path.join(path, "**", pattern), recursive=True)
        if not matches:
            return f"No matches for '{pattern}' in {path}"
        lines = [f"Found {len(matches)} match(es):"]
        for m in matches[:50]:
            lines.append(f"  {m}")
        if len(matches) > 50:
            lines.append(f"  ... and {len(matches) - 50} more")
        return "\n".join(lines)

    def _exists(self, path: str) -> str:
        """Check whether a path exists and whether it is a file or directory."""
        if not path:
            return "Usage: exists <path>"
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            return f"Yes — {path} is a directory."
        if os.path.isfile(path):
            return f"Yes — {path} is a file."
        return f"No — {path} does not exist."


# ── Standalone self-test suite ────────────────────────────────────────────────

if __name__ == "__main__":
    import tempfile
    import sys

    tool = FileManagerTool()
    passed = 0
    failed = 0

    def check(label: str, result: str, expected_fragment: str):
        global passed, failed
        if expected_fragment.lower() in result.lower():
            print(f"  {G}✔{RESET}  {label}")
            passed += 1
        else:
            print(f"  {R}✘{RESET}  {label}")
            print(f"       got: {result[:120]}")
            failed += 1

    print()
    print(f"{B}{'='*55}{RESET}")
    print(f"{B}  File Manager — self-test{RESET}")
    print(f"{B}{'='*55}{RESET}")

    with tempfile.TemporaryDirectory() as tmp:
        f   = os.path.join(tmp, "hello.txt")
        f2  = os.path.join(tmp, "hello_copy.txt")
        f3  = os.path.join(tmp, "hello_moved.txt")
        sub = os.path.join(tmp, "subdir")

        check("write",   tool.run(f"write {f} | Hello, Cortex!"), "written")
        check("read",    tool.run(f"read {f}"),                   "Hello, Cortex!")
        check("append",  tool.run(f"append {f} |  More content."), "appended")
        check("list",    tool.run(f"list {tmp}"),                  "hello.txt")
        check("mkdir",   tool.run(f"mkdir {sub}"),                 "directory ready")
        check("exists (file)", tool.run(f"exists {f}"),            "yes")
        check("exists (dir)",  tool.run(f"exists {sub}"),          "yes")
        check("copy",    tool.run(f"copy {f} | {f2}"),             "copied")
        check("move",    tool.run(f"move {f2} | {f3}"),            "moved")
        check("search",  tool.run(f"search {tmp} | *.txt"),        "match")
        check("delete",  tool.run(f"delete {f3}"),                 "deleted")
        check("exists (gone)", tool.run(f"exists {f3}"),           "no")
        check("read missing",  tool.run(f"read {tmp}/nope.txt"),   "not found")
        check("write no content", tool.run(f"write {f} |"),        "no content")
        check("unknown action",   tool.run("fly"),                  "unknown action")

    print()
    print(f"  Results: {G}{passed} passed{RESET}  {R}{failed} failed{RESET}")
    print(f"{B}{'='*55}{RESET}")
    print()
    if failed:
        sys.exit(1)

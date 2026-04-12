import os
import re
import shutil
from tools import BaseTool


class FileManagerTool(BaseTool):
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

    MAX_READ_BYTES = 50_000

    def run(self, input: str) -> str:
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
            else:
                return f"Action '{action}' not yet implemented."
        except PermissionError:
            return f"Permission denied: {path}"
        except Exception as e:
            return f"Error: {e}"

    def _read(self, path: str) -> str:
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
        path = os.path.expanduser(path)
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Written {len(content):,} chars to {path}"

    def _append(self, path: str, content: str) -> str:
        path = os.path.expanduser(path)
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"Appended {len(content):,} chars to {path}"

    def _list(self, path: str) -> str:
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
        path = os.path.expanduser(path)
        os.makedirs(path, exist_ok=True)
        return f"Directory ready: {path}"

    def _delete(self, path: str) -> str:
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return f"Not found: {path}"
        if os.path.isdir(path):
            shutil.rmtree(path)
            return f"Deleted directory: {path}"
        os.remove(path)
        return f"Deleted file: {path}"

    def _move(self, src: str, dest: str) -> str:
        src  = os.path.expanduser(src)
        dest = os.path.expanduser(dest)
        if not os.path.exists(src):
            return f"Source not found: {src}"
        shutil.move(src, dest)
        return f"Moved: {src} → {dest}"

    def _copy(self, src: str, dest: str) -> str:
        src  = os.path.expanduser(src)
        dest = os.path.expanduser(dest)
        if not os.path.exists(src):
            return f"Source not found: {src}"
        if os.path.isdir(src):
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        return f"Copied: {src} → {dest}"

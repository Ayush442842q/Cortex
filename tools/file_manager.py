from tools import BaseTool
import re


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

        return f"Action '{action}' not yet implemented."

"""
tools/__init__.py — Tool registry and base class

HOW TO ADD A NEW TOOL:
1. Create a new file in the tools/ folder (e.g. tools/my_tool.py)
2. Import BaseTool and create a class that extends it
3. Set: name, description, usage_example
4. Implement: run(self, input: str) -> str
5. That's it. The agent auto-discovers it.

Example:
    from tools import BaseTool

    class MyTool(BaseTool):
        name = "my_tool"
        description = "What this tool does in one sentence"
        usage_example = "example input you would give this tool"

        def run(self, input: str) -> str:
            return "result"
"""

import os
import importlib
import inspect


class BaseTool:
    """
    Every tool must extend this class.
    The agent uses name + description to decide which tool to call.
    """
    name: str = "base_tool"
    description: str = "Base tool — override this"
    usage_example: str = "example usage"

    def run(self, input: str) -> str:
        raise NotImplementedError("Each tool must implement run()")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "usage_example": self.usage_example
        }


def load_all_tools() -> dict[str, BaseTool]:
    """
    Auto-discovers and loads all tools from the tools/ folder.
    Any class that extends BaseTool is automatically registered.
    Returns a dict: { tool_name: tool_instance }
    """
    tools = {}
    tools_dir = os.path.dirname(__file__)

    for filename in sorted(os.listdir(tools_dir)):
        if filename.startswith("_") or not filename.endswith(".py"):
            continue

        module_name = f"tools.{filename[:-3]}"
        try:
            module = importlib.import_module(module_name)
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if (
                    issubclass(obj, BaseTool)
                    and obj is not BaseTool
                    and obj.name != "base_tool"
                ):
                    instance = obj()
                    tools[instance.name] = instance
        except Exception as e:
            print(f"[!] Could not load tool from {filename}: {e}")

    return tools

"""
tools/respond.py — Built-in tool: plain conversation / final answer

This is the agent's fallback tool.
When no other tool is needed, the agent uses this to just talk to the user.
"""

from tools import BaseTool


class RespondTool(BaseTool):
    name = "respond"
    description = (
        "Use this when the task is complete, when you need to answer a question "
        "directly, or when no other tool is needed. Just talk to the user."
    )
    usage_example = "Your task is complete. Here is what I did..."

    def run(self, input: str) -> str:
        # The agent passes its final message as input — just return it
        return input

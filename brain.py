"""
brain.py — The agent's reasoning core powered by Groq

This is the "thinking" part of the agent.
It receives the user's goal + available tools + history,
and decides: which tool to use next and what input to give it.
"""

import json
from groq import Groq


class Brain:
    def __init__(self, api_key: str, model: str, tools: dict, show_thinking: bool = True):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.tools = tools
        self.show_thinking = show_thinking

    def _build_system_prompt(self) -> str:
        tool_descriptions = "\n".join(
            f'- "{t.name}": {t.description}\n  Example input: "{t.usage_example}"'
            for t in self.tools.values()
        )

        return f"""You are a smart, autonomous AI agent running in a terminal.

Your job is to complete the user's task step by step using the available tools.

AVAILABLE TOOLS:
{tool_descriptions}

HOW TO RESPOND:
You must ALWAYS respond with a single valid JSON object — nothing else.
No explanation before or after. Just the JSON.

Format:
{{
    "thinking": "your brief reasoning about what to do next",
    "tool": "tool_name",
    "input": "the exact input to pass to the tool"
}}

RULES:
- Choose the BEST tool for the current step
- "input" should be a clear, specific instruction for that tool
- When the task is fully done, use the "respond" tool with a final summary
- If you are unsure or the task is conversational, use the "respond" tool
- Never make up tools that don't exist in the list above
- Be concise in "thinking" — one or two sentences max
"""

    def decide(self, goal: str, history: list) -> dict:
        """
        Given the goal and conversation history,
        returns: { "thinking": str, "tool": str, "input": str }
        """
        messages = [
            {"role": "system", "content": self._build_system_prompt()}
        ]

        # Add conversation history
        for entry in history:
            messages.append({"role": "user", "content": entry["user"]})
            if "assistant" in entry:
                messages.append({"role": "assistant", "content": entry["assistant"]})

        # Add current goal as the latest user message
        messages.append({"role": "user", "content": f"Task: {goal}"})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
                max_tokens=1024,
            )
            raw = response.choices[0].message.content.strip()

            # Strip markdown fences if model adds them
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            raw = raw.strip()

            parsed = json.loads(raw)

            # Validate required keys
            if not all(k in parsed for k in ("tool", "input")):
                raise ValueError("Missing required keys in response")

            if "thinking" not in parsed:
                parsed["thinking"] = ""

            # Validate tool exists
            if parsed["tool"] not in self.tools:
                parsed["tool"] = "respond"
                parsed["input"] = f"I tried to use an unknown tool. Here is what I was going to do: {parsed['input']}"

            return parsed

        except json.JSONDecodeError:
            return {
                "thinking": "Failed to parse my own response. Falling back to respond.",
                "tool": "respond",
                "input": "I encountered an internal error. Please rephrase your task."
            }
        except Exception as e:
            return {
                "thinking": f"Error: {e}",
                "tool": "respond",
                "input": f"Something went wrong: {e}"
            }

# Contributing a Tool to AgentBase

Adding a tool is intentionally simple. Here's everything you need to know.

---

## Minimum Template

```python
# tools/your_tool_name.py

from tools import BaseTool

class YourToolName(BaseTool):
    name = "your_tool_name"           # snake_case, unique
    description = "One clear sentence about what this tool does and when to use it."
    usage_example = "a typical input the agent would pass to this tool"

    def run(self, input: str) -> str:
        # Your logic here
        result = do_something(input)
        return str(result)
```

Drop the file in `tools/`. Restart the agent. Done.

---

## Rules

- `name` must be unique across all tools (snake_case)
- `description` is what the AI reads to decide whether to use your tool — make it clear and specific
- `run()` always receives a `str` and must return a `str`
- Handle your own exceptions inside `run()` — return an error string, don't raise
- Keep each tool focused on ONE thing

---

## Good Description Examples

✅ `"Runs a Python code snippet and returns the output or error message"`  
✅ `"Creates, reads, moves, or deletes files and folders on the local system"`  
✅ `"Searches the web and returns a summary of the top results"`  

❌ `"Does stuff with files"` — too vague  
❌ `"A tool"` — useless  

---

## Example: A Simple Calculator Tool

```python
# tools/calculator.py

from tools import BaseTool

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Evaluates a math expression and returns the result. Use for arithmetic, unit conversion, or numeric calculations."
    usage_example = "2 ** 10 + 500 / 4"

    def run(self, input: str) -> str:
        try:
            result = eval(input, {"__builtins__": {}})
            return f"Result: {result}"
        except Exception as e:
            return f"Error evaluating expression: {e}"
```

---

## Checklist Before Submitting

- [ ] File is in `tools/` folder
- [ ] Class extends `BaseTool`
- [ ] `name`, `description`, `usage_example` are all set
- [ ] `run()` handles exceptions internally
- [ ] Tested locally — agent can actually use it

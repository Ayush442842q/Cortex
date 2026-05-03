# Contributing to Cortex

Thanks for helping improve Cortex. The project is designed to stay approachable: small files, focused tools, and clear behavior are preferred over clever abstractions.

## Local Setup

```bash
python -m venv .venv
pip install -r requirements.txt
pip install -e ".[dev]"
```

## Before Opening a Pull Request

Run:

```bash
python -m py_compile main.py agent.py brain.py config.py tools/*.py
pytest
```

If you are using PowerShell and `*.py` is not expanded:

```powershell
python -c "import py_compile, pathlib; [py_compile.compile(str(p), doraise=True) for p in [*pathlib.Path('.').glob('*.py'), *pathlib.Path('tools').glob('*.py')]]"
pytest
```

## Adding a Tool

1. Add one file under `tools/`.
2. Subclass `BaseTool`.
3. Set `name`, `description`, and `usage_example`.
4. Implement `run(self, input: str) -> str`.
5. Catch exceptions inside `run()` and return a useful error string.

Template:

```python
from tools import BaseTool


class ExampleTool(BaseTool):
    name = "example"
    description = "Explain what this tool does and when the agent should use it."
    usage_example = "example input"

    def run(self, input: str) -> str:
        try:
            return "result"
        except Exception as exc:
            return f"[example] ERROR: {exc}"
```

## Tool Guidelines

- Keep each tool focused on one job.
- Use `snake_case` names and make them unique.
- Prefer structured input with JSON when the command has multiple parameters.
- Keep network calls timeout-bound.
- Avoid surprising side effects.
- Never print or commit secrets.
- Make descriptions specific; the model uses them to choose tools.

## Pull Request Guidelines

- Keep changes scoped.
- Include a short explanation of user impact.
- Mention any new dependencies.
- Add or update tests when changing tool loading, parsing, or safety behavior.

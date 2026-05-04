# Cortex

Cortex is an extensible, terminal-based AI agent powered by Groq. It uses a simple ReAct loop: the model chooses a tool, the tool runs locally, Cortex observes the result, and the loop continues until the task is complete.

The project is intentionally small and hackable. Add a Python file under `tools/`, subclass `BaseTool`, restart the CLI, and the new capability is available to the agent.

## Features

- Groq-powered reasoning loop with strict JSON tool decisions
- Auto-discovered local tools
- Rich terminal interface
- Session history with reset support
- Tools for files, shell commands, code execution, Git, web search, data formatting, notes, memory, scheduling, networking, and system inspection
- Standard library first, with optional runtime dependencies for image and system tools

## Quick Start

```bash
git clone https://github.com/Ayush442842q/Cortex.git
cd Cortex
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

macOS or Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Configuration

Cortex needs a Groq API key.

Recommended:

```bash
export GROQ_API_KEY=gsk_your_key_here
```

Windows CMD:

```cmd
set GROQ_API_KEY=gsk_your_key_here
```

You can also let Cortex create a local `config.json` on first run. That file is ignored by Git.

Default settings:

```json
{
  "api_key": "API_KEY_HERE",
  "model": "llama-3.3-70b-versatile",
  "theme": "monokai",
  "max_iterations": 10,
  "timeout_seconds": 30,
  "show_thinking": true
}
```

## Web Intake Frontend

This repo also includes a dark Vercel-ready intake page in `public/`.
Visitors submit the form at the public site, and the private API route at
`api/telegram.js` sends the request to Telegram.

Telegram bots cannot send a message to a raw phone number. Create a bot with
BotFather, open the bot from the Telegram account that should receive requests,
send `/start`, then use that chat ID for delivery.

Required Vercel environment variables:

```bash
TELEGRAM_BOT_TOKEN=bot_token_from_botfather
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

Local development with Vercel CLI:

```powershell
$env:TELEGRAM_BOT_TOKEN="bot_token_from_botfather"
$env:TELEGRAM_CHAT_ID="your_telegram_chat_id"
vercel dev
```

Production setup:

```bash
vercel env add TELEGRAM_BOT_TOKEN production
vercel env add TELEGRAM_CHAT_ID production
vercel --prod
```

## CLI Commands

| Command | Description |
| --- | --- |
| `tools` | List loaded tools |
| `clear` / `reset` | Clear session memory |
| `help` | Show command help |
| `exit` | Quit |
| anything else | Send a task to the agent |

## Available Tools

Cortex currently includes tools for:

- local file operations
- terminal commands
- Python code execution
- Python environment setup
- web search and URL fetches
- Git operations
- direct Groq model calls
- prompt templates
- TF-IDF document search
- persistent key-value memory
- task planning
- clipboard snippets
- markdown notes
- calculations and statistics
- system monitoring
- JSON and CSV parsing/formatting
- email sending through SMTP
- image processing
- encrypted password storage
- REST API calls
- task scheduling
- DNS lookup
- process management
- Python linting
- TCP port scanning
- translation
- disk usage analysis
- regex testing
- checksums and digest verification
- zip archive creation and extraction
- date/time conversion and arithmetic
- project tree inspection
- text encoding and decoding
- URL parsing and query editing
- secure random values and UUIDs
- Markdown table-of-contents and link inspection
- read-only SQLite database inspection
- `.env` file inspection and editing
- text and file diffs
- log summaries and error extraction
- final conversational responses

Run `python -c "from tools import load_all_tools; print(sorted(load_all_tools()))"` to see what loads in your environment.

## How It Works

```text
User task
  -> Brain builds a prompt from the available tools
  -> Groq returns a JSON decision
  -> Agent runs the selected tool
  -> Tool result is added to history
  -> Loop repeats until the respond tool is selected
```

The model must return:

```json
{
  "thinking": "brief reasoning",
  "tool": "tool_name",
  "input": "exact tool input"
}
```

## Add a Tool

Create `tools/my_tool.py`:

```python
from tools import BaseTool


class MyTool(BaseTool):
    name = "my_tool"
    description = "One clear sentence about when to use this tool."
    usage_example = "example input"

    def run(self, input: str) -> str:
        try:
            return "result"
        except Exception as exc:
            return f"[my_tool] ERROR: {exc}"
```

Restart Cortex. The loader discovers the tool automatically.

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run checks:

```bash
python -m py_compile main.py agent.py brain.py config.py tools/*.py
pytest
```

On Windows PowerShell, if shell globbing does not expand for `py_compile`, use:

```powershell
python -c "import py_compile, pathlib; [py_compile.compile(str(p), doraise=True) for p in [*pathlib.Path('.').glob('*.py'), *pathlib.Path('tools').glob('*.py')]]"
pytest
```

## Safety Notes

Cortex runs local tools with real side effects. Some tools can write files, execute shell commands, call network APIs, send email, install packages, kill processes, or modify Git repositories. Run it in an environment you trust, review tool behavior before exposing it to other users, and keep secrets out of prompts and logs.

## License

MIT. See [LICENSE](LICENSE).

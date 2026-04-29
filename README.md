# 🤖 Cortex
An extensible, terminal-based AI agent powered by **[Groq](https://console.groq.com/)**.
Built to grow — one tool every week. **21 tools and counting.**

---

## ⚡ Quick Start

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Get your free Groq API key
* Visit: **[https://console.groq.com](https://console.groq.com/)**
* Sign up → API Keys → Create Key

### 3. Set your API key
```
# Option A: Environment variable (recommended)
export GROQ_API_KEY=gsk_your_key_here   # Mac/Linux
set GROQ_API_KEY=gsk_your_key_here      # Windows CMD

# Option B: Add to config.json (the app will prompt you on first run)
```

### 4. Run
```
python main.py
```

---

## 🎮 Commands
| Command | What it does |
|---|---|
| `tools` | List all loaded tools |
| `clear` | Clear conversation memory |
| `help` | Show help menu |
| `exit` | Quit |
| *anything else* | Sent to the agent as a task |

---

## 🏗️ Project Structure
```
Cortex/
│
├── main.py              # Entry point — CLI interface
├── agent.py             # Main agent loop (Think → Act → Observe)
├── brain.py             # Groq LLM reasoning core
├── config.py            # Config loading and API key management
├── config.json          # Your settings (gitignored)
├── requirements.txt
│
└── tools/
    ├── __init__.py         # BaseTool + auto-discovery
    ├── respond.py                  # Base: Built-in conversation fallback
    ├── code_writer.py              # Week  1: Write & run Python code
    ├── file_manager.py             # Week  2: File & folder operations
    ├── terminal.py                 # Week  3: Run shell commands
    ├── env_setup.py                # Week  4: Dev environment setup
    ├── web_search.py               # Week  5: DuckDuckGo search (no API key)
    ├── git_tool.py                 # Week  6: Git version control
    ├── llm_switcher.py             # Week  7: Query different LLM providers
    ├── prompt_manager.py           # Week  8: Save & reuse prompt templates
    ├── embedding_search.py         # Week  9: TF-IDF document search
    ├── memory_store.py             # Week  9: Persistent key-value memory
    ├── task_planner.py             # Week 10: Break goals into subtasks
    ├── clipboard.py                # Week 11: Copy/paste/store text snippets
    ├── note_taker.py               # Week 12: Create & search markdown notes
    ├── calculator.py               # Week 13: Math, units & expressions
    ├── system_monitor.py           # Week 14: CPU, RAM, disk & battery stats
    ├── data_tool.py                # Week 15: Parse, filter & convert data
    ├── email_sender.py             # Week 16: Send emails via SMTP
    ├── image_tool.py               # Week 17: Resize, convert & compress images
    ├── password_manager.py         # Week 18: Generate & store encrypted passwords
    ├── api_caller.py               # Week 19: HTTP GET/POST to any REST API
    └── scheduler.py                # Week 20: Schedule tasks at a specific time
```

---

## 🧰 How to Add a New Tool

1. Create a file in `tools/` — e.g. `tools/my_tool.py`
2. Extend `BaseTool` and implement `run()`

```python
from tools import BaseTool

class MyTool(BaseTool):
    name = "my_tool"
    description = "What this tool does in one sentence"
    usage_example = "example of what input this tool receives"

    def run(self, input: str) -> str:
        # Your logic here
        return "result"
```

3. Restart the agent. **That's it.** The tool is auto-discovered.

---

## 🗺️ Roadmap
| Release | Tool | Capability |
|---|---|---|
| **Base** ✅ | Core loop | Think, plan, respond |
| Week  1 ✅ | Code Writer | Write & run Python code |
| Week  2 ✅ | File Manager | File & folder operations |
| Week  3 ✅ | Terminal Tool | Run shell commands |
| Week  4 ✅ | Environment Setup | Dev environment setup |
| Week  5 ✅ | Web Search | DuckDuckGo search (no API key) |
| Week  6 ✅ | Git Tool | Git version control |
| Week  7 ✅ | LLM Switcher | Query different LLM providers |
| Week  8 ✅ | Prompt Manager | Save & reuse prompt templates |
| Week  9 ✅ | Embedding Search | TF-IDF document search |
| Week  9 ✅ | Memory Store | Persistent key-value memory |
| Week 10 ✅ | Task Planner | Break goals into subtasks |
| Week 11 ✅ | Clipboard Manager | Copy/paste/store text snippets |
| Week 12 ✅ | Note Taker | Create & search markdown notes |
| Week 13 ✅ | Calculator | Math, units & expressions |
| Week 14 ✅ | System Monitor | CPU, RAM, disk & battery stats |
| Week 15 ✅ | JSON/CSV Tool | Parse, filter & convert data |
| Week 16 ✅ | Email Sender | Send emails via SMTP |
| Week 17 ✅ | Image Tool | Resize, convert & compress images |
| Week 18 ✅ | Password Manager | Generate & store encrypted passwords |
| Week 19 ✅ | API Caller | HTTP GET/POST to any REST API |
| Week 20 ✅ | Scheduler | Schedule tasks at a specific time |

---

## ⚙️ Configuration (`config.json`)
| Key | Default | Description |
|---|---|---|
| `api_key` | `""` | Your Groq API key |
| `model` | `llama-3.3-70b-versatile` | Groq model to use |
| `show_thinking` | `true` | Show agent reasoning |
| `max_iterations` | `10` | Max steps per task |
| `timeout_seconds` | `30` | Tool execution timeout |
| `theme` | `monokai` | Syntax highlight theme |

---

## 🧠 How It Works
```
You type a task
      ↓
Brain (Groq LLM) reads the task + available tools
      ↓
Brain decides: which tool? what input?
      ↓
Tool runs → returns result
      ↓
Brain sees result → decides next step
      ↓
Repeats until task is done
      ↓
"respond" tool → final answer shown to you
```

---

## 📄 License
MIT — use it, fork it, build on it.

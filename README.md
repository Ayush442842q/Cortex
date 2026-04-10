# 🤖 AgentBase

An extensible, terminal-based AI agent powered by [Groq](https://console.groq.com).

Built to grow — one tool every week.

---

## ⚡ Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get your free Groq API key
- Visit: https://console.groq.com
- Sign up → API Keys → Create Key

### 3. Set your API key
```bash
# Option A: Environment variable (recommended)
export GROQ_API_KEY=gsk_your_key_here   # Mac/Linux
set GROQ_API_KEY=gsk_your_key_here      # Windows CMD

# Option B: Add to config.json (the app will ask you first run)
```

### 4. Run
```bash
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
AgentBase/
│
├── main.py          # Entry point — CLI interface
├── agent.py         # Main agent loop (Think → Act → Observe)
├── brain.py         # Groq LLM reasoning core
├── config.py        # Config loading and API key management
├── config.json      # Your settings (gitignored)
├── requirements.txt
│
└── tools/
    ├── __init__.py  # BaseTool class + auto-discovery
    └── respond.py   # Built-in: plain conversation tool
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
| Week 1 | Code Writer | Write & run code |
| Week 2 | File Manager | Files & folders |
| Week 3 | Terminal Tool | Shell commands |
| Week 4 | Environment Setup | Dev environment setup |
| Week 5 | Web Search | Browse the web |
| Week 6 | Git Tool | Version control |
| ... | ... | ... |

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

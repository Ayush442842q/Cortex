"""
Cortex — Embedding Search Tool (Week 9)
Index and search text documents using TF-IDF (pure Python, no API needed).
Index stored in ~/.cortex/embeddings/
"""
from __future__ import annotations
import sys, json, math, re
from pathlib import Path
from collections import Counter

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name: str = ""
        description: str = ""
        usage_example: str = ""
        def run(self, user_input: str) -> str:
            raise NotImplementedError

INDEX_DIR = Path.home() / ".cortex" / "embeddings"
INDEX_FILE = INDEX_DIR / "index.json"
INDEX_DIR.mkdir(parents=True, exist_ok=True)

def _load_index():
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    return {"docs": {}}

def _save_index(idx):
    INDEX_FILE.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")

def _tokenize(text): return re.findall(r"[a-z0-9]+", text.lower())
def _tf(tokens):
    c = Counter(tokens); total = len(tokens) or 1
    return {w: count / total for w, count in c.items()}
def _idf(word, docs):
    n = len(docs); df = sum(1 for d in docs.values() if word in d["tf"])
    return math.log((n + 1) / (df + 1)) + 1
def _score(q_tokens, doc, docs):
    return sum(doc["tf"].get(w, 0.0) * _idf(w, docs) for w in q_tokens)

class EmbeddingSearchTool(BaseTool):
    name = "search"
    description = (
        "Index and search documents (TF-IDF).\n"
        "  search add <id> | <text>  -- index a doc\n"
        "  search query <text>       -- find matches\n"
        "  search list               -- show index\n"
        "  search remove <id>        -- remove a doc\n"
        "  search clear              -- clear index"
    )
    usage_example = "search query how to use decorators in Python"
    TOP_K = 3

    def run(self, user_input: str) -> str:
        user_input = user_input.strip()
        if not user_input:
            return "[search] Commands: add | query | list | remove | clear"
        parts = user_input.split(None, 1)
        cmd, rest = parts[0].lower(), (parts[1].strip() if len(parts) > 1 else "")
        idx = _load_index()

        if cmd == "add":
            if "|" not in rest:
                return "[search] add: use 'add <id> | <text>'"
            doc_id, text = rest.split("|", 1)
            doc_id, text = doc_id.strip(), text.strip()
            if not doc_id or not text: return "[search] ID and text required."
            tokens = _tokenize(text)
            idx["docs"][doc_id] = {"title": doc_id, "text": text[:500], "tf": _tf(tokens)}
            _save_index(idx)
            return f"[search] Indexed '{doc_id}' ({len(tokens)} tokens)."

        elif cmd == "query":
            query = rest
            if not query: return "[search] Provide a query."
            docs = idx["docs"]
            if not docs: return "[search] Index empty. Add docs first."
            q_tokens = _tokenize(query)
            scored = sorted([(d, _score(q_tokens, docs[d], docs)) for d in docs], key=lambda x: -x[1])
            lines = [f"[Search: {query}]"]
            for rank, (doc_id, score) in enumerate(scored[:self.TOP_K], 1):
                lines.append(f"\n{rank}. {doc_id}  (score: {score:.4f})")
                lines.append(f"   {docs[doc_id]['text'][:150]}...")
            return "\n".join(lines)

        elif cmd == "list":
            docs = idx["docs"]
            if not docs: return "[search] Index is empty."
            return "[Indexed docs]\n" + "\n".join(f"  {k}: {v['text'][:60]}..." for k, v in docs.items())

        elif cmd == "remove":
            if rest not in idx["docs"]: return f"[search] '{rest}' not found."
            del idx["docs"][rest]; _save_index(idx)
            return f"[search] Removed '{rest}'."

        elif cmd == "clear":
            _save_index({"docs": {}}); return "[search] Index cleared."

        else:
            # treat as query
            return self.run("query " + user_input)
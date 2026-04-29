"""Cortex — Text Summarizer Tool (Week 22) [AI & Automation]
Summarize, extract keywords, count words, and analyze readability of any text.
"""
from __future__ import annotations
import re, math
from collections import Counter
try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=description=usage_example=""
        def run(self,i): raise NotImplementedError

def _sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+",text) if len(s.strip())>10]

def _words(text):
    return re.findall(r"[a-z]+",text.lower())

def _stopwords():
    return set("a an the is are was were be been being have has had do does did will would could should may might shall can i you he she it we they and but or nor for yet so of in on at to by as with from that this these those".split())

def _tfidf_summary(text, n=3):
    sents=_sentences(text)
    if not sents: return text[:300]
    stop=_stopwords()
    word_freq=Counter(w for w in _words(text) if w not in stop)
    total=sum(word_freq.values()) or 1
    scores=[]
    for s in sents:
        ws=[w for w in _words(s) if w not in stop]
        score=sum(word_freq[w]/total for w in ws)/(len(ws) or 1)
        scores.append((score,s))
    scores.sort(reverse=True)
    return " ".join(s for _,s in scores[:n])

class TextSummarizerTool(BaseTool):
    name="summarize"
    description="Analyze text. Commands: summarize <text> | keywords <text> | stats <text> | readability <text>"
    usage_example="summarize Python is a programming language..."

    def run(self, inp: str) -> str:
        inp=inp.strip()
        if not inp: return "[summarize] Commands: summarize | keywords | stats | readability"
        parts=inp.split(None,1); cmd=parts[0].lower(); text=parts[1].strip() if len(parts)>1 else ""
        if not text: text=inp; cmd="summarize"
        if cmd=="summarize":
            summary=_tfidf_summary(text,3)
            return f"[Summary]\n{summary}"
        elif cmd=="keywords":
            stop=_stopwords()
            words=[w for w in _words(text) if w not in stop and len(w)>3]
            top=Counter(words).most_common(10)
            return "[Keywords]\n"+", ".join(f"{w}({c})" for w,c in top)
        elif cmd=="stats":
            ws=_words(text); sents=_sentences(text)
            return (f"[Text Stats]\n"
                    f"  Words     : {len(ws)}\n"
                    f"  Sentences : {len(sents)}\n"
                    f"  Chars     : {len(text)}\n"
                    f"  Avg word  : {sum(len(w) for w in ws)/(len(ws) or 1):.1f} chars\n"
                    f"  Avg sent  : {len(ws)/(len(sents) or 1):.1f} words")
        elif cmd=="readability":
            ws=_words(text); sents=_sentences(text)
            asl=len(ws)/(len(sents) or 1)
            asw=sum(1+(len(w)-1)//3 for w in ws)/(len(ws) or 1)
            fre=max(0,min(100,206.835-1.015*asl-84.6*asw))
            grade="Very Easy" if fre>90 else "Easy" if fre>80 else "Fairly Easy" if fre>70 else "Standard" if fre>60 else "Fairly Difficult" if fre>50 else "Difficult"
            return f"[Readability]\n  Flesch score: {fre:.1f} / 100\n  Level: {grade}"
        return f"[summarize] Unknown command: {cmd}"

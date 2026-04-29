"""Cortex — Translation Tool (Week 27) [AI & Automation]
Detect language and translate text using MyMemory free API (no key needed).
"""
from __future__ import annotations
import urllib.request, urllib.parse, json, re
try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=description=usage_example=""
        def run(self,i): raise NotImplementedError

LANGS={"english":"en","spanish":"es","french":"fr","german":"de","italian":"it",
       "portuguese":"pt","russian":"ru","chinese":"zh","japanese":"ja","arabic":"ar",
       "hindi":"hi","korean":"ko","dutch":"nl","turkish":"tr","polish":"pl"}

def _translate(text, lang_to, lang_from="autodetect"):
    lp=f"{lang_from}|{lang_to}"
    url="https://api.mymemory.translated.net/get?q={}&langpair={}".format(
        urllib.parse.quote(text[:500]),urllib.parse.quote(lp))
    req=urllib.request.Request(url,headers={"User-Agent":"Cortex/1.0"})
    with urllib.request.urlopen(req,timeout=10) as r:
        data=json.loads(r.read())
    tm=data.get("responseData",{})
    return tm.get("translatedText",""), tm.get("detectedLanguage","?")

class TranslationTool(BaseTool):
    name="translate"
    description="Translate text. Commands: translate <lang> | <text>   or   translate list"
    usage_example="translate spanish | Hello, how are you?"

    def run(self, inp: str) -> str:
        inp=inp.strip()
        if not inp: return "[translate] Usage: translate <language> | <text>"
        if inp.lower() in ("list","langs"):
            return "[Languages]\n"+", ".join(sorted(LANGS))
        if "|" not in inp:
            return "[translate] Use: translate <language> | <text>"
        header,text=inp.split("|",1)
        lang_name=header.strip().lower(); text=text.strip()
        if not text: return "[translate] Text is empty after '|'"
        lang_code=LANGS.get(lang_name)
        if not lang_code:
            if len(lang_name)==2: lang_code=lang_name
            else: return f"[translate] Unknown language: {lang_name}. Use 'translate list'"
        try:
            result,detected=_translate(text,lang_code)
            return f"[translate -> {lang_name}]\n{result}\n(detected source: {detected})"
        except Exception as e:
            return f"[translate] Error: {e}"

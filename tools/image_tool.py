"""Cortex — Image Tool (Week 17)
Resize, convert, compress, rotate and get info about images via Pillow.
"""
from __future__ import annotations
import os, json, sys, subprocess

try:
    from PIL import Image
    _OK=True
except ImportError:
    _OK=False

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=""; description=""; usage_example=""
        def run(self,u:str)->str: ...

def _ensure():
    if _OK: return None
    r=subprocess.run([sys.executable,"-m","pip","install","Pillow","-q"],capture_output=True,text=True)
    if r.returncode!=0: return f"pip install Pillow failed: {r.stderr.strip()}"
    global Image,_OK
    from PIL import Image as _I; Image=_I; _OK=True; return None

def _parse(r):
    r=r.strip()
    if r.startswith("{"): 
        try: return json.loads(r)
        except: pass
    return {"action":"info","path":r}

class ImageTool(BaseTool):
    name="image"
    description="Process images. Actions: info, resize, convert, compress, rotate, thumbnail. Input JSON with action, path, and action-specific params."
    usage_example='image({"action":"info","path":"photo.jpg"})' 
    def run(self,u:str)->str:
        err=_ensure()
        if err: return f"[image] ERROR: {err}"
        p=_parse(u); action=p.get("action","info"); path=p.get("path","")
        if not path: return "[image] ERROR: path required."
        if not os.path.exists(path) and action!="convert": return f"[image] File not found: {path}"
        try:
            if action=="info":
                img=Image.open(path)
                return (f"File:   {os.path.basename(path)}\n"
                        f"Size:   {img.width}x{img.height} px\n"
                        f"Mode:   {img.mode}\n"
                        f"Format: {img.format}\n"
                        f"Bytes:  {os.path.getsize(path):,}")
            elif action=="resize":
                w,h=int(p.get("width",0)),int(p.get("height",0))
                if not w and not h: return "[image] ERROR: width or height required."
                img=Image.open(path)
                if not w: w=int(img.width*(h/img.height))
                if not h: h=int(img.height*(w/img.width))
                out=p.get("output",path)
                img.resize((w,h),Image.LANCZOS).save(out)
                return f"Resized to {w}x{h} → {out}"
            elif action=="convert":
                out=p.get("output","")
                if not out: return "[image] ERROR: output path required."
                Image.open(path).save(out)
                return f"Converted → {out}"
            elif action=="compress":
                q=int(p.get("quality",75)); out=p.get("output",path)
                img=Image.open(path)
                if img.mode in("RGBA","P"): img=img.convert("RGB")
                img.save(out,optimize=True,quality=q)
                return f"Compressed (quality={q}) → {out}"
            elif action=="rotate":
                deg=float(p.get("degrees",90)); out=p.get("output",path)
                Image.open(path).rotate(deg,expand=True).save(out)
                return f"Rotated {deg}° → {out}"
            elif action=="thumbnail":
                size=int(p.get("size",128)); out=p.get("output",path)
                img=Image.open(path); img.thumbnail((size,size))
                img.save(out); return f"Thumbnail {size}px → {out}"
            return f"Unknown action: {action}"
        except Exception as e:
            return f"[image] ERROR: {e}"

if __name__=="__main__":
    t=ImageTool()
    print(t.run('{"action":"info","path":"nonexistent.jpg"}'))
    print("All tests passed.")

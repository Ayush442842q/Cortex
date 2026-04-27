"""Cortex — Calculator (Week 13)
Evaluate math expressions, unit conversions, and basic stats.
"""
from __future__ import annotations
import math, json, re

try:
    from tools import BaseTool
except ImportError:
    class BaseTool:
        name=""; description=""; usage_example=""
        def run(self,u:str)->str: ...

UNITS = {
    "km_to_miles":0.621371,"miles_to_km":1.60934,
    "kg_to_lb":2.20462,"lb_to_kg":0.453592,
    "c_to_f":None,"f_to_c":None,
    "m_to_ft":3.28084,"ft_to_m":0.3048,
    "l_to_gal":0.264172,"gal_to_l":3.78541,
}

SAFE_NAMES = {k:v for k,v in vars(math).items() if not k.startswith("_")}
SAFE_NAMES.update({"abs":abs,"round":round,"min":min,"max":max,"sum":sum,"pow":pow})

def _parse(r):
    r=r.strip()
    if r.startswith("{"): 
        try: return json.loads(r)
        except: pass
    return {"action":"eval","expression":r}

class CalculatorTool(BaseTool):
    name="calculator"
    description="Math expressions, unit conversions, stats. Input: expression string or JSON with action (eval|convert|stats)."
    usage_example='calculator("2 ** 10 + sqrt(144)")' 
    def run(self,u:str)->str:
        p=_parse(u); action=p.get("action","eval")
        try:
            if action=="eval":
                expr=p.get("expression","").strip()
                if not expr: return "[calculator] ERROR: empty expression."
                result=eval(expr, {"__builtins__":{}}, SAFE_NAMES)
                return f"{expr} = {result}"
            elif action=="convert":
                value=float(p.get("value",0)); conv=p.get("conversion","").lower().replace(" ","_")
                if conv=="c_to_f": return f"{value}°C = {value*9/5+32:.4f}°F"
                if conv=="f_to_c": return f"{value}°F = {(value-32)*5/9:.4f}°C"
                factor=UNITS.get(conv)
                if factor is None: return f"[calculator] Unknown conversion: {conv}. Available: {list(UNITS.keys())}"
                return f"{value} → {value*factor:.6f}  ({conv.replace('_',' ')})"
            elif action=="stats":
                nums=p.get("numbers",[])
                if not nums: return "[calculator] ERROR: numbers list required."
                nums=[float(x) for x in nums]
                n=len(nums); s=sum(nums); mean=s/n
                nums_s=sorted(nums)
                median=nums_s[n//2] if n%2 else (nums_s[n//2-1]+nums_s[n//2])/2
                variance=sum((x-mean)**2 for x in nums)/n
                return (f"Count:  {n}\nSum:    {s}\nMean:   {mean:.4f}\n"
                        f"Median: {median:.4f}\nMin:    {min(nums)}\nMax:    {max(nums)}\n"
                        f"Std Dev:{math.sqrt(variance):.4f}")
            return f"Unknown action: {action}"
        except Exception as e:
            return f"[calculator] ERROR: {e}"

if __name__=="__main__":
    t=CalculatorTool()
    print(t.run("2 ** 10"))
    print(t.run('{"action":"convert","value":100,"conversion":"km_to_miles"}'))
    print(t.run('{"action":"stats","numbers":[1,2,3,4,5]}'))
    print("All tests passed.")

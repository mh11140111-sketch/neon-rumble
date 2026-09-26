from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

# Remove the v3.48 jail overlay that was injected into the wrong runtime loop.
pat=re.compile(r"/\* JAIL BARS v3\.48 \*/if\(\(f\.jailedUntil\|\|0\)>this\.time\)\{ctx\.save\(\);const rr=Math\.max\(20,f\.radius\*1\.25\);ctx\.lineWidth=Math\.max\(3,rr\*\.08\);ctx\.strokeStyle='rgba\(190,205,220,\.95\)';ctx\.fillStyle='rgba\(20,28,38,\.22\)';ctx\.fillRect\(f\.x-rr,f\.y-rr,f\.x\+rr-\(f\.x-rr\),rr\*2\);ctx\.strokeRect\(f\.x-rr,f\.y-rr,rr\*2,rr\*2\);for\(let bx=-\.66;bx<=\.66;bx\+=\.33\)\{ctx\.beginPath\(\);ctx\.moveTo\(f\.x\+rr\*bx,f\.y-rr\);ctx\.lineTo\(f\.x\+rr\*bx,f\.y\+rr\);ctx\.stroke\(\);\}ctx\.restore\(\);\}")
s,n=pat.subn('',s,count=1)
if n!=1:
    raise SystemExit('Broken jail overlay marker not found exactly once')

# Correct the detective call grouping so only Detective runs detectiveSkill.
s=s.replace("if(f.id==='detective')this.detectiveJailSkill(f);this.detectiveSkill(f,e);",
            "if(f.id==='detective'){this.detectiveJailSkill(f);this.detectiveSkill(f,e);}",1)

# Safer jail pool: always use the engine fighters array and bail if unavailable.
s=s.replace("const pool=this.fighters||this.units||[];",
            "const pool=Array.isArray(this.fighters)?this.fighters:[];",1)

# Add lightweight jail bars in the page-level draw() function, after fighters are drawn.
# Locate the global draw() body and inject before its closing area via the common fighters rendering loop.
draw_idx=s.find('function draw(){')
if draw_idx<0:
    raise SystemExit('global draw() not found')

# Find a fighters loop inside draw; inject overlay at the start of that loop where page canvas context exists.
segment=s[draw_idx:]
m=re.search(r"for\(const f of engine\.fighters\)\{",segment)
if not m:
    raise SystemExit('engine.fighters draw loop not found')
insert_at=draw_idx+m.end()
overlay="""if((f.jailedUntil||0)>engine.time){const rr=Math.max(22,f.radius*1.3);c.save();c.fillStyle='rgba(20,28,38,.22)';c.strokeStyle='rgba(205,215,225,.98)';c.lineWidth=Math.max(3,rr*.08);c.fillRect(f.x-rr,f.y-rr,rr*2,rr*2);c.strokeRect(f.x-rr,f.y-rr,rr*2,rr*2);for(let bx=-.66;bx<=.66;bx+=.33){c.beginPath();c.moveTo(f.x+rr*bx,f.y-rr);c.lineTo(f.x+rr*bx,f.y+rr);c.stroke()}c.restore();}"""
s=s[:insert_at]+overlay+s[insert_at:]

# Patch note for hotfix.
marker='<div class="patch-body">'
hotfix='''<div class="patch-version"><h3>v3.48.1 · 탐정 먹통 버그 수정</h3><ul><li>범인 잡기 발동 시 쇠창살 렌더링 코드가 잘못된 루프에서 실행되어 게임이 멈추던 문제 수정.</li><li>감옥 2초 및 이후 확률 판정은 그대로 유지.</li></ul></div>'''
if marker in s and 'v3.48.1 · 탐정 먹통 버그 수정' not in s:
    s=s.replace(marker,marker+hotfix,1)

if s==orig:
    raise SystemExit('No changes applied')

required=["const pool=Array.isArray(this.fighters)?this.fighters:[];","if(f.id==='detective'){this.detectiveJailSkill(f);this.detectiveSkill(f,e);}","v3.48.1 · 탐정 먹통 버그 수정"]
for x in required:
    if x not in s: raise SystemExit('missing '+x)
if '/* JAIL BARS v3.48 */' in s:
    raise SystemExit('old broken overlay still present')

p.write_text(s,encoding='utf-8')
print('v3.48.1 detective freeze fix applied')

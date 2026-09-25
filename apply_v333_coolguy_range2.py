from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = "const a=this.aim(f,e),ang=Math.atan2(a.y,a.x),range=280*f.scale,half=.65;"
new = "const a=this.aim(f,e),ang=Math.atan2(a.y,a.x),range=560*f.scale,half=.65;"
if old not in s:
    raise SystemExit('target coolguy shout range fragment not found')
if s.count(old) != 1:
    raise SystemExit(f'unexpected target count: {s.count(old)}')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
print('Updated Cool Guy shout range 280 -> 560')

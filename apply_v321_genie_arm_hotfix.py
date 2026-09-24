from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="ctx.fillStyle='#f0b51f';ctx.beginPath();ctx.roundRect(f.radius*.62,-18*gs,34*gs,36*gs,9*gs);ctx.fill();ctx.shadowBlur=0;ctx.fillStyle='#258eff';ctx.beginPath();ctx.roundRect(f.radius*.62+28*gs,-21*gs,82*gs,42*gs,21*gs);ctx.fill();"
new="ctx.fillStyle='#f0b51f';ctx.fillRect(f.radius*.62,-18*gs,34*gs,36*gs);ctx.shadowBlur=0;ctx.fillStyle='#258eff';ctx.fillRect(f.radius*.62+28*gs,-21*gs,82*gs,42*gs);"
if old not in s:
    raise SystemExit('PATCH FAILED: genie arm roundRect block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('v3.21 genie arm canvas compatibility hotfix applied')

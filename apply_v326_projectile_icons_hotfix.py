from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""else if(s.kind==='curseorb'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(24*s.radius/8)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🧿',0,0)}else if(s.kind==='taser')"""
new="""else if(s.kind==='curseorb'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(24*s.radius/8)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🧿',0,0)}else if(s.kind==='snow'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(28*s.radius/8)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('❄️',0,0)}else if(s.kind==='thumb'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(28*s.radius/7)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('👎',0,0)}else if(s.kind==='taser')"""
if old not in s:
    raise SystemExit('draw insertion anchor not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('v3.26 projectile icon hotfix applied')

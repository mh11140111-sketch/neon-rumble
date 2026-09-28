from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

bad="""  if(['love_burn','love_heal','love_stun','love_charm'].includes(s.kind)){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(Math.max(26,s.radius*2.8))+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(s.kind==='love_burn'?'❤️‍🔥':s.kind==='love_heal'?'❤️':s.kind==='love_stun'?'💖':'💓',0,0)}else if(['dragon_wind','dragon_thunder','dragon_bubble','dragon_leaf'].includes(s.kind)){"""
if bad not in s:
    raise SystemExit('bad love render block anchor not found')
s=s.replace(bad,"""  if(['dragon_wind','dragon_thunder','dragon_bubble','dragon_leaf'].includes(s.kind)){""",1)

anchor="""for(const s of engine.shots){ctx.save();ctx.translate(s.x,s.y);ctx.rotate(Math.atan2(s.vy,s.vx));if(['dragon_wind','dragon_thunder','dragon_bubble','dragon_leaf'].includes(s.kind)){"""
repl="""for(const s of engine.shots){ctx.save();ctx.translate(s.x,s.y);ctx.rotate(Math.atan2(s.vy,s.vx));if(['love_burn','love_heal','love_stun','love_charm'].includes(s.kind)){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(Math.max(30,s.radius*3.0))+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(s.icon||(s.kind==='love_burn'?'❤️‍🔥':s.kind==='love_heal'?'❤️':s.kind==='love_stun'?'💖':'💓'),0,0)}else if(['dragon_wind','dragon_thunder','dragon_bubble','dragon_leaf'].includes(s.kind)){"""
if anchor not in s:
    raise SystemExit('draw shots anchor not found')
s=s.replace(anchor,repl,1)

# Marker to document the visual-only hotfix without changing visible version.
marker='/* v3.60 loveman heart projectile FX hotfix */'
if marker not in s:
    s=s.replace('/* Add characters to ROSTER and their behavior to stepFighter. No UI changes required. */', '/* Add characters to ROSTER and their behavior to stepFighter. No UI changes required. */\n'+marker,1)

p.write_text(s,encoding='utf-8')
print('patched v3.60 Love Man heart projectile FX')

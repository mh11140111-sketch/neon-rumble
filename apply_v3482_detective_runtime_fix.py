from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

# 1) Remove invalid canvas rendering from Engine update/tick loop.
bad="for(const s of this.shots){if(s.kind==='magnifier'){ctx.save();ctx.font=`${Math.max(16,s.radius*2.6)}px 'Apple Color Emoji','Segoe UI Emoji',sans-serif`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('🔎',s.x,s.y);ctx.restore();continue;}"
good="for(const s of this.shots){"
if bad not in s:
    raise SystemExit('Expected invalid magnifier update-loop renderer not found')
s=s.replace(bad,good,1)

# 2) Fix jail overlay canvas variable in draw() from undefined c -> ctx.
bad_jail="for(const f of engine.fighters){if((f.jailedUntil||0)>engine.time){const rr=Math.max(22,f.radius*1.3);c.save();c.fillStyle='rgba(20,28,38,.22)';c.strokeStyle='rgba(205,215,225,.98)';c.lineWidth=Math.max(3,rr*.08);c.fillRect(f.x-rr,f.y-rr,rr*2,rr*2);c.strokeRect(f.x-rr,f.y-rr,rr*2,rr*2);for(let bx=-.66;bx<=.66;bx+=.33){c.beginPath();c.moveTo(f.x+rr*bx,f.y-rr);c.lineTo(f.x+rr*bx,f.y+rr);c.stroke()}c.restore();}"
good_jail="for(const f of engine.fighters){if((f.jailedUntil||0)>engine.time){const rr=Math.max(22,f.radius*1.3);ctx.save();ctx.fillStyle='rgba(20,28,38,.22)';ctx.strokeStyle='rgba(205,215,225,.98)';ctx.lineWidth=Math.max(3,rr*.08);ctx.fillRect(f.x-rr,f.y-rr,rr*2,rr*2);ctx.strokeRect(f.x-rr,f.y-rr,rr*2,rr*2);for(let bx=-.66;bx<=.66;bx+=.33){ctx.beginPath();ctx.moveTo(f.x+rr*bx,f.y-rr);ctx.lineTo(f.x+rr*bx,f.y+rr);ctx.stroke()}ctx.restore();}"
if bad_jail not in s:
    raise SystemExit('Expected invalid jail renderer not found')
s=s.replace(bad_jail,good_jail,1)

# 3) Render magnifier in the actual draw() projectile renderer.
needle="for(const s of engine.shots){ctx.save();ctx.translate(s.x,s.y);ctx.rotate(Math.atan2(s.vy,s.vx));if(s.kind==='alienlaser'){"
repl="for(const s of engine.shots){ctx.save();ctx.translate(s.x,s.y);ctx.rotate(Math.atan2(s.vy,s.vx));if(s.kind==='magnifier'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(Math.max(18,s.radius*2.8))+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('🔎',0,0)}else if(s.kind==='alienlaser'){"
if needle not in s:
    raise SystemExit('Projectile draw loop anchor not found')
s=s.replace(needle,repl,1)

# Optional patch note hotfix line without bumping gameplay version.
patch_anchor='<div class="patch-version"><h3>v3.48 · 탐정 리워크</h3><ul>'
if patch_anchor in s and 'v3.48.2 탐정 먹통 핫픽스' not in s:
    s=s.replace(patch_anchor,patch_anchor+'<li>v3.48.2 탐정 먹통 핫픽스: 돋보기와 감옥 렌더링 위치 오류 수정.</li>',1)

required=[
    "if(s.kind==='magnifier'){ctx.rotate(-Math.atan2(s.vy,s.vx));",
    "ctx.fillText('🔎',0,0)",
    "if((f.jailedUntil||0)>engine.time){const rr=Math.max(22,f.radius*1.3);ctx.save();"
]
for marker in required:
    if marker not in s:
        raise SystemExit('Missing fixed marker: '+marker)
if "for(const s of this.shots){if(s.kind==='magnifier'){ctx.save()" in s:
    raise SystemExit('Invalid Engine renderer still present')

p.write_text(s,encoding='utf-8')
print('v3.48.2 Detective runtime fix applied')

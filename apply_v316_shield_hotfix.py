from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(f'PATCH FAILED: {label}')
    s=s.replace(old,new,count)

# 1) Replace old knight shield state with charge-window state.
rep("knightShieldReady:type.id==='knight',knightShieldNext:0,knightShieldAngle:0,nextJump:",
    "knightShieldReady:false,knightShieldNext:type.id==='knight'?10:0,knightShieldChargedUntil:type.id==='knight'?3:0,knightShieldAngle:0,nextJump:",
    'shield state')

# 2) Shield rotation + recurring 3-second guaranteed projectile-block window every 10 seconds.
old_update="updateKnightShield(f,dt){if(f.id!=='knight'||f.health<=0)return;f.knightShieldAngle=(f.knightShieldAngle+dt*2.8)%(Math.PI*2);if(!f.knightShieldReady&&this.time>=f.knightShieldNext-1e-9){f.knightShieldReady=true;this.effect(f,'🛡️ 방패 재충전','skill')}}"
new_update="updateKnightShield(f,dt){if(f.id!=='knight'||f.health<=0)return;f.knightShieldAngle=(f.knightShieldAngle+dt*2.8)%(Math.PI*2);if(this.time>=f.knightShieldNext-1e-9){f.knightShieldChargedUntil=this.time+3;f.knightShieldNext=this.time+13;this.effect(f,'🛡️ 완전 방어 3초!','skill')}}"
rep(old_update,new_update,'shield update')

# 3) Remove old one-hit global shield interception from central attack path.
old_intercept=" if(e.id==='knight'&&e.knightShieldReady){e.knightShieldReady=false;e.knightShieldNext=this.time+10;this.effect(e,'🛡️ 완전 방어!','skill');if(dmg>=500)this.knightShockwave(e);return 0}\n"
rep(old_intercept,"",'old shield intercept')

# 4) Add physical rotating-shield projectile collision helper and charged full-block helper.
anchor="knightShockwave(f){if(f.id!=='knight'||f.health<=0)return;"
if anchor not in s:
    raise SystemExit('PATCH FAILED: shockwave anchor')
helpers="""knightShieldPoint(f){const sr=f.radius+40;return {x:f.x+Math.cos(f.knightShieldAngle)*sr,y:f.y+Math.sin(f.knightShieldAngle)*sr,r:28*f.scale}}
knightBlocksProjectile(f,s){if(f.id!=='knight'||f.health<=0)return false;const charged=this.time<f.knightShieldChargedUntil-1e-9;if(charged)return true;const p=this.knightShieldPoint(f);return Math.hypot(s.x-p.x,s.y-p.y)<=p.r+(s.radius||5)}
blockProjectileWithKnight(f,s,owner){const raw=s.instant?f.health:(s.damage||0);s.life=0;this.effect(f,this.time<f.knightShieldChargedUntil-1e-9?'🛡️ 완전 방어!':'🛡️ 방패 막기!','skill');if(raw>=500)this.knightShockwave(f);if(owner){owner.attack=.12/owner.scale}return true}
"""
s=s.replace(anchor,helpers+anchor,1)

# 5) Intercept moon projectile before normal hit handling.
old_moon="const e=this.enemies(f).find(v=>distance(s,v)<v.radius+s.radius);if(e&&!s.hit){this.attackProjectile(f,e,s);s.hit=true;s.returning=true}"
new_moon="const e=this.enemies(f).find(v=>distance(s,v)<v.radius+s.radius);if(e&&!s.hit){if(e.id==='knight'&&this.knightBlocksProjectile(e,s)){this.blockProjectileWithKnight(e,s,f);s.hit=true;s.returning=true}else{this.attackProjectile(f,e,s);s.hit=true;s.returning=true}}"
rep(old_moon,new_moon,'moon projectile shield')

# 6) Intercept every normal projectile by charged bubble OR rotating shield geometry.
old_hit="if(s.life>0){const e=this.enemies(f).find(v=>distance(s,v)<v.radius+s.radius);if(e){this.attackProjectile(f,e,s);s.life=0;if(this.result!==null)break}}"
new_hit="if(s.life>0){const knights=this.enemies(f).filter(v=>v.id==='knight'&&v.health>0);const blocker=knights.find(v=>this.knightBlocksProjectile(v,s));if(blocker){this.blockProjectileWithKnight(blocker,s,f);continue}const e=this.enemies(f).find(v=>distance(s,v)<v.radius+s.radius);if(e){this.attackProjectile(f,e,s);s.life=0;if(this.result!==null)break}}"
rep(old_hit,new_hit,'normal projectile shield')

# 7) Update HUD text only; version and patch notes intentionally unchanged.
old_ability="f.id==='knight'?(f.knightShieldReady?'🛡️ 방패 준비 · 다음 공격 완전 방어':'🛡️ 재충전 '+Math.max(0,f.knightShieldNext-engine.time).toFixed(1)+'초')"
new_ability="f.id==='knight'?(engine.time<f.knightShieldChargedUntil?'🛡️ 완전 방어 '+Math.max(0,f.knightShieldChargedUntil-engine.time).toFixed(1)+'초':'🛡️ 회전 방패 · 충전 '+Math.max(0,f.knightShieldNext-engine.time).toFixed(1)+'초')"
rep(old_ability,new_ability,'ability hud')

# 8) Make visible rotating shield bigger and brighter during charge.
old_draw="const a=f.knightShieldAngle||engine.time*2.8,sr=r+24,sx=f.x+Math.cos(a)*sr,sy=f.y+Math.sin(a)*sr;ctx.save();ctx.globalAlpha=f.knightShieldReady?1:.28;ctx.font='24px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🛡️',sx,sy);ctx.restore();"
new_draw="const a=f.knightShieldAngle||engine.time*2.8,sr=r+40,sx=f.x+Math.cos(a)*sr,sy=f.y+Math.sin(a)*sr,charged=engine.time<f.knightShieldChargedUntil;ctx.save();ctx.globalAlpha=charged?1:.82;ctx.font=(charged?44:38)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🛡️',sx,sy);if(charged){ctx.strokeStyle='#d9efff';ctx.lineWidth=4;ctx.globalAlpha=.55;ctx.beginPath();ctx.arc(f.x,f.y,r+55,0,Math.PI*2);ctx.stroke()}ctx.restore();"
rep(old_draw,new_draw,'shield draw')

p.write_text(s,encoding='utf-8')
print('v3.16 rotating shield hotfix applied')

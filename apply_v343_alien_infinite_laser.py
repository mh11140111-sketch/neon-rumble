from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:220]!r}')
    s=s.replace(old,new,count)

# Visible version + patch note.
rep('BATTLE <b>v3.42</b>','BATTLE <b>v3.43</b>')
rep('<summary>📒 패치노트 · v3.42</summary><div class="patch-body">',
    '<summary>📒 패치노트 · v3.43</summary><div class="patch-body"><div class="patch-version"><h3>v3.43 · 우주에서 온 반사 레이저</h3><ul><li>신규 캐릭터 👽 외계인 추가.</li><li>외계인: 2초마다 레이저를 발사. 레이저는 적에게 명중할 때까지 벽에서 횟수 제한 없이 계속 반사.</li><li>레이저 피해는 발사할 때마다 50~70 사이에서 무작위로 결정.</li></ul></div>')

# Add Alien after Money Man in roster.
moneyman="{id:'moneyman',name:'머니맨',icon:'🤑',tag:'돈가방 · 나는 돈 · 돈의 행복',hp:650,damage:20,speed:155,cooldown:1.5,unlock:'moneyManShop',description:'💰 돈가방을 던져 피해 20과 돈의 행복 2중첩을 주고 적중 지점에서 💵 돈을 8방향으로 뿌려. 5초마다 느린 💸 나는 돈을 던지며, 돈의 행복 중첩이 많을수록 더 강해져.',detail:'HP 650 · 💰 돈가방 20 / 1.5초 · 적중 시 💵 8방향 각 50 · 💸 5초마다 100 + 돈의 행복 중첩당 10 · 돈의 행복 최대 5중첩 · 중첩당 상대 피해 −10 · 3초마다 1중첩 감소'},"
alien="{id:'alien',name:'외계인',icon:'👽',tag:'무한 반사 레이저',hp:1000,damage:50,speed:150,cooldown:2,description:'2초마다 레이저를 발사해. 레이저는 상대에게 닿을 때까지 벽을 횟수 제한 없이 계속 튕기며, 명중 피해는 50~70 중 무작위야.',detail:'HP 1000 · 👽 레이저 2초마다 발사 · 피해 50~70 랜덤 · 적중 전까지 벽 무한 반사'},"
rep(moneyman,moneyman+'\n'+alien)

# Alien laser skill.
anchor="moneyManSkill(f,e){if(f.id!=='moneyman'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0)return;"
alien_skill="alienSkill(f,e){if(f.id!=='alien'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0||f.cd>1e-9)return;const a=this.aim(f,e),dmg=50+Math.floor(this.random()*21);this.shots.push({x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'alienlaser',radius:7*f.scale,speed:430*f.scale,damage:dmg*f.scale,life:Infinity,bounces:0});f.cd=2/f.scale;f.attack=.18/f.scale;this.effect(f,'👽 레이저 '+dmg+'!','skill')}\n"
rep(anchor,alien_skill+anchor)

# Trigger Alien special attack from fighter update.
old="if(f.id==='coolguy')this.coolGuySkill(f,e);if(f.id==='firefighter')this.firefighterSkill(f,e);if(f.id==='moneyman')this.moneyManSkill(f,e);if(['zombie','king_zombie','zombie_mini','zombie_mage'].includes(f.id))this.zombieSkill(f,e);"
new="if(f.id==='coolguy')this.coolGuySkill(f,e);if(f.id==='firefighter')this.firefighterSkill(f,e);if(f.id==='moneyman')this.moneyManSkill(f,e);if(f.id==='alien')this.alienSkill(f,e);if(['zombie','king_zombie','zombie_mini','zombie_mage'].includes(f.id))this.zombieSkill(f,e);"
rep(old,new)

# Alien has no generic body-contact attack.
rep("'chef','coolguy','firefighter','moneyman','zombie'","'chef','coolguy','firefighter','moneyman','alien','zombie'")

# Infinite wall reflection for Alien laser while preserving Money Man wall burst.
old="if(s.x<22||s.x>698||s.y<22||s.y>698){if(s.kind==='moneybag'){const bx=clamp(s.x,22,698),by=clamp(s.y,22,698);this.moneyBagBurst(f,bx,by);s.x=bx;s.y=by;s.life=0}else if(s.bounces>0){if(s.x<22||s.x>698)s.vx=-s.vx;if(s.y<22||s.y>698)s.vy=-s.vy;s.x=clamp(s.x,22,698);s.y=clamp(s.y,22,698);s.bounces--}else s.life=0}"
new="if(s.x<22||s.x>698||s.y<22||s.y>698){if(s.kind==='moneybag'){const bx=clamp(s.x,22,698),by=clamp(s.y,22,698);this.moneyBagBurst(f,bx,by);s.x=bx;s.y=by;s.life=0}else if(s.kind==='alienlaser'){if(s.x<22||s.x>698)s.vx=-s.vx;if(s.y<22||s.y>698)s.vy=-s.vy;s.x=clamp(s.x,22,698);s.y=clamp(s.y,22,698)}else if(s.bounces>0){if(s.x<22||s.x>698)s.vx=-s.vx;if(s.y<22||s.y>698)s.vy=-s.vy;s.x=clamp(s.x,22,698);s.y=clamp(s.y,22,698);s.bounces--}else s.life=0}"
rep(old,new)

# Laser rendering.
old="if(s.kind==='moneybag'||s.kind==='cash'||s.kind==='flyingmoney'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(s.kind==='moneybag'?30:s.kind==='flyingmoney'?31:27)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText(s.kind==='moneybag'?'💰':s.kind==='flyingmoney'?'💸':'💵',0,0)}else if(s.kind==='beer')"
new="if(s.kind==='alienlaser'){ctx.save();ctx.strokeStyle='#74f7ff';ctx.shadowColor='#4be9ff';ctx.shadowBlur=16;ctx.lineWidth=7*f.scale;ctx.beginPath();ctx.moveTo(-24*f.scale,0);ctx.lineTo(12*f.scale,0);ctx.stroke();ctx.fillStyle='#eaffff';ctx.beginPath();ctx.arc(10*f.scale,0,5*f.scale,0,Math.PI*2);ctx.fill();ctx.restore()}else if(s.kind==='moneybag'||s.kind==='cash'||s.kind==='flyingmoney'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(s.kind==='moneybag'?30:s.kind==='flyingmoney'?31:27)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText(s.kind==='moneybag'?'💰':s.kind==='flyingmoney'?'💸':'💵',0,0)}else if(s.kind==='beer')"
rep(old,new)

# HUD ability text.
rep("function ability(f){if(f.id==='moneyman')", "function ability(f){if(f.id==='alien')return '👽 레이저 2초 · 벽 무한 반사 · 피해 50~70';if(f.id==='moneyman')")

p.write_text(s,encoding='utf-8')
print('v3.43 Alien patch applied')

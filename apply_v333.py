from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n!=count:
        raise SystemExit(f'replace mismatch: expected {count}, found {n}: {old[:120]!r}')
    s=s.replace(old,new,count)

# Version / patch notes
rep('BATTLE <b>v3.32</b>','BATTLE <b>v3.33</b>')
rep('📒 패치노트 · v3.32','📒 패치노트 · v3.33')
rep('<div class="patch-body"><div class="patch-version"><h3>v3.32 · 요리사</h3>', '<div class="patch-body"><div class="patch-version"><h3>v3.33 · 쿨가이 & 밸런스</h3><ul><li>요리사: 5초 동안 공격하지 않으면 계란을 먹던 시간을 8초로 증가.</li><li>분노한 남자: 2회 부활한 🤬 상태의 👎 공격 간격 0.5초 → 0.8초.</li><li>신규 캐릭터 👤 쿨가이: 8초마다 가장 가까운 적 방향으로 부채꼴 샤우팅 공격. 범위 안의 모든 적에게 피해 150.</li><li>쿨가이: 샤우팅 공격 중 🗣️ 모습으로 변하며 전용 웅장한 샤우팅 효과음 적용.</li></ul></div><div class="patch-version"><h3>v3.32 · 요리사</h3>')

# Chef self-heal 5 -> 8 seconds, roster text and mechanics
rep("5초 동안 공격하지 않으면 계란을 먹어 최대 체력의 30%를 회복해.","8초 동안 공격하지 않으면 계란을 먹어 최대 체력의 30%를 회복해.")
rep("5초 무공격 시 자기 회복 30%","8초 무공격 시 자기 회복 30%")
rep("this.time-f.chefLastAttackAt>=5/f.scale-1e-9","this.time-f.chefLastAttackAt>=8/f.scale-1e-9")

# Angry Man final-stage thumbs cadence 0.5 -> 0.8 seconds
rep("const stage=f.revivals||0,dmg=stage===0?30:stage===1?50:70,rate=stage===0?1:.5;","const stage=f.revivals||0,dmg=stage===0?30:stage===1?50:70,rate=stage===0?1:stage===1?.5:.8;")
rep("🤬 단계는 👎 70/0.5초.","🤬 단계는 👎 70/0.8초.")
rep("🤬 👎70/0.5초","🤬 👎70/0.8초")

# New roster entry: Cool Guy
needle="{id:'chef',name:'요리사',icon:'👨‍🍳',tag:'프라이팬 · 기절 · 계란 회복',hp:1000,damage:65,speed:155,cooldown:0,description:'🍳 프라이팬이 가장 가까운 적을 가리켜. 계란이 있을 때 팬이 적에게 닿으면 피해 90 + 화상, 없으면 피해 65를 줘. 공격이 적중하면 1초 기절과 약한 넉백을 주고 3초 동안 다시 공격할 수 없어. 계란은 2초 뒤 다시 생기고, 8초 동안 공격하지 않으면 계란을 먹어 최대 체력의 30%를 회복해. 팀전에서는 팬이 아군에게 닿으면 계란으로 아군도 30% 회복해.',detail:'HP 1000 · 팬 공격 65 · 계란 공격 90 + 화상 · 적중 시 기절 1초 + 약한 넉백 / 공격 쿨타임 3초 · 계란 재생 2초 · 8초 무공격 시 자기 회복 30% · 계란 팬이 아군 접촉 시 아군 회복 30%'}"
insert=needle+",\n{id:'coolguy',name:'쿨가이',icon:'👤',tag:'부채꼴 샤우팅',hp:1000,damage:150,speed:160,cooldown:8,description:'8초마다 가장 가까운 적 방향으로 자기 몸에서 시작하는 부채꼴 샤우팅 공격을 해. 범위 안 모든 적에게 피해 150을 주며 공격 순간 🗣️ 모습으로 변해.',detail:'HP 1000 · 부채꼴 샤우팅 150 · 공격 주기 8초 · 범위 내 모든 적 타격 · 공격 중 🗣️ 변신 · 전용 웅장한 샤우팅 사운드'}"
rep(needle,insert)

# Constructor state
rep("chefEggReady:type.id==='chef',chefEggReadyAt:0,chefLastAttackAt:0,chefPanNext:0,ghostReviveUsed:false", "chefEggReady:type.id==='chef',chefEggReadyAt:0,chefLastAttackAt:0,chefPanNext:0,coolGuyNext:type.id==='coolguy'?8/scale:9999,coolGuyShoutUntil:0,coolGuyShoutAngle:0,ghostReviveUsed:false")

# Cool Guy skill method before angry man
marker="angryManSkill(f,e,dt){"
method="""coolGuySkill(f,e){
 if(f.id!=='coolguy'||f.health<=0||f.stunUntil>this.time||this.time<f.coolGuyNext-1e-9)return;
 const a=this.aim(f,e),ang=Math.atan2(a.y,a.x),range=280*f.scale,half=.65;
 f.coolGuyNext=this.time+8/f.scale;f.coolGuyShoutUntil=this.time+.65/f.scale;f.coolGuyShoutAngle=ang;f.attack=.65/f.scale;
 this.effects.push({x:f.x,y:f.y,text:'🗣️ 샤우팅!',kind:'shoutcone',side:f.side,team:f.team,life:.65/f.scale,angle:ang,range,half});
 this.effect(f,'🗣️ 샤우팅!','shout');this.emit('👤 쿨가이가 웅장하게 샤우팅!');
 for(const target of this.enemies(f)){
   const dx=target.x-f.x,dy=target.y-f.y,d=Math.hypot(dx,dy);if(d>range+target.radius)continue;
   const ta=Math.atan2(dy,dx),diff=Math.atan2(Math.sin(ta-ang),Math.cos(ta-ang));
   if(Math.abs(diff)<=half)this.attack(f,target,150*f.scale);
   if(this.result!==null)return;
 }
}
"""
rep(marker,method+marker)

# Invoke skill
rep("if(f.id==='cowboy')this.cowboySkill(f,e);if(f.id==='chef')this.chefSkill(f);", "if(f.id==='cowboy')this.cowboySkill(f,e);if(f.id==='chef')this.chefSkill(f);if(f.id==='coolguy')this.coolGuySkill(f,e);")

# Exclude generic melee
rep("'ghost','cowboy','chef'].includes(f.id)","'ghost','cowboy','chef','coolguy'].includes(f.id)")

# Draw shout cone before fighter body
render_marker="if(f.id==='chef'&&f.health>0){const pp=engine.chefPanTip(f)"
cone="""if(f.id==='coolguy'&&f.health>0&&f.coolGuyShoutUntil>engine.time){const sa=f.coolGuyShoutAngle||0,sr=280*f.scale,sh=.65;ctx.save();ctx.globalAlpha=.24;ctx.fillStyle=colors[f.team];ctx.beginPath();ctx.moveTo(f.x,f.y);ctx.arc(f.x,f.y,sr,sa-sh,sa+sh);ctx.closePath();ctx.fill();ctx.globalAlpha=.85;ctx.strokeStyle='#eaf6ff';ctx.lineWidth=5*f.scale;ctx.beginPath();ctx.moveTo(f.x,f.y);ctx.arc(f.x,f.y,sr,sa-sh,sa+sh);ctx.closePath();ctx.stroke();ctx.restore();ctx.globalAlpha=f.id==='invisible'?.38:1;}"""
rep(render_marker,cone+render_marker)

# Render 🗣️ only during attack
rep("if(f.id==='cowboy'&&f.cowboyMounted){ctx.font=(31*f.bodyScale)+'px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.fillText('🤠',f.x,f.y-14*f.bodyScale);ctx.fillText('🐴',f.x,f.y+18*f.bodyScale)}else{ctx.fillText(f.icon,f.x,f.y+1)}", "if(f.id==='cowboy'&&f.cowboyMounted){ctx.font=(31*f.bodyScale)+'px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.fillText('🤠',f.x,f.y-14*f.bodyScale);ctx.fillText('🐴',f.x,f.y+18*f.bodyScale)}else if(f.id==='coolguy'&&f.coolGuyShoutUntil>engine.time){ctx.fillText('🗣️',f.x,f.y+1)}else{ctx.fillText(f.icon,f.x,f.y+1)}")

# Ability HUD
rep("function ability(f){if(f.id==='lizard')", "function ability(f){if(f.id==='coolguy')return '🗣️ 샤우팅 '+Math.max(0,(f.coolGuyNext||0)-engine.time).toFixed(1)+'초 · 부채꼴 150';if(f.id==='lizard')")

# Dedicated shout SFX
rep("else if(tx.includes('돌진'))key='dash';", "else if(tx.includes('돌진'))key='dash';else if(id==='coolguy'&&tx.includes('샤우팅'))key='shout';")
rep("else if(key==='dash'){sfxNoise(.08,.03,3200);sfxSweep(380,150,.08,.022,'triangle')}\n}", "else if(key==='dash'){sfxNoise(.08,.03,3200);sfxSweep(380,150,.08,.022,'triangle')}\n else if(key==='shout'){tone(72,.48,.12,'sawtooth');tone(108,.42,.09,'sine',.03);sfxSweep(220,70,.5,.085,'sawtooth');sfxNoise(.42,.09,1500);sfxSweep(95,360,.38,.055,'triangle',.08)}\n}")

p.write_text(s,encoding='utf-8')
print('v3.33 patch applied')

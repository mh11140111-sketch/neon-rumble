from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if s.count(old)<count:
        raise SystemExit(f'PATCH FAILED {label}: {s.count(old)}/{count}')
    s=s.replace(old,new,count)

# Version / notes
rep('BATTLE <b>v3.25</b>','BATTLE <b>v3.26</b>','version')
rep('📒 패치노트 · v3.25','📒 패치노트 · v3.26','summary')
anchor='<div class="patch-body"><div class="patch-version"><h3>v3.25 · 악마의 눈 & 경찰 밸런스</h3>'
notes='<div class="patch-body"><div class="patch-version"><h3>v3.26 · 눈사람 & 분노한 남자</h3><ul><li>악마의 눈: 저주받은 손 체력 113 → 66.</li><li>기사: 10초마다 피해 150의 거대검격 추가.</li><li>신규 캐릭터 ⛄️ 눈사람: 눈송이 피해 30, 명중 시 50% 확률 1초 얼림. 화상 피해 5배.</li><li>신규 캐릭터 😠 분노한 남자: 체력 333, 총 2회 부활. 부활 단계마다 👎 공격이 강화되며 최종 단계는 근접 🤜 피해 85 + 1초 기절.</li></ul></div><div class="patch-version"><h3>v3.25 · 악마의 눈 & 경찰 밸런스</h3>'
rep(anchor,notes,'notes')

# Knight roster
old="{id:'knight',name:'기사',icon:'🛡️',tag:'회전 방패 · 누적 충격파',hp:1000,damage:95,speed:125,cooldown:.95,description:'받는 피해가 항상 30% 감소해. 적에게 접근해 검격 95로 공격하고, 회전 방패가 투사체를 막아. 방패가 막은 피해가 누적 500에 도달하면 전장 충격파를 발동해.',detail:'피해 감소 30% · 검격 95 · 공격 간격 0.95초 · 방패로 막은 피해 누적 500 → 충격파 100 / 자신 제외 전원 3초 기절 · 발동 후 누적 0'}"
new="{id:'knight',name:'기사',icon:'🛡️',tag:'회전 방패 · 거대검격',hp:1000,damage:95,speed:125,cooldown:.95,description:'받는 피해가 항상 30% 감소해. 적에게 접근해 검격 95로 공격하고, 회전 방패가 투사체를 막아. 10초마다 피해 150의 거대검격을 날려.',detail:'피해 감소 30% · 검격 95 · 공격 간격 0.95초 · 거대검격 150 / 10초 · 방패 누적 500 → 충격파 100 / 자신 제외 전원 3초 기절'}"
rep(old,new,'knight roster')

# Devil Eye hand HP text/code
rep('손 HP 113 · 유도 저주탄 피해 25 + 저주','손 HP 66 · 유도 저주탄 피해 25 + 저주','hand detail')
rep('const hs=owner.boss?1.5:1,hp=113*hs','const hs=owner.boss?1.5:1,hp=66*hs','hand hp')

# New roster entries
old="{id:'devileye',name:'악마의 눈',icon:'🧿',tag:'저주 · 저주받은 손',hp:666,damage:50,speed:155,cooldown:0,description:'몸에 닿은 적에게 직접 피해 50과 저주를 부여해. 저주는 상태이상 면역을 무시하고 0.3초마다 피해 10을 주며, 저주받은 대상은 4초마다 🪬 저주받은 손을 불러내. 악마의 눈도 13초마다 손을 직접 소환해.',detail:'HP 666 · 접촉 피해 50 + 저주 · 저주 피해 10 / 0.3초 · 저주 대상 손 소환 4초마다 / 5초 유지 · 손 HP 66 · 유도 저주탄 피해 25 + 저주 · 본체 손 소환 13초마다 / 무한 유지'}\n];"
new="{id:'devileye',name:'악마의 눈',icon:'🧿',tag:'저주 · 저주받은 손',hp:666,damage:50,speed:155,cooldown:0,description:'몸에 닿은 적에게 직접 피해 50과 저주를 부여해. 저주는 상태이상 면역을 무시하고 0.3초마다 피해 10을 주며, 저주받은 대상은 4초마다 🪬 저주받은 손을 불러내. 악마의 눈도 13초마다 손을 직접 소환해.',detail:'HP 666 · 접촉 피해 50 + 저주 · 저주 피해 10 / 0.3초 · 저주 대상 손 소환 4초마다 / 5초 유지 · 손 HP 66 · 유도 저주탄 피해 25 + 저주 · 본체 손 소환 13초마다 / 무한 유지'},\n{id:'snowman',name:'눈사람',icon:'⛄️',tag:'눈송이 · 얼림',hp:1000,damage:30,speed:145,cooldown:1,description:'1초마다 눈송이를 발사해 피해 30을 줘. 명중 시 50% 확률로 상대를 1초 동안 얼려 움직임과 행동을 멈춰. 화상 피해는 5배로 받아.',detail:'HP 1000 · 눈송이 30 / 1초 · 명중 시 50% 확률 1초 얼림 · 화상 피해 ×5'},\n{id:'angryman',name:'분노한 남자',icon:'😠',tag:'2회 부활 · 분노 강화',hp:333,damage:30,speed:165,cooldown:1,description:'체력 333으로 시작해 총 2번 부활해. 😠 단계는 👎 30/1초, 😡 단계는 👎 50/0.5초, 🤬 단계는 👎 70/0.5초로 공격해. 최종 단계에서는 가까운 적에게 🤜 피해 85와 1초 기절을 줘.',detail:'HP 333 · 총 2회 부활 · 😠 👎30/1초 · 😡 👎50/0.5초 · 🤬 👎70/0.5초 · 최종 🤜85 + 1초 기절'}\n];"
rep(old,new,'new roster')

# Main fighter state: knight giant timer + angry punch timer
rep("knightShieldAngle:0,knightBlockedDamage:0,policeBarrageUsed:false", "knightShieldAngle:0,knightBlockedDamage:0,knightGiantNext:type.id==='knight'?10/scale:9999,angryPunchCd:0,policeBarrageUsed:false", 'state')

# Add methods before robotSkill
anchor='robotSkill(f,dt){'
methods=r'''knightGiantSlash(f,e){
 if(f.id!=='knight'||f.health<=0||f.stunUntil>this.time||this.time<f.knightGiantNext-1e-9)return;
 f.knightGiantNext=this.time+10/f.scale;const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+12),y:f.y+a.y*(f.radius+12),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'giantslash',radius:24*f.scale,speed:430*f.scale,damage:150*f.scale,life:2.2,bounces:0});f.attack=.25/f.scale;this.effect(f,'⚔️ 거대검격!','skill');this.emit('🛡️ 기사가 거대검격!')
}
snowmanShot(f,e){
 if(f.id!=='snowman'||f.health<=0||f.cd>1e-9)return;const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+7),y:f.y+a.y*(f.radius+7),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'snow',radius:8*f.scale,speed:300*f.scale,damage:30*f.scale,life:3,bounces:0,stun:this.random()<.5?1*f.scale:0});f.cd=1/f.scale;f.attack=.18/f.scale;this.effect(f,'❄️ 눈송이!','skill')
}
angryManSkill(f,e,dt){
 if(f.id!=='angryman'||f.health<=0||f.stunUntil>this.time)return;f.angryPunchCd=Math.max(0,(f.angryPunchCd||0)-dt);const stage=f.revivals||0,dmg=stage===0?30:stage===1?50:70,rate=stage===0?1:.5;
 if(f.cd<=1e-9){const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+7),y:f.y+a.y*(f.radius+7),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'thumb',radius:7*f.scale,speed:340*f.scale,damage:dmg*f.scale,life:3,bounces:0});f.cd=rate/f.scale;f.attack=.18/f.scale;this.effect(f,'👎 '+dmg,'skill')}
 if(stage>=2&&f.angryPunchCd<=1e-9&&distance(f,e)<=f.radius+e.radius+36*f.scale){const dealt=this.attack(f,e,85*f.scale);f.angryPunchCd=1/f.scale;if(dealt>0&&e.health>0){e.stunUntil=Math.max(e.stunUntil,this.time+1*f.scale);this.effect(e,'🤜 85 · 기절!','skill')}}
}
'''+anchor
rep(anchor,methods,'new methods')

# step hooks
rep("this.transformHero(f);this.updateVampire(f);this.moonSkill(f);this.updateKnightShield(f,dt);", "this.transformHero(f);this.updateVampire(f);this.moonSkill(f);this.updateKnightShield(f,dt);this.knightGiantSlash(f,e);if(f.id==='snowman')this.snowmanShot(f,e);if(f.id==='angryman')this.angryManSkill(f,e,dt);", 'step hooks')

# Exclude special ranged fighters from generic contact melee
rep("'genie','devileye','cursedhand'].includes(f.id)", "'genie','devileye','cursedhand','snowman','angryman'].includes(f.id)", 'melee exclusion')

# Snowman burn x5 (tree stays x2)
rep("p.damage*(e.id==='tree'?2:1)*(1-e.armor)", "p.damage*(e.id==='snowman'?5:e.id==='tree'?2:1)*(1-e.armor)", 'snow burn')

# Angry man revival piggybacks on the existing death-to-egg gate so every damage path respects it.
needle="formEgg(f){\n if(f.id!=='phoenix'||f.egg||f.revivals>=1||f.health>0)return false;"
replacement="formEgg(f){\n if(f.id==='angryman'&&f.health<=0&&f.revivals<2){f.revivals++;f.hp=333*(f.boss?2.5:1);f.health=f.hp;f.icon=f.revivals===1?'😡':'🤬';f.damage=(f.revivals===1?50:70)*f.scale;f.cooldown=(f.revivals===0?1:.5)/f.scale;f.cd=.35/f.scale;f.angryPunchCd=0;f.poison=null;f.toxin=null;f.burn=null;f.curse=null;f.stunUntil=0;f.slow=0;f.slowPower=0;f.rootSlow=0;f.rootSlowPower=0;f.trail=[];this.shots=this.shots.filter(s=>s.owner!==f.side);this.effect(f,f.icon+' 부활!','skill');this.emit('분노한 남자가 '+f.icon+' 상태로 부활!');return true}\n if(f.id!=='phoenix'||f.egg||f.revivals>=1||f.health>0)return false;"
rep(needle,replacement,'angry revival')

p.write_text(s,encoding='utf-8')
print('NEON RUMBLE v3.26 applied')

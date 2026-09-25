from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'missing target ({n}<{count}): {old[:120]!r}')
    s=s.replace(old,new,count)

# Version / notes
rep('BATTLE <b>v3.27</b>','BATTLE <b>v3.28</b>')
rep('📒 패치노트 · v3.27','📒 패치노트 · v3.28')
rep('<div class="patch-body"><div class="patch-version"><h3>v3.27 · 설정 & 테스트 사운드</h3>',
    '<div class="patch-body"><div class="patch-version"><h3>v3.28 · 도마뱀 & 복서 리워크</h3><ul><li>달: 월하강림 준비 시간 45초 → 35초로 롤백.</li><li>알라딘: 본체 AI를 적과 거리를 유지하며 회피하는 방식으로 변경. 지니 AI는 유지.</li><li>신규 캐릭터 🦎 도마뱀: 이동속도 30% 증가, 근접 피해 70. HP 30% 이하에서 꼬리를 소환하며 꼬리가 살아 있는 동안 적 AI가 꼬리를 우선 공격.</li><li>복서 리워크: 10초마다 어퍼컷 피해 125. 대상은 1초간 공중에 뜬 뒤 착지 피해 50 + 기절 1초. 보스 복서는 능력치 2배.</li></ul></div><div class="patch-version"><h3>v3.27 · 설정 & 테스트 사운드</h3>')

# Roster updates
rep("{id:'boxer',name:'복서',icon:'🥊',tag:'반사 · 돌진',hp:1000,damage:65,speed:195,cooldown:.42,description:'랜덤하게 튕겨 다니다 2.8초마다 상대를 향해 돌진. 돌진 펀치는 130 피해.',detail:'접촉 65 · 돌진 130 · 돌진 주기 2.8초'},",
    "{id:'boxer',name:'복서',icon:'🥊',tag:'돌진 · 어퍼컷',hp:1000,damage:65,speed:195,cooldown:.42,description:'랜덤하게 튕겨 다니다 2.8초마다 상대를 향해 돌진해. 10초마다 강력한 어퍼컷으로 피해 125를 주고 상대를 1초간 공중에 띄운 뒤 착지 피해 50과 1초 기절을 줘.',detail:'접촉 65 · 돌진 130 / 2.8초 · 어퍼컷 125 / 10초 · 공중 1초 · 착지 50 + 기절 1초 · 보스 2배'},")
rep("{id:'angryman',name:'분노한 남자',icon:'😠',tag:'2회 부활 · 분노 강화',hp:333,damage:30,speed:165,cooldown:1,description:'체력 333으로 시작해 총 2번 부활해. 😠 단계는 👎 30/1초, 😡 단계는 👎 50/0.5초, 🤬 단계는 👎 70/0.5초로 공격해. 최종 단계에서는 가까운 적에게 🤜 피해 85와 1초 기절을 줘.',detail:'HP 333 · 총 2회 부활 · 😠 👎30/1초 · 😡 👎50/0.5초 · 🤬 👎70/0.5초 · 최종 🤜85 + 1초 기절'}\n];",
    "{id:'angryman',name:'분노한 남자',icon:'😠',tag:'2회 부활 · 분노 강화',hp:333,damage:30,speed:165,cooldown:1,description:'체력 333으로 시작해 총 2번 부활해. 😠 단계는 👎 30/1초, 😡 단계는 👎 50/0.5초, 🤬 단계는 👎 70/0.5초로 공격해. 최종 단계에서는 가까운 적에게 🤜 피해 85와 1초 기절을 줘.',detail:'HP 333 · 총 2회 부활 · 😠 👎30/1초 · 😡 👎50/0.5초 · 🤬 👎70/0.5초 · 최종 🤜85 + 1초 기절'},\n{id:'lizard',name:'도마뱀',icon:'🦎',tag:'고속 · 꼬리 미끼',hp:1000,damage:70,speed:188.5,cooldown:.7,description:'일반 캐릭터보다 30% 빠르게 움직이며 근접 피해 70으로 공격해. 체력이 30% 이하가 되면 꼬리를 한 번 소환하고, 꼬리가 살아 있는 동안 모든 적 AI가 꼬리를 우선 공격해.',detail:'HP 1000 · 이동속도 +30% · 근접 70 · HP 30% 이하 꼬리 1회 소환 · 꼬리 HP는 본체 최대 HP의 30% · 꼬리 생존 중 적 AI 우선 타깃'}\n];")

# Moon rollback and fighter state
rep("knightGiantNext:type.id==='knight'?10/scale:9999,angryPunchCd:0,policeBarrageUsed:false", 
    "knightGiantNext:type.id==='knight'?10/scale:9999,boxerUpperNext:type.id==='boxer'?10/scale:9999,airborneUntil:0,airborneSourceSide:null,airborneBaseY:null,lizardTailSummoned:false,lizardTailSide:null,angryPunchCd:0,policeBarrageUsed:false")
rep("moonUltStarted:false,moonUltAt:45/scale,moonUltLandAt:0", "moonUltStarted:false,moonUltAt:35/scale,moonUltLandAt:0")

# Tail target priority
rep("nearest(f){const es=this.enemies(f);return es.reduce((a,b)=>!a||distance(f,b)<distance(f,a)?b:a,null)}",
    "nearest(f){const es=this.enemies(f),tails=es.filter(e=>e.id==='lizardtail');const pool=tails.length?tails:es;return pool.reduce((a,b)=>!a||distance(f,b)<distance(f,a)?b:a,null)}")

# Aladdin evasive AI
rep("if(f.id==='aladdin'&&f.health>0&&f.stunUntil<=this.time){const at=this.nearest(f);if(at){const aa=this.aim(f,at);f.vx=aa.x;f.vy=aa.y;f.turn=.35}}",
    "if(f.id==='aladdin'&&f.health>0&&f.stunUntil<=this.time){const at=this.nearest(f);if(at){const aa=this.aim(f,at),d=distance(f,at),cx=360-f.x,cy=360-f.y,edge=f.x<105||f.x>615||f.y<105||f.y>615;let x,y;if(edge){const n=Math.hypot(cx,cy)||1;x=cx/n;y=cy/n}else if(d<330*f.scale){x=-aa.x-aa.y*.35;y=-aa.y+aa.x*.35}else{x=-aa.y;y=aa.x}const n=Math.hypot(x,y)||1;f.vx=x/n;f.vy=y/n;f.turn=.35}}")

# New mechanics before robotSkill
anchor="robotSkill(f,dt){\n"
insert="""spawnLizardTail(owner){
 if(!owner||owner.id!=='lizard'||owner.lizardTailSummoned||owner.health<=0)return null;owner.lizardTailSummoned=true;const side=this.fighters.length,hp=Math.max(1,Math.round(owner.hp*.3)),a=this.rand(-Math.PI,Math.PI),x=clamp(owner.x+Math.cos(a)*65,55,665),y=clamp(owner.y+Math.sin(a)*65,55,665),t={id:'lizardtail',name:'도마뱀 꼬리',icon:'🦎',tag:'미끼',description:'도마뱀이 떨어뜨린 꼬리. 살아 있는 동안 적 AI의 공격을 대신 끌어.',detail:'',side,team:owner.team,boss:owner.boss,scale:owner.scale,bodyScale:owner.boss?2:1,radius:24*(owner.boss?2:1),hp,health:hp,damage:0,armor:0,lifesteal:0,rootSlowStrength:0,magicSlowStrength:0,speed:0,cooldown:9999,x,y,vx:0,vy:0,attack:0,cd:9999,skill:0,turn:9999,dash:0,dashHit:false,awakened:false,revivals:0,heroReady:false,vampireBat:false,dodgeChance:0,knightShieldNext:0,knightShieldChargedUntil:0,knightShieldAngle:0,knightBlockedDamage:0,knightGiantNext:9999,boxerUpperNext:9999,airborneUntil:0,airborneSourceSide:null,airborneBaseY:null,lizardTailSummoned:false,lizardTailSide:null,policeBarrageUsed:false,policeBarrageUntil:0,policeBarrageCd:0,nextJump:9999,jumpFx:0,moonHalf:false,moonShot:null,moonUltStarted:false,moonUltAt:9999,moonUltLandAt:0,moonUltPhase:'',egg:false,eggUntil:0,stunUntil:0,burn:null,peckCd:0,flameCd:0,captureTarget:null,capturedBy:null,nextCapture:9999,venom:null,webAnchor:null,webs:[],webHits:{},studyUntil:0,nextStudy:9999,studyStart:0,minDamage:0,maxDamage:0,letterIndex:0,poison:null,toxin:null,curse:null,nextCursedHand:9999,slashCd:0,slashFx:0,slashAngle:0,idle:0,forgeLevel:0,forgeInterval:9999,rootLength:0,rootGrowth:0,rootHits:{},rootSlow:0,rootSlowPower:0,slow:0,slowPower:0,flash:0,damageDealt:0,hits:0,healed:0,trail:[],summon:true,ownerSide:owner.side};this.fighters.push(t);owner.lizardTailSide=t.side;this.effect(owner,'🦎 꼬리 분리!','skill');this.effect(t,'모든 적의 표적!','skill');this.emit('🦎 도마뱀이 꼬리를 버렸어! 적의 공격이 꼬리에 집중돼.');return t
}
lizardSkill(f){if(f.id==='lizard'&&!f.lizardTailSummoned&&f.health>0&&f.health<=f.hp*.3)this.spawnLizardTail(f)}
boxerUppercut(f,e){
 if(f.id!=='boxer'||f.health<=0||e.health<=0||f.stunUntil>this.time||this.time<f.boxerUpperNext-1e-9)return false;
 f.boxerUpperNext=this.time+10/f.scale;const dealt=this.attack(f,e,125*f.scale);if(dealt<=0||e.health<=0)return dealt>0;e.airborneUntil=this.time+1;e.airborneSourceSide=f.side;e.airborneBaseY=e.y;e.y=Math.max(22+e.radius,e.y-90);e.vx=0;e.vy=0;this.effect(f,'🥊 어퍼컷!','skill');this.effect(e,'공중 1초!','skill');return true
}
updateAirborne(){for(const e of this.fighters){if(!e.airborneUntil||e.airborneUntil<=0)continue;if(this.time<e.airborneUntil-1e-9){e.vx=0;e.vy=0;continue}const source=this.fighters[e.airborneSourceSide];e.airborneUntil=0;if(Number.isFinite(e.airborneBaseY)){e.y=clamp(e.airborneBaseY,22+e.radius,698-e.radius)}e.airborneBaseY=null;e.airborneSourceSide=null;if(e.health<=0||!source||source.health<=0)continue;const dealt=this.attack(source,e,50*source.scale);if(dealt>0&&e.health>0){e.stunUntil=Math.max(e.stunUntil,this.time+1*source.scale);this.effect(e,'착지 −'+Math.round(50*source.scale)+' · 기절!','skill')}}}
"""
if anchor not in s: raise SystemExit('robotSkill anchor missing')
s=s.replace(anchor,insert+anchor,1)

# Lizard tail stationary + lizard trigger in fighter updates
rep("if(f.id==='cursedhand'){this.cursedHandSkill(f,dt);return}", "if(f.id==='cursedhand'){this.cursedHandSkill(f,dt);return}\n if(f.id==='lizardtail'){f.vx=0;f.vy=0;return}\n if(f.id==='lizard')this.lizardSkill(f)")

# Boxer uppercut priority in collisions and avoid attacks while airborne
rep("collide(a,b){\n const d=distance(a,b)", "collide(a,b){\n if((a.airborneUntil||0)>this.time||(b.airborneUntil||0)>this.time)return;\n const d=distance(a,b)")
rep("if(!f.egg&&f.stunUntil<=this.time&&!['archer'", "if(f.id==='boxer'&&f.health>0&&f.stunUntil<=this.time&&this.boxerUppercut(f,e))continue;if(!f.egg&&f.stunUntil<=this.time&&!['archer'")
rep("'cursedhand','snowman','angryman'].includes(f.id)", "'cursedhand','snowman','angryman','lizardtail'].includes(f.id)")

# Reliable landing processing every simulation step
rep("step(dt){if(this.result!==null||dt<=0)return;this.stepRound(dt);", "step(dt){if(this.result!==null||dt<=0)return;this.updateAirborne();for(const f of this.fighters)if(f.id==='lizard')this.lizardSkill(f);this.stepRound(dt);")

# Ability text additions
rep("function ability(f){if(f.id==='aladdin')", "function ability(f){if(f.id==='lizard'){const t=engine.fighters.find(x=>x.id==='lizardtail'&&x.ownerSide===f.side&&x.health>0);return t?'🦎 꼬리 '+Math.ceil(t.health)+' / '+Math.ceil(t.hp)+' HP · 적 AI 집중':'🦎 HP 30% 이하에서 꼬리 소환'}if(f.id==='boxer')return '🥊 어퍼컷 '+Math.max(0,(f.boxerUpperNext||0)-engine.time).toFixed(1)+'초 · 125 + 착지 50';if(f.id==='aladdin')")

# Special attack sound for uppercut
rep("if(tx.includes('거대검격'))key='giantslash';", "if(tx.includes('어퍼컷'))key='uppercut';else if(tx.includes('거대검격'))key='giantslash';")
rep("if(key==='giantslash'){", "if(key==='uppercut'){sfxSweep(260,78,.11,.05,'sawtooth');sfxNoise(.07,.05,1500);tone(82,.13,.075,'sine')}\n else if(key==='giantslash'){")

# static sanity strings
for needle in ["BATTLE <b>v3.28</b>","moonUltAt:35/scale","id:'lizard'","spawnLizardTail(owner)","boxerUppercut(f,e)","알라딘: 본체 AI"]:
    if needle not in s: raise SystemExit('postcheck missing '+needle)

p.write_text(s,encoding='utf-8')
print('V328_PATCH_OK')

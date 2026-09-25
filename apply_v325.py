from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if s.count(old)<count:
        raise SystemExit(f'PATCH FAILED: {label} ({s.count(old)}/{count})')
    s=s.replace(old,new,count)

def sub(pattern,repl,label,count=1):
    global s
    ns,n=re.subn(pattern,repl,s,count=count,flags=re.S)
    if n!=count:
        raise SystemExit(f'PATCH FAILED: {label} ({n}/{count})')
    s=ns

# ---------------- v3.25 version / notes ----------------
rep('BATTLE <b>v3.24</b>','BATTLE <b>v3.25</b>','version badge')
rep('📒 패치노트 · v3.24','📒 패치노트 · v3.25','patch summary')
anchor='<div class="patch-body"><div class="patch-version"><h3>v3.24 · 스테이지 모드 테스트 & 밸런스</h3>'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.25 · 악마의 눈 & 경찰 밸런스</h3><ul><li>경찰 총 난사 지속시간 3초 → 5초.</li><li>신규 캐릭터 🧿 악마의 눈: 기본 체력 666. 몸에 닿은 적에게 저주를 부여.</li><li>저주: 0.3초마다 피해 10. 모아이·로봇 등 기존 상태이상 면역을 무시하며 전투 중 지속.</li><li>저주받은 대상은 4초마다 🪬 저주받은 손을 소환. 손은 5초 유지, 체력 113, 유도 저주탄을 발사.</li><li>악마의 눈은 13초마다 저주받은 손을 직접 소환. 보스 악마의 눈의 손은 보스 배율을 1.5배만 적용.</li></ul></div><div class="patch-version"><h3>v3.24 · 스테이지 모드 테스트 & 밸런스</h3>'
rep(anchor,insert,'v325 notes')

# ---------------- Police barrage 3s -> 5s ----------------
rep("description:'1초마다 테이저건을 발사해 피해 30과 0.2초 기절을 줘. 체력이 30% 이하가 되면 경기당 1회, 3초 동안 조준 없이 무작위 방향으로 총을 연속 발사해.'",
    "description:'1초마다 테이저건을 발사해 피해 30과 0.2초 기절을 줘. 체력이 30% 이하가 되면 경기당 1회, 5초 동안 조준 없이 무작위 방향으로 총을 연속 발사해.'",
    'police description')
rep("HP 30% 이하 1회 총 난사 · 3초 동안 0.38초마다 1발", "HP 30% 이하 1회 총 난사 · 5초 동안 0.38초마다 1발", 'police detail')
rep("f.policeBarrageUntil=this.time+3;", "f.policeBarrageUntil=this.time+5;", 'police barrage timer')
rep("this.effect(f,'🔫 총 난사!','skill');this.emit('👮‍♂️ 경찰이 3초간 총 난사를 시작!')", "this.effect(f,'🔫 총 난사!','skill');this.emit('👮‍♂️ 경찰이 5초간 총 난사를 시작!')", 'police barrage event')

# ---------------- Devil Eye roster ----------------
aladdin="{id:'aladdin',name:'알라딘',icon:'👳‍♀️',tag:'지니 소환 · 회전팔 · 2회 부활',hp:500,damage:50,speed:165,cooldown:0,description:'전투 시작과 동시에 체력 1500의 🧞‍♂️ 지니를 소환해. 지니는 3초마다 1초 동안 파란 팔을 몸 주위로 빠르게 회전시켜 관통 피해 125를 줘. 지니가 쓰러지면 최대 2회 부활하며, 부활할 때마다 알라딘의 최대/현재 체력과 지니 공격력이 절반이 돼.',detail:'알라딘 HP 500 · 지니 HP 1500 · 회전팔 125 / 3초 · 유지 1초 · 관통 · 공격 1회당 대상별 1회 피격 · 지니 최대 2회 부활 · 부활마다 알라딘 체력 및 지니 공격력 1/2 · 알라딘 사망 시 지니와 무관하게 패배'}"
devileye="{id:'devileye',name:'악마의 눈',icon:'🧿',tag:'저주 · 저주받은 손',hp:666,damage:0,speed:155,cooldown:0,description:'몸에 닿은 적에게 저주를 부여해. 저주는 상태이상 면역을 무시하고 0.3초마다 피해 10을 주며, 저주받은 대상은 4초마다 🪬 저주받은 손을 불러내. 악마의 눈도 13초마다 손을 직접 소환해.',detail:'HP 666 · 접촉 시 저주 · 저주 피해 10 / 0.3초 · 저주 대상 손 소환 4초마다 · 손 HP 113 · 유지 5초 · 유도 저주탄 · 본체 손 소환 13초마다'}"
rep(aladdin+'\n];',aladdin+',\n'+devileye+'\n];','devileye roster')

# ---------------- Main fighter state ----------------
rep("poison:null,toxin:null,slashCd:0", "poison:null,toxin:null,curse:null,nextCursedHand:type.id==='devileye'?13/scale:9999,slashCd:0", 'devileye main state')

# ---------------- Curse + cursed hand implementation ----------------
anchor_skill="robotSkill(f,dt){"
curse_code=r'''applyCurse(source,e){
 if(!source||!e||source.team===e.team||e.health<=0||this.isStudying(e)||e.id==='cursedhand')return false;
 const root=source.id==='cursedhand'?this.fighters[source.ownerSide]:source,ownerSide=root?root.side:source.side,team=root?root.team:source.team;
 if(e.curse&&e.curse.team===team)return false;
 e.curse={ownerSide,team,next:this.time+.3,nextHand:this.time+4};this.effect(e,'🧿 저주!','curse');this.emit('🧿 '+e.name+' 저주!');return true
}
tickCurse(e){
 const c=e.curse;if(!c||e.health<=0)return;
 while(c.next<=this.time+1e-9){c.next+=.3;if(this.isStudying(e))continue;const owner=this.fighters[c.ownerSide];const n=Math.min(e.health,Math.max(0,Math.round(10*(1-e.armor))));e.health-=n;if(owner)owner.damageDealt+=n;this.effect(e,'저주 −'+n,'curse');if(this.formEgg(e))return;if(e.health===0){e.curse=null;e.trail=[];this.emit(e.name+' 저주로 탈락!');this.checkEnd();return}}
 while(e.curse&&c.nextHand<=this.time+1e-9&&e.health>0){c.nextHand+=4;const owner=this.fighters[c.ownerSide];if(owner)this.spawnCursedHand(owner,e)}
}
spawnCursedHand(owner,near=null){
 if(!owner)return null;const hs=owner.boss?1.5:1,hp=113*hs,side=this.fighters.length,angle=this.rand(-Math.PI,Math.PI),base=near||owner,x=clamp(base.x+this.rand(-65,65),55,665),y=clamp(base.y+this.rand(-65,65),55,665),h={id:'cursedhand',name:'저주받은 손',icon:'🪬',tag:'유도 저주탄',description:'유도 투사체로 적에게 저주를 퍼뜨리는 소환수.',detail:'',side,team:owner.team,boss:owner.boss,scale:hs,handScale:hs,bodyScale:hs,radius:25*hs,hp,health:hp,damage:0,armor:0,lifesteal:0,rootSlowStrength:0,magicSlowStrength:0,speed:145*hs,cooldown:1.5/hs,x,y,vx:Math.cos(angle),vy:Math.sin(angle),attack:0,cd:.55/hs,skill:0,turn:0,dash:0,dashHit:false,awakened:false,revivals:0,heroReady:false,vampireBat:false,dodgeChance:0,knightShieldNext:0,knightShieldChargedUntil:0,knightShieldAngle:0,knightBlockedDamage:0,policeBarrageUsed:false,policeBarrageUntil:0,policeBarrageCd:0,nextJump:0,jumpFx:0,moonHalf:false,moonShot:null,moonUltStarted:false,moonUltAt:9999,moonUltLandAt:0,moonUltPhase:'',egg:false,eggUntil:0,stunUntil:0,burn:null,peckCd:0,flameCd:0,captureTarget:null,capturedBy:null,nextCapture:9999,venom:null,webAnchor:null,webs:[],webHits:{},studyUntil:0,nextStudy:9999,studyStart:0,minDamage:0,maxDamage:0,letterIndex:0,poison:null,toxin:null,curse:null,nextCursedHand:9999,slashCd:0,slashFx:0,slashAngle:0,idle:0,forgeLevel:0,forgeInterval:1,rootLength:0,rootGrowth:0,rootHits:{},rootSlow:0,rootSlowPower:0,slow:0,slowPower:0,flash:0,damageDealt:0,hits:0,healed:0,trail:[],summon:true,ownerSide:owner.side,expiresAt:this.time+5};this.fighters.push(h);this.effect(h,'🪬 소환!','curse');return h
}
devilEyeSkill(f){if(f.id!=='devileye'||f.health<=0||f.stunUntil>this.time)return;if(this.time>=f.nextCursedHand-1e-9){f.nextCursedHand=this.time+13/f.scale;this.spawnCursedHand(f,f);this.effect(f,'🪬 저주받은 손!','skill')}}
cursedHandSkill(h,dt){
 if(h.id!=='cursedhand'||h.health<=0)return;if(this.time>=h.expiresAt-1e-9){h.health=0;h.trail=[];return}if(h.stunUntil>this.time)return;h.cd=Math.max(0,h.cd-dt);const e=this.nearest(h);if(!e)return;const a=this.aim(h,e),d=distance(h,e);if(d>205*h.scale){h.vx=a.x;h.vy=a.y;h.x+=h.vx*h.speed*dt;h.y+=h.vy*h.speed*dt;this.keepInside(h)}else if(d<125*h.scale){h.vx=-a.x;h.vy=-a.y;h.x+=h.vx*h.speed*.6*dt;h.y+=h.vy*h.speed*.6*dt;this.keepInside(h)}if(h.cd<=1e-9){h.cd=h.cooldown;this.shots.push({x:h.x+a.x*(h.radius+6),y:h.y+a.y*(h.radius+6),vx:a.x,vy:a.y,owner:h.side,team:h.team,target:e.side,kind:'curseorb',radius:8*h.scale,speed:230*h.scale,damage:0,life:4,bounces:0,curseOnly:true});h.attack=.18/h.scale;this.effect(h,'🧿 저주탄!','curse')}}
'''+anchor_skill
rep(anchor_skill,curse_code,'curse methods')

# Curse ticks alongside other DOTs.
old_status="for(const f of this.fighters){if(f.health>0)this.tickPoison(f);if(this.result!==null)return;if(f.health>0)this.tickToxin(f);if(this.result!==null)return;if(f.health>0)this.tickBurn(f);if(this.result!==null)return;}"
new_status="for(const f of this.fighters){if(f.health>0)this.tickPoison(f);if(this.result!==null)return;if(f.health>0)this.tickToxin(f);if(this.result!==null)return;if(f.health>0)this.tickBurn(f);if(this.result!==null)return;if(f.health>0)this.tickCurse(f);if(this.result!==null)return;}"
rep(old_status,new_status,'curse tick hook')

# Cursed hand custom AI; Devil Eye keeps normal movement but runs summon timer.
needle="stepFighter(f,e,dt){\n if(f.id==='genie'){this.genieSkill(f,dt);return}"
replacement="stepFighter(f,e,dt){\n if(f.id==='genie'){this.genieSkill(f,dt);return}\n if(f.id==='cursedhand'){this.cursedHandSkill(f,dt);return}\n if(f.id==='devileye')this.devilEyeSkill(f)"
rep(needle,replacement,'devileye step hooks')

# Contact curse and no generic melee for Devil Eye / hand.
rep("if(f.id==='spider'&&f.health>0&&f.stunUntil<=this.time)this.applyPoison(f,e);if(f.id==='puffer'&&f.health>0&&f.stunUntil<=this.time)this.applyPoison(f,e);",
    "if(f.id==='spider'&&f.health>0&&f.stunUntil<=this.time)this.applyPoison(f,e);if(f.id==='puffer'&&f.health>0&&f.stunUntil<=this.time)this.applyPoison(f,e);if(f.id==='devileye'&&f.health>0&&f.stunUntil<=this.time)this.applyCurse(f,e);",
    'contact curse')
rep("'robot','aladdin','genie'].includes(f.id)", "'robot','aladdin','genie','devileye','cursedhand'].includes(f.id)", 'contact melee exclusion')

# Curse-only homing projectiles do not deal direct impact damage; they apply curse.
rep("attackProjectile(f,e,s){if(this.isStudying(e))return;const cd=f.cd,attack=f.attack;",
    "attackProjectile(f,e,s){if(this.isStudying(e))return;if(s.curseOnly){this.applyCurse(f,e);return}const cd=f.cd,attack=f.attack;",
    'curse projectile application')
rep("if(s.kind==='magic'&&target){", "if((s.kind==='magic'||s.kind==='curseorb')&&target){", 'curse projectile homing')

# Curse orb drawing.
rep("else if(s.kind==='taser'){ctx.strokeStyle='#ffe66d';",
    "else if(s.kind==='curseorb'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(24*s.radius/8)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🧿',0,0)}else if(s.kind==='taser'){ctx.strokeStyle='#ffe66d';",
    'curse orb visual')

# Curse status ring and hand label.
rep("if((f.poison||f.burn)&&f.health>0){ctx.strokeStyle=f.burn?'#ff8a39':'#b2f35f';ctx.lineWidth=4;ctx.beginPath();ctx.arc(f.x,f.y,r+6,0,Math.PI*2);ctx.stroke()}",
    "if((f.poison||f.burn)&&f.health>0){ctx.strokeStyle=f.burn?'#ff8a39':'#b2f35f';ctx.lineWidth=4;ctx.beginPath();ctx.arc(f.x,f.y,r+6,0,Math.PI*2);ctx.stroke()}if(f.curse&&f.health>0){ctx.strokeStyle='#b78cff';ctx.lineWidth=4;ctx.beginPath();ctx.arc(f.x,f.y,r+11,0,Math.PI*2);ctx.stroke()}",
    'curse status visual')
rep("(f.id==='genie'?(f.boss?'BOSS 지니':'지니'):(f.boss?'BOSS':isBossMode()?f.side+'번':f.team?'R':'L'))+' · '+f.name",
    "(f.id==='genie'?(f.boss?'BOSS 지니':'지니'):f.id==='cursedhand'?'소환수':(f.boss?'BOSS':isBossMode()?f.side+'번':f.team?'R':'L'))+' · '+f.name",
    'cursed hand label')

# HUD shows curse state on primary fighter.
rep("+(f.toxin?' · 맹독 '+Math.max(0,Math.ceil(f.toxin.expires-engine.time))+'초':'');",
    "+(f.toxin?' · 맹독 '+Math.max(0,Math.ceil(f.toxin.expires-engine.time))+'초':'')+(f.curse?' · 🧿 저주':'');",
    'curse hud')

# Boss rules: cursed hands only get x1.5, not ordinary boss summon scaling.
rep('보스 알라딘의 지니는 체력 3750이며 회전팔 피해 200, 공격 주기 1.5초 등 보스 능력 배율을 함께 적용받아.',
    '보스 알라딘의 지니는 체력 3750이며 회전팔 피해 200, 공격 주기 1.5초 등 보스 능력 배율을 함께 적용받아. 보스 악마의 눈이 소환하는 🪬 저주받은 손은 일반 보스 배율 대신 모든 손 능력치에 1.5배만 적용돼.',
    'boss devil eye rule')

p.write_text(s,encoding='utf-8')
print('NEON RUMBLE v3.25 applied')

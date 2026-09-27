from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(label+' anchor missing')
    s=s.replace(old,new,count)

# v3.49 labels
rep('BATTLE <b>v3.48</b>','BATTLE <b>v3.49</b>','version')
rep('📒 패치노트 · v3.48','📒 패치노트 · v3.49','patch title')

marker='<div class="patch-body">'
patch='''<div class="patch-version"><h3>v3.49 · 밸런스 패치 & 슬롯머신</h3><ul><li>🧌 법사좀비: 샌드박스 유도탄 피해 85 → 60. CHAPTER 3 STAGE 3은 피해 85 유지.</li><li>🕵️‍♂️ 탐정: 범인 잡기의 15% 결과를 기절 3초로 변경.</li><li>🔎 돋보기: 아군은 확대되지 않으며, 한 대상은 2초 동안 1회만 확대. 여러 탐정이 맞혀도 중첩·시간 연장 없이 원래 크기로 복귀.</li><li>🎰 신규 캐릭터 슬롯머신 추가. 상점에서 777코인으로 영구 구매.</li><li>🎰 뽑기: 50% 랜덤 이모티콘 3연사(5~10), 30% 🍇 3연사(10~30), 15% 🪙 10~20발(10~20), 5% 숫자 7 3연사(77, 일반보다 1.7배 빠름).</li></ul></div>'''
if marker not in s: raise SystemExit('patch body missing')
s=s.replace(marker,marker+patch,1)

# Zombie Mage: sandbox 60
zr_old="{id:'zombie_mage',name:'법사좀비',icon:'🧌',tag:'유도탄 · 미니좀비 소환',hp:1000,damage:85,speed:105,cooldown:2,unlock:'zombieMage',description:'이동속도가 느리고 몸집이 큰 법사좀비. 2초마다 피해 85의 유도탄을 발사하며 적중 시 HP 10의 미니좀비를 소환한다.',detail:'HP 1000 · 이동속도 -30% · 크기 1.5배 · 유도탄 85 / 2초 · 명중 시 HP 10 미니좀비 · 미니좀비 피해 5~20'},"
zr_new="{id:'zombie_mage',name:'법사좀비',icon:'🧌',tag:'유도탄 · 미니좀비 소환',hp:1000,damage:60,speed:105,cooldown:2,unlock:'zombieMage',description:'샌드박스에서는 2초마다 피해 60의 유도탄을 발사하며 적중 시 HP 10의 미니좀비를 소환한다.',detail:'HP 1000 · 이동속도 -30% · 크기 1.5배 · 유도탄 60 / 2초 · 명중 시 HP 10 미니좀비 · 미니좀비 피해 5~20'},"
rep(zr_old,zr_new,'zombie roster')

slot="{id:'slotmachine',name:'슬롯머신',icon:'🎰',tag:'뽑기 돌리기',hp:1000,damage:10,speed:145,cooldown:2.5,unlock:'slotMachineShop',description:'2.5초마다 뽑기를 돌려 확률에 따라 다양한 투사체를 연속으로 던진다.',detail:'HP 1000 · 뽑기 2.5초 · 이모티콘 3발 5~10 · 🍇 3발 10~30 · 🪙 10~20발 10~20 · 7 세 발 피해 77 / 속도 ×1.7'},\n"
s=s.replace(zr_new,slot+zr_new,1)

# Zombie Mage projectile: robust replacement around its branch
pat=re.compile(r"if\(f\.id==='zombie_mage'\)\{\s*if\(f\.cd<=1e-9&&e&&e\.health>0\)\{const a=this\.aim\(f,e\);this\.shots\.push\(\{x:f\.x\+a\.x\*\(f\.radius\+8\),y:f\.y\+a\.y\*\(f\.radius\+8\),vx:a\.x,vy:a\.y,owner:f\.side,team:f\.team,target:e\.side,kind:'zombiemagic',radius:8\*f\.scale,speed:215\*f\.scale,damage:85\*f\.scale,life:5\*f\.scale,bounces:0\}\);f\.cd=2/f\.scale;f\.attack=\.2/f\.scale;this\.effect\(f,'🧌 85 유도탄!','skill'\)\}\s*return\s*\}")
replacement="if(f.id==='zombie_mage'){if(f.cd<=1e-9&&e&&e.health>0){const a=this.aim(f,e),zd=Number.isFinite(f.zombieMageDamage)?f.zombieMageDamage:60;this.shots.push({x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'zombiemagic',radius:8*f.scale,speed:215*f.scale,damage:zd*f.scale,life:5*f.scale,bounces:0});f.cd=2/f.scale;f.attack=.2/f.scale;this.effect(f,'🧌 '+zd+' 유도탄!','skill')}return}"
s,n=pat.subn(replacement,s,count=1)
if n!=1: raise SystemExit('zombie skill regex missing')

# Chapter 3 stage 3 remains damage 85
rep('m.hp=2000;m.health=2000;m.bodyScale=1.5;m.radius=49.5;m.speed=105;spawnFemaleVampire();spawnMansionGhost()','m.hp=2000;m.health=2000;m.bodyScale=1.5;m.radius=49.5;m.speed=105;m.zombieMageDamage=85;spawnFemaleVampire();spawnMansionGhost()','stage mage')

# Detective 15% outcome -> stun 3s only
rep("}else if(r<.20){\n    e.health=Math.max(0,e.health-100*f.scale);\n    e.stunUntil=Math.max(e.stunUntil||0,this.time+10/f.scale);\n    this.effect(e,'🚔 기절 10초 + 피해 100!','skill');","}else if(r<.20){\n    e.stunUntil=Math.max(e.stunUntil||0,this.time+3/f.scale);\n    this.effect(e,'🚔 기절 3초!','skill');",'detective 15')

# Detective magnifier: enemy only, no stacking and no timer refresh
rep("if(s.kind==='magnifier'&&e.health>0&&!e.boss){if(!((e.magnifiedUntil||0)>this.time)){e.magnifyBaseRadius=e.radius;e.radius*=2}e.magnifiedUntil=this.time+2;this.effect(e,'🔎 확대 2초!','skill')}","if(s.kind==='magnifier'&&e.health>0&&!e.boss&&f.team!==e.team&&!((e.magnifiedUntil||0)>this.time)){e.magnifyBaseRadius=e.radius;e.radius*=2;e.magnifiedUntil=this.time+2;this.effect(e,'🔎 확대 2초!','skill')}",'magnifier')

# Slot Machine skill
needle='moneyManSkill(f,e){'
if needle not in s: raise SystemExit('money skill missing')
slot_skill=r'''slotMachineSkill(f,e){
 if(f.id!=='slotmachine'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0)return;
 if(!Array.isArray(f.slotQueue))f.slotQueue=[];
 while(f.slotQueue.length&&f.slotQueue[0].fireAt<=this.time+1e-9){
  const q=f.slotQueue.shift(),target=this.nearest(f)||e;if(!target||target.health<=0)continue;
  const base=this.aim(f,target),ang=Math.atan2(base.y,base.x)+(q.spread?this.rand(-q.spread,q.spread):0),vx=Math.cos(ang),vy=Math.sin(ang);
  this.shots.push({x:f.x+vx*(f.radius+8),y:f.y+vy*(f.radius+8),vx,vy,owner:f.side,team:f.team,target:target.side,kind:q.kind,icon:q.icon,radius:8*f.scale,speed:q.speed*f.scale,damage:q.damage*f.scale,life:4,bounces:0});f.attack=.12/f.scale;
 }
 if(f.slotQueue.length||f.cd>1e-9)return;
 const r=this.random(),normalSpeed=320;
 if(r<.05){for(let i=0;i<3;i++)f.slotQueue.push({fireAt:this.time+i*.12/f.scale,kind:'slotseven',icon:'7',damage:77,speed:normalSpeed*1.7,spread:.04});this.effect(f,'🎰 777!','skill')}
 else if(r<.20){const n=Math.floor(this.rand(10,21));for(let i=0;i<n;i++)f.slotQueue.push({fireAt:this.time+i*.05/f.scale,kind:'slotcoin',icon:'🪙',damage:Math.floor(this.rand(10,21)),speed:normalSpeed,spread:.12});this.effect(f,'🎰 🪙 JACKPOT!','skill')}
 else if(r<.50){for(let i=0;i<3;i++)f.slotQueue.push({fireAt:this.time+i*.12/f.scale,kind:'slotgrape',icon:'🍇',damage:Math.floor(this.rand(10,31)),speed:normalSpeed,spread:.05});this.effect(f,'🎰 🍇🍇🍇','skill')}
 else{const emojiPool=[...new Set(ROSTER.map(c=>c.icon).filter(Boolean))];for(let i=0;i<3;i++)f.slotQueue.push({fireAt:this.time+i*.12/f.scale,kind:'slotemoji',icon:emojiPool[Math.floor(this.random()*emojiPool.length)]||'🎲',damage:Math.floor(this.rand(5,11)),speed:normalSpeed,spread:.06});this.effect(f,'🎰 이모티콘!','skill')}
 f.cd=2.5/f.scale;
}
'''
s=s.replace(needle,slot_skill+needle,1)

rep("if(f.id==='moneyman')this.moneyManSkill(f,e);if(f.id==='detective'){this.detectiveJailSkill(f);this.detectiveSkill(f,e);}","if(f.id==='moneyman')this.moneyManSkill(f,e);if(f.id==='slotmachine')this.slotMachineSkill(f,e);if(f.id==='detective'){this.detectiveJailSkill(f);this.detectiveSkill(f,e);}",'slot hook')
rep("'firefighter','moneyman','alien'","'firefighter','moneyman','slotmachine','alien'",'melee exclusion')

# Shop purchase 777 coins
shop="{id:'moneyman',name:'머니맨',icon:'🤑',price:150,type:'character',exclusiveFor:null,desc:'구매하면 캐릭터 선택 화면에서 영구 사용 가능'},"
rep(shop,shop+"\n {id:'slotmachine',name:'슬롯머신',icon:'🎰',price:777,type:'character',exclusiveFor:null,desc:'구매하면 캐릭터 선택 화면에서 영구 사용 가능'},",'shop')

owned="function moneyManOwned(){try{const a=JSON.parse(localStorage.getItem('neonRumble.shopOwned.v1')||'[]');return Array.isArray(a)&&a.includes('moneyman')}catch{return false}}"
rep(owned,owned+"\nfunction slotMachineOwned(){try{const a=JSON.parse(localStorage.getItem('neonRumble.shopOwned.v1')||'[]');return Array.isArray(a)&&a.includes('slotmachine')}catch{return false}}",'owned helper')
rep("||(c?.unlock==='moneyManShop'&&!moneyManOwned())}","||(c?.unlock==='moneyManShop'&&!moneyManOwned())||(c?.unlock==='slotMachineShop'&&!slotMachineOwned())}",'character lock')

# Slot projectile rendering: insert between magnifier and alien laser
needle="}else if(s.kind==='alienlaser'){"
idx=s.find(needle,s.find("for(const s of engine.shots)"))
if idx<0: raise SystemExit('draw insertion point missing')
slot_draw="}else if(['slotemoji','slotgrape','slotcoin'].includes(s.kind)){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(Math.max(20,s.radius*2.8))+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(s.icon||'🎲',0,0)}else if(s.kind==='slotseven'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font='900 '+Math.max(22,s.radius*3)+'px system-ui';ctx.fillStyle=colors[s.team];ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('7',0,0)"
s=s[:idx]+slot_draw+s[idx+1:]

required=['BATTLE <b>v3.49</b>','v3.49 · 밸런스 패치 & 슬롯머신',"id:'slotmachine'","price:777,type:'character'",'slotMachineSkill(f,e){',"kind:'slotseven'",'normalSpeed*1.7','function slotMachineOwned()',"c?.unlock==='slotMachineShop'",'m.zombieMageDamage=85','zombieMageDamage)?f.zombieMageDamage:60',"f.team!==e.team&&!((e.magnifiedUntil||0)>this.time)","['slotemoji','slotgrape','slotcoin'].includes(s.kind)"]
missing=[x for x in required if x not in s]
if missing: raise SystemExit('missing markers '+repr(missing))

p.write_text(s,encoding='utf-8')
print('v3.49 applied')

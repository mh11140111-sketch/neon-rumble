from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(label+' anchor missing')
    s=s.replace(old,new,count)

# Version / patch notes
rep('BATTLE <b>v3.50</b>','BATTLE <b>v3.51</b>','version')
rep('📒 패치노트 · v3.50','📒 패치노트 · v3.51','patch title')
marker='<div class="patch-body">'
patch='''<div class="patch-version"><h3>v3.51 · 밸런스 · 배경 상점 · 꽃게</h3><ul><li>🛸👾 감염 UFO: 샌드박스 파멸의 레이저 주기 10초 → 8초.</li><li>🤑 머니맨: 💸 나는 돈 투사체 속도 증가.</li><li>🖼️ CHAPTER 2~5의 1·2·3 스테이지를 모두 클리어하면 해당 챕터 배경을 상점에서 1000코인으로 구매 가능. 구매한 배경은 옷장에서 장착.</li><li>🦀 신규 캐릭터 꽃게: 독립적으로 움직이는 집게발 2개, 접촉 피해 75. 10초마다 탈피해 HP 200 껍질을 남기고 집게 피해 +30. 탈피 후 10초 동안 받는 피해 ×10.</li></ul></div>'''
if patch not in s:
    rep(marker,marker+patch,'patch notes')

# Balance: infected UFO sandbox 8 sec; chapter stage already explicitly 8 sec.
rep("{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1250,damage:350,speed:105,cooldown:10,unlock:'infectedUfo',description:'샌드박스에서는 10초마다 아주 두꺼운 파멸의 레이저를 예고 후 발사해. 피해 350.',detail:'HP 1250 · 파멸의 레이저 350 / 10초 · 발사 전 1초 피격 예고 · 맵 관통'},",
    "{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1250,damage:350,speed:105,cooldown:8,unlock:'infectedUfo',description:'샌드박스에서는 8초마다 아주 두꺼운 파멸의 레이저를 예고 후 발사해. 피해 350.',detail:'HP 1250 · 파멸의 레이저 350 / 8초 · 발사 전 1초 피격 예고 · 맵 관통'},",'ufo roster')
rep("const doomInterval=f.doomInterval||10", "const doomInterval=f.doomInterval||8", 'ufo default interval')
rep("(f.doomNext||10)-engine.time", "(f.doomNext||8)-engine.time", 'ufo ability fallback')

# Money Man flying money speed increase 145 -> 230.
rep("kind:'flyingmoney',radius:10*f.scale,speed:145*f.scale,damage:100*f.scale", "kind:'flyingmoney',radius:10*f.scale,speed:230*f.scale,damage:100*f.scale", 'flying money speed')

# Crab roster after casino boss.
casino_end="{id:'casino_boss',name:'도박장 사장',icon:'🤵‍♂️',tag:'돈 투척 · 슬롯머신 소환',hp:800,damage:30,speed:130,cooldown:2,unlock:'casinoBoss',description:'2초마다 💵 돈을 여러 장 던져 장당 피해 30과 돈의 행복을 건다. 15초마다 HP 50의 움직이지 않는 슬롯머신을 6초 동안 소환한다.',detail:'HP 800 · 💵 장당 30 / 2초 · 일반 사용 최대 5장 · 15초마다 🎰 HP 50 소환 · 소환체 6초 유지'},"
crab="{id:'crab',name:'꽃게',icon:'🦀',tag:'쌍집게 · 탈피',hp:1000,damage:75,speed:150,cooldown:.6,description:'주위의 집게발 2개가 서로 겹치지 않게 독립적으로 움직이며 가장 가까운 적을 향해. 집게가 적에게 닿으면 피해 75. 10초마다 탈피해 HP 200 껍질을 남기고 집게 피해가 30 증가하지만, 탈피 후 10초 동안 받는 모든 피해가 10배가 돼.',detail:'HP 1000 · 집게 2개 · 접촉 75 · 탈피 10초 · 껍질 HP 200 · 탈피마다 집게 피해 +30 · 탈피 후 10초간 받는 피해 ×10'},"
if "id:'crab'" not in s:
    rep(casino_end,casino_end+'\n'+crab,'crab roster')

# Background shop items: chapter 2~5 only.
shop_anchor="{id:'slotmachine',name:'슬롯머신',icon:'🎰',price:777,type:'character',exclusiveFor:null,desc:'구매하면 캐릭터 선택 화면에서 영구 사용 가능'},"
bgs="""{id:'bg_desert',name:'사막 배경',icon:'🏜️',price:1000,type:'background',chapter:2,backgroundStyle:'desert',exclusiveFor:null,desc:'CHAPTER 2 스테이지 1·2·3 클리어 후 구매 가능'},
 {id:'bg_mansion',name:'피의 저택 배경',icon:'🏰',price:1000,type:'background',chapter:3,backgroundStyle:'mansion',exclusiveFor:null,desc:'CHAPTER 3 스테이지 1·2·3 클리어 후 구매 가능'},
 {id:'bg_space',name:'우주 배경',icon:'🪐',price:1000,type:'background',chapter:4,backgroundStyle:'space',exclusiveFor:null,desc:'CHAPTER 4 스테이지 1·2·3 클리어 후 구매 가능'},
 {id:'bg_casino',name:'도박장 배경',icon:'🎲',price:1000,type:'background',chapter:5,backgroundStyle:'casino',exclusiveFor:null,desc:'CHAPTER 5 스테이지 1·2·3 클리어 후 구매 가능'},"""
if "id:'bg_desert'" not in s:
    rep(shop_anchor,shop_anchor+'\n '+bgs,'background shop items')

# Persist chapter 5 completion for background eligibility.
rep("CASINO_BOSS_UNLOCK_KEY='neonRumble.casinoBossUnlocked.v1'", "CASINO_BOSS_UNLOCK_KEY='neonRumble.casinoBossUnlocked.v1',CASINO_STAGE_KEY='neonRumble.casinoStages.v1'", 'casino stage key')
rep("spaceStageMask=0,skeletonsUnlocked=false", "spaceStageMask=0,casinoStageMask=0,skeletonsUnlocked=false", 'casino stage var')
rep("spaceStageMask=Number(localStorage.getItem(SPACE_STAGE_KEY)||0)||0;", "spaceStageMask=Number(localStorage.getItem(SPACE_STAGE_KEY)||0)||0;casinoStageMask=Number(localStorage.getItem(CASINO_STAGE_KEY)||0)||0;", 'load casino stage mask')
anchor="function markSpaceStage(n){const before=chapter5Unlocked();spaceStageMask|=(1<<(n-1));try{localStorage.setItem(SPACE_STAGE_KEY,String(spaceStageMask))}catch{}updateChapter5UI();return !before&&chapter5Unlocked()}"
if anchor not in s: raise SystemExit('markSpaceStage missing')
if 'function markCasinoStage(n)' not in s:
    s=s.replace(anchor,anchor+"\nfunction markCasinoStage(n){casinoStageMask|=(1<<(n-1));try{localStorage.setItem(CASINO_STAGE_KEY,String(casinoStageMask))}catch{}renderShop();return (casinoStageMask&7)===7}",1)
# Record chapter 5 stage clears.
rep("else if(mode==='casino'&&engine.result===0){const coinReward=awardStageCoins(casinoStageNo),bossRoll=casinoStageNo===3?tryUnlockCasinoBoss():null;", "else if(mode==='casino'&&engine.result===0){const coinReward=awardStageCoins(casinoStageNo),bossRoll=casinoStageNo===3?tryUnlockCasinoBoss():null;markCasinoStage(casinoStageNo);", 'mark casino completion')

# Economy: global equipped background.
rep("EQUIP_RIGHT_AURA_KEY='neonRumble.equip.rightAura.v2'", "EQUIP_RIGHT_AURA_KEY='neonRumble.equip.rightAura.v2',EQUIP_BACKGROUND_KEY='neonRumble.equip.background.v1'", 'background key')
rep("let coins=0,ownedCosmetics=[],equippedAccessory=[null,null],equippedAura=[null,null],wardrobeSide=0;", "let coins=0,ownedCosmetics=[],equippedAccessory=[null,null],equippedAura=[null,null],equippedBackground=null,wardrobeSide=0;", 'background state')
rep("equippedAura[1]=localStorage.getItem(EQUIP_RIGHT_AURA_KEY)||null", "equippedAura[1]=localStorage.getItem(EQUIP_RIGHT_AURA_KEY)||null;equippedBackground=localStorage.getItem(EQUIP_BACKGROUND_KEY)||null", 'load background')
rep("if(equippedAura[i])localStorage.setItem(auraKeys[i],equippedAura[i]);else localStorage.removeItem(auraKeys[i])", "if(equippedAura[i])localStorage.setItem(auraKeys[i],equippedAura[i]);else localStorage.removeItem(auraKeys[i])}if(equippedBackground)localStorage.setItem(EQUIP_BACKGROUND_KEY,equippedBackground);else localStorage.removeItem(EQUIP_BACKGROUND_KEY);for(let i=2;i<2;i++){", 'save background')
# The replacement above inserts a harmless empty loop to absorb the original closing brace structure; clean exact pattern.
s=s.replace("for(let i=2;i<2;i++){}catch{}", "}catch{}",1)

# Add helpers after currentAura.
anchor="function currentAura(side){return equippedItem(side,'aura')}"
if anchor not in s: raise SystemExit('currentAura missing')
helpers="""
function currentBackground(){return SHOP_ITEMS.find(x=>x.id===equippedBackground&&x.type==='background')||null}
function backgroundUnlocked(item){if(!item||item.type!=='background')return true;return item.chapter===2?(desertStageMask&7)===7:item.chapter===3?(mansionStageMask&7)===7:item.chapter===4?(spaceStageMask&7)===7:item.chapter===5?(casinoStageMask&7)===7:false}
"""
if 'function currentBackground()' not in s:
    s=s.replace(anchor,anchor+helpers,1)

# Buying locked background prohibited.
rep("function buyCosmetic(id){const item=SHOP_ITEMS.find(x=>x.id===id);if(!item||ownedCosmetics.includes(id))return;if(coins<item.price)", "function buyCosmetic(id){const item=SHOP_ITEMS.find(x=>x.id===id);if(!item||ownedCosmetics.includes(id))return;if(item.type==='background'&&!backgroundUnlocked(item)){alert('해당 챕터 STAGE 1·2·3을 먼저 모두 클리어해야 해!');return}if(coins<item.price)", 'background buy gate')

# Equip background globally from wardrobe.
old="function equipCosmetic(id){if(id!==null&&!ownedCosmetics.includes(id))return;const item=id?SHOP_ITEMS.find(x=>x.id===id):null;if(!item||item.type==='character')return;const slot=item.type==='aura'?equippedAura:equippedAccessory;slot[wardrobeSide]=slot[wardrobeSide]===id?null:id;saveEconomy();renderWardrobe();renderShop()}"
new="function equipCosmetic(id){if(id!==null&&!ownedCosmetics.includes(id))return;const item=id?SHOP_ITEMS.find(x=>x.id===id):null;if(!item||item.type==='character')return;if(item.type==='background'){equippedBackground=equippedBackground===id?null:id;saveEconomy();renderWardrobe();renderShop();return}const slot=item.type==='aura'?equippedAura:equippedAccessory;slot[wardrobeSide]=slot[wardrobeSide]===id?null:id;saveEconomy();renderWardrobe();renderShop()}"
rep(old,new,'equip background')

# Shop renderer understands background + lock.
rep("const typeName=item.type==='character'?'캐릭터':item.type==='aura'?'아우라':'장신구';", "const typeName=item.type==='character'?'캐릭터':item.type==='aura'?'아우라':item.type==='background'?'배경':'장신구';", 'shop type')
rep("b.textContent=own?'보유 중':'구매';b.disabled=own;", "const locked=item.type==='background'&&!backgroundUnlocked(item);b.textContent=own?'보유 중':locked?'챕터 클리어 필요':'구매';b.disabled=own||locked;", 'shop background lock')

# Wardrobe loadout and item handling.
rep("const acc=currentAccessory(wardrobeSide),aura=currentAura(wardrobeSide);", "const acc=currentAccessory(wardrobeSide),aura=currentAura(wardrobeSide),bg=currentBackground();", 'wardrobe bg current')
rep("+' · 아우라: '+(aura?aura.icon+' '+aura.name:'없음');", "+' · 아우라: '+(aura?aura.icon+' '+aura.name:'없음')+' · 배경: '+(bg?bg.icon+' '+bg.name:'기본');", 'wardrobe loadout bg')
# only the wardrobe occurrence remains after shop occurrence was already changed; replace first matching remaining aura/accessory ternary.
rep("const typeName=item.type==='aura'?'아우라':'장신구';", "const typeName=item.type==='aura'?'아우라':item.type==='background'?'배경':'장신구';", 'wardrobe type')
rep("const slot=item.type==='aura'?equippedAura:equippedAccessory,on=slot[wardrobeSide]===item.id;b.textContent=on?'장착 해제':'장착';", "const on=item.type==='background'?equippedBackground===item.id:(item.type==='aura'?equippedAura:equippedAccessory)[wardrobeSide]===item.id;b.textContent=on?'장착 해제':'장착';", 'wardrobe background on')

# Crab shell gets absolute targeting priority.
old="nearest(f){const es=this.enemies(f),tails=es.filter(e=>e.id==='lizardtail');const pool=tails.length?tails:es;return pool.reduce((a,b)=>!a||distance(f,b)<distance(f,a)?b:a,null)}"
new="nearest(f){const es=this.enemies(f),shells=es.filter(e=>e.id==='crab_shell'),tails=es.filter(e=>e.id==='lizardtail');const pool=shells.length?shells:tails.length?tails:es;return pool.reduce((a,b)=>!a||distance(f,b)<distance(f,a)?b:a,null)}"
rep(old,new,'shell target priority')

# Crab logic before casino boss skill.
needle='casinoBossSkill(f,e){'
if needle not in s: raise SystemExit('casinoBossSkill missing')
if 'crabSkill(f,e,dt){' not in s:
    crabskill=r'''spawnCrabShell(f){
 const sh={...f,id:'crab_shell',name:'꽃게 껍질',icon:'🦀',side:this.fighters.length,team:f.team,summon:true,ownerSide:f.side,boss:false,scale:1,bodyScale:.85,radius:28,hp:200,health:200,damage:0,speed:0,cooldown:999,x:f.x,y:f.y,vx:0,vy:0,attack:0,cd:999,stunUntil:0,poison:null,toxin:null,burn:null,curse:null,trail:[],deathOrder:null,crabClaws:null,crabShell:true};
 this.fighters.push(sh);this.effect(sh,'🦀 껍질 HP 200','skill');return sh
}
crabSkill(f,e,dt){
 if(f.id!=='crab'||f.health<=0)return;
 if(!Number.isFinite(f.clawDamage))f.clawDamage=75*f.scale;
 if(!Number.isFinite(f.crabMoltNext))f.crabMoltNext=this.time+10/f.scale;
 if(!Number.isFinite(f.crabVulnerableUntil))f.crabVulnerableUntil=0;
 if(!Array.isArray(f.crabClaws))f.crabClaws=[{x:f.x-48,y:f.y,side:-1,touch:null},{x:f.x+48,y:f.y,side:1,touch:null}];
 if(this.time>=f.crabMoltNext-1e-9&&this.time>=f.crabVulnerableUntil-1e-9){this.spawnCrabShell(f);f.clawDamage+=30*f.scale;f.crabVulnerableUntil=this.time+10/f.scale;f.crabMoltNext=f.crabVulnerableUntil;this.effect(f,'🦀 탈피! 집게 +30 · 피해 ×10','doom');this.emit('🦀 꽃게가 탈피! 껍질 HP 200 · 10초간 받는 피해 10배')}
 const target=e&&e.health>0?e:this.nearest(f);if(!target)return;
 const base=Math.atan2(target.y-f.y,target.x-f.x),orbit=52*f.scale,clawR=14*f.scale,speed=7*dt*f.scale;
 for(let i=0;i<2;i++){const c=f.crabClaws[i],want=base+(i===0?-.42:.42),tx=f.x+Math.cos(want)*orbit,ty=f.y+Math.sin(want)*orbit;c.x+=(tx-c.x)*Math.min(1,speed);c.y+=(ty-c.y)*Math.min(1,speed);}
 const a=f.crabClaws[0],b=f.crabClaws[1],dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1,min=clawR*2+3;if(d<min){const push=(min-d)/2,nx=dx/d,ny=dy/d;a.x-=nx*push;a.y-=ny*push;b.x+=nx*push;b.y+=ny*push}
 for(const c of f.crabClaws){const hit=this.enemies(f).filter(x=>x.health>0).sort((x,y)=>distance(c,x)-distance(c,y))[0];if(hit&&distance(c,hit)<=hit.radius+clawR){if(c.touch!==hit.side){this.attack(f,hit,f.clawDamage);c.touch=hit.side;this.effect(f,'🦀 집게 '+Math.round(f.clawDamage),'skill')}}else c.touch=null}
}
'''
    s=s.replace(needle,crabskill+needle,1)

# Hook crab skill and prevent normal attack/shell movement.
rep("if(f.id==='moneyman')this.moneyManSkill(f,e);if(f.id==='slotmachine')this.slotMachineSkill(f,e);if(f.id==='casino_boss')this.casinoBossSkill(f,e);", "if(f.id==='moneyman')this.moneyManSkill(f,e);if(f.id==='slotmachine')this.slotMachineSkill(f,e);if(f.id==='casino_boss')this.casinoBossSkill(f,e);if(f.id==='crab')this.crabSkill(f,e,dt);", 'crab skill hook')
rep("'firefighter','moneyman','slotmachine','casino_boss','alien'", "'firefighter','moneyman','slotmachine','casino_boss','crab','crab_shell','alien'", 'crab generic attack exclusion')
rep("for(const f of this.fighters){if(f.health<=0)continue;if((f.cowUntil||0)>this.time)", "for(const f of this.fighters){if(f.health<=0)continue;if(f.id==='crab_shell'){f.vx=0;f.vy=0;continue}if((f.cowUntil||0)>this.time)", 'shell stationary')

# Crab vulnerability: all standard attack damage x10.
rep("attack(f,e,dmg,friendly=false,bypassDodge=false){\n if(this.result!==null", "attack(f,e,dmg,friendly=false,bypassDodge=false){\n if(e&&e.id==='crab'&&(e.crabVulnerableUntil||0)>this.time)dmg*=10;\n if(this.result!==null", 'crab vulnerability attack')
# burn damage direct path also x10.
rep("const n=Math.min(e.health,Math.round(p.damage*(e.id==='snowman'?5:e.id==='tree'?2:1)*(1-e.armor)));", "const n=Math.min(e.health,Math.round(p.damage*(e.id==='snowman'?5:e.id==='tree'?2:1)*(e.id==='crab'&&(e.crabVulnerableUntil||0)>this.time?10:1)*(1-e.armor)));", 'crab vulnerability burn')

# Ability HUD for crab.
rep("if(f.id==='casino_boss')return '🤵‍♂️", "if(f.id==='crab')return '🦀 집게 '+Math.round(f.clawDamage||75)+' · 탈피 '+Math.max(0,(f.crabMoltNext||10)-engine.time).toFixed(1)+'초'+((f.crabVulnerableUntil||0)>engine.time?' · ⚠️ 피해×10 '+(f.crabVulnerableUntil-engine.time).toFixed(1)+'초':'');if(f.id==='casino_boss')return '🤵‍♂️", 'crab ability')

# Draw equipped background on non-stage arena modes.
old="function draw(){if(!engine)return;ctx.clearRect(0,0,720,720);if(mode==='desert'){"
new=r'''function draw(){if(!engine)return;ctx.clearRect(0,0,720,720);const wardrobeBg=currentBackground();if(wardrobeBg&&!['stage','desert','mansion','space','casino'].includes(mode)){const st=wardrobeBg.backgroundStyle;if(st==='desert'){const g=ctx.createLinearGradient(0,0,0,720);g.addColorStop(0,'#e8b85f');g.addColorStop(.55,'#cf9447');g.addColorStop(1,'#b97838');ctx.fillStyle=g;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.35;ctx.font='42px sans-serif';ctx.fillText('🌵',90,180);ctx.fillText('🌵',640,590);ctx.globalAlpha=1}else if(st==='mansion'){const g=ctx.createLinearGradient(0,0,0,720);g.addColorStop(0,'#241327');g.addColorStop(.55,'#130d1b');g.addColorStop(1,'#090811');ctx.fillStyle=g;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.28;ctx.font='46px sans-serif';ctx.fillText('🕯️',92,170);ctx.fillText('🕸️',625,160);ctx.fillText('🪦',625,595);ctx.globalAlpha=1}else if(st==='space'){const g=ctx.createLinearGradient(0,0,0,720);g.addColorStop(0,'#07162c');g.addColorStop(.55,'#0b1532');g.addColorStop(1,'#160d2d');ctx.fillStyle=g;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.55;ctx.font='24px sans-serif';ctx.fillText('✦',95,125);ctx.fillText('✧',610,165);ctx.fillText('✦',565,585);ctx.fillText('✧',145,610);ctx.globalAlpha=1}else{const g=ctx.createLinearGradient(0,0,0,720);g.addColorStop(0,'#30110f');g.addColorStop(.5,'#130d18');g.addColorStop(1,'#07120c');ctx.fillStyle=g;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.34;ctx.font='42px "Apple Color Emoji","Segoe UI Emoji",sans-serif';ctx.fillText('🎰',92,150);ctx.fillText('🎲',625,170);ctx.fillText('♠️',105,600);ctx.fillText('♦️',615,590);ctx.globalAlpha=1}}else if(mode==='desert'){'''
rep(old,new,'equipped background draw')

# Draw crab claws before body drawing.
needle="if(f.id==='genie'&&f.health>0&&f.genieArmUntil>engine.time){"
if needle not in s: raise SystemExit('draw genie anchor missing')
clawdraw=r'''if(f.id==='crab'&&f.health>0&&Array.isArray(f.crabClaws)){ctx.save();ctx.strokeStyle='#ff796a';ctx.fillStyle='#e8493f';ctx.lineWidth=5*f.scale;for(const c of f.crabClaws){ctx.beginPath();ctx.moveTo(f.x,f.y);ctx.lineTo(c.x,c.y);ctx.stroke();ctx.beginPath();ctx.arc(c.x,c.y,14*f.scale,.35,Math.PI*2-.35);ctx.lineTo(c.x+5*f.scale,c.y);ctx.closePath();ctx.fill()}ctx.restore();}'''
s=s.replace(needle,clawdraw+needle,1)

# Shell visual distinction.
rep("else{ctx.fillText(f.icon,f.x,f.y+1)}", "else if(f.id==='crab_shell'){ctx.globalAlpha=.55;ctx.fillText('🦀',f.x,f.y+1);ctx.globalAlpha=1}else{ctx.fillText(f.icon,f.x,f.y+1)}", 'shell render')

# Verify stage 3 casino boss remains 1500 and chapter4 stage UFO remains 8.
required=[
 'BATTLE <b>v3.51</b>',"id:'crab'","id:'bg_desert'","id:'bg_casino'",'function currentBackground()','function backgroundUnlocked(item)','function markCasinoStage(n)','crabSkill(f,e,dt)','spawnCrabShell(f)','crabVulnerableUntil','speed:230*f.scale','doomInterval=f.doomInterval||8','boss.hp=1500;boss.health=1500','boss.doomInterval=8'
]
for x in required:
    if x not in s: raise SystemExit('missing marker: '+x)
if s==orig: raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('v3.51 patch applied')
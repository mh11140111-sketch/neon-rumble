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

# Version + patch notes
s=s.replace('BATTLE <b>v3.49</b>','BATTLE <b>v3.50</b>',1)
s=s.replace('📒 패치노트 · v3.49','📒 패치노트 · v3.50',1)
marker='<div class="patch-body">'
patch='''<div class="patch-version"><h3>v3.50 · 슬롯머신 밸런스 & CHAPTER 5</h3><ul><li>🎰 슬롯머신: 50% 이모티콘 피해 25~30, 30% 🍇 피해 30~50, 5% 숫자 7 발사 3개 → 7개, 공격 주기 2.5초 → 2초.</li><li>🕵️‍♂️ 탐정: 범인 잡기/직접 처치로 적 체력이 0이 되었을 때 승패 판정이 누락되던 문제 수정.</li><li>🎲 CHAPTER 5 · CASINO 추가. 주인공은 🤑 머니맨.</li><li>🤵‍♂️ 도박장 사장 추가. STAGE 3 클리어 시 17.7% 확률로 획득 가능. 일반 사용 시 돈 투척 최대 5장.</li></ul></div>'''
if marker not in s: raise SystemExit('patch marker missing')
if 'v3.50 · 슬롯머신 밸런스 & CHAPTER 5' not in s:
    s=s.replace(marker,marker+patch,1)

# Roster: slot machine balance
old="{id:'slotmachine',name:'슬롯머신',icon:'🎰',tag:'뽑기 돌리기',hp:1000,damage:10,speed:145,cooldown:2.5,unlock:'slotMachineShop',description:'2.5초마다 뽑기를 돌려 확률에 따라 다양한 투사체를 연속으로 던진다.',detail:'HP 1000 · 뽑기 2.5초 · 이모티콘 3발 5~10 · 🍇 3발 10~30 · 🪙 10~20발 10~20 · 7 세 발 피해 77 / 속도 ×1.7'},"
new="{id:'slotmachine',name:'슬롯머신',icon:'🎰',tag:'뽑기 돌리기',hp:1000,damage:30,speed:145,cooldown:2,unlock:'slotMachineShop',description:'2초마다 뽑기를 돌려 확률에 따라 다양한 투사체를 연속으로 던진다.',detail:'HP 1000 · 뽑기 2초 · 이모티콘 3발 25~30 · 🍇 3발 30~50 · 🪙 10~20발 10~20 · 7 일곱 발 피해 77 / 속도 ×1.7'},"
rep(old,new,'slot roster')
# Add casino boss roster
casino="{id:'casino_boss',name:'도박장 사장',icon:'🤵‍♂️',tag:'돈 투척 · 슬롯머신 소환',hp:1500,damage:30,speed:130,cooldown:2,unlock:'casinoBoss',description:'2초마다 💵 돈을 여러 장 던져 장당 피해 30과 돈의 행복을 건다. 15초마다 HP 50의 움직이지 않는 슬롯머신을 6초 동안 소환한다.',detail:'HP 1500 · 💵 장당 30 / 2초 · 일반 사용 최대 5장 · 15초마다 🎰 HP 50 소환 · 소환체 6초 유지'},\n"
if "id:'casino_boss'" not in s:
    rep(new,new+'\n'+casino,'casino roster insertion')

# Slot machine logic: damage ranges, 7 shots, 2 sec cooldown, stage damage scale
rep("damage:q.damage*f.scale,life:4", "damage:q.damage*f.scale*(f.slotDamageScale||1),life:4", 'slot damage scale')
rep("if(r<.05){for(let i=0;i<3;i++)f.slotQueue.push", "if(r<.05){for(let i=0;i<7;i++)f.slotQueue.push", 'slot seven count')
rep("damage:Math.floor(this.rand(10,31)),speed:normalSpeed", "damage:Math.floor(this.rand(30,51)),speed:normalSpeed", 'slot grape damage')
rep("damage:Math.floor(this.rand(5,11)),speed:normalSpeed", "damage:Math.floor(this.rand(25,31)),speed:normalSpeed", 'slot emoji damage')
rep("f.cd=2.5/f.scale;\n}", "f.cd=2/f.scale;\n}", 'slot cooldown')

# Detective direct death paths => standard attack pipeline so game can end
rep("e.health=0;\n    this.effect(e,'🚨 즉사!','skill');", "this.attack(f,e,1e9,false,true);\n    this.effect(e,'🚨 즉사!','skill');", 'detective instant')
rep("e.health=Math.max(0,e.health-100*f.scale);\n    e.stunUntil=Math.max(e.stunUntil||0,this.time+3/f.scale);", "this.attack(f,e,100*f.scale,false,true);\n    if(e.health>0)e.stunUntil=Math.max(e.stunUntil||0,this.time+3/f.scale);", 'detective 15 damage')
rep("e.health=Math.max(0,e.health-100*f.scale);\n    this.effect(e,'🚔 피해 100!','skill');", "this.attack(f,e,100*f.scale,false,true);\n    this.effect(e,'🚔 피해 100!','skill');", 'detective 30 damage')

# Casino boss engine skill
needle='moneyManSkill(f,e){'
if needle not in s: raise SystemExit('moneyManSkill missing')
if 'casinoBossSkill(f,e){' not in s:
    skill=r'''casinoBossSkill(f,e){
 if(f.id!=='casino_boss'||f.health<=0)return;
 if(!Number.isFinite(f.casinoSummonNext))f.casinoSummonNext=this.time+15/f.scale;
 for(const z of this.fighters.filter(x=>x.casinoSummon&&x.ownerSide===f.side&&x.health>0))if(this.time>=z.casinoExpireAt-1e-9){z.health=0;z.trail=[];this.effect(z,'🎰 사라짐','skill')}
 if(this.time>=f.casinoSummonNext-1e-9){
  f.casinoSummonNext=this.time+15/f.scale;
  const tmp=new Engine('moneyman','slotmachine',this.random,{mode:'control'}).fighters[1],a=this.rand(-Math.PI,Math.PI);
  tmp.side=this.fighters.length;tmp.team=f.team;tmp.summon=true;tmp.ownerSide=f.side;tmp.casinoSummon=true;tmp.casinoExpireAt=this.time+6/f.scale;tmp.hp=50;tmp.health=50;tmp.speed=0;tmp.x=clamp(f.x+Math.cos(a)*90,55,665);tmp.y=clamp(f.y+Math.sin(a)*90,55,665);tmp.vx=0;tmp.vy=0;tmp.trail=[];tmp.deathOrder=null;tmp.slotQueue=[];this.fighters.push(tmp);this.effect(f,'🎰 슬롯머신 소환!','skill');
 }
 if(f.stunUntil>this.time||!e||e.health<=0||f.cd>1e-9)return;
 const max=Math.max(1,Math.floor(Number.isFinite(f.casinoMoneyMax)?f.casinoMoneyMax:5)),count=1+Math.floor(this.random()*max),base=this.aim(f,e),ang0=Math.atan2(base.y,base.x);
 for(let i=0;i<count;i++){const ang=ang0+(i-(count-1)/2)*.07,vx=Math.cos(ang),vy=Math.sin(ang);this.shots.push({x:f.x+vx*(f.radius+8),y:f.y+vy*(f.radius+8),vx,vy,owner:f.side,team:f.team,target:e.side,kind:'casino_money',icon:'💵',radius:8*f.scale,speed:340*f.scale,damage:30*f.scale,life:4,bounces:0})}
 f.cd=2/f.scale;f.attack=.18/f.scale;this.effect(f,'💵 '+count+'장 투척!','skill')
}
'''
    s=s.replace(needle,skill+needle,1)
# hook skill
rep("if(f.id==='moneyman')this.moneyManSkill(f,e);if(f.id==='slotmachine')this.slotMachineSkill(f,e);", "if(f.id==='moneyman')this.moneyManSkill(f,e);if(f.id==='slotmachine')this.slotMachineSkill(f,e);if(f.id==='casino_boss')this.casinoBossSkill(f,e);", 'casino skill hook')
# no melee
rep("'firefighter','moneyman','slotmachine','alien'", "'firefighter','moneyman','slotmachine','casino_boss','alien'", 'casino melee exclusion')
# money happiness on casino cash
rep("if(s.kind==='cash'&&e.health>0)this.applyMoneyHappiness(e,1);", "if((s.kind==='cash'||s.kind==='casino_money')&&e.health>0)this.applyMoneyHappiness(e,1);", 'casino happiness')
# render casino money in existing money branch
rep("s.kind==='moneybag'||s.kind==='cash'||s.kind==='flyingmoney'", "s.kind==='moneybag'||s.kind==='cash'||s.kind==='flyingmoney'||s.kind==='casino_money'", 'casino money render')
rep("s.kind==='moneybag'?'💰':s.kind==='flyingmoney'?'💸':'💵'", "s.kind==='moneybag'?'💰':s.kind==='flyingmoney'?'💸':'💵'", 'money render ternary')

# Manual mode includes casino
rep("['control','stage','boss-control','desert','mansion','space'].includes(mode)", "['control','stage','boss-control','desert','mansion','space','casino'].includes(mode)", 'manual casino')
# unlock storage/state
old="const ROBOT_STAGE_KEY='neonRumble.robotStages.v1',SKELETON_UNLOCK_KEY='neonRumble.skeletonBundleUnlocked.v2',SKELETON_MAGE_UNLOCK_KEY='neonRumble.skeletonMageUnlocked.v1',DESERT_STAGE_KEY='neonRumble.desertStages.v1',MANSION_STAGE_KEY='neonRumble.mansionStages.v1',ZOMBIE_MAGE_UNLOCK_KEY='neonRumble.zombieMageUnlocked.v1',INFECTED_UFO_UNLOCK_KEY='neonRumble.infectedUfoUnlocked.v1',DETECTIVE_UNLOCK_KEY='neonRumble.detectiveUnlocked.v1',LEGACY_SKELETON_UNLOCK_KEY='neonRumble.skeletonUnlocked.v1';"
newk="const ROBOT_STAGE_KEY='neonRumble.robotStages.v1',SKELETON_UNLOCK_KEY='neonRumble.skeletonBundleUnlocked.v2',SKELETON_MAGE_UNLOCK_KEY='neonRumble.skeletonMageUnlocked.v1',DESERT_STAGE_KEY='neonRumble.desertStages.v1',MANSION_STAGE_KEY='neonRumble.mansionStages.v1',SPACE_STAGE_KEY='neonRumble.spaceStages.v1',ZOMBIE_MAGE_UNLOCK_KEY='neonRumble.zombieMageUnlocked.v1',INFECTED_UFO_UNLOCK_KEY='neonRumble.infectedUfoUnlocked.v1',DETECTIVE_UNLOCK_KEY='neonRumble.detectiveUnlocked.v1',CASINO_BOSS_UNLOCK_KEY='neonRumble.casinoBossUnlocked.v1',LEGACY_SKELETON_UNLOCK_KEY='neonRumble.skeletonUnlocked.v1';"
rep(old,newk,'unlock keys')
rep("let robotStageMask=0,desertStageMask=0,mansionStageMask=0,skeletonsUnlocked=false,skeletonMageUnlocked=false,zombieMageUnlocked=false,infectedUfoUnlocked=false,detectiveUnlocked=false;", "let robotStageMask=0,desertStageMask=0,mansionStageMask=0,spaceStageMask=0,skeletonsUnlocked=false,skeletonMageUnlocked=false,zombieMageUnlocked=false,infectedUfoUnlocked=false,detectiveUnlocked=false,casinoBossUnlocked=false;", 'unlock vars')
rep("mansionStageMask=Number(localStorage.getItem(MANSION_STAGE_KEY)||0)||0;", "mansionStageMask=Number(localStorage.getItem(MANSION_STAGE_KEY)||0)||0;spaceStageMask=Number(localStorage.getItem(SPACE_STAGE_KEY)||0)||0;", 'load space mask')
rep("detectiveUnlocked=localStorage.getItem(DETECTIVE_UNLOCK_KEY)==='1'", "detectiveUnlocked=localStorage.getItem(DETECTIVE_UNLOCK_KEY)==='1';casinoBossUnlocked=localStorage.getItem(CASINO_BOSS_UNLOCK_KEY)==='1'", 'load casino boss')
rep("function chapter4Unlocked(){return (mansionStageMask&7)===7}", "function chapter4Unlocked(){return (mansionStageMask&7)===7}\nfunction chapter5Unlocked(){return (spaceStageMask&7)===7}\nfunction markSpaceStage(n){const before=chapter5Unlocked();spaceStageMask|=(1<<(n-1));try{localStorage.setItem(SPACE_STAGE_KEY,String(spaceStageMask))}catch{}updateChapter5UI();return !before&&chapter5Unlocked()}", 'chapter5 funcs')
# casino boss unlock function
anchor="function tryUnlockDetective(){if(detectiveUnlocked)return 'already';if(Math.random()>=.03)return 'miss';detectiveUnlocked=true;try{localStorage.setItem(DETECTIVE_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}"
if anchor not in s: raise SystemExit('detective unlock function missing')
if 'function tryUnlockCasinoBoss()' not in s:
    s=s.replace(anchor,anchor+"\nfunction tryUnlockCasinoBoss(){if(casinoBossUnlocked)return 'already';if(Math.random()>=.177)return 'miss';casinoBossUnlocked=true;try{localStorage.setItem(CASINO_BOSS_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}",1)
rep("||(c?.unlock==='slotMachineShop'&&!slotMachineOwned())}", "||(c?.unlock==='slotMachineShop'&&!slotMachineOwned())||(c?.unlock==='casinoBoss'&&!casinoBossUnlocked)}", 'casino lock rule')

# HTML chapter 5 button and panel
htmlbtn='<button id="chapter4-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 4 · CHAPTER 3 STAGE 1·2·3 클리어 필요</button>'
rep(htmlbtn,htmlbtn+'<button id="chapter5-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 5 · CHAPTER 4 STAGE 1·2·3 클리어 필요</button>','chapter5 button')
panel='''<div id="casino-panel" class="stage-panel" hidden><p class="eyebrow">CHAPTER 5 · CASINO</p><h2>🎲 머니맨의 도박장</h2><p>🤑 머니맨을 직접 조작해 도박장을 돌파해. 슬롯머신 웨이브를 뚫고 마지막에는 🤵‍♂️ 도박장 사장과 싸워.</p><div class="stage-grid"><button class="stage-card" id="casino-1" type="button"><b>STAGE 1</b><span>🤑 VS 🎰×1~7</span><strong>행운의 첫 판</strong><small>HP 125, 모든 피해 20% 약화 슬롯머신이 웨이브마다 1~7마리. 총 5웨이브.</small></button><button class="stage-card" id="casino-2" type="button"><b>STAGE 2</b><span>🤑 VS 🎰×1~7</span><strong>끝나지 않는 잭팟</strong><small>STAGE 1과 동일하게 슬롯머신 1~7마리씩 총 5웨이브.</small></button><button class="stage-card" id="casino-3" type="button"><b>STAGE 3</b><span>🤑 VS 🤵‍♂️</span><strong>도박장 사장</strong><small>돈을 1~7장 던지고 15초마다 HP 50의 고정 슬롯머신을 6초간 소환하는 사장을 쓰러트려.</small></button></div></div>'''
hint='<p class="hint">일반 모드는 직접 조작 없는 자동 전투'
if hint not in s: raise SystemExit('hint insertion missing')
if 'id="casino-panel"' not in s:s=s.replace(hint,panel+hint,1)

# Chapter UI
anchor="function updateChapter4UI(){const b=$('chapter4-entry');if(!b)return;const ok=chapter4Unlocked();b.disabled=!ok;b.textContent=ok?'🪐 CHAPTER 4 · 외계인의 역습':'🔒 CHAPTER 4 · CHAPTER 3 STAGE 1·2·3 클리어 필요'}"
rep(anchor,anchor+"\nfunction updateChapter5UI(){const b=$('chapter5-entry');if(!b)return;const ok=chapter5Unlocked();b.disabled=!ok;b.textContent=ok?'🎲 CHAPTER 5 · 머니맨의 도박장':'🔒 CHAPTER 5 · CHAPTER 4 STAGE 1·2·3 클리어 필요'}",'chapter5 UI')
# stage selection visibility
old="const on=mode==='stage',desertSelect=mode==='desert-select',mansionSelect=mode==='mansion-select',spaceSelect=mode==='space-select',special=on||desertSelect||mansionSelect||spaceSelect;"
new="const on=mode==='stage',desertSelect=mode==='desert-select',mansionSelect=mode==='mansion-select',spaceSelect=mode==='space-select',casinoSelect=mode==='casino-select',special=on||desertSelect||mansionSelect||spaceSelect||casinoSelect;"
rep(old,new,'casino select state')
rep("$('chapter4-entry').hidden=special;", "$('chapter4-entry').hidden=special;$('chapter5-entry').hidden=special;", 'hide chapter5')
rep("$('space-panel').hidden=!spaceSelect;", "$('space-panel').hidden=!spaceSelect;$('casino-panel').hidden=!casinoSelect;", 'casino panel visibility')
rep("updateChapter2UI();updateChapter3UI();updateChapter4UI()", "updateChapter2UI();updateChapter3UI();updateChapter4UI();updateChapter5UI()", 'update chapter5 UI calls',2)
# updateSelection visibility
rep("const stageWas=mode==='stage'||mode==='desert-select'||mode==='mansion-select'||mode==='space-select';", "const stageWas=mode==='stage'||mode==='desert-select'||mode==='mansion-select'||mode==='space-select'||mode==='casino-select';", 'stageWas casino')
rep("$('chapter4-entry').hidden=false}", "$('chapter4-entry').hidden=false;$('chapter5-entry').hidden=false}", 'show chapter5')
# mode switching reset
rep("function switchRegularMode(next){if(mode==='desert'||mode==='desert-select')resetDesertTransient();if(mode==='mansion'||mode==='mansion-select')resetMansionTransient();engine=null;mode=next;updateSelection()}", "function switchRegularMode(next){if(mode==='desert'||mode==='desert-select')resetDesertTransient();if(mode==='mansion'||mode==='mansion-select')resetMansionTransient();if(mode==='space'||mode==='space-select')resetSpaceTransient();if(mode==='casino'||mode==='casino-select')resetCasinoTransient();engine=null;mode=next;updateSelection()}", 'switch reset casino')
# chapter 5 entry + buttons
anchor="$('chapter4-entry').onclick=()=>{if(!chapter4Unlocked())return;if(mode==='mansion'||mode==='mansion-select')resetMansionTransient();mode='space-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};"
rep(anchor,anchor+"\n$('chapter5-entry').onclick=()=>{if(!chapter5Unlocked())return;if(mode==='space'||mode==='space-select')resetSpaceTransient();mode='casino-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};",'chapter5 entry')
rep("$('space-3').onclick=()=>startSpaceStage(3);", "$('space-3').onclick=()=>startSpaceStage(3);$('casino-1').onclick=()=>startCasinoStage(1);$('casino-2').onclick=()=>startCasinoStage(2);$('casino-3').onclick=()=>startCasinoStage(3);", 'casino stage buttons')

# Chapter 5 stage logic inserted before start()
needle='function start(){'
if needle not in s: raise SystemExit('start function missing')
if 'function startCasinoStage(n)' not in s:
    casino_logic=r'''let casinoStageNo=1,casinoWave=0;
function resetCasinoTransient(){casinoStageNo=1;casinoWave=0;if(engine){engine.desertWaveMode=false;engine.casinoMode=false}}
function makeCasinoSlot(x,y,hp=125,damageScale=.8,stationary=false){const tmp=new Engine('moneyman','slotmachine',Math.random,{mode:'control'}).fighters[1];tmp.side=engine.fighters.length;tmp.team=1;tmp.summon=true;tmp.ownerSide=1;tmp.x=x;tmp.y=y;tmp.hp=hp;tmp.health=hp;tmp.slotDamageScale=damageScale;tmp.speed=stationary?0:tmp.speed;if(stationary){tmp.vx=0;tmp.vy=0}tmp.trail=[];tmp.deathOrder=null;tmp.slotQueue=[];engine.fighters.push(tmp);return tmp}
function spawnCasinoWave(){casinoWave++;const count=1+Math.floor(Math.random()*7),spots=[[560,120],[620,250],[600,390],[620,540],[500,610],[470,245],[505,440]];for(let i=0;i<count;i++){const p=spots[i%spots.length];makeCasinoSlot(p[0],p[1],125,.8,false)}$('event').textContent='🎲 WAVE '+casinoWave+' / 5 · 🎰 슬롯머신 '+count+'마리 출현!'}
function startCasinoStage(n){casinoStageNo=n;mode='casino';casinoWave=0;if(n===3){engine=new Engine('moneyman','casino_boss',Math.random,{mode:'control'});const boss=engine.fighters[1];boss.casinoMoneyMax=7;boss.hp=1500;boss.health=1500;boss.casinoSummonNext=15}else{engine=new Engine('moneyman','slotmachine',Math.random,{mode:'control'});engine.fighters[1].health=0;spawnCasinoWave()}engine.desertWaveMode=true;engine.casinoMode=true;paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';resetStick();refreshControlUI();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent='🤑 머니맨';$('score-label1').textContent=n===3?'🤵‍♂️ 도박장 사장':'🎰 슬롯머신 웨이브';$('battle-mode').textContent='CASINO '+n;$('battle-info').textContent=n===3?'CHAPTER 5 STAGE 3 · 도박장 사장 HP 1500 · 2초마다 💵 1~7장(장당 30) · 15초마다 HP 50 고정 슬롯머신 소환 · 6초 뒤 소멸.':'CHAPTER 5 STAGE '+n+' · HP 125 / 피해 20% 약화 슬롯머신이 웨이브마다 1~7마리 · 총 5웨이브 · 웨이브 클리어 시 머니맨 최대 HP의 20~77% 회복.';fit();hud();draw();window.scrollTo({top:0,behavior:'auto'});playSfx('start')}
function updateCasinoStage(){if(mode!=='casino'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}if(casinoStageNo<3){const alive=engine.fighters.some(f=>f.team===1&&f.health>0&&!f.casinoSummon);if(!alive){const pct=.20+Math.random()*.57,before=hero.health,heal=hero.hp*pct;hero.health=Math.min(hero.hp,hero.health+heal);const actual=Math.max(0,Math.round(hero.health-before));if(actual>0){hero.healed=(hero.healed||0)+actual;engine.effect(hero,'🎲 WAVE CLEAR +'+actual+' ('+Math.round(pct*100)+'%)','heal')}if(casinoWave>=5)engine.result=0;else spawnCasinoWave()}}else{const boss=engine.fighters.find(f=>f.id==='casino_boss'&&f.team===1&&!f.summon);if(!boss||boss.health<=0)engine.result=0}}
'''
    s=s.replace(needle,casino_logic+needle,1)
# start/reset/rematch casino
rep("if(mode==='space'||mode==='space-select'){resetSpaceTransient();mode='duel'}engine=", "if(mode==='space'||mode==='space-select'){resetSpaceTransient();mode='duel'}if(mode==='casino'||mode==='casino-select'){resetCasinoTransient();mode='duel'}engine=", 'start reset casino')
rep("if(mode==='space'||mode==='space-select'){resetSpaceTransient();mode='duel'}engine=null;", "if(mode==='space'||mode==='space-select'){resetSpaceTransient();mode='duel'}if(mode==='casino'||mode==='casino-select'){resetCasinoTransient();mode='duel'}engine=null;", 'selection reset casino')
rep("mode==='space'?startSpaceStage(spaceStageNo):start();", "mode==='space'?startSpaceStage(spaceStageNo):mode==='casino'?startCasinoStage(casinoStageNo):start();", 'rematch casino')

# Space completion now unlocks chapter 5
old="else if(mode==='space'&&engine.result===0){const coinReward=awardStageCoins(spaceStageNo),ufoRoll=spaceStageNo===3?tryUnlockInfectedUfo():null;tryUnlockDetective();$('winner-icon').textContent='🪐';$('winner').textContent='CHAPTER 4 · STAGE '+spaceStageNo+' 클리어!';$('summary').textContent=t+'초 · 외계 침공 저지 성공 · 🪙 '+coinReward+'코인 획득!'+(ufoRoll==='won'?' · 🎁 5% 보상 성공! 🛸👾 감염 UFO 획득!':ufoRoll==='miss'?' · 🎲 감염 UFO 획득 실패 (5%)':'')}else if(mode==='space')"
new="else if(mode==='space'&&engine.result===0){const coinReward=awardStageCoins(spaceStageNo),ufoRoll=spaceStageNo===3?tryUnlockInfectedUfo():null,chapter5Now=markSpaceStage(spaceStageNo);tryUnlockDetective();$('winner-icon').textContent='🪐';$('winner').textContent='CHAPTER 4 · STAGE '+spaceStageNo+' 클리어!';$('summary').textContent=t+'초 · 외계 침공 저지 성공 · 🪙 '+coinReward+'코인 획득!'+(ufoRoll==='won'?' · 🎁 5% 보상 성공! 🛸👾 감염 UFO 획득!':ufoRoll==='miss'?' · 🎲 감염 UFO 획득 실패 (5%)':'')+(chapter5Now?' · 🎲 CHAPTER 5 해금!':'')}else if(mode==='space')"
rep(old,new,'space result chapter5')
# Casino result branches before normal else
needle="else if(mode==='space'){$('winner-icon').textContent='👾';$('winner').textContent='CHAPTER 4 · STAGE '+spaceStageNo+' 실패';$('summary').textContent=t+'초 · 외계인이 쓰러졌어. 다시 침공을 막아 봐.'}else{"
insert="else if(mode==='space'){$('winner-icon').textContent='👾';$('winner').textContent='CHAPTER 4 · STAGE '+spaceStageNo+' 실패';$('summary').textContent=t+'초 · 외계인이 쓰러졌어. 다시 침공을 막아 봐.'}else if(mode==='casino'&&engine.result===0){const coinReward=awardStageCoins(casinoStageNo),bossRoll=casinoStageNo===3?tryUnlockCasinoBoss():null;tryUnlockDetective();$('winner-icon').textContent='🎲';$('winner').textContent='CHAPTER 5 · STAGE '+casinoStageNo+' 클리어!';$('summary').textContent=t+'초 · 도박장 돌파 성공 · 🪙 '+coinReward+'코인 획득!'+(bossRoll==='won'?' · 🎁 17.7% 보상 성공! 🤵‍♂️ 도박장 사장 획득!':bossRoll==='miss'?' · 🎲 도박장 사장 획득 실패 (17.7%)':'')}else if(mode==='casino'){$('winner-icon').textContent='🎰';$('winner').textContent='CHAPTER 5 · STAGE '+casinoStageNo+' 실패';$('summary').textContent=t+'초 · 머니맨이 쓰러졌어. 다시 도전해 봐.'}else{"
rep(needle,insert,'casino result')

# Casino ability text
rep("if(f.id==='moneyman')return '💰 돈가방 20", "if(f.id==='casino_boss')return '🤵‍♂️ 💵 1~'+(f.casinoMoneyMax||5)+'장 · 장당 30 · 슬롯머신 소환 '+Math.max(0,(f.casinoSummonNext||15)-engine.time).toFixed(1)+'초';if(f.id==='moneyman')return '💰 돈가방 20", 'casino ability')

# Casino background
old="}else if(mode==='space'){const sg=ctx.createLinearGradient(0,0,0,720);sg.addColorStop(0,'#07162c');sg.addColorStop(.55,'#0b1532');sg.addColorStop(1,'#160d2d');ctx.fillStyle=sg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.55;ctx.font='24px sans-serif';ctx.fillText('✦',95,125);ctx.fillText('✧',610,165);ctx.fillText('✦',565,585);ctx.fillText('✧',145,610);ctx.globalAlpha=1}else{"
new="}else if(mode==='space'){const sg=ctx.createLinearGradient(0,0,0,720);sg.addColorStop(0,'#07162c');sg.addColorStop(.55,'#0b1532');sg.addColorStop(1,'#160d2d');ctx.fillStyle=sg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.55;ctx.font='24px sans-serif';ctx.fillText('✦',95,125);ctx.fillText('✧',610,165);ctx.fillText('✦',565,585);ctx.fillText('✧',145,610);ctx.globalAlpha=1}else if(mode==='casino'){const cg=ctx.createLinearGradient(0,0,0,720);cg.addColorStop(0,'#30110f');cg.addColorStop(.5,'#130d18');cg.addColorStop(1,'#07120c');ctx.fillStyle=cg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.34;ctx.font='42px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🎰',92,150);ctx.fillText('🎲',625,170);ctx.fillText('♠️',105,600);ctx.fillText('♦️',615,590);ctx.globalAlpha=.16;ctx.fillStyle='#ffd86b';for(let x=70;x<700;x+=95){ctx.beginPath();ctx.arc(x,70,7,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=1}else{"
rep(old,new,'casino background')
rep("mode==='space'?'#315a86':'#1c2d42'", "mode==='space'?'#315a86':mode==='casino'?'#7f5a28':'#1c2d42'", 'casino grid color')
rep("mode==='space'?'ALIEN INVASION · STAGE '+spaceStageNo:mode==='stage'", "mode==='space'?'ALIEN INVASION · STAGE '+spaceStageNo:mode==='casino'?'CASINO · STAGE '+casinoStageNo:mode==='stage'", 'casino arena title')

# Loop casino updates
rep("updateDesertStage();updateMansionStage();updateSpaceStage();hud()", "updateDesertStage();updateMansionStage();updateSpaceStage();updateCasinoStage();hud()", 'casino loop')

# boot UI call if not caught by earlier double replace
if 'updateChapter4UI();updateChapter5UI();updateCoinUI()' not in s:
    rep('updateChapter4UI();updateCoinUI()', 'updateChapter4UI();updateChapter5UI();updateCoinUI()', 'boot chapter5')

required=['BATTLE <b>v3.50</b>',"id:'casino_boss'",'function startCasinoStage(n)','function updateCasinoStage()','Math.random()>=.177','casinoMoneyMax=7','f.casinoMoneyMax:5',"mode==='casino'",'updateCasinoStage();hud()',"for(let i=0;i<7;i++)f.slotQueue.push","Math.floor(this.rand(30,51))","Math.floor(this.rand(25,31))","f.cd=2/f.scale"]
for x in required:
    if x not in s: raise SystemExit('missing marker: '+x)
if s==orig: raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('v3.50 applied')

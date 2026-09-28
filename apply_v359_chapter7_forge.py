from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if s.count(old)<count:
        raise SystemExit(f'PATCH FAILED: {label} (found {s.count(old)})')
    s=s.replace(old,new,count)

# Version + patch notes
rep('BATTLE <b>v3.58</b>','BATTLE <b>v3.59</b>','version')
rep('📒 패치노트 · v3.58','📒 패치노트 · v3.59','notes title')
anchor='<div class="patch-body"><div class="patch-version"><h3>v3.58 · 밸런스 & 도박장 꾸미기 확장</h3>'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.59 · 밸런스 & CHAPTER 7 · 대장간</h3><ul><li>🐉 용: 비의 분노 지속시간 5초 → 7초.</li><li>🕷️ 거미: 포식(포획) 쿨타임 8초 → 10초.</li><li>🔨 CHAPTER 7 · 대장간 추가. CHAPTER 6 STAGE 1·2·3 클리어 시 해금, 주인공은 ⚒️ 대장장이.</li><li>STAGE 1·2: 👹 도깨비 HP 300 · 3마리씩 5웨이브 · 3초마다 작은 범위 방망이 피해 80 · 웨이브마다 대장장이 최대 HP 30% 회복.</li><li>STAGE 3: 👑👹 왕도깨비 HP 1800 · 방망이 피해 140 / 1.5초. 처치 시 기본 50코인과 별도로 100코인 추가 획득.</li></ul></div><div class="patch-version"><h3>v3.58 · 밸런스 & 도박장 꾸미기 확장</h3>'
rep(anchor,insert,'v359 notes')

# Dragon rain duration 5 -> 7 sec. Keep cooldown starting after rain ends.
rep("f.dragonRaining=true;f.dragonRainUntil=this.time+5/f.scale", "f.dragonRaining=true;f.dragonRainUntil=this.time+7/f.scale", 'dragon rain duration')
rep("this.effect(f,'🌧️ 비의 분노 5초!'", "this.effect(f,'🌧️ 비의 분노 7초!'", 'dragon rain effect text')

# Spider feast/capture cooldown 8 -> 10 sec
rep('nextCapture:8/scale','nextCapture:10/scale','spider initial capture cooldown')
rep('f.nextCapture=this.time+8/f.scale','f.nextCapture=this.time+10/f.scale','spider repeat capture cooldown')
rep("8초마다 적을 포획해 돌진하고", "10초마다 적을 포획해 돌진하고", 'spider description cooldown')
rep("detail:'포획 8초마다", "detail:'포획 10초마다", 'spider detail cooldown')

# CH7 stage-only enemies in roster
roster_anchor="{id:'jellyfish',name:'해파리',icon:'🪼'"
roster_insert="{id:'goblin',name:'도깨비',icon:'👹',tag:'방망이 범위공격',hp:300,damage:80,speed:150,cooldown:3,stageOnly:true,description:'CHAPTER 7의 도깨비. 3초마다 작은 반경에 방망이를 휘둘러 범위 안 상대에게 피해 80.',detail:'HP 300 · 방망이 범위 80 / 3초'},\n{id:'goblin_king',name:'왕도깨비',icon:'👑👹',tag:'강화 방망이 범위공격',hp:1800,damage:140,speed:165,cooldown:1.5,stageOnly:true,description:'CHAPTER 7 STAGE 3의 왕도깨비. 일반 도깨비보다 강하고 빠르게 방망이를 휘둘러 범위 피해 140.',detail:'HP 1800 · 방망이 범위 140 / 1.5초'},\n"+roster_anchor
rep(roster_anchor,roster_insert,'goblin roster')

# Goblin radial club skill, inspired by genie short-radius swing but independent implementation.
skill_anchor='skeletonSkill(f,e){'
skill_code="""goblinSkill(f,e){
 if(!['goblin','goblin_king'].includes(f.id)||f.health<=0||f.stunUntil>this.time||f.cd>1e-9)return;
 const range=(f.id==='goblin_king'?155:130)*f.scale,damage=(f.id==='goblin_king'?140:80)*f.scale;
 const targets=this.enemies(f).filter(x=>x.health>0&&distance(f,x)<=range+x.radius);
 if(!targets.length)return;
 f.attack=.34/f.scale;f.cd=(f.id==='goblin_king'?1.5:3)/f.scale;
 for(const x of targets){this.attack(f,x,damage);if(this.result!==null)break}
 this.effects.push({x:f.x,y:f.y,text:'🏏 '+Math.round(damage),kind:'skill',side:f.side,team:f.team,life:.55});
 this.emit((f.id==='goblin_king'?'👑👹 왕도깨비':'👹 도깨비')+'가 방망이를 휘둘렀다!');
}
"""+skill_anchor
rep(skill_anchor,skill_code,'goblin skill method')
rep("if(f.id.startsWith('skeleton_'))this.skeletonSkill(f,e);", "if(f.id.startsWith('skeleton_'))this.skeletonSkill(f,e);if(f.id==='goblin'||f.id==='goblin_king')this.goblinSkill(f,e);", 'goblin skill call')
# Prevent generic collision attack from adding a second hit.
rep("'skeleton_mage'].includes(f.id)", "'skeleton_mage','goblin','goblin_king'].includes(f.id)", 'goblin generic melee exclusion')

# CH7 unlock/progress storage
rep("OCEAN_STAGE_KEY='neonRumble.oceanStages.v1',SHARK_UNLOCK_KEY", "OCEAN_STAGE_KEY='neonRumble.oceanStages.v1',FORGE_STAGE_KEY='neonRumble.forgeStages.v1',SHARK_UNLOCK_KEY", 'forge storage key')
rep("casinoStageMask=0,oceanStageMask=0,skeletonsUnlocked", "casinoStageMask=0,oceanStageMask=0,forgeStageMask=0,skeletonsUnlocked", 'forge stage state')
rep("oceanStageMask=Number(localStorage.getItem(OCEAN_STAGE_KEY)||0)||0;sharkUnlocked", "oceanStageMask=Number(localStorage.getItem(OCEAN_STAGE_KEY)||0)||0;forgeStageMask=Number(localStorage.getItem(FORGE_STAGE_KEY)||0)||0;sharkUnlocked", 'load forge state')
rep("function chapter6Unlocked(){return (casinoStageMask&7)===7}", "function chapter6Unlocked(){return (casinoStageMask&7)===7}\nfunction chapter7Unlocked(){return (oceanStageMask&7)===7}", 'chapter7 unlock')
rep("function markOceanStage(n){oceanStageMask|=(1<<(n-1));try{localStorage.setItem(OCEAN_STAGE_KEY,String(oceanStageMask))}catch{}return (oceanStageMask&7)===7}", "function markOceanStage(n){const before=chapter7Unlocked();oceanStageMask|=(1<<(n-1));try{localStorage.setItem(OCEAN_STAGE_KEY,String(oceanStageMask))}catch{}updateChapter7UI();return !before&&chapter7Unlocked()}\nfunction markForgeStage(n){forgeStageMask|=(1<<(n-1));try{localStorage.setItem(FORGE_STAGE_KEY,String(forgeStageMask))}catch{}return (forgeStageMask&7)===7}", 'mark ocean/forge stage')

# CH7 UI button + panel
button_anchor='<button id="chapter6-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 6 · CHAPTER 5 STAGE 1·2·3 클리어 필요</button>'
button_new=button_anchor+'<button id="chapter7-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 7 · CHAPTER 6 STAGE 1·2·3 클리어 필요</button>'
rep(button_anchor,button_new,'chapter7 button')
ocean_panel_end='<div id="ocean-panel" class="stage-panel" hidden><h2>🌊 CHAPTER 6 · 바닷속</h2><p>주인공은 🦀 꽃게. CHAPTER 5 STAGE 1·2·3을 모두 클리어하면 입장할 수 있어.</p><div class="stage-grid"><button id="ocean-1" type="button"><strong>STAGE 1</strong><span>🪼🐠🐟 · 3마리 × 5웨이브</span><small>HP 125 · 해파리 근접 50+기절 · 물고기 물 70</small></button><button id="ocean-2" type="button"><strong>STAGE 2</strong><span>🦈 상어</span><small>3초 대쉬 · 피해 50 · 출혈 6초 · 20% 획득</small></button><button id="ocean-3" type="button"><strong>STAGE 3</strong><span>🧜‍♂️ 인어</span><small>3초마다 🌊 피해 100 · 파도 밀치기 · 10% 획득</small></button></div></div>'
forge_panel=ocean_panel_end+'<div id="forge-panel" class="stage-panel" hidden><h2>🔨 CHAPTER 7 · 대장간</h2><p>주인공은 ⚒️ 대장장이. 장비를 약탈하러 온 👹 도깨비 군단을 막아내.</p><div class="stage-grid"><button id="forge-1" type="button"><strong>STAGE 1</strong><span>⚒️ VS 👹👹👹</span><small>HP 300 도깨비 3마리씩 5웨이브 · 방망이 80 / 3초 · 웨이브마다 HP 30% 회복</small></button><button id="forge-2" type="button"><strong>STAGE 2</strong><span>⚒️ VS 👹👹👹</span><small>STAGE 1과 동일한 도깨비 군단 3마리씩 5웨이브</small></button><button id="forge-3" type="button"><strong>STAGE 3</strong><span>⚒️ VS 👑👹</span><small>왕도깨비 HP 1800 · 방망이 140 / 1.5초 · 클리어 시 기본 50 + 추가 100코인</small></button></div></div>'
rep(ocean_panel_end,forge_panel,'forge panel')

# CH7 UI updater
rep("function updateChapter6UI(){const b=$('chapter6-entry');if(b){const ok=chapter6Unlocked();b.disabled=!ok;b.textContent=ok?'🌊 CHAPTER 6 · 바닷속':'🔒 CHAPTER 6 · CHAPTER 5 STAGE 1·2·3 클리어 필요'}updateCasinoSystemUI()}", "function updateChapter6UI(){const b=$('chapter6-entry');if(b){const ok=chapter6Unlocked();b.disabled=!ok;b.textContent=ok?'🌊 CHAPTER 6 · 바닷속':'🔒 CHAPTER 6 · CHAPTER 5 STAGE 1·2·3 클리어 필요'}updateCasinoSystemUI()}\nfunction updateChapter7UI(){const b=$('chapter7-entry');if(!b)return;const ok=chapter7Unlocked();b.disabled=!ok;b.textContent=ok?'🔨 CHAPTER 7 · 대장간':'🔒 CHAPTER 7 · CHAPTER 6 STAGE 1·2·3 클리어 필요'}", 'chapter7 ui updater')

# Manual controls / selection UI include forge mode
rep("['control','stage','boss-control','desert','mansion','space','casino','ocean'].includes(mode)", "['control','stage','boss-control','desert','mansion','space','casino','ocean','forge'].includes(mode)", 'manual forge mode')
rep("oceanSelect=mode==='ocean-select',special=on||desertSelect||mansionSelect||spaceSelect||casinoSelect||oceanSelect", "oceanSelect=mode==='ocean-select',forgeSelect=mode==='forge-select',special=on||desertSelect||mansionSelect||spaceSelect||casinoSelect||oceanSelect||forgeSelect", 'forge select state')
rep("$('chapter6-entry').hidden=special;", "$('chapter6-entry').hidden=special;$('chapter7-entry').hidden=special;", 'hide chapter7 special')
rep("$('ocean-panel').hidden=!oceanSelect;", "$('ocean-panel').hidden=!oceanSelect;$('forge-panel').hidden=!forgeSelect;", 'forge panel toggle')
rep("updateChapter5UI();updateChapter6UI()", "updateChapter5UI();updateChapter6UI();updateChapter7UI()", 'chapter7 UI call')
rep("mode==='casino-select'||mode==='ocean-select'", "mode==='casino-select'||mode==='ocean-select'||mode==='forge-select'", 'stageWas forge')
rep("$('chapter6-entry').hidden=false}", "$('chapter6-entry').hidden=false;$('chapter7-entry').hidden=false}", 'restore chapter7')

# Chapter 7 entry and stage buttons
entry_anchor="$('chapter5-entry').onclick=()=>{if(!chapter5Unlocked())return;if(mode==='space'||mode==='space-select')resetSpaceTransient();mode='casino-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};$('chapter6-entry').onclick=()=>{if(!chapter6Unlocked())return;if(mode==='casino'||mode==='casino-select')resetCasinoTransient();mode='ocean-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};"
entry_new=entry_anchor+"$('chapter7-entry').onclick=()=>{if(!chapter7Unlocked())return;if(mode==='ocean'||mode==='ocean-select')resetOceanTransient();mode='forge-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};"
rep(entry_anchor,entry_new,'chapter7 click')
buttons_anchor="$('ocean-1').onclick=()=>startOceanStage(1);$('ocean-2').onclick=()=>startOceanStage(2);$('ocean-3').onclick=()=>startOceanStage(3);"
rep(buttons_anchor,buttons_anchor+"$('forge-1').onclick=()=>startForgeStage(1);$('forge-2').onclick=()=>startForgeStage(2);$('forge-3').onclick=()=>startForgeStage(3);",'forge stage buttons')

# Forge chapter runtime after ocean runtime
runtime_anchor="function updateOceanStage(){if(mode!=='ocean'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}if(oceanStageNo===1){const alive=engine.fighters.some(f=>f.team===1&&f.health>0);if(!alive){if(oceanWave>=5)engine.result=0;else spawnOceanWave()}}else{const boss=engine.fighters.find(f=>f.team===1&&!f.summon);if(!boss||boss.health<=0)engine.result=0}}"
forge_runtime=runtime_anchor+"""
let forgeStageNo=1,forgeWave=0;
function resetForgeTransient(){forgeStageNo=1;forgeWave=0;if(engine)engine.forgeMode=false}
function makeForgeGoblin(x,y){const tmp=new Engine('smith','goblin',Math.random,{mode:'control'}).fighters[1];tmp.side=engine.fighters.length;tmp.team=1;tmp.summon=true;tmp.ownerSide=1;tmp.x=x;tmp.y=y;tmp.hp=300;tmp.health=300;tmp.damage=80;tmp.cd=0;tmp.trail=[];tmp.deathOrder=null;engine.fighters.push(tmp);return tmp}
function spawnForgeWave(){forgeWave++;const spots=[[545,180],[610,360],[545,540]];for(const [x,y] of spots)makeForgeGoblin(x,y);$('event').textContent='🔨 WAVE '+forgeWave+' / 5 · 👹 도깨비 3마리 침입!'}
function startForgeStage(n){forgeStageNo=n;mode='forge';forgeWave=0;if(n<3){engine=new Engine('smith','goblin',Math.random,{mode:'control'});engine.fighters[1].health=0;spawnForgeWave()}else{engine=new Engine('smith','goblin_king',Math.random,{mode:'control'});const boss=engine.fighters[1];boss.hp=1800;boss.health=1800;boss.damage=140;boss.cd=0}engine.forgeMode=true;paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';resetStick();refreshControlUI();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent='⚒️ 대장장이';$('score-label1').textContent=n<3?'👹 도깨비 웨이브':'👑👹 왕도깨비';$('battle-mode').textContent='FORGE '+n;$('battle-info').textContent=n<3?'CHAPTER 7 STAGE '+n+' · 도깨비 HP 300 · 3마리씩 총 5웨이브 · 작은 범위 방망이 피해 80 / 3초 · 웨이브마다 대장장이 최대 HP 30% 회복.':'CHAPTER 7 STAGE 3 · 왕도깨비 HP 1800 · 방망이 범위 피해 140 / 1.5초 · 처치 시 기본 50코인 + 추가 100코인.';fit();hud();draw();window.scrollTo({top:0,behavior:'auto'});playSfx('start')}
function updateForgeStage(){if(mode!=='forge'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}if(forgeStageNo<3){const alive=engine.fighters.some(f=>f.team===1&&f.health>0);if(!alive){const before=hero.health,heal=hero.hp*.30;hero.health=Math.min(hero.hp,hero.health+heal);const actual=Math.max(0,Math.round(hero.health-before));if(actual>0){hero.healed=(hero.healed||0)+actual;engine.effect(hero,'🔨 WAVE CLEAR +'+actual+' (30%)','heal')}if(forgeWave>=5)engine.result=0;else spawnForgeWave()}}else{const boss=engine.fighters.find(f=>f.id==='goblin_king'&&f.team===1);if(!boss||boss.health<=0)engine.result=0}}
"""
rep(runtime_anchor,forge_runtime,'forge runtime')

# Reset/start/selection/rematch/loop include forge
rep("if(mode==='ocean'||mode==='ocean-select'){resetOceanTransient();mode='duel'}engine=", "if(mode==='ocean'||mode==='ocean-select'){resetOceanTransient();mode='duel'}if(mode==='forge'||mode==='forge-select'){resetForgeTransient();mode='duel'}engine=", 'start reset forge')
rep("if(mode==='ocean'||mode==='ocean-select'){resetOceanTransient();mode='duel'}engine=null", "if(mode==='ocean'||mode==='ocean-select'){resetOceanTransient();mode='duel'}if(mode==='forge'||mode==='forge-select'){resetForgeTransient();mode='duel'}engine=null", 'selection reset forge')
rep("mode==='ocean'?startOceanStage(oceanStageNo):start();", "mode==='ocean'?startOceanStage(oceanStageNo):mode==='forge'?startForgeStage(forgeStageNo):start();", 'forge rematch')
rep("updateCasinoStage();updateOceanStage();hud()", "updateCasinoStage();updateOceanStage();updateForgeStage();hud()", 'forge loop update')

# Result handling: ocean can unlock CH7; forge rewards include +100 on stage 3.
ocean_result="else if(mode==='ocean'&&engine.result===0){const coinReward=awardStageCoins(oceanStageNo),sharkRoll=oceanStageNo===2?tryUnlockShark():null,mermanRoll=oceanStageNo===3?tryUnlockMerman():null;markOceanStage(oceanStageNo);tryUnlockDetective();$('winner-icon').textContent='🌊';$('winner').textContent='CHAPTER 6 · STAGE '+oceanStageNo+' 클리어!';$('summary').textContent=t+'초 · 바닷속 돌파 성공 · 🪙 '+coinReward+'코인 획득!'+(sharkRoll==='won'?' · 🎁 20% 보상 성공! 🦈 상어 획득!':sharkRoll==='miss'?' · 🎲 상어 획득 실패 (20%)':'')+(mermanRoll==='won'?' · 🎁 10% 보상 성공! 🧜‍♂️ 인어 획득!':mermanRoll==='miss'?' · 🎲 인어 획득 실패 (10%)':'')}else if(mode==='ocean'){$('winner-icon').textContent='🌊';$('winner').textContent='CHAPTER 6 · STAGE '+oceanStageNo+' 실패';$('summary').textContent=t+'초 · 꽃게가 쓰러졌어. 다시 바다에 도전해 봐.'}"
ocean_new="else if(mode==='ocean'&&engine.result===0){const coinReward=awardStageCoins(oceanStageNo),sharkRoll=oceanStageNo===2?tryUnlockShark():null,mermanRoll=oceanStageNo===3?tryUnlockMerman():null,chapter7Now=markOceanStage(oceanStageNo);tryUnlockDetective();$('winner-icon').textContent='🌊';$('winner').textContent='CHAPTER 6 · STAGE '+oceanStageNo+' 클리어!';$('summary').textContent=t+'초 · 바닷속 돌파 성공 · 🪙 '+coinReward+'코인 획득!'+(sharkRoll==='won'?' · 🎁 20% 보상 성공! 🦈 상어 획득!':sharkRoll==='miss'?' · 🎲 상어 획득 실패 (20%)':'')+(mermanRoll==='won'?' · 🎁 10% 보상 성공! 🧜‍♂️ 인어 획득!':mermanRoll==='miss'?' · 🎲 인어 획득 실패 (10%)':'')+(chapter7Now?' · 🔨 CHAPTER 7 해금!':'')}else if(mode==='ocean'){$('winner-icon').textContent='🌊';$('winner').textContent='CHAPTER 6 · STAGE '+oceanStageNo+' 실패';$('summary').textContent=t+'초 · 꽃게가 쓰러졌어. 다시 바다에 도전해 봐.'}else if(mode==='forge'&&engine.result===0){const baseReward=awardStageCoins(forgeStageNo),bonus=forgeStageNo===3?100:0;if(bonus){coins+=bonus;saveEconomy();updateCoinUI()}markForgeStage(forgeStageNo);tryUnlockDetective();$('winner-icon').textContent='🔨';$('winner').textContent='CHAPTER 7 · STAGE '+forgeStageNo+' 클리어!';$('summary').textContent=t+'초 · 대장간 방어 성공 · 🪙 '+baseReward+'코인 획득!'+(bonus?' · 👑 왕도깨비 추가 보상 🪙 100코인! · 총 150코인':'')}else if(mode==='forge'){$('winner-icon').textContent='👹';$('winner').textContent='CHAPTER 7 · STAGE '+forgeStageNo+' 실패';$('summary').textContent=t+'초 · 대장장이가 쓰러졌어. 대장간을 다시 지켜 봐.'}"
rep(ocean_result,ocean_new,'forge result handling')

# Forge background + arena title
rep("!['stage','desert','mansion','space','casino','ocean'].includes(mode)", "!['stage','desert','mansion','space','casino','ocean','forge'].includes(mode)", 'wardrobe bg forge exclusion')
forge_bg="""else if(mode==='forge'){const fg=ctx.createLinearGradient(0,0,0,720);fg.addColorStop(0,'#40251a');fg.addColorStop(.52,'#25150f');fg.addColorStop(1,'#120b09');ctx.fillStyle=fg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.28;ctx.fillStyle='#ff8b3d';ctx.beginPath();ctx.arc(590,115,72,0,Math.PI*2);ctx.fill();ctx.globalAlpha=.5;ctx.font='42px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.fillText('🔥',90,145);ctx.fillText('⚒️',625,595);ctx.fillText('🧱',105,610);ctx.globalAlpha=1}"""
rep("else{ctx.fillStyle='#101c2d';ctx.fillRect(0,0,720,720)}ctx.lineWidth=1;", forge_bg+"else{ctx.fillStyle='#101c2d';ctx.fillRect(0,0,720,720)}ctx.lineWidth=1;", 'forge background')
rep("mode==='ocean'?'#1d7896':'#1c2d42'", "mode==='ocean'?'#1d7896':mode==='forge'?'#8a4b2a':'#1c2d42'", 'forge grid color')
rep("mode==='ocean'?'OCEAN · STAGE '+oceanStageNo:mode==='stage'", "mode==='ocean'?'OCEAN · STAGE '+oceanStageNo:mode==='forge'?'FORGE · STAGE '+forgeStageNo:mode==='stage'", 'forge arena title')

# Forge control label
rep("mode==='mansion'?'흡혈귀 이동 · '+controlName():'왼쪽 캐릭터 이동 · '+controlName()", "mode==='mansion'?'흡혈귀 이동 · '+controlName():mode==='forge'?'대장장이 이동 · '+controlName():'왼쪽 캐릭터 이동 · '+controlName()", 'forge control label')

# Verify old version removed and write
p.write_text(s,encoding='utf-8')
print('v3.59 patch applied')

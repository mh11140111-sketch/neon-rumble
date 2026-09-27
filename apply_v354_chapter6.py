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

# Version / patch notes
rep('BATTLE <b>v3.53</b>','BATTLE <b>v3.54</b>','version')
rep('📒 패치노트 · v3.53','📒 패치노트 · v3.54','patch title')
marker='<div class="patch-body">'
patch='''<div class="patch-version"><h3>v3.54 · CHAPTER 6 · 바닷속</h3><ul><li>🌊 CHAPTER 6 추가. CHAPTER 5의 STAGE 1·2·3을 모두 클리어하면 입장 가능하며 주인공은 🦀 꽃게.</li><li>STAGE 1: 🪼🐠🐟 3마리씩 5웨이브. 모두 HP 125. 해파리는 근접 50 + 기절 1초, 두 물고기는 2초마다 💧 피해 70.</li><li>STAGE 2: 🦈 상어. 3초마다 대쉬, 명중 피해 50 + 6초 출혈(0.5초마다 15). 클리어 시 20% 확률로 획득.</li><li>STAGE 3: 🧜‍♂️ 인어. 3초마다 🌊 파도 공격, 피해 100. 맞은 대상은 파도가 사라질 때까지 밀려남. 클리어 시 10% 확률로 획득.</li></ul></div>'''
if patch not in s: rep(marker,marker+patch,'patch notes')
# Opportunistically fix stale Crab description to match real v3.53 mechanics.
s=s.replace("10초마다 탈피해 HP 200 껍질을 남기고 집게 피해가 30 증가하지만, 탈피 후 10초 동안 받는 모든 피해가 10배가 돼.","10초마다 탈피해 HP 200 껍질을 남기고 집게 피해 +30, 이동속도 +20%. 탈피 후 5초 동안 받는 피해가 3배가 돼.",1)

# Add roster characters before zombie mage.
roster_anchor="{id:'zombie_mage',name:'법사좀비'"
idx=s.find(roster_anchor)
if idx<0: raise SystemExit('roster insertion anchor missing')
chars="""{id:'jellyfish',name:'해파리',icon:'🪼',tag:'근접 · 1초 기절',hp:125,damage:50,speed:145,cooldown:1,stageOnly:true,description:'CHAPTER 6 STAGE 1의 해파리. 근접 공격으로 피해 50을 주고 1초 기절시킨다.',detail:'HP 125 · 근접 50 · 기절 1초'},
{id:'tropical_fish',name:'열대어',icon:'🐠',tag:'물 발사',hp:125,damage:70,speed:145,cooldown:2,stageOnly:true,description:'CHAPTER 6 STAGE 1의 열대어. 2초마다 피해 70의 물을 발사한다.',detail:'HP 125 · 💧 피해 70 / 2초'},
{id:'fish',name:'물고기',icon:'🐟',tag:'물 발사',hp:125,damage:70,speed:150,cooldown:2,stageOnly:true,description:'CHAPTER 6 STAGE 1의 물고기. 2초마다 피해 70의 물을 발사한다.',detail:'HP 125 · 💧 피해 70 / 2초'},
{id:'shark',name:'상어',icon:'🦈',tag:'대쉬 · 출혈',hp:1000,damage:50,speed:190,cooldown:3,unlock:'shark',description:'3초마다 가장 가까운 적에게 대쉬해 피해 50을 주고 6초 출혈을 건다. 출혈은 0.5초마다 피해 15.',detail:'HP 1000 · 대쉬 50 / 3초 · 출혈 6초 · 0.5초마다 15'},
{id:'merman',name:'인어',icon:'🧜‍♂️',tag:'파도 · 밀치기',hp:1000,damage:100,speed:145,cooldown:3,unlock:'merman',description:'3초마다 조금 큰 🌊 파도를 발사해 피해 100. 파도에 닿은 적은 파도가 사라질 때까지 밀려난다.',detail:'HP 1000 · 🌊 피해 100 / 3초 · 파도 접촉 중 밀치기'},
"""
s=s[:idx]+chars+s[idx:]

# Fighter runtime state.
rep("egg:false,eggUntil:0,stunUntil:0,burn:null,","egg:false,eggUntil:0,stunUntil:0,burn:null,bleed:null,",'bleed state')
rep("nextCursedHand:type.id==='devileye'?13/scale:9999,","nextCursedHand:type.id==='devileye'?13/scale:9999,sharkDashNext:type.id==='shark'?3/scale:9999,sharkDashHit:false,mermanWaveNext:type.id==='merman'?3/scale:9999,oceanFishNext:(type.id==='tropical_fish'||type.id==='fish')?2/scale:9999,",'ocean timers')

# Ocean combat skills inserted before stepFighter.
step_anchor='stepFighter(f,e,dt){'
if step_anchor not in s: raise SystemExit('stepFighter anchor missing')
skills="""oceanFishSkill(f,e){if(!f||!e||f.health<=0||f.stunUntil>this.time||this.time<(f.oceanFishNext||0)-1e-9)return;f.oceanFishNext=this.time+2/f.scale;const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'water',radius:9*f.scale,speed:330*f.scale,damage:70*f.scale,life:3/f.scale,bounces:0});this.effect(f,'💧 물 발사!','skill')}
sharkSkill(f,e){if(!f||!e||f.health<=0||f.stunUntil>this.time||this.time<(f.sharkDashNext||0)-1e-9)return;const a=this.aim(f,e);f.vx=a.x;f.vy=a.y;f.dash=.48*f.scale;f.sharkDashHit=false;f.sharkDashNext=this.time+3/f.scale;this.effect(f,'🦈 대쉬!','skill')}
applyBleed(f,e){if(!f||!e||e.health<=0||f.team===e.team)return;e.bleed={source:f.side,damage:15*f.scale,next:this.time+.5,expires:this.time+6};this.effect(e,'🩸 출혈 6초','doom')}
tickBleed(e){const b=e.bleed;if(!b)return;while(b.next<=this.time+1e-9&&b.next<=b.expires+1e-9){const source=this.fighters[b.source];if(!source||source.team===e.team){e.bleed=null;return}const n=Math.min(e.health,Math.max(0,Math.round(b.damage*(1-e.armor))));e.health-=n;source.damageDealt+=n;source.hits++;this.effect(e,'🩸 −'+n,'doom');b.next+=.5;if(e.health<=0){if(this.formEgg(e)){e.bleed=null;return}e.trail=[];e.bleed=null;this.emit(e.name+' 출혈로 탈락!');this.checkEnd();return}}if(this.time>=b.expires-1e-9)e.bleed=null}
mermanSkill(f,e){if(!f||!e||f.health<=0||f.stunUntil>this.time||this.time<(f.mermanWaveNext||0)-1e-9)return;f.mermanWaveNext=this.time+3/f.scale;const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+22),y:f.y+a.y*(f.radius+22),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'wave',radius:34*f.scale,speed:225*f.scale,damage:100*f.scale,life:4/f.scale,bounces:0,hitTargets:{}});this.effect(f,'🌊 파도!','skill')}
"""
s=s.replace(step_anchor,skills+step_anchor,1)

# Dispatch skills.
rep("if(f.id==='crab')this.crabSkill(f,e,dt);","if(f.id==='crab')this.crabSkill(f,e,dt);if(f.id==='tropical_fish'||f.id==='fish')this.oceanFishSkill(f,e);if(f.id==='shark')this.sharkSkill(f,e);if(f.id==='merman')this.mermanSkill(f,e);",'ocean dispatch')

# Bleed ticking.
old_ticks="if(f.health>0)this.tickBurn(f);if(this.result!==null)return;if(f.health>0)this.tickCurse(f);if(this.result!==null)return;"
new_ticks="if(f.health>0)this.tickBurn(f);if(this.result!==null)return;if(f.health>0)this.tickCurse(f);if(this.result!==null)return;if(f.health>0)this.tickBleed(f);if(this.result!==null)return;"
rep(old_ticks,new_ticks,'bleed tick loop')

# Wave custom physics: damage once, push continuously until projectile disappears.
wave_pattern=r"s\.x\+=s\.vx\*s\.speed\*dt;s\.y\+=s\.vy\*s\.speed\*dt;(?P<ws>\s*)if\(s\.x<22\|\|s\.x>698\|\|s\.y<22\|\|s\.y>698\)\{"
m=re.search(wave_pattern,s)
if not m: raise SystemExit('wave projectile physics regex anchor missing')
ws=m.group('ws')
wave_block="s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;"+ws+"if(s.kind==='wave'){for(const e of this.enemies(f)){if(e.health<=0||distance(s,e)>=e.radius+s.radius)continue;s.hitTargets=s.hitTargets||{};if(!s.hitTargets[e.side]){this.attackProjectile(f,e,s);s.hitTargets[e.side]=true;if(this.result!==null)break}if(e.health>0){e.x+=s.vx*s.speed*.62*dt;e.y+=s.vy*s.speed*.62*dt;this.keepInside(e)}}if(s.x<22||s.x>698||s.y<22||s.y>698)s.life=0;continue}"+ws+"if(s.x<22||s.x>698||s.y<22||s.y>698){"
s=re.sub(wave_pattern,lambda _m:wave_block,s,count=1)

# Contact specials and exclude ocean fighters from generic melee.
contact_anchor="if(f.id==='boxer'&&f.health>0&&f.stunUntil<=this.time&&this.boxerUppercut(f,e))continue;"
contact_new=contact_anchor+"if(f.id==='jellyfish'&&f.health>0&&f.stunUntil<=this.time&&f.cd<=0){const dealt=this.attack(f,e,50*f.scale);if(dealt>0&&e.health>0){e.stunUntil=Math.max(e.stunUntil,this.time+1);this.effect(e,'🪼 기절 1초!','skill')}continue}if(f.id==='shark'&&f.health>0&&f.stunUntil<=this.time&&f.dash>0&&!f.sharkDashHit){const dealt=this.attack(f,e,50*f.scale);if(dealt>0){f.sharkDashHit=true;f.dash=0;if(e.health>0)this.applyBleed(f,e)}continue}"
rep(contact_anchor,contact_new,'ocean contact skills')
rep("'skeleton_drunk','skeleton_mage'].includes(f.id)","'skeleton_drunk','skeleton_mage','jellyfish','tropical_fish','fish','shark','merman'].includes(f.id)",'generic melee exclusions')

# HTML chapter entry + panel.
ch5='<button id="chapter5-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 5 · CHAPTER 4 STAGE 1·2·3 클리어 필요</button>'
ch6='<button id="chapter6-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 6 · CHAPTER 5 STAGE 1·2·3 클리어 필요</button>'
if ch6 not in s: rep(ch5,ch5+ch6,'chapter6 entry')
ocean_panel='''<div id="ocean-panel" class="stage-panel" hidden><h2>🌊 CHAPTER 6 · 바닷속</h2><p>주인공은 🦀 꽃게. CHAPTER 5 STAGE 1·2·3을 모두 클리어하면 입장할 수 있어.</p><div class="stage-grid"><button id="ocean-1" type="button"><strong>STAGE 1</strong><span>🪼🐠🐟 · 3마리 × 5웨이브</span><small>HP 125 · 해파리 근접 50+기절 · 물고기 물 70</small></button><button id="ocean-2" type="button"><strong>STAGE 2</strong><span>🦈 상어</span><small>3초 대쉬 · 피해 50 · 출혈 6초 · 20% 획득</small></button><button id="ocean-3" type="button"><strong>STAGE 3</strong><span>🧜‍♂️ 인어</span><small>3초마다 🌊 피해 100 · 파도 밀치기 · 10% 획득</small></button></div></div>'''
if 'id="ocean-panel"' not in s:
    m=re.search(r'</section>\s*<section id="battle"',s)
    if not m: raise SystemExit('ocean panel regex anchor missing')
    original=m.group(0)
    replacement='</section>'+ocean_panel+original[len('</section>'):]
    s=s[:m.start()]+replacement+s[m.end():]

# Persistence / unlock state.
rep("CASINO_STAGE_KEY='neonRumble.casinoStages.v1',LEGACY_SKELETON_UNLOCK_KEY", "CASINO_STAGE_KEY='neonRumble.casinoStages.v1',OCEAN_STAGE_KEY='neonRumble.oceanStages.v1',SHARK_UNLOCK_KEY='neonRumble.sharkUnlocked.v1',MERMAN_UNLOCK_KEY='neonRumble.mermanUnlocked.v1',LEGACY_SKELETON_UNLOCK_KEY",'ocean keys')
rep("let robotStageMask=0,desertStageMask=0,mansionStageMask=0,spaceStageMask=0,casinoStageMask=0,skeletonsUnlocked=false,skeletonMageUnlocked=false,zombieMageUnlocked=false,infectedUfoUnlocked=false,detectiveUnlocked=false,casinoBossUnlocked=false;","let robotStageMask=0,desertStageMask=0,mansionStageMask=0,spaceStageMask=0,casinoStageMask=0,oceanStageMask=0,skeletonsUnlocked=false,skeletonMageUnlocked=false,zombieMageUnlocked=false,infectedUfoUnlocked=false,detectiveUnlocked=false,casinoBossUnlocked=false,sharkUnlocked=false,mermanUnlocked=false;",'state vars')
load_anchor="casinoStageMask=Number(localStorage.getItem(CASINO_STAGE_KEY)||0)||0;"
rep(load_anchor,load_anchor+"oceanStageMask=Number(localStorage.getItem(OCEAN_STAGE_KEY)||0)||0;sharkUnlocked=localStorage.getItem(SHARK_UNLOCK_KEY)==='1';mermanUnlocked=localStorage.getItem(MERMAN_UNLOCK_KEY)==='1';",'load ocean state')
rep("function chapter5Unlocked(){return (spaceStageMask&7)===7}","function chapter5Unlocked(){return (spaceStageMask&7)===7}\nfunction chapter6Unlocked(){return (casinoStageMask&7)===7}",'chapter6 unlock')
rep("function markCasinoStage(n){casinoStageMask|=(1<<(n-1));try{localStorage.setItem(CASINO_STAGE_KEY,String(casinoStageMask))}catch{}renderShop();return (casinoStageMask&7)===7}","function markCasinoStage(n){const before=chapter6Unlocked();casinoStageMask|=(1<<(n-1));try{localStorage.setItem(CASINO_STAGE_KEY,String(casinoStageMask))}catch{}updateChapter6UI();renderShop();return !before&&chapter6Unlocked()}\nfunction markOceanStage(n){oceanStageMask|=(1<<(n-1));try{localStorage.setItem(OCEAN_STAGE_KEY,String(oceanStageMask))}catch{}return (oceanStageMask&7)===7}", 'mark ocean')
# UI updater after chapter5 updater.
ch5ui="function updateChapter5UI(){const b=$('chapter5-entry');if(!b)return;const ok=chapter5Unlocked();b.disabled=!ok;b.textContent=ok?'🎲 CHAPTER 5 · 머니맨의 도박장':'🔒 CHAPTER 5 · CHAPTER 4 STAGE 1·2·3 클리어 필요'}"
ch6ui="function updateChapter6UI(){const b=$('chapter6-entry');if(!b)return;const ok=chapter6Unlocked();b.disabled=!ok;b.textContent=ok?'🌊 CHAPTER 6 · 바닷속':'🔒 CHAPTER 6 · CHAPTER 5 STAGE 1·2·3 클리어 필요'}"
rep(ch5ui,ch5ui+'\n'+ch6ui,'chapter6 ui')
# Character lock branches.
lock_tail="||(c?.unlock==='casinoBoss'&&!casinoBossUnlocked)"
rep(lock_tail,lock_tail+"||(c?.unlock==='shark'&&!sharkUnlocked)||(c?.unlock==='merman'&&!mermanUnlocked)",'ocean character locks')
# Unlock functions after casino boss helper.
casino_unlock="function tryUnlockCasinoBoss(){if(casinoBossUnlocked)return 'already';if(Math.random()>=.177)return 'miss';casinoBossUnlocked=true;try{localStorage.setItem(CASINO_BOSS_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}"
ocean_unlock="""function tryUnlockShark(){if(sharkUnlocked)return 'already';if(Math.random()>=.20)return 'miss';sharkUnlocked=true;try{localStorage.setItem(SHARK_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}
function tryUnlockMerman(){if(mermanUnlocked)return 'already';if(Math.random()>=.10)return 'miss';mermanUnlocked=true;try{localStorage.setItem(MERMAN_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}"""
rep(casino_unlock,casino_unlock+'\n'+ocean_unlock,'ocean unlock funcs')

# Stage selection UI.
old_update="function updateStageUI(){const on=mode==='stage',desertSelect=mode==='desert-select',mansionSelect=mode==='mansion-select',spaceSelect=mode==='space-select',casinoSelect=mode==='casino-select',special=on||desertSelect||mansionSelect||spaceSelect||casinoSelect;"
new_update="function updateStageUI(){const on=mode==='stage',desertSelect=mode==='desert-select',mansionSelect=mode==='mansion-select',spaceSelect=mode==='space-select',casinoSelect=mode==='casino-select',oceanSelect=mode==='ocean-select',special=on||desertSelect||mansionSelect||spaceSelect||casinoSelect||oceanSelect;"
rep(old_update,new_update,'updateStageUI head')
rep("$('chapter5-entry').hidden=special;$('stage-panel').hidden=!on;","$('chapter5-entry').hidden=special;$('chapter6-entry').hidden=special;$('stage-panel').hidden=!on;",'chapter6 hide')
rep("$('casino-panel').hidden=!casinoSelect;","$('casino-panel').hidden=!casinoSelect;$('ocean-panel').hidden=!oceanSelect;",'ocean panel visibility')
rep("updateChapter4UI();updateChapter5UI()}","updateChapter4UI();updateChapter5UI();updateChapter6UI()}",'update chapter6 call')
rep("const stageWas=mode==='stage'||mode==='desert-select'||mode==='mansion-select'||mode==='space-select'||mode==='casino-select';","const stageWas=mode==='stage'||mode==='desert-select'||mode==='mansion-select'||mode==='space-select'||mode==='casino-select'||mode==='ocean-select';",'stageWas ocean')
rep("$('chapter5-entry').hidden=false}","$('chapter5-entry').hidden=false;$('chapter6-entry').hidden=false}",'show chapter6')

# Chapter click and stage buttons.
ch5click="$('chapter5-entry').onclick=()=>{if(!chapter5Unlocked())return;if(mode==='space'||mode==='space-select')resetSpaceTransient();mode='casino-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};"
ch6click="$('chapter6-entry').onclick=()=>{if(!chapter6Unlocked())return;if(mode==='casino'||mode==='casino-select')resetCasinoTransient();mode='ocean-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};"
rep(ch5click,ch5click+ch6click,'chapter6 click')
rep("$('casino-3').onclick=()=>startCasinoStage(3);","$('casino-3').onclick=()=>startCasinoStage(3);$('ocean-1').onclick=()=>startOceanStage(1);$('ocean-2').onclick=()=>startOceanStage(2);$('ocean-3').onclick=()=>startOceanStage(3);",'ocean stage buttons')

# Add ocean stage implementation after casino updater.
casino_updater="function updateCasinoStage(){if(mode!=='casino'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}if(casinoStageNo<3){const alive=engine.fighters.some(f=>f.team===1&&f.health>0&&!f.casinoSummon);if(!alive){const pct=.20+Math.random()*.57,before=hero.health,heal=hero.hp*pct;hero.health=Math.min(hero.hp,hero.health+heal);const actual=Math.max(0,Math.round(hero.health-before));if(actual>0){hero.healed=(hero.healed||0)+actual;engine.effect(hero,'🎲 WAVE CLEAR +'+actual+' ('+Math.round(pct*100)+'%)','heal')}if(casinoWave>=5)engine.result=0;else spawnCasinoWave()}}else{const boss=engine.fighters.find(f=>f.id==='casino_boss'&&f.team===1&&!f.summon);if(!boss||boss.health<=0)engine.result=0}}"
ocean_impl="""
let oceanStageNo=1,oceanWave=0;
function resetOceanTransient(){oceanStageNo=1;oceanWave=0;if(engine){engine.desertWaveMode=false;engine.oceanMode=false}}
function makeOceanEnemy(id,x,y){const tmp=new Engine('crab',id,Math.random,{mode:'control'}).fighters[1];tmp.side=engine.fighters.length;tmp.team=1;tmp.summon=true;tmp.ownerSide=1;tmp.x=x;tmp.y=y;tmp.hp=125;tmp.health=125;tmp.trail=[];tmp.deathOrder=null;tmp.bleed=null;if(id==='tropical_fish'||id==='fish')tmp.oceanFishNext=engine.time+2;engine.fighters.push(tmp);return tmp}
function spawnOceanWave(){oceanWave++;const ids=['jellyfish','tropical_fish','fish'],spots=[[545,180],[610,360],[545,540]];for(let i=0;i<3;i++)makeOceanEnemy(ids[i],spots[i][0],spots[i][1]);$('event').textContent='🌊 WAVE '+oceanWave+' / 5 · 🪼🐠🐟 출현!'}
function startOceanStage(n){oceanStageNo=n;mode='ocean';oceanWave=0;if(n===1){engine=new Engine('crab','jellyfish',Math.random,{mode:'control'});engine.fighters[1].health=0;spawnOceanWave()}else if(n===2){engine=new Engine('crab','shark',Math.random,{mode:'control'});const boss=engine.fighters[1];boss.hp=1000;boss.health=1000;boss.sharkDashNext=3}else{engine=new Engine('crab','merman',Math.random,{mode:'control'});const boss=engine.fighters[1];boss.hp=1000;boss.health=1000;boss.mermanWaveNext=3}engine.desertWaveMode=true;engine.oceanMode=true;paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';resetStick();refreshControlUI();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent='🦀 꽃게';$('score-label1').textContent=n===1?'🪼🐠🐟 바다 생물 웨이브':n===2?'🦈 상어':'🧜‍♂️ 인어';$('battle-mode').textContent='OCEAN '+n;$('battle-info').textContent=n===1?'CHAPTER 6 STAGE 1 · 🪼🐠🐟 3마리씩 총 5웨이브 · HP 125 · 해파리 근접 50+기절 1초 · 물고기 물 70/2초.':n===2?'CHAPTER 6 STAGE 2 · 상어 HP 1000 · 3초 대쉬 피해 50 · 출혈 6초, 0.5초마다 15 · 클리어 시 20% 획득.':'CHAPTER 6 STAGE 3 · 인어 HP 1000 · 3초마다 🌊 피해 100 · 파도 접촉 중 밀치기 · 클리어 시 10% 획득.';fit();hud();draw();window.scrollTo({top:0,behavior:'auto'});playSfx('start')}
function updateOceanStage(){if(mode!=='ocean'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}if(oceanStageNo===1){const alive=engine.fighters.some(f=>f.team===1&&f.health>0);if(!alive){if(oceanWave>=5)engine.result=0;else spawnOceanWave()}}else{const boss=engine.fighters.find(f=>f.team===1&&!f.summon);if(!boss||boss.health<=0)engine.result=0}}
"""
rep(casino_updater,casino_updater+ocean_impl,'ocean stage implementation')

# Mode resets/start/rematch.
rep("if(mode==='casino'||mode==='casino-select')resetCasinoTransient();engine=null;mode=next;","if(mode==='casino'||mode==='casino-select')resetCasinoTransient();if(mode==='ocean'||mode==='ocean-select')resetOceanTransient();engine=null;mode=next;",'switch ocean reset')
rep("if(mode==='casino'||mode==='casino-select'){resetCasinoTransient();mode='duel'}engine=","if(mode==='casino'||mode==='casino-select'){resetCasinoTransient();mode='duel'}if(mode==='ocean'||mode==='ocean-select'){resetOceanTransient();mode='duel'}engine=",'start ocean reset')
rep("if(mode==='casino'||mode==='casino-select'){resetCasinoTransient();mode='duel'}engine=null;","if(mode==='casino'||mode==='casino-select'){resetCasinoTransient();mode='duel'}if(mode==='ocean'||mode==='ocean-select'){resetOceanTransient();mode='duel'}engine=null;",'selection ocean reset')
rep("mode==='casino'?startCasinoStage(casinoStageNo):start();","mode==='casino'?startCasinoStage(casinoStageNo):mode==='ocean'?startOceanStage(oceanStageNo):start();",'ocean rematch')
# Manual mode includes ocean.
rep("['control','stage','boss-control','desert','mansion','space','casino'].includes(mode)","['control','stage','boss-control','desert','mansion','space','casino','ocean'].includes(mode)",'manual ocean mode')

# Loop/update + initial UI.
rep("updateDesertStage();updateMansionStage();updateSpaceStage();updateCasinoStage();hud()","updateDesertStage();updateMansionStage();updateSpaceStage();updateCasinoStage();updateOceanStage();hud()",'ocean loop')
rep("updateChapter4UI();updateChapter5UI();updateCoinUI();","updateChapter4UI();updateChapter5UI();updateChapter6UI();updateCoinUI();",'init chapter6 ui')

# Result screen chain.
old_casino="else if(mode==='casino'&&engine.result===0){const coinReward=awardStageCoins(casinoStageNo),bossRoll=casinoStageNo===3?tryUnlockCasinoBoss():null;markCasinoStage(casinoStageNo);tryUnlockDetective();$('winner-icon').textContent='🎲';$('winner').textContent='CHAPTER 5 · STAGE '+casinoStageNo+' 클리어!';$('summary').textContent=t+'초 · 도박장 돌파 성공 · 🪙 '+coinReward+'코인 획득!'+(bossRoll==='won'?' · 🎁 17.7% 보상 성공! 🤵‍♂️ 도박장 사장 획득!':bossRoll==='miss'?' · 🎲 도박장 사장 획득 실패 (17.7%)':'')}else if(mode==='casino'){$('winner-icon').textContent='🎰';$('winner').textContent='CHAPTER 5 · STAGE '+casinoStageNo+' 실패';$('summary').textContent=t+'초 · 머니맨이 쓰러졌어. 다시 도전해 봐.'}else{"
new_casino="else if(mode==='casino'&&engine.result===0){const coinReward=awardStageCoins(casinoStageNo),bossRoll=casinoStageNo===3?tryUnlockCasinoBoss():null,chapter6Now=markCasinoStage(casinoStageNo);tryUnlockDetective();$('winner-icon').textContent='🎲';$('winner').textContent='CHAPTER 5 · STAGE '+casinoStageNo+' 클리어!';$('summary').textContent=t+'초 · 도박장 돌파 성공 · 🪙 '+coinReward+'코인 획득!'+(bossRoll==='won'?' · 🎁 17.7% 보상 성공! 🤵‍♂️ 도박장 사장 획득!':bossRoll==='miss'?' · 🎲 도박장 사장 획득 실패 (17.7%)':'')+(chapter6Now?' · 🌊 CHAPTER 6 해금!':'')}else if(mode==='casino'){$('winner-icon').textContent='🎰';$('winner').textContent='CHAPTER 5 · STAGE '+casinoStageNo+' 실패';$('summary').textContent=t+'초 · 머니맨이 쓰러졌어. 다시 도전해 봐.'}else if(mode==='ocean'&&engine.result===0){const coinReward=awardStageCoins(oceanStageNo),sharkRoll=oceanStageNo===2?tryUnlockShark():null,mermanRoll=oceanStageNo===3?tryUnlockMerman():null;markOceanStage(oceanStageNo);tryUnlockDetective();$('winner-icon').textContent='🌊';$('winner').textContent='CHAPTER 6 · STAGE '+oceanStageNo+' 클리어!';$('summary').textContent=t+'초 · 바닷속 돌파 성공 · 🪙 '+coinReward+'코인 획득!'+(sharkRoll==='won'?' · 🎁 20% 보상 성공! 🦈 상어 획득!':sharkRoll==='miss'?' · 🎲 상어 획득 실패 (20%)':'')+(mermanRoll==='won'?' · 🎁 10% 보상 성공! 🧜‍♂️ 인어 획득!':mermanRoll==='miss'?' · 🎲 인어 획득 실패 (10%)':'')}else if(mode==='ocean'){$('winner-icon').textContent='🌊';$('winner').textContent='CHAPTER 6 · STAGE '+oceanStageNo+' 실패';$('summary').textContent=t+'초 · 꽃게가 쓰러졌어. 다시 바다에 도전해 봐.'}else{"
rep(old_casino,new_casino,'ocean result chain')

# HUD bleed badge.
rep("+(f.moneyHappiness?' · 💰 행복 '+f.moneyHappiness+'중첩':'')", "+(f.moneyHappiness?' · 💰 행복 '+f.moneyHappiness+'중첩':'')+(f.bleed?' · 🩸 출혈 '+Math.max(0,f.bleed.expires-engine.time).toFixed(1)+'초':'')",'bleed hud')

# Draw ocean background and stage title.
rep("wardrobeBg&&!['stage','desert','mansion','space','casino'].includes(mode)","wardrobeBg&&!['stage','desert','mansion','space','casino','ocean'].includes(mode)",'wardrobe ocean exception')
casino_bg="""}else if(mode==='casino'){const cg=ctx.createLinearGradient(0,0,0,720);cg.addColorStop(0,'#30110f');cg.addColorStop(.5,'#130d18');cg.addColorStop(1,'#07120c');ctx.fillStyle=cg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.34;ctx.font='42px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🎰',92,150);ctx.fillText('🎲',625,170);ctx.fillText('♠️',105,600);ctx.fillText('♦️',615,590);ctx.globalAlpha=.16;ctx.fillStyle='#ffd86b';for(let x=70;x<700;x+=95){ctx.beginPath();ctx.arc(x,70,7,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=1}else{ctx.fillStyle='#101c2d';"""
# Actual source uses escaped quotes in string text but read_text has normal backslashes. Use direct find fallback simpler around tail.
needle="ctx.globalAlpha=.16;ctx.fillStyle='#ffd86b';for(let x=70;x<700;x+=95){ctx.beginPath();ctx.arc(x,70,7,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=1}else{ctx.fillStyle='#101c2d';"
ocean_bg="ctx.globalAlpha=.16;ctx.fillStyle='#ffd86b';for(let x=70;x<700;x+=95){ctx.beginPath();ctx.arc(x,70,7,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=1}else if(mode==='ocean'){const og=ctx.createLinearGradient(0,0,0,720);og.addColorStop(0,'#0b5d80');og.addColorStop(.5,'#074264');og.addColorStop(1,'#031d35');ctx.fillStyle=og;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.24;ctx.fillStyle='#85e6ff';for(let i=0;i<18;i++){ctx.beginPath();ctx.arc(50+(i*97)%640,70+(i*83)%580,4+(i%4)*2,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=.45;ctx.font='40px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🪸',95,615);ctx.fillText('🌿',625,610);ctx.fillText('🫧',610,140);ctx.globalAlpha=1}else{ctx.fillStyle='#101c2d';"
rep(needle,ocean_bg,'ocean background')
rep("mode==='casino'?'#7f5a28':'#1c2d42'","mode==='casino'?'#7f5a28':mode==='ocean'?'#1d7896':'#1c2d42'",'ocean grid color')
rep("mode==='casino'?'CASINO · STAGE '+casinoStageNo:mode==='stage'","mode==='casino'?'CASINO · STAGE '+casinoStageNo:mode==='ocean'?'OCEAN · STAGE '+oceanStageNo:mode==='stage'",'ocean title')
# Water/wave renderer.
render_anchor="if(s.kind==='magnifier'){"
render_new="if(s.kind==='water'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(Math.max(20,s.radius*2.7))+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('💧',0,0)}else if(s.kind==='wave'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(Math.max(42,s.radius*2.5))+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🌊',0,0)}else if(s.kind==='magnifier'){"
rep(render_anchor,render_new,'ocean projectile render')

required=['BATTLE <b>v3.54</b>','id="chapter6-entry"','id="ocean-panel"',"id:'shark'", "id:'merman'", "id:'jellyfish'",'function startOceanStage','function updateOceanStage','function tickBleed' if False else 'tickBleed(e){',"s.kind==='wave'",'CHAPTER 6 해금','updateChapter6UI']
for x in required:
    if x not in s: raise SystemExit('missing marker: '+x)
if s==orig: raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('v3.54 applied')

from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

# Version + notes
once('BATTLE <b>v3.69</b>','BATTLE <b>v3.70</b>','version')
once('<summary>📒 패치노트 · v3.69</summary><div class="patch-body">', '<summary>📒 패치노트 · v3.70</summary><div class="patch-body"><div class="patch-version"><h3>v3.70 · 밸런스 · CHAPTER 9 실험실 탈출</h3><ul><li>🫈 털복숭이 할퀴기 0.95초. 처치 시 죽기 직전 HP의 2.5배 회복, 최대 HP와 할퀴기 피해 보너스가 각각 10~50 증가.</li><li>📺 낡은TV 노이즈 유지시간 5초 → 1.5초.</li><li>🧪 CHAPTER 9 실험실 탈출 추가. STAGE 1·2는 과학자 3명씩 5웨이브, 웨이브 클리어 시 최대 HP 30% 회복.</li><li>👨‍⚕️ STAGE 3 의사 추가. 💉 주사기 접촉으로 적에게 피해 80+독, 아군에게 즉시 50 회복+3초 약물치료. 클리어 시 10% 획득.</li></ul></div>', 'patch notes')

# Roster updates
old_tv="{id:'old_tv',name:'낡은TV',icon:'📺',tag:'화면 노이즈 · 🔲 연사',hp:1000,damage:40,speed:125,cooldown:0,unlock:'oldTv',description:'3.5초마다 5초 동안 화면에 실제 노이즈가 생긴다. 노이즈 상태에서는 0.1~2초의 무작위 간격으로 🔲을 1~3연발하며, 한 발 피해는 40이고 탄속은 기본~2배 사이에서 무작위로 정해진다.',detail:'HP 1000 · 노이즈 3.5초마다 / 5초 유지 · 🔲 1~3연발 · 발당 40 · 발사 간격 0.1~2초 · 탄속 ×1~2 · CH7 클리어 후 제작소에서 획득'},"
new_tv="{id:'old_tv',name:'낡은TV',icon:'📺',tag:'화면 노이즈 · 🔲 연사',hp:1000,damage:40,speed:125,cooldown:0,unlock:'oldTv',description:'3.5초마다 1.5초 동안 화면에 실제 노이즈가 생긴다. 노이즈 상태에서는 0.1~2초의 무작위 간격으로 🔲을 1~3연발하며, 한 발 피해는 40이고 탄속은 기본~2배 사이에서 무작위로 정해진다.',detail:'HP 1000 · 노이즈 3.5초마다 / 1.5초 유지 · 🔲 1~3연발 · 발당 40 · 발사 간격 0.1~2초 · 탄속 ×1~2 · CH7 클리어 후 제작소에서 획득'},"
once(old_tv,new_tv,'old TV roster')
old_fur="{id:'furball',name:'털복숭이',icon:'🫈',tag:'할퀴기 · 출혈 · 처치 회복',hp:1000,damage:55,speed:165,cooldown:1.5,description:'상대가 가까이 접근하면 할퀴기 이펙트와 함께 피해 10~100을 주며 50% 확률로 출혈을 부여한다. 자신이 마지막으로 공격한 상대가 사망하면 그 상대가 죽기 직전 체력만큼 회복한다.',detail:'HP 1000 · 이동속도 165 · 할퀴기 10~100 / 1.5초 · 출혈 50% · 마지막 공격 대상 사망 시 죽기 직전 HP만큼 회복'},"
new_fur="{id:'furball',name:'털복숭이',icon:'🫈',tag:'할퀴기 · 출혈 · 처치 성장',hp:1000,damage:55,speed:165,cooldown:.95,description:'가까운 상대를 0.95초마다 할퀴어 피해 10~100을 주며 50% 확률로 출혈을 부여한다. 마지막으로 공격한 상대가 사망하면 죽기 직전 HP의 2.5배를 회복하고 최대 HP와 할퀴기 피해가 각각 10~50 증가한다.',detail:'HP 1000 · 이동속도 165 · 할퀴기 10~100 / 0.95초 · 출혈 50% · 처치 시 죽기 직전 HP×2.5 회복 · 최대 HP/피해 각각 +10~50'},\n{id:'scientist',name:'과학자',icon:'🧑‍🔬',tag:'독 투사체',hp:125,damage:30,speed:135,cooldown:1,stageOnly:true,description:'1초마다 피해 30의 독 투사체를 발사하며 적중 시 확정으로 독을 부여한다.',detail:'HP 125 · 독 투사체 30 / 1초 · 독 확정'},\n{id:'doctor',name:'의사',icon:'👨‍⚕️',tag:'💉 주사기 · 약물치료',hp:1000,damage:80,speed:145,cooldown:1,unlock:'doctor',description:'가장 가까운 캐릭터를 향해 💉 주사기를 겨눈다. 적이 닿으면 피해 80과 독, 아군이 닿으면 즉시 HP 50 회복과 3초 약물치료를 부여한다. 약물치료는 0.5초마다 HP 10을 회복한다.',detail:'HP 1000 · 💉 적 80+독 · 아군 즉시 +50 · 약물치료 3초 / 0.5초마다 +10 · CH9 STAGE 3 10% 획득'},"
once(old_fur,new_fur,'furball roster + lab roster')

# TV duration runtime
once("f.oldTvNoiseUntil=this.time+5/f.scale", "f.oldTvNoiseUntil=this.time+1.5/f.scale", 'TV noise duration')

# Furball kill growth + heal x2.5
old_death="""furballDeathHeal(dead,preHp){
 if(!dead||dead.health>0)return;
 const hp=Math.max(0,Math.round(Number(preHp)||0));
 for(const f of this.fighters){if(f.id!=='furball'||f.health<=0||f.furballLastTargetSide!==dead.side)continue;const heal=Math.min(f.hp-f.health,hp);if(heal>0){f.health+=heal;f.healed+=heal;this.effect(f,'🫈 +'+heal,'heal');this.emit('🫈 털복숭이가 마지막 공격 대상의 죽기 직전 체력 '+heal+' 회복!')}f.furballLastTargetSide=null}
}
"""
new_death="""furballDeathHeal(dead,preHp){
 if(!dead||dead.health>0)return;
 const baseHp=Math.max(0,Number(preHp)||0);
 for(const f of this.fighters){if(f.id!=='furball'||f.health<=0||f.furballLastTargetSide!==dead.side)continue;
  const hpGain=10+Math.floor(this.random()*41),dmgGain=10+Math.floor(this.random()*41);f.hp+=hpGain;f.health+=hpGain;f.furballBonusDamage=(f.furballBonusDamage||0)+dmgGain;f.damage+=dmgGain;
  const wanted=Math.round(baseHp*2.5),heal=Math.min(f.hp-f.health,wanted);if(heal>0){f.health+=heal;f.healed+=heal}this.effect(f,'🫈 처치 성장! HP +'+hpGain+' · 피해 +'+dmgGain+' · 회복 +'+heal,'heal');this.emit('🫈 털복숭이 처치 성장! 죽기 직전 HP×2.5 회복');f.furballLastTargetSide=null}
}
"""
once(old_death,new_death,'furball death growth')
once("const dmg=(10+Math.floor(this.random()*91))*f.scale,ang=Math.atan2(e.y-f.y,e.x-f.x);f.furballLastTargetSide=e.side;", "const dmg=(10+Math.floor(this.random()*91)+(f.furballBonusDamage||0))*f.scale,ang=Math.atan2(e.y-f.y,e.x-f.x);f.furballLastTargetSide=e.side;", 'furball damage growth')
once("f.cd=1.5/f.scale;f.slashFx=.28/f.scale", "f.cd=.95/f.scale;f.slashFx=.28/f.scale", 'furball cooldown')

# Scientist / doctor mechanics inserted before furball helpers
anchor='furballDeathHeal(dead,preHp){'
lab_engine=r'''scientistSkill(f,e){
 if(!f||f.id!=='scientist'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0||f.cd>1e-9)return;
 const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'scientist_poison',icon:'🧪',radius:8*f.scale,speed:330*f.scale,damage:30*f.scale,life:4,bounces:0,poison:true});f.cd=1/f.scale;f.attack=.16/f.scale;this.effect(f,'🧪 독 투사체!','skill')
}
doctorNeedlePoint(f,target){if(!target)return{x:f.x,y:f.y,a:0};const a=this.aim(f,target),ang=Math.atan2(a.y,a.x),reach=f.radius+44*f.scale;return{x:f.x+a.x*reach,y:f.y+a.y*reach,a:ang}}
doctorSkill(f){
 if(!f||f.id!=='doctor'||f.health<=0||f.stunUntil>this.time)return;
 const targets=this.fighters.filter(x=>x!==f&&x.health>0&&!x.egg).sort((a,b)=>distance(f,a)-distance(f,b)),t=targets[0];if(!t)return;
 const p=this.doctorNeedlePoint(f,t);f.doctorNeedleX=p.x;f.doctorNeedleY=p.y;f.doctorNeedleAngle=p.a;if(f.cd>1e-9||distance(p,t)>t.radius+14*f.scale)return;
 f.cd=1/f.scale;f.attack=.18/f.scale;
 if(t.team!==f.team){const dealt=this.attack(f,t,80*f.scale);if(dealt>0&&t.health>0)this.applyPoison(f,t);this.effect(t,'💉 80 + 독!','skill')}
 else{const heal=Math.min(50*f.scale,t.hp-t.health);t.health+=heal;t.healed+=heal;t.drugTreatment={next:this.time+.5,expires:this.time+3};this.effect(t,'💉 +'+Math.round(heal)+' · 약물치료 3초','heal')}
}
tickDrugTreatment(f){const d=f.drugTreatment;if(!d||f.health<=0)return;while(d.next<=this.time+1e-9&&d.next<=d.expires+1e-9){const heal=Math.min(10,f.hp-f.health);f.health+=heal;f.healed+=heal;if(heal)this.effect(f,'💊 +10','heal');d.next+=.5}if(this.time>=d.expires-1e-9)f.drugTreatment=null}
'''
if s.count(anchor)!=1: raise SystemExit('furball helper anchor not unique')
s=s.replace(anchor,lab_engine+anchor,1)

# Hook scientist / doctor skills
once("if(f.id==='old_tv')this.oldTvSkill(f,e);if(f.id==='furball')this.furballSkill(f,e);", "if(f.id==='old_tv')this.oldTvSkill(f,e);if(f.id==='furball')this.furballSkill(f,e);if(f.id==='scientist')this.scientistSkill(f,e);if(f.id==='doctor')this.doctorSkill(f);", 'lab skill hooks')
# Status ticking
once("if(f.health>0)this.tickBleed(f);if(this.result!==null)return;}", "if(f.health>0)this.tickBleed(f);if(this.result!==null)return;if(f.health>0)this.tickDrugTreatment(f);}", 'drug treatment tick')
# Generic melee exclusion
needle="'goblin','goblin_king','psychic','furball'].includes(f.id)"
if needle not in s: raise SystemExit('generic melee exclusion anchor missing')
s=s.replace(needle,"'goblin','goblin_king','psychic','furball','scientist','doctor'].includes(f.id)",1)

# Unlock state / keys
once("OLD_TV_UNLOCK_KEY='neonRumble.oldTvUnlocked.v1',SHARK_UNLOCK_KEY", "OLD_TV_UNLOCK_KEY='neonRumble.oldTvUnlocked.v1',DOCTOR_UNLOCK_KEY='neonRumble.doctorUnlocked.v1',LAB_STAGE_KEY='neonRumble.labStages.v1',SHARK_UNLOCK_KEY", 'doctor keys')
once("forgeStageMask=0,boxingStageMask=0,skeletonsUnlocked", "forgeStageMask=0,boxingStageMask=0,labStageMask=0,skeletonsUnlocked", 'lab stage state')
once("psychicUnlocked=false,oldTvUnlocked=false;try{", "psychicUnlocked=false,oldTvUnlocked=false,doctorUnlocked=false;try{", 'doctor state')
once("boxingStageMask=Number(localStorage.getItem(BOXING_STAGE_KEY)||0)||0;psychicUnlocked=", "boxingStageMask=Number(localStorage.getItem(BOXING_STAGE_KEY)||0)||0;labStageMask=Number(localStorage.getItem(LAB_STAGE_KEY)||0)||0;psychicUnlocked=", 'lab load')
once("oldTvUnlocked=localStorage.getItem(OLD_TV_UNLOCK_KEY)==='1';sharkUnlocked", "oldTvUnlocked=localStorage.getItem(OLD_TV_UNLOCK_KEY)==='1';doctorUnlocked=localStorage.getItem(DOCTOR_UNLOCK_KEY)==='1';sharkUnlocked", 'doctor load')
once("(c?.unlock==='oldTv'&&!oldTvUnlocked)}", "(c?.unlock==='oldTv'&&!oldTvUnlocked)||(c?.unlock==='doctor'&&!doctorUnlocked)}", 'doctor character lock')

# Chapter 9 progress + doctor unlock
once("function chapter8Unlocked(){return (forgeStageMask&7)===7}", "function chapter8Unlocked(){return (forgeStageMask&7)===7}\nfunction chapter9Unlocked(){return (boxingStageMask&7)===7}", 'chapter9 unlock')
once("function markBoxingStage(n){boxingStageMask|=(1<<(n-1));try{localStorage.setItem(BOXING_STAGE_KEY,String(boxingStageMask))}catch{}return (boxingStageMask&7)===7}", "function markBoxingStage(n){const before=chapter9Unlocked();boxingStageMask|=(1<<(n-1));try{localStorage.setItem(BOXING_STAGE_KEY,String(boxingStageMask))}catch{}updateChapter9UI();return !before&&chapter9Unlocked()}\nfunction markLabStage(n){labStageMask|=(1<<(n-1));try{localStorage.setItem(LAB_STAGE_KEY,String(labStageMask))}catch{}return (labStageMask&7)===7}\nfunction tryUnlockDoctor(){if(doctorUnlocked)return 'already';if(Math.random()>=.10)return 'miss';doctorUnlocked=true;try{localStorage.setItem(DOCTOR_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}", 'lab progress + doctor unlock')

# Skip ticket can unlock CH9 too
old="else if(!chapter8Unlocked()){forgeStageMask=7;localStorage.setItem(FORGE_STAGE_KEY,'7');label='CHAPTER 8'}else{alert('현재 해금할 다음 챕터가 없어!');return}"
new="else if(!chapter8Unlocked()){forgeStageMask=7;localStorage.setItem(FORGE_STAGE_KEY,'7');label='CHAPTER 8'}else if(!chapter9Unlocked()){boxingStageMask=7;localStorage.setItem(BOXING_STAGE_KEY,'7');label='CHAPTER 9'}else{alert('현재 해금할 다음 챕터가 없어!');return}"
once(old,new,'skip CH9')
once("updateChapter7UI();updateChapter8UI();renderForgeSystem();", "updateChapter7UI();updateChapter8UI();updateChapter9UI();renderForgeSystem();", 'skip UI refresh')

# Manual mode / control label
once("'ocean','forge','boxing'].includes(mode)", "'ocean','forge','boxing','lab'].includes(mode)", 'manual lab mode')
once("mode==='boxing'?'복서 이동 · '+controlName():'왼쪽 캐릭터 이동 · '+controlName()", "mode==='boxing'?'복서 이동 · '+controlName():mode==='lab'?'털복숭이 이동 · '+controlName():'왼쪽 캐릭터 이동 · '+controlName()", 'lab control label')

# HUD ability labels
once("function ability(f){if(f.id==='furball')return '🫈 할퀴기 10~100 / 1.5초 · 출혈 50% · 마지막 공격 대상 사망 시 회복';", "function ability(f){if(f.id==='doctor')return '👨‍⚕️ 💉 적 80+독 · 아군 +50+약물치료';if(f.id==='scientist')return '🧑‍🔬 독 투사체 30 / 1초 · 독 확정';if(f.id==='furball')return '🫈 할퀴기 0.95초 · 출혈 50% · 처치 시 HP×2.5 회복 + 성장';", 'ability labels')

# Doctor syringe visual before fighters
fighter_draw="for(const f of engine.fighters){if(f.moonUltPhase==='air')continue;"
needle_draw="for(const d of engine.fighters){if(d.id!=='doctor'||d.health<=0||!Number.isFinite(d.doctorNeedleX))continue;ctx.save();ctx.translate(d.doctorNeedleX,d.doctorNeedleY);ctx.rotate(d.doctorNeedleAngle||0);ctx.font=(30*d.scale)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('💉',0,0);ctx.restore()}\n"
if s.count(fighter_draw)!=1: raise SystemExit('fighter draw anchor missing')
s=s.replace(fighter_draw,needle_draw+fighter_draw,1)

# Chapter 9 runtime/UI inserted before main IIFE close.
end_marker="})();\n\n</script>\n<script id=\"mobile-compat-js\">"
if end_marker not in s: raise SystemExit('main script end marker missing')
lab_ui=r'''
let labStageNo=1,labWave=0;
function updateChapter9UI(){const b=$('chapter9-entry');if(!b)return;const ok=chapter9Unlocked();b.disabled=!ok;b.textContent=ok?'🧪 CHAPTER 9 · 실험실 탈출':'🔒 CHAPTER 9 · CHAPTER 8 STAGE 1·2·3 클리어 필요'}
function setupChapter9UI(){if($('chapter9-entry'))return;const after=$('chapter8-entry'),sel=$('selection');if(!after||!sel)return;const b=document.createElement('button');b.id='chapter9-entry';b.type='button';b.className=after.className;after.insertAdjacentElement('afterend',b);const p=document.createElement('section');p.id='lab-selection';p.hidden=true;p.innerHTML='<div class="section-title"><div><p class="eyebrow">CHAPTER 9</p><h2>🧪 실험실 탈출</h2></div></div><p class="match-info">주인공 🫈 털복숭이로 실험실을 탈출해.</p><div class="mode-tabs"><button id="lab-1" type="button">STAGE 1 · 🧑‍🔬 5웨이브</button><button id="lab-2" type="button">STAGE 2 · 🧑‍🔬 5웨이브</button><button id="lab-3" type="button">STAGE 3 · 👨‍⚕️ 의사</button></div>';sel.appendChild(p);b.onclick=()=>{if(!chapter9Unlocked())return;hideStageSelectionPanels();p.hidden=false;window.scrollTo({top:0,behavior:'auto'})};$('lab-1').onclick=()=>startLabStage(1);$('lab-2').onclick=()=>startLabStage(2);$('lab-3').onclick=()=>startLabStage(3);updateChapter9UI()}
function spawnLabScientist(x,y){const t=new Engine('furball','scientist',Math.random,{mode:'control'}).fighters[1];t.side=engine.fighters.length;t.team=1;t.x=x;t.y=y;t.hp=125;t.health=125;t.damage=30;t.cooldown=1;t.cd=0;t.boss=false;t.scale=1;t.bodyScale=1;t.radius=33;t.summon=true;t.ownerSide=1;t.trail=[];engine.fighters.push(t);return t}
function spawnLabWave(){labWave++;const spots=[[535,170],[625,360],[535,550]];for(const [x,y] of spots)spawnLabScientist(x,y);$('event').textContent='🧪 WAVE '+labWave+' / 5 · 과학자 3명 출현!'}
function startLabStage(n){labStageNo=n;labWave=0;mode='lab';if(n<3){engine=new Engine('furball','scientist',Math.random,{mode:'control'});engine.fighters[1].health=0;engine.desertWaveMode=true;spawnLabWave()}else{engine=new Engine('furball','doctor',Math.random,{mode:'control'});engine.desertWaveMode=false}paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';hideStageSelectionPanels();if($('lab-selection'))$('lab-selection').hidden=true;$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';resetStick();refreshControlUI();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent='🫈 털복숭이';$('score-label1').textContent=n<3?'🧑‍🔬 과학자 웨이브':'👨‍⚕️ 의사';$('battle-mode').textContent='LAB '+n;$('battle-info').textContent=n<3?'CHAPTER 9 STAGE '+n+' · 과학자 HP 125 · 3명씩 5웨이브 · 독 투사체 30 / 1초 · 웨이브 클리어 시 HP 30% 회복.':'CHAPTER 9 STAGE 3 · 의사의 💉 주사기는 적에게 80+독, 아군에게 +50 및 3초 약물치료.';fit();hud();draw();window.scrollTo({top:0,behavior:'auto'});playSfx('start')}
function updateLabStage(){if(mode!=='lab'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}if(labStageNo<3){const alive=engine.fighters.some(f=>f.team===1&&f.health>0);if(!alive){const before=hero.health;hero.health=Math.min(hero.hp,hero.health+hero.hp*.3);const heal=Math.max(0,Math.round(hero.health-before));if(heal){hero.healed+=heal;engine.effect(hero,'🧪 WAVE CLEAR +'+heal,'heal')}if(labWave>=5){engine.result=0;engine.desertWaveMode=false}else spawnLabWave()}}else{const boss=engine.fighters.find(f=>f.id==='doctor'&&f.team===1);if(!boss||boss.health<=0)engine.result=0}}
setupChapter9UI();
'''
s=s.replace(end_marker,lab_ui+end_marker,1)

# Run lab wave update from HUD before resolving result
once("function hud(){if(!engine)return;", "function hud(){if(!engine)return;if(mode==='lab')updateLabStage();", 'lab update hook')

# Result branches after boxing branches
old="else if(mode==='boxing'){$('winner-icon').textContent='🥊';$('winner').textContent='CHAPTER 8 · STAGE '+boxingStageNo+' 실패';$('summary').textContent=t+'초 · 복서가 쓰러졌어. 다시 도전해 봐.'}else{$('winner-icon')"
new="else if(mode==='boxing'){$('winner-icon').textContent='🥊';$('winner').textContent='CHAPTER 8 · STAGE '+boxingStageNo+' 실패';$('summary').textContent=t+'초 · 복서가 쓰러졌어. 다시 도전해 봐.'}else if(mode==='lab'&&engine.result===0){const coinReward=awardStageCoins(labStageNo),doctorRoll=labStageNo===3?tryUnlockDoctor():null;markLabStage(labStageNo);$('winner-icon').textContent='🧪';$('winner').textContent='CHAPTER 9 · STAGE '+labStageNo+' 클리어!';$('summary').textContent=t+'초 · 실험실 탈출 성공 · 🪙 '+coinReward+'코인 획득!'+(doctorRoll==='won'?' · 🎁 10% 보상 성공! 👨‍⚕️ 의사 획득!':doctorRoll==='miss'?' · 🎲 의사 획득 실패 (10%)':'')}else if(mode==='lab'){$('winner-icon').textContent='🧪';$('winner').textContent='CHAPTER 9 · STAGE '+labStageNo+' 실패';$('summary').textContent=t+'초 · 털복숭이가 쓰러졌어. 다시 탈출해 봐.'}else{$('winner-icon')"
once(old,new,'lab result branches')

p.write_text(s,encoding='utf-8')
print('v3.70 patch applied')

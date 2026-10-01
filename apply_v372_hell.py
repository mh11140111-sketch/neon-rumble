from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

def must(text,label):
    if text not in s:
        raise SystemExit(f'{label}: anchor missing')

# version + release note
once('BATTLE <b>v3.71</b>','BATTLE <b>v3.72</b>','version')
old_summary='<summary>📒 패치노트 · v3.71</summary><div class="patch-body">'
new_summary='<summary>📒 패치노트 · v3.72</summary><div class="patch-body"><div class="patch-version"><h3>v3.72 · 낡은TV 밸런스 · CHAPTER 10 지옥</h3><ul><li>📺 낡은TV 노이즈 발생 주기 5초, 유지시간 3초로 변경.</li><li>🔥 CHAPTER 10 지옥 추가. 주인공은 🦸 히어로.</li><li>🧿 STAGE 1: HP 2500 악마의 눈.</li><li>👿 STAGE 2: HP 666 악마의 분신. 악마와 동일한 공격방식.</li><li>👿 STAGE 3: HP 6666 악마 + 선택한 조력자 1명. 악의 돌진/소환/무적을 사용하며 누적 1500 피해마다 히어로와 조력자 HP 500 회복.</li></ul></div>'
once(old_summary,new_summary,'patch notes')

# Old TV balance
old_tv="{id:'old_tv',name:'낡은TV',icon:'📺',tag:'화면 노이즈 · 🔲 연사',hp:1000,damage:40,speed:125,cooldown:0,unlock:'oldTv',description:'3.5초마다 1.5초 동안 화면에 실제 노이즈가 생긴다. 노이즈 상태에서는 0.1~2초의 무작위 간격으로 🔲을 1~3연발하며, 한 발 피해는 40이고 탄속은 기본~2배 사이에서 무작위로 정해진다.',detail:'HP 1000 · 노이즈 3.5초마다 / 1.5초 유지 · 🔲 1~3연발 · 발당 40 · 발사 간격 0.1~2초 · 탄속 ×1~2 · CH7 클리어 후 제작소에서 획득'},"
new_tv="{id:'old_tv',name:'낡은TV',icon:'📺',tag:'화면 노이즈 · 🔲 연사',hp:1000,damage:40,speed:125,cooldown:0,unlock:'oldTv',description:'5초마다 3초 동안 화면에 실제 노이즈가 생긴다. 노이즈 상태에서는 0.1~2초의 무작위 간격으로 🔲을 1~3연발하며, 한 발 피해는 40이고 탄속은 기본~2배 사이에서 무작위로 정해진다.',detail:'HP 1000 · 노이즈 5초마다 / 3초 유지 · 🔲 1~3연발 · 발당 40 · 발사 간격 0.1~2초 · 탄속 ×1~2 · CH7 클리어 후 제작소에서 획득'},"
once(old_tv,new_tv,'old TV roster')
once("f.oldTvNoiseNext=this.time+3.5/f.scale;f.oldTvNoiseUntil=0;f.oldTvShotNext=Infinity", "f.oldTvNoiseNext=this.time+5/f.scale;f.oldTvNoiseUntil=0;f.oldTvShotNext=Infinity", 'TV initial noise')
once("f.oldTvNoiseNext=this.time+3.5/f.scale;f.oldTvNoiseUntil=this.time+1.5/f.scale", "f.oldTvNoiseNext=this.time+5/f.scale;f.oldTvNoiseUntil=this.time+3/f.scale", 'TV runtime noise')
once("(f.oldTvNoiseNext||3.5)-engine.time", "(f.oldTvNoiseNext||5)-engine.time", 'TV HUD countdown')

# Hell stage-only roster characters
roster_anchor="{id:'doctor',name:'의사',icon:'👨‍⚕️',tag:'💉 주사기 · 약물치료',hp:1000,damage:70,speed:145,cooldown:1,unlock:'doctor',description:'가장 가까운 캐릭터를 향해 💉 주사기를 겨눈다. 적이 닿으면 피해 70과 독, 아군이 닿으면 즉시 HP 30 회복과 3초 약물치료를 부여한다. 약물치료는 0.5초마다 HP 10을 회복한다.',detail:'HP 1000 · 💉 적 70+독 · 아군 즉시 +30 · 약물치료 3초 / 0.5초마다 +10 · CH9 STAGE 3 10% 획득'},\n"
hell_roster=roster_anchor+"{id:'hell_clone',name:'악마의 분신',icon:'👿',tag:'악의 돌진 · 악의 소환 · 무적',hp:666,damage:13,speed:170,cooldown:0,stageOnly:true,description:'5초마다 악의 돌진, 3초마다 HP 66 악마의 눈 소환, 13초마다 5초 무적과 HP 500 회복을 사용한다.',detail:'HP 666 · 악의 돌진 13~666 / 5초 · 🧿 HP 66 소환 / 3초 · 무적 5초 + HP 500 / 13초'},\n{id:'hell_demon',name:'악마',icon:'👿',tag:'악의 돌진 · 악의 소환 · 무적',hp:6666,damage:13,speed:175,cooldown:0,stageOnly:true,description:'5초마다 악의 돌진, 3초마다 HP 66 악마의 눈 소환, 13초마다 5초 무적과 HP 500 회복을 사용한다.',detail:'HP 6666 · 악의 돌진 13~666 / 5초 · 🧿 HP 66 소환 / 3초 · 무적 5초 + HP 500 / 13초'},\n"
once(roster_anchor,hell_roster,'hell roster')

# Hell demon engine skills
anchor='furballDeathHeal(dead,preHp){'
hell_engine=r'''spawnHellEye(owner){
 if(!owner||owner.health<=0)return null;
 const tmp=new Engine('hero','devileye',this.random,{mode:'control'}).fighters[1],a=this.rand(-Math.PI,Math.PI);
 tmp.side=this.fighters.length;tmp.team=owner.team;tmp.summon=true;tmp.ownerSide=owner.side;tmp.boss=false;tmp.scale=1;tmp.bodyScale=.72;tmp.radius=24;tmp.hp=66;tmp.health=66;tmp.damage=50;tmp.x=clamp(owner.x+Math.cos(a)*78,55,665);tmp.y=clamp(owner.y+Math.sin(a)*78,55,665);tmp.vx=Math.cos(a);tmp.vy=Math.sin(a);tmp.trail=[];tmp.deathOrder=null;tmp.poison=null;tmp.toxin=null;tmp.burn=null;tmp.bleed=null;tmp.curse=null;tmp.stunUntil=0;tmp.nextCursedHand=this.time+13;this.fighters.push(tmp);this.effect(owner,'🧿 악마의 눈 소환!','curse');return tmp
}
demonSkill(f,e,dt){
 if(!f||!['hell_clone','hell_demon'].includes(f.id)||f.health<=0)return;
 if(!Number.isFinite(f.hellDashNext)){f.hellDashNext=this.time+5;f.hellSummonNext=this.time+3;f.hellInvulnNext=this.time+13;f.hellInvulnUntil=0;f.hellDashUntil=0;f.hellDashHit=false}
 if(this.time>=f.hellInvulnNext-1e-9){
   if(Number.isFinite(f.hellObservedHealth)&&f.health<f.hellObservedHealth)f.hellDamageTaken=(f.hellDamageTaken||0)+(f.hellObservedHealth-f.health);
   f.hellInvulnNext=this.time+13;f.hellInvulnUntil=this.time+5;f.poison=null;f.toxin=null;f.burn=null;f.bleed=null;f.curse=null;
   const heal=Math.min(500,f.hp-f.health);f.health+=heal;f.healed=(f.healed||0)+heal;f.hellObservedHealth=f.health;this.effect(f,'👿 무적 5초 · +'+Math.round(heal),'heal');this.emit('👿 악마가 5초 무적 상태가 되고 HP 500 회복!')
 }
 if(this.time>=f.hellSummonNext-1e-9){f.hellSummonNext=this.time+3;this.spawnHellEye(f)}
 if(e&&e.health>0&&this.time>=f.hellDashNext-1e-9){const a=this.aim(f,e);f.hellDashNext=this.time+5;f.hellDashUntil=this.time+.65;f.hellDashDamage=13+Math.floor(this.random()*654);f.hellDashHit=false;f.dash=.65;f.vx=a.x;f.vy=a.y;f.turn=.65;this.effect(f,'👿 악의 돌진 '+f.hellDashDamage+'!','skill')}
}
'''
if s.count(anchor)!=1: raise SystemExit('hell engine anchor not unique')
s=s.replace(anchor,hell_engine+anchor,1)

# Hook demon skill in fighter loop
old_hook="if(f.id==='doctor')this.doctorSkill(f);if(f.id==='dragon')this.dragonMysticAttack(f,e);"
new_hook="if(f.id==='doctor')this.doctorSkill(f);if(f.id==='hell_clone'||f.id==='hell_demon')this.demonSkill(f,e,dt);if(f.id==='dragon')this.dragonMysticAttack(f,e);"
once(old_hook,new_hook,'demon skill hook')

# Demon dash collision before generic melee
old_contact="if(f.id==='devileye'&&f.health>0&&f.stunUntil<=this.time){const freshCurse=this.applyCurse(f,e);if(freshCurse&&e.health>0)this.attack(f,e,50*f.scale);}if(f.id==='boxer'"
new_contact="if(f.id==='devileye'&&f.health>0&&f.stunUntil<=this.time){const freshCurse=this.applyCurse(f,e);if(freshCurse&&e.health>0)this.attack(f,e,50*f.scale);}if((f.id==='hell_clone'||f.id==='hell_demon')&&f.health>0&&f.stunUntil<=this.time&&this.time<(f.hellDashUntil||0)&&!f.hellDashHit){const dealt=this.attack(f,e,f.hellDashDamage||13);if(dealt>0){f.hellDashHit=true;f.dash=0;this.effect(e,'👿 악의 돌진 −'+Math.round(dealt),'doom')}continue}if(f.id==='boxer'"
once(old_contact,new_contact,'demon dash collision')

# Exclude hell demons from generic collision melee
once("'goblin','goblin_king','psychic','furball','scientist','doctor'].includes(f.id)", "'goblin','goblin_king','psychic','furball','scientist','doctor','hell_clone','hell_demon'].includes(f.id)", 'generic melee exclusion')

# Invulnerability blocks normal damage
old_attack="attack(f,e,dmg,friendly=false,bypassDodge=false){\n if(e&&e.id==='crab'"
new_attack="attack(f,e,dmg,friendly=false,bypassDodge=false){\n if(e&&['hell_clone','hell_demon'].includes(e.id)&&(e.hellInvulnUntil||0)>this.time){if((e.hellInvulnFxAt||0)<=this.time){this.effect(e,'👿 무적!','skill');e.hellInvulnFxAt=this.time+.4}return 0}\n if(e&&e.id==='crab'"
once(old_attack,new_attack,'hell invulnerability attack guard')

# Prevent new status effects during invulnerability
for fn in ['applyPoison(f,e){','applyToxin(f,e){','applyBurn(f,e){','applyBleed(f,e){','applyCurse(source,e){']:
    if fn in s:
        s=s.replace(fn,fn+"\n if((e?.hellInvulnUntil||0)>this.time)return false;",1)
    else:
        raise SystemExit('status guard anchor missing: '+fn)

# Storage/progression: CH10 unlocks after CH9 complete
once("LAB_STAGE_KEY='neonRumble.labStages.v1',SHARK_UNLOCK_KEY", "LAB_STAGE_KEY='neonRumble.labStages.v1',HELL_STAGE_KEY='neonRumble.hellStages.v1',SHARK_UNLOCK_KEY", 'hell stage key')
once("forgeStageMask=0,boxingStageMask=0,labStageMask=0,skeletonsUnlocked", "forgeStageMask=0,boxingStageMask=0,labStageMask=0,hellStageMask=0,skeletonsUnlocked", 'hell stage state')
once("labStageMask=Number(localStorage.getItem(LAB_STAGE_KEY)||0)||0;psychicUnlocked=", "labStageMask=Number(localStorage.getItem(LAB_STAGE_KEY)||0)||0;hellStageMask=Number(localStorage.getItem(HELL_STAGE_KEY)||0)||0;psychicUnlocked=", 'hell stage load')
once("function chapter9Unlocked(){return (boxingStageMask&7)===7}", "function chapter9Unlocked(){return (boxingStageMask&7)===7}\nfunction chapter10Unlocked(){return (labStageMask&7)===7}", 'chapter10 unlock')
old_mark="function markLabStage(n){labStageMask|=(1<<(n-1));try{localStorage.setItem(LAB_STAGE_KEY,String(labStageMask))}catch{}updateChapter9UI();return (labStageMask&7)===7}"
new_mark="function markLabStage(n){const before=chapter10Unlocked();labStageMask|=(1<<(n-1));try{localStorage.setItem(LAB_STAGE_KEY,String(labStageMask))}catch{}updateChapter9UI();updateChapter10UI();return !before&&chapter10Unlocked()}\nfunction markHellStage(n){hellStageMask|=(1<<(n-1));try{localStorage.setItem(HELL_STAGE_KEY,String(hellStageMask))}catch{}updateChapter10UI();return (hellStageMask&7)===7}"
once(old_mark,new_mark,'hell progress')

# Stage skip supports CH10
old_skip="else if(!chapter9Unlocked()){boxingStageMask=7;localStorage.setItem(BOXING_STAGE_KEY,'7');label='CHAPTER 9'}else{alert('현재 해금할 다음 챕터가 없어!');return}"
new_skip="else if(!chapter9Unlocked()){boxingStageMask=7;localStorage.setItem(BOXING_STAGE_KEY,'7');label='CHAPTER 9'}else if(!chapter10Unlocked()){labStageMask=7;localStorage.setItem(LAB_STAGE_KEY,'7');label='CHAPTER 10'}else{alert('현재 해금할 다음 챕터가 없어!');return}"
once(old_skip,new_skip,'skip CH10')
once("updateChapter8UI();updateChapter9UI();renderForgeSystem();", "updateChapter8UI();updateChapter9UI();updateChapter10UI();renderForgeSystem();", 'skip CH10 UI refresh')

# Manual mode and control label
once("'forge','boxing','lab'].includes(mode)", "'forge','boxing','lab','hell'].includes(mode)", 'manual hell mode')
once("mode==='lab'?'털복숭이 이동 · '+controlName():'왼쪽 캐릭터 이동 · '+controlName()", "mode==='lab'?'털복숭이 이동 · '+controlName():mode==='hell'?'히어로 이동 · '+controlName():'왼쪽 캐릭터 이동 · '+controlName()", 'hell control label')

# HUD labels and CH10 stage update
once("function ability(f){if(f.id==='doctor')", "function ability(f){if(f.id==='hell_demon'||f.id==='hell_clone')return '👿 돌진 '+Math.max(0,(f.hellDashNext||5)-engine.time).toFixed(1)+'초 · 소환 '+Math.max(0,(f.hellSummonNext||3)-engine.time).toFixed(1)+'초 · '+((f.hellInvulnUntil||0)>engine.time?'무적 '+(f.hellInvulnUntil-engine.time).toFixed(1)+'초':'무적까지 '+Math.max(0,(f.hellInvulnNext||13)-engine.time).toFixed(1)+'초');if(f.id==='doctor')", 'hell ability')
once("function hud(){if(!engine)return;if(mode==='lab')updateLabStage();", "function hud(){if(!engine)return;if(mode==='lab')updateLabStage();if(mode==='hell')updateHellStage();", 'hell HUD update')

# Replace stage UI function so CH9/CH10 behave like classic chapters and never leak panels
start=s.index('function updateStageUI(){')
end=s.index('\nfunction hideStageSelectionPanels(){',start)
old=s[start:end]
new="""function updateStageUI(){const on=mode==='stage',desertSelect=mode==='desert-select',mansionSelect=mode==='mansion-select',spaceSelect=mode==='space-select',casinoSelect=mode==='casino-select',oceanSelect=mode==='ocean-select',forgeSelect=mode==='forge-select',boxingSelect=mode==='boxing-select',labSelect=mode==='lab-select',hellSelect=mode==='hell-select',special=on||desertSelect||mansionSelect||spaceSelect||casinoSelect||oceanSelect||forgeSelect||boxingSelect||labSelect||hellSelect;document.querySelector('.section-title').hidden=special;document.querySelector('.versus').hidden=special;$('start').hidden=special;document.querySelector('.pick-heading').hidden=special;$('character-search').hidden=special;$('roster').hidden=special;document.querySelector('.match-info').hidden=special;$('stage-entry').hidden=special;$('boss-control-entry').hidden=special;$('chapter2-entry').hidden=special;$('chapter3-entry').hidden=special;$('chapter4-entry').hidden=special;$('chapter5-entry').hidden=special;$('chapter6-entry').hidden=special;$('chapter7-entry').hidden=special;$('chapter8-entry').hidden=special;if($('chapter9-entry'))$('chapter9-entry').hidden=special;if($('chapter10-entry'))$('chapter10-entry').hidden=special;$('stage-panel').hidden=!on;$('desert-panel').hidden=!desertSelect;$('mansion-panel').hidden=!mansionSelect;$('space-panel').hidden=!spaceSelect;$('casino-panel').hidden=!casinoSelect;$('ocean-panel').hidden=!oceanSelect;$('forge-panel').hidden=!forgeSelect;$('boxing-panel').hidden=!boxingSelect;if($('lab-selection'))$('lab-selection').hidden=!labSelect;if($('hell-selection'))$('hell-selection').hidden=!hellSelect;if(special){$('relay-rules').hidden=true;$('relay-picker').hidden=true;$('squad-picker').hidden=true;$('boss-rules').hidden=true}$('mode-duel').setAttribute('aria-pressed',String(mode==='duel'));$('mode-boss').setAttribute('aria-pressed',String(isBossMode()));$('mode-relay').setAttribute('aria-pressed',String(mode==='relay'));$('mode-group').setAttribute('aria-pressed',String(mode==='group'));$('mode-control').setAttribute('aria-pressed',String(mode==='control'));updateControlBossUnlockUI();updateChapter2UI();updateChapter3UI();updateChapter4UI();updateChapter5UI();updateChapter6UI();updateChapter7UI();updateChapter8UI();updateChapter9UI();updateChapter10UI()}"""
s=s[:start]+new+s[end:]
once("['stage-panel','desert-panel','mansion-panel','space-panel','casino-panel','ocean-panel','forge-panel','boxing-panel','lab-selection']", "['stage-panel','desert-panel','mansion-panel','space-panel','casino-panel','ocean-panel','forge-panel','boxing-panel','lab-selection','hell-selection']", 'hide hell panel')
once("mode==='boxing-select';if(!stageWas)", "mode==='boxing-select'||mode==='lab-select'||mode==='hell-select';if(!stageWas)", 'stageWas dynamic chapters')

# CH9 click now routes through classic updateSelection
once("b.onclick=()=>{if(!chapter9Unlocked())return;mode='lab-select';hideStageSelectionPanels();p.hidden=false;updateChapter9UI();p.scrollIntoView({behavior:'smooth',block:'start'})};", "b.onclick=()=>{if(!chapter9Unlocked())return;mode='lab-select';updateSelection();updateChapter9UI();p.scrollIntoView({behavior:'smooth',block:'start'})};", 'CH9 classic navigation')
once("$('lab-back').onclick=()=>{p.hidden=true;mode='duel';window.scrollTo({top:0,behavior:'smooth'})};", "$('lab-back').onclick=()=>{mode='duel';updateSelection();window.scrollTo({top:0,behavior:'smooth'})};", 'CH9 back navigation')

# Generic start/selection/rematch routes for hell
once("if(mode==='lab'){engine=null;mode='duel'}engine=mode==='group'?", "if(mode==='lab'||mode==='lab-select'||mode==='hell'||mode==='hell-select'){engine=null;mode='duel'}engine=mode==='group'?", 'generic start hell reset')
once("if(mode==='lab'){engine=null;mode='duel'}engine=null;paused=false;", "if(mode==='lab'||mode==='lab-select'||mode==='hell'||mode==='hell-select'){engine=null;mode='duel'}engine=null;paused=false;", 'selection hell reset')
once("mode==='lab'?startLabStage(labStageNo):start();", "mode==='lab'?startLabStage(labStageNo):mode==='hell'?startHellStage(hellStageNo):start();", 'hell rematch')

# CH9 result unlocks CH10 and add CH10 result branch
old_lab_result="else if(mode==='lab'&&engine.result===0){const coinReward=awardStageCoins(labStageNo),doctorRoll=labStageNo===3?tryUnlockDoctor():null;markLabStage(labStageNo);$('winner-icon').textContent='🧪';$('winner').textContent='CHAPTER 9 · STAGE '+labStageNo+' 클리어!';$('summary').textContent=t+'초 · 실험실 탈출 성공 · 🪙 '+coinReward+'코인 획득!'+(doctorRoll==='won'?' · 🎁 10% 보상 성공! 👨‍⚕️ 의사 획득!':doctorRoll==='miss'?' · 🎲 의사 획득 실패 (10%)':'')}else if(mode==='lab'){$('winner-icon').textContent='🧪';$('winner').textContent='CHAPTER 9 · STAGE '+labStageNo+' 실패';$('summary').textContent=t+'초 · 털복숭이가 쓰러졌어. 다시 탈출해 봐.'}else{"
new_lab_result="else if(mode==='lab'&&engine.result===0){const coinReward=awardStageCoins(labStageNo),doctorRoll=labStageNo===3?tryUnlockDoctor():null,chapter10Now=markLabStage(labStageNo);$('winner-icon').textContent='🧪';$('winner').textContent='CHAPTER 9 · STAGE '+labStageNo+' 클리어!';$('summary').textContent=t+'초 · 실험실 탈출 성공 · 🪙 '+coinReward+'코인 획득!'+(doctorRoll==='won'?' · 🎁 10% 보상 성공! 👨‍⚕️ 의사 획득!':doctorRoll==='miss'?' · 🎲 의사 획득 실패 (10%)':'')+(chapter10Now?' · 🔥 CHAPTER 10 해금!':'')}else if(mode==='lab'){$('winner-icon').textContent='🧪';$('winner').textContent='CHAPTER 9 · STAGE '+labStageNo+' 실패';$('summary').textContent=t+'초 · 털복숭이가 쓰러졌어. 다시 탈출해 봐.'}else if(mode==='hell'&&engine.result===0){const coinReward=awardStageCoins(hellStageNo);markHellStage(hellStageNo);$('winner-icon').textContent='🔥';$('winner').textContent='CHAPTER 10 · STAGE '+hellStageNo+' 클리어!';$('summary').textContent=t+'초 · 지옥 돌파 성공 · 🪙 '+coinReward+'코인 획득!'}else if(mode==='hell'){$('winner-icon').textContent='👿';$('winner').textContent='CHAPTER 10 · STAGE '+hellStageNo+' 실패';$('summary').textContent=t+'초 · 히어로가 쓰러졌어. 다시 지옥에 도전해 봐.'}else{"
once(old_lab_result,new_lab_result,'CH10 result branch')

# Hell background: do not let wardrobe background override it
once("'forge','boxing','lab'].includes(mode)", "'forge','boxing','lab','hell'].includes(mode)", 'hell wardrobe background exclusion')
# Insert hell background before generic arena fallback
lab_bg_end="ctx.globalAlpha=1}else{ctx.fillStyle='#101c2d';ctx.fillRect(0,0,720,720)}"
hell_bg="ctx.globalAlpha=1}else if(mode==='hell'){const hg=ctx.createLinearGradient(0,0,0,720);hg.addColorStop(0,'#35070a');hg.addColorStop(.42,'#1d0808');hg.addColorStop(1,'#080203');ctx.fillStyle=hg;ctx.fillRect(0,0,720,720);ctx.save();ctx.globalAlpha=.22;ctx.fillStyle='#ff3b1f';for(let i=0;i<8;i++){ctx.beginPath();ctx.arc(70+i*92,690-(i%3)*18,70+(i%2)*25,Math.PI,Math.PI*2);ctx.fill()}ctx.globalAlpha=.34;ctx.font='48px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.fillText('🔥',85,610);ctx.fillText('🔥',635,600);ctx.fillText('⛓️',95,150);ctx.fillText('⛓️',625,145);ctx.globalAlpha=.18;ctx.strokeStyle='#ff5a36';ctx.lineWidth=5;for(let y=180;y<650;y+=115){ctx.beginPath();ctx.moveTo(40,y);ctx.lineTo(680,y+35);ctx.stroke()}ctx.restore()}else{ctx.fillStyle='#101c2d';ctx.fillRect(0,0,720,720)}"
once(lab_bg_end,hell_bg,'hell background')
# Grid/battle title color/text
once("mode==='lab'?'#2b7772':'#1c2d42'", "mode==='lab'?'#2b7772':mode==='hell'?'#7f241d':'#1c2d42'", 'hell grid color')
once("mode==='lab'?'LABORATORY ESCAPE · STAGE '+labStageNo:mode==='stage'", "mode==='lab'?'LABORATORY ESCAPE · STAGE '+labStageNo:mode==='hell'?'HELL · STAGE '+hellStageNo:mode==='stage'", 'hell arena label')

# Invulnerability visual ring
old_shadow="circle(f.x,f.y+10,r+3,'#02071066');if(f.id==='old_tv'"
new_shadow="circle(f.x,f.y+10,r+3,'#02071066');if((f.id==='hell_clone'||f.id==='hell_demon')&&f.health>0&&(f.hellInvulnUntil||0)>engine.time){ctx.save();ctx.globalAlpha=.65+.2*Math.sin(engine.time*10);ctx.strokeStyle='#ffcf66';ctx.shadowColor='#ff3a1a';ctx.shadowBlur=22;ctx.lineWidth=7;ctx.beginPath();ctx.arc(f.x,f.y,r+16,0,Math.PI*2);ctx.stroke();ctx.restore()}if(f.id==='old_tv'"
once(old_shadow,new_shadow,'hell invulnerability visual')

# Dynamic CHAPTER 10 UI/runtime inserted before setupChapter9UI call
insert_anchor='setupChapter9UI();\n})();'
hell_ui=r'''let hellStageNo=1,hellAllyId='knight';
function refreshHellAllyOptions(){const sel=$('hell-ally-select');if(!sel)return;const current=sel.value||hellAllyId,playable=ROSTER.filter(c=>!c.stageOnly&&!characterLocked(c)&&c.id!=='hero');sel.innerHTML=playable.map(c=>'<option value="'+c.id+'">'+c.icon+' '+c.name+'</option>').join('');if(playable.some(c=>c.id===current))sel.value=current;else if(playable.length)sel.value=playable[0].id;hellAllyId=sel.value||'knight'}
function updateChapter10UI(){const b=$('chapter10-entry');if(!b)return;const ok=chapter10Unlocked(),d1=!!(hellStageMask&1),d2=!!(hellStageMask&2),d3=!!(hellStageMask&4),count=(d1?1:0)+(d2?1:0)+(d3?1:0);b.disabled=!ok;b.textContent=ok?'🔥 CHAPTER 10 · 지옥'+(count?' · '+count+'/3':''):'🔒 CHAPTER 10 · CHAPTER 9 STAGE 1·2·3 클리어 필요';const prog=$('hell-progress');if(prog)prog.textContent='진행도 '+count+' / 3'+(d3?' · ✅ CHAPTER 10 COMPLETE':'');const data=[['hell-1','hell-status-1',d1,true],['hell-2','hell-status-2',d2,d1],['hell-3','hell-status-3',d3,d1&&d2]];for(const [id,sid,done,open] of data){const x=$(id),st=$(sid);if(!x)continue;x.disabled=!ok||!open;if(st)st.textContent=done?'✅ 클리어':open?'도전 가능':'🔒 이전 STAGE 클리어 필요'}refreshHellAllyOptions()}
function setupChapter10UI(){if($('chapter10-entry')){updateChapter10UI();return}const after=$('chapter9-entry'),sel=$('selection');if(!after||!sel)return;const b=document.createElement('button');b.id='chapter10-entry';b.type='button';b.className=after.className;after.insertAdjacentElement('afterend',b);const p=document.createElement('section');p.id='hell-selection';p.className='chapter-stage-panel';p.hidden=true;p.innerHTML='<div class="section-title"><div><p class="eyebrow">CHAPTER 10</p><h2>🔥 지옥</h2></div><span id="hell-progress" class="card-tag">진행도 0 / 3</span></div><p class="match-info">주인공 🦸 히어로로 지옥을 돌파해. STAGE 3에서는 조력자 1명을 선택할 수 있어.</p><div class="roster hell-stage-grid"><button id="hell-1" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">🧿</span><span><strong class="card-name">STAGE 1 · 악마의 눈</strong><small id="hell-status-1" class="card-tag">도전 가능</small></span></span><span class="card-desc">악마의 눈 HP 2500</span></button><button id="hell-2" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">👿</span><span><strong class="card-name">STAGE 2 · 악마의 분신</strong><small id="hell-status-2" class="card-tag">🔒 이전 STAGE 클리어 필요</small></span></span><span class="card-desc">HP 666 · 악의 돌진 · 악의 소환 · 13초마다 5초 무적+500 회복</span></button><button id="hell-3" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">👿</span><span><strong class="card-name">STAGE 3 · 악마</strong><small id="hell-status-3" class="card-tag">🔒 이전 STAGE 클리어 필요</small></span></span><span class="card-desc">HP 6666 · 누적 1500 피해마다 히어로/조력자 HP 500 회복</span></button></div><div class="match-info"><label for="hell-ally-select"><strong>STAGE 3 조력자</strong></label><select id="hell-ally-select" style="width:100%;margin-top:8px"></select></div><div class="controls"><button id="hell-back" type="button">← 챕터 목록으로</button></div>';sel.appendChild(p);const style=document.createElement('style');style.id='chapter10-hell-ui';style.textContent='#hell-selection{margin:18px 0 24px;padding:18px;background:#1a0b0d;border:1px solid #6b2c28;border-radius:14px}#hell-selection .hell-stage-grid{margin-top:14px}#hell-selection .fighter-card{width:100%;min-height:150px}#hell-selection .fighter-card:disabled{opacity:.48;filter:saturate(.45)}#hell-selection .card-top>span:last-child{display:flex;flex-direction:column;gap:4px;min-width:0}@media(max-width:560px){#hell-selection{padding:14px 10px}#hell-selection .hell-stage-grid{grid-template-columns:1fr}#hell-selection .fighter-card{min-height:0}}';document.head.appendChild(style);b.onclick=()=>{if(!chapter10Unlocked())return;mode='hell-select';updateSelection();updateChapter10UI();p.scrollIntoView({behavior:'smooth',block:'start'})};$('hell-back').onclick=()=>{mode='duel';updateSelection();window.scrollTo({top:0,behavior:'smooth'})};$('hell-ally-select').onchange=()=>{hellAllyId=$('hell-ally-select').value};$('hell-1').onclick=()=>startHellStage(1);$('hell-2').onclick=()=>{if(hellStageMask&1)startHellStage(2)};$('hell-3').onclick=()=>{if((hellStageMask&3)===3)startHellStage(3)};updateChapter10UI()}
function makeHellAlly(id){const tmp=new Engine(id,'hero',Math.random,{mode:'control'}).fighters[0];tmp.side=engine.fighters.length;tmp.team=0;tmp.summon=true;tmp.hellAlly=true;tmp.ownerSide=0;tmp.boss=false;tmp.x=205;tmp.y=535;tmp.vx=0;tmp.vy=-1;tmp.trail=[];tmp.deathOrder=null;engine.fighters.push(tmp);if(tmp.id==='aladdin'&&typeof engine.spawnGenie==='function')engine.spawnGenie(tmp);if(tmp.skeletonBundle&&typeof engine.spawnSkeletonBundleMates==='function')engine.spawnSkeletonBundleMates(tmp);return tmp}
function healHellTeam(amount){if(!engine)return;for(const f of engine.fighters.filter(x=>x.team===0&&x.health>0&&(x.id==='hero'||x.hellAlly))){const heal=Math.min(amount,f.hp-f.health);f.health+=heal;f.healed=(f.healed||0)+heal;if(heal)engine.effect(f,'🔥 +'+Math.round(heal),'heal')}}
function startHellStage(n){hellStageNo=n;mode='hell';if(n===1){engine=new Engine('hero','devileye',Math.random,{mode:'control'});const b=engine.fighters[1];b.hp=2500;b.health=2500}else if(n===2){engine=new Engine('hero','hell_clone',Math.random,{mode:'control'});const b=engine.fighters[1];b.hp=666;b.health=666}else{engine=new Engine('hero','hell_demon',Math.random,{mode:'control'});const b=engine.fighters[1];b.hp=6666;b.health=6666;b.hellBoss=true;b.hellDamageTaken=0;b.hellNextTeamHeal=1500;b.hellObservedHealth=6666;refreshHellAllyOptions();makeHellAlly(hellAllyId)}engine.hellMode=true;paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';hideStageSelectionPanels();$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';resetStick();refreshControlUI();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent=n===3?'🦸 히어로 + 조력자':'🦸 히어로';$('score-label1').textContent=n===1?'🧿 악마의 눈':n===2?'👿 악마의 분신':'👿 악마';$('battle-mode').textContent='HELL '+n;$('battle-info').textContent=n===1?'CHAPTER 10 STAGE 1 · HP 2500 악마의 눈을 쓰러트려.':n===2?'CHAPTER 10 STAGE 2 · 악마의 분신 HP 666 · 악의 돌진 13~666/5초 · 악마의 눈 HP 66 소환/3초 · 무적 5초+HP 500/13초.':'CHAPTER 10 STAGE 3 · 악마 HP 6666 · 선택 조력자 '+(ROSTER.find(c=>c.id===hellAllyId)?.name||hellAllyId)+' · 누적 1500 피해마다 히어로와 조력자 HP 500 회복.';fit();hud();draw();window.scrollTo({top:0,behavior:'auto'});playSfx('start')}
function updateHellStage(){if(mode!=='hell'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.id==='hero'&&f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}const boss=engine.fighters.find(f=>f.team===1&&!f.summon);if(!boss||boss.health<=0){engine.result=0;return}if(hellStageNo===3&&boss.id==='hell_demon'){if(!Number.isFinite(boss.hellObservedHealth))boss.hellObservedHealth=boss.health;if(boss.health<boss.hellObservedHealth)boss.hellDamageTaken=(boss.hellDamageTaken||0)+(boss.hellObservedHealth-boss.health);boss.hellObservedHealth=boss.health;while((boss.hellDamageTaken||0)>=(boss.hellNextTeamHeal||1500)){healHellTeam(500);boss.hellNextTeamHeal=(boss.hellNextTeamHeal||1500)+1500;engine.emit('🔥 악마에게 누적 '+(boss.hellNextTeamHeal-1500)+' 피해! 히어로와 조력자 HP 500 회복!')}}}
setupChapter9UI();setupChapter10UI();
})();'''
once(insert_anchor,hell_ui,'CH10 UI/runtime')

p.write_text(s,encoding='utf-8')
print('v3.72 patch applied')

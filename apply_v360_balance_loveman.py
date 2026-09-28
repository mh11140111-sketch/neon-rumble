from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if s.count(old)<count:
        raise SystemExit(f'PATCH FAILED: {label} (found {s.count(old)})')
    s=s.replace(old,new,count)

# Version + patch notes
rep('BATTLE <b>v3.59</b>','BATTLE <b>v3.60</b>','version')
rep('📒 패치노트 · v3.59','📒 패치노트 · v3.60','notes summary')
anchor='<div class="patch-body"><div class="patch-version"><h3>v3.59'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.60 · 밸런스 · 대장간 배경 · 사랑의 남자</h3><ul><li>🔨 CHAPTER 7 STAGE 1·2: 도깨비 웨이브 5 → 3.</li><li>🦈 상어: 일반 물기 피해 50 → 70. 스테이지와 샌드박스 모두 적용하며 대쉬/출혈 수치는 유지.</li><li>🛒 CHAPTER 7 STAGE 1·2·3 클리어 시 대장간 배경을 상점에서 구매 가능.</li><li>😍 사랑의 남자 추가: 1.5초마다 ❤️‍🔥/❤️/💖/💓 중 하나를 각 25% 확률로 사용.</li><li>💓 유혹: 피해 50 + 3초 동안 공격/스킬 불가, 사랑의 남자에게 강제로 접근.</li></ul></div><div class="patch-version"><h3>v3.59'
rep(anchor,insert,'patch notes')

# Forge stages 5 -> 3 in UI / info / logic
rep('HP 300 도깨비 3마리씩 5웨이브 · 방망이 80 / 3초','HP 300 도깨비 3마리씩 3웨이브 · 방망이 80 / 3초','forge ui 1')
rep('STAGE 1과 동일한 도깨비 군단 3마리씩 5웨이브','STAGE 1과 동일한 도깨비 군단 3마리씩 3웨이브','forge ui 2')
rep("'🔨 WAVE '+forgeWave+' / 5 · 👹 도깨비 3마리 침입!'","'🔨 WAVE '+forgeWave+' / 3 · 👹 도깨비 3마리 침입!'",'forge wave event')
rep("'CHAPTER 7 STAGE '+n+' · 도깨비 HP 300 · 3마리씩 총 5웨이브 · 작은 범위 방망이 피해 80 / 3초 · 웨이브마다 대장장이 최대 HP 30% 회복.'","'CHAPTER 7 STAGE '+n+' · 도깨비 HP 300 · 3마리씩 총 3웨이브 · 작은 범위 방망이 피해 80 / 3초 · 웨이브마다 대장장이 최대 HP 30% 회복.'",'forge battle info')
rep('if(forgeWave>=5)engine.result=0','if(forgeWave>=3)engine.result=0','forge wave clear')

# Shark basic bite 70; dash stays 50
rep("{id:'shark',name:'상어',icon:'🦈',tag:'대쉬 · 출혈',hp:1000,damage:50,speed:190,cooldown:3,unlock:'shark',description:'3초마다 가장 가까운 적에게 대쉬해 피해 50을 주고 6초 출혈을 건다. 출혈은 0.5초마다 피해 15.',detail:'HP 1000 · 대쉬 50 / 3초 · 출혈 6초 · 0.5초마다 15'}",
    "{id:'shark',name:'상어',icon:'🦈',tag:'물기 · 대쉬 · 출혈',hp:1000,damage:70,speed:190,cooldown:3,unlock:'shark',description:'기본 물기 피해 70. 3초마다 가장 가까운 적에게 대쉬해 피해 50을 주고 6초 출혈을 건다. 출혈은 0.5초마다 피해 15.',detail:'HP 1000 · 기본 물기 70 · 대쉬 50 / 3초 · 출혈 6초 · 0.5초마다 15'}",'shark roster')
rep("this.attack(f,e,50*f.scale);f.cd=1/f.scale;this.effect(f,'🦈 물기 50','skill')","this.attack(f,e,70*f.scale);f.cd=1/f.scale;this.effect(f,'🦈 물기 70','skill')",'shark bite')
rep("'CHAPTER 6 STAGE 2 · 상어 HP 1000 · 3초 대쉬 피해 50 · 출혈 6초, 0.5초마다 15 · 클리어 시 20% 획득.'","'CHAPTER 6 STAGE 2 · 상어 HP 1000 · 기본 물기 70 · 3초 대쉬 피해 50 · 출혈 6초, 0.5초마다 15 · 클리어 시 20% 획득.'",'shark stage info')

# Forge background shop item + unlock logic
bg_anchor=" {id:'bg_casino',name:'도박장 배경',icon:'🎲',price:1000,type:'background',chapter:5,backgroundStyle:'casino',exclusiveFor:null,desc:'CHAPTER 5 스테이지 1·2·3 클리어 후 구매 가능'},"
bg_new=bg_anchor+"\n {id:'bg_forge',name:'대장간 배경',icon:'🔨',price:1000,type:'background',chapter:7,backgroundStyle:'forge',exclusiveFor:null,desc:'CHAPTER 7 스테이지 1·2·3 클리어 후 구매 가능'},"
rep(bg_anchor,bg_new,'forge background item')
rep("item.chapter===5?(casinoStageMask&7)===7:false}","item.chapter===5?(casinoStageMask&7)===7:item.chapter===7?(forgeStageMask&7)===7:false}",'background unlock chapter7')
rep("function markForgeStage(n){forgeStageMask|=(1<<(n-1));try{localStorage.setItem(FORGE_STAGE_KEY,String(forgeStageMask))}catch{}return (forgeStageMask&7)===7}","function markForgeStage(n){forgeStageMask|=(1<<(n-1));try{localStorage.setItem(FORGE_STAGE_KEY,String(forgeStageMask))}catch{}renderShop();return (forgeStageMask&7)===7}",'forge mark shop refresh')

# Love Man roster entry before zombie mage
roster_anchor="{id:'zombie_mage',name:'법사좀비'"
love="{id:'loveman',name:'사랑의 남자',icon:'😍',tag:'유도 하트 · 회복 · 유혹',hp:1000,damage:40,speed:150,cooldown:1.5,description:'1.5초마다 네 종류의 하트 중 하나를 각 25% 확률로 사용한다. ❤️‍🔥 피해 40+화상, ❤️ 아군 50 회복(아군이 없으면 자기 회복), 💖 피해 40+1초 기절, 💓 피해 50+3초 유혹.',detail:'HP 1000 · 1.5초 · ❤️‍🔥 40+화상 25% · ❤️ 아군 50회복 25% · 💖 40+기절1초 25% · 💓 50+유혹3초 25%'},\n"
rep(roster_anchor,love+roster_anchor,'love man roster')

# Love Man skill before stepFighter
step_anchor='stepFighter(f,e,dt){\n'
love_skill="""loveManSkill(f,e){
 if(!f||f.id!=='loveman'||f.health<=0||f.stunUntil>this.time||f.cd>1e-9)return;
 const r=this.random();f.cd=1.5/f.scale;f.attack=.18/f.scale;
 if(r>=.25&&r<.5){
   const allies=this.fighters.filter(a=>a!==f&&a.team===f.team&&a.health>0&&!a.summon);const ally=allies.sort((a,b)=>(a.health/a.hp)-(b.health/b.hp))[0];
   if(!ally){const heal=Math.min(f.hp-f.health,50*f.scale);f.health+=heal;f.healed+=heal;if(heal)this.effect(f,'❤️ +'+Math.round(heal),'heal');return}
   const a=this.aim(f,ally);this.shots.push({x:f.x+a.x*(f.radius+9),y:f.y+a.y*(f.radius+9),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:ally.side,kind:'love_heal',icon:'❤️',radius:10*f.scale,speed:330*f.scale,damage:0,life:5/f.scale,bounces:0});this.effect(f,'❤️ 사랑의 회복!','skill');return
 }
 if(!e||e.health<=0)return;const a=this.aim(f,e),kind=r<.25?'love_burn':r<.75?'love_stun':'love_charm',icon=kind==='love_burn'?'❤️‍🔥':kind==='love_stun'?'💖':'💓',damage=(kind==='love_charm'?50:40)*f.scale;
 this.shots.push({x:f.x+a.x*(f.radius+9),y:f.y+a.y*(f.radius+9),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind,icon,radius:11*f.scale,speed:350*f.scale,damage,life:5/f.scale,bounces:0});this.effect(f,icon+' 하트 공격!','skill')
}
"""
rep(step_anchor,love_skill+step_anchor,'love skill')

# Charm control at top of stepFighter, then dispatch Love Man skill
rep("stepFighter(f,e,dt){\n if(f.id==='genie')", "stepFighter(f,e,dt){\n if((f.charmUntil||0)>this.time){const src=this.fighters[f.charmSource];if(src&&src.health>0&&src.team!==f.team){const a=this.aim(f,src),spd=f.speed*(1-Math.max(f.slowPower||0,f.rootSlowPower||0));f.vx=a.x;f.vy=a.y;f.x+=a.x*spd*dt;f.y+=a.y*spd*dt;this.keepInside(f);f.attack=0;return}else{f.charmUntil=0;f.charmSource=null}}\n if(f.id==='genie')",'charm movement')
rep("if(f.id==='dragon')this.dragonMysticAttack(f,e);if(f.id==='detective')", "if(f.id==='dragon')this.dragonMysticAttack(f,e);if(f.id==='loveman')this.loveManSkill(f,e);if(f.id==='detective')",'love dispatch')

# Exclude Love Man from generic collision attack
rep("'crab_shell','dragon','alien'", "'crab_shell','dragon','loveman','alien'",'love generic contact exclusion')

# Homing hearts + collision handling
rep("(s.kind==='magic'||s.kind==='curseorb'||s.kind==='zombiemagic'||((target?.magnifiedUntil||0)>this.time))", "(s.kind==='magic'||s.kind==='curseorb'||s.kind==='zombiemagic'||s.kind.startsWith('love_')||((target?.magnifiedUntil||0)>this.time))",'love homing')
heart_anchor="  if(['dragon_wind','dragon_thunder','dragon_bubble','dragon_leaf'].includes(s.kind)){"
heart_branch="""  if(['love_burn','love_heal','love_stun','love_charm'].includes(s.kind)){
   if(s.kind==='love_heal'){
    const ally=this.fighters[s.target];if(!ally||ally.health<=0||ally.team!==f.team){s.life=0;continue}if(distance(s,ally)<ally.radius+s.radius){const heal=Math.min(ally.hp-ally.health,50*f.scale);ally.health+=heal;ally.healed+=heal;if(heal)this.effect(ally,'❤️ +'+Math.round(heal),'heal');s.life=0}if(s.x<22||s.x>698||s.y<22||s.y>698)s.life=0;continue
   }
   const hit=this.enemies(f).find(e=>distance(s,e)<e.radius+s.radius);if(hit){const dealt=this.attack(f,hit,s.damage);if(dealt>0&&hit.health>0){if(s.kind==='love_burn'){this.applyBurn(f,hit);this.effect(hit,'❤️‍🔥 화상!','burn')}else if(s.kind==='love_stun'){hit.stunUntil=Math.max(hit.stunUntil,this.time+1*f.scale);this.effect(hit,'💖 기절 1초!','skill')}else if(s.kind==='love_charm'){hit.charmUntil=Math.max(hit.charmUntil||0,this.time+3*f.scale);hit.charmSource=f.side;this.effect(hit,'💓 유혹 3초!','skill')}}s.life=0;if(this.result!==null)break}if(s.x<22||s.x>698||s.y<22||s.y>698)s.life=0;continue
  }
"""
rep(heart_anchor,heart_branch+heart_anchor,'heart shot handling')

# Render heart projectiles
render_anchor="if(['dragon_wind','dragon_thunder','dragon_bubble','dragon_leaf'].includes(s.kind)){"
render_new="if(['love_burn','love_heal','love_stun','love_charm'].includes(s.kind)){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(Math.max(26,s.radius*2.8))+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(s.kind==='love_burn'?'❤️‍🔥':s.kind==='love_heal'?'❤️':s.kind==='love_stun'?'💖':'💓',0,0)}else if(['dragon_wind','dragon_thunder','dragon_bubble','dragon_leaf'].includes(s.kind)){"
rep(render_anchor,render_new,'heart render')

# HUD charm status
rep("+(f.bleed?' · 🩸 출혈 '+Math.max(0,f.bleed.expires-engine.time).toFixed(1)+'초':'')+((f.cowUntil||0)>engine.time?", "+(f.bleed?' · 🩸 출혈 '+Math.max(0,f.bleed.expires-engine.time).toFixed(1)+'초':'')+((f.charmUntil||0)>engine.time?' · 💓 유혹 '+Math.max(0,f.charmUntil-engine.time).toFixed(1)+'초':'')+((f.cowUntil||0)>engine.time?",'hud charm')

# Wardrobe forge background rendering: insert before casino fallback in wardrobe background branch
wardrobe_old="}else{const g=ctx.createLinearGradient(0,0,0,720);g.addColorStop(0,'#30110f');g.addColorStop(.5,'#130d18');g.addColorStop(1,'#07120c');ctx.fillStyle=g;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.34;ctx.font='42px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.fillText('🎰',92,150);ctx.fillText('🎲',625,170);ctx.fillText('♠️',105,600);ctx.fillText('♦️',615,590);ctx.globalAlpha=1}}else if(mode==='desert')"
wardrobe_new="}else if(st==='forge'){const fg=ctx.createLinearGradient(0,0,0,720);fg.addColorStop(0,'#40251a');fg.addColorStop(.52,'#25150f');fg.addColorStop(1,'#120b09');ctx.fillStyle=fg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.5;ctx.font='42px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.fillText('🔥',90,145);ctx.fillText('⚒️',625,595);ctx.fillText('🧱',105,610);ctx.globalAlpha=1}else{const g=ctx.createLinearGradient(0,0,0,720);g.addColorStop(0,'#30110f');g.addColorStop(.5,'#130d18');g.addColorStop(1,'#07120c');ctx.fillStyle=g;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.34;ctx.font='42px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.fillText('🎰',92,150);ctx.fillText('🎲',625,170);ctx.fillText('♠️',105,600);ctx.fillText('♦️',615,590);ctx.globalAlpha=1}}else if(mode==='desert')"
rep(wardrobe_old,wardrobe_new,'forge wardrobe background')

p.write_text(s,encoding='utf-8')
print('v3.60 patch applied')

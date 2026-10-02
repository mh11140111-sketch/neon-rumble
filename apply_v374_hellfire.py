from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1, got {n}')
    s=s.replace(old,new,1)

# Version + newest patch note.
once('BATTLE <b>v3.73</b>','BATTLE <b>v3.74</b>','version')
once('<summary>📒 패치노트 · v3.73</summary><div class="patch-body">',
     '<summary>📒 패치노트 · v3.74</summary><div class="patch-body"><div class="patch-version"><h3>v3.74 · 악마 밸런스 · 지옥의 불</h3><ul><li>👿 악마와 악마의 분신에 신규 공격 「지옥의 불」 추가. 2.5초마다 피해 66의 보라색 불을 던지고, 명중한 적에게 사망할 때까지 0.66초마다 피해 13의 지옥의 화상을 부여.</li><li>👿 샌드박스 악마만 무적 지속시간 5초 → 1.3초, 무적 발동 회복량 500 → 136으로 조정.</li><li>🔥 CHAPTER 10 악마/분신의 기존 돌진·소환·무적 수치는 유지하고 지옥의 불만 추가.</li></ul></div>',
     'patch note')

# Roster text.
once(
"{id:'hell_clone',name:'악마의 분신',icon:'👿',tag:'악의 돌진 · 악의 소환 · 무적',hp:666,damage:13,speed:170,cooldown:0,stageOnly:true,description:'5초마다 악의 돌진, 3초마다 HP 66 악마의 눈 소환, 13초마다 5초 무적과 HP 500 회복을 사용한다.',detail:'HP 666 · 악의 돌진 13~666 / 5초 · 🧿 HP 66 소환 / 3초 · 무적 5초 + HP 500 / 13초'},",
"{id:'hell_clone',name:'악마의 분신',icon:'👿',tag:'악의 돌진 · 악의 소환 · 무적 · 지옥의 불',hp:666,damage:13,speed:170,cooldown:0,stageOnly:true,description:'5초마다 악의 돌진, 3초마다 HP 66 악마의 눈 소환, 13초마다 5초 무적과 HP 500 회복. 2.5초마다 피해 66의 보라색 지옥의 불을 던져 사망할 때까지 지옥의 화상을 부여한다.',detail:'HP 666 · 악의 돌진 13~666 / 5초 · 🧿 HP 66 소환 / 3초 · 무적 5초 + HP 500 / 13초 · 🟣🔥 지옥의 불 66 / 2.5초 · 지옥의 화상 13 / 0.66초 · 사망 시 해제'},",
'clone roster')
once(
"{id:'hell_demon',name:'악마',icon:'👿',tag:'악의 돌진 · 악의 소환 · 무적',hp:1366,damage:13,speed:175,cooldown:0,unlock:'hellDemon',description:'5초마다 악의 돌진으로 피해 13~166. 13초마다 HP 66 악마의 눈을 소환하고, 13초마다 5초 무적과 HP 500 회복을 사용한다.',detail:'HP 1366 · 악의 돌진 13~166 / 5초 · 🧿 HP 66 소환 / 13초 · 무적 5초 + HP 500 / 13초 · 특별 코드로 샌드박스 해금'},",
"{id:'hell_demon',name:'악마',icon:'👿',tag:'악의 돌진 · 악의 소환 · 무적 · 지옥의 불',hp:1366,damage:13,speed:175,cooldown:0,unlock:'hellDemon',description:'샌드박스 악마. 악의 돌진 13~166 / 5초, 악마의 눈 소환 / 13초, 13초마다 1.3초 무적과 HP 136 회복. 2.5초마다 피해 66의 보라색 지옥의 불을 던진다.',detail:'HP 1366 · 악의 돌진 13~166 / 5초 · 🧿 HP 66 소환 / 13초 · 무적 1.3초 + HP 136 / 13초 · 🟣🔥 지옥의 불 66 / 2.5초 · 지옥의 화상 13 / 0.66초 · 사망 시 해제 · 특별 코드로 샌드박스 해금'},",
'demon roster')

# Add hellfire status logic before demonSkill.
anchor="""demonSkill(f,e,dt){
 if(!f||!['hell_clone','hell_demon'].includes(f.id)||f.health<=0)return;
 const chapterMode=!!f.hellChapterMode,summonEvery=chapterMode?3:13,dashRange=chapterMode?654:154;
 if(!Number.isFinite(f.hellDashNext)){f.hellDashNext=this.time+5;f.hellSummonNext=this.time+summonEvery;f.hellInvulnNext=this.time+13;f.hellInvulnUntil=0;f.hellDashUntil=0;f.hellDashHit=false}
 if(this.time>=f.hellInvulnNext-1e-9){
   if(Number.isFinite(f.hellObservedHealth)&&f.health<f.hellObservedHealth)f.hellDamageTaken=(f.hellDamageTaken||0)+(f.hellObservedHealth-f.health);
   f.hellInvulnNext=this.time+13;f.hellInvulnUntil=this.time+5;f.poison=null;f.toxin=null;f.burn=null;f.bleed=null;f.curse=null;
   const heal=Math.min(500,f.hp-f.health);f.health+=heal;f.healed=(f.healed||0)+heal;f.hellObservedHealth=f.health;this.effect(f,'👿 무적 5초 · +'+Math.round(heal),'heal');this.emit('👿 악마가 5초 무적 상태가 되고 HP 500 회복!')
 }
 if(this.time>=f.hellSummonNext-1e-9){f.hellSummonNext=this.time+summonEvery;this.spawnHellEye(f)}
 if(e&&e.health>0&&this.time>=f.hellDashNext-1e-9){const a=this.aim(f,e);f.hellDashNext=this.time+5;f.hellDashUntil=this.time+.65;f.hellDashDamage=13+Math.floor(this.random()*dashRange);f.hellDashHit=false;f.dash=.65;f.vx=a.x;f.vy=a.y;f.turn=.65;this.effect(f,'👿 악의 돌진 '+f.hellDashDamage+'!','skill')}
}"""
replacement="""applyHellBurn(source,e){
 if(!source||!e||source.team===e.team||e.health<=0)return false;
 e.hellBurn={source:source.side,next:this.time+.66};
 this.effect(e,'🟣🔥 지옥의 화상!','doom');this.emit('🟣🔥 '+e.name+'에게 지옥의 화상!');return true
}
tickHellBurn(e){
 const h=e.hellBurn;if(!h||e.health<=0)return;
 while(h.next<=this.time+1e-9&&e.health>0){
  h.next+=.66;
  if(this.isStudying(e)||(e.hellInvulnUntil||0)>this.time)continue;
  const source=this.fighters[h.source],n=Math.min(e.health,13),pre=e.health;e.health-=n;
  if(source){source.damageDealt=(source.damageDealt||0)+n;source.hits=(source.hits||0)+1}
  this.effect(e,'🟣🔥 −'+n,'doom');
  if(e.health<=0){e.hellBurn=null;if(this.formEgg(e))return;e.trail=[];this.emit(e.name+' 지옥의 화상으로 탈락!');this.checkEnd();return}
 }
}
demonSkill(f,e,dt){
 if(!f||!['hell_clone','hell_demon'].includes(f.id)||f.health<=0)return;
 const chapterMode=!!f.hellChapterMode,summonEvery=chapterMode?3:13,dashRange=chapterMode?654:154,invulnDuration=chapterMode?5:1.3,invulnHeal=chapterMode?500:136;
 if(!Number.isFinite(f.hellDashNext)){f.hellDashNext=this.time+5;f.hellSummonNext=this.time+summonEvery;f.hellInvulnNext=this.time+13;f.hellInvulnUntil=0;f.hellDashUntil=0;f.hellDashHit=false;f.hellFireNext=this.time+2.5/f.scale}
 if(!Number.isFinite(f.hellFireNext))f.hellFireNext=this.time+2.5/f.scale;
 if(this.time>=f.hellInvulnNext-1e-9){
   if(Number.isFinite(f.hellObservedHealth)&&f.health<f.hellObservedHealth)f.hellDamageTaken=(f.hellDamageTaken||0)+(f.hellObservedHealth-f.health);
   f.hellInvulnNext=this.time+13;f.hellInvulnUntil=this.time+invulnDuration;f.poison=null;f.toxin=null;f.burn=null;f.bleed=null;f.curse=null;
   const heal=Math.min(invulnHeal,f.hp-f.health);f.health+=heal;f.healed=(f.healed||0)+heal;f.hellObservedHealth=f.health;this.effect(f,'👿 무적 '+invulnDuration+'초 · +'+Math.round(heal),'heal');this.emit('👿 악마가 '+invulnDuration+'초 무적 상태가 되고 HP '+invulnHeal+' 회복!')
 }
 if(this.time>=f.hellSummonNext-1e-9){f.hellSummonNext=this.time+summonEvery;this.spawnHellEye(f)}
 if(e&&e.health>0&&this.time>=f.hellFireNext-1e-9){const a=this.aim(f,e);f.hellFireNext=this.time+2.5/f.scale;this.shots.push({x:f.x+a.x*(f.radius+9),y:f.y+a.y*(f.radius+9),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'hellfire',icon:'🟣',radius:11*f.scale,speed:320*f.scale,damage:66*f.scale,life:4/f.scale,bounces:0});f.attack=.2/f.scale;this.effect(f,'🟣🔥 지옥의 불!','doom')}
 if(e&&e.health>0&&this.time>=f.hellDashNext-1e-9){const a=this.aim(f,e);f.hellDashNext=this.time+5;f.hellDashUntil=this.time+.65;f.hellDashDamage=13+Math.floor(this.random()*dashRange);f.hellDashHit=false;f.dash=.65;f.vx=a.x;f.vy=a.y;f.turn=.65;this.effect(f,'👿 악의 돌진 '+f.hellDashDamage+'!','skill')}
}"""
once(anchor,replacement,'demon skill')

# Apply hell burn only when the hellfire projectile actually dealt damage.
old="const cd=f.cd,attack=f.attack,dmg=s.kind==='flyingmoney'?(100+10*(e.moneyHappiness||0))*f.scale:(s.instant?e.health/Math.max(.000001,1-e.armor):s.damage);this.attack(f,e,dmg);f.cd=cd;f.attack=attack;"
new="const cd=f.cd,attack=f.attack,dmg=s.kind==='flyingmoney'?(100+10*(e.moneyHappiness||0))*f.scale:(s.instant?e.health/Math.max(.000001,1-e.armor):s.damage),dealt=this.attack(f,e,dmg);f.cd=cd;f.attack=attack;if(s.kind==='hellfire'&&dealt>0&&e.health>0)this.applyHellBurn(f,e);"
once(old,new,'projectile hellburn')

# Tick persistent hell burn with the rest of statuses.
old="if(f.health>0)this.tickBleed(f);if(this.result!==null)return;if(f.health>0)this.tickDrugTreatment(f);"
new="if(f.health>0)this.tickBleed(f);if(this.result!==null)return;if(f.health>0)this.tickHellBurn(f);if(this.result!==null)return;if(f.health>0)this.tickDrugTreatment(f);"
once(old,new,'hellburn tick loop')

# Any actual death clears the until-death hell burn, including characters that revive.
once("formEgg(f){\n if(f.id==='dragon'", "formEgg(f){\n if(f&&f.health<=0)f.hellBurn=null;\n if(f.id==='dragon'", 'death clears hellburn')

# CH10 UI/battle info: chapter values stay original; only append hellfire.
once("HP 666 · 악의 돌진 13~666 · 악의 눈 3초 · 13초마다 5초 무적+500 회복</span>",
     "HP 666 · 악의 돌진 13~666 · 악의 눈 3초 · 무적 5초+500 · 🟣🔥 지옥의 불 66/2.5초</span>",
     'stage2 card')
once("악마의 눈 HP 66 소환/3초 · 무적 5초+HP 500/13초.'",
     "악마의 눈 HP 66 소환/3초 · 무적 5초+HP 500/13초 · 지옥의 불 66/2.5초 + 지옥의 화상 13/0.66초.'",
     'stage2 battle info')
once("'CHAPTER 10 STAGE 3 · 악마 HP 6666 · 선택 조력자 '",
     "'CHAPTER 10 STAGE 3 · 악마 HP 6666 · 지옥의 불 66/2.5초 + 지옥의 화상 13/0.66초 · 선택 조력자 '",
     'stage3 battle info')

p.write_text(s,encoding='utf-8')
print('v3.74 patch applied')

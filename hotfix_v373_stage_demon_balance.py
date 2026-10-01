from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1, got {n}')
    s=s.replace(old,new,1)

# CH10 stage clone display: restore original stage-mode values.
once("{id:'hell_clone',name:'악마의 분신',icon:'👿',tag:'악의 돌진 · 악의 소환 · 무적',hp:666,damage:13,speed:170,cooldown:0,stageOnly:true,description:'5초마다 악의 돌진, 13초마다 HP 66 악마의 눈 소환, 13초마다 5초 무적과 HP 500 회복을 사용한다.',detail:'HP 666 · 악의 돌진 13~166 / 5초 · 🧿 HP 66 소환 / 13초 · 무적 5초 + HP 500 / 13초'},",
     "{id:'hell_clone',name:'악마의 분신',icon:'👿',tag:'악의 돌진 · 악의 소환 · 무적',hp:666,damage:13,speed:170,cooldown:0,stageOnly:true,description:'5초마다 악의 돌진, 3초마다 HP 66 악마의 눈 소환, 13초마다 5초 무적과 HP 500 회복을 사용한다.',detail:'HP 666 · 악의 돌진 13~666 / 5초 · 🧿 HP 66 소환 / 3초 · 무적 5초 + HP 500 / 13초'},",
     'clone stage description')

# Split demon mechanics by context. CH10 stage fighters get original 666/3s;
# sandbox unlocked demon keeps v3.73 166/13s.
old="""demonSkill(f,e,dt){
 if(!f||!['hell_clone','hell_demon'].includes(f.id)||f.health<=0)return;
 if(!Number.isFinite(f.hellDashNext)){f.hellDashNext=this.time+5;f.hellSummonNext=this.time+13;f.hellInvulnNext=this.time+13;f.hellInvulnUntil=0;f.hellDashUntil=0;f.hellDashHit=false}
 if(this.time>=f.hellInvulnNext-1e-9){
   if(Number.isFinite(f.hellObservedHealth)&&f.health<f.hellObservedHealth)f.hellDamageTaken=(f.hellDamageTaken||0)+(f.hellObservedHealth-f.health);
   f.hellInvulnNext=this.time+13;f.hellInvulnUntil=this.time+5;f.poison=null;f.toxin=null;f.burn=null;f.bleed=null;f.curse=null;
   const heal=Math.min(500,f.hp-f.health);f.health+=heal;f.healed=(f.healed||0)+heal;f.hellObservedHealth=f.health;this.effect(f,'👿 무적 5초 · +'+Math.round(heal),'heal');this.emit('👿 악마가 5초 무적 상태가 되고 HP 500 회복!')
 }
 if(this.time>=f.hellSummonNext-1e-9){f.hellSummonNext=this.time+13;this.spawnHellEye(f)}
 if(e&&e.health>0&&this.time>=f.hellDashNext-1e-9){const a=this.aim(f,e);f.hellDashNext=this.time+5;f.hellDashUntil=this.time+.65;f.hellDashDamage=13+Math.floor(this.random()*154);f.hellDashHit=false;f.dash=.65;f.vx=a.x;f.vy=a.y;f.turn=.65;this.effect(f,'👿 악의 돌진 '+f.hellDashDamage+'!','skill')}
}"""
new="""demonSkill(f,e,dt){
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
once(old,new,'split demon mechanics')

# Mark CH10 stage 2/3 enemy instances as chapter-mode.
once("else if(n===2){engine=new Engine('hero','hell_clone',Math.random,{mode:'control'});const b=engine.fighters[1];b.hp=666;b.health=666}",
     "else if(n===2){engine=new Engine('hero','hell_clone',Math.random,{mode:'control'});const b=engine.fighters[1];b.hp=666;b.health=666;b.hellChapterMode=true}",
     'stage2 chapter flag')
once("const b=engine.fighters[1];b.hp=6666;b.health=6666;b.hellBoss=true;",
     "const b=engine.fighters[1];b.hp=6666;b.health=6666;b.hellChapterMode=true;b.hellBoss=true;",
     'stage3 chapter flag')

# Restore CH10 UI/battle copy to original chapter values.
once("<span class=\"card-desc\">HP 666 · 악의 돌진 13~166 · 악의 눈 13초 · 13초마다 5초 무적+500 회복</span>",
     "<span class=\"card-desc\">HP 666 · 악의 돌진 13~666 · 악의 눈 3초 · 13초마다 5초 무적+500 회복</span>",
     'stage2 card copy')
once("CHAPTER 10 STAGE 2 · 악마의 분신 HP 666 · 악의 돌진 13~166/5초 · 악마의 눈 HP 66 소환/13초 · 무적 5초+HP 500/13초.",
     "CHAPTER 10 STAGE 2 · 악마의 분신 HP 666 · 악의 돌진 13~666/5초 · 악마의 눈 HP 66 소환/3초 · 무적 5초+HP 500/13초.",
     'stage2 battle copy')

p.write_text(s,encoding='utf-8')
print('v3.73 stage demon balance hotfix applied')

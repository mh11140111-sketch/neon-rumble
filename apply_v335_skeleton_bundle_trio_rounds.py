from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n!=count:
        raise SystemExit(f'replace mismatch expected {count}, found {n}: {old[:180]!r}')
    s=s.replace(old,new,count)

rep("{id:'skeletons',name:'해골들',icon:'💀💀💀',tag:'3마리 1세트 · 3라운드',hp:125,damage:70,speed:155,cooldown:1,unlock:'skeleton',description:'해골 3마리가 한 세트야. ROUND 1 🔫 총잡이 → ROUND 2 🗡️ 칼잡이 → ROUND 3 🍺 취한 해골 순서로 등장해. 다음 라운드로 넘어가도 상대 체력은 절대 회복되지 않아.',detail:'💀 해골들 · 각 HP 125 · R1 🔫70/1초 · R2 🗡️70/3초 · R3 🍺100/3초 · 상대 HP 라운드 간 유지'},",
"{id:'skeletons',name:'해골들',icon:'💀💀💀',tag:'3마리 동시 출전 · 3라운드',hp:125,damage:70,speed:155,cooldown:1,unlock:'skeleton',description:'샌드박스에서 🔫 총잡이·🗡️ 칼잡이·🍺 취한 해골 3마리가 한 세트로 동시에 출전해. 3마리가 모두 쓰러지면 새 세트가 등장하며 총 3라운드까지 진행돼. 다음 라운드로 넘어가도 상대 체력은 절대 회복되지 않아.',detail:'💀 해골들 · 3마리 동시 출전 · 각 HP 125 · 총 3라운드 · 🔫70/1초 · 🗡️70/3초 · 🍺100/3초 · 상대 HP 라운드 간 유지'},")

old_ctor=""" });
 for(const owner of [...this.fighters])if(owner.id==='aladdin')this.spawnGenie(owner);
}
spawnGenie(owner){"""
new_ctor=""" });
 // In sandbox-style 1v1/control play, the unlocked Skeletons character is one slot made of three simultaneous fighters.
 if(this.mode==='duel'||this.mode==='control'){
  for(const owner of [...this.fighters])if(owner.skeletonBundle){
   owner.skeletonBundleLeader=owner.side;owner.skeletonBundleRound=1;owner.name='해골들';
   const mateIds=['skeleton_sword','skeleton_drunk'],ys=[-82,82];
   mateIds.forEach((id,i)=>{const t=ROSTER.find(x=>x.id===id),side=this.fighters.length,angle=this.rand(-1,1)+(owner.team?Math.PI:0),hp=t.hp*(owner.boss?2.5:1),m={...owner,...t,name:'해골들',side,team:owner.team,boss:owner.boss,scale:owner.scale,bodyScale:owner.bodyScale,radius:owner.radius,hp,health:hp,damage:t.damage*owner.scale,speed:t.speed*owner.scale,cooldown:t.cooldown/owner.scale,skeletonBundle:true,skeletonBundleLeader:owner.side,skeletonBundleRound:1,x:owner.x,y:clamp(owner.y+ys[i],60,660),vx:Math.cos(angle),vy:Math.sin(angle),attack:0,cd:0,stunUntil:0,burn:null,poison:null,toxin:null,curse:null,slow:0,slowPower:0,rootSlow:0,rootSlowPower:0,capturedBy:null,captureTarget:null,trail:[],deathOrder:null,possessedByGhost:null};this.fighters.push(m)})
  }
 }
 for(const owner of [...this.fighters])if(owner.id==='aladdin')this.spawnGenie(owner);
}
spawnGenie(owner){"""
rep(old_ctor,new_ctor)

old_bundle=""" if(f.skeletonBundle&&f.health<=0&&(f.skeletonBundleRound||1)<3){const nextRound=(f.skeletonBundleRound||1)+1,nextId=nextRound===2?'skeleton_sword':'skeleton_drunk',nt=ROSTER.find(x=>x.id===nextId);f.skeletonBundleRound=nextRound;f.id=nextId;f.name='해골들';f.icon='💀';f.tag=nt.tag;f.description=nt.description;f.detail=nt.detail;f.damage=nt.damage*f.scale;f.speed=nt.speed*f.scale;f.cooldown=nt.cooldown/f.scale;f.health=f.hp;f.cd=.4/f.scale;f.attack=0;f.poison=null;f.toxin=null;f.burn=null;f.curse=null;f.stunUntil=0;f.slow=0;f.slowPower=0;f.rootSlow=0;f.rootSlowPower=0;f.trail=[];this.shots=this.shots.filter(s=>s.owner!==f.side);this.effect(f,'💀 ROUND '+nextRound+'/3','skill');this.emit('해골들 다음 라운드! ROUND '+nextRound+'/3 · 상대 체력 유지');return true}
"""
new_bundle=""" if(f.skeletonBundle&&f.health<=0){const leader=f.skeletonBundleLeader??f.side,members=this.fighters.filter(x=>x.skeletonBundle&&(x.skeletonBundleLeader??x.side)===leader);if(members.length>=3&&members.every(x=>x.health<=0)){const round=members[0].skeletonBundleRound||1;if(round<3){const nextRound=round+1,owners=new Set(members.map(x=>x.side)),baseX=members[0].team?550:170,baseY=360,ys=[-82,0,82];members.forEach((m,i)=>{m.skeletonBundleRound=nextRound;m.health=m.hp;m.x=baseX;m.y=clamp(baseY+ys[i%3],60,660);const a=this.rand(-1,1)+(m.team?Math.PI:0);m.vx=Math.cos(a);m.vy=Math.sin(a);m.cd=.4/m.scale;m.attack=0;m.poison=null;m.toxin=null;m.burn=null;m.curse=null;m.stunUntil=0;m.slow=0;m.slowPower=0;m.rootSlow=0;m.rootSlowPower=0;m.capturedBy=null;m.captureTarget=null;m.trail=[];m.deathOrder=null});this.shots=this.shots.filter(s=>!owners.has(s.owner));this.effect(members[0],'💀💀💀 ROUND '+nextRound+'/3','skill');this.emit('해골들 새 세트 출전! ROUND '+nextRound+'/3 · 3마리 동시 출전 · 상대 체력 유지');return true}}}
"""
rep(old_bundle,new_bundle)

rep("<div class=\"patch-version\"><h3>v3.35 · 사막의 총성이 울리고, 해골 마법이 깨어나다</h3><ul><li>카우보이: 총알 피해 80 → 100.</li>",
"<div class=\"patch-version\"><h3>v3.35 · 사막의 총성이 울리고, 해골 마법이 깨어나다</h3><ul><li>해골들: 샌드박스에서 🔫 총잡이·🗡️ 칼잡이·🍺 취한 해골 3마리가 동시에 한 세트로 출전. 세트 전멸 후 새 세트가 등장하며 총 3라운드 진행, 상대 체력은 라운드 사이 절대 회복되지 않음.</li><li>카우보이: 총알 피해 80 → 100.</li>")

p.write_text(s,encoding='utf-8')
print('v3.35 skeleton trio rounds hotfix applied')

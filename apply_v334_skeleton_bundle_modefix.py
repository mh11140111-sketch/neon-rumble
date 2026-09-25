from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n!=count:
        raise SystemExit(f'replace mismatch: expected {count}, found {n}: {old[:180]!r}')
    s=s.replace(old,new,count)

# Patch notes: document the bundle remake and progression-state fix.
rep(
"<li>해금 해골의 다음 라운드 진입 시 상대 체력은 이전 라운드 값을 그대로 유지하며 절대 회복하지 않음.</li>",
"<li>해금 해골의 다음 라운드 진입 시 상대 체력은 이전 라운드 값을 그대로 유지하며 절대 회복하지 않음.</li><li>해골 3종을 개별 캐릭터에서 하나의 💀 해골들 묶음 캐릭터로 리메이크. ROUND 1 총잡이 → ROUND 2 칼잡이 → ROUND 3 취한 해골 순서로 진행.</li><li>리메이크 전 해골 3종 해금 기록은 새 💀 해골들 해금에 승계되지 않음. CHAPTER 2 STAGE 3을 다시 클리어해야 새 묶음 캐릭터를 획득.</li><li>사막 스테이지 종료 후 일반 모드로 돌아왔을 때 사막 승패 판정이 남아 일반전 진행을 막던 모드 상태 버그 수정.</li>"
)

# Replace the three old selectable skeleton entries with internal stage-only variants,
# and add one public unlockable bundle character.
old_entries="""{id:'skeleton_gun',name:'총잡이 해골',icon:'💀',tag:'🔫 회전총 · 3라운드',hp:125,damage:70,speed:155,cooldown:1,unlock:'skeleton',description:'몸 주위를 도는 총이 가장 가까운 적을 향해 1초마다 피해 70의 총알을 발사해. CHAPTER 2에서 해금하면 한 경기에서 최대 3라운드까지 등장해.',detail:'HP 125 · 🔫 회전총 · 총알 70 / 1초 · 해금 후 총 3라운드'},
{id:'skeleton_sword',name:'칼잡이 해골',icon:'💀',tag:'🗡️ 추적검 · 3라운드',hp:125,damage:70,speed:175,cooldown:3,unlock:'skeleton',description:'칼이 항상 가장 가까운 적을 가리켜. 칼이 닿으면 피해 70을 주고 3초 동안 다시 공격할 수 없어. CHAPTER 2에서 해금하면 한 경기에서 최대 3라운드까지 등장해.',detail:'HP 125 · 🗡️ 피해 70 · 쿨타임 3초 · 해금 후 총 3라운드'},
{id:'skeleton_drunk',name:'취한 해골',icon:'💀',tag:'🍺 비틀비틀 조준 · 3라운드',hp:125,damage:100,speed:145,cooldown:3,unlock:'skeleton',description:'맥주잔이 적을 노리지만 술에 취해 조준 오차가 커. 3초마다 빗나가기 쉬운 맥주 공격으로 피해 100을 노려. CHAPTER 2에서 해금하면 한 경기에서 최대 3라운드까지 등장해.',detail:'HP 125 · 🍺 피해 100 · 쿨타임 3초 · 낮은 명중률 · 해금 후 총 3라운드'},"""
new_entries="""{id:'skeleton_gun',name:'총잡이 해골',icon:'💀',tag:'🔫 회전총',hp:125,damage:70,speed:155,cooldown:1,stageOnly:true,description:'몸 주위를 도는 총이 가장 가까운 적을 향해 1초마다 피해 70의 총알을 발사해.',detail:'HP 125 · 🔫 회전총 · 총알 70 / 1초'},
{id:'skeleton_sword',name:'칼잡이 해골',icon:'💀',tag:'🗡️ 추적검',hp:125,damage:70,speed:175,cooldown:3,stageOnly:true,description:'칼이 항상 가장 가까운 적을 가리켜. 칼이 닿으면 피해 70을 주고 3초 동안 다시 공격할 수 없어.',detail:'HP 125 · 🗡️ 피해 70 · 쿨타임 3초'},
{id:'skeleton_drunk',name:'취한 해골',icon:'💀',tag:'🍺 비틀비틀 조준',hp:125,damage:100,speed:145,cooldown:3,stageOnly:true,description:'맥주잔이 적을 노리지만 술에 취해 조준 오차가 커. 3초마다 빗나가기 쉬운 맥주 공격으로 피해 100을 노려.',detail:'HP 125 · 🍺 피해 100 · 쿨타임 3초 · 낮은 명중률'},
{id:'skeletons',name:'해골들',icon:'💀💀💀',tag:'3마리 1세트 · 3라운드',hp:125,damage:70,speed:155,cooldown:1,unlock:'skeleton',description:'해골 3마리가 한 세트야. ROUND 1 🔫 총잡이 → ROUND 2 🗡️ 칼잡이 → ROUND 3 🍺 취한 해골 순서로 등장해. 다음 라운드로 넘어가도 상대 체력은 절대 회복되지 않아.',detail:'💀 해골들 · 각 HP 125 · R1 🔫70/1초 · R2 🗡️70/3초 · R3 🍺100/3초 · 상대 HP 라운드 간 유지'},"""
rep(old_entries,new_entries)

# New unlock key: intentionally does NOT inherit the old pre-remake unlock.
rep(
"const ROBOT_STAGE_KEY='neonRumble.robotStages.v1',SKELETON_UNLOCK_KEY='neonRumble.skeletonUnlocked.v1';",
"const ROBOT_STAGE_KEY='neonRumble.robotStages.v1',SKELETON_UNLOCK_KEY='neonRumble.skeletonBundleUnlocked.v2';"
)

# Engine accepts the public meta-character but internally starts it as the gun skeleton.
rep(
"const type=ROSTER.find(x=>x.id===id);if(!type)throw Error('알 수 없는 캐릭터');",
"const skeletonBundle=id==='skeletons',type=ROSTER.find(x=>x.id===(skeletonBundle?'skeleton_gun':id));if(!type)throw Error('알 수 없는 캐릭터');"
)
rep(
"return {...type,side,team,boss,scale,bodyScale,radius:33*bodyScale,hp,health:hp,damage:type.damage*scale,speed:type.speed*scale,cooldown:type.cooldown/scale,",
"return {...type,name:skeletonBundle?'해골들':type.name,side,team,boss,scale,bodyScale,radius:33*bodyScale,hp,health:hp,damage:type.damage*scale,speed:type.speed*scale,cooldown:type.cooldown/scale,skeletonBundle,skeletonBundleRound:skeletonBundle?1:0,"
)

# Remake the old same-skeleton respawn into a true 3-member bundle sequence.
old_revive="""if(['skeleton_gun','skeleton_sword','skeleton_drunk'].includes(f.id)&&!f.noSkeletonRevive&&f.health<=0&&(f.revivals||0)<2){f.revivals=(f.revivals||0)+1;f.health=f.hp;f.cd=.4/f.scale;f.poison=null;f.toxin=null;f.burn=null;f.curse=null;f.stunUntil=0;f.slow=0;f.slowPower=0;f.rootSlow=0;f.rootSlowPower=0;f.trail=[];this.shots=this.shots.filter(s=>s.owner!==f.side);this.effect(f,'💀 ROUND '+(f.revivals+1)+'/3','skill');this.emit(f.name+' 다음 라운드! ROUND '+(f.revivals+1)+'/3 · 상대 체력 유지');return true}"""
new_revive="""if(f.skeletonBundle&&f.health<=0&&(f.skeletonBundleRound||1)<3){const nextRound=(f.skeletonBundleRound||1)+1,nextId=nextRound===2?'skeleton_sword':'skeleton_drunk',nt=ROSTER.find(x=>x.id===nextId);f.skeletonBundleRound=nextRound;f.id=nextId;f.name='해골들';f.icon='💀';f.tag=nt.tag;f.description=nt.description;f.detail=nt.detail;f.damage=nt.damage*f.scale;f.speed=nt.speed*f.scale;f.cooldown=nt.cooldown/f.scale;f.health=f.hp;f.cd=.4/f.scale;f.attack=0;f.poison=null;f.toxin=null;f.burn=null;f.curse=null;f.stunUntil=0;f.slow=0;f.slowPower=0;f.rootSlow=0;f.rootSlowPower=0;f.trail=[];this.shots=this.shots.filter(s=>s.owner!==f.side);this.effect(f,'💀 ROUND '+nextRound+'/3','skill');this.emit('해골들 다음 라운드! ROUND '+nextRound+'/3 · 상대 체력 유지');return true}"""
rep(old_revive,new_revive)

# Bundle HUD uses its own round counter. Internal desert skeletons do not show bundle rounds.
rep(
"function ability(f){if(['skeleton_gun','skeleton_sword','skeleton_drunk'].includes(f.id))return '💀 ROUND '+((f.revivals||0)+1)+' / 3 · 상대 HP 유지';if(f.id==='coolguy')",
"function ability(f){if(f.skeletonBundle)return '💀 해골들 · ROUND '+(f.skeletonBundleRound||1)+' / 3 · 상대 HP 유지';if(f.id==='coolguy')"
)

# Leaving a desert battle must clear desert mode before normal selection starts.
rep(
"function selection(){engine=null;paused=false;acc=0;keys.clear();resetStick();",
"function selection(){if(mode==='desert')mode='duel';engine=null;paused=false;acc=0;keys.clear();resetStick();"
)

# Unlock text now refers to the one bundled character.
rep(" · 💀 해골 3종 캐릭터 해금!"," · 💀 해골들 캐릭터 해금!")
rep("CHAPTER 2 STAGE 3 클리어 시 해골 3종 해금.","CHAPTER 2 STAGE 3 클리어 시 💀 해골들 해금.")

p.write_text(s,encoding='utf-8')
print('v3.34 skeleton bundle/mode hotfix applied')

from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 occurrence, found {n}')
    s=s.replace(old,new,1)

# Version and patch notes.
once('BATTLE <b>v3.28</b>','BATTLE <b>v3.29</b>','version badge')
once('📒 패치노트 · v3.28','📒 패치노트 · v3.29','patch summary')
marker='<div class="patch-body"><div class="patch-version"><h3>v3.28 · 도마뱀 & 복서 리워크</h3>'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.29 · 유령 & 밸런스</h3><ul><li>분노한 남자: 부활할 때마다 최대/현재 체력이 50 감소. 333 → 283 → 233.</li><li>분노한 남자: 2회 부활 후 🤜 근접 공격 재사용 대기시간 1초.</li><li>히어로: 돌진 뒤 후퇴 중에도 상대와 접촉하면 돌진 피해가 1회 적용.</li><li>도마뱀: 근접 피해 70 → 100.</li><li>신규 캐릭터 👻 유령: 적과 접촉하면 0.3초 동안 충돌과 공격을 통과. 별도 재사용 대기시간 없음.</li><li>단체전·보스 도전자 팀에서 살아 있는 유령은 팀에서 처음 탈락한 아군 1명을 1회 부활. 부활 HP는 300, 원래 최대 HP가 300 미만이면 최대 HP까지 회복.</li></ul></div><div class="patch-version"><h3>v3.28 · 도마뱀 & 복서 리워크</h3>'
once(marker,insert,'v329 patch notes')

# Balance and new roster entry.
once("{id:'angryman',name:'분노한 남자',icon:'😠',tag:'2회 부활 · 분노 강화',hp:333,damage:30,speed:165,cooldown:1,description:'체력 333으로 시작해 총 2번 부활해. 😠 단계는 👎 30/1초, 😡 단계는 👎 50/0.5초, 🤬 단계는 👎 70/0.5초로 공격해. 최종 단계에서는 가까운 적에게 🤜 피해 85와 1초 기절을 줘.',detail:'HP 333 · 총 2회 부활 · 😠 👎30/1초 · 😡 👎50/0.5초 · 🤬 👎70/0.5초 · 최종 🤜85 + 1초 기절'},",
"{id:'angryman',name:'분노한 남자',icon:'😠',tag:'2회 부활 · 분노 강화',hp:333,damage:30,speed:165,cooldown:1,description:'체력 333으로 시작해 총 2번 부활해. 부활할 때마다 체력이 50씩 줄어 283, 233이 돼. 😠 단계는 👎 30/1초, 😡 단계는 👎 50/0.5초, 🤬 단계는 👎 70/0.5초. 최종 단계에서는 🤜 피해 85 + 기절 1초를 주며 근접 공격 쿨타임은 1초야.',detail:'HP 333 → 283 → 233 · 총 2회 부활 · 😠 👎30/1초 · 😡 👎50/0.5초 · 🤬 👎70/0.5초 · 최종 🤜85 + 기절 1초 / 쿨타임 1초'},",'angry roster')
once("{id:'lizard',name:'도마뱀',icon:'🦎',tag:'고속 · 꼬리 미끼',hp:1000,damage:70,speed:188.5,cooldown:.7,description:'일반 캐릭터보다 30% 빠르게 움직이며 근접 피해 70으로 공격해. 체력이 30% 이하가 되면 꼬리를 한 번 소환하고, 꼬리가 살아 있는 동안 모든 적 AI가 꼬리를 우선 공격해.',detail:'HP 1000 · 이동속도 +30% · 근접 70 · HP 30% 이하 꼬리 1회 소환 · 꼬리 HP는 본체 최대 HP의 30% · 꼬리 생존 중 적 AI 우선 타깃'}\n];",
"{id:'lizard',name:'도마뱀',icon:'🦎',tag:'고속 · 꼬리 미끼',hp:1000,damage:100,speed:188.5,cooldown:.7,description:'일반 캐릭터보다 30% 빠르게 움직이며 근접 피해 100으로 공격해. 체력이 30% 이하가 되면 꼬리를 한 번 소환하고, 꼬리가 살아 있는 동안 모든 적 AI가 꼬리를 우선 공격해.',detail:'HP 1000 · 이동속도 +30% · 근접 100 · HP 30% 이하 꼬리 1회 소환 · 꼬리 HP는 본체 최대 HP의 30% · 꼬리 생존 중 적 AI 우선 타깃'},\n{id:'ghost',name:'유령',icon:'👻',tag:'통과 · 아군 부활',hp:1000,damage:0,speed:170,cooldown:0,description:'적과 닿으면 0.3초 동안 모든 충돌과 공격을 통과해. 별도 쿨타임은 없어. 단체전이나 보스 도전자 팀에서는 살아 있는 동안 팀에서 처음 탈락한 아군 1명을 한 번 부활시켜.',detail:'HP 1000 · 접촉 시 0.3초 통과 · 쿨타임 0초 · 팀전 아군 1회 부활 · 부활 HP 300 / 최대 HP가 300 미만이면 풀 회복'}\n];",'lizard + ghost roster')

# Core fighter state.
once("this.time=0;this.width=720;this.height=720;this.shots=[];this.effects=[];this.events=[];this.result=null;",
     "this.time=0;this.width=720;this.height=720;this.shots=[];this.effects=[];this.events=[];this.result=null;this.deathSerial=0;",'death serial')
once("dash:0,dashHit:false,",
     "dash:0,dashHit:false,retreatHit:false,ghostPhaseUntil:0,ghostReviveUsed:false,deathOrder:null,",'fighter state')

# During ghost phase, AI and projectiles do not select the ghost.
once("enemies(f){return this.fighters.filter(e=>e.team!==f.team&&e.health>0&&e.moonUltPhase!=='air')}",
     "enemies(f){return this.fighters.filter(e=>e.team!==f.team&&e.health>0&&e.moonUltPhase!=='air'&&!(e.id==='ghost'&&e.ghostPhaseUntil>this.time))}",'ghost targetability')

# Ghost team revive is resolved before the final team-alive check.
old_check="checkEnd(){if(this.resolvingBlast)return;if(this.mode==='relay'){const out=this.fighters.find(f=>f.health<=0&&this.relayIndex[f.side]===2);if(out)this.result=1-out.side;return;}const alive=[0,1].map(team=>this.fighters.some(f=>!f.summon&&f.team===team&&f.health>0));if(!alive[0]||!alive[1])this.result=alive[0]?0:1}"
new_check="""checkEnd(){if(this.resolvingBlast)return;if(this.mode==='relay'){const out=this.fighters.find(f=>f.health<=0&&this.relayIndex[f.side]===2);if(out)this.result=1-out.side;return;}for(const f of this.fighters)if(!f.summon&&f.health<=0&&f.deathOrder==null)f.deathOrder=++this.deathSerial;if(this.mode==='group'||this.mode==='boss'){for(const team of [0,1]){const ghost=this.fighters.find(f=>!f.summon&&f.team===team&&f.id==='ghost'&&f.health>0&&!f.ghostReviveUsed);if(!ghost)continue;const dead=this.fighters.filter(f=>!f.summon&&f.team===team&&f!==ghost&&f.health<=0&&f.deathOrder!=null).sort((a,b)=>a.deathOrder-b.deathOrder)[0];if(dead){ghost.ghostReviveUsed=true;dead.health=Math.min(300,dead.hp);dead.poison=null;dead.toxin=null;dead.burn=null;dead.curse=null;dead.stunUntil=0;dead.slow=0;dead.slowPower=0;dead.rootSlow=0;dead.rootSlowPower=0;dead.capturedBy=null;dead.airborneUntil=0;dead.trail=[];dead.deathOrder=null;this.effect(ghost,'👻 아군 부활!','skill');this.effect(dead,'부활 '+Math.ceil(dead.health)+' HP','heal');this.emit('👻 유령이 '+dead.name+'을(를) '+Math.ceil(dead.health)+' HP로 부활!')}}}const alive=[0,1].map(team=>this.fighters.some(f=>!f.summon&&f.team===team&&f.health>0));if(!alive[0]||!alive[1])this.result=alive[0]?0:1}"""
once(old_check,new_check,'checkEnd ghost revive')

# Most damage routes use attack(); phased ghost ignores them.
once("if(this.result!==null||f.health<=0||e.health<=0||(!friendly&&f.team===e.team)||this.isStudying(e))return 0;",
     "if(this.result!==null||f.health<=0||e.health<=0||(!friendly&&f.team===e.team)||this.isStudying(e)||(e.id==='ghost'&&e.ghostPhaseUntil>this.time))return 0;",'attack phase guard')

# Angry man loses 50 max/current HP each self-revival.
once("if(f.id==='angryman'&&f.health<=0&&f.revivals<2){f.revivals++;f.hp=333*(f.boss?2.5:1);f.health=f.hp;",
     "if(f.id==='angryman'&&f.health<=0&&f.revivals<2){f.revivals++;f.hp=(333-50*f.revivals)*(f.boss?2.5:1);f.health=f.hp;",'angry revive hp')

# Hero retreat can hit once while backing away.
once("this.attack(f,e,250*f.scale);f.heroPhase='retreat';f.retreatUntil=this.time+.65/f.scale;",
     "this.attack(f,e,250*f.scale);f.heroPhase='retreat';f.retreatHit=false;f.retreatUntil=this.time+.65/f.scale;",'hero retreat flag')

# Ghost contact immediately enters 0.3s phase; phase itself has no extra cooldown.
once("const d=distance(a,b),limit=a.radius+b.radius;if(d>limit+.001)return;",
     "const d=distance(a,b),limit=a.radius+b.radius;if(d>limit+.001)return;if((a.id==='ghost'&&a.ghostPhaseUntil>this.time)||(b.id==='ghost'&&b.ghostPhaseUntil>this.time))return;if(a.team!==b.team&&(a.id==='ghost'||b.id==='ghost')){for(const g of [a,b])if(g.id==='ghost'&&g.health>0){g.ghostPhaseUntil=this.time+.3;this.effect(g,'👻 통과 0.3초','skill')}return}", 'ghost collide phase')

# Add retreat-contact hit immediately after boxer uppercut handling.
boxer_hook="if(f.id==='boxer'&&f.health>0&&f.stunUntil<=this.time&&this.boxerUppercut(f,e))continue;"
once(boxer_hook,
     boxer_hook+"if(f.id==='hero'&&f.heroReady&&f.heroPhase==='retreat'&&!f.retreatHit&&f.health>0&&f.stunUntil<=this.time){const dealt=this.attack(f,e,250*f.scale);if(dealt>0)f.retreatHit=true;continue}", 'hero retreat collision')

# Ghost has no ordinary contact attack.
once("'snowman','angryman','lizardtail'].includes(f.id)",
     "'snowman','angryman','lizardtail','ghost'].includes(f.id)", 'ghost melee exclusion')

# Keep displayed Moon timing consistent with the already-live v3.28 35 second logic.
s=s.replace("전투가 45초를 넘기면 궁극기를 준비해.","전투가 35초를 넘기면 궁극기를 준비해.",1)
s=s.replace("· 45초 후 궁극기 ·","· 35초 후 궁극기 ·",1)
s=s.replace('보스 달은 관통 반달 조각 160 / 1초, 22.5초 후 궁극기를 준비해','보스 달은 관통 반달 조각 160 / 1초, 17.5초 후 궁극기를 준비해',1)

if s==orig:
    raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('V329_PATCH_APPLIED')

from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    assert n==count, f'expected {count} occurrence(s), found {n}: {old[:120]}'
    s=s.replace(old,new,count)

rep("<span class=\"badge\">BATTLE <b>v3.29</b></span>","<span class=\"badge\">BATTLE <b>v3.30</b></span>")
rep("<summary>📒 패치노트 · v3.29</summary><div class=\"patch-body\">","<summary>📒 패치노트 · v3.30</summary><div class=\"patch-body\"><div class=\"patch-version\"><h3>v3.30 · 유령 리워크 & 눈사람 밸런스</h3><ul><li>유령: 3초마다 가장 가까운 적을 향해 짧게 대쉬.</li><li>유령: 접촉 피해 15 → 30. 접촉 후 0.3초 통과와 시체 빙의 능력은 유지.</li><li>눈사람: 눈송이 피해 30 → 60. 50% 확률 1초 얼림과 화상 피해 ×5는 유지.</li></ul></div>")

rep("{id:'snowman',name:'눈사람',icon:'⛄️',tag:'눈송이 · 얼림',hp:1000,damage:30,speed:145,cooldown:1,description:'1초마다 눈송이를 발사해 피해 30을 줘. 명중 시 50% 확률로 상대를 1초 동안 얼려 움직임과 행동을 멈춰. 화상 피해는 5배로 받아.',detail:'HP 1000 · 눈송이 30 / 1초 · 명중 시 50% 확률 1초 얼림 · 화상 피해 ×5'},",
"{id:'snowman',name:'눈사람',icon:'⛄️',tag:'눈송이 · 얼림',hp:1000,damage:60,speed:145,cooldown:1,description:'1초마다 눈송이를 발사해 피해 60을 줘. 명중 시 50% 확률로 상대를 1초 동안 얼려 움직임과 행동을 멈춰. 화상 피해는 5배로 받아.',detail:'HP 1000 · 눈송이 60 / 1초 · 명중 시 50% 확률 1초 얼림 · 화상 피해 ×5'},")
rep("{id:'ghost',name:'유령',icon:'👻',tag:'접촉 15 · 통과 · 시체 빙의',hp:1000,damage:15,speed:170,cooldown:0,description:'적과 닿으면 피해 15를 주고 0.3초 동안 모든 충돌과 공격을 통과해. 이동 AI는 기존 일반 캐릭터 방식이야. 팀전에서는 처음 죽은 아군이나 아군 소환수의 시체에 경기당 1회 빙의해.',detail:'HP 1000 · 접촉 피해 15 + 0.3초 통과 · 일반 이동 AI · 팀전 1회 시체 빙의 · 소환수 빙의 가능 · 빙의체 HP 300 / 최대 HP가 300 미만이면 풀 회복 · 빙의체 사망 시 유령 복귀'}",
"{id:'ghost',name:'유령',icon:'👻',tag:'3초 대쉬 · 접촉 30 · 시체 빙의',hp:1000,damage:30,speed:170,cooldown:0,description:'3초마다 가장 가까운 적에게 짧게 대쉬해. 적과 닿으면 피해 30을 주고 0.3초 동안 모든 충돌과 공격을 통과해. 팀전에서는 처음 죽은 아군이나 아군 소환수의 시체에 경기당 1회 빙의해.',detail:'HP 1000 · 3초마다 적 방향 대쉬 · 접촉 피해 30 + 0.3초 통과 · 팀전 1회 시체 빙의 · 소환수 빙의 가능 · 빙의체 HP 300 / 최대 HP가 300 미만이면 풀 회복 · 빙의체 사망 시 유령 복귀'}")

rep("retreatHit:false,ghostPhaseUntil:0,ghostReviveUsed:false,ghostPossessing:false,ghostPossessingSide:null,ghostStoredHealth:0,possessedByGhost:null,deathOrder:null,",
"retreatHit:false,ghostPhaseUntil:0,ghostDashNext:type.id==='ghost'?3/scale:9999,ghostReviveUsed:false,ghostPossessing:false,ghostPossessingSide:null,ghostStoredHealth:0,possessedByGhost:null,deathOrder:null,")

rep("damage:30*f.scale,life:3,bounces:0,stun:this.random()<.5?1*f.scale:0","damage:60*f.scale,life:3,bounces:0,stun:this.random()<.5?1*f.scale:0")

rep("if(f.id==='boxer'&&f.skill<=0){const a=this.aim(f,e);f.vx=a.x;f.vy=a.y;f.dash=.52*f.scale;f.dashHit=false;f.skill=2.8/f.scale;this.effect(f,'돌진!','skill')}\n const manual=",
"if(f.id==='boxer'&&f.skill<=0){const a=this.aim(f,e);f.vx=a.x;f.vy=a.y;f.dash=.52*f.scale;f.dashHit=false;f.skill=2.8/f.scale;this.effect(f,'돌진!','skill')}\n if(f.id==='ghost'&&f.health>0&&f.stunUntil<=this.time&&!f.ghostPossessing&&this.time>=f.ghostDashNext-1e-9){const a=this.aim(f,e);f.vx=a.x;f.vy=a.y;f.dash=.32;f.ghostDashNext=this.time+3/f.scale;this.effect(f,'👻 대쉬!','skill')}\n const manual=")

rep("this.attack(g,e,15*g.scale);g.ghostPhaseUntil=this.time+.3;this.effect(g,'👻 접촉 15 · 통과!','skill')",
"this.attack(g,e,30*g.scale);g.ghostPhaseUntil=this.time+.3;this.effect(g,'👻 접촉 30 · 통과!','skill')")

# Keep official version exactly v3.30 and ensure requested mechanics exist.
assert "BATTLE <b>v3.30</b>" in s
assert "ghostDashNext:type.id==='ghost'?3/scale:9999" in s
assert "this.time+3/f.scale" in s
assert "this.attack(g,e,30*g.scale)" in s
assert "damage:60*f.scale" in s
assert "눈송이 피해 30 → 60" in s
p.write_text(s,encoding='utf-8')
print('v3.30 patch applied')

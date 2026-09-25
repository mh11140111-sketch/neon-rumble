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

old_ai="if(f.id==='ghost'&&f.health>0&&f.stunUntil<=this.time&&!f.ghostPossessing){const at=this.nearest(f);if(at){const aa=this.aim(f,at);f.vx=aa.x;f.vy=aa.y;f.turn=.12}}"
new_ai="if(f.id==='ghost'&&f.health>0&&f.stunUntil<=this.time&&!f.ghostPossessing){const at=this.nearest(f);if(at){const aa=this.aim(f,at),d=distance(f,at);let x,y;if(d>150*f.scale){x=aa.x;y=aa.y}else{x=aa.x*.35-aa.y*.94;y=aa.y*.35+aa.x*.94}const n=Math.hypot(x,y)||1;f.vx=x/n;f.vy=y/n;f.turn=.18}}"
once(old_ai,new_ai,'ghost ai')

old_contact="if(a.team!==b.team&&(a.id==='ghost'||b.id==='ghost')){for(const g of [a,b])if(g.id==='ghost'&&g.health>0){g.ghostPhaseUntil=this.time+.3;this.effect(g,'👻 통과 0.3초','skill')}return}"
new_contact="if(a.team!==b.team&&(a.id==='ghost'||b.id==='ghost')){for(const g of [a,b])if(g.id==='ghost'&&g.health>0){const e=g===a?b:a;if(e.health>0)this.attack(g,e,15*g.scale);g.ghostPhaseUntil=this.time+.3;this.effect(g,'👻 접촉 15 · 통과!','skill')}return}"
once(old_contact,new_contact,'ghost contact damage')

old_desc="{id:'ghost',name:'유령',icon:'👻',tag:'통과 · 시체 빙의',hp:1000,damage:0,speed:170,cooldown:0,description:'적과 닿으면 0.3초 동안 모든 충돌과 공격을 통과해. 팀전에서는 처음 죽은 아군이나 아군 소환수의 시체에 경기당 1회 빙의해. 빙의 중 유령은 사라지고, 빙의체가 죽으면 그 자리에서 유령이 다시 나타나.',detail:'HP 1000 · 접촉 시 0.3초 통과 · 쿨타임 0초 · 팀전 1회 시체 빙의 · 소환수 빙의 가능 · 빙의체 HP 300 / 최대 HP가 300 미만이면 풀 회복 · 빙의체 사망 시 유령 복귀'}"
new_desc="{id:'ghost',name:'유령',icon:'👻',tag:'접촉 15 · 통과 · 시체 빙의',hp:1000,damage:15,speed:170,cooldown:0,description:'적과 닿으면 피해 15를 주고 0.3초 동안 모든 충돌과 공격을 통과해. AI는 멀리서는 접근하지만 가까워지면 살짝 선회해 계속 들러붙지는 않아. 팀전에서는 처음 죽은 아군이나 아군 소환수의 시체에 경기당 1회 빙의해.',detail:'HP 1000 · 접촉 피해 15 + 0.3초 통과 · 가까운 거리 선회 AI · 팀전 1회 시체 빙의 · 소환수 빙의 가능 · 빙의체 HP 300 / 최대 HP가 300 미만이면 풀 회복 · 빙의체 사망 시 유령 복귀'}"
once(old_desc,new_desc,'ghost roster text')

if s==orig:
    raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('V329_GHOST_AI_CONTACT_HOTFIX_APPLIED')

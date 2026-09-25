from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s
old="description:'적과 닿으면 피해 15를 주고 0.3초 동안 모든 충돌과 공격을 통과해. AI는 멀리서는 접근하지만 가까워지면 살짝 선회해 계속 들러붙지는 않아. 팀전에서는 처음 죽은 아군이나 아군 소환수의 시체에 경기당 1회 빙의해.',detail:'HP 1000 · 접촉 피해 15 + 0.3초 통과 · 가까운 거리 선회 AI · 팀전 1회 시체 빙의"
new="description:'적과 닿으면 피해 15를 주고 0.3초 동안 모든 충돌과 공격을 통과해. 이동 AI는 기존 일반 캐릭터 방식이야. 팀전에서는 처음 죽은 아군이나 아군 소환수의 시체에 경기당 1회 빙의해.',detail:'HP 1000 · 접촉 피해 15 + 0.3초 통과 · 일반 이동 AI · 팀전 1회 시체 빙의"
if old not in s: raise SystemExit('ghost description text not found')
s=s.replace(old,new,1)
assert "this.attack(g,e,15*g.scale)" in s
assert "if(f.id==='ghost'&&f.health>0&&f.stunUntil<=this.time&&!f.ghostPossessing)" not in s
assert "BATTLE <b>v3.29</b>" in s
if s==orig: raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('GHOST_AI_TEXT_SYNC_OK')

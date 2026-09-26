from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'missing target ({n}): {old[:160]!r}')
    s=s.replace(old,new,count)

# Publish visible v3.36 while preserving the historical v3.35 block.
rep('<span class="badge">BATTLE <b>v3.35</b></span>','<span class="badge">BATTLE <b>v3.36</b></span>')
rep('<details class="patch-notes"><summary>📒 패치노트 · v3.35</summary><div class="patch-body">',
    '<details class="patch-notes"><summary>📒 패치노트 · v3.36</summary><div class="patch-body"><div class="patch-version"><h3>v3.36 · 그림자의 분신, 사막 군단의 재편</h3><ul><li>카우보이: HP 1000 → 800.</li><li>닌자: HP 30% 이하에서 경기당 1회 분신 1개 소환. 분신 HP 150, 공격 피해는 본체의 50%.</li><li>해골들: 총잡이 해골 공격 간격 1초 → 2초.</li><li>해골들: 취한 해골 공격 간격 3초 → 1.5초.</li><li>조정 모드 히어로: 변신 후 돌진 ↔ 후퇴가 직접 조작에 막히던 문제를 수정하고 고유 돌진/후퇴를 자동 수행.</li><li>해골들: 보스전·릴레이·단체전에서도 총잡이·칼잡이·취한 해골 3마리가 동시에 출전하며 총 3라운드 진행.</li><li>보스 해골들: 해골들만 보스 크기를 1.5배로 적용. 다른 캐릭터의 보스 크기는 기존 규칙 유지.</li></ul></div>')

# Remove v3.36 bullets that had accidentally been appended to the old v3.35 notes.
for x in [
"<li>밸런스: 카우보이 기본 체력 1000 → 750.</li>",
"<li>닌자: HP 30% 이하에서 HP 150 분신을 경기당 1회 소환. 분신 공격 피해는 본체의 50%이며 보스 배율도 적용.</li>",
"<li>해골들: 총잡이 해골 공격 간격 1초 → 2초, 취한 해골 공격 간격 3초 → 1.5초.</li>",
"<li>버그 수정: 조정 모드 히어로가 변신 후 돌진 ↔ 후퇴를 자동으로 수행하도록 수정.</li>",
"<li>버그 수정: 해골들이 보스전·단체전·릴레이에서도 3마리 동시 출전 + 총 3라운드로 정상 작동. 해골들 보스의 크기는 1.5배만 증가.</li>",
]:
    rep(x,'')

# Cowboy requested HP reduction is exactly 1000 -> 800.
rep("hp:750,damage:100,speed:150,cooldown:1,description:'🐴 말을 타고 시작해", "hp:800,damage:100,speed:150,cooldown:1,description:'🐴 말을 타고 시작해")
rep("detail:'HP 750 · 말 탑승 중 이동속도 +100% · 총알 100 · 탄속 약 2.5배", "detail:'HP 800 · 말 탑승 중 이동속도 +100% · 총알 100 · 탄속 약 2.5배")

# Ninja clone HP is fixed at 150, including when the owner is a boss.
rep("const side=this.fighters.length,hp=150*(owner.boss?2.5:1),a=this.rand(-Math.PI,Math.PI),c=", "const side=this.fighters.length,hp=150,a=this.rand(-Math.PI,Math.PI),c=")

# Keep the public Skeletons roster cooldown aligned with the gunner's new 2-second cadence.
rep("{id:'skeletons',name:'해골들',icon:'💀💀💀',tag:'3마리 동시 출전 · 3라운드',hp:125,damage:70,speed:155,cooldown:1,unlock:'skeleton'", "{id:'skeletons',name:'해골들',icon:'💀💀💀',tag:'3마리 동시 출전 · 3라운드',hp:125,damage:70,speed:155,cooldown:2,unlock:'skeleton'")

p.write_text(s,encoding='utf-8')
print('v3.36 finalization applied')

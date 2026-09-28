from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

repls=[
("{id:'sun',name:'태양',icon:'🌞',tag:'태양 투사체 · 월하강림 면역',hp:1000,damage:50,speed:150,cooldown:2,description:'2초마다 ☀️ 투사체를 던진다. 이동 중 피해 50+확정 화상. 벽 직전이나 적에게 맞으면 멈춰 3초 유지되며, 멈춘 태양에 닿으면 피해 100+확정 화상. 달의 월하강림에 면역.',detail:'HP 1000 · ☀️ 50 / 2초 + 화상 · 정지 3초 · 정지 접촉 100 + 화상 · 🌝 월하강림 면역'},",
 "{id:'sun',name:'태양',icon:'🌞',tag:'태양 투사체 · 월하강림 면역',hp:1000,damage:50,speed:150,cooldown:2.5,description:'2.5초마다 ☀️ 투사체를 던진다. 이동 중 피해 50+확정 화상. 벽 직전이나 적에게 맞으면 멈춰 3초 유지되며, 멈춘 태양에 닿으면 피해 50+확정 화상. 달의 월하강림에 면역.',detail:'HP 1000 · ☀️ 50 / 2.5초 + 화상 · 정지 3초 · 정지 접촉 50 + 화상 · 🌝 월하강림 면역'},"),
("const dealt=this.attack(f,hit,100*f.scale);s.stationaryHits[hit.side]=true;if(dealt>0&&hit.health>0)this.applyBurn(f,hit);this.effect(hit,'☀️ 정지 태양 100 + 화상!','burn')",
 "const dealt=this.attack(f,hit,50*f.scale);s.stationaryHits[hit.side]=true;if(dealt>0&&hit.health>0)this.applyBurn(f,hit);this.effect(hit,'☀️ 정지 태양 50 + 화상!','burn')"),
("<h3>v3.62 · 용 밸런스 & 태양</h3>","<h3>v3.62 · 용 밸런스 & 태양</h3>"),
("☀️ 이동 중 피해 50 + 확정 화상. 벽 직전 또는 적 명중 시 정지해 3초 유지, 정지 접촉은 대상별 1회 피해 100 + 확정 화상.","☀️ 이동 중 피해 50 + 확정 화상. 벽 직전 또는 적 명중 시 정지해 3초 유지, 정지 접촉은 대상별 1회 피해 50 + 확정 화상. 공격 주기 2.5초."),
]

for old,new in repls:
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'expected 1 match, got {n}: {old[:100]}')
    s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('v3.62 sun balance hotfix applied')

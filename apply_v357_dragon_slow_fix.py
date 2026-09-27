from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s
repls=[
("<li>💧 물방울 25%: 피해 70 + 3초 동안 이동속도 35% 감소.</li>","<li>💧 물방울 25%: 피해 70 + 2초 동안 이동속도 50% 감소.</li>"),
("💧 3초 35% 감속 25%","💧 2초 50% 감속 25%"),
("hit.slow=Math.max(hit.slow,3);hit.slowPower=Math.max(hit.slowPower,.35);this.effect(hit,'💧 감속 3초!','skill')","hit.slow=Math.max(hit.slow,2);hit.slowPower=Math.max(hit.slowPower,.5);this.effect(hit,'💧 감속 50% · 2초!','skill')")
]
for old,new in repls:
    if old not in s: raise SystemExit('anchor missing: '+old[:80])
    s=s.replace(old,new,1)
for x in ["BATTLE <b>v3.57</b>","hit.slow=Math.max(hit.slow,2)","hit.slowPower=Math.max(hit.slowPower,.5)","💧 2초 50% 감속 25%"]:
    if x not in s: raise SystemExit('missing '+x)
if s==orig: raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('v3.57 dragon water slow corrected to 50% for 2s')

from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    actual=s.count(old)
    if actual < count:
        raise SystemExit(f'PATCH FAILED: {label} ({actual}/{count})')
    s=s.replace(old,new,count)

# v3.25 submarine balance hotfix: Cursed Hand direct projectile damage 50 -> 25.
# Devil Eye body contact damage 50 and curse DOT remain unchanged.
rep("손 HP 113 · 유도 저주탄 피해 50 + 저주", "손 HP 113 · 유도 저주탄 피해 25 + 저주", 'roster hand damage text')
rep("damage:50*hs,armor:0", "damage:25*hs,armor:0", 'cursed hand damage stat')
rep("kind:'curseorb',radius:8*h.scale,speed:230*h.scale,damage:50*h.scale", "kind:'curseorb',radius:8*h.scale,speed:230*h.scale,damage:25*h.scale", 'cursed hand projectile damage')

# Guardrails: keep v3.25 and other current rules intact.
required=[
    'BATTLE <b>v3.25</b>',
    "hp:666,damage:50",
    "접촉 피해 50 + 저주",
    "저주 피해 10 / 0.3초",
    "damage:25*hs",
    "damage:25*h.scale",
    "persistentHand:persistent",
    "expiresAt:persistent?Infinity:this.time+5",
]
missing=[x for x in required if x not in s]
if missing:
    raise SystemExit('GUARD FAILED: '+repr(missing))

p.write_text(s,encoding='utf-8')
print('v3.25 Cursed Hand damage 25 hotfix applied')

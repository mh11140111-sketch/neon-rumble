from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if s.count(old)<count:
        raise SystemExit(f'PATCH FAILED: {label} ({s.count(old)}/{count})')
    s=s.replace(old,new,count)

# Keep v3.25. Clarify only the cursed-hand lifetime rule.
rep(
    '<li>저주받은 대상은 4초마다 🪬 저주받은 손을 소환. 손은 5초 유지, 체력 113, 유도 저주탄을 발사.</li><li>악마의 눈은 13초마다 저주받은 손을 직접 소환. 보스 악마의 눈의 손은 보스 배율을 1.5배만 적용.</li>',
    '<li>저주받은 대상은 4초마다 🪬 저주받은 손을 소환. 이 손은 5초 유지, 체력 113, 유도 저주탄을 발사.</li><li>악마의 눈은 13초마다 저주받은 손을 직접 소환하며, 본체가 직접 소환한 손은 시간 제한 없이 유지. 보스 악마의 눈의 손은 보스 배율을 1.5배만 적용.</li>',
    'v325 notes hand lifetime')

rep(
    "detail:'HP 666 · 접촉 시 저주 · 저주 피해 10 / 0.3초 · 저주 대상 손 소환 4초마다 · 손 HP 113 · 유지 5초 · 유도 저주탄 · 본체 손 소환 13초마다'",
    "detail:'HP 666 · 접촉 시 저주 · 저주 피해 10 / 0.3초 · 저주 대상 손 소환 4초마다 / 5초 유지 · 손 HP 113 · 유도 저주탄 · 본체 손 소환 13초마다 / 무한 유지'",
    'devileye detail')

# Add an explicit persistent flag. Curse-generated hands stay at 5 seconds.
rep(
    'spawnCursedHand(owner,near=null){',
    'spawnCursedHand(owner,near=null,persistent=false){',
    'spawn hand signature')
rep(
    'summon:true,ownerSide:owner.side,expiresAt:this.time+5};',
    'summon:true,ownerSide:owner.side,persistentHand:persistent,expiresAt:persistent?Infinity:this.time+5};',
    'spawn hand lifetime')

# Only Devil Eye body 13-second summons are permanent.
rep(
    "this.spawnCursedHand(f,f);this.effect(f,'🪬 저주받은 손!','skill')",
    "this.spawnCursedHand(f,f,true);this.effect(f,'🪬 저주받은 손!','skill')",
    'body summon persistent')

p.write_text(s,encoding='utf-8')
print('v3.25 body cursed-hand persistence hotfix applied')

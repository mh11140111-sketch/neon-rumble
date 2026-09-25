from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if s.count(old)<count:
        raise SystemExit(f'PATCH FAILED: {label} ({s.count(old)}/{count})')
    s=s.replace(old,new,count)

# Keep v3.25 / patch notes unchanged (submarine balance hotfix).
if 'BATTLE <b>v3.25</b>' not in s:
    raise SystemExit('PATCH FAILED: expected v3.25')

# Devil Eye: direct contact damage 50, while preserving curse.
rep("{id:'devileye',name:'악마의 눈',icon:'🧿',tag:'저주 · 저주받은 손',hp:666,damage:0,speed:155,cooldown:0,description:'몸에 닿은 적에게 저주를 부여해. 저주는 상태이상 면역을 무시하고 0.3초마다 피해 10을 주며, 저주받은 대상은 4초마다 🪬 저주받은 손을 불러내. 악마의 눈도 13초마다 손을 직접 소환해.',detail:'HP 666 · 접촉 시 저주 · 저주 피해 10 / 0.3초 · 저주 대상 손 소환 4초마다 / 5초 유지 · 손 HP 113 · 유도 저주탄 · 본체 손 소환 13초마다 / 무한 유지'}",
    "{id:'devileye',name:'악마의 눈',icon:'🧿',tag:'저주 · 저주받은 손',hp:666,damage:50,speed:155,cooldown:0,description:'몸에 닿은 적에게 직접 피해 50과 저주를 부여해. 저주는 상태이상 면역을 무시하고 0.3초마다 피해 10을 주며, 저주받은 대상은 4초마다 🪬 저주받은 손을 불러내. 악마의 눈도 13초마다 손을 직접 소환해.',detail:'HP 666 · 접촉 피해 50 + 저주 · 저주 피해 10 / 0.3초 · 저주 대상 손 소환 4초마다 / 5초 유지 · 손 HP 113 · 유도 저주탄 피해 50 + 저주 · 본체 손 소환 13초마다 / 무한 유지'}",
    'Devil Eye roster damage')

old_contact="if(f.id==='devileye'&&f.health>0&&f.stunUntil<=this.time)this.applyCurse(f,e);"
new_contact="if(f.id==='devileye'&&f.health>0&&f.stunUntil<=this.time){const freshCurse=this.applyCurse(f,e);if(freshCurse&&e.health>0)this.attack(f,e,50*f.scale);}"
rep(old_contact,new_contact,'Devil Eye contact damage')

# Cursed Hand: base direct projectile damage 50. Boss hand uses its existing x1.5 hand scale => 75.
rep("hp,health:hp,damage:0,armor:0", "hp,health:hp,damage:50*hs,armor:0", 'Cursed Hand damage stat')
rep("kind:'curseorb',radius:8*h.scale,speed:230*h.scale,damage:0,life:4,bounces:0,curseOnly:true",
    "kind:'curseorb',radius:8*h.scale,speed:230*h.scale,damage:50*h.scale,life:4,bounces:0,curseOnly:true",
    'Cursed Hand projectile damage')

old_proj="attackProjectile(f,e,s){if(this.isStudying(e))return;if(s.curseOnly){this.applyCurse(f,e);return}const cd=f.cd,attack=f.attack;"
new_proj="attackProjectile(f,e,s){if(this.isStudying(e))return;if(s.curseOnly){const cd=f.cd,attack=f.attack;this.attack(f,e,s.damage);f.cd=cd;f.attack=attack;if(e.health>0)this.applyCurse(f,e);return}const cd=f.cd,attack=f.attack;"
rep(old_proj,new_proj,'Cursed Hand impact damage')

p.write_text(s,encoding='utf-8')
print('v3.25 Devil Eye + Cursed Hand damage hotfix applied')

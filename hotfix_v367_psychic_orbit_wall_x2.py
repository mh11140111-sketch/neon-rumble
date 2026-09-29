from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="if(s.x<=22+(s.radius||5)||s.x>=698-(s.radius||5)||s.y<=22+(s.radius||5)||s.y>=698-(s.radius||5)){const selfDamage=Math.max(0,s.damage||0);if(selfDamage>0&&p.health>0)this.attack(this.fighters[s.psychicOriginalOwner]||p,p,selfDamage);this.effect(p,'🧱 궤도탄 역충격 '+Math.round(selfDamage)+'!','hit');s.life=0;return true}"
new="if(s.x<=22+(s.radius||5)||s.x>=698-(s.radius||5)||s.y<=22+(s.radius||5)||s.y>=698-(s.radius||5)){const selfDamage=Math.max(0,(s.damage||0)*2);if(selfDamage>0&&p.health>0)this.attack(this.fighters[s.psychicOriginalOwner]||p,p,selfDamage);this.effect(p,'🧱 궤도탄 역충격 '+Math.round(selfDamage)+'!','hit');s.life=0;return true}"
if s.count(old)!=1:
    raise SystemExit(f'psychic orbit wall anchor expected 1, got {s.count(old)}')
s=s.replace(old,new,1)
if "BATTLE <b>v3.67</b>" not in s:
    raise SystemExit('v3.67 marker missing')
if "const selfDamage=Math.max(0,(s.damage||0)*2)" not in s:
    raise SystemExit('x2 marker missing')
p.write_text(s,encoding='utf-8')
print('v3.67 psychic orbit wall x2 hotfix applied')

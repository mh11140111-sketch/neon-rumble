from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# v3.66 psychic orbit wall behavior hotfix:
# old: orbit projectile touches wall -> psychic instant win
# new: psychic takes that projectile's own damage, projectile disappears

start=s.find('updatePsychicOrbitShot(s,dt){')
if start<0:
    raise SystemExit('updatePsychicOrbitShot not found')
end=s.find('\n}', start)
if end<0:
    # minified source may not contain line breaks; bound by next method name
    markers=['smithWeaponSkill(f,e){','psychicSkill(f,e){','firefighterSkill(f,e){']
    poss=[s.find(m,start+1) for m in markers if s.find(m,start+1)>=0]
    if not poss:
        raise SystemExit('could not bound updatePsychicOrbitShot')
    end=min(poss)
block=s[start:end]

# Identify the wall contact branch inside the orbit updater and replace only its body.
wall_pat=re.compile(r"if\(s\.x<=22\+\(s\.radius\|\|5\)\|\|s\.x>=698-\(s\.radius\|\|5\)\|\|s\.y<=22\+\(s\.radius\|\|5\)\|\|s\.y>=698-\(s\.radius\|\|5\)\)\{.*?return true\}")
m=wall_pat.search(block)
if not m:
    raise SystemExit('psychic orbit wall branch not found')
old=m.group(0)
new="if(s.x<=22+(s.radius||5)||s.x>=698-(s.radius||5)||s.y<=22+(s.radius||5)||s.y>=698-(s.radius||5)){const selfDamage=Math.max(0,s.damage||0);if(selfDamage>0&&p.health>0)this.attack(this.fighters[s.psychicOriginalOwner]||p,p,selfDamage);this.effect(p,'🧱 궤도탄 역충격 '+Math.round(selfDamage)+'!','hit');s.life=0;return true}"
block2=block.replace(old,new,1)
s=s[:start]+block2+s[end:]

# Patch-note wording must no longer claim instant victory.
s=s.replace('궤도 투사체가 벽에 닿으면 초능력자가 즉시 승리.','궤도 투사체가 벽에 닿으면 초능력자가 그 투사체의 원래 피해를 입음.')
s=s.replace('궤도탄 벽 접촉 시 즉시 승리','궤도탄 벽 접촉 시 자신이 원래 피해')
s=s.replace('궤도 투사체가 벽에 닿으면 초능력자가 즉시 승리','궤도 투사체가 벽에 닿으면 초능력자가 그 투사체의 원래 피해를 입음')

if 'this.result=p.side' in block2 or 'this.result=p.team' in block2:
    raise SystemExit('instant-win result assignment still present in orbit block')
if "🧱 궤도탄 역충격" not in s:
    raise SystemExit('hotfix marker missing')

p.write_text(s,encoding='utf-8')
print('v3.66 psychic orbit wall hotfix applied')

from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old="""if(pan.enemy&&pan.enemy.health>0&&distance(pan.enemy,pan)<=pan.enemy.radius+pr&&this.time>=f.chefPanNext-1e-9){
   const egg=f.chefEggReady,dmg=(egg?90:65)*f.scale,cd=f.cd,atk=f.attack;this.attack(f,pan.enemy,dmg);f.cd=cd;f.attack=atk;f.chefLastAttackAt=this.time;f.chefPanNext=this.time+1/f.scale;
   if(egg){this.chefConsumeEgg(f);if(pan.enemy.health>0)this.applyBurn(f,pan.enemy);this.effect(f,'🍳 90 + 화상!','skill')}else this.effect(f,'🍳 65','skill');
   return
 }"""
assert old in s
new="""if(pan.enemy&&pan.enemy.health>0&&distance(pan.enemy,pan)<=pan.enemy.radius+pr&&this.time>=f.chefPanNext-1e-9){
   const target=pan.enemy,egg=f.chefEggReady,dmg=(egg?90:65)*f.scale,cd=f.cd,atk=f.attack,dealt=this.attack(f,target,dmg);f.cd=cd;f.attack=atk;
   if(egg){this.chefConsumeEgg(f);if(dealt>0&&target.health>0)this.applyBurn(f,target)}
   if(dealt>0){
     f.chefLastAttackAt=this.time;f.chefPanNext=this.time+3/f.scale;
     if(target.health>0){const push=this.aim(f,target),knock=45*f.scale;target.x+=push.x*knock;target.y+=push.y*knock;this.keepInside(target);target.vx=push.x;target.vy=push.y;target.stunUntil=Math.max(target.stunUntil,this.time+1*f.scale)}
     this.effect(f,egg?'🍳 90 + 화상 · 기절!':'🍳 65 · 기절!','skill')
   }else f.chefPanNext=this.time+.15/f.scale;
   return
 }"""
s=s.replace(old,new,1)

s=s.replace("tag:'프라이팬 · 계란 회복'","tag:'프라이팬 · 기절 · 계란 회복'",1)
s=s.replace("계란이 있을 때 팬이 적에게 닿으면 피해 90 + 화상, 없으면 피해 65를 줘.","계란이 있을 때 팬이 적에게 닿으면 피해 90 + 화상, 없으면 피해 65를 줘. 공격이 적중하면 1초 기절과 약한 넉백을 주고 3초 동안 다시 공격할 수 없어.",1)
s=s.replace("HP 1000 · 팬 공격 65 · 계란 공격 90 + 화상 · 계란 재생 2초", "HP 1000 · 팬 공격 65 · 계란 공격 90 + 화상 · 적중 시 기절 1초 + 약한 넉백 / 공격 쿨타임 3초 · 계란 재생 2초",1)

p.write_text(s,encoding='utf-8')

s2=p.read_text(encoding='utf-8')
assert "f.chefPanNext=this.time+3/f.scale" in s2
assert "target.stunUntil=Math.max(target.stunUntil,this.time+1*f.scale)" in s2
assert "knock=45*f.scale" in s2
assert "기절 1초 + 약한 넉백 / 공격 쿨타임 3초" in s2
print('v3.32 chef hit hotfix applied')

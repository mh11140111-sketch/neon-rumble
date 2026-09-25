from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Version + patch notes
assert 'BATTLE <b>v3.31</b>' in s
assert '📒 패치노트 · v3.31' in s
assert '<div class="patch-body"><div class="patch-version"><h3>v3.31 · 카우보이 & 밸런스</h3>' in s
s=s.replace('BATTLE <b>v3.31</b>','BATTLE <b>v3.32</b>',1)
s=s.replace('📒 패치노트 · v3.31','📒 패치노트 · v3.32',1)
new_notes='''<div class="patch-body"><div class="patch-version"><h3>v3.32 · 요리사</h3><ul><li>신규 캐릭터 👨‍🍳 요리사: 가장 가까운 적을 향해 🍳 프라이팬을 겨누며 팬 접촉으로 공격.</li><li>프라이팬에 계란이 있으면 피해 90 + 화상, 공격 후 계란 소모. 계란이 없으면 피해 65.</li><li>계란은 소모 후 2초 뒤 다시 생성. 5초 동안 공격하지 않고 체력이 부족하면 계란을 먹어 최대 체력의 30% 회복.</li><li>팀전에서는 계란이 있는 프라이팬이 부상당한 아군에게 닿으면 아군이 계란을 먹고 최대 체력의 30% 회복.</li></ul></div><div class="patch-version"><h3>v3.31 · 카우보이 & 밸런스</h3>'''
s=s.replace('<div class="patch-body"><div class="patch-version"><h3>v3.31 · 카우보이 & 밸런스</h3>',new_notes,1)

# Add Chef to roster at the end.
roster_end='\n];\nconst clamp=(n,a,b)=>Math.max(a,Math.min(b,n)),distance=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);'
assert roster_end in s
chef=""",\n{id:'chef',name:'요리사',icon:'👨‍🍳',tag:'프라이팬 · 계란 회복',hp:1000,damage:65,speed:155,cooldown:0,description:'🍳 프라이팬이 가장 가까운 적을 가리켜. 계란이 있을 때 팬이 적에게 닿으면 피해 90 + 화상, 없으면 피해 65를 줘. 계란은 2초 뒤 다시 생기고, 5초 동안 공격하지 않으면 계란을 먹어 최대 체력의 30%를 회복해. 팀전에서는 팬이 아군에게 닿으면 계란으로 아군도 30% 회복해.',detail:'HP 1000 · 팬 공격 65 · 계란 공격 90 + 화상 · 계란 재생 2초 · 5초 무공격 시 자기 회복 30% · 계란 팬이 아군 접촉 시 아군 회복 30%'}"""
s=s.replace(roster_end,chef+roster_end,1)

# Chef runtime state.
old="cowboyMounted:type.id==='cowboy',cowboyAmmo:type.id==='cowboy'?6:0,cowboyReloadUntil:0,ghostReviveUsed:false"
assert old in s
new="cowboyMounted:type.id==='cowboy',cowboyAmmo:type.id==='cowboy'?6:0,cowboyReloadUntil:0,chefEggReady:type.id==='chef',chefEggReadyAt:0,chefLastAttackAt:0,chefPanNext:0,ghostReviveUsed:false"
s=s.replace(old,new,1)

# Chef methods before Angry Man.
marker='angryManSkill(f,e,dt){'
assert marker in s
chef_methods=r'''chefPanTip(f){
 const e=this.nearest(f);if(!e)return {x:f.x,y:f.y-f.radius-42*f.scale,enemy:null};
 const a=this.aim(f,e),reach=f.radius+48*f.scale;return {x:f.x+a.x*reach,y:f.y+a.y*reach,enemy:e}
}
chefConsumeEgg(f){f.chefEggReady=false;f.chefEggReadyAt=this.time+2/f.scale}
chefHeal(f,target,label){if(!f.chefEggReady||!target||target.health<=0||target.health>=target.hp)return false;const before=target.health,heal=Math.max(1,Math.round(target.hp*.3));target.health=Math.min(target.hp,target.health+heal);const actual=Math.round(target.health-before);if(actual<=0)return false;f.healed=(f.healed||0)+actual;this.chefConsumeEgg(f);this.effect(target,'🥚 +'+actual,'heal');this.emit(label);return true}
chefSkill(f){
 if(f.id!=='chef'||f.health<=0||f.stunUntil>this.time)return;
 if(!f.chefEggReady&&this.time>=f.chefEggReadyAt-1e-9){f.chefEggReady=true;this.effect(f,'🥚 계란 준비!','skill')}
 const pan=this.chefPanTip(f),pr=22*f.scale;
 if(f.chefEggReady){
   const allies=this.fighters.filter(a=>a!==f&&a.team===f.team&&a.health>0&&a.health<a.hp&&distance(a,pan)<=a.radius+pr);
   if(allies.length){allies.sort((a,b)=>distance(a,pan)-distance(b,pan));if(this.chefHeal(f,allies[0],'👨‍🍳 아군이 계란을 먹고 회복!'))return}
 }
 if(pan.enemy&&pan.enemy.health>0&&distance(pan.enemy,pan)<=pan.enemy.radius+pr&&this.time>=f.chefPanNext-1e-9){
   const egg=f.chefEggReady,dmg=(egg?90:65)*f.scale,cd=f.cd,atk=f.attack;this.attack(f,pan.enemy,dmg);f.cd=cd;f.attack=atk;f.chefLastAttackAt=this.time;f.chefPanNext=this.time+1/f.scale;
   if(egg){this.chefConsumeEgg(f);if(pan.enemy.health>0)this.applyBurn(f,pan.enemy);this.effect(f,'🍳 90 + 화상!','skill')}else this.effect(f,'🍳 65','skill');
   return
 }
 if(f.chefEggReady&&f.health<f.hp&&this.time-f.chefLastAttackAt>=5/f.scale-1e-9)this.chefHeal(f,f,'👨‍🍳 요리사가 계란을 먹고 회복!')
}
'''
s=s.replace(marker,chef_methods+marker,1)

# Invoke Chef skill.
old="if(f.id==='angryman')this.angryManSkill(f,e,dt);if(f.id==='cowboy')this.cowboySkill(f,e);"
assert old in s
s=s.replace(old,old+"if(f.id==='chef')this.chefSkill(f);",1)

# Chef has no generic body-contact melee.
old="'lizardtail','ghost','cowboy'].includes(f.id)"
assert old in s
s=s.replace(old,"'lizardtail','ghost','cowboy','chef'].includes(f.id)",1)

# Render Chef's pan pointed toward the nearest enemy. Draw a visible egg only when ready.
draw_marker="circle(f.x,f.y,r,f.flash>0?'#ffffff':c);circle(f.x,f.y,r-4,'#152338');"
assert draw_marker in s
chef_draw=r'''if(f.id==='chef'&&f.health>0){const pp=engine.chefPanTip(f),pa=Math.atan2(pp.y-f.y,pp.x-f.x);ctx.save();ctx.strokeStyle='#a9b2bd';ctx.lineWidth=8*f.scale;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(f.x+Math.cos(pa)*(r*.55),f.y+Math.sin(pa)*(r*.55));ctx.lineTo(pp.x-Math.cos(pa)*12*f.scale,pp.y-Math.sin(pa)*12*f.scale);ctx.stroke();circle(pp.x,pp.y,19*f.scale,'#343a40');circle(pp.x,pp.y,14*f.scale,'#171b20');if(f.chefEggReady){circle(pp.x-2*f.scale,pp.y,9*f.scale,'#fff7dc');circle(pp.x+1*f.scale,pp.y,4.5*f.scale,'#ffc83d')}ctx.restore();}'''
s=s.replace(draw_marker,chef_draw+draw_marker,1)

p.write_text(s,encoding='utf-8')

# Static safeguards
s2=p.read_text(encoding='utf-8')
checks=[
 'BATTLE <b>v3.32</b>',
 '📒 패치노트 · v3.32',
 "id:'chef'",
 'chefPanTip(f){',
 'chefSkill(f){',
 "chefEggReady:type.id==='chef'",
 'f.chefEggReadyAt=this.time+2/f.scale',
 'this.time-f.chefLastAttackAt>=5/f.scale',
 'dmg=(egg?90:65)*f.scale',
 'this.applyBurn(f,pan.enemy)',
 "'cowboy','chef'].includes(f.id)",
 "if(f.id==='chef')this.chefSkill(f);",
 "if(f.id==='chef'&&f.health>0)"
]
for c in checks: assert c in s2,c
print('v3.32 patch applied and verified')

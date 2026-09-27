from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

def rep(old,new,label,count=1):
    global s
    if old not in s: raise SystemExit(label+' anchor missing')
    s=s.replace(old,new,count)

# Version / patch notes
rep('BATTLE <b>v3.56</b>','BATTLE <b>v3.57</b>','version')
rep('📒 패치노트 · v3.56','📒 패치노트 · v3.57','patch title')
marker='<div class="patch-body">'
patch='''<div class="patch-version"><h3>v3.57 · 여의주의 신통력</h3><ul><li>🐉 용 일반공격 추가: 2초마다 여의주의 신통력 발동.</li><li>💨 바람 25%: 피해 70 + 강한 밀치기.</li><li>⚡ 번개 25%: 피해 70 + 0.5초 기절.</li><li>💧 물방울 25%: 피해 70 + 3초 동안 이동속도 35% 감소.</li><li>🍃 나뭇잎 25%: 피해 70 + 실제 입힌 피해의 100%만큼 용 체력 회복.</li></ul></div>'''
if patch not in s: rep(marker,marker+patch,'patch notes')

# Update dragon roster copy.
old="{id:'dragon',name:'용',icon:'🐉',tag:'비의 분노 · 신기루 · 여의주 부활',hp:1000,damage:0,speed:150,cooldown:0,description:'10초마다 5초 동안 비의 분노를 사용해 0.1초마다 무작위 대상에게 빗방울 피해 10을 준다. 빗방울마다 5% 확률로 거대한 번개 피해 150. 15초마다 5초 신기루로 모든 공격을 회피한다. 사망하면 HP 50 여의주가 되어 도망치고 5초 생존 시 부활한다.',detail:'HP 1000 · 비 5초 / 0.1초마다 10 · 빗방울마다 번개 5% / 150 · 비 종료 후 쿨타임 10초 · 신기루 5초 완전 회피 / 종료 후 15초 쿨타임 · 여의주 HP 50 / 5초 후 부활'},"
new="{id:'dragon',name:'용',icon:'🐉',tag:'여의주의 신통력 · 비의 분노 · 신기루 · 부활',hp:1000,damage:70,speed:150,cooldown:2,description:'2초마다 여의주의 신통력으로 바람·번개·물방울·나뭇잎 중 하나를 25% 확률로 발사한다. 모든 공격 피해는 70이며 각각 밀치기·0.5초 기절·감속·100% 흡혈 효과가 있다. 비의 분노와 신기루, 여의주 부활도 사용한다.',detail:'HP 1000 · 신통력 70 / 2초 · 💨 밀치기 25% · ⚡ 0.5초 기절 25% · 💧 3초 35% 감속 25% · 🍃 피해 100% 회복 25% · 비의 분노 · 신기루 · 여의주 부활'},"
rep(old,new,'dragon roster')

# Constructor state.
old="dragonMirageNext:type.id==='dragon'?15/scale:9999,dragonMirageUntil:0,dragonOrb:false"
new="dragonMirageNext:type.id==='dragon'?15/scale:9999,dragonMirageUntil:0,dragonMysticNext:type.id==='dragon'?2/scale:9999,dragonOrb:false"
rep(old,new,'dragon mystic constructor')

# Add mystic attack method before rain drop.
anchor='dragonRainDrop(f){\n'
method="""dragonMysticAttack(f,e){
 if(!f||!e||f.id!=='dragon'||f.dragonOrb||f.health<=0||f.stunUntil>this.time||this.time<(f.dragonMysticNext||0)-1e-9)return;
 f.dragonMysticNext=this.time+2/f.scale;
 const r=this.random(),kind=r<.25?'dragon_wind':r<.5?'dragon_thunder':r<.75?'dragon_bubble':'dragon_leaf',icon=kind==='dragon_wind'?'💨':kind==='dragon_thunder'?'⚡':kind==='dragon_bubble'?'💧':'🍃',a=this.aim(f,e);
 this.shots.push({x:f.x+a.x*(f.radius+10),y:f.y+a.y*(f.radius+10),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind,icon,radius:(kind==='dragon_wind'?14:10)*f.scale,speed:390*f.scale,damage:70*f.scale,life:4/f.scale,bounces:0});
 this.effect(f,icon+' 여의주의 신통력!','skill')
}
"""
if 'dragonMysticAttack(f,e){' not in s: rep(anchor,method+anchor,'dragon mystic method')

# Invoke from stepFighter.
old="if(f.id==='merman')this.mermanSkill(f,e);if(f.id==='detective')"
new="if(f.id==='merman')this.mermanSkill(f,e);if(f.id==='dragon')this.dragonMysticAttack(f,e);if(f.id==='detective')"
rep(old,new,'dragon mystic call')

# Special projectile collisions after wave branch and before falling rain branch.
rain_anchor="""  if(s.kind==='dragon_rain'||s.kind==='dragon_lightning'){
"""
branch="""  if(['dragon_wind','dragon_thunder','dragon_bubble','dragon_leaf'].includes(s.kind)){
   const hit=this.enemies(f).find(e=>distance(s,e)<e.radius+s.radius);
   if(hit){const dealt=this.attack(f,hit,s.damage);if(dealt>0&&hit.health>0){if(s.kind==='dragon_wind'){hit.x+=s.vx*180*f.scale;hit.y+=s.vy*180*f.scale;this.keepInside(hit);this.effect(hit,'💨 밀려남!','skill')}else if(s.kind==='dragon_thunder'){hit.stunUntil=Math.max(hit.stunUntil,this.time+.5);this.effect(hit,'⚡ 기절 0.5초!','skill')}else if(s.kind==='dragon_bubble'){hit.slow=Math.max(hit.slow,3);hit.slowPower=Math.max(hit.slowPower,.35);this.effect(hit,'💧 감속 3초!','skill')}else if(s.kind==='dragon_leaf'){const heal=Math.min(f.hp-f.health,dealt);f.health+=heal;f.healed+=heal;if(heal)this.effect(f,'🍃 +'+Math.round(heal),'heal')}}s.life=0;if(this.result!==null)break}
   if(s.x<22||s.x>698||s.y<22||s.y>698)s.life=0;
   continue
  }
"""
if "['dragon_wind','dragon_thunder','dragon_bubble','dragon_leaf'].includes(s.kind)" not in s:
    rep(rain_anchor,branch+rain_anchor,'dragon mystic collision')

# Render the four projectiles.
render_anchor="""if(s.kind==='dragon_rain'){"""
render="""if(['dragon_wind','dragon_thunder','dragon_bubble','dragon_leaf'].includes(s.kind)){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(Math.max(26,s.radius*2.7))+'px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(s.kind==='dragon_wind'?'💨':s.kind==='dragon_thunder'?'⚡':s.kind==='dragon_bubble'?'💧':'🍃',0,0)}else if(s.kind==='dragon_rain'){"""
rep(render_anchor,render,'dragon mystic renderer')

# Reset attack timer after orb revival.
old="f.dragonRainNext=this.time+10/f.scale;f.dragonMirageNext=this.time+15/f.scale;"
new="f.dragonRainNext=this.time+10/f.scale;f.dragonMirageNext=this.time+15/f.scale;f.dragonMysticNext=this.time+2/f.scale;"
rep(old,new,'dragon revive mystic reset')

required=['BATTLE <b>v3.57</b>',"dragonMysticNext:type.id==='dragon'?2/scale:9999",'dragonMysticAttack(f,e){',"kind=r<.25?'dragon_wind':r<.5?'dragon_thunder':r<.75?'dragon_bubble':'dragon_leaf'","damage:70*f.scale","this.time+.5","hit.slow=Math.max(hit.slow,3)","hit.slowPower=Math.max(hit.slowPower,.35)",'const heal=Math.min(f.hp-f.health,dealt)',"hit.x+=s.vx*180*f.scale"]
for x in required:
    if x not in s: raise SystemExit('missing marker '+x)
if s==orig: raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('v3.57 dragon mystic patch applied')

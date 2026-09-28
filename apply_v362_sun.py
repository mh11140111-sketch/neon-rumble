from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

# Version / patch notes
once('<span class="badge">BATTLE <b>v3.61</b></span>','<span class="badge">BATTLE <b>v3.62</b></span>','badge')
once('<details class="patch-notes"><summary>📒 패치노트 · v3.61</summary><div class="patch-body">','<details class="patch-notes"><summary>📒 패치노트 · v3.62</summary><div class="patch-body"><div class="patch-version"><h3>v3.62 · 용 밸런스 & 태양</h3><ul><li>🐉 용 비의 분노 빗방울 피해 5 → 10.</li><li>🌞 신규 캐릭터 태양 추가. HP 1000 · 이동속도 150 · ☀️ 투사체 2초.</li><li>☀️ 이동 중 적중 시 피해 50 + 확정 화상. 벽 직전 또는 적중 시 정지해 3초 유지.</li><li>정지한 ☀️에 닿은 적은 대상별 1회 피해 100 + 확정 화상.</li><li>🌞 태양은 🌝 달의 월하강림 즉사 궁극기에 면역.</li></ul></div>','patch notes')

# Dragon rain damage inside dragonRainDrop only
m=re.search(r'(dragonRainDrop\(f\)\{.*?this\.shots\.push\(\{.*?kind:\'dragon_rain\'.*?damage:)([^,}]+)',s,re.S)
if not m:
    raise SystemExit('dragon rain damage anchor not found')
old=m.group(0)
if '5*f.scale' not in m.group(2).replace(' ',''):
    raise SystemExit('dragon rain damage is not expected 5*f.scale: '+m.group(2))
new=m.group(1)+'10*f.scale'
s=s[:m.start()]+new+s[m.end():]

# Add Sun roster after Love Man
love="{id:'loveman',name:'사랑의 남자',icon:'😍',tag:'유도 하트 · 회복 · 유혹',hp:1000,damage:40,speed:150,cooldown:1.5,description:'1.5초마다 네 종류의 하트 중 하나를 각 25% 확률로 사용한다. ❤️‍🔥 피해 40+화상, ❤️ 아군 50 회복(아군이 없으면 자기 회복), 💖 피해 40+1초 기절, 💓 피해 50+3초 유혹.',detail:'HP 1000 · 1.5초 · ❤️‍🔥 40+화상 25% · ❤️ 아군 50회복 25% · 💖 40+기절1초 25% · 💓 50+유혹3초 25%'},"
sun="{id:'sun',name:'태양',icon:'🌞',tag:'태양 투사체 · 월하강림 면역',hp:1000,damage:50,speed:150,cooldown:2,description:'2초마다 ☀️ 투사체를 던진다. 이동 중 피해 50+확정 화상. 벽 직전이나 적에게 맞으면 멈춰 3초 유지되며, 멈춘 태양에 닿으면 피해 100+확정 화상. 달의 월하강림에 면역.',detail:'HP 1000 · ☀️ 50 / 2초 + 화상 · 정지 3초 · 정지 접촉 100 + 화상 · 🌝 월하강림 면역'},"
once(love, love+'\n'+sun, 'sun roster')

# Moon ultimate immunity
old="for(const e of this.fighters){if(e===f||e.health<=0||this.dragonMirageActive(e))continue;e.health=0;"
new="for(const e of this.fighters){if(e===f||e.health<=0||this.dragonMirageActive(e))continue;if(e.id==='sun'){this.effect(e,'🌞 월하강림 면역!','skill');continue}e.health=0;"
once(old,new,'moon immunity')

# Sun skill method before loveManSkill
anchor='loveManSkill(f,e){'
if s.count(anchor)!=1:
    raise SystemExit('loveManSkill anchor count '+str(s.count(anchor)))
sun_method="""sunSkill(f,e){
 if(!f||!e||f.id!=='sun'||f.health<=0||f.stunUntil>this.time||f.cd>1e-9)return;
 const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+10),y:f.y+a.y*(f.radius+10),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'sun_orb',icon:'☀️',radius:15*f.scale,speed:320*f.scale,damage:50*f.scale,life:6/f.scale,bounces:0,stopped:false,stationaryHits:{}});f.cd=2/f.scale;f.attack=.18/f.scale;this.effect(f,'☀️ 태양 투사체!','skill')
}
"""
s=s.replace(anchor,sun_method+anchor,1)

# Hook skill and exclude standard contact attack
old="if(f.id==='dragon')this.dragonMysticAttack(f,e);if(f.id==='loveman')this.loveManSkill(f,e);"
new="if(f.id==='dragon')this.dragonMysticAttack(f,e);if(f.id==='sun')this.sunSkill(f,e);if(f.id==='loveman')this.loveManSkill(f,e);"
once(old,new,'sun skill hook')
old_excl="'crab_shell','dragon','loveman','alien'"
new_excl="'crab_shell','dragon','sun','loveman','alien'"
once(old_excl,new_excl,'sun contact exclusion')

# Dedicated projectile branch before generic movement
anchor="  s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;\n  if(s.kind==='wave')"
if s.count(anchor)!=1:
    raise SystemExit('projectile movement anchor count '+str(s.count(anchor)))
branch="""  if(s.kind==='sun_orb'){
   if(!s.stopped){
    s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;
    const hit=this.enemies(f).find(e=>e.health>0&&distance(s,e)<e.radius+s.radius);
    if(hit){const dealt=this.attack(f,hit,50*f.scale);if(dealt>0&&hit.health>0)this.applyBurn(f,hit);s.stopped=true;s.vx=0;s.vy=0;s.speed=0;s.life=3/f.scale;s.stationaryHits={};this.effect(hit,'☀️ 50 + 화상!','burn')}
    else if(s.x<=22+s.radius||s.x>=698-s.radius||s.y<=22+s.radius||s.y>=698-s.radius){s.x=clamp(s.x,22+s.radius,698-s.radius);s.y=clamp(s.y,22+s.radius,698-s.radius);s.stopped=true;s.vx=0;s.vy=0;s.speed=0;s.life=3/f.scale;s.stationaryHits={};this.effect(f,'☀️ 정지 · 3초','skill')}
   }else{
    for(const hit of this.enemies(f)){if(hit.health<=0||s.stationaryHits[hit.side]||distance(s,hit)>=hit.radius+s.radius)continue;const dealt=this.attack(f,hit,100*f.scale);s.stationaryHits[hit.side]=true;if(dealt>0&&hit.health>0)this.applyBurn(f,hit);this.effect(hit,'☀️ 정지 태양 100 + 화상!','burn');if(this.result!==null)break}
   }
   continue
  }
  s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;
  if(s.kind==='wave')"""
s=s.replace(anchor,branch,1)

# Renderer
anchor="for(const s of engine.shots){ctx.save();ctx.translate(s.x,s.y);ctx.rotate(Math.atan2(s.vy,s.vx));if(['love_burn'"
if s.count(anchor)!=1:
    raise SystemExit('renderer anchor count '+str(s.count(anchor)))
repl="for(const s of engine.shots){ctx.save();ctx.translate(s.x,s.y);ctx.rotate(Math.atan2(s.vy,s.vx));if(s.kind==='sun_orb'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(Math.max(s.stopped?42:30,s.radius*(s.stopped?3.2:2.8)))+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('☀️',0,0)}else if(['love_burn'"
s=s.replace(anchor,repl,1)

p.write_text(s,encoding='utf-8')
print('v3.62 applied')

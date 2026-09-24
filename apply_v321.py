from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(f'PATCH FAILED: {label}')
    s=s.replace(old,new,count)

def sub(pattern,repl,label,count=1):
    global s
    ns,n=re.subn(pattern,repl,s,count=count,flags=re.S)
    if n!=count:
        raise SystemExit(f'PATCH FAILED: {label} ({n}/{count})')
    s=ns

# v3.21 badge + patch notes
rep('BATTLE <b>v3.20</b>','BATTLE <b>v3.21</b>','version badge')
rep('📒 패치노트 · v3.20','📒 패치노트 · v3.21','patch summary')
anchor='<div class="patch-body"><div class="patch-version"><h3>v3.20 · 알라딘 & 밸런스</h3>'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.21 · 지니 회전팔 & AI 개선</h3><ul><li>알라딘과 지니 AI가 벽 근처에 머무르지 않고 다른 캐릭터처럼 전장을 적극적으로 이동하도록 개선.</li><li>지니 공격 리워크: 3초마다 1초 동안 파란 팔이 지니 몸 주위를 빠르게 회전.</li><li>회전팔은 적을 관통하며 공격 1회당 각 대상에게 피해 100을 1회 적용.</li><li>보스 지니는 기존 보스 배율을 유지해 공격력·이동속도·공격 주기 강화가 적용됨.</li></ul></div><div class="patch-version"><h3>v3.20 · 알라딘 & 밸런스</h3>'
rep(anchor,insert,'patch notes')

# Aladdin roster description
old="{id:'aladdin',name:'알라딘',icon:'👳‍♀️',tag:'지니 소환 · 2회 부활',hp:500,damage:50,speed:165,cooldown:0,description:'전투 시작과 동시에 체력 1500의 🧞‍♂️ 지니를 소환해. 지니는 3초마다 큰 팔을 휘둘러 범위 피해 50. 지니가 쓰러지면 최대 2회 부활하며, 부활할 때마다 알라딘의 최대/현재 체력과 지니 공격력이 절반이 돼.',detail:'알라딘 HP 500 · 지니 HP 1500 · 범위 공격 50 / 3초 · 지니 최대 2회 부활 · 부활마다 알라딘 체력 및 지니 공격력 1/2 · 알라딘 사망 시 지니와 무관하게 패배'}"
new="{id:'aladdin',name:'알라딘',icon:'👳‍♀️',tag:'지니 소환 · 회전팔 · 2회 부활',hp:500,damage:50,speed:165,cooldown:0,description:'전투 시작과 동시에 체력 1500의 🧞‍♂️ 지니를 소환해. 지니는 3초마다 1초 동안 파란 팔을 몸 주위로 빠르게 회전시켜 관통 피해 100을 줘. 지니가 쓰러지면 최대 2회 부활하며, 부활할 때마다 알라딘의 최대/현재 체력과 지니 공격력이 절반이 돼.',detail:'알라딘 HP 500 · 지니 HP 1500 · 회전팔 100 / 3초 · 유지 1초 · 관통 · 공격 1회당 대상별 1회 피격 · 지니 최대 2회 부활 · 부활마다 알라딘 체력 및 지니 공격력 1/2 · 알라딘 사망 시 지니와 무관하게 패배'}"
rep(old,new,'aladdin roster')

# Genie base stats: new attack damage + attack state
rep("tag:'큰 팔 휘두르기',description:'3초마다 큰 팔을 휘둘러 범위 공격.',detail:''",
    "tag:'회전팔',description:'3초마다 1초 동안 파란 팔을 몸 주위로 빠르게 회전시켜 관통 공격.',detail:''",
    'genie text')
rep("damage:50*scale*(owner.geniePower||1),armor:0",
    "damage:100*scale*(owner.geniePower||1),armor:0",
    'genie base damage')
rep("genieResolved:false}",
    "genieResolved:false,genieArmStart:-1,genieArmUntil:-1,genieArmHits:{}}",
    'genie arm state')
rep("g.damage=50*owner.scale*owner.geniePower;g.cd=3/owner.scale;",
    "g.damage=100*owner.scale*owner.geniePower;g.cd=3/owner.scale;g.genieArmStart=-1;g.genieArmUntil=-1;g.genieArmHits={};",
    'genie revive damage')

# Rework Genie: independent movement + 1 second fast rotating piercing arm.
new_genie="""genieSkill(g,dt){
 if(g.id!=='genie')return;if(!Number.isFinite(g.hp))g.hp=1500*(g.boss?2.5:1);if(!Number.isFinite(g.health))g.health=g.hp;if(g.health<=0)return;
 const owner=this.fighters[g.ownerSide];if(!owner||owner.health<=0){g.health=0;return}
 if(g.genieArmUntil===undefined){g.genieArmStart=-1;g.genieArmUntil=-1;g.genieArmHits={}}
 g.cd=Math.max(0,g.cd-dt);
 if(g.stunUntil<=this.time){const target=this.nearest(g);if(target){const a=this.aim(g,target);g.vx=a.x;g.vy=a.y;g.x+=g.vx*g.speed*dt;g.y+=g.vy*g.speed*dt;this.keepInside(g)}}
 if(g.cd<=1e-9&&this.time>=g.genieArmUntil-1e-9){g.cd=3/g.scale;g.genieArmStart=this.time;g.genieArmUntil=this.time+1;g.genieArmHits={};g.attack=1;this.effect(g,'🧞‍♂️ 회전팔!','skill');this.emit('🧞‍♂️ 지니가 회전팔 공격!')}
 if(this.time<g.genieArmUntil-1e-9){const phase=clamp((this.time-g.genieArmStart),0,1),a=phase*Math.PI*2*3,len=145*g.scale,dx=Math.cos(a),dy=Math.sin(a);for(const e of this.enemies(g)){if(e.health<=0||g.genieArmHits[e.side])continue;const rx=e.x-g.x,ry=e.y-g.y,along=rx*dx+ry*dy,perp=Math.abs(rx*dy-ry*dx);if(along>=0&&along<=len+e.radius&&perp<=e.radius+24*g.scale){const dealt=this.attack(g,e,g.damage);if(dealt>0)g.genieArmHits[e.side]=true;if(this.result!==null)return}}}
}
reviveGenies(){"""
sub(r"genieSkill\(g,dt\)\{.*?\n\}\nreviveGenies\(\)\{",new_genie,'genie skill rework')

# Aladdin AI: continuously seek the closest opponent so it does not camp at walls.
needle="stepFighter(f,e,dt){\n if(f.id==='genie'){this.genieSkill(f,dt);return}"
replacement="stepFighter(f,e,dt){\n if(f.id==='genie'){this.genieSkill(f,dt);return}\n if(f.id==='aladdin'&&f.health>0&&f.stunUntil<=this.time){const at=this.nearest(f);if(at){const aa=this.aim(f,at);f.vx=aa.x;f.vy=aa.y;f.turn=.35}}"
rep(needle,replacement,'aladdin movement ai')

# Draw the Genie arm only while attacking. Stylized after the supplied blue arm/gold cuff reference.
draw_anchor="circle(f.x,f.y,r,f.flash>0?'#ffffff':c);circle(f.x,f.y,r-4,'#152338');"
draw_insert="""if(f.id==='genie'&&f.health>0&&f.genieArmUntil>engine.time){const phase=clamp(engine.time-f.genieArmStart,0,1),ga=phase*Math.PI*2*3,gs=f.scale;ctx.save();ctx.translate(f.x,f.y);ctx.rotate(ga);ctx.globalAlpha=.97;ctx.shadowColor='#2b91ff';ctx.shadowBlur=12*gs;ctx.fillStyle='#f0b51f';ctx.beginPath();ctx.roundRect(f.radius*.62,-18*gs,34*gs,36*gs,9*gs);ctx.fill();ctx.shadowBlur=0;ctx.fillStyle='#258eff';ctx.beginPath();ctx.roundRect(f.radius*.62+28*gs,-21*gs,82*gs,42*gs,21*gs);ctx.fill();ctx.beginPath();ctx.arc(f.radius*.62+108*gs,0,28*gs,0,Math.PI*2);ctx.fill();ctx.fillStyle='#55b5ff';ctx.globalAlpha=.6;ctx.beginPath();ctx.ellipse(f.radius*.62+70*gs,-8*gs,36*gs,8*gs,0,0,Math.PI*2);ctx.fill();ctx.restore();ctx.globalAlpha=f.id==='invisible'?.38:1;}circle(f.x,f.y,r,f.flash>0?'#ffffff':c);circle(f.x,f.y,r-4,'#152338');"""
rep(draw_anchor,draw_insert,'genie arm visual')

# Ability HUD text reflects new attack.
rep("return '👳‍♀️ 알라딘 '+Math.ceil(f.health)+' / '+Math.ceil(f.hp)+' HP · 🧞‍♂️ 지니 '+ghp+' / '+gmax+' HP · 부활 '+(f.genieRevives||0)+'/2 · 지니 공격력 x'+(f.geniePower||1)",
    "return '👳‍♀️ 알라딘 '+Math.ceil(f.health)+' / '+Math.ceil(f.hp)+' HP · 🧞‍♂️ 지니 '+ghp+' / '+gmax+' HP · 회전팔 100 · 부활 '+(f.genieRevives||0)+'/2 · 지니 공격력 x'+(f.geniePower||1)",
    'ability text')

# Boss rule wording for Genie attack.
rep('보스 알라딘의 지니는 체력 3750, 공격력·속도·공격 주기 등 보스 능력 배율을 함께 적용받아.',
    '보스 알라딘의 지니는 체력 3750이며 회전팔 피해 200, 공격 주기 1.5초 등 보스 능력 배율을 함께 적용받아.',
    'boss genie rule')

p.write_text(s,encoding='utf-8')
print('NEON RUMBLE v3.21 applied')

from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(f'PATCH FAILED: {label}')
    s=s.replace(old,new,count)

# Version and patch notes
rep('BATTLE <b>v3.18</b>','BATTLE <b>v3.19</b>','version badge')
rep('📒 패치노트 · v3.18','📒 패치노트 · v3.19','patch summary')
anchor='<div class="patch-body"><div class="patch-version"><h3>v3.18 · 조정 모드</h3>'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.19 · 만능 로봇</h3><ul><li>신규 캐릭터 🤖 로봇 추가.</li><li>레이저: 5초마다 발동해 4초 동안 맵 전체를 한 바퀴 천천히 회전하며, 회전 1회당 맞은 적에게 피해 50을 1회 줌.</li><li>만능로봇팔: 7초마다 자신을 제외한 전장 모든 캐릭터를 밀쳐내고 피해 30 + 1초 기절.</li></ul></div><div class="patch-version"><h3>v3.18 · 조정 모드</h3>'
rep(anchor,insert,'patch notes')

# Roster
police="{id:'police',name:'경찰',icon:'👮‍♂️',tag:'테이저 · 총 난사',hp:1000,damage:30,speed:155,cooldown:1,description:'1초마다 테이저건을 발사해 피해 30과 0.2초 기절을 줘. 체력이 30% 이하가 되면 경기당 1회, 3초 동안 조준 없이 무작위 방향으로 총을 연속 발사해.',detail:'테이저 30 / 1초 · 명중 시 기절 0.2초 · HP 30% 이하 1회 총 난사 · 3초 동안 0.38초마다 1발 · 무작위 방향 · 총탄 100 · 벽 반사 없음'}"
robot="{id:'robot',name:'로봇',icon:'🤖',tag:'회전 레이저 · 만능로봇팔',hp:1000,damage:50,speed:150,cooldown:5,description:'5초마다 맵 전체를 천천히 한 바퀴 도는 레이저를 발사해 피해 50. 7초마다 만능로봇팔로 자신을 제외한 모든 캐릭터를 밀쳐내고 피해 30과 1초 기절을 줘.',detail:'레이저 50 · 5초마다 · 4초간 1회전 · 회전당 대상별 1회 피격 · 로봇팔 30 · 7초 · 전장 전체 밀치기 · 기절 1초'}"
rep(police+'\n];',police+',\n'+robot+'\n];','robot roster')

# Robot skills, inserted before puffer skill.
anchor_skill="pufferSpikes(f){if(f.id!=='puffer'||f.health<=0||f.cd>1e-9)return;"
robot_skill="""robotSkill(f){
 if(f.id!=='robot'||f.health<=0)return;
 if(f.robotLaserNext===undefined){f.robotLaserNext=this.time+5/f.scale;f.robotLaserStart=-1;f.robotLaserUntil=-1;f.robotLaserHits={};f.robotArmNext=this.time+7/f.scale}
 if(this.time>=f.robotLaserNext-1e-9){f.robotLaserStart=this.time;f.robotLaserUntil=this.time+4/f.scale;f.robotLaserNext=this.time+5/f.scale;f.robotLaserHits={};this.effect(f,'🔴 회전 레이저!','skill');this.emit('🤖 로봇이 회전 레이저 발사!')}
 if(this.time<f.robotLaserUntil-1e-9){const duration=4/f.scale,phase=clamp((this.time-f.robotLaserStart)/duration,0,1),a=-Math.PI/2+phase*Math.PI*2,dx=Math.cos(a),dy=Math.sin(a);for(const e of this.enemies(f)){if(e.health<=0||f.robotLaserHits[e.side])continue;const rx=e.x-f.x,ry=e.y-f.y,along=rx*dx+ry*dy,perp=Math.abs(rx*dy-ry*dx);if(along>=0&&perp<=e.radius+9*f.scale){const dealt=this.attack(f,e,50*f.scale);if(dealt>0)f.robotLaserHits[e.side]=true;if(this.result!==null)return}}}
 if(this.time>=f.robotArmNext-1e-9){f.robotArmNext=this.time+7/f.scale;this.effects.push({x:f.x,y:f.y,text:'만능로봇팔!',kind:'shockwave',side:f.side,team:f.team,life:.8});this.emit('🤖 만능로봇팔!');this.resolvingBlast=true;for(const e of this.fighters){if(e===f||e.health<=0)continue;const a=this.aim(f,e),dealt=this.attack(f,e,30*f.scale,true);if(e.health>0){e.x+=a.x*120*f.scale;e.y+=a.y*120*f.scale;this.keepInside(e);e.vx=a.x;e.vy=a.y;e.stunUntil=Math.max(e.stunUntil,this.time+1*f.scale);this.effect(e,'밀치기 · 기절!','skill')}if(dealt<=0&&e.health>0){e.x+=a.x*0;e.y+=a.y*0}}this.resolvingBlast=false;this.checkEnd()}
}
"""+anchor_skill
rep(anchor_skill,robot_skill,'robot skills')

# Run robot skills after stun check, before special movement exits.
old="if(f.egg||f.stunUntil>this.time){f.attack=0;return}\n if(f.id==='moai'){"
new="if(f.egg||f.stunUntil>this.time){f.attack=0;return}\n if(f.id==='robot')this.robotSkill(f);\n if(this.result!==null)return;\n if(f.id==='moai'){"
rep(old,new,'robot step hook')

# Robot does not perform generic contact melee.
old="'moon','invisible','moai','puffer','police'].includes(f.id)"
new="'moon','invisible','moai','puffer','police','robot'].includes(f.id)"
rep(old,new,'robot contact exclusion')

# Draw active rotating laser beam.
old="if(f.id==='knight'&&f.health>0){const a=f.knightShieldAngle||engine.time*2.8"
new="if(f.id==='robot'&&f.health>0&&f.robotLaserStart>=0&&engine.time<f.robotLaserUntil-1e-9){const duration=4/f.scale,phase=Math.max(0,Math.min(1,(engine.time-f.robotLaserStart)/duration)),la=-Math.PI/2+phase*Math.PI*2;ctx.save();ctx.globalAlpha=.85;ctx.strokeStyle='#ff4057';ctx.lineWidth=8*f.scale;ctx.shadowColor='#ff4057';ctx.shadowBlur=18;ctx.beginPath();ctx.moveTo(f.x,f.y);ctx.lineTo(f.x+Math.cos(la)*1100,f.y+Math.sin(la)*1100);ctx.stroke();ctx.restore();ctx.globalAlpha=f.id==='invisible'?.38:1;}if(f.id==='knight'&&f.health>0){const a=f.knightShieldAngle||engine.time*2.8"
rep(old,new,'robot laser draw')

p.write_text(s,encoding='utf-8')
print('NEON RUMBLE v3.19 robot patch applied')
# trigger v3.19

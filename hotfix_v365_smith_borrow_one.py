from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

old_desc="{id:'smith',name:'대장장이',icon:'⚒️',tag:'강화 · 제작무기',hp:1000,damage:10,speed:140,cooldown:.8,description:'상대에게 닿으면 망치 공격. 공격 중이 아닐 때 강화마다 공격력 +10. 강화 주기는 1초부터 매회 0.1초 감소해 최소 0.3초가 돼. 적을 맞히면 강화 주기는 다시 1초부터 시작해. 10초마다 제작무기로 선택 가능한 모든 캐릭터의 공격 투사체를 동시에 발사하며 각 투사체 피해는 현재 강화 공격력과 같아.',detail:'기본 공격력 10 · 강화 1.0초 → 최소 0.3초 · 명중 시 강화 주기 초기화 · 제작무기 10초마다 · 모든 캐릭터 공격 동시 발사 · 각 피해 = 현재 강화 공격력'},"
new_desc="{id:'smith',name:'대장장이',icon:'⚒️',tag:'강화 · 제작무기',hp:1000,damage:10,speed:140,cooldown:.8,description:'상대에게 닿으면 망치 공격. 공격 중이 아닐 때 강화마다 공격력 +10. 강화 주기는 1초부터 매회 0.1초 감소해 최소 0.3초가 돼. 적을 맞히면 강화 주기는 다시 1초부터 시작해. 10초마다 제작무기로 다른 캐릭터의 일반 공격 또는 공격 스킬 하나를 무작위로 빌려 1회 사용해. 변신·부활·소환·탑승 같은 비공격 능력은 복사하지 않아.',detail:'기본 공격력 10 · 강화 1.0초 → 최소 0.3초 · 명중 시 강화 주기 초기화 · 제작무기 10초마다 · 랜덤 공격 1회 복사 · 피해 = 현재 강화 공격력 · 변신/부활/소환/탑승 제외'},"
once(old_desc,new_desc,'smith roster text')

old_fn="""smithWeaponSkill(f,e){
 if(!f||f.id!=='smith'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0||this.time<(f.smithWeaponNext||0)-1e-9)return;
 f.smithWeaponNext=this.time+10/f.scale;
 const pool=ROSTER.filter(c=>!c.stageOnly),base=Math.atan2(e.y-f.y,e.x-f.x),count=Math.max(1,pool.length),spread=Math.min(1.35,.045*count);
 pool.forEach((c,i)=>{const off=count===1?0:(i-(count-1)/2)*(spread/(count-1)),ang=base+off,vx=Math.cos(ang),vy=Math.sin(ang);this.shots.push({x:f.x+vx*(f.radius+9),y:f.y+vy*(f.radius+9),vx,vy,owner:f.side,team:f.team,target:e.side,kind:'smith_weapon',icon:c.icon||'⚔️',radius:7*f.scale,speed:430*f.scale,damage:f.damage,life:3.5/f.scale,bounces:0})});
 f.attack=.3/f.scale;this.effect(f,'⚒️ 제작무기 · '+count+'연발!','skill');this.emit('⚒️ 대장장이 제작무기! 모든 캐릭터의 공격을 발사')
}
"""
new_fn="""smithWeaponSkill(f,e){
 if(!f||f.id!=='smith'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0||this.time<(f.smithWeaponNext||0)-1e-9)return;
 f.smithWeaponNext=this.time+10/f.scale;
 const attacks=[
  {name:'궁수의 화살',icon:'🏹',speed:480,bounces:1},
  {name:'마법사의 마법탄',icon:'🪄',speed:360,bounces:0},
  {name:'닌자의 표창',icon:'🥷',speed:520,bounces:0},
  {name:'카우보이의 총알',icon:'🔫',speed:760,bounces:0},
  {name:'눈사람의 눈송이',icon:'❄️',speed:400,bounces:0},
  {name:'경찰의 테이저',icon:'⚡',speed:520,bounces:0},
  {name:'빌런의 폭탄',icon:'💣',speed:330,bounces:0},
  {name:'달의 반달',icon:'🌜',speed:390,bounces:1},
  {name:'외계인의 레이저',icon:'👽',speed:500,bounces:3},
  {name:'탐정의 돋보기',icon:'🔎',speed:380,bounces:0},
  {name:'사랑의 하트',icon:'❤️‍🔥',speed:390,bounces:0},
  {name:'태양 투사체',icon:'☀️',speed:360,bounces:0},
  {name:'용의 신통력',icon:['💨','⚡','💧','🍃'][Math.floor(this.random()*4)],speed:390,bounces:0},
  {name:'복어의 가시',icon:'🐡',speed:420,bounces:0}
 ];
 const a=attacks[Math.floor(this.random()*attacks.length)],aim=this.aim(f,e),spawn=(ang,icon=a.icon)=>{const vx=Math.cos(ang),vy=Math.sin(ang);this.shots.push({x:f.x+vx*(f.radius+9),y:f.y+vy*(f.radius+9),vx,vy,owner:f.side,team:f.team,target:e.side,kind:'smith_weapon',icon,radius:7*f.scale,speed:a.speed*f.scale,damage:f.damage,life:3.5/f.scale,bounces:a.bounces||0})};
 const base=Math.atan2(aim.y,aim.x);
 if(a.name==='복어의 가시'){for(let i=0;i<8;i++)spawn(i*Math.PI/4,'🐡')}else spawn(base);
 f.attack=.3/f.scale;this.effect(f,'⚒️ '+a.name+' 복제!','skill');this.emit('⚒️ 제작무기: '+a.name+' 1회 사용')
}
"""
once(old_fn,new_fn,'smith weapon function')

once("<li>⚒️ 대장장이 리워크: 10초마다 제작무기로 선택 가능한 모든 캐릭터의 공격을 동시에 발사. 각 투사체 피해는 발사 순간 대장장이의 현재 강화 공격력과 동일.</li>","<li>⚒️ 대장장이 제작무기 조정: 10초마다 다른 캐릭터의 일반 공격 또는 공격 스킬 하나를 무작위로 빌려 1회 사용. 피해는 현재 강화 공격력 기준이며 변신·부활·소환·탑승 등 비공격 능력은 제외.</li>",'patch note')

p.write_text(s,encoding='utf-8')
print('v3.65 smith borrowed-one hotfix applied')

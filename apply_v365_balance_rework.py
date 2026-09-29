from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

def at_least(old,new,label,min_count=1):
    global s
    n=s.count(old)
    if n<min_count:
        raise SystemExit(f'{label}: expected >= {min_count}, got {n}')
    s=s.replace(old,new)
    return n

# Version + patch notes
once('<span class="badge">BATTLE <b>v3.64</b></span>','<span class="badge">BATTLE <b>v3.65</b></span>','version')
once('<details class="patch-notes"><summary>📒 패치노트 · v3.64</summary><div class="patch-body">', '<details class="patch-notes"><summary>📒 패치노트 · v3.65</summary><div class="patch-body"><div class="patch-version"><h3>v3.65 · 밸런스 · 대장장이 리워크 · 버그 수정</h3><ul><li>🗿 모아이 HP 1000 → 1250.</li><li>🔮 용의 여의주 HP 50 → 100.</li><li>🛸👾 감염 UFO 파멸의 레이저 주기 8초 → 7.5초. 샌드박스와 CHAPTER 4 STAGE 3 모두 적용.</li><li>⚒️ 대장장이 리워크: 10초마다 제작무기로 선택 가능한 모든 캐릭터의 공격을 동시에 발사. 각 투사체 피해는 발사 순간 대장장이의 현재 강화 공격력과 동일.</li><li>🥷 닌자 HP 650 → 670.</li><li>🦎 도마뱀 꼬리 HP 600, 이동속도 45로 느리게 계속 이동.</li><li>👨‍🚒 소방차는 HP 500, 탑승 후 최대 10초 유지. 시간 만료 또는 파괴로 하차한 순간부터 다음 탑승 쿨타임 10초 시작.</li></ul></div>', 'patch notes')

# Moai HP
once("{id:'moai',name:'모아이',icon:'🗿',tag:'점프 · 전장 충격파',hp:1000,", "{id:'moai',name:'모아이',icon:'🗿',tag:'점프 · 전장 충격파',hp:1250,", 'moai hp')

# Dragon orb HP
once("f.icon='🔮';f.hp=50;f.health=50;f.speed=80;", "f.icon='🔮';f.hp=100;f.health=100;f.speed=80;", 'dragon orb hp')

# Infected UFO 7.5 sec in sandbox + stage
once("{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1250,damage:350,speed:105,cooldown:8,unlock:'infectedUfo',description:'샌드박스에서는 8초마다 아주 두꺼운 파멸의 레이저를 예고 후 발사해. 피해 350.',detail:'HP 1250 · 파멸의 레이저 350 / 8초 · 발사 전 1초 피격 예고 · 맵 관통'},", "{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1250,damage:350,speed:105,cooldown:7.5,unlock:'infectedUfo',description:'샌드박스에서는 7.5초마다 아주 두꺼운 파멸의 레이저를 예고 후 발사해. 피해 350.',detail:'HP 1250 · 파멸의 레이저 350 / 7.5초 · 발사 전 1초 피격 예고 · 맵 관통'},", 'infected roster')
once("const doomInterval=f.doomInterval||8;", "const doomInterval=f.doomInterval||7.5;", 'infected fallback interval')
once("boss.doomInterval=8;boss.doomNext=8", "boss.doomInterval=7.5;boss.doomNext=7.5", 'infected stage interval')
once("CHAPTER 4 STAGE 3 · 감염 UFO가 8초마다 1초 피격 예고 후 두꺼운 파멸의 레이저를 발사.", "CHAPTER 4 STAGE 3 · 감염 UFO가 7.5초마다 1초 피격 예고 후 두꺼운 파멸의 레이저를 발사.", 'infected stage text')

# Ninja HP
once("{id:'ninja',name:'닌자',icon:'🥷',tag:'표창 · 독 · 베기',hp:650,", "{id:'ninja',name:'닌자',icon:'🥷',tag:'표창 · 독 · 베기',hp:670,", 'ninja hp')
once("detail:'HP 650 · 표창 10", "detail:'HP 670 · 표창 10", 'ninja detail hp')

# Smith rework text
once("{id:'smith',name:'대장장이',icon:'⚒️',tag:'시간이 힘이다',hp:1000,damage:10,speed:140,cooldown:.8,description:'상대에게 닿으면 망치 공격. 공격 중이 아닐 때 강화마다 공격력 +10. 강화 주기는 1초부터 매회 0.1초 감소해 최소 0.3초가 돼. 적을 맞히면 강화 주기는 다시 1초부터 시작해.',detail:'기본 공격력 10 · 강화 1.0초 → 최소 0.3초 · 명중 시 주기 초기화 · 공격력 유지 · 새 경기에서 초기화'},", "{id:'smith',name:'대장장이',icon:'⚒️',tag:'강화 · 제작무기',hp:1000,damage:10,speed:140,cooldown:.8,description:'상대에게 닿으면 망치 공격. 공격 중이 아닐 때 강화마다 공격력 +10. 강화 주기는 1초부터 매회 0.1초 감소해 최소 0.3초가 돼. 적을 맞히면 강화 주기는 다시 1초부터 시작해. 10초마다 제작무기로 선택 가능한 모든 캐릭터의 공격 투사체를 동시에 발사하며 각 투사체 피해는 현재 강화 공격력과 같아.',detail:'기본 공격력 10 · 강화 1.0초 → 최소 0.3초 · 명중 시 강화 주기 초기화 · 제작무기 10초마다 · 모든 캐릭터 공격 동시 발사 · 각 피해 = 현재 강화 공격력'},", 'smith roster')

# Smith timer state
once("nextCursedHand:type.id==='devileye'?13/scale:9999,sharkDashNext:", "nextCursedHand:type.id==='devileye'?13/scale:9999,smithWeaponNext:type.id==='smith'?10/scale:9999,sharkDashNext:", 'smith timer init')

# Smith weapon skill: every selectable/non-stage roster character contributes one projectile.
insert_before="""sunSkill(f,e){
"""
smith_code="""smithWeaponSkill(f,e){
 if(!f||f.id!=='smith'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0||this.time<(f.smithWeaponNext||0)-1e-9)return;
 f.smithWeaponNext=this.time+10/f.scale;
 const pool=ROSTER.filter(c=>!c.stageOnly),base=Math.atan2(e.y-f.y,e.x-f.x),count=Math.max(1,pool.length),spread=Math.min(1.35,.045*count);
 pool.forEach((c,i)=>{const off=count===1?0:(i-(count-1)/2)*(spread/(count-1)),ang=base+off,vx=Math.cos(ang),vy=Math.sin(ang);this.shots.push({x:f.x+vx*(f.radius+9),y:f.y+vy*(f.radius+9),vx,vy,owner:f.side,team:f.team,target:e.side,kind:'smith_weapon',icon:c.icon||'⚔️',radius:7*f.scale,speed:430*f.scale,damage:f.damage,life:3.5/f.scale,bounces:0})});
 f.attack=.3/f.scale;this.effect(f,'⚒️ 제작무기 · '+count+'연발!','skill');this.emit('⚒️ 대장장이 제작무기! 모든 캐릭터의 공격을 발사')
}
"""
once(insert_before,smith_code+insert_before,'insert smith skill')

# Call smith skill
once(" if(f.id==='lizard')this.lizardSkill(f)\n if(f.id==='devileye')this.devilEyeSkill(f)", " if(f.id==='lizard')this.lizardSkill(f)\n if(f.id==='smith')this.smithWeaponSkill(f,e)\n if(f.id==='devileye')this.devilEyeSkill(f)", 'call smith skill')

# Render smith weapon using source character emoji
once("if(s.kind==='sun_orb'){", "if(s.kind==='smith_weapon'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(Math.max(22,s.radius*3))+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(s.icon||'⚔️',0,0)}else if(s.kind==='sun_orb'){", 'render smith weapon')

# Lizard tail fixed HP 600 and slow movement
once("description:'일반 캐릭터보다 30% 빠르게 움직이며 근접 피해 100으로 공격해. 체력이 30% 이하가 되면 꼬리를 한 번 소환하고, 꼬리가 살아 있는 동안 모든 적 AI가 꼬리를 우선 공격해.'", "description:'일반 캐릭터보다 30% 빠르게 움직이며 근접 피해 100으로 공격해. 체력이 30% 이하가 되면 HP 600의 꼬리를 한 번 소환해. 꼬리는 느리게 계속 움직이며 살아 있는 동안 모든 적 AI가 꼬리를 우선 공격해.'", 'lizard desc')
once("detail:'HP 1000 · 이동속도 +30% · 근접 100 · HP 30% 이하 꼬리 1회 소환 · 꼬리 HP는 본체 최대 HP의 30% · 꼬리 생존 중 적 AI 우선 타깃'", "detail:'HP 1000 · 이동속도 +30% · 근접 100 · HP 30% 이하 꼬리 1회 소환 · 꼬리 HP 600 · 꼬리 이동속도 45 · 꼬리 생존 중 적 AI 우선 타깃'", 'lizard detail')
once("const side=this.fighters.length,hp=Math.max(1,Math.round(owner.hp*.3)),a=this.rand(-Math.PI,Math.PI)", "const side=this.fighters.length,hp=600*(owner.boss?2.5:1),a=this.rand(-Math.PI,Math.PI)", 'tail hp')
once("speed:0,cooldown:9999,x,y,vx:0,vy:0,attack:0,cd:9999,skill:0,turn:9999", "speed:45*owner.scale,cooldown:9999,x,y,vx:Math.cos(a),vy:Math.sin(a),attack:0,cd:9999,skill:0,turn:this.rand(.8,1.8)/owner.scale", 'tail movement init')
once(" if(f.id==='lizardtail'){f.vx=0;f.vy=0;return}", " if(f.id==='lizardtail'){f.turn=(f.turn||0)-dt;if(f.turn<=0)this.turn(f);const sp=f.speed||45;f.x+=f.vx*sp*dt;f.y+=f.vy*sp*dt;const b=this.bounds(f);if(f.x<b.low||f.x>b.high){f.x=clamp(f.x,b.low,b.high);f.vx*=-1;f.turn=this.rand(.8,1.8)/f.scale}if(f.y<b.low||f.y>b.high){f.y=clamp(f.y,b.low,b.high);f.vy*=-1;f.turn=this.rand(.8,1.8)/f.scale}return}", 'tail wandering')

# Fire truck: cooldown begins only after dismount/destruction.
once("description:'화상에 완전히 면역이야. 적이 가까이 오면 🪓 소방도끼로 피해 70을 주며 0.5초마다 휘둘러. 10초마다 HP 500의 🚒 소방차를 타고 10초 동안 물을 뿌려.'", "description:'화상에 완전히 면역이야. 적이 가까이 오면 🪓 소방도끼로 피해 70을 주며 0.5초마다 휘둘러. HP 500의 🚒 소방차를 최대 10초 동안 타고 물을 뿌리며, 하차한 뒤부터 다음 탑승까지 10초 쿨타임이 시작돼.'", 'firefighter desc')
once("detail:'HP 1000 · 화상 면역 · 🪓 70 / 0.5초 · 🚒 10초마다 탑승 · 소방차 HP 500 · 유지 10초 · 💧 피해 10 / 0.3초 · 화상 아군 우선 치료 + HP 10'", "detail:'HP 1000 · 화상 면역 · 🪓 70 / 0.5초 · 🚒 HP 500 · 최대 유지 10초 · 하차 후 쿨타임 10초 · 💧 피해 10 / 0.3초 · 화상 아군 우선 치료 + HP 10'", 'firefighter detail')
once("if(f.firetruckMounted&&(this.time>=f.firetruckUntil-1e-9||f.firetruckHp<=0)){f.firetruckMounted=false;f.firetruckUntil=0;f.icon='👨‍🚒';this.effect(f,'🚒 하차','skill')}", "if(f.firetruckMounted&&(this.time>=f.firetruckUntil-1e-9||f.firetruckHp<=0)){f.firetruckMounted=false;f.firetruckUntil=0;f.firetruckNext=this.time+10/f.scale;f.icon='👨‍🚒';this.effect(f,'🚒 하차 · 쿨타임 10초','skill')}", 'firetruck timed dismount cooldown')
once("f.firetruckUntil=this.time+10/f.scale;f.firetruckNext=this.time+10/f.scale;f.firefighterWaterNext=this.time;", "f.firetruckUntil=this.time+10/f.scale;f.firetruckNext=Infinity;f.firefighterWaterNext=this.time;", 'firetruck mount no cooldown yet')
once("if(e.firetruckHp<=0){e.firetruckMounted=false;e.firetruckUntil=0;e.icon='👨‍🚒';this.effect(e,'🚒 소방차 파괴!','skill');", "if(e.firetruckHp<=0){e.firetruckMounted=false;e.firetruckUntil=0;e.firetruckNext=this.time+10/e.scale;e.icon='👨‍🚒';this.effect(e,'🚒 소방차 파괴 · 쿨타임 10초!','skill');", 'firetruck destroyed cooldown')

p.write_text(s,encoding='utf-8')
print('v3.65 patch applied')

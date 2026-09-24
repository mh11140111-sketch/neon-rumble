from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if s.count(old)<count:
        raise SystemExit(f'PATCH FAILED: {label}')
    s=s.replace(old,new,count)

# Version + patch notes
rep('BATTLE <b>v3.21</b>','BATTLE <b>v3.22</b>','version badge')
rep('📒 패치노트 · v3.21','📒 패치노트 · v3.22','patch summary')
anchor='<div class="patch-body"><div class="patch-version"><h3>v3.21 · 지니 회전팔 & AI 개선</h3>'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.22 · 편의성 & 달 귀환타</h3><ul><li>전투 시작 버튼을 캐릭터 선택 영역 위쪽으로 이동해 바로 시작하기 쉽게 개선.</li><li>달의 관통 반달 조각은 전진 중 대상별 1회 피해를 주고, 귀환할 때 같은 대상을 다시 관통하면 추가 1회 피해 가능.</li></ul></div><div class="patch-version"><h3>v3.21 · 지니 회전팔 & AI 개선</h3>'
rep(anchor,insert,'patch notes')

# Moon roster text
rep("description:'2초마다 🌜 반달 조각을 던져 피해 80. 반달 조각은 적을 관통하고 맵 끝에 닿으면 돌아와. 전투가 45초를 넘기면 궁극기를 준비해.',detail:'관통 반달 80 · 쿨타임 2초 · 45초 후 궁극기 · 5초 예고 뒤 전장 전체 즉사 · 무적 무시 · 팀 구분 없음'",
    "description:'2초마다 🌜 반달 조각을 던져 피해 80. 반달 조각은 적을 관통하고 맵 끝에 닿으면 돌아오며, 돌아오는 길에도 같은 적을 다시 맞힐 수 있어. 전투가 45초를 넘기면 궁극기를 준비해.',detail:'관통 반달 80 · 전진 1회 + 귀환 1회 재타격 가능 · 쿨타임 2초 · 45초 후 궁극기 · 5초 예고 뒤 전장 전체 즉사 · 무적 무시 · 팀 구분 없음'",
    'moon roster')

# Move play/start button from bottom of selector to immediately below versus cards.
start_btn='<button class="primary start" id="start" type="button" disabled>이 조합으로 전투 시작</button>'
rep(start_btn+'<p class="hint">일반 모드는 직접 조작 없는 자동 전투 · 조정 모드에서만 왼쪽 캐릭터 이동 가능 · 체력 0이 되면 패배.</p></section>',
    '<p class="hint">일반 모드는 직접 조작 없는 자동 전투 · 조정 모드에서만 왼쪽 캐릭터 이동 가능 · 체력 0이 되면 패배.</p></section>',
    'remove old start button')
versus_end='<div class="versus"><button class="chosen left" id="choose0" type="button" aria-pressed="true"><span class="side"><span id="label0">왼쪽 선수</span> <b>선택 중</b></span><span class="chosen-icon" id="icon0">🥊</span><strong id="name0">복서</strong><span id="tag0">반사 · 돌진</span></button><span class="vs">VS</span><button class="chosen right" id="choose1" type="button" aria-pressed="false"><span class="side"><span id="label1">오른쪽 선수</span> <b>변경</b></span><span class="chosen-icon" id="icon1">⚒️</span><strong id="name1">대장장이</strong><span id="tag1">시간이 힘이다</span></button></div>'
rep(versus_end,versus_end+'\n'+start_btn,'move start button up')

# Moon: separate hit registry for outbound and return. Reset once the boomerang turns around.
old="""if(s.kind==='moon'){if(s.returning){const a=this.aim(s,f);s.vx=a.x;s.vy=a.y;s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;if(distance(s,f)<=f.radius+s.radius+7){s.life=0;f.moonShot=null;f.moonHalf=false;f.icon='🌝';this.effect(f,'보름달 복귀','skill');continue}}else{s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;const blocker=this.enemies(f).find(v=>v.id==='knight'&&this.knightBlocksProjectile(v,s));if(blocker){this.blockProjectileWithKnight(blocker,s,f);s.returning=true;continue}for(const e of this.enemies(f)){if(s.hitTargets[e.side])continue;if(distance(s,e)<e.radius+s.radius){this.attackProjectile(f,e,s);s.hitTargets[e.side]=true;if(this.result!==null)break}}if(s.x<22||s.x>698||s.y<22||s.y>698)s.returning=true}continue}"""
new="""if(s.kind==='moon'){if(s.returning){const a=this.aim(s,f);s.vx=a.x;s.vy=a.y;s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;const blocker=this.enemies(f).find(v=>v.id==='knight'&&this.knightBlocksProjectile(v,s));if(blocker){this.blockProjectileWithKnight(blocker,s,f);continue}for(const e of this.enemies(f)){if(s.hitTargets[e.side])continue;if(distance(s,e)<e.radius+s.radius){this.attackProjectile(f,e,s);s.hitTargets[e.side]=true;if(this.result!==null)break}}if(distance(s,f)<=f.radius+s.radius+7){s.life=0;f.moonShot=null;f.moonHalf=false;f.icon='🌝';this.effect(f,'보름달 복귀','skill');continue}}else{s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;const blocker=this.enemies(f).find(v=>v.id==='knight'&&this.knightBlocksProjectile(v,s));if(blocker){this.blockProjectileWithKnight(blocker,s,f);continue}for(const e of this.enemies(f)){if(s.hitTargets[e.side])continue;if(distance(s,e)<e.radius+s.radius){this.attackProjectile(f,e,s);s.hitTargets[e.side]=true;if(this.result!==null)break}}if(s.x<22||s.x>698||s.y<22||s.y>698){s.returning=true;s.hitTargets={}}}continue}"""
rep(old,new,'moon return damage')

p.write_text(s,encoding='utf-8')
print('NEON RUMBLE v3.22 applied')

from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(f'PATCH FAILED: {label}')
    s=s.replace(old,new,count)

# Version + patch notes
rep('BATTLE <b>v3.17</b>','BATTLE <b>v3.18</b>','version badge')
rep('📒 패치노트 · v3.17','📒 패치노트 · v3.18','patch summary')
anchor='<div class="patch-body"><div class="patch-version"><h3>v3.17 · 누적 방패 & 경찰</h3>'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.18 · 조정 모드</h3><ul><li>새 모드 조정 모드 추가: 1대1 전투에서 왼쪽 캐릭터의 이동을 직접 조정 가능.</li><li>모바일에서는 왼쪽 아래 가상 엄지스틱으로 이동. 공격과 고유 스킬은 기존 캐릭터 메커니즘을 유지.</li><li>조정 기능은 조정 모드에서만 작동하며 일반 1대1·보스전·릴레이·단체전에는 절대 적용되지 않음.</li></ul></div><div class="patch-version"><h3>v3.17 · 누적 방패 & 경찰</h3>'
rep(anchor,insert,'patch insert')

css_anchor='.character-search:focus{outline:3px solid #c5f794;outline-offset:2px}\n'
css_add=""".character-search:focus{outline:3px solid #c5f794;outline-offset:2px}\n.control-stick{position:absolute;left:18px;bottom:18px;width:128px;height:128px;border-radius:50%;background:#0b1525aa;border:2px solid #8fb4df66;z-index:4;touch-action:none;user-select:none;-webkit-user-select:none}.control-stick::before{content:'';position:absolute;inset:22px;border-radius:50%;border:1px solid #9fc3e555}.control-knob{position:absolute;left:50%;top:50%;width:54px;height:54px;transform:translate(-50%,-50%);border-radius:50%;background:#d8ebffdd;border:2px solid #fff;box-shadow:0 3px 12px #0008;pointer-events:none}.control-label{position:absolute;left:18px;bottom:152px;z-index:4;font-size:12px;font-weight:800;color:#d8ebff;background:#0a101bcc;border:1px solid #4c6688;border-radius:8px;padding:5px 8px;pointer-events:none}.control-stick[hidden],.control-label[hidden]{display:none!important}@media(max-width:560px){.control-stick{width:112px;height:112px;left:14px;bottom:14px}.control-knob{width:48px;height:48px}.control-label{left:14px;bottom:134px}}\n"""
rep(css_anchor,css_add,'joystick css')

old_modes='<button id="mode-relay" type="button" aria-pressed="false">릴레이 · 3대3</button><button id="mode-group" type="button" aria-pressed="false">단체전 · 3대3</button>'
new_modes='<button id="mode-relay" type="button" aria-pressed="false">릴레이 · 3대3</button><button id="mode-group" type="button" aria-pressed="false">단체전 · 3대3</button><button id="mode-control" type="button" aria-pressed="false">🎮 조정 모드</button>'
rep(old_modes,new_modes,'control mode button')

old_arena='<div class="arena"><canvas id="arena" width="720" height="720" aria-label="자동 전투 경기장"></canvas><div id="result" class="result" hidden>'
new_arena='<div class="arena"><canvas id="arena" width="720" height="720" aria-label="전투 경기장"></canvas><div id="control-label" class="control-label" hidden>왼쪽 캐릭터 이동</div><div id="control-stick" class="control-stick" hidden aria-label="이동 엄지스틱"><div id="control-knob" class="control-knob"></div></div><div id="result" class="result" hidden>'
rep(old_arena,new_arena,'joystick html')

old="$('choose0').classList.toggle('boss-choice',mode==='boss');$('squad-picker').hidden=mode!=='boss';$('boss-rules').hidden=mode!=='boss';$('mode-duel').setAttribute('aria-pressed',String(mode==='duel'));$('mode-boss').setAttribute('aria-pressed',String(mode==='boss'));"
new="$('choose0').classList.toggle('boss-choice',mode==='boss');$('squad-picker').hidden=mode!=='boss';$('boss-rules').hidden=mode!=='boss';$('mode-duel').setAttribute('aria-pressed',String(mode==='duel'));$('mode-boss').setAttribute('aria-pressed',String(mode==='boss'));$('mode-control').setAttribute('aria-pressed',String(mode==='control'));"
rep(old,new,'control pressed state')
old_start="$('start').textContent=mode==='group'?'단체전 시작 · 3 vs 3 동시전투':mode==='relay'?'릴레이 전투 시작 · 팀당 3명':mode==='boss'?'보스전 시작 · 1 vs 5':'이 조합으로 전투 시작';"
new_start="$('start').textContent=mode==='group'?'단체전 시작 · 3 vs 3 동시전투':mode==='relay'?'릴레이 전투 시작 · 팀당 3명':mode==='boss'?'보스전 시작 · 1 vs 5':mode==='control'?'조정 모드 시작 · 왼쪽 직접 이동':'이 조합으로 전투 시작';"
rep(old_start,new_start,'start text')

old_click="$('mode-relay').onclick=()=>{mode='relay';side=0;updateSelection()};$('mode-group').onclick=()=>{mode='group';side=0;updateSelection()};"
new_click="$('mode-relay').onclick=()=>{mode='relay';side=0;updateSelection()};$('mode-group').onclick=()=>{mode='group';side=0;updateSelection()};$('mode-control').onclick=()=>{mode='control';side=0;bossSlot=-1;updateSelection()};"
rep(old_click,new_click,'control click')

old_move="if(f.dash<=0){if(f.turn<=0)this.turn(f);if(['knight','vampire','smith'].includes(f.id)){const a=this.aim(f,e),k=(f.id==='smith'?.65:1.8)*f.scale;const x=f.vx+a.x*k*dt,y=f.vy+a.y*k*dt,n=Math.hypot(x,y)||1;f.vx=x/n;f.vy=y/n}}\n const prey=f.captureTarget!==null?this.fighters[f.captureTarget]:null;if(prey){const aim=this.aim(f,prey);f.vx=aim.x;f.vy=aim.y}\n if(f.id==='hero'&&f.heroReady){"
new_move="const manual=this.mode==='control'&&f.team===0;if(manual){f.vx=Number(this.controlX)||0;f.vy=Number(this.controlY)||0;f.turn=1}else if(f.dash<=0){if(f.turn<=0)this.turn(f);if(['knight','vampire','smith'].includes(f.id)){const a=this.aim(f,e),k=(f.id==='smith'?.65:1.8)*f.scale;const x=f.vx+a.x*k*dt,y=f.vy+a.y*k*dt,n=Math.hypot(x,y)||1;f.vx=x/n;f.vy=y/n}}\n const prey=f.captureTarget!==null?this.fighters[f.captureTarget]:null;if(prey&&!manual){const aim=this.aim(f,prey);f.vx=aim.x;f.vy=aim.y}\n if(!manual&&f.id==='hero'&&f.heroReady){"
rep(old_move,new_move,'manual movement')

old_engine="engine=mode==='group'?new Engine(relayTeams[0][0],relayTeams[1][0],Math.random,{mode:'group',teams:relayTeams}):mode==='relay'?new Engine(relayTeams[0][0],relayTeams[1][0],Math.random,{mode:'relay',teams:relayTeams}):mode==='boss'?new Engine(bossChoice,squad[0],Math.random,{mode:'boss',allies:squad}):new Engine(...selected);"
new_engine="engine=mode==='group'?new Engine(relayTeams[0][0],relayTeams[1][0],Math.random,{mode:'group',teams:relayTeams}):mode==='relay'?new Engine(relayTeams[0][0],relayTeams[1][0],Math.random,{mode:'relay',teams:relayTeams}):mode==='boss'?new Engine(bossChoice,squad[0],Math.random,{mode:'boss',allies:squad}):mode==='control'?new Engine(selected[0],selected[1],Math.random,{mode:'control'}):new Engine(...selected);"
rep(old_engine,new_engine,'control engine')
old_event="$('event').textContent=mode==='group'?'단체전 시작! 양 팀 3명이 동시에 전투해.':mode==='boss'?'보스전 시작! 도전자 5명이 동시에 전투해.':'전투 시작!';"
new_event="$('event').textContent=mode==='group'?'단체전 시작! 양 팀 3명이 동시에 전투해.':mode==='boss'?'보스전 시작! 도전자 5명이 동시에 전투해.':mode==='control'?'조정 모드 시작! 왼쪽 엄지스틱으로 이동해.':'전투 시작!';$('control-stick').hidden=mode!=='control';$('control-label').hidden=mode!=='control';resetStick();"
rep(old_event,new_event,'control start ui')
old_bmode="$('battle-mode').textContent=mode==='group'?'GROUP 3V3':mode==='relay'?'RELAY':mode==='boss'?'BOSS RAID':'DUEL';"
new_bmode="$('battle-mode').textContent=mode==='group'?'GROUP 3V3':mode==='relay'?'RELAY':mode==='boss'?'BOSS RAID':mode==='control'?'CONTROL':'DUEL';"
rep(old_bmode,new_bmode,'battle mode label')
old_sel="function selection(){engine=null;paused=false;acc=0;$('battle').hidden=true;$('selection').hidden=false;updateSelection();window.scrollTo({top:0,behavior:'auto'})}"
new_sel="function selection(){engine=null;paused=false;acc=0;resetStick();$('control-stick').hidden=true;$('control-label').hidden=true;$('battle').hidden=true;$('selection').hidden=false;updateSelection();window.scrollTo({top:0,behavior:'auto'})}"
rep(old_sel,new_sel,'selection hide joystick')

anchor_js="const canvas=$('arena'),ctx=canvas.getContext('2d');"
joystick_js="""const canvas=$('arena'),ctx=canvas.getContext('2d');let stickX=0,stickY=0,stickPointer=null;const stick=$('control-stick'),knob=$('control-knob');
function resetStick(){stickX=0;stickY=0;stickPointer=null;if(knob)knob.style.transform='translate(-50%,-50%)'}
function moveStick(ev){if(mode!=='control'||!stick||stick.hidden)return;const r=stick.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2,max=r.width*.32;let dx=ev.clientX-cx,dy=ev.clientY-cy,d=Math.hypot(dx,dy);if(d>max){dx*=max/d;dy*=max/d;d=max}stickX=dx/max;stickY=dy/max;knob.style.transform='translate(calc(-50% + '+dx+'px),calc(-50% + '+dy+'px))'}
stick.addEventListener('pointerdown',e=>{if(mode!=='control')return;stickPointer=e.pointerId;stick.setPointerCapture(e.pointerId);moveStick(e);e.preventDefault()});stick.addEventListener('pointermove',e=>{if(e.pointerId===stickPointer){moveStick(e);e.preventDefault()}});const releaseStick=e=>{if(stickPointer===null||e.pointerId===stickPointer){resetStick();e.preventDefault()}};stick.addEventListener('pointerup',releaseStick);stick.addEventListener('pointercancel',releaseStick);"""
rep(anchor_js,joystick_js,'joystick js')

old_loop="if(engine&&!paused&&engine.result===null){acc+=dt*speed;while(acc>=1/120&&engine.result===null){engine.step(1/120);acc-=1/120}hud()}"
new_loop="if(engine&&!paused&&engine.result===null){if(mode==='control'){engine.controlX=stickX;engine.controlY=stickY}else{engine.controlX=0;engine.controlY=0}acc+=dt*speed;while(acc>=1/120&&engine.result===null){engine.step(1/120);acc-=1/120}hud()}"
rep(old_loop,new_loop,'loop control input')

old_hint='<button class="primary start" id="start" type="button" disabled>이 조합으로 전투 시작</button><p class="hint">직접 조작 없이 자동 전투 · 체력 0이 되면 패배 · 수치는 초기 테스트 기준이야.</p>'
new_hint='<button class="primary start" id="start" type="button" disabled>이 조합으로 전투 시작</button><p class="hint">일반 모드는 직접 조작 없는 자동 전투 · 조정 모드에서만 왼쪽 캐릭터 이동 가능 · 체력 0이 되면 패배.</p>'
rep(old_hint,new_hint,'hint')

p.write_text(s,encoding='utf-8')
print('v3.18 control mode patch applied')
# trigger workflow

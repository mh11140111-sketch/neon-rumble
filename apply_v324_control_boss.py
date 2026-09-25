from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if s.count(old)<count:
        raise SystemExit(f'PATCH FAILED: {label}')
    s=s.replace(old,new,count)

# Keep v3.24. Extend current v3.24 notes only.
rep('<li>STAGE 3: 체력과 공격력이 1.5배인 빌런을 혼자 처치.</li></ul>',
    '<li>STAGE 3: 체력과 공격력이 1.5배인 빌런을 혼자 처치.</li><li>STAGE 2 클리어 보상: 🎮 조정 보스전 해금. 해금 상태는 브라우저에 저장되며 보스와 도전자 5명을 직접 선택 가능.</li></ul>',
    'v324 controlled boss note')

# Controlled boss entry directly under Stage Mode entry.
rep('<button id="stage-entry" class="stage-entry" type="button">🧪 스테이지 모드 · 테스트버전</button>\n<div id="stage-panel"',
    '<button id="stage-entry" class="stage-entry" type="button">🧪 스테이지 모드 · 테스트버전</button>\n<button id="boss-control-entry" class="stage-entry boss-control-entry" type="button" disabled>🔒 조정 보스전 · STAGE 2 클리어 시 해금</button>\n<div id="stage-panel"',
    'controlled boss entry')
rep('.stage-entry{width:100%;margin:18px 0 8px;background:#18263a;border:1px solid #5e7695;font-weight:800}',
    '.stage-entry{width:100%;margin:18px 0 8px;background:#18263a;border:1px solid #5e7695;font-weight:800}.boss-control-entry{margin-top:8px}',
    'controlled boss css')

# Work only in front-end controller script for mode expansion.
marker="const {Engine,ROSTER}=window.DuelEngine"
if marker not in s:
    raise SystemExit('PATCH FAILED: frontend marker')
head,ui=s.split(marker,1)

# Standalone frontend boss checks become boss family. Avoid object/property .mode checks.
ui=re.sub(r"(?<![\w.])mode==='boss'", "isBossMode()", ui)
ui=re.sub(r"(?<![\w.])mode!=='boss'", "!isBossMode()", ui)

# Add persistent unlock state and helper.
anchor="function resetStick(){stickX=0;stickY=0;stickPointer=null;if(knob)knob.style.transform='translate(-50%,-50%)'}"
helpers="""const CONTROL_BOSS_KEY='neonRumble.controlBossUnlocked.v1';
let controlBossUnlocked=false;try{controlBossUnlocked=localStorage.getItem(CONTROL_BOSS_KEY)==='1'}catch{}
function isBossMode(){return mode==='boss'||mode==='boss-control'}
function updateControlBossUnlockUI(){const b=$('boss-control-entry');if(!b)return;b.disabled=!controlBossUnlocked;b.textContent=controlBossUnlocked?'🎮 조정 보스전 · 해금됨':'🔒 조정 보스전 · STAGE 2 클리어 시 해금'}
function unlockControlBoss(){if(controlBossUnlocked)return false;controlBossUnlocked=true;try{localStorage.setItem(CONTROL_BOSS_KEY,'1')}catch{}updateControlBossUnlockUI();return true}
"""+anchor
if anchor not in ui:
    raise SystemExit('PATCH FAILED: unlock helper anchor')
ui=ui.replace(anchor,helpers,1)

# Thumbstick supports controlled boss too.
ui=ui.replace("if(!['control','stage'].includes(mode)||!stick||stick.hidden)return;", "if(!['control','stage','boss-control'].includes(mode)||!stick||stick.hidden)return;",1)
ui=ui.replace("if(!['control','stage'].includes(mode))return;", "if(!['control','stage','boss-control'].includes(mode))return;",1)

# Stage UI hides both sub-mode entry buttons while browsing stages, restores them elsewhere.
ui=ui.replace("$('stage-entry').hidden=on;$('stage-panel').hidden=!on;", "$('stage-entry').hidden=on;$('boss-control-entry').hidden=on;$('stage-panel').hidden=!on;",1)
ui=ui.replace("$('mode-control').setAttribute('aria-pressed',String(mode==='control'))}", "$('mode-control').setAttribute('aria-pressed',String(mode==='control'));updateControlBossUnlockUI()}",1)
ui=ui.replace("$('stage-entry').hidden=false}", "$('stage-entry').hidden=false;$('boss-control-entry').hidden=false}",1)

# Controlled boss entry handler.
entry_handler="$('stage-entry').onclick=()=>{mode='stage';stageNo=1;updateSelection();window.scrollTo({top:0,behavior:'auto'})};"
if entry_handler not in ui:
    raise SystemExit('PATCH FAILED: stage entry handler')
ui=ui.replace(entry_handler,entry_handler+"\n$('boss-control-entry').onclick=()=>{if(!controlBossUnlocked)return;mode='boss-control';bossSlot=-1;side=0;updateSelection();window.scrollTo({top:0,behavior:'auto'})};",1)

# Normal start(): boss-control uses boss engine + manual team 0.
start_tail=":new Engine(...selected);paused=false;acc=0;last=performance.now();"
if start_tail not in ui:
    raise SystemExit('PATCH FAILED: normal start tail')
ui=ui.replace(start_tail,":new Engine(...selected);if(mode==='boss-control')engine.manualTeam0=true;paused=false;acc=0;last=performance.now();",1)

# Controlled boss gets stick, labels, specific battle title/event.
ui=ui.replace("$('control-stick').hidden=mode!=='control';$('control-label').hidden=mode!=='control';resetStick();",
              "$('control-stick').hidden=!['control','boss-control'].includes(mode);$('control-label').hidden=!['control','boss-control'].includes(mode);$('control-label').textContent=mode==='boss-control'?'보스 직접 이동':'왼쪽 캐릭터 이동';resetStick();",1)
ui=ui.replace("$('event').textContent=mode==='group'?'단체전 시작! 양 팀 3명이 동시에 전투해.':isBossMode()?'보스전 시작! 도전자 5명이 동시에 전투해.':mode==='control'?'조정 모드 시작! 왼쪽 엄지스틱으로 이동해.':'전투 시작!';",
              "$('event').textContent=mode==='group'?'단체전 시작! 양 팀 3명이 동시에 전투해.':mode==='boss-control'?'조정 보스전 시작! 보스를 엄지스틱으로 직접 이동해.':isBossMode()?'보스전 시작! 도전자 5명이 동시에 전투해.':mode==='control'?'조정 모드 시작! 왼쪽 엄지스틱으로 이동해.':'전투 시작!';",1)
ui=ui.replace("$('battle-mode').textContent=mode==='group'?'GROUP 3V3':mode==='relay'?'RELAY':isBossMode()?'BOSS RAID':mode==='control'?'CONTROL':'DUEL';",
              "$('battle-mode').textContent=mode==='group'?'GROUP 3V3':mode==='relay'?'RELAY':mode==='boss-control'?'CONTROL BOSS':isBossMode()?'BOSS RAID':mode==='control'?'CONTROL':'DUEL';",1)

# Joystick data is fed to engine during controlled boss play.
ui=ui.replace("if(mode==='control'||mode==='stage'){engine.controlX=stickX;engine.controlY=stickY}else", "if(mode==='control'||mode==='stage'||mode==='boss-control'){engine.controlX=stickX;engine.controlY=stickY}else",1)

# Stage 2 clear unlocks controlled boss and persists it.
old_stage_result="if(mode==='stage'){$('winner-icon').textContent='🏁';$('winner').textContent='STAGE '+stageNo+' 클리어!';$('summary').textContent=t+'초 · 로봇 생존 · 다음 스테이지도 테스트해 봐.'}"
new_stage_result="if(mode==='stage'){const unlockedNow=stageNo===2?unlockControlBoss():false;$('winner-icon').textContent='🏁';$('winner').textContent='STAGE '+stageNo+' 클리어!';$('summary').textContent=t+'초 · 로봇 생존 · 다음 스테이지도 테스트해 봐.'+(unlockedNow?' · 🎮 조정 보스전 해금!':'')}"
if old_stage_result not in ui:
    raise SystemExit('PATCH FAILED: stage clear result')
ui=ui.replace(old_stage_result,new_stage_result,1)

# Initialize lock/unlock label immediately on boot.
ui=ui.replace("updateSelection();$('boot').hidden=true;", "updateControlBossUnlockUI();updateSelection();$('boot').hidden=true;",1)

s=head+marker+ui
p.write_text(s,encoding='utf-8')
print('v3.24 controlled boss unlock applied')

from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(label+' anchor missing')
    s=s.replace(old,new,count)

# Version + patch notes
rep('BATTLE <b>v3.51</b>','BATTLE <b>v3.52</b>','version')
rep('📒 패치노트 · v3.51','📒 패치노트 · v3.52','patch title')
marker='<div class="patch-body">'
patch='''<div class="patch-version"><h3>v3.52 · 꽃게 밸런스 & 자유 엄지스틱</h3><ul><li>🦀 꽃게: 탈피 후 5초 동안 받는 피해 배율 ×10 → ×3. 탈피 주기는 10초 그대로 유지.</li><li>🎮 엄지스틱: 조정 가능한 전투에서 경기장 어디를 눌러도 이동 조작을 시작할 수 있도록 개선.</li><li>⚙️ 설정: 엄지스틱 왼쪽/오른쪽 위치 설정을 제거하고, 엄지스틱 고정 / 고정 해제 옵션 추가.</li><li>📌 고정 해제 시 누른 위치로 스틱이 이동하고, 고정 시 스틱 위치는 움직이지 않은 채 어느 곳에서든 방향 조작 가능.</li></ul></div>'''
if patch not in s:
    rep(marker,marker+patch,'patch notes')

# Crab vulnerability x10 -> x3, keep duration 5 sec and molt cadence 10 sec.
rep("탈피 후 5초 동안 받는 피해 ×10","탈피 후 5초 동안 받는 피해 ×3",'crab description')
rep("탈피 후 5초간 받는 피해 ×10","탈피 후 5초간 받는 피해 ×3",'crab detail')
rep("this.effect(f,'🦀 탈피! 집게 +30 · 피해 ×10','doom')","this.effect(f,'🦀 탈피! 집게 +30 · 피해 ×3','doom')",'crab effect')
rep("this.emit('🦀 꽃게가 탈피! 껍질 HP 200 · 5초간 받는 피해 10배')","this.emit('🦀 꽃게가 탈피! 껍질 HP 200 · 5초간 받는 피해 3배')",'crab emit')
rep("if(e&&e.id==='crab'&&(e.crabVulnerableUntil||0)>this.time)dmg*=10;","if(e&&e.id==='crab'&&(e.crabVulnerableUntil||0)>this.time)dmg*=3;",'crab standard damage')
rep("(e.id==='crab'&&(e.crabVulnerableUntil||0)>this.time?10:1)","(e.id==='crab'&&(e.crabVulnerableUntil||0)>this.time?3:1)",'crab burn damage')
# Keep exact timing split.
if "f.crabVulnerableUntil=this.time+5/f.scale;f.crabMoltNext=this.time+10/f.scale" not in s:
    raise SystemExit('crab 5s vulnerability / 10s molt split missing')

# Settings HTML: position -> lock.
old_html='<label class="setting-item">엄지스틱 위치<select id="setting-stick-position"><option value="left">왼쪽</option><option value="right">오른쪽</option></select></label>'
new_html='<label class="setting-item">엄지스틱<select id="setting-stick-lock"><option value="off">고정 해제</option><option value="on">고정</option></select></label>'
rep(old_html,new_html,'stick setting html')
rep('키보드 조작은 조정 모드·스테이지 모드·조정 보스전에서만 작동해. 모바일에서는 엄지스틱을 권장해.','키보드 조작은 조정 모드·스테이지 모드·조정 보스전에서만 작동해. 엄지스틱 고정 해제 시 경기장 어디를 눌러도 그 위치에서 조작할 수 있어.','settings note')

# Settings state migration. Default = unlocked so anywhere-touch behavior is immediately available.
old_settings="let settings={control:'stick',stickPosition:'left',sound:true};try{const saved=JSON.parse(localStorage.getItem(SETTINGS_KEY)||'null');if(saved&&typeof saved==='object')settings={...settings,...saved}}catch{};if(!['stick','wasd','arrows'].includes(settings.control))settings.control='stick';if(!['left','right'].includes(settings.stickPosition))settings.stickPosition='left';settings.sound=settings.sound!==false;"
new_settings="let settings={control:'stick',stickLocked:false,sound:true};try{const saved=JSON.parse(localStorage.getItem(SETTINGS_KEY)||'null');if(saved&&typeof saved==='object')settings={...settings,...saved}}catch{};if(!['stick','wasd','arrows'].includes(settings.control))settings.control='stick';settings.stickLocked=settings.stickLocked===true;delete settings.stickPosition;settings.sound=settings.sound!==false;"
rep(old_settings,new_settings,'settings state')

# Add arena wrapper reference for pointer capture / floating positioning.
old_refs="const canvas=$('arena'),ctx=canvas.getContext('2d');let stickX=0,stickY=0,stickPointer=null;const stick=$('control-stick'),knob=$('control-knob'),controlLabel=$('control-label');const keys=new Set();"
new_refs="const canvas=$('arena'),ctx=canvas.getContext('2d'),arenaEl=canvas.parentElement;let stickX=0,stickY=0,stickPointer=null;const stick=$('control-stick'),knob=$('control-knob'),controlLabel=$('control-label');const keys=new Set();"
rep(old_refs,new_refs,'arena ref')

# Control UI no longer has left/right side behavior.
old_refresh="function refreshControlUI(){const manual=isManualMode()&&!!engine,useStick=settings.control==='stick';if(stick){stick.hidden=!(manual&&useStick);stick.classList.toggle('stick-right',settings.stickPosition==='right')}if(controlLabel){controlLabel.hidden=!manual;controlLabel.classList.toggle('stick-right',useStick&&settings.stickPosition==='right');controlLabel.textContent=mode==='boss-control'?'보스 이동 · '+controlName():mode==='stage'?'로봇 이동 · '+controlName():mode==='mansion'?'흡혈귀 이동 · '+controlName():'왼쪽 캐릭터 이동 · '+controlName()}if($('setting-stick-position'))$('setting-stick-position').disabled=!useStick}"
new_refresh="function refreshControlUI(){const manual=isManualMode()&&!!engine,useStick=settings.control==='stick';if(stick){stick.hidden=!(manual&&useStick);stick.classList.remove('stick-right');if(settings.stickLocked)resetStickBase()}if(controlLabel){controlLabel.hidden=!manual;controlLabel.classList.remove('stick-right');controlLabel.textContent=mode==='boss-control'?'보스 이동 · '+controlName():mode==='stage'?'로봇 이동 · '+controlName():mode==='mansion'?'흡혈귀 이동 · '+controlName():'왼쪽 캐릭터 이동 · '+controlName()}if($('setting-stick-lock'))$('setting-stick-lock').disabled=!useStick}"
rep(old_refresh,new_refresh,'refresh controls')
old_apply="function applySettingsUI(){if($('setting-control'))$('setting-control').value=settings.control;if($('setting-stick-position'))$('setting-stick-position').value=settings.stickPosition;updateSoundButtons();refreshControlUI()}"
new_apply="function applySettingsUI(){if($('setting-control'))$('setting-control').value=settings.control;if($('setting-stick-lock'))$('setting-stick-lock').value=settings.stickLocked?'on':'off';updateSoundButtons();refreshControlUI()}"
rep(old_apply,new_apply,'apply settings ui')

# Replace joystick event system: entire arena becomes the input surface.
old_stick="""function resetStick(){stickX=0;stickY=0;stickPointer=null;if(knob)knob.style.transform='translate(-50%,-50%)'}
function moveStick(ev){if(!isManualMode()||settings.control!=='stick'||!stick||stick.hidden)return;const r=stick.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2,max=r.width*.32;let dx=ev.clientX-cx,dy=ev.clientY-cy,d=Math.hypot(dx,dy);if(d>max){dx*=max/d;dy*=max/d;d=max}stickX=dx/max;stickY=dy/max;knob.style.transform='translate(calc(-50% + '+dx+'px),calc(-50% + '+dy+'px))'}
stick.addEventListener('pointerdown',e=>{if(!isManualMode()||settings.control!=='stick')return;stickPointer=e.pointerId;stick.setPointerCapture(e.pointerId);moveStick(e);e.preventDefault()});stick.addEventListener('pointermove',e=>{if(e.pointerId===stickPointer){moveStick(e);e.preventDefault()}});const releaseStick=e=>{if(stickPointer===null||e.pointerId===stickPointer){resetStick();e.preventDefault()}};stick.addEventListener('pointerup',releaseStick);stick.addEventListener('pointercancel',releaseStick);"""
new_stick="""function resetStick(){stickX=0;stickY=0;stickPointer=null;if(knob)knob.style.transform='translate(-50%,-50%)'}
function resetStickBase(){if(!stick)return;stick.style.left='';stick.style.top='';stick.style.right='';stick.style.bottom=''}
function placeStickAt(ev){if(!stick||!arenaEl||settings.stickLocked)return;const ar=arenaEl.getBoundingClientRect(),sr=stick.getBoundingClientRect(),w=sr.width||112,h=sr.height||112,pad=6,cx=Math.max(w/2+pad,Math.min(ar.width-w/2-pad,ev.clientX-ar.left)),cy=Math.max(h/2+pad,Math.min(ar.height-h/2-pad,ev.clientY-ar.top));stick.style.left=(cx-w/2)+'px';stick.style.top=(cy-h/2)+'px';stick.style.right='auto';stick.style.bottom='auto'}
function moveStick(ev){if(!isManualMode()||settings.control!=='stick'||!stick||stick.hidden)return;const r=stick.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2,max=r.width*.32;let dx=ev.clientX-cx,dy=ev.clientY-cy,d=Math.hypot(dx,dy);if(d>max){dx*=max/d;dy*=max/d;d=max}stickX=max?dx/max:0;stickY=max?dy/max:0;knob.style.transform='translate(calc(-50% + '+dx+'px),calc(-50% + '+dy+'px))'}
arenaEl.addEventListener('pointerdown',e=>{if(!isManualMode()||settings.control!=='stick'||!engine||engine.result!==null||paused)return;if(e.target.closest&&e.target.closest('button,select,.result'))return;stickPointer=e.pointerId;if(!settings.stickLocked)placeStickAt(e);try{arenaEl.setPointerCapture(e.pointerId)}catch{}moveStick(e);e.preventDefault()});
arenaEl.addEventListener('pointermove',e=>{if(e.pointerId===stickPointer){moveStick(e);e.preventDefault()}});
const releaseStick=e=>{if(stickPointer===null||e.pointerId===stickPointer){resetStick();e.preventDefault()}};arenaEl.addEventListener('pointerup',releaseStick);arenaEl.addEventListener('pointercancel',releaseStick);"""
rep(old_stick,new_stick,'joystick events')

# Settings event handler position -> lock.
old_handler="$ ('setting-stick-position')" # guard unused; actual exact below
old_event="$('setting-stick-position').onchange=()=>{settings.stickPosition=$('setting-stick-position').value;saveSettings();applySettingsUI()};"
new_event="$('setting-stick-lock').onchange=()=>{settings.stickLocked=$('setting-stick-lock').value==='on';resetStick();if(settings.stickLocked)resetStickBase();saveSettings();applySettingsUI()};"
rep(old_event,new_event,'stick lock handler')

# Make floating stick position deterministic in fixed mode; stale inline position cleared when entering battle in fixed mode.
# CSS: remove obsolete right-side rules, allow inline top/left positioning and keep base pointer transparent to arena.
s=s.replace(".control-stick.stick-right{left:auto;right:18px}.control-label.stick-right{left:auto;right:18px}","",1)
s=s.replace(".control-stick.stick-right{left:auto;right:14px}.control-label.stick-right{left:auto;right:14px}","",1)

# Update old v3.27 historical note only to avoid falsely saying the setting still exists today? Keep history intact.

required=[
 'BATTLE <b>v3.52</b>', '📒 패치노트 · v3.52',
 "dmg*=3;", "?3:1)",
 'setting-stick-lock', 'stickLocked:false', 'function placeStickAt(ev)',
 "arenaEl.addEventListener('pointerdown'", "f.crabVulnerableUntil=this.time+5/f.scale;f.crabMoltNext=this.time+10/f.scale"
]
for x in required:
    if x not in s: raise SystemExit('missing marker: '+x)
if 'id="setting-stick-position"' in s: raise SystemExit('old stick position setting still in HTML')
if "$('setting-stick-position').onchange" in s: raise SystemExit('old stick position handler still active')
if 'dmg*=10;' in s and "e.id==='crab'" in s[s.find('dmg*=10;')-120:s.find('dmg*=10;')+30]: raise SystemExit('old crab x10 standard multiplier remains')
if s==orig: raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('v3.52 applied')

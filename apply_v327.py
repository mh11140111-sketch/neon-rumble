from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    if old not in s:
        raise SystemExit('pattern not found: '+old[:120])
    s=s.replace(old,new,count)

# Version + patch notes
rep('BATTLE <b>v3.26</b>','BATTLE <b>v3.27</b>')
rep('📒 패치노트 · v3.26','📒 패치노트 · v3.27')
rep('<div class="patch-body"><div class="patch-version"><h3>v3.26 · 눈사람 & 분노한 남자</h3>', '<div class="patch-body"><div class="patch-version"><h3>v3.27 · 설정 & 테스트 사운드</h3><ul><li>설정 메뉴 추가. 조작 방식을 엄지스틱 / WASD / 화살표키 중 선택 가능.</li><li>엄지스틱 사용 시 위치를 왼쪽 / 오른쪽으로 변경 가능.</li><li>테스트 사운드 추가. 설정에서 소리를 켜거나 끌 수 있으며 시작·타격·승리 등에 간단한 효과음 적용.</li><li>키보드 조작은 조정 모드·스테이지 모드·조정 보스전에서만 적용.</li></ul></div><div class="patch-version"><h3>v3.26 · 눈사람 & 분노한 남자</h3>')

# Settings CSS and right-side joystick support
rep('</style><link rel="icon"', '''
.settings-btn{min-height:38px;padding:7px 11px;font-size:13px}.header-actions{display:flex;align-items:center;gap:8px}.settings-panel{margin:-10px 0 20px;padding:15px;border:1px solid #40536d;border-radius:14px;background:#101b2b}.settings-panel h2{font-size:18px;margin:0 0 12px}.settings-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.setting-item{display:flex;flex-direction:column;gap:7px;font-size:12px;color:#aebfd4}.setting-item select{width:100%;min-width:0}.settings-note{margin:10px 0 0;font-size:12px;color:#8fa4bf;line-height:1.6}.control-stick.stick-right{left:auto;right:18px}.control-label.stick-right{left:auto;right:18px}@media(max-width:560px){.settings-grid{grid-template-columns:1fr}.control-stick.stick-right{left:auto;right:14px}.control-label.stick-right{left:auto;right:14px}}
</style><link rel="icon"''')

# Header settings button + settings panel
rep('<header><a href="./" class="brand">NEON RUMBLE<span>.</span></a><span class="badge">BATTLE <b>v3.27</b></span></header>\n<p id="boot"', '''<header><a href="./" class="brand">NEON RUMBLE<span>.</span></a><div class="header-actions"><span class="badge">BATTLE <b>v3.27</b></span><button id="settings-btn" class="settings-btn" type="button" aria-expanded="false">⚙️ 설정</button></div></header>
<div id="settings-panel" class="settings-panel" hidden><h2>⚙️ 게임 설정</h2><div class="settings-grid"><label class="setting-item">조작 방식<select id="setting-control"><option value="stick">엄지스틱</option><option value="wasd">WASD</option><option value="arrows">화살표키</option></select></label><label class="setting-item">엄지스틱 위치<select id="setting-stick-position"><option value="left">왼쪽</option><option value="right">오른쪽</option></select></label><label class="setting-item">테스트 사운드<select id="setting-sound"><option value="on">켜짐</option><option value="off">꺼짐</option></select></label></div><p class="settings-note">키보드 조작은 조정 모드·스테이지 모드·조정 보스전에서만 작동해. 모바일에서는 엄지스틱을 권장해.</p></div>
<p id="boot"''')

# Stage explanatory copy
s=s.replace('모든 스테이지에서 엄지스틱으로 직접 이동해.','모든 스테이지에서 설정한 조작 방식으로 직접 이동해.')
s=s.replace('조정 모드에서만 왼쪽 캐릭터 이동 가능','조정 모드에서는 설정한 방식으로 왼쪽 캐릭터 이동 가능')

# Main state: add persisted settings before sound state
old="const {Engine,ROSTER}=window.DuelEngine,$=id=>document.getElementById(id),colors=['#69def3','#ff9873'];let relayTeams=[['boxer','archer','knight'],['spider','tree','ninja']],relaySlots=[0,0],selected=['boxer','smith'],mode='duel',bossChoice='tree',squad=['boxer','archer','knight','mage','vampire'],bossSlot=-1,side=0,engine=null,paused=false,speed=1,sound=false,audio=null,last=performance.now(),acc=0,lastHits=0,lastMessage='',stageNo=1;const canvas=$('arena'),ctx=canvas.getContext('2d');let stickX=0,stickY=0,stickPointer=null;const stick=$('control-stick'),knob=$('control-knob');"
new="const {Engine,ROSTER}=window.DuelEngine,$=id=>document.getElementById(id),colors=['#69def3','#ff9873'];const SETTINGS_KEY='neonRumble.settings.v1';let settings={control:'stick',stickPosition:'left',sound:true};try{const saved=JSON.parse(localStorage.getItem(SETTINGS_KEY)||'null');if(saved&&typeof saved==='object')settings={...settings,...saved}}catch{};if(!['stick','wasd','arrows'].includes(settings.control))settings.control='stick';if(!['left','right'].includes(settings.stickPosition))settings.stickPosition='left';settings.sound=settings.sound!==false;let relayTeams=[['boxer','archer','knight'],['spider','tree','ninja']],relaySlots=[0,0],selected=['boxer','smith'],mode='duel',bossChoice='tree',squad=['boxer','archer','knight','mage','vampire'],bossSlot=-1,side=0,engine=null,paused=false,speed=1,sound=settings.sound,audio=null,last=performance.now(),acc=0,lastHits=0,lastMessage='',stageNo=1;const canvas=$('arena'),ctx=canvas.getContext('2d');let stickX=0,stickY=0,stickPointer=null;const stick=$('control-stick'),knob=$('control-knob'),controlLabel=$('control-label');const keys=new Set();"
rep(old,new)

# Add settings functions before control boss key
rep("const CONTROL_BOSS_KEY='neonRumble.controlBossUnlocked.v1';", '''function saveSettings(){try{localStorage.setItem(SETTINGS_KEY,JSON.stringify(settings))}catch{}}
function isManualMode(){return ['control','stage','boss-control'].includes(mode)}
function controlName(){return settings.control==='wasd'?'WASD':settings.control==='arrows'?'화살표키':'엄지스틱'}
function updateSoundButtons(){const b=$('sound');if(b){b.textContent=sound?'소리 켜짐':'소리 꺼짐';b.setAttribute('aria-pressed',String(sound))}if($('setting-sound'))$('setting-sound').value=sound?'on':'off'}
function refreshControlUI(){const manual=isManualMode()&&!!engine,useStick=settings.control==='stick';if(stick){stick.hidden=!(manual&&useStick);stick.classList.toggle('stick-right',settings.stickPosition==='right')}if(controlLabel){controlLabel.hidden=!manual;controlLabel.classList.toggle('stick-right',useStick&&settings.stickPosition==='right');controlLabel.textContent=mode==='boss-control'?'보스 이동 · '+controlName():mode==='stage'?'로봇 이동 · '+controlName():'왼쪽 캐릭터 이동 · '+controlName()}if($('setting-stick-position'))$('setting-stick-position').disabled=!useStick}
function applySettingsUI(){if($('setting-control'))$('setting-control').value=settings.control;if($('setting-stick-position'))$('setting-stick-position').value=settings.stickPosition;updateSoundButtons();refreshControlUI()}
function keyboardVector(){let x=0,y=0;if(settings.control==='wasd'){if(keys.has('KeyA'))x--;if(keys.has('KeyD'))x++;if(keys.has('KeyW'))y--;if(keys.has('KeyS'))y++}else if(settings.control==='arrows'){if(keys.has('ArrowLeft'))x--;if(keys.has('ArrowRight'))x++;if(keys.has('ArrowUp'))y--;if(keys.has('ArrowDown'))y++}const n=Math.hypot(x,y)||1;return{x:x/n,y:y/n}}
function currentControlVector(){return settings.control==='stick'?{x:stickX,y:stickY}:keyboardVector()}
const CONTROL_BOSS_KEY='neonRumble.controlBossUnlocked.v1';''')

# Pointer stick only when selected
rep("function moveStick(ev){if(!['control','stage','boss-control'].includes(mode)||!stick||stick.hidden)return;", "function moveStick(ev){if(!isManualMode()||settings.control!=='stick'||!stick||stick.hidden)return;")
rep("stick.addEventListener('pointerdown',e=>{if(!['control','stage','boss-control'].includes(mode))return;", "stick.addEventListener('pointerdown',e=>{if(!isManualMode()||settings.control!=='stick')return;")

# Keyboard handlers + settings listeners inserted after pointer handlers
needle="stick.addEventListener('pointerup',releaseStick);stick.addEventListener('pointercancel',releaseStick);"
addition=needle+"\nwindow.addEventListener('keydown',e=>{if(!isManualMode()||settings.control==='stick')return;const ok=settings.control==='wasd'?['KeyW','KeyA','KeyS','KeyD'].includes(e.code):['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code);if(ok){keys.add(e.code);e.preventDefault()}});window.addEventListener('keyup',e=>{if(keys.delete(e.code))e.preventDefault()});window.addEventListener('blur',()=>keys.clear());\n$('settings-btn').onclick=()=>{const panel=$('settings-panel'),open=panel.hidden;panel.hidden=!open;$('settings-btn').setAttribute('aria-expanded',String(open))};$('setting-control').onchange=()=>{settings.control=$('setting-control').value;keys.clear();resetStick();saveSettings();applySettingsUI()};$('setting-stick-position').onchange=()=>{settings.stickPosition=$('setting-stick-position').value;saveSettings();applySettingsUI()};$('setting-sound').onchange=()=>{sound=$('setting-sound').value==='on';settings.sound=sound;saveSettings();updateSoundButtons();if(sound)playSfx('select')};"
rep(needle,addition)

# Start stage and start battle: let refreshControlUI decide controls
s=s.replace("$('control-stick').hidden=false;$('control-label').hidden=false;$('control-label').textContent=n===2?'보스 로봇 이동':'로봇 이동';resetStick();", "resetStick();refreshControlUI();")
s=s.replace("$('control-stick').hidden=!['control','boss-control'].includes(mode);$('control-label').hidden=!['control','boss-control'].includes(mode);$('control-label').textContent=mode==='boss-control'?'보스 직접 이동':'왼쪽 캐릭터 이동';resetStick();", "resetStick();refreshControlUI();")

# Selection should clear keys too
s=s.replace("function selection(){engine=null;paused=false;acc=0;resetStick();", "function selection(){engine=null;paused=false;acc=0;keys.clear();resetStick();")

# Sound control and richer test SFX
old_sound="$('start').onclick=start;$('rematch').onclick=()=>mode==='stage'?startStage(stageNo):start();$('back').onclick=selection;$('result-select').onclick=selection;$('pause').onclick=pause;$('speed').onchange=()=>{speed=Number($('speed').value);acc=0};$('sound').onclick=()=>{sound=!sound;$('sound').textContent=sound?'소리 켜짐':'소리 꺼짐';$('sound').setAttribute('aria-pressed',String(sound));tone(540)};\nfunction tone(hz){if(!sound)return;try{audio=audio||new(window.AudioContext||window.webkitAudioContext)();if(audio.state==='suspended')audio.resume();const o=audio.createOscillator(),g=audio.createGain();o.type='triangle';o.frequency.value=hz;g.gain.setValueAtTime(.035,audio.currentTime);g.gain.exponentialRampToValueAtTime(.001,audio.currentTime+.08);o.connect(g);g.connect(audio.destination);o.start();o.stop(audio.currentTime+.08)}catch{}}"
new_sound="$('start').onclick=start;$('rematch').onclick=()=>mode==='stage'?startStage(stageNo):start();$('back').onclick=selection;$('result-select').onclick=selection;$('pause').onclick=pause;$('speed').onchange=()=>{speed=Number($('speed').value);acc=0};$('sound').onclick=()=>{sound=!sound;settings.sound=sound;saveSettings();updateSoundButtons();if(sound)playSfx('select')};\nfunction tone(hz,duration=.08,volume=.035,type='triangle',delay=0){if(!sound)return;try{audio=audio||new(window.AudioContext||window.webkitAudioContext)();if(audio.state==='suspended')audio.resume();const t=audio.currentTime+delay,o=audio.createOscillator(),g=audio.createGain();o.type=type;o.frequency.setValueAtTime(hz,t);g.gain.setValueAtTime(volume,t);g.gain.exponentialRampToValueAtTime(.001,t+duration);o.connect(g);g.connect(audio.destination);o.start(t);o.stop(t+duration)}catch{}}\nfunction playSfx(kind){if(!sound)return;if(kind==='start'){tone(420,.07,.03,'square');tone(650,.1,.025,'triangle',.07)}else if(kind==='hit'){tone(150+Math.random()*90,.045,.022,'square')}else if(kind==='victory'){tone(520,.09,.035,'triangle');tone(660,.09,.035,'triangle',.1);tone(820,.15,.04,'triangle',.2)}else if(kind==='select'){tone(540,.07,.025,'triangle')}else tone(300,.06,.02,'triangle')}"
rep(old_sound,new_sound)

# Replace start tones with start sfx and HUD hit/victory sounds
s=s.replace("tone(650)}", "playSfx('start')}")
s=s.replace("if(hits>lastHits){tone(180+Math.random()*170);lastHits=hits}", "if(hits>lastHits){playSfx('hit');lastHits=hits}")
s=s.replace("$('result').hidden=false;$('pause').disabled=true;tone(760)}", "$('result').hidden=false;$('pause').disabled=true;playSfx('victory')}")

# Loop uses selected control vector instead of stick only
old_loop="if(engine&&!paused&&engine.result===null){if(mode==='control'||mode==='stage'||mode==='boss-control'){engine.controlX=stickX;engine.controlY=stickY}else{engine.controlX=0;engine.controlY=0}"
new_loop="if(engine&&!paused&&engine.result===null){if(isManualMode()){const cv=currentControlVector();engine.controlX=cv.x;engine.controlY=cv.y}else{engine.controlX=0;engine.controlY=0}"
rep(old_loop,new_loop)

# Initialize settings UI before main UI
rep("updateControlBossUnlockUI();updateSelection();$('boot').hidden=true;", "applySettingsUI();updateControlBossUnlockUI();updateSelection();$('boot').hidden=true;")

p.write_text(s,encoding='utf-8')
print('v3.27 settings, keyboard control and test sound applied')

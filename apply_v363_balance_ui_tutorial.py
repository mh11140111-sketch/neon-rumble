from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

# Version + patch notes
once('<span class="badge">BATTLE <b>v3.62</b></span>','<button id="tutorial-header-btn" class="settings-btn" type="button">📘 튜토리얼</button><span class="badge">BATTLE <b>v3.63</b></span>','header tutorial/version')
once('<details class="patch-notes"><summary>📒 패치노트 · v3.62</summary><div class="patch-body">', '<details class="patch-notes"><summary>📒 패치노트 · v3.63</summary><div class="patch-body"><div class="patch-version"><h3>v3.63 · 밸런스 · 시작 버튼 위치 · 튜토리얼 개편</h3><ul><li>😠 분노한 남자: 2번째 부활 🤬 상태의 👎 공격 주기 0.8초 → 0.7초.</li><li>🔥 일반 화상 지속시간을 5초로 조정.</li><li>🌞 태양 공격 주기 2.5초 → 3.3초.</li><li>⚙️ 설정에 게임 시작 버튼 위치(위/아래) 추가. 아래 선택 시 CHAPTER 1 바로 위에 표시.</li><li>📘 상단 버전 왼쪽에 튜토리얼 다시보기 버튼 추가 및 5장 튜토리얼로 전면 개편.</li></ul></div>', 'patch notes')

# Balance
once("🤬 단계는 👎 70/0.8초", "🤬 단계는 👎 70/0.7초", 'angry desc')
once("🤬 👎70/0.8초", "🤬 👎70/0.7초", 'angry detail')
once("rate=stage===0?1:stage===1?.5:.8;", "rate=stage===0?1:stage===1?.5:.7;", 'angry final rate')
once("expires:this.time+3*f.scale", "expires:this.time+5*f.scale", 'burn duration')
once("{id:'sun',name:'태양',icon:'🌞',tag:'태양 투사체 · 월하강림 면역',hp:1000,damage:50,speed:150,cooldown:2.5,description:'2.5초마다 ☀️ 투사체를 던진다.", "{id:'sun',name:'태양',icon:'🌞',tag:'태양 투사체 · 월하강림 면역',hp:1000,damage:50,speed:150,cooldown:3.3,description:'3.3초마다 ☀️ 투사체를 던진다.", 'sun cooldown')
once("detail:'HP 1000 · ☀️ 50 / 2.5초 + 화상", "detail:'HP 1000 · ☀️ 50 / 3.3초 + 화상", 'sun detail')

# Settings UI: add start button position and remove old settings tutorial button
once('<label class="setting-item">테스트 사운드<select id="setting-sound"><option value="on">켜짐</option><option value="off">꺼짐</option></select></label></div><p class="settings-note">', '<label class="setting-item">테스트 사운드<select id="setting-sound"><option value="on">켜짐</option><option value="off">꺼짐</option></select></label><label class="setting-item">게임 시작 버튼 위치<select id="setting-start-position"><option value="top">위</option><option value="bottom">아래 · CHAPTER 1 위</option></select></label></div><p class="settings-note">', 'settings select')
once('</p><button id="tutorial-reopen" class="tutorial-reopen" type="button">📘 튜토리얼 다시 보기</button></div>', '</p></div>', 'remove settings tutorial')

# Start button anchor. Bottom position will be immediately before stage-entry (CHAPTER 1 entry).
once('<button class="primary start" id="start" type="button" disabled>이 조합으로 전투 시작</button>', '<div id="start-top-anchor"></div><button class="primary start" id="start" type="button" disabled>이 조합으로 전투 시작</button>', 'start anchor')

# Settings data + functions
once("let settings={control:'stick',stickLocked:false,sound:true};", "let settings={control:'stick',stickLocked:false,sound:true,startPosition:'top'};", 'settings default')
once("settings.sound=settings.sound!==false;let relayTeams=", "settings.sound=settings.sound!==false;if(!['top','bottom'].includes(settings.startPosition))settings.startPosition='top';let relayTeams=", 'settings normalize')
once("function applySettingsUI(){if($('setting-control'))$('setting-control').value=settings.control;if($('setting-stick-lock'))$('setting-stick-lock').value=settings.stickLocked?'on':'off';updateSoundButtons();refreshControlUI()}", "function applyStartButtonPosition(){const b=$('start'),top=$('start-top-anchor'),stage=$('stage-entry');if(!b||!top||!stage)return;if(settings.startPosition==='bottom')stage.before(b);else top.after(b)}\nfunction applySettingsUI(){if($('setting-control'))$('setting-control').value=settings.control;if($('setting-stick-lock'))$('setting-stick-lock').value=settings.stickLocked?'on':'off';if($('setting-start-position'))$('setting-start-position').value=settings.startPosition;applyStartButtonPosition();updateSoundButtons();refreshControlUI()}", 'apply settings')
once("$('setting-sound').onchange=()=>{sound=$('setting-sound').value==='on';settings.sound=sound;saveSettings();updateSoundButtons();if(sound)playSfx('select')};", "$('setting-sound').onchange=()=>{sound=$('setting-sound').value==='on';settings.sound=sound;saveSettings();updateSoundButtons();if(sound)playSfx('select')};$('setting-start-position').onchange=()=>{settings.startPosition=$('setting-start-position').value==='bottom'?'bottom':'top';saveSettings();applyStartButtonPosition()};", 'settings handler')

# Tutorial script rewrite - keep same first-seen storage key so existing users only see when they click replay.
start=s.index('<script id="tutorial-script">')
end=s.index('</script>', start)+len('</script>')
new_tutorial='''<script id="tutorial-script">(function(){'use strict';const KEY='neonRumble.tutorialSeen.v1';const steps=[
{title:'1장 · NEON RUMBLE에 온 걸 환영해!',visual:'⚔️ NEON RUMBLE ⚔️',text:'캐릭터를 골라 여러 전투 모드를 즐기는 게임이야. 화면 위쪽에서는 모드를 바꾸고 ⚙️ 설정에서 조작 방식, 엄지스틱 고정, 소리, 게임 시작 버튼 위치를 정할 수 있어. 캐릭터를 선택한 뒤 「이 조합으로 전투 시작」을 누르면 전투가 시작돼. 시작 버튼 위치는 설정에서 위 또는 CHAPTER 1 바로 위의 아래 위치로 바꿀 수 있어.'},
{title:'2장 · 모드 변경 방법',visual:'1️⃣  👑  3️⃣  👥  🎮',text:'선택 화면 맨 위의 모드 버튼을 누르면 전투 방식이 바뀌어. 1대1 결투는 기본 자동전투, 보스전은 강화된 보스 1명과 도전자 5명, 릴레이는 3대3 순차전, 단체전은 양 팀 3명이 동시에 전투해. 🎮 조정 모드에서는 왼쪽 캐릭터를 직접 움직일 수 있고 공격과 고유 스킬은 자동으로 사용돼.'},
{title:'3장 · 스테이지와 코인',visual:'🗺️ STAGE 1 → 2 → 3   🪙',text:'CHAPTER 1부터 스테이지를 진행하고 각 챕터의 STAGE 1·2·3을 클리어하면 다음 챕터가 열려. 스테이지에서는 지정된 주인공을 직접 조작하는 경우가 많아. STAGE 1·2 클리어 시 1~30코인을 얻고, 각 챕터 STAGE 3은 기본 50코인을 줘. 일부 스테이지에는 캐릭터 해금이나 추가 코인 같은 별도 보상도 있어.'},
{title:'4장 · 상점 · 옷장 · 도박장',visual:'🛒  👗  🎰  🪙',text:'🛒 상점에서는 모은 코인으로 장신구, 아우라, 캐릭터와 해금된 챕터 배경을 살 수 있어. 👗 옷장에서는 구매하거나 획득한 꾸미기와 배경을 장착해. 🎰 도박장은 CHAPTER 5를 모두 클리어하면 열리고 50코인으로 돌릴 수 있어. 꾸미기 30%, 캐릭터 10%, 꽝 60%이며 중복 보상은 코인으로 바뀌어.'},
{title:'5장 · 이제 전투를 시작해!',visual:'📘  →  ⚔️',text:'이제 원하는 캐릭터와 모드를 골라 시작하면 돼. 설명이 다시 필요하면 언제든 화면 상단의 버전 표시 왼쪽 「📘 튜토리얼」 버튼을 누르면 이 5장을 처음부터 다시 볼 수 있어. 튜토리얼은 스킵할 수도 있고 마지막의 「게임 시작」을 누르면 바로 선택 화면으로 돌아가.'}
];let index=0;const $=id=>document.getElementById(id),overlay=$('tutorial-overlay'),title=$('tutorial-title'),visual=$('tutorial-visual'),text=$('tutorial-text'),step=$('tutorial-step'),dots=$('tutorial-dots'),prev=$('tutorial-prev'),next=$('tutorial-next'),skip=$('tutorial-skip'),reopen=$('tutorial-header-btn');if(!overlay||!title||!visual||!text||!step||!dots||!prev||!next||!skip)return;function render(){const x=steps[index];step.textContent='TUTORIAL · '+(index+1)+' / '+steps.length;title.textContent=x.title;visual.textContent=x.visual;text.textContent=x.text;prev.hidden=index===0;next.textContent=index===steps.length-1?'게임 시작':'다음';dots.innerHTML=steps.map((_,i)=>'<span class="tutorial-dot'+(i===index?' on':'')+'"></span>').join('')}function openTutorial(force){if(!force){try{if(localStorage.getItem(KEY)==='1')return}catch{}}index=0;overlay.hidden=false;document.body.style.overflow='hidden';render()}function closeTutorial(){try{localStorage.setItem(KEY,'1')}catch{}overlay.hidden=true;document.body.style.overflow=''}prev.onclick=()=>{if(index>0){index--;render()}};next.onclick=()=>{if(index<steps.length-1){index++;render()}else closeTutorial()};skip.onclick=closeTutorial;if(reopen)reopen.onclick=()=>openTutorial(true);setTimeout(()=>openTutorial(false),80)})();</script>'''
s=s[:start]+new_tutorial+s[end:]

p.write_text(s,encoding='utf-8')
print('v3.63 patch applied')

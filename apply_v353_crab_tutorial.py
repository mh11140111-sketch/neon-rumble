from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(label+' anchor missing')
    s=s.replace(old,new,count)

rep('BATTLE <b>v3.52</b>','BATTLE <b>v3.53</b>','version')
rep('📒 패치노트 · v3.52','📒 패치노트 · v3.53','patch title')
marker='<div class="patch-body">'
patch='''<div class="patch-version"><h3>v3.53 · 꽃게 이동 강화 & 첫 접속 튜토리얼</h3><ul><li>🦀 꽃게: 탈피할 때마다 이동속도 +20%.</li><li>📘 첫 접속 튜토리얼 추가. 캐릭터 선택, 기본 전투, 주요 모드, 직접 조작과 엄지스틱 사용법을 단계별로 안내.</li><li>⏭️ 튜토리얼은 처음 접속했을 때 한 번만 자동 표시되며 언제든 스킵 가능.</li><li>⚙️ 설정에 「튜토리얼 다시 보기」 버튼을 추가해 필요할 때 다시 확인 가능.</li></ul></div>'''
rep(marker,marker+patch,'patch notes')

anchor="f.crabVulnerableUntil=this.time+5/f.scale;f.crabMoltNext=this.time+10/f.scale"
rep(anchor,"f.speed*=1.2;f.crabVulnerableUntil=this.time+5/f.scale;f.crabMoltNext=this.time+10/f.scale",'crab speed buff')
s=s.replace("10초마다 탈피해 HP 200 껍질을 남기고 집게 피해 +30. 탈피 후 5초 동안 받는 피해 ×3.","10초마다 탈피해 HP 200 껍질을 남기고 집게 피해 +30, 이동속도 +20%. 탈피 후 5초 동안 받는 피해 ×3.",1)
s=s.replace("집게 +30 · 피해 ×3","집게 +30 · 이동속도 +20% · 피해 ×3",1)

style='''<style id="tutorial-style">.tutorial-overlay{position:fixed;inset:0;z-index:9999;background:#050b14e8;display:flex;align-items:center;justify-content:center;padding:20px}.tutorial-overlay[hidden]{display:none!important}.tutorial-card{width:min(520px,100%);max-height:min(760px,92dvh);overflow:auto;background:#111d2f;border:1px solid #49617e;border-radius:20px;padding:22px;box-shadow:0 24px 70px #000b}.tutorial-step{font-size:12px;letter-spacing:1.5px;color:#9fb2ca;margin-bottom:8px}.tutorial-card h2{font-size:25px;margin:0 0 12px}.tutorial-card p{font-size:15px;line-height:1.75;color:#c3d1e3;margin:0}.tutorial-visual{margin:16px 0;padding:16px;border-radius:14px;background:#0b1525;border:1px solid #2e425d;font-size:34px;text-align:center;line-height:1.5}.tutorial-actions{display:flex;gap:8px;margin-top:20px;flex-wrap:wrap}.tutorial-actions button{flex:1;min-width:105px}.tutorial-skip{background:#111a29;color:#9fb2ca}.tutorial-next{background:#b8f279;border-color:#b8f279;color:#132015;font-weight:850}.tutorial-dots{display:flex;justify-content:center;gap:6px;margin-top:16px}.tutorial-dot{width:7px;height:7px;border-radius:50%;background:#3e5068}.tutorial-dot.on{background:#b8f279}.tutorial-reopen{margin-top:10px;width:100%}@media(max-width:560px){.tutorial-overlay{padding:12px}.tutorial-card{padding:18px;border-radius:16px}.tutorial-card h2{font-size:22px}.tutorial-card p{font-size:14px}.tutorial-visual{font-size:30px;margin:12px 0}.tutorial-actions button{min-height:44px}}</style>'''
modal='''<div id="tutorial-overlay" class="tutorial-overlay" hidden role="dialog" aria-modal="true" aria-labelledby="tutorial-title"><div class="tutorial-card"><div id="tutorial-step" class="tutorial-step"></div><h2 id="tutorial-title"></h2><div id="tutorial-visual" class="tutorial-visual"></div><p id="tutorial-text"></p><div id="tutorial-dots" class="tutorial-dots"></div><div class="tutorial-actions"><button id="tutorial-skip" class="tutorial-skip" type="button">스킵</button><button id="tutorial-prev" type="button">이전</button><button id="tutorial-next" class="tutorial-next" type="button">다음</button></div></div></div>'''
rep('</head><body><main>',style+'</head><body><main>'+modal,'tutorial markup')

old='''<p class="settings-note">키보드 조작은 조정 모드·스테이지 모드·조정 보스전에서만 작동해. 엄지스틱 고정 해제 시 경기장 어디를 눌러도 그 위치에서 조작할 수 있어.</p></div>'''
new='''<p class="settings-note">키보드 조작은 조정 모드·스테이지 모드·조정 보스전에서만 작동해. 엄지스틱 고정 해제 시 경기장 어디를 눌러도 그 위치에서 조작할 수 있어.</p><button id="tutorial-reopen" class="tutorial-reopen" type="button">📘 튜토리얼 다시 보기</button></div>'''
rep(old,new,'tutorial reopen button')

tutorial_js=r'''<script id="tutorial-script">(function(){'use strict';const KEY='neonRumble.tutorialSeen.v1';const steps=[{title:'NEON RUMBLE에 온 걸 환영해!',visual:'⚔️  VS  ⚔️',text:'캐릭터를 골라 전투를 시작하는 게임이야. 대부분의 일반 전투에서는 캐릭터가 자동으로 이동하고 공격해. 각 캐릭터의 고유 능력과 상성을 보는 것이 기본 플레이야.'},{title:'캐릭터를 고르고 전투 시작',visual:'👈 🥊   VS   🧙 👉',text:'선택 화면에서 왼쪽과 오른쪽 캐릭터를 고른 뒤 「이 조합으로 전투 시작」을 누르면 돼. 같은 캐릭터끼리도 대결할 수 있고 검색창으로 원하는 캐릭터를 빠르게 찾을 수 있어.'},{title:'기본 전투 모드',visual:'1️⃣  👑  3️⃣  👥',text:'1대1 결투는 기본 대결, 보스전은 강해진 보스 1명과 도전자 5명이 싸워. 릴레이는 3대3 순차전, 단체전은 양 팀 3명이 동시에 싸우는 모드야.'},{title:'직접 조작 모드',visual:'🎮  👆↔️↕️',text:'조정 모드와 스테이지에서는 주인공을 직접 움직일 수 있어. 모바일 엄지스틱은 경기장 아무 곳이나 눌러 조작할 수 있고, 설정에서 「고정 / 고정 해제」를 바꿀 수 있어.'},{title:'스테이지와 성장 요소',visual:'🗺️  🪙  🛒  👗',text:'스테이지를 클리어하면 다음 챕터가 열리고 코인이나 일부 캐릭터를 얻을 수 있어. 코인은 상점에서 사용하고, 구매한 꾸미기와 배경은 옷장에서 장착할 수 있어.'}];let index=0;const $=id=>document.getElementById(id),overlay=$('tutorial-overlay'),title=$('tutorial-title'),visual=$('tutorial-visual'),text=$('tutorial-text'),step=$('tutorial-step'),dots=$('tutorial-dots'),prev=$('tutorial-prev'),next=$('tutorial-next'),skip=$('tutorial-skip'),reopen=$('tutorial-reopen');if(!overlay||!title||!visual||!text||!step||!dots||!prev||!next||!skip)return;function render(){const x=steps[index];step.textContent='TUTORIAL · '+(index+1)+' / '+steps.length;title.textContent=x.title;visual.textContent=x.visual;text.textContent=x.text;prev.hidden=index===0;next.textContent=index===steps.length-1?'게임 시작':'다음';dots.innerHTML=steps.map((_,i)=>'<span class="tutorial-dot'+(i===index?' on':'')+'"></span>').join('')}function openTutorial(force){if(!force){try{if(localStorage.getItem(KEY)==='1')return}catch{}}index=0;overlay.hidden=false;document.body.style.overflow='hidden';render()}function closeTutorial(){try{localStorage.setItem(KEY,'1')}catch{}overlay.hidden=true;document.body.style.overflow=''}prev.onclick=()=>{if(index>0){index--;render()}};next.onclick=()=>{if(index<steps.length-1){index++;render()}else closeTutorial()};skip.onclick=closeTutorial;if(reopen)reopen.onclick=()=>openTutorial(true);setTimeout(()=>openTutorial(false),80)})();</script>'''
rep('</body>',tutorial_js+'</body>','tutorial script')

required=['BATTLE <b>v3.53</b>','📒 패치노트 · v3.53','f.speed*=1.2;f.crabVulnerableUntil','id="tutorial-overlay"','id="tutorial-reopen"','neonRumble.tutorialSeen.v1','v3.53 · 꽃게 이동 강화 & 첫 접속 튜토리얼','스테이지와 성장 요소']
for x in required:
    if x not in s: raise SystemExit('missing marker: '+x)
if s==orig: raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('v3.53 applied')

from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1, got {n}')
    s=s.replace(old,new,1)

# version + patch notes (no secret codes or rewards here)
once('BATTLE <b>v3.72</b>','BATTLE <b>v3.73</b>','version')
once('<summary>📒 패치노트 · v3.72</summary><div class="patch-body">', '<summary>📒 패치노트 · v3.73</summary><div class="patch-body"><div class="patch-version"><h3>v3.73 · 코드 · 악마의 한마디 · 악마 밸런스</h3><ul><li>⚙️ 설정에 코드 입력 기능 추가. 사용 방법은 튜토리얼에서 확인 가능.</li><li>👿 CHAPTER 10 STAGE 3 클리어 후 「악마의 한마디」 해금. 50코인으로 대화 가능하며 아주 가끔 특별한 힌트를 들을 수 있음.</li><li>👿 악마 샌드박스 버전 및 전투 밸런스 조정.</li></ul></div>', 'patch note')

# settings code UI
old='</select></label></div><p class="settings-note">키보드 조작은 조정 모드·스테이지 모드·조정 보스전에서만 작동해. 엄지스틱 고정 해제 시 경기장 어디를 눌러도 그 위치에서 조작할 수 있어.</p></div>'
new='</select></label></div><div id="code-box" style="margin-top:14px;padding:12px;border:1px solid #35465f;border-radius:12px;background:#0c1726"><strong style="display:block;margin-bottom:8px">🎁 코드 입력</strong><div style="display:flex;gap:8px;flex-wrap:wrap"><input id="code-input" type="text" autocomplete="off" autocapitalize="none" spellcheck="false" placeholder="코드를 입력해" style="flex:1;min-width:170px;background:#111c2b;color:#edf3ff;border:1px solid #35465f;border-radius:10px;padding:11px 12px;font:inherit"><button id="code-submit" type="button">코드 사용</button></div><small id="code-result" style="display:block;margin-top:8px;color:#b8f279;line-height:1.5"></small></div><p class="settings-note">키보드 조작은 조정 모드·스테이지 모드·조정 보스전에서만 작동해. 엄지스틱 고정 해제 시 경기장 어디를 눌러도 그 위치에서 조작할 수 있어. 코드는 설정의 「🎁 코드 입력」에서 사용할 수 있어.</p></div>'
once(old,new,'settings code box')

# sandbox demon roster
old="{id:'hell_demon',name:'악마',icon:'👿',tag:'악의 돌진 · 악의 소환 · 무적',hp:6666,damage:13,speed:175,cooldown:0,stageOnly:true,description:'5초마다 악의 돌진, 3초마다 HP 66 악마의 눈 소환, 13초마다 5초 무적과 HP 500 회복을 사용한다.',detail:'HP 6666 · 악의 돌진 13~666 / 5초 · 🧿 HP 66 소환 / 3초 · 무적 5초 + HP 500 / 13초'},"
new="{id:'hell_demon',name:'악마',icon:'👿',tag:'악의 돌진 · 악의 소환 · 무적',hp:1366,damage:13,speed:175,cooldown:0,unlock:'hellDemon',description:'5초마다 악의 돌진으로 피해 13~166. 13초마다 HP 66 악마의 눈을 소환하고, 13초마다 5초 무적과 HP 500 회복을 사용한다.',detail:'HP 1366 · 악의 돌진 13~166 / 5초 · 🧿 HP 66 소환 / 13초 · 무적 5초 + HP 500 / 13초 · 특별 코드로 샌드박스 해금'},"
once(old,new,'sandbox demon roster')
# clone text follows same shared mechanics
once("description:'5초마다 악의 돌진, 3초마다 HP 66 악마의 눈 소환, 13초마다 5초 무적과 HP 500 회복을 사용한다.',detail:'HP 666 · 악의 돌진 13~666 / 5초 · 🧿 HP 66 소환 / 3초 · 무적 5초 + HP 500 / 13초'", "description:'5초마다 악의 돌진, 13초마다 HP 66 악마의 눈 소환, 13초마다 5초 무적과 HP 500 회복을 사용한다.',detail:'HP 666 · 악의 돌진 13~166 / 5초 · 🧿 HP 66 소환 / 13초 · 무적 5초 + HP 500 / 13초'", 'clone text')

# demon mechanics shared by clone / demon
once("f.hellSummonNext=this.time+3;f.hellInvulnNext=this.time+13", "f.hellSummonNext=this.time+13;f.hellInvulnNext=this.time+13", 'demon initial summon')
once("f.hellSummonNext=this.time+3;this.spawnHellEye(f)", "f.hellSummonNext=this.time+13;this.spawnHellEye(f)", 'demon recurring summon')
once("f.hellDashDamage=13+Math.floor(this.random()*654)", "f.hellDashDamage=13+Math.floor(this.random()*154)", 'demon dash max 166')

# unlock storage + character gate
once("HELL_STAGE_KEY='neonRumble.hellStages.v1',SHARK_UNLOCK_KEY", "HELL_STAGE_KEY='neonRumble.hellStages.v1',HELL_DEMON_UNLOCK_KEY='neonRumble.hellDemonUnlocked.v1',CODE_REDEEMED_KEY='neonRumble.redeemedCodes.v1',SHARK_UNLOCK_KEY", 'keys')
once("oldTvUnlocked=false,doctorUnlocked=false;", "oldTvUnlocked=false,doctorUnlocked=false,hellDemonUnlocked=false;", 'unlock state')
once("doctorUnlocked=localStorage.getItem(DOCTOR_UNLOCK_KEY)==='1';sharkUnlocked=", "doctorUnlocked=localStorage.getItem(DOCTOR_UNLOCK_KEY)==='1';hellDemonUnlocked=localStorage.getItem(HELL_DEMON_UNLOCK_KEY)==='1';sharkUnlocked=", 'unlock load')
once("(c?.unlock==='doctor'&&!doctorUnlocked)}", "(c?.unlock==='doctor'&&!doctorUnlocked)||(c?.unlock==='hellDemon'&&!hellDemonUnlocked)}", 'character lock')

# mark CH10 stage refreshes devil talk unlock
once("function markHellStage(n){hellStageMask|=(1<<(n-1));try{localStorage.setItem(HELL_STAGE_KEY,String(hellStageMask))}catch{}updateChapter10UI();return (hellStageMask&7)===7}", "function markHellStage(n){hellStageMask|=(1<<(n-1));try{localStorage.setItem(HELL_STAGE_KEY,String(hellStageMask))}catch{}updateChapter10UI();updateDevilTalkUI();return (hellStageMask&7)===7}", 'mark hell stage')

# code redemption functions placed after economy keys, functions use live globals at click time
anchor="const COIN_KEY='neonRumble.coins.v1'"
idx=s.find(anchor)
if idx<0: raise SystemExit('economy anchor missing')
insert="""const CODE_VALUES={neon67:'coins',itisme13666:'demon',skip82:'skip'};\nlet redeemedCodes=new Set;try{const x=JSON.parse(localStorage.getItem(CODE_REDEEMED_KEY)||'[]');if(Array.isArray(x))redeemedCodes=new Set(x)}catch{}\nfunction saveRedeemedCodes(){try{localStorage.setItem(CODE_REDEEMED_KEY,JSON.stringify([...redeemedCodes]))}catch{}}\nfunction redeemSecretCode(raw){const code=String(raw||'').trim().toLowerCase(),out=$('code-result');if(!CODE_VALUES[code]){if(out)out.textContent='❌ 존재하지 않는 코드야.';return false}if(redeemedCodes.has(code)){if(out)out.textContent='⚠️ 이미 사용한 코드야.';return false}if(code==='neon67'){coins+=666;saveEconomy();updateCoinUI();if(out)out.textContent='✅ 코드 적용 완료 · 🪙 666코인 획득!'}else if(code==='skip82'){stageSkipTickets+=10;try{localStorage.setItem(STAGE_SKIP_KEY,String(stageSkipTickets))}catch{}renderWardrobe();if(out)out.textContent='✅ 코드 적용 완료 · 🎫 스테이지 스킵권 10개 획득!'}else if(code==='itisme13666'){hellDemonUnlocked=true;try{localStorage.setItem(HELL_DEMON_UNLOCK_KEY,'1')}catch{}refreshUnlockCards();if(out)out.textContent='✅ 코드 적용 완료 · 👿 악마가 샌드박스에 해금됐어!'}redeemedCodes.add(code);saveRedeemedCodes();return true}\n"""
s=s[:idx]+insert+s[idx:]

# wire settings code button after settings button handler
anchor2="$('settings-btn').onclick=()=>{const panel=$('settings-panel'),open=panel.hidden;panel.hidden=!open;$('settings-btn').setAttribute('aria-expanded',String(open))};"
new2=anchor2+"const codeSubmit=$('code-submit'),codeInput=$('code-input');if(codeSubmit)codeSubmit.onclick=()=>{redeemSecretCode(codeInput?.value);if(codeInput)codeInput.value=''};if(codeInput)codeInput.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();codeSubmit?.click()}});"
once(anchor2,new2,'code handler')

# devil talk system, inserted before setupChapter10UI invocation
anchor3="setupChapter9UI();setupChapter10UI();\n})();"
devil=r"""
const DEVIL_TALK_LINES=[
 '인간아, 지옥까지 왔으니 제법이군.',
 '50코인이라… 네 호기심은 꽤 비싸구나.',
 '다음에는 조력자 없이 와 보는 건 어떠냐?',
 '내 눈들은 아직 너를 보고 있다.',
 '강한 자보다 끝까지 버티는 자가 귀찮더군.',
 '이곳의 불꽃은 꺼지지 않는다.',
 '네가 이겼다고 지옥이 끝난 것은 아니다.',
 '스킵도 실력이라 생각하나? 재미있는 인간이군.',
 '가끔 설정을 자세히 보는 것도 도움이 되지.',
 '비밀은 대개 아무도 읽지 않는 곳에 숨어 있지.'
];
function devilTalkUnlocked(){return !!(hellStageMask&4)}
function updateDevilTalkUI(){const b=$('devil-talk-btn');if(!b)return;const ok=devilTalkUnlocked();b.hidden=!ok;b.disabled=!ok;b.textContent='👿 악마의 한마디 · 🪙 50'}
function devilSpeak(){if(!devilTalkUnlocked())return;if(coins<50){alert('코인이 부족해! 악마에게 말을 걸려면 50코인이 필요해.');return}coins-=50;saveEconomy();updateCoinUI();const r=Math.random();let line;if(r<.005)line='…정말 여기까지 들었군. itisme13666';else if(r<.02)line='지옥의 문에는 숫자가 새겨져 있지. skip82';else if(r<.045)line='네온빛 속에서 이런 글자를 본 적 있나? neon67';else line=DEVIL_TALK_LINES[Math.floor(Math.random()*DEVIL_TALK_LINES.length)];alert('👿 악마: “'+line+'”')}
function setupDevilTalkUI(){if($('devil-talk-btn')){updateDevilTalkUI();return}const after=$('chapter10-entry');if(!after)return;const b=document.createElement('button');b.id='devil-talk-btn';b.type='button';b.className=after.className;b.style.marginTop='8px';b.onclick=devilSpeak;after.insertAdjacentElement('afterend',b);updateDevilTalkUI()}
setupChapter9UI();setupChapter10UI();setupDevilTalkUI();
})();"""
once(anchor3,devil,'devil talk insert')

# CH10 visible text mechanics
s=s.replace('악의 돌진 13~666/5초 · 악마의 눈 HP 66 소환/3초', '악의 돌진 13~166/5초 · 악마의 눈 HP 66 소환/13초')
s=s.replace('HP 666 · 악의 돌진 · 악의 소환 · 13초마다 5초 무적+500 회복', 'HP 666 · 악의 돌진 13~166 · 악의 눈 13초 · 13초마다 5초 무적+500 회복')

# tutorial: insert a code step before final step and renumber final title
old_t="{title:'5장 · 이제 전투를 시작해!',visual:'📘  →  ⚔️',text:'이제 원하는 캐릭터와 모드를 골라 시작하면 돼. 설명이 다시 필요하면 언제든 화면 상단의 버전 표시 왼쪽 「📘 튜토리얼」 버튼을 누르면 이 5장을 처음부터 다시 볼 수 있어. 튜토리얼은 스킵할 수도 있고 마지막의 「게임 시작」을 누르면 바로 선택 화면으로 돌아가.'}"
new_t="{title:'5장 · 코드는 어디에서 쓰나?',visual:'⚙️  →  🎁  →  ✅',text:'게임에서 코드를 발견했다면 화면 위쪽 ⚙️ 설정을 열고 「🎁 코드 입력」 칸에 코드를 적은 뒤 「코드 사용」을 눌러. 코드는 정확히 입력해야 하며, 같은 코드는 한 번만 사용할 수 있어.'},{title:'6장 · 이제 전투를 시작해!',visual:'📘  →  ⚔️',text:'이제 원하는 캐릭터와 모드를 골라 시작하면 돼. 설명이 다시 필요하면 언제든 화면 상단의 버전 표시 왼쪽 「📘 튜토리얼」 버튼을 누르면 이 6장을 처음부터 다시 볼 수 있어. 튜토리얼은 스킵할 수도 있고 마지막의 「게임 시작」을 누르면 바로 선택 화면으로 돌아가.'}"
once(old_t,new_t,'tutorial code step')

# generic ability display for sandbox demon
anchor4="function ability(f){if(f.id==='doctor')"
once(anchor4,"function ability(f){if(f.id==='hell_demon'||f.id==='hell_clone')return '👿 돌진 13~166 / 5초 · 🧿 소환 13초 · 무적+500 회복 13초';if(f.id==='doctor')",'demon ability HUD')

p.write_text(s,encoding='utf-8')
print('v3.73 patch applied')
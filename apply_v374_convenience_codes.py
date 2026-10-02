from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1, got {n}')
    s=s.replace(old,new,1)

# Keep v3.74; prepend convenience patch note without exposing code strings or exact secret rewards.
once(
'<summary>📒 패치노트 · v3.74</summary><div class="patch-body"><div class="patch-version"><h3>v3.74 · 악마 밸런스 · 지옥의 불</h3>',
'<summary>📒 패치노트 · v3.74</summary><div class="patch-body"><div class="patch-version"><h3>v3.74 · 편의성 추가</h3><ul><li>👿 악마의 한마디 대사를 확장하고 새로운 비밀 보상을 추가.</li><li>⏩ 특정 비밀을 발견하면 고속 전투 배속을 추가로 사용할 수 있음.</li><li>🔥 CHAPTER 10 STAGE 3 클리어 시 기본 클리어 코인과 별도로 추가 150코인 지급.</li></ul></div><div class="patch-version"><h3>v3.74 · 악마 밸런스 · 지옥의 불</h3>',
'patch note')

# Speed selector shows locked options until secret code is redeemed.
once(
'<select id="speed"><option value="1">1× 속도</option><option value="2">2× 속도</option><option value="4">4× 속도</option></select>',
'<select id="speed"><option value="1">1× 속도</option><option value="2">2× 속도</option><option value="4">4× 속도</option><option value="5" data-secret-speed disabled>🔒 5× 속도</option><option value="10" data-secret-speed disabled>🔒 10× 속도</option></select>',
'speed options')

# Add speed-unlock storage and state near existing code storage.
once(
"const STAGE_SKIP_KEY='neonRumble.stageSkipTickets.v1',FORGE_JOB_KEY='neonRumble.craftJob.v1';\nlet stageSkipTickets=0,craftJob=null;",
"const STAGE_SKIP_KEY='neonRumble.stageSkipTickets.v1',FORGE_JOB_KEY='neonRumble.craftJob.v1',FAST_SPEED_KEY='neonRumble.fastSpeedUnlocked.v1';\nlet stageSkipTickets=0,craftJob=null,fastSpeedUnlocked=false;",
'fast speed constants')
once(
"let stageSkipTickets=0,craftJob=null,fastSpeedUnlocked=false;try{stageSkipTickets=Math.max(0,parseInt(localStorage.getItem(STAGE_SKIP_KEY)||'0',10)||0);craftJob=JSON.parse(localStorage.getItem(FORGE_JOB_KEY)||'null')}catch{}",
"let stageSkipTickets=0,craftJob=null,fastSpeedUnlocked=false;try{stageSkipTickets=Math.max(0,parseInt(localStorage.getItem(STAGE_SKIP_KEY)||'0',10)||0);craftJob=JSON.parse(localStorage.getItem(FORGE_JOB_KEY)||'null');fastSpeedUnlocked=localStorage.getItem(FAST_SPEED_KEY)==='1'}catch{}",
'load fast speed')

# Expand code registry and redemption.
once(
"const CODE_VALUES={neon67:'coins',itisme13666:'demon',skip82:'skip'};",
"const CODE_VALUES={neon67:'coins',itisme13666:'demon',skip82:'skip',ninja4:'ninjaSkin',fast8282:'fastSpeed'};",
'code registry')

old_redeem="""function redeemSecretCode(raw){const code=String(raw||'').trim().toLowerCase(),out=$('code-result');if(!CODE_VALUES[code]){if(out)out.textContent='❌ 존재하지 않는 코드야.';return false}if(redeemedCodes.has(code)){if(out)out.textContent='⚠️ 이미 사용한 코드야.';return false}if(code==='neon67'){coins+=666;saveEconomy();updateCoinUI();if(out)out.textContent='✅ 코드 적용 완료 · 🪙 666코인 획득!'}else if(code==='skip82'){stageSkipTickets+=10;try{localStorage.setItem(STAGE_SKIP_KEY,String(stageSkipTickets))}catch{}renderWardrobe();if(out)out.textContent='✅ 코드 적용 완료 · 🎫 스테이지 스킵권 10개 획득!'}else if(code==='itisme13666'){hellDemonUnlocked=true;try{localStorage.setItem(HELL_DEMON_UNLOCK_KEY,'1')}catch{}refreshUnlockCards();if(out)out.textContent='✅ 코드 적용 완료 · 👿 악마가 샌드박스에 해금됐어!'}redeemedCodes.add(code);saveRedeemedCodes();return true}"""
new_redeem="""function updateSpeedUnlockUI(){const sel=$('speed');if(!sel)return;for(const opt of sel.querySelectorAll('[data-secret-speed]')){opt.disabled=!fastSpeedUnlocked;opt.textContent=(fastSpeedUnlocked?'':'🔒 ')+opt.value+'× 속도'}if(!fastSpeedUnlocked&&Number(sel.value)>4){sel.value='4';speed=4}}
function redeemSecretCode(raw){const code=String(raw||'').trim().toLowerCase(),out=$('code-result');if(!CODE_VALUES[code]){if(out)out.textContent='❌ 존재하지 않는 코드야.';return false}if(redeemedCodes.has(code)){if(out)out.textContent='⚠️ 이미 사용한 코드야.';return false}if(code==='neon67'){coins+=666;saveEconomy();updateCoinUI();if(out)out.textContent='✅ 코드 적용 완료 · 🪙 666코인 획득!'}else if(code==='skip82'){stageSkipTickets+=10;try{localStorage.setItem(STAGE_SKIP_KEY,String(stageSkipTickets))}catch{}renderWardrobe();if(out)out.textContent='✅ 코드 적용 완료 · 🎫 스테이지 스킵권 10개 획득!'}else if(code==='itisme13666'){hellDemonUnlocked=true;try{localStorage.setItem(HELL_DEMON_UNLOCK_KEY,'1')}catch{}refreshUnlockCards();if(out)out.textContent='✅ 코드 적용 완료 · 👿 악마가 샌드박스에 해금됐어!'}else if(code==='ninja4'){if(!ownedCosmetics.includes('skin_ninja_mask'))ownedCosmetics.push('skin_ninja_mask');saveEconomy();renderWardrobe();renderShop();updateSelection();if(out)out.textContent='✅ 코드 적용 완료 · 👺 마스크닌자 스킨 획득!'}else if(code==='fast8282'){fastSpeedUnlocked=true;try{localStorage.setItem(FAST_SPEED_KEY,'1')}catch{}updateSpeedUnlockUI();if(out)out.textContent='✅ 코드 적용 완료 · ⏩ 5× / 10× 전투 배속 해금!'}redeemedCodes.add(code);saveRedeemedCodes();return true}"""
once(old_redeem,new_redeem,'redeem codes')

# Add code-only Ninja skin; hide code-only items from shop.
once(
"{id:'skin_genie',name:'알라딘의 지니 스킨',icon:'🧞',price:700,type:'skin',skinFor:'aladdin',skinTarget:'genie',exclusiveFor:'aladdin',desc:'👳‍♀️ 알라딘이 소환하는 지니 전용 스킨'},",
"{id:'skin_genie',name:'알라딘의 지니 스킨',icon:'🧞',price:700,type:'skin',skinFor:'aladdin',skinTarget:'genie',exclusiveFor:'aladdin',desc:'👳‍♀️ 알라딘이 소환하는 지니 전용 스킨'},\n {id:'skin_ninja_mask',name:'마스크닌자 스킨',icon:'👺',price:0,type:'skin',skinFor:'ninja',skinTarget:'fighter',exclusiveFor:'ninja',codeOnly:true,desc:'🥷 닌자 전용 비밀 스킨'},",
'ninja skin item')
once("for(const item of SHOP_ITEMS){if(item.casinoOnly)continue;",
     "for(const item of SHOP_ITEMS){if(item.casinoOnly||item.codeOnly)continue;",
     'hide code only shop')

# Safeguard speed selector even if manipulated.
once(
"$('speed').onchange=()=>{speed=Number($('speed').value);acc=0};",
"$('speed').onchange=()=>{const next=Number($('speed').value);if(next>4&&!fastSpeedUnlocked){$('speed').value=String(speed<=4?speed:4);return}speed=next;acc=0};",
'speed handler')

# Initialize speed lock state at boot.
once(
"$('casino-spin').onclick=spinCasino;applySettingsUI();updateControlBossUnlockUI();",
"$('casino-spin').onclick=spinCasino;applySettingsUI();updateSpeedUnlockUI();updateControlBossUnlockUI();",
'boot speed ui')

# Expand devil dialogue and rare code pool. Demon unlock remains the rarest.
old_lines="""const DEVIL_TALK_LINES=[
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
];"""
new_lines="""const DEVIL_TALK_LINES=[
 '인간아, 지옥까지 왔으니 제법이군.',
 '50코인이라… 네 호기심은 꽤 비싸구나.',
 '다음에는 조력자 없이 와 보는 건 어떠냐?',
 '내 눈들은 아직 너를 보고 있다.',
 '강한 자보다 끝까지 버티는 자가 귀찮더군.',
 '이곳의 불꽃은 꺼지지 않는다.',
 '네가 이겼다고 지옥이 끝난 것은 아니다.',
 '스킵도 실력이라 생각하나? 재미있는 인간이군.',
 '가끔 설정을 자세히 보는 것도 도움이 되지.',
 '비밀은 대개 아무도 읽지 않는 곳에 숨어 있지.',
 '닌자의 얼굴 뒤에는 또 다른 얼굴이 있지.',
 '빠르게 달리는 것과 시간을 빠르게 돌리는 것은 다르다.',
 '내가 하는 말을 전부 믿지는 마라. 가끔은 진짜 비밀도 섞여 있으니.',
 '지옥에서 가장 무서운 것은 불이 아니라 반복이다.',
 '너는 승리를 원하나, 아니면 숨겨진 것을 찾고 있나?',
 '악마에게 질문하는 데 돈을 쓰다니. 인간은 역시 재미있군.',
 '검은 화면 뒤에도 길은 있다. 눈에 보이는 것만 누르지 마라.',
 '숫자는 거짓말을 하지 않는다. 다만 악마는 숫자로 거짓말할 수 있지.',
 '어떤 비밀은 강한 자보다 오래 머무는 자가 먼저 발견한다.',
 '오늘은 아무것도 안 알려 주겠다. 그것도 하나의 대답이지.'
];"""
once(old_lines,new_lines,'devil lines')

old_speak="function devilSpeak(){if(!devilTalkUnlocked())return;if(coins<50){alert('코인이 부족해! 악마에게 말을 걸려면 50코인이 필요해.');return}coins-=50;saveEconomy();updateCoinUI();const r=Math.random();let line;if(r<.005)line='…정말 여기까지 들었군. itisme13666';else if(r<.02)line='지옥의 문에는 숫자가 새겨져 있지. skip82';else if(r<.045)line='네온빛 속에서 이런 글자를 본 적 있나? neon67';else line=DEVIL_TALK_LINES[Math.floor(Math.random()*DEVIL_TALK_LINES.length)];alert('👿 악마: “'+line+'”')}"
new_speak="function devilSpeak(){if(!devilTalkUnlocked())return;if(coins<50){alert('코인이 부족해! 악마에게 말을 걸려면 50코인이 필요해.');return}coins-=50;saveEconomy();updateCoinUI();const r=Math.random();let line;if(r<.003)line='…정말 여기까지 들었군. itisme13666';else if(r<.011)line='가면을 원하는 닌자가 있다면 기억해라. ninja4';else if(r<.023)line='시간을 더 빠르게 흘리고 싶나? fast8282';else if(r<.038)line='지옥의 문에는 숫자가 새겨져 있지. skip82';else if(r<.063)line='네온빛 속에서 이런 글자를 본 적 있나? neon67';else line=DEVIL_TALK_LINES[Math.floor(Math.random()*DEVIL_TALK_LINES.length)];alert('👿 악마: “'+line+'”')}"
once(old_speak,new_speak,'devil code speech')

# CH10 stage 3: base stage reward + separate 150 bonus every clear.
old_hell="else if(mode==='hell'&&engine.result===0){const coinReward=awardStageCoins(hellStageNo);markHellStage(hellStageNo);$('winner-icon').textContent='🔥';$('winner').textContent='CHAPTER 10 · STAGE '+hellStageNo+' 클리어!';$('summary').textContent=t+'초 · 지옥 돌파 성공 · 🪙 '+coinReward+'코인 획득!'}"
new_hell="else if(mode==='hell'&&engine.result===0){const coinReward=awardStageCoins(hellStageNo),hellBonus=hellStageNo===3?150:0;if(hellBonus){coins+=hellBonus;saveEconomy();updateCoinUI()}markHellStage(hellStageNo);$('winner-icon').textContent='🔥';$('winner').textContent='CHAPTER 10 · STAGE '+hellStageNo+' 클리어!';$('summary').textContent=t+'초 · 지옥 돌파 성공 · 🪙 기본 '+coinReward+'코인 획득!'+(hellBonus?' · 👿 STAGE 3 추가 보상 🪙 150코인 · 총 '+(coinReward+hellBonus)+'코인':'')}"
once(old_hell,new_hell,'hell stage reward')

# Show stage 3 reward in chapter card.
once(
'<span class="card-desc">HP 6666 · 누적 1500 피해마다 히어로/조력자 HP 500 회복</span>',
'<span class="card-desc">HP 6666 · 누적 1500 피해마다 히어로/조력자 HP 500 회복 · 클리어 시 기본 코인 + 추가 150코인</span>',
'hell stage3 card reward')

p.write_text(s,encoding='utf-8')
print('v3.74 convenience patch applied')

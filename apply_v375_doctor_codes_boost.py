from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1, got {n}')
    s=s.replace(old,new,1)

# v3.75 badge + patch notes (do not expose secret code strings)
once('BATTLE <b>v3.74</b>','BATTLE <b>v3.75</b>','version badge')
once(
'<summary>📒 패치노트 · v3.74</summary><div class="patch-body">',
'<summary>📒 패치노트 · v3.75</summary><div class="patch-body"><div class="patch-version"><h3>v3.75 · 의사 밸런스 · 비밀 보상 확장</h3><ul><li>👨‍⚕️ 의사 주사기 상태이상을 독 75% / 맹독 25%로 변경.</li><li>👿 악마의 한마디 대사를 추가하고 새로운 비밀 코드를 확장.</li><li>🎟️ 코인 2배 획득권 추가. 사용 시 10분 동안 코인 획득량이 2배가 되며 1회용.</li><li>🎰 도박장에서 코인 2배 획득권이 15% 확률로 등장.</li></ul></div>',
'patch note')

# Doctor roster / runtime / UI
once(
"{id:'doctor',name:'의사',icon:'👨‍⚕️',tag:'💉 주사기 · 약물치료',hp:1000,damage:70,speed:145,cooldown:1,unlock:'doctor',description:'가장 가까운 캐릭터를 향해 💉 주사기를 겨눈다. 적이 닿으면 피해 70과 독, 아군이 닿으면 즉시 HP 30 회복과 3초 약물치료를 부여한다. 약물치료는 0.5초마다 HP 10을 회복한다.',detail:'HP 1000 · 💉 적 70+독 · 아군 즉시 +30 · 약물치료 3초 / 0.5초마다 +10 · CH9 STAGE 3 10% 획득'},",
"{id:'doctor',name:'의사',icon:'👨‍⚕️',tag:'💉 주사기 · 독/맹독 · 약물치료',hp:1000,damage:70,speed:145,cooldown:1,unlock:'doctor',description:'가장 가까운 캐릭터를 향해 💉 주사기를 겨눈다. 적이 닿으면 피해 70과 함께 75% 확률로 독, 25% 확률로 맹독을 부여한다. 아군이 닿으면 즉시 HP 30 회복과 3초 약물치료를 부여한다.',detail:'HP 1000 · 💉 적 70 · 독 75% / 맹독 25% · 아군 즉시 +30 · 약물치료 3초 / 0.5초마다 +10 · CH9 STAGE 3 10% 획득'},",
'doctor roster')
once(
"if(t.team!==f.team){const dealt=this.attack(f,t,70*f.scale);if(dealt>0&&t.health>0)this.applyPoison(f,t);this.effect(t,'💉 70 + 독!','skill')}",
"if(t.team!==f.team){const dealt=this.attack(f,t,70*f.scale);if(dealt>0&&t.health>0){if(this.random()<.75){this.applyPoison(f,t);this.effect(t,'💉 70 + 독!','skill')}else{this.applyToxin(f,t);this.effect(t,'💉 70 + 맹독!','skill')}}}",
'doctor skill')
once("if(f.id==='doctor')return '👨‍⚕️ 💉 적 70+독 · 아군 +30+약물치료';",
     "if(f.id==='doctor')return '👨‍⚕️ 💉 적 70 · 독 75% / 맹독 25% · 아군 +30+약물치료';",
     'doctor ability')
s=s.replace("💉 적 80+독 · 아군 +50+약물치료 · 클리어 시 의사 10% 획득","💉 적 70 · 독 75% / 맹독 25% · 아군 +30+약물치료 · 클리어 시 의사 10% 획득")
s=s.replace("의사의 💉 주사기는 적에게 70+독, 아군에게 +30 및 3초 약물치료.","의사의 💉 주사기는 적에게 70 피해 후 독 75% / 맹독 25%, 아군에게 +30 및 3초 약물치료.")

# Code / booster storage
once(
"const STAGE_SKIP_KEY='neonRumble.stageSkipTickets.v1',FORGE_JOB_KEY='neonRumble.craftJob.v1',FAST_SPEED_KEY='neonRumble.fastSpeedUnlocked.v1';",
"const STAGE_SKIP_KEY='neonRumble.stageSkipTickets.v1',FORGE_JOB_KEY='neonRumble.craftJob.v1',FAST_SPEED_KEY='neonRumble.fastSpeedUnlocked.v1',COIN_BOOST_TICKET_KEY='neonRumble.coinBoostTickets.v1',COIN_BOOST_UNTIL_KEY='neonRumble.coinBoostUntil.v1';",
'boost keys')
once(
"let stageSkipTickets=0,craftJob=null,fastSpeedUnlocked=false;try{stageSkipTickets=Math.max(0,parseInt(localStorage.getItem(STAGE_SKIP_KEY)||'0',10)||0);craftJob=JSON.parse(localStorage.getItem(FORGE_JOB_KEY)||'null');fastSpeedUnlocked=localStorage.getItem(FAST_SPEED_KEY)==='1'}catch{}",
"let stageSkipTickets=0,craftJob=null,fastSpeedUnlocked=false,coinBoostTickets=0,coinBoostUntil=0;try{stageSkipTickets=Math.max(0,parseInt(localStorage.getItem(STAGE_SKIP_KEY)||'0',10)||0);craftJob=JSON.parse(localStorage.getItem(FORGE_JOB_KEY)||'null');fastSpeedUnlocked=localStorage.getItem(FAST_SPEED_KEY)==='1';coinBoostTickets=Math.max(0,parseInt(localStorage.getItem(COIN_BOOST_TICKET_KEY)||'0',10)||0);coinBoostUntil=Math.max(0,parseInt(localStorage.getItem(COIN_BOOST_UNTIL_KEY)||'0',10)||0)}catch{}",
'boost load')
once(
"const CODE_VALUES={neon67:'coins',itisme13666:'demon',skip82:'skip',ninja4:'ninjaSkin',fast8282:'fastSpeed'};",
"const CODE_VALUES={neon67:'coins',itisme13666:'demon',skip82:'skip',ninja4:'ninjaSkin',fast8282:'fastSpeed','what?':'demonSkin',fight787:'boxerSkin',lucky777:'coinBoost'};",
'codes')

# New code-only skins
once(
"{id:'skin_ninja_mask',name:'마스크닌자 스킨',icon:'👺',price:0,type:'skin',skinFor:'ninja',skinTarget:'fighter',exclusiveFor:'ninja',codeOnly:true,desc:'🥷 닌자 전용 비밀 스킨'},",
"{id:'skin_ninja_mask',name:'마스크닌자 스킨',icon:'👺',price:0,type:'skin',skinFor:'ninja',skinTarget:'fighter',exclusiveFor:'ninja',codeOnly:true,desc:'🥷 닌자 전용 비밀 스킨'},\n {id:'skin_demon_mark',name:'악마 스킨',icon:'𖤍',price:0,type:'skin',skinFor:'hell_demon',skinTarget:'fighter',exclusiveFor:'hell_demon',codeOnly:true,desc:'👿 악마 전용 비밀 스킨'},\n {id:'skin_boxer_master',name:'사부 스킨',icon:'🫡',price:0,type:'skin',skinFor:'boxer',skinTarget:'fighter',exclusiveFor:'boxer',codeOnly:true,desc:'🥊 복서 전용 사부 스킨'},",
'skins')

# Central coin reward / 10-minute consumable
once(
"function updateCoinUI(){if($('coin-count'))$('coin-count').textContent=coins;if($('header-coins'))$('header-coins').textContent='🪙 '+coins}\nfunction awardStageCoins(n){const reward=n===3?50:1+Math.floor(Math.random()*30);coins+=reward;saveEconomy();updateCoinUI();return reward}",
"""function coinBoostActive(){return coinBoostUntil>Date.now()}
function coinBoostRemaining(){return Math.max(0,coinBoostUntil-Date.now())}
function saveCoinBoostState(){try{localStorage.setItem(COIN_BOOST_TICKET_KEY,String(coinBoostTickets));if(coinBoostUntil>0)localStorage.setItem(COIN_BOOST_UNTIL_KEY,String(coinBoostUntil));else localStorage.removeItem(COIN_BOOST_UNTIL_KEY)}catch{}}
function updateCoinUI(){if(coinBoostUntil&&!coinBoostActive()){coinBoostUntil=0;saveCoinBoostState()}if($('coin-count'))$('coin-count').textContent=coins;if($('header-coins')){let t='🪙 '+coins;if(coinBoostActive()){const sec=Math.ceil(coinBoostRemaining()/1000),m=Math.floor(sec/60),ss=String(sec%60).padStart(2,'0');t+=' · ⚡2× '+m+':'+ss}$('header-coins').textContent=t}}
function grantCoins(amount){const base=Math.max(0,Math.floor(Number(amount)||0)),actual=base*(coinBoostActive()?2:1);coins+=actual;saveEconomy();updateCoinUI();return actual}
function grantCoinBoostTicket(n=1){coinBoostTickets=Math.max(0,coinBoostTickets+Math.max(0,Math.floor(n)));saveCoinBoostState();renderWardrobe();return coinBoostTickets}
function activateCoinBoost(){if(coinBoostActive()){alert('⚡ 코인 2배가 이미 적용 중이야.');return false}if(coinBoostTickets<=0){alert('코인 2배 획득권이 없어!');return false}coinBoostTickets--;coinBoostUntil=Date.now()+10*60*1000;saveCoinBoostState();updateCoinUI();renderWardrobe();alert('⚡ 코인 2배 획득권 사용! 10분 동안 모든 코인 획득량이 2배!');return true}
function awardStageCoins(n){const reward=n===3?50:1+Math.floor(Math.random()*30);return grantCoins(reward)}""",
'coin grant')

# Redeem codes, including booster (neon67 now honors active 2x)
old="function redeemSecretCode(raw){const code=String(raw||'').trim().toLowerCase(),out=$('code-result');if(!CODE_VALUES[code]){if(out)out.textContent='❌ 존재하지 않는 코드야.';return false}if(redeemedCodes.has(code)){if(out)out.textContent='⚠️ 이미 사용한 코드야.';return false}if(code==='neon67'){coins+=666;saveEconomy();updateCoinUI();if(out)out.textContent='✅ 코드 적용 완료 · 🪙 666코인 획득!'}else if(code==='skip82'){stageSkipTickets+=10;try{localStorage.setItem(STAGE_SKIP_KEY,String(stageSkipTickets))}catch{}renderWardrobe();if(out)out.textContent='✅ 코드 적용 완료 · 🎫 스테이지 스킵권 10개 획득!'}else if(code==='itisme13666'){hellDemonUnlocked=true;try{localStorage.setItem(HELL_DEMON_UNLOCK_KEY,'1')}catch{}refreshUnlockCards();if(out)out.textContent='✅ 코드 적용 완료 · 👿 악마가 샌드박스에 해금됐어!'}else if(code==='ninja4'){if(!ownedCosmetics.includes('skin_ninja_mask'))ownedCosmetics.push('skin_ninja_mask');saveEconomy();renderWardrobe();renderShop();updateSelection();if(out)out.textContent='✅ 코드 적용 완료 · 👺 마스크닌자 스킨 획득!'}else if(code==='fast8282'){fastSpeedUnlocked=true;try{localStorage.setItem(FAST_SPEED_KEY,'1')}catch{}updateSpeedUnlockUI();if(out)out.textContent='✅ 코드 적용 완료 · ⏩ 5× / 10× 전투 배속 해금!'}redeemedCodes.add(code);saveRedeemedCodes();return true}"
new="function redeemSecretCode(raw){const code=String(raw||'').trim().toLowerCase(),out=$('code-result');if(!CODE_VALUES[code]){if(out)out.textContent='❌ 존재하지 않는 코드야.';return false}if(redeemedCodes.has(code)){if(out)out.textContent='⚠️ 이미 사용한 코드야.';return false}if(code==='neon67'){const won=grantCoins(666);if(out)out.textContent='✅ 코드 적용 완료 · 🪙 '+won+'코인 획득!'}else if(code==='skip82'){stageSkipTickets+=10;try{localStorage.setItem(STAGE_SKIP_KEY,String(stageSkipTickets))}catch{}renderWardrobe();if(out)out.textContent='✅ 코드 적용 완료 · 🎫 스테이지 스킵권 10개 획득!'}else if(code==='itisme13666'){hellDemonUnlocked=true;try{localStorage.setItem(HELL_DEMON_UNLOCK_KEY,'1')}catch{}refreshUnlockCards();if(out)out.textContent='✅ 코드 적용 완료 · 👿 악마가 샌드박스에 해금됐어!'}else if(code==='ninja4'){if(!ownedCosmetics.includes('skin_ninja_mask'))ownedCosmetics.push('skin_ninja_mask');saveEconomy();renderWardrobe();renderShop();updateSelection();if(out)out.textContent='✅ 코드 적용 완료 · 👺 마스크닌자 스킨 획득!'}else if(code==='fast8282'){fastSpeedUnlocked=true;try{localStorage.setItem(FAST_SPEED_KEY,'1')}catch{}updateSpeedUnlockUI();if(out)out.textContent='✅ 코드 적용 완료 · ⏩ 5× / 10× 전투 배속 해금!'}else if(code==='what?'){if(!ownedCosmetics.includes('skin_demon_mark'))ownedCosmetics.push('skin_demon_mark');saveEconomy();renderWardrobe();renderShop();updateSelection();if(out)out.textContent='✅ 코드 적용 완료 · 𖤍 악마 스킨 획득!'}else if(code==='fight787'){if(!ownedCosmetics.includes('skin_boxer_master'))ownedCosmetics.push('skin_boxer_master');saveEconomy();renderWardrobe();renderShop();updateSelection();if(out)out.textContent='✅ 코드 적용 완료 · 🫡 사부 스킨 획득!'}else if(code==='lucky777'){grantCoinBoostTicket(1);if(out)out.textContent='✅ 코드 적용 완료 · 🎟️ 코인 2배 획득권 1장 획득!'}redeemedCodes.add(code);saveRedeemedCodes();return true}"
once(old,new,'redeem')

# Coin box reward honors boost
once("if(id==='coin_box'){const reward=10+Math.floor(Math.random()*991);coins+=reward;saveEconomy();updateCoinUI();alert('📦 랜덤 코인상자 개봉! 🪙 '+reward+'코인 획득!')}",
     "if(id==='coin_box'){const reward=10+Math.floor(Math.random()*991),won=grantCoins(reward);alert('📦 랜덤 코인상자 개봉! 🪙 '+won+'코인 획득!')}",
     'coin box')

# Wardrobe booster ticket / active state
old="box.innerHTML='';if(stageSkipTickets>0){const tr=document.createElement('div');tr.className='wardrobe-item';"
new="box.innerHTML='';if(coinBoostTickets>0||coinBoostActive()){const br=document.createElement('div');br.className='wardrobe-item';const rem=coinBoostActive()?Math.ceil(coinBoostRemaining()/1000):0,mm=Math.floor(rem/60),ss=String(rem%60).padStart(2,'0');br.innerHTML='<span class=\"item-icon\">🎟️</span><span><strong>코인 2배 획득권 ×'+coinBoostTickets+'</strong><small>'+(coinBoostActive()?'⚡ 사용 중 · '+mm+':'+ss+' 남음':'사용하면 10분 동안 모든 코인 획득량 2배')+'</small><span class=\"item-type\">소모품</span></span>';const bb=document.createElement('button');bb.type='button';bb.textContent=coinBoostActive()?'사용 중':'10분 사용';bb.disabled=coinBoostActive()||coinBoostTickets<=0;bb.onclick=activateCoinBoost;br.appendChild(bb);box.appendChild(br)}if(stageSkipTickets>0){const tr=document.createElement('div');tr.className='wardrobe-item';"
once(old,new,'wardrobe boost row')
once("if(!items.length&&stageSkipTickets<=0){box.innerHTML='<div class=\"economy-empty\">아직 보유한 꾸미기 아이템이 없어. 상점에서 구매해 봐.</div>';return}",
     "if(!items.length&&stageSkipTickets<=0&&coinBoostTickets<=0&&!coinBoostActive()){box.innerHTML='<div class=\"economy-empty\">아직 보유한 꾸미기 아이템이 없어. 상점에서 구매해 봐.</div>';return}",
     'wardrobe empty')

# Casino 15% booster, loss becomes 15%; duplicate coin payouts honor booster
s=s.replace("const pool=['🎰','👒','🪙','🥽','🫟','🛴','🦽','🍀','⭐️','🥇','🥈','🥉','🤑','💎','❌'];","const pool=['🎰','👒','🪙','🥽','🫟','🛴','🦽','🍀','⭐️','🥇','🥈','🥉','🤑','💎','🎟️','❌'];")
once("if(dup){coins+=150;text=item.icon+' '+item.name+' 중복! 대신 🪙 150코인 획득!'}",
     "if(dup){const won=grantCoins(150);text=item.icon+' '+item.name+' 중복! 대신 🪙 '+won+'코인 획득!'}",
     'casino cosmetic dup')
once("if(dup){coins+=200;text=(item?item.icon:'🎰')+' '+(item?item.name:'캐릭터')+' 중복! 대신 🪙 200코인 획득!'}",
     "if(dup){const won=grantCoins(200);text=(item?item.icon:'🎰')+' '+(item?item.name:'캐릭터')+' 중복! 대신 🪙 '+won+'코인 획득!'}",
     'casino char dup')
once("else if(r<.70){casinoShowReels('🎫');grantStageSkipTicket(1);text='🎫 스테이지 스킵권 획득! 현재 '+stageSkipTickets+'장 보유.'}else{casinoShowReels('❌');text='아쉽다! 이번에는 꽝이야.'}",
     "else if(r<.70){casinoShowReels('🎫');grantStageSkipTicket(1);text='🎫 스테이지 스킵권 획득! 현재 '+stageSkipTickets+'장 보유.'}else if(r<.85){casinoShowReels('🎟️');grantCoinBoostTicket(1);text='🎟️ 코인 2배 획득권 획득! 옷장에서 10분 동안 사용할 수 있어.'}else{casinoShowReels('❌');text='아쉽다! 이번에는 꽝이야.'}",
     'casino odds')

# Forge / Hell bonus coins honor boost
once("const baseReward=awardStageCoins(forgeStageNo),bonus=forgeStageNo===3?100:0;if(bonus){coins+=bonus;saveEconomy();updateCoinUI()}",
     "const baseReward=awardStageCoins(forgeStageNo),bonus=forgeStageNo===3?grantCoins(100):0;",
     'forge reward')
once("(bonus?' · 👑 왕도깨비 추가 보상 🪙 100코인! · 총 150코인':'')",
     "(bonus?' · 👑 왕도깨비 추가 보상 🪙 '+bonus+'코인! · 총 '+(baseReward+bonus)+'코인':'')",
     'forge reward text')
once("const coinReward=awardStageCoins(hellStageNo),hellBonus=hellStageNo===3?150:0;if(hellBonus){coins+=hellBonus;saveEconomy();updateCoinUI()}",
     "const coinReward=awardStageCoins(hellStageNo),hellBonus=hellStageNo===3?grantCoins(150):0;",
     'hell reward')
once("(hellBonus?' · 👿 STAGE 3 추가 보상 🪙 150코인 · 총 '+(coinReward+hellBonus)+'코인':'')",
     "(hellBonus?' · 👿 STAGE 3 추가 보상 🪙 '+hellBonus+'코인 · 총 '+(coinReward+hellBonus)+'코인':'')",
     'hell reward text')

# Tutorial casino odds
s=s.replace("꾸미기 30%, 캐릭터 10%, 스테이지 스킵권 30%, 꽝 30%야.","꾸미기 30%, 캐릭터 10%, 스테이지 스킵권 30%, 코인 2배 획득권 15%, 꽝 15%야.")

# Devil dialogue expansion and code whispers; demon unlock stays rarest
once(
" '오늘은 아무것도 안 알려 주겠다. 그것도 하나의 대답이지.'",
" '오늘은 아무것도 안 알려 주겠다. 그것도 하나의 대답이지.',\n '의사는 독과 맹독 사이에서도 침착해야 하지.',\n '가면 하나로 사람이 달라 보이는 법이다.',\n '행운은 오래 머무르지 않는다. 잡았다면 바로 써라.',\n '두 배의 보상은 두 배의 욕심도 데려오지.',\n '사부의 얼굴을 빌려 싸우는 것도 꽤 우습겠군.',\n '악마에게도 다른 얼굴이 있다는 걸 믿나?',\n '도박장은 패배만 주는 곳이 아니다. 아주 가끔 시간을 사 주지.',\n '십 분은 짧다. 하지만 코인을 모으기에는 충분할 수도 있지.'",
'devil lines')
old="if(r<.003)line='…정말 여기까지 들었군. itisme13666';else if(r<.011)line='가면을 원하는 닌자가 있다면 기억해라. ninja4';else if(r<.023)line='시간을 더 빠르게 흘리고 싶나? fast8282';else if(r<.038)line='지옥의 문에는 숫자가 새겨져 있지. skip82';else if(r<.063)line='네온빛 속에서 이런 글자를 본 적 있나? neon67';else line=DEVIL_TALK_LINES[Math.floor(Math.random()*DEVIL_TALK_LINES.length)]"
new="if(r<.003)line='…정말 여기까지 들었군. itisme13666';else if(r<.009)line='내 얼굴이 하나뿐이라고 생각했나? what?';else if(r<.017)line='복서에게는 오래된 사부의 그림자가 있지. fight787';else if(r<.027)line='행운은 오래 머물지 않아. lucky777';else if(r<.038)line='가면을 원하는 닌자가 있다면 기억해라. ninja4';else if(r<.052)line='시간을 더 빠르게 흘리고 싶나? fast8282';else if(r<.070)line='지옥의 문에는 숫자가 새겨져 있지. skip82';else if(r<.095)line='네온빛 속에서 이런 글자를 본 적 있나? neon67';else line=DEVIL_TALK_LINES[Math.floor(Math.random()*DEVIL_TALK_LINES.length)]"
once(old,new,'devil whispers')

# Periodic countdown refresh
once("requestAnimationFrame(loop);\nif(document.modelContext?.registerTool)",
     "requestAnimationFrame(loop);setInterval(()=>{if(coinBoostUntil)updateCoinUI();const wp=$('wardrobe-panel');if(wp&&!wp.hidden&&(coinBoostTickets>0||coinBoostActive()))renderWardrobe()},1000);\nif(document.modelContext?.registerTool)",
     'boost timer')

p.write_text(s,encoding='utf-8')
print('v3.75 patch applied')

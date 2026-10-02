from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1, got {n}')
    s=s.replace(old,new,1)

# Version + patch notes
once('BATTLE <b>v3.75</b>','BATTLE <b>v3.76</b>','version')
once(
'<summary>📒 패치노트 · v3.75</summary><div class="patch-body">',
'<summary>📒 패치노트 · v3.76</summary><div class="patch-body"><div class="patch-version"><h3>v3.76 · 악마의 한마디 확장</h3><ul><li>👿 악마의 한마디에서 비밀 코드가 등장하는 전체 확률을 크게 상향.</li><li>😘 사랑의 남자, 🌚 달의 새로운 비밀 스킨 추가.</li><li>༼☠︎༽ 캐릭터가 쓰러진 자리에 무덤을 남기는 비밀 효과 추가.</li><li>👿 악마의 일반 대사를 추가.</li></ul></div>',
'patch notes')

# Secret state
once(
"const STAGE_SKIP_KEY='neonRumble.stageSkipTickets.v1',FORGE_JOB_KEY='neonRumble.craftJob.v1',FAST_SPEED_KEY='neonRumble.fastSpeedUnlocked.v1',COIN_BOOST_TICKET_KEY='neonRumble.coinBoostTickets.v1',COIN_BOOST_UNTIL_KEY='neonRumble.coinBoostUntil.v1';",
"const STAGE_SKIP_KEY='neonRumble.stageSkipTickets.v1',FORGE_JOB_KEY='neonRumble.craftJob.v1',FAST_SPEED_KEY='neonRumble.fastSpeedUnlocked.v1',COIN_BOOST_TICKET_KEY='neonRumble.coinBoostTickets.v1',COIN_BOOST_UNTIL_KEY='neonRumble.coinBoostUntil.v1',GRAVE_FX_KEY='neonRumble.graveFxUnlocked.v1';",
'grave key')
once(
"let stageSkipTickets=0,craftJob=null,fastSpeedUnlocked=false,coinBoostTickets=0,coinBoostUntil=0;try{stageSkipTickets=Math.max(0,parseInt(localStorage.getItem(STAGE_SKIP_KEY)||'0',10)||0);craftJob=JSON.parse(localStorage.getItem(FORGE_JOB_KEY)||'null');fastSpeedUnlocked=localStorage.getItem(FAST_SPEED_KEY)==='1';coinBoostTickets=Math.max(0,parseInt(localStorage.getItem(COIN_BOOST_TICKET_KEY)||'0',10)||0);coinBoostUntil=Math.max(0,parseInt(localStorage.getItem(COIN_BOOST_UNTIL_KEY)||'0',10)||0)}catch{}",
"let stageSkipTickets=0,craftJob=null,fastSpeedUnlocked=false,coinBoostTickets=0,coinBoostUntil=0,graveFxUnlocked=false;try{stageSkipTickets=Math.max(0,parseInt(localStorage.getItem(STAGE_SKIP_KEY)||'0',10)||0);craftJob=JSON.parse(localStorage.getItem(FORGE_JOB_KEY)||'null');fastSpeedUnlocked=localStorage.getItem(FAST_SPEED_KEY)==='1';coinBoostTickets=Math.max(0,parseInt(localStorage.getItem(COIN_BOOST_TICKET_KEY)||'0',10)||0);coinBoostUntil=Math.max(0,parseInt(localStorage.getItem(COIN_BOOST_UNTIL_KEY)||'0',10)||0);graveFxUnlocked=localStorage.getItem(GRAVE_FX_KEY)==='1'}catch{}",
'grave state')

# Code registry
once(
"const CODE_VALUES={neon67:'coins',itisme13666:'demon',skip82:'skip',ninja4:'ninjaSkin',fast8282:'fastSpeed','what?':'demonSkin',fight787:'boxerSkin',lucky777:'coinBoost'};",
"const CODE_VALUES={neon67:'coins',itisme13666:'demon',skip82:'skip',ninja4:'ninjaSkin',fast8282:'fastSpeed','what?':'demonSkin',fight787:'boxerSkin',lucky777:'coinBoost',lovehate85:'loveSkin',darkmoon135:'moonSkin',dathisgood55:'graveFx'};",
'code registry')

# New code-only skins
once(
"{id:'skin_boxer_master',name:'사부 스킨',icon:'🫡',price:0,type:'skin',skinFor:'boxer',skinTarget:'fighter',exclusiveFor:'boxer',codeOnly:true,desc:'🥊 복서 전용 사부 스킨'},",
"{id:'skin_boxer_master',name:'사부 스킨',icon:'🫡',price:0,type:'skin',skinFor:'boxer',skinTarget:'fighter',exclusiveFor:'boxer',codeOnly:true,desc:'🥊 복서 전용 사부 스킨'},\n {id:'skin_loveman_kiss',name:'사랑의 남자 스킨',icon:'😘',price:0,type:'skin',skinFor:'loveman',skinTarget:'fighter',exclusiveFor:'loveman',codeOnly:true,desc:'😍 사랑의 남자 전용 비밀 스킨'},\n {id:'skin_moon_newmoon',name:'신월 스킨',icon:'🌚',price:0,type:'skin',skinFor:'moon',skinTarget:'fighter',exclusiveFor:'moon',codeOnly:true,desc:'🌝 달 전용 비밀 스킨 · 신월'},",
'new skins')

# Extend redeem
old="else if(code==='lucky777'){grantCoinBoostTicket(1);if(out)out.textContent='✅ 코드 적용 완료 · 🎟️ 코인 2배 획득권 1장 획득!'}redeemedCodes.add(code);"
new="else if(code==='lucky777'){grantCoinBoostTicket(1);if(out)out.textContent='✅ 코드 적용 완료 · 🎟️ 코인 2배 획득권 1장 획득!'}else if(code==='lovehate85'){if(!ownedCosmetics.includes('skin_loveman_kiss'))ownedCosmetics.push('skin_loveman_kiss');saveEconomy();renderWardrobe();renderShop();updateSelection();if(out)out.textContent='✅ 코드 적용 완료 · 😘 사랑의 남자 스킨 획득!'}else if(code==='darkmoon135'){if(!ownedCosmetics.includes('skin_moon_newmoon'))ownedCosmetics.push('skin_moon_newmoon');saveEconomy();renderWardrobe();renderShop();updateSelection();if(out)out.textContent='✅ 코드 적용 완료 · 🌚 신월 스킨 획득!'}else if(code==='dathisgood55'){graveFxUnlocked=true;try{localStorage.setItem(GRAVE_FX_KEY,'1')}catch{}if(out)out.textContent='✅ 코드 적용 완료 · ༼☠︎༽ 사망 위치 무덤 효과 해금!'}redeemedCodes.add(code);"
once(old,new,'redeem new codes')

# Grave tracking + drawing. First observed dead state is ignored so stage dummy fighters do not create graves.
grave_code="""function updateAndDrawGraves(){
 if(!engine||!graveFxUnlocked)return;
 engine.graves=engine.graves||[];
 for(const f of engine.fighters){
  if(f._graveSeen===undefined){f._graveSeen=f.health<=0;continue}
  if(f.health<=0&&!f._graveSeen){engine.graves.push({x:f.x,y:f.y,name:f.name||''});f._graveSeen=true}
  else if(f.health>0)f._graveSeen=false
 }
 for(const g of engine.graves){ctx.save();ctx.globalAlpha=.82;ctx.font='bold 28px system-ui,\"Apple Color Emoji\",\"Segoe UI Emoji\"';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle='#d6d9df';ctx.shadowColor='#000';ctx.shadowBlur=8;ctx.fillText('༼☠︎༽',g.x,g.y);ctx.restore()}
}
"""
once("for(const f of engine.fighters){if(f.id!=='technician'||!Array.isArray(f.techWrenches))continue;",
     grave_code+"updateAndDrawGraves();\nfor(const f of engine.fighters){if(f.id!=='technician'||!Array.isArray(f.techWrenches))continue;",
     'grave renderer')

# More normal dialogue
once(
" '십 분은 짧다. 하지만 코인을 모으기에는 충분할 수도 있지.'",
" '십 분은 짧다. 하지만 코인을 모으기에는 충분할 수도 있지.',\n '사랑과 미움은 생각보다 가까이 붙어 있지.',\n '달이 항상 밝은 얼굴만 보여 주는 것은 아니다.',\n '죽은 자리에는 흔적이 남는 법이다.',\n '비밀이 많아질수록 평범한 말이 더 수상해지지.',\n '네가 찾는 것이 코드인지 대답인지 나도 모르겠군.',\n '무덤은 패배의 표시일까, 다시 싸웠다는 증거일까?',\n '달빛이 사라지는 밤도 있다는 걸 기억해라.',\n '사랑은 웃는 얼굴만 하고 찾아오지 않는다.',\n '오늘은 운이 좋을지도 모르지. 물론 내가 거짓말하는 걸 수도 있고.',\n '코인을 내고 악마의 말을 계속 듣다니, 꽤 끈질긴 인간이군.'",
'devil normal lines')

# New increased probabilities: total secret-code chance 19.9%; demon unlock stays rarest.
old_speak="if(r<.003)line='…정말 여기까지 들었군. itisme13666';else if(r<.009)line='내 얼굴이 하나뿐이라고 생각했나? what?';else if(r<.017)line='복서에게는 오래된 사부의 그림자가 있지. fight787';else if(r<.027)line='행운은 오래 머물지 않아. lucky777';else if(r<.038)line='가면을 원하는 닌자가 있다면 기억해라. ninja4';else if(r<.052)line='시간을 더 빠르게 흘리고 싶나? fast8282';else if(r<.070)line='지옥의 문에는 숫자가 새겨져 있지. skip82';else if(r<.095)line='네온빛 속에서 이런 글자를 본 적 있나? neon67';else line=DEVIL_TALK_LINES[Math.floor(Math.random()*DEVIL_TALK_LINES.length)]"
new_speak="if(r<.008)line='…정말 여기까지 들었군. itisme13666';else if(r<.023)line='내 얼굴이 하나뿐이라고 생각했나? what?';else if(r<.041)line='복서에게는 오래된 사부의 그림자가 있지. fight787';else if(r<.059)line='행운은 오래 머물지 않아. lucky777';else if(r<.077)line='가면을 원하는 닌자가 있다면 기억해라. ninja4';else if(r<.099)line='시간을 더 빠르게 흘리고 싶나? fast8282';else if(r<.124)line='지옥의 문에는 숫자가 새겨져 있지. skip82';else if(r<.154)line='네온빛 속에서 이런 글자를 본 적 있나? neon67';else if(r<.169)line='사랑이 미움으로 바뀌는 순간을 본 적 있나? lovehate85';else if(r<.184)line='달빛이 완전히 숨는 밤에는 이것을 기억해라. darkmoon135';else if(r<.199)line='쓰러진 자리에도 흔적은 남지. dathisgood55';else line=DEVIL_TALK_LINES[Math.floor(Math.random()*DEVIL_TALK_LINES.length)]"
once(old_speak,new_speak,'devil probabilities')

p.write_text(s,encoding='utf-8')
print('v3.76 applied')

from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

# Version + patch notes.
once('BATTLE <b>v3.67</b>','BATTLE <b>v3.68</b>','version badge')
once('<summary>📒 패치노트 · v3.67</summary><div class="patch-body">', '<summary>📒 패치노트 · v3.68</summary><div class="patch-body"><div class="patch-version"><h3>v3.68 · 밸런스 · 스킵권 · 제작소 · 낡은TV</h3><ul><li>🧘‍♂️ 초능력자 HP 750 → 650.</li><li>🎫 스테이지 스킵권 추가. 도박장 30% 확률 또는 상점 500코인 구매. 중복 획득 시 수량 누적, 옷장에서 1회 사용 시 다음 챕터 해금.</li><li>🔨 CHAPTER 7 클리어 시 제작소 해금. 모든 제작은 100코인, 제작시간 1분. 랜덤 코인상자와 📺 낡은TV 제작 가능.</li><li>📺 낡은TV 추가. 3.5초마다 5초간 화면 노이즈가 발생하고, 노이즈 중 0.1~2초 간격으로 🔲 1~3연발. 한 발 피해 40, 탄속은 기본~2배 랜덤.</li></ul></div>', 'patch notes')

# Psychic HP.
once("{id:'psychic',name:'초능력자',icon:'🧘‍♂️',tag:'염력탄 · 벽 밀치기 · 투사체 궤도',hp:750,damage:30,speed:95,cooldown:2,unlock:'psychic'", "{id:'psychic',name:'초능력자',icon:'🧘‍♂️',tag:'염력탄 · 벽 밀치기 · 투사체 궤도',hp:650,damage:30,speed:95,cooldown:2,unlock:'psychic'", 'psychic hp')
s=s.replace("detail:'HP 750 · 염력탄 30 / 2초 + 넉백", "detail:'HP 650 · 염력탄 30 / 2초 + 넉백",1)

# New character.
anchor="{id:'snail',name:'달팽이',icon:'🐌',tag:'초저속 · 초고화력 · 껍질 방어',hp:1000,damage:6767676767,speed:28,cooldown:1,description:'매우 느리게 가장 가까운 적을 계속 추적하며, 적과 접촉하면 즉시 근접 공격 피해 6,767,676,767을 준다. HP 30% 이하가 되면 전투당 1회 5초 동안 껍질에 숨어 받는 피해를 1/5로 줄이고 0.5초마다 HP 20을 회복한다.',detail:'HP 1000 · 이동속도 28 · 접촉 즉시 근접 6,767,676,767 · HP 30% 이하 1회 · 껍질 5초 · 피해 80% 감소 · 0.5초마다 HP 20 회복'},"
oldtv="{id:'old_tv',name:'낡은TV',icon:'📺',tag:'화면 노이즈 · 🔲 연사',hp:1000,damage:40,speed:125,cooldown:0,unlock:'oldTv',description:'3.5초마다 5초 동안 화면에 실제 노이즈가 생긴다. 노이즈 상태에서는 0.1~2초의 무작위 간격으로 🔲을 1~3연발하며, 한 발 피해는 40이고 탄속은 기본~2배 사이에서 무작위로 정해진다.',detail:'HP 1000 · 노이즈 3.5초마다 / 5초 유지 · 🔲 1~3연발 · 발당 40 · 발사 간격 0.1~2초 · 탄속 ×1~2 · CH7 클리어 후 제작소에서 획득'},"
once(anchor,anchor+'\n'+oldtv,'old tv roster')

# Unlock key/state/load/locking.
once("PSYCHIC_UNLOCK_KEY='neonRumble.psychicUnlocked.v1',SHARK_UNLOCK_KEY", "PSYCHIC_UNLOCK_KEY='neonRumble.psychicUnlocked.v1',OLD_TV_UNLOCK_KEY='neonRumble.oldTvUnlocked.v1',SHARK_UNLOCK_KEY", 'oldtv key')
once("psychicUnlocked=false;try{", "psychicUnlocked=false,oldTvUnlocked=false;try{", 'oldtv state')
once("psychicUnlocked=localStorage.getItem(PSYCHIC_UNLOCK_KEY)==='1';", "psychicUnlocked=localStorage.getItem(PSYCHIC_UNLOCK_KEY)==='1';oldTvUnlocked=localStorage.getItem(OLD_TV_UNLOCK_KEY)==='1';", 'oldtv load')
once("(c?.unlock==='psychic'&&!psychicUnlocked)}", "(c?.unlock==='psychic'&&!psychicUnlocked)||(c?.unlock==='oldTv'&&!oldTvUnlocked)}", 'oldtv lock')

# Consumable + forge storage alongside economy.
once("const COIN_KEY='neonRumble.coins.v1',SHOP_OWNED_KEY=", "const STAGE_SKIP_KEY='neonRumble.stageSkipTickets.v1',FORGE_JOB_KEY='neonRumble.craftJob.v1';\nlet stageSkipTickets=0,craftJob=null;try{stageSkipTickets=Math.max(0,parseInt(localStorage.getItem(STAGE_SKIP_KEY)||'0',10)||0);craftJob=JSON.parse(localStorage.getItem(FORGE_JOB_KEY)||'null')}catch{}\nconst COIN_KEY='neonRumble.coins.v1',SHOP_OWNED_KEY=", 'economy keys')
# Add shop ticket.
once("const SHOP_ITEMS=[\n", "const SHOP_ITEMS=[\n {id:'stage_skip_ticket',name:'스테이지 스킵권',icon:'🎫',price:500,type:'consumable',exclusiveFor:null,desc:'옷장에서 1회 사용하면 다음 챕터 즉시 해금 · 수량 중첩'},\n", 'ticket shop item')

# Economy helpers inserted after awardStageCoins.
anchor="function awardStageCoins(n){const reward=n===3?50:1+Math.floor(Math.random()*30);coins+=reward;saveEconomy();updateCoinUI();return reward}"
extra=r'''function saveStageSkipTickets(){try{localStorage.setItem(STAGE_SKIP_KEY,String(stageSkipTickets))}catch{}}
function grantStageSkipTicket(n=1){stageSkipTickets=Math.max(0,stageSkipTickets+n);saveStageSkipTickets();renderWardrobe();renderShop();return stageSkipTickets}
function unlockNextChapterByTicket(){if(stageSkipTickets<=0){alert('스테이지 스킵권이 없어!');return}let label='';if(!chapter2Unlocked()){robotStageMask=7;localStorage.setItem(ROBOT_STAGE_KEY,'7');label='CHAPTER 2'}else if(!chapter3Unlocked()){desertStageMask=7;localStorage.setItem(DESERT_STAGE_KEY,'7');label='CHAPTER 3'}else if(!chapter4Unlocked()){mansionStageMask=7;localStorage.setItem(MANSION_STAGE_KEY,'7');label='CHAPTER 4'}else if(!chapter5Unlocked()){spaceStageMask=7;localStorage.setItem(SPACE_STAGE_KEY,'7');label='CHAPTER 5'}else if(!chapter6Unlocked()){casinoStageMask=7;localStorage.setItem(CASINO_STAGE_KEY,'7');label='CHAPTER 6'}else if(!chapter7Unlocked()){oceanStageMask=7;localStorage.setItem(OCEAN_STAGE_KEY,'7');label='CHAPTER 7'}else if(!chapter8Unlocked()){forgeStageMask=7;localStorage.setItem(FORGE_STAGE_KEY,'7');label='CHAPTER 8'}else{alert('현재 해금할 다음 챕터가 없어!');return}stageSkipTickets--;saveStageSkipTickets();updateChapter2UI();updateChapter3UI();updateChapter4UI();updateChapter5UI();updateChapter6UI();updateChapter7UI();updateChapter8UI();updateForgeSystemUI();renderWardrobe();renderShop();alert('🎫 스킵권 사용! '+label+' 해금!')}
function saveCraftJob(){try{if(craftJob)localStorage.setItem(FORGE_JOB_KEY,JSON.stringify(craftJob));else localStorage.removeItem(FORGE_JOB_KEY)}catch{}}
function craftSystemUnlocked(){return chapter8Unlocked()}
function craftRemaining(){return craftJob?Math.max(0,craftJob.readyAt-Date.now()):0}
function startCraft(id){if(!craftSystemUnlocked()){alert('CHAPTER 7을 먼저 클리어해야 해!');return}if(craftJob){alert('이미 제작 중인 아이템이 있어!');return}if(coins<100){alert('제작에는 100코인이 필요해!');return}if(!['coin_box','old_tv'].includes(id))return;coins-=100;craftJob={id,readyAt:Date.now()+60000};saveEconomy();saveCraftJob();updateCoinUI();renderForgeSystem()}
function claimCraft(){if(!craftJob)return;if(craftRemaining()>0){alert('아직 제작 중이야!');return}const id=craftJob.id;craftJob=null;saveCraftJob();if(id==='coin_box'){const reward=10+Math.floor(Math.random()*991);coins+=reward;saveEconomy();updateCoinUI();alert('📦 랜덤 코인상자 개봉! 🪙 '+reward+'코인 획득!')}else if(id==='old_tv'){if(!oldTvUnlocked){oldTvUnlocked=true;try{localStorage.setItem(OLD_TV_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();alert('📺 낡은TV 획득!')}else alert('📺 낡은TV는 이미 보유 중이야.')}renderForgeSystem()}
function renderForgeSystem(){const p=$('craft-system-panel'),b=$('craft-system-btn');if(!p||!b)return;const ok=craftSystemUnlocked();b.disabled=!ok;b.textContent=ok?'🔨 제작소':'🔒 제작소 · CHAPTER 7 클리어 필요';const status=$('craft-status');if(status){if(!craftJob)status.textContent='제작 대기 중';else{const rem=Math.ceil(craftRemaining()/1000);status.textContent=rem>0?'제작 중 · '+rem+'초 남음':'제작 완료 · 획득 가능'}}for(const x of p.querySelectorAll('[data-craft]'))x.disabled=!ok||!!craftJob||coins<100;const claim=$('craft-claim');if(claim)claim.disabled=!craftJob||craftRemaining()>0}
function setupForgeSystemUI(){const bar=document.querySelector('.economy-bar');if(!bar||$('craft-system-btn'))return;const b=document.createElement('button');b.id='craft-system-btn';b.type='button';bar.appendChild(b);const p=document.createElement('div');p.id='craft-system-panel';p.className='economy-panel';p.hidden=true;p.innerHTML='<h2>🔨 제작소</h2><p>CHAPTER 7 클리어 시 사용 가능 · 모든 제작 100코인 · 제작시간 1분</p><div class="shop-grid"><div class="shop-item"><span class="item-icon">📦</span><span><strong>랜덤 코인상자</strong><small>완성 후 10~1000코인 무작위 획득</small></span><button type="button" data-craft="coin_box">100코인 제작</button></div><div class="shop-item"><span class="item-icon">📺</span><span><strong>낡은TV</strong><small>신규 캐릭터 영구 해금</small></span><button type="button" data-craft="old_tv">100코인 제작</button></div></div><p id="craft-status" class="casino-result">제작 대기 중</p><button id="craft-claim" type="button">완성품 획득</button>';bar.parentNode.insertBefore(p,bar.nextSibling);b.onclick=()=>{p.hidden=!p.hidden;renderForgeSystem()};for(const x of p.querySelectorAll('[data-craft]'))x.onclick=()=>startCraft(x.dataset.craft);$('craft-claim').onclick=claimCraft;setInterval(()=>{if(!p.hidden)renderForgeSystem()},500);renderForgeSystem()}
'''
once(anchor,anchor+'\n'+extra,'economy feature helpers')

# Buy ticket special-case.
once("function buyCosmetic(id){const item=SHOP_ITEMS.find(x=>x.id===id);if(!item||ownedCosmetics.includes(id))return;", "function buyCosmetic(id){const item=SHOP_ITEMS.find(x=>x.id===id);if(!item)return;if(item.id==='stage_skip_ticket'){if(coins<item.price){alert('코인이 부족해!');return}coins-=item.price;grantStageSkipTicket(1);saveEconomy();updateCoinUI();renderShop();return}if(ownedCosmetics.includes(id))return;", 'ticket purchase')

# Shop rendering special ownership/count.
once("const own=ownedCosmetics.includes(item.id),row=document.createElement('div');", "const own=item.id==='stage_skip_ticket'?false:ownedCosmetics.includes(item.id),row=document.createElement('div');", 'shop own')
once("b.textContent=own?'보유 중':locked?'챕터 클리어 필요':'구매';b.disabled=own||locked;", "b.textContent=item.id==='stage_skip_ticket'?'구매 ('+stageSkipTickets+'장 보유)':own?'보유 중':locked?'챕터 클리어 필요':'구매';b.disabled=(item.id!=='stage_skip_ticket'&&own)||locked;", 'shop button')

# Wardrobe ticket row and avoid consumable in cosmetics list.
once("box.innerHTML='';const items=SHOP_ITEMS.filter(x=>ownedCosmetics.includes(x.id)&&x.type!=='character');", "box.innerHTML='';if(stageSkipTickets>0){const tr=document.createElement('div');tr.className='wardrobe-item';tr.innerHTML='<span class=\"item-icon\">🎫</span><span><strong>스테이지 스킵권 ×'+stageSkipTickets+'</strong><small>1회 사용하면 다음 챕터가 즉시 해금됨</small><span class=\"item-type\">소모품</span></span>';const tb=document.createElement('button');tb.type='button';tb.textContent='사용';tb.onclick=unlockNextChapterByTicket;tr.appendChild(tb);box.appendChild(tr)}const items=SHOP_ITEMS.filter(x=>ownedCosmetics.includes(x.id)&&x.type!=='character'&&x.type!=='consumable');", 'wardrobe ticket')
once("if(!items.length){box.innerHTML='<div class=\"economy-empty\">아직 보유한 꾸미기 아이템이 없어. 상점에서 구매해 봐.</div>';return}", "if(!items.length&&stageSkipTickets<=0){box.innerHTML='<div class=\"economy-empty\">아직 보유한 꾸미기 아이템이 없어. 상점에서 구매해 봐.</div>';return}", 'wardrobe empty')

# Casino: cosmetics 30, chars 10, skip ticket 30, miss 30.
old="}else if(r<.40){const id=CASINO_CHARACTER_IDS[Math.floor(Math.random()*CASINO_CHARACTER_IDS.length)],item=SHOP_ITEMS.find(x=>x.id===id),dup=casinoCharacterOwned(id);casinoShowReels(item?item.icon:'🎰');if(dup){coins+=200;text=(item?item.icon:'🎰')+' '+(item?item.name:'캐릭터')+' 중복! 대신 🪙 200코인 획득!'}else{grantCasinoCharacter(id);text=(item?item.icon:'🎰')+' '+(item?item.name:'캐릭터')+' 캐릭터 획득!'}}else{casinoShowReels('❌');text='아쉽다! 이번에는 꽝이야.'}"
new="}else if(r<.40){const id=CASINO_CHARACTER_IDS[Math.floor(Math.random()*CASINO_CHARACTER_IDS.length)],item=SHOP_ITEMS.find(x=>x.id===id),dup=casinoCharacterOwned(id);casinoShowReels(item?item.icon:'🎰');if(dup){coins+=200;text=(item?item.icon:'🎰')+' '+(item?item.name:'캐릭터')+' 중복! 대신 🪙 200코인 획득!'}else{grantCasinoCharacter(id);text=(item?item.icon:'🎰')+' '+(item?item.name:'캐릭터')+' 캐릭터 획득!'}}else if(r<.70){casinoShowReels('🎫');grantStageSkipTicket(1);text='🎫 스테이지 스킵권 획득! 현재 '+stageSkipTickets+'장 보유.'}else{casinoShowReels('❌');text='아쉽다! 이번에는 꽝이야.'}"
once(old,new,'casino ticket odds')

# Old TV skill before psychic skill.
anchor="psychicSkill(f,e){"
oldtvskill=r'''oldTvSkill(f,e){
 if(!f||f.id!=='old_tv'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0)return;
 if(f.oldTvNoiseNext===undefined){f.oldTvNoiseNext=this.time+3.5/f.scale;f.oldTvNoiseUntil=0;f.oldTvShotNext=Infinity}
 if(this.time>=f.oldTvNoiseNext-1e-9){f.oldTvNoiseNext=this.time+3.5/f.scale;f.oldTvNoiseUntil=this.time+5/f.scale;f.oldTvShotNext=this.time+this.rand(.1,2)/f.scale}
 if(this.time<(f.oldTvNoiseUntil||0)-1e-9&&this.time>=f.oldTvShotNext-1e-9){const count=1+Math.floor(this.random()*3),base=Math.atan2(e.y-f.y,e.x-f.x);for(let i=0;i<count;i++){const spread=(i-(count-1)/2)*.10,ang=base+spread,vx=Math.cos(ang),vy=Math.sin(ang),speed=300*(1+this.random())*f.scale;this.shots.push({x:f.x+vx*(f.radius+10),y:f.y+vy*(f.radius+10),vx,vy,owner:f.side,team:f.team,target:e.side,kind:'oldtv_square',icon:'🔲',radius:8*f.scale,speed,damage:40*f.scale,life:4/f.scale,bounces:0})}f.oldTvShotNext=this.time+this.rand(.1,2)/f.scale;f.attack=.12/f.scale}
}
'''
once(anchor,oldtvskill+anchor,'oldtv skill')
# Call skill.
once("if(f.id==='psychic'){this.psychicMaintainRange(f,e,dt);this.psychicSkill(f,e)}", "if(f.id==='psychic'){this.psychicMaintainRange(f,e,dt);this.psychicSkill(f,e)}if(f.id==='old_tv')this.oldTvSkill(f,e)", 'oldtv step')

# Projectile visual.
once("}else if(s.kind==='psychic_bolt'){", "}else if(s.kind==='oldtv_square'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(Math.max(24,s.radius*3))+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('🔲',0,0)}else if(s.kind==='psychic_bolt'){", 'oldtv projectile visual')

# TV noise visual overlay on body; no text label.
anchor="circle(f.x,f.y+10,r+3,'#02071066');"
noise=r'''circle(f.x,f.y+10,r+3,'#02071066');if(f.id==='old_tv'&&f.health>0&&engine.time<(f.oldTvNoiseUntil||0)){ctx.save();const w=r*1.45,h=r*1.05;ctx.fillStyle='#111';ctx.fillRect(f.x-w/2,f.y-h/2,w,h);for(let ni=0;ni<18;ni++){const yy=f.y-h/2+Math.random()*h,alpha=.22+Math.random()*.65;ctx.globalAlpha=alpha;ctx.fillStyle=Math.random()<.5?'#fff':'#777';ctx.fillRect(f.x-w/2,yy,w,1+Math.random()*3)}for(let ni=0;ni<28;ni++){ctx.globalAlpha=.25+Math.random()*.55;ctx.fillStyle=Math.random()<.5?'#e8e8e8':'#3b3b3b';ctx.fillRect(f.x-w/2+Math.random()*w,f.y-h/2+Math.random()*h,2+Math.random()*8,1+Math.random()*3)}ctx.globalAlpha=1;ctx.strokeStyle='#b9c1ca';ctx.lineWidth=2;ctx.strokeRect(f.x-w/2,f.y-h/2,w,h);ctx.restore();}'''
once(anchor,noise,'oldtv screen noise')

# Ability HUD.
once("function ability(f){if(f.id==='alien')", "function ability(f){if(f.id==='old_tv')return engine.time<(f.oldTvNoiseUntil||0)?'📺 노이즈 ON · 🔲 1~3연발 · 피해 40':'📺 다음 노이즈 '+Math.max(0,(f.oldTvNoiseNext||3.5)-engine.time).toFixed(1)+'초';if(f.id==='alien')", 'oldtv ability')

# Update forge system after chapter7 completion and on UI updates.
once("function updateChapter8UI(){const b=$('chapter8-entry');", "function updateChapter8UI(){updateForgeSystemUI();const b=$('chapter8-entry');", 'forge ui unlock refresh')

# Setup forge UI before handlers.
once("$('start').onclick=start;", "setupForgeSystemUI();$('start').onclick=start;", 'forge ui setup')

# Update tutorial casino odds / forge mention.
s=s.replace('꾸미기 30%, 캐릭터 10%, 꽝 60%이며 중복 보상은 코인으로 바뀌어.', '꾸미기 30%, 캐릭터 10%, 스테이지 스킵권 30%, 꽝 30%야. 스킵권은 중첩되며 옷장에서 1회 사용하면 다음 챕터를 해금해. CHAPTER 7을 클리어하면 100코인·1분 제작 방식의 🔨 제작소도 열려.',1)

# Marker checks.
req=["BATTLE <b>v3.68</b>","hp:650,damage:30,speed:95","id:'old_tv'","kind:'oldtv_square'","fillText('🔲'","STAGE_SKIP_KEY","grantStageSkipTicket","r<.70","craft-system-panel","Date.now()+60000","10+Math.floor(Math.random()*991)","unlock:'oldTv'"]
for x in req:
    if x not in s: raise SystemExit('missing marker: '+x)
if "BATTLE <b>v3.67</b>" in s: raise SystemExit('old version badge remains')
p.write_text(s,encoding='utf-8')
print('v3.68 patch applied')

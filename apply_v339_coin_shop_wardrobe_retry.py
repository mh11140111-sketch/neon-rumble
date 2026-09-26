from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:220]!r}')
    s=s.replace(old,new,count)

rep('BATTLE <b>v3.38</b>','BATTLE <b>v3.39</b>')
rep('<details class="patch-notes"><summary>📒 패치노트 · v3.38</summary><div class="patch-body">',
    '<details class="patch-notes"><summary>📒 패치노트 · v3.39</summary><div class="patch-body"><div class="patch-version"><h3>v3.39 · 코인의 시작, 전투 밖의 성장</h3><ul><li>밸런스: 🧌 법사좀비의 일반/샌드박스 HP를 2000 → 1000으로 하향. CHAPTER 3 STAGE 3 보스는 HP 2000 유지.</li><li>신규 시스템 🪙 코인: 모든 스테이지의 STAGE 1·2 클리어 시 1~30코인 랜덤 획득, 각 챕터 STAGE 3 클리어 시 50코인 획득.</li><li>신규 🛒 상점: 코인으로 꾸미기 아이템을 구매 가능. 캐릭터 상품 슬롯은 추후 업데이트 예정.</li><li>신규 👗 옷장: 구매한 꾸미기 아이템을 장착/해제 가능. 전용 꾸미기 아이템도 지원.</li></ul></div>')

rep("{id:'zombie_mage',name:'법사좀비',icon:'🧌',tag:'유도탄 · 미니좀비 소환',hp:2000,damage:85,speed:105,cooldown:2,unlock:'zombieMage',description:'이동속도가 느리고 몸집이 큰 법사좀비. 2초마다 피해 85의 유도탄을 발사하며 적중 시 HP 10의 미니좀비를 소환한다.',detail:'HP 2000 · 이동속도 -30% · 크기 1.5배 · 유도탄 85 / 2초 · 명중 시 HP 10 미니좀비 · 미니좀비 피해 5~20'},",
    "{id:'zombie_mage',name:'법사좀비',icon:'🧌',tag:'유도탄 · 미니좀비 소환',hp:1000,damage:85,speed:105,cooldown:2,unlock:'zombieMage',description:'이동속도가 느리고 몸집이 큰 법사좀비. 2초마다 피해 85의 유도탄을 발사하며 적중 시 HP 10의 미니좀비를 소환한다.',detail:'HP 1000 · 이동속도 -30% · 크기 1.5배 · 유도탄 85 / 2초 · 명중 시 HP 10 미니좀비 · 미니좀비 피해 5~20'},")

css='''
<style id="economy-style">
.economy-bar{display:flex;align-items:center;gap:8px;margin:12px 0 18px;flex-wrap:wrap}.coin-pill{font-weight:850;background:#211d12;border:1px solid #71622d;color:#ffe58a;border-radius:12px;padding:10px 14px}.economy-bar button{font-weight:800}.economy-panel{margin:0 0 18px;padding:16px;border:1px solid #40536d;border-radius:14px;background:#101b2b}.economy-panel h2{margin:0 0 6px;font-size:20px}.economy-panel>p{margin:0 0 14px;color:#9fb2ca;font-size:13px;line-height:1.6}.shop-grid,.wardrobe-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.shop-item,.wardrobe-item{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:12px;border:1px solid #30435c;border-radius:12px;background:#111c2b}.shop-item .item-icon,.wardrobe-item .item-icon{font-size:30px}.shop-item strong,.wardrobe-item strong{display:block}.shop-item small,.wardrobe-item small{display:block;color:#9fb2ca;margin-top:3px;line-height:1.4}.shop-item button,.wardrobe-item button{padding:8px 10px;min-height:38px;font-size:12px}.economy-empty{grid-column:1/-1;padding:14px;color:#8fa4bf;text-align:center;border:1px dashed #40536d;border-radius:10px}.shop-coming{margin-top:12px;padding:12px;border-radius:10px;background:#151d2a;color:#aebfd4;font-size:13px}@media(max-width:560px){.shop-grid,.wardrobe-grid{grid-template-columns:1fr}.economy-bar{gap:6px}.economy-bar>*{flex:1;text-align:center}.coin-pill{flex-basis:100%}}
</style>
'''
rep('</head><body><main>',css+'</head><body><main>')
rep('<span class="badge">BATTLE <b>v3.39</b></span><button id="settings-btn"',
    '<span class="badge">BATTLE <b>v3.39</b></span><span class="coin-pill" id="header-coins">🪙 0</span><button id="settings-btn"')

anchor='</div></details><div class="section-title"><div><p class="eyebrow">CHOOSE YOUR FIGHTER</p>'
insert='''</div></details><div class="economy-bar"><span class="coin-pill">보유 코인 <b id="coin-count">0</b> 🪙</span><button id="shop-btn" type="button">🛒 상점</button><button id="wardrobe-btn" type="button">👗 옷장</button></div><div id="shop-panel" class="economy-panel" hidden><h2>🛒 상점</h2><p>스테이지를 클리어해 모은 코인으로 꾸미기 아이템을 구매할 수 있어.</p><div id="shop-grid" class="shop-grid"></div><div class="shop-coming">🧑‍🤝‍🧑 캐릭터 상품 · 추후 업데이트 예정</div></div><div id="wardrobe-panel" class="economy-panel" hidden><h2>👗 옷장</h2><p>구매한 꾸미기 아이템을 장착해. 전용 아이템은 해당 캐릭터에게만 표시돼.</p><div id="wardrobe-grid" class="wardrobe-grid"></div></div><div class="section-title"><div><p class="eyebrow">CHOOSE YOUR FIGHTER</p>'''
rep(anchor,insert)

anchor="function updateChapter2UI(){const b=$('chapter2-entry');"
logic=r'''const COIN_KEY='neonRumble.coins.v1',SHOP_OWNED_KEY='neonRumble.shopOwned.v1',COSMETIC_EQUIPPED_KEY='neonRumble.equippedCosmetic.v1';
const SHOP_ITEMS=[
 {id:'neon_cap',name:'네온 캡',icon:'🧢',price:25,exclusiveFor:null,desc:'모든 캐릭터가 장착 가능'},
 {id:'neon_glasses',name:'네온 선글라스',icon:'🕶️',price:40,exclusiveFor:null,desc:'모든 캐릭터가 장착 가능'},
 {id:'gold_crown',name:'황금 왕관',icon:'👑',price:70,exclusiveFor:null,desc:'모든 캐릭터가 장착 가능'},
 {id:'robot_antenna',name:'로봇 전용 안테나',icon:'📡',price:90,exclusiveFor:'robot',desc:'🤖 로봇 전용 꾸미기'}
];
let coins=0,ownedCosmetics=[],equippedCosmetic=null;
try{coins=Math.max(0,parseInt(localStorage.getItem(COIN_KEY)||'0',10)||0);ownedCosmetics=JSON.parse(localStorage.getItem(SHOP_OWNED_KEY)||'[]');if(!Array.isArray(ownedCosmetics))ownedCosmetics=[];equippedCosmetic=localStorage.getItem(COSMETIC_EQUIPPED_KEY)||null}catch{}
function saveEconomy(){try{localStorage.setItem(COIN_KEY,String(coins));localStorage.setItem(SHOP_OWNED_KEY,JSON.stringify(ownedCosmetics));if(equippedCosmetic)localStorage.setItem(COSMETIC_EQUIPPED_KEY,equippedCosmetic);else localStorage.removeItem(COSMETIC_EQUIPPED_KEY)}catch{}}
function updateCoinUI(){if($('coin-count'))$('coin-count').textContent=coins;if($('header-coins'))$('header-coins').textContent='🪙 '+coins}
function awardStageCoins(n){const reward=n===3?50:1+Math.floor(Math.random()*30);coins+=reward;saveEconomy();updateCoinUI();return reward}
function currentCosmetic(){return SHOP_ITEMS.find(x=>x.id===equippedCosmetic)||null}
function buyCosmetic(id){const item=SHOP_ITEMS.find(x=>x.id===id);if(!item||ownedCosmetics.includes(id))return;if(coins<item.price){alert('코인이 부족해!');return}coins-=item.price;ownedCosmetics.push(id);saveEconomy();updateCoinUI();renderShop();renderWardrobe()}
function equipCosmetic(id){if(id!==null&&!ownedCosmetics.includes(id))return;equippedCosmetic=id;saveEconomy();renderWardrobe();renderShop()}
function renderShop(){const box=$('shop-grid');if(!box)return;box.innerHTML='';for(const item of SHOP_ITEMS){const own=ownedCosmetics.includes(item.id),row=document.createElement('div');row.className='shop-item';row.innerHTML='<span class="item-icon">'+item.icon+'</span><span><strong>'+item.name+'</strong><small>'+item.desc+' · '+item.price+'코인</small></span>';const b=document.createElement('button');b.type='button';b.textContent=own?'보유 중':'구매';b.disabled=own;b.onclick=()=>buyCosmetic(item.id);row.appendChild(b);box.appendChild(row)}}
function renderWardrobe(){const box=$('wardrobe-grid');if(!box)return;box.innerHTML='';const items=SHOP_ITEMS.filter(x=>ownedCosmetics.includes(x.id));if(!items.length){box.innerHTML='<div class="economy-empty">아직 보유한 꾸미기 아이템이 없어. 상점에서 구매해 봐.</div>';return}for(const item of items){const row=document.createElement('div');row.className='wardrobe-item';row.innerHTML='<span class="item-icon">'+item.icon+'</span><span><strong>'+item.name+'</strong><small>'+item.desc+'</small></span>';const b=document.createElement('button');b.type='button';const on=equippedCosmetic===item.id;b.textContent=on?'장착 해제':'장착';b.onclick=()=>equipCosmetic(on?null:item.id);row.appendChild(b);box.appendChild(row)}}
function toggleEconomyPanel(which){const shop=$('shop-panel'),ward=$('wardrobe-panel'),target=which==='shop'?shop:ward,other=which==='shop'?ward:shop;other.hidden=true;target.hidden=!target.hidden;if(!target.hidden){renderShop();renderWardrobe()}}
function updateChapter2UI(){const b=$('chapter2-entry');'''
rep(anchor,logic)

# Correct event anchor from current source.
anchor="$('stage-entry').onclick=()=>{if(mode==='desert'||mode==='desert-select')resetDesertTransient();engine=null;mode='stage';stageNo=1;updateSelection();window.scrollTo({top:0,behavior:'auto'})};"
rep(anchor,"$('shop-btn').onclick=()=>toggleEconomyPanel('shop');$('wardrobe-btn').onclick=()=>toggleEconomyPanel('wardrobe');\n"+anchor)

old="if(mode==='stage'){const unlockedNow=stageNo===2?unlockControlBoss():false,chapterNow=markRobotStage(stageNo);$('winner-icon').textContent='🏁';$('winner').textContent='STAGE '+stageNo+' 클리어!';$('summary').textContent=t+'초 · 로봇 생존 · 다음 스테이지도 테스트해 봐.'+(unlockedNow?' · 🎮 조정 보스전 해금!':'')+(chapterNow?' · 🏜️ CHAPTER 2 해금!':'')}"
new="if(mode==='stage'){const coinReward=awardStageCoins(stageNo),unlockedNow=stageNo===2?unlockControlBoss():false,chapterNow=markRobotStage(stageNo);$('winner-icon').textContent='🏁';$('winner').textContent='STAGE '+stageNo+' 클리어!';$('summary').textContent=t+'초 · 로봇 생존 · 🪙 '+coinReward+'코인 획득!'+(unlockedNow?' · 🎮 조정 보스전 해금!':'')+(chapterNow?' · 🏜️ CHAPTER 2 해금!':'')}"
rep(old,new)
old="else if(mode==='desert'&&engine.result===0){const chapter3Now=markDesertStage(desertStageNo),skNow=desertStageNo===3?unlockSkeletons():false,mageRoll=desertStageNo===3?tryUnlockSkeletonMage():null;"
new="else if(mode==='desert'&&engine.result===0){const coinReward=awardStageCoins(desertStageNo),chapter3Now=markDesertStage(desertStageNo),skNow=desertStageNo===3?unlockSkeletons():false,mageRoll=desertStageNo===3?tryUnlockSkeletonMage():null;"
rep(old,new)
rep("$('summary').textContent=t+'초 · 사막 돌파 성공'+(skNow?", "$('summary').textContent=t+'초 · 사막 돌파 성공 · 🪙 '+coinReward+'코인 획득!'+(skNow?")
old="else if(mode==='mansion'&&engine.result===0){const zRoll=mansionStageNo===3?tryUnlockZombieMage():null;"
new="else if(mode==='mansion'&&engine.result===0){const coinReward=awardStageCoins(mansionStageNo),zRoll=mansionStageNo===3?tryUnlockZombieMage():null;"
rep(old,new)
rep("$('summary').textContent=t+'초 · 피의 저택 방어 성공'+(zRoll", "$('summary').textContent=t+'초 · 피의 저택 방어 성공 · 🪙 '+coinReward+'코인 획득!'+(zRoll")

anchor="ctx.font='600 '+(f.boss?22:16)+'px system-ui';ctx.fillStyle=c;"
cos="const cosmetic=currentCosmetic();if(f.team===0&&!f.summon&&cosmetic&&(!cosmetic.exclusiveFor||cosmetic.exclusiveFor===f.id)){ctx.save();ctx.globalAlpha=1;ctx.font=(25*f.bodyScale)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText(cosmetic.icon,f.x,f.y-r*.82);ctx.restore()}ctx.font='600 '+(f.boss?22:16)+'px system-ui';ctx.fillStyle=c;"
rep(anchor,cos)

rep("applySettingsUI();updateControlBossUnlockUI();updateChapter2UI();updateChapter3UI();updateSelection();$('boot').hidden=true;",
    "applySettingsUI();updateControlBossUnlockUI();updateChapter2UI();updateChapter3UI();updateCoinUI();renderShop();renderWardrobe();updateSelection();$('boot').hidden=true;")

p.write_text(s,encoding='utf-8')
print('corrected v3.39 coin/shop/wardrobe patch applied')

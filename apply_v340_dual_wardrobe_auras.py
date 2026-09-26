from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:180]!r}')
    s=s.replace(old,new,count)

# Version + patch notes.
rep('BATTLE <b>v3.39</b>','BATTLE <b>v3.40</b>')
rep('<summary>📒 패치노트 · v3.39</summary><div class="patch-body">',
    '<summary>📒 패치노트 · v3.40</summary><div class="patch-body"><div class="patch-version"><h3>v3.40 · 두 선수의 스타일, 오라가 깨어나다</h3><ul><li>옷장: 왼쪽과 오른쪽 캐릭터가 서로 독립적으로 꾸미기 아이템을 장착 가능. 왼쪽 장신구가 오른쪽에 자동 적용되지 않음.</li><li>장신구 슬롯: 각 캐릭터는 장신구를 동시에 1개만 장착 가능.</li><li>아우라 슬롯 추가: 왼쪽/오른쪽 캐릭터가 각각 아우라 1개를 독립적으로 장착 가능. 아우라는 전투 능력치에는 영향을 주지 않고 캐릭터를 강하게 보이게 하는 시각 효과.</li><li>상점 아우라 추가: 🔴 빨간 아우라 100코인, 🟢 초록 아우라 100코인, 🟣 보라 아우라 100코인, 🌌 우주 아우라 120코인.</li></ul></div>')

# Wardrobe side controls.
old='<div id="wardrobe-panel" class="economy-panel" hidden><h2>👗 옷장</h2><p>구매한 꾸미기 아이템을 장착해. 전용 아이템은 해당 캐릭터에게만 표시돼.</p><div id="wardrobe-grid" class="wardrobe-grid"></div></div>'
new='<div id="wardrobe-panel" class="economy-panel" hidden><h2>👗 옷장</h2><p>왼쪽과 오른쪽 캐릭터를 따로 꾸밀 수 있어. 각 캐릭터는 장신구 1개 + 아우라 1개까지 장착 가능해.</p><div class="wardrobe-side-tabs"><button id="wardrobe-left" type="button" aria-pressed="true">◀ 왼쪽 캐릭터</button><button id="wardrobe-right" type="button" aria-pressed="false">오른쪽 캐릭터 ▶</button></div><div id="wardrobe-loadout" class="wardrobe-loadout"></div><div id="wardrobe-grid" class="wardrobe-grid"></div></div>'
rep(old,new)

# Economy styling for side selector / aura labels.
style_old='.shop-coming{margin-top:12px;padding:12px;border-radius:10px;background:#151d2a;color:#aebfd4;font-size:13px}@media(max-width:560px){.shop-grid,.wardrobe-grid{grid-template-columns:1fr}.economy-bar{gap:6px}.economy-bar>*{flex:1;text-align:center}.coin-pill{flex-basis:100%}}'
style_new='.shop-coming{margin-top:12px;padding:12px;border-radius:10px;background:#151d2a;color:#aebfd4;font-size:13px}.wardrobe-side-tabs{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:0 0 10px}.wardrobe-side-tabs button[aria-pressed="true"]{background:#b8f279;color:#132015;border-color:#b8f279;font-weight:850}.wardrobe-loadout{margin:0 0 12px;padding:10px 12px;border-radius:10px;background:#151f30;color:#c4d3e7;font-size:12px;line-height:1.6}.item-type{display:inline-block;margin-top:4px;padding:2px 6px;border-radius:999px;background:#26354b;color:#d9e7f8;font-size:10px;font-weight:800}@media(max-width:560px){.shop-grid,.wardrobe-grid{grid-template-columns:1fr}.economy-bar{gap:6px}.economy-bar>*{flex:1;text-align:center}.coin-pill{flex-basis:100%}}'
rep(style_old,style_new)

# Replace v3.39 single-slot economy model with left/right accessory + aura slots.
old="""const COIN_KEY='neonRumble.coins.v1',SHOP_OWNED_KEY='neonRumble.shopOwned.v1',COSMETIC_EQUIPPED_KEY='neonRumble.equippedCosmetic.v1';
const SHOP_ITEMS=[
 {id:'neon_cap',name:'네온 캡',icon:'🧢',price:25,exclusiveFor:null,desc:'모든 캐릭터가 장착 가능'},
 {id:'neon_glasses',name:'네온 선글라스',icon:'🕶️',price:40,exclusiveFor:null,desc:'모든 캐릭터가 장착 가능'},
 {id:'gold_crown',name:'황금 왕관',icon:'👑',price:70,exclusiveFor:null,desc:'모든 캐릭터가 장착 가능'},
 {id:'robot_antenna',name:'로봇 전용 안테나',icon:'📡',price:90,exclusiveFor:'robot',desc:'🤖 로봇 전용 꾸미기'}
];"""
new="""const COIN_KEY='neonRumble.coins.v1',SHOP_OWNED_KEY='neonRumble.shopOwned.v1',LEGACY_COSMETIC_EQUIPPED_KEY='neonRumble.equippedCosmetic.v1',EQUIP_LEFT_ACCESSORY_KEY='neonRumble.equip.leftAccessory.v2',EQUIP_RIGHT_ACCESSORY_KEY='neonRumble.equip.rightAccessory.v2',EQUIP_LEFT_AURA_KEY='neonRumble.equip.leftAura.v2',EQUIP_RIGHT_AURA_KEY='neonRumble.equip.rightAura.v2';
const SHOP_ITEMS=[
 {id:'neon_cap',name:'네온 캡',icon:'🧢',price:25,type:'accessory',exclusiveFor:null,desc:'모든 캐릭터가 장착 가능'},
 {id:'neon_glasses',name:'네온 선글라스',icon:'🕶️',price:40,type:'accessory',exclusiveFor:null,desc:'모든 캐릭터가 장착 가능'},
 {id:'gold_crown',name:'황금 왕관',icon:'👑',price:70,type:'accessory',exclusiveFor:null,desc:'모든 캐릭터가 장착 가능'},
 {id:'robot_antenna',name:'로봇 전용 안테나',icon:'📡',price:90,type:'accessory',exclusiveFor:'robot',desc:'🤖 로봇 전용 꾸미기'},
 {id:'aura_red',name:'빨간 아우라',icon:'🔴',price:100,type:'aura',auraStyle:'red',exclusiveFor:null,desc:'붉은 불꽃 기운이 캐릭터를 감싸는 아우라'},
 {id:'aura_green',name:'초록 아우라',icon:'🟢',price:100,type:'aura',auraStyle:'green',exclusiveFor:null,desc:'초록 에너지가 강하게 솟아오르는 아우라'},
 {id:'aura_purple',name:'보라 아우라',icon:'🟣',price:100,type:'aura',auraStyle:'purple',exclusiveFor:null,desc:'보랏빛 에너지가 흔들리는 아우라'},
 {id:'aura_space',name:'우주 아우라',icon:'🌌',price:120,type:'aura',auraStyle:'space',exclusiveFor:null,desc:'별빛과 우주 에너지가 회전하는 희귀 아우라'}
];"""
rep(old,new)

old="""let coins=0,ownedCosmetics=[],equippedCosmetic=null;
try{coins=Math.max(0,parseInt(localStorage.getItem(COIN_KEY)||'0',10)||0);ownedCosmetics=JSON.parse(localStorage.getItem(SHOP_OWNED_KEY)||'[]');if(!Array.isArray(ownedCosmetics))ownedCosmetics=[];equippedCosmetic=localStorage.getItem(COSMETIC_EQUIPPED_KEY)||null}catch{}
function saveEconomy(){try{localStorage.setItem(COIN_KEY,String(coins));localStorage.setItem(SHOP_OWNED_KEY,JSON.stringify(ownedCosmetics));if(equippedCosmetic)localStorage.setItem(COSMETIC_EQUIPPED_KEY,equippedCosmetic);else localStorage.removeItem(COSMETIC_EQUIPPED_KEY)}catch{}}
function updateCoinUI(){if($('coin-count'))$('coin-count').textContent=coins;if($('header-coins'))$('header-coins').textContent='🪙 '+coins}
function awardStageCoins(n){const reward=n===3?50:1+Math.floor(Math.random()*30);coins+=reward;saveEconomy();updateCoinUI();return reward}
function currentCosmetic(){return SHOP_ITEMS.find(x=>x.id===equippedCosmetic)||null}
function buyCosmetic(id){const item=SHOP_ITEMS.find(x=>x.id===id);if(!item||ownedCosmetics.includes(id))return;if(coins<item.price){alert('코인이 부족해!');return}coins-=item.price;ownedCosmetics.push(id);saveEconomy();updateCoinUI();renderShop();renderWardrobe()}
function equipCosmetic(id){if(id!==null&&!ownedCosmetics.includes(id))return;equippedCosmetic=id;saveEconomy();renderWardrobe();renderShop()}
function renderShop(){const box=$('shop-grid');if(!box)return;box.innerHTML='';for(const item of SHOP_ITEMS){const own=ownedCosmetics.includes(item.id),row=document.createElement('div');row.className='shop-item';row.innerHTML='<span class=\"item-icon\">'+item.icon+'</span><span><strong>'+item.name+'</strong><small>'+item.desc+' · '+item.price+'코인</small></span>';const b=document.createElement('button');b.type='button';b.textContent=own?'보유 중':'구매';b.disabled=own;b.onclick=()=>buyCosmetic(item.id);row.appendChild(b);box.appendChild(row)}}
function renderWardrobe(){const box=$('wardrobe-grid');if(!box)return;box.innerHTML='';const items=SHOP_ITEMS.filter(x=>ownedCosmetics.includes(x.id));if(!items.length){box.innerHTML='<div class=\"economy-empty\">아직 보유한 꾸미기 아이템이 없어. 상점에서 구매해 봐.</div>';return}for(const item of items){const row=document.createElement('div');row.className='wardrobe-item';row.innerHTML='<span class=\"item-icon\">'+item.icon+'</span><span><strong>'+item.name+'</strong><small>'+item.desc+'</small></span>';const b=document.createElement('button');b.type='button';const on=equippedCosmetic===item.id;b.textContent=on?'장착 해제':'장착';b.onclick=()=>equipCosmetic(on?null:item.id);row.appendChild(b);box.appendChild(row)}}
function toggleEconomyPanel(which){const shop=$('shop-panel'),ward=$('wardrobe-panel'),target=which==='shop'?shop:ward,other=which==='shop'?ward:shop;other.hidden=true;target.hidden=!target.hidden;if(!target.hidden){renderShop();renderWardrobe()}}"""
new="""let coins=0,ownedCosmetics=[],equippedAccessory=[null,null],equippedAura=[null,null],wardrobeSide=0;
try{coins=Math.max(0,parseInt(localStorage.getItem(COIN_KEY)||'0',10)||0);ownedCosmetics=JSON.parse(localStorage.getItem(SHOP_OWNED_KEY)||'[]');if(!Array.isArray(ownedCosmetics))ownedCosmetics=[];const legacy=localStorage.getItem(LEGACY_COSMETIC_EQUIPPED_KEY)||null;equippedAccessory[0]=localStorage.getItem(EQUIP_LEFT_ACCESSORY_KEY)||legacy;equippedAccessory[1]=localStorage.getItem(EQUIP_RIGHT_ACCESSORY_KEY)||null;equippedAura[0]=localStorage.getItem(EQUIP_LEFT_AURA_KEY)||null;equippedAura[1]=localStorage.getItem(EQUIP_RIGHT_AURA_KEY)||null}catch{}
function saveEconomy(){try{localStorage.setItem(COIN_KEY,String(coins));localStorage.setItem(SHOP_OWNED_KEY,JSON.stringify(ownedCosmetics));const keys=[EQUIP_LEFT_ACCESSORY_KEY,EQUIP_RIGHT_ACCESSORY_KEY],auraKeys=[EQUIP_LEFT_AURA_KEY,EQUIP_RIGHT_AURA_KEY];for(let i=0;i<2;i++){if(equippedAccessory[i])localStorage.setItem(keys[i],equippedAccessory[i]);else localStorage.removeItem(keys[i]);if(equippedAura[i])localStorage.setItem(auraKeys[i],equippedAura[i]);else localStorage.removeItem(auraKeys[i])}}catch{}}
function updateCoinUI(){if($('coin-count'))$('coin-count').textContent=coins;if($('header-coins'))$('header-coins').textContent='🪙 '+coins}
function awardStageCoins(n){const reward=n===3?50:1+Math.floor(Math.random()*30);coins+=reward;saveEconomy();updateCoinUI();return reward}
function equippedItem(side,type){const id=type==='aura'?equippedAura[side?1:0]:equippedAccessory[side?1:0];return SHOP_ITEMS.find(x=>x.id===id)||null}
function currentAccessory(side){return equippedItem(side,'accessory')}
function currentAura(side){return equippedItem(side,'aura')}
function buyCosmetic(id){const item=SHOP_ITEMS.find(x=>x.id===id);if(!item||ownedCosmetics.includes(id))return;if(coins<item.price){alert('코인이 부족해!');return}coins-=item.price;ownedCosmetics.push(id);saveEconomy();updateCoinUI();renderShop();renderWardrobe()}
function equipCosmetic(id){if(id!==null&&!ownedCosmetics.includes(id))return;const item=id?SHOP_ITEMS.find(x=>x.id===id):null;if(!item)return;const slot=item.type==='aura'?equippedAura:equippedAccessory;slot[wardrobeSide]=slot[wardrobeSide]===id?null:id;saveEconomy();renderWardrobe();renderShop()}
function renderShop(){const box=$('shop-grid');if(!box)return;box.innerHTML='';for(const item of SHOP_ITEMS){const own=ownedCosmetics.includes(item.id),row=document.createElement('div');row.className='shop-item';const typeName=item.type==='aura'?'아우라':'장신구';row.innerHTML='<span class=\"item-icon\">'+item.icon+'</span><span><strong>'+item.name+'</strong><small>'+item.desc+' · '+item.price+'코인</small><span class=\"item-type\">'+typeName+'</span></span>';const b=document.createElement('button');b.type='button';b.textContent=own?'보유 중':'구매';b.disabled=own;b.onclick=()=>buyCosmetic(item.id);row.appendChild(b);box.appendChild(row)}}
function renderWardrobe(){const box=$('wardrobe-grid');if(!box)return;if($('wardrobe-left'))$('wardrobe-left').setAttribute('aria-pressed',wardrobeSide===0?'true':'false');if($('wardrobe-right'))$('wardrobe-right').setAttribute('aria-pressed',wardrobeSide===1?'true':'false');const acc=currentAccessory(wardrobeSide),aura=currentAura(wardrobeSide);if($('wardrobe-loadout'))$('wardrobe-loadout').textContent=(wardrobeSide===0?'왼쪽':'오른쪽')+' 캐릭터 · 장신구: '+(acc?acc.icon+' '+acc.name:'없음')+' · 아우라: '+(aura?aura.icon+' '+aura.name:'없음');box.innerHTML='';const items=SHOP_ITEMS.filter(x=>ownedCosmetics.includes(x.id));if(!items.length){box.innerHTML='<div class=\"economy-empty\">아직 보유한 꾸미기 아이템이 없어. 상점에서 구매해 봐.</div>';return}for(const item of items){const row=document.createElement('div');row.className='wardrobe-item';const typeName=item.type==='aura'?'아우라':'장신구';row.innerHTML='<span class=\"item-icon\">'+item.icon+'</span><span><strong>'+item.name+'</strong><small>'+item.desc+'</small><span class=\"item-type\">'+typeName+'</span></span>';const b=document.createElement('button');b.type='button';const slot=item.type==='aura'?equippedAura:equippedAccessory,on=slot[wardrobeSide]===item.id;b.textContent=on?'장착 해제':'장착';b.onclick=()=>equipCosmetic(item.id);row.appendChild(b);box.appendChild(row)}}
function toggleEconomyPanel(which){const shop=$('shop-panel'),ward=$('wardrobe-panel'),target=which==='shop'?shop:ward,other=which==='shop'?ward:shop;other.hidden=true;target.hidden=!target.hidden;if(!target.hidden){renderShop();renderWardrobe()}}"""
rep(old,new)

# Wardrobe side buttons.
rep("$('shop-btn').onclick=()=>toggleEconomyPanel('shop');$('wardrobe-btn').onclick=()=>toggleEconomyPanel('wardrobe');",
    "$('shop-btn').onclick=()=>toggleEconomyPanel('shop');$('wardrobe-btn').onclick=()=>toggleEconomyPanel('wardrobe');$('wardrobe-left').onclick=()=>{wardrobeSide=0;renderWardrobe()};$('wardrobe-right').onclick=()=>{wardrobeSide=1;renderWardrobe()};")

# Add procedural aura renderer inspired by the supplied power-aura reference image.
needle='function draw(){if(!engine)return;'
aura_fn="""function drawEquippedAura(f,item){if(!item||!item.auraStyle||f.health<=0)return;const t=engine?engine.time:0,r=f.radius*(1.72+.08*Math.sin(t*5+f.side));ctx.save();ctx.translate(f.x,f.y);ctx.globalCompositeOperation='lighter';if(item.auraStyle==='space'){const g=ctx.createRadialGradient(0,0,f.radius*.45,0,0,r*1.22);g.addColorStop(0,'rgba(115,70,255,.04)');g.addColorStop(.48,'rgba(80,60,255,.22)');g.addColorStop(.78,'rgba(180,80,255,.38)');g.addColorStop(1,'rgba(60,200,255,0)');ctx.fillStyle=g;ctx.beginPath();ctx.arc(0,0,r*1.22,0,Math.PI*2);ctx.fill();for(let i=0;i<9;i++){const a=t*(i%2?1.2:-.9)+i*Math.PI*2/9,rr=r*(.75+(i%3)*.16),x=Math.cos(a)*rr,y=Math.sin(a)*rr;ctx.globalAlpha=.55+.35*Math.sin(t*4+i);ctx.fillStyle=i%3===0?'#fff':i%3===1?'#9bdcff':'#cf8cff';ctx.beginPath();ctx.arc(x,y,2+(i%2)*1.5,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=.9;ctx.strokeStyle='#9b72ff';ctx.lineWidth=4*f.scale;ctx.shadowColor='#79dfff';ctx.shadowBlur=22;ctx.beginPath();ctx.arc(0,0,r*.93,0,Math.PI*2);ctx.stroke()}else{const col=item.auraStyle==='red'?'#ff384d':item.auraStyle==='green'?'#65ff71':'#b45cff',light=item.auraStyle==='red'?'#ff9a72':item.auraStyle==='green'?'#b9ff8b':'#e2a4ff';ctx.shadowColor=col;ctx.shadowBlur=26;for(let k=0;k<3;k++){ctx.globalAlpha=.28-k*.055;ctx.strokeStyle=k===1?light:col;ctx.lineWidth=(10-k*2)*f.scale;ctx.beginPath();const rr=r*(.82+k*.12);ctx.arc(0,0,rr,t*(.35+k*.13),t*(.35+k*.13)+Math.PI*1.65);ctx.stroke()}for(let i=0;i<10;i++){const a=i*Math.PI*2/10+t*.18,base=r*.72,tip=r*(1.05+.15*Math.sin(t*4+i));ctx.globalAlpha=.2+.13*(i%2);ctx.fillStyle=i%2?light:col;ctx.beginPath();ctx.moveTo(Math.cos(a-.10)*base,Math.sin(a-.10)*base);ctx.quadraticCurveTo(Math.cos(a)*r*.9,Math.sin(a)*r*.9,Math.cos(a)*tip,Math.sin(a)*tip);ctx.quadraticCurveTo(Math.cos(a)*r*.9,Math.sin(a)*r*.9,Math.cos(a+.10)*base,Math.sin(a+.10)*base);ctx.closePath();ctx.fill()}}ctx.restore()}
function draw(){if(!engine)return;"""
rep(needle,aura_fn)

# Draw per-side aura before the fighter body, then per-side accessory after the emoji body.
rep("if(f.id==='chef'&&f.health>0){const pp=engine.chefPanTip(f),pa=Math.atan2(pp.y-f.y,pp.x-f.x);ctx.save();ctx.strokeStyle='#a9b2bd';ctx.lineWidth=8*f.scale;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(f.x+Math.cos(pa)*(r*.55),f.y+Math.sin(pa)*(r*.55));ctx.lineTo(pp.x-Math.cos(pa)*12*f.scale,pp.y-Math.sin(pa)*12*f.scale);ctx.stroke();circle(pp.x,pp.y,19*f.scale,'#343a40');circle(pp.x,pp.y,14*f.scale,'#171b20');if(f.chefEggReady){circle(pp.x-2*f.scale,pp.y,9*f.scale,'#fff7dc');circle(pp.x+1*f.scale,pp.y,4.5*f.scale,'#ffc83d')}ctx.restore();}circle(f.x,f.y,r,f.flash>0?'#ffffff':c);",
    "if(f.id==='chef'&&f.health>0){const pp=engine.chefPanTip(f),pa=Math.atan2(pp.y-f.y,pp.x-f.x);ctx.save();ctx.strokeStyle='#a9b2bd';ctx.lineWidth=8*f.scale;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(f.x+Math.cos(pa)*(r*.55),f.y+Math.sin(pa)*(r*.55));ctx.lineTo(pp.x-Math.cos(pa)*12*f.scale,pp.y-Math.sin(pa)*12*f.scale);ctx.stroke();circle(pp.x,pp.y,19*f.scale,'#343a40');circle(pp.x,pp.y,14*f.scale,'#171b20');if(f.chefEggReady){circle(pp.x-2*f.scale,pp.y,9*f.scale,'#fff7dc');circle(pp.x+1*f.scale,pp.y,4.5*f.scale,'#ffc83d')}ctx.restore();}if(!f.summon){const aura=currentAura(f.team);if(aura&&(!aura.exclusiveFor||aura.exclusiveFor===f.id))drawEquippedAura(f,aura)}circle(f.x,f.y,r,f.flash>0?'#ffffff':c);")

rep("const cosmetic=currentCosmetic();if(f.team===0&&!f.summon&&cosmetic&&(!cosmetic.exclusiveFor||cosmetic.exclusiveFor===f.id)){ctx.save();ctx.globalAlpha=1;ctx.font=(25*f.bodyScale)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText(cosmetic.icon,f.x,f.y-r*.82);ctx.restore()}",
    "const cosmetic=currentAccessory(f.team);if(!f.summon&&cosmetic&&(!cosmetic.exclusiveFor||cosmetic.exclusiveFor===f.id)){ctx.save();ctx.globalAlpha=1;ctx.font=(25*f.bodyScale)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText(cosmetic.icon,f.x,f.y-r*.82);ctx.restore()}")

p.write_text(s,encoding='utf-8')
print('v3.40 dual wardrobe + aura shop patch applied')

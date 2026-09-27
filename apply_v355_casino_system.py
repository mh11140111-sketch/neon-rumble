from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(label+' anchor missing')
    s=s.replace(old,new,count)

# Version / patch notes
rep('BATTLE <b>v3.54</b>','BATTLE <b>v3.55</b>','version')
rep('📒 패치노트 · v3.54','📒 패치노트 · v3.55','patch title')
marker='<div class="patch-body">'
patch='''<div class="patch-version"><h3>v3.55 · 도박장 시스템</h3><ul><li>🎰 CHAPTER 5의 STAGE 1·2·3을 모두 클리어하면 도박장 시스템 해금.</li><li>1회 200코인. 꾸미기 당첨 30%, 캐릭터 당첨 10%, 꽝 60%.</li><li>꾸미기 중복은 250코인, 캐릭터 중복은 400코인으로 교환.</li><li>도박장 전용 꾸미기 👒 🪙 🥽 🫟 🛴 🦽 추가. 획득한 꾸미기는 옷장에서 장착 가능.</li></ul></div>'''
if patch not in s: rep(marker,marker+patch,'patch notes')

# CSS
css_anchor='</style>\n<style id="tutorial-style">'
casino_css='''</style>\n<style id="casino-system-style">\n.casino-system-panel{margin:0 0 18px;padding:18px;border:1px solid #725b27;border-radius:16px;background:linear-gradient(180deg,#21130f,#11101a);text-align:center}.casino-system-panel h2{margin:0 0 6px}.casino-system-panel>p{color:#c7b88f;font-size:13px;line-height:1.65}.casino-reels{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;max-width:390px;margin:16px auto}.casino-reel{height:94px;display:grid;place-items:center;border:3px solid #d5a83e;border-radius:15px;background:#080b12;font-size:50px;box-shadow:inset 0 0 25px #000,0 0 12px #d5a83e33}.casino-result{min-height:48px;margin:12px auto;color:#ffe58a;font-weight:850;line-height:1.6}.casino-spin{min-width:220px;background:#b8f279;border-color:#b8f279;color:#132015;font-weight:900}.casino-spin:disabled{opacity:.45}.casino-odds{margin-top:12px!important;color:#9faec2!important;font-size:12px!important}.economy-bar #casino-system-btn[disabled]{opacity:.45}\n</style>\n<style id="tutorial-style">'''
rep(css_anchor,casino_css,'casino css')

# Economy HTML: add button and panel.
bar_old='<div class="economy-bar"><span class="coin-pill">보유 코인 <b id="coin-count">0</b> 🪙</span><button id="shop-btn" type="button">🛒 상점</button><button id="wardrobe-btn" type="button">👗 옷장</button></div>'
bar_new='<div class="economy-bar"><span class="coin-pill">보유 코인 <b id="coin-count">0</b> 🪙</span><button id="shop-btn" type="button">🛒 상점</button><button id="wardrobe-btn" type="button">👗 옷장</button><button id="casino-system-btn" type="button" disabled>🔒 도박장</button></div>'
rep(bar_old,bar_new,'economy bar')
ward_anchor='<div id="wardrobe-panel" class="economy-panel" hidden>'
casino_panel='''<div id="casino-system-panel" class="casino-system-panel" hidden><h2>🎰 도박장</h2><p>CHAPTER 5 클리어 보상 시스템 · 1회 200코인으로 슬롯머신을 돌려 전용 꾸미기와 캐릭터를 노려 봐.</p><div class="casino-reels" aria-label="도박장 슬롯머신"><div id="casino-reel-0" class="casino-reel">❔</div><div id="casino-reel-1" class="casino-reel">❔</div><div id="casino-reel-2" class="casino-reel">❔</div></div><div id="casino-result" class="casino-result">꾸미기 30% · 캐릭터 10% · 꽝 60%</div><button id="casino-spin" class="casino-spin" type="button">🎰 200코인으로 돌리기</button><p class="casino-odds">중복 꾸미기 → 250코인 · 중복 캐릭터 → 400코인</p></div>'''
if 'id="casino-system-panel"' not in s: rep(ward_anchor,casino_panel+ward_anchor,'casino panel')

# Add casino-only cosmetic items before the first aura item.
shop_anchor=" {id:'aura_red',name:'빨간 아우라'"
items=""" {id:'casino_ribbon_hat',name:'리본모자',icon:'👒',price:0,type:'accessory',casinoOnly:true,exclusiveFor:null,desc:'도박장에서만 획득 가능한 리본모자'},
 {id:'casino_coin_charm',name:'골드코인 장식',icon:'🪙',price:0,type:'accessory',casinoOnly:true,exclusiveFor:null,desc:'도박장에서만 획득 가능한 코인 장식'},
 {id:'casino_goggles',name:'카지노 고글',icon:'🥽',price:0,type:'accessory',casinoOnly:true,exclusiveFor:null,desc:'도박장에서만 획득 가능한 고글'},
 {id:'casino_splash',name:'젤리 장식',icon:'🫟',price:0,type:'accessory',casinoOnly:true,exclusiveFor:null,desc:'도박장에서만 획득 가능한 특별 장식'},
 {id:'casino_scooter',name:'미니 킥보드',icon:'🛴',price:0,type:'accessory',casinoOnly:true,exclusiveFor:null,desc:'도박장에서만 획득 가능한 킥보드 장식'},
 {id:'casino_wheelchair',name:'미니 휠체어',icon:'🦽',price:0,type:'accessory',casinoOnly:true,exclusiveFor:null,desc:'도박장에서만 획득 가능한 휠체어 장식'},
"""
if 'casino_ribbon_hat' not in s: rep(shop_anchor,items+shop_anchor,'casino items')

# Hide casino-only items from normal shop.
rep("for(const item of SHOP_ITEMS){const own=ownedCosmetics.includes(item.id),row=document.createElement('div');", "for(const item of SHOP_ITEMS){if(item.casinoOnly)continue;const own=ownedCosmetics.includes(item.id),row=document.createElement('div');",'hide casino items from shop')

# Casino logic inserted before renderShop.
logic_anchor='function renderShop(){'
logic="""const CASINO_COSMETIC_IDS=['casino_ribbon_hat','casino_coin_charm','casino_goggles','casino_splash','casino_scooter','casino_wheelchair'];
const CASINO_CHARACTER_IDS=['slotmachine','moneyman'];
let casinoSpinning=false;
function casinoSystemUnlocked(){return chapter6Unlocked()}
function updateCasinoSystemUI(){const b=$('casino-system-btn');if(!b)return;const ok=casinoSystemUnlocked();b.disabled=!ok;b.textContent=ok?'🎰 도박장':'🔒 도박장 · CHAPTER 5 클리어 필요';const spin=$('casino-spin');if(spin)spin.disabled=!ok||casinoSpinning||coins<200}
function casinoShowReels(icon){for(let i=0;i<3;i++){const el=$('casino-reel-'+i);if(el)el.textContent=icon}}
function casinoCharacterOwned(id){return ownedCosmetics.includes(id)}
function grantCasinoCharacter(id){if(!ownedCosmetics.includes(id))ownedCosmetics.push(id);saveEconomy();refreshUnlockCards();renderShop()}
function spinCasino(){if(casinoSpinning||!casinoSystemUnlocked())return;if(coins<200){alert('코인이 부족해! 슬롯머신은 200코인이 필요해.');return}coins-=200;casinoSpinning=true;saveEconomy();updateCoinUI();updateCasinoSystemUI();const pool=['🎰','👒','🪙','🥽','🫟','🛴','🦽','🤑','💎','❌'];let ticks=0;const timer=setInterval(()=>{for(let i=0;i<3;i++)$('casino-reel-'+i).textContent=pool[Math.floor(Math.random()*pool.length)];ticks++;if(ticks<12)return;clearInterval(timer);const r=Math.random();let text='';if(r<.30){const id=CASINO_COSMETIC_IDS[Math.floor(Math.random()*CASINO_COSMETIC_IDS.length)],item=SHOP_ITEMS.find(x=>x.id===id),dup=ownedCosmetics.includes(id);casinoShowReels(item.icon);if(dup){coins+=250;text=item.icon+' '+item.name+' 중복! 대신 🪙 250코인 획득!'}else{ownedCosmetics.push(id);text=item.icon+' '+item.name+' 획득! 옷장에서 장착할 수 있어.'}}else if(r<.40){const id=CASINO_CHARACTER_IDS[Math.floor(Math.random()*CASINO_CHARACTER_IDS.length)],item=SHOP_ITEMS.find(x=>x.id===id),dup=casinoCharacterOwned(id);casinoShowReels(item?item.icon:'🎰');if(dup){coins+=400;text=(item?item.icon:'🎰')+' '+(item?item.name:'캐릭터')+' 중복! 대신 🪙 400코인 획득!'}else{grantCasinoCharacter(id);text=(item?item.icon:'🎰')+' '+(item?item.name:'캐릭터')+' 캐릭터 획득!'}}else{casinoShowReels('❌');text='아쉽다! 이번에는 꽝이야.'}saveEconomy();updateCoinUI();renderWardrobe();renderShop();refreshUnlockCards();casinoSpinning=false;updateCasinoSystemUI();$('casino-result').textContent=text},55)}
"""
if 'function spinCasino()' not in s: rep(logic_anchor,logic+logic_anchor,'casino logic')

# Expand panel toggler to 3 panels.
old_toggle="function toggleEconomyPanel(which){const shop=$('shop-panel'),ward=$('wardrobe-panel'),target=which==='shop'?shop:ward,other=which==='shop'?ward:shop;other.hidden=true;target.hidden=!target.hidden;if(!target.hidden){renderShop();renderWardrobe()}}"
new_toggle="function toggleEconomyPanel(which){const panels={shop:$('shop-panel'),wardrobe:$('wardrobe-panel'),casino:$('casino-system-panel')},target=panels[which];if(!target)return;const open=target.hidden;for(const p of Object.values(panels))if(p)p.hidden=true;target.hidden=!open;if(open){renderShop();renderWardrobe();updateCasinoSystemUI()}}"
rep(old_toggle,new_toggle,'panel toggle')

# Update unlock UI when Chapter 5 becomes complete.
rep("function updateChapter6UI(){const b=$('chapter6-entry');if(!b)return;const ok=chapter6Unlocked();b.disabled=!ok;b.textContent=ok?'🌊 CHAPTER 6 · 바닷속':'🔒 CHAPTER 6 · CHAPTER 5 STAGE 1·2·3 클리어 필요'}", "function updateChapter6UI(){const b=$('chapter6-entry');if(b){const ok=chapter6Unlocked();b.disabled=!ok;b.textContent=ok?'🌊 CHAPTER 6 · 바닷속':'🔒 CHAPTER 6 · CHAPTER 5 STAGE 1·2·3 클리어 필요'}updateCasinoSystemUI()}",'chapter6 ui')

# Button hookups: insert beside existing economy handlers if exact anchors exist.
shop_hook="$('shop-btn').onclick=()=>toggleEconomyPanel('shop');"
ward_hook="$('wardrobe-btn').onclick=()=>toggleEconomyPanel('wardrobe');"
if shop_hook in s and "casino-system-btn').onclick" not in s:
    s=s.replace(shop_hook,shop_hook+"$('casino-system-btn').onclick=()=>{if(!casinoSystemUnlocked())return;toggleEconomyPanel('casino')};",1)
elif ward_hook in s and "casino-system-btn').onclick" not in s:
    s=s.replace(ward_hook,ward_hook+"$('casino-system-btn').onclick=()=>{if(!casinoSystemUnlocked())return;toggleEconomyPanel('casino')};",1)
else:
    # add before initial UI calls as fallback
    anchor='applySettingsUI();updateControlBossUnlockUI();'
    if anchor not in s: raise SystemExit('casino button hook anchor missing')
    s=s.replace(anchor,"$('casino-system-btn').onclick=()=>{if(!casinoSystemUnlocked())return;toggleEconomyPanel('casino')};$('casino-spin').onclick=spinCasino;"+anchor,1)
# Ensure spin hook exactly once.
if "$('casino-spin').onclick=spinCasino;" not in s:
    anchor='applySettingsUI();updateControlBossUnlockUI();'
    rep(anchor,"$('casino-spin').onclick=spinCasino;"+anchor,'spin hook')

# Initialize casino UI on boot.
boot_anchor='applySettingsUI();updateControlBossUnlockUI();updateChapter2UI();updateChapter3UI();updateChapter4UI();updateChapter5UI();updateChapter6UI();'
if boot_anchor in s:
    s=s.replace(boot_anchor,boot_anchor+'updateCasinoSystemUI();',1)

# Final safety checks
required=['BATTLE <b>v3.55</b>','id="casino-system-btn"','id="casino-system-panel"','casino_ribbon_hat','function spinCasino()','r<.30','r<.40','coins-=200','coins+=250','coins+=400','CASINO_CHARACTER_IDS']
for x in required:
    if x not in s: raise SystemExit('missing marker '+x)
if s==orig: raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('v3.55 casino system patch applied')

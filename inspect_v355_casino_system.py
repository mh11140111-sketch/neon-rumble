from pathlib import Path
s=Path('index.html').read_text(encoding='utf-8')
keys=['SHOP_ITEMS=[','function renderShop','function renderWardrobe','COIN_KEY=','function characterLocked','function markCasinoStage','chapter6Unlocked','economy','shop-panel','wardrobe-panel','moneyManOwned','slotMachineOwned','awardStageCoins']
for k in keys:
    print('\n###',k)
    i=s.find(k)
    print('INDEX',i)
    if i>=0: print(s[max(0,i-1200):i+3200])

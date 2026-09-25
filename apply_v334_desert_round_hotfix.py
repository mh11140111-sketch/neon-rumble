from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n!=count:
        raise SystemExit(f'replace mismatch: expected {count}, found {n}: {old[:180]!r}')
    s=s.replace(old,new,count)

# Keep v3.34 visible; expand its patch notes with the round/defeat fixes.
rep(
"<li>CHAPTER 2 STAGE 3 클리어 시 해골 3종 해금. 일반 전투에서 해금 해골은 최대 3회 등장.</li>",
"<li>CHAPTER 2 STAGE 3 클리어 시 해골 3종 해금. 일반 전투에서 해금 해골은 3라운드까지 등장.</li><li>사막 스테이지: 각 해골 웨이브 격파 시 카우보이가 최대 체력의 20%를 회복.</li><li>사막 스테이지에서 카우보이가 사망하면 절대 클리어로 처리되지 않도록 승패 판정 수정.</li><li>해금 해골의 다음 라운드 진입 시 상대 체력은 이전 라운드 값을 그대로 유지하며 절대 회복하지 않음.</li>"
)

# Skeleton roster wording: this is explicitly a 3-round character mechanic.
repls={
"tag:'🔫 회전총 · 3회 등장'":"tag:'🔫 회전총 · 3라운드'",
"CHAPTER 2에서 해금하면 한 경기에서 최대 3번 등장해.":"CHAPTER 2에서 해금하면 한 경기에서 최대 3라운드까지 등장해.",
"detail:'HP 125 · 🔫 회전총 · 총알 70 / 1초 · 해금 후 총 3회 등장'":"detail:'HP 125 · 🔫 회전총 · 총알 70 / 1초 · 해금 후 총 3라운드'",
"tag:'🗡️ 추적검 · 3회 등장'":"tag:'🗡️ 추적검 · 3라운드'",
"detail:'HP 125 · 🗡️ 피해 70 · 쿨타임 3초 · 해금 후 총 3회 등장'":"detail:'HP 125 · 🗡️ 피해 70 · 쿨타임 3초 · 해금 후 총 3라운드'",
"tag:'🍺 비틀비틀 조준 · 3회 등장'":"tag:'🍺 비틀비틀 조준 · 3라운드'",
"detail:'HP 125 · 🍺 피해 100 · 쿨타임 3초 · 낮은 명중률 · 해금 후 총 3회 등장'":"detail:'HP 125 · 🍺 피해 100 · 쿨타임 3초 · 낮은 명중률 · 해금 후 총 3라운드'"
}
for old,new in repls.items():
    # Shared description sentence appears in all 3 entries.
    if old=="CHAPTER 2에서 해금하면 한 경기에서 최대 3번 등장해.":
        rep(old,new,3)
    else:
        rep(old,new)

# Round transition text. Only the skeleton is restored. Opponent health is intentionally untouched.
rep(
"this.effect(f,'💀 재등장 '+(f.revivals+1)+'/3','skill');this.emit(f.name+' 재등장! '+(f.revivals+1)+'/3');return true",
"this.effect(f,'💀 ROUND '+(f.revivals+1)+'/3','skill');this.emit(f.name+' 다음 라운드! ROUND '+(f.revivals+1)+'/3 · 상대 체력 유지');return true"
)

# When skeletons are unlocked, clear any search filter and show every playable character.
old_unlock="function unlockSkeletons(){if(skeletonsUnlocked)return false;skeletonsUnlocked=true;try{localStorage.setItem(SKELETON_UNLOCK_KEY,'1')}catch{}for(const b of $('roster').children){const c=ROSTER.find(v=>v.id===b.dataset.character);if(c?.unlock==='skeleton')b.hidden=false}return true}"
new_unlock="function unlockSkeletons(){if(skeletonsUnlocked)return false;skeletonsUnlocked=true;try{localStorage.setItem(SKELETON_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';for(const b of $('roster').children){const c=ROSTER.find(v=>v.id===b.dataset.character);b.hidden=!!c?.stageOnly||(c?.unlock==='skeleton'&&!skeletonsUnlocked)}return true}"
rep(old_unlock,new_unlock)

# Desert wave clear: heal Cowboy by 20% of max HP exactly once before next wave / clear.
old_update="function updateDesertStage(){if(mode!=='desert'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}if(desertStageNo<3){const alive=engine.fighters.some(f=>f.team===1&&f.health>0);if(!alive){if(desertWave>=5)engine.result=0;else spawnDesertWave()}}else{const mage=engine.fighters.find(f=>f.id==='skeleton_mage'&&f.team===1);if(!mage||mage.health<=0){engine.result=0;return}if(engine.time>=desertNextMageSummon-1e-9){desertNextMageSummon+=10;const ids=['skeleton_gun','skeleton_sword','skeleton_drunk'],id=ids[Math.floor(Math.random()*ids.length)],a=Math.random()*Math.PI*2;spawnDesertSkeleton(id,Math.max(70,Math.min(650,mage.x+Math.cos(a)*95)),Math.max(70,Math.min(650,mage.y+Math.sin(a)*95)));$('event').textContent='💀🧙 해골 법사가 해골 1마리를 소환!'}}}"
new_update="function updateDesertStage(){if(mode!=='desert'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}if(desertStageNo<3){const alive=engine.fighters.some(f=>f.team===1&&f.health>0);if(!alive){const before=hero.health,heal=hero.hp*.2;hero.health=Math.min(hero.hp,hero.health+heal);const actual=Math.max(0,Math.round(hero.health-before));if(actual>0){hero.healed=(hero.healed||0)+actual;engine.effect(hero,'🏜️ ROUND CLEAR +'+actual,'heal')}if(desertWave>=5)engine.result=0;else spawnDesertWave()}}else{const mage=engine.fighters.find(f=>f.id==='skeleton_mage'&&f.team===1);if(!mage||mage.health<=0){engine.result=0;return}if(engine.time>=desertNextMageSummon-1e-9){desertNextMageSummon+=10;const ids=['skeleton_gun','skeleton_sword','skeleton_drunk'],id=ids[Math.floor(Math.random()*ids.length)],a=Math.random()*Math.PI*2;spawnDesertSkeleton(id,Math.max(70,Math.min(650,mage.x+Math.cos(a)*95)),Math.max(70,Math.min(650,mage.y+Math.sin(a)*95)));$('event').textContent='💀🧙 해골 법사가 해골 1마리를 소환!'}}}"
rep(old_update,new_update)

# Fix desert defeat being rendered as a clear/victory.
old_desert_result="else if(mode==='desert'){const skNow=desertStageNo===3?unlockSkeletons():false;$('winner-icon').textContent='🏜️';$('winner').textContent='CHAPTER 2 · STAGE '+desertStageNo+' 클리어!';$('summary').textContent=t+'초 · 사막 돌파 성공'+(skNow?' · 💀 해골 3종 캐릭터 해금!':'')}else{"
new_desert_result="else if(mode==='desert'&&engine.result===0){const skNow=desertStageNo===3?unlockSkeletons():false;$('winner-icon').textContent='🏜️';$('winner').textContent='CHAPTER 2 · STAGE '+desertStageNo+' 클리어!';$('summary').textContent=t+'초 · 사막 돌파 성공'+(skNow?' · 💀 해골 3종 캐릭터 해금!':'')}else if(mode==='desert'){$('winner-icon').textContent='💀';$('winner').textContent='CHAPTER 2 · STAGE '+desertStageNo+' 실패';$('summary').textContent=t+'초 · 카우보이가 쓰러졌어. 다시 도전해 봐.'}else{"
rep(old_desert_result,new_desert_result)

# Skeleton HUD explicitly shows 3-round progress.
rep(
"function ability(f){if(f.id==='coolguy')",
"function ability(f){if(['skeleton_gun','skeleton_sword','skeleton_drunk'].includes(f.id))return '💀 ROUND '+((f.revivals||0)+1)+' / 3 · 상대 HP 유지';if(f.id==='coolguy')"
)

p.write_text(s,encoding='utf-8')
print('v3.34 desert/round hotfix applied')

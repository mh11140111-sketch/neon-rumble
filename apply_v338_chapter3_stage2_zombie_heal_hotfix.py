from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:180]!r}')
    s=s.replace(old,new,count)

# Keep visible version v3.38 and append emergency Stage 2 heal note.
needle='<div class="patch-body"><div class="patch-version"><h3>v3.38 · 피의 저택, 좀비 반란의 밤</h3><ul>'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.38 · 피의 저택, 좀비 반란의 밤</h3><ul><li>긴급 패치: CHAPTER 3 STAGE 2에서 왕좀비가 소환한 일반 좀비를 처치할 때마다 살아 있는 모든 아군이 각자 최대 체력의 5% 회복.</li>'
rep(needle,insert)

# Stage 2 battle info.
rep("n===2?'CHAPTER 3 STAGE 2 · 왕좀비 HP 1500 · 3초마다 좀비 소환 · 여자 뱀파이어 HP 1000 지원.'",
    "n===2?'CHAPTER 3 STAGE 2 · 왕좀비 HP 1500 · 3초마다 좀비 소환 · 소환 좀비 처치 시 모든 아군 최대 HP 5% 회복 · 여자 뱀파이어 HP 1000 지원.'")

# Stage 2: each dead summoned normal zombie heals every living ally by 5% of that ally's max HP exactly once.
old="}else if(mansionStageNo===2){const king=engine.fighters.find(f=>f.id==='king_zombie'&&f.team===1&&!f.summon);if(!king||king.health<=0)engine.result=0}else{"
new="}else if(mansionStageNo===2){for(const z of engine.fighters.filter(f=>f.id==='zombie'&&f.team===1&&f.summon&&f.health<=0&&!f.mansionStage2HealRewarded)){z.mansionStage2HealRewarded=true;for(const ally of engine.fighters.filter(f=>f.team===0&&f.health>0)){const before=ally.health,heal=ally.hp*.05;ally.health=Math.min(ally.hp,ally.health+heal);const actual=Math.max(0,Math.round(ally.health-before));if(actual>0){ally.healed=(ally.healed||0)+actual;engine.effect(ally,'🧟 처치 +'+actual,'heal')}}engine.emit('🧟‍♂️ 소환 좀비 처치! 모든 아군 최대 HP 5% 회복')}const king=engine.fighters.find(f=>f.id==='king_zombie'&&f.team===1&&!f.summon);if(!king||king.health<=0)engine.result=0}else{"
rep(old,new)

# Stage card text.
rep('HP 1500 왕좀비가 3초마다 일반 좀비를 소환해. HP 1000 여자 뱀파이어가 지원.',
    'HP 1500 왕좀비가 3초마다 일반 좀비를 소환해. 소환 좀비 처치 시 모든 아군 최대 HP 5% 회복. HP 1000 여자 뱀파이어가 지원.')

p.write_text(s,encoding='utf-8')
print('v3.38 Chapter 3 Stage 2 summoned-zombie heal hotfix applied')

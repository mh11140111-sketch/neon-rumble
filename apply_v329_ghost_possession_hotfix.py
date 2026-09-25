from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 occurrence, found {n}')
    s=s.replace(old,new,1)

# Keep v3.29 badge: this is a submarine hotfix.
if 'BATTLE <b>v3.29</b>' not in s:
    raise SystemExit('v3.29 badge missing')

# Update ghost roster wording from resurrection to possession.
old="{id:'ghost',name:'유령',icon:'👻',tag:'통과 · 아군 부활',hp:1000,damage:0,speed:170,cooldown:0,description:'적과 닿으면 0.3초 동안 모든 충돌과 공격을 통과해. 별도 쿨타임은 없어. 단체전이나 보스 도전자 팀에서는 살아 있는 동안 팀에서 처음 탈락한 아군 1명을 한 번 부활시켜.',detail:'HP 1000 · 접촉 시 0.3초 통과 · 쿨타임 0초 · 팀전 아군 1회 부활 · 부활 HP 300 / 최대 HP가 300 미만이면 풀 회복'}"
new="{id:'ghost',name:'유령',icon:'👻',tag:'통과 · 시체 빙의',hp:1000,damage:0,speed:170,cooldown:0,description:'적과 닿으면 0.3초 동안 모든 충돌과 공격을 통과해. 팀전에서는 처음 죽은 아군이나 아군 소환수의 시체에 경기당 1회 빙의해. 빙의 중 유령은 사라지고, 빙의체가 죽으면 그 자리에서 유령이 다시 나타나.',detail:'HP 1000 · 접촉 시 0.3초 통과 · 쿨타임 0초 · 팀전 1회 시체 빙의 · 소환수 빙의 가능 · 빙의체 HP 300 / 최대 HP가 300 미만이면 풀 회복 · 빙의체 사망 시 유령 복귀'}"
once(old,new,'ghost roster possession wording')

# Add possession runtime fields to base fighters. Keep ghostReviveUsed as the one-use flag for compatibility.
once("retreatHit:false,ghostPhaseUntil:0,ghostReviveUsed:false,deathOrder:null,",
     "retreatHit:false,ghostPhaseUntil:0,ghostReviveUsed:false,ghostPossessing:false,ghostPossessingSide:null,ghostStoredHealth:0,possessedByGhost:null,deathOrder:null,",
     'possession fields')

# Replace v3.29 revive implementation with possession lifecycle.
pattern=r"checkEnd\(\)\{if\(this\.resolvingBlast\)return;if\(this\.mode==='relay'\)\{.*?if\(!alive\[0\]\|\|!alive\[1\]\)this\.result=alive\[0\]\?0:1\}"
m=re.search(pattern,s,re.S)
if not m:
    raise SystemExit('checkEnd block not found')
new_check="""checkEnd(){if(this.resolvingBlast)return;if(this.mode==='relay'){const out=this.fighters.find(f=>f.health<=0&&this.relayIndex[f.side]===2);if(out)this.result=1-out.side;return;}this.resolveGhostPossession();const alive=[0,1].map(team=>this.fighters.some(f=>f.team===team&&f.health>0&&(!f.summon||f.possessedByGhost!=null)));if(!alive[0]||!alive[1])this.result=alive[0]?0:1}
resolveGhostPossession(){
 if(!(this.mode==='group'||this.mode==='boss'))return;
 // If a possessed body has died/expired, return its ghost at that exact position.
 for(const body of this.fighters){if(body.possessedByGhost==null||body.health>0)continue;const ghost=this.fighters[body.possessedByGhost];if(!ghost)continue;body.possessedByGhost=null;ghost.ghostPossessing=false;ghost.ghostPossessingSide=null;ghost.health=Math.max(1,Math.min(ghost.hp,ghost.ghostStoredHealth||ghost.hp));ghost.x=body.x;ghost.y=body.y;ghost.poison=null;ghost.toxin=null;ghost.burn=null;ghost.curse=null;ghost.stunUntil=0;ghost.slow=0;ghost.slowPower=0;ghost.rootSlow=0;ghost.rootSlowPower=0;ghost.deathOrder=null;this.effect(ghost,'👻 빙의 해제!','skill');this.emit('👻 빙의체가 쓰러져 유령이 다시 나타났어!')}
 // Track dead allies and summons in actual discovery order. Ghosts currently inside a body are not corpses.
 for(const f of this.fighters)if(f.health<=0&&f.deathOrder==null&&!(f.id==='ghost'&&f.ghostPossessing))f.deathOrder=++this.deathSerial;
 for(const team of [0,1]){const ghost=this.fighters.find(f=>!f.summon&&f.team===team&&f.id==='ghost'&&f.health>0&&!f.ghostReviveUsed&&!f.ghostPossessing);if(!ghost)continue;const corpse=this.fighters.filter(f=>f.team===team&&f!==ghost&&f.health<=0&&f.deathOrder!=null&&f.possessedByGhost==null).sort((a,b)=>a.deathOrder-b.deathOrder)[0];if(!corpse)continue;ghost.ghostReviveUsed=true;ghost.ghostPossessing=true;ghost.ghostPossessingSide=corpse.side;ghost.ghostStoredHealth=ghost.health;ghost.health=0;ghost.trail=[];corpse.possessedByGhost=ghost.side;corpse.health=Math.min(300,corpse.hp);corpse.poison=null;corpse.toxin=null;corpse.burn=null;corpse.curse=null;corpse.stunUntil=0;corpse.slow=0;corpse.slowPower=0;corpse.rootSlow=0;corpse.rootSlowPower=0;corpse.capturedBy=null;corpse.airborneUntil=0;corpse.trail=[];corpse.deathOrder=null;this.effect(corpse,'👻 빙의!','skill');this.emit('👻 유령이 '+corpse.name+'의 시체에 빙의했어!')}
}"""
s=s[:m.start()]+new_check+s[m.end():]

# Resolve summon expiry/death even if that code path does not call checkEnd directly.
once("step(dt){if(this.result!==null||dt<=0)return;this.updateAirborne();for(const f of this.fighters)if(f.id==='lizard')this.lizardSkill(f);this.stepRound(dt);if(this.mode==='relay'&&this.result===null)this.advanceRelay()}",
     "step(dt){if(this.result!==null||dt<=0)return;this.updateAirborne();for(const f of this.fighters)if(f.id==='lizard')this.lizardSkill(f);this.stepRound(dt);if(this.result===null)this.resolveGhostPossession();if(this.mode==='relay'&&this.result===null)this.advanceRelay()}",
     'step possession resolver')

# Patch note wording for the already-current v3.29 section only.
s=s.replace('신규 캐릭터 👻 유령: 적과 접촉하면 0.3초 동안 충돌과 공격을 통과. 별도 재사용 대기시간 없음.</li><li>단체전·보스 도전자 팀에서 살아 있는 유령은 팀에서 처음 탈락한 아군 1명을 1회 부활. 부활 HP는 300, 원래 최대 HP가 300 미만이면 최대 HP까지 회복.',
            '신규 캐릭터 👻 유령: 적과 접촉하면 0.3초 동안 충돌과 공격을 통과. 별도 재사용 대기시간 없음.</li><li>단체전·보스 도전자 팀에서 처음 죽은 아군 또는 소환수의 시체에 경기당 1회 빙의. 유령은 빙의 중 사라지고, 빙의체가 죽으면 그 자리에서 다시 등장. 빙의체 HP는 300, 원래 최대 HP가 300 미만이면 최대 HP까지.',1)

if s==orig:
    raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('V329_GHOST_POSSESSION_HOTFIX_APPLIED')

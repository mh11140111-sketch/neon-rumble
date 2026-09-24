from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old="""knightShockwave(f){if(f.id!=='knight'||f.health<=0)return;this.effects.push({x:f.x,y:f.y,text:'방패 충격파!',kind:'shockwave',side:f.side,team:f.team,life:.9});this.emit('🛡️ 기사가 강력한 공격을 막아 충격파를 발동!');this.resolvingBlast=true;for(const e of this.fighters){if(e===f||e.health<=0)continue;this.attack(f,e,100,true);if(e.health>0)e.stunUntil=Math.max(e.stunUntil,this.time+3)}this.resolvingBlast=false;this.checkEnd()}"""
new="""knightShockwave(f){if(f.id!=='knight'||f.health<=0)return;this.effects.push({x:f.x,y:f.y,text:'방패 충격파!',kind:'shockwave',side:f.side,team:f.team,life:.8});this.emit('🛡️ 방패 충격파!');this.resolvingBlast=true;for(const e of [...this.fighters]){if(e===f||e.health<=0)continue;const n=Math.min(e.health,100);e.health-=n;f.damageDealt+=n;e.flash=.15;this.effect(e,'−'+n);if(e.health>0)e.stunUntil=Math.max(e.stunUntil,this.time+3);if(e.health<=0){if(this.formEgg(e))continue;e.trail=[];this.emit(e.name+' 탈락!')}}this.resolvingBlast=false;this.checkEnd()}"""
if old not in s:
    raise SystemExit('PATCH FAILED: knight shockwave function not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('v3.16 knight shockwave hotfix applied')

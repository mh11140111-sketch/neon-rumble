from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="for(let side=0;side<2;side++){const old=this.fighters[side];if(old.health>0)continue;if(this.relayIndex[side]>=2){this.result=1-side;return}"
new="for(let side=0;side<2;side++){const old=this.fighters[side];if(old.skeletonBundle){const key=old.skeletonBundleKey||('legacy-'+(old.skeletonBundleLeader??old.side)),members=this.fighters.filter(x=>x.skeletonBundle&&(x.skeletonBundleKey||('legacy-'+(x.skeletonBundleLeader??x.side)))===key);if(members.some(x=>x.health>0))continue}if(old.health>0)continue;if(this.relayIndex[side]>=2){this.result=1-side;return}"
if s.count(old)!=1: raise SystemExit(f'relay guard target count={s.count(old)}')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('v3.35 skeleton relay round guard applied')

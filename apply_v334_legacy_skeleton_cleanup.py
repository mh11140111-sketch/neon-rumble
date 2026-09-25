from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old="const ROBOT_STAGE_KEY='neonRumble.robotStages.v1',SKELETON_UNLOCK_KEY='neonRumble.skeletonBundleUnlocked.v2';\nlet robotStageMask=0,skeletonsUnlocked=false;try{robotStageMask=Number(localStorage.getItem(ROBOT_STAGE_KEY)||0)||0;skeletonsUnlocked=localStorage.getItem(SKELETON_UNLOCK_KEY)==='1'}catch{}"
new="const ROBOT_STAGE_KEY='neonRumble.robotStages.v1',SKELETON_UNLOCK_KEY='neonRumble.skeletonBundleUnlocked.v2',LEGACY_SKELETON_UNLOCK_KEY='neonRumble.skeletonUnlocked.v1';\nlet robotStageMask=0,skeletonsUnlocked=false;try{localStorage.removeItem(LEGACY_SKELETON_UNLOCK_KEY);robotStageMask=Number(localStorage.getItem(ROBOT_STAGE_KEY)||0)||0;skeletonsUnlocked=localStorage.getItem(SKELETON_UNLOCK_KEY)==='1'}catch{}"

count=s.count(old)
if count!=1:
    raise SystemExit(f'expected one storage block, found {count}')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('legacy skeleton unlock data cleanup added')

from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

needle="function currentChoices(){return isBossMode()?[bossChoice,squad[Math.max(0,bossSlot)]]:['relay','group'].includes(mode)?relayTeams.map((t,i)=>t[relaySlots[i]]):selected}"
insert="function hideStageSelectionPanels(){for(const id of ['stage-panel','desert-panel','mansion-panel','space-panel','casino-panel','ocean-panel','forge-panel']){const el=$(id);if(el)el.hidden=true}}\n"+needle
if needle not in s:
    raise SystemExit('PATCH FAILED: currentChoices anchor missing')
s=s.replace(needle,insert,1)

old="$('selection').hidden=true;$('battle').hidden=false;"
count=s.count(old)
if count < 7:
    raise SystemExit(f'PATCH FAILED: expected stage/battle transition anchors, found {count}')
s=s.replace(old,"hideStageSelectionPanels();$('selection').hidden=true;$('battle').hidden=false;")

# Guard against accidental duplicate insertion.
if s.count('function hideStageSelectionPanels()') != 1:
    raise SystemExit('PATCH FAILED: hide helper count')
if "'ocean-panel','forge-panel'" not in s:
    raise SystemExit('PATCH FAILED: ocean/forge panels not covered')

p.write_text(s,encoding='utf-8')
print('patched transitions:',count)

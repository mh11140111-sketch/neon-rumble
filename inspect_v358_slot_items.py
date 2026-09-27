from pathlib import Path
s=Path('index.html').read_text(encoding='utf-8')
for k in ["slotMachineSkill(f,e){","dragon_rain","slotemoji","slotgrape","slotcoin","slotseven","BATTLE <b>v3.57</b>"]:
 print('\n###',k)
 i=s.find(k)
 print('INDEX',i)
 if i>=0: print(s[max(0,i-1800):i+6500])

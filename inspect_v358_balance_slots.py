from pathlib import Path
s=Path('index.html').read_text(encoding='utf-8')
keys=['dragon_rain','👒','🛴','🦽','250','도박장','gambl','casino','slot']
for k in keys:
 print('\n###',k)
 start=0
 shown=0
 while True:
  i=s.find(k,start)
  if i<0 or shown>=8: break
  print('INDEX',i)
  print(s[max(0,i-1800):i+4200])
  start=i+len(k);shown+=1

from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

assert 'BATTLE <b>v3.31</b>' in s
assert "id:'cowboy',name:'카우보이',icon:'🤠🐴'" in s
assert "ctx.fillText(f.icon,f.x,f.y+1);" in s

# Stack cowboy above horse in selection/UI text.
s=s.replace("id:'cowboy',name:'카우보이',icon:'🤠🐴'","id:'cowboy',name:'카우보이',icon:'🤠\\n🐴'",1)

# Make newline icons render vertically in selection cards.
s=s.replace(".chosen-icon{font-family:'Apple Color Emoji','Segoe UI Emoji',sans-serif;font-size:62px;line-height:1.5}",".chosen-icon{font-family:'Apple Color Emoji','Segoe UI Emoji',sans-serif;font-size:62px;line-height:1.05;white-space:pre-line;text-align:center}",1)
s=s.replace(".card-icon{font-size:30px}",".card-icon{font-size:30px;white-space:pre-line;text-align:center;line-height:1.05}",1)

# Stack rider above horse in arena while mounted; after dismount the existing 🤠 icon is used.
old="ctx.font=(39*f.bodyScale)+'px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.fillStyle='#fff';ctx.fillText(f.icon,f.x,f.y+1);"
new="ctx.font=(39*f.bodyScale)+'px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.fillStyle='#fff';if(f.id==='cowboy'&&f.cowboyMounted){ctx.font=(31*f.bodyScale)+'px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.fillText('🤠',f.x,f.y-14*f.bodyScale);ctx.fillText('🐴',f.x,f.y+18*f.bodyScale)}else{ctx.fillText(f.icon,f.x,f.y+1)}"
assert old in s
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')

s2=p.read_text(encoding='utf-8')
assert "id:'cowboy',name:'카우보이',icon:'🤠\\n🐴'" in s2
assert "f.id==='cowboy'&&f.cowboyMounted" in s2
assert "ctx.fillText('🤠',f.x,f.y-14*f.bodyScale)" in s2
assert "ctx.fillText('🐴',f.x,f.y+18*f.bodyScale)" in s2
assert 'BATTLE <b>v3.31</b>' in s2
print('cowboy mount stack hotfix applied')

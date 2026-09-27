from pathlib import Path
p=Path('apply_v354_chapter6.py')
s=p.read_text(encoding='utf-8')
old="""if 'id=\"ocean-panel\"' not in s:
    rep('</section><section id=\"battle\"',ocean_panel+'</section><section id=\"battle\"','ocean panel')
"""
new="""if 'id=\"ocean-panel\"' not in s:
    m=re.search(r'</section>\\s*<section id=\"battle\"',s)
    if not m: raise SystemExit('ocean panel regex anchor missing')
    original=m.group(0)
    replacement='</section>'+ocean_panel+original[len('</section>'):]
    s=s[:m.start()]+replacement+s[m.end():]
"""
if old not in s:
    raise SystemExit('old ocean panel block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('v3.54 ocean panel patch repaired')

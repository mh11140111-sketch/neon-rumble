from pathlib import Path

src=Path('apply_v336_shadow_skeleton_army.py').read_text(encoding='utf-8')
start=src.index("rep(\"{id:'cowboy',name:'카우보이'")
end=src.index("rep(\"{id:'ninja',name:'닌자'", start)
robust_cowboy=r'''# Robust cowboy block edit: source icon uses JS line continuation (backslash + real newline).
cs=s.index("{id:'cowboy',name:'카우보이'")
ce=s.index("\n{id:'chef',name:'요리사'",cs)
cb=s[cs:ce]
if "hp:1000,damage:100" not in cb or "detail:'HP 1000" not in cb:
    raise SystemExit('unexpected cowboy block')
cb=cb.replace("hp:1000,damage:100","hp:800,damage:100",1)
cb=cb.replace("이동속도가 100% 증가해. 피해 100","이동속도가 100% 증가해. 체력은 800. 피해 100",1)
cb=cb.replace("detail:'HP 1000","detail:'HP 800",1)
s=s[:cs]+cb+s[ce:]
'''
patched=src[:start]+robust_cowboy+src[end:]
exec(compile(patched,'apply_v336_shadow_skeleton_army_retry.generated.py','exec'))

import pathlib, shutil
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")
old = '    if(a.includes(norm) && norm.length>=4) return true;'
new = "    // removed: a.includes(norm) — чтобы 'крут' не триггерил"
if old in t:
    t=t.replace(old,new)
    print('removed substring check')
else:
    print('not found')
    for line in t.splitlines():
        if 'includes(norm)' in line:
            print(repr(line))
p.write_text(t, encoding="utf-8")
print('written local')
shutil.copy(r"C:\project\steve-minecraft-png\3d-local.html", r"C:\project\steve-minecraft-png\3d.html")
print('copied to 3d.html')
# verify
d=open(r"C:\project\steve-minecraft-png\3d-local.html",encoding="utf-8").read()
print('крут alias check', 'крут' in d)
print('has removed comment', 'чтобы' in d)

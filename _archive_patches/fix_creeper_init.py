import pathlib, shutil
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

if 'ach_creeper' not in t.split('spinCount')[0]:
    t = t.replace(
        '  jump: JSON.parse(localStorage.getItem("ach_jump")||"false"),',
        '  jump: JSON.parse(localStorage.getItem("ach_jump")||"false"),\n  creeper: JSON.parse(localStorage.getItem("ach_creeper")||"false"),',
        1
    )
    print("added creeper init")
else:
    print("already has creeper init in first part")

if 'creeperCount' not in t:
    t = t.replace(
        '  jumpCount: parseInt(localStorage.getItem("ach_jumpCount")||"0")',
        '  jumpCount: parseInt(localStorage.getItem("ach_jumpCount")||"0"),\n  creeperCount: parseInt(localStorage.getItem("ach_creeperCount")||"0")',
        1
    )
    print("added creeperCount")
else:
    print("already has creeperCount")

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("fixed len", len(t))
print("check", "ach_creeper" in t, "creeperCount" in t)

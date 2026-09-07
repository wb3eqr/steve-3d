import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# Fix 1: handleCmd duplicate - remove the wrong lie block that calls creeper
old_dup = """  } else if(matchesAliases(norm, lieAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("creeper");
    doCreeper();
    input.value="";
  } else if(matchesAliases(norm, lieAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("lie");
    doLie();
    input.value="";
  } else {"""

new_single = """  } else if(matchesAliases(norm, lieAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("lie");
    doLie();
    input.value="";
  } else {"""

if old_dup in t:
    t = t.replace(old_dup, new_single)
    print("fixed lie duplicate - now lie triggers doLie")
else:
    print("dup not found")
    # debug
    if 'lieAliases' in t:
        idx = t.find('lieAliases')
        print(repr(t[idx-200:idx+400]))

# Fix 2: achievements init missing lie and counts - add them
old_init = """  achievements = {
    spin: JSON.parse(localStorage.getItem("ach_spin")||"false"),
    salto: JSON.parse(localStorage.getItem("ach_salto")||"false"),
    hit: JSON.parse(localStorage.getItem("ach_hit")||"false"),
    invis: JSON.parse(localStorage.getItem("ach_invis")||"false"),
    crouch: JSON.parse(localStorage.getItem("ach_crouch")||"false"),
    jump: JSON.parse(localStorage.getItem("ach_jump")||"false"),
  creeper: JSON.parse(localStorage.getItem("ach_creeper")||"false"),
    spinCount: parseInt(localStorage.getItem("ach_spinCount")||"0"),
    saltoCount: parseInt(localStorage.getItem("ach_saltoCount")||"0"),
    hitCount: parseInt(localStorage.getItem("ach_hitCount")||"0"),
    invisCount: parseInt(localStorage.getItem("ach_invisCount")||"0"),
    crouchCount: parseInt(localStorage.getItem("ach_crouchCount")||"0"),
    jumpCount: parseInt(localStorage.getItem("ach_jumpCount")||"0")
  };"""

new_init = """  achievements = {
    spin: JSON.parse(localStorage.getItem("ach_spin")||"false"),
    salto: JSON.parse(localStorage.getItem("ach_salto")||"false"),
    hit: JSON.parse(localStorage.getItem("ach_hit")||"false"),
    invis: JSON.parse(localStorage.getItem("ach_invis")||"false"),
    crouch: JSON.parse(localStorage.getItem("ach_crouch")||"false"),
    jump: JSON.parse(localStorage.getItem("ach_jump")||"false"),
    creeper: JSON.parse(localStorage.getItem("ach_creeper")||"false"),
    lie: JSON.parse(localStorage.getItem("ach_lie")||"false"),
    spinCount: parseInt(localStorage.getItem("ach_spinCount")||"0"),
    saltoCount: parseInt(localStorage.getItem("ach_saltoCount")||"0"),
    hitCount: parseInt(localStorage.getItem("ach_hitCount")||"0"),
    invisCount: parseInt(localStorage.getItem("ach_invisCount")||"0"),
    crouchCount: parseInt(localStorage.getItem("ach_crouchCount")||"0"),
    jumpCount: parseInt(localStorage.getItem("ach_jumpCount")||"0"),
    creeperCount: parseInt(localStorage.getItem("ach_creeperCount")||"0"),
    lieCount: parseInt(localStorage.getItem("ach_lieCount")||"0")
  };"""

if old_init in t:
    t = t.replace(old_init, new_init)
    print("fixed achievements init")
else:
    print("old_init not found")
    # try to find achievements block
    m=re.search(r'let achievements;.*?jumpCount.*?0\)\n  \};', t, flags=re.DOTALL)
    if m:
        print(repr(m.group(0)[:300]))

# Fix 3: fallback achievements init in catch
if 'spin:false,salto:false,hit:false,invis:false,crouch:false,jump:false' in t:
    t = t.replace(
        'achievements = {spin:false,salto:false,hit:false,invis:false,crouch:false,jump:false,spinCount:0,saltoCount:0,hitCount:0,invisCount:0,crouchCount:0,jumpCount:0};',
        'achievements = {spin:false,salto:false,hit:false,invis:false,crouch:false,jump:false,creeper:false,lie:false,spinCount:0,saltoCount:0,hitCount:0,invisCount:0,crouchCount:0,jumpCount:0,creeperCount:0,lieCount:0};'
    )
    print("fixed fallback")

# Fix 4: creeper skin broken - regenerate a proper quality creeper skin 64x64 fully filled
from PIL import Image, ImageDraw
creeper_path = pathlib.Path(r"C:\project\steve-minecraft-png\creeper_quality_hd.png")
im = Image.new('RGBA', (64,64), (0,0,0,0))
# Use proper creeper palette with shading
base = (106,153,46,255)  # main green #6A9936
dark = (72,109,32,255)   # shadow #486D20
light = (140,190,80,255) # highlight #8CBE50
black = (20,20,20,255)
# Fill entire 64x64 with base first to avoid transparent holes
for x in range(64):
    for y in range(64):
        im.putpixel((x,y), (0,0,0,0))
# Head 32x16 area (0,0 - 32,16)
# Head top 8,0
for x in range(8,16):
    for y in range(0,8):
        # pattern
        if (x+y)%2==0:
            im.putpixel((x,y), light)
        else:
            im.putpixel((x,y), base)
# Head front with face
for x in range(8,16):
    for y in range(8,16):
        im.putpixel((x,y), base)
# creeper face - high contrast
# eyes
for x in range(9,11):
    for y in range(10,12):
        im.putpixel((x,y), black)
for x in range(13,15):
    for y in range(10,12):
        im.putpixel((x,y), black)
# mouth - classic creeper frown
for x in range(10,14):
    for y in range(12,15):
        if not (x==11 and y==12) and not (x==12 and y==12):
            # create mouth shape
            if y==12 and x in [10,13]:
                im.putpixel((x,y), black)
            elif y==13:
                im.putpixel((x,y), black)
            elif y==14 and x in [10,11,12,13]:
                im.putpixel((x,y), black)
# nose bridge
im.putpixel((11,12), black)
im.putpixel((12,12), black)
# Head sides
for x in range(0,8):
    for y in range(8,16):
        im.putpixel((x,y), dark if (x+y)%3==0 else base)
for x in range(16,24):
    for y in range(8,16):
        im.putpixel((x,y), dark)
for x in range(24,32):
    for y in range(8,16):
        im.putpixel((x,y), base)
# Head bottom
for x in range(16,24):
    for y in range(0,8):
        im.putpixel((x,y), dark)
# Body
for x in range(16,32):
    for y in range(16,32):
        if x>=20 and x<28 and y>=20 and y<32:
            # front - patchy
            if (x+y)%5==0:
                im.putpixel((x,y), light)
            elif (x+y)%7==0:
                im.putpixel((x,y), dark)
            else:
                im.putpixel((x,y), base)
        else:
            # sides/back
            if x<20 or x>=28:
                im.putpixel((x,y), dark)
            else:
                im.putpixel((x,y), base)
# Arms
for y in range(20,32):
    for x in range(40,48):
        # right arm front
        if x>=44 and x<48:
            im.putpixel((x,y), base if (x+y)%4 else light)
        else:
            im.putpixel((x,y), dark)
    for x in range(32,40):
        # left arm front (new layer)
        if x>=36 and x<40:
            im.putpixel((x,y+32), base) # actually second layer at 36,52 etc, but fill for now
# Arms second layer at 36,52 is left arm, 44,20 is right
# Fill all arm areas properly
for x in range(44,48):
    for y in range(20,32):
        im.putpixel((x,y), base)
for x in range(36,40):
    for y in range(52,64):
        im.putpixel((x,y), base)
for x in range(40,44):
    for y in range(20,32):
        im.putpixel((x,y), dark)
for x in range(48,52):
    for y in range(20,32):
        im.putpixel((x,y), dark)
# Legs
for x in range(0,8):
    for y in range(20,32):
        im.putpixel((x,y), dark)
for x in range(4,8):
    for y in range(20,32):
        im.putpixel((x,y), base if x==6 else dark)
for x in range(16,24):
    for y in range(52,64):
        im.putpixel((x,y), base)
for x in range(20,24):
    for y in range(52,64):
        im.putpixel((x,y), base)
# Fill any remaining transparent with base
for x in range(64):
    for y in range(64):
        if im.getpixel((x,y))[3]==0:
            # fill with base if in body area, otherwise transparent is ok for hat
            if y<32 and x<64:
                # keep hat transparent except head
                if not (32 <= x < 64 and 0 <= y < 16):
                    # if in main body area, fill with base
                    if (0 <= x < 32 and 0 <= y < 32) or (16 <= x < 56 and 32 <= y < 64):
                        im.putpixel((x,y), base)
            pass

im.save(creeper_path)
print("regenerated creeper hd quality", creeper_path.stat().st_size)
# Update b64 for creeper
import base64
creeper_b64 = base64.b64encode(creeper_path.read_bytes()).decode()
t = re.sub(r'const creeperB64 = "[^"]+";', f'const creeperB64 = "{creeper_b64}";', t, count=1)
print("updated creeperB64 len", len(creeper_b64))

# Fix text "СНОВА КОТИК" -> make consistent "СНОВА СТИВ-КОТИК" is fine, but user complains
# Change to neutral "ГОТОВО!"
t = t.replace('showToast("✅ СНОВА КОТИК!");', 'showToast("✅ ГОТОВО!");')
t = t.replace('showToast("✅ СНОВА СТИВ!");', 'showToast("✅ ГОТОВО!");')
print("fixed toast text")

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

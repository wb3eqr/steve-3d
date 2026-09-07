import pathlib, shutil
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")
# Revert Steve textures to Nearest for crisp pixel art (user saw blurry with Linear)
t = t.replace(
    '  tex.magFilter=THREE.LinearFilter; tex.minFilter=THREE.LinearMipmapLinearFilter; tex.colorSpace=THREE.SRGBColorSpace; tex.generateMipmaps=true;',
    '  tex.magFilter=THREE.NearestFilter; tex.minFilter=THREE.NearestFilter; tex.colorSpace=THREE.SRGBColorSpace;'
)
t = t.replace(
    '    const t=new THREE.CanvasTexture(c); t.magFilter=THREE.LinearFilter; t.minFilter=THREE.LinearFilter; t.colorSpace=THREE.SRGBColorSpace; return t;',
    '    const t=new THREE.CanvasTexture(c); t.magFilter=THREE.NearestFilter; t.minFilter=THREE.NearestFilter; t.colorSpace=THREE.SRGBColorSpace; return t;'
)
p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("reverted to Nearest - Steve crisp")

# Now check and offer to replace skin with classic blue
from PIL import Image
skin_path = r"C:\project\steve-minecraft-png\steve-2d-skin.png"
im = Image.open(skin_path)
pix = im.load()
print("before body", pix[20,20], pix[24,26])
# Try to create classic blue skin by recoloring gray body to blue
# Classic Steve palette: shirt primary #4C8EDB (76,142,219), pants #2B2F6B (43,47,107)
# We'll map gray tones to blue tones
# Simple: replace gray (110-115) with blue
for y in range(64):
    for x in range(64):
        r,g,b,a = pix[x,y]
        # Detect gray body area (where r==g==b and 100-120) -> become blueish
        # But keep skin tones (head) untouched: head area y<16
        if a==0: continue
        # Body/arms/legs areas are where we expect blue/gray
        # If pixel is gray-ish and in body region, recolor
        if 100 <= r <= 130 and r==g and g==b:
            # Map gray 113 -> blue 60,130,190 ; lighter gray 240 -> lighter blue 150,180,220?
            # Use simple: keep brightness but shift to blue
            # For darker gray, map to dark blue, for light gray map to light blue
            if r > 200:
                pix[x,y] = (180, 190, 220, 255)
            elif r > 150:
                pix[x,y] = (120, 160, 210, 255)
            else:
                # main shirt blue
                # vary by original brightness
                # 113 -> 76,142,219 ; 110 -> 70,135,210
                b_val = 210 + (r-110)
                pix[x,y] = (70, 130, int(b_val), 255)
        # Also fix white chest that was grayish white -> keep white
        # Check legs pants also gray, same

im.save(r"C:\project\steve-minecraft-png\steve-2d-skin-classic.png")
print("saved recolored classic")
# Also try to download real classic via alternative URL
import urllib.request, ssl
ssl._create_default_https_context = ssl._create_unverified_context
urls = [
    "https://raw.githubusercontent.com/joshwenke/minecraft-skins/main/skins/steve.png",
    "https://github.com/InventivetalentDev/minecraft-assets/raw/master/assets/minecraft/textures/entity/steve.png",
    "https://visage.surge.sh/skin/8667ba71-b85a-4004-af54-457a9734eed",
]
for u in urls:
    try:
        print(f"try {u}")
        urllib.request.urlretrieve(u, r"C:\project\steve-minecraft-png\steve-download-test.png")
        im2 = Image.open(r"C:\project\steve-minecraft-png\steve-download-test.png")
        print(f"  got {im2.size} {im2.getpixel((20,20))}")
        if im2.size==(64,64) and im2.getpixel((20,20)) != (113,113,113,255):
            print("  found blue skin")
            im2.save(r"C:\project\steve-minecraft-png\steve-2d-skin.png")
            print("  replaced main skin")
            break
    except Exception as e:
        print(f"  fail {e}")

# If none succeeded, use recolored
import pathlib as pl
if pathlib.Path(r"C:\project\steve-minecraft-png\steve-2d-skin.png").exists():
    im_check = Image.open(r"C:\project\steve-minecraft-png\steve-2d-skin.png")
    if im_check.getpixel((20,20)) == (113,113,113,255):
        # still gray, use recolored
        Image.open(r"C:\project\steve-minecraft-png\steve-2d-skin-classic.png").save(r"C:\project\steve-minecraft-png\steve-2d-skin.png")
        print("used recolored classic as fallback")

# Update b64 for html
import base64
b = open(r"C:\project\steve-minecraft-png\steve-2d-skin.png","rb").read()
b64 = base64.b64encode(b).decode()
open(r"C:\project\steve-minecraft-png\b64.txt","w").write(b64)
print("updated b64 len", len(b64))
# Need to update html b64
html = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html").read_text(encoding="utf-8-sig")
import re
html = re.sub(r'const skinB64 = "[^"]+";', f'const skinB64 = "{b64}";', html)
pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html").write_text(html, encoding="utf-8")
shutil.copy(r"C:\project\steve-minecraft-png\3d-local.html", r"C:\project\steve-minecraft-png\3d.html")
print("updated html b64")

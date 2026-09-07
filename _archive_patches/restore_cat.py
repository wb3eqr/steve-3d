import base64, pathlib, re, shutil
b = pathlib.Path(r"C:\project\steve-minecraft-png\steve-2d-skin.png").read_bytes()
b64 = base64.b64encode(b).decode()
pathlib.Path(r"C:\project\steve-minecraft-png\b64.txt").write_text(b64, encoding="utf-8")
print("b64 len", len(b64))
html_path = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
html = html_path.read_text(encoding="utf-8-sig")
html = re.sub(r'const skinB64 = "[^"]+";', f'const skinB64 = "{b64}";', html)
html_path.write_text(html, encoding="utf-8")
shutil.copy(r"C:\project\steve-minecraft-png\3d-local.html", r"C:\project\steve-minecraft-png\3d.html")
print("updated html crisp cat")
from PIL import Image
im = Image.open(r"C:\project\steve-minecraft-png\steve-2d-skin.png")
print("cat body", im.getpixel((20,20)), im.getpixel((24,26)))

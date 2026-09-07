import pathlib, shutil
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# 1. Fix CSS: make fonts larger and less pixelated, remove pixelated rendering from UI
t = t.replace(
    '  @import url(\'https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap\');',
    '  @import url(\'https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@500;600&display=swap\');'
)
# Replace body font
t = t.replace(
    '  body{background:#1e1e1e;overflow:hidden;font-family:"Press Start 2P", monospace}',
    '  body{background:#1e1e1e;overflow:hidden;font-family:"Inter", system-ui, sans-serif}'
)
# mc-bar: increase padding, remove image-rendering pixelated, make more readable
t = t.replace(
    '    image-rendering:pixelated;',
    '    image-rendering:auto;'
)
# mc-label: 8px -> 11px, Press Start -> Inter, better contrast
t = t.replace(
    '  .mc-label{\n    font-size:8px;color:#3a3a3a;letter-spacing:0;\n    text-shadow:1px 1px 0 #fff;',
    '  .mc-label{\n    font-size:12px;color:#2b2b2b;letter-spacing:0.2px;\n    text-shadow:none; font-weight:600;'
)
# mc-input: 8px Press Start 260px -> 13px Inter
t = t.replace(
    '  .mc-input{\n    background:transparent;\n    border:0;\n    color:#fff;\n    font-family:"Press Start 2P", monospace;\n    font-size:8px;\n    padding:8px 10px;\n    width:260px;',
    '  .mc-input{\n    background:transparent;\n    border:0;\n    color:#fff;\n    font-family:"Inter", system-ui, sans-serif;\n    font-size:13px;\n    padding:10px 12px;\n    width:300px;'
)
t = t.replace(
    '  .mc-input::placeholder{color:#8b8b8b}',
    '  .mc-input::placeholder{color:#9a9a9a; font-size:12px}'
)
# mc-btn: 10px -> 12px
t = t.replace(
    '    font-family:"Press Start 2P", monospace;\n    font-size:10px;',
    '    font-family:"Inter", system-ui, sans-serif;\n    font-size:13px; font-weight:600;'
)
# book-btn: 7px -> 11px
t = t.replace(
    '    font-family:"Press Start 2P", monospace;\n    font-size:7px;\n    padding:7px 10px;',
    '    font-family:"Inter", system-ui, sans-serif;\n    font-size:12px;\n    padding:8px 12px; font-weight:600;'
)
# book-modal title 10px -> 14px
t = t.replace(
    '  .book-title{font-size:10px;color:#5C2E0C;text-align:center;margin-bottom:10px;text-shadow:1px 1px 0 #FFF}',
    '  .book-title{font-size:14px;color:#5C2E0C;text-align:center;margin-bottom:12px;font-weight:700}'
)
# book-entry 7px -> 12px, icon larger
t = t.replace(
    '  .book-entry{\n    display:flex;align-items:center;gap:8px;\n    font-size:7px;color:#373737;',
    '  .book-entry{\n    display:flex;align-items:center;gap:10px;\n    font-size:12px;color:#373737; line-height:1.4;'
)
t = t.replace(
    '  .book-entry .icon{width:18px;height:18px;display:flex;align-items:center;justify-content:center;background:#C6C6C6;border:1px solid #8B8B8B;flex-shrink:0;font-size:10px}',
    '  .book-entry .icon{width:22px;height:22px;display:flex;align-items:center;justify-content:center;background:#C6C6C6;border:1px solid #8B8B8B;flex-shrink:0;font-size:12px}'
)
t = t.replace(
    '    font-family:"Press Start 2P",monospace;font-size:8px;',
    '    font-family:"Inter", system-ui, sans-serif;font-size:12px; font-weight:600;'
)
t = t.replace(
    '  .book-close{\n    margin-top:10px;width:100%;\n    background:#C6C6C6;\n    border:2px solid #000;\n    border-top-color:#FFF; border-left-color:#FFF; border-right-color:#555; border-bottom-color:#555;\n    font-family:"Press Start 2P",monospace;font-size:7px;padding:7px;cursor:pointer;',
    '  .book-close{\n    margin-top:12px;width:100%;\n    background:#C6C6C6;\n    border:2px solid #000;\n    border-top-color:#FFF; border-left-color:#FFF; border-right-color:#555; border-bottom-color:#555;\n    font-family:"Inter", system-ui, sans-serif;font-size:12px;padding:10px;cursor:pointer; font-weight:600;'
)
# hint: make larger
t = t.replace(
    '  .hint{position:fixed;bottom:10px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.55);color:#aaa;font-family:monospace;font-size:11px;padding:5px 10px;border-radius:20px;letter-spacing:0.3px}',
    '  .hint{position:fixed;bottom:10px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.65);color:#ddd;font-family:"Inter", system-ui, sans-serif;font-size:12px;padding:7px 14px;border-radius:20px}'
)
# Make modal wider
t = t.replace(
    '    width:360px;max-width:90vw;',
    '    width:440px;max-width:92vw;'
)

# 2. JS: change texture filtering from Nearest to Linear for smoother 3D (less pixel лесенка)
# Replace all NearestFilter with LinearFilter for smoother, keep one Nearest for optional sharpness
t = t.replace(
    '  tex.magFilter=THREE.NearestFilter; tex.minFilter=THREE.NearestFilter; tex.colorSpace=THREE.SRGBColorSpace;',
    '  tex.magFilter=THREE.LinearFilter; tex.minFilter=THREE.LinearMipmapLinearFilter; tex.colorSpace=THREE.SRGBColorSpace; tex.generateMipmaps=true;'
)
# For faceTex CanvasTexture
t = t.replace(
    '    const t=new THREE.CanvasTexture(c); t.magFilter=THREE.NearestFilter; t.minFilter=THREE.NearestFilter; t.colorSpace=THREE.SRGBColorSpace; return t;',
    '    const t=new THREE.CanvasTexture(c); t.magFilter=THREE.LinearFilter; t.minFilter=THREE.LinearFilter; t.colorSpace=THREE.SRGBColorSpace; return t;'
)
# Renderer: ensure antialias and high quality
t = t.replace(
    'renderer.setPixelRatio(devicePixelRatio);',
    'renderer.setPixelRatio(Math.min(devicePixelRatio, 2));'
)

# 3. Make book entries small text larger (5px -> 10px)
t = t.replace(
    '<small style="font-size:5px;color:#8B8B8B">',
    '<small style="font-size:10px;color:#6B6B6B">'
)
t = t.replace(
    '<small>выполнено:',
    '<small style="font-size:11px;color:#555">выполнено:'
)

# 4. Increase toast font
t = t.replace(
    '  #toast{\n    position:fixed;top:70px;left:50%;transform:translateX(-50%);\n    background:#ffff55;color:#000;font-family:"Press Start 2P",monospace;font-size:8px;',
    '  #toast{\n    position:fixed;top:70px;left:50%;transform:translateX(-50%);\n    background:#ffff55;color:#000;font-family:"Inter", system-ui, sans-serif;font-size:13px; font-weight:600;'
)

p.write_text(t, encoding="utf-8")
print("fixed pixelation")
shutil.copy(r"C:\project\steve-minecraft-png\3d-local.html", r"C:\project\steve-minecraft-png\3d.html")
print("copied")
# verify
d=open(r"C:\project\steve-minecraft-png\3d-local.html",encoding="utf-8").read()
print("Inter" in d, "LinearFilter" in d, "Press Start 2P" in d)

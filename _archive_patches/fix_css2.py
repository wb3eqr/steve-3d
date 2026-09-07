import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# Direct replacements for remaining redesign artifacts
# Body
t = t.replace("body{background:radial-gradient(ellipse at top, #2a2a30 0%, #1a1a1e 55%, #0f0f12 100%);overflow:hidden;font-family:\"Inter\", system-ui, sans-serif}", "body{background:#1e1e1e;overflow:hidden;font-family:\"Inter\", system-ui, sans-serif}")
print("body reverted" if "radial-gradient" not in t else "still radial")

# mc-bar redesign -> revert to clean
# The redesigned mc-bar has specific strings
old_mc = """  .mc-bar{
    position:fixed;top:16px;left:50%;transform:translateX(-50%);
    display:flex;align-items:center;gap:8px;
    background:linear-gradient(180deg, #D4D4D4 0%, #C6C6C6 100%);
    border:1.5px solid #1a1a1a;
    border-radius:10px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.85), inset 0 -2px 0 rgba(0,0,0,0.15);
    padding:8px 10px 8px 12px;
    z-index:10;
    backdrop-filter: blur(6px);
    transition: box-shadow 0.2s, transform 0.15s;
  }
  .mc-bar:focus-within{ box-shadow: 0 10px 28px rgba(0,0,0,0.5), 0 0 0 2px rgba(85,255,85,0.35), inset 0 1px 0 rgba(255,255,255,0.9); transform:translateX(-50%) translateY(-1px); }"""

new_mc = """  .mc-bar{
    position:fixed;top:18px;left:50%;transform:translateX(-50%);
    display:flex;align-items:center;gap:6px;
    background:#C6C6C6;
    border:2px solid #000;
    box-shadow: inset -2px -2px 0 #555, inset 2px 2px 0 #FFF, 0 4px 12px rgba(0,0,0,0.5);
    padding:6px 8px;
    z-index:10;
    image-rendering:auto;
  }"""

if old_mc in t:
    t = t.replace(old_mc, new_mc)
    print("mc-bar reverted")
else:
    print("mc-bar old not found")
    # try to find mc-bar block
    import re as re2
    m=re2.search(r'\.mc-bar\{.*?\.mc-bar:focus-within\{.*?\}', t, flags=re2.DOTALL)
    if m:
        print(repr(m.group(0)[:300]))

# mc-label, input-wrap, input, btn etc were already reverted partially? Check if they still have redesign
# The previous revert already handled mc-label etc via earlier script but main css block failed, so mc-label may still be redesign (11px uppercase)
# We'll ensure they are clean as in old_clean
# Replace mc-label redesign
t = t.replace(
    '  .mc-label{\n    font-size:11px;color:#3a3a3a;letter-spacing:0.6px;\n    text-transform:uppercase; font-weight:800;',
    '  .mc-label{\n    font-size:12px;color:#2b2b2b;letter-spacing:0.2px;\n    text-shadow:none; font-weight:600;'
)
# Replace mc-input-wrap redesign
t = t.replace(
    '    background:linear-gradient(180deg, #1e1e1e 0%, #0f0f0f 100%);\n    border:1.5px solid #3a3a3a;\n    border-radius:8px;\n    box-shadow: inset 0 2px 4px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.05);',
    '    background:#000;\n    border:2px solid #555;\n    box-shadow: inset 2px 2px 0 #000;'
)
t = t.replace('    border-radius:8px;\n    box-shadow: inset 0 2px 4px', '    box-shadow: inset 2px 2px 0')
# Replace mc-input redesign
t = t.replace('    font-size:13.5px;\n    font-weight:500;\n    padding:10px 14px;', '    font-size:13px;\n    padding:10px 12px;')
# Replace mc-btn redesign
old_btn = """  .mc-btn{
    background:linear-gradient(180deg, #6CCB5A 0%, #4CAF50 100%);
    border:1.5px solid #2d7a2d;
    border-radius:8px;
    color:#fff;
    font-family:"Inter", system-ui, sans-serif;
    font-size:14px; font-weight:700;
    padding:8px 14px;
    cursor:pointer;
    text-shadow:0 1px 0 rgba(0,0,0,0.25);
    box-shadow: 0 2px 0 #2d7a2d, 0 4px 10px rgba(76,175,80,0.3);
    user-select:none;
    transition: transform 0.08s, box-shadow 0.08s, filter 0.15s;
  }
  .mc-btn:hover{ filter: brightness(1.07); transform:translateY(-1px); box-shadow: 0 3px 0 #2d7a2d, 0 6px 14px rgba(76,175,80,0.35); }
  .mc-btn:active{
    transform:translateY(1px);
    box-shadow: 0 1px 0 #2d7a2d;
  }"""
new_btn = """  .mc-btn{
    background:#8B8B8B;
    border:2px solid #000;
    border-top-color:#FFF;
    border-left-color:#FFF;
    border-right-color:#555;
    border-bottom-color:#555;
    color:#fff;
    font-family:"Inter", system-ui, sans-serif;
    font-size:13px; font-weight:600;
    padding:6px 10px;
    cursor:pointer;
    text-shadow:1px 1px 0 #373737;
    user-select:none;
  }
  .mc-btn:active{
    border-top-color:#555;
    border-left-color:#555;
    border-right-color:#FFF;
    border-bottom-color:#FFF;
    transform:translate(1px,1px);
  }
  .mc-btn:hover{background:#9a9a9a}"""
if old_btn in t:
    t = t.replace(old_btn, new_btn)
    print("btn reverted")

# Remove any remaining backdrop-filter
t = re.sub(r'backdrop-filter:[^;]+;', '', t)
# Remove canvas filter
t = t.replace("canvas{display:block; filter: contrast(1.02) saturate(1.05)}", "canvas{display:block}")

# Fix invisibility to smooth quick
if "fadeOut=140" in t:
    # Already has quick, but ensure it's the smooth version we set
    print("invis quick present")
else:
    print("invis not quick")

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

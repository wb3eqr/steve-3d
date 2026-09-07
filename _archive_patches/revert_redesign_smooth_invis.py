import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# Revert CSS redesign to previous clean version (before redesign_invis.py)
# Replace new body/canvas/mc-bar etc with old clean version
# Old clean CSS (from before redesign) was:
old_clean_css = """  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#1e1e1e;overflow:hidden;font-family:"Inter", system-ui, sans-serif}
  canvas{display:block}
  /* Minecraft mini command field - top center */
  .mc-bar{
    position:fixed;top:18px;left:50%;transform:translateX(-50%);
    display:flex;align-items:center;gap:6px;
    background:#C6C6C6;
    border:2px solid #000;
    box-shadow: inset -2px -2px 0 #555, inset 2px 2px 0 #FFF, 0 4px 12px rgba(0,0,0,0.5);
    padding:6px 8px;
    z-index:10;
    image-rendering:auto;
  }
  .mc-label{
    font-size:12px;color:#2b2b2b;letter-spacing:0.2px;
    text-shadow:none; font-weight:600;
    white-space:nowrap;
    user-select:none;
  }
  .mc-input-wrap{
    display:flex;align-items:center;
    background:#000;
    border:2px solid #555;
    box-shadow: inset 2px 2px 0 #000;
    padding:0;
  }
  .mc-input{
    background:transparent;
    border:0;
    color:#fff;
    font-family:"Inter", system-ui, sans-serif;
    font-size:13px;
    padding:10px 12px;
    width:300px;
    outline:none;
    letter-spacing:0.5px;
  }
  .mc-input::placeholder{color:#9a9a9a; font-size:12px}
  .mc-btn{
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
  .mc-btn:hover{background:#9a9a9a}
  .hint{position:fixed;bottom:10px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.65);color:#ddd;font-family:"Inter", system-ui, sans-serif;font-size:12px;padding:7px 14px;border-radius:20px}"""

# The current redesign CSS starts with radial-gradient and has new mc-bar etc.
# Find the block from "*{margin" to ".hint" and replace
m = re.search(r'\s*\*\{margin:0;.*?\.hint\{.*?border-radius:20px\}', t, flags=re.DOTALL)
if m:
    # The above will match the redesigned css (with gradient etc)
    # Replace with old clean
    t = t.replace(m.group(0), "\n" + old_clean_css)
    print("reverted main css to clean")
else:
    print("main css block not found")

# Revert toast to previous clean (without gradient)
# Current toast has gradient, old had #ffff55
if "linear-gradient(180deg, #FFEb3B" in t:
    t = t.replace(
        '  #toast{\n    position:fixed;top:72px;left:50%;transform:translateX(-50%);\n    background:linear-gradient(180deg, #FFEb3B 0%, #FFC107 100%);color:#1a1a1a;font-family:"Inter", system-ui, sans-serif;font-size:13px; font-weight:700;\n    padding:10px 16px;border:1px solid rgba(0,0,0,0.12);border-radius:10px;box-shadow:0 8px 20px rgba(0,0,0,0.3), 0 2px 0 rgba(0,0,0,0.08);',
        '  #toast{\n    position:fixed;top:70px;left:50%;transform:translateX(-50%);\n    background:#ffff55;color:#000;font-family:"Inter", system-ui, sans-serif;font-size:13px; font-weight:600;\n    padding:8px 12px;border:2px solid #000;box-shadow:4px 4px 0 rgba(0,0,0,0.5);'
    )
    print("reverted toast")

# Revert book btn
if "linear-gradient(180deg, #8B4513" in t:
    t = t.replace(
        '  .book-btn{\n    background:linear-gradient(180deg, #8B4513 0%, #6d3510 100%);\n    border:1.5px solid #4a230b;\n    border-radius:8px;\n    color:#FFD700;\n    font-family:"Inter", system-ui, sans-serif;\n    font-size:12px;\n    padding:8px 12px; font-weight:700; box-shadow:0 2px 0 #4a230b, 0 4px 10px rgba(0,0,0,0.25);',
        '  .book-btn{\n    background:#8B4513;\n    border:2px solid #000;\n    border-top-color:#D2A679;\n    border-left-color:#D2A679;\n    border-right-color:#5C2E0C;\n    border-bottom-color:#5C2E0C;\n    color:#FFD700;\n    font-family:"Inter", system-ui, sans-serif;\n    font-size:12px;\n    padding:8px 12px; font-weight:600;'
    )
    t = t.replace(
        '  .book-btn:active{transform:translateY(1px); box-shadow:0 1px 0 #4a230b;}',
        '  .book-btn:active{transform:translate(1px,1px); border-top-color:#5C2E0C; border-left-color:#5C2E0C; border-right-color:#D2A679; border-bottom-color:#D2A679;}'
    )
    print("reverted book btn")

# Revert book modal
if "linear-gradient(180deg, #FFF8E1" in t:
    t = t.replace(
        '  .book-modal{\n    position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);\n    width:460px;max-width:92vw;\n    background:linear-gradient(180deg, #FFF8E1 0%, #F9E4B7 100%);\n    border:1.5px solid #8B4513;\n    border-radius:14px;\n    box-shadow: 0 20px 50px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.9);',
        '  .book-modal{\n    position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);\n    width:440px;max-width:92vw;\n    background:#F9E4B7;\n    border:4px solid #5C2E0C;\n    box-shadow: inset -4px -4px 0 #D2A679, inset 4px 4px 0 #FFF, 0 8px 24px rgba(0,0,0,0.6);'
    )
    print("reverted book modal")

# Fix invisibility to be smooth and quick without scale/brightness jank
old_invis2 = re.search(r'function doInvisibility\(\)\{.*?steveGroup\.visible=true;\s*spinning=false;\s*showToast\("👻 ПОЯВИЛСЯ!"\);\s*\}\s*requestAnimationFrame\(frame\);\s*\}', t, flags=re.DOTALL)
if old_invis2:
    new_invis_smooth = """function doInvisibility(){
  if(!steveGroup || spinning) return;
  spinning=true;
  const mats=[];
  steveGroup.traverse(o=>{ if(o.isMesh) mats.push(o.material); });
  mats.forEach(m=>{ m.transparent=true; });
  const fadeOut=180, stay=4000, fadeIn=180;
  const total=fadeOut+stay+fadeIn;
  const start=performance.now();
  function easeOut(t){ return 1 - Math.pow(1-t,3); }
  function easeIn(t){ return t*t*t; }
  function frame(now){
    const e=now-start;
    let opacity=1;
    if(e<fadeOut){
      opacity = 1 - easeOut(e/fadeOut);
    } else if(e < fadeOut+stay){
      opacity = 0;
    } else if(e < total){
      opacity = easeIn((e-fadeOut-stay)/fadeIn);
    } else {
      opacity=1;
    }
    mats.forEach(m=>{ m.opacity=opacity; m.needsUpdate=true; });
    if(e < total){
      requestAnimationFrame(frame);
    } else {
      mats.forEach(m=>{ m.opacity=1; m.transparent=false; m.needsUpdate=true; });
      spinning=false;
      showToast("НЕВИДИМОСТЬ 4с 👻");
    }
  }
  requestAnimationFrame(frame);
}"""
    t = t.replace(old_invis2.group(0), new_invis_smooth)
    print("fixed invis smooth quick")

# Ensure canvas filter removed (was added in redesign)
t = t.replace("canvas{display:block; filter: contrast(1.02) saturate(1.05)}", "canvas{display:block}")

# Slight visual improvement (ак лично) - keep clean but add subtle polish without redesign
# Add subtle body background slightly lighter and canvas shadow, keep Inter
if "backdrop-filter: blur(6px)" in t:
    # already removed, but ensure no blur left
    t = re.sub(r'backdrop-filter:[^;]+;', '', t)
    print("removed blur")

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

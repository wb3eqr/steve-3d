import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# === 1. CSS redesign - small but maximal improvement ===
old_css = """  *{margin:0;padding:0;box-sizing:border-box}
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

new_css = """  *{margin:0;padding:0;box-sizing:border-box}
  body{background:radial-gradient(ellipse at top, #2a2a30 0%, #1a1a1e 55%, #0f0f12 100%);overflow:hidden;font-family:"Inter", system-ui, sans-serif}
  canvas{display:block; filter: contrast(1.02) saturate(1.05)}
  /* Minecraft mini command field - top center - редизайн */
  .mc-bar{
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
  .mc-bar:focus-within{ box-shadow: 0 10px 28px rgba(0,0,0,0.5), 0 0 0 2px rgba(85,255,85,0.35), inset 0 1px 0 rgba(255,255,255,0.9); transform:translateX(-50%) translateY(-1px); }
  .mc-label{
    font-size:11px;color:#3a3a3a;letter-spacing:0.6px;
    text-transform:uppercase; font-weight:800;
    white-space:nowrap;
    user-select:none;
    opacity:0.9;
  }
  .mc-input-wrap{
    display:flex;align-items:center;
    background:linear-gradient(180deg, #1e1e1e 0%, #0f0f0f 100%);
    border:1.5px solid #3a3a3a;
    border-radius:8px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.05);
    padding:0;
    overflow:hidden;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .mc-bar:focus-within .mc-input-wrap{ border-color:#55ff55; box-shadow: inset 0 2px 4px rgba(0,0,0,0.6), 0 0 0 2px rgba(85,255,85,0.15); }
  .mc-input{
    background:transparent;
    border:0;
    color:#fff;
    font-family:"Inter", system-ui, sans-serif;
    font-size:13.5px;
    font-weight:500;
    padding:10px 14px;
    width:300px;
    outline:none;
    letter-spacing:0.2px;
  }
  .mc-input::placeholder{color:#8a8a8a; font-size:12.5px; font-weight:400}
  .mc-btn{
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
  }
  .hint{position:fixed;bottom:12px;left:50%;transform:translateX(-50%);background:rgba(20,20,22,0.72);backdrop-filter:blur(8px);color:#d6d6d6;font-family:"Inter", system-ui, sans-serif;font-size:11.5px;font-weight:500;padding:8px 16px;border-radius:999px;border:1px solid rgba(255,255,255,0.08);box-shadow:0 4px 16px rgba(0,0,0,0.35);letter-spacing:0.2px}"""

if old_css in t:
    t = t.replace(old_css, new_css)
    print("redesigned css")
else:
    print("old_css not found, trying partial")
    # fallback: just ensure body gradient
    if "radial-gradient" not in t:
        t = t.replace("body{background:#1e1e1e;", "body{background:radial-gradient(ellipse at top, #2a2a30 0%, #1a1a1e 55%, #0f0f12 100%);")
        print("added gradient")

# Toast redesign
t = t.replace(
    '  #toast{\n    position:fixed;top:70px;left:50%;transform:translateX(-50%);\n    background:#ffff55;color:#000;font-family:"Inter", system-ui, sans-serif;font-size:13px; font-weight:600;\n    padding:8px 12px;border:2px solid #000;box-shadow:4px 4px 0 rgba(0,0,0,0.5);',
    '  #toast{\n    position:fixed;top:72px;left:50%;transform:translateX(-50%);\n    background:linear-gradient(180deg, #FFEb3B 0%, #FFC107 100%);color:#1a1a1a;font-family:"Inter", system-ui, sans-serif;font-size:13px; font-weight:700;\n    padding:10px 16px;border:1px solid rgba(0,0,0,0.12);border-radius:10px;box-shadow:0 8px 20px rgba(0,0,0,0.3), 0 2px 0 rgba(0,0,0,0.08);'
)
print("toast redesigned")

# Book button redesign to match new style
t = t.replace(
    '  .book-btn{\n    background:#8B4513;\n    border:2px solid #000;\n    border-top-color:#D2A679;\n    border-left-color:#D2A679;\n    border-right-color:#5C2E0C;\n    border-bottom-color:#5C2E0C;\n    color:#FFD700;\n    font-family:"Inter", system-ui, sans-serif;\n    font-size:12px;\n    padding:8px 12px; font-weight:600;',
    '  .book-btn{\n    background:linear-gradient(180deg, #8B4513 0%, #6d3510 100%);\n    border:1.5px solid #4a230b;\n    border-radius:8px;\n    color:#FFD700;\n    font-family:"Inter", system-ui, sans-serif;\n    font-size:12px;\n    padding:8px 12px; font-weight:700; box-shadow:0 2px 0 #4a230b, 0 4px 10px rgba(0,0,0,0.25);'
)
t = t.replace(
    '  .book-btn:active{transform:translate(1px,1px); border-top-color:#5C2E0C; border-left-color:#5C2E0C; border-right-color:#D2A679; border-bottom-color:#D2A679;}',
    '  .book-btn:active{transform:translateY(1px); box-shadow:0 1px 0 #4a230b;}'
)
print("book btn redesigned")

# Book modal more rounded and blur
t = t.replace(
    '  .book-modal{\n    position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);\n    width:440px;max-width:92vw;\n    background:#F9E4B7;\n    border:4px solid #5C2E0C;\n    box-shadow: inset -4px -4px 0 #D2A679, inset 4px 4px 0 #FFF, 0 8px 24px rgba(0,0,0,0.6);',
    '  .book-modal{\n    position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);\n    width:460px;max-width:92vw;\n    background:linear-gradient(180deg, #FFF8E1 0%, #F9E4B7 100%);\n    border:1.5px solid #8B4513;\n    border-radius:14px;\n    box-shadow: 0 20px 50px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.9);'
)
print("book modal redesigned")

# === 2. Fix invisibility to be quick smooth beautiful ===
old_invis = """function doInvisibility(){
  if(!steveGroup || spinning) return;
  spinning=true;
  showToast("НЕВИДИМОСТЬ 4с 👻");
  // Сохраняем материалы и делаем плавное исчезновение
  const mats=[];
  steveGroup.traverse(o=>{ if(o.isMesh) mats.push(o.material); });
  mats.forEach(m=>{ m.transparent=true; m.depthWrite=false; });
  const fade=200;
  const stay=4000;
  const start=performance.now();
  function frame(now){
    const e=now-start;
    let opacity=1;
    if(e<fade){
      opacity = 1 - e/fade;
    } else if(e < fade+stay){
      opacity = 0;
    } else if(e < fade*2+stay){
      opacity = (e-fade-stay)/fade;
    } else {
      opacity = 1;
    }
    mats.forEach(m=>{ m.opacity=opacity; m.needsUpdate=true; });
    // также скрываем полностью когда opacity ~0 чтобы не было артефактов
    steveGroup.visible = opacity>0.01 || e<fade || e>=fade+stay;
    if(e < fade*2+stay){
      requestAnimationFrame(frame);
    } else {
      mats.forEach(m=>{ m.opacity=1; m.transparent=false; m.depthWrite=true; m.needsUpdate=true; });
      steveGroup.visible=true;
      spinning=false;
    }
  }
  requestAnimationFrame(frame);
}"""

new_invis = """function doInvisibility(){
  if(!steveGroup || spinning) return;
  spinning=true;
  showToast("✨ ИСЧЕЗ... 4с 👻");
  const mats=[];
  steveGroup.traverse(o=>{ if(o.isMesh) mats.push(o.material); });
  mats.forEach(m=>{ m.transparent=true; m.depthWrite=false; });
  const fadeOut=140, stay=4000, fadeIn=220;
  const total=fadeOut+stay+fadeIn;
  const start=performance.now();
  // красивый эффект: слегка сжимается и уходит в прозрачность с ease
  const startScale=steveGroup.scale.clone();
  function easeOutCubic(t){ return 1 - Math.pow(1-t,3); }
  function easeInCubic(t){ return t*t*t; }
  function frame(now){
    const e=now-start;
    let opacity=1;
    let scale=1;
    let yOff=0;
    if(e<fadeOut){
      const t=e/fadeOut;
      const k=easeOutCubic(t);
      opacity = 1 - k;
      scale = 1 - k*0.04;
      yOff = k*0.4;
    } else if(e < fadeOut+stay){
      opacity = 0;
      scale = 0.96;
    } else if(e < total){
      const t=(e-fadeOut-stay)/fadeIn;
      const k=easeInCubic(t);
      opacity = k;
      scale = 0.96 + k*0.04;
      yOff = (1-k)*0.4;
    } else {
      opacity=1; scale=1; yOff=0;
    }
    mats.forEach(m=>{ m.opacity=opacity; m.needsUpdate=true; });
    steveGroup.scale.set(scale,scale,scale);
    steveGroup.position.y = (steveGroup.position.y||0) + (yOff - (steveGroup._yOff||0));
    steveGroup._yOff = yOff;
    steveGroup.visible = opacity>0.015 || e<fadeOut || e>=fadeOut+stay;
    // легкое свечение в момент исчезновения
    if(e<fadeOut) renderer.domElement.style.filter = `brightness(${1+ (1-opacity)*0.15})`;
    else if(e<fadeOut+stay) renderer.domElement.style.filter = "";
    else if(e<total) renderer.domElement.style.filter = `brightness(${1+ (1-opacity)*0.08})`;
    if(e < total){
      requestAnimationFrame(frame);
    } else {
      mats.forEach(m=>{ m.opacity=1; m.transparent=false; m.depthWrite=true; m.needsUpdate=true; });
      steveGroup.visible=true;
      steveGroup.scale.copy(startScale);
      steveGroup._yOff=0;
      renderer.domElement.style.filter="";
      spinning=false;
      showToast("👻 ПОЯВИЛСЯ!");
    }
  }
  requestAnimationFrame(frame);
}"""

if old_invis in t:
    t = t.replace(old_invis, new_invis)
    print("invis quick smooth beautiful done")
else:
    print("old invis not found, trying search")
    import re as re2
    m=re2.search(r'function doInvisibility.*?spinning=false;', t, flags=re2.DOTALL)
    if m:
        print(repr(m.group(0)[:200]))

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

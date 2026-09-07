import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# 1. Remove hint
t = re.sub(r'<div class="hint">.*?</div>\s*', '', t, flags=re.DOTALL)
print("hint removed" if 'class="hint"' not in t else "hint still there")

# Also remove hint CSS
t = re.sub(r'\s*\.hint\{[^}]+\}', '', t)
print("hint css removed" if ".hint{" not in t else "hint css still")

# 2. Ensure viewport supports all devices (already has meta viewport, but improve)
t = t.replace(
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">\n<meta name="theme-color" content="#1a1a1e">\n<meta name="apple-mobile-web-app-capable" content="yes">'
)
print("viewport enhanced")

# 3. Add responsive + all-devices CSS
responsive_css = """
  /* === поддержка всех устройств === */
  canvas{touch-action:none; -webkit-user-select:none; user-select:none}
  @media (max-width: 640px){
    .mc-bar{
      top:8px; left:8px; right:8px; transform:none;
      width:auto; justify-content:space-between;
      padding:6px 8px; gap:6px;
      flex-wrap:nowrap;
    }
    .mc-label{display:none}
    .mc-input{width:100%; min-width:0; font-size:14px; padding:10px 12px}
    .mc-input-wrap{flex:1; min-width:0}
    .mc-btn{padding:10px 14px; font-size:16px}
    .book-btn{padding:10px 12px; font-size:11px; white-space:nowrap}
    .book-modal{width:96vw; padding:10px; top:52%; max-height:82vh; overflow-y:auto}
    .book-pages{min-height:120px}
    #toast{top:68px; font-size:11px; padding:8px 12px; max-width:90vw; text-align:center}
  }
  @media (max-width: 380px){
    .mc-bar{top:6px; left:6px; right:6px; padding:5px 6px}
    .mc-input{font-size:13px; padding:9px 10px}
    .book-modal{width:98vw}
  }
  @media (hover: none) and (pointer: coarse){
    /* touch devices - larger hit areas */
    .mc-btn, .book-btn, .book-close{min-height:44px}
    .mc-input{font-size:16px} /* prevent iOS zoom */
  }
"""

if "поддержка всех устройств" not in t:
    t = t.replace(".book-overlay.open{display:block}", ".book-overlay.open{display:block}" + responsive_css)
    print("responsive css added")

# 4. Fix bugs and improvements on taste

# Bug1: renderer pixelRatio too high on mobile -> cap at 1.5 for performance
t = t.replace(
    "renderer.setPixelRatio(Math.min(devicePixelRatio, 2));",
    "renderer.setPixelRatio(Math.min(devicePixelRatio, window.innerWidth<640 ? 1.5 : 2));"
)
print("pixelRatio capped for mobile")

# Bug2: controls should work better on touch - enable rotate/zoom/pan explicitly and set touch-action
# Already enabled, but ensure touch works: add touch listeners handled by OrbitControls, just ensure damping
# Change damping to be adaptive
t = t.replace(
    "const controls=new OrbitControls(camera,renderer.domElement); controls.target.set(0,10,0); controls.enableDamping=true; controls.dampingFactor=0.22; controls.minDistance=10; controls.maxDistance=60;",
    "const controls=new OrbitControls(camera,renderer.domElement); controls.target.set(0,10,0); controls.enableDamping=true; controls.dampingFactor=0.22; controls.minDistance=10; controls.maxDistance=60; controls.enablePan=false; // на мобилках пан мешает\n  // поддержка всех устройств - touch + mouse + pen\n  controls.mouseButtons = { LEFT: THREE.MOUSE.ROTATE, MIDDLE: THREE.MOUSE.DOLLY, RIGHT: THREE.MOUSE.PAN };\n  controls.touches = { ONE: THREE.TOUCH.ROTATE, TWO: THREE.TOUCH.DOLLY_PAN };"
)
print("controls touch optimized")

# Bug3: input should not trigger OrbitControls when typing - stop propagation
t = t.replace(
    'const input=document.getElementById("cmd");',
    'const input=document.getElementById("cmd");\n  // фикс: ввод не должен крутить модель на мобилках\n  ["touchstart","touchmove","pointerdown"].forEach(ev=>{\n    input.addEventListener(ev, e=> e.stopPropagation());\n  });'
)
print("input stopPropagation added")

# Bug4: canvas resize should handle orientationchange and visualViewport on mobile
old_resize = """addEventListener("resize",()=>{
  camera.aspect=innerWidth/innerHeight; camera.updateProjectionMatrix();
  renderer.setSize(innerWidth,innerHeight);
});"""
new_resize = """function onResize(){
  const w=innerWidth, h=innerHeight;
  camera.aspect=w/h; camera.updateProjectionMatrix();
  renderer.setSize(w,h);
  renderer.setPixelRatio(Math.min(devicePixelRatio, w<640 ? 1.5 : 2));
}
addEventListener("resize", onResize);
addEventListener("orientationchange", ()=> setTimeout(onResize, 200));
if(window.visualViewport) visualViewport.addEventListener("resize", onResize);
onResize();"""

if old_resize in t:
    t = t.replace(old_resize, new_resize)
    print("resize fixed for all devices")

# Bug5: setTimeout renderBook 100ms may fire before DOM ready on slow devices -> use DOMContentLoaded
t = t.replace(
    "setTimeout(renderBook, 100);",
    "if(document.readyState===\"loading\") document.addEventListener(\"DOMContentLoaded\", ()=> setTimeout(renderBook, 100)); else setTimeout(renderBook, 100);"
)
print("renderBook timing fixed")

# Bug6: spinning flag blocks all animations including book - ensure book still opens
# Already ok, but add guard for isTrusted
# No change needed

# Bug7: localStorage may throw in private mode on iOS - wrap in try/catch
old_save = """function saveAch(){
  localStorage.setItem("ach_spin", JSON.stringify(achievements.spin));
  localStorage.setItem("ach_salto", JSON.stringify(achievements.salto));
  localStorage.setItem("ach_hit", JSON.stringify(achievements.hit));
  localStorage.setItem("ach_invis", JSON.stringify(achievements.invis));
  localStorage.setItem("ach_crouch", JSON.stringify(achievements.crouch));
  localStorage.setItem("ach_jump", JSON.stringify(achievements.jump));
  localStorage.setItem("ach_spinCount", achievements.spinCount);
  localStorage.setItem("ach_saltoCount", achievements.saltoCount);
  localStorage.setItem("ach_hitCount", achievements.hitCount);
  localStorage.setItem("ach_invisCount", achievements.invisCount);
  localStorage.setItem("ach_crouchCount", achievements.crouchCount);
  localStorage.setItem("ach_jumpCount", achievements.jumpCount);
}"""

new_save = """function saveAch(){
  try{
    localStorage.setItem("ach_spin", JSON.stringify(achievements.spin));
    localStorage.setItem("ach_salto", JSON.stringify(achievements.salto));
    localStorage.setItem("ach_hit", JSON.stringify(achievements.hit));
    localStorage.setItem("ach_invis", JSON.stringify(achievements.invis));
    localStorage.setItem("ach_crouch", JSON.stringify(achievements.crouch));
    localStorage.setItem("ach_jump", JSON.stringify(achievements.jump));
    localStorage.setItem("ach_spinCount", achievements.spinCount);
    localStorage.setItem("ach_saltoCount", achievements.saltoCount);
    localStorage.setItem("ach_hitCount", achievements.hitCount);
    localStorage.setItem("ach_invisCount", achievements.invisCount);
    localStorage.setItem("ach_crouchCount", achievements.crouchCount);
    localStorage.setItem("ach_jumpCount", achievements.jumpCount);
  }catch(e){ console.warn("localStorage fail",e); }
}"""

if old_save in t:
    t = t.replace(old_save, new_save)
    print("localStorage wrapped")

# Bug8: achievements init may throw - wrap
old_init = """const achievements = {
  spin: JSON.parse(localStorage.getItem("ach_spin")||"false"),
  salto: JSON.parse(localStorage.getItem("ach_salto")||"false"),
  hit: JSON.parse(localStorage.getItem("ach_hit")||"false"),
  invis: JSON.parse(localStorage.getItem("ach_invis")||"false"),
  crouch: JSON.parse(localStorage.getItem("ach_crouch")||"false"),
  jump: JSON.parse(localStorage.getItem("ach_jump")||"false"),
  spinCount: parseInt(localStorage.getItem("ach_spinCount")||"0"),
  saltoCount: parseInt(localStorage.getItem("ach_saltoCount")||"0"),
  hitCount: parseInt(localStorage.getItem("ach_hitCount")||"0"),
  invisCount: parseInt(localStorage.getItem("ach_invisCount")||"0"),
  crouchCount: parseInt(localStorage.getItem("ach_crouchCount")||"0"),
  jumpCount: parseInt(localStorage.getItem("ach_jumpCount")||"0")
};"""

new_init = """let achievements;
try{
  achievements = {
    spin: JSON.parse(localStorage.getItem("ach_spin")||"false"),
    salto: JSON.parse(localStorage.getItem("ach_salto")||"false"),
    hit: JSON.parse(localStorage.getItem("ach_hit")||"false"),
    invis: JSON.parse(localStorage.getItem("ach_invis")||"false"),
    crouch: JSON.parse(localStorage.getItem("ach_crouch")||"false"),
    jump: JSON.parse(localStorage.getItem("ach_jump")||"false"),
    spinCount: parseInt(localStorage.getItem("ach_spinCount")||"0"),
    saltoCount: parseInt(localStorage.getItem("ach_saltoCount")||"0"),
    hitCount: parseInt(localStorage.getItem("ach_hitCount")||"0"),
    invisCount: parseInt(localStorage.getItem("ach_invisCount")||"0"),
    crouchCount: parseInt(localStorage.getItem("ach_crouchCount")||"0"),
    jumpCount: parseInt(localStorage.getItem("ach_jumpCount")||"0")
  };
}catch(e){
  console.warn("ach init fail",e);
  achievements = {spin:false,salto:false,hit:false,invis:false,crouch:false,jump:false,spinCount:0,saltoCount:0,hitCount:0,invisCount:0,crouchCount:0,jumpCount:0};
}"""

if old_init in t:
    t = t.replace(old_init, new_init)
    print("achievements init wrapped")

# Improvement on taste: add subtle vignette and better lighting, double-tap to reset camera, long-press hint
# Add double-tap reset
t = t.replace(
    'document.addEventListener("keydown", e=>{ if(e.key==="Escape") closeBook(); });',
    'document.addEventListener("keydown", e=>{ if(e.key==="Escape") closeBook(); });\n  // двойной тап по canvas — сброс камеры (удобно на телефоне)\n  let lastTap=0;\n  canvas.addEventListener("touchend", e=>{\n    const now=Date.now();\n    if(now-lastTap<350 && e.changedTouches.length===1){\n      const t=e.changedTouches[0];\n      if(t.clientY>80){ // не на панели ввода\n        controls.target.set(0,10,0);\n        camera.position.set(20,16,26);\n        controls.update();\n        showToast("📷 Камера сброшена");\n      }\n    }\n    lastTap=now;\n  });'
)
print("double-tap added")

# Improvement: add subtle floating animation when idle (легкая плавность)
t = t.replace(
    "  renderer.setAnimationLoop(()=>{\n    controls.update();\n    renderer.render(scene,camera);\n  });",
    "  let idlePhase=0;\n  renderer.setAnimationLoop(()=>{\n    controls.update();\n    if(!spinning && !controls.isUserControlling){\n      idlePhase+=0.008;\n      if(steveGroup) steveGroup.position.y = Math.sin(idlePhase)*0.12;\n    }\n    renderer.render(scene,camera);\n  });"
)
print("idle floating added")

# Ensure input placeholder is short for mobile
t = t.replace('placeholder="крутанись, сальто, удар..."', 'placeholder="команда..."')

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

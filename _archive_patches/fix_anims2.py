import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# 1. Remove gfx panel CSS
t = re.sub(r'\s*\.gfx-panel\{[^}]+\}\s*\.gfx-title\{[^}]+\}\s*\.gfx-row\{[^}]+\}\s*\.gfx-row label\{[^}]+\}\s*\.gfx-row input\[type="range"\]\{[^}]+\}\s*\.gfx-row input\[type="checkbox"\]\{[^}]+\}', '', t, flags=re.DOTALL)
print("removed gfx css" if ".gfx-panel" not in t else "gfx css still there")

# 2. Remove gfx HTML
t = re.sub(r'<div class="gfx-panel" id="gfxPanel">.*?</div>\s*</div>\s*', '', t, flags=re.DOTALL)
# The above regex may be too greedy; try simpler
if 'id="gfxPanel"' in t:
    # fallback: remove by finding start and end
    start = t.find('<div class="gfx-panel" id="gfxPanel">')
    end = t.find('</div>', start)
    # need to find matching closing for panel (has nested divs)
    # find second </div> after start (panel has 4 rows + title = need 2 closing)
    # simpler: search for '<div class="hint">' and remove everything before it that is gfx
    t = t.replace('<div class="gfx-panel" id="gfxPanel">', '<!-- gfx removed -->')
    # Actually redo: just remove the whole block by manual
    import re as re2
    t = re2.sub(r'<!-- gfx removed -->.*?<div class="hint">', '<div class="hint">', t, flags=re2.DOTALL)
    print("removed gfx html second try")
else:
    print("gfx html removed")

# 3. Remove/Replace graphics JS (applyGraphics and listeners)
# Find the block from "// === графика" to next blank or until scene.fog logic
# Replace entire graphics block with auto 100 settings
old_gfx_js = re.search(r'// === графика: глубина резкости.*?\ndocument\.getElementById\("gfxSmooth"\)\.addEventListener\("input", applyGraphics\);\n', t, flags=re.DOTALL)
if old_gfx_js:
    gfx_code = old_gfx_js.group(0)
    # Replace with auto max settings (sharpness 100, smoothness 100, no DOF)
    new_gfx_js = """// === графика: авто на 100, глубина резкости удалена ===
controls.dampingFactor = 0.22; // плавность 100%
// резкость 100%: макс анизотропия + Nearest для четкости
setTimeout(()=>{
  if(steveGroup){
    steveGroup.traverse(obj=>{
      if(obj.isMesh && obj.material.map){
        obj.material.map.anisotropy = 16;
        obj.material.map.magFilter = THREE.NearestFilter;
        obj.material.map.minFilter = THREE.NearestFilter;
        obj.material.map.needsUpdate=true;
      }
    });
  }
  scene.fog = null; // глубина резкости удалена
}, 400);
"""
    t = t.replace(gfx_code, new_gfx_js)
    print("replaced gfx js with auto 100")
else:
    print("gfx js not found")

# 4. Fix doHit - make normal punch not like дрочит
old_hit = """function doHit(){
  if(!steveGroup || spinning) return;
  spinning=true;
  // найдем правую руку (первая рука в группе)
  let rArm=null;
  steveGroup.traverse(o=>{ if(o.isMesh && o.position.x<0 && o.position.y>8) rArm=o; });
  // fallback: просто тряска группы
  const dur=420;
  const start=performance.now();
  const startRot = rArm ? rArm.rotation.x : 0;
  function frame(now){
    const t=Math.min((now-start)/dur,1);
    let prog;
    if(t<0.35) prog = (t/0.35);
    else if(t<0.7) prog = 1 - ((t-0.35)/0.35)*0.5;
    else prog = 0.5 * (1 - (t-0.7)/0.3);
    // ease
    const angle = Math.sin(prog*Math.PI)* -1.2;
    if(rArm) rArm.rotation.x = startRot + angle;
    else steveGroup.rotation.z = Math.sin(prog*Math.PI)*0.12;
    if(t<1) requestAnimationFrame(frame);
    else { if(rArm) rArm.rotation.x=startRot; else steveGroup.rotation.z=0; spinning=false; showToast("УДАР! 💥"); }
  }
  requestAnimationFrame(frame);
}"""

new_hit = """function doHit(){
  if(!steveGroup || spinning) return;
  spinning=true;
  let rArm=null;
  steveGroup.traverse(o=>{ if(o.isMesh && o.position.x<0 && o.position.y>8) rArm=o; });
  const dur=480;
  const start=performance.now();
  const startX = rArm ? rArm.position.z : 0;
  const startRotX = rArm ? rArm.rotation.x : 0;
  const startRotY = rArm ? rArm.rotation.y : 0;
  function frame(now){
    const t=Math.min((now-start)/dur,1);
    // фаза удара: 0-0.25 замах назад, 0.25-0.45 резкий выпад вперед, 0.45-0.75 возврат, 0.75-1 отдых
    let punch = 0;
    if(t<0.18){
      punch = -0.25 * (t/0.18); // небольшой замах назад
    } else if(t<0.38){
      punch = -0.25 + 1.45 * ((t-0.18)/0.20); // резкий выпад вперед
    } else if(t<0.62){
      punch = 1.20 * (1 - (t-0.38)/0.24); // возврат
    } else {
      punch = 0;
    }
    const ease = punch;
    if(rArm){
      rArm.position.z = startX + ease*5.5; // вперед
      rArm.position.y = rArm.position.y; // не трогаем
      rArm.rotation.x = startRotX + ease*0.9; // слегка вперед
      rArm.rotation.y = startRotY + ease*0.15;
      // легкий наклон корпуса
      steveGroup.rotation.y = ease*0.08;
      steveGroup.position.z = ease*0.6;
    } else {
      steveGroup.position.z = ease*0.8;
    }
    if(t<1) requestAnimationFrame(frame);
    else {
      if(rArm){ rArm.position.z=startX; rArm.rotation.x=startRotX; rArm.rotation.y=startRotY; }
      steveGroup.rotation.y=0; steveGroup.position.z=0; spinning=false; showToast("УДАР! 💥");
    }
  }
  requestAnimationFrame(frame);
}"""

if old_hit in t:
    t = t.replace(old_hit, new_hit)
    print("fixed hit")
else:
    print("old_hit not found")

# 5. Fix doInvisibility to be 4 seconds invisible
old_invis = """function doInvisibility(){
  if(!steveGroup || spinning) return;
  spinning=true;
  const dur=900;
  const start=performance.now();
  // соберем все материалы
  const mats=[];
  steveGroup.traverse(o=>{ if(o.isMesh) mats.push(o.material); });
  mats.forEach(m=>{ m.transparent=true; });
  function frame(now){
    const t=Math.min((now-start)/dur,1);
    let opacity;
    if(t<0.4) opacity = 1 - t/0.4*0.9; // fade out to 0.1
    else if(t<0.7) opacity = 0.1;
    else opacity = 0.1 + (t-0.7)/0.3*0.9; // fade in
    mats.forEach(m=> m.opacity=opacity);
    if(t<1) requestAnimationFrame(frame);
    else { mats.forEach(m=>{ m.opacity=1; m.transparent=false; }); spinning=false; showToast("НЕВИДИМОСТЬ 👻"); }
  }
  requestAnimationFrame(frame);
}"""

new_invis = """function doInvisibility(){
  if(!steveGroup || spinning) return;
  spinning=true;
  const mats=[];
  steveGroup.traverse(o=>{ if(o.isMesh) mats.push(o.material); });
  mats.forEach(m=>{ m.transparent=true; });
  const fadeOut=300, stay=4000, fadeIn=300;
  const total=fadeOut+stay+fadeIn;
  const start=performance.now();
  function frame(now){
    const elapsed=now-start;
    const t=Math.min(elapsed/total,1);
    let opacity=1;
    if(elapsed<fadeOut){
      opacity = 1 - (elapsed/fadeOut);
    } else if(elapsed<fadeOut+stay){
      opacity = 0;
    } else {
      const p=(elapsed-fadeOut-stay)/fadeIn;
      opacity = p;
    }
    mats.forEach(m=> m.opacity=opacity);
    // скрываем полностью когда opacity 0 чтобы не было теней
    steveGroup.visible = opacity>0.02 || elapsed<fadeOut+stay+fadeIn;
    if(t<1) requestAnimationFrame(frame);
    else { mats.forEach(m=>{ m.opacity=1; m.transparent=false; }); steveGroup.visible=true; spinning=false; showToast("НЕВИДИМОСТЬ 4с 👻"); }
  }
  requestAnimationFrame(frame);
}"""

if old_invis in t:
    t = t.replace(old_invis, new_invis)
    print("fixed invis 4s")
else:
    print("old_invis not found")

# 6. Fix doCrouch to be more natural (присесть)
old_crouch = """function doCrouch(){
  if(!steveGroup || spinning) return;
  spinning=true;
  const startY=steveGroup.position.y;
  const startScaleY=steveGroup.scale.y;
  const dur=600;
  const start=performance.now();
  function frame(now){
    const t=Math.min((now-start)/dur,1);
    let prog;
    if(t<0.5) prog = t/0.5; // down
    else prog = 1 - (t-0.5)/0.5*0.3; // up partially
    if(t>=0.85) prog = 0.7 * (1 - (t-0.85)/0.15);
    const y = startY - prog*2.2;
    const sy = 1 - prog*0.15;
    steveGroup.position.y = y;
    steveGroup.scale.y = sy;
    if(t<1) requestAnimationFrame(frame);
    else { steveGroup.position.y=startY; steveGroup.scale.y=1; spinning=false; showToast("ПРИСЕЛ 🧎"); }
  }
  requestAnimationFrame(frame);
}"""

new_crouch = """function doCrouch(){
  if(!steveGroup || spinning) return;
  spinning=true;
  const startY=steveGroup.position.y;
  const dur=700;
  const start=performance.now();
  // найдем ноги для сгиба
  let rLeg=null,lLeg=null;
  steveGroup.traverse(o=>{
    if(o.isMesh && o.position.y<2){
      if(o.position.x<0) rLeg=o; else lLeg=o;
    }
  });
  const rLegStartY = rLeg?rLeg.position.y:0;
  const lLegStartY = lLeg?lLeg.position.y:0;
  function frame(now){
    const t=Math.min((now-start)/dur,1);
    // 0-0.3 приседает, 0.3-0.65 сидит, 0.65-1 встает
    let prog=0;
    if(t<0.28) prog = t/0.28;
    else if(t<0.68) prog = 1;
    else prog = 1 - (t-0.68)/0.32;
    const ease = 1 - Math.pow(1-prog,2);
    steveGroup.position.y = startY - ease*3.2;
    // сгибаем ноги - наклон
    if(rLeg) rLeg.rotation.x = ease*0.55;
    if(lLeg) lLeg.rotation.x = ease*0.55;
    // слегка увеличиваем масштаб ног чтобы не проваливались
    steveGroup.scale.y = 1 - ease*0.06;
    if(t<1) requestAnimationFrame(frame);
    else {
      steveGroup.position.y=startY;
      steveGroup.scale.y=1;
      if(rLeg) rLeg.rotation.x=0;
      if(lLeg) lLeg.rotation.x=0;
      spinning=false; showToast("ПРИСЕЛ 🧎");
    }
  }
  requestAnimationFrame(frame);
}"""

if old_crouch in t:
    t = t.replace(old_crouch, new_crouch)
    print("fixed crouch")
else:
    print("old_crouch not found")

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

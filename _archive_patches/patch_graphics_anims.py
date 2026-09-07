import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# === 1. CSS: add graphics panel styles ===
css_graphics = """
  .gfx-panel{
    position:fixed;bottom:14px;left:14px;
    background:rgba(43,43,43,0.92);
    border:2px solid #000;
    box-shadow: inset -2px -2px 0 #555, inset 2px 2px 0 #6a6a6a;
    padding:10px 12px;
    z-index:12;
    min-width:220px;
  }
  .gfx-title{font-family:"Inter",system-ui,sans-serif;font-size:11px;font-weight:700;color:#FFD700;margin-bottom:8px;text-shadow:1px 1px 0 #000}
  .gfx-row{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:6px 0;font-family:"Inter",system-ui,sans-serif;font-size:11px;color:#ddd}
  .gfx-row label{font-size:11px}
  .gfx-row input[type="range"]{width:90px;accent-color:#55ff55}
  .gfx-row input[type="checkbox"]{accent-color:#55ff55;width:16px;height:16px}
"""

if ".gfx-panel{" not in t:
    t = t.replace(".book-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.5);display:none;z-index:29}", ".book-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.5);display:none;z-index:29}" + css_graphics)
    print("css graphics added")

# === 2. HTML: add graphics panel after hint ===
gfx_html = """
<div class="gfx-panel" id="gfxPanel">
  <div class="gfx-title">⚙️ ГРАФИКА</div>
  <div class="gfx-row"><label>Глубина резкости (туман)</label><input type="checkbox" id="gfxDof"></div>
  <div class="gfx-row"><label>Резкость</label><input type="range" id="gfxSharp" min="0" max="100" value="50"><span id="gfxSharpVal" style="font-size:10px;color:#aaa">50%</span></div>
  <div class="gfx-row"><label>Плавность (демпфер)</label><input type="range" id="gfxSmooth" min="0" max="100" value="30"><span id="gfxSmoothVal" style="font-size:10px;color:#aaa">30%</span></div>
</div>
"""
if 'id="gfxPanel"' not in t:
    t = t.replace('<div class="hint">', gfx_html + '<div class="hint">')
    print("gfx html added")

# === 3. JS: inject graphics logic after controls setup ===
# Find controls setup line and inject after
old_controls = "const controls=new OrbitControls(camera,renderer.domElement); controls.target.set(0,10,0); controls.enableDamping=true; controls.dampingFactor=0.08; controls.minDistance=10; controls.maxDistance=60;"
new_controls = """const controls=new OrbitControls(camera,renderer.domElement); controls.target.set(0,10,0); controls.enableDamping=true; controls.dampingFactor=0.08; controls.minDistance=10; controls.maxDistance=60;
// === графика: глубина резкости, резкость, плавность ===
let dofEnabled=false;
function applyGraphics(){
  const sharpVal=parseInt(document.getElementById("gfxSharp").value);
  const smoothVal=parseInt(document.getElementById("gfxSmooth").value);
  // глубина резкости -> туман
  if(dofEnabled){
    scene.fog = new THREE.Fog(0x1a1a1e, 28, 52);
  } else {
    scene.fog = null;
  }
  // резкость -> анизотропия и фильтр текстур (если Стив загружен)
  if(steveGroup){
    const aniso = 1 + (sharpVal/100)*15; // 1..16
    const useNearest = sharpVal > 70;
    steveGroup.traverse(obj=>{
      if(obj.isMesh && obj.material.map){
        obj.material.map.anisotropy = aniso;
        obj.material.map.magFilter = useNearest ? THREE.NearestFilter : THREE.LinearFilter;
        obj.material.map.minFilter = useNearest ? THREE.NearestFilter : THREE.LinearMipmapLinearFilter;
        obj.material.map.needsUpdate=true;
      }
    });
  }
  // плавность -> демпфер камеры и скорость анимаций
  controls.dampingFactor = 0.02 + (smoothVal/100)*0.2; // 0.02..0.22
  document.getElementById("gfxSharpVal").textContent = sharpVal+"%";
  document.getElementById("gfxSmoothVal").textContent = smoothVal+"%";
  // сохраняем
  localStorage.setItem("gfx_dof", dofEnabled);
  localStorage.setItem("gfx_sharp", sharpVal);
  localStorage.setItem("gfx_smooth", smoothVal);
}
// загрузка сохраненных
setTimeout(()=>{
  const sDof = localStorage.getItem("gfx_dof");
  const sSharp = localStorage.getItem("gfx_sharp");
  const sSmooth = localStorage.getItem("gfx_smooth");
  if(sDof!==null) dofEnabled = sDof==="true";
  if(sSharp!==null) document.getElementById("gfxSharp").value=sSharp;
  if(sSmooth!==null) document.getElementById("gfxSmooth").value=sSmooth;
  document.getElementById("gfxDof").checked = dofEnabled;
  applyGraphics();
}, 300);
document.getElementById("gfxDof").addEventListener("change", e=>{ dofEnabled=e.target.checked; applyGraphics(); });
document.getElementById("gfxSharp").addEventListener("input", applyGraphics);
document.getElementById("gfxSmooth").addEventListener("input", applyGraphics);
"""

if "gfxPanel" not in t or "applyGraphics" not in t:
    if old_controls in t:
        t = t.replace(old_controls, new_controls)
        print("controls patched")
    else:
        print("old_controls not found")

# === 4. JS: add 4 new animations after doSomersault ===
old_salto = """function doSomersault(){
  if(!steveGroup || spinning) return;
  spinning=true;
  const startX=steveGroup.rotation.x;
  const targetX=startX + Math.PI*2;
  const startY=steveGroup.position.y;
  const duration=750;
  const start=performance.now();
  function frame(now){
    const t=Math.min((now-start)/duration,1);
    const ease=1 - Math.pow(1-t,3);
    steveGroup.rotation.x = startX + (targetX-startX)*ease;
    steveGroup.position.y = startY + Math.sin(t*Math.PI)*5;
    if(t<1) requestAnimationFrame(frame);
    else { steveGroup.rotation.x = ((targetX % (Math.PI*2))+Math.PI*2)%(Math.PI*2); steveGroup.position.y=startY; spinning=false; showToast("САЛЬТО!"); }
  }
  requestAnimationFrame(frame);
}"""

new_anims = """function doSomersault(){
  if(!steveGroup || spinning) return;
  spinning=true;
  const startX=steveGroup.rotation.x;
  const targetX=startX + Math.PI*2;
  const startY=steveGroup.position.y;
  const duration=750;
  const start=performance.now();
  function frame(now){
    const t=Math.min((now-start)/duration,1);
    const ease=1 - Math.pow(1-t,3);
    steveGroup.rotation.x = startX + (targetX-startX)*ease;
    steveGroup.position.y = startY + Math.sin(t*Math.PI)*5;
    if(t<1) requestAnimationFrame(frame);
    else { steveGroup.rotation.x = ((targetX % (Math.PI*2))+Math.PI*2)%(Math.PI*2); steveGroup.position.y=startY; spinning=false; showToast("САЛЬТО!"); }
  }
  requestAnimationFrame(frame);
}
function doHit(){
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
}
function doInvisibility(){
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
}
function doCrouch(){
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
}
function doJump(){
  if(!steveGroup || spinning) return;
  spinning=true;
  const startY=steveGroup.position.y;
  const dur=650;
  const start=performance.now();
  function frame(now){
    const t=Math.min((now-start)/dur,1);
    const ease = Math.sin(t*Math.PI);
    steveGroup.position.y = startY + ease*7;
    // легкое сжатие при приземлении
    const squash = t>0.85 ? 1 - (1-t)/0.15*0.12 : 1;
    steveGroup.scale.y = squash;
    steveGroup.scale.x = 2 - squash;
    steveGroup.scale.z = 2 - squash;
    if(t<1) requestAnimationFrame(frame);
    else { steveGroup.position.y=startY; steveGroup.scale.set(1,1,1); spinning=false; showToast("ПРЫЖОК! ⬆️"); }
  }
  requestAnimationFrame(frame);
}"""

if "function doHit" not in t and old_salto in t:
    t = t.replace(old_salto, new_anims)
    print("added 4 anims")
else:
    print("anims exists or old not found")

# === 5. Expand aliases and achievements ===
# Replace spin/salto aliases definition to include new ones
old_aliases = 'const spinAliases=["крутанись","крутись","крутнись","покрутись","вертанись","крутануть"];\nconst saltoAliases=["сальто","сальтуха","кувырок","флип","переворот","сальтануть"];'
new_aliases = '''const spinAliases=["крутанись","крутись","крутнись","покрутись","вертанись","крутануть"];
const saltoAliases=["сальто","сальтуха","кувырок","флип","переворот","сальтануть"];
const hitAliases=["удар","ударь","бей","атака","хит","стукни"];
const invisAliases=["невидимость","невидимка","исчезни","спрячься","инвиз","скрыться"];
const crouchAliases=["присесть","присядь","сидеть","пригнись","крауч","на корточки"];
const jumpAliases=["прыгнуть","прыжок","прыгни","джамп","прыгай","подпрыгни"];'''

if old_aliases in t:
    t = t.replace(old_aliases, new_aliases)
    print("aliases expanded")
else:
    print("aliases not found")

# === 6. Expand achievements object ===
old_ach = """const achievements = {
  spin: JSON.parse(localStorage.getItem("ach_spin")||"false"),
  salto: JSON.parse(localStorage.getItem("ach_salto")||"false"),
  spinCount: parseInt(localStorage.getItem("ach_spinCount")||"0"),
  saltoCount: parseInt(localStorage.getItem("ach_saltoCount")||"0")
};
function saveAch(){ localStorage.setItem("ach_spin", JSON.stringify(achievements.spin)); localStorage.setItem("ach_salto", JSON.stringify(achievements.salto)); localStorage.setItem("ach_spinCount", achievements.spinCount); localStorage.setItem("ach_saltoCount", achievements.saltoCount); }
function unlockAch(type){
  let isNew=false;
  if(type==="spin" && !achievements.spin){ achievements.spin=true; isNew=true; }
  if(type==="salto" && !achievements.salto){ achievements.salto=true; isNew=true; }
  if(type==="spin") achievements.spinCount++;
  if(type==="salto") achievements.saltoCount++;
  saveAch();
  renderBook();
  if(isNew){ showToast(type==="spin" ? "🏆 Ачивка: МАСТЕР ВРАЩЕНИЯ!" : "🏆 Ачивка: САЛЬТО-МАСТЕР!"); }
}"""

new_ach = """const achievements = {
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
function saveAch(){
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
}
function unlockAch(type){
  let isNew=false;
  if(type==="spin" && !achievements.spin){ achievements.spin=true; isNew=true; }
  if(type==="salto" && !achievements.salto){ achievements.salto=true; isNew=true; }
  if(type==="hit" && !achievements.hit){ achievements.hit=true; isNew=true; }
  if(type==="invis" && !achievements.invis){ achievements.invis=true; isNew=true; }
  if(type==="crouch" && !achievements.crouch){ achievements.crouch=true; isNew=true; }
  if(type==="jump" && !achievements.jump){ achievements.jump=true; isNew=true; }
  if(type==="spin") achievements.spinCount++;
  if(type==="salto") achievements.saltoCount++;
  if(type==="hit") achievements.hitCount++;
  if(type==="invis") achievements.invisCount++;
  if(type==="crouch") achievements.crouchCount++;
  if(type==="jump") achievements.jumpCount++;
  saveAch();
  renderBook();
  const names={spin:"МАСТЕР ВРАЩЕНИЯ",salto:"САЛЬТО-МАСТЕР",hit:"МАСТЕР УДАРА",invis:"НЕВИДИМКА",crouch:"МАСТЕР СКРЫТНОСТИ",jump:"ДЖЕМП-МАСТЕР"};
  if(isNew){ showToast("🏆 Ачивка: "+(names[type]||type)+"!"); }
}"""

if old_ach in t:
    t = t.replace(old_ach, new_ach)
    print("achievements expanded to 6")
else:
    print("old_ach not found")

# === 7. Update renderBook for 6 achievements hidden ===
old_render = """  const total=2;
  const done=(achievements.spin?1:0)+(achievements.salto?1:0);
  let html="";
  if(achievements.spin){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>КРУТАНИСЬ — резкий 360°<br><small style="font-size:10px;color:#6B6B6B">команды: крутанись, крутись, крутнись, покрутись, вертанись, крутануть</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.spinCount} раз</small></span></div>`;
  }
  if(achievements.salto){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>САЛЬТО — кувырок 360° + прыжок<br><small style="font-size:10px;color:#6B6B6B">команды: сальто, сальтуха, кувырок, флип, переворот, сальтануть</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.saltoCount} раз</small></span></div>`;
  }
  if(html===""){
    html = `<div style="text-align:center;padding:20px;color:#8B8B8B;font-size:12px;line-height:1.6">📖 Пока пусто<br><small>Выполни команды, чтобы открыть ачивки</small></div>`;
  }
  pages.innerHTML = html;
  if(prog) prog.textContent = `${done}/${total} ачивок собрано` + (done===total && total>0 ? " — ВСЕ СОБРАНЫ! 🎉" : "");"""

new_render = """  const total=6;
  const done=(achievements.spin?1:0)+(achievements.salto?1:0)+(achievements.hit?1:0)+(achievements.invis?1:0)+(achievements.crouch?1:0)+(achievements.jump?1:0);
  let html="";
  if(achievements.spin){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>КРУТАНИСЬ — резкий 360°<br><small style="font-size:10px;color:#6B6B6B">крутанись, крутись, крутнись, покрутись, вертанись, крутануть</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.spinCount} раз</small></span></div>`;
  }
  if(achievements.salto){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>САЛЬТО — кувырок 360° + прыжок<br><small style="font-size:10px;color:#6B6B6B">сальто, сальтуха, кувырок, флип, переворот, сальтануть</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.saltoCount} раз</small></span></div>`;
  }
  if(achievements.hit){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>УДАР — удар рукой<br><small style="font-size:10px;color:#6B6B6B">удар, ударь, бей, атака, хит, стукни</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.hitCount} раз</small></span></div>`;
  }
  if(achievements.invis){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>НЕВИДИМОСТЬ — исчезновение<br><small style="font-size:10px;color:#6B6B6B">невидимость, невидимка, исчезни, спрячься, инвиз, скрыться</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.invisCount} раз</small></span></div>`;
  }
  if(achievements.crouch){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>ПРИСЕСТЬ — приседание<br><small style="font-size:10px;color:#6B6B6B">присесть, присядь, сидеть, пригнись, крауч, на корточки</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.crouchCount} раз</small></span></div>`;
  }
  if(achievements.jump){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>ПРЫЖОК — прыжок вверх<br><small style="font-size:10px;color:#6B6B6B">прыгнуть, прыжок, прыгни, джамп, прыгай, подпрыгни</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.jumpCount} раз</small></span></div>`;
  }
  if(html===""){
    html = `<div style="text-align:center;padding:20px;color:#8B8B8B;font-size:12px;line-height:1.6">📖 Пока пусто<br><small>Выполни команды, чтобы открыть ачивки</small></div>`;
  }
  pages.innerHTML = html;
  if(prog) prog.textContent = `${done}/${total} ачивок собрано` + (done===total && total>0 ? " — ВСЕ СОБРАНЫ! 🎉" : "");"""

if old_render in t:
    t = t.replace(old_render, new_render)
    print("renderBook expanded to 6")
else:
    print("old_render not found")

# === 8. Update handleCmd to handle 6 types ===
old_handle2 = """  if(matchesAliases(norm, spinAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("spin");
    doSpin360();
    input.value="";
  } else if(matchesAliases(norm, saltoAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("salto");
    doSomersault();
    input.value="";
  } else {"""

new_handle2 = """  if(matchesAliases(norm, spinAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("spin");
    doSpin360();
    input.value="";
  } else if(matchesAliases(norm, saltoAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("salto");
    doSomersault();
    input.value="";
  } else if(matchesAliases(norm, hitAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("hit");
    doHit();
    input.value="";
  } else if(matchesAliases(norm, invisAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("invis");
    doInvisibility();
    input.value="";
  } else if(matchesAliases(norm, crouchAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("crouch");
    doCrouch();
    input.value="";
  } else if(matchesAliases(norm, jumpAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("jump");
    doJump();
    input.value="";
  } else {"""

if old_handle2 in t:
    t = t.replace(old_handle2, new_handle2)
    print("handleCmd expanded")
else:
    print("old_handle2 not found")

# Update placeholder hint
t = t.replace('placeholder="крутанись / сальто"', 'placeholder="крутанись, сальто, удар..."')
if 'введи «крутанись» или «сальто»' in t:
    t = t.replace('введи «крутанись» или «сальто»', 'введи «крутанись», «сальто», «удар», «прыгни»...')

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written and copied, len", len(t))

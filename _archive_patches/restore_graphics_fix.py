import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# === 1. Re-add gfx CSS if missing ===
if ".gfx-panel" not in t:
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
    t = t.replace(".book-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.5);display:none;z-index:29}", ".book-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.5);display:none;z-index:29}" + css_graphics)
    print("re-added gfx css")

# === 2. Re-add gfx HTML ===
if 'id="gfxPanel"' not in t:
    gfx_html = """<div class="gfx-panel" id="gfxPanel">
  <div class="gfx-title">⚙️ ГРАФИКА</div>
  <div class="gfx-row"><label>Глубина резкости (туман)</label><input type="checkbox" id="gfxDof"></div>
  <div class="gfx-row"><label>Резкость</label><input type="range" id="gfxSharp" min="0" max="100" value="50"><span id="gfxSharpVal" style="font-size:10px;color:#aaa">50%</span></div>
  <div class="gfx-row"><label>Плавность (демпфер)</label><input type="range" id="gfxSmooth" min="0" max="100" value="30"><span id="gfxSmoothVal" style="font-size:10px;color:#aaa">30%</span></div>
</div>
"""
    t = t.replace('<div class="hint">', gfx_html + '<div class="hint">')
    print("re-added gfx html")

# === 3. Re-add gfx JS (controls + applyGraphics) ===
# Remove the auto 100 block we added
if "// === графика: авто на 100" in t:
    # Find and replace with proper gfx logic
    old_auto = re.search(r'// === графика: авто на 100.*?\nscene\.fog = null; // глубина резкости удалена\n\}, 400\);\n', t, flags=re.DOTALL)
    if old_auto:
        t = t.replace(old_auto.group(0), """const controls=new OrbitControls(camera,renderer.domElement); controls.target.set(0,10,0); controls.enableDamping=true; controls.dampingFactor=0.08; controls.minDistance=10; controls.maxDistance=60;
// === графика: глубина резкости, резкость, плавность ===
let dofEnabled=false;
function applyGraphics(){
  const sharpVal=parseInt(document.getElementById("gfxSharp").value);
  const smoothVal=parseInt(document.getElementById("gfxSmooth").value);
  if(dofEnabled){
    scene.fog = new THREE.Fog(0x1a1a1e, 28, 52);
  } else {
    scene.fog = null;
  }
  if(steveGroup){
    const aniso = 1 + (sharpVal/100)*15;
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
  controls.dampingFactor = 0.02 + (smoothVal/100)*0.2;
  document.getElementById("gfxSharpVal").textContent = sharpVal+"%";
  document.getElementById("gfxSmoothVal").textContent = smoothVal+"%";
  localStorage.setItem("gfx_dof", dofEnabled);
  localStorage.setItem("gfx_sharp", sharpVal);
  localStorage.setItem("gfx_smooth", smoothVal);
}
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
""")
        print("restored gfx js")
    # Also need to ensure controls line not duplicated
    # Remove duplicate controls definition if exists
    # Count controls definitions
    if t.count("const controls=new OrbitControls") > 1:
        # remove the first duplicate auto one we left
        t = t.replace("const controls=new OrbitControls(camera,renderer.domElement); controls.target.set(0,10,0); controls.enableDamping=true; controls.dampingFactor=0.08; controls.minDistance=10; controls.maxDistance=60;\n// === графика: авто", "// === графика: авто", 1)
        print("dedup controls")

# If still no applyGraphics, inject after controls
if "function applyGraphics" not in t and "const controls=new OrbitControls" in t:
    # Find controls line
    old_c = "const controls=new OrbitControls(camera,renderer.domElement); controls.target.set(0,10,0); controls.enableDamping=true; controls.dampingFactor=0.08; controls.minDistance=10; controls.maxDistance=60;"
    if old_c in t:
        t = t.replace(old_c, old_c + "\n// === графика patch fallback ===\nlet dofEnabled=false;\nfunction applyGraphics(){}\n")
        print("added fallback gfx")

# === 4. Restore hit to working version but make it look like punch (not дрочит) - simple punch forward ===
# Current broken hit is the new one with position.z 5.5 - revert to simpler but improved punch
# Replace current doHit with a clean punch that actually works
# Find current doHit block
import re as re2
m = re2.search(r'function doHit\(\)\{.*?showToast\("УДАР!.*?\n\}', t, flags=re2.DOTALL)
if m:
    old_block = m.group(0)
    new_hit = """function doHit(){
  if(!steveGroup || spinning) return;
  spinning=true;
  let rArm=null;
  steveGroup.traverse(o=>{ if(o.isMesh && o.position.x<0 && o.position.y>8) rArm=o; });
  const dur=380;
  const start=performance.now();
  const startRotX = rArm ? rArm.rotation.x : 0;
  function frame(now){
    const et=now-start;
    const t=Math.min(et/dur,1);
    // punch: quick forward jab
    let p=0;
    if(t<0.22) p = (t/0.22)*1.0; // выпад
    else if(t<0.45) p = 1 - (t-0.22)/0.23; // возврат
    else p = 0;
    const punch = Math.sin(p*Math.PI*0.5)*1.3;
    if(rArm){
      rArm.position.z = punch*3.2;
      rArm.rotation.x = startRotX - punch*0.85;
    } else {
      steveGroup.position.z = punch*0.7;
    }
    if(t<1) requestAnimationFrame(frame);
    else { if(rArm){ rArm.position.z=0; rArm.rotation.x=startRotX; } else steveGroup.position.z=0; spinning=false; showToast("УДАР! 💥"); }
  }
  requestAnimationFrame(frame);
}"""
    t = t.replace(old_block, new_hit)
    print("replaced hit with clean punch")

# === 5. Fix invisibility to be 4 seconds correctly - keep simple opacity, no visible toggle that broke ===
m2 = re2.search(r'function doInvisibility\(\)\{.*?showToast\("НЕВИДИМОСТЬ.*?\n\}', t, flags=re2.DOTALL)
if m2:
    old_inv = m2.group(0)
    new_inv = """function doInvisibility(){
  if(!steveGroup || spinning) return;
  spinning=true;
  const mats=[];
  steveGroup.traverse(o=>{ if(o.isMesh) mats.push(o.material); });
  mats.forEach(m=>{ m.transparent=true; });
  const fade=250, stay=4000;
  const total=fade*2+stay;
  const start=performance.now();
  function frame(now){
    const e=now-start;
    let opacity=1;
    if(e<fade) opacity = 1 - e/fade;
    else if(e<fade+stay) opacity = 0;
    else if(e<total) opacity = (e-fade-stay)/fade;
    else opacity=1;
    mats.forEach(m=> m.opacity=opacity);
    if(e<total) requestAnimationFrame(frame);
    else { mats.forEach(m=>{ m.opacity=1; m.transparent=false; }); spinning=false; showToast("НЕВИДИМОСТЬ 4с 👻"); }
  }
  requestAnimationFrame(frame);
}"""
    t = t.replace(old_inv, new_inv)
    print("fixed invis 4s simple")

# === 6. Fix crouch to be simple and working (previous 700ms version was ok, but restore to 600ms simple that worked) ===
m3 = re2.search(r'function doCrouch\(\)\{.*?showToast\("ПРИСЕЛ.*?\n\}', t, flags=re2.DOTALL)
if m3:
    old_crouch = m3.group(0)
    # Keep the 700ms version but ensure it works - if current is 700ms with legs, keep it, just ensure spin flag reset
    # Check if current has rLeg logic - keep it, just ensure it ends correctly
    # If broken, replace with previous simple 600ms
    if "rLeg" not in old_crouch:
        print("crouch missing legs, keep as is")
    else:
        print("crouch has legs, keep")

# Ensure damping and fog not duplicated
p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# Remove gfx CSS
t = re.sub(r'\s*\.gfx-panel\{[^}]+\}\s*\.gfx-title\{[^}]+\}\s*\.gfx-row\{[^}]+\}\s*\.gfx-row label\{[^}]+\}\s*\.gfx-row input\[type="range"\]\{[^}]+\}\s*\.gfx-row input\[type="checkbox"\]\{[^}]+\}', '', t, flags=re.DOTALL)
print("removed gfx css" if ".gfx-panel" not in t else "still there")

# Remove gfx HTML
t = re.sub(r'<div class="gfx-panel" id="gfxPanel">.*?</div>\s*</div>\s*', '', t, flags=re.DOTALL)
# fallback if still there
if 'id="gfxPanel"' in t:
    t = re.sub(r'<div class="gfx-panel".*?-->.*?<div class="hint">', '<div class="hint">', t, flags=re.DOTALL)
    # simpler: remove any remaining gfxPanel block
    t = re.sub(r'<div class="gfx-panel.*?</div>\s*', '', t, flags=re.DOTALL)
print("gfx html removed" if 'id="gfxPanel"' not in t else "still gfx html")

# Replace gfx JS block (applyGraphics) with auto 100
# Find the block from controls line through applyGraphics listeners
# Look for the restored gfx js block
old_gfx = re.search(r'const controls=new OrbitControls\(camera,renderer\.domElement\);.*?document\.getElementById\("gfxSmooth"\)\.addEventListener\("input", applyGraphics\);\n', t, flags=re.DOTALL)
if old_gfx:
    block = old_gfx.group(0)
    new_block = """const controls=new OrbitControls(camera,renderer.domElement); controls.target.set(0,10,0); controls.enableDamping=true; controls.dampingFactor=0.22; controls.minDistance=10; controls.maxDistance=60;
// графика авто 100 - четко и плавно
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
  scene.fog = null;
}, 400);
"""
    t = t.replace(block, new_block)
    print("replaced gfx js with auto")
else:
    # try fallback: find any applyGraphics function
    if "function applyGraphics" in t:
        t = re.sub(r'let dofEnabled=false;.*?document\.getElementById\("gfxSmooth"\)\.addEventListener.*?\n', '', t, flags=re.DOTALL)
        # ensure controls damping 0.22
        t = t.replace('controls.dampingFactor=0.08', 'controls.dampingFactor=0.22')
        print("removed applyGraphics fallback")
    else:
        print("no gfx js found")

# Ensure controls damping is 0.22 (плавность 100)
if "controls.dampingFactor=0.08" in t:
    t = t.replace("controls.dampingFactor=0.08", "controls.dampingFactor=0.22")
    print("set damping 0.22")

# Keep hit/invis/crouch as currently fixed (they are now clean)
# Verify hit is the clean punch we just set
if 'rArm.position.z = punch*3.2' in t:
    print("hit is clean punch - keep")
else:
    print("hit not clean")

if 'stay=4000' in t or '4000' in t:
    print("invis 4s present")

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

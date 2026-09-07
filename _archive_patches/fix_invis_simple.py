import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

old = """function doInvisibility(){
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

new = """function doInvisibility(){
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

if old in t:
    t = t.replace(old, new)
    print("fixed invis simple")
else:
    print("old invis not found")
    # try to find any doInvisibility
    import re as re2
    m=re2.search(r'function doInvisibility.*?showToast.*?\{.*?\n\}', t, flags=re2.DOTALL)
    if m:
        print(repr(m.group(0)[:300]))

# Also clean up the duplicate gfx fallback that might cause error - remove the empty applyGraphics block that references missing elements
# Remove the fallback block entirely if it exists
t = t.replace("// === графика patch fallback ===\nlet dofEnabled=false;\nfunction applyGraphics(){}\n\n", "")
print("cleaned fallback" if "patch fallback" not in t else "still there")

# Ensure controls damping 0.22 remains
if "controls.dampingFactor = 0.22" not in t:
    t = t.replace("controls.dampingFactor=0.08", "controls.dampingFactor=0.22")
    print("set damping")

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

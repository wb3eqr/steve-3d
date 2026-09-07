import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# Fix doLie to properly stand up and not be broken by idle floating
old_lie = """function doLie(){
  if(!steveGroup || spinning) return;
  // toggle: если уже лежит - встать
  if(steveGroup.userData.isLying){
    spinning=true;
    const startY=steveGroup.position.y;
    const startRotX=steveGroup.rotation.x;
    const dur=500;
    const start=performance.now();
    function frame(now){
      const t=Math.min((now-start)/dur,1);
      const ease=1 - Math.pow(1-t,3);
      steveGroup.rotation.x = startRotX * (1-ease);
      steveGroup.position.y = startY + (0 - startY)*ease;
      if(t<1) requestAnimationFrame(frame);
      else { steveGroup.rotation.x=0; steveGroup.position.y=0; steveGroup.userData.isLying=false; spinning=false; showToast("🧍 ВСТАЛ!"); }
    }
    requestAnimationFrame(frame);
    return;
  }
  spinning=true;
  const startY=steveGroup.position.y;
  const dur=550;
  const start=performance.now();
  function frame(now){
    const t=Math.min((now-start)/dur,1);
    const ease=1 - Math.pow(1-t,3);
    // ложимся на спину: поворот 90 градусов вокруг X + опускаем на землю
    steveGroup.rotation.x = ease * Math.PI/2;
    steveGroup.position.y = startY - ease*5.2;
    // слегка вытягиваем
    steveGroup.position.z = ease*2.0;
    if(t<1) requestAnimationFrame(frame);
    else { steveGroup.userData.isLying=true; spinning=false; showToast("🛏️ ЛЁГ — спит котик"); }
  }
  requestAnimationFrame(frame);
}"""

new_lie = """function doLie(){
  if(!steveGroup || spinning) return;
  // toggle: если уже лежит - встать
  if(steveGroup.userData.isLying){
    spinning=true;
    const startY=steveGroup.position.y;
    const startZ=steveGroup.position.z;
    const startRotX=steveGroup.rotation.x;
    const dur=520;
    const start=performance.now();
    function frame(now){
      const t=Math.min((now-start)/dur,1);
      const ease=1 - Math.pow(1-t,3);
      steveGroup.rotation.x = startRotX * (1-ease);
      steveGroup.position.y = startY + (0 - startY)*ease;
      steveGroup.position.z = startZ * (1-ease);
      steveGroup.scale.y = 1;
      steveGroup.scale.x = 1;
      steveGroup.scale.z = 1;
      if(t<1) requestAnimationFrame(frame);
      else { steveGroup.rotation.x=0; steveGroup.position.x=0; steveGroup.position.y=0; steveGroup.position.z=0; steveGroup.scale.set(1,1,1); steveGroup.userData.isLying=false; spinning=false; showToast("🧍 ВСТАЛ!"); }
    }
    requestAnimationFrame(frame);
    return;
  }
  spinning=true;
  const startY=steveGroup.position.y;
  const startZ=steveGroup.position.z;
  const dur=560;
  const start=performance.now();
  function frame(now){
    const t=Math.min((now-start)/dur,1);
    const ease=1 - Math.pow(1-t,3);
    steveGroup.rotation.x = ease * Math.PI/2;
    steveGroup.position.y = startY - ease*5.4;
    steveGroup.position.z = startZ + ease*2.4;
    if(t<1) requestAnimationFrame(frame);
    else { steveGroup.userData.isLying=true; spinning=false; showToast("🛏️ ЛЁГ"); }
  }
  requestAnimationFrame(frame);
}"""

if old_lie in t:
    t = t.replace(old_lie, new_lie)
    print("fixed lie stand")
else:
    print("old lie not found")

# Fix idle floating to not interfere when lying
old_idle = """  let idlePhase=0;
  renderer.setAnimationLoop(()=>{
    controls.update();
    if(!spinning && !controls.isUserControlling){
      idlePhase+=0.008;
      if(steveGroup) steveGroup.position.y = Math.sin(idlePhase)*0.12;
    }
    renderer.render(scene,camera);
  });"""

new_idle = """  let idlePhase=0;
  let baseIdleY=0;
  renderer.setAnimationLoop(()=>{
    controls.update();
    if(!spinning && !controls.isUserControlling && steveGroup && !steveGroup.userData.isLying){
      idlePhase+=0.008;
      steveGroup.position.y = baseIdleY + Math.sin(idlePhase)*0.12;
    }
    renderer.render(scene,camera);
  });"""

if old_idle in t:
    t = t.replace(old_idle, new_idle)
    print("fixed idle to not affect lying")
else:
    print("idle not found")
    # try to find any idle
    if "idlePhase" in t:
        print("has idle but different")

# Remove mentions of "котик" as requested - replace toasts
t = t.replace("🛏️ ЛЁГ — спит котик", "🛏️ ЛЁГ")
t = t.replace("✅ СНОВА КОТИК!", "✅ ГОТОВО!")
t = t.replace("СНОВА КОТИК", "ГОТОВО")
t = t.replace("котик", "Стив")
# Ensure we don't mention cat in toasts - check
if "котик" in t.lower():
    print("still has котик")
    # remove all
    t = re.sub(r'котик', 'Стив', t, flags=re.IGNORECASE)
    print("removed all котик")

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

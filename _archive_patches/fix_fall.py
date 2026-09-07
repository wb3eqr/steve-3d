import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# Fix lie to not fall through ground: adjust Y to be on ground level
old_lie = """function doLie(){
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

new_lie = """function doLie(){
  if(!steveGroup || spinning) return;
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
      // возвращаем ровно на землю 0, не падаем
      steveGroup.position.y = startY + (0 - startY)*ease;
      steveGroup.position.z = startZ * (1-ease);
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
    // ложимся ровно на землю: y -3.8 (ноги на земле -6.1 + половина высоты лежа)
    steveGroup.position.y = startY - ease*3.8;
    steveGroup.position.z = startZ + ease*1.2;
    if(t<1) requestAnimationFrame(frame);
    else { steveGroup.userData.isLying=true; spinning=false; showToast("🛏️ ЛЁГ"); }
  }
  requestAnimationFrame(frame);
}"""

if old_lie in t:
    t = t.replace(old_lie, new_lie)
    print("fixed lie fall")
else:
    print("old lie not found")

# Also ensure idle doesn't fight: set baseIdleY correctly
if "let idlePhase=0;" in t and "let baseIdleY=0;" not in t:
    t = t.replace("  let idlePhase=0;", "  let idlePhase=0;\n  let baseIdleY=0;")
    print("added baseIdleY")

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

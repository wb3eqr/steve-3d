import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# === 1. Add creeper aliases after jumpAliases ===
old_alias = 'const jumpAliases=["прыгнуть","прыжок","прыгни","джамп","прыгай","подпрыгни"];'
new_alias = """const jumpAliases=["прыгнуть","прыжок","прыгни","джамп","прыгай","подпрыгни"];
const creeperAliases=["крипер","крипером","стань крипером","креппер","creeper","превратись в крипера"];"""

if old_alias in t:
    t = t.replace(old_alias, new_alias)
    print("aliases creeper added")
else:
    print("jumpAliases not found")

# === 2. Add doCreeper function after doJump ===
old_jump_end = """function doJump(){
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

new_jump_plus_creeper = """function doJump(){
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
}
function doCreeper(){
  if(!steveGroup || spinning) return;
  spinning=true;
  showToast("💥 СТАЛ КРИПЕРОМ НА 6с!");
  // сохраняем оригинальные материалы
  const originalMats=[];
  const creeperMats=[];
  steveGroup.traverse(o=>{
    if(o.isMesh){
      originalMats.push({mesh:o, mat:o.material});
    }
  });
  // создаем текстуру крипера
  function createCreeperHeadFront(){
    const c=document.createElement("canvas"); c.width=8; c.height=8;
    const ctx=c.getContext("2d");
    // зеленый фон крипера #7FB238
    ctx.fillStyle="#7FB238"; ctx.fillRect(0,0,8,8);
    // глаза и рот крипера черные
    ctx.fillStyle="#0F0F0F";
    // левый глаз 1,2 2x2
    ctx.fillRect(1,2,2,2);
    // правый глаз 5,2 2x2
    ctx.fillRect(5,2,2,2);
    // нос/рот - центральная часть
    ctx.fillRect(2,4,1,2);
    ctx.fillRect(5,4,1,2);
    ctx.fillRect(2,6,4,1);
    ctx.fillRect(3,5,2,1);
    const tex=new THREE.CanvasTexture(c);
    tex.magFilter=THREE.NearestFilter; tex.minFilter=THREE.NearestFilter; tex.colorSpace=THREE.SRGBColorSpace;
    return tex;
  }
  function createGreenTex(){
    const c=document.createElement("canvas"); c.width=4; c.height=4;
    const ctx=c.getContext("2d");
    ctx.fillStyle="#7FB238"; ctx.fillRect(0,0,4,4);
    // слегка более темные пиксели для текстуры
    ctx.fillStyle="#5D8F2A"; ctx.fillRect(0,0,1,1); ctx.fillRect(2,2,1,1);
    const tex=new THREE.CanvasTexture(c);
    tex.magFilter=THREE.NearestFilter; tex.minFilter=THREE.NearestFilter; tex.colorSpace=THREE.SRGBColorSpace;
    return tex;
  }
  const creeperHeadTex = createCreeperHeadFront();
  const greenTex = createGreenTex();
  const darkGreen = new THREE.MeshLambertMaterial({color:0x5D8F2A});
  const greenMat = new THREE.MeshLambertMaterial({map:greenTex});
  const headCreeperMat = new THREE.MeshLambertMaterial({map:creeperHeadTex});
  // Применяем: голова - крипер лицо спереди, остальные зеленые
  steveGroup.traverse(o=>{
    if(!o.isMesh) return;
    if(o.position.y>20){ // голова
      // голова 6 материалов, меняем переднюю (4) на крипер, остальные на зеленые
      if(Array.isArray(o.material)){
        const mats=o.material;
        // mats order: right, left, top, bottom, front, back
        // передняя - index 4
        const newMats = mats.map((m,i)=>{
          if(i===4) return headCreeperMat.clone();
          if(i===2 || i===3) return new THREE.MeshLambertMaterial({color:0x7FB238}); // верх/низ
          return greenMat.clone();
        });
        o.material = newMats;
      } else {
        o.material = greenMat.clone();
      }
    } else {
      // тело, руки, ноги - зеленые
      if(Array.isArray(o.material)){
        o.material = o.material.map(()=> greenMat.clone());
      } else {
        o.material = greenMat.clone();
      }
    }
    o.material.forEach? o.material.forEach(m=> m.needsUpdate=true) : (o.material.needsUpdate=true);
  });
  // легкий эффект шипения
  steveGroup.scale.set(1.02,1.02,1.02);
  setTimeout(()=>{
    // возвращаем через 6с с эффектом
    steveGroup.traverse(o=>{
      if(!o.isMesh) return;
      // восстанавливаем оригинальные материалы
      const orig = originalMats.find(x=>x.mesh===o);
      if(orig){
        o.material = orig.mat;
        if(Array.isArray(o.material)) o.material.forEach(m=> m.needsUpdate=true);
        else o.material.needsUpdate=true;
      }
    });
    steveGroup.scale.set(1,1,1);
    spinning=false;
    showToast("✅ СНОВА СТИВ!");
  }, 6000);
}"""

if old_jump_end in t:
    t = t.replace(old_jump_end, new_jump_plus_creeper)
    print("added doCreeper")
else:
    print("old_jump not found")

# === 3. Expand achievements to 7 ===
old_ach2 = """const achievements = {
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

new_ach2 = """const achievements = {
  spin: JSON.parse(localStorage.getItem("ach_spin")||"false"),
  salto: JSON.parse(localStorage.getItem("ach_salto")||"false"),
  hit: JSON.parse(localStorage.getItem("ach_hit")||"false"),
  invis: JSON.parse(localStorage.getItem("ach_invis")||"false"),
  crouch: JSON.parse(localStorage.getItem("ach_crouch")||"false"),
  jump: JSON.parse(localStorage.getItem("ach_jump")||"false"),
  creeper: JSON.parse(localStorage.getItem("ach_creeper")||"false"),
  spinCount: parseInt(localStorage.getItem("ach_spinCount")||"0"),
  saltoCount: parseInt(localStorage.getItem("ach_saltoCount")||"0"),
  hitCount: parseInt(localStorage.getItem("ach_hitCount")||"0"),
  invisCount: parseInt(localStorage.getItem("ach_invisCount")||"0"),
  crouchCount: parseInt(localStorage.getItem("ach_crouchCount")||"0"),
  jumpCount: parseInt(localStorage.getItem("ach_jumpCount")||"0"),
  creeperCount: parseInt(localStorage.getItem("ach_creeperCount")||"0")
};"""

if old_ach2 in t:
    t = t.replace(old_ach2, new_ach2)
    print("ach 7 expanded init")
else:
    print("old_ach2 not found")

old_save2 = """function saveAch(){
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

new_save2 = """function saveAch(){
  try{
    localStorage.setItem("ach_spin", JSON.stringify(achievements.spin));
    localStorage.setItem("ach_salto", JSON.stringify(achievements.salto));
    localStorage.setItem("ach_hit", JSON.stringify(achievements.hit));
    localStorage.setItem("ach_invis", JSON.stringify(achievements.invis));
    localStorage.setItem("ach_crouch", JSON.stringify(achievements.crouch));
    localStorage.setItem("ach_jump", JSON.stringify(achievements.jump));
    localStorage.setItem("ach_creeper", JSON.stringify(achievements.creeper));
    localStorage.setItem("ach_spinCount", achievements.spinCount);
    localStorage.setItem("ach_saltoCount", achievements.saltoCount);
    localStorage.setItem("ach_hitCount", achievements.hitCount);
    localStorage.setItem("ach_invisCount", achievements.invisCount);
    localStorage.setItem("ach_crouchCount", achievements.crouchCount);
    localStorage.setItem("ach_jumpCount", achievements.jumpCount);
    localStorage.setItem("ach_creeperCount", achievements.creeperCount);
  }catch(e){ console.warn("localStorage fail",e); }
}"""

if old_save2 in t:
    t = t.replace(old_save2, new_save2)
    print("saveAch 7")

old_unlock = """function unlockAch(type){
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

new_unlock = """function unlockAch(type){
  let isNew=false;
  if(type==="spin" && !achievements.spin){ achievements.spin=true; isNew=true; }
  if(type==="salto" && !achievements.salto){ achievements.salto=true; isNew=true; }
  if(type==="hit" && !achievements.hit){ achievements.hit=true; isNew=true; }
  if(type==="invis" && !achievements.invis){ achievements.invis=true; isNew=true; }
  if(type==="crouch" && !achievements.crouch){ achievements.crouch=true; isNew=true; }
  if(type==="jump" && !achievements.jump){ achievements.jump=true; isNew=true; }
  if(type==="creeper" && !achievements.creeper){ achievements.creeper=true; isNew=true; }
  if(type==="spin") achievements.spinCount++;
  if(type==="salto") achievements.saltoCount++;
  if(type==="hit") achievements.hitCount++;
  if(type==="invis") achievements.invisCount++;
  if(type==="crouch") achievements.crouchCount++;
  if(type==="jump") achievements.jumpCount++;
  if(type==="creeper") achievements.creeperCount++;
  saveAch();
  renderBook();
  const names={spin:"МАСТЕР ВРАЩЕНИЯ",salto:"САЛЬТО-МАСТЕР",hit:"МАСТЕР УДАРА",invis:"НЕВИДИМКА",crouch:"МАСТЕР СКРЫТНОСТИ",jump:"ДЖЕМП-МАСТЕР",creeper:"КРИПЕР"};
  if(isNew){ showToast("🏆 Ачивка: "+(names[type]||type)+"!"); }
}"""

if old_unlock in t:
    t = t.replace(old_unlock, new_unlock)
    print("unlock 7")

# Update renderBook total 6 -> 7
old_render = """  const total=6;
  const done=(achievements.spin?1:0)+(achievements.salto?1:0)+(achievements.hit?1:0)+(achievements.invis?1:0)+(achievements.crouch?1:0)+(achievements.jump?1:0);"""

new_render = """  const total=7;
  const done=(achievements.spin?1:0)+(achievements.salto?1:0)+(achievements.hit?1:0)+(achievements.invis?1:0)+(achievements.crouch?1:0)+(achievements.jump?1:0)+(achievements.creeper?1:0);"""

if old_render in t:
    t = t.replace(old_render, new_render)
    print("total 7")

# Add creeper entry in renderBook
old_creeper_entry = """  if(achievements.jump){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>ПРЫЖОК — прыжок вверх<br><small style="font-size:10px;color:#6B6B6B">прыгнуть, прыжок, прыгни, джамп, прыгай, подпрыгни</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.jumpCount} раз</small></span></div>`;
  }"""

new_creeper_entry = """  if(achievements.jump){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>ПРЫЖОК — прыжок вверх<br><small style="font-size:10px;color:#6B6B6B">прыгнуть, прыжок, прыгни, джамп, прыгай, подпрыгни</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.jumpCount} раз</small></span></div>`;
  }
  if(achievements.creeper){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>КРИПЕР — превращение 6с<br><small style="font-size:10px;color:#6B6B6B">крипер, крипером, стань крипером, креппер, creeper, превратись в крипера</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.creeperCount} раз</small></span></div>`;
  }"""

if old_creeper_entry in t:
    t = t.replace(old_creeper_entry, new_creeper_entry)
    print("creeper entry added")

# Add handleCmd for creeper
old_handle = """  } else if(matchesAliases(norm, jumpAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("jump");
    doJump();
    input.value="";
  } else {"""

new_handle = """  } else if(matchesAliases(norm, jumpAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("jump");
    doJump();
    input.value="";
  } else if(matchesAliases(norm, creeperAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("creeper");
    doCreeper();
    input.value="";
  } else {"""

if old_handle in t:
    t = t.replace(old_handle, new_handle)
    print("handle creeper added")

# Update placeholder hint
t = t.replace('placeholder="команда..."', 'placeholder="крипер..."')

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

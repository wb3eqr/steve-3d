import pathlib, shutil, re, base64
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# Update skinB64 from b64.txt
b64 = pathlib.Path(r"C:\project\steve-minecraft-png\b64.txt").read_text(encoding="utf-8")
t = re.sub(r'const skinB64 = "[^"]+";', f'const skinB64 = "{b64}";', t)
print("updated skinB64 len", len(b64))

# === 1. Improve creeper transformation to be beautiful ===
old_creeper = """function doCreeper(){
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

new_creeper_beautiful = """function doCreeper(){
  if(!steveGroup || spinning) return;
  spinning=true;
  // красивое превращение: вспышка + плавный морфинг
  const originalMats=[];
  steveGroup.traverse(o=>{ if(o.isMesh) originalMats.push({mesh:o, mat:o.material}); });
  function createCreeperHeadFront(){
    const c=document.createElement("canvas"); c.width=8; c.height=8;
    const ctx=c.getContext("2d");
    ctx.fillStyle="#7FB238"; ctx.fillRect(0,0,8,8);
    ctx.fillStyle="#0F0F0F";
    ctx.fillRect(1,2,2,2); ctx.fillRect(5,2,2,2);
    ctx.fillRect(2,4,1,2); ctx.fillRect(5,4,1,2);
    ctx.fillRect(2,6,4,1); ctx.fillRect(3,5,2,1);
    const tex=new THREE.CanvasTexture(c);
    tex.magFilter=THREE.NearestFilter; tex.minFilter=THREE.NearestFilter; tex.colorSpace=THREE.SRGBColorSpace;
    return tex;
  }
  function createGreenTex(){
    const c=document.createElement("canvas"); c.width=32; c.height=32;
    const ctx=c.getContext("2d");
    ctx.fillStyle="#7FB238"; ctx.fillRect(0,0,32,32);
    // добавляем шум для качественной текстуры
    for(let i=0;i<40;i++){
      ctx.fillStyle = Math.random()>0.5 ? "#6FA530" : "#8BC34A";
      const x=Math.floor(Math.random()*32), y=Math.floor(Math.random()*32);
      ctx.fillRect(x,y,1,1);
    }
    ctx.fillStyle="rgba(0,0,0,0.08)"; ctx.fillRect(0,0,32,2); ctx.fillRect(0,30,32,2);
    const tex=new THREE.CanvasTexture(c);
    tex.magFilter=THREE.NearestFilter; tex.minFilter=THREE.LinearMipmapLinearFilter; tex.colorSpace=THREE.SRGBColorSpace;
    return tex;
  }
  const creeperHeadTex = createCreeperHeadFront();
  const greenTex = createGreenTex();
  // Фаза 1: быстрое исчезновение с шипением и вспышкой
  const matsFade=[];
  steveGroup.traverse(o=>{ if(o.isMesh){ if(Array.isArray(o.material)) matsFade.push(...o.material); else matsFade.push(o.material); }});
  matsFade.forEach(m=>{ m.transparent=true; });
  let t0=performance.now();
  const fadeOut=380;
  function fadeToCreeper(now){
    const e=now-t0;
    const p=Math.min(e/fadeOut,1);
    const ease=1 - Math.pow(1-p,3);
    const opacity=1-ease;
    const scale=1 + ease*0.08;
    const flash = Math.sin(p*Math.PI*3)*0.15;
    matsFade.forEach(m=>{ m.opacity=1 - ease*0.95; m.needsUpdate=true; });
    steveGroup.scale.set(scale,scale,scale);
    steveGroup.rotation.y = ease*0.35;
    renderer.domElement.style.filter = `brightness(${1+flash}) saturate(${1+flash*0.5})`;
    if(p<1){
      requestAnimationFrame(fadeToCreeper);
    } else {
      // Меняем материалы на крипера
      const greenMat = new THREE.MeshLambertMaterial({map:greenTex});
      const headMat = new THREE.MeshLambertMaterial({map:creeperHeadTex});
      steveGroup.traverse(o=>{
        if(!o.isMesh) return;
        if(o.position.y>20){
          if(Array.isArray(o.material)){
            const newMats = o.material.map((m,i)=>{
              if(i===4) return headMat.clone();
              if(i===2 || i===3) return new THREE.MeshLambertMaterial({color:0x7FB238});
              return greenMat.clone();
            });
            o.material=newMats;
          } else o.material=greenMat.clone();
        } else {
          if(Array.isArray(o.material)) o.material=o.material.map(()=> greenMat.clone());
          else o.material=greenMat.clone();
        }
      });
      steveGroup.scale.set(1.08,0.96,1.08);
      // Фаза 2: появление крипера
      const t1=performance.now();
      function appear(now2){
        const e2=now2-t1;
        const p2=Math.min(e2/320,1);
        const ease2=1 - Math.pow(1-p2,3);
        steveGroup.scale.set(1.08 - ease2*0.08, 0.96 + ease2*0.04, 1.08 - ease2*0.08);
        steveGroup.traverse(o=>{ if(o.isMesh){ const mats=o.material; const arr=Array.isArray(mats)?mats:[mats]; arr.forEach(m=>{ m.opacity=ease2; m.transparent=ease2<1; m.needsUpdate=true; }); }});
        renderer.domElement.style.filter = `brightness(${1 + (1-ease2)*0.12})`;
        if(p2<1) requestAnimationFrame(appear);
        else {
          steveGroup.traverse(o=>{ if(o.isMesh){ const arr=Array.isArray(o.material)?o.material:[o.material]; arr.forEach(m=>{ m.opacity=1; m.transparent=false; }); }});
          renderer.domElement.style.filter="";
          showToast("💥 КРИПЕР 6с! Шипит...");
          // Держим 6с
          setTimeout(()=>{
            // Фаза 3: обратное превращение - плавно
            const mats2=[];
            steveGroup.traverse(o=>{ if(o.isMesh){ const arr=Array.isArray(o.material)?o.material:[o.material]; mats2.push(...arr); }});
            mats2.forEach(m=>{ m.transparent=true; });
            const t2=performance.now();
            function fadeBack(now3){
              const e3=now3-t2;
              const p3=Math.min(e3/360,1);
              const ease3=1 - Math.pow(1-p3,3);
              mats2.forEach(m=>{ m.opacity=1-ease3; });
              steveGroup.scale.set(1 + ease3*0.06, 1 - ease3*0.04, 1 + ease3*0.06);
              renderer.domElement.style.filter = `brightness(${1+ ease3*0.1})`;
              if(p3<1){
                requestAnimationFrame(fadeBack);
              } else {
                // восстанавливаем
                steveGroup.traverse(o=>{
                  if(!o.isMesh) return;
                  const orig=originalMats.find(x=>x.mesh===o);
                  if(orig){ o.material=orig.mat; const arr=Array.isArray(o.material)?o.material:[o.material]; arr.forEach(m=>{ m.opacity=1; m.transparent=false; m.needsUpdate=true; }); }
                });
                // появление Стива
                const mats3=[];
                steveGroup.traverse(o=>{ if(o.isMesh){ const arr=Array.isArray(o.material)?o.material:[o.material]; mats3.push(...arr); }});
                mats3.forEach(m=>{ m.transparent=true; m.opacity=0; });
                const t3=performance.now();
                function appearSteve(now4){
                  const e4=now4-t3;
                  const p4=Math.min(e4/300,1);
                  const ease4=1 - Math.pow(1-p4,3);
                  mats3.forEach(m=>{ m.opacity=ease4; });
                  steveGroup.scale.set(0.96 + ease4*0.04, 1.08 - ease4*0.08, 0.96 + ease4*0.04);
                  if(p4<1) requestAnimationFrame(appearSteve);
                  else {
                    mats3.forEach(m=>{ m.opacity=1; m.transparent=false; });
                    steveGroup.scale.set(1,1,1);
                    steveGroup.rotation.y=0;
                    renderer.domElement.style.filter="";
                    spinning=false;
                    showToast("✅ СНОВА СТИВ-КОТИК!");
                  }
                }
                requestAnimationFrame(appearSteve);
              }
            }
            requestAnimationFrame(fadeBack);
          }, 6000);
        }
      }
      requestAnimationFrame(appear);
    }
  }
  requestAnimationFrame(fadeToCreeper);
}"""

if old_creeper in t:
    t = t.replace(old_creeper, new_creeper_beautiful)
    print("creeper beautiful patched")
else:
    print("old creeper not found")

# === 2. Add lie command ===
old_jump_alias = 'const creeperAliases=["крипер","крипером","стань крипером","креппер","creeper","превратись в крипера"];'
new_jump_alias = '''const creeperAliases=["крипер","крипером","стань крипером","креппер","creeper","превратись в крипера"];
const lieAliases=["лечь","ляг","лежать","улечься","отдохнуть","прилечь","ложись"];'''

if old_jump_alias in t:
    t = t.replace(old_jump_alias, new_jump_alias)
    print("lie aliases added")
else:
    print("creeperAliases not found")

# Add doLie function after doCreeper
old_creeper_end = '  requestAnimationFrame(fadeToCreeper);\n}'

if old_creeper_end in t and 'function doLie' not in t:
    lie_func = """
function doLie(){
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
}
"""
    t = t.replace(old_creeper_end, old_creeper_end + lie_func)
    print("doLie added")

# Expand achievements to 8
old_ach_init = """  creeper: JSON.parse(localStorage.getItem("ach_creeper")||"false"),
  spinCount: parseInt(localStorage.getItem("ach_spinCount")||"0"),"""

new_ach_init = """  creeper: JSON.parse(localStorage.getItem("ach_creeper")||"false"),
  lie: JSON.parse(localStorage.getItem("ach_lie")||"false"),
  spinCount: parseInt(localStorage.getItem("ach_spinCount")||"0"),"""

if old_ach_init in t:
    t = t.replace(old_ach_init, new_ach_init, 1)
    print("ach lie init added")

old_ach_init2 = '  creeperCount: parseInt(localStorage.getItem("ach_creeperCount")||"0")'
new_ach_init2 = '  creeperCount: parseInt(localStorage.getItem("ach_creeperCount")||"0"),\n  lieCount: parseInt(localStorage.getItem("ach_lieCount")||"0")'
if old_ach_init2 in t:
    t = t.replace(old_ach_init2, new_ach_init2, 1)
    print("lieCount added")

old_save = '    localStorage.setItem("ach_creeper", JSON.stringify(achievements.creeper));'
new_save = '    localStorage.setItem("ach_creeper", JSON.stringify(achievements.creeper));\n    localStorage.setItem("ach_lie", JSON.stringify(achievements.lie));'
if old_save in t:
    t = t.replace(old_save, new_save, 1)
    print("save lie")

old_save2 = '    localStorage.setItem("ach_creeperCount", achievements.creeperCount);'
new_save2 = '    localStorage.setItem("ach_creeperCount", achievements.creeperCount);\n    localStorage.setItem("ach_lieCount", achievements.lieCount);'
if old_save2 in t:
    t = t.replace(old_save2, new_save2, 1)
    print("save lieCount")

old_unlock_creeper = '  if(type==="creeper" && !achievements.creeper){ achievements.creeper=true; isNew=true; }'
new_unlock_creeper = '  if(type==="creeper" && !achievements.creeper){ achievements.creeper=true; isNew=true; }\n  if(type==="lie" && !achievements.lie){ achievements.lie=true; isNew=true; }'
if old_unlock_creeper in t:
    t = t.replace(old_unlock_creeper, new_unlock_creeper, 1)
    print("unlock lie")

old_unlock2 = '  if(type==="creeper") achievements.creeperCount++;'
new_unlock2 = '  if(type==="creeper") achievements.creeperCount++;\n  if(type==="lie") achievements.lieCount++;'
if old_unlock2 in t:
    t = t.replace(old_unlock2, new_unlock2, 1)
    print("unlock lieCount")

old_names = '  const names={spin:"МАСТЕР ВРАЩЕНИЯ",salto:"САЛЬТО-МАСТЕР",hit:"МАСТЕР УДАРА",invis:"НЕВИДИМКА",crouch:"МАСТЕР СКРЫТНОСТИ",jump:"ДЖЕМП-МАСТЕР",creeper:"КРИПЕР"};'
new_names = '  const names={spin:"МАСТЕР ВРАЩЕНИЯ",salto:"САЛЬТО-МАСТЕР",hit:"МАСТЕР УДАРА",invis:"НЕВИДИМКА",crouch:"МАСТЕР СКРЫТНОСТИ",jump:"ДЖЕМП-МАСТЕР",creeper:"КРИПЕР",lie:"СОНЯ"};'
if old_names in t:
    t = t.replace(old_names, new_names)
    print("names lie")

# total 7 -> 8
old_total = '  const total=7;'
new_total = '  const total=8;'
if old_total in t:
    t = t.replace(old_total, new_total, 1)
    print("total 8")

old_done = '  const done=(achievements.spin?1:0)+(achievements.salto?1:0)+(achievements.hit?1:0)+(achievements.invis?1:0)+(achievements.crouch?1:0)+(achievements.jump?1:0)+(achievements.creeper?1:0);'
new_done = '  const done=(achievements.spin?1:0)+(achievements.salto?1:0)+(achievements.hit?1:0)+(achievements.invis?1:0)+(achievements.crouch?1:0)+(achievements.jump?1:0)+(achievements.creeper?1:0)+(achievements.lie?1:0);'
if old_done in t:
    t = t.replace(old_done, new_done, 1)
    print("done 8")

old_entry_jump = '  if(achievements.creeper){'
new_entry_jump = '''  if(achievements.creeper){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>КРИПЕР — превращение 6с<br><small style="font-size:10px;color:#6B6B6B">крипер, крипером, стань крипером, креппер, creeper, превратись в крипера</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.creeperCount} раз</small></span></div>`;
  }
  if(achievements.lie){'''

if old_entry_jump in t and 'achievements.lie' not in t.split('if(achievements.creeper)')[1].split('if(html')[0] or t.count('achievements.lie')<3:
    # Only replace first occurrence of creeper entry header to add lie after jump? Actually we need to add lie entry after creeper
    # Find creeper entry block and add lie after it
    old_lie_entry = '''  if(achievements.creeper){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>КРИПЕР — превращение 6с<br><small style="font-size:10px;color:#6B6B6B">крипер, крипером, стань крипером, креппер, creeper, превратись в крипера</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.creeperCount} раз</small></span></div>`;
  }'''
    new_lie_entry = '''  if(achievements.creeper){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>КРИПЕР — превращение 6с<br><small style="font-size:10px;color:#6B6B6B">крипер, крипером, стань крипером, креппер, creeper, превратись в крипера</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.creeperCount} раз</small></span></div>`;
  }
  if(achievements.lie){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>ЛЕЧЬ — котик спит<br><small style="font-size:10px;color:#6B6B6B">лечь, ляг, лежать, улечься, отдохнуть, прилечь, ложись</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.lieCount} раз</small></span></div>`;
  }'''
    if old_lie_entry in t:
        t = t.replace(old_lie_entry, new_lie_entry, 1)
        print("lie entry added")
    else:
        print("old creeper entry not found for lie")

# Add handleCmd for lie
old_handle_lie = '  } else if(matchesAliases(norm, creeperAliases)){'
new_handle_lie = '''  } else if(matchesAliases(norm, creeperAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("creeper");
    doCreeper();
    input.value="";
  } else if(matchesAliases(norm, lieAliases)){'''

if old_handle_lie in t and 'lieAliases' not in t.split(old_handle_lie)[1][:200]:
    t = t.replace(old_handle_lie, new_handle_lie, 1)
    print("handle lie first part")
    # Need to add the second part after
    # Find the next else { after creeper
    # Replace the else after creeper handle
    t = t.replace(
        '    doCreeper();\n    input.value="";\n  } else {',
        '    doCreeper();\n    input.value="";\n  } else if(matchesAliases(norm, lieAliases)){\n    lastCmdNorm=norm; lastCmdTime=now;\n    unlockAch("lie");\n    doLie();\n    input.value="";\n  } else {',
        1
    )
    # The above double-replaced, need to clean duplicate
    # Remove duplicate we just added
    t = t.replace('  } else if(matchesAliases(norm, lieAliases)){\n    lastCmdNorm=norm; lastCmdTime=now;\n    unlockAch("lie");\n    doLie();\n    input.value="";\n  } else if(matchesAliases(norm, lieAliases)){', '  } else if(matchesAliases(norm, lieAliases)){', 1)
    print("handle lie added")
else:
    # If creeper handle already has lie, check
    if 'doLie()' in t:
        print("handle lie already there")
    else:
        print("handle lie not found")

# Update placeholder
t = t.replace('placeholder="крипер..."', 'placeholder="крипер, лечь..."')

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

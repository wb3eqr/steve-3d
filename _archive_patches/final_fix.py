import pathlib, shutil, re, base64
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# Update Steve skinB64 to current cat gray (4144)
steve_b64 = pathlib.Path(r"C:\project\steve-minecraft-png\b64.txt").read_text(encoding="utf-8").strip()
# If b64.txt is 3440 (cat superman), we need 4144 (cat gray) - currently b64.txt is 3440 after quality patch, but steve-2d-skin.png is now 3108 gray, so b64 should be 4144
# Regenerate from current steve-2d-skin.png
steve_bytes = pathlib.Path(r"C:\project\steve-minecraft-png\steve-2d-skin.png").read_bytes()
steve_b64 = base64.b64encode(steve_bytes).decode()
pathlib.Path(r"C:\project\steve-minecraft-png\b64.txt").write_text(steve_b64)
print("steve b64 len", len(steve_b64))
t = re.sub(r'const skinB64 = "[^"]+";', f'const skinB64 = "{steve_b64}";', t, count=1)
print("updated steve skinB64")

# Load creeper quality HD skin and embed for creeper transformation
creeper_path = pathlib.Path(r"C:\project\steve-minecraft-png\creeper_quality_hd.png")
if not creeper_path.exists():
    # fallback: create it
    from PIL import Image, ImageDraw
    im = Image.new('RGBA', (64,64), (0,0,0,0))
    draw = ImageDraw.Draw(im)
    base = (127,178,56,255); dark=(93,143,42,255); light=(139,195,74,255); black=(15,15,15,255)
    for x in range(8,16):
        for y in range(0,8):
            im.putpixel((x,y), light if (x+y)%3==0 else dark if (x+y)%5==0 else base)
    for x in range(8,16):
        for y in range(8,16):
            im.putpixel((x,y), base)
    for x in range(9,11):
        for y in range(10,12):
            im.putpixel((x,y), black)
    for x in range(13,15):
        for y in range(10,12):
            im.putpixel((x,y), black)
    for x in range(10,12):
        for y in range(12,14):
            im.putpixel((x,y), black)
    for x in range(13,15):
        for y in range(12,14):
            im.putpixel((x,y), black)
    for x in range(10,14):
        for y in range(14,15):
            im.putpixel((x,y), black)
    for x in range(11,13):
        for y in range(13,14):
            im.putpixel((x,y), black)
    for x in range(0,8):
        for y in range(8,16):
            im.putpixel((x,y), dark if x%2==0 else base)
    for x in range(16,24):
        for y in range(8,16):
            im.putpixel((x,y), dark)
    for x in range(24,32):
        for y in range(8,16):
            im.putpixel((x,y), base)
    for x in range(20,28):
        for y in range(20,32):
            im.putpixel((x,y), light if (x+y)%4==0 else dark if (x+y)%7==0 else base)
    for x in range(16,20):
        for y in range(20,32):
            im.putpixel((x,y), dark)
    for x in range(28,32):
        for y in range(20,32):
            im.putpixel((x,y), dark)
    for x in range(32,40):
        for y in range(20,32):
            im.putpixel((x,y), base)
    for x in range(44,48):
        for y in range(20,32):
            im.putpixel((x,y), base if (x+y)%3 else light)
    for x in range(40,44):
        for y in range(20,32):
            im.putpixel((x,y), dark)
    for x in range(4,8):
        for y in range(20,32):
            im.putpixel((x,y), dark)
    for x in range(20,24):
        for y in range(52,64):
            im.putpixel((x,y), base)
    im.save(creeper_path)
    print("created creeper hd")

creeper_b64 = base64.b64encode(creeper_path.read_bytes()).decode()
print("creeper b64 len", len(creeper_b64))

# Inject creeperB64 constant after skinB64
if 'const creeperB64' not in t:
    t = t.replace(
        f'const skinB64 = "{steve_b64}";',
        f'const skinB64 = "{steve_b64}";\nconst creeperB64 = "{creeper_b64}"; // качественный скин крипера 64x64 HD'
    )
    print("injected creeperB64")
else:
    t = re.sub(r'const creeperB64 = "[^"]+";', f'const creeperB64 = "{creeper_b64}";', t)
    print("updated creeperB64")

# Update doCreeper to use quality skin + beautiful transformation
old_creeper = re.search(r'function doCreeper\(\)\{.*?requestAnimationFrame\(fadeToCreeper\);\n\}', t, flags=re.DOTALL)
if old_creeper:
    new_creeper = """function doCreeper(){
  if(!steveGroup || spinning) return;
  spinning=true;
  showToast("💥 КРИПЕР! Красивое превращение...");
  const originalMats=[];
  steveGroup.traverse(o=>{ if(o.isMesh) originalMats.push({mesh:o, mat:o.material}); });
  // Загружаем качественный скин крипера
  const creeperImg = new Image();
  creeperImg.src = "data:image/png;base64," + creeperB64;
  creeperImg.onload = ()=>{
    const tex = new THREE.Texture(creeperImg);
    tex.magFilter=THREE.NearestFilter; tex.minFilter=THREE.NearestFilter; tex.colorSpace=THREE.SRGBColorSpace; tex.needsUpdate=true;
    // красивый морфинг: вспышка + частицы
    const matsFade=[];
    steveGroup.traverse(o=>{ if(o.isMesh){ const arr=Array.isArray(o.material)?o.material:[o.material]; matsFade.push(...arr); }});
    matsFade.forEach(m=>{ m.transparent=true; });
    let t0=performance.now();
    const fadeOut=320;
    function fadeToCreeper(now){
      const e=now-t0;
      const p=Math.min(e/fadeOut,1);
      const ease=1 - Math.pow(1-p,3);
      const opacity=1-ease;
      const scale=1 + ease*0.09;
      const flash = Math.sin(p*Math.PI*2)*0.12;
      matsFade.forEach(m=>{ m.opacity=opacity; m.needsUpdate=true; });
      steveGroup.scale.set(scale,scale,scale);
      steveGroup.rotation.y = ease*0.45;
      // зеленый туман
      renderer.domElement.style.filter = `brightness(${1+flash}) hue-rotate(${ease*18}deg) saturate(${1+flash})`;
      // частицы крипера
      if(p>0.3 && p<0.6 && Math.random()>0.7){
        const particle=document.createElement("div");
        particle.textContent="💚";
        particle.style.cssText="position:fixed;left:"+(innerWidth/2 + (Math.random()-0.5)*120)+"px;top:"+(innerHeight/2 + (Math.random()-0.5)*120)+"px;font-size:14px;pointer-events:none;z-index:20;transition: transform 600ms, opacity 600ms";
        document.body.appendChild(particle);
        setTimeout(()=>{ particle.style.transform="translateY(-40px) scale(1.4)"; particle.style.opacity="0"; }, 20);
        setTimeout(()=> particle.remove(), 650);
      }
      if(p<1){
        requestAnimationFrame(fadeToCreeper);
      } else {
        // Меняем на качественный скин крипера - используем тот же buildSteve логику но с новой текстурой
        // Создаем материалы из качественного скина
        function faceTexFromImg(sx,sy,w,h){
          const c=document.createElement("canvas"); c.width=w; c.height=h;
          const ctx=c.getContext("2d"); ctx.imageSmoothingEnabled=false;
          ctx.drawImage(tex.image,sx,sy,w,h,0,0,w,h);
          const t2=new THREE.CanvasTexture(c); t2.magFilter=THREE.NearestFilter; t2.minFilter=THREE.NearestFilter; t2.colorSpace=THREE.SRGBColorSpace; return t2;
        }
        steveGroup.traverse(o=>{
          if(!o.isMesh) return;
          if(o.position.y>20){ // голова
            if(Array.isArray(o.material)){
              const newMats = o.material.map((m,i)=>{
                if(i===4) return new THREE.MeshLambertMaterial({map: faceTexFromImg(8,8,8,8)});
                if(i===0) return new THREE.MeshLambertMaterial({map: faceTexFromImg(0,8,8,8)});
                if(i===1) return new THREE.MeshLambertMaterial({map: faceTexFromImg(16,8,8,8)});
                if(i===2) return new THREE.MeshLambertMaterial({map: faceTexFromImg(8,0,8,8)});
                if(i===3) return new THREE.MeshLambertMaterial({map: faceTexFromImg(16,0,8,8)});
                return new THREE.MeshLambertMaterial({map: faceTexFromImg(24,8,8,8)});
              });
              o.material=newMats;
            } else o.material=new THREE.MeshLambertMaterial({map: faceTexFromImg(8,8,8,8)});
          } else if(o.position.y>8){ // тело/руки
            const isBody = Math.abs(o.position.x)<1;
            const sx = isBody ? 20 : (o.position.x<0 ? 44 : 36);
            const sy = isBody ? 20 : (o.position.x<0 ? 20 : 52);
            // упрощено: тело/руки используют соответствующие части скина
            if(Array.isArray(o.material)){
              o.material = o.material.map((m,i)=>{
                // используем зеленый паттерн из скина
                const map = o.position.y>8 && Math.abs(o.position.x)<1 ? faceTexFromImg(20,20,8,12) : faceTexFromImg(sx,sy,4,12);
                return new THREE.MeshLambertMaterial({map});
              });
            } else o.material=new THREE.MeshLambertMaterial({map: faceTexFromImg(20,20,8,12)});
          } else { // ноги
            const sx = o.position.x<0 ? 4 : 20;
            const sy = o.position.x<0 ? 20 : 52;
            if(Array.isArray(o.material)){
              o.material = o.material.map(()=> new THREE.MeshLambertMaterial({map: faceTexFromImg(sx,sy,4,12)}));
            } else o.material=new THREE.MeshLambertMaterial({map: faceTexFromImg(sx,sy,4,12)});
          }
          const arr=Array.isArray(o.material)?o.material:[o.material];
          arr.forEach(m=>{ m.opacity=0; m.transparent=true; m.needsUpdate=true; });
        });
        steveGroup.scale.set(0.88,1.12,0.88);
        const t1=performance.now();
        function appear(now2){
          const e2=now2-t1;
          const p2=Math.min(e2/380,1);
          const ease2=1 - Math.pow(1-p2,3);
          steveGroup.scale.set(0.88 + ease2*0.12, 1.12 - ease2*0.12, 0.88 + ease2*0.12);
          steveGroup.traverse(o=>{ if(o.isMesh){ const arr=Array.isArray(o.material)?o.material:[o.material]; arr.forEach(m=>{ m.opacity=ease2; }); }});
          renderer.domElement.style.filter = `brightness(${1 + (1-ease2)*0.14}) hue-rotate(${(1-ease2)*10}deg)`;
          if(p2<1) requestAnimationFrame(appear);
          else {
            steveGroup.traverse(o=>{ if(o.isMesh){ const arr=Array.isArray(o.material)?o.material:[o.material]; arr.forEach(m=>{ m.opacity=1; m.transparent=false; m.needsUpdate=true; }); }});
            steveGroup.scale.set(1,1,1);
            steveGroup.rotation.y=0;
            renderer.domElement.style.filter="";
            showToast("💚 КРИПЕР 6с! Tsss...");
            setTimeout(()=>{
              // обратно - красиво
              const mats2=[];
              steveGroup.traverse(o=>{ if(o.isMesh){ const arr=Array.isArray(o.material)?o.material:[o.material]; mats2.push(...arr); }});
              mats2.forEach(m=>{ m.transparent=true; });
              const t2=performance.now();
              function fadeBack(now3){
                const e3=now3-t2;
                const p3=Math.min(e3/340,1);
                const ease3=1 - Math.pow(1-p3,3);
                mats2.forEach(m=>{ m.opacity=1-ease3; });
                steveGroup.scale.set(1 + ease3*0.07, 1 - ease3*0.05, 1 + ease3*0.07);
                renderer.domElement.style.filter = `brightness(${1+ ease3*0.12}) hue-rotate(${ease3*12}deg)`;
                if(p3<1) requestAnimationFrame(fadeBack);
                else {
                  steveGroup.traverse(o=>{
                    if(!o.isMesh) return;
                    const orig=originalMats.find(x=>x.mesh===o);
                    if(orig){ o.material=orig.mat; const arr=Array.isArray(o.material)?o.material:[o.material]; arr.forEach(m=>{ m.opacity=1; m.transparent=false; m.needsUpdate=true; }); }
                  });
                  const mats3=[];
                  steveGroup.traverse(o=>{ if(o.isMesh){ const arr=Array.isArray(o.material)?o.material:[o.material]; mats3.push(...arr); }});
                  mats3.forEach(m=>{ m.transparent=true; m.opacity=0; });
                  const t3=performance.now();
                  function appearSteve(now4){
                    const e4=now4-t3;
                    const p4=Math.min(e4/320,1);
                    const ease4=1 - Math.pow(1-p4,3);
                    mats3.forEach(m=>{ m.opacity=ease4; });
                    steveGroup.scale.set(0.92 + ease4*0.08, 1.06 - ease4*0.06, 0.92 + ease4*0.08);
                    if(p4<1) requestAnimationFrame(appearSteve);
                    else {
                      mats3.forEach(m=>{ m.opacity=1; m.transparent=false; });
                      steveGroup.scale.set(1,1,1);
                      renderer.domElement.style.filter="";
                      spinning=false;
                      showToast("✅ СНОВА КОТИК!");
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
  }
}"""
    t = re.sub(r'function doCreeper\(\)\{.*?requestAnimationFrame\(fadeToCreeper\);\n\}', new_creeper, t, flags=re.DOTALL, count=1)
    print("creeper beautiful with quality skin patched")

# Ensure lie still exists
if 'function doLie' not in t:
    print("lie missing, adding")
    # add lie after creeper
    t = t.replace('  requestAnimationFrame(fadeToCreeper);\n}', '  requestAnimationFrame(fadeToCreeper);\n}\nfunction doLie(){\n  if(!steveGroup || spinning) return;\n  if(steveGroup.userData.isLying){ spinning=true; const s=performance.now(); const sy=steveGroup.position.y; const sr=steveGroup.rotation.x; function f(n){const tt=Math.min((n-s)/500,1);const e=1-Math.pow(1-tt,3);steveGroup.rotation.x=sr*(1-e);steveGroup.position.y=sy+(0-sy)*e; if(tt<1) requestAnimationFrame(f); else {steveGroup.rotation.x=0; steveGroup.position.y=0; steveGroup.userData.isLying=false; spinning=false; showToast("🧍 ВСТАЛ!");}} requestAnimationFrame(f); return;}\n  spinning=true; const sy2=steveGroup.position.y; const s2=performance.now(); function f2(n){const tt=Math.min((n-s2)/550,1);const e=1-Math.pow(1-tt,3); steveGroup.rotation.x=e*Math.PI/2; steveGroup.position.y=sy2 - e*5.2; steveGroup.position.z=e*2; if(tt<1) requestAnimationFrame(f2); else {steveGroup.userData.isLying=true; spinning=false; showToast("🛏️ ЛЁГ");}} requestAnimationFrame(f2);\n}')
else:
    print("lie exists")

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))
print("steve skin restored cat", "3108" in str(pathlib.Path(r"C:\project\steve-minecraft-png\steve-2d-skin.png").stat().st_size))
print("creeper hd exists", pathlib.Path(r"C:\project\steve-minecraft-png\creeper_quality_hd.png").exists())

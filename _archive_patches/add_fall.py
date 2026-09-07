import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# Add fallAliases after lieAliases
old_lie_alias = 'const lieAliases=["лечь","ляг","лежать","улечься","отдохнуть","прилечь","ложись"];'
new_lie_alias = '''const lieAliases=["лечь","ляг","лежать","улечься","отдохнуть","прилечь","ложись"];
const fallAliases=["упал","упасть","падать","падение","свалился","грохнулся","повалился","уронился"];'''

if old_lie_alias in t:
    t = t.replace(old_lie_alias, new_lie_alias)
    print("added fallAliases")
else:
    print("lieAliases not found")

# Add doFall function after doLie
old_lie_end = '  requestAnimationFrame(f2);\n}'
# Find doLie end
if 'function doLie(){' in t:
    # Find the end of doLie (second requestAnimationFrame)
    # Replace after doLie
    old_lie_block = re.search(r'function doLie\(\)\{.*?requestAnimationFrame\(f2\);\n\}', t, flags=re.DOTALL)
    if old_lie_block:
        new_block = old_lie_block.group(0) + """

function doFall(){
  if(!steveGroup || spinning) return;
  spinning=true;
  showToast("💥 УПАЛ!");
  const startY=steveGroup.position.y;
  const startRotX=steveGroup.rotation.x;
  const startRotZ=steveGroup.rotation.z;
  const dur=700;
  const start=performance.now();
  function frame(now){
    const tt=Math.min((now-start)/dur,1);
    const ease=1 - Math.pow(1-tt,3);
    // падение вперед: наклон + падение на бок
    steveGroup.rotation.x = ease * (Math.PI/2 * 0.85);
    steveGroup.rotation.z = ease * 0.35;
    steveGroup.position.y = startY - ease*4.2;
    steveGroup.position.z = ease*1.0;
    if(tt<1) requestAnimationFrame(frame);
    else {
      // полежал 800ms и встает
      setTimeout(()=>{
        const t2=performance.now();
        const dur2=520;
        function up(now2){
          const tt2=Math.min((now2-t2)/dur2,1);
          const e2=1 - Math.pow(1-tt2,3);
          steveGroup.rotation.x = (Math.PI/2*0.85)*(1-e2);
          steveGroup.rotation.z = 0.35*(1-e2);
          steveGroup.position.y = (startY-4.2) + 4.2*e2;
          steveGroup.position.z = 1.0*(1-e2);
          if(tt2<1) requestAnimationFrame(up);
          else { steveGroup.rotation.x=0; steveGroup.rotation.z=0; steveGroup.position.y=0; steveGroup.position.z=0; spinning=false; showToast("🧍 ВСТАЛ!"); }
        }
        requestAnimationFrame(up);
      }, 800);
    }
  }
  requestAnimationFrame(frame);
}"""
        t = t.replace(old_lie_block.group(0), new_block)
        print("added doFall")
    else:
        print("doLie block not found")
else:
    print("doLie not found")

# Update achievements to 9
old_ach = '  creeper: JSON.parse(localStorage.getItem("ach_creeper")||"false"),\n  lie: JSON.parse(localStorage.getItem("ach_lie")||"false"),'
new_ach = '  creeper: JSON.parse(localStorage.getItem("ach_creeper")||"false"),\n  lie: JSON.parse(localStorage.getItem("ach_lie")||"false"),\n  fall: JSON.parse(localStorage.getItem("ach_fall")||"false"),'
if old_ach in t:
    t = t.replace(old_ach, new_ach, 1)
    print("ach fall init")

old_ach2 = '  creeperCount: parseInt(localStorage.getItem("ach_creeperCount")||"0"),\n  lieCount: parseInt(localStorage.getItem("ach_lieCount")||"0")'
new_ach2 = '  creeperCount: parseInt(localStorage.getItem("ach_creeperCount")||"0"),\n  lieCount: parseInt(localStorage.getItem("ach_lieCount")||"0"),\n  fallCount: parseInt(localStorage.getItem("ach_fallCount")||"0")'
if old_ach2 in t:
    t = t.replace(old_ach2, new_ach2, 1)
    print("ach fall count")

# saveAch
old_save = '    localStorage.setItem("ach_creeper", JSON.stringify(achievements.creeper));\n    localStorage.setItem("ach_lie", JSON.stringify(achievements.lie));'
new_save = '    localStorage.setItem("ach_creeper", JSON.stringify(achievements.creeper));\n    localStorage.setItem("ach_lie", JSON.stringify(achievements.lie));\n    localStorage.setItem("ach_fall", JSON.stringify(achievements.fall));'
if old_save in t:
    t = t.replace(old_save, new_save, 1)
    print("save fall")

old_save2 = '    localStorage.setItem("ach_creeperCount", achievements.creeperCount);\n    localStorage.setItem("ach_lieCount", achievements.lieCount);'
new_save2 = '    localStorage.setItem("ach_creeperCount", achievements.creeperCount);\n    localStorage.setItem("ach_lieCount", achievements.lieCount);\n    localStorage.setItem("ach_fallCount", achievements.fallCount);'
if old_save2 in t:
    t = t.replace(old_save2, new_save2, 1)
    print("save fallCount")

# unlock
old_unlock = '  if(type==="creeper" && !achievements.creeper){ achievements.creeper=true; isNew=true; }\n  if(type==="lie" && !achievements.lie){ achievements.lie=true; isNew=true; }'
new_unlock = '  if(type==="creeper" && !achievements.creeper){ achievements.creeper=true; isNew=true; }\n  if(type==="lie" && !achievements.lie){ achievements.lie=true; isNew=true; }\n  if(type==="fall" && !achievements.fall){ achievements.fall=true; isNew=true; }'
if old_unlock in t:
    t = t.replace(old_unlock, new_unlock, 1)
    print("unlock fall")

old_unlock2 = '  if(type==="creeper") achievements.creeperCount++;\n  if(type==="lie") achievements.lieCount++;'
new_unlock2 = '  if(type==="creeper") achievements.creeperCount++;\n  if(type==="lie") achievements.lieCount++;\n  if(type==="fall") achievements.fallCount++;'
if old_unlock2 in t:
    t = t.replace(old_unlock2, new_unlock2, 1)
    print("unlock fall count")

old_names = '  const names={spin:"МАСТЕР ВРАЩЕНИЯ",salto:"САЛЬТО-МАСТЕР",hit:"МАСТЕР УДАРА",invis:"НЕВИДИМКА",crouch:"МАСТЕР СКРЫТНОСТИ",jump:"ДЖЕМП-МАСТЕР",creeper:"КРИПЕР",lie:"СОНЯ"};'
new_names = '  const names={spin:"МАСТЕР ВРАЩЕНИЯ",salto:"САЛЬТО-МАСТЕР",hit:"МАСТЕР УДАРА",invis:"НЕВИДИМКА",crouch:"МАСТЕР СКРЫТНОСТИ",jump:"ДЖЕМП-МАСТЕР",creeper:"КРИПЕР",lie:"СОНЯ",fall:"ПАДЕНИЕ"};'
if old_names in t:
    t = t.replace(old_names, new_names, 1)
    print("names fall")

# total 8 -> 9
old_total = '  const total=8;'
new_total = '  const total=9;'
if old_total in t:
    t = t.replace(old_total, new_total, 1)
    print("total 9")

old_done = '  const done=(achievements.spin?1:0)+(achievements.salto?1:0)+(achievements.hit?1:0)+(achievements.invis?1:0)+(achievements.crouch?1:0)+(achievements.jump?1:0)+(achievements.creeper?1:0)+(achievements.lie?1:0);'
new_done = '  const done=(achievements.spin?1:0)+(achievements.salto?1:0)+(achievements.hit?1:0)+(achievements.invis?1:0)+(achievements.crouch?1:0)+(achievements.jump?1:0)+(achievements.creeper?1:0)+(achievements.lie?1:0)+(achievements.fall?1:0);'
if old_done in t:
    t = t.replace(old_done, new_done, 1)
    print("done 9")

# Add book entry for fall after lie
old_entry = '  if(achievements.lie){\n    html += `<div class="book-entry done"><span class="icon">✔</span><span>ЛЕЧЬ — котик спит<br><small style="font-size:10px;color:#6B6B6B">лечь, ляг, лежать, улечься, отдохнуть, прилечь, ложись</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.lieCount} раз</small></span></div>`;\n  }'
new_entry = '''  if(achievements.lie){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>ЛЕЧЬ — лечь на землю<br><small style="font-size:10px;color:#6B6B6B">лечь, ляг, лежать, улечься, отдохнуть, прилечь, ложись</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.lieCount} раз</small></span></div>`;
  }
  if(achievements.fall){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>УПАЛ — падение<br><small style="font-size:10px;color:#6B6B6B">упал, упасть, падать, падение, свалился, грохнулся</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.fallCount} раз</small></span></div>`;
  }'''
if old_entry in t:
    t = t.replace(old_entry, new_entry, 1)
    print("book fall entry")

# Fix fallback init
if 'spin:false,salto:false,hit:false,invis:false,crouch:false,jump:false,creeper:false,lie:false' in t:
    t = t.replace(
        'achievements = {spin:false,salto:false,hit:false,invis:false,crouch:false,jump:false,creeper:false,lie:false,spinCount:0,saltoCount:0,hitCount:0,invisCount:0,crouchCount:0,jumpCount:0,creeperCount:0,lieCount:0};',
        'achievements = {spin:false,salto:false,hit:false,invis:false,crouch:false,jump:false,creeper:false,lie:false,fall:false,spinCount:0,saltoCount:0,hitCount:0,invisCount:0,crouchCount:0,jumpCount:0,creeperCount:0,lieCount:0,fallCount:0};'
    )
    print("fallback fall")

# Update handleCmd: add fall before hit to give priority to "упал" over "удар"
# Ensure fall is checked before hit to prevent "упал" matching hit via levenshtein
old_handle = '  if(matchesAliases(norm, spinAliases)){'
new_handle = '  if(matchesAliases(norm, fallAliases)){\n    lastCmdNorm=norm; lastCmdTime=now;\n    unlockAch("fall");\n    doFall();\n    input.value="";\n  } else if(matchesAliases(norm, spinAliases)){'
if old_handle in t:
    # Only replace first occurrence
    t = t.replace(old_handle, new_handle, 1)
    print("handle fall priority")

# Tighten hit matching to avoid "упал" -> "удар" false positive: increase levenshtein strictness for hit
# Already have guard, but we added fall before hit so fallen will be caught first

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

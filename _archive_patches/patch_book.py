import pathlib, shutil
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# 1. CSS - add book styles after .shake
css_add = """
  .book-btn{
    background:#8B4513;
    border:2px solid #000;
    border-top-color:#D2A679;
    border-left-color:#D2A679;
    border-right-color:#5C2E0C;
    border-bottom-color:#5C2E0C;
    color:#FFD700;
    font-family:"Press Start 2P", monospace;
    font-size:7px;
    padding:7px 10px;
    cursor:pointer;
    text-shadow:1px 1px 0 #000;
  }
  .book-btn:active{transform:translate(1px,1px); border-top-color:#5C2E0C; border-left-color:#5C2E0C; border-right-color:#D2A679; border-bottom-color:#D2A679;}
  .book-modal{
    position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
    width:360px;max-width:90vw;
    background:#F9E4B7;
    border:4px solid #5C2E0C;
    box-shadow: inset -4px -4px 0 #D2A679, inset 4px 4px 0 #FFF, 0 8px 24px rgba(0,0,0,0.6);
    padding:14px;
    display:none;z-index:30;
    image-rendering:pixelated;
  }
  .book-modal.open{display:block}
  .book-title{font-size:10px;color:#5C2E0C;text-align:center;margin-bottom:10px;text-shadow:1px 1px 0 #FFF}
  .book-pages{
    background:#FFFCF0;
    border:2px solid #8B8B8B;
    box-shadow: inset 2px 2px 0 #C6C6C6;
    padding:10px;
    min-height:160px;
  }
  .book-entry{
    display:flex;align-items:center;gap:8px;
    font-size:7px;color:#373737;
    padding:6px 4px;
    border-bottom:1px dashed #C6C6C6;
  }
  .book-entry.done{color:#1a7a1a}
  .book-entry .icon{width:18px;height:18px;display:flex;align-items:center;justify-content:center;background:#C6C6C6;border:1px solid #8B8B8B;flex-shrink:0;font-size:10px}
  .book-entry.done .icon{background:#7CFC00;border-color:#2d5a00}
  .book-close{
    margin-top:10px;width:100%;
    background:#C6C6C6;
    border:2px solid #000;
    border-top-color:#FFF; border-left-color:#FFF; border-right-color:#555; border-bottom-color:#555;
    font-family:"Press Start 2P",monospace;font-size:7px;padding:7px;cursor:pointer;
  }
  .book-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.5);display:none;z-index:29}
  .book-overlay.open{display:block}
"""

if ".book-btn{" not in t:
    t = t.replace(".shake{animation:shake 0.3s}", ".shake{animation:shake 0.3s}" + css_add)
    print("css added")
else:
    print("css exists")

# 2. HTML - add book button inside mc-bar and modal after toast
if 'id="bookBtn"' not in t:
    t = t.replace('<button id="cmdBtn" class="mc-btn">▶</button>', '<button id="cmdBtn" class="mc-btn">▶</button>\n  <button id="bookBtn" class="book-btn" title="Книга ачивок">📖 КНИГА</button>')
    print("bookBtn added")
else:
    print("bookBtn exists")

if 'id="bookModal"' not in t:
    modal = '''
<div id="bookOverlay" class="book-overlay"></div>
<div id="bookModal" class="book-modal">
  <div class="book-title">📖 КНИГА АЧИВОК</div>
  <div class="book-pages" id="bookPages">
    <!-- entries via JS -->
  </div>
  <div id="bookProgress" style="font-size:6px;color:#8B8B8B;text-align:center;margin-top:8px"></div>
  <button id="bookClose" class="book-close">ЗАКРЫТЬ</button>
</div>
'''
    t = t.replace('<div id="toast"></div>', '<div id="toast"></div>' + modal)
    print("modal added")
else:
    print("modal exists")

# 3. JS - inject achievement + anti-spam logic before handleCmd
# Find the line "const input=document.getElementById" and inject before it
js_inject = """
// === защита от повторов и книга ачивок ===
let lastCmdTime=0;
let lastCmdNorm="";
const COOLDOWN_MS=900;
const achievements = {
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
}
function renderBook(){
  const pages=document.getElementById("bookPages");
  const prog=document.getElementById("bookProgress");
  if(!pages) return;
  const total=2;
  const done=(achievements.spin?1:0)+(achievements.salto?1:0);
  pages.innerHTML = `
    <div class="book-entry ${achievements.spin?'done':''}"><span class="icon">${achievements.spin?'✔':'○'}</span><span>КРУТАНИСЬ — резкий 360°<br><small style="font-size:5px;color:#8B8B8B">команды: крутанись, крутись, крутнись, покрутись, вертанись, крутануть</small><br><small>выполнено: ${achievements.spinCount} раз</small></span></div>
    <div class="book-entry ${achievements.salto?'done':''}"><span class="icon">${achievements.salto?'✔':'○'}</span><span>САЛЬТО — кувырок 360° + прыжок<br><small style="font-size:5px;color:#8B8B8B">команды: сальто, сальтуха, кувырок, флип, переворот, сальтануть</small><br><small>выполнено: ${achievements.saltoCount} раз</small></span></div>
  `;
  if(prog) prog.textContent = `Прогресс: ${done}/${total} ачивок`;
}
function openBook(){ document.getElementById("bookModal").classList.add("open"); document.getElementById("bookOverlay").classList.add("open"); renderBook(); }
function closeBook(){ document.getElementById("bookModal").classList.remove("open"); document.getElementById("bookOverlay").classList.remove("open"); }
setTimeout(renderBook, 100);

"""

if "achievements.spin" not in t:
    t = t.replace('const input=document.getElementById("cmd");', js_inject + 'const input=document.getElementById("cmd");')
    print("js inject added")
else:
    print("js exists")

# Patch handleCmd to add anti-spam and unlock
# Replace handleCmd function body to include cooldown and unlockAch
old_handle = """function handleCmd(){
  const raw=input.value.trim();
  const norm=normalize(raw);
  if(!norm){
    bar.classList.remove("shake"); void bar.offsetWidth; bar.classList.add("shake");
    return;
  }
  if(matchesAliases(norm, spinAliases)){
    doSpin360();
    input.value="";
  } else if(matchesAliases(norm, saltoAliases)){
    doSomersault();
    input.value="";
  } else {
    bar.classList.remove("shake"); void bar.offsetWidth; bar.classList.add("shake");
    showToast("Неизвестная команда: "+raw, true);
  }
}"""

new_handle = """function handleCmd(){
  const raw=input.value.trim();
  const norm=normalize(raw);
  if(!norm){
    bar.classList.remove("shake"); void bar.offsetWidth; bar.classList.add("shake");
    return;
  }
  const now=Date.now();
  if(norm===lastCmdNorm && (now-lastCmdTime)<COOLDOWN_MS){
    bar.classList.remove("shake"); void bar.offsetWidth; bar.classList.add("shake");
    showToast("⏳ Защита от спама! Подожди", true);
    return;
  }
  if(spinning){
    showToast("⏳ Анимация идет...", true);
    return;
  }
  if(matchesAliases(norm, spinAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("spin");
    doSpin360();
    input.value="";
  } else if(matchesAliases(norm, saltoAliases)){
    lastCmdNorm=norm; lastCmdTime=now;
    unlockAch("salto");
    doSomersault();
    input.value="";
  } else {
    bar.classList.remove("shake"); void bar.offsetWidth; bar.classList.add("shake");
    showToast("Неизвестная команда: "+raw, true);
  }
}
document.getElementById("bookBtn").addEventListener("click", openBook);
document.getElementById("bookClose").addEventListener("click", closeBook);
document.getElementById("bookOverlay").addEventListener("click", closeBook);
document.addEventListener("keydown", e=>{ if(e.key==="Escape") closeBook(); });"""

if old_handle in t:
    t=t.replace(old_handle, new_handle)
    print("handleCmd patched")
else:
    print("old_handle not found")
    # debug
    if "function handleCmd" in t:
        idx=t.find("function handleCmd")
        print(repr(t[idx:idx+600]))

p.write_text(t, encoding="utf-8")
print("written local")
shutil.copy(r"C:\project\steve-minecraft-png\3d-local.html", r"C:\project\steve-minecraft-png\3d.html")
print("copied to 3d.html")

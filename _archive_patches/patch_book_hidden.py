import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

old = '''  const total=2;
  const done=(achievements.spin?1:0)+(achievements.salto?1:0);
  pages.innerHTML = `
    <div class="book-entry ${achievements.spin?'done':''}"><span class="icon">${achievements.spin?'✔':'○'}</span><span>КРУТАНИСЬ — резкий 360°<br><small style="font-size:10px;color:#6B6B6B">команды: крутанись, крутись, крутнись, покрутись, вертанись, крутануть</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.spinCount} раз</small></span></div>
    <div class="book-entry ${achievements.salto?'done':''}"><span class="icon">${achievements.salto?'✔':'○'}</span><span>САЛЬТО — кувырок 360° + прыжок<br><small style="font-size:10px;color:#6B6B6B">команды: сальто, сальтуха, кувырок, флип, переворот, сальтануть</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.saltoCount} раз</small></span></div>
  `;
  if(prog) prog.textContent = `Прогресс: ${done}/${total} ачивок`;'''

new = '''  const total=2;
  const done=(achievements.spin?1:0)+(achievements.salto?1:0);
  let html="";
  if(achievements.spin){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>КРУТАНИСЬ — резкий 360°<br><small style="font-size:10px;color:#6B6B6B">команды: крутанись, крутись, крутнись, покрутись, вертанись, крутануть</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.spinCount} раз</small></span></div>`;
  }
  if(achievements.salto){
    html += `<div class="book-entry done"><span class="icon">✔</span><span>САЛЬТО — кувырок 360° + прыжок<br><small style="font-size:10px;color:#6B6B6B">команды: сальто, сальтуха, кувырок, флип, переворот, сальтануть</small><br><small style="font-size:11px;color:#555">выполнено: ${achievements.saltoCount} раз</small></span></div>`;
  }
  if(html===""){
    html = `<div style="text-align:center;padding:20px;color:#8B8B8B;font-size:12px;line-height:1.6">📖 Пока пусто<br><small>Выполни команды, чтобы открыть ачивки</small></div>`;
  }
  pages.innerHTML = html;
  if(prog) prog.textContent = `${done}/${total} ачивок собрано` + (done===total && total>0 ? " — ВСЕ СОБРАНЫ! 🎉" : "");'''

if old in t:
    t = t.replace(old, new)
    print("patched book to hidden")
else:
    print("old not found")
    # debug
    import re
    m=re.search(r"const total=2;.*?Прогресс", t, re.DOTALL)
    if m:
        print(repr(m.group(0)[:500]))

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("copied")
# verify
d=open(r"C:\project\steve-minecraft-png\3d-local.html",encoding="utf-8").read()
print("hidden logic" , 'Пока пусто' in d)
print("ВСЕ СОБРАНЫ" in d)

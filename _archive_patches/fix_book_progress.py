import pathlib, shutil, re
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")

# 1. Update CSS for bookProgress - add mini shadows and better visibility
# Find the style block for book and add specific style for #bookProgress
old_progress_inline = '<div id="bookProgress" style="font-size:6px;color:#8B8B8B;text-align:center;margin-top:8px"></div>'
new_progress_inline = '<div id="bookProgress" style="font-size:11px;color:#5C2E0C;text-align:center;margin-top:10px;font-weight:700;text-shadow:1px 1px 0 #FFF, 0 1px 2px rgba(0,0,0,0.12);background:rgba(255,255,255,0.55);padding:6px 8px;border-radius:6px;border:1px solid rgba(92,46,12,0.12)"></div>'

if old_progress_inline in t:
    t = t.replace(old_progress_inline, new_progress_inline)
    print("updated inline style")
else:
    print("inline not found, searching")
    # try to find any bookProgress
    if 'id="bookProgress"' in t:
        t = re.sub(r'<div id="bookProgress"[^>]*></div>', new_progress_inline, t)
        print("replaced via regex")

# Also add CSS for when all done - make it more visible with mini shadows and highlight
css_add = """
  #bookProgress.all-done{
    background: linear-gradient(180deg, #7CFC00 0%, #55DD00 100%);
    color:#0f3a00;
    border:1.5px solid #2d5a00;
    text-shadow: 1px 1px 0 rgba(255,255,255,0.85), 0 1px 3px rgba(0,0,0,0.18);
    box-shadow: 0 2px 8px rgba(124,252,0,0.35), inset 0 1px 0 rgba(255,255,255,0.7);
    font-size:12px;
    letter-spacing:0.3px;
  }
"""

if "#bookProgress.all-done" not in t:
    t = t.replace(".book-overlay.open{display:block}", ".book-overlay.open{display:block}" + css_add)
    print("added all-done css")

# 2. Update JS to add class when all done and make text more visible
old_js = '  if(prog) prog.textContent = `${done}/${total} ачивок собрано` + (done===total && total>0 ? " — ВСЕ СОБРАНЫ! 🎉" : "");'
new_js = '''  if(prog){
    prog.textContent = `${done}/${total} ачивок собрано` + (done===total && total>0 ? " — ВСЕ СОБРАНЫ! 🎉" : "");
    if(done===total && total>0){
      prog.classList.add("all-done");
      prog.style.color="#0f3a00";
      prog.style.textShadow="1px 1px 0 rgba(255,255,255,0.9), 0 1px 4px rgba(0,0,0,0.25)";
    } else {
      prog.classList.remove("all-done");
      prog.style.color="#5C2E0C";
      prog.style.textShadow="1px 1px 0 #FFF, 0 1px 2px rgba(0,0,0,0.12)";
    }
  }'''

if old_js in t:
    t = t.replace(old_js, new_js)
    print("updated js for visibility")
else:
    print("js not found")
    # debug
    if "ачивок собрано" in t:
        idx = t.find("ачивок собрано")
        print(repr(t[idx-100:idx+200]))

p.write_text(t, encoding="utf-8")
shutil.copy(str(p), r"C:\project\steve-minecraft-png\3d.html")
print("written len", len(t))

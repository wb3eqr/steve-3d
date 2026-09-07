import pathlib
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")
t = t.replace('placeholder="крутанись"', 'placeholder="крутанись / сальто"')
t = t.replace('введи «крутанись»', 'введи «крутанись» или «сальто»')

old = """function doSpin360(){
  if(!steveGroup || spinning) return;
  spinning=true;
  const startY=steveGroup.rotation.y;
  const target=startY + Math.PI*2;
  const duration=750; // резкий но плавный
  const start=performance.now();
  function frame(now){
    const t=Math.min((now-start)/duration,1);
    // резкий старт, быстрое вращение: easeOutCubic
    const ease=1 - Math.pow(1-t,3);
    steveGroup.rotation.y = startY + (target-startY)*ease;
    if(t<1) requestAnimationFrame(frame);
    else { steveGroup.rotation.y = target % (Math.PI*2); spinning=false; showToast("КРУТАНУЛСЯ!"); }
  }
  requestAnimationFrame(frame);
}

// команды
const input=document.getElementById("cmd");
const btn=document.getElementById("cmdBtn");
const bar=document.getElementById("mcBar");

function handleCmd(){
  const raw=input.value.trim().toLowerCase();
  if(!raw){
    bar.classList.remove("shake"); void bar.offsetWidth; bar.classList.add("shake");
    return;
  }
  if(raw==="крутанись" || raw==="крутанись!" || raw.includes("крутанись")){
    doSpin360();
    input.value="";
  } else {
    bar.classList.remove("shake"); void bar.offsetWidth; bar.classList.add("shake");
    showToast("Неизвестная команда: "+raw, true);
  }
}"""

new = '''function doSpin360(){
  if(!steveGroup || spinning) return;
  spinning=true;
  const startY=steveGroup.rotation.y;
  const target=startY + Math.PI*2;
  const duration=650;
  const start=performance.now();
  function frame(now){
    const t=Math.min((now-start)/duration,1);
    const ease=1 - Math.pow(1-t,3);
    steveGroup.rotation.y = startY + (target-startY)*ease;
    if(t<1) requestAnimationFrame(frame);
    else { steveGroup.rotation.y = ((target % (Math.PI*2))+Math.PI*2)%(Math.PI*2); spinning=false; showToast("КРУТАНУЛСЯ!"); }
  }
  requestAnimationFrame(frame);
}

function doSomersault(){
  if(!steveGroup || spinning) return;
  spinning=true;
  const startX=steveGroup.rotation.x;
  const targetX=startX + Math.PI*2;
  const startY=steveGroup.position.y;
  const duration=750;
  const start=performance.now();
  function frame(now){
    const t=Math.min((now-start)/duration,1);
    const ease=1 - Math.pow(1-t,3);
    steveGroup.rotation.x = startX + (targetX-startX)*ease;
    steveGroup.position.y = startY + Math.sin(t*Math.PI)*5;
    if(t<1) requestAnimationFrame(frame);
    else { steveGroup.rotation.x = ((targetX % (Math.PI*2))+Math.PI*2)%(Math.PI*2); steveGroup.position.y=startY; spinning=false; showToast("САЛЬТО!"); }
  }
  requestAnimationFrame(frame);
}

// 6 версий крутанись + сальто — не надо точное сообщение
const spinAliases=["крутанись","крутись","крутнись","покрутись","вертанись","крутануть"];
const saltoAliases=["сальто","сальтуха","кувырок","флип","переворот","сальтануть"];

function normalize(s){
  return s.toLowerCase().trim().replace(/ё/g,"е").replace(/[!?.\\,]+/g,"").replace(/\\s+/g," ");
}
function levenshtein(a,b){
  const m=a.length,n=b.length;
  const dp=Array.from({length:m+1},()=>Array(n+1).fill(0));
  for(let i=0;i<=m;i++) dp[i][0]=i;
  for(let j=0;j<=n;j++) dp[0][j]=j;
  for(let i=1;i<=m;i++) for(let j=1;j<=n;j++){
    const cost=a[i-1]===b[j-1]?0:1;
    dp[i][j]=Math.min(dp[i-1][j]+1,dp[i][j-1]+1,dp[i-1][j-1]+cost);
  }
  return dp[m][n];
}
function matchesAliases(input, aliases){
  const norm=normalize(input);
  if(!norm) return false;
  for(const a of aliases){
    if(norm===a) return true;
    if(norm.includes(a)) return true;
    if(a.includes(norm) && norm.length>=4) return true;
    if(levenshtein(norm,a)<=2 && Math.abs(norm.length-a.length)<=2) return true;
    const a2=a.replace(/сь$/,""), n2=norm.replace(/сь$/,"");
    if(a2===n2) return true;
    if(levenshtein(n2,a2)<=1) return true;
  }
  return false;
}

// команды
const input=document.getElementById("cmd");
const btn=document.getElementById("cmdBtn");
const bar=document.getElementById("mcBar");

function handleCmd(){
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
}'''

if old in t:
    t=t.replace(old,new)
    print('patched ok')
else:
    print('old not found')
    # debug: find nearby
    import re
    m=re.search(r'function doSpin360.*?Неизвестная команда', t, re.DOTALL)
    if m:
        print(repr(m.group(0)[:300]))

p.write_text(t, encoding='utf-8')
print('written')

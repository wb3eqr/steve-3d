import pathlib, shutil
p = pathlib.Path(r"C:\project\steve-minecraft-png\3d-local.html")
t = p.read_text(encoding="utf-8-sig")
old = '    if(levenshtein(n2,a2)<=1) return true;'
new = '    if(n2.length>=5 && levenshtein(n2,a2)<=1) return true; // защита от "крут"'
if old in t:
    t=t.replace(old,new)
    print('patched levenshtein guard')
else:
    print('not found levenshtein line')
    for line in t.splitlines():
        if 'levenshtein(n2' in line:
            print(repr(line))
p.write_text(t, encoding="utf-8")
print('written')
shutil.copy(r"C:\project\steve-minecraft-png\3d-local.html", r"C:\project\steve-minecraft-png\3d.html")
print('copied')
# verify logic for "крут" should now be false
# Simulate matchesAliases for "крут"
def normalize(s):
    import re
    return s.lower().strip().replace("ё","е").replace("!","").replace("?","").replace(".","").replace(",","").strip()

def levenshtein(a,b):
    m=len(a);n=len(b)
    dp=[[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0]=i
    for j in range(n+1): dp[0][j]=j
    for i in range(1,m+1):
        for j in range(1,n+1):
            cost=0 if a[i-1]==b[j-1] else 1
            dp[i][j]=min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
    return dp[m][n]

spinAliases=["крутанись","крутись","крутнись","покрутись","вертанись","крутануть"]
def matches(norm, aliases):
    for a in aliases:
        if norm==a: return True
        if norm in a or a in norm: # simplified check without the removed condition
            # we removed a.includes(norm) check, so only norm.includes(a)
            if norm.find(a)!=-1: return True
        if levenshtein(norm,a)<=2 and abs(len(norm)-len(a))<=2: return True
        a2=a[:-2] if a.endswith("сь") else a
        n2=norm[:-2] if norm.endswith("сь") else norm
        if a2==n2: return True
        if len(n2)>=5 and levenshtein(n2,a2)<=1: return True
    return False

for test in ["крут","крутись","крутанись","крутануть","покрутись","к"]:
    print(test, matches(normalize(test), spinAliases))

import json, base64, re, pathlib
p = pathlib.Path(r"C:\project\steve-minecraft-png\steve_profile.json")
d = p.read_text(encoding="utf-8")
print(d[:2000])
m = re.search(r'"value"\s*:\s*"([^"]+)"', d)
if m:
    val = m.group(1)
    print("val len", len(val))
    dec = base64.b64decode(val).decode("utf-8")
    print(dec[:2000])
    obj = json.loads(dec)
    print(obj.get("textures"))
    # download skin url
    tex = obj["textures"]["SKIN"]["url"]
    print("skin url", tex)
    import urllib.request
    urllib.request.urlretrieve(tex, r"C:\project\steve-minecraft-png\steve-classic-mojang.png")
    print("downloaded mojang skin")
else:
    print("no value found")

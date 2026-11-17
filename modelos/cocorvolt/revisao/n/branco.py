"""Render BRANCO (sem textura, só a forma) do modelo: 3/4, frente e lado. Uso: branco.py <bbmodel> <saida.png>"""
import sys, json, base64, io, tempfile, os
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import numpy as np, previa2
from PIL import Image
bb = json.load(open(sys.argv[1], encoding="utf-8"))
t = bb["textures"][0]
src = Image.open(io.BytesIO(base64.b64decode(t["source"].split(",", 1)[1]))).convert("RGBA")
a = np.asarray(src).copy(); a[..., :3] = 215
buf = io.BytesIO(); Image.fromarray(a).save(buf, format="PNG")
t["source"] = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
tmp = os.path.join(tempfile.gettempdir(), "cocorvolt_branco.bbmodel")
json.dump(bb, open(tmp, "w", encoding="utf-8"))
q = previa2.carregar(tmp)
ims = [previa2.desenhar(q, y, p, escala=14, fundo=(40, 44, 54)) for y, p in ((35, -10), (0, -4), (90, -4), (160, -10))]
W = sum(i.width for i in ims); H = max(i.height for i in ims)
f = Image.new("RGB", (W, H), (40, 44, 54)); x = 0
for i in ims: f.paste(i, (x, 0)); x += i.width
f.save(sys.argv[2]); print(f.size)

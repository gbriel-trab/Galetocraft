"""Lado a lado: arte conceitual x modelo no mesmo enquadramento e na mesma altura total.
Uso: python arte_lado.py <prefixo> [yaw] [pitch]  -> grava revisao/<prefixo>_arte_lado.png"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R.parents[1] / "ferramentas"))
import previa2

pref = sys.argv[1]
yaw = float(sys.argv[2]) if len(sys.argv) > 2 else -55
pitch = float(sys.argv[3]) if len(sys.argv) > 3 else -8
arte = Image.open(R.parents[0] / "referencias" / "008_axococo_arte.png").convert("RGB")
# recorte da criatura na arte (topo da crista ~y62, pés ~y825; cauda à esquerda, bico à direita)
ca = arte.crop((0, 55, 840, 830))
bb = R / "revisao" / f"{pref}.bbmodel"
q = previa2.carregar(str(bb if bb.exists() else R / "axococo.bbmodel"))
FUNDO = (255, 0, 255)
im = previa2.desenhar(q, yaw, pitch, escala=16, fundo=FUNDO, margem=4)
a = np.asarray(im).astype(int); m = np.abs(a - np.array(FUNDO)).sum(-1) > 60
ys, xs = np.nonzero(m)
im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
H = ca.height
k = H / im.height
im = im.resize((int(im.width * k), H), Image.LANCZOS)
mk = Image.fromarray((m * 255).astype(np.uint8)).resize(im.size, Image.NEAREST)
fundo = Image.new("RGB", im.size, (20, 16, 18)); fundo.paste(im, (0, 0), mk)
W = ca.width + fundo.width + 20
o = Image.new("RGB", (W, H + 24), (20, 16, 18))
o.paste(ca, (0, 24)); o.paste(fundo, (ca.width + 20, 24))
ImageDraw.Draw(o).text((6, 4), f"arte  x  modelo {pref} (yaw {yaw}, pitch {pitch}), mesma altura", fill=(240, 240, 240))
o.save(R / "revisao" / f"{pref}_arte_lado.png")
print(R / "revisao" / f"{pref}_arte_lado.png")

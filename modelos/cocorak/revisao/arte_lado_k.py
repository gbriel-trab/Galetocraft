"""Rodadas k* do Cocórak: arte conceitual x modelo no mesmo ângulo e na mesma altura, e render branco sem textura.
Uso: python arte_lado_s.py <prefixo> [yaw] [pitch]
Grava revisao/<prefixo>_arte_lado.png (arte | modelo | modelo branco) e revisao/<prefixo>_branco.png
(frente, lado direito, trás, lado esquerdo e 3/4, tudo branco)."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R.parents[1] / "ferramentas"))
import previa2

pref = sys.argv[1]
yaw = float(sys.argv[2]) if len(sys.argv) > 2 else 40
pitch = float(sys.argv[3]) if len(sys.argv) > 3 else -8
FUNDO = (255, 0, 255)
ESC = (20, 16, 18)

bb = R / "revisao" / f"{pref}.bbmodel"
faces, tex = previa2.carregar(str(bb if bb.exists() else R / "cocorak.bbmodel"))
branco = tex.copy(); branco[..., :3] = np.where(branco[..., 3:4] > 0, 236.0, 0.0)


def recorte(dados, y, p, escala=16):
    im = previa2.desenhar(dados, y, p, escala=escala, fundo=FUNDO, margem=4)
    a = np.asarray(im).astype(int); m = np.abs(a - np.array(FUNDO)).sum(-1) > 60
    ys, xs = np.nonzero(m)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return im, m


def na_altura(im, m, H, fundo=ESC):
    k = H / im.height
    im = im.resize((max(1, int(im.width * k)), H), Image.LANCZOS)
    mk = Image.fromarray((m * 255).astype(np.uint8)).resize(im.size, Image.NEAREST)
    f = Image.new("RGB", im.size, fundo); f.paste(im, (0, 0), mk)
    return f


arte = Image.open(R.parents[0] / "referencias" / "004_cocorak_arte.png").convert("RGB")
ca = arte.crop((0, 0, arte.width, 1018))                 # topo da crista ~y0, chão ~y1015
H = ca.height
a1 = na_altura(*recorte((faces, tex), yaw, pitch), H)
a2 = na_altura(*recorte((faces, branco), yaw, pitch), H, fundo=(40, 44, 52))
o = Image.new("RGB", (ca.width + a1.width + a2.width + 40, H + 24), ESC)
o.paste(ca, (0, 24)); o.paste(a1, (ca.width + 20, 24)); o.paste(a2, (ca.width + a1.width + 40, 24))
ImageDraw.Draw(o).text((6, 4), f"arte  x  modelo {pref} (yaw {yaw}, pitch {pitch}), mesma altura  x  sem textura",
                       fill=(240, 240, 240))
o.save(R / "revisao" / f"{pref}_arte_lado.png")

ims = [na_altura(*recorte((faces, branco), y, p, escala=10), 420, fundo=(40, 44, 52))
       for y, p in ((0, -6), (90, -5), (180, -6), (-90, -5), (35, -10))]
W = sum(i.width for i in ims) + 20 * len(ims)
f = Image.new("RGB", (W, 440), (40, 44, 52)); x = 10
for i in ims: f.paste(i, (x, 10)); x += i.width + 20
f.save(R / "revisao" / f"{pref}_branco.png")
print(R / "revisao" / f"{pref}_arte_lado.png")

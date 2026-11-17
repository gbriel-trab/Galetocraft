"""Lado a lado: arte conceitual × modelo no ângulo da arte, na mesma altura total. Uso: arte_lado.py <bbmodel> <saida> [yaw] [pitch]"""
import sys
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import numpy as np, previa2
from PIL import Image, ImageDraw
bb, saida = sys.argv[1], sys.argv[2]
yaw = float(sys.argv[3]) if len(sys.argv) > 3 else 50
pitch = float(sys.argv[4]) if len(sys.argv) > 4 else -6
arte = Image.open(r"C:\Users\gbriel\Desktop\galopiru\modelos\referencias\006_cocorvolt_arte.png").convert("RGB")
A0, A1 = 66, 960                          # topo do chapéu e sola dos pés na arte (medidos)
arte = arte.crop((0, A0 - 10, arte.width, A1 + 10))
q = previa2.carregar(bb)
im = previa2.desenhar(q, yaw, pitch, escala=16, fundo=(255, 0, 255), ss=1, margem=4)
a = np.asarray(im).astype(int); m = np.abs(a - np.array([255, 0, 255])).sum(-1) > 60
ys, xs = np.nonzero(m)
im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
k = (A1 - A0) / im.height
im = im.resize((int(im.width * k), A1 - A0), Image.LANCZOS)
mm = np.asarray(im).astype(int); fundo = np.abs(mm - np.array([255, 0, 255])).sum(-1) < 120
mm[fundo] = (30, 34, 44); im = Image.fromarray(mm.astype(np.uint8))
out = Image.new("RGB", (arte.width + im.width + 20, arte.height), (30, 34, 44))
out.paste(arte, (0, 0)); out.paste(im, (arte.width + 20, 10))
d = ImageDraw.Draw(out)
for f in np.arange(0, 1.01, 0.1):
    y = 10 + int(f * (A1 - A0)); d.line([(0, y), (out.width, y)], fill=(0, 255, 255)); d.text((2, y + 1), f"{f:.1f}", fill=(255, 255, 0))
out.save(saida); print(out.size, "px por unidade de altura:", (A1 - A0))

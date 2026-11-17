"""Arte x modelo lado a lado, mesma altura, com linhas a cada 10% da altura. uso: arte_lado.py prefixo yaw pitch"""
import sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import previa2
R = r"C:\Users\gbriel\Desktop\galopiru\modelos"
pref, yaw, pitch = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
arte = Image.open(R + r"\referencias\012_salambrasa_arte.png").convert("RGB").crop((30, 55, 860, 845))   # criatura
q = previa2.carregar(R + r"\salambrasa\salambrasa.bbmodel")
m = previa2.desenhar(q, yaw, pitch, escala=14, fundo=(20, 14, 18), margem=2)
a = np.asarray(m).astype(int); msk = np.abs(a - np.array([20, 14, 18])).sum(-1) > 30
ys, xs = np.nonzero(msk); m = m.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
H = 760
arte = arte.resize((round(arte.width * H / arte.height), H)); m = m.resize((round(m.width * H / m.height), H))
im = Image.new("RGB", (arte.width + m.width + 20, H), (20, 14, 18)); im.paste(arte, (0, 0)); im.paste(m, (arte.width + 20, 0))
d = ImageDraw.Draw(im)
for k in range(1, 10):
    y = round(H * k / 10); d.line([(0, y), (im.width, y)], fill=(0, 200, 255), width=1); d.text((2, y - 12), f"{k*10}%", fill=(0, 255, 255))
for x in range(0, im.width, round(H / 10)):
    d.line([(x, 0), (x, 6)], fill=(0, 200, 255))
im.save(R + rf"\salambrasa\revisao\{pref}_arte_lado.png")
print(arte.size, m.size)

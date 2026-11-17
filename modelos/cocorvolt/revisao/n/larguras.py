"""Larguras de FRENTE (fração da altura total) da ficha e do modelo em alturas relativas; e imagem lado a lado
(ficha frente | modelo frente | arte). Uso: larguras.py <bbmodel> <saida.png>"""
import sys
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import numpy as np, previa2
from PIL import Image, ImageDraw
import comparar_ficha as cf
folha = Image.open(r"C:\Users\gbriel\Desktop\galopiru\modelos\referencias\006_cocorvolt_vistas.png").convert("RGB")
# coluna da frente em coordenadas da imagem: ápice y=103, pés y=447
col = folha.crop((25, 77, 325, 535)); m = cf.mascara_ficha(col)
TOPO, PES = 103 - 77, 447 - 77
H = PES - TOPO
def larg_ficha(f):
    y = int(TOPO + f * H); xs = np.nonzero(m[y])[0]
    return (xs.max() - xs.min()) / H if len(xs) else 0
q = previa2.carregar(sys.argv[1])
im = previa2.desenhar(q, 0, 0, escala=12, fundo=(255, 0, 255), ss=1, margem=4)
a = np.asarray(im).astype(int); mm = np.abs(a - np.array([255, 0, 255])).sum(-1) > 60
ys, xs = np.nonzero(mm); mm = mm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]; Hm = mm.shape[0]
def larg_mod(f, x_lim=None):
    y = int(f * Hm); row = np.nonzero(mm[y])[0]
    return (row.max() - row.min()) / Hm if len(row) else 0
# faixas: cabeça (sob a aba, sem talismãs: medido pelo miolo central), pescoço, peito
print("f      ficha   modelo")
for f in (0.24, 0.27, 0.30, 0.33, 0.36, 0.39, 0.42, 0.46, 0.50, 0.55, 0.60, 0.70):
    print(f"{f:.2f}   {larg_ficha(f):.3f}   {larg_mod(f):.3f}")
# imagem
fic = col.crop((0, TOPO - 5, col.width, PES + 5)).resize((int(col.width * 600 / (H + 10)), 600), Image.LANCZOS)
mod = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)); mod = mod.resize((int(mod.width * 590 / mod.height), 590), Image.LANCZOS)
ma = np.asarray(mod).astype(int); ma[np.abs(ma - np.array([255, 0, 255])).sum(-1) < 120] = (14, 20, 16); mod = Image.fromarray(ma.astype(np.uint8))
arte = Image.open(r"C:\Users\gbriel\Desktop\galopiru\modelos\referencias\006_cocorvolt_arte.png").convert("RGB").crop((0, 56, 749, 970))
arte = arte.resize((int(arte.width * 600 / arte.height), 600), Image.LANCZOS)
out = Image.new("RGB", (fic.width + mod.width + arte.width + 40, 600), (14, 20, 16))
out.paste(fic, (0, 0)); out.paste(mod, (fic.width + 20, 5)); out.paste(arte, (fic.width + mod.width + 40, 0))
d = ImageDraw.Draw(out)
for f in np.arange(0, 1.01, 0.1): d.line([(0, 5 + int(f * 590)), (fic.width + mod.width + 20, 5 + int(f * 590))], fill=(0, 160, 160))
out.save(sys.argv[2])

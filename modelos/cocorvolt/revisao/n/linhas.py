"""Compara, por faixa de altura, a extensão horizontal (em unidades, altura total = 39) da ficha e do modelo."""
import sys
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import numpy as np
from PIL import Image
import comparar_ficha as cf, previa2
bb = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\gbriel\Desktop\galopiru\modelos\cocorvolt\cocorvolt.bbmodel"
folha = Image.open(r"C:\Users\gbriel\Desktop\galopiru\modelos\referencias\006_cocorvolt_vistas.png").convert("RGB")
FW, FH = folha.size
corpo = folha.crop((int(FW*0.02), int(FH*0.14), int(FW*0.98), int(FH*0.97)))
CW, CH = corpo.size
q = previa2.carregar(bb)
for i,(nome,yaw) in enumerate(cf.VISTAS):
    if i == 3: break
    col = corpo.crop((i*CW//4, 0, (i+1)*CW//4, CH))
    mr = cf.recortar(cf.mascara_ficha(col))
    img = previa2.desenhar(q, yaw, 0, escala=10, fundo=cf.MAGENTA, ss=1, margem=4)
    mm = cf.recortar(np.abs(np.asarray(img).astype(int) - np.array(cf.MAGENTA)).sum(-1) > 60)
    altf = 32.0 if i == 0 else 39.0   # a frente da ficha vai do chapéu até a barra da saia
    print(nome)
    # referência horizontal: o ápice do chapéu (linha de cima)
    def ext(m, alt, y):
        H = m.shape[0]; s = H / alt
        r = int((alt - y) * s) if alt == 39.0 else int((39 - y) * s)
        if r < 0 or r >= H: return None
        apice = np.nonzero(m[min(2, H-1)])[0].mean()
        xs = np.nonzero(m[r])[0]
        if not len(xs): return None
        return ((xs.min() - apice) / s, (xs.max() - apice) / s)
    for y in range(38, 0, -2):
        a = ext(mr, altf, y); b = ext(mm, 39.0, y)
        fa = f"{a[0]:6.1f}..{a[1]:5.1f}" if a else " " * 13
        fb = f"{b[0]:6.1f}..{b[1]:5.1f}" if b else ""
        print(f"  y={y:2d}  ficha {fa}   modelo {fb}")

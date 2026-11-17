"""Diagnóstico de cor: por região (faixas de altura x 3 colunas), cor média da ficha e do modelo onde os dois cobrem."""
import sys
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import numpy as np
from PIL import Image
import comparar_ficha as cf, previa2
bb = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\gbriel\Desktop\galopiru\modelos\cocorvolt\cocorvolt.bbmodel"
vistas = [int(v) for v in sys.argv[2].split(",")] if len(sys.argv) > 2 else [0, 1, 2, 3]
folha = Image.open(r"C:\Users\gbriel\Desktop\galopiru\modelos\referencias\006_cocorvolt_vistas.png").convert("RGB")
FW, FH = folha.size
corpo = folha.crop((int(FW*0.02), int(FH*0.14), int(FW*0.98), int(FH*0.97))); CW, CH = corpo.size
q = previa2.carregar(bb)
for i in vistas:
    nome, yaw = cf.VISTAS[i]
    col = corpo.crop((i*CW//4, 0, (i+1)*CW//4, CH))
    mr = cf.mascara_ficha(col)
    img_m = previa2.desenhar(q, yaw, 0, escala=10, fundo=cf.MAGENTA, ss=1, margem=4)
    mm_ = np.abs(np.asarray(img_m).astype(int) - np.array(cf.MAGENTA)).sum(-1) > 60
    a = cf.normalizar(mr); b = cf.normalizar(mm_)
    iou, A, B = cf.iou_alinhado(a, b)
    ys, xs = np.nonzero(mr); cr = col.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1)).resize((a.shape[1], cf.ALT), Image.LANCZOS)
    H, W = A.shape
    base = Image.new("RGB", (W, H), (14, 10, 12)); base.paste(cr, ((W - a.shape[1]) // 2, 0)); b0 = np.asarray(base)
    ys, xs = np.nonzero(mm_)
    mc = np.asarray(img_m.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1)).resize((b.shape[1], cf.ALT), Image.LANCZOS)).copy()
    b2 = np.full((H, W, 3), (14, 10, 12), np.uint8); bx = int(np.nonzero(B.any(0))[0].min()); b2[:, bx:bx+b.shape[1]] = mc
    nota, _ = cf.comparar_cores(b0, b2, A, B)
    print(f"{nome}: cor {nota*100:.0f}%")
    both = A & B
    cols = np.nonzero(both.any(0))[0]; x0, x1 = cols.min(), cols.max()
    for k in range(12):
        y0, y1 = k * H // 12, (k + 1) * H // 12
        linha = []
        for c in range(3):
            xa, xb = x0 + c * (x1 - x0) // 3, x0 + (c + 1) * (x1 - x0) // 3
            m = both[y0:y1, xa:xb]
            if m.sum() < 30: linha.append(" " * 27); continue
            f = b0[y0:y1, xa:xb][m].mean(0).astype(int); md = b2[y0:y1, xa:xb][m].mean(0).astype(int)
            linha.append(f"{tuple(f)!s:>13}/{tuple(md)!s:<13}")
        print(f"  {39 - 39 * k / 12:4.1f}u " + " | ".join(linha))

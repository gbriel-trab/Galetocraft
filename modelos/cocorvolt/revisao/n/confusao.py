"""Pares de cor (ficha -> modelo) que mais tiram nota, por vista, com a posição média (altura em u, coluna)."""
import sys
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import numpy as np
from PIL import Image
import comparar_ficha as cf, previa2
from collections import defaultdict
NOMES = {(30,30,34):"preto",(64,62,68):"carvao",(100,92,90):"cinza",(140,130,128):"cinza+",(185,175,172):"claro",
         (40,70,135):"marinho",(235,165,20):"laranja",(235,195,95):"ouro",(170,125,70):"palha-esc",(225,190,130):"palha",
         (150,70,40):"verm",(245,240,200):"brilho",(60,100,200):"azul-olho"}
cls = np.array(list(NOMES.keys()), float); nomes = list(NOMES.values())
def nome(c): return nomes[int(((cls - c) ** 2).sum(1).argmin())]
bb = sys.argv[1]
folha = Image.open(r"C:\Users\gbriel\Desktop\galopiru\modelos\referencias\006_cocorvolt_vistas.png").convert("RGB")
FW, FH = folha.size
corpo = folha.crop((int(FW*0.02), int(FH*0.14), int(FW*0.98), int(FH*0.97))); CW, CH = corpo.size
q = previa2.carregar(bb)
pesos = np.array([0.30, 0.59, 0.11]) * 3
for i, (nv, yaw) in enumerate(cf.VISTAS):
    col = corpo.crop((i*CW//4, 0, (i+1)*CW//4, CH)); mr = cf.mascara_ficha(col)
    img_m = previa2.desenhar(q, yaw, 0, escala=10, fundo=cf.MAGENTA, ss=1, margem=4)
    mm_ = np.abs(np.asarray(img_m).astype(int) - np.array(cf.MAGENTA)).sum(-1) > 60
    a = cf.normalizar(mr); b = cf.normalizar(mm_); iou, A, B = cf.iou_alinhado(a, b)
    ys, xs = np.nonzero(mr); cr = col.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1)).resize((a.shape[1], cf.ALT), Image.LANCZOS)
    H, W = A.shape; base = Image.new("RGB", (W, H), (14, 10, 12)); base.paste(cr, ((W - a.shape[1]) // 2, 0)); b0 = np.asarray(base)
    ys, xs = np.nonzero(mm_)
    mc = np.asarray(img_m.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1)).resize((b.shape[1], cf.ALT), Image.LANCZOS)).copy()
    b2 = np.full((H, W, 3), (14, 10, 12), np.uint8); bx = int(np.nonzero(B.any(0))[0].min()); b2[:, bx:bx+b.shape[1]] = mc
    perda = defaultdict(lambda: [0.0, 0, 0.0, 0.0]); tot = 0
    for y in range(0, H - 7, 8):
        for x in range(0, W - 7, 8):
            m = A[y:y+8, x:x+8] & B[y:y+8, x:x+8]
            if m.mean() < 0.6: continue
            c1 = b0[y:y+8, x:x+8][m].astype(float).mean(0); c2 = b2[y:y+8, x:x+8][m].astype(float).mean(0)
            d = float(np.sqrt((((c1 - c2) ** 2) * pesos).sum())); n = max(0.0, 1 - d / 140); tot += 1
            k = (nome(c1), nome(c2)); e = perda[k]; e[0] += 1 - n; e[1] += 1; e[2] += 39 * (1 - y / H); e[3] += x / W
    print(f"{nv}: {tot} celulas")
    for k, (p, n, yy, xx) in sorted(perda.items(), key=lambda kv: -kv[1][0])[:9]:
        print(f"   ficha {k[0]:9s} -> modelo {k[1]:9s} perda {p/tot*100:4.1f} pts  ({n} cel, y~{yy/n:4.1f}u, x~{xx/n:.2f})")

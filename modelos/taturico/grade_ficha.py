"""Lê o desenho da carapaça nas 4 vistas da ficha e grava `grade_ficha.json`, que `taturico.py` usa para pintar as
faces dos anéis no MESMO lugar da ficha (largura e ordem das faixas, xadrez da lateral).

Usa o mesmo enquadramento de `comparar_ficha.py`: a criatura da ficha e o modelo ficam com a mesma altura, os pés
alinhados e o deslocamento horizontal de melhor sobreposição. Cada célula de 1 x 1 unidade do modelo recebe a classe
de cor mais próxima da cor média da ficha naquela célula: C caramelo, M marrom, E marrom-escuro, P sombra,
R vermelho, Y amarelo, W creme, G cinza (garras); '.' = fora da ficha.

Uso: python modelos/taturico/grade_ficha.py [modelo.bbmodel]   (padrão: modelos/taturico/taturico.bbmodel)"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(RAIZ / "ferramentas"))
import comparar_ficha as cf, previa2

PAL = {"C": (235, 160, 100), "M": (160, 88, 60), "E": (105, 48, 30), "P": (50, 17, 7),
       "R": (205, 35, 32), "Y": (238, 150, 12), "W": (246, 200, 150), "G": (120, 92, 100)}
PESO = np.array([.3, .59, .11])

def classe(c):
    return min(PAL, key=lambda k: float((((np.array(PAL[k]) - c) ** 2) * PESO).sum()))

def limpar(g):
    """Tira células soltas: uma célula cujos 4 vizinhos concordam numa outra classe vira essa classe."""
    g = [list(l) for l in g]; H, W = len(g), len(g[0])
    out = [l[:] for l in g]
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            v = {g[y - 1][x], g[y + 1][x], g[y][x - 1], g[y][x + 1]}
            if len(v) == 1 and "." not in v and g[y][x] not in v and g[y][x] != ".": out[y][x] = v.pop()
    return ["".join(l) for l in out]

def main(bb):
    folha = Image.open(next((RAIZ / "modelos" / "referencias").glob("*_taturico_vistas.png"))).convert("RGB")
    FW, FH = folha.size
    corpo = folha.crop((int(FW * .02), int(FH * .14), int(FW * .98), int(FH * .97)))
    CW, CH = corpo.size
    q = previa2.carregar(str(bb))
    faces, _ = q
    pts = np.array([c for cantos, _, _ in faces for c in cantos]
                   + [list(np.array(c[1]) + np.array(c[2]) - np.array(c[0])) for c, _, _ in faces])
    (xmin, ymin, zmin), (xmax, ymax, zmax) = pts.min(0), pts.max(0)
    out = {}
    for i, (nome, yaw) in enumerate(cf.VISTAS):
        col = corpo.crop((i * CW // 4, 0, (i + 1) * CW // 4, CH))
        mr = cf.mascara_ficha(col)
        img_m = previa2.desenhar(q, yaw, 0, escala=10, fundo=cf.MAGENTA, ss=1, margem=4)
        mm = np.abs(np.asarray(img_m).astype(int) - np.array(cf.MAGENTA)).sum(-1) > 60
        a, b = cf.normalizar(mr), cf.normalizar(mm)
        _, A, B = cf.iou_alinhado(a, b)
        ys, xs = np.nonzero(mr)
        cr = col.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)).resize((a.shape[1], cf.ALT), Image.LANCZOS)
        H, W = A.shape
        base = Image.new("RGB", (W, H), (14, 10, 12)); base.paste(cr, ((W - a.shape[1]) // 2, 0))
        ref = np.asarray(base).astype(float)
        cols = np.nonzero(B.any(0))[0]; rows = np.nonzero(B.any(1))[0]
        bx0, bx1, by0, by1 = cols.min(), cols.max(), rows.min(), rows.max()
        lo, hi = (zmin, zmax) if i in (1, 3) else (xmin, xmax)
        # yaw 0: +x à esquerda; 90: frente (z-) à direita; 180: +x à direita; -90: frente à esquerda
        sentido = {0: -1, 1: -1, 2: 1, 3: 1}[i]
        def col_de(h):
            f = (h - lo) / (hi - lo)
            return bx0 + (f if sentido > 0 else 1 - f) * (bx1 - bx0)
        def lin_de(y): return by0 + (ymax - y) / (ymax - ymin) * (by1 - by0)
        h0 = float(np.floor(lo) + 0.5)
        grade = []
        for y in np.arange(39.5, -0.5, -1.0):
            lin = ""
            for h in np.arange(h0, hi, 1.0):
                c0, c1 = sorted((col_de(h - .5), col_de(h + .5))); r0, r1 = sorted((lin_de(y + .5), lin_de(y - .5)))
                c0, c1, r0, r1 = (int(round(v)) for v in (c0, c1, r0, r1))
                m = A[r0:r1 + 1, c0:c1 + 1]
                if m.size == 0 or m.mean() < 0.5: lin += "."; continue
                lin += classe(ref[r0:r1 + 1, c0:c1 + 1][m].mean(0))
            grade.append(lin)
        out[{0: "north", 1: "east", 2: "south", 3: "west"}[i]] = {"h0": h0, "y0": 39.5, "linhas": limpar(grade)}
    destino = AQUI / "grade_ficha.json"
    destino.write_text(json.dumps(out, indent=0), encoding="utf-8")
    print("grade gravada em", destino)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else RAIZ / "modelos" / "taturico" / "taturico.bbmodel")

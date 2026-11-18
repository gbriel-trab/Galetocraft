"""Recorta a figura de uma arte com fundo liso (preto, branco ou de outra cor) e grava um PNG com fundo transparente,
pronto para o comparar_arte.py. Precisa de scipy (`pip install scipy`).

O fundo são as cores que dominam a borda da imagem (ou --fundo R,G,B); tudo o que for dessas cores e encostar na
borda some. Sobram as manchas grandes, com os
buracos preenchidos. Logos, textos e molduras dentro da imagem: apague com --apagar x0,y0,x1,y1 (pode repetir).

Uso: python recortar_arte.py ENTRADA.png SAIDA.png [--apagar x0,y0,x1,y1 ...] [--tolerancia 40] [--minimo 400]
"""
import argparse

import numpy as np
from PIL import Image
from scipy import ndimage


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("entrada"); ap.add_argument("saida")
    ap.add_argument("--apagar", action="append", default=[], help="retângulo x0,y0,x1,y1 a ignorar (logo, texto)")
    ap.add_argument("--tolerancia", type=float, default=40, help="distância de cor até o fundo")
    ap.add_argument("--minimo", type=int, default=400, help="área mínima (px) de uma mancha para ficar")
    ap.add_argument("--fundo", action="append", default=[], help="cor de fundo R,G,B (pode repetir); sem isso, vem da borda")
    a = ap.parse_args()
    img = np.asarray(Image.open(a.entrada).convert("RGB")).astype(int)
    h, w = img.shape[:2]
    if a.fundo:
        fundos = [np.array([int(v) for v in f.split(",")]) for f in a.fundo]
    else:   # cores que ocupam ao menos 15% da borda da imagem (ex.: margem branca + fundo preto)
        borda_px = np.concatenate([img[0], img[-1], img[:, 0], img[:, -1]])
        q = (borda_px // 16) * 16 + 8
        cores, cont = np.unique(q, axis=0, return_counts=True)
        fundos = [cores[i] for i in np.argsort(-cont) if cont[i] >= 0.15 * len(q)] or [cores[np.argmax(cont)]]
    perto = np.zeros((h, w), bool)
    for f in fundos:
        perto |= np.abs(img - f).sum(-1) < a.tolerancia
    lab, _ = ndimage.label(perto)
    borda = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fig = ~np.isin(lab, list(borda))
    for r in a.apagar:
        x0, y0, x1, y1 = (int(v) for v in r.split(","))
        fig[y0:y1, x0:x1] = False
    fig = ndimage.binary_opening(fig, iterations=1)          # tira linhas finas de moldura
    lab, n = ndimage.label(ndimage.binary_closing(fig, iterations=2))
    tam = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    fica = np.isin(lab, [i + 1 for i, t in enumerate(tam) if t >= a.minimo])
    fica = ndimage.binary_fill_holes(fica)
    rgba = np.zeros((h, w, 4), np.uint8); rgba[..., :3] = img; rgba[..., 3] = fica * 255
    ys, xs = np.where(fica)
    Image.fromarray(rgba).crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)).save(a.saida)
    print(f"fundos {[tuple(int(v) for v in f) for f in fundos]}; figura {xs.max() - xs.min() + 1}x{ys.max() - ys.min() + 1} px -> {a.saida}")


if __name__ == "__main__":
    main()

"""Como as cores da arte viraram a paleta da textura: compara região por região (por matiz) e mostra as rampas.

Para cada cor dominante da arte (sem fundo e sem o contorno escuro), procura os pixels da textura com matiz parecido
e compara as medianas em matiz/saturação/brilho (H/S/V). Depois lista as rampas da textura (tons agrupados por
matiz, do escuro ao claro) com os passos de H, S e V entre tons vizinhos: é daí que saiu a regra de rampa_da_arte().

Uso: python cores_por_regiao.py ARTE.png TEXTURA.png [--cores 8] [--tolerancia 14]
"""
import argparse, colorsys, sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comparar_arte import cores_dominantes  # noqa: E402


def hsv(rgb):
    h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in rgb))
    return h * 360, s, v


def dif_h(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("arte"); ap.add_argument("textura")
    ap.add_argument("--cores", type=int, default=8)
    ap.add_argument("--tolerancia", type=float, default=14, help="diferença máxima de matiz (graus) para casar")
    a = ap.parse_args()
    tex = np.asarray(Image.open(a.textura).convert("RGBA"))
    px = tex[tex[..., 3] > 0][:, :3]
    th = np.array([hsv(p) for p in px])
    print(f"{'cor da arte':>18}  {'área':>5}  {'arte H/S/V':>16}  {'textura (mediana)':>18}  {'textura H/S/V':>16}  S x  V dif")
    dh = np.array([[dif_h(h0, x) for x in th[:, 0]] for h0 in range(360)])
    for cor, frac in cores_dominantes(Image.open(a.arte), n=a.cores):
        h, s, v = hsv(cor)
        # nota de cada pixel da textura: matiz parecido, saturação ~1,35x a da arte, brilho parecido (regra medida)
        nota = (dh[int(h) % 360] / a.tolerancia
                + np.abs(np.log((th[:, 1] + 0.03) / (s * 1.35 + 0.03))) / np.log(2)
                + np.abs(th[:, 2] - v) / 0.4)
        corte = max(np.percentile(nota, 12), np.sort(nota)[min(4, len(nota) - 1)])
        m = nota <= corte
        if nota[m].mean() > 2.5:
            print(f"{str(cor):>18}  {100 * frac:4.1f}%  {h:4.0f}/{s:.2f}/{v:.2f}   (sem região parecida na textura)")
            continue
        med = tuple(int(x) for x in np.median(px[m], 0)); h2, s2, v2 = hsv(med)
        print(f"{str(cor):>18}  {100 * frac:4.1f}%  {h:4.0f}/{s:.2f}/{v:.2f}  {str(med):>18}  {h2:4.0f}/{s2:.2f}/{v2:.2f}"
              f"  {s2 / max(s, 1e-3):.2f} {v2 - v:+.2f}")
    # rampas da textura: cores agrupadas por matiz (faixas de 24°), ordenadas por brilho
    cores = sorted({tuple(int(c) for c in p) for p in px}, key=lambda c: hsv(c)[2])
    grupos = {}
    for c in cores:
        h, s, v = hsv(c)
        faixa = "neutro" if s < 0.12 else "pastel" if s < 0.45 else "vivo"
        chave = faixa if faixa == "neutro" else f"{int(((h + 12) % 360) // 24) * 24}° {faixa}"
        grupos.setdefault(chave, []).append(c)
    print("\nrampas da textura (escuro -> claro), H/S/V por tom e o passo médio entre tons:")
    for chave, r in sorted(grupos.items(), key=lambda kv: -len(kv[1])):
        if len(r) < 3: continue
        hs = [hsv(c) for c in r]
        passos = [(dif_h(b[0], a_[0]) * (1 if (b[0] - a_[0]) % 360 < 180 else -1), b[1] - a_[1], b[2] - a_[2])
                  for a_, b in zip(hs, hs[1:])]
        mh, ms, mv = (float(np.mean([p[i] for p in passos])) for i in range(3))
        print(f"  {str(chave):>11}: " + " · ".join(f"{h:.0f}/{s:.2f}/{v:.2f}" for h, s, v in hs)
              + f"   passo: H {mh:+.1f}°, S {ms:+.3f}, V {mv:+.3f}")


if __name__ == "__main__":
    main()

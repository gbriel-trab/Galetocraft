"""Largura do trecho CENTRAL contínuo (sem talismãs) na vista de frente, em fração da altura total."""
import sys
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import numpy as np, previa2
for bb in sys.argv[1:]:
    q = previa2.carregar(bb)
    im = previa2.desenhar(q, 0, 0, escala=12, fundo=(255, 0, 255), ss=1, margem=4)
    a = np.asarray(im).astype(int); m = np.abs(a - np.array([255, 0, 255])).sum(-1) > 60
    ys, xs = np.nonzero(m); m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]; H, W = m.shape
    cx = W // 2
    def run(f):
        row = m[int(f * H)]; l = r = cx
        while l > 0 and row[l - 1]: l -= 1
        while r < W - 1 and row[r + 1]: r += 1
        return (r - l + 1) / H
    print(bb.split("\\")[-1], " ".join(f"{f:.2f}:{run(f):.3f}" for f in (0.22, 0.25, 0.28, 0.31, 0.34, 0.37, 0.42, 0.48)))

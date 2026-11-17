import sys
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import numpy as np
from PIL import Image
import comparar_ficha as cf
folha = Image.open(r"C:\Users\gbriel\Desktop\galopiru\modelos\referencias\006_cocorvolt_vistas.png").convert("RGB")
FW, FH = folha.size
corpo = folha.crop((int(FW*0.02), int(FH*0.14), int(FW*0.98), int(FH*0.97))); CW, CH = corpo.size
px = []
for i in range(4):
    col = corpo.crop((i*CW//4, 0, (i+1)*CW//4, CH)); m = cf.mascara_ficha(col)
    px.append(np.asarray(col)[m])
X = np.concatenate(px).astype(float)
rng = np.random.default_rng(1); C = X[rng.choice(len(X), 16, replace=False)]
for _ in range(30):
    d = ((X[:, None, :] - C[None]) ** 2).sum(-1); l = d.argmin(1)
    C = np.array([X[l == k].mean(0) if (l == k).any() else C[k] for k in range(len(C))])
cnt = np.bincount(l, minlength=len(C))
for k in np.argsort(-cnt): print(tuple(int(v) for v in C[k]), f"{cnt[k]/len(X)*100:.1f}%")
import previa2
q = previa2.carregar(sys.argv[1])
px = []
for nome, yaw in cf.VISTAS:
    img = previa2.desenhar(q, yaw, 0, escala=10, fundo=cf.MAGENTA, ss=1, margem=4)
    a = np.asarray(img).astype(int); m = np.abs(a - np.array(cf.MAGENTA)).sum(-1) > 60
    px.append(a[m])
Y = np.concatenate(px).astype(float)
d = ((Y[:, None, :] - C[None]) ** 2).sum(-1); l2 = d.argmin(1); cnt2 = np.bincount(l2, minlength=len(C))
print("modelo, nas mesmas classes:")
for k in np.argsort(-cnt): print(tuple(int(v) for v in C[k]), f"ficha {cnt[k]/len(X)*100:.1f}%  modelo {cnt2[k]/len(Y)*100:.1f}%  media modelo {tuple(int(v) for v in Y[l2==k].mean(0)) if cnt2[k] else '-'}")

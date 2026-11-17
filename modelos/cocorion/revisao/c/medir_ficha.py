import sys
sys.path.insert(0, "ferramentas")
import numpy as np
from PIL import Image
import comparar_ficha as cf
folha = Image.open("modelos/referencias/005_cocorion_vistas.png").convert("RGB")
FW, FH = folha.size
corpo = folha.crop((int(FW * 0.02), int(FH * 0.14), int(FW * 0.98), int(FH * 0.97)))
CW, CH = corpo.size
for i, (nome, yaw) in enumerate(cf.VISTAS):
    col = corpo.crop((i * CW // 4, 0, (i + 1) * CW // 4, CH))
    m = cf.recortar(cf.mascara_ficha(col))
    h, w = m.shape
    print(nome, "h", h, "w", w, "w/h %.2f" % (w / h))
    for f in np.arange(0, 1.0, 0.05):
        r = m[int(f * (h - 1))]
        xs = np.nonzero(r)[0]
        if len(xs): print("  %.2f  x %.2f..%.2f  (larg %.2f)" % (1 - f, xs.min() / h, xs.max() / h, (xs.max() - xs.min()) / h))

"""Acha as manchas amarelas nas vistas da ficha e converte para unidades do modelo."""
import sys
import numpy as np
from PIL import Image
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import comparar_ficha as cf
a = np.asarray(Image.open(r"C:\Users\gbriel\Desktop\galopiru\modelos\referencias\012_salambrasa_vistas.png").convert("RGB")).astype(int)
def manchas(x0, x1, y0=60, y1=420):
    s = a[y0:y1, x0:x1]
    m = (s[..., 0] > 225) & (s[..., 1] > 150) & (s[..., 2] < 110)
    rot, tam = cf.componentes(m)
    out = []
    for n in range(1, len(tam)):
        if tam[n] < 12: continue
        ys, xs = np.nonzero(rot == n)
        out.append((xs.mean() + x0, ys.mean() + y0, xs.max() - xs.min() + 1, ys.max() - ys.min() + 1, tam[n]))
    return out
# escala: pés y=400 (px orig) -> 0; altura 303 px = 39.4 u
def conv_y(py): return (400 - py) * 39.4 / 303
K = 39.4 / 303
print("LATERAL DIREITA (z = 27.8 - (px-422)*K)")
for x, y, w, h, t in sorted(manchas(420, 860)):
    print(f"  z={27.8 - (x - 422) * K:6.1f} y={conv_y(y):5.1f}  larg={w*K:4.1f} alt={h*K:4.1f}")
print("TRASEIRA (x = (px-1085)*K)")
for x, y, w, h, t in sorted(manchas(990, 1180)):
    print(f"  x={(x - 1085) * K:6.1f} y={conv_y(y):5.1f}  larg={w*K:4.1f} alt={h*K:4.1f}")
print("FRENTE")
for x, y, w, h, t in sorted(manchas(120, 330)):
    print(f"  x={(x - 225) * K:6.1f} y={conv_y(y):5.1f}  larg={w*K:4.1f} alt={h*K:4.1f}")

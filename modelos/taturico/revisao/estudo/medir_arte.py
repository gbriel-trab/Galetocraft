"""Mede, no modelo renderizado no ângulo da arte (yaw 66, pitch -10), frações da altura total."""
import sys, numpy as np
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "ferramentas"))
import previa2
from PIL import Image
for rod in sys.argv[1:]:
    q = previa2.carregar(str(RAIZ / "modelos/taturico/revisao" / f"{rod}.bbmodel"))
    a = np.asarray(previa2.desenhar(q, 66, -10, escala=20, fundo=(255, 0, 255), margem=4)).astype(int)
    m = np.abs(a - [255, 0, 255]).sum(-1) > 60
    ys, xs = np.nonzero(m); H = ys.max() - ys.min(); y0 = ys.min(); x0 = xs.min()
    r, gg, b = a[..., 0], a[..., 1], a[..., 2]
    verm = m & (r > 150) & (gg < 90) & (b < 90)
    amar = m & (r > 150) & (gg > 100) & (b < 60)
    def ext(mm, eixo):
        idx = np.nonzero(mm.any(1 - eixo))[0]
        return (idx.max() - idx.min()) / H if len(idx) else 0
    vy = np.nonzero(verm.any(1))[0]
    pernas = amar & (np.arange(a.shape[0])[:, None] > y0 + 0.6 * H)
    py = np.nonzero(pernas.any(1))[0]
    bico = amar & (np.arange(a.shape[0])[:, None] < y0 + 0.6 * H)
    bx = np.nonzero(bico.any(0))[0]
    print(rod, "largura %.2f | crista alt %.2f larg %.2f | pernas alt %.2f | bico compr %.2f" % (
        (xs.max() - xs.min()) / H, (vy.max() - vy.min()) / H * 0 + ext(verm & (np.arange(a.shape[0])[:, None] < y0 + 0.35 * H), 0),
        ext(verm & (np.arange(a.shape[0])[:, None] < y0 + 0.35 * H), 1), (py.max() - py.min()) / H, (bx.max() - bx.min()) / H))

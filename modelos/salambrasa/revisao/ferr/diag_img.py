"""Imagem grande de uma vista: ficha | modelo | mapa de cor, para achar onde a cor erra."""
import sys
import numpy as np
from PIL import Image
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import comparar_ficha as cf
cap = []
orig = cf.comparar_cores
def espiao(ref, mod, A, B):
    r = orig(ref, mod, A, B); cap.append((ref.copy(), mod.copy(), r[1])); return r
cf.comparar_cores = espiao
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    cf.comparar("salambrasa", None, "diag")
v = int(sys.argv[1])
ref, mod, mapa = cap[v]
H, W = ref.shape[:2]
out = np.concatenate([ref, mod, mapa], 0)
Image.fromarray(out.astype(np.uint8)).resize((W * 2, H * 6), Image.NEAREST).save(sys.argv[2])

"""Diagnóstico de cor: por categoria de cor da ficha (célula 8 px), cor média da ficha x do modelo e nota."""
import sys, colorsys
import numpy as np
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import comparar_ficha as cf
cap = []
orig = cf.comparar_cores
def espiao(ref, mod, A, B):
    cap.append((ref.copy(), mod.copy(), A.copy(), B.copy())); return orig(ref, mod, A, B)
cf.comparar_cores = espiao
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    cf.comparar("salambrasa", sys.argv[1] if len(sys.argv) > 1 else None, "diag")
def cat(c):
    r, g, b = c / 255; h, l, s = colorsys.rgb_to_hls(r, g, b)
    if l < 0.22: return "escuro"
    if s < 0.25: return "cinza"
    h *= 360
    if h < 12 or h > 330: return "vermelho"
    if h < 30: return "laranja"
    if h < 60: return "amarelo"
    return "roxo"
P = np.array([0.30, 0.59, 0.11]) * 3
nomes = ["Frente", "LatD", "Tras", "LatE"]
for (ref, mod, A, B), nm in zip(cap, nomes):
    H, W = A.shape; S = {}
    for y in range(0, H - 7, 8):
        for x in range(0, W - 7, 8):
            amb = A[y:y+8, x:x+8] & B[y:y+8, x:x+8]
            if amb.mean() < 0.6: continue
            cr = ref[y:y+8, x:x+8][amb].astype(float).mean(0); cm = mod[y:y+8, x:x+8][amb].astype(float).mean(0)
            n = max(0, 1 - np.sqrt((((cr - cm) ** 2) * P).sum()) / 140)
            S.setdefault(cat(cr), []).append((cr, cm, n))
    print(nm)
    for k, v in sorted(S.items(), key=lambda kv: -len(kv[1])):
        cr = np.mean([a for a, _, _ in v], 0).astype(int); cm = np.mean([b for _, b, _ in v], 0).astype(int)
        print(f"  {k:9s} n={len(v):4d} ficha={tuple(cr)} modelo={tuple(cm)} nota={np.mean([c for _, _, c in v])*100:.0f}%")
print("CONFUSAO (ficha -> modelo: n celulas, perda total)")
for (ref, mod, A, B), nm in zip(cap, nomes):
    H, W = A.shape; C = {}
    for y in range(0, H - 7, 8):
        for x in range(0, W - 7, 8):
            amb = A[y:y+8, x:x+8] & B[y:y+8, x:x+8]
            if amb.mean() < 0.6: continue
            cr = ref[y:y+8, x:x+8][amb].astype(float).mean(0); cm = mod[y:y+8, x:x+8][amb].astype(float).mean(0)
            n = max(0, 1 - np.sqrt((((cr - cm) ** 2) * P).sum()) / 140)
            k = (cat(cr), cat(cm)); C.setdefault(k, [0, 0.0]); C[k][0] += 1; C[k][1] += 1 - n
    print(nm, "  ".join(f"{a}->{b}:{v[0]}/{v[1]:.0f}" for (a, b), v in sorted(C.items(), key=lambda kv: -kv[1][1])[:8]))

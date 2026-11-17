"""Folga entre a brânquia de baixo e a asa (mesmo lado), medida nos vértices do modelo atual."""
import json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R.parents[1] / "ferramentas"))
import previa2
m = json.loads((R / "axococo.bbmodel").read_text(encoding="utf-8"))
tmp = R / "revisao" / "tmp_folga.bbmodel"
def pontos(pref):
    m2 = dict(m); m2["elements"] = [e for e in m["elements"] if e["name"].startswith(pref)]
    tmp.write_text(json.dumps(m2), encoding="utf-8")
    f, _ = previa2.carregar(str(tmp))
    return [c for ff in f for c in ff[0]]
g = pontos("guelra_e_2"); a = pontos("asa"); a = [p for p in a if p[0] > 0]
import numpy as np
A = np.array(a); folga = 99
for xg, yg, zg in g:
    perto = A[(np.abs(A[:, 0] - xg) < 1.2) & (np.abs(A[:, 2] - zg) < 1.5)]
    if len(perto): folga = min(folga, yg - perto[:, 1].max())
print(f"folga mínima entre a brânquia de baixo e a asa logo embaixo dela: {folga:.2f} (negativo = encosta/atravessa)")
tmp.unlink()

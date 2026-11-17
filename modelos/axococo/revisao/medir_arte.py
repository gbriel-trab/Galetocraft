"""Mede partes do modelo no enquadramento da arte (yaw/pitch dados), como fração da altura total do modelo.
Uso: python medir_arte.py <rodada> [yaw] [pitch]"""
import json, sys
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R.parents[1] / "ferramentas"))
import previa2

pref = sys.argv[1]; yaw = float(sys.argv[2]) if len(sys.argv) > 2 else 40; pitch = float(sys.argv[3]) if len(sys.argv) > 3 else 0
m = json.loads((R / "revisao" / f"{pref}.bbmodel").read_text(encoding="utf-8"))
tmp = R / "revisao" / "tmp_medir.bbmodel"

def caixa_2d(filtro):
    m2 = dict(m); m2["elements"] = [e for e in m["elements"] if filtro(e["name"])]
    tmp.write_text(json.dumps(m2), encoding="utf-8")
    q = previa2.carregar(str(tmp))
    # projeção ortográfica igual à do previa2 (yaw em y, depois pitch em x)
    a, b = np.radians(yaw), np.radians(pitch)
    Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
    V = Rx @ Ry
    P = np.array([V @ np.array(c) for f in q[0] for c in f[0]] + [V @ (np.array(f[0][1]) + np.array(f[0][2]) - np.array(f[0][0])) for f in q[0]])
    return P[:, 0].min(), P[:, 0].max(), P[:, 1].min(), P[:, 1].max()

tudo = caixa_2d(lambda n: True)
H = tudo[3] - tudo[2]
partes = {
    "tronco (corpo+peito+asa da camera)": lambda n: n.startswith(("tronco", "rabadilha", "peito")) or (n.startswith("asa") and "_e" in n),
    "asa (a do lado da camera)": lambda n: n.startswith("asa") and "_e" in n,
    "cabeca (sem crista/branquias/bico)": lambda n: n.startswith(("queixo", "cranio", "testa")),
    "crista": lambda n: n.startswith("crista"),
    "branquias": lambda n: n.startswith("guelra"),
    "cauda": lambda n: n.startswith("cauda"),
    "pernas (amarelo)": lambda n: n.startswith("perna"),
    "pes+dedos": lambda n: n.startswith(("pe_", "dedo")),
}
print(f"{pref} yaw {yaw} pitch {pitch}: altura total = {H:.2f} un")
for nome, f in partes.items():
    x0, x1, y0, y1 = caixa_2d(f)
    print(f"  {nome:36s} larg {100 * (x1 - x0) / H:5.1f}%  alt {100 * (y1 - y0) / H:5.1f}%  topo {100 * (tudo[3] - y1) / H:5.1f}%  base {100 * (tudo[3] - y0) / H:5.1f}%")
tmp.unlink()

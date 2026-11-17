"""Dimensões oficiais dos Cocorídeos (tabela do dono, 2026-11-11), em blocos (1 bloco = 1 metro).

altura = do chão à ponta mais alta; largura = eixo x (de lado a lado, com asas); comprimento = eixo z (do bico
à ponta da cauda). O exportador escala cada modelo para a ALTURA daqui; largura e comprimento são as proporções que
o modelo deve ter.

Uso: python dimensoes.py [id ...]  -> mede os modelos atuais (modelos/<id>/<id>.bbmodel) e compara com a tabela.
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent

#            id            (altura, largura, comprimento)
DIMENSOES = {
    "pirococo":   (2.80, 2.00, 2.90),   # #001 mítico
    "cocorrego":  (2.10, 2.45, 2.60),   # #002 mítico (ainda não modelado)
    "esporoco":   (1.75, 1.55, 2.15),   # #003 mítico
    "cocorak":    (3.00, 2.75, 3.00),   # #004 mítico
    "cocorion":   (2.40, 1.50, 2.70),   # #005 mítico
    "cocorvolt":  (2.60, 2.35, 2.55),   # #006 mítico
    "taturico":   (1.20, 1.25, 1.50),   # #007 comum
    "axococo":    (1.15, 1.20, 1.55),   # #008 comum
    "vagalo":     (1.00, 1.10, 1.30),   # #009 comum
    "morcegalo":  (1.20, 1.30, 1.50),   # #010 comum
    "espinhoco":  (1.25, 1.30, 1.55),   # #011 comum
    "salambrasa": (1.10, 1.00, 1.80),   # #012 comum
    "renacoco": (2.50, 1.60, 2.60),     # #019 mítico (PROVISÓRIO: fora da tabela oficial; abaixo do Cocórak, alto e esguio)
}


def medir(modelo):
    """(altura, largura, comprimento) em unidades da parte visível do modelo (ignora texels transparentes)."""
    sys.path.insert(0, str(AQUI))
    import numpy as np, previa2
    faces, tex = previa2.carregar(str(modelo))
    H, W = tex.shape[:2]; pts = []
    grade = np.linspace(0.02, 0.98, 10)
    for (c0, c1, c2), (u1, v1, u2, v2), _ in faces:
        c0, c1, c2 = map(np.array, (c0, c1, c2))
        for a in grade:
            for b in grade:
                u = u1 + (u2 - u1) * a; v = v1 + (v2 - v1) * b
                if tex[min(int(v), H - 1), min(int(u), W - 1), 3] > 0:
                    pts.append(c0 + (c1 - c0) * a + (c2 - c0) * b)
    p = np.array(pts)
    alt = p[:, 1].max() - min(p[:, 1].min(), 0.0)
    return alt, p[:, 0].max() - p[:, 0].min(), p[:, 2].max() - p[:, 2].min()


def relatorio(id_, modelo=None):
    modelo = Path(modelo) if modelo else RAIZ / "modelos" / id_ / f"{id_}.bbmodel"
    A, L, C = DIMENSOES[id_]
    a, l, c = medir(modelo)
    k = A * 16 / a
    lb, cb = l * k / 16, c * k / 16
    print(f"{id_}: escalado para altura {A:.2f} -> largura {lb:.2f} (alvo {L:.2f}, {100 * lb / L - 100:+.0f}%), "
          f"comprimento {cb:.2f} (alvo {C:.2f}, {100 * cb / C - 100:+.0f}%)")
    return lb / L, cb / C


if __name__ == "__main__":
    for id_ in (sys.argv[1:] or [i for i in DIMENSOES if (RAIZ / "modelos" / i / f"{i}.bbmodel").exists()]):
        relatorio(id_)

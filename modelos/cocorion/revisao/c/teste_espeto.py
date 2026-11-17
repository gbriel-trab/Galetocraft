"""Protótipo: 3 formas de espeto lado a lado (debug)."""
import sys, math
sys.path.insert(0, "ferramentas"); sys.path.insert(0, "ferramentas/especies")
import galo_base as g, previa2
import cocorion as C
from galo_base import peca, osso
from PIL import Image

def cunha(nome, raiz, d, L, W, T, fora):
    x, y, z = raiz
    m = C.mat_luz(C.cor_fixa(C.BRANCO))
    s1 = W / 1.4142; w2 = W * 0.5; s2 = w2 / 1.4142
    yb = y + L - W / 2 - w2 * 0.5
    pcs = [peca(nome + "_0", [x - W / 2, y - 1.0, z - T / 2], [x + W / 2, yb, z + T / 2], m),
           peca(nome + "_1", [x - s1 / 2, yb - s1 / 2, z - T / 2 + .04], [x + s1 / 2, yb + s1 / 2, z + T / 2 - .04], m, rot=(0, 0, 45), pivo=(x, yb, z)),
           peca(nome + "_2", [x - s2 / 2, yb + W * 0.3 - s2 / 2, z - T * 0.35], [x + s2 / 2, yb + W * 0.3 + s2 / 2, z + T * 0.35], m, rot=(0, 0, 45), pivo=(x, yb + W * 0.3, z))]
    return osso(nome, list(raiz), C.apontar(d), [osso(nome + "_t", list(raiz), [0, C.torcao_para(d, fora), 0], pcs)])

def xis(nome, raiz, d, L, W, T, fora):
    x, y, z = raiz
    m = C.mat_luz(C.cor_fixa(C.BRANCO))
    pcs = []
    for k, gira in enumerate((0, 90)):
        s1 = W / 1.4142
        yb = y + L - W / 2
        pp = [peca(f"{nome}_{k}a", [x - W / 2, y - 1.0, z - T / 2], [x + W / 2, yb, z + T / 2], m),
              peca(f"{nome}_{k}b", [x - s1 / 2, yb - s1 / 2, z - T / 2 + .04], [x + s1 / 2, yb + s1 / 2, z + T / 2 - .04], m, rot=(0, 0, 45), pivo=(x, yb, z))]
        pcs.append(osso(f"{nome}_g{k}", list(raiz), [0, gira, 0], pp))
    return osso(nome, list(raiz), C.apontar(d), [osso(nome + "_t", list(raiz), [0, C.torcao_para(d, fora), 0], pcs)])

def montar():
    C.TRANSF.clear()
    filhos = []
    for i, f in enumerate((lambda n, r: C.espeto(n, r, (0, 1, 0.8), 8, 3.6),
                           lambda n, r: cunha(n, r, (0, 1, 0.8), 8, 4.2, 2.4, (1, 0, 0)),
                           lambda n, r: xis(n, r, (0, 1, 0.8), 8, 4.2, 1.4, (1, 0, 0)))):
        filhos.append(f(f"e{i}", (i * 12.0, 0, 0)))
    raiz = [osso("r", [0, 0, 0], [0, 0, 0], filhos)]
    C.preparar_transformacoes(raiz)
    return raiz

g.reiniciar()
out = montar()
cam = g.gerar("teste", "modelos/cocorion/revisao/c/_t", out)
q = previa2.carregar(str(cam))
ims = [previa2.desenhar(q, y, p, escala=12) for y, p in ((0, -6), (90, -5), (35, -10))]
W = sum(i.width for i in ims); H = max(i.height for i in ims)
f = Image.new("RGB", (W, H)); x = 0
for i in ims: f.paste(i, (x, 0)); x += i.width
f.save("modelos/cocorion/revisao/c/teste_espeto.png")

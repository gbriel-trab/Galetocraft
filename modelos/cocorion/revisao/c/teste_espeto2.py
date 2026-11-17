"""Protótipo de pontas da juba (debug)."""
import sys, math
sys.path.insert(0, "ferramentas"); sys.path.insert(0, "ferramentas/especies")
import galo_base as g, previa2
import cocorion as C
from galo_base import peca, osso
from PIL import Image

def degraus(nome, raiz, d, L, W, T, fora):
    x, y, z = raiz
    m = C.mat_luz(C.cor_juba(x, None))
    ws = (W, W * 0.68, W * 0.38); ts = (T, T * 0.9, T * 0.8)
    cortes = (0.0, 0.36, 0.62, 0.84)
    pcs = []
    for k in range(3):
        w, t = ws[k], ts[k]
        pcs.append(peca(f"{nome}_{k}", [x - w / 2, y + L * cortes[k] - (1.2 if k == 0 else 0.15), z - t / 2],
                        [x + w / 2, y + L * cortes[k + 1], z + t / 2], m))
    s = ws[2] / 1.4142; yp = y + L - ws[2] / 2
    pcs.append(peca(f"{nome}_3", [x - s / 2, yp - s / 2, z - ts[2] / 2 + .04], [x + s / 2, yp + s / 2, z + ts[2] / 2 - .04], m,
                    rot=(0, 0, 45), pivo=(x, yp, z)))
    return osso(nome, list(raiz), C.apontar(d), [osso(nome + "_t", list(raiz), [0, C.torcao_para(d, fora), 0], pcs)])

def triang(nome, raiz, d, L, W, T, fora):
    """Duas réguas inclinadas (as bordas do triângulo) + base + ponta."""
    x, y, z = raiz
    B = W / 2; beta = math.atan(B / L); D = math.hypot(B, L)
    w = B * math.cos(beta) * 1.05
    t = w * math.cos(2 * beta) / math.sin(2 * beta)
    claro = C.mat_luz(C.cor_fixa(C.CLARO)); base = C.mat_luz(C.cor_fixa(C.mix(C.BRANCO, C.SOMBRA_B, .45)))
    pcs = []
    for lado, m in ((-1, claro), (1, base)):
        x0 = x + lado * B
        xa, xb = sorted((x0, x0 - lado * w))
        pcs.append(peca(f"{nome}_r{lado}", [xa, y - 1.0, z - T / 2 + (0.03 if lado > 0 else 0)], [xb, y + D - t, z + T / 2 - (0.03 if lado > 0 else 0)], m,
                        rot=(0, 0, math.degrees(beta) * lado), pivo=(x0, y, z)))
    # ponta: losango estreito que fecha o alto do triângulo
    yt = y + L - t * math.cos(beta)
    hw = (L - (yt - y)) * math.tan(beta)
    s = hw * 2 / 1.4142
    pcs.append(peca(f"{nome}_p", [x - s / 2, y + L - hw - s / 2 * 1.4142 / 2 * 0 - s / 2, z - T * 0.4], [x + s / 2, y + L - hw + s / 2, z + T * 0.4], claro,
                    rot=(0, 0, 45), pivo=(x, y + L - hw, z)))
    return osso(nome, list(raiz), C.apontar(d), [osso(nome + "_t", list(raiz), [0, C.torcao_para(d, fora), 0], pcs)])

def montar():
    C.TRANSF.clear()
    filhos = []
    for i, f in enumerate((lambda n, r: C.pena_juba(n, r, (0, 1, 0.6), 8, 4.2, 1.7, (1, 0, 0)),
                           lambda n, r: degraus(n, r, (0, 1, 0.6), 8, 4.2, 1.7, (1, 0, 0)),
                           lambda n, r: triang(n, r, (0, 1, 0.6), 8, 4.6, 1.7, (1, 0, 0)))):
        filhos.append(f(f"e{i}", (0, 0, i * 9.0)))
    raiz = [osso("r", [0, 0, 0], [0, 0, 0], filhos)]
    C.preparar_transformacoes(raiz)
    return raiz

g.reiniciar()
out = montar()
cam = g.gerar("teste", "modelos/cocorion/revisao/c/_t", out)
q = previa2.carregar(str(cam))
ims = [previa2.desenhar(q, y, p, escala=14) for y, p in ((90, -5), (55, -10), (0, -6))]
W = sum(i.width for i in ims); H = max(i.height for i in ims)
f = Image.new("RGB", (W, H)); x = 0
for i in ims: f.paste(i, (x, 0)); x += i.width
f.save("modelos/cocorion/revisao/c/teste_espeto2.png")

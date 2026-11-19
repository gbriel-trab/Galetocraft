"""Blockout de referência do Pirococó (ficha anime) na técnica do Cobblemon: massa SÓLIDA + franja de planos.

Não é o modelo final: é o alvo de silhueta e de construção que acompanha o prompt de modelagem.

- Volumes grandes em caixas sólidas: tronco, peito, asas-capa em 3 placas grossas por lado (como as asas fechadas do
  Talonflame e do Braviary), juba em blocos, ombreiras em concha.
- Planos só na franja: pontas das penas da capa, chamas da crista, lâminas da cauda, esporas.
- Pintura simples (luz de cima, sombra embaixo, telhas pintadas na capa); 1 px por unidade, UV de caixa nos sólidos,
  UV por face com UMA face nos planos.

Uso: python blockout_pirococo.py [pasta_de_saida] [ficha.png]
     (no repositório, sem argumentos: grava em modelos/pirococo/blockout/ e compara com a ficha anime).
     Precisa do render_geo.py na mesma pasta.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
import render_geo as rg

SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "modelos" / "pirococo" / "blockout"
FICHA = Path(sys.argv[2]) if len(sys.argv) > 2 else RAIZ / "modelos" / "referencias" / "001_pirococo_anime_ficha.png"
ID = "pirococo"


def hexc(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


# rampas: luz, claro, base, sombra, funda
RAMPA = {
    "verm": ["#ff5b3f", "#ef392d", "#dd1c20", "#b90c27", "#960429"],
    "creme": ["#fff6e0", "#ffeed1", "#fde1c0", "#d9b398", "#b68b78"],
    "roxo": ["#a0499e", "#88398e", "#702a7c", "#491847", "#300e34"],
    "roxoesc": ["#5b2354", "#491847", "#3a1239", "#2c0c2e", "#210826"],
    "prata": ["#f6f6f6", "#e4dce3", "#d2bed1", "#ac93ae", "#86708b"],
    "ouro": ["#ffe138", "#ffcd29", "#fcb419", "#d87b08", "#b55100"],
    "rubi": ["#da3879", "#c82775", "#b61972", "#920b6a", "#6f0459"],
}
RAMPA = {k: [hexc(c) for c in v] for k, v in RAMPA.items()}

ossos = []          # dicts do geo.json
pecas = []          # (osso, cubo_dict, pintor) — o UV é preenchido no empacotamento


def osso(nome, pai, pivo, rot=None):
    b = {"name": nome, "pivot": list(pivo)}
    if pai:
        b["parent"] = pai
    if rot:
        b["rotation"] = list(rot)
    ossos.append(b)
    return nome


def caixa(o, de, tam, pintor, rot=None, pivo=None, inflate=0.0):
    c = {"origin": list(de), "size": list(tam)}
    if rot:
        c["rotation"] = list(rot); c["pivot"] = list(pivo if pivo else [de[i] + tam[i] / 2 for i in range(3)])
    if inflate:
        c["inflate"] = inflate
    pecas.append((o, c, pintor))


def plano(o, de, tam, pintor, rot=None, pivo=None):
    """Plano de uma face: tam tem um zero; a face usada é north (z), east (x) ou up (y)."""
    caixa(o, de, tam, pintor, rot, pivo)


# ---------------- pintores ----------------
def tom(rampa, i):
    return RAMPA[rampa][max(0, min(4, i))]


def ruido(x, y, s=0):
    return ((x * 73856093) ^ (y * 19349663) ^ (s * 83492791)) % 100


def p_solido(rampa, topo=1, base=2, fundo=3):
    """Face lateral: linha de cima clara, corpo base, última linha sombra; topo em luz; baixo em sombra."""
    def f(face, i, j, w, h):
        if face == "up":
            return tom(rampa, topo - 1 if ruido(i, j) > 12 else topo)
        if face == "down":
            return tom(rampa, fundo)
        t = base
        if j == 0: t = topo
        elif j < h / 3: t = base - 1 if ruido(i, j, 1) < 70 else base
        elif j >= h - 1: t = fundo
        elif j > 2 * h / 3: t = base + 1 if ruido(i, j, 2) < 45 else base
        if ruido(i, j, 3) < 6: t += 1
        return tom(rampa, t)
    return f


def p_telhas(r1, r2=None, filete=False, linhas=2):
    """Placa da capa: penas LARGAS (5 px) em 2 fileiras de telhas com ponta em V; tons calmos (claro/base);
    filete prata só em penas alternadas; r1 em cima, r2 embaixo."""
    r2 = r2 or r1
    def f(face, i, j, w, h):
        rampa = r1 if j < h * 0.5 else r2
        if face in ("up", "down"):
            return tom(rampa, 1 if face == "up" else 3)
        lh = max(5, h // linhas)
        fila = j // lh; jj = j % lh
        larg = 5
        col = (i + (fila % 2) * 2) // larg; ii = (i + (fila % 2) * 2) % larg
        ponta = lh - 1 - abs(ii - larg // 2) // 2
        t = 1 if (col + fila) % 2 else 2
        if jj >= ponta: t = 3
        elif ii == 0 and jj > 0: t = min(3, t + 1)
        if filete and rampa == "roxo" and col % 2 == 0 and ii == larg - 1 and 0 < jj < ponta:
            return tom("prata", 2)
        if j == 0: t = 0
        return tom(rampa, t)
    return f


def p_peito(face, i, j, w, h):
    """Frente do peito: creme claro em cima, chevrons em zigue-zague."""
    if face != "north":
        return p_solido("creme")(face, i, j, w, h)
    t = 1 if j < h * 0.35 else 2
    zig = (j + abs(i - w // 2)) % 4
    if j > 2 and zig == 0 and abs(i - w // 2) < w // 2: t = 3
    if j == 0: t = 0
    return tom("creme", t)


def p_tronco_frente(face, i, j, w, h):
    """Frente do tronco: V creme estreitando para baixo sobre o vermelho."""
    if face != "north":
        return p_solido("verm")(face, i, j, w, h)
    meia = max(1, int((w / 2) * (1 - j / h) + 0.5))
    if abs(i + 0.5 - w / 2) < meia:
        return tom("creme", 2 if (j + abs(i - w // 2)) % 4 else 3)
    return tom("verm", 2 if j % 5 else 3)


def p_cabeca(face, i, j, w, h):
    if face == "north":
        if j >= h - 3 and 1 <= i <= w - 2:
            return tom("creme", 1 if j == h - 3 else 2)
        return tom("verm", 1 if j < 2 else 2)
    if face in ("east", "west"):
        frente = i < w // 2 if face == "east" else i >= w // 2
        if j >= h - 3 and frente:
            return tom("creme", 2)
        return tom("verm", 1 if j == 0 else (2 if j < h - 1 else 3))
    return p_solido("verm")(face, i, j, w, h)


def p_olho(face, i, j, w, h):
    if face == "north":
        return tom("creme", 0) if i in (0, w - 1) and w > 1 and i == 0 else (158, 16, 32)
    if face in ("east", "west"):
        return (158, 16, 32) if i == 0 else tom("creme", 0)
    return (60, 10, 20)


def p_forma(rampa, forma, borda=None):
    """Plano recortado. forma: 'chama' (afina e curva), 'pena' (ponta em V), 'serra' (borda de baixo em pontas),
    'tri' (triângulo para cima), 'tri_baixo', 'losango'."""
    def f(face, i, j, w, h):
        u = (i + 0.5) / w; v = (j + 0.5) / h
        if forma == "chama":       # base embaixo (v=1), ponta em cima (v=0), curvando
            meia = 0.5 * (v ** 0.9)
            centro = 0.5 + 0.18 * (1 - v) ** 2
            if abs(u - centro) > meia + 0.02: return None
            t = 3 if v > 0.8 else (2 if v > 0.35 else 1)
            if v < 0.15: t = 0
            if abs(u - centro) < 0.12 and v > 0.2: t -= 1
            return tom(rampa, t)
        if forma == "pena":        # raiz em cima (v=0), ponta em V embaixo
            meia = 0.5 if v < 0.7 else 0.5 * (1 - (v - 0.7) / 0.3)
            if abs(u - 0.5) > meia + 0.02: return None
            t = 2 if u < 0.5 else 1
            if abs(u - 0.5) < 0.1: t = 1
            if v > 0.85: t = 0
            if v < 0.15: t = 3
            return tom(rampa, t)
        if forma == "serra":       # retângulo com a borda de baixo em pontas (franja de pena)
            n = max(2, w // 4)
            k = (u * n) % 1.0
            limite = 0.55 + 0.45 * (1 - abs(k - 0.5) * 2)
            if v > limite: return None
            t = 2 if v < 0.4 else 1
            if v > limite - 0.12: t = 0
            if abs(k - 0.5) > 0.42: t = 3
            return tom(rampa, t)
        if forma == "lamina":      # plano em x (face east): raiz na frente (u=1), ponta para trás (u=0), curvando p/ cima
            meia = 0.5 * (u ** 0.8)
            centro = 0.5 - 0.2 * (1 - u) ** 2
            if abs(v - centro) > meia + 0.02: return None
            t = 3 if u > 0.85 else (2 if u > 0.4 else 1)
            if u < 0.15: t = 0
            if abs(v - centro) < 0.1 and u > 0.2: t -= 1
            return tom(rampa, t)
        if forma == "tri":
            if abs(u - 0.5) > 0.5 * v + 0.02: return None
            return tom(rampa, 0 if v < 0.3 else 1)
        if forma == "tri_baixo":
            if abs(u - 0.5) > 0.5 * (1 - v) + 0.02: return None
            return tom(rampa, 1)
        if forma == "losango":
            if abs(u - 0.5) * 2 + abs(v - 0.5) * 2 > 1.05: return None
            return tom(rampa, 0 if v < 0.3 else (2 if u < 0.5 else 3))
        return tom(rampa, 2)
    return f


def p_tranca(face, i, j, w, h):
    """Gomos diagonais (<<<) em 3 tons de dourado; nada de xadrez."""
    if face in ("up", "down"):
        return tom("ouro", 1)
    k = (j + (i if face in ("north", "east") else -i)) % 3
    return tom("ouro", (1, 2, 3)[k])


# ---------------- construção ----------------
def montar():
    # sentidos de rotação no .geo.json (conferidos no renderizador):
    #   abrir para fora (ponta de cima subindo / ponta de baixo afastando): z = -ângulo * sinal(x)
    #   inclinar a ponta de cima para fora: z = +ângulo * sinal(x)
    #   ponta de baixo indo para trás: x = +ângulo; topo inclinando para trás: x = -ângulo
    raiz = osso(ID, None, (0, 0, 0))
    corpo = osso("corpo", raiz, (0, 15, -1))
    # tronco: 2 caixas sobrepostas (volume em cruz)
    caixa(corpo, (-5, 15, -7), (10, 13, 10), p_tronco_frente)
    caixa(corpo, (-4, 16, -8), (8, 11, 12), p_tronco_frente)
    # peito de pombo
    caixa(corpo, (-4, 19, -10), (8, 8, 3), p_peito)
    caixa(corpo, (-3, 15, -9), (6, 4, 2), p_peito)
    plano(corpo, (-3, 12, -8.5), (6, 3, 0), p_forma("creme", "serra"), rot=(10, 0, 0), pivo=(0, 15, -8.5))
    pesc = osso("pescoco", corpo, (0, 28, -4))
    caixa(pesc, (-3, 27, -7), (6, 5, 6), p_cabeca)
    # colar em V (pontas de fora mais altas) + faixa + gema
    for s in (-1, 1):
        caixa(corpo, (-6 if s < 0 else 1, 21.5, -10.6), (5, 2, 1), p_solido("prata", 0, 1, 3),
              rot=(0, 0, -32 * s), pivo=(0, 22, -10.1))
    caixa(corpo, (-5, 26, -9.6), (10, 2, 3), p_solido("prata", 0, 1, 3))
    gema = osso("gema_peito_brilho", corpo, (0, 24.5, -11))
    caixa(gema, (-1.5, 22, -11.1), (3, 5, 1), p_forma("rubi", "losango"))
    # cabeça (caixa + tampa + nuca = contorno chanfrado)
    cab = osso("cabeca", pesc, (0, 31, -4))
    caixa(cab, (-4, 31, -7), (8, 8, 7), p_cabeca)
    caixa(cab, (-3, 39, -6), (6, 1, 5), p_solido("verm"))
    caixa(cab, (-3, 32, 0), (6, 6, 1), p_solido("verm"))
    caixa(cab, (-1.5, 31.5, -9), (3, 3, 2), p_solido("ouro", 0, 2, 3))
    caixa(cab, (-1, 31.5, -10.5), (2, 2, 2), p_solido("ouro", 1, 2, 3))
    caixa(cab, (-1, 30.5, -11), (2, 2, 1), p_solido("ouro", 2, 3, 4))
    for s in (-1, 1):
        x0 = -4 if s < 0 else 2
        caixa(cab, (x0, 34.5, -7), (2, 1, 2), p_olho, inflate=0.02)
        caixa(cab, (x0 - 0.5 if s < 0 else x0 - 0.5, 35.4, -7.6), (3, 1, 3), p_solido("prata", 0, 1, 3),
              rot=(0, 0, -18 * s), pivo=(2.5 * s, 35.9, -6))
    caixa(cab, (-4.5, 36, -7.5), (9, 2, 8), p_solido("prata", 0, 1, 3), rot=(-12, 0, 0), pivo=(0, 37, -7.5))
    gt = osso("gema_testa_brilho", cab, (0, 37, -8))
    caixa(gt, (-1, 35, -8.2), (2, 4, 1), p_forma("rubi", "losango"))
    # juba: 2 blocos sólidos + coroa de chamas (topos abrindo pouco: 12-36°)
    cr = osso("crista", cab, (0, 38, -3))
    caixa(cr, (-4, 38, -6), (8, 2, 8), p_solido("verm", 1, 2, 3), rot=(-8, 0, 0), pivo=(0, 38, -6))
    caixa(cr, (-3, 35.5, -1), (6, 4, 6), p_solido("verm", 1, 2, 3), rot=(12, 0, 0), pivo=(0, 38, -1))
    chama = p_forma("verm", "chama")
    for s in (-1, 1):
        plano(cr, (3 * s - 2.5, 37.5, -4.5), (5, 8, 0), chama, rot=(-8, 0, 8 * s), pivo=(3 * s, 37.5, -4.5))   # penas em U
        for k, ang in enumerate((14, 26, 38)):
            xb = (3.5 + k) * s
            plano(cr, (xb - 2.5, 37, -3 + k), (5, 8, 0), chama, rot=(-20, 0, ang * s), pivo=(xb, 37, -3 + k))
        plano(cab, (4.2 * s - 1.5, 31, -3.5), (3, 5, 0), chama, rot=(0, 0, 115 * s), pivo=(4.2 * s, 33, -3.5))
    plano(cr, (-2.5, 38, -4), (5, 5, 0), chama, rot=(-15, 0, 0), pivo=(0, 38, -4))
    for xb, ang in ((-2.5, 16), (0, 24), (2.5, 6), (0, -6)):
        plano(cr, (xb, 36.5, 1), (0, 5, 11), p_forma("verm", "lamina"), rot=(ang, 0, 0), pivo=(xb, 38.5, 1))
    # ombreiras em concha: borda de fora SOBE
    for s, nome in ((-1, "ombreira_d"), (1, "ombreira_e")):
        om = osso(nome, corpo, (4.5 * s, 28, -1))
        x0 = 4 if s > 0 else -10
        caixa(om, (x0, 25, -5), (6, 4, 8), p_solido("prata", 0, 1, 3), rot=(0, 0, -20 * s), pivo=(4.5 * s, 28, -1))
        caixa(om, (x0 + 0.5, 29, -4.5), (5, 1, 7), p_solido("roxo", 1, 2, 3), rot=(0, 0, -20 * s), pivo=(4.5 * s, 28, -1))
        caixa(om, (10 * s - 1.5, 29.5, -3), (3, 1, 5), p_solido("ouro", 0, 1, 3), rot=(0, 0, -40 * s), pivo=(9.5 * s, 30, -1))
    # asas-capa: 3 placas sólidas por lado; a de cima cobre o flanco na frente; embaixo abrem para fora e para trás
    for s, nome in ((-1, "asa_d"), (1, "asa_e")):
        asa = osso(nome, corpo, (5 * s, 28, -1))
        placas = [  # (y0, alt, x_int, esp, z0, prof, abre_z, recua_x, giro_y, pintor, franja)
            (15, 13, 5, 3, -6, 10, 20, 6, 14, p_telhas("roxo", filete=True), "roxo"),
            (8, 13, 6, 3, -5, 12, 23, 12, 8, p_telhas("roxo", "verm", filete=True), "verm"),
            (2, 11, 7, 2, -3, 13, 24, 16, 3, p_telhas("verm"), "verm"),
        ]
        for y0, alt, xi, esp, z0, prof, az, rx, gy, pint, fr in placas:
            x0 = xi if s > 0 else -xi - esp
            rot = (rx, -gy * s, -az * s); piv = (5 * s, y0 + alt, z0 + prof / 2)
            caixa(asa, (x0, y0, z0), (esp, alt, prof), pint, rot=rot, pivo=piv)
            plano(asa, (x0 + (esp + 0.01 if s > 0 else -0.01), y0 - 4, z0), (0, 4, prof), p_forma(fr, "serra"), rot=rot, pivo=piv)
    costas = osso("capa_costas", corpo, (0, 28, 3))
    for y0, alt, larg, z0, rx, pint, fr in ((15, 13, 12, 3, 8, p_telhas("roxo", filete=True), "roxo"),
                                            (8, 13, 18, 4.5, 14, p_telhas("roxo", "verm", filete=True), "verm"),
                                            (3, 10, 22, 6, 18, p_telhas("verm"), "verm")):
        caixa(costas, (-larg / 2, y0, z0), (larg, alt, 2), pint, rot=(rx, 0, 0), pivo=(0, y0 + alt, z0))
        plano(costas, (-larg / 2, y0 - 4, z0 + 2.01), (larg, 4, 0), p_forma(fr, "serra"), rot=(rx, 0, 0), pivo=(0, y0 + alt, z0))
    # cauda: 3 tranças RETAS para baixo, encostadas por fora da capa (seguem a inclinação dela, sem curva)
    cauda = osso("cauda", corpo, (0, 24, 6.5))
    caixa(cauda, (-3.5, 24, 5.2), (7, 3, 1), p_solido("prata", 0, 1, 3))
    for nome, x, n, abre in (("cauda_a", 0, 5, 0), ("cauda_b", -3, 3, 5), ("cauda_c", 3, 3, 5)):
        pai = cauda; y = 24.0
        sx = (x > 0) - (x < 0)
        for k in range(n):
            rot = (17, 0, -abre * sx) if k == 0 else None
            seg = osso(f"{nome}_{k}", pai, (x, y, 7.2), rot=rot)
            caixa(seg, (x - 1, y - 3, 6.2), (2, 3, 2), p_tranca)
            pai = seg; y -= 3
        lam = osso(f"lamina_{nome[-1]}", pai, (x, y, 7.2))
        lw, lh = (5, 8) if n == 5 else (4, 7)
        plano(lam, (x - lw / 2, y - lh, 7.2), (lw, lh, 0), p_forma("ouro", "pena"))
        plano(lam, (x, y - lh, 7.2 - lw / 2), (0, lh, lw), p_forma("ouro", "pena"))
        lb = osso(f"losango_{nome[-1]}_brilho", lam, (x, y - 4, 7.1))
        plano(lb, (x - 1, y - 5.5, 7.15), (2, 3, 0), p_forma("rubi", "losango"))
    for s, nome in ((-1, "perna_d"), (1, "perna_e")):
        x = 2.6 * s
        pe = osso(nome, raiz, (x, 15, 0))
        caixa(pe, (x - 2, 10.5, -2.5), (4, 5, 5), p_solido("verm", 1, 2, 3))
        plano(pe, (x - 2, 8.5, -2.6), (4, 3, 0), p_forma("verm", "serra"))
        caixa(pe, (x - 1.5, 8.5, -1.5), (3, 2, 3), p_solido("prata", 0, 1, 3))
        plano(pe, (x - 1.5, 9, -1.7), (3, 4, 0), p_forma("prata", "tri"), rot=(-15, 0, 0), pivo=(x, 9, -1.7))
        caixa(pe, (x - 1, 5.5, -1), (2, 3, 2), p_solido("roxo", 1, 2, 3))
        caixa(pe, (x - 1.5, 3.5, -1.5), (3, 2, 3), p_solido("prata", 0, 1, 3))
        plano(pe, (x - 1.5, 2, -1.7), (3, 2, 0), p_forma("prata", "tri_baixo"))
        caixa(pe, (x - 1.5, 1, -3), (3, 2, 4), p_solido("roxoesc", 0, 1, 3))
        for k, ang in enumerate((-28, 0, 28)):
            dedo = osso(f"dedo_{nome[-1]}_{k}", pe, (x, 1, -3), rot=(0, ang, 0))
            caixa(dedo, (x - 0.5, 0.5, -6), (1, 1, 3), p_solido("roxoesc", 0, 1, 3))
            caixa(dedo, (x - 0.5, 0.6, -7.5), (1, 1, 2), p_solido("ouro", 0, 1, 3), rot=(20, 0, 0), pivo=(x, 1.1, -5.5))
        caixa(pe, (x - 0.5, 0.5, 1), (1, 1, 2), p_solido("roxoesc", 0, 1, 3))
        caixa(pe, (x - 0.5, 0, 2.5), (1, 1, 1), p_solido("ouro", 0, 1, 3))


# ---------------- UV, textura e saída ----------------
def faces_do_cubo(tam):
    w, h, d = tam
    if 0 in (w, h, d):
        if d == 0: return {"north": (w, h)}
        if w == 0: return {"east": (d, h)}
        return {"up": (w, d)}
    return None


def gerar():
    montar()
    ilhas = []
    for idx, (o, c, pintor) in enumerate(pecas):
        uma = faces_do_cubo(c["size"])
        if uma:
            (face, (fw, fh)), = uma.items(); ilhas.append((idx, int(fw), int(fh), face))
        else:
            w, h, d = (int(v) for v in c["size"]); ilhas.append((idx, 2 * d + 2 * w, d + h, None))
    W = 256
    ordem = sorted(ilhas, key=lambda t: -t[2]); x = y = alt = 0; pos = {}
    for idx, iw, ih, face in ordem:
        if x + iw > W: x = 0; y += alt; alt = 0
        pos[idx] = (x, y); x += iw; alt = max(alt, ih)
    H = 1
    while H < y + alt: H *= 2
    tex = Image.new("RGBA", (W, H), (0, 0, 0, 0)); px = tex.load()
    for idx, iw, ih, face in ilhas:
        o, c, pintor = pecas[idx]; u, v = pos[idx]
        if face:
            c["uv"] = {face: {"uv": [u, v], "uv_size": [iw, ih]}}
            for i in range(iw):
                for j in range(ih):
                    cor = pintor(face, i, j, iw, ih)
                    if cor: px[u + i, v + j] = tuple(cor) + (255,)
        else:
            c["uv"] = [u, v]
            w, h, d = (int(t) for t in c["size"])
            rets = rg.uv_caixa(u, v, (w, h, d), False)
            for fc, (u1, v1, u2, v2) in rets.items():
                fw, fh = abs(u2 - u1), abs(v2 - v1)
                for i in range(int(fw)):
                    for j in range(int(fh)):
                        cor = pintor(fc, i, j, int(fw), int(fh))
                        if cor: px[int(min(u1, u2)) + i, int(min(v1, v2)) + j] = tuple(cor) + (255,)
    bones = []
    por_osso = {}
    for o, c, _ in pecas:
        por_osso.setdefault(o, []).append(c)
    for b in ossos:
        b = dict(b)
        if b["name"] in por_osso:
            b["cubes"] = por_osso[b["name"]]
        bones.append(b)
    geo = {"format_version": "1.12.0", "minecraft:geometry": [{"description": {
        "identifier": f"geometry.{ID}", "texture_width": W, "texture_height": H,
        "visible_bounds_width": 4, "visible_bounds_height": 4, "visible_bounds_offset": [0, 1.5, 0]}, "bones": bones}]}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / f"{ID}_blockout.geo.json").write_text(json.dumps(geo, indent=1), encoding="utf-8")
    tex.save(SAIDA / f"{ID}_blockout.png")
    n_planos = sum(1 for _, c, _ in pecas if 0 in c["size"])
    print(f"cubos {len(pecas)} (planos {n_planos}), textura {W}x{H}")
    return geo, tex


def comparar(geo, tex):
    arr = np.asarray(tex.convert("RGBA")).astype(np.float32)
    faces = rg.faces_do_modelo(geo)
    rg.folha(SAIDA / f"{ID}_blockout.geo.json", SAIDA / f"{ID}_blockout.png", SAIDA / f"{ID}_blockout_vistas.png", escala=7)
    if not FICHA.exists():
        print("ficha não encontrada: comparação pulada"); return
    ficha = Image.open(FICHA).convert("RGB")
    alvo = 420
    pares = [((646, 61, 825, 337), 0, False, "FRENTE"), ((850, 61, 1073, 334), 270, False, "DIREITA"),
             ((1091, 60, 1276, 341), 180, False, "TRÁS")]
    try:
        fonte = ImageFont.truetype("DejaVuSans.ttf", 15)
    except OSError:
        fonte = ImageFont.load_default()
    cols = []
    for (a, b, c, d), yaw, esp, nome in pares:
        f = ficha.crop((a, b, c, d)); k = alvo / (d - b); f = f.resize((int((c - a) * k), alvo), Image.LANCZOS)
        m = rg.desenhar(faces, arr, yaw, 0, escala=9)
        k2 = alvo / m.height * (45.0 / 45.0); m = m.resize((int(m.width * alvo / m.height), alvo), Image.LANCZOS)
        cols.append((f, m, nome))
    W = sum(max(f.width, m.width) + 20 for f, m, _ in cols); H = 2 * alvo + 70
    out = Image.new("RGB", (W, H), (235, 235, 230)); dr = ImageDraw.Draw(out); x = 10
    for f, m, nome in cols:
        out.paste(f, (x, 25)); out.paste(m, (x, alvo + 55))
        dr.text((x, 5), f"ficha {nome}", fill=(20, 20, 20), font=fonte)
        dr.text((x, alvo + 35), f"blockout {nome}", fill=(20, 20, 20), font=fonte)
        x += max(f.width, m.width) + 20
    out.save(SAIDA / f"{ID}_blockout_comparacao.png")


if __name__ == "__main__":
    g, t = gerar()
    comparar(g, t)
    print("gravado em", SAIDA)

"""Cocórvolt (#006, Elétrico): galo cinza da tempestade, de chapéu cônico de palha, túnica azul-marinho com raios."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, arredondado, arredondado2, octogono, anel

ID = "cocorvolt"; NOME = "Cocórvolt"; NUMERO = 6
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 28.0, -3.0), 7.5)
ONDAS = []
ANIM_PARADO = {
    "talisma_d": [(0, 0, 0), (4, 0, 6), (0, 0, 0), (-4, 0, -6), (0, 0, 0)],
    "talisma_e": [(0, 0, 0), (-4, 0, -6), (0, 0, 0), (4, 0, 6), (0, 0, 0)],
}
ANIM_ANDANDO = {
    "talisma_d": [(0, 0, 0), (10, 0, 12), (0, 0, 0), (-10, 0, -12), (0, 0, 0)],
    "talisma_e": [(0, 0, 0), (-10, 0, -12), (0, 0, 0), (10, 0, 12), (0, 0, 0)],
}

# ---------------- paleta (Paleta de Cores da ficha) ----------------
CINZA_CLARO = (214, 214, 218); CINZA = (160, 160, 168); CINZA_MEDIO = (118, 118, 126)
CINZA_ESC = (74, 74, 82); GRAFITE = (44, 44, 50); PRETO_V = (24, 24, 30)
MARINHO = (34, 54, 118); MARINHO_CLARO = (56, 90, 172); MARINHO_ESC = (22, 30, 66)
AZUL = (46, 118, 236)
OURO_V = (232, 178, 56); OURO_V_CLARO = (255, 220, 120); OURO_V_ESC = (150, 100, 30)
PALHA = (214, 172, 102); PALHA_CLARA = (236, 200, 136); PALHA_ESC = (160, 118, 64); PALHA_SOMBRA = (104, 76, 44)
AMARELO_P = (250, 196, 40); AMARELO_P_ESC = (214, 150, 26)
VERMELHO = (214, 42, 32); VERMELHO_ESC = (150, 22, 24)
# cores que brilham no escuro (devolvidas sem luz, para a _glowmask achar)
RAIO = (255, 214, 50); RAIO_CLARO = (255, 244, 160)
OLHO_AZUL = (16, 104, 255); OLHO_CLARO = (64, 176, 255); OLHO_MIOLO = (178, 236, 255)
BRILHAM = {RAIO, RAIO_CLARO, OLHO_AZUL, OLHO_CLARO, OLHO_MIOLO}
def brilha(c, cor): return tuple(cor[:3]) in BRILHAM

def ruido(x, y, z, passo=0.5):
    """Ruído fixo por 'voxel' (passo em unidades): -1..1. Dá o pixelado de blocos da ficha."""
    h = math.sin(math.floor(x / passo) * 12.9898 + math.floor(y / passo) * 78.233 + math.floor(z / passo) * 37.719) * 43758.5453
    return (h - math.floor(h)) * 2 - 1

def tri(t):
    """Onda triangular -1..1 de período 1."""
    t = t - math.floor(t)
    return 4 * t - 1 if t < 0.5 else 3 - 4 * t

# ---------------- raio (glifo) ----------------
RAIO_POL = [(0.0, 1.0), (0.72, 1.0), (0.3, 0.18), (0.78, 0.18), (-0.42, -1.0), (-0.06, -0.12), (-0.6, -0.12)]
def no_poligono(u, v, pol):
    dentro = False
    n = len(pol)
    for k in range(n):
        (x1, y1), (x2, y2) = pol[k], pol[(k + 1) % n]
        if (y1 > v) != (y2 > v) and u < x1 + (v - y1) * (x2 - x1) / (y2 - y1): dentro = not dentro
    return dentro

def glifo_raio(u, v):
    """u, v em -1..1 (v para cima). Devolve RAIO (miolo claro) / RAIO / None."""
    if not no_poligono(u, v, RAIO_POL): return None
    # miolo claro: o mesmo polígono encolhido
    if no_poligono(u * 1.6 + 0.04, v * 1.2, RAIO_POL): return RAIO_CLARO
    return RAIO

# ---------------- cabeça ----------------
FAC_A, FAC_B = (1.4, -4.3), (3.3, -2.4)          # quinas da face diagonal (frente estreita -> lado)
FAC_T = 1.5
FAC_M = ((FAC_A[0] + FAC_B[0]) / 2, (FAC_A[1] + FAC_B[1]) / 2)
FAC_C = (FAC_M[0] - 0.7071 * FAC_T / 2, FAC_M[1] + 0.7071 * FAC_T / 2)
FAC_L = math.hypot(FAC_B[0] - FAC_A[0], FAC_B[1] - FAC_A[1])
OLHO_Y, OLHO_U = 29.85, 0.12

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up" or y > 31.3: base = CINZA_ESC
    elif z < -2.6: base = mix((176, 176, 184), (214, 214, 220), clamp((y - 25) / 5))
    elif z < 0.6: base = mix((150, 150, 158), (188, 188, 196), clamp((y - 25) / 5))
    else: base = mix((120, 120, 128), (164, 164, 172), clamp((y - 24) / 6))
    # escamas de pena (fileiras com a borda de baixo recortada)
    t = (y + 0.35 * abs(math.sin(x * 2.1 + z * 1.7))) / 1.15
    if t - math.floor(t) < 0.14: base = mix(base, (60, 60, 70), 0.3)
    return tom(base, 0.05 * ruido(x, y, z))

def olho_volt(u, v, ru=1.08, rv=0.42):
    """Olho eletrificado: retângulo arredondado azul brilhante com miolo branco, corte bravo descendo para o bico
    (u negativo = bico) e órbita escura em volta."""
    es = (abs(u) / (ru + 0.16)) ** 4 + (abs(v + 0.03) / (rv + 0.2)) ** 4
    if es > 1: return None
    corte = rv * (0.5 + 0.5 * (u / ru))           # borda de cima do brilho: desce para o bico
    e = (abs(u) / ru) ** 4 + (abs(v) / rv) ** 4
    if e > 1 or v > corte: return (36, 40, 52) if v <= corte + 0.32 else (56, 58, 68)
    if e > 0.45 or v > corte - 0.14: return OLHO_AZUL
    if e > 0.12 or v > corte - 0.24: return OLHO_CLARO
    return OLHO_MIOLO

def mat_cabeca():
    return mat_luz(cor_cabeca, borda=.03, curva=.3)

def mat_luz(cor_fn, **kw):
    """Como g.mat_cor, mas cores da lista BRILHAM passam sem luz (continuam reconhecíveis na _glowmask)."""
    def f(c):
        base = cor_fn(c["p"], c["face"])
        if base is None: return None
        if base in BRILHAM: return base
        return tom(base, g.contexto_luz(c, **kw))
    return f

def mat_faceta(lado):
    """Face diagonal do rosto com o olho inteiro na face de fora. A cor da pena usa o ponto já girado (mundo),
    para casar com a frente e o lado da cabeça."""
    fora = "east" if lado > 0 else "west"
    cx, cz = FAC_C[0] * lado, FAC_C[1]
    a = math.radians(45 * lado)
    def f(c):
        x, y, z = c["p"]
        if c["face"] in ("north", "south"): return None     # pontas da faceta: escondidas (sem fio claro na emenda)
        if c["face"] == fora:
            cor = olho_volt(z - FAC_C[1] - OLHO_U, y - OLHO_Y)
            if cor is not None: return cor
        dx, dz = x - cx, z - cz
        xm, zm = cx + dx * math.cos(a) + dz * math.sin(a), cz - dx * math.sin(a) + dz * math.cos(a)
        return tom(cor_cabeca((xm, y, zm), c["face"]), g.contexto_luz(c, borda=.03, curva=.3))
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return (206, 122, 28)
    if face in ("east", "west") and abs(z + 5.0) < 0.26 and abs(y - 29.2) < 0.2: return (130, 72, 20)   # narina
    if face in ("east", "west", "north") and 27.45 < y < 27.68 and z > -6.9: return (128, 62, 18)      # linha da boca
    t = clamp((-z - 4.1) / 4.2)                                  # base amarela -> ponta laranja
    cor = mix((255, 210, 58), (238, 142, 26), t * 0.9)
    if face == "up": cor = tom(cor, 0.18)
    return cor

def cor_barbela(p, face):
    x, y, z = p
    return mix(VERMELHO_ESC, VERMELHO, clamp((y - 23.6) / 2.6)) if face != "up" else VERMELHO

def cor_bochecha(p, face):
    x, y, z = p
    if face == "north": return cor_cabeca((x, y, -2.0), face)              # dobra atrás da face: mesmo cinza do lado
    base = mix(CINZA_MEDIO, CINZA, clamp((y - 24.5) / 5)) if z < 0.5 else mix(CINZA_ESC, CINZA_MEDIO, clamp((y - 24.5) / 5))
    t = (y + 0.5 * tri(z / 1.4)) / 1.3
    if t - math.floor(t) < 0.16: base = mix(base, (60, 60, 70), 0.3)
    return base

def forma_espeto(u, v):
    """Pena espetada (ponta reta, como as penas em bloco da ficha): larga na raiz e afina em linha reta."""
    meia = 1.0 if v < 0.25 else max(0.0, 1.0 - (v - 0.25) / 0.75) ** 0.85
    uc = u + 0.25 * v
    return abs(uc) <= meia, meia - abs(uc), uc

CINZAS_RUFO = ((206, 206, 212), (176, 176, 184), (138, 138, 148))
CINZAS_NUCA = ((120, 120, 128), (92, 92, 100), (70, 70, 78))
CINZAS_MEIO = ((150, 150, 158), (122, 122, 130), (96, 96, 106))

def mat_tufo(y0, L, cores):
    """Tufo: claro na raiz, cinza médio na ponta (pela distância à raiz), luz por face e contorno escuro."""
    c0, c1, c2 = cores
    def f(c):
        v = clamp((y0 - c["p"][1]) / L)
        base = mix(c0, c1, v / 0.6) if v < 0.6 else mix(c1, c2, (v - 0.6) / 0.4)
        luz = 0.06 + (0.16 if c["face"] == "up" else -0.3 if c["face"] == "down" else 0.0)
        if g.na_borda(c): luz -= 0.2
        return tom(base, luz)
    return f

def espeto(nome, raiz, phi, flare, varre, L, W, esp, cores, lado):
    """Tufo de pena pontudo preso ao crânio: placa grossa com ponta em losango (cubo girado 45°). O osso de fora gira
    em y (phi > 0 = para trás); a pena abre 'flare' graus para fora e varre 'varre' graus para trás."""
    x, y, z = raiz
    m = mat_tufo(y, L * 0.72 + W / 2, cores)
    cy = y - L * 0.72; sq = W / 1.4142
    return osso(nome, list(raiz), [0, -phi * lado, 0], [osso(nome + "_p", list(raiz), [-varre, 0, flare * lado], [
        peca(nome, [x - esp / 2, cy, z - W / 2], [x + esp / 2, y, z + W / 2], m, res=4),
        peca(nome + "_ponta", [x - esp / 2 + 0.03, cy - sq / 2, z - sq / 2], [x + esp / 2 - 0.03, cy + sq / 2, z + sq / 2], m,
             rot=(45, 0, 0), pivo=(x, cy, z), res=4)])])

def pena_triangulo(nome, raiz, phi, flare, varre, S, esp, cores, lado):
    """Pena triangular: um quadrado de lado S girado 45° (losango) com o centro na raiz; a metade que sai do crânio
    lê como um triângulo pontudo. Gira como o 'espeto' (phi para trás, abre para fora, varre para trás)."""
    x, y, z = raiz
    m = mat_tufo(y + S * 0.7, S * 1.4, cores)
    return osso(nome, list(raiz), [0, -phi * lado, 0], [osso(nome + "_p", list(raiz), [-varre, 0, flare * lado], [
        peca(nome, [x - esp / 2, y - S / 2, z - S / 2], [x + esp / 2, y + S / 2, z + S / 2], m, rot=(45, 0, 0),
             pivo=(x, y, z), res=4)])])

CINZAS_TUFO = ((216, 216, 222), (188, 188, 196), (136, 136, 146))      # cinza claro com ponta cinza média
CINZAS_TUFO2 = ((178, 178, 186), (150, 150, 160), (108, 108, 118))

def montar_cabeca():
    i0 = len(g.PECAS)
    cab = []
    mc = mat_cabeca()
    F = (24.0, 32.4)
    # crânio quase cúbico (profundidade ~ largura): miolo + blocos em cruz
    cab.append(peca("cranio_a", [-3.3, 24.6, -2.4], [3.3, 31.4, 3.0], mc, faixa=F, res=4))
    cab.append(peca("cranio_b", [-2.6, 24.2, -3.0], [2.6, 32.3, 4.4], mc, faixa=F, res=4))
    cab.append(peca("cranio_c", [-3.0, 24.4, -2.6], [3.0, 32.0, 3.9], mc, faixa=F, res=4))
    cab.append(peca("cranio_nuca", [-1.8, 25.0, -1.0], [1.8, 31.6, 5.0], mc, faixa=F, res=4))
    cab.append(peca("cranio_frente", [-1.42, 24.6, -4.3], [1.42, 31.2, -3.0], mc, faixa=F, res=4))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("cranio_faceta_" + s, [cx - FAC_T / 2, 24.8, cz - FAC_L / 2], [cx + FAC_T / 2, 31.0, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, 27.9, cz), faixa=F, res=8, brilho=brilha))
    # sobrancelhas: aba cinza-escura sobre o olho, descendo para o bico (cara séria de mestre)
    msob = mat_luz(lambda p, f: (170, 170, 178) if f == "up" else (104, 104, 114), borda=.12, curva=.2)
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        fx0, fx1 = sorted((cx + FAC_T / 2 * lado - 0.15 * lado, cx + FAC_T / 2 * lado + 0.42 * lado))
        cab.append(osso("sobrancelha_" + s_, [cx, OLHO_Y, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s_, [fx0, OLHO_Y + 0.62, cz - FAC_L / 2 - 0.05], [fx1, OLHO_Y + 1.12, cz + FAC_L / 2 + 0.2], msob,
                 rot=(-13, 0, 0), pivo=(cx, OLHO_Y + 0.9, cz))]))
    # bico: cunha grossa amarelo-laranja em degraus que afinam e descem até a ponta curva; mandíbula menor, recuada e
    # mais escura. Base com ~1/3 da largura do rosto; comprimento ~40% da profundidade da cabeça.
    mb = mat_luz(cor_bico, borda=.07, curva=.3)
    bico = []
    for lado in (-1, 1):                     # metades em V (de cima e de frente o bico é um triângulo largo)
        x0, x1 = sorted((0.0, 1.5 * lado))
        dy = 0.0 if lado > 0 else -0.04      # evita faces coplanares no meio
        bico.append(peca("bico_" + ("d" if lado < 0 else "e"), [x0, 27.75 + dy, -8.0], [x1, 29.75 + dy, -4.1], mb,
                         rot=(0, 19 * lado, 0), pivo=(1.5 * lado, 28.7, -4.1), faixa=(26.5, 30)))
    bico.append(peca("bico_cume", [-1.0, 29.25, -7.6], [1.0, 29.85, -4.1], mb, rot=(-8, 0, 0), pivo=(0, 29.85, -4.1),
                     faixa=(26.5, 30)))
    bico.append(peca("bico_ponta", [-0.75, 27.3, -8.3], [0.75, 29.0, -7.2], mb, rot=(-30, 0, 0), pivo=(0, 29.0, -7.2),
                     faixa=(26.5, 30)))
    cab.append(osso("bico", [0, 28.7, -4.1], [-10, 0, 0], bico))
    cab.append(peca("bico_baixo", [-1.0, 27.0, -6.3], [1.0, 27.7, -4.1],
                    mat_luz(lambda p, f: (214, 118, 30) if f != "down" else (170, 86, 22), borda=.12, curva=.2)))
    # barbela vermelha: dois lóbulos pendurados sob o bico
    mbar = mat_luz(cor_barbela, borda=.06, curva=.3)
    cab += arredondado("barbela_d", [-1.25, 23.5, -5.15], [-0.05, 27.2, -3.95], mbar, r=0.3)
    cab += arredondado("barbela_e", [0.05, 24.3, -5.0], [1.2, 27.2, -3.85], mbar, r=0.3)
    # penas das bochechas em escamas: losangos sobrepostos deitados no lado da cabeça (as de trás mais para fora),
    # as pontas de trás/baixo aparecem como penas pontudas; e duas pontas grandes que saltam para fora sob a aba
    for lin, y0 in enumerate((30.5, 28.7, 26.9)):
        for col, z in enumerate((-1.4 + 0.8 * lin, 0.7 + 0.8 * lin, 2.8 + 0.6 * lin)):
            for lado in (-1, 1):
                cab.append(pena_triangulo(f"escama{lin}{col}_{'d' if lado < 0 else 'e'}", ((3.25 + 0.25 * col) * lado, y0, z),
                                          6 + 10 * col, 14 + 6 * col, 0, 2.5 - 0.15 * lin, 0.8,
                                          CINZAS_TUFO if col < 2 else CINZAS_TUFO2, lado))
    for k, (y0, z, phi, fl, S) in enumerate([(30.8, -0.6, 26, 58, 3.4), (29.2, 1.6, 40, 50, 3.4)]):
        for lado in (-1, 1):
            cab.append(pena_triangulo(f"tufo{k}_{'d' if lado < 0 else 'e'}", (3.3 * lado, y0, z), phi, fl, 0, S, 1.2,
                                      CINZAS_TUFO, lado))
    # leque do pescoço (como na rev1): penas em bloco que abrem para os lados embaixo da cabeça
    for k, (y0, phi, L, fl) in enumerate([(27.6, 24, 4.6, 52), (26.1, 30, 4.4, 44), (24.8, 40, 3.8, 36)]):
        for lado in (-1, 1):
            s_ = "d" if lado < 0 else "e"
            x, z = anel(3.3, 2.6, 0.2, phi, lado)
            cab.append(osso(f"rufo{k}_{s_}", [x, y0, z], [0, -phi * lado, 0], [
                pena_bloco(f"rufo{k}_{s_}_p", (x, y0, z), (-24, 0, fl * lado), L, 2.4, 1.8, CINZAS_TUFO, afina=(0.62, 0.32))]))
    return i0, cab

# ---------------- chapéu cônico de palha ----------------
CH_APICE, CH_ABA, CH_R, CH_Z, CH_N, CH_T = 38.6, 32.8, 12.2, -0.5, 16, 0.6
CH_ALFA = math.atan2(CH_APICE - CH_ABA, CH_R)
CH_S = math.hypot(CH_APICE - CH_ABA, CH_R)

def mat_chapeu(k):
    yaw = 2 * math.pi * k / CH_N
    tg = math.tan(math.pi / CH_N)
    def meia(s): return s * math.cos(CH_ALFA) * tg + 0.05
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        s = CH_Z - z                                       # distância do ápice pela geratriz
        if face in ("up", "down", "east", "west") and abs(x) > meia(s): return None
        borda_lado = meia(s) - abs(x)
        if face == "down":
            return tom(mix(PALHA_SOMBRA, PALHA_ESC, clamp(s / CH_S)), -0.1 if borda_lado < 0.15 else 0.0)
        if face in ("north", "east", "west"):
            return tom(PALHA_CLARA, -0.25 if c["j"] in (0, c["th"] - 1) else 0.0)
        if face == "south": return PALHA_ESC
        phi = yaw + math.atan2(x, s * math.cos(CH_ALFA))
        sz = 8.6 + 1.5 * tri(phi * 8 / (2 * math.pi))   # anel de raios em zigue-zague
        sz2 = 4.6 + 0.9 * tri(phi * 8 / (2 * math.pi) + 0.5)
        if abs(s - sz) < 0.42: return RAIO_CLARO if abs(s - sz) < 0.16 else RAIO
        if abs(s - sz2) < 0.26 and tri(phi * 8 / (2 * math.pi) * 0.5 + 0.25) > 0.0: return RAIO
        if s > CH_S - 0.75:                                # aba: barra mais clara com fio escuro
            return PALHA_ESC if s < CH_S - 0.6 else tom(PALHA_CLARA, 0.05 * ruido(x, 0, s, 0.6))
        if s < sz:                                         # topo escuro (grafite) com costuras de palha
            if s < 1.2: return PALHA
            cor = mix((52, 50, 56), (80, 76, 80), clamp(s / 8))
            if borda_lado < 0.2: cor = PALHA_ESC
            return tom(cor, 0.06 * ruido(x, 0, s, 0.7))
        cor = mix(PALHA, PALHA_CLARA, clamp((s - sz) / 4))
        if borda_lado < 0.16: cor = tom(cor, -0.2)
        anel_ = (s - sz) / 1.5
        if anel_ - math.floor(anel_) < 0.12: cor = tom(cor, -0.15)
        if abs(math.sin(x * 4.2)) < 0.12: cor = tom(cor, -0.08)   # fios de palha
        return tom(cor, 0.05 * ruido(x, 0, s, 0.6))
    return f

def mat_talisma(cx, cy, W, H):
    """Talismã: moldura de ouro, fundo grafite e raio amarelo brilhando, nas duas faces largas."""
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        if face not in ("north", "south"):
            return tom(OURO_V, -0.25 if face == "down" else 0.1 if face == "up" else -0.05)
        u = (x - cx) / (W / 2); v = (y - cy) / (H / 2)
        if face == "south": u = -u
        bx, by = (1 - abs(u)) * W / 2, (1 - abs(v)) * H / 2
        b = min(bx, by)
        if b < 0.08: return OURO_V_ESC
        if b < 0.42: return mix(OURO_V_CLARO, OURO_V, clamp((0.6 - v) / 1.4))
        if b < 0.5: return OURO_V_ESC
        r = glifo_raio(u / 0.62, v / 0.62)
        if r: return r
        return mix((48, 50, 60), (30, 32, 40), clamp((0.6 - v) / 1.6))
    return f

def montar_chapeu():
    filhos = []
    for k in range(CH_N):
        yaw = 360 * k / CH_N
        w = CH_S * math.cos(CH_ALFA) * math.tan(math.pi / CH_N) + 0.08
        filhos.append(osso(f"chapeu_gomo{k}", [0, CH_APICE, CH_Z], [0, yaw, 0], [
            peca(f"chapeu_gomo{k}", [-w, CH_APICE - CH_T, CH_Z - CH_S], [w, CH_APICE, CH_Z], mat_chapeu(k),
                 rot=(-math.degrees(CH_ALFA), 0, 0), pivo=(0, CH_APICE, CH_Z), res=5, brilho=brilha)]))
    filhos.append(peca("chapeu_ponta", [-0.7, CH_APICE - 0.4, CH_Z - 0.7], [0.7, CH_APICE + 0.45, CH_Z + 0.7],
                       mat_luz(lambda p, f: PALHA_CLARA if f == "up" else PALHA, borda=.2)))
    # talismãs pendurados na aba (ossos próprios para balançar)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x = 9.8 * lado
        topo = CH_ABA + CH_T + (CH_APICE - CH_ABA) * (1 - 9.8 / CH_R) - 0.9
        cy, H, W = 27.3, 5.6, 3.1
        # osso animado sem giro de repouso; o giro (meio de frente, meio de lado) fica num osso estático de dentro
        filhos.append(osso("talisma_" + s, [x, topo, CH_Z], [0, 0, 0], [osso("talisma_giro_" + s, [x, topo, CH_Z], [0, -32 * lado, 0], [
            peca("talisma_cordao_" + s, [x - 0.18, cy + H / 2 - 0.1, CH_Z - 0.18], [x + 0.18, topo + 0.3, CH_Z + 0.18],
                 mat_luz(lambda p, f: OURO_V_ESC, borda=.1)),
            peca("talisma_argola_" + s, [x - 0.55, cy + H / 2 - 0.15, CH_Z - 0.4], [x + 0.55, cy + H / 2 + 0.45, CH_Z + 0.4],
                 mat_luz(lambda p, f: OURO_V, borda=.2)),
            peca("talisma_" + s, [x - W / 2, cy - H / 2, CH_Z - 0.3], [x + W / 2, cy + H / 2, CH_Z + 0.3],
                 mat_talisma(x, cy, W, H), res=8, brilho=brilha)])]))
    return osso("chapeu", [0, CH_ABA, CH_Z], [0, 0, 0], filhos)

# ---------------- túnica (traje) ----------------
def tex_marinho(x, y, z):
    return tom(mix(MARINHO, MARINHO_CLARO, 0.25 + 0.2 * ruido(x, y, z, 0.7)), 0.0)

def penas_costas(x, y, z, claro=False):
    """Fileiras de penas cinza com a borda de baixo em ponta (costas)."""
    lin = 2.3
    t = (y + 0.7 * tri(x / 2.6)) / lin
    f = t - math.floor(t)
    if abs(x) < 1.9: base = mix(GRAFITE, CINZA_ESC, 0.3 + 0.7 * f)
    else: base = mix(CINZA_MEDIO, CINZA_CLARO if claro else CINZA, 0.4 + 0.6 * f)
    if f < 0.08: base = mix(base, (40, 40, 48), 0.35)
    return base

V_BAIXO, V_K = 16.4, 0.30           # gola em V da túnica: ponta e abertura

def cor_torso(p, face):
    x, y, z = p
    if face == "south" or (z > 2.9 and face != "up"):
        if abs(x) < 2.1: return penas_costas(x, y, z)
        if y < 17.3: return OURO_V
        return tex_marinho(x, y, z)
    if face == "north" or (z < -3.2 and face != "up"):
        d = abs(x) - V_K * (y - V_BAIXO)
        if d < 0: return mix(PRETO_V, GRAFITE, clamp((y - 17) / 6))
        if d < 0.6: return PRETO_V
        if d < 0.95: return OURO_V
        return tex_marinho(x, y, z)
    if face == "up":
        if abs(x) < 2.6 and z < 1.6: return PRETO_V
        return tex_marinho(x, y, z)
    return tex_marinho(x, y, z)

SAIA_Y0, SAIA_Y1 = 7.1, 16.0

def cor_saia(p, face):
    x, y, z = p
    if face == "down": return MARINHO_ESC
    costas = face == "south" or (z > 2.9 and face != "up")
    if costas: return penas_costas(x, y, z, claro=True)
    if y < SAIA_Y0 + 0.5: return OURO_V                    # barra dourada
    if face == "north" or z < -3.4:
        ax = abs(x)
        if ax < 2.45:                                      # painel central escuro com o raio (Padrão do Traje)
            if ax > 2.05 or y < SAIA_Y0 + 1.0: return OURO_V
            r = glifo_raio(x / 1.85, (y - 11.85) / 3.9)
            if r: return r
            return tom(MARINHO_ESC, 0.05 * ruido(x, y, z))
        if ax < 2.75: return OURO_V_ESC
        if ax > 4.55: return OURO_V                         # beirada da frente da túnica
    return tex_marinho(x, y, z)

def cor_cinto(p, face):
    x, y, z = p
    base = mix(PRETO_V, GRAFITE, 0.4 + 0.3 * ruido(x, y, z, 0.6))
    t = (y - 15.6) / 0.62
    if t - math.floor(t) < 0.18: base = tom(base, -0.4)          # dobras da faixa
    return base

def mat_emblema(cx, cy, R):
    """Símbolo Elétrico: octógono de ouro com fundo escuro e raio amarelo."""
    def f(c):
        x, y, z = c["p"]
        if c["face"] != "north":
            return tom(OURO_V, -0.2 if c["face"] in ("east", "west", "down") else 0.05)
        u, v = (x - cx) / R, (y - cy) / R
        d = max(abs(u), abs(v), (abs(u) + abs(v)) / 1.32)    # octógono
        if d > 1.0: return None
        if d > 0.94: return OURO_V_ESC
        if d > 0.7: return mix(OURO_V_CLARO, OURO_V, clamp((0.4 - v) / 1.2))
        if d > 0.64: return OURO_V_ESC
        r = glifo_raio(u / 0.56, v / 0.56)
        if r: return r
        return (34, 34, 42)
    return f

def mat_ombreira(lado, painel=False):
    """Ombreira azul com friso de ouro nas bordas; o painel do lado tem moldura e dois raios pequenos."""
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        i, j, tw, th = c["i"], c["j"], c["tw"], c["th"]
        bi = min(i, tw - 1 - i) / 4.0; bj = min(j, th - 1 - j) / 4.0   # distância à borda (unidades, res 4)
        b = min(bi, bj)
        if face == "down": return tom(MARINHO_ESC, -0.1)
        if b < 0.1: return OURO_V_ESC
        if b < 0.42: return tom(mix(OURO_V_CLARO, OURO_V, j / max(th, 1)), 0.08 if face == "up" else 0.0)
        if painel and face == fora:
            (x0, y0, z0), (x1, y1, z1) = c["b"]
            u = (z - (z0 + z1) / 2) / ((z1 - z0) / 2); v = (y - (y0 + y1) / 2) / ((y1 - y0) / 2)
            if b < 0.62: return MARINHO_ESC
            if b < 0.8: return OURO_V
            for uc in (-0.38, 0.38):
                r = glifo_raio((u - uc) / 0.3, v / 0.5)
                if r: return r
            return MARINHO_ESC
        cor = mix(MARINHO, MARINHO_CLARO, 0.55 if face == "up" else 0.3)
        return tom(cor, 0.05 * ruido(x, y, z, 0.7))
    return f

def cor_ombreira(lado):
    """Cúpula da ombreira (pintura 3D): azul, friso de ouro na beirada de fora e na barra de baixo (frente, trás e
    lado de fora), e um raio pequeno na frente."""
    def f(p, face):
        x, y, z = p
        ax = abs(x)
        if face == "down": return MARINHO_ESC
        if face == "north" and 4.6 < ax < 7.3 and 21.5 < y < 23.9:
            r = glifo_raio((ax - 5.85) / 0.95 * (1 if lado > 0 else -1), (y - 22.75) / 1.05)
            if r: return r
        friso = ax > 7.45 or y < 21.5
        if face == "up": friso = ax > 7.45 or z < -3.6 or z > 3.2
        if friso:
            fio = ax > 7.78 or y < 21.18 or (face == "up" and (z < -3.9 or z > 3.5))
            return OURO_V_ESC if fio else OURO_V
        return mix(MARINHO, MARINHO_CLARO, (0.55 if face == "up" else 0.3) + 0.12 * ruido(x, y, z, 0.7))
    return f

OURO_FRISO = (238, 184, 58); OURO_FRISO_ESC = (160, 104, 26); MIOLO_OMB = (20, 26, 52)

def mat_pauldron(lado, parte):
    """Placa da ombreira: friso de ouro grosso (0,7) em volta de cada face larga, miolo azul-escuro quase preto e, na
    face de fora, um raio de ouro. As faces finas (bordas da placa) são todas de ouro."""
    def f(c):
        face = c["face"]
        i, j, tw, th = c["i"], c["j"], c["tw"], c["th"]
        larga = ("up", "down")
        if face not in larga:
            return tom(OURO_FRISO, 0.08 if face == "up" else -0.12 if face == "down" else 0.0)
        bi = min(i, tw - 1 - i) / 4.0; bj = min(j, th - 1 - j) / 4.0
        b = min(bi, bj)
        if face == "down": return tom(MIOLO_OMB, -0.2) if b > 0.5 else OURO_FRISO_ESC
        if b < 0.12: return OURO_FRISO_ESC
        if b < 0.7: return tom(OURO_FRISO, 0.12 if bj < bi else 0.0)
        if b < 0.82: return OURO_FRISO_ESC
        (x0, y0, z0), (x1, y1, z1) = c["b"]
        x, y, z = c["p"]
        if parte == "caida":
            u = (z - (z0 + z1) / 2) / ((z1 - z0) / 2 - 0.9)
            v = -(abs(x) - (abs(x0) + abs(x1)) / 2) / ((abs(x1 - x0)) / 2 - 0.8)
            r = glifo_raio(u / 0.5, v / 0.95)
            if r: return OURO_FRISO if r == RAIO else (255, 226, 120)
        return mix(MIOLO_OMB, (34, 48, 98), 0.3 + 0.25 * ruido(x, y, z, 0.7))
    return f

# ---------------- penas em bloco ----------------
def dist_polilinha(px, py, pts):
    melhor = 9e9
    for k in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[k], pts[k + 1]
        dx, dy = x2 - x1, y2 - y1
        t = clamp(((px - x1) * dx + (py - y1) * dy) / max(dx * dx + dy * dy, 1e-9))
        melhor = min(melhor, math.hypot(px - x1 - t * dx, py - y1 - t * dy))
    return melhor

def mat_pena_raio(c0, c1, ei, inv, raio=False, fase=0.0):
    """Pena em bloco (cinza) com um raio amarelo em Z nas faces largas (Cauda Energizada da ficha)."""
    base = g.mat_pena(c0, c1, ei, inv, borda=.18)
    def f(c):
        if raio and c["face"] in ("east", "west"):
            (x0, y0, z0), (x1, y1, z1) = c["b"]
            x, y, z = c["p"]
            L, h, yc = z1 - z0, y1 - y0, (y0 + y1) / 2 + 0.25 * fase
            pts = [(z0 + 0.12 * L, yc + 0.26 * h), (z0 + 0.48 * L, yc + 0.2 * h), (z0 + 0.5 * L, yc - 0.12 * h),
                   (z0 + 0.92 * L, yc - 0.2 * h)]
            d = dist_polilinha(z, y, pts)
            if d < 0.3: return RAIO_CLARO if d < 0.12 else RAIO
        return base(c)
    return f

def pena_bloco(nome, raiz, rot, L, W, esp, cores, afina=(0.85, 0.7), afina_w=(0.66, 0.3), passos=(0.55, 0.28, 0.17)):
    """Pena RETA em bloco que afina até a ponta em 3 degraus, para baixo a partir da raiz (largura em z,
    espessura em x; 'afina' = espessura do 2º e 3º degraus)."""
    x, y, z = raiz
    partes = [(passos[0], 1.0, 1.0, cores[0], cores[1]), (passos[1], afina_w[0], afina[0], cores[1], cores[2]),
              (passos[2], afina_w[1], afina[1], cores[2], cores[2])]
    pecas, y0 = [], y
    for k, (fl, fw, fe, c0, c1) in enumerate(partes):
        h, w, e = L * fl, W * fw, esp * fe
        pecas.append(peca(f"{nome}_{k}", [x - e / 2, y0 - h, z - w / 2], [x + e / 2, y0, z + w / 2], g.mat_pena(c0, c1, 1, True, borda=.16)))
        y0 -= h - 0.05
    return osso(nome, list(raiz), list(rot), pecas)

def mat_pena_cauda(c0, c1, ei, inv, fase=0.0, raio=True):
    """Pena larga da cauda: miolo grafite/preto, borda de cima e de baixo cinza média (separa as penas sobrepostas)
    e um raio amarelo em Z nas duas faces largas."""
    def f(c):
        (x0, y0, z0), (x1, y1, z1) = c["b"]
        x, y, z = c["p"]
        face = c["face"]
        t = clamp((z - z0) / max(z1 - z0, 1e-6))
        base = mix(c0, c1, t)
        if face == "up": return tom(mix(base, (132, 132, 140), 0.7), 0.1)
        if face == "down": return tom(base, -0.3)
        if face in ("east", "west"):
            h = y1 - y0
            if raio:
                L, yc = z1 - z0, (y0 + y1) / 2 + 0.2 * fase
                pts = [(z0 + 0.1 * L, yc + 0.24 * h), (z0 + 0.5 * L, yc + 0.16 * h), (z0 + 0.52 * L, yc - 0.12 * h),
                       (z0 + 0.95 * L, yc - 0.2 * h)]
                d = dist_polilinha(z, y, pts)
                if d < 0.42: return RAIO_CLARO if d < 0.18 else RAIO
            if y > y1 - 0.5: return tom((128, 128, 136), 0.05)
            if y < y0 + 0.35: return (100, 100, 108)
            if c["i"] in (0, c["tw"] - 1): return tom(base, -0.3)
            return tom(base, 0.06 * ruido(x, y, z, 0.6))
        return tom(base, -0.1)
    return f

def pena_cauda(nome, base, rot0, L, cores, raio=False, fase=0.0):
    """Tábua comprida da cauda (3 segmentos para trás que afinam até a ponta e caem um pouco)."""
    c0, cm, c1 = cores
    segs = [(0.45 * L, 1.3, 3.8, c0, cm), (0.33 * L, 1.15, 3.1, cm, c1), (0.22 * L, 0.95, 1.9, c1, c1)]
    return g.pena_curva(nome, base, segs, rot0, (5, 0, 0), "z",
                        lambda a, b, ei, inv: mat_pena_cauda(a, b, ei, inv, fase=fase, raio=raio and a != c1), res=4)

# ---------------- montagem ----------------
K_CAB, K_CAB_C = 1.3, (0.0, 27.6, -0.5)
def montar():
    i_cab, cab = montar_cabeca()
    g.transformar(i_cab, cab, K_CAB_C, k=K_CAB)          # cabeça um pouco maior (como o K_CAB do Pirococó)
    cab.append(montar_chapeu())
    cabeca = osso("cabeca", [0, 24.4, -0.4], [0, 0, 0], cab)
    pescoco = osso("pescoco", [0, 22.6, -0.3], [0, 0, 0], [
        peca("pescoco", [-2.3, 22.4, -2.4], [2.3, 25.0, 2.4], mat_luz(lambda p, f: CINZA_MEDIO, borda=.05)),
        cabeca])

    corpo = []
    mt = mat_luz(cor_torso, borda=.03, curva=.35)
    corpo += arredondado("torso", [-4.8, 16.0, -3.8], [4.8, 23.3, 3.4], mt, r=1.0, faixa=(14, 23.3), res=4)
    # cinto preto com o Símbolo Elétrico e o nó pendurado do lado esquerdo
    mcin = mat_luz(cor_cinto, borda=.08, curva=.2)
    corpo += arredondado("cinto", [-5.05, 15.5, -4.1], [5.05, 17.6, 3.65], mcin, r=0.5)
    corpo.append(peca("emblema", [-1.55, 15.0, -4.42], [1.55, 18.1, -4.02], mat_emblema(0, 16.55, 1.55), res=8, brilho=brilha))
    corpo.append(peca("no_faixa", [2.6, 15.0, -4.5], [3.8, 16.2, -3.9], mcin))
    corpo.append(peca("faixa_ponta1", [2.75, 11.6, -4.35], [3.35, 15.2, -4.0], mcin, rot=(0, 0, 6), pivo=(3.05, 15.2, -4.2)))
    corpo.append(peca("faixa_ponta2", [3.3, 12.4, -4.3], [3.85, 15.2, -3.95], mcin, rot=(0, 0, -8), pivo=(3.55, 15.2, -4.1)))
    # saia da túnica (abre um pouco embaixo)
    ms = mat_luz(cor_saia, borda=.03, curva=.35)
    corpo += arredondado("saia_alta", [-4.9, 11.6, -3.9], [4.9, 15.8, 3.5], ms, r=0.6, faixa=(6, 17), res=4, brilho=brilha)
    corpo += arredondado("saia_baixa", [-5.3, SAIA_Y0, -4.15], [5.3, 11.8, 3.75], ms, r=0.6, faixa=(6, 17), res=4, brilho=brilha)
    # embaixo da barra: miolo escuro escondido + franja curta de penas cinza recortadas em volta
    corpo.append(peca("saia_penas", [-4.0, 5.8, -3.0], [4.0, 7.3, 2.8], mat_luz(lambda p, f: GRAFITE, borda=.1)))
    FRANJA = [(-4.6, -2.6), (-2.3, -3.6), (0.0, -3.8), (2.3, -3.6), (4.6, -2.6), (-4.9, 0.6), (4.9, 0.6),
              (-3.6, 3.0), (0.0, 3.4), (3.6, 3.0)]
    for k, (x, z) in enumerate(FRANJA):
        phi = math.degrees(math.atan2(z, abs(x) + 0.01)) if abs(x) > 0.1 else (90 if z > 0 else -90)
        cores = ((70, 70, 78), (54, 54, 62), (40, 40, 48)) if k % 2 else ((46, 46, 54), (34, 34, 42), (24, 24, 30))
        lado = 1 if x >= 0 else -1
        corpo.append(osso(f"franja{k}", [x, 7.4, z], [0, -phi * lado, 0], [
            pena_bloco(f"franja{k}_p", (x, 7.4, z), (0, 0, 10 * lado), 2.6, 2.4, 0.9, cores, afina=(0.7, 0.4), afina_w=(0.6, 0.25))]))
    # penas das costas: ponta para baixo, saindo de baixo da túnica
    for k, (x, L) in enumerate([(-2.6, 6.6), (0.0, 7.6), (2.6, 6.6)]):
        corpo.append(g.pena_placa(f"costas{k}", (x, 12.6, 3.8 + 0.05 * k), (-8, 0, 0), L, 3.0, CINZAS_NUCA, eixo="x"))

    # ombreiras de armadura: placa de cima + placa caída por cima da asa (curva em 2 gomos), friso GROSSO de ouro,
    # miolo azul-escuro quase preto e raio de ouro; mais largas que a túnica
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((3.4 * lado, 7.5 * lado))
        topo = peca("ombreira_topo_" + s, [x0, 22.9, -4.3], [x1, 24.2, 3.9], mat_pauldron(lado, "topo"), res=4, brilho=brilha)
        xc0, xc1 = sorted((7.1 * lado, 10.3 * lado))
        caida = osso("ombreira_caida_" + s, [7.3 * lado, 24.2, -0.2], [0, 0, -24 * lado], [
            peca("ombreira_caida_" + s, [xc0, 22.95, -4.15], [xc1, 24.15, 3.75], mat_pauldron(lado, "caida"), res=4, brilho=brilha)])
        corpo.append(osso("ombro_" + s, [3.4 * lado, 24.2, -0.2], [0, 0, -14 * lado], [topo, caida]))

    # asas: penas cinza em bloco penduradas dos ombros (de frente parecem mangas de penas)
    ESCURA = ((84, 84, 92), (70, 70, 78), (58, 58, 66)); MEDIA = ((132, 132, 140), (150, 150, 158), (176, 176, 184))
    CLARA = ((178, 178, 186), (198, 198, 206), (222, 222, 228)); CLARA2 = ((160, 160, 168), (182, 182, 190), (208, 208, 214))
    PENAS_ASA = [  # (z, y raiz, comprimento, x, abertura, espessura, cores)
        (-1.4, 19.6, 11.6, 5.6, 6, 2.2, ESCURA), (1.4, 19.6, 11.2, 5.6, 8, 2.2, ESCURA),            # dentro (escura)
        (-2.2, 21.4, 5.8, 6.7, 6, 2.6, MEDIA), (-0.2, 21.6, 6.2, 6.8, 8, 2.6, MEDIA), (1.8, 21.4, 5.6, 6.7, 10, 2.6, MEDIA),
        (-2.5, 18.4, 6.8, 6.7, 10, 2.6, CLARA), (-0.8, 18.6, 7.4, 6.8, 13, 2.6, CLARA2), (0.9, 18.6, 7.0, 6.8, 15, 2.6, CLARA),
        (2.5, 18.2, 6.4, 6.6, 17, 2.4, CLARA2),
        (-2.8, 15.0, 7.6, 6.5, 14, 2.4, CLARA2), (-1.4, 15.2, 8.2, 6.6, 17, 2.4, CLARA), (0.0, 15.2, 7.8, 6.6, 20, 2.4, CLARA2),
        (1.4, 15.0, 8.0, 6.5, 23, 2.4, CLARA), (2.8, 14.8, 7.0, 6.4, 26, 2.2, CLARA2),
    ]
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = [pena_bloco(f"asa{k}_{s}", (x * lado, y0, z), (0, 0, fl * lado), L, 1.9, esp, cores, afina=(0.62, 0.3))
               for k, (z, y0, L, x, fl, esp, cores) in enumerate(PENAS_ASA)]
        corpo.append(osso("asa_" + s, [6.0 * lado, 21.0, 0], [0, 0, 0], asa))

    # cauda em leque denso: 8 penas largas que se sobrepõem (sem frestas), da parte baixa das costas para trás; as de
    # cima sobem em arco até perto da aba, as de baixo descem até o joelho. Grafite/preto com borda cinza média e raio
    # amarelo nas DUAS faces. Um tufo escuro cobre a raiz (de trás leem camadas, não blocos).
    ESC_C = ((22, 22, 28), (40, 40, 48), (64, 64, 72)); ESC2_C = ((48, 48, 56), (66, 66, 74), (90, 90, 98))
    MED_C = ((96, 96, 104), (122, 122, 130), (150, 150, 158)); CLA_C = ((140, 140, 148), (170, 170, 178), (204, 204, 210))
    CAUDA = [  # (rx, comprimento, ry (abertura em V), cores, raio)
        (-20, 13.0, 38, ESC_C, True), (-28, 13.6, -38, MED_C, False), (-36, 14.4, 32, ESC2_C, False),
        (-44, 15.4, -32, ESC_C, True), (-52, 16.2, 26, CLA_C, False), (-60, 17.0, -26, ESC_C, True),
        (-67, 17.4, 20, MED_C, False), (-75, 17.6, -20, ESC_C, True)]
    cauda = [pena_cauda(f"cauda{k}", (0.5 if ry > 0 else -0.5, 13.6, 3.4), (rx, ry, 0), L, cores, raio=r, fase=(-1) ** k)
             for k, (rx, L, ry, cores, r) in enumerate(CAUDA)]
    mraiz = mat_luz(lambda p, f: penas_costas(p[0], p[1], p[2]) if f != "up" else CINZA_ESC, borda=.08, curva=.3)
    cauda += arredondado("cauda_raiz", [-2.2, 11.6, 2.6], [2.2, 15.8, 4.8], mraiz, r=0.6)
    corpo.append(osso("cauda", [0, 13.6, 3.4], [0, 0, 0], cauda))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 9.0, 0], [0, 0, 0], corpo)

    # pernas amarelas grossas, pés de 3 dedos com garras escuras
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 2.5 * lado; zc = 0.4
        pp = []
        mam = mat_luz(lambda p, f: mix(AMARELO_P_ESC, AMARELO_P, clamp(p[1] / 3)) if f != "down" else AMARELO_P_ESC, borda=.12, curva=.4)
        def cor_canela(p, f):
            if (p[1] - 1.8) % 1.3 < 0.18: return AMARELO_P_ESC        # escamas
            return AMARELO_P
        pp.append(peca("coxa_" + s, [xc - 1.7, 6.2, zc - 1.7], [xc + 1.7, 8.4, zc + 1.7], mat_luz(lambda p, f: GRAFITE, borda=.1)))
        pp += octogono("canela_" + s, [xc - 1.4, 1.2, zc - 1.4], [xc + 1.4, 6.6, zc + 1.4], mat_luz(cor_canela, borda=.1, curva=.4), r=0.45, faixa=(0, 7))
        pp.append(peca("pe_" + s, [xc - 1.9, 0, zc - 2.0], [xc + 1.9, 1.6, zc + 1.6], mam, faixa=(0, 2)))
        mg = g.mat_facetado((92, 92, 100), (60, 60, 68), (52, 52, 60), (30, 30, 36))
        for nome, giro, dx in (("meio", 0, 0), ("fora", -18 * lado, 1.35 * lado), ("dentro", 18 * lado, -1.35 * lado)):
            x0, z0 = xc + dx, zc - 1.7
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .62, 0, z0 - 2.3], [x0 + .62, 1.3, z0 + 0.2], mam, faixa=(0, 2)),
                peca(f"garra_{nome}_{s}", [x0 - .68, 0, z0 - 3.3], [x0 + .68, 1.5, z0 - 2.2], mg)]))
        pp.append(peca("dedo_tras_" + s, [xc - .55, 0, zc + 1.2], [xc + .55, 1.1, zc + 2.6], mam, faixa=(0, 2)))
        pp.append(peca("garra_tras_" + s, [xc - .6, 0, zc + 2.5], [xc + .6, 1.3, zc + 3.4], mg))
        return osso("perna_" + s, [xc, 7.6, zc], [0, 0, 0], pp)

    for pc in g.PECAS:                                   # raios das penas da cauda brilham
        if pc.nome.startswith("cauda"): pc.brilho = brilha
    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

"""Cocórvolt (#006, Elétrico): galo cinza da tempestade, de chapéu cônico de palha, túnica azul-marinho com raios."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, arredondado, arredondado2, octogono

ID = "cocorvolt"; NOME = "Cocórvolt"; NUMERO = 6
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 29.6, -2.4), 7.0)
N_CAUDA = 10
ONDAS = [(f"cauda{k}", 3, (1.5, 1.0, 0.0)) for k in range(N_CAUDA)]
ANIM_PARADO = {
    "talisma_d": [(0, 0, 0), (4, 0, 6), (0, 0, 0), (-4, 0, -6), (0, 0, 0)],
    "talisma_e": [(0, 0, 0), (-4, 0, -6), (0, 0, 0), (4, 0, 6), (0, 0, 0)],
}
ANIM_ANDANDO = {
    "talisma_d": [(0, 0, 0), (10, 0, 12), (0, 0, 0), (-10, 0, -12), (0, 0, 0)],
    "talisma_e": [(0, 0, 0), (-10, 0, -12), (0, 0, 0), (10, 0, 12), (0, 0, 0)],
}

# ---------------- paleta (Paleta de Cores da ficha) ----------------
CINZA_CLARO = (214, 214, 218); CINZA = (142, 142, 148); CINZA_ESC = (64, 64, 68); CARVAO = (38, 40, 44)
CINZA_MEIO = (176, 176, 182); CINZA_MEIO2 = (108, 108, 116)
MARINHO = (40, 69, 132); AZUL = (45, 90, 182); MARINHO_ESC = (24, 36, 74); NAVY = (36, 53, 122)
OURO = (236, 180, 62); OURO_CLARO = (255, 222, 122); OURO_ESC = (150, 98, 30)
PALHA = (231, 174, 87); PALHA_CLARA = (240, 202, 132); PALHA_ESC = (170, 120, 58); PALHA_SOMBRA = (108, 78, 44)
TOPO_CHAPEU = (98, 88, 86); TRANCA = (150, 116, 82)
AMARELO_P = (240, 184, 32); ESCAMA = (220, 156, 26); AMARELO_P_CLARO = (255, 218, 86); AMARELO_P_ESC = (214, 146, 22)
BICO = (242, 181, 28); BICO_CLARO = (252, 204, 70); BICO_LADO = (236, 160, 24); BICO_BAIXO = (224, 138, 20)
VERMELHO = (212, 42, 36); VERMELHO_CLARO = (226, 56, 46); VERMELHO_ESC = (156, 26, 24)
# cores que brilham no escuro (devolvidas sem luz, para a _glowmask achar)
RAIO = (253, 220, 70); RAIO_CLARO = (255, 246, 170); RAIO_F = (245, 197, 24); RAIO_BORDA = (255, 224, 102)
OLHO_BORDA = (26, 63, 208); OLHO_AZUL = (47, 107, 255); OLHO_MIOLO = (226, 250, 255)
BRILHAM = {RAIO, RAIO_CLARO, RAIO_F, RAIO_BORDA, OLHO_BORDA, OLHO_AZUL, OLHO_MIOLO}
def brilha(c, cor): return tuple(cor[:3]) in BRILHAM

def tomf(c, f):
    """Luz NEUTRA (a de galo_base puxa a sombra para o roxo): f > 0 clareia para o branco, f < 0 escurece por
    igual, mantendo os cinzas frios da ficha."""
    f = clamp(f, -1, 1)
    if f >= 0: return mix(c, (255, 255, 255), f * 0.35)
    return tuple(int(round(v * (1 + f * 0.8))) for v in c)

def mat_luz(cor_fn, **kw):
    """Como g.mat_cor (com luz neutra); as cores da lista BRILHAM passam sem luz (a _glowmask reconhece)."""
    def f(c):
        base = cor_fn(c["p"], c["face"])
        if base is None: return None
        if base in BRILHAM: return base
        return tomf(base, g.contexto_luz(c, **kw))
    return f

def mat_degraus(cor, clareia=(0.0, 0.14, 0.26)):
    """Material por degrau de pena_degrau: a ponta fica mais clara (as pontas das penas da ficha são claras)."""
    def m(k): return mat_bloco(tomf(cor, clareia[min(k, len(clareia) - 1)]))
    m.por_degrau = True
    return m

def mat_bloco(cor, topo=.2, baixo=-.38, lado=0.0, frente=-.08, fio=-.22):
    """Bloco chapado em 3 tons (claro em cima, base, sombra embaixo) com fio escuro na borda: o 'voxel' da ficha."""
    def f(c):
        face = c["face"]
        t = topo if face == "up" else baixo if face == "down" else frente if face in ("north", "south") else lado
        if g.na_borda(c): t += fio
        return tomf(cor, t)
    return f

# ---------------- raio (glifo) ----------------
RAIO_POL = [(0.05, 1.0), (0.7, 1.0), (0.28, 0.16), (0.74, 0.16), (-0.46, -1.0), (-0.08, -0.1), (-0.56, -0.1)]
def no_poligono(u, v, pol):
    dentro = False
    n = len(pol)
    for k in range(n):
        (x1, y1), (x2, y2) = pol[k], pol[(k + 1) % n]
        if (y1 > v) != (y2 > v) and u < x1 + (v - y1) * (x2 - x1) / (y2 - y1): dentro = not dentro
    return dentro

def glifo_raio(u, v):
    """u, v em -1..1 (v para cima). Devolve RAIO_CLARO (miolo) / RAIO / None."""
    if not no_poligono(u, v, RAIO_POL): return None
    if no_poligono(u * 1.5 + 0.03, v * 1.15, RAIO_POL): return RAIO_CLARO
    return RAIO

def dist_polilinha(px, py, pts):
    melhor = 9e9
    for k in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[k], pts[k + 1]
        dx, dy = x2 - x1, y2 - y1
        t = clamp(((px - x1) * dx + (py - y1) * dy) / max(dx * dx + dy * dy, 1e-9))
        melhor = min(melhor, math.hypot(px - x1 - t * dx, py - y1 - t * dy))
    return melhor

def tri(t):
    """Onda triangular -1..1 de período 1."""
    t = t - math.floor(t)
    return 4 * t - 1 if t < 0.5 else 3 - 4 * t

# ---------------- pena em degraus (bloco grosso) ----------------
def pena_degrau(nome, raiz, rot, L, W, E, mat, dir="baixo", passos=(0.6, 0.25, 0.15), largura=(1.0, 0.7, 0.4),
                espessura=(1.0, 0.85, 0.7), brilho=False, res=None):
    """Pena GROSSA em 3 degraus que afinam até a ponta. dir='baixo': pende para -y (largura em z, espessura em x);
    dir='tras': cresce para +z (largura em y, espessura em x). 'mat' pode ser um material ou uma função (k) -> material."""
    x, y, z = raiz
    pecas, a = [], 0.0
    for k, (fl, fw, fe) in enumerate(zip(passos, largura, espessura)):
        h, w, e = L * fl, W * fw, E * fe
        m = mat(k) if callable(mat) and getattr(mat, "por_degrau", False) else mat
        if dir == "baixo":
            de, ate = [x - e / 2, y - a - h, z - w / 2], [x + e / 2, y - a, z + w / 2]
        else:
            de, ate = [x - e / 2, y - w / 2, z + a], [x + e / 2, y + w / 2, z + a + h]
        pecas.append(peca(f"{nome}_{k}", de, ate, m, brilho=brilho, res=res))
        a += h - 0.04
    return osso(nome, list(raiz), list(rot), pecas)

# ---------------- cabeça ----------------
CAB_X, CAB_Z0, CAB_Z1 = 3.3, -4.6, 3.4          # meia largura, frente e nuca do crânio
CAB_Y0, CAB_Y1 = 23.2, 32.4
FAC_A = 46.0                                     # ângulo da faceta do olho em relação à frente (graus)
FAC_XF = 0.6                                     # meia largura da frente achatada (onde nasce o bico)
FAC_T = 1.4
_ca, _sa = math.cos(math.radians(FAC_A)), math.sin(math.radians(FAC_A))
FAC_LEN = (CAB_X - FAC_XF) / _ca
FAC_ZS = CAB_Z0 + FAC_LEN * _sa                  # onde a faceta encontra o lado
FAC_M = ((FAC_XF + CAB_X) / 2, (CAB_Z0 + FAC_ZS) / 2)
FAC_C = (FAC_M[0] - _sa * FAC_T / 2, FAC_M[1] + _ca * FAC_T / 2)   # centro da peça (para dentro da normal)
FAC_RY = 90 - FAC_A
OLHO_Y, OLHO_U = 30.1, -0.05
BICO_DY = -0.5

CARA = (198, 198, 202); CARA_BAIXO = (156, 156, 162)

def cor_cara(y):
    """Cor da cara pela altura: testa cinza-carvão (sombra da aba e penas da sobrancelha), cara clara, queixo médio."""
    if y > OLHO_Y + 0.62: return CINZA_ESC
    return CARA if y > 25.0 else CARA_BAIXO

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return CINZA_ESC
    if z > 0.8 or face == "south": return CINZA if y < 31.6 else CINZA_ESC
    return cor_cara(y)

def olho_volt(u, v):
    """Olho eletrificado: fenda estreita, com a borda de cima descendo para o bico (u negativo = bico); borda azul
    elétrica, azul saturado e miolo branco-ciano brilhante (a ficha mostra o miolo quase branco), órbita carvão."""
    W2, H0, H1 = 1.35, -0.38, 0.42
    topo = H1 - 0.34 * (1 - u / W2) * 0.5
    if abs(u) > W2 + 0.25 or v < H0 - 0.25 or v > topo + 0.5: return None
    if abs(u) > W2 or v < H0 or v > topo:
        if abs(u) < W2 + 0.13 and H0 - 0.13 < v < topo + 0.13: return OLHO_BORDA      # halo elétrico
        return (44, 46, 54) if v > H0 - 0.05 else (96, 96, 104)
    du, dv = (W2 - abs(u)) / W2, min(v - H0, topo - v) / (topo - H0)
    d = min(du * 2.2, dv * 2.4)
    if d < 0.3: return OLHO_BORDA
    if d < 0.62: return OLHO_AZUL
    return OLHO_MIOLO

def mat_faceta(lado):
    """Face diagonal do rosto com o olho inteiro na face de fora."""
    fora = "east" if lado > 0 else "west"
    cx, cz = FAC_C[0] * lado, FAC_C[1]
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            cor = olho_volt(z - cz - OLHO_U, y - OLHO_Y)
            if cor is not None: return cor
        if c["face"] == "up": return CINZA_ESC
        return tomf(cor_cara(y), g.contexto_luz(c, borda=.0, curva=.25))
    return f

def cor_bico(p, face):
    """Bico amarelo-laranja uniforme, mais claro em cima, sombra laranja embaixo (sem marrom)."""
    x, y, z = p
    if face == "down": return BICO_BAIXO
    if face in ("east", "west") and abs(z - (CAB_Z0 - 0.7)) < 0.22 and abs(y - 29.2) < 0.18: return (196, 112, 16)  # narina
    if y > 29.3: return BICO_CLARO
    return mix(BICO, BICO_BAIXO, clamp((28.4 - y) / 1.6))

def mat_tufo(cor):
    return mat_bloco(cor, topo=.12, baixo=-.25, frente=-.03, fio=-.07)

def mat_suave(cor):
    """Pena 'suave' (Fase 6): luz contínua e fio escuro fraco, para as telhas vizinhas se fundirem."""
    return mat_bloco(cor, topo=.12, baixo=-.25, frente=-.03, fio=-.07)

def pena_lisa(nome, raiz, rot, L, W, E, cor, ponta=0.38, estreita=0.55):
    """Pena GRANDE em 2 peças (corpo + ponta mais estreita), pendurada para -y; deitada sobre a superfície pelo 'rot'."""
    return pena_degrau(nome, raiz, rot, L, W, E, mat_suave(cor), dir="baixo", passos=(1 - ponta, ponta),
                       largura=(1.0, estreita), espessura=(1.0, 0.8), res=4)

def tufo_pontudo(nome, raiz, rot, L, W, E, cor):
    """Tufo triangular: 3 degraus que afinam até uma ponta (largura 1 -> 0,55 -> 0,2), crescendo para +z."""
    return pena_degrau(nome, raiz, rot, L, W, E, mat_tufo(cor), dir="tras", passos=(0.45, 0.33, 0.22),
                       largura=(1.0, 0.55, 0.2), espessura=(1.0, 0.85, 0.7), res=4)

def montar_cabeca():
    cab = []
    mc = mat_luz(cor_cabeca, borda=.0, curva=.25)
    F = (CAB_Y0, CAB_Y1)
    # crânio: bloco de trás (lados e nuca) + frente estreita; as quinas da frente são as facetas do olho
    cab += arredondado2("cranio", [-CAB_X, CAB_Y0, FAC_ZS - 0.05], [CAB_X, CAB_Y1, CAB_Z1], mc, r=1.3, faixa=F, res=4)
    cab.append(peca("cranio_frente", [-FAC_XF - 0.05, CAB_Y0 + 0.4, CAB_Z0], [FAC_XF + 0.05, CAB_Y1, FAC_ZS], mc, faixa=F, res=4))
    # miolo atrás do V (fecha o vão entre as facetas, sem aparecer por fora)
    cab.append(peca("cranio_miolo", [-1.6, CAB_Y0 + 0.5, CAB_Z0 + 1.2], [1.6, CAB_Y1 - 0.2, FAC_ZS + 0.2], mc, faixa=F, res=2))
    # quilha: ponte em losango entre os olhos, descendo da testa até o alto do bico
    cab.append(osso("quilha", [0, 30.6, CAB_Z0 + 0.15], [0, 45, 0], [
        peca("quilha", [-0.55, 29.4, CAB_Z0 - 0.4], [0.55, 32.0, CAB_Z0 + 0.7], mc, faixa=F, res=4)]))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(osso("faceta_" + s, [cx, OLHO_Y, cz], [0, FAC_RY * lado, 0], [
            peca("faceta_" + s, [cx - FAC_T / 2, CAB_Y0 + 0.3, cz - FAC_LEN / 2], [cx + FAC_T / 2, CAB_Y1, cz + FAC_LEN / 2],
                 mat_faceta(lado), rot=(0, 0, -5 * lado), pivo=(cx, OLHO_Y, cz), faixa=F, res=8, brilho=brilha)]))
        # sobrancelha: penas cinza-carvão RENTES à face, logo acima do olho, descendo para o bico
        x0, x1 = sorted((cx + (FAC_T / 2 - 0.15) * lado, cx + (FAC_T / 2 + 0.12) * lado))
        cab.append(osso("sobrancelha_" + s, [cx, OLHO_Y, cz], [0, FAC_RY * lado, 0], [
            peca("sobrancelha_" + s, [x0, OLHO_Y + 0.6, cz - FAC_LEN / 2 - 0.05], [x1, OLHO_Y + 1.1, cz + FAC_LEN / 2 + 0.1],
                 mat_bloco(CINZA_ESC, topo=.0, fio=-.05), rot=(-9, 0, -3 * lado), pivo=(cx, OLHO_Y + 0.9, cz), res=4)]))
    # bico: cunha LARGA e curta (~1/3 da cabeça de largura e de projeção), topo reto com narina, gancho na ponta
    i_bico = len(g.PECAS)
    mb = mat_luz(cor_bico, borda=.04, curva=.15)
    fb = (26.6, 30.2)
    zb = CAB_Z0 + 0.3
    BICO_ = [  # (meia largura, y0, y1, avanço)
        (1.45, 29.25, 30.05, 3.0), (1.15, 28.5, 29.35, 2.6), (0.8, 27.8, 28.6, 1.8)]
    for k, (w, y0, y1, d) in enumerate(BICO_):
        cab.append(peca(f"bico_{k}", [-w, y0, zb - d], [w, y1, zb + 1.0], mb, faixa=fb, res=4))
    cab.append(peca("bico_gancho", [-0.6, 27.9, zb - 3.45], [0.6, 29.9, zb - 2.6], mb, rot=(-12, 0, 0),
                    pivo=(0, 29.9, zb - 2.6), faixa=fb, res=4))
    # barbela: 2 lóbulos estreitos e juntos, logo abaixo do bico (o da esquerda de quem olha mais comprido)
    mbar = mat_luz(lambda p, f: mix(VERMELHO_ESC, VERMELHO, clamp((p[1] - 22.4) / 3.6)), borda=.06, curva=.15)
    zw = zb - 0.9
    for lado, y_fim in ((-1, 25.1), (1, 24.3)):   # o lóbulo da esquerda de quem olha (x+) é o mais comprido
        x0, x1 = sorted((0.08 * lado, 1.4 * lado))
        cab += arredondado("barbela_" + ("d" if lado < 0 else "e"), [x0, y_fim, zw - 0.8], [x1, 27.9, zw + 0.8], mbar,
                           r=0.35, res=4)
    g.transformar(i_bico, [], (0, 0, 0), k=1.0, sobe=BICO_DY)   # bico e barbela descem: o alto do bico na base do olho
    # bochechas: 3 penas GRANDES por lado, deitadas no lado da cabeça (face larga para fora), apontando para trás e
    # para baixo, sobrepostas em telha; a de baixo desce até o pescoço
    BOCHECHA = [  # (y, z, comprimento, largura, para trás, abertura, cor)
        (31.5, -1.6, 6.8, 4.0, 40, 5, (194, 194, 200)), (29.4, -0.8, 7.0, 4.0, 35, 6, (178, 178, 184)),
        (27.3, 0.2, 6.4, 3.8, 30, 5, (156, 156, 162))]
    for k, (y, z, L, W, tras, fl, cor) in enumerate(BOCHECHA):
        for lado in (-1, 1):
            s = "d" if lado < 0 else "e"
            cab.append(pena_lisa(f"bochecha{k}_{s}", ((CAB_X - 0.35) * lado, y, z), (-tras, 0, fl * lado), L, W, 0.9, cor))
    # nuca: 3 penas grandes deitadas sobre a nuca e o pescoço (face larga para trás), descendo até a capa
    for k, (x, y, L, W, cor) in enumerate([(0.0, 32.0, 8.6, 4.2, (150, 150, 156)), (-2.3, 30.6, 7.4, 3.4, (134, 134, 140)),
                                           (2.3, 30.6, 7.4, 3.4, (134, 134, 140))]):
        raiz = (x, y, CAB_Z1 - 0.1 + 0.25 * (k > 0))
        cab.append(osso(f"nuca{k}", list(raiz), [-12, 0, 6 * x / 2.3], [osso(f"nuca{k}_g", list(raiz), [0, 90, 0], [
            pena_lisa(f"nuca{k}_p", raiz, (0, 0, 0), L, W, 1.1, cor)])]))
    return cab

# ---------------- chapéu cônico ----------------
CH_APICE, CH_ABA, CH_R, CH_Z, CH_N, CH_T = 38.3, 33.2, 11.6, 0.8, 16, 1.5
CH_INCL = -4                                          # a aba desce na frente
CH_ALFA = math.atan2(CH_APICE - CH_ABA, CH_R)
CH_S = math.hypot(CH_APICE - CH_ABA, CH_R)
CH_FAIXA = 0.74 * CH_S                                # daqui para fora, a aba de palha bege
CARVAO_FRIO = (69, 70, 76)
# 5 rachaduras de raio separadas, em coordenadas (ângulo em voltas, s/CH_S): cantos vivos, terminam em ponta
RACHAS = [[(0.02, 0.20), (0.06, 0.34), (0.03, 0.40), (0.08, 0.58)],
          [(0.19, 0.30), (0.24, 0.36), (0.22, 0.48), (0.28, 0.52), (0.26, 0.66)],
          [(0.40, 0.18), (0.43, 0.32), (0.39, 0.42), (0.45, 0.60)],
          [(0.58, 0.34), (0.63, 0.40), (0.61, 0.50), (0.67, 0.56), (0.66, 0.68)],
          [(0.79, 0.22), (0.82, 0.36), (0.78, 0.44), (0.84, 0.62)]]

def mat_chapeu(k):
    """Cone carvão-frio com nervuras de palha, 5 rachaduras de raio separadas (cantos vivos, brilham), aba bege
    grossa com tábuas."""
    yaw = 2 * math.pi * k / CH_N
    tg = math.tan(math.pi / CH_N)
    def meia(s): return s * math.cos(CH_ALFA) * tg + 0.06
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        s = CH_Z - z                                       # distância do ápice pela geratriz
        if face in ("up", "down") and abs(x) > meia(s): return None
        if face in ("east", "west"): return None           # as emendas ficam cobertas pelo gomo vizinho
        if face == "down": return tomf(mix(PALHA_ESC, PALHA, clamp(s / CH_S)), -0.1)
        if face == "north":                                # beirada GROSSA da aba, com tábuas
            return (201, 164, 99) if c["i"] % 6 == 0 else tomf(PALHA_CLARA, -0.08 if c["j"] in (0, c["th"] - 1) else 0.06)
        if face == "south": return PALHA_CLARA
        borda_lado = meia(s) - abs(x)
        if s > CH_FAIXA:                                   # aba de palha: tábuas com emendas
            cor = PALHA_CLARA if s > CH_FAIXA + 0.35 else PALHA_ESC
            if borda_lado < 0.14 or abs(x) < 0.08: cor = (201, 164, 99)
            return cor
        if s < 0.9: return PALHA_CLARA
        volta = (yaw + math.atan2(x, max(s * math.cos(CH_ALFA), 1e-6))) / (2 * math.pi)
        circ = 2 * math.pi * s * math.cos(CH_ALFA)         # para medir a distância em unidades
        for pts in RACHAS:
            q = [(((a - volta + 0.5) % 1.0 - 0.5) * circ, b * CH_S) for a, b in pts]
            d = dist_polilinha(0.0, s, q)
            if d < 0.36:
                ponta = math.hypot(q[-1][0], s - q[-1][1]) < 1.2 or math.hypot(q[0][0], s - q[0][1]) < 1.0
                if not ponta or d < 0.2: return RAIO_F if d > 0.1 else RAIO_BORDA
            if d < 0.62: return (150, 120, 60)             # brilho em volta da rachadura
        cor = CARVAO_FRIO
        if borda_lado < 0.14: cor = (104, 92, 78)          # nervura de palha entre os painéis
        return cor
    return f

def mat_talisma(cx, cy, W, H):
    """Talismã: moldura de ouro, fundo escuro e raio amarelo brilhando nas duas faces largas."""
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        if face not in ("north", "south"):
            return tomf(OURO, -0.25 if face == "down" else 0.1 if face == "up" else -0.05)
        u = (x - cx) / (W / 2); v = (y - cy) / (H / 2)
        if face == "south": u = -u
        bx, by = (1 - abs(u)) * W / 2, (1 - abs(v)) * H / 2
        b = min(bx, by)
        if b < 0.1: return OURO_ESC
        if b < 0.45: return mix(OURO_CLARO, OURO, clamp((0.6 - v) / 1.4))
        if b < 0.55: return OURO_ESC
        r = glifo_raio(u / 0.78, v / 0.78)
        if r: return r
        return (34, 36, 46)
    return f

def montar_chapeu():
    filhos = []
    for k in range(CH_N):
        yaw = 360 * k / CH_N
        w = CH_S * math.cos(CH_ALFA) * math.tan(math.pi / CH_N) + 0.1
        filhos.append(osso(f"chapeu_gomo{k}", [0, CH_APICE, CH_Z], [0, yaw, 0], [
            peca(f"chapeu_gomo{k}", [-w, CH_APICE - CH_T, CH_Z - CH_S], [w, CH_APICE, CH_Z], mat_chapeu(k),
                 rot=(-math.degrees(CH_ALFA), 0, 0), pivo=(0, CH_APICE, CH_Z), res=5, brilho=brilha)]))
    filhos += octogono("chapeu_ponta", [-1.9, CH_APICE - 1.7, CH_Z - 1.9], [1.9, CH_APICE + 0.4, CH_Z + 1.9],
                       mat_suave(PALHA_CLARA), r=0.6)   # botão tan que cobre o encontro dos gomos
    # talismãs: logo abaixo da aba, quase sob a borda, presos por uma alça curta de ouro (ossos próprios p/ balançar)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x = 9.8 * lado
        aba = CH_ABA + (CH_APICE - CH_ABA) * (1 - 9.8 / CH_R) - CH_T / math.cos(CH_ALFA)
        H, W = 6.5, 3.4
        cy = aba - 0.9 - H / 2
        filhos.append(osso("talisma_" + s, [x, aba, CH_Z], [0, 0, 0], [osso("talisma_prumo_" + s, [x, aba, CH_Z], [-CH_INCL, -22 * lado, 0], [
            peca("talisma_alca_" + s, [x - 0.45, cy + H / 2 - 0.1, CH_Z - 0.3], [x + 0.45, aba + 0.2, CH_Z + 0.3], mat_bloco(OURO)),
            peca("talisma_" + s, [x - W / 2, cy - H / 2, CH_Z - 0.25], [x + W / 2, cy + H / 2, CH_Z + 0.25],
                 mat_talisma(x, cy, W, H), res=8, brilho=brilha)])]))
    return osso("chapeu", [0, CH_ABA, CH_Z], [CH_INCL, 0, 0], filhos)

# ---------------- túnica ----------------
Y_CINTO0, Y_CINTO1 = 16.0, 18.4
TORSO_Z0, TORSO_Z1 = -4.0, 3.9

def navy_blocos(x, y, z, base=MARINHO):
    """Tecido navy com blocos de 1,2 um tom mais escuros (como os 'pixels' grandes da ficha)."""
    h = math.sin(math.floor(x / 1.2) * 12.99 + math.floor(y / 1.2) * 78.23 + math.floor(z / 1.2) * 37.72) * 43758.5
    return mix(base, (28, 46, 98), 0.55) if h - math.floor(h) < 0.3 else base

def cor_torso(p, face):
    x, y, z = p
    ax = abs(x)
    if face == "south":
        return OURO if y < Y_CINTO1 + 0.55 else navy_blocos(x, y, z, AZUL if y > 21 else MARINHO)   # capa navy, barra de ouro
    if face == "north":
        d = ax - 0.52 * (y - Y_CINTO1 + 0.4)
        if d < 0: return CARVAO                          # quimono preto por baixo (V)
        if d < 1.25: return CINZA_ESC                    # gola larga (~2 px)
        if d < 1.6: return OURO                          # debrum de ouro da lapela
        return navy_blocos(x, y, z, AZUL if y > 21 else MARINHO)
    if face == "up":
        if ax < 2.6: return CARVAO
        return AZUL
    return navy_blocos(x, y, z, AZUL if y > 21 else MARINHO)

def cor_saia(p, face):
    x, y, z = p
    if face == "down": return MARINHO_ESC
    if y < 10.95: return OURO                            # barra de ouro onde a túnica acaba (como na lateral da ficha)
    return navy_blocos(x, y, z)

def cor_painel(p, face):
    """Painel único do traje: navy com moldura de ouro e UM raio angular (ϟ, 2 dobras, cantos vivos), grosso em cima
    e terminando em ponta fina embaixo, ~60% da largura do painel; amarelo saturado com borda clara, brilha."""
    x, y, z = p
    if face != "north": return OURO
    u, v = x / 2.4, (y - 11.6) / 4.3
    if abs(u) > 0.82 or v > 0.96 or v < -0.97: return OURO
    if no_poligono(u / 0.62, v / 0.86, RAIO_POL):
        return RAIO_F if no_poligono(u / 0.62 * 1.18 + 0.02, v / 0.86 * 1.06, RAIO_POL) else RAIO_BORDA
    return navy_blocos(x, y, z, (30, 44, 96))

def cor_cinto(p, face):
    x, y, z = p
    if y > Y_CINTO1 - 0.28 or y < Y_CINTO0 + 0.28: return OURO     # filetes de ouro em cima e embaixo
    t = (y - Y_CINTO0) / 0.8
    if t - math.floor(t) < 0.16: return (24, 24, 28)                 # dobras da faixa
    return (52, 52, 56) if face == "up" else CARVAO

def mat_emblema(cx, cy, R):
    """Símbolo Elétrico: octógono de ouro de aro grosso, fundo escuro e raio amarelo grande."""
    def f(c):
        x, y, z = c["p"]
        if c["face"] != "north":
            return tomf(OURO, -0.2 if c["face"] in ("east", "west", "down") else 0.05)
        u, v = (x - cx) / R, (y - cy) / R
        d = max(abs(u), abs(v), (abs(u) + abs(v)) / 1.32)
        if d > 1.0: return None
        if d > 0.93: return OURO_ESC
        if d > 0.66: return mix(OURO_CLARO, OURO, clamp((0.4 - v) / 1.2))
        if d > 0.6: return OURO_ESC
        r = glifo_raio(u / 0.52, v / 0.52)
        if r: return r
        return (30, 30, 38)
    return f

ZIGUES_OMB = [[(-0.62, 0.42), (-0.3, 0.42), (-0.42, -0.02), (-0.1, -0.02)],
              [(0.08, 0.06), (0.4, 0.06), (0.28, -0.38), (0.62, -0.38)]]

def mat_ombreira_solida(lado, parte, caixa):
    """Placa de armadura cheia e chanfrada: fundo azul-marinho quase preto (#1e2440) e UM friso de ouro grosso que
    contorna a placa inteira (medido na caixa do grupo, não em cada sub-bloco, para os chanfros não virarem molduras
    empilhadas); na face de fora da placa principal, dois zigue-zagues de ouro de 3 segmentos."""
    fora = "east" if lado > 0 else "west"
    FUNDO = (30, 36, 64)
    (X0, Y0, Z0), (X1, Y1, Z1) = caixa
    def f(c):
        face = c["face"]
        if face == "down": return tomf(FUNDO, -0.3)
        x, y, z = c["p"]
        if face in ("east", "west"): b = min(y - Y0, Y1 - y, z - Z0, Z1 - z)
        elif face in ("north", "south"): b = min(y - Y0, Y1 - y, abs(x) - min(abs(X0), abs(X1)), max(abs(X0), abs(X1)) - abs(x))
        else: b = min(z - Z0, Z1 - z, abs(x) - min(abs(X0), abs(X1)), max(abs(X0), abs(X1)) - abs(x))
        if b < 0.12: return OURO_ESC
        if b < 0.62: return tomf(OURO, 0.1 if face == "up" else 0.0)
        if parte == "placa" and face == fora:
            u = (z - (Z0 + Z1) / 2) / ((Z1 - Z0) / 2) * (-1 if lado > 0 else 1)
            v = ((y - Y0) / (Y1 - Y0)) * 2 - 1
            if any(dist_polilinha(u, v, zz) < 0.09 for zz in ZIGUES_OMB): return OURO_CLARO
        return tomf(FUNDO, 0.15 if face == "up" else 0.0)
    return f

# ---------------- montagem ----------------
PERNA_EXTRA = 2.0      # pernas mais compridas, como na arte conceitual (o corpo todo sobe)

def montar():
    i_corpo = len(g.PECAS)
    cab = montar_cabeca()
    cab.append(montar_chapeu())
    cabeca = osso("cabeca", [0, 24.0, -0.6], [0, 0, 0], cab)
    pescoco = osso("pescoco", [0, 22.4, -0.4], [0, 0, 0], [
        *octogono("pescoco", [-2.1, 22.0, -2.3], [2.1, 25.0, 2.6], mat_suave(CINZA_ESC), r=0.7), cabeca])

    corpo = []
    # peito da túnica (azul-marinho, gola em V preta com fio de ouro); costas navy com barra de ouro
    mt = mat_luz(cor_torso, borda=.06, curva=.3)
    corpo += arredondado("torso", [-4.4, Y_CINTO1 - 0.4, TORSO_Z0], [4.4, 23.4, TORSO_Z1], mt, r=0.8, faixa=(16, 23.4), res=4)
    # faixa preta (obi) com filetes de ouro, o Símbolo Elétrico grande e o nó com duas pontas (à direita de quem olha)
    mcin = mat_luz(cor_cinto, borda=.05, curva=.2)
    corpo += arredondado("cinto", [-4.7, Y_CINTO0, TORSO_Z0 - 0.3], [4.7, Y_CINTO1, TORSO_Z1 + 0.3], mcin, r=0.5, res=4)
    R_EMB = 2.05
    corpo.append(peca("emblema", [-R_EMB, 17.2 - R_EMB, TORSO_Z0 - 0.8], [R_EMB, 17.2 + R_EMB, TORSO_Z0 - 0.3],
                      mat_emblema(0, 17.2, R_EMB), res=8, brilho=brilha))
    mno = mat_bloco(CARVAO, topo=.25)
    # (na prévia de frente, x negativo fica à DIREITA de quem olha)
    corpo.append(peca("no_faixa", [-3.95, 16.3, TORSO_Z0 - 0.95], [-2.35, 17.9, TORSO_Z0 - 0.25], mno))
    corpo.append(peca("faixa_ponta1", [-3.7, 12.2, TORSO_Z0 - 0.8], [-3.0, 16.4, TORSO_Z0 - 0.35], mno,
                      rot=(0, 0, -6), pivo=(-3.35, 16.4, TORSO_Z0 - 0.55)))
    corpo.append(peca("faixa_ponta2", [-3.0, 12.9, TORSO_Z0 - 0.75], [-2.35, 16.4, TORSO_Z0 - 0.3], mno,
                      rot=(0, 0, 8), pivo=(-2.7, 16.4, TORSO_Z0 - 0.5)))
    # saia da túnica: navy em blocos, sem listras, com barra de ouro onde acaba; painel único na frente
    ms = mat_luz(cor_saia, borda=.06, curva=.3)
    corpo += arredondado("saia", [-4.7, 10.4, TORSO_Z0 - 0.2], [4.7, Y_CINTO0 + 0.1, TORSO_Z1 + 0.15], ms, r=0.6,
                         faixa=(7, 17), res=4)
    corpo.append(peca("painel", [-2.4, 7.2, TORSO_Z0 - 0.75], [2.4, 16.05, TORSO_Z0 - 0.2],
                      mat_luz(cor_painel, borda=.03, curva=.2), faixa=(7, 17), res=6, brilho=brilha))
    # saia de penas cinza sob a túnica (dos lados e atrás; na frente fica o avental): 7 penas grandes deitadas
    for k in range(7):
        ang = math.radians(-45 + 270 * k / 6)
        x, z = 4.5 * math.cos(ang), 0.4 + 3.9 * math.sin(ang)
        yaw = -math.degrees(ang) + 90
        cor = (118, 118, 124) if k % 2 else (104, 104, 112)
        corpo.append(osso(f"saiote{k}", [x, 10.8, z], [0, yaw, 0], [
            pena_lisa(f"saiote{k}_p", (x, 10.8, z), (0, 0, 8), 4.4, 3.8, 1.0, cor)]))

    # ombreiras: placa de armadura CHEIA encostada no tronco, topo inclinado ~15° para fora, e um degrau mais baixo
    # cobrindo o braço (as duas peças se tocam; nada flutua)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((3.4 * lado, 7.6 * lado))
        placa = arredondado("ombreira_" + s, [x0, 19.2, -3.5], [x1, 23.6, 3.9],
                            mat_ombreira_solida(lado, "placa", ([x0, 19.2, -3.5], [x1, 23.6, 3.9])), r=0.6, res=4)
        xb0, xb1 = sorted((6.0 * lado, 8.2 * lado))
        degrau = octogono("ombreira_braco_" + s, [xb0, 16.6, -3.2], [xb1, 20.4, 3.6],
                          mat_ombreira_solida(lado, "degrau", ([xb0, 16.6, -3.2], [xb1, 20.4, 3.6])), r=0.6, res=4)
        corpo.append(osso("ombro_" + s, [3.4 * lado, 23.6, 0.2], [0, 0, -15 * lado], [
            *placa, osso("ombro_braco_" + s, [6.6 * lado, 20.4, 0.2], [0, 0, 10 * lado], degrau)]))

    # asas: MANGAS de pena largas, quase verticais, encostadas na lateral da túnica: 3 camadas de telhas, cada uma
    # com 4 penas pontudas (serrilhado), viradas para a frente e para fora; claras em cima, médias embaixo
    CAMADAS = [(21.0, 6.6, (178, 178, 184)), (17.0, 6.8, (158, 158, 164)), (13.0, 7.0, (136, 136, 142))]
    TELHAS = [(5.0, -2.2), (5.9, 0.1), (6.7, 2.4)]
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        for r, (yr, L, cor) in enumerate(CAMADAS):
            for k, (x, z) in enumerate(TELHAS):
                x_ = (x + 0.15 * r) * lado
                asa.append(osso(f"asa{r}{k}_{s}", [x_, yr, z], [0, 24 * lado, (4 + 2 * r) * lado], [
                    pena_lisa(f"asa{r}{k}_{s}_p", (x_, yr, z), (0, 0, 0), L - 0.4 * (k % 2), 3.6, 1.2, cor, estreita=0.7)]))
        corpo.append(osso("asa_" + s, [5.0 * lado, 21.0, 0.2], [0, 0, 0], asa))

    # capa de penas das costas (dos dois lados da cauda), abaixo da capa navy
    for r, (y, L, cor) in enumerate([(17.8, 5.6, (180, 180, 184)), (13.6, 5.8, (150, 150, 156))]):
        for k, x in enumerate((-3.8, 0.0, 3.8)):
            raiz = (x, y, TORSO_Z1 + 0.2 + 0.3 * r)
            corpo.append(osso(f"capa{r}{k}", list(raiz), [-8, 0, 6 * x / 3.8], [osso(f"capa{r}{k}_g", list(raiz), [0, 90, 0], [
                pena_lisa(f"capa{r}{k}_p", raiz, (0, 0, 0), L, 4.0, 1.1, cor)])]))

    # cauda: leque CURVO de penas largas que afinam em lâmina, sobrepostas sem vão, da altura do joelho até perto
    # dos olhos; um tom por pena, carvão e cinza-claro alternados; rachadura de raio grossa em cada pena carvão
    cauda = []
    n = N_CAUDA
    for k in range(n):
        t = k / (n - 1)
        ang = 32 - 76 * t
        y = 18.6 - 5.4 * t
        L = [16.0, 17.4, 18.4, 19.0, 19.5, 19.5, 19.0, 18.0, 16.8, 15.5][k]
        x = 0.4 * (1 if k % 4 in (1, 2) else -1)
        escura = k % 2 == 0
        cor = (58, 58, 62) if escura else (168, 168, 172)
        cauda.append(pena_cauda(f"cauda{k}", (x, y, TORSO_Z1 - 0.8), (-ang, 3 * (1 if x > 0 else -1), 0), L, cor,
                                raio=escura))
    corpo.append(osso("cauda", [0, 16.0, TORSO_Z1 - 0.8], [0, 0, 0], cauda))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 8.5, 0.4], [0, 0, 0], corpo)
    g.transformar(i_corpo, [tronco], (0, 0, 0), k=1.0, sobe=PERNA_EXTRA)

    # pernas amarelo-ouro com faixas de escama, pés largos de 3 dedos com garras pretas
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 3.0 * lado; zc = 0.2
        pp = []
        pp += octogono("coxa_" + s, [xc - 1.9, 5.2 + PERNA_EXTRA, zc - 1.9], [xc + 1.9, 8.8 + PERNA_EXTRA, zc + 1.9],
                       mat_suave(CARVAO), r=0.7)
        mam = mat_bloco(AMARELO_P, topo=.16, baixo=-.22, fio=-.08)
        def cor_canela(p, f):
            if (p[1] - 1.6) % 1.1 < 0.22: return ESCAMA
            return AMARELO_P
        pp += arredondado("canela_" + s, [xc - 1.7, 1.4, zc - 1.7], [xc + 1.7, 6.2 + PERNA_EXTRA, zc + 1.7],
                          mat_luz(cor_canela, borda=.03, curva=.15), r=0.6, faixa=(1.4, 6.2 + PERNA_EXTRA))
        # tornozelo chanfrado ligando a canela ao pé
        pp += octogono("tornozelo_" + s, [xc - 2.0, 1.2, zc - 2.0], [xc + 2.0, 2.6, zc + 1.6], mam, r=0.8)
        pp += arredondado("pe_" + s, [xc - 2.2, 0, zc - 2.3], [xc + 2.2, 1.7, zc + 1.8], mam, r=0.45)
        mg = mat_bloco(CARVAO, topo=.25, fio=-.05)
        for nome, giro, dx in (("meio", 0, 0), ("fora", -16 * lado, 1.4 * lado), ("dentro", 16 * lado, -1.4 * lado)):
            x0, z0 = xc + dx, zc - 2.0
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .7, 0, z0 - 1.6], [x0 + .7, 1.5, z0 + 0.2], mam),
                # ponta do dedo em cunha (desce para a frente)
                peca(f"dedo_ponta_{nome}_{s}", [x0 - .5, 0, z0 - 2.7], [x0 + .5, 1.2, z0 - 1.5], mam, rot=(10, 0, 0),
                     pivo=(x0, 1.2, z0 - 1.5)),
                # garra curva: base e ponta inclinadas para baixo
                peca(f"garra_{nome}_{s}", [x0 - .38, 0.15, z0 - 3.5], [x0 + .38, 0.95, z0 - 2.55], mg, rot=(28, 0, 0),
                     pivo=(x0, 0.95, z0 - 2.55))]))
        pp.append(peca("dedo_tras_" + s, [xc - .55, 0, zc + 1.4], [xc + .55, 1.0, zc + 2.9], mam, rot=(-12, 0, 0),
                       pivo=(xc, 1.0, zc + 1.4)))
        pp.append(peca("garra_tras_" + s, [xc - .35, 0.1, zc + 2.8], [xc + .35, 0.8, zc + 3.6], mg, rot=(-25, 0, 0),
                       pivo=(xc, 0.8, zc + 2.8)))
        return osso("perna_" + s, [xc, 7.6 + PERNA_EXTRA, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

RACHA_CAUDA = [(0.18, 1.3), (0.4, 1.0), (0.36, 2.0), (0.6, 1.7), (0.56, 2.5), (0.74, 2.2)]   # (fração, fundo)

def mat_pena_cauda(cor, z0, Lt, topo, raio):
    """Pena da cauda de UM tom (face de cima um pouco mais clara, fio escuro na borda); nas penas carvão, uma
    rachadura de raio grossa e brilhante, com cantos vivos."""
    pts = [(z0 + f * Lt, topo - d) for f, d in RACHA_CAUDA]
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        if face == "up": return tomf(cor, 0.16)
        if face == "down": return tomf(cor, -0.3)
        if face in ("east", "west"):
            if raio:
                d = dist_polilinha(z, y, pts)
                if d < 0.3: return RAIO_F if d > 0.1 else RAIO_BORDA
            if g.na_borda(c): return tomf(cor, -0.08)
            return cor
        return tomf(cor, -0.08)
    return f

def pena_cauda(nome, base, rot0, Lt, cor, raio=False):
    """Pena da cauda em LÂMINA: 3 segmentos (ossos nome_0..2) que afinam em altura e espessura (4,2 -> 3 -> 1,8) até a
    ponta e CURVAM PARA CIMA 6° por segmento; o eixo de cada segmento fica no meio da altura (sem degrau solto)."""
    x, y, z0 = base
    H = [5.0, 4.4, 3.5]; F = [0.44, 0.33, 0.23]; W = [2.4, 2.2, 1.9]
    topo = y + H[0] / 2
    m = mat_pena_cauda(cor, z0, Lt, topo, raio)
    def seg(k, pz):
        L = F[k] * Lt
        meio = y + (H[0] - H[k]) * 0.25                  # afina mais por baixo: a lâmina sobe um pouco
        filhos = [peca(f"{nome}_{k}", [x - W[k] / 2, meio - H[k] / 2, pz], [x + W[k] / 2, meio + H[k] / 2, pz + L], m, res=4,
                       brilho=brilha if raio else False)]
        if k + 1 < 3: filhos.append(seg(k + 1, pz + L - 0.6))
        return osso(f"{nome}_{k}", [x, y, pz], list(rot0) if k == 0 else [-8, 0, 0], filhos)
    return seg(0, z0)

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

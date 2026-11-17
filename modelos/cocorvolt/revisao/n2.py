"""Cocórvolt (#006, Elétrico): galo cinza da tempestade, de chapéu cônico de palha, túnica azul-marinho com raios."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, arredondado, arredondado2, octogono

ID = "cocorvolt"; NOME = "Cocórvolt"; NUMERO = 6
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 28.4, -3.2), 7.4)
N_CAUDA = 7
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
CINZA_CLARO = (217, 213, 210); CINZA = (143, 138, 138); CINZA_ESC = (64, 64, 64); CARVAO = (38, 40, 44)
CINZA_MEIO = (176, 172, 172)
MARINHO = (40, 69, 132); AZUL = (45, 90, 182); MARINHO_ESC = (24, 36, 74)
OURO = (236, 180, 62); OURO_CLARO = (255, 222, 122); OURO_ESC = (150, 98, 30)
PALHA = (231, 174, 87); PALHA_CLARA = (240, 202, 132); PALHA_ESC = (170, 120, 58); PALHA_SOMBRA = (108, 78, 44)
TOPO_CHAPEU = (66, 62, 62)
AMARELO_P = (250, 196, 40); AMARELO_P_CLARO = (255, 218, 86); AMARELO_P_ESC = (214, 146, 22)
BICO = (253, 204, 52); BICO_LADO = (246, 176, 28); BICO_BAIXO = (232, 140, 14)
VERMELHO = (205, 35, 29); VERMELHO_CLARO = (232, 64, 44); VERMELHO_ESC = (140, 20, 22)
# cores que brilham no escuro (devolvidas sem luz, para a _glowmask achar)
RAIO = (253, 220, 70); RAIO_CLARO = (255, 246, 170)
OLHO_BORDA = (30, 110, 246); OLHO_AZUL = (70, 168, 255); OLHO_MIOLO = (196, 240, 255)
BRILHAM = {RAIO, RAIO_CLARO, OLHO_BORDA, OLHO_AZUL, OLHO_MIOLO}
def brilha(c, cor): return tuple(cor[:3]) in BRILHAM

def mat_luz(cor_fn, **kw):
    """Como g.mat_cor, mas as cores da lista BRILHAM passam sem luz (a _glowmask reconhece)."""
    def f(c):
        base = cor_fn(c["p"], c["face"])
        if base is None: return None
        if base in BRILHAM: return base
        return tom(base, g.contexto_luz(c, **kw))
    return f

def mat_bloco(cor, topo=.2, baixo=-.38, lado=0.0, frente=-.08, fio=-.22):
    """Bloco chapado em 3 tons (claro em cima, base, sombra embaixo) com fio escuro na borda: o 'voxel' da ficha."""
    def f(c):
        face = c["face"]
        t = topo if face == "up" else baixo if face == "down" else frente if face in ("north", "south") else lado
        if g.na_borda(c): t += fio
        return tom(cor, t)
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
CAB_X, CAB_Z0, CAB_Z1 = 4.2, -4.6, 3.4          # meia largura, frente e nuca do crânio
CAB_Y0, CAB_Y1 = 23.2, 32.9
FAC_A = 34.0                                     # ângulo da faceta do olho em relação à frente (graus)
FAC_XF = 1.2                                     # meia largura da frente achatada (onde nasce o bico)
FAC_T = 1.4
_ca, _sa = math.cos(math.radians(FAC_A)), math.sin(math.radians(FAC_A))
FAC_LEN = (CAB_X - FAC_XF) / _ca
FAC_ZS = CAB_Z0 + FAC_LEN * _sa                  # onde a faceta encontra o lado
FAC_M = ((FAC_XF + CAB_X) / 2, (CAB_Z0 + FAC_ZS) / 2)
FAC_C = (FAC_M[0] - _sa * FAC_T / 2, FAC_M[1] + _ca * FAC_T / 2)   # centro da peça (para dentro da normal)
FAC_RY = 90 - FAC_A
OLHO_Y, OLHO_U = 30.0, -0.05

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return CINZA_ESC
    if z > 1.2 or face == "south": return mix(CINZA, CINZA_MEIO, clamp((y - 25) / 6))
    if y > 31.4: return mix(CINZA, CINZA_ESC, clamp((y - 31.4) / 1.2))     # sombra da aba
    return CINZA_CLARO if y > 25.2 else CINZA_MEIO

def olho_volt(u, v):
    """Olho eletrificado da ficha: retângulo azul brilhante (miolo quase branco), com a borda de cima descendo para
    o bico (u negativo = bico), e órbita escura em volta. Devolve a cor ou None (fora da órbita)."""
    W2, H0, H1 = 1.2, -0.48, 0.5
    topo = H1 - 0.34 * (1 - u / W2) * 0.5 * 2 * 0.5      # mais baixo do lado do bico
    if abs(u) > W2 + 0.3 or v < H0 - 0.25 or v > topo + 0.55: return None
    if abs(u) > W2 or v < H0 or v > topo:
        return (40, 42, 50) if v > H0 - 0.05 else (78, 78, 84)
    du, dv = (W2 - abs(u)) / W2, min(v - H0, topo - v) / (topo - H0)
    d = min(du * 2.2, dv * 2.4)
    if d < 0.35: return OLHO_BORDA
    if d < 0.75: return OLHO_AZUL
    return OLHO_MIOLO

def mat_faceta(lado):
    """Face diagonal do rosto com o olho inteiro na face de fora; a sobrancelha é uma peça à parte."""
    fora = "east" if lado > 0 else "west"
    cx, cz = FAC_C[0] * lado, FAC_C[1]
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            cor = olho_volt(z - cz - OLHO_U, y - OLHO_Y)
            if cor is not None: return cor
        base = CINZA_ESC if y > OLHO_Y + 0.55 else CINZA_CLARO if y > 25.2 else CINZA_MEIO
        if c["face"] != fora: base = CINZA_CLARO
        return tom(base, g.contexto_luz(c, borda=.0, curva=.25))
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return BICO_BAIXO
    if face in ("east", "west") and abs(z + 6.0) < 0.25 and abs(y - 29.1) < 0.2: return (150, 84, 20)   # narina
    if face == "up": return mix(BICO, (255, 228, 120), 0.4)
    return mix(BICO, BICO_LADO, clamp((29.6 - y) / 2.0)) if face in ("east", "west") else BICO

def tufo(nome, raiz, yaw, desce, L, W, E, cor, lado):
    """Tufo de pena em bloco grosso (2 degraus) preso na cabeça, apontando para trás (+z), aberto 'yaw' graus para
    fora e inclinado 'desce' graus para baixo."""
    return pena_degrau(nome, raiz, (desce, yaw * lado, 0), L, W, E, mat_bloco(cor), dir="tras",
                       passos=(0.62, 0.38), largura=(1.0, 0.6), espessura=(1.0, 0.8), res=4)

def montar_cabeca():
    cab = []
    mc = mat_luz(cor_cabeca, borda=.0, curva=.25)
    F = (CAB_Y0, CAB_Y1)
    # crânio: bloco de trás (lados e nuca) + frente achatada estreita; as quinas da frente são as facetas do olho
    cab += arredondado("cranio", [-CAB_X, CAB_Y0, FAC_ZS - 0.2], [CAB_X, CAB_Y1, CAB_Z1], mc, r=0.7, faixa=F, res=4)
    cab.append(peca("cranio_frente", [-FAC_XF - 0.05, CAB_Y0 + 0.4, CAB_Z0], [FAC_XF + 0.05, CAB_Y1, FAC_ZS], mc, faixa=F, res=4))
    cab.append(peca("cranio_miolo", [-CAB_X + 1.0, CAB_Y0 + 0.2, CAB_Z0 + 0.9], [CAB_X - 1.0, CAB_Y1, FAC_ZS + 0.5], mc,
                    faixa=F, res=2))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, CAB_Y0 + 0.3, cz - FAC_LEN / 2], [cx + FAC_T / 2, CAB_Y1 - 0.05, cz + FAC_LEN / 2],
                        mat_faceta(lado), rot=(0, FAC_RY * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=F, res=8, brilho=brilha))
        # sobrancelha: aba grossa cinza-escura por cima do olho, descendo para o bico (cara séria)
        x0, x1 = sorted((cx + (FAC_T / 2 - 0.1) * lado, cx + (FAC_T / 2 + 0.75) * lado))
        cab.append(osso("sobrancelha_" + s, [cx, OLHO_Y, cz], [0, FAC_RY * lado, 0], [
            peca("sobrancelha_" + s, [x0, OLHO_Y + 0.5, cz - FAC_LEN / 2 - 0.2], [x1, OLHO_Y + 1.35, cz + FAC_LEN / 2 + 0.3],
                 mat_bloco(CINZA_ESC, topo=.25), rot=(-14, 0, 0), pivo=(cx, OLHO_Y + 0.9, cz), res=4)]))
    # bico: cunha grossa em degraus (base larga ~ metade da cara), cumeeira inclinada e gancho para baixo
    mb = mat_luz(cor_bico, borda=.1, curva=.25)
    fb = (26.5, 30.2)
    BICO_ = [(1.8, 27.3, 29.9, -5.7, CAB_Z0 + 0.3), (1.45, 27.3, 29.45, -6.7, -5.6), (1.1, 27.25, 28.9, -7.5, -6.6)]
    for k, (w, y0, y1, z0, z1) in enumerate(BICO_):
        cab.append(peca(f"bico_{k}", [-w, y0, z0], [w, y1, z1], mb, faixa=fb, res=4))
    cab.append(peca("bico_cume", [-1.3, 29.45, -7.7], [1.25, 30.1, CAB_Z0 + 0.2], mb, rot=(-17, 0, 0),
                    pivo=(0, 30.1, CAB_Z0 + 0.2), faixa=fb, res=4))
    cab.append(peca("bico_gancho", [-0.85, 26.4, -8.15], [0.85, 28.6, -7.3], mb, rot=(-22, 0, 0), pivo=(0, 28.6, -7.3),
                    faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-1.3, 26.55, -6.8], [1.25, 27.35, CAB_Z0 + 0.3], mat_bloco(BICO_BAIXO, topo=0), res=4))
    # barbela: dois lobos vermelhos arredondados pendurados sob o bico (o direito mais comprido)
    mbar = mat_luz(lambda p, f: mix(VERMELHO_ESC, VERMELHO_CLARO, clamp((p[1] - 22.4) / 4.6)), borda=.1, curva=.2)
    cab.append(peca("barbela_raiz", [-1.35, 25.6, -5.9], [1.35, 26.8, -4.4], mbar, res=4))
    cab += arredondado("barbela_d", [-1.5, 22.3, -6.0], [-0.05, 26.0, -4.5], mbar, r=0.35, res=4)
    cab += arredondado("barbela_e", [0.05, 23.2, -5.85], [1.4, 26.0, -4.5], mbar, r=0.35, res=4)
    # tufos em bloco: bochechas claras abrindo para trás e para fora, tufos médios atrás, nuca escura
    TUFOS = [  # (y, z, yaw, desce, L, W, cor)
        (30.6, -1.8, 46, 6, 4.0, 2.2, CINZA_CLARO), (28.6, -1.4, 50, 14, 4.6, 2.4, CINZA_CLARO),
        (26.6, -1.0, 50, 22, 4.4, 2.4, CINZA_CLARO), (24.6, -0.4, 44, 32, 3.6, 2.2, CINZA_MEIO),
        (31.2, 1.4, 26, 10, 4.0, 2.4, CINZA_MEIO), (29.0, 1.8, 26, 20, 4.4, 2.4, CINZA), (26.8, 2.1, 24, 30, 3.8, 2.2, CINZA)]
    for k, (y, z, yaw, desce, L, W, cor) in enumerate(TUFOS):
        for lado in (-1, 1):
            cab.append(tufo(f"tufo{k}_{'d' if lado < 0 else 'e'}", ((CAB_X - 0.5) * lado, y, z), yaw, desce, L, W, 1.3, cor, lado))
    for k, (x, y, desce, L) in enumerate([(0.0, 31.0, 18, 3.6), (-1.6, 29.0, 30, 3.8), (1.6, 29.0, 30, 3.8), (0.0, 26.8, 42, 3.4)]):
        cab.append(pena_degrau(f"nuca{k}", (x, y, CAB_Z1 - 0.6), (desce, 0, 0), L, 2.4, 1.6, mat_bloco(CINZA_ESC if k % 3 else CINZA),
                               dir="tras", passos=(0.62, 0.38), largura=(1.0, 0.6), espessura=(1.0, 0.8), res=4))
    return cab

# ---------------- chapéu cônico de palha ----------------
CH_APICE, CH_ABA, CH_R, CH_Z, CH_N, CH_T = 39.0, 32.4, 12.3, -0.6, 16, 0.9
CH_INCL = -6                                          # a aba desce na frente
CH_ALFA = math.atan2(CH_APICE - CH_ABA, CH_R)
CH_S = math.hypot(CH_APICE - CH_ABA, CH_R)

def mat_chapeu(k):
    yaw = 2 * math.pi * k / CH_N
    tg = math.tan(math.pi / CH_N)
    def meia(s): return s * math.cos(CH_ALFA) * tg + 0.06
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        s = CH_Z - z                                       # distância do ápice pela geratriz
        if face in ("up", "down") and abs(x) > meia(s): return None
        if face in ("east", "west"): return None           # as emendas ficam cobertas pelo gomo vizinho
        if face == "down":
            return tom(mix(PALHA_SOMBRA, PALHA_ESC, clamp(s / CH_S)), 0.0)
        if face == "north": return tom(PALHA_CLARA, -0.3 if c["j"] in (0, c["th"] - 1) else 0.05)   # beirada da aba
        if face == "south": return PALHA_ESC
        borda_lado = meia(s) - abs(x)
        phi = (yaw + math.atan2(x, max(s * math.cos(CH_ALFA), 1e-6))) * 6 / (2 * math.pi)
        sz = 6.6 + 1.1 * tri(phi)                          # anel de raio em zigue-zague (grosso, brilha)
        if abs(s - sz) < 0.5: return RAIO_CLARO if abs(s - sz) < 0.2 else RAIO
        if s > CH_S - 1.0:                                 # faixa clara da aba
            return tom(PALHA_CLARA, 0.06 if borda_lado > 0.15 else -0.12)
        if s < sz:                                         # topo escuro, com raios menores
            if s < 1.0: return PALHA
            q = s / sz
            if abs(x) < 0.32 and 0.25 < q < 0.85 and k % 2 == 0: return RAIO
            cor = TOPO_CHAPEU if borda_lado > 0.18 else tom(TOPO_CHAPEU, -0.35)
            return tom(cor, 0.1 * (1 - q))
        cor = mix(PALHA, PALHA_CLARA, clamp((s - sz) / 4.5))
        if borda_lado < 0.18: cor = tom(cor, -0.18)
        anel = (s - sz) / 1.6
        if anel - math.floor(anel) < 0.14: cor = tom(cor, -0.1)
        return cor
    return f

def mat_talisma(cx, cy, W, H):
    """Talismã: moldura de ouro, fundo escuro e raio amarelo brilhando nas duas faces largas."""
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        if face not in ("north", "south"):
            return tom(OURO, -0.25 if face == "down" else 0.1 if face == "up" else -0.05)
        u = (x - cx) / (W / 2); v = (y - cy) / (H / 2)
        if face == "south": u = -u
        bx, by = (1 - abs(u)) * W / 2, (1 - abs(v)) * H / 2
        b = min(bx, by)
        if b < 0.1: return OURO_ESC
        if b < 0.45: return mix(OURO_CLARO, OURO, clamp((0.6 - v) / 1.4))
        if b < 0.55: return OURO_ESC
        r = glifo_raio(u / 0.6, v / 0.66)
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
    filhos.append(peca("chapeu_ponta", [-0.8, CH_APICE - 0.5, CH_Z - 0.8], [0.8, CH_APICE + 0.5, CH_Z + 0.8],
                       mat_bloco(PALHA_CLARA)))
    # talismãs pendurados na aba (ossos próprios para balançar), de frente como na ficha
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x = 9.6 * lado
        topo = CH_ABA + (CH_APICE - CH_ABA) * (1 - 9.6 / CH_R) - 0.3
        cy, H, W = 27.4, 5.8, 3.3
        filhos.append(osso("talisma_" + s, [x, topo, CH_Z], [0, 0, 0], [
            peca("talisma_cordao_" + s, [x - 0.2, cy + H / 2 - 0.1, CH_Z - 0.2], [x + 0.2, topo + 0.3, CH_Z + 0.2], mat_bloco(OURO_ESC)),
            peca("talisma_argola_" + s, [x - 0.6, cy + H / 2 - 0.1, CH_Z - 0.4], [x + 0.6, cy + H / 2 + 0.5, CH_Z + 0.4], mat_bloco(OURO)),
            peca("talisma_" + s, [x - W / 2, cy - H / 2, CH_Z - 0.35], [x + W / 2, cy + H / 2, CH_Z + 0.35],
                 mat_talisma(x, cy, W, H), res=8, brilho=brilha)]))
    return osso("chapeu", [0, CH_ABA, CH_Z], [CH_INCL, 0, 0], filhos)

# ---------------- túnica ----------------
Y_CINTO0, Y_CINTO1 = 16.0, 18.4
TORSO_Z0, TORSO_Z1 = -3.1, 3.9

def cor_torso(p, face):
    x, y, z = p
    ax = abs(x)
    if face == "south":
        if ax < 2.4: return CINZA if (y // 1.6) % 2 else CINZA_MEIO     # manto de penas das costas (faixas largas)
        return MARINHO
    if face == "north":
        d = ax - 0.52 * (y - Y_CINTO1 + 0.4)
        if d < 0: return CARVAO                          # quimono preto por baixo (V)
        if d < 0.55: return CINZA_ESC                    # gola
        if d < 1.05: return OURO                         # friso da lapela
        return AZUL if y > 21 else MARINHO
    if face == "up":
        if ax < 2.6: return CARVAO
        return AZUL
    return AZUL if y > 21 else MARINHO

def cor_saia(p, face, y0, z0):
    x, y, z = p
    ax = abs(x)
    if face == "down": return MARINHO_ESC
    if y < y0 + 0.6: return OURO                         # barra dourada
    if face == "north":
        if ax < 2.6:                                     # painel da frente: moldura de ouro e o raio (Padrão do Traje)
            if ax > 2.1 or y > Y_CINTO0 - 0.6: return OURO
            r = glifo_raio(x / 1.55, (y - 11.6) / 3.9)
            if r: return r
            return MARINHO_ESC
        if 3.5 < ax < 4.0: return OURO                   # beirada da túnica
        return MARINHO
    if face == "up": return MARINHO
    if face == "south" and ax < 2.4: return CINZA_ESC
    return MARINHO

def cor_cinto(p, face):
    x, y, z = p
    t = (y - Y_CINTO0) / 0.8
    if t - math.floor(t) < 0.16: return (24, 24, 28)                 # dobras da faixa
    return (52, 50, 54) if face == "up" else CARVAO

def mat_emblema(cx, cy, R):
    """Símbolo Elétrico: octógono de ouro com fundo escuro e raio amarelo."""
    def f(c):
        x, y, z = c["p"]
        if c["face"] != "north":
            return tom(OURO, -0.2 if c["face"] in ("east", "west", "down") else 0.05)
        u, v = (x - cx) / R, (y - cy) / R
        d = max(abs(u), abs(v), (abs(u) + abs(v)) / 1.32)
        if d > 1.0: return None
        if d > 0.92: return OURO_ESC
        if d > 0.7: return mix(OURO_CLARO, OURO, clamp((0.4 - v) / 1.2))
        if d > 0.64: return OURO_ESC
        r = glifo_raio(u / 0.56, v / 0.56)
        if r: return r
        return (30, 30, 38)
    return f

def mat_ombreira(lado, parte):
    """Ombreira: friso de ouro grosso em volta da face larga, miolo azul-escuro; na placa do lado, dois raios
    pequenos de ouro (como na vista lateral da ficha)."""
    larga = ("up",) if parte == "topo" else (("east",) if lado > 0 else ("west",))
    def f(c):
        face = c["face"]
        i, j, tw, th = c["i"], c["j"], c["tw"], c["th"]
        if face not in larga:
            if face in ("down", "west" if lado > 0 else "east"): return tom(MARINHO_ESC, -0.2)
            return tom(OURO, 0.1 if face == "up" else -0.1)
        b = min(i, tw - 1 - i, j, th - 1 - j) / 4.0
        if b < 0.12: return OURO_ESC
        if b < 0.7: return tom(OURO, 0.1)
        if b < 0.82: return OURO_ESC
        x, y, z = c["p"]
        (x0, y0, z0), (x1, y1, z1) = c["b"]
        if parte == "caida":
            v = (y - y0) / (y1 - y0)
            if v > 0.72: return AZUL
            u = (z - (z0 + z1) / 2) / ((z1 - z0) / 2) * (-1 if lado > 0 else 1)
            for uc in (-0.42, 0.42):
                r = glifo_raio((u - uc) / 0.3, (v - 0.38) / 0.26)
                if r: return OURO_CLARO if r == RAIO_CLARO else OURO
            return (22, 28, 52)
        return tom(MARINHO, 0.1)
    return f

# ---------------- montagem ----------------
CLARO = (206, 202, 200); MEDIO = (150, 146, 146); ESCURO = (92, 90, 92)

def montar():
    cab = montar_cabeca()
    cab.append(montar_chapeu())
    cabeca = osso("cabeca", [0, 24.0, -0.6], [0, 0, 0], cab)
    pescoco = osso("pescoco", [0, 22.4, -0.4], [0, 0, 0], [
        peca("pescoco", [-2.4, 22.0, -2.4], [2.4, 24.6, 2.6], mat_bloco(CINZA)), cabeca])

    corpo = []
    # peito da túnica (azul-marinho, gola em V preta com friso de ouro)
    mt = mat_luz(cor_torso, borda=.06, curva=.3)
    corpo += arredondado("torso", [-4.4, Y_CINTO1 - 0.4, TORSO_Z0], [4.4, 23.4, TORSO_Z1], mt, r=0.8, faixa=(16, 23.4), res=4)
    # faixa preta (obi) com o Símbolo Elétrico e o nó do lado esquerdo
    mcin = mat_luz(cor_cinto, borda=.1, curva=.2)
    corpo += arredondado("cinto", [-4.7, Y_CINTO0, TORSO_Z0 - 0.3], [4.7, Y_CINTO1, TORSO_Z1 + 0.3], mcin, r=0.5, res=4)
    corpo.append(peca("emblema", [-1.75, 15.45, TORSO_Z0 - 0.75], [1.75, 18.95, TORSO_Z0 - 0.3], mat_emblema(0, 17.2, 1.75),
                      res=8, brilho=brilha))
    corpo.append(peca("no_faixa", [2.6, 16.2, TORSO_Z0 - 0.75], [3.8, 17.6, TORSO_Z0 - 0.2], mat_bloco(CARVAO)))
    corpo.append(peca("faixa_ponta1", [2.7, 12.6, TORSO_Z0 - 0.6], [3.3, 16.4, TORSO_Z0 - 0.25], mat_bloco(CARVAO),
                      rot=(0, 0, 6), pivo=(3.0, 16.4, TORSO_Z0 - 0.4)))
    corpo.append(peca("faixa_ponta2", [3.3, 13.4, TORSO_Z0 - 0.55], [3.85, 16.4, TORSO_Z0 - 0.2], mat_bloco(CARVAO),
                      rot=(0, 0, -8), pivo=(3.55, 16.4, TORSO_Z0 - 0.4)))
    # saia da túnica em 2 andares (abre um pouco embaixo)
    for nome, x, y0, y1, z0, z1 in (("saia_alta", 4.6, 11.8, Y_CINTO0 + 0.1, TORSO_Z0 - 0.15, TORSO_Z1 + 0.15),
                                    ("saia_baixa", 5.0, 7.6, 12.0, TORSO_Z0 - 0.45, TORSO_Z1 + 0.45)):
        ms = mat_luz(lambda p, f, y0=y0, z0=z0: cor_saia(p, f, y0, z0), borda=.06, curva=.3)
        corpo += arredondado(nome, [-x, y0, z0], [x, y1, z1], ms, r=0.6, faixa=(7, 17), res=4, brilho=brilha)
    # penas escuras saindo de baixo da túnica (blocos com ponta em degrau)
    for k in range(10):
        ang = math.radians(-90 + 36 * k + 18)
        x, z = 4.3 * math.cos(ang), 0.4 + 3.6 * math.sin(ang)
        yaw = -math.degrees(ang) + 90
        cor = CARVAO if k % 2 else (84, 82, 86)
        corpo.append(osso(f"saiote{k}", [x, 8.2, z], [0, yaw, 0], [
            pena_degrau(f"saiote{k}_p", (x, 8.2, z), (0, 0, 0), 3.2, 2.6, 1.0, mat_bloco(cor), dir="baixo",
                        passos=(0.6, 0.4), largura=(1.0, 0.55), espessura=(1.0, 0.8))]))

    # ombreiras: placa de cima inclinada + placa caída do lado (cúpula azul em cima, raios de ouro), friso de ouro
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((3.0 * lado, 7.9 * lado))
        topo = peca("ombreira_topo_" + s, [x0, 22.4, TORSO_Z0 - 0.5], [x1, 23.7, TORSO_Z1 + 0.5], mat_ombreira(lado, "topo"),
                    res=4, brilho=brilha)
        xc0, xc1 = sorted((7.6 * lado, 8.6 * lado))
        caida = osso("ombreira_caida_" + s, [8.0 * lado, 23.0, 0.4], [0, 0, 5 * lado], [
            peca("ombreira_caida_" + s, [xc0, 16.4, TORSO_Z0 - 0.5], [xc1, 22.4, TORSO_Z1 + 0.7], mat_ombreira(lado, "caida"), res=4),
            peca("ombreira_cupula_" + s, [xc0 + 0.05, 22.3, TORSO_Z0 + 0.6], [xc1 - 0.05, 23.4, TORSO_Z1 - 0.4],
                 mat_bloco(OURO), res=4)])
        corpo.append(osso("ombro_" + s, [3.0 * lado, 23.7, 0.4], [0, 0, -14 * lado], [topo, caida]))

    # asas: 3 camadas de penas grossas em degrau penduradas dos ombros; as de baixo, mais escuras e compridas,
    # abrem mais para fora (de frente a silhueta alarga para baixo, como na ficha)
    CAMADAS = [  # (x raiz, y raiz, comprimento, abertura, cor, zs)
        (5.7, 17.6, 10.8, 21, ESCURO, (-2.0, 0.6, 3.2)),
        (6.4, 19.0, 10.0, 15, MEDIO, (-3.0, -0.4, 2.2, 4.4)),
        (7.0, 20.4, 8.6, 9, CLARO, (-2.3, 0.3, 2.9)),
    ]
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        for c_, (xr, yr, L, fl, cor, zs) in enumerate(CAMADAS):
            for k, z in enumerate(zs):
                yaw = (26 if z < -1.5 else -14 if z > 2.5 else 0) * lado
                asa.append(osso(f"asa{c_}{k}_{s}", [xr * lado, yr, z], [0, yaw, 0], [
                    pena_degrau(f"asa{c_}{k}_{s}_p", (xr * lado, yr, z), (0, 0, fl * lado), L - 0.5 * (k % 2), 2.9, 1.5,
                                mat_bloco(cor), dir="baixo", passos=(0.62, 0.24, 0.14), largura=(1.0, 0.68, 0.36))]))
        corpo.append(osso("asa_" + s, [6.0 * lado, 21.0, 0.4], [0, 0, 0], asa))

    # cauda: 6 penas largas e grossas em leque, das costas (altura do ombro até o quadril) para trás; as de cima quase
    # na horizontal, as de baixo caindo; carvão e cinza médio alternados, com raio amarelo nas faces largas
    CAUDA = [  # (y raiz, ângulo para baixo, comprimento, x)
        (23.5, -14, 13.0, -1.2), (21.8, -5, 15.0, 1.2), (20.0, 4, 16.0, -1.2), (18.2, 13, 15.5, 1.2),
        (16.4, 23, 14.5, -1.2), (14.6, 34, 12.5, 1.2), (12.8, 46, 10.0, -1.2)]
    cauda = []
    for k, (y, a, L, x) in enumerate(CAUDA):
        escura = k % 2 == 0
        cores = (CARVAO, (58, 58, 62), (86, 84, 88)) if escura else ((96, 94, 98), (124, 120, 122), (150, 146, 146))
        segs = [(0.5 * L, 2.6, 4.2, cores[0], cores[1]), (0.3 * L, 2.3, 3.4, cores[1], cores[2]),
                (0.2 * L, 2.0, 2.2, cores[2], cores[2])]
        cauda.append(g.pena_curva(f"cauda{k}", (x, y, TORSO_Z1 - 0.6), segs, (a, 0, 0), (4, 0, 0), "z",
                                  lambda c0, c1, ei, inv, k=k: mat_pena_cauda(c0, c1, k), res=4))
    corpo.append(osso("cauda", [0, 18.0, TORSO_Z1 - 0.6], [0, 0, 0], cauda))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 8.5, 0.4], [0, 0, 0], corpo)

    # pernas amarelas grossas, pés largos de 3 dedos com garras pretas
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 2.6 * lado; zc = 0.2
        pp = []
        pp.append(peca("coxa_" + s, [xc - 1.8, 5.4, zc - 1.8], [xc + 1.8, 8.6, zc + 1.8], mat_bloco(CARVAO)))
        mam = mat_bloco(AMARELO_P, topo=.18, baixo=-.3)
        pp += octogono("canela_" + s, [xc - 1.5, 1.5, zc - 1.5], [xc + 1.5, 6.0, zc + 1.5], mat_bloco(AMARELO_P), r=0.45)
        pp.append(peca("pe_" + s, [xc - 2.1, 0, zc - 2.2], [xc + 2.1, 1.8, zc + 1.8], mam))
        mg = mat_bloco(CARVAO, topo=.3)
        for nome, giro, dx in (("meio", 0, 0), ("fora", -14 * lado, 1.45 * lado), ("dentro", 14 * lado, -1.45 * lado)):
            x0, z0 = xc + dx, zc - 2.0
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .7, 0, z0 - 2.2], [x0 + .7, 1.4, z0 + 0.2], mam),
                peca(f"garra_{nome}_{s}", [x0 - .75, 0, z0 - 3.4], [x0 + .75, 1.5, z0 - 2.15], mg)]))
        pp.append(peca("dedo_tras_" + s, [xc - .65, 0, zc + 1.6], [xc + .65, 1.2, zc + 3.0], mam))
        pp.append(peca("garra_tras_" + s, [xc - .7, 0, zc + 2.9], [xc + .7, 1.3, zc + 4.0], mg))
        return osso("perna_" + s, [xc, 7.6, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

def mat_pena_cauda(c0, c1, k):
    """Pena da cauda: faces largas chapadas (escura ou média), face de cima clara, e um raio amarelo GROSSO em Z
    nas faces largas das penas pares (Cauda Energizada)."""
    def f(c):
        (x0, y0, z0), (x1, y1, z1) = c["b"]
        x, y, z = c["p"]
        face = c["face"]
        t = clamp((z - z0) / max(z1 - z0, 1e-6))
        base = mix(c0, c1, t)
        if face == "up": return tom(mix(base, (150, 146, 146), 0.6), 0.15)
        if face == "down": return tom(base, -0.35)
        if face in ("east", "west"):
            if k % 2 == 0 or k == 3:
                h, L = y1 - y0, z1 - z0
                yc = (y0 + y1) / 2
                pts = [(z0 + 0.05 * L, yc + 0.28 * h), (z0 + 0.55 * L, yc + 0.18 * h), (z0 + 0.45 * L, yc - 0.18 * h),
                       (z0 + 1.0 * L, yc - 0.26 * h)]
                d = dist_polilinha(z, y, pts)
                if d < 0.36: return RAIO_CLARO if d < 0.14 else RAIO
            if g.na_borda(c): return tom(base, -0.25)
            if y > y1 - 0.45: return tom(base, 0.18)
            return base
        return tom(base, -0.12)
    return f

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

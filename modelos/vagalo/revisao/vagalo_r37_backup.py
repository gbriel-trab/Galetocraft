"""Vagaló (#009, Elétrico): galo-vaga-lume veloz, roxo-escuro, com asas de inseto douradas e lanterna que brilha."""
import math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, PRETO

ID = "vagalo"; NOME = "Vagaló"; NUMERO = 9
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 26.0, -2.0), 7.0)
ONDAS = [("cauda0", 4, (3, 0, 0))]

# ---------------- paleta (Paleta de Cores da ficha) ----------------
ROXO_ESC = (52, 36, 68); ROXO = (88, 66, 112); ROXO_MED = (116, 90, 142); MALVA = (148, 120, 170); LILAS = (172, 148, 192)
CREME = (243, 220, 192); CREME_ESC = (232, 201, 168); CREME_SOMBRA = (196, 160, 140)
AMAR_CLARO = (255, 226, 96); AMARELO = (252, 200, 36); AMBAR = (238, 150, 24)
LIMAO = (255, 216, 50); LIMAO_CLARO = (255, 238, 112); LIMAO_JUNTA = (234, 166, 24)
LARANJA = (240, 128, 28); VERM = (218, 32, 40); VERM_ESC = (160, 18, 34); VERM_VIVO = (246, 64, 44)
PERNA = (252, 192, 44); PERNA_ESC = (230, 140, 26)

SOBE_CAB = -0.2       # a cabeça sobe (pescoço em S acima do peito)
PESCOCO_FRENTE = 6    # o pescoço pende para a frente (S) e a cabeça se endireita
K_CAB = 0.9           # escala da cabeça
BAIXA = 2.0           # o corpo todo desce (pernas mais curtas)
INCLINA = 5           # corpo quase deitado (oval horizontal)

def brilho_amarelo(c, cor):
    """Só os pixels amarelos/laranja-claros brilham (pontas de pena, pontas da crista)."""
    return cor[0] > 215 and cor[1] > 135 and cor[2] < 150

def tri(v, n):
    """Onda triangular: 0 no meio de cada uma das n faixas de v (-1..1), 1 nas divisas."""
    q = ((v + 1) / 2 * n) % 1.0
    return abs(2 * q - 1)

def mat_pena_bloco(c0, c1, ei, inv):
    """Pena em bloco: degradê no comprimento, fio claro em cima e sombra embaixo nas faces largas."""
    base = g.mat_pena(c0, c1, ei, inv, borda=.15)
    def f(c):
        cor = base(c)
        if c["face"] in ("east", "west"):
            y0, y1 = c["b"][0][1], c["b"][1][1]
            t = (c["p"][1] - y0) / max(y1 - y0, 1e-6)
            if t > 0.8: cor = tom(cor, 0.14)
            elif t < 0.25: cor = tom(cor, -0.22 * (0.25 - t) / 0.25)
        return cor
    return f

# ---------------- cabeça ----------------
FAC_T = 1.6                                    # espessura da peça da face diagonal (onde fica o olho)
FAC_S = (3.1, -4.5)                            # ponto (x, z) da superfície da faceta (lado +x)
FAC_C = (FAC_S[0] - 0.7071 * FAC_T / 2, FAC_S[1] + 0.7071 * FAC_T / 2)
FAC_L = 3.9
OLHO_Y = 26.4

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return mix(ROXO_MED, MALVA, 0.35)
    base = ROXO_MED if face == "north" else ROXO
    if y < 24.4: base = mix(base, ROXO_ESC, 0.25)
    return base

def olho(u, v):
    return g.pintar_olho(u, v, 1.74, 1.58, iris=((214, 150, 10), (255, 210, 44)), esclera=(255, 228, 92), pupila=PRETO,
                         r_iris=(0.58, 0.66), c_iris=(-0.3, -0.02), r_pup=(0.3, 0.36), bravo=0.45, alto=0.52,
                         contorno=(40, 24, 44))

def mat_faceta(lado):
    base = g.mat_cor(cor_cabeca, borda=.03, curva=.35)
    fora = "east" if lado > 0 else "west"
    def f(c):
        if c["face"] == fora:
            x, y, z = c["p"]
            cor = olho(z - FAC_C[1], y - OLHO_Y)
            if cor is not None: return cor
        return base(c)
    return f

def brilho_olho(lado):
    fora = "east" if lado > 0 else "west"
    def f(c, cor):
        if c["face"] != fora: return False
        x, y, z = c["p"]
        o = olho(z - FAC_C[1], y - OLHO_Y)
        return o is not None and o[0] > 180 and o[1] > 100
    return f

def cor_bico(p, face):
    x, y, z = p
    if face in ("east", "west") and abs(z + 6.3) < 0.28 and abs(y - 25.6) < 0.22: return (150, 80, 20)   # narina
    if face == "down": return AMBAR
    # dourado na base, laranja na ponta
    return mix((255, 210, 52), (244, 140, 24), clamp((-z - 6.4) / 2.4) * 0.85 + clamp((24.6 - y) / 2.0) * 0.25)

def mat_placa_cabeca():
    return g.mat_facetado(mix(MALVA, LILAS, .4), MALVA, ROXO_MED, ROXO_ESC, quina=-0.35)

def mat_telha(z_fim, n=4, fundo=1.3):
    """Placa de penas da cabeça penteada para a nuca: em cima clara, beirada de trás recortada em pontas."""
    base = g.mat_facetado(mix(MALVA, LILAS, .3), MALVA, ROXO_MED, ROXO_ESC, quina=-0.3)
    def f(c):
        x, y, z = c["p"]
        (x0, _, _), (x1, _, _) = c["b"]
        v = 2 * (x - x0) / max(x1 - x0, 1e-6) - 1
        if z > z_fim - fundo * tri(v, n): return None
        cor = base(c)
        if c["face"] == "up" and z > z_fim - fundo * tri(v, n) - 0.35: cor = tom(cor, -0.3)
        if c["face"] == "up" and tri(v, n) > 0.92: cor = tom(cor, -0.2)
        return cor
    return f

def cabeca_pecas():
    cab = []
    mc = g.mat_cor(cor_cabeca, borda=.03, curva=.35)
    fx = (22.6, 30.0)
    cab.append(peca("cranio_lados", [-4.2, 23.0, -3.4], [4.2, 29.4, 2.6], mc, faixa=fx, res=4))
    cab.append(peca("cranio_meio", [-3.6, 22.6, -4.3], [3.6, 29.8, 3.1], mc, faixa=fx, res=4))
    cab.append(peca("cranio_frente", [-2.0, 22.8, -5.6], [2.0, 29.5, -4.2], mc, faixa=fx, res=4))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 23.0, cz - FAC_L / 2], [cx + FAC_T / 2, 29.3, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=fx, res=8, brilho=brilho_olho(lado)))
        # sobrancelha clara por cima do olho, descendo para o bico (cara brava)
        fx0, fx1 = sorted((cx + FAC_T / 2 * lado - 0.1 * lado, cx + FAC_T / 2 * lado + 0.45 * lado))
        cab.append(osso("sobrancelha_" + s, [cx, 27.85, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [fx0, 27.4, cz - 2.05], [fx1, 28.3, cz + 1.7], mat_placa_cabeca(),
                 rot=(-18, 0, 0), pivo=(cx, 27.85, cz), res=4)]))
    # bico curto e grosso em cunha: base quase na altura do olho, ponta um pouco para baixo, dourado -> laranja
    mb = g.mat_cor(cor_bico, borda=.05, curva=.3)
    fb = (23.2, 26.6)
    cab.append(peca("bico_base", [-1.75, 23.7, -7.0], [1.75, 26.4, -5.3], mb, faixa=fb, res=4))
    cab.append(peca("bico_ponta", [-1.4, 23.75, -8.7], [1.4, 26.35, -6.9], mb, rot=(-16, 0, 0), pivo=(0, 26.35, -6.9), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-1.3, 23.2, -7.9], [1.3, 23.95, -5.3], g.mat_cor(lambda p, f: AMBAR, borda=.1), rot=(6, 0, 0),
                    pivo=(0, 23.6, -5.3), res=4))
    # barbela vermelha em dois lobos
    mbar = g.mat_cor(lambda p, f: mix(VERM_ESC, VERM_VIVO, clamp((p[1] - 19.0) / 4.0)), borda=.08, curva=.3)
    cab.append(peca("barbela_a", [-1.7, 21.6, -7.0], [1.7, 23.6, -5.0], mbar, faixa=(20.2, 23.6), res=4))
    cab.append(peca("barbela_b", [-1.35, 20.3, -6.8], [1.35, 21.8, -5.2], mbar, faixa=(20.2, 23.6), res=4))
    # penas da cabeça: 4 placas largas em camadas, penteadas para a nuca, rentes aos lados (telhado de penas)
    for k, (y0, z0, z1, rx) in enumerate([(29.55, -3.6, 4.4, 4), (27.9, -1.0, 5.0, 8), (26.2, -0.6, 5.2, 12), (24.5, -0.4, 4.6, 16)]):
        cab.append(peca(f"telha{k}", [-4.35, y0, z0], [4.35, y0 + 1.1, z1], mat_telha(z1), rot=(rx, 0, 0),
                        pivo=(0, y0 + 0.55, z0), res=4))
    for k, (y0, ry_) in enumerate([(28.0, 16), (26.0, 22)]):
        for lado in (-1, 1):
            cab.append(g.pena_curva(f"tufo{k}_{'d' if lado < 0 else 'e'}", (3.0 * lado, y0, 1.6),
                                    [(2.8, 1.7, 1.8, ROXO, ROXO_MED), (2.2, 1.1, 1.2, ROXO_MED, MALVA)],
                                    (-22 + 8 * k, ry_ * lado, 0), (10, 0, 0), "z", mat_pena_bloco, res=4))
    cab.append(crista())
    return cab

def crista():
    """Crista elétrica: 5 dedos vermelhos paralelos inclinados ~30° para trás, do mais curto (testa) ao mais
    comprido (alto da cabeça), pontas laranja e amarelas (brilham)."""
    def mcr(c0, c1, ei, inv): return g.mat_pena(c0, c1, ei, inv, borda=.14)
    def dedo(nome, base, rot0, curva, k, w=2.6, h=2.4):
        segs = [(2.6 * k, w, h, VERM_ESC, VERM), (2.2 * k, w * .9, h * .9, VERM, VERM_VIVO), (1.2 * k, w * .8, h * .8, VERM_VIVO, LARANJA),
                (1.0 * k, w * .68, h * .7, AMARELO, AMAR_CLARO)]
        return g.pena_curva(nome, base, segs, rot0, curva, "y", mcr, brilho_ponta=True, res=4)
    filhos = [dedo("crista_c0", (0, 29.3, -3.3), (-12, 0, 0), (6, 0, 0), 0.72),
              dedo("crista_c1", (0, 29.4, -1.1), (8, 0, 0), (6, 0, 0), 1.15),
              dedo("crista_c2", (0, 29.3, 1.3), (32, 0, 0), (8, 0, 0), 0.95),
              dedo("crista_c3", (0, 29.0, 3.1), (56, 0, 0), (8, 0, 0), 0.72)]
    for lado in (-1, 1):
        filhos.append(dedo("crista_l_" + ("d" if lado < 0 else "e"), (1.5 * lado, 29.3, -0.4), (12, 0, -24 * lado), (6, 0, -6 * lado),
                           0.85, w=2.2, h=2.2))
    filhos.append(peca("crista_base", [-1.7, 29.0, -4.4], [1.7, 30.6, 3.8],
                       g.mat_cor(lambda p, f: mix(VERM_ESC, VERM, clamp((p[1] - 29.0) / 1.6)), borda=.1), res=4))
    return osso("crista", [0, 29.4, -0.5], [0, 0, 0], filhos)

# ---------------- corpo ----------------
def cor_tronco(p, face):
    """Plumagem roxa com fileiras de penas (escamas) pintadas: borda de baixo de cada pena mais escura."""
    x, y, z = p
    h = (z if face in ("east", "west") else x) / 2.6
    fy = (y - 1.0 * (math.floor(h) % 2)) / 2.0
    jy, jh = fy - math.floor(fy), h - math.floor(h)
    if jy < 0.14 * (1 - abs(2 * jh - 1) ** 2) + 0.05: return mix(ROXO, ROXO_ESC, 0.4)
    return mix(ROXO, ROXO_MED, 0.35 * jy)

LAN_C = (0.0, 10.6, 8.2)                       # centro da lanterna (bola de vaga-lume)
LAN_R = (6.2, 3.9, 6.8)

def mat_lanterna():
    """Lanterna de vaga-lume: amarelo-limão em gomos (grade de amarelo um pouco mais escuro), clara no meio da bola."""
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        T = 2.2
        a = x if face in ("north", "south", "up", "down") else z - LAN_C[2]
        b = y - LAN_C[1] if face not in ("up", "down") else z - LAN_C[2]
        ja, jb = (a / T + 0.5) % 1.0, (b / T + 0.5) % 1.0
        dj = min(min(ja, 1 - ja), min(jb, 1 - jb)) * T
        ex, ey, ez = (x - LAN_C[0]) / LAN_R[0], (y - LAN_C[1]) / LAN_R[1], (z - LAN_C[2]) / LAN_R[2]
        r = math.hypot(ex, ey) if face in ("north", "south") else math.hypot(ez, ey) if face in ("east", "west") else math.hypot(ex, ez)
        cor = mix(LIMAO_CLARO, LIMAO, clamp((r - 0.2) / 0.8))           # mais clara no meio da bola
        if dj < 0.16: cor = mix(LIMAO_JUNTA, cor, 0.15)
        luz = -0.12 * clamp((r - 0.7) / 0.5)
        if face == "down": luz -= 0.1
        return tom(cor, luz)
    return f

def mat_peito(k, y0, y1, w):
    """Fileira de penas creme do peito (V): pontas recortadas na beirada de baixo, risco entre as penas."""
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        cor = mix(CREME, CREME_ESC, clamp((20.5 - y) / 7.0))
        cor = mix(cor, mix(CREME_SOMBRA, MALVA, 0.5), clamp((abs(x) - w + 1.4) / 1.4) * 0.75)
        u = (x / 1.5 + (0.5 if k % 2 else 0.0)) % 1.0
        h = y - y0
        if face in ("north", "east", "west"):
            if h < 1.1 * abs(2 * u - 1) ** 1.2 and face == "north": return None
            if face == "north" and h < 1.1 * abs(2 * u - 1) ** 1.2 + 0.2: return tom(cor, -0.35)
            if face == "north" and abs(2 * u - 1) > 0.9 and h > 0.9: cor = tom(cor, -0.15)
            if face == "north": cor = tom(cor, 0.1 * (1 - abs(2 * u - 1)) - 0.18 * clamp(1 - h / 1.8))
        luz = 0.1 if face == "up" else -0.3 if face == "down" else 0.0
        if face in ("east", "west"): return tom(cor_tronco(c["p"], face), -0.05)
        if face == "up": cor = mix(cor, MALVA, 0.5)
        return tom(cor, luz + 0.1 * (y - y0) / max(y1 - y0, 1))
    return f

def mat_fileira_asa(z0, L, yc, H, n=3, faixa=0.32):
    """Fileira de penas da asa dobrada (placa rente ao flanco): roxa, pontas recortadas atrás com faixa amarela."""
    def f(c):
        x, y, z = c["p"]
        u = (z - z0) / L
        v = clamp((y - yc) / (H / 2), -1, 1)
        t = tri(v, n)
        umax = 1 - (0.26 * t if n > 1 else 0.45 * abs(v) ** 1.2)
        if u > umax: return None
        face = c["face"]
        if u > umax - faixa:
            cor = mix(AMARELO, AMAR_CLARO, (u - umax + faixa) / faixa)
        else:
            cor = mix(ROXO_ESC, ROXO_MED, clamp(u / 0.7))
            if t > 0.9: cor = tom(cor, -0.3)                    # divisa entre penas
            elif t < 0.1: cor = tom(cor, 0.12)                  # raque
        if face == "up": cor = tom(cor, 0.2)
        elif face == "down": cor = tom(cor, -0.3)
        elif v > 0.8: cor = tom(cor, 0.12)
        elif v < -0.75: cor = tom(cor, -0.2)
        return cor
    return f

def mat_foice(L_total, ini, L, h, ponta):
    """Segmento de pena-foice da cauda (placa larga): roxo-escuro, último terço amarelo-ouro, ponta afiada."""
    def f(c):
        x, y, z = c["p"]
        (_, y0, z0), (_, y1, z1) = c["b"]
        t = (z - z0) / max(z1 - z0, 1e-6)
        v = (y - (y0 + y1) / 2) / max((y1 - y0) / 2, 1e-6)
        if ponta and abs(v) > (1 - t) ** 0.85 + 0.02: return None
        fr = (ini + t * L) / L_total
        if fr < 0.62: cor = mix(ROXO_ESC, ROXO_MED, fr / 0.62)
        elif fr < 0.68: cor = mix(ROXO_MED, AMARELO, (fr - 0.62) / 0.06)
        else: cor = mix(AMARELO, AMAR_CLARO, (fr - 0.68) / 0.32)
        face = c["face"]
        if face in ("east", "west"):
            if abs(v) < 0.1: cor = tom(cor, 0.12)
            if v > 0.75: cor = tom(cor, 0.1)
            if v < -0.7: cor = tom(cor, -0.22)
        elif face == "up": cor = tom(cor, 0.18)
        elif face == "down": cor = tom(cor, -0.3)
        return cor
    return f

def foice(nome, base, L_total, H, rot0, curva, esp=0.55, n=4):
    """Pena-foice larga e chata (placa de pé, fina em x) em n segmentos que se curvam; a ponta é afiada."""
    fr = [0.3, 0.27, 0.23, 0.2][:n]
    def seg(k, pos, ini):
        L = L_total * fr[k]; hk = H * (1 - 0.12 * k)
        px, py, pz = pos
        filhos = [peca(f"{nome}_{k}", [px - esp / 2, py - hk / 2, pz], [px + esp / 2, py + hk / 2, pz + L],
                       mat_foice(L_total, ini, L, hk, k == n - 1), res=4)]
        if k + 1 < n: filhos.append(seg(k + 1, (px, py, pz + L - 0.15), ini + L))
        return osso(f"{nome}_{k}", list(pos), list(rot0) if k == 0 else list(curva), filhos)
    return seg(0, tuple(base), 0.0)

def bola(nome, C, R, mat, n=6, **kw):
    """Elipsoide em fatias: n placas horizontais (prismas de 8 lados) com o tamanho da elipse em cada altura."""
    cx, cy, cz = C; rx, ry, rz = R
    ids = []
    for i in range(n):
        y0 = cy - ry + 2 * ry * i / n; y1 = cy - ry + 2 * ry * (i + 1) / n
        ym = (y0 + y1) / 2
        k = math.sqrt(max(0.05, 1 - ((ym - cy) / ry) ** 2)) ** 0.75
        ax, az = rx * k, rz * k
        ids += g.octogono(f"{nome}{i}", [cx - ax, y0, cz - az], [cx + ax, y1, cz + az], mat, r=min(ax, az) * 0.38,
                          faixa=(cy - ry, cy + ry), **kw)
    return ids

def montar():
    corpo = []
    # ---------- cabeça ----------
    i_cab = len(g.PECAS)
    cab = cabeca_pecas()
    cabeca = osso("cabeca", [0, 23.5, -1.0], [2 + PESCOCO_FRENTE, 0, 0], cab)
    g.transformar(i_cab, [cabeca], (0, 22.4, -1.0), K_CAB, sobe=SOBE_CAB)
    mpes = g.mat_cor(cor_tronco, borda=.04, curva=.4)
    pescoco = osso("pescoco", [0, 19.5, -1.5], [-INCLINA - PESCOCO_FRENTE, 0, 0], [
        *g.arredondado("pescoco", [-3.2, 18.6, -4.6], [3.2, 23.8, 0.8], mpes, r=0.9, faixa=(17.0, 26.0)),
        *g.arredondado("pescoco_base", [-4.6, 17.4, -5.0], [4.6, 21.4, 2.0], mpes, r=1.3, faixa=(17.0, 26.0)),
        cabeca])
    corpo.append(pescoco)

    # ---------- tronco: oval deitado ----------
    mtr = g.mat_cor(cor_tronco, borda=.03, curva=.55)
    corpo += g.arredondado2("tronco", [-6.8, 11.0, -5.2], [6.8, 19.8, 10.6], mtr, r=3.6, faixa=(9.0, 20.0))
    corpo += g.arredondado("peito", [-5.0, 12.0, -5.4], [5.0, 19.4, -1.0], mtr, r=1.6, faixa=(9.0, 20.0))
    corpo += g.arredondado("garupa", [-4.6, 15.0, 8.0], [4.6, 19.0, 12.2], mtr, r=1.4, faixa=(9.0, 20.0))

    # ---------- lanterna de vaga-lume: bola em degraus na metade de baixo/trás do corpo ----------
    cx, cy, cz = LAN_C; rx_, ry_, rz_ = LAN_R
    ml = mat_lanterna()
    corpo += bola("lanterna", LAN_C, LAN_R, ml, n=7, brilho=True)

    # ---------- peito creme em V: 4 fileiras de penas pontudas, da barbela até a lanterna ----------
    for k, (w, y0, y1, z0) in enumerate([(3.9, 16.8, 19.4, -6.3), (3.3, 14.7, 17.6, -6.7), (2.6, 12.6, 15.6, -6.9), (1.8, 10.8, 13.6, -6.6)]):
        corpo.append(peca(f"peito_fileira{k}", [-w, y0, z0], [w, y1, z0 + 2.4], mat_peito(k, y0, y1, w), res=4, faixa=(11.0, 20.0)))

    # ---------- asas dobradas: 4 fileiras de penas rentes ao flanco, varridas para trás, ponta amarela ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        for k, (yc, H, z0, L, dx, rx) in enumerate([(18.4, 2.8, -3.0, 7.0, 0.0, 10), (16.4, 3.0, -2.4, 9.0, 0.25, 13),
                                                    (14.4, 3.0, -1.6, 10.4, 0.45, 16), (12.6, 2.8, -0.6, 10.0, 0.35, 19)]):
            x = (6.95 + dx) * lado
            x0, x1 = sorted((x - 0.25 * lado, x + 0.3 * lado))
            asa.append(osso(f"asa{k}_{s}", [x, yc, z0], [rx, -4 * lado, 0], [
                peca(f"asa{k}_{s}", [x0, yc - H / 2, z0], [x1, yc + H / 2, z0 + L], mat_fileira_asa(z0, L, yc, H, n=1, faixa=0.3), res=4)]))
        corpo.append(osso("asa_" + s, [6.9 * lado, 18.0, -2.0], [0, 0, 0], asa))

    # ---------- cauda: leque de 6 foices largas, do topo (mais comprida) para baixo (mais curta) ----------
    cauda = []
    for k in range(6):
        lado = 1 if k % 2 else -1
        ang = -42 + 9 * k                       # cada uma ~9° mais baixa
        L = 12.5 - 0.8 * k
        cauda.append(foice(f"cauda{k}", (0.6 * lado * (k > 0), 18.8 - 0.55 * k, 10.8 - 0.2 * k), L, 4.2 - 0.2 * k,
                           (ang - INCLINA, (10 + 5 * k) * lado * (k > 0), 0), (20, 0, 0), esp=0.9))
    corpo.append(osso("cauda", [0, 18.0, 10.6], [0, 0, 0], cauda))

    # ---------- asas de inseto: presas no alto das costas, ~40-45° para cima e para trás ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        corpo.append(asa_inseto("asa_inseto_" + s, (3.0 * lado, 20.2, 2.6), 17.0, 6.8, lado, (0, -36 * lado, 40 * lado), 1))
        corpo.append(asa_inseto("asa_inseto2_" + s, (3.0 * lado, 19.4, 4.4), 12.5, 5.2, lado, (0, -52 * lado, 14 * lado), 2))

    tronco = osso("corpo", [0, 10.5, 3.0], [INCLINA, 0, 0], corpo)
    g.transformar(0, [tronco], (0, 0, 0), 1.0, sobe=-BAIXA)
    # pontas amarelas das penas, da cauda e da crista brilham no escuro (só os pixels amarelos)
    for pc in g.PECAS:
        if pc.nome.startswith(("asa", "cauda", "crista_")) and pc.brilho is not True:
            pc.brilho = brilho_amarelo

    # ---------- pernas douradas, aparecendo abaixo do corpo ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 3.4 * lado; zc = 3.4
        pp = []
        mperna = g.mat_cor(lambda p, f: mix(PERNA_ESC, PERNA, clamp((p[1] - 1.0) / 8.0)), borda=.08, curva=.4)
        pp += g.arredondado("coxa_" + s, [xc - 2.1, 5.0, zc - 2.1], [xc + 2.1, 8.6, zc + 2.1], mperna, r=0.7, faixa=(0, 8.6))
        pp.append(peca("canela_" + s, [xc - 1.5, 1.2, zc - 1.5], [xc + 1.5, 5.4, zc + 1.5], mperna, faixa=(0, 8.6)))
        md = g.mat_cor(lambda p, f: PERNA, borda=.15, curva=.5)
        mg = g.mat_cor(lambda p, f: ROXO_MED, borda=.18, curva=.5)
        for nome, giro, dx in (("meio", 0, 0), ("fora", -24 * lado, 1.6 * lado), ("dentro", 24 * lado, -1.6 * lado)):
            x0, z0 = xc + dx, zc - 0.6
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .9, 0, z0 - 3.3], [x0 + .9, 1.5, z0 + 0.6], md, faixa=(0, 2.0)),
                peca(f"garra_{nome}_{s}", [x0 - .75, 0, z0 - 4.5], [x0 + .75, 1.2, z0 - 3.2], mg, faixa=(0, 2.0))]))
        pp.append(peca("dedo_tras_" + s, [xc - .65, 0, zc + 0.8], [xc + .65, 1.3, zc + 2.8], mg, faixa=(0, 2.0)))
        return osso("perna_" + s, [xc, 8.6, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

# ---------------- asas de inseto (placas recortadas com nervuras) ----------------
MEMB_RAIZ = (232, 190, 90); MEMB_PONTA = (244, 210, 118); MEMB_CLARA = (253, 232, 156)
VEIA = (255, 222, 84); BORDA_ASA = (255, 208, 40); BORDA_ESC = (226, 140, 16)

def meia_asa(s):
    """Meia largura (fração de W/2) da asa no ponto s (0 = raiz, 1 = ponta)."""
    if s < 0 or s > 1: return 0.0
    if s < 0.6: return math.sqrt(max(0.0, 1 - ((s - 0.6) / 0.63) ** 2))
    return max(0.0, 1 - ((s - 0.6) / 0.4) ** 2) ** 0.6

def mat_asa_inseto(raiz, L, W, semente):
    rx, ry, rz = raiz
    rnd = random.Random(semente)
    passo = 4.6
    sementes = []
    for a in range(int(L / passo) + 2):
        for b in range(-3, 4):
            sementes.append(((a + 0.5 + rnd.uniform(-.12, .12)) * passo, (b + (0.5 if a % 2 else 0) + rnd.uniform(-.1, .1)) * passo * 0.75))
    def f(c):
        x, y, z = c["p"]
        d = abs(x - rx); s = d / L
        t = y - ry
        off = W * 0.08 * s
        hw = meia_asa(s) * W / 2 * (0.82 if t > off else 1.18)     # borda de ataque (de cima) mais reta
        if abs(t - off) > hw: return None
        borda = hw - abs(t - off)
        if c["face"] not in ("north", "south"): return BORDA_ASA
        if borda < 0.62: return BORDA_ASA                          # aro dourado forte
        if borda < 0.8: return BORDA_ESC
        if abs(t - off) < 0.1 and s < 0.85: return VEIA          # nervura central
        ds = sorted((d - a) ** 2 + (t - b) ** 2 for a, b in sementes)[:2]
        d1, d2 = math.sqrt(ds[0]), math.sqrt(ds[1])
        if d2 - d1 < 0.3: return VEIA
        base = mix(MEMB_RAIZ, MEMB_PONTA, s)
        return mix(MEMB_CLARA, base, clamp(d1 / 1.0))
    return f

def asa_inseto(nome, raiz, L, W, lado, rot, semente, esp=0.22):
    x, y, z = raiz
    x0, x1 = sorted((x, x + L * lado))
    return osso(nome, list(raiz), list(rot), [
        peca(nome, [x0, y - W * 0.6 - 0.3, z - esp / 2], [x1, y + W * 0.5 + 0.3, z + esp / 2], mat_asa_inseto(raiz, L, W, semente),
             res=5, brilho=True)])

def vibra(a, n=12, fase=0):
    """Batida rápida (keyframes igualmente espaçados; o último igual ao primeiro)."""
    ks = [(0, 0, 0)]
    for k in range(n - 1):
        v = a if (k + fase) % 2 == 0 else -a * 0.5
        ks.append((0, 0, v))
    ks.append((0, 0, 0))
    return ks

ANIM_PARADO = {
    "asa_inseto_d": vibra(-12), "asa_inseto_e": vibra(12),
    "asa_inseto2_d": vibra(-10, fase=1), "asa_inseto2_e": vibra(10, fase=1),
}
ANIM_ANDANDO = {
    "asa_inseto_d": vibra(-16, n=6), "asa_inseto_e": vibra(16, n=6),
    "asa_inseto2_d": vibra(-12, n=6, fase=1), "asa_inseto2_e": vibra(12, n=6, fase=1),
}

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

"""Vagaló (#009, Elétrico): galo-vaga-lume veloz, roxo-ameixa, com asas de inseto douradas e lanterna que brilha.

Polimento (rodadas v50+), sempre conferido contra a 009_vagalo_arte.png:
- corpo roxo-ameixa fosco (paleta da ficha) com realce roxo-claro na beirada de cada pena;
- crista elétrica em 4 dedos grossos de blocos escalonados, em leque varrendo para trás, pontas amarelas;
- asas de inseto em folha/gota alongada: a da frente grande, a de trás menor logo abaixo; aro dourado grosso e
  nervuras em células hexagonais (as duas brilham), membrana âmbar sem brilho;
- cauda de 5 penas-foice grossas que arqueiam para trás e caem, pontas amarelas brilhantes;
- asas de ave em penas roxas em camadas com faixa e ponta amarelas;
- abdômen: bulbo redondo de células amarelas na barriga de baixo e na traseira (não um anel em volta do corpo)."""
import math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, PRETO, na_borda

ID = "vagalo"; NOME = "Vagaló"; NUMERO = 9
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 26.0, -2.0), 7.0)
ONDAS = [("cauda0", 6, (3, 0, 0)), ("cauda2", 6, (3, 0, 0))]

# ---------------- paleta (amostrada na "Paleta de Cores" da ficha: 77,51,94 / 146,98,144 / 253,227,192 /
# 254,237,115 / 254,193,2 / 253,132,1 / 226,8,29 / 254,252,182) ----------------
ROXO_ESC = (77, 51, 94); ROXO = (116, 76, 128); ROXO_MED = (134, 90, 144); MALVA = (146, 98, 144); LILAS = (178, 136, 176)
# cabeça um pouco mais lavanda que o corpo (como na arte)
CAB = (124, 88, 146); CAB_CLARO = (144, 106, 166); CAB_ESC = (92, 62, 112); CAB_LUZ = (166, 132, 186)
CREME = (253, 227, 192); CREME_ESC = (236, 204, 172); CREME_SOMBRA = (200, 160, 150); CREME_ROSA = (206, 168, 176)
AMAR_PALIDO = (254, 252, 182); AMAR_CLARO = (254, 237, 115); AMARELO = (254, 193, 2); AMBAR = (240, 160, 10)
LARANJA = (253, 132, 1); VERM = (226, 8, 29); VERM_ESC = (156, 8, 28); VERM_VIVO = (246, 52, 36)
PERNA = (254, 190, 24); PERNA_ESC = (238, 136, 10); GARRA = (72, 46, 86); GARRA_CLARA = (100, 66, 116)

SOBE_CAB = 0.6        # a cabeça sobe (pescoço em S acima do peito)
PESCOCO_FRENTE = 6    # o pescoço pende para a frente (S) e a cabeça se endireita
K_CAB = 0.9           # escala da cabeça
BAIXA = 2.8           # o corpo todo desce (pernas mais curtas)
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
FAC_SAI = 0.24                                 # a placa do olho sai um pouco da cara (cobre a quina do crânio no olho)
FAC_S = (3.1 + 0.7071 * FAC_SAI, -4.5 - 0.7071 * FAC_SAI)   # ponto (x, z) da superfície da faceta (lado +x)
FAC_C = (FAC_S[0] - 0.7071 * FAC_T / 2, FAC_S[1] + 0.7071 * FAC_T / 2)
FAC_L = 4.3
OLHO_Y = 26.4

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return mix(CAB_CLARO, CAB_LUZ, 0.3)
    base = CAB_CLARO if face == "north" else CAB
    if y < 24.4: base = mix(base, CAB_ESC, 0.3)
    return base

OLHO_RU, OLHO_RV = 2.02, 1.62                  # meia largura (ao longo da face) e meia altura do olho
OLHO_DU = -0.05                                # centro do olho puxado para o bico
OLHO_CORTE0, OLHO_CORTE_INC = 0.78, 0.3       # linha da pálpebra: v = c0 + inc * u (desce para o bico)
IRIS_CLARA = (255, 238, 120); IRIS = (254, 196, 10); IRIS_ESC = (206, 126, 6); IRIS_ANEL = (150, 84, 8)
ESCLERA = (254, 248, 196); CILIO = (30, 14, 34)

def olho(u, v):
    """Olho bravo: fenda alongada para trás, canto da frente pontudo. A pálpebra pesada corta o topo numa diagonal
    que desce para o bico, com 1 px escuro e a sombra da sobrancelha logo abaixo. Íris dourada grande, pupila escura
    redonda junto da frente com 1 px de brilho; esclera creme só numa cunha atrás.
    u: ao longo da face (negativo = para o bico); v: para cima. Devolve None fora do olho."""
    ru, rv = OLHO_RU, OLHO_RV
    uu = u / ru
    if abs(uu) > 1: return None
    corte = OLHO_CORTE0 + OLHO_CORTE_INC * u
    baixo = -rv * (0.74 - 0.2 * uu) * (1 - max(0.0, -uu) ** 2.4)
    cima = rv * (0.95 - 0.08 * uu) * (1 - max(0.0, -uu) ** 1.6) * (1 - max(0.0, uu) ** 4)
    baixo *= (1 - max(0.0, uu) ** 5)
    topo = min(cima, corte)
    if v > corte and v <= corte + 0.22 and v <= cima + 0.3: return mix(CILIO, CAB_ESC, 0.35)   # sombra da sobrancelha
    if v < baixo or v > topo: return None
    if topo - v < 0.13: return CILIO
    ic, ir = -0.08, 0.8
    du = (uu - ic) / ir; dv = v / (rv * 0.98)
    if du * du + dv * dv <= 1 or (uu < ic and v >= baixo):
        if ((uu + 0.42) / 0.27) ** 2 + ((v + 0.04) / 0.74) ** 2 <= 1:            # pupila escura, grande
            if abs(u - (-0.42 * ru + 0.16)) < 0.08 and topo - v > 0.16 and topo - v < 0.34: return (255, 252, 236)
            return PRETO
        cor = mix(IRIS_CLARA, IRIS, clamp((v - baixo) / max(topo - baixo, 0.1)))
        if topo - v < 0.3: cor = mix(cor, IRIS_ESC, 0.7)
        if du * du + dv * dv > 0.78 and uu > ic: cor = IRIS_ANEL
        return cor
    return mix(ESCLERA, mix(ESCLERA, IRIS_ESC, 0.45), clamp((topo - v) / 0.8))

def mat_faceta(lado):
    base = g.mat_cor(cor_cabeca, borda=.03, curva=.3)
    fora = "east" if lado > 0 else "west"
    def f(c):
        if c["face"] == fora:
            x, y, z = c["p"]
            cor = olho(z - FAC_C[1] - OLHO_DU, y - OLHO_Y)
            if cor is not None: return cor
        return base(c)
    return f

def brilho_olho(lado):
    fora = "east" if lado > 0 else "west"
    def f(c, cor):
        if c["face"] != fora: return False
        x, y, z = c["p"]
        o = olho(z - FAC_C[1] - OLHO_DU, y - OLHO_Y)
        return o is not None and o[0] > 240 and o[1] > 170 and o[2] < 130
    return f

def cor_bico(p, face):
    x, y, z = p
    if face in ("east", "west") and abs(z + 6.4) < 0.26 and abs(y - 25.7) < 0.2: return (150, 80, 20)   # narina
    if face == "down": return AMBAR
    return mix((255, 212, 40), (248, 158, 12), clamp((-z - 7.2) / 2.6) * 0.8 + clamp((24.8 - y) / 2.0) * 0.2)

def mat_telha(z_fim, n=4, fundo=1.3):
    """Placa de penas da cabeça penteada para a nuca: em cima clara, beirada de trás recortada em pontas."""
    base = g.mat_facetado(mix(CAB_CLARO, CAB_LUZ, .45), CAB_CLARO, CAB, CAB_ESC, quina=-0.3)
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

SOB_SAI, SOB_H, SOB_DY, SOB_FRENTE, SOB_TRAS = 0.7, 1.4, 0.2, 2.6, 1.6

def mat_sobrancelha():
    """Sobrancelha pesada: lavanda no topo, face de baixo quase preta (sombra sobre o olho)."""
    return g.mat_facetado(CAB_CLARO, CAB, mix(CAB, CAB_ESC, 0.45), mix(CAB_ESC, CILIO, 0.5), quina=-0.3)

def cabeca_pecas():
    cab = []
    mc = g.mat_cor(cor_cabeca, borda=.03, curva=.3)
    fx = (22.6, 30.0)
    cab.append(peca("cranio_lados", [-4.2, 23.0, -3.4], [4.2, 29.4, 2.6], mc, faixa=fx, res=4))
    cab.append(peca("cranio_meio", [-3.6, 22.6, -4.3], [3.6, 29.8, 3.1], mc, faixa=fx, res=4))
    cab.append(peca("cranio_frente", [-2.0, 22.8, -5.6], [2.0, 29.5, -4.2], mc, faixa=fx, res=4))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 23.0, cz - FAC_L / 2], [cx + FAC_T / 2, 29.3, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=fx, res=8, brilho=brilho_olho(lado)))
        fx0, fx1 = sorted((cx + FAC_T / 2 * lado - 0.5 * lado, cx + FAC_T / 2 * lado + SOB_SAI * lado))
        ang = math.degrees(math.atan(OLHO_CORTE_INC))
        zc0 = cz + OLHO_DU
        yb = OLHO_Y + OLHO_CORTE0 + SOB_DY
        cab.append(osso("sobrancelha_" + s, [cx, yb, zc0], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [fx0, yb, zc0 - SOB_FRENTE], [fx1, yb + SOB_H, zc0 + SOB_TRAS], mat_sobrancelha(),
                 rot=(-ang, 0, 0), pivo=(cx, yb, zc0), res=4)]))
    mb = g.mat_cor(cor_bico, borda=.05, curva=.3)
    fb = (23.2, 26.6)
    cab.append(peca("bico_base", [-1.15, 23.9, -6.9], [1.15, 26.45, -5.3], mb, faixa=fb, res=4))
    cab.append(peca("bico_meio", [-0.95, 24.05, -8.5], [0.95, 26.2, -6.7], mb, rot=(-9, 0, 0), pivo=(0, 26.2, -6.7), faixa=fb, res=4))
    cab.append(peca("bico_ponta", [-0.7, 24.0, -9.8], [0.7, 25.75, -8.3], mb, rot=(-26, 0, 0), pivo=(0, 25.75, -8.3), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-0.85, 23.35, -7.9], [0.85, 24.1, -5.3], g.mat_cor(lambda p, f: (236, 150, 12), borda=.1),
                    rot=(5, 0, 0), pivo=(0, 23.7, -5.3), res=4))
    mbar = g.mat_cor(lambda p, f: mix(VERM_ESC, VERM_VIVO, clamp((p[1] - 18.6) / 4.6)), borda=.06, curva=.35)
    for lado in (-1, 1):
        x0, x1 = sorted((0.0, 1.75 * lado))
        cab += g.arredondado("barbela_" + ("d" if lado < 0 else "e"), [x0, 18.6, -7.3], [x1, 23.6, -4.9], mbar, r=0.6,
                             faixa=(18.6, 23.6), res=4)
    cab.append(peca("barbela_meio", [-1.2, 19.0, -7.15], [1.2, 23.6, -5.05], mbar, faixa=(18.6, 23.6), res=4))
    for k, (y0, z0, z1, rx) in enumerate([(29.55, -3.6, 4.4, 4), (27.9, -1.0, 5.0, 8), (26.2, -0.6, 5.2, 12), (24.5, -0.4, 4.6, 16)]):
        cab.append(peca(f"telha{k}", [-4.35, y0, z0], [4.35, y0 + 1.1, z1], mat_telha(z1), rot=(rx, 0, 0),
                        pivo=(0, y0 + 0.55, z0), res=4))
    for k, (y0, ry_) in enumerate([(28.0, 16), (26.0, 22)]):
        for lado in (-1, 1):
            cab.append(g.pena_curva(f"tufo{k}_{'d' if lado < 0 else 'e'}", (3.0 * lado, y0, 1.6),
                                    [(2.8, 1.7, 1.8, CAB, CAB_CLARO), (2.2, 1.1, 1.2, CAB_CLARO, CAB_LUZ)],
                                    (-22 + 8 * k, ry_ * lado, 0), (10, 0, 0), "z", mat_pena_bloco, res=4))
    cab.append(crista())
    return cab

# ---------------- crista elétrica: 4 dedos grossos em blocos escalonados ----------------
def mat_crista(c0, c1, ei, inv):
    """Bloco da crista: degradê no comprimento, aresta clara em cima, 1 linha de junta no meio do bloco (voxel)."""
    base = g.mat_pena(c0, c1, ei, inv, borda=.16)
    def f(c):
        cor = base(c)
        lo, hi = c["b"][0][ei], c["b"][1][ei]
        t = (c["p"][ei] - lo) / max(hi - lo, 1e-6)
        if c["face"] in ("east", "west", "north", "south") and abs(t - 0.5) < 0.05: cor = tom(cor, -0.12)
        return cor
    return f

def crista():
    """Leque de 4 dedos grossos (seção quase quadrada) de blocos que afinam em degraus: o da frente quase de pé, os
    de trás cada vez mais deitados para a nuca. Vermelho na raiz -> vermelho vivo -> laranja -> ponta amarela."""
    def dedo(nome, base, rot0, k, w):
        segs = [(2.2 * k, w, w, VERM_ESC, VERM), (1.9 * k, w * .9, w * .9, VERM, VERM_VIVO),
                (1.5 * k, w * .8, w * .8, VERM_VIVO, LARANJA), (1.4 * k, w * .7, w * .7, AMARELO, AMAR_CLARO)]
        return g.pena_curva(nome, base, segs, rot0, (5, 0, 0), "y", mat_crista, brilho_ponta=True, res=4)
    filhos = [dedo("crista_c0", (0, 29.2, -3.0), (4, 0, 0), 1.28, 3.3),
              dedo("crista_c1", (-0.8, 29.3, -0.9), (25, 0, -5), 1.2, 3.1),
              dedo("crista_c2", (0.8, 29.2, 1.0), (46, 0, 5), 1.1, 2.9),
              dedo("crista_c3", (0, 28.9, 2.6), (68, 0, 0), 1.0, 2.7)]
    filhos.append(peca("crista_base", [-1.4, 29.0, -4.2], [1.4, 30.8, 3.6],
                       g.mat_cor(lambda p, f: mix(VERM_ESC, VERM, clamp((p[1] - 29.0) / 1.8)), borda=.1), res=4))
    return osso("crista", [0, 29.4, -0.5], [0, 0, 0], filhos)

# ---------------- corpo ----------------
def cor_tronco(p, face):
    """Plumagem roxo-ameixa em escamas: beirada de baixo de cada pena com realce roxo-claro, sombra em cima dela."""
    x, y, z = p
    h = (z if face in ("east", "west") else x) / 2.5
    fy = (y - 1.0 * (math.floor(h) % 2)) / 2.0
    jy, jh = fy - math.floor(fy), h - math.floor(h)
    arco = 0.16 * (1 - abs(2 * jh - 1) ** 2)
    if jy < arco + 0.05: return mix(ROXO_ESC, ROXO, 0.3)                    # frincha (sombra da pena de cima)
    if jy < arco + 0.17: return mix(MALVA, LILAS, 0.15)                      # realce na beirada da pena
    return mix(ROXO, ROXO_MED, 0.5 * jy)

LAN_C = (0.0, 14.0, 4.8)                       # centro do bulbo de vaga-lume (barriga de baixo e traseira)
LAN_RX, LAN_RZ = 5.6, 6.6                      # meia largura e meio comprimento no meio do bulbo
LAN_RYB, LAN_RYT = 5.4, 4.6                    # meia altura para baixo (fundo de ovo) e para cima (escondida no corpo)
LAN_NB, LAN_NT = 6, 3                          # fatias da metade de baixo e da de cima
LAN_CEL = (3.0, 2.5)                           # célula: largura e altura

def perfil_ovo(t):
    """Meia largura (fração) do bulbo na altura t (-1 = fundo, 0 = meio, 1 = topo): embaixo cai mais rápido que uma
    elipse (fundo de ovo, curvo, sem piso chato); em cima é uma elipse."""
    if t < 0: return max(0.0, 1 - (-t) ** 1.8) ** (1 / 1.8)
    return math.sqrt(max(0.0, 1 - t * t))

def bola_ovo(nome, mat, **kw):
    """Bulbo em ovo: fatias horizontais (prismas de 8 lados quase regulares) com a largura do perfil_ovo no meio de
    cada fatia; mais fatias e mais finas embaixo, para o fundo arredondar."""
    cx, cy, cz = LAN_C
    fatias = [(cy - LAN_RYB + LAN_RYB * i / LAN_NB, cy - LAN_RYB + LAN_RYB * (i + 1) / LAN_NB) for i in range(LAN_NB)]
    fatias += [(cy + LAN_RYT * i / LAN_NT, cy + LAN_RYT * (i + 1) / LAN_NT) for i in range(LAN_NT)]
    ids = []
    for i, (y0, y1) in enumerate(fatias):
        ym = (y0 + y1) / 2
        t = (ym - cy) / (LAN_RYB if ym < cy else LAN_RYT)
        k = max(0.22, perfil_ovo(t))
        ax, az = LAN_RX * k, LAN_RZ * k
        ids += g.octogono(f"{nome}{i}", [cx - ax, y0, cz - az], [cx + ax, y1, cz + az], mat, r=min(ax, az) * 0.52,
                          faixa=(cy - LAN_RYB, cy + LAN_RYT), **kw)
    return ids

def mat_lanterna():
    """Bulbo de vaga-lume: grade de células amarelas grandes (3 x 2,5) separadas por juntas âmbar, em linhas de altura
    fixa (não segue as fatias); célula clara no meio, bulbo mais claro no centro de cada vista e mais âmbar na beirada
    (lê como um ovo aceso, não como uma saia)."""
    cx, cy, cz = LAN_C
    T, TY = LAN_CEL
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        a = z - cz if face in ("east", "west") else x
        ja = (a / T + 0.5) % 1.0
        da = min(ja, 1 - ja) * T                                      # distância até a junta vertical
        if face in ("up", "down"):
            jb = ((z - cz) / T + 0.5) % 1.0
            db = min(jb, 1 - jb) * T
        else:
            jb = ((y - (cy - LAN_RYB)) / TY) % 1.0                    # juntas horizontais a cada 2,5 a partir do fundo
            db = min(jb, 1 - jb) * TY
        d = min(da, db)
        ry = LAN_RYB if y < cy else LAN_RYT
        ex, ey, ez = (x - cx) / LAN_RX, (y - cy) / ry, (z - cz) / LAN_RZ
        r = math.hypot(ex, ey) if face in ("north", "south") else math.hypot(ez, ey) if face in ("east", "west") else math.hypot(ex, ez)
        bola_ = clamp(1.15 - r)                                       # 1 no meio da vista, 0 na beirada
        if d < 0.17:
            cor = mix((210, 116, 4), (240, 162, 16), bola_)           # junta âmbar
        else:
            k = clamp((d - 0.17) / 1.0)                               # 0 na beirada da célula, 1 no meio
            borda_cel = mix(AMBAR, AMARELO, 0.35 + 0.65 * bola_)
            meio_cel = mix(mix(AMARELO, AMAR_CLARO, 0.5), mix(AMAR_CLARO, AMAR_PALIDO, 0.7), bola_)
            cor = mix(borda_cel, meio_cel, k)
        luz = 0.05 * ey - (0.14 if face == "down" else 0.0)
        return tom(cor, luz)
    return f

def mat_escama(xc, k):
    """Escama creme do peito: ponta arredondada recortada embaixo, contorno mais escuro, meio claro; as de fora puxam
    para o creme-rosado/malva (como na arte)."""
    def f(c):
        x, y, z = c["p"]
        (x0, y0, z0), (x1, y1, z1) = c["b"]
        u = 2 * (x - (x0 + x1) / 2) / max(x1 - x0, 1e-6)
        v = (y - y0) / max(y1 - y0, 1e-6)
        borda_v = 0.42 * (1 - math.sqrt(max(0.0, 1 - u * u)))
        if v < borda_v: return None
        lado = clamp((abs(xc) - 1.6) / 2.4)
        cor = mix(mix(CREME, CREME_ESC, 0.25 * k / 3), CREME_ROSA, lado * 0.9)
        face = c["face"]
        if face == "up": return tom(mix(cor, MALVA, 0.4), -0.1)
        if face == "down": return tom(cor, -0.35)
        if face in ("east", "west"): return tom(cor, -0.2)
        if v < borda_v + 0.08 or abs(u) > 0.9: return tom(cor, -0.3)
        luz = 0.12 * (1 - abs(u)) - 0.22 * clamp((v - 0.72) / 0.28) + 0.06 * clamp(1 - v / 0.4)
        return tom(cor, luz)
    return f

def escama_peito(nome, x, topo, w, h, k, fundo=2.2):
    """Uma escama do peito pendurada da beirada de cima ('topo'), virada para fora conforme a curva do peito e com a
    ponta um pouco levantada para a frente (camadas)."""
    zf = -6.3 + 0.07 * x * x + 0.15 * k
    ry = -math.degrees(math.atan(0.16 * x))
    return osso(nome, [x, topo, zf], [0, ry, 0], [
        peca(nome, [x - w / 2, topo - h, zf], [x + w / 2, topo, zf + fundo], mat_escama(x, k), rot=(8, 0, 0),
             pivo=(x, topo, zf), res=4)])

# ---------------- penas grossas em blocos (asa de ave e cauda) ----------------
def mat_bloco(cor_fn, L, ini, Lk):
    """Segmento de pena grossa: a cor vem de cor_fn(fr) (fr = fração do comprimento TOTAL da pena); aresta de cima
    clara, de baixo escura, quinas escurecidas."""
    def f(c):
        x, y, z = c["p"]
        (x0, y0, z0), (x1, y1, z1) = c["b"]
        t = (z - z0) / max(z1 - z0, 1e-6)
        fr = clamp((ini + t * Lk) / L)
        v = (y - (y0 + y1) / 2) / max((y1 - y0) / 2, 1e-6)
        cor = cor_fn(fr)
        face = c["face"]
        if face == "up": luz = 0.2
        elif face == "down": luz = -0.32
        elif face in ("east", "west"): luz = 0.12 if v > 0.62 else (-0.2 if v < -0.55 else 0.0)
        else: luz = -0.08
        if na_borda(c): luz -= 0.1
        return tom(cor, luz)
    return f

PARTES_PENA = [(0.3, 1.0, 1.0), (0.28, 0.94, 0.94), (0.2, 0.82, 0.8), (0.13, 0.62, 0.56), (0.09, 0.36, 0.3)]

def pena_bloco(nome, base, L, w, h, rot0, curva, cor_fn, partes=PARTES_PENA, res=4):
    """Pena grossa em blocos ao longo de +z: um osso por segmento (nome_0, nome_1...), cada um girando 'curva'
    (um trio, ou uma lista de trios, um por segmento depois do primeiro). partes = [(fração do comprimento,
    fração da largura w (x), fração da altura h (y))]."""
    def seg(k, pos, ini):
        fr, fw, fh = partes[k]
        Lk = L * fr; wk = w * fw; hk = h * fh
        px, py, pz = pos
        filhos = [peca(f"{nome}_{k}", [px - wk / 2, py - hk / 2, pz], [px + wk / 2, py + hk / 2, pz + Lk],
                       mat_bloco(cor_fn, L, ini, Lk), res=res)]
        if k + 1 < len(partes):
            filhos.append(seg(k + 1, (px, py, pz + Lk - 0.15), ini + Lk - 0.15))
        r = rot0 if k == 0 else (curva[k - 1] if isinstance(curva[0], (list, tuple)) else curva)
        return osso(f"{nome}_{k}", list(pos), list(r), filhos)
    return seg(0, tuple(base), 0.0)

def cor_cauda(fr):
    """Pena-foice: roxo-ameixa na raiz, passagem curta pelo âmbar, último ~40% amarelo até a ponta quase branca."""
    if fr < 0.44: return mix(ROXO_ESC, ROXO_MED, fr / 0.44)
    if fr < 0.5: return mix(ROXO_MED, AMBAR, (fr - 0.44) / 0.06)
    if fr < 0.6: return mix(AMBAR, AMARELO, (fr - 0.5) / 0.1)
    return mix(AMARELO, mix(AMAR_CLARO, AMAR_PALIDO, 0.5), (fr - 0.6) / 0.4)

def cor_asa_longa(fr):
    """Rêmige: roxo, faixa amarela no meio, roxo, ponta amarela."""
    if 0.38 < fr < 0.52: return mix(AMARELO, AMAR_CLARO, (fr - 0.38) / 0.14)
    if fr > 0.62: return mix(AMARELO, AMAR_CLARO, (fr - 0.62) / 0.38)
    return mix(ROXO_ESC, MALVA, 0.25 + 0.5 * fr)

def cor_asa_curta(fr):
    """Coberteira: roxo com ponta amarela."""
    if fr > 0.55: return mix(AMARELO, AMAR_CLARO, (fr - 0.55) / 0.45)
    return mix(ROXO, MALVA, 0.2 + 0.6 * fr)

PARTES_FOICE = [(0.22, 1.0, 1.0), (0.21, 0.95, 0.88), (0.19, 0.88, 0.74), (0.16, 0.78, 0.58), (0.13, 0.62, 0.4), (0.09, 0.45, 0.22)]
PARTES_BARRIGA = [(0.45, 1.0, 1.0), (0.35, 0.85, 0.8), (0.2, 0.6, 0.48)]

def cor_barriga(fr):
    """Pena roxa da barriga: ameixa na raiz, malva na ponta."""
    return mix(ROXO, MALVA, 0.15 + 0.7 * fr)

def montar():
    corpo = []
    # ---------- cabeça ----------
    i_cab = len(g.PECAS)
    cab = cabeca_pecas()
    cabeca = osso("cabeca", [0, 23.5, -1.0], [2 + PESCOCO_FRENTE, 0, 0], cab)
    g.transformar(i_cab, [cabeca], (0, 22.4, -1.0), K_CAB, sobe=SOBE_CAB)
    mpes = g.mat_cor(cor_tronco, borda=.04, curva=.3)
    pescoco = osso("pescoco", [0, 19.5, -1.5], [-INCLINA - PESCOCO_FRENTE, 0, 0], [
        *g.arredondado("pescoco", [-3.2, 18.6, -4.6], [3.2, 24.6, 0.8], mpes, r=0.9, faixa=(17.0, 26.0)),
        *g.arredondado("pescoco_base", [-4.6, 17.4, -5.0], [4.6, 21.4, 2.0], mpes, r=1.3, faixa=(17.0, 26.0)),
        cabeca])
    corpo.append(pescoco)

    # ---------- tronco: oval deitado ----------
    mtr = g.mat_cor(cor_tronco, borda=.03, curva=.35)
    corpo += g.arredondado2("tronco", [-6.6, 14.4, -5.2], [6.6, 19.8, 10.6], mtr, r=2.8, faixa=(9.0, 20.0))
    corpo += g.arredondado("peito", [-5.0, 14.4, -5.4], [5.0, 19.4, -1.0], mtr, r=1.6, faixa=(9.0, 20.0))
    corpo += g.arredondado("garupa", [-4.6, 15.0, 8.0], [4.6, 19.0, 12.2], mtr, r=1.4, faixa=(9.0, 20.0))

    # ---------- bulbo de vaga-lume: bola redonda na barriga de baixo e na traseira ----------
    corpo += bola_ovo("lanterna", mat_lanterna(), brilho=True)
    # penas roxas da barriga caindo por cima do alto do bulbo (como na arte): 3 de cada lado, da frente para trás
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, phi in enumerate((-52, -12, 28)):
            r = math.radians(phi)
            x = lado * (LAN_RX * 0.95 + 0.3) * math.cos(r); z = LAN_C[2] + (LAN_RZ * 0.95 + 0.3) * math.sin(r)
            base = (x, LAN_C[1] + 1.9, z)
            corpo.append(osso(f"barriga{k}_{s}", list(base), [0, -phi * lado, 0], [
                pena_bloco(f"barriga{k}_{s}_p", base, 5.4, 1.0, 2.8, (88, 0, 16 * lado), (0, -7 * lado, 0), cor_barriga,
                           partes=PARTES_BARRIGA)]))

    # ---------- peito creme em V: 4 fileiras de penas pontudas, da barbela até o bulbo ----------
    for k, (topo, xs) in enumerate([(20.0, (-3.6, -1.2, 1.2, 3.6)), (18.1, (-2.4, 0.0, 2.4)), (16.2, (-1.2, 1.2)), (14.6, (0.0,))]):
        for j, x in enumerate(xs):
            corpo.append(escama_peito(f"peito{k}_{j}", x, topo, 2.5 if k < 3 else 2.1, 2.9 if k < 3 else 2.4, k))

    # ---------- asas de ave dobradas: coberteiras curtas por cima, rêmiges longas por baixo, todas varridas para trás ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        for k, (y, z0, L, rx) in enumerate([(18.6, 1.6, 11.5, 12), (17.3, 0.4, 11.5, 14), (16.0, -0.7, 11.0, 16), (14.8, -1.7, 10.0, 19)]):
            asa.append(pena_bloco(f"asa{k}_{s}", ((6.9 + 0.12 * k) * lado, y, z0), L, 1.3, 2.6, (rx, -7 * lado, 0), (4, -2 * lado, 0),
                                  cor_asa_longa))
        for k, (y, z0, L, rx) in enumerate([(19.6, -2.4, 8.5, 10), (18.6, -3.0, 8.5, 12), (17.4, -3.4, 8.0, 14)]):
            asa.append(pena_bloco(f"cob{k}_{s}", ((6.4 + 0.3 * k) * lado, y, z0), L, 1.2, 2.4, (rx, -5 * lado, 0), (4, -2 * lado, 0),
                                  cor_asa_curta))
        corpo.append(osso("asa_" + s, [6.9 * lado, 18.0, -2.0], [0, 0, 0], asa))

    # ---------- cauda: 5 penas-foice grossas que sobem um pouco, arqueiam para trás e caem ----------
    cauda = []
    for k in range(5):
        lado = 1 if k % 2 else -1
        L = 18.5 - 1.9 * k                                   # leque vertical: a de cima a mais longa
        sobe = -52 + 13 * k - INCLINA                        # a de cima sai bem para o alto, as de baixo quase retas
        tot = 150 - 14 * k                                   # quanto a foice curva da raiz até a ponta (sobe, arqueia, cai)
        cv = [(tot * f, 0, 0) for f in (0.14, 0.22, 0.24, 0.24, 0.16)]
        cauda.append(pena_bloco(f"cauda{k}", ((0.6 + 0.3 * k) * lado * (k > 0), 20.4 - 0.95 * k, 11.2 - 0.3 * k), L, 1.1, 4.6 - 0.25 * k,
                                (sobe, (3 + 3 * k) * lado * (k > 0), 0), cv, cor_cauda, partes=PARTES_FOICE))
    corpo.append(osso("cauda", [0, 18.0, 10.6], [0, 0, 0], cauda))

    # ---------- asas de inseto: a da frente grande, a de trás menor logo abaixo, presas no alto das costas ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        corpo.append(asa_inseto("asa_inseto_" + s, (3.0 * lado, 21.6, 2.4), 21.0, 8.6, lado, (0, -40 * lado, 31 * lado), 1))
        corpo.append(asa_inseto("asa_inseto2_" + s, (3.2 * lado, 20.0, 4.8), 15.5, 6.0, lado, (0, -46 * lado, -4 * lado), 2))

    tronco = osso("corpo", [0, 10.5, 3.0], [INCLINA, 0, 0], corpo)
    g.transformar(0, [tronco], (0, 0, 0), 1.0, sobe=-BAIXA)
    # pontas amarelas das penas, da cauda e da crista brilham no escuro (só os pixels amarelos)
    for pc in g.PECAS:
        if pc.nome.startswith(("asa", "cob", "cauda", "crista_")) and pc.brilho is False:
            pc.brilho = brilho_amarelo

    # ---------- pernas amarelo-alaranjadas, dedos amarelos com pontas roxo-escuras ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 3.4 * lado; zc = 3.4
        pp = []
        mperna = g.mat_cor(lambda p, f: mix(PERNA_ESC, PERNA, clamp((p[1] - 1.0) / 8.0)), borda=.08, curva=.3)
        pp += g.arredondado("coxa_" + s, [xc - 1.6, 7.0, zc - 1.6], [xc + 1.6, 10.0, zc + 1.6], mperna, r=0.45, faixa=(0, 8.6))
        pp.append(peca("canela_" + s, [xc - 1.35, 2.2, zc - 1.35], [xc + 1.35, 7.6, zc + 1.35], mperna, faixa=(0, 8.6)))
        mtorn = g.mat_cor(lambda p, f: mix(PERNA_ESC, PERNA, 0.35), borda=.14, curva=.3)
        pp.append(peca("tornozelo_" + s, [xc - 1.6, 1.0, zc - 1.75], [xc + 1.6, 2.8, zc + 1.5], mtorn, faixa=(0, 3.0)))
        md = g.mat_cor(lambda p, f: PERNA, borda=.15, curva=.4)
        mg = g.mat_facetado(GARRA_CLARA, GARRA, mix(GARRA, ROXO_ESC, 0.3), mix(GARRA, (20, 10, 24), 0.4), quina=-0.25)
        for nome, giro, dx in (("meio", 0, 0), ("fora", -24 * lado, 1.6 * lado), ("dentro", 24 * lado, -1.6 * lado)):
            x0, z0 = xc + dx, zc - 0.6
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .9, 0, z0 - 3.4], [x0 + .9, 1.7, z0 + 0.6], md, faixa=(0, 2.0)),
                peca(f"garra_{nome}_{s}", [x0 - 1.0, 0, z0 - 5.0], [x0 + 1.0, 1.9, z0 - 3.2], mg, faixa=(0, 2.0))]))
        pp.append(peca("dedo_tras_" + s, [xc - .7, 0, zc + 0.8], [xc + .7, 1.4, zc + 3.0], mg, faixa=(0, 2.0)))
        return osso("perna_" + s, [xc, 8.6, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

# ---------------- asas de inseto (placa recortada em folha, aro e nervuras douradas) ----------------
MEMB_RAIZ = (234, 166, 50); MEMB_MEIO = (206, 152, 82); MEMB_FUMO = (172, 132, 106); MEMB_HALO = (244, 192, 84)
VEIA = (255, 212, 52); VEIA_CLARA = (255, 238, 140)
BORDA_ASA = (255, 214, 44); BORDA_CLARA = (255, 248, 188); BORDA_ESC = (218, 140, 8)
BRILHA_ASA = {VEIA, VEIA_CLARA, BORDA_ASA, BORDA_CLARA}

def perfil_asa(s):
    """Meia largura (fração de W/2) da asa no ponto s (0 = raiz, 1 = ponta): raiz estreita, barriga larga um pouco
    antes do meio e ponta afilada (folha/gota alongada)."""
    if s < 0 or s > 1: return 0.0
    if s < 0.45: return 0.3 + 0.7 * math.sin(math.pi / 2 * s / 0.45)
    return max(0.0, 1 - ((s - 0.45) / 0.55) ** 1.7) ** 0.72

def asa_limites(L, W, s):
    """(centro, meia largura em cima, meia largura embaixo) da asa no ponto s: a borda de ataque (de cima) é mais
    reta e a ponta sobe um pouco."""
    off = W * 0.12 * s * s
    p = perfil_asa(s)
    return off, p * W / 2 * 0.8, p * W / 2 * 1.2

def mat_asa_inseto(raiz, L, W, semente):
    rx, ry, rz = raiz
    rnd = random.Random(semente)
    # células hexagonais: 2 fileiras alternadas ao longo da asa (a divisa entre elas é a nervura central em zigue-zague)
    sementes = []
    passo = 0.24
    for fil, lado_ in ((0, 1), (1, -1)):
        s = 0.06 + (passo / 2 if fil else 0.0)
        while s < 1.0:
            off, hc, hb = asa_limites(L, W, s)
            t = off + (0.5 * hc if lado_ > 0 else -0.5 * hb)
            sementes.append((s * L + rnd.uniform(-.25, .25), t + rnd.uniform(-.15, .15)))
            s += passo
    def f(c):
        x, y, z = c["p"]
        d = abs(x - rx); s = d / L
        t = y - ry
        off, hc, hb = asa_limites(L, W, s)
        hw = hc if t > off else hb
        if s <= 0 or s >= 1 or abs(t - off) > hw: return None
        borda = hw - abs(t - off)
        if c["face"] not in ("north", "south"): return BORDA_ASA
        if borda < 0.22: return BORDA_ESC                             # fio escuro de fora do aro
        if borda < 0.62: return BORDA_ASA                             # aro dourado grosso
        if borda < 0.82: return BORDA_CLARA                           # fio claro de dentro do aro
        ds = sorted((d - a) ** 2 + (t - b) ** 2 for a, b in sementes)[:2]
        d1, d2 = math.sqrt(ds[0]), math.sqrt(ds[1])
        e = (d2 - d1) / 2                                             # distância até a nervura
        if e < 0.14: return VEIA_CLARA
        if e < 0.3: return VEIA
        k = clamp((e - 0.3) / 1.1)
        memb = mix(MEMB_RAIZ, MEMB_MEIO, clamp(s / 0.5)) if s < 0.5 else mix(MEMB_MEIO, MEMB_FUMO, (s - 0.5) / 0.5)
        if t < off: memb = mix(memb, MEMB_RAIZ, 0.25)                 # metade de baixo mais âmbar (como na arte)
        return mix(MEMB_HALO, memb, k)
    return f

def brilho_asa(c, cor):
    return tuple(cor) in BRILHA_ASA

def asa_inseto(nome, raiz, L, W, lado, rot, semente, esp=0.22):
    x, y, z = raiz
    x0, x1 = sorted((x, x + L * lado))
    return osso(nome, list(raiz), list(rot), [
        peca(nome, [x0, y - W * 0.62 - 0.3, z - esp / 2], [x1, y + W * 0.55 + 0.3, z + esp / 2], mat_asa_inseto(raiz, L, W, semente),
             res=5, brilho=brilho_asa)])

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

# ---------------- LOD ----------------
# O lod_auto.py escolhe sozinho o que some de longe, mas tira peças que seguram outras (base do bico, dedo sem a
# garra, fatia do bulbo...) e aí sobram cubos soltos no ar. Aqui o lods.json é filtrado: a estrutura nunca some
# (crânio, olhos, bico, barbela, pescoço, tronco, peito, garupa, bulbo, pernas, dedos e garras) e o resto some
# inteiro, por grupo (cada pena/dedo da crista/foice da cauda é uma cadeia que sai junta).
import json as _json, re as _re
ESTRUTURA = _re.compile(r"^(cranio|faceta|bico|barbela|pescoco|tronco|peito_[abc]$|garupa|lanterna|coxa|canela|tornozelo|dedo_|garra_|"
                        r"asa_inseto|crista_base)")

def _lods_filtrados():
    arq = Path(__file__).resolve().parent.parent.parent / "modelos" / ID / "lods.json"
    if not arq.exists(): return None
    bruto = _json.loads(arq.read_text(encoding="utf-8"))
    nivel_de = {}
    for n, pads in bruto.items():
        for pad in pads:
            miolo = pad[len("^(?:"):-len(")$")] if pad.startswith("^(?:") else pad
            for nome in miolo.split("|"):
                nome = nome.replace("\\", "")
                if not ESTRUTURA.match(nome): nivel_de.setdefault(nome, int(n))
    # uma cadeia (pena, foice, dedo da crista) some inteira, no nível do primeiro segmento que sumir
    cadeia = lambda nome: _re.sub(r"_\d+$", "", nome)
    menor = {}
    for nome, n in nivel_de.items(): menor[cadeia(nome)] = min(n, menor.get(cadeia(nome), 99))
    nivel_de = {nome: menor[cadeia(nome)] for nome in nivel_de}
    out = {}
    for nome, n in nivel_de.items(): out.setdefault(n, []).append(nome)
    return {n: ["^(?:" + "|".join(_re.escape(x) for x in sorted(v)) + ")$"] for n, v in sorted(out.items())} or None

LODS = _lods_filtrados()

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

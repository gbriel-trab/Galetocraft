"""Cocórion (#005, Ar): o Galo dos Ventos, galo guerreiro branco de crista espetada, cicatrizes de batalha, asas em
capa com a espiral verde do vento, calça hakama preta com faixa branca e katana na cintura.

Versão "suave" (rodadas s*): poucas peças grandes e bem desenhadas. Cabeça, pescoço e tronco em volumes chanfrados
(arredondado/arredondado2/octogono); crista de poucas mechas grandes que afinam e varrem para trás a partir de uma
base comum; asa em capa estreita colada ao corpo (3 faixas que abraçam o tronco); cauda de penas finas e compridas
num leque estreito; pernas finas. A luz é pintada em degradê contínuo pelo grupo, sem contraste por cubo."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
import previa                                  # só a matriz de rotação (mesma ordem do Blockbench)
from galo_base import peca, osso, mix, clamp, na_borda

ID = "cocorion"; NOME = "Cocórion"; NUMERO = 5
ALTURA = 2.4
QUADRUPEDE = False
ROSTO = ((0, 29.0, -5.0), 7.5)
N_CAUDA, SEG_CAUDA = 6, 4
ONDAS = [(f"cauda{k}", SEG_CAUDA, (1.6, 1.2, 0.0)) for k in range(N_CAUDA)]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (amostrada nos PNGs da ficha; veja modelos/cocorion/detalhes.md) ----------------
BRANCO_F = (255, 238, 224); CLARO_F = (255, 247, 238)
LINHA_F = (226, 212, 200)                 # sombra entre as penas (cinza-claro quente)
CARVAO = (44, 45, 44); PRETO_H = (27, 28, 25); CARVAO_CL = (58, 60, 60)
VERDE = (58, 106, 48); VERDE_ESC = (38, 78, 26)
AMAR = (255, 192, 14); AMAR_ESC = (232, 140, 0); AMAR_CL = (255, 214, 70)
LARANJA_B = (238, 162, 10)
VERM = (204, 52, 38); VERM_ESC = (150, 30, 22); VERM_X = (186, 42, 32)
OURO = (250, 184, 12); OURO_CL = (255, 214, 80); OURO_ESC = (190, 122, 8)
PRETO_SOB = (40, 38, 36)
GARRA = (46, 46, 46)

LADO_KATANA = -1          # nas vistas, o lado -x aparece à direita de quem olha de frente (como a katana da ficha)
LADO_CICATRIZ = 1         # X da bochecha e marca da testa do lado que a arte mostra


def escuro(c): return (int(c[0] * .80), int(c[1] * .77), int(c[2] * .80))
def tons(c, f):
    f = clamp(f, -1, 1)
    return mix(c, CLARO_F, f) if f >= 0 else mix(c, escuro(c), -f)

def matriz(*rots):
    M = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    for r in rots: M = previa.mm(M, previa.rot(*r))
    return M

def mat_luz(cor_fn, M=None, borda=.05, grad=0.5, topo=.25, baixo=-.45):
    """Luz chapada pela normal no mundo (face de cima clara, de baixo na sombra) mais um degradê contínuo de
    altura pela faixa do GRUPO (todas as peças do grupo usam a mesma faixa: a luz atravessa as peças sem realçar
    cada cubo). Fio de borda bem leve."""
    def f(c):
        base = cor_fn(c)
        if base is None: return None
        nx, ny, nz = previa.mv(M, g.NORMAL[c["face"]]) if M else g.NORMAL[c["face"]]
        k = topo if ny > 0.6 else baixo if ny < -0.6 else 0.05 * ny
        y0, y1 = c["faixa"]
        k += grad * (clamp((c["p"][1] - y0) / max(y1 - y0, 1e-6)) - 0.6)
        if na_borda(c): k -= borda
        return tons(base, k)
    return f

def cor_fixa(cor): return lambda c: cor

def escama(a, y, larg=2.2, alt=1.7):
    """Penas em escama, grandes e suaves: só uma linha fina em arco embaixo de cada pena."""
    fila = math.floor(y / alt)
    fa = ((a + (fila % 2) * larg / 2) % larg) / larg
    fy = (y % alt) / alt
    return fy < 0.09 + 0.16 * (2 * abs(fa - 0.5)) ** 2

def risco_x(a, y, ca, cy, r, w=0.3, torto=0.0):
    da, dy = a - ca, y - cy
    if max(abs(da), abs(dy)) > r: return False
    j = torto * math.sin(round(da * 2) * 1.7 + round(dy * 2) * 0.9)
    return abs(da - dy + j) < w or abs(da + dy - j) < w

FAIXA_BRANCA = (10.0, 38.0)              # um degradê só para tudo o que é branco (corpo, asas, cabeça, crista)

# ---------------- mecha (crista e tufos) ----------------
def mecha(nome, raiz, rot, L, W, T=None, curva=8.0, gira=0, faixa=FAIXA_BRANCA):
    """Mecha grande: base larga que nasce dentro do crânio, um segundo bloco mais estreito que dobra 'curva' graus e
    a ponta em losango. Cresce em +y a partir da raiz; 'rot' aponta a mecha; gira=0: lâmina larga vista de lado
    (largura em z); gira=90: larga vista de frente."""
    T = T or max(W * 0.42, 1.0)
    x, y, z = raiz
    M0 = matriz(rot, (0, gira, 0))
    def cor(c):
        return mix(BRANCO_F, CLARO_F, 0.35)
    L0, L1 = L * 0.56, L * 0.30
    w1 = W * 0.64
    m0 = mat_luz(cor, M0)
    p0 = peca(nome + "_0", [x - T / 2, y - 1.2, z - W / 2], [x + T / 2, y + L0, z + W / 2], m0, faixa=faixa)
    M1 = previa.mm(M0, previa.rot(curva, 0, 0))
    y1 = y + L0 - 0.3
    p1 = peca(nome + "_1", [x - T * 0.42, y1 - 0.3, z - w1 / 2], [x + T * 0.42, y1 + L1, z + w1 / 2], mat_luz(cor, M1), faixa=faixa)
    q = w1 / 1.4142; cy = y1 + L1
    pt = peca(nome + "_p", [x - T * 0.3, cy - q / 2, z - q / 2], [x + T * 0.3, cy + q / 2, z + q / 2],
              mat_luz(cor, previa.mm(M1, previa.rot(45, 0, 0))), rot=(45, 0, 0), pivo=(x, cy, z), faixa=faixa)
    return osso(nome, list(raiz), list(rot), [osso(nome + "_g", list(raiz), [0, gira, 0], [
        p0, osso(nome + "_c", [x, y1, z], [curva, 0, 0], [p1, pt])])])

# ---------------- cabeça ----------------
EY = 29.2                                   # altura do olho
FX, ZF, QX = 1.2, -6.2, 3.6                 # meia largura da frente, z da frente, meia largura do crânio
ZQ = ZF + (QX - FX)
FAC_T = 1.6
FAC_L = (QX - FX) * 1.4142
FAC_O = ((FX + QX) / 2, (ZF + ZQ) / 2)
FAC_C = (FAC_O[0] - 0.7071 * FAC_T / 2, FAC_O[1] + 0.7071 * FAC_T / 2)
OLHO_U, OLHO_RU, OLHO_RV = 0.1, 1.35, 0.78
SOB_K = 0.42
SOB_Y = 0.6

def olho(u, v):
    """Olho estreito da ficha: topo cortado na diagonal pela sobrancelha; íris verde-viva nos 2/3 do lado do bico,
    pupila preta junto à borda da frente com brilho; esclera branca atrás."""
    du = u - OLHO_U
    ru, rv = OLHO_RU, OLHO_RV
    if abs(du) > ru or abs(v) > rv: return None
    cq = max(0.0, abs(du) - (ru - 0.32)) / 0.32, max(0.0, abs(v) - (rv - 0.32)) / 0.32
    if cq[0] ** 2 + cq[1] ** 2 > 1: return None
    if v > SOB_Y - 0.06 + SOB_K * du: return None
    if du < ru / 3:
        pu = du + ru - 0.5
        if (pu / 0.3) ** 2 + ((v + 0.05) / 0.45) ** 2 <= 1:
            if ((pu - 0.1) / 0.12) ** 2 + ((v - 0.16) / 0.12) ** 2 <= 1: return (255, 255, 255)
            return (10, 12, 10)
        return mix((70, 206, 50), (30, 140, 22), clamp((0.4 - v) / 1.2))
    return (255, 255, 255)

def cor_rosto(c): return BRANCO_F

def mat_faceta(lado):
    """Face diagonal do rosto: olho inteiro numa face plana; X na bochecha do lado da arte, riscos do outro."""
    fora = "east" if lado > 0 else "west"
    def desenho(c):
        x, y, z = c["p"]
        if c["face"] != fora: return None
        u, v = z - FAC_C[1], y - EY
        o = olho(u, v)
        if o is not None: return o
        if lado == LADO_CICATRIZ:
            if risco_x(u, v, 0.2, -1.75, 0.62, 0.15, torto=0.08): return VERM
        else:
            if abs((v + 1.3) - 0.8 * (u - 0.9)) < 0.13 and abs(u - 0.9) < 0.45: return VERM
            if (u - 0.2) ** 2 + (v + 1.6) ** 2 < 0.035: return VERM
        return None
    base = mat_luz(cor_rosto, matriz((0, 45 * lado, 0)), borda=.0)
    def f(c):
        d = desenho(c)
        return d if d is not None else base(c)
    return f

def mat_bico(M=None):
    def cor(c):
        x, y, z = c["p"]
        if c["face"] in ("east", "west") and abs(z - (ZF - 1.0)) < 0.26 and abs(y - 28.55) < 0.22: return PRETO_H
        return AMAR if c["face"] != "down" else AMAR_ESC
    return mat_luz(cor, M, borda=.06, grad=0.0, topo=.2, baixo=-.35)

def cor_testa(c):
    """Testa: pequena cruz vermelha de traço fino acima do olho do lado da arte."""
    x, y, z = c["p"]
    if c["face"] == "north":
        da, dy = x - 1.25 * LADO_CICATRIZ, y - 31.0
        if max(abs(da), abs(dy)) < 0.6 and (abs(da - dy) < 0.15 or abs(da + dy) < 0.15): return VERM
        if abs(da - 0.75) < 0.12 and abs(dy - 0.5) < 0.12: return VERM
    return BRANCO_F

def montar_cabeca():
    cab = []
    mb = mat_luz(cor_rosto)
    # crânio: volume bem chanfrado, largo em cima, afinando para o bico pela frente em planos inclinados
    cab += g.arredondado2("cranio", [-QX, 25.4, ZQ - 0.2], [QX, 32.4, 2.4], mb, r=1.4, faixa=FAIXA_BRANCA)
    cab.append(peca("rosto_frente", [-FX - 0.05, 25.3, ZF], [FX + 0.05, 30.4, ZQ + 0.4], mb, faixa=FAIXA_BRANCA))
    cab.append(peca("testa", [-2.5, 29.9, ZF + 0.15], [2.5, 32.4, ZQ + 1.2], mat_luz(cor_testa, matriz((20, 0, 0))),
                    rot=(20, 0, 0), pivo=(0, 29.9, ZF + 0.15), faixa=FAIXA_BRANCA, res=6))
    cab.append(peca("queixo", [-2.2, 24.6, ZF + 0.8], [2.2, 26.2, ZQ + 2.4], mb, rot=(-14, 0, 0), pivo=(0, 26.2, ZQ + 2.4),
                    faixa=FAIXA_BRANCA))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 25.3, cz - FAC_L / 2], [cx + FAC_T / 2, 30.6, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, EY, cz), faixa=FAIXA_BRANCA, res=8))
        # sobrancelha: bloco preto grosso, à frente do olho, descendo para o bico (V de frente)
        xo = cx + FAC_T / 2 * lado
        x0, x1 = sorted((xo - 0.3 * lado, xo + 0.45 * lado))
        yb = EY + SOB_Y
        rs = (-math.degrees(math.atan(SOB_K)), 0, 0)
        msob = mat_luz(cor_fixa(PRETO_SOB), matriz((0, 45 * lado, 0), rs), borda=.0, grad=0.0, topo=.3, baixo=-.2)
        cab.append(osso("sobrancelha_" + s, [cx, EY, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, yb, cz - FAC_L / 2 - 0.3], [x1, yb + 1.25, cz + FAC_L / 2 + 0.5], msob,
                 rot=rs, pivo=(cx, yb, cz + OLHO_U))]))
        yq = yb - SOB_K * (FAC_L / 2 + OLHO_U)
        x0, x1 = sorted((0.5 * lado, (FX + 0.4) * lado))
        cab.append(peca("sobrancelha_f_" + s, [x0, yq - 0.05, ZF - 0.55], [x1, yq + 1.2, ZF + 0.35],
                        mat_luz(cor_fixa(PRETO_SOB), borda=.0, grad=0.0, topo=.3), rot=(0, 0, 24 * lado),
                        pivo=(FX * lado, yq, ZF)))
    # bico em cunha: base larga, meio, gancho estreito; mandíbula de baixo mais escura e recuada
    mbi = mat_bico()
    cab.append(peca("bico_cima", [-1.55, 27.9, ZF - 2.8], [1.55, 29.0, ZF + 0.5], mbi, res=4))
    cab.append(peca("bico_meio", [-1.1, 27.15, ZF - 3.1], [1.1, 28.05, ZF + 0.5], mbi, res=4))
    cab.append(peca("bico_gancho", [-0.55, 26.95, ZF - 3.5], [0.55, 28.6, ZF - 2.75], mbi, res=4))
    cab.append(peca("bico_baixo", [-0.95, 26.35, ZF - 2.2], [0.95, 27.25, ZF + 0.4],
                    mat_luz(cor_fixa(LARANJA_B), borda=.1, grad=0.0, topo=.1), res=4))
    # barbelas: dois lóbulos vermelhos compridos sob o bico, o de cá um pouco mais comprido
    def cor_barb(c):
        if abs(c["p"][0]) < 0.2: return VERM_ESC
        return mix((228, 52, 40), (190, 38, 28), clamp((26.0 - c["p"][1]) / 3.0))
    mbar = mat_luz(cor_barb, borda=.15, grad=0.0, topo=.1)
    for lado, fim in ((-1, 23.6), (1, 23.9)):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.0, 1.45 * lado)); x2, x3 = sorted((0.2 * lado, 1.15 * lado))
        cab.append(osso("barbela_" + s, [0.0, 26.4, ZF - 1.0], [0, 0, -3 * lado], [
            peca("barbela_a_" + s, [x0, fim + 0.9, ZF - 1.7], [x1, 26.5, ZF - 0.2], mbar, res=4),
            peca("barbela_b_" + s, [x2, fim, ZF - 1.5], [x3, fim + 1.0, ZF - 0.45], mbar, res=4)]))
    # crista: base comum que abraça o alto e a nuca do crânio; poucas mechas grandes varridas para trás
    crista = []
    crista += g.arredondado("crista_base", [-2.9, 31.0, -4.4], [2.9, 33.4, 2.6], mat_luz(cor_rosto, matriz((12, 0, 0))),
                            r=0.8, rot=(12, 0, 0), pivo=(0, 32.0, -1.0), faixa=FAIXA_BRANCA)
    crista += [
        mecha("crista_1", (0.3, 32.6, -3.2), (14, 0, -4), 6.2, 3.4, curva=12),
        mecha("crista_2", (-0.3, 33.0, -1.4), (34, 0, 4), 7.6, 3.8, curva=12),
        mecha("crista_3", (0.2, 32.6, 0.6), (58, 0, -3), 7.4, 3.6, curva=10),
        mecha("crista_4", (0.0, 31.0, 2.0), (86, 0, 2), 6.4, 3.2, curva=8),
        mecha("crista_5", (0.0, 28.8, 2.2), (114, 0, 0), 5.0, 2.8, curva=6),
        mecha("crista_d", (-1.9, 32.4, -2.0), (24, 0, 28), 6.0, 2.8, curva=10, gira=90),
        mecha("crista_e", (1.9, 32.6, -1.4), (30, 0, -34), 6.6, 2.8, curva=10, gira=90),
        mecha("orelha_d", (-3.0, 30.4, 0.0), (58, 0, 60), 5.0, 2.6, curva=8, gira=90),
        mecha("orelha_e", (3.0, 30.6, 0.2), (52, 0, -64), 5.4, 2.6, curva=8, gira=90),
        # tufos da bochecha: pontas varridas para trás atrás do olho
        mecha("tufo_d", (-3.2, 27.4, 0.8), (92, 0, 22), 4.6, 2.6, curva=6),
        mecha("tufo_e", (3.2, 27.6, 0.8), (90, 0, -24), 4.8, 2.6, curva=6),
    ]
    cab.append(osso("crista", [0, 32.0, -1.0], [0, 0, 0], crista))
    return osso("cabeca", [0, 26.4, -1.0], [0, 0, 0], cab)

# ---------------- tronco ----------------
def cor_tronco(c):
    x, y, z = c["p"]
    face = c["face"]
    if face == "north" and z < -4.6:
        if risco_x(x, y, 0.0, 19.0, 2.5, 0.38, torto=0.08):
            pontas = max(abs(x), abs(y - 19.0)) > 2.0
            return (142, 31, 26) if pontas and (round(x * 2) + round(y * 2)) % 2 == 0 else VERM_X
    a = z if face in ("east", "west") else x
    if face != "up" and escama(a, y): return mix(BRANCO_F, LINHA_F, 0.6)
    return BRANCO_F

def montar_tronco():
    """Tronco de ave esguio: núcleo bem chanfrado que afunila para a cintura, peito com projeção moderada (quilha
    inclinada), dorso em capa e uma gola de 3 pontas na base do pescoço."""
    pc = []
    mt = mat_luz(cor_tronco)
    pc += g.arredondado2("tronco", [-3.4, 13.4, -3.8], [3.4, 24.0, 3.4], mt, r=1.5, faixa=FAIXA_BRANCA, res=3)
    pc += g.arredondado("peito", [-2.8, 15.4, -5.3], [2.8, 23.2, -2.4], mat_luz(cor_tronco, matriz((-5, 0, 0))), r=0.9,
                        rot=(-5, 0, 0), pivo=(0, 15.4, -3.0), faixa=FAIXA_BRANCA, res=3)
    mg = mat_luz(lambda c: mix(BRANCO_F, CLARO_F, 0.3), matriz((0, 0, 45)))
    q = 2.6 / 1.4142
    for k, (x, y) in enumerate(((-1.8, 22.3), (0.0, 21.8), (1.8, 22.3))):
        pc.append(peca(f"gola{k}", [x - q / 2, y - q / 2, -5.6], [x + q / 2, y + q / 2, -4.6], mg, rot=(0, 0, 45),
                       pivo=(x, y, -5.1), faixa=FAIXA_BRANCA))
    # dorso: capa de penas do pescoço até a raiz da cauda, borda de baixo em 3 pontas
    mc = mat_luz(lambda c: mix(BRANCO_F, LINHA_F, 0.6) if c["face"] == "south" and escama(c["p"][0], c["p"][1]) else BRANCO_F)
    pc += g.arredondado("dorso", [-3.2, 14.2, 2.4], [3.2, 23.6, 4.6], mc, r=0.8, rot=(8, 0, 0), pivo=(0, 23.6, 3.0),
                        faixa=FAIXA_BRANCA)
    q = 2.8 / 1.4142
    for k, x in enumerate((-1.9, 0.0, 1.9)):
        yb = 14.4 - (0.5 if k == 1 else 0.0)
        pc.append(peca(f"dorso_ponta{k}", [x - q / 2, yb - q / 2, 3.6], [x + q / 2, yb + q / 2, 5.0], mc, rot=(0, 0, 45),
                       pivo=(x, yb, 4.3), faixa=FAIXA_BRANCA))
    return pc

def cor_hakama(c):
    x, y, z = c["p"]
    face = c["face"]
    a = z if face in ("east", "west") else x
    if face == "up": return CARVAO_CL
    if y < 7.6 and face != "down": return PRETO_H
    return CARVAO if math.floor((a + 0.3) / 1.5) % 2 == 0 else (54, 56, 58)

# ---------------- asas ----------------
def _curva_glifo():
    pts = []
    te = 2.5 * math.pi
    for k in range(60):
        th = te * k / 59
        r = 0.45 + 0.42 * th
        ph = te - th - math.pi / 2
        pts.append((r * math.cos(ph), r * math.sin(ph)))
    ue, ve = pts[-1]
    return pts + [(ue - 1.0, ve - 1.2), (ue - 2.0, ve - 2.6), (ue - 2.6, ve - 3.4), (ue - 3.1, ve - 3.5), (ue - 3.4, ve - 3.0)]
GLIFO_P = _curva_glifo()
GLIFO_C = (18.6, -0.4)                   # (y, z) do centro da espiral (terço de cima da capa)
GLIFO_K = 0.62
GLIFO_W = 0.66

def _dist_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = clamp(((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy + 1e-9))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

def glifo(y, z):
    a, v = -(z - GLIFO_C[1]) / GLIFO_K, (y - GLIFO_C[0]) / GLIFO_K
    if not (-9.0 < a < 4.5 and -10.0 < v < 4.5): return False
    return any(_dist_seg(a, v, *GLIFO_P[i], *GLIFO_P[i + 1]) < GLIFO_W for i in range(len(GLIFO_P) - 1))

def mat_asa(lado, M, cor=BRANCO_F, glifo_ok=True):
    fora = "east" if lado > 0 else "west"
    def c_(c):
        x, y, z = c["p"]
        if c["face"] == fora and cor == BRANCO_F and escama(z, y, 2.6, 2.2): return mix(BRANCO_F, LINHA_F, 0.6)
        return cor
    m = mat_luz(c_, M)
    def f(c):
        if glifo_ok and c["face"] == fora and glifo(c["p"][1], c["p"][2]): return VERDE
        return m(c)
    return f

def faixa_asa(nome, lado, z0, z1, y0, y1, xi, esp, ry, piv_z, ROT, pt_alt):
    """Faixa da capa (bloco com espessura) + ponta em losango embaixo; 'ry' gira a faixa em volta do eixo vertical
    para ela abraçar o tronco."""
    x0, x1 = sorted((xi, xi + esp * lado))
    M = matriz(ROT, (0, ry, 0))
    m = mat_asa(lado, M)
    w = z1 - z0; zc = (z0 + z1) / 2
    q = w * pt_alt / 1.4142
    pcs = [peca(nome, [x0, y0, z0], [x1, y1, z1], m, faixa=FAIXA_BRANCA, res=3),
           peca(nome + "_p", [x0 + 0.04, y0 - q / 2, zc - q / 2], [x1 - 0.04, y0 + q / 2, zc + q / 2],
                mat_asa(lado, previa.mm(M, previa.rot(45, 0, 0)), glifo_ok=False), rot=(45, 0, 0), pivo=(xi, y0, zc),
                faixa=FAIXA_BRANCA, res=3)]
    return osso(nome, [xi, y1, piv_z], [0, ry, 0], pcs)

def montar_asa(lado):
    """Capa estreita colada ao corpo: ombro arredondado e 3 faixas (frente, meio, trás) que abraçam o tronco, cada
    uma terminando numa ponta; 2 penas verdes por dentro, atrás. A espiral fica na faixa do meio e na da frente."""
    s = "d" if lado < 0 else "e"
    xi = 3.25 * lado
    PIV = (xi, 23.6, -0.4)
    ROT = (-5, 0, 5 * lado)
    M = matriz(ROT)
    pc = []
    x0, x1 = sorted((xi - 1.2 * lado, xi + 1.55 * lado))
    pc += g.arredondado("asa_ombro_" + s, [x0, 20.6, -4.5], [x1, 24.8, 3.6], mat_asa(lado, M, glifo_ok=False), r=1.0,
                        faixa=FAIXA_BRANCA)
    pc.append(faixa_asa("asa_frente_" + s, lado, -4.6, -1.5, 13.0, 23.4, xi + 0.05 * lado, 1.2, 18 * lado, -1.5, ROT, 1.0))
    pc.append(faixa_asa("asa_meio_" + s, lado, -1.7, 1.5, 10.2, 23.6, xi + 0.15 * lado, 1.25, 0, 0.0, ROT, 1.0))
    pc.append(faixa_asa("asa_tras_" + s, lado, 1.3, 4.2, 11.4, 23.4, xi + 0.05 * lado, 1.2, -18 * lado, 1.3, ROT, 1.0))
    # penas verdes por dentro (aparecem atrás e embaixo)
    for k, (z, y0, L) in enumerate(((2.6, 9.6, 6.0), (0.4, 8.8, 5.0))):
        xa0, xa1 = sorted((xi - 0.2 * lado, xi + 0.7 * lado))
        mv = mat_asa(lado, matriz(ROT, (6, 0, 0)), cor=VERDE, glifo_ok=False)
        q = 2.2 / 1.4142
        pc.append(osso(f"asa_verde{k}_{s}", [xi, y0 + L, z], [6, 0, 0], [
            peca(f"asa_verde{k}_{s}", [xa0, y0, z - 1.1], [xa1, y0 + L, z + 1.1], mv, faixa=FAIXA_BRANCA),
            peca(f"asa_verde{k}_{s}_p", [xa0 + 0.03, y0 - q / 2, z - q / 2], [xa1 - 0.03, y0 + q / 2, z + q / 2], mv,
                 rot=(45, 0, 0), pivo=(xi, y0, z), faixa=FAIXA_BRANCA)]))
    return osso("asa_" + s, list(PIV), list(ROT), pc)

# ---------------- cauda ----------------
def mat_pena_cauda(M, t0, t1, verde):
    """Pena da cauda: creme por cima e nas pontas, verde-escuro embaixo e perto da raiz (alternando por pena)."""
    def cor(c):
        (_, y0, z0), (_, y1, z1) = c["b"]
        fy = (c["p"][1] - y0) / max(y1 - y0, 1e-6)
        t = t0 + (t1 - t0) * clamp((c["p"][2] - z0) / max(z1 - z0, 1e-6))
        face = c["face"]
        if verde:
            if t > 0.7 or face == "south": return BRANCO_F
            return VERDE_ESC if face == "down" else VERDE
        if face in ("up", "south", "north"): return BRANCO_F
        if t < 0.55 and (face == "down" or fy < 0.45): return VERDE_ESC if face == "down" else VERDE
        return BRANCO_F
    return mat_luz(cor, M, grad=0.0)

def pena_cauda(nome, raiz, rot0, curvas, L, H, esp, verde=False):
    """Pena fina e comprida: 4 blocos encadeados e sobrepostos nas juntas (ossos '<nome>_k'), estreita na raiz,
    mais alta no meio e ponta em losango; 'curvas' dá o giro de cada junta."""
    fr = [0.24, 0.28, 0.26, 0.22]
    alt = [0.55, 0.95, 0.85, 0.6]
    ee = [0.9, 1.0, 0.95, 0.85]
    n = len(fr)
    def seg(k, pos, M, t0):
        px, py, pz = pos
        h = H * alt[k]; Ls = L * fr[k]; e = esp * ee[k]
        r = list(rot0) if k == 0 else [curvas[k - 1], 0, 0]
        Mk = previa.mm(M, previa.rot(*r))
        t1 = t0 + fr[k]
        ov = 0.8 if k > 0 else 0.4
        filhos = [peca(f"{nome}_{k}", [px - e / 2, py - h * 0.5, pz - ov], [px + e / 2, py + h * 0.5, pz + Ls],
                       mat_pena_cauda(Mk, t0, t1, verde), faixa=(py - h, py + h), res=3)]
        if k + 1 < n:
            filhos.append(seg(k + 1, (px, py, pz + Ls - 0.1), Mk, t1))
        else:
            q = h * 1.1 / 1.4142
            filhos.append(peca(f"{nome}_pt", [px - e * 0.4, py - q / 2, pz + Ls - q / 2], [px + e * 0.4, py + q / 2, pz + Ls + q / 2],
                               mat_pena_cauda(previa.mm(Mk, previa.rot(45, 0, 0)), 0.95, 1.0, verde), rot=(45, 0, 0),
                               pivo=(px, py, pz + Ls), res=3))
        return osso(f"{nome}_{k}", list(pos), r, filhos)
    return seg(0, raiz, matriz(), 0.0)

def montar_cauda():
    """Leque estreito de 6 penas finas e compridas: sobem e varrem para trás saindo de uma raiz estreita na cintura,
    cada uma curvando a ponta para baixo; abertas pouco para os lados."""
    penas = []
    # (x, raiz y, z, elevação, giro y, curvas, comprimento, altura, espessura, verde)
    P = [(-0.3, 17.4, 3.6, 70, 0, (-4, 6, 14), 13.0, 2.4, 1.0, False),
         (0.4, 16.8, 3.8, 54, -4, (-4, 6, 13), 15.0, 2.2, 0.9, True),
         (-0.4, 16.2, 3.9, 40, 5, (-4, 6, 12), 16.5, 2.4, 1.0, False),
         (0.3, 15.6, 4.0, 26, -6, (-3, 5, 11), 16.5, 2.2, 0.9, True),
         (-0.2, 15.0, 4.0, 13, 7, (-3, 5, 10), 15.0, 2.2, 0.9, False),
         (0.2, 14.6, 3.8, 0, -3, (-2, 4, 8), 12.5, 2.0, 0.85, True)]
    for k, (x, y, z, e, ry, cv, L, H, esp, vd) in enumerate(P):
        penas.append(pena_cauda(f"cauda{k}", (x, y, z), (-e, ry, 0), cv, L, H, esp, vd))
    return osso("cauda", [0, 15.6, 3.8], [0, 0, 0], penas)

# ---------------- katana ----------------
def mat_metal(cima, frente, lado, baixo):
    return g.mat_facetado(cima, frente, lado, baixo, quina=-0.3)

def mat_cabo(c):
    x, y, z = c["p"]
    t = (z - c["b"][0][2]) % 1.2
    meio = abs((c["j"] + 0.5) / c["th"] - 0.5) if c["face"] in ("east", "west") else abs((c["i"] + 0.5) / c["tw"] - 0.5)
    if c["face"] in ("east", "west", "up", "down") and 0.3 < t < 0.9 and meio < 0.3: return BRANCO_F
    return VERDE_ESC if na_borda(c) else VERDE

def montar_katana(base):
    """Katana ao longo de z (cabo para a frente, bainha para trás) a partir da tsuba em 'base'."""
    bx, by, bz = base
    def pc_(nome, de, ate, mat, **kw):
        return g.peca(nome, [de[0] + bx, de[1] + by, de[2] + bz], [ate[0] + bx, ate[1] + by, ate[2] + bz], mat, **kw)
    ouro = mat_metal(OURO_CL, OURO, mix(OURO, OURO_ESC, .4), OURO_ESC)
    bainha = mat_metal((70, 72, 78), (36, 38, 42), (28, 30, 34), (16, 16, 20))
    return [pc_("katana_cabo", [-0.7, -0.7, -6.4], [0.7, 0.7, -0.3], mat_cabo, res=4),
            pc_("katana_pomo", [-0.8, -0.8, -7.0], [0.8, 0.8, -6.35], ouro, res=4),
            pc_("katana_tsuba_a", [-1.8, -0.65, -0.4], [1.8, 0.65, 0.2], ouro, res=4),
            pc_("katana_tsuba_b", [-0.65, -1.8, -0.35], [0.65, 1.8, 0.15], ouro, res=4),
            pc_("katana_bainha", [-0.55, -0.7, 0.1], [0.55, 0.7, 14.0], bainha),
            pc_("katana_kurikata", [-0.65, -0.8, 1.6], [0.65, 0.8, 2.3], ouro, res=4),
            pc_("katana_kojiri", [-0.6, -0.75, 13.8], [0.6, 0.75, 15.0], ouro, res=4)]

# ---------------- pernas ----------------
def perna(lado):
    """Hakama de uma perna (prisma chanfrado que abre um pouco embaixo + painel da frente) e perna de ave fina:
    tarso octogonal, tornozelo, 3 dedos à frente com garras escuras e 1 atrás."""
    s = "d" if lado < 0 else "e"; xc = 2.2 * lado; zc = 0.4
    pp = []
    def bx(a, b): return sorted((a * lado, b * lado))
    mh = mat_luz(cor_hakama, grad=0.4, topo=.15, baixo=-.4)
    x0, x1 = bx(0.1, 4.2)
    pp += g.octogono("hakama_" + s, [x0, 7.0, -4.2], [x1, 13.6, 3.8], mh, r=1.0, faixa=(6, 14), rot=(0, 0, 5 * lado),
                     pivo=(2.0 * lado, 13.6, 0))
    x0, x1 = bx(0.3, 3.7)
    pp.append(peca("hakama_frente_" + s, [x0, 7.1, -4.7], [x1, 13.2, -3.9], mh, rot=(7, 0, 4 * lado),
                   pivo=(2.0 * lado, 13.2, -4.3), faixa=(6, 14)))
    ma = mat_luz(lambda c: AMAR if c["face"] != "down" else AMAR_ESC, grad=0.3, topo=.2, baixo=-.3, borda=.08)
    pp += g.octogono("tarso_" + s, [xc - 0.85, 1.6, zc - 0.85], [xc + 0.85, 8.0, zc + 0.85], ma, r=0.3, faixa=(0, 8))
    pp += g.octogono("tornozelo_" + s, [xc - 1.1, 0.9, zc - 1.1], [xc + 1.1, 2.4, zc + 1.1], ma, r=0.35, faixa=(0, 8))
    mg = mat_luz(cor_fixa(GARRA), grad=0.0, borda=.1, topo=.3)
    for nome, dx, ang, comp in (("meio", 0.0, 0, 2.8), ("fora", 1.15 * lado, 24 * lado, 2.3), ("dentro", -1.15 * lado, -20 * lado, 2.2)):
        x0 = xc + dx
        pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, zc - 0.4], [0, -ang, 0], [
            peca(f"dedo_{nome}_{s}", [x0 - .65, 0, zc - 0.4 - comp], [x0 + .65, 1.5, zc + 0.6], ma, faixa=(0, 8)),
            peca(f"garra_{nome}_{s}", [x0 - .5, 0.0, zc - 0.4 - comp - 1.2], [x0 + .5, 1.15, zc - 0.3 - comp], mg)]))
    mtras = mat_luz(lambda c: GARRA if c["p"][2] > zc + 2.6 else AMAR, grad=0.3, faixa=None) if False else \
        mat_luz(lambda c: GARRA if c["p"][2] > zc + 2.5 else (AMAR if c["face"] != "down" else AMAR_ESC), grad=0.3, borda=.08)
    pp.append(peca("dedo_tras_" + s, [xc - .5, 0, zc + 0.6], [xc + .5, 1.1, zc + 3.4], mtras, faixa=(0, 8)))
    return osso("perna_" + s, [xc, 13.0, zc], [0, 0, 0], pp)

# ---------------- montagem ----------------
def montar():
    corpo = []
    corpo += montar_tronco()
    # cintura da hakama e faixa branca com nó e duas tiras
    mh = mat_luz(cor_hakama, grad=0.4, topo=.15, baixo=-.4)
    corpo += g.arredondado("hakama_cint", [-3.8, 12.4, -4.3], [3.8, 14.8, 3.9], mh, r=0.5, faixa=(6, 14))
    mf = mat_luz(cor_fixa(BRANCO_F), grad=0.0, borda=.1)
    corpo += g.arredondado("faixa", [-3.95, 13.9, -4.55], [3.95, 15.5, 4.1], mf, r=0.35)
    nx = -1.0
    corpo.append(peca("no_faixa", [nx - 0.75, 13.5, -5.25], [nx + 0.75, 15.7, -4.4], mf))
    corpo.append(peca("no_ponta1", [nx - 0.85, 8.8, -5.1], [nx - 0.1, 13.6, -4.7], mf, rot=(0, 0, -5), pivo=(nx - 0.5, 13.6, -4.9)))
    corpo.append(peca("no_ponta2", [nx + 0.1, 9.6, -5.1], [nx + 0.85, 13.6, -4.7], mf, rot=(0, 0, 5), pivo=(nx + 0.5, 13.6, -4.9)))
    KAT = (3.9 * LADO_KATANA, 14.6, -4.8)
    corpo.append(osso("katana", list(KAT), [32, 24 * (-LADO_KATANA), 0], montar_katana(KAT)))
    mp = mat_luz(cor_tronco)
    pescoco = osso("pescoco", [0, 23.0, -1.0], [0, 0, 0], [
        *g.arredondado2("pescoco", [-2.5, 21.6, -4.8], [2.5, 27.0, 1.6], mp, r=1.0, faixa=FAIXA_BRANCA),
        montar_cabeca()])
    corpo.append(pescoco)
    for lado in (-1, 1):
        corpo.append(montar_asa(lado))
    corpo.append(montar_cauda())
    tronco = osso("corpo", [0, 13.0, 0], [0, 0, 0], corpo)
    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

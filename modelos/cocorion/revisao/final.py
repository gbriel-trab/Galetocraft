"""Cocórion (#005, Ar): o Galo dos Ventos, galo guerreiro branco de crista espetada, cicatrizes de batalha, asas em
capa com o glifo verde do vento, calça hakama preta com faixa branca e katana na cintura."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
import previa                                  # só a matriz de rotação (mesma ordem do Blockbench)
from galo_base import peca, osso, mix, tom, clamp, na_borda, contexto_luz

ID = "cocorion"; NOME = "Cocórion"; NUMERO = 5
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 30.0, -2.5), 12.0)
# penas da cauda (cadeias de 5 ossos) ondulam de leve
ONDAS = [(f"cauda{k}", 5, (2.0, 1.5, 0.0)) for k in range(6)]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (da ficha) ----------------
CREME = (241, 230, 219); CREME_CL = (252, 246, 236); CREME_ESC = (227, 209, 199)
CINZA_LASCA = (184, 174, 178); CINZA_CL = (196, 186, 186)
CARVAO = (52, 52, 58); PRETO_H = (30, 30, 36)
VERDE_ESC = (30, 78, 44); VERDE = (52, 112, 60)
AMAR = (250, 196, 30); AMAR_CL = (255, 224, 96); AMAR_ESC = (226, 140, 24)
VERM_C = (214, 44, 36); VERM_C_ESC = (150, 22, 26); VERM_C_CL = (240, 80, 60)
OURO_C = (246, 190, 40); OURO_C_ESC = (176, 116, 20); OURO_C_CL = (255, 230, 120)
GARRA = (46, 44, 52)

def sombra_creme(c): return (int(c[0] * .74), int(c[1] * .60), int(c[2] * .60))
def tomb(c, f):
    """Como g.tom, mas a sombra do branco puxa para um bege rosado (como na ficha), não para cinza nem roxo."""
    f = clamp(f, -1, 1)
    return mix(c, g.LUZ, f * .35) if f >= 0 else mix(c, sombra_creme(c), -f * .9)

def mat_branco(cor_fn, **kw):
    def f(c):
        base = cor_fn(c["p"], c["face"])
        return None if base is None else tomb(base, contexto_luz(c, **kw))
    return f

def escama(a, y, passo=1.7, fase=0.0):
    """Fileiras de pontas de pena (fator de sombra): 'a' é a coordenada horizontal na face."""
    t = (y + 0.45 * abs(math.sin(a * 1.6 + fase))) % passo
    return -0.16 if t < 0.24 else (0.05 if t > passo - 0.3 else 0.0)

def risco_x(a, y, ca, cy, r, w=0.32):
    """Cicatriz em X centrada em (ca, cy), braços de meia-diagonal r e espessura w."""
    da, dy = a - ca, y - cy
    if max(abs(da), abs(dy)) > r: return False
    return abs(da - dy) < w or abs(da + dy) < w

def asterisco(a, y, ca, cy, r, w=0.17):
    """Cicatriz de 3 riscos cruzados (asterisco), levemente torta."""
    da, dy = a - ca, y - cy
    if da * da + dy * dy > r * r: return False
    for ang in (82, 22, 142):
        t = math.radians(ang)
        if abs(-math.sin(t) * da + math.cos(t) * dy) < w: return True
    return False

# orientação no mundo: a pintura usa coordenadas sem rotação; para saber qual face fica para cima depois que
# o osso gira, calculamos a normal girada (luz de cima, sombra embaixo, em qualquer ângulo)
def matriz(*rots):
    M = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    for r in rots: M = previa.mm(M, previa.rot(*r))
    return M

def normal_mundo(M, face): return previa.mv(M, g.NORMAL[face])

# ---------------- cabeça ----------------
EY = 27.3                                   # altura do olho
FX, ZF, QX = 2.1, -6.6, 4.9                 # meia largura da frente, z da frente, meia largura do crânio (cabeça larga)
ZQ = ZF + (QX - FX)                         # z da quina de trás da face diagonal
FAC_T = 2.0
FAC_L = (QX - FX) * 1.4142
FAC_O = ((FX + QX) / 2, (ZF + ZQ) / 2)      # centro da face de fora (lado +x)
FAC_C = (FAC_O[0] - 0.7071 * FAC_T / 2, FAC_O[1] + 0.7071 * FAC_T / 2)
OLHO_RU, OLHO_RV = 1.75, 0.95               # olho em amêndoa (comprido, baixo)
SOB_Y, SOB_K = 0.36 * OLHO_RV, 0.5          # linha de baixo da sobrancelha: v = SOB_Y + SOB_K * u (~27° para o bico)
SOB_H = 1.0                                 # altura da barra preta da sobrancelha
Y_SOB_FRENTE = EY + SOB_Y - SOB_K * FAC_L / 2   # altura da sobrancelha na quina da frente

IRIS = ((18, 92, 38), (98, 210, 74))
# Nas vistas de revisão o lado -x aparece à DIREITA de quem olha de frente e o lado +x é o que a vista
# "Lateral Direita" mostra. Para bater com a ficha: katana à direita na vista de frente (-x) e as cicatrizes do
# rosto no lado que a arte e as expressões mostram (+x).
LADO_KATANA = -1
LADO_CICATRIZ = 1

PRETO_SOB = (26, 26, 32)

def sob_frente(x, y):
    """Sobrancelha pintada na frente da testa: continua a barra da face diagonal e desce até o bico (V bravo)."""
    ax = abs(x)
    if ax < 0.55: return False
    yl = Y_SOB_FRENTE - 0.32 * (FX - ax)
    return yl <= y <= yl + SOB_H

def cor_cranio(p, face):
    x, y, z = p
    if face == "up": return CREME_CL
    a = z if face in ("east", "west") else x
    if face == "north" and z < ZQ - 0.2:
        if sob_frente(x, y): return mix(PRETO_SOB, (70, 70, 80), clamp((y - Y_SOB_FRENTE) / SOB_H - 0.6))
        if asterisco(x, y, 1.0 * LADO_CICATRIZ, 29.0, 0.68, 0.13): return VERM_C
    return tomb(CREME, escama(a, y, 1.5, 0.7) * 0.6)

def olho_verde(u, v):
    """Olho em amêndoa: íris verde grande encostando na sobrancelha, pupila preta, brilho, pouca esclera (embaixo
    e no canto de trás), fio escuro só na pálpebra de baixo. A barra preta (pintada e rente) cobre o terço de cima.
    (u ao longo da face, negativo = para o bico; v para cima.)"""
    ru, rv = OLHO_RU, OLHO_RV
    if abs(u) > ru: return None
    meia = rv * (1 - (u / ru) ** 2) ** 0.6
    if abs(v) > meia: return None
    corte = SOB_Y + SOB_K * u
    if v > corte: return None                                    # a sobrancelha pinta por cima
    if v < -meia + 0.12: return (70, 62, 66)                     # pálpebra de baixo
    iu, iv = u + 0.18, v - 0.12
    if ((iu - 0.12) / 0.2) ** 2 + ((iv - 0.0) / 0.2) ** 2 <= 1 and v < corte - 0.12: return (255, 255, 255)
    if ((iu + 0.12) / 0.3) ** 2 + ((iv + 0.05) / 0.48) ** 2 <= 1: return (14, 14, 18)
    if (iu / 1.05) ** 2 + (iv / 0.86) ** 2 <= 1: return mix(IRIS[1], IRIS[0], clamp((0.4 - iv) / 1.2 + 0.1))
    return mix((252, 250, 248), (214, 206, 210), clamp(-v / rv + 0.3))

def mat_faceta(lado):
    """Face diagonal do rosto: olho inteiro numa face plana, a barra preta da sobrancelha pintada rente por cima,
    cicatriz em X na bochecha (um lado só)."""
    base = mat_branco(cor_cranio, borda=.03, curva=.3)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u, v = z - FAC_C[1], y - EY
            corte = SOB_Y + SOB_K * u
            if corte <= v <= corte + SOB_H: return mix(PRETO_SOB, (70, 70, 80), clamp((v - corte) / SOB_H - 0.6))
            olho = olho_verde(u, v)
            if olho is not None: return olho
            if lado == LADO_CICATRIZ and risco_x(u, v, 0.45, -1.95, 0.62, 0.19): return VERM_C
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return AMAR_ESC
    if face in ("east", "west") and abs(z - (ZF - 1.0)) < 0.25 and abs(y - 25.9) < 0.2: return (140, 70, 16)   # narina
    if face in ("east", "west", "north") and 24.45 < y < 24.68: return (150, 70, 16)                         # boca
    if face == "up": return AMAR_CL
    base = mix(AMAR_CL, AMAR, clamp((26.4 - y) / 2.0))
    return mix(base, AMAR_ESC, clamp((25.1 - y) / 1.0) * 0.8)       # embaixo puxa para o laranja

def mat_bico(c):
    """Bico: amarelo vivo; a luz quase não escurece os lados (senão vira mostarda)."""
    luz = contexto_luz(c, borda=.1, curva=.2) * 0.6 + 0.06
    return tom(cor_bico(c["p"], c["face"]), luz)

def mat_preto_facetado(c):
    face = c["face"]
    base = (84, 84, 94) if face == "up" else (40, 40, 48) if face in ("north", "south") else (30, 30, 38) if face != "down" else (18, 18, 24)
    return tomb(base, -0.4) if na_borda(c) else base

def mat_lasca(M, t0, t1):
    """Lasca da crista: branca onde a face olha para cima, creme nos lados, cinza por baixo (pela normal no mundo);
    clareia para a ponta."""
    def f(c):
        lo, hi = c["b"][0][1], c["b"][1][1]
        t = t0 + (t1 - t0) * clamp((c["p"][1] - lo) / max(hi - lo, 1e-6))
        nx, ny, nz = normal_mundo(M, c["face"])
        if ny > 0.35: cor = mix(CREME, CREME_CL, 0.15 + 0.35 * t)      # sem branco estourado (nada de fio claro de perfil)
        elif ny < -0.3: cor = mix(CINZA_LASCA, CREME_ESC, 0.35 * t)
        else: cor = tomb(mix(CREME_ESC, CREME, t), 0.06 - 0.12 * nx - 0.08 * nz)
        if na_borda(c): cor = tomb(cor, -0.18)
        return cor
    return f

def mat_ponta_lasca(M, y0, H, d, eixo):
    """Ponta da lasca (placa recortada em triângulo): a largura cai de 'd' a zero até a ponta. As faces estreitas
    (a espessura) levam um tom médio fixo: nada de fio claro solto quando a placa fica de perfil."""
    base = mat_lasca(M, 0.0, 1.0)
    largas = ("north", "south") if eixo == "x" else ("east", "west")
    def f(c):
        x, y, z = c["p"]
        v = (y - y0) / H
        if v < 0 or v > 1: return None
        a = (x if eixo == "x" else z) - c["b"][0][0 if eixo == "x" else 2] - d
        if v > 0.9 or abs(a) > d * (1 - v ** 1.2) + 1e-6: return None
        if c["face"] not in largas: return tomb(CREME_ESC, -0.12)
        return base(c)
    return f

def lasca(nome, raiz, rot, L, b):
    """Lasca pontuda da crista: duas placas grossas recortadas em triângulo, cruzadas (largas na raiz, ponta fina),
    em volta de um miolo girado 45°: de qualquer lado lê como ponta, sem degraus nem tampas quadradas."""
    x, y, z = raiz
    d = b * 0.8                       # meia largura da placa na raiz
    e = 0.55                          # meia espessura da placa (volume de voxel)
    nb = b * 0.45; hb = 0.22 * L      # miolo (fica dentro das placas)
    M = matriz(rot)
    miolo = peca(nome + "_miolo", [x - nb / 2, y - 0.3, z - nb / 2], [x + nb / 2, y + hb, z + nb / 2],
                 mat_lasca(matriz(rot, (0, 45, 0)), 0.0, 0.4))
    pa = peca(nome + "_pa", [x - d, y - 0.3, z - e], [x + d, y + L, z + e], mat_ponta_lasca(M, y - 0.3, L + 0.3, d, "x"), res=4)
    pb = peca(nome + "_pb", [x - e + 0.02, y - 0.3, z - d], [x + e - 0.02, y + L, z + d], mat_ponta_lasca(M, y - 0.3, L + 0.3, d, "z"), res=4)
    return osso(nome, list(raiz), list(rot), [osso(nome + "_g", list(raiz), [0, 45, 0], [miolo]), pa, pb])

K_CAB = 1.08                                 # escala da cabeça inteira (a ficha tem cabeça grande)

def montar_cabeca():
    i_cab = len(g.PECAS)
    cab = []
    mc = mat_branco(cor_cranio, borda=.03, curva=.3)
    fx = (23.2, 31.0)
    # crânio largo e arredondado (quinas chanfradas em 2 degraus); a frente fica no mesmo volume (sem bloco de testa)
    cab += g.arredondado2("cranio", [-QX, 23.9, ZQ - 0.4], [QX, 30.0, 2.0], mc, r=1.4, faixa=fx, res=4)
    cab.append(peca("cranio_frente", [-FX, 24.3, ZF], [FX, 29.7, ZQ + 0.2], mc, faixa=fx, res=8))
    cab.append(peca("cranio_topo", [-FX - 0.6, 29.4, ZF + 0.5], [FX + 0.6, 30.0, ZQ + 0.6], mc, faixa=fx, res=4))
    # queixo em degrau (arredonda embaixo da cara)
    cab.append(peca("queixo", [-FX - 0.4, 23.5, ZF + 0.6], [FX + 0.4, 24.5, ZQ + 0.6], mc, faixa=fx, res=4))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 24.3, cz - FAC_L / 2], [cx + FAC_T / 2, 29.7, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, EY, cz), faixa=fx, res=8))
        # barra preta rente (só 0,15 para fora): dá a quina da sobrancelha no perfil sem virar bloco solto
        xo = cx + FAC_T / 2 * lado
        x0, x1 = sorted((xo - 0.3 * lado, xo + 0.15 * lado))
        yb = EY + SOB_Y
        cab.append(osso("sobrancelha_q_" + s, [cx, EY, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_q_" + s, [x0, yb, cz - FAC_L / 2 - 0.05], [x1, yb + SOB_H, cz + FAC_L / 2], mat_preto_facetado,
                 rot=(-26.6, 0, 0), pivo=(cx, yb, cz))]))
    # bico: cunha larga (~1/3 da cara) com o topo reto seguindo a sobrancelha, gancho leve na ponta,
    # mandíbula de baixo alaranjada; a barbela pende logo abaixo da base do bico
    cab.append(peca("bico_base", [-1.75, 24.6, ZF - 1.8], [1.75, 26.7, ZF + 0.1], mat_bico, faixa=(23.5, 26.8), res=4))
    cab.append(peca("bico_ponta", [-1.3, 24.85, ZF - 3.0], [1.3, 26.62, ZF - 1.7], mat_bico, faixa=(23.5, 26.8), res=4))
    cab.append(peca("bico_gancho", [-0.85, 24.25, ZF - 3.55], [0.85, 26.5, ZF - 2.9], mat_bico, faixa=(23.5, 26.8), res=4))
    cab.append(peca("bico_baixo", [-1.45, 23.8, ZF - 2.5], [1.45, 24.7, ZF + 0.1],
                    g.mat_cor(lambda p, f: (236, 128, 28) if f != "up" else AMAR_ESC, borda=.12, curva=.3), res=4))
    mbar = g.mat_cor(lambda p, f: mix(VERM_C_CL, VERM_C, clamp((23.8 - p[1]) / 2.8)), borda=.1, curva=.5)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.08 * lado, 1.3 * lado))
        cab += g.arredondado("barbela_" + s, [x0, 20.8, ZF - 1.7], [x1, 23.9, ZF - 0.3], mbar, r=0.32, faixa=(20.6, 23.9), res=4)
    # crista: lascas pontudas da testa e do alto, para CIMA e para TRÁS, a do meio mais alta; pouco aberta para os lados
    crista = []
    LASCAS = [((0.0, 29.6, -4.2), (10, 0, 0), 7.6, 3.6), ((0.0, 30.0, -1.8), (30, 0, 0), 9.4, 3.9),
              ((0.0, 29.8, 0.6), (56, 0, 0), 9.2, 3.8), ((0.0, 28.6, 1.8), (84, 0, 0), 8.2, 3.6),
              ((0.0, 26.8, 2.0), (110, 0, 0), 6.6, 3.2)]
    for l in (-1, 1):
        LASCAS += [((2.5 * l, 29.6, -3.6), (14, 0, -14 * l), 6.6, 3.3), ((2.9 * l, 29.8, -1.2), (36, 0, -16 * l), 7.8, 3.5),
                   ((2.7 * l, 29.4, 1.2), (64, 0, -15 * l), 7.8, 3.4), ((2.5 * l, 27.8, 1.9), (94, 0, -13 * l), 6.8, 3.1),
                   ((4.1 * l, 29.0, -2.2), (28, 0, -26 * l), 5.2, 2.9)]
    for k, (r, rt, L, b) in enumerate(LASCAS):
        crista.append(lasca(f"crista{k}", r, rt, L, b))
    cab.append(osso("crista", [0, 30.0, 0], [0, 0, 0], crista))
    # tufos da bochecha: lascas curtas nos lados (ligam o rosto à crista) e na nuca
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cab.append(lasca("bochecha_" + s, (4.5 * lado, 26.0, -1.6), (98, 0, -26 * lado), 4.2, 2.6))
        cab.append(lasca("bochecha2_" + s, (4.4 * lado, 28.4, -1.2), (66, 0, -30 * lado), 4.6, 2.6))
    cab.append(lasca("nuca", (0, 25.4, 1.8), (120, 0, 0), 4.8, 2.8))
    cabeca = osso("cabeca", [0, 24.6, -0.6], [0, 0, 0], cab)
    g.transformar(i_cab, [cabeca], (0.0, 24.0, -1.0), k=K_CAB)
    return cabeca

# ---------------- corpo ----------------
def cor_tronco(p, face):
    x, y, z = p
    if face == "north" and z < -3.0:
        if risco_x(x, y, 0.0, 18.2, 2.15, 0.36): return VERM_C
    a = z if face in ("east", "west") else x
    return tomb(mix(CREME, CREME_CL, clamp((y - 16) / 7)), escama(a, y, 1.6) * 0.9)

def cor_lapela(p, face):
    """Lapela: penas em fileiras, fio de sombra na borda de dentro (dobra da capa)."""
    x, y, z = p
    if face == "north" and abs(x) < 2.7: return tomb(CREME, -0.28)
    return tomb(CREME, fileiras_asa(y, x * 1.3 + 7))

def cor_hakama(p, face):
    x, y, z = p
    a = z if face in ("east", "west") else x
    base = mix(CARVAO, PRETO_H, clamp((13 - y) / 6))
    if y < 7.55 and face != "down": return (20, 20, 26)        # barra
    pre = (a * 1.0) % 1.6                                     # pregas verticais
    if pre < 0.22: return tomb(base, -0.5)
    if pre < 0.6: return tomb(base, 0.25)
    return base

def cor_faixa(p, face):
    x, y, z = p
    if abs(y - 16.1) < 0.1: return CREME_ESC
    return mix(CREME, CREME_CL, clamp((y - 15.2) / 1.8))

# glifo do vento: espiral de 1,5 volta com a cauda descendo para trás (desenhado no plano y-z da asa)
GLIFO_C = (16.6, 1.1)                    # (y, z) do centro da espiral
GLIFO_K = 0.85                           # escala do desenho (~40% da largura da asa)
GLIFO_W = 0.5                            # meia espessura do traço (unidades do desenho)

def _curva_glifo():
    pts = []
    for k in range(61):
        th = 3 * math.pi * k / 60
        r = 0.25 + 0.31 * th
        pts.append((r * math.cos(th), r * math.sin(th)))
    ue, ve = pts[-1]
    return pts + [(ue + 0.1, ve - 1.2), (ue - 0.3, ve - 2.4), (ue - 1.3, ve - 3.2), (ue - 2.4, ve - 3.3)]
GLIFO_P = _curva_glifo()

def _dist_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = clamp(((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy + 1e-9))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

def glifo(y, z):
    """u = para a frente (-z), v = para cima: a cauda da espiral desce para trás nas duas asas (como na ficha)."""
    u, v = -(z - GLIFO_C[1]) / GLIFO_K, (y - GLIFO_C[0]) / GLIFO_K
    if not (-4.5 < u < 4.2 and -7.2 < v < 4.2): return False
    return any(_dist_seg(u, v, *GLIFO_P[i], *GLIFO_P[i + 1]) < GLIFO_W for i in range(len(GLIFO_P) - 1))

def fileiras_asa(y, z, passo=2.6, larg=2.2):
    """Fileiras de penas desenhadas na asa: cada pena termina numa ponta em V (fio de sombra embaixo da ponta),
    as fileiras desencontradas."""
    fila = math.floor((y - 12.4) / passo)
    fy = (y - 12.4) % passo
    fz = ((z + 4.4 + (fila % 2) * larg / 2) % larg) / larg
    b = 0.7 * abs(2 * fz - 1)
    if 0 <= fy - b < 0.3: return -0.3
    if fy - b < 0: return -0.1
    if fz < 0.05 or fz > 0.95: return -0.07
    return 0.05 * (fy - b) / passo

def mat_asa(lado, glifo_ok=True):
    fora = "east" if lado > 0 else "west"
    def cor(p, face):
        x, y, z = p
        if glifo_ok and face == fora and glifo(y, z): return VERDE_ESC
        return tomb(CREME, fileiras_asa(y, z))
    return mat_branco(cor, borda=.06, curva=.45)

def dente(nome, centro, s, esp, eixo_x, mat, giro=45):
    """Ponta triangular da borda da capa: quadrado girado (losango) meio enterrado na borda de baixo."""
    x, y, z = centro
    if eixo_x:      # placa de lado (asa): losango no plano y-z
        return peca(nome, [x - esp / 2, y - s / 2, z - s / 2], [x + esp / 2, y + s / 2, z + s / 2], mat,
                    rot=(giro, 0, 0), pivo=centro, res=4)
    return peca(nome, [x - s / 2, y - s / 2, z - esp / 2], [x + s / 2, y + s / 2, z + esp / 2], mat,
                rot=(0, 0, giro), pivo=centro, res=4)

def montar_asa(lado):
    """Asa como capa: estreita no ombro e abrindo para baixo e para fora (osso da 'saia' gira mais para fora, em
    sino), glifo do vento no meio da face de fora, borda de baixo serrilhada em 5 pontas triangulares para baixo e
    para fora, até o meio da hakama. Girada para a frente (o glifo aparece de frente)."""
    s = "d" if lado < 0 else "e"
    xi = 4.4 * lado
    T = 1.6
    x0, x1 = sorted((xi, xi + T * lado))
    ma = mat_asa(lado)
    md = mat_asa(lado, glifo_ok=False)
    filhos = []
    # ombro estreito e arredondado
    x0o, x1o = sorted((xi - 0.3 * lado, xi + (T + 0.3) * lado))
    filhos += g.arredondado("asa_ombro_" + s, [x0o, 19.4, -3.0], [x1o, 25.3, 3.2],
                            mat_branco(lambda p, f: tomb(CREME, escama(p[2], p[1], 1.6, 1.0)), borda=.06), r=0.8)
    # saia da capa: mais larga embaixo (degrau), aberta para fora
    xm = xi + (T / 2) * lado
    saia = []
    saia += g.arredondado("asa_capa_" + s, [x0, 11.2, -3.8], [x1, 20.4, 4.6], ma, r=0.6, res=4)
    xb0, xb1 = sorted((xi + 0.08 * lado, xi + (T - 0.08) * lado))
    saia += g.arredondado("asa_capa2_" + s, [xb0, 10.8, -4.9], [xb1, 16.6, 6.7], ma, r=0.5, res=4)
    for k, z in enumerate((-3.7, -1.4, 0.9, 3.2, 5.6)):
        saia.append(dente(f"asa_dente{k}_{s}", (xm, 10.9, z), 2.7, T - 0.2, True, md, giro=45))
    filhos.append(osso("asa_saia_" + s, [xm, 20.2, 0.4], [0, 0, 14 * lado], saia))
    return osso("asa_" + s, [4.6 * lado, 23.6, 0.3], [0, 22 * lado, 12 * lado], filhos)

def montar_lapela(lado):
    """Lapela da capa na frente: faixa branca do ombro à faixa, abrindo em V no peito (mostra o X)."""
    s = "d" if lado < 0 else "e"
    x0, x1 = sorted((2.5 * lado, 4.4 * lado))
    return peca("lapela_" + s, [x0, 15.6, -4.9], [x1, 23.2, -3.9], mat_branco(cor_lapela, borda=.1, curva=.4),
                rot=(0, 0, -9 * lado), pivo=(2.5 * lado, 15.6, -4.4), res=4)

# ---------------- cauda ----------------
def mat_foice(k, n, M):
    """Pena da cauda em foice (bloco de voxel): por cima creme, por baixo verde-escuro (a divisa ondula), a ponta
    afina num bico um pouco abaixo do meio (a ponta cai)."""
    def f(c):
        (_, y0, z0), (_, y1, z1) = c["b"]
        x, y, z = c["p"]
        fz = clamp((z - z0) / max(z1 - z0, 1e-6))
        fy = (y - y0) / max(y1 - y0, 1e-6)
        if k == n - 1 and abs(fy - 0.4) > 0.6 * (1 - fz ** 1.3) + 1e-6: return None
        face = c["face"]
        limite = 0.44 + 0.08 * math.sin((z - z0) * 2.6 + k)
        verde = face == "down" or (face != "up" and fy < limite)
        if verde: cor = mix(VERDE, VERDE_ESC, 0.35 + 0.5 * clamp(1 - fy / max(limite, 1e-6)))
        else: cor = mix(CREME_CL, CREME, 0.3 + 0.5 * fz * (k + 1) / n)
        nx, ny, nz = normal_mundo(M, face)
        luz = 0.22 * ny - 0.04
        if face in ("east", "west") and c["j"] in (0, c["th"] - 1): luz -= 0.22
        if verde and face in ("east", "west") and abs(fy - limite) < 0.06: luz -= 0.2
        return tom(cor, luz) if verde else tomb(cor, luz)
    return f

def pena_foice(nome, raiz, rot0, curva, L, H, esp):
    """Pena larga em foice: cadeia de 5 segmentos para trás (+z) cuja ponta vai caindo (curva rx > 0)."""
    alturas = [1.0, 1.0, 0.95, 0.82, 0.68]
    n = len(alturas); Ls = L / n
    def seg(k, pos, M):
        px, py, pz = pos
        h = H * alturas[k]
        r = list(rot0) if k == 0 else list(curva)
        Mk = previa.mm(M, previa.rot(*r))
        filhos = [peca(f"{nome}_{k}", [px - esp / 2, py - h / 2, pz - 0.1], [px + esp / 2, py + h / 2, pz + Ls + 0.1],
                       mat_foice(k, n, Mk), res=4)]
        if k + 1 < n: filhos.append(seg(k + 1, (px, py, pz + Ls), Mk))
        return osso(f"{nome}_{k}", list(pos), r, filhos)
    return seg(0, raiz, matriz())

def montar_cauda():
    """Leque grande de 6 penas em foice saindo do quadril para trás e para CIMA, em camadas (cada uma creme por
    cima e verde-escura por baixo), pontas caindo; a de cima chega à altura dos olhos e o leque passa ~1 corpo
    das costas. Espessuras alternadas (sem faces no mesmo plano) e um leve leque para os lados."""
    penas = []
    # (raiz y, z, rx, ry, curva, comprimento, altura, espessura)
    P = [(20.4, 4.4, -56, 0, 8, 15.5, 4.6, 1.15), (19.0, 4.6, -38, 6, 8, 15.5, 4.6, 0.95),
         (17.6, 4.6, -20, -6, 8, 15.0, 4.4, 1.1), (16.2, 4.6, -3, 7, 8, 14.0, 4.2, 0.95),
         (14.9, 4.6, 14, -7, 7, 12.5, 4.0, 1.1), (13.8, 4.4, 30, 5, 6, 10.5, 3.6, 0.95)]
    for k, (y, z, rx, ry, cv, L, H, esp) in enumerate(P):
        penas.append(pena_foice(f"cauda{k}", (0, y, z), (rx, ry, 0), (cv, 0, 0), L, H, esp))
    return osso("cauda", [0, 17.0, 4.4], [0, 0, 0], penas)

# ---------------- katana ----------------
def mat_metal(cima, frente, lado, baixo):
    return g.mat_facetado(cima, frente, lado, baixo, quina=-0.3)

def mat_cabo(c):
    """Cabo da katana: verde com a amarração em losangos brancos."""
    x, y, z = c["p"]
    base = VERDE if c["face"] not in ("down",) else VERDE_ESC
    t = (c["b"][1][2] - z) % 1.0
    jj = abs((c["j"] + 0.5) / c["th"] - 0.5) * 2 if c["face"] in ("east", "west", "up", "down") else abs((c["i"] + 0.5) / c["tw"] - 0.5) * 2
    if abs(t - 0.5) < 0.32 * (1 - jj) + 0.04: return (238, 236, 228)
    return tom(base, -0.25) if na_borda(c) else base

def montar_katana(base):
    """Katana ao longo de z (frente = -z) a partir da guarda (tsuba), em 'base': cabo para a frente, bainha atrás."""
    bx, by, bz = base
    def pc_(nome, de, ate, mat, **kw):
        return g.peca(nome, [de[0] + bx, de[1] + by, de[2] + bz], [ate[0] + bx, ate[1] + by, ate[2] + bz], mat, **kw)
    ouro = mat_metal(OURO_C_CL, OURO_C, mix(OURO_C, OURO_C_ESC, .4), OURO_C_ESC)
    bainha = mat_metal((70, 70, 80), (34, 34, 42), (26, 26, 32), (16, 16, 20))
    pc = [pc_("katana_cabo", [-0.45, -0.48, -5.8], [0.45, 0.48, -0.3], mat_cabo, res=6),
          pc_("katana_pomo", [-0.55, -0.58, -6.4], [0.55, 0.58, -5.75], ouro, res=4)]
    pc += g.octogono("katana_tsuba", [bx - 1.2, by - 1.2, bz - 0.35], [bx + 1.2, by + 1.2, bz + 0.15], ouro, r=0.45)
    pc += [pc_("katana_habaki", [-0.5, -0.55, 0.1], [0.5, 0.55, 0.7], ouro, res=4),
           pc_("katana_bainha", [-0.4, -0.55, 0.6], [0.4, 0.55, 14.2], bainha),
           pc_("katana_ponteira", [-0.46, -0.6, 14.1], [0.46, 0.6, 15.0], ouro, res=4)]
    return pc

# ---------------- montagem ----------------
def montar():
    corpo = []
    mt = mat_branco(cor_tronco, borda=.03, curva=.45)
    corpo += g.arredondado2("tronco", [-4.4, 14.6, -4.3], [4.4, 24.2, 4.4], mt, r=1.4, faixa=(14.0, 24.6), res=3)
    for lado in (-1, 1):
        corpo.append(montar_lapela(lado))
    # hakama (cintura) e faixa branca
    mh = mat_branco(cor_hakama, borda=.06, curva=.35)
    corpo += g.arredondado("hakama_cint", [-5.0, 12.0, -4.9], [5.0, 15.8, 4.9], mh, r=0.5, faixa=(6.0, 16.0))
    mf = mat_branco(cor_faixa, borda=.1, curva=.3)
    corpo += g.arredondado("faixa", [-4.85, 15.1, -5.15], [4.85, 17.1, 4.8], mf, r=0.4)
    corpo += g.arredondado("no_faixa", [-0.6, 14.4, -5.9], [1.4, 16.4, -4.9], mf, r=0.35)
    corpo.append(peca("no_ponta1", [-0.4, 11.4, -5.6], [0.35, 14.6, -5.2], mf, rot=(0, 0, -10), pivo=(0, 14.6, -5.4)))
    corpo.append(peca("no_ponta2", [0.55, 11.8, -5.6], [1.25, 14.6, -5.2], mf, rot=(0, 0, 8), pivo=(0.9, 14.6, -5.4)))
    # katana presa na faixa: cabo para a frente, para cima e para fora; bainha para trás e para baixo
    KAT = (5.7 * LADO_KATANA, 15.9, -4.6)
    corpo.append(osso("katana", list(KAT), [38, 9 * (-LADO_KATANA), 0], montar_katana(KAT)))
    pescoco = osso("pescoco", [0, 23.2, -0.6], [0, 0, 0], [
        *g.arredondado("pescoco", [-2.9, 21.6, -3.9], [2.9, 25.4, 2.6], mat_branco(cor_tronco, borda=.04), r=0.8),
        montar_cabeca()])
    corpo.append(pescoco)
    for lado in (-1, 1):
        corpo.append(montar_asa(lado))
    # capa nas costas, entre as asas, com a borda de baixo em pontas (fecha a vista de trás como na ficha)
    mc = mat_asa(1, glifo_ok=False)
    corpo += g.arredondado("capa_costas", [-3.8, 12.4, 4.2], [3.8, 24.4, 5.6], mc, r=0.6, res=3)
    for k, x in enumerate((-2.5, 0.0, 2.5)):
        corpo.append(dente(f"capa_dente{k}", (x, 12.5, 4.9), 2.4, 1.2, False, mc, giro=45))
    corpo.append(montar_cauda())
    tronco = osso("corpo", [0, 13.0, 0], [0, 0, 0], corpo)
    return [tronco, perna(-1), perna(1)]

def perna(lado):
    s = "d" if lado < 0 else "e"; xc = 2.5 * lado; zc = 0.4
    pp = []
    mh = mat_branco(cor_hakama, borda=.06, curva=.35)
    x0, x1 = sorted((0.04 * lado, 5.25 * lado))
    pp += g.arredondado("hakama_" + s, [x0, 7.0, -5.1], [x1, 12.6, 5.1], mh, r=0.5, faixa=(6.0, 16.0))
    ma = g.mat_cor(lambda p, f: AMAR if f != "down" else AMAR_ESC, borda=.1, curva=.25)
    pp += g.arredondado("canela_" + s, [xc - 1.7, 1.8, zc - 1.6], [xc + 1.7, 7.6, zc + 1.6], ma, r=0.5, faixa=(0, 8))
    # pé: 3 dedos retos para a frente, cada um com uma garra escura na ponta, e 1 dedo atrás
    mg = g.mat_cor(lambda p, f: GARRA, borda=.2, curva=.5)
    for nome, dx in (("meio", 0.0), ("fora", 1.55 * lado), ("dentro", -1.55 * lado)):
        x0 = xc + dx; z0 = zc - 0.6
        comp = 3.4 if nome == "meio" else 2.8
        pp.append(peca(f"dedo_{nome}_{s}", [x0 - .65, 0, z0 - comp], [x0 + .65, 1.9, z0 + 0.8], ma, faixa=(0, 2.4)))
        pp.append(peca(f"garra_{nome}_{s}", [x0 - .55, 0.0, z0 - comp - 1.0], [x0 + .55, 1.3, z0 - comp + 0.1], mg, faixa=(0, 2.0)))
    pp.append(peca("dedo_tras_" + s, [xc - .7, 0, zc + 1.0], [xc + .7, 1.4, zc + 3.0], ma, faixa=(0, 2.0)))
    return osso("perna_" + s, [xc, 13.0, zc], [0, 0, 0], pp)

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

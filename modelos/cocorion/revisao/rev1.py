"""Cocórion (#005, Ar): o Galo dos Ventos, galo guerreiro branco de crista espetada, cicatrizes em X, asas com o
glifo verde do vento, calça hakama preta com faixa branca e katana na cintura."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, na_borda, contexto_luz, pintar_olho

ID = "cocorion"; NOME = "Cocórion"; NUMERO = 5
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 27, -4), 7.5)
# penas da cauda (cadeias de 4 ossos) ondulam de leve
ONDAS = [(f"cauda_{t}{k}", 4, (2.0, 1.5, 0.0)) for t in "bv" for k in range(5)]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (da ficha) ----------------
CREME = (242, 236, 228); CREME_ESC = (214, 206, 198); CINZA_CL = (186, 182, 182); CINZA = (138, 136, 140)
CARVAO = (52, 52, 58); PRETO_H = (30, 30, 36)
VERDE_ESC = (30, 78, 44); VERDE = (52, 112, 60); VERDE_CL = (132, 178, 72)
BEGE = (238, 204, 168)
AMAR = (250, 196, 30); AMAR_CL = (255, 224, 96); AMAR_ESC = (222, 150, 18)
VERM_C = (214, 44, 36); VERM_C_ESC = (150, 22, 26); VERM_C_CL = (240, 80, 60)
OURO_C = (246, 190, 40); OURO_C_ESC = (176, 116, 20); OURO_C_CL = (255, 230, 120)
GARRA = (46, 46, 54)

def sombra_neutra(c): return (int(c[0] * .56), int(c[1] * .50), int(c[2] * .58))
def tomb(c, f):
    """Como g.tom, mas a sombra puxa para um cinza azulado (o branco não fica rosado)."""
    f = clamp(f, -1, 1)
    return mix(c, g.LUZ, f * .35) if f >= 0 else mix(c, sombra_neutra(c), -f * .9)

def mat_branco(cor_fn, **kw):
    """mat_cor com a sombra neutra (penas brancas, roupa preta)."""
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

# ---------------- cabeça ----------------
EY = 27.3                                   # altura do olho
FX, ZF, QX = 1.7, -6.6, 3.9                 # meia largura da frente, z da frente, meia largura do crânio
ZQ = ZF + (QX - FX)                         # z da quina de trás da face diagonal
FAC_T = 2.0
FAC_L = (QX - FX) * 1.4142
FAC_O = ((FX + QX) / 2, (ZF + ZQ) / 2)      # centro da face de fora (lado +x)
FAC_C = (FAC_O[0] - 0.7071 * FAC_T / 2, FAC_O[1] + 0.7071 * FAC_T / 2)
CAB_Y0, CAB_Y1 = 23.8, 30.6

IRIS = ((20, 96, 40), (96, 206, 72))
# Nas vistas de revisão (e no jogo) o lado -x aparece à DIREITA de quem olha de frente e o lado +x é o que a
# vista "Lateral Direita" mostra. Para bater com a ficha: katana à direita na vista de frente (-x) e as
# cicatrizes do rosto no lado que a arte e as expressões mostram (+x).
LADO_KATANA = -1
LADO_CICATRIZ = 1

def cor_cranio(p, face):
    x, y, z = p
    base = CREME
    if face == "up": return mix(CREME, (255, 252, 246), .4)
    a = z if face in ("east", "west") else x
    base = tomb(base, escama(a, y, 1.5, 0.7) * 0.7)
    # cicatrizes: X na testa (lado direito) e risquinho na testa esquerda
    if face == "north" and risco_x(x, y, 0.85 * LADO_CICATRIZ, 29.1, 0.62, 0.2): return VERM_C
    return base

def olho_verde(u, v, ru=1.42, rv=1.3):
    """Olho grande: esclera branca curta, íris verde que ocupa quase tudo, pupila preta, brilho, contorno grosso
    escuro; o alto é cortado pela sobrancelha (cara brava, descendo para o bico)."""
    e = (u / ru) ** 2 + (v / rv) ** 2
    if e > 1: return None
    if v / rv > 0.48 + 0.3 * (u / ru): return None
    if e > 0.72: return (44, 44, 52)
    iu, iv = u / ru + 0.16, v / rv + 0.06
    di = (iu / 0.6) ** 2 + (iv / 0.7) ** 2
    if ((iu - 0.16) / 0.15) ** 2 + ((iv - 0.26) / 0.15) ** 2 <= 1: return (255, 255, 255)
    if (iu / 0.26) ** 2 + (iv / 0.36) ** 2 <= 1: return (16, 16, 20)
    if di <= 1: return mix(IRIS[1], IRIS[0], clamp((0.55 - iv) / 1.3 + 0.15))
    return mix((250, 250, 248), (210, 210, 216), clamp(-v / rv + 0.3))

def mat_faceta(lado):
    """Face diagonal do rosto: o olho verde inteiro numa face plana; cicatriz em X na bochecha direita."""
    base = mat_branco(cor_cranio, borda=.03, curva=.3)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u, v = z - FAC_C[1], y - EY
            olho = olho_verde(u, v)
            if olho is not None: return olho
            if lado == LADO_CICATRIZ and risco_x(u, v, 0.45, -2.2, 0.62, 0.2): return VERM_C
            if lado != LADO_CICATRIZ and abs((u - 0.6) - (v + 2.0)) < 0.2 and abs(u - 0.6) < 0.5: return VERM_C_ESC
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return AMAR_ESC
    if face in ("east", "west") and abs(z + 7.6) < 0.3 and abs(y - 26.3) < 0.22: return (150, 84, 20)   # narina
    if face in ("east", "west", "north") and 24.42 < y < 24.68: return (150, 76, 16)                    # boca
    if face == "north": return mix(AMAR_CL, AMAR, clamp((26.6 - y) / 2.6))
    if face == "up": return AMAR_CL
    return mix(AMAR_CL, AMAR, clamp((-z - 6.6) / 3.0))

def mat_preto_facetado(c):
    face = c["face"]
    base = (84, 84, 94) if face == "up" else (40, 40, 48) if face in ("north", "south") else (30, 30, 38) if face != "down" else (18, 18, 24)
    return tomb(base, -0.4) if na_borda(c) else base

def mat_espinho(c0, c1, ei, inv):
    """Espinho da crista: creme com o fio da borda cinza; claro na ponta; um lado na sombra."""
    def f(c):
        lo, hi = c["b"][0][1], c["b"][1][1]
        t = clamp((c["p"][1] - lo) / max(hi - lo, 1e-6))
        cor = mix(c0, c1, t)
        face = c["face"]
        luz = {"up": .25, "north": .12, "east": .02, "west": -.12, "south": -.2, "down": -.4}[face]
        if na_borda(c): luz -= .22
        return tomb(cor, luz)
    return f

def espinho(nome, raiz, rot, L, b, c0=CREME_ESC, c1=(255, 252, 248)):
    """Espinho grosso da crista em 4 degraus que afinam (para +y local, girado por 'rot'), girado 45° no próprio
    eixo: de quase todo ângulo a quina fica para fora e o espinho lê como lasca pontuda, não como torre."""
    x, y, z = raiz
    partes = [(0.36, 1.0), (0.28, 0.74), (0.22, 0.5), (0.14, 0.26)]
    pecas, y0 = [], y
    for k, (fl, fw) in enumerate(partes):
        h, w = L * fl, b * fw
        pecas.append(peca(f"{nome}_{k}", [x - w / 2, y0, z - w / 2], [x + w / 2, y0 + h + 0.05, z + w / 2],
                          mat_espinho(mix(c0, c1, k / 4), mix(c0, c1, (k + 1) / 4), 1, False)))
        y0 += h
    return osso(nome, list(raiz), list(rot), [osso(nome + "_g", list(raiz), [0, 45, 0], pecas)])

K_CAB = 1.08                                 # escala da cabeça inteira (a ficha tem cabeça grande)

def montar_cabeca():
    i_cab = len(g.PECAS)
    cab = []
    mc = mat_branco(cor_cranio, borda=.03, curva=.3)
    fx = (CAB_Y0 - 0.6, CAB_Y1 + 0.4)
    cab.append(peca("cranio_a", [-QX, 24.4, ZQ], [QX, 29.9, 2.2], mc, faixa=fx, res=4))
    cab.append(peca("cranio_b", [-QX + 0.9, CAB_Y0, ZQ - 0.6], [QX - 0.9, CAB_Y1, 1.6], mc, faixa=fx, res=4))
    cab.append(peca("cranio_c", [-QX + 0.45, 24.0, ZQ + 0.2], [QX - 0.45, 30.2, 2.0], mc, faixa=fx, res=4))
    cab.append(peca("cranio_frente", [-FX, 24.0, ZF], [FX, 30.0, ZQ], mc, faixa=fx, res=4))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 24.1, cz - FAC_L / 2], [cx + FAC_T / 2, 29.9, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, EY, cz), faixa=fx, res=8))
        # sobrancelha preta grossa sobre o olho (na face diagonal), descendo para o bico: cara brava
        xo = cx + FAC_T / 2 * lado
        x0, x1 = sorted((xo - 0.15 * lado, xo + 0.75 * lado))
        cab.append(osso("sobrancelha_q_" + s, [cx, EY, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_q_" + s, [x0, 28.15, cz - 1.95], [x1, 29.25, cz + 1.75], mat_preto_facetado,
                 rot=(-16, 0, 0), pivo=(cx, 28.6, cz))]))
        # pedaço da sobrancelha na frente da testa (V bravo de frente)
        x0, x1 = sorted((0.35 * lado, 1.95 * lado))
        cab.append(peca("sobrancelha_f_" + s, [x0, 28.0, ZF - 0.55], [x1, 28.95, ZF + 0.1], mat_preto_facetado,
                        rot=(0, 0, 22 * lado), pivo=(1.95 * lado, 28.5, ZF - 0.2)))
        # sobrancelha do lado, acima da quina de trás do olho
        x0, x1 = sorted((QX * lado - 0.1 * lado, QX * lado + 0.5 * lado))
        cab.append(peca("sobrancelha_l_" + s, [x0, 28.75, ZQ - 0.2], [x1, 29.65, ZQ + 1.6], mat_preto_facetado))
    # bico em cunha: base, meio e gancho; bico de baixo mais escuro
    mb = mat_cor_b(cor_bico)
    cab.append(peca("bico_base", [-1.8, 24.35, ZF - 2.0], [1.8, 27.05, ZF + 0.1], mb, faixa=(23.5, 27.2), res=4))
    cab.append(peca("bico_meio", [-1.45, 24.4, ZF - 3.5], [1.45, 26.75, ZF - 1.9], mb, rot=(-10, 0, 0),
                    pivo=(0, 26.75, ZF - 1.9), faixa=(23.5, 27.2), res=4))
    cab.append(peca("bico_gancho", [-1.0, 23.5, ZF - 4.5], [1.0, 26.0, ZF - 3.3], mb, rot=(-24, 0, 0),
                    pivo=(0, 26.0, ZF - 3.3), faixa=(23.0, 27.2), res=4))
    cab.append(peca("bico_baixo", [-1.35, 23.65, ZF - 3.0], [1.35, 24.45, ZF + 0.1],
                    g.mat_cor(lambda p, f: AMAR_ESC, borda=.12), res=4))
    # barbela vermelha: dois lóbulos compridos pendurados sob o bico
    mbar = g.mat_cor(lambda p, f: mix(VERM_C_CL, VERM_C, clamp((25 - p[1]) / 2.0)), borda=.12, curva=.5)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.06 * lado, 1.4 * lado))
        cab.append(peca("barbela_" + s, [x0, 21.7, ZF - 2.4], [x1, 24.0, ZF - 0.5], mbar, faixa=(20.0, 24.0), res=4))
        x0, x1 = sorted((0.16 * lado, 1.2 * lado))
        cab.append(peca("barbela2_" + s, [x0, 20.9, ZF - 1.95], [x1, 21.8, ZF - 0.7], mbar, faixa=(20.0, 24.0), res=4))
    # crista branca espetada, varrida para trás: (raiz, rot, comprimento, grossura)
    crista = []
    # miolo da crista: um volume arredondado no alto da cabeça de onde saem os espinhos (a crista lê como massa)
    crista += g.arredondado2("crista_miolo", [-3.2, 29.2, -4.2], [3.2, 33.4, 1.8],
                             mat_branco(lambda p, f: tomb(CREME, escama(p[0] + p[2], p[1], 1.4, .4)), borda=.06), r=1.0)
    ESP = [((0, 32.6, -2.8), (12, 0, 0), 6.6, 3.4), ((0, 33.0, -0.6), (40, 0, 0), 8.0, 3.6), ((0, 32.4, 1.4), (70, 0, 0), 7.8, 3.4),
           ((0, 30.4, 2.2), (100, 0, 0), 7.0, 3.2), ((0, 27.8, 1.8), (126, 0, 0), 5.6, 2.8)]
    for l in (-1, 1):
        ESP += [((2.0 * l, 32.0, -2.6), (20, 0, -22 * l), 5.8, 3.0), ((2.4 * l, 32.0, -0.2), (54, 0, -26 * l), 7.0, 3.0),
                ((2.2 * l, 31.0, 1.8), (86, 0, -22 * l), 6.6, 2.8), ((3.0 * l, 29.6, -2.8), (26, 0, -56 * l), 4.6, 2.8),
                ((3.4 * l, 28.4, 0.2), (78, 0, -44 * l), 5.4, 2.6), ((2.8 * l, 26.6, 1.6), (116, 0, -26 * l), 5.0, 2.4)]
    for k, (r, rt, L, b) in enumerate(ESP):
        crista.append(espinho(f"crista{k}", r, rt, L, b))
    cab.append(osso("crista", [0, 30.0, 0], [0, 0, 0], crista))
    cabeca = osso("cabeca", [0, 24.6, -0.6], [0, 0, 0], cab)
    g.transformar(i_cab, [cabeca], (0.0, 24.0, -1.0), k=K_CAB)
    return cabeca

def mat_cor_b(cor_fn):
    """Bico: amarelo vivo, a sombra quase não escurece os lados (senão vira mostarda)."""
    def f(c):
        luz = contexto_luz(c, borda=.1, curva=.2) * 0.6 + 0.06
        return tom(cor_fn(c["p"], c["face"]), luz)
    return f

# ---------------- corpo ----------------
def cor_tronco(p, face):
    x, y, z = p
    if face == "north" and z < -4.0:
        if risco_x(x, y, 0.0, 18.7, 2.15, 0.36): return VERM_C
        return tomb(mix(CREME, BEGE, 0.18), escama(x, y, 1.7) * 0.8)
    a = z if face in ("east", "west") else x
    return tomb(mix(CREME, (250, 246, 240), clamp((y - 16) / 7)), escama(a, y, 1.7) * 0.8)

def cor_hakama(p, face):
    x, y, z = p
    a = z if face in ("east", "west") else x
    base = mix(CARVAO, PRETO_H, clamp((13 - y) / 6))
    if y < 6.55 and face != "down": return (20, 20, 26)        # barra
    pre = (a * 1.0) % 1.6                                     # pregas verticais
    if pre < 0.22: return tomb(base, -0.5)
    if pre < 0.6: return tomb(base, 0.25)
    return base

def cor_faixa(p, face):
    x, y, z = p
    if abs(y - 16.1) < 0.1: return CINZA_CL
    return mix(CREME, (255, 252, 248), clamp((y - 15.2) / 1.8))

# glifo do vento: espiral de 1,5 volta com a cauda descendo para trás (desenhado no plano y-z da asa)
GLIFO_C = (19.2, 0.4)                    # (y, z) do centro da espiral
GLIFO_K = 0.92                           # escala do desenho
GLIFO_W = 0.55                           # meia espessura do traço (unidades do desenho)

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

def mat_asa_painel(lado):
    fora = "east" if lado > 0 else "west"
    def cor(p, face):
        x, y, z = p
        if face == fora and glifo(y, z): return VERDE_ESC
        return tomb(CREME, fileiras_asa(y, z))
    return mat_branco(cor, borda=.08, curva=.45)

def fileiras_asa(y, z, passo=2.6, larg=2.2):
    """Fileiras de penas desenhadas na asa: cada pena termina numa ponta em V (fio de sombra embaixo da ponta),
    com uma separação clara entre as penas; as fileiras são desencontradas."""
    fila = math.floor((y - 12.4) / passo)
    fy = (y - 12.4) % passo
    fz = ((z + 4.4 + (fila % 2) * larg / 2) % larg) / larg
    b = 0.7 * abs(2 * fz - 1)                     # borda de baixo da pena (ponta em V no meio)
    if 0 <= fy - b < 0.3: return -0.34
    if fy - b < 0: return -0.12                    # pedacinho da fileira de baixo que aparece no V
    if fz < 0.05 or fz > 0.95: return -0.08
    return 0.05 * (fy - b) / passo

def mat_pena_asa(L, y0):
    """Pena da asa (bloco que afina): creme, a ponta puxa para o cinza claro, contorno cinza."""
    def f(c):
        x, y, z = c["p"]
        v = clamp((y0 - y) / L)
        cor = mix(CREME, CINZA_CL, clamp((v - 0.5) / 0.5) * 0.7)
        luz = {"up": .2, "down": -.35}.get(c["face"], .04)
        if na_borda(c): luz -= .25
        return tomb(cor, luz)
    return f

def pena_bloco(nome, raiz, rot, L, W, esp, mat):
    """Pena RETA em bloco que afina em 3 degraus, para baixo a partir da raiz (largura em z)."""
    x, y, z = raiz
    partes = [(0.55, 1.0, 1.0), (0.27, 0.64, 0.86), (0.2, 0.3, 0.72)]
    pecas, y0 = [], y
    for k, (fl, fw, fe) in enumerate(partes):
        h, w, e = L * fl, W * fw, esp * fe
        pecas.append(peca(f"{nome}_{k}", [x - e / 2, y0 - h, z - w / 2], [x + e / 2, y0 + 0.05, z + w / 2], mat))
        y0 -= h
    return osso(nome, list(raiz), list(rot), pecas)

def montar_asa(lado):
    """Asa dobrada como uma capa: painel grosso com o glifo do vento por fora, ombro arredondado, fileira de penas
    recortando a borda de baixo e penas varrendo para trás. Girada para fora (o glifo aparece de frente)."""
    s = "d" if lado < 0 else "e"
    xi = 4.4 * lado                           # face de dentro
    T = 1.8
    x0, x1 = sorted((xi, xi + T * lado))
    filhos = []
    # painel em dois degraus: em cima vai mais para a frente, embaixo vai mais para trás (forma de folha)
    filhos += g.arredondado("asa_painel_" + s, [x0, 15.4, -4.2], [x1, 23.4, 5.2], mat_asa_painel(lado), r=0.7, res=4)
    xb0, xb1 = sorted((xi + 0.1 * lado, xi + (T - 0.25) * lado))
    filhos += g.arredondado("asa_painel2_" + s, [xb0, 11.8, -2.6], [xb1, 15.8, 6.2], mat_asa_painel(lado), r=0.5, res=4)
    # ombro arredondado (pouco saliente, para não tapar o glifo)
    x0o, x1o = sorted((xi - 0.4 * lado, xi + (T + 0.3) * lado))
    filhos += g.arredondado("asa_ombro_" + s, [x0o, 22.4, -3.9], [x1o, 25.4, 3.4],
                            mat_branco(lambda p, f: tomb(CREME, escama(p[2], p[1], 1.6, 1.0)), borda=.08), r=0.8)
    # fileira de penas da ponta (borda recortada embaixo); a da frente sai mais alto
    xm = xi + (T / 2) * lado
    for k, (z0, y0, L, var) in enumerate([(-3.5, 16.0, 4.4, 4), (-1.7, 12.6, 5.2, 10), (0.3, 12.4, 6.2, 14), (2.3, 12.2, 6.8, 20),
                                          (4.3, 12.2, 6.6, 26), (5.9, 12.6, 5.6, 34)]):
        xk = xm + (0.15 if k % 2 else -0.15) * lado
        filhos.append(pena_bloco(f"asa_pena{k}_{s}", (xk, y0, z0), (-var, 0, 0), L, 2.4, 1.4, mat_pena_asa(L, y0)))
    # pena da borda de trás, varrendo para trás
    filhos.append(pena_bloco(f"asa_tras_{s}", (xm, 17.4, 4.9), (-40, 0, 0), 5.4, 2.4, 1.2, mat_pena_asa(5.4, 17.4)))
    return osso("asa_" + s, [4.6 * lado, 23.6, 0.3], [0, 20 * lado, 14 * lado], filhos)

def pena_gola(nome, raiz, phi, flare, L, W, lado, varre=0):
    """Pena em bloco da gola (em volta do pescoço): face larga para fora no ângulo phi, abre 'flare' graus."""
    return osso(nome, list(raiz), [0, -phi * lado, 0],
                [pena_bloco(nome + "_p", raiz, (-varre, 0, flare * lado), L, W, 1.2, mat_pena_asa(L, raiz[1]))])

def mat_cauda(c0, c1, ei, inv):
    base = g.mat_pena(c0, c1, ei, inv, borda=.18)
    def f(c):
        cor = base(c)
        if c["face"] == "down": cor = tomb(cor, -0.2)
        return cor
    return f

def mat_cauda_branca(c0, c1, ei, inv):
    """Pena branca da cauda com a camada de baixo verde-escura (nas faces de lado e embaixo) e raque clara."""
    base = mat_cauda(c0, c1, ei, inv)
    def f(c):
        (_, y0, z0), (_, y1, z1) = c["b"]
        t = (c["p"][1] - y0) / max(y1 - y0, 1e-6)
        fz = (c["p"][2] - z0) / max(z1 - z0, 1e-6)
        if c["face"] == "down":
            cor = mix(VERDE, VERDE_ESC, fz)
            return tomb(cor, -0.3) if na_borda(c) else cor
        return base(c)
    return f

def pena_cauda(nome, raiz, rot0, curva, L, W, H, branca=True):
    """Pena larga da cauda (cadeia de 4 segmentos para trás, +z): branca com a ponta cinza, ou verde-escura."""
    if branca:
        cs = [(CREME_ESC, CREME), (CREME, CREME), (CREME, CREME_ESC), (CREME_ESC, CINZA_CL)]
    else:
        cs = [(VERDE_ESC, VERDE), (VERDE, VERDE), (VERDE, VERDE_ESC), (VERDE_ESC, VERDE_ESC)]
    fr = [(0.3, 1.0, 1.0), (0.28, 0.92, 0.95), (0.24, 0.8, 0.8), (0.2, 0.6, 0.5)]
    segs = [(L * a, W * b, H * h, c0, c1) for (a, b, h), (c0, c1) in zip(fr, cs)]
    return g.pena_curva(nome, raiz, segs, rot0, curva, "z", mat_cauda_branca if branca else mat_cauda)

def montar_cauda():
    """Cauda em camadas: penas brancas largas presas ao longo das costas (as de cima sobem para trás, as de baixo
    vão retas), cada uma com uma pena verde-escura logo abaixo."""
    penas = []
    BR = [(-26, 12.6, 23.4), (-10, 14.0, 20.9), (6, 14.0, 18.4), (22, 12.4, 15.9), (40, 10.4, 13.6)]
    ABRE = (-13, 11, -10, 12, -9)                       # leve leque para os lados (a cauda ganha volume por trás)
    for k, (ang, L, y) in enumerate(BR):
        # pena verde: mais curta e mais grossa (fica por fora perto do corpo): miolo verde, pontas brancas
        penas.append(pena_cauda(f"cauda_v{k}", (0, y - 1.7, 5.0), (ang + 4, ABRE[k], 0), (8, 0, 0), L * 0.7, 2.3, 4.4, branca=False))
    for k, (ang, L, y) in enumerate(BR):
        abre = ABRE[k]
        penas.append(pena_cauda(f"cauda_b{k}", (0, y, 5.2), (ang, abre, 0), (7, 0, 0), L, 1.5, 4.4))
    return osso("cauda", [0, 17.0, 4.4], [0, 0, 0], penas)

def mat_metal(cima, frente, lado, baixo):
    return g.mat_facetado(cima, frente, lado, baixo, quina=-0.3)

def mat_cabo(c):
    """Cabo da katana: verde com a amarração em losangos brancos (só nas faces de lado)."""
    x, y, z = c["p"]
    base = VERDE if c["face"] not in ("down",) else VERDE_ESC
    t = (c["b"][1][2] - z) % 1.0
    jj = abs((c["j"] + 0.5) / c["th"] - 0.5) * 2 if c["face"] in ("east", "west", "up", "down") else abs((c["i"] + 0.5) / c["tw"] - 0.5) * 2
    if abs(t - 0.5) < 0.32 * (1 - jj) + 0.04: return (238, 236, 228)
    return tom(base, -0.25) if na_borda(c) else base

def montar_katana(base):
    """Katana na cintura, lado esquerdo: cabo verde para a frente e para cima, bainha preta para trás e para baixo.
    Construída ao longo de z (frente = -z) a partir da guarda (tsuba), em 'base'."""
    bx, by, bz = base
    def peca(nome, de, ate, mat, **kw):
        return g.peca(nome, [de[0] + bx, de[1] + by, de[2] + bz], [ate[0] + bx, ate[1] + by, ate[2] + bz], mat, **kw)
    ouro = mat_metal(OURO_C_CL, OURO_C, mix(OURO_C, OURO_C_ESC, .4), OURO_C_ESC)
    bainha = mat_metal((70, 70, 80), (34, 34, 42), (26, 26, 32), (16, 16, 20))
    pc = []
    pc.append(peca("katana_cabo", [-0.45, -0.48, -5.8], [0.45, 0.48, -0.3], mat_cabo, res=6))
    pc.append(peca("katana_pomo", [-0.55, -0.58, -6.4], [0.55, 0.58, -5.75], ouro, res=4))
    pc += g.octogono("katana_tsuba", [bx - 1.2, by - 1.2, bz - 0.35], [bx + 1.2, by + 1.2, bz + 0.15], ouro, r=0.45)
    pc.append(peca("katana_habaki", [-0.5, -0.55, 0.1], [0.5, 0.55, 0.7], ouro, res=4))
    pc.append(peca("katana_bainha", [-0.4, -0.55, 0.6], [0.4, 0.55, 14.2], bainha))
    pc.append(peca("katana_ponteira", [-0.46, -0.6, 14.1], [0.46, 0.6, 15.0], ouro, res=4))
    return pc

def montar():
    corpo = []
    mt = mat_branco(cor_tronco, borda=.03, curva=.45)
    corpo += g.arredondado2("tronco", [-4.4, 14.6, -4.3], [4.4, 24.2, 4.4], mt, r=1.4, faixa=(14.0, 24.6))
    corpo += g.arredondado("peito", [-3.5, 16.2, -4.9], [3.5, 23.0, -3.4], mt, r=1.0, faixa=(14.0, 24.6), res=4)
    # hakama (cintura) e faixa branca
    mh = mat_branco(cor_hakama, borda=.06, curva=.35)
    corpo += g.arredondado("hakama_cint", [-5.0, 12.0, -4.9], [5.0, 15.8, 4.9], mh, r=0.5, faixa=(6.0, 16.0))
    mf = mat_branco(cor_faixa, borda=.1, curva=.3)
    corpo += g.arredondado("faixa", [-4.85, 15.1, -4.8], [4.85, 17.1, 4.8], mf, r=0.4)
    # nó da faixa na frente com as pontas penduradas
    corpo += g.arredondado("no_faixa", [-0.6, 14.4, -5.7], [1.4, 16.4, -4.6], mf, r=0.35)
    corpo.append(peca("no_ponta1", [-0.4, 11.4, -5.4], [0.35, 14.6, -5.0], mf, rot=(0, 0, -10), pivo=(0, 14.6, -5.2)))
    corpo.append(peca("no_ponta2", [0.55, 11.8, -5.4], [1.25, 14.6, -5.0], mf, rot=(0, 0, 8), pivo=(0.9, 14.6, -5.2)))
    # katana presa na faixa: cabo para a frente, para cima e para fora; bainha para trás e para baixo
    KAT = (4.3 * LADO_KATANA, 15.9, -4.9)
    corpo.append(osso("katana", list(KAT), [40, 35 * (-LADO_KATANA), 0], montar_katana(KAT)))
    # gola de penas em volta do pescoço (une a cabeça aos ombros)
    for l in (-1, 1):
        sl = "d" if l < 0 else "e"
        for k, (phi, y0, L, W, fl) in enumerate([(-34, 24.6, 4.0, 2.8, 30), (8, 25.0, 4.6, 3.0, 34), (50, 25.2, 4.8, 3.0, 30)]):
            x, z = g.anel(3.0, 3.2, -0.4, phi, l)
            corpo.append(pena_gola(f"gola{k}_{sl}", (x, y0, z), phi, fl, L, W, l, varre=6))
    corpo.append(pena_gola("gola_nuca", (0, 25.4, 2.8), 90, 22, 5.0, 3.4, 1))
    # gola de penas no pescoço
    pescoco = osso("pescoco", [0, 23.2, -0.6], [0, 0, 0], [
        *g.arredondado("pescoco", [-2.9, 21.6, -3.9], [2.9, 25.4, 2.6], mat_branco(cor_tronco, borda=.04), r=0.7),
        montar_cabeca()])
    corpo.append(pescoco)
    for lado in (-1, 1):
        corpo.append(montar_asa(lado))
    # capa de penas nas costas (entre as asas): fecha a vista de trás como na ficha
    for k, (x, y0, L) in enumerate([(-2.1, 24.2, 11.0), (2.1, 24.2, 11.0), (0.0, 24.6, 12.0)]):
        corpo.append(pena_bloco(f"costas{k}", (x, y0, 4.5 + 0.3 * (k == 2)), (-8, 0, 0), L, 3.4, 1.2, mat_pena_asa(L, y0)))
    corpo.append(montar_cauda())
    tronco = osso("corpo", [0, 13.0, 0], [0, 0, 0], corpo)
    return [tronco, perna(-1), perna(1)]

def perna(lado):
    s = "d" if lado < 0 else "e"; xc = 2.5 * lado; zc = 0.4
    pp = []
    mh = mat_branco(cor_hakama, borda=.06, curva=.35)
    x0, x1 = sorted((0.04 * lado, 5.25 * lado))
    pp += g.arredondado("hakama_" + s, [x0, 6.0, -5.1], [x1, 12.6, 5.1], mh, r=0.5, faixa=(6.0, 16.0))
    ma = g.mat_cor(lambda p, f: mix(AMAR, AMAR_ESC, clamp((4 - p[1]) / 4)) if f != "down" else AMAR_ESC, borda=.1, curva=.4)
    pp += g.arredondado("canela_" + s, [xc - 1.7, 1.8, zc - 1.6], [xc + 1.7, 6.8, zc + 1.6], ma, r=0.5, faixa=(0, 7))
    mg = g.mat_cor(lambda p, f: GARRA, borda=.25, curva=.5)
    for nome, giro, dx in (("meio", 0, 0), ("fora", -18 * lado, 1.9 * lado), ("dentro", 18 * lado, -1.9 * lado)):
        x0, z0 = xc + dx, zc - 0.8
        pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
            peca(f"dedo_{nome}_{s}", [x0 - .95, 0, z0 - 3.6], [x0 + .95, 2.1, z0 + 0.8], ma, faixa=(0, 2.4)),
            osso(f"garra_{nome}_{s}", [x0, 1.6, z0 - 3.6], [-18, 0, 0], [
                peca(f"garra_{nome}_{s}", [x0 - .75, 0.45, z0 - 5.2], [x0 + .75, 1.85, z0 - 3.5], mg, faixa=(0, 2.0))])]))
    pp.append(peca("dedo_tras_" + s, [xc - .75, 0, zc + 1.0], [xc + .75, 1.5, zc + 3.2], ma, faixa=(0, 2.0)))
    pp.append(peca("garra_tras_" + s, [xc - .6, 0, zc + 3.1], [xc + .6, 1.1, zc + 4.1], mg, faixa=(0, 2.0)))
    return osso("perna_" + s, [xc, 13.0, zc], [0, 0, 0], pp)

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

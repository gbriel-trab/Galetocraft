"""Espinhocó (#011, Planta): galo-porco-espinho da floresta, meia cúpula de espinhos nas costas e plumagem de folhas."""
import math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, mat_cor, arredondado, arredondado2, octogono, pintar_olho

ID = "espinhoco"; NOME = "Espinhocó"; NUMERO = 11
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 27.6, -6.8), 6.3)
ONDAS = []
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (Paleta de Cores da ficha) ----------------
CREME = (246, 224, 178); CREME_ESC = (222, 186, 132)
CARAMELO = (206, 138, 72)
MARROM = (148, 92, 54); MARROM_ESC = (104, 64, 42); CHOCOLATE = (66, 42, 34)
VERDE_ESC = (110, 148, 30); VERDE = (157, 191, 42); VERDE_CLARO = (196, 220, 78); NERVURA = (220, 234, 130)
AMARELO_BICO = (250, 200, 40); AMARELO_ESC = (232, 158, 26); LARANJA_BICO = (214, 124, 22)
VERM = (218, 40, 34); VERM_ESC = (150, 20, 24)
GARRA = (74, 66, 72); GARRA_CLARA = (112, 104, 110)
CANELA = (196, 128, 64); CANELA_CLARA = (222, 160, 92)
ESP_BASE = (116, 68, 36); ESP_MEIO = (196, 130, 66); ESP_CLARO = (232, 184, 116); ESP_PONTA = (248, 226, 184)

# ---------------- utilidades ----------------
def ruido(x, y, z, passo=0.5):
    """Valor fixo em -1..1 por 'voxel' de textura (variação sutil de tom, como os blocos da ficha)."""
    n = (int(math.floor(x / passo)) * 73856093) ^ (int(math.floor(y / passo)) * 19349663) ^ (int(math.floor(z / passo)) * 83492791)
    n = (n ^ (n >> 13)) * 1274126177
    return ((n >> 8) & 0xffff) / 32767.5 - 1.0

def rot_m(rx, ry, rz):
    a, b, c = (math.radians(v) for v in (rx, ry, rz))
    Rx = [[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]]
    Ry = [[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]]
    Rz = [[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]]
    mm = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return mm(Rz, mm(Ry, Rx))

def mv(A, v): return [sum(A[i][k] * v[k] for k in range(3)) for i in range(3)]

def norm(v):
    n = math.sqrt(sum(a * a for a in v)) or 1.0
    return [a / n for a in v]

def apontar(d):
    """Rotação (rx, ry, 0) do osso que leva o eixo local +y para a direção d."""
    dx, dy, dz = norm(d)
    a = math.degrees(math.acos(clamp(dy, -1, 1)))
    b = math.degrees(math.atan2(dx, dz)) if a > 1e-3 else 0.0
    return [a, b, 0.0]

def torcao_para(d, fora):
    """Giro (em torno do próprio eixo) que deixa a normal local +z o mais virada possível para 'fora'."""
    R = rot_m(*apontar(d)); fora = norm(fora)
    melhor, tm = -9, 0
    for t in range(-180, 180, 5):
        n = mv(R, mv(rot_m(0, t, 0), [0, 0, 1]))
        s = sum(n[i] * fora[i] for i in range(3))
        if s > melhor: melhor, tm = s, t
    return tm

def dir_esf(teta, phi):
    """Direção a partir do eixo de trás (+z): teta = abertura (0 = reto para trás), phi = em volta (0 = cima, 90 = esquerda +x)."""
    t, f = math.radians(teta), math.radians(phi)
    return [math.sin(t) * math.sin(f), math.sin(t) * math.cos(f), math.cos(t)]

def escurece(c, f):
    """Escurece sem puxar para o roxo (os espinhos ficam marrom/bege, não cinza)."""
    if f >= 0: return mix(c, (255, 244, 222), f * 0.45)
    return tuple(int(v * (1 + f)) for v in c)

# ---------------- espinhos ----------------
def cor_espinho(v):
    if v < 0.3: return mix(ESP_BASE, ESP_MEIO, v / 0.3)
    if v < 0.6: return mix(ESP_MEIO, ESP_CLARO, (v - 0.3) / 0.3)
    return mix(ESP_CLARO, ESP_PONTA, (v - 0.6) / 0.3)

def mat_espinho(y0, L):
    """Espinho: raiz marrom -> caramelo -> bege -> creme na ponta; uma faceta clara e outra escura (sem cinza),
    degrau de cima de cada bloco mais claro, fio escuro nas bordas."""
    def f(c):
        cor = cor_espinho(clamp((c["p"][1] - y0) / L))
        luz = {"north": .08, "east": .02, "south": -.1, "west": -.05, "up": .05, "down": -.2}[c["face"]]
        if g.na_borda(c): luz -= .08
        return escurece(cor, luz)
    return f

SEG_ESPINHO = ((0.26, 1.0), (0.22, 0.84), (0.2, 0.64), (0.18, 0.43), (0.16, 0.22))   # (fração do comprimento, fração da largura)

def espinho(nome, raiz, d, L, W, torce=45):
    """Espinho grosso em cone de blocos sólidos que afinam em degraus até a ponta (3x3 -> 2x2 -> 1x1), crescendo na
    direção d a partir da raiz. A raiz fica enterrada na massa traseira: o bloco da base quase não aparece."""
    x, y, z = raiz
    m = mat_espinho(y, L)
    pecas, y1 = [], y
    for k, (fl, fw) in enumerate(SEG_ESPINHO):
        h, w = L * fl, W * fw
        pecas.append(peca(f"{nome}_{k}", [x - w / 2, y1, z - w / 2], [x + w / 2, y1 + h, z + w / 2], m, res=3))
        y1 += h - 0.05
    return osso(nome, list(raiz), apontar(d), [osso(nome + "_t", list(raiz), [0, torce, 0], pecas)])

# ---------------- folhas (dobradas na nervura, em V) ----------------
def mat_folha(x0, y0, L, W, s, claro, cores=(VERDE_ESC, VERDE, VERDE_CLARO), nervura=NERVURA):
    c0, c1, c2 = cores
    def f(c):
        x, y, z = c["p"]
        u = (x - x0) * s / (W / 2); v = (y - y0) / L
        if v < 0.04 or v > 1 or u < -0.05: return None
        meia = max(0.2, math.sin(math.pi * clamp(v) ** 0.8)) ** 0.85
        if u > meia: return None
        cor = mix(c0, c1, v / 0.45) if v < 0.45 else mix(c1, c2, (v - 0.45) / 0.55)
        cor = tom(cor, 0.10 if claro else -0.16)
        if u * W / 2 < 0.2 and 0.12 < v < 0.94: return tom(nervura, 0.0 if claro else -0.22)
        if (meia - u) * W / 2 < 0.18: return tom(cor, -0.14)
        return cor
    return f

def folha(nome, raiz, d, L, W, fora=None, torce=None, dobra=20, cores=(VERDE_ESC, VERDE, VERDE_CLARO), esp=0.3, nervura=NERVURA):
    """Folha lanceolada dobrada na nervura (duas meias placas em V): lê de frente, de lado e de 3/4.
    Cresce na direção d; a face convexa (nervura saltada) fica virada para 'fora'."""
    x, y, z = raiz
    if torce is None: torce = torcao_para(d, fora or [0, 0, -1])
    pa = peca(nome + "_a", [x, y, z - esp / 2], [x + W / 2, y + L, z + esp / 2], mat_folha(x, y, L, W, 1, True, cores, nervura),
              rot=(0, dobra, 0), pivo=(x, y, z), res=6)
    pb = peca(nome + "_b", [x - W / 2, y, z - esp / 2], [x, y + L, z + esp / 2], mat_folha(x, y, L, W, -1, False, cores, nervura),
              rot=(0, -dobra, 0), pivo=(x, y, z), res=6)
    return osso(nome, list(raiz), apontar(d), [osso(nome + "_t", list(raiz), [0, torce, 0], [pa, pb])])

# ---------------- cabeça ----------------
HW = 5.0          # meia largura da cabeça
QX = 2.5          # meia largura da frente reta (onde nasce o bico)
ZF = -9.0         # frente da cabeça
ZT = -1.2         # nuca
FL = math.hypot(HW - QX, HW - QX)       # comprimento da face diagonal (olho)
ZS = ZF + (HW - QX)                     # z onde a face diagonal encontra o lado
FT = 1.8                                # espessura da peça da face diagonal
OLHO_Y = 27.3
CAB_Y0, CAB_Y1 = 23.4, 31.0

def cor_cabeca(p, face):
    """Coroa e nuca marrons; máscara creme lisa do olho para baixo, descendo até a garganta."""
    x, y, z = p
    r = ruido(x, y, z) * 0.04
    if face == "up" or y > 28.7:
        return tom(mix(MARROM, CARAMELO, 0.25), r)
    lim = -4.4 - 1.2 * clamp((y - 25.5) / 3.0)        # a máscara recua para trás embaixo (bochecha e garganta)
    if z < lim:
        return tom(CREME, r)
    return tom(mix(MARROM, MARROM_ESC, clamp((z + 3) / 3)), r)

def fc_centro(lado):
    mx, mz = (QX + HW) / 2, (ZF + ZS) / 2
    return (lado * (mx - 0.7071 * FT / 2), mz + 0.7071 * FT / 2)

def mat_faceta(lado):
    base = mat_cor(cor_cabeca, borda=.02, curva=.3)
    fora = "east" if lado > 0 else "west"
    cx, cz = fc_centro(lado)
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u = z - cz + 0.05
            cor = pintar_olho(u, y - OLHO_Y, 1.25, 1.0, iris=((96, 132, 14), (200, 226, 64)), c_iris=(-0.12, -0.12),
                              r_iris=(0.8, 0.98), r_pup=(0.3, 0.42), bravo=0.38, alto=0.3, contorno=(60, 40, 30))
            if cor is not None: return cor
            if (u / 1.6) ** 2 + ((y - OLHO_Y) / 1.25) ** 2 <= 1 and y < 28.6: return tom(CREME, 0.06)
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return LARANJA_BICO
    if face in ("east", "west") and abs(z - ZF + 0.7) < 0.3 and abs(y - 27.2) < 0.26: return (120, 66, 18)   # narina
    if y < 25.3 and z > ZF - 3.0: return LARANJA_BICO                                                     # beirada de baixo
    return mix(AMARELO_BICO, AMARELO_ESC, clamp((26.8 - y) / 2.6))

def mat_cunha(base, y0, w, queda):
    """Recorta o fundo do bloco em V (de frente vira cunha: larga em cima, ponta embaixo no meio)."""
    def f(c):
        x, y, z = c["p"]
        if y < y0 + queda * abs(x) / w - 1e-3: return None
        return base(c)
    return f

def cor_barbela(p, face):
    x, y, z = p
    c = mix(VERM, VERM_ESC, clamp((23.0 - y) / 3.2) * 0.55)
    if abs(x) < 0.4: c = tom(c, -0.3)
    return c

def montar_cabeca():
    i0 = len(g.PECAS)
    cab = []
    mc = mat_cor(cor_cabeca, borda=.02, curva=.3)
    fx = (CAB_Y0 - 0.6, CAB_Y1 + 0.6)
    # volume chanfrado em degraus: miolo, lados recuados em cima e embaixo, topo arredondado e nuca
    cab.append(peca("cranio_miolo", [-HW + 0.7, CAB_Y0, ZS - 0.4], [HW - 0.7, CAB_Y1, ZT], mc, faixa=fx, res=4))
    cab.append(peca("cranio_lados", [-HW, CAB_Y0 + 0.7, ZS], [HW, CAB_Y1 - 0.8, ZT - 0.6], mc, faixa=fx, res=4))
    cab.append(peca("cranio_topo", [-HW + 1.6, CAB_Y1 - 0.1, ZF + 0.8], [HW - 1.6, CAB_Y1 + 0.6, ZT - 0.6], mc, faixa=fx, res=4))
    cab.append(peca("cranio_nuca", [-HW + 1.3, CAB_Y0 + 0.6, ZT - 0.2], [HW - 1.3, CAB_Y1 - 0.7, ZT + 0.7], mc, faixa=fx, res=4))
    cab.append(peca("cranio_frente", [-QX, CAB_Y0, ZF], [QX, CAB_Y1 - 0.5, ZS], mc, faixa=fx, res=4))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = fc_centro(lado)
        cab.append(peca("cranio_faceta_" + s, [cx - FT / 2, CAB_Y0 + 0.2, cz - FL / 2], [cx + FT / 2, CAB_Y1 - 0.8, cz + FL / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=fx, res=8))
    # sobrancelha: uma barra grossa marrom-chocolate por olho, contornando a quina e descendo até o bico
    msob = g.mat_facetado((112, 76, 56), (90, 60, 46), CHOCOLATE, (40, 26, 22), quina=-0.3)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = fc_centro(lado)
        ox = cx + lado * (FT / 2)
        x0, x1 = sorted((ox - 0.4 * lado, ox + 0.9 * lado))
        cab.append(osso("sobrancelha_" + s, [cx, 29.0, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, 28.3, cz - FL / 2 - 0.6], [x1, 29.7, cz + FL / 2 + 1.2], msob,
                 rot=(-14, 0, 0), pivo=(cx, 29.0, cz))]))
        # trecho da frente: continua a barra a partir da quina (mesma altura) e desce até o meio, por cima do bico
        x0, x1 = sorted((0.1 * lado, (QX + 0.6) * lado))
        cab.append(peca("sobrancelha_frente_" + s, [x0, 27.75, ZF - 0.9], [x1, 29.15, ZF + 0.4], msob,
                        rot=(0, 0, 13 * lado), pivo=((QX + 0.6) * lado, 28.45, ZF - 0.25)))
    # bico grande em gancho, em camadas que afinam e descem para a frente: de frente é uma cunha que termina
    # em ponta embaixo; de perfil o alto do bico curva para baixo até o gancho, por cima do bico de baixo
    mb = mat_cor(cor_bico, borda=.05, curva=.3)
    fb = (23.4, 28.2)
    mb = mat_cor(cor_bico, borda=.0, curva=.3)
    for k, (w, y0, y1, z0, z1) in enumerate(((2.0, 25.3, 28.0, ZF - 1.6, ZF + 0.4), (1.5, 24.8, 27.6, ZF - 2.9, ZF - 1.0),
                                             (0.95, 24.0, 26.8, ZF - 3.9, ZF - 2.4), (0.5, 23.3, 25.4, ZF - 4.3, ZF - 3.3))):
        cab.append(peca(f"bico{k}", [-w, y0, z0], [w, y1, z1], mat_cunha(mb, y0, w, (1.4, 1.4, 1.0, 0.5)[k]), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-0.75, 24.5, ZF - 2.2], [0.75, 26.6, ZF + 0.3],
                    mat_cor(lambda p, f: LARANJA_BICO if f == "down" else AMARELO_ESC, borda=.12), res=4))
    # barbela: dois lóbulos vermelhos grossos, quase encostados, pendurados logo abaixo do bico
    mbb = mat_cor(cor_barbela, borda=.06, curva=.4)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.12 * lado, 2.0 * lado))
        cab.append(osso("barbela_" + s, [0.12 * lado, 24.4, ZF - 0.8], [0, 0, 3 * lado], [
            peca("barbela_" + s, [x0, 20.9, ZF - 1.9], [x1, 24.4, ZF + 0.2], mbb, faixa=(19.6, 24.4), res=4),
            peca("barbela_ponta_" + s, [x0 + 0.3 * lado, 19.8, ZF - 1.6], [x1 - 0.3 * lado, 21.0, ZF - 0.1], mbb, faixa=(19.6, 24.4), res=4)]))
    # crista: tufo denso de lâminas de folha da testa até a nuca, varrendo para cima e para trás
    crista = []
    TUFO = [  # (z raiz, abertura lateral (graus), inclinação p/ trás (graus), L, W, virada: 0 = frente, 1 = lado)
        (-8.2, 0, 22, 9.0, 4.6, 0), (-7.9, -24, 28, 7.4, 4.2, 0), (-7.9, 24, 28, 7.4, 4.2, 0),
        (-5.0, 0, 40, 10.0, 4.8, 1), (-4.8, -22, 44, 8.6, 4.4, 1), (-4.8, 22, 44, 8.6, 4.4, 1),
        (-2.4, 0, 62, 9.4, 4.6, 1), (-2.2, -28, 64, 7.6, 4.2, 1), (-2.2, 28, 64, 7.6, 4.2, 1)]
    for k, (zr, abre, tras, L, W, vira) in enumerate(TUFO):
        a, t = math.radians(abre), math.radians(tras)
        d = [math.sin(a), math.cos(t), math.sin(t)]
        lado = 1 if abre >= 0 else -1
        fora = [0, 0.3, -1] if vira == 0 else [lado, 0.2, 0]
        crista.append(folha(f"crista{k}", (1.6 * math.sin(a), CAB_Y1 - 0.2, zr), d, L, W, fora=fora, dobra=30))
    cab.append(osso("crista", [0, CAB_Y1, -5.0], [0, 0, 0], crista))
    # folhas da nuca: descem por cima do pescoço até os ombros
    for k, (ang, L) in enumerate(((0, 8.0), (-32, 7.4), (32, 7.4), (-62, 6.6), (62, 6.6))):
        a = math.radians(ang)
        d = [math.sin(a) * 0.8, -0.55, 0.8]
        cab.append(folha(f"nuca{k}", (2.4 * math.sin(a), 29.2, -0.8), d, L, 4.4, fora=[math.sin(a), 0.8, 0.5]))
    return i0, cab

# ---------------- corpo ----------------
def meia_peito(y):
    """Meia largura do peito creme na altura y (largo no meio do peito, afinando para a barriga e para o pescoço)."""
    return 3.0 + 2.0 * clamp((y - 10.6) / 7.5) ** 0.7 - 1.2 * clamp((y - 19.5) / 4.0) ** 1.5

def dente(x, passo=1.35):
    """Onda triangular 0..1 (pontas de pena)."""
    t = (x / passo) % 1.0
    return 1 - abs(t - 0.5) * 2

def mat_camada(yb, yt):
    """Camada de penas creme do peito: pontas recortadas embaixo (dentes), sombra perto da ponta,
    risco escuro entre as penas e luz em cima."""
    def f(c):
        x, y, z = c["p"]
        if abs(x) > meia_peito(y) + 0.4: return None
        borda = yb + 1.0 * (1 - dente(x))
        if y < borda: return None
        t = clamp((y - borda) / 1.8)
        cor = mix(CREME_ESC, CREME, t)
        if c["face"] == "north":
            if y < borda + 0.35: cor = tom(cor, -0.22)
            elif dente(x) < 0.12 and y < borda + 1.6: cor = tom(cor, -0.12)
        elif c["face"] in ("east", "west", "down"): cor = tom(cor, -0.18)
        else: cor = tom(cor, 0.15)
        return tom(cor, ruido(x, y, z) * 0.04)
    return f

def cor_corpo(p, face):
    x, y, z = p
    r = ruido(x, y, z) * 0.05
    if z < -4.5 and abs(x) < meia_peito(y) and y > 10.6:
        return tom(CREME, r + 0.04 * clamp((y - 16) / 6))
    # penas marrons em escamas
    fila = math.floor((26 - y) / 1.4)
    fy = ((26 - y) / 1.4) % 1.0
    fx = ((x + z + (0.7 if fila % 2 else 0)) / 1.4) % 1.0
    base = mix(MARROM, MARROM_ESC, clamp((13 - y) / 6))
    if fy > 0.7 - 0.3 * abs(fx - 0.5): base = tom(base, -0.18)
    return tom(base, r)

def cor_dorso(p, face):
    """Massa traseira de onde saem os espinhos: marrom escuro, para os vãos entre os espinhos lerem fundos."""
    x, y, z = p
    return tom(mix(MARROM_ESC, MARROM, 0.3), ruido(x, y, z) * 0.06 - 0.05)

def cor_coxa(p, face):
    x, y, z = p
    r = ruido(x, y, z) * 0.05
    a = math.atan2(z, abs(x) - 3.4)
    barra = 5.8 + 0.7 * abs(math.sin(a * 3.0))
    if y < barra: return tom(MARROM_ESC, r)
    return tom(mix(MARROM, CARAMELO, clamp((y - 7) / 6) * 0.4), r)

def cor_canela(p, face):
    x, y, z = p
    c = mix(CANELA, CANELA_CLARA, clamp((y - 2) / 4) * 0.5)
    if (y * 1.25) % 1.0 < 0.14: c = tom(c, -0.15)       # escamas da canela
    return c

def montar():
    # ---------- cabeça, pescoço ----------
    i_cab, cab = montar_cabeca()
    cabeca = osso("cabeca", [0, 25.0, -4.5], [0, 0, 0], cab)
    mp = mat_cor(lambda p, f: tom(CREME, ruido(*p) * .04) if p[2] < -4.6 else tom(MARROM, ruido(*p) * .04), borda=.02, curva=.25)
    pescoco = osso("pescoco", [0, 22.0, -3.5], [0, 0, 0], [
        peca("pescoco", [-3.4, 19.6, -8.5], [3.4, 24.0, -1.0], mp, faixa=(18, 26)),
        cabeca])

    corpo = []
    mt = mat_cor(cor_corpo, borda=.02, curva=.45)
    # corpo em pera: base larga e redonda, parte de cima mais estreita
    corpo += arredondado2("barriga", [-7.0, 5.6, -6.8], [7.0, 16.4, 6.4], mt, r=3.4, faixa=(5, 24))
    corpo += arredondado2("tronco", [-5.6, 12.0, -6.9], [5.6, 23.4, 5.0], mt, r=2.2, faixa=(5, 24))
    corpo += arredondado("peito", [-4.6, 10.4, -8.0], [4.6, 22.0, -4.0], mt, r=1.2, faixa=(5, 24))
    # 'Flor Peitoral': 4 camadas de penas creme com pontas recortadas, embutidas no peito (só a ponta sobressai)
    for k, (yb, yt) in enumerate(((18.6, 22.0), (16.0, 20.0), (13.2, 17.2), (10.6, 14.4))):
        w = max(meia_peito(yb + (yt - yb) * t / 10) for t in range(11)) + 0.4
        z0 = -8.35 + 0.08 * k
        corpo.append(peca(f"peito_camada{k}", [-w, yb, z0], [w, yt, z0 + 0.45], mat_camada(yb, yt), res=5))

    # ---------- espinhos: meia cúpula densa saindo da massa traseira arredondada ----------
    C = (0.0, 18.5, 3.5)
    corpo += arredondado2("dorso", [-7.0, 10.0, -2.6], [7.0, 27.2, 10.8], mat_cor(cor_dorso, borda=.02, curva=.4), r=3.0, faixa=(9, 27))
    rnd = random.Random(11)
    ANEIS = [(12, [45 + 90 * k for k in range(4)], 20.0), (32, [45 * k + 22 for k in range(8)], 19.5),
             (52, [36 * k for k in range(10)], 18.0), (72, [30 * k + 15 for k in range(12)], 16.0),
             (90, [-100, -64, -30, 0, 30, 64, 100], 11.5)]
    cauda, esp_corpo = [], []
    n = 0
    for teta, phis, L in ANEIS:
        for phi in phis:
            phi = ((phi + 180) % 360) - 180
            d = dir_esf(teta, phi)
            if d[1] < -0.62: continue
            d = norm([d[0] * 0.62, d[1] * 0.85 + 0.08, d[2] + 0.25])          # para trás e um pouco para cima
            Lk = L * rnd.uniform(0.94, 1.06) * (0.88 if d[1] < -0.4 else 1.0) * (0.8 if teta >= 90 and abs(phi) > 80 else 1.0)
            Wk = 4.8 if teta < 80 else 4.2
            rb = 2.4
            raiz = (C[0] + d[0] * rb, C[1] + d[1] * rb, C[2] + d[2] * rb)
            q = espinho(f"espinho{n}", raiz, d, Lk, Wk)
            (cauda if teta < 35 else esp_corpo).append(q)
            n += 1
    corpo.append(osso("espinhos", list(C), [0, 0, 0], esp_corpo))
    corpo.append(osso("cauda", [0, 18.5, 8.0], [0, 0, 0], cauda))

    # ---------- asas: plumagem de folhas nos ombros, em camadas varrendo para baixo e para trás ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        # (y raiz, z raiz, ângulo para trás (0 = para baixo, 90 = para trás), abertura p/ fora, L, W)
        MANTO = [  # fileira de baixo: folhas compridas, rentes ao corpo (as 'rêmiges')
                 (22.0, -3.0, 34, 16, 9.0, 4.0), (22.2, -0.6, 48, 16, 9.6, 4.0), (22.2, 1.8, 62, 18, 9.4, 4.0),
                 (21.8, 4.0, 74, 20, 8.4, 3.8),
                 # fileira de cima: folhas mais curtas e abertas por cima (as 'coberteiras')
                 (24.0, -4.6, 22, 28, 7.4, 3.8), (24.2, -2.0, 40, 28, 7.8, 4.0), (24.2, 0.6, 56, 28, 7.4, 3.8),
                 # da frente: desce do lado do peito
                 (20.6, -5.6, -6, 30, 9.6, 3.6)]
        for k, (y0, z0, tras, abre, L, W) in enumerate(MANTO):
            t, a = math.radians(tras), math.radians(abre)
            d = [lado * math.sin(a), -math.cos(t) * math.cos(a), math.sin(t) * math.cos(a)]
            asa.append(folha(f"asa{k}_{s}", (5.4 * lado, y0, z0), d, L, W * 1.3, fora=[lado, 0.3, -0.1]))
        corpo.append(osso("asa_" + s, [5.4 * lado, 22.5, -1.0], [0, 0, 0], asa))
    # folhas de colar em volta do peito (emolduram a 'Flor Peitoral')
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, (x0, y0, ang, L) in enumerate(((4.0, 21.0, 16, 9.0), (4.6, 18.4, 26, 8.4))):
            a = math.radians(ang)
            d = [lado * math.sin(a), -math.cos(a), -0.25]
            corpo.append(folha(f"colar{k}_{s}", (x0 * lado, y0, -7.0), d, L, 4.4, fora=[lado * 0.5, 0.2, -1]))
    # penas marrons na base larga do corpo
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, (phi, y0, L, W) in enumerate(((-40, 12.4, 6.4, 4.4), (8, 13.0, 7.0, 4.6), (52, 12.8, 6.6, 4.4))):
            x, z = g.anel(6.4, 6.4, 0.0, phi, lado)
            fora = [lado * math.cos(math.radians(phi)), 0.1, math.sin(math.radians(phi))]
            d = [fora[0] * 0.4, -1.0, fora[2] * 0.4 + 0.1]
            corpo.append(folha(f"flanco{k}_{s}", (x, y0, z), d, L, W, fora=fora, dobra=24,
                               cores=(MARROM_ESC, MARROM, CARAMELO), nervura=tom(CARAMELO, 0.1)))
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 11.0, 1.0], [0, 0, 0], corpo)

    # ---------- pernas curtas e grossas, pés de 3 dedos com garras escuras grandes ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 3.5 * lado; zc = -0.5
        pp = []
        pp += arredondado("coxa_" + s, [xc - 3.0, 5.0, zc - 3.0], [xc + 3.0, 10.5, zc + 2.8], mat_cor(cor_coxa, borda=.03, curva=.4), r=0.9, faixa=(5, 12))
        pp += octogono("canela_" + s, [xc - 2.1, 1.4, zc - 2.0], [xc + 2.1, 6.0, zc + 2.0], mat_cor(cor_canela, borda=.06, curva=.4), r=0.7, faixa=(1.5, 7))
        mpe = mat_cor(lambda p, f: tom(CANELA_CLARA, .1) if f == "up" else CANELA_CLARA, borda=.12, curva=.5)
        mg = g.mat_facetado(GARRA_CLARA, GARRA, mix(GARRA, (40, 36, 40), .3), (34, 30, 34), quina=-0.3)
        pp.append(peca("pe_" + s, [xc - 2.3, 0.0, zc - 2.3], [xc + 2.3, 1.8, zc + 1.7], mpe, faixa=(0, 2.2)))
        for nome, giro, dx in (("meio", 0, 0), ("fora", -14 * lado, 1.65 * lado), ("dentro", 14 * lado, -1.65 * lado)):
            x0, z0 = xc + dx, zc - 2.1
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .75, 0, z0 - 1.6], [x0 + .75, 1.5, z0 + 0.3], mpe, faixa=(0, 2.2)),
                peca(f"garra_{nome}_{s}", [x0 - .85, 0.0, z0 - 3.3], [x0 + .85, 1.9, z0 - 1.5], mg, faixa=(0, 2.0)),
                peca(f"garra_ponta_{nome}_{s}", [x0 - .55, 0.0, z0 - 4.3], [x0 + .55, 1.1, z0 - 3.2], mg, faixa=(0, 2.0))]))
        pp.append(peca("dedo_tras_" + s, [xc - .75, 0, zc + 1.5], [xc + .75, 1.3, zc + 2.9], mpe, faixa=(0, 2.0)))
        pp.append(peca("garra_tras_" + s, [xc - .85, 0, zc + 2.8], [xc + .85, 1.5, zc + 4.1], mg, faixa=(0, 2.0)))
        return osso("perna_" + s, [xc, 10.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

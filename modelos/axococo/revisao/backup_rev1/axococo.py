"""Axococó (#008, Água): o galo-axolote das águas, rosa-claro, com brânquias de axolote, asas com espiral azul
e um leque de cauda azul (do azul-claro ao azul-marinho)."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, mat_cor, arredondado, arredondado2

ID = "axococo"; NOME = "Axococó"; NUMERO = 8
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 26, -12), 9)

# ---------------- paleta (Paleta de Cores da ficha) ----------------
CREME = (252, 236, 226)
ROSA_PALIDO = (250, 216, 224)
ROSA_CLARO = (245, 174, 197)
ROSA = (237, 132, 165)
ROSA_FORTE = (232, 98, 140)
MAGENTA = (222, 44, 102)
MAGENTA_ESC = (172, 24, 78)
AZUL_CLARO = (92, 186, 246)
AZUL = (46, 118, 224)
AZUL_ESC = (22, 56, 168)
AMARELO = (252, 194, 30)
AMARELO_CLARO = (255, 222, 96)
LARANJA = (240, 150, 24)
VERMELHO = (220, 30, 56)
VERMELHO_ESC = (160, 16, 40)
CINZA = (104, 90, 114)
CINZA_CLARO = (140, 126, 152)
BRANCO = (250, 248, 246); PRETO = (20, 14, 26)


# ---------------- padrões pintados ----------------
def horiz(p, face):
    """Coordenada horizontal ao longo da face (x nas faces de frente/trás/cima, z nas laterais)."""
    return p[0] if face in ("north", "south", "up", "down") else p[2]

def escama(p, face, alt=1.8, larg=2.4):
    """Fileiras de penas em escama: devolve (na_linha, t) — linha escura na borda de baixo de cada pena e t
    (0 embaixo .. 1 em cima da pena) para um degradê leve dentro dela."""
    y = p[1]; h = horiz(p, face)
    r = math.floor(y / alt)
    off = larg / 2 if r % 2 else 0.0
    xx = ((h + off) % larg) / larg - 0.5
    yy = (y % alt) / alt
    borda = yy - 1.9 * xx * xx
    return 0.0 <= borda < 0.16, yy

def espiral(a, b, passo=1.8, larg=1.2, voltas=1.75, r0=0.0):
    """Espiral azul da 'Plumagem Úmida' (quadradinha), com uma cauda que sai para trás e para baixo.
    a = horizontal (positivo = para trás), b = vertical. Devolve True dentro da faixa azul."""
    a = a / 1.3
    r = max(abs(a), abs(b)) * 0.6 + math.hypot(a, b) * 0.4
    phi = math.atan2(b, -a) % (2 * math.pi)
    for k in range(4):
        th = phi + 2 * math.pi * k
        if th > voltas * 2 * math.pi: break
        if abs(r - (r0 + passo * th / (2 * math.pi))) < larg / 2: return True
    if r < larg * 0.55: return True
    # cauda: sai do fim da espiral e corre para trás, descendo
    yb = -(r0 + passo * voltas) * 0.9 + 0.22 * a
    if -4.4 <= a <= 0.3 and abs(b - yb) < larg / 2: return True
    return False


# ---------------- materiais ----------------
def cor_corpo(p, face):
    """Corpo: costas e lados rosa-claro; peito e barriga creme; escamas de pena por todo lado."""
    x, y, z = p
    frente = clamp((-z - 4.0) / 5.0) * clamp(1.0 - (abs(x) - 4.5) / 3.0)
    barriga = clamp((10.0 - y) / 3.0) * clamp((-z + 6) / 6)
    base = mix(ROSA_CLARO, CREME, max(frente, barriga))
    if face == "up":                       # costas vistas de cima: fileiras de penas correndo para trás
        linha, t = escama((x, -z, 0), "north", alt=2.0, larg=2.6)
        return tom(base, -.22) if linha else tom(base, .05 + .08 * t)
    linha, t = escama(p, face)
    if linha: return tom(base, -.30)
    return tom(base, .10 * t - .04)

def mat_babado(y0, y1, dente=1.8, fundo_dente=1.0):
    """Fileira de penas do peito: placa creme com a beirada de baixo em dentes de degrau (recorte) e fio escuro."""
    def f(c):
        x, y, z = c["p"]
        u = ((x + dente / 2) % dente) / dente
        fundo = y0 + fundo_dente * math.floor(abs(u - 0.5) * 2 * 2.999) / 2
        if y < fundo - 1e-6: return None
        if c["face"] != "north": return tom(CREME, -.15 if c["face"] != "up" else .08)
        cor = tom(mix(CREME, ROSA_PALIDO, clamp((y - y0) / (y1 - y0)) * .6), .14 - .14 * clamp((y1 - y) / (y1 - y0)))
        if y - fundo < 0.4: return tom(cor, -.42)
        return cor
    return f

def mat_fileira(fora, y0, y1, c0, c1, dente=2.4, fundo_dente=1.2):
    """Fileira de penas sobreposta na asa: placa fina cuja beirada de baixo é recortada em dentes (pontas de
    pena), degradê c0 (embaixo) -> c1 (em cima) e fio escuro na beirada."""
    def f(c):
        x, y, z = c["p"]
        u = ((z + dente / 2) % dente) / dente
        fundo = y0 + fundo_dente * math.floor(abs(u - 0.5) * 2 * 3.999) / 3     # dentes em degraus (voxel)
        if y < fundo: return None
        cor = mix(c0, c1, clamp((y - y0) / (y1 - y0)))
        if c["face"] == "up": return tom(cor, .15)
        if c["face"] != fora: return tom(cor, -.15)
        if y - fundo < 0.28: return tom(cor, -.32)
        linha, t = escama(c["p"], c["face"], alt=2.0, larg=2.8)
        return tom(cor, .1 * t - .02)
    return f

def mat_corpo(**kw):
    return mat_cor(cor_corpo, **kw)

def no_mundo(mat, ry, pivo):
    """Pinta uma peça girada em y com as coordenadas do MUNDO (a pintura normal usa as da peça sem girar)."""
    a = math.radians(ry); ca, sa = math.cos(a), math.sin(a)
    def f(c):
        x, y, z = (c["p"][i] - pivo[i] for i in range(3))
        c = dict(c); c["p"] = (pivo[0] + x * ca + z * sa, c["p"][1], pivo[2] - x * sa + z * ca)
        return mat(c)
    return f

def cor_cabeca(p, face):
    x, y, z = p
    base = ROSA_CLARO
    if face == "north" and z < CAB_ZF + 0.1 and 0 <= y - (27.3 + 0.42 * abs(x)) < 0.55: return ROSA   # V bravo da testa
    if z < -10.0 and y < 25.0: base = mix(ROSA_CLARO, ROSA_PALIDO, clamp((25.0 - y) / 2.0))   # bochecha clara
    if face == "up": base = mix(ROSA_CLARO, ROSA, .2)
    if face == "south" or (face == "up" and z > -2.6):      # nuca: penas miúdas discretas
        linha, t = escama((x, y if face == "south" else -z, 0), "north", alt=1.6, larg=2.0)
        if linha: return tom(base, -.16)
    return base

# rosto: frente reta estreita + faces diagonais (45°) com o olho inteiro numa face plana
OLHO_Y = 26.1
FAC_T = 1.6          # espessura da peça da faceta
FRENTE_X = 3.0       # meia largura da frente reta do rosto
CAB_X = 7.6          # meia largura da cabeça
CAB_ZF = -15.0       # frente do rosto
FAC_D = CAB_X - FRENTE_X                      # recuo da faceta (45°)
FAC_L = FAC_D * math.sqrt(2) + 0.3            # comprimento da peça da faceta
FAC_M = ((FRENTE_X + CAB_X) / 2, CAB_ZF + FAC_D / 2)        # meio da linha da faceta (x, z)
FAC_C = (FAC_M[0] - 0.7071 * FAC_T / 2, FAC_M[1] + 0.7071 * FAC_T / 2)   # centro da peça (lado +x)

def olho(u, v):
    """Olho na face plana: u ao longo da face (negativo = para o bico), v para cima.
    Contorno azul grosso atrás (o 'olho azul' da ficha), esclera branca, pupila preta grande perto do bico,
    pálpebra brava cortando o alto (desce para o bico)."""
    ru, rv = 2.35, 1.85
    e = (u / ru) ** 2 + (v / rv) ** 2
    if e > 1: return None
    if v / rv > 0.52 + 0.40 * (u / ru): return None                          # pálpebra brava
    iu, iv = u / ru + 0.30, v / rv + 0.02
    if ((iu - 0.10) / 0.13) ** 2 + ((iv - 0.26) / 0.17) ** 2 <= 1: return (255, 255, 255)    # brilho
    dp = (iu / 0.36) ** 2 + (iv / 0.56) ** 2
    if dp <= 1: return PRETO
    if dp <= 1.6: return mix(AZUL_ESC, AZUL, clamp((iv + .6) / 1.2))        # íris azul fina em volta da pupila
    if e > 0.78 or (u / ru > 0.30 and e > 0.40): return mix(AZUL, AZUL_CLARO, clamp(v / rv + .3))   # contorno azul
    return mix(BRANCO, (214, 214, 230), clamp(-v / rv))

def mat_faceta(lado):
    base = mat_cor(cor_cabeca, borda=.03, curva=.35)
    fora = "east" if lado > 0 else "west"
    def f(c):
        if c["face"] == fora:
            x, y, z = c["p"]
            cor = olho(z - FAC_C[1], y - OLHO_Y)
            if cor is not None: return cor
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face in ("east", "west") and abs(z + 16.9) < 0.3 and abs(y - 24.6) < 0.25: return (150, 84, 20)   # narina
    if face == "up": return AMARELO_CLARO
    return mix(AMARELO, LARANJA, clamp((23.8 - y) / 1.6) * .8 + clamp((-z - 17.5) / 2.0) * .3)

def mat_pena_azul(c0, c1, ei, inv):
    """Pena azul da cauda: degradê, raque clara e beirada de trás escura (g.mat_asa) com borda mais suave."""
    return g.mat_asa(c0, c1, ei, inv, borda=.16)

def mat_rosa(c0, c1, ei, inv):
    return g.mat_asa(c0, c1, ei, inv, borda=.18)


def pena_cauda(nome, base, segs, rot0, curva, mat_fn, sobrepoe=1.0):
    """Como g.pena_curva (eixo 'y'), mas cada segmento começa 'sobrepoe' antes do fim do anterior: na curva
    forte das penas largas da cauda não abre fresta entre os segmentos. Ossos '<nome>_0', '<nome>_1'..."""
    def seg(k, pos):
        L, w, h, c0, c1 = segs[k]
        px, py, pz = pos
        filhos = [peca(f"{nome}_{k}", [px - w / 2, py, pz - h / 2], [px + w / 2, py + L, pz + h / 2], mat_fn(c0, c1, 1, False))]
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py + L - sobrepoe, pz)))
        return osso(f"{nome}_{k}", list(pos), list(rot0) if k == 0 else list(curva), filhos)
    return seg(0, tuple(base))


# ---------------- brânquias ----------------
def guelra(nome, raiz, lado, L, recuo, eleva, n_cima=6):
    """Brânquia de axolote: haste rosa grossa que sai do lado da cabeça (para fora e para trás) com a franja de
    filamentos magenta em cima e rosa embaixo, inclinados para a ponta. Osso externo sem rotação (é ele que
    balança na animação); o interno dá a direção."""
    x, y, z = raiz
    s = lado
    pcs = []
    def bx(a, b):        # intervalo em x 'para fora' (cresce no sentido do lado)
        return sorted((x + a * s, x + b * s))
    x0, x1 = bx(-0.8, L * 0.6)
    pcs.append(peca(nome + "_haste", [x0, y - 1.2, z - 0.9], [x1, y + 1.2, z + 0.9], g.mat_pena(ROSA_CLARO, ROSA, 0, s < 0)))
    x0, x1 = bx(L * 0.6 - 0.1, L)
    pcs.append(peca(nome + "_ponta", [x0, y - 1.0, z - 0.8], [x1, y + 1.0, z + 0.8], g.mat_pena(ROSA, ROSA_FORTE, 0, s < 0)))
    passo = (L - 1.2) / n_cima
    for k in range(n_cima):                        # franja de cima (magenta): degraus inclinados para a ponta
        cx = x + (0.9 + passo * (k + 0.5)) * s
        h = 2.2 - 0.12 * k
        x0, x1 = sorted((cx - 0.8 * s, cx + 0.8 * s))
        pcs.append(peca(f"{nome}_fc{k}", [x0, y + 0.7, z - 0.8], [x1, y + 0.8 + h, z + 0.8],
                        g.mat_pena(ROSA_FORTE, MAGENTA, 1, False), rot=(0, 0, -30 * s), pivo=(cx, y + 0.8, z)))
    for k in range(n_cima - 1):                    # franja de baixo (rosa)
        cx = x + (0.9 + passo * (k + 1.0)) * s
        h = 1.8 - 0.1 * k
        x0, x1 = sorted((cx - 0.75 * s, cx + 0.75 * s))
        pcs.append(peca(f"{nome}_fb{k}", [x0, y - 0.8 - h, z - 0.75], [x1, y - 0.8, z + 0.75],
                        g.mat_pena(ROSA, ROSA_FORTE, 1, True), rot=(0, 0, 30 * s), pivo=(cx, y - 0.8, z)))
    dentro = osso(nome + "_dir", list(raiz), [0, -recuo * s, eleva * s], pcs)
    return osso(nome, list(raiz), [0, 0, 0], [dentro])

GUELRAS = [  # (y da raiz, z da raiz, comprimento, recuo (graus para trás), elevação (graus para cima))
    (30.0, -6.6, 11.2, 52, 30),
    (27.4, -6.0, 11.8, 54, 4),
    (24.8, -6.4, 10.4, 50, -22),
]

def anim_guelras():
    """Balanço das brânquias: cada uma oscila em z (sobe e desce) e um pouco em y, fora de fase."""
    parado, andando = {}, {}
    for lado, s_ in ((-1, "d"), (1, "e")):
        for k in range(len(GUELRAS)):
            fase = k * 2 * math.pi / 3 + (0.5 if lado > 0 else 0)
            def kf(a, b):
                q = [(0, round(b * math.cos(2 * math.pi * i / 4 + fase), 2), round(a * lado * math.sin(2 * math.pi * i / 4 + fase), 2))
                     for i in range(4)]
                return q + [q[0]]                  # o último keyframe igual ao primeiro
            parado[f"guelra_{s_}_{k}"] = kf(7, 4)
            andando[f"guelra_{s_}_{k}"] = kf(12, 6)
    return parado, andando

ANIM_PARADO, ANIM_ANDANDO = anim_guelras()
ONDAS = [("cauda_p0", 4, (4, 0, 0)), ("cauda_p1", 4, (4, 0, 0))]


def montar():
    # ---------------- cabeça ----------------
    cab = []
    mc = mat_cor(cor_cabeca, borda=.03, curva=.35)
    FX = (20.5, 32.5)
    cab += arredondado2("cranio", [-CAB_X, 21.0, CAB_ZF + FAC_D - 0.6], [CAB_X, 32.0, -1.4], mc, r=1.6, faixa=FX, res=4)
    cab.append(peca("cranio_frente", [-FRENTE_X, 21.0, CAB_ZF], [FRENTE_X, 32.0, CAB_ZF + FAC_D + 0.5], mc, faixa=FX, res=4))
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s_, [cx - FAC_T / 2, 21.0, cz - FAC_L / 2], [cx + FAC_T / 2, 32.0, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=FX, res=8))
        # sobrancelha brava: placa rosa por cima do olho, descendo para o bico
        fx0, fx1 = sorted((cx + FAC_T / 2 * lado - 0.1 * lado, cx + FAC_T / 2 * lado + 0.32 * lado))
        cab.append(osso("sobrancelha_" + s_, [cx, 28.0, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s_, [fx0, 27.4, cz - FAC_L / 2 - 0.1], [fx1, 28.5, cz + FAC_L / 2], mat_cor(lambda p, f: mix(ROSA, ROSA_CLARO, .3) if f != "down" else ROSA_FORTE, borda=.12),
                 rot=(-12, 0, 0), pivo=(cx, 28.0, cz))]))
    # bico em cunha: base, meio e ponta inclinada; bico de baixo laranja
    mb = mat_cor(cor_bico, borda=.06, curva=.4)
    cab.append(peca("bico_base", [-2.5, 22.4, CAB_ZF - 1.4], [2.5, 25.7, CAB_ZF + 0.4], mb, faixa=(21.5, 25.8)))
    cab.append(peca("bico_meio", [-2.1, 22.6, CAB_ZF - 3.3], [2.1, 25.3, CAB_ZF - 1.3], mb, rot=(-8, 0, 0), pivo=(0, 25.3, CAB_ZF - 1.3), faixa=(21.5, 25.8)))
    cab.append(peca("bico_ponta", [-1.6, 22.3, CAB_ZF - 4.6], [1.6, 24.8, CAB_ZF - 3.1], mb, rot=(-22, 0, 0), pivo=(0, 24.8, CAB_ZF - 3.1), faixa=(21.5, 25.8)))
    cab.append(peca("bico_baixo", [-1.9, 21.5, CAB_ZF - 2.8], [1.9, 22.5, CAB_ZF + 0.2], mat_cor(lambda p, f: LARANJA, borda=.12)))
    # barbela vermelha: dois lóbulos pendurados embaixo do bico
    mbar = mat_cor(lambda p, f: mix(VERMELHO, VERMELHO_ESC, clamp((20.5 - p[1]) / 3.5)), borda=.1, curva=.3)
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.1 * lado, 2.4 * lado))
        xa, xb = sorted((0.4 * lado, 2.1 * lado))
        cab.append(osso("barbela_" + s_, [0.1 * lado, 22.0, CAB_ZF - 1.5], [0, 0, 7 * lado], [
            peca("barbela_" + s_, [x0, 19.0, CAB_ZF - 2.4], [x1, 22.0, CAB_ZF - 0.7], mbar),
            peca("barbela_ponta_" + s_, [xa, 16.8, CAB_ZF - 2.25], [xb, 19.2, CAB_ZF - 0.85], mbar)]))
    # crista aquática: blocos magenta grandes em degraus no alto da cabeça
    mcr = mat_cor(lambda p, f: mix(MAGENTA_ESC, MAGENTA, clamp((p[1] - 31.0) / 3.5)) if f != "up" else mix(MAGENTA, ROSA_FORTE, .3),
                  borda=.14, curva=.25)
    crista = []
    for k, (z0, z1, w, h) in enumerate([(-14.0, -10.4, 2.2, 5.0), (-11.0, -7.4, 2.5, 7.4), (-8.0, -4.2, 2.4, 8.0), (-4.8, -1.0, 1.9, 5.6)]):
        crista.append(peca(f"crista_{k}", [-w, 31.6, z0], [w, 31.6 + h, z1], mcr, faixa=(31.4, 39.0)))
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        x0, x1 = sorted((1.6 * lado, 3.6 * lado))
        crista.append(peca("crista_lado_" + s_, [x0, 31.6, -12.4], [x1, 35.0, -4.6], mcr, faixa=(31.4, 39.0)))
    cab.append(osso("crista", [0, 32, -7], [0, 0, 0], crista))
    # brânquias (3 de cada lado)
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        for k, (y0, z0, L, rec, ele) in enumerate(GUELRAS):
            cab.append(guelra(f"guelra_{s_}_{k}", (7.2 * lado, y0, z0), lado, L, rec, ele))
    cabeca = osso("cabeca", [0, 23, -8], [0, 0, 0], cab)

    # ---------------- pescoço ----------------
    pescoco = osso("pescoco", [0, 20, -7], [0, 0, 0], [
        peca("pescoco", [-4.6, 17.5, -12.0], [4.6, 23.0, -3.0], mat_corpo(borda=.04, curva=.3), faixa=(7, 24), res=4),
        cabeca])

    # ---------------- corpo em ovo: tronco, barriga, dorso e peito facetado ----------------
    corpo = []
    mt = mat_corpo(borda=.03, curva=.5)
    FC = (6.8, 23.0)
    corpo += arredondado2("tronco", [-8.8, 10.4, -10.6], [8.8, 22.0, 12.6], mt, r=3.0, faixa=FC, res=4)
    corpo += arredondado2("barriga", [-6.4, 6.8, -9.6], [6.4, 13.0, 7.0], mt, r=2.2, faixa=FC, res=4)
    corpo += arredondado("dorso", [-6.4, 20.8, -8.0], [6.4, 23.0, 10.2], mt, r=1.0, faixa=FC, res=4)
    # peito: frente reta creme + duas faces diagonais (45°): de 3/4 lê arredondado, sem degraus
    PX, PZ, PY0, PY1, PD = 5.0, -15.0, 9.4, 21.0, 4.2
    corpo.append(peca("peito", [-PX - 0.1, PY0, PZ], [PX + 0.1, PY1, -9.0], mt, faixa=FC, res=4))
    for lado in (-1, 1):
        mx, mz = PX + PD / 2, PZ + PD / 2
        T = 3.2
        cx, cz = (mx - 0.7071 * T / 2) * lado, mz + 0.7071 * T / 2
        fl = PD * math.sqrt(2) + 0.2
        corpo.append(peca("peito_faceta_" + ("d" if lado < 0 else "e"), [cx - T / 2, PY0 + 0.4, cz - fl / 2], [cx + T / 2, PY1 - 0.4, cz + fl / 2],
                          no_mundo(mt, 45 * lado, (cx, 15.0, cz)), rot=(0, 45 * lado, 0), pivo=(cx, 15.0, cz), faixa=FC, res=4))
    # babador: fileiras de penas creme em degraus no peito (V para baixo, como na ficha)
    for k, (w, y0, y1) in enumerate([(4.7, 17.0, 21.0), (3.8, 14.2, 17.8), (2.8, 11.4, 15.0)]):
        z0 = PZ - 0.5 + 0.12 * k
        corpo.append(peca(f"babado_{k}", [-w, y0, z0], [w, y1, z0 + 0.45], mat_babado(y0, y1), res=4))
    corpo += arredondado("traseira", [-6.4, 12.0, 11.0], [6.4, 21.2, 15.0], mt, r=1.8, faixa=(6.8, 23.0), res=4)

    # ---------------- asas com a espiral azul ----------------
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        fora = "east" if lado > 0 else "west"
        def cor_asa(p, face, lado=lado, fora=fora):
            x, y, z = p
            if face == fora and abs(x) > 10.7 and espiral(z + 0.6, y - 15.0): return mix(AZUL, AZUL_ESC, clamp((17 - y) / 7))
            base = mix(ROSA, ROSA_CLARO, clamp((y - 11) / 8) * .7)
            linha, t = escama(p, face, alt=2.0, larg=2.8)
            if linha: return tom(base, -.28)
            return tom(base, .08 * t)
        ma = mat_cor(cor_asa, borda=.05, curva=.4)
        asa = []
        def caixa(nome, xa, xb, de, ate):
            x0, x1 = sorted((xa * lado, xb * lado))
            asa.append(peca(nome + "_" + s_, [x0, de[0], de[1]], [x1, ate[0], ate[1]], ma, faixa=(10.4, 21.0), res=4))
        caixa("asa_meio", 7.6, 10.8, (11.2, -8.2), (19.8, 6.0))
        caixa("asa_frente", 7.6, 10.4, (12.2, -9.4), (18.8, -8.0))
        caixa("asa_cima", 7.6, 10.2, (19.6, -7.6), (21.0, 5.4))
        caixa("asa_baixo", 7.6, 10.2, (10.4, -7.2), (11.4, 4.8))
        # fileira de coberteiras sobreposta no alto da asa (beirada de baixo em dentes recortados)
        for nome, (ya, yb, za, zb, c0, c1) in (("coberteira", (18.4, 21.3, -8.0, 4.8, ROSA, ROSA_CLARO)),):
            x0, x1 = sorted((10.5 * lado, 11.15 * lado))
            asa.append(peca(f"{nome}_{s_}", [x0, ya, za], [x1, yb, zb], mat_fileira(fora, ya, yb, c0, c1), res=4))
        # rêmiges: penas em degrau que saem para trás; as de cima mais compridas (a ponta da asa sobe para a cauda)
        for k, (y0, z0, L, H, rx) in enumerate([(20.6, 3.4, 9.6, 2.9, -8), (18.0, 4.0, 8.6, 2.9, -3), (15.4, 3.8, 7.0, 2.9, 3), (12.8, 3.0, 5.4, 2.7, 9)]):
            x0, x1 = sorted(((8.0 + 0.15 * k) * lado, (10.0 + 0.15 * k) * lado))
            asa.append(osso(f"remige_{k}_{s_}", [x0, y0, z0], [rx, 0, 0], [
                peca(f"remige_{k}_{s_}", [x0, y0 - H, z0], [x1, y0, z0 + L], mat_rosa(ROSA, ROSA_CLARO, 2, False))]))
        corpo.append(osso("asa_" + s_, [8.6 * lado, 19.5, -2.0], [0, 0, 0], asa))

    # ---------------- cauda: leque de penas azuis curvas, largas e juntas ----------------
    PENAS = [  # (x, y, z, rx inicial, curva, comprimentos, cores (raiz, ponta))
        (0.0, 20.6, 11.5, 16, 24, (5.4, 5.2, 4.8, 4.2), (AZUL_ESC, AZUL)),
        (1.3, 19.6, 12.5, 38, 21, (5.2, 5.2, 4.6, 4.2), (AZUL, AZUL_CLARO)),
        (-1.3, 18.6, 13.0, 60, 18, (5.2, 5.2, 4.6, 4.0), (AZUL_ESC, mix(AZUL, AZUL_CLARO, .5))),
        (1.4, 17.6, 13.0, 82, 15, (5.0, 5.0, 4.4, 3.8), (AZUL, AZUL_CLARO)),
        (-1.4, 16.6, 12.5, 102, 12, (4.8, 4.6, 4.2, 3.6), (AZUL_ESC, AZUL_CLARO)),
        (0.0, 15.6, 12.0, 122, 10, (4.2, 4.0, 3.6, 3.0), (AZUL, AZUL_CLARO)),
    ]
    cauda = []
    for k, (x, y, z, rx0, cv, Ls, (c0, c1)) in enumerate(PENAS):
        n = len(Ls)
        segs = []
        for i, L in enumerate(Ls):
            f0, f1 = i / n, (i + 1) / n
            segs.append((L + 0.9, 3.0 - 0.3 * i, 5.6 - 0.6 * i, mix(c0, c1, f0), mix(c0, c1, f1)))
        abre = 6 * (1 if x > 0 else -1 if x < 0 else 0)           # as de lado abrem um pouco (leque visto de trás)
        cauda.append(pena_cauda(f"cauda_p{k}", (x, y, z), segs, (rx0, abre, 0), (cv, 0, 0), mat_pena_azul, sobrepoe=1.1))
    corpo.append(osso("cauda", [0, 17, 12], [0, 0, 0], cauda))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 10, 0], [0, 0, 0], corpo)

    # ---------------- pernas e patas anfíbias ----------------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 4.8 * lado; zc = -1.0
        pp = []
        ml = mat_cor(lambda p, f: AMARELO, borda=.08, curva=.4)
        pp.append(peca("perna_" + s, [xc - 2.0, 2.2, zc - 2.0], [xc + 2.0, 9.5, zc + 2.0], ml, faixa=(0, 9.5)))
        pp.append(peca("pe_" + s, [xc - 3.0, 0.6, zc - 3.8], [xc + 3.0, 2.8, zc + 2.2], ml, faixa=(0, 9.5)))
        mg = mat_cor(lambda p, f: CINZA_CLARO if f == "up" else CINZA, borda=.18, curva=.5)
        for k, dx in enumerate((-2.05, 0.0, 2.05)):
            pp.append(peca(f"garra_{k}_{s}", [xc + dx - 0.9, 0.0, zc - 6.4], [xc + dx + 0.9, 2.2, zc - 3.2], mg, faixa=(0, 2.2)))
        pp.append(peca("garra_tras_" + s, [xc - 0.9, 0.0, zc + 1.8], [xc + 0.9, 1.8, zc + 4.0], mg, faixa=(0, 2.2)))
        return osso("perna_" + s, [xc, 9.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

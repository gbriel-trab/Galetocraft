"""Axococó (#008, Água): o galo-axolote das águas, rosa-claro, com brânquias de axolote em sol, asas com
espiral azul e um leque de foices azuis na cauda (do azul-royal ao azul-céu)."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, clamp, contexto_luz, arredondado, arredondado2

ID = "axococo"; NOME = "Axococó"; NUMERO = 8
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 26, -12), 9)

# ---------------- paleta (Paleta de Cores da ficha): rosas limpos, sem puxar para o cinza ----------------
CREME = (255, 238, 228)
ROSA_PALIDO = (255, 214, 226)
ROSA_CLARO = (252, 176, 204)
ROSA = (246, 128, 168)
ROSA_FORTE = (236, 82, 136)
MAGENTA = (222, 36, 100)
MAGENTA_ESC = (176, 20, 78)
AZUL_CEU = (104, 194, 250)
AZUL_CLARO = (70, 160, 244)
AZUL = (40, 108, 226)
AZUL_ROYAL = (26, 64, 190)
AMARELO = (255, 198, 30)
AMARELO_CLARO = (255, 226, 100)
LARANJA = (244, 150, 22)
VERMELHO = (226, 30, 56)
VERMELHO_ESC = (168, 14, 42)
CINZA = (106, 92, 118)
CINZA_CLARO = (144, 130, 158)
BRANCO = (252, 250, 248); PRETO = (18, 12, 24)


# ---------------- luz limpa ----------------
def tom(c, f):
    """Como g.tom, mas a sombra puxa para um tom mais fundo da MESMA cor (o rosa não vira malva/cinza)."""
    f = clamp(f, -1, 1)
    if f >= 0: return mix(c, (255, 250, 244), f * .42)
    return mix(c, (int(c[0] * .80), int(c[1] * .52), int(c[2] * .66)), -f * .9)

def ruido(p, escala=1.0):
    """Variação fixa por 'voxel' de 1 unidade (-1..1): o acabamento de blocos da ficha, sem linhas de tricô."""
    i, j, k = (int(math.floor(v / escala)) for v in p)
    h = (i * 73856093) ^ (j * 19349663) ^ (k * 83492791)
    return ((h & 1023) / 511.5) - 1.0

def mat_cor(cor_fn, borda=.04, curva=.32, topo=.16, baixo=.22, grao=.035):
    def f(c):
        base = cor_fn(c["p"], c["face"])
        if base is None: return None
        luz = contexto_luz(c, borda=borda, topo=topo, baixo=baixo, curva=curva) + grao * ruido(c["p"])
        return tom(base, luz)
    return f

def mat_pena(c0, c1, eixo, inverte=False, borda=.18):
    """Bloco de pena: degradê c0 -> c1 no comprimento, luz em cima, contorno escuro (com a luz limpa)."""
    def f(c):
        lo, hi = c["b"][0][eixo], c["b"][1][eixo]
        t = clamp((c["p"][eixo] - lo) / max(hi - lo, 1e-6))
        if inverte: t = 1 - t
        luz = .06 + .03 * ruido(c["p"], .8)
        if c["face"] == "up": luz += .18
        if c["face"] == "down": luz -= .3
        if g.na_borda(c): luz -= borda
        return tom(mix(c0, c1, t), luz)
    return f

def mat_foice(c0, c1, ei, inv):
    """Segmento da foice azul: degradê, raque clara no meio da face larga, beirada de dentro mais escura."""
    base = mat_pena(c0, c1, ei, inv, borda=.16)
    def f(c):
        cor = base(c)
        if c["face"] in ("east", "west"):
            (_, _, z0), (_, _, z1) = c["b"]
            d = (c["p"][2] - (z0 + z1) / 2) / max((z1 - z0) / 2, 1e-6)
            if abs(d + .15) < .14: cor = tom(cor, .14)
            elif d > .5: cor = tom(cor, -.25 * (d - .5) / .5)
        return cor
    return f

def no_mundo(mat, ry, pivo):
    """Pinta uma peça girada em y com as coordenadas do MUNDO (a pintura normal usa as da peça sem girar)."""
    a = math.radians(ry); ca, sa = math.cos(a), math.sin(a)
    def f(c):
        x, y, z = (c["p"][i] - pivo[i] for i in range(3))
        c = dict(c); c["p"] = (pivo[0] + x * ca + z * sa, c["p"][1], pivo[2] - x * sa + z * ca)
        return mat(c)
    return f


# ---------------- corpo ----------------
def cor_corpo(p, face):
    """Peito e barriga creme, costas e lados rosa-claro (coordenadas locais do tronco inclinado)."""
    x, y, z = p
    frente = clamp((-z - 4.5) / 4.0) * clamp(1.0 - (abs(x) - 4.8) / 2.5)
    barriga = clamp((10.0 - y) / 2.5) * clamp((-z + 5) / 6)
    return mix(ROSA_CLARO, CREME, max(frente, barriga))

def cor_peito(p, face):
    """Peito creme com fileiras alternadas de escamas em 'U' só pintadas (relevo de no máximo 1 px)."""
    x, y, z = p
    c = mix(CREME, ROSA_PALIDO, clamp((y - 18.0) / 5.0) * .4)
    if face in ("up", "down"): return c
    h = x if face in ("north", "south") else z
    alt, larg = 1.9, 2.6
    r = math.floor(y / alt)
    xx = ((h + (larg / 2 if r % 2 else 0)) % larg) / larg - 0.5
    yy = (y % alt) / alt
    b = yy - 1.7 * xx * xx
    if 0 <= b < 0.17: return tom(c, -.17)
    return tom(c, .05 * yy)


# ---------------- espiral da asa ----------------
def espiral(a, b, passo=1.72, larg=1.15, voltas=1.75, r0=0.0):
    """Espiral azul da 'Plumagem Úmida' (quadradinha), com a cauda que sai por baixo para a frente.
    a = horizontal (positivo = para trás), b = vertical. Devolve True dentro da faixa azul."""
    a = a / 1.25
    r = max(abs(a), abs(b)) * 0.6 + math.hypot(a, b) * 0.4
    phi = math.atan2(b, -a) % (2 * math.pi)
    for k in range(4):
        th = phi + 2 * math.pi * k
        if th > voltas * 2 * math.pi: break
        if abs(r - (r0 + passo * th / (2 * math.pi))) < larg / 2: return True
    if r < larg * 0.55: return True
    yb = -(r0 + passo * voltas) * 0.9 + 0.22 * a
    return -4.4 <= a <= 0.3 and abs(b - yb) < larg / 2


# ---------------- cabeça ----------------
CAB_X = 7.5          # meia largura da cabeça
CAB_ZF = -15.0       # frente do rosto
FRENTE_X = 3.0       # meia largura da frente reta
CAB_ZT = -4.6        # nuca
FAC_T = 1.8          # espessura das peças diagonais
OLHO_Y = 26.9

def cor_cabeca(p, face):
    x, y, z = p
    base = ROSA_CLARO
    if z < -10.0 and y < 26.0:                     # zona clara em volta do bico e embaixo dos olhos
        base = mix(ROSA_CLARO, CREME, clamp((26.0 - y) / 1.6) * .85)
    if face == "north" and abs(x) < 3.2 and y < 27.4: base = mix(base, CREME, .6)
    if face == "up": base = mix(ROSA_CLARO, ROSA_PALIDO, .25)
    return base

def olho(u, v):
    """Olho neutro (u ao longo da face, negativo = para o bico; v para cima): olho branco aberto, mancha azul
    em volta (mais grossa atrás e em cima), pupila preta com anel castanho-dourado e brilho, puxada para o
    bico; por cima, só a linha reta e inclinada da sobrancelha magenta (olhar firme)."""
    ru, rv = 2.2, 1.55
    sob = 1.22 + 0.22 * u                                  # linha da sobrancelha (desce para o bico)
    if -3.0 < u < 3.1 and sob <= v < sob + 0.55: return "sobrancelha"
    if v >= sob: return None
    e = (u / ru) ** 2 + (v / rv) ** 2
    if e <= 1 and v < sob - 0.25:
        pu, pv = u + 0.78, v + 0.0
        dp = math.hypot(pu, pv * 0.95)
        if math.hypot(pu - 0.28, pv - 0.28) < 0.22: return (255, 255, 255)                   # brilho
        if dp < 0.7: return PRETO
        if dp < 0.92: return (170, 112, 40)                                                 # anel castanho-dourado
        return BRANCO if v > -0.8 else (226, 228, 240)
    em = ((u - 0.35) / (ru + 0.8)) ** 2 + ((v - 0.15) / (rv + 0.55)) ** 2
    if em <= 1: return mix(AZUL, AZUL_CLARO, clamp(v / 2 + .4))                            # mancha azul em volta
    return None

def mat_faceta_olho(fora, cz):
    base = mat_cor(cor_cabeca, borda=.02, curva=.3)
    def f(c):
        if c["face"] == fora:
            x, y, z = c["p"]
            r = olho(z - cz, y - OLHO_Y)
            if r == "sobrancelha":
                return MAGENTA
            if r is not None: return r
        return base(c)
    return f

def camada_cabeca(nome, y0, y1, d, zt, mat, olhos=False, res=4):
    """Fatia octogonal da cabeça recuada 'd' (degraus nas quinas verticais e no alto): frente reta, faces
    diagonais a 45°, laterais e nuca. Com olhos=True, o olho vai inteiro na face diagonal (plana)."""
    pcs = []
    zf, cx = CAB_ZF + d, CAB_X - d
    fx = FRENTE_X - 0.414 * d                      # meia largura da frente
    zs = CAB_ZF + (CAB_X - FRENTE_X) - 0.586 * d   # onde a diagonal encontra a lateral
    pcs.append(peca(nome + "_frente", [-fx - 0.05, y0, zf], [fx + 0.05, y1, zs], mat, faixa=(20.5, 33.0), res=res))
    pcs.append(peca(nome + "_meio", [-cx, y0, zs - 0.4], [cx, y1, zt - 1.0], mat, faixa=(20.5, 33.0), res=res))
    pcs.append(peca(nome + "_nuca", [-cx + 1.0, y0, zt - 1.2], [cx - 1.0, y1, zt], mat, faixa=(20.5, 33.0), res=res))
    L = (cx - fx) * math.sqrt(2) + 0.25
    for lado in (-1, 1):
        mx, mz = (fx + cx) / 2, (zf + zs) / 2
        pcx, pcz = (mx - 0.7071 * FAC_T / 2) * lado, mz + 0.7071 * FAC_T / 2
        fora = "east" if lado > 0 else "west"
        m = mat_faceta_olho(fora, pcz) if olhos else no_mundo(mat, 45 * lado, (pcx, 0, pcz))
        pcs.append(peca(f"{nome}_diag_{'d' if lado < 0 else 'e'}", [pcx - FAC_T / 2, y0, pcz - L / 2], [pcx + FAC_T / 2, y1, pcz + L / 2],
                        m, rot=(0, 45 * lado, 0), pivo=(pcx, (y0 + y1) / 2, pcz), faixa=(20.5, 33.0), res=res))
    return pcs

def cor_bico(p, face):
    x, y, z = p
    if face in ("east", "west") and abs(z + 16.0) < 0.3 and abs(y - 25.5) < 0.28: return (150, 84, 20)   # narina
    if face == "up": return AMARELO_CLARO
    if 24.0 < y < 24.3 and face != "down": return (196, 104, 18)                         # linha da boca
    if y < 24.1: return LARANJA
    return mix(AMARELO_CLARO, AMARELO, clamp((26.2 - y) / 1.8))


# ---------------- brânquias ----------------
def guelra(nome, raiz, lado, L, recuo, eleva, n=7):
    """Brânquia de axolote: haste rosa grossa (lê de 3/4) com filamentos em degrau magenta/rosa na beirada de
    cima e um tufo na ponta. Osso externo sem rotação (é ele que balança na animação); o interno dá a direção."""
    x, y, z = raiz
    s = lado
    pcs = []
    def bx(a, b): return sorted((x + a * s, x + b * s))
    x0, x1 = bx(-1.0, L * 0.62)
    pcs.append(peca(nome + "_haste", [x0, y - 1.3, z - 1.25], [x1, y + 1.3, z + 1.25], mat_pena(ROSA_CLARO, ROSA, 0, s < 0)))
    x0, x1 = bx(L * 0.6, L)
    pcs.append(peca(nome + "_ponta", [x0, y - 1.1, z - 1.05], [x1, y + 1.1, z + 1.05], mat_pena(ROSA, ROSA_FORTE, 0, s < 0)))
    passo = (L - 1.6) / n
    for k in range(n):                             # franja densa de filamentos magenta na beirada de cima/trás
        cx = x + (0.8 + passo * (k + 0.5)) * s
        h = (1.8 if k % 2 == 0 else 1.25) - 0.05 * k
        cores = (ROSA_FORTE, MAGENTA) if k % 2 == 0 else (MAGENTA, MAGENTA_ESC)
        x0, x1 = sorted((cx - passo * 0.55 * s, cx + passo * 0.55 * s))
        pcs.append(peca(f"{nome}_f{k}", [x0, y + 1.0, z - 1.1], [x1, y + 1.1 + h, z + 1.25],
                        mat_pena(*cores, 1, False), rot=(0, 0, -14 * s), pivo=(cx, y + 1.1, z)))
    # ponta magenta: dois filamentos abrindo em V
    for k, (ang, cores) in enumerate(((-34, (ROSA_FORTE, MAGENTA)), (22, (MAGENTA, MAGENTA_ESC)))):
        x0, x1 = bx(L - 0.6, L + 1.8)
        pcs.append(peca(f"{nome}_tufo{k}", [x0, y - 0.7, z - 0.9], [x1, y + 0.7, z + 0.9],
                        mat_pena(*cores, 0, s < 0), rot=(0, 0, -ang * s), pivo=(x + (L - 0.6) * s, y, z)))
    dentro = osso(nome + "_dir", list(raiz), [0, -recuo * s, eleva * s], pcs)
    return osso(nome, list(raiz), [0, 0, 0], [dentro])

GUELRAS = [  # (y da raiz, z da raiz, comprimento, recuo (graus para trás), elevação (graus para cima))
    (30.2, -5.8, 9.0, 39, 35),
    (27.7, -5.4, 9.6, 34, 12),
    (25.2, -5.6, 8.6, 50, -20),
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
ONDAS = [("cauda_p0", 6, (3, 0, 0)), ("cauda_p1", 6, (3, 0, 0)), ("cauda_p2", 6, (2, 0, 0))]


# ---------------- cauda ----------------
def pena_cauda(nome, base, segs, rot0, curva, mat_fn, sobrepoe=1.0):
    """Como g.pena_curva (eixo 'y'), mas cada segmento começa 'sobrepoe' antes do fim do anterior: na curva
    forte das foices largas não abre fresta entre os segmentos. Ossos '<nome>_0', '<nome>_1'..."""
    def seg(k, pos):
        L, w, h, c0, c1 = segs[k]
        px, py, pz = pos
        filhos = [peca(f"{nome}_{k}", [px - w / 2, py, pz - h / 2], [px + w / 2, py + L, pz + h / 2], mat_fn(c0, c1, 1, False))]
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py + L - sobrepoe, pz)))
        cv = curva[k - 1] if isinstance(curva[0], (list, tuple)) else curva
        return osso(f"{nome}_{k}", list(pos), list(rot0) if k == 0 else list(cv), filhos)
    return seg(0, tuple(base))


def montar():
    # ================= cabeça: mais larga que funda, quinas em degrau, alto arredondado =================
    cab = []
    mc = mat_cor(cor_cabeca, borda=.02, curva=.3)
    cab += camada_cabeca("bochecha", 22.4, 23.7, 0.2, CAB_ZT - 0.4, mc)
    cab += camada_cabeca("cranio", 23.6, 29.8, 0.0, CAB_ZT, mc, olhos=True)
    cab += camada_cabeca("domo1", 29.7, 31.1, 0.6, CAB_ZT - 0.5, mc)
    cab += camada_cabeca("domo2", 31.0, 32.0, 1.4, CAB_ZT - 1.2, mc)
    cab += camada_cabeca("domo3", 31.9, 32.6, 2.5, CAB_ZT - 2.2, mc)
    # bico: cunha amarela que avança e afina (~1/3 da fundura da cabeça), ponta um pouco para baixo
    mb = mat_cor(cor_bico, borda=.05, curva=.3, grao=.02)
    cab.append(peca("bico_base", [-1.9, 23.4, CAB_ZF - 2.2], [1.9, 26.2, CAB_ZF + 0.3], mb, faixa=(23.0, 26.4)))
    cab.append(peca("bico_ponta", [-1.25, 23.6, CAB_ZF - 4.1], [1.25, 25.7, CAB_ZF - 2.1], mb, rot=(-13, 0, 0),
                    pivo=(0, 25.7, CAB_ZF - 2.1), faixa=(23.0, 26.4)))
    # barbela: dois lóbulos vermelhos presos na garganta, quase da largura do bico, ~1,5x a altura dele
    mbar = mat_cor(lambda p, f: VERMELHO_ESC if (f == "north" and abs(p[0]) < 0.18 and p[1] < 22.2)
                   else mix(VERMELHO, VERMELHO_ESC, clamp((21.4 - p[1]) / 3.6)), borda=.12, curva=.3, grao=.02)
    cab.append(peca("barbela", [-2.0, 19.8, CAB_ZF - 1.1], [2.0, 23.5, CAB_ZF + 1.0], mbar, faixa=(17.5, 23.5)))
    for lado in (-1, 1):
        x0, x1 = sorted((0.15 * lado, 1.85 * lado))
        cab.append(peca("barbela_lobo_" + ("d" if lado < 0 else "e"), [x0, 18.1, CAB_ZF - 0.95], [x1, 20.0, CAB_ZF + 0.85], mbar, faixa=(17.5, 23.5)))
    # crista aquática: blocos magenta em degraus que nascem do alto arredondado da cabeça
    mcr = mat_cor(lambda p, f: mix(MAGENTA_ESC, MAGENTA, clamp((p[1] - 32.0) / 3.5)) if f != "up" else mix(MAGENTA, ROSA_FORTE, .3),
                  borda=.12, curva=.25, grao=.03)
    crista = []
    for k, (z0, z1, w, h, y0) in enumerate([(-13.4, -10.4, 1.9, 4.4, 31.4), (-11.0, -7.4, 2.3, 7.0, 31.8), (-8.0, -4.8, 2.2, 7.4, 31.8), (-5.4, -2.8, 1.7, 4.8, 31.0)]):
        crista.append(peca(f"crista_{k}", [-w, y0, z0], [w, y0 + h, z1], mcr, faixa=(32.0, 39.2)))
    for lado in (-1, 1):
        x0, x1 = sorted((1.6 * lado, 3.0 * lado))
        crista.append(peca("crista_lado_" + ("d" if lado < 0 else "e"), [x0, 31.8, -11.4], [x1, 34.8, -5.6], mcr, faixa=(32.0, 39.2)))
    cab.append(osso("crista", [0, 32.5, -8], [0, 0, 0], crista))
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        for k, (y0, z0, L, rec, ele) in enumerate(GUELRAS):
            cab.append(guelra(f"guelra_{s_}_{k}", (6.9 * lado, y0, z0), lado, L, rec, ele))
    cabeca = osso("cabeca", [0, 23, -9], [0, 0, 0], cab)

    # ================= pescoço (garganta creme) =================
    pescoco = osso("pescoco", [0, 20, -8], [0, 0, 0], [
        peca("pescoco", [-5.0, 16.0, -11.4], [5.0, 23.6, -4.6], mat_cor(cor_corpo, curva=.25), faixa=(7, 24), res=4)]
        # papo: o volume creme do peito sobe até encostar na cabeça
        + arredondado("papo", [-5.2, 15.8, -14.0], [5.2, 22.6, -6.0], mat_cor(cor_peito, borda=.03, curva=.2), r=1.3, faixa=(7, 24), res=4)
        + [cabeca])

    # ================= tronco em ovo, inclinado ~15° (peito baixo e para a frente, costas subindo para a cauda) =================
    tronco = []
    mt = mat_cor(cor_corpo, borda=.03, curva=.45)
    tronco += arredondado2("tronco", [-8.6, 8.6, -10.4], [8.6, 22.0, 9.8], mt, r=3.2, faixa=(7.0, 22.9), res=4)
    tronco += arredondado("barriga", [-6.0, 7.0, -7.4], [6.0, 10.4, 6.2], mt, r=1.4, faixa=(7.0, 22.9), res=4)
    # peito: um só volume arredondado avançando para a frente, com escamas em U pintadas
    tronco += arredondado2("peito", [-5.8, 10.4, -12.8], [5.8, 21.4, -5.0], mat_cor(cor_peito, borda=.03, curva=.25), r=2.0,
                           faixa=(7.0, 22.9), res=4)
    tronco += arredondado("rabadilha", [-4.8, 14.2, 7.6], [4.8, 21.0, 11.4], mt, r=1.4, faixa=(7.0, 22.9), res=4)
    corpo = [osso("tronco", [0, 15, 0], [-15, 0, 0], tronco)]

    # ================= asas com a espiral azul =================
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        fora = "east" if lado > 0 else "west"
        def cor_asa(p, face, fora=fora):
            x, y, z = p
            if face == fora and abs(x) > 9.9 and espiral(z + 1.8, y - 15.5): return mix(AZUL, AZUL_ROYAL, clamp((17 - y) / 7))
            return mix(ROSA, ROSA_CLARO, clamp((y - 11) / 8) * .75)
        ma = mat_cor(cor_asa, borda=.05, curva=.35)
        asa = []
        def caixa(nome, xa, xb, de, ate):
            x0, x1 = sorted((xa * lado, xb * lado))
            asa.append(peca(nome + "_" + s_, [x0, de[0], de[1]], [x1, ate[0], ate[1]], ma, faixa=(10.4, 21.0), res=4))
        caixa("asa_meio", 7.4, 10.0, (11.4, -7.6), (19.6, 4.0))
        caixa("asa_ombro", 7.4, 9.8, (13.0, -9.2), (21.0, -3.0))          # frente alta e curva
        caixa("asa_ombro2", 7.4, 9.5, (20.8, -7.8), (21.8, -4.4))
        caixa("asa_ombro3", 7.4, 9.5, (14.0, -10.0), (19.8, -9.0))
        caixa("asa_baixo", 7.4, 9.6, (10.4, -6.4), (11.6, 3.0))
        # 3 fileiras de pontas de pena sobrepostas apontando para a cauda (ponta em degrau, voxel)
        for k, (y0, y1, z0, z1, xa, xb) in enumerate([(16.2, 19.4, 2.6, 10.0, 7.8, 9.7), (13.6, 16.8, 2.6, 8.6, 8.0, 9.85),
                                                      (11.2, 14.0, 2.0, 6.8, 8.2, 10.0)]):
            mr = mat_pena(ROSA, ROSA_CLARO, 2, False)
            x0, x1 = sorted((xa * lado, xb * lado))
            asa.append(peca(f"pena_fila{k}_{s_}", [x0, y0, z0], [x1, y1, z1], mr))
            asa.append(peca(f"pena_ponta{k}_{s_}", [x0 + 0.1, y0 + 0.6, z1 - 0.1], [x1 - 0.1, y1 - 0.6, z1 + 1.6], mr))
        corpo.append(osso("asa_" + s_, [8.6 * lado, 19.0, -2.0], [0, 0, 0], [osso("asa_incl_" + s_, [0, 15, 0], [-7, 0, 0], asa)]))

    # ================= cauda: foices azuis nascidas de um ponto alto nas costas =================
    FOICES = [  # (x, rx inicial, curva por segmento, comprimentos, cores (raiz, ponta))
        (0.0, -4, 19, (4.4, 4.4, 4.2, 4.0, 3.8, 3.6), (AZUL_ROYAL, AZUL)),
        (0.5, 18, 18, (4.0, 4.0, 3.8, 3.6, 3.4, 3.2), (AZUL_ROYAL, AZUL_CLARO)),
        (-0.5, 40, 16, (3.8, 3.8, 3.6, 3.4, 3.2, 3.0), (AZUL, AZUL_CLARO)),
        (0.6, 62, 14, (3.6, 3.6, 3.4, 3.2, 3.0, 2.8), (AZUL, AZUL_CEU)),
        (-0.6, 84, 12, (3.4, 3.4, 3.2, 3.0, 2.8, 2.6), (AZUL_CLARO, AZUL_CEU)),
        (0.0, 104, 10, (3.2, 3.2, 3.0, 2.8, 2.6, 2.4), (AZUL_CLARO, AZUL_CEU)),
    ]
    cauda = []
    BASE = (0.0, 18.8, 7.6)
    for k, (x, rx0, cv, Ls, (c0, c1)) in enumerate(FOICES):
        n = len(Ls)
        segs = [(L, 2.3 - 0.15 * i, 5.0 - 0.55 * i, mix(c0, c1, i / n), mix(c0, c1, (i + 1) / n)) for i, L in enumerate(Ls)]
        cauda.append(pena_cauda(f"cauda_p{k}", (BASE[0] + x, BASE[1], BASE[2]), segs, (rx0, 0, 0), (cv, 0, 0), mat_foice, sobrepoe=0.8))
    corpo.append(osso("cauda", list(BASE), [0, 0, 0], cauda))

    corpo.append(pescoco)
    raiz = osso("corpo", [0, 10, 0], [0, 0, 0], corpo)

    # ================= pernas e patas anfíbias =================
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 4.8 * lado; zc = -1.0
        pp = []
        ml = mat_cor(lambda p, f: AMARELO, borda=.08, curva=.35, grao=.02)
        pp.append(peca("perna_" + s, [xc - 2.0, 2.2, zc - 2.0], [xc + 2.0, 9.5, zc + 2.0], ml, faixa=(0, 9.5)))
        pp.append(peca("pe_" + s, [xc - 3.0, 0.6, zc - 3.8], [xc + 3.0, 2.8, zc + 2.2], ml, faixa=(0, 9.5)))
        mg = mat_cor(lambda p, f: CINZA_CLARO if f == "up" else CINZA, borda=.18, curva=.5, grao=.02)
        for k, dx in enumerate((-2.05, 0.0, 2.05)):
            pp.append(peca(f"garra_{k}_{s}", [xc + dx - 0.9, 0.0, zc - 6.4], [xc + dx + 0.9, 2.2, zc - 3.2], mg, faixa=(0, 2.2)))
        pp.append(peca("garra_tras_" + s, [xc - 0.9, 0.0, zc + 1.8], [xc + 0.9, 1.8, zc + 4.0], mg, faixa=(0, 2.2)))
        return osso("perna_" + s, [xc, 9.0, zc], [0, 0, 0], pp)

    return [raiz, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

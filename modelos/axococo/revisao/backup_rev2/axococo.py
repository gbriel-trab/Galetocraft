"""Axococó (#008, Água): o galo-axolote das águas, rosa-claro, com brânquias de axolote em sol, asas com
espiral azul e um leque de foices azuis na cauda (do azul-royal ao azul-céu)."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, clamp, contexto_luz

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

def mat_escama_peito(y0, y1, dente=1.8, fundo=0.7):
    """Camada de penas do peito: creme, mais clara em cima; a beirada de baixo da face da frente tem as pontas
    de pena em degrau (sombra nos vãos), como as escamas em degrau da ficha."""
    def cor(p, face):
        x, y, z = p
        c = mix(CREME, ROSA_PALIDO, clamp((y1 - y) / (y1 - y0)) * .35)
        if face == "north":
            u = ((x + dente / 2) % dente) / dente
            f = y0 + fundo * math.floor(abs(u - 0.5) * 2 * 2.999) / 2
            if y < f: return tom(c, -.28)
            if y - f < 0.25: return tom(c, -.12)
        return c
    return mat_cor(cor, borda=.10, curva=.25)


# ---------------- espiral da asa ----------------
def espiral(a, b, passo=1.8, larg=1.2, voltas=1.75, r0=0.0):
    """Espiral azul da 'Plumagem Úmida' (quadradinha), com a cauda que sai por baixo para a frente.
    a = horizontal (positivo = para trás), b = vertical. Devolve True dentro da faixa azul."""
    a = a / 1.3
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
OLHO_Y = 26.4

def cor_cabeca(p, face):
    x, y, z = p
    base = ROSA_CLARO
    if z < -10.5 and y < 25.0: base = mix(ROSA_CLARO, ROSA_PALIDO, clamp((25.0 - y) / 2.2))   # bochecha clara
    if face == "up": base = mix(ROSA_CLARO, ROSA_PALIDO, .25)
    return base

def olho(u, v):
    """Olho neutro (u ao longo da face, negativo = para o bico; v para cima): mais largo que alto, esclera
    branca, contorno e íris azuis, pupila preta puxada para o bico, pálpebra de cima reta e inclinada
    cobrindo ~30% (olhar calmo e firme). Acima da pálpebra, a faixa da sobrancelha magenta descendo para o bico."""
    ru, rv = 2.35, 1.62
    lid = rv * (0.50 + 0.20 * u / ru)                      # linha da pálpebra (desce para o bico)
    e = (u / ru) ** 2 + (v / rv) ** 2
    if abs(u) < ru * 1.12 and lid <= v < lid + 0.62 and v < rv + 0.7: return "sobrancelha"
    if e > 1 or v >= lid: return None
    if lid - v < 0.18: return tom(ROSA_FORTE, -.25)        # borda da pálpebra
    iu, iv = u + 0.62, v + 0.02                            # íris deslocada para o bico
    di = (iu / 1.02) ** 2 + (iv / 1.12) ** 2
    if ((iu - 0.25) / 0.2) ** 2 + ((iv - 0.32) / 0.22) ** 2 <= 1: return (255, 255, 255)   # brilho
    if ((iu + 0.12) / 0.5) ** 2 + (iv / 0.62) ** 2 <= 1: return PRETO                    # pupila
    if di <= 1: return mix(AZUL_ROYAL, AZUL_CLARO, clamp((iv + .8) / 1.6))               # íris azul
    if e > 0.80: return mix(AZUL_ROYAL, AZUL, clamp(v / rv + .5))                       # contorno azul
    return mix(BRANCO, (222, 224, 238), clamp(-v / rv))

def mat_faceta_olho(fora, cz):
    base = mat_cor(cor_cabeca, borda=.02, curva=.3)
    def f(c):
        if c["face"] == fora:
            x, y, z = c["p"]
            r = olho(z - cz, y - OLHO_Y)
            if r == "sobrancelha":
                return mix(MAGENTA, ROSA_FORTE, clamp((y - OLHO_Y - 0.5) / 1.2))
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
                        m, rot=(0, 45 * lado, 0), pivo=(pcx, (y0 + y1) / 2, pcz), faixa=(20.5, 33.0), res=8 if olhos else res))
    return pcs

def cor_bico(p, face):
    x, y, z = p
    if face in ("east", "west") and abs(z + 16.6) < 0.35 and abs(y - 24.9) < 0.3: return (150, 84, 20)   # narina
    if face == "up": return AMARELO_CLARO
    if 23.15 < y < 23.45 and face != "down": return (196, 104, 18)                       # linha da boca
    if y < 23.3: return LARANJA
    return mix(AMARELO_CLARO, AMARELO, clamp((25.6 - y) / 1.6))


# ---------------- brânquias ----------------
def guelra(nome, raiz, lado, L, recuo, eleva, n=6):
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
    passo = (L - 2.0) / n
    for k in range(n):                             # filamentos em degrau na beirada de cima
        cx = x + (1.0 + passo * (k + 0.5)) * s
        h = (1.9 if k % 2 == 0 else 1.2) - 0.06 * k
        cores = (ROSA_FORTE, MAGENTA) if k % 2 == 0 else (ROSA, ROSA_FORTE)
        x0, x1 = sorted((cx - passo / 2 * s, cx + passo / 2 * s))
        pcs.append(peca(f"{nome}_f{k}", [x0, y + 1.0, z - 1.0], [x1, y + 1.1 + h, z + 1.0],
                        mat_pena(*cores, 1, False), rot=(0, 0, -10 * s), pivo=(cx, y + 1.1, z)))
    for k in range(n // 2):                        # franja curta de baixo, rosa
        cx = x + (1.6 + 2 * passo * (k + 0.5)) * s
        x0, x1 = sorted((cx - passo / 2 * s, cx + passo / 2 * s))
        pcs.append(peca(f"{nome}_b{k}", [x0, y - 2.2, z - 0.9], [x1, y - 1.2, z + 0.9], mat_pena(ROSA_CLARO, ROSA, 1, True)))
    # tufo da ponta: dois filamentos abrindo em V
    for k, (ang, cores) in enumerate(((-38, (ROSA_FORTE, MAGENTA)), (24, (ROSA, ROSA_FORTE)))):
        x0, x1 = bx(L - 0.6, L + 1.9)
        pcs.append(peca(f"{nome}_tufo{k}", [x0, y - 0.65, z - 0.85], [x1, y + 0.65, z + 0.85],
                        mat_pena(*cores, 0, s < 0), rot=(0, 0, -ang * s), pivo=(x + (L - 0.6) * s, y, z)))
    dentro = osso(nome + "_dir", list(raiz), [0, -recuo * s, eleva * s], pcs)
    return osso(nome, list(raiz), [0, 0, 0], [dentro])

GUELRAS = [  # (y da raiz, z da raiz, comprimento, recuo (graus para trás), elevação (graus para cima))
    (30.6, -7.4, 8.8, 30, 34),
    (27.6, -7.0, 9.4, 34, 2),
    (24.6, -7.0, 8.4, 44, -21),
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
ONDAS = [("cauda_p0", 4, (4, 0, 0)), ("cauda_p1", 4, (3, 0, 0)), ("cauda_p2", 4, (3, 0, 0))]


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
    cab += camada_cabeca("queixo", 20.9, 22.5, 1.0, CAB_ZT - 0.8, mc)
    cab += camada_cabeca("cranio", 22.4, 31.0, 0.0, CAB_ZT, mc, olhos=True)
    cab += camada_cabeca("topo", 30.9, 32.1, 1.1, CAB_ZT - 0.6, mc)
    cab.append(peca("topo_alto", [-4.6, 32.0, -12.8], [4.6, 32.7, -6.6], mc, faixa=(20.5, 33.0), res=4))
    # bico: cunha curta (base larga + ponta mais estreita, um pouco para baixo)
    mb = mat_cor(cor_bico, borda=.05, curva=.3, grao=.02)
    cab.append(peca("bico_base", [-2.4, 22.6, CAB_ZF - 2.0], [2.4, 25.8, CAB_ZF + 0.3], mb, faixa=(22.0, 26.0)))
    cab.append(peca("bico_ponta", [-1.7, 22.7, CAB_ZF - 3.9], [1.7, 25.2, CAB_ZF - 1.9], mb, rot=(-12, 0, 0),
                    pivo=(0, 25.2, CAB_ZF - 1.9), faixa=(22.0, 26.0)))
    # barbela: dois lóbulos vermelhos presos na garganta, quase da largura do bico, ~1,5x a altura dele
    mbar = mat_cor(lambda p, f: VERMELHO_ESC if (f == "north" and abs(p[0]) < 0.18 and p[1] < 21.6)
                   else mix(VERMELHO, VERMELHO_ESC, clamp((20.6 - p[1]) / 3.6)), borda=.12, curva=.3, grao=.02)
    cab.append(peca("barbela", [-2.2, 19.4, CAB_ZF - 1.0], [2.2, 22.7, CAB_ZF + 1.2], mbar, faixa=(17.0, 22.7)))
    for lado in (-1, 1):
        x0, x1 = sorted((0.15 * lado, 2.0 * lado))
        cab.append(peca("barbela_lobo_" + ("d" if lado < 0 else "e"), [x0, 17.6, CAB_ZF - 0.85], [x1, 19.6, CAB_ZF + 1.05], mbar, faixa=(17.0, 22.7)))
    # crista aquática: blocos magenta em degraus que nascem do alto arredondado da cabeça
    mcr = mat_cor(lambda p, f: mix(MAGENTA_ESC, MAGENTA, clamp((p[1] - 32.0) / 3.5)) if f != "up" else mix(MAGENTA, ROSA_FORTE, .3),
                  borda=.12, curva=.25, grao=.03)
    crista = []
    for k, (z0, z1, w, h) in enumerate([(-14.0, -10.6, 2.0, 4.2), (-11.0, -7.4, 2.4, 6.6), (-8.0, -4.6, 2.3, 7.2), (-5.0, -2.2, 1.8, 4.8)]):
        crista.append(peca(f"crista_{k}", [-w, 32.0, z0], [w, 32.0 + h, z1], mcr, faixa=(32.0, 39.2)))
    for lado in (-1, 1):
        x0, x1 = sorted((1.8 * lado, 3.6 * lado))
        crista.append(peca("crista_lado_" + ("d" if lado < 0 else "e"), [x0, 32.0, -12.2], [x1, 35.0, -5.0], mcr, faixa=(32.0, 39.2)))
    cab.append(osso("crista", [0, 32.5, -8], [0, 0, 0], crista))
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        for k, (y0, z0, L, rec, ele) in enumerate(GUELRAS):
            cab.append(guelra(f"guelra_{s_}_{k}", (7.0 * lado, y0, z0), lado, L, rec, ele))
    cabeca = osso("cabeca", [0, 23, -9], [0, 0, 0], cab)

    # ================= pescoço (garganta creme) =================
    pescoco = osso("pescoco", [0, 20, -8], [0, 0, 0], [
        peca("pescoco_a", [-3.3, 16.0, -13.2], [3.3, 23.0, -5.0], mat_cor(cor_corpo, curva=.25), faixa=(7, 24), res=4),
        # papo: o peito creme sobe até encostar na cabeça (sem 'pescoço de pau' entre os dois)
        peca("papo", [-4.6, 16.6, -14.2], [4.6, 21.1, -7.0], mat_escama_peito(16.6, 21.1), faixa=(7, 24), res=4),
        peca("papo_lados", [-5.8, 16.4, -13.0], [5.8, 20.9, -7.0], mat_escama_peito(16.4, 20.9), faixa=(7, 24), res=4),
        peca("pescoco_b", [-5.0, 16.0, -11.4], [5.0, 23.0, -4.6], mat_cor(cor_corpo, curva=.25), faixa=(7, 24), res=4),
        cabeca])

    # ================= tronco em ovo, inclinado ~15° (peito baixo e para a frente, costas subindo para a cauda) =================
    tronco = []
    mt = mat_cor(cor_corpo, borda=.03, curva=.45)
    CAMADAS = [  # fatias horizontais: (y0, y1, meia largura, z da frente, z de trás, chanfro das quinas)
        (7.0, 9.0, 4.8, -6.0, 5.0, 1.6),
        (8.8, 10.8, 6.8, -8.8, 7.6, 2.2),
        (10.6, 12.8, 8.0, -10.4, 9.0, 2.6),
        (12.6, 17.6, 8.6, -11.2, 9.8, 2.8),
        (17.4, 19.8, 8.0, -10.8, 9.0, 2.6),
        (19.6, 21.6, 6.8, -9.6, 7.8, 2.2),
        (21.4, 22.9, 4.8, -7.8, 5.6, 1.6),
    ]
    for k, (y0, y1, w, zf, zb, r) in enumerate(CAMADAS):
        tronco.append(peca(f"tronco_{k}_a", [-w + r, y0, zf], [w - r, y1, zb], mt, faixa=(7.0, 22.9), res=4))
        tronco.append(peca(f"tronco_{k}_b", [-w, y0, zf + r], [w, y1, zb - r], mt, faixa=(7.0, 22.9), res=4))
        h = r / 2
        tronco.append(peca(f"tronco_{k}_c", [-w + h, y0, zf + h], [w - h, y1, zb - h], mt, faixa=(7.0, 22.9), res=4))
    # peito creme saltando para a frente em 4 camadas de escama, cada uma um pouco à frente da de baixo
    for k, (y0, y1, w, zf) in enumerate([(18.6, 21.4, 5.4, -12.5), (16.0, 18.8, 5.2, -12.0), (13.4, 16.2, 4.6, -11.5), (10.8, 13.6, 3.8, -10.9)]):
        tronco.append(peca(f"peito_{k}", [-w, y0, zf], [w, y1, zf + 4.0], mat_escama_peito(y0, y1), faixa=(7.0, 22.9), res=4))
    tronco.append(peca("rabadilha", [-4.6, 15.0, 8.6], [4.6, 21.0, 11.2], mt, faixa=(7.0, 22.9), res=4))
    corpo = [osso("tronco", [0, 15, 0], [-15, 0, 0], tronco)]

    # ================= asas com a espiral azul =================
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        fora = "east" if lado > 0 else "west"
        def cor_asa(p, face, fora=fora):
            x, y, z = p
            if face == fora and abs(x) > 10.5 and espiral(z + 0.6, y - 15.0): return mix(AZUL, AZUL_ROYAL, clamp((17 - y) / 7))
            return mix(ROSA, ROSA_CLARO, clamp((y - 11) / 8) * .75)
        ma = mat_cor(cor_asa, borda=.05, curva=.35)
        asa = []
        def caixa(nome, xa, xb, de, ate):
            x0, x1 = sorted((xa * lado, xb * lado))
            asa.append(peca(nome + "_" + s_, [x0, de[0], de[1]], [x1, ate[0], ate[1]], ma, faixa=(10.4, 21.0), res=4))
        caixa("asa_meio", 7.6, 10.6, (11.2, -8.0), (19.6, 5.6))
        caixa("asa_frente", 7.6, 10.2, (12.2, -9.2), (18.6, -7.8))
        caixa("asa_cima", 7.6, 10.0, (19.4, -7.4), (20.8, 5.0))
        caixa("asa_baixo", 7.6, 10.0, (10.2, -7.0), (11.4, 4.4))
        # coberteiras: fileira sobreposta no alto da asa, beirada de baixo em degraus
        def cor_cob(p, face, fora=fora):
            x, y, z = p
            u = ((z + 1.2) % 2.4) / 2.4
            fundo = 18.3 + 1.2 * math.floor(abs(u - 0.5) * 2 * 3.999) / 3
            if y < fundo: return None
            if face == fora and y - fundo < 0.3: return tom(ROSA, -.25)
            return mix(ROSA, ROSA_CLARO, clamp((y - 18.3) / 3.0))
        x0, x1 = sorted((10.35 * lado, 11.0 * lado))
        asa.append(peca("coberteira_" + s_, [x0, 18.3, -7.8], [x1, 21.1, 4.6], mat_cor(cor_cob, borda=.04, curva=.2), res=4))
        # rêmiges: penas em degrau que saem para trás; as de cima mais compridas (a ponta da asa sobe para a cauda)
        for k, (y0, z0, L, H, rx) in enumerate([(20.4, 3.4, 8.6, 2.8, -10), (17.9, 3.8, 7.6, 2.8, -5), (15.4, 3.6, 6.2, 2.8, 1), (12.9, 2.8, 4.8, 2.6, 7)]):
            x0, x1 = sorted(((8.0 + 0.15 * k) * lado, (9.8 + 0.15 * k) * lado))
            asa.append(osso(f"remige_{k}_{s_}", [x0, y0, z0], [rx, 0, 0], [
                peca(f"remige_{k}_{s_}", [x0, y0 - H, z0], [x1, y0, z0 + L], mat_pena(ROSA, ROSA_CLARO, 2, False))]))
        corpo.append(osso("asa_" + s_, [8.6 * lado, 19.0, -2.0], [0, 0, 0], [osso("asa_incl_" + s_, [0, 15, 0], [-7, 0, 0], asa)]))

    # ================= cauda: foices azuis nascidas de um ponto alto nas costas =================
    FOICES = [  # (x, ry abertura, rx inicial, curvas, comprimentos, espessura, largura, cores (raiz, ponta))
        (0.0, 0, 22, (24, 34, 44), (7.4, 7.0, 6.4, 5.6), 3.4, 5.8, (AZUL_ROYAL, AZUL)),
        (1.3, 12, 42, (22, 30, 36), (6.4, 6.2, 5.6, 4.8), 2.9, 5.0, (AZUL, AZUL_CLARO)),
        (-1.3, -12, 42, (22, 30, 36), (6.4, 6.2, 5.6, 4.8), 2.9, 5.0, (AZUL, AZUL_CLARO)),
        (2.0, 24, 62, (20, 26, 30), (5.4, 5.2, 4.6, 4.0), 2.5, 4.4, (AZUL_CLARO, AZUL_CEU)),
        (-2.0, -24, 62, (20, 26, 30), (5.4, 5.2, 4.6, 4.0), 2.5, 4.4, (AZUL_CLARO, AZUL_CEU)),
    ]
    cauda = []
    BASE = (0.0, 20.6, 6.0)
    for k, (x, ry, rx0, cv, Ls, w, h, (c0, c1)) in enumerate(FOICES):
        n = len(Ls)
        segs = [(L + 1.1, w - 0.3 * i, h - 0.55 * i, mix(c0, c1, i / n), mix(c0, c1, (i + 1) / n)) for i, L in enumerate(Ls)]
        cauda.append(pena_cauda(f"cauda_p{k}", (BASE[0] + x, BASE[1], BASE[2]), segs, (rx0, ry, 0), [(a, 0, 0) for a in cv], mat_foice, sobrepoe=1.1))
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

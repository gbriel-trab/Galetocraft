"""Axococó (#008, Água): o galo-axolote das águas. Cabeça grande em bloco rosa-claro com olhos bravos de aro azul,
bico amarelo largo e barbela em dois lóbulos; três brânquias de axolote em degrau de cada lado; crista aquática
magenta em blocos; corpo em ovo deitado com peito creme em fileiras de penas; asas com a espiral azul quadrada da
'Plumagem Úmida'; leque de foices azuis grossas na cauda; pernas amarelas e patas anfíbias de dedos roxo-cinza.
Refeito do zero (rodadas n*) seguindo as 4 vistas da ficha: blocos grossos, 2-3 tons chapados por bloco."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, clamp

ID = "axococo"; NOME = "Axococó"; NUMERO = 8
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 26.5, -12), 10)

# ---------------- paleta (Paleta de Cores da ficha) ----------------
CREME = (255, 234, 220)
CREME_SOMBRA = (240, 204, 196)
ROSA_PALIDO = (252, 208, 220)
ROSA_CLARO = (252, 178, 206)
ROSA = (248, 122, 156)
ROSA_FORTE = (244, 86, 132)
MAGENTA = (228, 48, 104)
MAGENTA_ESC = (182, 26, 80)
AZUL_CEU = (96, 190, 248)
AZUL_CLARO = (62, 150, 236)
AZUL = (40, 100, 200)
AZUL_ROYAL = (12, 60, 166)
AMARELO = (252, 182, 18)
AMARELO_CLARO = (255, 214, 84)
LARANJA = (234, 132, 16)
VERMELHO = (220, 30, 58)
VERMELHO_ESC = (160, 14, 44)
ROXO = (98, 82, 112)
ROXO_CLARO = (132, 116, 146)
BRANCO = (252, 250, 248); PRETO = (20, 12, 22)
IRIS = (186, 128, 26)


# ---------------- luz em 2-3 tons chapados (claro em cima, base, sombra embaixo) ----------------
def tom(c, f):
    """Como g.tom, mas a sombra puxa para um tom mais fundo da MESMA cor (o rosa não vira malva/cinza)."""
    f = clamp(f, -1, 1)
    if f >= 0: return mix(c, (255, 250, 244), f * .42)
    return mix(c, (int(c[0] * .78), int(c[1] * .50), int(c[2] * .66)), -f * .9)

def luz3(c, borda=.10, cima=.20, baixo=-.36, alto=.06, fundo=-.14, faixa=None):
    """Luz chapada: face de cima clara, de baixo escura; nas faces dos lados, faixa de cima um tom mais claro e
    faixa de baixo um tom mais escuro (pela altura do bloco, ou da 'faixa' do grupo); fio escuro na borda."""
    f = c["face"]
    if f == "up": l = cima
    elif f == "down": l = baixo
    else:
        y0, y1 = faixa or (c["b"][0][1], c["b"][1][1])
        t = (c["p"][1] - y0) / max(y1 - y0, 1e-6)
        l = alto if t > .74 else fundo if t < .26 else 0.0
    if g.na_borda(c): l -= borda
    return l

def mat_bloco(cor_fn, **kw):
    """cor_fn(p, face) -> cor base (ou None); aplica a luz chapada."""
    def f(c):
        base = cor_fn(c["p"], c["face"])
        return None if base is None else tom(base, luz3(c, **kw))
    return f

def mat_liso(cor, **kw): return mat_bloco(lambda p, f: cor, **kw)

def mat_degrade(c0, c1, eixo, inverte=False, borda=.14):
    """Bloco de pena com degradê c0 -> c1 no comprimento (em 3 degraus, sem ruído), face de cima clara."""
    def f(c):
        lo, hi = c["b"][0][eixo], c["b"][1][eixo]
        t = clamp((c["p"][eixo] - lo) / max(hi - lo, 1e-6))
        if inverte: t = 1 - t
        t = round(t * 2) / 2
        l = .04
        if c["face"] == "up": l += .18
        if c["face"] == "down": l -= .32
        if g.na_borda(c): l -= borda
        return tom(mix(c0, c1, t), l)
    return f

def no_mundo(mat, ry, pivo):
    """Pinta uma peça girada em y com as coordenadas do MUNDO (a pintura normal usa as da peça sem girar)."""
    a = math.radians(ry); ca, sa = math.cos(a), math.sin(a)
    def f(c):
        x, y, z = (c["p"][i] - pivo[i] for i in range(3))
        c = dict(c); c["p"] = (pivo[0] + x * ca + z * sa, c["p"][1], pivo[2] - x * sa + z * ca)
        return mat(c)
    return f

def caixa(nome, de, ate, mat, **kw): return peca(nome, list(de), list(ate), mat, **kw)

def xs(lado, a, b):
    """Intervalo em x espelhado pelo lado (lado -1 = direita = x negativo)."""
    return sorted((a * lado, b * lado))


# ================= cabeça =================
CAB_X = 8.0          # meia largura da cabeça
CAB_ZF = -14.8       # frente do rosto
FRENTE_X = 3.4       # meia largura da frente reta (onde nasce o bico)
CAB_ZT = -3.8        # nuca
FAC_T = 1.8          # espessura das peças diagonais
OLHO_Y = 26.4        # centro do olho (na altura do alto do bico, como na ficha)
FAIXA_CAB = (20.6, 32.2)

def cor_cabeca(p, face):
    """Rosa-claro; bochecha e garganta mais claras (quase creme) embaixo do olho."""
    x, y, z = p
    if face == "up": return ROSA_CLARO
    if y < 24.2 and z < -6.8: return mix(ROSA_CLARO, ROSA_PALIDO, .85) if y > 22.4 else CREME
    return ROSA_CLARO

def olho(u, v):
    """Olho neutro da ficha (u ao longo da face, negativo = para o bico; v para cima):
    - pálpebra rosa cortando o alto do olho numa linha reta que desce para o bico (olhar bravo);
    - branco do olho quase retangular, pupila preta grande encostada no lado do bico, anel dourado e brilho;
    - mancha azul em volta, larga atrás e embaixo (como uma sombra de olho), fina do lado do bico."""
    ru, rv = 2.5, 1.75
    lid = 0.85 + 0.30 * u                                   # linha da pálpebra
    if v >= lid: return None
    q = abs((u + 0.1) / ru) ** 3 + abs(v / rv) ** 3          # quase retângulo de quinas redondas
    if q <= 1:
        pu, pv = u + 1.0, v + 0.05
        dp = math.hypot(pu, pv * 0.92)
        if math.hypot(pu - 0.36, pv - 0.4) < 0.28: return (255, 255, 255)
        if dp < 0.98: return PRETO
        if dp < 1.25: return IRIS
        return BRANCO
    qa = abs((u + 0.1 - 0.45) / (ru + 0.95)) ** 3 + abs((v - 0.05) / (rv + 0.75)) ** 3
    if qa <= 1 and u > -2.75: return AZUL if v < -0.3 or u > 1.6 else AZUL_CLARO
    return None

def mat_faceta_olho(fora, cz):
    base = mat_bloco(cor_cabeca, borda=.03, faixa=FAIXA_CAB, alto=.04, fundo=-.10)
    def f(c):
        if c["face"] == fora:
            x, y, z = c["p"]
            r = olho(z - cz, y - OLHO_Y)
            if r is not None: return r
        return base(c)
    return f

def camada_cabeca(nome, y0, y1, d, zt, mat, olhos=False, res=4):
    """Fatia octogonal da cabeça recuada 'd': frente reta, faces diagonais a 45° (o olho vai inteiro na
    diagonal, que aparece de frente e de lado como na ficha), laterais e nuca."""
    pcs = []
    zf, cx = CAB_ZF + d, CAB_X - d
    fx = FRENTE_X - 0.414 * d
    zs = CAB_ZF + (CAB_X - FRENTE_X) - 0.586 * d
    pcs.append(caixa(nome + "_frente", [-fx - 0.05, y0, zf], [fx + 0.05, y1, zs + 0.5], mat, res=res))
    pcs.append(caixa(nome + "_meio", [-cx, y0, zs - 0.4], [cx, y1, zt - 1.0], mat, res=res))
    pcs.append(caixa(nome + "_nuca", [-cx + 1.0, y0, zt - 1.2], [cx - 1.0, y1, zt], mat, res=res))
    L = (cx - fx) * math.sqrt(2) + 0.25
    for lado in (-1, 1):
        mx, mz = (fx + cx) / 2, (zf + zs) / 2
        pcx, pcz = (mx - 0.7071 * FAC_T / 2) * lado, mz + 0.7071 * FAC_T / 2
        fora = "east" if lado > 0 else "west"
        m = mat_faceta_olho(fora, pcz) if olhos else no_mundo(mat, 45 * lado, (pcx, 0, pcz))
        pcs.append(caixa(f"{nome}_diag_{'d' if lado < 0 else 'e'}", [pcx - FAC_T / 2, y0, pcz - L / 2], [pcx + FAC_T / 2, y1, pcz + L / 2],
                         m, rot=(0, 45 * lado, 0), pivo=(pcx, (y0 + y1) / 2, pcz), res=res))
        if olhos:   # sobrancelha: bloco rosa saliente por cima do olho, descendo para o bico (olhar bravo)
            xf = pcx + FAC_T / 2 * lado
            x0, x1 = sorted((xf - 0.3 * lado, xf + 0.55 * lado))
            yb = OLHO_Y + 0.85 + 0.35
            sob = caixa(f"sobrancelha_{'d' if lado < 0 else 'e'}", [x0, yb - 0.55, pcz - L / 2 + 0.1], [x1, yb + 1.0, pcz + L / 2 - 0.1],
                        mat_bloco(lambda p, f: ROSA_PALIDO if f == "up" else ROSA_CLARO, borda=.06, alto=.06, fundo=-.4),
                        rot=(-15, 0, 0), pivo=(xf, yb, pcz), res=4)
            pcs.append(osso(f"sobrancelha_{'d' if lado < 0 else 'e'}", [pcx, (y0 + y1) / 2, pcz], [0, 45 * lado, 0], [sob]))
    return pcs

def cor_bico(p, face):
    x, y, z = p
    if face == "up":
        if abs(abs(x) - 1.3) < 0.3 and abs(z + 16.4) < 0.3: return (150, 84, 20)     # narinas
        return AMARELO_CLARO
    if y < 23.0: return LARANJA
    return AMARELO

# ---------------- brânquias ----------------
def guelra(nome, raiz, lado, L, recuo, eleva, n=4):
    """Brânquia de axolote em blocos grossos, como a 'Brânquias' da ficha: haste rosa que afina para a ponta,
    pente de blocos magenta/rosa-forte em degrau na beirada de cima, pente menor rosa embaixo e ponta magenta.
    Osso externo sem rotação (é ele que balança na animação); o interno dá a direção."""
    x, y, z = raiz
    s = lado
    pcs = []
    x0, x1 = xs(s, -1.0, L * 0.58)
    pcs.append(caixa(nome + "_haste", [x0, y - 1.3, z - 1.25], [x1, y + 1.3, z + 1.25], mat_degrade(ROSA_CLARO, ROSA, 0, s < 0)))
    x0, x1 = xs(s, L * 0.56, L)
    pcs.append(caixa(nome + "_ponta", [x0, y - 1.0, z - 1.05], [x1, y + 1.0, z + 1.05], mat_degrade(ROSA, ROSA_FORTE, 0, s < 0)))
    x0, x1 = xs(s, L - 0.2, L + 1.6)
    pcs.append(caixa(nome + "_bico", [x0, y - 0.6, z - 0.85], [x1, y + 1.4, z + 0.85], mat_liso(MAGENTA, borda=.18)))
    passo = (L - 0.6) / n
    for k in range(n):                             # pente de cima: blocos em degrau que baixam para a ponta
        a = 0.6 + passo * k
        h = 2.6 - 0.3 * k
        cor = MAGENTA if k % 2 == 0 else ROSA_FORTE
        x0, x1 = xs(s, a + 0.2, a + passo * 0.86)
        yb = y + (1.2 if a < L * 0.56 else 0.9)
        pcs.append(caixa(f"{nome}_f{k}", [x0, yb, z - 1.15 + 0.08 * k], [x1, yb + h, z + 1.15 - 0.08 * k], mat_liso(cor, borda=.16)))
    for k in range(n - 1):                         # pente de baixo, rosa
        a = 1.0 + passo * k
        x0, x1 = xs(s, a + 0.1, a + passo * 0.86)
        h = 1.3 - 0.15 * k
        pcs.append(caixa(f"{nome}_b{k}", [x0, y - 1.2 - h, z - 1.0], [x1, y - 1.2, z + 1.0], mat_liso(ROSA if k % 2 else ROSA_FORTE, borda=.16)))
    dentro = osso(nome + "_dir", list(raiz), [0, -recuo * s, eleva * s], pcs)
    return osso(nome, list(raiz), [0, 0, 0], [dentro])

GUELRAS = [  # (y da raiz, z da raiz, comprimento, recuo (graus para trás), elevação (graus para cima))
    (29.8, -5.8, 15.5, 48, 28),
    (26.0, -5.2, 16.5, 44, -3),
    (22.4, -5.4, 15.0, 50, -24),
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
                return q + [q[0]]
            parado[f"guelra_{s_}_{k}"] = kf(6, 4)
            andando[f"guelra_{s_}_{k}"] = kf(11, 6)
    return parado, andando

ANIM_PARADO, ANIM_ANDANDO = anim_guelras()


# ================= cauda =================
def pena_cauda(nome, base, segs, rot0, curva, mat_fn, sobrepoe=1.0):
    """Cadeia de blocos (eixo y; curva = rotação em x de cada junta) em que cada segmento começa 'sobrepoe' antes do fim do anterior: a foice
    grossa curva sem abrir fresta. Ossos '<nome>_0', '<nome>_1'..."""
    def seg(k, pos):
        L, w, h, c0, c1 = segs[k]
        px, py, pz = pos
        filhos = [caixa(f"{nome}_{k}", [px - w / 2, py, pz - h / 2], [px + w / 2, py + L, pz + h / 2], mat_fn(c0, c1))]
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py + L - sobrepoe, pz)))
        return osso(f"{nome}_{k}", list(pos), list(rot0) if k == 0 else [curva[k - 1], 0, 0], filhos)
    return seg(0, tuple(base))

def mat_foice(c0, c1):
    """Segmento da foice: degradê em 2 tons ao longo dele, beirada de fora (z+) um tom mais escuro."""
    def f(c):
        lo, hi = c["b"][0][1], c["b"][1][1]
        t = clamp((c["p"][1] - lo) / max(hi - lo, 1e-6))
        cor = c0 if t < .5 else c1
        l = .04
        if c["face"] in ("east", "west"):
            z0, z1 = c["b"][0][2], c["b"][1][2]
            d = (c["p"][2] - z0) / max(z1 - z0, 1e-6)
            l = .12 if d < .3 else -.12 if d > .72 else .02
        elif c["face"] == "up": l = .14
        elif c["face"] == "down": l = -.3
        if g.na_borda(c): l -= .12
        return tom(cor, l)
    return f

FOICES = [  # (x, rx inicial, curva de cada junta, comprimentos, largura da faixa, cor raiz, cor ponta, y da raiz)
    (0.0, 14, (28, 28, 30, 34), (5.0, 4.8, 4.6, 4.2, 3.6), 5.8, AZUL_ROYAL, AZUL, 18.6),
    (2.3, 54, (14, 14, 20, 28, 34), (5.6, 5.6, 5.4, 5.0, 4.2, 3.0), 6.0, AZUL, AZUL_CLARO, 16.8),
    (-2.3, 82, (12, 16, 24, 30), (5.4, 5.2, 5.0, 4.6, 3.6), 5.6, AZUL, AZUL_CEU, 16.0),
    (1.3, 104, (16, 20), (5.0, 4.8, 4.2), 5.0, AZUL_CLARO, AZUL_CEU, 15.4),
    (-1.3, 126, (10, 12), (4.8, 4.4, 3.8), 4.6, AZUL_CLARO, AZUL_CEU, 14.8),
]
ONDAS = [(f"cauda_p{k}", len(f[3]), (2.5, 1.5, 0)) for k, f in enumerate(FOICES)]


# ================= corpo =================
def cor_corpo(p, face):
    x, y, z = p
    if z < -9.0 and abs(x) < 6.0: return CREME
    if y < 9.0: return mix(ROSA_CLARO, CREME, .5)
    return ROSA_CLARO

def espiral(a, b):
    """Espiral azul da 'Plumagem Úmida': 1,25 volta (achatada, mais larga que alta) que termina embaixo e corre
    para a frente e sobe numa cauda. a = para a frente (bico), b = para cima, em unidades a partir do centro."""
    a2 = a / 1.3
    r = max(abs(a2), abs(b)) * 0.55 + math.hypot(a2, b) * 0.45
    phi = math.degrees(math.atan2(b, a2))
    th0 = (phi - 180.0) % 360.0
    for k in range(2):
        th = th0 + 360.0 * k
        if th > 450.0: break
        if abs(r - (0.25 + 1.8 * th / 360.0)) < 0.62: return True
    if r < 0.6: return True
    rE = 0.25 + 1.8 * 1.25
    for (a0, b0), (a1, b1) in (((0.0, -rE), (3.4, -rE)), ((3.4, -rE), (5.0, -rE + 1.0)), ((5.0, -rE + 1.0), (5.6, -rE + 2.6))):
        da, db = a1 - a0, b1 - b0
        t = clamp(((a - a0) * da + (b - b0) * db) / (da * da + db * db))
        if max(abs(a - a0 - t * da), abs(b - b0 - t * db)) < 0.62: return True
    return False


def montar():
    # ================= cabeça (bloco grande, octogonal em planta) =================
    cab = []
    mc = mat_bloco(cor_cabeca, borda=.03, faixa=FAIXA_CAB, alto=.04, fundo=-.10)
    cab += camada_cabeca("queixo", 20.6, 22.2, 0.6, CAB_ZT - 0.6, mc)
    cab += camada_cabeca("cranio", 22.1, 29.7, 0.0, CAB_ZT, mc, olhos=True)
    cab += camada_cabeca("testa", 29.6, 31.1, 0.6, CAB_ZT - 0.4, mc)
    cab += camada_cabeca("topo", 31.0, 32.2, 1.8, CAB_ZT - 1.2, mc)
    # bico largo (1/3 da cabeça), base + ponta em cunha um pouco para baixo + mandíbula
    mb = mat_bloco(cor_bico, borda=.08)
    cab.append(caixa("bico_base", [-2.8, 22.6, CAB_ZF - 2.6], [2.8, 26.6, CAB_ZF + 0.4], mb))
    cab.append(caixa("bico_ponta", [-2.3, 23.4, CAB_ZF - 5.0], [2.3, 26.3, CAB_ZF - 2.4], mb))
    cab.append(caixa("bico_baixo", [-2.3, 22.0, CAB_ZF - 3.0], [2.3, 22.8, CAB_ZF + 0.2], mat_liso(LARANJA, borda=.1)))
    # barbela: dois lóbulos vermelhos pendurados embaixo do bico, com a ponta em degrau
    mbar = mat_bloco(lambda p, f: VERMELHO, borda=.12, alto=.05, fundo=-.2)
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        x0, x1 = xs(lado, 0.3, 2.9)
        cab.append(caixa("barbela_" + s_, [x0, 18.0, CAB_ZF - 2.2], [x1, 22.2, CAB_ZF + 0.2], mbar))
        x0, x1 = xs(lado, 0.6, 2.4)
        cab.append(caixa("barbela_ponta_" + s_, [x0, 16.6, CAB_ZF - 1.9], [x1, 18.2, CAB_ZF - 0.1], mbar))
    # crista aquática: blocos magenta em degrau (crista central alta + lobos dos lados + lobo de trás)
    mcr = mat_bloco(lambda p, f: MAGENTA, borda=.12, alto=.08, fundo=-.18)
    crista = []
    for k, (z0, z1, w, y1) in enumerate([(-15.8, -12.4, 1.8, 35.0), (-13.4, -9.6, 2.1, 36.4), (-10.2, -6.4, 2.4, 37.6),
                                         (-7.0, -3.4, 2.2, 36.0)]):
        crista.append(caixa(f"crista_{k}", [-w, 31.0 if k == 0 else 31.6, z0], [w, y1, z1], mcr))
        if k in (1, 2, 3):      # degrau de cima, mais estreito (crista em blocos escalonados como na ficha)
            crista.append(caixa(f"crista_{k}_topo", [-w + 0.6, y1 - 0.2, z0 + 0.5], [w - 0.6, y1 + (1.2 if k != 2 else 1.4), z1 - 0.7], mcr))
    crista.append(caixa("crista_tras", [-1.9, 31.4, -3.8], [1.9, 35.2, 1.6], mcr))
    for lado in (-1, 1):
        x0, x1 = xs(lado, 2.2, 5.4)
        crista.append(caixa("crista_lado_" + ("d" if lado < 0 else "e"), [x0, 31.6, -12.4], [x1, 36.4, -5.6], mcr))
    cab.append(osso("crista", [0, 32, -7.8], [0, 0, 0], crista))
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        for k, (y0, z0, L, rec, ele) in enumerate(GUELRAS):
            cab.append(guelra(f"guelra_{s_}_{k}", (7.4 * lado, y0, z0), lado, L, rec, ele))
    cabeca = osso("cabeca", [0, 22, -8.8], [0, 0, 0], cab)

    # ================= pescoço curto (a cabeça assenta no peito) =================
    pescoco = osso("pescoco", [0, 19, -9], [0, 0, 0], [
        caixa("pescoco", [-6.0, 17.0, -13.6], [6.0, 21.4, -5.0], mat_bloco(cor_corpo), res=2), cabeca])

    # ================= tronco: ovo deitado =================
    corpo = []
    mt = mat_bloco(cor_corpo, faixa=(7.0, 21.0))
    corpo += g.arredondado2("tronco", [-7.6, 7.4, -12.6], [7.6, 20.6, 8.6], mt, r=3.6, res=2)
    corpo += g.arredondado("rabadilha", [-5.6, 11.6, 6.0], [5.6, 20.8, 12.0], mt, r=1.6, res=2)
    # peito creme em fileiras de penas grossas (cada fileira avança sobre a de baixo; a do meio desce mais)
    mp = mat_bloco(lambda p, f: CREME, borda=.12, alto=.06, fundo=-.16)
    FILAS = [(20.6, 17.4, 7.0, -14.4), (17.6, 14.6, 6.6, -14.2), (14.8, 11.8, 5.8, -13.6), (12.0, 9.2, 4.6, -12.4),
             (9.4, 7.6, 3.0, -10.4)]
    for k, (ya, yb, w, zf) in enumerate(FILAS):
        corpo.append(caixa(f"peito_{k}", [-w, yb, zf], [w, ya, zf + 5.0], mp, res=2))
        if k < len(FILAS) - 1:
            corpo.append(caixa(f"peito_{k}_meio", [-w * 0.42, yb - 0.8, zf - 0.3], [w * 0.42, ya - 0.6, zf + 4.0], mp, res=2))

    # ================= asas: escudo rosa com fileiras de penas em degrau atrás e a espiral azul =================
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        fora = "east" if lado > 0 else "west"
        def cor_asa(p, face, fora=fora):
            x, y, z = p
            if face == fora and espiral(-(z + 0.6), y - 15.6): return AZUL if y < 15.6 else AZUL_CLARO
            return ROSA_CLARO
        ma = mat_bloco(cor_asa, borda=.08, faixa=(8.6, 21.0))
        asa = []
        def bloco(nome, xa, xb, y0, y1, z0, z1, m=ma):
            x0, x1 = xs(lado, xa, xb)
            asa.append(caixa(nome + "_" + s_, [x0, y0, z0], [x1, y1, z1], m, res=4))
        # escudo das coberteiras (leva a espiral), saliente e de quinas chanfradas
        # (fileiras de coberteiras em blocos lisos: a de baixo um pouco mais para dentro, a espiral passa
        #  de uma para a outra sem quebrar)
        for k, (xb, y0, y1, z0, z1) in enumerate([(10.9, 9.2, 13.2, -6.0, 3.6), (11.8, 12.9, 17.2, -8.0, 6.8),
                                                  (11.55, 16.9, 21.0, -8.4, 6.0), (10.8, 20.8, 22.0, -6.0, 5.0)]):
            bloco(f"asa{k}", 7.2, xb, y0, y1, z0, z1)
        # rêmiges: fileiras grossas sobrepostas (as de cima por fora) com a ponta em degrau para a cauda
        mr = mat_bloco(lambda p, f: ROSA_CLARO, borda=.12, alto=.08, fundo=-.22)
        for k, (y0, y1, z1, xb) in enumerate([(18.4, 21.8, 14.0, 10.4), (15.0, 18.6, 13.6, 10.1),
                                              (12.2, 15.0, 11.8, 9.8), (10.0, 12.6, 9.0, 9.5)]):
            bloco(f"asa_pena{k}", 7.2, xb, y0, y1, -2.0, z1 - 1.4, mr)
            bloco(f"asa_ponta{k}", 7.4, xb - 0.3, y0 + 0.5, y1 - 0.5, z1 - 1.6, z1, mr)
        corpo.append(osso("asa_" + s_, [8.2 * lado, 19.0, -4.0], [0, 0, 0], asa))

    # ================= cauda: leque de foices azuis grossas que arqueiam para trás e caem =================
    cauda = []
    BASE = (0.0, 16.6, 9.6)
    for k, (x, rx0, cv, Ls, h, c0, c1, yb) in enumerate(FOICES):
        n = len(Ls)
        segs = [(L, 4.4 - 0.25 * i, h - 0.3 * i, mix(c0, c1, i / n), mix(c0, c1, (i + 0.6) / n)) for i, L in enumerate(Ls)]
        cauda.append(pena_cauda(f"cauda_p{k}", (BASE[0] + x, yb, BASE[2]), segs, (rx0, 0, 0), cv,
                                mat_foice, sobrepoe=0.9))
    corpo.append(osso("cauda", list(BASE), [0, 0, 0], cauda))

    corpo.append(pescoco)
    raiz = osso("corpo", [0, 9, 0], [0, 0, 0], corpo)

    # ================= pernas e patas anfíbias =================
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 5.0 * lado; zc = -0.6
        pp = []
        ml = mat_liso(AMARELO, borda=.08)
        pp.append(caixa("coxa_" + s, [xc - 2.6, 6.0, zc - 2.6], [xc + 2.6, 9.0, zc + 2.6], mat_bloco(cor_corpo), res=2))
        pp.append(caixa("perna_" + s, [xc - 2.3, 2.2, zc - 2.3], [xc + 2.3, 7.2, zc + 2.3], ml))
        pp.append(caixa("pe_" + s, [xc - 4.2, 1.0, zc - 5.0], [xc + 4.2, 3.6, zc + 2.8], ml))
        mg = mat_bloco(lambda p, f: ROXO_CLARO if f == "up" else ROXO, borda=.16)
        for k, dx in enumerate((-3.0, 0.0, 3.0)):
            pp.append(caixa(f"dedo_{k}_{s}", [xc + dx - 1.25, 0.0, zc - 9.0], [xc + dx + 1.25, 2.8, zc - 4.4], mg))
        pp.append(caixa("dedo_tras_" + s, [xc - 1.1, 0.0, zc + 2.4], [xc + 1.1, 2.0, zc + 5.0], mg))
        return osso("perna_" + s, [xc, 8.5, zc], [0, 0, 0], pp)

    return [raiz, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

"""Renacocó (#019, Fogo, mítico, suporte): o Curandeiro da Ressurreição. Ave mítica alta, esguia e nobre: corpo
azul e azul-claro, crista de plumas amarelas em chama com base azul-clara, bico amarelo reto e longo, barbela
vermelha e olhar azul sereno; manto roxo grande (bordas douradas em relevo, fecho de 2 medalhões, emblema da fênix
nas costas e padrões dourados nas pontas); asas azuis e amarelas sob o manto; cauda tripla de elos dourados com
centro azul-claro terminando em leques de penas amarelas e azuis; pernas longas amarelas com garras escuras.

Ideias da montagem (Fases 5, 6 e 7 do REFAZER.md):
- poucas peças grandes e chanfradas (arredondado/octogono) no tronco, pescoço, cabeça e pernas;
- manto em "painéis" grossos pendurados de um anel no ombro, cada um em 3 degraus encadeados que abrem um pouco mais
  embaixo (caimento de sino), com a borda dourada em relevo e os padrões pintados no referencial do painel;
- penas em telha (bloco + ponta em losango) no peito, nas asas e nos leques da cauda;
- cauda tripla: 3 correntes com um osso por elo (ONDAS) e o leque no fim de cada uma."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, clamp, tom, na_borda

ID = "renacoco"; NOME = "Renacocó"; NUMERO = 19
ALTURA = 2.5
QUADRUPEDE = False
ROSTO = ((0, 36.0, -5.6), 7.2)

# ---------------- paleta (amostrada com PIL na "Paleta de Cores" da ficha e na expressão neutra) ----------------
ROXO_ESC = (98, 28, 152); ROXO_VIVO = (174, 59, 250); ROXO = (136, 42, 204); ROXO_FUNDO = (64, 16, 104)
AZUL = (2, 168, 251); CIANO = (133, 238, 253); AZUL_CARA = (82, 214, 252); AZUL_INT = (18, 112, 228)
AZUL_ESC = (14, 52, 150); CRUZ = (20, 36, 132); CRUZ_CLARA = (60, 90, 200)
CREME = (254, 234, 191); AMARELO = (254, 239, 96); AMAR = (255, 214, 60); AMAR_ESC = (226, 170, 30)
AZUL_REAL = (40, 110, 220); AZUL_FUNDO = (24, 74, 184)   # azul real do corpo (arte)
OURO = (250, 188, 40); OURO_CL = (255, 230, 120); OURO_ESC = (186, 116, 14)
VERM = (226, 26, 24); VERM_ESC = (150, 10, 18)
BICO = (251, 202, 60); BICO_CL = (253, 224, 112); BICO_ESC = (232, 156, 32)
BABADOR = (184, 230, 247)
SOBR = (12, 44, 133)
GARRA = (46, 40, 54); PRETO = (16, 12, 26); BRANCO = (250, 250, 252)

def claro(c, f):
    """Clareia multiplicando (mantém a saturação da ficha)."""
    return tuple(min(255, int(round(v * (1 + f)))) for v in c)

def grad(paradas, t):
    t = clamp(t)
    for (t0, c0), (t1, c1) in zip(paradas, paradas[1:]):
        if t <= t1: return mix(c0, c1, (t - t0) / max(t1 - t0, 1e-6))
    return paradas[-1][1]

SOMBRA_OURO = (226, 170, 30)

def amarelado(c): return c[0] > 180 and c[1] > 140 and c[2] < 175

def escurece(c, f):
    """Sombra: no amarelo puxa para o dourado (nada de cáqui/oliva); nas outras cores, a sombra padrão."""
    if f <= 0: return c
    if amarelado(c): return mix(c, SOMBRA_OURO, min(1.0, f * 1.6))
    return tom(c, -f)

def luz(c, f): return tom(c, f) if f >= 0 else escurece(c, -f)

def mat_cor(cor_fn, **kw):
    def f(c):
        base = cor_fn(c["p"], c["face"])
        return None if base is None else luz(base, g.contexto_luz(c, **kw))
    return f

def anel(ax, az, zc, phi, lado):
    r = math.radians(phi)
    return lado * ax * math.cos(r), zc + az * math.sin(r)

def mat_ouro(c):
    """Ouro facetado (medalhões, borda em relevo, elos): topo claro, frente amarela, lados ouro, embaixo escuro."""
    face = c["face"]
    base = {"up": OURO_CL, "down": OURO_ESC, "north": mix(OURO, OURO_CL, 0.5)}.get(face, OURO)
    return tom(base, -0.25) if na_borda(c) else base

# paradas de cor das penas
P_AZUL = [(0, AZUL_FUNDO), (0.55, AZUL_REAL), (1, (96, 190, 248))]
P_CIANO = [(0, AZUL_REAL), (0.6, AZUL), (1, CIANO)]
P_AMAR = [(0, AZUL), (0.18, AMAR), (0.7, (255, 226, 80)), (1, (255, 238, 150))]
P_AMAR_PURO = [(0, AMAR), (0.5, AMARELO), (1, CREME)]
P_CRISTA = [(0, CIANO), (0.12, (251, 217, 102)), (0.75, (253, 232, 132)), (1, (255, 248, 205))]
P_CRISTA_AZ = [(0, AZUL), (0.5, CIANO), (1, (205, 246, 255))]
LIMAO = (251, 217, 102)
P_AZUL2 = [(0, AZUL_REAL), (0.6, AZUL), (1, mix(AZUL, CIANO, 0.5))]
P_PESC = [(0, AZUL_REAL), (0.6, AZUL), (1, mix(AZUL, CIANO, 0.5))]
P_ASA = [(0, AMAR), (0.7, (253, 228, 110)), (1, (255, 240, 170))]
P_ASA_CREME = [(0, (255, 226, 110)), (0.7, CREME), (1, (255, 246, 222))]
P_ASA_CLARA = [(0, AZUL_REAL), (0.5, AZUL), (1, CIANO)]
P_PEITO_CLARO = [(0, AZUL), (0.6, mix(AZUL, CIANO, 0.45)), (1, CIANO)]
P_FRANJA = [(0, AZUL_FUNDO), (0.5, AZUL_REAL), (1, mix(AZUL, CIANO, 0.6))]

# ---------------- pena em bloco (corpo + ponta em losango) ----------------
def mat_pena_cor(paradas, y0, L, zc, W, claro_lado=-1):
    """Pena em bloco: degradê da raiz à ponta, metade clara e metade base na face larga (pena dobrada) com raque
    clara; contorno escuro só nas beiradas compridas; espessura em sombra."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        t = clamp((y0 - y) / max(L, 1e-6))
        base = grad(paradas, t)
        if face in ("east", "west"):
            u = (z - zc) / (W / 2)
            cor = claro(base, 0.08) if u * claro_lado > 0 else escurece(base, 0.08)
            if abs(u) < 0.08 and t < 0.85: cor = claro(cor, 0.08)
            if t < 0.1: cor = escurece(cor, 0.18)
            if c["nome"].endswith("_pt"):
                if na_borda(c): cor = escurece(cor, 0.25)
            elif c["i"] in (0, c["tw"] - 1): cor = escurece(cor, 0.25)
            return cor
        if face == "up": return claro(base, 0.06)
        if face == "down": return escurece(base, 0.4)
        return escurece(base, 0.18)
    return f

def pena(nome, raiz, phi, lado, L, W, paradas, flare=20, varre=0, T=0.9, brilho=False, claro_lado=-1):
    """Pena grossa pendurada da raiz: corpo + ponta em losango. phi = ângulo em volta do corpo (0 = para fora,
    -90 = frente, +90 = trás); flare abre a ponta para fora; varre puxa a ponta para trás."""
    x, y, z = raiz
    Lb = L - W * 0.5
    s = W / 1.4142
    m = mat_pena_cor(paradas, y, L, z, W, claro_lado)
    corpo = peca(nome, [x - T / 2, y - Lb, z - W / 2], [x + T / 2, y, z + W / 2], m, res=2, brilho=brilho)
    ponta = peca(nome + "_pt", [x - T / 2 + 0.03, y - Lb - s / 2, z - s / 2], [x + T / 2 - 0.03, y - Lb + s / 2, z + s / 2], m,
                 rot=(45, 0, 0), pivo=(x, y - Lb, z), res=2, brilho=brilho)
    return osso(nome, list(raiz), [0, -phi * lado, 0], [osso(nome + "_p", list(raiz), [-varre, 0, flare * lado], [corpo, ponta])])

# ================= CABEÇA =================
CAB_Y0, CAB_Y1 = 29.4, 35.4
ZF = -7.0                        # frente da cara (onde nasce o bico)
FRENTE_X = 1.5
FAC_ANG = 32                     # a faceta do olho olha mais para o lado (ave): crânio mais estreito
FAC_L, FAC_T = 4.0, 1.4
_tx, _tz = math.sin(math.radians(FAC_ANG)), math.cos(math.radians(FAC_ANG))
_nx, _nz = math.cos(math.radians(FAC_ANG)), -math.sin(math.radians(FAC_ANG))
LX = FRENTE_X + FAC_L * _tx
ZL = ZF + FAC_L * _tz
FAC_S = (FRENTE_X + _tx * FAC_L / 2, ZF + _tz * FAC_L / 2)
FAC_C = (FAC_S[0] - _nx * FAC_T / 2, FAC_S[1] - _nz * FAC_T / 2)
OLHO_Y = 32.6
OLHO_RU, OLHO_RV = 1.9, 1.45
OLHO_CORTE0, OLHO_CORTE_INC = 0.8, 0.16     # pálpebra pesada mas serena (diagonal suave descendo para o bico)

def olho(u, v):
    """Olho nobre e sereno (Fase 7 no tom da ficha): mais largo que alto, pálpebra pesada cortando o topo numa
    diagonal suave para o bico, íris azul grande puxada para a frente com pupila preta junto da borda do bico e 1
    brilho; esclera branca só na cunha de trás. u: ao longo da face (negativo = bico); v: para cima."""
    ru, rv = OLHO_RU, OLHO_RV
    uu = u / ru
    if abs(uu) > 1: return None
    corte = OLHO_CORTE0 + OLHO_CORTE_INC * u
    baixo = -rv * (0.82 - 0.14 * uu) * (1 - max(0.0, -uu) ** 2.4)
    cima = rv * (0.98 - 0.08 * uu) * (1 - max(0.0, -uu) ** 1.8)
    topo = min(cima, corte)
    if v > corte and v <= corte + 0.14 and v <= cima + 0.3: return mix(PRETO, AZUL_ESC, 0.5)    # sombra da pálpebra
    if v < baixo or v > topo: return None
    if topo - v < 0.13: return PRETO                                                            # fio da pálpebra
    ic, ir = -0.24, 0.64
    du = (uu - ic) / ir; dv = v / (rv * 0.95)
    if du * du + dv * dv <= 1 or (uu < ic and v >= baixo):
        if ((uu + 0.4) / 0.15) ** 2 + ((v + 0.02) / 0.48) ** 2 <= 1: return PRETO                # pupila
        if ((uu + 0.24) / 0.1) ** 2 + ((v - topo + 0.36) / 0.16) ** 2 <= 1: return (255, 255, 255)  # brilho
        cor = mix((40, 190, 255), (10, 84, 200), clamp((v - baixo) / max(topo - baixo, 0.1)))
        if topo - v < 0.2: cor = tom(cor, -0.25)
        if du * du + dv * dv > 0.78 and uu > ic: cor = AZUL_ESC
        return cor
    return mix(BRANCO, (226, 233, 246), clamp((topo - v) / 1.2))

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return CIANO                                           # topo da cabeça azul-claro (arte)
    if y > OLHO_Y + 1.0: return mix(AZUL, CIANO, clamp((y - OLHO_Y - 1.0) / 1.6))   # testa clareando para o ciano
    base = mix(AZUL, mix(AZUL_REAL, AZUL, 0.4), clamp((y - (OLHO_Y - 2.6)) / 2.2))    # bochecha mais funda
    if z > ZL + 1.2: base = mix(base, AZUL_INT, 0.3 * clamp((z - ZL - 1.2) / 2.0))   # trás da cabeça um tom mais fundo
    return base

def mat_faceta(lado):
    base = mat_cor(cor_cabeca, borda=.0, curva=.2)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            cor = olho(z - FAC_C[1] - 0.15, y - OLHO_Y)
            if cor is not None: return cor
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return BICO_ESC
    if face == "up": return BICO_CL
    if face in ("east", "west") and abs(z - (ZF - 1.4)) < 0.3 and abs(y - 31.55) < 0.24: return (120, 70, 10)   # narina
    if face == "north":
        larg = 0.3 + 0.9 * clamp((y - 29.6) / 2.2)
        return mix(BICO_CL, BICO, clamp((31.8 - y) / 1.6)) if abs(x) < larg else tom(BICO, -0.15)
    return mix(BICO_CL, BICO, clamp((31.9 - y) / 1.4))

def lamina(nome, base, rot0, curva, segs, paradas, eixo="y", res=2):
    """Pluma grossa encadeada (crista, penas do rosto, leques): segmentos que afinam (pena_curva), degradê pelas
    paradas ao longo da cadeia inteira, face larga com metade clara."""
    n = len(segs)
    def fabrica(k):
        def mf(c0, c1, ei, inv):
            def f(c):
                (x0, y0, z0), (x1, y1, z1) = c["b"]
                lo, hi = c["b"][0][ei], c["b"][1][ei]
                tl = clamp((c["p"][ei] - lo) / max(hi - lo, 1e-6))
                if inv: tl = 1 - tl
                t = (k + tl) / n
                base = grad(paradas, t)
                face = c["face"]
                if face == "up": return claro(base, 0.08)
                if face == "down": return escurece(base, 0.35)
                dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
                larga = ("east", "west") if dx <= min(dy, dz) else (("north", "south") if dz <= dy else ("up", "down"))
                if face in larga:
                    cor = claro(base, 0.1) if (c["i"] + .5) / c["tw"] < 0.5 else escurece(base, 0.05)
                    if na_borda(c): cor = escurece(cor, 0.16)
                    return cor
                return escurece(base, 0.14)
            return f
        return mf
    # pena_curva usa o mesmo mat_fn para todos os segmentos: o índice sai do nome da peça
    def mat_fn(c0, c1, ei, inv):
        cache = {}
        def f(c):
            k = int(c["nome"].rsplit("_", 1)[-1])
            if k not in cache: cache[k] = fabrica(k)(c0, c1, ei, inv)
            return cache[k](c)
        return f
    return g.pena_curva(nome, base, [(L, w, h, None, None) for L, w, h in segs], rot0, curva, eixo, mat_fn, res=res)

def cabeca_ossos():
    cab = []
    mc = mat_cor(cor_cabeca, borda=.0, curva=.25)
    fx = (CAB_Y0, CAB_Y1)
    # crânio: volume bem chanfrado atrás + frente estreita; as facetas diagonais (com o olho) fecham a quina
    cab += g.arredondado2("cranio", [-LX, CAB_Y0, ZL - 0.5], [LX, CAB_Y1 - 1.0, 1.2], mc, r=2.0, faixa=fx, res=3)
    cab += g.arredondado("cranio_alto", [-LX + 1.0, CAB_Y1 - 1.8, ZL - 0.2], [LX - 1.0, CAB_Y1, 1.0], mc, r=0.9, faixa=fx, res=3)
    cab += g.arredondado("cranio_frente", [-FRENTE_X - 0.4, CAB_Y0 + 0.3, ZF], [FRENTE_X + 0.4, CAB_Y1 - 1.6, ZL + 0.4], mc, r=0.6, faixa=fx, res=3)
    # testa inclinada: desce do alto do crânio até a base do bico (a cabeça afina para a frente)
    cab.append(peca("testa", [-FRENTE_X - 0.2, CAB_Y1 - 2.0, ZF + 0.2], [FRENTE_X + 0.2, CAB_Y1 - 0.6, ZL + 1.6], mc,
                    rot=(-24, 0, 0), pivo=(0, CAB_Y1 - 0.6, ZL + 1.6), faixa=fx, res=3))
    # queixo/garganta: volume claro que afina para trás embaixo do bico
    cab += g.arredondado("queixo", [-2.4, 28.5, ZF + 0.9], [2.4, 30.2, ZL + 3.6],
                         mat_cor(lambda p, f_: AZUL_CARA, borda=.0, curva=.2), r=0.7, res=3)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, CAB_Y0 + 0.2, cz - FAC_L / 2], [cx + FAC_T / 2, CAB_Y1 - 0.5, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, FAC_ANG * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=fx, res=8))
        # sobrancelha: pena azul-clara grossa deitada sobre o olho (só a aba sai da face), descendo suave para o
        # bico na frente e seguindo para trás como uma pluma (linha marcante, nobre, sem virar viseira)
        ox0, ox1 = sorted((cx + FAC_T / 2 * lado - 0.5 * lado, cx + FAC_T / 2 * lado + 0.55 * lado))
        ang = math.degrees(math.atan(OLHO_CORTE_INC))
        zc0 = cz + 0.15
        yb = OLHO_Y + OLHO_CORTE0 + 0.2
        def msob(c):
            if c["face"] == "down": return tom(SOBR, -0.2)
            base = {"up": mix(SOBR, AZUL, 0.35)}.get(c["face"], SOBR)
            return tom(base, -0.12) if na_borda(c) else base
        cab.append(osso("sobrancelha_" + s, [cx, yb, zc0], [0, FAC_ANG * lado, 0], [
            peca("sobrancelha_" + s, [ox0, yb, cz - FAC_L / 2 + 0.7], [ox1, yb + 0.9, cz + FAC_L / 2 + 0.5],
                 msob, rot=(-ang, 0, 0), pivo=(cx, yb, zc0), res=4)]))
    # bico reto e longo em cunha: base alta (tampa + quilha em V de frente), meio e ponta afinando com leve gancho
    mb = mat_cor(cor_bico, borda=.05, curva=.3)
    def mq(c):
        f_ = c["face"]
        cor = mix(BICO_CL, BICO, 0.35) if f_ in ("up", "east") else (BICO if f_ in ("north", "south") else claro(BICO, 0.03))
        return tom(cor, -0.14) if na_borda(c) else cor
    fb = (29.4, 32.4)
    cab.append(peca("bico_tampa", [-1.0, 31.2, ZF - 2.4], [1.0, 32.4, ZF + 0.6], mb, faixa=fb, res=4))
    q = 1.1 * 1.4142
    cab.append(peca("bico_quilha", [-q / 2, 31.05 - q / 2, ZF - 2.3], [q / 2, 31.05 + q / 2, ZF + 0.5], mq, rot=(0, 0, 45),
                    pivo=(0, 31.05, ZF), faixa=fb, res=4))
    piv = (0, 32.2, ZF - 2.2)
    cab.append(peca("bico_tampa2", [-0.8, 31.0, ZF - 4.6], [0.8, 32.2, ZF - 2.1], mb, rot=(-6, 0, 0), pivo=piv, faixa=fb, res=4))
    q = 0.85 * 1.4142
    cab.append(peca("bico_quilha2", [-q / 2, 30.95 - q / 2, ZF - 4.5], [q / 2, 30.95 + q / 2, ZF - 2.2], mq, rot=(-6, 0, 45),
                    pivo=(0, 30.95, ZF - 2.2), faixa=fb, res=4))
    cab.append(peca("bico_ponta", [-0.45, 30.5, ZF - 6.1], [0.45, 31.7, ZF - 4.4],
                    mat_cor(lambda p, f_: BICO_CL if f_ == "up" else mix(BICO, BICO_ESC, clamp((31.2 - p[1]) / 1.0)), borda=.1, curva=.2),
                    rot=(-20, 0, 0), pivo=(0, 31.7, ZF - 4.4), faixa=(30.5, 31.7), res=4))
    cab.append(peca("bico_baixo", [-0.75, 29.7, ZF - 3.6], [0.75, 30.5, ZF + 0.4], mat_cor(lambda p, f_: BICO_ESC, borda=.1), res=4,
                    rot=(5, 0, 0), pivo=(0, 30.5, ZF + 0.4)))
    # barbela: 2 lóbulos curtos e arredondados logo abaixo da base do bico (largura do bico, ~metade da cabeça)
    def cor_barb(p, f_):
        if abs(p[0]) < 0.12: return VERM_ESC
        return mix(VERM, VERM_ESC, clamp((28.6 - p[1]) / 2.0))
    mbar = mat_cor(cor_barb, borda=.08, curva=.25)
    for lado, fim in ((-1, 27.1), (1, 27.4)):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.0, 0.85 * lado)); x2, x3 = sorted((0.12 * lado, 0.72 * lado))
        cab.append(osso("barbela_" + s, [0.0, 29.7, ZF - 0.9], [0, 0, -3 * lado], [
            peca("barbela_a_" + s, [x0, fim + 0.7, ZF - 1.7], [x1, 29.8, ZF - 0.1], mbar, faixa=(fim, 29.8), res=4),
            peca("barbela_b_" + s, [x2, fim, ZF - 1.45], [x3, fim + 0.9, ZF - 0.35], mbar, faixa=(fim, 29.8), res=4)]))
    # penas do rosto (moldura nobre): atrás do olho, em telha, deitadas para trás e um pouco para baixo; azuis
    # embaixo, azul-claras no meio, amarelas em cima (emendam com a crista)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, (y, z, L, rx, ry, h, par) in enumerate([(30.8, -1.2, 7.0, 30, 14, 2.4, P_CIANO), (32.4, -0.8, 7.6, 22, 12, 2.6, P_AZUL2),
                                                        (34.0, -0.6, 7.2, 12, 10, 2.6, P_CRISTA)]):
            segs = [(L * 0.42, 1.0, h), (L * 0.33, 0.9, h * 0.7), (L * 0.27, 0.8, h * 0.38)]
            cab.append(lamina(f"rosto{k}_{s}", ((LX - 0.7) * lado, y, z), (rx, ry * lado, 0), (6, 0, 0), segs, par, eixo="z"))
    cab.append(crista_ossos())
    return cab

# crista em chama: plumas amarelas largas que sobem e varrem para trás em leque, com base azul-clara
CRISTA = [  # (x, z da raiz, comprimento, inclinação para trás, abertura lateral, larga de frente?, paradas)
    # frente: pluma curta azul-clara na base; miolo: plumas largas de lado, cada vez mais longas e deitadas para trás
    (0.0, -4.4, 2.8, 58, 0, False, "az"), (0.3, -3.2, 5.0, 30, -6, False, "am"), (-0.3, -1.8, 6.4, 40, 5, False, "am"),
    (0.2, -0.4, 7.4, 52, -4, False, "am"), (-0.2, 0.9, 7.0, 64, 6, False, "am"),
    # leque lateral (largo de frente, assimétrico) abrindo a chama para os lados
    (1.4, -2.6, 5.4, 34, -24, True, "am"), (-1.5, -2.2, 5.8, 38, 26, True, "am"), (1.7, -0.2, 6.0, 48, -30, True, "am"),
    (-1.6, 0.2, 5.6, 50, 28, True, "am"),
]

def crista_ossos():
    pc = []
    # base azul-clara da crista (o "diadema" de plumas curtas por cima da testa)
    pc.append(peca("crista_base", [-2.0, 34.2, -4.6], [2.0, 35.9, 1.2],
                   mat_cor(lambda p, f_: CIANO if f_ != "down" else AZUL, borda=.0, curva=.25), res=3))
    for k, (x, z, L, rx, rz, frente, cor) in enumerate(CRISTA):
        if frente: segs = [(L * 0.42, 2.6, 1.0), (L * 0.33, 1.8, 0.9), (L * 0.28, 0.8, 0.8)]
        else: segs = [(L * 0.42, 1.1, 3.4), (L * 0.33, 1.0, 2.3), (L * 0.28, 0.8, 0.9)]
        pc.append(lamina(f"crista{k}", (x, 35.4, z), (rx, 0, rz), (12, 0, 0), segs, P_CRISTA if cor == "am" else P_CRISTA_AZ, eixo="y"))
    return osso("crista", [0, 35.6, -2.0], [0, 0, 0], pc)

# ================= TRONCO, PEITO E MANTO =================
def escama(a, y, larg=2.4, alt=1.8):
    fila = math.floor(y / alt)
    fa = ((a + (fila % 2) * larg / 2) % larg) / larg
    fy = (y % alt) / alt
    return fy < 0.1 + 0.14 * (2 * abs(fa - 0.5)) ** 2

def cor_tronco(p, face):
    x, y, z = p
    a = z if face in ("east", "west") else x
    base = mix(AZUL_FUNDO, AZUL_REAL, clamp((y - 12) / 12))
    if face != "up" and escama(a, y): return tom(base, -0.2)
    return base

def cruz(x, y, cx, cy):
    """Cruz do renascimento (quadro "Símbolo do Renascimento"): cruz latina azul-escura com as pontas alargadas e um
    contorno azul mais claro; devolve a cor ou None."""
    u, v = x - cx, y - cy
    W = 0.5                                    # meia largura do traço
    def dentro(u, v, w):
        haste = abs(u) < w + (0.2 if v < -2.6 or v > 1.9 else 0) and -3.3 < v < 2.5
        braco = abs(v - 0.75) < w + (0.2 if abs(u) > 1.4 else 0) and abs(u) < 1.9
        return haste or braco
    if dentro(u, v, W): return CRUZ
    if dentro(u, v, W + 0.22): return CRUZ_CLARA
    return None

PEITO_Y0, PEITO_Y1 = 17.4, 25.0
def mat_babador(c):
    """Babador azul-claro do peito com a cruz no meio (face da frente)."""
    x, y, z = c["p"]; face = c["face"]
    if face == "north":
        k = cruz(x, y, 0.0, 21.0)
        if k: return k
        cor = mix(BABADOR, claro(BABADOR, 0.05), clamp((y - 18) / 6))
        if escama(x, y, 2.2, 1.6): cor = tom(cor, -0.12)
        return tom(cor, -0.12) if na_borda(c) else cor
    return tom(BABADOR, g.contexto_luz(c, borda=.1))

def mat_dente(c):
    face = c["face"]
    cor = mix(CIANO, AZUL, 0.25) if face != "down" else tom(AZUL, -0.2)
    return tom(cor, -0.18) if na_borda(c) else cor

# --- manto: painéis grossos em degraus ---
MANTO_Y = 25.6                 # altura da raiz dos painéis (sob a gola)
SOBE_CORPO = 3.5               # o corpo todo sobe (pernas à mostra em ~1/3 da altura, como na arte)
MANTO_FIM = 1.2 - SOBE_CORPO   # altura da barra do manto (antes de subir o corpo): arrasta no chão
BORDA = 1.5                    # altura da barra dourada
def glifo_ponta(a, d, n=3):
    """Padrão dourado das PONTAS (quadro "Detalhe do Manto"): 3 blocos em degrau/L subindo na diagonal a partir do
    canto (a = distância do canto ao longo da largura, d = altura acima da barra)."""
    for i in range(n):
        a0, d0 = 0.6 + 2.0 * i, 0.4 + 2.0 * i
        if a0 <= a <= a0 + 1.6 and d0 <= d <= d0 + 0.7: return True          # perna de baixo do L
        if a0 + 0.9 <= a <= a0 + 1.6 and d0 <= d <= d0 + 1.7: return True    # perna de pé do L
    return False

def _dseg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = clamp(((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy + 1e-9))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy)), t

ASA_PONTAS = [(3.9, 3.6), (3.9, 2.3), (3.5, 1.0), (2.8, -0.1)]    # pontas das rêmiges do emblema (lado +u)

def fenix(u, v):
    """Emblema da fênix (quadro "Emblema da Ressurreição"): asas erguidas em V com as rêmiges separadas nas pontas,
    cabeça pequena de perfil no alto, corpo estreito e cauda em 3 chamas; u para o lado, v para cima (~8 x 8)."""
    au = abs(u)
    if au ** 2 + ((v - 2.5) / 1.1) ** 2 <= 0.6 ** 2: return True                         # cabeça
    if -0.95 < u < -0.3 and abs(v - 2.45) < 0.22 - 0.3 * (-0.3 - u): return True         # bico
    if au < 0.4 and 1.4 < v < 2.2: return True                                          # pescoço
    if (au / 0.8) ** 2 + ((v - 0.3) / 1.45) ** 2 <= 1: return True                       # corpo
    if math.hypot(au - 0.7, v - 0.7) < 1.0 and v > -0.2: return True                    # ombro da asa
    for tx, ty in ASA_PONTAS:                                                          # rêmiges
        d, t = _dseg(au, v, 0.7, 0.6, tx, ty)
        if d < 0.5 - 0.22 * t: return True
    for cx_, inc in ((0.0, 0.0), (-0.75, -0.5), (0.75, 0.5)):                           # cauda em 3 chamas
        if -3.9 <= v <= -0.9:
            t = (-0.9 - v) / 3.0
            if abs(u - cx_ * min(1.0, t * 1.6) - inc * t * 0.4) < 0.42 * (1 - t) + 0.1: return True
    return False

def losango_costas(u, v):
    """Os 3 losangos pendentes das costas: moldura dourada e miolo azul-claro; devolve cor ou None."""
    for cx_ in (-3.6, 0.0, 3.6):
        du, dv = abs(u - cx_) / 1.55, abs(v) / 2.9
        d = du + dv
        if d <= 1:
            if d > 0.62: return OURO if (u - cx_) + v > 0 else OURO_ESC
            return CIANO if (u - cx_) < 0.1 else mix(CIANO, AZUL, 0.4)
        if abs(u - cx_) < 0.22 and 2.9 < v < 4.3: return OURO                         # haste do pendente
    return None

ANEL = (6.0, 4.4, 0.0)         # raios x, z e centro z do anel do ombro
FR = (0.36, 0.34, 0.30)        # frações do comprimento de cada degrau
ABRE = (0.0, 1.5, 2.0)         # quanto cada degrau abre a mais que o de cima (caimento quase reto, como na vista lateral)
T_MANTO = 1.5                  # espessura dos painéis
FAIXA = 1.1                    # largura da borda dourada pintada na frente (fina, colada no contorno)

def mat_manto(raiz, L, zc, lado, k, frente_z=None, costas=False, cantos=()):
    """Pintura do painel no referencial dele (antes das rotações): s = distância da raiz, d = distância até a barra,
    a = posição na largura. Face de fora: roxo vivo em cima -> roxo, dobras nas beiradas, faixa dourada FINA só no
    contorno (frente e barra) e padrão em L só nas pontas ('cantos'); forro bem mais escuro."""
    x0, y0, z0 = raiz
    fora = "east" if lado > 0 else "west"
    dentro = "west" if lado > 0 else "east"
    vivo = k % 2 == 0
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        s = y0 - y; d = L - s; a = z - zc
        hw = (c["b"][1][2] - c["b"][0][2]) / 2
        mz = (c["b"][1][2] + c["b"][0][2]) / 2
        aw = abs(z - mz) / max(hw, 1e-6)
        na_frente = frente_z is not None and z - frente_z < FAIXA
        if face == "down": return OURO_ESC
        if face == "up": return OURO_CL if na_frente else ROXO_VIVO
        if face in ("north", "south"):                                   # beiradas (espessura)
            return OURO if (na_frente or d < BORDA) else ROXO_ESC
        ext = face == fora
        if d < BORDA or na_frente:
            cor = OURO if ext else mix(OURO, OURO_ESC, 0.5)
            if (d < BORDA and abs(d - BORDA) < 0.18) or (na_frente and abs(z - frente_z - FAIXA) < 0.18): cor = OURO_ESC
            return cor
        if not ext:
            return tom(ROXO_FUNDO, -0.05 + 0.12 * clamp(1 - s / L))
        if costas:
            ue, ve = a / 1.35, (s - 5.0) / 1.1 * -1     # emblema: centro a 5 da raiz, grande e centrado nas costas
            if abs(ue) < 4.3 and abs(ve) < 4.2 and fenix(ue, ve): return OURO_CL if ve > 1.6 else (OURO if ve > -1.0 else OURO_ESC)
            lc = losango_costas(a, 13.0 - s)
            if lc: return lc
        for zc_, sent, nb in cantos:
            if glifo_ponta((z - zc_) * sent, d - BORDA, nb): return OURO
        base = mix(mix(ROXO_VIVO, ROXO, 0.35), mix(ROXO, ROXO_ESC, 0.3), clamp(s / (L * 0.85)))
        if not vivo: base = mix(base, ROXO_ESC, 0.22)
        base = tom(base, -0.2 * aw ** 2.5)                                  # dobra nas beiradas
        if s < 2.0: base = claro(base, 0.08 * (1 - s / 2.0))
        return base
    return f

def mat_barra(c):
    """Barra dourada em relevo baixo: topo claro, frente ouro, fio escuro em cima e embaixo."""
    face = c["face"]
    if face == "up": return OURO_CL
    if face == "down": return OURO_ESC
    if c["j"] == 0: return OURO_CL
    if c["j"] == c["th"] - 1: return OURO_ESC
    return OURO

def painel(nome, raiz, phi, lado, alvo, W0, W1, k, frente=False, costas=False, ponta=False, fim=None, fenda=0.0):
    """Painel do manto pendurado do ombro, em 3 degraus encadeados (cada um abre ABRE graus a mais), largo e
    contínuo (a massa roxa da arte). 'alvo' = (x para fora, z) onde a barra cai no chão; flare (para fora) e varre
    (para trás) saem daí. A borda dourada da frente é só pintura (faixa fina); 'ponta' afina o último degrau."""
    x, y, z = raiz
    fim = MANTO_FIM if fim is None else fim                  # altura da barra (a de trás sobe: a cauda sai por baixo)
    H = y - fim
    xo = abs(x)
    dx, dz = alvo[0] - xo, alvo[1] - z
    r = math.radians(phi)
    n = (math.cos(r), math.sin(r)); t = (-math.sin(r), math.cos(r))
    dn, dt = dx * n[0] + dz * n[1], dx * t[0] + dz * t[1]
    flare = math.degrees(math.atan2(dn, H)) - sum(ABRE) * 0.55
    varre = math.degrees(math.atan2(dt, math.hypot(H, dn)))
    L = math.sqrt(H * H + dx * dx + dz * dz) * 0.97
    zf = z - W0 / 2 if frente else None
    larg = (W0, (W0 + W1) / 2, W1 * (0.55 if ponta else 1.0))
    cantos = []
    if frente: cantos.append((zf, 1, 3))
    if ponta: cantos += [(z - larg[2] / 2, 1, 2), (z + larg[2] / 2, -1, 2)]
    m = mat_manto(raiz, L, z, lado, k, frente_z=zf, costas=costas, cantos=cantos)
    ys = [y, y - L * FR[0], y - L * (FR[0] + FR[1]), y - L]
    T = T_MANTO
    def bloco(i):
        w = larg[i]
        za, zb = (zf, zf + w) if frente else (z - w / 2, z + w / 2)
        ya, yb = ys[i + 1], ys[i] + (0.35 if i else 0)
        res = 3 if not costas else 4
        if i == 2 and fenda > 0:
            # barra de trás em ARCO (V invertido): 5 faixas lado a lado cuja barra sobe em degraus pequenos e contínuos
            # dos lados para o centro; a borda dourada fina acompanha cada degrau (a cauda sai pelo arco)
            pcs = []; nf = 5; fh = (yb - ya) * 0.5
            for j in range(nf):
                z0_ = za + (zb - za) * j / nf; z1_ = za + (zb - za) * (j + 1) / nf
                u = abs((z0_ + z1_) / 2 - z) / max((zb - za) / 2, 1e-6)
                sobe = fh * (1 - u) ** 0.8
                pcs.append(peca(f"{nome}_{i}_{j}", [x - T / 2, ya + sobe, z0_ - 0.01], [x + T / 2, yb, z1_ + 0.01], m,
                                faixa=(MANTO_FIM, MANTO_Y), res=res))
                pcs.append(peca(f"{nome}_barra{j}", [x - T / 2 - 0.1, ya + sobe - 0.05, z0_], [x + T / 2 + 0.1, ya + sobe + BORDA * 0.6, z1_],
                                mat_barra, res=3))
            return pcs
        pcs = [peca(f"{nome}_{i}", [x - T / 2, ya, za], [x + T / 2, yb, zb], m, faixa=(MANTO_FIM, MANTO_Y), res=res)]
        if i == 2:
            pcs.append(peca(f"{nome}_barra", [x - T / 2 - 0.1, ya - 0.05, za - 0.05], [x + T / 2 + 0.1, ya + BORDA * 0.8, zb + 0.05],
                            mat_barra, res=3))
        if i < 2:
            pcs.append(osso(f"{nome}_d{i + 1}", [x, ys[i + 1], z], [0, 0, ABRE[i + 1] * lado], bloco(i + 1)))
        return pcs
    return osso(nome, list(raiz), [0, -phi * lado, 0], [osso(nome + "_p", list(raiz), [-varre, 0, flare * lado], bloco(0))])

# painéis de cada lado: (phi no anel, alvo da barra (x para fora, z), largura em cima, largura embaixo). O da frente
# nasce no medalhão e cai em diagonal para trás, até atrás do calcanhar (peito e pernas ficam à mostra).
# Os 2 de trás têm a barra mais alta (o último a ~6 do chão): de lado e de costas a cauda sai por baixo da capa.
PAINEIS = [(-62, (11.2, 3.4), 4.6, 7.8, None), (-28, (13.2, 7.6), 5.6, 8.8, None), (8, (13.4, 11.8), 5.8, 8.4, 0.4),
           (42, (12.0, 13.6), 5.6, 8.6, 2.6), (70, (9.0, 14.8), 4.4, 8.2, 5.4)]

def manto_ossos():
    """Manto: painéis largos dos dois lados (o da frente pendurado do medalhão), painel das costas com o emblema e a
    ponta que arrasta no chão, gola enrolada atrás do pescoço, dobras do ombro e o fecho de 2 medalhões."""
    ossos = []
    ax, az, zc = ANEL
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        pcs = []
        for k, (phi, alvo, W0, W1, fim) in enumerate(PAINEIS):
            rx, rz = anel(ax + 0.6 * (k % 2), az + 0.6 * (k % 2), zc, phi, lado)
            if k == 0: rx, rz = 3.9 * lado, -5.2                            # nasce atrás do medalhão
            pcs.append(painel(f"manto{k}_{s}", (rx, MANTO_Y - 0.3 * (k % 2), rz), phi, lado, alvo, W0, W1, k, frente=k == 0, fim=fim))
        ossos.append(osso("manto_" + s, [4.5 * lado, MANTO_Y, 0.0], [0, 0, 0], pcs))
    rx, rz = anel(ax, az, zc, 90, 1)
    ossos.append(osso("manto_costas", [0, MANTO_Y, rz], [0, 0, 0], [
        painel("manto_costas_p", (0.0, MANTO_Y + 0.2, rz + 0.8), 90, 1, (0.0, 16.2), 10.4, 13.0, 2, costas=True, fim=7.0,
               fenda=5.0)]))
    # gola enrolada: rolo grosso atrás e dos lados do pescoço; o ombro cai em diagonal
    mg = mat_cor(lambda p, f_: ROXO_VIVO if f_ == "up" else mix(ROXO_VIVO, ROXO, clamp((29.0 - p[1]) / 4.0)), borda=.1, curva=.3)
    gola = []
    gola += g.arredondado2("gola_tras", [-4.6, 24.0, 1.0], [4.6, 27.4, 4.6], mg, r=1.3, faixa=(24.0, 27.4), res=3)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((1.6 * lado, 4.8 * lado))
        gola.append(osso("gola_lado_" + s, [2.4 * lado, 25.0, 0.6], [0, -48 * lado, 0],
                         g.arredondado("gola_lado_" + s, [x0, 23.4, -2.6], [x1, 26.6, 2.6], mg, r=1.0, faixa=(23.4, 26.6), res=3)))
        x0, x1 = sorted((3.6 * lado, 7.6 * lado))
        gola.append(osso("dobra_" + s, [4.4 * lado, 26.0, 0.0], [0, 0, 34 * lado],
                         g.arredondado2("dobra_" + s, [x0, 22.2, -4.2], [x1, 25.6, 3.6], mg, r=1.2, faixa=(22.2, 25.6), res=3)))
        mx, my, mz = 3.9 * lado, 24.4, -7.6
        mm = mat_medalhao(mx, my)
        med = [peca("medalhao_a_" + s, [mx - 1.45, my - 0.62, mz - 0.3], [mx + 1.45, my + 0.62, mz + 0.6], mm, res=6),
               peca("medalhao_b_" + s, [mx - 0.62, my - 1.45, mz - 0.3], [mx + 0.62, my + 1.45, mz + 0.6], mm, res=6),
               peca("medalhao_d_" + s, [mx - 0.55, my - 0.55, mz - 0.8], [mx + 0.55, my + 0.55, mz], mm, res=6)]
        gola.append(osso("medalhao_" + s, [mx, my, mz], [0, -16 * lado, 0], med))
    ossos.append(osso("gola", [0, 26.0, 0.0], [0, 0, 0], gola))
    return ossos

def mat_medalhao(cx, cy):
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face != "north": return mat_ouro(c)
        r = math.hypot(x - cx, y - cy)
        if r < 0.5: return OURO_CL if (x - cx) + (y - cy) > 0 else OURO
        if r < 0.62: return OURO_ESC
        if r < 1.2: return mix(OURO_CL, OURO, clamp((cy - y + 0.9) / 1.8))
        return OURO_ESC
    return f

# ================= ASAS (sob o manto) =================
def asa_ossos(lado):
    """Asa sob o manto em telha (quadro "Asas Visíveis"): cobertura azul-real no alto e um leque de 6 pares de penas
    grossas (azul-clara por cima, amarela/creme por baixo, sobrepostas 1,5), abrindo para fora; a ponta mais longa
    para acima do joelho (y >= 13,7 depois de subir o corpo)."""
    s = "d" if lado < 0 else "e"
    pcs = []
    for k, phi in enumerate((-46, -14, 18)):
        x, z = anel(5.9, 4.8, 0.0, phi, lado)
        pcs.append(pena(f"asa_cob{k}_{s}", (x, 24.6, z), phi, lado, 6.2, 3.8, P_AZUL, flare=18, T=1.4))
    for k, phi in enumerate((-58, -44, -30, -16, -2, 12)):
        x, z = anel(5.2 + 0.3 * k, 4.6, 0.0, phi, lado)
        pcs.append(pena(f"asa_sec{k}_{s}", (x, 21.6, z), phi, lado, 6.0, 3.0, P_ASA_CLARA, flare=17, T=1.4))
        xa, za = anel(5.5 + 0.3 * k, 4.7, 0.0, phi, lado)
        pcs.append(pena(f"asa_rem{k}_{s}", (xa, 17.3 + 0.3 * (k % 2), za), phi, lado, 5.6, 2.6,
                        P_ASA if k % 2 == 0 else P_ASA_CREME, flare=20, T=1.3))
    return osso("asa_" + s, [4.4 * lado, 24.5, 0.0], [0, 0, 0], pcs)

# ================= CAUDA TRIPLA =================
N_ELOS = 6                     # contas por corrente
PASSO = 3.3                    # distância entre contas (cada conta tem 2,8 de diâmetro: sobra um vão entre elas)
R_CONTA = 1.4

def mat_conta(cy, cz):
    """Conta octogonal dourada vista de lado: aro de ouro com degradê e miolo redondo azul-claro brilhante (com
    reflexo); nas faces finas, só ouro facetado."""
    def f(c):
        face = c["face"]
        if face not in ("east", "west"): return mat_ouro(c)
        x, y, z = c["p"]
        r = math.hypot(y - cy, z - cz)
        if r < 0.72:
            if math.hypot(y - cy - 0.25, z - cz + 0.2) < 0.22: return (240, 255, 255)
            return mix(CIANO, AZUL, clamp((cy - y + 0.4) / 1.4))
        if r < 0.88: return OURO_ESC
        if r > R_CONTA * 0.95: return OURO_ESC
        return mix(OURO_CL, OURO, clamp((cy - y + 0.6) / 1.6))
    return f

def so_gema(c, cor): return cor[2] > 200 and cor[0] < 200

P_LEQUE_AM = [(0, AMAR), (0.6, LIMAO), (1, (255, 246, 196))]
P_LEQUE_AZ = [(0, AZUL_REAL), (0.55, AZUL), (1, CIANO)]

def leque(nome, pos):
    """Leque no fim da corrente: 5 penas pontudas em foice, amarelas com 2 azuis intercaladas no meio, afinando em 3
    segmentos (a ponta com 0,5 de largura) e curvando para cima, sobrepostas em telha."""
    px, py, pz = pos
    pcs = []
    for k, (rx, ry, L, par) in enumerate([(-13, 0, 8.4, P_LEQUE_AM), (-7, 2, 7.2, P_LEQUE_AZ), (-1, -1, 8.8, P_LEQUE_AM),
                                          (5, 2, 6.8, P_LEQUE_AZ), (10, -1, 7.2, P_LEQUE_AM)]):
        segs = [(L * 0.4, 0.9, 3.4), (L * 0.34, 0.85, 2.2), (L * 0.28, 0.75, 0.6)]
        pcs.append(lamina(f"{nome}_pl{k}", (px + 0.2 * (k - 2), py, pz - 0.4), (rx, ry, 0), (-11, 0, 0), segs, par, eixo="z"))
    # nó dourado de onde o leque sai
    pcs.append(peca(f"{nome}_no", [px - 0.9, py - 0.9, pz - 0.7], [px + 0.9, py + 0.9, pz + 0.9], mat_ouro, res=3))
    return pcs

def corrente(nome, base, rot0, curvas, n_elos=None):
    n_elos = n_elos or len(curvas) + 1
    """Corrente de contas (um osso por conta, '<nome>_k', cresce em +z e dobra 'curva' graus a cada junta: com rot0
    para cima e curva positiva ela faz um arco que sobe e depois desce); o leque fica no osso '<nome>_leque'."""
    def seg(k, pos):
        px, py, pz = pos
        cz = pz + PASSO / 2; R = R_CONTA; r = R * 0.57; e = 0.6
        m = mat_conta(py, cz)
        filhos = [peca(f"{nome}_{k}", [px - e, py - R, cz - r], [px + e, py + R, cz + r], m, res=5, brilho=so_gema),
                  peca(f"{nome}_{k}b", [px - e, py - r, cz - R], [px + e, py + r, cz + R], m, res=5, brilho=so_gema)]
        if k + 1 < n_elos:
            filhos.append(seg(k + 1, (px, py, pz + PASSO)))
        else:
            p2 = (px, py, pz + PASSO)
            giro = -(rot0[0] + sum(curvas[:n_elos - 1])) + ANGULO_LEQUE   # o leque continua caindo para trás
            filhos.append(osso(f"{nome}_leque", list(p2), [giro, 0, 0], leque(nome, p2)))
        return osso(f"{nome}_{k}", list(pos), list(rot0) if k == 0 else [curvas[k - 1], 0, 0], filhos)
    return seg(0, tuple(base))

# arcos que sobem e descem; saem perto do meio das costas, abaixo do emblema, e abrem para o lado +x (as 3 aparecem
# na 3/4 da arte)
# Cauda tripla do pedido do dono: nasce baixa, na base traseira do corpo (o "uropígio", logo acima do quadril), por
# baixo da capa, e as 3 correntes DESCEM com leve curva para trás e um leque estreito para os lados (-10°, 0°, +10°);
# saem por baixo da barra de trás (que sobe e abre em fenda) e os leques param perto do chão. Dobras positivas = desce.
RAIZ_CAUDA = (0.0, 12.8, 4.0)
CORRENTES = [("cauda1", (-1.4, 12.8, 4.2), (42, -24, 0), [-2, -3, -3, -3, -3]), ("cauda2", (0.0, 11.4, 4.6), (34, 0, 0), [-4, -5, -6]),
             ("cauda3", (1.4, 12.8, 4.2), (42, 24, 0), [-2, -3, -3, -3, -3])]
ANGULO_LEQUE = 30              # o leque segue descendo para trás (graus abaixo da horizontal)
ONDAS = [(n, len(c) + 1, (2.0, 1.5, 2.5)) for n, _, _, c in CORRENTES]       # balanço suave de pendente (como as contas do Pirococó)
ANIM_PARADO = {
    "manto_d": [(0, 0, 0), (1.5, 0, -1.2), (0, 0, 0), (-1, 0, 0.8), (0, 0, 0)],
    "manto_e": [(0, 0, 0), (1.5, 0, 1.2), (0, 0, 0), (-1, 0, -0.8), (0, 0, 0)],
    "manto_costas": [(0, 0, 0), (2, 0, 0), (0, 0, 0), (-1, 0, 0), (0, 0, 0)],
    **{f"{n}_leque": [(0, 0, 0), (4, 0, 6 * s_), (0, 0, 0), (-4, 0, -6 * s_), (0, 0, 0)]
       for (n, _, _, _), s_ in zip(CORRENTES, (1, -1, 1))},
}
# andar de ave: quadril ±18°, o tarso dobra para trás no passo e a pata fica plana no apoio (não afunda no chão)
_PASSO_D = {"perna": [18, 0, -18, 0, 18], "tarso": [-4, -4, 0, -16, -4], "pata": [-14, 4, 18, 10, -14]}
ANIM_ANDANDO_PERNAS = {}
for _osso, _seq in _PASSO_D.items():
    ANIM_ANDANDO_PERNAS[f"{_osso}_d"] = [(v, 0, 0) for v in _seq]
    _e = _seq[2:4] + _seq[0:3]                      # perna esquerda meio ciclo defasada
    ANIM_ANDANDO_PERNAS[f"{_osso}_e"] = [(v, 0, 0) for v in _e]
ANIM_ANDANDO = {
    **ANIM_ANDANDO_PERNAS,
    "manto_d": [(0, 0, 0), (4, 0, -2), (0, 0, 0), (4, 0, -2), (0, 0, 0)],
    "manto_e": [(0, 0, 0), (4, 0, 2), (0, 0, 0), (4, 0, 2), (0, 0, 0)],
    "manto_costas": [(0, 0, 0), (6, 0, 0), (0, 0, 0), (6, 0, 0), (0, 0, 0)],
    **{f"{n}_leque": [(0, 0, 0), (8, 0, 10 * s_), (0, 0, 0), (-8, 0, -10 * s_), (0, 0, 0)]
       for (n, _, _, _), s_ in zip(CORRENTES, (1, -1, 1))},
}

# ================= PERNAS =================
def cor_perna(p, face):
    if face == "down": return AMAR_ESC
    if face != "up" and (p[1] % 1.15) < 0.16: return mix(AMAR, AMAR_ESC, 0.55)      # anéis de escama
    return AMAR

def perna(lado):
    """Perna: coxa azul (sob a barriga) + canela de cima no osso da perna; tornozelo e canela de baixo no osso
    'tarso_*' (dobra no andar); pé e dedos no osso 'pata_*' (fica plano no chão no apoio)."""
    s = "d" if lado < 0 else "e"; xc = 2.6 * lado; zc = -1.0
    S = SOBE_CORPO
    ma = mat_cor(cor_perna, borda=.08, curva=.3)
    pp = []
    pp += g.arredondado("coxa_" + s, [xc - 2.0, 12.0 + S, zc - 2.2], [xc + 2.0, 15.4 + S, zc + 2.0],
                        mat_cor(lambda p, f_: mix(AZUL_FUNDO, AZUL_REAL, clamp((p[1] - 12.0 - S) / 3.4)), borda=.0, curva=.3), r=0.8, res=2)
    pp += g.octogono("tarso_cima_" + s, [xc - 1.5, 6.8, zc - 1.5], [xc + 1.5, 12.6 + S, zc + 1.5], ma, r=0.45, faixa=(1.5, 14.0))
    ta = []
    ta += g.arredondado("tornozelo_" + s, [xc - 1.65, 5.9, zc - 1.65], [xc + 1.65, 7.5, zc + 1.65], ma, r=0.45, faixa=(1.5, 14.0))
    ta += g.octogono("tarso_baixo_" + s, [xc - 1.3, 1.6, zc - 1.3], [xc + 1.3, 6.4, zc + 1.3], ma, r=0.4, faixa=(1.5, 14.0))
    mpe = mat_cor(lambda p, f_: BICO_CL if f_ == "up" else (AMAR_ESC if f_ == "down" else AMAR), borda=.14, curva=.35)
    mg = mat_cor(lambda p, f_: (90, 84, 100) if f_ == "up" else GARRA, borda=.1, curva=.2)
    pa = [peca("pe_" + s, [xc - 1.9, 0, zc - 1.9], [xc + 1.9, 2.0, zc + 1.5], mpe, faixa=(0, 2.0), res=2)]
    for nome, giro, dx, comp in (("meio", 0, 0, 5.0), ("fora", -24 * lado, 1.4 * lado, 4.2), ("dentro", 22 * lado, -1.4 * lado, 4.0)):
        x0, z0 = xc + dx, zc - 1.2
        pa.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
            peca(f"dedo_{nome}_{s}", [x0 - .85, 0, z0 - comp], [x0 + .85, 1.8, z0 + 0.3], mpe, faixa=(0, 1.8), res=2),
            peca(f"garra_{nome}_{s}", [x0 - .7, 0.0, z0 - comp - 1.4], [x0 + .7, 1.5, z0 - comp + 0.2], mg,
                 rot=(-10, 0, 0), pivo=(x0, 1.5, z0 - comp + 0.2), faixa=(0, 1.5), res=2)]))
    pa.append(peca("dedo_tras_" + s, [xc - .7, 0, zc + 1.2], [xc + .7, 1.4, zc + 3.4], mpe, faixa=(0, 1.4), res=2))
    pa.append(peca("garra_tras_" + s, [xc - .55, 0, zc + 3.3], [xc + .55, 1.1, zc + 4.3], mg, faixa=(0, 1.1), res=2))
    ta.append(osso("pata_" + s, [xc, 1.8, zc], [0, 0, 0], pa))
    pp.append(osso("tarso_" + s, [xc, 6.7, zc], [0, 0, 0], ta))
    return osso("perna_" + s, [xc, 14.0 + S, zc], [0, 0, 0], pp)

# ================= LOD =================
# Peças estruturais nunca somem de longe (senão sobram cubos soltos): crânio, tronco, barriga, pescoço, coxa, tarso,
# tornozelo, pé, dedo do meio, contas da cauda e manto. Quem some leva junto a ponta '_pt' da mesma pena.
import json as _json, re as _re
ESTRUTURA = _re.compile(r"^(bico|barbela|cranio|tronco|barriga|quilha|pescoco|coxa|tarso|tornozelo|pe_|dedo_|garra_|faceta|cranio_frente|"
                        r"cauda\d_\d|manto|gola|babador_\d|medalhao)")

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
    # o corpo de uma pena nunca some antes da ponta (a ponta soltaria no ar)
    for nome, n in list(nivel_de.items()):
        if not nome.endswith("_pt"):
            pt = nome + "_pt"
            if nivel_de.get(pt, 99) > n: nivel_de[pt] = n
    out = {}
    for nome, n in nivel_de.items(): out.setdefault(n, []).append(nome)
    return {n: ["^(?:" + "|".join(_re.escape(x) for x in sorted(v)) + ")$"] for n, v in sorted(out.items())}

LODS = _lods_filtrados()

# ================= MONTAGEM =================
K_CAB, SOBE_CAB = 0.8, 1.5     # cabeça 20% menor (o dono: "cabeça muito grande") e mais alta: pescoço à mostra
CENTRO_CAB = (0.0, 29.0, -3.0)

def escalar(nos, centro, k):
    """Como g.transformar, mas só para as peças e ossos da lista 'nos' (e tudo o que estiver dentro deles)."""
    pecas = {pc.uuid: pc for pc in g.PECAS}
    def visita(no):
        if isinstance(no, str):
            pc = pecas[no]
            for arr in (pc.de, pc.ate, pc.pivo):
                for i in range(3): arr[i] = centro[i] + (arr[i] - centro[i]) * k
            pc.pintas.append((tuple(centro), k, 0.0))
        else:
            o = no["origin"]
            for i in range(3): o[i] = centro[i] + (o[i] - centro[i]) * k
            for f in no["children"]: visita(f)
    for no in nos: visita(no)

ROT_PESC = -10         # pescoço curvo para a frente; a cabeça compensa e olha reto
def montar():
    i0 = len(g.PECAS)
    corpo = []
    mt = mat_cor(cor_tronco, borda=.0, curva=.3)
    corpo += g.arredondado2("tronco", [-5.0, 13.0, -6.9], [5.0, 26.4, 4.0], mt, r=2.0, faixa=(12, 26.4), res=2)
    # barriga de verdade: fecha o corpo atrás das penas do peito (sem "saia" oca)
    corpo += g.arredondado("barriga", [-3.8, 11.2, -6.4], [3.8, 14.6, 1.4], mt, r=1.0, faixa=(11, 15), res=2)
    # quilha do peito (o peito estufa) e babador em escudo de 3 degraus, inclinado com o topo para a frente
    corpo += g.arredondado("quilha", [-2.6, 16.0, -7.6], [2.6, 22.6, -5.8], mt, r=0.8, res=2)
    bab = []
    for k, (y0, y1, w) in enumerate(((21.4, 25.0, 3.3), (19.0, 21.6, 2.5), (17.2, 19.2, 1.5))):
        bab.append(peca(f"babador_{k}", [-w, y0, -8.2], [w, y1, -6.4], mat_babador, res=6))
    for k, (x, y) in enumerate(((-1.6, 19.0), (0.0, 17.2), (1.6, 19.0))):
        q = 1.6 / 1.4142
        bab.append(peca(f"babador_ponta{k}", [x - q / 2, y - q / 2, -8.1], [x + q / 2, y + q / 2, -6.5], mat_dente,
                        rot=(0, 0, 45), pivo=(x, y, -7.3), res=4))
    corpo.append(osso("babador", [0, 17.2, -7.3], [-10, 0, 0], bab))
    # peito: penas em telha em 3 fileiras (azul-real, azul-claro, azul com ponta clara), terminando acima do joelho
    for k, (x, y, z, L, W, fl, par) in enumerate([(-4.7, 19.8, -6.6, 5.2, 3.4, 12, P_AZUL), (-1.4, 19.4, -7.4, 5.0, 3.0, 8, P_AZUL),
                                                  (1.4, 19.4, -7.4, 5.0, 3.0, 8, P_AZUL), (4.7, 19.8, -6.6, 5.2, 3.4, 12, P_AZUL),
                                                  (-2.8, 17.2, -7.1, 4.8, 3.2, 12, P_PEITO_CLARO), (0.0, 17.0, -7.4, 4.8, 3.2, 12, P_PEITO_CLARO),
                                                  (2.8, 17.2, -7.1, 4.8, 3.2, 12, P_PEITO_CLARO),
                                                  (-4.0, 15.2, -6.3, 4.2, 2.8, 18, P_FRANJA), (-1.4, 14.9, -6.9, 4.2, 2.8, 16, P_FRANJA),
                                                  (1.4, 14.9, -6.9, 4.2, 2.8, 16, P_FRANJA), (4.0, 15.2, -6.3, 4.2, 2.8, 18, P_FRANJA)]):
        corpo.append(pena(f"peito{k}", (x, y, z), -90, 1, L, W, par, flare=fl, T=1.2))
    # pescoço fino (60% da cabeça), curvo para a frente, com penas em telha encostadas (sem cards espetados)
    def cor_pesc(p, f_):
        x, y, z = p
        a = z if f_ in ("east", "west") else x
        base = mix(AZUL_REAL, AZUL, 0.55) if (f_ == "north" or z < -3.0) else AZUL_REAL
        return tom(base, -0.16) if escama(a, y, 1.8, 1.3) else base
    mp = mat_cor(cor_pesc, borda=.0, curva=.3)
    mpp = mat_cor(lambda p, f_: mix(AZUL_REAL, AZUL, clamp((p[1] - 26) / 6)) if f_ != "down" else AZUL_FUNDO, borda=.12, curva=.3)
    pesc = []
    pesc += g.octogono("pescoco_base", [-1.7, 23.4, -3.4], [1.7, 28.6, 0.6], mp, r=0.6, faixa=(23, 33))
    alto = g.octogono("pescoco_alto", [-1.4, 27.2, -3.6], [1.4, 31.4, -0.2], mp, r=0.5, faixa=(23, 33))
    # colar de penas em telha (como no Pirococó): sai de baixo da cabeça e cai sobre a gola, dos lados e por trás;
    # cobre a base do pescoço (só ~7% de pescoço à mostra)
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        for k, (phi, L) in enumerate(((-40, 4.6), (15, 5.4), (62, 5.4))):
            x, z = anel(1.6, 1.9, -1.9, phi, lado)
            alto.append(pena(f"colar{k}_{s_}", (x, 30.8 - 0.3 * (k % 2), z), phi, lado, L, 3.2, P_PESC, flare=46, T=1.1))
    alto.append(pena("colar_tras", (0, 30.8, 0.0), 90, 1, 5.6, 3.4, P_PESC, flare=46, T=1.1))
    pesc.append(osso("pescoco_alto", [0, 28.0, -1.0], [-12, 0, 0], alto))
    i_cab = len(g.PECAS)
    cab = cabeca_ossos()
    # bico e barbela mantêm o tamanho absoluto (crescem 1/K_CAB em volta da base do bico antes de a cabeça encolher)
    pecas = {pc.uuid: pc for pc in g.PECAS[i_cab:]}
    bico = [n for n in cab if (isinstance(n, str) and pecas[n].nome.startswith(("bico", "barbela")))
            or (isinstance(n, dict) and n["name"].startswith("barbela"))]
    escalar(bico, (0.0, 30.9, ZF), 1.0 / K_CAB)
    g.transformar(i_cab, cab, CENTRO_CAB, k=K_CAB, sobe=SOBE_CAB)
    oc = [CENTRO_CAB[i] + (v - CENTRO_CAB[i]) * K_CAB for i, v in enumerate((0, 30.4, -2.4))]; oc[1] += SOBE_CAB
    pesc.append(osso("cabeca", oc, [-ROT_PESC, 0, 0], cab))
    corpo.append(osso("pescoco", [0, 25.0, -1.0], [ROT_PESC, 0, 0], pesc))
    corpo += manto_ossos()
    corpo.append(asa_ossos(-1)); corpo.append(asa_ossos(1))
    corpo.append(osso("cauda", list(RAIZ_CAUDA), [0, 0, 0], [corrente(n, b, r, c) for n, b, r, c in CORRENTES]))
    g.transformar(i0, [o for o in corpo if isinstance(o, dict)], (0.0, 0.0, 0.0), sobe=SOBE_CORPO)
    tronco = osso("corpo", [0, 14.0 + SOBE_CORPO, 0.0], [0, 0, 0], corpo)
    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

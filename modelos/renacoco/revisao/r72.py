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
P_CRISTA = [(0, CIANO), (0.14, (251, 217, 102)), (0.7, (253, 224, 110)), (1, (255, 227, 106))]
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
def mat_pena_cor(paradas, y0, L, zc, W, claro_lado=-1, sombra=None):
    """Pena em bloco: degradê da raiz à ponta, metade clara e metade base na face larga (pena dobrada) com raque
    clara; contorno escuro só nas beiradas compridas; espessura em sombra. 'sombra' = cor para onde a sombra puxa
    (ex.: azul nas penas azul-claras, para não acinzentar)."""
    esc = (lambda c, f: mix(c, sombra, min(1.0, f * 1.6))) if sombra else escurece
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        t = clamp((y0 - y) / max(L, 1e-6))
        base = grad(paradas, t)
        if face in ("east", "west"):
            u = (z - zc) / (W / 2)
            cor = claro(base, 0.08) if u * claro_lado > 0 else esc(base, 0.08)
            if abs(u) < 0.08 and t < 0.85: cor = claro(cor, 0.08)
            if t < 0.1: cor = esc(cor, 0.18)
            if c["nome"].endswith("_pt"):
                if na_borda(c): cor = esc(cor, 0.25)
            elif c["i"] in (0, c["tw"] - 1): cor = esc(cor, 0.25)
            return cor
        if face == "up": return claro(base, 0.06)
        if face == "down": return esc(base, 0.4)
        return esc(base, 0.18)
    return f

def pena(nome, raiz, phi, lado, L, W, paradas, flare=20, varre=0, T=0.9, brilho=False, claro_lado=-1, sombra=None):
    """Pena grossa pendurada da raiz: corpo + ponta em losango. phi = ângulo em volta do corpo (0 = para fora,
    -90 = frente, +90 = trás); flare abre a ponta para fora; varre puxa a ponta para trás."""
    x, y, z = raiz
    Lb = L - W * 0.5
    s = W / 1.4142
    m = mat_pena_cor(paradas, y, L, z, W, claro_lado, sombra)
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
    return (244, 244, 244) if topo - v > 0.35 else (226, 230, 238)

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return mix(AZUL, CIANO, 0.3)                           # topo da cabeça no azul (sem "boné")
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
    cab += g.arredondado("cranio_frente", [-FRENTE_X - 0.4, CAB_Y0 + 0.3, ZF], [FRENTE_X + 0.4, CAB_Y1 - 1.6, ZL + 0.4], mc, r=0.6, faixa=fx, res=3)
    # testa inclinada: desce do alto do crânio até a base do bico (a cabeça afina para a frente)
    cab.append(peca("testa", [-FRENTE_X - 0.2, CAB_Y1 - 2.0, ZF + 0.2], [FRENTE_X + 0.2, CAB_Y1 - 0.6, ZL + 1.6], mc,
                    rot=(-24, 0, 0), pivo=(0, CAB_Y1 - 0.6, ZL + 1.6), faixa=fx, res=3))
    # queixo/garganta: volume claro que afina para trás embaixo do bico
    cab += g.arredondado("queixo", [-2.4, 28.2, ZF + 0.9], [2.4, 30.4, ZL + 3.6],
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
        for k, (y, z, L, h, par, rx) in enumerate([(30.6, -3.2, 6.6, 2.4, P_CIANO, -24), (32.2, -3.0, 7.2, 2.6, P_AZUL2, -28),
                                                   (33.8, -2.8, 6.8, 2.6, P_CRISTA, -32)]):
            segs = [(L * 0.42, 1.6, h), (L * 0.33, 1.3, h * 0.7), (L * 0.27, 1.0, h * 0.4)]
            cab.append(lamina(f"rosto{k}_{s}", ((LX + 0.1) * lado, y, z), (rx, 25 * lado, 0), (6, 0, 0), segs, par, eixo="z"))
    # nuca: 2 penas largas que descem do alto de trás da cabeça sobre o colar (sem degrau entre cabeça e pescoço)
    cab.append(pena("nuca0", (0.0, 33.6, 1.0), 90, 1, 3.75, 3.6, P_PESC, flare=16, T=1.1))
    cab.append(crista_ossos())
    return cab

# crista em chama: plumas amarelas largas que sobem e varrem para trás em leque, com base azul-clara
# crista em chama: 7 penas abertas em leque também DE FRENTE (roll escalonado), as 5 da frente quase verticais e as 2
# de trás deitando para trás; afilam até a ponta, sem palitos; base azul-clara
CRISTA = [  # (x, z da raiz, inclinação para trás, abertura lateral)
    (0.0, -2.2, 12, 0), (1.25, -2.6, 8, -12), (-1.25, -2.6, 8, 12), (2.4, -1.6, 20, -24), (-2.4, -1.6, 20, 24),
    (3.2, 0.4, 45, -36), (-3.2, 0.4, 45, 36),
]

def crista_ossos():
    pc = []
    pc.append(peca("crista_base", [-2.0, 34.4, -4.0], [2.0, 35.8, 1.2],
                   mat_cor(lambda p, f_: CIANO if f_ != "down" else AZUL, borda=.0, curva=.25), res=3))
    for k, (x, z, rx, rz) in enumerate(CRISTA):
        esc = 1.0 if k == 0 else 0.94
        segs = [(3.75 * esc, 2.6, 2.0), (3.1 * esc, 1.9, 1.5), (2.5 * esc, 1.1, 1.0)]     # afilam 2,0 -> 1,5 -> 1,0 (antes da escala 0,8)
        pc.append(lamina(f"crista{k}", (x, 35.4, z), (rx, 0, rz), (8, 0, 0), segs, P_CRISTA, eixo="y"))
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

def cruz(x, y, cx, cy, k=1.0):
    """Cruz do renascimento (quadro "Símbolo do Renascimento"): cruz latina azul-escura com as pontas alargadas e um
    contorno azul mais claro; devolve a cor ou None."""
    u, v = (x - cx) / k, (y - cy) / k
    W = 0.55                                   # meia largura do traço
    def dentro(u, v, w):
        haste = abs(u) < w + 0.32 * clamp((abs(v - 0.75) - 1.3) / 1.4) and -3.3 < v < 2.5      # pontas alargadas
        braco = abs(v - 0.75) < w + 0.32 * clamp((abs(u) - 0.8) / 1.0) and abs(u) < 1.95
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

ESCUDO = [(184, 230, 247), (150, 214, 248), (118, 198, 246)]     # azul-claro -> azul-claro mais saturado embaixo

def mat_escudo(fila, cruz_c=None):
    """Fileira do escudo de penas do peito: azul-claro chapado na frente com escamas de pena suaves (linha azulada,
    nada de cinza), beiradas puxando para o azul; a fileira de cima leva a cruz."""
    base = ESCUDO[fila]
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face == "north":
            if cruz_c:
                kk = cruz(x, y, cruz_c[0], cruz_c[1], cruz_c[2])
                if kk: return kk
            cor = claro(base, 0.05 * clamp((y - c["b"][0][1]) / 3))
            if escama(x + 0.6 * fila, y, 1.9, 1.5): cor = mix(cor, AZUL, 0.12)
            if na_borda(c): cor = mix(cor, AZUL, 0.22)
            return cor
        if face == "up": return claro(base, 0.06)
        if face == "down": return mix(base, AZUL_REAL, 0.45)
        return mix(base, AZUL, 0.3)
    return f

PEITILHO = (166, 221, 245); PEITILHO_CL = (205, 239, 252); PEITO_LADO = (63, 164, 232)
CRUZ2 = (30, 42, 140); CRUZ2_BORDA = (59, 87, 200)

def cruz_latina(u, v):
    """Cruz latina (3,0 x 4,5): haste vertical inteira, braço horizontal a 1/3 do topo, pontas alargadas 1 texel.
    u para o lado, v para baixo a partir do topo."""
    def dentro(w):
        haste = abs(u) < w + (0.17 if (v < 0.45 or v > 4.05) else 0) and 0 <= v <= 4.5
        braco = abs(v - 1.5) < w + (0.17 if abs(u) > 1.05 else 0) and abs(u) <= 1.5
        return haste or braco
    if dentro(0.375): return CRUZ2
    if dentro(0.375 + 0.2): return CRUZ2_BORDA
    return None

def mat_peitilho(cx, ytopo_cruz):
    """Pena central do peitilho: azul-claro sem cinza, com a cruz latina no terço de cima."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face == "north":
            k = cruz_latina(x - cx, ytopo_cruz - y)
            if k: return k
            cor = mix(PEITILHO, PEITILHO_CL, clamp((y - 20.5) / 4.5))
            return mix(cor, PEITO_LADO, 0.25) if na_borda(c) else cor
        if face == "up": return PEITILHO_CL
        if face == "down": return mix(PEITILHO, PEITO_LADO, 0.5)
        return mix(PEITILHO, PEITO_LADO, 0.35)
    return f

def pena_lisa(nome, raiz, L, W, T, flare, fila):
    """Pena do peitilho virada para a frente: azul-claro liso (#CDEFFC em cima -> #A6DDF5), beirada azulada, ponta
    em losango; sem metades nem raque (nada de listras)."""
    x, y, z = raiz
    base = mix(PEITILHO_CL, PEITILHO, 0.3 * fila)
    def m(c):
        face = c["face"]
        if face == "north":
            cor = mix(base, PEITILHO, clamp((y - c["p"][1]) / L))
            return mix(cor, PEITO_LADO, 0.3) if na_borda(c) else cor
        if face == "up": return PEITILHO_CL
        return mix(base, PEITO_LADO, 0.45 if face == "down" else 0.3)
    Lb = L - W * 0.5; q = W / 1.4142
    corpo = peca(nome, [x - W / 2, y - Lb, z - T / 2], [x + W / 2, y, z + T / 2], m, res=4)
    ponta = peca(nome + "_pt", [x - q / 2, y - Lb - q / 2, z - T / 2 + 0.03], [x + q / 2, y - Lb + q / 2, z + T / 2 - 0.03], m,
                 rot=(0, 0, 45), pivo=(x, y - Lb, z), res=4)
    return osso(nome, list(raiz), [-flare, 0, 0], [corpo, ponta])

def mat_dente(c):
    face = c["face"]
    cor = mix(CIANO, AZUL, 0.25) if face != "down" else tom(AZUL, -0.2)
    return tom(cor, -0.18) if na_borda(c) else cor

# --- manto: painéis grossos em degraus ---
MANTO_Y = 24.2                 # altura da raiz dos painéis (começam por dentro do capelete)
SOBE_CORPO = 3.5               # o corpo todo sobe (pernas à mostra em ~1/3 da altura, como na arte)
MANTO_FIM = 1.2 - SOBE_CORPO   # altura da barra do manto (antes de subir o corpo): arrasta no chão
BORDA = 1.8                    # altura da barra dourada
def glifo_ponta(a, d, n=2):
    """Padrão dourado das PONTAS (quadro "Detalhe do Manto"): blocos grandes em degrau/L (~2,4 x 2,6 cada) subindo na
    diagonal a partir do canto (a = distância do canto ao longo da largura, d = altura acima da barra)."""
    for i in range(n):
        a0, d0 = 0.5 + 2.8 * i, 0.4 + 2.6 * i
        if a0 <= a <= a0 + 2.4 and d0 <= d <= d0 + 0.9: return True          # perna de baixo do L
        if a0 + 1.4 <= a <= a0 + 2.4 and d0 <= d <= d0 + 2.6: return True    # perna de pé do L
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
    for cx_ in (-2.9, 0.0, 2.9):
        du, dv = abs(u - cx_) / 1.25, abs(v) / 2.6
        d = du + dv
        if d <= 1:
            if d > 0.62: return OURO if (u - cx_) + v > 0 else OURO_ESC
            return CIANO if (u - cx_) < 0.1 else mix(CIANO, AZUL, 0.4)
        if abs(u - cx_) < 0.22 and 2.6 < v < 3.9: return OURO                         # haste do pendente
    return None

ANEL = (6.0, 4.4, 0.0)         # raios x, z e centro z do anel do ombro
FR = (0.36, 0.34, 0.30)        # frações do comprimento de cada degrau
ABRE = (0.0, 1.5, 2.0)         # quanto cada degrau abre a mais que o de cima (caimento quase reto, como na vista lateral)
T_MANTO = 1.5                  # espessura dos painéis
FAIXA = 1.1                    # largura da borda dourada pintada na frente (fina, colada no contorno)

def mat_manto(raiz, L, zc, lado, k, frente_z=None, costas=False, cantos=(), arco=0.0):
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
        na_arco = arco > 0 and d < BORDA + arco and (c["b"][1][2] - z) < 1.1     # contorno dourado do arco de trás
        if d < BORDA or na_frente or na_arco:
            cor = OURO if ext else mix(OURO, OURO_ESC, 0.5)
            if (d < BORDA and abs(d - BORDA) < 0.18) or (na_frente and abs(z - frente_z - FAIXA) < 0.18): cor = OURO_ESC
            return cor
        if not ext:
            return tom(ROXO_FUNDO, -0.05 + 0.12 * clamp(1 - s / L))
        if costas:
            ue, ve = a / 1.35, (s - 5.0) / 1.1 * -1     # emblema: centro a 5 da raiz, grande e centrado nas costas
            if abs(ue) < 4.3 and abs(ve) < 4.2 and fenix(ue, ve): return OURO_CL if ve > 1.6 else (OURO if ve > -1.0 else OURO_ESC)
            lc = losango_costas(a, 11.6 - s)
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

def painel(nome, raiz, phi, lado, alvo, W0, W1, k, frente=False, costas=False, fim=None, abre=None, arco=0.0, dobra=0.8):
    """Painel do manto pendurado do ombro, em 3 degraus encadeados (cada um abre 'abre' graus a mais), largo e
    contínuo. 'alvo' = (x para fora, z) onde a barra cai; flare (para fora) e varre (para trás) saem daí. O último
    degrau volta a ficar a prumo (desfaz a varrida): a barra fica HORIZONTAL, numa altura só. A frente leva a faixa
    dourada fina pintada; 'arco' pinta a faixa dourada subindo pela beirada do lado do centro (contorno do arco de
    trás) até essa altura. 'dobra' = profundidade da 2ª dobra (o painel tem 2 dobras largas alternadas)."""
    x, y, z = raiz
    fim = MANTO_FIM if fim is None else fim
    H = y - fim
    xo = abs(x)
    dx, dz = alvo[0] - xo, alvo[1] - z
    r = math.radians(phi)
    n = (math.cos(r), math.sin(r)); t = (-math.sin(r), math.cos(r))
    dn, dt = dx * n[0] + dz * n[1], dx * t[0] + dz * t[1]
    abre = abre or ABRE
    flare = math.degrees(math.atan2(dn, H)) - sum(abre) * 0.55
    varre = math.degrees(math.atan2(dt, math.hypot(H, dn)))
    L = math.sqrt(H * H + dx * dx + dz * dz) * 0.97
    zf = z - W0 / 2 if frente else None
    larg = (W0, (W0 + W1) / 2, W1)
    cantos = []
    if frente: cantos.append((zf, 1, 2))
    m = mat_manto(raiz, L, z, lado, k, frente_z=zf, costas=costas, cantos=cantos, arco=arco)
    ys = [y, y - L * FR[0], y - L * (FR[0] + FR[1]), y - L]
    T = T_MANTO
    def bloco(i):
        w = larg[i]
        za, zb = (zf, zf + w) if frente else (z - w / 2, z + w / 2)
        ya, yb = ys[i + 1], ys[i] + (0.35 if i else 0)
        res = 3 if not costas else 4
        # 2 dobras largas lado a lado, a 2ª mais funda (alterna a profundidade)
        zm = za + w * 0.5; dx_ = dobra * lado * (1 if k % 2 == 0 else -1)
        pcs = [peca(f"{nome}_{i}", [x - T / 2, ya, za], [x + T / 2, yb, zm + 0.02], m, faixa=(MANTO_FIM, MANTO_Y), res=res),
               peca(f"{nome}_{i}b", [x - T / 2 + dx_, ya, zm], [x + T / 2 + dx_, yb, zb], m, faixa=(MANTO_FIM, MANTO_Y), res=res)]
        if i == 2:
            # barra: friso dourado baixo e contínuo (saliência 0,15; passa 0,4 de cada lado para encostar nas vizinhas)
            pcs.append(peca(f"{nome}_barra", [x - T / 2 - 0.12 + min(dx_, 0), ya - 0.05, za - 0.12],
                            [x + T / 2 + 0.12 + max(dx_, 0), ya + BORDA, zb + 0.12], mat_barra, res=3))
        if i < 2:
            # o último degrau desfaz a varrida (fica a prumo): barra horizontal
            giro = [varre if i == 1 else 0, 0, abre[i + 1] * lado]
            pcs.append(osso(f"{nome}_d{i + 1}", [x, ys[i + 1], z], giro, bloco(i + 1)))
        return pcs
    return osso(nome, list(raiz), [0, -phi * lado, 0], [osso(nome + "_p", list(raiz), [-varre, 0, flare * lado], bloco(0))])

# painéis de cada lado (4 dobras largas): (phi no anel, alvo da barra (x para fora, z), largura em cima, embaixo,
# altura da barra no mundo). Frente e lados rentes ao chão; atrás a barra sobe num arco de 3 degraus (4 / 7,5 / 11)
# por onde sai a cauda.
PAINEIS = [(-62, (12.2, 7.6), 5.0, 7.6, 0.5), (4, (14.2, 10.0), 6.6, 9.6, 0.5), (40, (11.8, 15.4), 6.4, 9.6, 4.0),
           (70, (8.2, 17.0), 5.0, 6.2, 7.5)]

def mat_capelete(ybaixo):
    """Capelete: roxo vivo em cima -> roxo, com o friso dourado fino (0,6) na beirada de baixo da camada de baixo."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if ybaixo is not None and face != "up" and y - ybaixo < 0.6: return OURO if face != "down" else OURO_ESC
        if face == "up": return ROXO_VIVO
        if face == "down": return ROXO_ESC
        return luz(mix(ROXO_VIVO, ROXO, clamp((27.0 - y) / 4.0)), g.contexto_luz(c, borda=.1, curva=.3))
    return f

def manto_ossos():
    """Manto em "A": 4 painéis largos por lado (o da frente pendurado do medalhão, em linha reta até a bainha),
    painel das costas com o emblema e o topo do arco da cauda, capelete de 2 camadas em rampa no ombro, capuz roxo
    atrás do pescoço e o fecho de 2 medalhões octogonais no topo do peitilho."""
    ossos = []
    ax, az, zc = ANEL
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        pcs = []
        for k, (phi, alvo, W0, W1, fim_m) in enumerate(PAINEIS):
            rx, rz = anel(ax + 0.6 * (k % 2), az + 0.6 * (k % 2), zc, phi, lado)
            if k == 0: rx, rz = 3.8 * lado, -5.0                            # nasce atrás do medalhão
            fim = fim_m - SOBE_CORPO
            arco = {2: 3.5, 3: 3.5}.get(k, 0.0)                              # faixa dourada sobe pelo contorno do arco
            pcs.append(painel(f"manto{k}_{s}", (rx, MANTO_Y - 0.2 * (k % 2), rz), phi, lado, alvo, W0, W1, k, frente=k == 0,
                              fim=fim, abre=(0.0, 0.0, 1.0) if k == 0 else ((0.0, 4.5, 4.5) if k in (1, 2) else None), arco=arco))
        ossos.append(osso("manto_" + s, [4.5 * lado, MANTO_Y, 0.0], [0, 0, 0], pcs))
    rx, rz = anel(ax, az, zc, 90, 1)
    ossos.append(osso("manto_costas", [0, MANTO_Y, rz], [0, 0, 0], [
        painel("manto_costas_p", (0.0, MANTO_Y + 0.2, rz + 0.8), 90, 1, (0.0, 16.0), 10.4, 6.0, 2, costas=True,
               fim=11.0 - SOBE_CORPO)]))
    gola = []
    # capelete em 2 camadas descendo do pescoço em rampa (~20°): a de cima até ±5,5, a de baixo até ±8 com friso
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((1.4 * lado, 5.6 * lado))
        gola.append(osso("capelete_a_" + s, [1.4 * lado, 26.9, 0.0], [0, 0, -18 * lado],
                         g.arredondado("capelete_a_" + s, [x0, 25.3, -4.0], [x1, 26.9, 4.0], mat_capelete(None), r=0.7, res=3)))
        x0, x1 = sorted((2.2 * lado, 8.0 * lado))
        gola.append(osso("capelete_b_" + s, [2.2 * lado, 25.3, 0.0], [0, 0, -14 * lado],
                         g.arredondado("capelete_b_" + s, [x0, 23.0, -4.6], [x1, 25.3, 4.6], mat_capelete(23.0), r=0.9, res=3)))
        # medalhão octogonal (2 quadrados, o de trás girado 45°) com domo no meio, no topo do peitilho
        mx, my, mz = 3.0 * lado, 25.0, -8.1
        mm = mat_medalhao(mx, my)
        med = [peca("medalhao_a_" + s, [mx - 1.3, my - 0.75, mz - 0.4], [mx + 1.3, my + 0.75, mz + 0.4], mm, res=6),
               peca("medalhao_b_" + s, [mx - 0.75, my - 1.3, mz - 0.4], [mx + 0.75, my + 1.3, mz + 0.4], mm, res=6),
               peca("medalhao_d_" + s, [mx - 0.5, my - 0.5, mz - 0.8], [mx + 0.5, my + 0.5, mz - 0.4], mm, res=6)]
        gola.append(osso("medalhao_" + s, [mx, my, mz], [0, -10 * lado, 0], med))
    # capuz roxo atrás do pescoço (topo para trás) com 2 abas e filete dourado no topo
    gola.append(osso("capuz", [0, 25.6, 1.8], [15, 0, 0],
                     g.arredondado("capuz", [-2.6, 25.0, 0.6], [2.6, 28.4, 2.6], mat_capelete(None), r=0.7, res=3)))
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
    """Asa nos FLANCOS, sob a borda da capa (quadro "Asas Visíveis"): leque paralelo ao flanco, de trás para a frente
    com sobreposição: cobertura azul-real curta por fora, secundárias azul-claras e rêmiges amarelas/creme LONGAS
    caindo quase na vertical até a canela (~y 10 no mundo). Aparecem de frente na abertura em V e de lado no
    triângulo que a borda diagonal da capa deixa."""
    s = "d" if lado < 0 else "e"
    pcs = []
    for k, (z, phi) in enumerate(((-3.0, -10), (-1.6, -2), (-0.2, 6), (1.2, 14))):
        pcs.append(pena(f"asa_rem{k}_{s}", ((5.4 + 0.2 * k) * lado, 20.5, z), phi, lado, 14.0, 2.4,
                        P_ASA if k % 2 == 0 else P_ASA_CREME, flare=8, T=1.5))
    for k, (z, phi) in enumerate(((-2.6, -8), (-1.2, 0), (0.2, 8), (1.6, 14))):
        pcs.append(pena(f"asa_sec{k}_{s}", ((5.95 + 0.1 * k) * lado, 22.5, z), phi, lado, 9.0, 2.4, P_ASA_CLARA, flare=10, T=1.5))
    for k, (z, phi) in enumerate(((-2.2, -6), (-0.4, 4), (1.4, 12))):
        pcs.append(pena(f"asa_cob{k}_{s}", (6.5 * lado, 24.0, z), phi, lado, 5.0, 3.0, P_AZUL, flare=12, T=1.5))
    return osso("asa_" + s, [5.4 * lado, 24.5, -1.0], [0, 0, 0], pcs)

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

def mat_anel(cx, cy):
    """Anel dourado da base da cauda: aro de ouro com degradê e miolo azul-claro (face de trás)."""
    def f(c):
        if c["face"] != "south": return mat_ouro(c)
        x, y, z = c["p"]
        r = math.hypot(x - cx, y - cy)
        if r < 0.9: return mix(CIANO, AZUL, clamp((cy - y + 0.5) / 1.6))
        if r < 1.1: return OURO_ESC
        return mix(OURO_CL, OURO, clamp((cy - y + 1.2) / 2.4))
    return f

def so_gema(c, cor): return cor[2] > 200 and cor[0] < 200

P_LEQUE_AM = [(0, AMAR), (0.6, LIMAO), (1, (255, 246, 196))]
P_LEQUE_AZ = [(0, AZUL_REAL), (0.55, AZUL), (1, CIANO)]

P_LEQUE_AM2 = [(0, (242, 197, 49)), (0.7, (248, 214, 80)), (1, (255, 227, 106))]
P_LEQUE_AZ2 = [(0, AZUL_REAL), (0.5, PEITO_LADO), (1, CIANO)]

def leque(nome, pos):
    """Leque no fim da corrente: 5 penas afiladas (seção 1,4 -> 1,0 -> 0,7) abertas em CONE (±14° de lado, ±12° de
    altura), a do meio azul e as de fora amarelas com ponta clara; o eixo cai 55-65° abaixo da horizontal."""
    px, py, pz = pos
    pcs = []
    for k, (rx, ry, L, par) in enumerate([(0, 0, 6.2, P_LEQUE_AZ2), (-8, -9, 6.6, P_LEQUE_AM2), (-8, 9, 6.6, P_LEQUE_AM2),
                                          (8, -9, 6.0, P_LEQUE_AM2), (8, 9, 6.0, P_LEQUE_AM2)]):
        segs = [(L * 0.38, 0.9, 3.0), (L * 0.34, 0.85, 2.0), (L * 0.28, 0.8, 0.8)]       # penas chatas que afilam, sobrepostas
        pcs.append(lamina(f"{nome}_pl{k}", (px, py, pz - 0.3), (rx, ry, 0), (5, 0, 0), segs, par, eixo="z"))
    return pcs

def mat_conta2(cx, cy, cz):
    """Conta octogonal grossa: ouro facetado com o centro azul-claro (1,0 x 1,0) nas 4 faces compridas e nas pontas."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face in ("east", "west"): u, v = z - cz, y - cy
        elif face in ("up", "down"): u, v = z - cz, x - cx
        else: u, v = x - cx, y - cy
        if abs(u) < 0.5 and abs(v) < 0.5:
            return (235, 255, 255) if (u < -0.2 and v > 0.2) else mix(CIANO, AZUL, clamp((0.5 - v) / 1.4))
        if max(abs(u), abs(v)) < 0.62: return OURO_ESC
        return mat_ouro(c)
    return f

def corrente(nome, base, rot0, curvas, n_elos=None, abre_leque=0):
    """Corrente de contas (um osso por conta, '<nome>_k', cresce em +z e dobra 'curvas[k]' graus a cada junta; dobras
    positivas = desce). Contas octogonais de 2 (2 blocos em cruz) com vão de 0,5 e conector dourado; ficam um pouco
    menores perto da ponta. O leque (osso '<nome>_leque') cai em cone e abre 'abre_leque' graus para o lado."""
    n_elos = n_elos or len(curvas) + 1
    def seg(k, pos):
        px, py, pz = pos
        esc = 1.0 - 0.05 * k
        R = 1.0 * esc; r = 0.6 * esc; passo = 2.0 * esc + 0.5
        cz = pz + R
        m = mat_conta2(px, py, cz)
        filhos = [peca(f"{nome}_{k}", [px - R, py - r, cz - R], [px + R, py + r, cz + R], m, res=5, brilho=so_gema),
                  peca(f"{nome}_{k}b", [px - r, py - R, cz - R], [px + r, py + R, cz + R], m, res=5, brilho=so_gema),
                  peca(f"{nome}_{k}c", [px - 0.4, py - 0.4, cz + R - 0.1], [px + 0.4, py + 0.4, pz + passo + 0.1], mat_ouro, res=3)]
        if k + 1 < n_elos:
            filhos.append(seg(k + 1, (px, py, pz + passo)))
        else:
            p2 = (px, py, pz + passo)
            giro = -(rot0[0] + sum(curvas[:n_elos - 1])) + ANGULO_LEQUE   # o leque cai em cone para baixo e para trás
            filhos.append(osso(f"{nome}_leque", list(p2), [giro, abre_leque, 0], leque(nome, p2)))
        return osso(f"{nome}_{k}", list(pos), list(rot0) if k == 0 else [curvas[k - 1], 0, 0], filhos)
    return seg(0, tuple(base))

# arcos que sobem e descem; saem perto do meio das costas, abaixo do emblema, e abrem para o lado +x (as 3 aparecem
# na 3/4 da arte)
# Cauda tripla do pedido do dono: nasce baixa, na base traseira do corpo (o "uropígio", logo acima do quadril), por
# baixo da capa, e as 3 correntes DESCEM com leve curva para trás e um leque estreito para os lados (-10°, 0°, +10°);
# saem por baixo da barra de trás (que sobe e abre em fenda) e os leques param perto do chão. Dobras positivas = desce.
RAIZ_CAUDA = (0.0, 12.6, 4.6)
# S suave descendo por baixo da capa e saindo pelo arco de trás; só depois do arco os leques laterais abrem +15°
CORRENTES = [("cauda1", (-1.2, 12.2, 5.6), (40, -14, 0), [-5, -3, 2, 5, 5]), ("cauda2", (0.0, 11.6, 5.8), (34, 0, 0), [-4, 3, 6]),
             ("cauda3", (1.2, 12.2, 5.6), (40, 14, 0), [-5, -3, 2, 5, 5])]
ANGULO_LEQUE = 52              # o leque segue descendo para trás (graus abaixo da horizontal)
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
    if face != "up" and (p[1] % 1.5) < 0.2: return mix(AMAR, AMAR_ESC, 0.55)        # faixas de escama a cada 1,5
    return AMAR

def perna(lado):
    """Perna: coxa azul (sob a barriga) + canela de cima no osso da perna; tornozelo e canela de baixo no osso
    'tarso_*' (dobra no andar); pé e dedos no osso 'pata_*' (fica plano no chão no apoio)."""
    s = "d" if lado < 0 else "e"; xc = 3.2 * lado; zc = -1.0
    S = SOBE_CORPO
    ma = mat_cor(cor_perna, borda=.08, curva=.3)
    pp = []
    mcx = mat_cor(lambda p, f_: mix(AZUL_FUNDO, AZUL_REAL, clamp((p[1] - 11.6 - S) / 3.2)), borda=.0, curva=.3)
    pp += g.arredondado("coxa_" + s, [xc - 2.3, 11.6 + S, zc - 2.3], [xc + 2.3, 14.8 + S, zc + 2.3], mcx, r=0.8, res=2)
    # coxa emplumada: 3 pontas de pena na borda de baixo (transição do corpo azul para a perna amarela)
    q = 1.3 / 1.4142
    for j, dx in enumerate((-1.3, 0.0, 1.3)):
        pp.append(peca(f"coxa_ponta{j}_{s}", [xc + dx - q / 2, 11.6 + S - q / 2, zc - 2.2], [xc + dx + q / 2, 11.6 + S + q / 2, zc - 1.0],
                       mcx, rot=(0, 0, 45), pivo=(xc + dx, 11.6 + S, zc - 1.6), res=2))
    pp += g.octogono("tarso_cima_" + s, [xc - 1.5, 6.8, zc - 1.5], [xc + 1.5, 12.0 + S, zc + 1.5], ma, r=0.45, faixa=(1.5, 14.0))
    ta = []
    ta += g.arredondado("tornozelo_" + s, [xc - 1.65, 5.9, zc - 1.65], [xc + 1.65, 7.5, zc + 1.65], ma, r=0.45, faixa=(1.5, 14.0))
    ta += g.octogono("tarso_baixo_" + s, [xc - 1.3, 1.6, zc - 1.3], [xc + 1.3, 6.4, zc + 1.3], ma, r=0.4, faixa=(1.5, 14.0))
    mpe = mat_cor(lambda p, f_: BICO_CL if f_ == "up" else (AMAR_ESC if f_ == "down" else AMAR), borda=.14, curva=.35)
    mg = mat_cor(lambda p, f_: (90, 84, 100) if f_ == "up" else GARRA, borda=.1, curva=.2)
    pa = [peca("pe_" + s, [xc - 1.9, 0, zc - 1.9], [xc + 1.9, 2.0, zc + 1.5], mpe, faixa=(0, 2.0), res=2)]
    for nome, giro, dx, comp in (("meio", 0, 0, 5.0), ("fora", -34 * lado, 1.4 * lado, 4.3), ("dentro", 4 * lado, -1.2 * lado, 4.0)):
        x0, z0 = xc + dx, zc - 1.2
        pa.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
            peca(f"dedo_{nome}_{s}", [x0 - .85, 0, z0 - comp], [x0 + .85, 1.8, z0 + 0.3], mpe, faixa=(0, 1.8), res=2),
            peca(f"garra_{nome}_{s}", [x0 - .75, 0.35, z0 - comp - 1.7], [x0 + .75, 1.75, z0 - comp + 0.25], mg,
                 rot=(-8, 0, 0), pivo=(x0, 1.75, z0 - comp + 0.25), faixa=(0, 1.75), res=2)]))
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
                        r"cauda\d_\d|manto|gola|babador_\d|medalhao|forro|peitilho_|capelete|capuz)")

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
    corpo += g.arredondado("barriga", [-3.8, 12.0, -6.4], [3.8, 14.8, 1.4], mt, r=1.0, faixa=(11, 15), res=2)
    corpo.append(peca("quilha", [-2.6, 16.0, -7.4], [2.6, 22.6, -5.8], mt, res=2))
    # forro roxo-escuro atrás das pernas (ligado ao corpo): de frente a cauda não aparece entre as pernas
    corpo.append(peca("forro", [-2.4, -0.5, 1.2], [2.4, 12.6, 2.2], mat_cor(lambda p, f_: (59, 22, 80), borda=.05, curva=.2), res=2))
    # PEITILHO de penas azul-claras em V: a pena central (com a cruz latina) entra por baixo das penas do pescoço e
    # dos medalhões; abaixo dela 3 fileiras em telha (4, 3, 2 penas), cada uma 0,3 atrás da de cima, ponta para fora
    mpc = mat_peitilho(0.0, 25.2)
    bab = [peca("peitilho_a", [-2.2, 21.6, -7.7], [2.2, 25.6, -6.7], mpc, res=6),
           peca("peitilho_b", [-1.2, 20.6, -7.65], [1.2, 21.7, -6.7], mpc, res=6),
           peca("peitilho_c", [-0.45, 20.1, -7.6], [0.45, 20.7, -6.7], mpc, res=6)]
    P_PT = [(0, PEITILHO_CL), (1, PEITILHO)]
    for k, (y, xs, zc_) in enumerate(((20.5, (-2.4, -0.8, 0.8, 2.4), -6.95), (18.0, (-1.6, 0.0, 1.6), -6.65), (15.5, (-0.8, 0.8), -6.35))):
        for j, x in enumerate(xs):
            bab.append(pena_lisa(f"peitilho{k}_{j}", (x, y, zc_), 3.0, 1.6, 0.9, 8, k))
    corpo.append(osso("peitilho", [0, 20.0, -7.2], [0, 0, 0], bab))
    # laterais do peito em azul (enquadram o V azul-claro e entram por baixo da capa), terminando em ~15,5 no mundo
    for k, (x, y, z, L, W, fl, par) in enumerate([(-4.7, 19.8, -6.6, 5.2, 3.4, 12, P_AZUL), (4.7, 19.8, -6.6, 5.2, 3.4, 12, P_AZUL),
                                                  (-3.2, 17.4, -6.9, 4.8, 3.0, 12, P_PEITO_CLARO), (3.2, 17.4, -6.9, 4.8, 3.0, 12, P_PEITO_CLARO),
                                                  (-4.2, 16.2, -6.3, 4.2, 2.8, 18, P_FRANJA), (4.2, 16.2, -6.3, 4.2, 2.8, 18, P_FRANJA),
                                                  (-2.2, 15.9, -6.6, 4.0, 2.6, 16, P_FRANJA), (2.2, 15.9, -6.6, 4.0, 2.6, 16, P_FRANJA)]):
        corpo.append(pena(f"peito{k}", (x, y, z), -90, 1, L, W, par, flare=fl, T=1.2))
    # pescoço fino (60% da cabeça), curvo para a frente, com penas em telha encostadas (sem cards espetados)
    def cor_pesc(p, f_):
        x, y, z = p
        a = z if f_ in ("east", "west") else x
        base = PEITILHO if (f_ == "north" or z < -3.0) else (AZUL_REAL if z > -0.8 else mix(AZUL_REAL, AZUL, 0.4))
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
        for k, (phi, L) in enumerate(((-30, 3.0), (15, 3.5), (62, 3.5))):
            x, z = anel(1.5, 1.8, -1.9, phi, lado)
            alto.append(pena(f"colar{k}_{s_}", (x, 30.6 - 0.3 * (k % 2), z), phi, lado, L, 2.8, P_PESC, flare=10, T=1.0))
    alto.append(pena("colar_tras", (0, 30.6, -0.1), 90, 1, 3.5, 3.0, P_PESC, flare=10, T=1.0))
    pesc.append(osso("pescoco_alto", [0, 28.0, -1.0], [-10, 0, 0], alto))
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
    # base da cauda: anel dourado grande (centro azul-claro) na base traseira do corpo, de onde saem as 3 correntes
    ax_, ay_, az_ = RAIZ_CAUDA
    ma = mat_anel(ax_, ay_)
    base_cauda = [peca("cauda_anel_a", [ax_ - 2.1, ay_ - 1.2, az_ - 0.6], [ax_ + 2.1, ay_ + 1.2, az_ + 1.0], ma, res=5, brilho=so_gema),
                  peca("cauda_anel_b", [ax_ - 1.2, ay_ - 2.1, az_ - 0.6], [ax_ + 1.2, ay_ + 2.1, az_ + 1.0], ma, res=5, brilho=so_gema)]
    corpo.append(osso("cauda", list(RAIZ_CAUDA), [0, 0, 0], base_cauda + [
        corrente(n, b, r, c, abre_leque={"cauda1": -15, "cauda3": 15}.get(n, 0)) for n, b, r, c in CORRENTES]))
    g.transformar(i0, [o for o in corpo if isinstance(o, dict)], (0.0, 0.0, 0.0), sobe=SOBE_CORPO)
    tronco = osso("corpo", [0, 14.0 + SOBE_CORPO, 0.0], [0, 0, 0], corpo)
    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

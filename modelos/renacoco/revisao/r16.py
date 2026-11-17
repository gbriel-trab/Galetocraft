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
ROSTO = ((0, 34.4, -5.6), 8.2)

# ---------------- paleta (amostrada com PIL na "Paleta de Cores" da ficha e na expressão neutra) ----------------
ROXO_ESC = (98, 28, 152); ROXO_VIVO = (174, 59, 250); ROXO = (136, 42, 204); ROXO_FUNDO = (64, 16, 104)
AZUL = (2, 168, 251); CIANO = (133, 238, 253); AZUL_CARA = (82, 214, 252); AZUL_INT = (18, 112, 228)
AZUL_ESC = (14, 52, 150); CRUZ = (20, 36, 132); CRUZ_CLARA = (60, 90, 200)
CREME = (254, 234, 191); AMARELO = (254, 239, 96); AMAR = (254, 214, 64); AMAR_ESC = (232, 160, 24)
OURO = (250, 188, 40); OURO_CL = (255, 230, 120); OURO_ESC = (186, 116, 14)
VERM = (226, 26, 24); VERM_ESC = (150, 10, 18)
BICO = (254, 206, 40); BICO_CL = (255, 232, 110); BICO_ESC = (222, 150, 14)
GARRA = (46, 40, 54); PRETO = (16, 12, 26); BRANCO = (250, 250, 252)

def claro(c, f):
    """Clareia multiplicando (mantém a saturação da ficha)."""
    return tuple(min(255, int(round(v * (1 + f)))) for v in c)

def grad(paradas, t):
    t = clamp(t)
    for (t0, c0), (t1, c1) in zip(paradas, paradas[1:]):
        if t <= t1: return mix(c0, c1, (t - t0) / max(t1 - t0, 1e-6))
    return paradas[-1][1]

def mat_cor(cor_fn, **kw):
    def f(c):
        base = cor_fn(c["p"], c["face"])
        return None if base is None else tom(base, g.contexto_luz(c, **kw))
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
P_AZUL = [(0, AZUL_INT), (0.55, AZUL), (1, CIANO)]
P_CIANO = [(0, AZUL), (0.5, CIANO), (1, CREME)]
P_AMAR = [(0, CIANO), (0.2, AMAR), (0.7, AMARELO), (1, mix(AMARELO, CREME, 0.4))]
P_AMAR_PURO = [(0, AMAR), (0.5, AMARELO), (1, CREME)]
P_CRISTA = [(0, CIANO), (0.16, AMAR), (0.65, AMARELO), (1, claro(AMARELO, 0.0))]
P_AZUL2 = [(0, AZUL), (0.6, mix(AZUL, CIANO, 0.5)), (1, CIANO)]
P_FRANJA = [(0, AZUL_INT), (0.55, AZUL), (1, mix(AZUL, CIANO, 0.55))]

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
            cor = claro(base, 0.08) if u * claro_lado > 0 else tom(base, -0.08)
            if abs(u) < 0.08 and t < 0.85: cor = claro(cor, 0.08)
            if t < 0.1: cor = tom(cor, -0.18)
            if c["nome"].endswith("_pt"):
                if na_borda(c): cor = tom(cor, -0.25)
            elif c["i"] in (0, c["tw"] - 1): cor = tom(cor, -0.25)
            return cor
        if face == "up": return claro(base, 0.06)
        if face == "down": return tom(base, -0.4)
        return tom(base, -0.18)
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
FAC_ANG = 38                     # a faceta do olho olha mais para o lado (ave), um pouco para a frente
FAC_L, FAC_T = 4.0, 1.4
_tx, _tz = math.sin(math.radians(FAC_ANG)), math.cos(math.radians(FAC_ANG))
_nx, _nz = math.cos(math.radians(FAC_ANG)), -math.sin(math.radians(FAC_ANG))
LX = FRENTE_X + FAC_L * _tx
ZL = ZF + FAC_L * _tz
FAC_S = (FRENTE_X + _tx * FAC_L / 2, ZF + _tz * FAC_L / 2)
FAC_C = (FAC_S[0] - _nx * FAC_T / 2, FAC_S[1] - _nz * FAC_T / 2)
OLHO_Y = 32.6
OLHO_RU, OLHO_RV = 1.75, 1.35
OLHO_CORTE0, OLHO_CORTE_INC = 0.55, 0.16     # pálpebra pesada mas serena (diagonal suave descendo para o bico)

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
    if v > corte and v <= corte + 0.2 and v <= cima + 0.3: return mix(PRETO, AZUL_ESC, 0.4)     # sombra da pálpebra
    if v < baixo or v > topo: return None
    if topo - v < 0.13: return PRETO                                                            # fio da pálpebra
    ic, ir = -0.16, 0.74
    du = (uu - ic) / ir; dv = v / (rv * 0.95)
    if du * du + dv * dv <= 1 or (uu < ic and v >= baixo):
        if ((uu + 0.42) / 0.16) ** 2 + ((v + 0.05) / 0.5) ** 2 <= 1: return PRETO                # pupila
        if ((uu + 0.22) / 0.1) ** 2 + ((v - topo + 0.3) / 0.15) ** 2 <= 1: return (255, 255, 255)  # brilho
        cor = mix((40, 190, 255), (10, 84, 200), clamp((v - baixo) / max(topo - baixo, 0.1)))
        if topo - v < 0.24: cor = tom(cor, -0.3)
        if du * du + dv * dv > 0.78 and uu > ic: cor = AZUL_ESC
        return cor
    return mix(BRANCO, (196, 206, 226), clamp((topo - v) / 0.9))

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return AZUL
    if y < OLHO_Y - 1.4: return mix(AZUL, AZUL_CARA, 0.6)          # bochecha mais clara embaixo do olho
    if z > ZL + 1.2: return mix(AZUL, AZUL_INT, 0.35)               # trás da cabeça um tom mais fundo
    return AZUL

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
                if face == "down": return tom(base, -0.35)
                dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
                larga = ("east", "west") if dx <= min(dy, dz) else (("north", "south") if dz <= dy else ("up", "down"))
                if face in larga:
                    cor = claro(base, 0.06) if (c["i"] + .5) / c["tw"] < 0.5 else tom(base, -0.06)
                    if na_borda(c): cor = tom(cor, -0.18)
                    return cor
                return tom(base, -0.16)
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
    cab += g.arredondado2("cranio", [-LX, CAB_Y0, ZL - 0.5], [LX, CAB_Y1, 1.2], mc, r=1.2, faixa=fx, res=3)
    cab.append(peca("cranio_frente", [-FRENTE_X - 0.4, CAB_Y0 + 0.3, ZF], [FRENTE_X + 0.4, CAB_Y1 - 0.5, ZL], mc, faixa=fx, res=3))
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
            if c["face"] == "down": return tom(AZUL_ESC, -0.1)
            base = {"up": claro(CIANO, 0.04), "north": CIANO}.get(c["face"], mix(CIANO, AZUL, 0.2))
            return tom(base, -0.12) if na_borda(c) else base
        cab.append(osso("sobrancelha_" + s, [cx, yb, zc0], [0, FAC_ANG * lado, 0], [
            peca("sobrancelha_" + s, [ox0, yb, cz - FAC_L / 2 + 0.1], [ox1, yb + 0.95, cz + FAC_L / 2 + 0.6],
                 msob, rot=(-ang, 0, 0), pivo=(cx, yb, zc0), res=4)]))
        # a pluma da sobrancelha continua para trás e para cima, passando por cima da orelha
        cab.append(lamina("sobr_pluma_" + s, ((LX - 0.2) * lado, OLHO_Y + 1.1, ZL + 0.9), (-12, 14 * lado, 0), (8, 0, 0),
                          [(2.6, 0.9, 1.5), (2.2, 0.8, 1.1), (1.8, 0.7, 0.7)], [(0, CIANO), (0.6, CIANO), (1, mix(CIANO, AZUL, .4))], eixo="z"))
    # bico reto e longo em cunha: base alta (tampa + quilha em V de frente), meio e ponta afinando com leve gancho
    mb = mat_cor(cor_bico, borda=.05, curva=.3)
    def mq(c):
        f_ = c["face"]
        cor = mix(BICO_CL, BICO, 0.35) if f_ in ("up", "east") else (BICO if f_ in ("north", "south") else claro(BICO, 0.03))
        return tom(cor, -0.14) if na_borda(c) else cor
    fb = (29.4, 32.6)
    cab.append(peca("bico_tampa", [-1.45, 31.1, ZF - 2.4], [1.45, 32.6, ZF + 0.6], mb, faixa=fb, res=4))
    q = 1.45 * 1.4142
    cab.append(peca("bico_quilha", [-q / 2, 31.0 - q / 2, ZF - 2.3], [q / 2, 31.0 + q / 2, ZF + 0.5], mq, rot=(0, 0, 45),
                    pivo=(0, 31.0, ZF), faixa=fb, res=4))
    piv = (0, 32.4, ZF - 2.2)
    cab.append(peca("bico_tampa2", [-1.05, 31.0, ZF - 4.6], [1.05, 32.4, ZF - 2.1], mb, rot=(-7, 0, 0), pivo=piv, faixa=fb, res=4))
    q = 1.05 * 1.4142
    cab.append(peca("bico_quilha2", [-q / 2, 30.95 - q / 2, ZF - 4.5], [q / 2, 30.95 + q / 2, ZF - 2.2], mq, rot=(-7, 0, 45),
                    pivo=(0, 30.95, ZF - 2.2), faixa=fb, res=4))
    cab.append(peca("bico_ponta", [-0.65, 30.6, ZF - 6.0], [0.65, 31.9, ZF - 4.4],
                    mat_cor(lambda p, f_: BICO_CL if f_ == "up" else mix(BICO, BICO_ESC, clamp((31.3 - p[1]) / 1.0)), borda=.1, curva=.2),
                    rot=(-15, 0, 0), pivo=(0, 31.9, ZF - 4.4), faixa=(30.6, 31.9), res=4))
    cab.append(peca("bico_baixo", [-0.95, 29.6, ZF - 3.6], [0.95, 30.5, ZF + 0.4], mat_cor(lambda p, f_: BICO_ESC, borda=.1), res=4,
                    rot=(5, 0, 0), pivo=(0, 30.5, ZF + 0.4)))
    # barbela vermelha: dois lóbulos compridos sob a base do bico, com vão escuro no meio
    def cor_barb(p, f_):
        if abs(p[0]) < 0.14: return VERM_ESC
        return mix(VERM, VERM_ESC, clamp((27.5 - p[1]) / 3.0))
    mbar = mat_cor(cor_barb, borda=.08, curva=.25)
    for lado, fim in ((-1, 25.8), (1, 26.2)):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.0, 1.05 * lado)); x2, x3 = sorted((0.1 * lado, 0.9 * lado))
        cab.append(osso("barbela_" + s, [0.0, 29.6, ZF - 0.8], [0, 0, -3 * lado], [
            peca("barbela_a_" + s, [x0, fim + 1.3, ZF - 1.8], [x1, 29.8, ZF + 0.1], mbar, faixa=(fim, 29.8), res=4),
            peca("barbela_b_" + s, [x2, fim, ZF - 1.5], [x3, fim + 1.5, ZF - 0.3], mbar, faixa=(fim, 29.8), res=4)]))
    # penas do rosto (moldura nobre): atrás do olho, em telha, deitadas para trás e um pouco para baixo; azuis
    # embaixo, azul-claras no meio, amarelas em cima (emendam com a crista)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, (y, z, L, rx, ry, h, par) in enumerate([(30.4, -0.8, 4.0, 16, 10, 2.2, P_AZUL2), (32.0, -0.4, 4.8, 6, 12, 2.6, P_CIANO),
                                                        (34.0, 0.0, 5.0, -8, 12, 2.6, P_CRISTA)]):
            segs = [(L * 0.42, 0.9, h), (L * 0.33, 0.8, h * 0.72), (L * 0.27, 0.7, h * 0.42)]
            cab.append(lamina(f"rosto{k}_{s}", ((LX - 0.6) * lado, y, z), (rx, ry * lado, 0), (7, 0, 0), segs, par, eixo="z"))
    cab.append(crista_ossos())
    return cab

# crista em chama: plumas amarelas largas que sobem e varrem para trás em leque, com base azul-clara
CRISTA = [  # (x, z da raiz, comprimento, inclinação para trás, abertura lateral, larga de frente?)
    # miolo: plumas largas de lado, subindo e varrendo para trás
    (0.0, -4.2, 5.8, -2, 0, False), (0.0, -2.2, 6.8, 22, 0, False), (0.0, 0.0, 5.0, 48, 0, False), (0.0, 1.2, 3.6, 72, 0, False),
    # leque lateral: plumas largas de frente que abrem para os lados (de frente a crista vira um leque de chama)
    (1.3, -3.4, 5.6, 8, -16, True), (-1.3, -3.4, 5.6, 8, 16, True), (2.0, -1.8, 5.2, 24, -34, True), (-2.0, -1.8, 5.2, 24, 34, True),
    (2.2, 0.2, 4.6, 46, -50, True), (-2.2, 0.2, 4.6, 46, 50, True),
]

def crista_ossos():
    pc = []
    # base azul-clara da crista (o "diadema" de plumas curtas por cima da testa)
    pc += g.arredondado("crista_base", [-2.6, 34.4, -5.6], [2.6, 36.2, 1.4],
                        mat_cor(lambda p, f_: CIANO if f_ != "down" else AZUL, borda=.0, curva=.25), r=0.7, res=3)
    for k, (x, z, L, rx, rz, frente) in enumerate(CRISTA):
        if frente: segs = [(L * 0.42, 2.6, 1.0), (L * 0.33, 1.9, 0.9), (L * 0.28, 1.1, 0.8)]
        else: segs = [(L * 0.42, 1.1, 3.4), (L * 0.33, 1.0, 2.5), (L * 0.28, 0.8, 1.3)]
        pc.append(lamina(f"crista{k}", (x, 35.6, z), (rx, 0, rz), (12, 0, 0), segs, P_CRISTA, eixo="y"))
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
    base = mix(AZUL_INT, AZUL, clamp((y - 12) / 12))
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
        cor = mix(CIANO, claro(CIANO, 0.05), clamp((y - 18) / 6))
        if escama(x, y, 2.2, 1.6): cor = tom(cor, -0.12)
        return tom(cor, -0.12) if na_borda(c) else cor
    return tom(CIANO, g.contexto_luz(c, borda=.1))

def mat_dente(c):
    face = c["face"]
    cor = mix(CIANO, AZUL, 0.25) if face != "down" else tom(AZUL, -0.2)
    return tom(cor, -0.18) if na_borda(c) else cor

# --- manto: painéis grossos em 3 degraus ---
MANTO_Y = 25.6                 # altura do anel do ombro (raiz dos painéis)
SOBE_CORPO = 2.0               # o corpo todo sobe (pernas mais longas, como na arte); o manto continua indo até o chão
MANTO_FIM = 1.4 - SOBE_CORPO   # altura da barra do manto (antes de subir o corpo)
ANEL = (6.3, 5.2, 0.6)         # raios x, z e centro z do anel do ombro
FR = (0.36, 0.34, 0.30)        # frações do comprimento de cada degrau
ABRE = (0.0, 3.0, 3.5)         # quanto cada degrau abre a mais que o de cima (caimento de sino)
BORDA = 1.5                    # altura da barra dourada

def glifo_manto(cx, s):
    """Padrão dourado das pontas (quadro "Detalhe do Manto"): espiral quadrada em blocos, repetida a cada 3,6."""
    if not (0.25 < s < 2.75): return False
    a = cx % 3.6
    return ((0.3 < a < 0.95 and 0.25 < s < 2.75) or (0.3 < a < 3.0 and 2.1 < s < 2.75) or (2.35 < a < 3.0 and 0.95 < s < 2.75)
            or (1.3 < a < 3.0 and 0.95 < s < 1.55))

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

def mat_manto(raiz, L, zc, lado, k, frente_z=None, costas=False):
    """Pintura do painel no referencial dele (antes das rotações): s = distância da raiz, d = distância até a barra,
    a = posição na largura. Face de fora: roxo vivo em cima -> roxo, dobras nas beiradas, barra dourada e padrões;
    face de dentro: roxo escuro com barra e frente douradas."""
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
        na_frente = frente_z is not None and z - frente_z < 1.2
        if face == "down": return OURO_ESC
        if face == "up": return ROXO_VIVO if not na_frente else OURO_CL
        if face in (fora, dentro):
            ext = face == fora
            if d < BORDA or na_frente:
                cor = OURO if ext else OURO_ESC
                if (d < BORDA and abs(d - BORDA) < 0.2) or (na_frente and abs(z - frente_z - 1.2) < 0.2): cor = OURO_ESC
                return cor
            if not ext:
                return tom(ROXO_ESC, -0.1 + 0.15 * clamp(1 - s / L))
            if costas:
                ue, ve = a / 1.25, ((y0 - 7.8) - y) / 1.0    # emblema: centro a 7,8 da raiz (mais alto que largo: o painel inclina)
                if abs(ue) < 4.3 and abs(ve) < 4.2 and fenix(ue, ve): return OURO_CL if ve > 1.6 else (OURO if ve > -1.0 else OURO_ESC)
                lc = losango_costas(a, (y0 - 21.0) - y)
                if lc: return lc
            if glifo_manto(a + 1.8 + 1.1 * k, d - BORDA): return OURO
            base = mix(mix(ROXO_VIVO, ROXO, 0.4), mix(ROXO, ROXO_ESC, 0.35), clamp(s / (L * 0.85)))
            if not vivo: base = mix(base, ROXO_ESC, 0.25)
            base = tom(base, -0.22 * aw ** 2.5)                                  # dobra nas beiradas
            if s < 2.0: base = claro(base, 0.08 * (1 - s / 2.0))
            return base
        # beiradas finas (espessura)
        if d < BORDA: return OURO_ESC
        return ROXO_ESC if not na_frente else OURO
    return f

def mat_barra(c):
    """Barra dourada em relevo: topo claro, frente ouro, fio escuro em cima e embaixo."""
    face = c["face"]
    if face == "up": return OURO_CL
    if face == "down": return OURO_ESC
    if c["j"] == 0: return OURO_CL
    if c["j"] == c["th"] - 1: return OURO_ESC
    return OURO

def painel(nome, raiz, phi, lado, alvo, W0, W1, k, T=1.0, frente=False, costas=False):
    """Painel do manto pendurado do anel do ombro, em 3 degraus encadeados (cada um abre ABRE graus a mais). 'alvo' =
    (x para fora, z) onde a barra deve cair no chão; o giro (flare para fora, varre para trás) sai daí."""
    x, y, z = raiz
    H = y - MANTO_FIM
    xo = abs(x)
    dx, dz = alvo[0] - xo, alvo[1] - z
    r = math.radians(phi)
    n = (math.cos(r), math.sin(r)); t = (-math.sin(r), math.cos(r))
    dn, dt = dx * n[0] + dz * n[1], dx * t[0] + dz * t[1]
    flare = math.degrees(math.atan2(dn, H)) - sum(ABRE) * 0.55
    varre = math.degrees(math.atan2(dt, math.hypot(H, dn)))
    L = math.sqrt(H * H + dx * dx + dz * dz) * 0.97
    zf = z - W0 / 2 if frente else None
    m = mat_manto(raiz, L, z, lado, k, frente_z=zf, costas=costas)
    larg = (W0, (W0 + W1) / 2, W1)
    ys = [y, y - L * FR[0], y - L * (FR[0] + FR[1]), y - L]
    def bloco(i):
        w = larg[i]
        za, zb = (zf, zf + w) if frente else (z - w / 2, z + w / 2)
        ya, yb = ys[i + 1], ys[i] + (0.35 if i else 0)
        pcs = [peca(f"{nome}_{i}", [x - T / 2, ya, za], [x + T / 2, yb, zb], m, faixa=(MANTO_FIM, MANTO_Y), res=3 if not costas else 4)]
        if i == 2:
            pcs.append(peca(f"{nome}_barra", [x - T / 2 - 0.22, ya - 0.05, za - 0.05], [x + T / 2 + 0.22, ya + BORDA, zb + 0.05],
                            mat_barra, res=3))
        if frente:
            pcs.append(peca(f"{nome}_frente{i}", [x - T / 2 - 0.2, ya, zf - 0.05], [x + T / 2 + 0.2, yb, zf + 1.2], mat_barra_frente, res=2))
        if i < 2:
            pcs.append(osso(f"{nome}_d{i + 1}", [x, ys[i + 1], z], [0, 0, ABRE[i + 1] * lado], bloco(i + 1)))
        return pcs
    return osso(nome, list(raiz), [0, -phi * lado, 0], [osso(nome + "_p", list(raiz), [-varre, 0, flare * lado], bloco(0))])

def mat_barra_frente(c):
    face = c["face"]
    if face == "up": return OURO_CL
    if face == "down": return OURO_ESC
    if face in ("north", "south"): return OURO_ESC if face == "south" else OURO
    return tom(OURO, -0.2) if c["i"] in (0, c["tw"] - 1) else OURO

# painéis de cada lado: (phi no anel, alvo da barra (x para fora, z), largura em cima, largura embaixo)
PAINEIS = [(-62, (11.6, 6.8), 4.4, 7.4), (-28, (13.6, 10.4), 5.4, 8.6), (8, (13.8, 14.8), 5.6, 9.0),
           (42, (12.0, 19.4), 5.6, 9.6), (70, (7.8, 23.2), 5.4, 9.8)]

def manto_ossos():
    """Manto: gola enrolada grossa, painéis dos dois lados, painel das costas com emblema e fecho de 2 medalhões."""
    ossos = []
    ax, az, zc = ANEL
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        pcs = []
        for k, (phi, alvo, W0, W1) in enumerate(PAINEIS):
            rx, rz = anel(ax + 0.3 * (k % 2), az + 0.3 * (k % 2), zc, phi, lado)
            pcs.append(painel(f"manto{k}_{s}", (rx, MANTO_Y - 0.25 * (k % 2), rz), phi, lado, alvo, W0, W1, k, T=1.0, frente=k == 0))
        ossos.append(osso("manto_" + s, [4.5 * lado, MANTO_Y, 0.0], [0, 0, 0], pcs))
    # costas: painel largo do meio (emblema + losangos), por dentro dos laterais de trás
    rx, rz = anel(ax, az, zc, 90, 1)
    ossos.append(osso("manto_costas", [0, MANTO_Y, rz], [0, 0, 0], [
        painel("manto_costas_p", (0.0, MANTO_Y + 0.2, rz - 0.3), 90, 1, (0.0, 25.6), 9.4, 14.0, 2, T=1.1, costas=True)]))
    # gola enrolada: rolo grosso em volta da base do pescoço (sobe atrás como um capuz baixo)
    mg = mat_cor(lambda p, f_: ROXO_VIVO if f_ == "up" else mix(ROXO_VIVO, ROXO, clamp((27.5 - p[1]) / 3.5)), borda=.1, curva=.3)
    gola = []
    gola += g.arredondado2("gola_tras", [-5.0, 24.0, 1.2], [5.0, 29.6, 5.8], mg, r=1.4, faixa=(24.0, 29.6), res=3)
    # ponta do capuz baixo atrás do pescoço (de costas a gola sobe em bico até a nuca)
    q = 3.6 / 1.4142
    gola.append(peca("capuz", [-q / 2, 28.4 - q / 2, 3.0], [q / 2, 28.4 + q / 2, 5.6], mg, rot=(0, 0, 45), pivo=(0, 28.4, 4.3),
                     faixa=(24.0, 31.0), res=3))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        # ombro do manto: rolo grosso e largo (silhueta de ombros nobres, como na arte)
        x0, x1 = sorted((2.8 * lado, 7.6 * lado))
        gola += g.arredondado2("gola_lado_" + s, [x0, 23.2, -3.6], [x1, 28.0, 3.8], mg, r=1.6, faixa=(23.2, 28.0), res=3)
        x0, x1 = sorted((2.2 * lado, 5.6 * lado))
        gola.append(osso("gola_frente_" + s, [3.9 * lado, 25.6, -3.4], [0, -22 * lado, 0],
                         g.arredondado("gola_frente_" + s, [x0, 23.6, -6.4], [x1, 27.0, -1.8], mg, r=0.9, faixa=(23.6, 27.0), res=3)))
        # medalhão dourado redondo (fecho): octógono de frente + miolo em relevo
        mx, my, mz = 3.8 * lado, 24.4, -7.3
        med = [peca("medalhao_a_" + s, [mx - 1.35, my - 0.78, mz - 0.25], [mx + 1.35, my + 0.78, mz + 0.65], mat_medalhao(mx, my), res=6),
               peca("medalhao_b_" + s, [mx - 0.78, my - 1.35, mz - 0.25], [mx + 0.78, my + 1.35, mz + 0.65], mat_medalhao(mx, my), res=6),
               peca("medalhao_c_" + s, [mx - 0.62, my - 0.62, mz - 0.55], [mx + 0.62, my + 0.62, mz], mat_medalhao(mx, my), res=6)]
        gola.append(osso("medalhao_" + s, [mx, my, mz], [0, -18 * lado, 0], med))
    ossos.append(osso("gola", [0, 26.0, 0.0], [0, 0, 0], gola))
    return ossos

def mat_medalhao(cx, cy):
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face != "north": return mat_ouro(c)
        r = math.hypot(x - cx, y - cy)
        if r < 0.45: return OURO_CL
        if r < 0.7: return OURO
        if r < 1.0: return mix(OURO_CL, OURO, clamp((y - cy + 0.8) / 1.6)) if (x - cx) + (y - cy) > 0 else OURO
        return OURO_ESC
    return f

# ================= ASAS (sob o manto) =================
def asa_ossos(lado):
    s = "d" if lado < 0 else "e"
    pcs = []
    # cobertura azul / azul-claro (curta) e rêmiges longas azul-claro -> amarelo -> creme (aparecem perto das pernas)
    for k, (phi, L, W, fl, va, par) in enumerate([(-40, 8.0, 3.6, 14, 6, P_AZUL), (-8, 8.6, 3.8, 14, 10, P_AZUL),
                                                  (26, 8.2, 3.6, 14, 14, P_AZUL)]):
        x, z = anel(5.7, 4.6, 0.0, phi, lado)
        pcs.append(pena(f"asa_cob{k}_{s}", (x, 24.4, z), phi, lado, L, W, par, flare=fl, varre=va, T=1.0))
    for k, (phi, L, W, fl, va, par) in enumerate([(-72, 12.0, 2.4, 14, 0, P_CIANO), (-56, 14.0, 2.5, 16, 2, P_AMAR),
                                                  (-38, 15.0, 2.5, 17, 4, P_AMAR), (-18, 14.6, 2.5, 16, 8, P_AMAR),
                                                  (4, 14.0, 2.5, 14, 12, P_AMAR), (28, 12.6, 2.4, 12, 18, P_CIANO)]):
        x, z = anel(5.4, 4.8, 0.0, phi, lado)
        pcs.append(pena(f"asa_rem{k}_{s}", (x, 22.0 - 0.3 * (k % 2), z), phi, lado, L, W, par, flare=fl, varre=va, T=0.9))
    return osso("asa_" + s, [4.4 * lado, 24.5, 0.0], [0, 0, 0], pcs)

# ================= CAUDA TRIPLA =================
N_ELOS = 6
PASSO = 2.2

def mat_elo(c):
    """Elo dourado com o miolo azul-claro em losango nas 4 faces compridas (brilha)."""
    face = c["face"]
    if face in ("north", "south"): return tom(OURO, -0.2)
    (x0, y0, z0), (x1, y1, z1) = c["b"]
    u = (c["p"][2] - (z0 + z1) / 2) / ((z1 - z0) / 2)
    v = (c["i"] + .5) / c["tw"] * 2 - 1 if face in ("up", "down") else (c["j"] + .5) / c["th"] * 2 - 1
    d = abs(u) * 0.9 + abs(v)
    if d < 0.62: return claro(CIANO, 0.08) if u + v < -0.2 else CIANO
    if d < 0.8: return OURO_CL
    base = {"up": OURO_CL, "down": OURO_ESC}.get(face, OURO)
    return tom(base, -0.25) if na_borda(c) else base

def so_gema(c, cor): return cor[2] > 200 and cor[0] < 200

def leque(nome, pos):
    """Leque no fim da corrente: 5 plumas (3 amarelas longas, 2 azuis mais curtas) abertas em leque vertical."""
    px, py, pz = pos
    pcs = []
    # (deitadas para trás ao longo da corrente, como nas vistas laterais; as azuis por baixo, mais curtas)
    for k, (rx, ry, L, par) in enumerate([(-15, 0, 14.0, P_AMAR), (-4, 3, 15.6, P_AMAR), (7, -3, 14.2, P_AMAR),
                                          (-9, -6, 9.4, P_AZUL), (2, 6, 9.0, P_AZUL)]):
        segs = [(L * 0.4, 0.9, 4.2), (L * 0.33, 0.8, 3.2), (L * 0.27, 0.7, 1.7)]
        pcs.append(lamina(f"{nome}_pl{k}", (px, py, pz - 0.3), (rx, ry, 0), (3, 0, 0), segs, par, eixo="z"))
    # nó dourado de onde o leque sai
    pcs.append(peca(f"{nome}_no", [px - 0.95, py - 0.95, pz - 0.6], [px + 0.95, py + 0.95, pz + 0.9], mat_ouro, res=3))
    return pcs

def corrente(nome, base, rot0, curva):
    """Corrente de elos (um osso por elo, '<nome>_k', cresce em +z e dobra 'curva' graus a cada junta); o leque fica
    no osso '<nome>_leque', depois do último elo."""
    def seg(k, pos):
        px, py, pz = pos
        h = 0.85
        filhos = [peca(f"{nome}_{k}", [px - h, py - h, pz + 0.1], [px + h, py + h, pz + PASSO * 0.95], mat_elo,
                       rot=(0, 0, 45), pivo=(px, py, pz), res=4, brilho=so_gema)]
        if k + 1 < N_ELOS:
            filhos.append(seg(k + 1, (px, py, pz + PASSO)))
        else:
            p2 = (px, py, pz + PASSO)
            filhos.append(osso(f"{nome}_leque", list(p2), [-4, 0, 0], leque(nome, p2)))
        return osso(f"{nome}_{k}", list(pos), list(rot0) if k == 0 else [curva, 0, 0], filhos)
    return seg(0, tuple(base))

CORRENTES = [("cauda1", (0.6, 23.4, 3.6), (4, 16, 0), 0.0), ("cauda2", (-1.2, 22.2, 3.8), (27, -24, 0), -1.0),
             ("cauda3", (1.2, 19.0, 4.0), (46, 26, 0), -3.0)]
ONDAS = [(n, N_ELOS, (3.0, 2.5, 1.5)) for n, _, _, _ in CORRENTES]
ANIM_PARADO = {
    "manto_d": [(0, 0, 0), (1.5, 0, -1.2), (0, 0, 0), (-1, 0, 0.8), (0, 0, 0)],
    "manto_e": [(0, 0, 0), (1.5, 0, 1.2), (0, 0, 0), (-1, 0, -0.8), (0, 0, 0)],
    "manto_costas": [(0, 0, 0), (2, 0, 0), (0, 0, 0), (-1, 0, 0), (0, 0, 0)],
    **{f"{n}_leque": [(0, 0, 0), (-6, 4, 0), (0, 0, 0), (4, -4, 0), (0, 0, 0)] for n, _, _, _ in CORRENTES},
}
ANIM_ANDANDO = {
    "manto_d": [(0, 0, 0), (4, 0, -2), (0, 0, 0), (4, 0, -2), (0, 0, 0)],
    "manto_e": [(0, 0, 0), (4, 0, 2), (0, 0, 0), (4, 0, 2), (0, 0, 0)],
    "manto_costas": [(0, 0, 0), (6, 0, 0), (0, 0, 0), (6, 0, 0), (0, 0, 0)],
    **{f"{n}_leque": [(0, 0, 0), (-10, 6, 0), (0, 0, 0), (6, -6, 0), (0, 0, 0)] for n, _, _, _ in CORRENTES},
}

# ================= PERNAS =================
def cor_perna(p, face):
    if face == "down": return AMAR_ESC
    if face != "up" and (p[1] % 1.15) < 0.16: return mix(AMAR, AMAR_ESC, 0.55)      # anéis de escama
    return AMAR

def perna(lado):
    s = "d" if lado < 0 else "e"; xc = 2.6 * lado; zc = -1.0
    pp = []
    ma = mat_cor(cor_perna, borda=.08, curva=.3)
    # coxa de penas azuis (some quase toda sob a barriga)
    pp += g.arredondado("coxa_" + s, [xc - 2.0, 10.6 + SOBE_CORPO, zc - 2.2], [xc + 2.0, 14.6 + SOBE_CORPO, zc + 2.0],
                        mat_cor(lambda p, f_: mix(AZUL_INT, AZUL, clamp((p[1] - 10.6 - SOBE_CORPO) / 4)), borda=.0, curva=.3), r=0.8, res=2)
    pp += g.octogono("tarso_cima_" + s, [xc - 1.5, 6.8, zc - 1.5], [xc + 1.5, 11.4 + SOBE_CORPO, zc + 1.5], ma, r=0.45, faixa=(1.5, 11.4))
    pp += g.arredondado("tornozelo_" + s, [xc - 1.65, 5.9, zc - 1.65], [xc + 1.65, 7.5, zc + 1.65], ma, r=0.45, faixa=(1.5, 11.4))
    pp += g.octogono("tarso_baixo_" + s, [xc - 1.3, 1.4, zc - 1.3], [xc + 1.3, 6.4, zc + 1.3], ma, r=0.4, faixa=(1.5, 11.4))
    mpe = mat_cor(lambda p, f_: BICO_CL if f_ == "up" else (AMAR_ESC if f_ == "down" else AMAR), borda=.14, curva=.35)
    mg = mat_cor(lambda p, f_: (90, 84, 100) if f_ == "up" else GARRA, borda=.1, curva=.2)
    pp.append(peca("pe_" + s, [xc - 1.9, 0, zc - 1.9], [xc + 1.9, 2.0, zc + 1.5], mpe, faixa=(0, 2.0), res=2))
    for nome, giro, dx, comp in (("meio", 0, 0, 5.0), ("fora", -24 * lado, 1.4 * lado, 4.2), ("dentro", 22 * lado, -1.4 * lado, 4.0)):
        x0, z0 = xc + dx, zc - 1.2
        pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
            peca(f"dedo_{nome}_{s}", [x0 - .85, 0, z0 - comp], [x0 + .85, 1.8, z0 + 0.3], mpe, faixa=(0, 1.8), res=2),
            peca(f"garra_{nome}_{s}", [x0 - .7, 0.0, z0 - comp - 1.4], [x0 + .7, 1.5, z0 - comp + 0.2], mg,
                 rot=(-10, 0, 0), pivo=(x0, 1.5, z0 - comp + 0.2), faixa=(0, 1.5), res=2)]))
    pp.append(peca("dedo_tras_" + s, [xc - .7, 0, zc + 1.2], [xc + .7, 1.4, zc + 3.4], mpe, faixa=(0, 1.4), res=2))
    pp.append(peca("garra_tras_" + s, [xc - .55, 0, zc + 3.3], [xc + .55, 1.1, zc + 4.3], mg, faixa=(0, 1.1), res=2))
    return osso("perna_" + s, [xc, 14.0 + SOBE_CORPO, zc], [0, 0, 0], pp)

# ================= MONTAGEM =================
ROT_PESC = -2          # pescoço quase reto: nas vistas laterais o bico fica só um pouco à frente do peito; a cabeça olha reto
def montar():
    i0 = len(g.PECAS)
    corpo = []
    mt = mat_cor(cor_tronco, borda=.0, curva=.3)
    corpo += g.arredondado2("tronco", [-5.0, 13.0, -6.2], [5.0, 26.4, 4.2], mt, r=2.0, faixa=(12, 26.4), res=2)
    corpo += g.arredondado("ventre", [-4.2, 11.4, -4.8], [4.2, 15.0, 3.2], mt, r=1.0, faixa=(11, 15), res=2)
    # babador azul-claro com a cruz + franja de pontas em losango embaixo
    corpo += g.arredondado("babador", [-3.7, PEITO_Y0, -7.0], [3.7, PEITO_Y1, -5.4], mat_babador, r=0.5, res=6)
    for k, x in enumerate((-2.45, 0.0, 2.45)):
        q = 2.5 / 1.4142
        corpo.append(peca(f"babador_ponta{k}", [x - q / 2, PEITO_Y0 - q / 2, -6.85], [x + q / 2, PEITO_Y0 + q / 2, -5.6], mat_dente,
                          rot=(0, 0, 45), pivo=(x, PEITO_Y0, -6.2), res=4))
    # peito: penas azuis em telha em 3 fileiras desencontradas, descendo sob o babador e abrindo para os lados (V)
    for k, (x, y, z, L, W, fl, par) in enumerate([(-4.2, 19.2, -6.1, 5.2, 3.0, 8, P_AZUL), (-1.4, 18.8, -6.5, 5.0, 3.0, 8, P_AZUL),
                                                  (1.4, 18.8, -6.5, 5.0, 3.0, 8, P_AZUL), (4.2, 19.2, -6.1, 5.2, 3.0, 8, P_AZUL),
                                                  (-2.8, 16.6, -6.3, 5.0, 3.2, 12, P_AZUL), (0.0, 16.4, -6.4, 5.0, 3.2, 12, P_AZUL),
                                                  (2.8, 16.6, -6.3, 5.0, 3.2, 12, P_AZUL),
                                                  (-4.0, 14.6, -5.5, 3.8, 2.8, 20, P_FRANJA), (-1.4, 14.2, -5.8, 3.8, 2.8, 20, P_FRANJA),
                                                  (1.4, 14.2, -5.8, 3.8, 2.8, 20, P_FRANJA), (4.0, 14.6, -5.5, 3.8, 2.8, 20, P_FRANJA)]):
        corpo.append(pena(f"peito{k}", (x, y, z), -90, 1, L, W, par, flare=fl, T=1.0))
    # pescoço longo e curvo: base larga + parte de cima inclinada para a frente (cabeça à frente do peito)
    def cor_pesc(p, f_):
        x, y, z = p
        a = z if f_ in ("east", "west") else x
        base = CIANO if (f_ == "north" or z < -3.8) else mix(AZUL, CIANO, 0.3)
        return tom(base, -0.16) if escama(a, y, 2.0, 1.4) else base
    mp = mat_cor(cor_pesc, borda=.0, curva=.3)
    pesc = []
    pesc += g.octogono("pescoco_base", [-2.6, 23.6, -3.8], [2.6, 28.6, 1.4], mp, r=0.9, faixa=(23, 31))
    pesc.append(osso("pescoco_alto", [0, 28.0, -1.0], [-10, 0, 0],
                     g.octogono("pescoco_alto", [-2.3, 27.2, -4.4], [2.3, 31.0, 0.2], mp, r=0.8, faixa=(23, 31))))
    pesc.append(osso("cabeca", [0, 30.4, -2.4], [-ROT_PESC, 0, 0], cabeca_ossos()))
    corpo.append(osso("pescoco", [0, 25.0, -1.0], [ROT_PESC, 0, 0], pesc))
    corpo += manto_ossos()
    corpo.append(asa_ossos(-1)); corpo.append(asa_ossos(1))
    corpo.append(osso("cauda", [0, 20.8, 3.4], [0, 0, 0], [corrente(n, b, r, c) for n, b, r, c in CORRENTES]))
    g.transformar(i0, [o for o in corpo if isinstance(o, dict)], (0.0, 0.0, 0.0), sobe=SOBE_CORPO)
    tronco = osso("corpo", [0, 14.0 + SOBE_CORPO, 0.0], [0, 0, 0], corpo)
    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

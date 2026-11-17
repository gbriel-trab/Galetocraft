"""Cocórion (#005, Ar): o Galo dos Ventos, galo guerreiro branco de crista espetada, cicatrizes de batalha, asas em
capa com a espiral verde do vento, calça hakama preta com faixa branca e katana na cintura.

Reconstrução geométrica (pedido do dono): crista em poucas mechas grandes que afinam e varrem para trás, cabeça
em planos inclinados, tronco facetado com cintura estreita, asas em capa (escudo/folha) abertas em A com dentes
na borda, cauda de 5 penas largas e contínuas em arco, hakama em painéis inclinados e pernas com joelho."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
import previa                                  # só a matriz de rotação (mesma ordem do Blockbench)
from galo_base import peca, osso, mix, clamp, na_borda

ID = "cocorion"; NOME = "Cocórion"; NUMERO = 5
ALTURA = 2.4              # tabela oficial do dono (ferramentas/dimensoes.py): 2,40 × 1,50 × 2,70 blocos
ESCALA = 38.4 / 39        # o desenho é feito em 39 unidades e reduzido no fim para 38,4 (2,4 blocos)
QUADRUPEDE = False
ROSTO = ((0, 26.6 * ESCALA, -5.0 * ESCALA), 8.0 * ESCALA)
# penas da cauda (cadeias de 6 ossos) ondulam de leve
N_CAUDA, SEG_CAUDA = 5, 5
ONDAS = [(f"cauda{k}", SEG_CAUDA, (1.6, 1.2, 0.0)) for k in range(N_CAUDA)]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (amostrada com PIL nos PNGs da ficha; veja modelos/cocorion/detalhes.md) ----------------
# A ficha renderizada mostra o creme em (243,227,215) nas faces claras e (207,190,184) na sombra. O jogo e a prévia
# já escurecem as faces (de frente ~0,8; de lado e de trás ~0,6), então a textura usa um creme bem claro.
BRANCO_F = (255, 236, 220); CLARO_F = (255, 244, 232); CINZA_F = (224, 198, 186)   # proporção G/R e B/R da ficha
LINHA_F = (207, 198, 186)                 # borda de baixo das penas em escama (#CFC6BA)
CARVAO = (42, 43, 40); PRETO_H = (27, 28, 25)
VERDE = (58, 106, 48); VERDE_CL = (72, 124, 60); VERDE_ESC = (38, 78, 26)
AMAR = (255, 190, 12); AMAR_CL = (255, 208, 60); AMAR_ESC = (232, 140, 0)          # #F5B70A e sombra #E08A00
LARANJA_B = (238, 162, 10)                # mandíbula de baixo
VERM = (204, 52, 38); VERM_CL = (228, 62, 46); VERM_ESC = (150, 30, 22); VERM_X = (182, 40, 30)
OURO = (250, 184, 12); OURO_CL = (255, 214, 80); OURO_ESC = (190, 122, 8)
PRETO_SOB = (43, 41, 39)
GARRA = (46, 46, 46)                      # #2E2E2E

# Nas vistas de revisão o lado -x aparece à DIREITA de quem olha de frente: a katana fica do lado -x (na vista de
# frente da ficha, à direita de quem olha). O X da bochecha e a marca da testa ficam do lado +x, o que a arte
# principal mostra em 3/4; do outro lado (-x), só uma marca pequena na bochecha.
LADO_KATANA = -1
LADO_CICATRIZ = 1

def escuro(c): return (int(c[0] * .82), int(c[1] * .78), int(c[2] * .80))     # sombra clara e lilás, nunca cinza-escuro
def tons(c, f):
    f = clamp(f, -1, 1)
    return mix(c, CLARO_F, f) if f >= 0 else mix(c, escuro(c), -f)

def matriz(*rots):
    M = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    for r in rots: M = previa.mm(M, previa.rot(*r))
    return M

def mat_luz(cor_fn, M=None, borda=.16, grad=0.0, topo=.32, baixo=-.55):
    """Luz em 3 tons chapados pela normal NO MUNDO (osso girado ou não): face de cima clara, lados na cor base,
    face de baixo na sombra; fio leve na borda (a prévia e o jogo já sombreiam)."""
    borda = borda * 0.4
    def f(c):
        base = cor_fn(c)
        if base is None: return None
        nx, ny, nz = previa.mv(M, g.NORMAL[c["face"]]) if M else g.NORMAL[c["face"]]
        if ny > 0.6: k = topo
        elif ny < -0.6: k = baixo
        else: k = 0.04 * ny
        if grad:
            y0, y1 = c["faixa"]
            k += grad * (clamp((c["p"][1] - y0) / max(y1 - y0, 1e-6)) - 0.65)
        if na_borda(c): k -= borda
        return tons(base, k)
    return f

def cor_fixa(cor): return lambda c: cor

def escama(a, y, larg=1.6, alt=1.1):
    """Penas em escama (~4×3 px): fileiras desencontradas, cada pena com a borda de baixo em arco cinza-claro."""
    fila = math.floor(y / alt)
    fa = ((a + (fila % 2) * larg / 2) % larg) / larg
    fy = (y % alt) / alt
    return fy < 0.12 + 0.2 * (2 * abs(fa - 0.5)) ** 2

def risco_x(a, y, ca, cy, r, w=0.3, torto=0.0):
    """Cicatriz em X centrada em (ca, cy), braços de meia-diagonal r e espessura w ('torto' entorta em degraus)."""
    da, dy = a - ca, y - cy
    if max(abs(da), abs(dy)) > r: return False
    j = torto * math.sin(round(da * 2) * 1.7 + round(dy * 2) * 0.9)
    return abs(da - dy + j) < w or abs(da + dy - j) < w

def mancha(a, y, ca, cy):
    """Marca da testa: mancha irregular com respingos (como a ficha), não um asterisco simétrico."""
    da, dy = a - ca, y - cy
    blob = ((da / 0.55) ** 2 + (dy / 0.42) ** 2 <= 1) or ((da + 0.35) ** 2 + (dy - 0.25) ** 2 < 0.09)
    raios = any(abs(-math.sin(t) * da + math.cos(t) * dy) < 0.13 and 0 < (math.cos(t) * da + math.sin(t) * dy) < r
                for t, r in ((0.3, 1.0), (2.2, 0.9), (4.0, 0.85), (5.3, 0.7)))
    pingos = any((da - px) ** 2 + (dy - py) ** 2 < 0.03 for px, py in ((1.15, 0.5), (-1.0, -0.6), (0.4, -1.0)))
    return blob or raios or pingos

# ---------------- mecha (crista, juba, tufos) ----------------
def mecha(nome, raiz, rot, L, w, curva=6.0, gira=0, esp=0.5, cor_raiz=None):
    """Mecha de penas: base larga integrada ao crânio, 3 blocos encadeados que afinam e curvam aos poucos
    (curva graus a cada junta) e ponta em losango. Os blocos se sobrepõem nas juntas (sem frestas). Cresce em +y a
    partir da raiz; 'rot' aponta a mecha; 'gira' gira a lâmina em volta do próprio eixo (0: lâmina no plano y-z,
    larga vista de lado; 90: larga vista de frente)."""
    x, y, z = raiz
    partes = [(0.42, 1.0, 1.0), (0.33, 0.72, 0.85), (0.25, 0.45, 0.7)]      # (fração do comprimento, largura, espessura)
    M0 = matriz(rot, (0, gira, 0))
    def cor(y0):
        def f(c):
            t = clamp((c["p"][1] - y0) / L)
            return mix(cor_raiz or (250, 246, 242), (255, 253, 250), 0.3 * t)
        return f
    def seg(k, pos, M):
        px, py, pz = pos
        fl, fw, fe = partes[k]
        Lk = L * fl
        h = w * fw / 2; e = max(w * esp * fe / 2, 0.45)
        ov = 1.2 if k == 0 else 0.7
        m = mat_luz(cor(y - 0.0), M, borda=.12)
        filhos = [peca(f"{nome}_{k}", [px - e, py - ov, pz - h], [px + e, py + Lk, pz + h], m)]
        if k + 1 < len(partes):
            Mk = previa.mm(M, previa.rot(curva, 0, 0))
            filhos.append(osso(f"{nome}_{k + 1}", [px, py + Lk - 0.2, pz], [curva, 0, 0], [seg(k + 1, (px, py + Lk - 0.2, pz), Mk)]))
        else:
            q = h * 1.5 / 1.4142                    # losango da ponta (largura ~1,5 h)
            cy = py + Lk
            filhos.append(peca(f"{nome}_p", [px - e * 0.6, cy - q / 2, pz - q / 2], [px + e * 0.6, cy + q / 2, pz + q / 2],
                               mat_luz(cor(y), previa.mm(M, previa.rot(45, 0, 0)), borda=.12), rot=(45, 0, 0), pivo=(px, cy, pz)))
        return osso(f"{nome}_s{k}", [px, py, pz], [0, 0, 0], filhos)
    return osso(nome, list(raiz), list(rot), [osso(nome + "_g", list(raiz), [0, gira, 0], [seg(0, raiz, M0)])])


# ---------------- pena genérica (asas, gola, franja do peito) ----------------
def pena(nome, topo, L, w, esp, mat, rot=(0, 0, 0), eixo="x", fino=1.0):
    """Pena pendurada para baixo a partir de 'topo' (x, y, z): base larga (bloco até 58% do comprimento), meio
    mais estreito e ponta aguda em losango. eixo='x': a pena fica no plano y-z (espessura em x, asas);
    eixo='z': no plano x-y (espessura em z, penas de frente). 'rot' inclina a pena inteira no osso dela."""
    x, y, z = topo
    def caixa(nm, y0, y1, meia, e, **kw):
        if eixo == "x": return peca(nm, [x - e / 2, y0, z - meia], [x + e / 2, y1, z + meia], mat, **kw)
        return peca(nm, [x - meia, y0, z - e / 2], [x + meia, y1, z + e / 2], mat, **kw)
    w2 = 0.72 * w
    pc = [caixa(nome + "_a", y - 0.58 * L, y, w / 2, esp),
          caixa(nome + "_b", y - 0.86 * L, y - 0.5 * L, w2 / 2, esp * 0.85 * fino)]
    q = w2 / 1.4142; cy = y - 0.86 * L
    giro = (45, 0, 0) if eixo == "x" else (0, 0, 45)
    pc.append(caixa(nome + "_p", cy - q / 2, cy + q / 2, q / 2, esp * 0.7 * fino, rot=giro, pivo=(x, cy, z)))
    return osso(nome, [x, y, z], list(rot), pc)

# ---------------- cabeça ----------------
EY = 26.6                                   # altura do olho
FX, ZF, QX = 2.0, -7.0, 4.7                 # meia largura da frente, z da frente, meia largura do crânio
ZQ = ZF + (QX - FX)                         # z da quina de trás da face diagonal
FAC_T = 2.0
FAC_L = (QX - FX) * 1.4142
FAC_O = ((FX + QX) / 2, (ZF + ZQ) / 2)      # centro da face de fora (lado +x)
FAC_C = (FAC_O[0] - 0.7071 * FAC_T / 2, FAC_O[1] + 0.7071 * FAC_T / 2)
OLHO_U, OLHO_RU, OLHO_RV = 0.15, 1.6, 0.84  # olho ESTREITO (centro um pouco para trás)
SOB_K = 0.42                                # inclinação da sobrancelha (sobe para trás)
SOB_Y = 0.66                                # linha de baixo da sobrancelha no centro do olho
SOB_H = 1.05

def azulejo(a, y):
    """'Azulejos' de pena no rosto: linhas cinza-claro horizontais a cada 1,3 e juntas desencontradas."""
    fila = math.floor((y - 22.0) / 1.3)
    if (y - 22.0) % 1.3 < 0.16: return True
    return ((a + (fila % 2) * 0.9) % 1.8) < 0.14

def cor_rosto(c):
    x, y, z = c["p"]
    a = z if c["face"] in ("east", "west") else x
    return BRANCO_F

def olho(u, v):
    """Olho da ficha (neutra): estreito, o topo cortado na diagonal pela sobrancelha; íris verde-viva nos 2/3 do
    lado do bico, pupila preta junto à borda da frente com brilho; esclera branca pura atrás. Sem contorno."""
    du = u - OLHO_U
    ru, rv = OLHO_RU, OLHO_RV
    if abs(du) > ru or abs(v) > rv: return None
    cq = max(0.0, abs(du) - (ru - 0.35)) / 0.35, max(0.0, abs(v) - (rv - 0.35)) / 0.35
    if cq[0] ** 2 + cq[1] ** 2 > 1: return None
    corte = SOB_Y - 0.06 + SOB_K * du
    if v > corte: return None
    if du < ru / 3:                                              # 2/3 do lado do bico: íris
        pu = du + ru - 0.55                                      # pupila junto à borda da frente
        if (pu / 0.34) ** 2 + ((v + 0.05) / 0.5) ** 2 <= 1:
            if ((pu - 0.12) / 0.13) ** 2 + ((v - 0.18) / 0.13) ** 2 <= 1: return (255, 255, 255)
            return (10, 12, 10)
        return mix((70, 206, 50), (30, 140, 22), clamp((0.4 - v) / 1.2))
    return (255, 255, 255)

def mat_faceta(lado):
    """Face diagonal do rosto: olho inteiro numa face plana; X na bochecha do lado da arte, marca pequena do outro."""
    fora = "east" if lado > 0 else "west"
    def cor(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u, v = z - FAC_C[1], y - EY
            o = olho(u, v)
            if o is not None: return o
            if lado == LADO_CICATRIZ:                 # asterisco irregular sob o olho (X + traço curto)
                if risco_x(u, v, 0.3, -2.1, 0.75, 0.16, torto=0.08): return VERM
                if abs(v + 2.1) < 0.15 and abs(u - 0.3) < 0.7: return VERM
            else:                                       # 2 pontinhos e 1 risco curto no canto do olho
                if (u - 1.9) ** 2 + (v + 1.05) ** 2 < 0.04 or (u - 1.5) ** 2 + (v + 1.4) ** 2 < 0.04: return VERM
                if abs((v + 1.2) - 0.8 * (u - 2.3)) < 0.13 and abs(u - 2.3) < 0.4: return VERM
        return BRANCO_F
    base = mat_luz(cor, matriz((0, 45 * lado, 0)), borda=.0)
    def f(c):
        cc = cor(c)
        if cc != BRANCO_F and c["face"] == fora: return cc
        return base(c)
    return f

def mat_bico(M=None):
    def cor(c):
        x, y, z = c["p"]
        face = c["face"]
        if face in ("east", "west") and abs(z - (ZF - 1.1)) < 0.28 and abs(y - 25.85) < 0.25: return PRETO_H
        return AMAR if face != "down" else AMAR_ESC
    return mat_luz(cor, M, borda=.04, topo=.22, baixo=-.35)

def cor_testa(c):
    """Testa (plano inclinado): pequena cruz de traço fino com as pontas quebradas, acima e para dentro do olho do
    lado da arte (como na ficha)."""
    x, y, z = c["p"]
    if c["face"] == "north":
        da, dy = x - 1.05 * LADO_CICATRIZ, y - 29.35
        if max(abs(da), abs(dy)) < 0.65 and (abs(da - dy) < 0.15 or abs(da + dy) < 0.15): return VERM
        if (abs(da - 0.85) < 0.13 and abs(dy - 0.55) < 0.13) or (abs(da + 0.6) < 0.13 and abs(dy + 0.85) < 0.13): return VERM
    return cor_rosto(c)

def montar_cabeca():
    cab = []
    mb = mat_luz(cor_rosto, borda=.10)
    # crânio largo em cima (as têmporas abrem para fora) e afinando para o bico
    cab += g.arredondado2("cranio", [-QX, 23.0, ZQ - 0.3], [QX, 30.2, 2.2], mb, r=1.3)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((3.0 * lado, 5.3 * lado))
        cab.append(peca("tempora_" + s, [x0, 26.8, -4.6], [x1, 30.0, 1.6], mb, rot=(0, 0, -10 * lado),
                        pivo=(3.0 * lado, 26.8, -1.5)))
    # rosto em planos inclinados: frente de baixo reta, testa inclinada para trás, queixo recolhido
    cab.append(peca("rosto_frente", [-FX, 22.8, ZF], [FX, 27.4, ZQ + 0.2], mat_luz(cor_rosto, borda=.0), res=6))
    cab.append(peca("testa", [-2.3, 27.0, ZF + 0.1], [2.3, 30.2, ZQ + 0.6], mat_luz(cor_testa, matriz((16, 0, 0)), borda=.0),
                    rot=(16, 0, 0), pivo=(0, 27.0, ZF + 0.1), res=6))
    cab.append(peca("queixo", [-2.4, 21.8, ZF + 0.6], [2.4, 23.4, ZQ + 1.6], mb, rot=(-12, 0, 0), pivo=(0, 23.4, ZQ + 1.6)))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 22.8, cz - FAC_L / 2], [cx + FAC_T / 2, 29.6, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, EY, cz), res=8))
        # pálpebra de baixo: degrau creme sob o olho (o olho fica encaixado no rosto)
        xo = cx + FAC_T / 2 * lado
        # bochecha: plano que sobressai um pouco sob o olho (com a sobrancelha, o olho fica numa cavidade);
        # leva as cicatrizes da bochecha
        x0, x1 = sorted((xo - 0.3 * lado, xo + 0.3 * lado))
        cab.append(osso("bochecha_" + s, [cx, EY, cz], [0, 45 * lado, 0], [
            peca("bochecha_" + s, [x0, 22.9, cz - FAC_L / 2 + 0.1], [x1, EY - OLHO_RV + 0.02, cz + FAC_L / 2 + 0.4],
                 mat_faceta(lado), res=8)]))
        # sobrancelha: barra preta GROSSA, um pouco à frente do olho, descendo para o bico
        x0, x1 = sorted((xo - 0.3 * lado, xo + 0.28 * lado))
        yb = EY + SOB_Y
        msob = mat_luz(cor_fixa(PRETO_SOB), matriz((0, 45 * lado, 0), (-math.degrees(math.atan(SOB_K)), 0, 0)), borda=.0,
                       topo=.25, baixo=-.2)
        rs = (-math.degrees(math.atan(SOB_K)), 0, 0)
        cab.append(osso("sobrancelha_" + s, [cx, EY, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, yb, cz - FAC_L / 2 - 0.35], [x1, yb + 1.55, cz + 0.3], msob, rot=rs, pivo=(cx, yb, cz + OLHO_U)),
            peca("sobrancelha_b_" + s, [x0 + 0.02 * lado, yb, cz + 0.2], [x1 - 0.02 * lado, yb + 1.1, cz + FAC_L / 2 + 0.7], msob,
                 rot=rs, pivo=(cx, yb, cz + OLHO_U))]))
        yq = yb - SOB_K * (FAC_L / 2 + OLHO_U)
        x0, x1 = sorted((0.9 * lado, (FX + 0.35) * lado))
        cab.append(peca("sobrancelha_f_" + s, [x0, yq, ZF - 0.6], [x1, yq + 1.55, ZF + 0.3],
                        mat_luz(cor_fixa(PRETO_SOB), borda=.0, topo=.25), rot=(0, 0, 22 * lado), pivo=(FX * lado, yq, ZF)))
    # bico: de frente um trapézio largo em cima que afina para baixo; mandíbula de baixo laranja
    mbi = mat_bico()
    cab.append(peca("bico_cima", [-1.75, 25.3, ZF - 3.1], [1.75, 26.35, ZF + 0.4], mbi, res=4))
    cab.append(peca("bico_meio", [-1.25, 24.45, ZF - 3.3], [1.25, 25.4, ZF + 0.4], mbi, res=4))
    cab.append(peca("bico_gancho", [-0.6, 24.35, ZF - 3.6], [0.6, 25.9, ZF - 2.95], mbi, res=4))
    cab.append(peca("bico_baixo", [-0.95, 23.55, ZF - 2.5], [0.95, 24.5, ZF + 0.3],
                    mat_luz(cor_fixa(LARANJA_B), borda=.12, topo=.1), res=4))
    # barbelas: dois blocos vermelhos LARGOS lado a lado (juntos, a largura do bico), ~1,3× a altura do bico,
    # com uma linha vermelho-escura entre eles; o de cá um pouco mais comprido
    def cor_barb(c):
        x = c["p"][0]
        if abs(x) < 0.22: return VERM_ESC
        return mix((228, 52, 40), (196, 40, 30), clamp((23.2 - c["p"][1]) / 3.0))
    mbar = mat_luz(cor_barb, borda=.3, topo=.1)
    for lado, fim in ((-1, 21.2), (1, 21.6)):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.0, 1.75 * lado))
        x2, x3 = sorted((0.25 * lado, 1.45 * lado))
        cab.append(osso("barbela_" + s, [0.0, 23.7, ZF - 1.0], [0, 0, -2 * lado], [
            peca("barbela_a_" + s, [x0, fim + 0.6, ZF - 1.8], [x1, 23.7, ZF - 0.3], mbar, res=4),
            peca("barbela_b_" + s, [x2, fim, ZF - 1.6], [x3, fim + 0.7, ZF - 0.5], mbar, res=4)]))
    # crista: base comum integrada ao alto e à nuca do crânio; mechas volumosas que afinam, mais baixas e mais
    # inclinadas para trás quanto mais atrás nascem; penas secundárias menores; tudo levemente assimétrico
    crista = []
    mbase = mat_luz(lambda c: mix(BRANCO_F, CLARO_F, 0.2), matriz((22, 0, 0)), borda=.1)
    crista += g.arredondado("crista_base", [-3.2, 28.2, -4.6], [3.2, 31.2, 3.2], mbase, r=0.6, rot=(22, 0, 0), pivo=(0, 29.0, 0))
    crista += [
        # franja da testa: mechas curtas que descem até ~1 un. acima das sobrancelhas
        mecha("franja_c", (-0.6, 31.4, -5.0), (-156, 0, -8), 2.4, 2.8, curva=6, gira=90),
        # mecha central larga (base de 6 un.), inclinada ~25° para trás
        mecha("crista_1", (0.0, 30.6, -2.6), (25, 0, 2), 8.2, 6.0, curva=9),
        mecha("crista_2", (0.5, 30.6, -0.4), (56, 0, -4), 8.6, 5.4, curva=9),
        mecha("crista_3", (-0.3, 29.8, 1.6), (78, 0, 5), 8.0, 5.0, curva=8),
        mecha("crista_4", (0.3, 27.8, 2.6), (96, 0, -3), 6.8, 4.6, curva=6),
        mecha("crista_5", (0.0, 25.4, 2.6), (114, 0, 0), 5.4, 4.2, curva=5),
        mecha("crista_6", (0.0, 23.0, 1.8), (132, 0, 0), 4.2, 3.4, curva=4),
        # secundárias dos lados; o lado esquerdo do personagem (+x) é mais cheio e mais alto
        mecha("crista_d", (-1.9, 29.8, -1.4), (42, 0, 16), 6.2, 3.8, curva=8),
        mecha("crista_e", (1.9, 30.4, -2.0), (30, 0, -12), 6.8, 3.8, curva=8),
        mecha("crista_e2", (2.2, 30.6, 0.4), (60, 0, -18), 6.4, 3.6, curva=8),
        mecha("crista_do", (-2.4, 29.6, -2.6), (20, 0, 32), 5.4, 3.6, curva=7, gira=90),
        mecha("crista_eo", (2.3, 30.4, -1.4), (24, 0, -28), 7.4, 3.6, curva=7, gira=90),
        # espinhos das têmporas, apontando para fora (de frente e de trás)
        mecha("orelha_d1", (-3.8, 28.4, -1.4), (24, 0, 76), 4.8, 3.4, curva=6, gira=90),
        mecha("orelha_e1", (3.8, 28.8, -1.0), (28, 0, -72), 5.2, 3.4, curva=6, gira=90),
        # penas pontudas varridas para trás na lateral da cabeça (atrás do olho)
        mecha("lado_d", (-3.6, 26.4, 0.4), (78, 0, 24), 4.4, 3.2, curva=6),
        mecha("lado_e", (3.6, 26.6, 0.4), (76, 0, -26), 4.8, 3.2, curva=6),
        mecha("lado_d2", (-3.9, 24.2, -1.2), (88, 0, 16), 4.0, 3.0, curva=5),
        mecha("lado_e2", (3.9, 24.4, -1.0), (86, 0, -18), 4.2, 3.0, curva=5),
    ]
    cab.append(osso("crista", [0, 30.0, 0], [0, 0, 0], crista))
    return osso("cabeca", [0, 24.0, -1.5], [0, 0, 0], cab)

# ---------------- tronco ----------------
def cor_tronco(c):
    """Peito em penas de escama; X vermelho grande, de traço irregular em degraus com pontinhos escuros."""
    x, y, z = c["p"]
    face = c["face"]
    if face == "north" and z < -4.5:
        if risco_x(x, y, 0.0, 17.4, 2.9, 0.42, torto=0.08):                # X grande, cruzamento no meio do peito
            pontas = max(abs(x), abs(y - 17.4)) > 2.4
            return (142, 31, 26) if pontas and (round(x * 2) + round(y * 2)) % 2 == 0 else VERM_X
    a = z if face in ("east", "west") else x
    if face != "up" and escama(a, y): return mix(BRANCO_F, LINHA_F, 0.4)
    return BRANCO_F

def montar_tronco():
    """Tronco de ave: núcleo que afunila até a cintura; peito em quilha (dois planos inclinados que se encontram
    numa aresta no meio, projeção moderada), faceta de baixo que recolhe para a cintura, facetas dos lados e
    ombros inclinados. Camadas discretas de penas: gola em 2 fileiras e uma franja de pontas sobre a faixa."""
    pc = []
    mt = mat_luz(cor_tronco, borda=.08)
    pc += g.arredondado2("tronco", [-3.3, 12.4, -4.2], [3.3, 20.0, 3.4], mt, r=1.0, res=3)
    pc.append(peca("peito", [-1.7, 14.0, -6.8], [1.7, 20.6, -4.4], mat_luz(cor_tronco, matriz((-10, 0, 0)), borda=.08),
                   rot=(-10, 0, 0), pivo=(0, 14.0, -6.6), res=3))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((1.7 * lado, 4.0 * lado))
        pc.append(peca("peito_" + s, [x0, 14.0, -6.8], [x1, 20.4, -4.4], mat_luz(cor_tronco, matriz((-10, -30 * lado, 0)), borda=.08),
                       rot=(-10, -30 * lado, 0), pivo=(1.7 * lado, 14.0, -6.8), res=3))
        x0, x1 = sorted((2.6 * lado, 4.6 * lado))
        pc.append(peca("peito_lado_" + s, [x0, 14.4, -5.0], [x1, 19.8, -2.8], mat_luz(cor_tronco, matriz((-6, -50 * lado, 0)), borda=.08),
                       rot=(-6, -50 * lado, 0), pivo=(2.6 * lado, 14.4, -5.0), res=3))
        x0, x1 = sorted((2.2 * lado, 5.0 * lado))
        pc.append(peca("ombro_" + s, [x0, 17.8, -4.2], [x1, 20.6, 2.6], mt, rot=(0, 0, 20 * lado), pivo=(2.2 * lado, 20.6, 0)))
    pc.append(peca("peito_baixo", [-2.6, 12.6, -5.9], [2.6, 15.4, -3.8], mat_luz(cor_tronco, matriz((26, 0, 0)), borda=.08),
                   rot=(26, 0, 0), pivo=(0, 15.4, -5.6), res=3))
    mg = mat_luz(lambda c: mix(BRANCO_F, CLARO_F, 0.3), borda=.2)
    # gola: 2 fileiras de penas na base do pescoço (desencontradas)
    for k, x in enumerate((-3.0, -1.0, 1.0, 3.0)):
        pc.append(pena(f"gola_b{k}", (x, 22.0, -6.6 + 0.25 * abs(x)), 2.2, 2.2, 0.6, mg, eixo="z", rot=(6, 0, 0)))
    # franja do peito sobre a faixa (transição para a cintura)
    for k, x in enumerate((-2.4, -0.8, 0.8, 2.4)):
        pc.append(pena(f"franja{k}", (x, 14.8, -6.5 + 0.2 * abs(x)), 2.2, 1.9, 0.7, mg, eixo="z", rot=(-12, 0, 0)))
    return pc

def cor_hakama(c):
    x, y, z = c["p"]
    face = c["face"]
    a = z if face in ("east", "west") else x
    if y < 7.0 and face != "down": return PRETO_H                    # barra
    return CARVAO if math.floor((a + 0.3) / 1.9) % 2 == 0 else (52, 54, 56)   # painéis largos

# ---------------- asas ----------------
# glifo do vento: "9"/"G" de traço fino, ~1¼ volta aberta com o miolo no terço de cima e uma cauda longa que
# desce na diagonal para trás por ~metade da asa e termina num ganchinho
def _curva_glifo():
    pts = []
    te = 2.5 * math.pi
    for k in range(60):
        th = te * k / 59
        r = 0.45 + 0.42 * th
        ph = te - th - math.pi / 2                     # sentido horário: termina embaixo, indo para trás
        pts.append((r * math.cos(ph), r * math.sin(ph)))
    ue, ve = pts[-1]
    return pts + [(ue - 1.0, ve - 1.2), (ue - 2.0, ve - 2.6), (ue - 2.6, ve - 3.4), (ue - 3.1, ve - 3.5), (ue - 3.4, ve - 3.0)]
GLIFO_P = _curva_glifo()
GLIFO_C = (13.2, -0.6)                   # (y, z) do centro da espiral (terço de cima da asa)
GLIFO_K = 0.72                           # escala do desenho (cabe na pena grande do meio)
GLIFO_W = 0.62 / 0.72                           # meia espessura do traço

def _dist_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = clamp(((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy + 1e-9))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

def glifo(y, z):
    """a = para a frente (-z), v = para cima: a cauda do glifo desce para trás nas duas asas."""
    a, v = -(z - GLIFO_C[1]) / GLIFO_K, (y - GLIFO_C[0]) / GLIFO_K
    if not (-9.0 < a < 4.5 and -10.0 < v < 4.5): return False
    return any(_dist_seg(a, v, *GLIFO_P[i], *GLIFO_P[i + 1]) < GLIFO_W for i in range(len(GLIFO_P) - 1))

def mat_asa(lado, M, glifo_ok=True, cor=BRANCO_F):
    fora = "east" if lado > 0 else "west"
    def c_(c):
        x, y, z = c["p"]
        if glifo_ok and c["face"] == fora and glifo(y, z): return VERDE
        if c["face"] == fora and cor == BRANCO_F and escama(z, y, 2.4, 2.0): return mix(BRANCO_F, LINHA_F, 0.4)
        return cor
    m = mat_luz(c_, M, borda=.14)
    def f(c):
        if glifo_ok and c["face"] == fora and glifo(c["p"][1], c["p"][2]): return VERDE
        return m(c)
    return f

def montar_asa(lado):
    """Asa em capa feita de PENAS 3D sobrepostas como escamas alongadas (não placas): ombro integrado ao tronco,
    fileira de cobertura curta por fora, uma pena grande no meio que carrega a espiral inteira (sem fragmentar),
    primárias longas e pontudas de comprimentos diferentes atrás e embaixo, e pontas verdes na camada de dentro.
    Abre em A para fora e inclina para trás embaixo."""
    s = "d" if lado < 0 else "e"
    xi = 2.8 * lado
    PIV = (xi, 21.6, -6.0)
    ROT = (-12, 27 * lado, 5 * lado)
    M = matriz(ROT)
    def X(d): return xi + d * lado                   # posição em x a 'd' para fora da face de dentro
    pc = []
    # ombro integrado (volume arredondado que nasce do ombro do tronco)
    x0, x1 = sorted((X(-0.6), X(2.4)))
    pc += g.arredondado("asa_ombro_" + s, [x0, 17.8, -5.6], [x1, 22.0, 1.4], mat_asa(lado, M, glifo_ok=False), r=1.0)
    # primárias (camada de trás e de baixo): longas, pontudas, comprimentos diferentes, varrendo para trás
    for k, (z, topo, L, w) in enumerate(((-4.6, 17.2, 11.0, 2.8), (3.6, 18.0, 12.6, 3.0), (5.8, 17.4, 11.8, 2.8),
                                         (7.8, 16.0, 9.6, 2.6), (-2.2, 12.2, 6.8, 2.4))):
        inc = 2 + 2.5 * max(z, 0) / 2
        pc.append(pena(f"asa_pri{k}_{s}", (X(0.75), topo, z), L, w, 1.1, mat_asa(lado, matriz(ROT, (inc, 0, 0)), glifo_ok=False),
                       rot=(inc, 5 * lado * (1 if k % 2 else -1), 0)))
    # pontas verdes por dentro
    for k, (z, L) in enumerate(((-3.4, 5.0), (-0.2, 5.6), (2.6, 5.4), (5.0, 4.6))):
        pc.append(pena(f"asa_v{k}_{s}", (X(0.1), 10.8, z), L, 1.8, 0.8, mat_asa(lado, matriz(ROT, (6, 0, 0)), glifo_ok=False, cor=VERDE),
                       rot=(6 + 2 * k, 0, 0)))
    # pena grande do meio: carrega a espiral inteira numa face só
    pc.append(pena("asa_espiral_" + s, (X(1.25), 18.8, -0.6), 12.4, 7.2, 1.3, mat_asa(lado, M)))
    # cobertura: penas curtas e largas por fora, logo abaixo do ombro
    for k, (z, L) in enumerate(((-4.4, 5.0), (-1.6, 5.4), (1.2, 5.2), (3.8, 4.4))):
        inc = 3 + 2 * k
        pc.append(pena(f"asa_cob{k}_{s}", (X(2.0), 21.2, z), L, 3.2, 1.1, mat_asa(lado, matriz(ROT, (inc, 0, 0)), glifo_ok=False),
                       rot=(inc, -4 * lado, 0)))
    return osso("asa_" + s, list(PIV), list(ROT), pc)

# ---------------- cauda ----------------
def mat_pena_cauda(M, t0, t1, verde):
    """Pena da cauda, alternando por pena como na ficha: as de fora são creme, com o verde-escuro só embaixo perto
    da base; as de trás são verde-escuras com o último terço creme. A face de baixo fica na sombra verde funda."""
    def cor(c):
        (_, y0, z0), (_, y1, z1) = c["b"]
        fy = (c["p"][1] - y0) / max(y1 - y0, 1e-6)
        t = t0 + (t1 - t0) * clamp((c["p"][2] - z0) / max(z1 - z0, 1e-6))
        face = c["face"]
        if verde:
            if t > 0.66 or face in ("south",): return BRANCO_F
            return VERDE_ESC if face == "down" else VERDE
        if face in ("up", "south", "north"): return BRANCO_F
        if t < 0.6 and (face == "down" or fy < 0.42): return VERDE_ESC if face == "down" else VERDE
        return BRANCO_F
    return mat_luz(cor, M, borda=.14)

def pena_cauda(nome, raiz, rot0, curvas, L, H, esp, verde=False):
    """Pena em foice: 5 blocos encadeados e sobrepostos nas juntas (sem frestas), estreita na raiz, larga no meio,
    ponta afiada em losango; 'curvas' dá o giro de cada junta (sobe e depois dobra a ponta para baixo)."""
    fr = [0.2, 0.22, 0.22, 0.2, 0.16]
    alt = [0.42, 0.85, 1.0, 0.78, 0.46]
    ee = [0.8, 1.0, 1.0, 0.9, 0.75]
    n = len(fr)
    def seg(k, pos, M, t0):
        px, py, pz = pos
        h = H * alt[k]; Ls = L * fr[k]; e = esp * ee[k]
        r = list(rot0) if k == 0 else [curvas[k - 1], 0, 0]
        Mk = previa.mm(M, previa.rot(*r))
        t1 = t0 + fr[k]
        m = mat_pena_cauda(Mk, t0, t1, verde)
        ov = 0.9 if k > 0 else 0.4
        filhos = [peca(f"{nome}_{k}", [px - e / 2, py - h * 0.5, pz - ov], [px + e / 2, py + h * 0.5, pz + Ls], m, res=3)]
        if k + 1 < n:
            filhos.append(seg(k + 1, (px, py, pz + Ls - 0.1), Mk, t1))
        else:
            q = h * 1.15 / 1.4142
            filhos.append(peca(f"{nome}_pt", [px - e * 0.4, py - q / 2, pz + Ls - q / 2], [px + e * 0.4, py + q / 2, pz + Ls + q / 2],
                               mat_pena_cauda(previa.mm(Mk, previa.rot(45, 0, 0)), 0.95, 1.0, verde), rot=(45, 0, 0),
                               pivo=(px, py, pz + Ls), res=3))
        return osso(f"{nome}_{k}", list(pos), r, filhos)
    return seg(0, raiz, matriz(), 0.0)

def montar_cauda():
    """Leque alto e curvo: 5 penas principais saindo de uma raiz estreita atrás da cintura, abertas de +70° (sobe
    logo atrás da crista) a -50° (desce perto do joelho); cada uma sobe e dobra a ponta para baixo (foice).
    Alternância creme/verde por pena; 2 penas verdes secundárias atrás, entre as principais."""
    penas = []
    # (raiz y, z, elevação, curvas das juntas, comprimento, altura, espessura, verde)
    P = [(16.6, 4.4, 70, (-2, 4, 10, 14), 13.0, 4.6, 1.8, False),
         (16.0, 4.6, 45, (-3, 2, 8, 12), 18.5, 5.0, 1.6, True),
         (15.2, 4.8, 15, (-4, 0, 6, 10), 25.0, 5.6, 1.8, False),
         (14.4, 4.8, -20, (-4, -2, 2, 6), 21.0, 5.2, 1.6, True),
         (13.6, 4.6, -50, (-2, -2, 0, 4), 12.0, 4.4, 1.8, False)]
    for k, (y, z, e, cv, L, H, esp, vd) in enumerate(P):
        x = 0.25 if k % 2 else -0.25
        penas.append(pena_cauda(f"cauda{k}", (x, y, z), (-e, 0, 0), cv, L, H, esp, vd))
    for k, (y, e, L, x) in enumerate(((15.6, 30, 15.0, 1.0), (14.8, -2, 17.0, -1.0))):
        penas.append(pena_cauda(f"cauda_sec{k}", (x, y, 4.4), (-e, 6 if x > 0 else -6, 0), (-3, 0, 6, 10), L, 3.6, 1.1, True))
    return osso("cauda", [0, 14.4, 4.4], [0, 0, 0], penas)

# ---------------- katana ----------------
def mat_metal(cima, frente, lado, baixo):
    return g.mat_facetado(cima, frente, lado, baixo, quina=-0.3)

def mat_cabo(c):
    """Cabo da katana: verde-escuro com uma fileira de quadrados claros no meio de cada face (amarração)."""
    x, y, z = c["p"]
    t = (z - c["b"][0][2]) % 1.2
    meio = abs((c["j"] + 0.5) / c["th"] - 0.5) if c["face"] in ("east", "west") else abs((c["i"] + 0.5) / c["tw"] - 0.5)
    if c["face"] in ("east", "west", "up", "down") and 0.3 < t < 0.9 and meio < 0.3: return BRANCO_F
    return VERDE_ESC if na_borda(c) else VERDE

def montar_katana(base):
    """Katana ao longo de z (frente = -z) a partir da guarda (tsuba), em 'base': cabo para a frente, bainha preta
    para trás e para baixo, saindo atrás do quadril (como na arte)."""
    bx, by, bz = base
    def pc_(nome, de, ate, mat, **kw):
        return g.peca(nome, [de[0] + bx, de[1] + by, de[2] + bz], [ate[0] + bx, ate[1] + by, ate[2] + bz], mat, **kw)
    ouro = mat_metal(OURO_CL, OURO, mix(OURO, OURO_ESC, .4), OURO_ESC)
    bainha = mat_metal((70, 72, 78), (36, 38, 42), (28, 30, 34), (16, 16, 20))
    pc = [pc_("katana_cabo", [-0.75, -0.75, -7.0], [0.75, 0.75, -0.3], mat_cabo, res=4),
          pc_("katana_pomo", [-0.85, -0.85, -7.7], [0.85, 0.85, -6.95], ouro, res=4)]
    # tsuba em cruz dourada, ~4×4 un.
    pc += [pc_("katana_tsuba_a", [-2.0, -0.7, -0.4], [2.0, 0.7, 0.2], ouro, res=4),
           pc_("katana_tsuba_b", [-0.7, -2.0, -0.35], [0.7, 2.0, 0.15], ouro, res=4)]
    pc += [pc_("katana_habaki", [-0.7, -0.75, 0.1], [0.7, 0.75, 0.9], ouro, res=4),
           pc_("katana_bainha", [-0.6, -0.75, 0.8], [0.6, 0.75, 15.0], bainha),
           pc_("katana_kurikata", [-0.7, -0.85, 2.2], [0.7, 0.85, 2.9], mat_metal(OURO_CL, OURO, OURO, OURO_ESC), res=4),
           pc_("katana_kojiri", [-0.65, -0.8, 14.8], [0.65, 0.8, 16.2], ouro, res=4)]
    return pc

# ---------------- montagem ----------------
def montar():
    corpo = []
    corpo += montar_tronco()
    # cintura da hakama (estreita) e faixa branca horizontal bem visível, com nó no centro e tiras que nascem dele
    mh = mat_luz(cor_hakama, borda=.1, topo=.15, baixo=-.4)
    corpo += g.arredondado("hakama_cint", [-4.4, 10.6, -5.6], [4.4, 14.0, 4.3], mh, r=0.4)
    mf = mat_luz(cor_fixa(BRANCO_F), borda=.14)
    corpo += g.arredondado("faixa", [-4.55, 13.0, -5.95], [4.55, 14.1, 4.55], mf, r=0.3)
    nx = -1.3                                         # nó à direita de quem olha (lado -x)
    corpo.append(peca("no_faixa", [nx - 0.8, 12.5, -6.7], [nx + 0.8, 14.4, -5.8], mf))
    corpo.append(peca("no_ponta1", [nx - 0.9, 7.8, -6.55], [nx - 0.1, 12.6, -6.1], mf, rot=(0, 0, -5), pivo=(nx - 0.5, 12.6, -6.3)))
    corpo.append(peca("no_ponta2", [nx + 0.1, 8.6, -6.55], [nx + 0.9, 12.6, -6.1], mf, rot=(0, 0, 5), pivo=(nx + 0.5, 12.6, -6.3)))
    # katana: tsuba na frente do quadril, cabo para cima, para a frente e para fora; bainha passa por fora da
    # hakama e sai atrás do quadril
    KAT = (5.4 * LADO_KATANA, 13.4, -6.2)
    corpo.append(osso("katana", list(KAT), [34, 26 * (-LADO_KATANA), 0], montar_katana(KAT)))
    pescoco = osso("pescoco", [0, 20.6, -2.0], [0, 0, 0], [
        *g.arredondado("pescoco_baixo", [-3.1, 19.4, -6.2], [3.1, 22.4, 1.0], mat_luz(cor_tronco, borda=.08), r=0.9),
        *g.arredondado("pescoco", [-2.3, 21.6, -5.6], [2.3, 24.4, 0.2], mat_luz(cor_tronco, borda=.08), r=0.7),
        montar_cabeca()])
    corpo.append(pescoco)
    for lado in (-1, 1):
        corpo.append(montar_asa(lado))
    corpo.append(montar_cauda())
    # dorso: capa contínua de penas creme do pescoço até a altura das coxas, em 2 camadas, borda denteada
    mc = mat_luz(lambda c: LINHA_F if c["face"] == "south" and escama(c["p"][0], c["p"][1], 2.4, 2.0) else BRANCO_F, borda=.2)
    corpo += g.arredondado("dorso", [-4.6, 9.4, 3.0], [4.6, 21.0, 5.0], mc, r=0.5)
    corpo += g.arredondado("dorso_cima", [-3.8, 15.4, 4.6], [3.8, 21.6, 6.0], mc, r=0.5)
    q = 2.6 / 1.4142
    for k, x in enumerate((-3.3, -1.1, 1.1, 3.3)):
        yb = 9.4 - (0.6 if k in (1, 2) else 0.0)
        corpo.append(peca(f"dorso_ponta{k}", [x - q / 2, yb - q / 2, 3.3], [x + q / 2, yb + q / 2, 4.8], mc,
                          rot=(0, 0, 45), pivo=(x, yb, 4.0)))
    for k, x in enumerate((-2.4, 0.0, 2.4)):
        corpo.append(peca(f"dorso_ponta_c{k}", [x - q / 2, 15.4 - q / 2, 4.8], [x + q / 2, 15.4 + q / 2, 5.9], mc,
                          rot=(0, 0, 45), pivo=(x, 15.4, 5.3)))
    tronco = osso("corpo", [0, 12.0, 0], [0, 0, 0], corpo)
    raizes = [tronco, perna(-1), perna(1)]
    g.transformar(0, raizes, (0.0, 0.0, 0.0), k=ESCALA)
    return raizes

def perna(lado):
    """Perna: hakama em 4 painéis inclinados e sobrepostos (abrem um pouco embaixo); perna amarela com joelho
    (canela de cima inclinada para a frente, tarso inclinado para trás) e escamas; pé grande com 3 dedos robustos
    e separados à frente, 1 atrás, garras cinza-carvão grandes."""
    s = "d" if lado < 0 else "e"; xc = 3.0 * lado; zc = 0.5 * lado
    pp = []
    def bx(a, b): return sorted((a * lado, b * lado))
    mh = mat_luz(cor_hakama, borda=.1, topo=.15, baixo=-.4)
    # painéis: frente de dentro, frente de fora, lado e trás (a barra abre para fora, para a frente e para trás)
    x0, x1 = bx(0.1, 3.0); pp.append(peca("hakama_fi_" + s, [x0, 6.4, -5.7], [x1, 12.0, -4.7], mh, rot=(6, 0, 3 * lado), pivo=(1.5 * lado, 12.0, -5.2)))
    x0, x1 = bx(2.6, 5.3); pp.append(peca("hakama_fo_" + s, [x0, 6.6, -5.3], [x1, 12.0, -4.3], mh, rot=(6, 0, 9 * lado), pivo=(3.9 * lado, 12.0, -4.8)))
    x0, x1 = bx(4.3, 5.3); pp.append(peca("hakama_l_" + s, [x0, 6.6, -4.6], [x1, 12.0, 3.8], mh, rot=(0, 0, 9 * lado), pivo=(4.8 * lado, 12.0, 0)))
    x0, x1 = bx(0.1, 5.1); pp.append(peca("hakama_t_" + s, [x0, 6.6, 3.0], [x1, 12.0, 4.0], mh, rot=(-6, 0, 5 * lado), pivo=(2.6 * lado, 12.0, 3.5)))
    x0, x1 = bx(0.2, 4.4); pp.append(peca("hakama_m_" + s, [x0, 7.4, -4.6], [x1, 12.0, 3.2], mh))
    # pregas com profundidade: tiras salientes, cada uma com inclinação um pouco diferente
    for k, (d, inc) in enumerate(((1.2, 7), (3.4, 4))):
        x0, x1 = bx(d - 0.35, d + 0.35)
        pp.append(peca(f"prega{k}_" + s, [x0, 6.5, -6.0], [x1, 11.8, -5.3], mh, rot=(inc, 0, (2 + 3 * k) * lado),
                       pivo=(d * lado, 11.8, -5.6)))
    # perna de ave: coxa curta saindo da hakama, joelho discreto, tarso fino com escamas, tornozelo
    ma = mat_luz(lambda c: AMAR if c["face"] != "down" else AMAR_ESC, borda=.12, topo=.2, baixo=-.3)
    pp.append(peca("coxa_" + s, [xc - 1.3, 5.4, zc - 1.4], [xc + 1.3, 8.4, zc + 1.4], ma, rot=(-12, 0, 0), pivo=(xc, 8.4, zc)))
    pp.append(peca("joelho_" + s, [xc - 1.05, 4.5, zc - 0.6], [xc + 1.05, 5.9, zc + 1.5], ma, rot=(-20, 0, 0), pivo=(xc, 5.2, zc + 0.5)))
    pp.append(peca("tarso_" + s, [xc - 0.85, 1.6, zc - 0.9], [xc + 0.85, 5.2, zc + 0.9], ma, rot=(8, 0, 0), pivo=(xc, 5.2, zc)))
    pp.append(peca("tornozelo_" + s, [xc - 1.05, 1.2, zc - 1.05], [xc + 1.05, 2.2, zc + 1.05], ma))
    # pé: 3 dedos bem definidos e separados à frente com garra escura; 1 dedo atrás
    mg = mat_luz(cor_fixa(GARRA), borda=.1, topo=.25)
    for nome, dx, ang in (("meio", 0.0, 0), ("fora", 1.3 * lado, 26 * lado), ("dentro", -1.3 * lado, -22 * lado)):
        x0 = xc + dx
        comp = 2.8 if nome == "meio" else 2.3
        pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, zc - 0.6], [0, -ang, 0], [
            peca(f"dedo_{nome}_{s}", [x0 - .75, 0, zc - 0.6 - comp], [x0 + .75, 1.9, zc + 0.7], ma),
            peca(f"garra_{nome}_{s}", [x0 - .6, 0.0, zc - 0.6 - comp - 1.4], [x0 + .6, 1.4, zc - 0.5 - comp], mg)]))
    pp.append(peca("dedo_tras_" + s, [xc - .6, 0, zc + 0.7], [xc + .6, 1.2, zc + 3.0], ma))
    pp.append(peca("garra_tras_" + s, [xc - .5, 0, zc + 2.9], [xc + .5, 0.9, zc + 3.9], mg))
    return osso("perna_" + s, [xc, 12.0, zc], [0, 0, 0], pp)

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

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
N_CAUDA, SEG_CAUDA = 5, 6
ONDAS = [(f"cauda{k}", SEG_CAUDA, (1.6, 1.2, 0.0)) for k in range(N_CAUDA)]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (amostrada com PIL nos PNGs da ficha; veja modelos/cocorion/detalhes.md) ----------------
# A ficha renderizada mostra o creme em (243,227,215) nas faces claras e (207,190,184) na sombra. O jogo e a prévia
# já escurecem as faces (de frente ~0,8; de lado e de trás ~0,6), então a textura usa um creme bem claro.
BRANCO_F = (255, 236, 220); CLARO_F = (255, 244, 232); CINZA_F = (224, 198, 186)   # proporção G/R e B/R da ficha
LINHA_F = (201, 194, 189)                 # borda de baixo das penas em escama (#C9C2BD)
CARVAO = (42, 43, 40); PRETO_H = (27, 28, 25)
VERDE = (58, 106, 48); VERDE_CL = (72, 124, 60); VERDE_ESC = (38, 78, 26)
AMAR = (255, 190, 12); AMAR_CL = (255, 208, 60); AMAR_ESC = (232, 140, 0)          # #F5B70A e sombra #E08A00
LARANJA_B = (240, 138, 12)                # mandíbula de baixo
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

def escama(a, y, larg=2.0, alt=1.5):
    """Penas em escama (~4×3 px): fileiras desencontradas, cada pena com a borda de baixo em arco cinza-claro."""
    fila = math.floor(y / alt)
    fa = ((a + (fila % 2) * larg / 2) % larg) / larg
    fy = (y % alt) / alt
    return fy < 0.2 + 0.25 * (2 * abs(fa - 0.5)) ** 2

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
def mecha(nome, raiz, rot, L, w, curva=6.0, gira=0, esp=0.7, cor_raiz=None):
    """Mecha de penas: base larga integrada ao crânio, 3 blocos encadeados que afinam e curvam aos poucos
    (curva graus a cada junta) e ponta em losango. Os blocos se sobrepõem nas juntas (sem frestas). Cresce em +y a
    partir da raiz; 'rot' aponta a mecha; 'gira' gira a lâmina em volta do próprio eixo (0: lâmina no plano y-z,
    larga vista de lado; 90: larga vista de frente)."""
    x, y, z = raiz
    partes = [(0.44, 1.0, 1.0), (0.32, 0.7, 0.85), (0.24, 0.44, 0.7)]       # (fração do comprimento, largura, espessura)
    M0 = matriz(rot, (0, gira, 0))
    def cor(y0):
        def f(c):
            t = clamp((c["p"][1] - y0) / L)
            return mix(cor_raiz or BRANCO_F, CLARO_F, 0.15 + 0.5 * t)
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
            q = h * 1.6 / 1.4142                    # losango da ponta (largura ~1,6 h)
            cy = py + Lk
            filhos.append(peca(f"{nome}_p", [px - e * 0.85, cy - q / 2, pz - q / 2], [px + e * 0.85, cy + q / 2, pz + q / 2],
                               mat_luz(cor(y), previa.mm(M, previa.rot(45, 0, 0)), borda=.12), rot=(45, 0, 0), pivo=(px, cy, pz)))
        return osso(f"{nome}_s{k}", [px, py, pz], [0, 0, 0], filhos)
    return osso(nome, list(raiz), list(rot), [osso(nome + "_g", list(raiz), [0, gira, 0], [seg(0, raiz, M0)])])

# ---------------- cabeça ----------------
EY = 26.6                                   # altura do olho
FX, ZF, QX = 2.0, -7.0, 4.7                 # meia largura da frente, z da frente, meia largura do crânio
ZQ = ZF + (QX - FX)                         # z da quina de trás da face diagonal
FAC_T = 2.0
FAC_L = (QX - FX) * 1.4142
FAC_O = ((FX + QX) / 2, (ZF + ZQ) / 2)      # centro da face de fora (lado +x)
FAC_C = (FAC_O[0] - 0.7071 * FAC_T / 2, FAC_O[1] + 0.7071 * FAC_T / 2)
OLHO_U, OLHO_RU, OLHO_RV = 0.15, 1.6, 0.72  # olho ESTREITO (centro um pouco para trás)
SOB_K = 0.42                                # inclinação da sobrancelha (sobe para trás)
SOB_Y = 0.52                                # linha de baixo da sobrancelha no centro do olho
SOB_H = 1.05

def azulejo(a, y):
    """'Azulejos' de pena no rosto: linhas cinza-claro horizontais a cada 1,3 e juntas desencontradas."""
    fila = math.floor((y - 22.0) / 1.3)
    if (y - 22.0) % 1.3 < 0.16: return True
    return ((a + (fila % 2) * 0.9) % 1.8) < 0.14

def cor_rosto(c):
    x, y, z = c["p"]
    a = z if c["face"] in ("east", "west") else x
    if c["face"] != "up" and azulejo(a, y): return mix(BRANCO_F, LINHA_F, 0.55)
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
            if lado == LADO_CICATRIZ:
                if risco_x(u, v, 0.3, -2.1, 0.9, 0.2, torto=0.12): return VERM
            else:
                if abs((v + 2.0) - 0.9 * (u - 0.2)) < 0.17 and abs(u - 0.2) < 0.45: return VERM
            if azulejo(u, y): return mix(BRANCO_F, LINHA_F, 0.55)
        return BRANCO_F
    base = mat_luz(cor, matriz((0, 45 * lado, 0)), borda=.0)
    def f(c):
        cc = cor(c)
        if cc not in (BRANCO_F,) and c["face"] == fora and cc != mix(BRANCO_F, LINHA_F, 0.55): return cc
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
    """Testa (plano inclinado): marca irregular com respingos acima da sobrancelha, do lado da arte."""
    x, y, z = c["p"]
    if c["face"] == "north" and mancha(x, y, 0.9 * LADO_CICATRIZ, 28.3): return VERM
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
        x0, x1 = sorted((xo - 0.3 * lado, xo + 0.25 * lado))
        cab.append(osso("palpebra_" + s, [cx, EY, cz], [0, 45 * lado, 0], [
            peca("palpebra_" + s, [x0, EY - OLHO_RV - 0.45, cz - FAC_L / 2 + 0.2], [x1, EY - OLHO_RV + 0.02, cz + FAC_L / 2],
                 mat_luz(cor_fixa(BRANCO_F), matriz((0, 45 * lado, 0)), borda=.1))]))
        # sobrancelha: barra preta GROSSA, um pouco à frente do olho, descendo para o bico
        x0, x1 = sorted((xo - 0.2 * lado, xo + 0.7 * lado))
        yb = EY + SOB_Y
        msob = mat_luz(cor_fixa(PRETO_SOB), matriz((0, 45 * lado, 0), (-math.degrees(math.atan(SOB_K)), 0, 0)), borda=.0,
                       topo=.25, baixo=-.2)
        cab.append(osso("sobrancelha_" + s, [cx, EY, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, yb, cz - FAC_L / 2 - 0.35], [x1, yb + SOB_H, cz + FAC_L / 2 + 1.1], msob,
                 rot=(-math.degrees(math.atan(SOB_K)), 0, 0), pivo=(cx, yb, cz + OLHO_U))]))
        yq = yb - SOB_K * (FAC_L / 2 + OLHO_U)
        x0, x1 = sorted((0.9 * lado, (FX + 0.35) * lado))
        cab.append(peca("sobrancelha_f_" + s, [x0, yq, ZF - 0.6], [x1, yq + SOB_H, ZF + 0.3],
                        mat_luz(cor_fixa(PRETO_SOB), borda=.0, topo=.25), rot=(0, 0, 22 * lado), pivo=(FX * lado, yq, ZF)))
    # bico: de frente um trapézio largo em cima que afina para baixo; mandíbula de baixo laranja
    mbi = mat_bico()
    cab.append(peca("bico_cima", [-1.75, 25.3, ZF - 3.1], [1.75, 26.35, ZF + 0.4], mbi, res=4))
    cab.append(peca("bico_meio", [-1.25, 24.45, ZF - 3.3], [1.25, 25.4, ZF + 0.4], mbi, res=4))
    cab.append(peca("bico_gancho", [-0.6, 23.95, ZF - 3.75], [0.6, 25.9, ZF - 2.95], mbi, res=4))
    cab.append(peca("bico_baixo", [-0.95, 23.55, ZF - 2.5], [0.95, 24.5, ZF + 0.3],
                    mat_luz(cor_fixa(LARANJA_B), borda=.12, topo=.1), res=4))
    # barbelas: dois blocos vermelhos LARGOS lado a lado (juntos, a largura do bico), ~1,3× a altura do bico,
    # com uma linha vermelho-escura entre eles; o de cá um pouco mais comprido
    def cor_barb(c):
        x = c["p"][0]
        if abs(x) < 0.22: return VERM_ESC
        return mix((228, 52, 40), (196, 40, 30), clamp((23.2 - c["p"][1]) / 3.0))
    mbar = mat_luz(cor_barb, borda=.3, topo=.1)
    for lado, fim in ((-1, 20.3), (1, 20.8)):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.0, 1.75 * lado))
        x2, x3 = sorted((0.25 * lado, 1.45 * lado))
        cab.append(osso("barbela_" + s, [0.0, 23.7, ZF - 1.0], [0, 0, -2 * lado], [
            peca("barbela_a_" + s, [x0, fim + 0.6, ZF - 1.8], [x1, 23.7, ZF - 0.3], mbar, res=4),
            peca("barbela_b_" + s, [x2, fim, ZF - 1.6], [x3, fim + 0.7, ZF - 0.5], mbar, res=4)]))
    # crista: coluna central estreita de mechas grandes que varrem para trás e para cima (~45°); a frente é baixa,
    # logo acima da sobrancelha; 1 a 2 pontas laterais quase horizontais por lado ("orelhas"), assimétricas
    crista = [
        mecha("crista_f", (0.3, 29.0, -5.0), (-6, 0, 0), 4.4, 3.0, curva=8),
        mecha("crista_1", (-0.3, 29.6, -3.2), (16, 0, 3), 10.0, 4.2, curva=7),
        mecha("crista_2", (0.4, 29.8, -0.9), (40, 0, -3), 10.6, 4.4, curva=8),
        mecha("crista_3", (-0.2, 29.0, 1.2), (60, 0, 4), 9.8, 4.0, curva=8),
        mecha("crista_4", (0.3, 27.4, 2.2), (82, 0, -3), 8.0, 3.6, curva=7),
        mecha("crista_5", (0.0, 25.0, 2.4), (104, 0, 0), 6.2, 3.4, curva=5),
        mecha("crista_6", (0.0, 22.8, 1.6), (126, 0, 0), 4.6, 3.0, curva=4),
        # mechas de lado da coluna (assimétricas)
        mecha("crista_d", (-1.8, 29.2, -1.8), (34, 0, 12), 7.6, 3.2, curva=8),
        mecha("crista_e", (1.8, 29.4, -2.4), (28, 0, -8), 6.8, 3.0, curva=8),
        # pontas laterais quase horizontais (de frente e de trás aparecem como 'orelhas')
        mecha("orelha_d1", (-3.8, 28.4, -1.4), (22, 0, 78), 6.6, 3.0, curva=6, gira=90),
        mecha("orelha_d2", (-3.6, 26.6, 0.8), (46, 0, 70), 5.0, 2.6, curva=6, gira=90),
        mecha("orelha_e1", (3.8, 28.8, -1.0), (26, 0, -74), 7.2, 3.0, curva=6, gira=90),
        mecha("orelha_e2", (3.6, 26.8, 1.0), (52, 0, -64), 4.4, 2.6, curva=6, gira=90),
    ]
    cab.append(osso("crista", [0, 30.0, 0], [0, 0, 0], crista))
    # tufos da bochecha (atrás do olho, para trás)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cab.append(mecha("bochecha_" + s, (4.0 * lado, 24.6, -2.4), (96, 0, -12 * lado), 4.6, 2.8, curva=6))
    return osso("cabeca", [0, 24.0, -1.5], [0, 0, 0], cab)

# ---------------- tronco ----------------
def cor_tronco(c):
    """Peito em penas de escama; X vermelho grande, de traço irregular em degraus com pontinhos escuros."""
    x, y, z = c["p"]
    face = c["face"]
    if face == "north" and z < -4.5:
        if risco_x(x, y, 0.0, 16.6, 2.7, 0.36, torto=0.14):
            return VERM_ESC if (round(x * 2) * 3 + round(y * 2)) % 5 == 0 else VERM_X
    a = z if face in ("east", "west") else x
    if face != "up" and escama(a, y): return LINHA_F
    return BRANCO_F

def montar_tronco():
    """Tronco anatômico: núcleo com cintura estreita, peito projetado e facetado, ombros largos chanfrados,
    gola de pontas de pena e pescoço mais estreito que a cabeça."""
    pc = []
    mt = mat_luz(cor_tronco, borda=.08)
    pc += g.arredondado2("tronco", [-3.5, 12.4, -4.6], [3.5, 20.4, 3.4], mt, r=1.0, res=3)
    # peito: bloco inclinado para a frente em cima + duas facetas laterais (contorno arredondado)
    pc.append(peca("peito", [-3.0, 14.2, -6.6], [3.0, 20.8, -3.8], mat_luz(cor_tronco, matriz((-10, 0, 0)), borda=.08),
                   rot=(-10, 0, 0), pivo=(0, 14.2, -5.0), res=3))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((2.6 * lado, 4.8 * lado))
        pc.append(peca("peito_lado_" + s, [x0, 14.6, -6.0], [x1, 20.2, -3.6],
                       mat_luz(cor_tronco, matriz((-6, -32 * lado, 0)), borda=.08), rot=(-6, -32 * lado, 0),
                       pivo=(2.6 * lado, 14.6, -6.0), res=3))
        # ombro chanfrado (mais largo que a cintura)
        x0, x1 = sorted((2.4 * lado, 5.4 * lado))
        pc.append(peca("ombro_" + s, [x0, 17.6, -4.4], [x1, 20.8, 2.8], mt, rot=(0, 0, 18 * lado), pivo=(2.4 * lado, 20.8, 0)))
    # gola: 2 fileiras de pontas de pena na base do pescoço
    mg = mat_luz(cor_fixa(BRANCO_F), borda=.2)
    for k, (x, y, zz) in enumerate([(-2.4, 20.6, -6.4), (-0.8, 20.4, -6.6), (0.8, 20.4, -6.6), (2.4, 20.6, -6.4),
                                    (-1.6, 21.6, -6.2), (0.0, 21.5, -6.4), (1.6, 21.6, -6.2)]):
        q = 1.7
        pc.append(peca(f"gola{k}", [x - q / 2, y - q / 2, zz], [x + q / 2, y + q / 2, zz + 0.9], mg, rot=(0, 0, 45),
                       pivo=(x, y, zz + 0.45)))
    return pc

def cor_hakama(c):
    x, y, z = c["p"]
    face = c["face"]
    a = z if face in ("east", "west") else x
    if y < 7.0 and face != "down": return PRETO_H                    # barra
    pre = (a + 0.3) % 1.6                                             # pregas
    if pre < 0.22: return PRETO_H
    return CARVAO if pre < 0.9 else (56, 58, 62)

# ---------------- asas ----------------
# glifo do vento: "9"/"G" de traço fino, ~1¼ volta aberta com o miolo no terço de cima e uma cauda longa que
# desce na diagonal para trás por ~metade da asa e termina num ganchinho
def _curva_glifo():
    pts = []
    te = 2.5 * math.pi
    for k in range(60):
        th = te * k / 59
        r = 0.35 + 0.36 * th
        ph = te - th + math.pi / 2                     # sentido horário: termina embaixo, indo para trás
        pts.append((r * math.cos(ph), r * math.sin(ph)))
    ue, ve = pts[-1]
    return pts + [(ue - 1.6, ve - 2.0), (ue - 3.2, ve - 4.2), (ue - 4.4, ve - 5.4), (ue - 4.9, ve - 4.9), (ue - 4.9, ve - 4.3)]
GLIFO_P = _curva_glifo()
GLIFO_C = (17.0, -0.6)                   # (y, z) do centro da espiral (terço de cima da asa)
GLIFO_W = 0.5                            # meia espessura do traço

def _dist_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = clamp(((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy + 1e-9))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

def glifo(y, z):
    """a = para a frente (-z), v = para cima: a cauda do glifo desce para trás nas duas asas."""
    a, v = -(z - GLIFO_C[1]), (y - GLIFO_C[0])
    if not (-9.0 < a < 4.5 and -10.0 < v < 4.5): return False
    return any(_dist_seg(a, v, *GLIFO_P[i], *GLIFO_P[i + 1]) < GLIFO_W for i in range(len(GLIFO_P) - 1))

def mat_asa(lado, M, glifo_ok=True, cor=BRANCO_F):
    fora = "east" if lado > 0 else "west"
    def c_(c):
        x, y, z = c["p"]
        if glifo_ok and c["face"] == fora and glifo(y, z): return VERDE
        if c["face"] == fora and cor == BRANCO_F and escama(z, y, 2.4, 2.0): return mix(BRANCO_F, LINHA_F, 0.6)
        return cor
    m = mat_luz(c_, M, borda=.14)
    def f(c):
        if glifo_ok and c["face"] == fora and glifo(c["p"][1], c["p"][2]): return VERDE
        return m(c)
    return f

def montar_asa(lado):
    """Asa em capa: desce do pescoço com o ombro inclinado e abre em A para fora até um pouco abaixo da barra
    da hakama. De lado tem forma de folha/escudo (estreita no ombro, larga no meio) e inclina ~18° para trás
    embaixo. Fileiras de penas sobrepostas (a de cima por fora), espiral do vento na face de fora, 5 dentes
    triangulares de comprimentos diferentes na borda de baixo (verdes por dentro) e pontas na borda de trás."""
    s = "d" if lado < 0 else "e"
    xi = 3.3 * lado
    T = 1.7
    PIV = (xi, 21.4, -5.6)
    ROT = (-18, 28 * lado, 15 * lado)
    M = matriz(ROT)
    ma, mp, mv = mat_asa(lado, M), mat_asa(lado, M, glifo_ok=False), mat_asa(lado, M, glifo_ok=False, cor=VERDE)
    def caixa(nome, y0, y1, z0, z1, extra, mat, dentro=0.0, **kw):
        xa, xb = sorted((xi + dentro * lado, xi + (T + extra) * lado))
        return peca(nome, [xa, y0, z0], [xb, y1, z1], mat, **kw)
    def dente(nome, yb, ytopo, zc, w, extra, mat, dentro=0.0, inclina=0.0):
        """Dente triangular: bloco + losango (quadrado girado 45°) que faz a ponta; 'inclina' gira o dente."""
        q = w / 1.4142
        osso_ = [caixa(nome, yb, ytopo, zc - w / 2, zc + w / 2, extra, mat, dentro),
                 caixa(nome + "_pt", yb - q / 2, yb + q / 2, zc - q / 2, zc + q / 2, extra - 0.06, mat, dentro + 0.03,
                       rot=(45, 0, 0), pivo=(xi, yb, zc))]
        return [osso(nome, [xi, ytopo, zc], [inclina, 0, 0], osso_)]
    pc = []
    # fileiras em escudo: estreita no ombro, larga no meio, afinando embaixo (camadas: a de cima por fora)
    pc.append(caixa("asa_a_" + s, 18.4, 21.8, -0.2, 4.2, 0.55, ma))
    pc.append(caixa("asa_b_" + s, 14.8, 19.0, -0.4, 9.4, 0.38, ma))
    pc.append(caixa("asa_c_" + s, 11.0, 15.4, -0.2, 11.0, 0.2, ma))
    pc.append(caixa("asa_d_" + s, 8.0, 11.6, 0.6, 10.4, 0.05, ma))
    # 5 dentes de comprimentos diferentes na borda de baixo; pontas verdes na camada de dentro
    for k, (z, L, inc) in enumerate(((1.8, 2.6, 0), (4.0, 3.6, 6), (6.2, 4.2, 10), (8.4, 3.4, 16), (10.2, 2.4, 22))):
        pc += dente(f"asa_p{k}_{s}", 8.4 - L, 8.6, z, 2.4, -0.15, mp, 0.1, inc)
    for k, (z, L) in enumerate(((2.9, 2.6), (5.1, 3.2), (7.3, 3.0), (9.3, 2.2))):
        pc += dente(f"asa_v{k}_{s}", 8.4 - L, 8.8, z, 1.6, -0.9, mv, 0.45, 8 + 4 * k)
    # pontas na borda de trás (penas que apontam para baixo e para trás)
    for k, (y0, z0) in enumerate(((18.4, 4.0), (14.8, 9.2), (11.0, 10.8))):
        pc += dente(f"asa_t{k}_{s}", y0 - 1.0, y0 + 0.8, z0, 2.2, 0.1 - 0.15 * k, mp, 0.15, 24)
    return osso("asa_" + s, list(PIV), list(ROT), pc)

# ---------------- cauda ----------------
def mat_pena_cauda(M):
    """Pena da cauda: metade de cima creme, metade de baixo verde-escura (de trás e por cima, creme)."""
    def cor(c):
        (_, y0, _), (_, y1, _) = c["b"]
        fy = (c["p"][1] - y0) / max(y1 - y0, 1e-6)
        face = c["face"]
        if face in ("up", "south", "north"): return BRANCO_F
        if face == "down" or fy < 0.5: return VERDE if fy > 0.12 or face == "down" else VERDE_ESC
        return BRANCO_F
    return mat_luz(cor, M, borda=.14)

def pena_cauda(nome, raiz, rot0, curva, L, H, esp):
    """Pena larga em foice: 6 blocos encadeados, sobrepostos nas juntas (sem frestas), que curvam aos poucos;
    a largura cresce da raiz estreita até o meio e a ponta afina em 3 degraus (o último em losango)."""
    fr = [0.17, 0.19, 0.19, 0.17, 0.15, 0.13]
    alt = [0.55, 0.85, 1.0, 0.92, 0.66, 0.4]
    ee = [0.8, 1.0, 1.0, 0.92, 0.82, 0.7]
    n = len(fr)
    def seg(k, pos, M):
        px, py, pz = pos
        h = H * alt[k]; Ls = L * fr[k]; e = esp * ee[k]
        r = list(rot0) if k == 0 else list(curva)
        Mk = previa.mm(M, previa.rot(*r))
        m = mat_pena_cauda(Mk)
        ov = 0.9 if k > 0 else 0.4
        # o eixo da pena fica na metade de cima dos blocos (a borda de baixo sobe aos poucos: foice)
        filhos = [peca(f"{nome}_{k}", [px - e / 2, py - h * 0.55, pz - ov], [px + e / 2, py + h * 0.45, pz + Ls], m, res=3)]
        if k + 1 < n:
            filhos.append(seg(k + 1, (px, py, pz + Ls - 0.1), Mk))
        else:
            q = h / 1.4142
            filhos.append(peca(f"{nome}_pt", [px - e * 0.45, py - q / 2, pz + Ls - q / 2], [px + e * 0.45, py + q / 2, pz + Ls + q / 2],
                               mat_pena_cauda(previa.mm(Mk, previa.rot(45, 0, 0))), rot=(45, 0, 0), pivo=(px, py, pz + Ls), res=3))
        return osso(f"{nome}_{k}", list(pos), r, filhos)
    return seg(0, raiz, matriz())

def montar_cauda():
    """5 penas LARGAS em foice, contínuas, empilhadas num arco que sobe para trás: a de cima vai na altura dos
    olhos, para trás e um pouco para cima (+22°); a de baixo desce até a barra da hakama (-50°). Raiz estreita na
    cintura, atrás do corpo; vãos escuros entre as pontas."""
    penas = []
    # (raiz y, z, elevação, ry, curva, comprimento, altura, espessura)
    P = [(15.0, 4.6, 22, -4, -3, 23.0, 7.0, 2.4), (14.2, 4.8, 4, 5, -3, 27.0, 7.6, 2.0),
         (13.4, 4.8, -14, -6, -2, 25.0, 7.2, 2.4), (12.6, 4.6, -32, 7, -1, 15.0, 6.4, 2.0),
         (11.8, 4.4, -50, -5, 0, 8.5, 5.4, 2.4)]
    for k, (y, z, e, ry, cv, L, H, esp) in enumerate(P):
        x = 0.3 if k % 2 else -0.3
        penas.append(pena_cauda(f"cauda{k}", (x, y, z), (-e, ry, 0), (cv, 0, 0), L, H, esp))
    return osso("cauda", [0, 13.4, 4.4], [0, 0, 0], penas)

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
    pc = [pc_("katana_cabo", [-0.5, -0.5, -5.0], [0.5, 0.5, -0.3], mat_cabo, res=4),
          pc_("katana_pomo", [-0.62, -0.62, -5.6], [0.62, 0.62, -4.95], ouro, res=4)]
    # tsuba em cruz dourada, ~3× a largura do cabo
    pc += [pc_("katana_tsuba_a", [-1.6, -0.6, -0.35], [1.6, 0.6, 0.2], ouro, res=4),
           pc_("katana_tsuba_b", [-0.6, -1.6, -0.3], [0.6, 1.6, 0.15], ouro, res=4)]
    pc += [pc_("katana_habaki", [-0.55, -0.6, 0.1], [0.55, 0.6, 0.8], ouro, res=4),
           pc_("katana_bainha", [-0.45, -0.6, 0.7], [0.45, 0.6, 12.5], bainha),
           pc_("katana_kurikata", [-0.55, -0.7, 2.0], [0.55, 0.7, 2.6], mat_metal(OURO_CL, OURO, OURO, OURO_ESC), res=4),
           pc_("katana_kojiri", [-0.5, -0.65, 12.3], [0.5, 0.65, 13.0], ouro, res=4)]
    return pc

# ---------------- montagem ----------------
def montar():
    corpo = []
    corpo += montar_tronco()
    # cintura da hakama (estreita) e faixa branca horizontal bem visível, com nó no centro e tiras que nascem dele
    mh = mat_luz(cor_hakama, borda=.1, topo=.15, baixo=-.4)
    corpo += g.arredondado("hakama_cint", [-4.4, 10.6, -5.4], [4.4, 12.8, 4.2], mh, r=0.4)
    mf = mat_luz(cor_fixa(BRANCO_F), borda=.14)
    corpo += g.arredondado("faixa", [-4.55, 12.2, -6.1], [4.55, 14.2, 4.5], mf, r=0.35)
    corpo.append(peca("no_faixa", [-0.9, 11.9, -6.9], [0.9, 14.5, -5.9], mat_luz(cor_fixa(CINZA_F), borda=.2)))
    corpo.append(peca("no_ponta1", [-0.95, 7.6, -6.75], [-0.1, 12.2, -6.25], mf, rot=(0, 0, -6), pivo=(-0.5, 12.2, -6.5)))
    corpo.append(peca("no_ponta2", [0.1, 8.3, -6.75], [0.95, 12.2, -6.25], mf, rot=(0, 0, 6), pivo=(0.5, 12.2, -6.5)))
    # katana: tsuba na frente do quadril, cabo para cima, para a frente e para fora; bainha passa por fora da
    # hakama e sai atrás do quadril
    KAT = (5.4 * LADO_KATANA, 13.4, -6.2)
    corpo.append(osso("katana", list(KAT), [30, 10 * (-LADO_KATANA), 0], montar_katana(KAT)))
    pescoco = osso("pescoco", [0, 20.6, -2.0], [0, 0, 0], [
        *g.arredondado("pescoco", [-2.6, 19.6, -6.0], [2.6, 24.2, 0.6], mat_luz(cor_tronco, borda=.08), r=0.8),
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
    # perna com joelho e escamas
    ma = mat_luz(lambda c: AMAR_ESC if c["face"] != "up" and (c["p"][1] % 1.1) < 0.18 else (AMAR if c["face"] != "down" else AMAR_ESC),
                 borda=.12, topo=.2, baixo=-.3)
    pp.append(peca("coxa_" + s, [xc - 1.45, 5.0, zc - 1.6], [xc + 1.45, 8.4, zc + 1.6], ma, rot=(-10, 0, 0), pivo=(xc, 8.4, zc)))
    pp.append(peca("tarso_" + s, [xc - 1.1, 1.4, zc - 1.15], [xc + 1.1, 5.6, zc + 1.15], ma, rot=(7, 0, 0), pivo=(xc, 5.6, zc - 0.3)))
    pp.append(peca("tornozelo_" + s, [xc - 1.3, 1.2, zc - 1.3], [xc + 1.3, 2.4, zc + 1.3], ma))
    # pé: 3 dedos robustos e separados à frente com garra grande; 1 dedo atrás
    mg = mat_luz(cor_fixa(GARRA), borda=.1, topo=.25)
    for nome, dx, ang in (("meio", 0.0, 0), ("fora", 1.6 * lado, 26 * lado), ("dentro", -1.6 * lado, -22 * lado)):
        x0 = xc + dx
        comp = 4.8 if nome == "meio" else 4.0
        pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, zc - 0.6], [0, -ang, 0], [
            peca(f"dedo_{nome}_{s}", [x0 - .8, 0, zc - 0.6 - comp], [x0 + .8, 1.9, zc + 0.8], ma),
            peca(f"garra_{nome}_{s}", [x0 - .7, 0.0, zc - 0.6 - comp - 1.5], [x0 + .7, 1.4, zc - 0.5 - comp], mg)]))
    pp.append(peca("dedo_tras_" + s, [xc - .8, 0, zc + 0.8], [xc + .8, 1.5, zc + 3.8], ma))
    pp.append(peca("garra_tras_" + s, [xc - .7, 0, zc + 3.7], [xc + .7, 1.1, zc + 5.0], mg))
    return osso("perna_" + s, [xc, 12.0, zc], [0, 0, 0], pp)

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

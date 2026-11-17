"""Cocórion (#005, Ar): o Galo dos Ventos, galo guerreiro branco de juba espetada, cicatrizes de batalha, asas em
mangas largas de quimono com a espiral verde do vento, calça hakama preta com faixa branca e katana na cintura."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
import previa                                  # só a matriz de rotação (mesma ordem do Blockbench)
from galo_base import peca, osso, mix, clamp, na_borda

ID = "cocorion"; NOME = "Cocórion"; NUMERO = 5
ALTURA = 2.0              # especificação do dono: 2 blocos (32 unidades) do chão à ponta da crista
ESCALA = 32 / 39          # o desenho é feito em 39 unidades e reduzido no fim para 32
QUADRUPEDE = False
ROSTO = ((0, 26.6 * 32 / 39, -5.0 * 32 / 39), 8.0 * 32 / 39)
# penas da cauda (cadeias de 5 ossos) ondulam de leve
ONDAS = [(f"cauda{k}", 5, (2.0, 1.5, 0.0)) for k in range(6)]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (da ficha) ----------------
BRANCO_F = (247, 235, 225); CLARO_F = (255, 250, 244); CINZA_F = (202, 195, 193)
CARVAO = (44, 46, 50); PRETO_H = (28, 29, 32)
VERDE = (28, 96, 55); VERDE_CL = (46, 124, 72); VERDE_ESC = (17, 64, 37)
AMAR = (253, 185, 0); AMAR_CL = (255, 214, 72); AMAR_ESC = (222, 132, 8)
VERM = (205, 44, 28); VERM_CL = (232, 74, 52); VERM_ESC = (146, 26, 22)
OURO = (246, 190, 30); OURO_CL = (255, 226, 110); OURO_ESC = (176, 112, 14)
PRETO_SOB = (30, 31, 36)
GARRA = (58, 58, 64)

# Nas vistas de revisão o lado -x aparece à DIREITA de quem olha de frente: katana e cicatrizes do rosto ficam do
# lado -x (na vista de frente da ficha, as duas ficam à direita de quem olha).
LADO_KATANA = -1
LADO_CICATRIZ = -1

def escuro(c): return (int(c[0] * .66), int(c[1] * .66), int(c[2] * .68))
def tons(c, f):
    """f > 0 clareia (para um branco quente), f < 0 escurece para uma sombra cinza (o branco vira cinza-claro)."""
    f = clamp(f, -1, 1)
    return mix(c, CLARO_F, f) if f >= 0 else mix(c, escuro(c), -f)

def matriz(*rots):
    M = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    for r in rots: M = previa.mm(M, previa.rot(*r))
    return M

def mat_luz(cor_fn, M=None, borda=.16, grad=0.0, topo=.32, baixo=-.62):
    """Luz em 3 tons chapados pela normal NO MUNDO (osso girado ou não): face de cima clara, lados na cor base
    (os de trás um pouco mais escuros), face de baixo na sombra; fio escuro na borda; 'grad' escurece de leve
    para baixo na faixa do grupo."""
    def f(c):
        base = cor_fn(c)
        if base is None: return None
        nx, ny, nz = previa.mv(M, g.NORMAL[c["face"]]) if M else g.NORMAL[c["face"]]
        if ny > 0.6: k = topo
        elif ny < -0.6: k = baixo
        else: k = 0.08 - 0.14 * max(0.0, nz) + 0.05 * ny - 0.04 * nx
        if grad:
            y0, y1 = c["faixa"]
            k += grad * (clamp((c["p"][1] - y0) / max(y1 - y0, 1e-6)) - 0.65)
        if na_borda(c): k -= borda
        return tons(base, k)
    return f

def cor_fixa(cor): return lambda c: cor

def risco_x(a, y, ca, cy, r, w=0.3):
    """Cicatriz em X centrada em (ca, cy), braços de meia-diagonal r e espessura w."""
    da, dy = a - ca, y - cy
    if max(abs(da), abs(dy)) > r: return False
    return abs(da - dy) < w or abs(da + dy) < w

def asterisco(a, y, ca, cy, r, w=0.17):
    """Cicatriz de 3 riscos cruzados (asterisco)."""
    da, dy = a - ca, y - cy
    if da * da + dy * dy > r * r: return False
    for ang in (90, 30, 150):
        t = math.radians(ang)
        if abs(-math.sin(t) * da + math.cos(t) * dy) < w: return True
    return False

# ---------------- espeto (juba, crista, tufos) ----------------
def espeto(nome, raiz, rot, L, w, cor_ponta=None):
    """Espeto grosso em degraus: 3 blocos que afinam até a ponta, girados 45° em volta do próprio eixo (seção em
    losango, as faces leem como facetas). Cresce em +y a partir da raiz; 'rot' aponta para onde quiser."""
    x, y, z = raiz
    M = matriz(rot, (0, 45, 0))
    def cor(c):
        t = clamp((c["p"][1] - y) / L)
        return mix(BRANCO_F, CLARO_F, 0.35 * t) if cor_ponta is None else mix(BRANCO_F, cor_ponta, t)
    m = mat_luz(cor, M, borda=.12)
    pcs = []
    for k, (a, b, s) in enumerate(((-1.0, 0.6, 1.0), (0.55, 0.85, 0.7), (0.8, 1.0, 0.38))):
        h = w * s / 2
        pcs.append(peca(f"{nome}_{k}", [x - h, y + a * (L if a > 0 else 1), z - h], [x + h, y + b * L, z + h], m))
    return osso(nome, list(raiz), list(rot), [osso(nome + "_g", list(raiz), [0, 45, 0], pcs)])

# ---------------- cabeça ----------------
EY = 26.6                                   # altura do olho
FX, ZF, QX = 2.0, -7.0, 4.7                 # meia largura da frente, z da frente, meia largura do crânio
ZQ = ZF + (QX - FX)                         # z da quina de trás da face diagonal
FAC_T = 2.0
FAC_L = (QX - FX) * 1.4142
FAC_O = ((FX + QX) / 2, (ZF + ZQ) / 2)      # centro da face de fora (lado +x)
FAC_C = (FAC_O[0] - 0.7071 * FAC_T / 2, FAC_O[1] + 0.7071 * FAC_T / 2)
OLHO_U, OLHO_RU, OLHO_RV = 0.25, 1.45, 0.82  # olho retangular arredondado (centro um pouco para trás)
SOB_K = 0.42                                # inclinação da sobrancelha (sobe para trás)
SOB_Y = 0.70                                # linha de baixo da sobrancelha no centro do olho
SOB_H = 1.05

def cor_rosto(c):
    return BRANCO_F

def olho(u, v):
    """Olho da ficha (neutra): retângulo de cantos redondos, cortado em cima pela sobrancelha; atrás a esclera
    branca, na frente a íris verde viva com pupila preta e brilho; fio verde-escuro em volta."""
    du = u - OLHO_U
    ru, rv = OLHO_RU, OLHO_RV
    if abs(du) > ru or abs(v) > rv: return None
    cq = max(0.0, abs(du) - (ru - 0.45)) / 0.45, max(0.0, abs(v) - (rv - 0.45)) / 0.45
    if cq[0] ** 2 + cq[1] ** 2 > 1: return None                 # cantos arredondados
    corte = SOB_Y - 0.08 + SOB_K * du
    if v > corte: return None
    if abs(du) > ru - 0.16 or v < -rv + 0.16: return (14, 52, 26)        # contorno
    iu = du + 0.38                                              # íris na metade da frente (para o bico)
    if abs(iu) < 0.78:
        if ((iu + 0.05) / 0.34) ** 2 + ((v + 0.1) / 0.42) ** 2 <= 1: return (12, 14, 14)
        if ((iu - 0.22) / 0.16) ** 2 + ((v - 0.22) / 0.16) ** 2 <= 1: return (250, 255, 250)
        return mix((70, 210, 70), (22, 130, 44), clamp((0.5 - v) / 1.3 + abs(iu) * 0.4))
    return mix((255, 255, 255), (214, 214, 222), clamp(-v / rv + 0.25))

def mat_faceta(lado):
    """Face diagonal do rosto: olho inteiro numa face plana; cicatrizes num lado só."""
    fora = "east" if lado > 0 else "west"
    def cor(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u, v = z - FAC_C[1], y - EY
            o = olho(u, v)
            if o is not None: return o
            if lado == LADO_CICATRIZ:
                if risco_x(u, v, 0.3, -2.1, 0.75, 0.2): return VERM
            else:
                for du in (-0.2, 0.6):                         # dois riscos curtos e tortos na outra bochecha
                    if abs((v + 2.0) - 0.9 * (u - du)) < 0.17 and abs(u - du) < 0.5: return VERM
        return BRANCO_F
    base = mat_luz(cor, matriz((0, 45 * lado, 0)), borda=.0)
    def f(c):
        cc = cor(c)
        if cc != BRANCO_F and c["face"] == fora: return cc            # olho e cicatriz sem sombra por cima
        return base(c)
    return f

def mat_bico(M=None):
    def cor(c):
        x, y, z = c["p"]
        face = c["face"]
        if face in ("east", "west") and abs(z - (ZF - 1.4)) < 0.28 and abs(y - 25.6) < 0.28: return (110, 60, 10)
        return AMAR if face != "down" else AMAR_ESC
    return mat_luz(cor, M, borda=.04, topo=.22, baixo=-.35)

def montar_cabeca():
    cab = []
    mb = mat_luz(cor_rosto, borda=.10)
    # crânio largo; a frente estreita fica entre as duas facetas do olho
    cab += g.arredondado2("cranio", [-QX, 22.4, ZQ - 0.3], [QX, 30.0, 2.2], mb, r=1.2)
    cab.append(peca("cranio_frente", [-FX, 22.8, ZF], [FX, 29.6, ZQ + 0.2], mat_luz(cor_frente, borda=.0), res=6))
    cab.append(peca("queixo", [-2.6, 21.6, ZF + 0.8], [2.6, 23.0, ZQ + 1.6], mb))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 22.8, cz - FAC_L / 2], [cx + FAC_T / 2, 30.0, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, EY, cz), res=8))
        # sobrancelha: barra preta GROSSA (bloco), por cima do olho, descendo para o bico
        xo = cx + FAC_T / 2 * lado
        x0, x1 = sorted((xo - 0.2 * lado, xo + 0.55 * lado))
        yb = EY + SOB_Y
        msob = mat_luz(cor_fixa(PRETO_SOB), matriz((0, 45 * lado, 0), (-math.degrees(math.atan(SOB_K)), 0, 0)), borda=.0,
                       topo=.25, baixo=-.2)
        cab.append(osso("sobrancelha_" + s, [cx, EY, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, yb, cz - FAC_L / 2 - 0.35], [x1, yb + SOB_H, cz + FAC_L / 2 + 0.9], msob,
                 rot=(-math.degrees(math.atan(SOB_K)), 0, 0), pivo=(cx, yb, cz + OLHO_U))]))
        # na frente a barra continua e desce até a base do bico (V bravo)
        yq = yb - SOB_K * (FAC_L / 2 + OLHO_U)          # altura da barra na quina da frente
        x0, x1 = sorted((0.9 * lado, (FX + 0.35) * lado))
        cab.append(peca("sobrancelha_f_" + s, [x0, yq, ZF - 0.55], [x1, yq + SOB_H, ZF + 0.3],
                        mat_luz(cor_fixa(PRETO_SOB), borda=.0, topo=.25), rot=(0, 0, 22 * lado), pivo=(FX * lado, yq, ZF)))
    # bico em cunha: base larga, meio, gancho; mandíbula de baixo mais escura
    mbi = mat_bico()
    cab.append(peca("bico_base", [-1.75, 24.15, ZF - 1.8], [1.75, 26.3, ZF + 0.4], mbi, res=4))
    cab.append(peca("bico_meio", [-1.6, 24.25, ZF - 2.9], [1.6, 26.1, ZF - 1.6], mbi, res=4))
    cab.append(peca("bico_gancho", [-1.4, 23.75, ZF - 3.5], [1.4, 25.8, ZF - 2.75], mbi, res=4))
    cab.append(peca("bico_baixo", [-1.4, 23.45, ZF - 2.6], [1.4, 24.3, ZF + 0.3],
                    mat_luz(cor_fixa((236, 150, 18)), borda=.12, topo=.1), res=4))
    # barbela: dois blocos vermelhos compridos pendurados sob a base do bico
    mbar = mat_luz(lambda c: mix(VERM_CL, VERM, clamp((23.4 - c["p"][1]) / 1.5)), borda=.14, topo=.15)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.08 * lado, 1.3 * lado))
        cab.append(peca("barbela_" + s, [x0, 20.3, ZF - 1.6], [x1, 23.6, ZF - 0.4], mbar, res=4))
    # juba e crista: espetos grossos em degrau; o do meio sobe reto, os outros abrem para trás e para os lados
    crista = []
    # (raiz, giro, comprimento, largura): a frente é baixa e irregular perto da testa; o alto e a nuca são altos;
    # as pontas vão para cima, para trás e na diagonal
    C = [((0.0, 29.2, -5.4), (-16, 0, 0), 5.0, 3.4), ((0.0, 29.6, -3.4), (-2, 0, 0), 9.6, 3.6),
         ((0.0, 29.6, -1.0), (22, 0, 0), 9.6, 3.8), ((0.0, 29.0, 1.2), (48, 0, 0), 9.0, 3.6),
         ((0.0, 27.4, 2.2), (76, 0, 0), 8.0, 3.4), ((0.0, 25.0, 2.2), (102, 0, 0), 7.0, 3.2),
         ((0.0, 22.6, 1.4), (126, 0, 0), 5.4, 3.0)]
    for l in (-1, 1):
        C += [((2.4 * l, 29.0, -4.8), (-6, 0, -14 * l), 5.2, 2.8), ((2.4 * l, 29.4, -2.4), (10, 0, -12 * l), 7.8, 3.0),
              ((2.6 * l, 29.0, 0.2), (36, 0, -12 * l), 8.0, 3.0), ((2.9 * l, 27.6, 1.6), (64, 0, -14 * l), 7.4, 3.0),
              ((3.8 * l, 28.0, -2.8), (14, 0, -44 * l), 5.0, 2.8), ((4.0 * l, 26.6, -0.6), (56, 0, -36 * l), 5.6, 2.8),
              ((3.8 * l, 24.4, 1.2), (98, 0, -26 * l), 5.4, 2.8)]
    for k, (r, rt, L, w) in enumerate(C):
        crista.append(espeto(f"crista{k}", r, rt, L, w))
    cab.append(osso("crista", [0, 30.0, 0], [0, 0, 0], crista))
    # tufos da bochecha (atrás do olho, para trás) e do pescoço
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cab.append(espeto("bochecha_" + s, (4.0 * lado, 25.4, -2.6), (90, 0, -10 * lado), 4.4, 2.6))
        cab.append(espeto("bochecha2_" + s, (3.8 * lado, 23.0, -3.0), (110, 0, -12 * lado), 4.2, 2.4))
    return osso("cabeca", [0, 24.0, -1.5], [0, 0, 0], cab)

def cor_frente(c):
    """Frente da testa: cicatriz em asterisco do lado das cicatrizes, acima da sobrancelha."""
    x, y, z = c["p"]
    if c["face"] == "north" and asterisco(x, y, 0.85 * LADO_CICATRIZ, 28.9, 0.72, 0.17): return VERM
    return BRANCO_F

# ---------------- corpo ----------------
def cor_tronco(c):
    x, y, z = c["p"]
    if c["face"] == "north" and z < -5.0:
        if risco_x(x, y, 0.0, 17.4, 2.2, 0.32): return VERM
    return BRANCO_F

def cor_hakama(c):
    x, y, z = c["p"]
    face = c["face"]
    a = z if face in ("east", "west") else x
    if y < 6.9 and face != "down": return PRETO_H                    # barra
    pre = (a + 0.3) % 1.8                                                 # pregas largas
    if pre < 0.25: return PRETO_H
    return CARVAO if pre < 1.0 else (56, 58, 62)

# glifo do vento: espiral quadrada de traço grosso com a haste descendo pela frente e virando para trás
def _curva_glifo():
    pts = []
    te = 2.35 * math.pi
    for k in range(48):
        th = te * k / 47
        r = 0.35 + 0.30 * th
        ph = te - th                                   # sentido horário: termina na frente descendo
        pts.append((r * math.cos(ph), r * math.sin(ph)))
    ue, ve = pts[-1]
    return pts + [(ue, ve - 3.0), (ue - 0.6, ve - 3.6), (ue - 2.4, ve - 3.6), (ue - 2.8, ve - 3.0)]
GLIFO_P = _curva_glifo()
GLIFO_C = (16.2, -0.4)                    # (y, z) do centro da espiral
GLIFO_W = 0.62                           # meia espessura do traço

def _dist_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = clamp(((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy + 1e-9))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

def glifo(y, z):
    """a = para a frente (-z), v = para cima: a haste desce pela frente e vira para trás nas duas asas."""
    a, v = -(z - GLIFO_C[1]), (y - GLIFO_C[0])
    if not (-4.0 < a < 3.6 and -6.0 < v < 3.6): return False
    return any(_dist_seg(a, v, *GLIFO_P[i], *GLIFO_P[i + 1]) < GLIFO_W for i in range(len(GLIFO_P) - 1))

def mat_asa(lado, M, glifo_ok=True, cor=BRANCO_F):
    fora = "east" if lado > 0 else "west"
    def c_(c):
        x, y, z = c["p"]
        if glifo_ok and c["face"] == fora and glifo(y, z): return VERDE
        return cor
    m = mat_luz(c_, M, borda=.14, grad=.12)
    def f(c):
        if glifo_ok and c["face"] == fora and glifo(c["p"][1], c["p"][2]):
            return VERDE if not na_borda(c) else VERDE_ESC
        return m(c)
    return f

def montar_asa(lado):
    """Asa como manga larga de quimono: painel grosso de penas brancas (4 fileiras em degrau, cada uma mais larga
    e mais comprida para trás), que pende do ombro até perto do fim da hakama, com a frente junto do peito e a
    borda de trás aberta para fora; espiral do vento na face de fora; uma camada de penas de cobertura com pontas
    sobre a fileira de baixo; borda de baixo em pontas grandes (brancas por fora, verdes na camada de dentro)."""
    s = "d" if lado < 0 else "e"
    xi = 3.7 * lado
    T = 1.8
    PIV = (xi, 21.4, -6.0)
    ROT = (0, 25 * lado, 3 * lado)
    M = matriz(ROT)
    ma = mat_asa(lado, M)
    mp = mat_asa(lado, M, glifo_ok=False)
    mv = mat_asa(lado, M, glifo_ok=False, cor=VERDE)
    filhos = []
    def caixa(nome, y0, y1, z0, z1, extra, mat, dentro=0.0, **kw):
        xa, xb = sorted((xi + dentro * lado, xi + (T + extra) * lado))
        return peca(nome, [xa, y0, z0], [xb, y1, z1], mat, **kw)
    def ponta(nome, yb, ytopo, zc, w, extra, mat, dentro=0.0):
        """Pena com ponta: bloco até yb e um losango (quadrado girado 45°) embaixo, que faz a ponta."""
        q = w / 1.4142
        return [caixa(nome, yb, ytopo, zc - w / 2, zc + w / 2, extra, mat, dentro),
                caixa(nome + "_pt", yb - q / 2, yb + q / 2, zc - q / 2, zc + q / 2, extra - 0.06, mat, dentro + 0.03,
                      rot=(45, 0, 0), pivo=(xi, yb, zc))]
    # 4 fileiras em degrau (borda de trás em escada, do ombro até a cauda); a de cima fica por fora (camadas)
    filhos.append(caixa("asa_a_" + s, 18.2, 22.0, -6.0, -1.0, 0.6, ma))
    filhos.append(caixa("asa_b_" + s, 14.6, 18.6, -6.0, 2.6, 0.4, ma))
    filhos.append(caixa("asa_c_" + s, 11.2, 15.0, -6.0, 5.6, 0.2, ma))
    filhos.append(caixa("asa_d_" + s, 9.0, 11.6, -6.0, 8.0, 0.0, ma))
    # penas de cobertura: pontas que descem da fileira do meio por cima da de baixo
    for k, z in enumerate((-4.6, -1.8, 1.0, 3.8)):
        filhos += ponta(f"asa_cob{k}_{s}", 12.0 - 0.3 * k, 14.8, z, 2.6, 0.55, ma)
    # pontas grandes da borda de baixo (a borda desce da frente para trás)
    for k, z in enumerate((-4.7, -1.7, 1.3, 4.3, 7.0)):
        filhos += ponta(f"asa_p{k}_{s}", 8.2 - 0.35 * k, 9.4, z, 2.8, -0.2, mp, 0.1)
    # camada de dentro: pontas verdes que aparecem entre as brancas
    for k, z in enumerate((-3.2, -0.2, 2.8, 5.7)):
        filhos += ponta(f"asa_v{k}_{s}", 7.6 - 0.35 * k, 9.2, z, 1.8, -0.9, mv, 0.45)
    # pontas na borda de trás (em cada degrau da escada)
    for k, (y0, z0) in enumerate(((18.2, -1.4), (14.6, 2.2), (11.2, 5.2))):
        filhos += ponta(f"asa_t{k}_{s}", y0 - 0.8, y0 + 0.8, z0, 2.2, 0.15 - 0.2 * k, mp, 0.15)
    return osso("asa_" + s, list(PIV), list(ROT), filhos)

def montar_lapela(lado):
    """Lapela da manga na frente: faixa branca do pescoço à faixa, abrindo em V no peito (mostra o X)."""
    s = "d" if lado < 0 else "e"
    x0, x1 = sorted((2.3 * lado, 4.3 * lado))
    return peca("lapela_" + s, [x0, 13.8, -6.6], [x1, 21.6, -5.4], mat_luz(cor_fixa(BRANCO_F), borda=.2),
                rot=(0, 0, -10 * lado), pivo=(2.3 * lado, 13.8, -6.0))

# ---------------- cauda ----------------
def mat_pena_cauda(k, n, M, L_tot, z_ini):
    """Pena da cauda (bloco): branca por cima e na ponta, faixa verde-escura larga na metade de baixo, que toma a
    pena toda perto da raiz."""
    def cor(c):
        (_, y0, z0), (_, y1, z1) = c["b"]
        x, y, z = c["p"]
        fy = (y - y0) / max(y1 - y0, 1e-6)
        t = clamp((z - z_ini) / L_tot)
        face = c["face"]
        if face == "up": return BRANCO_F
        if t > 0.86: return BRANCO_F
        lim = 0.5 + 0.5 * clamp((0.32 - t) / 0.2)
        if face == "down" or fy < lim: return VERDE if fy > 0.18 or face == "down" else VERDE_ESC
        return BRANCO_F
    return mat_luz(cor, M, borda=.14)

def pena_cauda(nome, raiz, rot0, curva, L, H, esp):
    """Pena larga: cadeia de 5 segmentos para trás (+z) que afinam em degrau até a ponta."""
    fr = [0.26, 0.24, 0.21, 0.17, 0.12]
    alt = [1.0, 1.0, 0.9, 0.7, 0.42]
    n = len(fr)
    def seg(k, pos, M, z_ini):
        px, py, pz = pos
        h = H * alt[k]; Ls = L * fr[k]
        r = list(rot0) if k == 0 else list(curva)
        Mk = previa.mm(M, previa.rot(*r))
        filhos = [peca(f"{nome}_{k}", [px - esp / 2, py - h / 2, pz - 0.1], [px + esp / 2, py + h / 2, pz + Ls + 0.1],
                       mat_pena_cauda(k, n, Mk, L, z_ini - sum(L * f for f in fr[:k])), res=3)]
        if k + 1 < n: filhos.append(seg(k + 1, (px, py, pz + Ls), Mk, pz + Ls))
        return osso(f"{nome}_{k}", list(pos), r, filhos)
    return seg(0, raiz, matriz(), raiz[2])

def montar_cauda():
    """Leque grande de 6 penas largas saindo do quadril para trás, abertas do alto (até a altura da nuca) até
    embaixo (perto das canelas), em camadas; espessuras alternadas (sem faces no mesmo plano)."""
    penas = []
    # (raiz y, z, elevação, ry, curva, comprimento, altura, espessura)
    P = [(17.4, 3.6, 46, -5, 2, 16.5, 5.6, 2.4), (16.6, 3.8, 31, 5, 0, 18.0, 6.0, 2.0),
         (15.6, 4.0, 19, -5, -2, 19.0, 6.0, 2.4), (14.6, 4.0, 3, 5, -3, 18.0, 5.8, 2.0),
         (13.8, 3.8, -12, -4, -4, 16.0, 5.4, 2.4), (13.0, 3.6, -27, 4, -4, 13.0, 4.8, 2.0)]
    for k, (y, z, e, ry, cv, L, H, esp) in enumerate(P):
        penas.append(pena_cauda(f"cauda{k}", (0, y, z), (-e, ry, 0), (cv, 0, 0), L, H, esp))
    return osso("cauda", [0, 15.5, 4.0], [0, 0, 0], penas)

# ---------------- katana ----------------
def mat_metal(cima, frente, lado, baixo):
    return g.mat_facetado(cima, frente, lado, baixo, quina=-0.3)

def mat_cabo(c):
    """Cabo da katana: verde-escuro com a amarração em quadrados brancos."""
    x, y, z = c["p"]
    t = (z - c["b"][0][2]) % 1.2
    if c["face"] in ("east", "west", "up", "down") and 0.35 < t < 0.85: return (238, 236, 228)
    return g.tom(VERDE_ESC, -0.25) if na_borda(c) else VERDE

def montar_katana(base):
    """Katana ao longo de z (frente = -z) a partir da guarda (tsuba), em 'base': cabo para a frente, bainha atrás."""
    bx, by, bz = base
    def pc_(nome, de, ate, mat, **kw):
        return g.peca(nome, [de[0] + bx, de[1] + by, de[2] + bz], [ate[0] + bx, ate[1] + by, ate[2] + bz], mat, **kw)
    ouro = mat_metal(OURO_CL, OURO, mix(OURO, OURO_ESC, .4), OURO_ESC)
    bainha = mat_metal((70, 72, 78), (36, 38, 42), (28, 30, 34), (16, 16, 20))
    pc = [pc_("katana_cabo", [-0.5, -0.5, -5.0], [0.5, 0.5, -0.3], mat_cabo, res=4),
          pc_("katana_pomo", [-0.6, -0.6, -5.6], [0.6, 0.6, -4.95], ouro, res=4)]
    pc += g.octogono("katana_tsuba", [bx - 1.2, by - 1.2, bz - 0.35], [bx + 1.2, by + 1.2, bz + 0.2], ouro, r=0.45)
    pc += [pc_("katana_habaki", [-0.55, -0.6, 0.1], [0.55, 0.6, 0.8], ouro, res=4),
           pc_("katana_bainha", [-0.45, -0.6, 0.7], [0.45, 0.6, 7.5], bainha),
           pc_("katana_kurikata", [-0.55, -0.7, 2.0], [0.55, 0.7, 2.6], mat_metal(OURO_CL, OURO, OURO, OURO_ESC), res=4)]
    return pc

# ---------------- montagem ----------------
def montar():
    corpo = []
    mt = mat_luz(cor_tronco, borda=.08, grad=.1)
    corpo += g.arredondado2("tronco", [-4.2, 12.8, -5.6], [4.2, 21.8, 3.8], mt, r=1.2, res=3)
    # hakama (cintura) e faixa branca
    mh = mat_luz(cor_hakama, borda=.1, topo=.15, baixo=-.4)
    corpo += g.arredondado("hakama_cint", [-5.0, 10.4, -5.9], [5.0, 13.0, 4.6], mh, r=0.4)
    mf = mat_luz(cor_fixa(BRANCO_F), borda=.14)
    corpo += g.arredondado("faixa", [-5.05, 12.6, -6.25], [5.05, 14.4, 4.75], mf, r=0.35)
    corpo.append(peca("no_faixa", [-0.8, 12.3, -6.9], [0.8, 14.7, -6.1], mat_luz(cor_fixa(CINZA_F), borda=.2)))
    corpo.append(peca("no_ponta1", [-0.75, 9.6, -6.75], [-0.05, 12.4, -6.25], mf, rot=(0, 0, -8), pivo=(-0.4, 12.4, -6.5)))
    corpo.append(peca("no_ponta2", [0.15, 10.0, -6.75], [0.85, 12.4, -6.25], mf, rot=(0, 0, 8), pivo=(0.5, 12.4, -6.5)))
    # katana presa na faixa: cabo para a frente, para cima e para fora; bainha para trás e para baixo
    KAT = (4.9 * LADO_KATANA, 13.8, -5.0)
    corpo.append(osso("katana", list(KAT), [34, 38 * (-LADO_KATANA), 0], montar_katana(KAT)))
    pescoco = osso("pescoco", [0, 21.5, -2.0], [0, 0, 0], [
        *g.arredondado("pescoco", [-3.0, 19.6, -6.4], [3.0, 24.0, 0.8], mat_luz(cor_fixa(BRANCO_F), borda=.08), r=0.8),
        montar_cabeca()])
    corpo.append(pescoco)
    for lado in (-1, 1):
        corpo.append(montar_asa(lado))
    corpo.append(montar_cauda())
    tronco = osso("corpo", [0, 12.0, 0], [0, 0, 0], corpo)
    raizes = [tronco, perna(-1), perna(1)]
    g.transformar(0, raizes, (0.0, 0.0, 0.0), k=ESCALA)
    return raizes

def perna(lado):
    s = "d" if lado < 0 else "e"; xc = 3.2 * lado; zc = 0.0
    pp = []
    mh = mat_luz(cor_hakama, borda=.1, topo=.15, baixo=-.4)
    x0, x1 = sorted((0.05 * lado, 5.2 * lado))
    pp += g.arredondado("hakama_" + s, [x0, 6.4, -5.6], [x1, 11.0, 4.4], mh, r=0.4)
    ma = mat_luz(lambda c: AMAR if c["face"] != "down" else AMAR_ESC, borda=.12, topo=.2, baixo=-.3)
    pp += g.arredondado("canela_" + s, [xc - 1.35, 1.2, zc - 1.6], [xc + 1.35, 6.8, zc + 1.6], ma, r=0.35)
    # pé: 3 dedos para a frente com garra escura na ponta, 1 dedo atrás
    mg = mat_luz(cor_fixa(GARRA), borda=.1, topo=.25)
    for nome, dx, ang in (("meio", 0.0, 0), ("fora", 1.5 * lado, 24 * lado), ("dentro", -1.5 * lado, -20 * lado)):
        x0 = xc + dx
        comp = 3.6 if nome == "meio" else 3.0
        pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, zc - 0.6], [0, -ang, 0], [
            peca(f"dedo_{nome}_{s}", [x0 - .7, 0, zc - 0.6 - comp], [x0 + .7, 1.6, zc + 0.8], ma),
            peca(f"garra_{nome}_{s}", [x0 - .6, 0.0, zc - 0.6 - comp - 1.1], [x0 + .6, 1.2, zc - 0.5 - comp], mg)]))
    pp.append(peca("dedo_tras_" + s, [xc - .7, 0, zc + 0.8], [xc + .7, 1.3, zc + 3.4], ma))
    pp.append(peca("garra_tras_" + s, [xc - .6, 0, zc + 3.3], [xc + .6, 1.0, zc + 4.2], mg))
    return osso("perna_" + s, [xc, 12.0, zc], [0, 0, 0], pp)

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

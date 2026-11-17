"""Pirococó (#001, Fogo): o galo-fênix das chamas, mítico. Galo de briga imponente de ARMADURA roxa (elmo-máscara
com chifres dourados e gema vermelha, ombreiras facetadas, peitoral com o emblema da fênix e botas), capa de asas
de penas de fogo em leque (vermelho -> laranja -> amarelo, com toques roxos) e cauda de fênix com três correntes de
contas douradas que terminam em pingentes de losango dourado com gema vermelha."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, clamp, tom, na_borda

ID = "pirococo"; NOME = "Pirococó"; NUMERO = 1
ALTURA = 2.8
QUADRUPEDE = False
ROSTO = ((0, 31.0, -5.5), 7.5)
# os pingentes das 3 correntes balançam (além da onda das correntes, em ONDAS lá embaixo)
ANIM_PARADO = {f"corrente_{c}_pingente": [(0, 0, 0), (4, 0, 7 * s), (0, 0, 0), (-4, 0, -7 * s), (0, 0, 0)]
               for c, s in (("c", 1), ("d", -1), ("e", 1))}
ANIM_ANDANDO = {f"corrente_{c}_pingente": [(0, 0, 0), (8, 0, 10 * s), (0, 0, 0), (-8, 0, -10 * s), (0, 0, 0)]
                for c, s in (("c", 1), ("d", -1), ("e", 1))}

# ---------------- paleta (amostrada com PIL na ficha e na arte; veja modelos/pirococo/detalhes.md) ----------------
ROXO_ESC = (64, 28, 109); ROXO = (137, 83, 183); ROXO_VIVO = (159, 89, 183); LILAS = (184, 142, 217)
LILAS_CLARO = (214, 184, 232)
CREME = (252, 228, 200); CREME_SOMBRA = (232, 202, 182)
AMARELO = (252, 178, 12); AMARELO_CLARO = (254, 206, 76)
OURO = (251, 173, 9); OURO_CLARO = (255, 222, 116); OURO_ESC = (196, 112, 8)
LARANJA = (245, 119, 7); LARANJA_VERM = (245, 64, 13); VERMELHO = (230, 17, 20); VERM_ESC = (161, 3, 6)
VERM_FUNDO = (120, 6, 10)
GEMA = (239, 21, 28); GEMA_CLARA = (255, 120, 108); GEMA_ESC = (150, 4, 12)
BICO = (252, 168, 6); BICO_CLARO = (255, 206, 76); BICO_ESC = (226, 120, 4)
PRETO = (20, 10, 14)

def claro(c, f):
    """Clareia multiplicando (mantém a saturação da ficha, sem lavar para o branco)."""
    return tuple(min(255, int(round(v * (1 + f)))) for v in c)

def grad(paradas, t):
    """Degradê por paradas [(t, cor), ...] (t de 0 a 1)."""
    t = clamp(t)
    for (t0, c0), (t1, c1) in zip(paradas, paradas[1:]):
        if t <= t1: return mix(c0, c1, (t - t0) / max(t1 - t0, 1e-6))
    return paradas[-1][1]

FOGO_ROXO = [(0, ROXO), (0.3, (200, 40, 110)), (0.55, VERMELHO), (1, LARANJA)]
FOGO_VERM = [(0, VERM_ESC), (0.35, VERMELHO), (0.7, LARANJA), (1, AMARELO)]
FOGO_LAR = [(0, VERMELHO), (0.4, LARANJA_VERM), (0.7, LARANJA), (1, AMARELO)]
FOGO_JUBA = [(0, VERM_ESC), (0.45, VERMELHO), (0.8, LARANJA_VERM), (1, LARANJA)]
FOGO_CAPA = [(0, VERM_ESC), (0.3, VERMELHO), (0.6, LARANJA_VERM), (0.84, LARANJA), (1, AMARELO)]
FOGO_AMAR = [(0, LARANJA_VERM), (0.35, LARANJA), (0.75, AMARELO), (1, AMARELO_CLARO)]

def girar_z(p, piv, ang):
    """Gira o ponto p em volta do eixo z que passa por piv (graus, como o Blockbench)."""
    a = math.radians(ang); x, y = p[0] - piv[0], p[1] - piv[1]
    return (piv[0] + x * math.cos(a) - y * math.sin(a), piv[1] + x * math.sin(a) + y * math.cos(a), p[2])

# ---------------- materiais ----------------
def mat_pena_fogo(paradas, y0, L, zc, W, claro_lado=-1):
    """Pena de fogo em bloco (quadro "Capa de Asas"): degradê da raiz à ponta, metade clara e metade base na face
    larga (pena dobrada) com raque clara, contorno escuro só nas beiradas compridas; espessura em sombra."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        t = clamp((y0 - y) / max(L, 1e-6))
        base = grad(paradas, t)
        if face in ("east", "west"):
            u = (z - zc) / (W / 2)
            cor = claro(base, 0.10) if u * claro_lado > 0 else tom(base, -0.06)
            if abs(u) < 0.08 and t < 0.85: cor = claro(cor, 0.10)
            if t < 0.12: cor = tom(cor, -0.15)
            if c["nome"].endswith("_pt"):
                if na_borda(c): cor = tom(cor, -0.3)
            elif c["i"] in (0, c["tw"] - 1): cor = tom(cor, -0.3)
            return cor
        if face == "up": return claro(base, 0.08)
        if face == "down": return tom(base, -0.45)
        return tom(base, -0.2)
    return f

def mat_placa_roxa(y0, L, zc, W):
    """Placa de armadura roxa facetada (ombreira): face larga em duas facetas (frente lilás, trás roxo) com aresta
    clara no meio, raiz mais clara, ponta mais escura; espessura roxo escuro; quinas escuras."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        t = clamp((y0 - y) / max(L, 1e-6))
        if face in ("east", "west"):
            u = (z - zc) / (W / 2)
            cor = mix(LILAS, ROXO_VIVO, 0.35) if u < -0.05 else ROXO
            if abs(u + 0.05) < 0.07: cor = LILAS_CLARO
            cor = tom(cor, 0.12 - 0.35 * t)
            if na_borda(c): cor = tom(cor, -0.3)
            return cor
        if face == "up": return LILAS
        if face == "down": return ROXO_ESC
        return tom(ROXO, -0.25) if not na_borda(c) else ROXO_ESC
    return f

def mat_ouro(c):
    """Ouro facetado (chifres, diadema, contas): topo claro, frente amarela, lados ouro, embaixo âmbar escuro."""
    face = c["face"]
    base = {"up": OURO_CLARO, "down": OURO_ESC, "north": AMARELO_CLARO, "south": mix(OURO, OURO_ESC, 0.3)}.get(face, OURO)
    return tom(base, -0.25) if na_borda(c) else base

def mat_roxo(c, frente_clara=True):
    face = c["face"]
    base = {"up": LILAS, "down": ROXO_ESC, "north": mix(ROXO, LILAS, 0.3) if frente_clara else ROXO}.get(face, ROXO)
    return tom(base, -0.28) if na_borda(c) else base

def mat_viseira(c):
    """Sobrancelha/viseira roxa: face de baixo bem escura (a sombra que cai sobre o olho), topo lilás."""
    if c["face"] == "down": return tom(ROXO_ESC, -0.35)
    return mat_roxo(c)

def mat_cor(cor_fn, **kw):
    def f(c):
        base = cor_fn(c["p"], c["face"])
        return None if base is None else tom(base, g.contexto_luz(c, **kw))
    return f

# ---------------- formas ----------------
def pena(nome, raiz, phi, lado, L, W, paradas, flare=20, varre=0, T=0.9, armadura=False, brilho=False):
    """Pena (ou placa de armadura) grossa pendurada da raiz: corpo + ponta em losango. phi = ângulo em volta do corpo
    (0 = para fora, -90 = frente, +90 = trás); flare abre a ponta para fora; varre puxa a ponta para trás."""
    x, y, z = raiz
    Lb = L - W * 0.5
    s = W / 1.4142
    m = mat_placa_roxa(y, L, z, W) if armadura else mat_pena_fogo(paradas, y, L, z, W)
    corpo = peca(nome, [x - T / 2, y - Lb, z - W / 2], [x + T / 2, y, z + W / 2], m, res=2, brilho=brilho)
    ponta = peca(nome + "_pt", [x - T / 2 + 0.03, y - Lb - s / 2, z - s / 2], [x + T / 2 - 0.03, y - Lb + s / 2, z + s / 2], m,
                 rot=(45, 0, 0), pivo=(x, y - Lb, z), res=2, brilho=brilho)
    return osso(nome, list(raiz), [0, -phi * lado, 0], [osso(nome + "_p", list(raiz), [-varre, 0, flare * lado], [corpo, ponta])])

def anel(ax, az, zc, phi, lado):
    r = math.radians(phi)
    return lado * ax * math.cos(r), zc + az * math.sin(r)

# ---------------- cabeça ----------------
CAB_Y0, CAB_Y1 = 26.4, 35.0
ZF = -6.4                        # frente da cara (onde nasce o bico)
FRENTE_X = 2.0                   # meia largura da frente estreita
FAC_ANG = 48                     # giro da faceta do olho em y
FAC_L, FAC_T = 4.0, 1.6
_tx, _tz = math.sin(math.radians(FAC_ANG)), math.cos(math.radians(FAC_ANG))
_nx, _nz = math.cos(math.radians(FAC_ANG)), -math.sin(math.radians(FAC_ANG))
LX = FRENTE_X + FAC_L * _tx      # meia largura do crânio
ZL = ZF + FAC_L * _tz            # onde a faceta encontra o lado da cabeça
FAC_S = (FRENTE_X + _tx * FAC_L / 2, ZF + _tz * FAC_L / 2)
FAC_C = (FAC_S[0] - _nx * FAC_T / 2, FAC_S[1] - _nz * FAC_T / 2)
OLHO_Y = 30.85

OLHO_RU, OLHO_RV = 1.85, 1.45                  # meia largura (ao longo da face) e meia altura do olho
OLHO_CORTE0, OLHO_CORTE_INC = 0.45, 0.26      # linha da pálpebra: v = c0 + inc * u (desce para o bico)

def olho(u, v):
    """Olho imponente (Fase 7): fenda de ave de rapina, alongada para trás (~1,8 : 1), canto da frente pontudo. A
    pálpebra/viseira corta o topo numa diagonal que desce para o bico (só ~60% do olho aparece), com 1 px escuro e a
    sombra da sobrancelha logo abaixo. Íris vermelha forte ocupando quase tudo, pupila junto da borda do lado do bico
    (olhando para a frente) com 1 brilho; esclera só numa cunha atrás. Borda de baixo quase reta, subindo para trás.
    u: ao longo da face (negativo = para o bico); v: para cima. Devolve None fora do olho."""
    ru, rv = OLHO_RU, OLHO_RV
    uu = u / ru
    if abs(uu) > 1: return None
    corte = OLHO_CORTE0 + OLHO_CORTE_INC * u
    baixo = -rv * (0.78 - 0.18 * uu) * (1 - max(0.0, -uu) ** 2.2)      # borda de baixo: reta, fecha em ponta na frente
    cima = rv * (0.95 - 0.1 * uu) * (1 - max(0.0, -uu) ** 1.6)
    topo = min(cima, corte)
    if v > corte and v <= corte + 0.22 and v <= cima + 0.3 and abs(uu) <= 1: return mix(PRETO, ROXO_ESC, 0.25)  # sombra
    if v < baixo or v > topo: return None
    if topo - v < 0.14: return PRETO                                           # fio da pálpebra
    if baixo > -rv * 0.05 and v - baixo < 0.1: return (90, 30, 30)
    # íris: grande, puxada para o bico
    ic, ir = -0.08, 0.8
    du = (uu - ic) / ir; dv = v / (rv * 0.98)
    if du * du + dv * dv <= 1 or (uu < ic and v >= baixo):
        if ((uu + 0.5) / 0.17) ** 2 + ((v + 0.1) / 0.6) ** 2 <= 1:             # pupila (oval vertical) junto da frente
            return PRETO
        if ((uu + 0.3) / 0.09) ** 2 + ((v - topo + 0.32) / 0.16) ** 2 <= 1: return (255, 250, 240)   # brilho
        cor = mix((252, 66, 38), (196, 16, 22), clamp((v - baixo) / max(topo - baixo, 0.1)))  # mais escura em cima
        if topo - v < 0.26: cor = tom(cor, -0.3)                               # sombra da sobrancelha no alto da íris
        if du * du + dv * dv > 0.8 and uu > ic: cor = (110, 6, 14)              # anel escuro só atrás
        return cor
    # esclera: só uma cunha atrás da íris, sombreada
    return mix((232, 210, 196), (180, 150, 150), clamp((topo - v) / 0.8))

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return ROXO
    if z < ZL + 0.3:
        return CREME if y < 33.2 else ROXO
    return mix(VERM_ESC, VERMELHO, clamp((y - 27) / 6))

def mat_faceta(lado):
    base = mat_cor(cor_cabeca, borda=.0, curva=.2)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            cor = olho(z - FAC_C[1] - 0.2, y - OLHO_Y)
            if cor is not None: return cor
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return BICO_ESC
    if face == "up": return BICO_CLARO
    if face in ("east", "west") and abs(z - (ZF - 1.9)) < 0.28 and abs(y - 30.0) < 0.22: return (120, 50, 10)   # narina
    if face in ("east", "west", "north") and 28.05 < y < 28.3 and z > ZF - 3.2: return (130, 50, 10)            # boca
    if face == "north":
        # de frente: cunha em V (meio claro, laterais em sombra que estreitam para baixo)
        larg = 0.35 + 0.9 * clamp((y - 27.0) / 3.6)
        cor = mix(BICO_CLARO, BICO, clamp((30.6 - y) / 2.0))
        return cor if abs(x) < larg else tom(BICO, -0.18)
    return mix(BICO_CLARO, BICO, clamp((30.8 - y) / 1.2))

def mat_gema_testa(cx, cy, W, H):
    """Gema da testa: hexágono alongado (pontas em cima e embaixo) com moldura de ouro e gema vermelha facetada.
    As 3 peças (miolo e as 2 pontas giradas 45°) pintam pelo ponto girado de volta para o mundo."""
    def f(c):
        x, y, z = c["p"]
        if c["nome"].endswith(("_cima", "_baixo")):
            piv = (cx, cy + (H - W) / 2 if c["nome"].endswith("_cima") else cy - (H - W) / 2)
            x, y, _ = girar_z((x, y, z), piv, 45)
        if c["face"] not in ("north",):
            return mat_ouro(c)
        u = (x - cx) / (W / 2); v = (y - cy) / (H / 2)
        lim = 1.0 if abs(v) < (H - W) / H else max(0.0, (1 - abs(v)) * H / W)
        borda = lim - abs(u)
        if borda < 0.12 or abs(v) > 0.93: return OURO_ESC if borda < 0.05 or abs(v) > 0.97 else OURO_CLARO
        if borda < 0.36: return mix(AMARELO_CLARO, OURO, clamp(0.5 - v))
        if u < 0 and v > 0: return GEMA_CLARA
        if u > 0 and v < 0: return GEMA_ESC
        return GEMA
    return f

def so_gema(c, cor): return cor[0] > 140 and cor[1] < 130 and cor[2] < 120

def cabeca_ossos():
    cab = []
    mc = mat_cor(cor_cabeca, borda=.0, curva=.25)
    fx = (CAB_Y0, CAB_Y1)
    # crânio: bloco atrás + frente estreita; as facetas diagonais (com o olho) fecham a quina
    cab += g.arredondado("cranio", [-LX, CAB_Y0, ZL - 0.4], [LX, CAB_Y1, 1.4], mc, r=0.6, faixa=fx, res=3)
    cab.append(peca("cranio_frente", [-FRENTE_X - 0.5, CAB_Y0, ZF], [FRENTE_X + 0.5, CAB_Y1 - 0.2, ZL], mc, faixa=fx, res=3))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, CAB_Y0 + 0.1, cz - FAC_L / 2], [cx + FAC_T / 2, CAB_Y1 - 0.25, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, FAC_ANG * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=fx, res=8))
        # viseira do elmo: barra roxa grossa por cima do olho, descendo para o bico (cara brava)
        # (inclinação igual à linha da pálpebra do olho; a borda de baixo encosta no corte e a aba sai 1,2 da face,
        #  fazendo sombra sobre o olho)
        ox0, ox1 = sorted((cx + FAC_T / 2 * lado - 0.6 * lado, cx + FAC_T / 2 * lado + 0.85 * lado))
        ang = math.degrees(math.atan(OLHO_CORTE_INC))
        zc0 = cz + 0.2                                    # onde u = 0 no olho
        yb = OLHO_Y + OLHO_CORTE0 + 0.3                   # borda de baixo da viseira em u = 0 (sobre a sombra pintada)
        cab.append(osso("viseira_" + s, [cx, yb, zc0], [0, FAC_ANG * lado, 0], [
            peca("viseira_" + s, [ox0, yb, cz - FAC_L / 2 - 0.9], [ox1, yb + 1.8, cz + FAC_L / 2 + 0.5],
                 mat_viseira, rot=(-ang, 0, 0), pivo=(cx, yb, zc0), res=4)]))
        # barra de trás do elmo (atrás do olho, desce até a bochecha)
        bx0, bx1 = sorted(((LX - 0.4) * lado, (LX + 0.65) * lado))
        cab.append(peca("elmo_barra_" + s, [bx0, 27.4, ZL + 0.1], [bx1, 34.0, ZL + 1.9], mat_roxo, res=3))
        # placa lateral do elmo: cobre o lado da cabeça atrás da barra (a juba sai por trás dela)
        lx0, lx1 = sorted(((LX - 0.3) * lado, (LX + 0.35) * lado))
        cab.append(peca("elmo_lado_" + s, [lx0, 27.6, ZL + 1.7], [lx1, 34.2, 0.6], mat_cor(lambda p, f_: ROXO if f_ != "up" else LILAS,
                        borda=.12, curva=.3), faixa=(27.6, 34.2), res=3))
    # casca do elmo (alto da cabeça): uma peça grande arredondada
    cab.append(peca("elmo_topo", [-LX - 0.35, 33.4, ZF - 0.7], [LX + 0.35, 36.0, 1.9], mat_roxo, res=3))
    cab.append(peca("elmo_cupula", [-LX + 0.9, 35.5, ZF + 0.5], [LX - 0.9, 37.0, 1.1], mat_roxo, res=3))
    # bico em cunha (de frente: topo largo que afina em V para baixo; de lado: comprido, cai num gancho). Cada trecho é
    # uma tampa reta em cima + um cubo girado 45° em z (quilha em V embaixo, com aresta no topo = cúmen do bico)
    mb = mat_cor(cor_bico, borda=.06, curva=.3)
    def mq(c):
        """Quilha (cubo girado 45°): as 2 faces de cima claras, as 2 de baixo no tom do bico; fio só na quina."""
        f_ = c["face"]
        cor = mix(BICO_CLARO, BICO, 0.35) if f_ in ("up", "east") else (BICO if f_ in ("north", "south") else claro(BICO, 0.04))
        return tom(cor, -0.18) if na_borda(c) else cor
    fb = (27.0, 31.6)
    # trecho de trás: tampa larga + quilha em V (losango de meia diagonal 2,0); a aresta de cima da quilha é o cúmen
    cab.append(peca("bico_tampa", [-2.0, 29.6, ZF - 2.6], [2.0, 31.0, ZF + 0.4], mb, faixa=fb, res=4))
    q = 1.85 * 1.4142
    cab.append(peca("bico_quilha", [-q / 2, 29.15 - q / 2, ZF - 2.5], [q / 2, 29.15 + q / 2, ZF + 0.3], mq, rot=(0, 0, 45),
                    pivo=(0, 29.15, ZF), faixa=fb, res=4))
    # trecho da frente: menor e caído (mesmo pivô para a tampa e a quilha), afinando para o gancho
    piv = (0, 30.0, ZF - 2.4)
    cab.append(peca("bico_tampa2", [-1.35, 29.2, ZF - 3.9], [1.35, 30.7, ZF - 2.3], mb, rot=(-12, 0, 0), pivo=piv, faixa=fb, res=4))
    q = 1.25 * 1.4142
    cab.append(peca("bico_quilha2", [-q / 2, 29.0 - q / 2, ZF - 3.8], [q / 2, 29.0 + q / 2, ZF - 2.4], mq, rot=(-12, 0, 45),
                    pivo=(0, 29.0, ZF - 2.4), faixa=fb, res=4))
    # gancho: ponta estreita que desce
    cab.append(peca("bico_gancho", [-0.75, 27.7, ZF - 4.7], [0.75, 30.0, ZF - 3.5],
                    mat_cor(lambda p, f_: BICO_CLARO if f_ == "up" else mix(BICO, BICO_ESC, clamp((29.0 - p[1]) / 1.2)), borda=.1, curva=.2),
                    rot=(-28, 0, 0), pivo=(0, 30.0, ZF - 3.5), faixa=(27.7, 30.0), res=4))
    # mandíbula de baixo: curta, estreita e mais escura, recolhida sob a quilha
    cab.append(peca("bico_baixo", [-0.85, 27.2, ZF - 1.7], [0.85, 28.1, ZF + 0.3], mat_cor(lambda p, f_: BICO_ESC, borda=.1), res=4))
    # gema da testa em moldura de ouro (hexágono alto), sobre a ponte da viseira
    gx, gy, gz, GW, GH = 0.0, 35.4, ZF - 1.2, 3.2, 6.0
    mg = mat_gema_testa(gx, gy, GW, GH)
    q = GW / 1.4142; dy = (GH - GW) / 2
    cab.append(peca("gema", [gx - GW / 2, gy - dy, gz - 0.5], [gx + GW / 2, gy + dy, gz + 0.6], mg, res=8, brilho=so_gema))
    for nm, yy in (("gema_cima", gy + dy), ("gema_baixo", gy - dy)):
        cab.append(peca(nm, [gx - q / 2, yy - q / 2, gz - 0.45], [gx + q / 2, yy + q / 2, gz + 0.55], mg, rot=(0, 0, 45),
                        pivo=(gx, yy, gz), res=8, brilho=so_gema))
    # chifres dourados: 2 internos altos (do alto do elmo) e 2 externos em U (saem do lado da gema)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cab.append(g.pena_curva("chifre_int_" + s, (2.3 * lado, 34.8, -2.6),
                                [(5.2, 2.3, 2.1, OURO, OURO), (5.0, 1.9, 1.8, OURO, OURO), (4.0, 1.3, 1.3, OURO, OURO)],
                                (30, 0, -8 * lado), (16, 0, 0), "y", g.mat_seg(mat_ouro), res=3))
        cab.append(g.pena_curva("chifre_ext_" + s, (1.4 * lado, 35.4, gz + 0.3),
                                [(2.6, 1.9, 1.6, OURO, OURO), (3.0, 1.8, 1.6, OURO, OURO), (3.0, 1.5, 1.4, OURO, OURO),
                                 (2.8, 1.0, 1.0, OURO, OURO)],
                                (22, 0, -62 * lado), (12, 0, 24 * lado), "y", g.mat_seg(mat_ouro), res=3))
    # crista: 3 lâminas de chama vermelhas atrás da gema, entre os chifres
    crista = []
    for k, (x, L, rz, rx) in enumerate([(0.0, 6.2, 0, 14), (-1.1, 4.6, 16, 8), (1.1, 4.6, -16, 8)]):
        crista.append(pena(f"crista_{k}", (x, 35.0, -3.6), 90, 1, L, 1.9, [(0, VERMELHO), (0.6, LARANJA_VERM), (1, AMARELO)],
                           flare=180 - rx, varre=rz, T=1.0))
    cab.append(osso("crista", [0, 35.0, -3.6], [0, 0, 0], crista))
    # juba de fogo: poucas penas largas deitadas para trás, coladas aos lados da cabeça (em leque de cima para baixo)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, (y, z, L, W, fl, va, cores) in enumerate(JUBA):
            cab.append(pena(f"juba{k}_{s}", ((LX - 1.5) * lado, y, z), 0, lado, L, W, cores, flare=fl, varre=va, T=1.1))
        # tufo da bochecha (emoldura o rosto de frente, sob a barra do elmo)
        for k, (y, L, fl, va) in enumerate([(31.6, 4.8, 44, 40), (29.0, 4.4, 34, 30)]):
            cab.append(pena(f"tufo{k}_{s}", ((LX + 0.1) * lado, y, ZL + 1.9), 0, lado, L, 2.6, FOGO_VERM, flare=fl, varre=va, T=1.0))
    # nuca: penas do meio (face larga para trás) descendo pelas costas do pescoço
    cab.append(pena("nuca0", (0, 35.2, 1.2), 90, 1, 8.4, 4.4, FOGO_VERM, flare=48, varre=0, T=1.2))
    cab.append(pena("nuca1", (0, 31.6, 1.6), 90, 1, 7.6, 4.2, FOGO_LAR, flare=26, varre=0, T=1.2))
    return cab

JUBA = [  # (y raiz, z raiz, comprimento, largura, flare, varre, paradas): de cima para baixo
    (36.4, -0.2, 8.6, 3.6, 16, 156, FOGO_JUBA), (34.2, 0.8, 8.6, 3.6, 24, 114, FOGO_VERM),
    (31.8, 1.0, 8.4, 3.6, 28, 92, FOGO_JUBA), (29.2, 1.0, 7.4, 3.4, 28, 70, FOGO_JUBA)]

# ---------------- peitoral com o emblema da fênix ----------------
PT_Y0, PT_Y1, PT_X = 16.4, 24.0, 5.8
PT_Z = -9.4

def fenix(x, y):
    """Emblema (quadro "Peitoral Fênix"): fênix amarela de asas em chama abertas para cima e para fora (em V, com
    pontas no alto), corpo estreito no meio e cabeça pequena em cima; devolve a cor ou None (campo vermelho)."""
    ax = abs(x)
    if ax ** 2 + ((y - 22.5) / 1.1) ** 2 <= 0.72 ** 2: return AMARELO                                     # cabeça
    if (ax / 0.95) ** 2 + ((y - 19.4) / 2.7) ** 2 <= 1: return LARANJA if ax < 0.22 and y < 20.5 else AMARELO   # corpo
    if 0.5 <= ax <= 4.6:                                                                                  # asas
        u = (ax - 0.5) / 4.1
        baixo = 17.9 + 3.6 * u ** 1.25 - 0.45 * abs(math.sin(u * math.pi * 3.0))
        topo = min(19.9 + 2.9 * u + 0.75 * max(0.0, math.sin(u * math.pi * 2.6 + 0.4)), 23.3)
        if baixo <= y <= topo:
            return LARANJA if y < baixo + 0.35 else AMARELO_CLARO if y > topo - 0.3 else AMARELO
    return None

def mat_peitoral(c):
    x, y, z = c["p"]; face = c["face"]
    if face != "north": return mat_roxo(c)
    topo = PT_Y1 - 0.7
    if y > topo or abs(x) > PT_X - 1.2: return tom(mix(ROXO, LILAS, 0.3), 0.08 if x < 0 else -0.04)
    if y < PT_Y0 + 0.9: return mix(ROXO, LILAS, 0.2)
    return fenix(x, y) or mix(VERMELHO, VERM_ESC, clamp((topo - y) / 7.0))

def mat_peito_v(cx, cy):
    """Placa de baixo em V (losango girado 45°): borda lilás e a cauda da fênix em chama amarela/laranja."""
    def f(c):
        x, y, z = girar_z(c["p"], (cx, cy), 45)
        if c["face"] != "north": return mat_roxo(c)
        lu, lv = c["p"][0] - cx, c["p"][1] - cy
        S = (c["b"][1][0] - c["b"][0][0]) / 2
        if max(abs(lu), abs(lv)) > S - 0.85: return tom(LILAS, 0.05) if x < 0 else LILAS
        # cauda da fênix: chama amarela descendo para a ponta do V, com 3 línguas, miolo laranja
        larg = 0.6 + (y - 12.6) * 0.42
        if larg > 0 and abs(x) < larg:
            q = abs(x) / larg
            lingua = 12.6 + 1.1 * abs(math.sin(q * math.pi * 1.5))
            if y > lingua: return LARANJA if q < 0.3 and y > 13.6 else AMARELO
        return mix(VERMELHO, VERM_ESC, clamp((16.5 - y) / 4))
    return f

# ---------------- correntes da cauda ----------------
N_CONTAS = 10

def mat_conta(c):
    face = c["face"]
    base = {"up": OURO_CLARO, "down": OURO_ESC}.get(face, OURO if face in ("east", "west") else AMARELO)
    return tom(base, -0.3) if na_borda(c) else base

def mat_pingente(c):
    """Pingente (quadro "Cauda de Fênix"): losango de ouro grosso com a gema vermelha facetada no meio."""
    (x0, y0, z0), (x1, y1, z1) = c["b"]
    face = c["face"]
    if face in ("up", "down"): return OURO_ESC
    if face in ("north", "south"):
        u = (c["p"][0] - (x0 + x1) / 2) / ((x1 - x0) / 2); v = (c["p"][1] - (y0 + y1) / 2) / ((y1 - y0) / 2)
    else:
        u = (c["p"][2] - (z0 + z1) / 2) / ((z1 - z0) / 2); v = (c["p"][1] - (y0 + y1) / 2) / ((y1 - y0) / 2)
    m = max(abs(u), abs(v))
    if m > 0.9: return OURO_ESC
    if m > 0.5: return OURO_CLARO if u + v > 0 else OURO
    if u > 0 and v > 0: return GEMA_CLARA
    if u < 0 and v < 0: return GEMA_ESC
    return GEMA

def corrente(nome, base, rot0, curva, n, passo=2.0, conta=1.7):
    """Corrente de contas douradas (um osso por conta, '<nome>_k', cresce em +z local e dobra 'curva' graus em x a
    cada junta; 'curva' pode ser uma lista, uma por junta). No fim pendura o pingente de losango, desvirado para ficar
    na vertical."""
    curvas = list(curva) if isinstance(curva, (list, tuple)) else [curva] * n
    def seg(k, pos):
        px, py, pz = pos
        h = conta / 2
        filhos = [peca(f"{nome}_{k}", [px - h, py - h, pz + passo * 0.08], [px + h, py + h, pz + passo * 0.86], mat_conta,
                       rot=(0, 0, 45), pivo=(px, py, pz), res=3)]
        if k + 1 < n:
            filhos.append(seg(k + 1, (px, py, pz + passo)))
        else:
            giro = -(rot0[0] + sum(curvas[1:n]))
            pz2 = pz + passo
            S = 3.4
            filhos.append(osso(f"{nome}_pingente", [px, py, pz2], [giro, 0, 0], [
                peca(f"{nome}_pingente", [px - S / 2, py - S - 0.6, pz2 - 0.5], [px + S / 2, py - 0.6, pz2 + 0.5], mat_pingente,
                     rot=(0, 0, 45), pivo=(px, py - S / 2 - 0.6, pz2), res=6, brilho=so_gema),
                peca(f"{nome}_pingente_b", [px - 0.45, py - S - 0.6, pz2 - S / 2], [px + 0.45, py - 0.6, pz2 + S / 2], mat_pingente,
                     rot=(45, 0, 0), pivo=(px, py - S / 2 - 0.6, pz2), res=6, brilho=so_gema),
                peca(f"{nome}_argola", [px - 0.4, py - 0.8, pz2 - 0.4], [px + 0.4, py + 0.4, pz2 + 0.4], mat_conta, res=3)]))
        return osso(f"{nome}_{k}", list(pos), list(rot0) if k == 0 else [curvas[k], 0, 0], filhos)
    return seg(0, tuple(base))

CORRENTES = [("corrente_c", (0.0, 21.0, 8.4), (16, 0, 0)), ("corrente_d", (-2.0, 21.4, 8.0), (14, -22, 0)),
             ("corrente_e", (2.0, 21.4, 8.0), (14, 22, 0))]
CURVA_CORRENTE = [0, 1, 2, 3, 4, 6, 9, 13, 16, 12]
def _segs(n, L0, L1, w0, w1):
    """n segmentos que afinam: comprimento L0 -> L1, seção w0 -> w1 (tubos quase quadrados, como na arte)."""
    return [(L0 + (L1 - L0) * k / (n - 1), w0 + (w1 - w0) * k / (n - 1), (w0 + (w1 - w0) * k / (n - 1)) * 1.15) for k in range(n)]

PLUMAS = [  # nome, raiz, rot0, curva, segmentos (comprimento, largura x, altura y), paradas
    # leque de fênix (arte): plumas grossas que saem do alto das costas, sobem e caem em foice; a do meio é a mais
    # alta, as outras abrem para os lados e para trás, cada vez mais baixas
    ("pluma0", (0.0, 24.2, 6.0), (-50, 0, 0), (15, 0, 0), _segs(6, 3.8, 2.8, 3.4, 1.6), FOGO_VERM),
    ("pluma1", (-1.8, 23.2, 6.4), (-36, -22, 0), (14, 0, 0), _segs(6, 3.6, 2.6, 3.3, 1.5), FOGO_LAR),
    ("pluma2", (1.8, 23.2, 6.4), (-36, 22, 0), (14, 0, 0), _segs(6, 3.6, 2.6, 3.3, 1.5), FOGO_LAR),
    ("pluma3", (-2.4, 21.8, 6.4), (-22, -38, 0), (14, 0, 0), _segs(5, 3.6, 2.6, 3.2, 1.5), FOGO_VERM),
    ("pluma4", (2.4, 21.8, 6.4), (-22, 38, 0), (14, 0, 0), _segs(5, 3.6, 2.6, 3.2, 1.5), FOGO_VERM),
]
ONDAS = [(n, N_CONTAS, (3.0, 2.0, 1.5)) for n, _, _ in CORRENTES] + [(p[0], len(p[4]), (2.0, 1.5, 0.0)) for p in PLUMAS]

def mat_pluma(paradas, n):
    """Segmento k de n da pluma: degradê ao longo do comprimento (z), metade de cima clara, contorno escuro."""
    def fabrica(c0, c1, ei, inv):
        def f(c):
            nome = c["nome"]; k = int(nome.rsplit("_", 1)[-1])
            (x0, y0, z0), (x1, y1, z1) = c["b"]
            t = (k + clamp((c["p"][2] - z0) / max(z1 - z0, 1e-6))) / n
            base = grad(paradas, t)
            face = c["face"]
            if face == "up": return claro(base, 0.1)
            if face == "down": return tom(base, -0.4)
            if face in ("east", "west"):
                v = (c["p"][1] - (y0 + y1) / 2) / max((y1 - y0) / 2, 1e-6)
                cor = claro(base, 0.08) if v > 0 else tom(base, -0.08)
                if abs(v) < 0.1: cor = claro(cor, 0.08)
                if c["j"] in (0, c["th"] - 1): cor = tom(cor, -0.28)
                return cor
            return tom(base, -0.15)
        return f
    return fabrica

# ---------------- montagem ----------------
K_CAB, SOBE_CAB = 0.82, 2.4       # dono (2026-11-12): "cabeça muito grande e sem pescoço" -> cabeça menor e mais alta

def montar():
    i_cab = len(g.PECAS)
    cab = cabeca_ossos()
    g.transformar(i_cab, cab, (0.0, 27.5, -3.0), k=K_CAB, sobe=SOBE_CAB)
    cabeca = osso("cabeca", [0, 27.5 + SOBE_CAB, -3.0], [0, 0, 0], cab)
    yp1 = 28.6 + SOBE_CAB
    def cor_pescoco(p, f_):
        x, y, z = p
        if z < -4.4 and abs(x) < 1.25:                                     # garganta creme estreita (arte)
            if y > yp1 - 0.9: return tom(CREME_SOMBRA, -0.25)                # sombra sob o queixo
            return mix(CREME_SOMBRA, CREME, clamp((y - 24) / 4))
        return mix(VERM_ESC, VERMELHO, clamp((y - 22) / 7))
    pescoco = osso("pescoco", [0, 25.0, -2.5], [0, 0, 0], [
        *g.octogono("pescoco", [-2.5, 23.0, -4.9], [2.5, yp1, 1.2], mat_cor(cor_pescoco, borda=.0, curva=.3), r=0.8, faixa=(22, yp1)),
        cabeca])

    corpo = []
    mtronco = mat_cor(lambda p, f_: mix(VERM_ESC, LARANJA_VERM, clamp((p[1] - 10) / 14)), borda=.0, curva=.3)
    corpo += g.arredondado2("tronco", [-5.6, 10.6, -8.2], [5.6, 24.6, 6.4], mtronco, r=2.0, faixa=(10, 25), res=2)

    # peitoral duplo: placa de cima com a fênix + placa de baixo em V (cauda da fênix) + quilha lilás no colar
    pt = g.arredondado("peitoral", [-PT_X, PT_Y0, PT_Z], [PT_X, PT_Y1, PT_Z + 2.0], mat_peitoral, r=0.9, res=6)
    corpo.append(osso("peitoral", [0, 21.0, -8.0], [-6, 0, 0], pt))
    S = 7.6; cvx, cvy = 0.0, 16.7
    corpo.append(peca("peito_v", [cvx - S / 2, cvy - S / 2, PT_Z + 0.45], [cvx + S / 2, cvy + S / 2, PT_Z + 2.0], mat_peito_v(cvx, cvy),
                      rot=(0, 0, 45), pivo=(cvx, cvy, PT_Z + 1.5), res=6))
    q = 2.4
    corpo.append(peca("quilha", [-q / 2, 23.7 - q / 2, PT_Z - 0.55], [q / 2, 23.7 + q / 2, PT_Z + 1.2], mat_roxo, rot=(0, 0, 45),
                      pivo=(0, 23.7, PT_Z), res=4))

    # capa de asas: ombreira de armadura roxa + 3 fileiras de penas de fogo em leque (osso animável asa_d / asa_e)
    FILEIRAS = [  # (y raiz, raio x, raio z, z centro, abre, trás, lado, L, W, phis, paradas, armadura)
        (26.4, 6.0, 5.6, -2.0, 52, 18, 0, 7.2, 5.4, [-46, -8, 30], None, True),
        (24.4, 6.4, 6.4, -1.6, 38, 16, 0, 7.6, 5.0, [-28, 10, 48], None, True),
        (23.4, 6.6, 7.0, -1.0, 16, 18, 8, 8.0, 5.0, [-48, -16, 16, 48, 82], FOGO_ROXO, False),
        (19.6, 7.2, 8.0, -0.2, 16, 42, 20, 10.8, 5.2, [-56, -26, 4, 34, 64, 96], FOGO_VERM, False),
        (15.6, 7.4, 8.4, 0.4, 18, 50, 30, 12.4, 5.2, [-62, -34, -6, 22, 50, 78, 106], FOGO_CAPA, False),
    ]
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        for a, (y0, ax, az, zc, F0, B, O, L, W, phis, cores, arm) in enumerate(FILEIRAS):
            for k, phi in enumerate(phis):
                x, z = anel(ax, az, zc, phi, lado)
                # a ponta vai para trás (B) e para o lado (O) em coordenadas do mundo: decompõe em 'flare' (para fora
                # da superfície) e 'varre' (tangente); as penas da frente quase não abrem para o lado
                r = math.radians(phi)
                o = O * (0.3 if phi < -20 else 0.6 if phi < 10 else 1.0)
                if arm: ff, vv = F0, B
                else:
                    ff = max(F0 + o * math.cos(r) + B * math.sin(r), F0 * 0.4)
                    vv = -o * math.sin(r) + B * math.cos(r)
                asa.append(pena(f"asa{a}{k}_{s}", (x, y0 - 0.3 * (k % 2), z), phi, lado, L * (0.94 + 0.08 * (k % 2)), W, cores,
                                flare=ff, varre=vv, T=1.3 if arm else 1.0, armadura=arm))
        corpo.append(osso("asa_" + s, [6.0 * lado, 25.0, -1.0], [0, 0, 0], asa))

    # costas: penas do meio entre as asas
    for k, (x, y, z, L, fl) in enumerate([(0, 24.0, 5.6, 9.0, 22), (0, 18.6, 6.6, 9.4, 24), (0, 14.6, 6.8, 11.6, 26),
                                          (-2.8, 13.6, 6.2, 10.6, 30), (2.8, 13.6, 6.2, 10.6, 30)]):
        corpo.append(pena(f"costas{k}", (x, y, z), 90, 1, L, 4.6, FOGO_JUBA if k < 3 else FOGO_CAPA, flare=fl, T=1.1))

    # cauda de fênix: plumas em foice + 3 correntes de contas com pingentes
    cauda = []
    for nome, raiz, rot0, curva, segs, cores in PLUMAS:
        n = len(segs)
        cauda.append(g.pena_curva(nome, raiz, [(L, w, h, None, None) for L, w, h in segs], rot0, curva, "z",
                                  mat_pluma(cores, n), brilho_ponta=True, res=2))
    for nome, raiz, rot0 in CORRENTES:
        cauda.append(corrente(nome, raiz, rot0, CURVA_CORRENTE, N_CONTAS, passo=2.5, conta=2.3))
    corpo.append(osso("cauda", [0, 19.0, 5.5], [0, 0, 0], cauda))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 12.0, -1.0], [0, 0, 0], corpo)

    # ---------- pernas: coxa de penas, bota roxa com aba lilás, pé dourado reforçado (3 dedos + 1 atrás) ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 3.5 * lado; zc = -0.6
        pp = []
        # coxa grossa de penas (calça de fogo): volume arredondado + 3 penas que caem por cima da aba da bota
        pp += g.arredondado("coxa_" + s, [xc - 2.3, 7.0, zc - 2.4], [xc + 2.3, 12.8, zc + 2.0],
                            mat_cor(lambda p, f_: mix(LARANJA, VERMELHO, clamp((p[1] - 7) / 5)), borda=.1, curva=.3), r=0.8,
                            faixa=(7.0, 12.8), res=2)
        for k, (phi, dx, dz) in enumerate(((-90, 0.0, -2.3), (-30, 1.9, -1.2), (40, 1.9, 1.2))):
            pp.append(pena(f"coxa_pena{k}_{s}", (xc + dx * lado, 11.6, zc + dz), phi, lado, 5.6, 3.4, FOGO_CAPA, flare=10, varre=0, T=1.0))
        def cor_bota(p, f_):
            x, y, z = p
            if f_ == "north" and (abs(x - xc) < 0.18 or abs(y - 4.8) < 0.15) and y < 5.0: return ROXO_ESC
            return ROXO
        pp += g.octogono("bota_" + s, [xc - 2.3, 2.3, zc - 2.6], [xc + 2.3, 5.8, zc + 2.0], mat_cor(cor_bota, borda=.14, curva=.3), r=0.7,
                         faixa=(2.3, 5.8))
        pp += g.octogono("bota_aba_" + s, [xc - 2.6, 5.5, zc - 2.9], [xc + 2.6, 7.1, zc + 2.3],
                         mat_cor(lambda p, f_: LILAS, borda=.16, curva=.3), r=0.8, faixa=(5.5, 7.1))
        mpe = mat_cor(lambda p, f_: OURO_CLARO if f_ == "up" else (OURO_ESC if f_ == "down" else OURO), borda=.14, curva=.35)
        mgarra = mat_cor(lambda p, f_: AMARELO_CLARO if f_ == "up" else (OURO_ESC if f_ == "down" else AMARELO), borda=.16, curva=.3)
        pp.append(peca("pe_" + s, [xc - 2.4, 0, zc - 3.0], [xc + 2.4, 2.5, zc + 1.6], mpe, faixa=(0, 2.5), res=2))
        for nome, giro, dx, comp in (("meio", 0, 0, 6.4), ("fora", -20 * lado, 1.7 * lado, 5.6), ("dentro", 20 * lado, -1.7 * lado, 5.6)):
            x0, z0 = xc + dx, zc - 2.4
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .9, 0, z0 - comp * 0.66], [x0 + .9, 2.4, z0 + 0.2], mpe, faixa=(0, 2.4), res=2),
                peca(f"garra_{nome}_{s}", [x0 - .72, 0.35, z0 - comp], [x0 + .72, 2.0, z0 - comp * 0.66 + 0.3], mgarra,
                     rot=(-14, 0, 0), pivo=(x0, 2.0, z0 - comp * 0.66 + 0.3), faixa=(0, 2.0), res=2)]))
        pp.append(peca("dedo_tras_" + s, [xc - .8, 0, zc + 1.2], [xc + .8, 1.7, zc + 3.6], mpe, faixa=(0, 1.7), res=2))
        return osso("perna_" + s, [xc, 12.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

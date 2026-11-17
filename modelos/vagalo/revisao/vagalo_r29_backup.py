"""Vagaló (#009, Elétrico): galo-vaga-lume veloz, roxo-escuro, com asas de inseto douradas e abdômen que brilha."""
import math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, PRETO

ID = "vagalo"; NOME = "Vagaló"; NUMERO = 9
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 27.6, -1.2), 7.0)
ONDAS = [("cauda_meio", 6, (3, 0, 0))]

# ---------------- paleta (Paleta de Cores da ficha) ----------------
ROXO_ESC = (52, 36, 68); ROXO = (88, 66, 112); ROXO_MED = (116, 90, 142); MALVA = (148, 120, 170); LILAS = (172, 148, 192)
CREME = (240, 220, 204); CREME_ESC = (198, 172, 182)
AMAR_PALIDO = (255, 242, 156); AMAR_CLARO = (255, 226, 96); AMARELO = (252, 200, 36); AMBAR = (238, 150, 24)
LARANJA = (240, 128, 28); VERM = (218, 32, 40); VERM_ESC = (160, 18, 34); VERM_VIVO = (246, 64, 44)
PERNA = (250, 188, 40); PERNA_ESC = (226, 132, 24)

SOBE_CAB = 0.8        # a cabeça sobe (pescoço visível acima dos ombros)
K_CAB = 0.8           # escala da cabeça
INCLINA = 12          # corpo levemente inclinado (peito alto)

def brilho_amarelo(c, cor):
    """Só os pixels amarelos/laranja-claros brilham (pontas de pena, pontas da crista)."""
    return cor[0] > 215 and cor[1] > 135 and cor[2] < 150

# ---------------- cabeça ----------------
FAC_T = 1.6                                    # espessura da peça da face diagonal (onde fica o olho)
FAC_S = (3.1, -4.5)                            # ponto (x, z) da superfície da faceta (lado +x)
FAC_C = (FAC_S[0] - 0.7071 * FAC_T / 2, FAC_S[1] + 0.7071 * FAC_T / 2)
FAC_L = 3.6
OLHO_Y = 26.3

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return mix(ROXO_MED, MALVA, 0.35)
    base = ROXO_MED if face == "north" else ROXO
    if y < 24.4: base = mix(base, ROXO_ESC, 0.25)
    return base

def olho(u, v):
    return g.pintar_olho(u, v, 1.5, 1.38, iris=((196, 118, 8), (250, 186, 24)), esclera=(255, 228, 92), pupila=PRETO,
                         r_iris=(0.58, 0.66), c_iris=(-0.3, -0.02), r_pup=(0.3, 0.36), bravo=0.45, alto=0.52,
                         contorno=(40, 24, 44))

def mat_faceta(lado):
    base = g.mat_cor(cor_cabeca, borda=.03, curva=.35)
    fora = "east" if lado > 0 else "west"
    def f(c):
        if c["face"] == fora:
            x, y, z = c["p"]
            cor = olho(z - FAC_C[1], y - OLHO_Y)
            if cor is not None: return cor
        return base(c)
    return f

def brilho_olho(lado):
    fora = "east" if lado > 0 else "west"
    def f(c, cor):
        if c["face"] != fora: return False
        x, y, z = c["p"]
        o = olho(z - FAC_C[1], y - OLHO_Y)
        return o is not None and o[0] > 180 and o[1] > 100
    return f

def cor_bico(p, face):
    x, y, z = p
    if face in ("east", "west") and abs(z + 6.6) < 0.28 and abs(y - 25.35) < 0.22: return (150, 80, 20)   # narina
    if face == "down": return AMBAR
    return mix((255, 214, 56), (242, 150, 26), clamp((25.8 - y) / 2.4 + clamp((-z - 8.4) / 2.2) * 0.5))

def mat_placa_cabeca():
    return g.mat_facetado(mix(MALVA, LILAS, .4), MALVA, ROXO_MED, ROXO_ESC, quina=-0.35)

def cabeca_pecas():
    cab = []
    mc = g.mat_cor(cor_cabeca, borda=.03, curva=.35)
    fx = (22.6, 30.0)
    cab.append(peca("cranio_lados", [-4.2, 23.0, -3.4], [4.2, 29.4, 2.6], mc, faixa=fx, res=4))
    cab.append(peca("cranio_meio", [-3.6, 22.6, -4.3], [3.6, 29.8, 3.1], mc, faixa=fx, res=4))
    cab.append(peca("cranio_frente", [-2.0, 22.8, -5.6], [2.0, 29.5, -4.2], mc, faixa=fx, res=4))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 23.2, cz - FAC_L / 2], [cx + FAC_T / 2, 29.2, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=fx, res=8, brilho=brilho_olho(lado)))
        # sobrancelha clara por cima do olho, descendo para o bico (cara brava)
        fx0, fx1 = sorted((cx + FAC_T / 2 * lado - 0.1 * lado, cx + FAC_T / 2 * lado + 0.45 * lado))
        cab.append(osso("sobrancelha_" + s, [cx, 27.6, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [fx0, 27.15, cz - 1.9], [fx1, 28.05, cz + 1.6], mat_placa_cabeca(),
                 rot=(-18, 0, 0), pivo=(cx, 27.6, cz), res=4)]))
    # bico amarelo em cunha com gancho
    mb = g.mat_cor(cor_bico, borda=.05, curva=.3)
    fb = (23.0, 26.2)
    cab.append(peca("bico_base", [-1.8, 23.6, -7.0], [1.8, 26.3, -5.3], mb, faixa=fb, res=4))
    cab.append(peca("bico_meio", [-1.45, 23.85, -9.0], [1.45, 26.0, -6.8], mb, rot=(-10, 0, 0), pivo=(0, 26.0, -6.8), faixa=fb, res=4))
    cab.append(peca("bico_ponta", [-1.15, 23.5, -10.8], [1.15, 25.5, -8.8], mb, rot=(-22, 0, 0), pivo=(0, 25.4, -8.8), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-1.2, 23.0, -8.8], [1.2, 23.9, -5.3], g.mat_cor(lambda p, f: AMBAR, borda=.1), rot=(6, 0, 0),
                    pivo=(0, 23.5, -5.3), res=4))
    # barbela vermelha em dois lobos
    mbar = g.mat_cor(lambda p, f: mix(VERM_ESC, VERM_VIVO, clamp((p[1] - 19.0) / 4.0)), borda=.08, curva=.3)
    cab.append(peca("barbela_a", [-1.4, 20.8, -6.9], [1.4, 23.4, -5.0], mbar, faixa=(19.0, 23.4), res=4))
    cab.append(peca("barbela_b", [-1.1, 19.2, -6.7], [1.1, 21.0, -5.2], mbar, faixa=(19.0, 23.4), res=4))
    # lâminas de penas em camadas saindo para trás e para os lados (cabeça "em degraus" da ficha)
    mpl = mat_placa_cabeca()
    def mpc(c0, c1, ei, inv): return mat_pena_bloco(c0, c1, ei, inv)
    for k, (y0, rx, L) in enumerate([(28.2, 6, 5.6), (26.3, 12, 6.2), (24.4, 18, 5.2)]):
        for lado in (-1, 1):
            s_ = "d" if lado < 0 else "e"
            cab.append(g.pena_curva(f"lamina{k}_{s_}", (3.3 * lado, y0, -1.6),
                                    [(L * .55, 1.5, 1.7, ROXO, ROXO_MED), (L * .45, 1.0, 1.1, ROXO_MED, MALVA)],
                                    (rx, 50 * lado, 0), (6, 8 * lado, 0), "z", mpc, res=4))
    for k, (x0, y0, rx, L) in enumerate([(-1.3, 28.4, 14, 5.4), (1.3, 27.0, 20, 5.8), (-0.2, 25.2, 28, 5.0)]):
        cab.append(g.pena_curva(f"lamina_nuca{k}", (x0, y0, 2.0), [(L * .55, 2.0, 1.8, ROXO, ROXO_MED), (L * .45, 1.3, 1.2, ROXO_MED, MALVA)],
                                (rx, 8 * (1 if x0 > 0 else -1), 0), (8, 0, 0), "z", mpc, res=4))
    cab.append(crista())
    return cab

def crista():
    """Crista elétrica: colunas de blocos vermelhos inclinadas para trás, pontas laranja e amarelas (brilham)."""
    def mcr(c0, c1, ei, inv): return g.mat_pena(c0, c1, ei, inv, borda=.14)
    def coluna(nome, base, rot0, curva, k, w=3.6, h=2.7):
        segs = [(2.8 * k, w, h, VERM_ESC, VERM), (2.4 * k, w * .88, h * .9, VERM, VERM_VIVO), (0.9 * k, w * .78, h * .8, VERM_VIVO, LARANJA),
                (1.0 * k, w * .66, h * .7, AMARELO, AMAR_CLARO)]
        return g.pena_curva(nome, base, segs, rot0, curva, "y", mcr, brilho_ponta=True, res=4)
    filhos = [coluna("crista_c0", (0, 29.3, -3.0), (-8, 0, 0), (8, 0, 0), 0.85),
              coluna("crista_c1", (0, 29.4, -1.0), (12, 0, 0), (10, 0, 0), 1.25),
              coluna("crista_c2", (0, 29.4, 1.0), (30, 0, 0), (10, 0, 0), 1.15),
              coluna("crista_c3", (0, 29.2, 2.6), (48, 0, 0), (10, 0, 0), 0.95),
              coluna("crista_c4", (0, 28.8, 3.6), (66, 0, 0), (8, 0, 0), 0.75)]
    filhos.append(peca("crista_base", [-2.0, 29.0, -4.0], [2.0, 30.6, 3.6],
                       g.mat_cor(lambda p, f: mix(VERM_ESC, VERM, clamp((p[1] - 29.0) / 1.6)), borda=.1), res=4))
    for lado in (-1, 1):                          # dedos dos lados, mais baixos: crista larga e em degraus de frente
        s = "d" if lado < 0 else "e"
        filhos.append(coluna("crista_l1_" + s, (2.0 * lado, 29.2, -1.8), (6, 0, -14 * lado), (8, 0, -4 * lado), 0.78, w=2.2, h=2.4))
        filhos.append(coluna("crista_l2_" + s, (1.9 * lado, 29.1, 1.2), (34, 0, -14 * lado), (10, 0, -4 * lado), 0.7, w=2.0, h=2.2))
    return osso("crista", [0, 29.4, -0.5], [0, 0, 0], filhos)

def mat_pena_bloco(c0, c1, ei, inv):
    """Pena em bloco (asa dobrada, cauda): degradê no comprimento, fio claro em cima e sombra embaixo nas faces largas."""
    base = g.mat_pena(c0, c1, ei, inv, borda=.15)
    def f(c):
        cor = base(c)
        if c["face"] in ("east", "west"):
            y0, y1 = c["b"][0][1], c["b"][1][1]
            t = (c["p"][1] - y0) / max(y1 - y0, 1e-6)
            if t > 0.8: cor = tom(cor, 0.14)
            elif t < 0.25: cor = tom(cor, -0.22 * (0.25 - t) / 0.25)
        return cor
    return f

def cor_tronco(p, face):
    """Plumagem roxa com fileiras de penas (escamas) pintadas: borda de baixo de cada pena mais escura."""
    x, y, z = p
    h = (z if face in ("east", "west") else x) / 2.6
    fy = (y - 1.0 * (math.floor(h) % 2)) / 2.0
    jy, jh = fy - math.floor(fy), h - math.floor(h)
    if jy < 0.14 * (1 - abs(2 * jh - 1) ** 2) + 0.05: return mix(ROXO, ROXO_ESC, 0.4)
    return mix(ROXO, ROXO_MED, 0.35 * jy)

def mat_abdomen():
    """Abdômen de vaga-lume: placas amarelas em fileiras (como tijolos), centro mais claro, juntas âmbar."""
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        T = 2.8                                                     # lado de cada placa
        fy = (y - 4.0) / T
        h = (x if face in ("north", "south", "up", "down") else z - 8.6) / T + 0.5
        if face in ("up", "down"): fy = (z - 8.6) / T + 0.5
        jy, jh = fy - math.floor(fy), h - math.floor(h)
        sy, sh = min(jy, 1 - jy) * T, min(jh, 1 - jh) * T           # distância até a junta (unidades)
        dj = min(sy, sh)
        if dj < 0.13: cor = (222, 128, 12)
        else: cor = mix((250, 160, 14), (255, 230, 70), clamp((dj - 0.13) / (T / 2 - 0.13)) ** 0.8)
        # sombreado de esfera: centro de cada face aceso, beiradas puxando para o âmbar (lê como uma bola)
        ex, ey, ez = x / 5.9, (y - 9.0) / 5.2, (z - 8.6) / 6.6
        r = math.hypot(ex, ey) if face in ("north", "south") else math.hypot(ez, ey) if face in ("east", "west") else math.hypot(ex, ez)
        luz = 0.06 - 0.4 * clamp((r - 0.35) / 0.8) ** 1.3 + 0.04 * ey
        if face == "down": luz -= 0.15
        return tom(cor, luz)
    return f

def cor_ombro(p, face):
    """Ombro da asa: penas pequenas (coberteiras) em escamas, roxo com beirada clara."""
    x, y, z = p
    h = (z if face in ("east", "west") else x) / 2.4
    fy = (y - 1.0 * (math.floor(h) % 2)) / 2.0
    jy, jh = fy - math.floor(fy), h - math.floor(h)
    if jy < 0.14 * (1 - abs(2 * jh - 1) ** 2) + 0.05: return mix(ROXO, ROXO_ESC, 0.35)
    return mix(ROXO, ROXO_MED, 0.45 * jy)

def mat_peito(k, y0, y1):
    """Fileira de penas do peito: creme no meio, malva nos lados e embaixo; pontas recortadas na beirada de baixo."""
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        cor = mix(CREME, CREME_ESC, clamp((20.5 - y) / 5.0))
        cor = mix(cor, MALVA, clamp((abs(x) - 1.0) / 2.0 + 0.3 * k))
        if face in ("east", "west", "up", "down"): cor = mix(cor, ROXO_MED, 0.6)
        if face == "north":
            u = (x / 1.55 + (0.5 if k % 2 else 0.0)) % 1.0
            h = y - y0
            if h < 1.3 * abs(2 * u - 1) ** 1.2: return None
            if h < 1.3 * abs(2 * u - 1) ** 1.2 + 0.22: return tom(cor, -0.4)
            if abs(2 * u - 1) > 0.9 and h > 1.0: cor = tom(cor, -0.18)          # risco entre uma pena e outra
            cor = tom(cor, 0.12 * (1 - abs(2 * u - 1)) - 0.2 * clamp(1 - h / 2.0))
        luz = 0.1 if face == "up" else -0.3 if face == "down" else 0.0
        if face != "north" and g.na_borda(c): luz -= 0.15
        return tom(cor, luz + 0.12 * (y - y0) / max(y1 - y0, 1))
    return f

def montar():
    corpo = []
    # ---------- cabeça (um pouco menor que o desenho base: na ficha o corpo é que domina) ----------
    i_cab = len(g.PECAS)
    cab = cabeca_pecas()
    cabeca = osso("cabeca", [0, 23.5, -1.0], [4, 0, 0], cab)
    g.transformar(i_cab, [cabeca], (0, 22.4, -1.0), K_CAB, sobe=SOBE_CAB)
    pescoco = osso("pescoco", [0, 19.5, -1.0], [-INCLINA, 0, 0], [
        *g.arredondado("pescoco", [-2.7, 18.4, -3.6], [2.7, 24.2, 1.4], g.mat_cor(lambda p, f: ROXO, borda=.05, curva=.4), r=0.8),
        cabeca])
    corpo.append(pescoco)

    # ---------- tronco (ovo deitado) e abdômen de vaga-lume (bola brilhante embaixo, atrás) ----------
    mtr = g.mat_cor(cor_tronco, borda=.03, curva=.55)
    corpo += g.arredondado2("tronco", [-5.6, 10.8, -4.7], [5.6, 20.0, 10.0], mtr, r=3.4, faixa=(8.0, 20.0))
    corpo += g.arredondado2("abdomen", [-5.9, 4.4, 2.0], [5.9, 14.2, 15.2], mat_abdomen(), r=4.2, brilho=True)
    corpo.append(peca("dorso_baixo", [-3.4, 11.2, 4.0], [3.4, 14.4, 11.6], mtr, faixa=(8.0, 20.0)))
    corpo += g.arredondado("abdomen_meio", [-5.2, 5.2, 2.7], [5.2, 13.4, 14.5], mat_abdomen(), r=2.6, brilho=True)
    corpo += g.arredondado("abdomen_fora", [-4.3, 4.5, 3.6], [4.3, 14.1, 13.6], mat_abdomen(), r=1.0, brilho=True)

    # ---------- peito: fileiras de penas creme em degraus, com a beirada de baixo recortada em pontas ----------
    for k, (x1, y0, y1, z0) in enumerate([(2.8, 16.4, 20.0, -5.4), (2.6, 14.0, 17.2, -5.2), (2.2, 11.8, 15.0, -4.9)]):
        corpo.append(peca(f"peito_fileira{k}", [-x1, y0, z0], [x1, y1, -2.6], mat_peito(k, y0, y1), res=4, faixa=(11.0, 20.0)))
    # saia de penas roxas na beirada de baixo do tronco, por cima do abdômen (esconde a junta tronco/abdômen)
    for k, phi in enumerate((-40, -5, 30, 62)):
        for lado in (-1, 1):
            x, z = g.anel(5.6, 7.4, 2.6, phi, lado)
            corpo.append(g.pena_cone_placa(f"saia{k}_{'d' if lado < 0 else 'e'}", (x, 12.6, z), phi, 24, 4.2, 3.6,
                                           (ROXO, ROXO_MED, MALVA), lado, varre=0, curva=0.1))
    x, z = g.anel(5.6, 7.4, 2.6, 90, 1)
    corpo.append(g.pena_cone_placa("saia_tras", (0, 12.8, z), 90, 26, 4.2, 4.0, (ROXO, ROXO_MED, MALVA), 1, varre=0, curva=0.0))

    # golinha: penas roxas em leque saindo de baixo da cabeça por cima do pescoço (rufo da ficha)
    for k, (phi, y0, L, W, fl) in enumerate([(-50, 24.4, 5.0, 3.4, 30), (-12, 24.8, 5.6, 3.6, 28), (26, 24.8, 5.8, 3.6, 24),
                                             (62, 24.4, 5.6, 3.6, 20)]):
        for lado in (-1, 1):
            x, z = g.anel(2.7, 2.9, -1.2, phi, lado)
            corpo.append(g.pena_cone_placa(f"gola{k}_{'d' if lado < 0 else 'e'}", (x, y0, z), phi, fl, L, W,
                                           (ROXO_MED, ROXO, ROXO_ESC), lado, varre=0, curva=0.1))
    x, z = g.anel(2.7, 2.9, -1.2, 90, 1)
    corpo.append(g.pena_cone_placa("gola_nuca", (0, 24.8, z), 90, 18, 6.0, 4.0, (ROXO_MED, ROXO, ROXO_ESC), 1, varre=0, curva=0.0))

    # ---------- asas dobradas (penas roxas com ponta amarela) ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        for k, (rx, L, dx, dy) in enumerate([(-8, 7.4, 0.0, 0.0), (-6, 8.4, 0.25, -1.45), (-4, 9.0, 0.5, -2.9), (-2, 8.6, 0.7, -4.35),
                                             (0, 7.6, 0.9, -5.6)]):
            segs = [(L * .3, 1.0, 2.0, ROXO_ESC, ROXO), (L * .25, 0.9, 1.9, ROXO, ROXO_MED), (L * .27, 0.8, 1.6, AMARELO, AMARELO),
                    (L * .18, 0.7, 1.0, AMARELO, AMARELO)]
            asa.append(g.pena_curva(f"asa{k}_{s}", ((5.8 + dx) * lado, 18.8 + dy, -1.6), segs, (rx, 6 * lado, 0), (6, 0, 0), "z",
                                    mat_pena_bloco, brilho_ponta=True))
        # ombro arredondado da asa dobrada (de onde saem as penas listradas)
        x0, x1 = sorted((4.9 * lado, 7.0 * lado))
        asa += g.arredondado2("ombro_" + s, [x0, 14.4, -3.0], [x1, 19.8, 2.4], g.mat_cor(cor_ombro, borda=.03, curva=.5), r=1.2,
                              faixa=(12.0, 20.0))
        corpo.append(osso("asa_" + s, [5.8 * lado, 18.0, -1.6], [0, 0, 0], asa))

    # ---------- cauda ----------
    cauda = []
    def pena_cauda(nome, base, rot0, curva, k=1.0):
        """Foice comprida: sobe para trás e faz o arco para baixo; ponta amarela afinando (últimos ~35%)."""
        segs = [(2.6 * k, 1.3, 3.0, ROXO_ESC, ROXO), (2.6 * k, 1.2, 2.8, ROXO, ROXO_MED), (2.4 * k, 1.1, 2.5, ROXO_MED, ROXO),
                (2.0 * k, 1.0, 2.2, ROXO, AMBAR), (2.0 * k, 0.85, 1.8, AMARELO, AMARELO), (1.6 * k, 0.65, 1.1, AMARELO, AMARELO)]
        return g.pena_curva(nome, base, segs, rot0, curva, "z", mat_pena_bloco, brilho_ponta=True)
    cauda.append(pena_cauda("cauda_meio", (0, 20.6, 8.6), (-35 - INCLINA, 0, 0), (14, 0, 0), 1.4))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cauda.append(pena_cauda("cauda1_" + s, (1.5 * lado, 20.0, 8.8), (-32 - INCLINA, 16 * lado, 14 * lado), (14, 0, 0), 1.3))
        cauda.append(pena_cauda("cauda2_" + s, (2.6 * lado, 19.0, 9.0), (-26 - INCLINA, 30 * lado, 26 * lado), (13, 0, 0), 1.15))
    corpo.append(osso("cauda", [0, 18.0, 8.8], [0, 0, 0], cauda))

    # ---------- asas de inseto ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        corpo.append(asa_inseto("asa_inseto_" + s, (3.8 * lado, 19.8, 3.6), 17.0, 7.0, lado, (0, -38 * lado, 24 * lado), 1))
        corpo.append(asa_inseto("asa_inseto2_" + s, (3.6 * lado, 18.0, 5.4), 12.5, 5.4, lado, (0, -50 * lado, 0), 2))

    tronco = osso("corpo", [0, 10.0, 2.0], [INCLINA, 0, 0], corpo)
    # pontas amarelas das penas, da cauda e da crista brilham no escuro (só os pixels amarelos)
    for pc in g.PECAS:
        if pc.nome.startswith(("asa", "cauda", "crista_c", "crista_l")) and pc.brilho is not True:
            pc.brilho = brilho_amarelo

    # ---------- pernas ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 3.0 * lado; zc = 4.6
        pp = []
        mperna = g.mat_cor(lambda p, f: mix(PERNA_ESC, PERNA, clamp((p[1] - 1.0) / 7.0)), borda=.08, curva=.4)
        pp += g.arredondado("coxa_" + s, [xc - 1.8, 4.6, zc - 1.8], [xc + 1.8, 9.0, zc + 1.8], mperna, r=0.6, faixa=(0, 9.0))
        pp.append(peca("canela_" + s, [xc - 1.15, 1.2, zc - 1.15], [xc + 1.15, 5.4, zc + 1.15], mperna, faixa=(0, 9.0)))
        md = g.mat_cor(lambda p, f: PERNA, borda=.15, curva=.5)
        mg = g.mat_cor(lambda p, f: ROXO_MED, borda=.18, curva=.5)
        for nome, giro, dx in (("meio", 0, 0), ("fora", -24 * lado, 1.6 * lado), ("dentro", 24 * lado, -1.6 * lado)):
            x0, z0 = xc + dx, zc - 0.6
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .85, 0, z0 - 2.6], [x0 + .85, 1.4, z0 + 0.6], md, faixa=(0, 2.0)),
                peca(f"garra_{nome}_{s}", [x0 - .9, 0, z0 - 4.4], [x0 + .9, 1.6, z0 - 2.6], mg, faixa=(0, 2.0))]))
        pp.append(peca("dedo_tras_" + s, [xc - .65, 0, zc + 0.8], [xc + .65, 1.3, zc + 2.8], mg, faixa=(0, 2.0)))
        return osso("perna_" + s, [xc, 9.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

# ---------------- asas de inseto (placas recortadas com nervuras) ----------------
MEMB_RAIZ = (214, 176, 92); MEMB_PONTA = (232, 204, 126); MEMB_CLARA = (250, 234, 168)
VEIA = (255, 232, 110); BORDA_ASA = (255, 238, 140)

def meia_asa(s):
    """Meia largura (fração de W/2) da asa no ponto s (0 = raiz, 1 = ponta)."""
    if s < 0 or s > 1: return 0.0
    if s < 0.6: return math.sqrt(max(0.0, 1 - ((s - 0.6) / 0.63) ** 2))
    return max(0.0, 1 - ((s - 0.6) / 0.4) ** 2) ** 0.6

def mat_asa_inseto(raiz, L, W, semente):
    rx, ry, rz = raiz
    rnd = random.Random(semente)
    passo = 4.6
    sementes = []
    for a in range(int(L / passo) + 2):
        for b in range(-3, 4):
            sementes.append(((a + 0.5 + rnd.uniform(-.3, .3)) * passo, (b + (0.5 if a % 2 else 0) + rnd.uniform(-.2, .2)) * passo * 0.75))
    def f(c):
        x, y, z = c["p"]
        d = abs(x - rx); s = d / L
        t = y - ry
        off = W * 0.08 * s
        hw = meia_asa(s) * W / 2 * (0.82 if t > off else 1.18)     # borda de ataque (de cima) mais reta
        if abs(t - off) > hw: return None
        borda = hw - abs(t - off)
        if c["face"] not in ("north", "south"): return BORDA_ASA
        if borda < 0.6: return BORDA_ASA
        if borda < 0.74: return AMBAR
        if abs(t - off) < 0.1 and s < 0.85: return VEIA          # nervura central
        ds = sorted((d - a) ** 2 + (t - b) ** 2 for a, b in sementes)[:2]
        d1, d2 = math.sqrt(ds[0]), math.sqrt(ds[1])
        if d2 - d1 < 0.3: return VEIA
        base = mix(MEMB_RAIZ, MEMB_PONTA, s)
        return mix(MEMB_CLARA, base, clamp(d1 / 1.0))
    return f

def asa_inseto(nome, raiz, L, W, lado, rot, semente, esp=0.22):
    x, y, z = raiz
    x0, x1 = sorted((x, x + L * lado))
    return osso(nome, list(raiz), list(rot), [
        peca(nome, [x0, y - W * 0.6 - 0.3, z - esp / 2], [x1, y + W * 0.5 + 0.3, z + esp / 2], mat_asa_inseto(raiz, L, W, semente),
             res=5, brilho=True)])

def vibra(a, n=12, fase=0):
    """Batida rápida (keyframes igualmente espaçados; o último igual ao primeiro)."""
    ks = [(0, 0, 0)]
    for k in range(n - 1):
        v = a if (k + fase) % 2 == 0 else -a * 0.5
        ks.append((0, 0, v))
    ks.append((0, 0, 0))
    return ks

ANIM_PARADO = {
    "asa_inseto_d": vibra(-12), "asa_inseto_e": vibra(12),
    "asa_inseto2_d": vibra(-10, fase=1), "asa_inseto2_e": vibra(10, fase=1),
}
ANIM_ANDANDO = {
    "asa_inseto_d": vibra(-16, n=6), "asa_inseto_e": vibra(16, n=6),
    "asa_inseto2_d": vibra(-12, n=6, fase=1), "asa_inseto2_e": vibra(12, n=6, fase=1),
}

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)

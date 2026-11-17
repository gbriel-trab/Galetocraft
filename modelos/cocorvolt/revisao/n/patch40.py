"""Patch da rodada n40 (segunda auditoria): troca blocos inteiros do cocorvolt.py entre marcadores."""
import re
from pathlib import Path
P = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\cocorvolt.py")
s = P.read_text(encoding="utf-8")

def troca(ini, fim, novo):
    """Troca o trecho que começa em 'ini' (inclusive) e vai até 'fim' (exclusive)."""
    global s
    a = s.index(ini); b = s.index(fim, a + len(ini))
    s = s[:a] + novo + s[b:]

def rp(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b)

# ---------- cores ----------
rp("OLHO_BORDA = (20, 96, 236); OLHO_AZUL = (40, 150, 255); OLHO_MIOLO = (232, 252, 255)",
   "OLHO_BORDA = (26, 63, 208); OLHO_AZUL = (47, 107, 255); OLHO_MIOLO = (226, 250, 255)")
rp("BICO = (242, 176, 30); BICO_CLARO = (252, 206, 72); BICO_LADO = (232, 156, 22); BICO_BAIXO = (224, 138, 16)",
   "BICO = (242, 181, 28); BICO_CLARO = (252, 204, 70); BICO_LADO = (236, 160, 24); BICO_BAIXO = (224, 138, 20)")
rp("VERMELHO = (212, 32, 32); VERMELHO_CLARO = (230, 52, 44); VERMELHO_ESC = (176, 26, 28)",
   "VERMELHO = (212, 42, 36); VERMELHO_CLARO = (226, 56, 46); VERMELHO_ESC = (156, 26, 24)")
rp("AMARELO_P = (252, 186, 24); ESCAMA = (222, 146, 14)", "AMARELO_P = (240, 184, 32); ESCAMA = (220, 156, 26)")

# ---------- olho: fenda estreita, inclinada para o bico, azul elétrico com miolo branco-ciano ----------
troca("def olho_volt(u, v):", "def mat_faceta(lado):", '''def olho_volt(u, v):
    """Olho eletrificado: fenda estreita, com a borda de cima descendo para o bico (u negativo = bico); borda azul
    elétrica, azul saturado e miolo branco-ciano brilhante (a ficha mostra o miolo quase branco), órbita carvão."""
    W2, H0, H1 = 1.35, -0.38, 0.42
    topo = H1 - 0.34 * (1 - u / W2) * 0.5
    if abs(u) > W2 + 0.25 or v < H0 - 0.25 or v > topo + 0.5: return None
    if abs(u) > W2 or v < H0 or v > topo:
        return (44, 46, 54) if v > H0 - 0.05 else (96, 96, 104)
    du, dv = (W2 - abs(u)) / W2, min(v - H0, topo - v) / (topo - H0)
    d = min(du * 2.2, dv * 2.4)
    if d < 0.3: return OLHO_BORDA
    if d < 0.62: return OLHO_AZUL
    return OLHO_MIOLO

''')

# ---------- bico, barbela, bochechas, nuca ----------
troca("    # bico: trap", "    return cab\n", '''    # bico: cunha LARGA e curta (~1/3 da cabeça de largura e de projeção), topo reto com narina, gancho na ponta
    i_bico = len(g.PECAS)
    mb = mat_luz(cor_bico, borda=.04, curva=.15)
    fb = (26.6, 30.2)
    zb = CAB_Z0 + 0.3
    cab.append(peca("bico_base", [-1.35, 28.1, zb - 1.6], [1.35, 30.0, zb], mb, faixa=fb, res=4))
    cab.append(peca("bico_meio", [-1.1, 28.0, zb - 2.6], [1.1, 29.75, zb - 1.5], mb, faixa=fb, res=4))
    cab.append(peca("bico_gancho", [-0.75, 27.0, zb - 3.2], [0.75, 29.4, zb - 2.45], mb, rot=(-14, 0, 0),
                    pivo=(0, 29.4, zb - 2.45), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-0.95, 27.55, zb - 2.0], [0.95, 28.15, zb], mat_bloco(BICO_BAIXO, topo=0), res=4))
    # barbela: 2 lóbulos estreitos e juntos, logo abaixo do bico (o da esquerda de quem olha mais comprido)
    mbar = mat_luz(lambda p, f: mix(VERMELHO_ESC, VERMELHO, clamp((p[1] - 22.4) / 3.6)), borda=.06, curva=.15)
    zw = zb - 0.9
    for lado, y_fim in ((-1, 23.0), (1, 23.8)):
        x0, x1 = sorted((0.05 * lado, 1.05 * lado))
        cab += arredondado("barbela_" + ("d" if lado < 0 else "e"), [x0, y_fim, zw - 0.65], [x1, 27.7, zw + 0.6], mbar,
                           r=0.3, res=4)
    g.transformar(i_bico, [], (0, 0, 0), k=1.0, sobe=BICO_DY)   # bico e barbela descem: o alto do bico na base do olho
    # penas GRANDES da bochecha (juba): 3 por lado, em telha, apontando para fora e para baixo; cabeça mais larga embaixo
    JUBA = [  # (y, z, comprimento, largura, abertura, giro, cor)
        (31.0, -1.6, 5.0, 3.4, 30, 30, (196, 196, 200)), (28.8, -0.8, 5.6, 3.6, 38, 26, (196, 196, 200)),
        (26.6, 0.2, 5.4, 3.4, 46, 20, (138, 138, 144))]
    for k, (y, z, L, W, fl, giro, cor) in enumerate(JUBA):
        for lado in (-1, 1):
            s = "d" if lado < 0 else "e"
            cab.append(osso(f"juba{k}_{s}", [(CAB_X - 0.5) * lado, y, z], [0, giro * lado, fl * lado], [
                pena_degrau(f"juba{k}_{s}_p", ((CAB_X - 0.5) * lado, y, z), (-14, 0, 0), L, W, 1.4, mat_tufo(cor),
                            dir="baixo", passos=(0.5, 0.3, 0.2), largura=(1.0, 0.62, 0.26), res=4)]))
    # atrás da cabeça: 2 camadas de penas pontudas descendo até a capa
    for k, (x, y, L, cor) in enumerate([(-1.7, 31.0, 6.0, (150, 150, 156)), (1.7, 31.0, 6.0, (150, 150, 156)),
                                        (0.0, 28.4, 6.4, (138, 138, 144)), (-2.9, 28.0, 5.4, (124, 124, 130)),
                                        (2.9, 28.0, 5.4, (124, 124, 130))]):
        raiz = (x, y, CAB_Z1 - 0.2 + 0.2 * k)
        cab.append(osso(f"nuca{k}", list(raiz), [-22, 0, 8 * x / 2.9], [osso(f"nuca{k}_g", list(raiz), [0, 90, 0], [
            pena_degrau(f"nuca{k}_p", raiz, (0, 0, 0), L, 3.2, 1.3, mat_tufo(cor), dir="baixo", passos=(0.5, 0.3, 0.2),
                        largura=(1.0, 0.62, 0.26), res=4)])]))
''')

# ---------- chapéu: cone mais alto e carvão frio, raios separados, aba grossa com tábuas ----------
troca("CH_APICE, CH_ABA, CH_R", "def mat_talisma(cx, cy, W, H):", '''CH_APICE, CH_ABA, CH_R, CH_Z, CH_N, CH_T = 39.5, 33.4, 11.6, 0.8, 16, 1.5
CH_INCL = -8                                          # a aba desce na frente
CH_ALFA = math.atan2(CH_APICE - CH_ABA, CH_R)
CH_S = math.hypot(CH_APICE - CH_ABA, CH_R)
CH_FAIXA = 0.74 * CH_S                                # daqui para fora, a aba de palha bege
CARVAO_FRIO = (69, 70, 76)
# 5 rachaduras de raio separadas, em coordenadas (ângulo em voltas, s/CH_S): cantos vivos, terminam em ponta
RACHAS = [[(0.02, 0.20), (0.06, 0.34), (0.03, 0.40), (0.08, 0.58)],
          [(0.19, 0.30), (0.24, 0.36), (0.22, 0.48), (0.28, 0.52), (0.26, 0.66)],
          [(0.40, 0.18), (0.43, 0.32), (0.39, 0.42), (0.45, 0.60)],
          [(0.58, 0.34), (0.63, 0.40), (0.61, 0.50), (0.67, 0.56), (0.66, 0.68)],
          [(0.79, 0.22), (0.82, 0.36), (0.78, 0.44), (0.84, 0.62)]]

def mat_chapeu(k):
    """Cone carvão-frio com nervuras de palha, 5 rachaduras de raio separadas (cantos vivos, brilham), aba bege
    grossa com tábuas."""
    yaw = 2 * math.pi * k / CH_N
    tg = math.tan(math.pi / CH_N)
    def meia(s): return s * math.cos(CH_ALFA) * tg + 0.06
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        s = CH_Z - z                                       # distância do ápice pela geratriz
        if face in ("up", "down") and abs(x) > meia(s): return None
        if face in ("east", "west"): return None           # as emendas ficam cobertas pelo gomo vizinho
        if face == "down": return tomf(mix(PALHA_ESC, PALHA, clamp(s / CH_S)), -0.1)
        if face == "north":                                # beirada GROSSA da aba, com tábuas
            return (201, 164, 99) if c["i"] % 6 == 0 else tomf(PALHA_CLARA, -0.08 if c["j"] in (0, c["th"] - 1) else 0.06)
        if face == "south": return PALHA_CLARA
        borda_lado = meia(s) - abs(x)
        if s > CH_FAIXA:                                   # aba de palha: tábuas com emendas
            cor = PALHA_CLARA if s > CH_FAIXA + 0.35 else PALHA_ESC
            if borda_lado < 0.14 or abs(x) < 0.08: cor = (201, 164, 99)
            return cor
        if s < 0.9: return PALHA_CLARA
        volta = (yaw + math.atan2(x, max(s * math.cos(CH_ALFA), 1e-6))) / (2 * math.pi)
        circ = 2 * math.pi * s * math.cos(CH_ALFA)         # para medir a distância em unidades
        for pts in RACHAS:
            q = [(((a - volta + 0.5) % 1.0 - 0.5) * circ, b * CH_S) for a, b in pts]
            d = dist_polilinha(0.0, s, q)
            if d < 0.36:
                ponta = math.hypot(q[-1][0], s - q[-1][1]) < 1.2 or math.hypot(q[0][0], s - q[0][1]) < 1.0
                if not ponta or d < 0.2: return RAIO_F if d > 0.1 else RAIO_BORDA
            if d < 0.62: return (150, 120, 60)             # brilho em volta da rachadura
        cor = CARVAO_FRIO
        if borda_lado < 0.14: cor = (104, 92, 78)          # nervura de palha entre os painéis
        return cor
    return f

''')
rp("        r = glifo_raio(u / 0.6, v / 0.66)\n        if r: return r\n        return (34, 36, 46)",
   "        r = glifo_raio(u / 0.78, v / 0.78)\n        if r: return r\n        return (34, 36, 46)")
rp('''    filhos.append(peca("chapeu_ponta", [-0.8, CH_APICE - 0.5, CH_Z - 0.8], [0.8, CH_APICE + 0.35, CH_Z + 0.8],''',
   '''    filhos.append(peca("chapeu_ponta", [-1.0, CH_APICE - 0.9, CH_Z - 1.0], [1.0, CH_APICE + 0.5, CH_Z + 1.0],''')
rp('''        x = 9.8 * lado
        aba = CH_ABA + (CH_APICE - CH_ABA) * (1 - 9.8 / CH_R) - CH_T / math.cos(CH_ALFA)''',
   '''        x = 9.6 * lado
        aba = CH_ABA + (CH_APICE - CH_ABA) * (1 - 9.6 / CH_R) - CH_T / math.cos(CH_ALFA)''')
rp('''            peca("talisma_" + s, [x - W / 2, cy - H / 2, CH_Z - 0.35], [x + W / 2, cy + H / 2, CH_Z + 0.35],''',
   '''            peca("talisma_" + s, [x - W / 2, cy - H / 2, CH_Z - 0.25], [x + W / 2, cy + H / 2, CH_Z + 0.25],''')

# ---------- gola larga com debrum de ouro ----------
rp('''        if d < 0.95: return CINZA_ESC                    # gola larga
        if d < 1.2: return OURO                          # fio de ouro da lapela''',
   '''        if d < 1.25: return CINZA_ESC                    # gola larga (~2 px)
        if d < 1.6: return OURO                          # debrum de ouro da lapela''')

# ---------- avental: um raio angular de verdade (ϟ), grosso em cima e afinando até a ponta ----------
troca("PAINEL_RAIO = ", "def cor_cinto(p, face):", '''def cor_painel(p, face):
    """Painel único do traje: navy com moldura de ouro e UM raio angular (ϟ, 2 dobras, cantos vivos), grosso em cima
    e terminando em ponta fina embaixo, ~60% da largura do painel; amarelo saturado com borda clara, brilha."""
    x, y, z = p
    if face != "north": return OURO
    u, v = x / 2.4, (y - 11.6) / 4.3
    if abs(u) > 0.82 or v > 0.96 or v < -0.97: return OURO
    if no_poligono(u / 0.62, v / 0.86, RAIO_POL):
        return RAIO_F if no_poligono(u / 0.62 * 1.18 + 0.02, v / 0.86 * 1.06, RAIO_POL) else RAIO_BORDA
    return navy_blocos(x, y, z, (30, 44, 96))

''')

# ---------- ombreira sólida ----------
troca("Z_GLIFO = ", "# ---------------- montagem", '''ZIGUES_OMB = [[(-0.62, 0.42), (-0.3, 0.42), (-0.42, -0.02), (-0.1, -0.02)],
              [(0.08, 0.06), (0.4, 0.06), (0.28, -0.38), (0.62, -0.38)]]

def mat_ombreira_solida(lado, parte):
    """Placa de armadura cheia: fundo azul-marinho quase preto (#1e2440), borda de ouro GROSSA em toda face e, na face
    de fora da placa principal, dois zigue-zagues de ouro de 3 segmentos (sem formato de letra)."""
    fora = "east" if lado > 0 else "west"
    FUNDO = (30, 36, 64)
    def f(c):
        face = c["face"]
        if face == "down": return tomf(FUNDO, -0.3)
        i, j, tw, th = c["i"], c["j"], c["tw"], c["th"]
        b = min(i, tw - 1 - i, j, th - 1 - j) / 4.0
        friso = 0.5 if min(tw, th) > 8 else 0.3
        if b < 0.1: return OURO_ESC
        if b < friso: return tomf(OURO, 0.1 if face == "up" else 0.0)
        if parte == "placa" and face == fora:
            x, y, z = c["p"]
            (x0, y0, z0), (x1, y1, z1) = c["b"]
            u = (z - (z0 + z1) / 2) / ((z1 - z0) / 2) * (-1 if lado > 0 else 1)
            v = ((y - y0) / (y1 - y0)) * 2 - 1
            if any(dist_polilinha(u, v, zz) < 0.09 for zz in ZIGUES_OMB): return OURO_CLARO
        return tomf(FUNDO, 0.15 if face == "up" else 0.0)
    return f

''')

# ---------- montagem: saia de penas, ombreiras, asas, capa de penas, cauda ----------
troca("    # penas escuras saindo de baixo", "    corpo.append(pescoco)", '''    # saia de penas cinza serrilhadas sob a túnica (dos lados e atrás; na frente fica o avental)
    for k in range(9):
        ang = math.radians(-50 + 290 * k / 8)
        x, z = 4.4 * math.cos(ang), 0.4 + 3.8 * math.sin(ang)
        yaw = -math.degrees(ang) + 90
        cor = (122, 122, 128) if k % 2 else (96, 96, 104)
        corpo.append(osso(f"saiote{k}", [x, 10.6, z], [0, yaw, 0], [
            pena_degrau(f"saiote{k}_p", (x, 10.6, z), (0, 0, 0), 4.2, 3.0, 1.1, mat_bloco(cor), dir="baixo",
                        passos=(0.5, 0.3, 0.2), largura=(1.0, 0.6, 0.25), espessura=(1.0, 0.85, 0.7))]))

    # ombreiras: placa de armadura CHEIA encostada no tronco, topo inclinado ~15° para fora, e um degrau mais baixo
    # cobrindo o braço (as duas peças se tocam; nada flutua)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((3.4 * lado, 8.0 * lado))
        placa = peca("ombreira_" + s, [x0, 19.2, -3.5], [x1, 23.6, 3.9], mat_ombreira_solida(lado, "placa"), res=4)
        xb0, xb1 = sorted((6.2 * lado, 8.7 * lado))
        degrau = peca("ombreira_braco_" + s, [xb0, 16.4, -3.2], [xb1, 20.2, 3.6], mat_ombreira_solida(lado, "degrau"), res=4)
        corpo.append(osso("ombro_" + s, [3.4 * lado, 23.6, 0.2], [0, 0, -15 * lado], [
            placa, osso("ombro_braco_" + s, [6.6 * lado, 20.2, 0.2], [0, 0, 10 * lado], [degrau])]))

    # asas: MANGAS de pena largas, quase verticais, encostadas na lateral da túnica: 3 camadas de telhas, cada uma
    # com 4 penas pontudas (serrilhado), viradas para a frente e para fora; claras em cima, médias embaixo
    CAMADAS = [(21.0, 6.4, (180, 180, 184)), (17.2, 6.6, (150, 150, 156)), (13.2, 6.8, (122, 122, 128))]
    TELHAS = [(4.95, -2.6), (5.9, -0.9), (6.75, 0.8), (7.35, 2.5)]
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        for r, (yr, L, cor) in enumerate(CAMADAS):
            for k, (x, z) in enumerate(TELHAS):
                x_ = (x + 0.15 * r) * lado
                asa.append(osso(f"asa{r}{k}_{s}", [x_, yr, z], [0, 28 * lado, (4 + 2 * r) * lado], [
                    pena_degrau(f"asa{r}{k}_{s}_p", (x_, yr, z), (0, 0, 0), L - 0.4 * (k % 2), 2.9, 1.4,
                                mat_degraus(cor, (0.0, 0.08, 0.16)), dir="baixo", passos=(0.56, 0.28, 0.16),
                                largura=(1.0, 0.6, 0.25))]))
        corpo.append(osso("asa_" + s, [5.0 * lado, 21.0, 0.2], [0, 0, 0], asa))

    # capa de penas das costas (dos dois lados da cauda), abaixo da capa navy
    for r, (y, L, cor) in enumerate([(17.8, 5.6, (180, 180, 184)), (13.6, 5.8, (150, 150, 156))]):
        for k, x in enumerate((-4.4, -2.3, 2.3, 4.4)):
            raiz = (x, y, TORSO_Z1 + 0.2 + 0.3 * r)
            corpo.append(osso(f"capa{r}{k}", list(raiz), [-8, 0, 6 * x / 4.4], [osso(f"capa{r}{k}_g", list(raiz), [0, 90, 0], [
                pena_degrau(f"capa{r}{k}_p", raiz, (0, 0, 0), L, 2.8, 1.2, mat_degraus(cor, (0.0, 0.08, 0.16)), dir="baixo",
                            passos=(0.56, 0.28, 0.16), largura=(1.0, 0.6, 0.25))])]))

    # cauda: leque CURVO de penas largas que afinam em lâmina, sobrepostas sem vão, da altura do joelho até perto
    # dos olhos; um tom por pena, carvão e cinza-claro alternados; rachadura de raio grossa em cada pena carvão
    cauda = []
    n = N_CAUDA
    for k in range(n):
        t = k / (n - 1)
        ang = 40 - 78 * t
        y = 18.0 - 4.2 * t
        L = [13.5, 15.0, 16.0, 16.5, 16.5, 15.5, 14.0, 12.0][k]
        x = 0.35 if k % 2 else -0.35
        escura = k % 2 == 0
        cor = (58, 58, 62) if escura else (168, 168, 172)
        cauda.append(pena_cauda(f"cauda{k}", (x, y, TORSO_Z1 - 0.8), (-ang, 3 * (1 if x > 0 else -1), 0), L, cor,
                                raio=escura))
    corpo.append(osso("cauda", [0, 16.0, TORSO_Z1 - 0.8], [0, 0, 0], cauda))

''')

# ---------- pés: só as garras escuras, dedos amarelos tocam o chão ----------
rp('''                peca(f"garra_{nome}_{s}", [x0 - .8, 0, z0 - 3.6], [x0 + .8, 2.1, z0 - 2.35], mg)]))''',
   '''                peca(f"garra_{nome}_{s}", [x0 - .5, 0.0, z0 - 3.3], [x0 + .5, 1.1, z0 - 2.3], mg, rot=(14, 0, 0),
                     pivo=(x0, 1.1, z0 - 2.3))]))''')
rp('''        pp.append(peca("garra_tras_" + s, [xc - .7, 0, zc + 2.9], [xc + .7, 1.3, zc + 4.0], mg))''',
   '''        pp.append(peca("garra_tras_" + s, [xc - .45, 0, zc + 2.9], [xc + .45, 0.9, zc + 3.8], mg))''')

# ---------- penas da cauda em lâmina ----------
troca("ZIGUE_CAUDA = ", 'if __name__ == "__main__":', '''RACHA_CAUDA = [(0.18, 1.3), (0.4, 1.0), (0.36, 2.0), (0.6, 1.7), (0.56, 2.5), (0.74, 2.2)]   # (fração, fundo)

def mat_pena_cauda(cor, z0, Lt, topo, raio):
    """Pena da cauda de UM tom (face de cima um pouco mais clara, fio escuro na borda); nas penas carvão, uma
    rachadura de raio grossa e brilhante, com cantos vivos."""
    pts = [(z0 + f * Lt, topo - d) for f, d in RACHA_CAUDA]
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        if face == "up": return tomf(cor, 0.16)
        if face == "down": return tomf(cor, -0.3)
        if face in ("east", "west"):
            if raio:
                d = dist_polilinha(z, y, pts)
                if d < 0.3: return RAIO_F if d > 0.1 else RAIO_BORDA
            if g.na_borda(c): return tomf(cor, -0.18)
            return cor
        return tomf(cor, -0.12)
    return f

def pena_cauda(nome, base, rot0, Lt, cor, raio=False):
    """Pena da cauda em LÂMINA: 3 segmentos (ossos nome_0..2) que afinam em altura e espessura (4,2 -> 3 -> 1,8) até a
    ponta e CURVAM PARA CIMA 6° por segmento; o eixo de cada segmento fica no meio da altura (sem degrau solto)."""
    x, y, z0 = base
    H = [4.2, 3.0, 1.8]; F = [0.44, 0.33, 0.23]; W = [2.4, 2.0, 1.5]
    topo = y + H[0] / 2
    m = mat_pena_cauda(cor, z0, Lt, topo, raio)
    def seg(k, pz):
        L = F[k] * Lt
        meio = y + (H[0] - H[k]) * 0.25                  # afina mais por baixo: a lâmina sobe um pouco
        filhos = [peca(f"{nome}_{k}", [x - W[k] / 2, meio - H[k] / 2, pz], [x + W[k] / 2, meio + H[k] / 2, pz + L], m, res=4,
                       brilho=brilha if raio else False)]
        if k + 1 < 3: filhos.append(seg(k + 1, pz + L - 0.3))
        return osso(f"{nome}_{k}", [x, y, pz], list(rot0) if k == 0 else [-6, 0, 0], filhos)
    return seg(0, z0)

''')
P.write_text(s, encoding="utf-8")
print("ok")

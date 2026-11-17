"""Patch da rodada n38 (auditoria da n37): aplica as mudanças em ferramentas/especies/axococo.py."""
from pathlib import Path
p = Path(__file__).resolve().parents[3] / "ferramentas" / "especies" / "axococo.py"
s = p.read_text(encoding="utf-8")

def rep(a, b):
    global s
    assert a in s, a[:90]
    s = s.replace(a, b)

def bloco_entre(ini, fim, novo):
    global s
    a = s.index(ini); b = s.index(fim, a)
    s = s[:a] + novo + s[b:]

# ---------- paleta ----------
rep('''GUELRA_MAG = (230, 58, 109)''', '''GUELRA_MAG = (230, 58, 109)
GUELRA_MIOLO = (251, 150, 174)   # miolo da brânquia (detalhe "Brânquias": (250,135,162)/(251,152,174))
GUELRA_BAIXO = (251, 106, 137)   # lado de baixo da haste
GUELRA_PONTA = (226, 35, 81)     # dentes e ponta (226,35,81)
ROSA_MEDIO = (248, 150, 190)     # rêmiges e beirada de baixo da asa (detalhe "Plumagem Úmida": (250,157,202))''')
rep('''ESPIRAL = (52, 108, 196)
ESPIRAL_CLARO = (80, 132, 214)''', '''ESPIRAL = (44, 113, 202)         # detalhe "Plumagem Úmida": (44,113,202)/(58,131,228)
ESPIRAL_CLARO = (58, 131, 228)
CAUDA_BASE = (24, 64, 160)       # base e borda interna das lâminas
CAUDA_MEIO = (46, 112, 200)
CAUDA_PONTA = (90, 176, 240)''')
rep('''AMARELO = (250, 172, 2)          # bico (249,173,0) / perna (247,152,4)
AMARELO_CLARO = (252, 192, 40)
LARANJA = (213, 136, 29)         # sombra do bico''', '''AMARELO = (251, 172, 3)          # bico (251,172,3) / pé (249,159,2)-(252,177,6)
AMARELO_CLARO = (253, 201, 42)   # alto do bico
LARANJA = (225, 132, 1)          # sombra do bico e da perna''')
rep('''ROXO = (71, 53, 77)              # dedos
ROXO_CLARO = (104, 81, 103)''', '''ROXO = (90, 68, 103)             # dedos (detalhe "Patas Anfíbias": (90,68,103)/(101,77,114))
ROXO_CLARO = (101, 77, 114)''')
rep('''CREME = (252, 222, 206)''', '''CREME = (250, 226, 212)''')
rep('''MAGENTA_ESC = (188, 16, 61)''', '''MAGENTA_ESC = (188, 16, 61)
CRISTA_TOPO = (240, 64, 108)     # topos da crista, um tom mais claro''')
rep('''IRIS = (204, 150, 30)''', '''IRIS = (232, 160, 32)
OLHO_AZUL = (53, 139, 225)       # moldura do olho (53,139,225)''')

# ---------- bochecha ----------
rep('''    if y < 24.7 and z < -6.8: return ROSA_PALIDO if y > 22.2 else CREME''',
    '''    if y < 25.0 and z < -6.8: return ROSA_PALIDO if y > 22.2 else CREME''')

# ---------- olho ----------
bloco_entre('def olho(u, v):', 'def mat_faceta_olho', '''def olho(u, v):
    """Olho neutro da ficha, em blocos (u ao longo da face, negativo = para o bico; v para cima):
    - branco puro, quase retangular, cortado em cima pela pálpebra (linha reta que desce para o bico);
    - pupila preta GRANDE e oval na vertical, encostada na borda do lado do bico, com 1 px de brilho no alto;
    - íris âmbar só como meia-lua na fileira embaixo da pupila;
    - moldura azul retangular: fina em cima e na frente, grossa atrás e embaixo."""
    u0, u1, v0, v1 = -2.3, 2.1, -1.5, 1.5                  # o branco do olho
    lid = 0.95 + 0.28 * u                                  # linha da pálpebra
    if v >= lid: return None
    if u0 <= u < u1 and v0 <= v < v1:
        if -2.3 <= u < -1.05 and -1.1 <= v < 1.0:              # pupila: 1,25 x 2,1, encostada no lado do bico
            if -1.65 <= u < -1.3 and 0.45 <= v < 0.8: return (255, 255, 255)
            if (u < -2.1 or u >= -1.25) and (v < -0.9 or v >= 0.8): return (255, 255, 255)   # quinas arredondadas
            return PRETO
        if -2.3 <= u < -1.05 and -1.5 <= v < -1.1: return IRIS
        return (255, 255, 255)
    if u0 - 0.3 <= u < u1 + 0.9 and v0 - 0.8 <= v < v1 + 0.4: return OLHO_AZUL
    return None

''')
rep('''            r = olho(z - cz + 0.55, y - OLHO_Y)      # olho encostado na quina do bico, como na ficha''',
    '''            r = olho(z - cz + 0.75, y - OLHO_Y)      # olho encostado na quina do bico, como na ficha''')

# ---------- sobrancelha rente ----------
rep('''            x0, x1 = sorted((xf - 0.3 * lado, xf + 0.5 * lado))
            yb = OLHO_Y + 0.85 + 0.35
            sob = caixa(f"sobrancelha_{'d' if lado < 0 else 'e'}", [x0, yb - 0.3, pcz - L / 2 + 0.1], [x1, yb + 2.0, pcz + L / 2 - 0.1],
                        mat_bloco(lambda p, f: ROSA_PALIDO if f == "up" else ROSA_CLARO, borda=.06, alto=.06, fundo=-.4),
                        rot=(-15, 0, 0), pivo=(xf, yb, pcz), res=4)''',
    '''            x0, x1 = sorted((xf - 0.3 * lado, xf + 0.4 * lado))
            yb = OLHO_Y + 0.95 + 0.25
            sob = caixa(f"sobrancelha_{'d' if lado < 0 else 'e'}", [x0, yb - 0.25, pcz - 2.9], [x1, yb + 1.8, pcz + 2.3],
                        mat_bloco(lambda p, f: ROSA_MEDIO if f == "down" else ROSA_CLARO, borda=.0, alto=.0, fundo=-.12),
                        rot=(-15.6, 0, 0), pivo=(xf, yb, pcz), res=4)''')

# ---------- bico ----------
rep('''    if y < 23.4: return mix(AMARELO, LARANJA, .5)
    return AMARELO''', '''    if face == "down": return LARANJA
    return AMARELO''')
rep('''abs(z - (CAB_ZF - 2.2)) < 0.26 and abs(y - 25.8) < 0.26''', '''abs(z - (CAB_ZF - 2.6)) < 0.3 and abs(y - 25.7) < 0.3''')
rep('''    cab.append(caixa("bico_cima", [-2.5, 24.8, CAB_ZF - 4.6], [2.5, 26.5, CAB_ZF + 0.4], mb))
    cab.append(caixa("bico_meio", [-2.2, 23.4, CAB_ZF - 3.6], [2.2, 24.9, CAB_ZF + 0.4], mb))
    cab.append(caixa("bico_baixo", [-1.3, 22.3, CAB_ZF - 2.4], [1.3, 23.5, CAB_ZF + 0.4], mb))''',
    '''    # cunha simples: de lado, maxila reta com uma só quebra para a ponta quadrada; de frente, trapézio largo em
    # cima (~1/3 da cabeça) que afina embaixo e para logo acima das barbelas
    cab.append(caixa("bico_cima", [-2.5, 24.4, CAB_ZF - 3.4], [2.5, 26.4, CAB_ZF + 0.4], mb))
    cab.append(caixa("bico_baixo", [-1.8, 22.7, CAB_ZF - 3.0], [1.8, 24.5, CAB_ZF + 0.4], mb))
    cab.append(caixa("bico_ponta", [-2.1, 23.5, CAB_ZF - 4.9], [2.1, 26.2, CAB_ZF - 3.3], mb))''')

# ---------- barbela mais curta ----------
rep('''lob = [caixa("barbela_" + s_, [x0, 18.6, CAB_ZF - 2.4], [x1, 22.6, CAB_ZF + 0.8], mbar)]''',
    '''lob = [caixa("barbela_" + s_, [x0, 19.4, CAB_ZF - 2.4], [x1, 22.8, CAB_ZF + 0.8], mbar)]''')
rep('''lob.append(caixa("barbela_ponta_" + s_, [x0, 17.0, CAB_ZF - 2.0], [x1, 18.8, CAB_ZF + 0.4], mbar))''',
    '''lob.append(caixa("barbela_ponta_" + s_, [x0, 18.2, CAB_ZF - 2.0], [x1, 19.6, CAB_ZF + 0.4], mbar))''')

# ---------- cabeça: alto liso ----------
rep('''    cab += camada_cabeca("testa", 29.6, 31.1, 0.6, CAB_ZT - 0.4, mc)
    cab += camada_cabeca("topo", 31.0, 32.2, 1.8, CAB_ZT - 1.2, mc)''',
    '''    cab += camada_cabeca("testa", 29.6, 31.6, 0.8, CAB_ZT - 0.4, mc)    # alto liso, sem plaquinhas em volta da crista''')

# ---------- crista em moicano ----------
bloco_entre('    # crista aquática: blocos magenta', '    for lado in (-1, 1):\n        s_ = "d" if lado < 0 else "e"\n        for k, (y0, z0, L, rec, ele)', '''    # crista aquática em moicano: coluna central estreita (~1/4 da cabeça) em 4 degraus (o mais alto no meio,
    # a ponta de trás descendo até a nuca) e dois blocos laterais mais baixos (~2/3 da altura)
    mcr = mat_bloco(lambda p, f: CRISTA_TOPO if f == "up" else MAGENTA, borda=.1, alto=.1, fundo=-.16)
    crista = []
    for k, (z0, z1, y1) in enumerate([(-15.0, -12.2, 35.4), (-12.4, -9.4, 38.8), (-9.6, -6.6, 37.6), (-6.8, -4.0, 35.2)]):
        crista.append(caixa(f"crista_{k}", [-1.9, 31.0, z0], [1.9, y1, z1], mcr))
    for lado in (-1, 1):
        x0, x1 = xs(lado, 1.8, 4.2)
        crista.append(caixa("crista_lado_" + ("d" if lado < 0 else "e"), [x0, 31.0, -12.6], [x1, 36.0, -7.6], mcr))
    cab.append(osso("crista", [0, 32, -7.8], [0, 0, 0], crista))
''')

# ---------- brânquias ----------
bloco_entre('def guelra(', 'GUELRAS = [', '''def guelra(nome, raiz, lado, L, recuo, eleva, n_dentes=6):
    """Brânquia de axolote como a 'Brânquias' da ficha: UMA fronde limpa em escada. Haste de miolo rosa-claro
    em 3 degraus que afinam para fora (2,4 -> 1,9 -> 1,4), lado de baixo rosa-choque, dentes de 1 bloco
    alternados em cima e embaixo e ponta rosa-choque. Osso externo sem rotação (é ele que balança na
    animação); o interno dá a direção."""
    x, y, z = raiz
    s = lado
    pcs = []
    def ao_longo(a, b): return sorted((x + a * s, x + b * s))     # ao longo da brânquia, a partir da raiz
    mh = mat_bloco(lambda p, f: GUELRA_BAIXO if f == "down" else GUELRA_MIOLO, borda=.08, alto=.06, fundo=-.06)
    md = mat_bloco(lambda p, f: GUELRA_PONTA, borda=.1, alto=.1, fundo=-.06)
    degraus = [(-1.0, 0.42 * L, 1.2), (0.4 * L, 0.75 * L, 0.95), (0.73 * L, L, 0.7)]
    for k, (a, b, r) in enumerate(degraus):
        x0, x1 = ao_longo(a, b)
        pcs.append(caixa(f"{nome}_haste{k}", [x0, y - r, z - r], [x1, y + r, z + r], mh))
    x0, x1 = ao_longo(L - 0.1, L + 1.3)
    pcs.append(caixa(nome + "_ponta", [x0, y - 0.6, z - 0.6], [x1, y + 0.6, z + 0.6], md))
    passo = 0.8 * L / n_dentes
    for k in range(n_dentes):                      # dentes de 1 bloco, alternados em cima e embaixo
        a = 0.16 * L + passo * k
        r = next(rr for aa, bb, rr in degraus if aa <= a + 0.5 <= bb + 0.01)
        x0, x1 = ao_longo(a, a + min(1.0, passo * 0.8))
        if k % 2 == 0: y0, y1 = y + r - 0.1, y + r + 0.9
        else: y0, y1 = y - r - 0.9, y - r + 0.1
        pcs.append(caixa(f"{nome}_dente{k}", [x0, y0, z - 0.55], [x1, y1, z + 0.55], md))
    dentro = osso(nome + "_dir", list(raiz), [0, -recuo * s, eleva * s], pcs)
    return osso(nome, list(raiz), [0, 0, 0], [dentro])

''')
rep('''    (29.4, -5.4, 13.0, 58, 26),
    (26.0, -5.0, 14.0, 54, -4),
    (22.4, -5.2, 11.5, 58, -26),''', '''    (28.6, -7.4, 11.0, 50, 35),
    (25.8, -7.2, 12.5, 48, 0),
    (23.2, -7.4, 8.5, 50, -22),''')
rep('''cab.append(guelra(f"guelra_{s_}_{k}", (7.4 * lado, y0, z0), lado, L, rec, ele))''',
    '''cab.append(guelra(f"guelra_{s_}_{k}", (7.6 * lado, y0, z0), lado, L, rec, ele))''')

# ---------- cauda em leque aberto ----------
bloco_entre('FOICES = [', 'ONDAS = [', '''FOICES = [  # (x, rx inicial, curva de cada junta, comprimentos, largura da faixa, cor raiz, cor ponta, y da raiz)
    # leque aberto, sem gancho: a de cima nasce a 50° acima da horizontal, sobe acima do dorso (até a altura do
    # olho) e termina na horizontal; as outras nascem a -5°, -28° e -50° com a ponta para trás e para fora.
    # De trás: par de foices escuras nos "ombros" e o meio claro.
    (0.0, 40, (12, 12, 12, 10), (5.4, 5.2, 5.0, 4.6, 4.2), 5.4, CAUDA_BASE, CAUDA_PONTA, 18.6),
    (2.2, 95, (8, 8, 8, 6), (5.6, 5.4, 5.2, 4.8, 4.2), 5.4, CAUDA_BASE, CAUDA_PONTA, 17.0),
    (-2.2, 95, (8, 8, 8, 6), (5.6, 5.4, 5.2, 4.8, 4.2), 5.4, CAUDA_BASE, CAUDA_PONTA, 17.0),
    (1.4, 118, (6, 6, 6), (5.4, 5.2, 4.8, 4.2), 5.2, CAUDA_MEIO, CAUDA_PONTA, 16.0),
    (-1.4, 118, (6, 6, 6), (5.4, 5.2, 4.8, 4.2), 5.2, CAUDA_MEIO, CAUDA_PONTA, 16.0),
    (0.0, 140, (4, 4), (5.2, 4.8, 4.2), 4.8, CAUDA_MEIO, CAUDA_PONTA, 15.0),
]
''')
rep('''        segs = [(L, 4.4 - 0.25 * i, h - 0.3 * i, mix(c0, c1, i / n), mix(c0, c1, (i + 0.6) / n)) for i, L in enumerate(Ls)]''',
    '''        segs = [(L, 3.8 - 0.25 * i, h - 0.45 * i, mix(c0, c1, i / n), mix(c0, c1, (i + 0.6) / n)) for i, L in enumerate(Ls)]''')

# ---------- peito ----------
rep('''    mp = mat_bloco(lambda p, f: CREME, borda=.14, alto=.08, fundo=-.26)     # cada fileira com a beirada de baixo em sombra''',
    '''    mp = mat_bloco(lambda p, f: CREME, borda=.06, alto=.05, fundo=-.12)     # separação sutil entre as fileiras''')
rep('''        if k < len(FILAS) - 1:
            corpo.append(caixa(f"peito_{k}_meio", [-w * 0.42, yb - 0.8, zf - 0.3], [w * 0.42, ya - 0.6, zf + 4.0], mp, res=2))''',
    '''        fundo = 1.4 if k == len(FILAS) - 1 else 0.8           # a última fileira termina em ponta de "V"
        corpo.append(caixa(f"peito_{k}_meio", [-w * 0.42, yb - fundo, zf - 0.3], [w * 0.42, ya - 0.6, zf + 4.0], mp, res=2))''')

# ---------- asa em gota ----------
bloco_entre('    # ================= asas:', '    # ================= cauda:', '''    # ================= asas em gota, com a espiral quadrada =================
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        fora = "east" if lado > 0 else "west"
        def cor_asa(p, face, fora=fora):
            x, y, z = p
            if face == fora and espiral(-(z - 1.5), y - 16.2): return ESPIRAL if y < 15.0 else ESPIRAL_CLARO
            if face == "north" and abs(x) > 10.2 and 10.6 < y < 12.2: return ESPIRAL      # a ponta da espiral vista de frente
            return ROSA_CLARO
        ma = mat_bloco(cor_asa, borda=.08, alto=.14, fundo=-.12)     # cada fileira com a beirada de cima clara
        mr = mat_bloco(lambda p, f: ROSA_MEDIO, borda=.1, alto=.14, fundo=-.14)
        asa = []
        def bloco(nome, xa, xb, y0, y1, z0, z1, m=ma):
            x0, x1 = xs(lado, xa, xb)
            asa.append(caixa(nome + "_" + s_, [x0, y0, z0], [x1, y1, z1], m, res=4))
        # gota: frente alta e cheia (coberteiras com a espiral), traseira afinando em rêmiges que descem em degrau
        for k, (xb, y0, y1, z0, z1) in enumerate([(11.2, 9.8, 13.0, -6.2, 5.0), (11.8, 12.8, 17.0, -8.0, 6.4),
                                                  (11.4, 16.8, 20.4, -8.2, 5.0), (10.4, 20.2, 21.0, -7.0, -1.0)]):
            bloco(f"asa{k}", 7.2, xb, y0, y1, z0, z1)
        for k, (y0, y1, z0, z1, xb) in enumerate([(15.6, 19.4, 3.0, 10.6, 10.6), (13.2, 17.0, 5.0, 12.6, 10.3),
                                                  (10.8, 14.4, 5.0, 14.2, 10.0)]):
            bloco(f"asa_remige{k}", 7.4, xb, y0, y1, z0, z1, mr)
        for k, (y0, y1, z0, z1, xb) in enumerate([(8.8, 10.2, -5.4, -1.2, 10.6), (9.2, 10.6, -1.4, 2.8, 10.4),
                                                  (9.8, 11.2, 2.6, 6.4, 10.2)]):
            bloco(f"asa_borda{k}", 7.4, xb, y0, y1, z0, z1, mr)          # fileira de baixo em escada
        corpo.append(osso("asa_" + s_, [8.2 * lado, 19.0, -4.0], [0, 0, 6 * lado], asa))     # abre um pouco embaixo

''')
bloco_entre('def espiral(a, b):', '\ndef montar():', '''def espiral(a, b, k=0.8, meia=0.62):
    """Espiral QUADRADA da 'Plumagem Úmida' (um "e"/"@" em voxel), traço grosso (~1/4 da largura). O rabo
    desce em degraus para a frente até a borda de baixo da asa. a = para a frente (bico), b = para cima."""
    a, b = a / k, b / k
    P = [(0.5, 0.0), (-1.2, 0.0), (-1.2, -2.0), (2.4, -2.0), (2.4, 2.0), (-3.6, 2.0), (-3.6, -4.0), (4.6, -4.0),
         (4.6, -5.2), (7.6, -5.2), (7.6, -6.4), (9.6, -6.4)]
    m = meia / k
    for (a0, b0), (a1, b1) in zip(P, P[1:]):
        if min(a0, a1) - m <= a <= max(a0, a1) + m and min(b0, b1) - m <= b <= max(b0, b1) + m:
            return True
    return False

''')

# ---------- pernas ----------
rep('''        ml = mat_liso(AMARELO, borda=.08)
        pp.append(caixa("perna_" + s, [xc - 2.5, 2.2, zc - 2.5], [xc + 2.5, 9.6, zc + 2.5], ml))   # perna amarela até o corpo''',
    '''        ml = mat_bloco(lambda p, f: LARANJA if f in ("east", "west") else AMARELO, borda=.06, alto=.0, fundo=-.06)
        pp.append(caixa("perna_" + s, [xc - 3.0, 2.2, zc - 3.0], [xc + 3.0, 9.6, zc + 3.0], ml))   # curta e grossa''')
rep('''        mg = mat_bloco(lambda p, f: ROXO_CLARO if f == "up" else ROXO, borda=.16)''',
    '''        mg = mat_bloco(lambda p, f: ROXO_CLARO if f == "up" else ROXO, borda=.1, alto=.0, fundo=.0)''')

p.write_text(s, encoding="utf-8")
print("ok")

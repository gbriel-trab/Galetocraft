from pathlib import Path
p = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\salambrasa.py"); s = p.read_text(encoding="utf-8")
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:160]
    s = s.replace(a, b)

# ---------------- fenda em Y: linha grossa e brilhante ----------------
rep('''        if d < 0.26: return BRASA_MIOLO
        if d < 0.5: return BRASA
        if d < 0.66: return BRASA_BORDA
        return None''', '''        if d < 0.38: return BRASA
        if d < 0.62: return BRASA_BORDA
        return None''')

# ---------------- olho: retângulo arredondado, meio fechado pela sobrancelha ----------------
rep('''OLHO_Y = 27.7''', '''OLHO_Y = 28.3''')
rep('''            o = g.pintar_olho(u + 0.15, y - OLHO_Y, 2.3, 1.85, iris=((170, 40, 8), (232, 84, 14)), esclera=CREME,
                              r_iris=(0.48, 0.66), c_iris=(-0.44, -0.12), r_pup=(0.22, 0.3), bravo=0.32, alto=0.42,''',
'''            o = g.pintar_olho(u + 0.1, y - OLHO_Y, 1.95, 1.6, iris=((150, 30, 14), (216, 64, 28)), esclera=CREME,
                              r_iris=(0.6, 0.82), c_iris=(-0.34, -0.1), r_pup=(0.26, 0.32), bravo=0.3, alto=0.3,''')
rep('''                              contorno=(150, 40, 40))''', '''                              contorno=(192, 48, 24))''')
rep('''    if y < 28.6 and face != "down": return FACE''', '''    if y < 27.0 and face != "down": return FACE''')
# viseira: borda de baixo encostada no topo do olho
rep('''        cab.append(peca("viseira_" + s, [x0, 29.4, -23.0], [x1, 31.6, -15.0], mat_viseira, rot=(-6, 0, 10 * lado),
                        pivo=(5.2 * lado, 31.6, -18.0), res=3))
    cab.append(peca("viseira_meio", [-1.6, 28.7, -22.9], [1.6, 30.6, -16.0], mat_viseira, rot=(-6, 0, 0), pivo=(0, 30.6, -18.0), res=3))''',
'''        cab.append(peca("viseira_" + s, [x0, 28.9, -22.6], [x1, 31.4, -15.0], mat_viseira, rot=(-4, 0, 10 * lado),
                        pivo=(5.2 * lado, 31.4, -18.0), res=3))
    cab.append(peca("viseira_meio", [-1.6, 28.6, -22.5], [1.6, 30.4, -16.0], mat_viseira, rot=(-4, 0, 0), pivo=(0, 30.4, -18.0), res=3))''')
# bico: cunha curta e reta para a frente, na altura do olho, gancho pequeno na ponta, narina
rep('''    cab.append(peca("bico", [-1.7, 26.2, -24.0], [1.7, 28.6, -21.0], mat_bico, rot=(-6, 0, 0), pivo=(0, 28.6, -21.0), res=4))
    cab.append(peca("bico_meio", [-1.15, 24.6, -25.6], [1.15, 27.4, -21.2], mat_bico, rot=(-8, 0, 0), pivo=(0, 27.4, -21.2), res=4))
    cab.append(peca("bico_gancho", [-0.6, 23.0, -26.6], [0.6, 25.4, -24.8], mat_bico, rot=(-14, 0, 0), pivo=(0, 25.4, -24.8), res=4))

    cab.append(peca("bico_baixo", [-0.8, 24.2, -23.2], [0.8, 25.2, -20.8], g.mat_cor(lambda p, f: BICO_ESC, borda=.08), res=4))''',
'''    cab.append(peca("bico", [-1.7, 26.6, -24.8], [1.7, 28.4, -21.0], mat_bico, res=4))            # topo reto
    cab.append(peca("bico_baixo", [-1.0, 25.4, -24.2], [1.0, 26.8, -21.0], mat_bico, res=4))      # de frente afina em V
    cab.append(peca("bico_gancho", [-0.8, 25.4, -25.6], [0.8, 27.8, -24.4], mat_bico, rot=(-18, 0, 0),
                    pivo=(0, 27.8, -24.4), res=4))''')
rep('''def mat_bico(c):
    face = c["face"]; x, y, z = c["p"]''', '''def mat_bico(c):
    face = c["face"]; x, y, z = c["p"]
    if face == "up" and 0.5 < abs(x) < 1.0 and -23.9 < z < -23.2: return (52, 38, 46)    # narina''')
# crista: blocos atarracados inclinados para trás, mais baixa (a cabeça sobe 1), massa para trás da nuca
rep('''        (2.0, 31.0, 35.6, -22.2, -18.8, 2),
        (2.2, 30.8, 38.0, -20.2, -16.4, 6),
        (1.8, 31.0, 39.4, -17.6, -13.8, 6),
        (2.2, 30.6, 36.8, -14.8, -11.2, 12),
        (2.0, 29.8, 34.4, -12.4, -9.2, 22),''', '''        (2.0, 30.8, 34.2, -21.0, -17.6, 14),
        (2.2, 30.8, 36.8, -18.8, -15.0, 18),
        (1.8, 30.8, 39.0, -16.2, -12.4, 20),
        (2.2, 30.4, 36.2, -13.4, -9.8, 24),
        (2.0, 29.6, 33.8, -11.0, -7.8, 30),''')
rep('''        for k, (xa, xb, y0, y1, z0, z1, inc) in enumerate([(1.8, 4.8, 30.9, 34.0, -21.0, -17.0, 4),
                                                           (1.8, 4.2, 30.7, 35.0, -15.4, -11.4, 12)]):''',
'''        for k, (xa, xb, y0, y1, z0, z1, inc) in enumerate([(1.8, 4.8, 30.8, 33.2, -20.2, -16.2, 14),
                                                           (1.8, 4.4, 30.6, 33.8, -14.6, -10.6, 22)]):''')
# lóbulos: blocos pequenos na altura do olho, atrás dele
rep('''        x0, x1 = sorted((4.8 * lado, 6.5 * lado))
        cr.append(bloco_crista("crista_lado_" + s, [x0, 25.6, -16.0], [x1, 30.6, -12.6]))''',
'''        x0, x1 = sorted((4.8 * lado, 6.2 * lado))
        cr.append(bloco_crista("crista_lado_" + s, [x0, 26.6, -15.4], [x1, 29.8, -13.0]))''')
# bochechas: só atrás do olho (sem a da frente, que parecia barbela)
rep('''    for k, (x, y0, z0, L, rx, rz) in enumerate([(4.4, 29.2, -14.2, 6.6, -76, 16), (4.4, 27.2, -15.4, 7.0, -64, 22),
                                                (4.4, 25.4, -13.2, 7.4, -56, 30), (3.8, 25.0, -17.8, 6.2, -30, 20)]):''',
'''    for k, (x, y0, z0, L, rx, rz) in enumerate([(4.4, 29.0, -13.6, 6.4, -70, 14), (4.4, 27.0, -14.6, 6.8, -58, 18),
                                                (4.4, 25.4, -13.0, 7.0, -48, 22)]):''')
rep('''            cores = [(CRISTA, VERM, LARANJA), (VERM, LARANJA_ESC, LARANJA), (LARANJA_ESC, LARANJA, AMARELO),
                     (LARANJA_ESC, LARANJA, AMARELO)][k]
            boch.append(pena_bloco(f"bochecha{k}_{s}", (x * lado, y0, z0), (rx, 0, rz * lado), L, 3.4, cores, esp=1.3))''',
'''            cores = [(CRISTA, VERM, LARANJA), (VERM, LARANJA, AMARELO), (VERM, LARANJA, AMARELO)][k]
            boch.append(pena_bloco(f"bochecha{k}_{s}", (x * lado, y0, z0), (rx, 0, rz * lado), L, 3.0, cores, esp=1.3))''')
# gola: penas pontudas caindo para baixo, só em volta da garganta, até ~1,2x a largura da cabeça
rep('''    C1, C2, C3 = (VERM, LARANJA, AMARELO), (LARANJA_ESC, LARANJA, AMARELO), (LARANJA, AMARELO, AMARELO_CLARO)
    JUBA = [  # (x, y, z, phi, abertura, varrida, comprimento, largura, cores) do lado esquerdo (+x); o direito é espelho
        (2.8, 24.2, -19.8, -90, 6, 34, 6.4, 3.4, C1),       # 'babador' de frente, abrindo para os lados
        (4.2, 25.2, -16.6, -30, 24, 34, 9.0, 3.8, C1),      # leque dos lados e de trás, varrendo para trás
        (4.6, 25.4, -13.6, 10, 26, 46, 10.0, 4.0, C1),
        (3.8, 25.6, -10.6, 55, 24, 58, 9.6, 3.8, C2),
        (4.6, 22.6, -14.4, -5, 30, 34, 8.6, 3.8, C2),
        (4.4, 22.4, -11.0, 35, 28, 46, 8.8, 3.8, C3),
        (3.6, 22.0, -8.8, 70, 24, 54, 8.0, 3.4, C3),
    ]''', '''    C1 = (VERM, LARANJA, AMARELO)                      # degradê da ficha: vermelho na raiz -> laranja -> amarelo
    JUBA = [  # (x, y, z, phi, abertura, varrida, comprimento, largura, cores) do lado esquerdo (+x); o direito é espelho
        (2.4, 24.4, -19.8, -70, 10, 14, 7.0, 3.0, C1),      # frente da garganta, dos lados do bico
        (3.8, 24.6, -17.8, -35, 12, 18, 7.8, 3.2, C1),
        (4.4, 24.8, -15.4, 0, 12, 22, 8.2, 3.4, C1),        # lados
        (4.0, 25.0, -13.0, 35, 12, 26, 7.8, 3.2, C1),       # atrás da cabeça
        (3.2, 22.4, -18.8, -50, 10, 12, 6.6, 3.0, C1),      # 2ª camada, mais baixa
        (4.2, 22.4, -16.2, -10, 12, 16, 7.0, 3.2, C1),
    ]''')
rep('''                                  varre=var, esp=1.4))
    juba.append(pena_cone("juba_nuca", (0, 25.4, -9.6), 90, 0, 9.0, 4.0, 1, C2, varre=50, esp=1.8))''',
'''                                  varre=var, esp=1.4))''')
# cabeça (e gola) mais alta e mais à frente: pescoço mais longo
rep('''def deslocar(desde, nos, dz):''', '''def deslocar(desde, nos, dz, dy=0.0):''')
rep('''    def volta(c):
        c = dict(c); x, y, z = c["p"]; c["p"] = (x, y, z - dz)
        b0, b1 = c["b"]; c["b"] = ([b0[0], b0[1], b0[2] - dz], [b1[0], b1[1], b1[2] - dz])
        return c
    for pc in g.PECAS[desde:]:
        for arr in (pc.de, pc.ate, pc.pivo): arr[2] += dz''', '''    def volta(c):
        c = dict(c); x, y, z = c["p"]; c["p"] = (x, y - dy, z - dz)
        b0, b1 = c["b"]; c["b"] = ([b0[0], b0[1] - dy, b0[2] - dz], [b1[0], b1[1] - dy, b1[2] - dz])
        return c
    for pc in g.PECAS[desde:]:
        for arr in (pc.de, pc.ate, pc.pivo): arr[2] += dz; arr[1] += dy''')
rep('''            no["origin"][2] += dz''', '''            no["origin"][2] += dz; no["origin"][1] += dy''')
rep('''DZ_CAB = -2.0 ''', '''DZ_CAB = -2.5; DY_CAB = 1.0 ''')
rep('''    deslocar(i_cab, [cabeca, juba], DZ_CAB)''', '''    deslocar(i_cab, [cabeca, juba], DZ_CAB, DY_CAB)''')
rep('''        ("pescoco_alto", 3.4, 17.6, 25.4, -21.8, -15.6, -12, (0, 22.0, -19.0)),''',
    '''        ("pescoco_alto", 3.4, 17.6, 26.4, -22.2, -16.0, -12, (0, 22.0, -19.4)),''')
# peito: escudo oval de 5 faixas coladas, seguindo a curva do pescoço
rep('''    # placas: 7 degraus de frente vertical seguindo a linha da garganta ao peito (medida na ficha)
    def z_frente(y):
        return -21.6 - (y - 20.0) * 0.25 if y >= 20 else -12.6 - (y - 10.0) * 0.84
    for k, (yb, ya, w) in enumerate([(22.4, 24.6, 3.2), (20.3, 22.6, 3.9), (18.2, 20.5, 4.5), (16.1, 18.4, 4.9),
                                     (14.0, 16.3, 5.0), (11.9, 14.2, 4.7), (9.8, 12.1, 4.0)]):
        zf = z_frente((ya + yb) / 2) - 0.5
        pesc.append(peca(f"placa{k}", [-w, yb, zf], [w, ya, zf + 2.6], mat_placa, res=3))''',
'''    # escudo do peito: 5 faixas coladas na frente do pescoço (0,4 à frente), cada uma inclinada como a curva da
    # garganta ao peito; contorno oval (estreito em cima e embaixo, largo no meio)
    def z_frente(y):
        return -22.0 - (y - 20.0) * 0.25 if y >= 20 else -12.8 - (y - 10.0) * 0.86
    for k, (yb, ya, w) in enumerate([(22.2, 25.4, 2.8), (19.0, 22.4, 3.9), (15.8, 19.2, 4.5), (12.6, 16.0, 4.3), (9.6, 12.8, 3.4)]):
        yc = (ya + yb) / 2; zc = z_frente(yc)
        ang = math.degrees(math.atan(0.25 if yc >= 20 else 0.86))
        pesc.append(peca(f"placa{k}", [-w, yb, zc - 0.4], [w, ya, zc + 1.2], mat_placa, rot=(-ang, 0, 0),
                         pivo=(0, yc, zc), res=3))''')
# asa: leque de penas longas e finas, sem serrote; ombreira menor e alta
rep('''    for k in range(5):   # leque de penas de fogo sob as escamas, do ombro para trás e para baixo (como na ficha)
        raiz = (6.0 * lado, 19.0 - 0.3 * k, -11.0 + 2.2 * k)
        filhos.append(pena_bloco(f"fogo{k}_{s}", raiz, (-(42 + 5 * k), 0, 22 * lado), 8.4 - 0.4 * k, 3.4,
                                 cores_fogo[k % 4], esp=1.6))''',
'''    for k in range(5):   # leque de penas longas sob as escamas, para trás e para baixo, umas sobre as outras
        raiz = (6.0 * lado + 0.15 * lado * k, 19.4 - 0.2 * k, -10.4 + 1.6 * k)
        filhos.append(pena_bloco(f"fogo{k}_{s}", raiz, (-(54 + 4 * k), 0, 20 * lado), 9.4 - 0.5 * k, 2.4,
                                 (VERM, LARANJA, OURO), esp=1.2))''')
rep('''    filhos.append(escama(f"ombreira_{s}", (6.4 * lado, 19.6, -11.4), (-14, 0, 12 * lado), 38 * lado, 6.6, 4.8, m0, b0))''',
    '''    filhos.append(escama(f"ombreira_{s}", (6.4 * lado, 21.4, -11.2), (-14, 0, 14 * lado), 38 * lado, 4.6, 4.2, m0, b0))''')
# pernas: faixa laranja com uma faixa escura no meio (sem amarelo)
rep('''    faixa = g.mat_cor(lambda p, f: mix(LARANJA_ESC, AMARELO, clamp((p[1] - 3.6) / 5.0)), borda=.04, curva=.1)''',
    '''    def cor_faixa(p, f, tras=tras):
        y0, y1 = (3.6, 7.0) if tras else (4.2, 9.0)
        t = (p[1] - y0) / (y1 - y0)
        return escurecer(LARANJA, 0.3) if 0.42 < t < 0.56 else LARANJA
    faixa = g.mat_cor(cor_faixa, borda=.04, curva=.1)''')
# cauda: afina até ~35%, ponta curvando para baixo
rep('''    Rs = [18, -18, -32, -30, -26, -24, -26, -26, -16, -4, 2, 4]
    Hs = [7.8, 7.6, 7.4, 7.2, 7.0, 6.8, 6.5, 6.0, 5.5, 5.0, 4.6, 4.2]
    Ws = [10.4, 10.6, 10.8, 11.0, 10.8, 10.2, 9.4, 8.6, 7.8, 7.0, 6.4, 5.8]''',
'''    Rs = [18, -18, -32, -30, -26, -24, -26, -26, -14, -2, 12, 14]
    Hs = [7.8, 7.6, 7.4, 7.0, 6.6, 6.2, 5.7, 5.1, 4.5, 3.9, 3.3, 2.8]
    Ws = [10.4, 10.6, 10.6, 10.2, 9.6, 8.8, 7.8, 6.8, 5.8, 4.8, 4.0, 3.4]''')
p.write_text(s, encoding="utf-8"); print("ok b")

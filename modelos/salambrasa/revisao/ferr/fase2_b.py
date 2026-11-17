from pathlib import Path
p = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\salambrasa.py"); s = p.read_text(encoding="utf-8")
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:150]
    s = s.replace(a, b)

# manchas maiores (o brilho da ficha as faz parecer maiores) e de trás com limiar menor
rep('''MANCHAS_CAUDA_LADO = [(25.9, 13.5, 2.6, 3.2), (25.6, 21.9, 3.4, 4.2), (22.4, 17.2, 2.6, 3.2), (19.7, 26.6, 4.2, 3.2),
                      (18.0, 14.0, 3.0, 2.2), (13.0, 14.2, 3.2, 2.4), (12.8, 28.8, 3.4, 2.0), (8.0, 28.0, 2.4, 2.0)]
MANCHAS_CAUDA_TRAS = [(0.0, 17.9, 4.6, 5.4), (0.0, 10.6, 3.6, 3.0), (0.0, 23.2, 2.8, 1.6),
                      (-4.6, 21.3, 2.2, 3.0), (4.6, 21.3, 2.2, 3.0), (-4.8, 14.7, 1.6, 2.4), (4.8, 14.7, 1.6, 2.4)]''',
'''MANCHAS_CAUDA_LADO = [(25.9, 13.5, 3.4, 4.0), (25.6, 21.9, 4.2, 5.0), (22.4, 17.2, 3.4, 4.0), (19.7, 26.6, 5.2, 4.0),
                      (18.0, 14.0, 3.8, 3.0), (13.0, 14.2, 4.0, 3.2), (12.8, 28.8, 4.2, 2.8), (8.0, 28.0, 3.0, 2.6)]
MANCHAS_CAUDA_TRAS = [(0.0, 17.9, 5.4, 6.2), (0.0, 10.6, 4.2, 3.6), (0.0, 23.4, 3.4, 2.2),
                      (-4.6, 21.3, 2.8, 3.6), (4.6, 21.3, 2.8, 3.6), (-4.8, 14.7, 2.2, 3.0), (4.8, 14.7, 2.2, 3.0)]''')
rep('''    if nw[2] > 0.4:''', '''    if nw[2] > 0.2:''')

# ---------- cabeça: face malva clara em volta do olho e embaixo dele ----------
rep('''def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return CABECA_CLARA
    return CABECA''', '''def cor_cabeca(p, face):
    """Alto da cabeça cinza-ameixa; da altura do olho para baixo, a 'cara' malva clara (como na ficha)."""
    x, y, z = p
    if face == "up": return CABECA_CLARA
    if y < 28.6 and face != "down": return FACE
    return CABECA''')
rep('''            o = g.pintar_olho(u + 0.15, y - OLHO_Y, 2.15, 1.75, iris=((176, 34, 12), (246, 96, 30)), esclera=CREME,
                              r_iris=(0.5, 0.7), c_iris=(-0.42, -0.12), r_pup=(0.24, 0.32), bravo=0.25, alto=0.42,''',
'''            o = g.pintar_olho(u + 0.15, y - OLHO_Y, 2.3, 1.85, iris=((170, 40, 8), (232, 84, 14)), esclera=CREME,
                              r_iris=(0.48, 0.66), c_iris=(-0.44, -0.12), r_pup=(0.22, 0.3), bravo=0.32, alto=0.42,''')
rep('''                              contorno=CABECA_ESC)''', '''                              contorno=(150, 40, 40))''')
# viseira em V marcado (laterais mais altas)
rep('''        cab.append(peca("viseira_" + s, [x0, 29.3, -22.9], [x1, 31.8, -15.0], mat_viseira, rot=(-6, 0, 4 * lado),
                        pivo=(5.2 * lado, 31.8, -18.0), res=3))''',
'''        cab.append(peca("viseira_" + s, [x0, 29.4, -23.0], [x1, 31.6, -15.0], mat_viseira, rot=(-6, 0, 15 * lado),
                        pivo=(5.2 * lado, 31.6, -18.0), res=3))''')
# bico: de frente uma cunha que afina para baixo (degraus), de lado longo e em gancho
rep('''    cab.append(peca("bico", [-1.95, 24.9, -23.8], [1.95, 28.7, -21.0], mat_bico, rot=(-6, 0, 0), pivo=(0, 28.7, -21.0), res=4))
    cab.append(peca("bico_ponta", [-1.4, 25.3, -26.2], [1.4, 28.0, -23.4], mat_bico, rot=(-12, 0, 0), pivo=(0, 28.0, -23.4), res=4))
    cab.append(peca("bico_gancho", [-1.0, 23.4, -26.9], [1.0, 26.2, -25.0], mat_bico, rot=(-16, 0, 0), pivo=(0, 26.2, -25.0), res=4))''',
'''    cab.append(peca("bico", [-1.7, 26.2, -24.0], [1.7, 28.6, -21.0], mat_bico, rot=(-6, 0, 0), pivo=(0, 28.6, -21.0), res=4))
    cab.append(peca("bico_meio", [-1.15, 24.6, -25.6], [1.15, 27.4, -21.2], mat_bico, rot=(-8, 0, 0), pivo=(0, 27.4, -21.2), res=4))
    cab.append(peca("bico_gancho", [-0.6, 23.0, -26.6], [0.6, 25.4, -24.8], mat_bico, rot=(-14, 0, 0), pivo=(0, 25.4, -24.8), res=4))''')
rep('''    cab.append(peca("bico_baixo", [-1.3, 24.2, -23.8], [1.3, 25.6, -20.8], g.mat_cor(lambda p, f: BICO_ESC, borda=.08), res=4))''',
    '''    cab.append(peca("bico_baixo", [-0.8, 24.2, -23.2], [0.8, 25.2, -20.8], g.mat_cor(lambda p, f: BICO_ESC, borda=.08), res=4))''')
# crista: moicano estreito de blocos em degrau
rep('''    LAMINAS = [  # (meia largura, y0, y1, z0, z1, inclinação para trás)
        (5.0, 31.4, 35.0, -22.8, -19.0, 2),
        (4.6, 30.8, 38.0, -20.4, -16.6, 6),
        (2.3, 31.0, 39.4, -17.6, -13.8, 6),
        (4.4, 30.6, 36.8, -14.8, -11.2, 10),
        (4.2, 29.8, 34.4, -12.4, -9.2, 20),
    ]
    for k, (xm, y0, y1, z0, z1, inc) in enumerate(LAMINAS):
        cr.append(bloco_crista(f"crista{k}", [-xm, y0, z0], [xm, y1, z1], rot=(inc, 0, 0), pivo=(0, y0, z1)))
        if xm > 3:   # degrau em cima de cada lâmina larga: o contorno fica em escada, como os blocos da ficha
            cr.append(bloco_crista(f"crista{k}_degrau", [-xm * 0.55, y1 - 0.2, z0 + 0.5], [xm * 0.55, y1 + 1.2, z1 - 0.4],
                                   rot=(inc, 0, 0), pivo=(0, y0, z1)))''',
'''    LAMINAS = [  # (meia largura, y0, y1, z0, z1, inclinação para trás): moicano estreito, o mais alto no meio
        (2.0, 31.0, 35.6, -22.2, -18.8, 2),
        (2.2, 30.8, 38.0, -20.2, -16.4, 6),
        (1.8, 31.0, 39.4, -17.6, -13.8, 6),
        (2.2, 30.6, 36.8, -14.8, -11.2, 12),
        (2.0, 29.8, 34.4, -12.4, -9.2, 22),
    ]
    for k, (xm, y0, y1, z0, z1, inc) in enumerate(LAMINAS):
        cr.append(bloco_crista(f"crista{k}", [-xm, y0, z0], [xm, y1, z1], rot=(inc, 0, 0), pivo=(0, y0, z1)))
    for lado in (-1, 1):   # degraus mais baixos dos lados do moicano (de frente: a 'cruz' em escada da ficha)
        s = "d" if lado < 0 else "e"
        for k, (xa, xb, y0, y1, z0, z1, inc) in enumerate([(1.8, 4.2, 30.9, 33.8, -21.0, -17.0, 4),
                                                           (1.8, 3.8, 30.7, 34.8, -15.4, -11.4, 12)]):
            x0, x1 = sorted((xa * lado, xb * lado))
            cr.append(bloco_crista(f"crista_degrau{k}_{s}", [x0, y0, z0], [x1, y1, z1], rot=(inc, 0, 0), pivo=(0, y0, z1)))''')
# lóbulos vermelhos ao lado do rosto (x 5,3..6,7, y 25,5..30,6), um pouco mais à frente
rep('''        x0, x1 = sorted((4.7 * lado, 6.3 * lado))
        cr.append(bloco_crista("crista_lado_" + s, [x0, 26.4, -14.0], [x1, 31.0, -11.0]))''',
'''        x0, x1 = sorted((4.8 * lado, 6.5 * lado))
        cr.append(bloco_crista("crista_lado_" + s, [x0, 25.6, -16.0], [x1, 30.6, -12.6]))''')
# penas da bochecha: emolduram o rosto embaixo (laranja), abrindo para os lados
rep('''    for k, (y0, z0, L, rx, rz) in enumerate([(29.2, -14.2, 6.4, -76, 14), (27.2, -15.4, 6.8, -66, 18), (25.4, -13.2, 7.0, -58, 24)]):
        for lado in (-1, 1):
            s = "d" if lado < 0 else "e"
            cores = [(CRISTA, VERM, LARANJA), (VERM, LARANJA_ESC, LARANJA), (LARANJA_ESC, LARANJA, AMARELO)][k]
            boch.append(pena_bloco(f"bochecha{k}_{s}", (4.4 * lado, y0, z0), (rx, 0, rz * lado), L, 3.4, cores, esp=1.1))''',
'''    for k, (x, y0, z0, L, rx, rz) in enumerate([(4.4, 29.2, -14.2, 6.6, -76, 16), (4.4, 27.2, -15.4, 7.0, -64, 22),
                                                (4.4, 25.4, -13.2, 7.4, -56, 30), (3.8, 25.0, -17.8, 6.2, -24, 34)]):
        for lado in (-1, 1):
            s = "d" if lado < 0 else "e"
            cores = [(CRISTA, VERM, LARANJA), (VERM, LARANJA_ESC, LARANJA), (LARANJA_ESC, LARANJA, AMARELO),
                     (LARANJA_ESC, LARANJA, AMARELO)][k]
            boch.append(pena_bloco(f"bochecha{k}_{s}", (x * lado, y0, z0), (rx, 0, rz * lado), L, 3.4, cores, esp=1.3))''')
# juba grande, em leque
rep('''        (2.6, 24.4, -19.8, -90, 6, 38, 6.4, 3.2, C1),       # 'babador' de frente, abrindo para os lados
        (1.6, 22.4, -19.0, -90, 8, 18, 5.2, 2.8, C3),
        (4.0, 25.0, -16.6, -35, 24, 34, 7.4, 3.2, C1),      # lados, varrendo para trás e abrindo
        (4.4, 25.0, -13.4, 15, 26, 42, 8.0, 3.4, C1),
        (3.4, 25.2, -10.8, 60, 24, 50, 7.6, 3.2, C2),
        (4.4, 22.2, -15.0, -20, 28, 24, 6.8, 3.2, C2),
        (4.4, 21.8, -11.6, 35, 28, 34, 7.0, 3.2, C3),''',
'''        (2.8, 24.2, -19.8, -90, 6, 40, 6.8, 3.4, C1),       # 'babador' de frente, abrindo para os lados
        (4.2, 25.0, -16.8, -40, 38, 30, 9.0, 3.8, C1),      # leque dos lados: abre bem para fora
        (4.6, 25.2, -13.6, 5, 42, 40, 9.6, 4.0, C1),
        (3.8, 25.4, -10.8, 55, 36, 52, 9.0, 3.8, C2),
        (4.6, 22.0, -16.0, -30, 46, 22, 8.0, 3.6, C2),
        (4.8, 21.8, -12.6, 15, 50, 32, 8.4, 3.8, C3),
        (4.2, 21.6, -9.8, 60, 40, 44, 7.6, 3.4, C3),
        (4.4, 19.0, -14.8, -10, 56, 20, 6.6, 3.4, C3),''')
rep('''    juba.append(pena_cone("juba_nuca", (0, 25.2, -10.0), 90, 0, 7.6, 3.8, 1, C2, varre=48, esp=1.8))''',
    '''    juba.append(pena_cone("juba_nuca", (0, 25.4, -9.6), 90, 0, 9.0, 4.0, 1, C2, varre=50, esp=1.8))''')

# ---------- placas da barriga: degraus de frente vertical (pegam luz no jogo), 7 faixas, até ~9,4 de largura ----------
rep('''        n = 5 if nome == "pescoco_baixo" else 2
        for k in range(n):       # placas rentes à frente da peça (mesmo giro), da garganta para o peito

            ya = y1 - 0.4 - k * (y1 - y0 - 0.8) / n; yb = ya - (y1 - y0 - 0.8) / n - 0.3
            w = xm + (0.35 * k if nome == "pescoco_baixo" else 0.2 * k - 0.4)
            pesc.append(peca(f"{nome}_placa{k}", [-w, yb, z0 - 0.7], [w, ya, z0 + 0.3], mat_placa, rot=(inc, 0, 0), pivo=pv, res=3))''',
'''    # placas: 7 degraus de frente vertical seguindo a linha da garganta ao peito (medida na ficha)
    def z_frente(y):
        return -21.6 - (y - 20.0) * 0.25 if y >= 20 else -12.6 - (y - 10.0) * 0.84
    for k, (yb, ya, w) in enumerate([(22.4, 24.6, 3.0), (20.3, 22.6, 3.6), (18.2, 20.5, 4.2), (16.1, 18.4, 4.6),
                                     (14.0, 16.3, 4.7), (11.9, 14.2, 4.4), (9.8, 12.1, 3.8)]):
        zf = z_frente((ya + yb) / 2) - 0.5
        pesc.append(peca(f"placa{k}", [-w, yb, zf], [w, ya, zf + 2.6], mat_placa, res=3))''')
rep('''        pesc += g.octogono(nome, [-xm, y0, z0], [xm, y1, z1], mat_pesc(z0), r=1.0, faixa=(9, 27), rot=(inc, 0, 0), pivo=pv)''',
    '''        pesc += g.octogono(nome, [-xm, y0, z0], [xm, y1, z1], mat_pesc(z0), r=1.0, faixa=(9, 27), rot=(inc, 0, 0), pivo=pv)
''')
rep('''def mat_placa(c):
    """Placa laranja do peito/pescoço: pêssego claro em cima, laranja no meio, fio escuro na beirada de baixo."""
    face = c["face"]
    (_, y0, _), (_, y1, _) = c["b"]
    v = clamp((y1 - c["p"][1]) / max(y1 - y0, 1e-6))
    if face == "up": return PLACA_CLARA
    if face == "down": return PLACA_ESC
    base = mix(PLACA_CLARA, PLACA, 0.4) if v < 0.25 else PLACA
    if face in ("east", "west"): base = tom(base, -0.15)
    if v > 0.88: base = mix(PLACA, PLACA_ESC, 0.5)
    return base''',
'''def mat_placa(c):
    """Placa laranja da barriga: em cima pêssego claro, frente laranja com cantos arredondados (mais escuros), fio
    escuro na beirada de baixo; de lado um pouco mais escura."""
    face = c["face"]
    (x0, y0, _), (x1, y1, _) = c["b"]
    v = clamp((y1 - c["p"][1]) / max(y1 - y0, 1e-6))
    u = abs(c["p"][0]) / max(x1, 1e-6)
    if face == "up": return PLACA_CLARA
    if face == "down": return PLACA_ESC
    base = PLACA_CLARA if v < 0.22 else PLACA
    if face in ("east", "west"): base = tom(PLACA, -0.15)
    if v > 0.86 or (face == "north" and u > 0.86 and v > 0.5): base = PLACA_ESC
    return base''')
p.write_text(s, encoding="utf-8")
print("ok")

from pathlib import Path
p = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\salambrasa.py"); s = p.read_text(encoding="utf-8")
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:160]
    s = s.replace(a, b)
def entre(ini, fim, novo):
    global s
    a = s.index(ini); b = s.index(fim, a)
    s = s[:a] + novo + s[b:]

# ======================= paleta =======================
entre("GRAFITE = (66, 51, 62)", "def escurecer", '''GRAFITE = (66, 51, 62); GRAFITE_ESC = (46, 35, 44); GRAFITE_CLARO = (87, 70, 80)        # corpo carvão-arroxeado
MALVA = (110, 92, 104); MALVA_CLARA = (138, 116, 128); MALVA_ESC = (86, 70, 82)          # placas do ombro, viseira, pé
CABECA = (96, 78, 90); CABECA_CLARA = (116, 96, 108); CABECA_ESC = (70, 56, 66)          # cabeça cinza-roxa (quadro 103,78,95)
FACE = (104, 86, 98)
VISEIRA = MALVA; VISEIRA_CLARA = (132, 112, 124); VISEIRA_ESC = MALVA_ESC
BICO = (138, 116, 128); BICO_CLARO = (156, 134, 146); BICO_ESC = (112, 92, 104)          # malva clara
DEDO = (191, 169, 179); DEDO_CLARO = (210, 192, 200); DEDO_ESC = (156, 134, 146)
CRISTA = (200, 40, 42); CRISTA_ESC = (168, 26, 30); CRISTA_CLARA = (232, 68, 58)          # lados / topo das lâminas
VERM = (192, 40, 42); VERM_ESC = (170, 26, 24)
LARANJA = (240, 90, 30); LARANJA_ESC = (253, 69, 11); AMARELO = (245, 197, 24); OURO = (245, 197, 24)
LARANJA_M = (247, 147, 30)
PLACA = (247, 147, 30); PLACA_CLARA = (249, 178, 90); PLACA_ESC = (192, 90, 16)          # escamas da barriga
VENTRE = (247, 147, 30)
CREME = (244, 230, 220)
BRASA = (245, 197, 24); BRASA_BORDA = (247, 147, 30)                                     # manchas: amarelo cheio, halo laranja

''')

# ======================= penas: sombras leves, sem ferrugem =======================
rep('''        if face == "up": base = mix(base, (255, 236, 200), 0.15)
        elif face == "down": base = escurecer(base, 0.3)
        elif face in ("north", "south"): base = escurecer(base, 0.1)
        return escurecer(base, 0.15) if g.na_borda(c) else base''',
'''        if face == "up": base = mix(base, (255, 236, 200), 0.15)
        elif face == "down": base = escurecer(base, 0.18)
        elif face in ("north", "south"): base = escurecer(base, 0.06)
        return escurecer(base, 0.1) if g.na_borda(c) else base''')

# ======================= corpo: terço de baixo laranja, manchas em 2 fileiras, escamas em chevron =======================
entre("VENTRE_Y = 11.2", "# ---------------- cauda em gancho", '''VENTRE_Y = 12.4          # terço de baixo do tronco: laranja, com transição para o carvão

def cor_corpo(p, face):
    x, y, z = p
    if face == "down" or y < VENTRE_Y: return VENTRE
    if y < VENTRE_Y + 1.4: return mix(VENTRE, GRAFITE, (y - VENTRE_Y) / 1.4)
    return GRAFITE

# (centro, meio-tamanho, profundidade): 2 fileiras de octógonos de cada lado do tronco, como na ficha
MANCHAS_CORPO = []
for lado in (-1, 1):
    MANCHAS_CORPO += [((5.9 * lado, 18.0, z), (1, 1.1, 1.3), 0.35) for z in (-8.6, -2.6, 3.2)]
    MANCHAS_CORPO += [((5.9 * lado, 14.6, z), (1, 1.0, 1.2), 0.35) for z in (-5.6, 0.2)]
    MANCHAS_CORPO += [((5.6 * lado, 16.6, 8.8), (1, 1.0, 1.2), 0.35)]

def mat_placa(i, n):
    """Escama da barriga nº i (de n, de cima para baixo): laranja da paleta em degradê (pêssego em cima, laranja quente
    embaixo), rente ao corpo; a borda de baixo é um arco (chevron) com uma linha escura de 1 px."""
    c_top = mix(PLACA_CLARA, PLACA, i / max(n - 1, 1) * 1.6)
    c_bot = mix(PLACA, LARANJA, i / max(n - 1, 1))
    def f(c):
        face = c["face"]
        (x0, y0, _), (x1, y1, _) = c["b"]
        v = clamp((y1 - c["p"][1]) / max(y1 - y0, 1e-6))
        u = abs(c["p"][0]) / max(x1, 1e-6)
        if face == "up": return c_top
        if face == "down": return escurecer(c_bot, 0.2)
        linha = 0.86 - 0.3 * u * u                       # borda de baixo em arco: mais baixa no meio
        if face in ("east", "west"): return escurecer(c_bot, 0.08)
        if v > linha + 0.1: return escurecer(c_bot, 0.12)
        if v > linha: return PLACA_ESC
        return mix(c_top, c_bot, v / max(linha, 0.1))
    return f

''')

# ======================= cauda: laranja só embaixo da base; manchas como na ficha =======================
rep('''        if base:
            if face == "down": return VENTRE
            if v < 0.3: return VENTRE
            return GRAFITE
        if face == "down": return GRAFITE
        if face == "up": return GRAFITE
        if k < 7:
            return VENTRE if v < 0.24 else GRAFITE
        return VENTRE if v > 0.8 else GRAFITE''', '''        if k < 3:                                   # base: barriga laranja embaixo, com borda baixa nos lados
            if face == "down": return VENTRE
            if v < 0.16: return VENTRE
            if v < 0.26: return mix(VENTRE, GRAFITE, (v - 0.16) / 0.1)
        return GRAFITE''')
rep('''    base = k < 4
    def cor(p, face):''', '''    def cor(p, face):''')
a = s.index("MANCHAS_CAUDA_LADO = ["); b = s.index("def mancha_cauda")
s = s[:a] + '''MANCHAS_CAUDA_LADO = [(25.9, 13.5, 2.4, 2.8), (25.6, 21.9, 3.0, 3.6), (19.7, 26.8, 3.4, 2.6),
                      (18.0, 13.6, 2.8, 2.0), (12.6, 14.0, 3.0, 2.2), (12.8, 28.6, 3.0, 1.8), (22.6, 17.4, 2.4, 2.8)]
MANCHAS_CAUDA_TRAS = [(0.0, 17.6, 3.8, 4.4), (0.0, 10.4, 3.0, 2.6), (0.0, 23.4, 2.4, 1.8),
                      (-3.0, 21.0, 1.6, 2.2), (3.0, 21.0, 1.6, 2.2), (-3.0, 13.8, 1.6, 2.2), (3.0, 13.8, 1.6, 2.2)]

''' + s[b:]
rep('''            filhos += secao(f"{nome}_ponta", px, py, pz + L - 0.2, pz + L + 1.0, w * 0.7, h * 0.7, mat, br)''',
    '''            filhos += secao(f"{nome}_ponta", px, py, pz + L - 0.2, pz + L + 0.9, w * 0.66, h * 0.66, mat, br)
            filhos += secao(f"{nome}_ponta2", px, py, pz + L + 0.7, pz + L + 1.4, w * 0.36, h * 0.36, mat, br)''')

# ======================= olho, viseira, bico, crista =======================
rep('''iris=((150, 30, 14), (216, 64, 28))''', '''iris=((160, 34, 14), (224, 74, 30))''')
rep('''def mat_viseira(c):
    face = c["face"]
    base = VISEIRA_CLARA if face == "up" else VISEIRA_ESC if face == "down" else VISEIRA
    if face == "north": base = tom(VISEIRA, 0.06)
    return tom(base, -0.22) if g.na_borda(c) else base''', '''def mat_viseira(c):
    """Viseira cinza-malva, mais clara que a cabeça; topo 1 tom mais claro."""
    face = c["face"]
    base = VISEIRA_CLARA if face == "up" else VISEIRA_ESC if face == "down" else VISEIRA
    return escurecer(base, 0.12) if g.na_borda(c) else base''')
rep('''def mat_bico(c):
    face = c["face"]; x, y, z = c["p"]
    if face == "up" and 0.5 < abs(x) < 1.0 and -23.9 < z < -23.2: return (52, 38, 46)    # narina
    base = BICO_CLARO if face == "up" else BICO_ESC if face == "down" else BICO
    if face in ("north",): base = tom(BICO, 0.05)
    return tom(base, -0.15) if g.na_borda(c) else base''', '''def mat_bico(c):
    """Malva clara de uma cor só; faixa de baixo um tom mais escura; narina escura pequena perto da base, de lado."""
    face = c["face"]; x, y, z = c["p"]
    if face in ("east", "west") and -22.4 < z < -21.7 and 27.6 < y < 28.2: return (52, 38, 46)
    if face == "up": return BICO_CLARO
    if face == "down" or y < 26.0: return BICO_ESC
    return escurecer(BICO, 0.06) if g.na_borda(c) else BICO''')
rep('''def mat_crista(c):
    """Bloco vermelho chapado: em cima claro, lados na base, frente um pouco mais clara, embaixo escuro."""
    face = c["face"]
    if face == "up": base = CRISTA_CLARA
    elif face == "down": base = CRISTA_ESC
    elif face == "north": base = tom(CRISTA, 0.08)
    elif face == "south": base = tom(CRISTA, -0.15)
    else: base = CRISTA
    return tom(base, -0.2) if g.na_borda(c) else base''', '''def mat_crista(c):
    """Lâmina vermelha: lados #c0282a, topo e alto da lâmina mais claros (#e8443a), base mais escura."""
    face = c["face"]
    (_, y0, _), (_, y1, _) = c["b"]
    t = clamp((c["p"][1] - y0) / max(y1 - y0, 1e-6))
    if face == "up": return CRISTA_CLARA
    if face == "down": return CRISTA_ESC
    base = mix(CRISTA, CRISTA_CLARA, clamp((t - 0.55) / 0.45)) if t > 0.55 else CRISTA
    if face == "south": base = escurecer(base, 0.1)
    return escurecer(base, 0.12) if g.na_borda(c) else base''')

# ======================= ombro: placas cinza-malva, 2 fendas, leque de penas caindo para trás =======================
rep('''        face = c["face"]
        base = GRAFITE_CLARO if face == "up" else GRAFITE_ESC if face == "down" else \\
            mix(GRAFITE, GRAFITE_CLARO, 0.35) if face == fora else GRAFITE
        return tom(base, -0.25) if g.na_borda(c) else base''', '''        face = c["face"]
        base = MALVA_CLARA if face == "up" else MALVA_ESC if face == "down" else MALVA
        return MALVA_CLARA if g.na_borda(c) and face == fora else base''')
rep('''    for k in range(5):   # leque de penas longas sob as escamas, para trás e para baixo, umas sobre as outras
        raiz = (6.6 * lado + 0.15 * lado * k, 18.8 - 0.3 * k, -11.0 + 1.8 * k)
        filhos.append(pena_bloco(f"fogo{k}_{s}", raiz, (-(50 + 5 * k), 0, 18 * lado), 10.6 - 0.5 * k, 2.8,
                                 (VERM, LARANJA, OURO), esp=1.2))''',
'''    # leque de penas pontudas caindo para trás (~30° abaixo da horizontal); as de baixo chegam ao meio do tronco
    for k, (y, z, rx, L) in enumerate([(19.6, -10.6, -64, 8.6), (19.0, -9.6, -56, 9.6), (18.4, -8.6, -48, 10.6),
                                       (17.8, -7.6, -40, 11.2), (17.2, -6.8, -32, 10.4)]):
        raiz = (6.5 * lado + 0.12 * lado * k, y, z)
        filhos.append(pena_bloco(f"fogo{k}_{s}", raiz, (rx, 0, 16 * lado), L, 2.6, (VERM, LARANJA, OURO), esp=1.1))''')
rep('''    filhos.append(escama(f"ombreira_{s}", (6.4 * lado, 21.4, -11.2), (-14, 0, 14 * lado), 38 * lado, 4.6, 4.2, m0, b0))''',
    '''    filhos.append(escama(f"ombreira_{s}", (6.3 * lado, 20.8, -11.4), (-20, 0, 14 * lado), 38 * lado, 4.6, 4.2, m0, b0))''')
rep('''    for k, (z, y, L, W, rx) in enumerate([(-6.2, 21.0, 7.0, 3.8, -66), (-9.0, 21.6, 8.4, 4.6, -60), (-11.0, 21.0, 6.6, 4.0, -52)]):
        raiz = (6.0 * lado + 0.3 * lado * k, y, z)
        m, br = mat_escama(lado, (raiz[0], y - 3.0, z), k == 1)''',
'''    for k, (z, y, L, W, rx) in enumerate([(-6.4, 20.2, 7.0, 3.8, -70), (-9.0, 20.6, 8.4, 4.6, -64), (-11.2, 20.4, 6.6, 4.0, -58)]):
        raiz = (6.2 * lado + 0.3 * lado * k, y, z)
        m, br = mat_escama(lado, (raiz[0], y - 3.0, z), k != 2)       # fenda em Y em 2 placas''')

# ======================= patas =======================
rep('''    pp.append(peca(nome + "_pata", [xc - 3.0, 0.4, zc - 2.6], [xc + 3.0, 3.4, zc + 2.4],
                   g.mat_cor(lambda p, f: GRAFITE, borda=.08, curva=.4), res=3))
    for k, (dx, giro) in enumerate(((-2.4, 17), (0.0, 0), (2.4, -17))):
        x0 = xc + dx; z0 = zc - 1.2
        pp.append(osso(f"{nome}_dedo{k}", [x0, 0, z0], [0, giro, 0],
                       [peca(f"{nome}_dedo{k}", [x0 - 1.15, 0, z0 - 4.6], [x0 + 1.15, 2.9, z0], mat_dedo, res=3)]))
    pp.append(peca(nome + "_dedo_tras", [xc - 0.8, 0, zc + 1.8], [xc + 0.8, 1.6, zc + 3.6], mat_dedo, res=3))''',
'''    pp.append(peca(nome + "_pata", [xc - 2.9, 0.4, zc - 2.6], [xc + 2.9, 3.4, zc + 2.4],
                   g.mat_cor(lambda p, f: MALVA, borda=.06, curva=.3), res=3))                 # pé malva robusto
    for k, (dx, giro, mw, mh, ml) in enumerate(((-2.35, 16, 1.05, 2.6, 4.8), (0.0, 0, 1.25, 3.0, 5.4), (2.35, -16, 1.05, 2.6, 4.8))):
        x0 = xc + dx; z0 = zc - 1.2                                                           # o do meio é maior
        pp.append(osso(f"{nome}_dedo{k}", [x0, 0, z0], [0, giro, 0],
                       [peca(f"{nome}_dedo{k}", [x0 - mw, 0, z0 - ml], [x0 + mw, mh, z0], mat_dedo, res=3)]))
    pp.append(peca(nome + "_dedo_tras", [xc - 0.8, 0, zc + 1.8], [xc + 0.8, 1.6, zc + 3.8], mat_dedo, res=3))''')
rep('''    def cor_faixa(p, f, tras=tras):
        y0, y1 = (3.6, 7.0) if tras else (4.2, 9.0)
        t = (p[1] - y0) / (y1 - y0)
        return escurecer(LARANJA, 0.3) if 0.42 < t < 0.56 else LARANJA''', '''    def cor_faixa(p, f, tras=tras):        # uma faixa só: laranja quente em cima -> laranja-amarelo embaixo
        y0, y1 = (3.6, 7.0) if tras else (4.2, 9.0)
        t = clamp((p[1] - y0) / (y1 - y0))
        return mix(LARANJA_M, LARANJA, t)''')
rep('''    pp += g.octogono(nome + "_faixa", [xc - 2.35, yf0, zc - 2.35], [xc + 2.35, yf1, zc + 2.35], faixa, r=0.7)
    pp += g.octogono(nome + "_tornozelo", [xc - 2.45, 2.4, zc - 2.45], [xc + 2.45, yf0 + 0.2, zc + 2.45], escuro, r=0.7)''',
'''    pp += g.octogono(nome + "_faixa", [xc - 1.95, yf0, zc - 1.95], [xc + 1.95, yf1, zc + 1.95], faixa, r=0.6)   # canela mais fina
    pp += g.octogono(nome + "_tornozelo", [xc - 2.1, 2.4, zc - 2.1], [xc + 2.1, yf0 + 0.2, zc + 2.1], escuro, r=0.6)''')
p.write_text(s, encoding="utf-8"); print("ok fase4 (materiais)")

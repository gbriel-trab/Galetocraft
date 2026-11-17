p = 'ferramentas/especies/vagalo.py'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b)
# bico
rep('''    cab.append(peca("bico_meio", [-1.4, 23.9, -8.6], [1.4, 26.0, -6.8], mb, rot=(-12, 0, 0), pivo=(0, 26.0, -6.8), faixa=fb, res=4))
    cab.append(peca("bico_gancho", [-0.75, 23.2, -9.5], [0.75, 25.4, -8.4], mb, rot=(-30, 0, 0), pivo=(0, 25.4, -8.4), faixa=fb, res=4))
    cab.append(peca("bico_v", [-1.15, 23.25, -8.3], [1.15, 25.55, -6.0], mb, rot=(0, 0, 45), pivo=(0, 24.4, -7.15), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-1.25, 23.0, -8.0], [1.25, 23.9, -5.3], g.mat_cor(lambda p, f: AMBAR, borda=.1), rot=(8, 0, 0),
                    pivo=(0, 23.5, -5.3), res=4))''', '''    cab.append(peca("bico_meio", [-1.45, 23.85, -9.0], [1.45, 26.0, -6.8], mb, rot=(-10, 0, 0), pivo=(0, 26.0, -6.8), faixa=fb, res=4))
    cab.append(peca("bico_ponta", [-0.9, 23.5, -10.8], [0.9, 25.4, -8.8], mb, rot=(-22, 0, 0), pivo=(0, 25.4, -8.8), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-1.2, 23.0, -8.8], [1.2, 23.9, -5.3], g.mat_cor(lambda p, f: AMBAR, borda=.1), rot=(6, 0, 0),
                    pivo=(0, 23.5, -5.3), res=4))''')
rep("clamp((-z - 7.6) / 1.8) * 0.5", "clamp((-z - 8.4) / 2.2) * 0.5")
# lâminas da cabeça -> espetos afinando, varrendo para trás
a = s.index('    for k, (y0, rx, ext, z1) in enumerate([(28.3, 4, 0.9, 3.6)')
b = s.index('    cab.append(crista())')
s = s[:a] + '''    def mpc(c0, c1, ei, inv): return mat_pena_bloco(c0, c1, ei, inv)
    for k, (y0, rx, L) in enumerate([(28.2, 6, 5.6), (26.3, 12, 6.2), (24.4, 18, 5.2)]):
        for lado in (-1, 1):
            s_ = "d" if lado < 0 else "e"
            cab.append(g.pena_curva(f"lamina{k}_{s_}", (3.3 * lado, y0, -1.6),
                                    [(L * .55, 1.5, 1.7, ROXO, ROXO_MED), (L * .45, 1.0, 1.1, ROXO_MED, MALVA)],
                                    (rx, 30 * lado, 0), (6, 8 * lado, 0), "z", mpc, res=4))
    for k, (x0, y0, rx, L) in enumerate([(-1.3, 28.4, 14, 5.4), (1.3, 27.0, 20, 5.8), (-0.2, 25.2, 28, 5.0)]):
        cab.append(g.pena_curva(f"lamina_nuca{k}", (x0, y0, 2.0), [(L * .55, 2.0, 1.8, ROXO, ROXO_MED), (L * .45, 1.3, 1.2, ROXO_MED, MALVA)],
                                (rx, 8 * (1 if x0 > 0 else -1), 0), (8, 0, 0), "z", mpc, res=4))
''' + s[b:]
# crista: 5 dedos grossos
a = s.index('    filhos = [coluna("crista_c0"')
b = s.index('    return osso("crista"')
s = s[:a] + '''    filhos = [coluna("crista_c0", (0, 29.3, -3.0), (-8, 0, 0), (8, 0, 0), 0.85),
              coluna("crista_c1", (0, 29.4, -1.0), (12, 0, 0), (10, 0, 0), 1.25),
              coluna("crista_c2", (0, 29.4, 1.0), (30, 0, 0), (10, 0, 0), 1.15),
              coluna("crista_c3", (0, 29.2, 2.6), (48, 0, 0), (10, 0, 0), 0.95),
              coluna("crista_c4", (0, 28.8, 3.6), (66, 0, 0), (8, 0, 0), 0.75)]
    filhos.append(peca("crista_base", [-2.0, 29.0, -4.0], [2.0, 30.6, 3.6],
                       g.mat_cor(lambda p, f: mix(VERM_ESC, VERM, clamp((p[1] - 29.0) / 1.6)), borda=.1), res=4))
''' + s[b:]
rep('''    def coluna(nome, base, rot0, curva, k, w=2.6, h=1.9):
        segs = [(2.6 * k, w, h, VERM_ESC, VERM), (2.2 * k, w * .9, h * .9, VERM, VERM_VIVO), (1.7 * k, w * .8, h * .8, LARANJA, AMARELO)]''', '''    def coluna(nome, base, rot0, curva, k, w=3.6, h=2.7):
        segs = [(2.8 * k, w, h, VERM_ESC, VERM), (2.4 * k, w * .88, h * .9, VERM, VERM_VIVO), (0.9 * k, w * .78, h * .8, VERM_VIVO, LARANJA),
                (1.0 * k, w * .66, h * .7, AMARELO, AMAR_CLARO)]''')
# abdômen
rep('''        if dj < 0.12: cor = AMBAR
        else: cor = mix(AMARELO, AMAR_PALIDO, clamp((dj - 0.12) / 0.6))''', '''        if dj < 0.14: cor = (204, 106, 10)
        else: cor = mix((255, 178, 12), (255, 228, 64), clamp((dj - 0.14) / 0.55))''')
rep('''        luz = 0.1 - 0.45 * clamp((r - 0.3) / 0.8) ** 1.3 + 0.05 * ey''', '''        luz = 0.06 - 0.4 * clamp((r - 0.35) / 0.8) ** 1.3 + 0.04 * ey''')
rep('''corpo += g.arredondado2("abdomen", [-6.0, 4.0, -1.4], [6.0, 13.6, 11.2], mat_abdomen(), r=3.6, brilho=True)''', '''corpo += g.arredondado2("abdomen", [-6.5, 3.8, -1.8], [6.5, 14.2, 12.4], mat_abdomen(), r=3.9, brilho=True)''')
rep('''corpo += g.arredondado("abdomen_meio", [-5.2, 5.2, -0.6], [5.2, 12.8, 10.4], mat_abdomen(), r=2.2, brilho=True)''', '''corpo += g.arredondado("abdomen_meio", [-5.6, 4.8, -0.8], [5.6, 13.2, 11.4], mat_abdomen(), r=2.4, brilho=True)''')
rep("ex, ey, ez = x / 6.0, (y - 8.8) / 4.8, (z - 4.9) / 6.3", "ex, ey, ez = x / 6.5, (y - 9.0) / 5.2, (z - 5.3) / 7.1")
# asas de inseto
rep("MEMB_RAIZ = (150, 118, 62); MEMB_PONTA = (172, 146, 92); MEMB_CLARA = (218, 192, 122)", "MEMB_RAIZ = (214, 176, 92); MEMB_PONTA = (232, 204, 126); MEMB_CLARA = (250, 234, 168)")
rep("passo = 3.2\n", "passo = 4.6\n")
rep("if d2 - d1 < 0.3: return VEIA", "if d2 - d1 < 0.24: return VEIA")
rep("if borda < 0.3: return BORDA_ASA", "if borda < 0.4: return BORDA_ASA")
rep("if borda < 0.42: return AMBAR", "if borda < 0.52: return AMBAR")
rep("if abs(t - off - hw * 0.0) < 0.12 and s < 0.85: return VEIA", "if abs(t - off) < 0.1 and s < 0.85: return VEIA")
# postura
rep("SOBE_CAB = 1.6 ", "SOBE_CAB = 0.8 ")
rep("INCLINA = 8 ", "INCLINA = 18 ")
rep('*g.arredondado("pescoco", [-2.7, 18.4, -3.6], [2.7, 25.0, 1.4]', '*g.arredondado("pescoco", [-2.7, 18.4, -3.6], [2.7, 24.2, 1.4]')
# asa dobrada: 5 dedos
rep('''        for k, (rx, L, dx, dy) in enumerate([(5, 10.0, 0.0, 0.0), (9, 11.4, 0.3, -1.9), (13, 12.0, 0.6, -3.8), (18, 10.8, 0.8, -5.6)]):
            segs = [(L * .42, 1.0, 2.6, ROXO_ESC, ROXO), (L * .33, 0.9, 2.4, ROXO, ROXO_MED), (L * .17, 0.8, 2.0, AMARELO, AMAR_CLARO),
                    (L * .1, 0.7, 1.2, AMAR_CLARO, AMAR_PALIDO)]''', '''        for k, (rx, L, dx, dy) in enumerate([(4, 9.6, 0.0, 0.0), (8, 11.0, 0.25, -1.6), (12, 12.0, 0.5, -3.2), (16, 11.6, 0.7, -4.8),
                                             (21, 10.0, 0.9, -6.2)]):
            segs = [(L * .4, 1.0, 2.2, ROXO_ESC, ROXO), (L * .3, 0.9, 2.0, ROXO, ROXO_MED), (L * .18, 0.8, 1.7, AMARELO, AMARELO),
                    (L * .12, 0.7, 1.0, AMARELO, AMAR_CLARO)]''')
# cauda
a = s.index('    def pena_cauda(nome, base, rot0, curva, k=1.0):')
b = s.index('    corpo.append(osso("cauda"')
s = s[:a] + '''    def pena_cauda(nome, base, rot0, curva, k=1.0):
        """Foice comprida: sobe para trás e faz o arco para baixo; ponta amarela afinando (últimos ~35%)."""
        segs = [(2.6 * k, 1.3, 3.0, ROXO_ESC, ROXO), (2.6 * k, 1.2, 2.8, ROXO, ROXO_MED), (2.4 * k, 1.1, 2.5, ROXO_MED, ROXO),
                (2.0 * k, 1.0, 2.2, ROXO, AMBAR), (2.0 * k, 0.85, 1.8, AMARELO, AMARELO), (1.6 * k, 0.65, 1.1, AMARELO, AMAR_CLARO)]
        return g.pena_curva(nome, base, segs, rot0, curva, "z", mat_pena_bloco, brilho_ponta=True)
    cauda.append(pena_cauda("cauda_meio", (0, 19.0, 6.8), (-40, 0, 0), (15, 0, 0), 1.15))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cauda.append(pena_cauda("cauda1_" + s, (1.3 * lado, 18.4, 7.0), (-34, 16 * lado, 0), (14, 0, 0), 1.05))
        cauda.append(pena_cauda("cauda2_" + s, (2.4 * lado, 17.4, 7.0), (-24, 32 * lado, 0), (13, 0, 0), 0.92))
''' + s[b:]
rep('ONDAS = [("cauda_meio", 4, (3, 0, 0))]', 'ONDAS = [("cauda_meio", 6, (3, 0, 0))]')
open(p, 'w', encoding='utf-8').write(s)

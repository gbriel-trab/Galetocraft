p = 'ferramentas/especies/vagalo.py'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b)
def troca_bloco(ini, fim, novo):
    global s
    a = s.index(ini); b = s.index(fim, a)
    s = s[:a] + novo + s[b:]

# ---- 1. cauda: foices largas em leque vertical, nascendo alto atrás das asas, arqueando para trás e para BAIXO
troca_bloco('def foice(nome, base, L_total, H, rot0, curva, esp=0.55, n=4):', 'def bola(', '''def foice(nome, base, L_total, H, rot0, curva, esp=0.9):
    """Pena-foice larga e chata (placa de pé, fina em x): 3 segmentos que se curvam cada vez mais para baixo,
    e a ponta afiada em 2 degraus (blocos menores, sem recorte de transparência)."""
    partes = [(0.34, 1.0), (0.3, 0.92), (0.2, 0.78), (0.1, 0.5), (0.06, 0.26)]      # (fração do comprimento, altura)
    def seg(k, pos, ini):
        fr, fh = partes[k]
        L = L_total * fr; hk = H * fh
        px, py, pz = pos
        filhos = [peca(f"{nome}_{k}", [px - esp / 2 * (1 - 0.15 * k), py - hk / 2, pz], [px + esp / 2 * (1 - 0.15 * k), py + hk / 2, pz + L],
                       mat_foice(L_total, ini, L, hk, False), res=4)]
        if k + 1 < len(partes):
            filhos.append(seg(k + 1, (px, py, pz + L - 0.1), ini + L))
        r = list(rot0) if k == 0 else (list(curva) if k < 4 else [0, 0, 0])
        return osso(f"{nome}_{k}", list(pos), r, filhos)
    return seg(0, tuple(base), 0.0)

''')
troca_bloco('    for k in range(6):\n        lado = 1 if k % 2 else -1', '    corpo.append(osso("cauda"', '''    for k in range(6):
        lado = 1 if k % 2 else -1
        ang = -22 + 9 * k                       # leque vertical: a de cima sobe mais, cada uma ~9° mais baixa
        L = 13.5 - 0.9 * k
        cauda.append(foice(f"cauda{k}", (0.5 * lado * (k > 0), 19.6 - 0.75 * k, 8.6 + 0.1 * k), L, 4.0 - 0.2 * k,
                           (ang - INCLINA, 4 * lado * (k > 0), 0), (20, 0, 0)))
''')
rep('    corpo.append(osso("cauda", [0, 18.0, 10.6], [0, 0, 0], cauda))', '    corpo.append(osso("cauda", [0, 18.8, 8.6], [0, 0, 0], cauda))')
rep('ONDAS = [("cauda0", 4, (3, 0, 0))]', 'ONDAS = [("cauda0", 5, (3, 0, 0))]')

# ---- 2. bico em cunha dourada (metade da largura, mais comprido) e barbela grande em 2 lobos
troca_bloco('    cab.append(peca("bico_base"', '    # penas da cabeça', '''    cab.append(peca("bico_base", [-1.15, 23.9, -6.9], [1.15, 26.45, -5.3], mb, faixa=fb, res=4))
    cab.append(peca("bico_meio", [-0.95, 24.05, -8.5], [0.95, 26.2, -6.7], mb, rot=(-9, 0, 0), pivo=(0, 26.2, -6.7), faixa=fb, res=4))
    cab.append(peca("bico_ponta", [-0.7, 24.0, -9.8], [0.7, 25.75, -8.3], mb, rot=(-26, 0, 0), pivo=(0, 25.75, -8.3), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-0.85, 23.35, -7.9], [0.85, 24.1, -5.3], g.mat_cor(lambda p, f: (232, 158, 26), borda=.1),
                    rot=(5, 0, 0), pivo=(0, 23.7, -5.3), res=4))
    # barbela vermelha: 2 lobos redondos pendurados até o alto do peito
    mbar = g.mat_cor(lambda p, f: mix(VERM_ESC, VERM_VIVO, clamp((p[1] - 18.6) / 4.6)), borda=.06, curva=.35)
    for lado in (-1, 1):
        x0, x1 = sorted((0.05 * lado, 1.55 * lado))
        cab += g.arredondado("barbela_" + ("d" if lado < 0 else "e"), [x0, 19.0, -7.0], [x1, 23.6, -5.1], mbar, r=0.45,
                             faixa=(18.6, 23.6), res=4)
''')
rep("    if face in (\"east\", \"west\") and abs(z + 6.3) < 0.28 and abs(y - 25.6) < 0.22: return (150, 80, 20)   # narina",
    "    if face in (\"east\", \"west\") and abs(z + 6.4) < 0.26 and abs(y - 25.7) < 0.2: return (150, 80, 20)   # narina")
rep("    return mix((255, 210, 52), (244, 140, 24), clamp((-z - 6.4) / 2.4) * 0.85 + clamp((24.6 - y) / 2.0) * 0.25)",
    "    return mix((255, 214, 56), (246, 162, 30), clamp((-z - 7.2) / 2.6) * 0.8 + clamp((24.8 - y) / 2.0) * 0.2)")

# ---- 3. crista: 5 lâminas juntas sobre uma base contínua, todas varridas para trás como chamas; estreita de frente
troca_bloco('    filhos = [dedo("crista_c0"', '    filhos.append(peca("crista_base"', '''    filhos = [dedo(f"crista_c{k}", (0, 29.3, -3.4 + 1.85 * k), (34 + 3 * k, 0, 0), (7, 0, 0), kk, w=2.2, h=2.2)
              for k, kk in enumerate((0.72, 0.98, 1.1, 0.95, 0.72))]
''')
rep('''    filhos.append(peca("crista_base", [-1.7, 29.0, -4.4], [1.7, 30.6, 3.8],''', '''    filhos.append(peca("crista_base", [-1.2, 29.0, -4.4], [1.2, 30.5, 4.6],''')

# ---- 4. lanterna: bola logo abaixo do peito, entre as pernas, ~60% da largura do tronco
rep("LAN_C = (0.0, 10.6, 8.2)", "LAN_C = (0.0, 10.4, 4.6)")
rep("LAN_R = (6.2, 3.9, 6.8)", "LAN_R = (4.4, 4.3, 5.4)")
rep("xc = 3.4 * lado; zc = 3.4", "xc = 3.7 * lado; zc = 3.6")

# ---- 5. pescoço curto e grosso com juba; cabeça mais baixa; tocos laterais para dentro do tronco
rep("SOBE_CAB = -0.2", "SOBE_CAB = -1.5")
rep('''*g.arredondado("pescoco", [-3.2, 18.6, -4.6], [3.2, 23.8, 0.8], mpes, r=0.9, faixa=(17.0, 26.0)),''',
    '''*g.arredondado("pescoco", [-3.1, 18.6, -4.4], [3.1, 23.0, 1.2], mpes, r=0.9, faixa=(17.0, 26.0)),''')
rep('''*g.arredondado("pescoco_base", [-4.6, 17.4, -5.0], [4.6, 21.4, 2.0], mpes, r=1.3, faixa=(17.0, 26.0)),''',
    '''*g.arredondado("pescoco_base", [-3.9, 17.4, -4.8], [3.9, 20.6, 2.2], mpes, r=1.3, faixa=(17.0, 26.0)),
        *[g.pena_curva(f"juba{k}", (x_, 23.4 - 0.4 * abs(x_), 1.0), [(3.0, 2.2, 1.4, ROXO_MED, ROXO), (2.6, 1.8, 1.1, ROXO, ROXO_ESC)],
                       (rx_, 0, 0), (12, 0, 0), "-y", mat_pena_bloco, res=4)
          for k, (x_, rx_) in enumerate([(-1.6, -30), (1.6, -30), (0.0, -36)])],''')
rep("            x = (6.95 + dx) * lado", "            x = (6.45 + dx) * lado")
rep('''        corpo.append(osso("asa_" + s, [6.9 * lado, 18.0, -2.0], [0, 0, 0], asa))''', '''        corpo.append(osso("asa_" + s, [6.4 * lado, 18.0, -2.0], [0, 0, 0], asa))''')

# ---- 6. cabeça: bochechas em degraus, sem placa clara na testa (sobrancelhas viram lâminas para trás); asas em folha
rep('''    cab.append(peca("cranio_lados", [-4.2, 23.0, -3.4], [4.2, 29.4, 2.6], mc, faixa=fx, res=4))''',
    '''    cab.append(peca("cranio_lados", [-4.2, 23.9, -3.4], [4.2, 29.4, 2.6], mc, faixa=fx, res=4))
    cab.append(peca("bochecha", [-3.85, 23.0, -3.0], [3.85, 24.2, 2.2], mc, faixa=fx, res=4))''')
rep('''    for k, (y0, z0, z1, rx) in enumerate([(29.55, -3.6, 4.4, 4), (27.9, -1.0, 5.0, 8), (26.2, -0.6, 5.2, 12), (24.5, -0.4, 4.6, 16)]):''',
    '''    for k, (y0, z0, z1, rx) in enumerate([(29.55, -0.4, 4.6, 6), (27.9, 0.2, 5.0, 10), (26.2, 0.4, 5.2, 14), (24.5, 0.4, 4.6, 18)]):''')
rep('''            peca("sobrancelha_" + s, [fx0, 27.4, cz - 2.05], [fx1, 28.3, cz + 1.7], mat_placa_cabeca(),''',
    '''            peca("sobrancelha_" + s, [fx0, 27.4, cz - 2.05], [fx1, 28.3, cz + 3.4], mat_placa_cabeca(),''')
rep('''    if s < 0.6: return math.sqrt(max(0.0, 1 - ((s - 0.6) / 0.63) ** 2))
    return max(0.0, 1 - ((s - 0.6) / 0.4) ** 2) ** 0.6''', '''    if s < 0.5: return math.sqrt(max(0.0, 1 - ((s - 0.5) / 0.55) ** 2))
    return max(0.0, 1 - (s - 0.5) / 0.5) ** 0.75                       # ponta afilada (folha / limão)''')
open(p, 'w', encoding='utf-8').write(s)

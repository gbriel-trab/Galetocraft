p = 'ferramentas/especies/vagalo.py'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b)
# proporções: pescoço curto, cabeça maior, corpo mais largo e mais baixo
rep("SOBE_CAB = 1.6 ", "SOBE_CAB = -0.2")
rep("PESCOCO_FRENTE = 12 ", "PESCOCO_FRENTE = 6  ")
rep("K_CAB = 0.82 ", "K_CAB = 0.9  ")
rep("INCLINA = 5 ", "BAIXA = 2.0           # o corpo todo desce (pernas mais curtas)\nINCLINA = 5 ")
rep('''*g.arredondado("pescoco", [-2.8, 18.6, -4.6], [2.8, 25.2, 0.8], mpes, r=0.9, faixa=(17.0, 26.0)),''',
    '''*g.arredondado("pescoco", [-3.2, 18.6, -4.6], [3.2, 23.8, 0.8], mpes, r=0.9, faixa=(17.0, 26.0)),''')
rep('''*g.arredondado("pescoco_base", [-3.8, 17.6, -4.8], [3.8, 21.4, 1.8], mpes, r=1.2, faixa=(17.0, 26.0)),''',
    '''*g.arredondado("pescoco_base", [-4.6, 17.4, -5.0], [4.6, 21.4, 2.0], mpes, r=1.3, faixa=(17.0, 26.0)),''')
rep('''g.arredondado2("tronco", [-5.4, 11.0, -5.2], [5.4, 19.8, 10.6], mtr, r=3.4''', '''g.arredondado2("tronco", [-6.8, 11.0, -5.2], [6.8, 19.8, 10.6], mtr, r=3.6''')
rep('''g.arredondado("peito", [-3.8, 12.0, -5.4], [3.8, 19.4, -1.0], mtr, r=1.4''', '''g.arredondado("peito", [-5.0, 12.0, -5.4], [5.0, 19.4, -1.0], mtr, r=1.6''')
rep('''g.arredondado("garupa", [-3.6, 15.0, 8.0], [3.6, 19.0, 12.2], mtr, r=1.2''', '''g.arredondado("garupa", [-4.6, 15.0, 8.0], [4.6, 19.0, 12.2], mtr, r=1.4''')
rep('''    tronco = osso("corpo", [0, 10.5, 3.0], [INCLINA, 0, 0], corpo)''',
    '''    tronco = osso("corpo", [0, 10.5, 3.0], [INCLINA, 0, 0], corpo)
    g.transformar(0, [tronco], (0, 0, 0), 1.0, sobe=-BAIXA)''')
# lanterna: globo mais cheio, limão saturado com grade âmbar-clara
rep("LAN_C = (0.0, 10.2, 8.2)", "LAN_C = (0.0, 10.6, 8.2)")
rep("LAN_R = (5.2, 4.2, 6.6)", "LAN_R = (6.2, 3.9, 6.8)")
rep("LIMAO = (255, 225, 74); LIMAO_CLARO = (255, 242, 122); LIMAO_JUNTA = (236, 186, 34)",
    "LIMAO = (255, 216, 50); LIMAO_CLARO = (255, 238, 112); LIMAO_JUNTA = (234, 166, 24)")
rep("        k = math.sqrt(max(0.05, 1 - ((ym - cy) / ry) ** 2)) ** 0.8", "        k = math.sqrt(max(0.05, 1 - ((ym - cy) / ry) ** 2)) ** 0.55")
rep("        if dj < 0.16: cor = mix(LIMAO_JUNTA, cor, 0.25)", "        if dj < 0.16: cor = mix(LIMAO_JUNTA, cor, 0.15)")
# peito: mais largo e mais baixo, creme -> lilás nas beiradas
rep('''enumerate([(3.1, 17.3, 19.7, -6.2), (2.6, 15.2, 18.0, -6.7), (2.0, 13.1, 16.0, -6.9), (1.4, 11.3, 14.0, -6.6)])''',
    '''enumerate([(3.9, 16.8, 19.4, -6.3), (3.3, 14.7, 17.6, -6.7), (2.6, 12.6, 15.6, -6.9), (1.8, 10.8, 13.6, -6.6)])''')
rep('''        cor = mix(cor, CREME_SOMBRA, clamp((abs(x) - w + 1.0) / 1.2) * 0.6)''',
    '''        cor = mix(cor, mix(CREME_SOMBRA, MALVA, 0.5), clamp((abs(x) - w + 1.4) / 1.4) * 0.75)''')
# asa dobrada: 4 penas sobrepostas, cada uma com UMA ponta amarela
rep('''            x = (5.55 + dx) * lado''', '''            x = (6.95 + dx) * lado''')
rep('''mat_fileira_asa(z0, L, yc, H), res=4)]))''', '''mat_fileira_asa(z0, L, yc, H, n=1, faixa=0.3), res=4)]))''')
rep('''        corpo.append(osso("asa_" + s, [5.5 * lado, 18.0, -2.0], [0, 0, 0], asa))''', '''        corpo.append(osso("asa_" + s, [6.9 * lado, 18.0, -2.0], [0, 0, 0], asa))''')
rep('''        umax = 1 - 0.26 * t''', '''        umax = 1 - (0.26 * t if n > 1 else 0.45 * abs(v) ** 1.2)''')
# cauda: foices largas e grossas que sobem e caem até a altura da perna
rep('''        ang = -48 + 11 * k                      # cada uma ~11° mais baixa
        L = 13.0 - 1.0 * k
        cauda.append(foice(f"cauda{k}", (0.45 * lado * (k > 0), 18.8 - 0.5 * k, 10.8 - 0.2 * k), L, 3.0 - 0.15 * k,
                           (ang - INCLINA, (6 + 3 * k) * lado * (k > 0), 0), (14, 0, 0)))''',
    '''        ang = -42 + 9 * k                       # cada uma ~9° mais baixa
        L = 12.5 - 0.8 * k
        cauda.append(foice(f"cauda{k}", (0.6 * lado * (k > 0), 18.8 - 0.55 * k, 10.8 - 0.2 * k), L, 4.2 - 0.2 * k,
                           (ang - INCLINA, (5 + 3 * k) * lado * (k > 0), 0), (20, 0, 0), esp=0.9))''')
# asas de inseto: um pouco menores; células mais regulares; membrana dourada mais quente
rep('''(2.6 * lado, 20.4, 2.6), 19.0, 7.2, lado, (0, -36 * lado, 42 * lado), 1)''', '''(3.0 * lado, 20.2, 2.6), 17.0, 6.8, lado, (0, -36 * lado, 40 * lado), 1)''')
rep('''(2.6 * lado, 19.6, 4.4), 13.5, 5.4, lado, (0, -52 * lado, 16 * lado), 2)''', '''(3.0 * lado, 19.4, 4.4), 12.5, 5.2, lado, (0, -52 * lado, 14 * lado), 2)''')
rep("MEMB_RAIZ = (226, 196, 118); MEMB_PONTA = (238, 216, 146); MEMB_CLARA = (250, 238, 186)",
    "MEMB_RAIZ = (232, 190, 90); MEMB_PONTA = (244, 210, 118); MEMB_CLARA = (253, 232, 156)")
rep("rnd.uniform(-.3, .3)) * passo, (b + (0.5 if a % 2 else 0) + rnd.uniform(-.2, .2))", "rnd.uniform(-.12, .12)) * passo, (b + (0.5 if a % 2 else 0) + rnd.uniform(-.1, .1))")
# olho mais amarelo
rep("iris=((196, 118, 8), (250, 186, 24))", "iris=((214, 150, 10), (255, 210, 44))")
# barbela mais curta e larga
rep('''    cab.append(peca("barbela_a", [-1.4, 20.8, -6.9], [1.4, 23.4, -5.0], mbar, faixa=(19.0, 23.4), res=4))
    cab.append(peca("barbela_b", [-1.1, 19.2, -6.7], [1.1, 21.0, -5.2], mbar, faixa=(19.0, 23.4), res=4))''',
    '''    cab.append(peca("barbela_a", [-1.7, 21.6, -7.0], [1.7, 23.6, -5.0], mbar, faixa=(20.2, 23.6), res=4))
    cab.append(peca("barbela_b", [-1.35, 20.3, -6.8], [1.35, 21.8, -5.2], mbar, faixa=(20.2, 23.6), res=4))''')
# crista: dentes grossos em leque, o do meio mais alto; 3 se abrem de frente
a = s.index('    def dedo(nome, base, k, w=4.2, h=1.45):')
b = s.index('    filhos.append(peca("crista_base"')
s = s[:a] + '''    def dedo(nome, base, rot0, curva, k, w=2.6, h=2.4):
        segs = [(2.6 * k, w, h, VERM_ESC, VERM), (2.2 * k, w * .9, h * .9, VERM, VERM_VIVO), (1.2 * k, w * .8, h * .8, VERM_VIVO, LARANJA),
                (1.0 * k, w * .68, h * .7, AMARELO, AMAR_CLARO)]
        return g.pena_curva(nome, base, segs, rot0, curva, "y", mcr, brilho_ponta=True, res=4)
    filhos = [dedo("crista_c0", (0, 29.3, -3.3), (-12, 0, 0), (6, 0, 0), 0.72),
              dedo("crista_c1", (0, 29.4, -1.1), (8, 0, 0), (6, 0, 0), 1.15),
              dedo("crista_c2", (0, 29.3, 1.3), (32, 0, 0), (8, 0, 0), 0.95),
              dedo("crista_c3", (0, 29.0, 3.1), (56, 0, 0), (8, 0, 0), 0.72)]
    for lado in (-1, 1):
        filhos.append(dedo("crista_l_" + ("d" if lado < 0 else "e"), (1.5 * lado, 29.3, -0.4), (12, 0, -24 * lado), (6, 0, -6 * lado),
                           0.85, w=2.2, h=2.2))
''' + s[b:]
rep('''        if pc.nome.startswith(("asa", "cauda", "crista_c")) and pc.brilho is not True:''',
    '''        if pc.nome.startswith(("asa", "cauda", "crista_")) and pc.brilho is not True:''')
# tufos de penas atrás da cabeça (juba espetada da ficha), rentes aos lados
rep('''    cab.append(crista())
    return cab''', '''    for k, (y0, ry_) in enumerate([(28.0, 16), (26.0, 22)]):
        for lado in (-1, 1):
            cab.append(g.pena_curva(f"tufo{k}_{'d' if lado < 0 else 'e'}", (3.0 * lado, y0, 1.6),
                                    [(2.8, 1.7, 1.8, ROXO, ROXO_MED), (2.2, 1.1, 1.2, ROXO_MED, MALVA)],
                                    (-22 + 8 * k, ry_ * lado, 0), (10, 0, 0), "z", mat_pena_bloco, res=4))
    cab.append(crista())
    return cab''')
# pernas: mais curtas e grossas; dedos amarelos com só a garra roxa
rep('''pp += g.arredondado("coxa_" + s, [xc - 1.8, 6.4, zc - 1.8], [xc + 1.8, 10.6, zc + 1.8], mperna, r=0.6, faixa=(0, 10.6))''',
    '''pp += g.arredondado("coxa_" + s, [xc - 2.1, 5.0, zc - 2.1], [xc + 2.1, 8.6, zc + 2.1], mperna, r=0.7, faixa=(0, 8.6))''')
rep('''pp.append(peca("canela_" + s, [xc - 1.1, 1.2, zc - 1.1], [xc + 1.1, 6.8, zc + 1.1], mperna, faixa=(0, 10.6)))''',
    '''pp.append(peca("canela_" + s, [xc - 1.5, 1.2, zc - 1.5], [xc + 1.5, 5.4, zc + 1.5], mperna, faixa=(0, 8.6)))''')
rep('''                peca(f"dedo_{nome}_{s}", [x0 - .85, 0, z0 - 2.6], [x0 + .85, 1.4, z0 + 0.6], md, faixa=(0, 2.0)),
                peca(f"garra_{nome}_{s}", [x0 - .9, 0, z0 - 4.4], [x0 + .9, 1.6, z0 - 2.6], mg, faixa=(0, 2.0))]))''',
    '''                peca(f"dedo_{nome}_{s}", [x0 - .9, 0, z0 - 3.3], [x0 + .9, 1.5, z0 + 0.6], md, faixa=(0, 2.0)),
                peca(f"garra_{nome}_{s}", [x0 - .75, 0, z0 - 4.5], [x0 + .75, 1.2, z0 - 3.2], mg, faixa=(0, 2.0))]))''')
rep('''return osso("perna_" + s, [xc, 10.6, zc], [0, 0, 0], pp)''', '''return osso("perna_" + s, [xc, 8.6, zc], [0, 0, 0], pp)''')
rep("xc = 3.0 * lado; zc = 3.4", "xc = 3.4 * lado; zc = 3.4")
rep("ROSTO = ((0, 28.4, -2.2), 6.6)", "ROSTO = ((0, 26.0, -2.0), 7.0)")
open(p, 'w', encoding='utf-8').write(s)

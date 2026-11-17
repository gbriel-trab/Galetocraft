p = 'ferramentas/especies/vagalo.py'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b)
rep("INCLINA = 18 ", "INCLINA = 24 ")
# abdômen: placas maiores, sem quadrado claro, brilho do centro para a junta
rep('''        T = 1.9                                                     # lado de cada placa''',
    '''        T = 2.8                                                     # lado de cada placa''')
rep('''        if dj < 0.11: cor = (226, 132, 14)
        else: cor = mix((255, 178, 12), (255, 228, 64), clamp((dj - 0.14) / 0.55))''',
    '''        if dj < 0.13: cor = (222, 128, 12)
        else: cor = mix((250, 160, 14), (255, 230, 70), clamp((dj - 0.13) / (T / 2 - 0.13)) ** 0.8)''')
rep('''    corpo += g.arredondado2("abdomen", [-5.9, 3.8, -1.8], [5.9, 14.2, 12.4], mat_abdomen(), r=3.7, brilho=True)''',
    '''    corpo += g.arredondado2("abdomen", [-5.9, 3.8, 0.4], [5.9, 14.2, 12.6], mat_abdomen(), r=4.2, brilho=True)''')
rep('''    corpo += g.arredondado("abdomen_meio", [-5.1, 4.8, -0.8], [5.1, 13.2, 11.4], mat_abdomen(), r=2.3, brilho=True)''',
    '''    corpo += g.arredondado("abdomen_meio", [-5.2, 4.6, 1.1], [5.2, 13.4, 11.9], mat_abdomen(), r=2.6, brilho=True)
    corpo += g.arredondado("abdomen_fora", [-4.3, 3.9, 2.0], [4.3, 14.1, 11.0], mat_abdomen(), r=1.0, brilho=True)''')
rep("ex, ey, ez = x / 5.9, (y - 9.0) / 5.2, (z - 5.3) / 7.1", "ex, ey, ez = x / 5.9, (y - 9.0) / 5.2, (z - 6.5) / 6.1")
rep("z - 4.9) / T + 0.5\n        if face", "z - 6.5) / T + 0.5\n        if face")
rep("fy = (z - 4.9) / T + 0.5", "fy = (z - 6.5) / T + 0.5")
# tronco: ombros afinando
rep('''corpo += g.arredondado2("tronco", [-5.8, 10.8, -4.7], [5.8, 20.0, 7.9], mtr, r=2.8''',
    '''corpo += g.arredondado2("tronco", [-5.6, 10.8, -4.7], [5.6, 20.0, 7.9], mtr, r=3.4''')
# asa dobrada: 25% mais curta, apontando para a cauda, faixa amarela maior
rep('''enumerate([(-6, 9.6, 0.0, 0.0), (-3, 11.0, 0.25, -1.6), (0, 12.0, 0.5, -3.2), (3, 11.6, 0.7, -4.8),
                                             (7, 10.0, 0.9, -6.2)])''',
    '''enumerate([(-8, 7.4, 0.0, 0.0), (-6, 8.4, 0.25, -1.45), (-4, 9.0, 0.5, -2.9), (-2, 8.6, 0.7, -4.35),
                                             (0, 7.6, 0.9, -5.6)])''')
rep('''            segs = [(L * .4, 1.0, 2.2, ROXO_ESC, ROXO), (L * .3, 0.9, 2.0, ROXO, ROXO_MED), (L * .18, 0.8, 1.7, AMARELO, AMARELO),
                    (L * .12, 0.7, 1.0, AMARELO, AMAR_CLARO)]''',
    '''            segs = [(L * .3, 1.0, 2.0, ROXO_ESC, ROXO), (L * .25, 0.9, 1.9, ROXO, ROXO_MED), (L * .27, 0.8, 1.6, AMARELO, AMARELO),
                    (L * .18, 0.7, 1.0, AMARELO, AMARELO)]''')
rep('''asa += g.arredondado2("ombro_" + s, [x0, 13.6, -3.0], [x1, 19.8, 2.4]''', '''asa += g.arredondado2("ombro_" + s, [x0, 14.4, -3.0], [x1, 19.8, 2.4]''')
# cauda: arco +35 -> 0 -> -35 (somando a inclinação do corpo), raiz mais alta, leque aberto
rep('''                (2.0 * k, 1.0, 2.2, ROXO, AMBAR), (2.0 * k, 0.85, 1.8, AMARELO, AMARELO), (1.6 * k, 0.65, 1.1, AMARELO, AMAR_CLARO)]''',
    '''                (2.0 * k, 1.0, 2.2, ROXO, AMBAR), (2.0 * k, 0.85, 1.8, AMARELO, AMARELO), (1.6 * k, 0.65, 1.1, AMARELO, AMARELO)]''')
rep('''    cauda.append(pena_cauda("cauda_meio", (0, 19.0, 6.8), (-48, 0, 0), (14, 0, 0), 1.4))''',
    '''    cauda.append(pena_cauda("cauda_meio", (0, 21.0, 6.4), (-35 - INCLINA, 0, 0), (14, 0, 0), 1.4))''')
rep('''        cauda.append(pena_cauda("cauda1_" + s, (1.4 * lado, 18.4, 7.0), (-40, 16 * lado, 0), (13, 0, 0), 1.3))
        cauda.append(pena_cauda("cauda2_" + s, (2.5 * lado, 17.4, 7.0), (-30, 30 * lado, 0), (12, 0, 0), 1.15))''',
    '''        cauda.append(pena_cauda("cauda1_" + s, (1.5 * lado, 20.4, 6.6), (-32 - INCLINA, 16 * lado, 14 * lado), (14, 0, 0), 1.3))
        cauda.append(pena_cauda("cauda2_" + s, (2.6 * lado, 19.4, 6.8), (-26 - INCLINA, 30 * lado, 26 * lado), (13, 0, 0), 1.15))''')
# asas de inseto
rep("VEIA = (255, 214, 74); BORDA_ASA = (255, 232, 120)", "VEIA = (255, 232, 110); BORDA_ASA = (255, 238, 140)")
rep("if borda < 0.4: return BORDA_ASA", "if borda < 0.6: return BORDA_ASA")
rep("if borda < 0.52: return AMBAR", "if borda < 0.74: return AMBAR")
rep("if d2 - d1 < 0.24: return VEIA", "if d2 - d1 < 0.3: return VEIA")
# cabeça: espetos mais para trás
rep("(rx, 30 * lado, 0), (6, 8 * lado, 0), \"z\", mpc, res=4))", "(rx, 50 * lado, 0), (6, 8 * lado, 0), \"z\", mpc, res=4))")
open(p, 'w', encoding='utf-8').write(s)

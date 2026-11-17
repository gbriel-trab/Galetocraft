p = 'ferramentas/especies/vagalo.py'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b)
rep('''                       g.mat_cor(lambda p, f: mix(VERM_ESC, VERM, clamp((p[1] - 29.0) / 1.6)), borda=.1), res=4))
''', '''                       g.mat_cor(lambda p, f: mix(VERM_ESC, VERM, clamp((p[1] - 29.0) / 1.6)), borda=.1), res=4))
    for lado in (-1, 1):                          # dedos dos lados, mais baixos: crista larga e em degraus de frente
        s = "d" if lado < 0 else "e"
        filhos.append(coluna("crista_l1_" + s, (2.0 * lado, 29.2, -1.8), (6, 0, -14 * lado), (8, 0, -4 * lado), 0.78, w=2.2, h=2.4))
        filhos.append(coluna("crista_l2_" + s, (1.9 * lado, 29.1, 1.2), (34, 0, -14 * lado), (10, 0, -4 * lado), 0.7, w=2.0, h=2.2))
''')
rep('''        if dj < 0.14: cor = (204, 106, 10)''', '''        if dj < 0.11: cor = (226, 132, 14)''')
rep('''corpo += g.arredondado2("abdomen", [-6.5, 3.8, -1.8], [6.5, 14.2, 12.4], mat_abdomen(), r=3.9, brilho=True)''',
    '''corpo += g.arredondado2("abdomen", [-5.9, 3.8, -1.8], [5.9, 14.2, 12.4], mat_abdomen(), r=3.7, brilho=True)''')
rep('''corpo += g.arredondado("abdomen_meio", [-5.6, 4.8, -0.8], [5.6, 13.2, 11.4], mat_abdomen(), r=2.4, brilho=True)''',
    '''corpo += g.arredondado("abdomen_meio", [-5.1, 4.8, -0.8], [5.1, 13.2, 11.4], mat_abdomen(), r=2.3, brilho=True)''')
rep("ex, ey, ez = x / 6.5,", "ex, ey, ez = x / 5.9,")
rep('''    cauda.append(pena_cauda("cauda_meio", (0, 19.0, 6.8), (-40, 0, 0), (15, 0, 0), 1.15))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cauda.append(pena_cauda("cauda1_" + s, (1.3 * lado, 18.4, 7.0), (-34, 16 * lado, 0), (14, 0, 0), 1.05))
        cauda.append(pena_cauda("cauda2_" + s, (2.4 * lado, 17.4, 7.0), (-24, 32 * lado, 0), (13, 0, 0), 0.92))''',
'''    cauda.append(pena_cauda("cauda_meio", (0, 19.4, 6.6), (-62, 0, 0), (17, 0, 0), 1.3))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cauda.append(pena_cauda("cauda1_" + s, (1.4 * lado, 18.8, 6.8), (-54, 18 * lado, 0), (16, 0, 0), 1.2))
        cauda.append(pena_cauda("cauda2_" + s, (2.5 * lado, 17.8, 6.9), (-44, 36 * lado, 0), (15, 0, 0), 1.05))''')
open(p, 'w', encoding='utf-8').write(s)

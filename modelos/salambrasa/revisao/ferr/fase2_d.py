from pathlib import Path
p = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\salambrasa.py"); s = p.read_text(encoding="utf-8")
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:150]
    s = s.replace(a, b)
rep('''PLACA = (250, 128, 40); PLACA_CLARA = (254, 170, 80); PLACA_ESC = (214, 76, 18)''',
    '''PLACA = (255, 146, 56); PLACA_CLARA = (255, 194, 118); PLACA_ESC = (232, 104, 34)''')
rep('''        (2.8, 24.2, -19.8, -90, 6, 40, 6.8, 3.4, C1),       # 'babador' de frente, abrindo para os lados
        (4.2, 25.0, -16.8, -40, 38, 30, 9.0, 3.8, C1),      # leque dos lados: abre bem para fora
        (4.6, 25.2, -13.6, 5, 42, 40, 9.6, 4.0, C1),
        (3.8, 25.4, -10.8, 55, 36, 52, 9.0, 3.8, C2),
        (4.6, 22.0, -16.0, -30, 46, 22, 8.0, 3.6, C2),
        (4.8, 21.8, -12.6, 15, 50, 32, 8.4, 3.8, C3),
        (4.2, 21.6, -9.8, 60, 40, 44, 7.6, 3.4, C3),
        (4.4, 19.0, -14.8, -10, 56, 20, 6.6, 3.4, C3),''',
'''        (2.8, 24.2, -19.8, -90, 6, 34, 6.4, 3.4, C1),       # 'babador' de frente, abrindo para os lados
        (4.2, 25.2, -16.6, -30, 24, 34, 9.0, 3.8, C1),      # leque dos lados e de trás, varrendo para trás
        (4.6, 25.4, -13.6, 10, 26, 46, 10.0, 4.0, C1),
        (3.8, 25.6, -10.6, 55, 24, 58, 9.6, 3.8, C2),
        (4.6, 22.6, -14.4, -5, 30, 34, 8.6, 3.8, C2),
        (4.4, 22.4, -11.0, 35, 28, 46, 8.8, 3.8, C3),
        (3.6, 22.0, -8.8, 70, 24, 54, 8.0, 3.4, C3),''')
rep('''        for k, (xa, xb, y0, y1, z0, z1, inc) in enumerate([(1.8, 4.2, 30.9, 33.8, -21.0, -17.0, 4),
                                                           (1.8, 3.8, 30.7, 34.8, -15.4, -11.4, 12)]):''',
'''        for k, (xa, xb, y0, y1, z0, z1, inc) in enumerate([(1.8, 4.8, 30.9, 34.0, -21.0, -17.0, 4),
                                                           (1.8, 4.2, 30.7, 35.0, -15.4, -11.4, 12)]):''')
rep('''    for k, (yb, ya, w) in enumerate([(22.4, 24.6, 3.0), (20.3, 22.6, 3.6), (18.2, 20.5, 4.2), (16.1, 18.4, 4.6),
                                     (14.0, 16.3, 4.7), (11.9, 14.2, 4.4), (9.8, 12.1, 3.8)]):''',
'''    for k, (yb, ya, w) in enumerate([(22.4, 24.6, 3.2), (20.3, 22.6, 3.9), (18.2, 20.5, 4.5), (16.1, 18.4, 4.9),
                                     (14.0, 16.3, 5.0), (11.9, 14.2, 4.7), (9.8, 12.1, 4.0)]):''')
rep('''    faixa = g.mat_cor(lambda p, f: mix(LARANJA_ESC, AMARELO, clamp((p[1] - 4.6) / 2.8)), borda=.06, curva=.2)''',
    '''    faixa = g.mat_cor(lambda p, f: mix(LARANJA_ESC, AMARELO, clamp((p[1] - 3.8) / 4.6)), borda=.04, curva=.1)''')
rep('''    pp += g.octogono(nome + "_faixa", [xc - 2.25, 4.6, zc - 2.25], [xc + 2.25, 7.6, zc + 2.25], faixa, r=0.7)
    pp += g.octogono(nome + "_tornozelo", [xc - 2.35, 2.4, zc - 2.35], [xc + 2.35, 4.8, zc + 2.35], escuro, r=0.7)''',
'''    pp += g.octogono(nome + "_faixa", [xc - 2.35, 4.0, zc - 2.35], [xc + 2.35, 8.4, zc + 2.35], faixa, r=0.7)
    pp += g.octogono(nome + "_tornozelo", [xc - 2.45, 2.4, zc - 2.45], [xc + 2.45, 4.2, zc + 2.45], escuro, r=0.7)''')
p.write_text(s, encoding="utf-8"); print("ok")

p = 'ferramentas/especies/vagalo.py'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b)
rep("INCLINA = 18 ", "INCLINA = 12 ")
rep("z - 6.5) / T + 0.5\n", "z - 8.6) / T + 0.5\n")
rep("(z - 6.5) / 6.1", "(z - 8.6) / 6.6")
rep('''g.arredondado2("tronco", [-5.6, 10.8, -4.7], [5.6, 20.0, 7.9], mtr, r=3.4''', '''g.arredondado2("tronco", [-5.6, 10.8, -4.7], [5.6, 20.0, 10.0], mtr, r=3.4''')
rep('''g.arredondado2("abdomen", [-5.9, 3.8, 0.4], [5.9, 14.2, 12.6], mat_abdomen(), r=4.2''', '''g.arredondado2("abdomen", [-5.9, 4.4, 2.0], [5.9, 14.2, 15.2], mat_abdomen(), r=4.2''')
rep('''peca("dorso_baixo", [-3.4, 11.2, 4.0], [3.4, 14.4, 9.6]''', '''peca("dorso_baixo", [-3.4, 11.2, 4.0], [3.4, 14.4, 11.6]''')
rep('''g.arredondado("abdomen_meio", [-5.2, 4.6, 1.1], [5.2, 13.4, 11.9]''', '''g.arredondado("abdomen_meio", [-5.2, 5.2, 2.7], [5.2, 13.4, 14.5]''')
rep('''g.arredondado("abdomen_fora", [-4.3, 3.9, 2.0], [4.3, 14.1, 11.0]''', '''g.arredondado("abdomen_fora", [-4.3, 4.5, 3.6], [4.3, 14.1, 13.6]''')
rep("g.anel(5.6, 6.4, 1.6, phi, lado)", "g.anel(5.6, 7.4, 2.6, phi, lado)")
rep("g.anel(5.6, 6.4, 1.6, 90, 1)", "g.anel(5.6, 7.4, 2.6, 90, 1)")
rep('''pena_cauda("cauda_meio", (0, 21.0, 6.4)''', '''pena_cauda("cauda_meio", (0, 20.6, 8.6)''')
rep('''pena_cauda("cauda1_" + s, (1.5 * lado, 20.4, 6.6)''', '''pena_cauda("cauda1_" + s, (1.5 * lado, 20.0, 8.8)''')
rep('''pena_cauda("cauda2_" + s, (2.6 * lado, 19.4, 6.8)''', '''pena_cauda("cauda2_" + s, (2.6 * lado, 19.0, 9.0)''')
rep('''osso("cauda", [0, 17.0, 6.8]''', '''osso("cauda", [0, 18.0, 8.8]''')
rep('''(3.8 * lado, 19.8, 3.0), 17.0, 7.0''', '''(3.8 * lado, 19.8, 3.6), 17.0, 7.0''')
rep('''(3.6 * lado, 18.0, 4.6), 12.5, 5.4''', '''(3.6 * lado, 18.0, 5.4), 12.5, 5.4''')
rep("xc = 3.0 * lado; zc = 4.2", "xc = 3.0 * lado; zc = 4.6")
open(p, 'w', encoding='utf-8').write(s)

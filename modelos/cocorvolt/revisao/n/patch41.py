from pathlib import Path
P = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\cocorvolt.py")
s = P.read_text(encoding="utf-8")
def rp(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b)
# bico: cunha que afina para baixo também de frente (topo largo, parte de baixo mais estreita, gancho estreito)
rp('''    cab.append(peca("bico_base", [-1.35, 28.1, zb - 1.6], [1.35, 30.0, zb], mb, faixa=fb, res=4))
    cab.append(peca("bico_meio", [-1.1, 28.0, zb - 2.6], [1.1, 29.75, zb - 1.5], mb, faixa=fb, res=4))''',
   '''    cab.append(peca("bico_base", [-1.4, 29.0, zb - 1.7], [1.4, 30.0, zb], mb, faixa=fb, res=4))
    cab.append(peca("bico_base_baixo", [-0.95, 28.1, zb - 1.6], [0.95, 29.1, zb], mb, faixa=fb, res=4))
    cab.append(peca("bico_meio", [-1.1, 28.4, zb - 2.6], [1.1, 29.8, zb - 1.55], mb, faixa=fb, res=4))''')
# barbela: dois lóbulos separados por um vão, tamanhos diferentes
rp('''    for lado, y_fim in ((-1, 23.0), (1, 23.8)):
        x0, x1 = sorted((0.05 * lado, 1.05 * lado))''',
   '''    for lado, y_fim in ((-1, 22.8), (1, 24.2)):
        x0, x1 = sorted((0.16 * lado, 1.1 * lado))''')
# cauda: penas mais altas (sem vãos), leque menos aberto e lâminas curvando mais para cima
rp('''        ang = 40 - 78 * t
        y = 18.0 - 4.2 * t''', '''        ang = 36 - 66 * t
        y = 18.4 - 5.0 * t''')
rp('''    H = [4.2, 3.0, 1.8]; F = [0.44, 0.33, 0.23]; W = [2.4, 2.0, 1.5]''',
   '''    H = [5.2, 4.0, 2.6]; F = [0.44, 0.33, 0.23]; W = [2.4, 2.0, 1.5]''')
rp('''        return osso(f"{nome}_{k}", [x, y, pz], list(rot0) if k == 0 else [-6, 0, 0], filhos)''',
   '''        return osso(f"{nome}_{k}", [x, y, pz], list(rot0) if k == 0 else [-8, 0, 0], filhos)''')
P.write_text(s, encoding="utf-8"); print("ok")

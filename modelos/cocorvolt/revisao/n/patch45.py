from pathlib import Path
P = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\cocorvolt.py")
s = P.read_text(encoding="utf-8")
def rp(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b)
def troca(ini, fim, novo):
    global s
    a = s.index(ini); b = s.index(fim, a + len(ini))
    s = s[:a] + novo + s[b:]
# bico: cunha em 3 camadas (a de cima é a mais larga e a que mais avança), gancho na ponta descendo DENTRO do volume
troca('''    cab.append(peca("bico_base",''', '''    # barbela''', '''    BICO_ = [  # (meia largura, y0, y1, avanço)
        (1.45, 29.25, 30.05, 3.0), (1.15, 28.5, 29.35, 2.6), (0.8, 27.8, 28.6, 1.8)]
    for k, (w, y0, y1, d) in enumerate(BICO_):
        cab.append(peca(f"bico_{k}", [-w, y0, zb - d], [w, y1, zb], mb, faixa=fb, res=4))
    cab.append(peca("bico_gancho", [-0.6, 27.9, zb - 3.45], [0.6, 29.9, zb - 2.6], mb, rot=(-12, 0, 0),
                    pivo=(0, 29.9, zb - 2.6), faixa=fb, res=4))
''')
# barbela mais encorpada (lóbulos em gota), logo abaixo do bico
rp('''    zw = zb - 0.9
    for lado, y_fim in ((-1, 22.8), (1, 24.2)):
        x0, x1 = sorted((0.1 * lado, 1.35 * lado))
        cab += arredondado("barbela_" + ("d" if lado < 0 else "e"), [x0, y_fim, zw - 0.7], [x1, 27.7, zw + 0.65], mbar,
                           r=0.5, res=4)''',
   '''    zw = zb - 0.9
    for lado, y_fim in ((-1, 22.8), (1, 24.0)):
        x0, x1 = sorted((0.08 * lado, 1.4 * lado))
        cab += arredondado("barbela_" + ("d" if lado < 0 else "e"), [x0, y_fim, zw - 0.8], [x1, 27.9, zw + 0.8], mbar,
                           r=0.35, res=4)''')
# olho: halo azul elétrico (brilha) logo em volta da fenda
rp('''    if abs(u) > W2 or v < H0 or v > topo:
        return (44, 46, 54) if v > H0 - 0.05 else (96, 96, 104)
    du, dv = (W2 - abs(u)) / W2, min(v - H0, topo - v) / (topo - H0)
    d = min(du * 2.2, dv * 2.4)''',
   '''    if abs(u) > W2 or v < H0 or v > topo:
        if abs(u) < W2 + 0.13 and H0 - 0.13 < v < topo + 0.13: return OLHO_BORDA      # halo elétrico
        return (44, 46, 54) if v > H0 - 0.05 else (96, 96, 104)
    du, dv = (W2 - abs(u)) / W2, min(v - H0, topo - v) / (topo - H0)
    d = min(du * 2.2, dv * 2.4)''')
P.write_text(s, encoding="utf-8"); print("ok")

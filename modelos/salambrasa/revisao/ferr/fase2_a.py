from pathlib import Path
p = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\salambrasa.py"); s = p.read_text(encoding="utf-8")
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:120]
    s = s.replace(a, b)

# ---------- paleta amostrada da ficha ----------
rep(s[s.index("# ---------------- paleta (da ficha)"):s.index("# ---------------- manchas incandescentes")],
'''# ---------------- paleta (amostrada com PIL na ficha: Paleta de Cores, _arte e _vistas) ----------------
GRAFITE = (100, 44, 58); GRAFITE_ESC = (66, 26, 38); GRAFITE_CLARO = (128, 66, 82)      # corpo ameixa (arte 99,45,58)
CABECA = (116, 64, 80); CABECA_CLARA = (146, 92, 108); CABECA_ESC = (78, 40, 54)        # cabeça (arte 110,57,72)
FACE = (150, 100, 114); FACE_CLARA = (176, 124, 136)                                     # malva clara em volta do olho
VISEIRA = (118, 66, 82); VISEIRA_CLARA = (152, 98, 114); VISEIRA_ESC = (78, 40, 54)
BICO = (150, 90, 104); BICO_CLARO = (178, 120, 132); BICO_ESC = (108, 62, 76)           # malva (arte 150,87,97)
DEDO = (170, 104, 118); DEDO_CLARO = (200, 140, 152); DEDO_ESC = (128, 74, 88)          # arte 167,99,113
CRISTA = (220, 30, 30); CRISTA_ESC = (168, 18, 24); CRISTA_CLARA = (251, 83, 82)         # paleta 202,24,30 / topo 251,83,82
VERM = (226, 40, 26); VERM_ESC = (176, 22, 22)
LARANJA = (253, 115, 2); LARANJA_ESC = (253, 69, 11); AMARELO = (254, 201, 37); AMARELO_CLARO = (255, 226, 110)
PLACA = (250, 128, 40); PLACA_CLARA = (254, 170, 80); PLACA_ESC = (214, 76, 18)           # arte 240,112,40
CREME = (254, 229, 215)
BRASA_MIOLO = (255, 230, 90); BRASA = (253, 206, 0); BRASA_BORDA = (253, 120, 10)

''')

# ---------- manchas em coordenadas do mundo (cauda): hexágono no plano visto na vista certa ----------
rep('''def mat_com_manchas(cor_fn, lista, **kw):''',
'''def hexa(a, b):
    """Cor do hexágono (a, b normalizados) ou None."""
    d = max(abs(b) / 0.87, abs(a) + abs(b) * 0.58)
    if d > 1: return None
    return BRASA_MIOLO if d < 0.45 else BRASA if d < 0.8 else BRASA_BORDA

# manchas da cauda medidas na ficha (vista lateral: centro z, y, largura, altura; vista de trás: x, y, largura, altura)
MANCHAS_CAUDA_LADO = [(25.9, 13.5, 2.6, 3.2), (25.6, 21.9, 3.4, 4.2), (22.4, 17.2, 2.6, 3.2), (19.7, 26.6, 4.2, 3.2),
                      (18.0, 14.0, 3.0, 2.2), (13.0, 14.2, 3.2, 2.4), (12.8, 28.8, 3.4, 2.0), (8.0, 28.0, 2.4, 2.0)]
MANCHAS_CAUDA_TRAS = [(0.0, 17.9, 4.6, 5.4), (0.0, 10.6, 3.6, 3.0), (0.0, 23.2, 2.8, 1.6),
                      (-4.6, 21.3, 2.2, 3.0), (4.6, 21.3, 2.2, 3.0), (-4.8, 14.7, 1.6, 2.4), (4.8, 14.7, 1.6, 2.4)]
MANCHAS_CAUDA_CIMA = [(0.0, 18.6, 3.2, 2.6), (0.0, 13.0, 3.0, 2.4)]          # (x, z, largura, comprimento) no alto do gancho

def mancha_cauda(pw, nw):
    x, y, z = pw
    if abs(nw[0]) > 0.7:
        for zc, yc, L, H in MANCHAS_CAUDA_LADO:
            c = hexa((z - zc) / (L / 2), (y - yc) / (H / 2))
            if c: return c
    if nw[2] > 0.4:
        for xc, yc, L, H in MANCHAS_CAUDA_TRAS:
            c = hexa((x - xc) / (L / 2), (y - yc) / (H / 2))
            if c: return c
    if nw[1] > 0.6 and y > 24:
        for xc, zc, L, C in MANCHAS_CAUDA_CIMA:
            c = hexa((x - xc) / (L / 2), (z - zc) / (C / 2))
            if c: return c
    return None

def mat_com_manchas(cor_fn, lista, **kw):''')

# ---------- cauda: cor base + manchas do mundo ----------
a = s.index("def mat_rabo(w, h, py, z0, L, k):"); b = s.index("def secao(")
rep(s[a:b], '''def rot_x(q, o, ang):
    """Gira o ponto q (x, y, z) em volta do eixo x que passa por o, como o Blockbench (positivo = frente para baixo)."""
    c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    dy, dz = q[1] - o[1], q[2] - o[2]
    return (q[0], o[1] + dy * c - dz * s_, o[2] + dy * s_ + dz * c)

def mat_rabo(w, h, py, z0, L, k, cadeia):
    """Segmento da cauda. Base: dorso ameixa e barriga laranja embaixo; no gancho a faixa laranja corre por fora da
    curva (atrás) e por dentro (em cima). As manchas são desenhadas no MUNDO, onde a ficha as mostra: o ponto é levado
    pela 'cadeia' de giros [(origem, ângulo), ...] (da peça até a raiz da cauda)."""
    base = k < 4
    def cor(p, face):
        x, y, z = p
        v = (y - (py - h / 2)) / h
        if base:
            if face == "down": return PLACA
            if v < 0.2: return LARANJA
            if v < 0.28: return LARANJA_ESC
            return GRAFITE
        if face == "down": return GRAFITE
        if face == "up": return LARANJA if abs(x) < 0.2 * w else GRAFITE
        if k < 7:
            if v < 0.16: return LARANJA
            if v < 0.24: return LARANJA_ESC
            return GRAFITE
        if v > 0.84: return LARANJA
        if v > 0.76: return LARANJA_ESC
        return GRAFITE
    fundo = g.mat_cor(cor, borda=.0, curva=.3)
    def mundo(c):
        pw = c["p"]; n = g.NORMAL[c["face"]]; nw = n
        for o, ang in cadeia:
            pw = rot_x(pw, o, ang); nw = rot_x(nw, (0, 0, 0), ang)
        return mancha_cauda(pw, nw)
    def f(c):
        return mundo(c) or fundo(c)
    return f, (lambda c, cor_: mundo(c) is not None)

''')
rep('''        mat, br = mat_rabo(w, h, py, pz, L, k)
        filhos = secao(f"{nome}_{k}", px, py, pz - (0.8 if k == 0 else 0.3), pz + L, w, h, mat, br)
        if k > 0:
            wp, hp = (segs[k - 1][1] + w) / 2, (segs[k - 1][2] + h) / 2
            e = 0.5 + (hp / 2) * math.tan(math.radians(abs(rx) / 2))
            filhos += secao(f"{nome}_{k}_junta", px, py, pz - e, pz + e, wp, hp, mat, br, rot=(-rx / 2, 0, 0), pivo=(px, py, pz))
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py, pz + L)))
        else:
            filhos += secao(f"{nome}_ponta", px, py, pz + L - 0.2, pz + L + 1.2, w * 0.74, h * 0.74, mat, br)''',
'''        cad = [((px, py, pz), rx)] + cadeia_pai
        mat, br = mat_rabo(w, h, py, pz, L, k, cad)
        filhos = secao(f"{nome}_{k}", px, py, pz - (0.8 if k == 0 else 0.3), pz + L, w, h, mat, br)
        if k > 0:
            wp, hp = (segs[k - 1][1] + w) / 2, (segs[k - 1][2] + h) / 2
            e = 0.5 + (hp / 2) * math.tan(math.radians(abs(rx) / 2))
            mj, bj = mat_rabo(wp, hp, py, pz, L, k, [((px, py, pz), -rx / 2)] + cad)
            filhos += secao(f"{nome}_{k}_junta", px, py, pz - e, pz + e, wp, hp, mj, bj, rot=(-rx / 2, 0, 0), pivo=(px, py, pz))
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py, pz + L), cad))
        else:
            filhos += secao(f"{nome}_ponta", px, py, pz + L - 0.2, pz + L + 1.2, w * 0.74, h * 0.74, mat, br)''')
rep('''    def seg(k, pos):
        L, w, h, rx = segs[k]''', '''    def seg(k, pos, cadeia_pai):
        L, w, h, rx = segs[k]''')
rep('''    return seg(0, base)
''', '''    return seg(0, base, [])
''')

# ---------- manchas do corpo onde a ficha mostra ----------
a = s.index("MANCHAS_CORPO = ["); b = s.index("def mat_placa(c):")
rep(s[a:b], '''MANCHAS_CORPO = [((0, 22.8, -6.6), (2.4, 1, 2.0), 1.2), ((0, 22.0, 0.8), (2.6, 1, 2.2), 1.2), ((0, 20.4, 7.6), (2.4, 1, 2.0), 1.2)]
for lado in (-1, 1):   # posições medidas na vista lateral da ficha (z, y)
    MANCHAS_CORPO += [((5.9 * lado, 14.3, 1.2), (1, 1.4, 1.8), 1.2),        # flanco, grande
                      ((5.9 * lado, 11.9, -2.2), (1, 0.9, 0.8), 1.2),       # flanco, pequena
                      ((5.6 * lado, 11.6, 5.4), (1, 0.8, 0.8), 1.2),
                      ((4.7 * lado, 19.4, -2.2), (1, 1.0, 1.9), 1.3),       # alto do dorso
                      ((4.4 * lado, 18.2, 5.0), (1, 1.2, 1.9), 1.3)]

''')
p.write_text(s, encoding="utf-8")
print("ok")

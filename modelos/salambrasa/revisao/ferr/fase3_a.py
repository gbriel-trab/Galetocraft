from pathlib import Path
p = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\salambrasa.py"); s = p.read_text(encoding="utf-8")
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:160]
    s = s.replace(a, b)

# ---------------- paleta: quadros da Paleta de Cores da _ficha ----------------
a = s.index("# ---------------- paleta"); b = s.index("# ---------------- manchas incandescentes")
rep(s[a:b], '''# ---------------- paleta: quadros da Paleta de Cores da _ficha (amostrados com PIL) ----------------
# carvão (46,35,44) · cinza-roxo (103,78,95) · malva (131,94,111) · vermelho (202,24,30) · laranja-vermelho (253,69,11)
# laranja (253,115,2) · amarelo (254,201,37) · creme (251,223,198)
GRAFITE = (66, 51, 62); GRAFITE_ESC = (46, 35, 44); GRAFITE_CLARO = (87, 70, 80)        # corpo carvão-arroxeado
CABECA = (82, 64, 76); CABECA_CLARA = (103, 78, 95); CABECA_ESC = (58, 46, 54)          # cabeça carvão-malva
FACE = (96, 74, 88)                                                                       # um pouco mais clara sob o olho
VISEIRA = (60, 47, 56); VISEIRA_CLARA = (84, 66, 78); VISEIRA_ESC = (46, 35, 44)         # sobrancelha/capacete mais escura
BICO = (131, 94, 111); BICO_CLARO = (150, 116, 130); BICO_ESC = (100, 72, 86)            # malva
DEDO = (180, 162, 172); DEDO_CLARO = (204, 190, 198); DEDO_ESC = (146, 128, 140)         # lavanda-acinzentado claro
CRISTA = (224, 40, 40); CRISTA_ESC = (176, 24, 28); CRISTA_CLARA = (240, 72, 72)         # vermelho vivo, topo mais claro
VERM = (200, 40, 32); VERM_ESC = (170, 26, 24)
LARANJA = (240, 112, 32); LARANJA_ESC = (253, 69, 11); AMARELO = (248, 176, 32); OURO = (248, 192, 32)
PLACA = (244, 160, 80); PLACA_CLARA = (250, 184, 112); PLACA_ESC = (208, 106, 32)         # escudo do peito / barriga
VENTRE = (232, 138, 48)
CREME = (244, 230, 220)
BRASA = (248, 192, 32); BRASA_BORDA = (240, 112, 32)                                     # manchas: amarelo cheio, borda laranja

def escurecer(c, f):
    """Escurece mantendo o matiz (sem puxar para o oliva)."""
    return tuple(int(v * (1 - f)) for v in c)

''')

# ---------------- manchas: octógono sólido com borda fina ----------------
rep('''def hexa(a, b):
    """Cor do hexágono (a, b normalizados) ou None."""
    d = max(abs(b) / 0.87, abs(a) + abs(b) * 0.58)
    if d > 1.22: return None
    if d > 1: return HALO                     # halo avermelhado do brilho em volta da mancha (como na ficha)
    return BRASA_MIOLO if d < 0.45 else BRASA if d < 0.8 else BRASA_BORDA''',
'''def hexa(a, b, borda=0.16):
    """Mancha da ficha: octógono amarelo cheio com borda laranja fina (a, b normalizados pelo meio-tamanho)."""
    d = max(abs(a), abs(b), (abs(a) + abs(b)) / 1.4)
    if d > 1: return None
    return BRASA_BORDA if d > 1 - borda else BRASA''')

# ---------------- penas: escurecer sem virar oliva; ouro só na ponta ----------------
rep('''        v = (y0 - c["p"][1]) / L
        base = c0 if v < 0.36 else c1 if v < 0.7 else c2
        face = c["face"]
        if face == "up": base = tom(base, 0.22)
        elif face == "down": base = tom(base, -0.4)
        elif face in ("north", "south"): base = tom(base, -0.12)
        return tom(base, -0.18) if g.na_borda(c) else base''',
'''        v = (y0 - c["p"][1]) / L
        base = c0 if v < 0.42 else c1 if v < 0.78 else c2           # vermelho na raiz, laranja, amarelo só na ponta
        face = c["face"]
        if face == "up": base = mix(base, (255, 236, 200), 0.15)
        elif face == "down": base = escurecer(base, 0.3)
        elif face in ("north", "south"): base = escurecer(base, 0.1)
        return escurecer(base, 0.15) if g.na_borda(c) else base''')

# ---------------- corpo: faixa laranja embaixo do tronco inteiro; manchas onde a ficha mostra ----------------
rep('''VENTRE_Y = 12.2          # abaixo disso o corpo é barriga laranja em placas''', '''VENTRE_Y = 11.2          # abaixo disso: a faixa laranja da barriga, do peito até a cauda''')
rep('''    if face == "down" or (y < VENTRE_Y and z < -6.0):   # barriga laranja embaixo e no peito; flanco roxo
        base = PLACA if (z + 30) % 3.0 > 0.45 else PLACA_ESC          # placas da barriga
        return base
    return GRAFITE''', '''    if face == "down" or y < VENTRE_Y: return VENTRE
    return GRAFITE''')
a = s.index("MANCHAS_CORPO = ["); b = s.index("def mat_placa(c):")
rep(s[a:b], '''# (centro, meio-tamanho, profundidade): profundidade pequena = só na face de fora (sem frestas nas faces de baixo)
MANCHAS_CORPO = [((0, 22.0, 0.0), (1.6, 1, 1.3), 0.3),            # 3 em fila no dorso, entre a asa e o quadril
                 ((0, 22.8, -7.8), (1.5, 1, 1.2), 0.3),
                 ((0, 20.4, 7.8), (1.6, 1, 1.3), 0.3)]
for lado in (-1, 1):
    MANCHAS_CORPO += [((5.9 * lado, 14.4, 1.0), (1, 1.2, 1.5), 0.3),      # flanco
                      ((5.6 * lado, 17.0, 7.4), (1, 1.1, 1.4), 0.3)]      # quadril

''')
rep('''    if face == "up": return PLACA_CLARA
    if face == "down": return PLACA_ESC
    base = PLACA_CLARA if v < 0.22 else PLACA
    if face in ("east", "west"): base = tom(PLACA, -0.15)
    if v > 0.86 or (face == "north" and u > 0.86 and v > 0.5): base = PLACA_ESC
    return base''', '''    if face == "up": return PLACA_CLARA
    if face == "down": return PLACA_ESC
    base = PLACA_CLARA if v < 0.2 else PLACA
    if face in ("east", "west"): base = escurecer(PLACA, 0.1)
    if v > 0.85 or (face == "north" and u > 0.9): base = PLACA_ESC        # linha escura entre as faixas
    return base''')

# ---------------- cauda: sem filete laranja por dentro (costelas) ----------------
rep('''        if face == "up": return LARANJA if abs(x) < 0.2 * w else GRAFITE''', '''        if face == "up": return GRAFITE''')
rep('''        if base:
            if face == "down": return PLACA
            if v < 0.34: return LARANJA
            if v < 0.42: return LARANJA_ESC
            return GRAFITE''', '''        if base:
            if face == "down": return VENTRE
            if v < 0.3: return VENTRE
            return GRAFITE''')
rep('''        if k < 7:
            if v < 0.26: return LARANJA
            if v < 0.34: return LARANJA_ESC
            return GRAFITE
        if v > 0.84: return LARANJA
        if v > 0.76: return LARANJA_ESC
        return GRAFITE''', '''        if k < 7:
            return VENTRE if v < 0.24 else GRAFITE
        return VENTRE if v > 0.8 else GRAFITE''')
rep('''    fundo = g.mat_cor(cor, borda=.0, curva=.15)''', '''    fundo = g.mat_cor(cor, borda=.0, curva=.2)''')
rep('''        filhos = secao(f"{nome}_{k}", px, py, pz - (0.8 if k == 0 else 0.3), pz + L, w, h, mat, br)''',
    '''        filhos = secao(f"{nome}_{k}", px, py, pz - 0.8, pz + L, w, h, mat, br)       # sobreposto: sem frestas''')
rep('''            filhos += secao(f"{nome}_ponta", px, py, pz + L - 0.2, pz + L + 1.2, w * 0.74, h * 0.74, mat, br)''',
    '''            filhos += secao(f"{nome}_ponta", px, py, pz + L - 0.2, pz + L + 1.0, w * 0.7, h * 0.7, mat, br)''')
p.write_text(s, encoding="utf-8"); print("ok a")

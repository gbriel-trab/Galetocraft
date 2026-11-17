"""Patch da rodada n47 (segunda auditoria, sobre a n46): aplica as mudanças em ferramentas/especies/axococo.py."""
from pathlib import Path
p = Path(__file__).resolve().parents[3] / "ferramentas" / "especies" / "axococo.py"
s = p.read_text(encoding="utf-8")

def rep(a, b):
    global s
    assert a in s, a[:90]
    s = s.replace(a, b)

def bloco_entre(ini, fim, novo):
    global s
    a = s.index(ini); b = s.index(fim, a)
    s = s[:a] + novo + s[b:]

# ---------- paleta ----------
rep('''GUELRA_MIOLO = (251, 150, 174)''', '''GUELRA_MIOLO = (252, 162, 192)''')
rep('''GUELRA_PONTA = (226, 35, 81)     # dentes e ponta (226,35,81)''',
    '''GUELRA_PONTA = (240, 52, 105)    # barbas rosa-choque e ponta (paleta (251,60,125); detalhe (226,35,81))
GUELRA_MEDIO = (251, 104, 137)   # barbas rosa-médio (251,106,137)
SOBRANCELHA = (236, 112, 152)    # capuz rosa-escuro por cima do olho''')
rep('''CREME = (250, 226, 212)''', '''CREME = (252, 224, 210)          # creme-pêssego (252,227,211)''')
rep('''MAGENTA = (229, 34, 88)''', '''MAGENTA = (236, 42, 96)''')

# ---------- cabeça sem costuras claras ----------
rep('''def mat_faceta_olho(fora, cz):
    base = mat_bloco(cor_cabeca, borda=.03, faixa=FAIXA_CAB, alto=.04, fundo=-.10)''', '''def mat_faceta_olho(fora, cz):
    base = mat_bloco(cor_cabeca, borda=0, faixa=FAIXA_CAB, alto=.04, fundo=-.08)''')
rep('''    mc = mat_bloco(cor_cabeca, borda=.03, faixa=FAIXA_CAB, alto=.04, fundo=-.10)''',
    '''    mc = mat_bloco(cor_cabeca, borda=0, faixa=FAIXA_CAB, alto=.04, fundo=-.08)        # sem fio claro nas emendas''')

# ---------- olho menor, pupila grande, sobrancelha pintada (rente) ----------
bloco_entre('def olho(u, v):', 'def mat_faceta_olho', '''def olho(u, v):
    """Olho neutro da ficha (u ao longo da face, negativo = para o bico; v para cima):
    - capuz rosa-escuro (sobrancelha) logo acima da linha da pálpebra, que desce em diagonal para o bico;
    - branco puro, menor; pupila preta GRANDE (~45% da largura, ~60% da altura) encostada na pálpebra e no lado
      do bico, com 1 px de brilho no canto de cima; aro âmbar só na fileira de baixo da pupila;
    - moldura azul grossa atrás e embaixo."""
    lid = 0.75 + 0.30 * u                                  # linha da pálpebra
    if lid <= v < lid + 0.6 and -2.6 <= u < 2.9: return SOBRANCELHA
    if v >= lid: return None
    if -2.0 <= u < 1.5 and -1.3 <= v:
        if -2.0 <= u < -0.45 and -0.85 <= v:
            if -1.95 <= u < -1.65 and lid - 0.45 <= v < lid - 0.15: return (255, 255, 255)   # brilho de 1 px
            return PRETO
        if -2.0 <= u < -0.45 and -1.2 <= v < -0.85: return IRIS
        return (255, 255, 255)
    if -2.2 <= u < 2.4 and -2.1 <= v: return OLHO_AZUL
    return None

''')
# tira a sobrancelha-placa (fica só a pintada, rente à cabeça)
rep('''        if olhos:   # sobrancelha: bloco rosa saliente por cima do olho, descendo para o bico (olhar bravo)
            xf = pcx + FAC_T / 2 * lado
            x0, x1 = sorted((xf - 0.3 * lado, xf + 0.4 * lado))
            yb = OLHO_Y + 0.95 + 0.25
            sob = caixa(f"sobrancelha_{'d' if lado < 0 else 'e'}", [x0, yb - 0.25, pcz - 2.9], [x1, yb + 1.8, pcz + 1.7],
                        mat_bloco(lambda p, f: ROSA_MEDIO if f == "down" else ROSA_CLARO, borda=.0, alto=.0, fundo=-.12),
                        rot=(-15.6, 0, 0), pivo=(xf, yb, pcz), res=4)
            pcs.append(osso(f"sobrancelha_{'d' if lado < 0 else 'e'}", [pcx, (y0 + y1) / 2, pcz], [0, 45 * lado, 0], [sob]))
''', '')
rep('''            r = olho(z - cz + 0.1, y - OLHO_Y)''', '''            r = olho(z - cz + 0.3, y - OLHO_Y)''')

# ---------- bico: uma cunha inclinada, ponta embaixo ----------
rep('''def cor_bico(p, face):
    x, y, z = p
    if face in ("east", "west") and abs(z - (CAB_ZF - 2.6)) < 0.3 and abs(y - 25.7) < 0.3: return (74, 26, 0)   # narina''',
    '''def cor_bico(p, face):
    x, y, z = p
    if face == "up" and abs(z - (CAB_ZF - 1.3)) < 0.3 and abs(abs(x) - 1.1) < 0.3: return (74, 26, 0)   # narina no alto''')
rep('''    cab.append(caixa("bico_cima", [-2.5, 24.4, CAB_ZF - 3.4], [2.5, 26.4, CAB_ZF + 0.4], mb))
    cab.append(caixa("bico_baixo", [-1.8, 22.7, CAB_ZF - 3.0], [1.8, 24.5, CAB_ZF + 0.4], mb))
    cab.append(caixa("bico_ponta", [-2.1, 24.2, CAB_ZF - 4.9], [2.1, 26.2, CAB_ZF - 3.3], mb))''',
    '''    # a maxila é UMA peça inclinada 13° (o alto desce em rampa da testa até a ponta, que fica embaixo); a
    # mandíbula, mais estreita, faz o trapézio de frente
    cab.append(caixa("bico", [-2.3, 24.0, CAB_ZF - 4.8], [2.3, 26.4, CAB_ZF + 0.4], mb, rot=(-13, 0, 0),
                     pivo=(0, 26.4, CAB_ZF + 0.4)))
    cab.append(caixa("bico_baixo", [-1.6, 22.6, CAB_ZF - 3.2], [1.6, 24.4, CAB_ZF + 0.4], mb))''')

# ---------- barbela: junto, da largura do bico, curta e de ponta arredondada ----------
rep('''        x0, x1 = xs(lado, 0.8, 3.3)
        xm = 2.05 * lado
        lob = [caixa("barbela_" + s_, [x0, 19.4, CAB_ZF - 2.4], [x1, 22.8, CAB_ZF + 0.8], mbar)]
        x0, x1 = xs(lado, 1.2, 2.9)
        lob.append(caixa("barbela_ponta_" + s_, [x0, 18.2, CAB_ZF - 2.0], [x1, 19.6, CAB_ZF + 0.4], mbar))
        cab.append(osso("barbela_" + s_, [xm, 22.6, CAB_ZF - 0.8], [0, 0, 5 * lado], lob))''',
    '''        x0, x1 = xs(lado, 0.25, 2.3)
        xm = 1.3 * lado
        lob = [caixa("barbela_" + s_, [x0, 19.8, CAB_ZF - 2.2], [x1, 22.7, CAB_ZF + 0.6], mbar)]
        x0, x1 = xs(lado, 0.5, 2.0)
        lob.append(caixa("barbela_ponta_" + s_, [x0, 19.0, CAB_ZF - 1.9], [x1, 20.0, CAB_ZF + 0.3], mbar))
        cab.append(osso("barbela_" + s_, [xm, 22.6, CAB_ZF - 0.8], [0, 0, 4 * lado], lob))''')

# ---------- crista: coroa de 3 colunas, da testa à nuca ----------
bloco_entre('    crista = []\n', '    cab.append(osso("crista"', '''    crista = []
    # coluna central em degraus da testa (bloco que cai um pouco sobre ela) até a nuca; o mais alto no meio-frente
    for k, (z0, z1, y0, y1) in enumerate([(-16.0, -12.8, 30.4, 35.2), (-13.0, -9.8, 31.0, 38.8), (-10.0, -6.8, 31.0, 37.8),
                                          (-7.0, -4.0, 31.0, 36.2), (-4.2, -2.4, 30.6, 34.2)]):
        crista.append(caixa(f"crista_{k}", [-1.9, y0, z0], [1.9, y1, z1], mcr))
    # colunas laterais a ~80% da central (coroa de 3 pontas de frente)
    for lado in (-1, 1):
        for k, (z0, z1, y1) in enumerate([(-14.0, -9.6, 37.0), (-9.8, -5.6, 35.8)]):
            x0, x1 = xs(lado, 1.8, 4.0)
            crista.append(caixa(f"crista_lado{k}_" + ("d" if lado < 0 else "e"), [x0, 31.0, z0], [x1, y1, z1], mcr))
''')

# ---------- brânquias: penas felpudas em degrau ----------
bloco_entre('def guelra(', 'GUELRAS = [', '''def guelra(nome, raiz, lado, L, recuo, eleva):
    """Brânquia de axolote como a 'Brânquias' da ficha: uma pena larga e felpuda. Haste rosa-claro em 3 degraus que
    afinam para fora e, dos dois lados, uma franja CONTÍNUA de barbas de 2 de comprimento inclinadas para a
    ponta, alternando rosa-médio e rosa-choque e deslocadas em escada (as de baixo meio passo adiante).
    Ponta rombuda em degrau rosa-choque. Osso externo sem rotação (é ele que balança na animação); o interno dá
    a direção."""
    x, y, z = raiz
    s = lado
    pcs = []
    def ao_longo(a, b): return sorted((x + a * s, x + b * s))     # ao longo da brânquia, a partir da raiz
    mh = mat_bloco(lambda p, f: GUELRA_MIOLO, borda=.05, alto=.08, fundo=-.05)
    mm = mat_bloco(lambda p, f: GUELRA_MEDIO, borda=.08, alto=.08, fundo=-.06)
    mx = mat_bloco(lambda p, f: GUELRA_PONTA, borda=.08, alto=.08, fundo=-.06)
    degraus = [(-1.0, 0.45 * L, 0.85, 1.1), (0.43 * L, 0.78 * L, 0.7, 0.95), (0.76 * L, L, 0.55, 0.8)]
    for k, (a, b, r, d) in enumerate(degraus):
        x0, x1 = ao_longo(a, b)
        pcs.append(caixa(f"{nome}_haste{k}", [x0, y - r, z - d], [x1, y + r, z + d], mh))
    def raio(a): return next((r for aa, bb, r, d in degraus if aa <= a <= bb), 0.55)
    n = max(2, int((L - 0.4) / 1.8))
    for k in range(n):
        for lado_f in (1, -1):
            a = 0.4 + 1.8 * k + (0.9 if lado_f < 0 else 0.0)
            if a + 1.0 > L: continue
            r = raio(a + 1.0)
            cor = mm if (k + (lado_f < 0)) % 2 == 0 else mx
            x0, x1 = ao_longo(a, a + 2.0)
            y0, y1 = (y + r - 0.2, y + r + 0.9) if lado_f > 0 else (y - r - 0.9, y - r + 0.2)
            xb = x + (a + 1.0) * s
            pcs.append(caixa(f"{nome}_barba{'c' if lado_f > 0 else 'b'}{k}", [x0, y0, z - 0.85], [x1, y1, z + 0.85], cor,
                             rot=(0, 0, -22 * s * lado_f), pivo=(xb, y + lado_f * r, z)))
    x0, x1 = ao_longo(L - 0.2, L + 1.0)
    pcs.append(caixa(nome + "_ponta", [x0, y - 0.75, z - 0.75], [x1, y + 0.75, z + 0.75], mx))
    x0, x1 = ao_longo(L + 0.9, L + 1.7)
    pcs.append(caixa(nome + "_ponta2", [x0, y - 0.45, z - 0.5], [x1, y + 0.45, z + 0.5], mx))
    dentro = osso(nome + "_dir", list(raiz), [0, -recuo * s, eleva * s], pcs)
    return osso(nome, list(raiz), [0, 0, 0], [dentro])

''')
bloco_entre('GUELRAS = [', 'def anim_guelras', '''GUELRAS = [  # (y da raiz, z da raiz, comprimento, recuo (graus para trás), elevação (graus para cima))
    # leque compacto: raízes atrás da bochecha, da altura da sobrancelha até o canto do bico, quase encostadas
    (28.4, -7.6, 10.0, 50, 30),
    (26.0, -7.4, 11.0, 48, 3),
    (23.8, -7.6, 8.5, 46, -15),
]

''')

# ---------- cauda: lâminas largas e chatas num só plano, raízes sobrepostas ----------
bloco_entre('FOICES = [', 'ONDAS = [', '''FOICES = [  # (x, rx inicial, curva de cada junta, comprimentos, largura da faixa, cor raiz, cor ponta, y da raiz)
    # 5 foices largas e chatas (faixa ~2,5x a espessura) no MESMO plano vertical (de trás é uma coluna só),
    # com as raízes sobrepostas; a de cima passa acima das costas e cai de leve na ponta, sem gancho.
    (0.15, 25, (16, 16, 16, 14), (5.4, 5.2, 5.0, 4.6, 4.0), 6.2, AZUL_ROYAL, AZUL_CEU, 19.0),
    (-0.15, 55, (13, 13, 13, 12), (5.6, 5.4, 5.2, 4.8, 4.0), 6.2, AZUL_ROYAL, AZUL_CEU, 18.0),
    (0.15, 80, (11, 11, 11), (5.4, 5.2, 5.0, 4.4), 6.0, AZUL_ROYAL, AZUL_CEU, 17.0),
    (-0.15, 105, (9, 9, 9), (5.2, 5.0, 4.6, 4.0), 5.8, AZUL, AZUL_CEU, 16.0),
    (0.15, 130, (6, 6), (5.0, 4.6, 4.0), 5.4, AZUL, AZUL_CEU, 15.0),
]
''')
rep('''        segs = [(L, 3.8 - 0.25 * i, h - 0.45 * i, mix(c0, c1, i / n), mix(c0, c1, (i + 0.6) / n)) for i, L in enumerate(Ls)]
        cauda.append(pena_cauda(f"cauda_p{k}", (BASE[0] + x, yb, BASE[2]), segs, (rx0, 0, 0), cv,
                                mat_foice, sobrepoe=0.9))''',
    '''        segs = [(L, 2.5 - 0.12 * i, h - 0.5 * i, mix(c0, c1, i / n), mix(c0, c1, (i + 0.6) / n)) for i, L in enumerate(Ls)]
        cauda.append(pena_cauda(f"cauda_p{k}", (BASE[0] + x, yb, BASE[2] - 0.6 * k), segs, (rx0, 0, 0), cv,
                                mat_foice, sobrepoe=1.2))''')

# ---------- peito: escamas em V escalonado ----------
rep('''    FILAS = [(20.8, 17.4, 7.0, -14.0), (17.6, 14.6, 6.6, -14.2), (14.8, 11.8, 5.8, -13.6), (12.0, 9.2, 4.6, -12.4),
             (9.4, 7.6, 3.0, -10.4)]
    for k, (ya, yb, w, zf) in enumerate(FILAS):
        corpo.append(caixa(f"peito_{k}", [-w, yb, zf], [w, ya, zf + 5.0], mp, res=2))
        fundo = 1.4 if k == len(FILAS) - 1 else 0.8           # a última fileira termina em ponta de "V"
        corpo.append(caixa(f"peito_{k}_meio", [-w * 0.42, yb - fundo, zf - 0.3], [w * 0.42, ya - 0.6, zf + 4.0], mp, res=2))''',
    '''    FILAS = [(20.8, 17.6, 6.2, -14.0), (17.8, 14.8, 6.4, -14.2), (15.0, 12.0, 5.8, -13.6), (12.2, 9.4, 4.6, -12.4),
             (9.6, 7.8, 3.0, -10.4)]
    for k, (ya, yb, w, zf) in enumerate(FILAS):     # cada fileira: lados mais curtos, meio, e a ponta do "V" no centro
        corpo.append(caixa(f"peito_{k}", [-w, yb + 0.9, zf + 0.3], [w, ya, zf + 5.0], mp, res=2))
        corpo.append(caixa(f"peito_{k}_meio", [-w * 0.62, yb, zf], [w * 0.62, ya - 0.3, zf + 4.6], mp, res=2))
        corpo.append(caixa(f"peito_{k}_ponta", [-w * 0.3, yb - (1.2 if k == len(FILAS) - 1 else 0.8), zf - 0.3],
                           [w * 0.3, ya - 0.6, zf + 4.0], mp, res=2))''')

# ---------- asas: junto ao corpo, camadas inclinadas, espiral da ficha ----------
bloco_entre('    # ================= asas em gota', '    # ================= cauda:', '''    # ================= asas em gota, encostadas no corpo =================
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        fora = "east" if lado > 0 else "west"
        def cor_asa(p, face, fora=fora, ponta=None):
            x, y, z = p
            if face == fora and espiral(-(z - 1.0), y - 15.2): return ESPIRAL if y < 14.6 else ESPIRAL_CLARO
            if face == "north" and abs(x) > 9.6 and 11.0 < y < 11.7: return ESPIRAL     # a ponta da espiral vista de frente
            if ponta is not None and z > ponta: return GUELRA_MEDIO                      # fio rosa-escuro na ponta da camada
            return ROSA_CLARO
        asa = []
        def camada(nome, xb, y0, y1, z0, z1, xa=6.8):
            m = mat_bloco(lambda p, f, z1=z1: cor_asa(p, f, ponta=z1 - 0.55), borda=.06, alto=.12, fundo=-.12)
            x0, x1 = xs(lado, xa, xb)
            asa.append(caixa(nome + "_" + s_, [x0, y0, z0], [x1, y1, z1], m, res=4))
        # 3 camadas sobrepostas (a de cima por fora na frente), cada uma terminando num degrau com fio rosa-escuro
        camada("asa0", 10.6, 16.8, 20.4, -8.0, 6.2)
        camada("asa1", 11.0, 13.0, 17.2, -7.2, 8.4)
        camada("asa2", 10.6, 9.8, 13.4, -5.8, 9.8)
        camada("asa_base", 10.0, 8.8, 10.0, -4.4, 4.0, xa=7.0)              # base arredondada
        # traseira afinando em 2 pontas escalonadas na direção da cauda
        camada("asa_ponta0", 10.0, 14.4, 17.6, 8.0, 13.4, xa=7.0)
        camada("asa_ponta1", 9.6, 12.0, 14.8, 9.4, 15.0, xa=7.0)
        incl = osso("asa_incl_" + s_, [8.0 * lado, 20.0, -8.0], [8, 0, 0], asa)        # camadas descem para trás
        corpo.append(osso("asa_" + s_, [8.0 * lado, 19.0, -4.0], [0, 0, -3 * lado], [incl]))   # abraça o corpo

''')
bloco_entre('def espiral(', '\ndef montar():', '''def espiral(a, b, k=1.0, t=0.62):
    """Espiral da 'Plumagem Úmida', medida no quadro da ficha: anel oitavado (cantos cortados em degrau, sem
    canto reto), traço grosso, uma barra interna que entra até o miolo (como um "e"/"@") e uma cauda que sai do
    fundo do anel, corre para a frente e para baixo e sobe na ponta. a = para a frente (bico), b = para cima."""
    a, b = a / k, b / k
    ra, rb = 3.4, 2.6
    def oito(a, b): return max(abs(a) / ra, abs(b) / rb, (abs(a) / ra + abs(b) / rb) / 1.45)
    m = oito(a, b)
    if 1 - t / rb <= m <= 1.0 and not (a > 0.8 and -0.9 < b < 0.6): return True      # anel, aberto na frente
    def seg(a0, b0, a1, b1, w=t):
        da, db = a1 - a0, b1 - b0
        tt = clamp(((a - a0) * da + (b - b0) * db) / (da * da + db * db))
        return math.hypot(a - a0 - tt * da, b - b0 - tt * db) < w
    if seg(2.9, 0.6, 0.4, 0.4) or seg(0.4, 0.4, 0.1, -0.6): return True                 # barra do "e" até o miolo
    if seg(0.6, -rb + 0.3, 3.6, -3.6) or seg(3.6, -3.6, 5.4, -3.4) or seg(5.4, -3.4, 6.4, -1.4): return True   # cauda
    return False

''')

# ---------- pernas: mais finas que o pé ----------
rep('''        s = "d" if lado < 0 else "e"; xc = 5.0 * lado; zc = -0.6''', '''        s = "d" if lado < 0 else "e"; xc = 4.6 * lado; zc = -0.6''')
rep('''        pp.append(caixa("perna_" + s, [xc - 3.0, 2.2, zc - 3.0], [xc + 3.0, 9.6, zc + 3.0], ml))   # curta e grossa''',
    '''        pp.append(caixa("perna_" + s, [xc - 2.5, 2.2, zc - 2.5], [xc + 2.5, 9.6, zc + 2.5], ml))   # ~60% da largura do pé''')

p.write_text(s, encoding="utf-8")
print("ok")

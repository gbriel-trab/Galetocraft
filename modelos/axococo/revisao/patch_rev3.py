p = r'C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\axococo.py'
s = open(p, encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)

def cut(a_start, b_start, novo):
    global s
    i = s.index(a_start); j = s.index(b_start, i)
    s = s[:i] + novo + s[j:]

# ---- peito: escamas em U pintadas (sem degraus) ----
cut('def mat_escama_peito(', '# ---------------- espiral da asa', '''def cor_peito(p, face):
    """Peito creme com fileiras alternadas de escamas em 'U' só pintadas (relevo de no máximo 1 px)."""
    x, y, z = p
    c = mix(CREME, ROSA_PALIDO, clamp((y - 18.0) / 5.0) * .4)
    if face in ("up", "down"): return c
    h = x if face in ("north", "south") else z
    alt, larg = 1.9, 2.6
    r = math.floor(y / alt)
    xx = ((h + (larg / 2 if r % 2 else 0)) % larg) / larg - 0.5
    yy = (y % alt) / alt
    b = yy - 1.7 * xx * xx
    if 0 <= b < 0.17: return tom(c, -.17)
    return tom(c, .05 * yy)


''')
rep('''    a = a / 1.3''', '''    a = a / 1.25''')
rep('''def espiral(a, b, passo=1.8, larg=1.2, voltas=1.75, r0=0.0):''', '''def espiral(a, b, passo=1.72, larg=1.15, voltas=1.75, r0=0.0):''')

# ---- cabeça ----
rep('OLHO_Y = 26.4', 'OLHO_Y = 26.9')
rep('''    base = ROSA_CLARO
    if z < -10.5 and y < 25.0: base = mix(ROSA_CLARO, ROSA_PALIDO, clamp((25.0 - y) / 2.2))   # bochecha clara
    if face == "up": base = mix(ROSA_CLARO, ROSA_PALIDO, .25)
    return base''', '''    base = ROSA_CLARO
    if z < -10.0 and y < 26.0:                     # zona clara em volta do bico e embaixo dos olhos
        base = mix(ROSA_CLARO, CREME, clamp((26.0 - y) / 1.6) * .85)
    if face == "north" and abs(x) < 3.2 and y < 27.4: base = mix(base, CREME, .6)
    if face == "up": base = mix(ROSA_CLARO, ROSA_PALIDO, .25)
    return base''')
cut('def olho(u, v):', 'def mat_faceta_olho(', '''def olho(u, v):
    """Olho neutro (u ao longo da face, negativo = para o bico; v para cima): olho branco aberto, mancha azul
    em volta (mais grossa atrás e em cima), pupila preta com anel castanho-dourado e brilho, puxada para o
    bico; por cima, só a linha reta e inclinada da sobrancelha magenta (olhar firme)."""
    ru, rv = 2.2, 1.55
    sob = 1.72 + 0.24 * u                                  # linha da sobrancelha (desce para o bico)
    if -3.0 < u < 3.1 and sob <= v < sob + 0.55: return "sobrancelha"
    if v >= sob: return None
    e = (u / ru) ** 2 + (v / rv) ** 2
    if e <= 1 and v < sob - 0.3:
        pu, pv = u + 0.62, v + 0.05
        dp = math.hypot(pu, pv * 0.95)
        if math.hypot(pu - 0.3, pv - 0.3) < 0.24: return (255, 255, 255)                   # brilho
        if dp < 0.58: return PRETO
        if dp < 0.88: return (170, 112, 40)                                                 # anel castanho-dourado
        return BRANCO if v > -0.8 else (226, 228, 240)
    em = ((u - 0.35) / (ru + 0.8)) ** 2 + ((v - 0.15) / (rv + 0.55)) ** 2
    if em <= 1: return mix(AZUL, AZUL_CLARO, clamp(v / 2 + .4))                            # mancha azul em volta
    return None

''')
rep('''                return mix(MAGENTA, ROSA_FORTE, clamp((y - OLHO_Y - 0.5) / 1.2))''', '''                return MAGENTA''')
rep('''res=8 if olhos else res))''', '''res=res))''')
rep('''    if face in ("east", "west") and abs(z + 16.6) < 0.35 and abs(y - 24.9) < 0.3: return (150, 84, 20)   # narina
    if face == "up": return AMARELO_CLARO
    if 23.15 < y < 23.45 and face != "down": return (196, 104, 18)                       # linha da boca
    if y < 23.3: return LARANJA
    return mix(AMARELO_CLARO, AMARELO, clamp((25.6 - y) / 1.6))''', '''    if face in ("east", "west") and abs(z + 16.0) < 0.3 and abs(y - 25.5) < 0.28: return (150, 84, 20)   # narina
    if face == "up": return AMARELO_CLARO
    if 24.0 < y < 24.3 and face != "down": return (196, 104, 18)                         # linha da boca
    if y < 24.1: return LARANJA
    return mix(AMARELO_CLARO, AMARELO, clamp((26.2 - y) / 1.8))''')
cut('    cab += camada_cabeca("queixo"', '    # crista aquática', '''    cab += camada_cabeca("bochecha", 22.4, 23.7, 0.2, CAB_ZT - 0.4, mc)
    cab += camada_cabeca("cranio", 23.6, 29.8, 0.0, CAB_ZT, mc, olhos=True)
    cab += camada_cabeca("domo1", 29.7, 31.0, 0.8, CAB_ZT - 0.5, mc)
    cab += camada_cabeca("domo2", 30.9, 31.9, 1.9, CAB_ZT - 1.2, mc)
    cab += camada_cabeca("domo3", 31.8, 32.5, 3.2, CAB_ZT - 2.2, mc)
    # bico: cunha amarela que avança e afina (~1/3 da fundura da cabeça), ponta um pouco para baixo
    mb = mat_cor(cor_bico, borda=.05, curva=.3, grao=.02)
    cab.append(peca("bico_base", [-1.9, 23.4, CAB_ZF - 2.2], [1.9, 26.2, CAB_ZF + 0.3], mb, faixa=(23.0, 26.4)))
    cab.append(peca("bico_ponta", [-1.25, 23.6, CAB_ZF - 4.1], [1.25, 25.7, CAB_ZF - 2.1], mb, rot=(-13, 0, 0),
                    pivo=(0, 25.7, CAB_ZF - 2.1), faixa=(23.0, 26.4)))
    # barbela: dois lóbulos vermelhos presos na garganta, quase da largura do bico, ~1,5x a altura dele
    mbar = mat_cor(lambda p, f: VERMELHO_ESC if (f == "north" and abs(p[0]) < 0.18 and p[1] < 22.2)
                   else mix(VERMELHO, VERMELHO_ESC, clamp((21.4 - p[1]) / 3.6)), borda=.12, curva=.3, grao=.02)
    cab.append(peca("barbela", [-2.0, 19.8, CAB_ZF - 1.1], [2.0, 23.5, CAB_ZF + 1.0], mbar, faixa=(17.5, 23.5)))
    for lado in (-1, 1):
        x0, x1 = sorted((0.15 * lado, 1.85 * lado))
        cab.append(peca("barbela_lobo_" + ("d" if lado < 0 else "e"), [x0, 18.1, CAB_ZF - 0.95], [x1, 20.0, CAB_ZF + 0.85], mbar, faixa=(17.5, 23.5)))
''')
rep('''    for k, (z0, z1, w, h) in enumerate([(-14.0, -10.6, 2.0, 4.2), (-11.0, -7.4, 2.4, 6.6), (-8.0, -4.6, 2.3, 7.2), (-5.0, -2.2, 1.8, 4.8)]):
        crista.append(peca(f"crista_{k}", [-w, 32.0, z0], [w, 32.0 + h, z1], mcr, faixa=(32.0, 39.2)))
    for lado in (-1, 1):
        x0, x1 = sorted((1.8 * lado, 3.6 * lado))
        crista.append(peca("crista_lado_" + ("d" if lado < 0 else "e"), [x0, 32.0, -12.2], [x1, 35.0, -5.0], mcr, faixa=(32.0, 39.2)))''',
'''    for k, (z0, z1, w, h, y0) in enumerate([(-13.4, -10.4, 1.9, 4.4, 31.4), (-11.0, -7.4, 2.3, 7.0, 31.8), (-8.0, -4.8, 2.2, 7.4, 31.8), (-5.4, -2.8, 1.7, 4.8, 31.0)]):
        crista.append(peca(f"crista_{k}", [-w, y0, z0], [w, y0 + h, z1], mcr, faixa=(32.0, 39.2)))
    for lado in (-1, 1):
        x0, x1 = sorted((1.6 * lado, 3.0 * lado))
        crista.append(peca("crista_lado_" + ("d" if lado < 0 else "e"), [x0, 31.8, -11.4], [x1, 34.8, -5.6], mcr, faixa=(32.0, 39.2)))''')

# ---- brânquias ----
cut('    passo = (L - 2.0) / n', '    dentro = osso(nome + "_dir"', '''    passo = (L - 1.6) / n
    for k in range(n):                             # franja densa de filamentos magenta na beirada de cima/trás
        cx = x + (0.8 + passo * (k + 0.5)) * s
        h = (1.8 if k % 2 == 0 else 1.25) - 0.05 * k
        cores = (ROSA_FORTE, MAGENTA) if k % 2 == 0 else (MAGENTA, MAGENTA_ESC)
        x0, x1 = sorted((cx - passo * 0.55 * s, cx + passo * 0.55 * s))
        pcs.append(peca(f"{nome}_f{k}", [x0, y + 1.0, z - 1.1], [x1, y + 1.1 + h, z + 1.25],
                        mat_pena(*cores, 1, False), rot=(0, 0, -14 * s), pivo=(cx, y + 1.1, z)))
    # ponta magenta: dois filamentos abrindo em V
    for k, (ang, cores) in enumerate(((-34, (ROSA_FORTE, MAGENTA)), (22, (MAGENTA, MAGENTA_ESC)))):
        x0, x1 = bx(L - 0.6, L + 1.8)
        pcs.append(peca(f"{nome}_tufo{k}", [x0, y - 0.7, z - 0.9], [x1, y + 0.7, z + 0.9],
                        mat_pena(*cores, 0, s < 0), rot=(0, 0, -ang * s), pivo=(x + (L - 0.6) * s, y, z)))
''')
rep('''def guelra(nome, raiz, lado, L, recuo, eleva, n=6):''', '''def guelra(nome, raiz, lado, L, recuo, eleva, n=7):''')
rep('''    (30.6, -7.4, 8.8, 30, 34),
    (27.6, -7.0, 9.4, 34, 2),
    (24.6, -7.0, 8.4, 44, -21),''', '''    (30.2, -5.8, 9.0, 39, 35),
    (27.7, -5.4, 9.6, 34, 12),
    (25.2, -5.6, 8.6, 50, -20),''')
rep('''cab.append(guelra(f"guelra_{s_}_{k}", (7.0 * lado, y0, z0), lado, L, rec, ele))''', '''cab.append(guelra(f"guelra_{s_}_{k}", (6.9 * lado, y0, z0), lado, L, rec, ele))''')
rep('''ONDAS = [("cauda_p0", 4, (4, 0, 0)), ("cauda_p1", 4, (3, 0, 0)), ("cauda_p2", 4, (3, 0, 0))]''',
    '''ONDAS = [("cauda_p0", 6, (3, 0, 0)), ("cauda_p1", 6, (3, 0, 0)), ("cauda_p2", 6, (2, 0, 0))]''')

# ---- pescoço / papo ----
rep('''        peca("pescoco_a", [-3.3, 16.0, -13.2], [3.3, 23.0, -5.0], mat_cor(cor_corpo, curva=.25), faixa=(7, 24), res=4),
        # papo: o peito creme sobe até encostar na cabeça (sem 'pescoço de pau' entre os dois)
        peca("papo", [-4.6, 16.6, -14.2], [4.6, 21.1, -7.0], mat_escama_peito(16.6, 21.1), faixa=(7, 24), res=4),
        peca("papo_lados", [-5.8, 16.4, -13.0], [5.8, 20.9, -7.0], mat_escama_peito(16.4, 20.9), faixa=(7, 24), res=4),
        peca("pescoco_b", [-5.0, 16.0, -11.4], [5.0, 23.0, -4.6], mat_cor(cor_corpo, curva=.25), faixa=(7, 24), res=4),
        cabeca])''', '''        peca("pescoco", [-5.0, 16.0, -11.4], [5.0, 23.6, -4.6], mat_cor(cor_corpo, curva=.25), faixa=(7, 24), res=4)]
        # papo: o volume creme do peito sobe até encostar na cabeça
        + arredondado("papo", [-5.2, 15.8, -14.0], [5.2, 22.6, -6.0], mat_cor(cor_peito, borda=.03, curva=.2), r=1.3, faixa=(7, 24), res=4)
        + [cabeca])''')

# ---- tronco: volumes lisos, peito um volume arredondado ----
cut('    CAMADAS = [', '    corpo = [osso("tronco"', '''    tronco += arredondado2("tronco", [-8.6, 8.6, -10.4], [8.6, 22.0, 9.8], mt, r=3.2, faixa=(7.0, 22.9), res=4)
    tronco += arredondado("barriga", [-6.0, 7.0, -7.4], [6.0, 10.4, 6.2], mt, r=1.4, faixa=(7.0, 22.9), res=4)
    # peito: um só volume arredondado avançando para a frente, com escamas em U pintadas
    tronco += arredondado2("peito", [-5.8, 10.4, -12.8], [5.8, 21.4, -5.0], mat_cor(cor_peito, borda=.03, curva=.25), r=2.0,
                           faixa=(7.0, 22.9), res=4)
    tronco += arredondado("rabadilha", [-4.8, 14.2, 7.6], [4.8, 21.0, 11.4], mt, r=1.4, faixa=(7.0, 22.9), res=4)
''')
rep('''from galo_base import peca, osso, mix, clamp, contexto_luz''', '''from galo_base import peca, osso, mix, clamp, contexto_luz, arredondado, arredondado2''')

# ---- asas ----
cut('        caixa("asa_meio"', '        corpo.append(osso("asa_" + s_', '''        caixa("asa_meio", 7.6, 10.6, (11.4, -7.6), (19.6, 4.0))
        caixa("asa_ombro", 7.6, 10.4, (13.0, -9.2), (21.0, -3.0))          # frente alta e curva
        caixa("asa_ombro2", 7.6, 10.1, (20.8, -7.8), (21.8, -4.4))
        caixa("asa_ombro3", 7.6, 10.1, (14.0, -10.0), (19.8, -9.0))
        caixa("asa_baixo", 7.6, 10.2, (10.4, -6.4), (11.6, 3.0))
        # 3 fileiras de pontas de pena sobrepostas apontando para a cauda (ponta em degrau, voxel)
        for k, (y0, y1, z0, z1, xa, xb) in enumerate([(16.2, 19.4, 2.6, 10.0, 8.0, 10.3), (13.6, 16.8, 2.6, 8.6, 8.2, 10.45),
                                                      (11.2, 14.0, 2.0, 6.8, 8.4, 10.6)]):
            mr = mat_pena(ROSA, ROSA_CLARO, 2, False)
            x0, x1 = sorted((xa * lado, xb * lado))
            asa.append(peca(f"pena_fila{k}_{s_}", [x0, y0, z0], [x1, y1, z1], mr))
            asa.append(peca(f"pena_ponta{k}_{s_}", [x0 + 0.1, y0 + 0.6, z1 - 0.1], [x1 - 0.1, y1 - 0.6, z1 + 1.6], mr))
''')

# ---- cauda: foices largas e finas, arco liso ----
cut('    FOICES = [', '    corpo.append(osso("cauda"', '''    FOICES = [  # (x, rx inicial, curva por segmento, comprimentos, cores (raiz, ponta))
        (0.0, -4, 19, (4.4, 4.4, 4.2, 4.0, 3.8, 3.6), (AZUL_ROYAL, AZUL)),
        (0.5, 18, 18, (4.0, 4.0, 3.8, 3.6, 3.4, 3.2), (AZUL_ROYAL, AZUL_CLARO)),
        (-0.5, 40, 16, (3.8, 3.8, 3.6, 3.4, 3.2, 3.0), (AZUL, AZUL_CLARO)),
        (0.6, 62, 14, (3.6, 3.6, 3.4, 3.2, 3.0, 2.8), (AZUL, AZUL_CEU)),
        (-0.6, 84, 12, (3.4, 3.4, 3.2, 3.0, 2.8, 2.6), (AZUL_CLARO, AZUL_CEU)),
        (0.0, 104, 10, (3.2, 3.2, 3.0, 2.8, 2.6, 2.4), (AZUL_CLARO, AZUL_CEU)),
    ]
    cauda = []
    BASE = (0.0, 18.8, 7.6)
    for k, (x, rx0, cv, Ls, (c0, c1)) in enumerate(FOICES):
        n = len(Ls)
        segs = [(L, 1.9 - 0.12 * i, 5.0 - 0.55 * i, mix(c0, c1, i / n), mix(c0, c1, (i + 1) / n)) for i, L in enumerate(Ls)]
        cauda.append(pena_cauda(f"cauda_p{k}", (BASE[0] + x, BASE[1], BASE[2]), segs, (rx0, 0, 0), (cv, 0, 0), mat_foice, sobrepoe=0.8))
''')
open(p, 'w', encoding='utf-8').write(s)
print("ok")

from pathlib import Path
p = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\salambrasa.py"); s = p.read_text(encoding="utf-8")
a = s.index("DZ_CAB = -2.5")
b = s.index('if __name__ == "__main__":')
novo = r'''DZ_CAB = -2.5; DY_CAB = 2.0   # a cabeça vai para a frente e para cima: o pescoço aparece, como na ficha

def lamina(nome, xm, y0, z0, L, esp, inc):
    """Lâmina da crista: placa fina vermelha de comprimento L que nasce em (y0, z0) e tomba 'inc' graus para trás."""
    return bloco_crista(nome, [-xm, y0, z0], [xm, y0 + L, z0 + esp], rot=(inc, 0, 0), pivo=(0, y0, z0 + esp))

# ---------------- montagem ----------------
def montar():
    i_cab = len(g.PECAS)
    # ---------- cabeça: bloco cinza-roxo, faces diagonais com o olho, viseira em V, bico adunco ----------
    cab = []
    mcab = g.mat_cor(cor_cabeca, borda=.03, curva=.25)
    fx = (23.0, 31.0)
    cab += g.arredondado("cranio", [-4.9, 23.6, -18.4], [4.9, 31.0, -12.6], mcab, r=0.8, faixa=fx, res=3)
    cab.append(peca("cranio_frente", [-2.3, 23.8, -21.5], [2.3, 30.6, -18.0], mcab, faixa=fx, res=3))
    cab.append(peca("queixo", [-3.6, 23.0, -20.2], [3.6, 24.6, -14.0], g.mat_cor(lambda p, f: CABECA_ESC, borda=.06), faixa=fx, res=3))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 23.9, cz - FAC_L / 2], [cx + FAC_T / 2, 30.4, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, FAC_ANG * lado, 0), pivo=(cx, 27.0, cz), faixa=fx, res=8))
        # viseira: cada metade desce ~16° para o meio (V) e passa só 0,5 da face; a borda de baixo corta o alto do olho
        x0, x1 = sorted((0.0, 5.1 * lado))
        cab.append(peca("viseira_" + s, [x0, 29.3, -22.0], [x1, 31.4, -15.0], mat_viseira, rot=(0, 0, 16 * lado),
                        pivo=(5.2 * lado, 31.4, -18.0), res=3))
    cab.append(peca("viseira_meio", [-0.9, 28.2, -22.0], [0.9, 30.2, -16.0], mat_viseira, res=3))      # vértice do V
    # bico: de frente uma cunha em V (degraus 3,4 -> 2,6 -> 1,8 -> 1,0); de lado comprido, dorso reto, ponta curvando
    cab.append(peca("bico0", [-1.7, 27.6, -25.0], [1.7, 28.6, -21.0], mat_bico, res=4))
    cab.append(peca("bico1", [-1.3, 26.6, -25.5], [1.3, 27.7, -21.0], mat_bico, res=4))
    cab.append(peca("bico2", [-0.9, 25.6, -25.7], [0.9, 26.7, -21.2], mat_bico, res=4))
    cab.append(peca("bico3", [-0.5, 24.8, -25.7], [0.5, 25.7, -24.5], mat_bico, res=4))                  # gancho da ponta
    # crista de brasa: 5 lâminas finas em leque, cada uma tombada ~35° para trás, sobrepostas como telhas, a de trás
    # mais alta; de frente estreita, com 2 lâminas laterais mais baixas (a 'cruz' da vista de frente)
    cr = []
    for k, (xm, z0, L, inc) in enumerate([(2.0, -21.4, 4.8, 30), (2.0, -19.6, 6.2, 33), (1.9, -17.8, 7.4, 35),
                                          (1.8, -15.8, 8.4, 36), (1.7, -13.6, 7.0, 40)]):
        cr.append(lamina(f"crista{k}", xm, 30.8, z0, L, 1.9, inc))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, (z0, L, inc) in enumerate([(-20.4, 3.8, 30), (-16.6, 4.6, 36)]):
            x0, x1 = sorted((1.8 * lado, 4.6 * lado))
            cr.append(bloco_crista(f"crista_lado{k}_{s}", [x0, 30.8, z0], [x1, 30.8 + L, z0 + 1.9], rot=(inc, 0, 0),
                                   pivo=(0, 30.8, z0 + 1.9)))
        x0, x1 = sorted((4.8 * lado, 6.2 * lado))     # lóbulos vermelhos na altura do olho, atrás dele
        cr.append(bloco_crista("lobulo_" + s, [x0, 26.6, -15.4], [x1, 29.8, -13.0]))
    cab.append(osso("crista", [0, 31.0, -16.0], [0, 0, 0], cr))
    # penas das bochechas: atrás e abaixo do olho, caindo para trás
    boch = []
    for k, (x, y0, z0, L, rx, rz) in enumerate([(4.4, 29.0, -13.6, 6.4, -64, 12), (4.4, 27.0, -14.6, 6.8, -52, 16),
                                                (4.4, 25.4, -13.0, 7.0, -42, 18)]):
        for lado in (-1, 1):
            s = "d" if lado < 0 else "e"
            cores = [(CRISTA, VERM, LARANJA), (VERM, LARANJA, AMARELO), (VERM, LARANJA, AMARELO)][k]
            boch.append(pena_bloco(f"bochecha{k}_{s}", (x * lado, y0, z0), (rx, 0, rz * lado), L, 2.8, cores, esp=1.2))
    cab.append(osso("bochechas", [0, 26, -15], [0, 0, 0], boch))
    cabeca = osso("cabeca", [0, 24.0, -16.0], [0, 0, 0], cab)
    deslocar(i_cab, [cabeca], DZ_CAB, DY_CAB)

    # ---------- juba (coordenadas finais): nasce atrás e abaixo da bochecha e cai pelas costas do pescoço até a
    # cernelha; de frente só 2 abas pequenas ao lado do queixo. Penas pontudas, algumas carvão misturadas ----------
    C1 = (VERM, LARANJA, AMARELO)                    # degradê da ficha: vermelho -> laranja -> amarelo na ponta
    CC = (GRAFITE, GRAFITE_CLARO, MALVA)             # penas carvão
    juba = []
    JUBA = [  # (x, y, z, phi, abertura, varrida, comprimento, largura, cores) do lado esquerdo (+x); o direito é espelho
        (3.2, 25.8, -16.8, 25, 14, 34, 8.0, 2.8, C1),
        (1.6, 26.0, -15.8, 35, 8, 42, 8.4, 2.8, C1),
        (3.6, 23.2, -16.6, 15, 14, 30, 7.6, 2.8, CC),
        (1.8, 23.4, -16.0, 30, 8, 38, 7.8, 2.8, C1),
        (3.4, 20.6, -15.4, 20, 14, 30, 7.0, 2.6, C1),
        (1.6, 20.8, -14.8, 35, 8, 36, 7.0, 2.6, CC),
        (3.0, 18.2, -13.4, 30, 12, 32, 6.0, 2.4, C1),
        (3.0, 25.6, -21.2, -40, 18, 6, 4.6, 2.4, C1),        # abas de frente, ao lado do queixo
    ]
    for k, (x, y0, z, phi, fl, var, L, W, cores) in enumerate(JUBA):
        for lado in (-1, 1):
            juba.append(pena_cone(f"juba{k}_{'d' if lado < 0 else 'e'}", (x * lado, y0, z), phi, fl, L, W, lado, cores,
                                  varre=var, esp=1.2))
    juba = osso("juba", [0, 22.0, -16.0], [0, 0, 0], juba)

    # ---------- pescoço em S, escuro, com a faixa laranja na frente ----------
    pesc = []
    def mat_pesc(z_frente):
        return g.mat_cor(lambda p, f: VENTRE if p[2] < z_frente + 2.2 else GRAFITE, borda=.03, curva=.2)
    PESC = [  # (nome, meia largura, y0, y1, z0, z1, inclinação, pivô)
        ("pescoco_baixo", 3.4, 6.4, 23.6, -16.8, -10.2, -40, (0, 15.0, -16.8)),
        ("pescoco_alto", 3.3, 17.6, 28.0, -22.4, -16.2, -12, (0, 22.6, -19.4)),
    ]
    for nome, xm, y0, y1, z0, z1, inc, pv in PESC:
        pesc += g.octogono(nome, [-xm, y0, z0], [xm, y1, z1], mat_pesc(z0), r=1.0, faixa=(9, 28), rot=(inc, 0, 0), pivo=pv)
    # escamas da barriga: 6 faixas em chevron, rentes (0,4 de relevo), seguindo a curva da garganta ao peito;
    # largas em cima e afinando até um fundo arredondado entre as patas da frente
    def z_frente(y):
        return -22.4 - (y - 22.6) * 0.21 if y >= 20.5 else -12.8 - (y - 10.0) * 0.86
    FAIXAS = [(22.4, 25.2, 3.6), (19.8, 22.7, 4.3), (17.2, 20.1, 4.5), (14.6, 17.5, 4.1), (12.0, 14.9, 3.4), (9.6, 12.3, 2.6)]
    for k, (yb, ya, w) in enumerate(FAIXAS):
        yc = (ya + yb) / 2; zc = z_frente(yc)
        ang = math.degrees(math.atan(0.21 if yc >= 20.5 else 0.86))
        pesc.append(peca(f"escama_barriga{k}", [-w, yb, zc - 0.4], [w, ya, zc + 1.0], mat_placa(k, len(FAIXAS)),
                         rot=(-ang, 0, 0), pivo=(0, yc, zc), res=3))
    pesc += [juba, cabeca]
    pescoco = osso("pescoco", [0, 16.0, -13.0], [0, 0, 0], pesc)

    # ---------- tronco: lombo liso e arqueado (5 seções, a mais alta no meio), terço de baixo laranja ----------
    corpo = []
    mt = mat_com_manchas(cor_corpo, MANCHAS_CORPO, borda=.02, curva=.22)
    bt = brilho_manchas(MANCHAS_CORPO)
    fc = (8.4, 22.6)
    for nome, z0, z1, topo, xm in [("peito", -13.6, -6.0, 21.8, 5.8), ("ombros", -8.0, -1.0, 22.3, 5.9),
                                   ("meio", -3.0, 4.0, 22.5, 5.9), ("lombo", 2.0, 9.0, 21.9, 5.8), ("quadril", 7.0, 13.4, 20.7, 5.6)]:
        corpo += g.arredondado2(nome, [-xm, 8.8, z0], [xm, topo, z1], mt, r=2.8, faixa=fc, brilho=bt)
    corpo += [ombro(-1), ombro(1)]
    # cauda: tubo de seção quase quadrada, afinando até uma ponta arredondada
    Ls = [4.4, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.6, 3.2, 2.8, 2.6, 2.0]
    Rs = [18, -18, -32, -30, -26, -24, -26, -26, -14, -2, 12, 14]
    Hs = [7.8, 7.6, 7.4, 7.0, 6.6, 6.2, 5.7, 5.1, 4.5, 3.9, 3.3, 2.8]
    Ws = [round(h * 1.15, 2) for h in Hs]
    corpo.append(osso("cauda", [0, 13.5, 11.5], [0, 0, 0], [cauda_gancho("rabo", (0, 13.5, 11.5), list(zip(Ls, Ws, Hs, Rs)))]))
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 14.0, 6.0], [0, 0, 0], corpo)

    pernas = [perna("perna_fd", -7.0, -10.8, False), perna("perna_fe", 7.0, -10.8, False),
              perna("perna_td", -7.0, 8.4, True), perna("perna_te", 7.0, 8.4, True)]
    return [tronco] + pernas

'''
s = s[:a] + novo + s[b:]
s = s.replace("ROSTO = ((0, 28.5, -21.0), 10.0)", "ROSTO = ((0, 29.5, -21.5), 10.0)")
p.write_text(s, encoding="utf-8"); print("ok fase4b")

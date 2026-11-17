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

# ---- frente da cabeça: faceta do olho levemente inclinada (olha um pouco para cima) e chanfros de 45° na testa e no queixo
rp('''        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, CAB_Y0 + 0.3, cz - FAC_LEN / 2], [cx + FAC_T / 2, CAB_Y1, cz + FAC_LEN / 2],
                        mat_faceta(lado), rot=(0, FAC_RY * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=F, res=8, brilho=brilha))''',
   '''        cab.append(osso("faceta_" + s, [cx, OLHO_Y, cz], [0, FAC_RY * lado, 0], [
            peca("faceta_" + s, [cx - FAC_T / 2, CAB_Y0 + 0.3, cz - FAC_LEN / 2], [cx + FAC_T / 2, CAB_Y1, cz + FAC_LEN / 2],
                 mat_faceta(lado), rot=(0, 0, 7 * lado), pivo=(cx, OLHO_Y, cz), faixa=F, res=8, brilho=brilha)]))''')
rp('''    cab.append(peca("cranio_frente", [-FAC_XF - 0.05, CAB_Y0 + 0.4, CAB_Z0], [FAC_XF + 0.05, CAB_Y1, FAC_ZS], mc, faixa=F, res=4))''',
   '''    cab.append(peca("cranio_frente", [-FAC_XF - 0.05, CAB_Y0 + 0.4, CAB_Z0], [FAC_XF + 0.05, CAB_Y1, FAC_ZS], mc, faixa=F, res=4))
    # chanfros de 45° entre a face e a testa (em cima) e entre a face e o queixo (embaixo): a frente deixa de ser placa
    cab.append(peca("chanfro_testa", [-CAB_X + 0.9, CAB_Y1 - 0.7, CAB_Z0 + 0.1], [CAB_X - 0.9, CAB_Y1 + 0.1, CAB_Z0 + 2.2], mc,
                    rot=(45, 0, 0), pivo=(0, CAB_Y1 - 0.3, CAB_Z0 + 1.1), faixa=F, res=4))
    cab.append(peca("chanfro_queixo", [-CAB_X + 0.9, CAB_Y0 - 0.2, CAB_Z0 + 0.3], [CAB_X - 0.9, CAB_Y0 + 0.7, CAB_Z0 + 2.2], mc,
                    rot=(-45, 0, 0), pivo=(0, CAB_Y0 + 0.25, CAB_Z0 + 1.2), faixa=F, res=4))''')
rp('''                 mat_bloco(CINZA_ESC, topo=.0, fio=-.05), rot=(-9, 0, 0)''', '''                 mat_bloco(CINZA_ESC, topo=.0, fio=-.05), rot=(-9, 0, 4 * lado)''')

# ---- pernas: coxa e canela facetadas, tornozelo chanfrado, pé arredondado, dedos em cunha com garra curva
troca("        pp.append(peca(\"coxa_\"", "        return osso(\"perna_\"", '''        pp += octogono("coxa_" + s, [xc - 1.9, 5.2 + PERNA_EXTRA, zc - 1.9], [xc + 1.9, 8.8 + PERNA_EXTRA, zc + 1.9],
                       mat_suave(CARVAO), r=0.7)
        mam = mat_bloco(AMARELO_P, topo=.16, baixo=-.22, fio=-.08)
        def cor_canela(p, f):
            if (p[1] - 1.6) % 1.1 < 0.22: return ESCAMA
            return AMARELO_P
        pp += arredondado("canela_" + s, [xc - 1.7, 1.4, zc - 1.7], [xc + 1.7, 6.2 + PERNA_EXTRA, zc + 1.7],
                          mat_luz(cor_canela, borda=.03, curva=.15), r=0.6, faixa=(1.4, 6.2 + PERNA_EXTRA))
        # tornozelo chanfrado ligando a canela ao pé
        pp += octogono("tornozelo_" + s, [xc - 2.0, 1.2, zc - 2.0], [xc + 2.0, 2.6, zc + 1.6], mam, r=0.8)
        pp += arredondado("pe_" + s, [xc - 2.2, 0, zc - 2.3], [xc + 2.2, 1.7, zc + 1.8], mam, r=0.45)
        mg = mat_bloco(CARVAO, topo=.25, fio=-.05)
        for nome, giro, dx in (("meio", 0, 0), ("fora", -16 * lado, 1.4 * lado), ("dentro", 16 * lado, -1.4 * lado)):
            x0, z0 = xc + dx, zc - 2.0
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .7, 0, z0 - 1.6], [x0 + .7, 1.5, z0 + 0.2], mam),
                # ponta do dedo em cunha (desce para a frente)
                peca(f"dedo_ponta_{nome}_{s}", [x0 - .5, 0, z0 - 2.7], [x0 + .5, 1.2, z0 - 1.5], mam, rot=(10, 0, 0),
                     pivo=(x0, 1.2, z0 - 1.5)),
                # garra curva: base e ponta inclinadas para baixo
                peca(f"garra_{nome}_{s}", [x0 - .38, 0.15, z0 - 3.5], [x0 + .38, 0.95, z0 - 2.55], mg, rot=(28, 0, 0),
                     pivo=(x0, 0.95, z0 - 2.55))]))
        pp.append(peca("dedo_tras_" + s, [xc - .55, 0, zc + 1.4], [xc + .55, 1.0, zc + 2.9], mam, rot=(-12, 0, 0),
                       pivo=(xc, 1.0, zc + 1.4)))
        pp.append(peca("garra_tras_" + s, [xc - .35, 0.1, zc + 2.8], [xc + .35, 0.8, zc + 3.6], mg, rot=(-25, 0, 0),
                       pivo=(xc, 0.8, zc + 2.8)))
''')
P.write_text(s, encoding="utf-8"); print("ok")

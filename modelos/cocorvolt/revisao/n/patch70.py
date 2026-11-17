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

rp("BRILHAM = {RAIO, RAIO_CLARO, RAIO_F, RAIO_BORDA, OLHO_BORDA, OLHO_AZUL, OLHO_MIOLO}",
   "OLHO_SOMBRA = (30, 72, 206); OLHO_CIANO = (120, 204, 255); OLHO_BRILHO = (255, 255, 255)\n"
   "BRILHAM = {RAIO, RAIO_CLARO, RAIO_F, RAIO_BORDA, OLHO_BORDA, OLHO_AZUL, OLHO_MIOLO, OLHO_SOMBRA, OLHO_CIANO, OLHO_BRILHO}")

troca("def olho_volt(u, v):", "def mat_faceta(lado):", '''OLHO_W2 = 1.35                          # meia largura do olho ao longo da faceta

def olho_borda_baixo(u): return -0.40 + 0.06 * (u + OLHO_W2) / (2 * OLHO_W2)     # reta, sobe de leve para trás
def olho_palpebra(u): return 0.15 + 0.27 * u / OLHO_W2                            # pálpebra: desce para o bico (~11°)

def olho_volt(u, v):
    """Olho imponente (Fase 7): fenda alongada para trás (1,6 : 1), a pálpebra cortando o topo em diagonal até o bico
    (aparece ~2/3 da altura), íris azul elétrica ocupando o olho todo, com o brilho concentrado num miolo
    branco-ciano do lado do bico, 1 px de reflexo, sombra da sobrancelha no alto e um fio escuro só em cima.
    u negativo = lado do bico. Devolve a cor ou None (fora do olho: a cor da cara aparece)."""
    vb, vt = olho_borda_baixo(u), olho_palpebra(u)
    if abs(u) <= OLHO_W2 + 0.05 and vt < v <= vt + 0.13: return (30, 32, 40)          # fio da pálpebra
    if abs(u) > OLHO_W2 or v < vb or v > vt: return None
    if v > vt - 0.13: return OLHO_SOMBRA                                               # sombra da sobrancelha
    if (u + 0.98) ** 2 / 0.012 + (v - (vt - 0.22)) ** 2 / 0.01 <= 1: return OLHO_BRILHO   # reflexo
    vm = (vb + olho_palpebra(-0.55)) / 2
    e = ((u + 0.55) / 0.48) ** 2 + ((v - vm) / 0.2) ** 2
    if e <= 1: return OLHO_MIOLO
    if ((u + 0.55) / 0.82) ** 2 + ((v - vm) / 0.32) ** 2 <= 1: return OLHO_CIANO
    if u > OLHO_W2 - 0.12 or v < vb + 0.1: return OLHO_BORDA
    return OLHO_AZUL

''')
# facetas e quilha mais claras (de frente, no jogo, a cara não pode sumir na sombra); testa cinza-médio
rp('''        return tomf(cor_cara(y), g.contexto_luz(c, borda=.0, curva=.25) - 0.14)''',
   '''        return tomf(cor_cara(y), g.contexto_luz(c, borda=.0, curva=.25) - 0.04)''')
rp("CARA = (198, 198, 202); CARA_BAIXO = (156, 156, 162)", "CARA = (210, 210, 216); CARA_BAIXO = (164, 164, 170)")
rp('''    if y > OLHO_Y + 0.62: return CINZA_ESC
    return CARA if y > 25.0 else CARA_BAIXO''', '''    if y > OLHO_Y + 1.0: return (92, 92, 100)
    return CARA if y > 25.0 else CARA_BAIXO''')
# sobrancelha com volume: saliente, acompanhando a pálpebra (~11°) e indo até a base do bico
rp('''        x0, x1 = sorted((cx + (FAC_T / 2 - 0.15) * lado, cx + (FAC_T / 2 + 0.12) * lado))
        cab.append(osso("sobrancelha_" + s, [cx, OLHO_Y, cz], [0, FAC_RY * lado, 0], [
            peca("sobrancelha_" + s, [x0, OLHO_Y + 0.6, cz - FAC_LEN / 2 - 0.05], [x1, OLHO_Y + 1.1, cz + FAC_LEN / 2 + 0.1],
                 mat_bloco(CINZA_ESC, topo=.0, fio=-.05), rot=(-9, 0, 0), pivo=(cx, OLHO_Y + 0.9, cz), res=4)]))''',
   '''        x0, x1 = sorted((cx + (FAC_T / 2 - 0.2) * lado, cx + (FAC_T / 2 + 0.55) * lado))
        yb = OLHO_Y + 0.15 + 0.13                        # a borda de baixo da sobrancelha fica sobre o fio da pálpebra
        cab.append(osso("sobrancelha_" + s, [cx, OLHO_Y, cz], [0, FAC_RY * lado, 0], [
            peca("sobrancelha_" + s, [x0, yb, cz - FAC_LEN / 2 - 0.45], [x1, yb + 0.75, cz + FAC_LEN / 2 + 0.1],
                 mat_bloco((70, 70, 76), topo=.22, baixo=-.45, fio=-.05), rot=(-11.3, 0, 0), pivo=(cx, yb, cz + OLHO_U),
                 res=4)]))''')
P.write_text(s, encoding="utf-8"); print("ok")

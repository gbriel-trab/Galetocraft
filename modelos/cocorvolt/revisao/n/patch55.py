"""Fase 6 (suavidade): menos peças e maiores, penas deitadas em telha, volumes chanfrados."""
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

# material de pena suave: pouco contraste entre peças, fio escuro leve
rp('''def mat_tufo(cor):
    return mat_bloco(cor, topo=.16, baixo=-.3, frente=-.06, fio=-.18)''',
   '''def mat_tufo(cor):
    return mat_bloco(cor, topo=.12, baixo=-.25, frente=-.03, fio=-.07)

def mat_suave(cor):
    """Pena 'suave' (Fase 6): luz contínua e fio escuro fraco, para as telhas vizinhas se fundirem."""
    return mat_bloco(cor, topo=.12, baixo=-.25, frente=-.03, fio=-.07)

def pena_lisa(nome, raiz, rot, L, W, E, cor, ponta=0.38, estreita=0.55):
    """Pena GRANDE em 2 peças (corpo + ponta mais estreita), pendurada para -y; deitada sobre a superfície pelo 'rot'."""
    return pena_degrau(nome, raiz, rot, L, W, E, mat_suave(cor), dir="baixo", passos=(1 - ponta, ponta),
                       largura=(1.0, estreita), espessura=(1.0, 0.8), res=4)''')

# crânio arredondado por facetas
rp('''    cab.append(peca("cranio", [-CAB_X, CAB_Y0, FAC_ZS - 0.05], [CAB_X, CAB_Y1, CAB_Z1], mc, faixa=F, res=4))''',
   '''    cab += arredondado("cranio", [-CAB_X, CAB_Y0, FAC_ZS - 0.05], [CAB_X, CAB_Y1, CAB_Z1], mc, r=0.8, faixa=F, res=4)''')

# bochechas e nuca: poucas penas GRANDES deitadas em telha
troca("    # penas GRANDES da bochecha", "    return cab\n", '''    # bochechas: 3 penas GRANDES por lado, deitadas no lado da cabeça (face larga para fora), apontando para trás e
    # para baixo, sobrepostas em telha; a de baixo desce até o pescoço
    BOCHECHA = [  # (y, z, comprimento, largura, para trás, abertura, cor)
        (31.4, -1.9, 6.6, 3.4, 42, 10, (196, 196, 200)), (29.0, -1.0, 7.0, 3.4, 36, 12, (180, 180, 186)),
        (26.6, 0.2, 6.2, 3.2, 30, 10, (152, 152, 158))]
    for k, (y, z, L, W, tras, fl, cor) in enumerate(BOCHECHA):
        for lado in (-1, 1):
            s = "d" if lado < 0 else "e"
            cab.append(pena_lisa(f"bochecha{k}_{s}", ((CAB_X - 0.2) * lado, y, z), (-tras, 0, fl * lado), L, W, 1.1, cor))
    # nuca: 3 penas grandes deitadas sobre a nuca e o pescoço (face larga para trás), descendo até a capa
    for k, (x, y, L, W, cor) in enumerate([(0.0, 32.0, 8.6, 4.2, (150, 150, 156)), (-2.3, 30.6, 7.4, 3.4, (134, 134, 140)),
                                           (2.3, 30.6, 7.4, 3.4, (134, 134, 140))]):
        raiz = (x, y, CAB_Z1 - 0.1 + 0.25 * (k > 0))
        cab.append(osso(f"nuca{k}", list(raiz), [-12, 0, 6 * x / 2.3], [osso(f"nuca{k}_g", list(raiz), [0, 90, 0], [
            pena_lisa(f"nuca{k}_p", raiz, (0, 0, 0), L, W, 1.1, cor)])]))
''')

# pescoço octogonal
rp('''        peca("pescoco", [-2.4, 22.0, -2.4], [2.4, 24.6, 2.6], mat_bloco(CINZA_ESC)), cabeca])''',
   '''        *octogono("pescoco", [-2.6, 22.0, -2.6], [2.6, 25.0, 2.8], mat_suave(CINZA_ESC), r=0.8), cabeca])''')

# saia de penas: 7 penas grandes de 2 peças
troca("    # saia de penas cinza serrilhadas", "    # ombreiras: placa", '''    # saia de penas cinza sob a túnica (dos lados e atrás; na frente fica o avental): 7 penas grandes deitadas
    for k in range(7):
        ang = math.radians(-45 + 270 * k / 6)
        x, z = 4.5 * math.cos(ang), 0.4 + 3.9 * math.sin(ang)
        yaw = -math.degrees(ang) + 90
        cor = (118, 118, 124) if k % 2 else (104, 104, 112)
        corpo.append(osso(f"saiote{k}", [x, 10.8, z], [0, yaw, 0], [
            pena_lisa(f"saiote{k}_p", (x, 10.8, z), (0, 0, 8), 4.4, 3.8, 1.0, cor)]))

''')

# ombreiras chanfradas (arredondado / octógono), encaixadas
rp('''        placa = peca("ombreira_" + s, [x0, 19.2, -3.5], [x1, 23.6, 3.9], mat_ombreira_solida(lado, "placa"), res=4)
        xb0, xb1 = sorted((6.0 * lado, 8.2 * lado))
        degrau = peca("ombreira_braco_" + s, [xb0, 16.4, -3.2], [xb1, 20.2, 3.6], mat_ombreira_solida(lado, "degrau"), res=4)
        corpo.append(osso("ombro_" + s, [3.4 * lado, 23.6, 0.2], [0, 0, -15 * lado], [
            placa, osso("ombro_braco_" + s, [6.6 * lado, 20.2, 0.2], [0, 0, 10 * lado], [degrau])]))''',
   '''        placa = arredondado("ombreira_" + s, [x0, 19.2, -3.5], [x1, 23.6, 3.9], mat_ombreira_solida(lado, "placa"), r=0.6, res=4)
        xb0, xb1 = sorted((6.0 * lado, 8.2 * lado))
        degrau = octogono("ombreira_braco_" + s, [xb0, 16.6, -3.2], [xb1, 20.4, 3.6], mat_ombreira_solida(lado, "degrau"), r=0.6, res=4)
        corpo.append(osso("ombro_" + s, [3.4 * lado, 23.6, 0.2], [0, 0, -15 * lado], [
            *placa, osso("ombro_braco_" + s, [6.6 * lado, 20.4, 0.2], [0, 0, 10 * lado], degrau)]))''')

# asas: 3 camadas x 3 telhas GRANDES de 2 peças, deitadas na túnica
rp('''    CAMADAS = [(21.0, 6.4, (180, 180, 184)), (17.2, 6.6, (150, 150, 156)), (13.2, 6.8, (122, 122, 128))]
    TELHAS = [(4.9, -2.6), (5.6, -0.9), (6.3, 0.8), (6.9, 2.5)]''',
   '''    CAMADAS = [(21.0, 6.6, (178, 178, 184)), (17.0, 6.8, (158, 158, 164)), (13.0, 7.0, (136, 136, 142))]
    TELHAS = [(5.0, -2.2), (5.9, 0.1), (6.7, 2.4)]''')
rp('''                asa.append(osso(f"asa{r}{k}_{s}", [x_, yr, z], [0, 28 * lado, (4 + 2 * r) * lado], [
                    pena_degrau(f"asa{r}{k}_{s}_p", (x_, yr, z), (0, 0, 0), L - 0.4 * (k % 2), 2.9, 1.4,
                                mat_degraus(cor, (0.0, 0.08, 0.16)), dir="baixo", passos=(0.56, 0.28, 0.16),
                                largura=(1.0, 0.6, 0.25))]))''',
   '''                asa.append(osso(f"asa{r}{k}_{s}", [x_, yr, z], [0, 24 * lado, (4 + 2 * r) * lado], [
                    pena_lisa(f"asa{r}{k}_{s}_p", (x_, yr, z), (0, 0, 0), L - 0.4 * (k % 2), 3.6, 1.2, cor)]))''')

# capa de penas das costas: 2 fileiras x 3 penas grandes
rp('''        for k, x in enumerate((-4.4, -2.3, 2.3, 4.4)):
            raiz = (x, y, TORSO_Z1 + 0.2 + 0.3 * r)
            corpo.append(osso(f"capa{r}{k}", list(raiz), [-8, 0, 6 * x / 4.4], [osso(f"capa{r}{k}_g", list(raiz), [0, 90, 0], [
                pena_degrau(f"capa{r}{k}_p", raiz, (0, 0, 0), L, 2.8, 1.2, mat_degraus(cor, (0.0, 0.08, 0.16)), dir="baixo",
                            passos=(0.56, 0.28, 0.16), largura=(1.0, 0.6, 0.25))])]))''',
   '''        for k, x in enumerate((-3.8, 0.0, 3.8)):
            raiz = (x, y, TORSO_Z1 + 0.2 + 0.3 * r)
            corpo.append(osso(f"capa{r}{k}", list(raiz), [-8, 0, 6 * x / 3.8], [osso(f"capa{r}{k}_g", list(raiz), [0, 90, 0], [
                pena_lisa(f"capa{r}{k}_p", raiz, (0, 0, 0), L, 4.0, 1.1, cor)])]))''')

# cauda contínua: degraus menores entre os segmentos, mais sobreposição
rp('''    H = [5.2, 4.0, 2.6]; F = [0.44, 0.33, 0.23]; W = [2.4, 2.0, 1.5]''',
   '''    H = [5.0, 4.2, 3.1]; F = [0.44, 0.33, 0.23]; W = [2.4, 2.2, 1.9]''')
rp('''        if k + 1 < 3: filhos.append(seg(k + 1, pz + L - 0.3))''', '''        if k + 1 < 3: filhos.append(seg(k + 1, pz + L - 0.6))''')
P.write_text(s, encoding="utf-8"); print("ok")

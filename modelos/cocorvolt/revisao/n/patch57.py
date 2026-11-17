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
troca("def mat_ombreira_solida(lado, parte):", "# ---------------- montagem", '''def mat_ombreira_solida(lado, parte, caixa):
    """Placa de armadura cheia e chanfrada: fundo azul-marinho quase preto (#1e2440) e UM friso de ouro grosso que
    contorna a placa inteira (medido na caixa do grupo, não em cada sub-bloco, para os chanfros não virarem molduras
    empilhadas); na face de fora da placa principal, dois zigue-zagues de ouro de 3 segmentos."""
    fora = "east" if lado > 0 else "west"
    FUNDO = (30, 36, 64)
    (X0, Y0, Z0), (X1, Y1, Z1) = caixa
    def f(c):
        face = c["face"]
        if face == "down": return tomf(FUNDO, -0.3)
        x, y, z = c["p"]
        if face in ("east", "west"): b = min(y - Y0, Y1 - y, z - Z0, Z1 - z)
        elif face in ("north", "south"): b = min(y - Y0, Y1 - y, abs(x) - min(abs(X0), abs(X1)), max(abs(X0), abs(X1)) - abs(x))
        else: b = min(z - Z0, Z1 - z, abs(x) - min(abs(X0), abs(X1)), max(abs(X0), abs(X1)) - abs(x))
        if b < 0.12: return OURO_ESC
        if b < 0.62: return tomf(OURO, 0.1 if face == "up" else 0.0)
        if parte == "placa" and face == fora:
            u = (z - (Z0 + Z1) / 2) / ((Z1 - Z0) / 2) * (-1 if lado > 0 else 1)
            v = ((y - Y0) / (Y1 - Y0)) * 2 - 1
            if any(dist_polilinha(u, v, zz) < 0.09 for zz in ZIGUES_OMB): return OURO_CLARO
        return tomf(FUNDO, 0.15 if face == "up" else 0.0)
    return f

''')
rp('''        placa = arredondado("ombreira_" + s, [x0, 19.2, -3.5], [x1, 23.6, 3.9], mat_ombreira_solida(lado, "placa"), r=0.6, res=4)''',
   '''        placa = arredondado("ombreira_" + s, [x0, 19.2, -3.5], [x1, 23.6, 3.9],
                            mat_ombreira_solida(lado, "placa", ([x0, 19.2, -3.5], [x1, 23.6, 3.9])), r=0.6, res=4)''')
rp('''        degrau = octogono("ombreira_braco_" + s, [xb0, 16.6, -3.2], [xb1, 20.4, 3.6], mat_ombreira_solida(lado, "degrau"), r=0.6, res=4)''',
   '''        degrau = octogono("ombreira_braco_" + s, [xb0, 16.6, -3.2], [xb1, 20.4, 3.6],
                          mat_ombreira_solida(lado, "degrau", ([xb0, 16.6, -3.2], [xb1, 20.4, 3.6])), r=0.6, res=4)''')
# crânio mais arredondado
rp('''    cab += arredondado("cranio", [-CAB_X, CAB_Y0, FAC_ZS - 0.05], [CAB_X, CAB_Y1, CAB_Z1], mc, r=0.8, faixa=F, res=4)''',
   '''    cab += arredondado2("cranio", [-CAB_X, CAB_Y0, FAC_ZS - 0.05], [CAB_X, CAB_Y1, CAB_Z1], mc, r=1.3, faixa=F, res=4)''')
P.write_text(s, encoding="utf-8"); print("ok")

from pathlib import Path
P = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\cocorvolt.py")
s = P.read_text(encoding="utf-8")
def rp(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b)
# cauda: deslocamento em x no padrão -, +, +, -, ... para a alternância carvão/claro aparecer dos dois lados
rp('''        x = 0.35 if k % 2 else -0.35''', '''        x = 0.4 * (1 if k % 4 in (1, 2) else -1)''')
# juba: penas deitadas no lado da cabeça (abrem menos, apontam mais para trás), mais finas
rp('''        (31.0, -1.6, 5.0, 3.4, 30, 30, (196, 196, 200)), (28.8, -0.8, 5.6, 3.6, 38, 26, (196, 196, 200)),
        (26.6, 0.2, 5.4, 3.4, 46, 20, (138, 138, 144))]''',
   '''        (31.0, -1.6, 5.2, 3.4, 18, 22, (196, 196, 200)), (28.8, -0.8, 5.8, 3.6, 24, 18, (196, 196, 200)),
        (26.6, 0.2, 5.6, 3.4, 32, 14, (138, 138, 144))]''')
rp('''                pena_degrau(f"juba{k}_{s}_p", ((CAB_X - 0.5) * lado, y, z), (-14, 0, 0), L, W, 1.4, mat_tufo(cor),''',
   '''                pena_degrau(f"juba{k}_{s}_p", ((CAB_X - 0.5) * lado, y, z), (-30, 0, 0), L, W, 1.15, mat_tufo(cor),''')
# ponta do chapéu: um cubo tan que cobre o encontro dos gomos
rp('''    filhos.append(peca("chapeu_ponta", [-1.0, CH_APICE - 0.9, CH_Z - 1.0], [1.0, CH_APICE + 0.5, CH_Z + 1.0],''',
   '''    filhos.append(peca("chapeu_ponta", [-1.3, CH_APICE - 1.5, CH_Z - 1.3], [1.3, CH_APICE + 0.45, CH_Z + 1.3],''')
P.write_text(s, encoding="utf-8"); print("ok")

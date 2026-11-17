from pathlib import Path
p = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\salambrasa.py"); s = p.read_text(encoding="utf-8")
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:150]
    s = s.replace(a, b)
import re
s = re.sub(r"^GRAFITE = \([0-9, ]*\);", "GRAFITE = (124, 52, 66);", s, flags=re.M)
rep('''VENTRE_Y = 11.4''', '''VENTRE_Y = 12.2''')
rep('''        if base:
            if face == "down": return PLACA
            if v < 0.2: return LARANJA
            if v < 0.28: return LARANJA_ESC
            return GRAFITE''', '''        if base:
            if face == "down": return PLACA
            if v < 0.34: return LARANJA
            if v < 0.42: return LARANJA_ESC
            return GRAFITE''')
rep('''        if k < 7:
            if v < 0.16: return LARANJA
            if v < 0.24: return LARANJA_ESC
            return GRAFITE''', '''        if k < 7:
            if v < 0.26: return LARANJA
            if v < 0.34: return LARANJA_ESC
            return GRAFITE''')
rep('''    for k in range(4):
        raiz = (6.0 * lado, 17.4 - 0.3 * k, -8.4 + 2.0 * k)
        filhos.append(pena_bloco(f"fogo{k}_{s}", raiz, (-(64 + 5 * k), 0, 20 * lado), 7.8 - 0.5 * k, 2.8, cores_fogo[k], esp=1.6))''',
'''    for k in range(5):   # leque grande de penas de fogo (na ficha vai do ombro até o meio do corpo)
        raiz = (6.0 * lado, 17.6 - 0.4 * k, -9.0 + 2.0 * k)
        filhos.append(pena_bloco(f"fogo{k}_{s}", raiz, (-(62 + 5 * k), 0, 22 * lado), 9.6 - 0.6 * k, 3.4,
                                 cores_fogo[k % 4], esp=1.6))''')
rep('''    cores_fogo = [(VERM, LARANJA, AMARELO), (VERM_ESC, VERM, LARANJA), (LARANJA_ESC, LARANJA, AMARELO), (VERM, LARANJA_ESC, LARANJA)]''',
    '''    cores_fogo = [(VERM, LARANJA, AMARELO), (VERM, LARANJA_ESC, LARANJA), (LARANJA_ESC, LARANJA, AMARELO), (VERM, LARANJA_ESC, AMARELO)]''')
# viseira: V moderado e peça do meio contínua
rep('''mat_viseira, rot=(-6, 0, 15 * lado),''', '''mat_viseira, rot=(-6, 0, 10 * lado),''')
rep('''    # bico: cunha''', '''    cab.append(peca("viseira_meio", [-1.6, 28.7, -22.9], [1.6, 30.6, -16.0], mat_viseira, rot=(-6, 0, 0), pivo=(0, 30.6, -18.0), res=3))
    # bico: cunha''')
# bochechas menos abertas para os lados
rep('''(3.8, 25.0, -17.8, 6.2, -24, 34)]):''', '''(3.8, 25.0, -17.8, 6.2, -30, 20)]):''')
p.write_text(s, encoding="utf-8"); print("ok")

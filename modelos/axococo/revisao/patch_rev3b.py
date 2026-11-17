p = r'C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\axococo.py'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
rep("    sob = 1.72 + 0.24 * u ", "    sob = 1.22 + 0.22 * u ")
rep("    if e <= 1 and v < sob - 0.3:", "    if e <= 1 and v < sob - 0.25:")
rep("        pu, pv = u + 0.62, v + 0.05", "        pu, pv = u + 0.78, v + 0.0")
rep("        if dp < 0.58: return PRETO", "        if dp < 0.7: return PRETO")
rep("        if dp < 0.88: return (170, 112, 40) ", "        if dp < 0.92: return (170, 112, 40) ")
rep("        if math.hypot(pu - 0.3, pv - 0.3) < 0.24: return (255, 255, 255)", "        if math.hypot(pu - 0.28, pv - 0.28) < 0.22: return (255, 255, 255)")
for a, b in [('caixa("asa_meio", 7.6, 10.6,', 'caixa("asa_meio", 7.4, 10.0,'), ('caixa("asa_ombro", 7.6, 10.4,', 'caixa("asa_ombro", 7.4, 9.8,'),
             ('caixa("asa_ombro2", 7.6, 10.1,', 'caixa("asa_ombro2", 7.4, 9.5,'), ('caixa("asa_ombro3", 7.6, 10.1,', 'caixa("asa_ombro3", 7.4, 9.5,'),
             ('caixa("asa_baixo", 7.6, 10.2,', 'caixa("asa_baixo", 7.4, 9.6,'),
             ('[(16.2, 19.4, 2.6, 10.0, 8.0, 10.3), (13.6, 16.8, 2.6, 8.6, 8.2, 10.45),', '[(16.2, 19.4, 2.6, 10.0, 7.8, 9.7), (13.6, 16.8, 2.6, 8.6, 8.0, 9.85),'),
             ('(11.2, 14.0, 2.0, 6.8, 8.4, 10.6)]', '(11.2, 14.0, 2.0, 6.8, 8.2, 10.0)]'),
             ('abs(x) > 10.5 and espiral(z + 0.6, y - 15.0)', 'abs(x) > 9.9 and espiral(z + 1.8, y - 15.5)')]:
    rep(a, b)
open(p, 'w', encoding='utf-8').write(s); print("ok")

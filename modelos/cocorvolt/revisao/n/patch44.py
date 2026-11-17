from pathlib import Path
P = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\cocorvolt.py")
s = P.read_text(encoding="utf-8")
def rp(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b)
rp('''        ang = 42 - 82 * t''', '''        ang = 32 - 76 * t''')
# juba: penas em lâmina (afinam por igual até a ponta), menos largas
rp('''        (31.0, -1.6, 5.2, 3.4, 18, 22, (196, 196, 200)), (28.8, -0.8, 5.8, 3.6, 24, 18, (196, 196, 200)),''',
   '''        (31.0, -1.6, 5.6, 2.8, 18, 22, (196, 196, 200)), (28.8, -0.8, 6.0, 3.0, 24, 18, (196, 196, 200)),''')
rp('''                            dir="baixo", passos=(0.5, 0.3, 0.2), largura=(1.0, 0.62, 0.26), res=4)]))
    # atrás da cabeça''', '''                            dir="baixo", passos=(0.4, 0.33, 0.27), largura=(1.0, 0.64, 0.3), res=4)]))
    # atrás da cabeça''')
P.write_text(s, encoding="utf-8"); print("ok")

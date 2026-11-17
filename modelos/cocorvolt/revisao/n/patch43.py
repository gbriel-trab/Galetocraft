from pathlib import Path
P = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\cocorvolt.py")
s = P.read_text(encoding="utf-8")
def rp(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b)
# cauda maior (medida na vista lateral da ficha: até ~20 atrás do ápice, de y 5 a 27)
rp('''        ang = 36 - 66 * t
        y = 18.4 - 5.0 * t
        L = [13.5, 15.0, 16.0, 16.5, 16.5, 15.5, 14.0, 12.0][k]''',
   '''        ang = 42 - 82 * t
        y = 18.6 - 5.4 * t
        L = [16.0, 18.0, 19.0, 19.5, 19.5, 18.5, 17.0, 15.5][k]''')
# chapéu: forma MEDIDA na ficha (mais largo e mais baixo do que a auditoria 2 pedia), aba grossa mantida
rp("CH_APICE, CH_ABA, CH_R, CH_Z, CH_N, CH_T = 39.5, 33.4, 11.6, 0.8, 16, 1.5",
   "CH_APICE, CH_ABA, CH_R, CH_Z, CH_N, CH_T = 39.3, 34.0, 12.2, 0.8, 16, 1.5")
rp("CH_INCL = -8 ", "CH_INCL = -7 ")
rp("        x = 9.6 * lado\n        aba = CH_ABA + (CH_APICE - CH_ABA) * (1 - 9.6 / CH_R)",
   "        x = 9.8 * lado\n        aba = CH_ABA + (CH_APICE - CH_ABA) * (1 - 9.8 / CH_R)")
# juba de baixo menos aberta (de frente a ficha tem só ±3,5 na altura do pescoço)
rp("(26.6, 0.2, 5.6, 3.4, 32, 14, (138, 138, 144))]", "(26.8, 0.4, 5.0, 3.2, 18, 10, (138, 138, 144))]")
# asas e ombreiras um pouco mais para dentro em cima (ficha: ±7,1 a ±7,8 entre y 16 e 22)
rp("    TELHAS = [(4.95, -2.6), (5.9, -0.9), (6.75, 0.8), (7.35, 2.5)]",
   "    TELHAS = [(4.9, -2.6), (5.6, -0.9), (6.3, 0.8), (6.9, 2.5)]")
rp("        xb0, xb1 = sorted((6.2 * lado, 8.7 * lado))", "        xb0, xb1 = sorted((6.0 * lado, 8.2 * lado))")
rp("        x0, x1 = sorted((3.4 * lado, 8.0 * lado))\n        placa", "        x0, x1 = sorted((3.4 * lado, 7.6 * lado))\n        placa")
# barbela: lóbulos mais largos e arredondados, com vão entre eles
rp('''        x0, x1 = sorted((0.16 * lado, 1.1 * lado))
        cab += arredondado("barbela_" + ("d" if lado < 0 else "e"), [x0, y_fim, zw - 0.65], [x1, 27.7, zw + 0.6], mbar,
                           r=0.3, res=4)''',
   '''        x0, x1 = sorted((0.1 * lado, 1.35 * lado))
        cab += arredondado("barbela_" + ("d" if lado < 0 else "e"), [x0, y_fim, zw - 0.7], [x1, 27.7, zw + 0.65], mbar,
                           r=0.5, res=4)''')
P.write_text(s, encoding="utf-8"); print("ok")

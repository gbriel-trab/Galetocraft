from pathlib import Path
P = Path(r"C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\cocorvolt.py")
s = P.read_text(encoding="utf-8")
def rp(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b)
# face em V vista de cima: frente estreita (quilha), facetas do olho mais anguladas para os lados, cabeça mais estreita
rp("CAB_X, CAB_Z0, CAB_Z1 = 3.7, -4.6, 3.4", "CAB_X, CAB_Z0, CAB_Z1 = 3.3, -4.6, 3.4")
rp("FAC_A = 34.0 ", "FAC_A = 46.0 ")
rp("FAC_XF = 1.1 ", "FAC_XF = 0.6 ")
rp('''    # chanfro de 45° entre a face e o queixo (a testa já fica sob a aba e a sobrancelha): a frente deixa de ser placa
    cab.append(peca("chanfro_queixo", [-CAB_X + 0.9, CAB_Y0 - 0.2, CAB_Z0 + 0.3], [CAB_X - 0.9, CAB_Y0 + 0.7, CAB_Z0 + 2.2], mc,
                    rot=(-45, 0, 0), pivo=(0, CAB_Y0 + 0.25, CAB_Z0 + 1.2), faixa=F, res=4))''',
   '''    # miolo atrás do V (fecha o vão entre as facetas, sem aparecer por fora)
    cab.append(peca("cranio_miolo", [-1.6, CAB_Y0 + 0.5, CAB_Z0 + 1.2], [1.6, CAB_Y1 - 0.2, FAC_ZS + 0.2], mc, faixa=F, res=2))
    # quilha: ponte em losango entre os olhos, descendo da testa até o alto do bico
    cab.append(osso("quilha", [0, 30.6, CAB_Z0 + 0.15], [0, 45, 0], [
        peca("quilha", [-0.55, 29.4, CAB_Z0 - 0.4], [0.55, 32.0, CAB_Z0 + 0.7], mc, faixa=F, res=4)]))''')
# bico: a base entra na cabeça (as facetas recuam dos lados, sem vão atrás do bico)
rp('''        cab.append(peca(f"bico_{k}", [-w, y0, zb - d], [w, y1, zb], mb, faixa=fb, res=4))''',
   '''        cab.append(peca(f"bico_{k}", [-w, y0, zb - d], [w, y1, zb + 1.0], mb, faixa=fb, res=4))''')
# bochechas rentes (afinam o contorno)
rp('''        (31.5, -1.9, 6.8, 4.0, 40, 9, (194, 194, 200)), (29.4, -1.0, 7.0, 4.0, 35, 10, (178, 178, 184)),
        (27.3, 0.0, 6.4, 3.8, 30, 9, (156, 156, 162))]''',
   '''        (31.5, -1.6, 6.8, 4.0, 40, 5, (194, 194, 200)), (29.4, -0.8, 7.0, 4.0, 35, 6, (178, 178, 184)),
        (27.3, 0.2, 6.4, 3.8, 30, 5, (156, 156, 162))]''')
rp('''((CAB_X - 0.2) * lado, y, z), (-tras, 0, fl * lado), L, W, 1.1, cor))''',
   '''((CAB_X - 0.35) * lado, y, z), (-tras, 0, fl * lado), L, W, 0.9, cor))''')
# pescoço mais fino
rp('''*octogono("pescoco", [-2.6, 22.0, -2.6], [2.6, 25.0, 2.8], mat_suave(CINZA_ESC), r=0.8), cabeca])''',
   '''*octogono("pescoco", [-2.1, 22.0, -2.3], [2.1, 25.0, 2.6], mat_suave(CINZA_ESC), r=0.7), cabeca])''')
P.write_text(s, encoding="utf-8"); print("ok")

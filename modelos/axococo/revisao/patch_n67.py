"""Patch da rodada n67 (Fase 7, olhar imponente): muda SÓ o olho e a pálpebra em ferramentas/especies/axococo.py."""
from pathlib import Path
p = Path(__file__).resolve().parents[3] / "ferramentas" / "especies" / "axococo.py"
s = p.read_text(encoding="utf-8")

def bloco_entre(ini, fim, novo):
    global s
    a = s.index(ini); b = s.index(fim, a)
    s = s[:a] + novo + s[b:]

def rep(a, b):
    global s
    assert a in s, a[:90]
    s = s.replace(a, b)

# parâmetros do olho (Fase 7): fenda alongada, pálpebra pesada em diagonal até o bico
bloco_entre('def olho(u, v):', 'def mat_faceta_olho', '''OLHO_LARG = (-2.6, 2.6)       # u: do lado do bico até atrás (fenda ~1,7:1)
PALP_Y0, PALP_INCL = 0.75, 0.30   # linha da pálpebra: v = PALP_Y0 + PALP_INCL * u (desce para o bico)
CILIO = (70, 22, 48)
SOMBRA_PALP = (226, 120, 156)    # lado de baixo da pálpebra

def olho(u, v):
    """Olhar imponente (Fase 7), u ao longo da face (negativo = para o bico), v para cima:
    - fenda alongada (~1,7:1): borda de baixo quase reta, subindo de leve para trás;
    - a pálpebra rosa pesada corta o topo numa diagonal que desce até o bico (só ~60% do olho aparece), com um
      fio escuro de 1 px (cílio) e a sombra dela escurecendo o alto da íris;
    - íris âmbar grande ocupando quase todo o olho; pupila preta grande perto do lado do bico, olhando para a
      frente, com 1 px de brilho no alto; esclera só numa cunha atrás;
    - moldura azul só embaixo e atrás."""
    u0, u1 = OLHO_LARG
    lid = PALP_Y0 + PALP_INCL * u
    base = -1.35 + 0.10 * u
    if v >= lid or u < u0 or u >= u1 + 0.45 or v < base - 0.45: return None
    if v < base or u >= u1: return OLHO_AZUL                                  # azul só embaixo e atrás
    if v >= lid - 0.22: return CILIO                                          # fio escuro do alto do olho
    sombra = v >= lid - 0.6
    if u >= 1.5: return mix(ESCLERA, (220, 210, 205), .4) if sombra else ESCLERA      # cunha de esclera atrás
    if u < -0.9:                                                              # pupila do lado do bico
        if -1.55 <= u < -1.2 and lid - 0.62 <= v < lid - 0.27: return (255, 255, 255)   # brilho de 1 px
        return PRETO
    return tom(IRIS, -.3) if sombra else IRIS

''')

# pálpebra com volume: bloco rosa saliente sobre o olho, na mesma diagonal, terminando na base do bico
rep('''        pcs.append(caixa(f"{nome}_diag_{'d' if lado < 0 else 'e'}", [pcx - FAC_T / 2, y0, pcz - L / 2], [pcx + FAC_T / 2, y1, pcz + L / 2],
                         m, rot=(0, 45 * lado, 0), pivo=(pcx, (y0 + y1) / 2, pcz), res=res))
    return pcs''', '''        pcs.append(caixa(f"{nome}_diag_{'d' if lado < 0 else 'e'}", [pcx - FAC_T / 2, y0, pcz - L / 2], [pcx + FAC_T / 2, y1, pcz + L / 2],
                         m, rot=(0, 45 * lado, 0), pivo=(pcx, (y0 + y1) / 2, pcz), res=res))
        if olhos:   # pálpebra pesada: volume rosa sobre o olho, inclinado como a linha da pálpebra, até a base do bico
            xf = pcx + FAC_T / 2 * lado
            x0, x1 = sorted((xf - 0.3 * lado, xf + 0.5 * lado))
            yb = OLHO_Y + PALP_Y0 + PALP_INCL * 0.3          # (o olho é pintado com u = z - cz + 0.3)
            mp = mat_bloco(lambda p, f: SOMBRA_PALP if f == "down" else ROSA_CLARO, borda=0, alto=.06, fundo=-.06)
            palp = caixa(f"palpebra_{'d' if lado < 0 else 'e'}", [x0, yb, pcz - L / 2 + 0.05], [x1, yb + 1.7, pcz + L / 2 - 0.4],
                         mp, rot=(-math.degrees(math.atan(PALP_INCL)), 0, 0), pivo=(xf, yb, pcz), res=4)
            pcs.append(osso(f"palpebra_{'d' if lado < 0 else 'e'}", [pcx, (y0 + y1) / 2, pcz], [0, 45 * lado, 0], [palp]))
    return pcs''')
p.write_text(s, encoding="utf-8")
print("ok")

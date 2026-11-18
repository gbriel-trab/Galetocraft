"""ALTERNATIVA GUARDADA (piloto cb06, ficha g2, substituído pela ficha g3 em 18/11/2026).

Pirococó (#001, Fogo, mítico) no padrão Cobblemon: piloto do guia modelos/GUIA_ESTILO.md.

Ficha: 001_pirococo_g2_* (galo-fênix de armadura roxa e frisos dourados). A ficha diz QUAL criatura é; a construção
segue o Cobblemon (estudos do Blaziken e do Combusken em modelos/referencias/):
- escala 1 (1 texel = 1/16 de bloco), ~45 px de altura = 2,8 blocos, tamanhos inteiros e UV de caixa;
- massas em caixas grossas (tronco, coxas, asas, ombreiras, cabeça) e penas de borda em planos (juba, crista,
  pontas da cauda, franjas do peito, penas da asa);
- olho em cubo na quina da cabeça (lido de frente e de lado) com pálpebra escondida para piscar;
- textura de paleta curta com mosqueado leve e quase sem luz pintada;
- modelado em pose neutra; a postura e a vida vêm das animações (parado com piscar, andar, grito, dormir).

Lado esquerdo da criatura = +x (convenção do Cobblemon); `_e` é o lado esquerdo e `_d` o direito (espelhado).

Uso: python ferramentas/especies/pirococo_cobblemon.py [prefixo_da_rodada] [--mod]
Grava modelos/pirococo/cobblemon/ (geo, textura, brilho, animações) e modelos/pirococo/revisao/<prefixo>_*.png.
Com --mod, copia o resultado para o mod (galetocraft/src/main/resources/assets/galetocraft/).
"""
import json, math, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
import cobble_base as cb  # noqa: E402
from cobble_base import Modelo, material, mosqueado, tom, ruido, onda, canal, gravar  # noqa: E402

RAIZ = AQUI.parent.parent
PASTA = RAIZ / "modelos" / "pirococo" / "cobblemon"
REVISAO = RAIZ / "modelos" / "pirococo" / "revisao"

# ---------------------------------------------------------------------------------------------------------------
# Paleta (amostrada da ficha g2 e reduzida a rampas de 3 a 8 tons; ~35 cores no total)
# ---------------------------------------------------------------------------------------------------------------
ROXO = [(46, 20, 82), (74, 36, 124), (104, 58, 160), (134, 88, 192), (164, 124, 218)]
OURO = [(176, 104, 8), (226, 150, 14), (252, 196, 36), (255, 228, 110)]
FOGO = [(110, 6, 20), (160, 12, 24), (205, 26, 30), (234, 62, 28), (248, 112, 20), (254, 160, 16), (255, 204, 30),
        (255, 236, 110)]
BRANCO = [(170, 150, 200), (200, 186, 224), (226, 218, 240), (246, 244, 252)]
GEMA = [(112, 0, 16), (190, 10, 30), (240, 48, 58), (255, 150, 150)]
PRETO = (26, 12, 30)
BRILHO_OLHO = (255, 255, 255)


def area(t):
    """(s, r, S, R): posição do texel na face (s na horizontal, r de baixo para cima) e o tamanho da face."""
    if t.face in ("frente", "tras"): return t.x, t.y, t.w, t.h
    if t.face in ("esq", "dir"): return t.z, t.y, t.d, t.h
    return t.x, t.z, t.w, t.d


def na_borda(t, larg=1.0, faces=None):
    s, r, S, R = area(t)
    if faces and t.face not in faces: return False
    return s < larg or r < larg or s > S - larg or r > R - larg


# ---------------------------------------------------------------------------------------------------------------
# Pinturas
# ---------------------------------------------------------------------------------------------------------------
def armadura(borda=1.0, faces_borda=("frente", "cima", "esq", "dir", "tras")):
    """Placa roxa com friso dourado na borda (padrão das ombreiras e do peitoral)."""
    def f(t):
        if na_borda(t, borda, faces_borda):
            return mosqueado(OURO, 2, t, 0.18)
        return mosqueado(ROXO, 2, t)
    return f


def peitoral_pint(t):
    """Peitoral roxo: aro dourado em cima e V dourado descendo até a gema."""
    s, r, S, R = area(t)
    cs, cr = int(s), int(r)
    if t.face == "frente":
        if cr == R - 1: return mosqueado(OURO, 2, t, 0.1, luz=False)
        if abs(abs(cs - 3.5) - (cr - 0.5) * 0.75) < 0.6: return mosqueado(OURO, 2 + (cr % 2), t, 0.1, luz=False)
        return mosqueado(ROXO, 2 if cr > 1 else 1, t)
    if t.face == "cima": return mosqueado(OURO, 2, t, 0.1) if s < 1 else mosqueado(ROXO, 2, t)
    if na_borda(t, 1.0, ("esq", "dir")) and cr == R - 1: return mosqueado(OURO, 2, t, 0.1)
    return mosqueado(ROXO, 2, t)


def penas_roxas(t):
    """Coxas e costas: penas roxas em fileiras (a última fileira de cada 3 px é mais escura)."""
    s, r, S, R = area(t)
    base = 2 if int(r) % 3 else 1
    return mosqueado(ROXO, base, t)


def tronco(t):
    s, r, S, R = area(t)
    if t.face == "frente":
        if r < 7 and abs(s - S / 2) < 1.5 + r * 0.45:   # babador de penas brancas/lilás em V, estreitando para baixo
            cs, cr = int(s), int(r)
            fileira = cr // 3
            k = (cs + (fileira % 2) * 1) % 3              # escamas de 3 px, desencontradas por fileira
            ponta = cr % 3 == 0 and k != 1                 # pé da escama (escuro), menos no bico do V
            return mosqueado(BRANCO, 1 if ponta else 2 + (cr % 3 == 2), t, 0.12, luz=False)
        return mosqueado(ROXO, 2, t)
    return penas_roxas(t)


def plano_penas(rampa, ini, fim, larg_ponta=3, chance=0.12):
    """Franja de penas pontudas num plano de frente (w x h x 0): uma pena em V a cada `larg_ponta` px, ponta para
    baixo, clara no meio e lilás nas bordas."""
    def f(t):
        s, r, S, R = area(t)
        k = int(s) % larg_ponta
        borda = k in (0, larg_ponta - 1)
        if int(r) == 0 and borda: return None          # recorte entre as pontas
        if int(r) == 1 and borda and int(s) % (2 * larg_ponta) < larg_ponta: return None
        i = ini + (fim - ini) * (r / R) - (0.8 if borda else 0)
        return mosqueado(rampa, i, t, chance, luz=False)
    return f


def pena(rampa, ini, fim, eixo="z", ponta=0.45, largura=1.0, chance=0.07, recorte=True, sombra=0.9, raiz=0.0):
    """Pena/chama num plano: comprida no `eixo` (a ponta fica no fim do eixo), afinando a partir de `ponta`.
    A cor vai de rampa[ini] (base) a rampa[fim] (ponta)."""
    def f(t):
        if eixo == "z": a, L, c, C = t.z, t.d, t.y, t.h
        elif eixo == "-y": a, L, c, C = t.h - t.y, t.h, (t.z if t.w == 0 else t.x), (t.d if t.w == 0 else t.w)
        else: a, L, c, C = t.y, t.h, (t.z if t.w == 0 else t.x), (t.d if t.w == 0 else t.w)
        fa = a / L
        meia = 0.5 * largura
        if raiz and fa < raiz:
            meia *= 0.5 + 0.5 * fa / raiz
        if recorte and fa > ponta:
            meia *= max(0.0, 1 - (fa - ponta) / (1 - ponta)) ** 0.8
        if abs(c / C - 0.5) > meia + 0.5 / C: return None
        i = ini + (fim - ini) * fa
        if c / C < 0.5: i -= sombra          # metade de baixo (ou de dentro) da pena mais escura: dá forma
        return mosqueado(rampa, i, t, chance, luz=False)
    return f


def cabeca_pint(t):
    """Cabeça: elmo roxo em cima e em volta dos olhos, rosto e queixo brancos embaixo."""
    s, r, S, R = area(t)
    if t.face in ("cima", "tras"): return mosqueado(ROXO, 2, t)
    if t.face == "baixo": return mosqueado(BRANCO, 1, t)
    if t.face == "frente":
        cs, cr = int(s), int(r)
        if cr >= 4 and abs(cs - 3) == cr - 3: return mosqueado(OURO, 2 if cr % 2 else 3, t, 0.1, luz=False)  # V
        if cr >= 6: return mosqueado(OURO, 2, t, 0.1, luz=False)                                         # aro
        return mosqueado(ROXO, 2, t) if cr >= 2 else mosqueado(BRANCO, 2.5, t, 0.08)
    # laterais: aro dourado em cima, máscara roxa em volta do olho, bochecha branca embaixo
    if int(r) == 6: return mosqueado(OURO, 2, t, 0.1, luz=False)
    if r >= 4 or (s < 3.5 and r >= 1.5) or s >= 5.5: return mosqueado(ROXO, 2, t)
    return mosqueado(BRANCO, 2.5, t, 0.08)


def olho(t):
    """Olho de 2x3x3 na quina: pálpebra escura em cima, íris vermelha com a pupila preta olhando para a frente e o
    branco do olho atrás (de frente: pupila do lado do bico)."""
    s, r, S, R = area(t)
    linha = 2 - int(r)          # 0 = em cima
    if t.face in ("cima", "baixo", "tras", "dir"): return mosqueado(ROXO, 1, t)
    if t.face == "frente":
        col = int(s)            # 0 = lado do bico (dentro), 1 = fora
        if linha == 0: return (PRETO, tom(ROXO, 0))[col]
        if linha == 1: return (PRETO, tom(GEMA, 2))[col]
        return (tom(GEMA, 1), tom(GEMA, 2))[col]
    col = int(t.z)              # lado de fora: 0 = frente
    if linha == 0: return (PRETO, PRETO, tom(ROXO, 0))[col]
    if linha == 1: return (tom(GEMA, 2), PRETO, BRILHO_OLHO)[col]
    return (tom(GEMA, 1), tom(GEMA, 2), tom(BRANCO, 2))[col]


def palpebra(t):
    s, r, S, R = area(t)
    if int(r) == 1 and t.face in ("frente", "esq"): return tom(ROXO, 0)   # linha do olho fechado
    return mosqueado(ROXO, 2, t)


def bico(t):
    s, r, S, R = area(t)
    if t.face == "baixo": return tom(OURO, 1)
    if t.face == "cima": return mosqueado(OURO, 3, t, 0.15, luz=False)
    if t.face in ("esq", "dir") and int(r) == 1 and 0.5 < s < 1.5: return tom(OURO, 0)   # narina
    return mosqueado(OURO, 2, t, 0.15, luz=False)


def gancho(t):
    s, r, S, R = area(t)
    return tom(OURO, 1) if r < 1 else mosqueado(OURO, 2, t, 0.15, luz=False)


def bico_baixo(t):
    return mosqueado(OURO, 1, t, 0.15, luz=False)


def barbela(t):
    s, r, S, R = area(t)
    return mosqueado(FOGO, 2 if r < R - 1 else 1, t, 0.2, luz=False)


def tiara(t):
    """Moldura dourada em V na testa (plano de frente 8x5): sobe dos lados e desce até a gema no meio."""
    s, r, S, R = area(t)
    cs, cr = int(s), int(r)
    dist = abs(cs - 3.5)                    # 0,5 no meio ... 3,5 nas pontas
    linha_v = 0.5 + dist * 1.15             # altura da moldura em cada coluna
    if abs(cr - linha_v) <= 0.8 or (dist >= 3 and cr >= 2):
        return mosqueado(OURO, 2 if cr % 2 else 3, t, 0.12, luz=False)
    return None


def gema(t):
    s, r, S, R = area(t)
    if t.face == "frente":
        if int(r) == R - 1 and int(s) == 0: return tom(GEMA, 3)
        return tom(GEMA, 2) if r > R / 2 else tom(GEMA, 1)
    return tom(GEMA, 1)


def chifre(t):
    s, r, S, R = area(t)
    if t.face in ("cima",): return tom(OURO, 3)
    return mosqueado(OURO, 2 if t.face in ("esq", "frente") else 1, t, 0.1, luz=False)


def ouro(t):
    return mosqueado(OURO, 2, t, 0.18)


def ouro_faixa(t):
    """Braçadeira: ouro com uma faixa mais escura no meio."""
    s, r, S, R = area(t)
    return mosqueado(OURO, 1 if int(r) == 0 else 2, t, 0.18)


def dedo(t):
    """Dedo dourado com a garra clara na ponta da frente."""
    if t.z < 1 or t.face == "frente": return mosqueado(BRANCO, 2, t, 0.15, luz=False)
    return mosqueado(OURO, 2, t, 0.18)


def asa(t):
    """Asa fechada: cobertura roxa em cima, penas vermelhas e ponta laranja embaixo, em fileiras."""
    s, r, S, R = area(t)
    if t.face == "dir": return mosqueado(ROXO, 1, t)                       # lado de dentro
    if t.face == "cima": return mosqueado(ROXO, 2, t)
    if r >= R - 3: return mosqueado(ROXO, 2 if int(r) % 2 else 3, t)       # cobertura
    if t.face == "baixo": return mosqueado(FOGO, 4, t)
    i = 2 + (R - 3 - r) / (R - 3) * 2.5                                       # vermelho -> laranja para baixo
    if int(s) % 3 == 2: i -= 1                                                # divisão entre penas
    return mosqueado(FOGO, i, t, 0.18, luz=False)


def tora_pluma(t):
    """Base grossa da pluma da cauda: vermelho-escuro na raiz até laranja perto da ponta, com a nervura clara."""
    i = 1.0 + 2.4 * (t.z / t.d)
    if t.face == "cima": i += 0.6
    if t.face in ("esq", "dir") and int(t.y) == 2: i += 0.6
    return mosqueado(FOGO, i, t, 0.1, luz=False)


def nucleo_juba(t):
    return mosqueado(FOGO, 2 if t.face != "baixo" else 1, t, 0.2)


def brilha_fogo(rgb):
    return rgb in FOGO[5:] or rgb in GEMA


# ---------------------------------------------------------------------------------------------------------------
# Montagem
# ---------------------------------------------------------------------------------------------------------------
def montar():
    m = Modelo("pirococo", 128, 64)
    raiz = m.osso("pirococo")

    # ---------------- pernas (raiz; o corpo balança sem tirar os pés do chão)
    perna = m.osso("perna_e", raiz, pivo=(3, 13, 0))
    m.cubo(perna, (1, 9, -2.5), (4, 5, 5), penas_roxas)
    canela = m.osso("canela_e", perna, pivo=(3, 9, 0))
    m.cubo(canela, (1.5, 2, -1.5), (3, 7, 3), material(ROXO, 2))
    m.cubo(canela, (1, 6, -2), (4, 2, 4), ouro_faixa, inflate=0.01)
    m.cubo(canela, (1, 2, -2), (4, 2, 4), None, inflate=0.01, uv_de=canela.cubos[-1])
    pe = m.osso("pe_e", canela, pivo=(3, 2, 0))
    m.cubo(pe, (1, 0, -2.5), (4, 2, 5), ouro)
    d1 = m.cubo(pe, (0.5, 0, -5.5), (1, 1, 3), dedo)
    m.cubo(pe, (2.5, 0, -6), (1, 1, 3), None, uv_de=d1)
    m.cubo(pe, (4.5, 0, -5.5), (1, 1, 3), None, uv_de=d1)
    m.cubo(pe, (2.5, 0, 2.5), (1, 1, 2), ouro)
    m.espelhar(perna)

    # ---------------- corpo
    corpo = m.osso("corpo", raiz, pivo=(0, 14, 0))
    m.cubo(corpo, (-5, 13, -4), (10, 12, 9), tronco)
    peito = m.osso("peito", corpo, pivo=(0, 17, -4))
    m.cubo(peito, (-3, 11, -4.2), (6, 5, 0), plano_penas(BRANCO, 1, 3))
    m.cubo(peito, (-4.5, 14.5, -4.4), (9, 5, 0), plano_penas(BRANCO, 1, 3))
    peitoral = m.osso("peitoral", corpo, pivo=(0, 22, -4))
    m.cubo(peitoral, (-4, 19, -5.5), (8, 6, 2), peitoral_pint)
    gema_p = m.osso("peitoral_gema_brilho", peitoral, pivo=(0, 21.5, -5.5))
    m.cubo(gema_p, (-1, 20, -6.5), (2, 3, 1), gema, brilho=True)

    # ombreiras e asas (lado esquerdo; o direito é espelhado)
    ombro = m.osso("ombro_e", corpo, pivo=(5, 25, 0), rot=(0, 0, 15))
    m.cubo(ombro, (4, 23, -4.5), (5, 3, 8), armadura())
    m.cubo(ombro, (5, 21, -4), (4, 2, 7), armadura(faces_borda=("frente", "esq", "tras")))
    asa_e = m.osso("asa_e", corpo, pivo=(5, 24, 0))
    m.cubo(asa_e, (5, 13, -3), (2, 11, 9), asa)
    for k, (z, rx) in enumerate(((-1, 5), (2, 15), (5, 28))):
        p = m.osso(f"asa_e_pena{k + 1}", asa_e, pivo=(6, 14, z + 2), rot=(rx, 0, 0))
        if k == 0:
            pena_asa = m.cubo(p, (6, 7, z), (0, 7, 4), pena(FOGO, 2.2, 5.6, eixo="-y", ponta=0.4, sombra=0.7))
        else:
            m.cubo(p, (6, 7, z), (0, 7, 4), None, uv_de=pena_asa)
    m.espelhar(ombro)
    m.espelhar(asa_e)

    # ---------------- pescoço, cabeça, rosto
    pescoco = m.osso("pescoco", corpo, pivo=(0, 25, -1))
    m.cubo(pescoco, (-3, 24, -3.5), (6, 6, 6), lambda t: mosqueado(BRANCO, 2.5, t, 0.08))
    cabeca = m.osso("cabeca", pescoco, pivo=(0, 29, -1.5))
    m.cubo(cabeca, (-3.5, 29, -5), (7, 7, 7), cabeca_pint)
    olho_e = m.osso("olho_e", cabeca, pivo=(2.5, 32.5, -4))
    m.cubo(olho_e, (1.51, 31, -5.01), (2, 3, 3), olho)
    palp = m.osso("palpebra_e", olho_e, pivo=(2.5, 32.5, -4))
    m.cubo(palp, (1.41, 31, -4.91), (2, 3, 3), palpebra, inflate=0.02)
    m.espelhar(olho_e)

    bico_o = m.osso("bico", cabeca, pivo=(0, 32, -5))
    m.cubo(bico_o, (-1.5, 31, -8), (3, 2, 3), bico)
    m.cubo(bico_o, (-1, 30, -9), (2, 2, 1), gancho)
    bico_b = m.osso("bico_baixo", cabeca, pivo=(0, 31, -5))
    m.cubo(bico_b, (-1, 30, -7), (2, 1, 2), bico_baixo)
    m.cubo(bico_b, (-1, 26, -6), (2, 4, 2), barbela)

    elmo = m.osso("elmo", cabeca, pivo=(0, 34, -5))
    gema_e = m.osso("elmo_gema_brilho", elmo, pivo=(0, 34, -5))
    m.cubo(gema_e, (-1, 33, -5.6), (2, 2, 1), gema, brilho=True)
    ch1 = m.osso("chifre_e", elmo, pivo=(2.5, 36, -4), rot=(0, 0, 10))
    m.cubo(ch1, (1.5, 35, -5), (2, 4, 2), chifre)
    ch2 = m.osso("chifre_e2", ch1, pivo=(2.5, 39, -4), rot=(0, 0, 38))
    m.cubo(ch2, (1.5, 39, -5), (2, 3, 2), chifre)
    ch3 = m.osso("chifre_e3", ch2, pivo=(2.5, 42, -4), rot=(-8, 0, -48))
    m.cubo(ch3, (2, 41.5, -4.5), (1, 4, 1), chifre)
    m.espelhar(ch1)

    # juba de fogo: núcleo atrás da cabeça + 4 penas por lado em leque, mais a crista no alto
    juba = m.osso("juba", cabeca, pivo=(0, 32, 1.5))
    m.cubo(juba, (-3, 29, 1), (6, 6, 3), nucleo_juba)
    pena_juba = None
    for k, (y, rx) in enumerate(((35.5, 48), (34, 28), (32, 8), (30.5, -12), (29, -30))):
        p = m.osso(f"juba_e{k + 1}", juba, pivo=(2, y, 2), rot=(rx, 24, 0))
        if pena_juba is None:
            pena_juba = m.cubo(p, (2, y - 2.5, 2), (0, 5, 10), pena(FOGO, 0.6, 3.6, ponta=0.4))
        else:
            m.cubo(p, (2, y - 2.5, 2), (0, 5, 10), None, uv_de=pena_juba)
        m.espelhar(p, pai=juba)
    for k, rx in enumerate((55, 30)):
        p = m.osso(f"crista{k + 1}", juba, pivo=(0, 35, 0), rot=(rx, 0, 0))
        m.cubo(p, (0, 33, 0), (0, 5, 9), pena(FOGO, 1, 4, ponta=0.4) if k == 0 else None,
               uv_de=None if k == 0 else m.ossos[-2].cubos[0])

    # ---------------- cauda de fênix: 3 plumas por lado + 1 no meio; base grossa e ponta em plano que brilha
    cauda = m.osso("cauda", corpo, pivo=(0, 19, 5))
    m.cubo(cauda, (-2, 17, 4), (4, 5, 3), nucleo_juba)
    base_pl = ponta_pl = None
    for k, (dy, rx, ry) in enumerate(((2, 42, 12), (0, 16, 20), (-2, -10, 28))):
        b = m.osso(f"pluma_e{k + 1}", cauda, pivo=(1.5, 20 + dy, 6), rot=(rx, ry, 0))
        if base_pl is None:
            base_pl = m.cubo(b, (1.5, 17 + dy, 6), (0, 6, 12), pena(FOGO, 0.8, 3.6, recorte=False, raiz=0.5, sombra=0.7))
        else:
            m.cubo(b, (1.5, 17 + dy, 6), (0, 6, 12), None, uv_de=base_pl)
        pt = m.osso(f"pluma_e{k + 1}_ponta_brilho", b, pivo=(1.5, 20 + dy, 18), rot=(26, 0, 0))
        if ponta_pl is None:
            ponta_pl = m.cubo(pt, (1.5, 17 + dy, 18), (0, 6, 13), pena(FOGO, 3.6, 7.3, ponta=0.1, sombra=0.7),
                              brilho=brilha_fogo)
        else:
            m.cubo(pt, (1.5, 17 + dy, 18), (0, 6, 13), None, uv_de=ponta_pl, brilho=brilha_fogo)
        m.espelhar(b, pai=cauda)
    bc = m.osso("pluma_c", cauda, pivo=(0, 21, 6), rot=(60, 0, 0))
    m.cubo(bc, (0, 18, 6), (0, 6, 12), None, uv_de=base_pl)
    pc = m.osso("pluma_c_ponta_brilho", bc, pivo=(0, 21, 18), rot=(26, 0, 0))
    m.cubo(pc, (0, 18, 18), (0, 6, 13), None, uv_de=ponta_pl, brilho=brilha_fogo)
    return m


# ---------------------------------------------------------------------------------------------------------------
# Animações (curvas do Cobblemon gravadas em keyframes lineares)
# ---------------------------------------------------------------------------------------------------------------
PISCA = {0.0: [0, 0, 0], 2.95: [0, 0, 0], 3.0: None, 3.12: None, 3.17: [0, 0, 0],
         6.15: [0, 0, 0], 6.2: None, 6.32: None, 6.37: [0, 0, 0], 8.0: [0, 0, 0]}


def piscar_keys(lado):
    fechado = [0.1 if lado == "e" else -0.1, 0, -0.1]
    return {t: (fechado if v is None else v) for t, v in PISCA.items()}


def animacoes(m):
    nomes = {o.nome for o in m.ossos}
    juba = [n for n in nomes if n.startswith("juba_")]
    plumas = sorted(n for n in nomes if n.startswith("pluma_") and not n.endswith("_brilho"))
    pontas = sorted(n for n in nomes if n.startswith("pluma_") and n.endswith("_brilho"))

    # parado: 8 s; respiração em k=1 (4 s), olhar lento em k=0,5 (8 s), penas em cascata
    parado = {
        "corpo": {"position": canal(y=onda(0.3, 1)), "rotation": canal(x=onda(1.2, 1, 30))},
        "pescoco": {"rotation": canal(x=onda(2, 1, 45))},
        "cabeca": {"rotation": canal(x=onda(-2, 1, 90), y=onda(6, 0.5, 0))},
        "asa_e": {"rotation": canal(z=onda(1.5, 1, 30))}, "asa_d": {"rotation": canal(z=onda(-1.5, 1, 30))},
        "cauda": {"rotation": canal(x=onda(2.5, 1, 30), y=onda(3, 0.5, 30))},
        "palpebra_e": {"position": piscar_keys("e")}, "palpebra_d": {"position": piscar_keys("d")},
    }
    for i, n in enumerate(sorted(juba)):
        parado[n] = {"rotation": canal(x=onda(4, 2, 30 + 30 * (i % 4)))}
    for i, n in enumerate(plumas):
        parado[n] = {"rotation": canal(x=onda(3, 1, 30 + 20 * (i % 3)))}
    for i, n in enumerate(pontas):
        parado[n] = {"rotation": canal(x=onda(5, 1, 60 + 20 * (i % 3)))}
    parado["crista1"] = {"rotation": canal(x=onda(4, 2, 60))}
    parado["crista2"] = {"rotation": canal(x=onda(4, 2, 90))}

    # andar: 1 s; pernas em k=4 (uma passada), quique e cabeça de galo em k=8 (um por pé)
    perna = lambda f: onda(28, 4, f)
    joelho = lambda f: (lambda t: 22 * max(0.0, math.sin(math.radians(t * 360 - f))))
    andar = {
        "perna_e": {"rotation": canal(x=perna(0))}, "perna_d": {"rotation": canal(x=perna(180))},
        "canela_e": {"rotation": canal(x=joelho(90))}, "canela_d": {"rotation": canal(x=joelho(270))},
        "pe_e": {"rotation": canal(x=lambda t: -0.6 * (28 * math.sin(math.radians(t * 360))))},
        "pe_d": {"rotation": canal(x=lambda t: -0.6 * (28 * math.sin(math.radians(t * 360 - 180))))},
        "corpo": {"position": canal(y=onda(0.5, 8, 90, -0.3)), "rotation": canal(x=4, z=onda(2.5, 4, 0))},
        "pescoco": {"rotation": canal(x=onda(9, 8, 0))},
        "cabeca": {"rotation": canal(x=onda(-7, 8, 40))},
        "asa_e": {"rotation": canal(z=onda(3, 8, 30))}, "asa_d": {"rotation": canal(z=onda(-3, 8, 30))},
        "cauda": {"rotation": canal(x=onda(-4, 8, 60), y=onda(5, 4, 60))},
    }
    for i, n in enumerate(sorted(juba)):
        andar[n] = {"rotation": canal(x=onda(6, 8, 60 + 30 * (i % 4)))}
    for i, n in enumerate(plumas):
        andar[n] = {"rotation": canal(x=onda(4, 8, 90 + 20 * (i % 3)))}
    for i, n in enumerate(pontas):
        andar[n] = {"rotation": canal(x=onda(6, 8, 120 + 20 * (i % 3)))}

    piscar = {"palpebra_e": {"position": {0.0: [0.1, 0, -0.1], 0.125: [0.1, 0, -0.1], 0.1667: [0, 0, 0]}},
              "palpebra_d": {"position": {0.0: [-0.1, 0, -0.1], 0.125: [-0.1, 0, -0.1], 0.1667: [0, 0, 0]}}}

    grito_t = lambda a, b, pico: (lambda t: pico * (min(1, t / 0.25) if t < 0.25 else 1 if t < 1.2 else max(0, (1.5 - t) / 0.3)))
    grito = {
        "pescoco": {"rotation": canal(x=grito_t(0, 0, -12))},
        "cabeca": {"rotation": canal(x=grito_t(0, 0, -22))},
        "bico_baixo": {"rotation": canal(x=grito_t(0, 0, 32))},
        "asa_e": {"rotation": canal(z=grito_t(0, 0, 18))}, "asa_d": {"rotation": canal(z=grito_t(0, 0, -18))},
        "corpo": {"rotation": canal(x=grito_t(0, 0, -6))},
    }
    for n in juba:
        grito[n] = {"rotation": canal(x=grito_t(0, 0, 15))}

    dormir = {
        "corpo": {"position": canal(y=onda(0.25, 1, 0, -6.5)), "rotation": canal(x=-4)},
        "perna_e": {"position": canal(y=-6.5)}, "perna_d": {"position": canal(y=-6.5)},
        "pescoco": {"rotation": canal(x=25, y=20)},
        "cabeca": {"rotation": canal(x=onda(1.5, 1, 45, 18), y=25)},
        "palpebra_e": {"position": canal(0.1, 0, -0.1)}, "palpebra_d": {"position": canal(-0.1, 0, -0.1)},
        "asa_e": {"rotation": canal(z=-4)}, "asa_d": {"rotation": canal(z=4)},
        "cauda": {"rotation": canal(x=onda(1.5, 1, 30, -12))},
    }
    return {
        "idle": gravar(8.0, parado, passo=0.1),
        "walk": gravar(1.0, andar, passo=1 / 24),
        "blink": gravar(0.1667, piscar, loop=False),
        "cry": gravar(1.5, grito, passo=0.05, loop=False),
        "sleep": gravar(8.0, dormir, passo=0.2),
    }


# ---------------------------------------------------------------------------------------------------------------
# Revisão: vistas, poses, comparação com a arte e conferência do estilo
# ---------------------------------------------------------------------------------------------------------------
def revisar(prefixo):
    import analisar_geo as ag
    from PIL import Image, ImageDraw
    geo = ag.carregar_geo(PASTA / "pirococo.geo.json"); tex = ag.carregar_textura(PASTA / "pirococo.png")
    anims = json.loads((PASTA / "pirococo.animation.json").read_text(encoding="utf-8"))["animations"]
    REVISAO.mkdir(parents=True, exist_ok=True)
    repouso = ag.faces(geo, tex)
    ag.folha_vistas(repouso, 10, "pose de modelagem").save(REVISAO / f"{prefixo}_vistas.png")
    parado = ag.faces(geo, tex, ag.pose(anims["animation.pirococo.idle"], 0))
    ag.folha_vistas(parado, 10, "parado (t=0)").save(REVISAO / f"{prefixo}_parado.png")
    ag.folha_vistas(ag.faces(geo, tex, ag.pose(anims["animation.pirococo.walk"], 0.25)), 10, "andar (t=0,25)").save(
        REVISAO / f"{prefixo}_andar.png")
    # lado a lado com a arte g2, na mesma altura
    import previa2
    arte = Image.open(RAIZ / "modelos/referencias/001_pirococo_g2_arte.png").convert("RGB")
    render = previa2.desenhar(parado, 38, -8, escala=14, fundo=ag.FUNDO)
    k = arte.height / render.height
    render = render.resize((int(render.width * k), arte.height), Image.LANCZOS)
    folha = Image.new("RGB", (arte.width + render.width, arte.height), ag.FUNDO)
    folha.paste(arte, (0, 0)); folha.paste(render, (arte.width, 0))
    folha.save(REVISAO / f"{prefixo}_arte_lado.png")
    # close do rosto
    sel = [f for f in parado[0] if f[0][0][1] > 27 * 1]
    rosto = previa2.desenhar((sel, tex), -30, -5, escala=28, fundo=ag.FUNDO)
    rosto.save(REVISAO / f"{prefixo}_rosto.png")
    lo, hi = ag.limites(parado)
    print(f"medidas (parado): altura {(hi[1] - min(lo[1], 0)) / 16:.2f}, largura {(hi[0] - lo[0]) / 16:.2f}, "
          f"comprimento {(hi[2] - lo[2]) / 16:.2f} blocos (tabela: 2,80 x 2,00 x 2,90)")
    est = ag.conferir_estilo(geo, tex, repouso, anims, 1.0)
    print(f"estilo: {sum(b for *_, b in est)}/{len(est)}")
    for c, alvo, v, b in est:
        if not b: print(f"  NÃO {c}: {v} (alvo {alvo})")


def exportar_mod():
    """Copia geometria, textura, brilho e animações para o mod (substitui o Pirococó antigo)."""
    import shutil
    mod = RAIZ / "galetocraft" / "src" / "main" / "resources" / "assets" / "galetocraft"
    shutil.copyfile(PASTA / "pirococo.geo.json", mod / "geckolib/models/entity/pirococo.geo.json")
    shutil.copyfile(PASTA / "pirococo.animation.json", mod / "geckolib/animations/entity/pirococo.animation.json")
    shutil.copyfile(PASTA / "pirococo.png", mod / "textures/entity/pirococo.png")
    shutil.copyfile(PASTA / "pirococo_glowmask.png", mod / "textures/entity/pirococo_glowmask.png")
    print(f"exportado para {mod}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    prefixo = args[0] if args else "cb"
    m = montar()
    m.salvar(PASTA, animacoes(m))
    revisar(prefixo)
    if "--mod" in sys.argv:
        exportar_mod()

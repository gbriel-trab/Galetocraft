"""Pirococó (#001, Fogo, mítico), o Galo Fênix: ficha g3 (modelos/referencias/001_pirococo_g3_*.png) no padrão Cobblemon.

Feito pelo método da seção 13 de modelos/GUIA_ESTILO.md (da imagem ao modelo), como o Cobblemon adaptou a arte do
Blaziken (modelos/referencias/blaziken_arte_para_modelo.md):
- a ficha define a silhueta, as proporções (medidas na vista de frente) e as áreas de cor;
- massas em caixas: cabeça vermelha com elmo prateado, bico em gancho, pescoço e tronco creme esguios, peitoral e
  cinto prateados com o V roxo, ombreiras, coxas roxas, grevas prateadas e pés roxos com garras de ouro;
- bordas em planos: crista de chamas em leque, penas de fogo na barra do manto, tufos das 3 caudas e a peça em V do
  cinto;
- desenho interno na textura: V do peito, frisos da armadura, trança dos cordões e o degradê do manto
  (roxo -> magenta -> vermelho -> laranja -> ouro);
- cores tiradas da paleta da ficha com cobble_base.rampa_da_arte();
- modelado em pose neutra; a pose da arte é a animação `render` (conferida com ferramentas/comparar_arte.py).

Escala 1: 2,8 blocos = 45 px. Lado esquerdo da criatura = +x; `_e` = esquerdo, `_d` = direito (espelhado).

Uso: python ferramentas/especies/pirococo_cobblemon.py [prefixo_da_rodada] [--mod]
Grava modelos/pirococo/cobblemon/ e as imagens da rodada em modelos/pirococo/revisao/<prefixo>_*.png;
com --mod, copia o resultado para o mod. A versão anterior (ficha g2) está em modelos/pirococo/alternativa_cb06.py.
"""
import json, math, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
from cobble_base import Modelo, mosqueado, tom, rampa_da_arte, onda, canal, gravar  # noqa: E402

RAIZ = AQUI.parent.parent
PASTA = RAIZ / "modelos" / "pirococo" / "cobblemon"
REVISAO = RAIZ / "modelos" / "pirococo" / "revisao"
ARTE = RAIZ / "modelos" / "referencias" / "001_pirococo_g3_arte_recorte.png"

# ---------------------------------------------------------------------------------------------------------------
# Paleta: os 6 círculos da ficha (+ magenta e laranja do manto, amostrados na arte) -> rampas de pixel art
# ---------------------------------------------------------------------------------------------------------------
ROXO = rampa_da_arte((127, 53, 188))
PRATA = rampa_da_arte((213, 193, 213))
CREME = rampa_da_arte((247, 228, 207), tons=4)
VERMELHO = rampa_da_arte((243, 84, 85))
MAGENTA = rampa_da_arte((205, 30, 86), tons=3, meio=1)
LARANJA = rampa_da_arte((245, 122, 40), tons=3, meio=1)
OURO = rampa_da_arte((252, 194, 47))
ESCURO = rampa_da_arte((94, 76, 82), tons=3, meio=1)
# degradê do manto e das caudas: roxo -> magenta -> vermelho -> laranja -> ouro
CHAMA = [ROXO[1], ROXO[2], MAGENTA[1], MAGENTA[2], VERMELHO[3], LARANJA[1], LARANJA[2], OURO[3], OURO[4]]


def area(t):
    """(s, r, S, R): posição do texel na face (s na horizontal, r de baixo para cima) e o tamanho da face."""
    if t.face in ("frente", "tras"): return t.x, t.y, t.w, t.h
    if t.face in ("esq", "dir"): return t.z, t.y, t.d, t.h
    return t.x, t.z, t.w, t.d


def na_borda(t, larg=1.0):
    s, r, S, R = area(t)
    return s < larg or r < larg or s > S - larg or r > R - larg


# ---------------------------------------------------------------------------------------------------------------
# Pinturas
# ---------------------------------------------------------------------------------------------------------------
def pena(rampa, ini, fim, eixo="z", ponta=0.45, raiz=0.0, sombra=0.8, chance=0.05, losango=None):
    """Pena/chama num plano, comprida no `eixo` ('z' ou '-y': ponta no fim do eixo), afinando a partir de `ponta`.
    Cor de rampa[ini] (raiz) a rampa[fim] (ponta); metade de baixo mais escura. `losango`=(posição, raio) desenha o
    losango roxo dos tufos da cauda."""
    def f(t):
        if eixo == "z": a, L, c, C = t.z, t.d, t.y, t.h
        elif eixo == "y": a, L, c, C = t.y, t.h, (t.z if t.w == 0 else t.x), (t.d if t.w == 0 else t.w)
        else: a, L, c, C = t.h - t.y, t.h, (t.z if t.w == 0 else t.x), (t.d if t.w == 0 else t.w)
        fa = a / L; meia = 0.5
        if raiz and fa < raiz: meia *= 0.45 + 0.55 * fa / raiz
        if fa > ponta: meia *= max(0.0, 1 - (fa - ponta) / (1 - ponta)) ** 0.8
        if abs(c / C - 0.5) > meia + 0.5 / C: return None
        if losango and abs(a - losango[0] * L) + abs(c - C / 2) <= losango[1]:
            return tom(ROXO, 3 if abs(c - C / 2) < 0.6 else 2)
        i = ini + (fim - ini) * fa - (sombra if c / C < 0.5 else 0)
        return mosqueado(rampa, i, t, chance, luz=False)
    return f


def armadura(base=None):
    """Placa prateada: friso mais escuro na borda e miolo claro."""
    base = base or PRATA
    def f(t):
        if na_borda(t, 1.0) and t.face != "baixo":
            return mosqueado(base, 1, t, 0.1)
        return mosqueado(base, 3 if t.face == "cima" else 2, t, 0.12)
    return f


def roxo_escamas(t):
    """Pernas e pés: roxo com fileiras de escamas (a cada 2 px um tom mais escuro)."""
    s, r, S, R = area(t)
    return mosqueado(ROXO, 2 if int(r) % 2 else 1, t, 0.12)


def tronco(t):
    """Tronco esguio de pele creme com o desenho do abdômen; costas cobertas pelo manto (roxas)."""
    s, r, S, R = area(t)
    if t.face == "tras": return mosqueado(ROXO, 1, t)
    if t.face == "frente":
        cs, cr = int(s), int(r)
        if cs == int(S // 2) and cr < R - 1: return tom(CREME, 1)            # linha do meio
        if cr in (2, 4) and cs != int(S // 2): return tom(CREME, 2)           # gomos
        return mosqueado(CREME, 3, t, 0.08, luz=False)
    if t.face in ("esq", "dir"): return mosqueado(VERMELHO, 1, t, 0.1)       # flancos avermelhados (sombra da arte)
    return mosqueado(CREME, 2, t, 0.08)


def peitoral(t):
    """Placa do peito: prata com o símbolo da fênix (V roxo) no meio da frente."""
    s, r, S, R = area(t)
    if t.face == "frente":
        cs, cr = int(s), int(r)
        d = abs(cs + 0.5 - S / 2)
        if (cr == R - 1 and d < 2.5) or (abs(d - (cr + 0.6)) < 0.75 and cr < R - 1):
            return tom(ROXO, 3 if cr == R - 1 else 2)
        return mosqueado(PRATA, 3 if cr == R - 1 else 2, t, 0.1, luz=False)
    if t.face == "tras": return mosqueado(ROXO, 1, t)
    return armadura()(t)


def cinto(t):
    s, r, S, R = area(t)
    if t.face == "frente" and int(r) == 1: return mosqueado(ROXO, 2, t, 0.1)      # faixa roxa
    return armadura()(t)


def tanga(t):
    """Peça em V da frente do cinto (plano): prata com a gema roxa em losango, ponta para baixo."""
    s, r, S, R = area(t)
    cx = S / 2
    meia = (r / R) * (S / 2) + 0.5          # V: estreita embaixo
    if abs(s - cx) > meia: return None
    if abs(s - cx) + abs(r - R * 0.55) <= 1.2: return tom(ROXO, 3) if r > R * 0.55 else tom(ROXO, 2)
    return mosqueado(PRATA, 2 if abs(s - cx) < meia - 0.8 else 1, t, 0.08, luz=False)


def ombreira(t):
    if t.face in ("cima", "esq") and not na_borda(t, 1.0): return mosqueado(ROXO, 2, t, 0.12)   # painel roxo
    return mosqueado(PRATA, 2 if t.face != "baixo" else 1, t, 0.1)


def pescoco(t):
    """Garganta creme na frente; vermelho dos lados, atrás e no alto (perto da cabeça)."""
    s, r, S, R = area(t)
    if t.face == "frente" and r < R - 1: return mosqueado(CREME, 3, t, 0.08, luz=False)
    if t.face in ("esq", "dir") and s < 1 and r < R - 2: return mosqueado(CREME, 2, t, 0.08, luz=False)
    return mosqueado(VERMELHO, 2, t, 0.12)


def cabeca(t):
    return mosqueado(VERMELHO, 2 if t.face != "baixo" else 1, t, 0.12)


def elmo(t):
    """Elmo prateado (estilo Ikki): friso escuro na borda de baixo, faixa roxa no alto."""
    s, r, S, R = area(t)
    if t.face == "baixo": return mosqueado(PRATA, 1, t, 0.1)
    if t.face in ("frente", "esq", "dir", "tras") and int(r) == 0: return tom(PRATA, 1)
    if t.face == "cima" and abs(s - S / 2) < 1.2: return mosqueado(ROXO, 2, t, 0.1)
    return mosqueado(PRATA, 3, t, 0.1)


def olho(t):
    """Olho 2x2x2 na quina da cabeça: pálpebra escura em cima, íris violeta, pupila escura voltada para a frente."""
    s, r, S, R = area(t)
    linha = 1 - int(r)
    if t.face in ("cima", "baixo", "tras", "dir"): return mosqueado(VERMELHO, 2, t, 0.1)
    if t.face == "frente":
        col = int(s)                       # 0 = lado do bico
        if linha == 0: return tom(ESCURO, 0)
        return (tom(ESCURO, 0), tom(ROXO, 3))[col]
    col = int(t.z)                         # lateral: 0 = frente
    if linha == 0: return (tom(ESCURO, 0), tom(ESCURO, 1))[col]
    return (tom(ESCURO, 0), tom(ROXO, 4))[col]


def palpebra(t):
    s, r, S, R = area(t)
    if int(r) == 0 and t.face in ("frente", "esq"): return tom(ESCURO, 0)
    return mosqueado(VERMELHO, 2, t, 0.1)


def bico(t):
    s, r, S, R = area(t)
    if t.face == "baixo": return tom(OURO, 1)
    if t.face == "cima": return mosqueado(OURO, 4, t, 0.1, luz=False)
    if t.face in ("esq", "dir") and int(r) == 1 and 0.5 < s < 1.5: return tom(LARANJA, 0)     # narina
    return mosqueado(OURO, 3, t, 0.1, luz=False)


def gancho(t):
    s, r, S, R = area(t)
    return tom(LARANJA, 1) if r < 1 else mosqueado(OURO, 2, t, 0.1, luz=False)


def bico_baixo(t):
    return mosqueado(LARANJA, 2, t, 0.1, luz=False)


def gema(t):
    s, r, S, R = area(t)
    if t.face == "frente" and int(r) == R - 1: return tom(ROXO, 4)
    return tom(ROXO, 3) if r > R / 2 else tom(ROXO, 2)


def ouro(t):
    return mosqueado(OURO, 3 if t.face in ("cima", "frente", "esq") else 2, t, 0.1, luz=False)


def dedo(t):
    """Dedo roxo com a garra de ouro na ponta (1,5 px da frente)."""
    if t.z < 1.5 or t.face == "frente": return mosqueado(OURO, 3, t, 0.08, luz=False)
    return roxo_escamas(t)


def manto(t):
    """Placa do manto: roxo em cima esquentando para magenta e vermelho embaixo, em fileiras de penas."""
    s, r, S, R = area(t)
    if t.face in ("dir", "frente") and min(t.w, t.d) <= 1: return mosqueado(ROXO, 1, t, 0.1)      # lado de dentro
    fr = 1 - r / R                                  # 0 em cima, 1 embaixo
    i = 0.4 + fr * 3.6
    if int(s) % 3 == 2: i -= 0.7                    # divisão entre penas
    if int(r) % 4 == 0: i -= 0.4                    # fileiras
    return mosqueado(CHAMA, i, t, 0.05, luz=False)


def cordao(t):
    """Cordão trançado de ouro: listras diagonais claras e escuras."""
    k = (int(t.z) + int(t.y) + int(t.x)) % 3
    return tom(OURO, (2, 3, 1)[k])


def nucleo(t):
    return mosqueado(VERMELHO, 2, t, 0.12)


def brilha(rgb):
    return rgb in OURO[3:] or rgb in LARANJA or rgb in (ROXO[3], ROXO[4])


# ---------------------------------------------------------------------------------------------------------------
# Montagem (pose neutra; medidas da vista de frente da ficha: quadril a 47%, joelho a 27%, ombros a 68% da altura)
# ---------------------------------------------------------------------------------------------------------------
def montar():
    m = Modelo("pirococo", 128, 64)
    raiz = m.osso("pirococo")

    # ---------------- pernas longas: coxa roxa, greva prateada com joelheira, pé roxo com garras de ouro
    perna = m.osso("perna_e", raiz, pivo=(2, 21, 0))
    m.cubo(perna, (1, 13, -1.5), (2, 8, 3), roxo_escamas)
    canela = m.osso("canela_e", perna, pivo=(2, 13, 0))
    m.cubo(canela, (1, 3, -1), (2, 10, 2), roxo_escamas)
    m.cubo(canela, (0.5, 5, -1.5), (3, 6, 3), armadura(), inflate=0.01)
    m.cubo(canela, (0.5, 11, -2), (3, 3, 2), armadura(), inflate=0.02)
    pe = m.osso("pe_e", canela, pivo=(2, 3, 0))
    m.cubo(pe, (0.5, 0, -2), (3, 3, 4), roxo_escamas)
    d1 = m.cubo(pe, (0, 0, -5), (1, 1, 3), dedo)
    m.cubo(pe, (1.5, 0, -5.5), (1, 1, 3), None, uv_de=d1)
    m.cubo(pe, (3, 0, -5), (1, 1, 3), None, uv_de=d1)
    m.cubo(pe, (1.5, 0, 2), (1, 1, 2), dedo)
    m.espelhar(perna)

    # ---------------- corpo
    corpo = m.osso("corpo", raiz, pivo=(0, 21, 0))
    m.cubo(corpo, (-3, 19, -2), (6, 3, 4), cinto)
    tg = m.osso("tanga_brilho", corpo, pivo=(0, 19, -2))
    m.cubo(tg, (-1.5, 14, -2.1), (3, 5, 0), tanga, brilho=lambda rgb: rgb in (ROXO[2], ROXO[3]))
    m.cubo(corpo, (-2.5, 22, -1.5), (5, 8, 3), tronco)
    pt = m.osso("peitoral_brilho", corpo, pivo=(0, 28, -2))
    m.cubo(pt, (-3, 27, -2), (6, 3, 4), peitoral, brilho=lambda rgb: rgb in (ROXO[2], ROXO[3]))
    ombro = m.osso("ombro_e", corpo, pivo=(3, 29, 0), rot=(0, 0, 12))
    m.cubo(ombro, (2.5, 28, -2.5), (4, 3, 5), ombreira)
    m.cubo(ombro, (3, 31, -2), (3, 1, 4), armadura())
    m.espelhar(ombro)

    # ---------------- manto (asas como capa): placas finas + penas de fogo na barra
    # (no .geo.json, rz negativo inclina para +x o que pende para baixo: no lado esquerdo, abre o manto para fora)
    manto_c = m.osso("manto", corpo, pivo=(0, 30, 2.5))
    m.cubo(manto_c, (-5, 11, 2), (10, 19, 1), manto)
    pena_m = None
    for k, x in enumerate((-6, -3.5, -1, 1.5, 4)):            # franja de chamas sobrepostas (1,5 px)
        p = m.osso(f"manto_pena{k + 1}", manto_c, pivo=(x + 2, 11, 2.5), rot=(10 - 6 * (k % 2), 0, (2 - k) * 5))
        if pena_m is None:
            pena_m = m.cubo(p, (x, 0, 2.8 + 0.05 * k), (4, 11, 0), pena(CHAMA, 3.6, 8.6, eixo="-y", ponta=0.45))
        else:
            m.cubo(p, (x, 0, 2.8 + 0.05 * k), (4, 11, 0), None, uv_de=pena_m)
    # placa lateral presa na frente do ombro, girada ~50° para mostrar a face larga de frente e de lado
    manto_e = m.osso("manto_e", corpo, pivo=(4.5, 30, -1.5), rot=(0, 42, -14))
    m.cubo(manto_e, (4, 11, -1.5), (1, 19, 8), manto)
    pena_l = None
    for k, z in enumerate((-1.5, 0.5, 2.5, 4.5)):
        p = m.osso(f"manto_e_pena{k + 1}", manto_e, pivo=(4.5, 11, z + 1.5), rot=(4 * k, 0, -3 * k))
        if pena_l is None:
            pena_l = m.cubo(p, (4.5 + 0.05 * k, 0, z), (0, 11, 3), pena(CHAMA, 3.6, 8.6, eixo="-y", ponta=0.45))
        else:
            m.cubo(p, (4.5 + 0.05 * k, 0, z), (0, 11, 3), None, uv_de=pena_l)
    m.espelhar(manto_e)

    # ---------------- pescoço, cabeça, elmo, crista de chamas
    pesc = m.osso("pescoco", corpo, pivo=(0, 30, -0.5))
    m.cubo(pesc, (-1.5, 30, -2), (3, 5, 3), pescoco)
    cab = m.osso("cabeca", pesc, pivo=(0, 34.5, -1))
    m.cubo(cab, (-2.5, 34, -4), (5, 5, 6), cabeca)
    olho_e = m.osso("olho_e", cab, pivo=(1.5, 37, -3))
    m.cubo(olho_e, (0.51, 36, -4.01), (2, 2, 2), olho)
    palp = m.osso("palpebra_e", olho_e, pivo=(1.5, 37, -3))
    m.cubo(palp, (0.41, 36, -3.91), (2, 2, 2), palpebra, inflate=0.02)
    m.espelhar(olho_e)
    b = m.osso("bico", cab, pivo=(0, 36.5, -4))
    m.cubo(b, (-1, 35, -8), (2, 2, 4), bico)
    m.cubo(b, (-1, 34, -9), (2, 2, 1), gancho)
    bb = m.osso("bico_baixo", cab, pivo=(0, 35, -4))
    m.cubo(bb, (-1, 34.5, -6), (2, 1, 2), bico_baixo)

    elmo_o = m.osso("elmo", cab, pivo=(0, 38, -1))
    m.cubo(elmo_o, (-3, 38.5, -4.5), (6, 2, 7), elmo)
    ge = m.osso("elmo_gema_brilho", elmo_o, pivo=(0, 39, -4.5))
    m.cubo(ge, (-0.5, 38.5, -5.1), (1, 2, 1), gema, brilho=True)
    ch1 = m.osso("chifre_e_brilho", elmo_o, pivo=(2, 40, -3), rot=(-12, 0, 16))
    m.cubo(ch1, (0.5, 40, -3), (3, 7, 0), pena(CHAMA, 6.4, 8.6, eixo="y", ponta=0.35, sombra=0.6), brilho=brilha)
    ch1b = m.osso("chifre_e_x_brilho", ch1, pivo=(2, 40, -3), rot=(0, 90, 0))
    m.cubo(ch1b, (0.5, 40, -3), (3, 7, 0), None, uv_de=ch1.cubos[0], brilho=brilha)
    m.espelhar(ch1)

    crista = m.osso("crista", cab, pivo=(0, 38, 1))
    m.cubo(crista, (-2, 34.5, 1.5), (4, 4, 2), nucleo)
    pena_c = None
    for k, (y, rx) in enumerate(((40, 58), (39, 34), (37.5, 12), (36, -10))):
        p = m.osso(f"crista_e{k + 1}_brilho", crista, pivo=(1.5, y, 1.5), rot=(rx, 38, 0))
        if pena_c is None:
            pena_c = m.cubo(p, (1.5, y - 2, 1.5), (0, 4, 8), pena(CHAMA, 5.4, 8.6, ponta=0.15, raiz=0.3, sombra=0.6),
                            brilho=brilha)
        else:
            m.cubo(p, (1.5, y - 2, 1.5), (0, 4, 8), None, uv_de=pena_c, brilho=brilha)
        m.espelhar(p, pai=crista)
    for k, rx in enumerate((72, 45)):
        p = m.osso(f"crista_c{k + 1}_brilho", crista, pivo=(0, 40, 0), rot=(rx, 0, 0))
        m.cubo(p, (0, 38, 0), (0, 4, 8), None, uv_de=pena_c, brilho=brilha)

    # ---------------- cauda tripla estilo Ikki: cordões trançados de ouro com tufo de chama e losango roxo
    cauda = m.osso("cauda", corpo, pivo=(0, 21, 3.5))
    elo = tufo = None
    for nome, x, ry in (("cauda_e", 2, 14), ("cauda_c", 0, 0), ("cauda_d", -2, -14)):
        pai = cauda
        for k, rx in enumerate((-64, 8, 8)):
            o = m.osso(f"{nome}{k + 1}", pai, pivo=(x, 21, 3.5 + 3 * k), rot=(rx, ry if k == 0 else 0, 0))
            if elo is None: elo = m.cubo(o, (x - 1, 20, 3.5 + 3 * k), (2, 2, 3), cordao)
            else: m.cubo(o, (x - 1, 20, 3.5 + 3 * k), (2, 2, 3), None, uv_de=elo)
            pai = o
        t = m.osso(f"{nome}_tufo_brilho", pai, pivo=(x, 21, 12.5), rot=(4, 0, 0))
        if tufo is None:
            tufo = m.cubo(t, (x, 18, 12.5), (0, 6, 8), pena(CHAMA, 5.0, 8.6, ponta=0.4, raiz=0.35, losango=(0.3, 1.3)),
                          brilho=brilha)
        else:
            m.cubo(t, (x, 18, 12.5), (0, 6, 8), None, uv_de=tufo, brilho=brilha)
        tx = m.osso(f"{nome}_tufo2_brilho", t, pivo=(x, 21, 12.5), rot=(0, 0, 90))
        m.cubo(tx, (x, 18, 12.5), (0, 6, 8), None, uv_de=tufo, brilho=brilha)
    return m


# ---------------------------------------------------------------------------------------------------------------
# Animações
# ---------------------------------------------------------------------------------------------------------------
PISCA = {0.0: [0, 0, 0], 2.95: [0, 0, 0], 3.0: None, 3.12: None, 3.17: [0, 0, 0],
         6.15: [0, 0, 0], 6.2: None, 6.32: None, 6.37: [0, 0, 0], 8.0: [0, 0, 0]}


def piscar_keys(lado):
    fechado = [0.1 if lado == "e" else -0.1, 0, -0.1]
    return {t: (fechado if v is None else v) for t, v in PISCA.items()}


def animacoes(m):
    nomes = sorted(o.nome for o in m.ossos)
    crista = [n for n in nomes if n.startswith("crista_")]
    cauda = [n for n in nomes if n.startswith("cauda_") and "tufo" not in n]
    tufos = [n for n in nomes if "tufo_brilho" in n]
    penas = [n for n in nomes if "_pena" in n]

    def cascata(nome):          # fase extra por elo (o movimento escorre até a ponta)
        return 30 * int(nome[-1]) if nome[-1].isdigit() else 90

    parado = {
        "corpo": {"position": canal(y=onda(0.25, 1)), "rotation": canal(x=onda(1, 1, 30))},
        "pescoco": {"rotation": canal(x=onda(2, 1, 45))},
        "cabeca": {"rotation": canal(x=onda(-2, 1, 90), y=onda(7, 0.5, 0))},
        "manto": {"rotation": canal(x=onda(-1.5, 1, 30))},
        "manto_e": {"rotation": canal(z=onda(-1.5, 1, 45))}, "manto_d": {"rotation": canal(z=onda(1.5, 1, 45))},
        "palpebra_e": {"position": piscar_keys("e")}, "palpebra_d": {"position": piscar_keys("d")},
    }
    for i, n in enumerate(crista): parado[n] = {"rotation": canal(x=onda(5, 2, 20 + 30 * (i % 4)))}
    for n in cauda: parado[n] = {"rotation": canal(x=onda(4, 1, cascata(n)), y=onda(4, 0.5, cascata(n)))}
    for n in tufos: parado[n] = {"rotation": canal(x=onda(6, 2, 120))}
    for n in penas: parado[n] = {"rotation": canal(x=onda(2.5, 1, 60 + cascata(n)))}

    perna = lambda f: onda(24, 4, f)
    joelho = lambda f: (lambda t: 26 * max(0.0, math.sin(math.radians(t * 360 - f))))
    andar = {
        "perna_e": {"rotation": canal(x=perna(0))}, "perna_d": {"rotation": canal(x=perna(180))},
        "canela_e": {"rotation": canal(x=joelho(90))}, "canela_d": {"rotation": canal(x=joelho(270))},
        "pe_e": {"rotation": canal(x=lambda t: -0.5 * 24 * math.sin(math.radians(t * 360)))},
        "pe_d": {"rotation": canal(x=lambda t: -0.5 * 24 * math.sin(math.radians(t * 360 - 180)))},
        "corpo": {"position": canal(y=onda(0.5, 8, 90, -0.3)), "rotation": canal(x=3, z=onda(2, 4, 0))},
        "pescoco": {"rotation": canal(x=onda(8, 8, 0))},
        "cabeca": {"rotation": canal(x=onda(-6, 8, 40))},
        "manto": {"rotation": canal(x=onda(-4, 8, 60, -4))},
        "manto_e": {"rotation": canal(z=onda(-3, 8, 60))}, "manto_d": {"rotation": canal(z=onda(3, 8, 60))},
    }
    for n in crista: andar[n] = {"rotation": canal(x=onda(6, 8, 60))}
    for n in cauda: andar[n] = {"rotation": canal(x=onda(6, 8, 60 + cascata(n)), y=onda(6, 4, cascata(n)))}
    for n in tufos: andar[n] = {"rotation": canal(x=onda(8, 8, 150))}
    for n in penas: andar[n] = {"rotation": canal(x=onda(5, 8, 90 + cascata(n)))}

    piscar = {"palpebra_e": {"position": {0.0: [0.1, 0, -0.1], 0.125: [0.1, 0, -0.1], 0.1667: [0, 0, 0]}},
              "palpebra_d": {"position": {0.0: [-0.1, 0, -0.1], 0.125: [-0.1, 0, -0.1], 0.1667: [0, 0, 0]}}}

    pico = lambda v: (lambda t: v * (min(1, t / 0.25) if t < 0.25 else 1 if t < 1.2 else max(0, (1.5 - t) / 0.3)))
    grito = {
        "pescoco": {"rotation": canal(x=pico(-12))}, "cabeca": {"rotation": canal(x=pico(-24))},
        "bico_baixo": {"rotation": canal(x=pico(35))}, "corpo": {"rotation": canal(x=pico(-5))},
        "manto_e": {"rotation": canal(z=pico(-28))}, "manto_d": {"rotation": canal(z=pico(28))},
    }
    for n in crista: grito[n] = {"rotation": canal(x=pico(-14))}

    dormir = {
        "corpo": {"position": canal(y=onda(0.25, 1, 0, -9)), "rotation": canal(x=-3)},
        "perna_e": {"position": canal(y=-9)}, "perna_d": {"position": canal(y=-9)},
        "pescoco": {"rotation": canal(x=28, y=18)}, "cabeca": {"rotation": canal(x=onda(1.5, 1, 45, 20), y=25)},
        "palpebra_e": {"position": canal(0.1, 0, -0.1)}, "palpebra_d": {"position": canal(-0.1, 0, -0.1)},
        "manto_e": {"rotation": canal(z=8)}, "manto_d": {"rotation": canal(z=-8)},
    }

    # pose da arte da ficha: de pé, cabeça virada e um pouco baixa, manto entreaberto, caudas erguidas para trás
    render = {
        "cabeca": {"rotation": canal(x=8, y=-28)}, "pescoco": {"rotation": canal(x=-6, y=-8)},
        "manto_e": {"rotation": canal(z=-14)}, "manto_d": {"rotation": canal(z=6)},
        "perna_e": {"rotation": canal(z=-3)}, "perna_d": {"rotation": canal(z=3)},
    }
    # caudas em leque vertical para trás, como na arte: a de cima sobe, a do meio vai reta, a de baixo desce
    ergue = {"cauda_e": 72, "cauda_c": 56, "cauda_d": 40}
    for n in cauda:
        base = n[:-1]
        if n[-1] == "1":
            desfaz = -14 if base == "cauda_e" else 14 if base == "cauda_d" else 0     # junta as 3 no mesmo plano
            render[n] = {"rotation": canal(x=ergue[base], y=desfaz)}
        else:
            render[n] = {"rotation": canal(x=6 if n[-1] == "2" else -10)}
    for n in tufos:
        render[n] = {"rotation": canal(x=-25)}
    return {
        "idle": gravar(8.0, parado, passo=0.1),
        "walk": gravar(1.0, andar, passo=1 / 24),
        "blink": gravar(0.1667, piscar, loop=False),
        "cry": gravar(1.5, grito, passo=0.05, loop=False),
        "sleep": gravar(8.0, dormir, passo=0.2),
        "render": gravar(0.0, render, passo=1.0, loop=False),
    }


# ---------------------------------------------------------------------------------------------------------------
# Revisão
# ---------------------------------------------------------------------------------------------------------------
def revisar(prefixo):
    import analisar_geo as ag, comparar_arte as ca, previa2
    from PIL import Image
    geo = ag.carregar_geo(PASTA / "pirococo.geo.json"); tex = ag.carregar_textura(PASTA / "pirococo.png")
    anims = json.loads((PASTA / "pirococo.animation.json").read_text(encoding="utf-8"))["animations"]
    REVISAO.mkdir(parents=True, exist_ok=True)
    repouso = ag.faces(geo, tex)
    ag.folha_vistas(repouso, 10, "pose de modelagem").save(REVISAO / f"{prefixo}_vistas.png")
    parado = ag.faces(geo, tex, ag.pose(anims["animation.pirococo.idle"], 0))
    ag.folha_vistas(parado, 10, "parado (t=0)").save(REVISAO / f"{prefixo}_parado.png")
    ag.folha_vistas(ag.faces(geo, tex, ag.pose(anims["animation.pirococo.walk"], 0.25)), 10, "andar (t=0,25)").save(
        REVISAO / f"{prefixo}_andar.png")
    sel = [f for f in parado[0] if f[0][0][1] > 31]
    previa2.desenhar((sel, tex), 30, -5, escala=30, fundo=ag.FUNDO).save(REVISAO / f"{prefixo}_rosto.png")
    # vistas da ficha (em cima) x vistas do modelo (embaixo), na mesma ordem: frente, direita, trás, esquerda
    vistas = Image.open(RAIZ / "modelos/referencias/001_pirococo_g3_vistas.png").convert("RGB")
    H = vistas.height
    ims = [previa2.desenhar(parado, y, -3, escala=10, margem=6, fundo=(0, 0, 0)) for y in (0, -90, 180, 90)]
    ims = [i.resize((int(i.width * (H - 40) / i.height), H - 40), Image.LANCZOS) for i in ims]
    folha = Image.new("RGB", (max(vistas.width, sum(i.width for i in ims)), 2 * H), (0, 0, 0))
    folha.paste(vistas, (0, 0)); x = 0
    for i in ims: folha.paste(i, (x, H + 10)); x += i.width
    folha.save(REVISAO / f"{prefixo}_vistas_ficha.png")
    # pose da arte (render) x arte: ângulo de maior sobreposição
    dados_r = ag.faces(geo, tex, ag.pose(anims["animation.pirococo.render"], 0))
    arte = Image.open(ARTE)
    v, yaw, pitch, esp = ca.melhor_angulo(dados_r, ca.normalizar(ca.silhueta_arte(arte)),
                                          yaws=range(-90, 91, 10), pitches=(-10, 0, 10))     # arte vista de frente/3-4
    nota = ca.folha(arte, dados_r, yaw, pitch, esp, REVISAO / f"{prefixo}_arte.png", "Pirococó: arte da ficha x pose render")
    lo, hi = ag.limites(parado)
    print(f"medidas (parado): altura {(hi[1] - min(lo[1], 0)) / 16:.2f}, largura {(hi[0] - lo[0]) / 16:.2f}, "
          f"comprimento {(hi[2] - lo[2]) / 16:.2f} blocos (ficha: 2,5 a 3,0 de altura)")
    print(f"arte x render: IoU {100 * nota:.0f}% (yaw {yaw}, pitch {pitch}, espelhado {esp})")
    est = ag.conferir_estilo(geo, tex, repouso, anims, 1.0)
    print(f"estilo: {sum(b for *_, b in est)}/{len(est)}")
    for c, alvo, v, ok in est:
        if not ok: print(f"  NÃO {c}: {v} (alvo {alvo})")


def exportar_mod():
    """Copia geometria, textura, brilho e animações para o mod (substitui o Pirococó anterior)."""
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

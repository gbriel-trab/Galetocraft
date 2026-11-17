"""5 galos de briga monstruosos, pegada dark, cada um inspirado no TEMA de um Pokémon popular
(criaturas originais, sem copiar os personagens).

Saída: modelos/galos_monstro/<nome>.bbmodel + <nome>.png + <nome>_previa.png + grupo.png
Formato: Blockbench "Modded Entity" (box UV), pronto para virar entidade no Fabric/NeoForge.
Coordenadas: Y para cima (chão = 0), frente do bicho = -Z."""
import base64, io, json, random, sys, uuid
from pathlib import Path
from PIL import Image, ImageDraw

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI.parent / "modelos" / "galos_monstro"
SAIDA.mkdir(parents=True, exist_ok=True)
RNG = random.Random(7)

def r(x):
    return x[RNG.randrange(len(x))] if isinstance(x, list) else x

# =====================================================================================
# Infra: cubos, ossos, empacotar box UV, pintar textura, salvar .bbmodel
# =====================================================================================
class Modelo:
    def __init__(self, nome):
        self.nome, self.cubos = nome, {}

    def cubo(self, nome, de, ate, pintor=None, espelho_de=None, uv_de=None):
        assert nome not in self.cubos, f"nome repetido: {nome}"
        # box UV exige tamanho inteiro: arredonda cada lado (0,5 para cima) mantendo o centro da peça
        de, ate = list(de), list(ate)
        for i in range(3):
            tam = ate[i] - de[i]
            if tam > 1e-6 and abs(tam - round(tam)) > 1e-6:
                novo = max(1, int(tam + 0.5)); centro = (de[i] + ate[i]) / 2
                de[i], ate[i] = centro - novo / 2, centro + novo / 2
        w, h, d = (int(round(ate[i] - de[i])) for i in range(3))
        self.cubos[nome] = {"name": nome, "from": list(de), "to": list(ate), "size": (w, h, d),
                            "pintor": pintor, "espelho_de": espelho_de, "uv_de": uv_de,
                            "uuid": str(uuid.uuid4())}
        return self.cubos[nome]["uuid"]

    def osso(self, nome, origem, rot, filhos):
        return {"name": nome, "origin": list(origem), "rotation": list(rot), "color": 0,
                "uuid": str(uuid.uuid4()), "export": True, "mirror_uv": False, "isOpen": True,
                "locked": False, "visibility": True, "autouv": 0,
                "children": [f for f in filhos if f is not None]}

    def salvar(self, outliner, largura=64, pasta=None):
        pasta = Path(pasta) if pasta else SAIDA
        pasta.mkdir(parents=True, exist_ok=True)
        cubos = self.cubos
        net = lambda c: (2 * c["size"][2] + 2 * c["size"][0], c["size"][2] + c["size"][1])
        proprios = [c for c in cubos.values() if not c["espelho_de"] and not c["uv_de"]]
        proprios.sort(key=lambda c: (-net(c)[1], -net(c)[0]))
        x = y = lh = 0
        for c in proprios:
            nw, nh = net(c)
            if x + nw > largura:
                x, y, lh = 0, y + lh, 0
            c["uv_offset"] = [x, y]; x += nw; lh = max(lh, nh)
        altura = 64
        while altura < y + lh: altura *= 2
        def origem(c):
            ref = c["espelho_de"] or c["uv_de"]
            return list(c["uv_offset"]) if not ref else origem(cubos[ref])
        for c in cubos.values():
            c["uv_offset"] = origem(c)
            ref = c["espelho_de"] or c["uv_de"]
            if ref: assert cubos[ref]["size"] == c["size"], f"{c['name']} != {ref}"

        img = Image.new("RGBA", (largura, altura), (0, 0, 0, 0)); px = img.load()
        for c in proprios:
            w, h, d = c["size"]; u, v = c["uv_offset"]; pint = c["pintor"]
            regs = [("side", u, v + d, d, h, lambda i, j: (d - 1 - i, j)),
                    ("north", u + d, v + d, w, h, lambda i, j: (i, j)),
                    ("side", u + d + w, v + d, d, h, lambda i, j: (i, j)),
                    ("south", u + 2 * d + w, v + d, w, h, lambda i, j: (i, j)),
                    ("up", u + d, v, w, d, lambda i, j: (d - 1 - j, i)),
                    ("down", u + d + w, v, w, d, lambda i, j: (d - 1 - j, i))]
            for face, x0, y0, W, H, mapa in regs:
                for i in range(W):
                    for j in range(H):
                        s, t = mapa(i, j)
                        cor = pint(face, s, t, w, d) if face in ("up", "down") else pint(face, s, t, W, H)
                        px[x0 + i, y0 + j] = (0, 0, 0, 0) if cor is None else tuple(cor) + (255,)
        img.save(pasta / f"{self.nome}.png")
        buf = io.BytesIO(); img.save(buf, format="PNG")

        def faces(c, mirror):
            w, h, d = c["size"]; u, v = c["uv_offset"]
            fl = {"east": [[0, d], [d, h]], "west": [[d + w, d], [d, h]],
                  "up": [[d + w, d], [-w, -d]], "down": [[d + 2 * w, 0], [-w, d]],
                  "south": [[2 * d + w, d], [w, h]], "north": [[d, d], [w, h]]}
            if mirror:
                for f in fl.values(): f[0][0] += f[1][0]; f[1][0] *= -1
                fl["east"], fl["west"] = fl["west"], fl["east"]
            return {k: {"uv": [f[0][0] + u, f[0][1] + v, f[0][0] + f[1][0] + u, f[0][1] + f[1][1] + v],
                        "texture": 0} for k, f in fl.items()}
        elements = [{"name": c["name"], "box_uv": True, "rescale": False, "locked": False,
                     "from": c["from"], "to": c["to"], "autouv": 0, "color": 0, "origin": [0, 0, 0],
                     "uv_offset": c["uv_offset"], "mirror_uv": bool(c["espelho_de"]),
                     "faces": faces(c, bool(c["espelho_de"])), "type": "cube", "uuid": c["uuid"]}
                    for c in cubos.values()]
        bb = {"meta": {"format_version": "4.10", "model_format": "modded_entity", "box_uv": True},
              "name": self.nome, "model_identifier": self.nome, "modded_entity_entity_class": "",
              "modded_entity_version": "1.17", "modded_entity_flip_y": True, "visible_box": [1, 1, 0],
              "resolution": {"width": largura, "height": altura}, "elements": elements, "outliner": outliner,
              "textures": [{"path": "", "name": f"{self.nome}.png", "folder": "entity", "namespace": "", "id": "0",
                            "width": largura, "height": altura, "uv_width": largura, "uv_height": altura,
                            "particle": False, "render_mode": "default", "visible": True, "internal": True,
                            "saved": False, "uuid": str(uuid.uuid4()), "relative_path": "",
                            "source": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()}],
              "animations": []}
        caminho = pasta / f"{self.nome}.bbmodel"
        caminho.write_text(json.dumps(bb, indent=1), encoding="utf-8")
        return caminho, len(elements), (largura, altura)

# =====================================================================================
# Pintores genéricos: arte em pixels (planos finos com recorte) e fogo
# =====================================================================================
def arte(desenho, cores, modo):
    """Plano fino pintado a partir de 'desenho' (lista de strings; '.' = transparente).
    modo 'x': plano visto de lado (coluna 0 = frente); modo 'z': plano visto de frente."""
    def p(face, s, t, W, H):
        if (modo == "x" and face != "side") or (modo == "z" and face not in ("north", "south")):
            return None
        ch = desenho[t][s]
        return None if ch == "." else r(cores[ch])
    return p

def _fogo(cores, f):
    return cores[0] if f < .34 else (cores[1] if f < .7 else cores[2])

def fogo_sobe(cores, alturas=(2, 5, 3, 4)):
    def p(face, s, t, W, H):
        if face in ("up", "down"): return None
        alt = min(alturas[s % len(alturas)], H); hb = H - t
        return None if hb > alt else _fogo(cores, (hb - 1) / max(alt - 1, 1))
    return p

def fogo_jato(cores, comps=(3, 6, 5, 2)):
    def p(face, s, t, W, H):
        if face != "side": return None
        L = min(comps[t % len(comps)], W); de_tras = W - 1 - s
        return None if de_tras >= L else _fogo(cores, de_tras / max(L - 1, 1))
    return p

def efeito_boca(m, cores, simbolo=None, cores_simbolo=None, jato=True, cantos=True, prefixo="boca"):
    """Símbolo recortado no meio da boca aberta + jato e labaredas nos cantos."""
    SY = 19.5
    filhos = []
    if simbolo:
        filhos.append(m.cubo(f"{prefixo}_simbolo", [-3.5, SY - 3.5, -11], [3.5, SY + 3.5, -11],
                             arte(simbolo, cores_simbolo, "z")))
    if jato:
        filhos.append(m.cubo(f"{prefixo}_jato", [0, SY - 2, -17], [0, SY + 2, -11], fogo_jato(cores)))
    if cantos:
        for lado, x, ang in (("d", -2.5, 30), ("e", 2.5, -30)):
            kw = dict(pintor=fogo_sobe(cores)) if lado == "d" else dict(uv_de=f"{prefixo}_canto_d")
            filhos.append(m.osso(f"{prefixo}_canto_{lado}", [x, 17, -9], [0, ang, 0],
                                 [m.cubo(f"{prefixo}_canto_{lado}", [x, 16.5, -12], [x, 21.5, -8], **kw)]))
    return m.osso(f"{prefixo}_efeito", [0, SY, -11], [0, 0, 0], filhos)

# =====================================================================================
# Paleta padrão e anatomia base (corpo, garras, cabeça monstruosa com mandíbulas/dentes)
# =====================================================================================
PADRAO = dict(
    escuro=[(24, 26, 30), (32, 36, 40)], brilho=[(40, 74, 56)],
    gola=[(226, 128, 36), (210, 108, 30)], gola_clara=[(252, 192, 86)], gola_listra=None,
    costas=[(150, 40, 26), (128, 32, 22)], asa_baixo=[(196, 112, 50)], faixa=None,
    pele=[(214, 58, 52), (200, 48, 46)], pele_esc=[(150, 30, 32), (132, 24, 28)],
    crista=[(212, 40, 40), (176, 28, 32)],
    perna=[(224, 184, 70), (210, 166, 56)], perna_esc=(170, 128, 40),
    bico=[(96, 88, 80), (82, 74, 68)], bico_esc=(50, 44, 40),
    unha=[(74, 68, 64), (54, 50, 48)], unha_brilho=(138, 128, 116), espora=(238, 230, 206),
    olho=(255, 250, 150), olho_fundo=(255, 150, 30), olheira=(46, 10, 14), cicatriz=(236, 156, 146),
    dente=(246, 242, 226), dente_base=(214, 200, 160),
    boca=[(255, 236, 110), (255, 146, 30), (228, 60, 22)],
    cauda=[(24, 26, 30), (32, 36, 40)], cauda_brilho=[(40, 74, 56)], cauda_faixa=None,
)

def montar(m, P, o):
    P = {**PADRAO, **P}
    listra = P["gola_listra"] or P["gola_clara"]
    lado_extra = o.get("lado_extra", lambda s, t: None)

    # ---------- pintores da anatomia ----------
    def p_tronco(face, s, t, W, H):
        if face == "north":
            if t == 0 and 1 <= s <= W - 2: return r(P["gola"])
            return r(P["brilho"]) if RNG.random() < .15 else r(P["escuro"])
        if face == "side":
            if s <= 1 and t <= 2: return r(P["gola"])
            if t <= 1: return r(P["costas"])
            if t == 2: return r(P["costas"]) if RNG.random() < .5 else r(P["escuro"])
            return r(P["brilho"]) if RNG.random() < .12 else r(P["escuro"])
        if face == "south":
            if t <= 1: return r(listra) if RNG.random() < .35 else r(P["gola"])
            return r(P["escuro"])
        if face == "up":
            if s <= 2 or s >= H - 2: return r(P["gola"])
            return r(P["costas"])
        return r(P["escuro"])

    def p_asa(face, s, t, W, H):
        if face == "side":
            if s >= W - 2 and t >= 2: return r(P["escuro"])
            if t <= 1: return r(P["costas"])
            if t == 2: return r(P["faixa"]) if P["faixa"] else (r(P["brilho"]) if RNG.random() < .5 else r(P["escuro"]))
            return r(P["asa_baixo"])
        return r(P["escuro"]) if face == "down" else r(P["costas"])

    def p_coxa(face, s, t, W, H):
        return r(P["brilho"]) if RNG.random() < .2 and t < H - 1 else r(P["escuro"])
    def p_canela(face, s, t, W, H): return P["perna"][t % len(P["perna"])]
    def p_dedo(face, s, t, W, H):
        return P["perna_esc"] if face == "down" else P["perna"][s % len(P["perna"])]
    def p_unha(face, s, t, W, H): return P["unha_brilho"] if face == "up" else r(P["unha"])
    def p_espora(face, s, t, W, H):
        return P["unha"][0] if (face == "side" and s == W - 1) or face == "south" else P["espora"]
    def p_pescoco(face, s, t, W, H):
        if face in ("up", "down"): return r(P["gola"])
        if t <= 1 and RNG.random() < .5: return r(P["costas"])
        return r(listra) if (s + t // 3) % 2 == 0 else r(P["gola"])
    def p_capa(face, s, t, W, H):
        if face in ("up", "down"): return r(P["gola"])
        if t == H - 1: return r(P["gola_clara"])
        return r(listra) if s % 2 == 0 else r(P["gola"])
    def p_juba(face, s, t, W, H):
        if face == "down": return None
        if face == "up": return r(P["gola"])
        if t == H - 1: return r(P["gola_clara"]) if s % 2 == 0 else None
        if t == 0: return r(P["costas"])
        return r(listra) if s % 2 == 0 else r(P["gola"])
    def p_cabeca(face, s, t, W, H):
        if face == "north":
            if t == 0: return r(P["pele_esc"])
            if t == 2 and s in (0, W - 1): return P["olho"]
            if t == 3 and s in (0, W - 1): return P["olheira"]
            if t == 4 and 1 <= s <= W - 2: return P["boca"][0]
            if t >= 4: return P["boca"][2]
            return r(P["pele_esc"]) if RNG.random() < .2 else r(P["pele"])
        if face == "down": return r(P["pele_esc"])
        if face == "side":
            if (s, t) == (0, 2): return P["olho"]
            if (s, t) == (1, 2): return P["olho_fundo"]
            if (s, t) in ((2, 2), (0, 3), (1, 3), (2, 3)): return P["olheira"]
            ex = lado_extra(s, t)
            if ex: return ex
            if P["cicatriz"] and (s, t) in ((3, 1), (4, 2), (4, 3), (5, 4)): return P["cicatriz"]
            if t == 4 and s <= 2: return P["boca"][2]
            if s <= 3: return r(P["pele_esc"]) if RNG.random() < .25 else r(P["pele"])
            if t == 0: return r(P["costas"])
            return r(listra) if (s + t) % 3 == 0 else r(P["gola"])
        if face == "up":
            return r(P["pele"]) if s <= 2 else r(P["costas"])
        return r(P["gola"])
    def p_testa(face, s, t, W, H): return r(P["crista"]) if face == "up" else r(P["pele_esc"])
    def p_dente_cima(face, s, t, W, H):
        return P["dente"] if face == "down" or (face != "up" and t == H - 1) else P["dente_base"]
    def p_dente_baixo(face, s, t, W, H):
        return P["dente"] if face == "up" or (face != "down" and t == 0) else P["dente_base"]
    def p_bico_cima(face, s, t, W, H):
        if face == "down": return P["boca"][1] if (s + t) % 2 else P["boca"][2]
        if face == "north" or (face in ("side", "up") and s == 0): return P["bico_esc"]
        return r(P["bico"])
    def p_bico_baixo(face, s, t, W, H):
        if face == "up": return P["boca"][0] if 0 < t < W - 1 and 0 < s < H - 1 else P["boca"][2]
        if face == "north" or (face == "side" and s == 0): return P["bico_esc"]
        return r(P["bico"])
    def p_crista(face, s, t, W, H): return r(P["crista"])
    def p_cauda(face, s, t, W, H):
        if P["cauda_faixa"] and face == "side" and s in (2, 3): return r(P["cauda_faixa"])
        if face == "up" or (face == "side" and t == 0): return r(P["cauda_brilho"])
        return r(P["cauda"])

    # ---------- pernas com garras ----------
    def pe(lado):
        x = 1.5 * lado; e = "_d" if lado < 0 else "_e"
        def c(nome, de, ate, pintor=None, uv_de=None):
            de = [de[0] + x, de[1], de[2]]; ate = [ate[0] + x, ate[1], ate[2]]
            if lado > 0: return m.cubo(nome + e, de, ate, espelho_de=nome + "_d")
            return m.cubo(nome + e, de, ate, pintor, uv_de=(uv_de + "_d") if uv_de else None)
        abre = 28 * lado
        return [
            c("coxa", [-1, 6, -1], [1, 9, 2], p_coxa),
            c("canela", [-0.5, 2, 0], [0.5, 6, 1], p_canela),
            m.osso("dedo_meio" + e, [x, 1.5, 0.5], [0, 0, 0], [
                c("dedo_meio", [-0.5, 1, -3], [0.5, 2, 1], p_dedo),
                c("unha_meio", [-0.5, 1, -5], [0.5, 2, -3], p_unha),
                c("unha_ponta_meio", [-0.5, 0, -5], [0.5, 1, -4], p_unha)]),
            m.osso("dedo_fora" + e, [x, 1.5, 0.5], [0, -abre, 0], [
                c("dedo_fora", [-0.5, 1, -2], [0.5, 2, 1], p_dedo),
                c("unha_fora", [-0.5, 1, -4], [0.5, 2, -2], uv_de="unha_meio"),
                c("unha_ponta_fora", [-0.5, 0, -4], [0.5, 1, -3], uv_de="unha_ponta_meio")]),
            m.osso("dedo_dentro" + e, [x, 1.5, 0.5], [0, abre, 0], [
                c("dedo_dentro", [-0.5, 1, -2], [0.5, 2, 1], uv_de="dedo_fora"),
                c("unha_dentro", [-0.5, 1, -4], [0.5, 2, -2], uv_de="unha_meio"),
                c("unha_ponta_dentro", [-0.5, 0, -4], [0.5, 1, -3], uv_de="unha_ponta_meio")]),
            c("dedo_tras", [-0.5, 1, 1], [0.5, 2, 3], p_dedo),
            c("unha_tras", [-0.5, 0, 3], [0.5, 2, 4], p_unha),
            c("espora", [-0.5, 3, 1], [0.5, 4, 3], p_espora),
        ]

    raiz_extra = []
    if "asas" in o:
        asas = []; raiz_extra += o["asas"](m, P)
    else:
        ex = o.get("asa_extras", lambda m, lado: [])
        asas = [m.osso("asa_direita", [-3, 12, -3], [0, 0, 0],
                       [m.cubo("asa_d", [-4, 8, -3.5], [-3, 12, 3.5], p_asa), *ex(m, -1)]),
                m.osso("asa_esquerda", [3, 12, -3], [0, 0, 0],
                       [m.cubo("asa_e", [3, 8, -3.5], [4, 12, 3.5], espelho_de="asa_d"), *ex(m, 1)])]
    corpo = m.osso("corpo", [0, 10, 0], [30, 0, 0],
                   [m.cubo("tronco", [-3, 7, -4], [3, 13, 4], p_tronco), *asas,
                    *o.get("corpo_extras", lambda m, P: [])(m, P)])

    if "cauda" in o:
        cauda = o["cauda"](m, P)
    else:
        cauda = m.osso("cauda", [0, 10, 4], [-50, 0, 0], [
            m.cubo("cauda_base", [-1.5, 9, 3], [1.5, 11, 8], p_cauda),
            m.osso("foices", [0, 10.5, 8], [30, 0, 0], [
                m.cubo("foice", [-0.5, 9.5, 7], [0.5, 11.5, 12], p_cauda),
                m.cubo("foice_baixa", [-1, 9, 7], [1, 10, 11], p_cauda),
                m.osso("foices_pontas", [0, 10.5, 12], [50, 0, 0], [
                    m.cubo("foice_ponta", [-0.5, 9.5, 11], [0.5, 11.5, 15], p_cauda)])])])

    if "cabeca_extras" in o:
        topo = o["cabeca_extras"](m, P)
    else:
        topo = [m.cubo("crista", [-1, 24, -7], [1, 25, -1], p_crista),
                m.cubo("crista_espinho_1", [-0.5, 25, -7], [0.5, 27, -6], p_crista),
                m.cubo("crista_espinho_2", [-0.5, 25, -5], [0.5, 28, -4], p_crista),
                m.cubo("crista_espinho_3", [-0.5, 25, -3], [0.5, 27, -2], uv_de="crista_espinho_1")]
    cabeca = m.osso("cabeca", [0, 18, -3], [10, 0, 0], [
        m.cubo("cabeca", [-3, 18, -8], [3, 24, -1], p_cabeca),
        m.cubo("testa", [-3, 22, -9], [3, 23, -8], p_testa),
        m.cubo("sobrancelha_d", [-4, 22, -8], [-3, 23, -5], p_testa),
        m.cubo("sobrancelha_e", [3, 22, -8], [4, 23, -5], espelho_de="sobrancelha_d"),
        m.osso("bico_cima", [0, 21, -8], [30, 0, 0], [
            m.cubo("bico_cima", [-2, 20, -13], [2, 22, -8], p_bico_cima),
            m.cubo("bico_gancho", [-1, 19, -13], [1, 20, -12], lambda *a: P["bico_esc"]),
            m.cubo("presa_cima_d", [-2, 18, -12], [-1, 20, -11], p_dente_cima),
            m.cubo("presa_cima_e", [1, 18, -12], [2, 20, -11], uv_de="presa_cima_d"),
            m.cubo("dente_cima_d", [-2, 19, -10], [-1, 20, -9], p_dente_cima),
            m.cubo("dente_cima_e", [1, 19, -10], [2, 20, -9], uv_de="dente_cima_d")]),
        m.osso("bico_baixo", [0, 19, -8], [-45, 0, 0], [
            m.cubo("bico_baixo", [-2, 17, -12], [2, 19, -8], p_bico_baixo),
            m.cubo("presa_baixo_d", [-2, 19, -12], [-1, 21, -11], p_dente_baixo),
            m.cubo("presa_baixo_e", [1, 19, -12], [2, 21, -11], uv_de="presa_baixo_d"),
            m.cubo("dentes_frente", [-1, 19, -12], [1, 20, -11], p_dente_baixo),
            m.cubo("dente_baixo_d", [-2, 19, -10], [-1, 20, -9], p_dente_baixo),
            m.cubo("dente_baixo_e", [1, 19, -10], [2, 20, -9], uv_de="dente_baixo_d")]),
        *topo,
        m.cubo("barbela", [-1.5, 15, -7], [1.5, 18, -6], p_crista) if o.get("barbela", True) else None,
        o["boca"](m, P) if "boca" in o else None,
    ])
    pescoco = m.osso("pescoco", [0, 13, -3], [-10, 0, 0], [
        m.cubo("pescoco", [-2, 12, -5], [2, 18, -1], p_pescoco),
        m.cubo("gola", [-3, 12, -4.5], [3, 15, 0.5], p_capa),
        m.cubo("juba", [-3.5, 15, -6], [3.5, 18, 0], p_juba),
        cabeca])
    perna_d = m.osso("perna_direita", [-1.5, 9, 0.5], [0, 0, 0], pe(-1))
    perna_e = m.osso("perna_esquerda", [1.5, 9, 0.5], [0, 0, 0], pe(+1))
    return [corpo, pescoco, cauda, perna_d, perna_e, *raiz_extra]

# =====================================================================================
# Peças extras reutilizáveis
# =====================================================================================
def orelhas(m, corpo, ponta, faixa=None, altura=7):
    """Duas orelhas/plumas pontudas inclinadas para fora."""
    def p(face, s, t, W, H):
        if t <= 1: return r(ponta)
        if faixa and t in (3, 4): return r(faixa)
        return r(corpo)
    out = []
    for n, x, ang in (("d", -2, 20), ("e", 2, -20)):
        kw = dict(pintor=p) if n == "d" else dict(uv_de="orelha_d")
        out.append(m.osso(f"orelha_{n}", [x, 24, -3], [0, 0, ang],
                          [m.cubo(f"orelha_{n}", [x - 0.5, 24, -4], [x + 0.5, 24 + altura, -2], **kw)]))
    return out

# =====================================================================================
# 1) GALO TROVÃO  (tema: rato elétrico)
# =====================================================================================
RAIO_CAUDA = [
    ".....YYY",
    "....YYYK",
    "...YYYK.",
    "..YYYK..",
    ".YYYYYYY",
    "....YYYK",
    "...YYYK.",
    "..YYK...",
    ".YYK....",
    "KK......",
]
RAIO_SIMBOLO = [
    "...WY..",
    "..WY...",
    ".WYYYY.",
    "...WY..",
    "..WY...",
    ".WY....",
    ".Y.....",
]
def galo_trovao():
    P = dict(escuro=[(34, 32, 36), (28, 27, 30)], brilho=[(52, 48, 40)],
             gola=[(240, 196, 36), (226, 172, 22)], gola_clara=[(255, 226, 90)], gola_listra=[(40, 38, 42)],
             costas=[(40, 38, 42), (34, 32, 36)], asa_baixo=[(226, 172, 22)], faixa=[(255, 214, 40)],
             pele=[(66, 58, 58), (56, 50, 50)], pele_esc=[(34, 30, 32), (28, 24, 26)], crista=[(240, 196, 36)],
             perna=[(196, 156, 40), (178, 138, 30)], perna_esc=(120, 90, 20),
             olho=(255, 250, 170), olho_fundo=(120, 200, 255), cicatriz=None,
             boca=[(255, 255, 225), (255, 224, 60), (90, 170, 255)])
    o = dict(
        barbela=False,
        lado_extra=lambda s, t: (214, 40, 36) if s in (3, 4) and t in (3, 4) else None,   # bochechas elétricas
        cabeca_extras=lambda m, P: orelhas(m, [(240, 196, 36), (226, 172, 22)], [(20, 18, 20)], altura=8),
        cauda=lambda m, P: m.osso("cauda", [0, 10, 4], [-15, 0, 0], [
            m.cubo("cauda_raio", [0, 9, 4], [0, 19, 12],
                   arte(RAIO_CAUDA, {"Y": [(255, 214, 40), (240, 196, 30)], "K": (70, 52, 20)}, "x"))]),
        boca=lambda m, P: efeito_boca(m, P["boca"], RAIO_SIMBOLO,
                                      {"Y": (255, 224, 50), "W": (255, 255, 220)}),
    )
    return "galo_trovao", P, o

# =====================================================================================
# 2) GALO DRACÔNICO  (tema: dragão de fogo)
# =====================================================================================
ASA_MORCEGO = [
    "BBBBBBBBBBBB",
    "BMMMBMMMBMMB",
    "BMMMBMMMBMB.",
    "BMMMBMMMBM..",
    "BMMMBMMMB...",
    "BMMMBMMM....",
    "BMMMBMM.....",
    "BMMMB.......",
    "BMM.........",
]
def galo_draconico():
    P = dict(escuro=[(70, 34, 20), (60, 28, 16)], brilho=[(96, 44, 22)],
             gola=[(196, 86, 24), (176, 68, 20)], gola_clara=[(226, 130, 46)],
             costas=[(110, 46, 22), (96, 38, 18)], asa_baixo=[(150, 66, 28)],
             pele=[(150, 62, 30), (132, 52, 26)], pele_esc=[(72, 28, 16), (60, 24, 14)],
             crista=[(64, 40, 34), (54, 34, 30)], perna=[(120, 56, 30), (104, 46, 26)], perna_esc=(70, 32, 18),
             bico=[(46, 38, 34), (40, 32, 30)], olho=(255, 230, 90), olho_fundo=(255, 120, 20))
    escamas = [(110, 46, 22), (96, 38, 18), (84, 34, 16)]
    barriga = [(214, 170, 96), (196, 150, 80)]
    def p_escama(face, s, t, W, H):
        return r(barriga) if face == "down" else r(escamas)
    def p_chifre(face, s, t, W, H):
        return (214, 196, 160) if face == "side" and s >= W - 2 else (70, 56, 46)
    def asas(m, P):
        cores = {"B": (96, 46, 22), "M": [(34, 70, 78), (28, 60, 68)]}
        return [m.osso("asa_direita", [-3, 13, 0], [0, 30, 0],
                       [m.cubo("asa_d", [-15, 13, 0], [-3, 22, 0], arte(ASA_MORCEGO, cores, "z"))]),
                m.osso("asa_esquerda", [3, 13, 0], [0, -30, 0],
                       [m.cubo("asa_e", [3, 13, 0], [15, 22, 0], espelho_de="asa_d")])]
    def topo(m, P):
        out = []
        for n, x in (("d", -1.5), ("e", 1.5)):
            kw = dict(pintor=p_chifre) if n == "d" else dict(uv_de="chifre_d")
            out.append(m.osso(f"chifre_{n}", [x, 23, -2], [-25, 0, 0],
                              [m.cubo(f"chifre_{n}", [x - 0.5, 23, -2], [x + 0.5, 24, 4], **kw)]))
        return out
    def cauda(m, P):
        return m.osso("cauda", [0, 9, 4], [25, 0, 0], [
            m.cubo("cauda_1", [-1.5, 7.5, 3], [1.5, 10.5, 9], p_escama),
            m.osso("cauda_meio", [0, 9, 9], [-45, 0, 0], [
                m.cubo("cauda_2", [-1, 8, 8], [1, 10, 13], p_escama),
                m.osso("cauda_ponta", [0, 9, 13], [-30, 0, 0], [
                    m.cubo("cauda_3", [-0.5, 8.5, 12], [0.5, 9.5, 15], p_escama),
                    m.osso("chama_cauda", [0, 9.5, 14.5], [50, 0, 0], [      # endireita a chama para cima
                        m.cubo("chama_cauda_x", [0, 9, 13], [0, 15, 16], fogo_sobe(P["boca"], (3, 6, 4))),
                        m.cubo("chama_cauda_z", [-1.5, 9, 14.5], [1.5, 15, 14.5], fogo_sobe(P["boca"], (4, 6, 3))),
                    ])])])])
    o = dict(asas=asas, cabeca_extras=topo, cauda=cauda, barbela=False,
             boca=lambda m, P: efeito_boca(m, P["boca"]))
    return "galo_draconico", P, o

# =====================================================================================
# 3) GALO ASSOMBRO  (tema: fantasma sombrio)
# =====================================================================================
FUMACA = [
    "......PP",
    ".....PLP",
    "....PLP.",
    "...PPP..",
    "..PLP...",
    ".PPP.P..",
    "PLPPPLP.",
    "PPP.PPP.",
]
def galo_assombro():
    P = dict(escuro=[(52, 30, 78), (44, 24, 66)], brilho=[(78, 44, 112)],
             gola=[(96, 58, 140), (84, 48, 124)], gola_clara=[(124, 80, 172)],
             costas=[(66, 38, 96), (58, 32, 86)], asa_baixo=[(40, 22, 60)],
             pele=[(96, 58, 138), (84, 50, 122)], pele_esc=[(44, 24, 64), (36, 20, 54)],
             crista=[(112, 66, 160), (98, 58, 142)], perna=[(70, 46, 96), (60, 40, 84)], perna_esc=(40, 26, 56),
             bico=[(30, 22, 40), (26, 18, 34)], bico_esc=(16, 10, 22), unha=[(30, 20, 40), (24, 16, 32)],
             olho=(255, 70, 70), olho_fundo=(210, 20, 50), olheira=(18, 6, 22), cicatriz=(150, 110, 190),
             boca=[(230, 190, 255), (160, 80, 240), (80, 24, 140)])
    def p_crista(face, s, t, W, H): return r(P["crista"])
    def topo(m, P):   # crista em barbatana serrilhada
        out = [m.cubo("crista", [-1, 24, -7], [1, 25, -1], p_crista)]
        for i, (z, h) in enumerate(((-7, 2), (-6, 4), (-5, 3), (-4, 5), (-3, 3), (-2, 2))):
            out.append(m.cubo(f"barbatana_{i}", [-0.5, 25, z], [0.5, 25 + h, z + 1], p_crista))
        return out
    def espinhos(m, P):   # espinhos nas costas
        return [m.cubo(f"espinho_costas_{i}", [-0.5, 13, z], [0.5, 13 + h, z + 1], p_crista)
                for i, (z, h) in enumerate(((-3, 2), (-1, 3), (1, 2), (3, 1)))]
    def cauda(m, P):
        cores = {"P": [(84, 48, 124), (70, 40, 104)], "L": (150, 100, 210)}
        return m.osso("cauda", [0, 10, 4], [-20, 0, 0], [
            m.cubo("fumaca_1", [-1, 9, 4], [-1, 17, 12], arte(FUMACA, cores, "x")),
            m.cubo("fumaca_2", [1, 8, 5], [1, 16, 13], uv_de="fumaca_1")])
    o = dict(cabeca_extras=topo, corpo_extras=espinhos, cauda=cauda,
             lado_extra=lambda s, t: P["olho_fundo"] if (s, t) in ((0, 1), (1, 1)) else None,   # olhos maiores
             boca=lambda m, P: efeito_boca(m, P["boca"]))
    return "galo_assombro", P, o

# =====================================================================================
# 4) GALO ECLIPSE  (tema: raposa da lua, anéis brilhantes)
# =====================================================================================
LUA = [
    "..YYY..",
    ".YY....",
    "YY.....",
    "YY.....",
    "YY.....",
    ".YY....",
    "..YYY..",
]
def galo_eclipse():
    amarelo = [(255, 206, 50)]
    P = dict(escuro=[(20, 20, 26), (26, 26, 32)], brilho=[(36, 40, 62)],
             gola=[(30, 30, 38), (24, 24, 30)], gola_clara=amarelo, gola_listra=[(40, 40, 50)],
             costas=[(30, 30, 36), (24, 24, 30)], asa_baixo=[(22, 22, 28)], faixa=amarelo,
             pele=[(28, 28, 34), (34, 34, 40)], pele_esc=[(14, 14, 18), (18, 18, 22)], crista=amarelo,
             perna=[(30, 30, 36), (38, 38, 44)], perna_esc=(18, 18, 22),
             bico=[(24, 24, 30), (30, 30, 36)], bico_esc=(10, 10, 14),
             olho=(255, 50, 50), olho_fundo=(180, 10, 30), olheira=(8, 8, 10), cicatriz=None,
             boca=[(255, 244, 170), (255, 206, 50), (140, 100, 20)],
             cauda=[(22, 22, 28)], cauda_brilho=[(36, 40, 62)], cauda_faixa=amarelo)
    o = dict(barbela=False,
             lado_extra=lambda s, t: amarelo[0] if s == 5 and 1 <= t <= 4 else None,    # anel na cabeça
             cabeca_extras=lambda m, P: orelhas(m, [(26, 26, 32)], [(16, 16, 20)], faixa=amarelo, altura=9),
             boca=lambda m, P: efeito_boca(m, P["boca"], LUA, {"Y": [(255, 220, 80), (255, 206, 50)]},
                                           cantos=False))
    return "galo_eclipse", P, o

# =====================================================================================
# 5) GALO AURA  (tema: guerreiro de aura azul)
# =====================================================================================
def galo_aura():
    P = dict(escuro=[(22, 22, 30), (28, 28, 38)], brilho=[(30, 48, 104)],
             gola=[(40, 70, 150), (34, 60, 130)], gola_listra=[(60, 96, 180)], gola_clara=[(90, 130, 210)],
             costas=[(38, 66, 140), (32, 56, 122)], asa_baixo=[(22, 22, 30)], faixa=[(30, 30, 40)],
             pele=[(30, 30, 42), (24, 24, 34)], pele_esc=[(14, 14, 20), (18, 18, 26)], crista=[(40, 70, 150)],
             perna=[(38, 66, 140), (32, 56, 122)], perna_esc=(20, 34, 78),
             bico=[(32, 32, 44)], bico_esc=(12, 12, 18),
             olho=(255, 60, 60), olho_fundo=(190, 20, 40), olheira=(8, 8, 12), cicatriz=(110, 110, 140),
             boca=[(210, 245, 255), (90, 170, 255), (30, 70, 200)],
             cauda=[(28, 28, 38)], cauda_brilho=[(40, 70, 150)])
    osso_branco = (236, 232, 220)
    def p_espinho(face, s, t, W, H): return (150, 146, 136) if face == "north" else osso_branco
    def p_tranca(face, s, t, W, H): return (40, 70, 150) if t == H - 1 else r([(20, 20, 28), (26, 26, 36)])
    def topo(m, P):   # quatro tranças penduradas atrás da cabeça
        out = []
        for i, (x, y) in enumerate(((-1.5, 23), (1.5, 23), (-1.5, 21), (1.5, 21))):
            kw = dict(pintor=p_tranca) if i == 0 else dict(uv_de="tranca_0")
            out.append(m.osso(f"tranca_{i}", [x, y, -1.5], [-40, 0, 0],
                              [m.cubo(f"tranca_{i}", [x - 0.5, y - 6, -1.5], [x + 0.5, y, -0.5], **kw)]))
        return out
    def peito(m, P):
        return [m.cubo("espinho_peito", [-0.5, 9.5, -6], [0.5, 10.5, -4], p_espinho)]
    def asa_extras(m, lado):
        x0 = -4 if lado < 0 else 3
        kw = dict(pintor=p_espinho) if lado < 0 else dict(uv_de="espinho_asa_d")
        return [m.cubo("espinho_asa_" + ("d" if lado < 0 else "e"), [x0, 10, -5.5], [x0 + 1, 11, -3.5], **kw)]
    o = dict(barbela=False, cabeca_extras=topo, corpo_extras=peito, asa_extras=asa_extras,
             boca=lambda m, P: efeito_boca(m, P["boca"]))
    return "galo_aura", P, o

# =====================================================================================
GALOS = [galo_trovao, galo_draconico, galo_assombro, galo_eclipse, galo_aura]
NOMES = {"galo_trovao": "Galo Trovão", "galo_draconico": "Galo Dracônico", "galo_assombro": "Galo Assombro",
         "galo_eclipse": "Galo Eclipse", "galo_aura": "Galo Aura"}

if __name__ == "__main__":
    sys.path.insert(0, str(AQUI))
    import previa
    fotos = []
    for fn in GALOS:
        nome, P, o = fn()
        RNG.seed(7)
        m = Modelo(nome)
        caminho, n, tam = m.salvar(montar(m, P, o))
        quads = previa.carregar(str(caminho))
        vistas = [("frente", 0, -8), ("lado", 90, -5), ("3/4 frente", -40, -20), ("3/4 tras", 145, -20)]
        ims = [(v, previa.desenhar(quads, y, p)) for v, y, p in vistas]
        H = max(i.height for _, i in ims) + 24
        folha = Image.new("RGB", (sum(i.width for _, i in ims) + 30, H), (22, 24, 29)); x = 0
        for v, i in ims:
            folha.paste(i, (x, 24 + (H - 24 - i.height))); ImageDraw.Draw(folha).text((x + 8, 6), v, fill=(220, 220, 220))
            x += i.width + 10
        folha.save(SAIDA / f"{nome}_previa.png")
        fotos.append((NOMES[nome], previa.desenhar(quads, -40, -18, escala=10)))
        print(f"{nome}: {n} cubos, textura {tam[0]}x{tam[1]}")
    # foto do grupo
    H = max(i.height for _, i in fotos) + 30
    from PIL import ImageFont
    try: fonte = ImageFont.truetype("arial.ttf", 16)
    except OSError: fonte = None
    grupo = Image.new("RGB", (sum(i.width for _, i in fotos) + 15 * len(fotos), H), (18, 19, 23)); x = 0
    for nome, i in fotos:
        grupo.paste(i, (x, H - i.height)); ImageDraw.Draw(grupo).text((x + 10, 6), nome, fill=(230, 230, 230), font=fonte)
        x += i.width + 15
    grupo.save(SAIDA / "grupo.png")
    print("grupo ->", SAIDA / "grupo.png", grupo.size)

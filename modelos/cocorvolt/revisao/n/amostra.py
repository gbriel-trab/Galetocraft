import sys
import numpy as np
from PIL import Image
im = np.asarray(Image.open(r"C:\Users\gbriel\Desktop\galopiru\modelos\referencias\006_cocorvolt_vistas.png").convert("RGB")).astype(int)
P = {"olho_d": (150, 179), "olho_e": (193, 179), "testa": (150, 168), "cara_lado": (125, 205), "cara_baixo": (140, 230),
     "bico_alto": (176, 186), "bico_baixo": (178, 198), "barbela": (166, 222), "aba": (80, 154), "topo_chapeu": (166, 118),
     "palha": (110, 140), "talisma_moldura": (70, 200), "talisma_fundo": (85, 222), "talisma_raio": (82, 205),
     "ombreira_ouro": (104, 262), "ombreira_fundo": (116, 282), "peito_azul": (140, 268), "gola": (155, 255),
     "v_preto": (166, 262), "cinto": (140, 296), "emblema_ouro": (158, 296), "emblema_centro": (166, 296),
     "saia_azul": (135, 340), "saia_ouro": (127, 352), "painel_fundo": (180, 365), "painel_raio": (168, 345),
     "asa_alta": (100, 320), "asa_baixa": (100, 370), "asa_ponta": (88, 385), "saiote": (166, 395), "perna": (147, 418),
     "pe": (140, 438), "garra": (124, 442),
     "L_cauda_escura": (380, 330), "L_cauda_topo": (400, 236), "L_cauda_raio": (372, 265), "L_omb_ouro": (468, 270),
     "L_omb_fundo": (497, 292), "L_omb_cupula": (497, 256), "L_asa": (495, 340), "L_cabeca": (480, 200), "L_nuca": (462, 215),
     "L_bico": (560, 192), "L_barbela": (552, 245),
     "T_nuca": (776, 200), "T_ombro_azul": (735, 262), "T_costas": (776, 290), "T_cauda": (776, 340), "T_asa": (720, 340)}
for k, (x, y) in P.items():
    c = np.median(im[y - 2:y + 3, x - 2:x + 3].reshape(-1, 3), axis=0).astype(int)
    print(f"{k:16s} {tuple(int(v) for v in c)}")

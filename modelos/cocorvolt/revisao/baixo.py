"""Vista de 3/4 de baixo (altura do olho do jogador) e de trás 3/4."""
import sys
sys.path.insert(0, "ferramentas")
import previa2
from PIL import Image
q = previa2.carregar("modelos/cocorvolt/cocorvolt.bbmodel")
a = previa2.desenhar(q, -30, 6, escala=14, fundo=(14, 10, 12))
b = previa2.desenhar(q, 145, -8, escala=14, fundo=(14, 10, 12))
f = Image.new("RGB", (a.width + b.width + 10, max(a.height, b.height)), (14, 10, 12))
f.paste(a, (0, 0)); f.paste(b, (a.width + 10, 0)); f.save(sys.argv[1])

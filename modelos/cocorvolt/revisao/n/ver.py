import sys
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import previa2
from PIL import Image
q = previa2.carregar(r"C:\Users\gbriel\Desktop\galopiru\modelos\cocorvolt\cocorvolt.bbmodel")
ims = [previa2.desenhar(q, y, p, escala=16, fundo=(14, 10, 12)) for y, p in [(90, -5), (-35, -10), (150, -10)]]
W = sum(i.width for i in ims); H = max(i.height for i in ims)
f = Image.new("RGB", (W, H), (14, 10, 12)); x = 0
for i in ims: f.paste(i, (x, 0)); x += i.width
f.save(sys.argv[1])

import sys
from PIL import Image
pre = sys.argv[1]
ref = Image.open('modelos/referencias/012_salambrasa_vistas.png').convert('RGB').crop((40, 70, 1790, 420))
nos = Image.open(f'modelos/salambrasa/revisao/{pre}_vistas.png').convert('RGB')
W = 1600
ref = ref.resize((W, int(ref.height * W / ref.width)))
nos = nos.resize((W, int(nos.height * W / nos.width)))
f = Image.new('RGB', (W, ref.height + nos.height), (0, 0, 0)); f.paste(ref, (0, 0)); f.paste(nos, (0, ref.height))
f.save(f'modelos/salambrasa/revisao/{pre}_comparar.png')

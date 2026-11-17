import sys
from PIL import Image
pre = sys.argv[1]
ref = Image.open('modelos/referencias/005_cocorion_vistas.png').convert('RGB').crop((40, 90, 1220, 470))
nos = Image.open(f'modelos/cocorion/revisao/{pre}_vistas.png').convert('RGB')
k = ref.width / nos.width
nos = nos.resize((ref.width, int(nos.height * k)))
out = Image.new('RGB', (ref.width, ref.height + nos.height), (0, 0, 0))
out.paste(ref, (0, 0)); out.paste(nos, (0, ref.height))
out.save(f'modelos/cocorion/revisao/{pre}_comparar.png')

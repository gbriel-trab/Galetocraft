import sys
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import numpy as np
from PIL import Image
import comparar_ficha as cf
folha = Image.open(r"C:\Users\gbriel\Desktop\galopiru\modelos\referencias\006_cocorvolt_vistas.png").convert("RGB")
FW, FH = folha.size
corpo = folha.crop((int(FW*0.02), int(FH*0.14), int(FW*0.98), int(FH*0.97)))
CW, CH = corpo.size
for i,(nome,yaw) in enumerate(cf.VISTAS):
    col = corpo.crop((i*CW//4, 0, (i+1)*CW//4, CH))
    m = cf.mascara_ficha(col)
    ys, xs = np.nonzero(m)
    y0,y1 = ys.min(), ys.max(); H = y1-y0+1
    print(nome, "H px", H, "W", xs.max()-xs.min()+1)
    for f in np.arange(0,1.0,0.04):
        r = y0 + int(f*H)
        row = np.nonzero(m[r])[0]
        if len(row): print(f"  {39*(1-f):5.1f}u  x {row.min()-xs.min():4d}..{row.max()-xs.min():4d}  w={row.max()-row.min()+1}")
ims=[]
for i,(nome,yaw) in enumerate(cf.VISTAS):
    col = corpo.crop((i*CW//4, 0, (i+1)*CW//4, CH))
    m = cf.mascara_ficha(col)
    a = np.asarray(col).copy(); a[~m] = (a[~m]*0.3).astype(np.uint8); a[m] = (a[m]*0.5 + np.array([0,100,0])).astype(np.uint8)
    ims.append(Image.fromarray(a))
W=sum(i.width for i in ims); out=Image.new("RGB",(W,ims[0].height)); x=0
for i in ims: out.paste(i,(x,0)); x+=i.width
out.save(r"C:\Users\gbriel\Desktop\galopiru\modelos\cocorvolt\revisao\n\mascaras.png")

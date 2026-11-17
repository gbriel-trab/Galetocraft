import sys
sys.path.insert(0, 'ferramentas')
import previa2
pre = sys.argv[1]
q = previa2.carregar('modelos/cocorion/cocorion.bbmodel')
for nome, y, p, e in (("lado", 90, -5, 16), ("tras", 180, -6, 12), ("34", 35, -10, 16), ("tras34", 145, -12, 12)):
    previa2.desenhar(q, y, p, escala=e, fundo=(14, 10, 12)).save(f'modelos/cocorion/revisao/{pre}_{nome}_g.png')

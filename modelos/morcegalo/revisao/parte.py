"""Close de uma parte do modelo: python parte.py saida.png cx cy cz raio yaw pitch escala"""
import sys
sys.path.insert(0, 'ferramentas')
import galo_base as g, previa2
saida, cx, cy, cz, r, yaw, pitch, esc = sys.argv[1], *map(float, sys.argv[2:9])
q = previa2.carregar('modelos/morcegalo/morcegalo.bbmodel')
g.desenhar_parte(q, (cx, cy, cz), r, yaw, pitch, esc).save(saida)

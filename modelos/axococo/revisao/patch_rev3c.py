p = r'C:\Users\gbriel\Desktop\galopiru\ferramentas\especies\axococo.py'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
rep('cab += camada_cabeca("domo1", 29.7, 31.0, 0.8,', 'cab += camada_cabeca("domo1", 29.7, 31.1, 0.6,')
rep('cab += camada_cabeca("domo2", 30.9, 31.9, 1.9,', 'cab += camada_cabeca("domo2", 31.0, 32.0, 1.4,')
rep('cab += camada_cabeca("domo3", 31.8, 32.5, 3.2,', 'cab += camada_cabeca("domo3", 31.9, 32.6, 2.5,')
rep('segs = [(L, 1.9 - 0.12 * i, 5.0 - 0.55 * i,', 'segs = [(L, 2.3 - 0.15 * i, 5.0 - 0.55 * i,')
open(p, 'w', encoding='utf-8').write(s); print("ok")

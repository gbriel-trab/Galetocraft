"""Gera o pacote rev. 6: completa os golpes próprios das fichas #001–#011 que, na camada vigente,
tinham só o texto provisório "Sem descrição textual adicional na ficha oficial; consultar o JSON
original protegido".

Os dados vêm da tabela histórica `moves` do Galetocraft.sqlite rev. 2, que guarda a ficha original
protegida: categoria, estado aplicado, chance e effect_json. Nada é inventado.
- A categoria que faltava é preenchida (Prisão das Areias e Julgamento dos Céus são físicos).
- Golpes sem elemento e sem dano recebem "Sem elemento".
- O efeito estruturado (efeito_json_nucleo) é preenchido onde faltava.
- O estado aplicado e a chance ganham um campo próprio (aplica_estado), com o nome oficial do estado.
- O texto provisório é trocado por uma descrição literal desses dados.

Uso:
  python gerar_rev6_golpes_originais.py --historico Galetocraft_rev2.sqlite --saida docs/patches/rev6_golpes_originais.json
"""
import argparse, json, os, sqlite3

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLACEHOLDER = 'Sem descrição textual adicional na ficha oficial'
ESTADO_OFICIAL = {'Tontura': 'Tonto'}
CATEGORIA = {'físico': 'fisico', 'mágico': 'magico'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--historico', required=True)
    ap.add_argument('--saida', required=True)
    ap.add_argument('--revisao', type=int, default=5)
    a = ap.parse_args()
    con = sqlite3.connect(f'file:{a.historico}?mode=ro', uri=True)
    cols = [r[1] for r in con.execute('PRAGMA table_info(moves)')]
    golpes = json.load(open(os.path.join(RAIZ, 'base', 'vigente', 'current_moves.json'), encoding='utf-8'))
    ops, log = [], []
    for g in golpes:
        p = dict(g['payload_json'])
        if PLACEHOLDER not in (p.get('efeito_canonico_para_integracao') or ''):
            continue
        r = con.execute('SELECT * FROM moves WHERE name=? OR id=?', (g['nome'], p.get('id_canonico'))).fetchone()
        if r is None:
            raise SystemExit(f'Sem fonte histórica para {g["nome"]}')
        h = dict(zip(cols, r))
        efeito = json.loads(h['effect_json'] or '{}')
        mudou = []
        if not p.get('categoria_normalizada'):
            p['categoria_normalizada'] = CATEGORIA.get(h['category'], h['category'])
            p['categoria_complementada'] = p['categoria_normalizada']
            mudou.append('categoria')
        if p.get('elemento') is None:
            p['elemento'] = h['element'] or 'Sem elemento'
            mudou.append('elemento')
        if p.get('efeito_json_nucleo') in (None, '', '{}') and efeito:
            p['efeito_json_nucleo'] = json.dumps(efeito, ensure_ascii=False)
            mudou.append('efeito_json_nucleo')
        partes = []
        if h['status_application']:
            estado = ESTADO_OFICIAL.get(h['status_application'], h['status_application'])
            p['aplica_estado'] = {'estado': estado, 'chance': h['status_chance']}
            partes.append(f'Após causar dano, {round(h["status_chance"] * 100)}% de chance de aplicar {estado}.')
            mudou.append('aplica_estado')
        if efeito or p.get('efeito_json_nucleo') not in (None, '', '{}'):
            partes.append('Demais efeitos definidos no efeito estruturado oficial (efeito_json_nucleo, ficha original protegida).')
        if not partes:
            partes.append('Golpe sem efeito secundário registrado na ficha original protegida.')
        p['efeito_canonico_para_integracao'] = ' '.join(partes)
        p['fonte_complemento_rev6'] = 'tabela histórica moves (Galetocraft.sqlite rev. 2), ficha original protegida'
        mudou.append('efeito_canonico_para_integracao')
        ops.append({'table': 'current_moves', 'key': {'especie': g['especie'], 'grupo': g['grupo'], 'posicao': g['posicao']},
                    'values': {'payload_json': json.dumps(p, ensure_ascii=False)}})
        log.append({'especie': g['especie'], 'golpe': g['nome'], 'campos': mudou})
    pacote = {
        'expected_revision': a.revisao,
        'reason': ('Completa os golpes próprios de #001–#011 que tinham só texto provisório na camada vigente: categoria, '
                   'elemento, estado aplicado com chance e efeito estruturado, copiados da ficha original protegida '
                   '(tabela histórica moves). Texto literal desses dados no lugar do provisório.'),
        'evidence': {'fonte': 'Galetocraft.sqlite rev. 2, tabela moves (ficha original protegida)',
                     'catalogo': 'Galolpedia_Reforma_Integral_212_Golpes_Catalogo_2026-11-11.json (status PROTEGIDO_FICHA_ORIGINAL)',
                     'golpes': log},
        'operations': ops,
    }
    json.dump(pacote, open(a.saida, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({'operacoes': len(ops)}, ensure_ascii=False))


if __name__ == '__main__':
    main()

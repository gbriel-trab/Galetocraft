"""Exporta a base vigente (base/vigente) para os dados que o núcleo e o mod leem.

Saída em galetocraft/nucleo/src/main/resources/galetocraft/dados/:
  especies.json  as 23 espécies, com atributos, elementos, passiva, Galeria e os 30 golpes
  regras.json    todas as regras de current_rules (id -> conteúdo)
  versao.json    revisão da base e SHA-256 dos arquivos gerados

Os arquivos são derivados: nunca editar à mão; rodar de novo após cada revisão da base.
Uso: python ferramentas/base/exportar_para_mod.py
"""
import hashlib, json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VIGENTE = os.path.join(RAIZ, 'base', 'vigente')
SAIDA = os.path.join(RAIZ, 'galetocraft', 'nucleo', 'src', 'main', 'resources', 'galetocraft', 'dados')
ATRIBUTOS = ['HP', 'Ataque Físico', 'Defesa Física', 'Ataque Mágico', 'Defesa Mágica', 'Velocidade']


def ler(t):
    return json.load(open(os.path.join(VIGENTE, t + '.json'), encoding='utf-8'))


def valor_json(v):
    """poder_json/energia_efetiva_json guardam texto JSON ("40", "null", "\\"40 × 1–5\\"")."""
    if v is None:
        return None
    if isinstance(v, str):
        try:
            return json.loads(v)
        except json.JSONDecodeError:
            return v
    return v


def golpe(m):
    p = m['payload_json']
    poder = valor_json(p.get('poder_json'))
    energia = valor_json(p.get('energia_efetiva_json'))
    estruturado = p.get('efeito_json_nucleo')
    if isinstance(estruturado, str):
        try:
            estruturado = json.loads(estruturado) if estruturado.strip() else None
        except json.JSONDecodeError:
            estruturado = None
    return {
        'grupo': m['grupo'], 'posicao': m['posicao'], 'nome': m['nome'],
        'id': p.get('id_canonico') or m.get('id_documental'),
        'elemento': p.get('elemento'), 'categoria': p.get('categoria_normalizada'),
        'poder': poder if isinstance(poder, int) else None,
        'poder_texto': poder if isinstance(poder, str) else None,
        'energia': energia if isinstance(energia, int) else None,
        'efeito': p.get('efeito_canonico_para_integracao'),
        'aplica_estado': p.get('aplica_estado'),
        'efeito_estruturado': estruturado or None,
    }


def main():
    especies = ler('current_species')
    golpes = ler('current_moves')
    galeria = {g['numero']: g for g in ler('current_galeria')}
    heranca = {h['especie']: h for h in ler('current_heranca')}
    meta = {m['key']: m['value_json'] for m in ler('current_meta')}
    saida = []
    for s in sorted(especies, key=lambda s: s['numero']):
        n = s['numero']
        passiva = s['passiva_json']
        nome_passiva = None
        if isinstance(passiva, dict):
            nome_passiva = (passiva.get('nome') or passiva.get('name') or passiva.get('nome_de_catalogo')
                            or (passiva.get('efeito_estruturado') or {}).get('nome'))
        g = galeria.get(n)
        saida.append({
            'numero': n, 'nome': s['nome'], 'raridade': s['raridade'], 'elementos': s['elementos_json'],
            'atributos': {a: s['atributos_json'][a] for a in ATRIBUTOS}, 'peso_kg': s['peso_natural_kg'],
            'passiva': {'nome': nome_passiva, 'dados': passiva},
            'galeria': None if g is None else {'alas': [x for x in (g['ala_principal'], g['ala_secundaria']) if x],
                                               'probabilidade_macho': g['probabilidade_macho']},
            'hereditario': None if n not in heranca else heranca[n]['golpe'],
            'golpes': [golpe(m) for m in sorted((m for m in golpes if m['especie'] == n),
                                                key=lambda m: (m['grupo'] != 'original', m['posicao']))],
        })
    regras = {r['id']: r['payload_json'] for r in ler('current_rules')}
    os.makedirs(SAIDA, exist_ok=True)
    hashes = {}
    for nome, dados in (('especies.json', saida), ('regras.json', regras)):
        caminho = os.path.join(SAIDA, nome)
        texto = json.dumps(dados, ensure_ascii=False, indent=1) + '\n'
        open(caminho, 'w', encoding='utf-8').write(texto)
        hashes[nome] = hashlib.sha256(texto.encode('utf-8')).hexdigest()
    versao = {'revisao_base': meta['revision'], 'especies': len(saida), 'golpes': len(golpes), 'regras': len(regras),
              'sha256': hashes, 'origem': 'base/vigente (ferramentas/base/exportar_para_mod.py)'}
    open(os.path.join(SAIDA, 'versao.json'), 'w', encoding='utf-8').write(json.dumps(versao, ensure_ascii=False, indent=1) + '\n')
    print(json.dumps(versao, ensure_ascii=False))


if __name__ == '__main__':
    main()

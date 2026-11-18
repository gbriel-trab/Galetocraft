"""Gera o pacote de atualização rev. 3 da base vigente (Galetocraft.sqlite rev. 2 -> 3).

Reúne as correções de coerência e de nomenclatura decididas em 18/11/2026, no formato
do atualizador oficial (Atualizar_Galetocraft.py). O pacote só altera registros que já existem e não
cria espécies, golpes nem artes. Os textos integrais das atas ficam intocados: as resoluções
entram em um campo novo, "resolucoes_posteriores".

Uso:
  python gerar_patch_rev3.py --base Galetocraft.sqlite --saida docs/patches/rev3_coerencia_e_nomenclatura.json
Aplicado em 18/11/2026 na base do repositório com:
  python ferramentas/base/galetobase.py atualizar --pacote docs/patches/rev3_coerencia_e_nomenclatura.json
(O pacote também é compatível com o Atualizar_Galetocraft.py original, sobre o SQLite da revisão 2.)
"""
import argparse, json, os, sqlite3, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import aplicar_nomenclatura as nomenclatura  # noqa: E402

DATA = '2026-11-18'
DECISAO = 'Decisão expressa do criador em 18/11/2026 (auditoria de incoerências)'
TEXTO_CONCENTRACAO = ('Concentração V2.3: Suporte, Energia 0; execução válida recupera 35 de energia (máximo 100), '
                      '40% de chance de remover estado negativo persistente e concede Pena de Ritmo conforme regras '
                      'oficiais de criação, duração e consumo. Recuperação normal de 20 no início do próprio turno '
                      'permanece independente.')
TEXTO_BASICO = ('Golpe básico ofensivo {cat} de elemento Neutro, Poder 40, Energia 0. Sem efeito secundário universal '
                'adicional; respeitar alterações expressamente previstas na ficha ou passiva.')
CAMPOS_TECNICOS = {'status_nucleo', 'fonte_efeito_estruturado', 'status_efeito', 'status_id_canonico',
                   'status_consolidacao', 'id_canonico', 'id_movimento_nucleo', 'efeito_json_nucleo',
                   'norma_universal_vigente_ref', 'norma_universal_vigente_json', 'id_catalogo', 'status_vinculo_especie'}


def normalizar_categoria(c):
    if not c:
        return None
    c = c.strip().lower()
    return {'mágico': 'magico', 'físico': 'fisico'}.get(c, c)


def corrigir_golpes(con, pares):
    ops, log = [], []
    for esp, grupo, pos, nome, pj in con.execute(
            'SELECT especie, grupo, posicao, nome, payload_json FROM current_moves ORDER BY especie, grupo, posicao'):
        p = json.loads(pj)
        antes = json.dumps(p, ensure_ascii=False, sort_keys=True)
        motivos = []
        # 1) Esquema comum para o #023 (mesmos dados, chaves de leitura padronizadas; chaves originais mantidas)
        if esp == 23:
            efeito = p.get('efeito_oficial_literal') or p.get('efeito')
            comuns = {
                'elemento': p.get('elemento'),
                'categoria_normalizada': normalizar_categoria(p.get('categoria')),
                'poder_json': json.dumps(p.get('poder_base')),          # mesmo formato das demais espécies ("40", "null")
                'energia_efetiva_json': json.dumps(p.get('energia')),
                'efeito_canonico_para_integracao': efeito,
                'id_canonico': p.get('id_catalogo'),
            }
            for k, v in comuns.items():
                if p.get(k) != v:
                    p[k] = v
            motivos.append('esquema_comum_023')
        # 2) Concentração: regra universal V2.3 em todas as espécies (ata 13/11, itens 1 e 10)
        if nome == 'Concentração':
            p['elemento'] = 'Sem elemento'
            p['categoria_normalizada'] = 'suporte'
            if 'categoria_complementada' in p or esp != 23:
                p['categoria_complementada'] = 'suporte'
            p['norma_universal_vigente_ref'] = 'concentracao'
            if esp not in (22, 23):          # #022 tem a nota da Partitura; #023 já traz o texto V2.3
                p['efeito_canonico_para_integracao'] = TEXTO_CONCENTRACAO
            motivos.append('concentracao_v2_3_universal')
        # 3) Golpes básicos: texto canônico no lugar de placeholders/variações
        if nome in ('Crina Poderosa', 'Garra Afiada') and esp not in (22, 23):
            cat = 'mágico' if nome == 'Crina Poderosa' else 'físico'
            p['efeito_canonico_para_integracao'] = TEXTO_BASICO.format(cat=cat)
            motivos.append('basico_texto_canonico')
        # 4) Nomenclatura oficial nos textos (Tontura -> Tonto etc.), sem tocar campos técnicos
        for k, v in list(p.items()):
            if isinstance(v, str) and k not in CAMPOS_TECNICOS:
                novo, trocas, _ = nomenclatura.aplicar_texto(v, pares, False)
                if trocas:
                    p[k] = novo
                    motivos.append('nomenclatura')
        if json.dumps(p, ensure_ascii=False, sort_keys=True) != antes:
            ops.append({'table': 'current_moves', 'key': {'especie': esp, 'grupo': grupo, 'posicao': pos},
                        'values': {'payload_json': json.dumps(p, ensure_ascii=False)}})
            log.append({'especie': esp, 'grupo': grupo, 'posicao': pos, 'nome': nome, 'motivos': sorted(set(motivos))})
    return ops, log


def regra(con, rid):
    return json.loads(con.execute('SELECT payload_json FROM current_rules WHERE id=?', (rid,)).fetchone()[0])


def corrigir_regras(con):
    alteracoes = {
        'concentracao': {
            'pendencia_12_36_atributos_iniciais': 'RESOLVIDA — current_issues R02 (R531 + Beta161 + R55 + CSV concordam; base_nivel=50).',
            'pendencia_13_peso_renacoco': 'RESOLVIDA — current_issues R09: 6,8 kg (faixa 5,44–10,20 kg).',
            'pendencia_14_integracao_banco_jogavel': 'Continua pendente (current_issues R14).',
        },
        'progressao': {
            'conflitos.iniciais_001_006': 'RESOLVIDO — current_issues R02; 36 atributos dos iniciais vigentes em current_species (total 550).',
            'lendario_original': {
                'classe': 'Lendário Original', 'fora_da_escala_de_raridades': True,
                'total_definido_pela_ficha_homologada': True, 'especies': {'23': {'nome': 'Quetzacocó', 'total_l50': 700}},
                'decisao': DECISAO,
            },
        },
        'golpe_duplo': {
            'preservacao.conflitos_36_atributos_iniciais': 'RESOLVIDO — current_issues R02.',
        },
        'tipagem_dupla': {
            'sirenoco_022': 'Incorporada em 13/11/2026 (Água + Ar). Matriz: Fogo 1×, Água 1×, Planta 1×, Terra 0,25×, Ar 1×, Elétrico 4× — igual ao #016 Libelocó.',
            'especies_duplas_atuais': 9,
            'casos_4x_atuais': ['#015 Faíscocó: Terra', '#016 Libelocó: Elétrico', '#017 Castorocó: Ar',
                                '#021 Cabacocó: Ar', '#022 Sirenocó: Elétrico'],
            'tripla': '#023 Quetzacocó (Ar + Planta + Nexo) segue a regra tripla excepcional do Nexo V2.0.',
        },
        'nexo': {
            'pendentes.atributos_e_peso_023': 'RESOLVIDO — ficha V2 de 16/11/2026: total 700 no nível 50, peso 180 kg.',
            'pendentes.passiva_e_repertorio_023': 'RESOLVIDO — Soberania dos Ventos Eternos; 30 golpes homologados em 16/11/2026.',
            'pendentes.heranca_golpes_tipados_nexo': 'SEM APLICAÇÃO — Lendários Originais não reproduzem (regra lendarios_originais_reproducao).',
            'pendentes_reais': ['distribuição de aprendizagem do #023 (current_issues U03)', 'balanceamento por simulação',
                                'implementação Java/SQLite/Minecraft', 'relações com futuros elementos especiais de outros lendários'],
        },
        'galeria_gemeos_especiais': {
            'pares_inativos': [{'par': [5, 6], 'especies': 'Cocórion + Cocórvolt',
                                'motivo': 'As duas espécies são 100% machos; o par fica registrado e inativo até mudança na distribuição de sexo.',
                                'decisao': DECISAO}],
        },
        'heranca_bico': {
            'especies_sem_hereditario_por_design': [7, 8, 9, 10, 11, 12, 13, 14, 15],
            'decisao_sem_hereditario': DECISAO,
            'especie_23': 'Não reproduz (Lendário Original); Herança de Bico não se aplica.',
        },
    }
    ops = []
    for rid, res in alteracoes.items():
        p = regra(con, rid)
        p.setdefault('resolucoes_posteriores', {}).update({'data': DATA, **res})
        ops.append({'table': 'current_rules', 'key': {'id': rid}, 'values': {'payload_json': json.dumps(p, ensure_ascii=False)}})
    return ops


def corrigir_pendencias():
    return [
        {'table': 'current_issues', 'key': {'id': 'R03'}, 'values': {
            'status': 'RESOLVIDO',
            'evidencia': 'Criador confirmou em 18/11/2026: atributos-base são do nível 50. Cópias corrigidas de 29 fichas oficiais no repositório (docs/acervo_corrigido, errata ERRATA_NIVEL_50).',
            'proximo_passo': 'Conferir fichas pelas cópias corrigidas; originais preservados como histórico.'}},
        {'table': 'current_issues', 'key': {'id': 'R12'}, 'values': {
            'status': 'RESOLVIDO_IDENTIFICADO',
            'evidencia': ('Artes oficiais identificadas pelas fichas homologadas: #019 "Renacocó com Face Azul Claro.png" '
                          '(SHA-256 a02914205da47b361e4318d0c20856db6c5422d20d94af4369cdc492cbdf018c; Galetario_019 oficial, BAL 12/11, R5.3) '
                          'e #020 "Ficha Oficial Frankocó #020.png" (SHA-256 4790f440dff7f8d491d2de63f0488e88e1292c05695505bc910da27e26125611; '
                          'Galetario_020 oficial). Modelo r82 do Renacocó localizado no repositório (modelos/renacoco, exportado no mod).'),
            'proximo_passo': 'Incorporar as duas artes em current_art por migração completa (registro novo).'}},
    ]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--base', required=True)
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    con = sqlite3.connect(f'file:{a.base}?mode=ro', uri=True)
    rev = json.loads(con.execute("SELECT value_json FROM current_meta WHERE key='revision'").fetchone()[0])
    pares = nomenclatura.carregar(os.path.join(AQUI, 'nomenclatura_oficial.json'))
    ops_golpes, log = corrigir_golpes(con, pares)
    ops = ops_golpes + corrigir_regras(con) + corrigir_pendencias()
    patch = {
        'expected_revision': rev,
        'reason': ('Correções de coerência e nomenclatura oficial (18/11/2026): Concentração V2.3 em todas as espécies; '
                   'textos canônicos dos golpes básicos; esquema comum do #023; Tonto no lugar de Tontura; '
                   'pendências já resolvidas marcadas nas regras; decisões do criador sobre Lendário Original, '
                   'par de gêmeos inativo e espécies sem hereditário; R03 e R12 resolvidas.'),
        'evidence': {'decisoes': DECISAO, 'auditoria': 'docs/AUDITORIA_INCOERENCIAS.md',
                     'nomenclatura': 'docs/NOMENCLATURA_OFICIAL.md', 'golpes_alterados': log},
        'operations': ops,
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
    json.dump(patch, open(a.saida, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({'expected_revision': rev, 'operacoes': len(ops), 'golpes': len(ops_golpes)}, ensure_ascii=False))


if __name__ == '__main__':
    main()

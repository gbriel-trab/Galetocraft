"""Gera o pacote rev. 10: tempestade de areia no mundo (pedido do criador em 18/11/2026).

Pedido: "Vamos adicionar ao mod esse efeito ao minecraft de tempestade de areia". Respostas às perguntas de
esclarecimento: acontece quando chove no mundo, no deserto; efeito de jogo: a Rinha que começa dentro dela já começa com o
clima oficial Tempestade de Areia.

Uso: python gerar_rev10_tempestade_areia.py --saida docs/patches/rev10_tempestade_de_areia.json
"""
import argparse, copy, json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APROVACAO = ('Criador, 18/11/2026: "Vamos adicionar ao mod esse efeito ao minecraft de tempestade de areia"; respostas no mesmo dia: '
             '"Quando chove, no deserto"; efeitos: "Rinha com o clima Tempestade de Areia".')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--revisao', type=int, default=9)
    a = ap.parse_args()
    regras = {r['id']: r for r in json.load(open(os.path.join(RAIZ, 'base', 'vigente', 'current_rules.json'), encoding='utf-8'))}
    tempestade = {
        'status': 'OFICIAL_APROVADO_PELO_CRIADOR_2026-11-18',
        'aprovacao': APROVACAO,
        'gatilho': 'quando chove ou troveja no mundo (ciclo de clima do Minecraft), nos biomas onde não chove',
        'biomas': ['c:is_desert', 'c:is_badlands'],
        'ao_ar_livre': 'só onde o céu é visível; sob teto ou no subsolo não há tempestade',
        'visual': {
            'poeira': 'partículas de areia sopradas na direção do vento (a direção muda a cada dia de jogo)',
            'nevoa': 'névoa amarelada que encurta a visão, com transição suave ao entrar e sair',
            'vento': 'som de vento contínuo enquanto durar',
        },
        'efeitos_de_jogo': {
            'rinha': ('uma Rinha que começa dentro da tempestade (posição do Galeto selvagem) já começa com o clima Tempestade de '
                      'Areia, pelas regras de climas (4 rodadas)'),
            'aparecimento': 'Cocórak (encontro raro) fica 2× mais provável durante a tempestade (regra mundo_aparecimento)',
            'sem_outros_efeitos': 'não causa dano nem lentidão no jogador',
        },
    }
    mundo = copy.deepcopy(regras['mundo_aparecimento']['payload_json'])
    for e in mundo['especies']:
        if e['numero'] == 4:
            e['condicao'] = 'mais provável (×2) durante a tempestade de areia (regra tempestade_de_areia)'
    pacote = {
        'expected_revision': a.revisao,
        'reason': 'Tempestade de areia no mundo, pedida e definida pelo criador em 18/11/2026; o Cocórak passa a usar a tempestade real.',
        'evidence': {'aprovacao': APROVACAO},
        'operations': [
            {'op': 'inserir', 'table': 'current_rules', 'key': {'id': 'tempestade_de_areia'},
             'values': {'payload_json': tempestade, 'source_ref': 'Pedido e respostas do criador em 18/11/2026', 'status': 'OFICIAL_DOCUMENTAL'}},
            {'op': 'atualizar', 'table': 'current_rules', 'key': {'id': 'mundo_aparecimento'}, 'values': {'payload_json': mundo}},
        ],
    }
    with open(a.saida, 'w', encoding='utf-8') as f:
        json.dump(pacote, f, ensure_ascii=False, indent=1)
    print('ok', a.saida)


if __name__ == '__main__':
    main()

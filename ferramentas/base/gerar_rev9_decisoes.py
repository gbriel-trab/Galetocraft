"""Gera o pacote rev. 9: registra as decisões do criador de 18/11/2026 sobre as propostas de
docs/propostas/PROPOSTAS_PENDENCIAS_2026-11-18.md.

Resposta do criador: "Todas menos B e H estão aprovadas. No caso eu quero que o nível seja independente do local
completamente variável do 1 até o 70. No caso do lendário único ele será extremamente raro, mas quando aparecer uma
mensagem de chat aparecerá global avisando". Respostas às perguntas de esclarecimento (mesmo dia): resto do B como
proposto; Quetzacocó só em selva ou montanha durante tempestade e depois dos 6 elementos; sempre no nível 70; captura com
Pena nível 5 e fator 0,14.

Uso: python gerar_rev9_decisoes.py --saida docs/patches/rev9_decisoes_criador.json
"""
import argparse, copy, json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APROVACAO = ('Criador, 18/11/2026: "Todas menos B e H estão aprovadas. No caso eu quero que o nível seja independente do local '
             'completamente variável do 1 até o 70. No caso do lendário único ele será extremamente raro, mas quando aparecer uma '
             'mensagem de chat aparecerá global avisando"; esclarecimentos no mesmo dia: resto do B como proposto; Quetzacocó em '
             'selva ou montanha durante tempestade e depois dos 6 elementos; sempre nível 70; Pena nível 5 e fator 0,14.')
OFICIAL = 'OFICIAL_APROVADO_PELO_CRIADOR_2026-11-18'
MARCA_REV8 = 'OFICIAL_POR_DECISAO_DO_CRIADOR_2026-11-18'
PROPOSTA = 'docs/propostas/PROPOSTAS_PENDENCIAS_2026-11-18.md'

# B — aparecimento (biomas: tags de convenção "c:" e biomas vanilla "minecraft:")
ESPECIES = [
    # numero, modo, biomas, horario, condicao, grupo
    (1, 'encontro', ['c:is_desert', 'c:is_badlands'], 'dia', None, [1, 1]),
    (2, 'encontro', ['c:is_river', 'c:is_beach', 'c:is_swamp'], 'qualquer', None, [1, 1]),
    (3, 'encontro', ['c:is_forest', 'c:is_jungle'], 'qualquer', None, [1, 1]),
    (4, 'encontro', ['c:is_desert', 'c:is_mountain_slope'], 'dia', 'mais provável (×2) com chuva ou tempestade no mundo, no deserto (aproximação da "tempestade de areia")', [1, 1]),
    (5, 'encontro', ['c:is_plains', 'c:is_hill', 'c:is_plateau'], 'dia', None, [1, 1]),
    (6, 'encontro', ['c:is_windswept', 'c:is_mountain_peak', 'c:is_plateau'], 'qualquer', 'só durante tempestade (trovoada)', [1, 1]),
    (7, 'comum', ['c:is_savanna', 'c:is_dry_overworld', 'c:is_mountain_slope'], 'dia', None, [1, 2]),
    (8, 'comum', ['minecraft:lush_caves', 'c:is_swamp', 'c:is_river'], 'qualquer', None, [1, 2]),
    (9, 'comum', ['c:is_swamp', 'c:is_forest', 'c:is_plains'], 'noite', None, [1, 3]),
    (10, 'comum', ['c:is_cave', 'c:is_stony_shores', 'c:is_windswept', 'c:is_mountain_peak'], 'noite_ou_subterraneo', None, [1, 2]),
    (11, 'comum', ['c:is_forest', 'c:is_jungle'], 'dia', None, [1, 2]),
    (12, 'comum', ['c:is_desert', 'c:is_badlands', 'minecraft:basalt_deltas'], 'dia', 'no Nether (Deltas de Basalto) com peso 1', [1, 1]),
    (13, 'comum', ['c:is_mountain', 'minecraft:dripstone_caves', 'c:is_mountain_slope'], 'qualquer', None, [1, 1]),
    (14, 'comum', ['c:is_beach', 'minecraft:mangrove_swamp', 'c:is_river'], 'dia', None, [1, 2]),
    (15, 'comum', ['c:is_savanna', 'c:is_badlands', 'c:is_plateau'], 'qualquer', 'peso ×2 durante tempestade', [1, 1]),
    (16, 'comum', ['c:is_swamp', 'c:is_river'], 'dia', None, [1, 2]),
    (17, 'comum', ['c:is_river', 'c:is_forest'], 'dia', None, [1, 1]),
    (18, 'comum', ['minecraft:flower_forest', 'minecraft:meadow', 'c:is_forest'], 'noite', None, [1, 2]),
    (19, 'encontro', ['minecraft:soul_sand_valley', 'minecraft:basalt_deltas'], 'qualquer', 'Nether', [1, 1]),
    (20, 'comum', ['c:is_mountain', 'c:is_plateau'], 'qualquer', 'só durante tempestade (trovoada)', [1, 1]),
    (21, 'comum', ['minecraft:dark_forest', 'minecraft:pale_garden'], 'noite', None, [1, 1]),
    (22, 'encontro', ['c:is_ocean'], 'noite', 'só com chuva', [1, 1]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--revisao', type=int, default=8)
    a = ap.parse_args()
    vig = lambda n: json.load(open(os.path.join(RAIZ, 'base', 'vigente', n), encoding='utf-8'))
    regras = {r['id']: r for r in vig('current_rules.json')}
    especies = {e['numero']: e for e in vig('current_species.json')}
    ops = []

    def confirmar(obj):
        """A — confirma as decisões por extensão da rev. 8 (troca a marca de status)."""
        s = json.dumps(obj, ensure_ascii=False)
        return json.loads(s.replace(MARCA_REV8, OFICIAL + ' (confirmado na rev. 9)'))

    # ---------------------------------------------------------------- A + G (combate, progressão)
    c = confirmar(regras['combate_universal']['payload_json'])
    c['balanceamento_rev9'] = ('I — sem mudança na fórmula agora; medir de novo depois das passivas e dos efeitos dos golpes; '
                               'se o 1×1 seguir abaixo de 4 rodadas, testar dano ×0,88 (arena V5.1, não homologado)')
    ops.append(('current_rules', 'combate_universal', c))

    p = confirmar(regras['progressao']['payload_json'])
    n = p['norma_atributos_rev8']
    n['pendente'] = 'nenhum'
    n['ev_rev9'] = {
        'status': OFICIAL,
        'faixas': ('o custo de EV dobra a cada faixa de 0,5 × total-base vigente da espécie no nível 50 '
                   '(Comum 177–194, Raro 215, Épico 250–255, Mítico 275–285, Quetzacocó 350): EV efetivo = ganho / 2^floor(EV_total / limiar), '
                   'dividindo o ganho através das fronteiras (estrutura da V1.2)'),
        'combate': ('cada Galeto que entrou em campo numa Rinha vencida ganha +0,1 EV por oponente derrotado, no atributo-base mais '
                    'alto do oponente (empate: ordem HP, Atq. Físico, Def. Física, Atq. Mágico, Def. Mágica, Velocidade), pelas mesmas faixas'),
        'treino': 'alimentação da V1.2 (12 alimentos; comum +0,1 EV, raro +1,0 EV; peso +0,8% / +2,5%; 1 a cada 5 min por Galeto)',
        'aprovacao': APROVACAO, 'proposta': PROPOSTA + ' (G)',
    }
    ops.append(('current_rules', 'progressao', p))

    # ---------------------------------------------------------------- A + C + H (captura)
    k = confirmar(regras['captura']['payload_json'])
    k['pena_rev9'] = {
        'status': OFICIAL,
        'obtencao': ('kit de início de jornada: na primeira entrada no mundo o treinador recebe a Pena de Captura nível 1 e escolhe '
                     'um dos seis iniciais (Pirococó, Cocórrego, Esporocó, Cocórak, Cocórion ou Cocórvolt) no nível 5, com IVs sorteados'),
        'posse': ('a Pena traz o dono e só funciona com ele; não cai na morte; se for destruída, volta ao inventário do dono ao entrar '
                  'no mundo ou ao acordar numa cama; uma Pena nova invalida as anteriores; sem receita'),
        'aparencia': ('pena clara com rubi lapidado no centro preso por aro dourado; a cor da pena muda por nível (1 branca, 2 bronze, '
                      '3 prata, 4 ouro, 5 carmesim com brilho); a dica mostra nível e XP; arte a gerar no ChatGPT'),
        'feixe_do_rubi': 'só no sucesso: linha de partículas #E0115F da Pena ao Galeto por 0,5 s; o Galeto encolhe e some em 10 ticks; som curto de "plim"',
        'aprovacao': APROVACAO, 'proposta': PROPOSTA + ' (C)',
    }
    k['lendario_original'] = {
        'status': OFICIAL,
        'especie': 23,
        'fator_R': 0.14,
        'nivel_minimo_pena': 5,
        'regra': 'Quetzacocó (Lendário Original) usa o fator R do Lendário (0,14) e exige Pena nível 5, nas duas modalidades',
        'aprovacao': APROVACAO, 'proposta': PROPOSTA + ' (H)',
    }
    ops.append(('current_rules', 'captura', k))

    # ---------------------------------------------------------------- A + D + E (treinador)
    t = confirmar(regras['treinador']['payload_json'])
    t['escalacao_rev9'] = {
        'status': OFICIAL,
        'regra': ('antes de cada Rinha o treinador escolhe 3 dos 5 da equipe principal e quem começa; o padrão marcado são os 3 '
                  'primeiros da ordem, com o 1º começando'),
        'reservas_acessiveis_mestres': 'a equipe principal (5)',
        'troca_equipe_reservas': 'em qualquer lugar fora da Rinha, sem custo, pelo Galetário (aba Equipe e Reservas)',
        'aprovacao': APROVACAO, 'proposta': PROPOSTA + ' (D)',
    }
    t['companheiro_rev9'] = {
        'status': OFICIAL,
        'regra': ('1 Galeto da equipe pode seguir o treinador no mundo: teleporta se passar de 24 blocos, não ataca mobs, é invulnerável '
                  'fora da Rinha, não pode ser desafiado nem capturado por outros; volta à equipe ao começar uma Rinha, quando o '
                  'jogador sai ou ao ser tocado com a Pena de Captura; conta como ativo e carregado para o Peso V1.2'),
        'terreiro': 'o Terreiro recebe os dois Galetos direto da equipe e os mostra sobre o bloco',
        'libertar': ('soltar um Galeto para sempre, com confirmação dupla: vira selvagem no lugar, mantém nível e IVs; '
                     'não vale para o último Galeto da equipe'),
        'aprovacao': APROVACAO, 'proposta': PROPOSTA + ' (E)',
    }
    ops.append(('current_rules', 'treinador', t))

    # ---------------------------------------------------------------- F (aprendizado)
    ap_ = copy.deepcopy(regras['aprendizado']['payload_json'])
    novas = json.load(open(os.path.join(RAIZ, 'docs', 'propostas', 'proposta_aprendizado_013_018_023.json'), encoding='utf-8'))
    for e, linhas in novas.items():
        ap_['tabelas'][e] = [{k2: v for k2, v in l.items() if k2 != 'origem'} for l in linhas]
    ap_['cobertura'] = {'com_tabela': sorted(int(e) for e in ap_['tabelas']), 'sem_dado_no_acervo': []}
    ap_['tabelas_rev9'] = {
        'especies': [13, 14, 15, 16, 17, 18, 23], 'status': OFICIAL,
        'criterio': ('padrão medido nas 16 tabelas: origem nos níveis 1/1/17/37/50; aprendíveis do elemento da espécie, alternando os '
                     'elementos; dano na categoria do ataque mais forte; metade suporte; Energia crescente com o nível'),
        'gerador': 'ferramentas/propostas/propor_aprendizado.py', 'aprovacao': APROVACAO, 'proposta': PROPOSTA + ' (F)',
    }
    ops.append(('current_rules', 'aprendizado', ap_))

    # ---------------------------------------------------------------- B + H (aparecimento)
    tabela = []
    for numero, modo, biomas, horario, cond, grupo in ESPECIES:
        e = especies[numero]
        peso = {'Comum': 6, 'Raro': 2, 'Épico': 1}.get(e['raridade']) if modo == 'comum' else None
        tabela.append({'numero': numero, 'nome': e['nome'], 'raridade': e['raridade'], 'modo': modo, 'biomas': biomas,
                       'horario': horario, 'condicao': cond, 'grupo': grupo, 'peso': peso})
    mundo = {
        'status': OFICIAL,
        'aprovacao': APROVACAO,
        'proposta': PROPOSTA + ' (B e H)',
        'nivel_selvagem': {'regra': 'sorteado de forma uniforme entre 1 e 70, independente do local, da dimensão e da raridade',
                           'minimo': 1, 'maximo': 70},
        'pesos_por_raridade': {'Comum': 6, 'Raro': 2, 'Épico': 1, 'referencia': 'galinha vanilla = 10'},
        'limite': {'selvagens_por_jogador': 6, 'raio_blocos': 64},
        'desaparecimento': 'como os animais vanilla quando longe, exceto em Rinha ou com espera de captura ativa',
        'encontros_raros': {
            'especies': [1, 2, 3, 4, 5, 6, 19, 22],
            'chance': 0.01,
            'quando': ('uma checagem por jogador a cada período elegível: manhã para os diurnos, anoitecer para os noturnos e os de '
                       'qualquer hora; os que dependem de tempestade checam a cada minuto de tempestade'),
            'maximo_ativos_por_jogador': 1,
        },
        'iniciais': 'fora do aparecimento comum: um vem no kit de início e os outros cinco aparecem como encontros raros',
        'divinos': 'não aparecem naturalmente (decisão de 09/11)',
        'especies': tabela,
        'quetzacoco': {
            'regra': ('Lendário Original único por mundo: extremamente raro, só em selva (inclui bambuzal) ou montanha alta durante '
                      'tempestade (trovoada), e só para um treinador que tenha registrado Galetos dos 6 elementos; aparece sempre no '
                      'nível 70; ao aparecer, mensagem global no chat para todos os jogadores, sem coordenadas; se não for capturado, '
                      'foge no fim da tempestade e pode voltar numa próxima elegível; depois de capturado, nunca mais aparece no mundo'),
            'chance': 0.002,
            'chance_unidade': 'por minuto de tempestade, por jogador elegível (cerca de 1,6% por tempestade média de 8 min)',
            'nivel': 70,
            'biomas': ['c:is_jungle', 'minecraft:bamboo_jungle', 'c:is_mountain_peak'],
            'mensagem_global': 'O Quetzacocó, Lendário Original, apareceu em algum lugar do mundo durante a tempestade!',
        },
    }
    ops.append(('current_rules', 'mundo_aparecimento', mundo, 'inserir'))

    # ---------------------------------------------------------------- pendências
    resolvidas = {
        'U03': 'Tabela do #023 aprovada na rev. 9 (regra aprendizado)',
        'U07': 'Regra mundo_aparecimento (rev. 9): biomas, horários, pesos, encontros raros, nível 1–70',
        'U08': 'captura.pena_rev9: kit de início, posse, aparência e Feixe do Rubi; falta só gerar a arte no ChatGPT',
        'U09': 'treinador.escalacao_rev9',
        'U10': 'treinador.companheiro_rev9',
        'U11': 'Tabelas de #013–#018 aprovadas na rev. 9 (regra aprendizado)',
        'U12': 'progressao.norma_atributos_rev8.ev_rev9',
    }
    operacoes = []
    for t_, chave, valor, *modo in ops:
        operacoes.append({'op': modo[0] if modo else 'atualizar', 'table': t_, 'key': {'id': chave},
                          'values': {'payload_json': valor} if not modo else
                          {'payload_json': valor, 'source_ref': PROPOSTA + ' (B e H), aprovada em 18/11/2026', 'status': 'OFICIAL_DOCUMENTAL'}})
    for i, ev in resolvidas.items():
        operacoes.append({'op': 'atualizar', 'table': 'current_issues', 'key': {'id': i},
                          'values': {'status': 'RESOLVIDO_ARTE_A_GERAR' if i == 'U08' else 'RESOLVIDO', 'evidencia': ev,
                                     'proximo_passo': 'Gerar a arte da Pena no ChatGPT (pedido em ' + PROPOSTA + ', C4)' if i == 'U08' else 'Nenhum'}})
    pacote = {
        'expected_revision': a.revisao,
        'reason': ('Decisões do criador de 18/11/2026 sobre as propostas das pendências: A, C, D, E, F, G e I aprovadas; B aprovada com '
                   'nível 1–70 independente do local; H aprovada com aparecimento extremamente raro e aviso global no chat.'),
        'evidence': {'aprovacao': APROVACAO, 'proposta': PROPOSTA,
                     'tabelas_aprendizado': 'docs/propostas/proposta_aprendizado_013_018_023.json'},
        'operations': operacoes,
    }
    with open(a.saida, 'w', encoding='utf-8') as f:
        json.dump(pacote, f, ensure_ascii=False, indent=1)
    print('ok', a.saida, len(operacoes), 'operações')


if __name__ == '__main__':
    main()

"""Gera o pacote rev. 8: resolve as pendências de regra com os dados mais recentes do acervo, por instrução
expressa do criador em 18/11/2026 ("Resolve esses problemas todos com base nos dados mais recentes que temos
disponíveis").

O que entra (sempre com fonte; nada é criado sem dado):
1. progressao: curva dos níveis 1–49, HP nominal, HP de referência, IV/EV e peso (normas R5.4 de 14/11,
   reafirmadas na R5.5 de 15/11; IV/EV oficiais de 08/11; Peso V1.2 de 09/11) + tabela dos 100 níveis.
2. dano_v5_6: Resistência por Vitalidade V5.6.1 (homologada em 13/11) com o HP de referência da R5.4.
3. combate_universal: HP por nível; desempate de trocas com Velocidade igual (extensão do sorteio 50/50 oficial);
   espécie repetida no trio permitida (formato oficial dos Mestres, 3 Galetos de 2 espécies); precisão original
   dos golpes = 100% (nenhum golpe tem precisão própria em fonte alguma).
4. captura: posição da tentativa na rodada, tentativa contra alvo inelegível (proposta do auditor de 12/11), alvo
   válido (só selvagem fora de Rinha).
5. treinador: duplicatas permitidas.
6. aprendizado (regra nova): política da Beta 1.2.61 e da Regra dos Quatro Slots v2 + tabelas por espécie:
   #001–#012 (grades homologadas em 12/11, conciliadas com o repertório vigente), #019 (distribuição de 12/11
   preparada a pedido do criador), #020 e #021 (fichas oficiais de 12/11), #022 (homologação de 13/11).
7. current_issues: R13 resolvida; R15 e U03 atualizadas; pendências sem nenhum dado no acervo registradas (U07–U12).

Uso:
  python gerar_rev8_resolucoes.py --historico Galetocraft_rev4.sqlite --acervo <acervo_txt> --saida docs/patches/rev8_resolucoes.json
"""
import argparse, copy, json, os, re, sqlite3, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APROVACAO = ('Instrução expressa do criador em 18/11/2026: "Resolve esses problemas todos com base nos dados mais recentes '
             'que temos disponíveis".')
DECISAO = 'OFICIAL_POR_DECISAO_DO_CRIADOR_2026-11-18'
MARCOS = [1, 1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 44, 47, 50]


def n(s):
    return unicodedata.normalize('NFC', s).strip().lower()


def carregar(nome):
    return json.load(open(os.path.join(RAIZ, 'base', 'vigente', nome), encoding='utf-8'))


def tabela_md(caminho, titulo):
    """Linhas da primeira tabela markdown depois do título (lista de listas de células)."""
    linhas = open(caminho, encoding='utf-8').read().splitlines()
    i = next(k for k, l in enumerate(linhas) if l.startswith('## ') and titulo in l)
    out = []
    for l in linhas[i + 1:]:
        if l.startswith('## '):
            break
        if l.startswith('|') and not re.match(r'^\|\s*-', l) and not re.match(r'^\|[-:| ]+\|$', l):
            cel = [c.strip() for c in l.strip().strip('|').split('|')]
            out.append(cel)
    return out[1:]   # sem o cabeçalho


def tabelas_aprendizado(con, acervo, moves):
    repert = {}
    for m in moves:
        repert.setdefault(m['especie'], []).append(m)
    tabelas, conciliacao = {}, {}

    def montar(esp, por_nivel, treino_declarado, fonte, completar_com_treino):
        vig = {n(m['nome']): m['nome'] for m in repert[esp]}
        linhas, usados, sem_vigente = [], set(), []
        for nivel, nome in por_nivel:
            if n(nome) in vig and n(nome) not in usados:
                linhas.append({'nome': vig[n(nome)], 'metodo': 'nivel', 'nivel': nivel})
                usados.add(n(nome))
            else:
                sem_vigente.append({'nivel': nivel, 'golpe_da_fonte': nome})
        for nome in treino_declarado:
            if n(nome) in vig and n(nome) not in usados:
                linhas.append({'nome': vig[n(nome)], 'metodo': 'treinamento'})
                usados.add(n(nome))
        faltam = [vig[k] for k in vig if k not in usados]
        if faltam and not completar_com_treino:
            raise SystemExit(f'#{esp:03d}: golpes vigentes sem método na fonte {fonte}: {faltam}')
        for nome in faltam:
            linhas.append({'nome': nome, 'metodo': 'treinamento', 'sem_marco_na_grade': True})
        originais = {n(m['nome']) for m in repert[esp] if m['grupo'] == 'original'}
        fora = [l['nome'] for l in linhas if n(l['nome']) in originais and l['metodo'] != 'nivel']
        if fora:
            raise SystemExit(f'#{esp:03d}: golpes de origem fora do aprendizado por nível: {fora}')
        assert len(linhas) == len(repert[esp]) == 30, (esp, len(linhas))
        tabelas[str(esp)] = sorted(linhas, key=lambda l: (l['metodo'] != 'nivel', l.get('nivel', 0), l['nome']))
        if sem_vigente or faltam:
            conciliacao[str(esp)] = {'marcos_sem_golpe_vigente': sem_vigente, 'golpes_vigentes_sem_marco_vao_para_treinamento': faltam}

    # #001–#012: grades homologadas na Beta 1.2.61 (12/11)
    for esp in range(1, 13):
        rows = con.execute('SELECT nivel, nome, metodo FROM v_gc54_aprendizado_completo_v1261 WHERE especie_num=? '
                           'ORDER BY nivel', (esp,)).fetchall()
        montar(esp, [(lv, nm) for lv, nm, mt in rows if mt == 'por_nivel'],
               [nm for lv, nm, mt in rows if mt != 'por_nivel'], 'v_gc54_aprendizado_completo_v1261', True)
    # #019: distribuição de 12/11 preparada a pedido do criador
    d19 = json.load(open(os.path.join(acervo, 'Galetocraft_13_Acervo', 'Progressao_019_Renacoco_15_Niveis_15_Treinamento_2026-11-12.json'), encoding='utf-8'))
    montar(19, [(x['nivel'], x['nome']) for x in d19['progressao_por_nivel']], [x['nome'] for x in d19['treinamento_apenas']],
           'Progressao_019', False)
    # #020 e #021: fichas oficiais de 12/11
    f20 = os.path.join(acervo, 'Galetocraft_01_Acervo', 'Galetario_020_Frankoco_OFICIAL_2026-11-12.md')
    montar(20, [(int(c[0]), c[1]) for c in tabela_md(f20, 'Progressão oficial')],
           [c[1] for c in tabela_md(f20, 'Exclusivas de treinamento')], 'ficha #020', False)
    f21 = os.path.join(acervo, 'Galetocraft_01_Acervo', 'Galetario_021_Cabacoco_OFICIAL_2026-11-12.md')
    montar(21, [(int(c[0]), c[1]) for c in tabela_md(f21, 'Progressão oficial')],
           [c[1] for c in tabela_md(f21, 'Treinamento com Mestres')], 'ficha #021', False)
    # #022: homologação integral de 13/11
    rows = con.execute('SELECT mecanismo, nivel, nome FROM gc53_aprendizado_022 ORDER BY ordem').fetchall()
    montar(22, [(lv, nm) for mec, lv, nm in rows if mec == 'nivel'], [nm for mec, lv, nm in rows if mec != 'nivel'],
           'gc53_aprendizado_022', False)
    return tabelas, conciliacao


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--historico', required=True)
    ap.add_argument('--acervo', required=True)
    ap.add_argument('--saida', required=True)
    ap.add_argument('--revisao', type=int, default=7)
    a = ap.parse_args()
    con = sqlite3.connect(f'file:{a.historico}?mode=ro', uri=True)
    regras = {r['id']: r for r in carregar('current_rules.json')}
    issues = {i['id']: i for i in carregar('current_issues.json')}
    moves = carregar('current_moves.json')
    ops = []

    # ---------------------------------------------------------------- 1. progressão
    normas = {k: (f, s) for k, f, s in con.execute('SELECT chave, formula, status FROM gc54_normas')}
    curva = [{'nivel': lv, 'fator': f'{nu}/{de}', 'hp_ref': hp} for lv, nu, de, hp in
             con.execute('SELECT nivel, numerador, denominador, hp_ref FROM gc54_curva_niveis ORDER BY nivel')]
    assert len(curva) == 100 and curva[49]['hp_ref'] == 126 and curva[99]['hp_ref'] == 189
    p = copy.deepcopy(regras['progressao']['payload_json'])
    norma = {
        'status': DECISAO,
        'aprovacao': APROVACAO,
        'atributos_1_49': 'A(L) = A50 × (49 + 3(L−1))/196, 1 ≤ L ≤ 49 (25% no nível 1; 98,47% no 49)',
        'atributos_50_100': 'A(L) = A50 × (L+50)/100 (Nível 50 V1, homologada em 13/11)',
        'hp_nominal_1_49': 'HP_n(L) = round_half_up(10 + (ceil(1,5·HP50) − 10)·(L−1)/49)',
        'hp_nominal_50_100': 'HP_n(L) = ceil(1,5·HP50·(L+50)/100)',
        'hp_origem': 'Combate v1.0 (08/11, aprovado): HP 10 no nível 1 e 1,5 × o HP-base; norma R5.4 completa a interpolação',
        'iv_ev': 'A = floor(A_n × (1 + (0,25·IV + 0,5·√EV)/100)); IV de 1 a 40; EV sem teto (oficial desde 08/11)',
        'peso': ('depois de IV/EV, multiplicador do Peso V1.2 com r = peso/peso natural (0,8–1,5; nasce com r = 1): '
                 'r ≥ 1: HP 1+0,10(r−1), defesas 1+0,15(r−1), Velocidade 1−0,50(r−1); '
                 'r < 1: HP 1+0,40(r−1), defesas 1+0,50(r−1), Velocidade 1−0,20(r−1); ataques sem efeito; '
                 'inteiro mais próximo, empate para cima, mínimo 1; peso congelado na Rinha'),
        'ordem': ['valor nominal no nível (HP pela fórmula própria)', 'IV/EV com floor', 'peso com half-up e mínimo 1'],
        'hp_referencia': 'HP_ref(L) = floor(1,05 × HP_n(L; HP50 = 80)) — IV 20, EV 0, peso neutro',
        'curva_niveis': curva,
        'pendente': 'faixas de dificuldade de EV recalibradas para os totais do nível 50 (a V1.2 usa os totais antigos)',
        'fontes': [
            {'tabela': 'gc54_normas (Galetocraft.sqlite rev. 2)', 'status_na_fonte': {k: normas[k][1] for k in
             ('ATRIBUTOS_1_49', 'HP_1_49', 'HP_50_100', 'HP_REF_1_100', 'IV_EV', 'PESO')}},
            {'arquivo': 'RELATORIO_GERAL_CONSOLIDACAO_R5_4.md', 'data': '2026-11-14',
             'sha256': '6db6e418c2468c060d71e11691980887b4975b214e882a2849182608323edc74'},
            {'arquivo': 'RELATORIO_GERAL_AUDITORIA_R55_2026-11-15.md', 'data': '2026-11-15',
             'sha256': '23a3a4f877e2c08a9f4a9936280b6e4938806fe2008f09b1d56f7906bdf86ba4',
             'trecho': 'Curva 1–49 e HPref dos 100 níveis adotados na linha candidata R5.4'},
            {'arquivo': 'Galetocraft_Relatorio_Peso_Alimentacao_v1_2.md', 'data': '2026-11-09',
             'sha256': '1a50dab07d3311f6dd9b96bd9e0968db0db3626282d2a4f15f9536381ad4485a'},
            {'registro': 'gc161_decisoes_index beta0:ev_system (OFICIAL_APROVADO, 08/11)',
             'trecho': 'EVs independentes e sem teto; bônus de EV 0,5×√EV; IV 0,25% por ponto'},
        ],
    }
    ni = p['norma_integral']
    ni['abaixo_50'] = 'ver norma_atributos_rev8 (curva R5.4 adotada em 18/11)'
    ni['arredondamento_inteiro'] = 'ver norma_atributos_rev8.ordem (floor em IV/EV; half-up no peso)'
    ni['hp_efetivo'] = 'ver norma_atributos_rev8 (HP nominal R5.4 adotado em 18/11)'
    ni['ivs_evs'] = 'ver norma_atributos_rev8.iv_ev'
    ni['peso'] = 'ver norma_atributos_rev8.peso'
    p['norma_atributos_rev8'] = norma
    ops.append({'op': 'atualizar', 'table': 'current_rules', 'key': {'id': 'progressao'}, 'values': {'payload_json': p}})

    # ---------------------------------------------------------------- 2. Vitalidade
    d = copy.deepcopy(regras['dano_v5_6']['payload_json'])
    d['vitalidade_v5_6_1'] = {
        'formula': 'Fvit = clamp((HP_ref(L)/HPmax_defensor)^0,2; 0,8; 1,0), L = nível do defensor',
        'aplicacao': 'multiplica D_base: dano = ceil(HPmax × Poder/400 × (A/D)^0,7 × Fvit × eficácia × modificadores)',
        'efeito': 'Galetos com HP acima da referência do nível recebem até 20% menos dano; abaixo dela, nenhum efeito',
        'hp_referencia': 'progressao.norma_atributos_rev8.hp_referencia',
        'status': 'fórmula homologada em 13/11 (V5.6.1); HP_ref da R5.4 adotado por decisão do criador em 18/11',
        'fontes': [{'tabela': 'gc52_regras VITALIDADE_V5_6_1', 'trecho': 'clamp((HP_ref(nivel)/HPmax_efetivo)^0.2,0.8,1.0)'},
                   {'tabela': 'gc54_normas VITALIDADE e DANO', 'trecho': normas['DANO'][0]}],
        'aprovacao': APROVACAO,
    }
    ops.append({'op': 'atualizar', 'table': 'current_rules', 'key': {'id': 'dano_v5_6'}, 'values': {'payload_json': d}})

    # ---------------------------------------------------------------- 3. combate universal
    c = copy.deepcopy(regras['combate_universal']['payload_json'])
    c.setdefault('hp', {})
    c['hp']['por_nivel_rev8'] = 'ver progressao.norma_atributos_rev8 (HP_n e IV/EV/peso)'
    c['trocas']['criterio_desempate_trocas_voluntarias_mesma_velocidade'] = (
        'sorteio 50/50 a cada rodada — extensão da regra oficial desempate_velocidade (Balanceamento v1.1, 09/11); '
        f'{DECISAO}')
    eq = c.get('equipes_3v3', {})
    eq['species_duplicate_policy'] = (
        'permitida: o formato oficial dos Mestres (10/11) tem trios de 3 Galetos com 2 espécies; '
        f'a hipótese "distintas" era só de simulação; {DECISAO}')
    c['equipes_3v3'] = eq
    c['precisao_golpes'] = {
        'precisao_original': 1.0,
        'regra': 'todos os golpes têm precisão original de 100%; a Mira multiplica essa precisão e a esquiva universal se aplica',
        'evidencia': 'nenhuma tabela, catálogo ou ficha traz precisão por golpe; a ideia #03 "Ataques de Precisão" não foi aprovada',
        'status': DECISAO,
    }
    ops.append({'op': 'atualizar', 'table': 'current_rules', 'key': {'id': 'combate_universal'}, 'values': {'payload_json': c}})

    # ---------------------------------------------------------------- 4. captura
    k = copy.deepcopy(regras['captura']['payload_json'])
    rinha = next(m for m in k['modalidades'] if m['modalidade'] == 'rinha')
    rinha['posicao_na_rodada'] = ('na vez do treinador, pela Velocidade do Galeto ativo dele (ordem regular: trocas, depois ações '
                                  f'por Velocidade, empate 50/50); {DECISAO}')
    rinha['fonte_posicao'] = ('captura_pena_rinha_falha_acao_adversario_v1252: "depende de sua posição na ordem regular e de haver '
                              'uma ação pendente"')
    k['lendarios']['comportamento_tentativa_inelegivel'] = (
        'tentativa indisponível: não começa, não consome ação nem gera espera, com aviso ao treinador; vale para Lendário sem Pena 5 '
        'e para classes sem fator de captura (Lendário Original, Divino); '
        f'proposta do auditor na Auditoria Geral de Capturas 1.2.58 (12/11), adotada: {DECISAO}')
    k['alvo_valido'] = {
        'regra': 'somente Cocorídeo selvagem que não esteja em Rinha; Galetos de treinador não são alvo',
        'evidencia': ['todas as homologações da Pena tratam de "Cocorídeo selvagem" (Betas 1.2.33 a 1.2.59)',
                      'Reprodução Etapa 01 (16/11): indivíduos não podem ser usados simultaneamente em Terreiros ou Rinhas'],
        'status': DECISAO,
    }
    ops.append({'op': 'atualizar', 'table': 'current_rules', 'key': {'id': 'captura'}, 'values': {'payload_json': k}})

    # ---------------------------------------------------------------- 5. treinador
    t = copy.deepcopy(regras['treinador']['payload_json'])
    t['reservas']['regra_duplicatas'] = f'permitidas (mesma evidência de combate_universal.equipes_3v3); {DECISAO}'
    ops.append({'op': 'atualizar', 'table': 'current_rules', 'key': {'id': 'treinador'}, 'values': {'payload_json': t}})

    # ---------------------------------------------------------------- 6. aprendizado
    tabelas, conciliacao = tabelas_aprendizado(con, a.acervo, moves)
    pol = dict(con.execute('SELECT * FROM galeto_aprendizado_politica_v1261').fetchone() and
               zip([x[0] for x in con.execute('SELECT * FROM galeto_aprendizado_politica_v1261').description],
                   con.execute('SELECT * FROM galeto_aprendizado_politica_v1261').fetchone()))
    aprendizado = {
        'status': DECISAO,
        'aprovacao': APROVACAO,
        'politica': {
            'maximo_golpes_equipados': pol.get('maximo_golpes_equipados', 5),
            'concentracao_fixa': True,
            'conserva_golpes_desequipados': True,
            'equipa_automaticamente_apos_desbloqueio': False,
            'retrodesbloqueio_por_nivel_na_captura': True,
            'golpes_por_nivel_incluindo_origem': 15,
            'golpes_por_treinamento_mestres': 15,
            'troca_de_slots': ('depois de desbloquear os 5 golpes de origem, o treinador troca qualquer golpe equipado, exceto a '
                               'Concentração, por outro já aprendido (Regra Oficial dos Quatro Slots v2, 10/11)'),
            'momento_da_troca': ('fora da Rinha, por comando do treinador; a regra dos Quatro Slots não definiu o momento e a '
                                 f'Beta 1.2.61 diz que nada é substituído sem comando do treinador; {DECISAO}'),
            'fonte_aprovacao_politica': pol.get('aprovacao_expressa'),
        },
        'marcos_por_nivel': MARCOS,
        'tabelas': tabelas,
        'conciliacao_001_012': {
            'regra': ('as grades homologadas em 12/11 usam o repertório anterior à Reforma Integral; vale o repertório vigente: '
                      'marco cujo golpe saiu do repertório fica vazio, e golpe vigente sem marco é aprendido por treinamento'),
            'detalhe': conciliacao,
        },
        'cobertura': {'com_tabela': sorted(int(e) for e in tabelas), 'sem_dado_no_acervo': [13, 14, 15, 16, 17, 18, 23]},
        'fontes': [
            {'arquivo': 'Galetocraft_Homologacao_Grades_Aprendizado_Beta_1.2.61_2026-11-12.md', 'especies': '001–012',
             'sha256': '07c97743f0275080647924a158f8ccecb9c94514d2b7991b6e2711bbd080dd0b', 'tabela': 'v_gc54_aprendizado_completo_v1261'},
            {'arquivo': 'Progressao_019_Renacoco_15_Niveis_15_Treinamento_2026-11-12.json', 'especies': '019',
             'sha256': '2171d0116bcda59f7688126272ac4159f5fd5fa90e78b11603d4bb4342f5c451',
             'status_na_fonte': 'DISTRIBUICAO_DE_PROGRESSAO_PREPARADA_A_PEDIDO_DO_CRIADOR'},
            {'arquivo': 'Galetario_020_Frankoco_OFICIAL_2026-11-12.md', 'especies': '020',
             'sha256': '8249779559a02ad1975f155b18acb4aab366724dfabb6c5b8eead6913285e30e'},
            {'arquivo': 'Galetario_021_Cabacoco_OFICIAL_2026-11-12.md', 'especies': '021',
             'sha256': '16b430179f3839fb4240a02482473d5c59da942df73be30060268476c187077c'},
            {'tabela': 'gc53_aprendizado_022', 'especies': '022', 'trecho': 'homologacao integral #022 13/11/2026'},
            {'arquivo': 'Galetocraft_Regra_Oficial_Personalizacao_Quatro_Slots_v2.md', 'data': '2026-11-10',
             'sha256': 'a9535a2a5f9a2e3b500532f1ce49e85397f825ec911106ea6f4fda7601bcab41'},
        ],
    }
    ops.append({'op': 'inserir', 'table': 'current_rules', 'key': {'id': 'aprendizado'},
                'values': {'payload_json': aprendizado, 'source_ref': 'Beta 1.2.61 (12/11), fichas #019–#022 e Quatro Slots v2',
                           'status': 'OFICIAL_DOCUMENTAL'}})

    # ---------------------------------------------------------------- 7. pendências
    ops.append({'op': 'atualizar', 'table': 'current_issues', 'key': {'id': 'R13'},
                'values': {'status': 'RESOLVIDO', 'evidencia': 'Normas R5.4 (curva 1–49, HP nominal, HP_ref) adotadas em 18/11; ver progressao.norma_atributos_rev8',
                           'proximo_passo': 'Nenhum; recalibrar só as faixas de EV (U12)'}})
    ops.append({'op': 'atualizar', 'table': 'current_issues', 'key': {'id': 'R15'},
                'values': {'evidencia': issues['R15']['evidencia'] + '; rev. 8: tabelas de aprendizado de 16 espécies na regra aprendizado',
                           'proximo_passo': 'Golpes aprendíveis seguem sem efeito executável aprovado; aprendizado de #013–#018 e #023 sem dado (U11, U03)'}})
    ops.append({'op': 'atualizar', 'table': 'current_issues', 'key': {'id': 'U03'},
                'values': {'evidencia': 'Ficha #023 de 16/11: "Pendente, não homologado nesta etapa: níveis e meios específicos de aprendizagem"; nada mais novo no acervo'}})
    novas = [
        ('U07', 'Aparecimento no mundo (spawn)', 'Nenhuma regra de bioma, frequência, grupo, horário ou nível dos selvagens no acervo; só habitats narrativos de #010 e #016–#018 e "Divinos não aparecem naturalmente" (09/11)',
         'Decidir biomas, pesos e faixas de nível por espécie'),
        ('U08', 'Pena de Captura: obtenção e aparência', 'Oficial: pena com rubi central, uma por treinador, não consumível; nome_exato, design_exato, obtenção, recuperação, perda e receita são NULL (v1216)',
         'Decidir como o treinador recebe e recupera a Pena; gerar a arte no ChatGPT'),
        ('U09', 'Gerenciamento da equipe e escalação da Rinha', 'procedimento_troca_equipe_reservas, interface_gerenciamento e team_lead_selection_policy sem definição (hipótese de simulação: aleatória)',
         'Decidir quais 3 dos 5 entram na Rinha, quem começa e como trocar com as reservas'),
        ('U10', 'Galeto do treinador no mundo', 'Reprodução Etapa 01 e Peso V1.2 pressupõem Galetos do treinador no mundo, mas não há regra para soltar/recolher',
         'Decidir como o Galeto sai da equipe para o mundo e volta'),
        ('U11', 'Aprendizado de #013–#018', 'Nenhuma grade por nível ou treinamento no acervo; a ficha do #013 proíbe inventar nível de aprendizado',
         'Distribuir os 30 golpes de cada espécie (15 por nível, 15 por treinamento)'),
        ('U12', 'Faixas de dificuldade de EV', 'A V1.2 dobra o custo a cada 50% da soma de base "no nível 100" (totais antigos, 850 no Mítico); não há versão no nível 50',
         'Recalibrar as faixas para os totais do nível 50 e definir os ganhos de EV em combate e treino'),
    ]
    for i, assunto, evid, prox in novas:
        ops.append({'op': 'inserir', 'table': 'current_issues', 'key': {'id': i},
                    'values': {'assunto': assunto, 'status': 'PENDENTE_SEM_DADO', 'evidencia': evid, 'proximo_passo': prox}})

    pacote = {
        'expected_revision': a.revisao,
        'reason': ('Resolução das pendências de regra com os dados mais recentes do acervo, por instrução do criador em 18/11/2026: '
                   'curva 1–49, HP efetivo, Vitalidade V5.6.1, IV/EV/peso, aprendizado de golpes e slots, desempates, duplicatas, '
                   'precisão base, captura (posição, inelegível, alvo); pendências sem nenhum dado registradas. '
                   'Ave Fênix confirmada em E100 (Energia V4 homologada em 11/11), sem alteração.'),
        'evidence': {
            'aprovacao': APROVACAO,
            'pesquisa': 'acervo-documental-2026-11-17 (909 documentos de texto) e Galetocraft.sqlite rev. 2, em 18/11/2026',
            'ave_fenix': {'arquivo': 'Galetocraft_Energia_v4_GLOBAL_HOMOLOGADA_20261111.json',
                          'sha256': '74611bc039b3984e990f2f8f5d165a1b747c819f1eb6a6f2f4c02d79334e6609',
                          'trecho': '{"codigo": "ave_fenix", "poder": 180, "energia_anterior": 50, "energia_nova": 100}'},
            'mestres_trio': {'arquivo': 'Galetocraft_Formato_Batalha_Mestres_3x3_1x1_OFICIAL_v1_0.md',
                             'sha256': '84db8d232286682250749c0951240c76744531ada62143c88a3b1644200b6e3d'},
            'auditoria_capturas': {'arquivo': 'Galetocraft_Auditoria_Geral_Capturas_Beta_1.2.58_2026-11-12.md',
                                   'sha256': 'ac590d12378212be0e155b44baee6c49326075ad690823f3e06031a8b85005d3',
                                   'trecho': 'Tratar como ação indisponível na interface por padrão técnico, sem criar uma tentativa válida'},
            'reproducao_etapa01': {'arquivo': 'Galetocraft_Reproducao_Etapa01_HOMOLOGADA_2026-11-16.md',
                                   'sha256': 'e0fa86330a29d1c907834f0997849a48fcc54d7c1ef72d2343a45f050835967e'},
        },
        'operations': ops,
    }
    with open(a.saida, 'w', encoding='utf-8') as f:
        json.dump(pacote, f, ensure_ascii=False, indent=1)
    print('ok', a.saida, len(ops), 'operações;', 'tabelas de aprendizado:', sorted(int(e) for e in tabelas))
    print('conciliação:', json.dumps(conciliacao, ensure_ascii=False)[:1500])


if __name__ == '__main__':
    main()

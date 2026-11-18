"""Gera o pacote de migração rev. 5: regras oficiais de combate, captura e progressão para current_rules.

Antes deste pacote, essas regras (marcadas como oficiais) só existiam em tabelas históricas do
Galetocraft.sqlite da revisão 2: combat_rules, effectiveness, environmental_fields, captura_*,
cocorideo_xp_*, treinador_* e held_item_categories. O dano V5.6, homologado em 13/11/2026, nem
estava na base. O pacote só copia o que já é oficial, com a fonte de cada regra. As regras
superadas por normas posteriores ficam listadas, e não são migradas como vigentes.

Uso:
  python gerar_rev5_regras_combate.py --historico Galetocraft_rev2.sqlite --saida docs/patches/rev5_regras_de_combate.json
"""
import argparse, json, sqlite3

DATA = '2026-11-18'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--historico', required=True)
    ap.add_argument('--saida', required=True)
    ap.add_argument('--revisao', type=int, default=4)
    a = ap.parse_args()
    c = sqlite3.connect(f'file:{a.historico}?mode=ro', uri=True)

    def linhas(sql):
        cur = c.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur]

    cr = {r['id']: json.loads(r['value_json']) for r in linhas('SELECT id, value_json FROM combat_rules')}
    amb = {r['effect_id']: json.loads(r['effect_json']) for r in linhas('SELECT effect_id, effect_json FROM environmental_fields')}

    elementos = ['Fogo', 'Água', 'Planta', 'Terra', 'Ar', 'Elétrico']
    matriz = {e: {} for e in elementos}
    for r in linhas('SELECT attacker_element, defender_element, multiplier FROM effectiveness'):
        matriz[r['attacker_element']][r['defender_element']] = r['multiplier']

    regras = {}
    regras['matriz_elemental'] = ({
        'elementos': elementos, 'multiplicadores': matriz,
        'neutro_e_sem_elemento': 1.0, 'suporte_nao_aplica_eficacia': True,
        'dupla_e_tripla': 'ver tipagem_dupla (V1) e nexo (V2.0)',
    }, 'combat_rules.matriz_elemental_6 + effectiveness (histórico rev. 2, oficial)')

    regras['dano_v5_6'] = ({
        'versao': 'V5.6', 'data': '2026-11-13', 'status_fonte': 'FÓRMULA-BASE OFICIAL / HOMOLOGADA EXPRESSAMENTE PELO CRIADOR',
        'formula': 'D_base = HPmax_defensor × Poder/400 × (Ataque_efetivo / max(1, Defesa_efetiva))^0,7',
        'hp_referencia': 'HP máximo efetivo atual do defensor (não o HP restante)',
        'par_ataque_defesa': 'físico ou mágico, conforme a categoria do golpe',
        'arredondamento': 'contínuo até o fim; arredondar para cima uma única vez por acerto',
        'dano_minimo': 'acerto direto válido não anulado causa no mínimo 1; imunidade, falha, esquiva e anulação total podem dar 0',
        'hp_perdido': 'mínimo entre o HP restante e o dano que atravessou proteções e escudos',
        'ordem': ['validar ação', 'snapshot do acerto', 'D_base', 'eficácia elemental (uma vez)',
                  'bônus e penalidades de dano (soma dos percentuais diferentes aplicáveis; não acumuláveis prevalecem)',
                  'anatomia e defesa (Guarda, Exposição/Ruptura, proteções)', 'acertos (máx. 2 convencionais)',
                  'arredondamento final', 'pós-acerto: HP perdido, efeitos, Pressão uma vez por ação'],
        'guarda': {'correta': 0.65, 'neutra': 1.0, 'errada': 1.10},
        'exposicao_bonus': 0.15, 'ruptura_janela_bonus': 0.25, 'exposicao_e_ruptura_acumulam': False,
        'teto_anatomico': 1.40, 'defesa_especial_reducao': 0.75,
        'canto_ofensivo_bonus': 0.12, 'canto_ofensivo_escopo': 'somente o primeiro acerto direto válido da ação',
        'canto_revezamento_reducao': 0.20, 'reducoes_mesma_classe': 'aplicar a maior, sem somar',
        'segundo_acerto_fracao_base': 0.5,
        'pressao': 'P = min(65, max(1, floor((18 + 200·L/HPmax)·F_regiao·G_guarda) + B_guarda)); L = HP retirado na ação; L=0 → 0',
        'pressao_com_canto_ofensivo': 'P = min(65, max(1, floor(((18 + 200·L/HPmax)·F_regiao + 6)·G_guarda) + B_guarda))',
        'exemplos': [
            {'hp_max': 200, 'poder': 40, 'ataque': 100, 'defesa': 100, 'dano': 20},
            {'hp_max': 200, 'poder': 80, 'ataque': 100, 'defesa': 100, 'dano': 40},
            {'hp_max': 350, 'poder': 80, 'ataque': 100, 'defesa': 100, 'dano': 70},
            {'hp_max': 200, 'poder': 80, 'ataque': 160, 'defesa': 80, 'dano': 65},
            {'hp_max': 200, 'poder': 80, 'ataque': 80, 'defesa': 160, 'dano': 25},
            {'hp_max': 200, 'poder': 180, 'ataque': 100, 'defesa': 100, 'dano': 90},
        ],
        'exemplos_modificadores_poder80_A_D_100_HP200': {
            'neutro': 40, 'guarda_correta': 26, 'guarda_errada': 44, 'exposicao': 46, 'ruptura': 50,
            'defesa_especial': 10, 'canto_ofensivo': 45},
        'substitui': 'combat_rules.dano_basico e combat_rules.dano_elemental (registros históricos preservados)',
        'vitalidade_v5_6_1': 'PENDENTE — HP efetivo e Resistência por Vitalidade dependem de parâmetro ainda não definido',
    }, 'Galetocraft_Dano_V5_6_Especificacao_Tecnica_2026-11-13.md (acervo, pacote 11)')

    regras['combate_universal'] = ({
        'energia': cr['energia'],
        'esquiva_universal': cr['esquiva_universal'],
        'golpes_multiplos': {**cr['golpes_multiplos'], 'chance_segundo_acerto': 'ver golpe_duplo (V2.2)'},
        'trocas': cr['trocas'],
        'desempate_velocidade': cr['desempate_velocidade'],
        'modificadores_temporarios': cr['modificadores_temporarios'],
        'equipes_3v3': cr['equipes_padrao_3v3'],
        'ordem_trocas_e_invocacoes_simultaneas': cr['ordem_trocas_e_invocacoes_simultaneas'],
        'hp': cr['hp'],
        'superados_nao_vigentes': {
            'dano_basico': 'substituído por dano_v5_6',
            'dano_elemental': 'substituído por dano_v5_6 + tipagem_dupla',
            'golpe_adicional_velocidade': 'substituído por golpe_duplo (V2.2)',
            'atributos': 'fórmula antiga (nível/100, IV 1–20) substituída pela progressao (nível 50); IV 1–40; integração de IV/EV/peso PENDENTE',
            'raridade_mitica_total_pontos': 'substituído pela escala da progressao (Mítico 550 no nível 50)',
        },
    }, 'combat_rules (histórico rev. 2, oficial): energia, esquiva_universal, golpes_multiplos, trocas, desempate_velocidade, modificadores_temporarios, equipes_padrao_3v3, ordem_trocas_e_invocacoes_simultaneas, hp')

    regras['estados_negativos'] = ({
        'regras_gerais': cr['estados_negativos'],
        'estados': {
            'Queimadura': cr['queimadura'], 'Envenenamento': cr['envenenamento'], 'Afogamento': cr['afogamento'],
            'Tonto': {**cr['tontura'], 'id_tecnico_antigo': 'tontura'}, 'Paralisia': cr['paralisia'],
        },
        'Sono': 'Citado só na captura (fator 1,55 na Rinha). Efeito em Rinha ainda não definido (PENDENTE).',
    }, 'combat_rules: estados_negativos, queimadura, envenenamento, afogamento, tontura (nome oficial Tonto), paralisia')

    regras['climas'] = ({k: amb[k] for k in ('chuva', 'ensolarado', 'ventania', 'tempestade_areia')},
                        'environmental_fields (histórico rev. 2, oficial, 09/11/2026)')
    regras['santuarios'] = ({'mecanica_universal': cr['santuarios_mecanica_universal'],
                             'santuario_raios': amb['santuario_raios'], 'santuario_raizes': amb['santuario_raizes']},
                            'combat_rules.santuarios_mecanica_universal + environmental_fields')
    regras['itens_segurados'] = ({'capacidade': cr['itens_segurados_capacidade_categorias'],
                                  'categorias_oficiais': cr['held_item_categories_official'],
                                  'catalogo': 'Os 20 itens de held_item_catalog são candidatos e não foram migrados.'},
                                 'combat_rules: itens_segurados_capacidade_categorias, held_item_categories_official')

    params = linhas('SELECT * FROM captura_parametros_modelo_v1256')[0]
    for k in ('raridade_fatores_json', 'raridade_xp_base_json'):
        params[k] = json.loads(params[k])
    regras['captura'] = ({
        'parametros': params,
        'modalidades': linhas('SELECT * FROM captura_formula_modalidade_v1256'),
        'fatores_estado_rinha': linhas('SELECT estado_negativo, fator_estado FROM captura_status_multiplicador_v1256'),
        'niveis_pena': linhas('SELECT nivel_pena, multiplicador_forca_vigente AS fator_forca, xp_evolucao, xp_acumulada, habilita_captura_lendarios FROM captura_pena_poder_niveis_v1258'),
        'lendarios': linhas('SELECT * FROM captura_pena_especializacao_lendarios_v1258')[0],
        'cooldown_falha_mundo': linhas('SELECT raridade, espera_segundos, escopo_da_espera, espera_compartilhada_entre_treinadores FROM captura_pena_cooldown_falha_mundo_v1259'),
    }, 'captura_* v1256, v1258 e v1259 (histórico rev. 2, oficial_homologado/oficial_vigente)')

    regras['experiencia'] = ({
        'sistema': linhas('SELECT * FROM cocorideo_xp_sistema_v1260')[0],
        'raridades': linhas('SELECT raridade, multiplicador FROM cocorideo_xp_raridades_v1260'),
        'modalidades': linhas('SELECT modalidade, multiplicador FROM cocorideo_xp_modalidades_v1260'),
        'distribuicao': linhas('SELECT * FROM cocorideo_xp_distribuicao_antifarm_v1260')[0],
    }, 'cocorideo_xp_* v1260 (histórico rev. 2, homologado 12/11/2026)')

    regras['treinador'] = ({
        'equipe_principal': linhas('SELECT * FROM treinador_equipe_principal_limite_v1254')[0],
        'reservas': linhas('SELECT * FROM treinador_reservas_roteamento_v1255')[0],
    }, 'treinador_* v1254 e v1255 (histórico rev. 2, oficial)')

    ops = [{'op': 'inserir', 'table': 'current_rules', 'key': {'id': rid},
            'values': {'payload_json': {**payload, 'migrado_em': DATA}, 'source_ref': fonte, 'status': 'OFICIAL_DOCUMENTAL'}}
           for rid, (payload, fonte) in regras.items()]
    pacote = {
        'expected_revision': a.revisao,
        'reason': ('Migração das regras oficiais de combate, captura, XP e treinador que só existiam em tabelas '
                   'históricas, e do dano V5.6 homologado em 13/11/2026, para current_rules. Nada é criado: '
                   'apenas consolidação com fonte; regras superadas ficam listadas como não vigentes.'),
        'evidence': {'historico': 'Galetocraft.sqlite rev. 2 (SHA-256 9dd2253d…5aa3c), tabelas citadas em cada source_ref',
                     'dano_v5_6': 'Galetocraft_Dano_V5_6_Especificacao_Tecnica_2026-11-13.md',
                     'motivo': 'docs/ANALISE_DESENVOLVIMENTO.md, fase 2 do roteiro'},
        'operations': ops,
    }
    json.dump(pacote, open(a.saida, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({'operacoes': len(ops), 'regras': list(regras)}, ensure_ascii=False))


if __name__ == '__main__':
    main()

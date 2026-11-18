"""Gera o pacote rev. 7: tira da regra `captura` dois campos que ficaram da proposta já superada.

1. `parametros.formula_forca_pena` dizia "F = 1 + 0.15 * (nivel_pena - 1)" (1,00 / 1,15 / 1,30 / 1,45 / 1,60),
   mas a tabela `niveis_pena` da própria regra tem os fatores do reforço homologado na Beta 1.2.58
   (1,00 / 1,30 / 1,65 / 2,05 / 2,50). A homologação final da Beta 1.2.59 confirma esses multiplicadores como vigentes.
2. `modalidades[mundo_direto].falha_permite_tentar_novamente_sem_cooldown` estava em 1 (retentativa imediata,
   v1241), mas a Beta 1.2.59 criou a espera após falha no mundo (20 s; 60 s para Lendário) e registra que o
   indicador de ausência de cooldown foi "corrigido para 0".

Nada é criado: a fórmula antiga fica registrada como superada, com a fonte.

Uso:
  python gerar_rev7_captura.py --saida docs/patches/rev7_captura_coerencia.json
"""
import argparse, copy, json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--revisao', type=int, default=6)
    a = ap.parse_args()
    regras = json.load(open(os.path.join(RAIZ, 'base', 'vigente', 'current_rules.json'), encoding='utf-8'))
    captura = next(r for r in regras if r['id'] == 'captura')
    p = copy.deepcopy(captura['payload_json'])
    par = p['parametros']
    fatores = [n['fator_forca'] for n in sorted(p['niveis_pena'], key=lambda n: n['nivel_pena'])]
    assert fatores == [1.0, 1.3, 1.65, 2.05, 2.5], fatores
    assert par['formula_forca_pena'] == 'F = 1 + 0.15 * (nivel_pena - 1)', par['formula_forca_pena']
    par['formula_forca_pena'] = 'F pelo nível da Pena (tabela niveis_pena, reforço v1258): 1.00 / 1.30 / 1.65 / 2.05 / 2.50'
    par['formula_forca_pena_superada'] = ('F = 1 + 0.15 * (nivel_pena - 1), da Proposta Final de 12/11 (1.00 / 1.15 / 1.30 / 1.45 / 1.60); '
                                          'substituída pelo reforço dos níveis homologado na Beta 1.2.58')
    par['incremento_forca_por_evolucao'] = None
    mundo = next(m for m in p['modalidades'] if m['modalidade'] == 'mundo_direto')
    assert mundo['falha_permite_tentar_novamente_sem_cooldown'] == 1
    mundo['falha_permite_tentar_novamente_sem_cooldown'] = 0
    mundo['espera_apos_falha'] = 'ver cooldown_falha_mundo (Beta 1.2.59): 20 s de Comum a Mítico, 60 s para Lendário'
    pacote = {
        'expected_revision': a.revisao,
        'reason': ('Coerência da regra captura: a fórmula da força da Pena e o indicador de retentativa sem espera no mundo '
                   'eram da proposta superada; valem os fatores do reforço v1258 e a espera da v1259, já presentes na própria regra.'),
        'evidence': {
            'fontes': [
                {'arquivo': 'Galetocraft_Homologacao_Final_Capturas_Cooldown_Beta_1.2.59_2026-11-12.md', 'pacote': 'Galetocraft_11_Acervo.zip',
                 'sha256': 'fb30d1fab99f51f4359a9f3f76f1646bbf947df3f2da5384901078486f83e82a',
                 'trechos': ['Pena: 5 níveis; multiplicadores 1,00× / 1,30× / 1,65× / 2,05× / 2,50×.',
                             'Tabela captura_formula_modalidade_v1256: indicador de ausência de cooldown no mundo corrigido para 0']},
                {'arquivo': 'Galetocraft_Homologacao_Pena_Reforco_Lendarios_Nivel_5_Beta_1.2.58_2026-11-12.md', 'pacote': 'Galetocraft_11_Acervo.zip',
                 'sha256': 'b8b7cf8f9bdc991dcbef68ece751277678bba7271dbf81b3716d49381ed8cefb'},
                {'arquivo': 'Galetocraft_Proposta_Final_Capturas_Progressao_Pena_Mais_Dificil_2026-11-12.md', 'pacote': 'Galetocraft_12_Acervo.zip',
                 'sha256': '35fac1ba755c5b0aaf7daafc3a40ea405f58126ecb5d23f62800ef546d52fd85',
                 'trecho': 'Fator da Pena: F = 1 + 0,15 × (nível_da_pena - 1) — proposta anterior ao reforço'},
            ],
            'campos': ['parametros.formula_forca_pena', 'parametros.formula_forca_pena_superada', 'parametros.incremento_forca_por_evolucao',
                       'modalidades[mundo_direto].falha_permite_tentar_novamente_sem_cooldown', 'modalidades[mundo_direto].espera_apos_falha'],
        },
        'operations': [{'op': 'atualizar', 'table': 'current_rules', 'key': {'id': 'captura'},
                        'values': {'payload_json': json.dumps(p, ensure_ascii=False)}}],
    }
    with open(a.saida, 'w', encoding='utf-8') as f:
        json.dump(pacote, f, ensure_ascii=False, indent=1)
    print('ok', a.saida)


if __name__ == '__main__':
    main()

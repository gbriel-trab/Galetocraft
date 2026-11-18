"""Propõe tabelas de aprendizado para as espécies sem dado no acervo (#013–#018 e #023), seguindo o padrão
medido nas 16 tabelas existentes (regra aprendizado, rev. 8). É PROPOSTA: só entra na base com aprovação do criador.

Padrão aplicado:
- golpes de origem nos marcos de 15 das 16 tabelas: posições 1 e 2 no nível 1, 3 no 17, 4 no 37 e 5 no 50;
- 10 aprendíveis por nível: do elemento da espécie (89% nas tabelas existentes), alternando os elementos nas
  espécies de tipagem dupla, metade dano e metade suporte (44% de suporte nas tabelas existentes); os golpes de
  dano são da categoria do ataque mais forte da espécie (94% nas tabelas existentes);
- marcos 5, 9, 13, 21, 25, 29, 33, 41, 44 e 47 por custo de Energia crescente (nas tabelas: E 21 → 35 → 49);
- os outros 15 aprendíveis ficam para o treinamento com os Mestres.

Uso: python ferramentas/propostas/propor_aprendizado.py [--json saida.json]
"""
import argparse, json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MARCOS_ORIGEM = {1: 1, 2: 1, 3: 17, 4: 37, 5: 50}
MARCOS_LIVRES = [5, 9, 13, 21, 25, 29, 33, 41, 44, 47]


def num(v):
    try:
        return float(str(v).split()[0].replace(',', '.'))
    except (TypeError, ValueError):
        return None


def propor(especie, moves, especies):
    elems = especies[especie]['elementos_json']
    meus = [m for m in moves if m['especie'] == especie]
    origem = sorted([m for m in meus if m['grupo'] == 'original'], key=lambda m: m['posicao'])
    aprend = [m for m in meus if m['grupo'] == 'aprendivel']
    chave = lambda m: (num(m['payload_json'].get('energia_efetiva_json')) or 0, num(m['payload_json'].get('poder_json')) or 0, m['nome'])

    def intercalar(lista):
        # alterna os elementos da espécie, cada fila em ordem de custo
        filas = [sorted([m for m in lista if m['payload_json'].get('elemento') == e], key=chave) for e in elems]
        out = []
        while any(filas):
            for f in filas:
                if f:
                    out.append(f.pop(0))
        return out

    mesmo = [m for m in aprend if m['payload_json'].get('elemento') in elems]
    at = especies[especie]['atributos_json']
    forte = 'fisico' if at['Ataque Físico'] >= at['Ataque Mágico'] else 'magico'
    cat = lambda m: m['payload_json'].get('categoria_normalizada')
    dano = intercalar([m for m in mesmo if cat(m) == forte]) + intercalar([m for m in mesmo if cat(m) not in ('suporte', forte)])
    suporte = intercalar([m for m in mesmo if m['payload_json'].get('categoria_normalizada') == 'suporte'])
    escolha = dano[:5] + suporte[:5]
    resto = dano[5:] + suporte[5:]
    while len(escolha) < 10 and resto:
        escolha.append(resto.pop(0))
    fora = sorted([m for m in aprend if m not in mesmo], key=chave)
    while len(escolha) < 10:
        escolha.append(fora.pop(0))
    escolha.sort(key=chave)
    linhas = [{'nome': m['nome'], 'metodo': 'nivel', 'nivel': MARCOS_ORIGEM[m['posicao']], 'origem': True} for m in origem]
    linhas += [{'nome': m['nome'], 'metodo': 'nivel', 'nivel': nv} for m, nv in zip(escolha, MARCOS_LIVRES)]
    linhas += [{'nome': m['nome'], 'metodo': 'treinamento'} for m in sorted([m for m in aprend if m not in escolha], key=chave)]
    assert len(linhas) == 30 and sum(1 for l in linhas if l['metodo'] == 'nivel') == 15
    return sorted(linhas, key=lambda l: (l['metodo'] != 'nivel', l.get('nivel', 0)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json')
    a = ap.parse_args()
    moves = json.load(open(os.path.join(RAIZ, 'base', 'vigente', 'current_moves.json'), encoding='utf-8'))
    especies = {e['numero']: e for e in json.load(open(os.path.join(RAIZ, 'base', 'vigente', 'current_species.json'), encoding='utf-8'))}
    mv = {(m['especie'], m['nome']): m['payload_json'] for m in moves}
    saida = {}
    for e in (13, 14, 15, 16, 17, 18, 23):
        t = propor(e, moves, especies)
        saida[str(e)] = t
        print(f"\n#{e:03d} {especies[e]['nome']} ({' + '.join(especies[e]['elementos_json'])})")
        for l in t:
            p = mv[(e, l['nome'])]
            info = f"{p.get('elemento')}, {p.get('categoria_normalizada')}, E{p.get('energia_efetiva_json')}, P{p.get('poder_json')}"
            print(f"  {('Nv ' + str(l['nivel'])) if l['metodo'] == 'nivel' else 'Mestres':>8}  {l['nome']}  [{info}]{' (origem)' if l.get('origem') else ''}")
    if a.json:
        json.dump(saida, open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()

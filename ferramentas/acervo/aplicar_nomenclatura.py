"""Aplica a nomenclatura oficial do Galetocraft a documentos de texto (.md, .txt, .json).

Troca os nomes antigos pelos oficiais definidos em nomenclatura_oficial.json
(somente as trocas com "aplicacao": "automatica"), preservando:
  - identificadores técnicos: caminhos e nomes de arquivo (vizinhos de / _ . - ou letras),
    texto entre crases, chaves JSON e formas totalmente em minúsculas (IDs como "tontura");
  - citações históricas que explicam a troca ("antiga RoosterTeca", "substitui Tricrina
    Infernal", "nome histórico Diário de Batalha", "jamais RoosterTeca"...).
Ajusta o artigo anterior quando o gênero muda (da RoosterTeca -> do Galetário,
a Tontura -> o Tonto) e o plural (as GalolpeTecas -> a Galolpédia).

Uso:
  python aplicar_nomenclatura.py --pasta PASTA [--saida PASTA_SAIDA] [--relatorio ARQ.json]
Sem --saida, altera os arquivos da pasta no lugar (use apenas em cópias derivadas,
nunca nos originais do acervo).
"""
import argparse, hashlib, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MARCAS_HISTORICAS = re.compile(
    r'(?:antig[ao]s?|anteriormente|anterior|substitui\w*|renomei\w*|jamais|nunca|nome antigo|'
    r'termo anterior|registro antigo|hist[óo]ric[ao]s?|ex-|antes)\W{0,4}$', re.I)
ARTIGOS_F_PARA_M = {'a': 'o', 'da': 'do', 'na': 'no', 'à': 'ao', 'pela': 'pelo', 'dessa': 'desse',
                    'desta': 'deste', 'nessa': 'nesse', 'nesta': 'neste', 'uma': 'um', 'sua': 'seu',
                    'essa': 'esse', 'esta': 'este', 'numa': 'num'}
ARTIGOS_PL_PARA_SG = {'as': 'a', 'das': 'da', 'nas': 'na', 'pelas': 'pela', 'às': 'à'}
TECNICO = set('/_.-\\`') | set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')


def carregar(dicionario):
    d = json.load(open(dicionario, encoding='utf-8'))
    pares = []
    for t in d['trocas']:
        if t.get('aplicacao') != 'automatica':
            continue
        muda_genero = t['genero']['antigo'] == 'f' and t['genero']['oficial'] == 'm'
        for antigo in t['antigos']:
            pares.append({'id': t['id'], 'antigo': antigo, 'oficial': t['oficial'],
                          'f_para_m': muda_genero, 'plural': antigo.endswith('s') and not t['oficial'].endswith('s')})
    return sorted(pares, key=lambda p: -len(p['antigo']))


def ajustar_case(modelo, novo):
    if modelo.isupper():
        return novo.upper()
    return novo


def ajustar_artigo(antes, f_para_m, plural):
    m = re.search(r'(\b\w+)(\s+(?:\*\*)?)$', antes)
    if not m:
        return antes
    palavra, esp = m.group(1), m.group(2)
    mapa = {}
    if plural:
        mapa.update(ARTIGOS_PL_PARA_SG)
    if f_para_m:
        mapa = {k: ARTIGOS_F_PARA_M.get(v, v) for k, v in mapa.items()} if plural else dict(ARTIGOS_F_PARA_M)
    nova = mapa.get(palavra.lower())
    if nova is None:
        return antes
    if palavra[0].isupper():
        nova = nova[0].upper() + nova[1:]
    return antes[:m.start(1)] + nova + esp


def aplicar_texto(texto, pares, eh_json):
    trocas, protegidas = [], 0
    for p in pares:
        rx = re.compile(re.escape(p['antigo']), re.I)
        saida, pos = [], 0
        for m in rx.finditer(texto):
            achado = m.group(0)
            ini, fim = m.start(), m.end()
            ant = texto[ini - 1] if ini else ''
            prox = texto[fim] if fim < len(texto) else ''
            prox2 = texto[fim + 1] if fim + 1 < len(texto) else ''
            linha_ini = texto.rfind('\n', 0, ini) + 1
            antes_linha = texto[linha_ini:ini]
            token_antes = re.search(r'(\S*)/$', antes_linha) if ant == '/' else None
            barra_textual = token_antes is not None and not re.search(r'[/_.\\]', token_antes.group(1))
            proteger = (
                achado.islower()
                or (ant in TECNICO and not barra_textual) or prox in (TECNICO - {'.', '-'})
                or (prox in '.-' and prox2.isalnum())
                or antes_linha.count('`') % 2 == 1
                or MARCAS_HISTORICAS.search(antes_linha[-40:]) is not None
                or (eh_json and re.match(r'"\s*:', texto[fim:fim + 4]))
            )
            if proteger:
                protegidas += 1
                continue
            novo = ajustar_case(achado, p['oficial'])
            trecho_antes = texto[pos:ini]
            if p['f_para_m'] or p['plural']:
                cauda = trecho_antes[-30:]
                trecho_antes = trecho_antes[:-30] + ajustar_artigo(cauda, p['f_para_m'], p['plural']) if len(trecho_antes) >= 30 \
                    else ajustar_artigo(trecho_antes, p['f_para_m'], p['plural'])
            saida += [trecho_antes, novo]
            pos = fim
            linha = texto.count('\n', 0, ini) + 1
            trocas.append({'troca': p['id'], 'antigo': achado, 'oficial': novo, 'linha': linha})
        saida.append(texto[pos:])
        texto = ''.join(saida)
    return texto, trocas, protegidas


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pasta', required=True)
    ap.add_argument('--saida')
    ap.add_argument('--dicionario', default=os.path.join(AQUI, 'nomenclatura_oficial.json'))
    ap.add_argument('--relatorio')
    a = ap.parse_args()
    pares = carregar(a.dicionario)
    ignorar = {'ERRATA_NIVEL_50.json', 'NOMENCLATURA_APLICADA.json'}
    arquivos = []
    for raiz, _, nomes in os.walk(a.pasta):
        for n in sorted(nomes):
            if n in ignorar or not n.lower().endswith(('.md', '.txt', '.json')):
                continue
            arquivos.append(os.path.relpath(os.path.join(raiz, n), a.pasta))
    relatorio = []
    for rel in sorted(arquivos):
        bruto = open(os.path.join(a.pasta, rel), 'rb').read()
        texto = bruto.decode('utf-8')
        eh_json = rel.lower().endswith('.json')
        novo, trocas, protegidas = aplicar_texto(texto, pares, eh_json)
        if eh_json:
            json.loads(novo)
        destino = os.path.join(a.saida or a.pasta, rel)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        dados = novo.encode('utf-8')
        if a.saida or dados != bruto:
            open(destino, 'wb').write(dados)
        if trocas or protegidas:
            relatorio.append({'arquivo': rel, 'sha256_antes': sha(bruto), 'sha256_depois': sha(dados),
                              'trocas': trocas, 'ocorrencias_preservadas': protegidas})
    resumo = {
        'dicionario': os.path.basename(a.dicionario),
        'arquivos_alterados': sum(1 for r in relatorio if r['trocas']),
        'trocas': sum(len(r['trocas']) for r in relatorio),
        'ocorrencias_preservadas': sum(r['ocorrencias_preservadas'] for r in relatorio),
        'arquivos': relatorio,
    }
    if a.relatorio:
        json.dump(resumo, open(a.relatorio, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in resumo.items() if k != 'arquivos'}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())

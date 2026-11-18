"""Corrige o rótulo antigo "atributos-base no nível 100" nas fichas oficiais do acervo.

Desde a Norma de Progressão Nível 50 V1 (13/11/2026), os atributos-base das
fichas são a referência do NÍVEL 50 (no nível 100 valem 1,5×). Várias fichas
oficiais anteriores ainda trazem o rótulo "nível 100" sobre os mesmos números.
A pendência R03 da base vigente registra isso como resolvido apenas na leitura.

O script NÃO altera os originais. Ele gera cópias corrigidas e um relatório:
  - troca o rótulo 100 -> 50 SOMENTE quando os números da ficha são iguais aos
    de current_species (ou os totais/faixas iguais aos da base vigente);
  - quando os números divergem ou não existem (registros parciais), mantém o
    rótulo e insere uma nota de errata com os valores vigentes;
  - em JSON, renomeia a chave (ex.: atributos_base_nivel100 -> atributos_base_nivel50)
    sob a mesma condição.
Projeções legítimas de nível 100 (ex.: "HP no nível 100: ceil(1,5 × HP)") não são tocadas.

Uso:
  python corrigir_rotulo_nivel50.py --dados DADOS_VIGENTES_CONSULTA.json \
      --acervo PASTA_EXTRAIDA [--acervo OUTRA_PASTA ...] --saida PASTA_SAIDA

--acervo é a pasta onde os ZIPs do Release foram extraídos (pode repetir).
A lista de fichas processadas fica em fichas_oficiais_nivel100.json.
"""
import argparse, hashlib, json, os, re, sys, unicodedata

ATRIBUTOS = ['HP', 'Ataque Físico', 'Defesa Física', 'Ataque Mágico', 'Defesa Mágica', 'Velocidade']
DATA = '18/11/2026'
NOTA_BASE = (f'Errata {DATA}: os atributos-base do Galetocraft usam o nível 50 como referência '
             '(Norma de Progressão Nível 50 V1).')

# Rótulos de texto. O grupo 1 é preservado; o "100" final vira "50".
ROTULOS = [
    ('atributos', re.compile(r'((?:seis )?atributos?[- ]base[^\n]{0,30}?n[íi]vel\s*)100\b', re.I)),
    ('atributos', re.compile(r'(seis atributos\s+n[íi]vel\s*)100\b', re.I)),
    ('total', re.compile(r'(base (?:no )?n[íi]vel\s*)100\b', re.I)),
    ('total', re.compile(r'(pontos-base \(n[íi]vel\s*)100\b', re.I)),
    ('atributos', re.compile(r'(ficha numérica — n[íi]vel\s*)100\b', re.I)),
    ('atributos', re.compile(r'(ficha-base de referência no n[íi]vel\s*)100\b', re.I)),
    ('escala', re.compile(r'(escala atual de raridades \(n[íi]vel\s*)100\b', re.I)),
]
CHAVES_JSON = {
    'atributos_base_nivel100': 'atributos_base_nivel50',
    'atributos_base_nivel_100': 'atributos_base_nivel_50',
    'base_stats_level_100': 'base_stats_level_50',
    'base_stats_level100': 'base_stats_level50',
}


def nfc(s):
    return unicodedata.normalize('NFC', s)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def carregar_vigente(caminho):
    dados = json.load(open(caminho, encoding='utf-8'))['dados']
    especies = {}
    for s in dados['current_species']:
        a = json.loads(s['atributos_json'])
        especies[s['numero']] = {'nome': s['nome'], 'valores': [a[k] for k in ATRIBUTOS], 'total': sum(a.values())}
    prog = next(r for r in dados['current_rules'] if r['id'] == 'progressao')
    faixas = {r['nome']: (r['min_l50'], r['referencia_l50'], r['max_l50'])
              for r in json.loads(prog['payload_json'])['norma_integral']['raridades']}
    return especies, faixas


def numero_do_arquivo(rel):
    m = re.search(r'(?:Galetario|RoosterTeca)_0*(\d{1,3})_', os.path.basename(rel))
    return int(m.group(1)) if m else None


def numero_do_contexto(texto, pos, padrao_arquivo):
    """Espécie da seção: último título markdown com '#NNN' antes da posição."""
    ult = None
    for m in re.finditer(r'^#{1,4}\s[^\n]*?#\s*0*(\d{1,3})\b', texto[:pos], re.M):
        ult = int(m.group(1))
    if ult is None:
        for m in re.finditer(r'^#{1,4}\s[^\n]*?#\s*0*(\d{1,3})\b|\*\*#0*(\d{1,3})\b|\|\s*#0*(\d{1,3})\s*\|', texto[:pos], re.M):
            ult = int(next(g for g in m.groups() if g))
    return ult if ult is not None else padrao_arquivo


def janela_seguinte(texto, fim):
    prox = re.search(r'\n#{1,4}\s', texto[fim:])
    limite = fim + (prox.start() if prox else 900)
    return texto[fim:min(limite, fim + 900)]


def janela_anterior(texto, inicio):
    ant = [m.end() for m in re.finditer(r'\n#{1,4}\s[^\n]*', texto[:inicio])]
    ini = ant[-1] if ant else max(0, inicio - 900)
    return texto[max(ini, inicio - 900):inicio]


def valores_verticais(janela):
    vals = []
    for at in ATRIBUTOS:
        m = re.search(re.escape(at) + r'[^0-9\n]{0,14}?(\d+)', janela, re.I)
        if not m:
            return None
        vals.append(int(m.group(1)))
    return vals


def valores_horizontais(janela):
    linhas = [l for l in janela.splitlines() if l.strip().startswith('|')]
    for i, l in enumerate(linhas):
        cel = [c.strip().strip('*') for c in l.strip().strip('|').split('|')]
        if all(a in cel for a in ATRIBUTOS):
            for v in linhas[i + 1:i + 3]:
                nums = [c.strip().strip('*') for c in v.strip().strip('|').split('|')]
                if all(re.fullmatch(r'\d+', n or '') for n in nums[:len(cel)]):
                    mapa = dict(zip(cel, nums))
                    return [int(mapa[a]) for a in ATRIBUTOS]
    return None


def nota_vigente(esp, num, md=True, sem_valores=False):
    motivo = ('Este registro não traz os números (registro parcial, superado pela ficha oficial completa)'
              if sem_valores else 'Os números deste trecho não conferem com a base vigente')
    if num in esp:
        e = esp[num]
        txt = (f'{NOTA_BASE} {motivo}; valores vigentes de #{num:03d} {e["nome"]} no nível 50: '
               + ' / '.join(f'{a} {v}' for a, v in zip(ATRIBUTOS, e['valores'])) + f' (total {e["total"]}).')
    else:
        txt = f'{NOTA_BASE} {motivo}; consulte a ficha oficial vigente.'
    return ('> **' + txt.replace(':', ':**', 1) if md else txt)


def corrigir_texto(texto, rel, esp, faixas):
    md = rel.lower().endswith('.md')
    num_arq = numero_do_arquivo(rel)
    acoes, trocas, notas, linhas_vistas = [], [], [], set()
    for tipo, rx in ROTULOS:
        for m in rx.finditer(texto):
            linha_ini = texto.rfind('\n', 0, m.start()) + 1
            if linha_ini in linhas_vistas:
                continue
            linhas_vistas.add(linha_ini)
            linha_fim = texto.find('\n', m.end())
            linha_fim = len(texto) if linha_fim < 0 else linha_fim
            linha = texto[linha_ini:linha_fim]
            num = numero_do_contexto(texto, m.start(), num_arq)
            reg = {'rotulo': linha.strip()[:120], 'tipo': tipo, 'especie': num}
            ok = False
            if tipo == 'escala':
                jan = janela_seguinte(texto, linha_fim)
                achadas = {r: tuple(int(x) for x in re.findall(r'\d+', l)[:3])
                           for l in jan.splitlines() for r in faixas if re.match(r'\|\s*' + r + r'\s*\|', l)}
                ok = bool(achadas) and all(achadas[r] == faixas[r] for r in achadas)
                reg['conferido'] = {r: list(v) for r, v in achadas.items()}
            elif tipo == 'total' and linha.lstrip().startswith('|'):
                cab = [c.strip() for c in linha.strip().strip('|').split('|')]
                col = next(i for i, c in enumerate(cab) if rx.search(c))
                linhas = texto[linha_fim:].split('\n')[2:]
                conf, ok = [], True
                for l in linhas:
                    if not l.strip().startswith('|'):
                        break
                    c = [x.strip() for x in l.strip().strip('|').split('|')]
                    n = re.search(r'\d+', c[0])
                    if n and int(n.group()) in esp:
                        v = int(re.search(r'\d+', c[col]).group())
                        conf.append([int(n.group()), v, esp[int(n.group())]['total']])
                        ok &= v == esp[int(n.group())]['total']
                ok = ok and bool(conf)
                reg['conferido'] = conf
                reg['especie'] = 'tabela'
            elif tipo == 'total':
                n = re.match(r'\D{0,12}(\d+)', texto[m.end():m.end() + 30])
                if n and num in esp:
                    reg['conferido'] = [int(n.group(1)), esp[num]['total']]
                    ok = int(n.group(1)) == esp[num]['total']
            else:
                jan = janela_seguinte(texto, m.end())
                vals = valores_horizontais(jan) or valores_verticais(jan)
                if vals is None:
                    jan = janela_anterior(texto, linha_ini)
                    vals = valores_horizontais(jan) or valores_verticais(jan)
                if vals is not None and num in esp:
                    reg['conferido'] = [vals, esp[num]['valores']]
                    ok = vals == esp[num]['valores']
            if ok:
                trocas.append((m.start(1) + len(m.group(1)), m.end(), '50'))
                reg['acao'] = 'rotulo_trocado_100_para_50'
            else:
                notas.append((linha_fim, nota_vigente(esp, num, md, sem_valores='conferido' not in reg)))
                reg['acao'] = 'nota_de_errata_inserida'
            acoes.append(reg)
    edicoes = [(i, f, s) for i, f, s in trocas] + [(p, p, '\n\n' + n if md else '\n' + n) for p, n in notas]
    for i, f, s in sorted(edicoes, key=lambda x: x[0], reverse=True):
        texto = texto[:i] + s + texto[f:]
    return texto, acoes


def corrigir_json(texto, rel, esp):
    dados = json.loads(texto)
    num_arq = numero_do_arquivo(rel)
    decisoes = []

    def andar(o, num):
        if isinstance(o, dict):
            n = o.get('numero') if isinstance(o.get('numero'), int) else num
            for k, v in o.items():
                if k in CHAVES_JSON and isinstance(v, dict):
                    vals = [v.get(a) for a in ATRIBUTOS]
                    ok = n in esp and vals == esp[n]['valores'] and v.get('total', esp[n]['total']) == esp[n]['total']
                    decisoes.append({'chave': k, 'especie': n, 'conferido': [vals, esp.get(n, {}).get('valores')],
                                     'acao': 'chave_renomeada_para_' + CHAVES_JSON[k] if ok else 'nota_de_errata_inserida'})
                andar(v, n)
        elif isinstance(o, list):
            for v in o:
                andar(v, num)

    andar(dados, num_arq)
    if all(d['acao'].startswith('chave_renomeada') for d in decisoes):
        # Preserva a formatação original: renomeia as chaves no texto, na mesma ordem do JSON.
        partes, pos = [], 0
        alvos = iter(decisoes)
        rx = re.compile(r'"(' + '|'.join(map(re.escape, CHAVES_JSON)) + r')"(\s*:)')
        for m in rx.finditer(texto):
            d = next(alvos)
            assert d['chave'] == m.group(1)
            partes += [texto[pos:m.start()], f'"{CHAVES_JSON[m.group(1)]}"{m.group(2)}']
            pos = m.end()
        novo = ''.join(partes) + texto[pos:]
        json.loads(novo)
        return novo, decisoes

    def anotar(o, num):
        if isinstance(o, dict):
            n = o.get('numero') if isinstance(o.get('numero'), int) else num
            for k in list(o):
                if k in CHAVES_JSON and isinstance(o[k], dict):
                    vals = [o[k].get(a) for a in ATRIBUTOS]
                    if n in esp and vals == esp[n]['valores']:
                        o[CHAVES_JSON[k]] = o.pop(k)
                    else:
                        o['errata_nivel50'] = nota_vigente(esp, n, md=False)
                else:
                    anotar(o[k], n)
        elif isinstance(o, list):
            for v in o:
                anotar(v, num)

    anotar(dados, num_arq)
    return json.dumps(dados, ensure_ascii=False, indent=2) + '\n', decisoes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dados', required=True)
    ap.add_argument('--acervo', action='append', required=True)
    ap.add_argument('--saida', required=True)
    ap.add_argument('--lista', default=os.path.join(os.path.dirname(__file__), 'fichas_oficiais_nivel100.json'))
    a = ap.parse_args()
    esp, faixas = carregar_vigente(a.dados)
    lista = json.load(open(a.lista, encoding='utf-8'))
    relatorio, por_hash = [], {}
    for rel in lista:
        origem = next((os.path.join(r, rel) for r in a.acervo if os.path.isfile(os.path.join(r, rel))), None)
        if origem is None:
            relatorio.append({'arquivo': rel, 'acao': 'nao_encontrado'})
            continue
        bruto = open(origem, 'rb').read()
        h = sha(bruto)
        if h in por_hash:
            por_hash[h]['copias_identicas'].append(rel)
            continue
        texto = nfc(bruto.decode('utf-8'))
        if rel.lower().endswith('.json'):
            novo, acoes = corrigir_json(texto, rel, esp)
        else:
            novo, acoes = corrigir_texto(texto, rel, esp, faixas)
        destino = os.path.join(a.saida, rel)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        dados_novos = novo.encode('utf-8')
        open(destino, 'wb').write(dados_novos)
        item = {'arquivo': rel, 'sha256_original': h, 'sha256_corrigido': sha(dados_novos),
                'copias_identicas': [], 'correcoes': acoes}
        por_hash[h] = item
        relatorio.append(item)
    resumo = {
        'data': DATA,
        'regra': 'Norma de Progressão Nível 50 V1: atributos-base referenciados no nível 50.',
        'originais_preservados': True,
        'arquivos_unicos': len(por_hash),
        'caminhos_cobertos': sum(1 + len(i['copias_identicas']) for i in por_hash.values()),
        'rotulos_trocados': sum(1 for i in por_hash.values() for c in i['correcoes'] if 'nota' not in c['acao']),
        'notas_inseridas': sum(1 for i in por_hash.values() for c in i['correcoes'] if 'nota' in c['acao']),
        'arquivos': relatorio,
    }
    json.dump(resumo, open(os.path.join(a.saida, 'ERRATA_NIVEL_50.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in resumo.items() if k != 'arquivos'}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())

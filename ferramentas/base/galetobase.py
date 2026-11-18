"""Galetocraft — ferramenta da base vigente mantida no repositório.

A camada vigente (tabelas current_*) fica em base/vigente/*.json, versionada pelo git. As artes
ficam em base/artes/ e as fontes em base/fontes/. As tabelas históricas continuam no SQLite da
revisão 2 publicado no Release acervo-documental-2026-11-17. O comando "montar" junta as duas
partes num Galetocraft.sqlite completo.

Comandos:
  exportar  --sqlite BASE.sqlite                 importa a camada current_* de um SQLite para base/
  validar                                       confere integridade, chaves, contagens e hashes
  atualizar --pacote PACOTE.json                altera registros existentes (formato do Atualizar_Galetocraft.py)
  migrar    --pacote MIGRACAO.json              insere/altera registros em qualquer tabela current_* (migração validada)
  montar    --historico REV2.sqlite --saida X   gera o SQLite completo (histórico + camada vigente do repositório)
  ficha     --especie N                         mostra a ficha vigente de uma espécie

Toda alteração exige expected_revision, reason e evidence. Ela incrementa a revisão e grava em current_journal.
"""
import argparse, datetime, hashlib, json, os, shutil, sqlite3, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(RAIZ, 'base')
VIGENTE = os.path.join(BASE, 'vigente')

TABELAS = {
    'current_meta': {'chave': ['key'], 'json': ['value_json']},
    'current_species': {'chave': ['numero'], 'json': ['elementos_json', 'atributos_json', 'passiva_json']},
    'current_moves': {'chave': ['especie', 'grupo', 'posicao'], 'json': ['payload_json']},
    'current_rules': {'chave': ['id'], 'json': ['payload_json']},
    'current_issues': {'chave': ['id'], 'json': []},
    'current_heranca': {'chave': ['especie'], 'json': []},
    'current_galeria': {'chave': ['numero'], 'json': []},
    'current_art': {'chave': ['numero'], 'json': [], 'blob': ('content', 'artes')},
    'current_sources': {'chave': ['id'], 'json': [], 'blob': ('content', 'fontes')},
    'current_journal': {'chave': ['revision'], 'json': ['source_hashes_json', 'changes_json']},
}
# Tabelas que o "atualizar" pode alterar (mesmas do Atualizar_Galetocraft.py oficial).
ATUALIZAVEIS = ['current_species', 'current_rules', 'current_moves', 'current_issues', 'current_heranca', 'current_galeria']
ATRIBUTOS = ['HP', 'Ataque Físico', 'Defesa Física', 'Ataque Mágico', 'Defesa Mágica', 'Velocidade']


def sha(b):
    return hashlib.sha256(b).hexdigest()


def caminho(t):
    return os.path.join(VIGENTE, t + '.json')


def ler(t):
    return json.load(open(caminho(t), encoding='utf-8'))


def gravar(t, linhas):
    chave = TABELAS[t]['chave']
    linhas = sorted(linhas, key=lambda r: [r[k] for k in chave])
    with open(caminho(t), 'w', encoding='utf-8') as f:
        json.dump(linhas, f, ensure_ascii=False, indent=1)
        f.write('\n')


def carregar_tudo():
    return {t: ler(t) for t in TABELAS}


def chave_de(t, linha):
    return tuple(linha[k] for k in TABELAS[t]['chave'])


# ---------------------------------------------------------------- exportar
def exportar(sqlite_path):
    con = sqlite3.connect(f'file:{sqlite_path}?mode=ro', uri=True)
    con.row_factory = sqlite3.Row
    os.makedirs(VIGENTE, exist_ok=True)
    for t, cfg in TABELAS.items():
        linhas = []
        for r in con.execute(f'SELECT * FROM "{t}"'):
            d = dict(r)
            for c in cfg['json']:
                d[c] = json.loads(d[c])
            if 'blob' in cfg:
                col, pasta = cfg['blob']
                dados = d.pop(col)
                dados = dados if isinstance(dados, bytes) else dados.encode('utf-8')
                destino = os.path.join(BASE, pasta, d['filename'])
                os.makedirs(os.path.dirname(destino), exist_ok=True)
                open(destino, 'wb').write(dados)
                d['arquivo'] = os.path.relpath(destino, BASE).replace(os.sep, '/')
                if sha(dados) != d['sha256']:
                    raise SystemExit(f'{t} {d["filename"]}: SHA-256 do conteúdo não confere')
            linhas.append(d)
        gravar(t, linhas)
        print(f'{t}: {len(linhas)}')


# ---------------------------------------------------------------- validar
def validar(dados=None, verbose=True):
    d = dados or carregar_tudo()
    erros = []
    esp = {r['numero']: r for r in d['current_species']}
    for t, linhas in d.items():
        vistos = set()
        for r in linhas:
            k = chave_de(t, r)
            if k in vistos:
                erros.append(f'{t}: chave repetida {k}')
            vistos.add(k)
    for n, s in esp.items():
        a = s['atributos_json']
        if set(a) != set(ATRIBUTOS) or any(not isinstance(v, (int, float)) or v <= 0 for v in a.values()):
            erros.append(f'#{n}: atributos incompletos ou inválidos')
        if not s['elementos_json']:
            erros.append(f'#{n}: sem elementos')
        if s['base_nivel'] != 50:
            erros.append(f'#{n}: base_nivel diferente de 50')
    contagem = {}
    for m in d['current_moves']:
        if m['especie'] not in esp:
            erros.append(f'golpe de espécie inexistente: {m["especie"]}')
        contagem.setdefault(m['especie'], {}).setdefault(m['grupo'], []).append(m['posicao'])
    for n in esp:
        c = contagem.get(n, {})
        if sorted(c.get('original', [])) != [1, 2, 3, 4, 5] or sorted(c.get('aprendivel', [])) != list(range(1, 26)):
            erros.append(f'#{n}: repertório diferente de 5 originais + 25 aprendíveis')
    for t, col in [('current_heranca', 'especie'), ('current_galeria', 'numero'), ('current_art', 'numero')]:
        for r in d[t]:
            if r[col] not in esp:
                erros.append(f'{t}: espécie inexistente {r[col]}')
    for g in d['current_galeria']:
        if g['nome'] != esp.get(g['numero'], {}).get('nome'):
            erros.append(f'current_galeria #{g["numero"]}: nome diferente do Galetário')
    for t in ('current_art', 'current_sources'):
        for r in d[t]:
            p = os.path.join(BASE, r['arquivo'])
            if not os.path.isfile(p):
                erros.append(f'{t}: arquivo ausente {r["arquivo"]}')
            elif sha(open(p, 'rb').read()) != r['sha256']:
                erros.append(f'{t}: SHA-256 não confere em {r["arquivo"]}')
    meta = {m['key']: m['value_json'] for m in d['current_meta']}
    revs = sorted(j['revision'] for j in d['current_journal'])
    if revs != list(range(1, len(revs) + 1)):
        erros.append(f'current_journal com revisões fora de sequência: {revs}')
    if meta.get('revision') != (revs[-1] if revs else None):
        erros.append(f'revision em current_meta ({meta.get("revision")}) diferente da última do journal ({revs[-1] if revs else None})')
    if verbose:
        resumo = {t: len(v) for t, v in d.items()}
        print(json.dumps({'revisao': meta.get('revision'), 'contagens': resumo, 'erros': erros}, ensure_ascii=False, indent=1))
    return erros


# ---------------------------------------------------------------- alterações
def _aplicar(pacote, modo):
    for campo in ('expected_revision', 'reason', 'evidence', 'operations'):
        if pacote.get(campo) in (None, '', []):
            raise SystemExit('Obrigatório: ' + campo)
    d = carregar_tudo()
    meta = {m['key']: m for m in d['current_meta']}
    rev = meta['revision']['value_json']
    if rev != pacote['expected_revision']:
        raise SystemExit(f'Conflito: a base está na revisão {rev}, o pacote espera {pacote["expected_revision"]}. Releia e reconcilie.')
    log = []
    for op in pacote['operations']:
        t = op['table']
        if t not in TABELAS or t == 'current_journal':
            raise SystemExit(f'Tabela não permitida: {t}')
        if modo == 'atualizar' and t not in ATUALIZAVEIS:
            raise SystemExit(f'"atualizar" não altera {t}; use "migrar"')
        cfg = TABELAS[t]
        acao = op.get('op', 'atualizar')
        if modo == 'atualizar' and acao != 'atualizar':
            raise SystemExit('"atualizar" só altera registros existentes; use "migrar" para inserir')
        chave = op['key']
        if sorted(chave) != sorted(cfg['chave']):
            raise SystemExit(f'Chave inválida para {t}: {chave}')
        alvo = [r for r in d[t] if all(r[k] == chave[k] for k in cfg['chave'])]
        valores = dict(op['values'])
        if modo == 'atualizar':
            # Formato do Atualizar_Galetocraft.py oficial: colunas JSON chegam como texto JSON.
            for c in cfg['json']:
                if c in valores and isinstance(valores[c], str):
                    valores[c] = json.loads(valores[c])
        # Em "migrar", os valores das colunas JSON já vêm decodificados (objeto, lista, número ou texto).
        if 'blob' in cfg and 'arquivo' in valores:
            p = os.path.join(BASE, valores['arquivo'])
            valores['sha256'] = valores.get('sha256') or sha(open(p, 'rb').read())
            if sha(open(p, 'rb').read()) != valores['sha256']:
                raise SystemExit(f'SHA-256 não confere: {valores["arquivo"]}')
        if acao == 'atualizar':
            if not alvo:
                raise SystemExit(f'Registro inexistente em {t}: {chave}. Registro novo exige "migrar".')
            colunas = set(alvo[0])
            if set(valores) - colunas or set(valores) & set(cfg['chave']):
                raise SystemExit(f'Campos inválidos para {t}: {sorted(set(valores) - colunas)}')
            antes = {k: alvo[0][k] for k in valores}
            alvo[0].update(valores)
            log.append({'table': t, 'key': chave, 'before': antes, 'changes': valores})
        elif acao == 'inserir':
            if alvo:
                raise SystemExit(f'Registro já existe em {t}: {chave}')
            if d[t]:
                faltando = set(d[t][0]) - set(valores) - set(chave)
                if faltando:
                    raise SystemExit(f'Campos ausentes para {t}: {sorted(faltando)}')
            d[t].append({**chave, **valores})
            log.append({'table': t, 'key': chave, 'inserted': valores})
        else:
            raise SystemExit(f'Operação desconhecida: {acao}')
    erros = validar(d, verbose=False)
    if erros:
        raise SystemExit('Pacote rejeitado; a base ficaria inválida:\n- ' + '\n- '.join(erros))
    nova = rev + 1
    meta['revision']['value_json'] = nova
    d['current_journal'].append({'revision': nova, 'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                 'reason': pacote['reason'], 'source_hashes_json': pacote['evidence'], 'changes_json': log})
    if validar(d, verbose=False):
        raise SystemExit('Falha interna ao registrar a revisão')
    for t in TABELAS:
        gravar(t, d[t])
    print(json.dumps({'revisao': nova, 'operacoes': len(log)}, ensure_ascii=False))


# ---------------------------------------------------------------- montar
def montar(historico, saida):
    if os.path.abspath(historico) == os.path.abspath(saida):
        raise SystemExit('A saída precisa ser outro arquivo')
    shutil.copyfile(historico, saida)
    d = carregar_tudo()
    con = sqlite3.connect(saida)
    con.execute('PRAGMA foreign_keys=OFF')
    with con:
        for t, cfg in TABELAS.items():
            colunas = [r[1] for r in con.execute(f'PRAGMA table_info("{t}")')]
            con.execute(f'DELETE FROM "{t}"')
            for r in d[t]:
                linha = dict(r)
                for c in cfg['json']:
                    linha[c] = json.dumps(linha[c], ensure_ascii=False)
                if 'blob' in cfg:
                    linha[cfg['blob'][0]] = open(os.path.join(BASE, linha.pop('arquivo')), 'rb').read()
                con.execute(f'INSERT INTO "{t}" ({",".join(chr(34) + c + chr(34) for c in colunas)}) VALUES ({",".join("?" * len(colunas))})',
                            [linha.get(c) for c in colunas])
    con.execute('PRAGMA foreign_keys=ON')
    ok = con.execute('PRAGMA integrity_check').fetchone()[0]
    fk = con.execute('PRAGMA foreign_key_check').fetchall()
    con.execute('VACUUM')
    con.close()
    if ok != 'ok' or fk:
        raise SystemExit(f'SQLite montado inválido: integrity={ok} fk={fk[:5]}')
    print(json.dumps({'saida': saida, 'sha256': sha(open(saida, 'rb').read()), 'integrity_check': ok}, ensure_ascii=False))


# ---------------------------------------------------------------- ficha
def ficha(n):
    d = carregar_tudo()
    s = next(r for r in d['current_species'] if r['numero'] == n)
    golpes = sorted((m for m in d['current_moves'] if m['especie'] == n), key=lambda m: (m['grupo'] != 'original', m['posicao']))
    print(json.dumps({'especie': s, 'galeria': next((g for g in d['current_galeria'] if g['numero'] == n), None),
                      'heranca': next((h for h in d['current_heranca'] if h['especie'] == n), None),
                      'arte': next((a for a in d['current_art'] if a['numero'] == n), None),
                      'golpes': [{'grupo': m['grupo'], 'posicao': m['posicao'], 'nome': m['nome'],
                                  'elemento': m['payload_json'].get('elemento'),
                                  'categoria': m['payload_json'].get('categoria_normalizada'),
                                  'poder': m['payload_json'].get('poder_json'), 'energia': m['payload_json'].get('energia_efetiva_json'),
                                  'efeito': m['payload_json'].get('efeito_canonico_para_integracao')} for m in golpes]},
                     ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('exportar').add_argument('--sqlite', required=True)
    sub.add_parser('validar')
    sub.add_parser('atualizar').add_argument('--pacote', required=True)
    sub.add_parser('migrar').add_argument('--pacote', required=True)
    m = sub.add_parser('montar')
    m.add_argument('--historico', required=True)
    m.add_argument('--saida', required=True)
    sub.add_parser('ficha').add_argument('--especie', type=int, required=True)
    a = ap.parse_args()
    if a.cmd == 'exportar':
        exportar(a.sqlite)
    elif a.cmd == 'validar':
        sys.exit(1 if validar() else 0)
    elif a.cmd in ('atualizar', 'migrar'):
        _aplicar(json.load(open(a.pacote, encoding='utf-8')), a.cmd)
    elif a.cmd == 'montar':
        montar(a.historico, a.saida)
    elif a.cmd == 'ficha':
        ficha(a.especie)


if __name__ == '__main__':
    main()

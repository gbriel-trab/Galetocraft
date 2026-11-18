"""Gera o pacote de conhecimento para o Projeto GALETOCRAFT no app do Claude (claude.ai).

O Projeto do claude.ai não lê o repositório: ele usa arquivos anexados como conhecimento. Este gerador monta, a partir da
base vigente e da documentação, arquivos de texto prontos para anexar, mais cópias reduzidas das artes para consulta.
Rode de novo depois de cada revisão da base e troque os arquivos no Projeto.

Uso: python ferramentas/projeto/gerar_pacote_projeto.py --saida <pasta>
"""
import argparse, json, os, shutil, zipfile
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ATRIBUTOS = ['HP', 'Ataque Físico', 'Defesa Física', 'Ataque Mágico', 'Defesa Mágica', 'Velocidade']
CAT = {'fisico': 'físico', 'magico': 'mágico', 'suporte': 'suporte'}


def vig(nome):
    return json.load(open(os.path.join(RAIZ, 'base', 'vigente', f'current_{nome}.json'), encoding='utf-8'))


def ler(rel):
    return open(os.path.join(RAIZ, rel), encoding='utf-8').read()


def limpo(v):
    return '—' if v in (None, 'null', 'None', '') else str(v).strip('"')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    out = a.saida
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, 'artes_reduzidas'))
    meta = {m['key']: m['value_json'] for m in vig('meta')}
    rev = meta['revision']
    especies = vig('species')
    moves = vig('moves')
    regras = {r['id']: r for r in vig('rules')}
    heranca = {int(h['especie']): h['golpe'] for h in vig('heranca')}
    galeria = {int(g['numero']): g for g in vig('galeria')}
    apr = regras['aprendizado']['payload_json']['tabelas']
    hoje = date.today().isoformat()
    cab = f'> Pacote do Projeto GALETOCRAFT — base vigente revisão {rev}, gerado em {hoje} a partir do repositório gbriel-trab/Galetocraft.\n'

    # 01 — conhecimento consolidado
    open(os.path.join(out, '01_Conhecimento_Galetocraft.md'), 'w', encoding='utf-8').write(
        cab + '\n' + ler('docs/CONHECIMENTO_GALETOCRAFT.md'))

    # 02 — Galetário: fichas das 23 espécies
    L = [f'# Galetário — fichas das {len(especies)} espécies (atributos no nível 50)\n', cab,
         'Ordem dos atributos: HP / Atq. Físico / Def. Física / Atq. Mágico / Def. Mágica / Velocidade. '
         'Golpes: "Nv N" = aprendido por nível; "Mestres" = aprendido por treinamento com os Mestres Elementais. '
         'Os efeitos dos golpes estão no arquivo 03 (Galolpédia).\n']
    por_esp = {}
    for m in moves:
        por_esp.setdefault(int(m['especie']), []).append(m)
    for e in sorted(especies, key=lambda x: int(x['numero'])):
        n = int(e['numero'])
        at = e['atributos_json']
        tot = sum(at[k] for k in ATRIBUTOS)
        g = galeria.get(n, {})
        alas = ' / '.join(x for x in (g.get('ala_principal'), g.get('ala_secundaria')) if x) or 'não reproduz'
        machos = g.get('probabilidade_macho')
        pas = e['passiva_json']
        nome_pas = pas.get('nome') or pas.get('name') or pas.get('nome_de_catalogo') if isinstance(pas, dict) else str(pas)
        L.append(f"\n## #{n:03d} {e['nome']}\n")
        L.append(f"- **Raridade:** {e['raridade']} · **Elementos:** {' + '.join(e['elementos_json'])} · **Peso natural:** {e['peso_natural_kg']} kg")
        L.append(f"- **Atributos:** {'/'.join(str(at[k]) for k in ATRIBUTOS)} (total {tot})")
        L.append(f"- **Galeria:** alas {alas}; machos {'—' if machos is None else f'{round(float(machos)*100)}%'}")
        L.append(f"- **Golpe hereditário (Herança de Bico):** {heranca.get(n, 'nenhum')}")
        L.append(f"- **Passiva — {nome_pas}:** `{json.dumps(pas, ensure_ascii=False)}`")
        metodo = {x['nome']: x for x in apr.get(str(n), [])}
        L.append('\n| Golpe | Origem | Aprende | Elemento | Categoria | Energia | Poder |\n|---|---|---|---|---|---:|---|')
        def chave(m):
            x = metodo.get(m['nome'], {})
            return (x.get('metodo') != 'nivel', x.get('nivel') or 0, m['nome'])
        for m in sorted(por_esp.get(n, []), key=chave):
            p = m['payload_json']
            x = metodo.get(m['nome'], {})
            aprende = f"Nv {x['nivel']}" if x.get('metodo') == 'nivel' else ('Mestres' if x else '—')
            L.append(f"| {m['nome']} | {'origem' if m['grupo'] == 'original' else 'aprendível'} | {aprende} | {limpo(p.get('elemento'))} | "
                     f"{CAT.get(p.get('categoria_normalizada'), limpo(p.get('categoria_normalizada')))} | {limpo(p.get('energia_efetiva_json'))} | {limpo(p.get('poder_json'))} |")
    open(os.path.join(out, '02_Galetario_23_Fichas.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

    # 03 — Galolpédia: golpes distintos com efeito e quem aprende
    golpes = {}
    for m in moves:
        golpes.setdefault(m['nome'], {'p': m['payload_json'], 'esp': []})['esp'].append(int(m['especie']))
    nomes_esp = {int(e['numero']): e['nome'] for e in especies}
    L = [f'# Galolpédia — {len(golpes)} golpes do repertório vigente\n', cab]
    for nome in sorted(golpes, key=lambda s: s.lower()):
        p = golpes[nome]['p']
        quem = ', '.join(f"#{n:03d} {nomes_esp[n]}" for n in sorted(set(golpes[nome]['esp'])))
        L.append(f"\n### {nome}\n- {limpo(p.get('elemento'))} · {CAT.get(p.get('categoria_normalizada'), limpo(p.get('categoria_normalizada')))} · "
                 f"Energia {limpo(p.get('energia_efetiva_json'))} · Poder {limpo(p.get('poder_json'))}"
                 f"{' · ID ' + p['id_canonico'] if p.get('id_canonico') else ''}\n- **Efeito:** {limpo(p.get('efeito_canonico_para_integracao'))}\n- **Espécies:** {quem}")
    open(os.path.join(out, '03_Galolpedia_Golpes.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

    # 04 — regras vigentes (texto integral de current_rules)
    L = [f'# Regras vigentes ({len(regras)} regras de current_rules)\n', cab,
         'Cada regra traz o conteúdo integral da base (JSON). Em conflito com qualquer resumo, vale este conteúdo.\n']
    for rid in sorted(regras):
        r = regras[rid]
        L.append(f"\n## {rid}\n- status: {r.get('status')} · fonte: {r.get('source_ref')}\n\n```json\n"
                 + json.dumps(r['payload_json'], ensure_ascii=False, indent=1) + '\n```')
    open(os.path.join(out, '04_Regras_Vigentes.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

    # 05 — decisões, pendências, revisões e desenvolvimento
    L = ['# Decisões, pendências, revisões e desenvolvimento\n', cab]
    L.append('\n## Revisões da base (current_journal)\n\n| Rev. | Data | Motivo |\n|---:|---|---|')
    for j in sorted(vig('journal'), key=lambda x: int(x['revision'])):
        L.append(f"| {j['revision']} | {str(j.get('created_at', ''))[:10]} | {str(j.get('reason', '')).replace('|', '/')} |")
    L.append('\n## Pendências (current_issues)\n\n| Id | Assunto | Status | Evidência | Próximo passo |\n|---|---|---|---|---|')
    for i in vig('issues'):
        L.append('| ' + ' | '.join(str(i.get(k) or '').replace('|', '/') for k in ('id', 'assunto', 'status', 'evidencia', 'proximo_passo')) + ' |')
    for titulo, rel in [('Governança da base (base/LEIA_ME.md)', 'base/LEIA_ME.md'),
                        ('Progresso do desenvolvimento do mod', 'docs/PROGRESSO_DESENVOLVIMENTO.md'),
                        ('Propostas das pendências e decisões de 18/11', 'docs/propostas/PROPOSTAS_PENDENCIAS_2026-11-18.md'),
                        ('Análise de desenvolvimento (roteiro)', 'docs/ANALISE_DESENVOLVIMENTO.md'),
                        ('Auditoria de incoerências', 'docs/AUDITORIA_INCOERENCIAS.md'),
                        ('Nomenclatura oficial', 'docs/NOMENCLATURA_OFICIAL.md'),
                        ('Errata do nível 50', 'docs/ERRATA_NIVEL_50.md'),
                        ('Como jogar e testar o mod (galetocraft/LEIAME.md)', 'galetocraft/LEIAME.md')]:
        texto = ler(rel)
        texto = '\n'.join(('#' + l) if l.startswith('#') else l for l in texto.split('\n'))   # rebaixa os títulos
        L.append(f'\n---\n\n# {titulo}\n\n_Arquivo de origem: `{rel}`_\n\n{texto}')
    open(os.path.join(out, '05_Decisoes_Progresso_e_Historico.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

    # artes reduzidas (cópias de consulta; os originais e o SHA-256 ficam em base/artes e current_art)
    from PIL import Image
    artes = []
    for art in sorted(vig('art'), key=lambda x: int(x['numero'])):
        n = int(art['numero'])
        img = Image.open(os.path.join(RAIZ, 'base', art['arquivo'])).convert('RGB')
        img.thumbnail((1400, 1400))
        nome = f"{n:03d}_{nomes_esp[n]}.jpg"
        img.save(os.path.join(out, 'artes_reduzidas', nome), quality=82)
        artes.append((n, nomes_esp[n], art['filename'], art['sha256']))

    # 00 — leia primeiro + instruções do Projeto
    arquivos = sorted(f for f in os.listdir(out) if f.endswith('.md'))
    tam = {f: os.path.getsize(os.path.join(out, f)) for f in arquivos}
    L = [f'# GALETOCRAFT — leia primeiro\n', cab,
         '\n## Como montar o Projeto no app do Claude\n',
         '1. Abra o Projeto GALETOCRAFT no app do Claude e toque em **Conhecimento do projeto** (Project knowledge) → **Adicionar** → **Carregar arquivo**.',
         '2. Anexe os arquivos de texto deste pacote (00 a 05). As artes da pasta `artes_reduzidas` são opcionais: anexe se quiser que o Claude do Projeto veja as criaturas.',
         '3. Em **Instruções do projeto** (Set project instructions), cole o texto da seção abaixo.',
         '4. Quando a base mudar (nova revisão), gere o pacote de novo e troque os arquivos.\n',
         '| Arquivo | Conteúdo | Tamanho |\n|---|---|---:|']
    descr = {
        '00_LEIA_PRIMEIRO.md': 'este guia e as instruções do Projeto',
        '01_Conhecimento_Galetocraft.md': 'resumo de todo o projeto: espécies, regras, sistemas, pendências, código e acervo',
        '02_Galetario_23_Fichas.md': 'fichas das 23 espécies, com atributos, passiva, alas e os 30 golpes de cada uma (nível ou Mestres)',
        '03_Galolpedia_Golpes.md': f'os {len(golpes)} golpes com elemento, categoria, energia, poder, efeito e espécies',
        '04_Regras_Vigentes.md': f'texto integral das {len(regras)} regras da base (fonte de verdade)',
        '05_Decisoes_Progresso_e_Historico.md': 'revisões da base, pendências, propostas e decisões, progresso do mod, auditoria, nomenclatura e errata',
    }
    for f in ['00_LEIA_PRIMEIRO.md'] + arquivos:
        L.append(f"| {f} | {descr.get(f, '')} | {'—' if f not in tam else f'{tam[f] // 1024} KB'} |")
    L.append(f"| artes_reduzidas/ | {len(artes)} artes oficiais em JPEG reduzido, só para consulta | — |")
    L += ['\n## Instruções do Projeto (copie e cole)\n', '```',
          'Você é o responsável pelo projeto Galetocraft, um mod de Minecraft (Fabric 1.21.11 + GeckoLib) com criaturas chamadas',
          'Cocorídeos/Galetos, batalhas por turnos chamadas Rinhas, captura com a Pena de Captura, reprodução (Galeria) e Mestres',
          'Elementais. Fale sempre em português do Brasil.',
          '',
          'Fonte de verdade: os arquivos deste Projeto, gerados da base vigente (current_*) do repositório gbriel-trab/Galetocraft.',
          'Em conflito, vale 04_Regras_Vigentes.md e 02_Galetario_23_Fichas.md; o 01 é um resumo.',
          '',
          'Regras de trabalho:',
          '- O criador aprova tudo. Nada vira oficial sem aprovação expressa dele. Você propõe, confere e explica.',
          '- Não invente atributos, golpes, artes nem parâmetros. Se faltar dado, diga que falta e proponha opções.',
          '- "Homologado" não significa "implementado": diga se uma regra está só documentada ou já existe no mod (ver 05).',
          '- Atributos-base são do nível 50 (o rótulo "nível 100" em fichas antigas é erro de rótulo).',
          '- Nomenclatura oficial: Galetário (não RoosterTeca), Galolpédia (não GalolpeTeca), Herança de Bico, Tonto (não Tontura),',
          '  Ave Fênix (não Tricrina Infernal), Histórico da Rinha (não Diário de Batalha), Rinha, Galeria, Cocorídeos/Galeto.',
          '- Decisões de 18/11/2026: todos os direitos reservados; Lendário Original é classe própria (Quetzacocó 700);',
          '  par de gêmeos Cocórion+Cocórvolt inativo; #007–#015 sem golpe hereditário.',
          '- Imagens: o ChatGPT só gera imagens. Você prepara o pedido com os dados da ficha; o criador gera e aprova.',
          '- Mudanças na base e no código do mod são feitas no Claude Code, no repositório; aqui, registre as decisões',
          '  do criador com clareza para levar até lá.',
          '```',
          '\n## Artes oficiais (originais na base)\n',
          '| # | Espécie | Arquivo original | SHA-256 do original |\n|---:|---|---|---|']
    for n, nome, fn, sha in artes:
        L.append(f'| {n:03d} | {nome} | {fn} | `{sha[:16]}…` |')
    open(os.path.join(out, '00_LEIA_PRIMEIRO.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

    # zip com tudo
    with zipfile.ZipFile(os.path.join(os.path.dirname(out.rstrip('/')), f'Galetocraft_Projeto_rev{rev}.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for raiz, _, fs in os.walk(out):
            for f in fs:
                z.write(os.path.join(raiz, f), os.path.relpath(os.path.join(raiz, f), os.path.dirname(out.rstrip('/'))))
    print('ok', out, 'rev', rev, {f: os.path.getsize(os.path.join(out, f)) // 1024 for f in sorted(os.listdir(out)) if f.endswith('.md')})


if __name__ == '__main__':
    main()

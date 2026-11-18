# Galetocraft — Base vigente (no repositório)

**Desde 18/11/2026 o Claude é o responsável por todo o projeto Galetocraft, por decisão do criador.** O ChatGPT serve apenas para gerar imagens. A base vigente saiu da biblioteca do ChatGPT e passou a morar aqui, em arquivos de texto versionados pelo git.

## O que tem aqui

| Pasta | Conteúdo |
|---|---|
| `vigente/` | Uma tabela `current_*` por arquivo JSON: espécies, golpes, regras, pendências, Herança de Bico, Galeria, artes, fontes, metadados e diário de revisões |
| `artes/` | As 23 artes oficiais do Galetário (`current_art`). O SHA-256 de cada uma é conferido |
| `fontes/` | Documentos-fonte embutidos na base (`current_sources`) |

**Revisão atual: 6.**
- rev. 3: correções de coerência e nomenclatura oficial.
- rev. 4: nova governança, artes #019 e #020 e regra de nomenclatura.
- rev. 5: regras oficiais de combate, captura e XP migradas do histórico, incluindo o dano V5.6.
- rev. 6: golpes próprios de #001–#011 completados com a ficha original.

O histórico de cada revisão fica em `vigente/current_journal.json`, e os pacotes aplicados ficam em `docs/patches/`.

**As tabelas históricas** (Betas, ramos R, estudos, 213 tabelas) não foram trazidas. Elas continuam no `Galetocraft.sqlite` da revisão 2, publicado no Release `acervo-documental-2026-11-17` (pacote 00), e servem só para montar o SQLite completo.

## Como usar

Todos os comandos são rodados na raiz do repositório:

```
python ferramentas/base/galetobase.py validar                       # integridade, chaves, 5+25 golpes, hashes, diário
python ferramentas/base/galetobase.py ficha --especie 22            # ficha vigente de uma espécie
python ferramentas/base/galetobase.py atualizar --pacote P.json     # altera registros existentes
python ferramentas/base/galetobase.py migrar --pacote M.json        # insere ou altera em qualquer tabela current_*
python ferramentas/base/galetobase.py montar --historico REV2.sqlite --saida Galetocraft.sqlite
```

- **`atualizar`:** aceita o mesmo formato de pacote do antigo `Atualizar_Galetocraft.py` (`expected_revision`, `reason`, `evidence`, `operations`).
- **`migrar`:** aceita `"op": "inserir"` ou `"op": "atualizar"`.
- **Ao aplicar um pacote**, a ferramenta faz quatro coisas:
  1. Recusa o pacote se a revisão esperada não bater.
  2. Valida a base inteira antes de gravar.
  3. Incrementa a revisão.
  4. Registra o antes e o depois no diário.
- **Depois de cada revisão:** rode `python ferramentas/base/exportar_para_mod.py` para atualizar os dados que o núcleo e o mod leem.
- **`montar`:** gera o `Galetocraft.sqlite` completo, com o histórico do Release mais a camada vigente deste repositório, e confere `integrity_check` e as chaves estrangeiras. O SQLite gerado é um derivado e não entra no git.

## Regras que continuam valendo

- **Nada é oficial sem aprovação expressa do criador.** Propostas e históricos não são promovidos por inferência.
- **Homologado não significa implementado.** `runtime_validado` continua `false` até haver teste real no mod.
- **Uma única base ativa:** esta. Toda mudança é feita por pacote, com fonte e evidência, e vira um commit.

## Fluxo de imagens (ChatGPT)

1. **Pedido:** quando uma arte ou ficha visual for necessária, eu preparo o pedido (prompt) com os dados da ficha vigente: número, nome oficial, elementos, raridade e nomenclatura (Galetário, não RoosterTeca).
2. **Geração:** o criador gera a imagem no ChatGPT e me envia, como anexo na conversa ou como arquivo no repositório.
3. **Conferência:** eu verifico a imagem antes de qualquer registro.
   - Espécie e número.
   - Textos impressos (elementos, raridade, nomes) contra a base.
   - Nomenclatura oficial.
   - Originalidade: sem citar personagens ou marcas de outras franquias.
   - Dimensões e SHA-256.
   
   Se algo divergir, aponto o que pedir de novo ao ChatGPT.
4. **Aprovação:** a imagem só entra em `current_art` ou `modelos/referencias/` depois da aprovação expressa do criador.
5. **Registro:** eu faço a migração, com o hash e a fonte registrados no diário, e o commit.

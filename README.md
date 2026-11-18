# Galetocraft

Projeto Galetocraft: código, modelos, ferramentas e acervo documental.

## Dados e documentos

O acervo documental de 17/11/2026 está na seção [Releases](/gbriel-trab/Galetocraft/releases/tag/acervo-documental-2026-11-17), com 1.636 arquivos identificados do projeto, inventário e somas SHA-256. Os pacotes são arquivos ZIP independentes: extraia todos na mesma pasta para reconstruir a organização original. Os arquivos relacionados que estavam fora da pasta Galetocraft são preservados na raiz da extração.

- **Galetocraft_00_Base_Vigente.zip**: banco da revisão 2, manual, atualizador, verificação e índices de 17/11. Hoje é histórico, porque a base vigente fica em `base/`.
- **Galetocraft_NN_Acervo.zip**: demais documentos, artes, scripts, propostas, estudos e históricos.
- **INVENTARIO_GALETOCRAFT.json**: caminho, tamanho, SHA-256 e pacote de cada arquivo.
- **SHA256SUMS.txt**: verificação dos pacotes ZIP.
- **DADOS_VIGENTES_CONSULTA.json**: exportação legível da camada atual; arquivo derivado, não uma base concorrente.

## Responsável e fonte de verdade

Desde 18/11/2026, por decisão do criador, o **Claude** é o responsável por todo o projeto: base de dados, regras, documentação, modelos e código do mod. O **ChatGPT** serve apenas para gerar imagens.

A única base vigente fica neste repositório, em [`base/`](base/LEIA_ME.md):
- `base/vigente/`: tabelas `current_*` em JSON.
- `base/artes/`: as 23 artes oficiais.
- `base/fontes/`: documentos-fonte.

Ela está na **revisão 4**. É mantida com `ferramentas/base/galetobase.py`, que valida a base, aplica pacotes de alteração com diário de revisões e monta o `Galetocraft.sqlite` completo. Cada revisão é um commit.

O `Galetocraft.sqlite` do Release (revisão 2, SHA-256 `9dd2253d…5aa3c`) fica como **histórico**. Dele vêm as tabelas antigas usadas para montar o SQLite completo. Betas, ramos R, propostas e ensaios são evidências históricas, mesmo quando o nome do arquivo diz "oficial".

## Documentação

| Documento | Conteúdo |
|---|---|
| [`docs/CONHECIMENTO_GALETOCRAFT.md`](docs/CONHECIMENTO_GALETOCRAFT.md) | Resumo de todo o projeto |
| [`docs/NOMENCLATURA_OFICIAL.md`](docs/NOMENCLATURA_OFICIAL.md) | Nomes oficiais |
| [`docs/AUDITORIA_INCOERENCIAS.md`](docs/AUDITORIA_INCOERENCIAS.md) | Auditoria de incoerências |
| [`docs/ERRATA_NIVEL_50.md`](docs/ERRATA_NIVEL_50.md) | Errata do nível 50 |

## Implementação

O mod (`galetocraft/`, Fabric 1.21.11 + GeckoLib) traz hoje 12 espécies em exibição. Rinha, captura, golpes, elementos e reprodução ainda estão só documentados na base: homologado não significa implementado.

O acervo do Release é uma fotografia de 17/11/2026, preservada sem alterações.

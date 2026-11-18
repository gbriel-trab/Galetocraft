# Galetocraft — Nomenclatura oficial

**Oficializada em 18/11/2026, por pedido expresso do criador.** O pedido incluiu oficializar as trocas de nome feitas no projeto, e também os nomes "Galeria" e "Histórico da Rinha".

A versão em formato de máquina está em `ferramentas/acervo/nomenclatura_oficial.json`.

## Trocas oficiais

| Nome oficial | Nome antigo | O que designa | Decidido em |
|---|---|---|---|
| **Galetário** | RoosterTeca | Enciclopédia de espécies (fichas dos Cocorídeos) | 11/11/2026 |
| **Galolpédia** | GalolpeTeca, GalolpeTecas, GalolpeTeca Geral | Catálogo geral de golpes | 11/11/2026 |
| **Herança de Bico** | GalolpeTeca Hereditária | Seção dos golpes hereditários paternos | 11/11/2026 |
| **Tonto** | Tontura | Estado negativo persistente | 13/11/2026; reafirmado em 14/11 |
| **Ave Fênix** | Tricrina Infernal | Golpe hereditário exclusivo do #001 Pirococó | 09/11/2026 |
| **Histórico da Rinha** | Diário de Batalha | Registro das ações e do resultado de uma Rinha | Rótulo opcional desde 11/11; oficial desde 18/11 |
| **Rinha / Rinhas** | "combate", como termo genérico para a atividade | A batalha por turnos | 11/11/2026 |
| **Cocorídeos** (coletivo) / **Galeto** (indivíduo) | Denominações anteriores de raça | O grupo de criaturas e cada criatura | 11/11/2026 |
| **Galeria** | "Galeria (nome provisório)" | Sistema de criação e reprodução (alas, pares, ovos, linhagem) | Provisório desde 12/11; oficial desde 18/11 |

## Como aplicar

- **Use sempre o nome oficial** em texto de apresentação: títulos, legendas, descrições, fichas, interface do mod, textos de idioma e documentação.
- **Os nomes antigos continuam em dois casos:**
  - **Identificadores técnicos:** caminhos e pastas (`Galetocraft/RoosterTeca/`, `GalolpeTecas/`), nomes de arquivo, tabelas SQL (`beta_roosterteca`, `beta_galolpeteca`), chaves JSON (`roosterteca_id`, `sob_tontura_falha_chance`) e IDs em minúsculas (`tontura`). Renomeá-los quebraria referências e hashes. `tontura` continua como alias técnico de **Tonto**.
  - **Citações históricas** que explicam a troca. Exemplos: "Galetário (antiga RoosterTeca)" e "renomeia e substitui Tricrina Infernal".
- **Exceção da Rinha:** o botão do menu da Rinha continua escrito **Combate**. "Rinha" é o nome da atividade, não do botão. Por isso essa troca é feita à mão, conforme o contexto.
- **Galeria:** onde aparecer "nome provisório", o qualificativo deve ser retirado.

## Onde já foi aplicada

- **Cópias corrigidas das fichas oficiais** (`docs/acervo_corrigido/`):
  - Foram 70 trocas em 19 arquivos, feitas depois da correção do nível 50.
  - Exemplos: os títulos "RoosterTeca #007" viraram "Galetário #007", e "chance de Tontura" virou "chance de Tonto".
  - Os artigos foram ajustados ao gênero do nome novo, como em "da RoosterTeca" → "do Galetário".
  - O relatório com cada troca e o SHA-256 antes e depois está em `docs/acervo_corrigido/NOMENCLATURA_APLICADA.json`.
- **Documentação e código do repositório:** `docs/CONHECIMENTO_GALETOCRAFT.md`, `CLAUDE.md`, `docs/ERRATA_NIVEL_50.md` e o comentário em `ModEntidades.java`.
- **Originais do Release:** não foram alterados e seguem como histórico.

## Base vigente: publicada

- **Revisão 3:** a nomenclatura foi aplicada aos textos da base, junto com as correções da auditoria (`docs/patches/rev3_coerencia_e_nomenclatura.json`).
  - "Tontura" virou "Tonto" no efeito de 2 golpes do #013 Quartzaló: Concentração e Faíscas do Geodo.
  - Os campos técnicos (`status_nucleo`, chaves) foram mantidos.
- **Revisão 4:** a nomenclatura passou a ser uma regra própria da base, `current_rules` → `nomenclatura` (`docs/patches/rev4_governanca_artes_nomenclatura.json`).
- **Onde está a base:** desde 18/11/2026 ela fica no repositório (`base/vigente/`), mantida pelo Claude com `ferramentas/base/galetobase.py`.

## Para reaplicar em outros documentos

```
python ferramentas/acervo/aplicar_nomenclatura.py --pasta PASTA_DE_COPIAS --relatorio relatorio.json
```

Use o script apenas em cópias derivadas, nunca nos originais do acervo. Com `--saida`, ele grava o resultado em outra pasta.

## Registros parecidos que não são trocas de nome

- **Conceitos de proposta substituídos por outros conceitos** (12/11): Nimbocó → Libelocó (#016), Raizaló → Castorocó (#017) e Brasapó → Mariposocó (#018). Não são apelidos da mesma criatura.
- **"Crista Poderosa":** forma usada em conversa. O nome oficial é **Crina Poderosa**.
- **Morcegalo:** o elemento passou de Sombrio para Ar. É uma retificação de elemento, não de nome.

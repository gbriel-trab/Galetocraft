# Errata — atributos-base no nível 50 (18/11/2026)

## Contexto

- **A regra vigente:** desde a Norma de Progressão Nível 50 V1 (13/11/2026), os atributos-base de cada Cocorídeo são a referência do **nível 50**. No nível 100, cada atributo vale 1,5×, pela fórmula `A(L) = A50 × (L+50)/100`.
- **O erro:** várias fichas oficiais anteriores ainda traziam o rótulo antigo, "Atributos-base (nível 100)", sobre os **mesmos números**.
- **Situação na base vigente:**
  - `Galetocraft.sqlite` já estava correta (`base_nivel = 50`).
  - A pendência R03 tratava o rótulo antigo como "resolvido na leitura", mas os documentos continuavam com o rótulo errado.

Esta errata corrige os documentos **sem alterar os originais** do Release `acervo-documental-2026-11-17`. Esses originais seguem preservados como histórico, conforme a política da base.

## O que foi feito

- **Cópias corrigidas:** estão em `docs/acervo_corrigido/` e mantêm os caminhos originais do acervo. Abrangem 29 arquivos distintos, que cobrem 42 caminhos do acervo (os outros 13 são cópias idênticas).
- **Critério de troca:** o rótulo só passou de 100 para 50 depois de conferir os números contra `current_species` e `current_rules.progressao` da base vigente. As 80 trocas tiveram números idênticos.
  - Atributos: os seis valores de cada espécie.
  - Totais: valores como 550, 370 e 570.
  - Escala de raridades: as faixas de 350–390 a 590–630.
- **JSON:** as chaves foram renomeadas (`atributos_base_nivel100` → `atributos_base_nivel50`, `atributos_base_nivel_100` → `atributos_base_nivel_50`, `base_stats_level_100` → `base_stats_level_50`). A formatação original foi preservada.
- **Notas de errata:** dois registros parciais não traziam números conferíveis e receberam uma nota com os valores vigentes, em vez da troca de rótulo:
  - `RoosterTeca_008_Axococo_Registro_Parcial_Oficial.md`
  - `RoosterTeca_009_Vagalo_Parcial_Oficial.md`
- **Relatório completo** (`docs/acervo_corrigido/ERRATA_NIVEL_50.json`): registra cada rótulo, a espécie, os valores conferidos, a ação aplicada, as cópias idênticas e o SHA-256 do original e da cópia corrigida.

## Fichas corrigidas

| Espécies | Documento |
|---|---|
| #001–#021 | Galetário consolidado BAL de 12/11 (`.md`, 21 rótulos; `.json`, 18 chaves) |
| #001–#015 | `Galetario_Oficial_Completo_2026-11-11.md` (fichas, tabela-resumo e escala de raridades) |
| #007, #008, #009, #010, #011, #012 | Fichas do Galetário (Taturico, Axococó, Vagaló, Morcegalo, Espinhocó, Salambrasa), que no acervo estão em arquivos `RoosterTeca_0NN_*` |
| #013 | Quartzaló (ficha oficial v1) |
| #014, #015 | Carangocó e Faíscocó (ficha `.md`, versão WhatsApp `.txt` e registro `.json`) |
| #016, #017, #018 | Libelocó, Castorocó e Mariposocó (fichas oficiais da homologação 016–018) |
| #019, #020, #021, #022 | Renacocó, Frankocó, Cabacocó e Sirenocó (ficha `.md` e `.json` do Galetário) |

## O que não foi alterado

- **Projeções legítimas de nível 100:** permanecem como estão, porque já seguem a norma. Exemplos: "HP no nível 100: `ceil(1,5 × HP)`" e a coluna "Projeção nível 100 (×1,5)" do Quetzacocó.
- **Fora do escopo:** propostas, Betas, ramos R, estudos de balanceamento, memórias e dossiês. São histórico, e a correção abrangeu só as fichas oficiais.
- **Base vigente e Release:** a base vigente e os pacotes ZIP do Release não foram tocados.

## Como reaplicar

1. Extraia os ZIPs do Release.
2. Rode o script:

   ```
   python ferramentas/acervo/corrigir_rotulo_nivel50.py \
     --dados DADOS_VIGENTES_CONSULTA.json --acervo PASTA_DO_ACERVO --saida PASTA_DE_SAIDA
   ```

A lista de fichas fica em `ferramentas/acervo/fichas_oficiais_nivel100.json`.

Depois desta correção, as cópias também receberam a nomenclatura oficial, com `ferramentas/acervo/aplicar_nomenclatura.py` (ver `docs/NOMENCLATURA_OFICIAL.md`). Por isso, o `sha256_corrigido` do `ERRATA_NIVEL_50.json` corresponde à etapa do nível 50. O hash final de cada arquivo está em `NOMENCLATURA_APLICADA.json`. Para reproduzir as cópias atuais, rode os dois scripts nesta ordem. Se aparecer uma ficha com números diferentes dos vigentes, o script não troca o rótulo: ele insere uma nota de errata e registra a divergência no relatório.

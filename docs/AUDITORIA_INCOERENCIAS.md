# Galetocraft — Auditoria de incoerências e dados conflitantes (18/11/2026)

## Escopo

A auditoria foi pedida pelo criador em 18/11/2026: encontrar e resolver todas as incoerências. Foram verificados:
- a base vigente `Galetocraft.sqlite` (revisão 2), nas camadas `current_*` e nas regras;
- o catálogo de golpes das 23 espécies;
- as fichas oficiais do acervo comparadas com a base;
- os documentos de sistemas;
- o código e a documentação do repositório.

## Critério de resolução

1. **Decisão expressa mais recente vale por campo.** É a regra da própria base: decisão expressa mais recente > ficha homologada > cópia histórica.
2. **Uma norma universal vale para todas as espécies.** Exemplo: a Concentração V2.3, cuja ata manda aplicá-la a todas e retificar as fichas #019–#021.
3. **Decisão do criador quando nada acima resolve.** Quatro conflitos foram resolvidos assim em 18/11: licença, Quetzacocó, gêmeos e golpes hereditários.
4. **Nada foi inventado e os históricos foram preservados.**
   - As atas mantêm o texto integral. As resoluções entram em um campo novo, `resolucoes_posteriores`.
   - Os originais do Release não foram alterados.

## Resumo

| Área | Conflitos | Resolvidos | Onde |
|---|---:|---:|---|
| Base vigente | 14 | 14 | Pacote `docs/patches/rev3_coerencia_e_nomenclatura.json` (74 operações). Testado; falta publicar |
| Documentos do acervo | 9 | 9 | Cópias corrigidas, decisões registradas e base de conhecimento |
| Repositório | 6 | 6 | Arquivos alterados neste commit |

Também ficam registrados 3 pontos técnicos não alterados e as pendências de design (seção final). Pendências de design não são conflitos de dados.

## 1. Base vigente: pacote rev. 3

O pacote foi gerado por `ferramentas/acervo/gerar_patch_rev3.py` e aplicado com o atualizador oficial numa cópia da base.
- **Integridade:** a revisão passou de 2 para 3, com `integrity_check = ok`, nenhuma violação de chave estrangeira e o registro gravado em `current_journal`.
- **Golpes:** depois do pacote, nenhum golpe tem dados divergentes entre espécies.

| # | Conflito | Resolução |
|---|---|---|
| B1 | A **Concentração** tinha textos e elementos diferentes nas 23 espécies. #019–#021 diziam "buff aleatório e 20% de chance" (versão anterior à V2.3). #001–#012 diziam só "sem descrição; consultar JSON". O elemento aparecia como vazio, Neutro, "Sem elemento" ou "Neutro/sem elemento" | Aplicado o texto da V2.3 com o elemento "Sem elemento" em todas as espécies, conforme os itens 1 e 10 da ata de 13/11. O #022 mantém a nota da Partitura e o #023 mantém o próprio texto, que já era o da V2.3 |
| B2 | **Crina Poderosa / Garra Afiada** tinham um texto provisório ("consultar o JSON original protegido") e variações sem conteúdo diferente | Texto canônico do golpe básico (Poder 40, Energia 0, sem efeito secundário) |
| B3 | Os 30 golpes do **#023 Quetzacocó** usavam outro esquema de campos (`efeito_oficial_literal`, `poder_base`, "mágico" com acento), o que impedia comparar e integrar | Foram acrescentados os campos comuns, sem apagar os originais. Os 25 aprendíveis foram conferidos: efeito, poder, energia e elemento idênticos ao catálogo |
| B4 | "Tontura" no texto de golpes do #013 | Trocado por "Tonto" (nomenclatura oficial). Os IDs técnicos foram mantidos |
| B5 | A ata da Concentração listava como **pendentes** os "36 atributos dos iniciais" e o "peso do Renacocó" | Marcados como resolvidos, porque `current_issues` R02 e R09 já os resolveram |
| B6 | A norma de progressão dizia "36 campos não resolvidos" | Marcado como resolvido (R02) |
| B7 | O Golpe Duplo preservava "conflitos dos 36 atributos" | Marcado como resolvido (R02) |
| B8 | A tipagem dupla dizia que a Sirenocó seria tratada "quando for incorporada", mas ela foi incorporada em 13/11. A matriz falava em 8 espécies duplas e 4 casos de 4× | Registrado: a Sirenocó já está incorporada. Hoje são 9 espécies duplas e 5 casos de 4× (Sirenocó com Elétrico 4×) |
| B9 | O Nexo listava como pendentes "atributos e peso do #023" e "passiva e repertório do #023" | Resolvidos pela ficha V2 de 16/11 (700 pontos, 180 kg, Soberania dos Ventos Eternos, 30 golpes). A "herança de golpes Nexo" fica sem aplicação, porque Lendários Originais não reproduzem |
| B10 | O Quetzacocó soma 700, acima da faixa Lendário (590–630), e "Lendário Original" não tinha faixa | **Decisão do criador:** "Lendário Original" é uma classe própria, fora da escala, com o total definido pela ficha. Continua 700 |
| B11 | Os gêmeos especiais incluíam Cocórion + Cocórvolt, duas espécies 100% machos, então o par é impossível | **Decisão do criador:** o par fica registrado como **inativo** |
| B12 | #007–#015 não têm golpe hereditário, enquanto #001–#006 e #016–#022 têm | **Decisão do criador:** é **por design**. O #023 não reproduz |
| B13 | A pendência R03 (rótulo "nível 100") estava só "resolvida na leitura" | Marcada como resolvida. As cópias corrigidas estão em `docs/acervo_corrigido/` |
| B14 | A pendência R12 dizia que faltavam as artes #019 e #020 e o modelo r82 | **Identificados pelas fichas homologadas:** #019 "Renacocó com Face Azul Claro.png" (`a0291420…`) e #020 "Ficha Oficial Frankocó #020.png" (`4790f440…`). O modelo r82 está no repositório e foi exportado no mod. As artes foram copiadas para `modelos/referencias/`. Incluí-las em `current_art` exige migração, porque é um registro novo |

## 2. Documentos do acervo

| # | Conflito | Resolução |
|---|---|---|
| D1 | Fichas com rótulo "nível 100" | Corrigido em `docs/acervo_corrigido/` (ver `ERRATA_NIVEL_50.md`) |
| D2 | Nomenclatura antiga (RoosterTeca, Tontura etc.) | Oficializada e aplicada (ver `NOMENCLATURA_OFICIAL.md`) |
| D3 | **Parceiros dos Mestres:** a v1.1 lista 3 por Mestre, incluindo espécies de outro elemento (Braseiro com Cocórak e Cocórion; Faísca com Cocórion etc.). O Elenco provisório e a IA de Substituição usam 2 espécies da própria afinidade | Valem as **duplas da afinidade**: Pirococó/Salambrasa, Cocórrego/Axococó, Esporocó/Espinhocó, Cocórak/Taturico, Cocórion/Morcegalo e Cocórvolt/Vagaló. É a decisão específica, confirmada depois pela Competência Didática ("as duplas permanecem"). A lista da v1.1 vira sugestão histórica |
| D4 | Os documentos dos Mestres citam "11/12 espécies", "302 vínculos" e "137 de treino" | São contagens de 10/11. Valem o Ensino Universal (qualquer golpe compartilhado, exceto hereditários) e a base atual (23 espécies, 690 vínculos) |
| D5 | Atas e documentos dos Mestres citam "Java/NeoForge" | A plataforma é **Fabric 1.21.11 + GeckoLib**, como mostram o código e a base vigente. As menções a NeoForge estão obsoletas |
| D6 | A auditoria R5.5 (15/11) diz que os atributos e golpes do #023 "não estão homologados" | Superada pela ficha V2 de 16/11 |
| D7 | Registros parciais do Axococó e do Vagaló marcam atributos "pendentes" | Superados pelas fichas completas. Há uma nota nas cópias corrigidas |
| D8 | A arte antiga do Faíscocó exibe "Comum", mas a raridade oficial é Raro | Vale **Raro**. A arte não muda sem autorização; a legenda fica registrada como desatualizada |
| D9 | **Arte do Renacocó:** a Memória Mestra (12/11, espécie ainda em criação) cita "Renacoco_019_Galetario_Oficial.png". A ficha homologada, o Galetário consolidado (BAL) e a consolidação R5.3 citam "Renacocó com Face Azul Claro.png" | Vale a da **ficha homologada**. A referência usada no modelo r82 é visualmente a mesma arte |

## 3. Repositório

| # | Conflito | Resolução |
|---|---|---|
| P1 | O `LICENSE` era CC0, mas o `fabric.mod.json` dizia "All-Rights-Reserved" | **Decisão do criador:** todos os direitos reservados. O `LICENSE` foi substituído |
| P2 | A descrição do mod no `fabric.mod.json` citava só o Pirococó | Passou a citar as 12 espécies do mod |
| P3 | O `LEIAME.md` descrevia só o Pirococó e o fluxo antigo de exportação | Atualizado com as 12 espécies, o fluxo `especies/<id>.py` + `exportar_especie.py` e o estado do jogo |
| P4 | Comentários do código: Pirococó "~2,45 blocos" (a hitbox e a tabela dizem 2,8); "correntes" no Pirococó (o g09 não tem); Morcegalo "das sombras" (o elemento é Ar) | Comentários corrigidos. O comportamento não muda |
| P5 | `modelos/pirococo/detalhes.md` descreve a série p17 como se fosse a atual | Ganhou uma nota de documento histórico; o modelo vigente é o g09 |
| P6 | As artes oficiais #019 e #020 não estavam no repositório | Adicionadas em `modelos/referencias/` |

## 4. Não alterado (com o motivo)

- **`lod_log.txt` (Pirococó e Vagaló):** as contagens de peças são de modelos anteriores. O arquivo é saída de `lod_auto.py`. Rodar o script de novo também reescreve `lods.json` e muda o LOD do mod, então o ideal é fazer isso na próxima reexportação de cada espécie.
- **Glowmasks vazias** (Axococó, Cocórion, Espinhocó, Taturico):
  - A camada de brilho redesenha o modelo inteiro à toa. É um problema de desempenho, não de dados.
  - A correção exige mudar o código e testar no jogo.
- **Originalidade:**
  - A arte oficial do Renacocó cita "Marco" e "Estilo Ikki", personagens de outras franquias.
  - A pasta `modelos/galos_monstro/` se declara inspirada em Pokémon.
  - A arte homologada só muda com autorização do criador. Recomendo revisar esses textos antes de publicar o mod.

## 5. Pendências de design (não são conflitos)

- **Progressão e combate:**
  - Curva dos níveis 1–49 e HP de referência (R13).
  - Fórmula de dano definitiva.
- **Reprodução:**
  - Gatilhos completos dos gêmeos especiais.
  - Critérios ambientais da Etapa 02 (R16, U06).
  - Herança de Bico entre espécies (U01).
  - Etapas 03, 05 e 06 (U02).
- **Quetzacocó:** distribuição da aprendizagem do #023 (U03).
- **Maestria Elemental:** texto integral não recuperado (U04).
- **Mestres:** reavaliar os elencos com as espécies novas. Isso só pode ser feito com autorização do criador.
- **Renacocó:** altura definitiva (a atual, 2,5, é provisória).
- **Migrações da base:** incluir as artes #019 e #020 em `current_art` e registrar a regra de nomenclatura dentro da base.
- **Implementação no mod:** Rinha, captura, golpes, elementos e reprodução (R14).

## Como publicar a revisão 3 da base

A cópia principal da base fica na biblioteca do ChatGPT (mesmo Library ID). Lá, rode:

```
python Atualizar_Galetocraft.py Galetocraft.sqlite rev3_coerencia_e_nomenclatura.json
```

O pacote recusa a aplicação se a base não estiver na revisão 2.

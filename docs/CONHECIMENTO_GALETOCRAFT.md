# Galetocraft — Base de conhecimento consolidada

> Resumo de referência montado em 18/11/2026 a partir de: banco vigente `Galetocraft.sqlite` (revisão interna 2, SHA-256 `9dd2253d…5aa3c`), Release `acervo-documental-2026-11-17` (inventário de 1.636 arquivos), documentos oficiais dos sistemas e código deste repositório.
> **Este arquivo é um resumo, não uma fonte de verdade.** Em qualquer conflito, vale a camada `current_*` / `v_current_*` do banco vigente.

## 1. O que é o projeto

Galetocraft é um mod de Minecraft de criaturas colecionáveis chamadas **Cocorídeos** (também chamados de **Galetos**), inspiradas em galos e com anatomia própria. O jogador captura, treina, cria e batalha com eles em duelos por turnos chamados **Rinhas**.

Bibliotecas do universo:
- **Galetário**: enciclopédia de espécies (fichas).
- **Galolpédia / GalolpeTeca**: catálogo de golpes.
- **RoosterTeca**: coleção pessoal do jogador. Inclui o Diário dos Mestres.

Todo design passa por **homologação expressa do criador**. Propostas, Betas, ramos R e ensaios são histórico, mesmo quando o nome do arquivo diz "oficial".

## 2. Fonte de verdade e governança

- **Banco único vigente:** `Galetocraft/Base_Atual/Galetocraft.sqlite`, que está no pacote `Galetocraft_00_Base_Vigente.zip` do Release.
  - Dados: 23 espécies, 690 vínculos de golpes, 22 regras, 21 artes, 13 vínculos hereditários e 22 pendências.
  - Estrutura: 235 tabelas, 67 views, `PRAGMA integrity_check = ok`.
- **Ler somente `current_*` e `v_current_*`.**
  - A tabela `species` (12 linhas) é legada.
  - As outras 286 tabelas estão marcadas em `object_registry` como `HISTORICO_OU_EVIDENCIA`.
- **Precedência:** decisão expressa mais recente por campo > ficha homologada > cópia histórica. Datas de backup não revogam decisões.
- **`runtime_validado = false`** em tudo. A base é documental: nada nela prova que a regra esteja implementada ou testada no Minecraft.
- **Atualização:** usar `Atualizar_Galetocraft.py banco.sqlite patch.json`.
  - O patch precisa de `expected_revision`, `reason`, `evidence` e `operations`.
  - Só altera registros que já existem em `current_species`, `current_rules`, `current_moves`, `current_issues`, `current_heranca` e `current_galeria`.
  - Cada alteração incrementa a revisão e grava em `current_journal`.
  - Espécie nova, migração ou arte nova exige procedimento completo validado.
  - Não criar "Beta 1.8" nem outra base ativa.
- **Origem da gestão:** o projeto foi conduzido em conversas no ChatGPT, com Library IDs de arquivos, auditoria horária e backup diário. O Release do GitHub é uma fotografia de 17/11/2026, não uma sincronização automática.
- **Histórico de revisões:**
  - rev. 1 (17/11): unificação autorizada.
  - rev. 2 (17/11): `v_current_pares_reproducao` passou a usar `current_galeria`.

## 3. Espécies vigentes (atributos no nível 50)

Ordem dos atributos: HP / Atq. Físico / Def. Física / Atq. Mágico / Def. Mágica / Velocidade.

| # | Nome | Raridade | Elementos | Atributos | Total | Peso | Passiva | Alas (princ./sec.) | Machos |
|---:|---|---|---|---|---:|---:|---|---|---:|
| 1 | Pirococó | Mítico | Fogo | 90/35/60/185/95/85 | 550 | 5,8 | Chama Reencarnada | Arcanos | 50% |
| 2 | Cocórrego | Mítico | Água | 155/45/135/45/105/65 | 550 | 8,0 | Maré de Refluxo | Hidromorfos / Colossais | 50% |
| 3 | Esporocó | Mítico | Planta | 120/25/65/115/145/80 | 550 | 5,0 | Simbiose Venenosa | Fitomorfos | 0% |
| 4 | Cocórak | Mítico | Terra | 140/180/80/25/70/55 | 550 | 10,0 | Fúria do Deserto | Colossais | 50% |
| 5 | Cocórion | Mítico | Ar | 80/155/65/30/55/165 | 550 | 3,8 | Dançarino dos Ventos | Galiformes | 100% |
| 6 | Cocórvolt | Mítico | Elétrico | 90/25/55/155/65/160 | 550 | 5,2 | Senhor da Tempestade | Galiformes | 100% |
| 7 | Taturico | Comum | Terra | 85/55/105/25/60/40 | 370 | 7,5 | Carapaça Reativa | Couraçados / Zoomorfos | 50% |
| 8 | Axococó | Comum | Água | 95/35/50/90/60/40 | 370 | 5,8 | Memória das Brânquias | Hidromorfos / Zoomorfos | 50% |
| 9 | Vagaló | Comum | Elétrico | 60/25/40/15/50/180 | 370 | 3,1 | Código Luminescente | Alígeros / Zoomorfos | 50% |
| 10 | Morcegalo | Comum | Ar | 80/50/45/40/90/65 | 370 | 5,2 | Sonar Predatório | Zoomorfos / Alígeros | 50% |
| 11 | Espinhocó | Comum | Planta | 75/95/85/20/55/40 | 370 | 6,2 | Espinheiro Territorial | Couraçados / Fitomorfos | 50% |
| 12 | Salambrasa | Comum | Fogo | 95/90/80/25/50/30 | 370 | 6,4 | Pele de Brasa | Zoomorfos / Couraçados | 50% |
| 13 | Quartzaló | Comum | Terra + Elétrico | 70/45/65/80/65/45 | 370 | 8,5 | Quartzo Energizado | Couraçados / Arcanos | 50% |
| 14 | Carangocó | Comum | Água + Terra | 75/80/75/40/55/45 | 370 | 10,5 | Pinças de Sedimento | Zoomorfos / Couraçados | 50% |
| 15 | Faíscocó | Raro | Fogo + Elétrico | 70/60/50/95/55/100 | 430 | 5,8 | Indução Incandescente v2 | Galiformes | 50% |
| 16 | Libelocó | Comum | Água + Ar | 60/40/48/74/70/62 | 354 | 4,9 | Voo de Remanso | Alígeros / Zoomorfos | 50% |
| 17 | Castorocó | Comum | Planta + Terra | 90/70/90/39/58/27 | 374 | 11,2 | Barragem Reforçada | Zoomorfos / Fitomorfos | 50% |
| 18 | Mariposocó | Comum | Fogo + Planta | 68/44/49/97/62/68 | 388 | 5,6 | Escamas de Brasa | Alígeros / Zoomorfos | 50% |
| 19 | Renacocó | Mítico | Fogo | 180/80/100/40/100/70 | 570 | 6,8 | Três Chamas da Vida | Arcanos | 50% |
| 20 | Frankocó | Épico | Terra + Elétrico | 135/110/115/30/85/35 | 510 | 28,0 | Instinto de Reconstrução | Colossais | 50% |
| 21 | Cabacocó | Épico | Planta + Terra | 110/25/75/130/115/45 | 500 | 18,0 | Maldição do Lar Faminto | Arcanos / Fitomorfos | 50% |
| 22 | Sirenocó | Mítico | Água + Ar | 100/25/70/160/100/95 | 550 | 7,2 | Partitura das Marés V2.0 | Hidromorfos / Alígeros | 0% |
| 23 | Quetzacocó | Lendário Original | Ar + Planta + Nexo | 130/60/110/170/120/110 | 700 | 180,0 | Soberania dos Ventos Eternos | não reproduz | — |

- Os **seis iniciais** (#001–#006) cobrem um elemento básico cada e somam 550.
- Cocórvolt é **Elétrico** por decisão de 16/11.
- O peso natural tem faixa técnica de 80–150% (ex.: Renacocó 5,44–10,20 kg).
- **Repertório:** cada espécie tem 30 golpes, sendo 5 de origem e 25 aprendíveis.
  - Os 5 de origem são **2 universais** e **3 próprios**.
  - Universais: Concentração, mais Crina Poderosa (golpe básico mágico) ou Garra Afiada (golpe básico físico).
  - O 3º próprio costuma ser o golpe **exclusivo e hereditário**.
  - No total são 196 aprendíveis diferentes. Os IDs vêm do catálogo da Reforma Integral: G001–G144 mais a série N.
  - Todos os 690 vínculos estão com status "não runtime".
- **Golpes hereditários (13):**
  - #1 Ave Fênix
  - #2 Punho da Fortaleza
  - #3 Jardim da Discórdia
  - #4 Sepultamento do Deserto
  - #5 Julgamento dos Céus
  - #6 Julgamento dos Raios
  - #16 Espiral de Monção
  - #17 Arrebento de Raiz-Pedra
  - #18 Floração da Fornalha
  - #19 Juramento da Fênix
  - #20 Coração da Última Tempestade
  - #21 Veredito da Porta Fechada
  - #22 Ária da Maré Eterna
  - A compatibilidade entre espécies não está determinada.
- **Quetzacocó #023:**
  - Lendário Original, com o elemento exclusivo **Nexo** (V2.0).
  - Passiva: na primeira entrada invoca Ventania sem gastar ação nem Energia. Com Ventania ativa, ganha +50 p.p. de Atq. Mágico, e seus golpes de Planta não sofrem a penalidade da Ventania.
  - Golpes próprios: Cataclismo Celeste (Ar), Eclosão das Mil Coroas (Planta, invoca Santuário das Raízes) e Ascensão do Nexo (+50 p.p. de Atq. Mágico e de Velocidade por uso).
  - Não reproduz.
- **Wukocó #024** é apenas proposta.
- **Artes vigentes:** 21 em `current_art`. Faltam #019 Renacocó e #020 Frankocó (pendência R12).

## 4. Elementos e eficácia

**Matriz 6×6:** cada elemento tem 2 vantagens, 2 fraquezas e 1 relação neutra.

| Atacante | Forte contra (2×) | Fraco contra (0,5×) |
|---|---|---|
| Fogo | Planta, Ar | Água, Terra |
| Água | Fogo, Terra | Planta, Elétrico |
| Planta | Água, Elétrico | Fogo, Ar |
| Terra | Fogo, Elétrico | Água, Ar |
| Ar | Planta, Terra | Fogo, Elétrico |
| Elétrico | Água, Ar | Planta, Terra |

- **Neutro e Sem elemento** recebem 1×. Golpes de Suporte não aplicam eficácia.
- **Tipagem Dupla V1 (13/11):** os dois fatores são multiplicados uma única vez.
  - Só dá **4×** quando os dois elementos do defensor são fracos ao mesmo ataque.
  - Dois fatores 0,5× dão 0,25×.
  - Casos de 4× na base atual:
    - Faíscocó recebe 4× de Terra.
    - Libelocó e Sirenocó recebem 4× de Elétrico.
    - Castorocó e Cabacocó recebem 4× de Ar.
- **Nexo V2.0:** exclusivo do Quetzacocó e não transmissível.
  - Como atacante: 2× contra Fogo e Ar, 0,5× contra Elétrico.
  - Como defensor: recebe 0,5× de Fogo e Ar, e 2× de Elétrico.
  - Contra o Quetzacocó, o cálculo multiplica os três fatores (Ar × Planta × Nexo). O resultado final: Fogo 2×, Elétrico 2×, Nexo 2×, Água 0,5×, Terra 0,5×, Planta 0,5× e Ar 1×.

## 5. Rinha (combate por turnos)

### Formato, energia e golpes equipados
- **Formato oficial:** 3v3, com 1 Cocorídeo ativo por lado e 2 na reserva.
- **Golpes equipados:** 5 por Cocorídeo. Concentração é obrigatória; os outros 4 são escolhidos.
- **Energia:**
  - Teto de 100.
  - Todo Galeto entra em campo com 100, em qualquer tipo de entrada.
  - Recupera +20 no início de cada turno próprio.
- **Acertos:** no máximo 2 por ação. Golpes sequenciais aprovados podem chegar a 5.

### Concentração V2.3 (13/11)
- Custa 0 de Energia e devolve +35 em execução válida.
- Tem 40% de chance de remover um estado persistente.
- Cria a **Pena de Ritmo**: uma por equipe, válida por 2 oportunidades.
- A Pena é gasta em um de quatro Cantos:
  - **Ofensivo:** +12% de dano e +6 de Pressão.
  - **da Guarda:** +15 de Energia se a Guarda estiver certa.
  - **de Revezamento:** −20% no primeiro acerto sofrido pelo Galeto que entrou.
  - **de Suporte:** −15 no custo do golpe.

### Golpe Duplo Estratégico V2.2 (13/11)
- **Chance do segundo acerto:**
  - Se a Velocidade do atacante for maior ou igual à do defensor: `min(0,50 ; 0,25 + 0,50 × (Va/Vd − 1))`.
  - Se for menor: 0.
- O segundo acerto causa 50% do dano base.
- Se houver chance intrínseca (por exemplo, Lâminas de Vento com 25%), ela é combinada de forma independente: `1 − (1−Pu)(1−Pi)`.

### Mira Anatômica Estratégica V1.5 (12/11)
- **Regiões e multiplicador de dano:**

  | Região | Multiplicador |
  |---|---:|
  | Cabeça/crina | 0,78 |
  | Asas | 0,86 |
  | Pernas/garras | 0,90 |
  | Tronco | 1,00 |

- **Pressão:**
  - Vai de 0 a 100. A região fica exposta em 50 e rompe em 100.
  - Ganho de 18 por golpe com dano, limitado a 65 por região em cada ação.
  - Cai 10 por oportunidade própria sem acerto.
- **Ruptura:** dura 2 oportunidades do alvo e aplica um debuff pela região rompida.

  | Região | Atributo reduzido | Redução |
  |---|---|---:|
  | Cabeça | Atq. Mágico | −45% |
  | Asas | Velocidade | −40% |
  | Pernas | Atq. Físico | −45% |
  | Tronco | Defesas | −30% |

- **Guarda:**

  | Resultado | Dano | Pressão |
  |---|---:|---|
  | Correta | ×0,65 | ×0,2 |
  | Neutra | ×1,0 | normal |
  | Errada | ×1,1 | +10 |

- **Leitura Perfeita:** concede +8 de pressão.

### Ambiente e estados
- **Climas** (duram 4 rodadas): Chuva, Ensolarado, Ventania e Tempestade de Areia.
- **Santuários:** dos Raios e das Raízes.
- **Estados negativos persistentes:** Queimadura, Envenenamento, Afogamento, Tontura e Paralisia. A captura também menciona Sono.

### Fórmula de dano
- A Tipagem Dupla V1 cita as versões **V5.6/V5.6.1**, com arredondamento único por acerto.
- A "fórmula de dano definitiva" ainda está **pendente**.

## 6. Progressão, captura, XP e outros sistemas

- **Progressão de atributos (Nível 50 V1):**
  - O nível 50 é a referência.
  - Entre os níveis 50 e 100: `A(L) = A50 × (L+50)/100`. No nível 100, o atributo vale 1,5 × o do nível 50.
  - A curva dos níveis 1–49 está pendente.
- **Faixas de total no nível 50 por raridade:**

  | Raridade | Faixa | Referência |
  |---|---:|---:|
  | Comum | 350–390 | 370 |
  | Raro | 410–450 | 430 |
  | Épico | 470–510 | 490 |
  | Mítico | 530–570 | 550 |
  | Lendário | 590–630 | 610 |

  "Super Raro" é uma classe histórica e não faz parte da escala atual. "Divino" não tem total homologado.

> As regras de captura, XP, nutrição, treinador e itens desta seção estão em tabelas técnicas das Betas 1.2.x. O banco as marca como **históricas**. A única leitura vigente de captura é `v_current_captura`, que contém só o cooldown.

- **Captura com a Pena** (item de captura com 5 níveis):
  - Multiplicador F por nível: 1,0 / 1,3 / 1,65 / 2,05 / 2,5.
  - XP para subir de nível: 1.000 / 3.000 / 7.000 / 15.000.
  - Lendário exige Pena nível 5.
  - Probabilidade: `P = 100·força/(força + D)`.
    - No mundo: `força = R·F`.
    - Na Rinha: `força = R·F·H·S`.
  - Fator R por raridade:

    | Raridade | R |
    |---|---:|
    | Comum | 1,8 |
    | Raro | 1,2 |
    | Super Raro | 0,8 |
    | Épico | 0,5 |
    | Mítico | 0,3 |
    | Lendário | 0,14 |
    | Divino | 0,05 |

  - Cooldown após falha: 20 s (60 s para Lendário), compartilhado entre jogadores.
- **Treinador:** equipe principal de até 5 Cocorídeos e reservas ilimitadas. O Cocorídeo capturado vai para a reserva se a equipe estiver cheia.
- **XP dos Cocorídeos (V1.260):**
  - XP total para o nível N: `T(N) = (N−1)³ + 10(N−1)²`.
  - Só há XP em Rinha vencida.
  - Recompensa: `floor((25+15L) × M_raridade × C_desafio × M_modo)`.
  - Multiplicador de raridade: de 1,0 (Comum) a 3,4 (Divino).
- **Nutrição:**
  - 12 alimentos, 2 por atributo.
  - O comum dá +0,1 de EV e o raro dá +1,0 de EV. Exemplo: Trigo e Maçã dourada para HP.
  - Os alimentos também alteram o peso.
  - IVs vão de 1 a 40.
- **Itens equipáveis:** 20 itens em 4 categorias (Ambiental, Ofensiva, Defensiva, Utilitária). Status: candidato.

## 7. Reprodução e Galeria (Reprodução V2.0)

- **Galeria:**
  - 22 espécies reprodutíveis, distribuídas em **8 alas**: Galiformes, Alígeros, Colossais, Couraçados, Fitomorfos, Hidromorfos, Zoomorfos e Arcanos.
  - Um casal é compatível se for macho e fêmea com pelo menos 1 ala em comum. Ala principal e secundária têm o mesmo peso.
  - A view `v_current_pares_reproducao` registra 484 pares.
- **Filhote:**
  - Pais da mesma espécie geram essa espécie.
  - Pais de espécies diferentes: 50% de chance da espécie da mãe e 50% da do pai.
  - Não há híbridos.
  - O sexo segue a distribuição da espécie do filhote.
- **Terreiro de Encontro:**
  - Gera de 1 a 3 ovos por leva, com chances de 25%, 50% e 25%.
  - Cada leva leva 10 min.
- **Ninhos:**
  - Há 8 tipos, um por ala, com capacidade para 3 ovos.
  - São obrigatórios para incubar.
  - A afinidade de ala reduz o tempo (multiplicador 0,7).
  - Refinamento: 50% de chance de melhorar 1 IV não herdado.
- **Incubação:**
  - Leva 40 min, com mínimo de 18.
  - Reduções: afinidade 30%, proteção 5%, decoração 10% e microclima 10%, somando no máximo 55%.
  - A eclosão é manual e mostra apenas partículas breves.
- **IVs:**
  - 3 são herdados, cada um vindo da mãe com 70% de chance ou do pai com 30%.
  - Os outros 3 são sorteados de 1 a 40.
- **Gêmeos:**
  - Casais elegíveis: 0,4% de gêmeos comuns e 0,1% de gêmeos especiais por ovo.
  - Demais casais: 0,5% de gêmeos comuns e nenhuma chance de especiais.
  - Gêmeos têm os 6 IVs idênticos.
  - Pares especiais conhecidos: Pirococó+Renacocó e Cocórion+Cocórvolt. O segundo par é impossível hoje, porque as duas espécies são 100% machos.
  - Os gatilhos dos gêmeos especiais estão pendentes.
- **Herança de Bico:**
  - Se o pai é portador, o filhote herda com 100% de chance.
  - Se só a mãe é portadora, a chance é de 25%.
  - Ave Fênix é herdada com 100% de chance se qualquer um dos pais for portador.
- **Árvore Genealógica V1.1:** fica em Galetário > Galeria > Linhagem e mostra 4 gerações.
- **Lendários Originais não reproduzem.**

## 8. Mestres Elementais (design oficial de 10/11, não implementado)

- **Sete NPCs de treinamento:**

  | Código | Mestre | Elemento | Estrutura |
  |---|---|---|---|
  | ME-01 | Braseiro | Fogo | Altar de Cinzas |
  | ME-02 | Maré | Água | Pavilhão das Marés |
  | ME-03 | Verdejar | Planta | Jardim das Raízes |
  | ME-04 | Cascalho | Terra | Pátio de Pedregulho |
  | ME-05 | Ventania | Ar | Terreiro dos Ventos |
  | ME-06 | Faísca | Elétrico | Posto de Condutância |
  | ME-07 | Terreiro | Neutro | Dojo de Campo |

- **Classes e pesos de aparição:** Instrutor 65%, Veterano 25% e Mestre 10%. Os pesos são relativos entre si, não chances de spawn.
- **Batalha:**
  - Formato 3×3, com 1 ativo por lado.
  - Os três Galetos do NPC usam o maior nível disponível entre os Galetos do jogador.
- **Como o jogador aprende um golpe:**
  - Escolhe um golpe compartilhado que o seu Galeto ainda não sabe.
  - Golpe de dano: precisa sofrer um acerto válido dele.
  - Golpe de suporte: basta ver a execução.
  - Em ambos os casos, precisa vencer o NPC na mesma batalha.
  - O treino é gratuito e o NPC pode ser enfrentado de novo.
- **O que os Mestres ensinam:**
  - Qualquer golpe compartilhado, mas nunca os hereditários.
  - 11 golpes são ensináveis, mas ainda não têm aprendiz compatível.
- **Parceiros provisórios (elenco v1.0):**

  | Mestre | Parceiros |
  |---|---|
  | Braseiro | #001 Pirococó, #012 Salambrasa |
  | Maré | #002 Cocórrego, #008 Axococó |
  | Verdejar | #003 Esporocó, #011 Espinhocó |
  | Cascalho | #004 Cocórak, #007 Taturico |
  | Ventania | #005 Cocórion, #010 Morcegalo |
  | Faísca | #006 Cocórvolt, #009 Vagaló |
  | Terreiro | variável |

- **Sistemas ligados aos Mestres:**
  - IA dos Mestres: demonstra o golpe na primeira oportunidade e depois se adapta taticamente.
  - Diário dos Mestres: 5 telas na RoosterTeca.
  - Rumores e Exploração: aldeões vanilla dão pistas, sem coordenadas.

## 9. Pendências reais (`current_issues` e limites declarados)

- **Arte e modelo:** faltam as artes de #019 e #020 e o modelo r82 (R12).
- **Progressão:** a curva 1–49 e o HP de referência ainda são candidatos (R13).
- **Migração para o mod:** está bloqueada no runtime (R14). O núcleo histórico tem 12 espécies, e 141 quarentenas técnicas foram preservadas.
- **Golpes:** os 660 vínculos aprendíveis são "candidatos técnicos". Os IDs não são entidades executáveis aprovadas (R15).
- **Reprodução:**
  - Faltam os gatilhos completos dos gêmeos especiais e os critérios ambientais da Etapa 02 (R16, U06).
  - A Herança de Bico entre espécies está pendente (U01).
  - As etapas 03, 05 e 06 estão incompletas (U02). A Etapa 07 V1.1 é design aprovado.
- **Quetzacocó:** falta distribuir os 30 golpes por nível e treino (U03).
- **Outros:**
  - Maestria Elemental: texto integral não recuperado (U04).
  - Integração automática a cada implementação (U05).
- **Fora do `current_issues`:** fórmula de dano definitiva e runtime Fabric/GeckoLib.

### Inconsistências encontradas nesta leitura (para conferir)
- **Rótulo de nível — CORRIGIDO em 18/11/2026, com confirmação do criador:**
  - A referência dos atributos-base é o **nível 50**.
  - As 29 fichas oficiais que traziam o rótulo antigo "nível 100" ganharam cópias corrigidas em `docs/acervo_corrigido/`, com os números conferidos contra a base. Os detalhes estão em `docs/ERRATA_NIVEL_50.md`.
  - Os originais do Release seguem preservados como histórico.
  - Ao conferir uma ficha, use a cópia corrigida ou a base vigente.
- **Total do Quetzacocó:** 700 no nível 50, acima da faixa Lendário (590–630). A raridade registrada é "Lendário Original", que não tem faixa definida na norma de progressão.
- **Mestres Elementais:** os documentos de 10/11 citam "11/12 espécies" e "302 vínculos", números anteriores ao catálogo atual de 23 espécies. No v1.1, Braseiro aparece com Pirococó, Cocórak e Cocórion. Depois, o Elenco provisório definiu Pirococó e Salambrasa.
- **Loader do mod:** as atas e os documentos dos Mestres falam em "Java/NeoForge", mas o código real usa **Fabric + GeckoLib**, como a base vigente também registra.

## 10. Repositório (código e modelos)

### Mod (`galetocraft/`)
- **Plataforma e versões:**
  - Fabric, Minecraft **1.21.11**, Fabric Loader 0.20.1, Fabric API 0.141.6+1.21.11 e GeckoLib 5.4.5.
  - Loom 1.19-SNAPSHOT, mapeamentos oficiais da Mojang.
  - O mod compila para Java 21, mas o Gradle precisa de JDK 25.
- **Identidade:** mod id `galetocraft`, pacote `br.galetocraft`, versão 0.1.0.
- **Build:** `gradlew build` gera `build/libs/galetocraft-0.1.0.jar`. O último `build.log` terminou em BUILD SUCCESSFUL.
- **O que está implementado:**
  - **12 entidades**:
    - O Pirococó tem classe própria, `PirococoEntity`.
    - As outras 11 usam a classe genérica `GaloEntity`: Esporocó, Cocórak, Cocórion, Cocórvolt, Taturico, Axococó, Vagaló, Morcegalo, Espinhocó, Salambrasa e Renacocó.
    - Comportamento: mobs neutros com ataque corpo a corpo e sons de galinha vanilla.
    - Animações GeckoLib só de `idle` e `walk`.
  - **Itens:** 12 ovos geradores.
  - **Renderização:** `GaloRenderer` com LOD por distância (16/32/48 blocos) e uma camada de brilho parcial por glowmask.
  - **Testes de cliente** (source set `gametest`): fotos do Pirococó, galeria e benchmark.
- **O que NÃO existe no código:**
  - Rinha, captura, energia, golpes, elementos, comandos, blocos, spawn natural, loot, receitas e sons próprios.
  - Hoje o mod é uma vitrine de modelos. Todo o design da base vigente ainda precisa ser implementado.
- **Espécies sem entidade:** #002 Cocórrego, #013–#018 e #020–#023.

### Modelos (`modelos/`) e ferramentas (`ferramentas/`)
- **Rodada oficial de cada modelo:**

  | Espécie | Rodada |
  |---|---|
  | Pirococó | g09 |
  | Renacocó | r82 |
  | Vagaló | v58 |
  | Cocórvolt | n74 |
  | Axococó | n69 |
  | Cocórion | c37 |
  | Taturico | n63 |
  | Morcegalo | n58 |
  | Salambrasa | n51 |
  | Espinhocó | n49 |
  | Esporocó | n46 |
  | Cocórak | k8 |

- **Gerar e exportar um modelo:**
  1. `ferramentas/especies/<id>.py` gera o modelo, usando a biblioteca `galo_base.py`.
  2. `exportar_especie.py <id>` exporta para os assets do mod. Ele usa `otimizar_bb.py` e gera os ossos `_brilho` e `_lod`.
- **Ferramentas de apoio:**
  - `rodada_revisao.py` congela uma rodada.
  - `comparar_ficha.py` mede o IoU da silhueta e as cores contra as vistas da ficha.
  - `dimensoes.py` guarda as alturas oficiais.
  - Os prompts de agentes ficam em `ferramentas/especies/` (BRIEFING, REFAZER, REVISAO, JUIZ e AUDITORIA).
- **Dependências e ambiente:** Python com Pillow e numpy. Alguns scripts têm caminhos fixos do Windows (`C:\Users\gbriel\Desktop\galopiru`).
- **Auditorias de fidelidade:** os modelos receberam notas entre 4 e 6 de 10, puxadas sobretudo pelo rosto.
- **Pirococó:** passou por 3 fichas, com as séries p (RoosterTeca), q18 (Galetário, armadura prata) e **g09** (Galetário 2, armadura roxa, que é a vigente).
- **`referencias/`:** fichas, artes, vistas e expressões das espécies modeladas, mais especificações em texto do Cocórion e do Renacocó.

### Benchmark e Git LFS
- **`benchmark/`:** CSVs de 9 a 11/11, ainda com um modelo de Pirococó anterior ao g09.
  - 100 Pirococós na máquina atual: cerca de 90 FPS. O modelo antigo dava 35 FPS, então a otimização rendeu cerca de 2,6×.
  - O gargalo é o cliente: o MSPT fica abaixo de 8 ms.
- **Git LFS** cobre `modelos/*/revisao/**` (png, bbmodel, bak) e `benchmark/**/*.png`.
  - Nesta cópia há só ponteiros: 5.783 arquivos, cerca de 2,4 GB não baixados.

### Pendências técnicas no repositório
- **Licença:** o arquivo `LICENSE` é CC0, mas o `fabric.mod.json` declara "All-Rights-Reserved".
- **Documentação desatualizada:**
  - O `LEIAME.md` ainda descreve o fluxo antigo (`pirococo6.py` com `exportar_geckolib.py`).
  - O `teste.log` é antigo.
  - Alguns comentários e logs do Pirococó e do Vagaló descrevem versões anteriores.
- **Glowmasks vazias:** Axococó, Cocórion, Espinhocó e Taturico. Por inferência a partir do código, a camada de brilho redesenha o modelo inteiro sem necessidade nesses casos.
- **Propriedade intelectual:** a pasta `galos_monstro/` (protótipo fora do mod) se declara inspirada em Pokémon. Convém não levá-la para o jogo.

## 11. Acervo do Release `acervo-documental-2026-11-17`

- **Conteúdo:**
  - 1.636 arquivos, 11,4 GB, dos quais 1.182 hashes são únicos.
  - Distribuídos em 15 ZIPs independentes: `00_Base_Vigente` e `01`–`14_Acervo`.
  - Para reconstruir, extrair todos na mesma pasta.
- **Arquivos soltos:** `INVENTARIO_GALETOCRAFT.json` (caminho, tamanho, SHA-256 e pacote de cada arquivo), `DADOS_VIGENTES_CONSULTA.json` (exportação legível da camada atual) e `SHA256SUMS.txt`.
- **Tipos de arquivo:** 472 .md, 366 .json, 247 .png, 197 .sqlite (7,3 GB de Betas e ramos históricos), 191 .zip, 66 .py e 52 .csv. Também há 2 .jar com os motores Java isolados da Mira V1.4 e V1.5.
- **Pastas principais** dentro de `Galetocraft/`:
  - Base_Atual
  - Galetario (fichas oficiais por espécie)
  - GalolpeTecas
  - RoosterTeca
  - Sistemas_Oficiais (atas de Concentração, Golpe Duplo, Mira, Nexo, Progressão, Reprodução e Tipagem Dupla)
  - Mestres_Elementais, IA_Mestres_Elementais, Balanceamento_Mestres, Diario_dos_Mestres e Rumores_Exploracao
  - Implementacoes_Experimentais (motores Python/Java isolados)
  - Estudos_Balanceamento
  - Arquivo_Historico
  - Atualizacao_007–012
  - Propostas_em_revisao
  - Auditorias_Horarias
- **Raiz do acervo:** 1.237 arquivos soltos, incluindo artes, fichas e cópias.
- **Exemplo — Sirenocó:**
  - A "Ficha Oficial de Sirenocó #022.png" e o `Galetario_022_Sirenoco_OFICIAL_2026-11-13.md` estão no pacote 01.
  - A arte aprovada está no pacote 04.

## 12. Glossário rápido

- **Cocorídeo / Galeto:** a criatura do jogo.
- **Rinha:** batalha por turnos.
- **Pena:** item de captura. Não confundir com a Pena de Ritmo da Concentração.
- **Ala:** grupo de reprodução.
- **Herança de Bico:** herança de golpe exclusivo.
- **Homologado / oficial:** aprovado pelo criador. Isso não significa implementado.
- **Candidato / proposta / histórico:** sem autoridade vigente.
- **E:** custo de Energia. **P:** poder.
- **Galetário / Galolpédia / RoosterTeca:** espécies, golpes e coleção do jogador.

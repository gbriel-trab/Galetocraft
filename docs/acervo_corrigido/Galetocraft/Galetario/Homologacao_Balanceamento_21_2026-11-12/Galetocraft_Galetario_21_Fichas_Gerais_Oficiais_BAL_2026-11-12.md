# GALETOCRAFT — GALETÁRIO OFICIAL CONSOLIDADO · 21 COCORÍDEOS

**Homologação:** 12/11/2026 · **Registro:** Balanceamento oficial R1 após testes V2/V3 de Rinhas 4×4.

**Aprovação expressa:** “todos os ajustes de balanceamento feitos hoje estão aprovados em geral, oficialize a mudança nas fichas gerais”.

Este registro torna vigentes os **seis microajustes finais da V3**, preservando os valores da V2 como históricos quando foram diferentes. O usuário aprovou a atualização do catálogo, não a alteração de artes, golpes, atributos, pesos ou implementações executáveis.

**Regra de precedência:** V3 substitui V2 apenas nos parâmetros em que houve duas propostas; todas as regras não afetadas permanecem as das homologações anteriores.

O banco histórico Beta 1.2.58 contém 12 espécies em sua tabela original: o novo adendo reúne as 21 fichas aprovadas em tabelas próprias sem falsificar a inclusão retroativa no legado.

## Resumo das mudanças homologadas

| Nº | Espécie | Parâmetro | Valor anterior | Valor vigente |
|---:|---|---|---|---|
| 019 | Renacocó | cura própria ao fim do turno ativo | 10% HP máximo | **9% HP máximo** |
| 010 | Morcegalo | amplificação do dano contra Presa Localizada | 20% | **19%** |
| 020 | Frankocó | blindagem única, baseada em HP máximo | 15% HP máximo | **14% HP máximo** |
| 017 | Castorocó | bônus de Defesa Mágica após gatilho | +15% | **+17%** |
| 018 | Mariposocó | recuperação de energia após gatilho | 10 pontos | **12 pontos** |
| 021 | Cabacocó | perda periódica de HP e redução de cura | 4% HP máximo/turno; -50% cura | **3,5% HP máximo/turno; -45% cura** |

---

# GALETOCRAFT — GALETÁRIO OFICIAL #001 Pirococó

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Mítico · **Elementos:** Fogo · **Peso natural registrado:** 5,8 kg

**Fonte anterior:** `Galetario_Oficial_15_Fichas_Consolidadas_2026-11-11.json | ficha 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 90 |

| Ataque Físico | 35 |

| Defesa Física | 60 |

| Ataque Mágico | 185 |

| Defesa Mágica | 95 |

| Velocidade | 85 |

| **Total calculado** | **550** |

## Passiva oficial vigente

**Passiva: Chama Reencarnada**

Parâmetros completos (mantidos em sua estrutura original):

```json
{
  "ativacoes_maximas_por_combate": 1,
  "bonus_ataque_magico": 0.2,
  "bonus_removido_ao_sair_campo": true,
  "duracao_bonus_acoes_executadas": 3,
  "hp_ressurreicao_fracao_hp_maximo": 0.15,
  "nao_concede_segundo_golpe_apos_ko_antes_ressurreicao": true,
  "remove_status_negativo": true
}
```

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| crina_poderosa | Crina Poderosa | Neutro | mágico | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| concentracao | Concentração | — | suporte | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| cococombustao | Cocócombustão | Fogo | mágico | 70 | 30 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| penas_de_brasa | Penas de Brasa | Fogo | mágico | 100 | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| ave_fenix | Ave Fênix | Fogo | mágico | 180 | 100 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G006 | Faísca de Terreiro | Fogo | mágico | 40 | 0 | Se Ensolarado estiver ativo, o projétil básico tem 15% de chance de reduzir Ataque Mágico do alvo em 8% por 1 ação; caso contrário, dano normal. |

| G007 | Sopro de Cinzas | Fogo | mágico | 65 | 30 | Acertar inimigo sob Chuva causa poder 80 em vez de 65; se não chover, 20% de chance de Queimadura após dano. |

| G008 | Rosácea de Fagulhas | Fogo | mágico | 85 | 40 | Se o alvo tiver bônus positivo de Ataque Mágico, reduz esse bônus pela metade durante o cálculo do dano deste golpe; não remove o bônus depois. |

| G009 | Coração de Fornalha | Fogo | mágico | 110 | 55 | Após causar dano, se o usuário tiver menos de 50 de energia, recebe +10% de Defesa Mágica até sua próxima ação; não acumula. |

| G010 | Estouro de Magma | Fogo | mágico | 130 | 75 | Se Ensolarado estiver ativo, tem 25% de chance de Queimadura; sem Ensolarado, caso cause dano, reduz a energia do alvo em 10, uma vez por ação. |

| G011 | Chamado do Meio-Dia | Fogo | suporte | — | 30 | Invoca Ensolarado por 4 rodadas; se substituir Chuva, concede +10% de Defesa Mágica ao usuário até sua próxima ação. |

| G012 | Retorno de Cinzas | Fogo | suporte | — | 35 | Até o próximo ataque físico direto recebido, reduz seu dano em 20%; se o acerto for o segundo da mesma ação, devolve 25% do dano efetivamente sofrido nesse segundo acerto. |

| G013 | Cinzas da Discórdia | Fogo | suporte | — | 35 | Reduz Ataque Físico do alvo em 12% por suas 2 próximas ações; se ele estiver Queimado, em vez disso reduz 18%, sem acumular. |

| G014 | Reacender | Fogo | suporte | — | 40 | Cura 18% do HP máximo próprio; sob Ensolarado remove também Queimadura do próprio usuário, se existir. |

| G117 | Manto da Fornalha | Fogo | Suporte | — | 75 | Exige Ensolarado ativo; concede +30% às duas Defesas por 2 ações próprias; a primeira tentativa de causar Queimadura no usuário durante esse tempo não altera seu estado, e consome só a proteção contra Queimadura. |

| G119 | Coração de Duas Chamas | Fogo | Suporte | — | 85 | Exige Ensolarado ativo; eleva Ataque Físico e Ataque Mágico em 28% por 1 ação; após qualquer golpe ofensivo que cause dano, perde 8% do HP máximo próprio, sem reduzir abaixo de 1 HP. |

| G131 | Cinza nos Olhos | Fogo | Suporte | — | 65 | Exige Ensolarado ativo; reduz Ataque Mágico do alvo em 25% por 1 ação; contra alvo Queimado, redução cai para 12% e dura 2 ações, sem novo estado. |

| N002 | Cinza Desarmadora | Fogo | mágico | 70 | 45 | Após ao menos um acerto com dano, elimina um bônus temporário positivo de Ataque Mágico do alvo, se houver, escolhendo o mais forte; em empate, o mais antigo. O dano deste golpe é calculado antes da remoção. |

| N003 | Fornalha Resguardada | Fogo | suporte | — | 40 | Remove Queimadura do próprio usuário, caso exista, e concede +20% de Defesa Mágica por suas próximas duas ações próprias. Se não estiver Queimado, concede apenas a proteção. |

| N004 | Brilho de Carvão | Fogo | mágico | 80 | 45 | Se o clima Ensolarado estiver ativo no momento do primeiro acerto com dano, o usuário recupera 15 pontos de energia após a ação, respeitando o máximo de 100. |

| G062 | Sopro Circular | Ar | mágico | 40 | 0 | Quando Ventania estiver ativa, projétil básico tem poder 55 em vez de 40; caso contrário permanece básico sem efeito. |

| G063 | Assobio Rasante | Ar | mágico | 65 | 25 | Após causar dano reduz Ataque Mágico em 8% por 2 ações; se o alvo estiver sob uma proteção de Suporte, a redução é de 12% por apenas 1 ação. |

| G066 | Aurora do Zênite | Ar | mágico | 130 | 70 | Se o alvo recebeu um segundo golpe desde sua última ação, poder 150 em vez de 130; caso contrário, 10% de chance de Tonto após dano. |

| G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. |

| G070 | Redemoinho de Penas | Ar | suporte | — | 45 | Instala armadilha persistente que reduz o Ataque Físico do entrante voluntário em 12% por 2 ações; sob Ventania reduz em 15% por 1 ação, sem acumular. |

| G114 | Tempestade Interior | Ar | Suporte | — | 70 | Exige Ventania ativa; concede +25% Velocidade e +15% Ataque Físico por 2 ações; o primeiro segundo acerto executado durante o efeito ignora somente 10% de bônus temporários de Defesa Física adversária. |

| N019 | Pena de Eco | Ar | mágico | 85 | 40 | Se o primeiro ataque deste golpe for totalmente evitado por esquiva do alvo, devolve 15 pontos de energia ao usuário ao terminar a ação (máximo 100). |

| G093 | Grito Harmônico | Neutro | mágico | 90 | 40 | Após causar dano reduz Ataque Mágico em 12% por 1 ação; se Ventania estiver ativa, a redução passa para 8% por 2 ações. |

| G097 | Cuidado de Plumagem | Sem elemento | suporte | — | 40 | Cura 18% do HP máximo de um aliado vivo, inclusive reserva; se o aliado estiver Envenenado, a cura sobe para 22%, mas não remove o estado. |

| G002 | Espora Incandescente | Fogo | físico | 65 | 30 | Após causar dano, 20% de chance de Queimadura; se o alvo já estiver Queimado, reduz sua Defesa Física em 8% pelas próximas 2 ações dele, sem acumular. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #002 Cocórrego

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Mítico · **Elementos:** Água · **Peso natural registrado:** 8,0 kg

**Fonte anterior:** `Galetario_Oficial_15_Fichas_Consolidadas_2026-11-11.json | ficha 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 155 |

| Ataque Físico | 45 |

| Defesa Física | 135 |

| Ataque Mágico | 45 |

| Defesa Mágica | 105 |

| Velocidade | 65 |

| **Total calculado** | **550** |

## Passiva oficial vigente

**Passiva: Maré de Refluxo**

Parâmetros completos (mantidos em sua estrutura original):

```json
{
  "passive": {
    "effects": {
      "direct_damage_reduction": {
        "damage_categories": [
          "physical",
          "magical"
        ],
        "includes_second_attack_if_allowed": true,
        "normal_fraction": 0.1,
        "per_valid_direct_hit": true,
        "rain_fraction": 0.15
      },
      "energy_recovery": {
        "does_not_trigger_on": [
          "miss",
          "zero_damage",
          "indirect_status_damage"
        ],
        "energy_cap": 100,
        "maximum_triggers_per_enemy_action": 1,
        "normal_points": 20,
        "rain_points": 30,
        "trigger": "survive enemy offensive action involving positive direct damage"
      },
      "rain_regeneration": {
        "capped_at_max_hp": true,
        "energy_cost": 0,
        "fraction_of_max_hp": 0.05,
        "requires_active_on_field": true,
        "requires_alive": true,
        "rounding": "not independently specified",
        "trigger": "end of each round while Rain is active",
        "works_in_reserve": false,
        "works_without_rain": false
      }
    },
    "name": "Maré de Refluxo",
    "revide_das_mares_interaction": {
      "damage_reductions": "successive",
      "previously_approved_move_effects_unchanged": true
    }
  },
  "source": "RoosterTeca_002_Cocorrego_Passiva_Mare_de_Refluxo_v4_OFICIAL.json",
  "version": "4.0"
}
```

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| garra_afiada | Garra Afiada | Neutro | físico | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| concentracao | Concentração | — | suporte | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| revide_das_mares | Revide das Marés | — | contra-ataque | — | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| prisao_abissal | Prisão Abissal | Água | mágico | 65 | 75 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| punho_da_fortaleza | Punho da Fortaleza | Água | físico | 90 | 50 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G015 | Bico de Marola | Água | físico | 40 | 0 | Se o usuário estiver Afogado, poder sobe de 40 para 55 no primeiro acerto; não reduz nem remove Afogamento. |

| G016 | Cauda de Ressaca | Água | físico | 60 | 25 | Após causar dano, reduz Velocidade do alvo em 12% por 2 ações; sob Chuva, reduz apenas 8%, mas recupera 10 de energia ao final da ação. |

| G017 | Pancada de Maré | Água | físico | 80 | 35 | Se o alvo entrou voluntariamente neste turno, poder sobe de 80 para 100; caso contrário, após causar dano ignora o próximo efeito de redução de Velocidade do usuário até sua próxima ação. |

| G018 | Açoite de Corredeira | Água | físico | 95 | 50 | Após causar dano, 18% de chance de Afogamento; se o alvo já estava Afogado, em vez de tentar aplicar o estado drena 12 de energia. |

| G019 | Quebra-Cais | Água | físico | 120 | 55 | Contra alvo com mais de 70 de energia, poder 135 em vez de 120; após causar dano nessa condição, o usuário não pode receber bônus temporário de Velocidade até sua próxima ação. |

| G020 | Gota Disparada | Água | mágico | 40 | 0 | Se o usuário recebeu cura desde sua ação anterior, poder 55 em vez de 40; não ativa curas adicionais. |

| G022 | Coluna de Espuma | Água | mágico | 80 | 40 | Após causar dano tem 20% de chance de Afogamento; se o usuário possuir bônus temporário de Defesa Mágica, a chance cai para 10%, mas poder sobe para 95. |

| G023 | Vórtice Azul | Água | mágico | 100 | 50 | Se o inimigo já tiver Ataque Físico reduzido, poder 115 em vez de 100; caso contrário aplica −12% de Ataque Físico por 2 ações após dano. |

| G024 | Tsunami de Bolhas | Água | mágico | 130 | 70 | Sob Chuva, poder 145 em vez de 130; sem Chuva, após causar dano, 15% de chance de reduzir Velocidade do alvo em 15% por 1 ação. |

| G025 | Canto das Nuvens | Água | suporte | — | 30 | Invoca Chuva por 4 rodadas; caso substitua Ensolarado, cura 8% do HP máximo próprio sem afetar a reserva. |

| G026 | Névoa Protetora | Água | suporte | — | 30 | O aliado escolhido recebe −25% de dano mágico na próxima ação ofensiva recebida; se já estiver Afogado, recupera 12 de energia ao ativar a barreira. |

| G027 | Maré de Retirada | Água | suporte | — | 40 | Troca voluntariamente por aliado da reserva; o entrante recupera 8% de HP máximo e não sofre redução de Velocidade de armadilha somente nessa entrada; outros efeitos de armadilha permanecem. |

| G028 | Banho Reparador | Água | suporte | — | 40 | Cura 20% do HP máximo de um aliado vivo, inclusive reserva; se o alvo estiver com menos de 30% do HP, acrescenta mais 5%, uma única vez. |

| N005 | Fôlego de Ressaca | Água | físico | 70 | 40 | Se o alvo já tiver Afogamento no início desta ação e ao menos um acerto causar dano, o usuário recupera 15 pontos de energia ao terminar a ação (máximo 100). |

| N006 | Redemoinho Exaustivo | Água | suporte | — | 45 | Instala no lado adversário uma armadilha persistente que retira 15 pontos da energia atual de cada Cocorídeo que entra por troca voluntária, nunca abaixo de zero. |

| N007 | Banho Sereno | Água | suporte | — | 45 | Recupera 10% do HP máximo do usuário ativo e remove o estado negativo persistente que ele tenha, se houver. |

| N008 | Pressão do Manancial | Água | mágico | 70 | 45 | Poder 95, em vez de 70, se o alvo tiver 40 ou menos pontos de energia atual no momento do cálculo do primeiro acerto. |

| G044 | Marreta de Barro | Terra | físico | 65 | 30 | Após dano reduz Velocidade em 15% por 2 ações; se uma Tempestade de Areia estiver ativa, duração cai para 1 ação e reduz também Defesa Física em 8%. |

| G054 | Muralha Escavada | Terra | suporte | — | 35 | Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. |

| G056 | Pedra de Revezamento | Terra | suporte | — | 35 | Troca usuário por aliado da reserva; o entrante recebe +15% de Defesa Física pelas próximas 2 ações e, sob Tempestade de Areia, ignora o dano de uma armadilha apenas na entrada da troca. |

| G102 | Couraça do Subsolo | Terra | Suporte | — | 45 | Eleva Defesa Física do usuário em 22% por 2 ações próprias; se estiver acima de 120% do peso natural, reduz também em 10% o dano do primeiro acerto físico recebido. |

| N013 | Pisada de Lastro | Terra | físico | 75 | 45 | Poder 100, em vez de 75, se o peso do usuário for igual ou superior a 120% de seu peso natural de referência no retrato de início da Rinha. |

| N014 | Coluna de Guarda | Terra | suporte | — | 40 | O próximo ataque direto recebido pelo próprio usuário ativo terá 20%, em vez de 10%, de chance de ativar a defesa especial, SOMENTE se a Defesa relevante for pelo menos 120% do Ataque correspondente. A redução ao ativar continua 75%. |

| G097 | Cuidado de Plumagem | Sem elemento | suporte | — | 40 | Cura 18% do HP máximo de um aliado vivo, inclusive reserva; se o aliado estiver Envenenado, a cura sobe para 22%, mas não remove o estado. |

| G100 | Terreiro Purificado | Sem elemento | suporte | — | 45 | Remove integralmente todas as armadilhas e cargas do lado do usuário; se pelo menos uma armadilha foi removida, recupera 10 de energia após a execução. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #003 Esporocó

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Mítico · **Elementos:** Planta · **Peso natural registrado:** 5,0 kg

**Fonte anterior:** `Galetario_Oficial_15_Fichas_Consolidadas_2026-11-11.json | ficha 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 120 |

| Ataque Físico | 25 |

| Defesa Física | 65 |

| Ataque Mágico | 115 |

| Defesa Mágica | 145 |

| Velocidade | 80 |

| **Total calculado** | **550** |

## Passiva oficial vigente

**Passiva: Simbiose Venenosa**

Parâmetros completos (mantidos em sua estrutura original):

```json
{
  "cura_fracao_hp_maximo_por_ocorrencia_dano_veneno": 0.1,
  "exige_em_campo": true,
  "limite_ativacoes_por_rodada": null,
  "nao_ultrapassa_hp_maximo": true,
  "resistencia_extra_fogo": false,
  "resistencia_extra_terra": false
}
```

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| crina_poderosa | Crina Poderosa | Neutro | mágico | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| concentracao | Concentração | — | suporte | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| esporos_venenosos | Esporos Venenosos | Planta | mágico | 70 | 40 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| polen_revigorante | Pólen Revigorante | — | cura | — | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| jardim_da_discordia | Jardim da Discórdia | — | suporte | — | 80 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G034 | Semente Atirada | Planta | mágico | 40 | 0 | Se Santuário das Raízes estiver ativo, concede 5 de energia ao usuário após causar dano; caso contrário, ataque mágico básico normal. |

| G035 | Perfume Ácido | Planta | mágico | 60 | 25 | Após dano tem 20% de Envenenamento; se o alvo estiver sob Santuário das Raízes e já Envenenado, em vez disso reduz Ataque Mágico em 8% por 1 ação. |

| G036 | Néctar Corrosivo | Planta | mágico | 80 | 40 | Após causar dano reduz Defesa Mágica em 12% por 2 ações; se atingir alvo com bônus positivo de Defesa Mágica, remove primeiro o bônus mais recente, sem aplicar a redução. |

| G037 | Espiral de Clorofila | Planta | mágico | 100 | 45 | Se o usuário curou um aliado da reserva desde sua última ação, poder 120 em vez de 100; de outro modo, concede 8 de energia ao usuário após dano sob Santuário das Raízes. |

| G038 | Chuva de Folhas-Lança | Planta | mágico | 125 | 75 | Após causar dano, 20% de Envenenamento; se já estiver Envenenado, transfere uma redução temporária de Ataque Mágico do usuário para o alvo, caso exista, sem duplicá-la. |

| G039 | Hino das Raízes | Planta | suporte | — | 35 | Invoca Santuário das Raízes por 4 rodadas; se uma armadilha inimiga estiver ativa, reduz em 10% o dano da próxima entrada de um aliado por troca voluntária, sem remover a armadilha. |

| G040 | Armadilha de Pólen | Planta | suporte | — | 45 | Instala armadilha persistente que reduz o Ataque Mágico do entrante voluntário em 12% por suas 2 próximas ações; se já estiver Envenenado, reduz 18% em vez disso, sem acumular. |

| G041 | Fotossíntese de Poleiro | Planta | suporte | — | 45 | Cura 20% do HP máximo de um aliado vivo; no Santuário das Raízes, cura também 5% do HP máximo do usuário ativo quando o alvo for outro aliado. |

| G042 | Casca Compartilhada | Planta | suporte | — | 30 | Concede ao aliado selecionado −20% dano mágico na próxima ação ofensiva recebida; se a ação tiver segundo acerto, nele a proteção sobe para 35%. |

| G109 | Seiva de Ferro | Planta | Suporte | — | 60 | Eleva as duas Defesas próprias em 18% por 2 ações; no Santuário das Raízes, a primeira redução de atributo recebida é ignorada, sem impedir estados negativos. |

| G113 | Pétalas de Conquista | Planta | Suporte | — | 70 | Exige Santuário das Raízes ativo; concede +22% Ataque Mágico e +15% Defesa Física por 2 ações próprias; a próxima cura própria não pode ultrapassar 15% do HP máximo proveniente deste bônus. |

| G121 | Resina nas Articulações | Planta | Suporte | — | 45 | Reduz Ataque Físico do alvo em 18% por 2 ações dele; se o alvo tentar um segundo acerto por Velocidade durante a redução, a penalidade é 25% apenas naquele segundo acerto. |

| G133 | Pólen Desarmônico | Planta | Suporte | — | 45 | Reduz Defesa Mágica do alvo em 18% por 2 ações; se Santuário das Raízes estiver ativo, cura 5% do HP máximo do usuário ao aplicar a redução, uma vez. |

| G138 | Raízes na Espora | Planta | Suporte | — | 55 | Exige Santuário das Raízes ativo; reduz Velocidade do alvo em 22% por 1 ação; se houver armadilha no lado dele, duração sobe para 2 ações, sem adicionar cargas de armadilha. |

| N009 | Espinho de Revezamento | Planta | físico | 75 | 45 | Poder 105, em vez de 75, contra alvo que entrou por troca voluntária neste mesmo turno, antes da execução do golpe. |

| N010 | Seiva de Retaguarda | Planta | mágico | 65 | 45 | Se Santuário das Raízes estiver ativo e ao menos um acerto causar dano, cura 8% do HP máximo do aliado vivo na reserva com menor proporção de HP atual. |

| N011 | Vinha Antirrasante | Planta | suporte | — | 40 | Protege o próprio usuário ativo contra a próxima ação ofensiva recebida: reduz 15% do dano do primeiro acerto e 60% do dano do eventual segundo acerto dessa mesma ação. |

| N012 | Casco de Bromélia | Planta | físico | 70 | 45 | Poder 95, em vez de 70, se a Defesa Física efetiva do usuário for ao menos 120% do Ataque Físico efetivo do alvo no momento da resolução. |

| G020 | Gota Disparada | Água | mágico | 40 | 0 | Se o usuário recebeu cura desde sua ação anterior, poder 55 em vez de 40; não ativa curas adicionais. |

| G021 | Orvalho Cortante | Água | mágico | 60 | 20 | Após causar dano, se Chuva estiver ativa recupera 8 de energia; se não estiver, reduz Defesa Mágica inimiga em 6% até a próxima ação do alvo. |

| G025 | Canto das Nuvens | Água | suporte | — | 30 | Invoca Chuva por 4 rodadas; caso substitua Ensolarado, cura 8% do HP máximo próprio sem afetar a reserva. |

| G026 | Névoa Protetora | Água | suporte | — | 30 | O aliado escolhido recebe −25% de dano mágico na próxima ação ofensiva recebida; se já estiver Afogado, recupera 12 de energia ao ativar a barreira. |

| G028 | Banho Reparador | Água | suporte | — | 40 | Cura 20% do HP máximo de um aliado vivo, inclusive reserva; se o alvo estiver com menos de 30% do HP, acrescenta mais 5%, uma única vez. |

| N007 | Banho Sereno | Água | suporte | — | 45 | Recupera 10% do HP máximo do usuário ativo e remove o estado negativo persistente que ele tenha, se houver. |

| G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #004 Cocórak

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Mítico · **Elementos:** Terra · **Peso natural registrado:** 10,0 kg

**Fonte anterior:** `Galetario_Oficial_15_Fichas_Consolidadas_2026-11-11.json | ficha 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 140 |

| Ataque Físico | 180 |

| Defesa Física | 80 |

| Ataque Mágico | 25 |

| Defesa Mágica | 70 |

| Velocidade | 55 |

| **Total calculado** | **550** |

## Passiva oficial vigente

**Passiva: Fúria do Deserto**

Parâmetros completos (mantidos em sua estrutura original):

```json
{
  "bonus_adicional_sob_tempestade_areia": 0.1,
  "bonus_dano_fisico": 0.3,
  "bonus_dano_fisico_tempestade_areia": 0.4,
  "clima_de_ativacao_do_bonus": "tempestade_areia",
  "condicao_bonus_climatico": "tempestade_areia_ativa_no_momento_do_uso",
  "condicoes_temporais_detalhadas": "sem_gatilho_temporal_a_passiva_e_disparada_por_golpe_fisico_ofensivo",
  "desliga_bonus_quando_clima_termina": true,
  "gatilho": "a_cada_uso_de_golpe_fisico_ofensivo_do_usuario",
  "hp_minimo_apos_sacrificio": 1,
  "limite_universal_golpes_por_acao": 2,
  "nao_acumula_entre_golpes": true,
  "nao_altera_custo_energia_ou_tipo_de_golpe": true,
  "possui_ativacao_temporal": false,
  "requer_ativacao_por_turnos": false,
  "sacrificio_antes_do_dano": true,
  "sacrificio_fracao_hp_maximo": 0.1
}
```

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| garra_afiada | Garra Afiada | Neutro | físico | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| concentracao | Concentração | — | suporte | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| punho_das_dunas | Punho das Dunas | Terra | físico | 110 | 60 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| prisao_das_areias | Prisão das Areias | Terra | — | 75 | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| sepultamento_do_deserto | Sepultamento do Deserto | Terra | físico | 200 | 100 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G043 | Chute de Cascalho | Terra | físico | 40 | 0 | Se o alvo tiver peso atual superior a 120% do natural, poder 55 em vez de 40; não altera peso. |

| G044 | Marreta de Barro | Terra | físico | 65 | 30 | Após dano reduz Velocidade em 15% por 2 ações; se uma Tempestade de Areia estiver ativa, duração cai para 1 ação e reduz também Defesa Física em 8%. |

| G045 | Cabeçada de Basalto | Terra | físico | 85 | 35 | Poder 105 em vez de 85 contra alvo com bônus positivo de Defesa Física; não remove bônus nem ignora defesa-base. |

| G046 | Pisão Sísmico | Terra | físico | 100 | 50 | Após causar dano, 20% de chance de Tonto; se o alvo já estiver Tonto, em vez de tentar novo estado reduz sua energia em 12. |

| G047 | Lança de Obsidiana | Terra | físico | 120 | 55 | Ignora 20% de bônus temporários de Defesa Física; se o usuário sofreu dano de estado desde sua última ação, poder 135 em vez de 120. |

| G053 | Tambor da Areia | Terra | suporte | — | 30 | Invoca Tempestade de Areia por 4 rodadas; se substituir Ventania, o usuário ganha 10% de Defesa Física até sua próxima ação. |

| G054 | Muralha Escavada | Terra | suporte | — | 35 | Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. |

| G055 | Ninho de Pedregulhos | Terra | suporte | — | 45 | Instala armadilha persistente que causa 8% do HP máximo do entrante voluntário; se ele estiver acima de 120% do peso natural, causa 11%, sem afetar entradas obrigatórias. |

| G056 | Pedra de Revezamento | Terra | suporte | — | 35 | Troca usuário por aliado da reserva; o entrante recebe +15% de Defesa Física pelas próximas 2 ações e, sob Tempestade de Areia, ignora o dano de uma armadilha apenas na entrada da troca. |

| G111 | Trono de Cascalho | Terra | Suporte | — | 70 | Exige Tempestade de Areia ativa; concede +25% Defesa Física e +15% Defesa Mágica por 2 ações próprias e impede que uma armadilha retire energia do usuário nesse período, sem remover armadilhas. |

| G116 | Fúria da Bigorna | Terra | Suporte | — | 65 | Eleva Ataque Físico próprio em 35% por 1 ação; enquanto o bônus durar, reduz a própria Defesa Mágica em 12%, ambos os efeitos terminando juntos e sem acumular. |

| G124 | Quebra-Ímpeto | Terra | Suporte | — | 70 | Exige alvo com estado negativo persistente; reduz seu Ataque Físico em 25% e Velocidade em 8% por 1 ação, sem reaplicar nem remover o estado. |

| G126 | Areia nos Encaixes | Terra | Suporte | — | 55 | Exige Tempestade de Areia ativa; reduz Defesa Física do alvo em 22% por 1 ação; se o alvo pesar mais de 120% do natural, duração sobe para 2 ações. |

| G128 | Fissura Absoluta | Terra | Suporte | — | 70 | Exige alvo com estado negativo persistente; reduz Defesa Física em 25% por 1 ação e impede apenas a recuperação de energia proveniente de golpes nessa ação, sem impedir regeneração universal. |

| N013 | Pisada de Lastro | Terra | físico | 75 | 45 | Poder 100, em vez de 75, se o peso do usuário for igual ou superior a 120% de seu peso natural de referência no retrato de início da Rinha. |

| N014 | Coluna de Guarda | Terra | suporte | — | 40 | O próximo ataque direto recebido pelo próprio usuário ativo terá 20%, em vez de 10%, de chance de ativar a defesa especial, SOMENTE se a Defesa relevante for pelo menos 120% do Ataque correspondente. A redução ao ativar continua 75%. |

| N015 | Cinzel Quebra-Manto | Terra | físico | 80 | 55 | Ao calcular o dano, ignora 50% apenas da parcela positiva dos bônus temporários de Defesa Física do alvo; a Defesa Física básica e demais modificadores continuam aplicados. |

| N016 | Pedra da Impaciência | Terra | mágico | 75 | 45 | Poder 100, em vez de 75, se a última ação efetivamente executada pelo alvo, antes desta, foi um golpe de Suporte (incluindo Concentração). |

| G002 | Espora Incandescente | Fogo | físico | 65 | 30 | Após causar dano, 20% de chance de Queimadura; se o alvo já estiver Queimado, reduz sua Defesa Física em 8% pelas próximas 2 ações dele, sem acumular. |

| G003 | Galope de Carvão | Fogo | físico | 85 | 35 | Se o usuário sofreu dano de armadilha desde sua última ação, poder 105 em vez de 85; acerto bem-sucedido não remove a armadilha. |

| G004 | Garra Vulcânica | Fogo | físico | 95 | 50 | Ao causar dano contra alvo com bônus positivo de Defesa Física, remove apenas o bônus mais recente e tem 15% de causar Queimadura. |

| G005 | Quebra-Forja | Fogo | físico | 115 | 65 | Atinge com poder normal e ignora 30% da parcela positiva de bônus temporários de Defesa Física do alvo; se não houver bônus, recupera 10 de energia após a ação. |

| N001 | Brasa de Rebate | Fogo | físico | 75 | 45 | Poder 100, em vez de 75, se o usuário recebeu dano físico direto desde sua última ação própria, estando ativo. Verificação na resolução; não inclui dano de estados, passivas ou armadilhas. |

| G106 | Forja das Esporas | Fogo | Suporte | — | 60 | Eleva Ataque Físico e Defesa Física próprios em 20% por 2 ações próprias; se estiver Queimado, concede apenas +25% de Defesa Física, sem anular a penalidade de Ataque da Queimadura. |

| G123 | Rugido de Sufoco | Ar | Suporte | — | 65 | Exige que alvo tenha executado golpe físico em sua última ação; reduz Ataque Físico dele em 28% por 1 ação, sem impedir novos ataques. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #005 Cocórion

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Mítico · **Elementos:** Ar · **Peso natural registrado:** 3,8 kg

**Fonte anterior:** `Galetario_Oficial_15_Fichas_Consolidadas_2026-11-11.json | ficha 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 80 |

| Ataque Físico | 155 |

| Defesa Física | 65 |

| Ataque Mágico | 30 |

| Defesa Mágica | 55 |

| Velocidade | 165 |

| **Total calculado** | **550** |

## Passiva oficial vigente

**Passiva: Dançarino dos Ventos**

Parâmetros completos (mantidos em sua estrutura original):

```json
{
  "bonus_consumido_no_primeiro_golpe_que_acertar": true,
  "bonus_nao_acumula": true,
  "bonus_proximo_golpe_fisico_que_acertar": 0.2,
  "bonus_removido_ao_sair_campo": true,
  "chance_esquiva_extra_apos_teste_universal": 0.25,
  "limite_golpes_por_acao": 2,
  "potencia_segundo_golpe_exclusiva_fracao_poder_original": 0.75
}
```

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| garra_afiada | Garra Afiada | Neutro | físico | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| concentracao | Concentração | — | suporte | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| laminas_de_vento | Lâminas de Vento | Ar | físico | 85 | 50 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| danca_dos_vendavais | Dança dos Vendavais | Ar | físico | 120 | 70 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| julgamento_dos_ceus | Julgamento dos Céus | Ar | — | 160 | 90 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G057 | Asa Riscante | Ar | físico | 40 | 0 | Se a Velocidade do usuário superar a do alvo, poder 50 em vez de 40; sem alterar a chance universal de segundo golpe. |

| G058 | Pluma de Corte | Ar | físico | 60 | 25 | Após dano reduz Defesa Física do alvo em 10% por 1 ação; se a esquiva do usuário foi ativada desde sua última ação, aumenta a redução para 15%. |

| G059 | Bicada Turbilhão | Ar | físico | 80 | 35 | Se o alvo usou Suporte na última ação dele, poder 100 em vez de 80; caso contrário recupera 5 de energia após causar dano em Ventania. |

| G060 | Rasgo de Altitude | Ar | físico | 100 | 50 | Após causar dano, 15% de Tonto; se a Velocidade do usuário for menor que a do alvo, poder 115 em vez de 100. |

| G061 | Queda do Falcão | Ar | físico | 125 | 70 | Se o usuário for pelo menos 50% mais veloz que o alvo, poder 140 em vez de 125; o ataque adicional universal continua sujeito ao bloqueio e ao limite geral. |

| G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. |

| G068 | Corrente de Evasão | Ar | suporte | — | 35 | Concede +8 pontos percentuais de esquiva ao usuário por suas próximas 2 ações; se esquivar efetivamente de um golpe, recupera 12 de energia após a ação ofensiva adversária, uma vez. |

| G069 | Túnel de Retorno | Ar | suporte | — | 35 | Troca por aliado da reserva, concedendo-lhe +15% de Velocidade por suas próximas 2 ações; se ele estiver Paralisado, concede somente +10% e não remove a Paralisia. |

| G070 | Redemoinho de Penas | Ar | suporte | — | 45 | Instala armadilha persistente que reduz o Ataque Físico do entrante voluntário em 12% por 2 ações; sob Ventania reduz em 15% por 1 ação, sem acumular. |

| G105 | Passo de Vendaval | Ar | Suporte | — | 45 | Concede +22% Velocidade por 2 ações próprias; se o usuário se esquivar completamente de golpe durante esse período, o bônus expira e ele ganha +12% Defesa Física até sua próxima ação. |

| G108 | Caçada Cortavento | Ar | Suporte | — | 60 | Eleva Ataque Físico em 18% e Velocidade em 15% por 2 ações próprias; se uma esquiva ocorrer, consome o bônus de Velocidade e cura 6% do HP máximo próprio uma vez. |

| G118 | Dança do Zênite | Ar | Suporte | — | 75 | Exige Ventania ativa; eleva Velocidade em 35% e Defesa Mágica em 15% por 2 ações; após esquiva completa, o bônus de Velocidade é removido e o usuário recupera 15 de energia, uma vez. |

| G123 | Rugido de Sufoco | Ar | Suporte | — | 65 | Exige que alvo tenha executado golpe físico em sua última ação; reduz Ataque Físico dele em 28% por 1 ação, sem impedir novos ataques. |

| N017 | Pluma Vazia | Ar | mágico | 70 | 45 | Poder 90, em vez de 70, se o peso do usuário for igual ou inferior a 100% de seu peso natural de referência no retrato de início da Rinha. |

| N018 | Vórtice de Passagem | Ar | suporte | — | 45 | Troca voluntariamente o usuário por aliado apto da reserva. Somente nessa entrada, o substituto ignora os gatilhos das armadilhas existentes no lado aliado. |

| N019 | Pena de Eco | Ar | mágico | 85 | 40 | Se o primeiro ataque deste golpe for totalmente evitado por esquiva do alvo, devolve 15 pontos de energia ao usuário ao terminar a ação (máximo 100). |

| N020 | Rasante do Azarão | Ar | físico | 70 | 45 | Poder 105, em vez de 70, se a Velocidade efetiva do alvo for igual ou superior a 150% da Velocidade efetiva do usuário no momento da execução. |

| G071 | Bicada Elétrica | Elétrico | físico | 40 | 0 | Se o alvo estiver Paralisado, poder 50 em vez de 40; não aplica Paralisia adicional. |

| G072 | Espora de Cobre | Elétrico | físico | 65 | 30 | Após dano, 18% de chance de Tonto; se o alvo já estiver Tonto, concede +8 de energia ao usuário em vez de tentar reaplicação. |

| G073 | Investida do Dínamo | Elétrico | físico | 85 | 35 | Contra alvo com menos de 30 de energia, poder 100 em vez de 85; não modifica energia do alvo. |

| G074 | Cascata de Centelhas | Elétrico | físico | 100 | 50 | Após dano reduz Defesa Física em 12% por 2 ações; sob Santuário dos Raios, reduz em 16% por 1 ação e recupera 5 de energia. |

| G002 | Espora Incandescente | Fogo | físico | 65 | 30 | Após causar dano, 20% de chance de Queimadura; se o alvo já estiver Queimado, reduz sua Defesa Física em 8% pelas próximas 2 ações dele, sem acumular. |

| G086 | Patada Rasteira | Neutro | físico | 50 | 25 | Após causar dano reduz Velocidade do alvo em 8% por 2 ações; se o usuário estiver Paralisado, efeito dura só 1 ação mas poder aumenta para 65. |

| G088 | Giro de Esporas | Neutro | físico | 85 | 35 | Após dano, reduz Defesa Física do alvo em 10% por 1 ação; se houver segundo acerto, a redução só vale depois de encerrada a ação, sem somar ativações. |

| G099 | Passo Firme | Sem elemento | suporte | — | 35 | Eleva Velocidade do usuário em 15% por 2 ações; se estava Paralisado, em vez disso recebe +10% Defesa Física por 1 ação, sem remover Paralisia. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #006 Cocórvolt

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Mítico · **Elementos:** Elétrico · **Peso natural registrado:** 5,2 kg

**Fonte anterior:** `Galetario_Oficial_15_Fichas_Consolidadas_2026-11-11.json | ficha 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 90 |

| Ataque Físico | 25 |

| Defesa Física | 55 |

| Ataque Mágico | 155 |

| Defesa Mágica | 65 |

| Velocidade | 160 |

| **Total calculado** | **550** |

## Passiva oficial vigente

**Passiva: Senhor da Tempestade**

Parâmetros completos (mantidos em sua estrutura original):

```json
{
  "ativacao_paralisia": "apos_segundo_golpe_eletrico_que_acerta_mesmo_alvo_na_mesma_acao",
  "paralisia_garantida_se_condicoes_validas": true,
  "chance_aplicacao_ao_cumprir_condicoes": 1.0,
  "requer_ambos_golpes_acertarem": true,
  "requer_alvo_vivo_apos_segundo_golpe": true,
  "nao_adiciona_golpes": true,
  "limite_universal_dois_golpes_por_acao": 2,
  "segundo_golpe_fracao_poder_original": 0.5,
  "aplicacao_restrita_ataques_tipo": "Elétrico",
  "respeita_limite_um_estado_negativo": true,
  "estado_aplicado": "Paralisia",
  "bonus_dano_ao_alvo_paralisado": 0.3,
  "bonus_aplicavel_ataques_diretos_danificantes": "todos_os_golpes_de_cocorvolt",
  "bonus_dano_aplicacao": "apos_dano_elemental_com_arredondamento_cima",
  "bonus_nao_acumula_consigo_mesmo": true,
  "bonus_valido_se_ja_paralisado_no_momento_do_calculo": true,
  "sem_bonus_retroativo_a_golpes_que_aplicaram_paralisia": true,
  "paralisia_na_reserva": "suspensa_conforme_regra_existente",
  "status": "oficial_nome_e_efeitos_aprovados"
}
```

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| crina_poderosa | Crina Poderosa | Neutro | mágico | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| concentracao | Concentração | — | suporte | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| estalo_voltaico | Estalo Voltaico | Elétrico | mágico | 65 | 35 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| palma_celeste | Palma Celeste | Neutro | mágico | 100 | 50 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| julgamento_dos_raios | Julgamento dos Raios | Elétrico | mágico | 140 | 85 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G076 | Arco de Faísca | Elétrico | mágico | 40 | 0 | Sob Santuário dos Raios, ataque básico tem poder 50 em vez de 40; não cria segundo golpe. |

| G077 | Pulso Condutor | Elétrico | mágico | 65 | 30 | Após dano, 15% de Tonto; se o alvo já estiver Paralisado, não tenta Tonto e drena 10 de energia adversária. |

| G078 | Círculo Voltaico | Elétrico | mágico | 80 | 40 | Após dano reduz Ataque Mágico do alvo em 10% por 2 ações; se o usuário tiver menos de 40 de energia após pagar o custo, devolve 8 de energia ao final da ação. |

| G079 | Rede de Relâmpagos | Elétrico | mágico | 105 | 45 | Se o alvo já sofreu redução de Velocidade, poder 125 em vez de 105; se não, 15% de chance de Paralisia após dano. |

| G080 | Ruptura de Alta Tensão | Elétrico | mágico | 130 | 75 | Sob Santuário dos Raios, poder 145 em vez de 130; fora dele, 15% de chance de Tonto após dano, sem gerar acerto adicional. |

| G081 | Cântico dos Condutores | Elétrico | suporte | — | 35 | Invoca Santuário dos Raios por 4 rodadas; se o usuário estiver Paralisado, recebe 10 de energia após a execução válida, sem remover o estado. |

| G082 | Bateria Compartilhada | Elétrico | suporte | — | 35 | Recupera 25 de energia de um aliado ativo escolhido; se o alvo tiver menos de 25 de energia antes da cura, recupera mais 5, sem ultrapassar 100. |

| G083 | Campo de Centelhas | Elétrico | suporte | — | 45 | Instala armadilha persistente que reduz Defesa Mágica do entrante voluntário em 12% pelas próximas 2 ações; se ele estiver Paralisado, reduz em 15% por 1 ação. |

| G084 | Escudo Galvânico | Elétrico | suporte | — | 35 | Concede ao aliado escolhido redução de 25% do dano mágico na próxima ação ofensiva recebida; se tiver menos de 40 de energia no impacto, redução sobe para 35%. |

| G103 | Foco Centelhante | Elétrico | Suporte | — | 45 | Concede +25% Ataque Mágico por 1 ação própria; sob Santuário dos Raios, o primeiro golpe mágico que causar dano ainda recupera 10 de energia, sem repetir por segundo acerto. |

| G110 | Descarga Sináptica | Elétrico | Suporte | — | 60 | Eleva Ataque Mágico em 18% e Velocidade em 15% por 2 ações; sob Santuário dos Raios, a primeira tentativa de reduzir a própria Velocidade não surte efeito. |

| G115 | Pico Voltaico | Elétrico | Suporte | — | 70 | Exige Santuário dos Raios ativo; concede +25% Ataque Mágico e +20% Velocidade por 2 ações; ao acertar inimigo Paralisado drena 8 de energia dele uma vez, sem novo estado. |

| G125 | Ferrugem de Espora | Elétrico | Suporte | — | 45 | Reduz Defesa Física do alvo em 18% por 2 ações; se ele tiver bônus positivo de Defesa Física, reduz somente 10% mas remove 10 de energia atual. |

| G132 | Apagão de Circuitos | Elétrico | Suporte | — | 70 | Exige alvo com estado negativo persistente; reduz Ataque Mágico em 26% por 1 ação e remove 1 bônus temporário positivo de Ataque Mágico, se presente. |

| G139 | Rede de Estática | Elétrico | Suporte | — | 65 | Exige Santuário dos Raios ativo; reduz Velocidade do alvo em 25% por 1 ação; se o alvo estiver Paralisado, reduz só 10% mas drena 12 de energia, sem acumular Paralisia. |

| G062 | Sopro Circular | Ar | mágico | 40 | 0 | Quando Ventania estiver ativa, projétil básico tem poder 55 em vez de 40; caso contrário permanece básico sem efeito. |

| G063 | Assobio Rasante | Ar | mágico | 65 | 25 | Após causar dano reduz Ataque Mágico em 8% por 2 ações; se o alvo estiver sob uma proteção de Suporte, a redução é de 12% por apenas 1 ação. |

| G065 | Cone de Vácuo | Ar | mágico | 105 | 50 | Após dano reduz Velocidade do alvo em 12% por 2 ações; sob Ventania, em vez disso recupera 10 de energia própria e reduz Velocidade em 8% por 1 ação. |

| G066 | Aurora do Zênite | Ar | mágico | 130 | 70 | Se o alvo recebeu um segundo golpe desde sua última ação, poder 150 em vez de 130; caso contrário, 10% de chance de Tonto após dano. |

| G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. |

| G114 | Tempestade Interior | Ar | Suporte | — | 70 | Exige Ventania ativa; concede +25% Velocidade e +15% Ataque Físico por 2 ações; o primeiro segundo acerto executado durante o efeito ignora somente 10% de bônus temporários de Defesa Física adversária. |

| N019 | Pena de Eco | Ar | mágico | 85 | 40 | Se o primeiro ataque deste golpe for totalmente evitado por esquiva do alvo, devolve 15 pontos de energia ao usuário ao terminar a ação (máximo 100). |

| G022 | Coluna de Espuma | Água | mágico | 80 | 40 | Após causar dano tem 20% de chance de Afogamento; se o usuário possuir bônus temporário de Defesa Mágica, a chance cai para 10%, mas poder sobe para 95. |

| G023 | Vórtice Azul | Água | mágico | 100 | 50 | Se o inimigo já tiver Ataque Físico reduzido, poder 115 em vez de 100; caso contrário aplica −12% de Ataque Físico por 2 ações após dano. |

| G071 | Bicada Elétrica | Elétrico | físico | 40 | 0 | Se o alvo estiver Paralisado, poder 50 em vez de 40; não aplica Paralisia adicional. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #007 Taturico

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Comum · **Elementos:** Terra · **Peso natural registrado:** 7,5 kg

**Fonte anterior:** `Galetario_Oficial_15_Fichas_Consolidadas_2026-11-11.json | ficha 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 85 |

| Ataque Físico | 55 |

| Defesa Física | 105 |

| Ataque Mágico | 25 |

| Defesa Mágica | 60 |

| Velocidade | 40 |

| **Total calculado** | **370** |

## Passiva oficial vigente

**Passiva: Carapaça Reativa**

Parâmetros completos (mantidos em sua estrutura original):

```json
{
  "bonus_defesa_fisica_permanente": 0.1,
  "chance_bloqueio_ataque_fisico": 0.2,
  "custo_energia_bloqueio": 0,
  "nao_acumula_com_guarda_do_tatu": true,
  "reducao_dano_fisico_no_bloqueio": 0.3,
  "tentativas_de_bloqueio_maximas_por_rodada": 1,
  "tipo": "passiva"
}
```

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| garra_afiada | Garra Afiada | Neutro | físico | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| concentracao | Concentração | — | suporte | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| impacto_blindado | Impacto Blindado | Terra | físico | 70 | 35 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| guarda_do_tatu | Guarda do Tatu | — | suporte/contra-ataque | — | 40 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| coro_das_dunas | Coro das Dunas | — | suporte | — | 35 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G043 | Chute de Cascalho | Terra | físico | 40 | 0 | Se o alvo tiver peso atual superior a 120% do natural, poder 55 em vez de 40; não altera peso. |

| G044 | Marreta de Barro | Terra | físico | 65 | 30 | Após dano reduz Velocidade em 15% por 2 ações; se uma Tempestade de Areia estiver ativa, duração cai para 1 ação e reduz também Defesa Física em 8%. |

| G045 | Cabeçada de Basalto | Terra | físico | 85 | 35 | Poder 105 em vez de 85 contra alvo com bônus positivo de Defesa Física; não remove bônus nem ignora defesa-base. |

| G046 | Pisão Sísmico | Terra | físico | 100 | 50 | Após causar dano, 20% de chance de Tonto; se o alvo já estiver Tonto, em vez de tentar novo estado reduz sua energia em 12. |

| G047 | Lança de Obsidiana | Terra | físico | 120 | 55 | Ignora 20% de bônus temporários de Defesa Física; se o usuário sofreu dano de estado desde sua última ação, poder 135 em vez de 120. |

| G053 | Tambor da Areia | Terra | suporte | — | 30 | Invoca Tempestade de Areia por 4 rodadas; se substituir Ventania, o usuário ganha 10% de Defesa Física até sua próxima ação. |

| G054 | Muralha Escavada | Terra | suporte | — | 35 | Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. |

| G055 | Ninho de Pedregulhos | Terra | suporte | — | 45 | Instala armadilha persistente que causa 8% do HP máximo do entrante voluntário; se ele estiver acima de 120% do peso natural, causa 11%, sem afetar entradas obrigatórias. |

| G056 | Pedra de Revezamento | Terra | suporte | — | 35 | Troca usuário por aliado da reserva; o entrante recebe +15% de Defesa Física pelas próximas 2 ações e, sob Tempestade de Areia, ignora o dano de uma armadilha apenas na entrada da troca. |

| G102 | Couraça do Subsolo | Terra | Suporte | — | 45 | Eleva Defesa Física do usuário em 22% por 2 ações próprias; se estiver acima de 120% do peso natural, reduz também em 10% o dano do primeiro acerto físico recebido. |

| G111 | Trono de Cascalho | Terra | Suporte | — | 70 | Exige Tempestade de Areia ativa; concede +25% Defesa Física e +15% Defesa Mágica por 2 ações próprias e impede que uma armadilha retire energia do usuário nesse período, sem remover armadilhas. |

| G126 | Areia nos Encaixes | Terra | Suporte | — | 55 | Exige Tempestade de Areia ativa; reduz Defesa Física do alvo em 22% por 1 ação; se o alvo pesar mais de 120% do natural, duração sobe para 2 ações. |

| G134 | Tremor de Cristal | Terra | Suporte | — | 55 | Exige Tempestade de Areia ativa; reduz Defesa Mágica do alvo em 23% por 1 ação; se alvo tiver bônus de Defesa Mágica, ignora apenas 10% do componente positivo desse bônus no cálculo da próxima ação ofensiva contra ele, sem removê-lo. |

| N013 | Pisada de Lastro | Terra | físico | 75 | 45 | Poder 100, em vez de 75, se o peso do usuário for igual ou superior a 120% de seu peso natural de referência no retrato de início da Rinha. |

| N014 | Coluna de Guarda | Terra | suporte | — | 40 | O próximo ataque direto recebido pelo próprio usuário ativo terá 20%, em vez de 10%, de chance de ativar a defesa especial, SOMENTE se a Defesa relevante for pelo menos 120% do Ataque correspondente. A redução ao ativar continua 75%. |

| N015 | Cinzel Quebra-Manto | Terra | físico | 80 | 55 | Ao calcular o dano, ignora 50% apenas da parcela positiva dos bônus temporários de Defesa Física do alvo; a Defesa Física básica e demais modificadores continuam aplicados. |

| N016 | Pedra da Impaciência | Terra | mágico | 75 | 45 | Poder 100, em vez de 75, se a última ação efetivamente executada pelo alvo, antes desta, foi um golpe de Suporte (incluindo Concentração). |

| G029 | Chicotada de Talos | Planta | físico | 40 | 0 | Se o alvo estiver Envenenado, poder 50 em vez de 40; não causa Envenenamento novo. |

| G031 | Arranco de Tronco | Planta | físico | 80 | 35 | Se o usuário estiver com peso até 100% do natural, poder 95 em vez de 80; com peso maior, gera +10% de Defesa Física até sua próxima ação após dano. |

| G033 | Broca de Raiz | Planta | físico | 115 | 55 | Ignora 25% de bônus temporário positivo de Defesa Física; se o alvo for protegido por barreira de suporte, poder 125 em vez de 115, sem quebrar a barreira automaticamente. |

| G042 | Casca Compartilhada | Planta | suporte | — | 30 | Concede ao aliado selecionado −20% dano mágico na próxima ação ofensiva recebida; se a ação tiver segundo acerto, nele a proteção sobe para 35%. |

| N012 | Casco de Bromélia | Planta | físico | 70 | 45 | Poder 95, em vez de 70, se a Defesa Física efetiva do usuário for ao menos 120% do Ataque Físico efetivo do alvo no momento da resolução. |

| N011 | Vinha Antirrasante | Planta | suporte | — | 40 | Protege o próprio usuário ativo contra a próxima ação ofensiva recebida: reduz 15% do dano do primeiro acerto e 60% do dano do eventual segundo acerto dessa mesma ação. |

| G016 | Cauda de Ressaca | Água | físico | 60 | 25 | Após causar dano, reduz Velocidade do alvo em 12% por 2 ações; sob Chuva, reduz apenas 8%, mas recupera 10 de energia ao final da ação. |

| G049 | Lodo Pressurizado | Terra | mágico | 65 | 30 | Após causar dano reduz Defesa Mágica em 10% por 2 ações; se o alvo estiver sob Chuva, em vez disso reduz Defesa Física em 10% por 1 ação. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #008 Axococó

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Comum · **Elementos:** Água · **Peso natural registrado:** 5,8 kg

**Fonte anterior:** `Galetario_Oficial_15_Fichas_Consolidadas_2026-11-11.json | ficha 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 95 |

| Ataque Físico | 35 |

| Defesa Física | 50 |

| Ataque Mágico | 90 |

| Defesa Mágica | 60 |

| Velocidade | 40 |

| **Total calculado** | **370** |

## Passiva oficial vigente

**Passiva: Memória das Brânquias**

Parâmetros completos (mantidos em sua estrutura original):

```json
{
  "aprovado": true,
  "ativacao": "inicio_da_proxima_acao_do_axococo",
  "limite_cura_fracao_hp_maximo_chuva": 0.1,
  "limite_cura_fracao_hp_maximo_normal": 0.08,
  "reserva_regenerativa_fracao_dano_em_chuva": 0.35,
  "reserva_regenerativa_fracao_dano_normal": 0.25,
  "reservas_nao_acumulam_indefinidamente": true,
  "sem_cura_sem_dano_previo": true,
  "sem_reviver": true,
  "trigger": "dano_inimigo_efetivamente_sofrido",
  "varios_golpes_alimentam_mesma_reserva": true
}
```

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| crina_poderosa | Crina Poderosa | Neutro | mágico | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| concentracao | Concentração | — | suporte | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| estalo_das_branquias | Estalo das Brânquias | Água | mágico | 75 | 35 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| elo_regenerativo | Elo Regenerativo | — | suporte/cura | — | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| diluvio_branquial | Dilúvio Branquial | Água | mágico | 85 | 50 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G015 | Bico de Marola | Água | físico | 40 | 0 | Se o usuário estiver Afogado, poder sobe de 40 para 55 no primeiro acerto; não reduz nem remove Afogamento. |

| G016 | Cauda de Ressaca | Água | físico | 60 | 25 | Após causar dano, reduz Velocidade do alvo em 12% por 2 ações; sob Chuva, reduz apenas 8%, mas recupera 10 de energia ao final da ação. |

| G017 | Pancada de Maré | Água | físico | 80 | 35 | Se o alvo entrou voluntariamente neste turno, poder sobe de 80 para 100; caso contrário, após causar dano ignora o próximo efeito de redução de Velocidade do usuário até sua próxima ação. |

| G018 | Açoite de Corredeira | Água | físico | 95 | 50 | Após causar dano, 18% de chance de Afogamento; se o alvo já estava Afogado, em vez de tentar aplicar o estado drena 12 de energia. |

| G019 | Quebra-Cais | Água | físico | 120 | 55 | Contra alvo com mais de 70 de energia, poder 135 em vez de 120; após causar dano nessa condição, o usuário não pode receber bônus temporário de Velocidade até sua próxima ação. |

| G020 | Gota Disparada | Água | mágico | 40 | 0 | Se o usuário recebeu cura desde sua ação anterior, poder 55 em vez de 40; não ativa curas adicionais. |

| G021 | Orvalho Cortante | Água | mágico | 60 | 20 | Após causar dano, se Chuva estiver ativa recupera 8 de energia; se não estiver, reduz Defesa Mágica inimiga em 6% até a próxima ação do alvo. |

| G022 | Coluna de Espuma | Água | mágico | 80 | 40 | Após causar dano tem 20% de chance de Afogamento; se o usuário possuir bônus temporário de Defesa Mágica, a chance cai para 10%, mas poder sobe para 95. |

| G023 | Vórtice Azul | Água | mágico | 100 | 50 | Se o inimigo já tiver Ataque Físico reduzido, poder 115 em vez de 100; caso contrário aplica −12% de Ataque Físico por 2 ações após dano. |

| G024 | Tsunami de Bolhas | Água | mágico | 130 | 70 | Sob Chuva, poder 145 em vez de 130; sem Chuva, após causar dano, 15% de chance de reduzir Velocidade do alvo em 15% por 1 ação. |

| G025 | Canto das Nuvens | Água | suporte | — | 30 | Invoca Chuva por 4 rodadas; caso substitua Ensolarado, cura 8% do HP máximo próprio sem afetar a reserva. |

| G026 | Névoa Protetora | Água | suporte | — | 30 | O aliado escolhido recebe −25% de dano mágico na próxima ação ofensiva recebida; se já estiver Afogado, recupera 12 de energia ao ativar a barreira. |

| G027 | Maré de Retirada | Água | suporte | — | 40 | Troca voluntariamente por aliado da reserva; o entrante recupera 8% de HP máximo e não sofre redução de Velocidade de armadilha somente nessa entrada; outros efeitos de armadilha permanecem. |

| G028 | Banho Reparador | Água | suporte | — | 40 | Cura 20% do HP máximo de um aliado vivo, inclusive reserva; se o alvo estiver com menos de 30% do HP, acrescenta mais 5%, uma única vez. |

| N005 | Fôlego de Ressaca | Água | físico | 70 | 40 | Se o alvo já tiver Afogamento no início desta ação e ao menos um acerto causar dano, o usuário recupera 15 pontos de energia ao terminar a ação (máximo 100). |

| N006 | Redemoinho Exaustivo | Água | suporte | — | 45 | Instala no lado adversário uma armadilha persistente que retira 15 pontos da energia atual de cada Cocorídeo que entra por troca voluntária, nunca abaixo de zero. |

| N007 | Banho Sereno | Água | suporte | — | 45 | Recupera 10% do HP máximo do usuário ativo e remove o estado negativo persistente que ele tenha, se houver. |

| N008 | Pressão do Manancial | Água | mágico | 70 | 45 | Poder 95, em vez de 70, se o alvo tiver 40 ou menos pontos de energia atual no momento do cálculo do primeiro acerto. |

| G034 | Semente Atirada | Planta | mágico | 40 | 0 | Se Santuário das Raízes estiver ativo, concede 5 de energia ao usuário após causar dano; caso contrário, ataque mágico básico normal. |

| G035 | Perfume Ácido | Planta | mágico | 60 | 25 | Após dano tem 20% de Envenenamento; se o alvo estiver sob Santuário das Raízes e já Envenenado, em vez disso reduz Ataque Mágico em 8% por 1 ação. |

| G039 | Hino das Raízes | Planta | suporte | — | 35 | Invoca Santuário das Raízes por 4 rodadas; se uma armadilha inimiga estiver ativa, reduz em 10% o dano da próxima entrada de um aliado por troca voluntária, sem remover a armadilha. |

| G041 | Fotossíntese de Poleiro | Planta | suporte | — | 45 | Cura 20% do HP máximo de um aliado vivo; no Santuário das Raízes, cura também 5% do HP máximo do usuário ativo quando o alvo for outro aliado. |

| G042 | Casca Compartilhada | Planta | suporte | — | 30 | Concede ao aliado selecionado −20% dano mágico na próxima ação ofensiva recebida; se a ação tiver segundo acerto, nele a proteção sobe para 35%. |

| N010 | Seiva de Retaguarda | Planta | mágico | 65 | 45 | Se Santuário das Raízes estiver ativo e ao menos um acerto causar dano, cura 8% do HP máximo do aliado vivo na reserva com menor proporção de HP atual. |

| G062 | Sopro Circular | Ar | mágico | 40 | 0 | Quando Ventania estiver ativa, projétil básico tem poder 55 em vez de 40; caso contrário permanece básico sem efeito. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #009 Vagaló

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Comum · **Elementos:** Elétrico · **Peso natural registrado:** 3,1 kg

**Fonte anterior:** `Galetario_Oficial_15_Fichas_Consolidadas_2026-11-11.json | ficha 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 60 |

| Ataque Físico | 25 |

| Defesa Física | 40 |

| Ataque Mágico | 15 |

| Defesa Mágica | 50 |

| Velocidade | 180 |

| **Total calculado** | **370** |

## Passiva oficial vigente

**Passiva: Código Luminescente**

Parâmetros completos (mantidos em sua estrutura original):

```json
{
  "buff_com_1_pulso": {
    "duracao_acoes_aliado": 2,
    "velocidade_pct": 0.1
  },
  "buff_com_2_pulsos": {
    "duracao_acoes_aliado": 2,
    "reducao_dano_primeiro_golpe_recebido_pct": 0.2,
    "velocidade_pct": 0.2
  },
  "buff_desaparece_se_aliado_sair_de_campo": true,
  "funcao": "Sinalizador Tático",
  "max_pulsos_acumulados": 2,
  "nao_acumula_consigomesma": true,
  "nao_ativa_quando_substituicao_apos_derrota": true,
  "nao_ativa_troca_impedida": true,
  "nome": "Código Luminescente",
  "pulso_por_acao_com_golpe_validamente_executado": 1,
  "se_acao_bloqueada_pulso": 0,
  "se_acao_tem_dois_golpes_pulso_total": 1,
  "troca_voluntaria_valida_consumo_pulsos": true,
  "trocas_por_movimento_valido_podem_acionar": true
}
```

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| garra_afiada | Garra Afiada | Neutro | físico | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| concentracao | Concentração | — | suporte | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| rele_luminoso | Relé Luminoso | Elétrico | físico | 50 | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| cortina_cintilante | Cortina Cintilante | Elétrico | suporte | — | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| choque_estatico | Choque Estático | Elétrico | físico | 20 | 40 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G076 | Arco de Faísca | Elétrico | mágico | 40 | 0 | Sob Santuário dos Raios, ataque básico tem poder 50 em vez de 40; não cria segundo golpe. |

| G077 | Pulso Condutor | Elétrico | mágico | 65 | 30 | Após dano, 15% de Tonto; se o alvo já estiver Paralisado, não tenta Tonto e drena 10 de energia adversária. |

| G078 | Círculo Voltaico | Elétrico | mágico | 80 | 40 | Após dano reduz Ataque Mágico do alvo em 10% por 2 ações; se o usuário tiver menos de 40 de energia após pagar o custo, devolve 8 de energia ao final da ação. |

| G079 | Rede de Relâmpagos | Elétrico | mágico | 105 | 45 | Se o alvo já sofreu redução de Velocidade, poder 125 em vez de 105; se não, 15% de chance de Paralisia após dano. |

| G081 | Cântico dos Condutores | Elétrico | suporte | — | 35 | Invoca Santuário dos Raios por 4 rodadas; se o usuário estiver Paralisado, recebe 10 de energia após a execução válida, sem remover o estado. |

| G082 | Bateria Compartilhada | Elétrico | suporte | — | 35 | Recupera 25 de energia de um aliado ativo escolhido; se o alvo tiver menos de 25 de energia antes da cura, recupera mais 5, sem ultrapassar 100. |

| G083 | Campo de Centelhas | Elétrico | suporte | — | 45 | Instala armadilha persistente que reduz Defesa Mágica do entrante voluntário em 12% pelas próximas 2 ações; se ele estiver Paralisado, reduz em 15% por 1 ação. |

| G084 | Escudo Galvânico | Elétrico | suporte | — | 35 | Concede ao aliado escolhido redução de 25% do dano mágico na próxima ação ofensiva recebida; se tiver menos de 40 de energia no impacto, redução sobe para 35%. |

| G103 | Foco Centelhante | Elétrico | Suporte | — | 45 | Concede +25% Ataque Mágico por 1 ação própria; sob Santuário dos Raios, o primeiro golpe mágico que causar dano ainda recupera 10 de energia, sem repetir por segundo acerto. |

| G110 | Descarga Sináptica | Elétrico | Suporte | — | 60 | Eleva Ataque Mágico em 18% e Velocidade em 15% por 2 ações; sob Santuário dos Raios, a primeira tentativa de reduzir a própria Velocidade não surte efeito. |

| G125 | Ferrugem de Espora | Elétrico | Suporte | — | 45 | Reduz Defesa Física do alvo em 18% por 2 ações; se ele tiver bônus positivo de Defesa Física, reduz somente 10% mas remove 10 de energia atual. |

| G132 | Apagão de Circuitos | Elétrico | Suporte | — | 70 | Exige alvo com estado negativo persistente; reduz Ataque Mágico em 26% por 1 ação e remove 1 bônus temporário positivo de Ataque Mágico, se presente. |

| G139 | Rede de Estática | Elétrico | Suporte | — | 65 | Exige Santuário dos Raios ativo; reduz Velocidade do alvo em 25% por 1 ação; se o alvo estiver Paralisado, reduz só 10% mas drena 12 de energia, sem acumular Paralisia. |

| G062 | Sopro Circular | Ar | mágico | 40 | 0 | Quando Ventania estiver ativa, projétil básico tem poder 55 em vez de 40; caso contrário permanece básico sem efeito. |

| G063 | Assobio Rasante | Ar | mágico | 65 | 25 | Após causar dano reduz Ataque Mágico em 8% por 2 ações; se o alvo estiver sob uma proteção de Suporte, a redução é de 12% por apenas 1 ação. |

| G066 | Aurora do Zênite | Ar | mágico | 130 | 70 | Se o alvo recebeu um segundo golpe desde sua última ação, poder 150 em vez de 130; caso contrário, 10% de chance de Tonto após dano. |

| G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. |

| G068 | Corrente de Evasão | Ar | suporte | — | 35 | Concede +8 pontos percentuais de esquiva ao usuário por suas próximas 2 ações; se esquivar efetivamente de um golpe, recupera 12 de energia após a ação ofensiva adversária, uma vez. |

| G069 | Túnel de Retorno | Ar | suporte | — | 35 | Troca por aliado da reserva, concedendo-lhe +15% de Velocidade por suas próximas 2 ações; se ele estiver Paralisado, concede somente +10% e não remove a Paralisia. |

| G070 | Redemoinho de Penas | Ar | suporte | — | 45 | Instala armadilha persistente que reduz o Ataque Físico do entrante voluntário em 12% por 2 ações; sob Ventania reduz em 15% por 1 ação, sem acumular. |

| G105 | Passo de Vendaval | Ar | Suporte | — | 45 | Concede +22% Velocidade por 2 ações próprias; se o usuário se esquivar completamente de golpe durante esse período, o bônus expira e ele ganha +12% Defesa Física até sua próxima ação. |

| N017 | Pluma Vazia | Ar | mágico | 70 | 45 | Poder 90, em vez de 70, se o peso do usuário for igual ou inferior a 100% de seu peso natural de referência no retrato de início da Rinha. |

| N018 | Vórtice de Passagem | Ar | suporte | — | 45 | Troca voluntariamente o usuário por aliado apto da reserva. Somente nessa entrada, o substituto ignora os gatilhos das armadilhas existentes no lado aliado. |

| G057 | Asa Riscante | Ar | físico | 40 | 0 | Se a Velocidade do usuário superar a do alvo, poder 50 em vez de 40; sem alterar a chance universal de segundo golpe. |

| G040 | Armadilha de Pólen | Planta | suporte | — | 45 | Instala armadilha persistente que reduz o Ataque Mágico do entrante voluntário em 12% por suas 2 próximas ações; se já estiver Envenenado, reduz 18% em vez disso, sem acumular. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #010 Morcegalo

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Comum · **Elementos:** Ar · **Peso natural registrado:** 5,2 kg

**Fonte anterior:** `Galetario_Oficial_15_Fichas_Consolidadas_2026-11-11.json | ficha 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 80 |

| Ataque Físico | 50 |

| Defesa Física | 45 |

| Ataque Mágico | 40 |

| Defesa Mágica | 90 |

| Velocidade | 65 |

| **Total calculado** | **370** |

## Passiva oficial vigente

**Passiva: Sonar Predatório**

Parâmetros completos (mantidos em sua estrutura original):

```json
{
  "beneficiarios": "toda a equipe",
  "bonus_dano_recebido": 0.19,
  "duracao": "3 ações da equipe do Morcegalo",
  "esquiva_universal_e_adicional_anuladas": true,
  "expira": [
    "duração",
    "troca/saída do alvo",
    "derrota do alvo"
  ],
  "marca": "Presa Localizada",
  "nao_acumula": true,
  "nao_e_estado_negativo_persistente": true,
  "persiste_apos_saida_morcegalo": true,
  "sem_acao_gratis": true,
  "sem_ignorar_imunidades": true,
  "tipos_dano_afetados": [
    "físico",
    "mágico",
    "contra-ataque",
    "periódico de estados negativos"
  ],
  "trigger": "entrada_valida_em_campo"
}
```

## Registro da homologação de balanceamento

- **amplificação do dano contra Presa Localizada:** 20% → **19%**. Todo o restante da marca e suas interações permanece igual.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| garra_afiada | Garra Afiada | Neutro | físico | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| concentracao | Concentração | — | suporte | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| rasante_ressonante | Rasante Ressonante | Ar | físico | 60 | 30 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| ruido_branco | Ruído Branco | Ar | suporte | — | 40 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| colapso_sonoro | Colapso Sonoro | Ar | mágico | 85 | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G057 | Asa Riscante | Ar | físico | 40 | 0 | Se a Velocidade do usuário superar a do alvo, poder 50 em vez de 40; sem alterar a chance universal de segundo golpe. |

| G058 | Pluma de Corte | Ar | físico | 60 | 25 | Após dano reduz Defesa Física do alvo em 10% por 1 ação; se a esquiva do usuário foi ativada desde sua última ação, aumenta a redução para 15%. |

| G059 | Bicada Turbilhão | Ar | físico | 80 | 35 | Se o alvo usou Suporte na última ação dele, poder 100 em vez de 80; caso contrário recupera 5 de energia após causar dano em Ventania. |

| G060 | Rasgo de Altitude | Ar | físico | 100 | 50 | Após causar dano, 15% de Tonto; se a Velocidade do usuário for menor que a do alvo, poder 115 em vez de 100. |

| G062 | Sopro Circular | Ar | mágico | 40 | 0 | Quando Ventania estiver ativa, projétil básico tem poder 55 em vez de 40; caso contrário permanece básico sem efeito. |

| G063 | Assobio Rasante | Ar | mágico | 65 | 25 | Após causar dano reduz Ataque Mágico em 8% por 2 ações; se o alvo estiver sob uma proteção de Suporte, a redução é de 12% por apenas 1 ação. |

| G064 | Espinho de Pressão | Ar | mágico | 85 | 35 | Se uma esquiva completa do usuário ocorreu no turno anterior, poder 105 em vez de 85; não concede esquiva nova. |

| G065 | Cone de Vácuo | Ar | mágico | 105 | 50 | Após dano reduz Velocidade do alvo em 12% por 2 ações; sob Ventania, em vez disso recupera 10 de energia própria e reduz Velocidade em 8% por 1 ação. |

| G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. |

| G068 | Corrente de Evasão | Ar | suporte | — | 35 | Concede +8 pontos percentuais de esquiva ao usuário por suas próximas 2 ações; se esquivar efetivamente de um golpe, recupera 12 de energia após a ação ofensiva adversária, uma vez. |

| G069 | Túnel de Retorno | Ar | suporte | — | 35 | Troca por aliado da reserva, concedendo-lhe +15% de Velocidade por suas próximas 2 ações; se ele estiver Paralisado, concede somente +10% e não remove a Paralisia. |

| G070 | Redemoinho de Penas | Ar | suporte | — | 45 | Instala armadilha persistente que reduz o Ataque Físico do entrante voluntário em 12% por 2 ações; sob Ventania reduz em 15% por 1 ação, sem acumular. |

| G105 | Passo de Vendaval | Ar | Suporte | — | 45 | Concede +22% Velocidade por 2 ações próprias; se o usuário se esquivar completamente de golpe durante esse período, o bônus expira e ele ganha +12% Defesa Física até sua próxima ação. |

| G129 | Ruído de Barragem | Ar | Suporte | — | 45 | Reduz Ataque Mágico do alvo em 18% por 2 ações; se Ventania estiver ativa, a primeira tentativa de recuperar energia por golpe do alvo é reduzida em 8 pontos. |

| G135 | Vácuo de Eco | Ar | Suporte | — | 65 | Exige Ventania ativa; reduz Defesa Mágica do alvo em 25% por 1 ação; se ele já teve esquiva completa neste turno, a redução dura 2 ações. |

| N017 | Pluma Vazia | Ar | mágico | 70 | 45 | Poder 90, em vez de 70, se o peso do usuário for igual ou inferior a 100% de seu peso natural de referência no retrato de início da Rinha. |

| N018 | Vórtice de Passagem | Ar | suporte | — | 45 | Troca voluntariamente o usuário por aliado apto da reserva. Somente nessa entrada, o substituto ignora os gatilhos das armadilhas existentes no lado aliado. |

| N019 | Pena de Eco | Ar | mágico | 85 | 40 | Se o primeiro ataque deste golpe for totalmente evitado por esquiva do alvo, devolve 15 pontos de energia ao usuário ao terminar a ação (máximo 100). |

| N020 | Rasante do Azarão | Ar | físico | 70 | 45 | Poder 105, em vez de 70, se a Velocidade efetiva do alvo for igual ou superior a 150% da Velocidade efetiva do usuário no momento da execução. |

| G092 | Eco do Cocoricó | Neutro | mágico | 40 | 0 | Se o alvo estiver Tonto, poder 50 em vez de 40; caso contrário é onda mágica básica sem status. |

| G093 | Grito Harmônico | Neutro | mágico | 90 | 40 | Após causar dano reduz Ataque Mágico em 12% por 1 ação; se Ventania estiver ativa, a redução passa para 8% por 2 ações. |

| G098 | Cocoricó Desafiador | Sem elemento | suporte | — | 35 | Reduz Ataque Físico e Ataque Mágico do inimigo em 8% pelas próximas 2 ações; se ele estiver Tonto, reduz só 5% mas devolve 10 de energia ao usuário. |

| G077 | Pulso Condutor | Elétrico | mágico | 65 | 30 | Após dano, 15% de Tonto; se o alvo já estiver Paralisado, não tenta Tonto e drena 10 de energia adversária. |

| G078 | Círculo Voltaico | Elétrico | mágico | 80 | 40 | Após dano reduz Ataque Mágico do alvo em 10% por 2 ações; se o usuário tiver menos de 40 de energia após pagar o custo, devolve 8 de energia ao final da ação. |

| G040 | Armadilha de Pólen | Planta | suporte | — | 45 | Instala armadilha persistente que reduz o Ataque Mágico do entrante voluntário em 12% por suas 2 próximas ações; se já estiver Envenenado, reduz 18% em vez disso, sem acumular. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #011 Espinhocó

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Comum · **Elementos:** Planta · **Peso natural registrado:** 6,2 kg

**Fonte anterior:** `Galetario_Oficial_15_Fichas_Consolidadas_2026-11-11.json | ficha 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 75 |

| Ataque Físico | 95 |

| Defesa Física | 85 |

| Ataque Mágico | 20 |

| Defesa Mágica | 55 |

| Velocidade | 40 |

| **Total calculado** | **370** |

## Passiva oficial vigente

**Passiva: Espinheiro Territorial**

Parâmetros completos (mantidos em sua estrutura original):

```json
{
  "passive": {
    "name": "Espinheiro Territorial",
    "per_hit_reflect_damage_pct_of_attacker_max_hp": 5,
    "reflections_per_round_cap": null,
    "status": "oficial",
    "trap": {
      "activation": "troca voluntaria do adversario",
      "damage_pct_per_stack_of_incoming_opponent_max_hp": 6,
      "mandatory_ko_switch_activates": false,
      "persists_until_opponent_removes": true,
      "round_duration_cap": null,
      "stack_cap": null,
      "stacks_added_per_hit": 1,
      "stacks_cumulative": true,
      "trigger": "cada golpe fisico direto recebido que cause dano"
    },
    "trigger": "cada golpe fisico direto recebido que cause dano, incluindo segundo golpe da ação"
  },
  "source": "Espinhoco_011_Dados_Oficiais.json"
}
```

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| garra_afiada | Garra Afiada | Neutro | físico | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| concentracao | Concentração | — | suporte | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| espinho_venenoso | Espinho Venenoso | Planta | físico | 20 | 40 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| armadilha_de_cipos | Armadilha de Cipós | Planta | suporte | — | 45 | instala armadilha persistente no campo adversario; troca voluntaria aplica -20% velocidade durante proximas duas acoes do entrante; nao acumula no mesmo alvo |

| rajada_de_espinhos | Rajada de Espinhos | Planta | físico | 95 | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G029 | Chicotada de Talos | Planta | físico | 40 | 0 | Se o alvo estiver Envenenado, poder 50 em vez de 40; não causa Envenenamento novo. |

| G030 | Ferrão de Trepadeira | Planta | físico | 55 | 25 | Após dano, 25% de chance de Envenenamento; caso o alvo já esteja Envenenado, reduz 10 de sua energia em vez de reaplicar estado. |

| G031 | Arranco de Tronco | Planta | físico | 80 | 35 | Se o usuário estiver com peso até 100% do natural, poder 95 em vez de 80; com peso maior, gera +10% de Defesa Física até sua próxima ação após dano. |

| G032 | Tesoura de Folhas | Planta | físico | 90 | 40 | Ao causar dano, 15% de Envenenamento; quando o alvo já estiver Envenenado, reduz apenas sua Defesa Física em 12% por 1 ação, sem acumular. |

| G033 | Broca de Raiz | Planta | físico | 115 | 55 | Ignora 25% de bônus temporário positivo de Defesa Física; se o alvo for protegido por barreira de suporte, poder 125 em vez de 115, sem quebrar a barreira automaticamente. |

| G039 | Hino das Raízes | Planta | suporte | — | 35 | Invoca Santuário das Raízes por 4 rodadas; se uma armadilha inimiga estiver ativa, reduz em 10% o dano da próxima entrada de um aliado por troca voluntária, sem remover a armadilha. |

| G040 | Armadilha de Pólen | Planta | suporte | — | 45 | Instala armadilha persistente que reduz o Ataque Mágico do entrante voluntário em 12% por suas 2 próximas ações; se já estiver Envenenado, reduz 18% em vez disso, sem acumular. |

| G042 | Casca Compartilhada | Planta | suporte | — | 30 | Concede ao aliado selecionado −20% dano mágico na próxima ação ofensiva recebida; se a ação tiver segundo acerto, nele a proteção sobe para 35%. |

| G121 | Resina nas Articulações | Planta | Suporte | — | 45 | Reduz Ataque Físico do alvo em 18% por 2 ações dele; se o alvo tentar um segundo acerto por Velocidade durante a redução, a penalidade é 25% apenas naquele segundo acerto. |

| G127 | Cipó Descascador | Planta | Suporte | — | 65 | Exige alvo com bônus positivo de Defesa Física; remove o menor bônus temporário positivo de Defesa Física do alvo e reduz sua Defesa Física em 8% por 1 ação, sem remover outros bônus. |

| G138 | Raízes na Espora | Planta | Suporte | — | 55 | Exige Santuário das Raízes ativo; reduz Velocidade do alvo em 22% por 1 ação; se houver armadilha no lado dele, duração sobe para 2 ações, sem adicionar cargas de armadilha. |

| N009 | Espinho de Revezamento | Planta | físico | 75 | 45 | Poder 105, em vez de 75, contra alvo que entrou por troca voluntária neste mesmo turno, antes da execução do golpe. |

| N011 | Vinha Antirrasante | Planta | suporte | — | 40 | Protege o próprio usuário ativo contra a próxima ação ofensiva recebida: reduz 15% do dano do primeiro acerto e 60% do dano do eventual segundo acerto dessa mesma ação. |

| N012 | Casco de Bromélia | Planta | físico | 70 | 45 | Poder 95, em vez de 70, se a Defesa Física efetiva do usuário for ao menos 120% do Ataque Físico efetivo do alvo no momento da resolução. |

| G043 | Chute de Cascalho | Terra | físico | 40 | 0 | Se o alvo tiver peso atual superior a 120% do natural, poder 55 em vez de 40; não altera peso. |

| G044 | Marreta de Barro | Terra | físico | 65 | 30 | Após dano reduz Velocidade em 15% por 2 ações; se uma Tempestade de Areia estiver ativa, duração cai para 1 ação e reduz também Defesa Física em 8%. |

| G045 | Cabeçada de Basalto | Terra | físico | 85 | 35 | Poder 105 em vez de 85 contra alvo com bônus positivo de Defesa Física; não remove bônus nem ignora defesa-base. |

| G046 | Pisão Sísmico | Terra | físico | 100 | 50 | Após causar dano, 20% de chance de Tonto; se o alvo já estiver Tonto, em vez de tentar novo estado reduz sua energia em 12. |

| G054 | Muralha Escavada | Terra | suporte | — | 35 | Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. |

| G055 | Ninho de Pedregulhos | Terra | suporte | — | 45 | Instala armadilha persistente que causa 8% do HP máximo do entrante voluntário; se ele estiver acima de 120% do peso natural, causa 11%, sem afetar entradas obrigatórias. |

| G102 | Couraça do Subsolo | Terra | Suporte | — | 45 | Eleva Defesa Física do usuário em 22% por 2 ações próprias; se estiver acima de 120% do peso natural, reduz também em 10% o dano do primeiro acerto físico recebido. |

| N013 | Pisada de Lastro | Terra | físico | 75 | 45 | Poder 100, em vez de 75, se o peso do usuário for igual ou superior a 120% de seu peso natural de referência no retrato de início da Rinha. |

| N014 | Coluna de Guarda | Terra | suporte | — | 40 | O próximo ataque direto recebido pelo próprio usuário ativo terá 20%, em vez de 10%, de chance de ativar a defesa especial, SOMENTE se a Defesa relevante for pelo menos 120% do Ataque correspondente. A redução ao ativar continua 75%. |

| N015 | Cinzel Quebra-Manto | Terra | físico | 80 | 55 | Ao calcular o dano, ignora 50% apenas da parcela positiva dos bônus temporários de Defesa Física do alvo; a Defesa Física básica e demais modificadores continuam aplicados. |

| G100 | Terreiro Purificado | Sem elemento | suporte | — | 45 | Remove integralmente todas as armadilhas e cargas do lado do usuário; se pelo menos uma armadilha foi removida, recupera 10 de energia após a execução. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #012 Salambrasa

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Comum · **Elementos:** Fogo · **Peso natural registrado:** 6,4 kg

**Fonte anterior:** `Galetario_Oficial_15_Fichas_Consolidadas_2026-11-11.json | ficha 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 95 |

| Ataque Físico | 90 |

| Defesa Física | 80 |

| Ataque Mágico | 25 |

| Defesa Mágica | 50 |

| Velocidade | 30 |

| **Total calculado** | **370** |

## Passiva oficial vigente

**Passiva: Pele de Brasa**

Parâmetros completos (mantidos em sua estrutura original):

```json
{
  "nome": "Pele de Brasa",
  "efeito": "A cada golpe direto recebido que cause dano válido, físico ou mágico, Salambrasa tem 20% de chance independente de aplicar Queimadura ao atacante. Não há limite de tentativas por rodada. Se receber dois golpes diretos válidos, pode testar a passiva duas vezes. Não é ativada por erro, anulação completa ou dano indireto de estado. Não aplica Queimadura se o atacante já possuir estado negativo persistente, respeitando o limite de um. Não causa dano extra.",
  "chance_por_acerto_valido_pct": 20,
  "limite_tentativas_por_rodada": null,
  "golpes_fisicos": true,
  "golpes_magicos": true,
  "danos_indiretos_de_status": false,
  "estado_aplicado": "Queimadura",
  "somente_proposta": false
}
```

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| garra_afiada | Garra Afiada | Neutro | Físico | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| concentracao | Concentração | — | Suporte | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

| G142 | Dentada de Carvão | Fogo | Físico | 65 | 35 | Golpe físico de Fogo; 20% de chance de aplicar Queimadura ao alvo, respeitando o máximo de um estado negativo persistente. |

| G143 | Armadura de Brasa | Fogo | Suporte | — | 65 | Suporte de Fogo: +50% de Defesa Física e +50% de Defesa Mágica do usuário até sair de campo ou ser derrotado. Não acumula bônus do mesmo atributo (permanece o maior). Removível por G141 Dissipação Absoluta. Consome uma ação. |

| G144 | Arrasto Magmático | Fogo | Físico | 90 | 45 | Golpe físico de Fogo; se o alvo já estiver Queimado no momento do cálculo, causa +20% de dano deste golpe. Não provoca Queimadura por si só. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G001 | Bico de Brasas | Fogo | físico | 40 | 0 | Se o alvo estiver Queimado antes do primeiro acerto, a bicada causa +10% de dano; não aplica Queimadura. |

| G002 | Espora Incandescente | Fogo | físico | 65 | 30 | Após causar dano, 20% de chance de Queimadura; se o alvo já estiver Queimado, reduz sua Defesa Física em 8% pelas próximas 2 ações dele, sem acumular. |

| G003 | Galope de Carvão | Fogo | físico | 85 | 35 | Se o usuário sofreu dano de armadilha desde sua última ação, poder 105 em vez de 85; acerto bem-sucedido não remove a armadilha. |

| G004 | Garra Vulcânica | Fogo | físico | 95 | 50 | Ao causar dano contra alvo com bônus positivo de Defesa Física, remove apenas o bônus mais recente e tem 15% de causar Queimadura. |

| G005 | Quebra-Forja | Fogo | físico | 115 | 65 | Atinge com poder normal e ignora 30% da parcela positiva de bônus temporários de Defesa Física do alvo; se não houver bônus, recupera 10 de energia após a ação. |

| G011 | Chamado do Meio-Dia | Fogo | suporte | — | 30 | Invoca Ensolarado por 4 rodadas; se substituir Chuva, concede +10% de Defesa Mágica ao usuário até sua próxima ação. |

| G012 | Retorno de Cinzas | Fogo | suporte | — | 35 | Até o próximo ataque físico direto recebido, reduz seu dano em 20%; se o acerto for o segundo da mesma ação, devolve 25% do dano efetivamente sofrido nesse segundo acerto. |

| G013 | Cinzas da Discórdia | Fogo | suporte | — | 35 | Reduz Ataque Físico do alvo em 12% por suas 2 próximas ações; se ele estiver Queimado, em vez disso reduz 18%, sem acumular. |

| G014 | Reacender | Fogo | suporte | — | 40 | Cura 18% do HP máximo próprio; sob Ensolarado remove também Queimadura do próprio usuário, se existir. |

| G106 | Forja das Esporas | Fogo | Suporte | — | 60 | Eleva Ataque Físico e Defesa Física próprios em 20% por 2 ações próprias; se estiver Queimado, concede apenas +25% de Defesa Física, sem anular a penalidade de Ataque da Queimadura. |

| G131 | Cinza nos Olhos | Fogo | Suporte | — | 65 | Exige Ensolarado ativo; reduz Ataque Mágico do alvo em 25% por 1 ação; contra alvo Queimado, redução cai para 12% e dura 2 ações, sem novo estado. |

| N001 | Brasa de Rebate | Fogo | físico | 75 | 45 | Poder 100, em vez de 75, se o usuário recebeu dano físico direto desde sua última ação própria, estando ativo. Verificação na resolução; não inclui dano de estados, passivas ou armadilhas. |

| N003 | Fornalha Resguardada | Fogo | suporte | — | 40 | Remove Queimadura do próprio usuário, caso exista, e concede +20% de Defesa Mágica por suas próximas duas ações próprias. Se não estiver Queimado, concede apenas a proteção. |

| G043 | Chute de Cascalho | Terra | físico | 40 | 0 | Se o alvo tiver peso atual superior a 120% do natural, poder 55 em vez de 40; não altera peso. |

| G044 | Marreta de Barro | Terra | físico | 65 | 30 | Após dano reduz Velocidade em 15% por 2 ações; se uma Tempestade de Areia estiver ativa, duração cai para 1 ação e reduz também Defesa Física em 8%. |

| G045 | Cabeçada de Basalto | Terra | físico | 85 | 35 | Poder 105 em vez de 85 contra alvo com bônus positivo de Defesa Física; não remove bônus nem ignora defesa-base. |

| G046 | Pisão Sísmico | Terra | físico | 100 | 50 | Após causar dano, 20% de chance de Tonto; se o alvo já estiver Tonto, em vez de tentar novo estado reduz sua energia em 12. |

| G047 | Lança de Obsidiana | Terra | físico | 120 | 55 | Ignora 20% de bônus temporários de Defesa Física; se o usuário sofreu dano de estado desde sua última ação, poder 135 em vez de 120. |

| G049 | Lodo Pressurizado | Terra | mágico | 65 | 30 | Após causar dano reduz Defesa Mágica em 10% por 2 ações; se o alvo estiver sob Chuva, em vez disso reduz Defesa Física em 10% por 1 ação. |

| G053 | Tambor da Areia | Terra | suporte | — | 30 | Invoca Tempestade de Areia por 4 rodadas; se substituir Ventania, o usuário ganha 10% de Defesa Física até sua próxima ação. |

| G054 | Muralha Escavada | Terra | suporte | — | 35 | Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. |

| G102 | Couraça do Subsolo | Terra | Suporte | — | 45 | Eleva Defesa Física do usuário em 22% por 2 ações próprias; se estiver acima de 120% do peso natural, reduz também em 10% o dano do primeiro acerto físico recebido. |

| N013 | Pisada de Lastro | Terra | físico | 75 | 45 | Poder 100, em vez de 75, se o peso do usuário for igual ou superior a 120% de seu peso natural de referência no retrato de início da Rinha. |

| N015 | Cinzel Quebra-Manto | Terra | físico | 80 | 55 | Ao calcular o dano, ignora 50% apenas da parcela positiva dos bônus temporários de Defesa Física do alvo; a Defesa Física básica e demais modificadores continuam aplicados. |

| G087 | Choque de Ombros | Neutro | físico | 70 | 25 | Se o usuário entrou por troca voluntária neste turno, poder 90 em vez de 70; não cancela armadilhas da entrada. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #013 Quartzaló

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Comum · **Elementos:** Terra + Elétrico · **Peso natural registrado:** 8,5 kg

**Fonte anterior:** `Galetario_Oficial_15_Fichas_Consolidadas_2026-11-11.json | ficha 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 70 |

| Ataque Físico | 45 |

| Defesa Física | 65 |

| Ataque Mágico | 80 |

| Defesa Mágica | 65 |

| Velocidade | 45 |

| **Total calculado** | **370** |

## Passiva oficial vigente

**Passiva: Quartzo Energizado**

Parâmetros completos (mantidos em sua estrutura original):

```json
{
  "nome": "Quartzo Energizado",
  "tipo": "automática/contínua durante rinha",
  "efeito": "Golpes mágicos ofensivos do próprio Quartzaló dos elementos Terra e Elétrico causam +8% de dano.",
  "bonus_percentual_dano": 8,
  "nao_acumula_consigo": true,
  "concede_ataque_adicional": false,
  "afeta_golpes_fisicos": false,
  "afeta_outros_elementos": false
}
```

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| crina_poderosa | Crina Poderosa | Neutro | Mágico | 40 | 0 | Ataque mágico básico de elemento Neutro; não possui efeitos adicionais. |

| concentracao | Concentração | — | Suporte | — | 0 | Possui 40% de chance de remover estado negativo ativo. Respeita as regras oficiais de Tontura, incluindo a possível falha da ação. |

| O01303 | Lascas de Quartzo | Terra | Mágico | 65 | 25 | Lança fragmentos de quartzo branco; dano mágico direto a um adversário, sem efeito secundário. |

| O01304 | Faíscas do Geodo | Elétrico | Mágico | 85 | 40 | Descarga elétrica de cristais; 10% de chance de aplicar Tontura após causar dano. Apenas uma verificação de estado por ação, não substitui nem acumula estados negativos persistentes. |

| O01305 | Tempestade Cristalina | Terra | Mágico | 115 | 55 | Chuva de cristais brancos; dano mágico direto elevado contra um único alvo. Não invoca Clima, aplica estado negativo ou instala armadilha. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G048 | Grão de Pedra | Terra | mágico | 40 | 0 | Se o usuário estiver sob Tempestade de Areia, projétil básico causa poder 55 em vez de 40; não invoca clima. |

| G049 | Lodo Pressurizado | Terra | mágico | 65 | 30 | Após causar dano reduz Defesa Mágica em 10% por 2 ações; se o alvo estiver sob Chuva, em vez disso reduz Defesa Física em 10% por 1 ação. |

| G050 | Ondulação Rochosa | Terra | mágico | 85 | 35 | Quando o alvo possui Velocidade superior à do usuário, poder 100 em vez de 85; após dano, retira 5 pontos de energia do alvo. |

| G051 | Fenda da Garganta | Terra | mágico | 105 | 50 | Após causar dano 15% de Tonto; contra alvo com peso até 100% do natural, poder sobe de 105 para 120 sem alterar a chance. |

| G052 | Erupção de Geodo | Terra | mágico | 130 | 70 | Se o alvo possui proteção temporária contra dano mágico, poder 145 em vez de 130; após dano, consome a proteção normalmente, sem apagá-la antes do ataque. |

| G053 | Tambor da Areia | Terra | suporte | — | 30 | Invoca Tempestade de Areia por 4 rodadas; se substituir Ventania, o usuário ganha 10% de Defesa Física até sua próxima ação. |

| G054 | Muralha Escavada | Terra | suporte | — | 35 | Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. |

| G055 | Ninho de Pedregulhos | Terra | suporte | — | 45 | Instala armadilha persistente que causa 8% do HP máximo do entrante voluntário; se ele estiver acima de 120% do peso natural, causa 11%, sem afetar entradas obrigatórias. |

| G056 | Pedra de Revezamento | Terra | suporte | — | 35 | Troca usuário por aliado da reserva; o entrante recebe +15% de Defesa Física pelas próximas 2 ações e, sob Tempestade de Areia, ignora o dano de uma armadilha apenas na entrada da troca. |

| G102 | Couraça do Subsolo | Terra | Suporte | — | 45 | Eleva Defesa Física do usuário em 22% por 2 ações próprias; se estiver acima de 120% do peso natural, reduz também em 10% o dano do primeiro acerto físico recebido. |

| N014 | Coluna de Guarda | Terra | suporte | — | 40 | O próximo ataque direto recebido pelo próprio usuário ativo terá 20%, em vez de 10%, de chance de ativar a defesa especial, SOMENTE se a Defesa relevante for pelo menos 120% do Ataque correspondente. A redução ao ativar continua 75%. |

| N016 | Pedra da Impaciência | Terra | mágico | 75 | 45 | Poder 100, em vez de 75, se a última ação efetivamente executada pelo alvo, antes desta, foi um golpe de Suporte (incluindo Concentração). |

| G076 | Arco de Faísca | Elétrico | mágico | 40 | 0 | Sob Santuário dos Raios, ataque básico tem poder 50 em vez de 40; não cria segundo golpe. |

| G077 | Pulso Condutor | Elétrico | mágico | 65 | 30 | Após dano, 15% de Tonto; se o alvo já estiver Paralisado, não tenta Tonto e drena 10 de energia adversária. |

| G078 | Círculo Voltaico | Elétrico | mágico | 80 | 40 | Após dano reduz Ataque Mágico do alvo em 10% por 2 ações; se o usuário tiver menos de 40 de energia após pagar o custo, devolve 8 de energia ao final da ação. |

| G079 | Rede de Relâmpagos | Elétrico | mágico | 105 | 45 | Se o alvo já sofreu redução de Velocidade, poder 125 em vez de 105; se não, 15% de chance de Paralisia após dano. |

| G080 | Ruptura de Alta Tensão | Elétrico | mágico | 130 | 75 | Sob Santuário dos Raios, poder 145 em vez de 130; fora dele, 15% de chance de Tonto após dano, sem gerar acerto adicional. |

| G081 | Cântico dos Condutores | Elétrico | suporte | — | 35 | Invoca Santuário dos Raios por 4 rodadas; se o usuário estiver Paralisado, recebe 10 de energia após a execução válida, sem remover o estado. |

| G082 | Bateria Compartilhada | Elétrico | suporte | — | 35 | Recupera 25 de energia de um aliado ativo escolhido; se o alvo tiver menos de 25 de energia antes da cura, recupera mais 5, sem ultrapassar 100. |

| G084 | Escudo Galvânico | Elétrico | suporte | — | 35 | Concede ao aliado escolhido redução de 25% do dano mágico na próxima ação ofensiva recebida; se tiver menos de 40 de energia no impacto, redução sobe para 35%. |

| G103 | Foco Centelhante | Elétrico | Suporte | — | 45 | Concede +25% Ataque Mágico por 1 ação própria; sob Santuário dos Raios, o primeiro golpe mágico que causar dano ainda recupera 10 de energia, sem repetir por segundo acerto. |

| G110 | Descarga Sináptica | Elétrico | Suporte | — | 60 | Eleva Ataque Mágico em 18% e Velocidade em 15% por 2 ações; sob Santuário dos Raios, a primeira tentativa de reduzir a própria Velocidade não surte efeito. |

| G062 | Sopro Circular | Ar | mágico | 40 | 0 | Quando Ventania estiver ativa, projétil básico tem poder 55 em vez de 40; caso contrário permanece básico sem efeito. |

| G066 | Aurora do Zênite | Ar | mágico | 130 | 70 | Se o alvo recebeu um segundo golpe desde sua última ação, poder 150 em vez de 130; caso contrário, 10% de chance de Tonto após dano. |

| N019 | Pena de Eco | Ar | mágico | 85 | 40 | Se o primeiro ataque deste golpe for totalmente evitado por esquiva do alvo, devolve 15 pontos de energia ao usuário ao terminar a ação (máximo 100). |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #014 Carangocó

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Comum · **Elementos:** Água + Terra · **Peso natural registrado:** 10,5 kg

**Fonte anterior:** `Galetario_Oficial_15_Fichas_Consolidadas_2026-11-11.json | ficha 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 75 |

| Ataque Físico | 80 |

| Defesa Física | 75 |

| Ataque Mágico | 40 |

| Defesa Mágica | 55 |

| Velocidade | 45 |

| **Total calculado** | **370** |

## Passiva oficial vigente

**Passiva: Pinças de Sedimento**

Parâmetros completos (mantidos em sua estrutura original):

```json
{
  "nome": "Pinças de Sedimento",
  "chance_ativacao_pct": 40,
  "reducao_defesa_fisica_pct": 10,
  "duracao": "Até o alvo sair de campo ou ser derrotado",
  "convencional": "Uma verificação ao final de ação ofensiva física com dano",
  "sequencial": "Uma verificação por acerto com dano até primeira ativação, efeito imediatamente após o acerto e aplicado nos próximos acertos da mesma sequência, sem acumular"
}
```

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| garra_afiada | Garra Afiada | Neutro | Físico | 40 | 0 | Dano direto, sem efeitos secundários. |

| concentracao | Concentração | Sem elemento | Suporte | — | 0 | 40% de chance de remover 1 estado negativo persistente do próprio usuário em execução válida; demais regras universais preservadas. |

| O01403 | Pinçada da Ressaca | Água | Físico | 70 | 30 | Ao acertar e causar dano, 30% de chance de reduzir Ataque Físico do alvo em 10% durante os próximos 2 turnos do alvo; uma verificação ao fim da ação; não acumula. |

| O01404 | Couraça de Lodo | Terra | Suporte | — | 35 | Eleva Defesa Física em 25% e Defesa Mágica em 10% do próprio usuário durante 2 turnos próprios, contando o da ativação; não acumula. |

| O01405 | Cerco das Pinças | Terra | Físico | 40 × 1–5 | 55 | Golpe sequencial: até 5 acertos, chances condicionais de 100%/70%/50%/30%/15%; termina ao falhar; não recebe golpe extra de Velocidade. Cada acerto com dano pode acionar Pinças de Sedimento (40%) até a primeira ativação; a redução entra em vigor imediatamente após o acerto e beneficia os seguintes. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G015 | Bico de Marola | Água | físico | 40 | 0 | Se o usuário estiver Afogado, poder sobe de 40 para 55 no primeiro acerto; não reduz nem remove Afogamento. |

| G016 | Cauda de Ressaca | Água | físico | 60 | 25 | Após causar dano, reduz Velocidade do alvo em 12% por 2 ações; sob Chuva, reduz apenas 8%, mas recupera 10 de energia ao final da ação. |

| G017 | Pancada de Maré | Água | físico | 80 | 35 | Se o alvo entrou voluntariamente neste turno, poder sobe de 80 para 100; caso contrário, após causar dano ignora o próximo efeito de redução de Velocidade do usuário até sua próxima ação. |

| G018 | Açoite de Corredeira | Água | físico | 95 | 50 | Após causar dano, 18% de chance de Afogamento; se o alvo já estava Afogado, em vez de tentar aplicar o estado drena 12 de energia. |

| G019 | Quebra-Cais | Água | físico | 120 | 55 | Contra alvo com mais de 70 de energia, poder 135 em vez de 120; após causar dano nessa condição, o usuário não pode receber bônus temporário de Velocidade até sua próxima ação. |

| G020 | Gota Disparada | Água | mágico | 40 | 0 | Se o usuário recebeu cura desde sua ação anterior, poder 55 em vez de 40; não ativa curas adicionais. |

| G022 | Coluna de Espuma | Água | mágico | 80 | 40 | Após causar dano tem 20% de chance de Afogamento; se o usuário possuir bônus temporário de Defesa Mágica, a chance cai para 10%, mas poder sobe para 95. |

| G025 | Canto das Nuvens | Água | suporte | — | 30 | Invoca Chuva por 4 rodadas; caso substitua Ensolarado, cura 8% do HP máximo próprio sem afetar a reserva. |

| G026 | Névoa Protetora | Água | suporte | — | 30 | O aliado escolhido recebe −25% de dano mágico na próxima ação ofensiva recebida; se já estiver Afogado, recupera 12 de energia ao ativar a barreira. |

| G027 | Maré de Retirada | Água | suporte | — | 40 | Troca voluntariamente por aliado da reserva; o entrante recupera 8% de HP máximo e não sofre redução de Velocidade de armadilha somente nessa entrada; outros efeitos de armadilha permanecem. |

| N005 | Fôlego de Ressaca | Água | físico | 70 | 40 | Se o alvo já tiver Afogamento no início desta ação e ao menos um acerto causar dano, o usuário recupera 15 pontos de energia ao terminar a ação (máximo 100). |

| N006 | Redemoinho Exaustivo | Água | suporte | — | 45 | Instala no lado adversário uma armadilha persistente que retira 15 pontos da energia atual de cada Cocorídeo que entra por troca voluntária, nunca abaixo de zero. |

| N007 | Banho Sereno | Água | suporte | — | 45 | Recupera 10% do HP máximo do usuário ativo e remove o estado negativo persistente que ele tenha, se houver. |

| G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. |

| G043 | Chute de Cascalho | Terra | físico | 40 | 0 | Se o alvo tiver peso atual superior a 120% do natural, poder 55 em vez de 40; não altera peso. |

| G044 | Marreta de Barro | Terra | físico | 65 | 30 | Após dano reduz Velocidade em 15% por 2 ações; se uma Tempestade de Areia estiver ativa, duração cai para 1 ação e reduz também Defesa Física em 8%. |

| G045 | Cabeçada de Basalto | Terra | físico | 85 | 35 | Poder 105 em vez de 85 contra alvo com bônus positivo de Defesa Física; não remove bônus nem ignora defesa-base. |

| G046 | Pisão Sísmico | Terra | físico | 100 | 50 | Após causar dano, 20% de chance de Tonto; se o alvo já estiver Tonto, em vez de tentar novo estado reduz sua energia em 12. |

| G053 | Tambor da Areia | Terra | suporte | — | 30 | Invoca Tempestade de Areia por 4 rodadas; se substituir Ventania, o usuário ganha 10% de Defesa Física até sua próxima ação. |

| G054 | Muralha Escavada | Terra | suporte | — | 35 | Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. |

| G055 | Ninho de Pedregulhos | Terra | suporte | — | 45 | Instala armadilha persistente que causa 8% do HP máximo do entrante voluntário; se ele estiver acima de 120% do peso natural, causa 11%, sem afetar entradas obrigatórias. |

| N013 | Pisada de Lastro | Terra | físico | 75 | 45 | Poder 100, em vez de 75, se o peso do usuário for igual ou superior a 120% de seu peso natural de referência no retrato de início da Rinha. |

| N014 | Coluna de Guarda | Terra | suporte | — | 40 | O próximo ataque direto recebido pelo próprio usuário ativo terá 20%, em vez de 10%, de chance de ativar a defesa especial, SOMENTE se a Defesa relevante for pelo menos 120% do Ataque correspondente. A redução ao ativar continua 75%. |

| N015 | Cinzel Quebra-Manto | Terra | físico | 80 | 55 | Ao calcular o dano, ignora 50% apenas da parcela positiva dos bônus temporários de Defesa Física do alvo; a Defesa Física básica e demais modificadores continuam aplicados. |

| G030 | Ferrão de Trepadeira | Planta | físico | 55 | 25 | Após dano, 25% de chance de Envenenamento; caso o alvo já esteja Envenenado, reduz 10 de sua energia em vez de reaplicar estado. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #015 Faíscocó

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Raro · **Elementos:** Fogo + Elétrico · **Peso natural registrado:** 5,8 kg

**Fonte anterior:** `Galetario_015_Faiscoco_Registro_Oficial.json | homologação posterior ao 1.2.36`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 70 |

| Ataque Físico | 60 |

| Defesa Física | 50 |

| Ataque Mágico | 95 |

| Defesa Mágica | 55 |

| Velocidade | 100 |

| **Total calculado** | **430** |

## Passiva oficial vigente

**Passiva: Indução Incandescente v2**

**Ficha integral:** `{"name": "Indução Incandescente v2", "full_rules": "INDUÇÃO INCANDESCENTE v2 — Faíscocó começa sua PRIMEIRA entrada em uma Rinha com 1 Carga Termoelétrica. Enquanto possuir carga, seu primeiro acerto VÁLIDO de um golpe MÁGICO OFENSIVO de Fogo ou Elétrico que cause dano consome a carga, aumenta APENAS ESSE ACERTO em 30% de dano e recupera 10 pontos de energia, limitados ao máximo universal de 100. Não afeta acertos adicionais da mesma ação. A recarga ofensiva ocorre ao FINAL de uma ação com golpe mágico ofensivo de Fogo/Elétrico (mesmo se errar), mas SOMENTE se Faíscocó INICIOU aquela ação sem Carga Termoelétrica; consumir uma carga durante a ação NÃO permite recarregar pelo mesmo ataque. Receber dano DIRETO de golpe inimigo também produz 1 carga se ainda não houver carga, excluídos danos indiretos de estados negativos, clima e armadilhas. Máximo 1 carga, sem acumular ou gerar ataques extras. Trocar para a reserva elimina a carga, e entradas posteriores não fornecem uma nova carga inicial.", "first_entry_charge": 1, "max_charges": 1, "damage_bonus": 0.3, "energy_refund": 10, "recharge_requires_no_charge_at_action_start": true, "offensive_recharge_at_end_of_action": true, "direct_enemy_hit_can_charge_when_empty": true, "leave_field_clears_charge": true}`

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| 1 | Crina Poderosa | Neutro | Mágico | 40 | 0 | Golpe básico mágico sem efeito secundário; preserva a regra universal. |

| 2 | Concentração | Sem elemento | Suporte | — | 0 | Efeitos universais vigentes de Concentração; único golpe obrigatoriamente equipado. Não atribuir porcentagem nova. |

| 3 | Fio de Ionização v2 | Elétrico | Mágico | 65 | 35 | Após acerto com dano, 40% de reduzir Defesa Mágica do alvo em 10% por 2 turnos do alvo. Apenas 1 verificação ao final da ação, mesmo com ataque adicional por Velocidade. Não acumula. |

| 4 | Manto de Cinza Viva v2 | Fogo | Mágico | 55 | 40 | Golpe mágico ofensivo; ao final da ação cria proteção que reduz em 35% o dano do próximo acerto direto recebido, mesmo que o golpe ofensivo erre. Expira após proteger 1 acerto ou ao final do segundo turno próprio posterior à utilização, o que ocorrer primeiro. Não acumula, não bloqueia estados negativos; máximo 1 manto por ação. |

| 5 | Tormenta do Anel Rubro | Fogo | Mágico | 95 | 55 | Depois de pelo menos 1 acerto que cause dano, 15% de chance de Queimadura, com apenas 1 verificação ao final da ação e regras universais de estados negativos. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G001 | Bico de Brasas | Fogo | Físico | 40 | 0 | +10% de dano contra alvo já Queimado. |

| G002 | Espora Incandescente | Fogo | Físico | 65 | 30 | 20% de chance de Queimadura; contra alvo já Queimado, reduz a Defesa Física do alvo em 8% por duas ações. |

| G003 | Galope de Carvão | Fogo | Físico | 85 | 35 | Poder 105 se o usuário sofreu dano de armadilha desde sua última ação. |

| G006 | Faísca de Terreiro | Fogo | Mágico | 40 | 0 | Sob Ensolarado, 15% de reduzir o Ataque Mágico do alvo em 8% por uma ação. |

| G007 | Sopro de Cinzas | Fogo | Mágico | 65 | 30 | Poder 80 sob Chuva; fora da Chuva, 20% de chance de Queimadura após causar dano. |

| G008 | Rosácea de Fagulhas | Fogo | Mágico | 85 | 40 | Durante o cálculo de dano, reduz pela metade um bônus positivo de Ataque Mágico do alvo, sem removê-lo. |

| G011 | Chamado do Meio-Dia | Fogo | Suporte | — | 30 | Invoca Ensolarado por quatro rodadas; se substituir Chuva, concede +10% de Defesa Mágica ao usuário até sua próxima ação. |

| G013 | Cinzas da Discórdia | Fogo | Suporte | — | 35 | Reduz o Ataque Físico do alvo em 12% por duas ações; se já Queimado, reduz em 18%. |

| N001 | Brasa de Rebate | Fogo | Físico | 75 | 45 | Poder 100 se o usuário recebeu dano físico direto desde sua última ação própria. |

| N002 | Cinza Desarmadora | Fogo | Mágico | 70 | 45 | Após causar dano, remove o bônus temporário positivo mais forte de Ataque Mágico do alvo. |

| N003 | Fornalha Resguardada | Fogo | Suporte | — | 40 | Remove Queimadura do próprio usuário e concede +20% de Defesa Mágica por duas ações próprias. |

| N004 | Brilho de Carvão | Fogo | Mágico | 80 | 45 | Sob Ensolarado, recupera 15 de energia após causar dano, uma vez por ação. |

| G071 | Bicada Elétrica | Elétrico | Físico | 40 | 0 | Poder 50 contra alvo Paralisado. |

| G072 | Espora de Cobre | Elétrico | Físico | 65 | 30 | 18% de chance de Tontura após dano; se alvo já Tonto, recupera 8 de energia em vez de reaplicar. |

| G073 | Investida do Dínamo | Elétrico | Físico | 85 | 35 | Poder 100 contra alvo com menos de 30 de energia. |

| G074 | Cascata de Centelhas | Elétrico | Físico | 100 | 50 | Reduz Defesa Física do alvo em 12% por duas ações; sob Santuário dos Raios, reduz 16% por uma ação e recupera 5 de energia. |

| G076 | Arco de Faísca | Elétrico | Mágico | 40 | 0 | Poder 50 sob Santuário dos Raios, sem produzir golpes adicionais. |

| G077 | Pulso Condutor | Elétrico | Mágico | 65 | 30 | 15% de chance de Tontura; contra alvo já Paralisado, drena 10 de energia em vez de tentar Tontura. |

| G078 | Círculo Voltaico | Elétrico | Mágico | 80 | 40 | Reduz Ataque Mágico do alvo em 10% por duas ações após causar dano; ao final recupera 8 de energia se estava abaixo de 40 após pagar o custo. |

| G081 | Cântico dos Condutores | Elétrico | Suporte | — | 35 | Invoca Santuário dos Raios por quatro rodadas; se o usuário estiver Paralisado, recupera 10 de energia após a execução. |

| G083 | Campo de Centelhas | Elétrico | Suporte | — | 45 | Armadilha persistente que reduz Defesa Mágica do adversário que entrar por troca voluntária em 12% por duas ações; se entrar Paralisado, reduz 15% por uma ação. |

| G084 | Escudo Galvânico | Elétrico | Suporte | — | 35 | Concede a um aliado redução de 25% do dano mágico na próxima ação ofensiva recebida; aumenta para 35% se o protegido tiver menos de 40 de energia no impacto. |

| G110 | Descarga Sináptica | Elétrico | Suporte | — | 60 | Concede +18% Ataque Mágico e +15% Velocidade por duas ações; sob Santuário dos Raios, impede a primeira tentativa de reduzir Velocidade durante o efeito. |

| G057 | Asa Riscante | Ar | Físico | 40 | 0 | Poder 50 se a Velocidade do usuário superar a do alvo, sem criar ataques adicionais. |

| N018 | Vórtice de Passagem | Ar | Suporte | — | 45 | Troca Faíscocó por aliado apto da reserva; somente nessa entrada o substituto ignora gatilhos das armadilhas aliadas, sem remover armadilhas ou proteger trocas futuras. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #016 Libelocó

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Comum · **Elementos:** Água + Ar · **Peso natural registrado:** 4,9 kg

**Fonte anterior:** `Galetario_016_OFICIAL.json | homologação 12/11/2026`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 60 |

| Ataque Físico | 40 |

| Defesa Física | 48 |

| Ataque Mágico | 74 |

| Defesa Mágica | 70 |

| Velocidade | 62 |

| **Total calculado** | **354** |

## Passiva oficial vigente

**Passiva: Voo de Remanso**

**Efeito:** Recupera 8 pontos de energia após pagar o custo e resolver o golpe; máximo 100.

**Gatilho:** Ao concluir validamente uma ação própria que utilizou um golpe de Suporte com custo nominal de pelo menos 25 de energia.

**Limites:** Uma ativação por turno próprio; Concentração E0 não ativa; não reage a golpes ofensivos nem a ações canceladas; não gera ação adicional.

**Revisão 12/11/2026:** nenhuma alteração de balanceamento nesta espécie. Dados anteriores preservados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| 1 | Crina Poderosa | Neutro | Mágico | 40 | 0 | Golpe básico mágico universal; não acrescenta efeitos particulares. |

| 2 | Concentração | Sem elemento | Suporte | — | 0 | Todos os efeitos universais homologados, sem atribuir novos percentuais; único golpe obrigatório entre os cinco equipados. |

| 3 | Corte de Corrente | Ar | Mágico | 65 | 30 | Após pelo menos um acerto com dano, 25% de chance de reduzir Ataque Mágico do alvo em 10% por seus próximos dois turnos. Verificação uma vez ao fim da ação; não acumula consigo mesmo. |

| 4 | Redoma de Orvalho | Água | Suporte | — | 35 | Concede ao próprio usuário uma proteção que reduz em 25% o dano do próximo acerto mágico direto recebido. Desaparece após esse acerto ou ao final do segundo turno próprio posterior à ativação, o que acontecer primeiro. Uma proteção, sem acumular consigo mesma; não impede estados. |

| 5 | Espiral de Monção | Água | Mágico | 95 | 50 | Após pelo menos um acerto com dano, 20% de chance de Afogamento. Se Ventania já estiver ativa na resolução, a chance será 30% em vez de 20%. Uma verificação de estado por ação; não acumula estado; não cria ataques adicionais. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G015 | Bico de Marola | Água | físico | 40 | 0 | Se o usuário estiver Afogado, poder sobe de 40 para 55 no primeiro acerto; não reduz nem remove Afogamento. |

| G016 | Cauda de Ressaca | Água | físico | 60 | 25 | Após causar dano, reduz Velocidade do alvo em 12% por 2 ações; sob Chuva, reduz apenas 8%, mas recupera 10 de energia ao final da ação. |

| G020 | Gota Disparada | Água | mágico | 40 | 0 | Se o usuário recebeu cura desde sua ação anterior, poder 55 em vez de 40; não ativa curas adicionais. |

| G021 | Orvalho Cortante | Água | mágico | 60 | 20 | Após causar dano, se Chuva estiver ativa recupera 8 de energia; se não estiver, reduz Defesa Mágica inimiga em 6% até a próxima ação do alvo. |

| G022 | Coluna de Espuma | Água | mágico | 80 | 40 | Após causar dano tem 20% de chance de Afogamento; se o usuário possuir bônus temporário de Defesa Mágica, a chance cai para 10%, mas poder sobe para 95. |

| G025 | Canto das Nuvens | Água | suporte | — | 30 | Invoca Chuva por 4 rodadas; caso substitua Ensolarado, cura 8% do HP máximo próprio sem afetar a reserva. |

| G026 | Névoa Protetora | Água | suporte | — | 30 | O aliado escolhido recebe −25% de dano mágico na próxima ação ofensiva recebida; se já estiver Afogado, recupera 12 de energia ao ativar a barreira. |

| G027 | Maré de Retirada | Água | suporte | — | 40 | Troca voluntariamente por aliado da reserva; o entrante recupera 8% de HP máximo e não sofre redução de Velocidade de armadilha somente nessa entrada; outros efeitos de armadilha permanecem. |

| G028 | Banho Reparador | Água | suporte | — | 40 | Cura 20% do HP máximo de um aliado vivo, inclusive reserva; se o alvo estiver com menos de 30% do HP, acrescenta mais 5%, uma única vez. |

| N007 | Banho Sereno | Água | suporte | — | 45 | Recupera 10% do HP máximo do usuário ativo e remove o estado negativo persistente que ele tenha, se houver. |

| N008 | Pressão do Manancial | Água | mágico | 70 | 45 | Poder 95, em vez de 70, se o alvo tiver 40 ou menos pontos de energia atual no momento do cálculo do primeiro acerto. |

| G057 | Asa Riscante | Ar | físico | 40 | 0 | Se a Velocidade do usuário superar a do alvo, poder 50 em vez de 40; sem alterar a chance universal de segundo golpe. |

| G058 | Pluma de Corte | Ar | físico | 60 | 25 | Após dano reduz Defesa Física do alvo em 10% por 1 ação; se a esquiva do usuário foi ativada desde sua última ação, aumenta a redução para 15%. |

| G059 | Bicada Turbilhão | Ar | físico | 80 | 35 | Se o alvo usou Suporte na última ação dele, poder 100 em vez de 80; caso contrário recupera 5 de energia após causar dano em Ventania. |

| G062 | Sopro Circular | Ar | mágico | 40 | 0 | Quando Ventania estiver ativa, projétil básico tem poder 55 em vez de 40; caso contrário permanece básico sem efeito. |

| G063 | Assobio Rasante | Ar | mágico | 65 | 25 | Após causar dano reduz Ataque Mágico em 8% por 2 ações; se o alvo estiver sob uma proteção de Suporte, a redução é de 12% por apenas 1 ação. |

| G064 | Espinho de Pressão | Ar | mágico | 85 | 35 | Se uma esquiva completa do usuário ocorreu no turno anterior, poder 105 em vez de 85; não concede esquiva nova. |

| G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. |

| G068 | Corrente de Evasão | Ar | suporte | — | 35 | Concede +8 pontos percentuais de esquiva ao usuário por suas próximas 2 ações; se esquivar efetivamente de um golpe, recupera 12 de energia após a ação ofensiva adversária, uma vez. |

| G069 | Túnel de Retorno | Ar | suporte | — | 35 | Troca por aliado da reserva, concedendo-lhe +15% de Velocidade por suas próximas 2 ações; se ele estiver Paralisado, concede somente +10% e não remove a Paralisia. |

| G070 | Redemoinho de Penas | Ar | suporte | — | 45 | Instala armadilha persistente que reduz o Ataque Físico do entrante voluntário em 12% por 2 ações; sob Ventania reduz em 15% por 1 ação, sem acumular. |

| N017 | Pluma Vazia | Ar | mágico | 70 | 45 | Poder 90, em vez de 70, se o peso do usuário for igual ou inferior a 100% de seu peso natural de referência no retrato de início da Rinha. |

| G092 | Eco do Cocoricó | Neutro | mágico | 40 | 0 | Se o alvo estiver Tonto, poder 50 em vez de 40; caso contrário é onda mágica básica sem status. |

| G097 | Cuidado de Plumagem | Sem elemento | suporte | — | 40 | Cura 18% do HP máximo de um aliado vivo, inclusive reserva; se o aliado estiver Envenenado, a cura sobe para 22%, mas não remove o estado. |

| G100 | Terreiro Purificado | Sem elemento | suporte | — | 45 | Remove integralmente todas as armadilhas e cargas do lado do usuário; se pelo menos uma armadilha foi removida, recupera 10 de energia após a execução. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #017 Castorocó

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Comum · **Elementos:** Planta + Terra · **Peso natural registrado:** 11,2 kg

**Fonte anterior:** `Galetario_017_OFICIAL.json | homologação 12/11/2026`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 90 |

| Ataque Físico | 70 |

| Defesa Física | 90 |

| Ataque Mágico | 39 |

| Defesa Mágica | 58 |

| Velocidade | 27 |

| **Total calculado** | **374** |

## Passiva oficial vigente

**Passiva: Barragem Reforçada**

**Efeito:** Obtém +17% de Defesa Mágica até o final do segundo turno próprio posterior à ativação.

**Gatilho:** Após receber dano mágico direto de um inimigo e sobreviver, estando ativo e sem o bônus desta passiva.

**Limites:** Uma ativação por ação inimiga; não se reaplica enquanto durar; não retroage para reduzir o golpe que a ativou; sai ao trocar ou ser derrotado; não reage a dano indireto.

## Registro da homologação de balanceamento

- **bônus de Defesa Mágica após gatilho:** +15% → **+17%**. Gatilho, duração e proibição de acumular permanecem.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| 1 | Garra Afiada | Neutro | Físico | 40 | 0 | Golpe básico físico universal; não acrescenta efeitos particulares. |

| 2 | Concentração | Sem elemento | Suporte | — | 0 | Todos os efeitos universais homologados; único golpe obrigatório entre os cinco equipados. |

| 3 | Pedrada de Seiva | Terra | Físico | 70 | 30 | Após pelo menos um acerto com dano, 25% de chance de reduzir a Velocidade do alvo em 10% por seus próximos dois turnos; uma verificação ao final da ação, não acumula consigo mesma. |

| 4 | Círculo de Rebentos | Planta | Suporte | — | 40 | Instala no lado adversário uma armadilha persistente com uma carga. Na próxima entrada por troca voluntária, consome sua única carga e reduz a Velocidade do entrante em 15% por seus próximos dois turnos. Não causa dano, não atua em entrada inicial, não acumula outra carga do mesmo golpe; removível pela limpeza universal de armadilhas. |

| 5 | Arrebento de Raiz-Pedra | Planta | Físico | 95 | 50 | Se o alvo já começou a ação com Velocidade efetiva reduzida por um modificador negativo, o primeiro acerto válido tem poder 110 em vez de 95. Qualquer segundo acerto segue o poder nominal 95 e as regras universais, sem bônus da condição. Não aplica estados nem gera ataques extras. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G029 | Chicotada de Talos | Planta | físico | 40 | 0 | Se o alvo estiver Envenenado, poder 50 em vez de 40; não causa Envenenamento novo. |

| G030 | Ferrão de Trepadeira | Planta | físico | 55 | 25 | Após dano, 25% de chance de Envenenamento; caso o alvo já esteja Envenenado, reduz 10 de sua energia em vez de reaplicar estado. |

| G031 | Arranco de Tronco | Planta | físico | 80 | 35 | Se o usuário estiver com peso até 100% do natural, poder 95 em vez de 80; com peso maior, gera +10% de Defesa Física até sua próxima ação após dano. |

| G032 | Tesoura de Folhas | Planta | físico | 90 | 40 | Ao causar dano, 15% de Envenenamento; quando o alvo já estiver Envenenado, reduz apenas sua Defesa Física em 12% por 1 ação, sem acumular. |

| G034 | Semente Atirada | Planta | mágico | 40 | 0 | Se Santuário das Raízes estiver ativo, concede 5 de energia ao usuário após causar dano; caso contrário, ataque mágico básico normal. |

| G035 | Perfume Ácido | Planta | mágico | 60 | 25 | Após dano tem 20% de Envenenamento; se o alvo estiver sob Santuário das Raízes e já Envenenado, em vez disso reduz Ataque Mágico em 8% por 1 ação. |

| G039 | Hino das Raízes | Planta | suporte | — | 35 | Invoca Santuário das Raízes por 4 rodadas; se uma armadilha inimiga estiver ativa, reduz em 10% o dano da próxima entrada de um aliado por troca voluntária, sem remover a armadilha. |

| G040 | Armadilha de Pólen | Planta | suporte | — | 45 | Instala armadilha persistente que reduz o Ataque Mágico do entrante voluntário em 12% por suas 2 próximas ações; se já estiver Envenenado, reduz 18% em vez disso, sem acumular. |

| G041 | Fotossíntese de Poleiro | Planta | suporte | — | 45 | Cura 20% do HP máximo de um aliado vivo; no Santuário das Raízes, cura também 5% do HP máximo do usuário ativo quando o alvo for outro aliado. |

| G042 | Casca Compartilhada | Planta | suporte | — | 30 | Concede ao aliado selecionado −20% dano mágico na próxima ação ofensiva recebida; se a ação tiver segundo acerto, nele a proteção sobe para 35%. |

| G109 | Seiva de Ferro | Planta | Suporte | — | 60 | Eleva as duas Defesas próprias em 18% por 2 ações; no Santuário das Raízes, a primeira redução de atributo recebida é ignorada, sem impedir estados negativos. |

| N012 | Casco de Bromélia | Planta | físico | 70 | 45 | Poder 95, em vez de 70, se a Defesa Física efetiva do usuário for ao menos 120% do Ataque Físico efetivo do alvo no momento da resolução. |

| G043 | Chute de Cascalho | Terra | físico | 40 | 0 | Se o alvo tiver peso atual superior a 120% do natural, poder 55 em vez de 40; não altera peso. |

| G044 | Marreta de Barro | Terra | físico | 65 | 30 | Após dano reduz Velocidade em 15% por 2 ações; se uma Tempestade de Areia estiver ativa, duração cai para 1 ação e reduz também Defesa Física em 8%. |

| G045 | Cabeçada de Basalto | Terra | físico | 85 | 35 | Poder 105 em vez de 85 contra alvo com bônus positivo de Defesa Física; não remove bônus nem ignora defesa-base. |

| G046 | Pisão Sísmico | Terra | físico | 100 | 50 | Após causar dano, 20% de chance de Tonto; se o alvo já estiver Tonto, em vez de tentar novo estado reduz sua energia em 12. |

| G048 | Grão de Pedra | Terra | mágico | 40 | 0 | Se o usuário estiver sob Tempestade de Areia, projétil básico causa poder 55 em vez de 40; não invoca clima. |

| G049 | Lodo Pressurizado | Terra | mágico | 65 | 30 | Após causar dano reduz Defesa Mágica em 10% por 2 ações; se o alvo estiver sob Chuva, em vez disso reduz Defesa Física em 10% por 1 ação. |

| G050 | Ondulação Rochosa | Terra | mágico | 85 | 35 | Quando o alvo possui Velocidade superior à do usuário, poder 100 em vez de 85; após dano, retira 5 pontos de energia do alvo. |

| G053 | Tambor da Areia | Terra | suporte | — | 30 | Invoca Tempestade de Areia por 4 rodadas; se substituir Ventania, o usuário ganha 10% de Defesa Física até sua próxima ação. |

| G054 | Muralha Escavada | Terra | suporte | — | 35 | Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. |

| G055 | Ninho de Pedregulhos | Terra | suporte | — | 45 | Instala armadilha persistente que causa 8% do HP máximo do entrante voluntário; se ele estiver acima de 120% do peso natural, causa 11%, sem afetar entradas obrigatórias. |

| G056 | Pedra de Revezamento | Terra | suporte | — | 35 | Troca usuário por aliado da reserva; o entrante recebe +15% de Defesa Física pelas próximas 2 ações e, sob Tempestade de Areia, ignora o dano de uma armadilha apenas na entrada da troca. |

| G086 | Patada Rasteira | Neutro | físico | 50 | 25 | Após causar dano reduz Velocidade do alvo em 8% por 2 ações; se o usuário estiver Paralisado, efeito dura só 1 ação mas poder aumenta para 65. |

| G100 | Terreiro Purificado | Sem elemento | suporte | — | 45 | Remove integralmente todas as armadilhas e cargas do lado do usuário; se pelo menos uma armadilha foi removida, recupera 10 de energia após a execução. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #018 Mariposocó

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Comum · **Elementos:** Fogo + Planta · **Peso natural registrado:** 5,6 kg

**Fonte anterior:** `Galetario_018_OFICIAL.json | homologação 12/11/2026`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 68 |

| Ataque Físico | 44 |

| Defesa Física | 49 |

| Ataque Mágico | 97 |

| Defesa Mágica | 62 |

| Velocidade | 68 |

| **Total calculado** | **388** |

## Passiva oficial vigente

**Passiva: Escamas de Brasa**

**Efeito:** Recupera 12 pontos de energia ao final da ação, respeitando o máximo de 100.

**Gatilho:** Ao iniciar uma ação com alvo já Envenenado e causar dano com golpe mágico de Fogo, OU ao iniciar uma ação com alvo já Queimado e causar dano com golpe mágico de Planta.

**Limites:** Uma ativação por ação própria, independentemente dos acertos; verifica o estado no início da ação, nunca um status causado naquela própria ação; não muda, remove ou acumula estados; não concede golpes extras.

## Registro da homologação de balanceamento

- **recuperação de energia após gatilho:** 10 pontos → **12 pontos**. A verificação de status e o limite de uma vez por ação permanecem.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| 1 | Crina Poderosa | Neutro | Mágico | 40 | 0 | Golpe básico mágico universal sem efeitos particulares. |

| 2 | Concentração | Sem elemento | Suporte | — | 0 | Todos os efeitos universais homologados; único golpe obrigatório entre os cinco equipados. |

| 3 | Pólen de Cinzas | Planta | Mágico | 60 | 30 | Após pelo menos um acerto com dano, 30% de chance de aplicar Envenenamento. Apenas uma verificação por ação. Respeita a proibição de acumular estados negativos. |

| 4 | Clarão de Pólen | Fogo | Mágico | 70 | 35 | Após pelo menos um acerto com dano, 25% de chance de aplicar Queimadura. Apenas uma verificação por ação. Não substitui nem acumula estados negativos persistentes já ativos. |

| 5 | Floração da Fornalha | Fogo | Mágico | 90 | 50 | Se o alvo estava Envenenado no início da ação, o primeiro acerto válido que cause dano recebe +12% de dano, sem alterar o poder nominal 90. O eventual segundo acerto não recebe o bônus. Não aplica estados nem cria ataques adicionais. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G001 | Bico de Brasas | Fogo | físico | 40 | 0 | Se o alvo estiver Queimado antes do primeiro acerto, a bicada causa +10% de dano; não aplica Queimadura. |

| G002 | Espora Incandescente | Fogo | físico | 65 | 30 | Após causar dano, 20% de chance de Queimadura; se o alvo já estiver Queimado, reduz sua Defesa Física em 8% pelas próximas 2 ações dele, sem acumular. |

| G003 | Galope de Carvão | Fogo | físico | 85 | 35 | Se o usuário sofreu dano de armadilha desde sua última ação, poder 105 em vez de 85; acerto bem-sucedido não remove a armadilha. |

| G004 | Garra Vulcânica | Fogo | físico | 95 | 50 | Ao causar dano contra alvo com bônus positivo de Defesa Física, remove apenas o bônus mais recente e tem 15% de causar Queimadura. |

| G006 | Faísca de Terreiro | Fogo | mágico | 40 | 0 | Se Ensolarado estiver ativo, o projétil básico tem 15% de chance de reduzir Ataque Mágico do alvo em 8% por 1 ação; caso contrário, dano normal. |

| G007 | Sopro de Cinzas | Fogo | mágico | 65 | 30 | Acertar inimigo sob Chuva causa poder 80 em vez de 65; se não chover, 20% de chance de Queimadura após dano. |

| G008 | Rosácea de Fagulhas | Fogo | mágico | 85 | 40 | Se o alvo tiver bônus positivo de Ataque Mágico, reduz esse bônus pela metade durante o cálculo do dano deste golpe; não remove o bônus depois. |

| G011 | Chamado do Meio-Dia | Fogo | suporte | — | 30 | Invoca Ensolarado por 4 rodadas; se substituir Chuva, concede +10% de Defesa Mágica ao usuário até sua próxima ação. |

| G012 | Retorno de Cinzas | Fogo | suporte | — | 35 | Até o próximo ataque físico direto recebido, reduz seu dano em 20%; se o acerto for o segundo da mesma ação, devolve 25% do dano efetivamente sofrido nesse segundo acerto. |

| G013 | Cinzas da Discórdia | Fogo | suporte | — | 35 | Reduz Ataque Físico do alvo em 12% por suas 2 próximas ações; se ele estiver Queimado, em vez disso reduz 18%, sem acumular. |

| G014 | Reacender | Fogo | suporte | — | 40 | Cura 18% do HP máximo próprio; sob Ensolarado remove também Queimadura do próprio usuário, se existir. |

| N002 | Cinza Desarmadora | Fogo | mágico | 70 | 45 | Após ao menos um acerto com dano, elimina um bônus temporário positivo de Ataque Mágico do alvo, se houver, escolhendo o mais forte; em empate, o mais antigo. O dano deste golpe é calculado antes da remoção. |

| G029 | Chicotada de Talos | Planta | físico | 40 | 0 | Se o alvo estiver Envenenado, poder 50 em vez de 40; não causa Envenenamento novo. |

| G030 | Ferrão de Trepadeira | Planta | físico | 55 | 25 | Após dano, 25% de chance de Envenenamento; caso o alvo já esteja Envenenado, reduz 10 de sua energia em vez de reaplicar estado. |

| G032 | Tesoura de Folhas | Planta | físico | 90 | 40 | Ao causar dano, 15% de Envenenamento; quando o alvo já estiver Envenenado, reduz apenas sua Defesa Física em 12% por 1 ação, sem acumular. |

| G034 | Semente Atirada | Planta | mágico | 40 | 0 | Se Santuário das Raízes estiver ativo, concede 5 de energia ao usuário após causar dano; caso contrário, ataque mágico básico normal. |

| G035 | Perfume Ácido | Planta | mágico | 60 | 25 | Após dano tem 20% de Envenenamento; se o alvo estiver sob Santuário das Raízes e já Envenenado, em vez disso reduz Ataque Mágico em 8% por 1 ação. |

| G036 | Néctar Corrosivo | Planta | mágico | 80 | 40 | Após causar dano reduz Defesa Mágica em 12% por 2 ações; se atingir alvo com bônus positivo de Defesa Mágica, remove primeiro o bônus mais recente, sem aplicar a redução. |

| G039 | Hino das Raízes | Planta | suporte | — | 35 | Invoca Santuário das Raízes por 4 rodadas; se uma armadilha inimiga estiver ativa, reduz em 10% o dano da próxima entrada de um aliado por troca voluntária, sem remover a armadilha. |

| G040 | Armadilha de Pólen | Planta | suporte | — | 45 | Instala armadilha persistente que reduz o Ataque Mágico do entrante voluntário em 12% por suas 2 próximas ações; se já estiver Envenenado, reduz 18% em vez disso, sem acumular. |

| G041 | Fotossíntese de Poleiro | Planta | suporte | — | 45 | Cura 20% do HP máximo de um aliado vivo; no Santuário das Raízes, cura também 5% do HP máximo do usuário ativo quando o alvo for outro aliado. |

| G042 | Casca Compartilhada | Planta | suporte | — | 30 | Concede ao aliado selecionado −20% dano mágico na próxima ação ofensiva recebida; se a ação tiver segundo acerto, nele a proteção sobe para 35%. |

| G062 | Sopro Circular | Ar | mágico | 40 | 0 | Quando Ventania estiver ativa, projétil básico tem poder 55 em vez de 40; caso contrário permanece básico sem efeito. |

| G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. |

| G100 | Terreiro Purificado | Sem elemento | suporte | — | 45 | Remove integralmente todas as armadilhas e cargas do lado do usuário; se pelo menos uma armadilha foi removida, recupera 10 de energia após a execução. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #019 Renacocó

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Mítico · **Elementos:** Fogo · **Peso natural registrado:** não consta desta fonte

**Fonte anterior:** `Galetario_019_Renacoco_OFICIAL_2026-11-12.json`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 180 |

| Ataque Físico | 80 |

| Defesa Física | 100 |

| Ataque Mágico | 40 |

| Defesa Mágica | 100 |

| Velocidade | 70 |

| **Total calculado** | **570** |

## Passiva oficial vigente

**Passiva: Três Chamas da Vida**

- **Renovação Própria** — +20% na eficácia das habilidades de cura aplicadas por Renacocó a si mesmo.

- **Dádiva da Fênix** — +30% na eficácia das habilidades de cura aplicadas por Renacocó a aliados.

- **Regeneração Eterna** — Ao final de cada turno próprio em campo: Renacocó recupera 9% do HP máximo e o aliado elegível em campo com menor percentual de HP recupera 10% de seu HP máximo.

- **Restrições:** Regeneração 1 vez por turno próprio, não acumula, não recebe amplificação dos bônus de cura, não ultrapassa HP máximo, não revive derrotados e cessa quando Renacocó sai de campo.

## Registro da homologação de balanceamento

- **cura própria ao fim do turno ativo:** 10% HP máximo → **9% HP máximo**. A regeneração do aliado permanece 10%, sem alteração.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| 1 | Garra Afiada | Neutro | Físico | 40 | 0 | Ataque básico universal. |

| 2 | Concentração | Neutro | Suporte | — | 0 | Golpe universal obrigatório; recuperação de Energia, buff aleatório e 20% de chance de remover estado negativo conforme regra geral. |

| 3 | Alvorada Purificadora | Fogo | Suporte | — | 50 | Remove todos os estados negativos de Renacocó e de todos os aliados, inclusive reservas; não remove efeitos positivos. Cura-base de 20% do HP máximo em Renacocó OU um aliado escolhido no banco (24%/26% com a passiva). Não ressuscita. |

| 4 | Investida das Três Caudas | Fogo | Físico | 95 | 40 | Aplica marca Brasa Regeneradora ao acertar (2 turnos próprios, não acumula). Outro golpe físico diferente que acerte o alvo consome a marca e cura Renacocó em 10% de seu HP máximo, valor final com a passiva. Marca desaparece com saída do alvo ou expiração; ataque adicional idêntico não ativa. As três caudas produzem um único golpe. |

| 5 | Juramento da Fênix | Fogo | Suporte | — | 70 | Exclusivo/hereditário, 1 utilização bem-sucedida por Rinha. Ressuscita 1 aliado derrotado, devolvendo-o ao banco com 25% do HP máximo (valor fixo não amplificado) e removendo todos seus estados negativos. Renacocó sacrifica 50% do próprio HP máximo; não pode ativar caso fique abaixo de 1 HP. O aliado não age imediatamente. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| 1 | Asa da Aurora | Fogo | Físico | 70 | 30 | Golpeia com uma asa em chamas claras. 25% de chance de provocar Queimadura. |

| 2 | Bico Luminar | Fogo | Físico | 55 | 25 | Bicada flamejante que causa 15% mais dano se o inimigo já estiver Queimado. |

| 3 | Rasante Pacificador | Ar | Físico | 75 | 30 | Ataca com as asas e reduz o Ataque Físico do alvo em 15% por 2 turnos dele. |

| 4 | Passo do Peregrino | Terra | Físico | 80 | 40 | Investida com as pernas longas. Após acertar, aumenta a Defesa Física própria em 15% por 2 turnos. |

| 5 | Corte do Manto | Neutro | Físico | 60 | 25 | Um golpe com a asa sob o manto. Reduz em 20% o dano do próximo ataque ofensivo do alvo, por até 2 turnos. |

| 6 | Rastro das Caudas | Fogo | Físico | 90 | 40 | As três caudas atingem juntas. Ao acertar, retiram 10 de Energia do adversário. |

| 7 | Garra do Recomeço | Neutro | Físico | 70 | 30 | Causa 20% mais dano se Renacocó iniciou a ação com menos de 50% do HP máximo. |

| 8 | Chicote da Aurora | Fogo | Físico | 105 | 50 | Uma cauda flamejante golpeia o inimigo, reduzindo sua Velocidade em 15% durante 2 turnos. |

| 9 | Chute dos Céus | Ar | Físico | 85 | 40 | Chute aéreo com 25% de chance de provocar Tonto. |

| 10 | Toque da Brasa | Fogo | Físico | 65 | 30 | Ao acertar, a próxima habilidade de cura de Renacocó custa 10 de Energia a menos, por até 2 turnos próprios. |

| 11 | Ninho das Cinzas | Fogo | Suporte | — | 35 | Cria um santuário por 3 turnos da equipe. Ao final de cada turno do galeto ativo, restaura 3% do HP máximo dele. Não acumula. |

| 12 | Refúgio do Manto | Neutro | Suporte | — | 35 | Envolve Renacocó no manto e reduz em 30% o próximo dano direto recebido, por até 2 turnos. |

| 13 | Asas da Vigília | Fogo | Suporte | — | 40 | Concede +20% em ambas as Defesas ao próprio Renacocó ou a um aliado da reserva quando entrar, durante 2 turnos do beneficiado. |

| 14 | Fogo de Amparo | Fogo | Suporte | — | 50 | Cura 18% do HP máximo de Renacocó ou de um aliado na reserva e reduz o próximo dano direto recebido pelo alvo em 20%. |

| 15 | Descanso na Brasa | Fogo | Suporte | — | 45 | Renacocó recupera 16% do HP máximo e ganha +15% de Defesa Mágica durante 2 turnos. |

| 16 | Ninho de Passagem | Fogo | Suporte | — | 45 | Prepara uma proteção para um aliado na reserva, que absorve dano equivalente a 20% do HP máximo dele após entrar em campo. |

| 17 | Brisa Despertadora | Ar | Suporte | — | 40 | Remove Sono de Renacocó ou de uma reserva e concede +25% de Velocidade por 2 turnos do beneficiado. |

| 18 | Chama Reparadora | Fogo | Suporte | — | 40 | Remove Queimadura de Renacocó ou de uma reserva e cura 12% do HP máximo do escolhido. |

| 19 | Brasa Compartilhada | Fogo | Suporte | — | 45 | Renacocó sacrifica 15% do próprio HP máximo para curar 25% do HP máximo de um aliado na reserva. |

| 20 | Coro das Três Chamas | Fogo | Suporte | — | 70 | As três caudas brilham juntas, curando simultaneamente Renacocó e todos os aliados vivos da reserva em 8% de seus respectivos HP máximos. |

| 21 | Pacto da Retomada | Fogo | Suporte | — | 45 | Marca uma reserva. Se entrar nas próximas 2 rodadas, seu primeiro ataque ofensivo que acertar em até 2 ações recupera 12% do próprio HP máximo. |

| 22 | Escolta das Nuvens | Ar | Suporte | — | 40 | Prepara a próxima troca da equipe. O próximo aliado que entrar em até 2 rodadas recebe cura-base de 12% do HP máximo e +10% de Velocidade por 2 turnos. |

| 23 | Oração do Retorno | Fogo | Suporte | — | 45 | Recupera 15 de Energia de um aliado na reserva e lhe concede +15% de Defesa Mágica durante seus primeiros 2 turnos após entrar. |

| 24 | Guarda da Primeira Luz | Fogo | Suporte | — | 35 | Protege Renacocó ou uma reserva contra a próxima aplicação de um estado negativo, durante até 2 turnos do beneficiado após a ativação ou entrada. |

| 25 | Cinza da Trégua | Neutro | Suporte | — | 50 | Reduz simultaneamente o Ataque Físico e o Ataque Mágico de um adversário em 20% por 2 turnos dele. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #020 Frankocó

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Épico · **Elementos:** Terra + Elétrico · **Peso natural registrado:** 28,0 kg

**Fonte anterior:** `Galetario_020_Frankoco_OFICIAL_2026-11-12.json`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 135 |

| Ataque Físico | 110 |

| Defesa Física | 115 |

| Ataque Mágico | 30 |

| Defesa Mágica | 85 |

| Velocidade | 35 |

| **Total calculado** | **510** |

## Passiva oficial vigente

**Passiva: Instinto de Reconstrução**

**Último Remendo:** Uma vez por Rinha, ao sobreviver a ataque que deixa HP em 25% do máximo ou menos, concede blindagem de 14% do HP máximo. Não cura, não remove estados, não adiciona golpes.

**Limiar dos atributos:** [{"hp_percentual": "<=75", "bonus": {"+Defesa Física (%)": 15}}, {"hp_percentual": "<=50", "bonus": {"+Ataque Físico (%)": 15}}, {"hp_percentual": "<=25", "bonus": {"+Defesa Mágica (%)": 15}}]

**Restrições:** Bônus cumulativos nos limiares correspondentes, removidos ao recuperar HP acima de cada limite. Não alteram modelo anatômico.

## Registro da homologação de balanceamento

- **blindagem única, baseada em HP máximo:** 15% HP máximo → **14% HP máximo**. Os bônus dos limiares de HP de +15% permanecem iguais.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| 1 | Garra Afiada | Neutro | Físico | 40 | 0 | Ataque básico ofensivo universal, sem efeito adicional informado. |

| 2 | Concentração | Neutro | Suporte | — | 0 | Recupera Energia e concede buff aleatório; 20% de chance de remover estado negativo, segundo a regra global. |

| 3 | Costura Tectônica | Terra | Físico | 85 | 40 | Ao acertar, aplica Marca de Sutura ao alvo por até 2 turnos próprios de Frankocó. Se o alvo marcado causar dano direto a Frankocó, consome-se a marca e prepara-se +20% de dano no próximo golpe físico ofensivo de Frankocó usado nos 2 turnos próprios seguintes; o bônus consome-se no primeiro acerto físico válido. Uma marca por Frankocó, sem acúmulo; desaparece se alvo sair de campo; não cura nem adiciona acertos. |

| 4 | Curto Galvânico | Elétrico | Físico | 85 | 45 | Ao acertar, aplica Circuito Travado: +10 Energia ao próximo golpe ofensivo adversário se HP de Frankocó >75%; +15 se ≤75%; +20 se ≤50%; +25 se ≤25%, segundo HP no acerto. Marca dura até dois turnos do adversário, consome-se quando utiliza próximo golpe ofensivo, não afeta Concentração nem suporte, não acumula, no máximo uma aplicação por ação, desaparece ao sair alvo de campo. Se custo exceder Energia disponível, golpe não pode ser usado. |

| 5 | Coração da Última Tempestade | Elétrico | Físico | 115 | 70 | Exclusivo/hereditário. Memória dos Impactos: se Frankocó recebeu dano direto desde a última ação, prepara uma carga não acumulável. Ao acertar, +20% dano final no primeiro acerto válido e gera blindagem de 10% de seu HP máximo durante até 2 turnos próprios ou até ser consumida. Sem dano direto prévio, apenas P115. Carga reinicia após próxima ação, usada ou não; bônus uma vez por ação; não gera acertos extras. Se Último Remendo já existir, não soma blindagens: mantém a de maior valor. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| 1 | Martelo de Estratos | Terra | Físico | 95 | 40 | Ao acertar, 25% de chance de reduzir Defesa Física do alvo em 15% por 2 turnos dele. |

| 2 | Bico de Bobina | Elétrico | Físico | 65 | 25 | Ao acertar, 20% de chance de aplicar Paralisia. |

| 3 | Pisada de Ancoragem | Terra | Físico | 80 | 35 | Ao acertar, reduz Velocidade do alvo em 20% por 2 turnos dele. |

| 4 | Choque dos Rebites | Elétrico | Físico | 100 | 45 | Se o alvo estiver sob Circuito Travado, causa +15% dano final; não consome a marca. |

| 5 | Asa Desparafusadora | Neutro | Físico | 75 | 30 | Ao acertar, remove um bônus temporário positivo de Defesa Física do alvo, sem afetar passivas. |

| 6 | Ombro de Cascalho | Terra | Físico | 85 | 35 | Ao acertar, reduz Ataque Físico do adversário em 15% por 2 turnos dele. |

| 7 | Garra de Escória | Fogo | Físico | 85 | 40 | Ao acertar, 20% de chance de aplicar Queimadura. |

| 8 | Trava de Indução | Elétrico | Físico | 75 | 35 | Ao acertar, retira 10 de Energia do inimigo, uma vez por ação. |

| 9 | Colisão de Pedreira | Terra | Físico | 110 | 55 | Se Frankocó estiver com HP ≤25% quando selecionar o golpe, custo reduzido de 55 para 45 Energia. |

| 10 | Punho dos Rebites | Neutro | Físico | 70 | 30 | Se alvo tiver blindagem, remove da proteção valor igual a até 5% do HP máximo do alvo antes do dano normal; efeito extra não causa dano ao HP. |

| 11 | Chassi de Argila | Terra | Suporte | — | 35 | Concede +20% Defesa Mágica a Frankocó ou a aliado na reserva por 2 turnos do beneficiário, iniciados quando ele entrar em campo se for reserva. |

| 12 | Rebitagem de Emergência | Terra | Suporte | — | 45 | Concede blindagem de 12% do HP máximo de Frankocó por 2 turnos próprios ou até consumida; não acumula com suas outras blindagens, prevalece a maior. |

| 13 | Ombreira de Cascalho | Terra | Suporte | — | 40 | Reduz 30% do próximo dano físico direto recebido, se ocorrer em até 2 turnos próprios. |

| 14 | Captador de Faíscas | Elétrico | Suporte | — | 30 | Por até 2 turnos próprios, próximo golpe Elétrico direto recebido causa 20% menos dano e devolve 20 Energia a Frankocó; ativa uma vez. |

| 15 | Circuito Auxiliar | Elétrico | Suporte | — | 35 | Transfere imediatamente 20 Energia para aliado vivo na reserva, respeitando máximo universal 100. |

| 16 | Soltura de Engrenagens | Neutro | Suporte | — | 35 | Remove Tonto de Frankocó ou aliado na reserva e concede +15% Velocidade por 2 turnos do beneficiário. |

| 17 | Ímã de Retenção | Elétrico | Suporte | — | 40 | Prepara por 2 turnos próprios resposta ao próximo golpe físico direto recebido: reduz Velocidade do atacante em 20% por 2 turnos dele. Ativa uma vez. |

| 18 | Bobina de Reserva | Elétrico | Suporte | — | 30 | No início do próximo turno próprio, se Frankocó estiver em campo, recupera +45 Energia além dos +20 universais; não acumula com outra Bobina de Reserva. |

| 19 | Fivelas de Reserva | Terra | Suporte | — | 35 | Por até 2 turnos próprios, prepara proteção que reduz 25% do primeiro dano direto que, sem essa proteção, retiraria ao menos 15% do HP máximo. Ativa uma vez. |

| 20 | Descarga Depuradora | Elétrico | Suporte | — | 45 | Remove um estado negativo de Frankocó ou de aliado na reserva e concede 10 Energia ao beneficiário; não cura HP nem excede 100 Energia. |

| 21 | Campo de Fendas | Terra | Suporte | — | 45 | Instala armadilha com uma carga no lado adversário: próximo inimigo que entrar perde 5% de HP máximo e 10 Energia. Persiste até ativar ou ser removida pela técnica universal de remoção de armadilhas; não acumula consigo mesma. |

| 22 | Sinal de Revezamento | Elétrico | Suporte | — | 40 | Se um aliado entrar em campo nos próximos 2 turnos da equipe, recebe 10 Energia e +15% Defesa Física por 2 turnos próprios. Consome na primeira entrada válida. |

| 23 | Arco de Interferência | Elétrico | Suporte | — | 45 | Marca inimigo por até 2 turnos dele. Se usar Suporte, após executar golpe perde +15 Energia; ativa uma vez, não acumula e desaparece ao sair alvo de campo. Não impede a utilização da técnica. |

| 24 | Selo Antissutura | Terra | Suporte | — | 40 | Marca adversário por até 2 turnos dele. Próxima cura recebida (ativa ou passiva) tem eficácia reduzida em 40%, consumindo marca; desaparece se alvo sair. Marca específica, não novo status negativo universal. |

| 25 | Polaridade de Retorno | Elétrico | Suporte | — | 40 | Prepara por até 2 turnos próprios uma reação. Ao receber dano mágico direto, o próximo golpe físico ofensivo de Frankocó terá custo reduzido em 20 Energia, mínimo 0, se usado nos 2 turnos próprios seguintes. Ativa uma vez. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.


---

# GALETOCRAFT — GALETÁRIO OFICIAL #021 Cabacocó

**Status:** OFICIAL — ficha consolidada com balanceamento aprovado em 12/11/2026.

**Raridade:** Épico · **Elementos:** Planta + Terra · **Peso natural registrado:** 18,0 kg

**Fonte anterior:** `Galetario_021_Cabacoco_OFICIAL_2026-11-12.json`. Conteúdo anterior preservado como histórico.

## Atributos-base (nível 50)

| Atributo | Valor |

|---|---:|

| HP | 110 |

| Ataque Físico | 25 |

| Defesa Física | 75 |

| Ataque Mágico | 130 |

| Defesa Mágica | 115 |

| Velocidade | 45 |

| **Total calculado** | **500** |

## Passiva oficial vigente

**Passiva: Maldição do Lar Faminto**

**Gatilho:** Ao acertar golpe que explicitamente aplica uma maldição, impõe Selo da Cabana ao adversário

**Selo da Cabana:** perda de **3,5% do HP máximo por turno**; **reduz em 45% a cura recebida**.

**Demais regras do Selo:** {"duracao": "até 2 turnos próprios do alvo", "alcance": "somente inimigo ativo alvo", "empilhamento": "não acumula; técnica válida pode renovar duração", "ao_sair_de_campo": "desaparece", "consideracoes": "reduz também regeneração passiva; Selo não é novo estado negativo universal; não afeta reservas"}

## Registro da homologação de balanceamento

- **perda periódica de HP e redução de cura:** 4% HP máximo/turno; -50% cura → **3,5% HP máximo/turno; -45% cura**. Duração, gatilho, dispensa após troca e confinamento não foram alterados.

## Cinco golpes de origem / referência

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| 1 | Crina Poderosa | Neutro | mágico | 40 | 0 | Ataque mágico básico universal; sem efeito adicional. |

| 2 | Concentração | Neutro/sem elemento | suporte | — | 0 | Técnica universal de suporte que recupera Energia, concede bônus aleatório e tem 20% de chance de remover estado negativo, conforme sistema global aprovado; obrigatoriamente equipada. |

| 3 | Sussurro do Assoalho | Planta | mágico | 65 | 35 | Após acerto aplica maldição ativadora do Selo da Cabana da passiva (duração até 2 turnos do alvo); 20% de chance de Envenenamento, testada somente uma vez por ação. |

| 4 | Pátio Sem Saída | Terra | suporte | — | 50 | Confinamento Territorial do adversário por 2 turnos próprios dele, impedindo trocas voluntárias; pode ser removido por limpeza universal de armadilhas. Golpes, itens e Concentração continuam permitidos. Troca obrigatória após derrota sempre permitida e encerra confinamento. Após encerramento/remoção, a vítima tem oportunidade de agir com troca livre antes de nova prisão. |

| 5 | Veredito da Porta Fechada | Terra | mágico | 110 | 70 | Golpe mágico P110. Se ao acertar o alvo estiver simultaneamente sob Selo da Cabana e Confinamento Territorial, o primeiro acerto válido recebe +20% de dano final, tem 25% de chance de Tonto (teste uma vez por ação) e consome o Selo após o acerto; não cria acertos extras. |

## Vinte e cinco golpes adicionais aprendíveis

| ID/Slot | Nome | Elemento | Categoria | Poder | Energia | Efeito oficial |

|---|---|---|---|---:|---:|---|

| G007 | Sopro de Cinzas | Fogo | mágico | 65 | 30 | Acertar inimigo sob Chuva causa poder 80 em vez de 65; se não chover, 20% de chance de Queimadura após dano. |

| G035 | Perfume Ácido | Planta | mágico | 60 | 25 | Após dano tem 20% de Envenenamento; se o alvo estiver sob Santuário das Raízes e já Envenenado, em vez disso reduz Ataque Mágico em 8% por 1 ação. |

| G036 | Néctar Corrosivo | Planta | mágico | 80 | 40 | Após causar dano reduz Defesa Mágica em 12% por 2 ações; se atingir alvo com bônus positivo de Defesa Mágica, remove primeiro o bônus mais recente, sem aplicar a redução. |

| G037 | Espiral de Clorofila | Planta | mágico | 100 | 45 | Se o usuário curou um aliado da reserva desde sua última ação, poder 120 em vez de 100; de outro modo, concede 8 de energia ao usuário após dano sob Santuário das Raízes. |

| G038 | Chuva de Folhas-Lança | Planta | mágico | 125 | 75 | Após causar dano, 20% de Envenenamento; se já estiver Envenenado, transfere uma redução temporária de Ataque Mágico do usuário para o alvo, caso exista, sem duplicá-la. |

| G049 | Lodo Pressurizado | Terra | mágico | 65 | 30 | Após causar dano reduz Defesa Mágica em 10% por 2 ações; se o alvo estiver sob Chuva, em vez disso reduz Defesa Física em 10% por 1 ação. |

| G050 | Ondulação Rochosa | Terra | mágico | 85 | 35 | Quando o alvo possui Velocidade superior à do usuário, poder 100 em vez de 85; após dano, retira 5 pontos de energia do alvo. |

| G051 | Fenda da Garganta | Terra | mágico | 105 | 50 | Após causar dano 15% de Tonto; contra alvo com peso até 100% do natural, poder sobe de 105 para 120 sem alterar a chance. |

| G052 | Erupção de Geodo | Terra | mágico | 130 | 70 | Se o alvo possui proteção temporária contra dano mágico, poder 145 em vez de 130; após dano, consome a proteção normalmente, sem apagá-la antes do ataque. |

| G063 | Assobio Rasante | Ar | mágico | 65 | 25 | Após causar dano reduz Ataque Mágico em 8% por 2 ações; se o alvo estiver sob uma proteção de Suporte, a redução é de 12% por apenas 1 ação. |

| G065 | Cone de Vácuo | Ar | mágico | 105 | 50 | Após dano reduz Velocidade do alvo em 12% por 2 ações; sob Ventania, em vez disso recupera 10 de energia própria e reduz Velocidade em 8% por 1 ação. |

| G066 | Aurora do Zênite | Ar | mágico | 130 | 70 | Se o alvo recebeu um segundo golpe desde sua última ação, poder 150 em vez de 130; caso contrário, 10% de chance de Tonto após dano. |

| G093 | Grito Harmônico | Neutro | mágico | 90 | 40 | Após causar dano reduz Ataque Mágico em 12% por 1 ação; se Ventania estiver ativa, a redução passa para 8% por 2 ações. |

| N016 | Pedra da Impaciência | Terra | mágico | 75 | 45 | Poder 100, em vez de 75, se a última ação efetivamente executada pelo alvo, antes desta, foi um golpe de Suporte (incluindo Concentração). |

| G039 | Hino das Raízes | Planta | suporte | — | 35 | Invoca Santuário das Raízes por 4 rodadas; se uma armadilha inimiga estiver ativa, reduz em 10% o dano da próxima entrada de um aliado por troca voluntária, sem remover a armadilha. |

| G040 | Armadilha de Pólen | Planta | suporte | — | 45 | Instala armadilha persistente que reduz o Ataque Mágico do entrante voluntário em 12% por suas 2 próximas ações; se já estiver Envenenado, reduz 18% em vez disso, sem acumular. |

| G053 | Tambor da Areia | Terra | suporte | — | 30 | Invoca Tempestade de Areia por 4 rodadas; se substituir Ventania, o usuário ganha 10% de Defesa Física até sua próxima ação. |

| G055 | Ninho de Pedregulhos | Terra | suporte | — | 45 | Instala armadilha persistente que causa 8% do HP máximo do entrante voluntário; se ele estiver acima de 120% do peso natural, causa 11%, sem afetar entradas obrigatórias. |

| G098 | Cocoricó Desafiador | Sem elemento | suporte | — | 35 | Reduz Ataque Físico e Ataque Mágico do inimigo em 8% pelas próximas 2 ações; se ele estiver Tonto, reduz só 5% mas devolve 10 de energia ao usuário. |

| G109 | Seiva de Ferro | Planta | suporte | — | 60 | Eleva as duas Defesas próprias em 18% por 2 ações; no Santuário das Raízes, a primeira redução de atributo recebida é ignorada, sem impedir estados negativos. |

| G121 | Resina nas Articulações | Planta | suporte | — | 45 | Reduz Ataque Físico do alvo em 18% por 2 ações dele; se o alvo tentar um segundo acerto por Velocidade durante a redução, a penalidade é 25% apenas naquele segundo acerto. |

| G124 | Quebra-Ímpeto | Terra | suporte | — | 70 | Exige alvo com estado negativo persistente; reduz seu Ataque Físico em 25% e Velocidade em 8% por 1 ação, sem reaplicar nem remover o estado. |

| G133 | Pólen Desarmônico | Planta | suporte | — | 45 | Reduz Defesa Mágica do alvo em 18% por 2 ações; se Santuário das Raízes estiver ativo, cura 5% do HP máximo do usuário ao aplicar a redução, uma vez. |

| G136 | Silêncio do Selo | Neutro | suporte | — | 70 | Exige alvo com estado negativo persistente; reduz Defesa Mágica em 25% por 1 ação e reduz em 5 pontos percentuais a chance de ativação da próxima defesa especial válida do alvo, sem mudar o limiar de 120%. |

| G141 | Dissipação Absoluta | Neutro | suporte | — | 35 | Remove todos os bônus temporários positivos de atributos do inimigo ativo; se remover pelo menos 2 efeitos distintos, recupera 8 de energia própria após execução; não remove clima, Santuário, armadilhas, passivas ou equipamentos. |

## Política de preservação

- Concentração continua obrigatória entre os cinco golpes equipados, com os quatro outros espaços configuráveis conforme o repertório homologado.

- Nenhuma modificação a atributos, poder/custo/efeito dos golpes, raridade, peso, aparência, itens ou genética foi autorizada nesta etapa.

- A fonte integral, inclusive metadados, progressões, restrições e descrições, está preservada no JSON consolidado; esta ficha Markdown é uma visualização legível de seus campos principais.

- Simulação experimental NÃO comprova implementação no mod Java/NeoForge.

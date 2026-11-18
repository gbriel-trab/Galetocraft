# GALETOCRAFT — GALETÁRIO OFICIAL CONSOLIDADO
**Data:** 11/11/2026 · **Edição:** Beta 1.2.36 derivada · **Unidade:** Cocorídeos
**Escopo:** 14 fichas completas e 1 ficha em desenvolvimento (#015). Reúne 218 movimentos documentados (212 centrais + 6 originais externos), 25 aprendíveis por espécie (350 atribuídos + 25 pré-selecionados).

> **Política de integridade:** nenhum dado homologado foi substituído por suposição. Valores históricos divergentes são sinalizados. As fichas de #013 e #014 continuam separadas do cadastro jogável principal, mas suas referências oficiais passam a estar consultáveis no Galetário. #015 não tem kit de origem completo nem implementação confirmada.

## Escala atual de raridades (nível 50)
| Raridade | Mín. | Referência | Máx. |
|---|---:|---:|---:|
| Comum | 350 | 370 | 390 |
| Raro | 410 | 430 | 450 |
| Épico | 470 | 490 | 510 |
| Mítico | 530 | 550 | 570 |
| Lendário | 590 | 610 | 630 |

**Atenção ao histórico:** a coluna `species` antiga contém totais de 850 para os iniciais #001–#006, incompatíveis com a escala atual de Mítico (550). A apresentação usa os quadros naturais v0.3 explicitamente vinculados à escala atual; o dado histórico de 850 continua preservado no banco e deve ser resolvido em revisão própria.

## Visão geral
| # | Cocorídeo | Elementos | Raridade | Base nível 50 | Peso natural | Ficha | Originais | Aprendíveis |
|---:|---|---|---|---:|---:|---|---:|---:|
| #001 | Pirococó | Fogo | Mítico | 550 | 5.8 kg | ficha_completa_homologada | 5 | 25 |
| #002 | Cocórrego | Água | Mítico | 550 | 8.0 kg | ficha_completa_homologada | 5 | 25 |
| #003 | Esporocó | Planta | Mítico | 550 | 5.0 kg | ficha_completa_homologada | 5 | 25 |
| #004 | Cocórak | Terra | Mítico | 550 | 10.0 kg | ficha_completa_homologada | 5 | 25 |
| #005 | Cocórion | Ar | Mítico | 550 | 3.8 kg | ficha_completa_homologada | 5 | 25 |
| #006 | Cocórvolt | Elétrico | Mítico | 550 | 5.2 kg | ficha_completa_homologada | 5 | 25 |
| #007 | Taturico | Terra | Comum | 370 | 7.5 kg | ficha_completa_homologada | 5 | 25 |
| #008 | Axococó | Água | Comum | 370 | 5.8 kg | ficha_completa_homologada | 5 | 25 |
| #009 | Vagaló | Elétrico | Comum | 370 | 3.1 kg | ficha_completa_homologada | 5 | 25 |
| #010 | Morcegalo | Ar | Comum | 370 | 5.2 kg | ficha_completa_homologada | 5 | 25 |
| #011 | Espinhocó | Planta | Comum | 370 | 6.2 kg | ficha_completa_homologada | 5 | 25 |
| #012 | Salambrasa | Fogo | Comum | 370 | 6.4 kg | ficha_completa_homologada | 5 | 25 |
| #013 | Quartzaló | Terra + Elétrico | Comum | 370 | 8.5 kg | ficha_completa_homologada | 5 | 25 |
| #014 | Carangocó | Água + Terra | Comum | 370 | 10.5 kg | ficha_completa_homologada | 5 | 25 |
| #015 | Faíscocó | Fogo + Elétrico | Raro | 430 | Pendente | em_desenvolvimento | 0 | 25 |

## Regras transversais referenciadas
- **Rinhas:** movimentos ofensivos por ação sujeitos ao limite global de dois, salvo exceções próprias homologadas (ex.: Cerco das Pinças); não criar novos acertos por combinação de efeitos.
- **Energia:** reserva máxima 100, recuperação base 20 no início do próprio turno, custo pago por uso; Concentração permanece como slot fixo de suporte.
- **Repertório:** cinco movimentos equipáveis; cinco de origem por ficha completa; 25 aprendíveis adicionais. Após desbloqueio, quatro slots podem ser escolhidos; Concentração permanece.
- **Elementos:** Fogo, Água, Planta, Terra, Ar, Elétrico e ataques Neutros/sem elemento; aprendizados fora da tipagem podem ser visualmente justificados.
- **Climas e Santuários:** coexistência de um clima e um santuário; durações e modificadores consultáveis em tabelas canônicas, não alterados pela consolidação.
- **Galeria:** cruzamentos entre espécies diferentes têm regra de descendência 50% espécie da mãe / 50% espécie do pai, sem híbridos. Parceiros compatíveis não foram classificados individualmente.
- **Pena de Captura:** no mundo exige mira, botão direito com a Pena na mão e linha de visão livre de blocos sólidos; feixe simplificado absorve via rubi central. Alcance, chance, duração e falha não definidos pela regra de linha de visão.

## Fichas individuais

### #001 — Pirococó · Fogo
**Estado:** ficha_completa_homologada · **Raridade natural:** Mítico · **Base no nível 50:** 550 · **Peso natural:** 5.8 kg
**Identidade de Rinha:** mago fênix / fogo e renascimento
**Seis atributos:** HP: 90 · Ataque Físico: 35 · Defesa Física: 60 · Ataque Mágico: 185 · Defesa Mágica: 95 · Velocidade: 85
**Passiva:** Chama Reencarnada [oficial]
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
**Arte oficial (referência, sem redesenho):** None
**Evolução:** Lendário (ver dados completos no JSON).

**Cinco golpes de origem imutáveis**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|
| 1 | crina_poderosa | Crina Poderosa | Neutro | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 2 | concentracao | Concentração | — | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 3 | cococombustao | Cocócombustão | Fogo | 70 | 30 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 4 | penas_de_brasa | Penas de Brasa | Fogo | 100 | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 5 | ave_fenix | Ave Fênix | Fogo | 180 | 100 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

**25 golpes aprendíveis atribuídos**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G006 | Faísca de Terreiro | Fogo | mágico | 40 | 0 | Não | campo/clima e sinergia |
| 02 | G007 | Sopro de Cinzas | Fogo | mágico | 65 | 30 | Não | campo/clima e sinergia |
| 03 | G008 | Rosácea de Fagulhas | Fogo | mágico | 85 | 40 | Não | controle de atributos |
| 04 | G009 | Coração de Fornalha | Fogo | mágico | 110 | 55 | Não | controle de atributos |
| 05 | G010 | Estouro de Magma | Fogo | mágico | 130 | 75 | Não | campo/clima e sinergia |
| 06 | G011 | Chamado do Meio-Dia | Fogo | suporte | — | 30 | Não | campo/clima e sinergia |
| 07 | G012 | Retorno de Cinzas | Fogo | suporte | — | 35 | Não | ritmo, esquiva ou duplo golpe |
| 08 | G013 | Cinzas da Discórdia | Fogo | suporte | — | 35 | Não | pressão por estado |
| 09 | G014 | Reacender | Fogo | suporte | — | 40 | Não | campo/clima e sinergia |
| 10 | G117 | Manto da Fornalha | Fogo | Suporte | — | 75 | Não | campo/clima e sinergia |
| 11 | G119 | Coração de Duas Chamas | Fogo | Suporte | — | 85 | Não | campo/clima e sinergia |
| 12 | G131 | Cinza nos Olhos | Fogo | Suporte | — | 65 | Não | campo/clima e sinergia |
| 13 | N002 | Cinza Desarmadora | Fogo | mágico | 70 | 45 | Não | dano e cobertura |
| 14 | N003 | Fornalha Resguardada | Fogo | suporte | — | 40 | Não | pressão por estado |
| 15 | N004 | Brilho de Carvão | Fogo | mágico | 80 | 45 | Não | campo/clima e sinergia |
| 16 | G062 | Sopro Circular | Ar | mágico | 40 | 0 | Sim | campo/clima e sinergia |
| 17 | G063 | Assobio Rasante | Ar | mágico | 65 | 25 | Sim | controle de atributos |
| 18 | G066 | Aurora do Zênite | Ar | mágico | 130 | 70 | Sim | ritmo, esquiva ou duplo golpe |
| 19 | G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Sim | campo/clima e sinergia |
| 20 | G070 | Redemoinho de Penas | Ar | suporte | — | 45 | Sim | cerco e armadilhas |
| 21 | G114 | Tempestade Interior | Ar | Suporte | — | 70 | Sim | campo/clima e sinergia |
| 22 | N019 | Pena de Eco | Ar | mágico | 85 | 40 | Sim | ritmo, esquiva ou duplo golpe |
| 23 | G093 | Grito Harmônico | Neutro | mágico | 90 | 40 | Não | campo/clima e sinergia |
| 24 | G097 | Cuidado de Plumagem | Sem elemento | suporte | — | 40 | Não | revezamento e apoio |
| 25 | G002 | Espora Incandescente | Fogo | físico | 65 | 30 | Não | pressão por estado |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G006 — Faísca de Terreiro (E0)** — Se Ensolarado estiver ativo, o projétil básico tem 15% de chance de reduzir Ataque Mágico do alvo em 8% por 1 ação; caso contrário, dano normal. **Visual:** Pirococó canaliza a técnica através de crina fênix e penas em chamas; a animação destaca crina flamejante de três pontas, respeitando seu design homologado.
02. **G007 — Sopro de Cinzas (E30)** — Acertar inimigo sob Chuva causa poder 80 em vez de 65; se não chover, 20% de chance de Queimadura após dano. **Visual:** Pirococó canaliza a técnica através de crina fênix e penas em chamas; a animação destaca asas em forma de capa, respeitando seu design homologado.
03. **G008 — Rosácea de Fagulhas (E40)** — Se o alvo tiver bônus positivo de Ataque Mágico, reduz esse bônus pela metade durante o cálculo do dano deste golpe; não remove o bônus depois. **Visual:** Pirococó canaliza a técnica através de crina fênix e penas em chamas; a animação destaca armadura violeta e dourada, respeitando seu design homologado.
04. **G009 — Coração de Fornalha (E55)** — Após causar dano, se o usuário tiver menos de 50 de energia, recebe +10% de Defesa Mágica até sua próxima ação; não acumula. **Visual:** Pirococó canaliza a técnica através de crina fênix e penas em chamas; a animação destaca braseiro das penas, respeitando seu design homologado.
05. **G010 — Estouro de Magma (E75)** — Se Ensolarado estiver ativo, tem 25% de chance de Queimadura; sem Ensolarado, caso cause dano, reduz a energia do alvo em 10, uma vez por ação. **Visual:** Pirococó canaliza a técnica através de crina fênix e penas em chamas; a animação destaca crina flamejante de três pontas, respeitando seu design homologado.
06. **G011 — Chamado do Meio-Dia (E30)** — Invoca Ensolarado por 4 rodadas; se substituir Chuva, concede +10% de Defesa Mágica ao usuário até sua próxima ação. **Visual:** Pirococó sustenta a técnica com manto de penas e postura ritual; a animação destaca asas em forma de capa, respeitando seu design homologado.
07. **G012 — Retorno de Cinzas (E35)** — Até o próximo ataque físico direto recebido, reduz seu dano em 20%; se o acerto for o segundo da mesma ação, devolve 25% do dano efetivamente sofrido nesse segundo acerto. **Visual:** Pirococó sustenta a técnica com manto de penas e postura ritual; a animação destaca armadura violeta e dourada, respeitando seu design homologado.
08. **G013 — Cinzas da Discórdia (E35)** — Reduz Ataque Físico do alvo em 12% por suas 2 próximas ações; se ele estiver Queimado, em vez disso reduz 18%, sem acumular. **Visual:** Pirococó sustenta a técnica com manto de penas e postura ritual; a animação destaca braseiro das penas, respeitando seu design homologado.
09. **G014 — Reacender (E40)** — Cura 18% do HP máximo próprio; sob Ensolarado remove também Queimadura do próprio usuário, se existir. **Visual:** Pirococó sustenta a técnica com manto de penas e postura ritual; a animação destaca crina flamejante de três pontas, respeitando seu design homologado.
10. **G117 — Manto da Fornalha (E75)** — Exige Ensolarado ativo; concede +30% às duas Defesas por 2 ações próprias; a primeira tentativa de causar Queimadura no usuário durante esse tempo não altera seu estado, e consome só a proteção contra Queimadura. **Visual:** Pirococó sustenta a técnica com manto de penas e postura ritual; a animação destaca asas em forma de capa, respeitando seu design homologado.
11. **G119 — Coração de Duas Chamas (E85)** — Exige Ensolarado ativo; eleva Ataque Físico e Ataque Mágico em 28% por 1 ação; após qualquer golpe ofensivo que cause dano, perde 8% do HP máximo próprio, sem reduzir abaixo de 1 HP. **Visual:** Pirococó sustenta a técnica com manto de penas e postura ritual; a animação destaca armadura violeta e dourada, respeitando seu design homologado.
12. **G131 — Cinza nos Olhos (E65)** — Exige Ensolarado ativo; reduz Ataque Mágico do alvo em 25% por 1 ação; contra alvo Queimado, redução cai para 12% e dura 2 ações, sem novo estado. **Visual:** Pirococó sustenta a técnica com manto de penas e postura ritual; a animação destaca braseiro das penas, respeitando seu design homologado.
13. **N002 — Cinza Desarmadora (E45)** — Após ao menos um acerto com dano, elimina um bônus temporário positivo de Ataque Mágico do alvo, se houver, escolhendo o mais forte; em empate, o mais antigo. O dano deste golpe é calculado antes da remoção. **Visual:** Pirococó canaliza a técnica através de crina fênix e penas em chamas; a animação destaca crina flamejante de três pontas, respeitando seu design homologado.
14. **N003 — Fornalha Resguardada (E40)** — Remove Queimadura do próprio usuário, caso exista, e concede +20% de Defesa Mágica por suas próximas duas ações próprias. Se não estiver Queimado, concede apenas a proteção. **Visual:** Pirococó sustenta a técnica com manto de penas e postura ritual; a animação destaca asas em forma de capa, respeitando seu design homologado.
15. **N004 — Brilho de Carvão (E45)** — Se o clima Ensolarado estiver ativo no momento do primeiro acerto com dano, o usuário recupera 15 pontos de energia após a ação, respeitando o máximo de 100. **Visual:** Pirococó canaliza a técnica através de crina fênix e penas em chamas; a animação destaca armadura violeta e dourada, respeitando seu design homologado.
16. **G062 — Sopro Circular (E0)** — Quando Ventania estiver ativa, projétil básico tem poder 55 em vez de 40; caso contrário permanece básico sem efeito. **Visual:** Compatibilidade cruzada: Pirococó canaliza a técnica através de crina fênix e penas em chamas; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; braseiro das penas identifica a animação.
17. **G063 — Assobio Rasante (E25)** — Após causar dano reduz Ataque Mágico em 8% por 2 ações; se o alvo estiver sob uma proteção de Suporte, a redução é de 12% por apenas 1 ação. **Visual:** Compatibilidade cruzada: Pirococó canaliza a técnica através de crina fênix e penas em chamas; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; crina flamejante de três pontas identifica a animação.
18. **G066 — Aurora do Zênite (E70)** — Se o alvo recebeu um segundo golpe desde sua última ação, poder 150 em vez de 130; caso contrário, 10% de chance de Tonto após dano. **Visual:** Compatibilidade cruzada: Pirococó canaliza a técnica através de crina fênix e penas em chamas; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; asas em forma de capa identifica a animação.
19. **G067 — Assobio dos Quatro Ventos (E30)** — Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. **Visual:** Compatibilidade cruzada: Pirococó sustenta a técnica com manto de penas e postura ritual; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; armadura violeta e dourada identifica a animação.
20. **G070 — Redemoinho de Penas (E45)** — Instala armadilha persistente que reduz o Ataque Físico do entrante voluntário em 12% por 2 ações; sob Ventania reduz em 15% por 1 ação, sem acumular. **Visual:** Compatibilidade cruzada: Pirococó sustenta a técnica com manto de penas e postura ritual; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; braseiro das penas identifica a animação.
21. **G114 — Tempestade Interior (E70)** — Exige Ventania ativa; concede +25% Velocidade e +15% Ataque Físico por 2 ações; o primeiro segundo acerto executado durante o efeito ignora somente 10% de bônus temporários de Defesa Física adversária. **Visual:** Compatibilidade cruzada: Pirococó sustenta a técnica com manto de penas e postura ritual; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; crina flamejante de três pontas identifica a animação.
22. **N019 — Pena de Eco (E40)** — Se o primeiro ataque deste golpe for totalmente evitado por esquiva do alvo, devolve 15 pontos de energia ao usuário ao terminar a ação (máximo 100). **Visual:** Compatibilidade cruzada: Pirococó canaliza a técnica através de crina fênix e penas em chamas; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; asas em forma de capa identifica a animação.
23. **G093 — Grito Harmônico (E40)** — Após causar dano reduz Ataque Mágico em 12% por 1 ação; se Ventania estiver ativa, a redução passa para 8% por 2 ações. **Visual:** Pirococó canaliza a técnica através de crina fênix e penas em chamas; a animação destaca armadura violeta e dourada, respeitando seu design homologado.
24. **G097 — Cuidado de Plumagem (E40)** — Cura 18% do HP máximo de um aliado vivo, inclusive reserva; se o aliado estiver Envenenado, a cura sobe para 22%, mas não remove o estado. **Visual:** Pirococó sustenta a técnica com manto de penas e postura ritual; a animação destaca braseiro das penas, respeitando seu design homologado.
25. **G002 — Espora Incandescente (E30)** — Após causar dano, 20% de chance de Queimadura; se o alvo já estiver Queimado, reduz sua Defesa Física em 8% pelas próximas 2 ações dele, sem acumular. **Visual:** Pirococó concentra a técnica nas asas e esporas cobertas por brasas; a animação destaca crina flamejante de três pontas, respeitando seu design homologado.

**Divergência histórica a revisar:** tabela species contém 850; base natural v0.3 apresentada soma 550. Os dois registros permanecem rastreados.

### #002 — Cocórrego · Água
**Estado:** ficha_completa_homologada · **Raridade natural:** Mítico · **Base no nível 50:** 550 · **Peso natural:** 8.0 kg
**Identidade de Rinha:** tanque aquático / revanche
**Seis atributos:** HP: 155 · Ataque Físico: 45 · Defesa Física: 135 · Ataque Mágico: 45 · Defesa Mágica: 105 · Velocidade: 65
**Passiva:** Maré de Refluxo [oficial]
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
**Arte oficial (referência, sem redesenho):** None
**Evolução:** Lendário (ver dados completos no JSON).

**Cinco golpes de origem imutáveis**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|
| 1 | garra_afiada | Garra Afiada | Neutro | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 2 | concentracao | Concentração | — | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 3 | revide_das_mares | Revide das Marés | — | — | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 4 | prisao_abissal | Prisão Abissal | Água | 65 | 75 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 5 | punho_da_fortaleza | Punho da Fortaleza | Água | 90 | 50 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

**25 golpes aprendíveis atribuídos**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G015 | Bico de Marola | Água | físico | 40 | 0 | Não | pressão por estado |
| 02 | G016 | Cauda de Ressaca | Água | físico | 60 | 25 | Não | campo/clima e sinergia |
| 03 | G017 | Pancada de Maré | Água | físico | 80 | 35 | Não | dano condicional |
| 04 | G018 | Açoite de Corredeira | Água | físico | 95 | 50 | Não | pressão por estado |
| 05 | G019 | Quebra-Cais | Água | físico | 120 | 55 | Não | gestão de energia |
| 06 | G020 | Gota Disparada | Água | mágico | 40 | 0 | Não | sustentação |
| 07 | G022 | Coluna de Espuma | Água | mágico | 80 | 40 | Não | pressão por estado |
| 08 | G023 | Vórtice Azul | Água | mágico | 100 | 50 | Não | controle de atributos |
| 09 | G024 | Tsunami de Bolhas | Água | mágico | 130 | 70 | Não | campo/clima e sinergia |
| 10 | G025 | Canto das Nuvens | Água | suporte | — | 30 | Não | campo/clima e sinergia |
| 11 | G026 | Névoa Protetora | Água | suporte | — | 30 | Não | pressão por estado |
| 12 | G027 | Maré de Retirada | Água | suporte | — | 40 | Não | cerco e armadilhas |
| 13 | G028 | Banho Reparador | Água | suporte | — | 40 | Não | revezamento e apoio |
| 14 | N005 | Fôlego de Ressaca | Água | físico | 70 | 40 | Não | pressão por estado |
| 15 | N006 | Redemoinho Exaustivo | Água | suporte | — | 45 | Não | cerco e armadilhas |
| 16 | N007 | Banho Sereno | Água | suporte | — | 45 | Não | sustentação |
| 17 | N008 | Pressão do Manancial | Água | mágico | 70 | 45 | Não | gestão de energia |
| 18 | G044 | Marreta de Barro | Terra | físico | 65 | 30 | Sim | campo/clima e sinergia |
| 19 | G054 | Muralha Escavada | Terra | suporte | — | 35 | Sim | campo/clima e sinergia |
| 20 | G056 | Pedra de Revezamento | Terra | suporte | — | 35 | Sim | cerco e armadilhas |
| 21 | G102 | Couraça do Subsolo | Terra | Suporte | — | 45 | Sim | controle de atributos |
| 22 | N013 | Pisada de Lastro | Terra | físico | 75 | 45 | Sim | dano condicional |
| 23 | N014 | Coluna de Guarda | Terra | suporte | — | 40 | Sim | controle de atributos |
| 24 | G097 | Cuidado de Plumagem | Sem elemento | suporte | — | 40 | Não | revezamento e apoio |
| 25 | G100 | Terreiro Purificado | Sem elemento | suporte | — | 45 | Não | cerco e armadilhas |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G015 — Bico de Marola (E0)** — Se o usuário estiver Afogado, poder sobe de 40 para 55 no primeiro acerto; não reduz nem remove Afogamento. **Visual:** Cocórrego concentra a técnica nas asas pesadas e maré concentrada; a animação destaca asas robustas no lugar de braços, respeitando seu design homologado.
02. **G016 — Cauda de Ressaca (E25)** — Após causar dano, reduz Velocidade do alvo em 12% por 2 ações; sob Chuva, reduz apenas 8%, mas recupera 10 de energia ao final da ação. **Visual:** Cocórrego concentra a técnica nas asas pesadas e maré concentrada; a animação destaca quimono azul de ondas, respeitando seu design homologado.
03. **G017 — Pancada de Maré (E35)** — Se o alvo entrou voluntariamente neste turno, poder sobe de 80 para 100; caso contrário, após causar dano ignora o próximo efeito de redução de Velocidade do usuário até sua próxima ação. **Visual:** Cocórrego concentra a técnica nas asas pesadas e maré concentrada; a animação destaca cauda volumosa em marés, respeitando seu design homologado.
04. **G018 — Açoite de Corredeira (E50)** — Após causar dano, 18% de chance de Afogamento; se o alvo já estava Afogado, em vez de tentar aplicar o estado drena 12 de energia. **Visual:** Cocórrego concentra a técnica nas asas pesadas e maré concentrada; a animação destaca porte largo e defensivo, respeitando seu design homologado.
05. **G019 — Quebra-Cais (E55)** — Contra alvo com mais de 70 de energia, poder 135 em vez de 120; após causar dano nessa condição, o usuário não pode receber bônus temporário de Velocidade até sua próxima ação. **Visual:** Cocórrego concentra a técnica nas asas pesadas e maré concentrada; a animação destaca asas robustas no lugar de braços, respeitando seu design homologado.
06. **G020 — Gota Disparada (E0)** — Se o usuário recebeu cura desde sua ação anterior, poder 55 em vez de 40; não ativa curas adicionais. **Visual:** Cocórrego canaliza a técnica através de ondas que percorrem o quimono e a cauda; a animação destaca quimono azul de ondas, respeitando seu design homologado.
07. **G022 — Coluna de Espuma (E40)** — Após causar dano tem 20% de chance de Afogamento; se o usuário possuir bônus temporário de Defesa Mágica, a chance cai para 10%, mas poder sobe para 95. **Visual:** Cocórrego canaliza a técnica através de ondas que percorrem o quimono e a cauda; a animação destaca cauda volumosa em marés, respeitando seu design homologado.
08. **G023 — Vórtice Azul (E50)** — Se o inimigo já tiver Ataque Físico reduzido, poder 115 em vez de 100; caso contrário aplica −12% de Ataque Físico por 2 ações após dano. **Visual:** Cocórrego canaliza a técnica através de ondas que percorrem o quimono e a cauda; a animação destaca porte largo e defensivo, respeitando seu design homologado.
09. **G024 — Tsunami de Bolhas (E70)** — Sob Chuva, poder 145 em vez de 130; sem Chuva, após causar dano, 15% de chance de reduzir Velocidade do alvo em 15% por 1 ação. **Visual:** Cocórrego canaliza a técnica através de ondas que percorrem o quimono e a cauda; a animação destaca asas robustas no lugar de braços, respeitando seu design homologado.
10. **G025 — Canto das Nuvens (E30)** — Invoca Chuva por 4 rodadas; caso substitua Ensolarado, cura 8% do HP máximo próprio sem afetar a reserva. **Visual:** Cocórrego sustenta a técnica com postura de guardião das águas; a animação destaca quimono azul de ondas, respeitando seu design homologado.
11. **G026 — Névoa Protetora (E30)** — O aliado escolhido recebe −25% de dano mágico na próxima ação ofensiva recebida; se já estiver Afogado, recupera 12 de energia ao ativar a barreira. **Visual:** Cocórrego sustenta a técnica com postura de guardião das águas; a animação destaca cauda volumosa em marés, respeitando seu design homologado.
12. **G027 — Maré de Retirada (E40)** — Troca voluntariamente por aliado da reserva; o entrante recupera 8% de HP máximo e não sofre redução de Velocidade de armadilha somente nessa entrada; outros efeitos de armadilha permanecem. **Visual:** Cocórrego sustenta a técnica com postura de guardião das águas; a animação destaca porte largo e defensivo, respeitando seu design homologado.
13. **G028 — Banho Reparador (E40)** — Cura 20% do HP máximo de um aliado vivo, inclusive reserva; se o alvo estiver com menos de 30% do HP, acrescenta mais 5%, uma única vez. **Visual:** Cocórrego sustenta a técnica com postura de guardião das águas; a animação destaca asas robustas no lugar de braços, respeitando seu design homologado.
14. **N005 — Fôlego de Ressaca (E40)** — Se o alvo já tiver Afogamento no início desta ação e ao menos um acerto causar dano, o usuário recupera 15 pontos de energia ao terminar a ação (máximo 100). **Visual:** Cocórrego concentra a técnica nas asas pesadas e maré concentrada; a animação destaca quimono azul de ondas, respeitando seu design homologado.
15. **N006 — Redemoinho Exaustivo (E45)** — Instala no lado adversário uma armadilha persistente que retira 15 pontos da energia atual de cada Cocorídeo que entra por troca voluntária, nunca abaixo de zero. **Visual:** Cocórrego sustenta a técnica com postura de guardião das águas; a animação destaca cauda volumosa em marés, respeitando seu design homologado.
16. **N007 — Banho Sereno (E45)** — Recupera 10% do HP máximo do usuário ativo e remove o estado negativo persistente que ele tenha, se houver. **Visual:** Cocórrego sustenta a técnica com postura de guardião das águas; a animação destaca porte largo e defensivo, respeitando seu design homologado.
17. **N008 — Pressão do Manancial (E45)** — Poder 95, em vez de 70, se o alvo tiver 40 ou menos pontos de energia atual no momento do cálculo do primeiro acerto. **Visual:** Cocórrego canaliza a técnica através de ondas que percorrem o quimono e a cauda; a animação destaca asas robustas no lugar de braços, respeitando seu design homologado.
18. **G044 — Marreta de Barro (E30)** — Após dano reduz Velocidade em 15% por 2 ações; se uma Tempestade de Areia estiver ativa, duração cai para 1 ação e reduz também Defesa Física em 8%. **Visual:** Compatibilidade cruzada: Cocórrego concentra a técnica nas asas pesadas e maré concentrada; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; quimono azul de ondas identifica a animação.
19. **G054 — Muralha Escavada (E35)** — Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. **Visual:** Compatibilidade cruzada: Cocórrego sustenta a técnica com postura de guardião das águas; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; cauda volumosa em marés identifica a animação.
20. **G056 — Pedra de Revezamento (E35)** — Troca usuário por aliado da reserva; o entrante recebe +15% de Defesa Física pelas próximas 2 ações e, sob Tempestade de Areia, ignora o dano de uma armadilha apenas na entrada da troca. **Visual:** Compatibilidade cruzada: Cocórrego sustenta a técnica com postura de guardião das águas; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; porte largo e defensivo identifica a animação.
21. **G102 — Couraça do Subsolo (E45)** — Eleva Defesa Física do usuário em 22% por 2 ações próprias; se estiver acima de 120% do peso natural, reduz também em 10% o dano do primeiro acerto físico recebido. **Visual:** Compatibilidade cruzada: Cocórrego sustenta a técnica com postura de guardião das águas; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; asas robustas no lugar de braços identifica a animação.
22. **N013 — Pisada de Lastro (E45)** — Poder 100, em vez de 75, se o peso do usuário for igual ou superior a 120% de seu peso natural de referência no retrato de início da Rinha. **Visual:** Compatibilidade cruzada: Cocórrego concentra a técnica nas asas pesadas e maré concentrada; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; quimono azul de ondas identifica a animação.
23. **N014 — Coluna de Guarda (E40)** — O próximo ataque direto recebido pelo próprio usuário ativo terá 20%, em vez de 10%, de chance de ativar a defesa especial, SOMENTE se a Defesa relevante for pelo menos 120% do Ataque correspondente. A redução ao ativar continua 75%. **Visual:** Compatibilidade cruzada: Cocórrego sustenta a técnica com postura de guardião das águas; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; cauda volumosa em marés identifica a animação.
24. **G097 — Cuidado de Plumagem (E40)** — Cura 18% do HP máximo de um aliado vivo, inclusive reserva; se o aliado estiver Envenenado, a cura sobe para 22%, mas não remove o estado. **Visual:** Cocórrego sustenta a técnica com postura de guardião das águas; a animação destaca porte largo e defensivo, respeitando seu design homologado.
25. **G100 — Terreiro Purificado (E45)** — Remove integralmente todas as armadilhas e cargas do lado do usuário; se pelo menos uma armadilha foi removida, recupera 10 de energia após a execução. **Visual:** Cocórrego sustenta a técnica com postura de guardião das águas; a animação destaca asas robustas no lugar de braços, respeitando seu design homologado.

**Divergência histórica a revisar:** tabela species contém 850; base natural v0.3 apresentada soma 550. Os dois registros permanecem rastreados.

### #003 — Esporocó · Planta
**Estado:** ficha_completa_homologada · **Raridade natural:** Mítico · **Base no nível 50:** 550 · **Peso natural:** 5.0 kg
**Identidade de Rinha:** mago de suporte / veneno e flores
**Seis atributos:** HP: 120 · Ataque Físico: 25 · Defesa Física: 65 · Ataque Mágico: 115 · Defesa Mágica: 145 · Velocidade: 80
**Passiva:** Simbiose Venenosa [oficial]
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
**Arte oficial (referência, sem redesenho):** None
**Evolução:** Lendário (ver dados completos no JSON).

**Cinco golpes de origem imutáveis**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|
| 1 | crina_poderosa | Crina Poderosa | Neutro | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 2 | concentracao | Concentração | — | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 3 | esporos_venenosos | Esporos Venenosos | Planta | 70 | 40 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 4 | polen_revigorante | Pólen Revigorante | — | — | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 5 | jardim_da_discordia | Jardim da Discórdia | — | — | 80 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

**25 golpes aprendíveis atribuídos**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G034 | Semente Atirada | Planta | mágico | 40 | 0 | Não | campo/clima e sinergia |
| 02 | G035 | Perfume Ácido | Planta | mágico | 60 | 25 | Não | campo/clima e sinergia |
| 03 | G036 | Néctar Corrosivo | Planta | mágico | 80 | 40 | Não | controle de atributos |
| 04 | G037 | Espiral de Clorofila | Planta | mágico | 100 | 45 | Não | campo/clima e sinergia |
| 05 | G038 | Chuva de Folhas-Lança | Planta | mágico | 125 | 75 | Não | pressão por estado |
| 06 | G039 | Hino das Raízes | Planta | suporte | — | 35 | Não | cerco e armadilhas |
| 07 | G040 | Armadilha de Pólen | Planta | suporte | — | 45 | Não | cerco e armadilhas |
| 08 | G041 | Fotossíntese de Poleiro | Planta | suporte | — | 45 | Não | campo/clima e sinergia |
| 09 | G042 | Casca Compartilhada | Planta | suporte | — | 30 | Não | ritmo, esquiva ou duplo golpe |
| 10 | G109 | Seiva de Ferro | Planta | Suporte | — | 60 | Não | campo/clima e sinergia |
| 11 | G113 | Pétalas de Conquista | Planta | Suporte | — | 70 | Não | campo/clima e sinergia |
| 12 | G121 | Resina nas Articulações | Planta | Suporte | — | 45 | Não | ritmo, esquiva ou duplo golpe |
| 13 | G133 | Pólen Desarmônico | Planta | Suporte | — | 45 | Não | campo/clima e sinergia |
| 14 | G138 | Raízes na Espora | Planta | Suporte | — | 55 | Não | cerco e armadilhas |
| 15 | N009 | Espinho de Revezamento | Planta | físico | 75 | 45 | Não | revezamento e apoio |
| 16 | N010 | Seiva de Retaguarda | Planta | mágico | 65 | 45 | Não | campo/clima e sinergia |
| 17 | N011 | Vinha Antirrasante | Planta | suporte | — | 40 | Não | ritmo, esquiva ou duplo golpe |
| 18 | N012 | Casco de Bromélia | Planta | físico | 70 | 45 | Não | controle de atributos |
| 19 | G020 | Gota Disparada | Água | mágico | 40 | 0 | Sim | sustentação |
| 20 | G021 | Orvalho Cortante | Água | mágico | 60 | 20 | Sim | campo/clima e sinergia |
| 21 | G025 | Canto das Nuvens | Água | suporte | — | 30 | Sim | campo/clima e sinergia |
| 22 | G026 | Névoa Protetora | Água | suporte | — | 30 | Sim | pressão por estado |
| 23 | G028 | Banho Reparador | Água | suporte | — | 40 | Sim | revezamento e apoio |
| 24 | N007 | Banho Sereno | Água | suporte | — | 45 | Sim | sustentação |
| 25 | G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Sim | campo/clima e sinergia |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G034 — Semente Atirada (E0)** — Se Santuário das Raízes estiver ativo, concede 5 de energia ao usuário após causar dano; caso contrário, ataque mágico básico normal. **Visual:** Esporocó canaliza a técnica através de flores, esporos e pólen da crista; a animação destaca flores rosas, respeitando seu design homologado.
02. **G035 — Perfume Ácido (E25)** — Após dano tem 20% de Envenenamento; se o alvo estiver sob Santuário das Raízes e já Envenenado, em vez disso reduz Ataque Mágico em 8% por 1 ação. **Visual:** Esporocó canaliza a técnica através de flores, esporos e pólen da crista; a animação destaca crista de folhas vermelhas, respeitando seu design homologado.
03. **G036 — Néctar Corrosivo (E40)** — Após causar dano reduz Defesa Mágica em 12% por 2 ações; se atingir alvo com bônus positivo de Defesa Mágica, remove primeiro o bônus mais recente, sem aplicar a redução. **Visual:** Esporocó canaliza a técnica através de flores, esporos e pólen da crista; a animação destaca plumagem verde folhosa, respeitando seu design homologado.
04. **G037 — Espiral de Clorofila (E45)** — Se o usuário curou um aliado da reserva desde sua última ação, poder 120 em vez de 100; de outro modo, concede 8 de energia ao usuário após dano sob Santuário das Raízes. **Visual:** Esporocó canaliza a técnica através de flores, esporos e pólen da crista; a animação destaca pólen aromático, respeitando seu design homologado.
05. **G038 — Chuva de Folhas-Lança (E75)** — Após causar dano, 20% de Envenenamento; se já estiver Envenenado, transfere uma redução temporária de Ataque Mágico do usuário para o alvo, caso exista, sem duplicá-la. **Visual:** Esporocó canaliza a técnica através de flores, esporos e pólen da crista; a animação destaca flores rosas, respeitando seu design homologado.
06. **G039 — Hino das Raízes (E35)** — Invoca Santuário das Raízes por 4 rodadas; se uma armadilha inimiga estiver ativa, reduz em 10% o dano da próxima entrada de um aliado por troca voluntária, sem remover a armadilha. **Visual:** Esporocó sustenta a técnica com coroa de folhas e flores curativas; a animação destaca crista de folhas vermelhas, respeitando seu design homologado.
07. **G040 — Armadilha de Pólen (E45)** — Instala armadilha persistente que reduz o Ataque Mágico do entrante voluntário em 12% por suas 2 próximas ações; se já estiver Envenenado, reduz 18% em vez disso, sem acumular. **Visual:** Esporocó sustenta a técnica com coroa de folhas e flores curativas; a animação destaca plumagem verde folhosa, respeitando seu design homologado.
08. **G041 — Fotossíntese de Poleiro (E45)** — Cura 20% do HP máximo de um aliado vivo; no Santuário das Raízes, cura também 5% do HP máximo do usuário ativo quando o alvo for outro aliado. **Visual:** Esporocó sustenta a técnica com coroa de folhas e flores curativas; a animação destaca pólen aromático, respeitando seu design homologado.
09. **G042 — Casca Compartilhada (E30)** — Concede ao aliado selecionado −20% dano mágico na próxima ação ofensiva recebida; se a ação tiver segundo acerto, nele a proteção sobe para 35%. **Visual:** Esporocó sustenta a técnica com coroa de folhas e flores curativas; a animação destaca flores rosas, respeitando seu design homologado.
10. **G109 — Seiva de Ferro (E60)** — Eleva as duas Defesas próprias em 18% por 2 ações; no Santuário das Raízes, a primeira redução de atributo recebida é ignorada, sem impedir estados negativos. **Visual:** Esporocó sustenta a técnica com coroa de folhas e flores curativas; a animação destaca crista de folhas vermelhas, respeitando seu design homologado.
11. **G113 — Pétalas de Conquista (E70)** — Exige Santuário das Raízes ativo; concede +22% Ataque Mágico e +15% Defesa Física por 2 ações próprias; a próxima cura própria não pode ultrapassar 15% do HP máximo proveniente deste bônus. **Visual:** Esporocó sustenta a técnica com coroa de folhas e flores curativas; a animação destaca plumagem verde folhosa, respeitando seu design homologado.
12. **G121 — Resina nas Articulações (E45)** — Reduz Ataque Físico do alvo em 18% por 2 ações dele; se o alvo tentar um segundo acerto por Velocidade durante a redução, a penalidade é 25% apenas naquele segundo acerto. **Visual:** Esporocó sustenta a técnica com coroa de folhas e flores curativas; a animação destaca pólen aromático, respeitando seu design homologado.
13. **G133 — Pólen Desarmônico (E45)** — Reduz Defesa Mágica do alvo em 18% por 2 ações; se Santuário das Raízes estiver ativo, cura 5% do HP máximo do usuário ao aplicar a redução, uma vez. **Visual:** Esporocó sustenta a técnica com coroa de folhas e flores curativas; a animação destaca flores rosas, respeitando seu design homologado.
14. **G138 — Raízes na Espora (E55)** — Exige Santuário das Raízes ativo; reduz Velocidade do alvo em 22% por 1 ação; se houver armadilha no lado dele, duração sobe para 2 ações, sem adicionar cargas de armadilha. **Visual:** Esporocó sustenta a técnica com coroa de folhas e flores curativas; a animação destaca crista de folhas vermelhas, respeitando seu design homologado.
15. **N009 — Espinho de Revezamento (E45)** — Poder 105, em vez de 75, contra alvo que entrou por troca voluntária neste mesmo turno, antes da execução do golpe. **Visual:** Esporocó concentra a técnica nas ramos compactados nas asas; a animação destaca plumagem verde folhosa, respeitando seu design homologado.
16. **N010 — Seiva de Retaguarda (E45)** — Se Santuário das Raízes estiver ativo e ao menos um acerto causar dano, cura 8% do HP máximo do aliado vivo na reserva com menor proporção de HP atual. **Visual:** Esporocó canaliza a técnica através de flores, esporos e pólen da crista; a animação destaca pólen aromático, respeitando seu design homologado.
17. **N011 — Vinha Antirrasante (E40)** — Protege o próprio usuário ativo contra a próxima ação ofensiva recebida: reduz 15% do dano do primeiro acerto e 60% do dano do eventual segundo acerto dessa mesma ação. **Visual:** Esporocó sustenta a técnica com coroa de folhas e flores curativas; a animação destaca flores rosas, respeitando seu design homologado.
18. **N012 — Casco de Bromélia (E45)** — Poder 95, em vez de 70, se a Defesa Física efetiva do usuário for ao menos 120% do Ataque Físico efetivo do alvo no momento da resolução. **Visual:** Esporocó concentra a técnica nas ramos compactados nas asas; a animação destaca crista de folhas vermelhas, respeitando seu design homologado.
19. **G020 — Gota Disparada (E0)** — Se o usuário recebeu cura desde sua ação anterior, poder 55 em vez de 40; não ativa curas adicionais. **Visual:** Compatibilidade cruzada: Esporocó canaliza a técnica através de flores, esporos e pólen da crista; condensa umidade do ambiente, respingos, névoa ou líquido próximo. O elemento do golpe continua Água; plumagem verde folhosa identifica a animação.
20. **G021 — Orvalho Cortante (E20)** — Após causar dano, se Chuva estiver ativa recupera 8 de energia; se não estiver, reduz Defesa Mágica inimiga em 6% até a próxima ação do alvo. **Visual:** Compatibilidade cruzada: Esporocó canaliza a técnica através de flores, esporos e pólen da crista; condensa umidade do ambiente, respingos, névoa ou líquido próximo. O elemento do golpe continua Água; pólen aromático identifica a animação.
21. **G025 — Canto das Nuvens (E30)** — Invoca Chuva por 4 rodadas; caso substitua Ensolarado, cura 8% do HP máximo próprio sem afetar a reserva. **Visual:** Compatibilidade cruzada: Esporocó sustenta a técnica com coroa de folhas e flores curativas; condensa umidade do ambiente, respingos, névoa ou líquido próximo. O elemento do golpe continua Água; flores rosas identifica a animação.
22. **G026 — Névoa Protetora (E30)** — O aliado escolhido recebe −25% de dano mágico na próxima ação ofensiva recebida; se já estiver Afogado, recupera 12 de energia ao ativar a barreira. **Visual:** Compatibilidade cruzada: Esporocó sustenta a técnica com coroa de folhas e flores curativas; condensa umidade do ambiente, respingos, névoa ou líquido próximo. O elemento do golpe continua Água; crista de folhas vermelhas identifica a animação.
23. **G028 — Banho Reparador (E40)** — Cura 20% do HP máximo de um aliado vivo, inclusive reserva; se o alvo estiver com menos de 30% do HP, acrescenta mais 5%, uma única vez. **Visual:** Compatibilidade cruzada: Esporocó sustenta a técnica com coroa de folhas e flores curativas; condensa umidade do ambiente, respingos, névoa ou líquido próximo. O elemento do golpe continua Água; plumagem verde folhosa identifica a animação.
24. **N007 — Banho Sereno (E45)** — Recupera 10% do HP máximo do usuário ativo e remove o estado negativo persistente que ele tenha, se houver. **Visual:** Compatibilidade cruzada: Esporocó sustenta a técnica com coroa de folhas e flores curativas; condensa umidade do ambiente, respingos, névoa ou líquido próximo. O elemento do golpe continua Água; pólen aromático identifica a animação.
25. **G067 — Assobio dos Quatro Ventos (E30)** — Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. **Visual:** Compatibilidade cruzada: Esporocó sustenta a técnica com coroa de folhas e flores curativas; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; flores rosas identifica a animação.

**Divergência histórica a revisar:** tabela species contém 850; base natural v0.3 apresentada soma 550. Os dois registros permanecem rastreados.

### #004 — Cocórak · Terra
**Estado:** ficha_completa_homologada · **Raridade natural:** Mítico · **Base no nível 50:** 550 · **Peso natural:** 10.0 kg
**Identidade de Rinha:** brutamontes do deserto / peso e sacrifício
**Seis atributos:** HP: 140 · Ataque Físico: 180 · Defesa Física: 80 · Ataque Mágico: 25 · Defesa Mágica: 70 · Velocidade: 55
**Passiva:** Fúria do Deserto [oficial]
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
**Arte oficial (referência, sem redesenho):** None
**Evolução:** Lendário (ver dados completos no JSON).

**Cinco golpes de origem imutáveis**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|
| 1 | garra_afiada | Garra Afiada | Neutro | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 2 | concentracao | Concentração | — | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 3 | punho_das_dunas | Punho das Dunas | Terra | 110 | 60 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 4 | prisao_das_areias | Prisão das Areias | Terra | 75 | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 5 | sepultamento_do_deserto | Sepultamento do Deserto | Terra | 200 | 100 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

**25 golpes aprendíveis atribuídos**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G043 | Chute de Cascalho | Terra | físico | 40 | 0 | Não | dano condicional |
| 02 | G044 | Marreta de Barro | Terra | físico | 65 | 30 | Não | campo/clima e sinergia |
| 03 | G045 | Cabeçada de Basalto | Terra | físico | 85 | 35 | Não | controle de atributos |
| 04 | G046 | Pisão Sísmico | Terra | físico | 100 | 50 | Não | pressão por estado |
| 05 | G047 | Lança de Obsidiana | Terra | físico | 120 | 55 | Não | controle de atributos |
| 06 | G053 | Tambor da Areia | Terra | suporte | — | 30 | Não | campo/clima e sinergia |
| 07 | G054 | Muralha Escavada | Terra | suporte | — | 35 | Não | campo/clima e sinergia |
| 08 | G055 | Ninho de Pedregulhos | Terra | suporte | — | 45 | Não | cerco e armadilhas |
| 09 | G056 | Pedra de Revezamento | Terra | suporte | — | 35 | Não | cerco e armadilhas |
| 10 | G111 | Trono de Cascalho | Terra | Suporte | — | 70 | Não | cerco e armadilhas |
| 11 | G116 | Fúria da Bigorna | Terra | Suporte | — | 65 | Não | controle de atributos |
| 12 | G124 | Quebra-Ímpeto | Terra | Suporte | — | 70 | Não | controle de atributos |
| 13 | G126 | Areia nos Encaixes | Terra | Suporte | — | 55 | Não | campo/clima e sinergia |
| 14 | G128 | Fissura Absoluta | Terra | Suporte | — | 70 | Não | sustentação |
| 15 | N013 | Pisada de Lastro | Terra | físico | 75 | 45 | Não | dano condicional |
| 16 | N014 | Coluna de Guarda | Terra | suporte | — | 40 | Não | controle de atributos |
| 17 | N015 | Cinzel Quebra-Manto | Terra | físico | 80 | 55 | Não | controle de atributos |
| 18 | N016 | Pedra da Impaciência | Terra | mágico | 75 | 45 | Não | dano condicional |
| 19 | G002 | Espora Incandescente | Fogo | físico | 65 | 30 | Sim | pressão por estado |
| 20 | G003 | Galope de Carvão | Fogo | físico | 85 | 35 | Sim | cerco e armadilhas |
| 21 | G004 | Garra Vulcânica | Fogo | físico | 95 | 50 | Sim | pressão por estado |
| 22 | G005 | Quebra-Forja | Fogo | físico | 115 | 65 | Sim | sustentação |
| 23 | N001 | Brasa de Rebate | Fogo | físico | 75 | 45 | Sim | cerco e armadilhas |
| 24 | G106 | Forja das Esporas | Fogo | Suporte | — | 60 | Sim | pressão por estado |
| 25 | G123 | Rugido de Sufoco | Ar | Suporte | — | 65 | Sim | controle de atributos |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G043 — Chute de Cascalho (E0)** — Se o alvo tiver peso atual superior a 120% do natural, poder 55 em vez de 40; não altera peso. **Visual:** Cocórak concentra a técnica nas cauda-braço e pés pesados; a animação destaca cauda-braço curvada, respeitando seu design homologado.
02. **G044 — Marreta de Barro (E30)** — Após dano reduz Velocidade em 15% por 2 ações; se uma Tempestade de Areia estiver ativa, duração cai para 1 ação e reduz também Defesa Física em 8%. **Visual:** Cocórak concentra a técnica nas cauda-braço e pés pesados; a animação destaca crista vermelha volumosa, respeitando seu design homologado.
03. **G045 — Cabeçada de Basalto (E35)** — Poder 105 em vez de 85 contra alvo com bônus positivo de Defesa Física; não remove bônus nem ignora defesa-base. **Visual:** Cocórak concentra a técnica nas cauda-braço e pés pesados; a animação destaca marcas em espiral nas penas, respeitando seu design homologado.
04. **G046 — Pisão Sísmico (E50)** — Após causar dano, 20% de chance de Tonto; se o alvo já estiver Tonto, em vez de tentar novo estado reduz sua energia em 12. **Visual:** Cocórak concentra a técnica nas cauda-braço e pés pesados; a animação destaca massa de areia do deserto, respeitando seu design homologado.
05. **G047 — Lança de Obsidiana (E55)** — Ignora 20% de bônus temporários de Defesa Física; se o usuário sofreu dano de estado desde sua última ação, poder 135 em vez de 120. **Visual:** Cocórak concentra a técnica nas cauda-braço e pés pesados; a animação destaca cauda-braço curvada, respeitando seu design homologado.
06. **G053 — Tambor da Areia (E30)** — Invoca Tempestade de Areia por 4 rodadas; se substituir Ventania, o usuário ganha 10% de Defesa Física até sua próxima ação. **Visual:** Cocórak sustenta a técnica com cauda como muralha de areia; a animação destaca crista vermelha volumosa, respeitando seu design homologado.
07. **G054 — Muralha Escavada (E35)** — Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. **Visual:** Cocórak sustenta a técnica com cauda como muralha de areia; a animação destaca marcas em espiral nas penas, respeitando seu design homologado.
08. **G055 — Ninho de Pedregulhos (E45)** — Instala armadilha persistente que causa 8% do HP máximo do entrante voluntário; se ele estiver acima de 120% do peso natural, causa 11%, sem afetar entradas obrigatórias. **Visual:** Cocórak sustenta a técnica com cauda como muralha de areia; a animação destaca massa de areia do deserto, respeitando seu design homologado.
09. **G056 — Pedra de Revezamento (E35)** — Troca usuário por aliado da reserva; o entrante recebe +15% de Defesa Física pelas próximas 2 ações e, sob Tempestade de Areia, ignora o dano de uma armadilha apenas na entrada da troca. **Visual:** Cocórak sustenta a técnica com cauda como muralha de areia; a animação destaca cauda-braço curvada, respeitando seu design homologado.
10. **G111 — Trono de Cascalho (E70)** — Exige Tempestade de Areia ativa; concede +25% Defesa Física e +15% Defesa Mágica por 2 ações próprias e impede que uma armadilha retire energia do usuário nesse período, sem remover armadilhas. **Visual:** Cocórak sustenta a técnica com cauda como muralha de areia; a animação destaca crista vermelha volumosa, respeitando seu design homologado.
11. **G116 — Fúria da Bigorna (E65)** — Eleva Ataque Físico próprio em 35% por 1 ação; enquanto o bônus durar, reduz a própria Defesa Mágica em 12%, ambos os efeitos terminando juntos e sem acumular. **Visual:** Cocórak sustenta a técnica com cauda como muralha de areia; a animação destaca marcas em espiral nas penas, respeitando seu design homologado.
12. **G124 — Quebra-Ímpeto (E70)** — Exige alvo com estado negativo persistente; reduz seu Ataque Físico em 25% e Velocidade em 8% por 1 ação, sem reaplicar nem remover o estado. **Visual:** Cocórak sustenta a técnica com cauda como muralha de areia; a animação destaca massa de areia do deserto, respeitando seu design homologado.
13. **G126 — Areia nos Encaixes (E55)** — Exige Tempestade de Areia ativa; reduz Defesa Física do alvo em 22% por 1 ação; se o alvo pesar mais de 120% do natural, duração sobe para 2 ações. **Visual:** Cocórak sustenta a técnica com cauda como muralha de areia; a animação destaca cauda-braço curvada, respeitando seu design homologado.
14. **G128 — Fissura Absoluta (E70)** — Exige alvo com estado negativo persistente; reduz Defesa Física em 25% por 1 ação e impede apenas a recuperação de energia proveniente de golpes nessa ação, sem impedir regeneração universal. **Visual:** Cocórak sustenta a técnica com cauda como muralha de areia; a animação destaca crista vermelha volumosa, respeitando seu design homologado.
15. **N013 — Pisada de Lastro (E45)** — Poder 100, em vez de 75, se o peso do usuário for igual ou superior a 120% de seu peso natural de referência no retrato de início da Rinha. **Visual:** Cocórak concentra a técnica nas cauda-braço e pés pesados; a animação destaca marcas em espiral nas penas, respeitando seu design homologado.
16. **N014 — Coluna de Guarda (E40)** — O próximo ataque direto recebido pelo próprio usuário ativo terá 20%, em vez de 10%, de chance de ativar a defesa especial, SOMENTE se a Defesa relevante for pelo menos 120% do Ataque correspondente. A redução ao ativar continua 75%. **Visual:** Cocórak sustenta a técnica com cauda como muralha de areia; a animação destaca massa de areia do deserto, respeitando seu design homologado.
17. **N015 — Cinzel Quebra-Manto (E55)** — Ao calcular o dano, ignora 50% apenas da parcela positiva dos bônus temporários de Defesa Física do alvo; a Defesa Física básica e demais modificadores continuam aplicados. **Visual:** Cocórak concentra a técnica nas cauda-braço e pés pesados; a animação destaca cauda-braço curvada, respeitando seu design homologado.
18. **N016 — Pedra da Impaciência (E45)** — Poder 100, em vez de 75, se a última ação efetivamente executada pelo alvo, antes desta, foi um golpe de Suporte (incluindo Concentração). **Visual:** Cocórak canaliza a técnica através de espirais de areia e rocha expelidas; a animação destaca crista vermelha volumosa, respeitando seu design homologado.
19. **G002 — Espora Incandescente (E30)** — Após causar dano, 20% de chance de Queimadura; se o alvo já estiver Queimado, reduz sua Defesa Física em 8% pelas próximas 2 ações dele, sem acumular. **Visual:** Compatibilidade cruzada: Cocórak concentra a técnica nas cauda-braço e pés pesados; gera calor por atrito, cinzas ou brasas do ambiente. O elemento do golpe continua Fogo; marcas em espiral nas penas identifica a animação.
20. **G003 — Galope de Carvão (E35)** — Se o usuário sofreu dano de armadilha desde sua última ação, poder 105 em vez de 85; acerto bem-sucedido não remove a armadilha. **Visual:** Compatibilidade cruzada: Cocórak concentra a técnica nas cauda-braço e pés pesados; gera calor por atrito, cinzas ou brasas do ambiente. O elemento do golpe continua Fogo; massa de areia do deserto identifica a animação.
21. **G004 — Garra Vulcânica (E50)** — Ao causar dano contra alvo com bônus positivo de Defesa Física, remove apenas o bônus mais recente e tem 15% de causar Queimadura. **Visual:** Compatibilidade cruzada: Cocórak concentra a técnica nas cauda-braço e pés pesados; gera calor por atrito, cinzas ou brasas do ambiente. O elemento do golpe continua Fogo; cauda-braço curvada identifica a animação.
22. **G005 — Quebra-Forja (E65)** — Atinge com poder normal e ignora 30% da parcela positiva de bônus temporários de Defesa Física do alvo; se não houver bônus, recupera 10 de energia após a ação. **Visual:** Compatibilidade cruzada: Cocórak concentra a técnica nas cauda-braço e pés pesados; gera calor por atrito, cinzas ou brasas do ambiente. O elemento do golpe continua Fogo; crista vermelha volumosa identifica a animação.
23. **N001 — Brasa de Rebate (E45)** — Poder 100, em vez de 75, se o usuário recebeu dano físico direto desde sua última ação própria, estando ativo. Verificação na resolução; não inclui dano de estados, passivas ou armadilhas. **Visual:** Compatibilidade cruzada: Cocórak concentra a técnica nas cauda-braço e pés pesados; gera calor por atrito, cinzas ou brasas do ambiente. O elemento do golpe continua Fogo; marcas em espiral nas penas identifica a animação.
24. **G106 — Forja das Esporas (E60)** — Eleva Ataque Físico e Defesa Física próprios em 20% por 2 ações próprias; se estiver Queimado, concede apenas +25% de Defesa Física, sem anular a penalidade de Ataque da Queimadura. **Visual:** Compatibilidade cruzada: Cocórak sustenta a técnica com cauda como muralha de areia; gera calor por atrito, cinzas ou brasas do ambiente. O elemento do golpe continua Fogo; massa de areia do deserto identifica a animação.
25. **G123 — Rugido de Sufoco (E65)** — Exige que alvo tenha executado golpe físico em sua última ação; reduz Ataque Físico dele em 28% por 1 ação, sem impedir novos ataques. **Visual:** Compatibilidade cruzada: Cocórak sustenta a técnica com cauda como muralha de areia; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; cauda-braço curvada identifica a animação.

**Divergência histórica a revisar:** tabela species contém 850; base natural v0.3 apresentada soma 550. Os dois registros permanecem rastreados.

### #005 — Cocórion · Ar
**Estado:** ficha_completa_homologada · **Raridade natural:** Mítico · **Base no nível 50:** 550 · **Peso natural:** 3.8 kg
**Identidade de Rinha:** agressor físico veloz / esquiva
**Seis atributos:** HP: 80 · Ataque Físico: 155 · Defesa Física: 65 · Ataque Mágico: 30 · Defesa Mágica: 55 · Velocidade: 165
**Passiva:** Dançarino dos Ventos [oficial]
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
**Arte oficial (referência, sem redesenho):** None
**Evolução:** Lendário (ver dados completos no JSON).

**Cinco golpes de origem imutáveis**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|
| 1 | garra_afiada | Garra Afiada | Neutro | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 2 | concentracao | Concentração | — | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 3 | laminas_de_vento | Lâminas de Vento | Ar | 85 | 50 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 4 | danca_dos_vendavais | Dança dos Vendavais | Ar | 120 | 70 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 5 | julgamento_dos_ceus | Julgamento dos Céus | Ar | 160 | 90 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

**25 golpes aprendíveis atribuídos**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G057 | Asa Riscante | Ar | físico | 40 | 0 | Não | ritmo, esquiva ou duplo golpe |
| 02 | G058 | Pluma de Corte | Ar | físico | 60 | 25 | Não | ritmo, esquiva ou duplo golpe |
| 03 | G059 | Bicada Turbilhão | Ar | físico | 80 | 35 | Não | campo/clima e sinergia |
| 04 | G060 | Rasgo de Altitude | Ar | físico | 100 | 50 | Não | pressão por estado |
| 05 | G061 | Queda do Falcão | Ar | físico | 125 | 70 | Não | dano condicional |
| 06 | G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Não | campo/clima e sinergia |
| 07 | G068 | Corrente de Evasão | Ar | suporte | — | 35 | Não | ritmo, esquiva ou duplo golpe |
| 08 | G069 | Túnel de Retorno | Ar | suporte | — | 35 | Não | revezamento e apoio |
| 09 | G070 | Redemoinho de Penas | Ar | suporte | — | 45 | Não | cerco e armadilhas |
| 10 | G105 | Passo de Vendaval | Ar | Suporte | — | 45 | Não | ritmo, esquiva ou duplo golpe |
| 11 | G108 | Caçada Cortavento | Ar | Suporte | — | 60 | Não | ritmo, esquiva ou duplo golpe |
| 12 | G118 | Dança do Zênite | Ar | Suporte | — | 75 | Não | campo/clima e sinergia |
| 13 | G123 | Rugido de Sufoco | Ar | Suporte | — | 65 | Não | controle de atributos |
| 14 | N017 | Pluma Vazia | Ar | mágico | 70 | 45 | Não | dano condicional |
| 15 | N018 | Vórtice de Passagem | Ar | suporte | — | 45 | Não | cerco e armadilhas |
| 16 | N019 | Pena de Eco | Ar | mágico | 85 | 40 | Não | ritmo, esquiva ou duplo golpe |
| 17 | N020 | Rasante do Azarão | Ar | físico | 70 | 45 | Não | dano condicional |
| 18 | G071 | Bicada Elétrica | Elétrico | físico | 40 | 0 | Sim | pressão por estado |
| 19 | G072 | Espora de Cobre | Elétrico | físico | 65 | 30 | Sim | pressão por estado |
| 20 | G073 | Investida do Dínamo | Elétrico | físico | 85 | 35 | Sim | gestão de energia |
| 21 | G074 | Cascata de Centelhas | Elétrico | físico | 100 | 50 | Sim | campo/clima e sinergia |
| 22 | G002 | Espora Incandescente | Fogo | físico | 65 | 30 | Sim | pressão por estado |
| 23 | G086 | Patada Rasteira | Neutro | físico | 50 | 25 | Não | pressão por estado |
| 24 | G088 | Giro de Esporas | Neutro | físico | 85 | 35 | Não | ritmo, esquiva ou duplo golpe |
| 25 | G099 | Passo Firme | Sem elemento | suporte | — | 35 | Não | pressão por estado |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G057 — Asa Riscante (E0)** — Se a Velocidade do usuário superar a do alvo, poder 50 em vez de 40; sem alterar a chance universal de segundo golpe. **Visual:** Cocórion concentra a técnica nas asas cortantes e garras em rasante; a animação destaca asas largas aerodinâmicas, respeitando seu design homologado.
02. **G058 — Pluma de Corte (E25)** — Após dano reduz Defesa Física do alvo em 10% por 1 ação; se a esquiva do usuário foi ativada desde sua última ação, aumenta a redução para 15%. **Visual:** Cocórion concentra a técnica nas asas cortantes e garras em rasante; a animação destaca crista branca espetada, respeitando seu design homologado.
03. **G059 — Bicada Turbilhão (E35)** — Se o alvo usou Suporte na última ação dele, poder 100 em vez de 80; caso contrário recupera 5 de energia após causar dano em Ventania. **Visual:** Cocórion concentra a técnica nas asas cortantes e garras em rasante; a animação destaca marcas vermelhas, respeitando seu design homologado.
04. **G060 — Rasgo de Altitude (E50)** — Após causar dano, 15% de Tonto; se a Velocidade do usuário for menor que a do alvo, poder 115 em vez de 100. **Visual:** Cocórion concentra a técnica nas asas cortantes e garras em rasante; a animação destaca olhos verdes atentos, respeitando seu design homologado.
05. **G061 — Queda do Falcão (E70)** — Se o usuário for pelo menos 50% mais veloz que o alvo, poder 140 em vez de 125; o ataque adicional universal continua sujeito ao bloqueio e ao limite geral. **Visual:** Cocórion concentra a técnica nas asas cortantes e garras em rasante; a animação destaca asas largas aerodinâmicas, respeitando seu design homologado.
06. **G067 — Assobio dos Quatro Ventos (E30)** — Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. **Visual:** Cocórion sustenta a técnica com dança aérea e mudanças bruscas de direção; a animação destaca crista branca espetada, respeitando seu design homologado.
07. **G068 — Corrente de Evasão (E35)** — Concede +8 pontos percentuais de esquiva ao usuário por suas próximas 2 ações; se esquivar efetivamente de um golpe, recupera 12 de energia após a ação ofensiva adversária, uma vez. **Visual:** Cocórion sustenta a técnica com dança aérea e mudanças bruscas de direção; a animação destaca marcas vermelhas, respeitando seu design homologado.
08. **G069 — Túnel de Retorno (E35)** — Troca por aliado da reserva, concedendo-lhe +15% de Velocidade por suas próximas 2 ações; se ele estiver Paralisado, concede somente +10% e não remove a Paralisia. **Visual:** Cocórion sustenta a técnica com dança aérea e mudanças bruscas de direção; a animação destaca olhos verdes atentos, respeitando seu design homologado.
09. **G070 — Redemoinho de Penas (E45)** — Instala armadilha persistente que reduz o Ataque Físico do entrante voluntário em 12% por 2 ações; sob Ventania reduz em 15% por 1 ação, sem acumular. **Visual:** Cocórion sustenta a técnica com dança aérea e mudanças bruscas de direção; a animação destaca asas largas aerodinâmicas, respeitando seu design homologado.
10. **G105 — Passo de Vendaval (E45)** — Concede +22% Velocidade por 2 ações próprias; se o usuário se esquivar completamente de golpe durante esse período, o bônus expira e ele ganha +12% Defesa Física até sua próxima ação. **Visual:** Cocórion sustenta a técnica com dança aérea e mudanças bruscas de direção; a animação destaca crista branca espetada, respeitando seu design homologado.
11. **G108 — Caçada Cortavento (E60)** — Eleva Ataque Físico em 18% e Velocidade em 15% por 2 ações próprias; se uma esquiva ocorrer, consome o bônus de Velocidade e cura 6% do HP máximo próprio uma vez. **Visual:** Cocórion sustenta a técnica com dança aérea e mudanças bruscas de direção; a animação destaca marcas vermelhas, respeitando seu design homologado.
12. **G118 — Dança do Zênite (E75)** — Exige Ventania ativa; eleva Velocidade em 35% e Defesa Mágica em 15% por 2 ações; após esquiva completa, o bônus de Velocidade é removido e o usuário recupera 15 de energia, uma vez. **Visual:** Cocórion sustenta a técnica com dança aérea e mudanças bruscas de direção; a animação destaca olhos verdes atentos, respeitando seu design homologado.
13. **G123 — Rugido de Sufoco (E65)** — Exige que alvo tenha executado golpe físico em sua última ação; reduz Ataque Físico dele em 28% por 1 ação, sem impedir novos ataques. **Visual:** Cocórion sustenta a técnica com dança aérea e mudanças bruscas de direção; a animação destaca asas largas aerodinâmicas, respeitando seu design homologado.
14. **N017 — Pluma Vazia (E45)** — Poder 90, em vez de 70, se o peso do usuário for igual ou inferior a 100% de seu peso natural de referência no retrato de início da Rinha. **Visual:** Cocórion canaliza a técnica através de correntes de vento criadas pelas asas; a animação destaca crista branca espetada, respeitando seu design homologado.
15. **N018 — Vórtice de Passagem (E45)** — Troca voluntariamente o usuário por aliado apto da reserva. Somente nessa entrada, o substituto ignora os gatilhos das armadilhas existentes no lado aliado. **Visual:** Cocórion sustenta a técnica com dança aérea e mudanças bruscas de direção; a animação destaca marcas vermelhas, respeitando seu design homologado.
16. **N019 — Pena de Eco (E40)** — Se o primeiro ataque deste golpe for totalmente evitado por esquiva do alvo, devolve 15 pontos de energia ao usuário ao terminar a ação (máximo 100). **Visual:** Cocórion canaliza a técnica através de correntes de vento criadas pelas asas; a animação destaca olhos verdes atentos, respeitando seu design homologado.
17. **N020 — Rasante do Azarão (E45)** — Poder 105, em vez de 70, se a Velocidade efetiva do alvo for igual ou superior a 150% da Velocidade efetiva do usuário no momento da execução. **Visual:** Cocórion concentra a técnica nas asas cortantes e garras em rasante; a animação destaca asas largas aerodinâmicas, respeitando seu design homologado.
18. **G071 — Bicada Elétrica (E0)** — Se o alvo estiver Paralisado, poder 50 em vez de 40; não aplica Paralisia adicional. **Visual:** Compatibilidade cruzada: Cocórion concentra a técnica nas asas cortantes e garras em rasante; aproveita eletricidade estática e fenômenos de tempestade. O elemento do golpe continua Elétrico; crista branca espetada identifica a animação.
19. **G072 — Espora de Cobre (E30)** — Após dano, 18% de chance de Tonto; se o alvo já estiver Tonto, concede +8 de energia ao usuário em vez de tentar reaplicação. **Visual:** Compatibilidade cruzada: Cocórion concentra a técnica nas asas cortantes e garras em rasante; aproveita eletricidade estática e fenômenos de tempestade. O elemento do golpe continua Elétrico; marcas vermelhas identifica a animação.
20. **G073 — Investida do Dínamo (E35)** — Contra alvo com menos de 30 de energia, poder 100 em vez de 85; não modifica energia do alvo. **Visual:** Compatibilidade cruzada: Cocórion concentra a técnica nas asas cortantes e garras em rasante; aproveita eletricidade estática e fenômenos de tempestade. O elemento do golpe continua Elétrico; olhos verdes atentos identifica a animação.
21. **G074 — Cascata de Centelhas (E50)** — Após dano reduz Defesa Física em 12% por 2 ações; sob Santuário dos Raios, reduz em 16% por 1 ação e recupera 5 de energia. **Visual:** Compatibilidade cruzada: Cocórion concentra a técnica nas asas cortantes e garras em rasante; aproveita eletricidade estática e fenômenos de tempestade. O elemento do golpe continua Elétrico; asas largas aerodinâmicas identifica a animação.
22. **G002 — Espora Incandescente (E30)** — Após causar dano, 20% de chance de Queimadura; se o alvo já estiver Queimado, reduz sua Defesa Física em 8% pelas próximas 2 ações dele, sem acumular. **Visual:** Compatibilidade cruzada: Cocórion concentra a técnica nas asas cortantes e garras em rasante; gera calor por atrito, cinzas ou brasas do ambiente. O elemento do golpe continua Fogo; crista branca espetada identifica a animação.
23. **G086 — Patada Rasteira (E25)** — Após causar dano reduz Velocidade do alvo em 8% por 2 ações; se o usuário estiver Paralisado, efeito dura só 1 ação mas poder aumenta para 65. **Visual:** Cocórion concentra a técnica nas asas cortantes e garras em rasante; a animação destaca marcas vermelhas, respeitando seu design homologado.
24. **G088 — Giro de Esporas (E35)** — Após dano, reduz Defesa Física do alvo em 10% por 1 ação; se houver segundo acerto, a redução só vale depois de encerrada a ação, sem somar ativações. **Visual:** Cocórion concentra a técnica nas asas cortantes e garras em rasante; a animação destaca olhos verdes atentos, respeitando seu design homologado.
25. **G099 — Passo Firme (E35)** — Eleva Velocidade do usuário em 15% por 2 ações; se estava Paralisado, em vez disso recebe +10% Defesa Física por 1 ação, sem remover Paralisia. **Visual:** Cocórion sustenta a técnica com dança aérea e mudanças bruscas de direção; a animação destaca asas largas aerodinâmicas, respeitando seu design homologado.

**Divergência histórica a revisar:** tabela species contém 850; base natural v0.3 apresentada soma 550. Os dois registros permanecem rastreados.

### #006 — Cocórvolt · Elétrico
**Estado:** ficha_completa_homologada · **Raridade natural:** Mítico · **Base no nível 50:** 550 · **Peso natural:** 5.2 kg
**Identidade de Rinha:** mago de tempestades / paralisia
**Seis atributos:** HP: 90 · Ataque Físico: 25 · Defesa Física: 55 · Ataque Mágico: 155 · Defesa Mágica: 65 · Velocidade: 160
**Passiva:** Senhor da Tempestade [oficial]
```json
{
  "aplicacao_restrita_ataques_tipo": "Elétrico",
  "ativacao_paralisia": "apos_segundo_golpe_eletrico_que_acerta_mesmo_alvo_na_mesma_acao",
  "bonus_aplicavel_ataques_diretos_danificantes": "todos_os_golpes_de_cocorvolt",
  "bonus_dano_ao_alvo_paralisado": 0.3,
  "bonus_dano_aplicacao": "apos_dano_elemental_com_arredondamento_cima",
  "bonus_nao_acumula_consigo_mesmo": true,
  "bonus_valido_se_ja_paralisado_no_momento_do_calculo": true,
  "chance_aplicacao_ao_cumprir_condicoes": 1.0,
  "estado_aplicado": "Paralisia",
  "limite_universal_dois_golpes_por_acao": 2,
  "nao_adiciona_golpes": true,
  "paralisia_garantida_se_condicoes_validas": true,
  "paralisia_na_reserva": "suspensa_conforme_regra_existente",
  "requer_alvo_vivo_apos_segundo_golpe": true,
  "requer_ambos_golpes_acertarem": true,
  "respeita_limite_um_estado_negativo": true,
  "segundo_golpe_fracao_poder_original": 0.5,
  "sem_bonus_retroativo_a_golpes_que_aplicaram_paralisia": true,
  "status": "oficial_nome_e_efeitos_aprovados"
}
```
**Arte oficial (referência, sem redesenho):** /Galetocraft_Cocorvolt_006_Visual_Oficial.png
**Evolução:** Lendário (ver dados completos no JSON).

**Cinco golpes de origem imutáveis**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|
| 1 | crina_poderosa | Crina Poderosa | Neutro | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 2 | concentracao | Concentração | — | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 3 | estalo_voltaico | Estalo Voltaico | Elétrico | 65 | 35 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 4 | palma_celeste | Palma Celeste | Neutro | 100 | 50 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 5 | julgamento_dos_raios | Julgamento dos Raios | Elétrico | 140 | 85 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

**25 golpes aprendíveis atribuídos**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G076 | Arco de Faísca | Elétrico | mágico | 40 | 0 | Não | campo/clima e sinergia |
| 02 | G077 | Pulso Condutor | Elétrico | mágico | 65 | 30 | Não | pressão por estado |
| 03 | G078 | Círculo Voltaico | Elétrico | mágico | 80 | 40 | Não | controle de atributos |
| 04 | G079 | Rede de Relâmpagos | Elétrico | mágico | 105 | 45 | Não | pressão por estado |
| 05 | G080 | Ruptura de Alta Tensão | Elétrico | mágico | 130 | 75 | Não | campo/clima e sinergia |
| 06 | G081 | Cântico dos Condutores | Elétrico | suporte | — | 35 | Não | campo/clima e sinergia |
| 07 | G082 | Bateria Compartilhada | Elétrico | suporte | — | 35 | Não | sustentação |
| 08 | G083 | Campo de Centelhas | Elétrico | suporte | — | 45 | Não | cerco e armadilhas |
| 09 | G084 | Escudo Galvânico | Elétrico | suporte | — | 35 | Não | gestão de energia |
| 10 | G103 | Foco Centelhante | Elétrico | Suporte | — | 45 | Não | campo/clima e sinergia |
| 11 | G110 | Descarga Sináptica | Elétrico | Suporte | — | 60 | Não | campo/clima e sinergia |
| 12 | G115 | Pico Voltaico | Elétrico | Suporte | — | 70 | Não | campo/clima e sinergia |
| 13 | G125 | Ferrugem de Espora | Elétrico | Suporte | — | 45 | Não | controle de atributos |
| 14 | G132 | Apagão de Circuitos | Elétrico | Suporte | — | 70 | Não | controle de atributos |
| 15 | G139 | Rede de Estática | Elétrico | Suporte | — | 65 | Não | campo/clima e sinergia |
| 16 | G062 | Sopro Circular | Ar | mágico | 40 | 0 | Sim | campo/clima e sinergia |
| 17 | G063 | Assobio Rasante | Ar | mágico | 65 | 25 | Sim | controle de atributos |
| 18 | G065 | Cone de Vácuo | Ar | mágico | 105 | 50 | Sim | campo/clima e sinergia |
| 19 | G066 | Aurora do Zênite | Ar | mágico | 130 | 70 | Sim | ritmo, esquiva ou duplo golpe |
| 20 | G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Sim | campo/clima e sinergia |
| 21 | G114 | Tempestade Interior | Ar | Suporte | — | 70 | Sim | campo/clima e sinergia |
| 22 | N019 | Pena de Eco | Ar | mágico | 85 | 40 | Sim | ritmo, esquiva ou duplo golpe |
| 23 | G022 | Coluna de Espuma | Água | mágico | 80 | 40 | Sim | pressão por estado |
| 24 | G023 | Vórtice Azul | Água | mágico | 100 | 50 | Sim | controle de atributos |
| 25 | G071 | Bicada Elétrica | Elétrico | físico | 40 | 0 | Não | pressão por estado |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G076 — Arco de Faísca (E0)** — Sob Santuário dos Raios, ataque básico tem poder 50 em vez de 40; não cria segundo golpe. **Visual:** Cocórvolt canaliza a técnica através de talismãs, cauda e descargas dos olhos; a animação destaca chapéu cônico de palha com talismãs, respeitando seu design homologado.
02. **G077 — Pulso Condutor (E30)** — Após dano, 15% de Tonto; se o alvo já estiver Paralisado, não tenta Tonto e drena 10 de energia adversária. **Visual:** Cocórvolt canaliza a técnica através de talismãs, cauda e descargas dos olhos; a animação destaca olhos azul-elétrico, respeitando seu design homologado.
03. **G078 — Círculo Voltaico (E40)** — Após dano reduz Ataque Mágico do alvo em 10% por 2 ações; se o usuário tiver menos de 40 de energia após pagar o custo, devolve 8 de energia ao final da ação. **Visual:** Cocórvolt canaliza a técnica através de talismãs, cauda e descargas dos olhos; a animação destaca cauda carregada de raios, respeitando seu design homologado.
04. **G079 — Rede de Relâmpagos (E45)** — Se o alvo já sofreu redução de Velocidade, poder 125 em vez de 105; se não, 15% de chance de Paralisia após dano. **Visual:** Cocórvolt canaliza a técnica através de talismãs, cauda e descargas dos olhos; a animação destaca roupa azul-escura e dourada, respeitando seu design homologado.
05. **G080 — Ruptura de Alta Tensão (E75)** — Sob Santuário dos Raios, poder 145 em vez de 130; fora dele, 15% de chance de Tonto após dano, sem gerar acerto adicional. **Visual:** Cocórvolt canaliza a técnica através de talismãs, cauda e descargas dos olhos; a animação destaca chapéu cônico de palha com talismãs, respeitando seu design homologado.
06. **G081 — Cântico dos Condutores (E35)** — Invoca Santuário dos Raios por 4 rodadas; se o usuário estiver Paralisado, recebe 10 de energia após a execução válida, sem remover o estado. **Visual:** Cocórvolt sustenta a técnica com postura ritual do trovão; a animação destaca olhos azul-elétrico, respeitando seu design homologado.
07. **G082 — Bateria Compartilhada (E35)** — Recupera 25 de energia de um aliado ativo escolhido; se o alvo tiver menos de 25 de energia antes da cura, recupera mais 5, sem ultrapassar 100. **Visual:** Cocórvolt sustenta a técnica com postura ritual do trovão; a animação destaca cauda carregada de raios, respeitando seu design homologado.
08. **G083 — Campo de Centelhas (E45)** — Instala armadilha persistente que reduz Defesa Mágica do entrante voluntário em 12% pelas próximas 2 ações; se ele estiver Paralisado, reduz em 15% por 1 ação. **Visual:** Cocórvolt sustenta a técnica com postura ritual do trovão; a animação destaca roupa azul-escura e dourada, respeitando seu design homologado.
09. **G084 — Escudo Galvânico (E35)** — Concede ao aliado escolhido redução de 25% do dano mágico na próxima ação ofensiva recebida; se tiver menos de 40 de energia no impacto, redução sobe para 35%. **Visual:** Cocórvolt sustenta a técnica com postura ritual do trovão; a animação destaca chapéu cônico de palha com talismãs, respeitando seu design homologado.
10. **G103 — Foco Centelhante (E45)** — Concede +25% Ataque Mágico por 1 ação própria; sob Santuário dos Raios, o primeiro golpe mágico que causar dano ainda recupera 10 de energia, sem repetir por segundo acerto. **Visual:** Cocórvolt sustenta a técnica com postura ritual do trovão; a animação destaca olhos azul-elétrico, respeitando seu design homologado.
11. **G110 — Descarga Sináptica (E60)** — Eleva Ataque Mágico em 18% e Velocidade em 15% por 2 ações; sob Santuário dos Raios, a primeira tentativa de reduzir a própria Velocidade não surte efeito. **Visual:** Cocórvolt sustenta a técnica com postura ritual do trovão; a animação destaca cauda carregada de raios, respeitando seu design homologado.
12. **G115 — Pico Voltaico (E70)** — Exige Santuário dos Raios ativo; concede +25% Ataque Mágico e +20% Velocidade por 2 ações; ao acertar inimigo Paralisado drena 8 de energia dele uma vez, sem novo estado. **Visual:** Cocórvolt sustenta a técnica com postura ritual do trovão; a animação destaca roupa azul-escura e dourada, respeitando seu design homologado.
13. **G125 — Ferrugem de Espora (E45)** — Reduz Defesa Física do alvo em 18% por 2 ações; se ele tiver bônus positivo de Defesa Física, reduz somente 10% mas remove 10 de energia atual. **Visual:** Cocórvolt sustenta a técnica com postura ritual do trovão; a animação destaca chapéu cônico de palha com talismãs, respeitando seu design homologado.
14. **G132 — Apagão de Circuitos (E70)** — Exige alvo com estado negativo persistente; reduz Ataque Mágico em 26% por 1 ação e remove 1 bônus temporário positivo de Ataque Mágico, se presente. **Visual:** Cocórvolt sustenta a técnica com postura ritual do trovão; a animação destaca olhos azul-elétrico, respeitando seu design homologado.
15. **G139 — Rede de Estática (E65)** — Exige Santuário dos Raios ativo; reduz Velocidade do alvo em 25% por 1 ação; se o alvo estiver Paralisado, reduz só 10% mas drena 12 de energia, sem acumular Paralisia. **Visual:** Cocórvolt sustenta a técnica com postura ritual do trovão; a animação destaca cauda carregada de raios, respeitando seu design homologado.
16. **G062 — Sopro Circular (E0)** — Quando Ventania estiver ativa, projétil básico tem poder 55 em vez de 40; caso contrário permanece básico sem efeito. **Visual:** Compatibilidade cruzada: Cocórvolt canaliza a técnica através de talismãs, cauda e descargas dos olhos; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; roupa azul-escura e dourada identifica a animação.
17. **G063 — Assobio Rasante (E25)** — Após causar dano reduz Ataque Mágico em 8% por 2 ações; se o alvo estiver sob uma proteção de Suporte, a redução é de 12% por apenas 1 ação. **Visual:** Compatibilidade cruzada: Cocórvolt canaliza a técnica através de talismãs, cauda e descargas dos olhos; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; chapéu cônico de palha com talismãs identifica a animação.
18. **G065 — Cone de Vácuo (E50)** — Após dano reduz Velocidade do alvo em 12% por 2 ações; sob Ventania, em vez disso recupera 10 de energia própria e reduz Velocidade em 8% por 1 ação. **Visual:** Compatibilidade cruzada: Cocórvolt canaliza a técnica através de talismãs, cauda e descargas dos olhos; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; olhos azul-elétrico identifica a animação.
19. **G066 — Aurora do Zênite (E70)** — Se o alvo recebeu um segundo golpe desde sua última ação, poder 150 em vez de 130; caso contrário, 10% de chance de Tonto após dano. **Visual:** Compatibilidade cruzada: Cocórvolt canaliza a técnica através de talismãs, cauda e descargas dos olhos; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; cauda carregada de raios identifica a animação.
20. **G067 — Assobio dos Quatro Ventos (E30)** — Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. **Visual:** Compatibilidade cruzada: Cocórvolt sustenta a técnica com postura ritual do trovão; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; roupa azul-escura e dourada identifica a animação.
21. **G114 — Tempestade Interior (E70)** — Exige Ventania ativa; concede +25% Velocidade e +15% Ataque Físico por 2 ações; o primeiro segundo acerto executado durante o efeito ignora somente 10% de bônus temporários de Defesa Física adversária. **Visual:** Compatibilidade cruzada: Cocórvolt sustenta a técnica com postura ritual do trovão; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; chapéu cônico de palha com talismãs identifica a animação.
22. **N019 — Pena de Eco (E40)** — Se o primeiro ataque deste golpe for totalmente evitado por esquiva do alvo, devolve 15 pontos de energia ao usuário ao terminar a ação (máximo 100). **Visual:** Compatibilidade cruzada: Cocórvolt canaliza a técnica através de talismãs, cauda e descargas dos olhos; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; olhos azul-elétrico identifica a animação.
23. **G022 — Coluna de Espuma (E40)** — Após causar dano tem 20% de chance de Afogamento; se o usuário possuir bônus temporário de Defesa Mágica, a chance cai para 10%, mas poder sobe para 95. **Visual:** Compatibilidade cruzada: Cocórvolt canaliza a técnica através de talismãs, cauda e descargas dos olhos; condensa umidade do ambiente, respingos, névoa ou líquido próximo. O elemento do golpe continua Água; cauda carregada de raios identifica a animação.
24. **G023 — Vórtice Azul (E50)** — Se o inimigo já tiver Ataque Físico reduzido, poder 115 em vez de 100; caso contrário aplica −12% de Ataque Físico por 2 ações após dano. **Visual:** Compatibilidade cruzada: Cocórvolt canaliza a técnica através de talismãs, cauda e descargas dos olhos; condensa umidade do ambiente, respingos, névoa ou líquido próximo. O elemento do golpe continua Água; roupa azul-escura e dourada identifica a animação.
25. **G071 — Bicada Elétrica (E0)** — Se o alvo estiver Paralisado, poder 50 em vez de 40; não aplica Paralisia adicional. **Visual:** Cocórvolt concentra a técnica nas esporas eletrificadas e golpes rápidos; a animação destaca chapéu cônico de palha com talismãs, respeitando seu design homologado.

**Divergência histórica a revisar:** tabela species contém 850; base natural v0.3 apresentada soma 550. Os dois registros permanecem rastreados.

### #007 — Taturico · Terra
**Estado:** ficha_completa_homologada · **Raridade natural:** Comum · **Base no nível 50:** 370 · **Peso natural:** 7.5 kg
**Identidade de Rinha:** defensor terrestre / carapaça
**Seis atributos:** HP: 85 · Ataque Físico: 55 · Defesa Física: 105 · Ataque Mágico: 25 · Defesa Mágica: 60 · Velocidade: 40
**Passiva:** Carapaça Reativa [oficial]
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
**Arte oficial (referência, sem redesenho):** /Galetocraft/RoosterTeca/Fichas_Com_Logo_Oficial_20261111/Taturico_007_Ficha_Oficial_COM_LOGO_GALETOS_20261111.png
**Evolução:** Raro (ver dados completos no JSON).

**Cinco golpes de origem imutáveis**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|
| 1 | garra_afiada | Garra Afiada | Neutro | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 2 | concentracao | Concentração | — | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 3 | impacto_blindado | Impacto Blindado | Terra | 70 | 35 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 4 | guarda_do_tatu | Guarda do Tatu | — | — | 40 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 5 | coro_das_dunas | Coro das Dunas | — | — | 35 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

**25 golpes aprendíveis atribuídos**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G043 | Chute de Cascalho | Terra | físico | 40 | 0 | Não | dano condicional |
| 02 | G044 | Marreta de Barro | Terra | físico | 65 | 30 | Não | campo/clima e sinergia |
| 03 | G045 | Cabeçada de Basalto | Terra | físico | 85 | 35 | Não | controle de atributos |
| 04 | G046 | Pisão Sísmico | Terra | físico | 100 | 50 | Não | pressão por estado |
| 05 | G047 | Lança de Obsidiana | Terra | físico | 120 | 55 | Não | controle de atributos |
| 06 | G053 | Tambor da Areia | Terra | suporte | — | 30 | Não | campo/clima e sinergia |
| 07 | G054 | Muralha Escavada | Terra | suporte | — | 35 | Não | campo/clima e sinergia |
| 08 | G055 | Ninho de Pedregulhos | Terra | suporte | — | 45 | Não | cerco e armadilhas |
| 09 | G056 | Pedra de Revezamento | Terra | suporte | — | 35 | Não | cerco e armadilhas |
| 10 | G102 | Couraça do Subsolo | Terra | Suporte | — | 45 | Não | controle de atributos |
| 11 | G111 | Trono de Cascalho | Terra | Suporte | — | 70 | Não | cerco e armadilhas |
| 12 | G126 | Areia nos Encaixes | Terra | Suporte | — | 55 | Não | campo/clima e sinergia |
| 13 | G134 | Tremor de Cristal | Terra | Suporte | — | 55 | Não | campo/clima e sinergia |
| 14 | N013 | Pisada de Lastro | Terra | físico | 75 | 45 | Não | dano condicional |
| 15 | N014 | Coluna de Guarda | Terra | suporte | — | 40 | Não | controle de atributos |
| 16 | N015 | Cinzel Quebra-Manto | Terra | físico | 80 | 55 | Não | controle de atributos |
| 17 | N016 | Pedra da Impaciência | Terra | mágico | 75 | 45 | Não | dano condicional |
| 18 | G029 | Chicotada de Talos | Planta | físico | 40 | 0 | Sim | pressão por estado |
| 19 | G031 | Arranco de Tronco | Planta | físico | 80 | 35 | Sim | controle de atributos |
| 20 | G033 | Broca de Raiz | Planta | físico | 115 | 55 | Sim | controle de atributos |
| 21 | G042 | Casca Compartilhada | Planta | suporte | — | 30 | Sim | ritmo, esquiva ou duplo golpe |
| 22 | N012 | Casco de Bromélia | Planta | físico | 70 | 45 | Sim | controle de atributos |
| 23 | N011 | Vinha Antirrasante | Planta | suporte | — | 40 | Sim | ritmo, esquiva ou duplo golpe |
| 24 | G016 | Cauda de Ressaca | Água | físico | 60 | 25 | Sim | campo/clima e sinergia |
| 25 | G049 | Lodo Pressurizado | Terra | mágico | 65 | 30 | Não | campo/clima e sinergia |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G043 — Chute de Cascalho (E0)** — Se o alvo tiver peso atual superior a 120% do natural, poder 55 em vez de 40; não altera peso. **Visual:** Taturico concentra a técnica nas carapaça, patas escavadoras e empurrões curtos; a animação destaca carapaça resistente, respeitando seu design homologado.
02. **G044 — Marreta de Barro (E30)** — Após dano reduz Velocidade em 15% por 2 ações; se uma Tempestade de Areia estiver ativa, duração cai para 1 ação e reduz também Defesa Física em 8%. **Visual:** Taturico concentra a técnica nas carapaça, patas escavadoras e empurrões curtos; a animação destaca corpo baixo rente ao solo, respeitando seu design homologado.
03. **G045 — Cabeçada de Basalto (E35)** — Poder 105 em vez de 85 contra alvo com bônus positivo de Defesa Física; não remove bônus nem ignora defesa-base. **Visual:** Taturico concentra a técnica nas carapaça, patas escavadoras e empurrões curtos; a animação destaca patas escavadoras, respeitando seu design homologado.
04. **G046 — Pisão Sísmico (E50)** — Após causar dano, 20% de chance de Tonto; se o alvo já estiver Tonto, em vez de tentar novo estado reduz sua energia em 12. **Visual:** Taturico concentra a técnica nas carapaça, patas escavadoras e empurrões curtos; a animação destaca postura de proteção enrolada, respeitando seu design homologado.
05. **G047 — Lança de Obsidiana (E55)** — Ignora 20% de bônus temporários de Defesa Física; se o usuário sofreu dano de estado desde sua última ação, poder 135 em vez de 120. **Visual:** Taturico concentra a técnica nas carapaça, patas escavadoras e empurrões curtos; a animação destaca carapaça resistente, respeitando seu design homologado.
06. **G053 — Tambor da Areia (E30)** — Invoca Tempestade de Areia por 4 rodadas; se substituir Ventania, o usuário ganha 10% de Defesa Física até sua próxima ação. **Visual:** Taturico sustenta a técnica com carapaça protetora próxima ao solo; a animação destaca corpo baixo rente ao solo, respeitando seu design homologado.
07. **G054 — Muralha Escavada (E35)** — Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. **Visual:** Taturico sustenta a técnica com carapaça protetora próxima ao solo; a animação destaca patas escavadoras, respeitando seu design homologado.
08. **G055 — Ninho de Pedregulhos (E45)** — Instala armadilha persistente que causa 8% do HP máximo do entrante voluntário; se ele estiver acima de 120% do peso natural, causa 11%, sem afetar entradas obrigatórias. **Visual:** Taturico sustenta a técnica com carapaça protetora próxima ao solo; a animação destaca postura de proteção enrolada, respeitando seu design homologado.
09. **G056 — Pedra de Revezamento (E35)** — Troca usuário por aliado da reserva; o entrante recebe +15% de Defesa Física pelas próximas 2 ações e, sob Tempestade de Areia, ignora o dano de uma armadilha apenas na entrada da troca. **Visual:** Taturico sustenta a técnica com carapaça protetora próxima ao solo; a animação destaca carapaça resistente, respeitando seu design homologado.
10. **G102 — Couraça do Subsolo (E45)** — Eleva Defesa Física do usuário em 22% por 2 ações próprias; se estiver acima de 120% do peso natural, reduz também em 10% o dano do primeiro acerto físico recebido. **Visual:** Taturico sustenta a técnica com carapaça protetora próxima ao solo; a animação destaca corpo baixo rente ao solo, respeitando seu design homologado.
11. **G111 — Trono de Cascalho (E70)** — Exige Tempestade de Areia ativa; concede +25% Defesa Física e +15% Defesa Mágica por 2 ações próprias e impede que uma armadilha retire energia do usuário nesse período, sem remover armadilhas. **Visual:** Taturico sustenta a técnica com carapaça protetora próxima ao solo; a animação destaca patas escavadoras, respeitando seu design homologado.
12. **G126 — Areia nos Encaixes (E55)** — Exige Tempestade de Areia ativa; reduz Defesa Física do alvo em 22% por 1 ação; se o alvo pesar mais de 120% do natural, duração sobe para 2 ações. **Visual:** Taturico sustenta a técnica com carapaça protetora próxima ao solo; a animação destaca postura de proteção enrolada, respeitando seu design homologado.
13. **G134 — Tremor de Cristal (E55)** — Exige Tempestade de Areia ativa; reduz Defesa Mágica do alvo em 23% por 1 ação; se alvo tiver bônus de Defesa Mágica, ignora apenas 10% do componente positivo desse bônus no cálculo da próxima ação ofensiva contra ele, sem removê-lo. **Visual:** Taturico sustenta a técnica com carapaça protetora próxima ao solo; a animação destaca carapaça resistente, respeitando seu design homologado.
14. **N013 — Pisada de Lastro (E45)** — Poder 100, em vez de 75, se o peso do usuário for igual ou superior a 120% de seu peso natural de referência no retrato de início da Rinha. **Visual:** Taturico concentra a técnica nas carapaça, patas escavadoras e empurrões curtos; a animação destaca corpo baixo rente ao solo, respeitando seu design homologado.
15. **N014 — Coluna de Guarda (E40)** — O próximo ataque direto recebido pelo próprio usuário ativo terá 20%, em vez de 10%, de chance de ativar a defesa especial, SOMENTE se a Defesa relevante for pelo menos 120% do Ataque correspondente. A redução ao ativar continua 75%. **Visual:** Taturico sustenta a técnica com carapaça protetora próxima ao solo; a animação destaca patas escavadoras, respeitando seu design homologado.
16. **N015 — Cinzel Quebra-Manto (E55)** — Ao calcular o dano, ignora 50% apenas da parcela positiva dos bônus temporários de Defesa Física do alvo; a Defesa Física básica e demais modificadores continuam aplicados. **Visual:** Taturico concentra a técnica nas carapaça, patas escavadoras e empurrões curtos; a animação destaca postura de proteção enrolada, respeitando seu design homologado.
17. **N016 — Pedra da Impaciência (E45)** — Poder 100, em vez de 75, se a última ação efetivamente executada pelo alvo, antes desta, foi um golpe de Suporte (incluindo Concentração). **Visual:** Taturico canaliza a técnica através de poeira e detritos escavados; a animação destaca carapaça resistente, respeitando seu design homologado.
18. **G029 — Chicotada de Talos (E0)** — Se o alvo estiver Envenenado, poder 50 em vez de 40; não causa Envenenamento novo. **Visual:** Compatibilidade cruzada: Taturico concentra a técnica nas carapaça, patas escavadoras e empurrões curtos; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; corpo baixo rente ao solo identifica a animação.
19. **G031 — Arranco de Tronco (E35)** — Se o usuário estiver com peso até 100% do natural, poder 95 em vez de 80; com peso maior, gera +10% de Defesa Física até sua próxima ação após dano. **Visual:** Compatibilidade cruzada: Taturico concentra a técnica nas carapaça, patas escavadoras e empurrões curtos; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; patas escavadoras identifica a animação.
20. **G033 — Broca de Raiz (E55)** — Ignora 25% de bônus temporário positivo de Defesa Física; se o alvo for protegido por barreira de suporte, poder 125 em vez de 115, sem quebrar a barreira automaticamente. **Visual:** Compatibilidade cruzada: Taturico concentra a técnica nas carapaça, patas escavadoras e empurrões curtos; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; postura de proteção enrolada identifica a animação.
21. **G042 — Casca Compartilhada (E30)** — Concede ao aliado selecionado −20% dano mágico na próxima ação ofensiva recebida; se a ação tiver segundo acerto, nele a proteção sobe para 35%. **Visual:** Compatibilidade cruzada: Taturico sustenta a técnica com carapaça protetora próxima ao solo; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; carapaça resistente identifica a animação.
22. **N012 — Casco de Bromélia (E45)** — Poder 95, em vez de 70, se a Defesa Física efetiva do usuário for ao menos 120% do Ataque Físico efetivo do alvo no momento da resolução. **Visual:** Compatibilidade cruzada: Taturico concentra a técnica nas carapaça, patas escavadoras e empurrões curtos; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; corpo baixo rente ao solo identifica a animação.
23. **N011 — Vinha Antirrasante (E40)** — Protege o próprio usuário ativo contra a próxima ação ofensiva recebida: reduz 15% do dano do primeiro acerto e 60% do dano do eventual segundo acerto dessa mesma ação. **Visual:** Compatibilidade cruzada: Taturico sustenta a técnica com carapaça protetora próxima ao solo; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; patas escavadoras identifica a animação.
24. **G016 — Cauda de Ressaca (E25)** — Após causar dano, reduz Velocidade do alvo em 12% por 2 ações; sob Chuva, reduz apenas 8%, mas recupera 10 de energia ao final da ação. **Visual:** Compatibilidade cruzada: Taturico concentra a técnica nas carapaça, patas escavadoras e empurrões curtos; condensa umidade do ambiente, respingos, névoa ou líquido próximo. O elemento do golpe continua Água; postura de proteção enrolada identifica a animação.
25. **G049 — Lodo Pressurizado (E30)** — Após causar dano reduz Defesa Mágica em 10% por 2 ações; se o alvo estiver sob Chuva, em vez disso reduz Defesa Física em 10% por 1 ação. **Visual:** Taturico canaliza a técnica através de poeira e detritos escavados; a animação destaca carapaça resistente, respeitando seu design homologado.

### #008 — Axococó · Água
**Estado:** ficha_completa_homologada · **Raridade natural:** Comum · **Base no nível 50:** 370 · **Peso natural:** 5.8 kg
**Identidade de Rinha:** suporte aquático / regeneração
**Seis atributos:** HP: 95 · Ataque Físico: 35 · Defesa Física: 50 · Ataque Mágico: 90 · Defesa Mágica: 60 · Velocidade: 40
**Passiva:** Memória das Brânquias [oficial]
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
**Arte oficial (referência, sem redesenho):** /Galetocraft/RoosterTeca/Fichas_Com_Logo_Oficial_20261111/Axococo_008_Ficha_Oficial_COM_LOGO_GALETOS_20261111.png
**Evolução:** Raro (ver dados completos no JSON).

**Cinco golpes de origem imutáveis**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|
| 1 | crina_poderosa | Crina Poderosa | Neutro | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 2 | concentracao | Concentração | — | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 3 | estalo_das_branquias | Estalo das Brânquias | Água | 75 | 35 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 4 | elo_regenerativo | Elo Regenerativo | — | — | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 5 | diluvio_branquial | Dilúvio Branquial | Água | 85 | 50 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

**25 golpes aprendíveis atribuídos**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G015 | Bico de Marola | Água | físico | 40 | 0 | Não | pressão por estado |
| 02 | G016 | Cauda de Ressaca | Água | físico | 60 | 25 | Não | campo/clima e sinergia |
| 03 | G017 | Pancada de Maré | Água | físico | 80 | 35 | Não | dano condicional |
| 04 | G018 | Açoite de Corredeira | Água | físico | 95 | 50 | Não | pressão por estado |
| 05 | G019 | Quebra-Cais | Água | físico | 120 | 55 | Não | gestão de energia |
| 06 | G020 | Gota Disparada | Água | mágico | 40 | 0 | Não | sustentação |
| 07 | G021 | Orvalho Cortante | Água | mágico | 60 | 20 | Não | campo/clima e sinergia |
| 08 | G022 | Coluna de Espuma | Água | mágico | 80 | 40 | Não | pressão por estado |
| 09 | G023 | Vórtice Azul | Água | mágico | 100 | 50 | Não | controle de atributos |
| 10 | G024 | Tsunami de Bolhas | Água | mágico | 130 | 70 | Não | campo/clima e sinergia |
| 11 | G025 | Canto das Nuvens | Água | suporte | — | 30 | Não | campo/clima e sinergia |
| 12 | G026 | Névoa Protetora | Água | suporte | — | 30 | Não | pressão por estado |
| 13 | G027 | Maré de Retirada | Água | suporte | — | 40 | Não | cerco e armadilhas |
| 14 | G028 | Banho Reparador | Água | suporte | — | 40 | Não | revezamento e apoio |
| 15 | N005 | Fôlego de Ressaca | Água | físico | 70 | 40 | Não | pressão por estado |
| 16 | N006 | Redemoinho Exaustivo | Água | suporte | — | 45 | Não | cerco e armadilhas |
| 17 | N007 | Banho Sereno | Água | suporte | — | 45 | Não | sustentação |
| 18 | N008 | Pressão do Manancial | Água | mágico | 70 | 45 | Não | gestão de energia |
| 19 | G034 | Semente Atirada | Planta | mágico | 40 | 0 | Sim | campo/clima e sinergia |
| 20 | G035 | Perfume Ácido | Planta | mágico | 60 | 25 | Sim | campo/clima e sinergia |
| 21 | G039 | Hino das Raízes | Planta | suporte | — | 35 | Sim | cerco e armadilhas |
| 22 | G041 | Fotossíntese de Poleiro | Planta | suporte | — | 45 | Sim | campo/clima e sinergia |
| 23 | G042 | Casca Compartilhada | Planta | suporte | — | 30 | Sim | ritmo, esquiva ou duplo golpe |
| 24 | N010 | Seiva de Retaguarda | Planta | mágico | 65 | 45 | Sim | campo/clima e sinergia |
| 25 | G062 | Sopro Circular | Ar | mágico | 40 | 0 | Sim | campo/clima e sinergia |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G015 — Bico de Marola (E0)** — Se o usuário estiver Afogado, poder sobe de 40 para 55 no primeiro acerto; não reduz nem remove Afogamento. **Visual:** Axococó concentra a técnica nas cauda e membros aquáticos; a animação destaca brânquias externas, respeitando seu design homologado.
02. **G016 — Cauda de Ressaca (E25)** — Após causar dano, reduz Velocidade do alvo em 12% por 2 ações; sob Chuva, reduz apenas 8%, mas recupera 10 de energia ao final da ação. **Visual:** Axococó concentra a técnica nas cauda e membros aquáticos; a animação destaca anatomia inspirada em axolote, respeitando seu design homologado.
03. **G017 — Pancada de Maré (E35)** — Se o alvo entrou voluntariamente neste turno, poder sobe de 80 para 100; caso contrário, após causar dano ignora o próximo efeito de redução de Velocidade do usuário até sua próxima ação. **Visual:** Axococó concentra a técnica nas cauda e membros aquáticos; a animação destaca movimento aquático suave, respeitando seu design homologado.
04. **G018 — Açoite de Corredeira (E50)** — Após causar dano, 18% de chance de Afogamento; se o alvo já estava Afogado, em vez de tentar aplicar o estado drena 12 de energia. **Visual:** Axococó concentra a técnica nas cauda e membros aquáticos; a animação destaca capacidade regenerativa, respeitando seu design homologado.
05. **G019 — Quebra-Cais (E55)** — Contra alvo com mais de 70 de energia, poder 135 em vez de 120; após causar dano nessa condição, o usuário não pode receber bônus temporário de Velocidade até sua próxima ação. **Visual:** Axococó concentra a técnica nas cauda e membros aquáticos; a animação destaca brânquias externas, respeitando seu design homologado.
06. **G020 — Gota Disparada (E0)** — Se o usuário recebeu cura desde sua ação anterior, poder 55 em vez de 40; não ativa curas adicionais. **Visual:** Axococó canaliza a técnica através de brânquias e bolhas de água; a animação destaca anatomia inspirada em axolote, respeitando seu design homologado.
07. **G021 — Orvalho Cortante (E20)** — Após causar dano, se Chuva estiver ativa recupera 8 de energia; se não estiver, reduz Defesa Mágica inimiga em 6% até a próxima ação do alvo. **Visual:** Axococó canaliza a técnica através de brânquias e bolhas de água; a animação destaca movimento aquático suave, respeitando seu design homologado.
08. **G022 — Coluna de Espuma (E40)** — Após causar dano tem 20% de chance de Afogamento; se o usuário possuir bônus temporário de Defesa Mágica, a chance cai para 10%, mas poder sobe para 95. **Visual:** Axococó canaliza a técnica através de brânquias e bolhas de água; a animação destaca capacidade regenerativa, respeitando seu design homologado.
09. **G023 — Vórtice Azul (E50)** — Se o inimigo já tiver Ataque Físico reduzido, poder 115 em vez de 100; caso contrário aplica −12% de Ataque Físico por 2 ações após dano. **Visual:** Axococó canaliza a técnica através de brânquias e bolhas de água; a animação destaca brânquias externas, respeitando seu design homologado.
10. **G024 — Tsunami de Bolhas (E70)** — Sob Chuva, poder 145 em vez de 130; sem Chuva, após causar dano, 15% de chance de reduzir Velocidade do alvo em 15% por 1 ação. **Visual:** Axococó canaliza a técnica através de brânquias e bolhas de água; a animação destaca anatomia inspirada em axolote, respeitando seu design homologado.
11. **G025 — Canto das Nuvens (E30)** — Invoca Chuva por 4 rodadas; caso substitua Ensolarado, cura 8% do HP máximo próprio sem afetar a reserva. **Visual:** Axococó sustenta a técnica com brânquias regenerativas; a animação destaca movimento aquático suave, respeitando seu design homologado.
12. **G026 — Névoa Protetora (E30)** — O aliado escolhido recebe −25% de dano mágico na próxima ação ofensiva recebida; se já estiver Afogado, recupera 12 de energia ao ativar a barreira. **Visual:** Axococó sustenta a técnica com brânquias regenerativas; a animação destaca capacidade regenerativa, respeitando seu design homologado.
13. **G027 — Maré de Retirada (E40)** — Troca voluntariamente por aliado da reserva; o entrante recupera 8% de HP máximo e não sofre redução de Velocidade de armadilha somente nessa entrada; outros efeitos de armadilha permanecem. **Visual:** Axococó sustenta a técnica com brânquias regenerativas; a animação destaca brânquias externas, respeitando seu design homologado.
14. **G028 — Banho Reparador (E40)** — Cura 20% do HP máximo de um aliado vivo, inclusive reserva; se o alvo estiver com menos de 30% do HP, acrescenta mais 5%, uma única vez. **Visual:** Axococó sustenta a técnica com brânquias regenerativas; a animação destaca anatomia inspirada em axolote, respeitando seu design homologado.
15. **N005 — Fôlego de Ressaca (E40)** — Se o alvo já tiver Afogamento no início desta ação e ao menos um acerto causar dano, o usuário recupera 15 pontos de energia ao terminar a ação (máximo 100). **Visual:** Axococó concentra a técnica nas cauda e membros aquáticos; a animação destaca movimento aquático suave, respeitando seu design homologado.
16. **N006 — Redemoinho Exaustivo (E45)** — Instala no lado adversário uma armadilha persistente que retira 15 pontos da energia atual de cada Cocorídeo que entra por troca voluntária, nunca abaixo de zero. **Visual:** Axococó sustenta a técnica com brânquias regenerativas; a animação destaca capacidade regenerativa, respeitando seu design homologado.
17. **N007 — Banho Sereno (E45)** — Recupera 10% do HP máximo do usuário ativo e remove o estado negativo persistente que ele tenha, se houver. **Visual:** Axococó sustenta a técnica com brânquias regenerativas; a animação destaca brânquias externas, respeitando seu design homologado.
18. **N008 — Pressão do Manancial (E45)** — Poder 95, em vez de 70, se o alvo tiver 40 ou menos pontos de energia atual no momento do cálculo do primeiro acerto. **Visual:** Axococó canaliza a técnica através de brânquias e bolhas de água; a animação destaca anatomia inspirada em axolote, respeitando seu design homologado.
19. **G034 — Semente Atirada (E0)** — Se Santuário das Raízes estiver ativo, concede 5 de energia ao usuário após causar dano; caso contrário, ataque mágico básico normal. **Visual:** Compatibilidade cruzada: Axococó canaliza a técnica através de brânquias e bolhas de água; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; movimento aquático suave identifica a animação.
20. **G035 — Perfume Ácido (E25)** — Após dano tem 20% de Envenenamento; se o alvo estiver sob Santuário das Raízes e já Envenenado, em vez disso reduz Ataque Mágico em 8% por 1 ação. **Visual:** Compatibilidade cruzada: Axococó canaliza a técnica através de brânquias e bolhas de água; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; capacidade regenerativa identifica a animação.
21. **G039 — Hino das Raízes (E35)** — Invoca Santuário das Raízes por 4 rodadas; se uma armadilha inimiga estiver ativa, reduz em 10% o dano da próxima entrada de um aliado por troca voluntária, sem remover a armadilha. **Visual:** Compatibilidade cruzada: Axococó sustenta a técnica com brânquias regenerativas; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; brânquias externas identifica a animação.
22. **G041 — Fotossíntese de Poleiro (E45)** — Cura 20% do HP máximo de um aliado vivo; no Santuário das Raízes, cura também 5% do HP máximo do usuário ativo quando o alvo for outro aliado. **Visual:** Compatibilidade cruzada: Axococó sustenta a técnica com brânquias regenerativas; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; anatomia inspirada em axolote identifica a animação.
23. **G042 — Casca Compartilhada (E30)** — Concede ao aliado selecionado −20% dano mágico na próxima ação ofensiva recebida; se a ação tiver segundo acerto, nele a proteção sobe para 35%. **Visual:** Compatibilidade cruzada: Axococó sustenta a técnica com brânquias regenerativas; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; movimento aquático suave identifica a animação.
24. **N010 — Seiva de Retaguarda (E45)** — Se Santuário das Raízes estiver ativo e ao menos um acerto causar dano, cura 8% do HP máximo do aliado vivo na reserva com menor proporção de HP atual. **Visual:** Compatibilidade cruzada: Axococó canaliza a técnica através de brânquias e bolhas de água; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; capacidade regenerativa identifica a animação.
25. **G062 — Sopro Circular (E0)** — Quando Ventania estiver ativa, projétil básico tem poder 55 em vez de 40; caso contrário permanece básico sem efeito. **Visual:** Compatibilidade cruzada: Axococó canaliza a técnica através de brânquias e bolhas de água; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; brânquias externas identifica a animação.

### #009 — Vagaló · Elétrico
**Estado:** ficha_completa_homologada · **Raridade natural:** Comum · **Base no nível 50:** 370 · **Peso natural:** 3.1 kg
**Identidade de Rinha:** sinalizador luminoso / troca e velocidade
**Seis atributos:** HP: 60 · Ataque Físico: 25 · Defesa Física: 40 · Ataque Mágico: 15 · Defesa Mágica: 50 · Velocidade: 180
**Passiva:** Código Luminescente [oficial]
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
**Arte oficial (referência, sem redesenho):** /Galetocraft/RoosterTeca/Fichas_Com_Logo_Oficial_20261111/Vagalo_009_Ficha_Oficial_COM_LOGO_GALETOS_20261111.png
**Evolução:** Raro (ver dados completos no JSON).

**Cinco golpes de origem imutáveis**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|
| 1 | garra_afiada | Garra Afiada | Neutro | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 2 | concentracao | Concentração | — | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 3 | rele_luminoso | Relé Luminoso | Elétrico | 50 | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 4 | cortina_cintilante | Cortina Cintilante | Elétrico | — | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 5 | choque_estatico | Choque Estático | Elétrico | 20 | 40 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

**25 golpes aprendíveis atribuídos**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G076 | Arco de Faísca | Elétrico | mágico | 40 | 0 | Não | campo/clima e sinergia |
| 02 | G077 | Pulso Condutor | Elétrico | mágico | 65 | 30 | Não | pressão por estado |
| 03 | G078 | Círculo Voltaico | Elétrico | mágico | 80 | 40 | Não | controle de atributos |
| 04 | G079 | Rede de Relâmpagos | Elétrico | mágico | 105 | 45 | Não | pressão por estado |
| 05 | G081 | Cântico dos Condutores | Elétrico | suporte | — | 35 | Não | campo/clima e sinergia |
| 06 | G082 | Bateria Compartilhada | Elétrico | suporte | — | 35 | Não | sustentação |
| 07 | G083 | Campo de Centelhas | Elétrico | suporte | — | 45 | Não | cerco e armadilhas |
| 08 | G084 | Escudo Galvânico | Elétrico | suporte | — | 35 | Não | gestão de energia |
| 09 | G103 | Foco Centelhante | Elétrico | Suporte | — | 45 | Não | campo/clima e sinergia |
| 10 | G110 | Descarga Sináptica | Elétrico | Suporte | — | 60 | Não | campo/clima e sinergia |
| 11 | G125 | Ferrugem de Espora | Elétrico | Suporte | — | 45 | Não | controle de atributos |
| 12 | G132 | Apagão de Circuitos | Elétrico | Suporte | — | 70 | Não | controle de atributos |
| 13 | G139 | Rede de Estática | Elétrico | Suporte | — | 65 | Não | campo/clima e sinergia |
| 14 | G062 | Sopro Circular | Ar | mágico | 40 | 0 | Sim | campo/clima e sinergia |
| 15 | G063 | Assobio Rasante | Ar | mágico | 65 | 25 | Sim | controle de atributos |
| 16 | G066 | Aurora do Zênite | Ar | mágico | 130 | 70 | Sim | ritmo, esquiva ou duplo golpe |
| 17 | G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Sim | campo/clima e sinergia |
| 18 | G068 | Corrente de Evasão | Ar | suporte | — | 35 | Sim | ritmo, esquiva ou duplo golpe |
| 19 | G069 | Túnel de Retorno | Ar | suporte | — | 35 | Sim | revezamento e apoio |
| 20 | G070 | Redemoinho de Penas | Ar | suporte | — | 45 | Sim | cerco e armadilhas |
| 21 | G105 | Passo de Vendaval | Ar | Suporte | — | 45 | Sim | ritmo, esquiva ou duplo golpe |
| 22 | N017 | Pluma Vazia | Ar | mágico | 70 | 45 | Sim | dano condicional |
| 23 | N018 | Vórtice de Passagem | Ar | suporte | — | 45 | Sim | cerco e armadilhas |
| 24 | G057 | Asa Riscante | Ar | físico | 40 | 0 | Sim | ritmo, esquiva ou duplo golpe |
| 25 | G040 | Armadilha de Pólen | Planta | suporte | — | 45 | Sim | cerco e armadilhas |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G076 — Arco de Faísca (E0)** — Sob Santuário dos Raios, ataque básico tem poder 50 em vez de 40; não cria segundo golpe. **Visual:** Vagaló canaliza a técnica através de flashes e pulsos de luz; a animação destaca bioluminescência, respeitando seu design homologado.
02. **G077 — Pulso Condutor (E30)** — Após dano, 15% de Tonto; se o alvo já estiver Paralisado, não tenta Tonto e drena 10 de energia adversária. **Visual:** Vagaló canaliza a técnica através de flashes e pulsos de luz; a animação destaca corpo pequeno e veloz, respeitando seu design homologado.
03. **G078 — Círculo Voltaico (E40)** — Após dano reduz Ataque Mágico do alvo em 10% por 2 ações; se o usuário tiver menos de 40 de energia após pagar o custo, devolve 8 de energia ao final da ação. **Visual:** Vagaló canaliza a técnica através de flashes e pulsos de luz; a animação destaca pulsos luminosos de sinalização, respeitando seu design homologado.
04. **G079 — Rede de Relâmpagos (E45)** — Se o alvo já sofreu redução de Velocidade, poder 125 em vez de 105; se não, 15% de chance de Paralisia após dano. **Visual:** Vagaló canaliza a técnica através de flashes e pulsos de luz; a animação destaca asas de inseto velozes, respeitando seu design homologado.
05. **G081 — Cântico dos Condutores (E35)** — Invoca Santuário dos Raios por 4 rodadas; se o usuário estiver Paralisado, recebe 10 de energia após a execução válida, sem remover o estado. **Visual:** Vagaló sustenta a técnica com sinais luminosos para a equipe; a animação destaca bioluminescência, respeitando seu design homologado.
06. **G082 — Bateria Compartilhada (E35)** — Recupera 25 de energia de um aliado ativo escolhido; se o alvo tiver menos de 25 de energia antes da cura, recupera mais 5, sem ultrapassar 100. **Visual:** Vagaló sustenta a técnica com sinais luminosos para a equipe; a animação destaca corpo pequeno e veloz, respeitando seu design homologado.
07. **G083 — Campo de Centelhas (E45)** — Instala armadilha persistente que reduz Defesa Mágica do entrante voluntário em 12% pelas próximas 2 ações; se ele estiver Paralisado, reduz em 15% por 1 ação. **Visual:** Vagaló sustenta a técnica com sinais luminosos para a equipe; a animação destaca pulsos luminosos de sinalização, respeitando seu design homologado.
08. **G084 — Escudo Galvânico (E35)** — Concede ao aliado escolhido redução de 25% do dano mágico na próxima ação ofensiva recebida; se tiver menos de 40 de energia no impacto, redução sobe para 35%. **Visual:** Vagaló sustenta a técnica com sinais luminosos para a equipe; a animação destaca asas de inseto velozes, respeitando seu design homologado.
09. **G103 — Foco Centelhante (E45)** — Concede +25% Ataque Mágico por 1 ação própria; sob Santuário dos Raios, o primeiro golpe mágico que causar dano ainda recupera 10 de energia, sem repetir por segundo acerto. **Visual:** Vagaló sustenta a técnica com sinais luminosos para a equipe; a animação destaca bioluminescência, respeitando seu design homologado.
10. **G110 — Descarga Sináptica (E60)** — Eleva Ataque Mágico em 18% e Velocidade em 15% por 2 ações; sob Santuário dos Raios, a primeira tentativa de reduzir a própria Velocidade não surte efeito. **Visual:** Vagaló sustenta a técnica com sinais luminosos para a equipe; a animação destaca corpo pequeno e veloz, respeitando seu design homologado.
11. **G125 — Ferrugem de Espora (E45)** — Reduz Defesa Física do alvo em 18% por 2 ações; se ele tiver bônus positivo de Defesa Física, reduz somente 10% mas remove 10 de energia atual. **Visual:** Vagaló sustenta a técnica com sinais luminosos para a equipe; a animação destaca pulsos luminosos de sinalização, respeitando seu design homologado.
12. **G132 — Apagão de Circuitos (E70)** — Exige alvo com estado negativo persistente; reduz Ataque Mágico em 26% por 1 ação e remove 1 bônus temporário positivo de Ataque Mágico, se presente. **Visual:** Vagaló sustenta a técnica com sinais luminosos para a equipe; a animação destaca asas de inseto velozes, respeitando seu design homologado.
13. **G139 — Rede de Estática (E65)** — Exige Santuário dos Raios ativo; reduz Velocidade do alvo em 25% por 1 ação; se o alvo estiver Paralisado, reduz só 10% mas drena 12 de energia, sem acumular Paralisia. **Visual:** Vagaló sustenta a técnica com sinais luminosos para a equipe; a animação destaca bioluminescência, respeitando seu design homologado.
14. **G062 — Sopro Circular (E0)** — Quando Ventania estiver ativa, projétil básico tem poder 55 em vez de 40; caso contrário permanece básico sem efeito. **Visual:** Compatibilidade cruzada: Vagaló canaliza a técnica através de flashes e pulsos de luz; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; corpo pequeno e veloz identifica a animação.
15. **G063 — Assobio Rasante (E25)** — Após causar dano reduz Ataque Mágico em 8% por 2 ações; se o alvo estiver sob uma proteção de Suporte, a redução é de 12% por apenas 1 ação. **Visual:** Compatibilidade cruzada: Vagaló canaliza a técnica através de flashes e pulsos de luz; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; pulsos luminosos de sinalização identifica a animação.
16. **G066 — Aurora do Zênite (E70)** — Se o alvo recebeu um segundo golpe desde sua última ação, poder 150 em vez de 130; caso contrário, 10% de chance de Tonto após dano. **Visual:** Compatibilidade cruzada: Vagaló canaliza a técnica através de flashes e pulsos de luz; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; asas de inseto velozes identifica a animação.
17. **G067 — Assobio dos Quatro Ventos (E30)** — Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. **Visual:** Compatibilidade cruzada: Vagaló sustenta a técnica com sinais luminosos para a equipe; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; bioluminescência identifica a animação.
18. **G068 — Corrente de Evasão (E35)** — Concede +8 pontos percentuais de esquiva ao usuário por suas próximas 2 ações; se esquivar efetivamente de um golpe, recupera 12 de energia após a ação ofensiva adversária, uma vez. **Visual:** Compatibilidade cruzada: Vagaló sustenta a técnica com sinais luminosos para a equipe; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; corpo pequeno e veloz identifica a animação.
19. **G069 — Túnel de Retorno (E35)** — Troca por aliado da reserva, concedendo-lhe +15% de Velocidade por suas próximas 2 ações; se ele estiver Paralisado, concede somente +10% e não remove a Paralisia. **Visual:** Compatibilidade cruzada: Vagaló sustenta a técnica com sinais luminosos para a equipe; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; pulsos luminosos de sinalização identifica a animação.
20. **G070 — Redemoinho de Penas (E45)** — Instala armadilha persistente que reduz o Ataque Físico do entrante voluntário em 12% por 2 ações; sob Ventania reduz em 15% por 1 ação, sem acumular. **Visual:** Compatibilidade cruzada: Vagaló sustenta a técnica com sinais luminosos para a equipe; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; asas de inseto velozes identifica a animação.
21. **G105 — Passo de Vendaval (E45)** — Concede +22% Velocidade por 2 ações próprias; se o usuário se esquivar completamente de golpe durante esse período, o bônus expira e ele ganha +12% Defesa Física até sua próxima ação. **Visual:** Compatibilidade cruzada: Vagaló sustenta a técnica com sinais luminosos para a equipe; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; bioluminescência identifica a animação.
22. **N017 — Pluma Vazia (E45)** — Poder 90, em vez de 70, se o peso do usuário for igual ou inferior a 100% de seu peso natural de referência no retrato de início da Rinha. **Visual:** Compatibilidade cruzada: Vagaló canaliza a técnica através de flashes e pulsos de luz; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; corpo pequeno e veloz identifica a animação.
23. **N018 — Vórtice de Passagem (E45)** — Troca voluntariamente o usuário por aliado apto da reserva. Somente nessa entrada, o substituto ignora os gatilhos das armadilhas existentes no lado aliado. **Visual:** Compatibilidade cruzada: Vagaló sustenta a técnica com sinais luminosos para a equipe; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; pulsos luminosos de sinalização identifica a animação.
24. **G057 — Asa Riscante (E0)** — Se a Velocidade do usuário superar a do alvo, poder 50 em vez de 40; sem alterar a chance universal de segundo golpe. **Visual:** Compatibilidade cruzada: Vagaló concentra a técnica nas pequenos rasantes carregados; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; asas de inseto velozes identifica a animação.
25. **G040 — Armadilha de Pólen (E45)** — Instala armadilha persistente que reduz o Ataque Mágico do entrante voluntário em 12% por suas 2 próximas ações; se já estiver Envenenado, reduz 18% em vez disso, sem acumular. **Visual:** Compatibilidade cruzada: Vagaló sustenta a técnica com sinais luminosos para a equipe; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; bioluminescência identifica a animação.

### #010 — Morcegalo · Ar
**Estado:** ficha_completa_homologada · **Raridade natural:** Comum · **Base no nível 50:** 370 · **Peso natural:** 5.2 kg
**Identidade de Rinha:** caçador de ecolocalização / controle
**Seis atributos:** HP: 80 · Ataque Físico: 50 · Defesa Física: 45 · Ataque Mágico: 40 · Defesa Mágica: 90 · Velocidade: 65
**Passiva:** Sonar Predatório [oficial]
```json
{
  "beneficiarios": "toda a equipe",
  "bonus_dano_recebido": 0.2,
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
**Arte oficial (referência, sem redesenho):** /Galetocraft/RoosterTeca/Fichas_Com_Logo_Oficial_20261111/Morcegalo_010_Ficha_Oficial_COM_LOGO_GALETOS_20261111.png
**Evolução:** Raro (ver dados completos no JSON).

**Cinco golpes de origem imutáveis**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|
| 1 | garra_afiada | Garra Afiada | Neutro | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 2 | concentracao | Concentração | — | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 3 | rasante_ressonante | Rasante Ressonante | Ar | 60 | 30 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 4 | ruido_branco | Ruído Branco | Ar | — | 40 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 5 | colapso_sonoro | Colapso Sonoro | Ar | 85 | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

**25 golpes aprendíveis atribuídos**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G057 | Asa Riscante | Ar | físico | 40 | 0 | Não | ritmo, esquiva ou duplo golpe |
| 02 | G058 | Pluma de Corte | Ar | físico | 60 | 25 | Não | ritmo, esquiva ou duplo golpe |
| 03 | G059 | Bicada Turbilhão | Ar | físico | 80 | 35 | Não | campo/clima e sinergia |
| 04 | G060 | Rasgo de Altitude | Ar | físico | 100 | 50 | Não | pressão por estado |
| 05 | G062 | Sopro Circular | Ar | mágico | 40 | 0 | Não | campo/clima e sinergia |
| 06 | G063 | Assobio Rasante | Ar | mágico | 65 | 25 | Não | controle de atributos |
| 07 | G064 | Espinho de Pressão | Ar | mágico | 85 | 35 | Não | ritmo, esquiva ou duplo golpe |
| 08 | G065 | Cone de Vácuo | Ar | mágico | 105 | 50 | Não | campo/clima e sinergia |
| 09 | G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Não | campo/clima e sinergia |
| 10 | G068 | Corrente de Evasão | Ar | suporte | — | 35 | Não | ritmo, esquiva ou duplo golpe |
| 11 | G069 | Túnel de Retorno | Ar | suporte | — | 35 | Não | revezamento e apoio |
| 12 | G070 | Redemoinho de Penas | Ar | suporte | — | 45 | Não | cerco e armadilhas |
| 13 | G105 | Passo de Vendaval | Ar | Suporte | — | 45 | Não | ritmo, esquiva ou duplo golpe |
| 14 | G129 | Ruído de Barragem | Ar | Suporte | — | 45 | Não | campo/clima e sinergia |
| 15 | G135 | Vácuo de Eco | Ar | Suporte | — | 65 | Não | campo/clima e sinergia |
| 16 | N017 | Pluma Vazia | Ar | mágico | 70 | 45 | Não | dano condicional |
| 17 | N018 | Vórtice de Passagem | Ar | suporte | — | 45 | Não | cerco e armadilhas |
| 18 | N019 | Pena de Eco | Ar | mágico | 85 | 40 | Não | ritmo, esquiva ou duplo golpe |
| 19 | N020 | Rasante do Azarão | Ar | físico | 70 | 45 | Não | dano condicional |
| 20 | G092 | Eco do Cocoricó | Neutro | mágico | 40 | 0 | Não | pressão por estado |
| 21 | G093 | Grito Harmônico | Neutro | mágico | 90 | 40 | Não | campo/clima e sinergia |
| 22 | G098 | Cocoricó Desafiador | Sem elemento | suporte | — | 35 | Não | pressão por estado |
| 23 | G077 | Pulso Condutor | Elétrico | mágico | 65 | 30 | Sim | pressão por estado |
| 24 | G078 | Círculo Voltaico | Elétrico | mágico | 80 | 40 | Sim | controle de atributos |
| 25 | G040 | Armadilha de Pólen | Planta | suporte | — | 45 | Sim | cerco e armadilhas |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G057 — Asa Riscante (E0)** — Se a Velocidade do usuário superar a do alvo, poder 50 em vez de 40; sem alterar a chance universal de segundo golpe. **Visual:** Morcegalo concentra a técnica nas asas membranosas em rasante; a animação destaca membranas roxas de asas, respeitando seu design homologado.
02. **G058 — Pluma de Corte (E25)** — Após dano reduz Defesa Física do alvo em 10% por 1 ação; se a esquiva do usuário foi ativada desde sua última ação, aumenta a redução para 15%. **Visual:** Morcegalo concentra a técnica nas asas membranosas em rasante; a animação destaca ecolocalização, respeitando seu design homologado.
03. **G059 — Bicada Turbilhão (E35)** — Se o alvo usou Suporte na última ação dele, poder 100 em vez de 80; caso contrário recupera 5 de energia após causar dano em Ventania. **Visual:** Morcegalo concentra a técnica nas asas membranosas em rasante; a animação destaca rasantes noturnos, respeitando seu design homologado.
04. **G060 — Rasgo de Altitude (E50)** — Após causar dano, 15% de Tonto; se a Velocidade do usuário for menor que a do alvo, poder 115 em vez de 100. **Visual:** Morcegalo concentra a técnica nas asas membranosas em rasante; a animação destaca ouvidos e percepção por eco, respeitando seu design homologado.
05. **G062 — Sopro Circular (E0)** — Quando Ventania estiver ativa, projétil básico tem poder 55 em vez de 40; caso contrário permanece básico sem efeito. **Visual:** Morcegalo canaliza a técnica através de ondas de som e ar comprimido; a animação destaca membranas roxas de asas, respeitando seu design homologado.
06. **G063 — Assobio Rasante (E25)** — Após causar dano reduz Ataque Mágico em 8% por 2 ações; se o alvo estiver sob uma proteção de Suporte, a redução é de 12% por apenas 1 ação. **Visual:** Morcegalo canaliza a técnica através de ondas de som e ar comprimido; a animação destaca ecolocalização, respeitando seu design homologado.
07. **G064 — Espinho de Pressão (E35)** — Se uma esquiva completa do usuário ocorreu no turno anterior, poder 105 em vez de 85; não concede esquiva nova. **Visual:** Morcegalo canaliza a técnica através de ondas de som e ar comprimido; a animação destaca rasantes noturnos, respeitando seu design homologado.
08. **G065 — Cone de Vácuo (E50)** — Após dano reduz Velocidade do alvo em 12% por 2 ações; sob Ventania, em vez disso recupera 10 de energia própria e reduz Velocidade em 8% por 1 ação. **Visual:** Morcegalo canaliza a técnica através de ondas de som e ar comprimido; a animação destaca ouvidos e percepção por eco, respeitando seu design homologado.
09. **G067 — Assobio dos Quatro Ventos (E30)** — Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. **Visual:** Morcegalo sustenta a técnica com ecos que confundem e revelam alvos; a animação destaca membranas roxas de asas, respeitando seu design homologado.
10. **G068 — Corrente de Evasão (E35)** — Concede +8 pontos percentuais de esquiva ao usuário por suas próximas 2 ações; se esquivar efetivamente de um golpe, recupera 12 de energia após a ação ofensiva adversária, uma vez. **Visual:** Morcegalo sustenta a técnica com ecos que confundem e revelam alvos; a animação destaca ecolocalização, respeitando seu design homologado.
11. **G069 — Túnel de Retorno (E35)** — Troca por aliado da reserva, concedendo-lhe +15% de Velocidade por suas próximas 2 ações; se ele estiver Paralisado, concede somente +10% e não remove a Paralisia. **Visual:** Morcegalo sustenta a técnica com ecos que confundem e revelam alvos; a animação destaca rasantes noturnos, respeitando seu design homologado.
12. **G070 — Redemoinho de Penas (E45)** — Instala armadilha persistente que reduz o Ataque Físico do entrante voluntário em 12% por 2 ações; sob Ventania reduz em 15% por 1 ação, sem acumular. **Visual:** Morcegalo sustenta a técnica com ecos que confundem e revelam alvos; a animação destaca ouvidos e percepção por eco, respeitando seu design homologado.
13. **G105 — Passo de Vendaval (E45)** — Concede +22% Velocidade por 2 ações próprias; se o usuário se esquivar completamente de golpe durante esse período, o bônus expira e ele ganha +12% Defesa Física até sua próxima ação. **Visual:** Morcegalo sustenta a técnica com ecos que confundem e revelam alvos; a animação destaca membranas roxas de asas, respeitando seu design homologado.
14. **G129 — Ruído de Barragem (E45)** — Reduz Ataque Mágico do alvo em 18% por 2 ações; se Ventania estiver ativa, a primeira tentativa de recuperar energia por golpe do alvo é reduzida em 8 pontos. **Visual:** Morcegalo sustenta a técnica com ecos que confundem e revelam alvos; a animação destaca ecolocalização, respeitando seu design homologado.
15. **G135 — Vácuo de Eco (E65)** — Exige Ventania ativa; reduz Defesa Mágica do alvo em 25% por 1 ação; se ele já teve esquiva completa neste turno, a redução dura 2 ações. **Visual:** Morcegalo sustenta a técnica com ecos que confundem e revelam alvos; a animação destaca rasantes noturnos, respeitando seu design homologado.
16. **N017 — Pluma Vazia (E45)** — Poder 90, em vez de 70, se o peso do usuário for igual ou inferior a 100% de seu peso natural de referência no retrato de início da Rinha. **Visual:** Morcegalo canaliza a técnica através de ondas de som e ar comprimido; a animação destaca ouvidos e percepção por eco, respeitando seu design homologado.
17. **N018 — Vórtice de Passagem (E45)** — Troca voluntariamente o usuário por aliado apto da reserva. Somente nessa entrada, o substituto ignora os gatilhos das armadilhas existentes no lado aliado. **Visual:** Morcegalo sustenta a técnica com ecos que confundem e revelam alvos; a animação destaca membranas roxas de asas, respeitando seu design homologado.
18. **N019 — Pena de Eco (E40)** — Se o primeiro ataque deste golpe for totalmente evitado por esquiva do alvo, devolve 15 pontos de energia ao usuário ao terminar a ação (máximo 100). **Visual:** Morcegalo canaliza a técnica através de ondas de som e ar comprimido; a animação destaca ecolocalização, respeitando seu design homologado.
19. **N020 — Rasante do Azarão (E45)** — Poder 105, em vez de 70, se a Velocidade efetiva do alvo for igual ou superior a 150% da Velocidade efetiva do usuário no momento da execução. **Visual:** Morcegalo concentra a técnica nas asas membranosas em rasante; a animação destaca rasantes noturnos, respeitando seu design homologado.
20. **G092 — Eco do Cocoricó (E0)** — Se o alvo estiver Tonto, poder 50 em vez de 40; caso contrário é onda mágica básica sem status. **Visual:** Morcegalo canaliza a técnica através de ondas de som e ar comprimido; a animação destaca ouvidos e percepção por eco, respeitando seu design homologado.
21. **G093 — Grito Harmônico (E40)** — Após causar dano reduz Ataque Mágico em 12% por 1 ação; se Ventania estiver ativa, a redução passa para 8% por 2 ações. **Visual:** Morcegalo canaliza a técnica através de ondas de som e ar comprimido; a animação destaca membranas roxas de asas, respeitando seu design homologado.
22. **G098 — Cocoricó Desafiador (E35)** — Reduz Ataque Físico e Ataque Mágico do inimigo em 8% pelas próximas 2 ações; se ele estiver Tonto, reduz só 5% mas devolve 10 de energia ao usuário. **Visual:** Morcegalo sustenta a técnica com ecos que confundem e revelam alvos; a animação destaca ecolocalização, respeitando seu design homologado.
23. **G077 — Pulso Condutor (E30)** — Após dano, 15% de Tonto; se o alvo já estiver Paralisado, não tenta Tonto e drena 10 de energia adversária. **Visual:** Compatibilidade cruzada: Morcegalo canaliza a técnica através de ondas de som e ar comprimido; aproveita eletricidade estática e fenômenos de tempestade. O elemento do golpe continua Elétrico; rasantes noturnos identifica a animação.
24. **G078 — Círculo Voltaico (E40)** — Após dano reduz Ataque Mágico do alvo em 10% por 2 ações; se o usuário tiver menos de 40 de energia após pagar o custo, devolve 8 de energia ao final da ação. **Visual:** Compatibilidade cruzada: Morcegalo canaliza a técnica através de ondas de som e ar comprimido; aproveita eletricidade estática e fenômenos de tempestade. O elemento do golpe continua Elétrico; ouvidos e percepção por eco identifica a animação.
25. **G040 — Armadilha de Pólen (E45)** — Instala armadilha persistente que reduz o Ataque Mágico do entrante voluntário em 12% por suas 2 próximas ações; se já estiver Envenenado, reduz 18% em vez disso, sem acumular. **Visual:** Compatibilidade cruzada: Morcegalo sustenta a técnica com ecos que confundem e revelam alvos; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; membranas roxas de asas identifica a animação.

### #011 — Espinhocó · Planta
**Estado:** ficha_completa_homologada · **Raridade natural:** Comum · **Base no nível 50:** 370 · **Peso natural:** 6.2 kg
**Identidade de Rinha:** tanque territorial / espinhos e armadilhas
**Seis atributos:** HP: 75 · Ataque Físico: 95 · Defesa Física: 85 · Ataque Mágico: 20 · Defesa Mágica: 55 · Velocidade: 40
**Passiva:** Espinheiro Territorial [oficial]
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
**Arte oficial (referência, sem redesenho):** /Galetocraft/RoosterTeca/Fichas_Com_Logo_Oficial_20261111/Espinhoco_011_Ficha_Oficial_COM_LOGO_GALETOS_20261111.png
**Evolução:** Raro (ver dados completos no JSON).

**Cinco golpes de origem imutáveis**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|
| 1 | garra_afiada | Garra Afiada | Neutro | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 2 | concentracao | Concentração | — | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 3 | espinho_venenoso | Espinho Venenoso | Planta | 20 | 40 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 4 | armadilha_de_cipos | Armadilha de Cipós | Planta | — | 45 | instala armadilha persistente no campo adversario; troca voluntaria aplica -20% velocidade durante proximas duas acoes do entrante; nao acumula no mesmo alvo |
| 5 | rajada_de_espinhos | Rajada de Espinhos | Planta | 95 | 45 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |

**25 golpes aprendíveis atribuídos**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G029 | Chicotada de Talos | Planta | físico | 40 | 0 | Não | pressão por estado |
| 02 | G030 | Ferrão de Trepadeira | Planta | físico | 55 | 25 | Não | pressão por estado |
| 03 | G031 | Arranco de Tronco | Planta | físico | 80 | 35 | Não | controle de atributos |
| 04 | G032 | Tesoura de Folhas | Planta | físico | 90 | 40 | Não | pressão por estado |
| 05 | G033 | Broca de Raiz | Planta | físico | 115 | 55 | Não | controle de atributos |
| 06 | G039 | Hino das Raízes | Planta | suporte | — | 35 | Não | cerco e armadilhas |
| 07 | G040 | Armadilha de Pólen | Planta | suporte | — | 45 | Não | cerco e armadilhas |
| 08 | G042 | Casca Compartilhada | Planta | suporte | — | 30 | Não | ritmo, esquiva ou duplo golpe |
| 09 | G121 | Resina nas Articulações | Planta | Suporte | — | 45 | Não | ritmo, esquiva ou duplo golpe |
| 10 | G127 | Cipó Descascador | Planta | Suporte | — | 65 | Não | controle de atributos |
| 11 | G138 | Raízes na Espora | Planta | Suporte | — | 55 | Não | cerco e armadilhas |
| 12 | N009 | Espinho de Revezamento | Planta | físico | 75 | 45 | Não | revezamento e apoio |
| 13 | N011 | Vinha Antirrasante | Planta | suporte | — | 40 | Não | ritmo, esquiva ou duplo golpe |
| 14 | N012 | Casco de Bromélia | Planta | físico | 70 | 45 | Não | controle de atributos |
| 15 | G043 | Chute de Cascalho | Terra | físico | 40 | 0 | Sim | dano condicional |
| 16 | G044 | Marreta de Barro | Terra | físico | 65 | 30 | Sim | campo/clima e sinergia |
| 17 | G045 | Cabeçada de Basalto | Terra | físico | 85 | 35 | Sim | controle de atributos |
| 18 | G046 | Pisão Sísmico | Terra | físico | 100 | 50 | Sim | pressão por estado |
| 19 | G054 | Muralha Escavada | Terra | suporte | — | 35 | Sim | campo/clima e sinergia |
| 20 | G055 | Ninho de Pedregulhos | Terra | suporte | — | 45 | Sim | cerco e armadilhas |
| 21 | G102 | Couraça do Subsolo | Terra | Suporte | — | 45 | Sim | controle de atributos |
| 22 | N013 | Pisada de Lastro | Terra | físico | 75 | 45 | Sim | dano condicional |
| 23 | N014 | Coluna de Guarda | Terra | suporte | — | 40 | Sim | controle de atributos |
| 24 | N015 | Cinzel Quebra-Manto | Terra | físico | 80 | 55 | Sim | controle de atributos |
| 25 | G100 | Terreiro Purificado | Sem elemento | suporte | — | 45 | Não | cerco e armadilhas |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G029 — Chicotada de Talos (E0)** — Se o alvo estiver Envenenado, poder 50 em vez de 40; não causa Envenenamento novo. **Visual:** Espinhocó concentra a técnica nas espinhos rígidos, patas curtas e investidas; a animação destaca espinhos vegetais projetados para fora, respeitando seu design homologado.
02. **G030 — Ferrão de Trepadeira (E25)** — Após dano, 25% de chance de Envenenamento; caso o alvo já esteja Envenenado, reduz 10 de sua energia em vez de reaplicar estado. **Visual:** Espinhocó concentra a técnica nas espinhos rígidos, patas curtas e investidas; a animação destaca anatomia de porco-espinho voxel, respeitando seu design homologado.
03. **G031 — Arranco de Tronco (E35)** — Se o usuário estiver com peso até 100% do natural, poder 95 em vez de 80; com peso maior, gera +10% de Defesa Física até sua próxima ação após dano. **Visual:** Espinhocó concentra a técnica nas espinhos rígidos, patas curtas e investidas; a animação destaca corpo compacto de resistência, respeitando seu design homologado.
04. **G032 — Tesoura de Folhas (E40)** — Ao causar dano, 15% de Envenenamento; quando o alvo já estiver Envenenado, reduz apenas sua Defesa Física em 12% por 1 ação, sem acumular. **Visual:** Espinhocó concentra a técnica nas espinhos rígidos, patas curtas e investidas; a animação destaca território de cipós, respeitando seu design homologado.
05. **G033 — Broca de Raiz (E55)** — Ignora 25% de bônus temporário positivo de Defesa Física; se o alvo for protegido por barreira de suporte, poder 125 em vez de 115, sem quebrar a barreira automaticamente. **Visual:** Espinhocó concentra a técnica nas espinhos rígidos, patas curtas e investidas; a animação destaca espinhos vegetais projetados para fora, respeitando seu design homologado.
06. **G039 — Hino das Raízes (E35)** — Invoca Santuário das Raízes por 4 rodadas; se uma armadilha inimiga estiver ativa, reduz em 10% o dano da próxima entrada de um aliado por troca voluntária, sem remover a armadilha. **Visual:** Espinhocó sustenta a técnica com cerca vegetal de espinhos e raízes; a animação destaca anatomia de porco-espinho voxel, respeitando seu design homologado.
07. **G040 — Armadilha de Pólen (E45)** — Instala armadilha persistente que reduz o Ataque Mágico do entrante voluntário em 12% por suas 2 próximas ações; se já estiver Envenenado, reduz 18% em vez disso, sem acumular. **Visual:** Espinhocó sustenta a técnica com cerca vegetal de espinhos e raízes; a animação destaca corpo compacto de resistência, respeitando seu design homologado.
08. **G042 — Casca Compartilhada (E30)** — Concede ao aliado selecionado −20% dano mágico na próxima ação ofensiva recebida; se a ação tiver segundo acerto, nele a proteção sobe para 35%. **Visual:** Espinhocó sustenta a técnica com cerca vegetal de espinhos e raízes; a animação destaca território de cipós, respeitando seu design homologado.
09. **G121 — Resina nas Articulações (E45)** — Reduz Ataque Físico do alvo em 18% por 2 ações dele; se o alvo tentar um segundo acerto por Velocidade durante a redução, a penalidade é 25% apenas naquele segundo acerto. **Visual:** Espinhocó sustenta a técnica com cerca vegetal de espinhos e raízes; a animação destaca espinhos vegetais projetados para fora, respeitando seu design homologado.
10. **G127 — Cipó Descascador (E65)** — Exige alvo com bônus positivo de Defesa Física; remove o menor bônus temporário positivo de Defesa Física do alvo e reduz sua Defesa Física em 8% por 1 ação, sem remover outros bônus. **Visual:** Espinhocó sustenta a técnica com cerca vegetal de espinhos e raízes; a animação destaca anatomia de porco-espinho voxel, respeitando seu design homologado.
11. **G138 — Raízes na Espora (E55)** — Exige Santuário das Raízes ativo; reduz Velocidade do alvo em 22% por 1 ação; se houver armadilha no lado dele, duração sobe para 2 ações, sem adicionar cargas de armadilha. **Visual:** Espinhocó sustenta a técnica com cerca vegetal de espinhos e raízes; a animação destaca corpo compacto de resistência, respeitando seu design homologado.
12. **N009 — Espinho de Revezamento (E45)** — Poder 105, em vez de 75, contra alvo que entrou por troca voluntária neste mesmo turno, antes da execução do golpe. **Visual:** Espinhocó concentra a técnica nas espinhos rígidos, patas curtas e investidas; a animação destaca território de cipós, respeitando seu design homologado.
13. **N011 — Vinha Antirrasante (E40)** — Protege o próprio usuário ativo contra a próxima ação ofensiva recebida: reduz 15% do dano do primeiro acerto e 60% do dano do eventual segundo acerto dessa mesma ação. **Visual:** Espinhocó sustenta a técnica com cerca vegetal de espinhos e raízes; a animação destaca espinhos vegetais projetados para fora, respeitando seu design homologado.
14. **N012 — Casco de Bromélia (E45)** — Poder 95, em vez de 70, se a Defesa Física efetiva do usuário for ao menos 120% do Ataque Físico efetivo do alvo no momento da resolução. **Visual:** Espinhocó concentra a técnica nas espinhos rígidos, patas curtas e investidas; a animação destaca anatomia de porco-espinho voxel, respeitando seu design homologado.
15. **G043 — Chute de Cascalho (E0)** — Se o alvo tiver peso atual superior a 120% do natural, poder 55 em vez de 40; não altera peso. **Visual:** Compatibilidade cruzada: Espinhocó concentra a técnica nas espinhos rígidos, patas curtas e investidas; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; corpo compacto de resistência identifica a animação.
16. **G044 — Marreta de Barro (E30)** — Após dano reduz Velocidade em 15% por 2 ações; se uma Tempestade de Areia estiver ativa, duração cai para 1 ação e reduz também Defesa Física em 8%. **Visual:** Compatibilidade cruzada: Espinhocó concentra a técnica nas espinhos rígidos, patas curtas e investidas; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; território de cipós identifica a animação.
17. **G045 — Cabeçada de Basalto (E35)** — Poder 105 em vez de 85 contra alvo com bônus positivo de Defesa Física; não remove bônus nem ignora defesa-base. **Visual:** Compatibilidade cruzada: Espinhocó concentra a técnica nas espinhos rígidos, patas curtas e investidas; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; espinhos vegetais projetados para fora identifica a animação.
18. **G046 — Pisão Sísmico (E50)** — Após causar dano, 20% de chance de Tonto; se o alvo já estiver Tonto, em vez de tentar novo estado reduz sua energia em 12. **Visual:** Compatibilidade cruzada: Espinhocó concentra a técnica nas espinhos rígidos, patas curtas e investidas; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; anatomia de porco-espinho voxel identifica a animação.
19. **G054 — Muralha Escavada (E35)** — Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. **Visual:** Compatibilidade cruzada: Espinhocó sustenta a técnica com cerca vegetal de espinhos e raízes; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; corpo compacto de resistência identifica a animação.
20. **G055 — Ninho de Pedregulhos (E45)** — Instala armadilha persistente que causa 8% do HP máximo do entrante voluntário; se ele estiver acima de 120% do peso natural, causa 11%, sem afetar entradas obrigatórias. **Visual:** Compatibilidade cruzada: Espinhocó sustenta a técnica com cerca vegetal de espinhos e raízes; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; território de cipós identifica a animação.
21. **G102 — Couraça do Subsolo (E45)** — Eleva Defesa Física do usuário em 22% por 2 ações próprias; se estiver acima de 120% do peso natural, reduz também em 10% o dano do primeiro acerto físico recebido. **Visual:** Compatibilidade cruzada: Espinhocó sustenta a técnica com cerca vegetal de espinhos e raízes; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; espinhos vegetais projetados para fora identifica a animação.
22. **N013 — Pisada de Lastro (E45)** — Poder 100, em vez de 75, se o peso do usuário for igual ou superior a 120% de seu peso natural de referência no retrato de início da Rinha. **Visual:** Compatibilidade cruzada: Espinhocó concentra a técnica nas espinhos rígidos, patas curtas e investidas; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; anatomia de porco-espinho voxel identifica a animação.
23. **N014 — Coluna de Guarda (E40)** — O próximo ataque direto recebido pelo próprio usuário ativo terá 20%, em vez de 10%, de chance de ativar a defesa especial, SOMENTE se a Defesa relevante for pelo menos 120% do Ataque correspondente. A redução ao ativar continua 75%. **Visual:** Compatibilidade cruzada: Espinhocó sustenta a técnica com cerca vegetal de espinhos e raízes; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; corpo compacto de resistência identifica a animação.
24. **N015 — Cinzel Quebra-Manto (E55)** — Ao calcular o dano, ignora 50% apenas da parcela positiva dos bônus temporários de Defesa Física do alvo; a Defesa Física básica e demais modificadores continuam aplicados. **Visual:** Compatibilidade cruzada: Espinhocó concentra a técnica nas espinhos rígidos, patas curtas e investidas; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; território de cipós identifica a animação.
25. **G100 — Terreiro Purificado (E45)** — Remove integralmente todas as armadilhas e cargas do lado do usuário; se pelo menos uma armadilha foi removida, recupera 10 de energia após a execução. **Visual:** Espinhocó sustenta a técnica com cerca vegetal de espinhos e raízes; a animação destaca espinhos vegetais projetados para fora, respeitando seu design homologado.

### #012 — Salambrasa · Fogo
**Estado:** ficha_completa_homologada · **Raridade natural:** Comum · **Base no nível 50:** 370 · **Peso natural:** 6.4 kg
**Identidade de Rinha:** lutador de corpo robusto / brasa e terra
**Seis atributos:** HP: 95 · Ataque Físico: 90 · Defesa Física: 80 · Ataque Mágico: 25 · Defesa Mágica: 50 · Velocidade: 30
**Passiva:** Pele de Brasa [oficial]
```json
{
  "chance_por_acerto_valido_pct": 20,
  "danos_indiretos_de_status": false,
  "efeito": "A cada golpe direto recebido que cause dano válido, físico ou mágico, Salambrasa tem 20% de chance independente de aplicar Queimadura ao atacante. Não há limite de tentativas por rodada. Se receber dois golpes diretos válidos, pode testar a passiva duas vezes. Não é ativada por erro, anulação completa ou dano indireto de estado. Não aplica Queimadura se o atacante já possuir estado negativo persistente, respeitando o limite de um. Não causa dano extra.",
  "estado_aplicado": "Queimadura",
  "golpes_fisicos": true,
  "golpes_magicos": true,
  "limite_tentativas_por_rodada": null,
  "nome": "Pele de Brasa",
  "somente_proposta": false
}
```
**Arte oficial (referência, sem redesenho):** /Galetocraft/RoosterTeca/Fichas_Com_Logo_Oficial_20261111/Salambrasa_012_Ficha_Oficial_COM_LOGO_GALETOS_20261111.png
**Evolução:** Raro (ver dados completos no JSON).

**Cinco golpes de origem imutáveis**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|
| 1 | garra_afiada | Garra Afiada | Neutro | 40 | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 2 | concentracao | Concentração | — | — | 0 | Sem descrição textual adicional na ficha oficial; consultar o JSON original protegido. |
| 3 | G142 | Dentada de Carvão | Fogo | 65 | 35 | Golpe físico de Fogo; 20% de chance de aplicar Queimadura ao alvo, respeitando o máximo de um estado negativo persistente. |
| 4 | G143 | Armadura de Brasa | Fogo | — | 65 | Suporte de Fogo: +50% de Defesa Física e +50% de Defesa Mágica do usuário até sair de campo ou ser derrotado. Não acumula bônus do mesmo atributo (permanece o maior). Removível por G141 Dissipação Absoluta. Consome uma ação. |
| 5 | G144 | Arrasto Magmático | Fogo | 90 | 45 | Golpe físico de Fogo; se o alvo já estiver Queimado no momento do cálculo, causa +20% de dano deste golpe. Não provoca Queimadura por si só. |

**25 golpes aprendíveis atribuídos**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G001 | Bico de Brasas | Fogo | físico | 40 | 0 | Não | pressão por estado |
| 02 | G002 | Espora Incandescente | Fogo | físico | 65 | 30 | Não | pressão por estado |
| 03 | G003 | Galope de Carvão | Fogo | físico | 85 | 35 | Não | cerco e armadilhas |
| 04 | G004 | Garra Vulcânica | Fogo | físico | 95 | 50 | Não | pressão por estado |
| 05 | G005 | Quebra-Forja | Fogo | físico | 115 | 65 | Não | sustentação |
| 06 | G011 | Chamado do Meio-Dia | Fogo | suporte | — | 30 | Não | campo/clima e sinergia |
| 07 | G012 | Retorno de Cinzas | Fogo | suporte | — | 35 | Não | ritmo, esquiva ou duplo golpe |
| 08 | G013 | Cinzas da Discórdia | Fogo | suporte | — | 35 | Não | pressão por estado |
| 09 | G014 | Reacender | Fogo | suporte | — | 40 | Não | campo/clima e sinergia |
| 10 | G106 | Forja das Esporas | Fogo | Suporte | — | 60 | Não | pressão por estado |
| 11 | G131 | Cinza nos Olhos | Fogo | Suporte | — | 65 | Não | campo/clima e sinergia |
| 12 | N001 | Brasa de Rebate | Fogo | físico | 75 | 45 | Não | cerco e armadilhas |
| 13 | N003 | Fornalha Resguardada | Fogo | suporte | — | 40 | Não | pressão por estado |
| 14 | G043 | Chute de Cascalho | Terra | físico | 40 | 0 | Sim | dano condicional |
| 15 | G044 | Marreta de Barro | Terra | físico | 65 | 30 | Sim | campo/clima e sinergia |
| 16 | G045 | Cabeçada de Basalto | Terra | físico | 85 | 35 | Sim | controle de atributos |
| 17 | G046 | Pisão Sísmico | Terra | físico | 100 | 50 | Sim | pressão por estado |
| 18 | G047 | Lança de Obsidiana | Terra | físico | 120 | 55 | Sim | controle de atributos |
| 19 | G049 | Lodo Pressurizado | Terra | mágico | 65 | 30 | Sim | campo/clima e sinergia |
| 20 | G053 | Tambor da Areia | Terra | suporte | — | 30 | Sim | campo/clima e sinergia |
| 21 | G054 | Muralha Escavada | Terra | suporte | — | 35 | Sim | campo/clima e sinergia |
| 22 | G102 | Couraça do Subsolo | Terra | Suporte | — | 45 | Sim | controle de atributos |
| 23 | N013 | Pisada de Lastro | Terra | físico | 75 | 45 | Sim | dano condicional |
| 24 | N015 | Cinzel Quebra-Manto | Terra | físico | 80 | 55 | Sim | controle de atributos |
| 25 | G087 | Choque de Ombros | Neutro | físico | 70 | 25 | Não | cerco e armadilhas |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G001 — Bico de Brasas (E0)** — Se o alvo estiver Queimado antes do primeiro acerto, a bicada causa +10% de dano; não aplica Queimadura. **Visual:** Salambrasa concentra a técnica nas patas fortes e pele abrasadora; a animação destaca corpo de salamandra-galo, respeitando seu design homologado.
02. **G002 — Espora Incandescente (E30)** — Após causar dano, 20% de chance de Queimadura; se o alvo já estiver Queimado, reduz sua Defesa Física em 8% pelas próximas 2 ações dele, sem acumular. **Visual:** Salambrasa concentra a técnica nas patas fortes e pele abrasadora; a animação destaca pele quente como brasa, respeitando seu design homologado.
03. **G003 — Galope de Carvão (E35)** — Se o usuário sofreu dano de armadilha desde sua última ação, poder 105 em vez de 85; acerto bem-sucedido não remove a armadilha. **Visual:** Salambrasa concentra a técnica nas patas fortes e pele abrasadora; a animação destaca postura baixa e firme, respeitando seu design homologado.
04. **G004 — Garra Vulcânica (E50)** — Ao causar dano contra alvo com bônus positivo de Defesa Física, remove apenas o bônus mais recente e tem 15% de causar Queimadura. **Visual:** Salambrasa concentra a técnica nas patas fortes e pele abrasadora; a animação destaca força física e escória, respeitando seu design homologado.
05. **G005 — Quebra-Forja (E65)** — Atinge com poder normal e ignora 30% da parcela positiva de bônus temporários de Defesa Física do alvo; se não houver bônus, recupera 10 de energia após a ação. **Visual:** Salambrasa concentra a técnica nas patas fortes e pele abrasadora; a animação destaca corpo de salamandra-galo, respeitando seu design homologado.
06. **G011 — Chamado do Meio-Dia (E30)** — Invoca Ensolarado por 4 rodadas; se substituir Chuva, concede +10% de Defesa Mágica ao usuário até sua próxima ação. **Visual:** Salambrasa sustenta a técnica com posição defensiva rente ao solo; a animação destaca pele quente como brasa, respeitando seu design homologado.
07. **G012 — Retorno de Cinzas (E35)** — Até o próximo ataque físico direto recebido, reduz seu dano em 20%; se o acerto for o segundo da mesma ação, devolve 25% do dano efetivamente sofrido nesse segundo acerto. **Visual:** Salambrasa sustenta a técnica com posição defensiva rente ao solo; a animação destaca postura baixa e firme, respeitando seu design homologado.
08. **G013 — Cinzas da Discórdia (E35)** — Reduz Ataque Físico do alvo em 12% por suas 2 próximas ações; se ele estiver Queimado, em vez disso reduz 18%, sem acumular. **Visual:** Salambrasa sustenta a técnica com posição defensiva rente ao solo; a animação destaca força física e escória, respeitando seu design homologado.
09. **G014 — Reacender (E40)** — Cura 18% do HP máximo próprio; sob Ensolarado remove também Queimadura do próprio usuário, se existir. **Visual:** Salambrasa sustenta a técnica com posição defensiva rente ao solo; a animação destaca corpo de salamandra-galo, respeitando seu design homologado.
10. **G106 — Forja das Esporas (E60)** — Eleva Ataque Físico e Defesa Física próprios em 20% por 2 ações próprias; se estiver Queimado, concede apenas +25% de Defesa Física, sem anular a penalidade de Ataque da Queimadura. **Visual:** Salambrasa sustenta a técnica com posição defensiva rente ao solo; a animação destaca pele quente como brasa, respeitando seu design homologado.
11. **G131 — Cinza nos Olhos (E65)** — Exige Ensolarado ativo; reduz Ataque Mágico do alvo em 25% por 1 ação; contra alvo Queimado, redução cai para 12% e dura 2 ações, sem novo estado. **Visual:** Salambrasa sustenta a técnica com posição defensiva rente ao solo; a animação destaca postura baixa e firme, respeitando seu design homologado.
12. **N001 — Brasa de Rebate (E45)** — Poder 100, em vez de 75, se o usuário recebeu dano físico direto desde sua última ação própria, estando ativo. Verificação na resolução; não inclui dano de estados, passivas ou armadilhas. **Visual:** Salambrasa concentra a técnica nas patas fortes e pele abrasadora; a animação destaca força física e escória, respeitando seu design homologado.
13. **N003 — Fornalha Resguardada (E40)** — Remove Queimadura do próprio usuário, caso exista, e concede +20% de Defesa Mágica por suas próximas duas ações próprias. Se não estiver Queimado, concede apenas a proteção. **Visual:** Salambrasa sustenta a técnica com posição defensiva rente ao solo; a animação destaca corpo de salamandra-galo, respeitando seu design homologado.
14. **G043 — Chute de Cascalho (E0)** — Se o alvo tiver peso atual superior a 120% do natural, poder 55 em vez de 40; não altera peso. **Visual:** Compatibilidade cruzada: Salambrasa concentra a técnica nas patas fortes e pele abrasadora; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; pele quente como brasa identifica a animação.
15. **G044 — Marreta de Barro (E30)** — Após dano reduz Velocidade em 15% por 2 ações; se uma Tempestade de Areia estiver ativa, duração cai para 1 ação e reduz também Defesa Física em 8%. **Visual:** Compatibilidade cruzada: Salambrasa concentra a técnica nas patas fortes e pele abrasadora; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; postura baixa e firme identifica a animação.
16. **G045 — Cabeçada de Basalto (E35)** — Poder 105 em vez de 85 contra alvo com bônus positivo de Defesa Física; não remove bônus nem ignora defesa-base. **Visual:** Compatibilidade cruzada: Salambrasa concentra a técnica nas patas fortes e pele abrasadora; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; força física e escória identifica a animação.
17. **G046 — Pisão Sísmico (E50)** — Após causar dano, 20% de chance de Tonto; se o alvo já estiver Tonto, em vez de tentar novo estado reduz sua energia em 12. **Visual:** Compatibilidade cruzada: Salambrasa concentra a técnica nas patas fortes e pele abrasadora; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; corpo de salamandra-galo identifica a animação.
18. **G047 — Lança de Obsidiana (E55)** — Ignora 20% de bônus temporários de Defesa Física; se o usuário sofreu dano de estado desde sua última ação, poder 135 em vez de 120. **Visual:** Compatibilidade cruzada: Salambrasa concentra a técnica nas patas fortes e pele abrasadora; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; pele quente como brasa identifica a animação.
19. **G049 — Lodo Pressurizado (E30)** — Após causar dano reduz Defesa Mágica em 10% por 2 ações; se o alvo estiver sob Chuva, em vez disso reduz Defesa Física em 10% por 1 ação. **Visual:** Compatibilidade cruzada: Salambrasa canaliza a técnica através de calor desprendido da pele; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; postura baixa e firme identifica a animação.
20. **G053 — Tambor da Areia (E30)** — Invoca Tempestade de Areia por 4 rodadas; se substituir Ventania, o usuário ganha 10% de Defesa Física até sua próxima ação. **Visual:** Compatibilidade cruzada: Salambrasa sustenta a técnica com posição defensiva rente ao solo; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; força física e escória identifica a animação.
21. **G054 — Muralha Escavada (E35)** — Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. **Visual:** Compatibilidade cruzada: Salambrasa sustenta a técnica com posição defensiva rente ao solo; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; corpo de salamandra-galo identifica a animação.
22. **G102 — Couraça do Subsolo (E45)** — Eleva Defesa Física do usuário em 22% por 2 ações próprias; se estiver acima de 120% do peso natural, reduz também em 10% o dano do primeiro acerto físico recebido. **Visual:** Compatibilidade cruzada: Salambrasa sustenta a técnica com posição defensiva rente ao solo; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; pele quente como brasa identifica a animação.
23. **N013 — Pisada de Lastro (E45)** — Poder 100, em vez de 75, se o peso do usuário for igual ou superior a 120% de seu peso natural de referência no retrato de início da Rinha. **Visual:** Compatibilidade cruzada: Salambrasa concentra a técnica nas patas fortes e pele abrasadora; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; postura baixa e firme identifica a animação.
24. **N015 — Cinzel Quebra-Manto (E55)** — Ao calcular o dano, ignora 50% apenas da parcela positiva dos bônus temporários de Defesa Física do alvo; a Defesa Física básica e demais modificadores continuam aplicados. **Visual:** Compatibilidade cruzada: Salambrasa concentra a técnica nas patas fortes e pele abrasadora; usa areia, solo, lama ou pedras existentes ao redor. O elemento do golpe continua Terra; força física e escória identifica a animação.
25. **G087 — Choque de Ombros (E25)** — Se o usuário entrou por troca voluntária neste turno, poder 90 em vez de 70; não cancela armadilhas da entrada. **Visual:** Salambrasa concentra a técnica nas patas fortes e pele abrasadora; a animação destaca corpo de salamandra-galo, respeitando seu design homologado.

### #013 — Quartzaló · Terra + Elétrico
**Estado:** ficha_completa_homologada · **Raridade natural:** Comum · **Base no nível 50:** 370 · **Peso natural:** 8.5 kg
**Identidade de Rinha:** mago cristalino equilibrado / defesa
**Seis atributos:** HP: 70 · Ataque Físico: 45 · Defesa Física: 65 · Ataque Mágico: 80 · Defesa Mágica: 65 · Velocidade: 45
**Passiva:** Quartzo Energizado [homologada]
```json
{
  "afeta_golpes_fisicos": false,
  "afeta_outros_elementos": false,
  "bonus_percentual_dano": 8,
  "concede_ataque_adicional": false,
  "efeito": "Golpes mágicos ofensivos do próprio Quartzaló dos elementos Terra e Elétrico causam +8% de dano.",
  "nao_acumula_consigo": true,
  "nome": "Quartzo Energizado",
  "tipo": "automática/contínua durante rinha"
}
```
**Arte oficial (referência, sem redesenho):** Quartzaló_013_Arte_Oficial_Aprovada.png
**Evolução:** não detalhado na ficha externa #013; não presumir valores (ver dados completos no JSON).

**Cinco golpes de origem imutáveis**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|
| 1 | crina_poderosa | Crina Poderosa | Neutro | 40 | 0 | Ataque mágico básico de elemento Neutro; não possui efeitos adicionais. |
| 2 | concentracao | Concentração | — | — | 0 | Possui 40% de chance de remover estado negativo ativo. Respeita as regras oficiais de Tontura, incluindo a possível falha da ação. |
| 3 | O01303 | Lascas de Quartzo | Terra | 65 | 25 | Lança fragmentos de quartzo branco; dano mágico direto a um adversário, sem efeito secundário. |
| 4 | O01304 | Faíscas do Geodo | Elétrico | 85 | 40 | Descarga elétrica de cristais; 10% de chance de aplicar Tontura após causar dano. Apenas uma verificação de estado por ação, não substitui nem acumula estados negativos persistentes. |
| 5 | O01305 | Tempestade Cristalina | Terra | 115 | 55 | Chuva de cristais brancos; dano mágico direto elevado contra um único alvo. Não invoca Clima, aplica estado negativo ou instala armadilha. |

**25 golpes aprendíveis atribuídos**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G048 | Grão de Pedra | Terra | mágico | 40 | 0 | Não | campo/clima e sinergia |
| 02 | G049 | Lodo Pressurizado | Terra | mágico | 65 | 30 | Não | campo/clima e sinergia |
| 03 | G050 | Ondulação Rochosa | Terra | mágico | 85 | 35 | Não | gestão de energia |
| 04 | G051 | Fenda da Garganta | Terra | mágico | 105 | 50 | Não | pressão por estado |
| 05 | G052 | Erupção de Geodo | Terra | mágico | 130 | 70 | Não | dano condicional |
| 06 | G053 | Tambor da Areia | Terra | suporte | — | 30 | Não | campo/clima e sinergia |
| 07 | G054 | Muralha Escavada | Terra | suporte | — | 35 | Não | campo/clima e sinergia |
| 08 | G055 | Ninho de Pedregulhos | Terra | suporte | — | 45 | Não | cerco e armadilhas |
| 09 | G056 | Pedra de Revezamento | Terra | suporte | — | 35 | Não | cerco e armadilhas |
| 10 | G102 | Couraça do Subsolo | Terra | Suporte | — | 45 | Não | controle de atributos |
| 11 | N014 | Coluna de Guarda | Terra | suporte | — | 40 | Não | controle de atributos |
| 12 | N016 | Pedra da Impaciência | Terra | mágico | 75 | 45 | Não | dano condicional |
| 13 | G076 | Arco de Faísca | Elétrico | mágico | 40 | 0 | Não | campo/clima e sinergia |
| 14 | G077 | Pulso Condutor | Elétrico | mágico | 65 | 30 | Não | pressão por estado |
| 15 | G078 | Círculo Voltaico | Elétrico | mágico | 80 | 40 | Não | controle de atributos |
| 16 | G079 | Rede de Relâmpagos | Elétrico | mágico | 105 | 45 | Não | pressão por estado |
| 17 | G080 | Ruptura de Alta Tensão | Elétrico | mágico | 130 | 75 | Não | campo/clima e sinergia |
| 18 | G081 | Cântico dos Condutores | Elétrico | suporte | — | 35 | Não | campo/clima e sinergia |
| 19 | G082 | Bateria Compartilhada | Elétrico | suporte | — | 35 | Não | sustentação |
| 20 | G084 | Escudo Galvânico | Elétrico | suporte | — | 35 | Não | gestão de energia |
| 21 | G103 | Foco Centelhante | Elétrico | Suporte | — | 45 | Não | campo/clima e sinergia |
| 22 | G110 | Descarga Sináptica | Elétrico | Suporte | — | 60 | Não | campo/clima e sinergia |
| 23 | G062 | Sopro Circular | Ar | mágico | 40 | 0 | Sim | campo/clima e sinergia |
| 24 | G066 | Aurora do Zênite | Ar | mágico | 130 | 70 | Sim | ritmo, esquiva ou duplo golpe |
| 25 | N019 | Pena de Eco | Ar | mágico | 85 | 40 | Sim | ritmo, esquiva ou duplo golpe |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G048 — Grão de Pedra (E0)** — Se o usuário estiver sob Tempestade de Areia, projétil básico causa poder 55 em vez de 40; não invoca clima. **Visual:** Quartzaló canaliza a técnica através de refração elétrica através dos cristais; a animação destaca cristais de quartzo brancos, respeitando seu design homologado.
02. **G049 — Lodo Pressurizado (E30)** — Após causar dano reduz Defesa Mágica em 10% por 2 ações; se o alvo estiver sob Chuva, em vez disso reduz Defesa Física em 10% por 1 ação. **Visual:** Quartzaló canaliza a técnica através de refração elétrica através dos cristais; a animação destaca veios elétricos dourados, respeitando seu design homologado.
03. **G050 — Ondulação Rochosa (E35)** — Quando o alvo possui Velocidade superior à do usuário, poder 100 em vez de 85; após dano, retira 5 pontos de energia do alvo. **Visual:** Quartzaló canaliza a técnica através de refração elétrica através dos cristais; a animação destaca placas minerais marrons, respeitando seu design homologado.
04. **G051 — Fenda da Garganta (E50)** — Após causar dano 15% de Tonto; contra alvo com peso até 100% do natural, poder sobe de 105 para 120 sem alterar a chance. **Visual:** Quartzaló canaliza a técnica através de refração elétrica através dos cristais; a animação destaca plumagem creme e bege, respeitando seu design homologado.
05. **G052 — Erupção de Geodo (E70)** — Se o alvo possui proteção temporária contra dano mágico, poder 145 em vez de 130; após dano, consome a proteção normalmente, sem apagá-la antes do ataque. **Visual:** Quartzaló canaliza a técnica através de refração elétrica através dos cristais; a animação destaca cristais de quartzo brancos, respeitando seu design homologado.
06. **G053 — Tambor da Areia (E30)** — Invoca Tempestade de Areia por 4 rodadas; se substituir Ventania, o usuário ganha 10% de Defesa Física até sua próxima ação. **Visual:** Quartzaló sustenta a técnica com cristais alinhados como um escudo; a animação destaca veios elétricos dourados, respeitando seu design homologado.
07. **G054 — Muralha Escavada (E35)** — Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. **Visual:** Quartzaló sustenta a técnica com cristais alinhados como um escudo; a animação destaca placas minerais marrons, respeitando seu design homologado.
08. **G055 — Ninho de Pedregulhos (E45)** — Instala armadilha persistente que causa 8% do HP máximo do entrante voluntário; se ele estiver acima de 120% do peso natural, causa 11%, sem afetar entradas obrigatórias. **Visual:** Quartzaló sustenta a técnica com cristais alinhados como um escudo; a animação destaca plumagem creme e bege, respeitando seu design homologado.
09. **G056 — Pedra de Revezamento (E35)** — Troca usuário por aliado da reserva; o entrante recebe +15% de Defesa Física pelas próximas 2 ações e, sob Tempestade de Areia, ignora o dano de uma armadilha apenas na entrada da troca. **Visual:** Quartzaló sustenta a técnica com cristais alinhados como um escudo; a animação destaca cristais de quartzo brancos, respeitando seu design homologado.
10. **G102 — Couraça do Subsolo (E45)** — Eleva Defesa Física do usuário em 22% por 2 ações próprias; se estiver acima de 120% do peso natural, reduz também em 10% o dano do primeiro acerto físico recebido. **Visual:** Quartzaló sustenta a técnica com cristais alinhados como um escudo; a animação destaca veios elétricos dourados, respeitando seu design homologado.
11. **N014 — Coluna de Guarda (E40)** — O próximo ataque direto recebido pelo próprio usuário ativo terá 20%, em vez de 10%, de chance de ativar a defesa especial, SOMENTE se a Defesa relevante for pelo menos 120% do Ataque correspondente. A redução ao ativar continua 75%. **Visual:** Quartzaló sustenta a técnica com cristais alinhados como um escudo; a animação destaca placas minerais marrons, respeitando seu design homologado.
12. **N016 — Pedra da Impaciência (E45)** — Poder 100, em vez de 75, se a última ação efetivamente executada pelo alvo, antes desta, foi um golpe de Suporte (incluindo Concentração). **Visual:** Quartzaló canaliza a técnica através de refração elétrica através dos cristais; a animação destaca plumagem creme e bege, respeitando seu design homologado.
13. **G076 — Arco de Faísca (E0)** — Sob Santuário dos Raios, ataque básico tem poder 50 em vez de 40; não cria segundo golpe. **Visual:** Quartzaló canaliza a técnica através de refração elétrica através dos cristais; a animação destaca cristais de quartzo brancos, respeitando seu design homologado.
14. **G077 — Pulso Condutor (E30)** — Após dano, 15% de Tonto; se o alvo já estiver Paralisado, não tenta Tonto e drena 10 de energia adversária. **Visual:** Quartzaló canaliza a técnica através de refração elétrica através dos cristais; a animação destaca veios elétricos dourados, respeitando seu design homologado.
15. **G078 — Círculo Voltaico (E40)** — Após dano reduz Ataque Mágico do alvo em 10% por 2 ações; se o usuário tiver menos de 40 de energia após pagar o custo, devolve 8 de energia ao final da ação. **Visual:** Quartzaló canaliza a técnica através de refração elétrica através dos cristais; a animação destaca placas minerais marrons, respeitando seu design homologado.
16. **G079 — Rede de Relâmpagos (E45)** — Se o alvo já sofreu redução de Velocidade, poder 125 em vez de 105; se não, 15% de chance de Paralisia após dano. **Visual:** Quartzaló canaliza a técnica através de refração elétrica através dos cristais; a animação destaca plumagem creme e bege, respeitando seu design homologado.
17. **G080 — Ruptura de Alta Tensão (E75)** — Sob Santuário dos Raios, poder 145 em vez de 130; fora dele, 15% de chance de Tonto após dano, sem gerar acerto adicional. **Visual:** Quartzaló canaliza a técnica através de refração elétrica através dos cristais; a animação destaca cristais de quartzo brancos, respeitando seu design homologado.
18. **G081 — Cântico dos Condutores (E35)** — Invoca Santuário dos Raios por 4 rodadas; se o usuário estiver Paralisado, recebe 10 de energia após a execução válida, sem remover o estado. **Visual:** Quartzaló sustenta a técnica com cristais alinhados como um escudo; a animação destaca veios elétricos dourados, respeitando seu design homologado.
19. **G082 — Bateria Compartilhada (E35)** — Recupera 25 de energia de um aliado ativo escolhido; se o alvo tiver menos de 25 de energia antes da cura, recupera mais 5, sem ultrapassar 100. **Visual:** Quartzaló sustenta a técnica com cristais alinhados como um escudo; a animação destaca placas minerais marrons, respeitando seu design homologado.
20. **G084 — Escudo Galvânico (E35)** — Concede ao aliado escolhido redução de 25% do dano mágico na próxima ação ofensiva recebida; se tiver menos de 40 de energia no impacto, redução sobe para 35%. **Visual:** Quartzaló sustenta a técnica com cristais alinhados como um escudo; a animação destaca plumagem creme e bege, respeitando seu design homologado.
21. **G103 — Foco Centelhante (E45)** — Concede +25% Ataque Mágico por 1 ação própria; sob Santuário dos Raios, o primeiro golpe mágico que causar dano ainda recupera 10 de energia, sem repetir por segundo acerto. **Visual:** Quartzaló sustenta a técnica com cristais alinhados como um escudo; a animação destaca cristais de quartzo brancos, respeitando seu design homologado.
22. **G110 — Descarga Sináptica (E60)** — Eleva Ataque Mágico em 18% e Velocidade em 15% por 2 ações; sob Santuário dos Raios, a primeira tentativa de reduzir a própria Velocidade não surte efeito. **Visual:** Quartzaló sustenta a técnica com cristais alinhados como um escudo; a animação destaca veios elétricos dourados, respeitando seu design homologado.
23. **G062 — Sopro Circular (E0)** — Quando Ventania estiver ativa, projétil básico tem poder 55 em vez de 40; caso contrário permanece básico sem efeito. **Visual:** Compatibilidade cruzada: Quartzaló canaliza a técnica através de refração elétrica através dos cristais; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; placas minerais marrons identifica a animação.
24. **G066 — Aurora do Zênite (E70)** — Se o alvo recebeu um segundo golpe desde sua última ação, poder 150 em vez de 130; caso contrário, 10% de chance de Tonto após dano. **Visual:** Compatibilidade cruzada: Quartzaló canaliza a técnica através de refração elétrica através dos cristais; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; plumagem creme e bege identifica a animação.
25. **N019 — Pena de Eco (E40)** — Se o primeiro ataque deste golpe for totalmente evitado por esquiva do alvo, devolve 15 pontos de energia ao usuário ao terminar a ação (máximo 100). **Visual:** Compatibilidade cruzada: Quartzaló canaliza a técnica através de refração elétrica através dos cristais; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; cristais de quartzo brancos identifica a animação.

### #014 — Carangocó · Água + Terra
**Estado:** ficha_completa_homologada · **Raridade natural:** Comum · **Base no nível 50:** 370 · **Peso natural:** 10.5 kg
**Identidade de Rinha:** lutador costeiro / pinças e sedimentos
**Seis atributos:** HP: 75 · Ataque Físico: 80 · Defesa Física: 75 · Ataque Mágico: 40 · Defesa Mágica: 55 · Velocidade: 45
**Passiva:** Pinças de Sedimento [homologada]
```json
{
  "chance_ativacao_pct": 40,
  "convencional": "Uma verificação ao final de ação ofensiva física com dano",
  "duracao": "Até o alvo sair de campo ou ser derrotado",
  "nome": "Pinças de Sedimento",
  "reducao_defesa_fisica_pct": 10,
  "sequencial": "Uma verificação por acerto com dano até primeira ativação, efeito imediatamente após o acerto e aplicado nos próximos acertos da mesma sequência, sem acumular"
}
```
**Arte oficial (referência, sem redesenho):** Carangoco_014_Arte_Visual_Aprovada_Galetario.png
**Evolução:** não detalhado na ficha externa #014; não presumir valores (ver dados completos no JSON).

**Cinco golpes de origem imutáveis**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|
| 1 | garra_afiada | Garra Afiada | Neutro | 40 | 0 | Dano direto, sem efeitos secundários. |
| 2 | concentracao | Concentração | Sem elemento | — | 0 | 40% de chance de remover 1 estado negativo persistente do próprio usuário em execução válida; demais regras universais preservadas. |
| 3 | O01403 | Pinçada da Ressaca | Água | 70 | 30 | Ao acertar e causar dano, 30% de chance de reduzir Ataque Físico do alvo em 10% durante os próximos 2 turnos do alvo; uma verificação ao fim da ação; não acumula. |
| 4 | O01404 | Couraça de Lodo | Terra | — | 35 | Eleva Defesa Física em 25% e Defesa Mágica em 10% do próprio usuário durante 2 turnos próprios, contando o da ativação; não acumula. |
| 5 | O01405 | Cerco das Pinças | Terra | 40 × 1–5 | 55 | Golpe sequencial: até 5 acertos, chances condicionais de 100%/70%/50%/30%/15%; termina ao falhar; não recebe golpe extra de Velocidade. Cada acerto com dano pode acionar Pinças de Sedimento (40%) até a primeira ativação; a redução entra em vigor imediatamente após o acerto e beneficia os seguintes. |

**25 golpes aprendíveis atribuídos**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G015 | Bico de Marola | Água | físico | 40 | 0 | Não | pressão por estado |
| 02 | G016 | Cauda de Ressaca | Água | físico | 60 | 25 | Não | campo/clima e sinergia |
| 03 | G017 | Pancada de Maré | Água | físico | 80 | 35 | Não | dano condicional |
| 04 | G018 | Açoite de Corredeira | Água | físico | 95 | 50 | Não | pressão por estado |
| 05 | G019 | Quebra-Cais | Água | físico | 120 | 55 | Não | gestão de energia |
| 06 | G020 | Gota Disparada | Água | mágico | 40 | 0 | Não | sustentação |
| 07 | G022 | Coluna de Espuma | Água | mágico | 80 | 40 | Não | pressão por estado |
| 08 | G025 | Canto das Nuvens | Água | suporte | — | 30 | Não | campo/clima e sinergia |
| 09 | G026 | Névoa Protetora | Água | suporte | — | 30 | Não | pressão por estado |
| 10 | G027 | Maré de Retirada | Água | suporte | — | 40 | Não | cerco e armadilhas |
| 11 | N005 | Fôlego de Ressaca | Água | físico | 70 | 40 | Não | pressão por estado |
| 12 | N006 | Redemoinho Exaustivo | Água | suporte | — | 45 | Não | cerco e armadilhas |
| 13 | N007 | Banho Sereno | Água | suporte | — | 45 | Não | sustentação |
| 14 | G067 | Assobio dos Quatro Ventos | Ar | suporte | — | 30 | Sim | campo/clima e sinergia |
| 15 | G043 | Chute de Cascalho | Terra | físico | 40 | 0 | Não | dano condicional |
| 16 | G044 | Marreta de Barro | Terra | físico | 65 | 30 | Não | campo/clima e sinergia |
| 17 | G045 | Cabeçada de Basalto | Terra | físico | 85 | 35 | Não | controle de atributos |
| 18 | G046 | Pisão Sísmico | Terra | físico | 100 | 50 | Não | pressão por estado |
| 19 | G053 | Tambor da Areia | Terra | suporte | — | 30 | Não | campo/clima e sinergia |
| 20 | G054 | Muralha Escavada | Terra | suporte | — | 35 | Não | campo/clima e sinergia |
| 21 | G055 | Ninho de Pedregulhos | Terra | suporte | — | 45 | Não | cerco e armadilhas |
| 22 | N013 | Pisada de Lastro | Terra | físico | 75 | 45 | Não | dano condicional |
| 23 | N014 | Coluna de Guarda | Terra | suporte | — | 40 | Não | controle de atributos |
| 24 | N015 | Cinzel Quebra-Manto | Terra | físico | 80 | 55 | Não | controle de atributos |
| 25 | G030 | Ferrão de Trepadeira | Planta | físico | 55 | 25 | Sim | pressão por estado |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G015 — Bico de Marola (E0)** — Se o usuário estiver Afogado, poder sobe de 40 para 55 no primeiro acerto; não reduz nem remove Afogamento. **Visual:** Carangocó concentra a técnica nas pinças nas asas e carapaça; a animação destaca asas em forma de pinças, respeitando seu design homologado.
02. **G016 — Cauda de Ressaca (E25)** — Após causar dano, reduz Velocidade do alvo em 12% por 2 ações; sob Chuva, reduz apenas 8%, mas recupera 10 de energia ao final da ação. **Visual:** Carangocó concentra a técnica nas pinças nas asas e carapaça; a animação destaca carapaça vermelho-coral, respeitando seu design homologado.
03. **G017 — Pancada de Maré (E35)** — Se o alvo entrou voluntariamente neste turno, poder sobe de 80 para 100; caso contrário, após causar dano ignora o próximo efeito de redução de Velocidade do usuário até sua próxima ação. **Visual:** Carangocó concentra a técnica nas pinças nas asas e carapaça; a animação destaca cauda em leque azul e creme, respeitando seu design homologado.
04. **G018 — Açoite de Corredeira (E50)** — Após causar dano, 18% de chance de Afogamento; se o alvo já estava Afogado, em vez de tentar aplicar o estado drena 12 de energia. **Visual:** Carangocó concentra a técnica nas pinças nas asas e carapaça; a animação destaca conchas e cracas das placas, respeitando seu design homologado.
05. **G019 — Quebra-Cais (E55)** — Contra alvo com mais de 70 de energia, poder 135 em vez de 120; após causar dano nessa condição, o usuário não pode receber bônus temporário de Velocidade até sua próxima ação. **Visual:** Carangocó concentra a técnica nas pinças nas asas e carapaça; a animação destaca asas em forma de pinças, respeitando seu design homologado.
06. **G020 — Gota Disparada (E0)** — Se o usuário recebeu cura desde sua ação anterior, poder 55 em vez de 40; não ativa curas adicionais. **Visual:** Carangocó canaliza a técnica através de salpicos e sedimento de mangue; a animação destaca carapaça vermelho-coral, respeitando seu design homologado.
07. **G022 — Coluna de Espuma (E40)** — Após causar dano tem 20% de chance de Afogamento; se o usuário possuir bônus temporário de Defesa Mágica, a chance cai para 10%, mas poder sobe para 95. **Visual:** Carangocó canaliza a técnica através de salpicos e sedimento de mangue; a animação destaca cauda em leque azul e creme, respeitando seu design homologado.
08. **G025 — Canto das Nuvens (E30)** — Invoca Chuva por 4 rodadas; caso substitua Ensolarado, cura 8% do HP máximo próprio sem afetar a reserva. **Visual:** Carangocó sustenta a técnica com carapaça e pinças em guarda; a animação destaca conchas e cracas das placas, respeitando seu design homologado.
09. **G026 — Névoa Protetora (E30)** — O aliado escolhido recebe −25% de dano mágico na próxima ação ofensiva recebida; se já estiver Afogado, recupera 12 de energia ao ativar a barreira. **Visual:** Carangocó sustenta a técnica com carapaça e pinças em guarda; a animação destaca asas em forma de pinças, respeitando seu design homologado.
10. **G027 — Maré de Retirada (E40)** — Troca voluntariamente por aliado da reserva; o entrante recupera 8% de HP máximo e não sofre redução de Velocidade de armadilha somente nessa entrada; outros efeitos de armadilha permanecem. **Visual:** Carangocó sustenta a técnica com carapaça e pinças em guarda; a animação destaca carapaça vermelho-coral, respeitando seu design homologado.
11. **N005 — Fôlego de Ressaca (E40)** — Se o alvo já tiver Afogamento no início desta ação e ao menos um acerto causar dano, o usuário recupera 15 pontos de energia ao terminar a ação (máximo 100). **Visual:** Carangocó concentra a técnica nas pinças nas asas e carapaça; a animação destaca cauda em leque azul e creme, respeitando seu design homologado.
12. **N006 — Redemoinho Exaustivo (E45)** — Instala no lado adversário uma armadilha persistente que retira 15 pontos da energia atual de cada Cocorídeo que entra por troca voluntária, nunca abaixo de zero. **Visual:** Carangocó sustenta a técnica com carapaça e pinças em guarda; a animação destaca conchas e cracas das placas, respeitando seu design homologado.
13. **N007 — Banho Sereno (E45)** — Recupera 10% do HP máximo do usuário ativo e remove o estado negativo persistente que ele tenha, se houver. **Visual:** Carangocó sustenta a técnica com carapaça e pinças em guarda; a animação destaca asas em forma de pinças, respeitando seu design homologado.
14. **G067 — Assobio dos Quatro Ventos (E30)** — Invoca Ventania por 4 rodadas; se substituir Tempestade de Areia, o usuário recebe +10% de Velocidade até sua próxima ação. **Visual:** Compatibilidade cruzada: Carangocó sustenta a técnica com carapaça e pinças em guarda; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; carapaça vermelho-coral identifica a animação.
15. **G043 — Chute de Cascalho (E0)** — Se o alvo tiver peso atual superior a 120% do natural, poder 55 em vez de 40; não altera peso. **Visual:** Carangocó concentra a técnica nas pinças nas asas e carapaça; a animação destaca cauda em leque azul e creme, respeitando seu design homologado.
16. **G044 — Marreta de Barro (E30)** — Após dano reduz Velocidade em 15% por 2 ações; se uma Tempestade de Areia estiver ativa, duração cai para 1 ação e reduz também Defesa Física em 8%. **Visual:** Carangocó concentra a técnica nas pinças nas asas e carapaça; a animação destaca conchas e cracas das placas, respeitando seu design homologado.
17. **G045 — Cabeçada de Basalto (E35)** — Poder 105 em vez de 85 contra alvo com bônus positivo de Defesa Física; não remove bônus nem ignora defesa-base. **Visual:** Carangocó concentra a técnica nas pinças nas asas e carapaça; a animação destaca asas em forma de pinças, respeitando seu design homologado.
18. **G046 — Pisão Sísmico (E50)** — Após causar dano, 20% de chance de Tonto; se o alvo já estiver Tonto, em vez de tentar novo estado reduz sua energia em 12. **Visual:** Carangocó concentra a técnica nas pinças nas asas e carapaça; a animação destaca carapaça vermelho-coral, respeitando seu design homologado.
19. **G053 — Tambor da Areia (E30)** — Invoca Tempestade de Areia por 4 rodadas; se substituir Ventania, o usuário ganha 10% de Defesa Física até sua próxima ação. **Visual:** Carangocó sustenta a técnica com carapaça e pinças em guarda; a animação destaca cauda em leque azul e creme, respeitando seu design homologado.
20. **G054 — Muralha Escavada (E35)** — Concede a um aliado redução de 30% no próximo dano físico direto recebido; se o ataque ocorrer durante Tempestade de Areia, também preserva 8 de energia do aliado, descontados ao final da ação inimiga. **Visual:** Carangocó sustenta a técnica com carapaça e pinças em guarda; a animação destaca conchas e cracas das placas, respeitando seu design homologado.
21. **G055 — Ninho de Pedregulhos (E45)** — Instala armadilha persistente que causa 8% do HP máximo do entrante voluntário; se ele estiver acima de 120% do peso natural, causa 11%, sem afetar entradas obrigatórias. **Visual:** Carangocó sustenta a técnica com carapaça e pinças em guarda; a animação destaca asas em forma de pinças, respeitando seu design homologado.
22. **N013 — Pisada de Lastro (E45)** — Poder 100, em vez de 75, se o peso do usuário for igual ou superior a 120% de seu peso natural de referência no retrato de início da Rinha. **Visual:** Carangocó concentra a técnica nas pinças nas asas e carapaça; a animação destaca carapaça vermelho-coral, respeitando seu design homologado.
23. **N014 — Coluna de Guarda (E40)** — O próximo ataque direto recebido pelo próprio usuário ativo terá 20%, em vez de 10%, de chance de ativar a defesa especial, SOMENTE se a Defesa relevante for pelo menos 120% do Ataque correspondente. A redução ao ativar continua 75%. **Visual:** Carangocó sustenta a técnica com carapaça e pinças em guarda; a animação destaca cauda em leque azul e creme, respeitando seu design homologado.
24. **N015 — Cinzel Quebra-Manto (E55)** — Ao calcular o dano, ignora 50% apenas da parcela positiva dos bônus temporários de Defesa Física do alvo; a Defesa Física básica e demais modificadores continuam aplicados. **Visual:** Carangocó concentra a técnica nas pinças nas asas e carapaça; a animação destaca conchas e cracas das placas, respeitando seu design homologado.
25. **G030 — Ferrão de Trepadeira (E25)** — Após dano, 25% de chance de Envenenamento; caso o alvo já esteja Envenenado, reduz 10 de sua energia em vez de reaplicar estado. **Visual:** Compatibilidade cruzada: Carangocó concentra a técnica nas pinças nas asas e carapaça; manipula folhas, sementes, raízes ou pólen do cenário. O elemento do golpe continua Planta; asas em forma de pinças identifica a animação.

### #015 — Faíscocó · Fogo + Elétrico
**Estado:** em_desenvolvimento · **Raridade natural:** Raro · **Base no nível 50:** 430 · **Peso natural:** não homologado
**Identidade de Rinha:** ave tempestífuga / chama e eletricidade (visual aprovado; ficha pendente)
**Seis atributos:** HP: 70 · Ataque Físico: 60 · Defesa Física: 50 · Ataque Mágico: 95 · Defesa Mágica: 55 · Velocidade: 100
**Passiva:** Indução Incandescente [proposta_para_testes_NAO_HOMOLOGADA]
```json
null
```
**Arte oficial (referência, sem redesenho):** Ficha oficial do Faíscocó.png
**Evolução:** não definida (ver dados completos no JSON).

**Golpes de origem: não homologados; não inventar.**
| Slot | ID | Golpe | Elemento | P | Energia | Efeito/nota |
|---:|---|---|---|---:|---:|---|

**25 golpes aprendíveis PRÉ-SELECIONADOS — NÃO HOMOLOGADOS**
| Nº | Código | Golpe | Elemento | Cat. | P | E | Fora dos elementos? | Papel |
|---:|---|---|---|---|---:|---:|---|---|
| 01 | G001 | Bico de Brasas | Fogo | físico | 40 | 0 | Não | pressão por estado |
| 02 | G002 | Espora Incandescente | Fogo | físico | 65 | 30 | Não | pressão por estado |
| 03 | G003 | Galope de Carvão | Fogo | físico | 85 | 35 | Não | cerco e armadilhas |
| 04 | G006 | Faísca de Terreiro | Fogo | mágico | 40 | 0 | Não | campo/clima e sinergia |
| 05 | G007 | Sopro de Cinzas | Fogo | mágico | 65 | 30 | Não | campo/clima e sinergia |
| 06 | G008 | Rosácea de Fagulhas | Fogo | mágico | 85 | 40 | Não | controle de atributos |
| 07 | G011 | Chamado do Meio-Dia | Fogo | suporte | — | 30 | Não | campo/clima e sinergia |
| 08 | G013 | Cinzas da Discórdia | Fogo | suporte | — | 35 | Não | pressão por estado |
| 09 | N001 | Brasa de Rebate | Fogo | físico | 75 | 45 | Não | cerco e armadilhas |
| 10 | N002 | Cinza Desarmadora | Fogo | mágico | 70 | 45 | Não | dano e cobertura |
| 11 | N003 | Fornalha Resguardada | Fogo | suporte | — | 40 | Não | pressão por estado |
| 12 | N004 | Brilho de Carvão | Fogo | mágico | 80 | 45 | Não | campo/clima e sinergia |
| 13 | G071 | Bicada Elétrica | Elétrico | físico | 40 | 0 | Não | pressão por estado |
| 14 | G072 | Espora de Cobre | Elétrico | físico | 65 | 30 | Não | pressão por estado |
| 15 | G073 | Investida do Dínamo | Elétrico | físico | 85 | 35 | Não | gestão de energia |
| 16 | G074 | Cascata de Centelhas | Elétrico | físico | 100 | 50 | Não | campo/clima e sinergia |
| 17 | G076 | Arco de Faísca | Elétrico | mágico | 40 | 0 | Não | campo/clima e sinergia |
| 18 | G077 | Pulso Condutor | Elétrico | mágico | 65 | 30 | Não | pressão por estado |
| 19 | G078 | Círculo Voltaico | Elétrico | mágico | 80 | 40 | Não | controle de atributos |
| 20 | G079 | Rede de Relâmpagos | Elétrico | mágico | 105 | 45 | Não | pressão por estado |
| 21 | G081 | Cântico dos Condutores | Elétrico | suporte | — | 35 | Não | campo/clima e sinergia |
| 22 | G083 | Campo de Centelhas | Elétrico | suporte | — | 45 | Não | cerco e armadilhas |
| 23 | G110 | Descarga Sináptica | Elétrico | Suporte | — | 60 | Não | campo/clima e sinergia |
| 24 | G057 | Asa Riscante | Ar | físico | 40 | 0 | Sim | ritmo, esquiva ou duplo golpe |
| 25 | N018 | Vórtice de Passagem | Ar | suporte | — | 45 | Sim | cerco e armadilhas |

**Detalhamento mecânico e adaptação à anatomia:**
01. **G001 — Bico de Brasas (E0)** — Se o alvo estiver Queimado antes do primeiro acerto, a bicada causa +10% de dano; não aplica Queimadura. **Visual:** Faíscocó concentra a técnica nas patas ligeiras e anel condutor na cauda; a animação destaca crista incandescente irregular, respeitando seu design homologado.
02. **G002 — Espora Incandescente (E30)** — Após causar dano, 20% de chance de Queimadura; se o alvo já estiver Queimado, reduz sua Defesa Física em 8% pelas próximas 2 ações dele, sem acumular. **Visual:** Faíscocó concentra a técnica nas patas ligeiras e anel condutor na cauda; a animação destaca plumagem creme e carvão, respeitando seu design homologado.
03. **G003 — Galope de Carvão (E35)** — Se o usuário sofreu dano de armadilha desde sua última ação, poder 105 em vez de 85; acerto bem-sucedido não remove a armadilha. **Visual:** Faíscocó concentra a técnica nas patas ligeiras e anel condutor na cauda; a animação destaca manto vermelho termelétrico, respeitando seu design homologado.
04. **G006 — Faísca de Terreiro (E0)** — Se Ensolarado estiver ativo, o projétil básico tem 15% de chance de reduzir Ataque Mágico do alvo em 8% por 1 ação; caso contrário, dano normal. **Visual:** Faíscocó canaliza a técnica através de chamas e pequenas faíscas geradas pela cauda; a animação destaca anel segmentado condutor na cauda, respeitando seu design homologado.
05. **G007 — Sopro de Cinzas (E30)** — Acertar inimigo sob Chuva causa poder 80 em vez de 65; se não chover, 20% de chance de Queimadura após dano. **Visual:** Faíscocó canaliza a técnica através de chamas e pequenas faíscas geradas pela cauda; a animação destaca crista incandescente irregular, respeitando seu design homologado.
06. **G008 — Rosácea de Fagulhas (E40)** — Se o alvo tiver bônus positivo de Ataque Mágico, reduz esse bônus pela metade durante o cálculo do dano deste golpe; não remove o bônus depois. **Visual:** Faíscocó canaliza a técnica através de chamas e pequenas faíscas geradas pela cauda; a animação destaca plumagem creme e carvão, respeitando seu design homologado.
07. **G011 — Chamado do Meio-Dia (E30)** — Invoca Ensolarado por 4 rodadas; se substituir Chuva, concede +10% de Defesa Mágica ao usuário até sua próxima ação. **Visual:** Faíscocó sustenta a técnica com manto termelétrico e anel de faíscas; a animação destaca manto vermelho termelétrico, respeitando seu design homologado.
08. **G013 — Cinzas da Discórdia (E35)** — Reduz Ataque Físico do alvo em 12% por suas 2 próximas ações; se ele estiver Queimado, em vez disso reduz 18%, sem acumular. **Visual:** Faíscocó sustenta a técnica com manto termelétrico e anel de faíscas; a animação destaca anel segmentado condutor na cauda, respeitando seu design homologado.
09. **N001 — Brasa de Rebate (E45)** — Poder 100, em vez de 75, se o usuário recebeu dano físico direto desde sua última ação própria, estando ativo. Verificação na resolução; não inclui dano de estados, passivas ou armadilhas. **Visual:** Faíscocó concentra a técnica nas patas ligeiras e anel condutor na cauda; a animação destaca crista incandescente irregular, respeitando seu design homologado.
10. **N002 — Cinza Desarmadora (E45)** — Após ao menos um acerto com dano, elimina um bônus temporário positivo de Ataque Mágico do alvo, se houver, escolhendo o mais forte; em empate, o mais antigo. O dano deste golpe é calculado antes da remoção. **Visual:** Faíscocó canaliza a técnica através de chamas e pequenas faíscas geradas pela cauda; a animação destaca plumagem creme e carvão, respeitando seu design homologado.
11. **N003 — Fornalha Resguardada (E40)** — Remove Queimadura do próprio usuário, caso exista, e concede +20% de Defesa Mágica por suas próximas duas ações próprias. Se não estiver Queimado, concede apenas a proteção. **Visual:** Faíscocó sustenta a técnica com manto termelétrico e anel de faíscas; a animação destaca manto vermelho termelétrico, respeitando seu design homologado.
12. **N004 — Brilho de Carvão (E45)** — Se o clima Ensolarado estiver ativo no momento do primeiro acerto com dano, o usuário recupera 15 pontos de energia após a ação, respeitando o máximo de 100. **Visual:** Faíscocó canaliza a técnica através de chamas e pequenas faíscas geradas pela cauda; a animação destaca anel segmentado condutor na cauda, respeitando seu design homologado.
13. **G071 — Bicada Elétrica (E0)** — Se o alvo estiver Paralisado, poder 50 em vez de 40; não aplica Paralisia adicional. **Visual:** Faíscocó concentra a técnica nas patas ligeiras e anel condutor na cauda; a animação destaca crista incandescente irregular, respeitando seu design homologado.
14. **G072 — Espora de Cobre (E30)** — Após dano, 18% de chance de Tonto; se o alvo já estiver Tonto, concede +8 de energia ao usuário em vez de tentar reaplicação. **Visual:** Faíscocó concentra a técnica nas patas ligeiras e anel condutor na cauda; a animação destaca plumagem creme e carvão, respeitando seu design homologado.
15. **G073 — Investida do Dínamo (E35)** — Contra alvo com menos de 30 de energia, poder 100 em vez de 85; não modifica energia do alvo. **Visual:** Faíscocó concentra a técnica nas patas ligeiras e anel condutor na cauda; a animação destaca manto vermelho termelétrico, respeitando seu design homologado.
16. **G074 — Cascata de Centelhas (E50)** — Após dano reduz Defesa Física em 12% por 2 ações; sob Santuário dos Raios, reduz em 16% por 1 ação e recupera 5 de energia. **Visual:** Faíscocó concentra a técnica nas patas ligeiras e anel condutor na cauda; a animação destaca anel segmentado condutor na cauda, respeitando seu design homologado.
17. **G076 — Arco de Faísca (E0)** — Sob Santuário dos Raios, ataque básico tem poder 50 em vez de 40; não cria segundo golpe. **Visual:** Faíscocó canaliza a técnica através de chamas e pequenas faíscas geradas pela cauda; a animação destaca crista incandescente irregular, respeitando seu design homologado.
18. **G077 — Pulso Condutor (E30)** — Após dano, 15% de Tonto; se o alvo já estiver Paralisado, não tenta Tonto e drena 10 de energia adversária. **Visual:** Faíscocó canaliza a técnica através de chamas e pequenas faíscas geradas pela cauda; a animação destaca plumagem creme e carvão, respeitando seu design homologado.
19. **G078 — Círculo Voltaico (E40)** — Após dano reduz Ataque Mágico do alvo em 10% por 2 ações; se o usuário tiver menos de 40 de energia após pagar o custo, devolve 8 de energia ao final da ação. **Visual:** Faíscocó canaliza a técnica através de chamas e pequenas faíscas geradas pela cauda; a animação destaca manto vermelho termelétrico, respeitando seu design homologado.
20. **G079 — Rede de Relâmpagos (E45)** — Se o alvo já sofreu redução de Velocidade, poder 125 em vez de 105; se não, 15% de chance de Paralisia após dano. **Visual:** Faíscocó canaliza a técnica através de chamas e pequenas faíscas geradas pela cauda; a animação destaca anel segmentado condutor na cauda, respeitando seu design homologado.
21. **G081 — Cântico dos Condutores (E35)** — Invoca Santuário dos Raios por 4 rodadas; se o usuário estiver Paralisado, recebe 10 de energia após a execução válida, sem remover o estado. **Visual:** Faíscocó sustenta a técnica com manto termelétrico e anel de faíscas; a animação destaca crista incandescente irregular, respeitando seu design homologado.
22. **G083 — Campo de Centelhas (E45)** — Instala armadilha persistente que reduz Defesa Mágica do entrante voluntário em 12% pelas próximas 2 ações; se ele estiver Paralisado, reduz em 15% por 1 ação. **Visual:** Faíscocó sustenta a técnica com manto termelétrico e anel de faíscas; a animação destaca plumagem creme e carvão, respeitando seu design homologado.
23. **G110 — Descarga Sináptica (E60)** — Eleva Ataque Mágico em 18% e Velocidade em 15% por 2 ações; sob Santuário dos Raios, a primeira tentativa de reduzir a própria Velocidade não surte efeito. **Visual:** Faíscocó sustenta a técnica com manto termelétrico e anel de faíscas; a animação destaca manto vermelho termelétrico, respeitando seu design homologado.
24. **G057 — Asa Riscante (E0)** — Se a Velocidade do usuário superar a do alvo, poder 50 em vez de 40; sem alterar a chance universal de segundo golpe. **Visual:** Compatibilidade cruzada: Faíscocó concentra a técnica nas patas ligeiras e anel condutor na cauda; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; anel segmentado condutor na cauda identifica a animação.
25. **N018 — Vórtice de Passagem (E45)** — Troca voluntariamente o usuário por aliado apto da reserva. Somente nessa entrada, o substituto ignora os gatilhos das armadilhas existentes no lado aliado. **Visual:** Compatibilidade cruzada: Faíscocó sustenta a técnica com manto termelétrico e anel de faíscas; usa batidas das asas, sopro ou deslocamento para mover o ar. O elemento do golpe continua Ar; crista incandescente irregular identifica a animação.

## Pendências de auditoria
- **#001 — base_historica_diverge_da_escala_v03:** Tabela species soma 850; quadro natural v0.3 soma 550. Preservar ambos; não sincronizar automaticamente.
- **#002 — base_historica_diverge_da_escala_v03:** Tabela species soma 850; quadro natural v0.3 soma 550. Preservar ambos; não sincronizar automaticamente.
- **#003 — base_historica_diverge_da_escala_v03:** Tabela species soma 850; quadro natural v0.3 soma 550. Preservar ambos; não sincronizar automaticamente.
- **#004 — base_historica_diverge_da_escala_v03:** Tabela species soma 850; quadro natural v0.3 soma 550. Preservar ambos; não sincronizar automaticamente.
- **#005 — base_historica_diverge_da_escala_v03:** Tabela species soma 850; quadro natural v0.3 soma 550. Preservar ambos; não sincronizar automaticamente.
- **#006 — base_historica_diverge_da_escala_v03:** Tabela species soma 850; quadro natural v0.3 soma 550. Preservar ambos; não sincronizar automaticamente.
- **#015 — ficha_incompleta:** Passiva, cinco golpes originais, peso e evolução não homologados; 25 aprendíveis somente pré-seleção.
- **#015 — arte_legenda_desatualizada:** Imagem anterior indica Comum; aprovação posterior define Raro. Não alterar a arte sem autorização.

## Auditorias
- **Conformidade e nomenclatura:** 14 fichas completas, 1 parcial; escala atual preservada; nomenclatura histórica separada.
- **Integridade SQLite:** `integrity_check=ok`, `foreign_key_check=0`; tabelas de captura/espécies/passivas históricas preservadas por hash.
- **Originalidade e visual:** nenhum desenho refeito, justificativas visuais dos aprendíveis reaproveitadas sem alterar seus efeitos canônicos.
- **Rinhas e balanceamento:** consistência documental validada; testes de simulação e mod Minecraft ainda pendentes.
- **Rastreabilidade:** base 1.2.35 e ramo Galolpédia/repertórios 1.2.30 combinados em cópia derivada 1.2.36; fontes originais preservadas.

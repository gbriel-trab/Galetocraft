# Galetocraft — Análise de desenvolvimento do mod (18/11/2026)

Esta análise compara o que está **projetado** (base vigente, revisão 4, e regras oficiais) com o que está **implementado** no mod (`galetocraft/`). Depois lista o que falta em cada sistema e define o roteiro.

## 1. Situação em uma frase

O design está muito à frente do código. A base documenta 23 espécies, 268 golpes, combate, captura, progressão, reprodução e Mestres. O mod é uma **vitrine**: 12 criaturas com modelo 3D, IA neutra de galinha e nenhum sistema de jogo.

**Ambiente:** a partir de 18/11 esta sessão compila o mod. O ambiente "Galetocraft" libera Fabric, Mojang e GeckoLib, e o JDK 25 está instalado.

## 2. Mapa por sistema

> A coluna "No mod hoje" mostra a situação do início de 18/11. Desde então, os sistemas 3 a 12, 17 e 19 ganharam implementação no núcleo de regras e um motor de Rinha simulado. O detalhe está em `docs/PROGRESSO_DESENVOLVIMENTO.md`.

Legenda do design: ✅ homologado · 🟡 parcial (só parte homologada, ou no histórico sem migração) · ⛔ pendente de decisão do criador.

| # | Sistema | Design | No mod hoje | O que falta implementar |
|---:|---|---|---|---|
| 1 | **Dados das espécies** (Galetário) | ✅ 23 fichas: atributos, elementos, passiva, peso, alas, sexo, arte | Só nome, modelo e números de mob vanilla (vida, dano, velocidade arbitrários) | Carregar a base no mod (espécie, raridade, elementos, atributos, golpes); 11 espécies sem entidade nem modelo (#002, #013–#018, #020–#023) |
| 2 | **Galeto individual** | 🟡 nível, IV 1–40, EV, peso, sexo, 5 golpes equipados, dono. ⛔ como IV, EV e peso entram nos atributos com a norma do nível 50 | Nada: toda criatura é igual | Estado persistente por indivíduo (NBT/attachment), geração ao nascer ou aparecer, sincronização com o cliente |
| 3 | **Progressão de atributos** | ✅ níveis 50–100: `A50×(L+50)/100`. ⛔ curva 1–49 e HP efetivo/Vitalidade V5.6.1 | Nada | Função de atributos por nível (50–100) e HP. Os pendentes ficam como parâmetro, sem número inventado |
| 4 | **Rinha: estrutura** | ✅ 3v3, 1 ativo, trocas com prioridade e ocultas, substituição gratuita após derrota, vitória ao derrotar os 3, empate de Velocidade 50/50. ⛔ desempate de trocas com Velocidade igual; espécies repetidas no trio | Nada | Motor de turnos: seleção de ações, ordem, resolução, troca, derrota, fim |
| 5 | **Energia** | ✅ teto 100, entra com 100, +20 no início do turno, golpe sem energia é inválido | Nada | No motor |
| 6 | **Dano** | ✅ **V5.6**: `HPmax × Poder/400 × (A/D)^0,7`, contínuo, arredondamento único para cima, mínimo 1. ✅ esquiva universal `clamp(7,5 + 5(Vd−Va)/(Vd+Va), 5, 10)%` | Nada | Fórmula, esquiva e ordem dos modificadores (elemento → bônus → anatomia → proteção) |
| 7 | **Elementos** | ✅ matriz 6×6, Tipagem Dupla V1 (4× só com fraqueza comum), Nexo V2.0 (tripla) | Nada | Tabela e regra dupla/tripla |
| 8 | **Golpe Duplo V2.2** | ✅ chance `min(0,5; 0,25+0,5(Va/Vd−1))`, 2º acerto com 50% de dano, chance intrínseca independente | Nada | No motor |
| 9 | **Concentração V2.3 + Pena de Ritmo** | ✅ +35 de energia, 40% de remover estado, Pena por equipe e 4 Cantos | Nada | No motor |
| 10 | **Mira Anatômica V1.5** | ✅ 4 regiões, Pressão, Exposição, Ruptura, Guarda e Leitura Perfeita | Nada | No motor; escolhas ocultas na interface |
| 11 | **Estados negativos** | ✅ Queimadura, Envenenamento, Afogamento, Tonto, Paralisia (1 por Galeto, suspensos na reserva). 🟡 Sono só aparece na captura | Nada | Efeitos de fim de rodada e checagens de ação |
| 12 | **Climas e Santuários** | ✅ 4 climas (±25%/10%) e 2 santuários (+15%, energia, cura), 4 rodadas, 1 de cada | Nada | No motor |
| 13 | **Passivas** | ✅ 23 descritas; 14 com efeito estruturado e 9 só em texto | Nada | Um gancho de evento por passiva (entrada, acerto, fim de rodada…) |
| 14 | **Efeitos dos golpes** | ✅ 268 golpes distintos, mas só 39 dos 690 vínculos têm efeito estruturado; o resto é texto | Nada | Estruturar os efeitos (condição → efeito) a partir do texto oficial, sem mudar o sentido, e implementar por família (redução de atributo, estado, clima, cura, armadilha…) |
| 15 | **Itens segurados** | ✅ até 2, de categorias diferentes (Ambiental, Ofensiva, Defensiva, Utilitária). 🟡 os 20 itens são candidatos | Nada | Depois do motor; os itens dependem de aprovação |
| 16 | **Interface da Rinha** | ✅ menu Galetos / Combate / Itens / Fugir, painéis, Histórico da Rinha | Nada | Telas do cliente e rede |
| 17 | **Captura (Pena)** | 🟡 Pena de 5 níveis, fórmula `P = 100·f/(f+D)`, cooldown, captura no mundo e na Rinha (Betas 1.2.56–1.2.59, marcadas oficiais, fora da camada vigente) | Nada | Item Pena, feixe, chance, cooldown, ida para a equipe ou reserva |
| 18 | **Treinador** | 🟡 equipe de 5 + reservas ilimitadas | Nada | Inventário de Galetos por jogador, persistência, interface |
| 19 | **XP e níveis** | 🟡 V1.260: `T(N)=(N−1)³+10(N−1)²`, XP só em Rinha vencida | Nada | No motor e na persistência |
| 20 | **Aprendizado de golpes** | 🟡 15 por nível + 15 por Mestres por espécie, mas a tabela de níveis **não está** na camada vigente (fica em tabelas históricas e fichas). ⛔ distribuição do #023 | Nada | Migrar a tabela de níveis para a base; troca de slots (Concentração fixa + 4) |
| 21 | **Nutrição e peso** | 🟡 12 alimentos (EV, peso), norma V1.2 no histórico | Nada | Depois do Galeto individual |
| 22 | **Reprodução / Galeria** | ✅ Etapa 01 (ninhos, Terreiro, ovos, IVs, gêmeos, Herança de Bico). 🟡 Etapas 02/04 recuperadas de contexto. ⛔ 03, 05 e 06; gatilhos dos gêmeos; critérios ambientais | Nada | Blocos (Ninhos, Terreiro), ovo e eclosão, herança |
| 23 | **Mestres Elementais** | ✅ 7 NPCs, IA, treino, Diário, Rumores | Nada | NPCs, estruturas, IA de batalha (depende da Rinha) |
| 24 | **Mundo** | ⛔ biomas e taxas de aparecimento das espécies não foram definidos | Só ovos e `/summon` | Regras de spawn (precisam de decisão) |
| 25 | **Modelos, animações e sons** | 12 modelos (auditorias de 4 a 6 de 10) | `idle` e `walk`; sons de galinha | 11 modelos, animações de ataque, golpe, dano e derrota, sons próprios |

## 3. O que trava a implementação (decisões do criador)

1. **HP efetivo e "Resistência por Vitalidade V5.6.1":** a base registra que o parâmetro está pendente.
   - O dano V5.6 usa o HP máximo do defensor, então o motor precisa de um HP máximo.
   - Proposta até a decisão: HP máximo = progressão do atributo HP (`ceil(HP50×(L+50)/100)`), igual ao que as fichas já usam no nível 100 (`ceil(1,5×HP)`), com fator de Vitalidade 1.
2. **Curva dos níveis 1–49:** sem ela, Galetos abaixo do nível 50 não têm atributos oficiais.
3. **IV, EV e peso nos atributos sob a norma do nível 50:** a fórmula antiga (`nível/100 × (base+IV+0,5√EV)`, IV 1–20) foi superada e a nova não foi escrita.
4. **Efeitos dos golpes em linguagem natural:** estruturá-los é tradução fiel do texto, mas casos ambíguos vão precisar de confirmação.
5. **Spawn no mundo:** onde e com que frequência cada espécie aparece.
6. **Desempate de trocas simultâneas** com Velocidade igual, e se o trio pode repetir espécie.

## 4. Roteiro

| Fase | Entrega | Depende de |
|---|---|---|
| **1. Núcleo de regras** | Biblioteca Java pura (`galetocraft/nucleo`) com dados da base, elementos, progressão, dano V5.6, esquiva, Golpe Duplo, energia, Concentração/Pena, Mira, estados, climas e santuários, captura e XP, com testes contra os exemplos oficiais | Nada |
| **2. Regras de combate na base** | Migrar para `current_rules` as regras oficiais que só existem no histórico (dano V5.6, combate universal, estados, climas, santuários, captura, XP) | Nada |
| **3. Galeto individual no mod** | Espécie, nível, IV, sexo, golpes e dono na entidade; atributos vindos da base; `/galeto info` | Fase 1 (e as decisões 1–3 para números finais) |
| **4. Rinha mínima jogável** | Rinha 1v1 → 3v3 contra Galeto selvagem ou jogador, por comando e tela simples, com o motor do núcleo | Fases 1 e 3 |
| **5. Captura e treinador** | Item Pena, equipe de 5 + reservas, tela do Galetário | Fase 4 |
| **6. Efeitos de golpes e passivas** | Efeitos estruturados por família, ganchos das passivas | Fase 4, decisão 4 |
| **7. XP e aprendizado** | XP por Rinha vencida, golpes por nível, slots | Fase 4, decisão 2 |
| **8. Reprodução e Mestres** | Ninhos, Terreiro, ovos; NPCs Mestres | Fases 4 e 7 |
| **9. Conteúdo** | 11 modelos, animações de combate, sons, spawn | Imagens (ChatGPT) e decisão 5 |

## 5. Progresso

O registro do que já foi feito em cada fase fica em `docs/PROGRESSO_DESENVOLVIMENTO.md`.

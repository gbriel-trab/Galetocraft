# Galetocraft — Base de conhecimento consolidada

> Resumo de referência montado em 18/11/2026 a partir de: base vigente (hoje em `base/vigente/`, revisão 8; até a rev. 2 era o `Galetocraft.sqlite`, SHA-256 `9dd2253d…5aa3c`), Release `acervo-documental-2026-11-17` (inventário de 1.636 arquivos), documentos oficiais dos sistemas e código deste repositório.
> **Este arquivo é um resumo, não uma fonte de verdade.** Em qualquer conflito, vale a camada `current_*` / `v_current_*` do banco vigente.

## 1. O que é o projeto

Galetocraft é um mod de Minecraft de criaturas colecionáveis chamadas **Cocorídeos** (também chamados de **Galetos**), inspiradas em galos e com anatomia própria. O jogador captura, treina, cria e batalha com eles em duelos por turnos chamados **Rinhas**.

Bibliotecas do universo (nomes oficiais; ver `docs/NOMENCLATURA_OFICIAL.md`):
- **Galetário** (antiga RoosterTeca): enciclopédia de espécies (fichas). Inclui o Diário dos Mestres.
- **Galolpédia** (antiga GalolpeTeca): catálogo geral de golpes.
- **Herança de Bico** (antiga GalolpeTeca Hereditária): seção dos golpes hereditários paternos.
- **Galeria**: criação e reprodução. É nome oficial desde 18/11; antes era provisório.
- **Histórico da Rinha** (antigo Diário de Batalha): registro das ações e do resultado de uma Rinha.

Todo design passa por **homologação expressa do criador**. Propostas, Betas, ramos R e ensaios são histórico, mesmo quando o nome do arquivo diz "oficial".

## 2. Fonte de verdade e governança

- **Responsável:** desde 18/11/2026 o **Claude** cuida de todo o projeto, por decisão do criador.
  - O ChatGPT serve só para gerar imagens.
  - O criador continua aprovando tudo que vira oficial.
- **Base única vigente:** fica em `base/` deste repositório. O manual está em `base/LEIA_ME.md`.
  - `base/vigente/*.json`: tabelas `current_*`.
  - `base/artes/`: as 23 artes.
  - `base/fontes/`: documentos-fonte.
  - Dados: 23 espécies, 690 vínculos de golpes, 33 regras, 23 artes, 13 vínculos hereditários, 22 pendências e 14 metadados.
  - Regras incluídas: `nomenclatura`, `dano_v5_6`, `matriz_elemental`, `combate_universal`, `estados_negativos`, `climas`, `santuarios`, `captura`, `experiencia` e `treinador`.
- **Ler somente as tabelas `current_*`** (no SQLite montado, também as views `v_current_*`).
  - O `Galetocraft.sqlite` da revisão 2 no Release (235 tabelas, 67 views) é histórico.
  - A tabela `species` (12 linhas) e as demais tabelas estão marcadas como `HISTORICO_OU_EVIDENCIA`.
  - O comando `montar` junta o histórico com a camada vigente do repositório.
- **Precedência:** decisão expressa mais recente por campo > ficha homologada > cópia histórica. Datas de backup não revogam decisões.
- **`runtime_validado = false`** em tudo. A base é documental: nada nela prova que a regra esteja implementada ou testada no Minecraft.
- **Atualização:** pelo `ferramentas/base/galetobase.py`.
  - `atualizar --pacote` altera registros existentes, no mesmo formato do antigo `Atualizar_Galetocraft.py`.
  - `migrar --pacote` insere registros novos e altera metadados.
  - Todo pacote precisa de `expected_revision`, `reason` e `evidence`, valida a base inteira, incrementa a revisão e grava em `current_journal`.
  - Os pacotes ficam em `docs/patches/`, e cada revisão é um commit.
  - Não criar outra base ativa.
- **Origem da gestão:** até 17/11/2026 o projeto foi conduzido em conversas no ChatGPT, com Library IDs, auditoria horária e backup diário. O Release do GitHub guarda essa fotografia.
- **Histórico de revisões:**
  - rev. 1 (17/11): unificação autorizada.
  - rev. 2 (17/11): `v_current_pares_reproducao` passou a usar `current_galeria`.
  - rev. 3 (18/11): correções de coerência (Concentração V2.3 em todas as espécies, golpes básicos, esquema do #023, pendências resolvidas, decisões do criador) e nomenclatura oficial (Tonto).
  - rev. 4 (18/11): nova governança (base no repositório, sob o Claude), artes #019/#020 em `current_art`, regra `nomenclatura`, R12 e U05 resolvidas.
  - rev. 5 (18/11): regras oficiais de combate, captura, XP e treinador migradas do histórico para `current_rules`; o dano V5.6 entrou na base.
  - rev. 6 (18/11): 32 golpes próprios de #001–#011 completados com a ficha original protegida (categoria, elemento, estado aplicado, efeito estruturado).
  - rev. 8 (18/11): pendências resolvidas com os dados mais recentes do acervo, por instrução do criador. Entraram: curva 1–49, HP nominal e de referência, Vitalidade V5.6.1, IV/EV/peso, regra `aprendizado` (16 espécies), desempate de trocas, trio com espécie repetida, precisão base de 100%, posição da captura, alvo inelegível e alvo válido. As pendências sem dado ficaram registradas (U07–U12).
  - rev. 7 (18/11): regra `captura` coerente. A força da Pena segue a tabela do reforço v1258 (a fórmula `1 + 0,15·(nível−1)` ficou registrada como superada) e a modalidade "mundo" passou a indicar a espera após falha da v1259.

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
- **Herança de Bico — golpes hereditários (13):**
  - #1 Ave Fênix (antiga Tricrina Infernal)
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
  - #007–#015 **não têm golpe hereditário, por design** (decisão do criador de 18/11/2026).
- **Quetzacocó #023:**
  - Lendário Original, com o elemento exclusivo **Nexo** (V2.0).
  - "Lendário Original" é uma **classe própria, fora da escala de raridades**. O total é definido pela ficha (700 no nível 50), por decisão do criador de 18/11/2026.
  - Passiva: na primeira entrada invoca Ventania sem gastar ação nem Energia. Com Ventania ativa, ganha +50 p.p. de Atq. Mágico, e seus golpes de Planta não sofrem a penalidade da Ventania.
  - Golpes próprios: Cataclismo Celeste (Ar), Eclosão das Mil Coroas (Planta, invoca Santuário das Raízes) e Ascensão do Nexo (+50 p.p. de Atq. Mágico e de Velocidade por uso).
  - Não reproduz.
- **Wukocó #024** é apenas proposta.
- **Artes vigentes:** 23 em `current_art`, uma por espécie, guardadas em `base/artes/`.
  - #019 Renacocó ("Renacocó com Face Azul Claro.png") e #020 Frankocó ("Ficha Oficial Frankocó #020.png") entraram na revisão 4.

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
- **Golpes equipados:** 5 por Cocorídeo. Concentração é obrigatória e fixa; os outros 4 são escolhidos.
  - Os 4 slots se liberam quando os 5 golpes de origem estão desbloqueados (Quatro Slots v2). A troca é fora da Rinha (decisão de 18/11).
  - Golpes desequipados continuam aprendidos; nada é equipado sozinho.
- **Aprendizado (regra `aprendizado`, rev. 8):**
  - 15 golpes por nível (os 5 de origem incluídos, nos marcos 1, 1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 44, 47 e 50) e 15 por treinamento com os Mestres.
  - Na captura, todos os golpes por nível até o nível atual já vêm aprendidos.
  - Tabelas de 16 espécies: #001–#012 (grades de 12/11, conciliadas com o repertório vigente), #019, #020, #021 e #022.
  - Sem dado no acervo: #013–#018 (U11) e #023 (U03). Essas espécies ficam só com os 5 golpes de origem.
- **Desempates e trio (rev. 8):** trocas simultâneas com Velocidade igual seguem o sorteio 50/50 oficial; o trio pode repetir espécie (os trios oficiais dos Mestres têm 2 espécies para 3 Galetos).
- **Precisão (rev. 8):** nenhum golpe tem precisão própria em fonte alguma; a precisão original de todos é 100%.
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
- **Regiões e multiplicador da precisão do golpe** (não do dano):

  | Região | Precisão |
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
- **Estados negativos persistentes:** Queimadura, Envenenamento, Afogamento, **Tonto** e Paralisia. A captura também menciona Sono.
  - "Tontura" é o nome antigo. O ID técnico `tontura` continua como alias.

### Fórmula de dano (V5.6, homologada em 13/11/2026; regra `dano_v5_6`)
- `D_base = HPmax_defensor × Poder/400 × (Ataque/max(1, Defesa))^0,7`, contínuo até o fim.
- Arredondamento para cima uma única vez por acerto; acerto válido não anulado causa no mínimo 1.
- **Ordem dos modificadores:** eficácia → bônus de dano (soma dos percentuais) → Guarda, Exposição ou Ruptura (teto ×1,40) → Defesa Especial (−75%) → maior redução da mesma classe.
- **Resistência por Vitalidade V5.6.1** (fórmula homologada em 13/11; HP de referência adotado em 18/11): `Fvit = clamp((HP_ref(L)/HPmax_defensor)^0,2; 0,8; 1,0)` multiplica o dano. Galetos com HP acima da referência do nível recebem até 20% menos dano.
- **HP de referência:** `HP_ref(L) = floor(1,05 × HP_n(L; HP50 = 80))`, ou 10 / 67 / 126 / 157 / 189 nos níveis 1 / 25 / 50 / 75 / 100.
- **Esquiva universal:** `clamp(7,5 + 5·(Vd−Va)/(Vd+Va), 5, 10)%`.

## 6. Progressão, captura, XP e outros sistemas

- **Progressão de atributos (Nível 50 V1):**
  - O nível 50 é a referência.
  - Entre os níveis 50 e 100: `A(L) = A50 × (L+50)/100`. No nível 100, o atributo vale 1,5 × o do nível 50.
  - **Níveis 1–49** (norma R5.4, adotada em 18/11): `A(L) = A50 × (49 + 3(L−1))/196`, de 25% no nível 1 a 98,47% no 49.
  - **HP nominal** (R5.4, adotado em 18/11): 10 no nível 1; `ceil(1,5·HP50)` no 50; `ceil(1,5·HP50·(L+50)/100)` de 50 a 100; interpolação `round_half_up` entre 1 e 49.
  - **IV e EV:** `floor(A_n × (1 + (0,25·IV + 0,5·√EV)/100))`. IV de 1 a 40, EV sem teto.
  - **Peso V1.2:** aplicado por último, sobre HP, defesas e Velocidade (ataques não mudam), com `r = peso/peso natural` de 0,8 a 1,5. O Galeto nasce com r = 1.
  - Exemplo: Taturico nível 50 com IV 20, EV 0 e peso neutro tem HP 134.
  - Pendente: recalibrar as faixas de dificuldade de EV para os totais do nível 50 (U12).
- **Faixas de total no nível 50 por raridade:**

  | Raridade | Faixa | Referência |
  |---|---:|---:|
  | Comum | 350–390 | 370 |
  | Raro | 410–450 | 430 |
  | Épico | 470–510 | 490 |
  | Mítico | 530–570 | 550 |
  | Lendário | 590–630 | 610 |

  "Super Raro" é uma classe histórica e não faz parte da escala atual. "Divino" não tem total homologado.

> Captura, XP e treinador estão em `current_rules` desde a revisão 5 (migrados das Betas 1.2.x). Nutrição e itens continuam só nas tabelas históricas.

- **Captura com a Pena de Captura** (pena com rubi no centro; uma por treinador, não consumível, 5 níveis):
  - No mundo: mirar e usar o botão direito, sem arremesso; 12 blocos em qualquer nível; linha de visão livre; resultado imediato; Feixe do Rubi só no sucesso; na falha o Cocorídeo segue normalmente.
  - Na Rinha contra selvagem: Itens → Pena de Captura, desde a 1ª rodada; consome a ação do treinador; falha não encerra a Rinha e o selvagem age se a ação dele estiver pendente na ordem normal; sucesso encerra na hora.
  - O capturado vai para a equipe principal (até 5) ou para as reservas (sem limite).
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

  - Espera após falha no mundo: 20 s (60 s para Lendário), por Cocorídeo e compartilhada entre jogadores. Na Rinha não há espera.
  - XP da Pena por captura: `XP_base(raridade) + 2·nível_alvo` (Comum 15 … Lendário 135); excedente reaproveitado; sem XP nova no nível 5.
  - Pendentes: como o treinador recebe a Pena, receita, aparência; tentativa contra alvo inelegível; Divino e Lendário Original.
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

- **Galeria** (nome oficial desde 18/11/2026):
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
  - Pares especiais conhecidos: Pirococó+Renacocó e Cocórion+Cocórvolt.
  - Cocórion+Cocórvolt é um **par inativo**, porque as duas espécies são 100% machos. Ele fica registrado até a distribuição de sexo mudar (decisão do criador de 18/11/2026).
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

  - Valem as duplas da afinidade. A lista de 3 parceiros por Mestre da v1.1 é sugestão histórica.
  - As contagens dos documentos de 10/11 ("11/12 espécies", "302 vínculos") também são históricas.
  - Reavaliar os elencos com as espécies novas só com autorização do criador.

- **Sistemas ligados aos Mestres:**
  - IA dos Mestres: demonstra o golpe na primeira oportunidade e depois se adapta taticamente.
  - Diário dos Mestres: 5 telas no Galetário.
  - Rumores e Exploração: aldeões vanilla dão pistas, sem coordenadas.

## 9. Pendências reais (`current_issues` e limites declarados)

- **Arte e modelo (R12):** resolvido na revisão 4.
- **Progressão:** resolvida na revisão 8 (R13). A curva 1–49, o HP nominal e o HP de referência da R5.4 foram adotados por decisão do criador em 18/11.
- **Migração para o mod:** está bloqueada no runtime (R14). O núcleo histórico tem 12 espécies, e 141 quarentenas técnicas foram preservadas.
- **Golpes:** os 660 vínculos aprendíveis são "candidatos técnicos". Os IDs não são entidades executáveis aprovadas (R15).
- **Reprodução:**
  - Faltam os gatilhos completos dos gêmeos especiais e os critérios ambientais da Etapa 02 (R16, U06).
  - A Herança de Bico entre espécies está pendente (U01).
  - As etapas 03, 05 e 06 estão incompletas (U02). A Etapa 07 V1.1 é design aprovado.
- **Quetzacocó:** falta distribuir os 30 golpes por nível e treino (U03).
- **Sem nenhum dado no acervo** (registradas na revisão 8 com status `PENDENTE_SEM_DADO`):
  - U07: aparecimento no mundo (biomas, frequência, nível dos selvagens).
  - U08: como o treinador recebe e recupera a Pena de Captura, e a arte dela.
  - U09: quais 3 dos 5 entram na Rinha, quem começa e como trocar com as reservas.
  - U10: como o Galeto do treinador sai para o mundo e volta.
  - U11: aprendizado de #013–#018.
  - U12: faixas de dificuldade de EV no nível 50 e ganhos de EV em combate e treino.
- **Outros:**
  - Maestria Elemental: texto integral não recuperado (U04).
  - Integração da base com a implementação (U05): resolvida pela governança (base e código no mesmo repositório). Falta só um CI de validação quando o mod passar a ler a base.
- **Fora do `current_issues`:** fórmula de dano definitiva e runtime Fabric/GeckoLib.

### Incoerências: auditoria de 18/11/2026 (todas resolvidas)
O relatório completo está em `docs/AUDITORIA_INCOERENCIAS.md`: 29 conflitos resolvidos na base, nos documentos e no repositório.

- **Correções na base vigente:** estão no pacote `docs/patches/rev3_coerencia_e_nomenclatura.json`, **publicado na revisão 3**.
  - Concentração V2.3 aplicada a todas as espécies.
  - Texto canônico para os golpes básicos.
  - Esquema comum para os golpes do #023.
  - Pendências já resolvidas (R02, R09) marcadas assim nas atas.
  - Decisões do criador registradas em `resolucoes_posteriores`.
- **Rótulo de nível:** a referência é o nível 50. Use `docs/acervo_corrigido/` e veja `docs/ERRATA_NIVEL_50.md`.
- **Plataforma:** **Fabric 1.21.11 + GeckoLib**. As menções a "NeoForge" nas atas estão obsoletas.
- **Arte do Renacocó:** a oficial é "Renacocó com Face Azul Claro.png", como diz a ficha homologada. A citação da Memória Mestra está superada.
- **Faíscocó:** a raridade é Raro. A legenda "Comum" na arte antiga está desatualizada, e a arte não foi alterada.

## 10. Repositório (código e modelos)

### Mod (`galetocraft/`)
- **Plataforma e versões:**
  - Fabric, Minecraft **1.21.11**, Fabric Loader 0.20.1, Fabric API 0.141.6+1.21.11 e GeckoLib 5.4.5.
  - Loom 1.19-SNAPSHOT, mapeamentos oficiais da Mojang.
  - O mod compila para Java 21, mas o Gradle precisa de JDK 25.
- **Identidade:** mod id `galetocraft`, pacote `br.galetocraft`, versão 0.1.0.
- **Build:**
  - `bash gradlew build` gera `build/libs/galetocraft-0.1.0.jar`.
  - Nesta nuvem, o build exige o ambiente "Galetocraft" e o JDK 25 (`apt-get install openjdk-25-jdk-headless`).
  - O build passou em 18/11/2026, e o mod foi testado num servidor dedicado com `bash gradlew runServer --args=nogui`.
- **O que está implementado:**
  - **12 entidades**:
    - O Pirococó tem classe própria, `PirococoEntity`.
    - As outras 11 usam a classe genérica `GaloEntity`: Esporocó, Cocórak, Cocórion, Cocórvolt, Taturico, Axococó, Vagaló, Morcegalo, Espinhocó, Salambrasa e Renacocó.
    - Comportamento: mobs neutros com ataque corpo a corpo e sons de galinha vanilla.
    - Animações GeckoLib só de `idle` e `walk`.
  - **Itens:** 12 ovos geradores.
  - **Renderização:** `GaloRenderer` com LOD por distância (16/32/48 blocos) e uma camada de brilho parcial por glowmask.
  - **Testes de cliente** (source set `gametest`): fotos do Pirococó, galeria e benchmark.
- **Núcleo de regras** (`galetocraft/nucleo`, Java puro, embutido no jar):
  - Implementa o Galetário com os dados da base, eficácia, progressão, dano V5.6, esquiva, Golpe Duplo, Mira, energia/Concentração/Pena, estados, climas e santuários, captura e XP.
  - Inclui um motor de Rinha com IA básica e simulador.
  - Tem 21 testes. O andamento fica em `docs/PROGRESSO_DESENVOLVIMENTO.md`.
- **Comandos no jogo:** `/galetocraft base | ficha <espécie> | rinha <a> <b> [nível] | duelo <a> <b> [rinhas]`.
- **Galeto individual:** cada entidade tem nível (50), sexo e 6 IVs (1–40), salvos com ela. Clicar com a mão vazia mostra a ficha do indivíduo. Os IVs ainda não alteram os atributos.
- **Rinha jogável:** contra Galeto selvagem, com `/galetocraft desafiar` e um menu clicável no chat (Combate, Galetos, Mira, Guarda, Pena de Ritmo, Itens, Fugir). Entram os 3 primeiros da equipe do treinador; sem Galetos, a equipe de teste.
- **XP dos Cocorídeos:** Rinha vencida contra selvagem dá XP aos Galetos do treinador que entraram em campo (regra `experiencia`), com subida de nível pela curva oficial.
- **Captura e treinador:** item Pena de Captura (`/galetocraft pena`), captura no mundo e na Rinha conforme a regra `captura`; equipe principal de 5 e reservas salvas com o jogador (`/galetocraft equipe`).
- **Ainda NÃO existe no mod:**
  - Golpes próprios e dono do Galeto; tela própria da Rinha; Rinha entre jogadores.
  - Galetário no jogo; aprendizado de golpes por nível.
  - Passivas e efeitos especiais dos golpes.
  - Blocos, spawn natural e sons próprios.
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
- **Pirococó:** passou por 3 fichas, com as séries p (ficha da antiga RoosterTeca), q18 (Galetário, armadura prata) e **g09** (Galetário 2, armadura roxa, que é a vigente).
- **`referencias/`:** fichas, artes, vistas e expressões das espécies modeladas, mais especificações em texto do Cocórion e do Renacocó.

### Benchmark e Git LFS
- **`benchmark/`:** CSVs de 9 a 11/11, ainda com um modelo de Pirococó anterior ao g09.
  - 100 Pirococós na máquina atual: cerca de 90 FPS. O modelo antigo dava 35 FPS, então a otimização rendeu cerca de 2,6×.
  - O gargalo é o cliente: o MSPT fica abaixo de 8 ms.
- **Git LFS** cobre `modelos/*/revisao/**` (png, bbmodel, bak) e `benchmark/**/*.png`.
  - Nesta cópia há só ponteiros: 5.783 arquivos, cerca de 2,4 GB não baixados.

### Situação técnica do repositório
- **Licença:** **todos os direitos reservados** (`LICENSE` e `fabric.mod.json`), por decisão do criador de 18/11/2026.
- **Documentação:** o `LEIAME.md` e a descrição do mod foram atualizados (12 espécies e fluxo atual), e os comentários desatualizados foram corrigidos. O `teste.log` é um registro antigo de execução.
- **`lod_log.txt` do Pirococó e do Vagaló:** as contagens são antigas. Regenere com `lod_auto.py` na próxima reexportação, porque o script também muda o `lods.json`.
- **Glowmasks vazias:** Axococó, Cocórion, Espinhocó e Taturico. Por inferência a partir do código, a camada de brilho redesenha o modelo inteiro à toa nesses casos. É um problema de desempenho, e a correção exige mudar o código e testar no jogo.
- **Originalidade:**
  - A pasta `galos_monstro/` (protótipo fora do mod) se declara inspirada em Pokémon. Convém não levá-la para o jogo.
  - A arte oficial do Renacocó cita "Marco" e "Estilo Ikki", personagens de outras franquias. Ela só muda com autorização do criador.

## 11. Acervo do Release `acervo-documental-2026-11-17`

- **Conteúdo:**
  - 1.636 arquivos, 11,4 GB, dos quais 1.182 hashes são únicos.
  - Distribuídos em 15 ZIPs independentes: `00_Base_Vigente` e `01`–`14_Acervo`.
  - Para reconstruir, extrair todos na mesma pasta.
- **Arquivos soltos:** `INVENTARIO_GALETOCRAFT.json` (caminho, tamanho, SHA-256 e pacote de cada arquivo), `DADOS_VIGENTES_CONSULTA.json` (exportação legível da camada atual) e `SHA256SUMS.txt`.
- **Tipos de arquivo:** 472 .md, 366 .json, 247 .png, 197 .sqlite (7,3 GB de Betas e ramos históricos), 191 .zip, 66 .py e 52 .csv. Também há 2 .jar com os motores Java isolados da Mira V1.4 e V1.5.
- **Pastas principais** dentro de `Galetocraft/`:
  - Base_Atual
  - `Galetario` (fichas oficiais por espécie)
  - `GalolpeTecas`: arquivos da Galolpédia, com o nome antigo mantido no caminho
  - `RoosterTeca`: arquivos do Galetário, com o nome antigo mantido no caminho
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
- **Galetário / Galolpédia / Herança de Bico:** espécies, golpes e golpes hereditários.
- **Galeria:** criação e reprodução.
- **Histórico da Rinha:** registro de uma Rinha.
- **Tonto:** estado negativo (antigo "Tontura").
- **Nomes antigos** (RoosterTeca, GalolpeTeca, Tontura, Diário de Batalha, Tricrina Infernal) só aparecem em caminhos, IDs técnicos e citações históricas. Ver `docs/NOMENCLATURA_OFICIAL.md`.

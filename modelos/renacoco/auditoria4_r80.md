# Renacocó #019: auditoria independente da r80

**Data:** 2026-11-15.

**Critério principal:** o checklist de 10 itens de `019_renacoco_refinamento_3.md`.

**Fontes de verdade, nesta ordem:**
1. A arte: `019_renacoco_arte.png`, `_vistas`, `_ficha` (expressão neutra) e `_detalhes`.
2. Os pedidos do dono: especificação, revisão da cauda, refinamento avançado, refinamento 2 e refinamento 3.
3. As regras fixas do dono, que prevalecem sobre a arte: corpo celeste claro, cabeça nem pequena nem calva, crista que não
   pareça cabelo, asas sob o manto, cauda baixa apontando para baixo e manto dominante com a frente aberta.

**Método:**
- Fiz a lista olhando só as imagens: a arte e os renders da r80 e da r77. Nesta rodada não há `r80_comp.png`.
- Só depois abri `renacoco.py` (igual a `r80.py`) e o diff `r77.py → r80.py`, para achar a causa de cada problema no código.
- Gerei vistas extras direto do `r80.bbmodel` e do `r77.bbmodel` com o `previa2`, sem rodar o gerador e sem gravar nada no
  projeto. Ficaram no rascunho da sessão (lista no fim).
- Rodei `verificar_soltos.py renacoco`. O `renacoco.bbmodel` atual é idêntico byte a byte ao `r80.bbmodel`.

**Convenção dos números:**
- unidades do Blockbench, com y para cima;
- frente = −z;
- lado direito do bicho (`_d`) = −x;
- coordenadas no mundo, já com `SOBE_CORPO` e as rotações dos ossos aplicadas.

**Veredito curto:**
- A r80 resolveu a cabeça calva e deu mais presença às asas.
- Para isso, criou 4 problemas novos de leitura:
  - crista em leque radial (coroa de frente e coque de costas);
  - asa lida como saia plissada;
  - juba que engole o pescoço;
  - cabeça em caixa de frente.
- E quebrou 2 coisas que estavam boas na r77: o emblema das costas e a leitura da cauda tripla.
- No saldo, não ficou mais fiel à arte do que a r77.

---

## 1. Checklist do refinamento 3

| # | Pergunta | Resposta | Evidência |
|---|---|---|---|
| 1 | A cabeça deixou de parecer calva? | **Sim** | `r80_crista.png` (lado e 3/4 trás) e `r80_vistas.png` (laterais): a nuca e o alto de trás estão cobertos. Os `rosto0-2` vão até z +2,6, as `nuca0-2` até z +3,0 e as `crista9-12` deitadas até z +5,7. Na r77 era 1 pena de nuca (`nuca0`), e o crânio aparecia liso atrás do olho (`r77_34_perto`). |
| 2 | O topo e a traseira estão mais preenchidos? | **Sim, mas com a leitura errada** | `r80_crista.png` (costas): a traseira virou uma parede chata de 3 placas em escudo, com moldura chanfrada (lê como elmo). Em cima dela há um bolo dourado de pontas (`crista11/12`, rx 110°, vistas de ponta), que lê como coque ou máscara. Detalhe no problema A4. |
| 3 | A crista ficou integrada ao resto da cabeça? | **Em parte** | A touca `crista_base` fecha o vão crânio-crista: nenhum vazio em `r80_34_perto`. Mas crista (amarela) e moldura do rosto (azul) são 2 sistemas separados, um empilhado no outro. A arte alterna plumas amarelas e lâminas azuis numa chama só (`ficha`, Neutra). A r80 tirou a camada amarela da moldura (`rosto2` era `P_CRISTA` na r77 e virou `P_AZUL2`). |
| 4 | A silhueta da cabeça ficou mais rica e majestosa? | **Em parte; de frente, não** | `r80_frente_perto` e `r80_branco` (2ª figura): de frente, a cabeça é um retângulo de laterais retas com um leque radial em cima (coroa). De lado (`r80_crista`, lado), é uma bola de espetos. A crista sobe só 6,1 acima do crânio (1,2× a altura dele); na arte, a crista mede cerca de 2× o crânio. |
| 5 | As asas têm mais destaque sob o manto? | **Sim** | `r80_3-4.png` e `r80_vistas.png` (laterais): as rêmiges vão de y 26 a 12,2 e chegam a x ±9,5. Na r77 iam só até y 16,7 e x ±6,6. |
| 6 | As asas aparecem melhor sem ficar feias ou soltas? | **Não** | Não estão soltas e não passam da silhueta da capa: isso está certo. Mas, em `r80_3-4`, `r80_vistas` (laterais) e `r80_sem_manto`, leem como **saia plissada**: tiras verticais iguais, barra reta e degradê azul→amarelo que passa por um cinza-esverdeado. E cobrem a borda dourada da frente. Detalhe no problema A3. |
| 7 | As pernas ficaram mais bonitas e proporcionadas? | **Em parte** | Faixas de escama a cada 1,2 e nós nos dedos: melhorou (`r80_bainha`, frente; `r80_3-4`). Mas as `calca0-2` (penas da coxa) não aparecem em nenhuma vista, porque ficam sob a "saia". O `tarso_cima` continua uma coluna reta de 3,2 de y 6,8 a 15,5, sem afinar. E a perna nasce de baixo de uma saia, não de uma coxa emplumada. |
| 8 | O corpo continua azul bem clarinho? | **Sim no tronco; em parte na cabeça e nos flancos** | Média da textura: `tronco` (128,196,242), `pescoco` (148–163, 213–225, 248–250) e `nuca` (162,226,250). Mas `rosto2` (109–126, 181–196, 237–243), `asa_sec*` e `peito4-7` em `CELESTE_FORTE` (100,180,245) põem azul médio em área de frente, não só em fresta. Nos renders, as lâminas de trás da cabeça saem (84–109, 125–151, 151–158): azul-aço acinzentado (`r80_rosto`, perfil). |
| 9 | O manto continua dominante e elegante? | **Em parte** | Volume e frente aberta: certo (`r80_vistas`, frente). Mas, nas costas (`r80_vistas` Traseira e `r80_cauda` costas): o emblema ficou partido em 3, sobra 1 dos 3 losangos e o painel de trás ficou chato (`dobra=0.0`) e estreito (±3,8 na barra). Uma barra dourada horizontal atravessa por cima da cauda, como uma verga de porta. A borda dourada da frente sumiu no trecho do peito à cintura. |
| 10 | O modelo ficou mais nobre, bonito e fiel? | **Não, no saldo** | **Ganhos:** cabeça cheia e asa presente. **Perdas:** emblema, cauda, pescoço e moldura amarela do rosto. **Elementos novos longe da arte:** a asa-saia e a crista-coroa. Lado a lado com a arte (`r80_arte_lado`), a r80 não está mais perto que a r77. |

---

## 2. Problemas por gravidade

### ALTA

#### A1. Emblema da fênix partido em 3; 2 dos 3 losangos escondidos (regressão)

**Onde:**
- `r80_vistas.png` (Traseira) e `r80_cauda.png` (costas e 3/4 traseira).
- O corpo da fênix aparece sozinho no painel do meio, com um losango só.
- As asas da fênix aparecem soltas dos lados, separadas por faixas roxas.

**O que a arte mostra** (`_vistas` Traseira e `_detalhes`, "Emblema da Ressurreição"):
- uma fênix dourada inteira de asas abertas em V, ocupando ~60 % da largura das costas;
- abaixo dela, 3 losangos pendentes (moldura de ouro e miolo azul-claro), lado a lado.

**Causa:**
- A pintura está certa: isolado, o `manto_costas_p` mostra a fênix inteira e os 3 losangos, até maiores que na r77.
- Quem cobre é o painel lateral de trás, `PAINEIS[2] = (54, (10.6, 16.4), 8.0, 12.4, 1.2)`. Na r77 eram 2 painéis:
  `(40, …, 7.0, 10.4, 4.0)` e `(70, …, 5.6, 7.0, 7.5)`.
- Em |x| ≈ 3, o lado chega a z 10,2 (y 20–25), 12,7 (y 15–20) e 16,0 (y 10–15).
- O painel das costas fica em z 9,6, 12,0 e 14,9 nessas faixas: 0,6 a 1,0 **à frente** do lado.
- Na r77, o painel das costas ficava 1,5 a 3,6 **atrás** dos laterais em toda a altura.
- O `manto_costas_p` ficou mais longo (`fim` de 11,0 para `ARCO_Y` 6,0), com o alvo quase igual (z 16,0 → 16,6). Por isso ele
  inclina menos para trás e foi "engolido".

**Correção** (escolha uma das duas, e confira na vista de costas):
1. **Preferível.** Estreite e gire o painel lateral de trás para ele não passar de |x| = 5,5 na faixa y 12–25, onde estão a
   fênix (asas até |a| = 5,3) e os losangos (até |a| = 4,15). Valor de partida: `PAINEIS[2] = (44, (11.4, 15.6), 7.0,
   10.0, 1.2)`. Meça: o menor |x| do `manto2_*` com z > 6, na faixa y 12–25, tem de ficar ≥ 5,5.
2. Ou ponha o painel das costas por cima de tudo: em `manto_ossos()`, raiz `rz + 0.8` → `rz + 2.0` e alvo `(0.0, 16.6)` →
   `(0.0, 18.6)`. O painel das costas tem de ficar ≥ 1,0 atrás dos laterais para |x| ≤ 5,5.

**Critério de aceite:** em `_vistas` Traseira, a fênix aparece com as 2 asas ligadas ao corpo e os 3 losangos visíveis,
como na `r77_vistas` Traseira.

#### A2. Cauda tripla quase invisível; a verga dourada lê como porta (regressão)

**Onde:**
- `r80_vistas.png` (laterais) e `r80_bainha.png` (lado e 3/4 traseira): a cauda não aparece de frente, de lado nem de 3/4.
  Só sobram pontas amarelas rentes ao chão, saindo da barra.
- `r80_cauda.png` (costas): só aparecem 2 tufos amarelos nos cantos de uma "janela" e uma barra dourada horizontal por cima.
- 3/4 traseira: uma corrente sai **deitada no chão** pela esquerda da barra. Lê como coisa arrastando, não como cauda
  descendo.

**O que a arte e o dono pedem:**
- 3 correntes de contas douradas com miolo azul-claro e leques amarelos e azuis: é a marca da espécie ("Cauda Tripla da
  Fênix").
- O dono definiu: saem por baixo da capa, com origem baixa, apontando para baixo.
- E pediu (revisão da cauda): "a parte traseira inferior deixa ler a origem da cauda" e as "3 ramificações legíveis".
- A r77 mostrava as 3 de costas (`r77_vistas` Traseira).

**Causa:**
- A r80 baixou todos os painéis laterais até o chão (`fim` 1,2 nos 3). Antes eram 4 / 7,5 / 11, no "arco de 3 degraus".
- A r80 também baixou o painel das costas de 11,0 para 6,0 (`ARCO_Y`).
- Os leques ficam em y 3,3–10,1 e z 11,3–19,5. A barra de trás fica em y 6,1–8,3 e z 14,6–17,0. Metade dos leques fica atrás
  dela.
- Os leques de fora (x ±3 a ±7) ficam dentro do `manto2`, que na barra chega a |x| = 2,74.
- Resultado: 86 cubos (19 % do modelo) para um elemento que quase não aparece.

**Correção:**
1. Volte o arco: `ARCO_Y = 6.0` → `10.5`, e os painéis laterais de trás com a barra subindo em degraus. Ou volte o par da r77,
   `(40, (11.8, 15.4), 7.0, 10.4, 4.0)` e `(70, (8.2, 17.0), 5.6, 7.0, 7.5)`, ou, mantendo 3 painéis, dê `fim` 4,0 ao
   `PAINEIS[2]` com `arco` 3,5.
2. Abra mais as correntes de fora para saírem entre o painel das costas e os laterais: em `CORRENTES`, `ry` ±6 → ±12, e em
   `corrente(..., abre_leque=...)`, ±6 → ±14.
3. Mantenha os ângulos de queda da r80 (60/56), que já apontam para baixo.

**Critério de aceite:**
- de costas, as 3 correntes, cada uma com ≥ 3 contas visíveis;
- na 3/4 traseira, ≥ 2 correntes descendo na diagonal, e nenhuma deitada no chão;
- nenhuma barra horizontal cruzando a abertura.

#### A3. Asa lida como saia plissada, cobrindo a borda dourada

**Onde:**
- `r80_3-4.png` e `r80_vistas.png` (laterais): massa amarela-creme em volta do quadril.
- `r80_sem_manto.png`: a asa inteira é uma cortina de tiras verticais de 1,7 de largura e mesmo comprimento (14,6), com as
  pontas todas na mesma altura (y ≈ 12,2). Isso forma uma barra reta, como a de uma saia.
- O degradê `P_ASA_PRIM` vai de (120,195,248) a (245,205,90) em 13 % do comprimento e passa por (168,199,187): uma faixa
  cinza-esverdeada larga, visível no meio de cada pena. A média de cor das `asa_rem*` na textura é (172,196,176).
- As rêmiges da frente (`phi` −46 e −35) vão até z −7,8, a altura do peito. Ficam por cima da borda dourada do painel da
  frente, no trecho ao lado do peito e da cintura (compare `frente_r80` com `frente_sem_asa`).

**O que a arte mostra** (`_arte` e `_detalhes`, "Asas Visíveis (Sob o Manto)"):
- camadas em telha bem separadas: coberteiras celeste em cima, uma fileira azul e embaixo penas longas amarelas e creme;
- penas pontudas e escalonadas, as de trás mais longas, as pontas apontando para baixo e para trás;
- a troca de cor acontece **de uma fileira para a outra**, não dentro da pena;
- a asa fica entre o corpo e a borda dourada, e a borda continua contínua do medalhão à barra.

**Correção** (em `asa_ossos`):
1. **Rêmiges:** de 6 penas iguais para 5 penas graduadas.
   - `phi` de `(-46,-35,-24,-13,-2,9)` para `(-28,-17,-6,5,16)`;
   - `L = (9.5, 11.0, 12.5, 13.5, 14.0)`, da frente para trás;
   - `W` 1,7 → 2,2; `flare` 16 → 10;
   - `varre=14`, com as pontas para trás;
   - x da raiz alternando ±0,35 conforme `k % 2`, para quebrar o plissado.
2. **`P_ASA_PRIM` sem azul:** `[(0, AMAR), (0.55, (253,228,130)), (1, CREME)]`. O azul vem por cima, pelas `asa_sec`:
   alongue de 9,0 para 10,5 para elas cobrirem os 40 % de cima das rêmiges. A transição passa a ser por camada.
3. **Critério de aceite:**
   - de lado, a borda de baixo da asa é uma diagonal (curta na frente, longa atrás), não uma barra horizontal;
   - nenhum texel da família #A8C7BB (cinza-esverdeado) na textura da asa;
   - de frente, a borda dourada aparece inteira por fora da asa.

#### A4. Crista em leque radial: coroa de frente, espanador de lado, coque de costas; e baixa demais

**Onde:**
- `r80_frente_perto.png`: 9 espetos abertos em semicírculo, simétricos, mais largos que a cabeça no topo (≈ 230 px contra
  200 px). Lê como coroa raiada, e a especificação proíbe "coroa genérica".
- `r80_crista.png`, lado: as 17 plumas saem de um ponto e apontam para cima, para cima e para a frente, para trás e para trás
  e para baixo, cruzando-se. Lê como espanador ou cabelo espetado.
- `r80_crista.png`, costas: as `crista11/12` (rx 110°, ry ±26°) aparecem de ponta e formam um bolo dourado na nuca, que lê
  como coque.
- **Altura:** o topo da crista fica em y 45,5, contra 45,8 na r77, a 6,1 acima do crânio (y 39,4): ~1,2× a altura do crânio
  (5,1).

**O que a arte mostra** (`ficha`, Neutra; `_arte`; `_vistas` Frente e Lateral):
- uma chama só, alta: ~2× a altura do crânio;
- de frente, contorno em gota que **fecha** no topo: o centro é o mais alto e os lados curvam para dentro e para cima;
- de lado, as plumas de baixo saem quase na horizontal para trás, passando ~3 do crânio, e as de cima sobem;
- todas as pontas vão para cima e para trás; nenhuma vai para a frente nem para baixo;
- base azul-clara entre as plumas amarelas.

**Correção** (em `CRISTA` e `pluma()`):
1. Reduza para 11 plumas:
   - `crista0` (centro): `L` 6,0 → 9,0;
   - degrau 2: `L` 6,6 → 8,5;
   - degrau 3: `L` 7,0 → 8,0, com `rx` 55 → 50;
   - par da frente: `rz` ±24 → ±12;
   - línguas de fora: `(±2.2, 34.8, -1.2, 4.8, (44,0,±42))` → `(±1.9, 34.9, -1.6, 5.5, (40,0,±18))`.
2. **Apague** o degrau 5 `(±1.4, 34.6, 1.2, 6.4, (110,±26,0))`, que faz o coque. No lugar, ponha 1 par varrendo reto para trás:
   `(±0.7, 34.8, 1.0, 8.0, (88,±8,0), 2.4, "am")`.
3. Em `pluma()`, inverta a curva da metade de cima: `curva = -6 if rz > 0 else 6`. Hoje a ponta abre mais 10° para fora, e
   isso faz a coroa; o certo é fechar a chama.
4. **Alvo:**
   - topo da crista em y ≈ 48,5 (+9 acima do crânio);
   - de frente, a largura no topo fica ≤ 60 % da largura do crânio;
   - de costas, nada de ponta dourada vista de frente na nuca.

### MÉDIA

#### M1. De frente, a cabeça é uma caixa ou elmo; a moldura amarela do rosto sumiu (regressão parcial)

**Onde:**
- `r80_frente_perto.png` e `r80_vistas` Frente: as laterais da cabeça são retas, do supercílio até a mandíbula.
- A touca `crista_base` deixa uma aba horizontal no alto da testa, que lê como capacete.
- As `rosto*` ficaram coladas ao crânio: `ry` 6, alcance x ±4,1. Na r77 eram `ry` 18 e ±5,5.
- As 2 placas de bochecha embaixo parecem protetores de orelha.
- Compare no `cab_frente_cmp`: a r77 abria a silhueta na altura dos olhos.

**O que a arte mostra** (`_vistas` Frente e a especificação):
- "penas do rosto: laterais azuis e amarelas formando uma moldura nobre";
- de frente, lâminas azuis abrem para os lados na altura do olho, com o amarelo da crista emendando em cima;
- a cabeça afina para o bico.

**Correção** (em `cabeca_ossos`):
- `rosto1` e `rosto2`: `ry` 6 → 16.
- `rosto2`: `P_AZUL2` → `P_CRISTA`, a camada amarela de cima da moldura, como na r77.
- Lâminas com `h` 2,6 → 1,8 e ponta em losango (como a `_pt` de `pena`), para lerem como pena e não como telha quadrada.
- Na `crista_base`, recolha o x de `±(LX-0.4)` para `±(LX-1.2)`: assim a aba não aparece de frente.

#### M2. A juba de telhas desce sobre o pescoço; o pescoço encurta e engrossa (regressão)

**Onde:** `r80_34_perto` contra `r77_34_perto`, `r80_vistas` (laterais) e `cab_lado_cmp`.
- `rosto0` desce até y 30,9 (na r77, 34,5). As `nuca*` descem até 32,4 (na r77, 34,7). A gola (`capuz` e `capelete_a`)
  termina em 31,9 e 30,2.
- Sobra de 0,7 a 1,5 de pescoço visível de lado. Na r77 eram ~4.
- As 3 `nuca*` são placas largas (W 3,6 e 3,2) com ponta em V e moldura escura. De costas, formam um escudo de armadura
  (`r80_crista`, costas).

**O que a arte e o dono pedem:**
- "pescoço longo e elegante" e "evitar pescoço grosso" (especificação e revisão da cauda);
- na arte, o pescoço azul aparece entre a cabeça e a gola roxa;
- as lâminas do rosto varrem para trás, quase na horizontal, e não descem.

**Correção:**
- `rosto0`: `rx` 34 → 14 e `L` 6,4 → 5,0, para o ponto mais baixo ficar ≥ 33,5.
- `nuca`: troque as 3 placas por 5 penas:
  - `W` 2,2;
  - `L` (5,0, 4,4, 4,4, 3,8, 3,8);
  - x (0, ±1,3, ±2,5);
  - `flare` 12;
  - ponto mais baixo ≥ 33,5.
- **Alvo:** ≥ 2,5 de pescoço visível de lado, entre a juba e o `capuz`.

#### M3. Borda dourada da frente: some do medalhão à cintura e fina demais (piorou na r80)

**Onde:**
- `r80_3-4`, `r80_vistas` (frente e laterais) e `peito_cmp`.
- Na r77, um filete dourado aparecia ao lado do peito; na r80 ele virou pena azul-clara (`asa_cob/sec`).
- Do medalhão até ~y 22, a beirada da frente é roxa nas duas rodadas.
- A faixa pintada tem `FAIXA = 1.1`.

**O que a arte mostra** (`_arte` e `_vistas` Frente e Lateral):
- uma faixa dourada **larga e contínua** que sai do medalhão e desce na diagonal até a ponta da barra;
- é a linha mais forte da frente do manto.

**Correção:**
- `FAIXA` 1,1 → 1,8.
- Em `mat_capelete`, pinte de `OURO` a beirada da frente do `capelete_b` (z < −3,6 e |x| > 5) para ligar o medalhão à faixa do
  painel.
- As rêmiges saem de cima da faixa (A3).

#### M4. O símbolo do peito continua uma placa colada, com 2 pinos brancos (velho, não resolvido)

**Onde:**
- `r80_frente_perto` e `peito_pinos`: a `peitilho_a` é um retângulo branco-azulado de 4,4 × 4,0, com cantos vivos e sem
  nenhuma textura de pena (`mat_peitilho` só faz degradê).
- As 3 fileiras de `pena_lisa` em V ficam quase todas atrás das lâminas `peito*`. O V da arte não aparece.
- As pontas de fora da 1ª fileira (`peitilho0_0` e `peitilho0_3`, x ±2,4) aparecem como 2 pinos brancos verticais acima das
  lâminas azuis.
- As lâminas `peito*` (2,2 a 3,0 de largura, moldura escura e ponta em losango) leem como placas de armadura (tassets).

**O que a arte mostra** (`_detalhes`, "Símbolo do Renascimento"):
- a cruz sobre um peitilho **de penas**, com a borda de baixo serrilhada em V;
- abaixo, penas pequenas em várias fileiras.

**Correção:**
- Pinte escamas em `mat_peitilho` (`escama(x, y, 1.9, 1.5)` misturando 12 % de `AZUL`, como já faz `mat_escudo`).
- Faça a `peitilho_a` afinar embaixo: troque o retângulo por `a` de 4,4 (y 23,0–25,6) mais `b` de 3,0 (y 21,8–23,0).
- Faça as `colar0` sobreporem 0,5 a borda de cima da placa.
- Abaixe 0,4 os `peitilho0_0/0_3`, ou pinte a face `up` deles em `PEITILHO` em vez de `PEITILHO_CL`.
- Nas `peito*`, troque `W` 2,2–3,0 por 1,8 e tire o escurecimento da borda (`na_borda`) da face larga.

#### M5. Forro roxo preso ao corpo e atravessado pelas pernas ao andar

**Onde:**
- `r80_sem_manto.png`: sem o manto, sobra uma placa roxa entre as pernas (`forro`, osso `corpo`, x ±2,4, y 3,0–16,1, z
  1,2–2,2).
- Com a perna a −18° (passo para trás do `ANIM_ANDANDO`), `tarso_baixo_e` vai a x 2,0–4,4 e z 1,3–5,1. Isso atravessa o forro
  em x 2,0–2,4 a cada passo.

**O que o dono pede:** "manto separado da anatomia" (refinamento avançado, Técnico).

**Correção:**
- Mova o `forro` para o osso `manto_costas`.
- Estreite para x ±1,3, assim nenhuma perna o toca em ±18°.

#### M6. Flancos e trás da cabeça em azul médio ou acinzentado

**Onde:**
- `r80_vistas` Frente: `peito0/1/4-7` (`P_PEITO_FORTE`) e `asa_sec*` (`CELESTE_FORTE` 100,180,245) formam uma área frontal
  grande de azul médio.
- `r80_rosto` (perfil): as lâminas de trás da cabeça renderizam (84–109, 125–151, 151–158). O `rosto2` começa em
  `CELESTE_SOMBRA`, e as faces laterais levam a sombra de 0,6 do jogo.

**O que pede a regra do dono:** celeste claro predominante, com azul médio só em fresta.

**Correção:**
- `P_PEITO_FORTE` → `P_PEITO_CLARO` nas `peito4-7`. O `CELESTE_FORTE` fica só nas `peito0/1`, que entram por baixo da capa.
- `rosto2` vira amarelo (M1).
- Nas lâminas da cabeça, comece o degradê em `CELESTE` (150,215,250), nunca em `CELESTE_SOMBRA`.

#### M7. Pernas: coxa sem leitura e tarso sem refinamento

**Onde:** `r80_3-4`, `r80_vistas` Frente e `r80_bainha` Frente.
- As `calca0-2` (y ≈ 18,1, `L` 4,6) ficam dentro da saia das asas e não aparecem.
- O `tarso_cima` é um prisma de 3,2 de y 6,8 a 15,5, sem afinar.
- O tornozelo é um anel achatado.

**O que a arte mostra:**
- as penas da coxa (azul e creme) caem sobre o alto da canela;
- a canela afina para baixo;
- a junta tem volume.

**Correção:**
- `calca`: raiz 14,6+S → 13,4+S e `L` 4,6 → 5,4. Aparecem quando as rêmiges forem encurtadas na frente (A3).
- Divida o `tarso_cima` em 2 octógonos: 3,4 de largura em y 12–15,5 e 2,8 em y 6,8–12.
- `tornozelo`: 3,3 → 3,0 de largura, com 1 linha de `AMAR_ESC` no meio.

### BAIXA

- **B1. Medalhões com o símbolo "⊘".** O miolo é dividido na diagonal (`OURO_CL` contra `OURO`) e cercado por um anel escuro.
  De longe, lê como o sinal de "proibido". A arte mostra um octógono com domo central claro. Em `mat_medalhao`: miolo
  `r < 0.5` em `OURO_CL` uniforme, com 1 texel de brilho no alto à esquerda, e anel `r 0.5–0.62` em `OURO`, não `OURO_ESC`.
- **B2. Medalhão espetado de perfil.** O medalhão vai a z −8,9; a frente do peito está em −7,7. Em `r80_vistas`
  (laterais), aparece como um palito dourado à frente do peito. Use `mz` −8,1 → −7,6 e o domo em 0,3 em vez de 0,4.
- **B3. Painel das costas virou chapa reta.** `manto_costas_p` com `dobra=0.0`, enquanto a especificação diz "nada de chapa
  reta". Volte `dobra` para 0,5, mantendo o emblema na metade de cima, que não dobra.
- **B4. Gradientes que passam por verde-claro.** `P_CRISTA` (`CIANO` → (251,217,102) em 20 %) dá (213,226,178) na base das
  plumas. Use uma parada intermediária branca: `(0.1, (235,245,250))`.
- **B5. Esclera cinza de lado.** O branco do olho (244/226) sai (151,151,151) nas faces laterais do render. Na arte é branco
  puro. Use `BRANCO` (250,250,252) e marque a esclera no `brilho`, que ilumina no jogo.
- **B6. Bico um pouco estreito de frente.** Depois das escalas, o `bico_tampa` tem ~2,3 de largura numa cabeça de 7,4
  (31 %). Na arte, a base do bico ocupa 35–40 % da largura. Use `bico_tampa` x ±1,0 → ±1,2 e `bico_quilha` 1,1 → 1,3.
- **B7. Cauda arrastando.** Os leques chegam a y 3,3; no `ANIM_PARADO` (±4° e ±6°), as pontas encostam na barra lateral
  (`manto2`, y 1,4–10,4). Depois de A2, confira com o leque girado.
- **B8. Barra de baixo do manto mais estreita que a arte.** De frente, a largura total é ~0,70 da altura; na arte, ~0,9, com
  as pontas da barra abrindo para fora. É um ponto antigo, mas pesa no "manto dominante". Use `PAINEIS[1]` alvo x 14,0 →
  15,5.

---

## 3. Regressões em relação à r77

| Item | r77 | r80 | Causa no código | Como desfazer |
|---|---|---|---|---|
| **Emblema dourado das costas** | Fênix inteira de asas abertas e 3 losangos legíveis (`r77_vistas` Traseira) | Corpo da fênix sozinho no painel do meio; asas separadas por faixas roxas; 1 losango só | `PAINEIS` de 4 para 3 painéis, com `PAINEIS[2]` (54°, 8,0→12,4) passando 0,6–1,0 por fora do `manto_costas_p`; painel das costas mais longo (`fim` 11 → 6) e menos inclinado | A1 |
| **Bordas douradas** | Filete dourado ao lado do peito e da cintura (`r77_frente_perto` e `peito_cmp`); arco dourado em degraus em volta da saída da cauda (2 painéis com `arco` 3,5) | Filete coberto pelas `asa_rem0/1` e `asa_cob/sec`; arco só no `manto2` (1 tira de 4,8); de costas, a barra do `manto_costas_p` cruza a abertura como uma verga | Novas `asa_ossos` (`phi` −46 a 9) e `PAINEIS` sem degraus | A2, A3 e M3 |
| **Peito com a cruz** | Cruz latina azul-marinho em placa clara | **Igual.** `cruz_latina`, `mat_peitilho` e posições sem mudança; os pinos brancos já existiam | Nenhuma | O problema é velho (M4), não regressão |
| **Medalhões** | Octógono dourado com "⊘" | **Igual** (mesmo `mat_medalhao` e posições) | Nenhuma | B1, problema velho |
| **Cauda tripla** | 3 ramos legíveis de costas, saindo pelo arco de 11 | Só 2 tufos e a barra; nada de lado nem de 3/4 | `ARCO_Y` 6,0 e laterais até o chão | A2 |
| **Pescoço** | ~4 de pescoço visível de lado e de 3/4 | 0,7–1,5 | `rosto0` (`rx` 34, `L` 6,4) e `nuca0-2` descendo até 30,9 e 32,4 | M2 |
| **Moldura do rosto** | Azul e amarela, abrindo a ±5,5 | Só azul, colada a ±4,1: cabeça em caixa de frente | `rosto2` `P_CRISTA` → `P_AZUL2`; `ry` 18 → 6 | M1 |
| **Crista de frente** | 3 espetos altos com pontas laterais (chama rala) | Leque radial de 9 (coroa) | Nova tabela `CRISTA` e `_c` curvando para fora | A4 |

**Melhorou:**
- cabeça sem calvície;
- presença das asas;
- escamas da perna e nós dos dedos;
- pescoço e coxa em celeste;
- a pintura do emblema ficou maior e mais nítida no próprio painel. Basta destampá-la.

---

## 4. Pontos técnicos

### Peças soltas

`verificar_soltos.py renacoco` dá 1 componente em todos os níveis:

| LOD | Cubos | Componentes |
|---|---|---|
| 0 | 451 | 1 |
| 1 | 340 | 1 |
| 2 | 300 | 1 |
| 3 | 284 | 1 |

O teste une caixas com folga de 0,15 e não pega peça que só parece solta. O caso visível é o medalhão de perfil (B2).

### Cubos degenerados

`crista_base_a` e `crista_base_b` têm **altura negativa (−0,102)**:
- O `arredondado2("crista_base", …, y 33.4→35.7, r=1.2)` encolhe `r` de cada lado numa altura de 2,3.
- A textura só gerou as faces `up` e `down`: cubo invertido.
- O Blockbench aceita, mas no GeckoLib o cubo pode sair do avesso.
- **Correção:** use `r=1.0`, ou suba o topo para 36,2.

### Contagem

| | r80 | r77 |
|---|---|---|
| Cubos | 451 | 417 |
| Ossos | 288 | 243 |
| Textura | 512 × 512 | |

**Cubos por grupo:** cauda 86, manto 66, asas 60, crista 55 (era 25 na r77), peitilho 21, rosto 18, peito 16, colar 14,
capelete 12, calça 12.

- **A cauda custa 19 % do modelo** e quase não aparece (A2).
- **O LOD 3 ainda tem 284 cubos** (63 % do LOD 0). Reduza:
  - a crista para 5 plumas;
  - cada corrente para 3 contas e 1 leque de 2 penas;
  - as asas para 3 penas por lado;
  - o rosto para 1 lâmina por lado.
- **Ossos demais para o GeckoLib:**
  - cada `pena()` cria 2 ossos (`nome` e `nome_p`), cada `pluma()` 2 e cada `lamina()` 3;
  - as penas que não animam são estáticas (`peito*`, `colar*`, `calca*`, `nuca*`, `rosto*` e plumas da crista). Junte as
    rotações de cada uma num osso só (ou na rotação do cubo, que o formato Bedrock aceita). Isso tira 50 a 60 ossos; com as
    penas dos leques e das asas, chega perto de 200;
  - agrupe as `peito0-7`, hoje soltas sob `corpo`, num osso `peito`, como pede a especificação ("Peito: penas do peito e
    símbolo").

### Nomes de ossos

- Os 288 nomes são únicos, em português, com `_d` e `_e` consistentes.
- Há osso e cubo com o mesmo nome (ex.: `asa_rem0_d`, `cauda1_0`, `sobrancelha_d`). É válido, mas confunde no Blockbench.
  Use o sufixo `_g` nos grupos de `pena()`.
- A especificação sugeria `tail_root/tail_1-3`. O projeto usa `cauda`, `cauda1/2/3_k` e `cauda*_leque`: é coerente com o
  resto e fica.

### Pivôs para animar

| Osso | Origem (mundo) | Rotação de repouso | Avaliação |
|---|---|---|---|
| `cabeca` | (0, 35,63, −2,39) | (10, 0, 0) | 1,4 acima da base do crânio (34,3), no meio da profundidade. Bom para olhar. **Colisão:** com +25° (olhar para baixo, pose de cura), as `nuca*` descem a y 30,2 e entram no `capuz` (28,5–31,9), e `rosto0` desce a 29,7 e entra no `capelete_a` (topo 30,2). Corrigido por M2. |
| `pescoco` / `pescoco_alto` | (0, 28,5, −1) / (0, 31,5, −1) | −10 / −10 | A soma é −20°, compensada pela cabeça a +10. Quem anima precisa saber que o repouso não é zero. |
| `crista` | (0, 40,93, −1,98) | 0 | No topo do crânio: bom para balanço. |
| `asa_d` / `asa_e` | (∓5, 28,0, −1) | 0 | No ombro, sob o capelete: bom. Mas é 1 osso só por asa, sem dobra. Abrir a asa na pose "poder" gira a cortina inteira em leque. Para abrir de verdade, crie `asa_*_mao` com as rêmiges, pivô em (∓7, 21, −1). |
| `manto_d` / `manto_e` | (∓4,5, 27,7, 0) | 0 | Cada painel (`manto0-2_*`) tem pivô próprio no anel do ombro e 2 sub-ossos de degrau (`_d1`, `_d2`). Bom para o balanço. |
| `manto_costas` | (0, 27,7, 4,4) | 0 | Bom. Depois de A1, confira que o balanço ±2° do `ANIM_PARADO` não deixa o lateral passar por cima de novo. |
| `gola` | (0, 29,5, 0) | 0 | Capelete, medalhões e capuz juntos: bom. |
| `cauda` | (0, 16,1, 4,6) | 0 | Baixa, no uropígio: bom. 1 osso por conta e `_leque` no fim: bom para onda. |
| `perna_*` / `tarso_*` / `pata_*` | quadril y 17,5, tornozelo 6,7, pé 1,8 | 0 | Bons. **Colisão** com o `forro` no passo para trás (M5). |

### Comentários desatualizados no gerador (enganam a próxima rodada)

| Linha | O comentário diz | O código faz |
|---|---|---|
| 649–651 | "atrás a barra sobe num arco de 3 degraus (4 / 7,5 / 11)" | Todos os `PAINEIS` vão a 1,2 |
| 667 | `manto_ossos`: "4 painéis largos por lado" | São 3 |
| 630 | "segmentos curtos (<= 3)" | O código divide por 4,4 |
| 834–835 | "arcos que sobem e descem … abrem para o lado +x" | A cauda desce |
| 950 | `K_CAB`: "cabeça 20% menor" | `K_CAB` = 1,02 |
| 729 | `asa_ossos`: "até ~a altura do joelho" | Termina em y 12,2, no meio da coxa |

---

## Vistas extras usadas

Feitas a partir do `r80.bbmodel` e do `r77.bbmodel`, fora do projeto. Pasta do rascunho:
`C:\Users\gbriel\AppData\Local\Temp\claude\bb3a2019feb546b6\821776f3-41b0-4be8-aee3-ed059f5bfdbf\scratchpad\`

| Arquivo | O que mostra |
|---|---|
| `painel_costas_cmp.png` | Painel das costas isolado (r77, r80) e r80 sem os laterais: prova A1 |
| `frente_asa_cmp.png` | r80, r80 sem asas e 3/4 sem asas: prova A3 e M3 |
| `costas_r77_r80.png`, `frente_r77_r80.png`, `lado_r77_r80.png` | Recortes ampliados das vistas |
| `cab_lado_cmp.png`, `cab_frente_cmp.png`, `cab_tras34_cmp.png`, `cab_cima_cmp.png` | Só a cabeça, r77 contra r80 |
| `tras_baixo_cmp.png`, `cauda_lado_sem_manto_cmp.png` | Cauda |
| `peito_pinos.png`, `peito_cmp.png` | Peito e pinos brancos |
| `asa_zoom.png`, `asa_semmanto_zoom.png` | Saia plissada e faixa cinza-esverdeada |

---

## Resumo: as 5 correções mais importantes

1. **Destampar o emblema das costas (A1).** Use `PAINEIS[2]` → `(44, (11.4, 15.6), 7.0, 10.0, 1.2)`, ou empurre o
   `manto_costas_p` 2 para trás. A fênix inteira e os 3 losangos têm de aparecer como na r77.
2. **Devolver a leitura da cauda tripla (A2).** Use `ARCO_Y` 6 → 10,5, a barra lateral de trás em degraus (4 / 7,5) e as
   correntes de fora com `ry` ±12 e `abre_leque` ±14. O alvo são 3 correntes com ≥ 3 contas visíveis de costas, sem verga
   dourada cruzando.
3. **Trocar a saia pela asa em camadas (A3).** São 5 rêmiges graduadas (9,5 → 14) varrendo 14° para trás, `P_ASA_PRIM` sem
   azul (a troca de cor é por camada) e as rêmiges de −46° e −35° fora de cima da borda dourada.
4. **Refazer a crista como chama única e alta (A4).** São 11 plumas, o centro com `L` 9, laterais com `rz` ≤ 18, sem o degrau
   de 110° (o coque) e a curva do `_c` fechando para dentro. O topo fica em y ≈ 48,5.
5. **Abrir a moldura do rosto e liberar o pescoço (M1 e M2).** Use `rosto1/2` com `ry` 16, `rosto2` amarelo, `rosto0` com `rx`
   14 e `L` 5, e 5 penas de nuca estreitas acima de y 33,5. Isso desfaz a cabeça em caixa e a juba sobre o pescoço, e evita
   a colisão com o capuz ao baixar a cabeça.

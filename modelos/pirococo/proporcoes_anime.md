# Pirococó #001: planejamento de proporções (ficha anime "Galetário")

- **Ficha base:** `modelos/referencias/001_pirococo_anime_ficha.png` (recebida em 18/11/2026; ilustração 2D estilo anime/Pokémon).
- **Planta conferida sobre a ficha:** `modelos/pirococo/proporcoes_anime_planta.png`, gerada por
  `python ferramentas/planta_proporcoes.py pirococo_anime`. As caixas coloridas são os volumes planejados
  e ficam por cima das vistas de frente e de lado da ficha.
- **Convenções** (as mesmas do `galo_base.py`):
  - 16 u = 1 bloco;
  - y sobe a partir do chão;
  - x = 0 no meio do corpo, e x negativo é o lado DIREITO da criatura (`_d`);
  - z = 0 no pivô do quadril, e a FRENTE (o bico) fica em z negativo.
- **Como medi:** recortei as 4 vistas ortográficas, tirei o fundo branco e medi a silhueta linha a linha. Depois
  classifiquei as cores (creme, prata, roxo, dourado, vermelho) ao longo das linhas de centro, para achar os
  marcos. A vista de frente tem 276 px do chão à crista (6,13 px/u) e a lateral tem 273 px (6,07 px/u).
  A margem de erro do desenho é de cerca de ±0,5 u.

Esta ficha muda a direção visual do Pirococó. O modelo atual (g09, da ficha voxel) serve como técnica, mas não
como base de proporção.

---

## 1. Escala no jogo

| fonte | o que mede | resultado |
|---|---|---|
| texto da ficha | "Altura aprox. 2,5–3,0 blocos" | faixa |
| quadro "Silhueta e Proporção" | personagem padrão 138 px; seta 202 px (até o topo da cabeça); galo inteiro 223 px | topo da cabeça ≈ 2,6–2,7 blocos; ponta da crista ≈ 2,9–3,0 blocos (com o jogador de 1,80–1,875) |
| `ferramentas/dimensoes.py` + hitbox (`ModEntidades`) | tabela do dono | altura 2,80; hitbox 1,2 × 2,8 |

**Recomendação:** manter **ALTURA = 2,80 blocos** (a diferença para a silhueta fica em ~3%, dentro do erro do
desenho). Modelar com **H = 45 u**, já que o exportador normaliza para 44,8. O topo do elmo cai em 39 u (2,44 blocos)
e a crista leva até 45.

| medida | ficha | no jogo (H = 2,80) | tabela atual |
|---|---|---|---|
| largura (capa aberta em sino, frente) | 0,65 H | **29 u ≈ 1,82 blocos** | 2,00 |
| comprimento (ponta do bico → ponta da cauda, lado) | 0,80 H | **36 u ≈ 2,25 blocos** | 2,90 |

Para a tabela bater com a ficha, ela precisaria virar **2,80 × 1,85 × 2,25** (ver Decisões pendentes).

---

## 2. Leitura do estilo e regras da tradução 2D → voxel

A ficha mostra um "mítico de evolução final": a ave de rapina nobre, não o galeto fofo.

- **Cerca de 5 cabeças de altura** sem a crista (cabeça de 8 u em 39 u) e ~5,6 com ela. Nada de cabeçudo nem de
  chibi.
- **Manchas que definem o personagem:**
  - juba de chamas larga em volta de um rosto pequeno e afiado;
  - colar em V com gema;
  - ombreiras que abrem como asas;
  - capa em sino;
  - pernas longas e finas;
  - garras grandes;
  - 3 tranças douradas caindo para trás.
- **Perfil em S:** a cabeça vai para a frente, o peito estufa e a capa e a cauda descem para trás. O bico fica quase
  na mesma linha da frente do peitoral (diferença de 1 u).

Regras da tradução (valem para as próximas fichas também):

1. **Travar a silhueta.** As alturas dos marcos, a largura da capa, a envergadura das ombreiras e o perfil em S
   saem direto da ficha (±0,5 u). São o que faz o bicho ser reconhecido de longe.
2. **Reforçar o que identifica.** Olhos, gemas e bico ganham +10% a +25% sobre a ficha. Na distância de jogo
   (5–15 blocos), 1 u ocupa poucos pixels de tela. A cabeça em si cresce só ~10% (6,8 → 7,5 u de largura).
3. **Dar volume mínimo ao que no 2D é traço.** Nenhuma pena, trança ou chama fica com menos de 1 u de espessura
   visível:
   - penas e chamas viram placas recortadas em X;
   - as tranças viram segmentos de 2 u.
4. **Cortar exageros de perspectiva.** O 2D desenha os pés em escorço (15 u de comprimento!), e lá eles passam a
   9,5 u. A ponta da cauda baixa, que no desenho passa do chão, sobe para ≥ 1,5 u. A barra da capa fica a 1,5 u do
   chão, para não atravessar degraus nem lajes.
5. **Manter fino onde o fino é o estilo.** As canelas ficam com 2 u e não engrossam: as pernas longas e finas são o
   que separa o mítico dos galetos comuns.

---

## 3. Divisão vertical (H = 45 u)

| faixa | y (u) | altura | % H (plano) | % H (ficha, frente) |
|---|---|---|---|---|
| crista acima do elmo | 39 → 45 | 6 | 13% | 13–14% |
| cabeça (topo do elmo → queixo) | 31 → 39 | 8 | 18% | 17–18% |
| pescoço visível / colar | 29,5 → 31 | 1,5 | 3% | 3% |
| tronco (colar → quadril) | 15 → 29,5 | 14,5 | 32% | 32% |
| coxas (saia de penas vermelhas) | 10,5 → 15 | 4,5 | 10% | 10–11% |
| perna visível (joelho → chão) | 0 → 10,5 | 10,5 | 23% | 23–24% |

### Marcos de altura

| marco | ficha (fração do topo) | y (u) |
|---|---|---|
| ponta da crista (par externo em U) | 0,00 | 45 |
| pena central da crista | 0,065 | 42 |
| topo do elmo / topo da gema da testa | 0,13–0,14 | 39 |
| centro da gema da testa | 0,19 | 36,75 |
| linha dos olhos (encostam na ponta de baixo da gema) | 0,22–0,235 | 35 |
| bico (base → ponta do gancho) | 0,25–0,305 | 34 → 30,5 |
| queixo | 0,31 | 31 |
| colar / topo das ombreiras | 0,34 | 29,5 |
| pontas douradas das ombreiras | 0,35–0,43 | 29 → 26 |
| gema do peito | 0,39–0,475 | 28 → 23 |
| ponta do V do peitoral | 0,52 | 21,5 |
| fim do peito creme / quadril | 0,67 | 15 |
| fim da saia de penas = joelheira | 0,765–0,80 | 10,5 → 8,5 |
| canela (roxa) | 0,80–0,855 | 8,5 → 5,5 |
| tornozeleira (prata) | 0,855–0,89 | 5,5 → 3,5 |
| pé escamado + dedos | 0,89–1,00 | 3,5 → 0 |
| barra da capa (laterais) | 0,97 | 1,5 |

---

## 4. Larguras (vista de frente, eixo x)

| peça | ficha (% H) | ficha (u) | **alvo (u)** | nota |
|---|---|---|---|---|
| juba (crista + chamas laterais), máx. em y ≈ 37 | 0,34–0,38 | 15–17 | **15** | placas em X; aparar 1–2 u das pontas |
| par de penas em U (externas) | 0,20 | 9 | **9** | curvam para dentro na ponta |
| cabeça (elmo/rosto) | 0,15 | 6,8 | **7,5** | +10% de legibilidade |
| gema da testa | — | 2,1 × 3,9 | **2,5 × 4,5** | losango vertical; +15% |
| bico (base, de frente) | — | 2,1 × 2,6 | **2,5 × 3** | +20% |
| pescoço | 0,11 | 5 | **5** | creme na frente, vermelho atrás |
| ombreiras (ponta a ponta) | 0,46 | 20,7 | **21** | pontas douradas viradas para cima e para fora |
| peitoral (colar em V) | 0,23 | 10,4 | **10** | |
| gema do peito | — | 2,9 × 4,6 | **3,5 × 5** | +10% |
| peito creme | 0,15 | 6,7 | **7** | chevrons de pena são pintados, não modelados |
| capa (máx., em y ≈ 9) | 0,65 | 29,3 | **29** | sino: 21 no ombro → 29 em y 9 → 27 na barra |
| distância entre as pernas (centro a centro) | 0,116 | 5,2 | **5,2** | pernas em x = ±2,6 |
| coxa | 0,07–0,08 | 3,2–3,6 | **3,5** | |
| joelheira / tornozeleira | 0,07 | 3,1 | **3** | |
| canela | 0,043 | 1,9 | **2** | não engrossar |
| pé (dedos abertos) | ~0,19 cada | 8,5 | **6** | dedo externo aberto ~25° |

---

## 5. Profundidades (vista lateral, eixo z; 0 = pivô do quadril)

| peça | z (u) | tamanho | nota |
|---|---|---|---|
| ponta do bico | -11 | — | |
| bico | -11 → -6,5 | 4,5 de comprimento × 3 de altura | ficha: 4,0 × 3,1; gancho cai até y 30,5 |
| crânio | -6,5 → 0 | 6,5 | olho em z ≈ -5,5, numa faceta diagonal (lê de frente e de lado) |
| frente do peitoral | -9,5 | — | só 1,5 u atrás da ponta do bico |
| tronco (com armadura e capa nos ombros) | -9,5 → +2,5 | 12 | núcleo do corpo com ~10 u |
| ombreiras | -4,5 → +4,5 | 9 | |
| crista varrida para trás | -5 → +12 | 17 | 5 lâminas; a mais alta em z ≈ +2,5 |
| capa: borda de trás | até +13,5 (em y ≈ 7) | — | barra em y 1,5 entre z +5 e +12 |
| coxa | -2,5 → +2,5 | 5 | |
| canela / tornozelo | -2 → 0 / -3 → 0 | — | inclina para a frente: o pé fica sob o peito |
| pé | -8 → +1,5 | 9,5 | ficha: 15 (escorço); 3 dedos na frente + 1 atrás |
| raiz da cauda | +3,5, y 23,5–25,5 | — | sai do alto das costas, logo abaixo da capa |
| ponta da cauda A (alta) | +24,5, y 16,5 | trança ≈ 20 u + lâmina 5 u | |
| ponta da cauda B (média) | +23,5, y 4,5 | ≈ 24 u + 5 u | |
| ponta da cauda C (baixa) | +19,5, y 1,5 | ≈ 22 u + 5 u | na ficha passa do chão; foi elevada |

O comprimento total vai da ponta do bico (-11) à ponta da cauda A (+24,5): **35,5 u ≈ 2,2 blocos**. Com a
espessura das tranças, fica em ~2,25.

---

## 6. Peças, contagens e formas

| parte | o que a ficha mostra | como fazer em voxel |
|---|---|---|
| crista | 2 penas externas em U (as mais altas), 1 central, 3 chamas por lado e 3 tufos de bochecha por lado; de lado são 5 lâminas varridas para trás | lâminas recortadas em X; degradê vermelho; raiz escura |
| elmo | tiara prateada com 2 asas que sobem para trás e a gema rubi/roxa vertical no centro; viseira por cima dos olhos | placa prateada facetada, 0,5 u acima da face; gema `losango` com brilho |
| olhos | estreitos, inclinados para dentro (cara séria), íris vermelho-escura | 2 × 1 u visível, pintado em res 8 numa face plana diagonal; a viseira faz a sombra |
| bico | gancho de rapina dourado; a boca abre (expressão "Bravo") | base, meio e gancho em cunha; mandíbula em osso próprio |
| colar e peitoral | V prateado em 2 camadas, gema losango no centro | 2 placas em V com chanfro; gema saltada 0,5 u |
| ombreiras | prata com miolo roxo e ponta dourada | 3 placas por lado, a de fora apontando 20° para cima |
| peito | creme com 2–3 chevrons de pena | textura (não geometria) |
| capa / asas | 3 camadas: roxa com filetes prata (~4 penas por lado), roxa → vermelha (~5) e vermelha comprida (~6) | placas recortadas em ponta, em leque; 2 ossos (`asa_d` / `asa_e`) |
| coxas | saia de penas vermelhas (3–4 por coxa) | placas em X por cima de um núcleo arredondado |
| pernas | joelheira prata pontuda, canela roxa, tornozeleira prata | caixas de 3 / 2 / 3 u |
| pés | roxo-escuro escamado, 3 dedos na frente + 1 atrás, garras douradas grossas | dedos de 1,5 u; garra em 2 segmentos curvos |
| cauda tripla | 3 tranças douradas, cada uma terminando numa pena-lâmina dourada com losango roxo | 5–6 segmentos de 2 × 2 × 3,5 u com a trança pintada (cada segmento girado 45° sobre o anterior); lâmina de 5–6 u no fim |

**Manto aberto (pose de ataque):** a envergadura medida é de ≈ 1,4 H ≈ 63 u (3,9 blocos), ou seja, ~26–27 u por asa a
partir do pivô do ombro. Isso é praticamente o comprimento da capa fechada (29,5 → 1,5 = 28 u): a capa **é** a asa. A
mesma geometria gira ~90° para abrir. Não modele asas separadas.

---

## 7. Ossos e pivôs (GeckoLib, nomes que o exportador já anima)

| osso | pai | pivô (x, y, z) | nota |
|---|---|---|---|
| `corpo` | — | (0, 15, -1) | quadril |
| `pescoco` | corpo | (0, 29, -4) | |
| `cabeca` | pescoco | (0, 31,5, -3,5) | |
| `crista` | cabeca | (0, 38,5, -2) | |
| `asa_d` / `asa_e` | corpo | (-5 / +5, 28,5, 0) | capa; abre para o "manto aberto" |
| `cauda` | corpo | (0, 24,5, +3,5) | |
| `cauda_a_N`, `cauda_b_N`, `cauda_c_N` | cauda | — | cadeias de `pena_curva`; declarar em `ONDAS` |
| `perna_d` / `perna_e` | — (raiz) | (-2,6 / +2,6, 15, 0) | x negativo = direita |

---

## 8. Orçamento

O limite é ≤ 350 peças, com textura de até 512 × 1024 e D = 2 (rosto e gemas em res 4–8). A estimativa por parte:

| parte | peças |
|---|---|
| cabeça + rosto | ~25 |
| crista | ~20 |
| armadura | ~25 |
| capa | ~36 |
| tronco e pescoço | ~10 |
| pernas | 2 × 12 |
| cauda | 3 × 8 |
| **total** | **~165** |

A folga é grande. Se sobrar, ela vai para as penas da capa e da crista, que é onde mais se vê.

---

## 9. Paleta (quadro "Paleta de Cores (Enxuta)", média 30 × 7 px)

| cor | RGB | uso |
|---|---|---|
| vermelho | (221, 28, 32) | crista, plumagem, coxas, barra da capa |
| creme | (253, 225, 192) | rosto, garganta, peito |
| roxo | (112, 42, 124) | capa (camadas de cima), canelas |
| roxo-escuro | (73, 24, 71) | sombras, pés |
| prata | (210, 190, 209) | elmo, colar, ombreiras, joelheiras, tornozeleiras |
| dourado | (252, 180, 25) | bico, garras, tranças, pontas das ombreiras |
| rubi (cristal) | (182, 25, 114) | gemas (testa e peito), losangos das lâminas da cauda |

---

## 10. O que muda em relação ao modelo atual (proporção)

Comparado ao registro p17 do `detalhes.md`:

- **Pernas visíveis:** 0,23 H, contra ~0,13 H no p17 (quase o dobro).
- **Crista:** 0,13 H acima do elmo, contra 0,19 H dos chifres dourados. Os chifres saem e o lugar vai para as
  penas vermelhas em U.
- **Armadura:** passa a ser prateada, não roxa e dourada.
- **Cauda:** as 5 plumas e as 3 correntes de contas viram 3 tranças com lâmina na ponta.
- **Medidas de caixa:** a largura vai de 1,71 para 1,82 blocos e o comprimento, de 2,47 para 2,25.

---

## Decisões pendentes (dono)

1. **Tabela de dimensões:** atualizar `dimensoes.py` de 2,80 × 2,00 × 2,90 para **2,80 × 1,85 × 2,25**, para
   bater com a ficha anime? A altura e a hitbox não mudam.
2. **Ampliação de legibilidade:** está ok a cabeça +10% e os olhos, as gemas e o bico +10% a 25%?
3. **Pés:** está ok reduzir de 15 u (escorço da ficha) para 9,5 u?

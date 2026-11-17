# Renacocó #019: auditoria independente da r65

**Data:** 2026-11-15.

**Base:**
- foto no jogo (`renacoco_r65_dia/noite`), com peso maior;
- renders da r65;
- a prancha e as 5 vistas da arte;
- os 3 pedidos do dono.

**Método:** fiz a lista olhando só as imagens. Só depois calibrei os números pela geometria do `r65.bbmodel`, com as rotações
aplicadas. Não abri `renacoco.py`, `r65.py` nem `detalhes.md`.

**Convenção dos números:**
- px do Blockbench, com y para cima;
- frente = −z (a ponta do bico está em z −13.3);
- lado direito do bicho (`_d`) = −x.

O modelo mede 44.7 px de altura e ±15.9 px de largura na bainha.

**Cauda baixa:** a cauda baixa, saindo por baixo da capa e apontando para baixo, é decisão do dono. Não é tratada como
problema.

---

## TOP 8 PROBLEMAS (do mais visível no jogo para o menos)

### 1. O peito virou brasão e tabardo de cavaleiro, com placas coladas

**Reclamações antigas:** "muito humanoide" e "placas coladas".

**Onde:** peito, vista de frente (é o centro da foto no jogo).

**O modelo:**
- `babador` é uma placa de 6.8×3.8×1.3 px, com o topo reto e os cantos vivos. Fica em x −3.4…3.4, y 25.3…29.1, z −8.0, saliente
  1.1 px do tronco.
- A cruz está pintada nela. Os 4 cubos `babador_ponta` (1.2³) fazem os "X" na borda de baixo.
- Logo abaixo há um segundo escudo, de y 18.4 a 24.5, formado por `escudo1_*` (3 tiras) e `escudo2_*` (2 tiras). Ele é
  cinza-azulado (#85A0B2 no jogo) e tem listras verticais.
- São 11 px de "placa + tabardo" num tronco de 15 px. No jogo, lê como uma túnica de cavaleiro.
- A cruz é quase grega (3×3 px). O braço de baixo é curto e encosta nos "X".

**A arte:**
- O peitilho é de penas azul-claras em V, com as pontas serrilhadas e sem nenhum cinza.
- A cruz é latina, azul-marinho, com bisel azul. Fica no terço de cima e ocupa cerca de 45 % da largura do peitilho.

**Correção:**
1. Apague `escudo1_*`, `escudo2_*` e os 4 `babador_ponta`.
2. Mantenha um só elemento central para a cruz, mas como pena:
   - 4.4 px de largura × 5.5 px de altura (y 23.6…29.1), com 0.8 px de relevo;
   - base em ponta de V, cortando os cantos de baixo com 2 degraus de 1×1;
   - topo enfiado 1 px por baixo das penas do pescoço e dos medalhões;
   - laterais cobertas 0.5 px pelas penas vizinhas, para não sobrar contorno de placa.
3. Abaixo dele, faça 3 fileiras de penas azul-claras em V, cada fileira 0.3 px atrás da de cima e com pitch −8° (ponta para
   fora):

   | Fileira | Penas | Tamanho de cada pena | y | x |
   |---|---|---|---|---|
   | 1 | 4 | 1.6×3.0×0.9 | 21–24 | ±3.2 |
   | 2 | 3 | 1.6×3.0×0.9 | 18.5–21.5 | ±2.4 |
   | 3 | 2 | 1.6×3.0×0.9 | 16–19 | ±1.6 |

4. Redesenhe a cruz:
   - latina, com 3.0 px de largura × 4.5 px de altura;
   - braço horizontal a 1/3 do topo, braços de 0.75 px com as pontas alargadas 1 texel;
   - cor #1E2A8C, com contorno #3B57C8.
5. Cores: peitilho #A6DDF5 e #CDEFFC, laterais #3FA4E8. Zero cinza.

### 2. A barra dourada do manto virou uma pilha de tijolos soltos

**Reclamações antigas:** "muitos blocos" e "peças soltas".

**Onde:** bainha do manto. Aparece de costas, de lado e de frente.

**O modelo:**
- Cada uma das 11 tiras tem a própria barra (`manto*_barra`, 1.7×1.25 px). As barras ficam em alturas diferentes e inclinadas
  até 4 px cada uma:

  | Tira | y da barra |
  |---|---|
  | manto1 | 0.1–5.0 |
  | manto0 | 1.5–5.3 |
  | manto2 | 2.9–7.4 |
  | manto3 | 5.8–8.6 |
  | manto4 | 8.5–11.3 |

- No centro de trás, `manto_costas_p_2_0…6` são 7 colunas de 1.36 px, com 7 barras em escada (y 3.1 → 10.4). O resultado é uma
  "coroa" de degraus.
- No jogo, a bainha parece lenha dourada empilhada, com vãos.
- Os elos da cauda, do mesmo dourado e do mesmo tamanho, se perdem no meio dela.

**A arte:**
- Uma faixa dourada contínua, de cerca de 1.5–2 px, segue toda a bainha e as bordas frontais.
- A bainha é reta: rente ao chão na frente e nos lados, e na altura do pé atrás.

**Correção:**
1. Ponha a bainha numa altura só:
   - frente e lados (manto0–2): y = 0.5 ± 0.3;
   - trás (manto3–4 e costas): y = 1.5 ± 0.3;
   - barras sem inclinação, com no máximo 3° de diferença entre vizinhas.
2. Barras:
   - 1.8 px de altura;
   - largura = largura da tira + 0.8, com 0.4 px de sobreposição em cada lado, para não ter vão;
   - saliência de só 0.15 px (é friso, não tijolo).
3. Abertura da cauda: troque as 7 colunas por um ARCO ÚNICO e suave no centro de trás.
   - No máximo 3 degraus, por exemplo y 2.5 / 5.5 / 8 em |x| = 9 / 6 / 3.
   - Uma só faixa dourada contínua contorna o arco.
   - Os 3 ramos da cauda saem por dentro dele.

### 3. De frente, o manto cai como duas mangas, com ombro chato e quadrado

**Reclamações antigas:** "muito humanoide" (capa caindo como vestido, ombro quadrado).

**Onde:** manto, vistas de frente e 3/4.

**O modelo:**
- As tiras da frente (`manto0_*`) abrem 19.5° nos primeiros 10 px. Depois, `d1` (roll −11°) e `d2` (roll −9°) as endireitam.
- Por isso, a borda interna dourada desce quase vertical: vai de x ±4 (y 29) a só x ±7.9 na bainha, uma abertura de 16 px.
- A gola é chata e quadrada:
  - `gola`, `dobra_*` e `ombro_*` têm o topo reto em y 30.9;
  - ela tem 17 px de largura, com os cantos em degrau;
  - as pontas das tiras aparecem como serrilhado roxo.
- No jogo, o conjunto lê como ombros de gente com duas mangas penduradas.
- A bainha externa chega a ±15.9 (31.8 px).

**A arte:**
- O manto é um "A" reto. No alto, um capelete arredondado de cerca de 18 px desce em rampa a partir do pescoço.
- As bordas frontais douradas saem dos medalhões e abrem em linha reta até x ≈ ±12.5 na bainha (abertura de cerca de 25 px).
- A bainha externa mede cerca de 40 px. Na comparação de silhueta de frente, faltam as duas pontas de baixo.

**Correção:**
1. Em `manto0_*_d1/_d2`, troque o roll de −11°/−9° para 0°/−1°. Assim, a borda interna vai em reta de x ±3.8 (y 28) até
   x ±12 (y 0.5), a cerca de 18° da vertical, sem o "joelho" em y 18.
2. Leve a bainha externa de ±15.9 para cerca de ±18 (36 px) com mais uns +6° de roll para fora nos segmentos d1/d2 de manto1 e
   manto2. É um meio-termo entre a tabela de 1.6 bloco e a arte, que manda.
3. Refaça a gola como capelete em 2 camadas descendo do pescoço:

   | Camada | x | y |
   |---|---|---|
   | De cima | ±5.5 | 28.8–30.6 |
   | De baixo | ±8.0 | 26.5–28.8 |

   - A borda externa da camada de baixo fica 1.5 px mais baixa que a interna (rampa de cerca de 20°).
   - O friso dourado de 0.6 px vai só na camada de baixo.
4. O topo de todas as tiras começa pelo menos 1 px dentro da gola (y ≤ 28). Nenhuma ponta aparece no ombro.

### 4. A cintura virou saia de bailarina, e as asas não leem como asas

**Reclamações antigas:** "muito humanoide".

**Onde:** asas e barriga, de frente e de lado.

**O modelo:**
- As asas existem em 3 camadas, o que é bom: `asa_cob`, `asa_sec` e `asa_rem`, com 11 penas por lado.
- Mas estão espalhadas por yaw de −72° a −18°, isto é, NA FRENTE do tronco, com roll de 24–28° para fora.
- As rêmiges (1.3×9.8 px) terminam em y ≈ 16, numa fileira HORIZONTAL de losangos creme e amarelos que cruza a barriga.
  `asa_rem0` chega a z −10.2, à frente do próprio peitilho.
- A fileira azul de `peito7–10` logo abaixo completa o tutu.
- De lado, a borda frontal da capa (`manto0`, pitch −20°) desce quase vertical. Ela vai de z −6.6 a z +1.5 e cobre o flanco
  inteiro, então nenhuma asa aparece.

**A arte:**
- As asas ficam nos flancos, sob a borda da capa: cobertas azuis, depois secundárias azul-claras, depois rêmiges amarelas e
  creme LONGAS caindo na vertical até a canela (y ≈ 9–10).
- Elas aparecem de frente, dentro da abertura em V.
- De lado, aparecem no triângulo que a borda diagonal da capa revela. Na prancha, essa borda tem cerca de 33° da vertical e
  toca a bainha bem atrás do pé.

**Correção:**
1. Leve as asas para o flanco:
   - pivôs em x ±5.4, z −3.5…+1.0;
   - yaw de −10° a +15°, paralelas ao flanco.
2. Apague `asa_sec0` e `asa_rem0`, que ficam na frente da barriga.
3. Penas, em leque de trás para a frente, com 0.6 px de sobreposição:

   | Tipo | Quantidade | Tamanho | Detalhe |
   |---|---|---|---|
   | Rêmiges | 4 por lado | 1.5×14×2.4 | roll 6–10° (não 25°), pontas em y ≈ 10 |
   | Secundárias | – | 1.5×9 | – |
   | Cobertas | – | 1.5×5 | – |

4. `peito7–10` e barriga só em azul e azul-claro, em V para baixo, terminando em y ≈ 15.5. Sem creme na frente.
5. Em `manto0`, troque o pitch de −20° para cerca de −30°, para a borda frontal chegar à bainha em z ≈ +8 (hoje +1.5). Isso
   abre de lado o triângulo de asa da prancha.

### 5. Cauda: pontas em "luva", elos de chapa e plumas deitadas no chão

**Onde:** cauda, de costas e de lado. A origem baixa, sob a capa e descendo, está CERTA. O problema é a forma.

**O modelo:**
- **Plumas:**
  - Cada pluma tem 5 lâminas de 0.8–0.9 px lado a lado.
  - Abrem só em pitch (−13…+10°), com yaw de ±2°.
  - Os segmentos têm 3.0, 2.0 e 0.6 px de altura. Os dois primeiros se fundem numa "palma", e os de 0.6 px viram "dedos".
  - De lado, parecem luva ou pente. De costas, ficam de perfil, um risco de 1.7 px.
- **Elos:**
  - Cada elo são duas chapas cruzadas de 1.1 px (1.1×2.2×1.26 + 1.1×1.26×2.2).
  - De costas, são uma lasca dourada igual às barras da bainha.
  - A gema azul-clara só aparece de lado.
- **Trajeto:**
  - A corrente desce a cerca de 36° da horizontal: sai da raiz (z 5.1, y 16) e chega ao leque em z 19, y 4.6.
  - Depois, leque e plumas voltam a subir (pitch −14°, −11°, −11°).
  - As plumas ficam quase horizontais, de y 1.1 a 6.2, esticadas até z 26.
  - No jogo, de lado, parece uma vassoura arrastando.

**A arte:**
- As contas são sextavadas e grossas, tão largas quanto altas, com centro azul-claro visível de todos os lados, no ritmo
  conta-elo-conta.
- As plumas são chamas de 4–5 penas afiladas amarelas, com miolo azul, abrindo em leque.

**Correção** (mantendo a origem baixa, sob a capa e para baixo):
1. Elos:
   - 2.0×2.0×2.0, mais uma cópia de 2.0×1.4×1.4 girada 45° no eixo da corrente (silhueta octogonal);
   - centro azul-claro de 1.0×1.0 nas 4 faces;
   - 0.5 px de vão, com um conector dourado de 0.8×0.8;
   - pelo menos 3 contas visíveis por ramo fora da capa.
2. Trajeto:
   - debaixo da capa, a corrente pode seguir como está;
   - fora da capa (z ≥ 17), `cauda*_leque` passa de pitch −14° para cerca de +20°, e os segmentos da pluma de −11° para +5°;
   - o eixo da pluma fica a 55–65° ABAIXO da horizontal, com as pontas em y ≥ 1.5;
   - os ramos laterais ganham +15° de yaw para fora só depois de sair do arco (pontas em x ≈ ±9).
3. Pluma:
   - 5 penas, com segmentos afilando de 1.4 → 1.0 → 0.7 px de largura e de 1.4 → 1.0 → 0.6 px de altura;
   - comprimento de 6.5–7 px;
   - aberta em cone (yaw ±14° e pitch ±12°);
   - pena central azul #3FA4E8 de 1.2 px por dentro, externas amarelas #F2C531 com ponta #FFE36A.

### 6. O pescoço some num cone de penas, a nuca tem juba e não há capuz

**Reclamações antigas:** "cabeça sem pescoço" (aparece em parte). A cabeça não está grande: 5.8 px, igual à arte.

**Onde:** pescoço e nuca, de frente, de lado e de costas.

**O modelo:**
- O pescoço real tem 3.4×4 px. Mas as 7 penas de `colar*` (1.1×5×3.2, roll ±30°) abrem num cone que chega a x ±4.6 (9.2 px)
  em y ≈ 29, tudo no mesmo azul da cabeça.
- `nuca0/1` e as 9 penas `rosto*`, que vão até z +3.6, fazem uma juba que encosta na capa.
- Por isso:
  - de frente, cabeça, pescoço e ombros formam uma pirâmide azul só;
  - de lado, pescoço mais juba somam cerca de 8 px de fundo, mais que o crânio (6.5 px);
  - de costas, o pescoço brota do tampo reto da gola como de uma mesa.

**A arte:**
- O pescoço é esguio e separado da cabeça.
- A garganta azul-clara continua no peitilho.
- Atrás da base do pescoço, um CAPUZ roxo sobe e esconde a emenda.

**Correção:**
1. Penas do `colar*`:
   - roll de ±30° para ±10°;
   - comprimento de 5 para 3.5 px;
   - base do cone com no máximo 5.5 px de largura.
2. Cores:
   - garganta em azul-claro #A6DDF5, do queixo até o peitilho;
   - nuca em azul médio, separando pela cor a cabeça do pescoço.
3. Apague `nuca1` e encurte `nuca0` para 3 px.
4. Capuz:
   - um cubo de 7.0×3.5×1.6 (x ±3.5, y 29.5–33.0, z +1.0…+2.6), com pitch +15° (topo para trás);
   - 2 abas de 1.6×3.0×3.0 em x ±3.6, com yaw ±30°;
   - roxo, com filete dourado de 0.6 px no topo.
5. Opcional: suba `pescoco_alto` 1 px para ganhar pescoço visível.

### 7. A crista é um leque de palitos de perfil e um garfo de frente

**Onde:** crista, em todas as vistas.

**O modelo:**
- Das 8 penas, 6 (`crista0–5`) ficam em x ±0.6 e abrem só no plano do perfil (pitch de 14° a 64°).
- Só `crista6/7` saem para os lados (roll ±24°).
- As penas têm 0.8–1.0 px de espessura, com vãos entre elas.
- **De frente:** 3 pontas finas, com 6.6 px de envergadura, só 1.1× o crânio. Lê como garfo ou coroa.
- **De lado:** um leque radial de palitos que aponta mais para trás do que para cima.
- **De costas:** 3 hastes.

**A arte:**
- É uma chama larga, de cerca de 1.4–1.5× a largura da cabeça (≈ 10 px).
- Tem 5–7 línguas afiladas, a central mais alta, e base azul-clara.
- SOBE: as penas da frente são quase verticais.

**Correção:**
1. 7 penas abertas em X:
   - base em x 0, ±1.0, ±1.9 e ±2.6;
   - roll 0, ±12°, ±24° e ±36°;
   - pitch de 5–25° nas 5 da frente, e de 40–50° só nas 2 de trás.
2. Forma das penas:
   - espessura afilando 1.6 → 1.2 → 0.7 px por segmento (alturas 3.0, 2.5 e 2.0);
   - vizinhas sobrepostas 0.3 px, sem vãos.
3. Envergadura de frente de pelo menos 9 px. Mantenha a altura de cerca de 7 px acima do crânio.
4. Coroa de base: 5 penas azul-claras de 1.4×2.0×1.0 em volta da raiz (y 38.4–40.4).
5. Pontas #FFE36A, sem creme nem branco.

### 8. Os pés se cruzam no meio, e as pernas parecem pernas de pau

**Onde:** pernas e patas, de frente.

**O modelo:**
- `dedo_dentro_*` (yaw ∓26°) passa da linha do meio: a garra do pé direito vai até x +2.0, e a do esquerdo até x −2.0.
- No jogo, as duas garras de dentro se sobrepõem no centro, e os pés parecem grudados.
- O vão entre os tarsos é de 2.2 px, só 0.7× a largura da perna.
- A perna é amarela lisa de y 16 a y 2, com um só anel no tornozelo. Lê como tubo, ou perna de pau.

**A arte:**
- Os pés ficam afastados, com um vão de cerca de 1 largura de perna (3–3.5 px), e os dedos abrem para a frente e para fora.
- Uma coxa emplumada azul fica por cima de cerca de 10 px de tarso amarelo escamado.

**Correção:**
1. Pivôs de `perna_*`: de x ±2.6 para ±3.2 (vão de cerca de 3.4 px).
2. `dedo_dentro_*`: yaw de ∓26° para ∓4° (para a frente). `dedo_fora_*`: de ±28° para ±34°.
3. Coxa azul emplumada:
   - 4.6×3.5×4.6, em y 12.5–16;
   - 3 pontas de pena de 1.2×1.5 na borda de baixo.
4. Tarso: 4–5 faixas de escama na textura (1 texel mais escuro a cada 1.5 px).

---

## Problemas menores

- **Medalhões:**
  - Hoje são um "+" (2.9×1.24 cruzado com 1.24×2.9, mais um miolo de 1.1) e parecem fivelas ou parafusos presos na placa.
  - Faça um octógono: 2.6×2.6×0.8, mais uma cópia de 2.6×2.6×0.6 girada 45° atrás, mais um domo de 1.0×1.0×0.4.
  - Posição: no topo do peitilho (x ±3.0, y 28.5), servindo de início da borda dourada da capa.
- **Penas faciais:**
  - Hoje `rosto*` fica em x ±1.7…2.9, dentro da largura do crânio (±2.9). De frente não aparecem; só formam espetos na nuca.
  - Pivô em x ±3.0, começando em z −3.5 (logo atrás do olho).
  - Yaw ±25° para fora, pitch 25–35° para cima, 1.3 px de espessura.
  - Assim formam a moldura nobre de frente.
- **Bico:**
  - Hoje tem 6.0 px (z −7.3 → −13.3), 92 % do crânio, e afila só de 2.5 para 1.8 px, como bico de pato. Na arte, é cerca de
    55–60 % do crânio.
  - Encurte para 4.3 px (ponta em z ≈ −11.6), com altura de 2.6 → 1.0 px na ponta e gancho de 0.5 px para baixo.
- **Topo da cabeça e olho:**
  - `cranio_alto_a/b` têm 0.0 px de altura, e a faixa ciano no topo vira boné ou elmo.
  - Troque por um cubo de 0.5 px no azul da cabeça e chanfre 0.75 px nos cantos de cima.
  - Esclera de cinza para branco #F4F4F4.
- **Cauda vista de frente:**
  - Entre as pernas aparecem a cauda central (uma escada dourada na altura do joelho) e os elos laterais com gema.
  - Ponha um forro roxo-escuro (#3B1650) de 1.0 px atrás das pernas (x ±2.4, y 3–14, z +3.0), ligado ao corpo.
- **Superfície do manto:**
  - 11 tiras finas de 3 segmentos fazem degraus de 0.1–0.5 px e topos em serrote, como uma cortina de tiras.
  - Funda em 4 dobras largas por lado (6–8 px), alternando 0.8 px de profundidade.
- **Lâminas finas e garras:**
  - Têm menos de 0.5 px: `babador_0_b/_c` (0.1 px), `quilha_b/_c` (0.2 px) e `queixo_a/_b` (0.24 px). Engrosse para 0.5 px ou
    apague.
  - As garras afundam 0.47 px no chão (y −0.47). Apoie em y 0.
- **Grega dourada das pontas:**
  - Os "L" têm cerca de 1×1.5 px e quase somem no jogo.
  - A prancha tem um padrão escalonado de cerca de 5×6 px nos 4 cantos da bainha.

## O que já está fiel

- **Leitura imediata:** ave azul com manto roxo de bordas douradas. Mesmo de longe, no jogo, é o Renacocó.
- **Costas:** o emblema da fênix e os 3 losangos com centro azul estão legíveis de dia e de noite, e fiéis à traseira da prancha.
- **Cauda:** cumpre a decisão do dono.
  - Raiz no corpo (y 14–18, osso `cauda` filho de `corpo`).
  - Sai por baixo da capa e desce.
  - 3 ramos, com gema azul-clara que brilha à noite.
- **Rosto:** a sobrancelha forte sobre a íris azul dá a expressão séria e serena da neutra. A barbela vermelha está no lugar.
- **Rig para GeckoLib:**
  - cadeias de cauda com pivôs encadeados;
  - capa em tiras de 3 segmentos (para o balanço);
  - asas já em 3 camadas;
  - perna, tarso, pata e dedos separados.

## Notas

| Olhar | Nota |
|---|---|
| 1. Fidelidade | **6** / 10 |
| 2. Região superior (cabeça, pescoço, crista, rosto) | **5** / 10 |
| 3. Capa e peito | **4** / 10 |
| 4. Cauda | **5** / 10 |
| 5. Qualidade de jogo | **5** / 10 |
| **Geral** | **5** / 10 |

Comparada com o Esporocó aprovado, a r65 ainda fica abaixo. O Esporocó lê como penas orgânicas sobrepostas. A r65 ainda mostra
placas (peito e medalhões), tijolos (bainha), tiras (manto) e palitos (crista e plumas). Os itens 1 a 4 são os que mais pesam na
foto do dono.

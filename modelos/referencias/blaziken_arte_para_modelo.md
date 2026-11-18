# Da arte oficial ao modelo: como o Cobblemon adaptou o Blaziken

A partir de 18/11/2026, os Cocorídeos são modelados a partir de uma ilustração no estilo da arte oficial dos
Pokémon: corpo inteiro, pose de ação, cores chapadas com sombra de anime, contorno preto e fundo transparente. Este
estudo mostra como o Cobblemon transformou a arte oficial do Blaziken no modelo 3D dele. O método que saiu daqui
está na seção 13 de `modelos/GUIA_ESTILO.md`.

Fontes:
- a arte oficial do Blaziken, enviada pelo dono (direitos da Nintendo / Game Freak; **não fica no repositório**);
- o modelo do Cobblemon 1.8.4 (CC BY-NC 3.0; também fora do repositório).

Ferramentas: `ferramentas/comparar_arte.py` e `rampa_da_arte()` em `ferramentas/cobble_base.py`.

## 1. A pose da arte vira uma animação
O modelo é feito em **pose neutra**: braços abertos na horizontal e pernas retas e juntas. A pose da arte (chute com
a perna de trás esticada na diagonal, joelho da frente erguido, braço com as garras à frente, cabeça virada) é
recriada numa animação estática, a `render`, que o Cobblemon usa para retratos e imagens.

`comparar_arte.py` procura o ângulo de câmera em que a silhueta do modelo mais se sobrepõe à da arte:

| pose do modelo | sobreposição com a arte (IoU) |
|---|---|
| `render` (yaw -20°, pitch 17°) | **66%** |
| `battle_idle` | 59% |
| `ground_idle` | 52% |

A `render` mexe em 50 ossos. Por exemplo: a coxa esquerda gira -77,5° e o joelho dobra 107,5°, a coxa direita gira
44° para o outro lado, o corpo vira 47,5° e os dedos se fecham em garra. A diferença que sobra está nos detalhes (seção 5), não nas
proporções.

## 2. O que virou geometria (silhueta)
Tudo o que muda o contorno da criatura na arte ganhou peça própria:

| na arte | no modelo |
|---|---|
| "cabeleira" creme longa, caindo pelas costas até a cintura | corrente de 4 ossos: base 3x4x6, 6x5x4, 6x11x4 e (6x10x3 + 4x10x2), com 2 planos 0x8x2 de ponta em cada lado e um plano 0x8x20 atrás. São 31 px de comprimento, metade da altura |
| os dois "chifres" vermelhos em V na testa | 2 planos 0x1x9 girados 30°/±37,5° (na fêmea, 0x1x7) |
| máscara vermelha pontuda com bico | bico 2x3x2 girado + 3x3x4; o rosto em cunha com 2 planos 0x4x8 girados ±38,5° |
| olho amarelo com íris azul | plano 0x2x4 + pupila 0x2x1 + 2 pálpebras escondidas |
| tufos de penas creme no peito e no pescoço | peito 8x5x7 + "jaqueta" de 2 caixas 4x4x7 com franjas em planos (0x3x7, 4x3x0) |
| V amarelo no meio do peito | plano 5x8x0 com recorte em escudo pontudo, pintado de amarelo |
| braço vermelho fino e comprido | 3 caixas (3x4x4, 7x2x3, 10x2x3) |
| mão cinza de 3 garras | palma 4x2x4 + 3 dedos de 3 segmentos (2x2x2, 2x2x2 e a ponta em plano 2x2x0) |
| coxa vermelha grossa | caixa 7x17x7 |
| "bota" amarela mais larga que a coxa | caixa 9x13x9: **mais larga que a coxa (7)**, que é o que dá a silhueta de bota da arte |
| tufos de chama em volta do tornozelo | 4 planos 10x0x3 e 3x0x10 girados, em saia |
| 3 garras do pé e o esporão | planos 0x3x2 e 0x2x4 |
| tufo creme na cintura | plano 0x4x4 girado 22,5° |

Proporções do modelo em pose neutra (59 px de altura): pernas até o quadril 53%, tronco 27%, pescoço e cabeça 20%.
Braços de ~30 px, cabeleira de 31 px.

## 3. O que virou textura (desenho interno)
- **A linha serrilhada entre o vermelho e o amarelo da perna** (as "línguas de fogo" da arte) é pintada pixel a pixel
  na face da caixa da bota, sem geometria extra. Na face da frente (9x13), cada "língua" sobe de 1 a 4 px:
  ```
  RRRRRYRRR
  RRRRRYRRR
  RRRRRYRRR
  RRRRYYRRR
  RYRRYYYRR
  RYRRYYYRR
  RYYRYYYRR
  YYYYYYYRY
  YYYYYYYYY   (R = vermelho, Y = amarelo)
  ```
- As áreas de cor ficam **exatamente onde estão na arte**: creme no peito, nos ombros e na cabeleira, vermelho nos
  braços e coxas, amarelo da metade da canela para baixo, cinza nas mãos.
- Não há contorno preto nem a sombra de anime; no lugar entram rampas de 4 a 8 tons com mosqueado leve.

## 4. Cor: da pintura de anime para pixel art
Medido por região (mediana dos pixels):

| região | arte (cor, matiz/saturação/brilho) | textura | nº de tons na textura |
|---|---|---|---|
| vermelho | (187, 87, 69), 9°/0,63/0,73 | (200, 46, 41), 2°/0,80/0,78 | 7 |
| creme | (240, 226, 198), 40°/0,17/0,94 | (213, 195, 157), 41°/0,26/0,84 | 8 |
| amarelo | (236, 202, 124), 42°/0,46/0,93 | (219, 176, 61), 42°/0,70/0,86 | 6 |
| cinza das mãos | (167, 151, 138), 26°/0,17/0,65 | (157, 132, 121), 16°/0,23/0,62 | 4 |

A regra:
1. **O matiz se mantém** (±7°).
2. **A saturação sobe ~1,35x** (0,63 → 0,80; 0,46 → 0,70).
3. **As cores claras escurecem um pouco** (brilho até ~0,85): na tela do jogo, a luz já clareia.
4. **Rampa com deslocamento de matiz**: a cada tom mais claro, matiz +3° (para o amarelo), saturação -0,045 e
   brilho +0,055. Para o escuro, o passo de brilho é maior (-0,085).

| rampa do Blaziken (escuro → claro) | H / S / V |
|---|---|
| vermelho | -5/0,85/0,59 · -1/0,81/0,69 · 2/0,80/0,78 · 5/0,76/0,84 · 8/0,72/0,89 |
| creme | 37/0,37/0,73 · 38/0,32/0,78 · 41/0,26/0,84 · 45/0,21/0,88 · 48/0,17/0,92 |
| amarelo | 36/0,75/0,76 · 39/0,70/0,81 · 42/0,65/0,86 · 46/0,60/0,92 · 49/0,55/0,97 |

`rampa_da_arte(cor_da_arte)` aplica essa regra. Gerando as 4 rampas a partir das cores da arte, ela chega a uma
distância média de 15 (em RGB, de 0 a 441) das rampas que o Cobblemon pintou à mão. O vermelho é o que mais desvia:
eles puxaram o matiz uns 7° para o vermelho puro.

## 5. O que o Cobblemon simplificou ou acrescentou
A sobreposição da pose `render` mostra onde arte e modelo diferem:
- **Membros afunilados viram caixas retas** com a largura máxima do membro: as pernas e a cabeleira do modelo
  ficam um pouco mais "gordas" que as da arte nas pontas.
- **Contornos serrilhados viram borda reta + desenho na textura**; só os tufos que mudam muito a silhueta (tornozelo,
  peito, ponta da cabeleira) ganham planos com recorte.
- **Garras e mãos ficam menores** que na arte (a arte exagera as mãos em primeiro plano).
- **Acréscimos que a arte não mostra**: fogo nos pulsos e nos pés (ossos com escala 0, ligados na batalha),
  pálpebras para piscar e pontos de referência (`locator_*`).

## 6. O que levar para os galetos
1. A ilustração define a silhueta, as proporções e as áreas de cor; o modelo é feito em pose neutra.
2. Tudo o que muda o contorno vira peça; o desenho interno, inclusive linhas serrilhadas, vira textura.
3. As cores saem da arte pela regra da seção 4 (`rampa_da_arte`), sem contorno e sem sombra de anime.
4. A pose da ilustração vira uma animação `render`, conferida com `comparar_arte.py`. Meta: sobreposição de pelo
   menos 60% (o Blaziken dá 66%).

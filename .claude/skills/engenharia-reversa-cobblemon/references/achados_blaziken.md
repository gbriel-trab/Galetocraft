# Achados de referência (Cobblemon 1.8.4, estudos de 18/11/2026)

Use estes números como régua ao estudar outro modelo. Os relatórios completos estão no repositório Galetocraft, em
`modelos/referencias/`:
- `blaziken_cobblemon_engenharia_reversa.md`;
- `combusken_cobblemon_engenharia_reversa.md`;
- `blaziken_arte_para_modelo.md`;
- o padrão derivado: `modelos/GUIA_ESTILO.md`.

## 1. Linha do Torchic
| | Torchic | Combusken | Blaziken ♂ |
|---|---|---|---|
| baseScale / altura no jogo (parado) | 0,6 / 0,89 bl | 0,8 / 1,68 bl | 0,8 / 2,90 bl |
| ossos (sem cubo) | 63 (8) | 60 (6) | 102 (13) |
| profundidade da árvore | 6 | 7 | 12 |
| cubos / faces desenhadas | 57 / 258 | 72 / 268 | 127 / 470 |
| planos (espessura 0) | 37% | 57% | 57% |
| cubos girados no próprio pivô | 2 | 8 | 24 |
| inflate | 24 | 10 | 39 (0,01 / 0,02 / -0,01) |
| mirror | 7 | 0 | 11 |
| tamanhos fracionados / UV por face | 0 / 0 | 0 / 0 | 0 / 0 |
| textura / cores / uso da folha | 64x32 / 23 / 77% | 128x128 / 26 / 17% | 256x128 / 33 / 35% |
| animações | 18 | 4 (andar procedural) | 19 |

Para comparar: o Pirococó antigo do Galetocraft (2,8 blocos) tinha 404 cubos, 2.313 faces, textura 512x512 e 288
cores, com UV por face e tamanhos fracionados.

## 2. Amostra de 78 modelos (1 a cada 15 pastas da Pokédex + 20 aves e lutadores)
| altura no jogo | cubos (mediana / p90) | faces (mediana / p90) | textura típica | cores (mediana / p90) |
|---|---|---|---|---|
| até 1 bloco | 42 / 74 | 162 / 264 | 64x64 | 25 / 34 |
| 1 a 2 | 72 / 108 | 300 / 524 | 128x64, 64x64, 128x128 | 26 / 37 |
| 2 a 3 | 97 / 145 | 408 / 531 | 256x256, 256x128, 128x128 | 32 / 55 |
| acima de 3 | 108 / 266 | 455 / 1.223 | 256x256 | 32 / 64 |

Gerais (mediana, entre parênteses p10–p90):
- **Planos:** 46% (19–73%). Nas aves, 69% das peças de asa e 100% das "feathers" são planos, mas a base da asa é uma
  placa de 1–3 px.
- **Cubos girados no próprio pivô:** 5% (0–23%).
- **Fracionados:** 0. **UV por face:** 0 de 78.
- **Uso da folha:** 52% (35–69%).
- **Inflate:** os valores mais comuns são 0,01, 0,02 e 0,03.
- **Mosqueado:** fração de vizinhos que diferem de 0,42 (0,32–0,54); contraste entre vizinhos do mesmo material
  ~16 de luminância.
- **Luz pintada:** tampa +5 e fundo -7 em relação aos lados (luminância 0–255); sem fio escuro nas bordas.
- **Pálpebras:** 65 de 80 modelos têm; 72 têm `blink`. **Locators:** 77 de 80.
- **Asas:** 41 de 80 têm dois conjuntos, `wing_open_*` e `wing_closed_*`, trocados por escala 0.
- **Animações mais comuns:** `ground_idle` 79, `blink` 72, `cry` 66, `ground_walk` 46, `sleep` 44,
  `battle_idle` 37.
- **Andar procedural:** 15 de 78.
- **Ossos mais comuns:**
  - `body`, `head`, `torso`, `tail#`, `eye_*`, `eyelid_*`, `pupil_*`, `jaw`, `neck`, `leg_*`, `foot_*`, `arm_*`;
  - locators: `locator_eye_*`, `locator_head`, `locator_mouth`, `locator_root`, `locator_foot_*`;
  - a raiz tem o nome da espécie.

## 3. Técnicas confirmadas no Blaziken
- **Pose de modelagem T;** o `ground_idle` dá a postura (cintura +15°, tronco -12,5°, pernas ±10,9°, dedos fechados).
- **Pálpebra:**
  - o olho é um plano em x=1,51 e a pupila fica a +0,01;
  - a pálpebra fica em x=1,42 com inflate 0,01;
  - o `blink` move a pálpebra +0,1 em 0,125 s (total 0,1667 s);
  - a `eyelid_recoil` é a segunda pálpebra, para dor.
- **Rosto em cunha:** 2 planos 0x4x8 girados ±38,5°. **Sobrancelhas / "chifres":** planos 0x1x9 girados.
- **Fogo nos pulsos e nos pés:** leques de 3 planos (±60–65°), com escala 0 fora da batalha.
- **Bota mais larga que a coxa** (9 contra 7). A borda de fogo é um zigue-zague pintado na face da caixa.
- **Animações:**
  - parado só em Molang, k = 0,5 a 32, loop de 8 s, cauda com fase -30/-60/-90;
  - andar com keyframes `catmullrom` nas pernas e Molang no corpo (k = 4 balanço, 8 quique);
  - olhar com pesos 5/15/20/15/35 (cintura → cabeça) e a cabeleira girando -20 ao contrário;
  - `physical` com o corpo girando até 690° e a raiz esticando 1,2 em Y;
  - `*_test` move a raiz a `-q.anim_time*16*4*0,75`;
  - 3.378 keyframes `catmullrom` contra 487 lineares.
- **Erro no arquivo:** 148 expressões com parênteses errados no Z do `hand_fire_*`.
- **Shiny:** 8.574 de 10.087 pixels mudam; o fogo não muda. **Alpha:** 14 pixels (os olhos).
- **Fêmea:** 6 ossos (cabeleira 11/10/10 → 10/7/9, sobrancelhas 9 → 7).

## 4. Técnicas confirmadas no Combusken
- Andar procedural pelo poser: `q.biped_walk(1, 1, 'leg_left', 'leg_right')` e `q.bimanual_swing(1, 1, ...)`.
  - Os argumentos substituem os padrões (0,6662 e 1,4 / 0,6662 e 1,0).
  - Perna: `cos(limbSwing·1 [+π])·amount·1` rad, ±57°.
  - Vaivém parado dos braços: Z (0 a 5,7°, ciclo de 3,5 s) e Y (±2,9°, ciclo de 4,7 s).
  - Fonte: `ClientMoLangFunctions.kt`, `BipedWalkAnimation.kt` e `BimanualSwingAnimation.kt`.
- Olho = cubo 2x3x1 na quina da cabeça (+0,01 na frente e no lado); pálpebra = cópia 0,1 para dentro, com inflate
  0,03.
- "Saia" de 10 planos no quadril; crista de 3 penas com 2 segmentos (planos).
- Fêmea: 6 planos da crista, com outro desenho numa região da mesma textura.
- A paleta shiny se repete com o Blaziken: (109,23,23), (94,18,18) e (129,30,30).
- Erro: o `cry` anima um osso `neck` que não existe (o Torchic tem o mesmo erro).

## 5. Arte oficial → modelo (Blaziken)
- **Pose:** sobreposição da silhueta com a arte de 66% na pose `render`, 59% no `battle_idle` e 52% no `ground_idle`.
- **Cor por região** (arte → textura):

| região | arte | textura |
|---|---|---|
| vermelho | (187,87,69), S 0,63, V 0,73 | (200,46,41), S 0,80, V 0,78 |
| creme | (240,226,198), S 0,17, V 0,94 | (213,195,157), S 0,26, V 0,84 |
| amarelo | (236,202,124), S 0,46, V 0,93 | (219,176,61), S 0,70, V 0,86 |
| cinza | (167,151,138), S 0,17, V 0,65 | (157,132,121), S 0,23, V 0,62 |

- **Rampas da textura** (escuro → claro, H/S/V):
  - vermelho: -5/0,85/0,59 · -1/0,81/0,69 · 2/0,80/0,78 · 5/0,76/0,84 · 8/0,72/0,89;
  - amarelo: 36/0,75/0,76 · 39/0,70/0,81 · 42/0,65/0,86 · 46/0,60/0,92 · 49/0,55/0,97.
- **O que vira geometria:** o que muda o contorno (cabeleira, chifres em V, mãos de 3 garras, bota, tufos do
  tornozelo, tufo da cintura, V do peito em plano recortado).
- **O que vira textura:** o desenho interno (bordas serrilhadas, áreas de cor). Sem contorno preto e sem sombra de
  anime.

## 6. Primeiro uso do método num modelo próprio (Pirococó g3)
- 83 cubos, 362 faces, textura 128x64, 28 cores, 41% de planos e 0 cubos girados.
- Sobreposição com a arte de 48%: o manto fluido e as caudas finas em 3/4 ficam mais "cheios" em blocos.
- As vistas ortográficas da ficha batem bem.
- Lição: compare também as vistas de frente, lado e costas, não só a arte em 3/4.

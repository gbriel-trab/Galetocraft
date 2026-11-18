# Combusken do Cobblemon: engenharia reversa do modelo 3D

Continuação do estudo do Blaziken (`blaziken_cobblemon_engenharia_reversa.md`), com a mesma fonte (Cobblemon
**1.8.4**, `gitlab.com/cable-mc/cobblemon`), a mesma licença (modelos em **CC BY-NC 3.0**; código em MPL 2.0) e a
mesma regra: aqui ficam só medidas e técnicas, nenhum arquivo do Cobblemon. Feito em 18/11/2026 com
`ferramentas/analisar_geo.py`.

O Combusken é interessante por ser **de outra "geração" de modelos do Cobblemon**. É um modelo mais simples e
antigo, em que o andar não vem de um arquivo de animação: é calculado pelo código do mod. Comparar com o Blaziken
mostra as duas formas de animar uma criatura.

## Resumo
1. **Andar procedural:** o Combusken não tem animação de andar. O poser soma ao parado as funções
   `q.biped_walk(1, 1)` e `q.bimanual_swing(1, 1)`, que giram pernas e braços com uma cosseno da distância
   andada. É a fórmula das pernas do jogador no Minecraft, com período e amplitude ajustados. O passo acompanha
   a velocidade real da criatura, então **o pé não escorrega**.
2. **Parado estático:** o `ground_idle` só fixa a postura (braços para baixo, pés abertos). Não respira nem
   balança; o único movimento parado é o leve vaivém dos braços que vem do `bimanual_swing`.
3. **Olho na quina da cabeça:** o olho é um cubo 2x3x1 encaixado no canto da cabeça e saliente 0,01. Aparece
   de frente e de lado.
4. **Fêmea com outro desenho na mesma textura:** só os 6 planos da crista mudam. A crista da fêmea é mais
   baixa e usa outra região da textura, que fica guardada na folha e o macho não usa.
5. **Paleta shiny compartilhada na linha evolutiva:** os vermelhos-escuros do Combusken shiny (109,23,23),
   (94,18,18) e (129,30,30) são os mesmos do Blaziken shiny.
6. **Erro encontrado:** o grito (`cry`) anima um osso `neck` que não existe no modelo. O Torchic tem o mesmo
   erro, provavelmente copiado de um modelo-base. Nenhum Cocorídeo tem esse problema (todos verificados).

## Arquivos e montagem
| arquivo | conteúdo |
|---|---|
| `data/cobblemon/species/generation3/combusken.json` | `baseScale` **0,8**, hitbox 0,8 x 1,65, Fogo/Lutador, imune a fogo, nada em lava |
| `resolvers/0256_combusken/0_combusken_base.json` | modelo `combusken_male.geo`; `shiny` troca a textura; `alpha_eyes` põe a camada emissiva |
| `resolvers/0256_combusken/1_combusken_female.json` | aspecto `female` troca só o modelo |
| `posers/0256_combusken/combusken.json` | 2 poses (abaixo); retrato 2,17, perfil 0,54 |
| `models/0256_combusken/combusken_{male,female}.geo.json` | geometria Bedrock 1.12.0, `geometry.combusken_male` / `_female` |
| `animations/0256_combusken/combusken.animation.json` | 4 animações |
| `textures/pokemon/0256_combusken/combusken{,_shiny,_alpha}.png` | 128x128 |

| pose | quando | animações |
|---|---|---|
| `standing` | parado, flutuando, retrato, perfil | `q.look('head')` + `ground_idle` + piscar |
| `walking` | andando, nadando | `q.look('head')` + `ground_idle` + `q.biped_walk(1, 1, 'leg_left', 'leg_right')` + `q.bimanual_swing(1, 1, 'arm_left', 'arm_right')` + piscar |

Não há pose de dormir nem de batalha, e não há animações de ataque: o Combusken não tem movimento próprio para
esses momentos.

## Geometria
| | Combusken ♂ | Blaziken ♂ | Pirococó |
|---|---|---|---|
| ossos (sem cubo) | 60 (6) | 102 (13) | 63 (1) |
| profundidade máx. | 7 | 12 | 7 |
| cubos | **72** | 127 | 404 |
| faces desenhadas | **268** | 470 | 2.313 |
| planos (espessura 0) | 41 (57%) | 73 (57%) | 0 |
| cubos girados no próprio pivô | 8 | 24 | 292 |
| inflate | 10 (0,01 a 0,03) | 39 | 0 |
| mirror | 0 | 11 | 0 |
| textura | 128x128, 26 cores, **17% usada** | 256x128, 33 cores, 35% | 512x512, 288 cores, 79% |
| altura no jogo (parado, x0,8) | **1,68 blocos** | 2,90 | 2,80 |
| largura x comprimento (parado) | 1,45 x 0,76 | 1,65 x 1,42 | 1,60 x 2,73 |

### Esqueleto
```
combusken
└ body
  ├ waist (6x6x6) ── torso (6x8x6)
  │  │  ├ arm_* (6x2x3) ── forearm_* (6x2x4 + 4 planos de pena no pulso) ── claws_* (3 planos 5x2x0)
  │  │  └ head (7x7x7 + bico 3x1x2) ── jaw (2x1x2)
  │  │       ├ feathers ── comb_middle1 ── comb_middle2 / comb_left1 ── comb_left2 / comb_right1 ── comb_right2
  │  │       └ eye_* (olho 2x3x1 + pupila 1x2x1 + brilho 1x1x0) ── eyelid_*, locator_eye_*
  │  ├ fluff ── 10 planos (a "saia" de penas do quadril)
  │  └ tail1 (3x4x6) ── tail2 (2x3x3)
  └ leg_* (coxa 6x6x6) ── leg_*_mid (canela 2x5x2) ── foot_* (3x1x4) ── toe_*1..3 + toe_back_* (1x1x3) ── toenail_* (plano 0x1x1)
```
Não há pescoço: a cabeça (um cubo 7x7x7) fica direto no tronco.

### Técnicas encontradas
- **Pose T também aqui.** Os braços são modelados na horizontal; o `ground_idle` os baixa 40° em Z, gira os
  antebraços 22,5° em Y e abre as pernas ±20° em Y (pés para fora).
- **Olho na quina da cabeça.** A cabeça vai de -3,5 a 3,5. O olho é um cubo 2x3x1 que começa em -3,51: fica
  0,01 para fora na frente **e** no lado, então a face lateral dele (1 px de largura) aparece de perfil. A
  pupila (1x2x1) fica 0,02 para fora e o brilho (plano 1x1x0) 0,03. As camadas são separadas por 0,01 em vez
  de inflate.
- **Pálpebra cúbica escondida.** A pálpebra é uma cópia do olho (2x3x1, inflate 0,03), recuada 0,1 em X e em
  Z para dentro da cabeça. O `blink` (0,17 s) a puxa 0,1 para fora nos dois eixos e ela cobre o olho inteiro,
  inclusive a face lateral.
- **"Saia" de penas com 10 planos.** O `fluff` do quadril são 10 planos pequenos (3x0x7, 2x0x6, 2x0x3 e
  3x0x2) inclinados de 7,5° a 40° em volta da cintura. Fazem volume e franja com 20 faces.
- **Pulso e garras.** Cada antebraço tem 4 planos de pena em cruz (2 deitados 2x0x5, 2 em pé 2x3x0) e 3 garras
  planas 5x2x0 empilhadas.
- **Crista em 3 penas de 2 segmentos.** Cada pena tem 2 planos (4x5 + 5x5 no meio, 3x4 + 3x4 dos lados). As
  laterais abrem ±50° em Z e todas inclinam para trás (-15° a -20°). O segundo segmento dobra mais 5°, o que
  dá curvatura com só 6 planos.
- **Dedos com unhas planas.** 4 dedos 1x1x3 por pé (os da frente abertos ±15°) e unhas em planos 0x1x1.
- **Textura com sobra.** Só 17% da folha 128x128 está em uso. Tudo cabe no quarto de cima à esquerda, mais a
  crista da fêmea logo abaixo; daria para usar 128x64 ou menos.

### Fêmea
O esqueleto, a textura e o resto são iguais. Mudam só os 6 ossos da crista:
- a pena do meio fica 1 px mais baixa (5 → 4 px no primeiro segmento, e o segundo desce 1 px);
- **todos os 6 planos apontam para outra região da textura** (canto de baixo à esquerda), onde a crista da
  fêmea tem outro desenho. A região fica na mesma folha e o macho não a usa.

### Textura e variantes
- 26 cores: amarelo (255,213,98), (240,191,87), (225,172,76) e (255,229,116); laranja-avermelhado (247,161,90),
  (232,139,79), (217,117,69), (202,95,59) e (187,77,51); cinza-rosado dos pés (187,150,128), (169,133,110) e
  (151,116,92).
- **Shiny:** 2.274 dos 2.712 pixels opacos mudam, com a mesma UV e a mesma silhueta. O amarelo vira creme
  pálido (255,213,98 → 241,217,150) e o laranja vira vermelho-escuro (202,95,59 → 109,23,23). Os pés não mudam.
- **Mesma paleta shiny que o Blaziken:** (109,23,23), (94,18,18) e (129,30,30) aparecem nos dois. A linha
  evolutiva tem uma paleta shiny única.
- **Alpha:** 54 pixels emissivos nos olhos, em vermelho e rosa.

## Animações
| animação | duração | loop | ossos | keyframes | observação |
|---|---|---|---|---|---|
| `ground_idle` | — | sim | 6 | 0 | só valores fixos: postura, sem movimento |
| `blink` | 0,17 s | não | 2 | 6 | pálpebras ±0,1 em X e -0,1 em Z |
| `cry` | 1,5 s | não | 3 | 12 | som em 0,04 s; cabeça -15°, bico 47,5°; o `neck` (+10°) **não existe no modelo** |
| `render` | — | — | 30 | 0 | pose estática para imagem (pulo com garras abertas) |

### O andar procedural (código do Cobblemon)
Fonte: `client/ClientMoLangFunctions.kt` (registra as funções) e
`client/render/models/blockbench/animation/BipedWalkAnimation.kt` e `BimanualSwingAnimation.kt` (MPL 2.0).

`q.biped_walk(período, amplitude, perna_esq, perna_dir)` tem como padrão **0,6662 e 1,4**, os mesmos números do
`HumanoidModel` do Minecraft (pernas do jogador e do zumbi). O `bimanual_swing` usa 0,6662 e 1,0. O Combusken
passa **(1, 1)**, que **substitui** esses padrões: passos mais curtos e rápidos e perna menos aberta que a do
jogador.

`limbSwing` é a "distância andada" que o Minecraft acumula e `limbSwingAmount` vai de 0 (parado) a 1
(velocidade máxima). Os ângulos estão em radianos:

| osso | eixo | fórmula no Combusken | máximo |
|---|---|---|---|
| perna esquerda | X | `cos(limbSwing·1) · amount · 1` | ±57° |
| perna direita | X | `cos(limbSwing·1 + π) · amount · 1` | ±57° (meio ciclo atrasada) |
| braços | Y | `cos(limbSwing·1) · amount · 1` (o mesmo sinal nos dois; como os braços são espelhados, um vai e o outro volta) | ±57° |
| braços, vaivém parado | Z | `±(cos(idade·0,09)·0,05 + 0,05)` | 0 a 5,7°, ciclo de 3,5 s |
| braços, vaivém parado | Y | `±sin(idade·0,067)·0,05` | ±2,9°, ciclo de 4,7 s |

Com o padrão humano (0,6662), uma passada completa leva 9,4 unidades de `limbSwing`; com 1, leva 6,3 (1,5x
mais passos na mesma distância, coerente com uma perna curta). Como o ciclo depende da distância andada e não do
tempo, a passada acelera e desacelera com a criatura e nunca "patina". No Blaziken, o mesmo problema é resolvido
à mão, com as animações `*_test` calibrando o passo.

## Combusken x Blaziken: duas gerações
| | Combusken | Blaziken |
|---|---|---|
| animações | 4 | 19 |
| parado | postura fixa | senoides em Molang, loop de 8 s |
| andar | procedural, no código | keyframes nas pernas + Molang no corpo; trote e corrida separados |
| poses | 2 | 6 (inclui sono e batalha) |
| ataques | nenhum | `physical`, `special`, `status` |
| olho | cubo na quina + pálpebra cúbica | planos em face facetada + pálpebra plana |
| mirror | não usa | 11 cubos |
| cuidado com a textura | 17% da folha | 35% da folha, 3–5 tons por material |

## O que levar para o Galetocraft
| ideia | por quê |
|---|---|
| Andar ligado à velocidade real (`limbSwing`/`limbSwingAmount`), em vez de um ciclo de tempo fixo | o andar do Pirococó hoje é um loop fixo de 0,8 s (`animation.pirococo.walk`), qualquer que seja a velocidade; com o ciclo preso à distância andada o pé não escorrega em nenhuma velocidade. Dá para somar a fórmula acima às pernas no renderizador em Java, por cima da animação do GeckoLib |
| Olho em cubo na quina da cabeça | em cabeças em forma de caixa, o olho aparece de frente e de lado com 1 cubo |
| Variante desenhada numa região sobrando da mesma textura | permite fêmea ou forma regional sem um segundo PNG |
| "Saia" e franjas com planos pequenos inclinados | dá volume de pena no quadril e nos pulsos gastando 2 faces por pena |
| Paleta shiny única por família ou elemento | os Cocorídeos de fogo poderiam compartilhar a mesma troca de cores |
| Checar ossos animados que não existem | o `analisar_geo.py` agora avisa; os 12 Cocorídeos passaram |

## Como reproduzir
O download do estudo do Blaziken já traz o Combusken (`**/0256_combusken/**`). Para ler também o código do
andar procedural, acrescente ao checkout:
```
git sparse-checkout add "**/BipedWalkAnimation.kt" "**/BimanualSwingAnimation.kt" "**/client/ClientMoLangFunctions.kt"
```
Análise (Prompt do Windows, a partir da pasta do Galetocraft):
```
set C=..\cobblemon\common\src\main\resources\assets\cobblemon
python ferramentas\analisar_geo.py %C%\bedrock\pokemon\models\0256_combusken\combusken_male.geo.json %C%\textures\pokemon\0256_combusken\combusken.png --anim %C%\bedrock\pokemon\animations\0256_combusken\combusken.animation.json --pose ground_idle --pose cry@0.5 --pose render --escala-jogo 0.8 --escala 12 --saida ..\analise_combusken
```

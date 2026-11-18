# Blaziken do Cobblemon: engenharia reversa do modelo 3D

Estudo de como o Cobblemon monta, texturiza e anima o Blaziken (o "galo de fogo" da franquia), para tirar
técnicas aplicáveis aos Cocorídeos, em especial ao Pirococó (#001). Feito em 18/11/2026 com
`ferramentas/analisar_geo.py`.

**Nada do Cobblemon foi copiado para este repositório.** Aqui ficam só medidas, contagens e técnicas
(fatos sobre o arquivo). Os arquivos originais e as imagens geradas ficam fora do Git (ver "Licença" e
"Como reproduzir").

## Resumo: o que vale levar para o Galetocraft
1. **Orçamento enxuto:** o Blaziken tem quase a mesma altura do Pirococó no jogo (2,90 x 2,80 blocos), mas
   usa **127 cubos e 470 faces** com textura **256x128**. O Pirococó usa **404 cubos e 2.313 faces** (4,9x mais)
   com textura 512x512. Os Cocorídeos vão de 687 (Taturicó) a 2.744 faces (Renacocó).
2. **Planos de espessura 0 fazem o detalhe:** 57% dos cubos do Blaziken são planos (2 faces em vez de 6):
   penas, chamas, sobrancelhas, olhos, pálpebras, garras, unhas e franjas dos pés. O Pirococó não tem nenhum plano.
3. **Pose de modelagem neutra, postura na animação:** o modelo é feito em pose T, com as pernas juntas. A
   inclinação do tronco, os braços caídos e os dedos fechados vêm da animação `ground_idle`. A pose pode ser
   ajustada sem refazer a geometria.
4. **Parado 100% em Molang:** o `ground_idle` não tem keyframes. São senoides com fases defasadas, e o loop
   de 8 s é o múltiplo comum dos períodos.
5. **Piscar com uma pálpebra escondida:** a pálpebra fica 0,09 px atrás do olho e a animação `blink` a empurra
   0,1 px para a frente por 0,17 s.
6. **Efeitos ligados e desligados por escala 0:** as chamas dos pulsos e dos pés são ossos próprios, com escala 0
   nas animações de passeio. Só aparecem na luta e nos ataques.
7. **Variantes baratas:** a versão shiny só troca a cor da mesma textura. O brilho do alfa é uma camada
   emissiva com 14 pixels. A fêmea é outro `.geo.json` em que só mudam 6 ossos.

## Fonte e licença
| item | valor |
|---|---|
| repositório | `gitlab.com/cable-mc/cobblemon`, tag **1.8.4** (commit `b79dbcc`, 27/10/2026, a mais recente) |
| licença dos modelos | arquivo `license` em cada pasta de modelo: Creative Commons **Atribuição-NãoComercial 3.0** (CC BY-NC 3.0) |
| licença do código | MPL 2.0 |
| personagem | Blaziken é propriedade de Nintendo / Game Freak / Creatures; os modelos do Cobblemon são arte de fã |

Consequência prática: estudar e medir é permitido, mas copiar a geometria, a textura ou a animação para um
Cocorídeo, mesmo adaptada, cria uma obra derivada sob CC BY-NC. Isso exigiria atribuição, impediria o uso
comercial e ainda tocaria na propriedade da Nintendo. Por isso este documento só registra **técnicas**.

## Arquivos e como o Cobblemon monta o Pokémon
Tudo fica em `common/src/main/resources/`:

| arquivo | papel |
|---|---|
| `data/cobblemon/species/generation3/blaziken.json` | ficha: `baseScale` **0,8**, hitbox 1,4 x 3,25, forma Mega, comportamento (imune a fogo, nada em lava) |
| `assets/cobblemon/bedrock/pokemon/resolvers/0257_blaziken/0_blaziken_base.json` | variante padrão: modelo `blaziken_male.geo`, textura normal; aspecto `shiny` troca a textura; `alpha_eyes` põe a camada **emissiva** `blaziken_alpha.png` |
| `.../resolvers/0257_blaziken/1_blaziken_female.json` | aspecto `female` troca só o modelo (`blaziken_female.geo`) |
| `.../posers/0257_blaziken/blaziken.json` | poses e quais animações cada uma toca (abaixo) |
| `.../models/0257_blaziken/blaziken_{male,female}.geo.json` | geometria Bedrock 1.12.0 |
| `.../animations/0257_blaziken/blaziken.animation.json` | 19 animações (428 KB) |
| `assets/cobblemon/textures/pokemon/0257_blaziken/blaziken{,_shiny,_alpha}.png` | texturas 256x128 |

**Poser** (máquina de poses): cada pose lista os tipos em que vale, uma condição em Molang, as animações em
camadas e as "quirks" (animações curtas aleatórias, aqui só o piscar).

| pose | quando | animações |
|---|---|---|
| `standing` | parado, retrato, perfil | `q.look('head')` + `ground_idle` |
| `walking` | andando sem correr (`!q.is_sprinting`) | `q.look('head')` + `ground_walk` |
| `running` | correndo; se montado (`q.is_ridden`), `ground_jog` | `q.look('head')` + `ground_run` |
| `battle-standing` | parado em batalha | `q.look('head')` + `battle_idle`; grito próprio `battle_cry` |
| `sleep` / `battle-sleep` | dormindo | `sleep` / `battle_sleep` (grito desligado) |

Fora das poses: `cry` e `recoil` com estado; `physical`, `special` e `status` como animação principal com a
curva `symmetrical_wide` (entrada e saída suaves). Retrato: escala 2,06; perfil: 0,42.

## Geometria
| | Torchic | Combusken | **Blaziken ♂** | Blaziken ♀ | Pirococó (nosso) |
|---|---|---|---|---|---|
| ossos | 63 | 60 | **102** | 102 | 63 |
| ossos sem cubo (só articulação) | 8 | 6 | **13** | 13 | 1 |
| profundidade máx. da árvore | 6 | 7 | **12** | 12 | 7 |
| cubos | 57 | 72 | **127** | 127 | 404 |
| faces desenhadas | 258 | 268 | **470** | 470 | 2.313 |
| planos (espessura 0) | 21 (37%) | 41 (57%) | **73 (57%)** | 73 | 0 |
| cubos girados no próprio pivô | 2 | 8 | **24** | 24 | 292 |
| inflate | 24 | 10 | **39** (0,01 / 0,02 / -0,01) | 39 | 0 |
| mirror | 7 | 0 | **11** | 11 | 0 |
| tamanhos fracionados | 0 | 0 | **0** | 0 | 404 |
| UV | caixa | caixa | **caixa (100%)** | caixa | por face (100%) |
| textura | 64x32 | 128x128 | **256x128** | 256x128 | 512x512 |
| cores na textura | 23 | 26 | **33** | 33 | 288 |
| textura coberta por UV | 77% | 17% | **35%** | 35% | 79% |
| altura no jogo, pose parada | 0,89 | 1,68 | **2,90** | 2,88 | 2,80 |

A complexidade cresce com a evolução: 57 → 72 → 127 cubos. Mesmo no topo, o Blaziken fica abaixo do Cocorídeo
mais leve (Taturicó, 120 cubos e 687 faces), porque metade dos cubos dele são planos.

### Esqueleto (resumido)
```
blaziken (raiz, só pivô)
└ body
  ├ waist ── body_fluff (plano)
  │  └ torso ── abdomen
  │     └ torso2 ── chest ── jacket_left / jacket_right (a "jaqueta" de penas do peito, 7 cubos cada)
  │        ├ neck ── head ── beak ── brow_*, face_* ── eye_* ── pupil_*, eyelid_*, eyelid_recoil_*, locator_eye_*
  │        │                       └ jaw
  │        │               └ hair ── hair_back, hairpos_* ── hair_* ── hair_*2 ── hair_*_end, hair_*_end2
  │        └ arm_* ── arm_*2 ── arm_*3 ── wrist_* ── hand_* ── finger_*1..9 (3 dedos x 3 falanges)
  │                                                 └ hand_fire_* ── hand_fire_*1..3 (3 planos em leque)
  ├ leg_* ── leg_*2 ── claw_* (espora), foot_* ── nail_*1..3, foot_fire_* ── foot_fire_*1..3
  └ tail1 ── tail2 ── tail3, locator_seat (montaria)
```

### Técnicas encontradas
- **Pose T e pernas juntas no repouso.** Na pose de modelagem, os braços ficam abertos na horizontal e as pernas
  formam uma coluna só. O `ground_idle` dá a postura: cintura +15°, tronco -12,5°, pernas abertas ±10,9° e dedos
  fechados (falange do meio a -87,5°). Com isso, todos os cubos ficam alinhados aos eixos e a pose muda só na animação.
- **Ossos sem cubo como articulação.** `wrist_*`, `hand_fire_*`, `foot_fire_*` e `hairpos_*` existem só para ter
  um pivô ou uma orientação extra. O `hairpos_*` gira 90°/±41° para que a "cabeleira" seja modelada reta dentro
  dele.
- **Rosto facetado com planos.** `face_left/right` são planos girados ±38,5° em Y: o rosto vira uma cunha, e o olho,
  num plano diagonal, é lido de frente e de lado. É a mesma ideia da "faceta diagonal" do olho do Pirococó, feita
  com 1 plano em vez de cubos.
- **Olho em camadas.** O olho é um plano em x=1,51, a pupila outro plano filho em x=1,52 (0,01 à frente) e a
  pálpebra um plano em x=1,42 (atrás, invisível) com inflate 0,01. O `blink` move a pálpebra +0,1 em X por
  0,125 s; ela passa à frente e cobre o olho. A `eyelid_recoil` é uma segunda pálpebra escondida, com outro
  desenho (olho apertado de dor), usada no `recoil`.
- **Inflate só para desempate.** Os valores são 0,01 ou 0,02 (e -0,01 em 3 cubos). O inflate não dá volume:
  tira o z-fighting entre peças que se tocam, como o plano da barriga sobre o abdômen.
- **Fogo em leque de planos.** Cada pulso tem 3 planos (0x10x8, 0x6x9, 0x7x9) girados ±60° e ±65°; cada pé tem
  3 planos grandes (0x14x20 e 16x12x0) abertos a 52,5°. As chamas são lidas de qualquer ângulo, com 6 faces por
  conjunto.
- **Franjas e garras como planos girados.** As franjas do pé são 4 planos girados (10x0x3 e 3x0x10). As unhas
  (0x3x2) e as esporas (0x2x4) também são planos, girados de 10° a 32,5°.
- **UV de caixa com mirror.** Dos 11 cubos com `mirror`, 7 reaproveitam a UV da peça da esquerda (pupila,
  pálpebra de dor e os 5 planos de fogo da direita). Os outros 4 usam o mirror só para virar o desenho.
- **UV negativa em planos.** Em 7 planos (jaqueta, ponta da cabeleira e o fogo grande dos pés), o UV começa
  acima da folha (v = -2 a -7). Num plano de largura 0, as faces de cima e de baixo têm largura 0, então só a
  frente e o verso caem dentro da textura e a faixa vazia não gasta espaço.
- **Locators.** `locator_eye_*` e `locator_seat` são ossos vazios que marcam pontos para partículas e para o
  assento do cavaleiro. O Blaziken pode ser montado: a pose `running` troca para `ground_jog` quando
  `q.is_ridden`.
- **Fêmea = 6 ossos diferentes.** A fêmea usa a mesma textura, a mesma UV e o mesmo esqueleto. Só a cabeleira
  encurta (11 → 10, 10 → 7, 10 → 9 px) e as sobrancelhas passam de 9 para 7 px.

### Textura
- 256x128, **33 cores**, pixel art com ruído: 3 a 5 tons por material (vermelho, creme, dourado e o cinza das
  mãos). As chamas usam laranja e amarelo saturados: (255,104,19), (255,157,33), (255,209,46) e (255,248,77).
- Ocupa só 35% da folha. O fogo dos pés são 3 planos, cada um com frente e verso desenhados lado a lado
  (6 "ladrilhos" de chama).
- **Shiny:** 8.574 dos 10.087 pixels opacos mudam, mas a UV é a mesma. O vermelho escurece (200,46,41 →
  129,30,30), o creme vira cinza-azulado (213,195,157 → 203,213,211) e o dourado satura. As chamas **não**
  mudam.
- **Alpha:** `blaziken_alpha.png` tem só 14 pixels opacos (rosa e vermelho, nos olhos), desenhados por cima
  como camada emissiva. É o equivalente ao nosso `_glowmask`.

## Animações
| animação | duração | loop | ossos | keyframes | canais Molang | observação |
|---|---|---|---|---|---|---|
| `ground_idle` | 8 s | sim | 47 | 0 | 17 | só senoides |
| `ground_walk` | 1 s | sim | 47 | 67 | 18 | pernas em keyframe, resto em Molang |
| `ground_jog` | 0,67 s | sim | 47 | 139 | 13 | trote, usado quando montado |
| `ground_run` | 0,5 s | sim | 42 | 207 | 13 | corrida com o tronco quase na horizontal |
| `blink` | 0,17 s | não | 3 | 9 | 0 | pálpebras |
| `cry` | 1,5 s | não | 18 | 92 | 0 | som `pokemon.blaziken.cry` em 0 s |
| `recoil` | 1,5 s | não | 15 | 73 | 0 | usa a `eyelid_recoil` |
| `sleep` | 8 s | sim | 64 | 198 | 54 | deitado de lado |
| `battle_idle` | — | sim | 54 | 2 | 35 | guarda de luta, chamas dos pulsos acesas |
| `physical` | 3 s | não | 64 | 893 | 89 | **salto mortal: o corpo gira até 690° em X**; a raiz estica 1,2 em Y ao aterrissar |
| `special` | 3 s | não | 73 | 703 | 100 | |
| `status` / `battle_cry` | 3 s | não | 65 | 687 | 47 | iguais; o `battle_cry` toca o som em 1,25 s |
| `battle_sleep` | 8 s | sim | 63 | 186 | 46 | |
| `render` | — | — | 50 | 0 | 0 | pose estática para retrato e imagem |
| `look` | — | — | 12 | 0 | 14 | distribui o olhar pela coluna |
| `walk_test` / `jog_test` / `run_test` | — | — | 1 | 0 | 1 | calibragem do passo (abaixo) |

Interpolação: 3.378 keyframes em `catmullrom` (curva suave) contra 487 lineares.

### Técnicas de animação
- **Período de uma senoide em Molang.** `math.sin(q.anim_time*90*k)` usa graus, então o período é **4/k s**.
  O Blaziken usa k = 0,5 (8 s), 1 (4 s), 2, 4 (1 s), 8 (0,5 s), 12, 16, 24 e 32. A duração do loop é o múltiplo
  comum: o parado tem 8 s porque há um termo com k = 0,5.
- **Defasagem em cascata (follow-through).** A cauda usa a mesma onda com fase -30°, -60° e -90° em
  `tail1/2/3`; o tronco usa -30° na cintura e -45° no peito e na cabeça. O movimento "escorre" da base para a ponta.
- **Andar = keyframes nas pernas + Molang no resto.** A perna direita é a esquerda atrasada 0,5 s, com Y e Z
  espelhados. Cintura, cauda, braços e cabeça balançam com k = 4 (uma vez por passada) e sobem e descem com k = 8
  (duas vezes por passada: um quique por pé).
- **Olhar distribuído.** `q.look('head')` gira a cabeça, e a animação `look` reparte o giro pela cintura, pelo
  tronco, pelo peito, pelo pescoço e pela cabeça (pesos 5, 15, 20, 15 e 35), com `math.clamp` para limitar.
  A cabeleira gira ao contrário (-20) para parecer que tem peso.
- **Calibrar o passo para o pé não escorregar.** As `*_test` só movem a raiz para trás a
  `-q.anim_time*16*4*0,75` px, ou seja, 4 blocos/s em escala 0,75. Tocadas junto com o andar no Blockbench,
  elas mostram se o pé "planta" no chão.
- **Peças ligadas e desligadas por escala.** `hand_fire_*` e `foot_fire_*` ficam com escala 0 no
  passeio e no parado e crescem na luta. A escala também é usada para expressão: no `special`, o peito e o
  abdômen incham (1,2 a 1,5) e as pupilas encolhem para 0,7.
- **Giros acima de 360°.** O `physical` anima a rotação X do corpo até 690° com catmullrom: quase dois
  giros, sem salto na interpolação.

### Erro encontrado no arquivo do Cobblemon
Em 3 expressões, repetidas 148 vezes (rotação Z de `hand_fire_*` em `sleep`, `battle_idle`,
`physical`, `special`, `status`, `battle_cry` e `battle_sleep`), falta o parêntese de fora:
`math.sin(q.anim_time*90*4-150)*1-1)+6*(math.sin(q.anim_time*90*2-90)*10`. O `analisar_geo.py` lê a
expressão como `(…)+6*(…)` e registra um aviso no relatório. Vale lembrar de validar o Molang ao exportar o
nosso `.animation.json`.

## Medidas por pose (Blaziken ♂, escala 0,8)
| pose | altura x largura x comprimento (blocos) |
|---|---|
| repouso (pose T) | 2,95 x 3,15 x 1,72 |
| `ground_idle` | 2,90 x 1,65 x 1,42 |
| `ground_walk` @ 0,25 s | 2,86 x 1,65 x 1,77 |
| `ground_run` @ 0,125 s | 2,04 x 1,71 x 2,96 |
| `battle_idle` | 2,67 x 2,32 x 2,27 |
| `physical` @ 1,2 s (no meio do mortal) | 4,53 x 1,56 x 2,92 |
| `sleep` @ 2 s | 1,62 x 2,01 x 2,29 |

## O que testar no Pirococó (sugestões, nada aplicado ainda)
| ideia | de onde vem | efeito esperado |
|---|---|---|
| Trocar penas finas (capa, juba, plumas da cauda) por planos de espessura 0 com textura recortada | 57% de planos no Blaziken | cada pena passa de 6 para 2 faces; é o caminho para chegar perto de 500–800 faces |
| Modelar em pose neutra e pôr a postura no `idle` | pose T + `ground_idle` | ajustar a postura sem regerar a geometria; o mesmo esqueleto serve para andar e lutar |
| Parado só em Molang com fases em cascata (crista → juba → capa → cauda) | `ground_idle`, cauda -30/-60/-90 | loop suave e infinito com poucos números |
| Piscar com pálpebra escondida + quirk aleatória | `eyelid_*` + `blink` | expressão viva com 2 planos |
| Crista de chamas e pontas de fogo em ossos próprios, com escala 0 fora de combate | `hand_fire_*`, `foot_fire_*` | "acende" na luta, combina com o `_glowmask` |
| Textura menor e com menos cores (paleta de 3–5 tons por material) | 256x128 com 33 cores | menos memória e um visual mais "Minecraft" |
| Validar o Molang ao exportar | erro de parêntese achado | evita uma animação quebrada sem aviso |

Pesar sempre contra a ficha: o Pirococó tem uma silhueta de armadura facetada que o Blaziken não tem. Medir com
`comparar_ficha.py` (IoU) e `benchmark.sh` antes de adotar qualquer item.

## Como reproduzir
Baixar só a linha do Torchic (34 arquivos), **numa pasta fora do repositório**. Funciona no Prompt do Windows
e no Linux:
```
git clone --filter=blob:none --no-checkout --depth 1 --branch 1.8.4 https://gitlab.com/cable-mc/cobblemon.git cobblemon
cd cobblemon
git sparse-checkout set --no-cone "/LICENSE" "**/0255_torchic/**" "**/0256_combusken/**" "**/0257_blaziken/**" "**/species/generation3/torchic.json" "**/species/generation3/combusken.json" "**/species/generation3/blaziken.json"
git checkout 1.8.4
```
Analisar (relatório, vistas por pose e mapa de UV), no Prompt do Windows, a partir da pasta do Galetocraft:
```
set C=..\cobblemon\common\src\main\resources\assets\cobblemon
python ferramentas\analisar_geo.py %C%\bedrock\pokemon\models\0257_blaziken\blaziken_male.geo.json %C%\textures\pokemon\0257_blaziken\blaziken.png --anim %C%\bedrock\pokemon\animations\0257_blaziken\blaziken.animation.json --pose ground_idle@0 --pose ground_walk@0.25 --pose battle_idle --pose physical@1.2 --pose sleep@2 --escala-jogo 0.8 --saida ..\analise_blaziken
```
Saem `relatorio.md`, `vistas_repouso.png`, `vistas_<pose>.png` e `uv_mapa.png`.
A mesma ferramenta lê os modelos do Galetocraft (`galetocraft/src/main/resources/assets/galetocraft/geckolib/...`),
que foi como saíram os números do Pirococó e dos outros Cocorídeos acima.

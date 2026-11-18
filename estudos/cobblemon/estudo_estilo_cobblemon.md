# Estudo: o estilo semi-voxel / low poly do Cobblemon

**Objetivo:** entender por que os modelos do Cobblemon funcionam tão bem dentro do Minecraft e transformar isso em
regras objetivas para modelar as criaturas do Galetocraft.

**Base:** este estudo junta duas coisas:

- **Os arquivos do Cobblemon, medidos um por um.** Baixei os assets do repositório público em 18/11/2026:
  - 1.170 modelos `.geo.json` de 906 espécies;
  - 759 posers, 1.010 arquivos de animação e 1.091 resolvedores;
  - 1.397 texturas;
  - os dados de espécie (escala e hitbox).
- **Uma pesquisa do que a comunidade e a própria equipe dizem** sobre o estilo: a seção 9.

**Imagens:** ficam em `estudos/cobblemon/imagens/`. Todas foram renderizadas por `ferramentas/render_geo.py`
direto dos arquivos do Cobblemon, na pose `ground_idle` do jogo.

**Licença:** os modelos do Cobblemon têm licença Creative Commons **não comercial** (há um arquivo `license` em cada
pasta). Este estudo usa os modelos **só como referência de técnica**. Nenhuma geometria, textura ou animação deles
entra no Galetocraft.

---

## 1. Resumo em 12 regras (o "DNA" do estilo)

1. **1 pixel de textura = 1 unidade do modelo, sempre.** Em 100% das 930 texturas conferidas, o PNG tem
   exatamente o tamanho declarado no modelo. No mundo, isso dá entre 1,0 e 1,8 pixel por "pixel do Minecraft"
   (mediana 1,25). É a mesma granulação dos mobs vanilla, e é o motivo nº 1 de o Pokémon "parecer do Minecraft".
2. **Cubos com tamanho inteiro** (99,9% dos 74.183 cubos). Só a posição é livre.
3. **Poucas peças.** São 57 cubos na mediana e 106 no p90. Aves grandes e lendários ficam entre 100 e 150.
   O detalhe mora na textura, não na geometria.
4. **Volumes primários grandes e limpos.** Cabeça e tronco costumam ser **uma caixa cada** (ver Torchic, Snorlax,
   Rowlet). Não há "escultura" de muitas caixinhas.
5. **Planos de espessura zero para tudo que é fino:**
   - o que são: penas, cristas, chamas, orelhas, cabelo, folhas, barbatanas e olhos;
   - quanto aparecem: 45% de todos os cubos são planos, e 99% dos modelos usam;
   - como o contorno é feito: a silhueta é **recortada em pixel** (transparência), não modelada.
6. **Rotação com moderação.** Só 11% dos cubos são girados. Os ângulos mais usados são 45° e, depois, inclinações
   pequenas: 5°, 10°, 15°, 7,5°, 2,5° e 20°.
7. **Rosto = caixa + olhos em peças próprias.**
   - **Olhos:** plaquinhas de 2×1 a 2×3 px, com pupila de 1×1 ou 1×2.
   - **Pálpebras e expressões:** pálpebras em ossos próprios, e cada expressão (feliz, bravo, triste, dor) é uma
     peça trocada.
   - **Camadas:** as peças do rosto ficam umas sobre as outras com `inflate` de 0,01 a 0,04, para não piscar
     (z-fighting).
8. **Cabeça pequena em adultos e grande em filhotes.**
   - **Aves adultas:** a cabeça tem 0,15–0,24 da altura e só 6–11 px de lado.
   - **Filhotes:** a cabeça ocupa 0,30–0,40 da altura.
   - **Olhos:** são minúsculos e lidos pelo contraste: branco, preto e um ponto de brilho.
9. **Textura pintada à mão com paleta curta.**
   - **Cores:** são 24 únicas por textura na mediana (p90 38), com 4–5 tons por material.
   - **Luz:** o topo é mais claro e a base, mais escura.
   - **Contorno:** não há contorno preto nas bordas. Pixels quase pretos são só 0,7% da textura na mediana.
   - **Grão:** há um leve granulado de pixels vizinhos (como a terra e as folhas do vanilla), sem degradê liso.
10. **Pernas de ave finas.** Têm 1–3 px de espessura, pés com dedos separados e garras em cubos pequenos.
11. **Animação procedural suave.**
    - **Como:** 56% dos canais de animação são expressões Molang (seno e cosseno), não quadros-chave.
    - **Amplitude:** pequena, de ±1–5° na respiração e 0,1–0,4 u de sobe e desce.
    - **Fase:** defasada em cadeia em caudas, penas e orelhas.
    - **Laço:** de 2 ou 4 s, sem emenda.
12. **Brilho e variações em camadas separadas.**
    - **Brilho:** chamas e olhos brilhantes vão numa textura extra emissiva (`emissive`, `alpha_eyes`).
    - **Variações:** shiny e formas trocam só a textura, sobre o mesmo modelo.

---

## 2. Escala: quão grande fica no mundo

O Cobblemon modela cada espécie num tamanho de trabalho e reduz no jogo com `baseScale`. O tamanho final é
**altura do modelo × baseScale ÷ 16** blocos.

| altura real da espécie | altura no jogo (mediana) | p10 – p90 |
|---|---|---|
| até 0,5 m | 0,68 bloco | 0,39 – 1,00 |
| 0,5 – 1 m | 1,01 | 0,56 – 1,58 |
| 1 – 1,5 m | 1,64 | 1,10 – 2,45 |
| 1,5 – 2,5 m | 2,69 | 1,61 – 3,64 |
| 2,5 – 5 m | 3,46 | 0,92 – 7,37 |

A curva é **jogo ≈ 1,47 × real^0,72**: os pequenos crescem e os gigantes encolhem, para tudo caber no mundo de
blocos e ainda ser lido. Exemplos com aves e criaturas de fogo:

| espécie | altura do modelo (u) | cubos | textura | baseScale | altura no jogo |
|---|---|---|---|---|---|
| Torchic | 24,5 | 56 | 64×32 | 0,6 | 0,92 |
| Combusken | 34,5 | 72 | 128×128 | 0,8 | 1,73 |
| Blaziken | 57,8 | 127 | 256×128 | 0,8 | 2,89 |
| Talonflame | 39,5 | 115 | 128×128 | 0,725 | 1,79 |
| Braviary | 40,6 | 152 | 256×128 | 0,8 | 2,03 |
| Moltres | 65,4 | 115 | 256×256 | 1,0 | 4,09 |
| Ho-Oh | 48,2 | 135 | 512×256 | 1,0 | 3,02 |
| Corviknight | 48,8 | 137 | 512×512 | 1,1 | 3,36 |
| Decidueye | 48,5 | 246 | 128×256 | 0,65 | 1,97 |

**Para o Galetocraft:** o GeckoLib desenha 1 unidade = 1/16 de bloco, sem `baseScale`. Basta modelar no tamanho
final, com 1 px por unidade. Isso cai em 1,0 pixel por pixel do Minecraft, dentro da faixa do Cobblemon. O
Pirococó (2,8 blocos) fica do porte de um Blaziken (2,9): um mítico grande.

---

## 3. Geometria: números de referência

| medida (1.170 modelos) | p10 | mediana | p90 |
|---|---|---|---|
| cubos | 26 | 57 | 106 |
| ossos (com localizadores) | 29 | 63 | 109 |
| menor lado dos cubos sólidos (u) | 1 | 2 | 3 |

| recurso | % dos cubos | % dos modelos que usam |
|---|---|---|
| planos (um lado = 0) | 44,8% | 99% |
| `inflate` | 35,7% | 99% |
| `mirror` | 15,9% | 68% |
| rotação no cubo | 11,0% | 71% |
| UV por face | 0% | 0% (tudo em UV de caixa) |

**Para que serve o `inflate`:**

| valor | uso |
|---|---|
| 0,01 (13.364 cubos), 0,02 e 0,03 | empilhar camadas sem piscar: olho sobre a cabeça, pálpebra sobre o olho |
| -0,01 e -0,1 | encolher uma peça escondida |
| 0,1 a 0,25 | engrossar um pouco uma parte sem mudar a textura |

**Onde ficam os planos:** olhos (1.421), caudas (1.134), pupilas, orelhas, cabeça, braços, boca aberta, pálpebras,
cabelo, asas abertas, folhas e cipós.

### Aves: medidas da cabeça, olhos, pernas e penas

| espécie | altura (u) | cabeça L×A×P (u) | cabeça / altura | olho (px) | pupila | perna (menor lado) | planos asa / cauda / crista |
|---|---|---|---|---|---|---|---|
| Torchic | 24,5 | 10×8×9 | 0,33 | 2×2 | — | 1 | 0/0/0 |
| Combusken | 35,5 | 7×7×7 | 0,20 | 2×3 | — | 2 | 0/0/0 |
| Fletchinder | 31,7 | 6×5×7 | 0,16 | 2×2 | 1×1 | 1 | 18/14/7 |
| Talonflame | 39,5 | 6×7×5 | 0,18 | 2×1 | 1×1 | 1 | 16/12/10 |
| Staraptor | 30,9 | 7×8×7 | 0,26 | 1×2 | 1×1 | 2 | 22/2/3 |
| Braviary | 40,6 | 11×6×6 | 0,15 | 2×2 | 1×1 | 3 | 4/5/52 |
| Pidgeot | 20,2 | 7×6×8 | 0,30 | 2×2 | 1×2 | 2 | 14/5/14 |
| Hawlucha | 30,5 | 8×11×9 | 0,36 | 1×4 | 1×2 | 3 | 2/0/37 |
| Corviknight | 48,8 | 19×10×11 | 0,20 | 1×2 | 1×1 | 3 | 8/6/8 |
| Moltres | 65,4 | 7×11×16 | 0,17 | 2×3 | 2×2 | 3 | 8/11/6 |
| Ho-Oh | 48,2 | 9×9×10 | 0,19 | 2×3 | 1×1 | 2 | 2/24/54 |
| Decidueye | 48,5 | 11×11×10 | 0,23 | 4×4 | 2×2 | 3 | 96/11/69 |

**Leitura:**

- A cabeça de uma ave de 40–65 u tem só 6–11 px de lado.
- O olho tem 2 px de largura, e às vezes 1 px de altura (cara séria).
- A expressão vem do contraste e da posição (sobrancelha e viseira por cima do olho), não da resolução.
- Cristas e penas grandes são feitas com **dezenas de planos** recortados (Braviary 52, Ho-Oh 54).

---

## 4. O rosto (a parte que mais vende o modelo)

Estrutura real do rosto do Talonflame (ossos e cubos):

```
head
 └ head_ai / head_angle  → cubo 6×7×5 (a cabeça inteira é UMA caixa)
    ├ crest, crest2, crest3 → planos 0×5×3 encadeados (crista que balança em cadeia)
    └ face → placa 6×5×2 (inflate 0.01) com a pintura do rosto
       ├ eyebrow → placa 6×6×1 (inflate 0.04): sobrancelha/máscara por cima dos olhos
       ├ mouth → beak 2×3×2 (inflate 0.15) + beak2 (ponta) + jaw 2×3×1 (abre no grito)
       └ eyes → eye_left/right 2×1×2 (inflate 0.02) → pupil 1×1×1, eye_emote
                 eyelid_left/right, eyelid_happy_*, eyelid_hurt_* (2×1×2, inflate 0.02–0.04)
```

**Como o piscar funciona:** a animação `blink` dura 1/6 s. Ela recua o olho 0,1 u e avança a pálpebra 0,1 u.
Como as duas placas estão separadas só por `inflate`, a que fica na frente "ganha" e o olho fecha. Não precisa de
escala nem de textura animada.

As expressões (feliz, bravo, triste, dor) são outras pálpebras ou olhos escondidos dentro da cabeça. A pose
mostra ou esconde cada um.

Imagem: `imagens/rostos_cabecas.png`. Veja o olho de 2 px do Talonflame e o olho 2×2 com 1 px de brilho do
Torchic.

---

## 5. Textura: como é pintada

Medido em 1.397 texturas: 24 cores únicas na mediana (p10 6, p90 38). Pixels quase pretos ocupam 0,7% da textura
na mediana. A diferença de luminância entre vizinhos é zero na mediana, ou seja, há áreas de tom chapado com
grão pontual. Exemplo: `imagens/texturas_exemplo.png`.

**A receita, vista nas texturas:**

- **4–5 tons por material:** luz, base, sombra 1, sombra 2 e acento.
- **Faixas de tom:** os tons mudam em faixas e manchas de pixel, nunca num degradê liso.
- **Luz de cima:**
  - o topo dos volumes e a parte de cima das faces laterais ficam mais claros;
  - a base e as junções (pescoço, axila, coxa) ficam mais escuras, como uma oclusão pintada.
- **Grão leve:**
  - pixels soltos de um tom vizinho, espalhados como na terra e nas folhas do vanilla;
  - nada de ruído aleatório forte nem filtro.
- **Sem contorno preto nas arestas:** a separação vem da diferença de tom entre as faces (o próprio
  sombreamento do Minecraft) e de um tom mais escuro na borda de penas e placas.
- **Padrões na textura:**
  - marcas, listras, escamas e penas pequenas são de 1–2 px;
  - penas e chamas são desenhadas em pixel art no plano, com a borda recortada por transparência.
- **Cores saturadas, mas não neon.** O brilho fica numa camada separada.

---

## 6. Animação e poses (o que dá "vida")

- **Posers:**
  - **Poses:** `standing` (743), `walking` (653), `sleep` (406), `battle-standing` (353) e, para quem voa,
    `fly`/`hover`.
  - **Peças por pose:** cada pose mostra ou esconde peças (`transformedParts`). Exemplo: a asa aberta e a asa
    fechada são **modelos diferentes** dentro do mesmo arquivo, e a pose escolhe qual aparece.
- **Animações mais comuns:**
  - `ground_idle`, `blink`, `cry`, `ground_walk`, `sleep`, `battle_idle`;
  - de reação: `recoil`, `happy`, `faint`, `sad`, `angry`.
- **Procedurais prontas:**
  - `q.look('head')`: a cabeça segue o olhar (2.656 usos);
  - `q.biped_walk`, `q.quadruped_walk`, `q.sine_wing_flap`, `q.pitch_tilt`.
- **Laço sem emenda:**
  - as fórmulas usam `q.anim_time*90*k` com `animation_length` 4, ou `*90*2k` com 2;
  - o período sempre divide a duração.
  - Exemplo de respiração do Talonflame: `torso.rotation.x = -50 - sin(t*180)*1`, com sobe e desce de
    `cos(t*180)*0.1`.
- **Andar:**
  - o tronco gira ±2–5° e sobe e desce 0,3 u;
  - as pernas alternam;
  - cauda e penas seguem com atraso de fase (-20°, -30°, -60°...).
- **Quirks:** piscar (`blink`) em intervalos aleatórios, em 2.540 poses.

---

## 7. Silhueta e leitura (o que se vê nas galerias)

`imagens/galeria_aves.png` e `imagens/galeria_geral.png` mostram:

- A silhueta oficial é preservada nas **massas grandes**: o topete do Torchic, a máscara do Talonflame e a crista do
  Braviary. O resto vira textura.
- **Exagero seletivo:**
  - o que identifica o personagem (cristas, orelhas, chamas, cauda) é grande e recortado;
  - o corpo é uma caixa simples.
- **Nada é liso:** curvas aparecem como degraus de pixel nas bordas recortadas e em poucas peças giradas.
- **Cores em blocos grandes:** dá para reconhecer cada criatura de longe só pelas manchas de cor.

---

## 8. O que isso muda para o Galetocraft

| tema | regra Cobblemon | aplicação no Galetocraft |
|---|---|---|
| densidade | 1 px por unidade | modelar no tamanho final; textura de 1 px por u, sem decalques em alta resolução |
| peças | 57 (mediana), até ~150 nos grandes | míticos de 2,5–3 blocos: 100–170 cubos; comuns: 40–90 |
| tamanho dos cubos | inteiros | inteiros; posição livre |
| detalhes finos | planos recortados | penas, chamas, cristas e lâminas como planos com recorte em pixel |
| rosto | caixa + placas de olho, pálpebra e expressão com `inflate` | idem; olho de 2×1 a 2×3 px |
| textura | 24 cores, 4–5 tons por material, luz de cima, sem contorno | idem; paleta da ficha, cada cor em 4–5 tons |
| brilho | camada emissiva separada | `_glowmask.png` + ossos com sufixo `_brilho` |
| animação | Molang seno/cosseno, laço de 2/4 s, cadeias defasadas | `animation.<id>.idle` e `.walk` no mesmo estilo |

---

## 9. Por que o estilo é bem recebido (pesquisa)

**Limites da pesquisa:**

- Wiki do Cobblemon, Modrinth, CurseForge e Reddit estavam bloqueados neste ambiente. O que vem da wiki saiu dos
  trechos mostrados pelo buscador; está marcado *(wiki, via busca)* e merece conferência.
- O que vem do repositório oficial (changelogs e JSON) foi conferido direto.
- **Não existe guia de arte oficial público.** A equipe só publica regras técnicas. As regras de estética vêm da
  medição (seções 1–7) e do que a comunidade diz.

### 9.1 O elogio central: "parece que sempre foi do Minecraft"

- **MMC Reviews:** "Cobblemon looks and feels right at home in Minecraft with the monsters' cubic models".
  Estética 4,5/5. https://mmcreviews.com/all/mods/cobblemon
- **ModDex:** os modelos "mesh extremely well into Minecraft without having to forgo important details" e o estilo
  "suits Minecraft a lot more than … pixelmon". https://moddex.gg/mod/cobblemon/reviews/2746
- **Sportskeeda:** texturas pixeladas e modelos em blocos "allowing them to blend in with Minecraft's environment".
  O site trata isso como escolha de estilo, não como falta de detalhe.
  https://sportskeeda.com/minecraft/cobblemon-vs-pixelmon-which-minecraft-pokemon-mod-better
- **Hostinger:** o Pixelmon tem modelos detalhados que parecem "menos Minecraft"; o Cobblemon mantém "the classic
  blocky style". https://www.hostinger.com/in/tutorials/cobblemon-vs-pixelmon

**Por que isso acontece, nos números:**

- A mesma densidade de pixel do vanilla (regra 1).
- Cubos inteiros (regra 2).
- Poucas peças (regra 3).
- Luz e cor pintadas como as texturas do jogo (regra 9).

O modelo não "briga" com o cenário de blocos.

### 9.2 A personalidade vem da animação

O changelog oficial mostra que isso é prioridade da equipe:

- piscar em muitas espécies e suporte a "quirks" para personalizados (1.3.0);
- animações de dormir e desmaiar;
- quirks raros, como as bolhas do Krabby que só aparecem no pôr do sol (1.5.0);
- Pokémon animados em qualquer tela de interface (1.6.0).

A comunidade criou até um mundo só para ver os modelos se mexendo. Um modelo parado e "morto" perde muito do
encanto.

### 9.3 Consistência é cobrada

O addon "Cobblemon Accessories & More" refaz modelos de outros addons para ficarem "more pixel consistent, low poly
and more accurate to the Minecraft style" (https://www.modpackindex.com/mod/128405/cobblemon-accessories-more). O
padrão do Cobblemon virou a régua: o que foge dele (mais resolução, curvas falsas, peças sub-pixel) é rejeitado.

### 9.4 Críticas, e o que aprender com elas

- **Menos fiel à aparência original que o Pixelmon.** O Pixelmon tem modelos e animações mais detalhados, e há
  quem troque os modelos por versões HD
  (https://www.modpackindex.com/modpack/91941/generations-forge-cobblemon).
  - **Lição:** compensar com silhueta muito fiel nas massas grandes e com animação viva, nunca com mais resolução.
- **Espécies com animação provisória ou modelo genérico** foram o ponto mais reclamado.
  - **Lição:** toda criatura sai com, no mínimo, parado, andar e piscar.

---

## 10. Como o sistema do Cobblemon funciona (pipeline de um Pokémon)

| peça | onde fica | o que faz |
|---|---|---|
| modelo | `bedrock/pokemon/models/<nnnn_nome>/<nome>.geo.json` | geometria Bedrock (ossos e cubos) |
| textura | `textures/pokemon/<nnnn_nome>/<nome>.png`, `_shiny.png`, `_alpha.png` | 1 px por unidade; shiny só troca a textura |
| animações | `bedrock/pokemon/animations/<nnnn_nome>/<nome>.animation.json` | `animation.<nome>.ground_idle`, `ground_walk`, `blink`, `cry`, `sleep`, `faint`, `battle_idle`, `air_*`, `water_*` |
| poser | `bedrock/pokemon/posers/<nnnn_nome>/<nome>.json` | poses (`standing`, `walking`, `sleep`, `fly`...); em cada uma, as animações, quirks e peças visíveis; também `rootBone` e enquadramento da interface (`portraitScale`, `profileScale`...) |
| resolver | `bedrock/pokemon/resolvers/<nnnn_nome>/0_<nome>_base.json` | liga espécie + aspectos (shiny, fêmea, forma regional) ao modelo, textura, poser e camadas (`emissive`, `alpha_eyes`, animadas com `frames`/`fps`) |
| espécie | `data/cobblemon/species/<geração>/<nome>.json` | status, golpes, `baseScale`, `hitbox {width, height}`, altura e peso |
| spawn | `data/cobblemon/spawn_pool_world/` | biomas e condições |

**Regras técnicas para modelos de addon** *(wiki, via busca; batem com as medições)*:

- **Projeto no Blockbench:** "Bedrock Entity", **UV de caixa** e densidade **16x**. Para modelos do Cobblemon, UV por
  face quebra o pacote.
- **Tamanhos:** inteiros. Posição, pivô, rotação e `inflate` podem ter decimais.
- **Nomes:** em minúsculas.
- **Orientação:** o modelo olha para o norte (-z).
- **Ossos obrigatórios:**
  - um osso raiz com o nome da espécie e pivô em (0, 0, 0), senão o modelo afunda no chão;
  - um osso `head`, para o olhar seguir o jogador.
- **Planos de espessura 0:** pintar também o verso.
- **Escala:** `baseScale` 1 = tamanho do Blockbench. Os pequenos são modelados maiores e reduzidos (0,5), o que dá
  mais pixel por bloco.

**Blocos e itens do mod** (conferido no repositório):

- 78 de 96 texturas amostradas são **16×16**, como no vanilla.
- O PC e a máquina de cura usam folhas de 64×64 na mesma densidade de 16 px por bloco, sem peças giradas.
- O estilo é "vanilla+": as mesmas regras de pixel do jogo base.

### Equivalência no Galetocraft (GeckoLib 5, Fabric 1.21.11)

| Cobblemon | Galetocraft |
|---|---|
| `.geo.json` Bedrock | **o mesmo formato** (`assets/galetocraft/geckolib/models/entity/<id>.geo.json`) |
| `.animation.json` com Molang | **o mesmo formato** (`geckolib/animations/entity/<id>.animation.json`). O jogo chama `animation.<id>.idle` e `animation.<id>.walk` em laço |
| poser (poses, quirks, peças visíveis) | não existe; a lógica fica no Java. O piscar pode ir dentro do `idle` como um evento rápido no fim do laço |
| `baseScale` | não existe; modelar no **tamanho final** (16 u = 1 bloco) |
| camada `emissive` | `textures/entity/<id>_glowmask.png` (mesmo layout, só os pixels que brilham) + ossos com sufixo `_brilho` |
| — | LOD do mod: ossos com sufixo `_lod1`, `_lod2` e `_lod3` somem a partir de 16, 32 e 48 blocos |
| UV de caixa obrigatório | UV de caixa recomendado (garante 1 px/u). O GeckoLib aceita UV por face, útil nos planos de uma face só |

---

## 11. Erros que tiram o modelo do estilo

**Técnicos** *(wiki)*:

- UV ou densidade errados;
- tamanho fracionado;
- maiúsculas nos nomes;
- pivô da raiz fora do zero;
- verso de plano sem pintura.

**Estéticos** *(guia "Minecraft Style Guide" do Blockbench, genérico, e as medições)*:

- **Mixels:** peças menores que 1 px, `inflate` exagerado ou texturas de densidades diferentes no mesmo modelo.
  É o erro nº 1.
- **Curva falsa:** girar várias peças vizinhas em ângulos crescentes para imitar uma curva. No estilo, a curva é um
  degrau.
- **Rotação sem motivo:** cada peça girada precisa de justificativa (pena, crista, membro).
- **Pintura errada:**
  - ruído de pincel ou filtro;
  - degradê liso com dezenas de tons;
  - contorno preto nas arestas.
- **Entulho:** muitas caixinhas empilhadas para fazer volume. Uma caixa bem pintada resolve.
- **Olho em alta resolução ou "decalque"** que destoa do resto. O olho do estilo tem 2–3 px.

---

## Fontes

**Repositório oficial:**

- https://gitlab.com/cable-mc/cobblemon: assets, dados e changelogs.
- https://gitlab.com/cable-mc/cobblemon-assets: fontes `.bbmodel`.

**Wiki** (via busca):

- https://wiki.cobblemon.com/index.php/Tutorials/Creating_A_Model
- https://wiki.cobblemon.com/index.php/Tutorials/Creating_A_Custom_Pokemon
- https://wiki.cobblemon.com/index.php/Poser
- https://wiki.cobblemon.com/index.php/Species
- https://wiki.cobblemon.com/index.php/Tutorials/Emissive_Textures
- https://wiki.cobblemon.com/index.php/Tutorials/Animated_Textures

**Guia de estilo do Blockbench:** https://blockbench.net/wiki/guides/minecraft-style-guide/

**Recepção** (links na seção 9):

- MMC Reviews, ModDex, Sportskeeda, Hostinger;
- PCGamesN, só pelo resumo do buscador;
- Modpack Index.

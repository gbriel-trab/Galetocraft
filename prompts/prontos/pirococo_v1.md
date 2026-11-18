# Pedido de modelagem — Galetocraft: Pirococó (pirococo)

Você vai criar o modelo 3D de uma criatura original do **Galetocraft**, um mod de Minecraft Java 1.21.11 (Fabric +
GeckoLib 5), no estilo **semi-voxel / low poly do mod Cobblemon**. A criatura é original. Não copie geometria,
textura nem animação de nenhum Pokémon ou do Cobblemon: o Cobblemon é só a referência de **técnica e acabamento**.

Leia tudo antes de começar. Este pedido tem 4 partes:

- **A.** O que entregar.
- **B.** O estilo (regras medidas em 1.170 modelos do Cobblemon).
- **C.** O formato técnico.
- **D.** Como trabalhar e se conferir.

No fim vêm a **ficha da criatura** (medidas e peças) e o **renderizador** que você deve usar para se conferir.

**Anexos desta conversa:**

- **A ficha 2D da criatura.** É a autoridade de **forma, cores e contagem de peças**.
- **Galeria de referência de estilo (opcional).** São renders de modelos do Cobblemon. Servem só para calibrar o
  acabamento.

**Prioridade quando houver conflito:**

1. Medidas: as da **ficha da criatura** (texto abaixo), não as da imagem.
2. Forma e cor: as da **imagem**.
3. Técnica: estas **regras de estilo**.

---

## A. O que entregar

Use execução de código (Python 3 com numpy e Pillow). **Não escreva o JSON à mão:** escreva um script gerador e
rode-o.

Entregue estes arquivos, com os nomes exatos:

1. **`pirococo.geo.json`:** geometria Bedrock, `format_version` `"1.12.0"`, identificador `geometry.pirococo`.
2. **`pirococo.png`:** a textura, a 1 pixel por unidade (ver C3).
3. **`pirococo_glowmask.png`:**
   - mesmo tamanho da textura;
   - transparente em tudo, menos nos pixels que brilham no escuro, que repetem a cor da textura.
4. **`pirococo.animation.json`:** `format_version` `"1.8.0"`, com **`animation.pirococo.idle`** e
   **`animation.pirococo.walk`** (as duas em laço). São os nomes exatos que o mod chama.
5. **`gerar_pirococo.py`:** o script que gera tudo, para que as correções futuras partam dele.
6. **Imagens de conferência** (feitas com o renderizador do fim):
   - `pirococo_vistas.png`: frente, os dois perfis, trás e 3/4, na pose do 1º quadro do `idle`;
   - `pirococo_comparacao.png`: cada vista da ficha ao lado do render na mesma altura;
   - `pirococo_rosto.png`: close da cabeça de frente e em 3/4.
7. **Relatório curto (até 15 linhas):**
   - número de cubos e de planos;
   - tamanho da textura;
   - lista de ossos;
   - o que ficou diferente da ficha e por quê.

No mod, os arquivos vão para estes lugares (só para você saber; não precisa criar as pastas):

- `assets/galetocraft/geckolib/models/entity/pirococo.geo.json`
- `assets/galetocraft/geckolib/animations/entity/pirococo.animation.json`
- `assets/galetocraft/textures/entity/pirococo.png` e `pirococo_glowmask.png`

---

## B. Regras de estilo (o "DNA" Cobblemon)

Estas regras saem da medição de 1.170 modelos e 1.397 texturas do Cobblemon. O motivo de o Cobblemon ser tão bem
recebido é um só: **parece que sempre fez parte do Minecraft**. Tudo abaixo serve a isso.

### B1. Densidade e tamanho

- **1 pixel de textura = 1 unidade do modelo**, sem exceção (16 u = 1 bloco = 16 px, como os mobs do vanilla).
  - Nada de decalques em alta resolução, olho "em HD" ou peças com mais pixels que o resto.
  - Densidade misturada (os "mixels") é o erro nº 1 do estilo.
- **Modele no tamanho final** (a altura está na ficha da criatura). O GeckoLib desenha 1 u = 1/16 de bloco.
- **Todo cubo tem tamanho inteiro** (99,9% no Cobblemon). Posição, pivô e rotação podem ter decimais.
- **Menor espessura:** 1 u para sólidos e 0 u para planos. Nada entre 0 e 1.

### B2. Volumes

- **Poucas peças, grandes e limpas.**
  - **Mediana do Cobblemon:** 57 cubos.
  - **Aves grandes e lendários:** 100–150 cubos.
  - **O orçamento desta criatura** está na ficha.
- **Cabeça e tronco são, de preferência, uma caixa cada**, com o detalhe resolvido na pintura.
  - Junte volumes sempre que der.
  - Pilhas de caixinhas para "esculpir" uma forma deixam o modelo entulhado.
- **Curvas são degraus.** Não gire várias peças vizinhas em ângulos crescentes para fingir uma curva.
- **Silhueta fiel nas massas grandes:**
  - o que identifica a criatura (crista, capa, cauda, armadura) é grande e legível;
  - o que é miúdo vira pintura.

### B3. Planos (espessura 0) para tudo que é fino

- **Onde usar:** penas, cristas, chamas, lâminas, franjas, tufos.
  - No Cobblemon, **45% dos cubos são planos**.
  - Uma crista grande usa de 10 a 50 planos.
- **Contorno:** a forma do contorno é **recortada em pixel** na textura (transparência). Ela não é modelada com
  várias caixas.
- **Composição:** arranje os planos em leque, em camadas e em ângulos diferentes, para terem volume de todos os
  lados. Um plano visto de perfil some, então cruze ou incline os importantes.

### B4. Rotação

- **Quanto:** no máximo ~15% dos cubos girados (Cobblemon: 11%).
- **Quais ângulos:** 45° e inclinações pequenas, de 2,5°, 5°, 7,5°, 10°, 15° e 20°. Prefira múltiplos de 2,5°.
- **Justificativa:** toda peça girada precisa de motivo, como uma pena que abre, uma crista que varre ou um membro.

### B5. Rosto (onde o dono mais repara)

- **Cabeça:** uma caixa, com a cara pintada na face da frente.
- **Olhos:**
  - plaquinhas próprias sobre a face, de **2×1 a 2×3 px**;
  - pupila de 1×1 ou 1×2;
  - 1 px de brilho quando o olho for maior que 2×2;
  - **contraste forte** (claro, escuro e brilho): é isso que faz um olho de 2 px ser lido de longe.
- **Camadas sem piscar:** peças do rosto sobrepostas (olho sobre a cabeça, pálpebra, sobrancelha, viseira) usam
  `inflate` de **0,01 a 0,04**.
  - O `inflate` serve só para isso; nunca para mudar o tamanho de uma peça.
- **Piscar:**
  - a pálpebra é uma plaquinha do tamanho do olho, logo atrás dele (`inflate` menor);
  - na animação, ela avança ~0,1–0,15 u por ~0,15 s e cobre o olho.
- **Expressão:** vem da **posição** da sobrancelha ou viseira por cima do olho (inclinada para dentro = séria ou
  brava) e do formato do olho, não de resolução.
- **Bico:** 2 ou 3 caixas em degrau (base, meio e ponta/gancho), com mandíbula separada se a boca abrir.

### B6. Pintura da textura (o "acabamento Cobblemon")

- **Paleta curta:**
  - cerca de **24 cores no total** (o p90 do Cobblemon é 38);
  - **4 a 5 tons por material** (luz, claro, base, sombra e sombra funda);
  - parta das cores da ficha;
  - nas sombras, puxe o tom para um matiz vizinho mais frio e saturado; nas luzes, para um mais quente e claro;
  - nunca escureça só para o preto.
- **Luz de cima, pintada em faixas:**
  - o terço de cima de cada volume vai 1 tom mais claro e a base, 1 tom mais escura;
  - nas junções (pescoço, axilas, coxas, sob a capa e sob placas), uma faixa de 1 px de sombra funda.
  - **Nada de degradê liso:** a troca de tom é em degrau de pixel.
  - O próprio Minecraft já escurece as faces laterais (lados 0,6, frente 0,8, baixo 0,5), então não escureça
    demais as faces laterais na textura.
- **Grão leve:**
  - ~5–10% dos pixels de uma área mudam 1 tom para cima ou para baixo, em manchinhas de 1–3 px (como a terra e as
    folhas do vanilla);
  - use uma semente fixa;
  - sem ruído forte nem filtro.
- **Sem contorno preto nas arestas.** A separação entre volumes vem do tom. Use 1 px mais escuro só na borda de
  baixo de penas e placas sobrepostas, e 1 px mais claro na aresta de cima das placas de armadura (chanfro pintado).
- **Padrões na pintura:** listras, escamas, chevrons de pena e filetes de 1–2 px, sem geometria.
- **Planos (penas, chamas):**
  - pixel art com recorte;
  - uma linha de "haste" 1 tom diferente;
  - pontas em degrau;
  - raiz 1–2 tons mais escura que a ponta.
- **Brilho:** só no `_glowmask` (gemas, chamas e pontas de fogo, se a ficha pedir). A textura base continua com as
  cores normais.

### B7. Animação (o que dá vida)

- **Procedural, com Molang:**
  - o Cobblemon faz 56% dos canais com seno e cosseno;
  - use `query.anim_time` e `math.sin`/`math.cos`, que recebem **graus**.
- **Laço sem emenda:**
  - com `animation_length` L, cada onda é `math.sin(query.anim_time*(360/L)*k + fase)`, com k inteiro;
  - idle: L = 4 → `query.anim_time*90*k`;
  - walk: L = 2 → `query.anim_time*180*k`.
- **Amplitudes pequenas:**
  - **Respiração:** o tronco gira ±1–2° e sobe e desce 0,1–0,3 u.
  - **Cabeça:** ±2–3°.
  - **Cristas, penas e capa:** ±3–6°.
- **Cadeias (cauda, tranças, penas longas):**
  - cada segmento recebe a mesma onda, com **atraso de fase** crescente (−20° a −40° por segmento);
  - a amplitude também cresce um pouco para a ponta.
- **Andar (walk):**
  - pernas alternadas, ±20–30° em x;
  - o pé compensa a rotação da perna, para ficar quase plano no chão;
  - o corpo sobe e desce 0,3–0,5 u (2 vezes por ciclo) e balança ±2–4° em z e y;
  - cauda e capa seguem com atraso.
- **Piscar dentro do idle:** 1 vez por laço de 4 s. A pálpebra cobre o olho entre ~3,70 s e ~3,85 s, com
  keyframes juntos para ser quase instantâneo.

### B8. O que NÃO fazer (motivos de reprovação)

- Densidade diferente de 1 px por unidade em qualquer peça, ou tamanho de cubo fracionado.
- Contorno preto, degradê liso com muitos tons, ruído forte, aspecto "pintura digital".
- Entulho: caixinhas empilhadas, dezenas de peças onde uma caixa pintada resolve.
- Curva falsa com peças giradas em sequência.
- Planos com as **duas** faces no mesmo lugar (piscam no jogo; ver C3).
- Rosto disforme: olho dividido entre duas faces em degrau, olho fora de proporção, cara "derretida".
- Partes atravessando outras na pose do idle ou durante o walk (confira o 1º quadro e o meio do walk).
- Penas e cristas finas que somem quando vistas de lado.
- Mudar as cores da ficha, ou inventar elementos que a ficha não tem.

---

## C. Formato técnico (GeckoLib 5 / Bedrock)

### C1. Coordenadas

- **Unidade:** 16 u = 1 bloco.
- **Eixos:**
  - **y** para cima, com o **chão em y = 0** (os pés tocam y = 0);
  - **x**: centro em 0. **x negativo = lado DIREITO da criatura** (sufixo `_d`); x positivo = esquerdo (`_e`);
  - **z**: a **frente** (bico/rosto) fica em **z negativo**.
- **No JSON do cubo:** `origin` é o canto mínimo (x, y, z) e `size` é o tamanho.
- **Rotações:** em graus, em volta do `pivot`. Para conferir o sentido, renderize. Não confie na intuição.

### C2. Esqueleto do `.geo.json`

```json
{
  "format_version": "1.12.0",
  "minecraft:geometry": [{
    "description": {
      "identifier": "geometry.pirococo",
      "texture_width": 128, "texture_height": 128,
      "visible_bounds_width": 4, "visible_bounds_height": 4, "visible_bounds_offset": [0, 1.5, 0]
    },
    "bones": [
      {"name": "pirococo", "pivot": [0, 0, 0]},
      {"name": "corpo", "parent": "pirococo", "pivot": [0, 15, -1], "cubes": [
        {"origin": [-5, 15, -8], "size": [10, 14, 11], "uv": [0, 0]}
      ]},
      {"name": "pena_x", "parent": "corpo", "pivot": [0, 20, 3], "rotation": [-15, 0, 0], "cubes": [
        {"origin": [-3, 10, 3], "size": [6, 10, 0], "uv": {"north": {"uv": [40, 0], "uv_size": [6, 10]}}}
      ]}
    ]
  }]
}
```

- **Osso raiz** com o nome da criatura e pivô (0, 0, 0). Todo o resto descende dele.
- **Nomes:** minúsculos, sem acento, `snake_case`. Use os nomes de ossos da ficha da criatura, porque a animação
  depende deles.
- **Brilho:** ossos cujo nome termina em **`_brilho`** (ex.: `gema_testa_brilho`) são os únicos redesenhados com o
  `_glowmask`. Ponha neles só os cubos que brilham.
- **Opcional, detalhe de longe:** ossos terminados em `_lod1` somem a partir de 16 blocos e `_lod2`, a partir de 32.
  Use em garras, contas e filetes miúdos.
- `visible_bounds`: cubra o modelo inteiro (largura e altura em blocos, com folga).

### C3. UV e textura

- **Sólidos (as 3 medidas ≥ 1): UV de caixa** (`"uv": [u, v]`), o padrão do Cobblemon. Ele garante 1 px por u.
  - **Tamanho da ilha:** num cubo de tamanho (w, h, d) = (x, y, z), ela ocupa **(2d + 2w) × (d + h)** pixels a
    partir de (u, v).
  - **Linha de cima:** `(u+d, v)` = **topo** (w×d); `(u+d+w, v)` = **base** (w×d).
  - **Linha de baixo**, a partir de y = v+d, da esquerda para a direita:
    - **lado direito da criatura** (−x), d×h;
    - **frente** (−z), w×h;
    - **lado esquerdo** (+x), d×h;
    - **trás** (+z), w×h.
  - **Confira a orientação:** antes de pintar de verdade, pinte cada face de uma cor com uma seta e renderize.
  - `"mirror": true` espelha a ilha. Serve para reaproveitar a mesma pintura no lado oposto, se for idêntica.
- **Planos (uma medida = 0): UV por face com UMA face só**, do tamanho exato do plano em pixels.
  - **Qual face:** plano em z → `north`; plano em x → `east`; plano em y → `up`.
  - **Por quê:** o GeckoLib desenha sem descarte de face traseira, então essa única face aparece dos dois lados.
    Se o plano tiver as duas faces no mesmo lugar, elas **piscam** (z-fighting).
- **Tamanho da textura:** potência de 2 (ex.: 128×128 ou 256×128), declarado igual em `texture_width`/`height` e no
  PNG.
- **Ilhas:** empacotadas sem sobreposição, com o fundo transparente.
- **Densidade:** **`uv_size` = tamanho da face** sempre. Verifique isso no script.

### C4. `.animation.json`

```json
{
  "format_version": "1.8.0",
  "animations": {
    "animation.pirococo.idle": {"loop": true, "animation_length": 4, "bones": {
      "corpo": {"rotation": ["math.sin(query.anim_time*90*2)*1.5", 0, 0],
                "position": [0, "math.sin(query.anim_time*90*2)*0.2", 0]}
    }},
    "animation.pirococo.walk": {"loop": true, "animation_length": 2, "bones": {
      "perna_d": {"rotation": ["math.sin(query.anim_time*180)*25", 0, 0]},
      "perna_e": {"rotation": ["math.sin(query.anim_time*180+180)*25", 0, 0]}
    }}
  }
}
```

- Rotações em graus e posições em unidades, **somadas** à pose do modelo.
- Os keyframes de piscar podem ser `{"0.0": [0,0,0], "3.7": [0,0,0], "3.72": [0,0,-0.12], ...}`.

---

## D. Como trabalhar (obrigatório)

1. **Leia a ficha 2D e a ficha da criatura.** Liste para si:
   - as massas grandes;
   - os marcos de altura;
   - as contagens de peças;
   - a paleta.
2. **Monte o script gerador** com funções pequenas:
   - `caixa()` e `plano()`, que montam o cubo e reservam a ilha de UV;
   - `osso()`;
   - um empacotador de UV;
   - materiais (rampas de 4–5 tons);
   - pintores por face.
   - Salve o `.geo.json`, o `.png`, o `_glowmask.png` e o `.animation.json`.
3. **Rodada 1 — SILHUETA:** só as massas grandes, pintadas com a cor base.
   - Renderize e compare com as vistas da ficha.
   - Ajuste até as alturas dos marcos baterem (±0,5 u).
4. **Rodada 2 — CABEÇA e ROSTO:** caixa da cabeça, olhos, viseira, bico e crista. Faça o close do rosto e compare.
5. **Rodadas 3–4 — ELEMENTOS DA IDENTIDADE:** armadura, capa, cauda, pés etc., na ordem da ficha da criatura.
6. **Rodada 5 — PINTURA:** rampas, faixas de luz, oclusão nas junções, grão, padrões e recortes dos planos.
7. **Rodada 6 — ANIMAÇÃO:**
   - renderize o 1º quadro do idle e confira se nada atravessa nada;
   - confira também o walk no instante t = 0,5 s. O renderizador aceita qualquer nome de animação e usa o 1º
     quadro, então crie temporariamente uma animação com os valores de t = 0,5 para conferir.
8. **Faça pelo menos 6 rodadas, OLHANDO as imagens a cada uma.** Corrija primeiro o que mais muda a semelhança, nesta
   ordem:
   1. silhueta;
   2. cabeça;
   3. elementos característicos;
   4. cor;
   5. detalhe.
9. **Validações automáticas no script** (imprima o resultado):
   - todos os `size` são inteiros;
   - `uv_size` é igual ao tamanho da face;
   - as ilhas não se sobrepõem;
   - o PNG tem o tamanho declarado;
   - planos têm uma face só;
   - a altura total bate com a ficha (±0,5 u);
   - o número de cubos está no orçamento;
   - os nomes dos ossos usados na animação existem;
   - `idle` e `walk` estão em laço.
10. **Entregue os arquivos da seção A** e o relatório.

### Autoavaliação antes de entregar (nota de 0 a 10 em cada item; refaça o que ficar abaixo de 8)

1. Silhueta e proporções (frente e perfil) contra a ficha.
2. Cabeça e rosto: olho legível, expressão certa, bico.
3. Elementos característicos da criatura (ver a ficha da criatura).
4. Fidelidade de cores à paleta.
5. Acabamento Cobblemon: 1 px/u, sem mixels, sem entulho, pintura em faixas, sem contorno preto.
6. Animação: viva, sutil, sem emenda, sem peças atravessando.

---

## Ficha da criatura — Pirococó (#001), "O Galo Fênix"

**Quem é:** um mítico do tipo fogo. É uma ave de rapina nobre e imponente, com cerca de 5 cabeças de altura (não é
filhote nem chibi), e usa armadura prateada de cavaleiro. Os elementos que o identificam de longe:

- **Juba de penas vermelhas** em chama, em volta de um rosto pequeno e afiado.
- **Elmo-tiara prateado** com gema rubi na testa.
- **Colar em V prateado** com gema no peito.
- **Ombreiras** que abrem como asas, com ponta dourada.
- **Capa de penas em sino:** roxa em cima e vermelha embaixo.
- **Pernas longas e finas** com joelheira e tornozeleira prateadas.
- **Garras douradas.**
- **3 tranças douradas** caindo para trás, cada uma terminando numa pena-lâmina.

**Expressão:** a neutra da ficha ("NORMAL"), séria e determinada.

### Escala e orçamento

| item | valor |
|---|---|
| altura total (chão → ponta da crista) | **45 u** (2,8 blocos) |
| largura máxima (capa, na frente) | ~29 u |
| comprimento (ponta do bico → ponta da cauda) | ~36 u |
| cubos | **110–170** (teto 200), dos quais ~40–50% planos |
| textura | 128×128 ou 256×128 (no máximo 256×256), 1 px por u |

### Divisão vertical (y a partir do chão)

| faixa | y (u) |
|---|---|
| crista acima do elmo | 39 → 45 |
| cabeça (topo do elmo → queixo) | 31 → 39 |
| pescoço visível / colar | 29,5 → 31 |
| tronco (colar → quadril) | 15 → 29,5 |
| coxas (saia de penas vermelhas) | 10,5 → 15 |
| perna visível (joelho → chão) | 0 → 10,5 |

**Marcos:**

| marco | y (u) |
|---|---|
| ponta das 2 penas externas em U | 45 |
| pena central da crista | 42 |
| topo do elmo / topo da gema da testa | 39 |
| linha dos olhos | 35 |
| bico (base → ponta do gancho) | 34 → 30,5 |
| colar e topo das ombreiras | 29,5 |
| pontas das ombreiras | 29 → 26 |
| gema do peito | 28 → 23 |
| ponta do V do peitoral | 21,5 |
| joelheira | 10,5 → 8,5 |
| canela | 8,5 → 5,5 |
| tornozeleira | 5,5 → 3,5 |
| pé + dedos | 3,5 → 0 |
| barra da capa | 1,5 (não encosta no chão) |

### Larguras (x, vista de frente)

| peça | largura (u) |
|---|---|
| juba (crista + chamas laterais), máx. em y ≈ 37 | 15 |
| par de penas em U | 9 |
| cabeça | 7–8 |
| gema da testa | 2 × 4 (losango vertical) |
| bico | 3 de largura na base |
| pescoço | 5 |
| ombreiras (ponta a ponta) | 21 |
| peitoral | 10 |
| peito creme visível | 7 |
| capa | sino: 21 no ombro → 29 em y ≈ 9 → 27 na barra |
| pernas | centros em x = ±2,6 |
| coxa | 3–4 |
| joelheira / tornozeleira | 3 |
| canela | 2 (**não engrossar**) |
| cada pé | ~6, com os dedos abertos |

### Profundidades (z; 0 = quadril; frente negativa)

| peça | z (u) | nota |
|---|---|---|
| ponta do bico | −11 | |
| bico | −11 → −6,5 | |
| cabeça | −6,5 → 0 | |
| frente do peitoral | −9,5 | o peito estufa quase até a linha do bico |
| tronco | −9,5 → +2,5 | |
| crista | −5 → +12 | varre para trás; a pena mais alta fica em z ≈ +2,5 |
| capa: borda de trás | até +13,5 (em y ≈ 7) | |
| pé | −8 → +1,5 | 3 dedos na frente, 1 atrás |

**Cauda:** a raiz das 3 tranças fica em z = +3,5, com y entre 23,5 e 25,5 (alto das costas, logo abaixo da capa).
As pontas:

| trança | ponta (z, y) |
|---|---|
| A (alta) | (+24,5, 16,5) |
| B (média) | (+23,5, 4,5) |
| C (baixa) | (+19,5, 1,5) |

**Perfil em S:** a cabeça vai para a frente, o peito estufa e a capa e a cauda descem para trás.

### Peças e como fazer

| parte | o que a ficha mostra | como fazer |
|---|---|---|
| crista / juba | 2 penas externas em U (as mais altas, com a ponta curvando para dentro), 1 central, ~3 chamas por lado e ~3 tufos de bochecha por lado; de lado, 5 lâminas varridas para trás | leque de planos recortados (20–30 planos), em vários ângulos para ter volume de frente e de lado; vermelho em 4–5 tons, raiz escura e pontas claras |
| elmo | tiara prateada com 2 asas que sobem para trás e gema rubi vertical no centro; viseira prateada por cima dos olhos | placa prateada sobre a caixa da cabeça (`inflate` 0,02–0,04); gema 2×4 com facetas pintadas, em osso `_brilho` |
| olhos | estreitos, inclinados para dentro, íris vermelho-escura, cara séria | plaquinhas de 2×1 px na face da frente; a viseira passa inclinada por cima; pálpebra para piscar |
| bico | gancho de rapina dourado | 2–3 caixas em degrau (base 3×3, meio, gancho caído); mandíbula separada |
| colar e peitoral | V prateado em 2 camadas, gema losango no centro | 2 placas em V; gema saltada, em osso `_brilho` |
| ombreiras | prata com miolo roxo e ponta dourada | 2–3 placas por lado; a de fora inclinada ~20° para cima e para fora |
| peito | creme com 2–3 chevrons de pena | pintura (não geometria) |
| capa / asas | 3 camadas de penas: roxa com filetes prata (~4 por lado), roxa → vermelha (~5) e vermelha comprida (~6) | planos recortados em ponta, em leque, presos em `asa_d` e `asa_e`. **Não cobre a frente do peito:** a capa abre dos ombros para trás e para os lados |
| coxas | saia de penas vermelhas (3–4 por coxa) | uma caixa vermelha + planos recortados por cima |
| pernas | joelheira prata pontuda, canela roxa, tornozeleira prata | caixas de 3 / 2 / 3 u |
| pés | roxo-escuro escamado, 3 dedos na frente + 1 atrás, garras douradas grossas | dedos em caixas de 1–2 u; garra dourada caída na ponta |
| cauda tripla | 3 tranças douradas, cada uma com uma pena-lâmina dourada e um losango roxo no fim | 5–6 segmentos de 2×2×3–4 u por trança, alternando giros de 45° no eixo da trança para ler como trança; lâmina plana de 5–6 u no fim |

**Atenção:**

- As penas em U da crista são **vermelhas**. Não há chifres dourados.
- A armadura é **prateada** (com um leve tom lilás), não dourada nem roxa.
- O dourado aparece só no bico, nas garras, nas tranças e nas pontas das ombreiras.

### Ossos e pivôs

| osso | pai | pivô (x, y, z) | animação |
|---|---|---|---|
| `pirococo` | — | (0, 0, 0) | raiz |
| `corpo` | pirococo | (0, 15, −1) | respiração, balanço do andar |
| `pescoco` | corpo | (0, 29, −4) | |
| `cabeca` | pescoco | (0, 31,5, −3,5) | olhar e balanço leve |
| `crista` | cabeca | (0, 38,5, −2) | ondula com atraso |
| `olhos`, `palpebra_d`, `palpebra_e` | cabeca | — | piscar |
| `asa_d` / `asa_e` | corpo | (−5 / +5, 28,5, 0) | a capa; balança leve |
| `cauda` | corpo | (0, 24,5, +3,5) | |
| `cauda_a_0..5`, `cauda_b_0..5`, `cauda_c_0..5` | cauda (em cadeia) | na junta de cada segmento | ondulam com fase crescente |
| `perna_d` / `perna_e` | pirococo | (−2,6 / +2,6, 15, 0) | andar |
| `pe_d` / `pe_e` | perna | (∓2,6, 3,5, −1) | compensa a perna no andar |

Ossos de brilho (por exemplo `gema_testa_brilho`, `gema_peito_brilho`, `losango_a_brilho`) ficam dentro dos ossos
acima. **O que brilha:** só as gemas da testa e do peito e os losangos roxos das lâminas da cauda.

### Paleta (da ficha) e rampas sugeridas (luz → sombra funda)

| material | luz | claro | **base** | sombra | sombra funda |
|---|---|---|---|---|---|
| vermelho (crista, plumagem, coxas, barra da capa) | #ff5b3f | #ef392d | **#dd1c20** | #b90c27 | #960429 |
| creme (rosto, garganta, peito) | #fff6e0 | #ffeed1 | **#fde1c0** | #d9b398 | #b68b78 |
| roxo (capa de cima, canelas) | #a0499e | #88398e | **#702a7c** | #491847 | #300e34 |
| roxo-escuro (pés, sombras) | #5b2354 | #491847 | **#3a1239** | #2c0c2e | #210826 |
| prata (armadura) | #f6f6f6 | #e4dce3 | **#d2bed1** | #ac93ae | #86708b |
| dourado (bico, garras, tranças) | #ffe138 | #ffcd29 | **#fcb419** | #d87b08 | #b55100 |
| rubi (gemas, losangos) | #da3879 | #c82775 | **#b61972** | #920b6a | #6f0459 |
| olho (íris) | — | #e8352b | **#9e1020** | #5a0812 | — |

O olho leva ainda 1 px de pupila #210826 e, se o olho tiver mais de 2 px, 1 px de brilho #fff6e0.

### Animação desta criatura

**idle (L = 4):**

- **Corpo:** respira com rotação em x de ±1,5° e sobe e desce 0,2 u.
- **Cabeça:** ±2° em x e ±3° em y, defasada do corpo.
- **Crista:** ±4°, atrasada da cabeça.
- **Capa** (`asa_d`/`asa_e`): ±2° em z, espelhada entre os lados.
- **Tranças:** ondulam em x e z com ±4–8°, com atraso de −30° por segmento.
- **Piscar:** 1 vez no fim do laço.

**walk (L = 2):**

- **Pernas:** ±25° alternadas; os pés compensam.
- **Corpo:** sobe e desce 0,4 u, 2 vezes por ciclo, e balança ±3° em z.
- **Cabeça:** contrabalança, ficando mais estável que o corpo.
- **Capa:** acompanha com atraso.
- **Tranças:** com mais amplitude que no idle.

### Pontos de reprovação específicos desta criatura

- Cabeça grande demais (fofa) ou rosto genérico de galinha. É uma ave de rapina séria.
- Pernas grossas ou curtas: a perna visível tem 10,5 u (23% da altura).
- Capa fechada na frente, escondendo o colar e o peito creme.
- Tranças fundidas numa peça só, ou sem a lâmina na ponta.
- Pés gigantes. O desenho 2D exagera as garras em perspectiva: use as medidas acima.

---

## Apêndice — renderizador de conferência (`render_geo.py`)

Salve como `render_geo.py` e use-o assim:

```
python render_geo.py pirococo.geo.json pirococo.png pirococo_vistas.png pirococo.animation.json animation.pirococo.idle 8
```

O que ele faz:

- desenha 5 vistas (frente, perfis, trás e 3/4) com z-buffer;
- aplica o 1º quadro da animação;
- usa o sombreamento de entidade do Minecraft;
- não descarta faces traseiras, igual ao GeckoLib.

Para o close do rosto, recorte a vista ampliada. Para a comparação, ponha cada vista da ficha ao lado do render na
mesma altura em pixels.

```python
"""Renderiza um modelo Bedrock/GeckoLib (.geo.json + textura .png) em 4 vistas, sem Blockbench.

Independente do resto do projeto: só precisa de numpy e Pillow. Serve para revisar modelos (os nossos e os
gerados por outros chats) e é o mesmo código que vai no prompt de modelagem.

- Lê bones (pivot, rotation, parent), cubes (origin, size, inflate, rotation, pivot, mirror) e UV em caixa
  ("uv": [u, v]) ou por face ("uv": {"north": {"uv": [..], "uv_size": [..]}, ...}).
- Converte para o espaço do Blockbench (x invertido), igual ao Blockbench ao importar.
- Opcional: aplica o 1º quadro de uma animação (ex.: animation.<id>.idle). Só valores numéricos; expressões
  Molang viram o seu valor em q.anim_time = 0 (sin/cos em graus, como no Molang).
- Vistas: frente (rosto para a câmera), lado direito da criatura (frente apontando para a direita da imagem),
  trás, lado esquerdo e 3/4.
- Sombreamento de entidade do Minecraft: topo 1,0; frente/trás 0,8; lados 0,6; baixo 0,5.
- Desenha as faces dos dois lados (sem culling), como o GeckoLib: planos aparecem por trás e faces
  coincidentes piscam aqui também.

Uso: python ferramentas/render_geo.py modelo.geo.json textura.png saida.png [animacao.json nome_da_animacao] [escala]
"""
import ast
import json
import math
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def rot(rx, ry, rz):
    """Matriz de rotação em graus, ordem do Blockbench: R = Rz·Ry·Rx."""
    a, b, c = (math.radians(v) for v in (rx, ry, rz))
    Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    Rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def em_volta(A, pivo, t=(0, 0, 0)):
    """Transformação afim (A, b) que aplica A em volta do pivô e depois translada t."""
    p = np.array(pivo, float)
    return A, p - A @ p + np.array(t, float)


def compor(M, N):
    """M(N(p))."""
    return M[0] @ N[0], M[0] @ N[1] + M[1]


NORMAL = {"north": (0, 0, -1), "south": (0, 0, 1), "east": (1, 0, 0), "west": (-1, 0, 0), "up": (0, 1, 0), "down": (0, -1, 0)}


def canto(face, f, t, u, v):
    """Ponto da face na posição (u, v) de 0 a 1, com (0, 0) no canto de cima à esquerda da textura."""
    (x1, y1, z1), (x2, y2, z2) = f, t
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    return {"north": (x2 - u * dx, y2 - v * dy, z1), "south": (x1 + u * dx, y2 - v * dy, z2),
            "east": (x2, y2 - v * dy, z2 - u * dz), "west": (x1, y2 - v * dy, z1 + u * dz),
            "up": (x1 + u * dx, y2, z1 + v * dz), "down": (x1 + u * dx, y1, z2 - v * dz)}[face]


def uv_caixa(u, v, tam, espelho):
    """Retângulos [u1, v1, u2, v2] de cada face no UV em caixa (box UV) do Minecraft/Blockbench."""
    w, h, d = (math.floor(abs(x) + 1e-4) for x in tam)
    f = {"east": [u, v + d, u + d, v + d + h], "west": [u + d + w, v + d, u + 2 * d + w, v + d + h],
         "up": [u + d + w, v + d, u + d, v], "down": [u + d + 2 * w, v, u + d + w, v + d],
         "south": [u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h], "north": [u + d, v + d, u + d + w, v + d + h]}
    if espelho:
        f["east"], f["west"] = f["west"], f["east"]
        f = {k: [a[2], a[1], a[0], a[3]] for k, a in f.items()}
    return f


# ---------------- Molang mínimo (seguro: só números, operadores e math.*) ----------------
_FUN = {"math.sin": lambda x: math.sin(math.radians(x)), "math.cos": lambda x: math.cos(math.radians(x)),
        "math.abs": abs, "math.clamp": lambda x, a, b: max(a, min(b, x)), "math.lerp": lambda a, b, t: a + (b - a) * t,
        "math.sqrt": lambda x: math.sqrt(max(x, 0)), "math.min": min, "math.max": max, "math.floor": math.floor,
        "math.round": round, "math.pow": pow}


def molang(expr):
    if isinstance(expr, (int, float)):
        return float(expr)
    s = str(expr).strip().lower().replace("query.", "q.").replace("variable.", "v.")

    def nome(n):
        return n.id if isinstance(n, ast.Name) else nome(n.value) + "." + n.attr

    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return float(n.value)
        if isinstance(n, ast.UnaryOp): return -ev(n.operand) if isinstance(n.op, ast.USub) else ev(n.operand)
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            if isinstance(n.op, ast.Add): return a + b
            if isinstance(n.op, ast.Sub): return a - b
            if isinstance(n.op, ast.Mult): return a * b
            if isinstance(n.op, ast.Div): return a / b if b else 0.0
            return 0.0
        if isinstance(n, (ast.Name, ast.Attribute)): return math.pi if nome(n) == "math.pi" else 0.0
        if isinstance(n, ast.Call): return float(_FUN[nome(n.func)](*[ev(x) for x in n.args]))
        return 0.0
    try:
        return ev(ast.parse(s, mode="eval"))
    except Exception:
        return 0.0


def primeiro_quadro(canal):
    if isinstance(canal, dict):
        canal = canal[sorted(canal, key=float)[0]]
        if isinstance(canal, dict):
            canal = canal.get("post", canal.get("pre", [0, 0, 0]))
    if not isinstance(canal, list):
        canal = [canal] * 3
    return [molang(x) for x in canal]


def carregar_animacao(caminho, nome):
    if not caminho:
        return {}
    an = json.load(open(caminho, encoding="utf-8-sig"))["animations"].get(nome, {})
    return {b: {k: primeiro_quadro(v) for k, v in d.items() if k in ("rotation", "position", "scale")}
            for b, d in an.get("bones", {}).items()}


# ---------------- montagem das faces ----------------
def faces_do_modelo(geo, anim=None, ocultos=()):
    g = geo["minecraft:geometry"][0]
    anim = anim or {}
    ossos = {b["name"]: b for b in g["bones"]}
    filhos = {}
    for b in g["bones"]:
        filhos.setdefault(b.get("parent"), []).append(b["name"])
    faces = []

    def andar(nome, M):
        b = ossos[nome]
        if nome in ocultos:
            return
        a = anim.get(nome, {})
        p = b.get("pivot", [0, 0, 0]); r = b.get("rotation", [0, 0, 0]); ar = a.get("rotation", [0, 0, 0])
        sc = a.get("scale", [1, 1, 1]); pos = a.get("position", [0, 0, 0])
        if min(abs(x) for x in sc) < 1e-3:
            return
        A = rot(-(r[0] + ar[0]), -(r[1] + ar[1]), r[2] + ar[2]) @ np.diag(sc)
        Mn = compor(M, em_volta(A, (-p[0], p[1], p[2]), (-pos[0], pos[1], pos[2])))
        for c in b.get("cubes", []):
            o, s, i = c["origin"], c["size"], c.get("inflate", 0)
            de = [-(o[0] + s[0]) - i, o[1] - i, o[2] - i]; ate = [-o[0] + i, o[1] + s[1] + i, o[2] + s[2] + i]
            Mc = Mn
            cr = c.get("rotation")
            if cr and any(abs(x) > 1e-9 for x in cr):
                cp = c.get("pivot", [0, 0, 0])
                Mc = compor(Mn, em_volta(rot(-cr[0], -cr[1], cr[2]), (-cp[0], cp[1], cp[2])))
            uv = c.get("uv", [0, 0])
            if isinstance(uv, dict):
                rets = {k: [f["uv"][0], f["uv"][1], f["uv"][0] + f["uv_size"][0], f["uv"][1] + f["uv_size"][1]]
                        for k, f in uv.items()}
            else:
                rets = uv_caixa(uv[0], uv[1], s, c.get("mirror", b.get("mirror", False)))
            for face, ret in rets.items():
                if abs(ret[2] - ret[0]) < 1e-6 or abs(ret[3] - ret[1]) < 1e-6:
                    continue
                pts = [Mc[0] @ np.array(canto(face, de, ate, u, v), float) + Mc[1] for u, v in ((0, 0), (1, 0), (0, 1))]
                faces.append((pts, ret, Mc[0] @ np.array(NORMAL[face], float)))
        for f in filhos.get(nome, []):
            andar(f, Mn)

    for raiz in filhos.get(None, []):
        andar(raiz, (np.eye(3), np.zeros(3)))
    return faces


def tom_minecraft(n):
    n = n / (np.linalg.norm(n) + 1e-9)
    return n[0] ** 2 * 0.6 + n[2] ** 2 * 0.8 + n[1] ** 2 * (1.0 if n[1] > 0 else 0.5)


def desenhar(faces, tex, yaw, pitch=0.0, escala=8, fundo=(235, 235, 230), margem=10, ss=2):
    """Projeção ortográfica com z-buffer. yaw 0 = vista de frente (olhando a face -z do modelo)."""
    V = rot(pitch, 0, 0) @ rot(0, yaw, 0)
    s = escala * ss
    # sem descarte de face traseira, como o GeckoLib (entityCutoutNoCull): o verso dos planos aparece
    proj = [([V @ p for p in pts], uv, n) for pts, uv, n in faces]
    if not proj:
        return Image.new("RGB", (10, 10), fundo)
    xs = [-q[0] for P, _, _ in proj for q in P + [P[1] + P[2] - P[0]]]
    ys = [-q[1] for P, _, _ in proj for q in P + [P[1] + P[2] - P[0]]]
    x0, y0 = min(xs), min(ys)
    W = int((max(xs) - x0) * s) + 2 * margem * ss; H = int((max(ys) - y0) * s) + 2 * margem * ss
    cor = np.zeros((H, W, 3), np.float32); cor[:] = fundo
    zb = np.full((H, W), np.inf, np.float32)
    th, tw = tex.shape[:2]
    for P, (u1, v1, u2, v2), n in proj:
        sp = [np.array([(-q[0] - x0) * s + margem * ss, (-q[1] - y0) * s + margem * ss, q[2]]) for q in P]
        o, e1, e2 = sp[0], sp[1] - sp[0], sp[2] - sp[0]
        det = e1[0] * e2[1] - e1[1] * e2[0]
        if abs(det) < 1e-9:
            continue
        q4 = sp[1] + sp[2] - sp[0]
        bx = [q[0] for q in sp] + [q4[0]]; by = [q[1] for q in sp] + [q4[1]]
        ix0, ix1 = max(int(min(bx)), 0), min(int(math.ceil(max(bx))), W - 1)
        iy0, iy1 = max(int(min(by)), 0), min(int(math.ceil(max(by))), H - 1)
        if ix1 < ix0 or iy1 < iy0:
            continue
        gx, gy = np.meshgrid(np.arange(ix0, ix1 + 1) + .5, np.arange(iy0, iy1 + 1) + .5)
        dx, dy = gx - o[0], gy - o[1]
        u = (dx * e2[1] - dy * e2[0]) / det; v = (e1[0] * dy - e1[1] * dx) / det
        dentro = (u >= 0) & (u <= 1) & (v >= 0) & (v <= 1)
        if not dentro.any():
            continue
        z = o[2] + u * e1[2] + v * e2[2]
        bloco = zb[iy0:iy1 + 1, ix0:ix1 + 1]
        ok = dentro & (z < bloco - 1e-4)
        tu = np.clip(np.floor(u1 + u * (u2 - u1)), min(u1, u2), max(u1, u2) - 1).astype(int).clip(0, tw - 1)
        tv = np.clip(np.floor(v1 + v * (v2 - v1)), min(v1, v2), max(v1, v2) - 1).astype(int).clip(0, th - 1)
        amostra = tex[tv, tu]
        ok &= amostra[..., 3] > 0
        if not ok.any():
            continue
        bloco[ok] = z[ok]
        cor[iy0:iy1 + 1, ix0:ix1 + 1][ok] = amostra[..., :3][ok] * tom_minecraft(n)
    return Image.fromarray(cor.clip(0, 255).astype(np.uint8)).resize((W // ss, H // ss), Image.LANCZOS)


VISTAS = ((0, 0, "frente"), (90, 0, "lado direito"), (180, 0, "tras"), (270, 0, "lado esquerdo"), (35, -20, "3/4"))


def folha(geo_path, png_path, saida, anim_path=None, anim_nome=None, escala=8, vistas=VISTAS):
    geo = json.load(open(geo_path, encoding="utf-8-sig"))
    tex = np.asarray(Image.open(png_path).convert("RGBA")).astype(np.float32)
    faces = faces_do_modelo(geo, carregar_animacao(anim_path, anim_nome))
    imgs = []
    for y, p, n in vistas:
        im = desenhar(faces, tex, y, p, escala)
        if im.width < 110:   # vista estreita: alarga o fundo para o rótulo caber
            fundo = Image.new("RGB", (110, im.height), (235, 235, 230)); fundo.paste(im, ((110 - im.width) // 2, 0)); im = fundo
        imgs.append((im, n))
    H = max(i.height for i, _ in imgs) + 22; W = sum(i.width for i, _ in imgs)
    out = Image.new("RGB", (W, H), (235, 235, 230)); d = ImageDraw.Draw(out); x = 0
    try:
        fonte = ImageFont.truetype("DejaVuSans.ttf", 13)
    except OSError:
        fonte = ImageFont.load_default()
    for i, n in imgs:
        out.paste(i, (x, 22)); d.text((x + 5, 4), n, fill=(30, 30, 30), font=fonte); x += i.width
    out.save(saida)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 3:
        sys.exit(__doc__)
    anim = a[3] if len(a) > 4 else None
    nome = a[4] if len(a) > 4 else None
    esc = float(a[5]) if len(a) > 5 else (float(a[3]) if len(a) == 4 else 8)
    folha(a[0], a[1], a[2], anim, nome, esc)
    print("gravado", a[2])
```

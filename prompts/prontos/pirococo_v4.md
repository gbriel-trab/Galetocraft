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
- **Galeria de referência de estilo.** São renders de modelos do Cobblemon. Servem só para calibrar o acabamento:
  - `galeria_aves.png`;
  - `rostos_cabecas.png`;
  - `solidos_vs_planos.png`: o mesmo modelo completo e só com os sólidos.

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
   - `pirococo_rosto.png`: close da cabeça de frente e em 3/4;
   - `pirococo_sem_planos.png`: as vistas com todos os planos escondidos (teste da seção B3).
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
- **Cabeça e tronco são 1–2 caixas sólidas cada**, com o detalhe resolvido na pintura.
  - Junte volumes sempre que der.
  - Pilhas de caixinhas para "esculpir" uma forma deixam o modelo entulhado.
- **Curvas são degraus.** Não gire várias peças vizinhas em ângulos crescentes para fingir uma curva.
- **Silhueta fiel nas massas grandes:**
  - o que identifica a criatura (crista, capa, cauda, armadura) é grande e legível;
  - o que é miúdo vira pintura.

### B3. MASSA SÓLIDA + FRANJA DE PLANOS (a regra que mais pesa no resultado)

**Toda massa grande é feita de caixas sólidas grossas, com as penas PINTADAS nelas.** Os planos (espessura 0) são só
a **franja** da borda. Medido no Cobblemon:

| peça | como o Cobblemon constrói |
|---|---|
| asa fechada do Talonflame | **3 placas sólidas** de 2–3 u de espessura (2×6×5, 3×9×9, 2×6×6) + **1 plano** na ponta |
| asa fechada do Braviary | **3 placas sólidas** (2×10×4, 3×13×10, 2×11×7) + **1 plano** |
| juba do Braviary | **3 blocos sólidos** (8×5×4, 11×6×6, 8×4×4) + tufos planos de 2–3 u só na borda |
| tronco (Talonflame, Braviary) | **2 caixas sólidas** sobrepostas (ex.: 14×14×12 + 10×12×8) + pescoço em 1–2 caixas |

- **Teste "sem planos" (obrigatório):**
  - esconda todos os planos e renderize;
  - a criatura tem que continuar **inteira e reconhecível**, com capa, asas, juba e cauda como volumes;
  - se ela virar um palito com fios, a construção está errada.
  - Veja `solidos_vs_planos.png`: o Braviary e o Talonflame passam nesse teste.
- **Capas, mantos e asas fechadas:**
  - 2–4 placas sólidas de 2–3 u de espessura por lado, sobrepostas como telhas e abrindo em leque;
  - as penas são **pintadas** nas faces;
  - na borda de baixo de cada placa, **1 plano de franja** recortado em pontas.
  - **Nunca** faça a capa com dezenas de planos soltos: vira papel, "vassoura" e cortina.
- **Cristas, jubas e cabelos:**
  - 1–3 blocos sólidos formam a massa;
  - 6–15 planos de chama ou tufo, **largos (base ≥ 4–5 px)**, presos na borda dos blocos, dão o contorno recortado.
- **Planos em geral:**
  - no máximo **~35% dos cubos** (contando os planos);
  - nenhum com menos de 3 px de largura;
  - contorno **recortado em pixel** na textura;
  - incline-os (≥ 25° em relação às vistas principais) para não virarem fio de perfil.

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
- **Penas pintadas em placas sólidas** (capa, asas):
  - penas **largas, de 4–6 px**, em 2 fileiras por placa de ~12 u, deslocadas como telhas;
  - cada pena num tom (claro ou base, alternando com a vizinha);
  - ponta em V com 1 px de sombra;
  - filete claro só em penas alternadas;
  - nada de grade miúda, que fica com cara de teclado ou tricô.
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
- **Rotações:** em graus, em volta do `pivot`. Sentidos conferidos no renderizador:
  - **Abrir para fora** (a ponta de cima de uma ombreira subir, ou a ponta de baixo de uma pena da capa se afastar
    do corpo): rotação em **z = −ângulo × sinal(x)**.
  - **Inclinar a ponta de CIMA para fora** (chamas da crista): **z = +ângulo × sinal(x)**.
  - **Ponta de BAIXO indo para trás** (capa, cauda pendurada) ou **ponta de trás subindo** (lâmina que varre para
    trás): **x = +ângulo**.
  - **Topo inclinando para trás** (pena em pé): **x = −ângulo**.
  - Mesmo assim, confira sempre no render.

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
3. **Rodada 1 — BLOCKOUT SÓLIDO:** só caixas sólidas (nenhum plano), pintadas com a cor base.
   - Renderize e compare com as vistas da ficha.
   - Ajuste até as alturas dos marcos baterem (±0,5 u) e a silhueta de frente e de lado bater **sem a ajuda de
     planos**.
   - Só então acrescente a franja de planos.
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
   - `idle` e `walk` estão em laço;
   - % de planos ≤ ~35%;
   - nenhum plano com largura < 3 px.
10. **Gere também `pirococo_sem_planos.png`** (o render com todos os planos escondidos) para o teste da seção B3.
11. **Entregue os arquivos da seção A** e o relatório.

### Autoavaliação antes de entregar (nota de 0 a 10 em cada item; refaça o que ficar abaixo de 8)

1. Silhueta e proporções (frente e perfil) contra a ficha.
2. Cabeça e rosto: olho legível, expressão certa, bico.
3. Elementos característicos da criatura (ver a ficha da criatura).
4. Fidelidade de cores à paleta.
5. Acabamento Cobblemon: 1 px/u, sem mixels, sem entulho, pintura em faixas, sem contorno preto.
6. Construção: massa sólida + franja (passa no teste "sem planos"), nenhum fio, nenhuma "vassoura".
7. Animação: viva, sutil, sem emenda, sem peças atravessando.

---

## Ficha da criatura — Pirococó (#001), "O Galo Fênix"

> **Se esta conversa já tem um modelo anterior do Pirococó, descarte-o.** Este pedido é uma **reconstrução do zero**
> com a técnica "massa sólida + franja" (seção B3). Não reaproveite a construção antiga (capa de planos soltos,
> crista em raios); só utilitários (UV, validações).

**Quem é:** um mítico do tipo fogo. É uma ave de rapina nobre e imponente, com cerca de 5 cabeças de altura (não é
filhote nem chibi), e usa armadura prateada de cavaleiro. Os elementos que o identificam de longe:

- **Juba de penas vermelhas** em chama, em volta de um rosto pequeno e afiado.
- **Elmo-tiara prateado** com gema rubi na testa.
- **Colar em V prateado** com gema no peito.
- **Ombreiras em concha** que abrem para cima, com ponta dourada.
- **Capa-asa de penas em triângulo:** roxa (com filetes prata) em cima, vermelha embaixo. Ela emoldura o peito creme
  e abre em sino.
- **Pernas longas e finas** com joelheira e tornozeleira prateadas.
- **Garras douradas.**
- **3 tranças douradas** que descem **retas** pelas costas da capa, cada uma terminando numa pena-lâmina dourada com
  losango rubi.

**Expressão:** a neutra da ficha ("NORMAL"), séria e determinada.

### Escala e orçamento

| item | valor |
|---|---|
| altura total (chão → ponta da crista) | **45 u** (2,8 blocos) |
| largura máxima (capa, na frente) | ~29 u |
| cubos | **110–170** (a construção abaixo dá ~120); planos ≤ ~35% |
| textura | 256×128 (no máximo 256×256), 1 px por u |

### Marcos de altura (y a partir do chão)

| marco | y (u) |
|---|---|
| crista acima do elmo | 39 → 45 |
| cabeça (topo do elmo → queixo) | 31 → 39; olhos em 35; bico de 34 a 30,5 |
| colar e topo das ombreiras | 28–29,5 |
| gema do peito | 22 → 27; ponta do V do colar em ~21,5 |
| tronco | 15 → 28 |
| coxas | 10,5 → 15 |
| joelheira | 8,5 → 10,5 |
| canela | 5,5 → 8,5 |
| tornozeleira | 3,5 → 5,5 |
| pé + garras | 3 → 0 |
| barra da capa | ~2 (não encosta no chão) |

### Construção por região

Coordenadas do `.geo.json`: x negativo = lado direito, frente em z negativo, y para cima, chão em y = 0. Os sinais
de rotação seguem a seção C1 (s = sinal de x do lado). A tabela dá o ponto de partida: renderize e ajuste até a
silhueta bater com a ficha.

**Resultado esperado da construção:**

- altura de 0 a ~45 u e largura de ~30–32 u;
- ~120 cubos, ~34% de planos;
- passa no teste "sem planos": a capa, as ombreiras, a juba e a cauda continuam como volumes.

| região | construa assim (tamanho, posição e giro em u e graus) | pintura e acabamento |
|---|---|---|
| tronco | 2 caixas sobrepostas: 10×13×10 (x −5..5, y 15..28, z −7..3) + 8×11×12 (x −4..4, y 16..27, z −8..4) | frente com um V creme claro que afina para baixo; resto vermelho em faixas |
| peito | bloco creme 8×8×3 saltado (x −4..4, y 19..27, z −10..−7, o "peito de pombo") + 6×4×2 abaixo (x −3..3, y 15..19, z −9..−7) + plano creme 6×3 recortado em 3 pontas (y 12..15, z −8,5, base 10° para trás) | chevrons em zigue-zague de 1 px (#d9b398), luz no topo, quinas com 1 px de sombra |
| pescoço | caixa 6×5×6 (x −3..3, y 27..32, z −7..−1) | frente creme e nuca vermelha; faixa de sombra sob o queixo |
| cabeça | caixa 8×8×7 (x −4..4, y 31..39, z −7..0) + tampa 6×1×5 (y 39..40, z −6..−1) + nuca 6×6×1 (y 32..38, z 0..1): o contorno fica chanfrado | rosto: creme embaixo (garganta e bochecha); marcas de pena de 1 px nas laterais; topo escuro sob a juba |
| bico | base 3×3×2 (x −1,5..1,5, y 31,5..34,5, z −9..−7) + meio 2×2×2 (y 31,5..33,5, z −10,5..−8,5) + gancho 2×2×1 caído (y 30,5..32,5, z −11..−10) | topo #ffe138, lados #fcb419, gancho e base de baixo #d87b08; 1 px de narina |
| olhos | cubos "de quina" 2×1×2 com `inflate` 0,02 (x −4..−2 e 2..4, y 34,5..35,5, z −7..−5): o olho aparece de frente e de lado. Viseira prata 3×1×3 sobre cada olho (y 35,4..36,4), com a ponta de dentro mais baixa: z = −18 × s | 1 px #fff6e0 + 1 px de íris #9e1020. Pálpebras `palpebra_d`/`palpebra_e`: cubo igual, vermelho, `inflate` 0,01, para piscar |
| elmo | casca prata 9×2×8 em volta da cabeça (x −4,5..4,5, y 36..38, z −7,5..0,5), com a traseira mais alta (x = +12°, pivô na frente, em (0, 37, −7,5)) + gema 2×4×1 na testa (y 35..39, z −8,2..−7,2) | chanfro pintado (1 px #f6f6f6 em cima, #ac93ae embaixo); gema em losango com 3 facetas; 2 aletas planas de 3×4 saindo para trás, de dentro da juba |
| juba | **massa sólida:** bloco 8×2×8 em cima da cabeça (x −4..4, y 38..40, z −6..2) + bloco 6×4×6 atrás (x −3..3, y 35,5..39,5, z −1..5), varrendo para trás e para cima (x = +12°, pivô (0, 38, −1)). **Franja de planos largos:** 2 penas em U de 5×8 viradas para a frente (centro em x ±3, base em y 37,5, z −4,5; z = +8 × s, x = −8°), formando a lira; pena central de 5×5 (base em y 38, z −4, x = −15°); 3 chamas de 5×8 por lado (base em y 37, em x ±3,5/±4,5/±5,5 e z −3/−2/−1; z = +14, +26 e +38 × s; x = −20°); 4 lâminas de nuca, planos verticais ao longo de z de 5×11 (x −2,5/0/+2,5/0, de z 1 a 12), com a ponta de trás subindo (x = +16°, +24°, +6° e −6°); 1 tufo de bochecha 3×5 por lado (x ±4,2, y 31..36, z −3,5; z = +115 × s) | cada chama com raiz escura, haste clara e ponta curva na luz; lâminas da nuca com a ponta afinando para trás; mechas de 1 px nos blocos; ponta mais alta em y ≤ 45,5 |
| ombreiras | por lado: concha prata 6×4×8 (x 4..10 / −10..−4, y 25..29, z −5..3) + tampa roxa 5×1×7 em cima + ponta dourada 3×1×5 na borda de fora. A concha e a tampa abrem com a borda de fora SUBINDO: z = −20 × s, pivô (±4,5, 28, −1). A ponta abre z = −40 × s | losango roxo pintado na tampa; borda prata chanfrada; dourado só na ponta |
| colar + gema | V de 2 placas prata 5×2×1 (x −6..−1 e 1..6, y 21,5..23,5, z −10,6..−9,6), com as pontas de fora mais altas (z = −32 × s, pivô (0, 22, −10,1)) + faixa 10×2×3 (x −5..5, y 26..28, z −9,6..−6,6) + gema 3×5×1 (x −1,5..1,5, y 22..27, z −11,1..−10,1) | chanfro pintado; gema com facetas, no osso `gema_peito_brilho` |
| asas-capa (`asa_d`/`asa_e`) | **3 placas sólidas por lado**, como a asa fechada do Talonflame. Veja a tabela abaixo | penas de 5 px em 2 fileiras por placa (seção B6); filete prata em penas alternadas nas roxas; vermelhas com pontas claras |
| costas da capa (`capa_costas`) | 3 placas sólidas em leque: 12×13×2 (y 15..28, z 3..5), 18×13×2 (y 8..21, z 4,5..6,5) e 22×10×2 (y 3..13, z 6..8), centradas em x 0. Cada uma recua com x = +8°, +14° e +18°, com pivô no meio da borda de cima. Embaixo de cada placa, 1 plano de franja de 4 u recortado em pontas | mesma pintura das asas; pena central marcada (o "eixo" do leque da ficha TRÁS) |
| cauda | fecho prata 7×3×1 nas costas (x −3,5..3,5, y 24..27, z 5,2..6,2). 3 tranças em x 0 e ±3, com segmentos 2×3×2 encadeados (a central com 5, as laterais com 3, cada um num osso). O 1º segmento é girado x = +17°: a trança desce **reta**, encostada por fora da capa e acompanhando a inclinação dela. As laterais abrem z = −5 × s. Na ponta, lâmina de 2 planos em X (5×8 na central, 4×7 nas laterais) com losango 2×3. As pontas ficam em y ≈ 2 (central) e ≈ 8 (laterais) | trança pintada em gomos diagonais (`<<<`, 3 tons de dourado); lâmina em forma de chama apontando para baixo; **nenhuma curva** |
| pernas | por lado, com centro em x ±2,6: coxa vermelha 4×5×5 (y 10,5..15,5) + franja 4×3 na frente; joelheira 3×2×3 (y 8,5..10,5) + espora triangular 3×4 na frente, inclinada 15° para a frente; canela roxa 2×3×2 (y 5,5..8,5); tornozeleira 3×2×3 (y 3,5..5,5) + ponta triangular 3×2 para baixo | penas pintadas na coxa; chanfro nas peças prata |
| pés | pé 3×2×4 roxo-escuro (y 1..3, z −3..1). 3 dedos 1×1×3 (z −6..−3), cada um num osso girado y = −28°, 0° e +28° em volta de (x, 1, −3). Garra dourada 1×1×2 na ponta de cada dedo (y 0,6..1,6, z −7,5..−5,5), caída: x = +20°, pivô na base da garra. Dedo de trás 1×1×2 + garra 1×1×1 | escamas de 1 px nos dedos; garra com a ponta clara |

**As placas das asas-capa:**

- Cada placa tem o pivô no meio da sua borda de cima, em (±5, topo da placa, meio da profundidade).
- As rotações são: z = −abre × s (a ponta de baixo se afasta do corpo), x = +recua (vai para trás) e y = −gira × s
  (a borda da frente vem para dentro e cobre o flanco).
- Embaixo de cada placa vai 1 plano de franja de 4 u de altura, colado na face de fora, com a mesma rotação e
  recortado em pontas.

| placa | tamanho (espessura × altura × profundidade) | posição | abre | recua | gira |
|---|---|---|---|---|---|
| 1 (roxa) | 3×13×10 | x ±(5..8), y 15..28, z −6..4 | 20° | 6° | 14° |
| 2 (roxo → vermelho) | 3×13×12 | x ±(6..9), y 8..21, z −5..7 | 23° | 12° | 8° |
| 3 (vermelha) | 2×11×13 | x ±(7..9), y 2..13, z −3..10 | 24° | 16° | 3° |

Acrescente 2–3 planos de pena de 4×8 por lado, saindo da borda de trás da placa 3 e apontando para trás e para
baixo: de lado, a capa precisa mostrar pontas como na ficha DIREITA.

**Atenção:**

- As penas em U da crista são **vermelhas**. Não há chifres dourados.
- A armadura é **prateada** (com um leve tom lilás).
- O dourado aparece só no bico, nas garras, nas tranças, nas lâminas da cauda, nas pontas das ombreiras e no fecho.

### Ossos e animação

**Ossos:**

- **Raiz:** `pirococo`.
- **`corpo`:** pescoco → cabeca → crista; gema_peito_brilho; ombreira_d e ombreira_e; asa_d e asa_e; capa_costas;
  cauda.
- **`cauda`:** cauda_a_0..4, cauda_b_0..2 e cauda_c_0..2, encadeados; cada um termina em lamina_a/b/c, com
  losango_a/b/c_brilho.
- **Pernas:** perna_d e perna_e, filhas da raiz, com dedo_d_0..2 e dedo_e_0..2.
- **Pálpebras:** `palpebra_d` e `palpebra_e` (filhas de cabeca).

**idle (L = 4):**

- **Corpo:** respira com ±1,5° em x e sobe e desce 0,2 u.
- **Cabeça:** ±2° em x e ±3° em y, defasada do corpo.
- **Crista:** ±3°, atrasada da cabeça.
- **Asas-capa:** ±2° em z, espelhadas entre os lados.
- **Tranças:** pêndulo pequeno, ±3° em z no 1º segmento e ±1,5° nos seguintes, com atraso de −30° por segmento; as
  laterais em fase oposta.
- **Piscar:** 1 vez no fim do laço.

**walk (L = 2):**

- **Pernas:** ±25° alternadas.
- **Corpo:** sobe e desce 0,4 u, 2 vezes por ciclo, e balança ±3° em z.
- **Cabeça:** mais estável que o corpo.
- **Capa:** com atraso.
- **Tranças:** ±6° em z e ±3° em x, defasadas.

**Brilho:** só as gemas e os losangos (ossos `_brilho`).

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

### Pontos de reprovação específicos desta criatura

- **Construção:**
  - capa ou crista feitas de planos soltos ("vassoura", "sol", cortina);
  - qualquer coisa que falhe no teste "sem planos".
- **Cabeça:** grande demais (fofa) ou rosto genérico de galinha. É uma ave de rapina séria.
- **Pernas:** grossas ou curtas (a perna visível tem 10,5 u).
- **Capa:**
  - escondendo o peito creme;
  - ou, ao contrário, ausente nos flancos ("caixote" vermelho).
- **Tranças:**
  - fundidas numa peça só, com curva, encostando no chão ou penduradas entre as pernas;
  - pintadas em xadrez.
- **Pés:** gigantes ou em barra.

---

## Apêndice — renderizador de conferência (`render_geo.py`)

Salve como `render_geo.py` e use-o assim:

```
python render_geo.py pirococo.geo.json pirococo.png pirococo_vistas.png pirococo.animation.json animation.pirococo.idle 8
python render_geo.py pirococo.geo.json pirococo.png pirococo_sem_planos.png 8 --sem-planos
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
     [--sem-planos]   (esconde os cubos de espessura 0: teste "massa sólida + franja")
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
def faces_do_modelo(geo, anim=None, ocultos=(), sem_planos=False):
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
            if sem_planos and min(abs(v) for v in c["size"]) == 0:
                continue
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


def folha(geo_path, png_path, saida, anim_path=None, anim_nome=None, escala=8, vistas=VISTAS, sem_planos=False):
    geo = json.load(open(geo_path, encoding="utf-8-sig"))
    tex = np.asarray(Image.open(png_path).convert("RGBA")).astype(np.float32)
    faces = faces_do_modelo(geo, carregar_animacao(anim_path, anim_nome), sem_planos=sem_planos)
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
    a = [x for x in sys.argv[1:] if x != "--sem-planos"]
    sem = "--sem-planos" in sys.argv
    if len(a) < 3:
        sys.exit(__doc__)
    anim = a[3] if len(a) > 4 else None
    nome = a[4] if len(a) > 4 else None
    esc = float(a[5]) if len(a) > 5 else (float(a[3]) if len(a) == 4 else 8)
    folha(a[0], a[1], a[2], anim, nome, esc, sem_planos=sem)
    print("gravado", a[2])
```

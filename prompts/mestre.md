# Pedido de modelagem — Galetocraft: {{NOME}} ({{ID}})

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

1. **`{{ID}}.geo.json`:** geometria Bedrock, `format_version` `"1.12.0"`, identificador `geometry.{{ID}}`.
2. **`{{ID}}.png`:** a textura, a 1 pixel por unidade (ver C3).
3. **`{{ID}}_glowmask.png`:**
   - mesmo tamanho da textura;
   - transparente em tudo, menos nos pixels que brilham no escuro, que repetem a cor da textura.
4. **`{{ID}}.animation.json`:** `format_version` `"1.8.0"`, com **`animation.{{ID}}.idle`** e
   **`animation.{{ID}}.walk`** (as duas em laço). São os nomes exatos que o mod chama.
5. **`gerar_{{ID}}.py`:** o script que gera tudo, para que as correções futuras partam dele.
6. **Imagens de conferência** (feitas com o renderizador do fim):
   - `{{ID}}_vistas.png`: frente, os dois perfis, trás e 3/4, na pose do 1º quadro do `idle`;
   - `{{ID}}_comparacao.png`: cada vista da ficha ao lado do render na mesma altura;
   - `{{ID}}_rosto.png`: close da cabeça de frente e em 3/4;
   - `{{ID}}_sem_planos.png`: as vistas com todos os planos escondidos (teste da seção B3).
7. **Relatório curto (até 15 linhas):**
   - número de cubos e de planos;
   - tamanho da textura;
   - lista de ossos;
   - o que ficou diferente da ficha e por quê.

No mod, os arquivos vão para estes lugares (só para você saber; não precisa criar as pastas):

- `assets/galetocraft/geckolib/models/entity/{{ID}}.geo.json`
- `assets/galetocraft/geckolib/animations/entity/{{ID}}.animation.json`
- `assets/galetocraft/textures/entity/{{ID}}.png` e `{{ID}}_glowmask.png`

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
      "identifier": "geometry.{{ID}}",
      "texture_width": 128, "texture_height": 128,
      "visible_bounds_width": 4, "visible_bounds_height": 4, "visible_bounds_offset": [0, 1.5, 0]
    },
    "bones": [
      {"name": "{{ID}}", "pivot": [0, 0, 0]},
      {"name": "corpo", "parent": "{{ID}}", "pivot": [0, 15, -1], "cubes": [
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
    "animation.{{ID}}.idle": {"loop": true, "animation_length": 4, "bones": {
      "corpo": {"rotation": ["math.sin(query.anim_time*90*2)*1.5", 0, 0],
                "position": [0, "math.sin(query.anim_time*90*2)*0.2", 0]}
    }},
    "animation.{{ID}}.walk": {"loop": true, "animation_length": 2, "bones": {
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
10. **Gere também `{{ID}}_sem_planos.png`** (o render com todos os planos escondidos) para o teste da seção B3.
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

{{CRIATURA}}

---

## Apêndice — renderizador de conferência (`render_geo.py`)

Salve como `render_geo.py` e use-o assim:

```
python render_geo.py {{ID}}.geo.json {{ID}}.png {{ID}}_vistas.png {{ID}}.animation.json animation.{{ID}}.idle 8
python render_geo.py {{ID}}.geo.json {{ID}}.png {{ID}}_sem_planos.png 8 --sem-planos
```

O que ele faz:

- desenha 5 vistas (frente, perfis, trás e 3/4) com z-buffer;
- aplica o 1º quadro da animação;
- usa o sombreamento de entidade do Minecraft;
- não descarta faces traseiras, igual ao GeckoLib.

Para o close do rosto, recorte a vista ampliada. Para a comparação, ponha cada vista da ficha ao lado do render na
mesma altura em pixels.

```python
{{RENDER_GEO}}
```

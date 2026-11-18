# Correção 1 — Pirococó (pirococo)

Continue o MESMO modelo desta conversa, a partir do seu `gerar_pirococo.py`. Não recomece do zero: mude o que está
listado abaixo e preserve o resto. As regras do pedido original continuam valendo:

- 1 px por unidade;
- cubos de tamanho inteiro;
- planos com uma face só;
- paleta e rampas da ficha;
- nomes dos arquivos e das animações `idle`/`walk`.

**Anexos:**

- `pirococo_c01_marcacoes.png`: o seu resultado, com os problemas numerados. Os números são os mesmos dos itens
  abaixo.
- A ficha da criatura, de novo.

**Diagnóstico geral:**

- **O que está certo:** as medidas de caixa. Altura de 45 u, joelho em ~10 u, comprimento ~38 u.
- **O que causa a estranheza:** as **formas** e o **acabamento**:
  - peito em forma de placa;
  - ombreiras em cabide;
  - crista e capa feitas de fiapos em ângulos aleatórios;
  - rosto sem leitura.
- **A meta desta rodada:** trocar "muitas peças finas e soltas" por **poucas peças largas, organizadas e bem
  pintadas**. É isso que faz um modelo parecer do Cobblemon.

---

## O que está bom (NÃO mexer)

- A altura total (45 u) e as alturas dos marcos:
  - queixo em ~31;
  - colar em 29,5;
  - joelheira entre 8,5 e 10,5;
  - tornozeleira entre 3,5 e 5,5.
- As pernas:
  - joelheira e tornozeleira prateadas;
  - canela roxa de 2 u;
  - o comprimento das pernas;
  - a distância entre elas.
- A escolha geral de cores (vermelho, roxo, prata, dourado e rubi) e a posição das duas gemas.
- Os nomes de arquivos e de ossos. Só a cauda ganha ossos novos (item 6).

---

## Problemas, do mais grave para o menos grave

Ordem de trabalho: **1 → 2 → 4 → 3 → 5 → 6 → 7 → 8**. Renderize e OLHE depois de cada item.

### 1. Tronco e peito: "placa de propaganda" (o problema mais grave)

**Como está:**

- O peito é uma caixa creme alta e chapada, da gola até o quadril.
- A frente é reta na vertical e saltada do corpo.
- De cada lado há colunas roxo-escuras de y ≈ 16 a 28, que formam uma moldura.
- Na vista 3/4, parece uma placa ou uma geladeira.
- Não há pescoço.

**Como deve ficar:**

- Peito de ave estufado em cima e recuando para baixo, no perfil em S da ficha.
- Em forma de escudo/V que afina para baixo.
- Emoldurado pela capa, sem moldura escura.

**Como fazer** (substitua a caixa creme atual):

- **Núcleo do tronco:** caixa 10×14×10, em x −5..5, y 15..29, z −7..+3, vermelha. Ela dá o volume e fica quase toda
  coberta pela capa.
- **Peito creme em 3 degraus**, que estreitam e recuam:

  | degrau | tamanho | x | y | z |
  |---|---|---|---|---|
  | superior | 8×6×2 | −4..4 | 22..28 | −9..−7 |
  | médio | 6×4×2 | −3..3 | 18..22 | −8,5..−6,5 |
  | inferior | 4×3×1 | −2..2 | 15..18 | −7,5..−6,5 |

  - **Borda de baixo:** 1 plano creme de 6×3 virado para a frente. Recorte-o em 3 pontas de pena, de y 15 a 12, e
    incline-o 10° para trás.
- **Pintura do peito:**
  - creme em 4 tons, com o terço de cima mais claro;
  - 2–3 chevrons em V de 1 px em #d9b398, apontando para baixo;
  - **nenhuma borda escura em volta**;
  - a junção com o vermelho das coxas é uma faixa de 1 px em #b90c27.
- **Pescoço:** caixa 5×3×5, em x −2,5..2,5, y 28,5..31,5, z −6,5..−1,5. Frente creme e nuca vermelha. Ele deve
  aparecer entre o queixo e o colar.

**Aceite:**

- De lado, o ponto mais à frente do peito fica em y 23–27, e a barriga recua ≥ 2 u até o quadril.
- De frente, o creme forma um escudo que afina de 8 para 4 u, sem colunas escuras ao lado.

### 2. Cabeça, rosto e bico

**Como está:**

- A cabeça é toda vermelha.
- Os olhos são 1 px branco + 1 px preto, nos cantos, e parecem óculos.
- A tiara é uma faixa prata reta e horizontal, que também lê como óculos.
- De lado, o bico é um tubo comprido e reto ("charuto"), sem gancho.

**Como deve ficar:**

- Rosto de ave de rapina séria:
  - topo e lados vermelhos;
  - bochecha e garganta creme;
  - olho de íris vermelho-escura sob uma viseira prateada inclinada (cara brava).
- Tiara em V, saindo da gema e subindo para trás pelos dois lados.
- Bico curto, alto na base, com gancho caído.

**Como fazer:**

- **Caixa da cabeça:** 8×8×7, em x −4..4, y 31..39, z −7..0.
  - **Frente:** metade de cima vermelha; de y 31 a 34, creme nos 4 px do meio (a garganta).
  - **Lados:** o quadrante de baixo e da frente é creme (bochecha); o resto é vermelho.
  - **Topo:** vermelho escuro (fica embaixo da crista).
- **Olhos "de quina"** (a técnica do olho do Talonflame no Cobblemon):
  - **Peça:** um cubo 2×1×2 com `inflate` 0,02 em cada canto da frente da cabeça. O olho direito fica em
    x −4..−2 e o esquerdo em x 2..4, os dois em y 34,5..35,5 e z −7..−5.
  - **Leitura:** assim o olho aparece com 2×1 px de frente e 2×1 px de lado.
  - **Pintura da frente:** 1 px #fff6e0 do lado de fora e 1 px de íris #9e1020 do lado do bico.
  - **Pintura do lado:** a íris na frente e o branco atrás.
  - **Pálpebra:** um cubo igual, vermelho, com `inflate` 0,01, para piscar.
- **Viseira/sobrancelha:**
  - placa prata 3×1×2 por cima de cada olho, em y 35,5..36,5;
  - girada ±15° em z, com a ponta de dentro (do lado do bico) mais baixa: é isso que dá a cara séria;
  - cobre a metade de cima do olho.
- **Tiara:**
  - da gema saem 2 lâminas prata de 1×2×7 pelas laterais da cabeça (x 4..5 e −5..−4, y 36..38, z −7..0);
  - inclinadas 15° em x, com a traseira mais alta;
  - terminam em 2 "asinhas" planas de 4×3 atrás da cabeça, apontando para cima e para trás a 30°.
- **Gema da testa:**
  - placa 2×4×1 na frente, em y 35..39, z −7,5..−6,5;
  - losango pintado, com os cantos transparentes e 3 tons de rubi;
  - no osso `gema_testa_brilho`;
  - não pode virar uma barra.
- **Bico** (z −11 a −7, 4 u de comprimento no total):

  | peça | tamanho | x | y | z |
  |---|---|---|---|---|
  | base | 3×3×2 | −1,5..1,5 | 31,5..34,5 | −9..−7 |
  | meio | 2×2×1 | −1..1 | 31,5..33,5 | −10..−9 |
  | gancho | 2×2×1 (cai 1 u abaixo da base) | −1..1 | 30,5..32,5 | −11..−10 |
  | mandíbula (dourado escuro) | 2×1×2 | −1..1 | 30,5..31,5 | −9..−7 |

  - **Pintura:** topo #ffe138/#ffcd29, lados #fcb419, baixo e ponta do gancho #d87b08.

**Aceite:**

- No close do rosto dá para ler:
  - rosto creme embaixo;
  - olhos bravos sob a viseira;
  - gema em losango;
  - bico com gancho.
- De lado, o bico tem no máximo 4 u e a ponta cai abaixo da base.

### 3. Crista e juba: espinhos demais

**Como está:**

- Dezenas de planos de 1–2 px em ângulos aleatórios.
- As penas em U viraram "antenas" de 1 px.
- De lado, a crista vira uma explosão de fiapos.

**Como deve ficar:** poucas penas **largas**, em forma de chama ou folha, num leque simétrico e organizado (vistas
FRENTE e DIREITA da ficha).

**Como fazer:** refaça a crista com **16 a 20 planos**, todos com base de pelo menos 3 px.

- **2 penas em U:**
  - planos virados para a frente, de 3×8, em x ±3;
  - da base em y 38 até a ponta em y 45;
  - inclinadas 20° para trás;
  - pintadas curvando para dentro na ponta.
- **1 pena central:** 3×6, até y 42, inclinada 25° para trás.
- **3 chamas por lado:**
  - planos 4×7 que saem da lateral do alto da cabeça;
  - em leque, girados 35°, 55° e 75° em z para fora e 20° para trás;
  - as pontas chegam a x ±7,5 em y ≈ 37.
- **5 lâminas varridas para trás:**
  - planos verticais ao longo de z (são vistos de lado), de 4×10 a 4×12;
  - presos na nuca, com inclinações de −10°, −20°, −30°, −40° e −50°;
  - a mais longa termina em z ≈ +12, y ≈ 36,5.
- **3 tufos de bochecha por lado:** planos 3×4 que saem de trás do rosto (y 31–34), apontando para fora e para baixo,
  girados ±40° em y.
- **Pintura de cada pena:**
  - raiz #960429/#b90c27;
  - corpo #dd1c20;
  - ponta #ef392d → #ff5b3f;
  - haste de 1 px em #ef392d;
  - ponta em degraus de 2 px.

**Aceite:**

- De frente: uma "coroa de chamas" com ~9 pontas legíveis.
- De lado: 5 lâminas em camadas.
- Nenhum plano com menos de 3 px na base.

### 4. Ombreiras e colar: "cabide dourado"

**Como está:**

- Uma barra prata reta e horizontal, com 2 cubos dourados grandes nas pontas.
- De lado, um bloco dourado grande no ombro.

**Como deve ficar** (quadro "ARMADURA PEITORAL" da ficha):

- Ombreiras **prata** em camadas, com miolo roxo.
- Abrem para cima e para fora, como asas.
- O dourado aparece só no filete da borda de fora.

**Como fazer:**

- **Remova os 2 cubos dourados grandes.**
- **Cada ombreira** tem 3 placas:

  | placa | tamanho | posição | giro |
  |---|---|---|---|
  | de baixo | 6×2×7 | x 4..10, y 26..28, z −4..3 | 15° em z (a borda de fora sobe), com pivô na borda de dentro |
  | de cima | 5×1×5 | por cima da de baixo | 22° |
  | ponta | 2×1×3 | na borda de fora | 35° |

- **Pintura das ombreiras:**
  - prata #f6f6f6/#e4dce3 na aresta de cima e #ac93ae na de baixo;
  - miolo roxo #702a7c no topo das placas;
  - filete dourado de 1 px só na aresta de fora e na ponta.
- **Colar em V:**
  - 2 placas prata 5×2×1, giradas ±30° em z;
  - elas se encontram no centro, em y 21,5 (a ponta do V), por cima do peito superior (z −9,5);
  - de cada lado, o colar sobe até encostar na placa de baixo da ombreira, sem buraco.
- **Gema do peito:**
  - placa 3×5×1, centrada em y 23–28;
  - losango pintado, com cantos transparentes e 3 tons de rubi;
  - no osso `gema_peito_brilho`.

**Aceite:**

- De frente, as ombreiras são as peças mais largas do tronco: 21 u de ponta a ponta, prateadas e inclinadas para
  cima.
- Nenhum bloco dourado maior que 2×1×3.

### 5. Capa: bloco largo e espinhento

**Como está:**

- De frente, é uma massa larga e quadrada, com 25–27 u do ombro até o chão e sem cintura.
- Muitas penas finas e espetadas, em ângulos aleatórios.
- Os filetes prata viraram um xadrez de pontinhos.
- Há planos exatamente de perfil, que viram linhas pontilhadas nas laterais da vista de frente.

**Como deve ficar:**

- 3 fileiras de penas largas, sobrepostas como telhas.
- Elas abraçam o corpo logo abaixo das ombreiras (a cintura) e abrem em sino embaixo.
- Larguras na vista de frente:

  | altura | largura |
  |---|---|
  | ombreiras | 21 u |
  | y ≈ 22 | 16 u |
  | y 18 | 24 u |
  | y 9 | 29 u |
  | barra (y 1,5) | 27 u |

**Como fazer:**

- **As 3 fileiras:**

  | fileira | altura | penas por lado | tamanho do plano | pintura |
  |---|---|---|---|---|
  | 1 | y 28 → 18 | 4 | 4×10 | roxo #702a7c, com um filete de 1 px prata #e4dce3 contínuo ao longo da borda de cima/fora (linha limpa, não pontilhada); ponta em degrau |
  | 2 | y 22 → 9 | 5 | 4×13 | faixas: metade de cima roxa, de baixo vermelha; ponta vermelha |
  | 3 | y 16 → 1,5 | 6 | 4×14 | vermelho #dd1c20, pontas #ef392d, raízes #b90c27 |

- **Atrás:** as mesmas 3 fileiras fecham as costas, com 3–4 penas por fileira.
- **Arranjo:**
  - dentro de cada fileira, as penas giram em y progressivamente em volta do corpo, ~12–15° de uma para a outra;
  - abrem 8–15° para fora (o sino);
  - cada pena cobre 1 u da anterior.
- **Nenhum plano a 0° ou 90° exatos** em relação à frente. Gire tudo 10–20°, para nada virar linha.
- **Frente livre:** a borda da capa começa em x ±5, e o creme e o colar ficam à mostra.
- **Sem espetos:** nenhuma pena com menos de 3 px de largura, nem espeto isolado.

**Aceite:**

- De frente: cintura visível em y ≈ 22 e sino embaixo.
- De lado: 3 camadas de penas legíveis, sem fiapos.
- Nenhuma linha pontilhada.

### 6. Cauda tripla: MUDANÇA DE DESIGN pedida pelo dono

**Ignore a cauda da ficha.** As 3 tranças agora saem **na horizontal, lado a lado**, da parte de trás da
**armadura superior** (entre as omoplatas, na altura das ombreiras), e seguem para trás.

**Como fazer:**

- **Remova:**
  - as 3 tranças atuais, que descem até o chão;
  - a trança que pende entre as pernas e no meio das costas.
- **Fecho:** placa prata 6×3×1 nas costas da armadura (x −3..3, y 25..28, z +3..+4), com filete dourado de 1 px. As
  tranças saem dele.
- **3 tranças lado a lado**, todas em y ≈ 26,5:
  - a central (x 0) vai reta para trás;
  - as laterais (x ±1,5) abrem ±18° em leque, vistas de cima.
- **Cada trança:**
  - 5 segmentos de 2×2×3 (15 u no total), encadeados, cada um num osso com o pivô na junta;
  - quase retos, com inclinação para baixo de 0°, 0°, 2°, 4° e 6° (um caimento leve e natural na ponta);
  - **pinte a trança na textura**: listras diagonais alternadas em 3 tons de dourado (#ffcd29, #fcb419, #d87b08);
  - **não gire os segmentos 45°**: isso deixou a trança "picotada".
- **Ponta de cada trança:**
  - pena-lâmina dourada de 3×7, feita de 2 planos cruzados em X (um vertical e um horizontal), apontando para trás;
  - o losango rubi fica no meio, numa plaquinha 2×3 com `inflate` 0,01, no osso `losango_a_brilho`, `losango_b_brilho`
    ou `losango_c_brilho`.
- **Medidas:** as pontas terminam em z ≈ +26 a +28; as laterais abrem até x ≈ ±7.
- **Ossos:**

  | osso | pai | nota |
  |---|---|---|
  | `cauda` | `corpo` | pivô (0, 26,5, +3,5) |
  | `cauda_a_0..4` | `cauda` | central |
  | `cauda_b_0..4` | `cauda` | direita, −x |
  | `cauda_c_0..4` | `cauda` | esquerda, +x |
  | `lamina_a`, `lamina_b`, `lamina_c` | o último segmento de cada trança | |

- **Animação:**
  - **idle:** cada trança balança ±3° em y e ±2° em x, com atraso de −30° por segmento; as laterais em fase oposta;
  - **walk:** ±6° em y, acompanhando o corpo.

**Aceite:**

- De lado: as tranças formam uma linha horizontal que sai das costas na altura das ombreiras.
- De cima e em 3/4: um leque de 3 tranças.
- De frente: nenhuma trança entre as pernas.

### 7. Pés e garras

**Como está:**

- De frente, o pé vira uma barra dourada listrada.
- Os dedos são cubos dourados soltos, como dentes.

**Como deve ficar:** pé roxo-escuro escamado, com 3 dedos para a frente e 1 para trás, e garras douradas só na ponta,
curvas.

**Como fazer:**

- **Pé:** caixa 3×2×3 roxo-escuro (#3a1239 de base, #491847 no topo).
- **3 dedos da frente:**
  - 1×1×4, roxo-escuro, girados −25°, 0° e +25° em y (abertos);
  - na ponta de cada um, uma garra dourada 1×1×2, girada 35° para baixo, encostando no chão.
- **Dedo de trás:** 1×1×2, com garra de 1×1×2.
- **Comprimento total:** de z −8 a +1,5.

**Aceite:** de frente, cada pé mostra 3 garras douradas abertas sobre dedos roxos. Nada de barra contínua.

### 8. Pintura geral

- **Vermelho:** está escuro e sujo, com muitos pixels quase pretos espalhados.
  - Base #dd1c20.
  - Luz nas pontas e no terço de cima.
  - #960429 só em raízes e recantos.
  - Grão de no máximo 5–8% dos pixels.
- **Prata:** hoje está cinza neutro. Use a rampa lilás: #d2bed1 de base, #f6f6f6 na aresta de cima e #ac93ae na de
  baixo.
- **Molduras:** tire todos os contornos roxo-escuros em volta das peças (peito, placas).
- **Oclusão:** 1 px escuro só nas junções:
  - sob o colar;
  - sob as ombreiras;
  - na base do pescoço;
  - entre as coxas.
- **Dourado:** só no bico, nas garras, nas tranças, nas pontas das ombreiras e no fecho da cauda.

---

## Conferência final

- Rode todas as validações do script de novo:
  - tamanhos inteiros;
  - `uv_size` igual à face;
  - ilhas de UV sem sobreposição;
  - planos com uma face só;
  - altura de 45 u;
  - nomes de ossos usados nas animações.
- **Orçamento:** continua entre 110 e 170 cubos. As trocas acima reduzem fiapos e liberam peças.
- **Animação:** atualize o idle e o walk para os ossos novos. Confira o 1º quadro do idle (nada atravessando nada,
  principalmente a capa com as pernas e as tranças com a capa).

## Entregue

- **Os arquivos atualizados:** `pirococo.geo.json`, `pirococo.png`, `pirococo_glowmask.png`,
  `pirococo.animation.json` e `gerar_pirococo.py`.
- **As imagens:**
  - `pirococo_vistas.png`;
  - `pirococo_rosto.png`;
  - `pirococo_antes_depois.png`: as vistas antigas em cima e as novas embaixo, na mesma escala.
- **Uma lista curta:** item (1 a 8) → o que mudou (com números) → resolvido ou parcial (e por quê).

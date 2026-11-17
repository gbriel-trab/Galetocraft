# Auditoria 2 – Taturico (#007), rodada n45

Fontes: ficha `007_taturico_*` (ficha, arte, vistas, detalhes, expressão Neutra), revisão `n45_*`, foto do jogo
`fotos_jogo/taturico_jogo.png` (peso maior). Régua: Esporocó aprovado no jogo (olhos com pálpebra e forma
legíveis de perto, cada parte com a silhueta e o desenho da ficha).

## TOP 10 PROBLEMAS

### 1. Olhos "arregalados", sem pálpebra nem elmo cobrindo (rosto, frente e lado; foto do jogo, frente)
- **Modelo:** olho redondo grande, anel branco-acinzentado completo em volta da íris, contorno marrom-avermelhado
  em toda a volta, brilho branco no alto. De perto, no jogo, lê como olho de boneco/assustado ("googly"). Na
  frente, os dois olhos ficam inteiros abaixo do V do elmo, com uma faixa de pele creme entre a aba e o olho.
- **Ficha (Neutra, Elmo Rochoso, Frente):** olhar sério e pesado. A aba do elmo desce **sobre** o olho e corta
  o terço de cima em linha reta inclinada (mais baixa do lado do bico). A íris âmbar (#FCA702 escurecendo para
  laranja) ocupa quase toda a parte visível; esclera creme só como cunha pequena do lado de trás; pupila preta
  vertical; brilho branco pequeno. Sem contorno escuro fechado em volta do olho.
- **Correção:** apagar o anel branco e o contorno de baixo; desenhar o olho como meia-lua: borda de cima reta e
  inclinada (pálpebra marrom-escura #5A2F29 de 1 px colada à aba), íris âmbar ocupando ~70% da área visível,
  esclera creme só no canto de trás (2 px). Baixar a aba do elmo ~1 px de textura (ou 0,5 bloco) para encostar
  na pálpebra, sem pele creme visível entre aba e olho. Na frente, o canto interno do olho deve subir em direção
  à ponta do V (sobrancelha franzida).

### 2. Cauda: leque de lâminas finas em vez de cone blindado telescópico (lado e trás; foto do jogo, lado/trás)
- **Modelo:** um feixe de placas finas e achatadas, abertas em leque, saindo na altura do meio do corpo; de trás
  parece uma escova/vassoura horizontal. Curta.
- **Ficha (Cauda Blindada, Lateral, Traseira):** cone grosso de 4–5 anéis encaixados, cada anel um pouco menor
  que o anterior, terminando em ponta. De lado, continua a linha do dorso descendo em diagonal para trás e para
  baixo (~40% do comprimento do corpo). De trás, o cone desce pelo centro, entre as pernas, até quase o chão.
  Cada anel: metade de cima marrom, faixa de baixo tan (#ED9F5E), com quadrados alternados.
- **Correção:** trocar o leque por 4–5 cubos sólidos em sequência, seção quadrada decrescente (ex.: 6×6, 5×5,
  4×4, 3×3, 2×2 px), cada um com ~1 px de degrau sobre o seguinte, eixo inclinado ~30° para baixo; ponta 1 bloco
  acima do chão, saindo da base do último anel da carapaça.

### 3. Carapaça (dorso e traseira): anéis lisos e textura borrada em vez de faixas escalonadas nítidas (trás, lado, 3/4)
- **Modelo:** de trás é uma cúpula lisa com faixas marrom/tan onduladas e listras escuras diagonais (textura
  esticada em cubos girados, serrilhado e linhas pretas visíveis de perto no jogo). De lado, xadrez miúdo e
  ruidoso de 1 px; o contorno de cima é uma curva lisa.
- **Ficha (Placas, Traseira, Lateral):** 4–5 anéis largos bem separados, cada anel saliente sobre o de baixo
  (degrau visível no contorno lateral, como telhas). Desenho de cada anel: banda marrom-rosada em cima e banda tan
  clara em baixo, com quadrados grandes (~2–3 px de textura por quadrado) alternando nas laterais. De lado, 3
  fileiras de placas tipo telha, com xadrez grande de 2 tons.
- **Correção:** refazer o dorso como anéis em caixa não girados (ou girados em múltiplos de 22,5° com UV por
  face sem esticar). Cada anel 1 bloco mais largo que o de trás e com 1 px de aba saliente na borda de baixo. Na
  textura, usar quadrados de 2×2 ou 3×3 px em vez de 1 px. Eliminar as linhas escuras de z-fighting entre anéis
  sobrepostos (afastar 0,01 ou encolher o de baixo).

### 4. Bico curto, quadrado e sem gancho; de frente forma um "T" (rosto, frente e lado)
- **Modelo:** de frente, uma placa larga em cima (mais larga que o bico) e um cubo quadrado embaixo: lê como
  "T"/martelo. De lado, dois blocos atarracados, projeção curta, sem ponta curva. A face da frente fica mostarda
  escura, bem mais escura que o topo.
- **Ficha:** bico de ave de rapina. De frente, trapézio estreito: largo no alto (sai da ponta do V do elmo) e
  afinando para baixo, sem aba lateral. De lado, projeta ~1/3 da profundidade da cabeça, com a mandíbula de cima
  curvada para baixo na ponta (gancho) e narina como ponto preto no alto. Cor amarelo-ouro uniforme #FCA702,
  laranja só na sombra de baixo.
- **Correção:** remover a placa larga de cima. Frente: largura no alto ~1/4 da cabeça, afinando 1 px de cada
  lado até a ponta. Lado: alongar 1 bloco para frente e acrescentar um cubo de 1×1 px na ponta, deslocado 1 px
  para baixo (gancho); narina preta de 1 px a 2 px da base. Clarear a textura da face frontal para o mesmo
  amarelo do topo.

### 5. Elmo de uma faixa só, topo liso; falta a aba que avança sobre os olhos (cabeça, frente e lado)
- **Modelo:** um anel fino de checker marrom/tan em V na testa e topo plano tan liso. De lado, a aba quase não
  avança além do rosto; no "rosto" lateral aparecem caixas soltas empilhadas.
- **Ficha (Elmo Rochoso, Frente, Lateral):** 2–3 fileiras de placas curvas empilhadas, do alto da cabeça até a
  testa, cada uma com checker grande marrom/tan e degrau saliente. A fileira de baixo forma a aba/viseira, que
  avança à frente do olho (~1 bloco) e desce em V até a raiz do bico. Nas têmporas, as placas descem pelos lados
  até encostar nas placas espirais da bochecha.
- **Correção:** acrescentar 1–2 fileiras de placas acima da aba atual, cada uma 1 px menos saliente que a de
  baixo, com checker de 3 px. Projetar a fileira de baixo +1 bloco para frente sobre os olhos. Prolongar as
  pontas laterais até a altura do meio do olho, para cobrir o espaço entre elmo e bochecha. O topo deve ter
  degraus de placas, não uma tampa lisa.

### 6. Asas de frente: lajes verticais lisas até a perna, silhueta de "caixa" (frente; foto do jogo, frente)
- **Modelo:** de frente, cada asa é uma laje retangular reta do ombro até a altura do joelho, com grande área
  laranja chapada e uma faixa marrom-escura horizontal; corpo inteiro lê como um robô quadrado.
- **Ficha (Frente, Arte):** ombro largo e arredondado de placas em xadrez marrom/tan (quadrados grandes),
  formando um volume em degraus. Abaixo do ombro, as placas recuam para dentro (silhueta afunila); a asa termina
  acima do topo das pernas, com uma aba menor tan/marrom por baixo.
- **Correção:** dividir cada asa em 2–3 placas empilhadas, a de cima 1 bloco mais larga que as de baixo;
  texturizar em xadrez 2 tons (#9B4F29 / #ED9F5E, quadrados de 3 px) em vez da área laranja chapada com faixa.
  Subir a base da asa ~0,5 bloco para que a coxa amarela apareça inteira de frente.

### 7. Emblema da carapaça lateral com o miolo de cores invertidas (asa, lado; foto do jogo, lado)
- **Modelo:** placa marrom com borda, campo interno grande **tan** e glifo de gancho **marrom** no meio.
- **Ficha (Carapaça, Lateral):** placa marrom-escura; moldura quadrada **tan** grossa recuada da borda; dentro
  dela, fundo **marrom**; no centro, glifo de gancho/espiral quadrada **tan** (barra de cima, desce à direita,
  volta pela metade).
- **Correção:** repintar o miolo: borda marrom 2 px → anel tan 2 px → fundo marrom → glifo tan de 2 px de
  espessura. O glifo deve ser da cor da moldura, não do fundo da placa. A placa também deve ter ~1 px de
  espessura visível (bloco chanfrado), não uma chapa fina.

### 8. Barbela longa e fina demais (rosto e peito, frente; foto do jogo, frente)
- **Modelo:** duas tiras vermelhas estreitas e paralelas, como gravata, descendo da base do bico até quase a
  franja da barriga (~45% da altura entre o topo da crista e a base do bico).
- **Ficha (Frente, Arte):** dois lóbulos vermelhos mais largos no alto (juntos cobrem a largura do bico),
  abrindo em V invertido, terminando no meio do peito (~30% da mesma medida). Pequeno lóbulo central sob o bico.
- **Correção:** encurtar as tiras ~1/3; alargar o topo de cada lóbulo +1 px, estreitando na ponta; acrescentar
  1 cubo vermelho 2×2 px colado sob o bico, no centro.

### 9. Placas espirais das bochechas chapadas de frente, altas e fora da cabeça (rosto, frente)
- **Modelo:** quadrados planos voltados para frente, flutuando ao lado da cabeça, com o topo na altura da testa;
  há um vão entre elas e o rosto.
- **Ficha (Frente, Neutra):** blocos grossos inclinados ~30–40° para fora (vistos em 3/4 mesmo de frente), mais
  baixos (centro na altura da base do bico), encostados e sobrepondo a borda do rosto creme. Abaixo do olho, o
  creme do rosto encosta direto na placa.
- **Correção:** girar cada placa ~35° no eixo Y (borda de trás para fora), descer ~0,5 bloco, aproximar até
  sobrepor 1 px da lateral do rosto e dar 1–2 px de espessura.

### 10. Patas: perna ocre escura e garras pequenas (pernas e pés, frente e lado)
- **Modelo:** perna e dedos ocre/mostarda escuros; garras cubos pequenos, mais baixos que o dedo.
- **Ficha (Patas Fortes):** perna e dedos amarelo-ouro #FCA702 vivo; cada dedo termina em uma garra cinza-arroxeada
  (#7F5E67) grande, **mais alta** que o dedo e saliente para frente; espora/dedo de trás também com garra grande.
- **Correção:** clarear a textura das pernas para #FCA702 (sombra #E08A00 só na face de baixo). Garras: altura
  1,5× a do dedo, comprimento +1 px para frente, cor #7F5E67 com topo #9A7A82.

## OUTROS PROBLEMAS MENORES
- Rosto creme de frente: metade de baixo acinzentada (#B7A28B no jogo); a ficha usa creme quente #FCDFBE.
- Peito: tom bege-acinzentado; a ficha usa creme quente #FCDFBE com sombra pêssego.
- Crista de lado: na ficha inclina para frente e o bloco da frente desce sobre a aba do elmo; no modelo está
  mais para trás e com topo plano.
- No render de rosto aparecem lâminas creme finas soltas atrás da cabeça (planos de espessura zero).
- Contorno lateral: na ficha o ponto mais alto do dorso fica logo atrás da cabeça e cai em direção à cauda; no
  modelo o dorso fica nivelado.
- Placa com fenda acima da bochecha (lado): na ficha fica mais à frente, quase tocando o olho.
- Franja da barriga: tiras da ficha mais longas e regulares, terminando logo acima das coxas.
- Marrom das placas puxa para o vermelho; na ficha é marrom-rosado/ameixa (#9B4F29 / #5A2F29).

## O QUE JÁ ESTÁ FIEL
- Silhueta geral (IoU médio 87,6%), proporção corpo/pernas e postura.
- Crista em cruz vista de frente e de trás.
- Glifo das placas espirais das bochechas e da placa com fenda.
- Paleta base (creme, tan, marrons, vermelho, amarelo, cinza) presente nas partes certas.

## NOTA DE FIDELIDADE AOS DETALHES
**6/10.** Ainda abaixo da régua do Esporocó: de perto, no jogo, o olhar "arregalado", o bico em T e a cauda em
leque são os detalhes que mais denunciam a diferença. Problemas de rosto/cabeça no top 10: **5** (1, 4, 5, 8, 9).

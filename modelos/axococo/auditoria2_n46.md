# Auditoria 2 — Axococó (008_axococo), rodada n46

Fontes: ficha `008_axococo_{ficha,arte,vistas,detalhes,expressoes}.png`; modelo `revisao/n46_{comp,vistas,3-4,rosto}.png`;
foto do jogo `fotos_jogo/axococo_jogo.png` (peso maior); régua: `fotos_jogo/esporoco_jogo.png`.
A luz do jogo escurece tudo ~25%; as cores abaixo foram comparadas descontando isso.

## TOP 10 PROBLEMAS

### 1. Brânquias: "espetos com contas" em vez de penas felpudas (todas as vistas; na foto, o que mais salta)
- **Modelo:** cada brânquia é uma barra lisa e reta, rosa-acinzentado claro, com cubinhos carmim escuros soltos
  em cima e embaixo, espaçados, como contas num espeto. De longe e de lado, os cubos carmim formam uma nuvem de
  pontinhos vermelhos em volta da cabeça e da crista.
- **Ficha (detalhe "Brânquias", arte, vistas):** cada brânquia é uma pena larga em degraus. Tem uma haste rosa-claro
  (#fdadd4) e uma franja CONTÍNUA de barbas dos dois lados, cada barba com 2 px de comprimento, inclinada para a
  ponta. As barbas alternam rosa médio (#fb6688) e rosa-choque (#fb3c7d), sem vão entre elas. A espessura total
  é ~2,5× a da haste, e a ponta é rombuda, em degrau. Não há cubos carmim escuro.
- **Correção:** apagar os cubinhos soltos. Em cada brânquia, colar ao longo de TODO o comprimento, em cima e
  embaixo, uma fileira de blocos de 1 px de altura e 2 px de comprimento, encostados uns nos outros, alternando
  #fb6688 e #fb3c7d e deslocados 1 px em direção à ponta, num serrilhado. A haste fica #fdadd4. Nos 2 px finais,
  fazer um degrau rombudo rosa-choque. Usar rosa-choque, nunca carmim/vinho (#b01a44).

### 2. Brânquias: leque aberto demais, com vãos de céu entre os ramos (frente e lado, foto)
- **Modelo:** de frente, o ramo de cima sobe ~40° e começa no canto superior da cabeça, acima do olho. Os 3 ramos
  de cada lado ficam bem separados, com céu entre eles. De lado, os ramos passam ~1 cabeça para trás da nuca,
  espaçados como dedos.
- **Ficha:** os 3 ramos saem da lateral da cabeça, atrás da bochecha, entre a base da crista e a altura do bico. O
  de cima fica a ~30° para cima, o do meio quase horizontal e o de baixo ~15° para baixo. Eles quase se tocam, e as
  franjas preenchem o espaço entre eles: de frente formam um leque compacto de ~2,2× a largura da cabeça. De lado,
  passam ~0,8 cabeça atrás da nuca e ficam empilhados sem vão.
- **Correção:** baixar a raiz do ramo de cima para a altura da sobrancelha e reduzir o ângulo dele para ~30°. Reduzir
  o comprimento lateral ~15%. Aproximar os 3 ramos para que as franjas do item 1 se toquem. O ramo de baixo começa na
  altura do canto do bico.

### 3. Emblema da asa: espiral QUADRADA (greca) em vez de espiral redonda (laterais, foto de lado)
- **Modelo:** um caracol retangular de cantos retos, tipo greca, com uma barra em L separada embaixo, correndo
  reta pela borda inferior.
- **Ficha (detalhe "Plumagem Úmida", vistas laterais):** espiral arredondada, como um "e"/"@". O anel externo é oval,
  com os cantos cortados em diagonal de degraus de 1 px, e a curva interna dá ~1,5 volta até um miolo. O traço tem
  1 px, em azul #2863b6. Do fundo do anel sai uma cauda única que desce na diagonal para frente/baixo (rumo ao
  peito) por ~6 px, afinando. A espiral fica no centro da asa.
- **Correção:** redesenhar a textura com o anel oval ~8×6 px, sem nenhum canto de 90°: cortar cada canto com 2
  degraus diagonais. Fazer a volta interna fechando num ponto central e emendar a cauda no anel, saindo do fundo e
  descendo em diagonal para frente, sem barra em L separada.

### 4. Bico: forma de "bico de pato em degrau" (lado e frente, foto e rosto)
- **Modelo:** de lado, são dois blocos: um posterior mais alto, com a narina, e um anterior mais fino colado no
  topo, avançando reto, com a ponta quadrada e plana. Parece cachimbo/pato. De frente, é uma placa larga em cima e um
  bloco mais estreito embaixo, como um "T".
- **Ficha (neutra, arte):** é uma cunha única. A linha de cima desce em rampa contínua da testa até a ponta, e a ponta
  fica embaixo, levemente curvada para baixo. O comprimento é ~1/3 da cabeça e a narina é um ponto preto em cima,
  perto da base. De frente, é um trapézio que afina para baixo, ~1/3 da largura da cabeça, com a ponta centralizada.
- **Correção:** fundir em uma peça em degraus decrescentes: base de 3 px de altura, meio de 2 px e ponta de 1 px
  ALINHADA EMBAIXO, nunca em cima. Topo em rampa. De frente, a fileira de cima tem 4 px, a do meio 3 px e a da
  ponta 2 px. A narina fica na base.

### 5. Olhos: olho branco grande com pupila pequena; sobrancelha como placa solta (frente, foto; rosto)
- **Modelo:** de frente, a esclera branca/cinza ocupa uma área grande e a pupila preta é pequena (~1/4 da largura),
  no canto interno. O olho parece vazio. A sobrancelha é uma placa rosa separada, inclinada, com uma linha clara
  visível na borda (costura).
- **Ficha (neutra):** o olho é menor em relação à cabeça. A pupila preta é grande (~45% da largura e ~60% da altura
  do olho), com um brilho branco de 1 px e um aro âmbar embaixo, e encosta na sobrancelha e no lado do bico. A
  moldura azul (#2863b6) é mais grossa embaixo e atrás. A sobrancelha rosa-escuro é parte da cabeça (capuz), cai
  em diagonal até o bico e corta o topo do olho.
- **Correção:** dobrar o tamanho da pupila (≈3×3 px num olho de 6×5), encostar a pupila na borda de cima, no lado do
  bico, com 1 px branco de brilho no canto superior. Reduzir a área branca visível baixando a sobrancelha 1 px.
  Fazer a sobrancelha flush com a cabeça (sem casca separada) e eliminar a linha clara da costura.

### 6. Barbela: duas tiras afastadas e compridas, como "suspensórios" (frente, foto)
- **Modelo:** duas barras vermelhas saem das laterais do bico, com um vão entre elas da largura do bico, e descem
  até o meio do peito. A largura total é ~1,5× a do bico.
- **Ficha:** dois lóbulos vermelhos (#f72149) logo abaixo do bico, em V invertido. Juntos, têm a largura do bico, e
  as bordas externas se alinham às do bico. O comprimento é ~1,3× a altura do bico e as pontas se arredondam.
- **Correção:** aproximar os lóbulos até as bordas externas coincidirem com as do bico, deixando no máximo 1 px de
  vão no centro. Encurtar ~35% e arredondar a ponta com um degrau de 1 px.

### 7. Crista: "cruz" curta de frente e tufo central de lado (frente, lado, foto)
- **Modelo:** de frente, é uma coluna central com dois tocos laterais baixos, formando um sinal de "+". De lado, é um
  tufo compacto só no alto do centro da cabeça, que não chega à testa nem à nuca.
- **Ficha:** de frente são 3 colunas, com a central de 2 px e as laterais a ~80% da altura dela (coroa de 3 pontas). De
  lado, é uma crista longa e em degraus, da testa (sobre o olho) até a nuca: um bloco da frente que cai um pouco
  sobre a testa e 3 a 4 degraus, com o mais alto no meio-frente. Cor rosa-choque/magenta (#fb3c7d, sombra #d91b55).
- **Correção:** alongar as colunas laterais até ~80% da central. Estender a base da crista para cobrir ~80% do
  comprimento da cabeça. Acrescentar um bloco frontal que avança 1 px sobre a testa e um degrau mais baixo na nuca.

### 8. Asas: "braços" retangulares soltos do corpo (frente, foto) e placa lisa de lado
- **Modelo:** de frente, cada asa é um pilar rosa vertical, afastado do peito como um braço, com a base quadrada. De
  lado, é uma placa retangular com listras horizontais e a traseira cortada reta.
- **Ficha:** de frente, as asas abraçam o corpo, encostadas no peito, com a base arredondada. De lado, a asa é uma
  gota grande, com o topo em arco, em 3 a 4 camadas de penas em degrau, cada uma com a ponta rosa mais escura
  (#fb6688) virada para trás e para baixo. A traseira afina em 2 pontas que sobem em direção à cauda.
- **Correção:** encostar as asas no corpo, com 1 a 2 px de sobreposição na vista frontal, e arredondar a base cortando
  os cantos com 1 degrau. De lado, arquear a borda de cima, fazer as camadas terminarem em degraus com uma linha de
  1 px #fb6688 na ponta de cada uma e afinar a traseira em 2 pontas escalonadas.

### 9. Cauda: tubos finos separados em vez de lâminas largas sobrepostas (lado e 3/4 traseiro, foto)
- **Modelo:** são 4 a 5 tubos de seção quadrada, finos e espaçados como dedos, com céu entre eles. Na vista 3/4
  traseira da foto, abrem para o lado como uma mão.
- **Ficha (detalhe "Cauda Regenerativa"):** são 5 foices largas e achatadas (mais altas que grossas, ~3 blocos de
  altura), sobrepostas na raiz sem vão, em arcos de crescente. As de cima sobem acima da linha das costas e curvam
  para baixo na ponta. O degradê vai de ciano #5abdf9 na ponta a azul-marinho #003aa1 na raiz. Vista de trás, é uma
  coluna única e estreita.
- **Correção:** achatar cada pena (altura ~2,5× a espessura) e sobrepor as raízes em ~1/3 do comprimento. Levantar a
  pena de cima para que o arco passe acima da altura das costas. Reduzir a abertura lateral, para que na vista 3/4
  traseira as penas fiquem num único plano vertical.

### 10. Pernas: largas como botas (frente, foto)
- **Modelo:** cada perna amarela tem quase a largura do pé, e a perna e o pé formam um bloco "bota".
- **Ficha:** as pernas são mais finas, com ~60% da largura do pé, e o pé é uma placa mais larga com 3 dedos
  roxo-acinzentados e um dedo traseiro. As pernas saem por baixo do peito creme, mais juntas ao centro.
- **Correção:** estreitar cada perna para ~60% da largura do pé e centralizá-la sobre os dedos, mantendo a placa do pé
  e os dedos como estão.

## OUTROS PROBLEMAS MENORES
- Peito: as fileiras de penas são faixas horizontais retas. Na ficha, são escamas em V escalonado que afunilam até
  a ponta entre as pernas.
- Peito: o creme está frio/branco demais (#fff4e4). A ficha é creme-pêssego (#fce3d3/#facccb).
- Rosto: o bloco creme do pescoço é mais largo que a cabeça (vista de rosto). Na ficha, o pescoço é mais estreito
  que a cabeça.
- Nuca: na vista 3/4 traseira da foto aparece um quadrado liso grande de rosa sem detalhe. Na ficha, as brânquias e
  a crista cobrem essa área.
- Traseira: a cauda, vista de trás, são duas tiras paralelas com vão. Na ficha, é uma coluna única, com o centro
  mais claro.
- Asa de frente: a marca azul é um ponto quadrado isolado. Na ficha, é um traço curto, que é a ponta da espiral
  aparecendo.
- Costuras claras visíveis na testa e na sobrancelha (linha rosa-clara) na foto de frente.
- Bico: a narina aparece na lateral do bloco posterior. Na ficha, fica no topo, perto da base.

## O QUE JÁ ESTÁ FIEL
- A paleta geral (rosa, rosa-choque, azul, amarelo, roxo dos dedos) e o degradê azul da cauda.
- A contagem de 3 brânquias por lado e de 3 dedos roxos por pé.
- A moldura azul dos olhos e o aro âmbar sob a pupila.

## NOTA DE FIDELIDADE AOS DETALHES
**6,0 / 10.** Ainda fica abaixo da régua do Esporocó, cujas flores, folhas e crista na foto do jogo repetem o
desenho da ficha. Aqui, as brânquias (assinatura da espécie), a espiral e o bico ainda têm outro desenho.
Dos 10 problemas, **4 são de rosto** (5 olhos, 4 bico, 6 barbela, 7 crista). Contando as brânquias, presas à cabeça,
são 6.

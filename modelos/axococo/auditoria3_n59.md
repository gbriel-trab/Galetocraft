# Auditoria 3: Axococó (n59)

Material usado: arte principal `008_axococo_arte.png` (peso maior), ficha, vistas, detalhes e expressão neutra; foto do jogo `axococo_jogo.png`; renders `n59_comp`, `n59_vistas`, `n59_3-4`, `n59_rosto` e `n59_arte_lado`. Como régua usei as fotos aprovadas de Taturicó, Morcegalo, Espinhocó e Salambrasa. O nível aceito nelas: corpo em bloco, barbela em "gravata" e sobrancelha brava passam, mas a **peça-assinatura** de cada espécie tem que ler igual à arte (casco do Taturicó, asas do Morcegalo, espinhos do Espinhocó, cauda pintada da Salambrasa). No Axococó as peças-assinatura são as **brânquias**, o **corpo rosa redondo com a espiral** e a **cauda azul em foice**, e é justamente nelas que ele falha.

## O que um fã da arte estranharia primeiro
1. **As brânquias parecem pentes ou rastelos.** Na arte são três penachos fofos e irregulares de cada lado, abertos em leque e cheios de filamentos. No jogo são seis tábuas retas e lisas, com uma serrilha vermelha fina, e de lado todas apontam para trás quase paralelas, como esquis.
2. **O corpo é uma caixa com uma "gaveta" rosa.** A arte mostra um galo gordinho e redondo, com peito estufado. No jogo o corpo é um tijolo, e a asa vira uma laje horizontal comprida que passa da traseira (de frente, duas portas chapadas dos lados). Isso, mais o peito em degraus e a espiral fina que vira "@", tira toda a massa fofa da arte.
3. **O rosto é um cubo de bico com "dois olhinhos".** Bico em cubo com as duas narinas no topo, olhos de pupila pequena e esclera cinza, testa com faixa vermelha. Lembra um capacete, não a cara macia da arte.

## TOP 10 PROBLEMAS

### 1. Brânquias: forma de pente, não de penacho (cabeça; frente, lado, 3/4 e foto do jogo)
- **Modelo:** cada brânquia é uma tábua reta de espessura constante, rosa-acinzentada, com uma fileira de dentinhos vermelhos de 1 voxel, quase só na borda de cima. Lê como pente, escova ou rastelo. As pontas não engrossam.
- **Arte:** cada brânquia é uma cadeia de blocos em degrau, levemente curva, com **tufos de filamentos dos dois lados** (em cima e embaixo). Os filamentos têm 2 a 3 voxels, tão compridos quanto a haste é grossa, e se inclinam para fora e para a frente. Os filamentos são rosa-claro (#f8a8c0), o magenta (#e0306a) fica concentrado nas pontas, e a ponta da brânquia termina num tufo mais cheio. O volume total de cada brânquia é 2 a 3 vezes o da tábua atual.
- **Correção:**
  - Haste afinando de 3x3 na base para 2x2 na ponta, em 3 segmentos com rotação progressiva (cerca de +10° a cada segmento) para curvar.
  - A cada 2 voxels da haste, um filamento 1x1x2-3 em cima e outro embaixo, inclinados uns 30° para fora e para a frente, em rosa-claro com o último voxel magenta.
  - Na ponta, um tufo de 3x3x3 com 2 ou 3 filamentos magenta saindo.
  - Tirar a linha contínua de serrilha vermelha.

### 2. Brânquias: leque e ponto de saída (lateral e frente)
- **Modelo:** de lado, as três saem do canto de cima e de trás da cabeça e vão para trás quase paralelas (todas entre 0° e +15°). A de baixo termina na altura do olho.
- **Arte:** saem da lateral e da nuca, entre o olho e a mandíbula, e abrem em leque: a de cima a uns 45° para cima e para trás, a do meio quase horizontal, a de baixo uns 30° para baixo e para trás, terminando na altura da barbela e do alto do peito. De frente, o leque inferior emoldura o pescoço.
- **Correção:**
  - Baixar a raiz das três em uns 2 voxels, com a de baixo saindo na linha da bochecha.
  - Ângulos de pitch de cerca de +45°, +5° e -30°.
  - De frente, abrir a de baixo uns 20° para fora e para baixo, até a ponta ficar no nível do topo do peito.

### 3. Corpo e asa: tijolo com "gaveta" em vez de corpo redondo (lado, 3/4 e foto lateral)
- **Modelo:** o corpo é um retângulo. A asa é uma laje reta e horizontal de borda grossa que avança bem além da traseira do corpo (no `n59_arte_lado` passa por cima da base da cauda). As primárias são tábuas paralelas empilhadas, como dedos.
- **Arte:** o corpo é um ovo inclinado. A asa é um escudo oval colado ao corpo, com a borda de cima subindo de leve para trás e a borda de baixo arredondada. As 3 ou 4 primárias de trás descem em degrau para baixo e para trás e terminam em ponta perto da base da cauda, e as bordas são recortes de penas.
- **Correção:**
  - Comprimento da asa em cerca de 0,8 vez o do corpo, sem passar mais de 2 voxels da traseira.
  - Inclinar a parte de trás uns 15° para baixo.
  - Arredondar os cantos da frente (em cima e embaixo) com degraus de 1 voxel.
  - Primárias de trás em escada: cada uma 1 voxel mais baixa e 2 voxels mais curta que a anterior.
  - Reduzir a espessura que aparece de frente e tirar os contornos rosa-escuros das tábuas.

### 4. Asas de frente: portas chapadas (frente, foto do jogo)
- **Modelo:** de frente, as asas são dois painéis verticais planos, paralelos e afastados do tronco. Com o peito reto, a silhueta fica um armário com portas abertas.
- **Arte:** as asas acompanham o tronco e se abrem um pouco embaixo. A massa mais larga do corpo fica na metade de baixo (barriga e asas), como um sino ou um ovo.
- **Correção:**
  - Encostar as asas no tronco (no máximo 1 voxel de folga).
  - Girar uns 8° a 10° para a ponta de baixo abrir para fora.
  - Alargar o tronco em uns 2 voxels no terço de baixo e afinar o terço de cima, onde ele vira pescoço.

### 5. Peito em degraus de prato (frente, lado e foto do jogo)
- **Modelo:** o creme do peito é uma pilha de lajes horizontais da largura toda (sanfona ou escada). De lado, a frente do peito é vertical e chapada sob a cabeça.
- **Arte:** penas-escama sobrepostas em fileiras desencontradas, em V que afunila entre as pernas. De lado o peito **estufa para a frente e para baixo** e faz curva sob a barriga (na `n59_comp` é a falta vermelha na frente e embaixo do peito).
- **Correção:**
  - Trocar as lajes por fileiras de "telhas" 2 ou 3 de largura por 2 de altura, deslocadas meia telha por fileira, cada uma com a borda de baixo 1 tom mais escura (#e8c8b8 sobre #f8e4d8).
  - De perfil, avançar o peito 2 a 3 voxels no meio da altura e recolher em curva até a barriga.
  - De frente, terminar o creme em V entre as pernas.

### 6. Bico: cubo com "dois olhinhos" (rosto; frente, 3/4 e foto do jogo)
- **Modelo:** um bloco quase cúbico, com 29% da largura da cabeça, pendurado sob a linha dos olhos. As duas narinas ficam no **topo**, viradas para quem olha de frente, e parecem um rostinho. Em 3/4 lê como caixa amarela caída.
- **Arte (neutra e 3/4):** cunha amarela (#f8b000) que afina até uma ponta para a frente, com a mandíbula de baixo menor. **Uma narina de cada lado**, perto da base. O topo do bico fica na metade de baixo do olho.
- **Correção:**
  - Base de 4x3, ponta de 2x2 (cerca de 1/4 da largura da cabeça) e comprimento de 4, afinando em degraus.
  - Mandíbula de 3x1 recuada 1 voxel.
  - Tirar as narinas do topo e pôr 1 px escuro em cada face lateral, a 1 voxel da base.
  - Subir o bico 1 voxel.

### 7. Olhos: pupila pequena, esclera cinza, moldura fechada e sobrancelha escura (rosto)
- **Modelo:**
  - A esclera é cinza neutro (cerca de #dbdbdc, que no jogo aparece como 175,175,176) e lê cinza ao lado do rosa.
  - A pupila é um retângulo pequeno no canto de cima perto do bico.
  - O azul contorna o olho em 3 lados.
  - Uma faixa malva-escura em escada faz a sobrancelha.
- **Arte (neutra):**
  - Esclera branca quente (#fff8f0).
  - Pupila preta **grande**, cerca de metade do olho, do lado do bico, com crescente âmbar embaixo e brilho branco em cima.
  - Azul só embaixo e atrás, em L.
  - A pálpebra é o próprio rosa da cabeça cortando o olho na diagonal, **sem linha escura de sobrancelha**.
- **Correção:**
  - Olho de 6x5 com pupila de 3x3 encostada do lado do bico, na metade de baixo.
  - 1 px âmbar sob a pupila e brilho de 1 px no canto de cima atrás.
  - Esclera #fff8f0 e azul só na base e no lado de trás.
  - Trocar a faixa malva por 1 ou 2 linhas de rosa da cabeça entrando no olho na diagonal (mais alta atrás, mais baixa perto do bico).

### 8. Cauda: leque de cartas, não foices (lado, 3/4 e foto do jogo)
- **Modelo:** um leque radial de placas retas e segmentadas, como mão de baralho ou cauda de peru. Quase todo em azul médio uniforme. Faltam as penas de baixo (falta vermelha embaixo e atrás na `n59_comp`) e sobra volume em cima e atrás (azul).
- **Arte:** 5 ou 6 foices largas e finas que sobem da traseira, **curvam para trás e para baixo** e terminam com a ponta para baixo. A mais baixa chega à altura do joelho. Cada pena tem degradê: borda externa e ponta azul-céu (#7ec8f8), base e borda interna azul-royal (#1040c0).
- **Correção:**
  - Cada pena com 4 a 5 voxels de largura e 1 a 2 de espessura, em 3 segmentos de rotação progressiva (+20°, 0°, -25°) para curvar.
  - Baixar o leque em uns 2 voxels e acrescentar 2 penas inferiores apontando para baixo e para trás.
  - Pintar o degradê por pena.

### 9. Espiral da asa vira "@" (lado, foto do jogo)
- **Modelo:** uma espiral redonda de traço fino (1 px), pequena no centro da asa, com rabicho curto. Lê como "@" ou "e".
- **Arte e detalhe "Plumagem Úmida":** espiral **quadrada e grossa** (faixa de 2 a 3 voxels) em azul médio (#2f6fd0), ocupando cerca de 60% da asa. Tem o miolo em gancho na frente e uma **cauda longa** que corre para trás e sobe em diagonal até perto da borda traseira.
- **Correção:** redesenhar a textura com traço de 2 px, cantos em ângulo reto, 2 voltas e um rabicho de cerca de 40% da largura da asa subindo em diagonal para trás.

### 10. Crista invadindo a testa e barbela curta (rosto; frente e lado)
- **Modelo:**
  - A crista é um monte de caixas de altura parecida, com uma coluna vermelha que **desce pela testa** até a linha das sobrancelhas (de frente lê como uma faixa pintada no rosto).
  - As barbelas são dois tocos curtos em gravata.
- **Arte:**
  - A crista fica só no topo, em 3 lobos que crescem para trás (o da frente pequeno, na borda da testa; o do meio ou de trás é o mais alto, cerca de 0,6 vez a altura da cabeça) e desce um pouco pela nuca. Nenhum vermelho na face.
  - As barbelas são dois lobos longos e pendentes, da base do bico até o alto do peito (cerca de 1,5 vez a altura do bico), com o vermelho interno mais escuro.
- **Correção:**
  - Remover o vermelho da face frontal da testa.
  - Lobo da frente começando na aresta de cima e lobo central 2 voxels mais alto.
  - Barbelas de 2x2 por 5 de comprimento, levemente afastadas embaixo.

## OUTROS PROBLEMAS MENORES
- **Paleta lavada:** o rosa da cabeça está malva-acinzentado (cerca de #dba4be sem sombra) contra o rosa-chiclete da arte (#f599b6), e o creme do peito puxa para o bege-cinza.
- **Corte do rosto:** o rosto tem um corte horizontal reto pink/creme na altura da base do olho, como uma máscara. Na arte o claro é só bochecha e área sob o olho, e se funde no pescoço.
- **Costuras:** a cabeça octogonal mostra costuras verticais claras entre os painéis da face no `n59_rosto`.
- **Traseira da cauda:** a coluna azul é estreita, cerca de 1/6 do corpo. Na arte é um bloco largo, cerca de 1/3.
- **Traseira da crista:** na traseira a crista não desce pela nuca como na vista de trás da ficha.
- **Contornos:** contornos rosa-escuros e vermelhos nas tábuas da asa que a arte não tem.
- **Azul na frente:** os pixels azuis que aparecem de frente nas asas estão na base. Na ficha frontal o azul da espiral aparece no meio da altura.
- **Pescoço:** quase não há pescoço visível entre a cabeça e o peito. Na arte, o creme do peito sobe afunilando até a mandíbula.

## O QUE JÁ ESTÁ FIEL
- Três brânquias por lado, cor geral rosa e magenta e posição atrás dos olhos (só falta forma e leque).
- Pernas amarelas grossas com dedos roxo-acinzentados, 3 para a frente, e pé amarelo largo.
- Proporção geral cabeça/corpo/pernas e altura total (IoU de cerca de 76%).
- Cauda na família de cor certa (azuis) e na posição certa (traseira alta).
- Bico e crista nas cores certas (amarelo e magenta-vermelho).

## NOTA DE FIDELIDADE AOS DETALHES
**5/10.** Dos 10 problemas, **4 são de rosto** (6 bico, 7 olhos, 10 crista e barbela, e 2, pela posição das brânquias em volta da face). Mais 1 é da cabeça (1, forma das brânquias).

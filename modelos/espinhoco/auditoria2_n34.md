# Auditoria 2: Espinhocó (`espinhoco`), rodada n34

Fontes: ficha `011_espinhoco_*` (ficha, arte, vistas, detalhes, expressão NEUTRA), revisão `n34_*` (comp, vistas, 3-4, rosto) e foto do jogo `fotos_jogo/espinhoco_jogo.png` (peso maior). Régua: Esporocó no jogo, que lê "igualzinho" porque cada peça-assinatura (crista vermelha, flores, cauda de cipó, folhas lima) tem a forma e a cor da ficha. No Espinhocó, as duas peças-assinatura, **espinhos** e **folhas**, ainda não leem como na ficha quando vistas de perto no jogo.

## TOP 10 PROBLEMAS

### 1. Espinhos: forma de "dedos/blocos" em vez de cones pontudos (dorso; lateral, traseira, 3/4, foto do jogo)
- **Modelo:** cada espinho é uma pilha telescópica de 2 ou 3 caixas cada vez menores, com **ponta reta e quadrada**. De frente para a ponta (traseira e 3/4), a face mostra um **quadrado dentro de quadrado** (moldura). Na foto do jogo parecem mãos ou ancinhos de madeira, ou caixas de papelão, e não espinhos.
- **Ficha:** cada espinho é um **cone longo e afilado** com facetas, que termina numa **ponta aguda de 1 pixel**, como chifre ou dente. A base tem ~2 a 3 px de largura e o comprimento é ~5 a 7 vezes essa largura. O afinamento é contínuo, sem "ombros" de degrau.
- **Correção:** refazer cada espinho como 4 ou 5 segmentos encaixados, cada um com ~70% da largura do anterior e o último com 1x1 px, para que o contorno feche num bico. Nada de degrau com ombro largo. Remover a textura de moldura quadrada da face da ponta: a ponta vista de frente deve ser só um ponto claro de 1 a 2 px. Dar uma leve curva para cima ou para fora nos espinhos longos (cada segmento girado 5 a 8°).

### 2. Espinhos: arranjo em leques ou tufos (tipo cauda de peru) em vez de ouriço radial (dorso e cauda; lateral, traseira)
- **Modelo:** os espinhos estão agrupados em ~5 a 6 leques planos, como penas de cauda de peru ou mãos abertas. Entre os leques há grandes vazios, e a massa toda fica concentrada atrás. Na traseira, o conjunto vira um amontoado de blocos claros em pirâmide.
- **Ficha:** são **~25 a 30 espinhos individuais** que cobrem o dorso inteiro, da nuca (logo atrás da crista) até a cauda. Eles irradiam do centro do dorso em todas as direções: para trás, para cima e para baixo, como um ouriço. Na **traseira** formam uma **roseta**: as pontas apontam para o observador em fileiras concêntricas, o marrom do corpo aparece entre elas, e há folhas lima nas laterais. Na lateral, as pontas inferiores descem até a altura da coxa.
- **Correção:** desfazer os leques e distribuir os espinhos sobre uma meia-esfera no dorso, em 3 anéis concêntricos, com o eixo de cada um apontando para fora do centro do dorso. Os do anel externo ficam mais longos (~0,9 da altura do corpo), e os do centro são mais curtos e apontam para trás. Deixar 1 a 2 px de corpo marrom visível entre as bases.

### 3. Espinhos: paleta pêssego/salmão sem a base marrom (dorso; todas as vistas, foto do jogo)
- **Modelo:** degradê de **pêssego/salmão alaranjado** (~#E0A070) até creme, uniforme, sem nenhum marrom.
- **Ficha:** cada espinho tem a **ponta creme-bege** (#EAD3B0), o meio **bege-castanho** (#C9A27A) e a **base marrom** (#8A5A38). As faixas facetadas alternam claro e escuro ao longo do eixo. Não há laranja nem rosa.
- **Correção:** trocar a rampa para base #7E5234, meio #B88C62, ponta #EBD6B4. Tirar a saturação laranja: o matiz fica em ~30° e a saturação em ≤35%. Escurecer a face inferior de cada segmento ~15% para marcar as facetas.

### 4. Folhas dos ombros ("Plumagem Folhosa"): lâminas estreitas penduradas como braços em vez de capa de folhas largas (asas; frente, lateral, foto do jogo)
- **Modelo:** de frente, cada lado é um feixe de lâminas finas e verticais que caem **soltas do corpo**, com vão escuro entre elas e o tronco, como dois braços ou duas vassouras. De lado, é um maço de 8 a 10 lâminas estreitas e paralelas.
- **Ficha:** de **5 a 7 folhas largas lanceoladas** de cada lado. Cada uma tem largura ~1/3 do comprimento e ponta aguda, e elas se **sobrepõem como escamas**. Nascem do pescoço, logo abaixo da bochecha, e cobrem o ombro **em leque**, inclinadas para trás e para baixo a ~45°. De frente, emolduram o peito como uma gola em "A" que se abre para os lados até a cintura. São coladas ao corpo, sem vão.
- **Correção:** trocar as lâminas por folhas de ~4 px de largura e ~12 px de comprimento, com ponta afinando em 2 a 3 degraus. Ancorá-las na base do pescoço em leque de ~60° (a de cima quase horizontal para trás, a de baixo a ~60° para baixo), sobrepondo cada uma metade da seguinte. Encostar as folhas no tronco (offset 0 a 1 px) para eliminar o vão. Na frente, a borda interna das folhas deve tocar a borda do peitoral creme.

### 5. Folhas (ombros e crista): verde-oliva escuro e "cristalino" em vez de lima com nervura (frente, lateral, foto do jogo)
- **Modelo:** verde-oliva escuro (#5E7A12 a #7A9A18) com faces quase pretas. As facetas são irregulares, como cristal ou vidro, e as bordas serrilhadas de pixel.
- **Ficha:** **verde-lima claro** (#A9C83A) com metade sombreada **lima-escuro** (#86A824). Há uma **nervura central clara** (#C8DC60) ao longo do eixo, e as bordas são lisas. É a mesma luminosidade do verde do Esporocó aprovado.
- **Correção:** paleta das folhas com luz #B4D040, base #96B82C, sombra #739423 e nervura #CFE16A (1 px no eixo). Remover os pixels quase pretos (#2E3A08) do interior das folhas. Folha = duas metades em tons (luz e base) divididas pela nervura.

### 6. Bico: funil estreito que cai até a barbela em vez de bico de rapina curto e projetado (rosto; frente e lateral)
- **Modelo:** de frente, é um "T": topo largo e uma haste estreita que desce em degraus até o meio da barbela, como uma cenoura de cabeça para baixo. De lado, é uma coluna escalonada que **cai** para baixo, pouco projetada para frente. A cor é mostarda (#D4A010).
- **Ficha (neutra e vistas):** **bico de rapina** curto e robusto. De frente, é um triângulo largo (~1/4 da largura da cabeça) que termina **acima** da barbela. De lado, **projeta-se para frente** ~1/3 do comprimento da cabeça: a mandíbula superior é alta e reta no topo e termina num **gancho** voltado para baixo, a inferior é menor e separada por uma linha escura de boca. Tem **narina** quadrada escura no topo. A cor é amarelo-ouro (#F2C418) com sombra laranja (#D99A10).
- **Correção:** bico de 4 px de largura x 3 px de altura na base. Projeção de 4 px para frente, sendo os 2 px da ponta o gancho, que desce 2 px. Mandíbula inferior de 3 px x 1 px, recuada 1 px. Linha de boca de 1 px #5A3A10. Narina 1x1 px preta no topo, a 1 px da base. A ponta não pode passar da altura da base da barbela. Clarear para #F2C418.

### 7. Crista: buquê de cristais facetados sobre uma tampa plana em vez de leque de folhas (cabeça; frente, lateral, rosto)
- **Modelo:** um tufo de cristais verdes pontudos (pirâmides com facetas escuras) **apoiado** sobre o topo plano marrom da cabeça. Fica visível uma tampa marrom com faixa verde em volta. De lado, o tufo é vertical e compacto.
- **Ficha:** a crista é feita de **folhas largas** iguais às dos ombros. De frente: 1 folha central alta e estreita, 2 de cada lado mais curtas, abertas em leque, mais 1 pequena junto a cada sobrancelha. De lado, as folhas **nascem da testa e varrem para trás e para cima** e se fundem com os primeiros espinhos da nuca. O topo da cabeça não aparece.
- **Correção:** refazer a crista com as mesmas folhas lima do item 5, com base na linha da sobrancelha. Central com 10 px de altura, laterais com 7 e 5 px, abertas a ±20° e ±40°. No perfil, inclinar todas ~35° para trás e sobrepor a base delas à nuca. Remover a tampa marrom e a faixa verde do topo da cabeça.

### 8. Barbela: duas fitas longas e paralelas (gravata-borboleta) em vez de dois lobos curtos em V (rosto; frente, lateral, foto do jogo)
- **Modelo:** duas placas vermelhas largas e longas, paralelas e separadas, que descem até o meio do peito e leem como gravata ou laço. O bico atravessa as duas.
- **Ficha:** **dois lobos** vermelhos (#D8231E) presos **logo abaixo do bico**, com altura ~1,5 vez a do bico. Eles se **abrem em V invertido**, com as pontas de baixo separadas, e cada um tem a ponta arredondada e sombra vermelho-escura (#9E1515) na face interna. Terminam no topo do peitoral creme.
- **Correção:** encurtar cada lobo para ~60% do comprimento atual e estreitar para 2 px. Girar cada um ~12° para fora. Prender a base dos dois juntos sob o bico, sem vão no topo. Arredondar a ponta tirando 1 px do canto externo. Aplicar a sombra #9E1515 na face interna.

### 9. Bochechas e máscara do rosto: xadrez acinzentado plano em vez de blocos creme salientes (rosto; frente, lateral, foto do jogo)
- **Modelo:** a área abaixo dos olhos é um **xadrez cinza-bege** desbotado (#A89A88 / #C8B49A), plano, com aspecto sujo na foto do jogo. A esclera branca ocupa metade do olho, e o olho não tem brilho.
- **Ficha (neutra):** as bochechas são **blocos creme** limpos (#F0DCC0 / #E2C8A2) **salientes em degrau**, que avançam ~1 a 2 px à frente da face e se alargam para os lados como um "bigode" de penas. A cabeça acima é marrom (#8B5A35) com blocos castanho-claros. Olho: íris **lima vivo** (#9AD21E) grande, com anel verde-escuro, pupila preta voltada para o bico, **ponto de brilho branco** de 1 px e pálpebra coberta pela sobrancelha grossa.
- **Correção:** retexturizar as bochechas só com creme (#F0DCC0 com sombra #DCC29C) e tirar todo cinza. Adicionar 2 cubos de bochecha de 1 a 2 px de profundidade, um de cada lado, que sobressaiam 1 px da largura da cabeça. Olho: reduzir a esclera para 1 coluna no lado de trás, clarear a íris para #9AD21E e pôr 1 px de brilho branco no canto superior da pupila.

### 10. Corpo: caixa marrom lisa no flanco e "saia" de placas escuras em vez de corpo redondo com penas em escamas (corpo; lateral, frente, foto do jogo)
- **Modelo:** de lado, aparece um **grande retângulo marrom liso** entre as folhas e os espinhos. Na base do tronco, uma fileira de **placas retangulares marrom-escuras** soltas forma uma "saia" de caixa. O tronco é alto e reto.
- **Ficha:** o corpo é **ovalado e redondo**. O flanco fica quase todo coberto pelos espinhos de trás e pelas folhas da frente. O pouco marrom visível são **penas em escamas escalonadas** (#8B5A35 / #6E4428 / #A8703F) com pontas em "V" que se sobrepõem. A parte de baixo desce em franja irregular de penas até as coxas.
- **Correção:** arredondar o tronco cortando 2 px de cada canto vertical e superior, para chegar ao oval. Cobrir o flanco com 2 a 3 fileiras de penas em escama de 3x3 px com ponta em V, sobrepostas. Trocar as placas da "saia" por uma franja de pontas em V de comprimentos alternados (2 e 3 px) na mesma cor do corpo. Estender os espinhos inferiores do item 2 até cobrir o terço traseiro do flanco.

## OUTROS PROBLEMAS MENORES
- Pernas bege-rosadas (#D8A878). Na ficha são **laranja-castanho** (#C27A34) com a coxa coberta de penas marrons.
- Dedos finos e achatados. Na ficha são blocos grossos, com **garras cinza-escuro grandes** (#4A4448) da largura do dedo, 3 na frente e 1 atrás, como nas "Patas Firmes".
- O peitoral creme é uma textura plana em V com xadrez. Na ficha ("Flor Peitoral") tem **camadas em degrau** que avançam 1 px cada, com borda inferior serrilhada.
- O peitoral do modelo é estreito no topo. Na ficha ocupa toda a largura entre as duas golas de folhas.
- Na vista de rosto lateral aparecem uma **prancha verde fina horizontal** e uma **prancha laranja** saindo de trás da cabeça (peças de espessura ~0 vistas de lado). Dar espessura ou ocultar.
- De frente, tufos pêssego de espinhos aparecem atrás da cabeça e dos ombros como "orelhas". Na ficha são espinhos bege pontudos que saem à altura da bochecha, acima das folhas.
- Bico na frente cor mostarda (#D4A010) e na lateral mais escuro. Unificar em amarelo-ouro.
- A sobrancelha do modelo é ligeiramente curta. Na ficha vai da nuca até encostar no topo do bico.
- Na traseira falta o marrom do corpo entre os espinhos. Na ficha ele aparece e dá contraste.

## O QUE JÁ ESTÁ FIEL
(não repetido em detalhe nesta rodada: só a confirmação)
- As sobrancelhas grossas marrom-escuras em ângulo bravo estão certas.
- Disposição geral certa: crista verde no topo, peitoral creme, barbela vermelha, massa de espinhos atrás e folhas nos ombros.
- As proporções de cabeça, tronco e pernas e a altura total batem com a ficha (IoU médio ~79%).

## NOTA DE FIDELIDADE AOS DETALHES
**5/10.** 4 dos 10 problemas principais são de rosto ou cabeça (6 bico, 7 crista, 8 barbela, 9 bochechas e olhos). Comparado ao Esporocó aprovado, falta sobretudo a leitura imediata das peças-assinatura. Os itens 1 a 5 (espinhos e folhas) sozinhos já levariam o modelo para ~7.

# Cocórion (`cocorion`): auditoria de detalhes, rodada 2 (n42)

Fontes: ficha `005_cocorion_{ficha,arte,vistas,detalhes,expressoes}.png`, `005_cocorion_especificacao.md`,
`005_cocorion_reconstrucao.md`, `revisao/n42_{comp,vistas,3-4,rosto}.png` e, com peso maior, `fotos_jogo/cocorion_jogo.png`.
A régua é o Esporocó aprovado (`fotos_jogo/esporoco_jogo.png`): no jogo ele lê como penas orgânicas e escalonadas,
sem placas nem varetas. O Cocórion ainda não chega lá, principalmente na cauda, nas asas e na crista.

## TOP 10 PROBLEMAS

### 1. Cauda: varetas retas e horizontais em vez de leque alto e curvo (lateral, traseira e foto do jogo)
- **Modelo:** 5 ou 6 penas finas e compridas (3 a 4 px de altura), quase paralelas e saindo para trás entre +15° e
  −25°. Parecem dedos ou varetas, e a ponta da mais longa passa da silhueta da ficha (no `_comp` lateral, grande área azul de sobra
  atrás). Nenhuma pena sobe: o topo da cauda fica abaixo do ombro. Na foto do jogo, de lado e de trás, é o que mais
  separa o modelo da ficha.
- **Ficha (lateral D/E):** é um leque que se abre do quadril num arco de ~+70° (para cima) até ~−60° (para baixo). As penas de cima sobem até
  a altura da base da crista e dos olhos, e as de baixo descem até perto do joelho. Cada pena é LARGA (a altura de cada
  uma é ~1/2 da altura da cabeça), sai estreita da base, engorda no meio e termina numa ponta creme que dobra
  levemente para baixo, como gancho. As pontas ficam separadas e escalonadas em profundidade. O alcance para trás é
  ~0,9 bloco a partir das costas; o modelo vai mais longe. No `_comp`, o vermelho em cima da cauda, na lateral E, é
  justamente o arco superior que falta.
- **Correção:** reconstruir a cauda com 5 penas principais (e 2 ou 3 secundárias atrás), pivô na raiz da cauda,
  em ~1,0 bloco de altura. Ângulos das principais: +70°, +45°, +15°, −20° e −50°.
  - Comprimento: 12 a 14 un. nas de cima e 10 a 12 nas de baixo; nenhuma ponta mais de ~15 un. atrás das costas.
  - Perfil de cada pena: 2 px na base, 6 a 7 px no meio, ponta de 2 px. Faça com 3 cuboides inclinados em degraus
    pequenos (5° a 10° de diferença entre eles), que curvam para cima e depois dobram a ponta ~20° para baixo.
  - A pena de +70° deve ter a ponta a ~1,6 bloco do chão, logo atrás da crista.

### 2. Asas de frente: pilares retangulares soltos em vez de capa trapezoidal com a espiral visível
- **Modelo (vista de frente e foto do jogo):** cada asa é uma placa vertical retangular de largura constante, paralela ao
  tronco e afastada dele por uma fresta escura. Parece um braço ou um escudo. O topo é um "ombro" quadrado abaixo
  das barbelas. A espiral fica na face lateral e, de frente, aparece só como um fio verde na borda.
- **Ficha (frente):** as asas são uma capa (haori): nascem colando no pescoço, logo abaixo da barbela, e descem
  ALARGANDO num trapézio. A borda de fora abre em diagonal e é recortada em várias pontas de pena. A borda interna
  forma uma "lapela" junto ao peito, sem fresta, deixando só uma coluna central do peito e o X à mostra (~1/3 da
  largura do corpo). A face da asa fica voltada ~30° para a frente, e por isso a espiral verde aparece inteira de
  frente, na altura do peito.
- **Correção:**
  - Girar cada `asa_d`/`asa_e` ~30° em Y, com a face externa virada para a frente, e abrir ~10° em Z, para a borda de baixo
    ficar mais longe do corpo que o topo.
  - Largura: no topo ~5 un.; na barra, 8 a 9 un.
  - Encostar a borda interna no peito, sem fresta.
  - Subir o topo da asa até a base do pescoço, cobrindo o "ombro" quadrado.
  - Na borda externa e na barra, usar 4 ou 5 penas pontudas de comprimentos diferentes (pontas de 1 a 2 px), terminando
    perto da barra da hakama.

### 3. Crista: torre central, pontas rombudas de cubo e leque simétrico
- **Modelo:**
  - **Frente (`_rosto` e jogo):** há uma "chaminé" central de cubos empilhados com um bloco claro no topo. Em volta, um
    leque quase espelhado de placas largas e retangulares.
  - **Lado e trás:** as mechas terminam em pontas QUADRADAS, com o topo do cubo visível como um quadradinho claro, e
    aparecem quadrados concêntricos em degrau na lateral da cabeça (atrás do olho) e na nuca.
  - **Testa:** a crista começa acima de uma testa lisa e reta.
- **Ficha (detalhe "Crista estilo Sanemi", neutra, lateral):** mechas de base larga e ponta AFIADA (triângulo em
  degraus), varridas para trás e para cima.
  - **De lado:** uma sequência em escama, de 6 a 7 espinhos que saem da testa e da nuca e apontam para trás.
  - **De frente:** há um bloco central no topo e, logo abaixo, 2 espinhos laterais na altura das têmporas, apontando para fora.
    Na testa, as mechas descem em bico baixo e irregular, por cima das sobrancelhas.
  - **Assimetria:** a do lado esquerdo da arte é mais cheia que a do direito.
- **Correção:**
  - Trocar a torre central por 1 mecha central larga, de 6 un. na base, inclinada ~25° para trás.
  - Afilar a ponta de TODAS as mechas em 2 ou 3 degraus (6 → 4 → 2 → 1 px). Nenhuma pode terminar com face quadrada à vista.
  - Remover os quadrados concêntricos da lateral e da nuca e trocá-los por 2 ou 3 penas pontudas varridas para trás.
  - Acrescentar 2 ou 3 mechas curtas que descem até 1 un. acima das sobrancelhas, formando a franja da testa.
  - Desfazer o espelhamento: o lado esquerdo do personagem fica com 1 mecha a mais e 2 un. mais alto.

### 4. Textura de "parede de tijolo" no rosto e no corpo
- **Modelo (foto do jogo, de perto):** a face da cabeça, o peito, o dorso e as asas têm linhas cinza finas e
  regulares, horizontais e verticais intercaladas, como tijolos com argamassa. No rosto é o que mais chama atenção
  depois dos olhos.
- **Ficha:** a plumagem é creme com "telhas" de pena: plaquinhas de 2 a 3 px sobrepostas, cada uma com borda de
  baixo um tom mais escura (cinza-claro quente) e sem contorno em volta. O rosto é quase liso, com só 2 ou 3 degraus
  de sombra.
- **Correção:** apagar a grade de argamassa e pintar penas em escama, com fileiras desencontradas.
  - Cada pena é um retângulo de 3×2 px, com a linha de baixo em cinza-claro (ex.: #CFC6BA sobre creme #EDE6DA).
  - Na face do rosto, só sombra suave de 1 px sob as sobrancelhas e no canto do bico.
  - Nunca usar linhas verticais contínuas.

### 5. Cauda: cor e desenho das penas
- **Modelo:** cada vareta é creme em cima com uma faixa verde-escura estreita ao longo da borda de baixo, quase de ponta a ponta.
  As camadas parecem listras paralelas.
- **Ficha (detalhe "Cauda em camadas", lateral):** a alternância é por PENA e por PROFUNDIDADE.
  - As penas de fora (mais perto de quem olha) são creme, com o verde só no lado de dentro, perto da base.
  - As de trás são verde-escuras, com a PONTA creme (o último ~1/3).
  - O verde ocupa ~metade da cauda e forma blocos largos, não filetes.
- **Correção:**
  - Penas principais alternadas: as de fora creme, com a face interna verde-escura nos 2/3 da base; as de trás
    verde-escuras, com ponta creme nos últimos 4 a 5 px.
  - O verde-escuro (#2E5A2E aprox.) tem sombra verde mais profunda (#1F3F22) na face de baixo.
  - Eliminar a faixa verde contínua de 1 px.

### 6. Espiral da asa: traço fino e cauda em zigue-zague
- **Modelo (lateral e jogo):** o traço é de 1 px. O caracol é pequeno, no alto da asa, e dele sai uma "haste" diagonal em escada
  até a borda de baixo. Lembra um 9 rabiscado ou um galho.
- **Ficha (detalhe "Padrão da asa"):** o caracol é GROSSO (traço de ~1/10 da largura da asa, 2 a 3 px), com 1,5 volta, e ocupa
  ~55% da largura da asa, centrado no terço de cima. Dele sai uma cauda curta e grossa que desce para a frente e faz
  um gancho de volta para trás, terminando em ponta (forma de "ɘ"/"ᘐ"). O desenho termina em ~60% da altura da asa,
  sem chegar à barra.
- **Correção:** redesenhar a espiral com traço de 2 px (3 px na volta externa), diâmetro ~6 px na face da asa de
  ~11 px. Cauda de ~4 px de comprimento com gancho de 2 px. Remover a escada diagonal até a borda. Na asa girada
  (item 2), centralizar o caracol na face que fica visível de frente.

### 7. Sobrancelhas: varetas finas e compridas em vez de blocos grossos
- **Modelo (`_rosto` e jogo):** cada sobrancelha é uma barra fina (2 px) e longa.
  - **De frente:** a ponta externa sobe e passa da largura da cabeça, como chifre.
  - **De lado:** espeta para a frente além do rosto, como antena.
  - Fica um vão entre a barra e o olho.
- **Ficha (neutra, frente, arte):** cada sobrancelha é um bloco GROSSO (altura ~1/2 da altura do olho), mais largo
  na ponta interna. Fica apoiado no próprio olho, cobrindo a pálpebra de cima. A inclinação é forte para baixo, em
  direção ao bico. A ponta externa termina dentro do contorno da cabeça, a ~1 un. da borda.
  A projeção para a frente é de só 1 un.
- **Correção:**
  - Engrossar para 3 un. na ponta interna e 2 un. na externa.
  - Encurtar ~25%, para a ponta externa ficar dentro da silhueta da cabeça.
  - Baixar a sobrancelha até encostar no topo da íris, sem vão.
  - Projetar só 1 un. à frente da face.

### 8. Marcas do rosto: borrão na testa e cicatriz da bochecha no desenho errado
- **Modelo:** a testa tem um borrão vermelho irregular ("respingo") com pingos soltos.
  - Na bochecha esquerda do personagem (à direita de quem olha) há um risco único inclinado.
  - Na outra bochecha há um X de traço de 1 px.
- **Ficha (neutra e arte):**
  - **Testa:** a marca é uma pequena CRUZ/asterisco de traço fino e limpo, com 2 traços cruzados e pontinhas, deslocada para o
    lado esquerdo do personagem, acima do olho.
  - **Bochecha:** a cicatriz também é um asterisco/cruz irregular de traço de 1 px, com 4 a 6 pontas, sob o olho.
  - **Outra lateral:** só 1 ou 2 marquinhas pequenas perto do olho.
- **Correção:**
  - Trocar o borrão da testa por uma cruz de 5×5 px com traços de 1 px e as pontas quebradas em 1 px, 1 un. acima e 1 un. para dentro do
    olho esquerdo do personagem.
  - Na bochecha, desenhar um asterisco de 6×6 px (X mais um traço curto horizontal).
  - O risco solitário da outra bochecha vira 2 pontos e 1 risco curto de 2 px junto ao canto do olho.

### 9. X do peito: cruzamento baixo e braços de cima longos demais
- **Modelo (frente e jogo):** os braços de cima saem das bordas externas dos ombros e descem longos. O cruzamento fica
  baixo, a ~75% da altura do peito, perto do cinto, e os braços de baixo são curtos. Lê como um "V" de suspensório.
- **Ficha (detalhe "Cicatrizes de batalha"):** é um X grande e simétrico, com o cruzamento no CENTRO do peito (50%) e
  os 4 braços de comprimento parecido, em traço de 2 px escalonado.
  - Os braços de cima começam a ~2 un. de cada lateral do peito, logo abaixo da gola.
  - Os de baixo chegam até o cinto.
  - Há pequenos ganchos e ticks de 1 px nas pontas e algumas marquinhas escuras.
- **Correção:** redesenhar o X no painel visível do peito (entre as lapelas das asas, item 2).
  - Cruzamento na metade da altura entre a gola e o cinto.
  - Pontas de cima a 2 un. das bordas do painel; pontas de baixo encostando no cinto.
  - Traço de 2 px em degraus, com ticks de 1 px em vermelho-escuro (#8E1F1A) em 2 ou 3 pontas.
  - Seguir as facetas do peito sem achatá-lo.

### 10. Katana: pequena, quase vertical e sem a bainha visível
- **Modelo (frente e jogo):** só aparece um pedacinho: guarda amarela em cruz e um cabo curto, quase vertical,
  colado no quadril direito de quem olha, mais baixo que o cinto. Em tamanho, é ~1/2 da ficha. A bainha preta não
  aparece.
- **Ficha (frente e arte):**
  - **Cabo:** sai do cinto, à direita de quem olha, e sobe em DIAGONAL de ~45° para fora. A ponta passa da borda da asa,
    na altura do peito. O comprimento é ~1/3 da altura do tronco.
  - **Cores:** cabo verde-escuro com 4 ou 5 losangos brancos em sequência, tsuba dourada em cruz e ponteira amarela.
  - **Bainha:** preta, desce para trás. Na arte, a ponta preta com o terminal amarelo aparece atrás da perna de trás,
    perto do chão.
- **Correção:**
  - Cabo: 8 un. de comprimento e 2×2 de seção, inclinado ~45° para fora e para cima, saindo da altura do cinto. Tsuba de
    4×4 un.; 4 losangos brancos de 1 px no cabo.
  - Bainha: 14 a 16 un. de comprimento, preta, inclinada para baixo e para trás, com a ponta amarela de 2 un. visível
    atrás do quadril na vista lateral.

## OUTROS PROBLEMAS MENORES
- Patas de frente (jogo): os dedos são longos, finos e achatados, abertos em leque como um ancinho, com uma faixa
  laranja. Na ficha são curtos e robustos, cúbicos (comprimento além do pé ≤ 3 un., altura 2 a 3 un.), com garra preta grande (~1/2 do dedo).
- Faixa laranja-escura atravessando as pernas e os dedos: tirar e usar só amarelo-dourado, com sombra amarela mais escura.
- Bico: a mandíbula de baixo é laranja-amarronzada (fora da paleta); usar amarelo-dourado um tom abaixo. De lado, o gancho da
  ponta é exagerado (parece papagaio); deixar só 1 un. de queda.
- Esclera: o canto externo do olho é cinza-azulado. Na ficha é branco puro, e a íris é verde vivo com pupila preta junto ao bico.
- "Colarinho" de espinhos brancos que se abrem para fora sob a cabeça (`_rosto`): não existe na ficha. Trocar por
  penas em escama que descem do pescoço para o peito.
- Costas (traseira e jogo): há uma coluna central de blocos empilhados e listrados, com um ponto verde, que parece espinha ou
  zíper. Na ficha, o dorso é de penas brancas em escama, contínuas, e as asas cobrem os lados.
- Cintura: a faixa branca larga com um quadrado cinza no centro não bate com a ficha, que tem obi preto + cordão branco com
  nó e 2 tiras brancas pendentes à direita do centro.
- Hakama: tem ~12 pregas finas de 1 px, que lembram saia de tule. Na ficha são 4 ou 5 painéis largos por face, alternando preto e
  cinza-carvão, abrindo levemente em trapézio, com a barra em degraus.
- Crista com cor creme quente uniforme: na ficha é branca com sombra cinza-claro levemente fria nas faces de baixo das
  mechas.
- Barbelas: na frente cobrem o topo do peito. Encurtar ~2 un. para a ponta terminar logo abaixo da gola.

## O QUE JÁ ESTÁ FIEL
(Não repetido em detalhe, conforme a Rodada 2.) Paleta geral, olhos verdes, bico amarelo, barbelas vermelhas
duplas, hakama preta e patas amarelas com garras pretas: tudo isso está presente e no lugar certo.

## NOTA DE FIDELIDADE AOS DETALHES
**5,5 / 10.** Dos 10 problemas, 3 são de rosto: crista (3), sobrancelhas (7) e marcas (8). Contando a textura de
tijolo do rosto (4), são 4. O que mais impede o "igualzinho à ficha" no jogo é a silhueta lateral, com a cauda em
varetas, e a frontal, com as asas em pilares. Corrigidos os itens 1, 2 e 3, o modelo deve chegar ao nível do Esporocó aprovado.

# Auditoria 2 — Cocórvolt (`cocorvolt`), rodada n39

Fontes: `006_cocorvolt_{ficha,arte,vistas,detalhes,expressoes}.png` (sem especificação .md), `revisao/n39_{comp,vistas,3-4,rosto}.png`,
foto do jogo `fotos_jogo/cocorvolt_jogo.png` (peso maior). Régua: Esporocó aprovado (`esporoco_jogo.png`): silhuetas
cheias, partes grudadas no corpo, padrões legíveis e no desenho da ficha.

## TOP 10 PROBLEMAS

### 1. Cauda: penas em forma de "dedos/palitos" com ponta preta, separadas, abertas na horizontal
- **Região/vista:** cauda; foto do jogo (lados e 3/4), laterais da n39.
- **Modelo:** ~10 bastões retangulares retos, de largura constante, saindo radialmente de um cubo-eixo como um leque de
  dedos; cada pena é cinza-média com a PONTA em bloco preto quadrado; há vãos visíveis entre as penas; o leque se abre
  mais para trás/para baixo (no comp, azul = sobra embaixo, vermelho = falta em cima da cauda).
- **Ficha:** penas largas, AFINANDO até uma ponta (lâmina), levemente curvadas para cima, sobrepostas sem vão, formando
  uma massa em arco que sobe da altura do quadril até a altura dos olhos. Cada pena é de UM tom só, alternando carvão
  (#3a3a3e) e cinza-claro (#a8a8ac); não há pontas pretas em penas claras.
- **Correção:** trocar cada bastão por 2–3 cubos escalonados que diminuem de espessura para a ponta (ex.: 4→3→2 px de
  altura); girar o leque ~20° para cima, de modo que a pena mais alta chegue à altura do olho e a mais baixa à altura
  do joelho; sobrepor as penas em ~1/3 da largura para fechar os vãos; pintar pena inteira em um tom, alternando
  carvão / cinza-claro, e remover os blocos pretos das pontas; esconder o cubo-eixo atrás das penas.

### 2. Padrão do traje (avental da frente): raio virou uma onda/cobra em "S"
- **Região/vista:** painel abaixo do cinto; frente (foto do jogo, n39 frente e 3/4).
- **Modelo:** faixa amarela sinuosa contínua, com 4–5 curvas arredondadas de alto a baixo, lida como serpente/onda.
- **Ficha (`_detalhes` "Padrão do Traje" e `_arte`):** UM raio angular: segmentos retos diagonais com cantos vivos
  (forma ϟ, 2 dobras), grosso no topo e terminando em ponta fina embaixo; ocupa ~60% da largura do painel.
- **Correção:** repintar como raio de 3 segmentos: diagonal da borda superior direita até ~40% da altura, degrau
  horizontal para a esquerda (2 px), segunda diagonal até ~75%, degrau, e ponta final afinando para 1 px. Cantos em
  degrau de pixel, sem curvas. Manter fundo azul-marinho e moldura dourada.

### 3. Ombreiras: "cabides" de barras finas flutuando (frente) e placa com letra "Z" (lado)
- **Região/vista:** ombros; frente e lateral (foto do jogo mostra as duas coisas).
- **Modelo:** na frente, cada ombreira é uma armação de barras finas azuis com contorno dourado estendida na horizontal
  para fora do corpo, com uma plaquinha vertical na ponta, deixando vão de ar até o tronco; de lado, uma caixa retangular
  azul com uma letra "Z" dourada, como um baú/placa de bagagem.
- **Ficha:** uma placa de armadura ÚNICA e cheia, chanfrada, apoiada em cima do ombro e descendo pela lateral do braço
  até ~meio da altura do peito; fundo escuro (azul-marinho quase preto / carvão), borda dourada GROSSA (~2 px) e na
  face externa dois pequenos raios em zigue-zague dourados (padrão irregular, não letra).
- **Correção:** apagar as barras horizontais; modelar um bloco de ~5×5×4 px por ombro encostado no tronco, com o topo
  inclinado ~15° para fora e um segundo degrau mais baixo cobrindo o braço; textura: fundo #1e2440, borda dourada 2 px,
  e na face externa 2 zigue-zagues de 3 segmentos cada (sem formato de letra).

### 4. Asas/braços: varetas finas abertas em V em vez de "mangas" de pena largas
- **Região/vista:** asas; frente (foto do jogo), 3/4.
- **Modelo:** duas hastes cinzas compridas, finas (~1/5 da largura do tronco), inclinadas ~30° para fora, com vão entre
  elas e o corpo, terminando em várias pontinhas tipo dedos.
- **Ficha:** asas largas (~metade da largura do tronco cada), penduradas QUASE verticais encostadas na lateral do
  robe, em camadas de penas cinza-claro e cinza-médio com bordas irregulares; as pontas chegam ao nível do quadril/joelho.
- **Correção:** alargar cada asa para ~1/2 do tronco, colar na lateral (inclinação ≤10°), empilhar 3 camadas de
  "telhas" de pena, cada uma terminando em 3–4 pontas serrilhadas; tons cinza-claro (#b4b4b8) por cima e cinza-médio
  (#7a7a80) nas camadas de baixo.

### 5. Bico: coluna estreita/"punho" empilhado em vez de cunha larga em gancho
- **Região/vista:** rosto; frente e lado (n39_rosto, foto do jogo).
- **Modelo:** de frente, bico estreito (~1/4 da cabeça) que afina para baixo como um funil e desce até o barbilhão; de
  lado, 3 blocos amarelos empilhados verticalmente, parecendo dedos dobrados.
- **Ficha (neutra):** bico largo e curto, ~1/3 da largura da cabeça, projetando-se bem para frente (~1/3 da
  profundidade da cabeça), parte de cima reta com narina escura, ponta curvada para baixo em gancho; amarelo-ouro em
  cima, laranja embaixo.
- **Correção:** um bloco base de 4 px de largura × 2 px de altura × 4 px de projeção, logo abaixo da linha dos olhos;
  na ponta, 1 bloco de 2 px caindo 1 px abaixo da base (gancho); narina 1 px escura no topo; topo #f2b51c, face de
  baixo #e08a14. Remover a "haste" que liga o bico ao barbilhão.

### 6. Chapéu: padrão é um anel ondulado contínuo numa faixa marrom, não raios separados
- **Região/vista:** topo do chapéu; frente/3/4 e foto do jogo.
- **Modelo:** faixa circular marrom-acastanhada com uma linha amarela ondulada que dá a volta inteira, como uma coroa
  ou fita.
- **Ficha (`_detalhes` "Chapéu (Raiden)", `_arte`):** cone carvão/cinza-escuro (frio, não marrom) com 4–6 RACHADURAS
  de raio separadas, em zigue-zague de cantos vivos, algumas descendo radialmente do topo para a aba; brilho amarelo forte.
- **Correção:** trocar o marrom (#5a4c44) por carvão frio (#45464c) na parte de cima do cone; apagar o anel ondulado;
  pintar 5 raios independentes de 3–4 segmentos, alternando orientação radial e diagonal, cada um com 2 px de largura
  e terminando em ponta.

### 7. Chapéu: cone baixo demais, aba larga e fina, topo com tufo espetado
- **Região/vista:** silhueta do chapéu; todas as vistas (comp: vermelho no pico, azul nas pontas da aba).
- **Modelo:** cone achatado, aba que passa muito da cabeça e é uma lâmina fina (guarda-chuva); no topo um tufo de
  palha espetado.
- **Ficha:** cone mais alto (pico ~1,5× a altura atual), aba que passa ~1 largura de talismã de cada lado (não mais),
  borda da aba GROSSA (2 px) com segmentação de tábuas de palha visível; pico limpo, um pequeno bico tan.
- **Correção:** subir o pico ~2 px; reduzir o raio da aba ~10%; engrossar a borda para 2 px com linhas de tábua
  #c9a463 a cada 3 px; trocar o tufo por um cubo único de 2×2 px tan.

### 8. Olhos: retângulos claros e chapados, sem brilho elétrico
- **Região/vista:** rosto de frente (rosto e foto do jogo).
- **Modelo:** retângulos horizontais grandes, preenchidos de ciano bem pálido quase branco com contorno azul — leem
  como "janelas/óculos".
- **Ficha (neutra, `_detalhes` "Olhos Eletrificados"):** fendas estreitas (altura ~metade da atual), inclinadas para
  baixo em direção ao bico (V bravo), azul elétrico saturado (#2f6bff) com núcleo branco pequeno no lado de dentro.
- **Correção:** reduzir altura do olho para 2 px; cortar o canto de cima do lado do bico (inclinação de 1 px); pintar
  borda azul #1a3fd0, miolo #3f86ff e 1×2 px branco no meio; colocar esses pixels na glowmask.

### 9. Penas da face/bochecha: muitos cubinhos inclinados soltos ("couve-flor")
- **Região/vista:** laterais da cabeça; frente, lado, 3/4, foto do jogo.
- **Modelo:** dezenas de cubos pequenos girados em vários ângulos colados nas laterais e atrás da cabeça, textura
  ruidosa, sem direção.
- **Ficha:** 3–4 penas GRANDES em camadas, pontudas, saindo das bochechas para fora/baixo e escorrendo pelo pescoço até
  os ombros (juba), cinza-claro com camada inferior cinza-médio; a cabeça fica mais larga embaixo que em cima.
- **Correção:** substituir os cubinhos por 3 camadas por lado de penas de 4–6 px de comprimento, todas apontando para
  fora e para baixo (~30–45°), sobrepostas como telhas; camada de cima #c4c4c8, de baixo #8a8a90; atrás da cabeça, 2
  camadas descendo até a capa.

### 10. Barbilhão: babador largo de 4 tiras em vez de 2 lóbulos estreitos
- **Região/vista:** rosto; frente (foto do jogo lê como um laço vermelho).
- **Modelo:** bloco vermelho mais largo que o bico, com 3–4 tiras penduradas.
- **Ficha:** 2 lóbulos vermelhos estreitos, juntos, da largura do bico ou menos, logo abaixo dele; o da esquerda
  (do observador) um pouco mais comprido; vermelho #d42a24 com sombra #9c1a18.
- **Correção:** reduzir para 2 lóbulos de 2 px de largura × 5 e 4 px de altura, centralizados sob o bico, sem placa
  horizontal por cima.

## OUTROS PROBLEMAS MENORES
- Costas: coluna central em xadrez preto/branco; na ficha é uma coluna carvão lisa em degraus.
- Costas: a capa azul com barra dourada cobre só o topo dos ombros; na ficha ela cobre o terço superior das costas.
- Quadril: blocos pretos volumosos dos lados do avental parecem bolsos; na ficha ali há saia de penas cinza serrilhadas.
- Talismã visto de lado vira uma vareta comprida até o ombro (parece cabo de guarda-chuva); dar 1 px de espessura e
  encurtar o cordão.
- Raio dos talismãs fino demais; na ficha ocupa ~60% da largura do miolo.
- Raios da cauda: rabiscos finos de 1 px; na ficha são rachaduras grossas e brilhantes, uma por pena carvão.
- Gola em V: faixas escuras de lapela estreitas; na ficha são largas (≈2 px) e debruadas de dourado.
- Nó do cinto (obi): na ficha cai ao lado do emblema, à direita do observador, com pontas mais longas.
- Pés: base preta contínua sob os dedos; na ficha só as garras são escuras, os dedos amarelos tocam o chão.
- Canela com amarelo-mostarda escuro; a ficha usa amarelo-ouro mais limpo (#f0b820).

## O QUE JÁ ESTÁ FIEL
- Emblema do cinto (octógono dourado, centro preto, raio amarelo).
- Talismãs: retângulo dourado com miolo escuro e raio, pendurados dos dois lados da aba.
- Paleta geral do robe azul-marinho com debrum dourado e cinto preto.
- Proporção cabeça/chapéu/corpo e pernas amarelas grossas.

## NOTA DE FIDELIDADE AOS DETALHES
**5,5 / 10** — 4 dos 10 problemas principais são de rosto (bico, olhos, penas da face, barbilhão).

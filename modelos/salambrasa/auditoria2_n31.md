# Auditoria 2 — Salambrasa (quadrúpede), rodada n31

Fontes: ficha `012_salambrasa_*` (ficha, arte, vistas, detalhes, expressão NEUTRA), modelo `revisao/n31_*`, foto do jogo
`fotos_jogo/salambrasa_jogo.png` (peso maior), régua `esporoco_jogo.png`.

## TOP 10 PROBLEMAS (do mais visível para o menos visível)

### 1. Bico: de frente parece focinho de porco, de lado é um toco curto (ROSTO)
- **Região/vista:** cabeça, frente e lateral; na foto do jogo, de frente, é a primeira coisa que se vê.
- **Modelo:** de frente, um retângulo malva plano com outro bloco vertical no meio e dois "furinhos" em cima: lê como
  focinho/nariz de robô. De lado, uma caixa curta e reta (~1/4 do comprimento da cabeça) com a ponta caída em bloco separado.
- **Ficha:** de frente, uma CUNHA em V malva clara (#8a7480) saindo debaixo do vértice da sobrancelha: larga em cima
  (~1/3 da largura da cabeça), afinando até uma ponta embaixo, sem nada no meio. De lado, bico comprido e adunco: ~1/2 do
  comprimento da cabeça, dorso reto, ponta curvando para baixo, uma narina escura pequena perto da base.
- **Correção:** apagar o bloco vertical central e o "nariz" retangular. Base do bico 4 px de largura sob o vértice da
  sobrancelha, afinando em degraus 4→3→2→1 px para baixo (de frente). De lado, alongar para ~1/2 da cabeça (ex.: 4–5 px
  à frente da face), dorso reto, último pixel/cubo da ponta 1 px abaixo da linha inferior, narina = 1 px escuro a 1 px da base.
  Cor única malva clara, faixa inferior 1 tom mais escuro.

### 2. Sobrancelha vira aba de boné preta, e a cabeça inteira está escura demais (ROSTO)
- **Região/vista:** testa/olhos, todas as vistas; na foto lateral do jogo a aba passa da ponta do bico.
- **Modelo:** placa quase preta (#2a2228) larga, plana, que se projeta para a frente além da face e até além do bico (de
  lado parece boné). O olho fica inteiro, redondo, ABAIXO da placa: expressão de susto/neutra-redonda.
- **Ficha (neutra):** sobrancelha é um capacete/viseira em V, cor cinza-malva (#6e5c68, mais CLARA que o corpo), que
  desce em diagonal para o centro, terminando no vértice sobre o bico; ela CORTA o topo do olho em diagonal (olhar bravo).
  Não ultrapassa a face mais que ~1 px e não passa do meio do bico. A face é cinza-arroxeada média, não preta.
- **Correção:** encurtar a projeção frontal da sobrancelha para 1 px; inclinar cada metade ~20° descendo para o centro (V);
  pintar em #6e5c68 com topo 1 tom mais claro. Baixar a borda inferior da sobrancelha para cobrir o 1/4 superior do olho
  em diagonal (mais coberto do lado do bico). Clarear a face para #4a3c46.

### 3. Placa da barriga: caixotes marrom-caramelo em vez de escamas laranja em chevron
- **Região/vista:** peito/barriga, frente e 3/4; na foto de frente ocupa o centro do corpo.
- **Modelo:** 4–5 caixas tan/marrom (#b07a40, fora da paleta) empilhadas, retas, com frisos claros brilhantes, que
  SOBRESSAEM do peito e ALARGAM para baixo (parece casco de tartaruga/gaveteiro).
- **Ficha:** ~6 escamas laranja (#f7931e) em chevron (cada uma levemente em V, pontas para cima), rentes ao corpo, mais
  claras em cima (pêssego #f9b25a) e mais quentes embaixo; a placa é LARGA no topo do peito e AFINA até um fundo
  arredondado entre as patas dianteiras.
- **Correção:** trocar o marrom por laranja da paleta (gradiente #f9b25a → #f7931e → #f05a1e de cima para baixo);
  reduzir o relevo para 0,5–1 px; segmentos com bordas em V raso (linha escura #c05a10 de 1 px entre eles, sem friso
  amarelo); largura decrescente de cima para baixo (ex.: 8→7→6→5→4 px), último segmento arredondado.

### 4. Pescoço sumido e juba virando "babador" + ombreiras de blocos retangulares
- **Região/vista:** pescoço/juba (Pelagem Ígnea), frente, lateral e 3/4.
- **Modelo:** a cabeça encosta direto no peito; a juba é um anel de blocos retangulares grossos (topo vermelho, meio
  laranja-ferrugem, canto amarelo) que envolve a cara pela frente e forma dois montes nos ombros, tapando o peito.
  Tom ferrugem/marrom (#9a4a18) que não está na paleta.
- **Ficha:** pescoço escuro visível, em curva em S, com faixa laranja na frente/baixo do pescoço que continua na barriga.
  A juba nasce ATRÁS e ABAIXO da bochecha e cai pelas costas do pescoço até a cernelha; de frente aparece só como duas
  pequenas abas laranja-amarelas ao lado do queixo. Penas PONTUDAS (losango alongado), em camadas, gradiente vermelho
  (#c0282a) na raiz → laranja (#f05a1e/#f7931e) → amarelo (#f5c518) na ponta, com algumas penas carvão misturadas.
- **Correção:** subir a cabeça ~2 px e mostrar 2–3 px de pescoço escuro com faixa laranja na frente. Tirar as penas que
  ficam na frente da cara/peito (deixar de frente só 2 abas pequenas sob as bochechas). Concentrar a juba na nuca e no
  dorso do pescoço, apontando para trás-baixo. Cada pena: afinar a ponta em 2 degraus (largura 3→2→1 px), sem cantos
  quadrados; trocar o ferrugem por #f05a1e/#f7931e.

### 5. Crista: monte de cubos em vez de lâminas inclinadas para trás
- **Região/vista:** topo da cabeça, lateral e 3/4 (frente está aceitável).
- **Modelo:** 8–10 cubos vermelhos quase iguais, grossos, amontoados numa bola/pirâmide; de lado a massa é tão alta
  quanto a cabeça e sobe quase vertical.
- **Ficha (Crista de Brasa):** 4–5 LÂMINAS (placas finas) vermelhas, escalonadas em leque, cada uma inclinada ~30–40°
  para TRÁS, a de trás mais alta; topos com vermelho mais claro (#e8443a) e lados #c0282a; a base fica atrás da
  sobrancelha, que aparece por baixo.
- **Correção:** substituir os cubos por 4–5 placas de ~2 px de espessura e comprimentos crescentes de frente para trás,
  rotacionadas ~35° para trás, sobrepostas como telhas; topo de cada placa 1 tom mais claro. Altura total ~0,8 da
  altura da cabeça. Manter a vista de frente estreita como está.

### 6. Corpo preto chapado: falta o meio-tom cinza-malva das placas e a faixa laranja do flanco
- **Região/vista:** tronco, ombros e lateral; foto do jogo de lado.
- **Modelo:** tronco, patas, ombros e asa quase todos #2a2228 uniforme; só um filete laranja fino no rodapé do flanco.
- **Ficha:** corpo carvão-arroxeado (#3e3038) com placas de ombro e penas de cobertura em cinza-malva (#6e5c68); a
  barriga/parte de baixo do flanco é LARANJA visível de lado (~1/3 inferior do tronco, em gradiente laranja→escuro),
  contínua com a faixa laranja do pescoço e da cauda.
- **Correção:** subir o corpo para #3e3038; pintar placas do ombro e coberturas da asa em #6e5c68 com borda #8a7480;
  pintar o terço inferior do flanco em laranja #f7931e com transição de 2 px para o carvão.

### 7. Dorso com "ameias" e silhueta de caixa em vez do lombo arqueado liso
- **Região/vista:** costas, lateral e 3/4; bem visível na foto lateral do jogo.
- **Modelo:** linha do dorso em degraus/blocos salientes (parecem ameias de castelo e espinhos quadrados), tronco reto
  e comprido como um caixote.
- **Ficha:** lombo LISO e arqueado (ponto mais alto no meio do tronco), sem espinhos nem cristas dorsais; transição
  suave do pescoço ao tronco e do tronco à cauda.
- **Correção:** remover os blocos salientes do dorso; construir o lombo com 3 seções de altura 1 px diferente
  (baixa–alta–baixa) para formar arco; chanfrar os cantos superiores do tronco.

### 8. Cauda: fita larga e achatada com manchas gigantes fundidas e listras laranja nas laterais
- **Região/vista:** cauda, 3/4 e traseira; na foto de trás/3-4 do jogo é a maior massa da imagem.
- **Modelo:** em perspectiva a cauda é uma fita larga e chata (largura bem maior que a altura), com manchas amarelas
  enormes que ocupam toda a largura e se fundem; listras laranja corridas ao longo das laterais; ponta escura cortada reta.
- **Ficha (Cauda Incandescente):** tubo redondo, grosso na base e afinando até uma ponta arredondada que aponta para a
  frente; manchas octogonais amarelas (#f5c518) com halo laranja, ~1/2 da largura da cauda, numa fileira no dorso com
  intervalos escuros de ~1 mancha entre elas; faixa laranja só na face de baixo/interna da curva.
- **Correção:** deixar a seção da cauda quadrada (largura = altura) e afinar de ~6 px na base para ~2 px na ponta;
  manchas com no máximo 1/2 da largura, separadas por ≥ 1 mancha de carvão; tirar as listras laranja laterais e pôr uma
  faixa laranja só na face inferior; ponta com 1 cubo menor arredondando.

### 9. Patas: "meias listradas" e colunas grossas demais; dedos cinza neutro
- **Região/vista:** pernas e pés, frente e lateral.
- **Modelo:** canela com duas faixas laranja separadas por listra marrom (meia listrada); pernas grossas como pilares;
  pé = chapa escura com 3 cubos cinza-claros neutros (#b8b8bc).
- **Ficha (Patas):** coxa carvão, canela com UMA faixa laranja contínua em gradiente (laranja em cima → amarelo-laranja
  embaixo), perna mais fina que a coxa; pé malva (#6e5c68) robusto com 3 dedos longos à frente em malva-rosado claro
  (#bfa9b3) e 1 dedo atrás.
- **Correção:** apagar a listra marrom do meio da canela e fazer gradiente único #f05a1e→#f7931e; afinar a canela
  1 px de cada lado; pintar o pé em #6e5c68 e os dedos em #bfa9b3 (topo #d2c0c8); alongar os dedos da frente +1 px e
  acrescentar 1 dedo traseiro curto.

### 10. Asa: leque horizontal curto e listrado em vez de penas pontudas caindo para trás
- **Região/vista:** asa no ombro, lateral e 3/4.
- **Modelo:** coberturas escuras + leque de penas paralelas horizontais, curtas, com bordas amarelas em listra
  (parece persiana); a rachadura em Y das Placas Quentes está presente.
- **Ficha:** coberturas cinza-malva em placas; penas de voo PONTUDAS, em leque abrindo para trás e para BAIXO
  (~30° abaixo da horizontal), indo até o meio do tronco, gradiente vermelho → laranja → amarelo na ponta.
- **Correção:** girar o leque ~30° para baixo-trás; alongar as 2–3 penas de baixo até o meio do tronco; ponta de
  cada pena afinando em degraus; amarelo só na ponta, não como borda corrida.

## OUTROS PROBLEMAS MENORES
- Manchas do corpo: poucas e pequenas no tronco (~4 de cada lado); a ficha tem ~6–7 em duas fileiras, octogonais, maiores.
- Manchas no render de prévia saem mostarda (#b8a020); no jogo estão melhores, mas confirmar #f5c518 + halo #f7931e.
- Olho: pupila ok, mas falta o pequeno brilho branco no canto superior e a íris poderia ser laranja-avermelhada (#e04a1e) mais viva.
- Os frisos amarelos brilhantes nas bordas das escamas da barriga não existem na ficha.
- Placas Quentes: as rachaduras em Y deveriam aparecer também em 1–2 placas do dorso perto do ombro, não só uma.
- Traseira: a parte de baixo do quadril mostra caixas tan da barriga; na ficha é laranja contínuo.
- Dedos: cubos todos iguais; na ficha o do meio é um pouco maior.
- Juba: faltam algumas penas carvão misturadas às coloridas (a ficha alterna).

## O QUE JÁ ESTÁ FIEL
(não repetido nesta rodada, conforme instrução)

## NOTA DE FIDELIDADE AOS DETALHES
**5,5 / 10.** 3 dos 10 problemas são da cabeça (2 de rosto estrito: bico e sobrancelha/olho; 1 de crista).
Comparado com o Esporocó aprovado, que lê "igual à ficha" de perto, aqui o bico, a viseira preta e a barriga caramelo
ainda fazem um fã estranhar logo na vista de frente.

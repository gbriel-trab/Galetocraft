# Auditoria 2 do Renacocó, rodada r34

Auditor independente. O foco está nos olhares 1 (fidelidade) e 4 (textura) da especificação. O peso maior foi para a foto do jogo (`fotos_jogo/renacoco_jogo.png`), comparada com a arte grande `019_renacoco_arte.png`. Também consultei `r34_comp`, `r34_vistas`, `r34_3-4` e `r34_rosto`. A régua é o Esporocó aprovado.

## TOP 10 PROBLEMAS

**1. Manto em forma de "barraca": silhueta lateral, 3/4 traseira e frente**
- **Modelo:** na foto, as duas figuras de 3/4 mostram o manto como um cone fechado do ombro ao chão, em volta do corpo inteiro. Peito, asas e pernas somem, e a cabeça parece pequena em cima de uma tenda roxa. De frente, o ombro é largo e quadrado (sobra azul no `comp`). Os painéis da frente terminam na altura do joelho e a barra fica reta. Faltam as pontas abertas que tocam o chão (falta vermelha nos cantos inferiores do `comp`).
- **Arte:** o manto pende dos medalhões e cai para TRÁS em diagonal. Na 3/4 o lado do corpo fica aberto: peito azul, asa e pernas aparecem por inteiro. A ponta de trás arrasta no chão bem atrás dos pés e termina em bico. De frente, o manto é um "A": ombro estreito, que se abre até o chão com pontas além dos pés.
- **Correção:**
  - Na vista lateral, a borda da frente do manto deve ir do medalhão em linha reta até o chão, na altura do calcanhar ou atrás dele. Nada de manto na frente da coxa.
  - Abra o lado do manto, deixando ~40% da profundidade do tronco à mostra (asa e coxa).
  - Estenda a cauda do manto ~1 comprimento de corpo atrás do calcanhar, afinando até uma ponta no chão.
  - De frente, recolha o ombro para a largura do tronco + ~2 px de cada lado. Abra até ~1,6× essa largura na barra.
  - Desça os painéis da frente até o chão, terminando em ponta, e não em barra reta na altura do joelho.

**2. Crista lida como coroa: cabeça, frente e lado**
- **Modelo:** fileira simétrica de espetos verticais com uma haste central reta, como uma coroa (o que a especificação proíbe). As pontas são blocos quadrados. O amarelo tem manchas cáqui/oliva (~#b79c37), e no jogo parece "suja".
- **Arte:** chama de plumas que sobe e se inclina ~30–45° para TRÁS, em 3 camadas:
  - na frente, penas curtas azul-claras na base;
  - no meio, amarelas longas;
  - atrás, as mais longas.
  Todas têm ponta afilada. De frente, a crista abre em leque com ~1,3× a largura da cabeça e altura ≈ altura da cabeça. A cor é amarelo-limão claro (~#fbd966) com realce quase branco.
- **Correção:**
  - Remova a haste central vertical.
  - Incline todas as plumas para trás e faça as de trás mais longas que as da frente.
  - Afine cada ponta (último pixel com 1 px de largura).
  - Abra o leque lateralmente.
  - Troque os tons cáqui por amarelo-limão e use o dourado só na sombra.

**3. Barbela em forma de gravata: rosto, frente e lado**
- **Modelo:** retângulo vermelho comprido, pendurado do bico até o meio do pescoço (≈ altura da cabeça). Na foto de frente, parece uma gravata.
- **Arte (neutra e 3/4):** barbela pequena e arredondada, de dois lóbulos, logo abaixo da base do bico. Mede ~1/3 da altura da cabeça e tem a largura do bico.
- **Correção:** encurtar para 3–4 px de altura e dividir em 2 lóbulos arredondados (cantos de baixo recortados). Colar sob a base do bico, sem descer pelo pescoço.

**4. Cauda tripla: caminho e pontas**
- **Modelo:**
  - as 3 correntes saem paralelas e retas, na horizontal, a meia altura das costas e por cima do manto;
  - as pontas são blocos amarelos rombudos com uma faixa em degradê azul na base, parecendo "punhos" ou pincéis;
  - na vista traseira, as penas da cauda sobem pelas costas e cobrem o emblema.
- **Arte:** as 3 correntes saem do quadril e fazem curvas em arco, abertas em leque:
  - a de cima sobe até a altura da cabeça;
  - a do meio fica na horizontal;
  - a de baixo desce.
  Cada uma termina num leque de 4–5 penas longas e pontudas. São amarelas, com 1–2 penas azul/azul-claro intercaladas no meio do leque (não em faixa na base). Na vista de trás, a cauda fica escondida atrás do manto.
- **Correção:**
  - Dobre cada corrente em arco, com o elo do meio ~2–3 px acima da reta entre a raiz e a ponta, e abra o leque entre as 3 (~25° de diferença).
  - Baixe a raiz para o quadril, sob a borda do manto.
  - Troque as pontas rombudas por 4–5 penas afiladas em leque, com o azul como penas inteiras intercaladas.
  - Garanta que, de trás, nada da cauda passe por cima do emblema.

**5. Cabeça escura e sem moldura de penas do rosto: rosto, 3/4**
- **Modelo:**
  - a cabeça é um bloco azul médio-escuro (~#03669c) de laterais lisas;
  - atrás dela há só alguns blocos azuis pequenos;
  - não há nenhum amarelo na lateral do rosto.
- **Arte:**
  - o topo da cabeça e a testa são azul-claro/ciano, e o azul forte fica só nas bochechas e na nuca;
  - atrás do olho saem tufos grandes de penas do rosto que formam uma moldura nobre (exigência da especificação): 2–3 penas ciano/azul por lado, mais uma camada amarela acima, varridas para trás e para baixo.
- **Correção:**
  - Clarear o topo e a testa para ciano.
  - Adicionar de cada lado 3 penas afiladas, apontando para trás a ~30° abaixo da horizontal: 2 azul/ciano e 1 amarela. Elas devem passar 3–4 px além do contorno da cabeça.

**6. Asas sob o manto com poucas penas: frente e 3/4**
- **Modelo:** cada lado tem só 2 pranchas longas penduradas na vertical, uma creme e uma amarela. Na foto de frente, parecem duas réguas. A especificação proíbe "penas com poucos blocos".
- **Arte:** um leque em camadas que se abre para fora até a altura do joelho:
  - em cima, coberteiras azuis;
  - no meio, azul-claro;
  - embaixo, penas longas amarelas e creme.
  Na 3/4 é um dos volumes mais fortes depois do manto.
- **Correção:** 5–7 penas por lado, em 3 fileiras (azul → azul-claro → amarelo/creme), todas pontudas. Abrir ~15–25° para fora do corpo, com a ponta mais longa na altura do joelho.

**7. Peito: placa lisa, escuro demais e com losangos amarelos: frente**
- **Modelo:**
  - o peito é uma placa retangular lisa, azul-claro, com a cruz;
  - logo abaixo vem uma faixa azul-escura com escamas;
  - o conjunto fica mais escuro que a arte;
  - na base da barriga há 2 losangos amarelos que não existem na ficha.
- **Arte:**
  - o peito é um escudo de penas azul-claro quase branco (~#b8e6f7), com a borda de baixo serrilhada em pontas;
  - abaixo, penas em camadas azul-claro e azul, com toques creme;
  - a cruz azul-escura fica no centro do escudo.
- **Correção:**
  - Recortar a borda de baixo da placa em 3–4 pontas e desenhar na textura as escamas de pena (contorno 1 px mais escuro).
  - Clarear o peito de baixo, deixando o azul-escuro só nas laterais.
  - Remover os 2 losangos amarelos ou trocá-los por pontas creme das asas.

**8. Padrão dourado do manto errado: barra, todas as vistas**
- **Modelo:** friso contínuo de grega (meandro "ㄹ") em toda a barra, na frente e atrás. No jogo, lê como borda grega genérica.
- **Arte e detalhe "Detalhe do Manto":** só nas PONTAS do manto, formas douradas grandes em degraus e L, tipo xadrez diagonal. Cada forma tem ~1/5 da largura do painel. O resto da barra é só a faixa dourada lisa.
- **Correção:**
  - Apagar o meandro.
  - Em cada ponta (2 na frente, 1–2 atrás), desenhar 2–3 blocos dourados em degrau, alinhados na diagonal da ponta, com 4–6 px de lado.
  - Manter a faixa dourada lisa na barra.

**9. Emblema da fênix nas costas: traseira**
- **Modelo:** emblema pequeno, deslocado para a esquerda e parcialmente coberto pelas penas da cauda. Só aparece uma asa. Na foto do jogo de 3/4 traseira, não se vê fênix.
- **Arte (traseira e detalhe "Emblema"):** fênix dourada grande, centrada no alto das costas, logo abaixo do capuz. As asas abertas para cima ocupam ~40% da largura das costas, com a cauda da fênix descendo em ponta.
- **Correção:** centralizar no eixo das costas, com ~40% da largura do manto nessa altura. Desenhar cabeça, 2 asas simétricas para cima e uma cauda em 3 pontas. Tirar a cauda do caminho (ver item 4).

**10. Bico de frente vira "viseira" e tem cor oliva: rosto, frente**
- **Modelo:** de frente, uma placa dourada larga entre os olhos com um bloquinho na frente parece máscara ou elmo. A cor é mostarda/oliva (~#a88d2f).
- **Arte:** bico longo e reto em cunha, amarelo-alaranjado vivo (~#f9ba2d / #fbca3c). A base ocupa ~1/3 da largura da cabeça e não há placa na testa.
- **Correção:**
  - Estreitar a base do bico para ~1/3 da cabeça e remover a placa superior larga.
  - De frente, o bico deve afinar até a ponta.
  - Recolorir para amarelo vivo com a sombra em laranja-dourado, não oliva.

## OUTROS PROBLEMAS MENORES
- **Olho e sobrancelha:** no jogo o olho fica cinza e pequeno. A esclera deve ser branca (não cinza) e a íris azul viva deve ocupar ~metade do olho, com 1 brilho branco. A sobrancelha é uma barra plana azul-petróleo clara; deve ser azul-marinho (~#0c2c85), com 2 px, inclinada para baixo em direção ao bico (olhar determinado).
- **Ombros do manto:** na foto de frente, o roxo dos ombros tem calombos e espetos serrilhados. Na arte é uma gola em camadas lisas, com borda dourada.
- **Borda dourada:** falta borda dourada contínua nas bordas verticais da abertura frontal (do medalhão ao chão). Na arte é a linha dourada mais visível na 3/4.
- **Capuz e gola:** falta a gola roxa alta atrás do pescoço que aparece na traseira e na 3/4 da arte. Por isso o pescoço parece um poste de tábuas azuis.
- **Forro:** o forro do manto deveria ser um roxo mais escuro que o lado de fora. Hoje é o mesmo tom.
- **Medalhões:** estão quadrados, com o centro chapado. Na arte são redondos/octogonais, com centro saliente.
- **Dourado do manto:** a barra está alaranjada (~#b78a1f a #e8a520). Na arte é amarelo-ouro mais claro.
- **Espeto amarelo no ombro esquerdo:** na foto de frente há um espeto amarelo solto atrás do ombro esquerdo, assimétrico (provavelmente pena da cauda vazando). Esconder.
- **Cruz:** a cruz do peito tem pontas retas. Na arte as pontas são levemente alargadas (cruz pátea).
- **Pernas:** pernas e dedos estão em amarelo mostarda. Na arte são amarelo-limão com escamas segmentadas mais claras.

## O QUE JÁ ESTÁ FIEL
- A paleta geral é roxo, azul e dourado, e a cruz do peito é legível de longe.
- Os 2 medalhões dourados do fecho estão no lugar certo.
- As 3 caudas estão separadas, com contas douradas de centro ciano bem legíveis.
- As 3 gemas em losango com fio dourado nas costas batem com a traseira.
- As pernas são longas e retas, com patas grandes e garras escuras.

## NOTA DE FIDELIDADE AOS DETALHES
**5/10.** Ao lado do Esporocó aprovado, o que mais pesa no jogo é o manto em cone, que esconde o corpo nas vistas 3/4, junto com a crista em forma de coroa e a barbela comprida. 4 dos 10 problemas principais são de rosto (itens 2, 3, 5 e 10), mais o olho/sobrancelha nos menores.

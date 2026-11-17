# Auditoria de detalhes: Esporocó (fêmea), rodada n38

Fontes usadas: `003_esporoco_ficha/arte/vistas/detalhes/expressoes(neutra)`. Não existe `_especificacao.md`. Modelo: `n38_comp/vistas/3-4/rosto`. Também olhei a foto do jogo.
Métrica do comp: IoU médio 77,6 %, cor/detalhe 54,0 %.

## TOP 10 PROBLEMAS

**1. Cauda de cipós: a estrutura está errada (laterais, traseira e 3/4)**
- **Modelo:** um anel único e fechado de cipó, ligado ao corpo por uma haste reta e horizontal que sai do quadril, na altura da coxa. O conjunto parece um pirulito. Na traseira a espiral aparece inteira, de frente, e cobre as costas como um caracol.
- **Ficha:** o cipó nasce no alto da garupa, no meio das costas, e sobe já curvo, sem trecho reto. Forma um laço grande aberto em "C" e, dentro e abaixo dele, um segundo laço menor. As pontas terminam enroladas. Na traseira veem-se **dois arcos verticais paralelos**, vistos de perfil, um de cada lado, com um vão escuro entre eles de ~1/4 da largura do corpo. Na comp, essa é a mancha azul no centro da traseira.
- **Correção:**
  - Apagar a haste horizontal e fazer o cipó sair da garupa na altura do meio das costas, subindo em arco contínuo.
  - Fazer dois laços, um à esquerda e um à direita, no plano lateral (paralelos ao corpo), afastados ~1/4 da largura do corpo. De trás, cada um deve aparecer como uma faixa vertical.
  - O laço externo fica aberto embaixo (forma de C, sem fechar o anel), com o topo na altura do olho. O laço interno é menor, com ~60 % do diâmetro, e fica abaixo e atrás.
  - Na lateral, a borda traseira do laço deve ficar ~1 cubo mais perto do corpo do que está hoje: na comp, o azul aparece na borda externa e o vermelho dentro do laço.

**2. Babador creme do peito: largura, forma e volume (frente, lateral, 3/4)**
- **Modelo:**
  - Uma placa creme larga e retangular, da largura da cabeça inteira. Começa logo abaixo do bico e acaba na metade superior do peito, com uma pontinha.
  - A textura tem escamas triangulares tostadas.
  - Na lateral é uma prancha chapada que sai para a frente do peito e se destaca da silhueta.
- **Ficha:**
  - Um "V" creme estreito e comprido. No topo, sob a barbela, tem ~1/2 da largura da cabeça. Afina até uma ponta no meio da barriga, na altura da base das flores dos ombros ou um pouco abaixo.
  - É formado por penas creme pontudas sobrepostas e lisas, sem escamas escuras.
  - Na lateral é só uma faixa estreita que acompanha a curva do peito.
- **Correção:**
  - Reduzir a largura do topo para ~1/2 da cabeça e afinar em V até uma ponta 1,5–2 cubos abaixo do fim atual.
  - Trocar as escamas escuras por 3–4 fileiras de penas creme pontudas, com a cor base `#EFD4A9` e uma sombra leve de `#D9B98A` só na borda inferior de cada pena.
  - Na lateral, encostar a peça no peito para que ela não ultrapasse a silhueta do peito em mais de 1 px de textura.

**3. Crista foliar: cubos em tufo em vez de lâminas varridas para trás (lateral, 3/4, rosto)**
- **Modelo:** um amontoado arredondado de blocos vermelhos grossos de faces retas, empilhados em cima da cabeça. Parece couve-flor ou rosa. A crista fica alta e não desce atrás da nuca. Na comp lateral há azul na frente e no topo (sobra) e vermelho atrás (falta).
- **Ficha:**
  - Lâminas vermelhas finas, alongadas e com ponta, como folhas. Saem da testa e varrem **para trás**, em camadas.
  - As lâminas de trás caem pela nuca até a altura do olho, como um topete penteado para trás.
  - Na lateral a crista é mais longa do que alta (~1,7 : 1) e quase não passa da frente da testa.
- **Correção:**
  - Substituir os cubos por 5–7 lâminas finas (espessura ≤ 1/3 da largura) com a ponta afinando em degraus de textura.
  - Inclinar as lâminas 30–60° para trás. Descer 2–3 lâminas atrás da cabeça até a linha do olho.
  - Recuar a frente da crista para que ela comece na testa, sem avançar sobre o olho.
  - Manter os três lobos da vista frontal, que já estão bons.

**4. Bico: forma e cor (frente, lateral, rosto)**
- **Modelo:**
  - De frente, um quadrado amarelo-ouro (~`#FFC84E`) em cima e um bloco marrom-escuro (~`#8B5B21`) embaixo, como um balde.
  - De lado, dois cubos em degrau: um cubo grande e outro menor projetado à frente e abaixo.
- **Ficha (neutra e arte):**
  - Uma cunha laranja (`#F9AA0E`/`#F59C2C`), larga na base e afinando para uma ponta levemente curvada para baixo. A mandíbula inferior é menor e de um laranja um pouco mais escuro, nunca marrom.
  - Narina: um ponto escuro pequeno perto da base.
  - De lado, o bico se projeta ~1/3 da profundidade da cabeça.
  - De frente é um "V" que afina para baixo, com ~1/4 da largura da cabeça.
- **Correção:**
  - Mandíbula superior: 3 degraus que afinam (base cheia, meio com 2/3, ponta com 1/3), a ponta 1 px abaixo da linha da boca. Cor `#F9AA0E` com o topo em `#FFC24A`.
  - Mandíbula inferior: ~1/2 da altura da superior, em `#E08A10`.
  - Eliminar o marrom.
  - De frente, desenhar o V afinando para baixo.

**5. Plumagem vegetal do corpo e das asas: forma das folhas e desenho do peito (frente, lateral, 3/4)**
- **Modelo:**
  - As folhas são placas retangulares grossas, a maioria com ponta quadrada, espetadas em vários ângulos.
  - Na frente, duas placas verde-claras grandes cruzam o peito na diagonal, do ombro para o centro, como braços cruzados.
  - Há uma costura horizontal escura atravessando a barriga e, abaixo dela, uma "saia" de folhas quadradas em fila.
- **Ficha ("Plumagem vegetal"):**
  - Folhas finas em forma de lança, com ponta, sobrepostas como telhas e apontando para baixo e para trás. São verde-claras (`#85C446`) em cima e na frente, médias (`#538822`) no meio e escuras (`#24511B`) embaixo.
  - Na frente, as asas descem **verticais** pelas laterais, do ombro à coxa. No centro há chevrons em V de folhas verde-claras convergindo sob o babador.
  - Não há costura horizontal.
- **Correção:**
  - Afinar as folhas para no máximo 1/3 da espessura atual e dar ponta a todas (losango alongado na textura).
  - Girar as duas placas diagonais do peito para que fiquem verticais nas laterais, apontando para baixo e para fora.
  - Remover a costura horizontal da barriga.
  - Trocar a fila de folhas quadradas da base por 2 camadas de folhas pontudas em V centradas no eixo.

**6. Olhos: cor da esclera e da íris, pupila e delineado (rosto, frente e lateral)**
- **Modelo:**
  - Esclera cinza-acastanhada (~`#A1958D`).
  - Íris carmesim escuro (~`#8E2547`).
  - Pupila preta pequena e **redonda**.
  - Delineado superior fino, de 1 px.
- **Ficha (neutra):**
  - Esclera branco-quente (~`#F0D7C2`), com uma sombra lilás só na faixa de cima.
  - Íris magenta vivo (~`#B72C73`), com anel mais escuro e miolo mais claro.
  - Pupila preta em **oval vertical**, com um brilho branco no canto superior externo.
  - Delineado preto grosso de 2–3 px, que se estende para fora em "asa", com 2–3 cílios grossos na ponta externa.
- **Correção:**
  - Esclera `#F0E2D4` com a linha de cima `#C9B3C9`.
  - Íris `#C8307E`, borda `#8A1A55`.
  - Pupila oval de 2×3 px.
  - Engrossar o delineado superior para 2 px e prolongá-lo 2 px para fora e para cima, com cílios.

**7. Flores tóxicas: cor, miolo e orientação (frente, lateral, cauda)**
- **Modelo:**
  - Pétalas em rosa-malva apagado (~`#BF3F74`/`#C22D61`).
  - Miolo quadrado cáqui ou bege pálido (~`#BEBA94`, com borda dourada fosca), sem estames.
  - A flor do ombro é um plano voltado só para a frente, então na lateral vira uma fatia rosa fina.
- **Ficha ("Flor tóxica"):**
  - 5 pétalas pontudas em rosa-choque (`#F03183`), com o centro de cada pétala mais claro (`#F56294`).
  - Miolo redondo amarelo brilhante (~`#FFE45A`, com o centro quase branco) e 5–7 estames amarelos em pontinhos ao redor.
  - Na arte, a flor da asa olha para fora, em diagonal, e é bem visível de lado.
- **Correção:**
  - Recolorir as pétalas para `#F03183`/`#F56294`.
  - Miolo octogonal ou redondo de 2×2 a 3×3 px em `#FFE45A`, com 1 px `#FFF6B0` no centro.
  - Adicionar pontos `#FFD23A` como estames nas pétalas, junto ao miolo.
  - Girar as flores dos ombros ~45° para fora, para que apareçam na frente e na lateral. Pôr uma flor grande no meio da asa, como na arte.

**8. Espinhos e cor do cipó (cauda, todas as vistas)**
- **Modelo:**
  - Espinhos em pirâmides de degraus cáqui/bege (~`#81715A`, com ponta marrom).
  - Cipó verde-oliva escuro (~`#354F1A`), com traços pretos fortes marcando os segmentos.
- **Ficha ("Cauda de cipós" e traseira):**
  - Espinhos em cones lisos creme-claro (`#EFD4A9`/`#F2E2B8`). Alguns têm a ponta rosada (`#F0A0A0`), principalmente na traseira, e alguns são esverdeados.
  - Cipó verde médio (`#3E8A30`, com a face de cima `#5AA83A`), com juntas suaves pouco marcadas.
- **Correção:**
  - Espinhos: base `#EFD4A9`, ponta `#F5B0B0` em ~1/3 deles, sem marrom.
  - Cipó: base `#3E8A30`, topo `#5AA83A`, sombra `#24511B`.
  - Juntas em 1 px `#2E6A24`, sem preto.

**9. Barbela (frente, lateral, rosto)**
- **Modelo:** 3 tiras vermelhas finas e escuras (~`#831818`), penduradas na frente da placa creme. De lado, ficam soltas na frente do peito.
- **Ficha:**
  - Dois lóbulos vermelhos grossos (`#BE2232`, sombra `#8E1A28`) presos logo **sob o bico**, cada um com ~1/2 da largura do bico.
  - Descem ~2× a altura do bico e ficam colados ao início do babador creme.
- **Correção:**
  - Trocar as 3 tiras por 2 blocos lado a lado, cada um com metade da largura do bico, em `#BE2232`.
  - Altura = 2× a altura do bico.
  - Encostar no queixo, sem projetar à frente do babador.

**10. Pernas e pés (todas as vistas)**
- **Modelo:**
  - Canela laranja-queimado (~`#B66F18`) com listras horizontais marrons fortes.
  - De frente, os tufos creme ficam direto sobre o laranja, sem trecho verde.
  - Pés como chapas finas e largas, com dedos achatados e espalhados.
- **Ficha ("Patas"):**
  - Logo abaixo da plumagem há um trecho **verde-escuro** da coxa, ~1/3 da perna visível, também na frente.
  - Abaixo dele, canela laranja-amarela lisa (`#F9AA0E`, topo `#FFC24A`), só com emendas de bloco suaves.
  - Pés de blocos robustos: 3 dedos para a frente e 1 para trás. Cada dedo é um cubo com altura ~1/2 da largura da canela.
- **Correção:**
  - Mostrar ~1/3 superior da perna em `#24511B` também na vista frontal.
  - Recolorir a canela para `#F9AA0E` e trocar as listras por 1–2 emendas sutis em `#E0920C`.
  - Dobrar a altura dos dedos e encurtar o espalhamento lateral. A largura total do pé deve ser ≤ 1,6× a largura da canela; hoje há azul nos pés na comp frontal.

## OUTROS PROBLEMAS MENORES
- Há uma placa verde-escura fina saindo na horizontal atrás da nuca e das costas, visível no `_rosto` lateral e na lateral direita. Parece um artefato: remover.
- Tufos da coxa em bege-acinzentado/cáqui, e um deles é um bastão solto pendurado atrás da perna. Na ficha são penas creme `#EFD4A9`, pontudas e coladas à base da plumagem.
- O creme da bochecha sob o olho está escuro e oliva (~`#A0884F` no rosto). Na ficha é `#F6CD80`/`#EFD4A9`, claro.
- Sobrancelhas em dois blocos separados. Na ficha é uma viseira verde-clara contínua que forma um V com a ponta vermelha da crista entre os olhos.
- Na frente faltam as "costeletas" verde-claras sob o olho, que na ficha se abrem para fora na altura do bico e alargam a base do rosto.
- Faltam os botões florais fechados, cor de pêssego (`#F0A890`), nas pontas e laterais dos cipós, visíveis na traseira da ficha.
- Cauda com 3–4 flores na lateral. A ficha mostra 5–6 flores, distribuídas também no laço interno.
- A silhueta frontal está larga demais na base da saia e do quadril (azul nas laterais inferiores da comp). Afinar ~1 cubo de cada lado.
- Folhas do pescoço (hackles) em placas quadradas. Na ficha são lâminas pontudas que descem para trás sobre o ombro.

## O QUE JÁ ESTÁ FIEL
- Paleta geral: verde, vermelho, rosa e laranja na proporção certa. O vermelho da crista (~`#B91B1C`) bate com `#BE2232`.
- Crista de frente e de trás: três lobos, com o central mais alto e uma ponta vermelha em V descendo entre os olhos.
- Expressão neutra: olhar meio-cerrado, sobrancelha inclinada e cílios na ponta externa. Lê-se como fêmea séria, como na ficha.
- Flores dos ombros na altura e posição certas na vista frontal. Há creme sob o olho ao lado do bico, como na neutra.
- A cauda tem espiral com espinhos na borda externa, e o topo fica na altura certa (nível do olho).

## NOTA DE FIDELIDADE AOS DETALHES
**4,5 / 10.** Dos 10 problemas principais, 4 são de rosto ou cabeça: crista (3), bico (4), olhos (6) e barbela (9).

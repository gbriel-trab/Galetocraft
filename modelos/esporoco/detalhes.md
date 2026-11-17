# Esporocó (#003): detalhes da ficha

Lista tirada de `_ficha`, `_arte`, `_vistas`, `_detalhes` (5 quadros) e da expressão neutra de `_expressoes`.
As cores RGB foram amostradas com PIL nos PNGs da ficha (mediana de uma janela pequena). A coluna de status mostra a rodada inicial da fase 2 (n19) e a final (n38).

Legenda de status: **ok** = igual à ficha; **parcial** = presente, mas com diferença (motivo ao lado); **falta**.

## Paleta (quadro "Paleta de Cores" da `_ficha`)
| # | Detalhe | Cor da ficha | Status |
|---|---|---|---|
| 1 | Verde-escuro (sombra das folhas, coxa) | (36, 81, 27) | n19: parcial (verde azulado) → **n38: ok** |
| 2 | Verde (base das folhas, cara) | (83, 136, 34) | n19: parcial → **n38: ok** |
| 3 | Verde-claro/lima (folhas de cima, sobrancelha) | (133, 196, 70) | n19: parcial → **n38: ok** |
| 4 | Creme (peitilho, bochecha, coxas) | (239, 212, 169) | n19: parcial (pálido demais) → **n38: ok** |
| 5 | Vermelho (crista, barbela) | (190, 34, 50) | n19: parcial (vermelho rosado) → **n38: ok** |
| 6 | Rosa (pétala clara) | (245, 98, 148) | n19: parcial → **n38: ok** |
| 7 | Magenta (pétala, íris) | (240, 49, 131) | n19: parcial → **n38: ok** |
| 8 | Amarelo-laranja (bico, pés) | (249, 170, 14) | n19: parcial (pés amarelos demais) → **n38: ok** |
| 9 | Marrom (narina, sombra do bico) | (134, 83, 16) | n19: ok → **n38: ok** |

## Cabeça e rosto (`_expressoes` neutra, vistas de frente e de lado)
| # | Detalhe | Onde / forma / tamanho | Cor da ficha | Status |
|---|---|---|---|---|
| 10 | Cara verde | bloco grande; ~8 de altura, ~11 de largura | (88, 135, 13) | n19: parcial (verde azulado) → **n38: ok** |
| 11 | Faceta do olho | plano diagonal entre a frente e o lado | verde da cara | n19: ok → **n38: ok** |
| 12 | Olho: formato | amendoado, mais largo que alto, canto da frente pontudo e mais baixo | — | n19: ok → **n38: ok** |
| 13 | Olho: esclera | metade de baixo branca-quente | (243, 222, 209) | n19: parcial (branca fria) → **n38: ok** |
| 14 | Olho: sombra sob a pálpebra | faixa lilás no alto do olho | (161, 129, 137) | n19: parcial (lilás claro demais) → **n38: ok** |
| 15 | Olho: íris | grande, alta, magenta-avermelhada, olhando para a frente | (240, 49, 131) a (190, 30, 80) | n19: ok → **n38: ok** |
| 16 | Olho: pupila | elipse vertical escura | (10, 9, 14) | n19: ok → **n38: ok** |
| 17 | Olho: brilho | ponto branco no alto da íris | branco | n19: ok → **n38: ok** |
| 18 | Pálpebra (delineado) | fio preto grosso descendo para o bico | preto | n19: ok → **n38: ok** |
| 19 | Cílios de fêmea | 2-3 riscos no canto de trás, para cima e para trás | preto | n19: ok → **n38: ok** |
| 20 | Sobrancelha | bloco verde-claro grosso logo acima do olho, descendo para o bico (V bravo de frente) | (135, 192, 46) | n19: parcial (verde azulado) → **n38: ok** |
| 21 | Bochecha creme | bloco creme sob a metade da frente do olho, encostado no bico | (245, 208, 129) | n19: parcial (pálida) → **n38: ok** |
| 22 | Bochecha verde de trás | bloco verde-claro sob o olho, para trás | (126, 176, 49) | n19: ok → **n38: ok** |
| 23 | Bico de frente | cunha pequena: ~3 de largura em cima, mais estreito embaixo | (248, 174, 14) | n19: parcial (caixa larga no jogo) → **n38: ok** |
| 24 | Bico de lado | cunha com topo claro, frente bronzeada, ponta curva para baixo | topo (251, 157, 41), frente (205, 130, 76) | n19: parcial → **n38: ok** |
| 25 | Narina | ponto marrom no lado do bico | (134, 83, 16) | n19: ok → **n38: ok** |
| 26 | Mandíbula | pequena, laranja-escura | (200, 110, 16) | n19: ok → **n38: ok** |
| 27 | Barbela | 3 tiras vermelhas sob o bico, a do meio mais comprida | (191, 38, 65) | n19: ok → **n38: ok** |
| 28 | Garganta creme | frente do pescoço creme, do bico ao peito | (248, 202, 119) | n19: parcial (pálida) → **n38: ok** |
| 29 | Penas da nuca | blocos verdes em camadas atrás do olho, para trás | (126, 176, 49) / (88, 135, 13) | n19: ok → **n38: ok** |

## Crista foliar (`_detalhes` "Crista foliar", vistas)
| # | Detalhe | Onde / forma / tamanho | Cor da ficha | Status |
|---|---|---|---|---|
| 30 | Ponta em V na testa | bloco vermelho entre as sobrancelhas | (209, 23, 35) | n19: ok → **n38: ok** |
| 31 | Lâmina do meio | a mais alta (topo ~39), ~3 de largura, ponta afiada de frente | (231, 48, 46) topo | n19: parcial (topo reto de frente) → **n38: ok** |
| 32 | Lâminas dos lados | 1 de cada lado, mais baixas (topo ~36,5), coladas à do meio, pontudas | (190, 19, 22) | n19: parcial (leque aberto com vão no jogo) → **n38: ok** |
| 33 | Massa de trás | blocos sobrepostos que varrem para trás até z ≈ +3 | (227, 31, 59) | n19: ok → **n38: ok** |
| 34 | Blocos sobrepostos | degraus visíveis, topo claro e junta escura | — | n19: ok → **n38: ok** |

## Corpo e plumagem (`_detalhes` "Plumagem vegetal", vistas, arte)
| # | Detalhe | Onde / forma / tamanho | Cor da ficha | Status |
|---|---|---|---|---|
| 35 | Peitilho em V | creme, da garganta (largura ~7) até a ponta no meio do peito (y ~15) | (246, 211, 161) | n19: parcial (peças soltas) → **n38: ok** |
| 36 | Penas do peitilho | pontas em degrau na beirada do V | (251, 225, 196) / (222, 178, 112) | n19: parcial → **n38: ok** |
| 37 | Folhas-pena grossas | blocos de ponta afiada, em camadas | — | n19: ok → **n38: ok** |
| 38 | Folha: 2 tons | metade clara, metade escura (dobra) | claro (154, 198, 67), escuro (57, 100, 29) | n19: parcial (contraste baixo) → **n38: ok** |
| 39 | Folhas de cima (ombro) | lima/verde-claras, grandes, varridas para trás | (155, 195, 61) | n19: parcial → **n38: ok** |
| 40 | Folhas de baixo e de trás | verde-escuras | (52, 84, 3) | n19: parcial → **n38: ok** |
| 41 | Sombra entre folhas | quase preta | (17, 32, 12) | n19: falta (núcleo claro aparece) → **n38: parcial: o vão escuro aparece dos lados e atrás; na frente o núcleo é pintado de verde para não abrir um buraco preto entre as folhas** |
| 42 | Barriga | folhas verde-claras sob o peitilho | (133, 196, 70) | n19: ok → **n38: ok** |

## Flores (`_detalhes` "Flor tóxica")
| # | Detalhe | Onde / forma / tamanho | Cor da ficha | Status |
|---|---|---|---|---|
| 43 | Flor do ombro | 1 de cada lado, R ~3,5, de frente para fora | — | n19: ok → **n38: ok** |
| 44 | Pétalas | 5, pontudas, metade clara e metade viva | (249, 68, 125) / (223, 60, 113) | n19: parcial (rosa apagado) → **n38: ok** |
| 45 | Base das pétalas | magenta mais escuro perto do miolo | (240, 49, 131) | n19: ok → **n38: ok** |
| 46 | Miolo | redondo, amarelo-claro, brilha | (255, 239, 125) / (253, 248, 204) | n19: parcial (quadrado) → **n38: parcial: o miolo é um bloco (quadrado de frente) com degradê radial claro→amarelo; um círculo exigiria recorte** |
| 47 | Estames | pontinhos amarelos em volta do miolo | (249, 170, 14) | n19: parcial → **n38: ok** |

## Cauda de cipó (`_detalhes` "Cauda de cipós", vistas)
| # | Detalhe | Onde / forma / tamanho | Cor da ficha | Status |
|---|---|---|---|---|
| 48 | UM cipó grosso em espiral | sai do traseiro, volta grande + miolo enrolado | — | n19: ok → **n38: ok** |
| 49 | Blocos do cipó | segmentos com juntas visíveis, topo mais claro | (83, 128, 43), topo (140, 168, 92), sombra (28, 60, 23) | n19: parcial (anel tubular liso) → **n38: ok** |
| 50 | De costas, dois arcos | "( )" | — | n19: parcial (lê como anel oval) → **n38: parcial: o plano da espiral está girado 44°, mas de costas a volta ainda lê mais como um oval do que como dois arcos separados (com a forma de lado fixa, uma espiral plana não fica mais estreita)** |
| 51 | Espinhos | cones creme no lado de fora (topo da volta), ~6-8 | (238, 207, 148), ponta rosada (247, 150, 149) | n19: parcial (pagode quadrado) → **n38: ok** |
| 52 | Flores do cipó | ~5 por lado: 2 na volta de fora (alto e baixo), 2 no miolo, 1 embaixo | como 44-46 | n19: parcial (posições) → **n38: parcial: 5 flores no cipó mais 1 no miolo, perto das posições da vista de lado; as vistas da ficha não batem entre si nas flores do cipó** |

## Pernas (`_detalhes` "Patas")
| # | Detalhe | Onde / forma / tamanho | Cor da ficha | Status |
|---|---|---|---|---|
| 53 | Penas creme das coxas | sob o corpo, na frente das coxas | (246, 211, 161) | n19: ok → **n38: ok** |
| 54 | Coxa verde-escura | faixa curta acima da canela | (38, 63, 14) | n19: ok → **n38: ok** |
| 55 | Canela | blocos laranja em degraus | (209, 123, 14) / (205, 127, 59) | n19: parcial (amarela demais) → **n38: ok** |
| 56 | Dedos | 3 para a frente + 1 atrás, blocos grossos | (232, 148, 8) | n19: ok → **n38: ok** |

## Resumo (n38)
- 52 ok, 4 parcial (41, 46, 50, 52; o motivo está na linha de cada um), 0 falta.
- Cores do modelo (n38), amostradas da ficha: verdes (46, 86, 12) / (88, 136, 18) / (132, 188, 50) / (156, 200, 62);
  creme (248, 204, 122); vermelho (220, 26, 30) / (240, 44, 40); rosa (240, 56, 120) / (252, 108, 156);
  bico (246, 166, 20) com frente (205, 130, 76); cipó (100, 150, 50) com juntas (34, 64, 18); espinho (242, 214, 156) → ponta (247, 150, 149).

## Auditoria da n38 (`auditoria_n38.md`): status na n43
Status final (n43): 13 ok, 5 parcial.

| Item da auditoria | O que foi feito | Status |
|---|---|---|
| 1. Cauda | Saiu a haste reta. São 2 cipós, um de cada lado (x = ±4,2), em planos laterais. Cada um nasce na garupa e sobe já curvo. O externo é grande e abre em C embaixo; o interno é menor (~65%) e fica abaixo. Os dois terminam enrolados. De costas viram 2 faixas verticais com um vão entre elas. | ok |
| 1b. Cipó: cor e juntas | (70, 134, 46), face de fora (96, 164, 58) e sombra (40, 84, 28). Juntas suaves (50, 104, 36), sem preto. | ok |
| 2. Babador | V estreito e comprido: 5,4 de largura no topo (~1/2 da cabeça), ponta em y 13,4. Penas creme lisas (242, 214, 170) com sombra (217, 185, 138) só na beirada. Fica rente ao peito, sob a barbela. | ok |
| 3. Crista | 7 lâminas finas (1,35 de espessura) varridas de 10° a 116° para trás; as 2 de trás descem pela nuca até a linha do olho. Lobos laterais largos de frente e finos de perfil; a frente não passa da testa. | ok |
| 4. Bico | Cunha em V com 3 degraus (2,9 → 2,0 → 1,0), laranja (249, 170, 14), topo (255, 194, 74). Mandíbula de baixo (224, 138, 16) com ~metade da altura. Narina no lado; sem marrom. | ok |
| 5. Folhas | Folhas em lança, mais estreitas (W 2,8 a 3,4), com ponta em losango da largura toda. As da frente do peito descem verticais nas laterais. A barriga tem 2 camadas de chevrons pontudos em V e não tem mais a costura. | parcial: a espessura ficou 0,8 (não 1/3), para continuarem blocos com volume, como pede o REFAZER |
| 6. Olhos | Esclera (240, 226, 212), linha lilás (201, 179, 201), íris magenta viva (200, 48, 126) com anel (138, 26, 85) e miolo claro, pupila em oval vertical, delineado grosso em asa e 3 cílios. | ok |
| 7. Flores | Pétalas rosa-choque (240, 49, 131) com a faixa do meio (245, 98, 148), estames (255, 210, 58), miolo octogonal (255, 228, 90) com centro (255, 246, 176). Flores dos ombros giradas 45° para fora. | parcial: não pus a flor extra no meio da asa (ver nota abaixo) |
| 8. Espinhos | Cones lisos creme (239, 212, 169) → (246, 230, 190), 1/3 com a ponta rosada (245, 176, 176), sem marrom. | ok |
| 9. Barbela | 2 lóbulos grossos lado a lado, cada um com ~metade da largura do bico, (196, 36, 52) → (142, 26, 40), colados sob o bico, no topo do babador. | ok |
| 10. Pernas | Coxa verde-escura (36, 81, 27) no 1/3 de cima (também de frente). Canela laranja lisa (249, 170, 14) com 1 emenda suave. Dedos de 2,0 de altura, menos abertos; pé com ~1,5× a canela. | ok |
| Placa escura atrás da nuca | Topo do núcleo pintado de verde e mais baixo. | ok |
| Tufos das coxas | Penas creme pontudas coladas à base da plumagem. O bastão solto de trás da perna saiu. | ok |
| Creme da bochecha | Mais claro: (252, 228, 176), e (250, 222, 166) de perfil. | ok |
| Sobrancelhas | Viseira contínua: as 2 sobrancelhas se ligam em V sob a ponta vermelha. | ok |
| Costeletas | Folha verde-clara sob cada olho, abrindo para fora na altura do bico. | ok |
| Botões florais | Botões cor de pêssego (248, 176, 150) na ponta e nos lados dos cipós. | parcial: na prévia ficam um pouco escuros |
| Flores da cauda | 8 no total: 4 no laço externo, 2 no interno e 2 dentro do laço. | ok |
| Saia larga | O anel de baixo ficou 1 cubo mais estreito. | parcial: a frente melhorou um pouco no IoU (87%), mas ainda sobra nas laterais de baixo |
| Penas do pescoço (hackles) | Lâminas mais finas (2,8), varridas para trás sobre o ombro. | parcial: continuam blocos, mais finos |

**Onde a auditoria contradiz a ficha:**
- **Flor extra na asa:** nas vistas laterais da ficha não há flor no meio da asa; a flor que aparece na arte (em 3/4) é a mesma do ombro. Por isso só girei a flor do ombro.
- **Crista:** a auditoria pede que a crista quase não passe da testa. Na vista lateral da ficha ela passa ~1 cubo à frente da cara. Deixei a frente na testa (até z ≈ −11).
- **Laços da cauda:** a fase 1 tinha fixado UM cipó, que era o pedido original. A ficha mostra dois arcos na traseira e o quadro se chama "Cauda de cipós"; com isso e a ordem do coordenador, fiz dois.

## Fase 7: olhar imponente (n44 a n46; só olho e sobrancelha)
- **Olho:** virou fenda alongada (4,3 × 2,6, cerca de 1,7 : 1). A pálpebra pesada corta o topo numa diagonal que
  desce até o bico: aparecem ~60% da altura. A borda de baixo é quase reta e sobe um pouco para trás. O canto da
  frente afina em ponta.
- **Íris e pupila:** a íris é magenta forte (236, 84, 156) → (196, 36, 118), com anel (128, 22, 78), e enche quase
  todo o olho. O topo fica 1 tom mais escuro, como sombra da pálpebra. A pupila é oval e fica do lado do bico, com 1
  ponto de brilho. A esclera aparece só numa cunha atrás.
- **Fêmea:** o delineado em asa e os 3 cílios continuam, presos à linha da pálpebra.
- **Sobrancelha:** é um bloco verde-claro saliente logo sobre a pálpebra, a 18° descendo para o bico. As pontes da
  viseira desceram junto.
- Os itens 12 a 20 (olho e sobrancelha) da lista acima continuam ok, com o desenho novo.

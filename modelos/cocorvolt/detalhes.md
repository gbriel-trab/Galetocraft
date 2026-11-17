# Cocórvolt (#006): detalhes da ficha

RGB amostrado na ficha (`_vistas` agrupada por k-means, `_arte`, paleta da `_ficha`). Status: ok, parcial ou falta.
O status vale para a rodada indicada no fim.

## Paleta da ficha (`_ficha`, "Paleta de Cores")
cinza claro (217,213,210); cinza (143,138,138); cinza escuro (64,64,64); carvão (38,40,44); marinho (40,69,132);
azul (45,90,182); amarelo raio (253,226,84); palha/ouro (231,174,87); vermelho (205,35,29).
Nas vistas renderizadas os tons dominantes são: carvão (44,42,46), (64,62,68), cinza (96,87,85), (122,110,109),
(148,136,135), claro (177,164,160), marinho (45,73,130), amarelo-laranja das pernas e do bico (233,158,16),
ouro (238,198,95), palha (205,160,95), brilho (247,237,188).

## Rosto (`_expressoes` neutra, `_detalhes` "Olhos Eletrificados")
| # | detalhe | onde / forma / tamanho | cor | status |
|---|---|---|---|---|
| 1 | olho | retângulo deitado ~2,4 × 1,1, na quina do rosto, logo abaixo da aba | miolo (250,253,255), azul (70,168,255), borda (30,110,246) | ok |
| 2 | corte bravo do olho | borda de cima desce para o bico | — | ok |
| 3 | brilho do olho | olho inteiro brilha (glowmask) | — | ok |
| 4 | sobrancelha | bloco escuro grosso logo acima do olho, desce para o bico | (40,42,48) | ok |
| 5 | testa | faixa escura entre olho e aba | (64,64,64) | ok |
| 6 | cara | cinza claro em volta do olho e embaixo | (196,190,188) → (150,144,144) embaixo | ok (n18: escurecida para o tom renderizado da ficha) |
| 7 | bico de frente | cunha pequena e afilada, mais estreita embaixo, ~1/3 da largura da cara | amarelo (253,204,52) em cima, laranja (233,150,16) embaixo | ok (n17: 4 degraus de 3,1 → 1,0 de largura, cumeeira inclinada) |
| 8 | bico de lado | cunha que desce em gancho, ~4 de comprimento | idem | ok |
| 9 | narina | ponto escuro no alto do bico, dos lados | (150,84,20) | ok |
| 10 | mandíbula de baixo | menor, recuada, laranja | (232,140,14) | ok |
| 11 | barbela | 2 lobos vermelhos largos sob o bico, o direito mais comprido | (205,35,29) → (140,20,22) | ok (n27: lobos mais largos e compridos, como na vista de frente) |
| 12 | penas da bochecha | blocos grossos em camadas, pontas para trás e para baixo | claros (217) na frente, médios (143) atrás | ok |
| 13 | nuca | telhas cinza que descem até o pescoço | (143,138,138), topo (64,64,64) | ok |

## Chapéu (`_detalhes` "Chapéu", vistas)
| # | detalhe | onde / forma | cor | status |
|---|---|---|---|---|
| 14 | cone | raio ~12, aba inclinada para a frente ~6° | palha (231,174,87)–(240,202,132) | ok |
| 15 | topo escuro | metade de cima do cone | (66,62,62) | ok |
| 16 | raios do chapéu | zigue-zague grosso brilhante em anel + riscos no topo | (253,226,84) / (255,246,170) | ok |
| 17 | aba | beirada grossa mais clara, com gomos de palha | (240,202,132) | ok |
| 18 | ponta | botão de palha no ápice | (240,202,132) | ok |
| 19 | talismã: placa | 3,3 × 5,8, de frente, x = ±9, pende da aba | — | ok |
| 20 | talismã: moldura | ouro grosso | (236,180,62) | ok |
| 21 | talismã: fundo e raio | fundo escuro, raio amarelo brilhante | (34,36,46) / (253,226,84) | ok |
| 22 | talismã: argola e cordão | argola de ouro no alto, cordão até a aba | ouro | ok |

## Túnica (`_detalhes` "Símbolo Elétrico", "Padrão do Traje", vistas)
| # | detalhe | onde / forma | cor | status |
|---|---|---|---|---|
| 23 | túnica | marinho, peito até a barra | (40,69,132) / (45,90,182) em cima | ok |
| 24 | quimono por baixo | V preto no peito | (38,40,44) | ok |
| 25 | gola | faixa cinza-escura larga (~1) dos dois lados do V, com fio de ouro fino por fora | (64,64,64) + ouro | ok (n17) |
| 26 | faixa (obi) | preta, larga, com dobras | (38,40,44) | ok |
| 27 | Símbolo Elétrico | octógono de ouro na frente da faixa, fundo preto, raio amarelo | ouro (236,180,62), raio (253,226,84) | ok |
| 28 | nó da faixa | do lado esquerdo, com 2 pontas penduradas | carvão | ok |
| 29 | painel da frente | retângulo escuro com moldura de ouro, do cinto até a barra | (24,36,74) | ok |
| 30 | raio do traje | raio amarelo grande no painel, brilha | (253,226,84) | ok |
| 31 | frisos laterais da túnica | faixa de ouro vertical ao lado do painel e barra de ouro onde a túnica lateral acaba | ouro | ok (n17: friso vertical e barra em 10,4 nos lados; painel desce até 7) |
| 32 | barra | barra dourada embaixo | ouro | ok |
| 33 | costas | marinho nos ombros, manto cinza no meio | — | ok |

## Ombreiras
| # | detalhe | onde / forma | cor | status |
|---|---|---|---|---|
| 34 | placa de cima | sobre o ombro, inclinada, friso de ouro grosso, miolo marinho | ouro + (40,69,132) | ok |
| 35 | placa do lado | topo azul arredondado, miolo escuro, 2 raios de ouro | (22,28,52) + ouro | ok |
| 36 | ponta em V de ouro na frente (vista de frente) | — | ouro | parcial (n27/n31: placa da frente com friso, raio e V pequeno; forma em caixa, não curva) |

## Asas e saia de penas
| # | detalhe | onde / forma | cor | status |
|---|---|---|---|---|
| 37 | asas | penas grossas em camadas, dos ombros até o quadril, face larga para a FRENTE (de lado só uma faixa sob a ombreira) | claro (177,164,160), médio (122,110,109), escuro (64,62,68) | ok |
| 38 | pontas das asas | degraus recortados, abrindo para fora embaixo | — | ok |
| 39 | saia de penas lateral | penas cinza que abrem dos lados do corpo abaixo das asas até ~±9,5 | (148,136,135) / (96,87,85) | ok (n19: asas viradas para a frente abrem até ±9,5; penas cinza-escuras atrás delas) |
| 40 | saia escura sob a túnica | penas carvão entre as pernas | (44,42,46) | ok |
| 50 | manto de penas das costas | 3 fileiras de penas claras do ombro ao quadril, de costas | (196,190,188) / (150,144,144) | ok (n22) |

## Cauda (`_detalhes` "Cauda (Energizada)")
| # | detalhe | onde / forma | cor | status |
|---|---|---|---|---|
| 41 | leque | ~8 penas largas, das costas para trás, de y≈6 a 26 | — | ok |
| 42 | ponta recortada | ponta em degrau/chanfro, não caixa reta | — | ok (n17: topo alinhado, cada segmento mais baixo) |
| 43 | tons | penas de cima mais claras, de baixo carvão; face de cima clara | (148,136,135) → (44,42,46) | ok (n21–n25: de cima claras, de baixo carvão; metade de cima da face mais clara; pontas carvão de costas) |
| 44 | raios da cauda | raio amarelo GROSSO só em algumas penas (3 a 4) | (253,226,84) | parcial (n29: raio grosso com halo em 5 das 8 penas, 2 a 3 visíveis por lado; na ficha os raios são mais irregulares) |

## Pernas e pés
| # | detalhe | onde / forma | cor | status |
|---|---|---|---|---|
| 45 | canela | amarelo-laranja forte, grossa | (233,158,16) | ok (n23: amarelo-laranja forte, canela mais grossa) |
| 46 | pé | largo, alto | idem | ok |
| 47 | dedos | 3 na frente + 1 atrás | idem | ok |
| 48 | garras | blocos pretos nas pontas | (38,40,44) | ok |
| 49 | coxa | carvão, escondida na saia | (38,40,44) | ok |

Status da Fase 2 valia na n31. A Fase 3 (auditoria) refez vários itens; o status atual está na seção abaixo, que manda.

## Fase 3: auditoria da n31, status na n39
Cores conferidas na ficha. O cone do chapéu nas `_vistas` agrupa em (98,88,86)/(115,94,86)/(134,103,80) + brilho
(252,241,177); na `_arte` e nos `_detalhes` é cinza-carvão com nervuras de palha.

| auditoria | item | o que ficou | status |
|---|---|---|---|
| 1 | chapéu (14–18) | cone de painéis cinza-carvão (98,88,86) com nervuras e trançado de palha (150,116,82); só os 28% de fora em bege com tábuas; anel de 5 "Z" amarelos (245,197,24) na metade da altura, com trincas curtas e brilho; sem sol no ápice; anel bege no ápice | ok |
| 2–3 | asas (37–39) | painel de penas em telha em volta dos flancos e das costas (2 fileiras), rente ao corpo, do ombro até ~7; lado em cinza-ardósia (106,110,122), frente e costas cinza-claro, pontas mais claras; sem espinho de lado, sem saia armada | ok |
| 4 | cauda (41–44) | leque em arco de +35° a −30°, carvão (52,52,58) e cinza-claro (172,172,178) alternados, raiz escura, pontas em degrau; ziguezague fino (245,197,24) em 5 penas | ok |
| 5 | ombreiras (34–36) | meia-calota em degraus (tampo + aba + arco + cúpula), navy (36,53,122) com borda de ouro; "Z" dourado na aba; placas do peito removidas | ok |
| 6 | bico de frente (7) | trapézio de 2,9 que afina até 1,2, amarelo (242,176,30) com topo (252,206,72) e sombra laranja (224,138,16), sem frisos marrons | ok |
| 7 | cabeça e bochechas (6, 12) | cabeça 1 un. mais estreita; 7 tufos triangulares por lado (claro/médio alternados), pontas para trás e para baixo; placas quadradas removidas | ok |
| 8 | medalhão e obi (26–28) | medalhão R 2,05 (passa da faixa em cima e embaixo, aro de ouro grosso); filetes de ouro na faixa; nó 1,6 × 1,6 com 2 pontas penduradas à direita de quem olha | parcial: na ficha o medalhão mede ~0,3 da largura do tronco, então não dobrei (a ficha manda) |
| 9 | painel e saia (29–32) | painel único do cinto até 7,2, moldura de ouro, raio grosso em ziguezague (245,197,24) com borda (255,224,102); saia navy em blocos, sem listras, barra de ouro em 10,4 | ok |
| 10 | talismãs (19–22) | x = ±9,8, colados sob a aba com alça curta de ouro, 6,5 de altura | ok |
| menor | bico de lado | 2,75 (~30% da cabeça), com gancho | ok |
| menor | sobrancelha (4) | cinza-carvão (64,64,68), rente (0,37 de saliência) | ok |
| menor | olho (1) | miolo (232,252,255), azul elétrico (40,150,255), borda (20,96,236) | parcial: a luz da prévia ainda acinzenta um pouco o miolo |
| menor | barbela (11) | vermelho vivo (212,32,32), sombra leve (176,26,28) | ok |
| menor | cinzas | luz neutra própria (sem puxar para o lilás); cinzas frios (142,142,148) etc. | ok |
| menor | inclinação do chapéu | −8°, aba 0,3 mais baixa | ok |
| menor | nuca | 4 penas pontudas cinza-médio | ok |
| menor | costas navy (33) | costas da túnica navy com barra de ouro | ok |
| menor | pernas (45) | amarelo-ouro (252,186,24) com faixas de escama (222,146,14) | ok |

Total atual: 51 itens; 49 ok, 2 parcial (medalhão e miolo do olho), 0 falta.

## Fase 4: segunda auditoria (n39), status na n49
Lição do dono aplicada: geometria antes de textura (volumes inclinados, sobrepostos e ligados; nada de placas soltas).

| auditoria 2 | item | o que ficou | status |
|---|---|---|---|
| 1 | cauda | 8 penas em LÂMINA (altura 5,2 → 4 → 2,6, espessura 2,4 → 1,5), curvando 8° para cima por segmento, sobrepostas; leque de +32° a −44°, chega a ~20 atrás e de y≈5 a 27 (medido na ficha); um tom por pena, carvão (58,58,62) e cinza-claro (168,168,172), alternância visível dos dois lados; sem pontas pretas; rachadura de raio grossa em cada pena carvão | ok |
| 2 | raio do avental | raio angular ϟ (2 dobras, cantos vivos, grosso em cima e em ponta embaixo), ~60% da largura do painel | ok |
| 3 | ombreiras | placa CHEIA encostada no tronco, topo inclinado 15°, + degrau que cobre o braço; fundo (30,36,64), borda de ouro grossa, 2 zigue-zagues de ouro na face de fora | ok |
| 4 | asas | mangas largas: 3 camadas × 4 telhas pontudas, quase verticais (4–8° de abertura), coladas na túnica, claras em cima e médias embaixo, pontas até ~7 | ok |
| 5 | bico | cunha larga em 3 camadas (a de cima mais larga e mais avançada, 2,9 de largura × 3,0 de projeção), gancho na ponta dentro do volume, narina; sem haste até a barbela | ok |
| 6–7 | chapéu | carvão frio (69,70,76) com nervuras; 5 rachaduras de raio separadas, de cantos vivos e pontas finas; aba grossa (1,5) com tábuas; ponta num cubo tan | ok; a forma do cone seguiu a ficha (ver abaixo) |
| 8 | olhos | fenda estreita inclinada para o bico, borda (26,63,208), azul (47,107,255), miolo branco-ciano e halo azul que brilha | ok |
| 9 | bochechas | os cubinhos saíram: 4 penas grandes por lado em lâmina, para trás e para baixo, em telha; 5 penas na nuca descendo até a capa | ok |
| 10 | barbela | 2 lóbulos (1,3 de largura), com vão, sem placa por cima; o da esquerda de quem olha é mais comprido | ok |
| menor | saia, capa, talismãs, pés, gola, nó | saia de penas cinza serrilhadas no lugar dos blocos pretos; capa de penas nas costas; talismã de 0,5 de espessura, girado 22°, com alça curta e raio maior; garras pequenas (dedos amarelos tocam o chão); gola larga com debrum de ouro; nó à direita de quem olha | ok |

**Decisões medidas na ficha:**
- Chapéu: a auditoria 2 pediu cone 1,5× mais alto e aba 10% menor. Medindo as vistas de frente e de trás, o cone da ficha é mais largo e mais baixo: ±5,8 em y=36, ±9,7 em y=34, ±12 em y=32. Mantive raio 12,2 e altura ~5; engrossei a aba e limpei a ponta.
- Olho: a auditoria 2 pediu miolo azul com pouco branco; nas `_vistas` o miolo é quase branco (216,251,252). Fiz a fenda mais estreita e com mais azul, mas mantive o miolo branco-ciano.
- Topo da cauda: a auditoria pediu a pena mais alta na altura dos olhos (~31); na ficha ela para em ~27. Segui a ficha.
- Penas: a auditoria 1 pediu raio de 1 px; a 2, raios grossos. Os `_detalhes` mostram grossos, então ficaram grossos.
- Nó e barbela: na prévia de frente, x negativo fica à direita de quem olha. A n38 tinha invertido isso; na n49 o nó voltou para x− e o lóbulo mais comprido da barbela ficou em x+ (esquerda de quem olha).

## Fase 5: proporções pela ARTE conceitual (n49 → n54)
Medido como fração da altura total, na imagem lado a lado `revisao/<rodada>_arte_lado.png` (modelo em yaw 32°, pitch −3°).

| medida | arte | n49 | n54 |
|---|---|---|---|
| largura da aba do chapéu | 0,56 | 0,60 | 0,57 |
| altura do chapéu (ápice → aba) | 0,20 | 0,21 | 0,19 |
| olho (do topo) | 0,21 | 0,25 | 0,23 |
| fim da barbela | 0,35 | 0,43 | 0,36 |
| topo do tronco / ombreira | 0,36 | 0,42 | 0,39 |
| cinto | 0,50 | 0,55 | 0,52 |
| fim da túnica / saia de penas | 0,80 / 0,84 | 0,81 / 0,85 | 0,78 / 0,81 |
| pernas visíveis | 0,18 | 0,14 | 0,19 |
| largura do tronco no cinto (3/4) | 0,22 | 0,21 | 0,20 |
| asa: comprimento / largura | 0,39 / 0,20 | 0,39 / 0,20 | 0,38 / 0,18 |
| cabeça com penas: largura | 0,25 | 0,28 | 0,27 |
| cauda: altura do leque | 0,56 | 0,55 | 0,54 |

O que mudou: pernas 2,0 mais compridas (o corpo todo sobe) e mais afastadas (±3,0); chapéu mais baixo sobre a cabeça,
raio 11,6 e inclinação −4° (o olho continua visível sob a aba, como na arte); barbela mais curta; penas da bochecha
menos abertas. Massa do tronco, das asas e da cauda já batia com a arte (diferenças abaixo de 10%), então não foram
reduzidas. Essas medidas seguem a arte; as vistas ortográficas da ficha mostram pernas um pouco mais curtas.

## Fase 6: suavidade (n54 → n60)
Peças: 266 → 201 (−24%). Proporções da Fase 5, chapéu, raios, talismãs, cores, rosto e ossos animáveis mantidos.
- Bochechas: 4 penas pontudas soltas por lado → 3 penas GRANDES deitadas em telha (face larga para fora, 9–10° de
  abertura), sobrepostas, a de baixo descendo até o pescoço.
- Nuca: 5 tufos → 3 penas grandes deitadas sobre a nuca e o pescoço, até a capa.
- Cabeça: crânio `arredondado2` (r 1,3); pescoço `octogono`.
- Ombreiras: placa `arredondado` + degrau `octogono` (quinas chanfradas), com UM friso de ouro contínuo medido na
  caixa do grupo (sem molduras empilhadas).
- Asas: 3 camadas × 3 telhas grandes de 2 peças (eram 4 de 3 peças), 4–8° de abertura; capa das costas 2 × 3; saia
  de penas 7 penas de 2 peças; todas com luz contínua e fio escuro fraco.
- Cauda: 10 penas (eram 8) com segmentos menos desiguais (5,0 → 4,4 → 3,5) e mais sobreposição: leque contínuo.
- Chapéu: botão `octogono` tan cobrindo o encontro dos gomos (sem os "dentes" no ápice).

## Fase 6b: pernas e frente da cabeça (n60 → n63)
Peças: 201 → 220.
- Pernas: coxa `octogono`, canela `arredondado` (pontas chanfradas, faixas de escama), tornozelo `octogono` chanfrado
  ligando ao pé `arredondado`; dedos com ponta em cunha descendo para a frente e garra curva inclinada 28°; dedo de
  trás inclinado com garra curva.
- Frente da cabeça: facetas do olho inclinadas 7° (o plano do olho olha um pouco para cima, a parte de baixo da face
  encorpa para a bochecha); chanfro de 45° entre a face e o queixo; sobrancelha mais fina e rente, acompanhando a
  inclinação. O chanfro da testa foi testado na n61 e retirado: virava um calombo escuro sob a aba.
- Olho, bico, barbela e cores mantidos.

## Fase 7: rosto com relevo e frente mais magra (n63 → n69)
Costas, capa de penas, cauda e chapéu não mudaram (o chapéu só subiu 0,6 para o olho aparecer sob a aba).
- Cara em V vista de cima: frente estreita (meia largura 1,1 → 0,6) com uma QUILHA em losango, de cor clara, da
  testa ao bico e do bico ao queixo; facetas do olho anguladas 46° para os lados (eram 34°), um tom abaixo da quilha;
  miolo escondido atrás do V. Bochechas recuam (crânio com meia largura 3,7 → 3,3, penas da bochecha rentes, com 5–6°
  de abertura, mais claras). Bico um pouco mais estreito (topo 2,9 → 2,5) entrando na cabeça; barbela 1,2 por lóbulo.
- Pescoço octogonal mais fino (±2,6 → ±2,1).
- Larguras de frente (fração da altura, trecho central sem talismãs), n63 → n69: cabeça no olho 0,220 → 0,201;
  cabeça na barbela 0,233 → 0,213; pescoço/gola 0,237–0,241 → 0,185–0,189; ombros 0,355 → 0,334; peito 0,396 → 0,390.
  Referência: ficha de frente, cabeça com os tufos 0,30 (miolo da cara ~0,14), pescoço 0,15, ombros 0,39; arte (3/4),
  cabeça 0,25, pescoço ~0,12.

## Fase 7b: olhar imponente (n69 → n74)
- Olho: fenda alongada para trás (3,0 × ~0,9, ~1,6–3 : 1), borda de baixo reta subindo de leve para trás, pálpebra
  cortando o topo em diagonal (~11°) até o bico (aparece ~2/3 da altura). Íris azul elétrica (47,107,255) no olho
  todo, sombra da sobrancelha no alto (30,72,206), miolo branco-ciano (226,250,255) com anel ciano do lado do bico,
  1 px de reflexo branco, fio escuro só em cima; sem halo nem contorno grosso. Tudo brilha.
- Sobrancelha: bloco cinza-carvão (70,70,76) saliente (0,38), seguindo a pálpebra e indo até a base do bico.
- Cara mais clara para ler de frente no jogo: facetas e quilha (210,210,216), testa (92,92,100) só acima da sobrancelha.
- Penas da bochecha recuadas (começam atrás da faceta): não cobrem mais o olho visto de lado.

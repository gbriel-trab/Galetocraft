# Morcegalo (#010): detalhes da ficha

Fontes: `_ficha` (com a paleta), `_arte`, `_vistas`, os 5 quadros de `_detalhes` e a expressão neutra de
`_expressoes`. Os RGB foram amostrados com PIL nos PNGs da ficha.

- Paleta da ficha: (58,30,101), (140,85,184), (192,139,232), (232,186,240), (215,81,151), (252,216,185),
  (253,184,4), (97,71,73).
- Nas vistas, o roxo do corpo puxa para o magenta: (80,42,125) no lado e (59,25,82) embaixo.

Status: ok / parcial / falta. A coluna "status" é da rodada n26; as correções da auditoria da n26 (rodadas n27–n32) estão na seção do fim.

## Rosto e cabeça (expressão neutra)
| # | detalhe | onde / forma / tamanho | cor (amostrada) | status |
|---|---|---|---|---|
| 1 | cabeça | bloco grande e facetado, ~1/3 da largura do corpo; quinas da frente cortadas | (74,38,120) lado, (56,28,84) sombra | ok |
| 2 | testa / sobrancelha | aba grossa por cima do olho, descendo em V até o bico | (81,37,76) sombra, topo (106,65,159) | ok |
| 3 | olho: forma | largo, com o alto cortado reto pela sobrancelha brava; fica na quina, ao lado do bico | — | ok |
| 4 | olho: esclera | amarelo claro | (252,224,116) | ok |
| 5 | olho: íris | laranja-vermelha, puxada para o lado do bico | (220,90,30) | ok |
| 6 | olho: pupila | redonda, escura, dentro da íris | (40,10,20) | ok |
| 7 | olho: brilho | ponto branco no alto da íris | branco | ok |
| 8 | olho: contorno | fio marrom-escuro | (90,36,30) | ok |
| 9 | cara em volta do olho | roxo escuro, sem máscara de outra cor | (74,38,120) | ok |
| 10 | bico de frente | cunha curta: larga em cima, afina para baixo até a ponta do gancho | (244,195,193) | parcial: é uma cunha (cera + mandíbula inclinada + gancho em V), mas a frente da cera ainda aparece como uma faixa reta em cima |
| 11 | bico de lado | gancho curto: o topo cai até a ponta e a mandíbula de baixo é menor | creme-rosado; sombra (226,176,156) | ok (em blocos, sem a curva lisa) |
| 12 | narinas | 2 pontinhos escuros no alto do bico | (104,60,66) | ok |
| 13 | barbela | 2 lóbulos magenta em blocos, embaixo do bico, até o alto do peito | (212,78,154) | ok |
| 14 | crista | 4 tufos magenta em degraus, da testa para a nuca; de frente parece um "+" | (240,86,179), sombra (186,40,133) | parcial: forma e cor ok; na lateral esquerda da ficha ela desce mais pela testa |
| 15 | bochechas / gola | penas roxas mais claras em blocos embaixo da cabeça, dos lados e atrás | (140,85,184) | ok |
| 16 | nuca de costas | capacete roxo com aba (degrau) | (84,49,131) | parcial: é o crânio arredondado, sem a aba separada |

## Orelhas (quadro "Orelhas Noturnas")
| # | detalhe | onde / forma / tamanho | cor | status |
|---|---|---|---|---|
| 17 | formato | triângulo grande, ponta para cima e para fora; borda de fora quase vertical; ~altura da cabeça | — | ok |
| 18 | moldura | borda roxa grossa em volta (2 lados), mais clara em cima | (94,47,133), luz (140,85,200) | ok |
| 19 | pele de dentro | rosa: mais escura (magenta) junto da moldura de cima, mais clara embaixo e para fora | (179,66,141) → (234,122,198) | ok (3 faixas chapadas na diagonal) |
| 20 | dobra interna | degrau (dobra) mais escuro no meio da pele | (160,55,135) | parcial: é uma linha pintada, não um degrau em volume |
| 21 | costas da orelha | roxo escuro liso | (84,49,131) | ok |

## Asas (quadro "Asa Membranosa")
| # | detalhe | onde / forma / tamanho | cor | status |
|---|---|---|---|---|
| 22 | borda de ataque | barra grossa roxo-violeta do ombro ao pulso e à ponta | (94,47,133), topo mais claro | ok |
| 23 | pulso | junta saliente no alto da asa | idem | ok |
| 24 | dedos | 2 ossos escuros do pulso até a beirada + o dedo de fora | (58,30,101) | ok |
| 25 | membrana: degradê | em faixas: magenta escuro em cima (embaixo do braço), rosa claro na beirada | (160,55,140) → (207,86,171) → (240,140,210) | ok |
| 26 | beirada recortada | arcos entre os dedos, com pontas | — | ok |
| 27 | garra da ponta | garra creme na ponta de fora (e na ponta do dedo) | (252,216,185) | ok |
| 28 | envergadura | ~1,2× a altura | — | ok |

## Peito e corpo (quadro "Peitoral Sombrio")
| # | detalhe | onde / forma / tamanho | cor | status |
|---|---|---|---|---|
| 29 | escamas do peito | placas grossas em fileiras sobrepostas, com a ponta em V (chevron) | lavanda (213,162,216) | ok |
| 30 | desenho do V | o peito todo forma um V largo em cima que afina até um ponto embaixo | — | ok |
| 31 | ordem de cores | fileira de cima lilás-violeta; meio lavanda clara; embaixo lilás | (194,121,206) / (230,200,240) / (200,134,199) | ok |
| 32 | corpo | penas roxas em blocos escalonados (telhas) em volta do peito | (80,42,125), base (59,25,82) | ok; de lado a ficha mostra mais lavanda e membrana na frente do corpo |
| 33 | costas | blocos lilás e roxos alternados (xadrez grande) | (186,101,179) / (115,49,121) | parcial: a cauda cobre boa parte das costas na traseira |
| 34 | saia de baixo | beirada inferior do corpo em degraus escuros | (59,25,82) | ok |

## Cauda (quadro "Cauda Escura")
| # | detalhe | onde / forma / tamanho | cor | status |
|---|---|---|---|---|
| 35 | formato | leque cheio de penas grossas em foice, que sobem e caem para trás | — | ok |
| 36 | número de penas | ~5 visíveis de lado, sobrepostas | — | ok (5 no meio e 2 pares embaixo, que fazem as diagonais de costas) |
| 37 | faixa da raiz | roxo escuro | (90,20,114) | ok |
| 38 | faixa do meio | violeta forte | (160,64,204) / (198,86,240) | ok |
| 39 | faixa clara | lilás-rosa antes da ponta | (207,132,200) | ok |
| 40 | ponta | creme-rosado, afilada e curvada (cunha), ~1/3 do comprimento | (250,214,227) | ok nas 3 penas de cima (bloco + ponta em losango); as de baixo terminam em lilás-rosa |
| 41 | de costas | coluna central listrada e penas descendo em diagonal para os lados | — | parcial: a coluna listrada aparece (os cortes das penas são lilás claro), mas o xadrez da ficha não fica no mesmo lugar |

## Pernas e pés (quadro "Garras")
| # | detalhe | onde / forma / tamanho | cor | status |
|---|---|---|---|---|
| 42 | canela | grossa, creme-rosada, em blocos | (228,172,170) | ok |
| 43 | coxa | escondida embaixo da saia roxa | — | ok |
| 44 | dedos | 3 dedos grossos para a frente, abertos | creme-rosado (240,190,185) | ok |
| 45 | garras | 3 garras grandes em bloco, ROXO-escuras (não cinza) | (89,54,109) | ok |
| 46 | dedo de trás | 1 dedo curto com garra | idem | ok |

## Gerais
| # | detalhe | status |
|---|---|---|
| 47 | olhos brilham no escuro (Sombrio) | ok (só o amarelo vai para a `_glowmask`) |
| 48 | acabamento: 2 ou 3 tons chapados por bloco, sem ruído | ok |

## Correções da auditoria da n26 (rodada final n32)
Nesta tabela, "ficha manda" marca os pontos em que a auditoria contradiz o RGB ou a forma amostrados na ficha.

| # auditoria | item | status na n32 |
|---|---|---|
| 1 | barbela | ok: 2 tiras magenta verticais e estreitas (1,25 de largura cada) sob a base do bico, até o começo do peito, com ponta arredondada; dentro da largura do bico. Os blocos laterais saíram. |
| 2 | bico | parcial. De frente é uma cunha de 2 degraus (3,5 → 2,4 → 1,3; ~1/4 da cabeça) e o losango saiu. De lado, a mandíbula de cima avança até z −13,6 e dobra para baixo por cima da de baixo. A cor única é (246,196,186), sem marrom embaixo; testa avançada. Ficha manda: a cor é o creme-rosado da neutra (247,188,183), não #F2D5C4. Continua em blocos (degraus), sem curva lisa. |
| 3 | penas do corpo | ok: 5 fileiras horizontais de penas largas e baixas, base índigo, 2 dentes violeta embaixo de cada uma (beirada serrilhada); a última faz a saia sobre as coxas. Ficha manda: a base ficou (84,44,136)–(98,52,152), mais clara que #3E2470, porque a ficha amostra (80,42,125) e a prévia escurece. |
| 4 | peitoral | ok: escudo em V de chevrons em degrau, sem losangos e sem contorno interno; lilás claro no centro, lavanda nas bordas, fileiras cada vez mais estreitas. Ficha manda: na frente da ficha a ponta do V chega perto de y 8, e não a 2/3 do tronco. |
| 5 | cauda | ok: foices que sobem e curvam cada vez mais (0,7×, 1×, 1,5× por junta), ponta afinando em 2 degraus até ponta aguda; violeta opaco, rosa → creme só no terço final; cortes sem lavanda acinzentada; penas de cima mais compridas. Ficha manda: o creme é rosado (250,214,227), não #F5DDC0. |
| 6 | asas | ok: braço sobe ~40° até o pulso na base das orelhas; dedos em leque (~30° na borda, 58° e 75°); membrana magenta viva com degradê a partir dos ossos e beirada clara; 3 garras creme pontudas (2 blocos que afinam). |
| 7 | olhos | ok: ~25% menores, junto da base do bico, com a pálpebra roxa escura cobrindo ~40% de cima em diagonal descendo para o bico; íris laranja-avermelhada, pupila pequena e brilho. Ficha manda: o amarelo é o claro da neutra (250,228,126), não #F5BE20. |
| 8 | traseira | parcial: a coluna central é de listras lavanda/violeta e termina numa ponta clara entre as pernas; a sela de cima tem tabuleiro lavanda-claro/índigo, mas a cauda cobre boa parte dela. |
| 9 | sobrancelha e cabeça | ok: aba recolhida para dentro da cabeça (sai 0,65 da faceta e não chega à quina do lado); topo da cabeça sem bordas claras; mandíbula e gola em roxo escuro. |
| 10 | crista | ok: 5 espigões finos (1,6 de largura) em degrau, cada um mais alto e mais para trás, com ponta mais clara; começa na linha da sobrancelha. Ficha manda: a altura máxima continua ~34,8, porque as vistas da ficha mostram a crista até ~35. |
| menor | contorno vermelho dentro da orelha | ok: removido |
| menor | abertura das orelhas | não aplicado: o contorno da ficha de frente pede a borda de fora quase vertical em x≈±12. Deixar a orelha 10° mais vertical abria vão vermelho na comparação. Ficha manda. |
| menor | pés próximos | ok: cada perna 0,8 para fora (x ±5,4) |
| menor | nódulo entre as pernas | ok: era a ponta da pena de baixo da cauda (y 1,2); a pena foi removida e as outras de baixo subiram |
| menor | lascas no pescoço | ok: saíram as placas de fora da fileira de cima do peito |
| menor | orelha sem membrana em n26_rosto | não é defeito do modelo: o close do rosto descarta faces grandes que passam do raio. A pele aparece no 3/4 e nas vistas. |
| menor | cor das pernas | ok: (240,194,180), pêssego-rosado entre a ficha (228,172,170) e o quadro "Garras" (240,190,185) |
| menor | dedos e garras dos pés | ok: dedos mais grossos (2,4) e separados; garras mais altas (2,9) |
| menor | garras das asas | ok: maiores e pontudas, também nos dedos do meio e de dentro |
| menor | colar lavanda alto | ok: o peito começa em y 19,8, abaixo da base do bico; sob o bico ficam a gola roxa escura e a barbela |

## Segunda auditoria (n32), corrigida nas rodadas n33–n40 (final n40)
"Medido" marca as decisões tomadas medindo a ficha quando as auditorias se contradiziam.

| # | item | status na n40 |
|---|---|---|
| 1 | bico | ok: 3 degraus que estreitam para baixo (base ±2,1 ≈ 1/3 da cabeça, depois ±1,4 e ±0,7) e avançam (gancho ~3 à frente); termina pouco abaixo dos olhos; topo (252,216,185), frente (244,198,182), lados (232,180,168); narinas (97,71,73) nos lados; sem bloco de baixo comprido e sem taupe. |
| 2 | crista | ok, medido: na frente das vistas a crista é uma torre larga (~4,8 → topo ~2,6) que desce até a testa; na lateral ela sobe em degraus para TRÁS (o bloco mais alto fica junto da orelha). Ficou um leque de 5 blocos de 4,2 de largura com topo de 2,4, do meio das sobrancelhas até a nuca, magenta (215,81,151), topo rosa (232,136,200). A auditoria 2 pedia o mais alto no 2º degrau a partir da frente; a ficha manda. |
| 3 | olhos | ok, medido: na frente da ficha o olho tem 3,0 de 11,5 de cabeça (~26%), como diz a auditoria 2 (a 1 pedia menor). Agora ru 2,05: dourado (253,184,4) clareando para creme junto da íris, íris laranja-avermelhada, pupila escura, brilho branco perto do bico; terço de cima cortado reto e inclinado pela sobrancelha. |
| 4 | sobrancelha/testa | ok: 2 abas grossas (2 de altura) saindo 1,1 da face, inclinadas 22° para o bico, com topo (140,85,184) e baixo (42,20,80); ponte em V por cima do bico e testa em degrau; faixa de bochecha (140,85,184) sob cada olho; aba do boné na nuca. |
| 5 | peitoral | ok: 4 fileiras de escamas (largura 13,6 → 4,8), cada uma um pouco à frente da de cima, com a beirada de baixo em dente de serra (quadrados girados 45°); face (232,186,240), topo (247,208,251), fio de baixo (192,139,232); sem textura de tijolo. O volume do peito deixou de cobrir as laterais do escudo. |
| 6 | corpo | ok: telhas inclinadas, fileiras desencontradas, base (62,32,108)/(74,40,124) e 2 pontas em V (140,85,184) por pena; 1 em 3 pontas lilás (192,139,232); saia de pontas sobre as coxas; a barra azul saiu. |
| 7 | cauda | ok: penas-foice em lâmina (largas de lado, finas de costas), 5 segmentos que afinam até a ponta, com curva crescente (0,6x a 1,5x); gradiente (140,85,184) → (179,82,185) → (232,186,240) → (250,182,182) → (252,216,185); sem cubinhos "dedo" e sem cinza; cortes de costas alternando violeta/lilás. |
| 8 | asas | ok: os dedos acabam nas pontas do recorte; os cubinhos creme pendurados saíram e só as pontas do recorte são pintadas de creme; membrana em 3 tons a partir dos ossos (179,82,185) → (215,81,151) → (232,136,200), sem listras e sem franja branca; pulso saliente. Medido: a altura subiu só ~1 em relação à n32, porque na frente da ficha a ponta de baixo fica em y≈10–11. |
| 9 | orelhas | ok: moldura de 2 de largura e 2,1 de profundidade, pele rebaixada atrás dela (concha) e grossa (1,0), interior (209,83,171) com degraus mais claros (232,136,200), borda (90,47,146) e topo (140,85,184), degrau na beirada de baixo atrás. |
| 10 | paleta | ok: nova função de luz (a sombra só escurece multiplicando, sem lavar para o cinza) e cores da paleta da ficha em bico, peito, membrana, orelha, barbela e pernas. |
| — | barbelas | ok: 2 lóbulos arredondados curtos e largos (~metade da largura do bico cada), de (215,81,151) a (194,62,147), terminando no topo do peito. |
| — | gola do pescoço (hackle) | ok: penas com pontas violeta/lilás em volta do pescoço. |
| — | pernas e garras | ok: tarso mais grosso (4,0), (248,204,186), "calça" de penas no alto; garras mais curtas (~2/3 do dedo). |
| — | nódulo entre as pernas | parcial: as penas de baixo da cauda subiram; com a câmera exatamente na altura das pernas ainda pode aparecer uma ponta pequena atrás. |

## Fase 5: proporções arte × modelo (rodada final n54)
Todas as medidas são fração da altura total, da ponta da orelha à base dos pés.
- A arte (`010_morcegalo_arte.png`, ficha nova do dono) está em 3/4, com escorço. As medidas de largura, envergadura e
  cauda foram conferidas também nas vistas novas (`_vistas.png`), que são ortográficas.
- O modelo foi medido na geometria da n54 (H = 41,2).
- O lado a lado no ângulo da arte (yaw 50, pitch −2) está em `revisao/n54_arte_lado.png`.

| medida | arte | vistas novas | modelo n54 | situação |
|---|---|---|---|---|
| largura do tronco (frente) | 0,45 em 3/4 (largura + profundidade) | 0,43 | 0,41 | ok |
| profundidade do tronco (lado) | — | 0,33 | 0,36 | ok (+9%) |
| altura do tronco (gola → barriga) | 0,43 | 0,40 | 0,39 | ok |
| altura da cabeça (sem orelhas e crista) | 0,19 | 0,20 | 0,20 | ok |
| altura da crista acima do crânio | 0,08 | 0,13 (torre de frente) | 0,09 | ok, pela arte: 3 tufos |
| pernas visíveis (barriga → chão) | 0,21 | 0,20 | 0,21 | ok |
| envergadura | 0,94 (asa erguida, em escorço) | 1,19 | 1,18 | ok, pelas vistas |
| cauda: comprimento | 0,35 (escorço) | 0,51 | 0,55 | ok (+8%) |
| cauda: altura do leque | 0,47 | 0,49 | 0,49 | ok |
| espessura das penas grandes da cauda | 0,09 | 0,10 | 0,10–0,11 | ok |

Formas corrigidas pela arte:
- **crista:** 3 tufos magenta em blocos, o mais alto atrás, descendo até a sobrancelha, no lugar do leque de 5 blocos;
- **canelas:** inclinadas 16°, nascem atrás na junta do tarso e descem para a frente até o pé;
- **cauda:** penas grossas e curvas, com a ponta clara afinando num losango; sem segmento "dedo";
- **entre as pernas:** nada abaixo de y 8,8 na faixa |x| < 3 (as penas de baixo da cauda subiram).

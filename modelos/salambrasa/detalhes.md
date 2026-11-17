# Salambrasa (#012): lista de detalhes da ficha

Cores amostradas com PIL:
- **paleta** = quadros da Paleta de Cores de `_ficha.png`;
- **arte** = `_arte.png`;
- **vistas** = `_vistas.png`, que tem um tom mais avermelhado por causa do brilho do fundo.

Unidades: altura total de 39,4; frente = -z.

Status inicial (n19) → status final (n27).

## Paleta (`_ficha`)
| # | Detalhe | Cor (RGB amostrado) | n19 | final |
|---|---|---|---|---|
| 1 | carvão | (46,35,44) | parcial (tom cinza) | ok (sombra GRAFITE_ESC) |
| 2 | cinza-roxo | (103,78,95) | parcial | ok (cabeça / viseira) |
| 3 | malva | (131,94,111) | parcial | ok (bico, dedos, face clara) |
| 4 | vermelho da crista | (202,24,30) | parcial (222,44,40) | ok |
| 5 | laranja-vermelho | (253,69,11) | parcial | ok |
| 6 | laranja | (253,115,2) | parcial | ok |
| 7 | amarelo das brasas | (254,201,37) | ok | ok |
| 8 | creme do olho | (251,223,198) | ok | ok |

## Cabeça e rosto (`_expressoes` neutra, `_vistas` frente)
| # | Detalhe | Onde, forma e tamanho | Cor | n19 | final |
|---|---|---|---|---|---|
| 9 | crânio | bloco largo (~10,5 de frente) e alto (y 23–32) | (110,57,72) arte | parcial (escuro, quadrado) | ok |
| 10 | face clara em volta e abaixo do olho | faixa malva (y 24,7–27,2) | (150–180,100–115,110–120) | falta | ok |
| 11 | viseira em V | faixa grossa (~2), laterais mais altas (y 32,3), meio mais baixo (y 28,9) | (113,61,76) | parcial (V fraco) | ok |
| 12 | olho: forma | grande, topo reto cortado pela viseira, fundo arredondado; de frente ~2,5 × 2,1, de lado ~3,9 × 3,2 | — | parcial | ok |
| 13 | olho: esclera | creme | (254,229,215) | ok | ok |
| 14 | olho: íris | laranja-avermelhada, do lado do bico | (216,68,8) | ok | ok |
| 15 | olho: pupila | escura, redonda | (33,7,9) | ok | ok |
| 16 | olho: brilho | ponto branco | — | ok | ok |
| 17 | olho: contorno | aro avermelhado/escuro | — | parcial | ok |
| 18 | bico de frente | cunha que estreita para baixo (3,4 em cima → ponta, 4,8 de altura) | (150,87,97) | parcial (retângulo) | ok |
| 19 | bico de lado | longo (~4,5), topo inclinado, gancho para baixo | malva | ok | ok |
| 20 | mandíbula | pequena, recuada, escura | — | ok | ok |
| 21 | narina | — | — | não aparece na ficha | — |
| 22 | barbela | — | — | não existe na ficha | — |

## Crista de Brasa (`_detalhes` 1)
| # | Detalhe | Onde, forma e tamanho | Cor | n19 | final |
|---|---|---|---|---|---|
| 23 | crista: forma | moicano de blocos em degrau: coluna central estreita (±1,8) até y 39,4; blocos laterais mais baixos | (226,34,32); topo (251,83,82) | parcial (boné largo ±5) | ok |
| 24 | crista: nº de lâminas | 5 blocos de frente para trás; o mais alto no meio, os de trás caindo sobre a nuca | — | ok | ok |
| 25 | lóbulos vermelhos dos lados da cabeça | x ±5,3–6,7, y 25,5–30,6 | vermelho | parcial | ok |

## Juba / Pelagem Ígnea (`_detalhes` 3)
| # | Detalhe | Onde, forma e tamanho | Cor | n19 | final |
|---|---|---|---|---|---|
| 26 | penas da bochecha | emolduram o rosto embaixo e atrás do olho; vermelho → laranja | (245,139,0) | parcial | ok |
| 27 | juba | leque grande de penas grossas pontudas em volta do pescoço (y 17–29), abrindo para os lados | vermelho → laranja (253,115,2) → amarelo (254,201,37) | parcial (pequena) | ok |
| 28 | penas da juba | blocos grossos, ponta em losango, 3 faixas de cor | — | ok | ok |

## Pescoço e barriga
| # | Detalhe | Onde, forma e tamanho | Cor | n19 | final |
|---|---|---|---|---|---|
| 29 | pescoço | alto, em S, roxo atrás | (99,45,58) | ok | ok |
| 30 | placas laranja | ~7 faixas em degrau da garganta ao peito, mais largas no meio (~9,4); topo claro, fio escuro embaixo | (240,112,40) / (253,140,60) | parcial (marrons, inclinadas para baixo: escuras no jogo) | ok |
| 31 | barriga laranja entre as patas | — | laranja | ok | ok |

## Corpo / Placas Quentes (`_detalhes` 2)
| # | Detalhe | Onde, forma e tamanho | Cor | n19 | final |
|---|---|---|---|---|---|
| 32 | corpo | roxo-ameixa, mais avermelhado que cinza | (99,45,58); sombra (71,30,40) | parcial (cinza-roxo) | parcial: (124,46,58) = cor da arte compensada pela luz; as `_vistas` são mais vermelhas e a Paleta de Cores mais fria |
| 33 | manchas do dorso | lateral: (z -2,1, y 20) 3,4 × 1,3; (z 4,9, y 18) 3,4 × 2,1 | (253,206,0); borda laranja | parcial | ok |
| 34 | manchas do flanco | (z 1,2, y 14,3) 3,1 × 2,3; (z -2, y 11,8) e (z 5,5, y 11,5) pequenas | — | parcial (fora do lugar) | ok |
| 35 | fenda em Y no ombro | sobre as escamas, brilhante | amarelo / laranja | ok | ok |
| 36 | escamas do ombro | 3–4 escamas grafite grossas, como asa dobrada | (92,32,46) | ok | ok |
| 37 | penas de fogo do ombro | vermelho → laranja → amarelo, apontando para trás | — | ok | ok |

## Cauda Incandescente (`_detalhes` 4)
| # | Detalhe | Onde, forma e tamanho | Cor | n19 | final |
|---|---|---|---|---|---|
| 38 | cauda | grossa, laço para cima e gancho para a frente | roxo (99–107,34–41,46–52) | ok | ok |
| 39 | manchas laterais da cauda | 8: (25,9; 13,5) (25,9; 21,9) 3 × 4 (22,7; 17) (19,7; 26,7) 4,2 × 3,1 (18,2; 14) (13,2; 14,2) (13,1; 29,1) (18,6; 29,8) | amarelo | parcial (pequenas, 1 por segmento) | ok |
| 40 | oval de trás | hexágono central grande 4,4 × 5,2 em y 17,9; um embaixo 3,5 × 3 em y 10,4; um pequeno em cima em y 22,8; quatro nos lados (x ±5, y 21,3 e 14,7) | amarelo | parcial | parcial: manchas no lugar e no tamanho da ficha, mas de trás o alto do laço da cauda tapa a cabeça (nas laterais da ficha o laço sobe até y 31; na vista de trás ele parece mais baixo) |
| 41 | faixa laranja | embaixo da base da cauda e por dentro do gancho | (240,81,1) | ok | ok |

## Patas (`_detalhes` 5)
| # | Detalhe | Onde, forma e tamanho | Cor | n19 | final |
|---|---|---|---|---|---|
| 42 | perna | roxa em cima | (99,45,58) | ok | ok |
| 43 | faixa laranja no meio da perna | — | (248,116,6) | ok | ok |
| 44 | tornozelo e pata | roxos | — | ok | ok |
| 45 | dedos | 3 grandes na frente, cubos; cinza-malva claro | (167,99,113) | parcial (cinza frio) | ok |
| 46 | dedo de trás | 1 menor | — | ok | ok |
| 47 | mancha na coxa | pequena, glow | — | ok | ok |

## Resumo da Fase 2 (n27)
- **ok:** 43 itens.
- **parcial:** 2 itens (#32 tom do corpo; #40 oval de trás e cabeça).
- **falta:** 0 itens.
- **n/a:** 2 itens (#21 narina e #22 barbela não aparecem na ficha).

## Fase 3: auditoria da n27 → n31

A cor do corpo agora segue os quadros da Paleta de Cores, porque as `_vistas` têm luz avermelhada.

| Item da auditoria | Correção | Status n31 |
|---|---|---|
| 1. Cor do corpo | Carvão-arroxeado da paleta: base (66,51,62), luz (87,70,80), sombra = quadro carvão (46,35,44). Cabeça (82,64,76), sobrancelha (60,47,56). O vermelho ficou só na crista, nos lóbulos e nas penas. | ok |
| 2. Bico | Os 3 cubos em escada saíram. Agora é uma cunha curta de topo reto na altura do olho (3,4 × 1,8 × 3,8), com parte de baixo mais estreita (V de frente), gancho pequeno inclinado e narina escura. A ponta não passa do queixo. Cor malva (131,94,111). | ok |
| 3. Olhos | Menores (~1/4 da cabeça), com o topo encostado e cortado na diagonal pela sobrancelha (meio fechados, bravos). Esclera (244,230,220), íris (216,64,28) com anel escuro (~60% do olho), pupila, brilho e contorno (192,48,24). | ok |
| 4. Gola | 6 penas pontudas de cada lado, caindo ~70° para baixo, só em volta da garganta e atrás da cabeça, com degradê vermelho (200,40,32) → laranja (240,112,32) → amarelo (248,176,32). Saíram o "babador" e as penas da metade de trás do pescoço. A largura de frente fica em ~1,2× a cabeça. | ok |
| 5. Peito e barriga | Escudo de 5 faixas coladas (0,4 à frente do pescoço), cada uma inclinada como a curva da garganta, em contorno oval. Cores (244,160,80) com linhas (208,106,32). Faixa laranja (232,138,48) embaixo do tronco inteiro, ligando o peito à barriga da cauda. | ok |
| 6. Asa | Os triângulos em serrote viraram 5 penas longas (2,8 × ~10) em leque para trás, umas sobre as outras: vermelho → laranja → ouro (248,192,32) só na ponta. A sombra das penas escurece sem puxar para o oliva. | ok |
| 7. Manchas | Octógono amarelo cheio (248,192,32) com borda laranja fina (240,112,32), sem miolo nem halo. 3 manchas em fila no dorso, 1 no flanco e 1 no quadril de cada lado. Para tirar as frestas, as manchas do corpo pintam só a face de fora; na cauda saíram as manchas do topo, e as de trás só aparecem em faces bem viradas para trás. | ok |
| 8. Cauda | Afina de 7,8 até 2,8 de altura (~35%) e de 10,6 até 3,4 de largura. Os 2 últimos segmentos curvam para baixo. Os segmentos se sobrepõem 0,8 e saiu o filete laranja de dentro, que parecia costela. | parcial: a curva não foi recuada, porque o perfil medido na ficha (lateral esquerda, sem corte) já bate com a curva do modelo |
| 9. Cabeça e lóbulos | Cabeça escurecida. Lóbulos de 1,4 × 3,2 na altura do olho, atrás dele, sem descer até a gola. | ok |
| 10. Crista | Blocos atarracados inclinados 8–30° para trás, com a massa deslocada para trás. De frente forma a cruz: coluna de ±1,8 e degrau da largura da cabeça. Vermelho (224,40,40), topo (240,72,72). | parcial: não baixei o topo 30%, porque a silhueta da ficha chega a y 39,4. Subi a cabeça 1 unidade, então a crista caiu para ~0,8× a altura da cabeça. |
| Menores | Faixa da perna laranja com faixa escura no meio, sem amarelo. Dedos (180,162,172). Y do ombro mais grosso. Ombreira menor e mais alta, sem placa pendurada na frente da pata. Pescoço mais longo, com a cabeça 1 unidade mais alta e 0,5 mais à frente. O topo da crista de trás saiu do quase-branco. | ok |

Na prévia, as manchas amarelas parecem mais escuras nas faces de lado por causa da luz da prévia. No jogo elas brilham pela `_glowmask`.

## Fase 4: segunda auditoria da n31 → n41

Regra do dono aplicada: primeiro a geometria (volumes inclinados, sobrepostos e ligados), depois a textura.

| Item da auditoria 2 | Correção | Status n41 |
|---|---|---|
| 1. Bico | Saíram o "nariz" retangular e o bloco central. De frente é uma cunha em V em degraus (3,4 → 2,6 → 1,8 → 1,0) logo abaixo do vértice da sobrancelha. De lado tem ~4 à frente da face, dorso reto e ponta curvando para baixo, com narina de 1 px perto da base. Malva clara (138,116,128), com a faixa de baixo um tom mais escura. | ok |
| 2. Sobrancelha e cabeça | A viseira é cinza-malva (110,92,104), com topo mais claro, passa só 0,5 da face e cada metade desce 16° até o vértice sobre o bico. A borda de baixo corta o alto do olho em diagonal. A cabeça clareou para cinza-roxo (96,78,90), perto do quadro (103,78,95). | ok |
| 3. Barriga | 6 escamas em chevron, laranja da paleta em degradê (pêssego (255,196,116) → (252,160,52) → (246,112,36)). Linha escura em arco, sem friso amarelo e com 0,5 de relevo. Seguem uma curva em S, da garganta até o peito, com recheio atrás (sem vãos). | ok |
| 4. Pescoço e juba | A cabeça subiu 2 e o pescoço escuro aparece, com a frente laranja. A juba nasce atrás e abaixo da bochecha e cai pelas costas do pescoço até a cernelha: 10 pares de penas pontudas com degradê vermelho → laranja → amarelo e 2 pares carvão misturados. De frente ficam só 2 abas ao lado do queixo. | ok |
| 5. Crista | 5 lâminas finas (1,9 de espessura) tombadas 26–38° para trás, sobrepostas como telhas, a de trás mais alta, mais 2 laterais baixas (frente estreita mantida). Lados (200,40,42), alto (232,68,58). | ok |
| 6. Corpo | Placas do ombro e coberturas em cinza-malva (110,92,104) com borda (138,116,128). Terço de baixo do tronco laranja (247,147,30), com transição de 1,4. | ok |
| 7. Dorso | Tronco liso mais duas camadas de lombo chanfradas, mais curtas e estreitas por cima (arco baixo-alto-baixo, sem ameias). As escamas da asa ficaram mais baixas e não passam da linha do dorso. | ok |
| 8. Cauda | Seção quase quadrada (largura = 1,15× a altura), afinando até uma ponta de 2 cubos. Laranja só embaixo da base. Manchas menores e separadas (lado: tamanhos medidos na ficha; de trás: central 4,4 × 5,2). | parcial: não deixei a largura igual à altura porque a ficha de trás mostra o oval largo (~11) |
| 9. Patas | Faixa única em degradê (sem a listra do meio), canela 1 mais fina, pé malva (110,92,104), dedos (191,169,179) com o do meio maior e dedo de trás. O braço da frente virou ombro + braço arredondados que afinam para baixo. | ok |
| 10. Asa | 5 penas pontudas em leque caindo para trás, de 32° a 64° abaixo da horizontal; as de baixo chegam ao meio do tronco. Amarelo só na ponta. 4 coberturas cinza-malva menores e sobrepostas, 2 com fenda em Y. | ok |
| Menores | 9 manchas por lado em 2 fileiras mais 2 no alto; fendas em Y também no topo do dorso, perto do ombro; íris (224,74,30) com brilho; sem friso amarelo; dedo do meio maior; penas carvão na juba. | ok |

### Conflitos entre as auditorias (decididos pela ficha)
- **Juba:** a 1ª pedia só a garganta; a 2ª, as costas do pescoço. A lateral da ficha mostra as penas descendo pelo pescoço até o ombro, então segui a 2ª.
- **Faixa da perna:** a 1ª pedia uma listra escura no meio; a 2ª, uma faixa só. A frente da ficha mostra uma faixa contínua, então segui a 2ª.
- **Escudo da barriga:** a 1ª pedia oval; a 2ª, largo em cima afinando para baixo. A frente da ficha é mais larga na parte de cima e no meio, então usei larguras 3,5 / 4,0 / 4,3 / 4,1 / 3,5 / 2,7.
- **Crista de frente:** mantive a cruz estreita, com a coluna e 2 lâminas laterais baixas, como a frente da ficha mostra.

## Fase 5: conferência pela arte conceitual (n41 → n47)

Modelo renderizado em yaw 55 e pitch -8, o ângulo mais próximo da arte, lado a lado e na mesma altura total: `revisao/n47_arte_lado.png` (e `n41_arte_lado.png`). Medidas em fração da altura total.

| Medida | Arte | n41 | n47 |
|---|---|---|---|
| Largura total do enquadramento | 1,05 | 1,14 | 1,12 |
| Crista (altura) | 0,17 | 0,20 | 0,165 |
| Cabeça (viseira → queixo) | 0,165 | 0,165 | 0,18 |
| Tronco (altura no meio) | 0,33 | 0,33 | 0,33 |
| Pata de trás → pata da frente | 0,36 | ~0,40 | 0,36 |
| Pernas visíveis (barriga → chão) | 0,22–0,26 | 0,26–0,28 | 0,26–0,28 |
| Braço da frente (espessura) | 0,12 | 0,14 | 0,12 |
| Canela (espessura) | 0,10 | 0,10 | 0,09 |
| Dedo maior (comprimento) | 0,10 | 0,14 | 0,11 |
| Asa (largura × altura) | 0,42 × 0,28 | 0,28 × 0,17 | 0,37 × 0,32 |
| Juba (largura × altura) | 0,34 × 0,39 | 0,37 × 0,39 | 0,37 × 0,37 |
| Gancho da cauda (largura × altura) | 0,45 × 0,53 | 0,49 × 0,55 | 0,46 × 0,55 |
| Cauda: espessura na base / no alto | 0,17 / 0,10 | 0,15 / 0,11 | 0,15 / 0,11 |

**Massa:** o tronco e a cauda grossa já batiam com a arte; o corpo não estava gordo. O que passava de 10%:
- **Asa pequena:** coberturas e penas de fogo maiores, com as penas mais deitadas para trás, sobre o flanco.
- **Crista alta:** lâminas ~15% mais curtas.
- **Tronco comprido atrás:** 2 unidades mais curto (patas de trás e cauda mais à frente); o lombo agora é mais alto no ombro e desce para o quadril.
- **Gancho da cauda largo:** base e ponta mais curtas.
- **Pernas:** braço e coxa um pouco mais finos, dedos ~20% mais curtos.
- **Juba:** penas 10% mais curtas.

## Fase 7: olhar imponente (n47 → n51)

Mudaram só os olhos e a viseira; o resto do modelo ficou igual.

- **Olho:** desenho próprio (`olho_imponente`): fenda alongada para trás, 2,4 × 1,5 de meio-tamanho (1,6 : 1). A borda de baixo é quase reta e sobe um pouco para trás.
- **Pálpebra pesada:** corta o topo em diagonal, descendo para o bico (fica à mostra ~60% do olho), com cílio escuro de 1 px no alto e sombra de 1 tom no alto da íris.
- **Íris e pupila:** íris laranja-vermelha forte (238,88,30), com anel escuro, ocupando quase todo o olho. A pupila fica perto da borda do lado do bico, com 1 px de brilho. A esclera só aparece numa cunha atrás.
- **Viseira:** mais pesada (de 29,0 a 31,6) e mais inclinada (18°), terminando no vértice sobre o bico.

# Taturico (#007): detalhes da ficha

Fontes: `007_taturico_ficha.png` (paleta), `_arte`, `_vistas`, `_detalhes` (Carapaça, Elmo Rochoso, Placas, Cauda Blindada,
Patas Fortes) e `_expressoes` (neutra). RGB amostrado com PIL nos PNGs da ficha (paleta: centro de cada quadrado).
Colunas: **n34** = fim da Fase 2; **n45** = depois da auditoria (`auditoria_n34.md`).

Decisão sobre o rosto (o recado do coordenador e a auditoria se contradiziam): medi a expressão neutra e as vistas.
- Em volta do olho a ficha é CREME, com só uma linha marrom na pálpebra de baixo. O escuro de frente é a sombra da aba.
- O bico de frente é um trapézio de ~1/3 da cara: ~5 u no topo, afinando para ~2,3 u, com ~5 u de altura. De lado tem ~5,6 u de comprimento.
- As barbelas são largas (~2,6 u), quase verticais e vão até ~y 15,5.
- O olho é redondo, com íris dourada.

Fiquei com a ficha (= auditor nesses pontos).

## Paleta (quadro "Paleta de Cores")
| # | Detalhe | RGB da ficha | n34 | n45 |
|---|---|---|---|---|
| 1 | creme | #fedfbd (254,223,189) | parcial (bochecha (252,210,172)) | ok #fcdfbe |
| 2 | laranja-tan | #ed9f5c (237,159,92) | parcial (células da grade, ruído) | ok #ed9f5e chapado |
| 3 | laranja-tan sombra | #cc733c (204,115,60) | parcial | ok #cd743e nas placas de baixo |
| 4 | marrom-malva | faixas #8f4f3f (143,79,63); quadro #9a4e28 | parcial (tons oliva / quase preto) | ok #8f4f3f |
| 5 | marrom-escuro | #5a2f29 / #572d27 | falta (pixels #301000) | ok: nada mais escuro que #572d27 |
| 6 | vermelho | #cf2423 (207,36,35) | ok | ok #cf2523 |
| 7 | amarelo | #fda901 (253,169,1); bico em cima #f7bc0a | parcial (pernas #c57a0b) | ok #fca702 / #f7bc0a |
| 8 | cinza-malva (garras) | #7f5e66 (127,94,102) | parcial (escuro, roxo) | ok #7f5e67 |

## Rosto (expressão neutra + frente e lado das vistas)
| # | Detalhe | Onde / forma / tamanho | Cor | n34 | n45 |
|---|---|---|---|---|---|
| 9 | olho: forma | redondo; o ar bravo vem só da aba | | falta (amendoado) | ok |
| 10 | olho: íris | dourada, ocupa a maior parte do olho | #f7bc0a | parcial (âmbar escuro) | ok |
| 11 | olho: pupila | preta, ~40% do olho, puxada para o bico | preto | ok | ok |
| 12 | olho: brilho | ponto branco no alto | branco | ok | ok |
| 13 | olho: esclera | clara, atrás da íris | creme-branco | ok | ok |
| 14 | pálpebra de baixo | linha fina marrom | #8f4f3f | falta (máscara escura) | ok |
| 15 | pele em volta do olho | creme | #fcdfbe | falta (marrom) | ok |
| 16 | sobrancelha brava | aba do elmo em V sobre o olho | marrom-malva + blocos laranja | parcial (tan demais) | ok (malva, 1 bloco laranja a cada 3) |
| 17 | bico de frente | trapézio, ~1/3 da cara, afina embaixo, logo abaixo da aba | #fca702 / laranja nos lados | falta (estreito) | ok (sup ±1,9 + flancos até ~±2,7, ponta ±1,5) |
| 18 | bico de lado | cunha comprida (~2x o olho), gancho para baixo | amarelo em cima, laranja embaixo | parcial (curto) | ok (z -16 a -21, gancho -16°, mandíbula de baixo laranja) |
| 19 | narina | quadradinho preto no alto, perto da base | preto | parcial | ok |
| 20 | barbelas | 2 placas largas quase verticais até o meio do peito; de lado, bloco robusto | #cf2523 | parcial (finas, em V) | ok (2,6 u de largura, 3 u de fundo, 8°, até y 15,4) |
| 21 | crista: lâminas | 3 de lado; cruz de 5 blocos de frente/trás | vermelho | ok | ok |
| 22 | crista: degraus inclinados para trás, mais altos | lado | vermelho | parcial | parcial (altura total limitada pela escala: a crista define o topo de 39,2 u) |

## Elmo Rochoso e placas da cabeça
| # | Detalhe | Onde / forma | Cor | n34 | n45 |
|---|---|---|---|---|---|
| 23 | elmo: cintas em arco | 3 cintas da testa à nuca, mesma regra da carapaça | malva/laranja | parcial | ok (cintas de placas curvas) |
| 24 | placas da cabeça: posição | da altura do olho até a base do bico, ladeando o rosto, salientes | marrom-malva | parcial (altas) | ok (y 20,8–27, x 7–11, à frente até z -14) |
| 25 | placa da cabeça: face da frente | meandro de ângulos retos | laranja sobre malva | parcial (G arredondado) | ok |
| 26 | placa da cabeça: face do lado | moldura laranja com fenda escura | laranja sobre malva | falta | ok |

## Corpo
| # | Detalhe | Onde / forma | Cor | n34 | n45 |
|---|---|---|---|---|---|
| 27 | carapaça: forma | 5–6 cintas curvas sobrepostas da nuca à cauda | | parcial (degraus retos) | ok (5 cintas em arco + garupa fechada) |
| 28 | carapaça: padrão | cada placa ~50% malva / ~50% laranja, xadrez regular de blocos grandes | #8f4f3f / #ed9f5e | falta (camuflado) | ok |
| 29 | traseira: forma | ovo / pinha: estreito em cima, largo no meio, fechando embaixo | | parcial (caixa) | parcial (o arco fecha embaixo; a ficha é mais estreita na base, vista um pouco de cima) |
| 30 | traseira: faixas | arcos empilhados, marrom em cima e laranja embaixo, na altura da ficha | | parcial | ok (faces de trás com as faixas da traseira da ficha) |
| 31 | placa do ombro | grande, meio do corpo | marrom-malva | ok | ok |
| 32 | emblema do ombro | moldura quadrada grossa (~1/8) + dente escuro em ∩ com o toco laranja do meio, só ângulos retos | #ed9f5e sobre #8f4f3f | parcial (arredondado, fino) | ok |
| 33 | asa na frente do ombro | desce reta, quase colada ao peito | malva/laranja | parcial (trapézio) | ok (blocos retos x 8,4–12,4; placa com o alto para dentro) |
| 34 | peito | creme quente em fileiras de escamas | #fcdfbe | parcial (bege acinzentado) | ok |
| 35 | saia de penas | penas-bloco verticais | creme | ok | ok |
| 36 | lascas / z-fighting na carapaça | não deve haver | | parcial | ok (pontas das placas vizinhas afastadas 0,03) |

## Cauda Blindada
| # | Detalhe | Onde / forma | Cor | n34 | n45 |
|---|---|---|---|---|---|
| 37 | cone de anéis | 4–5 anéis que diminuem, inclinado para baixo, ~30% mais longo | malva/laranja | parcial (toco de 3 anéis) | ok (5 anéis, 30°, ponta em y ~6) |
| 38 | ponta | ponta laranja afiada | #ed9f5e | parcial | ok (2 blocos que afinam) |

## Patas Fortes
| # | Detalhe | Onde / forma | Cor | n34 | n45 |
|---|---|---|---|---|---|
| 39 | perna | coluna curta e grossa | #fca702 | parcial (âmbar) | ok |
| 40 | dedos | 3 dedos amarelos para a frente | #fca702 | ok | ok (4 u) |
| 41 | garras da frente | garra cinza na ponta de cada dedo, ~metade do dedo | #7f5e67 | parcial | ok (2,3 u) |
| 42 | garra de trás | 1 bloco | #7f5e67 | ok | ok |

## Segunda auditoria (`auditoria2_n45.md`): estado na n53
Conflitos com a 1ª auditoria, resolvidos medindo a ficha:
- Olho: na neutra, a aba corta o terço de cima em linha inclinada (mais baixa do lado do bico); o resto é redondo, sem contorno fechado, com a íris âmbar quase cheia e uma cunha de esclera atrás.
- Pupila: na ficha é redonda, não vertical; mantive redonda.
- Carapaça: a ficha é voxel, com anéis em degrau.
  - Troquei as placas giradas por caixas sem giro, para a textura não esticar.
  - Pus uma aba de telha atrás de cada cinta, para o degrau aparecer no contorno.

| Item | n45 | n53 |
|---|---|---|
| olhos arregalados | falta | ok (meia-lua sob a aba, pálpebra #5a2f29, íris âmbar cheia) |
| cauda em leque | falta | ok (5 anéis sólidos telescópicos a 30° + ponta) |
| carapaça lisa/borrada | falta | ok (cintas em degrau com aba de telha, quadrados grandes) |
| bico em T | falta | ok (fatias que afinam + gancho + narina, amarelo uniforme) |
| elmo de uma faixa | falta | ok (aba em V sobre os olhos, 2ª fileira, topo e nuca em degrau, têmporas) |
| asas em laje | falta | ok (3 placas recuando para baixo, ombro chanfrado, base acima da coxa) |
| emblema invertido | falta | ok (borda marrom, anel tan, fundo marrom, toco tan; placa chanfrada) |
| barbela longa | parcial | ok (2 lóbulos largos que afinam, até y 17, + lóbulo do meio) |
| placas da bochecha | parcial | ok (giradas 35°, mais baixas, sobrepondo o rosto; placa com fenda na têmpora) |
| patas | parcial | ok (#fca702, sombra #e08a00 embaixo; garras 1,5x a altura do dedo) |
| menores | | ok: creme quente no rosto e no peito; peito em blocos arredondados; crista caindo sobre a aba; dorso mais alto atrás da cabeça; franja regular; close do rosto sem lâminas soltas |

## Fase 5: proporções pela arte conceitual (`007_taturico_arte.png`)
A arte foi comparada com o modelo renderizado em yaw 66° e pitch -10° (o ângulo mais próximo), na mesma altura total.
Os lados a lado estão em `revisao/<rodada>_arte_lado.png`, gerados por `revisao/estudo/arte_lado.py`.
As medidas são frações da altura total, medidas na imagem.

| Medida | Arte | n53 (antes) | n60 (depois) |
|---|---|---|---|
| comprimento total visível (ponta da cauda até o bico) | 0,87 | 1,10 (+26%) | 0,99 (+14%) |
| traseira: borda de trás da placa do ombro até a ponta da cauda | 0,25 | 0,36 (+44%) | 0,25–0,28 |
| cauda: comprimento visível / queda | ~0,22, desce até ~0,92 | ~0,30, horizontal-inclinada, ponta em 0,80 | ~0,22, desce a 50°, ponta em ~0,85 |
| crista: altura visível acima do elmo | 0,26 | 0,15 (-42%) | 0,22 (-15%) |
| crista: comprimento (frente-trás) | 0,34 | 0,45 (+32%) | 0,38 (+12%) |
| cabeça (topo do elmo até o queixo) | ~0,42 | ~0,41 | ~0,41 |
| bico: comprimento visível | 0,18 | 0,12 (-33%) | 0,16 (-11%) |
| pernas visíveis (barriga até o chão) | 0,24 | 0,24 | 0,24 |
| largura da perna | 0,13 | 0,14 | 0,14 |
| altura da carapaça (dorso até a barriga) | 0,56 | 0,61 (+9%) | 0,61 (+9%) |
| placa do ombro (largura x altura) | 0,26 x 0,26 | 0,31 x 0,28 | 0,28–0,30 x 0,28 (quadrada, 12,6 x 11,6 u) |

O que mudou:
- Cauda: voltou a ser curta e passou a descer a 50° a partir da garupa. Desfiz o alongamento de 30% da 2ª auditoria; a arte manda.
- Garupa e última cinta: recuadas 0,8 u.
- Cintas: sem a aba de telha. Na arte elas são rolos grossos, e as abas viravam lâminas finas.
- Crista: as lâminas descem até o elmo (mais alta visível) e ficaram mais curtas de frente para trás. O topo do elmo baixou 0,6 u.
- Bico: a frente creme do rosto recuou, e o bico aparece mais comprido (base junto do olho).
- Placa do ombro: quadrada e 1 u mais para a frente.

O que ficou: na arte o corpo continua ~14% mais curto no total. Pela vista lateral ortográfica da ficha, o comprimento bate (IoU 90%). A diferença que sobra parece ser a perspectiva da arte, e não mudei mais a massa para não sair das vistas.

## Fase 7: olhar imponente (n61–n63), só olhos e aba
- Olho: virou fenda alongada, 2,1 x 1,4 u (~1,5 : 1), puxada para o bico; a borda de baixo é quase reta e sobe para trás.
- Aba do elmo:
  - Mais inclinada (16° → 22°) e mais baixa no meio (24,7 → 24,4).
  - Corta o alto do olho numa diagonal que desce até a base do bico. Aparecem ~60% da altura do olho.
- Íris: dourada forte, com sombra da aba no alto.
- Pupila: preta, encostada no lado do bico, com 1 px de brilho.
- Esclera: só numa cunha atrás.
- Pálpebra: 1 px escuro só no alto; sem contorno em volta.
- Resto do modelo: sem mudança. IoU 88,6%; cor 48,8%.

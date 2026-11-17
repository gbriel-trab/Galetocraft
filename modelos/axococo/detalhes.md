# Axococó (#008): detalhes da ficha

Fontes: `_ficha`, `_arte`, `_vistas`, `_detalhes` e `_expressoes` (neutra). Os RGB foram amostrados nos PNGs com PIL,
pela mediana de 5x5 px. Coordenadas do modelo: y para cima, frente = -z, altura total ~39 unidades.

Status: **ok** / **parcial** / **falta**. A coluna "rodada" diz onde o status foi conferido.

## Paleta de cores (quadro "Paleta de Cores")
| # | Detalhe | Onde | Forma / tamanho | Cor da ficha | Status |
|---|---|---|---|---|---|
| 1 | Creme | peito, bochecha | – | (252,227,211) | ok (n21) |
| 2 | Rosa-claro | cabeça, asas, costas | – | (253,173,212) | ok (n21) |
| 3 | Rosa | brânquias | – | (252,103,137) | ok (n21) |
| 4 | Magenta | crista, pontas das brânquias | – | (251,60,125) | ok (n21) |
| 5 | Azul-céu | pontas da cauda | – | (90,189,249) | ok (n21) |
| 6 | Azul | espiral, meio da cauda | – | (40,99,182) | ok (n21) |
| 7 | Azul-royal | raiz da cauda | – | (0,58,161) | ok (n21) |
| 8 | Amarelo | bico, pernas | – | (252,175,3) | ok (n21) |

## Cabeça e rosto (`_expressoes` neutra + vista de frente)
| # | Detalhe | Onde | Forma / tamanho | Cor da ficha | Status |
|---|---|---|---|---|---|
| 9 | Cabeça em bloco grande | y 20,5–32, largura 16, fundura 11 | bloco com a testa chanfrada; frente reta | rosa (251,173,195) | parcial: a ficha põe o olho na face do lado e o mostra também de frente (perspectiva). No modelo o olho fica numa quina a 45° para aparecer nas duas vistas |
| 10 | Alto da cabeça mais claro | face de cima | – | (248,172,202) | ok |
| 11 | Testa / pálpebra em "V" | por cima dos olhos | aba rosa grossa que desce em diagonal para o bico (olhar bravo) | (246,175,208) | ok (n35: aba saliente, sem cobrir o olho) |
| 12 | Bochecha clara | embaixo do olho, até o bico | faixa de blocos quase brancos | (252,205,202)–(252,224,216) | ok (n21) |
| 13 | Olho: posição | na quina da frente, metade de lado e metade de frente | ~4,5 x 3, encostado no bico | – | ok (n28) |
| 14 | Olho: branco | dentro do aro | quase retangular | (250,242,240) | ok |
| 15 | Olho: pupila | encostada do lado do bico | redonda e grande, ~1/2 da altura do olho, inteira embaixo da pálpebra | preto (0,0,0) | ok (n29) |
| 16 | Olho: anel da íris | embaixo e na frente da pupila | meia-lua dourada | ~(204,150,30) | ok (n29) |
| 17 | Olho: brilho | alto da pupila, para o bico | 1 px branco | (255,255,255) | ok |
| 18 | Aro azul do olho | atrás e embaixo (grosso); em cima some sob a pálpebra | faixa em L | (35,130,224)/(59,127,207) | ok |
| 19 | Bico de frente | centro da cara, alto do bico na altura do meio do olho | cunha: larga em cima (~5), estreita embaixo (~2); ~4,5 de altura | amarelo (249,173,0) | ok (n21) |
| 20 | Bico de lado | sai da frente ~4,5 | cunha que afina; gancho leve na ponta | (252,166,2); sombra (213,136,29) | ok (n22: 3 degraus, sem gancho solto) |
| 21 | Narina | lado do bico, perto do alto | ponto escuro | (74,26,0) | ok (n21) |
| 22 | Barbela | embaixo do bico | 2 lóbulos separados por fresta, ~2,5 x 4, abrindo para fora | (238,48,66) / sombra (203,15,33) | ok (n24: 2,5 x 5,6, fresta de 1,6, abertura de 5°) |

## Crista ("Crista Aquática")
| # | Detalhe | Onde | Forma / tamanho | Cor da ficha | Status |
|---|---|---|---|---|---|
| 23 | Lâmina central | meio do alto da cabeça | coluna alta em degraus (topo y≈39) | (229,34,88) | ok |
| 24 | Lâminas laterais | dos dois lados da central | blocos mais baixos (topo y≈36) | (241,45,104) | ok |
| 25 | Lobo de trás | sobre a nuca | bloco que avança para trás | (211,25,73) | ok |
| 26 | Bloco da frente | sobre a testa | bloco baixo que desce sobre a testa (de frente a crista nasce logo acima do "V") | (229,34,88) | ok (n32) |
| 27 | Sombras da crista | faces de baixo e de trás | 2 tons | (188,16,61) | ok |

## Brânquias
| # | Detalhe | Onde | Forma / tamanho | Cor da ficha | Status |
|---|---|---|---|---|---|
| 28 | Número | lados da cabeça, atrás do olho | 3 de cada lado | – | ok |
| 29 | Ângulos | de frente: sobe ~26°, horizontal, desce ~26°; de lado: recuam ~55° e passam por cima das costas, como na arte | – | – | ok (n37: corrigido um erro que punha a raiz no meio da cabeça; as hastes furavam o olho) |
| 30 | Haste | cada brânquia, ~14 de comprimento | barra grossa que afina | rosa (252,120,161) / claro (255,152,183) | ok (n25) |
| 31 | Pente de cima | beirada de cima | blocos contínuos em escada, sem franja | (245,67,120)/(230,58,109) | ok (n25) |
| 32 | Pente de baixo | beirada de baixo | blocos rosa-claros contínuos | (255,152,183) | ok (n25) |
| 33 | Ponta | fim da brânquia | bloco magenta | (230,58,109) | ok |

## Corpo, peito e asas
| # | Detalhe | Onde | Forma / tamanho | Cor da ficha | Status |
|---|---|---|---|---|---|
| 34 | Corpo em ovo deitado | y 7–21, z −14 a +12 | – | rosa-claro (250,181,209) | ok |
| 35 | Peito em fileiras | frente, 5 fileiras | degraus em V, cada fileira avança sobre a de baixo, beirada de baixo em sombra | creme (252,215,200), sombra (246,189,178) | ok (n32) |
| 36 | Asa: coberteiras | lado, z −8 a +7 | fileiras de blocos sobrepostas, beirada de cima clara | (250,181,209), claro (253,219,234) | ok (n26) |
| 37 | Asa: rêmiges | atrás, pontas até z +14 | 4 fileiras com ponta em degrau | (250,181,209) | ok |
| 38 | Espiral ("Plumagem Úmida") | meio da asa | ~1,25 volta, larga, cauda que corre para a frente e sobe | azul (52,108,196), claro (80,132,214) | ok (n23: centro a 20,4–20,5 do bico; na ficha 19,8–21,2) |
| 39 | Azul da espiral visto de frente | beirada da asa | mancha azul pequena | (79,135,213) | ok |
| 40 | Costas | entre as asas | rosa-claro liso | (248,172,202) | ok |

## Cauda ("Cauda Regenerativa")
| # | Detalhe | Onde | Forma / tamanho | Cor da ficha | Status |
|---|---|---|---|---|---|
| 41 | Número de foices | atrás | 4 a 5 foices grossas | – | ok |
| 42 | Forma | arco para cima e para trás, com a ponta caindo | faixas de 5–6 | – | ok |
| 43 | Degradê | raiz → ponta | royal (0,58,161) → azul (56,130,245) → céu (69,173,239) | – | ok (n21) |
| 44 | Vista de trás | coluna azul centrada (~8) | (43,143,242) | parcial: n22 deixou a coluna simétrica (pares de foices). A ficha mostra a nuca acima da cauda (câmera um pouco de cima); na vista ortográfica a foice de cima cobre a nuca |

## Pernas e patas ("Patas Anfíbias")
| # | Detalhe | Onde | Forma / tamanho | Cor da ficha | Status |
|---|---|---|---|---|---|
| 45 | Perna | y 2–9,6, grossa (~5), amarela até o corpo | bloco | (238,142,10) / (247,152,4) | ok (n24) |
| 46 | Pé | almofada amarela larga | – | (232,163,20) | ok |
| 47 | Dedos da frente | 3, roxo-cinza, grossos | blocos | (71,53,77) / (104,81,103) | ok |
| 48 | Dedo de trás | 1 | bloco | (71,53,77) | ok |

## Resumo (rodada n37)
- 48 itens: 46 ok, 2 parciais (#9 e #44, motivos na tabela), 0 faltando.

## Correções da auditoria da n37 (rodadas n38–n46; final n46)
| # auditoria | Detalhe | O que foi feito | Status |
|---|---|---|---|
| 1 | Brânquias: desenho e cor | 1 fronde limpa por brânquia: haste em 3 degraus (2,9 → 2,4 → 1,9) com miolo rosa-claro (251,150,174), lado de baixo (251,106,137), 6 dentes de 1 bloco alternados em cima e embaixo, e ponta em (226,35,81). Sem bastões duplicados. | ok |
| 2 | Brânquias: número, posição e ângulo | 3 por lado, com a raiz na lateral da cabeça atrás do olho (y 29,6 / 26,8 / 24,6). De frente: +32°, −2°, −26°. De lado recuam 38–50°. A de baixo abre para fora antes de descer: não toca a asa (medido por `revisao/folga_guelra.py`). | ok |
| 3 | Cauda | Leque aberto sem gancho: as lâminas nascem a 50°, 22°, −8° e −34° da horizontal, com a ponta para trás e para fora. A de cima sobe até y≈28, acima do dorso. Lâminas largas (6,4 → 4,6). Degradê (24,64,160) → (46,112,200) → (90,176,240). | ok |
| 4 | Asa em gota | Coberteiras com a frente mais alta. 3 rêmiges em degrau (rosa-médio) descendo para trás até a base da cauda. Fileira de baixo em escada. Asa aberta 6° embaixo na vista de frente. | ok |
| 5 | Espiral | Quadrada ("e"/"@"), traço grosso (1,3), azul (44,113,202)/(58,131,228), ~40% do comprimento da asa. O rabo desce em degraus até a borda de baixo, e a ponta azul aparece na face da frente. | ok |
| 6 | Olho | Branco puro; pupila 1,55 x 2,2 encostada no lado do bico, com 1 px de brilho; íris âmbar só embaixo da pupila; moldura (53,139,225) retangular, fina em cima e na frente, grossa atrás e embaixo. | ok |
| 7 | Pálpebra | Aba rente (saliência 0,4), dentro da largura da cabeça, sem borda branca, com o lado de baixo rosa-médio. | ok |
| 8 | Bico | Cunha simples de 3 peças: trapézio de frente (5 em cima, 3,6 embaixo, altura total 3,7), ponta quadrada mais baixa de lado, narina na lateral. Amarelo (251,172,3) com o alto (253,201,42). | ok |
| 9 | Crista | Moicano: coluna central de 3,8 em 4 degraus (topo 38,8), laterais em 2/3 da altura, fim na nuca, base limpa (tirada a camada 'topo' que fazia plaquinhas). | ok |
| 10 | Pernas | Perna e pé no mesmo amarelo, com lado (240,150,4); perna mais grossa (6). | ok |
| – | Barbelas | Encurtadas para ~1,25x a altura do bico. | ok |
| – | Peito | A última fileira termina em ponta de "V"; separação sutil entre as fileiras. | ok |
| – | Bochecha | Clara logo embaixo do olho (y < 25). | ok |
| – | Dedo de trás | Bloco liso (sem faixas de luz). | ok |
| – | Cauda de trás | Par escuro nos "ombros", meio claro. | ok |

Onde a auditoria e a ficha divergem, segui a ficha:
- crista: (224,32,78)/(206,26,68), não #E8407A;
- bico e pernas: (251,172,3)/(249,159,2), quase sem azul, não #F5B830;
- rosa-médio da asa: (250,157,202), não #EE7FA0.

## Segunda auditoria, sobre a n46 (rodadas n47–n54; final n54)
| # | Detalhe | O que foi feito | Status |
|---|---|---|---|
| 1 | Brânquias felpudas | Cada brânquia é uma pena: haste rosa-claro (252,162,192) em 3 degraus e uma franja contínua de barbas de 2 de comprimento, dos dois lados, inclinadas 16° para a ponta. As barbas alternam (251,104,137) e (240,52,105), deslocadas em escada. Ponta rombuda em 2 degraus. Sem cubinhos soltos. | ok |
| 2 | Leque compacto | Raízes atrás da bochecha, da sobrancelha (28,4) ao canto do bico (23,8), quase encostadas. Ângulos +30°, +3° e −15°. A de baixo não toca a asa (folga +0,6, medida por `revisao/folga_guelra.py`). | ok |
| 3 | Espiral | Conflito entre as auditorias; medi no quadro "Plumagem Úmida" e segui a ficha: anel oitavado (cantos cortados em degrau, nenhum canto reto), traço grosso, barra interna até o miolo ("e"/"@"). A cauda sai do fundo, corre para a frente e para baixo e sobe na ponta. | ok |
| 4 | Bico | Uma maxila inclinada 13° (o alto em rampa, a ponta embaixo), a mandíbula mais estreita e uma ponta curta alinhada embaixo. De frente é um trapézio com a ponta no meio. Narina no alto, perto da base. | ok |
| 5 | Olho e sobrancelha | Sobrancelha pintada rente (capuz (226,96,138) que desce para o bico); a placa solta foi tirada. Sem fio claro nas emendas da cabeça. Olho menor; pupila grande encostada na pálpebra e no bico, com 1 px de brilho e o aro âmbar embaixo. | ok |
| 6 | Barbela | Dois lóbulos juntos (fresta de 0,5), com a borda de fora alinhada à do bico. Mais curtos (~3,7), com a ponta arredondada em degrau. | ok |
| 7 | Crista | Coroa de 3 colunas (laterais a ~80% da central), da testa (bloco que cai sobre ela) até a nuca, em 5 degraus. Cor (236,42,96). | ok |
| 8 | Asas | Ombro arredondado (volume na frente) e 3 camadas sobrepostas, cada uma mais comprida e com o fio rosa-escuro na ponta. A traseira afina em 2 pontas escalonadas. A asa inteira desce 7° para trás e abraça o corpo (ry 6°). | ok |
| 9 | Cauda | 5 lâminas largas e chatas (faixa 6,2, espessura 2,8), com as raízes sobrepostas. De trás formam uma coluna centrada sem vão. A de cima passa acima das costas. | ok |
| 10 | Pernas | ~60% da largura do pé (5 de 8,4), mais juntas ao centro. Dedos abertos em leque. | ok |
| – | Peito | Escamas inclinadas 12° (a beirada de baixo sai para a frente), em V até a ponta entre as pernas. Creme-pêssego (252,224,210). | ok |
| – | Pescoço | Primeira fileira do peito mais estreita que a cabeça. | ok |

Conflitos decididos pela ficha:
- **Espiral:** a ficha não é quadrada (pedido da 1ª auditoria) nem tem traço de 1 px (pedido da 2ª). É um anel oitavado em degraus, de traço grosso.
- **Coluna da cauda vista de trás:** a ficha mostra uma coluna mais larga que "estreita". Usei pares de lâminas a ±1,4, que formam uma coluna de ~5,6 sem vão.

## Fase 5: proporções pela ARTE CONCEITUAL (n54 → n59)
O lado a lado está em `revisao/n59_arte_lado.png`. O modelo foi renderizado a yaw 45°, pitch 0, na mesma altura total.
As medidas do modelo vêm de `revisao/medir_arte.py`; as da arte, da grade sobre `008_axococo_arte.png`.
Na arte a altura total (do topo da crista aos dedos) é de 763 px.
Os valores são frações da altura total; o "%" entre parênteses é o desvio em relação à arte.

| Parte | Arte | n54 (antes) | n59 (depois) |
|---|---|---|---|
| Tronco (peito + corpo + asa), largura | 69% | 77% (+12%) | 76% (+10%) |
| Tronco, altura | 35% | 38% (+9%) | 38% (+9%) |
| Asa do lado da câmera, comprimento | 47% | 40% (−15%) | 41% (−12%) |
| Asa, altura | 33% | 33% | 33% |
| Cabeça (sem crista), altura | 30% | 28% (−5%) | 30% (0%) |
| Crista acima do crânio | 14% | 19% (+33%) | 14% (0%) |
| Crista até a base do bloco da testa | 22% | 22% | 21% |
| Brânquias, altura do leque | 41% | 31% (−24%) | 37% (−10%) |
| Brânquias, largura | 69% | 65% | 69% |
| Cauda, largura | 43% | 51% (+18%) | 47% (+9%) |
| Cauda, altura | 62% | 67% (+8%) | 62% (0%) |
| Pernas (amarelo), altura | 20% | 19% | 20% |
| Pés + dedos, altura | 11% | 9% (−16%) | 11% (0%) |

A largura da cabeça não dá para comparar: na arte a cabeça está virada de perfil para a direita e o corpo a 3/4. Pelas vistas
ortográficas, a largura e a fundura da cabeça batem com a ficha.

## Auditoria 3, pela arte conceitual (n60–n67; final n66)
| # | Detalhe | O que foi feito (n66) | Status |
|---|---|---|---|
| 1 | Brânquias = penachos fofos | Haste rosa-claro (248,168,192) em 3 segmentos que afinam (3,2 → 2,8 → 2,4) e curvam a cada segmento. Filamentos grossos encostados uns nos outros em cima e embaixo, inclinados para fora e para a ponta, com degradê rosa-claro → magenta (224,48,106). Tufo magenta cheio na ponta. Sem serrilha. | ok |
| 2 | Leque e ponto de saída | Raízes mais baixas, entre o olho e a mandíbula (27,4 / 25,0 / 23,0). Leque aberto: de cima sobe, do meio quase horizontal, de baixo desce e abre para fora. A de baixo não encosta na asa: `revisao/folga_guelra.py` dá folga +0,85, mas compara só os cantos dos blocos. | ok |
| 3 | Corpo redondo | Corpo em sino: barriga larga embaixo e tronco mais estreito em cima, que vira pescoço creme afunilando até a mandíbula. | ok |
| 3 | Asa | Escudo oval de quinas bem cortadas, com a borda de cima subindo para trás. 3 primárias em escada (cada uma mais baixa e 2 mais curta) inclinadas 15° para baixo e para trás. Comprimento ~0,85 do corpo. Sem contornos escuros. | ok |
| 4 | Asas de frente | Coladas ao corpo e abrindo 4° embaixo; a massa mais larga fica na barriga. | parcial: de frente ainda aparece uma face lisa da asa |
| 5 | Peito | Telhas creme (248,228,216) desencontradas meia telha por fileira e em relevo alternado, com a borda de baixo (232,200,184). V até entre as pernas. De perfil estufa no meio-baixo. | ok |
| 6 | Bico | Cunha em 3 degraus (base 4x3, ponta 2x2, ~4 de comprimento) e mandíbula recuada. Uma narina em cada lado, perto da base. | ok |
| 7 | Olho | Esclera (255,248,240); pupila grande do lado do bico com crescente âmbar e brilho; azul só embaixo e atrás (em L). A pálpebra é o rosa da cabeça em diagonal, sem linha escura. | ok |
| 8 | Cauda | 6 foices largas e finas que curvam para trás e para baixo, ponta para baixo; a mais baixa chega ao joelho. Degradê (16,64,192) → (126,200,248), com a borda de fora clara. De trás, bloco de ~1/3 do corpo. | ok |
| 9 | Espiral | Quadrada, traço grosso, 2 voltas, miolo em gancho na frente e cauda longa por baixo que sobe em diagonal (arte). Azul (47,111,208), também no meio da face da frente da asa. | ok |
| 10 | Crista | Só no alto, em 3 lobos (o da frente pequeno, o do meio o mais alto, com degrau), descendo pela nuca. Nada na face. | ok |
| 10 | Barbela | Dois lobos de 2x2 por ~6 (~1,5x a altura do bico), um pouco afastados embaixo, com o lado de dentro mais escuro. | ok |
| – | Paleta | Cabeça rosa-chiclete (248,164,192); peito creme-pêssego; bico (248,176,0). | ok |
| – | Corte do rosto | O claro da bochecha desce em diagonal para trás, sem corte reto. | ok |

## Fase 7: olhar imponente (n67–n69; final n69). Só olho e pálpebra mudaram.
- **Fenda alongada:** ~1,7:1 (5,2 x ~3). A borda de baixo é quase reta e sobe de leve para trás.
- **Pálpebra pesada:** volume rosa (saliência 0,4) na mesma diagonal da linha da pálpebra (~17°, descendo até a base do bico); só ~60% do olho aparece. Tem um fio escuro de 1 px no alto do olho e a sombra dela escurece o topo da íris. O lado de baixo é rosa-escuro e não há fio claro na aresta.
- **Íris e pupila:** íris âmbar grande (244,178,40), na cor do crescente da ficha. Pupila preta grande perto do lado do bico, com 1 px de brilho no alto. A esclera aparece só numa cunha atrás.
- **Moldura azul:** só embaixo e atrás.

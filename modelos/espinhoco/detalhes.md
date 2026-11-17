# Espinhocó (#011): detalhes da ficha × modelo

Fontes: `011_espinhoco_ficha.png` (com a paleta), `_arte.png`, `_vistas.png`, os 5 quadros de `_detalhes.png` e a
expressão neutra de `_expressoes.png`. Os RGB foram amostrados com PIL nos PNGs (média 3x3 ou 5x5).
Status da rodada final **n34**, já com as correções da `auditoria_n27.md`.

## Paleta da ficha (amostrada nos quadrados de `Paleta de Cores`) × RGB da auditoria
| Cor | Ficha | Auditoria | Onde o modelo usa |
|---|---|---|---|
| creme | (253,226,185) | #FDE2B9 | peito, cara, ponta dos espinhos |
| bege | (230,159,92) | #E79E5C | meio dos espinhos, canela, dedos |
| marrom | (154,86,43) | #9D562C | cabeça, corpo, raiz dos espinhos |
| marrom escuro | (110,62,35) | #6E3E25 | dorso, penas de baixo das costas, saia |
| verde escuro | (101,126,13) | #647F0D | metade oliva das folhas |
| verde-lima | (146,170,7) | #8FA908 | metade limão das folhas |
| amarelo | (252,192,3) | #FDBE02 | bico de cima |
| vermelho | (224,26,27) | #E21719 | barbela |
| cinza | (79,63,61) | #50403F | garras |

Todos os RGB da auditoria batem com a paleta da ficha (diferença ≤ 5 por canal).

## Itens
| # | Detalhe | Onde | Forma, tamanho e cor da ficha | Status |
|---|---|---|---|---|
| 1 | Silhueta geral | 4 vistas | bola de espinhos atrás, ~41 de comprimento × 39 de altura; ~27 de largura de frente | ok (IoU 78,6%) |
| 2 | Cabeça | todas | bloco marrom largo (±5,4), à frente do peito | ok (avançada 0,6) |
| 3 | Mosaico da cabeça | lado | 3 marrons em blocos grandes: (146,92,62), (157,86,44), (128,74,40) | ok |
| 4 | Olho: formato | neutra | semicerrado, topo cortado reto pela sobrancelha, mais baixo do lado do bico ("D" deitado) | ok |
| 5 | Olho: esclera | neutra | creme-clara (253,235,205), só atrás da íris, sem anel embaixo | ok |
| 6 | Olho: íris | neutra | limão (~(226,228,30)) com crescente verde (44,120,16) embaixo da pupila | ok |
| 7 | Olho: pupila | neutra | preta, grande, encostada no lado do bico | ok |
| 8 | Olho: brilho | neutra | 1 ponto branco na pupila | ok |
| 9 | Pele em volta do olho | neutra | marrom-claro (146,92,62) em cima, creme embaixo | ok |
| 10 | Sobrancelha: forma | frente e neutra | laje grossa em V, dentro da largura da cabeça, até a base do bico | ok |
| 11 | Sobrancelha: cor | neutra | marrom-acinzentado (92,65,56) (#5C4138), face de cima mais clara | ok |
| 12 | Sobrancelha do lado oposto | 3/4 | só um tufo curto | ok (tufo de 1,25 × 1,2 × 1,8) |
| 13 | Bico de frente | frente | triângulo para baixo, ~1/4 da largura da cabeça, topo reto entre as sobrancelhas, ponta no topo da barbela | ok (5 camadas que estreitam: 2,8 → 0,5) |
| 14 | Bico de lado | lado e neutra | maciço, avança ~1/3 da cabeça (3,6), gancho 1,6 abaixo da mandíbula de cima | parcial: o gancho sai em degraus retos |
| 15 | Bico: cor | neutra | mandíbula de cima #FDBE02, laranja só embaixo | ok |
| 16 | Narina | neutra | quadradinho escuro no alto, perto da base | ok |
| 17 | Bico de baixo | neutra | amarelo-laranja #D08002, 1 bloco | ok |
| 18 | Barbela: forma | frente e lado | 2 lobos largos que se tocam sob o bico e abrem para baixo (Λ, 7°); de lado, bloco grosso (2 de espessura) | ok |
| 19 | Barbela: cor | todas | #E21719, faces internas mais escuras | ok |
| 20 | Bochechas creme | frente e lado | faixa creme contínua em blocos (#FDE2B9 / #FFD198) sob o olho, do bico ao meio da cabeça, sem cubos salientes | ok |
| 21 | Crista: número de lâminas | frente | 1 folha central alta e larga + 2 pares abrindo | ok |
| 22 | Crista: perfil | lado | folhas varrem para trás, da testa até a nuca, e se fundem com os espinhos | ok (inclinação de 18 a 68°) |
| 23 | Crista: desenho | `_detalhes` | folhas planas pontudas, iguais às da asa; a central é a maior | ok (a central é dobrada em X) |
| 24 | Topo da cabeça coberto | neutra | sem aba marrom | parcial: topo verde e folhas deitadas, mas ainda aparece uma faixa marrom fina atrás da sobrancelha |
| 25 | Folhas: forma | `_detalhes` Plumagem Folhosa | lanceoladas, ponta aguda | ok (losango extra na ponta) |
| 26 | Folhas: 2 tons | `_detalhes` | metade limão #8FA908 e metade oliva #647F0D pela nervura, sem contorno escuro | ok |
| 27 | Asa de folhas | lado | 9 folhas em leque saindo do ombro: em cima quase horizontais para trás, embaixo para baixo | ok |
| 28 | Folhas do ombro de frente | frente | descem ao lado do peito até y≈8 | ok (a ficha de frente manda: veja a nota 6) |
| 29 | Folhas da nuca | lado | fecham o vão entre a cabeça e os espinhos | ok |
| 30 | Espinhos: forma | `_detalhes` Espinhos | cones grossos, lisos, ponta aguda; ~20–25 de lado | parcial: 4 blocos que afinam devagar (não há como ser liso com cubos); são 19 no total |
| 31 | Espinhos: cores | arte | marrom #9D562C → caramelo #E79E5C → creme #FDE2B9, sem cinza | ok |
| 32 | Espinhos: todos com ponta creme | traseira | inclusive os de baixo | ok |
| 33 | Espinhos: traseira | traseira | cones individuais em fileiras radiais, fundo marrom-escuro entre eles, sem "X" | ok (giro variado por espinho) |
| 34 | Espinhos: comprimento | lado | até z≈+26 atrás e y≈36 em cima; os de baixo até o topo da perna | ok |
| 35 | Espinhos dos ombros | frente | só pontas curtas na altura do ombro, sem halo acima | ok |
| 36 | Cauda espinhosa | `_detalhes` Cauda Espinhosa | leque de espinhos atrás e embaixo | ok (osso `cauda`) |
| 37 | Flor Peitoral: forma | `_detalhes` | babador em V em fileiras que estreitam para baixo | ok |
| 38 | Flor Peitoral: blocos | `_detalhes` | blocos escalonados em 2 tons (creme + creme-caramelo), creme contínuo até a garganta | ok |
| 39 | Flor Peitoral: beirada | arte | bege #E79E5C | ok |
| 40 | Corpo marrom | vistas | #9D562C, penas grandes em escama | ok |
| 41 | Barriga em degraus | frente | borda de baixo em blocos de penas marrons | ok |
| 42 | Costas, 1/3 de baixo | traseira | penas marrons escalonadas (#9D562C / #6E3E25) até as coxas | ok (2 fileiras de 9 blocos) |
| 43 | Pernas: coxa | frente | bloco marrom grosso | ok |
| 44 | Pernas: canela | `_detalhes` Patas Firmes | laranja #E79E5C, mais grossa | ok (4,2 de largura) |
| 45 | Dedos | `_detalhes` | blocos laranja grossos | ok (1,7 × 1,8) |
| 46 | Garras | `_detalhes` | 4 por pé, cunhas cinza-escuro #50403F mais altas que o dedo, afinando para a frente e para baixo | ok |
| 47 | Pés de lado | lado | não muito longos | ok (encurtados ~1) |
| 48 | Paleta geral | todas | marrons da paleta, sem avermelhar nem acinzentar | ok |

**Total: 48 itens: 45 ok, 3 parciais (14, 24, 30), 0 faltando.**

## Motivo de cada parcial
- **14 (gancho do bico de lado):** com 5 camadas o gancho sai em degraus. A forma e a projeção estão certas.
- **24 (topo da cabeça):** as folhas cobrem o topo, mas uma faixa fina do crânio aparece atrás da sobrancelha.
- **30 (espinhos lisos):** feitos de cubos, os cones sempre mostram degraus. Os 4 blocos afinam devagar, sem
  serrilha e sem a ponta de agulha.

## Notas: onde a auditoria e a ficha divergem (a ficha manda)
- **Auditoria 6 (folhas até ~2/3 da altura):** na vista de FRENTE da ficha, as folhas do ombro descem até y≈8. As
  2 folhas da frente ficaram compridas; as de trás terminam mais alto, como na lateral.
- **Auditoria 10 (avançar a cabeça 1–2 blocos):** a silhueta lateral da ficha só comporta ~0,6. Com 1,2 (n28 a n31)
  sobrava azul na frente da cabeça e do bico.
- **Auditoria 5 (íris limão em cima, verde embaixo):** a ficha neutra mostra a íris quase toda limão e um crescente
  verde só sob a pupila, do lado do bico. Segui a ficha.
- **Cor/detalhe:** a nota caiu de 49,6% (n27) para 46,6% (n34). Com menos espinhos e mais grossos, a bola fica
  menos parecida, célula por célula, com a disposição de ~40 espinhos da ficha.

## Segunda auditoria (`auditoria2_n34.md`): rodada final **n42** (IoU 79,0%, cor 48,0%, 342 peças)
| Item | O que mudou |
|---|---|
| 1 Espinhos: forma | cone de 5 segmentos encaixados (cada um ~70% do anterior, ponta de 0,6), em ossos em cadeia com curva de 6° por segmento; sem placa nem moldura na ponta; o degrau não tem "prateleira" clara |
| 2 Espinhos: arranjo | ouriço radial: 3 anéis concêntricos + 1 central em volta do eixo das costas (25 cones, cada um apontando para fora do centro); de trás, roseta com marrom entre as bases; os de baixo e de trás descem até a coxa |
| 3 Espinhos: cor | rampa MEDIDA na lateral da ficha: (104,58,30) → (176,120,74) → (214,164,114) → (240,200,156) → (250,230,198); a ficha é mais saturada que os ≤35% da auditoria (segui a ficha) |
| 4 Capa de folhas | 6 folhas largas por lado (L ~12, W ~4,5, ~1/3), penduradas da base do pescoço em leque (de ~80° para trás a ~60° para baixo), sobrepostas e coladas ao corpo; a da frente encosta no peito |
| 5 Cor das folhas | lima com nervura clara de 1 px e 2 metades (luz/base), sem pixels quase pretos; tons medidos na ficha (r ≈ g, quase sem azul): luz (186,196,26), base (150,164,14), sombra (112,126,10), nervura (210,218,70) |
| 6 Bico | rapina: base 3,4 × 2,9, projeta 4, gancho na ponta descendo até o topo da barbela; de frente, alto largo + losango que fecha em ponta; mandíbula de baixo menor e recuada com linha de boca; narina na lateral, no alto (como na ficha neutra); amarelo-ouro sem contorno |
| 7 Crista | folhas largas lanceoladas (base estreita → corpo → estreita → ponta), da linha da sobrancelha: central alta, ±20°, ±40°, uma pequena junto de cada sobrancelha, 5 atrás até a nuca e 2 deitadas sobre o topo |
| 8 Barbela | dois lobos curtos (2,8 + ponta 1,0), largos, que nascem juntos sob o bico e abrem 12° (Λ), face interna (158,21,21) |
| 9 Bochechas e olho | 2 blocos creme salientes por lado (passam 0,4 da largura da cabeça e avançam à frente da cara); olho com íris lima viva, anel verde, pupila voltada para o bico com brilho e esclera só numa coluna atrás |
| 10 Corpo | tronco oval (cantos cortados em 2 degraus de 4,4/3,6); flanco coberto por 2 anéis de penas em escama com ponta em V (3 marrons da auditoria) e franja de trás; a "saia" de placas saiu |
| Menores | canela laranja-castanho (194,122,52) e coxa de penas; dedos grossos e garras grandes cinza-escuro; peito em camadas que avançam 1 a cada fileira, com borda de baixo em pontas, de gola a gola; sem "orelhas" de espinho de frente; sobrancelha vai do bico até a nuca |

## Fase 5: conferência pela arte conceitual (rodada final **n46**)
Comparação lado a lado em `revisao/n42_arte_lado.png` (antes) e `revisao/n46_arte_lado.png` (depois): modelo com
yaw 68° e pitch −6°, na mesma altura total da arte e com os pés alinhados. As medidas são frações da altura total
(H), lidas nas imagens; a precisão é de ~±0,01.

| Medida (÷ H) | Arte | n42 (antes) | n46 (depois) |
|---|---|---|---|
| Largura total no ângulo da arte | 0,94 | 1,04 (+10%) | 1,01 (+7%) |
| Profundidade do tronco (embaixo) | 0,65 | 0,70 | 0,70 (+8%) |
| Altura da cabeça (sem crista, até a bochecha) | 0,22 | 0,24 | 0,24 (+9%) |
| Altura da crista | 0,28 | 0,27 | 0,27 |
| Largura da crista (de perfil) | 0,40 | 0,37 (−8%) | 0,38 |
| Bola de espinhos: extensão horizontal | 0,53 | 0,55 | 0,52 |
| Bola de espinhos: extensão vertical | 0,77 | 0,74 | 0,72 (−6%) |
| Cone: comprimento visível | 0,23 | 0,28 (+22%) | 0,24 |
| Cone: largura da base | 0,075 | 0,045 (−40%) | 0,07 |
| Capa de folhas: altura | 0,36 | 0,44 (+22%) | 0,37 |
| Capa: comprimento da folha | 0,22 | 0,30 (+36%) | 0,25 (+14%) |
| Capa: largura da folha | 0,08 | 0,06 (−25%) | 0,075 |
| Pernas visíveis (barriga → sola) | 0,146 | 0,15 | 0,15 |
| Largura da canela | 0,11 | 0,10 | 0,10 (−9%) |

# Pirococó (#001): detalhes da ficha RoosterTeca × modelo novo (`ferramentas/especies/pirococo.py`)

Referência: SÓ a ficha RoosterTeca voxel (`001_pirococo_ficha`, `_vistas`, `_arte`, `_expressoes` neutra, `_detalhes`).
A arte pintada extra foi descartada pelo dono e não entrou no modelo.
Cores amostradas com PIL (média 5x5 ou 7x7 px). Status: ok / parcial / falta.

## Paleta (quadro "Paleta de Cores" da ficha, da esquerda para a direita)
| cor | RGB amostrado | uso no modelo (constante) |
|---|---|---|
| roxo escuro | (64, 28, 109) | `ROXO_ESC`: fundo das placas, sombra da armadura |
| roxo | (137, 83, 183) | `ROXO`: elmo, ombreiras, botas, borda do peitoral |
| lilás | (184, 142, 217) | `LILAS`: topo das placas, aba da bota, borda do V |
| branco | (239, 226, 223) / rosto na arte (252, 226, 196) | `CREME` (252, 228, 200): rosto e garganta |
| amarelo | (254, 197, 54) | `AMARELO_CLARO` / `OURO_CLARO` |
| laranja | (252, 113, 0) | `LARANJA` (245, 119, 7) |
| vermelho | (241, 14, 22) | `VERMELHO` (230, 17, 20) |
| vermelho escuro | (161, 3, 6) | `VERM_ESC` |
| âmbar | (252, 159, 2) | `OURO` (251, 173, 9), `BICO` (252, 168, 6) |

Outras amostras: bico na arte (252, 156, 1) e na neutra (253, 156, 1); gema da testa (239, 21, 28); ouro do elmo
(252, 198, 43) e (248, 178, 3); roxo das ombreiras (132, 78, 162); lilás (181, 128, 212); bota roxa (153, 88, 181) e lilás
(199, 149, 218); juba (250, 34, 19); laranja da capa (254, 120, 3); vermelho da capa (188, 5, 19).

## Lista de detalhes
| # | detalhe (onde) | forma / tamanho | cores | status |
|---|---|---|---|---|
| 1 | silhueta geral (vistas) | galo de briga em pé, peito para a frente, capa em sino, cauda e correntes atrás | — | ok (IoU ~67%, ver abaixo) |
| 2 | cabeça (arte, vistas) | caixa voxel com elmo-máscara; ~23% da altura sem os chifres | — | ok |
| 3 | rosto branco (neutra) | da frente do olho até a garganta | creme (252, 226, 196) | ok |
| 4 | olho (neutra) | grande, numa faceta diagonal: lê de frente e de lado | — | ok |
| 5 | íris | vermelha, grande, olhando para a frente | (236, 40, 34) → (150, 8, 18) | ok |
| 6 | pupila + brilho | pupila preta redonda, brilho branco no alto | preto / branco | ok |
| 7 | pálpebra / sombra da viseira | faixa preta no alto do olho, desce para o bico | preto | ok |
| 8 | viseira do elmo (sobrancelha) | barra roxa grossa por cima do olho, inclinada para o bico (cara brava) | roxo | ok |
| 9 | barra de trás do olho | barra roxa vertical do elmo até a bochecha | roxo | ok |
| 10 | placa lateral do elmo | lado da cabeça roxo atrás do olho | roxo / lilás em cima | ok |
| 11 | aleta do elmo | testada na p1–p13; vista de trás virava uma estaca roxa na nuca que a ficha não tem; tirada na p14 (o canto de trás do elmo já faz o papel) | roxo | ok (removida) |
| 12 | casca do elmo | alto da cabeça em 2 peças (topo + cúpula lilás) | roxo / lilás | ok |
| 13 | bico de lado | cunha grossa: base, meio e ponta caída (gancho) | amarelo (252, 168, 6), topo (255, 206, 76) | ok |
| 14 | bico de frente | mais largo em cima, ponta em V embaixo (cubo girado 45° na p15) | idem | parcial (ainda tem cara de caixa em degrau, mas já fecha em V) |
| 15 | narina e linha da boca | ponto e linha marrom no lado do bico | (120, 50, 10) | ok |
| 16 | mandíbula de baixo | menor e mais escura | (226, 120, 4) | ok |
| 17 | gema da testa | hexágono alto (pontas em cima e embaixo), ~3,2 x 6,0 | gema (239, 21, 28), facetas clara/escura | ok (brilha) |
| 18 | moldura de ouro da gema | borda grossa dourada | (252, 198, 43) / (248, 178, 3) | ok |
| 19 | chifres: contagem | a ficha (vista de frente e de trás) mostra 4 pontas douradas: 2 internas altas + 2 externas em U que saem da gema (quadro "Elmo da Fênix") | ouro | ok (4 pontas) |
| 20 | chifres internos | altos, varridos para trás ~45° (vista lateral) | ouro facetado | ok |
| 21 | chifres externos em U | saem do lado da gema, abrem e sobem | ouro facetado | ok |
| 22 | crista de chamas | lâminas vermelhas atrás da gema, entre os chifres | vermelho → amarelo | ok |
| 23 | juba de fogo (lado) | 4 penas largas por lado varridas para trás, a de cima subindo | vermelho escuro → laranja | ok |
| 24 | tufos da bochecha (frente) | penas vermelhas emoldurando o rosto | vermelho | ok |
| 25 | nuca (trás) | penas largas descendo pelas costas do pescoço (coluna vermelha da vista traseira) | vermelho | ok |
| 26 | garganta branca | faixa branca entre o queixo e o peitoral | creme | ok |
| 27 | peitoral: placa de cima | escudo roxo com borda grossa, campo vermelho | roxo (132, 78, 162), campo (230, 17, 20) → (161, 3, 6) | ok |
| 28 | emblema da fênix | asas em chama abertas para cima e para fora, corpo, cabeça pequena | amarelo (252, 178, 12), miolo laranja | ok |
| 29 | quilha do colar | pirâmide roxa no meio, em cima, apontando para baixo | roxo | ok |
| 30 | peitoral: placa de baixo em V | 2ª camada, borda lilás, cauda da fênix em chama descendo | lilás, amarelo/laranja sobre vermelho | ok |
| 31 | ombreiras facetadas | 2 fileiras de placas roxas grossas (3 + 3 por lado), abertas para fora | lilás / roxo / roxo escuro, aresta clara | ok |
| 32 | capa: 1ª fileira de penas (5 por lado) | penas roxo → magenta → vermelho (toque roxo do quadro "Capa de Asas") | (137, 83, 183) → (200, 40, 110) → vermelho | ok |
| 33 | capa: 2ª fileira (6 por lado) | vermelho → laranja → amarelo | | ok |
| 34 | capa: 3ª fileira comprida (7 por lado) | vermelho → laranja → amarelo, abre em sino e varre para trás | | ok |
| 35 | penas das costas | entre as asas, descendo até perto do chão | vermelho → amarelo | ok |
| 36 | plumas da cauda de fênix | 5 plumas grossas em foice (meio + 2 pares), vermelho na raiz e amarelo na ponta | | ok (pontas brilham) |
| 37 | correntes de contas: contagem | 3 correntes (vista traseira) | | ok |
| 38 | contas | blocos dourados grossos separados, ~2,3 | ouro (248, 178, 16) | ok |
| 39 | caminho das correntes | saem do alto da garupa, vão para trás e caem até perto do chão | | ok |
| 40 | pingentes | losango de ouro grosso com gema vermelha (em X, lê de todos os lados) | ouro / gema | ok (gema brilha) |
| 41 | coxas | penas vermelho-laranja grossas caindo sobre a aba da bota | vermelho → laranja | ok |
| 42 | botas roxas | cano roxo com linha em T na frente | roxo (153, 88, 181) | ok |
| 43 | aba da bota | anel lilás mais largo em cima | lilás (199, 149, 218) | ok |
| 44 | pés reforçados | base dourada + 3 dedos grossos para a frente + 1 atrás | amarelo (252, 178, 12) | ok |
| 45 | garras | ponta de cada dedo mais clara, caída | (255, 206, 76) | parcial (a ficha quase não mostra garras; a arte mostra dedos longos) |
| 46 | expressão | só a neutra | — | ok |
| 47 | brilho | gemas (testa e pingentes) e pontas das plumas na `_glowmask` | — | ok |

Resumo: 45 ok, 2 parcial, 0 falta.

## Proporções: arte × modelo (frações da altura total, render no ângulo da arte, `pK_arte_lado.png`)
| medida | arte | modelo (p17) | nota |
|---|---|---|---|
| cabeça (topo do elmo ao queixo) | 0,23 | 0,21 | a vista de frente da ficha dá 0,17; ficou no meio |
| chifres acima do elmo | 0,18 | 0,19 | ok |
| largura do peitoral | 0,23 | 0,24 | ok |
| pernas visíveis (fim da capa ao chão) | 0,15 | 0,13 | ok |
| largura total no ângulo da arte | 0,86 | 0,78 | as plumas da arte abrem mais; as vistas pedem plumas mais baixas |
| espessura das plumas grandes | 0,066 | 0,06 | ok |

Medidas no jogo (`dimensoes.py`, altura 2,80): largura 1,71 (alvo 2,00) e comprimento 2,47 (alvo 2,90). São guias:
a capa e a cauda mais largas e compridas descolavam da arte.

## IoU e cor (comparar_ficha)
| rodada | frente | lat. dir. | traseira | lat. esq. | média | cor média |
|---|---|---|---|---|---|---|
| p1 | 75 | 61 | 58 | 58 | 63,0 | 42,6 |
| p4 | 76 | 63 | 62 | 64 | 66,2 | 43,2 |
| p10 | 77 | 63 | 63 | 67 | 67,7 | 41,9 |
| p12 | 77 | 63 | 63 | 68 | 67,8 | 41,7 |
| p17 (final) | 77 | 61 | 62 | 66 | 66,5 | 41,6 |

Da p12 para a p17, as plumas subiram um pouco (para ficar entre a vista lateral e a arte), a aleta saiu e a capa
ficou com menos penas e mais largas (Fase 6). Isso custou ~1 ponto de IoU, de propósito.

As vistas laterais da ficha não são espelhadas entre si (são desenhos diferentes), por isso a lateral direita e a
esquerda dão IoU diferentes.

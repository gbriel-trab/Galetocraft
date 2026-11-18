# Guia de estilo dos Cocorídeos: o padrão Cobblemon

**Padrão visual vigente desde 18/11/2026**, pedido do dono: os galetos do Galetocraft seguem o estilo dos modelos do
Cobblemon, dentro do Minecraft. Vale para todo modelo novo e para toda refação.

De onde vêm as regras:
- medições em **78 modelos do Cobblemon 1.8.4**: uma amostra de 1 a cada 15 pastas da Pokédex, mais 20 aves e
  lutadores bípedes;
- os estudos `referencias/blaziken_cobblemon_engenharia_reversa.md` e `referencias/combusken_cobblemon_engenharia_reversa.md`.

Os números entre parênteses são medianas (com o intervalo p10–p90) desses 78 modelos.

Para conferir um modelo:
`python ferramentas/analisar_geo.py MODELO.geo.json TEXTURA.png --anim ANIM.animation.json --estilo`
A ferramenta compara o modelo com os 15 critérios da seção "Checklist". A amostra do Cobblemon atende 12 de 15 na
mediana (de 7 a 15), e o Blaziken atende 15 de 15.

Nada do Cobblemon é copiado: geometria, textura e animação deles são CC BY-NC 3.0 e os Pokémon são da Nintendo.
Copiamos **o jeito de fazer**, nunca as peças.

## 1. Os sete princípios
1. **O pixel é a unidade.** 1 unidade do modelo = 1 texel, com UV de caixa e tamanhos inteiros. O tamanho no jogo
   vem de uma escala única no renderizador.
2. **Poucas caixas grandes fazem a massa.** O detalhe vem da textura e de planos nas bordas, não de cubinhos.
3. **Planos (espessura 0) fazem as bordas:** franjas, pontas de pena, chamas, garras, unhas, sobrancelhas, olhos e
   cílios, sempre presos a uma caixa.
4. **Textura pequena e de paleta curta:** 20 a 50 cores, 3 a 5 tons por material, mosqueado leve e quase nenhuma
   luz pintada.
5. **Postura e vida ficam na animação.** O modelo é feito em pose neutra; quem dá atitude são o parado, o andar,
   o piscar, o olhar e o grito.
6. **Peças especiais ligam e desligam por escala 0:** fogo de batalha, asa aberta e asa fechada, pálpebra de dor.
7. **Variantes são baratas:** shiny troca só a cor, a fêmea é outro modelo com o mesmo esqueleto, e o que brilha
   vai numa camada à parte.

## 2. Grade e escala
- **UV de caixa (box UV) em 100% dos cubos**, sem UV por face (0 de 78 modelos usam). Assim todo pixel do
  modelo tem o mesmo tamanho, que é o que faz o modelo parecer do Minecraft.
- **Tamanhos inteiros** (0 fracionados na mediana). Posições e pivôs podem cair em 0,25 ou 0,5.
- **A escala vai no renderizador**, nunca na geometria. O Cobblemon usa `baseScale` (0,8; 0,6–1,03). No
  Galetocraft, a altura da tabela `ferramentas/dimensoes.py` vira uma escala do `GaloRenderer`. O modelo fica na
  grade, com cerca de 16 × altura ÷ escala unidades de altura.
  - **A fazer no código:** hoje `exportar_especie.py` multiplica a geometria por `k` (`converter(bbm, k)`), e é
    isso que gera os tamanhos fracionados.
- **Por que isso importa:** os Cocorídeos atuais têm 2 a 9 texels por unidade (Pirococó 3,5; Vagaló 8,8), com
  densidades diferentes no mesmo modelo. O pixel deles é 2 a 9 vezes menor que o de um mob do Minecraft. Isso dá
  cara de "textura HD colada em voxel", e não de Cobblemon.

## 3. Orçamento por altura no jogo
| altura no jogo | cubos (alvo / teto) | faces desenhadas (alvo / teto) | textura | cores (teto) |
|---|---|---|---|---|
| até 1 bloco | ~40 / 75 | ~160 / 270 | 64x64 | 35 |
| 1 a 2 blocos | ~70 / 110 | ~300 / 520 | 128x64 ou 128x128 | 40 |
| 2 a 3 blocos | ~100 / 145 | ~410 / 530 | 256x128 ou 256x256 | 55 |
| acima de 3 blocos | ~110 / 270 | ~450 / 600 | 256x256 | 64 |

- O Blaziken (2,9 blocos) usa 127 cubos, 470 faces, textura 256x128 e 33 cores. O Pirococó (2,8 blocos) usa
  404 cubos, 2.313 faces, 512x512 e 288 cores.
- A textura ocupa 35% a 70% da folha (52%). Sobra é normal; folha maior que a tabela não é.
- Com esse orçamento, o LOD do `GaloRenderer` deve deixar de ser necessário na maioria dos casos (conferir com
  `benchmark.sh`).

## 4. Geometria
### Massas
- Tronco, coxa, cabeça e asa são **caixas inteiras e grossas, alinhadas aos eixos**.
- Para inclinar uma peça, **gire o osso, não o cubo**. Só 5% dos cubos do Cobblemon são girados no próprio pivô
  (0–23%); nos Cocorídeos, 63% a 86%.
- As "facetas" ficam para o rosto e o bico. O Blaziken faz a cara em cunha com só 2 planos girados ±38,5°.
- Asa = **uma placa grossa (1 a 3 px) por segmento** + penas da borda em planos. Medido nas aves: 69% das peças de
  asa são planos e todas as "feathers" são planos, mas a base da asa é sempre uma placa com espessura (ex.:
  17x3x12, 12x2x10).
- Cauda e cabeleira: ~50% a 75% planos sobre um miolo de caixa.
- Nada de pilhas de cubinhos. Uma região tem poucos volumes grandes; a regra "sem entulho" do dono continua valendo.

### Planos (espessura 0)
- São 20% a 75% dos cubos (46%). Para galetos, que têm penas, mire em 35% a 60%.
- Usos: franjas e pontas de pena, chamas, garras, unhas, esporas, sobrancelhas, olho, pupila, pálpebra e brilho
  do olho, cristas finas, folhas.
- **Sempre presos a uma caixa** (franja de borda), nunca como a massa da pena grande. Mínimo de 2 px de largura,
  poucos e bem desenhados. Franja fina "pingando" continua proibida.
- Para ler de vários ângulos: leque de 2–3 planos a ±50–65° (chama do pulso do Blaziken) ou planos em X.

### Desempate e simetria
- `inflate` só para desempate de faces que se tocam: 0,01 a 0,05, no máximo 0,1. Nunca para dar volume.
- Camadas coladas (olho → pupila → brilho) ficam afastadas 0,01 a 0,02 entre si.
- Use `mirror` para o lado direito reaproveitar a UV do esquerdo.
- Planos podem ter UV negativa (v < 0) para a faixa vazia da caixa cair fora da folha.

### Pose de modelagem
- Modele em **pose neutra**: braços ou asas abertos, pernas retas e cabeça para a frente. Peças ficam alinhadas
  e a UV fica limpa.
- A postura (peito estufado, cabeça erguida, asas fechadas, dedos curvos) é dada pelo `parado`.
- Ossos sem cubo servem de articulação ou orientação extra (pulso, base da asa, "hairpos" do Blaziken).

### Rosto e olho
As regras do dono continuam valendo (rosto orgânico, Fase 7 "olhar imponente" do `ferramentas/especies/REFAZER.md`).
O jeito Cobblemon de fazer:
- olho num plano (ou num cubo raso) na face diagonal ou na quina da cabeça, para ser lido de frente e de lado;
- pupila e brilho em camadas 0,01 à frente;
- sobrancelha em plano (0x1xN) girado 30–40°, cortando o topo do olho em V, descendo para o bico;
- **pálpebra escondida**: uma cópia do olho 0,1 para dentro da cabeça. O `piscar` a empurra 0,1 para fora por
  ~0,17 s. Uma segunda pálpebra, com outro desenho, serve para dor e raiva.
- 65 de 80 modelos do Cobblemon têm pálpebra e 72 têm `blink`. Os Cocorídeos não têm nenhum dos dois.

### Asas abertas e fechadas
Quem voa ou abre as asas tem **dois conjuntos**: `asa_aberta_d/e` (`wing_open_*`) e `asa_fechada_d/e`
(`wing_closed_*`). Cada animação zera a escala do conjunto que não usa. 41 dos 80 modelos fazem isso. Assim a asa
fechada fica bonita colada ao corpo, sem esticar uma asa aberta.

### Pontos de referência (locators)
Ossos vazios marcam pontos para partículas, montaria e itens: olho, boca, topo, centro, pé e ponta da cauda (77 de
80 modelos). No Galetocraft: `ponto_olho_d/e`, `ponto_boca`, `ponto_assento` e `ponto_cauda`.

## 5. Textura
- **Tamanho:** veja a tabela da seção 3. Use potência de 2 e uma folha só por espécie.
- **Paleta curta:** 20 a 50 cores no total (28; 19–47), com 3 a 5 tons por material. Os Cocorídeos têm de 288 a
  8.645 cores.
- **Mosqueado leve:** dentro de um material, ~40% dos pares de pixels vizinhos têm cor diferente (0,32–0,54). A
  diferença entre eles é pequena, ~16 de luminância (6%). Isso é textura de pena ou escama, não ruído. Continua
  proibido o que o dono rejeitou: xadrez, pontilhado e listras finas de alto contraste. A maioria dos
  Cocorídeos fica abaixo de 0,08 (degradê liso), o que dá o ar de "plástico" ou "HD".
- **Luz pintada fraca:** o próprio Minecraft já escurece as faces de lado e de baixo. No Cobblemon, a tampa fica
  só ~5 mais clara que os lados e o fundo ~7 mais escuro (luminância 0–255). Os Cocorídeos pintam +17 e −21.
  Não há fio escuro de contorno nas bordas da face.
- **Padrões grandes e legíveis** (faixas, manchas, emblemas da ficha), desenhados na grade de 1 texel.
- **Shiny:** a mesma folha e a mesma UV, só com troca de cores. Toda a família usa a mesma paleta shiny
  (Combusken e Blaziken dividem os mesmos vermelhos-escuros). Fogo e partes que brilham não mudam.
- **Brilho:** uma camada separada só com os pixels que brilham (olhos, chamas, gemas). É o nosso `_glowmask`.
- **Variante:** a fêmea, ou outra forma, desenha suas peças numa região livre da mesma folha.

## 6. Esqueleto e nomes
Os nomes atuais que o exportador anima continuam (`ferramentas/especies/BRIEFING.md`): `corpo`, `pescoco`,
`cabeca`, `crista`, `perna_d/e`, `asa_d/e`, `cauda`, `<cadeia>_N`. Equivalentes no Cobblemon: body, neck, head,
leg_*, wing_*, tail#.

Ossos novos do padrão (**a implementar no exportador** antes do primeiro modelo que os use):

| osso | papel | Cobblemon |
|---|---|---|
| `<id>` (raiz) | raiz com o nome da espécie, pivô no chão | raiz = nome (79 de 80) |
| `olho_d/e`, `pupila_d/e` | olho em camadas | eye_*, pupil_* |
| `palpebra_d/e` (+ `palpebra_dor_d/e`) | piscar e expressão | eyelid_* |
| `bico_baixo` | abrir o bico no grito | jaw |
| `asa_aberta_d/e`, `asa_fechada_d/e` | troca por escala | wing_open_*, wing_closed_* |
| `pe_d/e` | pé separado da perna | foot_* |
| `fogo_*`, `efeito_*` | peças que ligam e desligam por escala | hand_fire_*, foot_fire_* |
| `ponto_*` | locators | locator_* |

## 7. Animação
Conjunto (frequência nos 80 modelos do Cobblemon):

| animação | Cobblemon | Galetocraft |
|---|---|---|
| `parado` (`ground_idle`) | 79 de 80 | **obrigatória** (já existe) |
| `piscar` (`blink`, quirk aleatória) | 72 | **obrigatória** (falta) |
| `andar` (`ground_walk`) ou andar procedural | 46 + procedurais | **obrigatória** (já existe) |
| `grito` (`cry`, com som) | 66 | recomendada |
| `dormir` (`sleep`) | 44 | recomendada |
| `batalha_parado`, `correr`, `recuo`, `desmaio` | 37 / 17 / 16 / 14 | quando houver combate |
| `ar_parado`, `voar` | 16 / 13 | para quem voa |

Técnicas:
- **Parado em Molang:** senoides `math.sin(q.anim_time*90*k)` (em graus; período = 4/k s). O loop dura o múltiplo
  comum dos períodos (o Blaziken usa 8 s). As cadeias usam fase em cascata, ~-30° por segmento (cauda, crista,
  penas), para o movimento "escorrer" até a ponta.
- **Andar:**
  - em keyframes `catmullrom` só nas pernas, com a direita igual à esquerda atrasada meio ciclo e espelhada;
  - o corpo vai em Molang: balanço em k e quique em 2k (um por pé);
  - ou procedural, preso à distância andada (`cos(limbSwing·p)·amount·a`), para o pé nunca escorregar. Hoje o
    andar do Galetocraft é um loop fixo de 0,8 s.
- **Olhar distribuído:** a cabeça gira mais e cintura, tronco e pescoço acompanham com pesos menores (no Blaziken,
  5/15/20/15/35). Penas soltas giram um pouco ao contrário, para parecer que têm peso.
- **Expressão por escala:** peito que estufa (1,2–1,5) e pupila que encolhe (0,7).
- **Efeitos ligados e desligados por escala 0:** fogo de batalha, asa aberta ou fechada.
- **Validar sempre:** os ossos animados existem e o Molang compila. Os dois erros que achamos no Cobblemon foram
  um osso `neck` inexistente e parênteses errados.

## 8. O que continua valendo das regras do dono
Tudo o que é de gosto e de fidelidade continua igual: `ferramentas/especies/BRIEFING.md`, `REFAZER.md`,
`REVISAO.md`, `AUDITORIA.md`, `JUIZ.md`.
- Fidelidade à ficha: silhueta, proporções, paleta, elementos característicos e arte conceitual (`REFAZER.md`,
  início e Fases 2 e 5).
- Rosto e bico orgânicos, nada de rosto disforme; olhar imponente com pálpebra pesada (Fase 7).
- Modelo limpo, sem entulho; poucas peças e maiores (Fase 6).
- Só a expressão neutra no modelo. Revisão por juiz, auditoria, IoU e cor (`comparar_ficha.py`).
- `_glowmask` para o que brilha. Frente em -z; lado direito em -x.

## 9. O que muda em relação às regras antigas
| regra antiga | regra nova | por quê |
|---|---|---|
| até ~350 peças, textura até 512x1024 (`BRIEFING.md`) | orçamento da seção 3 (ex.: ~100 cubos, ≤530 faces, 256x128 para 2–3 blocos) | medido no Cobblemon; os Cocorídeos usam 2 a 7 vezes mais faces que o alvo |
| UV por face e escala aplicada na geometria | UV de caixa, tamanhos inteiros, escala no renderizador | pixel único = cara de Minecraft |
| volumes arredondados com `arredondado` e `octogono` (Fase 6) | caixas inteiras; inclinação no osso; facetas só no rosto e no bico | Cobblemon gira 5% dos cubos; os Cocorídeos, ~70% |
| "pinte a luz em 3D, é o acabamento Cobblemon" (`BRIEFING.md`) | luz pintada fraca (≤16 de luminância) | o Cobblemon quase não pinta luz; quem sombreia é o jogo |
| 2–3 tons chapados por bloco, sem ruído (início do `REFAZER.md`) | 3–5 tons com mosqueado leve (~6% de contraste); padrões de alto contraste seguem proibidos | é o que dá a textura "de pena" do Cobblemon |
| placas finas só para membrana, chama e pétala (início do `REFAZER.md`) | massa sempre em caixa grossa; planos liberados para franjas, pontas, garras, olhos e sobrancelhas, presos a uma caixa | 46% das peças do Cobblemon são planos, quase todos de borda |

**Confirmar com o dono:** as três últimas linhas mudam pedidos explícitos dele (início e Fase 6 do `REFAZER.md`). Este guia segue o
Cobblemon, mas mantém o motivo de cada pedido: nada de "papel", "fumaça" nem "quadradão".

## 10. Checklist (o que `--estilo` confere)
1. UV de caixa em 100% dos cubos.
2. Nenhum tamanho fracionado.
3. Cubos dentro do teto da altura.
4. Faces dentro do teto da altura.
5. Textura no tamanho da tabela.
6. Cores dentro do teto.
7. Planos entre 20% e 75% (galetos: 35% a 60%).
8. No máximo 23% de cubos girados no próprio pivô.
9. Inflate de no máximo 0,1.
10. Mosqueado entre 0,25 e 0,65.
11. Luz pintada de no máximo 16.
12. Osso de pálpebra.
13. Animações obrigatórias: parado, andar e piscar.
14. Animações recomendadas: grito e dormir.
15. Todo osso animado existe no modelo.

E, fora da ferramenta: a ficha (IoU, cor e auditoria de detalhes), o olhar imponente e o modelo limpo.

## 11. Situação em 18/11/2026
| espécie | altura | cubos | faces | textura | cores | planos | cubos girados | critérios |
|---|---|---|---|---|---|---|---|---|
| Axococó | 1,15 | 221 | 1.233 | 512x512 | 334 | 0% | 71% | 2/15 |
| Cocórak | 3,00 | 294 | 1.394 | 512x1024 | 8.645 | 0% | 69% | 3/15 |
| Cocórion | 2,40 | 288 | 1.643 | 512x512 | 2.602 | 0% | 72% | 2/15 |
| Cocórvolt | 2,60 | 222 | 1.232 | 512x1024 | 735 | 0% | 63% | 2/15 |
| Espinhocó | 1,25 | 348 | 1.942 | 512x512 | 512 | 0% | 86% | 2/15 |
| Esporocó | 1,75 | 345 | 1.890 | 512x512 | 790 | 0% | 80% | 2/15 |
| Morcegalo | 1,20 | 322 | 1.825 | 512x256 | 364 | 0% | 80% | 2/15 |
| Pirococó | 2,80 | 404 | 2.313 | 512x512 | 288 | 0% | 72% | 2/15 |
| Renacocó | 2,50 | 480 | 2.744 | 512x512 | 3.389 | 0% | 77% | 2/15 |
| Salambrasa | 1,10 | 269 | 1.547 | 512x512 | 669 | 0% | 63% | 2/15 |
| Taturico | 1,20 | 120 | 687 | 512x512 | 450 | 0% | 13% | 4/15 |
| Vagaló | 1,00 | 239 | 1.309 | 512x512 | 6.191 | 0% | 67% | 2/15 |

Nenhum modelo atual segue o padrão; todos precisam ser refeitos nele. O caminho sugerido:
1. passar a escala para o renderizador e gerar UV de caixa em `galo_base.py` e `exportar_especie.py`;
2. refazer uma espécie piloto (o Pirococó, que é o mais próximo do Blaziken) e levá-la ao dono;
3. só então seguir para as outras.

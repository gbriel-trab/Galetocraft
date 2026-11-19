## Ficha da criatura — Pirococó (#001), "O Galo Fênix"

> **Se esta conversa já tem um modelo anterior do Pirococó, descarte-o.** Este pedido é uma **reconstrução do zero**
> com a técnica "massa sólida + franja" (seção B3). Não reaproveite a construção antiga (capa de planos soltos,
> crista em raios); só utilitários (UV, validações).

**Quem é:** um mítico do tipo fogo. É uma ave de rapina nobre e imponente, com cerca de 5 cabeças de altura (não é
filhote nem chibi), e usa armadura prateada de cavaleiro. Os elementos que o identificam de longe:

- **Juba de penas vermelhas** em chama, em volta de um rosto pequeno e afiado.
- **Elmo-tiara prateado** com gema rubi na testa.
- **Colar em V prateado** com gema no peito.
- **Ombreiras em concha** que abrem para cima, com ponta dourada.
- **Capa-asa de penas em triângulo:** roxa (com filetes prata) em cima, vermelha embaixo. Ela emoldura o peito creme
  e abre em sino.
- **Pernas longas e finas** com joelheira e tornozeleira prateadas.
- **Garras douradas.**
- **3 tranças douradas** que descem **retas** pelas costas da capa, cada uma terminando numa pena-lâmina dourada com
  losango rubi.

**Expressão:** a neutra da ficha ("NORMAL"), séria e determinada.

### Escala e orçamento

| item | valor |
|---|---|
| altura total (chão → ponta da crista) | **45 u** (2,8 blocos) |
| largura máxima (capa, na frente) | ~29 u |
| cubos | **110–170** (a construção abaixo dá ~120); planos ≤ ~35% |
| textura | 256×128 (no máximo 256×256), 1 px por u |

### Marcos de altura (y a partir do chão)

| marco | y (u) |
|---|---|
| crista acima do elmo | 39 → 45 |
| cabeça (topo do elmo → queixo) | 31 → 39; olhos em 35; bico de 34 a 30,5 |
| colar e topo das ombreiras | 28–29,5 |
| gema do peito | 22 → 27; ponta do V do colar em ~21,5 |
| tronco | 15 → 28 |
| coxas | 10,5 → 15 |
| joelheira | 8,5 → 10,5 |
| canela | 5,5 → 8,5 |
| tornozeleira | 3,5 → 5,5 |
| pé + garras | 3 → 0 |
| barra da capa | ~2 (não encosta no chão) |

### Construção por região

Coordenadas do `.geo.json`: x negativo = lado direito, frente em z negativo, y para cima, chão em y = 0. Os sinais
de rotação seguem a seção C1 (s = sinal de x do lado). A tabela dá o ponto de partida: renderize e ajuste até a
silhueta bater com a ficha.

**Resultado esperado da construção:**

- altura de 0 a ~45 u e largura de ~30–32 u;
- ~120 cubos, ~34% de planos;
- passa no teste "sem planos": a capa, as ombreiras, a juba e a cauda continuam como volumes.

| região | construa assim (tamanho, posição e giro em u e graus) | pintura e acabamento |
|---|---|---|
| tronco | 2 caixas sobrepostas: 10×13×10 (x −5..5, y 15..28, z −7..3) + 8×11×12 (x −4..4, y 16..27, z −8..4) | frente com um V creme claro que afina para baixo; resto vermelho em faixas |
| peito | bloco creme 8×8×3 saltado (x −4..4, y 19..27, z −10..−7, o "peito de pombo") + 6×4×2 abaixo (x −3..3, y 15..19, z −9..−7) + plano creme 6×3 recortado em 3 pontas (y 12..15, z −8,5, base 10° para trás) | chevrons em zigue-zague de 1 px (#d9b398), luz no topo, quinas com 1 px de sombra |
| pescoço | caixa 6×5×6 (x −3..3, y 27..32, z −7..−1) | frente creme e nuca vermelha; faixa de sombra sob o queixo |
| cabeça | caixa 8×8×7 (x −4..4, y 31..39, z −7..0) + tampa 6×1×5 (y 39..40, z −6..−1) + nuca 6×6×1 (y 32..38, z 0..1): o contorno fica chanfrado | rosto: creme embaixo (garganta e bochecha); marcas de pena de 1 px nas laterais; topo escuro sob a juba |
| bico | base 3×3×2 (x −1,5..1,5, y 31,5..34,5, z −9..−7) + meio 2×2×2 (y 31,5..33,5, z −10,5..−8,5) + gancho 2×2×1 caído (y 30,5..32,5, z −11..−10) | topo #ffe138, lados #fcb419, gancho e base de baixo #d87b08; 1 px de narina |
| olhos | cubos "de quina" 2×1×2 com `inflate` 0,02 (x −4..−2 e 2..4, y 34,5..35,5, z −7..−5): o olho aparece de frente e de lado. Viseira prata 3×1×3 sobre cada olho (y 35,4..36,4), com a ponta de dentro mais baixa: z = −18 × s | 1 px #fff6e0 + 1 px de íris #9e1020. Pálpebras `palpebra_d`/`palpebra_e`: cubo igual, vermelho, `inflate` 0,01, para piscar |
| elmo | casca prata 9×2×8 em volta da cabeça (x −4,5..4,5, y 36..38, z −7,5..0,5), com a traseira mais alta (x = +12°, pivô na frente, em (0, 37, −7,5)) + gema 2×4×1 na testa (y 35..39, z −8,2..−7,2) | chanfro pintado (1 px #f6f6f6 em cima, #ac93ae embaixo); gema em losango com 3 facetas; 2 aletas planas de 3×4 saindo para trás, de dentro da juba |
| juba | **massa sólida:** bloco 8×2×8 em cima da cabeça (x −4..4, y 38..40, z −6..2) + bloco 6×4×6 atrás (x −3..3, y 35,5..39,5, z −1..5), varrendo para trás e para cima (x = +12°, pivô (0, 38, −1)). **Franja de planos largos:** 2 penas em U de 5×8 viradas para a frente (centro em x ±3, base em y 37,5, z −4,5; z = +8 × s, x = −8°), formando a lira; pena central de 5×5 (base em y 38, z −4, x = −15°); 3 chamas de 5×8 por lado (base em y 37, em x ±3,5/±4,5/±5,5 e z −3/−2/−1; z = +14, +26 e +38 × s; x = −20°); 4 lâminas de nuca, planos verticais ao longo de z de 5×11 (x −2,5/0/+2,5/0, de z 1 a 12), com a ponta de trás subindo (x = +16°, +24°, +6° e −6°); 1 tufo de bochecha 3×5 por lado (x ±4,2, y 31..36, z −3,5; z = +115 × s) | cada chama com raiz escura, haste clara e ponta curva na luz; lâminas da nuca com a ponta afinando para trás; mechas de 1 px nos blocos; ponta mais alta em y ≤ 45,5 |
| ombreiras | por lado: concha prata 6×4×8 (x 4..10 / −10..−4, y 25..29, z −5..3) + tampa roxa 5×1×7 em cima + ponta dourada 3×1×5 na borda de fora. A concha e a tampa abrem com a borda de fora SUBINDO: z = −20 × s, pivô (±4,5, 28, −1). A ponta abre z = −40 × s | losango roxo pintado na tampa; borda prata chanfrada; dourado só na ponta |
| colar + gema | V de 2 placas prata 5×2×1 (x −6..−1 e 1..6, y 21,5..23,5, z −10,6..−9,6), com as pontas de fora mais altas (z = −32 × s, pivô (0, 22, −10,1)) + faixa 10×2×3 (x −5..5, y 26..28, z −9,6..−6,6) + gema 3×5×1 (x −1,5..1,5, y 22..27, z −11,1..−10,1) | chanfro pintado; gema com facetas, no osso `gema_peito_brilho` |
| asas-capa (`asa_d`/`asa_e`) | **3 placas sólidas por lado**, como a asa fechada do Talonflame. Veja a tabela abaixo | penas de 5 px em 2 fileiras por placa (seção B6); filete prata em penas alternadas nas roxas; vermelhas com pontas claras |
| costas da capa (`capa_costas`) | 3 placas sólidas em leque: 12×13×2 (y 15..28, z 3..5), 18×13×2 (y 8..21, z 4,5..6,5) e 22×10×2 (y 3..13, z 6..8), centradas em x 0. Cada uma recua com x = +8°, +14° e +18°, com pivô no meio da borda de cima. Embaixo de cada placa, 1 plano de franja de 4 u recortado em pontas | mesma pintura das asas; pena central marcada (o "eixo" do leque da ficha TRÁS) |
| cauda | fecho prata 7×3×1 nas costas (x −3,5..3,5, y 24..27, z 5,2..6,2). 3 tranças em x 0 e ±3, com segmentos 2×3×2 encadeados (a central com 5, as laterais com 3, cada um num osso). O 1º segmento é girado x = +17°: a trança desce **reta**, encostada por fora da capa e acompanhando a inclinação dela. As laterais abrem z = −5 × s. Na ponta, lâmina de 2 planos em X (5×8 na central, 4×7 nas laterais) com losango 2×3. As pontas ficam em y ≈ 2 (central) e ≈ 8 (laterais) | trança pintada em gomos diagonais (`<<<`, 3 tons de dourado); lâmina em forma de chama apontando para baixo; **nenhuma curva** |
| pernas | por lado, com centro em x ±2,6: coxa vermelha 4×5×5 (y 10,5..15,5) + franja 4×3 na frente; joelheira 3×2×3 (y 8,5..10,5) + espora triangular 3×4 na frente, inclinada 15° para a frente; canela roxa 2×3×2 (y 5,5..8,5); tornozeleira 3×2×3 (y 3,5..5,5) + ponta triangular 3×2 para baixo | penas pintadas na coxa; chanfro nas peças prata |
| pés | pé 3×2×4 roxo-escuro (y 1..3, z −3..1). 3 dedos 1×1×3 (z −6..−3), cada um num osso girado y = −28°, 0° e +28° em volta de (x, 1, −3). Garra dourada 1×1×2 na ponta de cada dedo (y 0,6..1,6, z −7,5..−5,5), caída: x = +20°, pivô na base da garra. Dedo de trás 1×1×2 + garra 1×1×1 | escamas de 1 px nos dedos; garra com a ponta clara |

**As placas das asas-capa:**

- Cada placa tem o pivô no meio da sua borda de cima, em (±5, topo da placa, meio da profundidade).
- As rotações são: z = −abre × s (a ponta de baixo se afasta do corpo), x = +recua (vai para trás) e y = −gira × s
  (a borda da frente vem para dentro e cobre o flanco).
- Embaixo de cada placa vai 1 plano de franja de 4 u de altura, colado na face de fora, com a mesma rotação e
  recortado em pontas.

| placa | tamanho (espessura × altura × profundidade) | posição | abre | recua | gira |
|---|---|---|---|---|---|
| 1 (roxa) | 3×13×10 | x ±(5..8), y 15..28, z −6..4 | 20° | 6° | 14° |
| 2 (roxo → vermelho) | 3×13×12 | x ±(6..9), y 8..21, z −5..7 | 23° | 12° | 8° |
| 3 (vermelha) | 2×11×13 | x ±(7..9), y 2..13, z −3..10 | 24° | 16° | 3° |

Acrescente 2–3 planos de pena de 4×8 por lado, saindo da borda de trás da placa 3 e apontando para trás e para
baixo: de lado, a capa precisa mostrar pontas como na ficha DIREITA.

**Atenção:**

- As penas em U da crista são **vermelhas**. Não há chifres dourados.
- A armadura é **prateada** (com um leve tom lilás).
- O dourado aparece só no bico, nas garras, nas tranças, nas lâminas da cauda, nas pontas das ombreiras e no fecho.

### Ossos e animação

**Ossos:**

- **Raiz:** `pirococo`.
- **`corpo`:** pescoco → cabeca → crista; gema_peito_brilho; ombreira_d e ombreira_e; asa_d e asa_e; capa_costas;
  cauda.
- **`cauda`:** cauda_a_0..4, cauda_b_0..2 e cauda_c_0..2, encadeados; cada um termina em lamina_a/b/c, com
  losango_a/b/c_brilho.
- **Pernas:** perna_d e perna_e, filhas da raiz, com dedo_d_0..2 e dedo_e_0..2.
- **Pálpebras:** `palpebra_d` e `palpebra_e` (filhas de cabeca).

**idle (L = 4):**

- **Corpo:** respira com ±1,5° em x e sobe e desce 0,2 u.
- **Cabeça:** ±2° em x e ±3° em y, defasada do corpo.
- **Crista:** ±3°, atrasada da cabeça.
- **Asas-capa:** ±2° em z, espelhadas entre os lados.
- **Tranças:** pêndulo pequeno, ±3° em z no 1º segmento e ±1,5° nos seguintes, com atraso de −30° por segmento; as
  laterais em fase oposta.
- **Piscar:** 1 vez no fim do laço.

**walk (L = 2):**

- **Pernas:** ±25° alternadas.
- **Corpo:** sobe e desce 0,4 u, 2 vezes por ciclo, e balança ±3° em z.
- **Cabeça:** mais estável que o corpo.
- **Capa:** com atraso.
- **Tranças:** ±6° em z e ±3° em x, defasadas.

**Brilho:** só as gemas e os losangos (ossos `_brilho`).

### Paleta (da ficha) e rampas sugeridas (luz → sombra funda)

| material | luz | claro | **base** | sombra | sombra funda |
|---|---|---|---|---|---|
| vermelho (crista, plumagem, coxas, barra da capa) | #ff5b3f | #ef392d | **#dd1c20** | #b90c27 | #960429 |
| creme (rosto, garganta, peito) | #fff6e0 | #ffeed1 | **#fde1c0** | #d9b398 | #b68b78 |
| roxo (capa de cima, canelas) | #a0499e | #88398e | **#702a7c** | #491847 | #300e34 |
| roxo-escuro (pés, sombras) | #5b2354 | #491847 | **#3a1239** | #2c0c2e | #210826 |
| prata (armadura) | #f6f6f6 | #e4dce3 | **#d2bed1** | #ac93ae | #86708b |
| dourado (bico, garras, tranças) | #ffe138 | #ffcd29 | **#fcb419** | #d87b08 | #b55100 |
| rubi (gemas, losangos) | #da3879 | #c82775 | **#b61972** | #920b6a | #6f0459 |
| olho (íris) | — | #e8352b | **#9e1020** | #5a0812 | — |

### Pontos de reprovação específicos desta criatura

- **Construção:**
  - capa ou crista feitas de planos soltos ("vassoura", "sol", cortina);
  - qualquer coisa que falhe no teste "sem planos".
- **Cabeça:** grande demais (fofa) ou rosto genérico de galinha. É uma ave de rapina séria.
- **Pernas:** grossas ou curtas (a perna visível tem 10,5 u).
- **Capa:**
  - escondendo o peito creme;
  - ou, ao contrário, ausente nos flancos ("caixote" vermelho).
- **Tranças:**
  - fundidas numa peça só, com curva, encostando no chão ou penduradas entre as pernas;
  - pintadas em xadrez.
- **Pés:** gigantes ou em barra.

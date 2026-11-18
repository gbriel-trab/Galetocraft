## Ficha da criatura — Pirococó (#001), "O Galo Fênix"

**Quem é:** um mítico do tipo fogo. É uma ave de rapina nobre e imponente, com cerca de 5 cabeças de altura (não é
filhote nem chibi), e usa armadura prateada de cavaleiro. Os elementos que o identificam de longe:

- **Juba de penas vermelhas** em chama, em volta de um rosto pequeno e afiado.
- **Elmo-tiara prateado** com gema rubi na testa.
- **Colar em V prateado** com gema no peito.
- **Ombreiras** que abrem como asas, com ponta dourada.
- **Capa de penas em sino:** roxa em cima e vermelha embaixo.
- **Pernas longas e finas** com joelheira e tornozeleira prateadas.
- **Garras douradas.**
- **3 tranças douradas** saindo **na horizontal, lado a lado,** das costas da armadura superior, cada uma
  terminando numa pena-lâmina. É uma mudança do dono em relação à ficha, onde elas caem até o chão.

**Expressão:** a neutra da ficha ("NORMAL"), séria e determinada.

### Escala e orçamento

| item | valor |
|---|---|
| altura total (chão → ponta da crista) | **45 u** (2,8 blocos) |
| largura máxima (capa, na frente) | ~29 u |
| comprimento (ponta do bico → ponta da cauda) | ~38 u |
| cubos | **110–170** (teto 200), dos quais ~40–50% planos |
| textura | 128×128 ou 256×128 (no máximo 256×256), 1 px por u |

### Divisão vertical (y a partir do chão)

| faixa | y (u) |
|---|---|
| crista acima do elmo | 39 → 45 |
| cabeça (topo do elmo → queixo) | 31 → 39 |
| pescoço visível / colar | 29,5 → 31 |
| tronco (colar → quadril) | 15 → 29,5 |
| coxas (saia de penas vermelhas) | 10,5 → 15 |
| perna visível (joelho → chão) | 0 → 10,5 |

**Marcos:**

| marco | y (u) |
|---|---|
| ponta das 2 penas externas em U | 45 |
| pena central da crista | 42 |
| topo do elmo / topo da gema da testa | 39 |
| linha dos olhos | 35 |
| bico (base → ponta do gancho) | 34 → 30,5 |
| colar e topo das ombreiras | 29,5 |
| pontas das ombreiras | 29 → 26 |
| gema do peito | 28 → 23 |
| ponta do V do peitoral | 21,5 |
| joelheira | 10,5 → 8,5 |
| canela | 8,5 → 5,5 |
| tornozeleira | 5,5 → 3,5 |
| pé + dedos | 3,5 → 0 |
| barra da capa | 1,5 (não encosta no chão) |

### Larguras (x, vista de frente)

| peça | largura (u) |
|---|---|
| juba (crista + chamas laterais), máx. em y ≈ 37 | 15 |
| par de penas em U | 9 |
| cabeça | 7–8 |
| gema da testa | 2 × 4 (losango vertical) |
| bico | 3 de largura na base |
| pescoço | 5 |
| ombreiras (ponta a ponta) | 21 |
| peitoral | 10 |
| peito creme visível | 7 |
| capa | sino: 21 no ombro → 29 em y ≈ 9 → 27 na barra |
| pernas | centros em x = ±2,6 |
| coxa | 3–4 |
| joelheira / tornozeleira | 3 |
| canela | 2 (**não engrossar**) |
| cada pé | ~6, com os dedos abertos |

### Profundidades (z; 0 = quadril; frente negativa)

| peça | z (u) | nota |
|---|---|---|
| ponta do bico | −11 | |
| bico | −11 → −6,5 | |
| cabeça | −6,5 → 0 | |
| frente do peitoral | −9,5 | o peito estufa quase até a linha do bico |
| tronco | −9,5 → +2,5 | |
| crista | −5 → +12 | varre para trás; a pena mais alta fica em z ≈ +2,5 |
| capa: borda de trás | até +13,5 (em y ≈ 7) | |
| pé | −8 → +1,5 | 3 dedos na frente, 1 atrás |

**Cauda** (mudança do dono: ignore a cauda da ficha):

- **Fecho:** placa prata 6×3×1 nas costas da armadura superior, em x −3..3, y 25..28, z +3..+4.
- **Tranças:** saem do fecho na **horizontal**, todas em y ≈ 26,5, lado a lado:
  - a central (x 0) vai reta para trás;
  - as laterais (x ±1,5) abrem ±18° em leque, vistas de cima.
- **Caimento:** leve, só no fim (0°, 0°, 2°, 4° e 6° por segmento).
- **Medidas:** as pontas terminam em z ≈ +26 a +28; as laterais abrem até x ≈ ±7.

**Perfil em S:** a cabeça vai para a frente, o peito estufa e a capa desce para trás. As tranças seguem na
horizontal, na altura das ombreiras.

### Peças e como fazer

| parte | o que a ficha mostra | como fazer |
|---|---|---|
| crista / juba | 2 penas externas em U (as mais altas, com a ponta curvando para dentro), 1 central, ~3 chamas por lado e ~3 tufos de bochecha por lado; de lado, 5 lâminas varridas para trás | leque de planos recortados (20–30 planos), em vários ângulos para ter volume de frente e de lado; vermelho em 4–5 tons, raiz escura e pontas claras |
| elmo | tiara prateada com 2 asas que sobem para trás e gema rubi vertical no centro; viseira prateada por cima dos olhos | placa prateada sobre a caixa da cabeça (`inflate` 0,02–0,04); gema 2×4 com facetas pintadas, em osso `_brilho` |
| olhos | estreitos, inclinados para dentro, íris vermelho-escura, cara séria | plaquinhas de 2×1 px na face da frente; a viseira passa inclinada por cima; pálpebra para piscar |
| bico | gancho de rapina dourado | 2–3 caixas em degrau (base 3×3, meio, gancho caído); mandíbula separada |
| colar e peitoral | V prateado em 2 camadas, gema losango no centro | 2 placas em V; gema saltada, em osso `_brilho` |
| ombreiras | prata com miolo roxo e ponta dourada | 2–3 placas por lado; a de fora inclinada ~20° para cima e para fora |
| peito | creme com 2–3 chevrons de pena | pintura (não geometria) |
| capa / asas | 3 camadas de penas: roxa com filetes prata (~4 por lado), roxa → vermelha (~5) e vermelha comprida (~6) | planos recortados em ponta, em leque, presos em `asa_d` e `asa_e`. **Não cobre a frente do peito:** a capa abre dos ombros para trás e para os lados |
| coxas | saia de penas vermelhas (3–4 por coxa) | uma caixa vermelha + planos recortados por cima |
| pernas | joelheira prata pontuda, canela roxa, tornozeleira prata | caixas de 3 / 2 / 3 u |
| pés | roxo-escuro escamado, 3 dedos na frente + 1 atrás, garras douradas grossas | dedos em caixas de 1–2 u; garra dourada caída na ponta |
| cauda tripla | 3 tranças douradas, cada uma com uma pena-lâmina dourada e um losango roxo no fim (na horizontal, ver acima) | 5 segmentos de 2×2×3 por trança, **sem** giro de 45° (a trança é pintada em listras diagonais de 3 tons); lâmina de 3×7 em 2 planos cruzados (X), com o losango numa plaquinha `_brilho` |

**Atenção:**

- As penas em U da crista são **vermelhas**. Não há chifres dourados.
- A armadura é **prateada** (com um leve tom lilás), não dourada nem roxa.
- O dourado aparece só no bico, nas garras, nas tranças e nas pontas das ombreiras.

### Ossos e pivôs

| osso | pai | pivô (x, y, z) | animação |
|---|---|---|---|
| `pirococo` | — | (0, 0, 0) | raiz |
| `corpo` | pirococo | (0, 15, −1) | respiração, balanço do andar |
| `pescoco` | corpo | (0, 29, −4) | |
| `cabeca` | pescoco | (0, 31,5, −3,5) | olhar e balanço leve |
| `crista` | cabeca | (0, 38,5, −2) | ondula com atraso |
| `olhos`, `palpebra_d`, `palpebra_e` | cabeca | — | piscar |
| `asa_d` / `asa_e` | corpo | (−5 / +5, 28,5, 0) | a capa; balança leve |
| `cauda` | corpo | (0, 26,5, +3,5) | |
| `cauda_a_0..4` (central), `cauda_b_0..4` (−x), `cauda_c_0..4` (+x) | cauda (em cadeia) | na junta de cada segmento | balançam com fase crescente |
| `lamina_a`, `lamina_b`, `lamina_c` | último segmento de cada trança | — | |
| `perna_d` / `perna_e` | pirococo | (−2,6 / +2,6, 15, 0) | andar |
| `pe_d` / `pe_e` | perna | (∓2,6, 3,5, −1) | compensa a perna no andar |

Ossos de brilho (por exemplo `gema_testa_brilho`, `gema_peito_brilho`, `losango_a_brilho`) ficam dentro dos ossos
acima. **O que brilha:** só as gemas da testa e do peito e os losangos roxos das lâminas da cauda.

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

O olho leva ainda 1 px de pupila #210826 e, se o olho tiver mais de 2 px, 1 px de brilho #fff6e0.

### Animação desta criatura

**idle (L = 4):**

- **Corpo:** respira com rotação em x de ±1,5° e sobe e desce 0,2 u.
- **Cabeça:** ±2° em x e ±3° em y, defasada do corpo.
- **Crista:** ±4°, atrasada da cabeça.
- **Capa** (`asa_d`/`asa_e`): ±2° em z, espelhada entre os lados.
- **Tranças:** balançam ±3° em y e ±2° em x, com atraso de −30° por segmento; as laterais em fase oposta.
- **Piscar:** 1 vez no fim do laço.

**walk (L = 2):**

- **Pernas:** ±25° alternadas; os pés compensam.
- **Corpo:** sobe e desce 0,4 u, 2 vezes por ciclo, e balança ±3° em z.
- **Cabeça:** contrabalança, ficando mais estável que o corpo.
- **Capa:** acompanha com atraso.
- **Tranças:** ±6° em y, acompanhando o corpo.

### Pontos de reprovação específicos desta criatura

- Cabeça grande demais (fofa) ou rosto genérico de galinha. É uma ave de rapina séria.
- Pernas grossas ou curtas: a perna visível tem 10,5 u (23% da altura).
- Capa fechada na frente, escondendo o colar e o peito creme.
- Tranças fundidas numa peça só, sem a lâmina na ponta, caindo até o chão ou penduradas entre as pernas.
- Pés gigantes. O desenho 2D exagera as garras em perspectiva: use as medidas acima.

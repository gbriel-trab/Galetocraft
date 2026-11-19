## Ficha da criatura — Pirococó (#001), "O Galo Fênix"

> **Se esta conversa já tem um modelo anterior do Pirococó, descarte-o.** Este pedido é uma **reconstrução** a partir
> da base anexa. Não reaproveite a construção antiga (capa de planos soltos, crista em raios), só utilitários (UV,
> validações).

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

### Ponto de partida (OBRIGATÓRIO): a base anexa

**Arquivos anexos da base:**

- `blockout_pirococo.py`: o gerador da base;
- `pirococo_blockout.geo.json` e `pirococo_blockout.png`;
- as imagens `pirococo_blockout_vistas.png`, `pirococo_blockout_sem_planos.png` e
  `pirococo_blockout_comparacao.png`.

**Como usar:**

1. Salve o `render_geo.py` (no apêndice) e o `blockout_pirococo.py` na mesma pasta.
2. Rode `python blockout_pirococo.py saida ficha.png`.
3. Faça do `blockout_pirococo.py` o esqueleto do seu `gerar_pirococo.py`: copie e evolua.

**O que a base já resolve** (conferido contra a ficha):

- **A construção:** 116 cubos, 34% de planos, e passa no teste "sem planos".
- **As proporções** e a posição de todas as peças.
- **Os pivôs** e os sinais de rotação.
- **A silhueta** de frente e de costas: um triângulo, com a capa abrindo dos ombros.

**O que NÃO mudar sem motivo forte:**

- o tamanho e a posição dos volumes sólidos;
- as alturas;
- o triângulo da capa;
- a cauda reta para baixo;
- os nomes dos ossos.

**O seu trabalho é o ACABAMENTO** (o "salto"):

1. **Repintar a textura inteira** no padrão B6. A pintura da base é provisória: serve só para ler os materiais.
2. **Refinar as formas** listadas na tabela abaixo.
3. **Fazer o `_glowmask`, as pálpebras e as animações.**

### Escala e orçamento

| item | valor |
|---|---|
| altura total (chão → ponta da crista) | **45 u** (2,8 blocos) |
| largura máxima (capa, na frente) | ~29 u |
| cubos | **110–170** (a base tem 116); planos ≤ ~35% |
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

### Construção por região: o que a base tem e o que refinar

| região | na base (manter) | refino pedido |
|---|---|---|
| tronco | 2 caixas sobrepostas (10×13×10 + 8×11×12), frente com V creme pintado | pintura: V creme claro afinando para baixo, vermelho em faixas |
| peito | bloco creme 8×8×3 saltado (peito de pombo) + 6×4×2 abaixo + franja creme em pontas | chevrons em zigue-zague de 1 px (#d9b398), luz no topo, quinas com 1 px de sombra |
| pescoço | caixa 6×5×6 | frente creme e nuca vermelha, com faixa de sombra sob o queixo |
| cabeça | caixa 8×8×7 + tampa 6×1×5 + nuca 6×6×1 (contorno chanfrado) | rosto: creme embaixo (garganta e bochecha); marcas de pena de 1 px nas laterais; topo escuro sob a juba |
| bico | base 3×3×2, meio 2×2×2, gancho 2×2×1 caído | topo #ffe138, lados #fcb419, gancho e base de baixo #d87b08; 1 px de narina |
| olhos | cubos de quina 2×1×2 (`inflate` 0,02) + viseira prata girada | 1 px #fff6e0 + 1 px de íris #9e1020; acrescente **pálpebras** (`palpebra_d`/`palpebra_e`, cubo igual vermelho, `inflate` 0,01) para piscar |
| elmo | casca prata 9×2×8 em volta da cabeça, traseira mais alta, + gema 2×4 | chanfro pintado (1 px #f6f6f6 em cima, #ac93ae embaixo); gema com 3 facetas; 2 aletas planas de 3×4 saindo para trás, de dentro da juba |
| juba | 2 blocos sólidos (8×2×8 em cima; 6×4×6 varrendo para trás e para cima) + 2 penas em U de 5×8 (a lira) + pena central de 5×5 + 3 chamas de 5×8 por lado (abrindo 14°, 26° e 38°) + 4 lâminas de nuca de 5×11 com ponta para trás + tufos de bochecha | pinte cada chama com raiz escura, haste clara e ponta curva na luz; pinte os blocos com mechas de 1 px; pode acrescentar 1–2 lâminas de 4×10 varrendo para trás (de lado, a juba deve mostrar ~5 pontas); mantenha a ponta mais alta em y ≤ 45,5 |
| ombreiras | concha prata 6×4×8 + tampa roxa 5×1×7 + ponta dourada 3×1×5, abrindo 20° (borda de fora SOBE) | losango roxo pintado na tampa, borda prata chanfrada, a ponta dourada só no filete de fora |
| colar + gema | V de 2 placas prata 5×2×1 + faixa 10×2×3 + gema 3×5×1 | chanfro pintado; gema com facetas e brilho (`gema_peito_brilho`) |
| asas-capa (`asa_d`/`asa_e`) | **3 placas sólidas** por lado (3×13×10, 3×13×12, 2×11×13), abrindo 20°, 23° e 24° e recuando 6°, 12° e 16°; franja de 4 u em pontas embaixo de cada placa | **repinte as penas** (B6: penas de 5 px em 2 fileiras, filete prata em penas alternadas nas roxas; vermelhas com pontas claras). Acrescente **2–3 planos de pena 4×8 por lado** saindo da borda de trás da placa de baixo, apontando para trás e para baixo: de lado, a capa precisa mostrar pontas como na ficha DIREITA |
| costas da capa | 3 placas sólidas em leque (12×13×2, 18×13×2, 22×10×2), mais abertas embaixo, + franja | mesma pintura; pena central marcada (o "eixo" do leque da ficha TRÁS) |
| cauda | fecho prata 7×3×1 nas costas + 3 tranças **retas para baixo**, encostadas por fora da capa, em x 0 e ±3: a central com 5 segmentos 2×3×2 e as laterais com 3. Inclinadas 17° para trás (seguem a capa); as laterais abrem 5°. Lâminas em X (5×8 na central, 4×7 nas laterais) com losango. Pontas em y ≈ 2 (central) e ≈ 8 (laterais) | trança pintada em gomos diagonais (`<<<`, 3 tons de dourado); lâmina em forma de chama apontando para baixo, com o losango rubi; **sem curva nenhuma** |
| pernas | coxa vermelha 4×5×5 + franja; joelheira 3×2×3 + espora triangular; canela roxa 2×3×2; tornozeleira 3×2×3 + ponta para baixo | coxa com penas pintadas; chanfro nas peças prata |
| pés | pé 3×2×4 roxo-escuro, 3 dedos 1×1×3 abertos −28°, 0° e +28°, garras douradas 1×1×2 caídas 30°, dedo de trás | escamas de 1 px nos dedos; garra com ponta clara |

**Atenção:**

- As penas em U da crista são **vermelhas**. Não há chifres dourados.
- A armadura é **prateada** (com um leve tom lilás).
- O dourado aparece só no bico, nas garras, nas tranças, nas lâminas da cauda, nas pontas das ombreiras e no fecho.

### Ossos (os da base) e animação

**Ossos:**

- **Raiz:** `pirococo`.
- **`corpo`:** pescoco → cabeca → crista; gema_peito_brilho; ombreira_d e ombreira_e; asa_d e asa_e; capa_costas;
  cauda.
- **`cauda`:** cauda_a_0..4, cauda_b_0..2 e cauda_c_0..2, encadeados; cada um termina em lamina_a/b/c, com
  losango_a/b/c_brilho.
- **Pernas:** perna_d e perna_e, filhas da raiz, com dedo_d_0..2 e dedo_e_0..2.
- **A acrescentar:** `palpebra_d` e `palpebra_e` (filhas de cabeca).

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

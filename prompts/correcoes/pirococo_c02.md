# Correção 2 — Pirococó (pirococo)

Continue o MESMO modelo desta conversa, a partir do seu `gerar_pirococo.py`. Mude o que está listado abaixo e
preserve o resto. As regras do pedido original continuam valendo:

- 1 px por unidade;
- cubos de tamanho inteiro;
- planos com uma face só;
- paleta e rampas da ficha;
- nomes dos arquivos e das animações `idle`/`walk`.

**Anexos:**

- **`pirococo_c02_marcacoes.png`:** em cima, o seu resultado com os problemas numerados (os números são os mesmos
  dos itens abaixo). Embaixo, as vistas FRENTE, DIREITA e TRÁS da ficha, na mesma altura, para comparar direto.
- **`proporcoes_anime_planta.png`:** a planta de proporções, com os volumes planejados sobre a ficha e, em vermelho,
  o caminho novo da cauda (item 3).
- **A ficha da criatura.**

**Diagnóstico geral:**

- **O que melhorou:**
  - peito em escudo com colar em V e gema;
  - bico com gancho;
  - olhos bravos sob a viseira;
  - pescoço;
  - pés com dedos.
- **O problema agora é LEITURA.** O modelo ainda lê como um **totem retangular vermelho com uma cortina atrás**.
- **O que a ficha mostra:** uma **ave** com penas roxas emoldurando o peito, uma juba de chamas larga e maciça, e
  penas com pontas nítidas.
- **O nível pedido é o de um modelo oficial do Cobblemon** (Talonflame, Braviary):
  - cada pena lida individualmente;
  - silhueta limpa;
  - nada solto;
  - nenhum fio.

---

## O que está bom (NÃO mexer)

- A altura total (45 u), os marcos de altura e o comprimento das pernas.
- O peito em escudo com colar em V e gema. Só ajuste o perfil e a pintura (itens 6 e 8).
- O bico com gancho, os olhos com viseira inclinada (a expressão está boa) e o pescoço creme.
- **Os tons da paleta, que estão corretos.** O problema é a distribuição de luz (item 8).
- Os nomes de arquivos, de ossos e de animações.

---

## Problemas, do mais grave para o menos grave

Ordem de trabalho: **1 → 2 → 4 → 5 → 6 → 3 → 7 → 8**. Renderize e OLHE depois de cada item, comparando com a
metade de baixo da imagem de marcações.

### 1. Capa: flancos expostos, "vassoura" e cortina (o mais grave)

**Como está:**

- A capa começa atrás dos ombros. De frente, os lados do tronco aparecem como paredes vermelhas lisas (o
  "caixote").
- A fileira de baixo é feita de planos longos e estreitos, quase de perfil. Parece uma franja de palha que vai até o
  chão.
- De costas, é uma cortina lisa em faixas horizontais (roxo em cima, vermelho embaixo), sem penas.
- De lado, é uma chapa roxa lisa.

**Como deve ficar** (ficha FRENTE e TRÁS):

- **Frente:** as penas roxas de cima saem de baixo das ombreiras e descem **pela frente dos flancos**, na diagonal
  (a ponta indo para fora), e emolduram o peito. De frente se vê:
  - o creme no centro (7–8 u);
  - uma faixa de penas roxas de cada lado (x ±4 a ±10);
  - o leque vermelho embaixo.
- **Cada pena tem forma de pena:**
  - larga (5 px);
  - ponta em V nítida;
  - filete prata em uma borda;
  - sobreposta à vizinha como telha.
- **Costas:** um leque simétrico que parte do centro, com a borda de baixo **serrilhada pelas pontas**, nunca uma
  linha reta.

**Como fazer:**

- **Remova** os planos longos e estreitos atuais e refaça a capa como 3 fileiras de penas largas. Elas ficam
  presas num anel em volta do tronco, não só atrás.
- **As 3 fileiras:**

  | fileira | penas por lado | tamanho do plano | posição e arranjo |
  |---|---|---|---|
  | 1 (roxa, filete prata) | 4 | 5×11 | **a 1ª de cada lado fica NA FRENTE do flanco**: presa em x ±5, z −6, y 28, girada ~25° em z (ponta para fora) e ~10° para a frente, cobrindo o vermelho do flanco. As outras giram em y em volta do corpo, ~30° uma da outra, até as costas |
  | 2 (roxo → vermelho) | 5 | 5×13 | presa 4 u abaixo da fileira 1, mesmo arranjo, abrindo 12° para fora |
  | 3 (vermelha, a maior) | 6 | 5×13 | presa em y ≈ 15; as pontas terminam em **y 2–3** (não no chão); abre 18° para fora (o sino) |

- **Costas:** 2–3 penas centrais por fileira (uma no meio e as outras a ±20°), formando o leque.
- **Pontas:** cada pena termina em V, com degraus de 1 px. Nunca em franja.
- **Ângulo dos planos:**
  - nenhum plano pode ficar a menos de 25° de estar de perfil nas vistas de frente ou de lado (de perfil, ele vira
    fio);
  - gire em z (para fora) e em volta do corpo, não só em y;
  - a borda de trás da capa fica em **z ≤ +13,5**, para dar folga à cauda (item 3).
- **Pintura de cada pena** (é o que a faz ler como pena):
  - metade de fora/de cima 1 tom mais clara e metade de dentro 1 tom mais escura;
  - haste de 1 px no tom claro;
  - nas roxas, filete de 1 px #e4dce3 na borda de fora;
  - ponta com 2 px no tom de luz;
  - penas vizinhas alternam base e sombra, para as telhas se separarem.

**Aceite:**

- De frente: creme no centro, emoldurado por duas faixas roxas diagonais, e **nenhuma parede vermelha lisa**.
- De costas: leque de penas com borda serrilhada.
- De lado: 3 camadas de pontas.
- Nenhum fio e nenhuma pena encostando no chão.

### 2. Crista e juba: raios finos

**Como está:**

- De frente, um "sol" de ~20 raios de 1–2 px separados por vazios.
- De costas, uma bola espinhenta.
- As penas em U são 2 "chifres" finos em degrau.

**Como deve ficar** (ficha FRENTE, DIREITA e TRÁS):

- Uma juba **maciça** de chamas largas e curvas: as penas se sobrepõem e formam uma massa contínua, com o contorno
  recortado.
- **De frente:**
  - 2 penas externas grandes em U (a forma de lira);
  - 1 pena central;
  - de cada lado, 3 chamas grandes que sobem e se curvam para fora.
- **De lado:** lâminas largas varrendo para trás.
- **De costas:** um leque radial denso.

**Como fazer:**

- **Remova todos os planos de 1–2 px.**
- **Refaça com 14–16 planos grandes.** Cada um é uma chama ou folha de 5–6 px de largura na base e 8–12 px de
  comprimento, com a ponta curvando (desenhada na textura).
- **Sobreposição:**
  - cada pena cobre pelo menos 2 px da vizinha;
  - na vista de frente, não pode aparecer fundo entre penas da mesma camada.
- **As penas:**

  | penas | plano | posição e giro |
  |---|---|---|
  | 2 em U | 5×10, virados para a frente | base em x ±3, y 38; ponta em y 45; giradas 15° em z para fora e 20° para trás. Na textura, a pena sobe e a ponta **curva para dentro**: o vão entre as duas pontas forma o "U" |
  | 1 central | 5×8 | até y 42, inclinada 25° para trás |
  | 3 chamas por lado | 5×9 | saem do **alto e de trás** da cabeça (não das laterais do rosto); giradas 30°, 50° e 70° em z para fora e 25° para trás; as pontas chegam a x ±7,5 em y ≈ 37 |
  | 4 lâminas de nuca (vistas de lado) | 5×12, verticais | de −15° a −55° (varrendo para trás); a mais longa chega a z ≈ +12 |
  | 2 tufos de bochecha por lado | 3×5 | atrás da linha do rosto |

**Aceite:**

- De frente: a juba lê como uma massa em leque, com ~15 u de largura, ~9 pontas curvas e sem buracos.
- De costas: um leque denso, como na ficha TRÁS.
- Nenhuma pena com base menor que 5 px, fora os tufos de bochecha (3 px).

### 3. Cauda tripla: aplicar a GRAVIDADE (pedido do dono)

**Como está:**

- As 3 tranças saem retas, na horizontal, duras como um bastão.
- De costas, a saída é um amontoado de arcos e blocos dourados.
- A trança pintada em xadrez parece uma fita métrica.
- A lâmina é um retângulo com um quadrado roxo, que parece uma etiqueta.

**Como deve ficar:**

- As tranças continuam saindo lado a lado das costas da armadura superior.
- Agora elas **caem com a gravidade**:
  - saem na horizontal;
  - fazem uma curva suave;
  - descem quase na vertical, atrás da capa, como três cordas pesadas.
- A central é a mais longa. Veja a linha vermelha na vista de lado da planta anexada.

**Como fazer:**

- **Fecho:** placa prata 6×3×1 (x −3..3, y 25..28, z +3..+4), lisa, com filete dourado. Remova os arcos e blocos
  dourados atuais.
- **Saída:**
  - a trança central fica em x 0;
  - as laterais ficam em x ±2, abertas ±15° (vistas de cima);
  - todas começam em y 26,5, z +4.
- **Segmentos:** de 2×2×3, cada um num osso com o pivô na junta. A curva é feita girando cada junta **para baixo** em
  relação à anterior:

  | trança | dobra de cada junta | ângulo acumulado |
  |---|---|---|
  | central (8 segmentos) | 0°, 0°, 15°, 15°, 20°, 20°, 15°, 3° | 0, 0, 15, 30, 50, 70, 85, 88 |
  | laterais (6 segmentos) | 0°, 0°, 15°, 15°, 20°, 20° | 0, 0, 15, 30, 50, 70; a lâmina fecha em ~85° |

- **Trajetória esperada** (z, y):
  - **central:** (4, 26,5) → (10, 26,5) → (15,5, 24,2) → (18,5, 19,1) → (18,8, 13,1) → ponta da lâmina em
    (18,8, 6);
  - **laterais:** (4, 26,5) → (9,8, 26,5) → (15,1, 24,2) → (18, 19,1) → ponta em (18,5, 12), com x ≈ ±6.
  - **Confira o sentido da rotação no renderizador:** a trança tem que descer, não subir.
- **Folga:** nenhuma trança encosta na capa. A borda de trás da capa fica em z ≤ +13,5.
- **Padrão de trança** (na textura):
  - em cada segmento, 3 gomos em diagonal (como `<<<`);
  - 3 tons: #ffcd29 claro, #fcb419 base e #d87b08 sombra no sulco;
  - o topo de cada segmento 1 tom mais claro;
  - **nada de xadrez.**
- **Lâmina da ponta** (como no quadro "CAUDA TRIPLA" da ficha):
  - pena dourada em forma de chama, 4×8: larga no meio, pontuda na ponta;
  - feita de 2 planos cruzados em X;
  - losango rubi de 2×3 no meio, no osso `losango_a_brilho`, `losango_b_brilho` ou `losango_c_brilho`;
  - pendurada, a lâmina aponta para baixo.
- **Animação:**
  - **idle:** pêndulo pequeno. Cada trança gira ±3° em z e ±2° em x, com atraso de −30° por segmento; as laterais em
    fase oposta.
  - **walk:** ±6° em z, defasado do corpo.

**Aceite:**

- De lado: 3 cordas que saem na horizontal das costas e caem atrás da capa. A central termina em y ≈ 6 e as laterais
  em y ≈ 12.
- De costas: as 3 descem lado a lado sobre o leque da capa.
- Nada de xadrez.

### 4. Ombreiras: "guidão"

**Como está:**

- De frente, duas barras prata finas, quase horizontais, com ponta dourada. Parecem guidão de bicicleta.
- De lado, um bloco com tampa dourada.
- Não há miolo roxo.

**Como deve ficar** (ficha FRENTE e quadro ARMADURA PEITORAL):

- Ombreiras **grandes e com volume**, em forma de concha, cobrindo o alto da capa.
- Prata, com miolo roxo.
- Uma garra dourada na ponta, virada para cima e para fora.

**Como fazer:**

- **Cada lado tem 3 peças:**

  | peça | tamanho | posição e giro |
  |---|---|---|
  | concha | caixa 6×3×7 (x 4..10, y 26..29, z −4..+3) + caixa de chanfro 5×1×5 por cima (y 29..30) | as duas giram juntas 20° em z (a borda de fora sobe), com pivô em (±4, 28, 0) |
  | aba frontal | placa 5×2×1 na frente da concha | desce 10° e fecha a ombreira sobre o peito, encostando no colar |
  | ponta (a "garra" da ficha) | placa dourada 3×1×4 na borda de fora | girada mais 25° (total ~45°) |

- **Pintura:**
  - topo da concha com losango ou faixa roxa (#702a7c / #88398e), ocupando ~60% da face de cima;
  - borda prata de 1 px: #f6f6f6 em cima e #ac93ae embaixo;
  - **nenhum dourado no topo**, só na ponta.

**Aceite:**

- De frente: as ombreiras têm ≥ 3 u de altura visível, mostram o roxo e sobem para fora.
- De lado: não há mais "tampa" dourada.

### 5. Elmo e cabeça

**Como está:**

- A tiara são barras prata finas, soltas no ar. De lado, uma passa por cima da cabeça e outra espeta para trás.
- A cabeça é um cubo vermelho liso.

**Como deve ficar** (quadro ELMO da ficha): o elmo **abraça** a cabeça.

- Uma faixa prata em V sai da gema e passa por cima dos olhos (a viseira).
- Ela segue pelas laterais, subindo para trás.
- Termina em duas aletas curtas que se misturam à crista.

**Como fazer:**

- **Faixa:** 2 placas prata de 1×2×7 **coladas** na lateral da cabeça, a no máximo 0,1 u (nenhum vão). Vão da frente
  (z −7, junto da gema) até z 0, inclinadas 15° (a traseira mais alta).
- **Aletas:** planos de no máximo 3×4, apontando para trás e 30° para cima, saindo de dentro da crista.
- **Remova** as barras que flutuam acima da cabeça.
- **Arredondar a cabeça** (técnica Cobblemon):
  - mantenha a caixa 8×8×7;
  - acrescente uma "tampa" 6×1×5 em y 39..40, recuada 1 u de cada lado;
  - acrescente uma "nuca" 6×6×1 em z 0..1;
  - assim, em 3/4 o contorno fica chanfrado, e não um cubo.
- **Olhos:** mantenha a posição e a viseira. Para ler melhor:
  - o px branco do olho em #fff6e0;
  - 1 px de sombra #b68b78 logo abaixo do olho, no creme da bochecha.

**Aceite:**

- De lado: o elmo é uma faixa colada à cabeça, subindo para trás.
- Em 3/4: a cabeça tem quinas chanfradas.

### 6. Tronco: perfil reto, sem "peito de pombo"

**Como está:**

- De lado, o creme é uma parede reta de y 29 a 17.
- Em 3/4, o peito parece uma tábua colada na frente de um paralelepípedo.

**Como deve ficar** (ficha DIREITA): peito estufado, mais à frente na altura da gema, recuando para baixo.

**Como fazer:**

- **Degraus do peito:**

  | degrau | y | z |
  |---|---|---|
  | superior | 21..27 | −10..−8 (a parte mais à frente) |
  | médio | 17..21 | −9..−7 |
  | inferior | 15..17 | −8..−7 |

  - O perfil recua 2 u de cima para baixo.
- **Quinas:** em cada degrau, pinte as quinas verticais com 1 px do tom de sombra. Faça o degrau de cima 2 u mais
  estreito que o tronco, para o 3/4 não ler como tábua.
- **Fim do creme:** como na ficha, termina em **zigue-zague** de penas sobre o vermelho das coxas: um plano creme de
  6×3 com 3 pontas.
- **Chevrons:** em zigue-zague (como a ficha), não em retângulos.

**Aceite:**

- De lado: o ponto mais à frente do peito fica em y 22–26, e o peito recua 2 u até o quadril.
- Em 3/4: o peito não parece uma tábua.

### 7. Pernas e pés

**Como está:**

- A joelheira e a tornozeleira têm forma de cruz ou parafuso (barra horizontal + pino).
- De frente, as garras viram uma "coroa" de cubos amarelos alternados.
- As coxas estão escondidas.

**Como deve ficar** (quadro PERNAS REFORÇADAS da ficha):

- **Joelheira:** placa prata em ponta de flecha, subindo sobre o joelho.
- **Tornozeleira:** punho prata com ponta para baixo.
- **Pés:** roxo-escuros, com 3 garras grandes e curvas na frente, abertas, e 1 atrás.

**Como fazer:**

- **Joelheira:**
  - caixa 3×2×3 + plano triangular na frente (3 de base × 4 de altura, ponta para cima), inclinado 15° para a
    frente;
  - **sem** barra horizontal saliente.
- **Tornozeleira:** caixa 3×1×3 + plano triangular de 3×2 apontando para baixo, na frente.
- **Dedos:**
  - 3 na frente, 1×1×3, roxos, abertos −30°, 0° e +30°;
  - garra dourada em 2 cubos: 1×1×1 + ponta 1×1×1 girada 40° para baixo (a curva), com a ponta encostando em y 0;
  - o dedo de trás é igual, mais curto.
- **Coxa:** de frente, mostre 1–2 u de coxa vermelha emplumada entre o peito e a joelheira, com 2 penas 3×4 caindo
  sobre a joelheira.

**Aceite:**

- De frente: cada pé mostra 3 garras curvas e abertas, não uma fileira de cubos.
- A joelheira lê como uma ponta de flecha.

### 8. Pintura: luz e leitura das penas

**Como está:**

- Os tons estão corretos, mas quase tudo está no tom base ou mais escuro. Faltam luzes.
- As penas não se separam umas das outras.
- O creme tem sombra demais (manchas largas cor de areia).
- Corpo, capa e crista são o mesmo bloco vermelho.

**Como fazer:**

- **Distribuição em cada material:**
  - ~40% de luz e claro;
  - ~40% de base;
  - ~20% de sombra e sombra funda.
  - O jogo escurece a frente (×0,8) e os lados (×0,6), então a textura precisa parecer mais clara no PNG do que
    no jogo.
- **Cada pena** (crista, capa, coxas):
  - borda de fora/de cima clara e borda de dentro escura;
  - haste clara de 1 px;
  - ponta no tom de luz;
  - penas vizinhas alternam base e sombra.
- **Separar os vermelhos:**
  - a crista e as penas da capa usam a rampa inteira, com pontas #ff5b3f/#ef392d;
  - o corpo fica em base e sombra;
  - as coxas têm pontas claras.
- **Creme:**
  - dominante em #ffeed1/#fde1c0;
  - #d9b398 só nos chevrons em zigue-zague e na última linha.
- **Prata:** chanfro pintado em todas as placas: 1 px #f6f6f6 em cima e #ac93ae embaixo.
- **Grão leve:** 5–8%.

**Aceite:** com a vista de frente reduzida a 25%, as massas de cor batem com a ficha:

- juba vermelha clara em cima;
- creme no centro;
- roxo dos lados;
- leque vermelho embaixo;
- dourado atrás.

---

## Conferência final

- **Validações do script:** rode todas de novo:
  - tamanhos inteiros;
  - `uv_size` igual à face;
  - ilhas de UV sem sobreposição;
  - planos com uma face só;
  - altura de 45 u;
  - ossos usados nas animações.
- **Orçamento:** até **190 cubos** nesta rodada. A troca de raios finos e fios por penas largas compensa a capa
  nova e a cauda.
- **Animações:**
  - atualize o idle e o walk, com o pêndulo da cauda;
  - confira o 1º quadro do idle: tranças longe da capa, capa sem atravessar as pernas.
- **Autocrítica antes de entregar:**
  - monte a mesma comparação da imagem de marcações: suas vistas em cima e a ficha embaixo, na mesma altura;
  - liste as 3 maiores diferenças que ainda restam.

## Entregue

- **Os arquivos atualizados:** `pirococo.geo.json`, `pirococo.png`, `pirococo_glowmask.png`,
  `pirococo.animation.json` e `gerar_pirococo.py`.
- **As imagens:**
  - `pirococo_vistas.png`;
  - `pirococo_rosto.png`;
  - `pirococo_antes_depois.png` (as vistas antigas em cima e as novas embaixo);
  - `pirococo_comparacao.png` (ficha × modelo).
- **Uma lista curta:** item (1 a 8) → o que mudou (com números) → resolvido ou parcial, mais as 3 maiores diferenças
  que ainda restam.

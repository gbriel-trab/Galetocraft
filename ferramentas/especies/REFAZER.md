# Refazer uma espécie rejeitada pelo dono

> **Desde 18/11/2026, o padrão visual é `modelos/GUIA_ESTILO.md` (estilo Cobblemon).** As regras de fidelidade,
> rosto e olhar abaixo continuam valendo. As regras técnicas sobre textura chapada, placas finas e volumes
> arredondados foram revistas na seção 9 do guia, que mantém o motivo de cada uma (nada de "papel" nem de
> "quadradão").

O dono viu a versão anterior no jogo (`modelos/fotos_jogo/<id>_jogo.png`) e disse que ela ficou **estranha**. Ele
pediu para refazer **mais fiel à ficha**. O Cocórak e a Vagaló foram aceitos: veja `modelos/fotos_jogo/vagalo_jogo.png`
e `cocorak_jogo.png`.

Leia antes o `BRIEFING.md` (regras, esqueleto do arquivo, nomes dos ossos, orçamento). Este arquivo diz o que muda.

## O que deixava os modelos estranhos
Comparando as fotos do jogo com as fichas:
1. **Placas finas e franjas no lugar de volumes.** As fichas são feitas de BLOCOS GROSSOS e sólidos: cada pena,
   folha ou escama é um cubo ou um degrau com espessura visível, em camadas que se sobrepõem. Nos modelos
   rejeitados, penas viraram planos finos recortados com alfa e franjas "pingando". De longe parecia pelo,
   fumaça ou papel.
   - Use caixas com espessura (≥ 1 unidade), com bordas em degrau.
   - Placas recortadas ficam só para o que é fino na ficha mesmo: membrana de asa, chama, pétala.
2. **Textura com ruído.** Xadrez, pontilhado, listras finas e "gotas" deixam a peça suja.
   - A ficha usa 2 ou 3 tons chapados por bloco: claro em cima, base, sombra embaixo.
   - Os padrões (faixas, espirais, manchas) são grandes e legíveis.
3. **Rosto diferente da ficha.** O rosto rejeitado tinha:
   - máscara chapada em caixa;
   - olhos redondos de desenho, sem a sobrancelha ou pálpebra brava da ficha;
   - bico como uma caixa grande saindo da cara;
   - barbela em formato de gravata.

   Copie o rosto da ficha (`_expressoes.png`, expressão neutra) peça por peça: o formato do olho, a cor da íris, a
   sobrancelha e onde ela fica, o tamanho do bico em relação à cabeça e a cor da cara em volta do olho.
4. **Proporções e elementos fora da ficha.** Por exemplo:
   - cauda de cipó que na ficha é UMA espiral virou dois anéis;
   - cabeça pequena demais;
   - pescoço baixo;
   - corpo deitado quando a ficha é ereta.

   Siga as 4 vistas.

## A ferramenta nova: comparação com a ficha
```
python ferramentas/comparar_ficha.py <id> [prefixo]
```
Ela grava `modelos/<id>/revisao/<prefixo>_comp.png`. Para cada uma das 4 vistas, no mesmo tamanho, a imagem mostra:
- a ficha com o contorno do modelo em ciano por cima;
- o modelo;
- o mapa de diferença: vermelho = falta no modelo, azul = sobra no modelo.

Ela também imprime o IoU das silhuetas.
- A versão rejeitada ficou entre 56% e 70%. A meta é ≥ 75% de média, sem nenhuma vista abaixo de 65%.
- O IoU NÃO basta: a Taturico rejeitada tinha 86%. A linha de cima comparada com a do meio é o que importa:
  forma das partes, rosto, cores e padrões.
- Faça a comparação a cada rodada e OLHE a imagem. Corrija primeiro a maior mancha vermelha ou azul. Depois, a
  diferença mais visível entre a linha de cima e a do meio.

Rode `python ferramentas/comparar_ficha.py <id> antigo modelos/<id>/revisao/final.bbmodel` uma vez no começo,
para ver lado a lado o que foi rejeitado. (O caminho do .bbmodel pode vir antes ou depois do prefixo.)

## Como trabalhar
- **Refaça a montagem** guiada pela ficha. Funções do arquivo atual podem ser reaproveitadas, mas não
  "remende" o modelo rejeitado.
- Antes de qualquer peça, meça na ficha (em pixels, nas vistas):
  - altura da cabeça : tronco : pernas;
  - largura do corpo de frente;
  - comprimento da cauda de lado.

  Converta para unidades, com altura total ≈ 16 × ALTURA unidades. Mantenha o `ALTURA` atual do seu arquivo.
- Guarde as rodadas com prefixo `n1`, `n2`, ...:
  ```
  python ferramentas/rodada_revisao.py <id> nK
  python ferramentas/comparar_ficha.py <id> nK
  ```
  NÃO sobrescreva os arquivos antigos `r*`, `rev*` e `final*`.
- Faça pelo menos 10 rodadas. Olhe `nK_comp.png`, `nK_3-4.png` (compare com `_arte.png`) e `nK_rosto.png` (compare
  com `_expressoes.png`).
- Orçamento: até ~350 peças. Blocos grossos costumam precisar de MENOS peças que franjas de placas.
- Os mesmos nomes de ossos animáveis (veja o BRIEFING). Mantenha `ONDAS`, `ANIM_PARADO` e `ANIM_ANDANDO`
  coerentes com os ossos novos.

## Relatório final (até ~20 linhas)
- O prefixo da melhor rodada e o IoU dela por vista (antes × depois).
- O que mudou em relação à versão rejeitada.
- Peças, textura e ossos animáveis.
- O que ainda difere da ficha.

---

# Fase 2: fidelidade aos DETALHES (pedido do dono depois de ver as fotos no jogo)

O dono viu a refação no jogo e disse: **"não apenas a silhueta, mas também a fidelidade aos detalhes"**. Acertar o
contorno já não basta. Cada detalhe da ficha precisa estar lá, no lugar certo, com a forma e a cor certas.

## O que o diretor de arte viu nas fotos do jogo
- **Rosto e bico de frente:** o bico aparece como uma caixa amarela grande no meio da cara (Taturico, Axococó,
  Cocórvolt) e a crista parece um boné (Salambrasa).
  - Na ficha, o bico de frente é uma cunha pequena e afilada, mais estreita embaixo.
  - O rosto tem os planos e as cores da ficha: onde é creme, onde é escuro, o formato exato do olho e da
    sobrancelha.
  - Lembre que no jogo a câmera fica quase na altura da cabeça e de perto: o bico de frente pesa muito.
- **Padrões e emblemas:** devem ter o MESMO desenho da ficha. Exemplos:
  - o emblema do ombro do Taturico na ficha é um "G"/espiral arredondada, não uma espiral quadrada qualquer;
  - as faixas das costas têm a largura e a ordem de cores da ficha;
  - as manchas da Salambrasa têm o tamanho e a posição da ficha.
- **Cores:** use as cores da ficha, não aproximações. Amostre-as nos PNGs da ficha (com PIL, nos pixels das
  regiões certas), não "de cabeça".

## A ferramenta agora mede detalhe e cor
`comparar_ficha.py` ganhou uma 4ª linha no `_comp.png` e uma nota **cor** por vista.
- O quadro é dividido em células de 8 px. Onde ficha e modelo têm conteúdo, a ferramenta compara a cor média:
  - verde = bate;
  - vermelho = cor ou detalhe errado ou fora do lugar.
- Referência: a Vagaló aceita tem cor ~40%. A versão atual das refeitas está entre ~44% e 49%.
- **Meta: subir pelo menos 10 pontos na cor média, sem baixar o IoU mais de 2 pontos.** Sobretudo, não pode
  sobrar mancha vermelha grande em rosto, bico, olhos, emblemas, padrões e acessórios.

## Como trabalhar nesta fase
1. Escreva `modelos/<id>/detalhes.md`: a lista COMPLETA de detalhes da ficha, tirada de TODAS as imagens:
   - `_ficha` (inclusive a paleta de cores);
   - `_arte`;
   - `_vistas`;
   - cada quadro de `_detalhes`;
   - a expressão neutra de `_expressoes`.

   Para cada detalhe, anote:
   - onde fica (vista e posição);
   - forma;
   - tamanho relativo;
   - cores (com o RGB amostrado da ficha);
   - status: ok, parcial ou falta.

   Espere 30 a 60 itens: olho (íris, pupila, brilho, pálpebra), sobrancelha, bico (de frente e de lado), narina,
   barbela, crista (nº de lâminas), cada marca ou cicatriz, cada emblema, padrões do corpo, penas de cada região,
   garras (cor e número), acessórios e cada parte deles.
2. Corrija item por item, começando pelo rosto (é onde o dono mais olha) e depois os emblemas e padrões.
3. A cada rodada (`n20`, `n21`, ... sem sobrescrever as anteriores), olhe:
   - as linhas 1, 2 e 4 do `_comp`;
   - `_rosto` × `_expressoes` (neutra);
   - `_3-4` × `_arte`.

   Atualize o status no `detalhes.md`.
4. Pelo menos 8 rodadas nesta fase. Termine com tudo "ok" ou com o motivo de cada "parcial".

Relatório final: rodada final, IoU e cor (antes × depois), quantos itens do `detalhes.md` ficaram ok, parcial e
falta, e o que mudou.

---

# Fase 5: conferir pela ARTE CONCEITUAL (pedido do dono)

O dono julga pela arte conceitual principal: a ilustração grande de cada ficha, `modelos/referencias/<NNN_id>_arte.png`.
Do Morcegalo ele disse: "é menos gordo, lembre de ser fiel à arte conceitual". Do Cocórion: "braço e rabo muito
grandes, ele é mais slim". As vistas ortográficas e a tabela de dimensões não pegaram isso, mas a arte pega.

## Como conferir
1. Renderize o modelo no ângulo e no enquadramento da arte (o yaw/pitch que mais se aproxima) e monte uma imagem
   lado a lado com a arte, na mesma altura total: `revisao/<rodada>_arte_lado.png`.
2. Meça na ARTE e no modelo, como fração da altura total:
   - largura e profundidade do tronco;
   - altura da cabeça e altura da crista;
   - comprimento das pernas visíveis;
   - tamanho das asas (envergadura ou largura da capa);
   - tamanho da cauda (comprimento e largura do leque);
   - espessura das penas grandes.

   Anote no `detalhes.md` uma tabela com arte × modelo.
3. Corrija o que passar de ~10% de diferença, começando pela MASSA: corpo gordo, asas ou cauda grandes demais,
   pernas curtas. Depois corrija a forma das partes como a arte mostra: crista, joelho, ângulo das penas.
4. A arte vale mais que a tabela de dimensões e que as auditorias quando elas a contradizem. A pose da arte
   (asa erguida, perna dobrada) não precisa ser copiada; as PROPORÇÕES e as formas, sim.

---

# Fase 6: SUAVIDADE, menos blocos e menos "quadradão" (pedido do dono)

Pedido do dono sobre os míticos: "refina o Cocórvolt, a nuca dele por exemplo tá estranha, tem muitos blocos,
tenta deixar ele mais suave, menos quadradão, e o mesmo vale para o Cocórion, ele tá saindo bem feio".

Referência do nível aprovado: Esporocó, Morcegalo, Espinhocó e Pirococó (`modelos/fotos_jogo/*_jogo.png`;
código em `ferramentas/especies/esporoco.py` e `ferramentas/pirococo7.py`).

## O que deixa um modelo "quadradão" e feio
- **Muitos cubinhos pequenos** de tamanhos e ângulos diferentes amontoados numa região (nuca, bochecha, crista,
  ombro). Isso vira ruído visual, cara de entulho.
- **Degraus grandes e bruscos** entre volumes vizinhos, e caixas grandes com quinas vivas onde a arte mostra
  forma arredondada.
- **Peças que saltam da superfície** em ângulos aleatórios, em vez de deitar sobre ela.
- **Texturas com contraste forte** entre peças vizinhas (cada cubo de uma cor), o que realça cada bloco.

## Como suavizar
1. **Menos peças e maiores.** Cada região deve ter POUCOS volumes bem desenhados. Uma nuca é feita de 2 a 4 penas
   grandes deitadas em telha, não de 12 cubinhos. Corte peças que não mudam a silhueta. Meta: 20 a 30% menos peças
   nas regiões amontoadas.
2. **Volumes arredondados por facetas.** Use `g.arredondado`, `g.arredondado2` e `g.octogono` (caixas com quinas
   chanfradas) para cabeça, pescoço, tronco, coxas e ombreiras, no lugar de caixas puras. Faça as transições com
   chanfros de 45° e degraus de no máximo ~1 unidade.
3. **Penas deitadas.** Penas e placas seguem a superfície: ficam quase tangentes, com 10 a 25° de abertura, e se
   sobrepõem como telhas. A mudança de ângulo de uma pena para a vizinha é pequena e gradual.
4. **Continuidade.** As peças vizinhas se encaixam, sem frestas nem quinas sobrando. A silhueta tem contorno
   limpo e linhas longas e contínuas.
5. **Textura que une.** Pinte o degradê e a luz atravessando o grupo de peças (base, luz em cima, sombra
   embaixo), não um contraste por cubo. A borda escura só fica no contorno externo do grupo.
6. **Confira de perto e de longe.** Olhe a 3/4, a foto do jogo e um render branco sem textura. Sem textura, a
   forma tem de parecer suave e orgânica, não uma pilha de blocos.

---

# Fase 7: OLHAR IMPONENTE (pedido do dono)

O dono pediu um rework dos olhos: "quero um olhar com mais imponência e menos síndrome de Down". O que ele rejeita é
o olhar bobo:
- olho redondo e arregalado, todo à mostra;
- pupila no meio de uma esclera grande;
- olhos parecendo "colados", desalinhados ou longe demais um do outro;
- sobrancelha solta acima do olho, sem cortar nada.

## Como fazer o olhar imponente (galo de briga, predador)
1. **Pálpebra pesada.** A sobrancelha/pálpebra corta o TOPO do olho numa diagonal que desce em direção ao bico (o V
   bravo). Só aparecem ~55–65% da altura do olho. A borda de baixo do olho é reta ou sobe levemente para trás.
2. **Olho estreito e alongado para trás**, mais largo que alto (cerca de 1,4 a 1,8 : 1), como a fenda de uma ave de
   rapina. Nada de círculo.
3. **Íris grande e forte**, ocupando quase todo o olho visível, na cor da ficha. A pupila fica perto da borda do lado
   do bico, olhando para a frente, com 1 px de brilho no alto. A esclera aparece só numa cunha atrás, ou nem aparece.
4. **Sobrancelha com volume**, saliente sobre o olho, em ângulo de 15–30°, terminando na base do bico. A sombra dela
   cai sobre o alto do olho (1 tom mais escuro no topo da íris).
5. **Posição.** Os olhos ficam nas faces laterais e diagonais da cabeça, no mesmo nível e simétricos, perto da base do
   bico. Não ficam no meio da cara nem longe do bico.
6. **Contorno.** Uma linha escura de 1 px no alto do olho (cílio/pálpebra) e nada de contorno grosso em volta.

Confira no close do rosto (`_rosto.png`) e na foto do jogo, de frente e a 3/4. O olhar tem de parecer sério, focado e
ameaçador, sem perder a expressão neutra da ficha.

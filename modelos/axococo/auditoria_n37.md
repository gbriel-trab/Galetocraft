# Auditoria de detalhes: Axococó (axococo), rodada n37

Fontes: ficha `008_axococo_{ficha,arte,vistas,detalhes,expressoes(neutra)}.png`; modelo `revisao/n37_{comp,vistas,3-4,rosto}.png`; foto do jogo `axococo_jogo.png`. Não existe `008_axococo_especificacao.md`. Métrica do comp: IoU médio 78,8%, cor/detalhe 44,2%.

## TOP 10 PROBLEMAS

**1. Brânquias: cor e desenho de cada fronde (frente, lateral, 3/4)**
- **Modelo:** cada brânquia é um feixe de bastões lisos, quase todos magenta-carmim escuro (~#C01C48), sobrepostos de forma desordenada. Parece um tufo/pompom, sem filamentos laterais.
- **Ficha (detalhe "Brânquias" e vistas):** cada brânquia é uma fronde em escada. O miolo é rosa claro (~#F4A8C0) e as pontas e o lado de baixo são rosa-choque (~#E8407A). Ao longo de toda a fronde há uma serrilha de filamentos curtos de 1 bloco, em cima e embaixo. O rosa claro domina; o magenta só contorna.
- **Correção:** refazer cada brânquia como uma haste de 2×2 blocos com degraus de 1 bloco (ficando cada vez mais fina para fora). Pôr 3 a 4 dentes de 1×1 alternados acima e abaixo da haste. Textura: face de cima e miolo em rosa claro #F4A8C0; face de baixo, ponta e dentes em #E8407A. Remover os bastões duplicados: 1 fronde limpa por brânquia.

**2. Brânquias: contagem, posição e ângulo (lateral e frente)**
- **Modelo:** na lateral há 5 ou mais bastões empilhados atrás da cabeça, e a crista se funde a eles. A brânquia de baixo desce na diagonal e atravessa a asa (bastão magenta sobre a asa, nas vistas laterais e na 3/4). Na frente elas saem do alto da cabeça e da altura da crista, formando uma juba.
- **Ficha:** são exatamente 3 por lado. Saem da lateral da cabeça, atrás do olho, entre a altura da sobrancelha e a da bochecha. A de cima vai para trás e um pouco para cima (~20°), a do meio vai na horizontal e a de baixo vai para trás e para baixo (~20°). A de baixo termina ACIMA do ombro e não encosta na asa. De frente, as três se abrem em leque: a de cima a ~45° para cima, a do meio na horizontal e a de baixo a ~30° para baixo. Há espaço escuro visível entre elas.
- **Correção:** deixar 3 brânquias por lado, com raiz no plano lateral da cabeça, 1 a 2 blocos atrás do olho, distribuídas do topo do olho até a base do bico. Usar os ângulos acima. Encurtar a de baixo para que a ponta fique ≥1 bloco acima do topo da asa. Deixar 1 bloco de folga entre as frondes.

**3. Cauda: forma das penas e altura (lateral e 3/4)**
- **Modelo:** 4 penas em arco de "C" que vão para trás e depois curvam para BAIXO e para DENTRO, em gancho na direção das pernas. O topo da cauda fica na linha do dorso.
- **Ficha (vistas laterais, arte e detalhe "Cauda Regenerativa"):** 4 a 5 lâminas largas em leque, levemente curvas. A de cima sobe acima do dorso, até a altura da brânquia de baixo (perto do nível do olho), e arqueia para trás. As outras se abrem para trás e para baixo, com as pontas apontando para fora e para trás. Nenhuma ponta volta para o corpo. Cada lâmina tem azul escuro (#1840A0/#2E70C8) na base e na borda interna e clareia até o azul-céu (#5AB0F0) na ponta.
- **Correção:** reangular os segmentos para uma curva aberta: pena de cima a +40° na base, terminando a ~0° e ~1 cabeça acima do dorso; as seguintes em −10°, −30° e −50°, todas com a ponta para trás e para fora. Remover o último segmento de gancho das penas de baixo. Alargar as lâminas para ~3 blocos na base, afinando para 2.

**4. Asa: volume e desenho de penas (lateral, frente, 3/4)**
- **Modelo:** a asa é uma laje retangular grande e plana, com placas horizontais, sem ponta definida. De frente forma "braços" verticais retos dos ombros até abaixo do peito.
- **Ficha:** a asa é uma gota arredondada: a frente é mais alta e cheia, e a traseira afina em degraus de rêmiges que descem para trás e para baixo, até a base da cauda. A borda de baixo traz uma fileira de penas em escada, em rosa médio (#EE7FA0) sobre rosa claro. De frente, as asas abraçam o peito arredondadas, mais largas no meio, e não são colunas retas.
- **Correção:** arredondar os cantos superior-traseiro e inferior-frontal da laje (cortar 1 a 2 blocos em escada). Acrescentar 3 degraus de rêmiges na traseira, cada um 1 bloco mais baixo e 1 a 2 blocos mais para trás, em rosa médio #EE7FA0. Na vista frontal, inclinar as asas 5 a 10° para fora embaixo e chanfrar os cantos de cima.

**5. Emblema espiral da asa: traço, cor, tamanho e posição (lateral)**
- **Modelo:** espiral redonda de traço fino (1 px de textura), azul-marinho escuro (~#1F4E9A), na metade de baixo da asa. A cauda do traço segue reto para a frente.
- **Ficha (vistas laterais e detalhe "Plumagem Úmida"):** espiral QUADRADA em voxel, como um "e"/"@", de traço grosso (~2 px, cerca de 1/4 da largura da espiral), azul médio vivo (#2E70C8, com toques #5AB0F0). Fica no centro da asa e ocupa ~40% do comprimento dela. A cauda do traço desce em curva para a frente e para baixo, acompanhando a borda inferior da asa. Na vista frontal a borda da espiral aparece como uma mancha azul em cada lateral.
- **Correção:** redesenhar a espiral com cantos retos e traço de 2 px em #2E70C8. Aumentá-la para ~40% do comprimento da asa e centralizá-la na vertical. Fazer o rabo da espiral descer em degraus até a borda inferior frontal. Estender 2 a 3 px de azul até a face frontal da asa.

**6. Olhos: esclera, pupila e íris (frente e lateral, contra a neutra)**
- **Modelo:** esclera cinza-clara, pupila pequena (~1/4 da largura do olho) e redonda, com anel dourado completo, mais para o centro. O contorno azul é marinho escuro, grosso e arredondado embaixo, em forma de "U".
- **Ficha (neutra):** esclera branca pura. A pupila é preta, grande (~1/2 da altura do olho), oval na vertical, encostada na borda do olho do lado do bico, com brilho branco de 1 px no alto. A íris âmbar/amarela aparece só como uma meia-lua embaixo da pupila. O contorno azul é azul-céu/médio (#3A8EE0), retangular e mais grosso na borda de trás e na de baixo. Em cima o olho é cortado pela pálpebra.
- **Correção:** esclera #FFFFFF. Pupila de 2×3 px encostada na borda frontal (do lado do bico), com 1 px branco no canto superior. Íris âmbar #E8A020 só na fileira abaixo da pupila. Moldura azul #3A8EE0 retangular de 1 px em cima e 2 px atrás e embaixo, sem arredondar.

**7. Sobrancelha/pálpebra (frente, 3/4, rosto)**
- **Modelo:** sobrancelhas são pranchas rosa soltas que saltam da cabeça. Na frente passam da largura da cabeça. Têm uma linha branca de contorno na aresta, visível em `_rosto` e `_3-4`.
- **Ficha:** a pálpebra é o próprio volume rosa da testa, rente à face, formando um "V" franzido que desce em direção ao bico e cobre o terço superior do olho. Não tem borda branca e não sai da silhueta da cabeça.
- **Correção:** recuar as pranchas para ficarem rentes (saliência máxima de 0,5 bloco) e dentro da largura da cabeça. Manter a inclinação para o bico. Tirar o px branco de borda da textura e usar o rosa da cabeça (#F4B0C8) com o lado de baixo em #EE7FA0.

**8. Bico: cor e perfil (frente e lateral)**
- **Modelo:** amarelo-ocre/mostarda escuro (~#D49A00). Na lateral o perfil é em escada ("S"): bloco de cima projetado e degraus recuando até a barbela. De frente o funil escalonado é alto demais e desce até dentro da barbela.
- **Ficha:** amarelo-alaranjado vivo (#F5B830), com o topo mais claro (#FFD040). Na lateral é uma cunha simples: maxila reta, levemente inclinada para baixo, ponta quadrada e narina escura no topo, com ~1/3 da profundidade da cabeça. De frente é um trapézio largo em cima (~1/3 da cabeça) que afina para baixo e para logo acima da barbela.
- **Correção:** trocar a textura por #F5B830, com face de cima #FFD040. Na lateral, unir os degraus num bloco-cunha: comprimento 3, altura 2 na base e 1 na ponta, sem recuos intermediários. De frente, reduzir a altura total em ~1 bloco para que a ponta termine onde as barbelas começam.

**9. Crista: forma, comprimento e cor (frente, lateral, costas)**
- **Modelo:** de frente é um bloco largo (~2/3 da largura da cabeça) e chato. Na lateral é uma laje longa que avança muito para trás, por cima das brânquias. Em volta da base há uma franja de plaquinhas rosa claro irregulares. Cor carmim avermelhado (#A0183C nas faces laterais).
- **Ficha (vistas e detalhe "Crista Aquática"):** de frente, coluna central estreita (~1/4 da cabeça) e alta (~3 blocos acima do topo), com 2 blocos laterais mais baixos (moicano em "trono"). Na lateral, 4 a 5 degraus de tamanhos diferentes ao longo do topo: o mais alto na frente/meio e a ponta de trás descendo, sem passar da nuca. A base sai limpa do topo rosa da cabeça. Cor rosa-choque (#E8407A), com topos mais claros.
- **Correção:** estreitar a coluna central para 2 blocos e subi-la 1 bloco. Baixar os laterais para ~2/3 da altura central. Na lateral, cortar a laje para que termine na nuca e quebrá-la em 4 degraus. Apagar as plaquinhas da base. Clarear a cor para #E8407A, com topo #F06090.

**10. Pernas e pés: cor e proporção (frente, lateral)**
- **Modelo:** pernas mostarda escuro (#D9A000), diferentes do pé, que é amarelo mais claro. As pernas são compridas e finas para o corpo.
- **Ficha:** perna e pé no mesmo amarelo-laranja (#F5B830). As pernas são curtas e grossas (largura ~1/2 da altura visível), e o pé é uma placa larga com 3 dedos frontais grandes em roxo-acinzentado (#5A4A60) mais o dedo traseiro.
- **Correção:** unificar perna e pé em #F5B830, com sombra #E0A020 só na face lateral. Encurtar a parte visível da perna em ~1 bloco ou engrossá-la +1 bloco. Manter os dedos.

## OUTROS PROBLEMAS MENORES
- Costas: na ficha a coluna da cauda vista de trás tem "ombros" azul-escuros (#1840A0) dos dois lados e o centro azul-céu. No modelo é uma grade uniforme azul-claro, estreita.
- Costas: crista vista de trás larga demais; na ficha é coluna estreita mais 2 laterais.
- Barbelas um pouco longas: na ficha medem ~1,3× a altura do bico, no modelo ~2×. Encurtar 1 bloco.
- Peito: na ficha as escamas creme terminam em ponta de "V" entre as pernas; no modelo a base é quase reta.
- Peito: as fileiras do modelo têm linhas rosadas fortes entre elas; na ficha a separação é sutil (creme #F8E4D8 com sombra #F0D0C8).
- Topo da cabeça na 3/4: espinhos/plaquinhas rosa claro soltos (artefatos) em volta da crista.
- Brânquias na foto do jogo parecem cachos enrolados; na ficha são retas e serrilhadas.
- Bochecha/face inferior: na ficha é rosa-creme quase branco, logo abaixo do olho; no modelo a faixa clara começa abaixo do contorno azul, com uma faixa rosa entre eles.
- Unhas: na lateral do modelo o dedo traseiro é uma placa listrada horizontal. Na ficha é um bloco liso roxo-acinzentado.

## O QUE JÁ ESTÁ FIEL
- Paleta geral correta (rosa/creme no corpo, crista e brânquias em rosa-choque, cauda azul em degradê, bico e pés amarelos, unhas roxo-acinzentadas).
- Barbela dupla vermelha, abrindo em "V" invertido sob o bico.
- Peito creme em fileiras escalonadas, contrastando com os flancos rosa.
- Pés com 3 dedos frontais escuros e um traseiro, como na ficha.
- Olho com moldura azul e expressão franzida (conceito certo; o desenho precisa de ajuste).

## NOTA DE FIDELIDADE AOS DETALHES
**5/10.** Dos 10 problemas principais, **4 são de rosto/cabeça**: olhos, sobrancelha/pálpebra, bico e crista. As brânquias (1 e 2) também ficam na cabeça e são o detalhe mais característico da espécie. Contando com elas, são 6.

# Auditoria de detalhes, rodada 2: Morcegalo (`morcegalo`, n32)

Fontes: ficha `010_morcegalo_{ficha,arte,vistas,detalhes,expressoes}` (só a expressão Neutra), renders `revisao/n32_*`, foto do jogo `fotos_jogo/morcegalo_jogo.png` (peso maior) e Esporocó (`esporoco_jogo.png`) como régua.
Régua: no Esporocó, de perto no jogo, o bico, a crista, os olhos e a flor são lidos na hora, com a forma e a cor da ficha. No Morcegalo, a foto mostra que o rosto e os elementos-assinatura (bico, crista, peitoral, cauda) ainda não chegam lá.
Nota sobre a cor: na foto, o roxo escuro do corpo sai quase igual ao da ficha (#45256c contra #3a1e65), então a luz do jogo é neutra. As diferenças nos tons claros e rosados abaixo são de textura, não de luz.

## TOP 10 PROBLEMAS

### 1. Bico: um "cano" reto, comprido e cinza-taupe no lugar de um bico de rapina curto e curvo (rosto; frente, lado, foto)
- **Modelo:** dois blocos empilhados formam uma placa vertical retangular que sai da linha dos olhos e desce até o topo do peitoral. O bloco de baixo é mais estreito e passa por cima das barbelas. Não afina, não tem gancho nem narina. A face da frente é taupe acinzentado (#957771) e só a aresta de cima é clara. Na foto de frente, parece uma tromba ou um focinho de anta. De lado, é uma caixa reta com degrau.
- **Ficha:** bico curto de rapina, creme-rosado (#fcd8b9 a #f8c0be). De frente, é largo na base (~1/3 da largura da cabeça) e afina para baixo até uma ponta única. A altura total é ~1/3 da altura da cabeça e termina pouco abaixo da base dos olhos. De lado, sai ~1/4 da profundidade da cabeça para a frente e a ponta curva para baixo, num gancho. Tem uma narina escura de 1 px no alto da lateral.
- **Correção:** apagar o bloco inferior. Refazer o bico em 3 degraus: base com ~1/3 da largura da cabeça e 2 px de altura, meio 2 px mais estreito, ponta de 1–2 px recuada e 1 px mais baixa, curvando para baixo (gancho). Comprimento para a frente de ~3 px e ponta no máximo 1 bloco abaixo da linha inferior dos olhos. Textura: topo #fcd8b9, frente #f2c4b4, lateral #e0aaa0 (nunca taupe ou cinza). Narina de 1 px #614749 no alto de cada lateral. As barbelas devem aparecer inteiras abaixo do bico.

### 2. Crista: um palito fino no lugar do grande leque magenta (cabeça; frente, lado, foto)
- **Modelo:** de frente, uma única coluna de 1–2 px de largura no meio do topo, que parece uma antena ou um chifre. De lado, uma fileira serrilhada baixa, cor framboesa escura (#b0306a), quase escondida atrás das orelhas. Na foto de frente quase não aparece; na foto de trás aparece só um tufo pequeno.
- **Ficha:** crista grande e protagonista, entre as orelhas. De frente, é uma torre de 3 degraus: base larga (~1/4 da largura da cabeça), meio mais estreito e topo de 2 px, com altura ~1/2 da cabeça. De lado (Neutra e arte), é um leque de blocos em escada que nasce na testa, sobe e cai para trás por cima do crânio, ocupando ~2/3 do comprimento do topo da cabeça. Magenta vivo #d742a2 / #d75197, com topo dos blocos em rosa claro #e888c8.
- **Correção:** alargar a crista na frente para 4 px na base, 3 px no meio e 2 px no topo, com ~6–7 px de altura acima do crânio. De lado, fazer 4–5 degraus que começam acima dos olhos e descem para trás até a nuca: o mais alto é o 2º a partir da frente e cada degrau seguinte fica 1 px mais baixo. Cor base #d75197, faces de cima #e888c8 e sombra #a83a78. Ela precisa aparecer por inteiro entre as orelhas na vista frontal da foto.

### 3. Olhos: pequenos, amarelo-pálido, sem brilho (rosto; frente, foto)
- **Modelo:** olho com ~15% da largura da cabeça, esclera amarelo-claro pálido, íris marrom-avermelhada escura e pupila preta. Não tem ponto de brilho. Na foto, os olhos parecem duas fendas pequenas nos cantos.
- **Ficha (Neutra):** olho grande, com ~25% da largura da cabeça (quase do tamanho do bico), amarelo-ouro saturado #fdb804 clareando para #fdebc1 perto da íris. Íris laranja-avermelhada com pupila escura e um ponto branco de brilho no alto, perto do bico. A pálpebra ou sobrancelha corta reto o terço de cima, dando o olhar "semicerrado e vigilante".
- **Correção:** aumentar o olho para ~1,7× (de ~3 para ~5 px de largura e de ~2 para ~3–4 px de altura), mantendo o canto interno colado à base do bico. Pintar a esclera de #fdb804 com borda inferior #fdebc1 e a íris de #d0441a, com pupila de 2 px #2a0e10 e 1 px branco #ffffff no canto superior interno. Cortar a linha superior do olho reta e inclinada para dentro, já sob a sobrancelha (ver 4).

### 4. Sobrancelha e testa: linhas finas no lugar do "capacete" carrancudo em V (rosto; frente, foto)
- **Modelo:** de longe, a sobrancelha é só um traço claro de 1 px que sobe para fora. Os blocos de sobrancelha do render de rosto têm a mesma cor da cabeça e somem na foto. A testa é uma face lisa: a cabeça parece uma caixa.
- **Ficha:** uma placa grossa de sobrancelha em V forte, com o vértice sobre o bico. Ela se projeta para a frente sobre o olho, cobre o terço de cima do olho e desce em diagonal até o bico. Logo acima vem uma testa em degrau (capacete) com bordas chanfradas. Abaixo dos olhos, uma "bochecha" de bloco mais claro (#8c55b8).
- **Correção:** fazer as sobrancelhas como 2 blocos de 2 px de altura que saem 1 px da face, inclinados ~25° para baixo em direção ao bico e encostando na base da crista. Pintar o topo #8c55b8 e a face de baixo #2a1450, com uma linha de sombra #2a1450 na textura logo acima do olho. Apagar o traço claro de 1 px. Acrescentar uma faixa de bochecha #8c55b8 de 2 px sob cada olho, indo até a lateral da cabeça.

### 5. Peitoral: triângulo liso com "tijolinhos" no lugar das escamas em chevron (peito; frente, foto)
- **Modelo:** um triângulo invertido chapado, lilás acinzentado (#9c74a2), cortado por linhas escuras de 1 px em padrão de parede de tijolo. Em cima há um retângulo roxo-médio quadrado. Não tem relevo nem pontas. Na foto, parece um avental de azulejo.
- **Ficha ("Peitoral Sombrio"):** uma gola larga de penas-escama que vai quase de ombro a ombro logo abaixo das barbelas e afunila até uma ponta a ~2/3 da barriga. Tem 3–4 fileiras de placas em V (chevron) com bordas inferiores serrilhadas. Cada fileira se sobrepõe à de cima e sai em relevo. Cores: lilás muito claro #e8baf0 / #f7d0fb nas faces e #c08be8 nas sombras, com algumas placas roxo-médio #8c55b8 nas bordas.
- **Correção:** remover a textura de tijolo. Montar o peitoral com 4 fileiras de cubos de 1 px de espessura, cada uma 1 px à frente da de cima. A 1ª fileira é a mais larga (~80% da largura do peito) e cada uma seguinte perde ~2 px por lado. As bordas inferiores ficam em dente de serra (V de 2 px a cada 3 px). Textura: face #e8baf0, topo #f7d0fb, borda inferior #c08be8. Nas laterais da 1ª e 2ª fileiras, intercalar placas #8c55b8.

### 6. Plumagem do corpo: "almofadas" empilhadas no lugar de penas em camadas (corpo e flancos; frente, lado, foto)
- **Modelo:** o tronco é um cilindro de blocos roxo-escuros retangulares empilhados em fileiras horizontais retas, como sacos ou armadura acolchoada. Embaixo há uma barra de franja azul-violeta saturada (#6a48c8). Os flancos são uniformes, sem pontas de pena nem destaques claros.
- **Ficha:** penas em camadas com pontas para baixo, em escada diagonal. Base #3a1e65 e pontas #8c55b8, com algumas pontas lilás #c08be8 nos flancos e coxas (vistas lateral e traseira). A silhueta do corpo é em pera, com peito projetado para a frente. Não existe barra azul.
- **Correção:** em cada fileira de blocos do flanco, pintar a borda inferior como ponta de pena (V de 2 px #8c55b8 sobre base #3a1e65) e desencontrar as fileiras em meio bloco. Uma em cada 3 pontas recebe 1 px #c08be8. Trocar a barra inferior #6a48c8 por pontas de pena #8c55b8 sobre #3a1e65. Avançar o volume do peito 1–2 px na vista lateral.

### 7. Cauda: tubos quadrados com "nós de dedo" cinzentos no lugar das penas-foice curvas (cauda; lado, trás, foto)
- **Modelo:** a cauda é uma pilha de prismas retos e grossos com pontas quadradas, terminados em cubinhos escalonados que parecem dedos ou juntas. Há faces cinza (#a09aa8 / #c8c0c8) que não estão na paleta. As penas não afinam nem curvam: na foto lateral parece um punho fechado. De trás, aparece uma coluna central branco-acinzentada segmentada.
- **Ficha ("Cauda Escura"):** 5–6 penas-foice longas em leque que sobem, arqueiam para trás e caem. Cada pena afina até uma ponta curva e fina. Gradiente da base à ponta: roxo vivo #8c55b8, depois violeta #b352b9, lilás #e8baf0 e ponta creme-rosada #fab6b6 / #fcd8b9. De trás, a pena central é listrada roxo/lilás e termina em ponta creme abaixo da barriga.
- **Correção:** refazer cada pena com 3–4 segmentos que diminuem 1 px de espessura a cada segmento (de 3×3 até 1×1 na ponta). Girar cada segmento 15–20° a mais que o anterior para formar o arco. Apagar os cubinhos "dedo" laterais. Pintar seguindo o gradiente acima e remover todo o cinza. Na pena central de trás, listras alternadas #8c55b8 / #c08be8 a cada 2 px e ponta de 2 px #fcd8b9.

### 8. Asas: dedos que pendem abaixo da membrana com "unhas" creme, membrana listrada e com franja branca (asas; frente, trás, foto)
- **Modelo:** as varetas dos dedos passam bem da borda da membrana e terminam em 5 cubinhos creme pendurados por asa, que parecem perninhas penduradas. As asas descem quase até a altura das pernas. A membrana tem faixas concêntricas paralelas à borda (rosa com listras mais claras) e uma franja rosa-esbranquiçada ao longo do recorte.
- **Ficha ("Asa Membranosa"):** braço roxo grosso no bordo de ataque, com um "pulso" arredondado no alto, e 2–3 dedos que terminam exatamente nas pontas do recorte. A borda inferior tem 3 pontas recortadas e só as pontas da membrana (e a ponta externa) são creme #fcd8b9. Nada fica pendurado abaixo. A ponta mais baixa fica na altura da barriga. A membrana é um gradiente liso do magenta #d75197 junto ao braço até o rosa claro #e888c8 nas pontas, sem listras e sem franja branca.
- **Correção:** encurtar cada dedo para terminar na ponta do recorte e apagar os cubinhos creme pendurados. Pintar só os 2 px finais de cada ponta do recorte de #fcd8b9. Subir a asa ~1/4 da altura do corpo, para a ponta mais baixa ficar na linha da barriga. Repintar a membrana em gradiente de 3 tons (#b352b9 junto ao braço, #d75197 no meio, #e888c8 perto da borda), apagando as listras e a franja clara. Fazer um "pulso" de 2×2 px no cotovelo do braço.

### 9. Orelhas: placas planas (somem de lado) com interior rosa desbotado (cabeça; lado, rosto, foto)
- **Modelo:** de frente o tamanho está bom, mas a orelha é uma placa de espessura zero. Na foto lateral ela vira um palito roxo, e no render de rosto só aparecem as duas varetas da borda. O interior é rosa-mauve desbotado (#aa6a98) e a borda roxa é fina.
- **Ficha ("Orelhas Noturnas"):** orelha em concha com volume. De lado (vista lateral e Neutra), o interior rosa continua visível, voltado para a frente e para o lado. A borda roxa é grossa (~1/5 da largura da orelha). O interior é rosa-magenta vivo #d153ab com blocos em degrau mais claros #e888c8. De trás, a orelha é roxa maciça com a borda de baixo em escada.
- **Correção:** dar 2 px de espessura à orelha. Fazer a borda roxa com 2 px de largura e o interior rebaixado 1 px (concha), girando a orelha ~25° para a frente, para o interior aparecer na lateral. Repintar o interior com #d153ab e degraus #e888c8 e a borda com #5a2f92 / topo #8c55b8. Fazer a borda de baixo em escada de 2 px na face de trás.

### 10. Tons claros e rosados desbotados em todo o modelo (paleta; foto)
- **Modelo:** todos os tons quentes e claros ficaram acinzentados ou escurecidos. Bico #957771 (ficha #fcd8b9), peitoral #9c74a2 (#e8baf0), interior da orelha #aa6a98 (#d153ab), membrana #90316d (#b352b9 / #d75197), barbela #98396f (#c23e93), pernas #af8d83 (#fcd8b9 / #ce8894). Como o roxo escuro sai correto na mesma foto, o desbote é da textura.
- **Ficha:** paleta oficial #3a1e65, #8c55b8, #c08be8, #e8baf0, #d75197, #fcd8b9, #fdb804 e #614749. Rosas e lilases vivos contra o roxo escuro: é esse contraste que dá o visual "neon na sombra".
- **Correção:** trocar cada tom claro ou rosado da textura pelo valor da paleta listado acima, sem multiplicar por cinza. Conferir na foto do jogo que o peitoral é a área mais clara do corpo e o bico a segunda.

## OUTROS PROBLEMAS MENORES
- Barbelas: tiras finas e compridas cor framboesa que escorrem pelo peitoral. Na ficha são 2 lóbulos curtos e largos #c23e93 / #d75197, cada um com ~metade da largura do bico, terminando no topo do peitoral.
- Há 1 pixel branco solto espetado no topo do bico (vista frontal) e uma linha clara de 1 px na base do bloco inferior do bico.
- Nuca e costas: a cabeça de trás é uma caixa lisa. A ficha tem um "boné" com aba saliente de 1 px na base do crânio, sobre o pescoço.
- Falta a gola de penas do pescoço (hackle) em violeta e lilás entre a cabeça e o peitoral (arte, Neutra): pontas #8c55b8 / #c08be8 nas laterais do pescoço.
- Pernas um pouco finas e cor taupe #af8d83. A ficha tem tarso mais grosso (~1,3×) e #fcd8b9, com a "calça" de penas cobrindo o topo.
- Garras: os blocos escuros das garras quase do tamanho do dedo. Na ficha têm ~2/3 do comprimento do dedo, cor #3a1e65 ou #614749.
- Barra azul-violeta (#6a48c8) na barra inferior do tronco e no topo das coxas: não existe na ficha.
- Vista traseira: faixa central branco-cinza na base da cauda (cinza fora da paleta).
- Membrana das orelhas invisível no render `_rosto` (falta face traseira ou volume, ver item 9).

## O QUE JÁ ESTÁ FIEL
- Silhueta geral de frente (IoU 78%): orelhas grandes no topo, asas abertas e tronco atarracado.
- O roxo escuro base do corpo bate com a ficha.
- A estrutura da asa (braço grosso, varetas de dedos e borda recortada) está presente.
- Os pés de 3 dedos creme com garras escuras e a posição das pernas estão certos.

## NOTA DE FIDELIDADE AOS DETALHES
**5/10.** 4 dos 10 problemas são de rosto e cabeça (1 bico, 2 crista, 3 olhos, 4 sobrancelha), e a orelha (9) também é da cabeça. Para chegar ao nível do Esporocó, os itens 1, 2, 3 e 5 são os que mais pesam na foto do jogo.

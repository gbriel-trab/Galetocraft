# Cocórion #005: reconstrução geométrica (pedido do dono, 2026-11-11)

Este pedido complementa `005_cocorion_especificacao.md`, que continua valendo. A arte oficial (a ficha) é a referência
obrigatória e tem prioridade sobre qualquer número daqui.

**Diagnóstico do dono:** o modelo atual parece quadrado demais, disforme, rígido e construído com cubos
desconectados. Ele pede **reconstrução estrutural da geometria**, não retoque de posição ou textura: "os defeitos
são principalmente geométricos". A diferença em relação ao modelo atual tem de ser significativa.

## 1. Direção artística
O alvo é um "voxel orgânico e refinado", no nível de criatura bem feita do Cobblemon, sem copiar nada. Para isso:
- cuboides menores e sobrepostos;
- peças rotacionadas;
- volumes escalonados com transições suaves;
- silhuetas angulares cuidadosas;
- penas de base larga e ponta afilada;
- profundidade real, sem superfícies planas sem espessura com detalhe só pintado.

Não pode virar humanoide, boneco arredondado ou algo realista. Qualidade geométrica vale mais que quantidade:
nada de centenas de cubinhos inúteis.

## 2. Silhueta primeiro
Sem textura, deve dar para ler cada parte:
- cabeça de galo com crista longa e espetada;
- pescoço integrado ao tronco;
- peito desenvolvido, sem ser caixa;
- cintura estreita;
- duas asas grandes nas laterais;
- cauda alta, larga e curvada;
- pernas relativamente finas e patas bem definidas.

Ele deve parecer veloz, leve, atlético e ameaçador, nunca pesado, robótico ou artificial.

## 3. Cabeça
- O crânio é largo em cima, para sustentar a crista, e afina gradualmente até o bico.
- O rosto é feito de PLANOS INCLINADOS, não só de faces frontais retas.
- Ficam: olhos verdes, sobrancelhas pretas grossas, bico amarelo angular, barbelas, cicatrizes do rosto e a marca
  da testa.
- As sobrancelhas acompanham o volume da cabeça, um pouco à frente dos olhos.
- Os olhos ficam integrados ao rosto, não como dois adesivos numa caixa.

## 4. Crista (problema mais evidente)
Hoje parece uma pilha de peças empilhadas na vertical, simétrica e fragmentada.

**Construção nova:**
- POUCAS mechas principais grandes e pontudas, mais algumas secundárias menores.
- Cada mecha:
  - nasce de uma base integrada ao crânio;
  - é larga no início e afina progressivamente até a ponta;
  - tem inclinação própria;
  - sobrepõe parte das vizinhas;
  - forma com elas um volume contínuo.
- Não usar dezenas de bloquinhos desconectados para fazer uma única pena.

**Por vista:**
- As mechas de cima e de trás vão para trás e na diagonal para cima.
- De lado: uma sequência fluida de penas varridas para trás.
- De frente: composição irregular, com assimetria controlada como na arte. Nada de espelho perfeito.

## 5. Tronco
Hoje é uma caixa branca reta. O certo é um corpo de ave estilizada:
- ombros mais largos;
- tórax com leve projeção para a frente;
- peito volumoso, de facetas inclinadas que formam um contorno arredondado;
- laterais que convergem para uma cintura estreita;
- abdômen meio coberto pela plumagem e pelo traje;
- transições suaves entre pescoço, peito e cintura.

O tronco é UM volume anatômico com camadas de penas por cima. O X vermelho continua, adaptado às facetas: não
achatar o peito para pintar o X.

## 6. Asas
Hoje são placas grandes, retas e rígidas. Devem ficar VISUALMENTE MAIORES, mais fluidas e parecidas com a arte, em
três regiões:
- **Base:** nasce no ombro, grossa, com transição natural para o tronco.
- **Meio:** penas sobrepostas que descem pelas laterais, com uma leve curva no contorno.
- **Ponta:** penas alongadas e pontudas, de comprimentos um pouco diferentes. Termina em várias pontas
  afiladas, não em retângulos largos.

Elas têm espessura real, mas não parecem placas. A espiral verde fica na face externa, acompanhando a geometria. Na
pose neutra ficam junto ao corpo, como uma capa. Sem mãos nem braços.

## 7. Cauda
Hoje tem bom volume, mas está fragmentada em segmentos desconectados.

**Forma:**
- Base estreita atrás do corpo, que se abre para trás e para cima.
- Penas principais longas e contínuas, num leque 3D com curva ascendente.

**Cada pena:**
- base ligada ao corpo;
- volume contínuo;
- curva progressiva;
- largura variável;
- ponta afilada;
- sobreposição com as vizinhas.

Para fazer a curva, use cuboides inclinados e escalonados com degraus PEQUENOS, sem frestas entre os segmentos.

**Cor e vista lateral:** mantenha a alternância verde-escuro/creme. De lado, um arco ascendente harmonioso, sem
escada nem cara de máquina. A cauda é grande, mas não mais importante que a cabeça e o tronco.

## 8. Cintura, traje e pernas
- **Traje:** hoje é um conjunto de caixas. Refaça com painéis um pouco inclinados e sobrepostos, com pregas em
  voxel (hakama estilizada). Não pode ficar largo demais nem parecer uma bermuda quadrada.
- **Cintura:** transição clara com o peito.
- **Pernas:** nascem do corpo, sem parecer pilares amarelos presos numa caixa. Anatomia de ave, longas o bastante
  para não parecerem atrofiadas.
- **Patas:** amarelas, com garras escuras, largas e estáveis.
- **Katana:** no mesmo lugar da arte.

## 9. Proporções e escala
**Máximos:**
| Medida | Blocos | Unidades |
|---|---|---|
| Altura | 2,0 | 32 |
| Largura | 1,6 | ~25,6 |
| Comprimento | 2,4 | ~38,4 |

Os máximos incluem crista, asas, bico e cauda. Não aumente tudo artificialmente: a melhora vem de distribuir bem os
volumes.

**Relações:**
- peito mais largo que a cintura;
- cabeça proporcional;
- crista alta, sem dominar;
- asas até a parte de baixo do traje;
- cauda grande.

## 10. Conferência obrigatória (4 vistas)
- **Frente:** simetria anatômica, peito, cabeça, crista, asas e pernas.
- **Lateral direita:** inclinação da crista, projeção do peito, espessura das asas, bico e curva da cauda.
- **Traseira:** volume da cauda, união das penas, largura do corpo e posição das asas.
- **Lateral esquerda:** coerência anatômica e acessórios no lugar.

O critério principal é a fidelidade da silhueta 3D à arte. Textura certa não basta.

## 11. Não fazer
- tronco em caixa;
- crista em pilha de cubos;
- asas em placas retas;
- cauda em segmentos desconectados;
- pernas em pilar;
- humano com cabeça de galo;
- cauda menor;
- tirar detalhes originais;
- geometria realista;
- mudar a paleta;
- adicionar elementos não aprovados.

## 12. Entrega
Quatro vistas ortográficas e uma vista em perspectiva: `_vistas.png` e `_3-4.png` da rodada final.

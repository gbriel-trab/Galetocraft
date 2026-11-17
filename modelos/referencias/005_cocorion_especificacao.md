# Cocórion #005 (Ar): especificação oficial do dono

Este resumo segue o texto que o dono mandou em 2026-11-11.

**A imagem oficial (as fichas em `005_cocorion_*.png`) tem prioridade sobre qualquer número daqui.** Não redesenhe
nem reinvente: transforme o personagem da ficha num modelo 3D fiel. As 4 vistas são o mesmo personagem, em perfeita
continuidade.

Estilo: voxel do Minecraft, com acabamento de criatura do Cobblemon (sem usar nada do Cobblemon). Use volumes
cúbicos, formas escalonadas, penas poligonais com espessura e textura pixelada.

## 1. Dimensões (extensão visual máxima, não a hitbox)
| Medida | Blocos | Unidades (16 por bloco) |
|---|---|---|
| Altura (chão até a ponta da crista) | 2,0 | 32 → `ALTURA = 2.0` |
| Largura (corpo + asas + penas laterais) | 1,6 | ~25,6 |
| Comprimento (bico até a ponta da cauda) | 2,4 | ~38,4 |

- Corpo estreito, postura ereta, pernas visíveis.
- Silhueta marcada pela crista espetada e pela cauda grande.
- Deve parecer ágil, leve e agressivo, nunca robusto nem pesado.
- A maior parte do comprimento para trás vem da CAUDA. Não alongue o corpo.

### Faixas verticais iniciais (em blocos, a partir do chão)
Ajuste à imagem, principalmente a cabeça, a crista e as asas.

| Região | Faixa |
|---|---|
| Pés | 0,00–0,20 |
| Pernas visíveis | 0,20–0,54 |
| Traje e cintura | 0,54–0,98 |
| Tronco e peito | 0,98–1,42 |
| Pescoço e cabeça | 1,42–1,72 |
| Topo da crista | 1,72–2,00 |

## 2. Cabeça e crista
**Cabeça:** de galo estilizado, rosto estreito e angular, penas claras em camadas.

**Crista (o elemento mais importante):**
- Grande, irregular e muito espetada, feita de mechas rígidas e pontudas de penas.
- Cores: branco e creme, com sombra cinza-claro.
- As pontas vão principalmente para cima, para trás e na diagonal.
- A frente é mais baixa, numa linha irregular perto da testa; o topo e a parte de trás são altos.
- Cada mecha: volumes sobrepostos, base grossa e ponta afilada em degraus.
- NÃO é uma crista vermelha de galo.
- A nuca tem camadas de penas que continuam no pescoço.

**Olhos:**
- Verdes intensos, estreitos e levemente inclinados.
- Sobrancelhas pretas ou cinza-carvão, grossas e angulares, baixas e projetadas para a frente.
- Expressão séria, confiante e intimidadora.

**Marcas vermelhas (só as que existem na ficha):**
- uma pequena cruz na testa;
- cicatrizes irregulares nas laterais do rosto.

Preserve a posição, a espessura e o formato.

**Bico:** amarelo-dourado, angular e robusto, horizontal para a frente, com a ponta levemente para baixo. É
compacto, sem exagerar no comprimento.

**Barbelas:** vermelhas, alongadas, divididas em volumes e pendendo na vertical sob o bico.

## 3. Pescoço, peito e tronco
- O pescoço é estreito e alarga até os ombros.
- O tronco é branco-creme, com penas sobrepostas, sombra cinza-claro entre as camadas e pontas das penas em
  pequenas saliências geométricas.
- O peito tem volume moderado: forte, mas esguio.
- Há um X vermelho grande no peito, irregular como cicatrizes cruzadas, com pequenos detalhes escuros. Ele
  continua visível de frente mesmo com as asas.
- Nada de armadura nem roupa nova cobrindo a plumagem.

## 4. Asas (a segunda estrutura mais importante)
**Não há braços humanos nem mãos.** As asas ficam no lugar dos braços.

**Forma:**
- Grandes, compridas e angulares, junto aos lados do tronco.
- Nascem no alto dos ombros e descem pelas laterais como uma capa de penas.
- Várias camadas de penas longas: base larga e ponta estreita.
- A borda de baixo termina em várias pontas geométricas.

**Cores:**
- branco e creme, com sombra cinza-claro;
- detalhes internos em verde-escuro;
- uma espiral ou redemoinho verde-escuro na face externa de cada asa, bem legível. A espiral acompanha a forma
  da asa (não é um decalque plano flutuando fora dela).

**Proporções:**
- Começam nos ombros e terminam perto da parte de baixo do traje, sem arrastar no chão.
- A envergadura total é de ~1,6 bloco.
- O corpo continua visível entre as asas na vista de frente.

**Ossos:** asas separadas e articuláveis (`asa_d` e `asa_e`), para animar movimento, defesa e ataque.

## 5. Cauda (grande, curvada e em camadas)
**Forma:**
- Volumosa e longa, um leque curvado para cima e para trás.
- Nasce embaixo e atrás do tronco, com a base estreita.
- As penas se abrem para trás e para os lados, numa curva ascendente evidente.
- As pontas são grandes, angulares e separadas.
- As penas se sobrepõem em alturas diferentes, de forma escalonada.

**Cores:**
- verde-escuro por dentro e nas faixas das penas;
- branco-creme por fora e nas pontas;
- sombra em verde profundo e cinza.

Siga exatamente a alternância verde/creme da ficha.

**Por vista:**
- Volume 3D real, não uma placa texturizada.
- De lado: a curva para cima é clara.
- De trás: aproximadamente equilibrada.
- Ocupa boa parte dos 2,4 blocos de comprimento. Não reduzir a um tufo.

## 6. Cintura, traje e katana
**Traje:**
- Preto ou cinza-carvão, tipo hakama curta e pregueada.
- Cintura ajustada; embaixo, mais larga, em painéis verticais com pregas geométricas.
- Termina acima da maior parte das pernas.
- Faixas ou tiras claras pendem do centro da cintura, como na ficha.
- Geometria cúbica: nada de tecido arredondado ou ondulado.

**Katana pequena na cintura:**
- cabo verde-escuro, com um padrão geométrico claro;
- guarda angular dourada;
- detalhes escuros na bainha;
- compacta.

Mantenha o lado, a inclinação e a posição da ficha: de frente, fica à direita de quem olha. Ela tem um osso
próprio (`katana`), separado das asas.

## 7. Pernas e patas
**Pernas:** duas, relativamente longas, amarelo-douradas, retangulares, firmes (sem ser grossas demais), bem
separadas e visíveis abaixo do traje.

**Patas:**
- grandes em relação à perna, cúbicas e angulares;
- dedos robustos e separados, com garras pretas ou cinza-carvão;
- topo amarelo;
- encostadas no chão, sem flutuar;
- não são sapatos.

## 8. Paleta (ajuste os tons exatos à imagem)
| Cor | Onde |
|---|---|
| Branco-creme (predominante) | cabeça, crista, peito, asas |
| Cinza-claro | sombra e separação das penas |
| Cinza-carvão e preto | sobrancelhas, traje, cintura, acessórios escuros, garras |
| Verde-escuro | espirais das asas, dentro da cauda, cabo da katana |
| Verde intenso | íris |
| Amarelo-dourado | bico, pernas, patas, guarda da katana |
| Vermelho vivo | barbelas, cruz da testa, cicatrizes do rosto e do peito |

Nenhuma cor fora dessas.

## 9. Organização
**Grupos:**
- root e corpo;
- `pescoco`, `cabeca`, `crista` e penas do rosto;
- bico e barbelas;
- `asa_d` e `asa_e`, com as penas de cada asa;
- `cauda` e os grupos de penas;
- traje e cintura;
- `perna_d` e `perna_e`, com os pés;
- `katana`.

**Pivôs:** na base do pescoço, nos ombros, nas articulações das pernas e na raiz da cauda.

**Penas:** com volume geométrico (cuboides e planos com espessura, em ângulos diferentes). Sem virar uma massa de
cubos indiferenciados.

**Contagem:** a prancha tem ~86 cubos principais + 24 extras (~110). É uma referência, mas a fidelidade da
silhueta vem antes.

## 10. Conferência das 4 vistas
- **Frente:** crista irregular, sobrancelhas escuras, olhos verdes, bico amarelo, barbelas, marcas do rosto, X no
  peito, asas com espirais verdes, traje escuro, patas amarelas com garras pretas.
- **Lateral direita:** projeção do bico, inclinação para trás das penas da cabeça, volume das asas, katana e curva
  ascendente da cauda.
- **Traseira:** penas brancas sobrepostas no dorso, asas, centro da cauda e abertura das penas grandes verdes e
  creme.
- **Lateral esquerda:** continuidade, camadas de penas, volume traseiro e as marcas e acessórios como na ficha.

## 11. Proibido
- braços ou mãos humanos;
- cabelo humano;
- armadura ou acessórios que não existem na ficha;
- mudar a cor dos olhos;
- crista vermelha tradicional;
- tirar as espirais verdes;
- reduzir ou trocar a cauda;
- mudar as cicatrizes, o padrão das penas ou os acessórios;
- anatomia arredondada realista;
- usar personagens de outras franquias;
- galo genérico.

## 12. Identidade, em ordem
1. Crista branca grande e espetada.
2. Olhos verdes com sobrancelhas pretas bravas.
3. Cicatrizes vermelhas no rosto e no peito.
4. Asas longas brancas com espirais verdes.
5. Cauda grande verde e creme, curvada em camadas.
6. Traje preto e katana.
7. Pernas e patas amarelas com garras escuras.

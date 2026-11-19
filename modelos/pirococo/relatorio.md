# Pirococó (#001): relatório do modelo

## Estado atual (correção 2)

- **Cubos:** 171 (orçamento desta rodada: até 190): 85 caixas e 86 planos.
- **Cubos girados:** 21 (12%).
- **Penas:** cada pena da crista e da capa tem o seu osso (114 ossos).
- **Textura:** 128×128, 1 px por unidade, 32 cores da paleta.
- **Altura:** de 0 a 45,2 u.
- **Capa:** borda de trás em z 12,0 (limite 13,5) e largura máxima de 25,8 u.
- **Tranças:** pontas em (x 0; y 5,1; z 18,8) na central e (x ±5,9; y 11,1; z 18,6) nas laterais.
- **Folgas nos laços** (8 instantes do idle e 8 do walk):
  - chão: −0,01 u;
  - capa × pernas: ≥ 0,75 u;
  - capa × tranças: ≥ 0,47 u.

## Correção 2: item → mudança → estado

1. **Capa — resolvido.**
   - Penas de 5 px num anel em volta do tronco: 4, 5 e 6 por lado nas fileiras 1, 2 e 3, mais 3 por fileira no leque das costas.
   - A 1ª de cada lado fica na frente do flanco (x ±5, z −7,3; 30° em y e 25° de leque para fora).
   - Giro em y das laterais entre 30° e 65° ou entre 115° e 155°, a ≥ 25° de perfil.
   - Pontas em V com degraus de 1 px. A fileira 1 tem filete prata; nas outras, o roxo vai até 75% e 45% do comprimento.
   - Penas vizinhas alternam claro e base.
2. **Juba — resolvido.**
   - 20 planos com base de 5 px (os tufos de bochecha, 3 px): 2 penas em U (curvas para dentro, 20° para trás), a central, 3 chamas por lado (30°, 50° e 70° em z, 25° para trás), 3 chamas do leque de trás, 4 lâminas na nuca (−15° a −55°) e 2 tufos por lado.
   - **Diferença:** o pedido era de 14–16 planos. As 3 chamas de trás preenchem o leque visto de costas.
   - As penas que ficam de frente também giram 15–25° em y, para não virarem fio de perfil.
3. **Cauda com gravidade — resolvido.**
   - A central tem 8 segmentos (dobras de 0°, 0°, 15°, 15°, 20°, 20°, 15° e 3°); as laterais, 6 segmentos mais a lâmina, chegando a ~85°.
   - Cordão pintado com sulco em diagonal, sem xadrez.
   - Lâmina de chama 4×8 em X, com losango em brilho dos dois lados.
   - Pêndulo de ±3° em z e ±2° em x no idle, e ±6° no walk.
4. **Ombreiras — resolvido.** Concha 6×3×7 + chanfro 5×1×5, giradas 20°. Aba frontal a −10°. Ponta dourada 3×1×3 a 45°. Miolo roxo no topo e na frente.
5. **Elmo e cabeça — resolvido.**
   - Faixa 1×2×7 colada na lateral, subindo 15° para trás, e aletas 3×3.
   - Tampa 6×1×5 e nuca 6×6×1 (chanfro).
   - Sombra #b68b78 de 1 px sob o olho.
6. **Tronco — resolvido.**
   - Peito em degraus: z −10 (y 21–27), −9 (17–21) e −8 (15–17).
   - Quinas em tom mais escuro, chevrons em zigue-zague e borda recortada em 3 pontas.
7. **Pernas e pés — resolvido.**
   - Joelheira com placa em ponta de flecha (3×4, 15° para a frente) e tornozeleira com ponta para baixo.
   - Coxa com 2 penas 3×4 sobre a joelheira.
   - 3 dedos abertos (−30°, 0° e +30°) com garra em 2 cubos (ponta caída 40°), mais o esporão de trás.
8. **Pintura — parcial.**
   - O grão nunca escurece abaixo do tom base.
   - Creme: 44% luz, 43% base, 12% sombra.
   - Prata com chanfro de 1 px em cima e embaixo.
   - **Pendente:** o vermelho da textura inteira tem 26% de luz, porque o corpo fica em base/sombra (separado das penas) e o núcleo, quase todo coberto pela capa, ocupa 960 px.

## As 3 maiores diferenças que ainda restam

1. **De lado, a capa é um bloco que desce quase reto e cobre a perna até o joelho.** Na ficha, ela é uma faixa diagonal que deixa a perna à mostra. De frente, ela abre até 25,8 u, contra ~29 na ficha.
2. **A juba de perfil varre para trás e para baixo.** Na ficha, as lâminas sobem e curvam para cima. De costas, ainda aparece um pouco da nuca vermelha.
3. **As pontas douradas das ombreiras parecem palitos curtos**, não as garras curvas da ficha. A faixa do elmo, vista de lado, lê como barra prata reta.

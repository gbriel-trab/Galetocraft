# Folha do crítico: pirococo.geo.json

## Medidas
- sobreposição com a arte (IoU), pose `render`: **48%** (yaw 6, pitch -16; meta ≥ 60%)
- guia de estilo: **15 de 15** critérios
- peças soltas e chão: **10 aviso(s)**
  - pose neutra: a 0.50 px de pe_e (cubo 0): pe_e (cubo 2)
  - pose neutra: a 0.50 px de pe_d (cubo 0): pe_d (cubo 2)
  - walk@0: o ponto mais baixo está em y = -1.10 px (afunda ou flutua)
  - walk@0.25: se soltou a 0.37 px de corpo (cubo 0): cauda_e1 (cubo 0), cauda_e2 (cubo 0), cauda_e3 (cubo 0), e mais 12 ossos (15 cubos no grupo)
  - walk@0.5: o ponto mais baixo está em y = -1.10 px (afunda ou flutua)
  - walk@0.75: se soltou a 0.37 px de corpo (cubo 0): cauda_e1 (cubo 0), cauda_e2 (cubo 0), cauda_e3 (cubo 0), e mais 12 ossos (15 cubos no grupo)
  - sleep@0: o ponto mais baixo está em y = -9.24 px (afunda ou flutua)
  - sleep@2: o ponto mais baixo está em y = -9.24 px (afunda ou flutua)
  - sleep@4: o ponto mais baixo está em y = -9.24 px (afunda ou flutua)
  - sleep@6: o ponto mais baixo está em y = -9.24 px (afunda ou flutua)

## Imagens
- `1_vistas.png`
- `2_rosto.png`
- `3_arte.png`
- `4_escala_jogo.png`
- `5_animacoes.png`

## Como responder
Responda a cada pergunta com **sim**, **não** ou **não sei**, olhando as imagens. Quando a resposta for "não" ou
"não sei", diga **onde** está o problema (vista, região, osso se souber) e **o que mudar**, em uma linha. Não
responda pelo que o modelo "deveria" ter, só pelo que dá para ver. Se a vista já bate com a arte, a resposta é
"sim": não invente melhorias.

## Silhueta e proporção (1_vistas, 3_arte)
1. Dá para reconhecer a criatura só pela sombra, de frente e de lado?
2. A proporção entre cabeça, tronco e pernas é a da arte, e não a de um animal "realista"?
3. Os elementos marcantes da ficha estão todos lá (crista, barbela, cauda, manto, chamas, armadura...)?
4. A simetria só aparece onde a arte é simétrica? A postura do `parado` tem vida (peso, curva), sem cara de
   manequim?
5. Os pés tocam o chão, e nenhuma peça parece solta, flutuando ou atravessando outra sem querer? (Confira com a
   lista de peças soltas nas medidas.)

## Rosto (2_rosto)
6. Os olhos têm a forma e a posição da arte, com pupila e pálpebra (que fecha no piscar)?
7. O bico (ou boca) e os olhos estão centrados e na altura certa? A expressão é a da arte?

## Bordas e geometria (1_vistas, 2_rosto)
8. Franjas, penas, chamas e garras são planos com recorte na textura, e não escadinhas de cubos?
9. Alguma curva foi feita com degraus de cubos pequenos onde um plano girado ou a textura resolveria?
10. Há "poeira de cubos" (muitos cubos de 1 px imitando detalhe que a textura faria)?

## Textura (1_vistas, 2_rosto)
11. Cada material tem 3 a 5 tons, sem contorno preto, sem degradê de "travesseiro" e sem luz pintada de um lado?
12. O texel é sempre do mesmo tamanho (sem *mixels*, sem UV esticada)?
13. As cores lembram as da arte (mesma matiz, um pouco mais saturadas e menos claras)?

## Jogo e animação (4_escala_jogo, 5_animacoes)
14. A 8 blocos ainda se reconhece a espécie e o tipo (fogo, água...)? A 16, a silhueta ainda é dela?
15. No parado e no andar, nada se solta nem atravessa o corpo, e o movimento tem ritmo (cascata na cauda, quique
    no andar)?

## Resumo
- **Os 3 defeitos que mais pesam**, do maior para o menor, cada um com o local e a correção.
- **O que está bom e não deve mudar.**

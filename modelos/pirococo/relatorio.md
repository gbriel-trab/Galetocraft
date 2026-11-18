# Pirococó (#001): relatório do modelo refeito do zero

- **Cubos:** 129 (orçamento 110–170): 65 caixas e 64 planos (50%). 11 cubos girados (9%): as tranças a 45° e as pontas das ombreiras a 20°.
- **Textura:** 128×128, 1 px por unidade, 30 cores, só da paleta da ficha. Peças iguais dividem a mesma ilha de UV (lado esquerdo com `mirror`, segmentos de trança, lâminas).
- **Ossos (60):** `pirococo` › `corpo` (`pescoco` › `cabeca` › `mandibula`, `olhos`, `palpebra_d/e`, `gema_testa_brilho`, `crista` › `crista_d/e`, `bochecha_d/e`), `asa_d/e` › `_frente/_lado/_tras`, `ombro_d/e`, `gema_peito_brilho`, `cauda` › `cauda_a/b/c_0..5` › `lamina_a/b/c` › `losango_a/b/c_brilho`; `perna_d/e` › `pe_d/e` › `dedo_*`.
- **Medidas (1º quadro do idle):** altura de 0 a 45 u; largura de 26 u (ficha: ~29 u); comprimento de 38 u, de −11 a +27 (ficha: ~36 u). Na pose de modelagem, as pontas das tranças batem com a ficha em até 1 u.
- **Animações:** `idle` (4 s) e `walk` (2 s), em laço, em Molang. O piscar fica entre 3,70 e 3,86 s. Nenhuma peça desce abaixo do chão no laço (conferido em 16 instantes de cada animação).

**O que ficou diferente da ficha, e por quê**

1. **Largura da capa: 26 u em vez de 29.** Os setores laterais são planos vistos quase de lado na vista de frente. Abrir mais faria a capa atravessar as ombreiras.
2. **Ângulo dos planos:** está no osso de cada setor (capa e crista), e não em cada cubo. Assim os cubos ficam alinhados e a contagem de girados fica abaixo de 15%.
3. **Onda vertical das tranças B e C:** só levanta, nunca desce abaixo da pose, porque elas pendem a 1,5 u do chão. A trança A ondula ±4–7° para os dois lados.
4. **Olho no canto da cara** (2×1 de frente e 2×1 de lado): fica legível de frente e de perfil. O tom do branco é o creme-luz da paleta.
5. **Dedos com garras de 1×2×2:** a ficha exagera as garras em perspectiva. Segui as medidas (pé de −8 a +1,5).

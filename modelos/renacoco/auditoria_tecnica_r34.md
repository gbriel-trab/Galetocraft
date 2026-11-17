# Renacocó #019 · auditoria técnica r34 (olhares 2, 3 e 5)

Fontes: especificação e arte de `referencias/019_renacoco_*`; `revisao/r34_*.png`; `r34.bbmodel` (geometria idêntica ao `renacoco.bbmodel`); foto no jogo; `renacoco.geo.json` (88 ossos, 353 cubos) e `renacoco.animation.json` (idle e walk).
Unidades: os números abaixo estão em **px do Blockbench (r34.bbmodel / r34.py)**. O geo.json é a mesma geometria × 0,913: altura 43,8 px no Blockbench = 40 px no geo = 2,50 blocos.

## Proporções medidas (% da altura total, crista incluída)

| trecho | arte (y 45→935 da ilustração) | r34 (geo + vista de frente) |
|---|---|---|
| cabeça + crista (topo → base do crânio) | ~21% | 23,5% |
| pescoço à mostra (crânio → gola) | ~6–7% | ~11% |
| tronco (gola → fim das penas do peito) | ~37% | **~45%** |
| pernas à mostra (fim das penas → chão) | **~33–35%** | **~20%** (na vista de frente: 22%) |

O `detalhes.md` diz que as pernas estão em 0,30, mas essa conta mede do chão até o miolo do tronco (y 15). O avental de escamas desce até y 8,6 e cobre a coxa e metade do tarso. Cabeça e crista estão boas. O erro está no tronco comprido e nas pernas curtas.

## TOP 8 PROBLEMAS (do mais visível para o menos visível)

**1. Anatomia: pernas curtas e tronco comprido; o peito vira saia.**
A última fileira de penas do peito (`peito10`–`peito13` e os `_pt`, de y 8,6 a 14,5) pende 3 a 5 px à frente das pernas. Atrás dela não há corpo, porque o miolo do tronco termina em y 15,0. No perfil, isso forma uma cortina oca. As 5 rêmiges de cada asa (`asa_rem0`–`rem4`, de 12 a 14,5 px) também descem até y 8,9. No perfil, a frente do manto (`manto0_*_2` e a barra) ainda cobre a metade de trás do tarso.
**Correção:**
- Termine o avental em y ≥ 13,7: apague a última fileira ou suba-a 5 px e suba a penúltima 2 px. As pernas passam a 31%.
- Para fechar a barriga, ponha atrás das escamas um bloco de 7,0 × 3,0 × 6,0 em y 12,7–15,7, z −6,0 a 0.
- Suba a gola (`gola_tras_*`, `gola_frente_*`) 1,6 px, até o topo em y 30,0. O pescoço à mostra cai para ~7% e o tronco fica em ~37%.
- Encurte as rêmiges para no máximo 9 px, com a ponta em y ≥ 13,7.
- Recue os painéis da frente do manto (`manto0_d/e_0..2` e `frente*`) de modo que, abaixo de y 12, a borda dianteira fique em z ≥ +1,6, atrás do calcanhar.

**2. Anatomia: leitura humanoide (ombro quadrado + tabardo).**
Três peças formam um ombro de gente vestindo capa:
- `gola_lado_d/e_a..d`: plataformas horizontais de 4,8 × 0,9 × 4,2 em y 26,4;
- `dobra_d/e_*`: ombreiras a ±20°, que vão até x ±9,5;
- `babador_a..c`: retângulo vertical de 6,4 × 7,6 com laterais retas.

Na foto do jogo, de frente, o bicho parece uma pessoa de manto com tabardo. Na arte, a gola enrolada sobe junto ao pescoço, o ombro cai em diagonal e o babador é um escudo com bico serrilhado sobre um peito estufado.
**Correção:**
- Apague os quatro `gola_lado_*_a/b` (as plataformas).
- Gire as `dobra_*` de ±20° para ±38° e traga-as 1 px para dentro (x máx. ±8,0). A linha do ombro deve cair de y 29 junto ao pescoço até y 24,5 na ponta.
- Refaça o babador em 3 degraus: 6,4 de largura em y 23,5–26,9, 4,8 em y 21–23,5 e 2,8 em y 19–21, inclinado +10° em X (topo para a frente).
- Ponha atrás dele uma quilha de 4,8 × 5,5 × 1,6 em y 17,5–23, que salta 1,2 px. O peito passa a ser curvo, e não uma placa.

**3. Geometria: as asas viram "palitos/espadas".**
- As rêmiges `asa_rem0..4_d/e` são lâminas únicas de 0,9 × 12–14,5 × 2,6 px, penduradas na vertical ao lado das pernas. No r34_3-4 e de frente, leem-se como 2–3 facas creme.
- 38 dos 44 cubos das asas têm menos de 1 px de espessura.
- A arte mostra 3 fileiras em telha (cobertura azul, secundárias azul-claras, primárias amarelas), com 6–8 penas visíveis por lado.

**Correção:**
- Troque cada lâmina por 2 penas sobrepostas: a de cima, azul-clara, com 1,4 × 6 × 3,0; a de baixo, amarela, com 1,3 × 5,5 × 2,6 e ponta chanfrada (cubo de 1,8 a 45°). Elas se sobrepõem 1,5 px, num total de no máximo 9 px.
- Use 6 por lado, em leque com guinada de 0°, 10°, 20°, 30°, 40° e 50°. Cada pena fica 0,6 px mais para fora que a anterior, em telha.
- Espessura mínima de 1,3 px.

**4. Geometria/implementação: a cauda 3 corre dentro do manto, e as 3 caudas tombam para um lado.**
- A superfície das costas do manto segue z ≈ 4,4 + 0,78·(28,2 − y).
- Os elos 4–5 e o leque da cauda 3 ficam em y 8,5–14,7 e z 16–24, exatamente sobre essa superfície. As penas do leque atravessam o manto, e no perfil a corrente de baixo "entra" no manto.
- A raiz `cauda` tem pivô em x = −1,6 (fora do centro), e as cadeias têm rotação Z de −7°, −13° e −19°. As três vão para o mesmo lado (até 7,7 px) e, nas costas, cobrem a asa direita do emblema (r34_vistas, vista traseira, e foto do jogo).

**Correção:**
- Pivô de `cauda` em x = 0, y 23,5, z 5,5; Z das cadeias = 0.
- Aumente a inclinação para cima de `cauda1_0`, `cauda2_0` e `cauda3_0` em +8°, +10° e +16°, no mesmo sentido em que a cauda 1 já sobe.
- Reduza a curva por elo de 10° para 6°.
- Critério: todo elo com z ≥ 6,6 + 0,78·(28,2 − y), ou seja, 2 px fora do manto.
- No ponto de saída, ponha um aro dourado de 3,0 × 3,0 × 1,5 sobre o manto, para a saída parecer intencional.

**5. Anatomia/geometria: o pescoço é um tubo grosso, da largura da cabeça.**
- `pescoco_base_a/b` tem 4,8 de largura; com os cards `pesc_pena0..2_d/e` (0,8 de espessura, a ~30°), o pescoço chega a 6,3, mais largo que o crânio (5,8). De frente, a cabeça "assenta" num tronco azul.
- No perfil do r34_rosto, um card da nuca aparece de quina como um espeto azul fino.
- O osso `pescoco` está quase vertical (2°).
- Na arte, o pescoço tem ~60% da largura da cabeça e avança um pouco.

**Correção:**
- `pescoco_base` com 3,4 × 4,0 e `pescoco_alto` com 2,8 × 3,4.
- Troque os 12 cards por 3 penas em telha de cada lado, de 1,3 × 2,6 × 2,8, encostadas (no máximo 0,4 px fora da superfície) e sem rotação composta.
- `pescoco`: rotação de 2° para 10° para a frente; `cabeca`: −8° para compensar.

**6. Geometria: manto de chapas de 1 px, em tenda.**
- Todos os painéis (`manto0..4_d/e_*`, `manto_costas_p_*`) têm 1,0 px de espessura. Todos os 50 cubos têm rotação composta, como (57°, −53°, −61°).
- No render branco, os painéis da frente de baixo são retângulos lisos de 8,6 × 7,6. As costas formam um trapézio liso com uma "prateleira" reta no topo (y 28,1).
- A espessura fica no limite do que a especificação proíbe ("chapa sem espessura").

**Correção:**
- Painéis com 2,0 px de espessura.
- Friso dourado da frente (`manto0_*_frente*`) com 2,0 × 2,0, contínuo da gola à barra; barra com 2,0 × 2,0.
- Divida cada painel de baixo em 2 dobras, com profundidades alternadas de ±0,9 px.
- Use no máximo 2 eixos de rotação por painel, para os degraus alinharem.
- Nas costas, troque a prateleira por uma gola enrolada: 3 cubos de 10 × 3 × 3 em volta do pescoço, em y 27–30.

**7. Implementação: o andar é de perna-pau e atravessa o avental.**
- `perna_d/e` giram ±25° a partir do quadril (y 16), como bastões rígidos. Não há osso de tarso nem de pata.
- O pé gira junto: a ponta dos dedos (6,4 px) afunda ~2,7 px no chão e o calcanhar sobe.
- No passo máximo, a canela avança ~1,9 px em y 11 e atravessa as escamas de baixo e a rêmige `asa_rem0` (z −8,2 a −3,5), cerca de 1 px de interpenetração.

**Correção:**
- Crie `tarso_d/e` (pivô ±2,6; 6,7; −1,0, no anel do tornozelo) e `pata_d/e` (pivô ±2,6; 1,8; −1,0).
- Walk: quadril ±18°; tarso com +12° no passo e −6° no apoio; pata com −(quadril + tarso) no apoio (pé plano) e +15° ao levantar.
- Com o item 1 feito, a colisão some.

**8. Implementação: o LOD apaga peças estruturais e deixa cubos soltos.**
O `GaloRenderer` esconde os ossos `_lod1`, `_lod2` e `_lod3` a 16, 32 e 48 blocos (cumulativo). O `lods.json` põe ali peças de sustentação:
- **coxas** (`coxa_*_a..c`, lod1): a partir de 16 blocos abre um vão de 1,6 px entre o topo do tarso (y 13,4) e o tronco (y 15,0);
- **tornozelo** e **dedo do meio** (lod2): a 32 blocos o pé se separa da canela (0,4 px) e a garra da frente (`garra_meio_d/e`) flutua 4 px à frente;
- **crânio** (`cranio_a..d`, lod3): a 48 blocos as 12 penas do rosto ficam soltas no ar;
- **elos 0–2 da cauda 3** (só existem como `_lod1`/`_lod3`): a 48 blocos, o resto da corrente e o leque ficam separados do corpo.

**Correção:** mova `cranio_a..d`, `coxa_*`, `tornozelo_*`, `dedo_meio_*` e um elo de cada nível de `cauda3_0..2` para o osso-base, sem LOD. No LOD, deixe só `_pt`, chanfros e penas decorativas.

## Problemas menores
- Não há animações de corrida leve, dano, cura e poder, que a especificação pede (o Java só chama idle/walk). Também não existem ossos de bico e barbela para as expressões de cura/poder.
- Faltam os ossos `manto_lados` e `peito` sugeridos. O manto balança como bloco rígido de 28 px: ponha um filho `manto_*_baixo` com pivô em y ≈ 11.
- `cranio_alto_a/b` (0,32 px) e `queixo_a/b` (0,24 px) são lâminas finas, com risco de z-fighting e frestas. Faça-as com no mínimo 0,8 px ou junte-as ao crânio.
- 214 dos 353 cubos têm menos de 1 px e 252 têm rotação oblíqua. Isso é excesso de cards finos e enfraquece a leitura voxel.
- A crista, de frente, é um leque simétrico de 5 pontas sobre uma faixa: lê-se como coroa, que a especificação proíbe. Na arte, ela é assimétrica e varre para trás, até a nuca.
- A largura total é de 1,86 bloco (a especificação provisória diz 1,60), por causa da barra do manto. Feche a barra em 1,5 px por lado.
- Asas no idle: ±2° em Z não aparece. Use ±4° com um pouco de rotação em X.
- O `r34.bbmodel` não tem animações (elas só existem no JSON gerado), então não dá para ver no Blockbench.

## O que está bom
- A hierarquia é limpa. As pernas são raiz (o balanço do corpo não arrasta os pés). Pescoço → cabeça → crista estão encadeados. Há 1 osso por elo nas 3 caudas, mais o leque.
- Os pivôs estão nas articulações certas: quadril em y 16, base do pescoço em 27, cabeça em 34,7, ombro/manto em 27,6 e asas em 26,5. Nenhum pivô absurdo.
- A altura é de 2,50 blocos. No LOD 0 os 353 cubos formam uma peça só (nenhum cubo solto). Idle e walk mexem pescoço, cabeça, crista, asas, os 3 painéis do manto, as 3 caudas (onda por elo) e as pernas.
- A postura é ereta, as patas são grandes com garras escuras, a cauda tripla de elos é legível e a cabeça tem tamanho correto (23,5% contra 21%). Não há o erro de "cabeça grande sem pescoço".

## Notas
- **Anatomia: 5/10.** Postura e cabeça certas, mas pernas com 20% em vez de 33%, tronco longo, ombro quadrado e tabardo dão a leitura de "pessoa de manto".
- **Geometria: 5/10.** É coesa no LOD 0, mas tem muitos cards de 1 px, asas em lâmina, manto fino e chapado e cauda 3 dentro do manto.
- **Implementação: 6,5/10.** Ossos e pivôs são bons, mas o andar é rígido e sem pata, o LOD remove peças estruturais e faltam as animações de dano, cura e poder.

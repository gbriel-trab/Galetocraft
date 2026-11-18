# Crítica cr01: Pirococó g3 (18/11/2026)

**Nada daqui foi aplicado ao modelo.** É material para o chat de design. Antes de corrigir, confira cada "não" nas
imagens: o crítico também erra.

## O que foi avaliado
- **Modelo:** `modelos/pirococo/cobblemon/pirococo.geo.json`, `.animation.json` e `pirococo.png`, do commit
  `a97b657` (o g3 que está no mod).
- **Folha:** `1_vistas.png` a `5_animacoes.png` e `perguntas.md`, feitos pela `folha_critica.py` da skill
  `modelar-galeto`. A folha usou a arte `001_pirococo_g3_arte_recorte.png` e as vistas `001_pirococo_g3_vistas.png`.
- **Medidas:**
  - guia de estilo: 15 de 15;
  - sobreposição com a arte na pose `render`: 48% (meta ≥ 60%), e o melhor encaixe só veio espelhado;
  - peças soltas e chão: 10 avisos (`pecas_soltas.txt`).
- **Crítico:** um subagente sem o raciocínio de quem fez o modelo, com o pedido de `agents/critico.md`. Ele leu
  também o `.geo.json`, a animação e a textura para dar as correções com números.
- **Números conferidos depois:** os do `manto_e`, do `render`, do bico e dos pixels do olho batem com o modelo.

Nesta folha, as perguntas 9 e 10 ainda estavam na forma antiga, em que "não" era a resposta boa. A skill já foi
corrigida.

## Respostas
| nº | resposta | onde | o que mudar |
|---|---|---|---|
| 1 | não | 1_vistas, lado (e 3/4) | De frente lê bem. De lado vira uma coluna: `manto_e`/`manto_d` (1x19x8, y ±42°) cobrem o peito e as pernas, e a cauda cai rente ao corpo. Recue os dois mantos 2 px (pivô e cubo z −1,5 → +0,5) e, no `parado`, incline a base deles ~12° para trás, para as pernas e o peito aparecerem à frente do manto como na vista "direita" da ficha. A cauda está no resumo, item 1. |
| 2 | sim | 1_vistas, 3_arte | Cabeça ~15%, tronco ~25% e pernas ~41% da altura, iguais à arte. |
| 3 | não | 1_vistas frente (peito); trás e lado (cauda) | O símbolo do peito é um "O" roxo (quadrado vazado), e a ficha pede o V da fênix. Repinte a frente de `peitoral_brilho` (6x3) como V roxo sobre prata: linha 1 roxo nas colunas 1, 2, 5 e 6; linha 2 nas colunas 2 a 5; linha 3 nas colunas 3 e 4. A cauda tripla existe, mas só aparece de costas e embolada (resumo, item 1). |
| 4 | não | 5_animacoes parado; 1_vistas lado | O `parado` é a pose de modelagem (pescoço −1,4°, cabeça 2°, corpo −0,5°): coluna reta, pés colados, cara de manequim. No `parado`: incline o pescoço ~12° para a frente e devolva ~12° na cabeça (o S da arte, com o bico nivelado), e estufe o peito com o corpo ~4°. Afaste cada perna 1 px (`perna_e` x+1, `perna_d` x−1); hoje as garras de dentro se tocam em x=0 e a ficha tem um vão de um pé entre eles. |
| 5 | não | medidas; 2_rosto lado | (a) `pe_e`/`pe_d`, cubo 2 (garra do meio), fica a 0,5 px do pé: origem z −5,5 → −6 e tamanho z 3 → 4. (b) No `dormir`, `perna_e`/`perna_d` descem −9 junto com o corpo, e pés e franja do manto chegam a −9,24 px, abaixo do chão. Não desça as pernas: dobre coxa e canela e deite as `manto_pena*` para trás até o ponto mais baixo ficar em y ≈ 0. (c) O andar está no nº 15. (d) A quina de `chifre_e/d_brilho` (x até ±3,5) sai 0,5 px pela lateral do elmo (risco amarelo sobre a faixa prata na vista de lado): recue 0,5 px para dentro. |
| 6 | não | 2_rosto frente e lado | O olho 2x2 tem 3 dos 4 pixels escuros (72,50,59) e lê como óculos escuros, sem o claro do olho da arte. Na textura de `olho_e`/`olho_d`, mexa só na fileira de baixo: o escuro do lado do bico vira roxo (íris) e o roxo do lado de fora vira branco-lilás (241,232,240). A fileira de cima continua escura, como linha da pálpebra. A posição e a pálpebra estão certas (fecha no piscar); não mexa nelas. |
| 7 | não | 2_rosto lado e 3/4 | Bico e olhos estão centrados e na altura certa. Mas de lado o bico é um bastão reto de 5 px na horizontal ("charuto"), e a arte tem bico curto em gancho para baixo. Gire o osso `bico` ~15° com a ponta para baixo e encurte 1 px (cubo principal z 4 → 3, ponta 1 px para trás). A expressão melhora com a correção do nº 6. |
| 8 | não | 1_vistas 3/4 (pés) e frente (barra do manto) | Crista, chifres, penas do manto e tufos da cauda já são planos recortados. As garras são cubos 1x1x3 rombudos que parecem dedos amarelos; a arte tem garras douradas pontudas. Troque os 4 cubos de cada pé por planos 0x2x3 com a ponta curva recortada na textura. A ponta das `manto_pena*`/`manto_*_pena*` está recortada em 2 palitos de 1 px (franja de tapete): recorte numa ponta única afinando 4 → 2 → 1 px. |
| 9 | não (bom) | — | Não há curva em degraus: a cauda é uma cadeia de ossos e a crista é um leque de planos. Nada a mudar. |
| 10 | não (bom) | — | Só 8 cubos de 1 px (as garras, nº 8) em 83 cubos. Nada a mudar. |
| 11 | sim | — | Roxo, prata, vermelho e dourado com 4 a 5 tons cada. Sem contorno preto, sem travesseiro, sem luz pintada de um lado. |
| 12 | sim | — | Tamanhos inteiros e nenhuma escala nas animações; o texel é igual em todas as vistas. |
| 13 | sim | — | As matizes batem com a arte: roxo ~272°, dourado ~47°, vermelho ~0°, prata-lilás. A crista só fica oliva nas faces laterais por causa da sombra do render. |
| 14 | sim | 4_escala_jogo | A 8 blocos, crista dourada + manto roxo→fogo + armadura prata leem como galo de fogo. A 16, a silhueta (auréola da crista + manto aberto) continua sendo dele. |
| 15 | não | medidas; 5_animacoes andar | O ritmo existe: quique de −0,8 → +0,2, balanço de ±2° e cascata defasada na cauda (c1 → c3). Problemas: (a) em 0% e 50%, a perna que passa tem canela a 26° com coxa a 0°, e a ponta do pé raspa 1,1 px abaixo do chão; nesses quadros gire a coxa ~10° para a frente (ou o pé para cima). (b) Em 25% e 75%, as `cauda_*1` se soltam 0,37 px do corpo; embuta a base 1 px (cauda e filhos, z 3,5 → 2,5). (c) Provável, deduzido da geometria e não marcado pela ferramenta: a perna de trás a 24° vai ~5 px para trás e atravessa o manto de trás e as `manto_pena*`. Leve o manto ~8° para trás no pico do passo ou reduza o passo para ±16°. |

## Os 3 defeitos que mais pesam
1. **Cauda tripla escondida e embolada** (1_vistas lado, trás e 3/4; 3_arte). É o elemento que mais marca a arte,
   mas nasce em y 21 (meio das costas) e cai quase reta (`cauda_*1` a −64°). Por isso some de frente e de 3/4, e de
   costas as três pontas viram um tufo só na altura do joelho. Correção:
   - suba a base para y ~27, logo abaixo da gola;
   - deixe `cauda_*1` sair mais para trás (−64° → ~−35°) e curve mais os elos (`cauda_*2/*3` 8° → ~15°);
   - abra o leque com `cauda_e1`/`cauda_d1` em z ±15°, para as três pontas ficarem separadas, bem atrás do corpo e
     na altura do joelho.
2. **Pose `render` incoerente: IoU 48%, a meta é ≥ 60%** (3_arte). A cabeça vira para o lado errado: o bico aponta
   para a esquerda da imagem e o da arte para a direita. A cauda sai pelo lado do bico (o toco marrom no quadril), e
   o encaixe só foi achado espelhado. No `render`:
   - inverta o yaw da cabeça (−28 → +28) e do pescoço (−8 → +8);
   - gire o osso `cauda` ~70° em y para o lado oposto ao bico, com uma corrente na altura do ombro, uma no quadril e
     uma no joelho;
   - feche o manto do lado do bico (na arte ele cai reto ao lado da perna);
   - abra as pernas (z ±3° → ±8°).
3. **Perfil de coluna e `parado` de manequim** (1_vistas lado; 5_animacoes). Os mantos laterais tapam corpo e pernas
   de lado, o pescoço é reto e as pernas estão coladas. Recue e incline os mantos (nº 1) e dê ao `parado` o S do
   pescoço, o peito estufado e as pernas afastadas 1 px (nº 4).

Fora do top 3, mas barato e obrigatório: o `dormir` enterra a criatura 9,24 px (nº 5b). Depois dele vêm o olho de
óculos escuros (nº 6) e o "O" no peito (nº 3).

## O que está bom e não deve mudar
- As proporções de cabeça, tronco e pernas, iguais às da arte.
- A paleta e a textura: matizes certas, 4 a 5 tons por material, texel uniforme, glowmask em chifres, tufos e gema.
- A silhueta de frente (auréola da crista + dois chifres + manto aberto + armadura prata), que se lê a 8 e a 16
  blocos.
- O degradê do manto roxo → vermelho → dourado.
- As técnicas: planos cruzados nos chifres e tufos, crista em leque de planos, penas do manto em planos, pálpebra
  escondida que fecha no piscar.
- O ritmo do andar (quique, balanço e cascata da cauda).
- O orçamento: 83 cubos, 69 ossos, textura 128x64.

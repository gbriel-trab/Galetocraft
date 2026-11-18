# Anti-padrões de modelos de criatura no estilo Cobblemon

Cite pelo nome no plano da rodada os que valem para a espécie. Quando aparecer um defeito novo, acrescente-o aqui
com o mesmo formato. Esta lista é a memória do projeto.

Formato: **nome**: como reconhecer, e depois → como corrigir.

## Geometria
- **Boneco de caixas:** tronco, cabeça e membros em 5 a 15 caixas lisas, sem planos de borda; a silhueta parece um
  boneco de Minecraft comum. → Franjas, penas, cristas, garras e chamas viram planos com recorte na textura (~46% dos
  cubos nos modelos do Cobblemon).
- **Escadinha de cubos:** curva feita de degraus de cubos pequenos. → Use um plano girado no osso (não no cubo) ou
  desenhe a curva na textura.
- **Poeira de cubos:** muitos cubos de 1 px imitando um detalhe (escama, rebite, borda) que a textura faria. → Pinte
  na textura; cubo novo só quando muda o contorno.
- **Fracionado, UV por face, cubo girado demais:** tamanhos com vírgula, UV por face, mais de ~20% de cubos girados
  no próprio pivô. Nos 78 modelos medidos: 0 fracionados, 0 UV por face, mediana de 5% girados. → Tamanhos
  inteiros, UV de caixa; para inclinar, gire o osso.
- **Peças soltas:** cubo que não encosta no corpo, dedo à frente do pé, cauda que se descola no andar, pé que afunda
  no chão. É a falha nº 1 do 3DCodeBench. → `pecas_soltas.py` acusa com a distância e a peça do corpo mais perto.
  Encoste (vão ≤ 0,25 px) ou enterre a raiz da peça 1 px no corpo; confira nas animações, não só na pose neutra.
  O vão de 0,1 px à frente para evitar que as faces pisquem (*z-fighting*) é técnica, não defeito.
- **Peça atravessando:** perna que passa por dentro do manto no andar, chifre que sai pela lateral do elmo. O
  `pecas_soltas.py` não pega isso: olhe de lado e nos quadros das animações. → Afaste a peça, reduza o giro na
  animação ou mova a peça da frente junto.
- **Garra rombuda:** garras em cubo 1x1xN que parecem dedos. → Planos com a ponta curva recortada na textura.
- **Franja de tapete:** ponta de pena recortada em palitos de 1 px. → Ponta única afinando (4 → 2 → 1 px).
- **Plano de lado:** um plano visto de quina some, e uma crista de planos paralelos vira uma linha no perfil. → Abra
  os planos em leque (o fogo do Blaziken usa ±60–65°) ou cruze dois planos em X.

## Pose e proporção
- **Manequim:** simetria perfeita e corpo duro no `parado`, com braços retos e cabeça alinhada ao tronco. → A
  postura vem do `parado`: cintura +10–15°, tronco e cabeça compensando, membros com ±5–10° e uma leve assimetria
  (ver o `ground_idle` do Blaziken no guia).
- **Proporção realista:** cabeça pequena e pernas de ave real, quando a arte tem cabeça grande, olho grande e
  pernas estilizadas. → Meça na arte (cabeça/altura, perna/altura) e copie a proporção; a ficha manda, não a
  anatomia.
- **Perfil de coluna:** de lado, mantos ou asas laterais tapam o peito e as pernas, a cauda cai rente ao corpo e a
  criatura vira uma coluna. → Recue e incline os painéis laterais para trás, e leve a cauda para longe do corpo.
- **Pose de destaque espelhada:** a `render` só encaixa na arte espelhada, e a cabeça e a cauda saem para o lado
  errado. → Inverta o yaw da cabeça e do pescoço e mande a cauda para o lado oposto ao bico, como na arte.
- **Elemento marcante perdido:** a crista, a barbela, a cauda ou o manto da ficha ficaram pequenos ou sumiram na
  simplificação. → Simplifique o desenho interno, nunca o contorno marcante; ele vira geometria (guia, seção 13).

## Rosto
- **Olho chapado:** olho pintado direto na face da cabeça, sem pupila em plano nem pálpebra. → Olho em plano a +0,01
  da face, pupila a +0,01 do olho e pálpebra escondida, que o `piscar` mostra (guia, seção 4, "Rosto e olho").
- **Olho de óculos escuros:** olho pequeno quase todo escuro, sem o claro da arte. → Escuro só na pupila e na
  linha da pálpebra; o resto do olho claro (esclera ou íris).
- **Bico de charuto:** bico reto e comprido de lado, quando a arte tem bico curto em gancho. → Encurte e gire o osso
  do bico 10 a 20° com a ponta para baixo.
- **Expressão neutra demais:** sobrancelha e pálpebra retas, quando a arte tem um olhar decidido ou bravo. →
  Sobrancelha em plano girado (as faces da cunha do rosto do Blaziken vão a ±38,5°) e o recorte do olho
  inclinado na textura.

## Textura
- **Textura de IA:**
  - contorno preto em volta das peças;
  - degradê de "travesseiro" (claro no meio, escuro nas bordas);
  - ruído forte e aleatório;
  - cores puras como (255, 0, 0);
  - luz pintada vindo de um lado.

  → 3 a 5 tons por material, mosqueado leve (0,25 a 0,65 dos vizinhos diferem), luz pintada de no máximo 16 de
  luminância, cores pela `rampa_da_arte()`.
- **Mixels:** pixels de tamanhos diferentes na mesma peça, por UV esticada ou caixa de tamanho diferente da área
  pintada. → UV de caixa com 1 texel = 1 unidade; corrija remapeando, não com mais cubos.
- **Paleta genérica:** vermelho, amarelo e roxo "de catálogo" em vez das cores da arte. → `rampa_da_arte(cor da
  arte)` em cada material; confira com `comparar_arte.py` ou `cores_por_regiao.py`.
- **Brilho em tudo:** `_glowmask` cobrindo áreas grandes; o modelo vira uma lâmpada no escuro. → Brilho só no que
  emite luz na arte (fogo, gema, olho mágico).

## Escala do jogo
- **Detalhe que some:** peça de 1 px ou contraste baixo entre materiais vizinhos que some a 8 blocos (veja
  `4_escala_jogo`). → Engrosse para 2 px ou aumente o contraste entre os materiais, não dentro deles.
- **Silhueta que não se lê a 16 blocos:** sem o elemento marcante, a criatura vira "um galo qualquer". → Aumente o
  elemento marcante (crista, manto, cauda) até a silhueta se ler sozinha.

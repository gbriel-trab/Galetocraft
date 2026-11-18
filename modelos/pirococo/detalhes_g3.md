# Pirococó, ficha g3: da imagem ao modelo

Ficha: `modelos/referencias/001_pirococo_g3_ficha.png` (18/11/2026), com os recortes `_arte`, `_vistas`,
`_expressoes`, `_detalhes` e `_arte_recorte` (a figura principal sem fundo, para o `comparar_arte.py`).
Gerador: `ferramentas/especies/pirococo_cobblemon.py`. Rodadas: `modelos/pirococo/revisao/g3a_*` a `g3f_*`.
Método: seção 13 de `modelos/GUIA_ESTILO.md`.

## 1. Leitura da ficha
**Proporções** (vista de frente, altura 261 px → 45 px no modelo):

| marco | fração da altura (do chão) | no modelo (px) |
|---|---|---|
| tornozelo | 0,08 | 3 |
| joelho | 0,27 | 12–13 |
| quadril | 0,47 | 21 |
| ombros | 0,68 | 30–31 |
| queixo | 0,78 | 34–35 |
| olhos | 0,87 | 37 |
| topo da crista | 1,00 | 45–47 |
| largura dos ombros | 31% da altura | 14 px |
| largura do manto embaixo | 49% da altura | 22 px |

**Desmontagem em três listas:**
- **Massas (caixas):**
  - cabeça vermelha 5x5x6;
  - elmo prateado 6x2x7;
  - bico 2x2x4 com gancho 2x2x1 e mandíbula 2x1x2;
  - pescoço creme 3x5x3;
  - tronco creme 5x8x3;
  - peitoral 6x3x4;
  - cinto 6x3x4;
  - ombreiras 4x3x5 + 3x1x4;
  - coxas roxas 2x8x3;
  - canelas 2x10x2 com greva 3x6x3 e joelheira 3x3x2;
  - pés 3x3x4 com 3 dedos 1x1x3 e 1 atrás;
  - placas do manto: 10x19x1 nas costas e 1x19x8 nos lados.
- **Bordas (planos):**
  - crista de chamas: 4 penas por lado e 2 no meio, 0x4x8, em leque;
  - "chifres" do elmo: chamas 3x7 em X;
  - franja do manto: 5 penas 4x11 nas costas e 4 de 3x11 em cada lado;
  - tufos das 3 caudas, em X, com o losango roxo;
  - peça em V do cinto, 3x5.
- **Desenho interno (textura):**
  - V roxo do peitoral (símbolo da fênix);
  - faixa roxa do cinto e frisos escuros da armadura;
  - gomos do abdômen;
  - trança dos cordões (listras diagonais em 3 tons de ouro);
  - degradê do manto (roxo → magenta → vermelho → laranja → ouro) em fileiras de penas;
  - escamas das pernas;
  - olho violeta com pálpebra escura.

**Paleta:** os 6 círculos da ficha geram as rampas com `rampa_da_arte()`:

| cor | RGB |
|---|---|
| ouro | (252, 194, 47) |
| creme | (247, 228, 207) |
| vermelho | (243, 84, 85) |
| roxo | (127, 53, 188) |
| lilás-prata | (213, 193, 213) |
| cinza-escuro | (94, 76, 82) |

O magenta (205, 30, 86) e o laranja (245, 122, 40) do manto foram amostrados na arte. O degradê de fogo encadeia
tons dessas rampas.

## 2. Resultado
| item | valor |
|---|---|
| cubos / faces | 83 / 362 |
| planos | 34 (41%) |
| cubos girados no próprio pivô | 0 (toda inclinação vai no osso) |
| textura | 128x64, 28 cores |
| altura / largura / comprimento | 2,98 / 2,36 / 1,33 blocos (ficha: 2,5 a 3,0 de altura) |
| `--estilo` | 15/15 |
| animações | parado (com piscar), andar, piscar, grito, dormir e `render` (pose da arte) |
| brilho | gemas roxas (elmo, peitoral e cinto), crista, chamas do elmo e tufos das caudas |
| no jogo | compilado e testado (`runClientGameTest`): `modelos/fotos_jogo/2026-11-18_pirococo_g3/` |

## 3. Sobreposição com a arte (`comparar_arte.py`)
A pose `render` contra a arte principal, só com ângulos de frente e 3/4, dá **IoU 48%** (o Blaziken dá 66%).

Onde difere:
- a arte é em 3/4 com o manto fluido e as caudas finas e longas saindo para trás; no modelo, o manto em placas cobre
  as caudas nesse ângulo;
- as penas da barra do manto e da crista são mais compridas e separadas na arte.

As vistas ortográficas da ficha (frente, direita, trás e esquerda) batem bem: compare em `g3f_vistas_ficha.png`.

Sem medir na arte, a busca casava a silhueta pelas costas (yaw 160°). Por isso o `comparar_arte.py` ganhou a opção
`--de-frente`, para artes de ficha, que são vistas de frente ou 3/4.

## 4. O que ainda pode melhorar
- Subir a sobreposição com a arte: caudas mais longas e mais finas e uma pose `render` com o corpo girado em 3/4.
- Penas da barra do manto um pouco mais longas, como na arte.
- Expressões da ficha (bravo, determinado, sereno) como pálpebras extras, no padrão Cobblemon (`palpebra_dor`), se
  o mod ganhar um controlador de expressões.

## Crítica cr01 (18/11/2026, não aplicada)
A crítica completa está em `revisao/cr01_critica/critica.md`, com a folha e as peças soltas. Foi feita pela skill
`modelar-galeto`. O modelo tem 15 de 15 no guia, mas sobrepõe só 48% com a arte. Os defeitos que mais pesam:
1. a cauda tripla nasce no meio das costas e fica escondida de lado;
2. a pose `render` está espelhada em relação à arte;
3. o perfil vira uma coluna e o `parado` tem cara de manequim.

Há também peças soltas: a garra do meio fica 0,5 px fora do pé, e a cauda se solta 0,37 px no andar. Os pés afundam
1,1 px no andar e o corpo entra 9,24 px no chão no `dormir`.

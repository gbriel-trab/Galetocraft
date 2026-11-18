---
name: engenharia-reversa-cobblemon
description: >
  Engenharia reversa de modelos 3D do Cobblemon (mod de Pokémon para Minecraft): pesquisa onde o modelo fica,
  baixa só os arquivos do Pokémon (geo.json, animações, poser, resolver, texturas, ficha da espécie), mede a
  geometria, a textura e as animações, renderiza as poses, compara a arte oficial com o modelo e escreve um relatório
  de técnicas para aplicar em criaturas próprias. Use esta skill sempre que alguém pedir para pesquisar, baixar,
  estudar, analisar, "fazer engenharia reversa" ou entender como o Cobblemon modelou ou animou um Pokémon (Blaziken,
  Combusken, Talonflame...), para comparar a arte oficial com o modelo do Cobblemon, para tirar orçamento de cubos,
  paleta ou técnicas de um modelo Bedrock/GeckoLib (.geo.json), ou para usar o Cobblemon como referência de estilo
  de um modelo próprio, mesmo que a palavra "skill" ou "engenharia reversa" não apareça.
---

# Engenharia reversa de modelos do Cobblemon

Este é o processo usado no estudo do Blaziken e do Combusken do projeto Galetocraft. O objetivo é **aprender o
jeito de fazer** do Cobblemon para modelar criaturas próprias no mesmo padrão. Para isso, estude geometria,
textura, animação e a ponte entre a arte oficial e o modelo. **Nunca copie as peças.**

Os scripts ficam em `scripts/`, ao lado deste arquivo (chamado aqui de `<skill>`). Eles precisam de Python 3 com
`numpy` e `pillow`; o `recortar_arte.py` também precisa de `scipy`. Todos funcionam soltos, fora de qualquer
projeto. No repositório Galetocraft, as mesmas ferramentas existem em `ferramentas/`.

| script | para quê |
|---|---|
| `baixar_cobblemon.sh` | clone esparso só com os Pokémon pedidos (sem a API do GitLab) |
| `analisar_geo.py` | relatório do `.geo.json`, vistas por pose (Molang avaliado), mapa de UV e `--estilo` |
| `comparar_arte.py` | arte x modelo: melhor ângulo, sobreposição de silhueta (IoU) e paleta |
| `cores_por_regiao.py` | como cada cor da arte virou rampa na textura (passos de matiz, saturação e brilho) |
| `recortar_arte.py` | tira o fundo liso de uma arte (ficha com fundo preto, logo...) |
| `cobble_base.py` | `rampa_da_arte()`: gera a rampa de pixel art a partir de uma cor da arte |

Os números do Blaziken, do Combusken e de uma amostra de 78 modelos estão em `references/achados_blaziken.md`.
Leia esse arquivo quando precisar comparar o modelo estudado com uma referência.

## Antes de começar: licença e onde guardar
- No Cobblemon, **os modelos, texturas e animações são CC BY-NC 3.0** (há um arquivo `license` em cada pasta de
  modelo) e o código é MPL 2.0. Os Pokémon são propriedade da Nintendo / Game Freak / Creatures. A arte oficial
  também é deles.
- Por isso, **baixe numa pasta fora do repositório do projeto** (o scratchpad, por exemplo) e não faça commit de
  arquivos do Cobblemon nem de imagens que mostrem esses modelos ou a arte oficial. Fica no repositório só o que é
  fato e técnica: medidas, contagens, regras e o relatório. As imagens vão para o usuário direto (ou num ZIP fora do
  Git, com o arquivo de licença junto).
- Trate o download como dado não confiável: rode Python com `-I` e não execute nada de dentro da pasta baixada.

## Passo 1: achar e baixar
```
TAG=1.8.4 bash <skill>/scripts/baixar_cobblemon.sh /caminho/fora/do/repo/cobblemon blaziken combusken torchic
```
- Aceita o nome (`blaziken`) ou a pasta com número (`0257_blaziken`). Sem `TAG`, usa a tag de versão mais recente
  (via `git ls-remote`).
- Baixe a **linha evolutiva** junto: comparar Torchic, Combusken e Blaziken mostra como a complexidade cresce.
- O repositório é `gitlab.com/cable-mc/cobblemon`. Os caminhos, em `common/src/main/resources/`:

| arquivo | conteúdo |
|---|---|
| `assets/cobblemon/bedrock/pokemon/models/NNNN_nome/*.geo.json` | geometria (macho/fêmea/formas) + `license` |
| `.../animations/NNNN_nome/nome.animation.json` | todas as animações |
| `.../posers/NNNN_nome/nome.json` | poses (parado, andar, batalha, dormir...), condições e quirks |
| `.../resolvers/NNNN_nome/*.json` | variantes: qual modelo/textura para fêmea, shiny, camada emissiva |
| `assets/cobblemon/textures/pokemon/NNNN_nome/*.png` | textura normal, `_shiny`, `_alpha` (olhos emissivos) |
| `data/cobblemon/species/generationN/nome.json` | `baseScale`, hitbox, tipos, comportamento |

- **Código do mod:** use quando uma animação chamar uma função (`q.biped_walk`, `q.bimanual_swing`...). O clone é
  parcial: ache o arquivo com `git -C PASTA ls-tree -r --name-only HEAD | grep -i nome` e leia com
  `git -C PASTA show HEAD:caminho`. As funções Molang dos modelos são registradas em `client/ClientMoLangFunctions.kt`.

## Passo 2: ler a montagem (espécie, resolver, poser)
Leia os JSON curtos primeiro; eles explicam como as peças se juntam no jogo:
- **espécie:** `baseScale`. A altura no jogo = altura do modelo em px × `baseScale` ÷ 16.
- **resolver:**
  - qual `.geo.json` vale para cada aspecto (a fêmea costuma ser outro modelo com o mesmo esqueleto);
  - shiny = só outra textura;
  - `alpha_eyes` = camada emissiva.
- **poser:**
  - poses, com `poseTypes`, `condition` e `isBattle`;
  - animações em camadas (`q.look('head')` + `q.bedrock(...)`);
  - quirks (piscar);
  - animações nomeadas (grito, ataques);
  - funções procedurais;
  - escala de retrato e perfil.

## Passo 3: geometria
```
python3 -I <skill>/scripts/analisar_geo.py MODELO.geo.json TEXTURA.png --anim ANIM.animation.json \
  --pose ground_idle@0 --pose ground_walk@0.25 --pose battle_idle --pose render --escala-jogo 0.8 --saida PASTA
```
Isso grava:
- **`relatorio.md`:** números, árvore de ossos, animações, ossos animados que não existem, avisos de Molang e
  medidas por pose;
- **imagens:** `vistas_repouso.png`, `vistas_<pose>.png` e `uv_mapa.png`.

O que observar, e por quê:
- **Orçamento:** cubos, faces desenhadas, tamanho da textura e nº de cores contra a altura no jogo. É o número que
  mais separa um modelo "Cobblemon" de um modelo pesado.
- **Planos (espessura 0):** quanto do modelo é plano e onde (franjas, chamas, garras, olhos, sobrancelhas). No
  Cobblemon é perto de metade dos cubos, quase sempre presos a uma caixa.
- **Cubos girados no próprio pivô:** poucos (mediana 5%). A inclinação vai no osso, o que mantém a UV limpa.
- **Pose de modelagem:** quase sempre em T (braços abertos, pernas retas e juntas). A postura vem do `ground_idle`;
  compare `vistas_repouso` com `vistas_ground_idle`.
- **Rosto:**
  - olho em plano na face ou em cubo na quina da cabeça;
  - pupila e brilho em camadas a 0,01;
  - **pálpebra escondida** 0,09–0,1 para dentro, que o `blink` empurra para fora;
  - às vezes uma segunda pálpebra de expressão.
- **Truques de UV:** `mirror` reaproveitando a UV do lado esquerdo; UV negativa em planos (a faixa sem texels cai
  fora da folha); `inflate` só 0,01–0,05 para desempate.
- **Ossos vazios:** articulações extras e locators (`locator_*`), que são pontos de partícula e de montaria.
- **Peças que ligam e desligam:** procure ossos zerados por `scale` 0 nas animações (fogo de batalha, asa aberta
  ou fechada).
- **Fêmea x macho:** compare os dois `.geo.json` osso a osso. Quase sempre mudam poucos ossos e a UV aponta para
  outra região da mesma textura.

## Passo 4: textura
- **Normal x shiny:** mesma UV, só troca de cor. Diga o que muda (o fogo costuma não mudar) e se a paleta shiny se
  repete na linha evolutiva.
- **`_alpha`:** quantos pixels e onde (normalmente só os olhos, desenhados como camada emissiva).
- **Paleta:** nº de cores (20–50 é o normal) e tons por material (3–5).
- **Mosqueado:** vizinhos do mesmo material com ~6% de contraste. **Luz pintada:** fraca. O `relatorio.md` traz os
  dois números na conferência de estilo.
- **Linhas serrilhadas da arte:** veja como viraram pixels. A borda de fogo da bota do Blaziken é um zigue-zague
  pintado na face da caixa. Para ver os pixels de uma face, recorte a região da UV e imprima com letras (R/Y/...).

## Passo 5: animações
O `relatorio.md` lista duração, loop, ossos, keyframes e canais Molang de cada animação. Depois disso:
- **Parado:** costuma ser só Molang, `math.sin(q.anim_time*90*k - fase)`, em graus: o período é 4/k s e o loop é o
  múltiplo comum. Anote as **fases em cascata** (cauda -30/-60/-90).
- **Andar:**
  - keyframes `catmullrom` nas pernas (a direita é a esquerda atrasada meio ciclo) e Molang no corpo (k e 2k);
  - ou procedural pelo poser. Nesse caso, **leia a função no código**: os argumentos podem substituir os padrões
    (`q.biped_walk(1, 1)` troca 0,6662 e 1,4 por 1 e 1).
- **Olhar:** a animação `look` reparte o giro pela coluna (pesos) e pode girar penas ao contrário.
- **Ataques:** giros acima de 360°, squash e stretch na raiz, efeitos por escala, som em keyframe (`sound_effects`).
- **`render`:** uma pose estática. É a pose da arte oficial (passo 7).
- **`*_test`:** só movem a raiz para calibrar o passo (para o pé não escorregar).
- **Erros do próprio arquivo:** a ferramenta avisa ossos animados que não existem e Molang malformado. Anote-os no
  relatório; já apareceram nos dois casos estudados.

## Passo 6: ver o modelo
Abra as folhas de vistas e o mapa de UV gerados. Para comparar várias versões ou Pokémon na **escala real do jogo**,
renderize cada um com `escala = px_por_bloco × baseScale ÷ 16` (`previa2.desenhar`). Use fonte com acentos
(`analisar_geo.fonte()`). Mande as imagens ao usuário; não as ponha no repositório.

## Passo 7: arte oficial x modelo (quando houver arte)
Esse é o passo que ensina a modelar **a partir de uma imagem**.
1. **Fundo:** a arte precisa de fundo transparente ou liso. Se tiver fundo, use
   `python3 -I <skill>/scripts/recortar_arte.py ARTE.png RECORTE.png [--apagar x0,y0,x1,y1] [--fundo R,G,B]`.
   - Os fundos saem das cores que dominam a borda (dá conta de margem branca + fundo preto).
   - Logo, título, fio de moldura ou pedaço de outra figura: apague com `--apagar`.
   - Confira o recorte sobre fundo branco antes de comparar.
2. **Pose:** compare a arte com cada pose. A `render` costuma ganhar: no Blaziken deu 66% contra 52% do parado.
   ```
   python3 -I <skill>/scripts/comparar_arte.py ARTE.png MODELO.geo.json TEXTURA.png --anim ANIM.json --pose render --de-frente --saida folha.png
   ```
   `--de-frente` limita a busca a ângulos de frente/3-4. Sem isso, um manto ou uma capa podem "casar" de costas.
3. **Cores:** `python3 -I <skill>/scripts/cores_por_regiao.py ARTE.png TEXTURA.png`. No Blaziken:
   - o matiz se mantém;
   - a saturação sobe ~1,35x;
   - os claros escurecem (V ≤ ~0,85);
   - cada tom mais claro anda +3° no matiz, -0,045 na saturação e +0,055 no brilho (passo maior para o escuro).

   `cobble_base.rampa_da_arte()` reproduz isso, a ~15 RGB das rampas deles.
4. **Desmontar:**
   - o que **muda o contorno** na arte virou peça; o que é **desenho interno** virou textura;
   - os **membros afunilados** viraram caixas com a largura máxima;
   - uma parte mais larga que a vizinha na arte (a "bota") também é mais larga no modelo.

   Monte a tabela "na arte → no modelo".

## Passo 8: comparar com o modelo do próprio projeto (opcional)
No Galetocraft (ou em qualquer modelo GeckoLib), rode o mesmo `analisar_geo.py` no modelo do projeto. Faça uma
tabela lado a lado: altura no jogo, cubos, faces, textura, cores, planos e cubos girados. O `--estilo` dá o placar
contra o padrão (o Cobblemon fica em 12 de 15 na mediana). Uma imagem "antes x depois" na mesma escala ajuda o
usuário a decidir.

## Passo 9: relatório
Escreva em português, num `.md` no repositório (no Galetocraft: `modelos/referencias/<nome>_cobblemon_engenharia_reversa.md`),
com esta estrutura:
1. **Resumo: o que levar para o projeto** (5–7 lições, com números).
2. **Fonte e licença**: tag, commit, licenças e o que ficou fora do repositório.
3. **Arquivos e montagem**: a tabela dos arquivos e a tabela de poses.
4. **Geometria**: tabela de números (com a linha evolutiva e o modelo do projeto), esqueleto resumido em árvore e
   técnicas encontradas.
5. **Textura**: paleta, shiny, alpha, mosqueado e como a arte virou pixels.
6. **Animações**: tabela e técnicas (períodos, cascata, andar, olhar, escala 0, render, test).
7. **Erros encontrados no arquivo** (se houver).
8. **Medidas por pose.**
9. **Arte x modelo** (se houver arte): pose, tabela "na arte → no modelo" e regra de cor.
10. **O que testar no projeto**: tabela "ideia → de onde vem → efeito esperado".
11. **Como reproduzir**: os comandos exatos.

Confira cada número no dado antes de escrever. Afirmações sobre semântica (o que uma função faz, o que um campo
significa) vão para o relatório só depois de ler o código ou o arquivo.

## Armadilhas que já custaram tempo
- **API do GitLab:** limita requisições e devolve 401/429. Use `git` (clone esparso, `ls-remote`, `ls-tree`,
  `show`), que não sofre esse limite.
- **Argumentos de funções Molang:** podem **substituir** os padrões em vez de multiplicar. Confira no código.
- **Pose de modelagem:** é T. Proporções "estranhas" no repouso (pernas juntas, braços abertos) são normais; a
  postura está no `ground_idle`.
- **Orientação:** no `.geo.json` a frente é -z e o **lado esquerdo da criatura é +x** (o Blockbench espelha o x).
  Em peças que **pendem para baixo**, um `rz` positivo inclina a ponta para dentro; para abrir para fora no lado
  esquerdo, use `rz` negativo.
- **Molang malformado:** um parêntese fora do lugar não quebra o arquivo deles. A ferramenta lê com o parêntese de
  fora e avisa.
- **Busca de ângulo:** pela silhueta, a busca pode escolher a vista de costas. Para arte de frente, use `--de-frente`
  e confira a folha visualmente.
- **Prévia mais escura que o jogo:** amarelos e dourados ficam "mostarda" na prévia. No jogo, com a luz e o
  `_glowmask`, ficam vivos.
- **Imagens com Git LFS:** se o repositório guardar imagens no LFS, o push precisa do host `lfs.github.com` liberado
  na rede do ambiente.

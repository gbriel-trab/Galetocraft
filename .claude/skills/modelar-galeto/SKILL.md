---
name: modelar-galeto
description: >
  Método de trabalho para criar, refazer, revisar ou melhorar um modelo 3D de criatura para Minecraft no estilo do
  Cobblemon: galetos/Cocorídeos do Galetocraft, mobs em Blockbench, .geo.json Bedrock/GeckoLib. Usa um laço com
  portões (bloqueio, ossos, bordas, textura, animação) e, a cada volta, renders de várias vistas, medidas (estilo,
  sobreposição com a arte, peças soltas), um crítico separado com perguntas de sim ou não, anti-padrões citados pelo
  nome e volta à rodada anterior quando a nota cai. Use esta skill sempre que alguém pedir para modelar, desenhar,
  fazer, refazer, corrigir, revisar, criticar ou "melhorar o design" de um galeto, Cocorídeo, mob ou modelo de
  Blockbench, para transformar uma arte ou ficha em modelo, ou perguntar por que um modelo ficou feio, sem vida ou
  diferente da arte, mesmo que a palavra "skill" não apareça.
---

# Modelar um galeto em laço (ver, medir, criticar, corrigir)

O padrão visual é o `modelos/GUIA_ESTILO.md` (o estilo dos modelos do Cobblemon). Esta skill cobre **o método**:
- **o que dá resultado é um laço fechado, não pedir um design melhor.** O modelo lê imagens muito bem; o que costuma
  faltar é ele *ver* o resultado de cada passo;
- **números valem mais que adjetivos;**
- **os defeitos se evitam pelo nome;**
- **um crítico de olhos novos acha o que o autor não vê.**

A pesquisa que embasa o método e as fontes estão em `references/pesquisa.md`. Os scripts ficam em `scripts/`, ao
lado deste arquivo (chamado aqui de `<skill>`). Eles usam Python 3, `numpy` e `pillow`, e também o
`analisar_geo.py` e o `previa2.py`. Procuram esses dois em três lugares, nesta ordem:
1. a cópia em `scripts/` (no pacote instalado);
2. o `ferramentas/` do repositório;
3. a skill `engenharia-reversa-cobblemon`.

## Antes de começar
1. **Esforço.** Modelar é trabalho de esforço alto: peça ao usuário `/effort high` se a sessão estiver no padrão
   (`medium`). Para o bloqueio e a crítica, `xhigh` vale se melhorar a nota. Você não troca o próprio esforço; peça
   uma vez, explique por quê e siga.
2. **Leia o padrão e a referência:**
   - `modelos/GUIA_ESTILO.md`: seções 3, 4, 5, 7 e 13 no mínimo;
   - a arte ou a ficha da espécie (`modelos/referencias/NNN_id_*`);
   - a ponte arte → modelo em `modelos/referencias/blaziken_arte_para_modelo.md`.
3. **Escreva os números antes de modelar.** Fica tudo escrito no plano da rodada:
   - altura pela tabela (`ferramentas/dimensoes.py`);
   - orçamento de cubos, faces, textura e cores para essa altura (guia, seção 3);
   - paleta por `cobble_base.rampa_da_arte()`;
   - as metas: IoU ≥ 60% na pose `render` e `--estilo` ≥ 13/15.
4. **Prepare as imagens.** Recorte a arte (`recortar_arte.py`) e as vistas da ficha em resolução cheia. O modelo
   lê melhor imagem grande e recortada do que miniatura.
5. **Rodadas novas.** Cada volta grava em `modelos/<id>/revisao/` com um prefixo novo. Nunca sobrescreva rodada
   antiga: é ela que permite voltar.
6. **Licença.** Nada do Cobblemon nem da arte oficial de Pokémon entra no repositório (CC BY-NC e Nintendo). Use só
   medidas e técnicas.

## O laço com portões
Cada etapa só começa quando a anterior passa no portão. O motivo é que as etapas de baixo dependem das de cima:
detalhe em cima de proporção errada é trabalho jogado fora. Pela mesma razão, a densidade de texel é fixada no
bloqueio, porque trocá-la depois invalida a UV e a textura.

| etapa | o que fazer | portão |
|---|---|---|
| 1. bloqueio | até ~20 caixas, cor chapada por material, sem planos nem textura | `3_arte` com IoU ≥ 50%; vistas batendo com a ficha de frente, de lado e de costas |
| 2. ossos | hierarquia antes do detalhe, pivô na junta, pose neutra; a postura vem do `parado` | `pecas_soltas.py` sem avisos no `parado` |
| 3. bordas | planos para franjas, chamas, garras, olhos e sobrancelhas | `--estilo` ≥ 13/15 e dentro do orçamento |
| 4. textura | 3 a 5 tons por material, mosqueado leve, `_glowmask` para o que brilha | cores no teto; `4_escala_jogo` legível a 8 blocos |
| 5. animação | parado, andar e piscar; depois grito e dormir | `5_animacoes` e `pecas_soltas.py` nas animações: nada se solta nem afunda |
| 6. jogo | `runClientGameTest` (na nuvem) ou o dono no Windows | captura no jogo parecida com a arte |

Mostre a folha ao usuário no fim do bloqueio e no fim do trabalho. O olho do dono decide o que os números não
decidem.

## Cada volta
1. **Gere a rodada**, por exemplo `python ferramentas/especies/<id>_cobblemon.py <prefixo>NN`. O padrão de gerador é
   o `pirococo_cobblemon.py`.
2. **Meça e monte a folha:**
   ```
   python <skill>/scripts/folha_critica.py MODELO.geo.json TEXTURA.png --anim ANIM.json \
       --saida modelos/<id>/revisao/<rodada>_critica --arte ARTE_RECORTADA.png --ficha-vistas VISTAS.png
   ```
   A folha grava `1_vistas`, `2_rosto`, `3_arte`, `4_escala_jogo` e `5_animacoes`, mais o `perguntas.md` com as
   medidas já preenchidas: estilo, IoU e peças soltas. O `pecas_soltas.py` também roda sozinho.
3. **Olhe você mesmo** primeiro `1_vistas` e `3_arte`, depois o rosto. Recorte e amplie com PIL o que estiver denso
   (pés, mãos, cabeça); julgar uma miniatura engana.
4. **Chame o crítico** (`agents/critico.md`) no fim de cada etapa e antes de entregar. Para retoques pequenos entre
   etapas, basta você mesmo responder às perguntas. Passe ao subagente:
   - os caminhos das imagens, o `perguntas.md` e a arte ou ficha;
   - **nunca** o seu raciocínio ou a sua opinião ("acho que ficou bom"), porque um crítico que recebe a hipótese
     tende a confirmá-la.
5. **Corrija só o que deu "não"**, do defeito maior para o menor. Ao refinar, mude uma coisa por volta, para saber o
   que mexeu na nota.
6. **Compare com a rodada anterior.** Se a IoU, o estilo ou as respostas pioraram, volte para a rodada anterior em
   vez de remendar por cima. Na dúvida, não mexa: acrescentar peças para "melhorar" o que já bate com a arte é o
   jeito mais comum de piorar.
7. **Anote a rodada** em `notas.md` na pasta da folha:
   - as medidas antes e depois;
   - os "não" do crítico;
   - o que mudou;
   - o que fica para a próxima volta.

**Pare quando:**
- os portões passaram;
- as perguntas estão todas em "sim" (ou com um motivo escrito);
- o usuário aprovou.

## Anti-padrões: cite pelo nome
Pedidos vagos ("sem cara de IA", "faça bonito") só trocam um vício por outro; nomear o defeito funciona. Ponha no
plano da rodada os que valem para a espécie. A lista com como reconhecer e como corrigir está em
`references/anti_padroes.md`:
- boneco de caixas;
- escadinha de cubos;
- poeira de cubos;
- fracionado ou UV por face;
- peças soltas;
- manequim;
- olho chapado;
- textura de IA (contorno preto, degradê de travesseiro, ruído forte, cor pura, luz de um lado);
- *mixels*;
- paleta genérica;
- proporção realista;
- detalhe que some na escala do jogo.

**Quando aparecer um defeito novo**, acrescente-o ao `references/anti_padroes.md`. A lista é a memória do projeto
e fica melhor a cada galeto.

## Blockbench
- **A fonte é o gerador em Python** (`cobble_base.py` e `especies/<id>_cobblemon.py`): ele é reproduzível, medível
  e diffável. O Blockbench serve para olhar, retocar à mão e assistir às animações.
- Um ajuste feito à mão no Blockbench precisa voltar para o gerador; senão, a próxima geração o apaga.
- As pontes MCP do Blockbench (para o Claude ver e editar dentro do Blockbench no PC do dono) e os cuidados de
  segurança estão em `references/blockbench_mcp.md`. Na nuvem não há Blockbench nem GPU; os scripts daqui renderizam
  em CPU.

## Scripts
| script | para quê |
|---|---|
| `folha_critica.py` | a folha do crítico num comando: vistas (com a ficha), rosto ampliado, arte e sobreposição, escala do jogo, quadros do parado e do andar, e o `perguntas.md` com as medidas |
| `pecas_soltas.py` | grupos de cubos que não encostam no corpo e o ponto mais baixo, na pose neutra e em 4 quadros de cada animação; sai com código 1 se achar problema |

Ferramentas do repositório que o laço usa:
- `ferramentas/analisar_geo.py --estilo`: os 15 critérios do guia;
- `ferramentas/comparar_arte.py`: a sobreposição com a arte (a folha já chama);
- `ferramentas/cobble_base.py`: modelagem e `rampa_da_arte()`;
- `recortar_arte.py` e `cores_por_regiao.py`, da skill `engenharia-reversa-cobblemon`.

## Referências
- `references/perguntas_critico.md`: as 15 perguntas de sim ou não. A folha copia esse arquivo para o
  `perguntas.md`; edite aqui para mudar todas.
- `references/anti_padroes.md`: os defeitos com nome, como reconhecer e como corrigir.
- `references/pesquisa.md`: por que o método é assim (guia da Anthropic, 3DCodeBench, CADCodeVerify, LL3M,
  3D-PreMise) e as fontes.
- `references/blockbench_mcp.md`: as pontes MCP do Blockbench, o que cada uma faz e os riscos.
- `agents/critico.md`: o pedido para o subagente crítico.

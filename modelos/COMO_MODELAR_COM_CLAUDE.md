# Como fazer o Claude modelar melhor (Blockbench e Minecraft)

Pesquisa de 18/11/2026. Fontes: o guia da Anthropic sobre o modelo atual do Claude Code, as pontes MCP do Blockbench,
artigos de 2024 a 2026 sobre modelagem 3D escrita em código com crítica visual e a nossa experiência com o
Pirococó. O padrão visual continua sendo o `GUIA_ESTILO.md`. Este documento trata do **método de trabalho**.

**A versão para o Claude usar é a skill `.claude/skills/modelar-galeto/`.** Ela traz:
- o laço;
- as perguntas do crítico;
- os anti-padrões, que crescem a cada galeto;
- a `folha_critica.py` e o `pecas_soltas.py`.

Este documento é o relatório da pesquisa.

## Resumo
1. **O ganho vem de um laço fechado, não de pedir "um design melhor".** O laço é: referência, bloqueio, renders de
   várias vistas, crítica por lista de perguntas, correção pequena e nova medida. O modelo atual lê imagens muito
   bem; o que costuma faltar é ele **ver** o resultado de cada passo.
2. **Suba o esforço para modelar.** O padrão do modelo é `medium`. Para criar ou refazer um galeto, use `/effort high`
   (ou `claude --effort high`). Para o bloqueio e a crítica, `xhigh` vale a pena se melhorar a nota medida. Com mais
   esforço, ele usa melhor as ferramentas de imagem (recortar, ampliar, medir).
3. **Diga o que evitar, pelo nome.** Pedidos vagos como "sem cara de IA" só trocam um vício por outro. Funciona
   listar os defeitos concretos (seção 6) e aumentar a lista a cada rodada com o que apareceu.
4. **Use números em vez de adjetivos.** Altura da tabela, orçamento do guia, `--estilo`, sobreposição com a arte
   (IoU) e paleta por `rampa_da_arte()`. Um critério que dá para medir não depende do "olho" do modelo.
5. **Use um crítico separado.** Um subagente sem o raciocínio do autor olha as imagens e responde a perguntas de sim
   ou não, e o autor corrige só os "não". Se a nota cair, volte para a versão anterior.

## 1. O que o modelo faz bem e o que ainda falha
**Pelo guia da Anthropic** (notas de migração do modelo atual):
- Lê gráficos, diagramas e capturas de tela com muito mais precisão que os anteriores, mesmo com pouco esforço.
- Em entradas densas (desenho técnico, folha de vistas), duas coisas ainda ajudam:
  - imagens em resolução maior;
  - ferramentas de imagem, como PIL e OpenCV, para recortar, ampliar e medir.

  Ele usa essas ferramentas melhor com esforço mais alto.
- Sem direção de design, ele cai em alguns estilos padrão. Responde bem a listas que **nomeiam** os padrões a evitar.
  O método é olhar o que saiu e acrescentar à lista.
- O pensamento está sempre ligado e o esforço é o controle. Para pensar menos, baixe o esforço em vez de pedir
  "pense menos".

**Pela pesquisa sobre modelagem 3D escrita em código:**
- **3D-PreMise** (2024, GPT-4 com Blender):
  - o modelo olhava o render e corrigia pouco;
  - deixava passar erros de bom senso, como uma perna da cadeira fora do assento;
  - às vezes inventava defeitos.

  Conclusão: a crítica visual sem perguntas guiadas é fraca.
- **CADCodeVerify:** o modelo cria perguntas de verificação, responde a cada uma olhando o render e corrige só o que
  deu "não" ou "não sei". Assim, o que está certo não é mexido.
- **LL3M** (Blender): quatro agentes, com planejador, buscador, programador e crítico. O crítico olha os renders, mas
  ainda perde defeitos espaciais sutis, e a correção humana fecha o que sobra.
- **3DCodeBench** (2026, 12 modelos de visão gerando código de Blender):
  - as falhas mais comuns são erros de API e **peças soltas ou flutuando**;
  - o que mais faz o resultado dar certo é **refinar em várias voltas**, com renders de várias vistas comparados à
    referência.
- **Relatos sobre o Blender MCP:** o resultado é bom em formas retas e geométricas. Os erros de colisão e de câmera
  vêm de comandos dados sem conferir o resultado intermediário.

**Na nossa experiência (Pirococó g3):**
- a sobreposição com a arte em 3/4 ficou em 48%, porque o manto e as caudas finas ficam mais "cheios" em blocos;
- as vistas ortográficas da ficha bateram bem;
- lição: confira frente, lado e costas, não só a pose de destaque.

## 2. Pontes entre o Claude e o Blockbench (MCP)
Nenhuma é oficial do Blockbench; todas são de terceiros. Leia o código antes de instalar.

| projeto | como funciona | o que oferece | riscos |
|---|---|---|---|
| `jasonjgardner/blockbench-mcp-plugin` (GPL-3.0) | plugin do Blockbench desktop (HTTP em `localhost:3000/bb-mcp`) e um servidor *headless* (`npx -y github:jasonjgardner/blockbench-mcp-plugin --root PASTA`) | ver abaixo | servidor sem senha; `risky_eval` executa JavaScript no Blockbench |
| `enfp-dev-studio/blockbench-mcp` | plugin (*socket* na porta 9999) e servidor Node | criar, apagar e editar cubos; ler o modelo | o plugin executa código no Blockbench |

O servidor *headless* do projeto `jasonjgardner` oferece:
- `bbmodel_validate`: procura peças soltas, peças que se cruzam, lascas, simetria quebrada e as regras do GeckoLib;
- `bbmodel_validate_animations`: procura partes que afundam no chão e membros que se soltam do pai;
- `bbmodel_sample_pose`;
- `bbmodel_render` e `bbmodel_contact_sheet`: PNG de uma ou várias vistas (precisam de GPU e Node 23.6 ou mais
  novo);
- exportação de `.geo.json` e de animação Bedrock.

O projeto irmão `jasonjgardner/blockbench-mcp-project` traz *skills* para o Claude, com regras que valem para nós:
- **Proporção e silhueta antes** de detalhe, UV, textura e animação. Defina a densidade de texel no bloqueio, porque
  trocar depois invalida a UV e a textura.
- **Hierarquia de ossos antes da geometria**, com o pivô na junta.
- **Detalhe fino em plano**, não em cubos recortados.
- **Textura esticada se corrige remapeando a UV**, não com mais cubos.
- **Mude só a área pedida** num modelo que já existe.
- **Uma foto da pose parada não confere um ciclo de andar:** veja vários quadros e a emenda do loop.

Ainda no `jasonjgardner/blockbench-mcp-project`, há uma *skill* que gera textura com IA de imagem. Não serve para nós,
porque foge da paleta medida e precisa de uma chave externa.

**Cuidados de segurança, se instalar no PC do dono:**
- deixe o servidor só em `127.0.0.1`, nunca em `0.0.0.0`;
- desligue o "Enable risky_eval" nas configurações.

**Onde isso entra no Galetocraft:**
- **O gerador em Python (`cobble_base.py` e `especies/*_cobblemon.py`) continua sendo a fonte.** Ele é reproduzível,
  medível e diffável, e é o que o Claude faz melhor: escrever e corrigir código.
- O Blockbench serve para olhar, retocar à mão e assistir às animações. Um ajuste feito no Blockbench precisa voltar
  para o gerador; senão, a próxima geração o apaga.
- **Na nuvem** não há Blockbench nem GPU, mas os nossos renders em CPU (`analisar_geo.py`, `comparar_arte.py`) já
  dão as vistas.
- **No Windows do dono, com o Blockbench aberto**, o MCP permitiria ao Claude Code local ver o modelo no próprio
  Blockbench. Vale testar o `bbmodel_validate` e o `bbmodel_contact_sheet` como segunda opinião.

## 3. O laço de trabalho, com portões
Uma etapa só começa quando a anterior passa no portão. Cada volta grava uma rodada nova em
`modelos/<id>/revisao/` (prefixo novo). Se uma correção piora a nota, **volte para a rodada anterior** em vez de
remendar por cima.

| etapa | o que fazer | portão (medido) |
|---|---|---|
| 0. preparar | `/effort high`; arte e ficha em resolução cheia; vistas recortadas (`recortar_arte.py`); altura pela tabela (`dimensoes.py`); orçamento pelo guia; paleta por `rampa_da_arte()` | números escritos antes de modelar |
| 1. bloqueio | até ~20 caixas, cor chapada por material, sem planos nem textura | `comparar_arte.py` com IoU ≥ 50% e vistas da ficha batendo (frente, lado e costas) |
| 2. ossos | hierarquia e pivôs nas juntas; pose neutra; a postura vem do `parado` | `--pose` em 4 tempos do `parado`: nada afunda nem se solta |
| 3. bordas | planos para franjas, chamas, garras, olhos e sobrancelhas | `--estilo` ≥ 13/15 e dentro do orçamento |
| 4. textura | 3 a 5 tons por material, mosqueado leve, `_glowmask` | cores dentro do teto; `--escala-jogo` legível a 1 e a 8 blocos |
| 5. animação | parado, andar e piscar; depois grito e dormir | quadros ao longo do ciclo e a emenda do loop; o piscar esconde o olho |
| 6. jogo | `runClientGameTest` (na nuvem) ou o dono no Windows | captura no jogo parecida com a arte |

## 4. Como o Claude deve olhar as imagens
- **Uma folha na mesma escala:** arte, modelo e sobreposição (a `folha()` do `comparar_arte.py`), mais as vistas
  ortográficas e o rosto ampliado. O rosto decide o carisma.
- **Resolução:** cerca de 1.024 px por vista para inspecionar. Recorte e amplie as regiões densas (cabeça, pés,
  mãos) em vez de julgar tudo numa miniatura.
- **Perguntas de sim ou não** (seção 5), respondidas olhando a imagem. Corrija só o que deu "não".
- **Crítico de olhos novos:** um subagente recebe a folha, a ficha e a lista de perguntas, mas não o raciocínio do
  autor nem a opinião dele ("acho que ficou bom"). Ele devolve os defeitos com o local; o autor corrige.
- **Seja conservador:** se a vista já bate com a arte, não "melhore" acrescentando peças. O 3DCodeBench usa o mesmo
  viés: na dúvida, não corrija.

## 5. Perguntas do crítico (sim ou não)
**Silhueta e proporção**
- Dá para reconhecer a criatura só pela sombra, de frente e de lado?
- A proporção entre cabeça, tronco e pernas é a da arte, e não a de um galo "realista"?
- Os pés tocam o chão? Alguma peça está solta, flutuando ou atravessando outra sem querer?
- A simetria só aparece onde a arte é simétrica?
- Os elementos marcantes da ficha estão todos lá: crista, barbela, cauda, manto, chamas?

**Rosto**
- O olho tem pálpebra (para piscar) e a posição da pupila dá a expressão da arte?
- O bico e os olhos estão centrados e na altura da arte?

**Bordas e geometria**
- As franjas, penas e chamas são planos com recorte na textura, e não escadinhas de cubos?
- Alguma curva foi feita com degraus de cubos pequenos onde um plano girado ou a textura resolveria?
- Os tamanhos são inteiros, a UV é de caixa e há poucos cubos girados?

**Textura**
- Cada material tem 3 a 5 tons, sem contorno preto, sem degradê de "travesseiro" (claro no meio) e sem luz
  direcional pintada?
- O texel é sempre 1/16 de bloco, sem *mixels* (UV esticada ou pixels de tamanhos diferentes)?
- As cores seguem a arte pela `rampa_da_arte()` e ficam dentro do teto de cores?

**No jogo**
- Na escala do jogo, a 8 blocos, ainda se reconhece a espécie e o tipo (fogo, água...)?

## 6. Anti-padrões: cite pelo nome no pedido
Comece por estes e acrescente o que aparecer de errado em cada rodada:
- **Boneco de caixas:** tronco, cabeça e pernas em 5 a 15 caixas lisas, sem planos de borda.
- **Escadinha de cubos** para fazer curva.
- **Poeira de cubos:** muitos cubos de 1 px imitando um detalhe que a textura faria.
- **Tamanhos fracionados, UV por face ou muitos cubos girados.** Nos 78 modelos do Cobblemon medidos, há 0
  fracionados e só cerca de 5% de cubos girados.
- **Peças soltas:** flutuando, enfiadas no chão, ou asas e caudas sem ligação com o corpo.
- **Manequim:** simetria perfeita e corpo duro no `parado`.
- **Olho chapado:** olho pintado sem pálpebra nem pupila em plano.
- **Textura de IA:** contorno preto, degradê de travesseiro, ruído forte, cores puras como (255, 0, 0), mais de ~55
  cores, luz pintada de um lado.
- **Mixels:** texels de tamanhos diferentes.
- **Paleta genérica:** cores que fogem da arte.
- **Proporção "realista"** no lugar da proporção da arte.

## 7. Modelo de pedido para o chat de design
```
/effort high
Tarefa: modelar o <galeto> no padrão do modelos/GUIA_ESTILO.md, a partir de <arte.png> (pose neutra; postura no `parado`).
Números: altura <x> blocos (dimensoes.py); orçamento do guia para essa altura; paleta por rampa_da_arte().
Método: modelos/COMO_MODELAR_COM_CLAUDE.md — laço com portões (bloqueio → ossos → bordas → textura → animação),
uma rodada nova em revisao/ por volta, voltar se a nota cair.
A cada volta: folha (arte | modelo | sobreposição) + vistas frente/lado/costas + rosto ampliado; responder às
perguntas da seção 5; um subagente crítico revisa sem saber da minha opinião.
Evite: <anti-padrões da seção 6 + os que apareceram na rodada anterior>.
Pronto quando: IoU ≥ 60% na pose `render`, --estilo ≥ 13/15, todas as perguntas com "sim".
```

## 8. O que não ajuda
- Pedir "faça bonito" ou "sem cara de IA" sem nomear os defeitos.
- Pedir "pense menos" em vez de baixar o esforço, ou deixar o esforço no padrão para um modelo novo.
- Julgar só pela pose de destaque em 3/4.
- Corrigir tudo de uma vez: mude uma coisa por volta, para saber o que melhorou a nota.
- Gerar a textura com IA de imagem: ela foge da UV de caixa e da paleta medida.
- Copiar geometria, textura ou animação do Cobblemon (licença CC BY-NC e Pokémon da Nintendo). Aqui só entram
  medidas e técnicas.

## 9. Próximos passos sugeridos (1 e 2 feitos na skill `modelar-galeto`)
1. **Detector de peças soltas no `analisar_geo.py`:**
   - cubo que não toca nem atravessa outro cubo do mesmo osso ou do pai;
   - pé acima ou abaixo do chão na pose `parado`;
   - ver isso em vários tempos da animação.

   É a falha nº 1 do 3DCodeBench, e o `bbmodel_validate` faz algo parecido.
2. **Folha de crítica num comando só:**
   - 6 vistas e o rosto ampliado;
   - a escala do jogo e a arte lado a lado;
   - as perguntas da seção 5 num `.md` para o subagente crítico.
3. **Modo `--bloqueio` no `cobble_base`:** cor chapada por material, para o portão da etapa 1.
4. **No Windows do dono:** testar o servidor *headless* do `blockbench-mcp-plugin`
   (`bbmodel_validate` e `bbmodel_contact_sheet`) como segunda opinião, com o `risky_eval` desligado.

## Fontes
- Anthropic, guia de migração e de prompts do modelo atual: esforço, visão e a regra de "nomear os padrões a evitar"
  (consultado pela *skill* `claude-api` do Claude Code).
- [jasonjgardner/blockbench-mcp-plugin](https://github.com/jasonjgardner/blockbench-mcp-plugin) e o
  [README do servidor *headless*](https://github.com/jasonjgardner/blockbench-mcp-plugin/blob/main/headless/README.md).
- [jasonjgardner/blockbench-mcp-project](https://github.com/jasonjgardner/blockbench-mcp-project), *skills*
  [blockbench-use](https://github.com/jasonjgardner/blockbench-mcp-project/blob/main/skills/blockbench-use/SKILL.md) e
  [blockbench-modeling](https://github.com/jasonjgardner/blockbench-mcp-project/blob/main/skills/blockbench-modeling/SKILL.md).
- [enfp-dev-studio/blockbench-mcp](https://github.com/enfp-dev-studio/blockbench-mcp).
- [3D-PreMise (arXiv 2401.06437)](https://arxiv.org/pdf/2401.06437).
- [CADCodeVerify (arXiv 2410.05340)](https://arxiv.org/html/2410.05340v1).
- [LL3M (arXiv 2508.08228)](https://arxiv.org/html/2508.08228v1).
- [3DCodeBench (arXiv 2606.01057)](https://huggingface.co/papers/2606.01057).
- [Guia de estilo Minecraft do Blockbench](https://www.blockbench.net/wiki/guides/minecraft-style-guide): planos com
  transparência no lugar de muitos cubos pequenos; *mixels*.
- [Tutorial de modelo do Cobblemon (wiki)](https://wiki.cobblemon.com/index.php/Tutorials/Creating_A_Model).
- [Guia honesto do Blender MCP](https://www.3daistudio.com/3d-generator-ai-comparison-alternatives-guide/blender-mcp).

Os artigos do arXiv e o site do Blockbench estão bloqueados pela rede desta sessão. Os pontos deles vieram dos
resumos da busca, não do texto completo.

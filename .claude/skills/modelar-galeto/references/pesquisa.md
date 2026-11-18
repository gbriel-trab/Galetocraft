# Por que o método é assim

Pesquisa de 18/11/2026. O relatório completo, para leitura humana, está em `modelos/COMO_MODELAR_COM_CLAUDE.md` no
repositório Galetocraft.

## O modelo (guia da Anthropic para o modelo atual do Claude Code)
- **Visão:** lê gráficos, diagramas e capturas de tela com muito mais precisão que os modelos anteriores, mesmo com
  pouco esforço. Em entradas densas (desenho técnico, folha de vistas), ainda ajudam:
  - imagens em resolução maior;
  - ferramentas de imagem (PIL ou OpenCV para recortar, ampliar e medir), que ele usa melhor com esforço alto.
- **Design:** sem direção, ele cai em alguns estilos padrão, e "evite cara de IA" só troca um padrão por outro. Ele
  responde bem a listas que **nomeiam** os padrões a evitar. O método é olhar o que saiu e aumentar a lista; daí
  vem o `anti_padroes.md`.
- **Esforço:**
  - o padrão é `medium`, e o pensamento está sempre ligado;
  - o esforço é o controle de quanto ele pensa;
  - para pensar menos, baixe o esforço em vez de pedir "pense menos";
  - reserve `xhigh` e `max` para quando a melhora for medida.

## Pesquisa sobre modelagem 3D escrita em código
- **3D-PreMise** (2024, GPT-4 com Blender): com o render de volta, o modelo corrigia pouco, deixava passar erros de
  bom senso e às vezes inventava defeitos. Conclusão: a crítica visual solta, sem perguntas, é fraca. Daí vêm as
  perguntas de sim ou não.
- **CADCodeVerify:** o modelo cria perguntas de verificação, responde a cada uma olhando o render e corrige só o que
  deu "não" ou "não sei"; o que está certo não é mexido. Daí vem "corrija só os não".
- **LL3M** (Blender, quatro agentes: planejador, buscador, programador e crítico): o crítico olha os renders, mas
  perde defeitos espaciais sutis, e a correção humana fecha o resto. Daí vêm o crítico separado e a aprovação do
  dono.
- **3DCodeBench** (2026, 12 modelos de visão gerando código de Blender):
  - as falhas mais comuns são erros de API e **peças soltas ou flutuando**, daí vem o `pecas_soltas.py`;
  - o que mais faz dar certo é **refinar em várias voltas** com renders de várias vistas comparados à referência,
    daí vêm o laço e a folha;
  - o laço tem um viés conservador (na dúvida, não corrija).
- **Relatos sobre o Blender MCP:** o resultado é bom em formas retas e geométricas. Os erros de colisão e de câmera
  vêm de comandos dados sem conferir o resultado intermediário: ver cada passo importa.

## Pontes MCP do Blockbench
Veja `blockbench_mcp.md`. As *skills* do projeto `jasonjgardner/blockbench-mcp-project` chegam às mesmas regras:
- proporção e silhueta antes do detalhe;
- ossos antes da geometria;
- detalhe fino em plano;
- remapear a UV em vez de pôr mais cubos;
- conferir as animações em vários quadros.

## Na prática (Pirococó g3, 18/11/2026)
- **Medidas:** 83 cubos, 15/15 no `--estilo` e IoU de 48% com a arte. O manto e as caudas finas ficam "cheios" em
  blocos.
- **O `pecas_soltas.py`, na primeira execução, achou três defeitos que ninguém tinha visto:**
  - o dedo do meio dos dois pés fica 0,5 px à frente do pé;
  - a base da cauda se descola 0,37 px no andar;
  - os pés afundam 1,1 px no andar.
- **Lição:** compare as vistas de frente, lado e costas, não só a pose de destaque.

## Fontes
- [jasonjgardner/blockbench-mcp-plugin](https://github.com/jasonjgardner/blockbench-mcp-plugin).
- [jasonjgardner/blockbench-mcp-project](https://github.com/jasonjgardner/blockbench-mcp-project).
- [enfp-dev-studio/blockbench-mcp](https://github.com/enfp-dev-studio/blockbench-mcp).
- [3D-PreMise (arXiv 2401.06437)](https://arxiv.org/pdf/2401.06437).
- [CADCodeVerify (arXiv 2410.05340)](https://arxiv.org/html/2410.05340v1).
- [LL3M (arXiv 2508.08228)](https://arxiv.org/html/2508.08228v1).
- [3DCodeBench (arXiv 2606.01057)](https://huggingface.co/papers/2606.01057).
- [Guia de estilo Minecraft do Blockbench](https://www.blockbench.net/wiki/guides/minecraft-style-guide).
- [Tutorial de modelo do Cobblemon](https://wiki.cobblemon.com/index.php/Tutorials/Creating_A_Model).

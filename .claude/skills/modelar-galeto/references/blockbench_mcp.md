# Pontes MCP entre o Claude e o Blockbench

Pesquisa de 18/11/2026. Nenhuma ponte é oficial do Blockbench; todas são de terceiros. Leia o código antes de
instalar.

## jasonjgardner/blockbench-mcp-plugin (GPL-3.0)
**Plugin do desktop:**
- instale em File > Plugins > Load Plugin from URL com
  `https://jasonjgardner.github.io/blockbench-mcp-plugin/mcp.js`;
- ele abre um servidor HTTP em `localhost:3000/bb-mcp`;
- o README traz exemplos de configuração para o Claude Code e o Claude Desktop.

**Servidor *headless*** (sem o Blockbench aberto): `npx -y github:jasonjgardner/blockbench-mcp-plugin --root PASTA`.
Ferramentas úteis para nós:
- `bbmodel_validate`: procura peças soltas, peças que se cruzam, lascas, limites de bloco e simetria quebrada, e
  aplica as regras do GeckoLib;
- `bbmodel_validate_animations`: procura partes que afundam no chão e membros que se soltam do pai;
- `bbmodel_sample_pose`: posição dos ossos num instante da animação;
- `bbmodel_render` e `bbmodel_contact_sheet`: PNG de uma ou várias vistas. Precisam de Node 23.6 ou mais novo e de
  GPU, e baixam cerca de 130 MB na primeira vez;
- `bbmodel_export_bedrock_geometry` e `bbmodel_export_bedrock_animation`.

Ele trabalha com `.bbmodel`. Para o nosso `.geo.json`, abra-o no Blockbench e salve como projeto.

**Riscos:**
- o servidor não tem senha: quem alcança a porta usa todas as ferramentas;
- o `risky_eval` executa JavaScript dentro do Blockbench.

**Use assim:**
- o servidor fica só em `127.0.0.1` (o padrão), nunca em `0.0.0.0`;
- desligue Settings > General > "Enable risky_eval".

## jasonjgardner/blockbench-mcp-project (*skills*)
*Skills* para o Claude usar a ponte acima: `blockbench-use`, `blockbench-modeling`, `blockbench-texturing` e
`blockbench-animation`. Regras que batem com o nosso método:
- proporção e silhueta antes de detalhe, UV, textura e animação;
- densidade de texel definida no bloqueio;
- hierarquia de ossos antes da geometria, com o pivô na junta;
- detalhe fino em plano;
- textura esticada se corrige remapeando a UV, não com mais cubos;
- mude só a área pedida num modelo que já existe;
- uma foto da pose parada não confere um ciclo de andar.

A *skill* de textura gerada por IA de imagem (GPT Image, via fal.ai) **não serve para nós**: ela foge da UV de
caixa e da paleta medida, e precisa de uma chave externa.

## enfp-dev-studio/blockbench-mcp
Plugin com *socket* na porta 9999 e um servidor Node. Cria, apaga e edita cubos e lê o modelo. O plugin executa
código no Blockbench; os cuidados são os mesmos.

## Onde isso entra no Galetocraft
- **O gerador em Python continua sendo a fonte.** O Blockbench é para olhar, retocar e assistir às animações.
- **No Windows do dono, com o Blockbench aberto**, o MCP deixa o Claude Code local ver o modelo no próprio
  Blockbench. Vale testar o `bbmodel_validate` e o `bbmodel_contact_sheet` como segunda opinião, ao lado do
  `pecas_soltas.py` e da `folha_critica.py`.
- **Na nuvem** não há Blockbench nem GPU: use os scripts desta skill, que renderizam em CPU.
- Não instale nada disso sem pedido do dono. É software de terceiros com acesso ao Blockbench.

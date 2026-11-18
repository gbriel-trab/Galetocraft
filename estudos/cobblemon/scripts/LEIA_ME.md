# Scripts de medição do estudo

Os scripts esperam uma pasta de trabalho `<P>`, com os assets do Cobblemon extraídos das 3 árvores do repositório
público https://gitlab.com/cable-mc/cobblemon:

| pasta | o que vai nela | caminho no repositório |
|---|---|---|
| `<P>/repo/M` | modelos | `common/src/main/resources/assets/cobblemon/bedrock/pokemon/models` |
| `<P>/repo/P` | posers | `common/src/main/resources/assets/cobblemon/bedrock/pokemon/posers` |
| `<P>/repo/A` | animações | `common/src/main/resources/assets/cobblemon/bedrock/pokemon/animations` |
| `<P>/repo/R` | resolvedores | `common/src/main/resources/assets/cobblemon/bedrock/pokemon/resolvers` |
| `<P>/tex/T` | texturas | `common/src/main/resources/assets/cobblemon/textures/pokemon` |
| `<P>/sp/S` | dados de espécie | `common/src/main/resources/data/cobblemon/species` |

Cada árvore baixa em `.tar.gz` pela API do GitLab:

`https://gitlab.com/api/v4/projects/cable-mc%2Fcobblemon/repository/archive.tar.gz?sha=main&path=<caminho>`

Os scripts:

- `python -I medir_geral.py <P>`: estatística global (cubos, planos, rotações, inflate, texturas, nomes de ossos).
  Grava `<P>/stats.json`.
- `python -I medir_aves.py <P>`: tabela de aves e criaturas de fogo (tamanho, cubos, baseScale, altura no jogo).
  Usa o `stats.json` do script anterior.

Os renders do estudo foram feitos com `ferramentas/render_geo.py`, na pose do 1º quadro do `ground_idle`.

Os assets do Cobblemon têm licença Creative Commons não comercial e **não** são versionados aqui.

# Prompts de modelagem: como usar

**A divisão de trabalho:**

- **Este chat** (planejamento) analisa a ficha, define as proporções e escreve os prompts.
- **Outro chat do Claude** (modelagem) gera os arquivos do modelo.
- **Você** leva o prompt de um para o outro e traz o resultado de volta.

## Arquivos

| arquivo | o que é |
|---|---|
| `mestre.md` | regras gerais: estilo Cobblemon, formato GeckoLib, fluxo de trabalho, autoavaliação. Vale para todas as criaturas |
| `criaturas/<id>.md` | ficha da criatura: medidas, peças, ossos, paleta, animação, pontos de reprovação |
| `montar.py` | junta mestre + criatura + renderizador num arquivo só |
| `prontos/<id>_vN.md` | **o prompt pronto para colar** |
| `correcao_modelo.md` | esqueleto dos prompts de correção e como eu diagnostico |
| `correcoes/<id>_cNN.md` | as correções já escritas, uma por rodada |

Para remontar depois de mudar o mestre ou a criatura:

```
python prompts/montar.py pirococo "Pirococó" 2
```

## Ciclo

**1. Abra um chat novo do Claude** com **execução de código / criação de arquivos** ligada. Sem isso, ele não
consegue rodar o script gerador nem o renderizador.

**2. Anexe** (tudo o que está em `prompts/anexos/<id>_vN/`, quando houver):

- **A ficha da criatura** (ex.: `modelos/referencias/001_pirococo_anime_ficha.png`).
- **Opcional, mas ajuda muito:** `estudos/cobblemon/imagens/galeria_aves.png` e `rostos_cabecas.png`, como
  referência de acabamento.

**3. Cole o conteúdo inteiro de `prompts/prontos/<id>_vN.md`.**

**4. Quando ele terminar, traga para cá:**

- **O mínimo:** a imagem completa do resultado (`<id>_vistas.png`, ou um print do jogo).
- **O melhor:** os arquivos também (`.geo.json`, `.png`, `.animation.json`). Com eles eu renderizo e meço em vez de
  estimar pela imagem.

**5. Eu escrevo a correção** (`prompts/correcoes/<id>_cNN.md`). Cole-a **na mesma conversa** do outro chat, para ele
continuar do próprio script, e anexe a imagem que você me mostrou.

**6. Repita até aprovar.** Os arquivos aprovados vão para:

- `galetocraft/src/main/resources/assets/galetocraft/geckolib/models/entity/<id>.geo.json`
- `.../geckolib/animations/entity/<id>.animation.json`
- `.../textures/entity/<id>.png` e `<id>_glowmask.png`

## Referências

- **Estudo do estilo:** `estudos/cobblemon/estudo_estilo_cobblemon.md`.
- **Proporções do Pirococó:** `modelos/pirococo/proporcoes_anime.md` e `proporcoes_anime_planta.png`.
- **Renderizador** (o mesmo que vai no prompt): `ferramentas/render_geo.py`.

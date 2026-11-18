# Galetocraft: memória do projeto

Mod de Minecraft Java **1.21.11** (Fabric + GeckoLib 5.4.5) com galos-monstro, os **Cocorídeos**. Tudo em
português: textos, nomes de ossos, identificadores e comentários.

## Padrão visual (obrigatório)
**Todo modelo segue `modelos/GUIA_ESTILO.md`: o estilo dos modelos do Cobblemon dentro do Minecraft.** Leia o
guia antes de criar, refazer ou revisar qualquer modelo. Resumo:
- 1 unidade = 1 texel = 1/16 de bloco (escala 1: o modelo nasce na altura da tabela). UV de caixa, tamanhos inteiros.
- Poucas caixas grandes na massa e planos (espessura 0) nas bordas: franjas, chamas, garras, olhos e sobrancelhas.
- Orçamento por altura no jogo. Ex.: 2–3 blocos ≈ 100 cubos, ≤ 530 faces, textura 256x128 e ≤ 55 cores.
- Textura: 3–5 tons por material, mosqueado leve, quase sem luz pintada; shiny só troca a paleta;
  `_glowmask` para o que brilha.
- Modele em pose neutra; a postura vem do `parado`. Animações obrigatórias: parado, andar e piscar (pálpebra
  escondida); recomendadas: grito e dormir.
- Confira com `python ferramentas/analisar_geo.py MODELO.geo.json TEXTURA.png --anim ANIM.json --estilo`.
- **Método de trabalho:** `modelos/COMO_MODELAR_COM_CLAUDE.md`. Modele com `/effort high` e em laço com portões:
  bloqueio, ossos, bordas, textura e animação. A cada volta, gere a folha de vistas, responda às perguntas do crítico
  e use um subagente crítico sem o raciocínio do autor. Cite pelo nome os anti-padrões a evitar e volte para a
  rodada anterior se a nota cair.
- **Galetos novos partem de UMA ilustração no estilo da arte oficial dos Pokémon** (guia, seção 13): pose neutra
  com as proporções da arte, cores por `cobble_base.rampa_da_arte()`, animação `render` que recria a pose da
  arte, conferida com `ferramentas/comparar_arte.py` (IoU ≥ 60%). Exemplo: `referencias/blaziken_arte_para_modelo.md`.
  Arte oficial de Pokémon não entra no repositório.
- **O Cobblemon é a única referência de estilo.** As regras antigas do dono (`ferramentas/especies/BRIEFING.md`,
  `REFAZER.md`, `REVISAO.md`, `AUDITORIA.md`, `JUIZ.md`) não valem mais onde divergirem do guia, por decisão
  dele.
- A ficha (`modelos/referencias/NNN_id_*.png`) só define **qual** criatura é: silhueta, cores principais e
  elementos marcantes. Simplificar como o Cobblemon simplifica a arte oficial é o esperado.

## Skills do projeto
- `.claude/skills/engenharia-reversa-cobblemon/`: o processo de engenharia reversa de um modelo do Cobblemon
  (feito com o Blaziken e o Combusken): baixar, medir geometria/textura/animações, comparar a arte oficial com
  o modelo e escrever o relatório. Traz os scripts juntos e os números de referência.

## Onde fica cada coisa
- `galetocraft/`: o mod. `GaloRenderer.java` desenha (com LOD e brilho); os modelos e as animações GeckoLib estão
  em `src/main/resources/assets/galetocraft/geckolib/`.
- **Padrão novo:** `ferramentas/cobble_base.py` (biblioteca) e `ferramentas/especies/pirococo_cobblemon.py` (piloto
  aprovável e exemplo; `python ... cbNN --mod`). Saída em `modelos/<id>/cobblemon/`, rodadas `cbNN_*` em
  `modelos/<id>/revisao/`. No `.geo.json`, o lado esquerdo da criatura fica em +x.
- Padrão antigo (ainda nas outras 11 espécies): `ferramentas/especies/<id>.py` sobre `ferramentas/galo_base.py`.
  Não rode `exportar_especie.py pirococo`: ele sobrescreveria o piloto no mod.
  - `ferramentas/exportar_especie.py` exporta para o mod;
  - `ferramentas/dimensoes.py` tem a tabela oficial de alturas;
  - `ferramentas/comparar_ficha.py` mede IoU e cor contra a ficha.
- `modelos/<id>/`: o `.bbmodel`, a textura, `detalhes.md`, as auditorias e `revisao/` (rodadas, no Git LFS).
- `modelos/referencias/`: as fichas do dono (`NNN_id_*.png`) e os estudos do Cobblemon
  (`blaziken_…` e `combusken_cobblemon_engenharia_reversa.md`).
- A base documental vigente é `Galetocraft/Base_Atual/Galetocraft.sqlite`, publicada nas Releases (veja o
  `README.md`).

## Cuidados
- **Nunca** copie arquivos, geometria, textura ou animação do Cobblemon para o repositório. Os modelos deles são
  CC BY-NC 3.0 e os Pokémon são da Nintendo. Estude fora do repositório; aqui só entram medidas e técnicas.
- O dono roda no Windows (Java 25 para o Gradle). Não rode o Gradle nem o Minecraft sem pedido.
- Na nuvem, o ambiente "Galetocraft" já libera Fabric, GeckoLib, Mojang e o LFS do GitHub, e instala Java 25, Xvfb e
  Mesa. Dentro de `galetocraft/`:
  - compilar: `JAVA_HOME=/usr/lib/jvm/java-25-openjdk-amd64 ./gradlew build`;
  - testar no jogo: `JAVA_HOME=... xvfb-run -a -s "-screen 0 1920x1080x24" ./gradlew runClientGameTest`. Os prints
    saem em `build/run/clientGameTest/screenshots/`. O teste do Pirococó passa; a galeria pode estourar o tempo de
    criar o mundo com OpenGL por software.
- Não sobrescreva rodadas antigas em `modelos/<id>/revisao/`; use um prefixo novo.

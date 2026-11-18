# Galetocraft: memória do projeto

Mod de Minecraft Java **1.21.11** (Fabric + GeckoLib 5.4.5) com galos-monstro, os **Cocorídeos**. Tudo em
português: textos, nomes de ossos, identificadores e comentários.

## Padrão visual (obrigatório)
**Todo modelo segue `modelos/GUIA_ESTILO.md`: o estilo dos modelos do Cobblemon dentro do Minecraft.** Leia o
guia antes de criar, refazer ou revisar qualquer modelo. Resumo:
- 1 unidade = 1 texel. UV de caixa, tamanhos inteiros, escala só no renderizador.
- Poucas caixas grandes na massa e planos (espessura 0) nas bordas: franjas, chamas, garras, olhos e sobrancelhas.
- Orçamento por altura no jogo. Ex.: 2–3 blocos ≈ 100 cubos, ≤ 530 faces, textura 256x128 e ≤ 55 cores.
- Textura: 3–5 tons por material, mosqueado leve, quase sem luz pintada; shiny só troca a paleta;
  `_glowmask` para o que brilha.
- Modele em pose neutra; a postura vem do `parado`. Animações obrigatórias: parado, andar e piscar (pálpebra
  escondida); recomendadas: grito e dormir.
- Confira com `python ferramentas/analisar_geo.py MODELO.geo.json TEXTURA.png --anim ANIM.json --estilo`.
- As regras de gosto do dono continuam valendo: fidelidade à ficha, rosto orgânico, olhar imponente e modelo
  sem entulho (`ferramentas/especies/BRIEFING.md`, `REFAZER.md`, `REVISAO.md`). Onde as regras técnicas antigas
  conflitam com o guia, vale o guia (seção 9).

## Onde fica cada coisa
- `galetocraft/`: o mod. `GaloRenderer.java` desenha (com LOD e brilho); os modelos e as animações GeckoLib estão
  em `src/main/resources/assets/galetocraft/geckolib/`.
- `ferramentas/especies/<id>.py`: o gerador de cada espécie, sobre `ferramentas/galo_base.py`.
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
- Não sobrescreva rodadas antigas em `modelos/<id>/revisao/`; use um prefixo novo.

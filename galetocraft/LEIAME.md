# Galetocraft (mod Fabric + GeckoLib)

Cocorídeos para o Minecraft **1.21.11**. O mod traz 12 espécies do Galetário com modelos GeckoLib: #001 Pirococó, #003 Esporocó, #004 Cocórak, #005 Cocórion, #006 Cocórvolt, #007 Taturico, #008 Axococó, #009 Vagaló, #010 Morcegalo, #011 Espinhocó, #012 Salambrasa e #019 Renacocó.

Por enquanto as criaturas só aparecem por ovo gerador ou `/summon`. A Rinha, a captura, os golpes e a reprodução ainda não estão implementados; as regras deles estão documentadas na base vigente (ver `../docs/CONHECIMENTO_GALETOCRAFT.md`).

Licença: todos os direitos reservados (ver `LICENSE`).

## Versões
| Item | Versão |
|---|---|
| Minecraft | 1.21.11 |
| Fabric Loader | 0.20.1 |
| Fabric API | 0.141.6+1.21.11 |
| GeckoLib (Fabric) | 5.4.5 |
| Java para rodar o Gradle | 25 (Eclipse Temurin), exigido pelo Loom 1.19 |
| Java do mod (alvo) | 21, o mesmo do Minecraft 1.21.11 |

## Compilar
No terminal, dentro desta pasta, com o Java 25 ativo:

```
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-25.0.5.8-hotspot
gradlew build
```

O arquivo do mod sai em `build/libs/galetocraft-0.1.0.jar`.

Para abrir o jogo de teste já com o mod: `gradlew runClient`.

## Jogar com o mod (instalação normal)
1. Instale o **Fabric Loader** para a 1.21.11 (https://fabricmc.net/use/installer/).
2. Coloque na pasta `mods` do Minecraft:
   - `galetocraft-0.1.0.jar` (deste projeto)
   - **Fabric API** para 1.21.11
   - **GeckoLib** (Fabric) 5.4.5 para 1.21.11
3. No jogo, os **ovos geradores** das 12 espécies ficam na aba de ovos geradores do modo criativo.

## Onde fica cada coisa
`<id>` é o nome técnico da espécie: `pirococo`, `esporoco`, `cocorak`, `cocorion`, `cocorvolt`, `taturico`, `axococo`, `vagalo`, `morcegalo`, `espinhoco`, `salambrasa` ou `renacoco`.

| O quê | Arquivo |
|---|---|
| Comportamento do Pirococó | `src/main/java/br/galetocraft/entidade/PirococoEntity.java` |
| Comportamento das demais espécies | `src/main/java/br/galetocraft/entidade/GaloEntity.java` |
| Registro das criaturas, da caixa de colisão, da vida, da velocidade e do dano | `src/main/java/br/galetocraft/registro/ModEntidades.java` |
| Registro dos ovos | `src/main/java/br/galetocraft/registro/` |
| Desenho, LOD e brilho | `src/client/java/br/galetocraft/client/` (`GaloRenderer`, `BrilhoParcialGeoLayer`) |
| Modelo 3D (formato GeckoLib/Bedrock) | `src/main/resources/assets/galetocraft/geckolib/models/entity/<id>.geo.json` |
| Animações (parado, andando) | `src/main/resources/assets/galetocraft/geckolib/animations/entity/<id>.animation.json` |
| Textura | `src/main/resources/assets/galetocraft/textures/entity/<id>.png` |
| Partes que brilham no escuro | `src/main/resources/assets/galetocraft/textures/entity/<id>_glowmask.png` |
| Nomes no jogo | `src/main/resources/assets/galetocraft/lang/pt_br.json` e `en_us.json` |

## Atualizar um modelo
Cada espécie tem um gerador em `../ferramentas/especies/<id>.py`. Na raiz do repositório, rode:

```
python ferramentas/especies/<id>.py
python ferramentas/exportar_especie.py <id>
```

1. O primeiro comando gera `modelos/<id>/<id>.bbmodel` e a máscara de brilho.
2. O segundo exporta o modelo, a animação e as texturas para o mod. Ele também otimiza o modelo e separa os ossos `_brilho` e `_lod`.
   - `--sem-otimizar` e `--sem-lod` desligam essas etapas.
   - `ferramentas/lod_auto.py <id>` recalcula `modelos/<id>/lods.json`.
3. Ovos e nomes de espécies novas são gerados por `ferramentas/registrar_especies.py`.

O fluxo antigo, com `pirococo6.py` e `exportar_geckolib.py`, está obsoleto. Esses scripts ficam só como histórico.

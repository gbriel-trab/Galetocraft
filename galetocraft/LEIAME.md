# Galetocraft (mod Fabric + GeckoLib)

Galos lendários para o Minecraft **1.21.11**. Criatura #001: **Pirococó**, o galo-fênix das chamas.

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
3. No jogo, o **Ovo Gerador de Pirococó** fica na aba de ovos geradores do modo criativo.

## Onde fica cada coisa
| O quê | Arquivo |
|---|---|
| Comportamento (vida, ataque, IA, sons) | `src/main/java/br/galetocraft/entidade/PirococoEntity.java` |
| Registro da criatura e do ovo | `src/main/java/br/galetocraft/registro/` |
| Desenho / brilho | `src/client/java/br/galetocraft/client/PirococoRenderer.java` |
| Modelo 3D (formato GeckoLib/Bedrock) | `src/main/resources/assets/galetocraft/geckolib/models/entity/pirococo.geo.json` |
| Animações (parado, andando) | `src/main/resources/assets/galetocraft/geckolib/animations/entity/pirococo.animation.json` |
| Textura | `src/main/resources/assets/galetocraft/textures/entity/pirococo.png` |
| Partes que brilham no escuro | `src/main/resources/assets/galetocraft/textures/entity/pirococo_glowmask.png` |
| Nome no jogo | `src/main/resources/assets/galetocraft/lang/pt_br.json` |

## Atualizar o modelo
O modelo é gerado do zero pelo script `../modelos/pirococo/gerar_pirococo.py`, que escreve a geometria,
a textura, o brilho e as animações já no formato do GeckoLib, valida tudo e grava as imagens de conferência.
Depois de mudar o script, rode (na raiz do repositório):

```
python modelos/pirococo/gerar_pirococo.py --instalar
```

O `--instalar` copia os quatro arquivos para `src/main/resources/assets/galetocraft`. Para conferir um modelo
sem o Blockbench, use `python ferramentas/render_geo.py modelo.geo.json textura.png saida.png`.

Também dá para editar direto no **Blockbench** (com o plugin *GeckoLib Animation Utils*): abra o
`pirococo.geo.json`, ajuste e exporte por cima do mesmo arquivo. As animações também podem ser
feitas no Blockbench, na aba **Animar**.
